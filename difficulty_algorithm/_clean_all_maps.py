#!/usr/bin/env python3
"""
通用 OCR 残骸清理 v1_1_0
v1_1_0 变更：保留所有2字符纯拉丁词（避免误删 id/is 等真词）
统一清理 4 个算法 JSON 文件：
  - form_chapter_map.json (value: int 章节号)
  - lemma_chapter_map.json (value: int 章节号)
  - word_lemma_map.json (value: str 词元)
  - word_chapter_map_normalized.json (value: int 章节号)

清理策略（基于第一性原理）：
  算法文件的唯一用途是"查表"——evaluate_v2.py 把故事词形（去长音+小写）扔进来查。
  任何永不会被故事文本匹配的键，都是纯噪音。

清理项：
  1. 删除含数字前缀/纯数字的键
  2. 删除含非拉丁字符（标点/引号/句点/逗号/省略号）的键
  3. 删除超长键 (>20字符，OCR粘连)
  4. 删除驼峰拼接键
  5. 删除跨句粘连键 (含 ." 或 !" 等)
  6. 删除含连字符的键（永不会被故事文本匹配）
  7. 删除含管道/斜杠的键，但先抢救真词形
  8. 删除2字符碎片键（ae/be/ce等），保留真词（in/et/me等）
  9. 删除英语注释混入

安全措施：
  - 输出到 *_cleaned.json，不动原文件
  - 自动创建带时间戳的 .bak
  - 抢救词不覆盖已有键（v1_1_0 修复）
  - 详细的清理日志
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
# 配置：4 个文件的元信息
# ============================================================
FILES_CONFIG = [
    {
        "name": "form_chapter_map.json",
        "value_type": "chapter",  # int
    },
    {
        "name": "lemma_chapter_map.json",
        "value_type": "chapter",  # int
    },
    {
        "name": "word_lemma_map.json",
        "value_type": "lemma",  # str
    },
    {
        "name": "word_chapter_map_normalized.json",
        "value_type": "chapter",  # int
    },
]

# ============================================================
# 2字符真词白名单（明确的拉丁词，其余2字符键视为碎片删除）
# ============================================================
TWO_CHAR_REAL_WORDS = {
    # 介词/连词/代词/副词
    "in", "et", "ac", "at", "ut", "ne", "se", "si", "tu", "te", "me",
    "da", "do", "de", "ex", "ab", "ad", "ob", "per", "pro", "sub",
    # 感叹/小品词
    "eu", "o", "ah", "oh", "he", "ha", "ho", "ei", "au",
    # 动词形式
    "es", "est", "ed", "it", "is",
    # 名词缩写
    "re",  # res
    "mi",  # mihi
}

# ============================================================
# 垃圾检测函数
# ============================================================
LATIN_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                  "\u0101\u0113\u012B\u014D\u016B\u0233\u01E2"
                  "\u0100\u0112\u012A\u014C\u016A\u0232")

def is_pure_latin(w):
    return all(c in LATIN_CHARS for c in w) and len(w) >= 1

def has_non_latin_non_hyphen(w):
    """含非拉丁字母、非连字符、非管道、非斜杠的字符"""
    for ch in w:
        if ch in "-|/":
            continue
        cat = unicodedata.category(ch)
        if not (cat.startswith("L") or cat == "Mn"):
            return True
    return False

def classify_garbage(key):
    """返回删除原因列表，空列表=保留"""
    reasons = []

    if not key or not key.strip():
        return ["empty"]

    if key.strip().isdigit():
        return ["pure_number"]

    if re.match(r'^\d', key):
        return ["number_prefix"]

    if len(key) > 20:
        reasons.append("too_long")

    # 含数字
    if re.search(r'\d', key):
        reasons.append("contains_digit")

    # 英语注释
    english = {"the","and","for","with","from","this","that","which",
               "book","page","chapter","following","note","see","also",
               "grammar","vocab","practice","exercise","lesson","part",
               "verb","noun","adj","adv","conj","prep","pron","interj",
               "line","lines","read","reading","text","sentence"}
    if key.lower().strip() in english:
        return ["english"]

    # 跨句粘连
    if re.search(r'[\.!\?][",\']*[A-ZĀĒĪŌŪ]', key):
        reasons.append("cross_sentence")

    # 引号粘连
    if re.search(r'[!\?\.]["]', key):
        reasons.append("quote_joined")

    # 省略号
    if "..." in key:
        reasons.append("ellipsis")

    # 驼峰拼接（两个大写字母段粘连）
    if re.search(r'[A-Z][a-zāēīōūȳ]{2,}[A-Z]', key) and len(key) > 5:
        reasons.append("camel_joint")

    # 含非拉丁字符（杂类残骸）
    if has_non_latin_non_hyphen(key):
        reasons.append("non_latin_misc")

    # 含逗号
    if "," in key:
        reasons.append("comma_join")

    # 含连字符
    if "-" in key:
        reasons.append("hyphenated")

    # 2字符碎片：v1_1_0 改为保留所有2字符纯拉丁词
    # 原因：id/is/in/et 等都是真词，逐个甄别风险大于收益
    # （386条占比极小，保留无副作用，删错会降低覆盖率）
    # if len(key) == 2 and is_pure_latin(key) and key.lower() not in TWO_CHAR_REAL_WORDS:
    #     reasons.append("two_char_fragment")

    return reasons


def try_rescue(key, value):
    """尝试从管道/斜杠词中抢救真词形。返回 [(clean_word, value), ...]"""
    rescued = []

    if "|" in key:
        clean = key.replace("|", "").strip()
        if len(clean) >= 3 and is_pure_latin(clean):
            rescued.append((clean, value))

    if "/" in key and key.count("/") == 1:
        parts = [p.strip() for p in key.split("/")]
        for p in parts:
            if len(p) >= 3 and is_pure_latin(p):
                rescued.append((p, value))

    return rescued


# ============================================================
# 主清理逻辑
# ============================================================
def clean_one_file(config):
    fname = config["name"]
    vtype = config["value_type"]
    src = DIR / fname
    dst = DIR / fname.replace(".json", "_cleaned.json")

    if not src.exists():
        print(f"[跳过] {fname} 不存在")
        return None

    # 自动备份
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = DIR / fname.replace(".json", f"_clean_bak_{ts}.json")
    shutil.copy2(src, bak)

    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    cleaned = {}
    rescued_entries = []
    deleted = []

    for key, value in data.items():
        reasons = classify_garbage(key)

        # 抢救管道/斜杠词
        if "|" in key or ("/" in key and key.count("/") == 1):
            rescued_entries.extend(try_rescue(key, value))

        if reasons:
            deleted.append((key, value, reasons))
        else:
            cleaned[key] = value

    # 合并抢救词（不覆盖已有）
    added = 0
    merged = 0
    for clean_word, value in rescued_entries:
        word_lower = clean_word.lower()
        if word_lower in cleaned:
            merged += 1
        else:
            cleaned[word_lower] = value
            added += 1

    # 保存
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False)

    # 统计
    delete_reasons = Counter()
    for _, _, reasons in deleted:
        for r in reasons:
            delete_reasons[r] += 1

    result = {
        "file": fname,
        "original": len(data),
        "cleaned": len(cleaned),
        "deleted": len(deleted),
        "rescued_new": added,
        "rescued_merged": merged,
        "delete_reasons": dict(delete_reasons.most_common()),
        "backup": bak.name,
    }

    print(f"\n[{fname}]")
    print(f"  原始: {len(data):,} → 清理: {len(cleaned):,}  ({len(cleaned)/len(data)*100:.1f}%)")
    print(f"  删除: {len(deleted):,}  抢救新增: {added}  抢救跳过: {merged}")
    print(f"  备份: {bak.name}")
    print(f"  删除原因 Top5:")
    for r, c in list(delete_reasons.most_common(5)):
        print(f"    {r:<25}: {c:>5}")

    return result


def main():
    print("=" * 70)
    print("通用 OCR 残骸清理 v1_0_0")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    results = []
    for config in FILES_CONFIG:
        r = clean_one_file(config)
        if r:
            results.append(r)

    # 汇总日志
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log = {
        "version": "1_0_0",
        "timestamp": ts,
        "files": results,
        "total_original": sum(r["original"] for r in results),
        "total_cleaned": sum(r["cleaned"] for r in results),
        "total_deleted": sum(r["deleted"] for r in results),
    }
    log_file = DIR / "_clean_all_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print("汇总")
    print(f"{'='*70}")
    print(f"  总原始: {log['total_original']:,}")
    print(f"  总清理: {log['total_cleaned']:,}")
    print(f"  总删除: {log['total_deleted']:,}")
    print(f"  日志: {log_file.name}")


if __name__ == "__main__":
    main()
