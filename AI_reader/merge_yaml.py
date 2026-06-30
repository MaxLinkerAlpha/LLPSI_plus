#!/usr/bin/env python3
"""
merge_yaml.py v2_11_0 — 合并AI输出的12字段YAML与evaluate_v2.py评估结果 + AI 审查，输出MD Front Matter格式 + 维护realitates.json索引。

管线位置：Step 4 — AI生成后 → evaluate_v2.py评估 → ai_review.py审查（可选） → merge_yaml.py合并 → 入库

v2_11_0 变更（相对 v2_10_0）：
  - 路径重命名：realites → realitates（修正拉丁语拼写错误）
  - 函数 update_realites_index → update_realitates_index

v2_10_0 变更（相对 v2_9_0）：
  - 新增 --review / --review-ai-command / --review-strict 三参数
  - 在 evaluate_v2.py 之后、写入文件之前，调用 ai_review.py 做长音/用词/古典性审查
  - 审查结果（macrons_issues / vocabulary_issues / classical_issues / verdict）
    追加到 YAML Front Matter（字段：ai_review）
  - --review-strict：verdict="fail" 时跳过该篇（不写入文件）
  - 采纳"评估打标"哲学：审查结果是观察，不是约束
  - 配合 generate_prompt.py v1_5_0 的「grammar 自由使用」+「vocab 清洗版」

v2_9_0 变更（相对 v2_8_0）：
  - 暂停自动调用 auto_supplement_map.py（v2_8_0 的"入库后自动分析"已取消）
  - 原因：当前样本量 34 OOV 词，自动建议准确率仅约 50%（centuriō、Morta 等近邻推断错）
  - 改方案：方案C — 生成冗余 + 自动筛选（一次生成 5+ 篇，每篇自动归到真实难度文件夹，人工从同章节择优）
  - OOV 数据继续在 oov_corrections.jsonl 累积，积累到 20+ 唯一词后人工批量审核

v2_8_0 变更（相对 v2_7_0）：
  - 入库完成自动调用 auto_supplement_map.py 做 OOV 增量分析（方案D 自动化）
  - 建议写入 AI_reader/supplement_suggestions.jsonl（不直接修改映射表）

v2_7_0 变更（相对 v2_6_0）：
  - target_chapter 自动校准：用算法实测章节覆盖 AI 声明，保证YAML精准性
  - 新增 log_oov()：每次入库把 OOV 词追加到 oov_corrections.jsonl（方案D 数据闭环）
  - 合并字段顺序按"AI 声明 → 算法实测 → 元数据"分组

v2_6_0 变更（相对 v2_5_0）：
  - 命名规范全面拉丁化：Cap{N}_{title_slug}_{length_la}_{NNN}.md
  - 四要素：难度章节 + 拉丁语标题 + 篇幅拉丁标识 + 序号
  - 篇幅标识：短篇→brevis 中篇→medius 长篇→longus
  - 新增 title_to_slug()、LENGTH_TIER_LA 映射表
  - next_story_filename() 签名变更：增加 title_la 参数

v2_3_0 变更（相对 v2_2_0）：
  - 默认输出目录：stories/  →  realitates/
  - 索引文件：stories.json  →  realitates.json
  - 函数 update_stories_index()  →  update_realitates_index()

v2_0_0 变更（相对 v1_0_0）：
  - 输出格式：纯YAML 文本  →  MD文件（YAML Front Matter + 拉丁语正文）
  - 默认文件命名：realitates/Cap{N}_{NNN}.md（N=目标章节，NNN=三位递增序号）
  - 新增 --output-dir（默认 realitates/）与 --auto-number（默认 true）参数
  - 每次运行后自动维护 realitates.json 索引（仅文件名清单，~2KB）

用法：
    # 默认行为：自动编号写入 realitates/Cap{N}_{NNN}.md
    cat ai_output.txt | python AI_reader/merge_yaml.py

    # 从文件读取
    python AI_reader/merge_yaml.py --file ai_output.txt

    # 显式指定输出文件（向后兼容）
    python AI_reader/merge_yaml.py --file ai_output.txt --output my_story.md

    # 关闭自动编号 + 自定义输出目录
    python AI_reader/merge_yaml.py --file ai_output.txt --output-dir /tmp/realitates --auto-number=false

    # 输出到 stdout（保持旧行为，便于管道传递）
    python AI_reader/merge_yaml.py --file ai_output.txt --stdout

输出：MD文件（YAML Front Matter + 拉丁语正文），或 stdout（使用 --stdout 时）

依赖：Python 3.9+（无外部pip依赖）。需要 ../difficulty_algorithm/evaluate_v2.py 及其数据文件。
"""

import sys
import json
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# 常量
# ============================================================

AI_KNOWN_FIELDS = [
    "story_id", "title_la", "title_zh", "target_chapter",
    "theme", "style", "genre", "character_type", "length_tier",
    "narrative_mode", "word_count", "macrons_status"
]

EVAL_SCRIPT_NAME = "evaluate_v2.py"
EVAL_TIMEOUT = 60  # 秒

# ============================================================
# 解析AI输出
# ============================================================

def parse_ai_output(text: str) -> tuple[dict, str]:
    """从单段 AI 输出中分离 YAML 元数据头（12字段）和拉丁语正文。

    返回：(meta_dict, latin_text)
    容错：YAML字段缺失不报错，只记录缺失项。

    注意：本函数假定 text 只包含 1 个故事的 YAML头+正文。
    多篇故事应先用 split_into_stories() 拆分。
    """
    # 按 --- 分隔符拆分
    parts = text.split("---")
    if len(parts) < 2:
        raise ValueError("无法解析AI输出：未找到YAML头（缺少 --- 分隔符）。"
                         "AI输出格式应为：---\n字段: 值\n---\n拉丁语正文")

    yaml_block = parts[1]
    latin_text = "---".join(parts[2:]).strip()

    if not latin_text:
        raise ValueError("拉丁语正文为空。请检查AI输出是否包含正文。")

    meta = {}
    for field in AI_KNOWN_FIELDS:
        # 匹配 "field: value" 或 'field: "value"' 格式
        match = re.search(rf"^{field}:\s*(.+?)$", yaml_block, re.MULTILINE)
        if match:
            val = match.group(1).strip().strip("\"'")
            if field in ("target_chapter", "word_count"):
                try:
                    val = int(val)
                except ValueError:
                    pass  # 保持字符串，不阻塞管线
            meta[field] = val

    # 如果 story_id 未生成或为空模板，自动生成 UUID
    if not meta.get("story_id") or meta["story_id"] in ("auto_generated_uuid", ""):
        meta["story_id"] = str(uuid.uuid4())

    # 重新核算 word_count（以实际分词为准，不信任AI自报）
    tokens = [t for t in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", latin_text) if len(t) >= 2]
    meta["word_count"] = len(tokens)

    missing = [f for f in AI_KNOWN_FIELDS if f not in meta]
    if missing:
        print(f"[merge_yaml] 警告：YAML头缺失字段 {missing}，将继续合并。", file=sys.stderr)

    return meta, latin_text


def split_into_stories(text: str) -> list:
    """将多篇 AI 输出拆分为单篇段落列表。

    AI 输出格式：每个故事以 "---" 开头（YAML 头标记），紧跟字段行，再以 "---" 结束 YAML 头，
    然后是拉丁语正文。下一篇故事以前导 "---" 重新开始。

    算法：使用行级扫描，跟踪是否在 YAML 头内。每遇到「行首 --- 且行尾 ---」切分为单段。

    Returns:
        list[str] - 每个元素是单篇故事的完整文本（以 --- 开头）。
        若无法拆分出至少 1 个故事，返回 [text]（单篇兜底）。
    """
    lines = text.splitlines()
    stories: list = []
    current: list = []
    in_yaml = False
    yaml_close_seen = False

    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_yaml:
                # 新的 YAML 头开始
                if current:
                    # 前一段有内容 → 入栈
                    stories.append("\n".join(current).strip())
                    current = []
                in_yaml = True
                yaml_close_seen = False
                current.append(line)
            elif not yaml_close_seen:
                # YAML 头结束
                current.append(line)
                in_yaml = False
                yaml_close_seen = True
            else:
                # 已经关闭后再次遇到 ---，视为新故事的 YAM 头
                if current:
                    stories.append("\n".join(current).strip())
                    current = []
                in_yaml = True
                yaml_close_seen = False
                current.append(line)
        else:
            current.append(line)

    if current:
        stories.append("\n".join(current).strip())

    # 过滤空段
    stories = [s for s in stories if s and "story_id" in s]
    if not stories:
        return [text]  # 兜底：原样返回
    return stories


# ============================================================
# 调用 evaluate_v2.py
# ============================================================

def find_eval_script() -> Path:
    """定位 evaluate_v2.py 脚本路径。"""
    # 相对于 merge_yaml.py 的路径：../difficulty_algorithm/evaluate_v2.py
    script_dir = Path(__file__).resolve().parent
    candidate = script_dir.parent / "difficulty_algorithm" / EVAL_SCRIPT_NAME
    if candidate.exists():
        return candidate
    # 备选：当前工作目录
    cwd_candidate = Path.cwd() / "difficulty_algorithm" / EVAL_SCRIPT_NAME
    if cwd_candidate.exists():
        return cwd_candidate
    raise FileNotFoundError(
        f"找不到 {EVAL_SCRIPT_NAME}。"
        f"尝试了：{candidate}、{cwd_candidate}"
    )


def evaluate_text(latin_text: str) -> dict:
    """调用 evaluate_v2.py --text --json 评估拉丁语文本难度。

    返回：evaluate_v2.py 的 JSON 输出（dict）。
    """
    eval_script = find_eval_script()
    cwd = str(eval_script.parent)

    result = subprocess.run(
        ["python3", str(eval_script), "--text", latin_text, "--json"],
        capture_output=True, text=True, timeout=EVAL_TIMEOUT,
        cwd=cwd
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"evaluate_v2.py 执行失败（exit={result.returncode}）。\n"
            f"stderr: {result.stderr[:500]}"
        )

    # evaluate_v2.py 的 JSON 输出是唯一一行（stderr 上的日志已过滤）
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("{"):
            return json.loads(line)

    raise RuntimeError(
        f"evaluate_v2.py 未返回JSON。stdout前200字符: {result.stdout[:200]}"
    )


# ============================================================
# 调用 ai_review.py
# ============================================================

AI_REVIEW_SCRIPT = "ai_review.py"
AI_REVIEW_TIMEOUT = 240  # 秒（免费 AI 慢一些）


def find_ai_review_script() -> Path:
    """定位 ai_review.py 脚本路径。"""
    script_dir = Path(__file__).resolve().parent
    candidate = script_dir / AI_REVIEW_SCRIPT
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        f"找不到 {AI_REVIEW_SCRIPT}。"
        f"尝试了：{candidate}"
    )


def run_ai_review(
    latin_text: str, chapter: int, ai_command: str,
    tmp_dir: Path, story_id: str
) -> dict:
    """调用 ai_review.py 做 macrons / 用词 / 古典性审查。

    Args:
        latin_text: 拉丁语正文
        chapter: 目标章节（用于 prompt 中的 Cap.N 匹配检查）
        ai_command: AI 后端 shell 命令
        tmp_dir: 临时文件存放目录
        story_id: 故事 ID（用于临时文件命名）

    Returns:
        ai_review.py 返回的 review dict（含 macrons_issues / verdict / etc.）
    """
    review_script = find_ai_review_script()

    # 把故事正文写到临时文件
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_story = tmp_dir / f"_review_{story_id[:8]}.md"
    tmp_story.write_text(
        f"---\nstory_id: \"{story_id}\"\n---\n\n{latin_text}\n",
        encoding="utf-8"
    )

    try:
        result = subprocess.run(
            [
                "python3", str(review_script),
                "--story", str(tmp_story),
                "--chapter", str(chapter),
                "--ai-command", ai_command,
                "--timeout", str(AI_REVIEW_TIMEOUT),
            ],
            capture_output=True, text=True, timeout=AI_REVIEW_TIMEOUT
        )

        if result.returncode not in (0, 1, 2):
            # 0=pass, 1=needs_fixes, 2=fail —— 这三个都是预期的退出码
            raise RuntimeError(
                f"ai_review.py 异常退出（exit={result.returncode}）。\n"
                f"stderr: {result.stderr[:500]}"
            )

        # ai_review.py 输出 JSON 到 stdout
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)

        raise RuntimeError(
            f"ai_review.py 未返回 JSON。stdout 前 200 字符: {result.stdout[:200]}"
        )
    finally:
        # 清理临时文件
        if tmp_story.exists():
            tmp_story.unlink()


# ============================================================
# 合并
# ============================================================

def merge(ai_meta: dict, eval_result: dict) -> dict:
    """合并AI的12字段 + evaluate_v2.py的评估结果 → 完整元数据dict。

    分组顺序：
      A. AI 声明（12 字段，由 AI 生成时自报）
      B. 算法实测（6 字段，由 evaluate_v2.py 计算）
      C. 元数据（created_at / updated_at / status）
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # 降级时 v2_level 为 null，用 v2_best_fit 兜底
    effective_chapter = eval_result.get("v2_level") or eval_result.get("v2_best_fit")
    # 用算法实测的章节覆盖 AI 声明的 target_chapter（保证YAML精准性）
    ai_meta_corrected = {**ai_meta}
    if isinstance(effective_chapter, int) and effective_chapter > 0:
        ai_meta_corrected["target_chapter"] = effective_chapter
    merged = {
        # A. AI 声明（target_chapter 已被算法实测覆盖）
        **ai_meta_corrected,
        # B. 算法实测
        "evaluated_chapter": eval_result.get("v2_level"),
        "best_fit_chapter": eval_result.get("v2_best_fit"),
        "coverage_rate": eval_result.get("v2_rate"),
        "oov_words": eval_result.get("v2_oov", []),
        "top_10_lemmas": None,
        "grammar_features": None,
        # C. 元数据
        "created_at": now,
        "updated_at": now,
        "status": "evaluated"
    }
    return merged, effective_chapter


# ============================================================
# 输出
# ============================================================

def output_md(merged: dict, latin_text: str) -> str:
    """生成 MD 文件内容：YAML Front Matter + 拉丁语正文。

    格式：
        ---
        story_id: ...
        title_la: ...
        ...（所有19字段，按原顺序）
        ---

        [拉丁语正文，每段用空行分隔]

    与 v1_0_0 区别：v1 是纯YAML+正文同文本；v2 是MD文件，Front Matter用 --- 包围，
    YAML字段值用双引号包裹保持向后兼容，正文与 Front Matter 之间空一行。
    """
    lines = ["---"]
    for key, value in merged.items():
        if isinstance(value, str):
            # 用双引号包裹并转义 YAML 特殊字符
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{key}: "{escaped}"')
        elif isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        elif value is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")  # Front Matter 与正文之间空一行
    lines.append(latin_text)
    return "\n".join(lines) + "\n"


# 向后兼容：保留旧函数名为 output_md 的别名
def output_yaml(merged: dict, latin_text: str) -> str:
    """[已弃用] 旧版本输出函数，等价于 output_md。保留以防有外部调用。"""
    return output_md(merged, latin_text)


LENGTH_TIER_LA = {
    "短篇": "brevis",
    "中篇": "medius",
    "长篇": "longus",
}


def title_to_slug(title_la: str) -> str:
    """将拉丁语标题转为文件名安全 slug。

    规则：保留字母数字，空格/标点替换为下划线，去重下划线，去除首尾下划线。
    示例："Taberna Speī" → "Taberna_Spei"
    """
    slug = re.sub(r"[^A-Za-z0-9\u0100-\u017F]+", "_", title_la)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "sine_titulo"


def next_story_filename(
    output_dir: Path, chapter: int, title_la: str, length_tier: str = "短篇"
) -> Path:
    """生成下一个故事文件名：Cap{N}_{title_slug}_{length_la}_{NNN}.md。

    文件存放于 {output_dir}/Cap{N}/ 子目录下。
    命名要素（均拉丁文）：
      - Cap{N}：难度章节
      - title_slug：文章拉丁语标题（空格转下划线）
      - length_la：篇幅标识（brevis/medius/longus）
      - NNN：三位递增序号

    算法：扫描该子目录下所有匹配 Cap{N}_*_*_NNN.md 的文件，
    提取 NNN 编号最大值 + 1，三位补零。
    目录不存在则自动创建。
    """
    if not isinstance(chapter, int) or chapter <= 0:
        raise ValueError(f"chapter 必须为正整数，当前值: {chapter!r}")
    chapter_dir = output_dir / f"Cap{chapter}"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    title_slug = title_to_slug(title_la)
    length_la = LENGTH_TIER_LA.get(length_tier, "brevis")
    pattern = re.compile(rf"^Cap{chapter}_.*_.*_(\d+)\.md$")
    max_n = 0
    for p in chapter_dir.iterdir():
        m = pattern.match(p.name)
        if m:
            n = int(m.group(1))
            if n > max_n:
                max_n = n
    next_n = max_n + 1
    return chapter_dir / f"Cap{chapter}_{title_slug}_{length_la}_{next_n:03d}.md"


def update_realitates_index(ai_reader_dir: Path, entry: dict) -> None:
    """追加或更新 realitates.json 索引条目。

    路径：{ai_reader_dir}/realitates.json
    格式：[{"path": "realitates/Cap10_001.md", "chapter": 10, "title_zh": "..."}, ...]
    去重：以 path 为唯一键，更新该条目的所有字段。
    排序：按 (chapter, path) 升序。
    """
    index_path = ai_reader_dir / "realitates.json"
    items: list = []
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, list):
                items = loaded
            else:
                print(f"[merge_yaml] 警告：realitates.json 顶层不是数组，重建为空列表。",
                      file=sys.stderr)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[merge_yaml] 警告：realitates.json 读取失败（{e}），重建为空列表。",
                  file=sys.stderr)

    # 去重：以 path 为键
    new_path = entry.get("path")
    items = [it for it in items if it.get("path") != new_path]
    items.append(entry)

    # 排序：先按 chapter，再按 path
    items.sort(key=lambda it: (it.get("chapter", 0), it.get("path", "")))

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")


def log_oov(ai_reader_dir: Path, story_path: str, oov_list: list, target_chapter: int) -> None:
    """把 OOV 词追加写到 oov_corrections.jsonl（方案D 数据闭环）。

    每行一个 JSON 对象：
      {"ts": "...", "path": "...", "target": 8, "oov": ["..."]}
    用于后续人工审核 + 批量补充 lemma_chapter_map.json。
    """
    if not oov_list:
        return
    log_path = ai_reader_dir / "oov_corrections.jsonl"
    entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": story_path,
        "target": target_chapter,
        "oov": sorted(set(oov_list)),
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ============================================================
# 校验（validate 子命令）
# ============================================================

# 必填字段：故事生成 + 索引维护必须的最小集
REQUIRED_FIELDS = (
    "title_la", "title_zh", "target_chapter",
    "theme", "style", "genre", "character_type", "length_tier",
    "narrative_mode",
)

# 推荐字段：有则更好（如缺不影响主流程）
RECOMMENDED_FIELDS = (
    "story_id", "word_count", "macrons_status",
)


def validate_output(text: str) -> int:
    """校验 AI 输出格式合法性。

    检查项：
      1. 必含 --- 分隔符（YAML 头标记）
      2. 拉丁语正文非空
      3. 9 个必填字段全部存在且非空
      4. target_chapter 为 1-34 整数
      5. macrons_status 为合法值

    Returns:
        0 = 校验通过
        1 = 校验失败
    """
    errors = []
    warnings = []

    if not text or not text.strip():
        print("[validate] 错误：输入为空。")
        return 1

    parts = text.split("---")
    if len(parts) < 2:
        errors.append("未找到 YAML 头（缺少 --- 分隔符）。"
                      "AI 输出应形如：---\n字段: 值\n---\n正文")
    else:
        yaml_block = parts[1]
        latin_text = "---".join(parts[2:]).strip()

        if not latin_text:
            errors.append("拉丁语正文为空（--- 之后无内容）。")

        for field in REQUIRED_FIELDS:
            match = re.search(rf"^{field}:\s*(.+?)$", yaml_block, re.MULTILINE)
            if not match:
                errors.append(f"必填字段缺失: {field}")
            else:
                val = match.group(1).strip().strip("\"'")
                if not val or val in ("null", "None"):
                    errors.append(f"必填字段为空: {field}")

        m = re.search(r"^target_chapter:\s*(\d+)\s*$", yaml_block, re.MULTILINE)
        if m:
            try:
                ch = int(m.group(1))
                if not 1 <= ch <= 34:
                    errors.append(
                        f"target_chapter={ch} 超出范围（LLPSI 共 1-34 章）。"
                    )
            except ValueError:
                errors.append(f"target_chapter 不是整数: {m.group(1)}")

        m = re.search(r"^macrons_status:\s*\"?(\w+)\"?\s*$", yaml_block, re.MULTILINE)
        if m:
            v = m.group(1).strip().strip("\"'")
            if v not in ("generated", "verified", "pending"):
                warnings.append(
                    f"macrons_status={v!r} 不在推荐值内（generated/verified/pending）。"
                )

        for field in RECOMMENDED_FIELDS:
            if not re.search(rf"^{field}:", yaml_block, re.MULTILINE):
                warnings.append(f"推荐字段缺失（将自动补全）: {field}")

    if errors:
        print(f"[validate] 失败：发现 {len(errors)} 个错误：")
        for e in errors:
            print(f"  ✗ {e}")
        if warnings:
            print(f"\n[validate] 附加 {len(warnings)} 个警告：")
            for w in warnings:
                print(f"  ⚠ {w}")
        return 1
    else:
        print(f"[validate] 通过：所有必填字段齐全，格式合法。")
        if warnings:
            print(f"\n[validate] {len(warnings)} 个警告（不阻塞）：")
            for w in warnings:
                print(f"  ⚠ {w}")
        return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="合并AI生成的12字段YAML与evaluate_v2.py评估结果，输出MD Front Matter格式。"
    )
    parser.add_argument(
        "--file", "-f",
        help="AI输出文件路径。不提供则从 stdin 读取。"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出文件路径。指定后忽略 --output-dir / --auto-number，仍会更新 realitates.json。"
    )
    parser.add_argument(
        "--output-dir",
        default="realitates",
        help="自动编号模式下的输出目录（相对 AI_reader/）。默认 realitates/。"
    )
    parser.add_argument(
        "--auto-number",
        type=lambda s: s.lower() not in ("false", "0", "no"),
        default=True,
        help="自动按 Cap{N}_{NNN}.md 编号写入。默认 true；传入 false 关闭。"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="输出到 stdout（v1 旧行为，便于管道传递）。与 --output 互斥。"
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="启用 AI 审查流程（macrons / 用词 / 古典性）。"
             "需要同时指定 --review-ai-command。"
    )
    parser.add_argument(
        "--review-ai-command",
        default="",
        help="AI 审查后端 shell 命令（传给 ai_review.py 的 --ai-command）。"
             "例如：'ollama run llama3.1' 或 'curl ...'"
    )
    parser.add_argument(
        "--review-strict",
        action="store_true",
        help="AI 审查 verdict=fail 时跳过该篇（不写入文件）。默认仅记录审查结果。"
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # validate 子命令：仅校验 AI 输出的 YAML 头合法性，不写文件
    validate_parser = subparsers.add_parser(
        "validate", help="校验 AI 输出（YAML 头格式 + 必要字段），不写文件"
    )
    validate_parser.add_argument(
        "--file", "-f",
        help="AI输出文件路径。不提供则从 stdin 读取。"
    )

    # print subcommand usage if no command given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # validate 子命令处理
    if args.command == "validate":
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()
        sys.exit(validate_output(raw))

    # 1. 读取输入
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        print("[merge_yaml] 错误：输入为空。", file=sys.stderr)
        sys.exit(1)

    # 2. 拆分多篇故事（单篇时返回 [raw]，循环可统一处理）
    stories = split_into_stories(raw)
    n = len(stories)
    print(f"[merge_yaml] 检测到 {n} 篇故事，开始批量处理...", file=sys.stderr)

    if n == 0:
        print("[merge_yaml] 错误：未检测到任何故事（YAML 头缺失或字段不全）。", file=sys.stderr)
        sys.exit(1)

    # script_dir 在循环外预先解析，供 auto-number 模式与索引维护使用
    script_dir = Path(__file__).resolve().parent

    # 3-N. 逐篇处理
    for i, story in enumerate(stories, 1):
        print(f"\n[merge_yaml] [{i}/{n}] 解析中...", file=sys.stderr)
        try:
            ai_meta, latin_text = parse_ai_output(story)
        except ValueError as e:
            print(f"[merge_yaml] [{i}/{n}] 解析失败：{e}，跳过。", file=sys.stderr)
            continue

        print(f"[merge_yaml] [{i}/{n}] 解析完成：story_id={str(ai_meta.get('story_id'))[:8]}... "
              f"标题={ai_meta.get('title_la')}  "
              f"词数={ai_meta.get('word_count')}", file=sys.stderr)

        # 难度评估
        print(f"[merge_yaml] [{i}/{n}] 正在评估难度...", file=sys.stderr)
        try:
            eval_result = evaluate_text(latin_text)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"[merge_yaml] [{i}/{n}] 评估失败：{e}，跳过。", file=sys.stderr)
            continue

        print(f"[merge_yaml] [{i}/{n}] 评估结果：覆盖率={eval_result.get('v2_rate')}%  "
              f"等级=Cap.{eval_result.get('v2_level')}  "
              f"最适章节=Cap.{eval_result.get('v2_best_fit')}  "
              f"超纲词={len(eval_result.get('v2_oov', []))}个", file=sys.stderr)

        # 合并 + 生成 MD（merge() 返回元组：(merged_dict, effective_chapter)）
        merged, effective_chapter = merge(ai_meta, eval_result)

        # AI 审查（v2_10_0 新增，可选步骤）
        if args.review:
            if not args.review_ai_command:
                print(f"[merge_yaml] [{i}/{n}] 警告：--review 启用但未指定 --review-ai-command，跳过审查。",
                      file=sys.stderr)
            else:
                print(f"[merge_yaml] [{i}/{n}] 正在 AI 审查（macrons / 用词 / 古典性）...",
                      file=sys.stderr)
                try:
                    review_result = run_ai_review(
                        latin_text=latin_text,
                        chapter=effective_chapter,
                        ai_command=args.review_ai_command,
                        tmp_dir=Path("/tmp"),
                        story_id=ai_meta.get("story_id", "unknown"),
                    )
                    merged["ai_review"] = review_result
                    verdict = review_result.get("verdict", "needs_fixes")
                    n_macrons = len(review_result.get("macrons_issues", []))
                    n_vocab = len(review_result.get("vocabulary_issues", []))
                    n_crit = len(review_result.get("critical_issues", []))
                    print(f"[merge_yaml] [{i}/{n}] 审查结果：verdict={verdict}  "
                          f"长音={n_macrons}  用词={n_vocab}  阻塞={n_crit}",
                          file=sys.stderr)
                    if args.review_strict and verdict == "fail":
                        print(f"[merge_yaml] [{i}/{n}] --review-strict 启用且 verdict=fail，跳过。",
                              file=sys.stderr)
                        continue
                except Exception as e:
                    print(f"[merge_yaml] [{i}/{n}] AI 审查失败：{e}，继续入库。",
                          file=sys.stderr)
                    merged["ai_review"] = {"verdict": "needs_fixes", "error": str(e)}

        md_content = output_md(merged, latin_text)

        # 以算法评估的难度为目录归属（降级时 v2_best_fit 兜底）
        if not isinstance(effective_chapter, int) or effective_chapter <= 0:
            print(f"[merge_yaml] [{i}/{n}] 错误：无法确定难度章节（覆盖率过低），跳过。", file=sys.stderr)
            continue

        # 提取当前故事的篇幅标识 + 拉丁语标题
        length_tier_raw = ai_meta.get("length_tier", "短篇")
        title_la = ai_meta.get("title_la", "sine_titulo")

        if args.stdout and i == 1:
            sys.stdout.write(md_content)
        else:
            if args.output:
                if i == 1:
                    output_path = Path(args.output).resolve()
                else:
                    base = Path(args.output).resolve()
                    output_path = base.with_name(f"{base.stem}_part{i}{base.suffix}")
            elif args.auto_number:
                output_dir = (script_dir / args.output_dir).resolve()
                output_path = next_story_filename(
                    output_dir, effective_chapter, title_la, str(length_tier_raw)
                )
            else:
                print(f"[merge_yaml] [{i}/{n}] 未指定 --output 且 --auto-number=false，回退到 stdout。",
                      file=sys.stderr)
                sys.stdout.write(md_content)
                continue

            # 写入文件
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"[merge_yaml] [{i}/{n}] 已写入 {output_path}", file=sys.stderr)

            # 维护 realitates.json 索引（以评估难度章节为键）
            try:
                rel_path = output_path.relative_to(script_dir).as_posix()
            except ValueError:
                rel_path = output_path.name
            index_entry = {
                "path": rel_path,
                "chapter": effective_chapter,
                "title_zh": ai_meta.get("title_zh", "")
            }
            update_realitates_index(script_dir, index_entry)
            print(f"[merge_yaml] [{i}/{n}] 索引已更新：{rel_path}", file=sys.stderr)

            # OOV 反馈日志（方案D 数据闭环）
            oov_list = eval_result.get("v2_oov", [])
            if oov_list:
                log_oov(script_dir, rel_path, oov_list, effective_chapter)
                print(f"[merge_yaml] [{i}/{n}] OOV 已记录：{len(oov_list)} 个 → oov_corrections.jsonl", file=sys.stderr)

    # 注意：原"自动调用 auto_supplement_map"已暂停（v2_8_0 → v2_9_0）。
    # 原因：当前样本量太小，OOV 自动建议的准确率仅约 50%，不应自动应用。
    # OOV 数据继续在 oov_corrections.jsonl 累积，积累到 20+ 唯一词后再人工审。
    # 手动触发：python difficulty_algorithm/auto_supplement_map.py

    print(f"\n[merge_yaml] 全部完成：{n} 篇故事处理完毕。", file=sys.stderr)


if __name__ == "__main__":
    main()
