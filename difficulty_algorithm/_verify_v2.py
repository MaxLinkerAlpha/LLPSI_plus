#!/usr/bin/env python3
"""
清理质量深度验证 v2_0_0
对比 form_chapter_map.json (原) vs form_chapter_map_cleaned.json (清理后)
逐项核查：误删、误改、丢失章节、抢救质量
"""

import json, random, re
from collections import Counter

with open("form_chapter_map.json") as f: orig = json.load(f)
with open("form_chapter_map_cleaned.json") as f: clean = json.load(f)

print("=" * 70)
print("清理质量深度验证 v2.0")
print("=" * 70)
print(f"原始: {len(orig):,} 条")
print(f"清理: {len(clean):,} 条")
print(f"变化: {len(clean)-len(orig):+,d} 条 ({(len(clean)-len(orig))/len(orig)*100:+.1f}%)")
print()

# ============================================================
# 1. 双向对比 — 找出所有"消失的键"和"新增的键"
# ============================================================
print("=" * 70)
print("[1] 双向键对比")
print("=" * 70)
deleted_keys = [k for k in orig if k not in clean]
new_keys = [k for k in clean if k not in orig]
print(f"消失的键: {len(deleted_keys):,}")
print(f"新增的键: {len(new_keys):,}")

# ============================================================
# 2. 误删检查 — 消失的键中，哪些看起来是合法拉丁词
# ============================================================
print()
print("=" * 70)
print("[2] 误删检查 — 消失的键中疑似合法拉丁词")
print("=" * 70)

latin_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\u0101\u0113\u012B\u014D\u016B\u0233\u01E2\u0100\u0112\u012A\u014C\u016A\u0232")
def is_pure_latin(w):
    return all(c in latin_chars for c in w) and len(w) >= 2

false_positives = []
for k in deleted_keys:
    if is_pure_latin(k):
        # 进一步检查：长度合理、含元音、不是明显碎片
        has_vowel = any(c in "aeiouy\u0101\u0113\u012B\u014D\u016B\u0233AEIOUY" for c in k)
        if has_vowel and 3 <= len(k) <= 15:
            false_positives.append((k, orig[k]))

print(f"疑似合法拉丁词被删: {len(false_positives)} 条 (共 {len(deleted_keys)} 删除中)")
if false_positives:
    # 按长度排序，短的更可能是真词
    false_positives.sort(key=lambda x: len(x[0]))
    print(f"\n前 20 条最短的疑似误删:")
    for k, v in false_positives[:20]:
        print(f'  "{k}" → Cap{v}  (len={len(k)})')

# ============================================================
# 3. 章节号篡改检查 — 保留的键是否章节号被改了
# ============================================================
print()
print("=" * 70)
print("[3] 章节号篡改检查 — 保留键的值是否被修改")
print("=" * 70)
modified_values = []
for k in orig:
    if k in clean and orig[k] != clean[k]:
        modified_values.append((k, orig[k], clean[k]))
print(f"章节号被修改的键: {len(modified_values)}")
if modified_values:
    for k, old, new in modified_values[:10]:
        print(f'  "{k}": Cap{old} → Cap{new}')

# ============================================================
# 4. 抢救词质量 — 新增的键是否合法
# ============================================================
print()
print("=" * 70)
print("[4] 抢救新增词质量")
print("=" * 70)
print(f"新增总数: {len(new_keys)}")

# 分类新增词
good_rescue = []  # 纯拉丁字母，3-15字符
bad_rescue = []   # 含异常字符
for k in new_keys:
    if is_pure_latin(k) and 3 <= len(k) <= 15:
        good_rescue.append((k, clean[k]))
    else:
        bad_rescue.append((k, clean[k]))

print(f"  合法拉丁词形: {len(good_rescue)} ({len(good_rescue)/len(new_keys)*100:.0f}%)")
print(f"  疑似异常: {len(bad_rescue)} ({len(bad_rescue)/len(new_keys)*100:.0f}%)")
if bad_rescue:
    print(f"\n  异常样例:")
    for k, v in bad_rescue[:10]:
        print(f'    "{k}" → Cap{v}')

# ============================================================
# 5. 章节覆盖度 — 清理后每章的词条数对比
# ============================================================
print()
print("=" * 70)
print("[5] 章节覆盖度对比 (前 15 章)")
print("=" * 70)
orig_chap = Counter()
clean_chap = Counter()
for k, v in orig.items():
    ch = min(v) if isinstance(v, list) else v
    orig_chap[ch] += 1
for k, v in clean.items():
    ch = min(v) if isinstance(v, list) else v
    clean_chap[ch] += 1

print(f"  章    原始    清理    变化")
for ch in sorted(set(orig_chap) | set(clean_chap))[:35]:
    o = orig_chap.get(ch, 0)
    c = clean_chap.get(ch, 0)
    diff = c - o
    marker = "⚠️" if diff < -50 else ""
    print(f"  Cap{ch:>2}  {o:>5}  {c:>5}  {diff:>+5}  {marker}")

# ============================================================
# 6. 真实故事命中率测试 — 用 5 篇故事对比清理前后覆盖率
# ============================================================
print()
print("=" * 70)
print("[6] 真实故事命中率测试")
print("=" * 70)
import sys, re, unicodedata
sys.path.insert(0, ".")

def strip_macrons(w):
    return re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()

def coverage(text, form_map):
    tokens = re.findall(r"[A-Za-z\u0100-\u0233]+", text)
    unique = set(tokens)
    matched = 0
    for w in unique:
        clean_w = strip_macrons(w)
        if clean_w in form_map:
            matched += 1
    return matched / len(unique) * 100 if unique else 0

from pathlib import Path
test_stories = [
    "Cap1/Cap1_Īnsulae_Graecae_brevis_020.md",
    "Cap5/Cap5_Duo_puerī_medius_003.md",
    "Cap10/Cap10_finis_viae_brevis_001.md",
    "Cap17/Cap17_Faber_et_gladius_medius_054.md",
    "Cap25/Cap25_Quattuor_Īnsulae_brevis_001.md",
]
base = Path("../AI_reader/realitates")
print(f"  故事                                       原始覆盖率  清理后覆盖率  变化")
for rel in test_stories:
    p = base / rel
    if not p.exists():
        print(f"  {rel}  — 文件不存在")
        continue
    text = p.read_text(encoding="utf-8")
    if text.startswith("---"):
        text = text.split("---", 2)[2]
    cov_orig = coverage(text, orig)
    cov_clean = coverage(text, clean)
    diff = cov_clean - cov_orig
    mark = "↑" if diff > 0 else ("↓" if diff < 0 else "=")
    print(f"  {rel:<45}  {cov_orig:>5.1f}%      {cov_clean:>5.1f}%       {diff:+.1f} {mark}")
