#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终审计: 精确定位 OCR 粘连 + 外来词 + 不合理的短词"""

import json
import re

with open('difficulty_algorithm/word_chapter_map.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keys = list(data.keys())

# ====== 1. 识别 OCR 粘连词 ======
# 启发式: 长度>=12, 不含大写中间字母, 不含连字符, 且包含内部词尾模式
print("=" * 70)
print("1. OCR 粘连词 (多个拉丁词被错误合并)")
print("=" * 70)

# Common Latin inflectional endings that signal word boundaries
ENDINGS = ['que', 'tur', 'ntur', 'mus', 'tis', 'nt', 'rum', 'bus', 'bat',
           'vit', 'bit', 'ris', 'mur', 'mini', 're', 'ndum', 'ns', 'ntem',
           'rumque', 'busque', 'ntque']

ocr_merged = []

for k in keys:
    if len(k) < 12 or '-' in k:
        continue

    # Skip if it has internal uppercase (different issue, possibly valid)
    has_internal_upper = any(c.isupper() for c in k[1:])
    
    # Count common endings that appear in the middle of the word (not at end)
    endings_found = []
    # Check "internal word break" pattern: does this look like concatenation?
    # A concatenation often shows a pattern like: ...us + ...um  or ...is + ...es
    # Check for common patterns
    patterns = [
        (r'(us|um|is|es|am|em|as|os|ae|ei|ii|ibus|ebus|ebat|ebant|avit|ivit|erunt|erant|isse|atus|itus)[a-z]', '词尾后紧跟字母(粘连)'),
    ]
    
    flags = []
    for pat, desc in patterns:
        if re.search(pat, k):
            flags.append(desc)
    
    # Also check: does this word contain recognizable Latin fragments?
    # Almost all these long keys will be from chapters 35-56 (Pensa + later chapters)
    chs = data[k]
    first_ch = min(chs) if chs else 0
    
    if flags:
        ocr_merged.append((k, len(k), first_ch, flags))

# Sort by likelihood: words with internal upper = certain, then by length
ocr_merged.sort(key=lambda x: (-x[1]))

print(f"明确识别为 OCR 粘连: {len(ocr_merged)} 个")
print()

# Separate into "certain" vs "likely"
certain_ocr = []
likely_ocr = []
for k, l, ch, flags in ocr_merged:
    has_upper = any(c.isupper() for c in k[1:])
    # Manual pattern: if the word length >= 15 and it doesn't look like a valid Latin compound
    # Valid compounds: magnificus, circumdatus, etc.
    # OCR merges: words like "sternerestrāvissestratum" have recognizable word breaks
    
    # Heuristic: if the word has more than 2 recognizable word endings embedded,
    # or if length >= 18 (very unlikely for a single Latin word), flag it
    if has_upper or l >= 18:
        certain_ocr.append((k, l, ch, flags))
    else:
        likely_ocr.append((k, l, ch, flags))

print(f"  确认粘连 (len>=18 或含内部大写): {len(certain_ocr)}")
for k, l, ch, flags in certain_ocr:
    print(f"  len={l:2d} ch={ch:2d}  {k}")

print(f"\n  疑似粘连 (12<=len<18, 有内部词尾模式): {len(likely_ocr)}")
for k, l, ch, flags in likely_ocr:
    print(f"  len={l:2d} ch={ch:2d}  {k}")

# ====== 2. 明显的外来词/非拉丁词 ======
print()
print("=" * 70)
print("2. 明显非拉丁语词 (英语/外来词)")
print("=" * 70)

# English words that got into the OCR
NON_LATIN = []
for k in keys:
    issues = []
    # Contains 'w' (not in classical Latin)
    if 'w' in k.lower():
        issues.append("含 'w'")
    # Contains 'k' not in Kalendae/Karthago etc
    if 'k' in k.lower() and not k.lower().startswith('kal') and not k.lower().startswith('kar'):
        issues.append("含 'k'")
    # Looks like English
    if k.lower() in ['following', 'words', 'own', 'book', 'now', 'how', 'show', 'know', 'new', 'few']:
        issues.append("英语词汇")
    # Contains 'oo' (not Latin, except cooptare)
    if 'oo' in k.lower() and k.lower() not in ['cooptare', 'cooptatus', 'coopto']:
        issues.append("含 'oo'")
    if issues:
        NON_LATIN.append((k, data[k], issues))

print(f"疑似非拉丁词: {len(NON_LATIN)}")
for k, chs, issues in NON_LATIN:
    first_ch = min(chs) if chs else '?'
    print(f"  {k:25s} ch={first_ch:2d}  {'; '.join(issues)}")

# ====== 3. 2字母中明显不是拉丁语词的 ======
print()
print("=" * 70)
print("3. 2 字母 key 中明显可疑的")
print("=" * 70)

# All valid Latin prepositions, conjunctions, interjections
VALID_2LETTER = {
    'ab', 'ac', 'ad', 'an', 'at',
    'da', 'de', 'do',
    'ea', 'ei', 'eo', 'es', 'et', 'ex',
    'he', 'hi',
    'id', 'ii', 'in', 'io', 'is', 'it',
    'me', 'mi',
    'ne', 'ni',
    'ob', 'os',
    're', 'ru',
    'se', 'si',
    'te', 'tu',
    'ut',
    've', 'vi',
    # macron variants
    'dē', 'hīc',  # hīc is 3 letters
    'ā', 'ē', 'ī', 'ō', 'ū',
}
# Also abbreviations common in LLPSI margins
VALID_ABBREV = {
    'c.', 'l.', 'p.', 's.', 't.', 'n.', 'm.',
    'cf', 'cp', 'ct',  # confer, comparare, etc.
}

# Actually, let me just look at the ones that are clearly NOT valid
# Invalid patterns: consonant clusters that don't appear in Latin
suspicious_2 = []
for k in sorted([k for k in keys if len(k) == 2]):
    kl = k.lower()
    # Latin 2-letter words are almost always: vowel+consonant, consonant+vowel, or vowel+vowel
    # Consonant+consonant is extremely rare (st, sp are not standalone words)
    vowels = set('aeiouāēīōū')
    c1_is_vowel = kl[0] in vowels
    c2_is_vowel = kl[1] in vowels
    # If both are consonants → suspicious (there's no CV pattern possible)
    # Actually in Latin, preposition/conjunction can be C+C in abbreviations only
    if not c1_is_vowel and not c2_is_vowel:
        suspicious_2.append((k, data[k], "两个都是辅音,不像是独立拉丁词"))

print(f"可疑 2 字母词 (两端都是辅音): {len(suspicious_2)}")
for k, chs, reason in suspicious_2:
    first_ch = min(chs) if chs else '?'
    print(f"  {k:6s} ch={first_ch:2d}  {reason}")

# ====== 4. 含数字或特殊字符的 (more permissive check) ======
print()
print("=" * 70)
print("4. 含括号/标点等特殊字符")
print("=" * 70)

special = []
for k in keys:
    for c in k:
        if ord(c) < 32 or (33 <= ord(c) <= 44) or (46 <= ord(c) <= 47) or (58 <= ord(c) <= 64) or (91 <= ord(c) <= 96) or (123 <= ord(c) <= 126):
            special.append((k, c, ord(c)))
            break

print(f"含特殊符号: {len(special)}")
for k, c, code in special:
    print(f"  {repr(k)}  (字符: '{c}' U+{code:04X})")

# ====== 5. 整体评估 ======
print()
print("=" * 70)
print("5. 质量总结")
print("=" * 70)

total = len(keys)
bad_categories = {
    "OCR粘连 (确认)": len(certain_ocr),
    "OCR粘连 (疑似)": len(likely_ocr),
    "明确非拉丁词": len(NON_LATIN),
    "2字母辅音团": len(suspicious_2),
    "含特殊符号": len(special),
}

# Count unique bad keys (avoid double counting)
bad_keys = set()
for k, *_ in certain_ocr:
    bad_keys.add(k)
for k, *_ in likely_ocr:
    bad_keys.add(k)
for k, *_ in NON_LATIN:
    bad_keys.add(k)
for k, *_ in suspicious_2:
    bad_keys.add(k)
for k, *_ in special:
    bad_keys.add(k)

for cat, cnt in bad_categories.items():
    print(f"  {cat}: {cnt}")

print(f"\n去重后总问题 key 数: {len(bad_keys)}")
print(f"总 key 数: {total}")
print(f"格式/字符层面正确率: {(total - len(bad_keys)) / total * 100:.2f}%")

# Note about OCR quality
print(f"\n重要提示:")
print(f"  - 上述统计仅覆盖了明确的格式/字符异常")
print(f"  - OCR 的「字母级」错误 (如 causå → causā, cũ → cum 等) 无法通过脚本检测")
print(f"  - OCR 粘连词 (如 sternerestrāvissestratum) 是本书 OCR 的常见问题")
print(f"  - 这些粘连词发生在前35章之后的比例很大，可能因为后半部分排版更密")
