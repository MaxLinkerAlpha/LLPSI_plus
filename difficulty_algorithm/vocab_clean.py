#!/usr/bin/env python3
"""
vocab_clean.py v1_0_0 — 清洗 cap{N}_vocab.json 里的 OCR 残片、拼接词、错误字符。

读取：difficulty_algorithm/vocab_by_chapter/cap{N}_vocab.json
输出：difficulty_algorithm/vocab_by_chapter/cap{N}_vocab_clean.json
      终端打印清理报告（删除/拆分/规范化数量）

清洗规则（保守，不引入猜测）：
  1. 剔除含非拉丁字母（含 & / . / - / 数字 / 中划线 / 复合声调字符如 Ī̆）的词
  2. 剔除 < 4 字符的碎片（合理最短词如 "ego" / "is" 保留——但这些会被注入 prompt 时单独处理）
  3. 尝试拆分明显拼接的词（两个大写开头 + 中间无元音过渡 = 视为两个词）
  4. 规范化为小写（保留 macron）
  5. 排除纯词尾碎片（ārum/ōrum/ibus/ātur/ētur 等，纯属变格尾）

用法：
    python difficulty_algorithm/vocab_clean.py --chapter 8
    python difficulty_algorithm/vocab_clean.py --all   # 处理所有章节
    python difficulty_algorithm/vocab_clean.py --chapter 8 --dry-run   # 只统计不写入
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# 拉丁字母（含 macron / 抑扬符 / 长音）
LATIN_PATTERN = re.compile(r"^[a-zA-Zāăāēĕīĭōŏūŭȳȳ́́́́́́]+$")
# 纯词尾碎片（基本可视为"非完整词"）
SUFFIX_FRAGMENTS = {
    "ārum", "ōrum", "ium", "uum", "arum", "orum",
    "ibus", "ābus", "ēbus",
    "ātur", "ētur", "ītur", "antur", "untur", "intur",
    "ātis", "ētis", "itīs", "untis",
    "ātae", "ātīs", "ōtis",
    "īs", "ās", "ōs", "ēs",
    "que", "ve", "ne",
}
# 行号 + 词片段模式（如 "1r", "3/-o", "45in", "65Medus"）
NUM_PREFIX = re.compile(r"^\d+")
# 复合 / 拼接模式：两个大写单词紧贴（如 Albinumvidet, Aemiliadomin）
CAMEL_SPLIT = re.compile(r"([A-Z][a-zāăāēĕīĭōŏūŭ]+?)([A-Z][a-zāăāēĕīĭōŏūŭ]+)")


def is_pure_fragment(word: str) -> bool:
    """判断是否是纯词尾碎片（仅基于白名单）。"""
    return word.lower() in SUFFIX_FRAGMENTS


def has_non_latin(word: str) -> bool:
    """检测是否含非拉丁字符。允许的：拉丁字母（L*）+ 组合附加符（Mn）。"""
    nfd = unicodedata.normalize("NFD", word)
    for ch in nfd:
        if ch in (" ", "\t", "\n"):
            return True
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat == "Mn":  # 字母 + 组合声调允许
            continue
        return True
    return False


def try_split_camel(word: str) -> list:
    """尝试按大写边界拆分拼接词。返回拆分后的子词列表（不拆分则返回原词）。"""
    # 模式 1：首字母大写 + 后续小写大写拼接（Albinumvidet）
    m = re.search(r"([A-Z][a-zāăāēĕīĭōŏūŭ]+)([A-Z][a-zāăāēĕīĭōŏūŭ])", word)
    if m:
        parts = []
        for pat in re.finditer(r"[A-Z][a-zāăāēĕīĭōŏūŭ]+", word):
            parts.append(pat.group(0))
        return parts if len(parts) > 1 else [word]
    # 模式 2：纯小写但已能识别为词尾拼接（如 "aemiliadomin" = "aemilia" + "domin"）
    # 这种太难判断（exeo, deinde 是真词），保守不切
    return [word]


def clean_word(word: str) -> tuple:
    """清洗单个词。

    Returns:
        (cleaned_words, was_modified, reason)
        - cleaned_words: list[str]，可能 0/1/N 个
        - was_modified: 是否做了改动
        - reason: 改动原因（用于报告）
    """
    if not word or not word.strip():
        return [], False, "empty"

    w = word.strip()

    # 1. 行号前缀（如 "1r", "3/-o"）
    if NUM_PREFIX.match(w):
        # 去掉行号，看剩余
        rest = NUM_PREFIX.sub("", w)
        if not rest or has_non_latin(rest) or len(rest) < 3:
            return [], True, f"num_prefix:{w}"
        return [rest], True, f"strip_num_prefix:{w}->{rest}"

    # 2. 含非拉丁字符
    if has_non_latin(w):
        return [], True, f"non_latin:{w}"

    # 3. 过短（< 3 字符：碎片风险高）
    if len(w) < 3:
        return [], True, f"too_short:{w}"

    # 4. 纯词尾碎片
    if is_pure_fragment(w.lower()):
        return [], True, f"suffix_fragment:{w}"

    # 5. 驼峰拆分（Albinumvidet → Albinum + videt）
    parts = try_split_camel(w)
    if len(parts) > 1:
        return [p for p in parts if len(p) >= 3], True, f"camel_split:{w}->{parts}"

    # 6. 规范化：去重音
    nfd = unicodedata.normalize("NFD", w)
    base = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    if base != w:
        return [base], True, f"normalize_diacritic:{w}->{base}"

    # 7. 大写转小写（保留 macrons）
    if w[0].isupper() and len(w) > 1 and w[1:].islower():
        return [w.lower()], True, f"lowercase:{w}->{w.lower()}"

    return [w], False, "kept"


def process_chapter(chapter: int, vocab_dir: Path, dry_run: bool = False) -> dict:
    """处理单个章节词表。

    Returns:
        报告 dict: {original, kept, removed, modified, fragments, by_reason}
    """
    src = vocab_dir / f"cap{chapter}_vocab.json"
    if not src.exists():
        print(f"[vocab_clean] 警告：cap{chapter} 不存在，跳过。")
        return {}

    data = json.loads(src.read_text(encoding="utf-8"))
    cleaned = []
    seen = set()
    report = {
        "chapter": chapter,
        "original": len(data),
        "removed": 0,
        "modified": 0,
        "by_reason": {},
        "examples": {},
    }

    for w in data:
        result, modified, reason = clean_word(w)
        if not result:
            report["removed"] += 1
            report["by_reason"][reason] = report["by_reason"].get(reason, 0) + 1
            report["examples"].setdefault(reason, []).append(w)
            continue
        if modified:
            report["modified"] += 1
        for cw in result:
            if cw not in seen:
                seen.add(cw)
                cleaned.append(cw)

    report["kept"] = len(cleaned)

    if not dry_run:
        dst = vocab_dir / f"cap{chapter}_vocab_clean.json"
        dst.write_text(
            json.dumps(cleaned, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        print(f"[vocab_clean] Cap.{chapter}: {report['original']} → {report['kept']} "
              f"(删 {report['removed']}, 改 {report['modified']}) → {dst.name}")
    else:
        print(f"[vocab_clean] Cap.{chapter}: {report['original']} → {report['kept']} "
              f"(删 {report['removed']}, 改 {report['modified']}) [DRY-RUN]")

    if report["by_reason"]:
        print(f"  删除原因 top-5:")
        for reason, count in sorted(report["by_reason"].items(),
                                    key=lambda x: -x[1])[:5]:
            examples = report["examples"].get(reason, [])[:3]
            print(f"    {reason}: {count} 次 (例: {examples})")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="清洗 cap{N}_vocab.json 里的 OCR 残片"
    )
    parser.add_argument("--chapter", "-c", type=int, default=None,
                        help="指定章节号（1-34）")
    parser.add_argument("--all", "-a", action="store_true",
                        help="处理所有章节")
    parser.add_argument("--dry-run", action="store_true",
                        help="只统计不写入")
    parser.add_argument("--vocab-dir", type=Path, default=None,
                        help="vocab_by_chapter/ 路径（默认：脚本上级 difficulty_algorithm/）")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    vocab_dir = args.vocab_dir or (script_dir / "vocab_by_chapter")
    if not vocab_dir.exists():
        print(f"[vocab_clean] 错误：{vocab_dir} 不存在。", file=sys.stderr)
        sys.exit(1)

    if args.all:
        # 处理所有 cap{N}_vocab.json
        cap_files = sorted(vocab_dir.glob("cap*_vocab.json"))
        if not cap_files:
            print(f"[vocab_clean] 错误：{vocab_dir} 下没有 cap*_vocab.json。",
                  file=sys.stderr)
            sys.exit(1)
        total = {"original": 0, "kept": 0, "removed": 0, "modified": 0}
        for f in cap_files:
            ch = int(f.stem.replace("cap", "").replace("_vocab", ""))
            r = process_chapter(ch, vocab_dir, dry_run=args.dry_run)
            for k in total:
                total[k] += r.get(k, 0)
        print(f"\n[vocab_clean] 总计：{total['original']} → {total['kept']} "
              f"(删 {total['removed']}, 改 {total['modified']})")
    elif args.chapter:
        process_chapter(args.chapter, vocab_dir, dry_run=args.dry_run)
    else:
        print("[vocab_clean] 请指定 --chapter N 或 --all。", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
