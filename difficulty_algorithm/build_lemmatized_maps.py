#!/usr/bin/env python3
"""
Step 1: 将 LLPSI 的 20,944 个词形通过 simplemma 做词形还原，
        构建 word→lemma 和 lemma→chapter 映射表。
"""

import json
import sys
from collections import defaultdict

import simplemma

WORD_MAP = "word_chapter_map.json"
DST_WORD_LEMMA = "word_lemma_map.json"
DST_LEMMA_CHAPTER = "lemma_chapter_map.json"

# 加载已有词形→章节映射
with open(WORD_MAP, encoding="utf-8") as f:
    word_chapter = json.load(f)

print(f"加载词形→章节: {len(word_chapter)} 条")

# 词形还原
word_lemma = {}          # 词形 → 原形
lemma_chapter = {}       # 原形 → 最早章节号
lemma_forms = defaultdict(set)  # 原形 → 该原形的所有词形（调试用）
no_lemma_count = 0       # 还原失败的词形数

for i, (word, chapter) in enumerate(word_chapter.items()):
    try:
        lemma = simplemma.lemmatize(word, lang="la")
    except Exception:
        lemma = word  # 还原失败，用自身作原形
        no_lemma_count += 1

    word_lemma[word] = lemma
    lemma_forms[lemma].add(word)

    # 保留最早出现的章节号
    if lemma not in lemma_chapter or chapter < lemma_chapter[lemma]:
        lemma_chapter[lemma] = chapter

    if (i + 1) % 5000 == 0:
        print(f"  已处理 {i+1}/{len(word_chapter)} ...")

print(f"词形→原形映射: {len(word_lemma)} 条")
print(f"原形→章节映射: {len(lemma_chapter)} 条")
print(f"原形类别数: {len(lemma_forms)}")
print(f"还原失败: {no_lemma_count} 条")

# 保存
with open(DST_WORD_LEMMA, "w", encoding="utf-8") as f:
    json.dump(word_lemma, f, ensure_ascii=False, indent=2)
print(f"已保存 → {DST_WORD_LEMMA}")

with open(DST_LEMMA_CHAPTER, "w", encoding="utf-8") as f:
    # 按章节号排序输出
    sorted_data = dict(sorted(lemma_chapter.items(), key=lambda x: x[1]))
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)
print(f"已保存 → {DST_LEMMA_CHAPTER}")

# 验证：与 FR 官方原形列表对比
with open("fr_lemmas.json", encoding="utf-8") as f:
    fr_lemmas = set(json.load(f))
print(f"\nFR 官方原形: {len(fr_lemmas)}")

our_lemmas = set(lemma_chapter.keys())
overlap = our_lemmas & fr_lemmas
only_ours = our_lemmas - fr_lemmas
only_fr = fr_lemmas - our_lemmas
print(f"交集（双方一致）: {len(overlap)}")
print(f"仅 simplemma 输出: {len(only_ours)}")
print(f"仅 FR 单词表: {len(only_fr)}")
print(f"simplemma 覆盖 FR 单词表的: {len(overlap)/len(fr_lemmas)*100:.1f}%")
