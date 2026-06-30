#!/usr/bin/env python3
"""
Step 1: 合并 word_lemma_map.json + lemma_chapter_map.json → form_chapter_map.json
       再用 word_chapter_map.json（OCR 直接观测）兜底未覆盖的词形。
       零外部依赖，运行时纯 dict.get() 查表。
"""

import json
from pathlib import Path

DIR = Path(__file__).resolve().parent

# 加载三张表
with open(DIR / "word_lemma_map.json", encoding="utf-8") as f:
    word_lemma = json.load(f)          # {词形: 原形}  20,944 条

with open(DIR / "lemma_chapter_map.json", encoding="utf-8") as f:
    lemma_chapter = json.load(f)       # {原形: 章节号} 14,613 条

with open(DIR / "word_chapter_map.json", encoding="utf-8") as f:
    word_chapter = json.load(f)        # {词形: 章节号} 16,665 条 (OCR 直接观测)

# 合成: 词形 → 原形 → 章节（取最早章节）
form_chapter = {}
lemma_miss = 0

for form, lemma in word_lemma.items():
    ch = lemma_chapter.get(lemma)
    if ch is not None:
        # 如果值是列表，取最小值
        form_chapter[form] = min(ch) if isinstance(ch, list) else ch
    else:
        lemma_miss += 1

print(f"word_lemma → lemma_chapter 合成: {len(form_chapter)} 条")

# 兜底: word_chapter_map.json（OCR 直接观测的，冲突时优先）
# 原因：OCR 观测是"实际出现了"，比还原推断更可靠
added_from_ocr = 0
for form, ch in word_chapter.items():
    if form not in form_chapter:
        form_chapter[form] = min(ch) if isinstance(ch, list) else ch
        added_from_ocr += 1

print(f"word_chapter_map 兜底补充: {added_from_ocr} 条")
print(f"最终 form_chapter_map: {len(form_chapter)} 条")
print(f"原形不在章节表: {lemma_miss} 条")

# 保存
dst = DIR / "form_chapter_map.json"
with open(dst, "w", encoding="utf-8") as f:
    json.dump(form_chapter, f, ensure_ascii=False)

import os
size_kb = os.path.getsize(dst) / 1024
print(f"已保存 → {dst.name}  ({size_kb:.0f} KB)")