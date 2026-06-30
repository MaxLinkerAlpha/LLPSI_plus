#!/usr/bin/env python3
"""
non_latin 深度调研 v2_0_0
逐条检查 form_chapter_map.json.bak 中 non_latin 残骸，
输出子分类 + 真实样例（完整 key→value），供人工评估。
"""

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent
BAK = DIR / "form_chapter_map.json.bak"

with open(BAK) as f:
    data = json.load(f)

# 重新分类 non_latin — 更细粒度的子类型
subtypes = defaultdict(list)

for k, v in data.items():
    # 先确定是否 non_latin
    nfd = unicodedata.normalize("NFD", k)
    non_latin_chars = []
    for i, ch in enumerate(nfd):
        cat = unicodedata.category(ch)
        # 跳过拉丁字母 (L) 和非间距修饰符 (Mn, 如组合附加符)
        if cat.startswith("L") or cat == "Mn" or cat == "Zs":
            continue
        if ch in ("'", "’"):
            continue
        non_latin_chars.append((i, ch, cat))
    if not non_latin_chars:
        continue
    
    # 子分类
    raw = k
    
    # 含句点
    if "." in raw:
        if raw.endswith('."') or raw.endswith(".'"):
            subtypes["dot+quote_end"].append((k, v))
        elif re.search(r'\.\.\.', raw):
            subtypes["ellipsis"].append((k, v))
        elif re.search(r'\.[A-Z]', raw):
            subtypes["dot+sentence_join"].append((k, v))
        else:
            subtypes["dot_other"].append((k, v))
    # 含引号
    elif '"' in raw or "'" in raw or "‘" in raw or "’" in raw or "“" in raw or "”" in raw:
        subtypes["quotes"].append((k, v))
    # 含数字
    elif re.search(r'\d', raw):
        subtypes["contains_digit"].append((k, v))
    # 含斜杠/括号
    elif "/" in raw or "(" in raw or ")" in raw or "[" in raw or "]" in raw:
        subtypes["slash_paren"].append((k, v))
    # 含等号/管道等
    elif "=" in raw or "|" in raw or "~" in raw:
        subtypes["special_char"].append((k, v))
    # 含制表符/换行
    elif "\t" in raw or "\n" in raw:
        subtypes["whitespace"].append((k, v))
    # 含逗号
    elif "," in raw:
        subtypes["comma"].append((k, v))
    # 其他
    else:
        subtypes["other"].append((k, v))

print("=" * 70)
print("non_latin 深度调研 v2.0")
print(f"总 non_latin: {sum(len(v) for v in subtypes.values())} 条")
print("=" * 70)

for stype, entries in sorted(subtypes.items(), key=lambda x: -len(x[1])):
    print(f"\n── {stype}  ({len(entries)} 条) ──")
    sample = entries[:8]
    for k, v in sample:
        # 显示完整 key 和 value
        v_str = str(v)
        if len(v_str) > 40:
            v_str = v_str[:40] + "..."
        print(f'  "{k}"  →  {v_str}')
    if len(entries) > 8:
        print(f"  ... +{len(entries)-8} 条相同类型")

# 额外：检查有没有"可能是真拉丁词但被标点污染"的
print("\n" + "=" * 70)
print("边缘案例：可能移除标点后是合法词")
print("=" * 70)
combined = []
for entries in subtypes.values():
    combined.extend(entries)

salvageable = 0
for k, v in combined:
    # 尝试移除所有非字母字符
    cleaned = re.sub(r'[^A-Za-zāēīōūȳĀĒĪŌŪȲ]', '', k)
    if len(cleaned) >= 2 and not cleaned.isdigit():
        # 检查 cleaned 是否已在干净的键中
        if cleaned.lower() in data:
            salvageable += 1
            if salvageable <= 5:
                print(f'  "{k}" → 清理后 → "{cleaned}" (已在词表中, Cap{v})')
        else:
            salvageable += 1
            if salvageable <= 5:
                print(f'  "{k}" → 清理后 → "{cleaned}" (不在词表中, Cap{v})')
    if salvageable >= 10:
        break
print(f"\n可清理恢复的条目总数: {salvageable}")
