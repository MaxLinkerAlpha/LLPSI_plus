#!/usr/bin/env python3
"""
auto_supplement_map.py v1_0_0 — 自动分析 OOV 日志，对映射表做保守补全。

策略（保守）：
  - 读 oov_corrections.jsonl
  - 对每个 OOV 词做：
    1. 剥长音 → simplemma 还原
    2. 如果 lemma 已在 lemma_chapter_map.json → 这是 evaluate_v2 漏匹配，不动映射表
    3. 如果 lemma 不在表中：
       a. 词首 4 字符相同 → 在表里查近邻词 → 推断章节（仅作"建议"）
       b. 写入 supplement_suggestions.jsonl（供人工审核）
  - 不自动修改 lemma_chapter_map.json（避免引入错误）

用法：
  # 仅看建议（不写任何文件）
  python difficulty_algorithm/auto_supplement_map.py --dry-run

  # 生成建议文件
  python difficulty_algorithm/auto_supplement_map.py
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

MACRON_MAP = str.maketrans("āēīōūȳĀĒĪŌŪȲ", "aeiouyAEIOUY")

# 加载预计算词形→章节映射表
def load_form_chapter_map(map_path: Path) -> dict:
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================
# 加载映射表
# ============================================================

def load_lemma_chapter_map(map_path: Path) -> dict:
    """加载 lemma_chapter_map.json（LLPSI lemma → 章节号）。"""
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_oov_log(log_path: Path) -> list:
    """加载 oov_corrections.jsonl。"""
    if not log_path.exists():
        return []
    entries = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# ============================================================
# 分析单个 OOV 词
# ============================================================

def analyze_oov(word: str, lemma_chapter_map: dict, form_chapter_map: dict) -> dict:
    """对单个 OOV 词做分析，返回建议 dict。"""
    clean = word.translate(MACRON_MAP).lower()

    # 直接查预计算词形表（已包含 word_lemma → lemma_chapter 的合成）
    if clean in form_chapter_map:
        return {
            "word": word,
            "clean": clean,
            "form_matched": True,
            "verdict": "lemma_in_map",
            "actual_chapter": form_chapter_map[clean],
            "suggestion": f"词形 '{clean}' 已在 form_chapter_map 中（Cap.{form_chapter_map[clean]}），可能是 evaluate_v2 漏匹配，不动映射表",
            "action": "none",
        }

    # 不在 form_chapter_map 中 → 无法从预计算获得，需要人工处理
    # 我们仍然可以尝试用 lemma_chapter_map 找近邻，但找不到还原结果
    prefix4 = clean[:4]
    neighbors = [
        (k, v) for k, v in lemma_chapter_map.items()
        if k.startswith(prefix4) and k != clean
    ]
    if neighbors:
        # 取前 3 个近邻中 chapter 最低的（保守：认为这是早期章节的词）
        neighbors_chapters = [v for _, v in neighbors]
        min_chapter = min(neighbors_chapters)
        return {
            "word": word,
            "clean": clean,
            "verdict": "lemma_not_in_map",
            "nearest_chapter": min_chapter,
            "nearest_neighbors": [k for k, _ in neighbors[:3]],
            "suggestion": f"词形 '{clean}' 不在 form_chapter_map 中，近邻词（如 '{neighbors[0][0]}'）属于 Cap.{min_chapter}",
            "action": "suggest_add",
            "suggested_chapter": min_chapter,
        }

    return {
        "word": word,
        "clean": clean,
        "verdict": "lemma_not_in_map_no_neighbors",
        "suggestion": f"词形 '{clean}' 不在 form_chapter_map 中，且无近邻词，需要人工判断章节归属",
        "action": "needs_human",
    }


# ============================================================
# 主入口
# ============================================================

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="自动分析 OOV 日志，对映射表做保守补全（不直接修改映射表）"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="仅打印分析结果，不写建议文件"
    )
    parser.add_argument(
        "--oov-log", type=Path,
        default=Path(__file__).resolve().parent.parent / "AI_reader" / "oov_corrections.jsonl",
        help="OOV 日志路径（默认 ../AI_reader/oov_corrections.jsonl）"
    )
    parser.add_argument(
        "--map", type=Path,
        default=Path(__file__).resolve().parent / "lemma_chapter_map.json",
        help="映射表路径（默认 ./lemma_chapter_map.json）"
    )
    parser.add_argument(
        "--output", "-o", type=Path,
        default=Path(__file__).resolve().parent.parent / "AI_reader" / "supplement_suggestions.jsonl",
        help="建议文件输出路径"
    )
    parser.add_argument(
        "--min-frequency", "-f", type=int, default=2,
        help="至少出现 N 次才生成建议（默认 2，避免噪声）"
    )
    args = parser.parse_args()

    if not args.map.exists():
        print(f"[auto_supplement] 错误：找不到映射表 {args.map}", file=sys.stderr)
        return 1

    lemma_chapter_map = load_lemma_chapter_map(args.map)
    form_chapter_map = load_form_chapter_map(Path(__file__).resolve().parent / "form_chapter_map.json")
    oov_entries = load_oov_log(args.oov_log)

    if not oov_entries:
        print(f"[auto_supplement] OOV 日志为空（{args.oov_log}），无需分析。")
        return 0

    # 统计 OOV 词频
    oov_counter: Counter = Counter()
    for entry in oov_entries:
        for w in entry.get("oov", []):
            oov_counter[w] += 1

    print(f"[auto_supplement] 分析 {len(oov_counter)} 个去重 OOV 词（min_frequency={args.min_frequency}）")

    suggestions = []
    stats = {"lemma_in_map": 0, "suggest_add": 0, "needs_human": 0, "skipped_low_freq": 0}

    for word, freq in oov_counter.most_common():
        if freq < args.min_frequency:
            stats["skipped_low_freq"] += 1
            continue
        result = analyze_oov(word, lemma_chapter_map, form_chapter_map)
        result["frequency"] = freq
        result["analyzed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        suggestions.append(result)
        if result["verdict"] == "lemma_in_map":
            stats["lemma_in_map"] += 1
        elif result["action"] == "suggest_add":
            stats["suggest_add"] += 1
        else:
            stats["needs_human"] += 1

    # 打印统计
    print(f"[auto_supplement] 分析结果：")
    print(f"  - lemma 已在表中（evaluate_v2 漏匹配）: {stats['lemma_in_map']}")
    print(f"  - 建议补全（近邻推断）: {stats['suggest_add']}")
    print(f"  - 需人工判断: {stats['needs_human']}")
    print(f"  - 跳过低频: {stats['skipped_low_freq']}")

    if args.dry_run:
        print(f"\n[auto_supplement] DRY RUN 模式：不写任何文件")
        for s in suggestions:
            print(f"  [{s['frequency']}x] {s['word']:20} → lemma={s['lemma']:15}  {s['verdict']}")
            print(f"           {s['suggestion']}")
        return 0

    # 写建议文件
    with open(args.output, "w", encoding="utf-8") as f:
        for s in suggestions:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"[auto_supplement] 建议已写入: {args.output}  ({len(suggestions)} 条)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
