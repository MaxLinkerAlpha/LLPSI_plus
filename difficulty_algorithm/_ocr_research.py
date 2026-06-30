#!/usr/bin/env python3
"""
OCR 残骸调研 v1_0_0
不修改任何文件，只统计备份中：
  1. OCR 残骸类型分布
  2. 每类残骸数量
  3. 删除后的预期收益（覆盖率、内存）
  4. 误删风险评估
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from collections import Counter, defaultdict

# 用备份数据（当前文件已恢复，不动它）
BAK_FILES = {
    "form_chapter_map": "form_chapter_map.json.bak",
    "lemma_chapter_map": "lemma_chapter_map.json.bak",
    "word_lemma_map": "word_lemma_map.json.bak",
    "word_chapter_map_normalized": "word_chapter_map_normalized.json.bak",
}

DIR = Path(__file__).resolve().parent


# ============================================================
# OCR 残骸分类规则
# ============================================================

# 行号前缀：1r, 3/-o, 45in, 65Medus
NUM_PREFIX = re.compile(r'^\d')

# 纯数字
PURE_NUMBER = re.compile(r'^\d+$')

# 2 字母辅音碎片（OCR 把词内辅音团当独立词）
SHORT_CONSONANT = re.compile(r'^[bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ]{1,2}$')

# 英语词混入（LLPSI 页边注释被 OCR 误识别）
ENGLISH_HINT = re.compile(
    r'^(the|and|for|with|from|this|that|which|book|page|chapter|'
    r'following|note|see|also|grammar|vocab|practice|exercise|'
    r'lesson|part|verb|noun|adj|adv|conj|prep|pron|interj)$',
    re.IGNORECASE
)

# 含非拉丁字符
def has_non_latin(word: str) -> bool:
    """含非拉丁字符（允许拉丁字母+组合附加符）"""
    nfd = unicodedata.normalize("NFD", word)
    for ch in nfd:
        if ch in (" ", "\t", "\n", "-", "'", "’"):
            continue
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat == "Mn":
            continue
        return True
    return False

# 过长（>20 字符大概率是粘连词）
def is_too_long(word: str) -> bool:
    return len(word) > 20

# 纯词尾碎片
SUFFIX_FRAGMENTS = {
    "ārum", "ōrum", "ium", "uum", "arum", "orum",
    "ibus", "ābus", "ēbus",
    "ātur", "ētur", "ītur", "antur", "untur", "intur",
    "ātis", "ētis", "itīs", "untis",
    "ātae", "ātīs", "ōtis",
    "īs", "ās", "ōs", "ēs",
    "que", "ve", "ne",
    "st", "tr", "ct", "sp", "sc", "sq",
}


def classify(word: str) -> str:
    """分类 OCR 残骸类型。返回：clean / num_prefix / pure_number / short_consonant / english / non_latin / too_long / suffix_fragment / camel_joint"""
    if not word or not word.strip():
        return "empty"
    w = word.strip()
    
    if PURE_NUMBER.match(w):
        return "pure_number"
    if NUM_PREFIX.match(w) and len(w) <= 6:
        return "num_prefix"  # 行号或行号+短词
    if SHORT_CONSONANT.match(w):
        return "short_consonant"
    if ENGLISH_HINT.match(w):
        return "english"
    if has_non_latin(w):
        return "non_latin"
    if is_too_long(w):
        return "too_long"
    if w.lower() in SUFFIX_FRAGMENTS:
        return "suffix_fragment"
    
    # 驼峰拼接：两个大写开头（如 Albinumvidet）
    if re.search(r'([A-Z][a-zāăāēĕīĭōŏūŭ]+)([A-Z])', w) and len(w) > 5:
        return "camel_joint"
    
    return "clean"


def main():
    print("=" * 70)
    print("OCR 残骸调研 v1.0 — 不修改任何文件")
    print("=" * 70)
    
    for label, fname in BAK_FILES.items():
        path = DIR / fname
        if not path.exists():
            print(f"\n[跳过] {label}: {fname} 不存在")
            continue
        
        with open(path) as f:
            data = json.load(f)
        
        # 统计分类
        class_counter = Counter()
        class_examples = defaultdict(list)
        chapter_impact = Counter()  # 残骸在每个章节的分布
        for k in data:
            cls = classify(k)
            class_counter[cls] += 1
            if cls != "clean":
                if len(class_examples[cls]) < 5:
                    class_examples[cls].append(k)
                # 影响哪个章节
                v = data[k]
                if isinstance(v, int):
                    chapter_impact[v] += 1
        
        total = len(data)
        clean = class_counter.get("clean", 0)
        garbage = total - clean
        garbage_pct = garbage / total * 100 if total else 0
        
        print(f"\n{'='*70}")
        print(f"  {label} ({fname})")
        print(f"  总条目: {total:,}")
        print(f"  干净: {clean:,} ({100-garbage_pct:.1f}%)")
        print(f"  残骸: {garbage:,} ({garbage_pct:.1f}%)")
        print(f"\n  残骸分类：")
        for cls, cnt in class_counter.most_common():
            if cls == "clean":
                continue
            examples = class_examples.get(cls, [])
            print(f"    {cls:<20}: {cnt:>6,}  例: {examples[:3]}")
        
        # 章节分布影响（前 10 个受影响最严重的章）
        if chapter_impact:
            print(f"\n  残骸影响 top-10 章节：")
            for ch, cnt in sorted(chapter_impact.items(), key=lambda x: -x[1])[:10]:
                print(f"    Cap{ch:>2}: {cnt} 条残骸")


if __name__ == "__main__":
    main()
