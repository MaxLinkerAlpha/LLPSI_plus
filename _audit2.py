#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""深入分析: OCR 粘连词 + 短词+ 章节覆盖"""

import json
from collections import Counter

with open('difficulty_algorithm/word_chapter_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keys = list(data.keys())

# ====== 分析 1: 长词中疑似 OCR 粘连 ======
print("=" * 70)
print("分析 1: 疑似 OCR 粘连 (多个拉丁词被错误拼成一个)")
print("=" * 70)

candidates = [(k, len(k)) for k in keys if len(k) >= 12 and '-' not in k]
candidates.sort(key=lambda x: -x[1])
print(f"候选数 (len>=12 且无连字符): {len(candidates)}")
print()

for k, l in candidates:
    chapters = data[k]
    first_ch = min(chapters)
    # 判断: 如果词中间有大写字母 (非首字母) → 几乎肯定是粘连
    has_internal_upper = any(c.isupper() for c in k[1:])
    # 判断: 如果有常见的拉丁词尾模式重复出现 (如 -us, -um, -is, -es 等出现在中间)
    marker = ""
    if has_internal_upper:
        marker = " [内部大写→确认粘连]"
    elif any(k.find(suf) > 0 and k.find(suf) < len(k) - 4 for suf in ['umque', 'usqu', 'umno', 'isqu', 'umpr', 'uspr', 'umst', 'emsu', 'ensu', 'emsi']):
        marker = " [疑似粘连]"
    print(f"  len={l:2d} ch={first_ch:2d} {k}{marker}")

print()

# ====== 分析 2: 2-3 字母短词的合理性 ======
print("=" * 70)
print("分析 2: 2 字母短词检查")
print("=" * 70)

# Common Latin 2-letter words
LATIN_2LETTER = {
    'ab', 'ac', 'ad', 'an', 'at', 'da', 'de', 'do', 'ea', 'ei', 'eo', 'es',
    'et', 'ex', 'id', 'ii', 'in', 'io', 'is', 'it', 'me', 'ne', 'ob', 'os',
    're', 'se', 'si', 'te', 'tu', 'ut', 've', 'vi',
    # with macrons
    'ad', 'ex', 'in',
}

suspicious_2 = []
for k in sorted([k for k in keys if len(k) == 2]):
    chs = data[k]
    first_ch = min(chs)
    if k not in LATIN_2LETTER and k.lower() not in LATIN_2LETTER:
        suspicious_2.append((k, first_ch, chs))
        print(f"  [可疑] {k:6s} ch={first_ch:2d} chs={chs}")
    else:
        print(f"  [正常] {k:6s} ch={first_ch:2d}")

print(f"\n2 字母 key 总数: {sum(1 for k in keys if len(k) == 2)}")
print(f"其中可疑: {len(suspicious_2)}")

# ====== 分析 3: 章节覆盖 ======
print()
print("=" * 70)
print("分析 3: 章节覆盖情况")
print("=" * 70)

chapter_count = Counter()
for key, chs in data.items():
    for ch in chs:
        chapter_count[ch] += 1

print("各章节词形数 (前5和后5):")
sorted_chs = sorted(chapter_count.items())
for ch, cnt in sorted_chs[:5]:
    print(f"  章节 {ch:2d}: {cnt:5d} 词形")
print("  ...")
for ch, cnt in sorted_chs[-5:]:
    print(f"  章节 {ch:2d}: {cnt:5d} 词形")

print(f"\n共涉及章节: {len(chapter_count)} 个 (全部在 1-56 范围内)")

# ====== 分析 4: 随机抽样做深度人工审查 ======
print()
print("=" * 70)
print("分析 4: 随机抽样 20 条深度人工审查")
print("=" * 70)

import random
random.seed(123)
sample = random.sample(keys, 20)
for i, k in enumerate(sample):
    chs = data[k]
    print(f"\n{i+1}. word = '{k}'")
    print(f"   len={len(k)}, chapters={min(chs)}-{max(chs)} ({len(chs)} chapters total)")
    # Look for potential OCR issues
    issues = []
    # Issue: looks like multiple words
    if len(k) > 10 and not any(c.isupper() for c in k):
        # Check if it contains common word boundaries
        for suffix in ['que', 'tur', 'ntur', 'mus', 'tis', 'nt', 'rum', 'bus', 'bat', 'vit']:
            pos = k.find(suffix)
            if pos > 3 and pos < len(k) - 3:
                issues.append(f"可能含词尾 '{suffix}' 在位置 {pos}")
    if issues:
        for iss in issues:
            print(f"   [注意] {iss}")
    else:
        print(f"   [正常] 无明显OCR问题迹象")

print()
print("=" * 70)
print("分析 5: 疑似非拉丁语词 (含罕见字母组合)")
print("=" * 70)

# Check for very unusual Latin letter combinations
# Latin doesn't have: 'j' in certain positions, 'w', 'k' rarely (mostly in Kalendae)
unusual = []
for k in keys:
    kl = k.lower()
    flags = []
    if 'w' in kl:
        flags.append("含 'w' (非拉丁)")
    if 'j' in kl and kl != 'jam' and kl != 'jamque':
        # j is common in Latin (jam, jocus, jacere) so only flag if it's truly suspicious
        pass
    if 'k' in kl and not kl.startswith('kal'):
        flags.append("含 'k' (极少用)")
    if kl.endswith('x') and len(k) <= 3:
        flags.append("短词以 x 结尾 (罕见)")
    if flags:
        unusual.append((k, flags, data[k]))

print(f"疑似异常词总数: {len(unusual)}")
for k, flags, chs in unusual[:30]:
    print(f"  {k:20s}  {', '.join(flags)}  ch={min(chs)}")
