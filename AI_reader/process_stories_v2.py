#!/usr/bin/env python3
"""
一次性处理 /tmp/stories_v2_15.txt 中的 15 篇故事:
  1. 拆分故事
  2. 写入对应 Cap 目录
  3. 更新 progress.json
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
PROGRESS_FILE = Path(__file__).resolve().parent / "progress.json"
EVAL_SCRIPT = PROJECT_ROOT / "difficulty_algorithm" / "evaluate_v2.py"
STORIES_FILE = Path("/tmp/stories_v2_15.txt")

# 篇幅映射
LENGTH_MAP = {"短篇": "brevis", "中篇": "medius", "长篇": "longus"}

def title_to_slug(title_la: str) -> str:
    """拉丁标题 → 文件名 slug"""
    # 保留字母、数字、空格，去掉标点
    slug = re.sub(r"[^A-Za-z0-9āēīōūȳĀĒĪŌŪȲ\s]", "", title_la)
    slug = slug.strip().replace(" ", "_")
    # 去重下划线
    slug = re.sub(r"_+", "_", slug)
    return slug

def next_number(chapter_dir: Path, target_chapter: int) -> str:
    """找到下一个可用的 NNN"""
    existing = list(chapter_dir.glob(f"Cap{target_chapter}_*_brevis_*.md"))
    existing += list(chapter_dir.glob(f"Cap{target_chapter}_*_medius_*.md"))
    existing += list(chapter_dir.glob(f"Cap{target_chapter}_*_longus_*.md"))

    max_n = 0
    for f in existing:
        match = re.search(r"_(\d{3})\.md$", f.name)
        if match:
            n = int(match.group(1))
            if n > max_n:
                max_n = n
    return f"{max_n + 1:03d}"

def split_stories(text: str) -> list[dict]:
    """拆分多篇故事，返回 (meta, latin_text) 列表"""
    parts = text.strip().split("---")
    stories = []
    i = 0
    while i < len(parts):
        # 找 YAML 头
        yaml_block = parts[i].strip() if i < len(parts) else ""
        i += 1
        if not yaml_block or "story_id" not in yaml_block:
            continue

        # 找正文（下一个 --- 之前的内容）
        body = ""
        while i < len(parts):
            block = parts[i].strip()
            i += 1
            if "story_id" in block:
                # 这是下一篇的 YAML 头，回退
                i -= 1
                break
            body += block + "\n"

        body = body.strip()
        if not body:
            continue

        # 解析 YAML 字段
        meta = {}
        for field in ["story_id", "title_la", "title_zh", "target_chapter",
                      "theme", "style", "genre", "character_type", "length_tier",
                      "narrative_mode", "word_count", "macrons_status"]:
            match = re.search(rf"^{field}:\s*(.+?)$", yaml_block, re.MULTILINE)
            if match:
                val = match.group(1).strip().strip("\"'")
                if field in ("target_chapter", "word_count"):
                    try:
                        val = int(val)
                    except ValueError:
                        pass
                meta[field] = val

        if not meta.get("story_id"):
            continue

        stories.append((meta, body))
    return stories

def evaluate_text(latin_text: str) -> dict:
    """调用 evaluate_v2.py 评估"""
    result = subprocess.run(
        ["python3", str(EVAL_SCRIPT), "--text", latin_text, "--json"],
        capture_output=True, text=True, timeout=60,
        cwd=str(EVAL_SCRIPT.parent)
    )
    if result.returncode != 0:
        print(f"  [WARN] evaluate_v2.py 失败: {result.stderr[:200]}", file=sys.stderr)
        return {"v2_level": None, "v2_best_fit": None, "v2_rate": 0, "v2_oov": []}

    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)
    return {"v2_level": None, "v2_best_fit": None, "v2_rate": 0, "v2_oov": []}

def build_front_matter(meta: dict, eval_result: dict) -> str:
    """构建完整的 YAML Front Matter"""
    now = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                         capture_output=True, text=True).stdout.strip()
    effective_ch = eval_result.get("v2_level") or eval_result.get("v2_best_fit")
    lines = [
        "---",
        f'story_id: "{meta["story_id"]}"',
        f'title_la: "{meta["title_la"]}"',
        f'title_zh: "{meta["title_zh"]}"',
        f'target_chapter: {meta["target_chapter"]}',
        f'evaluated_chapter: {effective_ch if effective_ch else "null"}',
        f'theme: "{meta["theme"]}"',
        f'style: "{meta["style"]}"',
        f'genre: "{meta["genre"]}"',
        f'character_type: "{meta["character_type"]}"',
        f'length_tier: "{meta["length_tier"]}"',
        f'narrative_mode: "{meta["narrative_mode"]}"',
        f'word_count: {meta["word_count"]}',
        f'macrons_status: "{meta["macrons_status"]}"',
        f'v2_rate: {eval_result.get("v2_rate", 0)}',
        f'v2_oov: {json.dumps(eval_result.get("v2_oov", []), ensure_ascii=False)}',
        f'created_at: "{now}"',
        f'updated_at: "{now}"',
        f'status: "active"',
        "---",
    ]
    return "\n".join(lines)

def main():
    # 读取故事
    text = STORIES_FILE.read_text(encoding="utf-8")
    stories = split_stories(text)
    print(f"共解析 {len(stories)} 篇故事")

    # 加载 progress.json
    progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))

    # 更新进度
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    batch_id = f"batch_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    batch_record = {
        "batch_id": batch_id,
        "phase": "fill_gaps",
        "target_chapters": [5, 7, 8],
        "stories": [],
        "completed_at": now
    }

    for meta, body in stories:
        chap = str(meta["target_chapter"])
        story_id = meta["story_id"]
        print(f"\n处理: {story_id} → Cap.{chap}")

        # 评估
        eval_result = evaluate_text(body)
        v2_level = eval_result.get("v2_level") or eval_result.get("v2_best_fit")
        v2_rate = eval_result.get("v2_rate", 0)
        print(f"  算法评估: v2_rate={v2_rate}%, v2_level={v2_level}")

        # 确保目录存在
        cap_dir = REALITATES_DIR / f"Cap{chap}"
        cap_dir.mkdir(parents=True, exist_ok=True)

        # 找下一个编号
        nnn = next_number(cap_dir, meta["target_chapter"])

        # 构建文件名
        slug = title_to_slug(meta["title_la"])
        length_la = LENGTH_MAP.get(meta.get("length_tier", "短篇"), "brevis")
        filename = f"Cap{chap}_{slug}_{length_la}_{nnn}.md"
        filepath = cap_dir / filename

        # 构建文件内容
        front_matter = build_front_matter(meta, eval_result)
        content = f"{front_matter}\n\n{body}\n"

        # 写入文件
        filepath.write_text(content, encoding="utf-8")
        print(f"  写入: {filepath.name}")

        # 更新 progress.json
        if chap not in progress["chapters"]:
            progress["chapters"][chap] = {
                "done": 0, "target": 10, "need": 10,
                "strategy": "standard",
                "used_dimensions": {"themes": [], "styles": [], "genres": [], "characters": [], "narratives": []}
            }

        ch_data = progress["chapters"][chap]
        ch_data["done"] = ch_data.get("done", 0) + 1
        ch_data["need"] = max(0, ch_data["target"] - ch_data["done"])

        dims = ch_data["used_dimensions"]
        dims["themes"].append(meta.get("theme", ""))
        dims["styles"].append(meta.get("style", ""))
        dims["genres"].append(meta.get("genre", ""))
        dims["characters"].append(meta.get("character_type", ""))
        dims["narratives"].append(meta.get("narrative_mode", ""))

        batch_record["stories"].append({
            "story_id": story_id,
            "title_la": meta["title_la"],
            "target_chapter": meta["target_chapter"],
            "evaluated_chapter": v2_level,
            "file": filename
        })

    # 写入 progress.json
    progress["batches"].append(batch_record)
    progress["last_updated"] = now
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")

    # 汇总
    print(f"\n{'='*60}")
    print(f"处理完成! 批次: {batch_id}")
    for ch in ["5", "7", "8"]:
        if ch in progress["chapters"]:
            d = progress["chapters"][ch]
            print(f"  Cap.{ch}: {d['done']}/{d['target']} (尚需 {d['need']})")
    print(f"progress.json 已更新")

if __name__ == "__main__":
    main()