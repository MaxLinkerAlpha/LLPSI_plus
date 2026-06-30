#!/usr/bin/env python3
"""
4 文件清理质量验证 v1_0_0
对比每个文件的原版 vs cleaned 版本
"""

import json, re, random
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent

FILES = [
    "form_chapter_map.json",
    "lemma_chapter_map.json",
    "word_lemma_map.json",
    "word_chapter_map_normalized.json",
]

LATIN_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                  "\u0101\u0113\u012B\u014D\u016B\u0233\u01E2"
                  "\u0100\u0112\u012A\u014C\u016A\u0232")

def is_pure_latin(w):
    return all(c in LATIN_CHARS for c in w) and len(w) >= 2

def strip_macrons(w):
    return re.sub(r"[āēīōūȳĀĒĪŌŪȲǣǞ]",
                  lambda m: "aeiouyAEIOUYæÆ"["āēīōūȳĀĒĪŌŪȲǣǞ".index(m.group(0))], w).lower()

print("=" * 70)
print("4 文件清理质量验证")
print("=" * 70)

for fname in FILES:
    orig_path = DIR / fname
    clean_path = DIR / fname.replace(".json", "_cleaned.json")

    with open(orig_path) as f: orig = json.load(f)
    with open(clean_path) as f: clean = json.load(f)

    print(f"\n{'='*70}")
    print(f"[{fname}]")
    print(f"  原始: {len(orig):,} → 清理: {len(clean):,}  (变化 {len(clean)-len(orig):+,d})")
    print(f"{'='*70}")

    # 1. 误删检查
    deleted_keys = [k for k in orig if k not in clean]
    false_pos = []
    for k in deleted_keys:
        if is_pure_latin(k) and 3 <= len(k) <= 15:
            # 排除2字符碎片
            has_vowel = any(c in "aeiouyāēīōūȳAEIOUYĀĒĪŌŪȲ" for c in k)
            if has_vowel:
                false_pos.append((k, orig[k]))

    print(f"  [1] 误删检查: 疑似合法拉丁词被删: {len(false_pos)}")
    if false_pos:
        false_pos.sort(key=lambda x: len(x[0]))
        for k, v in false_pos[:8]:
            print(f'      "{k}" → {v}')

    # 2. 值篡改检查
    modified = []
    for k in orig:
        if k in clean and orig[k] != clean[k]:
            modified.append((k, orig[k], clean[k]))
    print(f"  [2] 值篡改: {len(modified)} 处")
    if modified:
        for k, o, c in modified[:5]:
            print(f'      "{k}": {o} → {c}')

    # 3. 抢救新增词质量
    new_keys = [k for k in clean if k not in orig]
    bad_new = [k for k in new_keys if not is_pure_latin(k) or len(k) < 3]
    print(f"  [3] 抢救新增: {len(new_keys)} 条, 疑似异常: {len(bad_new)}")
    if bad_new:
        for k in bad_new[:5]:
            print(f'      "{k}" → {clean[k]}')

# === 真实故事覆盖率测试 ===
print(f"\n{'='*70}")
print("[真实故事覆盖率测试] form_chapter_map")
print(f"{'='*70}")

with open(DIR / "form_chapter_map.json") as f: orig_fcm = json.load(f)
with open(DIR / "form_chapter_map_cleaned.json") as f: clean_fcm = json.load(f)

def coverage(text, form_map):
    tokens = re.findall(r"[A-Za-z\u0100-\u0233]+", text)
    unique = set(tokens)
    if not unique: return 0
    matched = 0
    for w in unique:
        if strip_macrons(w) in form_map:
            matched += 1
    return matched / len(unique) * 100

base = Path("../AI_reader/realitates")
test_stories = []
for cap_dir in sorted(base.iterdir())[:10]:
    if cap_dir.is_dir():
        mds = list(cap_dir.glob("*.md"))[:2]
        test_stories.extend(mds)

print(f"  测试 {len(test_stories)} 篇故事")
print(f"  {'故事':<50} {'原始':>8} {'清理':>8} {'变化':>8}")
total_orig = 0
total_clean = 0
for p in test_stories:
    text = p.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    cov_o = coverage(text, orig_fcm)
    cov_c = coverage(text, clean_fcm)
    total_orig += cov_o
    total_clean += cov_c
    diff = cov_c - cov_o
    mark = "↑" if diff > 0 else ("↓" if diff < 0 else "=")
    name = f"{p.parent.name}/{p.name[:30]}"
    print(f"  {name:<50} {cov_o:>7.1f}% {cov_c:>7.1f}% {diff:>+7.1f} {mark}")

n = len(test_stories)
print(f"\n  平均覆盖率: 原始 {total_orig/n:.1f}% → 清理 {total_clean/n:.1f}%  (变化 {total_clean/n - total_orig/n:+.1f}%)")
