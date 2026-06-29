#!/usr/bin/env python3
"""
迁移脚本 v1_0_0
从 /tmp/story_audit_report.csv 读取错位故事，按算法实测章节迁移：
  1. 移动文件到 algo_chapter 对应目录
  2. 修正文件名中的 Cap 前缀
  3. 更新 YAML front matter 中 target_chapter
  4. 更新 progress.json
"""

import csv
import json
import re
import shutil
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
AUDIT_CSV = Path("/tmp/story_audit_report.csv")
PROGRESS_FILE = Path(__file__).resolve().parent / "progress.json"

def find_next_number(target_dir: Path, cap_num: int) -> int:
    """找到目录中的最大序号 + 1"""
    max_n = 0
    for f in target_dir.glob(f"Cap{cap_num}_*_*.md"):
        m = re.search(r"_(\d{3})\.md$", f.name)
        if m:
            n = int(m.group(1))
            if n > max_n:
                max_n = n
    return max_n + 1

def main():
    # 1. 读审计 CSV
    rows = []
    with open(AUDIT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            severity = row.get("severity", "")
            if severity in ("MODERATE", "SEVERE"):
                rows.append(row)

    print(f"从审计报告找到 {len(rows)} 篇需迁移的故事\n")

    # 2. 加载 progress.json
    progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))

    migrations = []  # (from_path, to_path, old_ch, new_ch, title_la)
    skipped = []

    for row in rows:
        filename = row["file"]
        source_dir = row["dir"]
        target_ch = int(row["target_chapter"])
        algo_ch = int(row["algo_chapter"])
        severity = row["severity"]
        title_la = row.get("title_la", "")

        # 如果算法章 = 目标章，跳过（实际上不该发生，但安全起见）
        if algo_ch == target_ch:
            skipped.append((filename, "already correct"))
            continue

        source_path = REALITATES_DIR / source_dir / filename
        if not source_path.exists():
            skipped.append((filename, "file not found"))
            continue

        # 目标目录
        target_dir_name = f"Cap{algo_ch}"
        target_dir = REALITATES_DIR / target_dir_name
        target_dir.mkdir(parents=True, exist_ok=True)

        # 新文件名：替换 Cap 前缀 + 重新编号
        # 原文件名格式: Cap{N}_{title}_{length}_{NNN}.md
        new_nnn = find_next_number(target_dir, algo_ch)
        # 把 Cap{N}_ 替换为 Cap{algo_ch}_
        new_filename = re.sub(r"^Cap\d+_", f"Cap{algo_ch}_", filename)
        # 替换序号部分
        new_filename = re.sub(r"_(\d{3})\.md$", f"_{new_nnn:03d}.md", new_filename)
        target_path = target_dir / new_filename

        # 避免覆盖已存在的文件
        if target_path.exists():
            # 用原编号 + 偏移
            new_filename = re.sub(r"_(\d{3})\.md$", f"_{new_nnn + 100:03d}.md", new_filename)
            target_path = target_dir / new_filename

        migrations.append((source_path, target_path, target_ch, algo_ch, title_la, severity))

    # 3. 执行迁移
    print(f"{'='*70}")
    print(f"执行迁移 ({len(migrations)} 篇):")
    print(f"{'='*70}")

    for src, dst, old_ch, new_ch, title, sev in migrations:
        # 3a. 读取文件内容
        content = src.read_text(encoding="utf-8")

        # 3b. 更新 target_chapter
        content = re.sub(
            r"(target_chapter:\s*)\d+",
            f"\\g<1>{new_ch}",
            content
        )

        # 3c. 写入目标位置
        dst.write_text(content, encoding="utf-8")
        print(f"  [{sev:>8s}] {src.parent.name}/{src.name}")
        print(f"           → {dst.parent.name}/{dst.name}  (Cap.{old_ch} → Cap.{new_ch})")

        # 3d. 删除源文件
        src.unlink()

    # 4. 更新 progress.json
    # 重新统计各章数量
    chapter_counts = defaultdict(int)
    chapter_dims = defaultdict(lambda: {"themes": [], "styles": [], "genres": [], "characters": [], "narratives": []})

    for cap_dir in sorted(REALITATES_DIR.glob("Cap*")):
        if not cap_dir.is_dir():
            continue
        cap_name = cap_dir.name
        for md_file in sorted(cap_dir.glob("*.md")):
            chapter_counts[cap_name] += 1
            # 提取维度
            text = md_file.read_text(encoding="utf-8")
            yaml_match = re.search(r"---\n(.*?)\n---", text, re.DOTALL)
            if yaml_match:
                yb = yaml_match.group(1)
                for dim in ["theme", "style", "genre", "character_type", "narrative_mode"]:
                    dm = re.search(rf"^{dim}:\s*\"?(.+?)\"?$", yb, re.MULTILINE)
                    if dm:
                        val = dm.group(1).strip().strip("\"'")
                        if dim == "character_type":
                            chapter_dims[cap_name]["characters"].append(val)
                        elif dim == "narrative_mode":
                            chapter_dims[cap_name]["narratives"].append(val)
                        else:
                            chapter_dims[cap_name][dim + "s"].append(val)

    # 重建 chapters
    for cap_name in list(progress["chapters"].keys()):
        ch_num = int(re.sub(r"\D", "", cap_name) or 0)
        count = chapter_counts.get(cap_name, 0)
        progress["chapters"][cap_name]["done"] = count
        progress["chapters"][cap_name]["need"] = max(0, progress["chapters"][cap_name]["target"] - count)
        if cap_name in chapter_dims:
            progress["chapters"][cap_name]["used_dimensions"] = dict(chapter_dims[cap_name])

    # 添加新出现的章节
    for cap_name, count in chapter_counts.items():
        if cap_name not in progress["chapters"]:
            ch_num = int(re.sub(r"\D", "", cap_name) or 0)
            progress["chapters"][cap_name] = {
                "done": count,
                "target": 10,
                "need": max(0, 10 - count),
                "strategy": "standard",
                "used_dimensions": dict(chapter_dims.get(cap_name, {}))
            }

    from datetime import datetime, timezone
    progress["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")

    # 5. 汇总
    print(f"\n{'='*70}")
    print("迁移完成!")
    print(f"  成功迁移: {len(migrations)} 篇")
    print(f"  跳过: {len(skipped)} 篇")

    # 显示受影响的章节
    affected = set()
    for _, _, old_ch, new_ch, _, _ in migrations:
        affected.add(old_ch)
        affected.add(new_ch)

    print("\n受影响章节当前状态:")
    for ch in sorted(affected):
        cn = f"Cap{ch}"
        count = chapter_counts.get(cn, 0)
        print(f"  {cn}: {count} 篇")

    print(f"\nprogress.json 已更新")


if __name__ == "__main__":
    main()
