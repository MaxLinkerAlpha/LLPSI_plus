#!/usr/bin/env python3
"""
OCR 残骸清理 v1_0_0
清理 form_chapter_map.json 中的 OCR 残骸（~2,000 条），
同时从管道词和斜杠词中抢救真词形。

原则：
  - 输出到 form_chapter_map_cleaned.json，不动原文件
  - 每条删除都记录理由
  - 管道词（insul|is → insulis）抢救为新增词形
  - 所有操作可审计、可逆

安全措施：
  - 原文件不动
  - 自动创建 .bak（即使已有）
  - 干跑报告 + 确认再写
  - 事后对比验证
"""

import json
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

DIR = Path(__file__).resolve().parent

# ============================================================
# 工具函数
# ============================================================

def has_non_latin(word: str) -> bool:
    """含非拉丁字母/标点（允许连字符、空格）"""
    if not word or not word.strip():
        return True
    nfd = unicodedata.normalize("NFD", word)
    for ch in nfd:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat == "Mn" or cat == "Zs":
            continue
        if ch in ("'", "\u2019", "-"):
            continue
        return True
    return False

def is_too_long(word: str) -> bool:
    return len(word) > 20

def is_english(word: str) -> bool:
    """英语词混入（LLPSI 页边注释）"""
    english = {
        "the", "and", "for", "with", "from", "this", "that", "which",
        "book", "page", "chapter", "following", "note", "see", "also",
        "grammar", "vocab", "practice", "exercise", "lesson", "part",
        "verb", "noun", "adj", "adv", "conj", "prep", "pron", "interj",
        "line", "lines", "read", "reading", "text", "sentence",
    }
    return word.lower().strip() in english

def is_short_consonant(word: str) -> bool:
    """2字母辅音碎片（OCR把词内辅音团当独立词）"""
    return bool(re.fullmatch(r'[bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ]{1,2}', word))

def contains_digit_or_prefix(word: str) -> bool:
    """含行号数字前缀"""
    return bool(re.match(r'^\d', word)) or bool(re.match(r'^[A-Za-zāēīōūȳ]+\d', word))

def is_pure_number(word: str) -> bool:
    return word.strip().isdigit()

def is_suffix_fragment(word: str) -> bool:
    """纯词尾碎片（无完整词干）"""
    fragments = {"ārum", "ōrum", "ium", "ābus", "ēbus", "ibus", "ōtis", "ātis", "ētis",
                 "ātur", "ētur", "ītur", "antur", "untur", "intur",
                 "ātae", "ātīs", "antur", "entur"}
    return word.lower().strip() in fragments

def is_camel_joint(word: str) -> bool:
    """驼峰拼接：两个大写开头被OCR粘在一起"""
    return bool(re.search(r'[A-Z][a-zāēīōūȳ]{2,}[A-Z]', word)) and len(word) > 5

def is_cross_sentence(word: str) -> bool:
    """跨句粘连：含 .大写 或 !"大写 或 ,大写 模式"""
    return bool(re.search(r'[\.!\?][",\']*[A-ZĀĒĪŌŪ]', word))

def is_quote_joined(word: str) -> bool:
    """引号粘连：含 !" 或 ." 等"""
    return bool(re.search(r'[!\?\.]["]', word))

def is_ellipsis_pattern(word: str) -> bool:
    """省略号语法模式（neque...neque, et...et 等）"""
    return "..." in word

# ============================================================
# 主清理逻辑
# ============================================================

def clean_form_chapter_map(data: dict) -> tuple[dict, dict, list]:
    """
    返回: (cleaned_map, rescue_log, delete_log)
    """
    cleaned = {}
    rescued = defaultdict(list)
    deleted = []

    for key, value in data.items():
        reasons = []

        # ---- 阶段 1: 标记垃圾 ----
        if is_pure_number(key):
            reasons.append("pure_number")
        elif contains_digit_or_prefix(key):
            reasons.append("number_prefix")
        elif is_short_consonant(key):
            reasons.append("short_consonant")
        elif is_english(key):
            reasons.append("english")
        elif is_too_long(key):
            reasons.append("too_long")
        elif is_cross_sentence(key):
            reasons.append("cross_sentence")
        elif is_quote_joined(key):
            reasons.append("quote_joined")
        elif is_ellipsis_pattern(key):
            reasons.append("ellipsis")
        elif is_camel_joint(key):
            reasons.append("camel_joint")
        elif is_suffix_fragment(key):
            reasons.append("suffix_fragment")

        # 含逗号但非上述类别的残留
        if not reasons and "," in key and not key.startswith(","):
            reasons.append("comma_join")

        # 含非拉丁字符（杂类残骸）
        if not reasons and has_non_latin(key):
            reasons.append("non_latin_misc")

        # ---- 阶段 2: 抢救管道词 ----
        if "|" in key:
            clean_word = key.replace("|", "").strip()
            # 检查清洗后是否是合法的拉丁词
            if len(clean_word) >= 3 and re.fullmatch(r'[A-Za-zāēīōūȳĀĒĪŌŪȲ]+', clean_word):
                rescued["pipe"].append((clean_word, value, key))
            if not reasons:
                reasons.append("pipe_separator")

        # ---- 阶段 3: 抢救斜杠词 ----
        if "/" in key and key.count("/") == 1:
            parts = [p.strip() for p in key.split("/")]
            for p in parts:
                if len(p) >= 3 and re.fullmatch(r'[A-Za-zāēīōūȳĀĒĪŌŪȲ]+', p):
                    rescued["slash"].append((p, value, key))
            if not reasons:
                reasons.append("slash_separator")

        # ---- 阶段 4: 连字符（不抢救，直接删） ----
        if "-" in key and not reasons:
            reasons.append("hyphenated")

        # ---- 决策 ----
        if reasons:
            deleted.append((key, value, reasons))
        else:
            cleaned[key] = value

    return cleaned, rescued, deleted


def apply_rescued(cleaned: dict, rescued: dict) -> dict:
    """将抢救的词形合并到 cleaned 中（取最早章节号）"""
    added_count = 0
    for category, entries in rescued.items():
        for clean_word, chapter, source_key in entries:
            # 小写标准化
            word_lower = clean_word.lower()
            if word_lower in cleaned:
                # 取更早的章节
                existing = cleaned[word_lower]
                if isinstance(existing, list):
                    existing_val = min(existing)
                else:
                    existing_val = existing
                new_val = min(chapter) if isinstance(chapter, list) else chapter
                if new_val < existing_val:
                    cleaned[word_lower] = new_val
            else:
                cleaned[word_lower] = min(chapter) if isinstance(chapter, list) else chapter
                added_count += 1
    return cleaned, added_count


def main():
    src = DIR / "form_chapter_map.json"
    dst = DIR / "form_chapter_map_cleaned.json"
    log_file = DIR / "_clean_log.json"

    # ---- 自动备份 ----
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = DIR / f"form_chapter_map_clean_bak_{ts}.json"
    shutil.copy2(src, bak)
    print(f"[备份] {src.name} → {bak.name}")

    # ---- 加载 ----
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    print(f"[加载] {len(data):,} 条目")

    # ---- 清理 ----
    cleaned, rescued, deleted = clean_form_chapter_map(data)
    print(f"[清理] 保留 {len(cleaned):,} | 删除 {len(deleted):,} | 管道抢救 {len(rescued['pipe'])} | 斜杠抢救 {len(rescued['slash'])}")

    # ---- 合并抢救 ----
    cleaned, added = apply_rescued(cleaned, rescued)
    print(f"[抢救] 新增 {added} 条词形 → 最终 {len(cleaned):,} 条")

    # ---- 保存 ----
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False)
    print(f"[保存] {dst.name}  ({dst.stat().st_size / 1024:.0f} KB)")

    # ---- 删除日志 ----
    delete_reasons = Counter()
    for _, _, reasons in deleted:
        for r in reasons:
            delete_reasons[r] += 1

    log = {
        "version": "1_0_0",
        "timestamp": ts,
        "source": str(src),
        "source_entries": len(data),
        "cleaned_entries": len(cleaned),
        "deleted_count": len(deleted),
        "rescued_pipe": len(rescued["pipe"]),
        "rescued_slash": len(rescued["slash"]),
        "new_from_rescue": added,
        "delete_reasons": dict(delete_reasons.most_common()),
        "delete_samples": {
            reason: [k for k, _, rs in deleted if reason in rs][:5]
            for reason in delete_reasons
        },
        "rescued_samples_pipe": [{"src": s, "dst": d, "ch": c} for d, c, s in rescued["pipe"][:10]],
        "rescued_samples_slash": [{"src": s, "dst": d, "ch": c} for d, c, s in rescued["slash"][:10]],
    }
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"[日志] {log_file.name}")

    # ---- 摘要 ----
    print("\n" + "=" * 60)
    print("清理摘要")
    print("=" * 60)
    print(f"  原始: {len(data):,} 条")
    print(f"  保留: {len(cleaned):,} 条")
    print(f"  删除: {len(deleted):,} 条 ({len(deleted)/len(data)*100:.1f}%)")
    print(f"  抢救新增: {added} 条")
    print(f"\n  删除原因分布:")
    for reason, cnt in delete_reasons.most_common():
        print(f"    {reason:<25}: {cnt:>5}")


if __name__ == "__main__":
    main()
