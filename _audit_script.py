#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""word_chapter_map.json 质量审计脚本"""

import json
import re
import random
from collections import Counter

FILEPATH = '/Users/max/Downloads/Projects/LLPSI_plus/difficulty_algorithm/word_chapter_map.json'

with open(FILEPATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

total = len(data)
print(f"总条目数: {total}")
print()

# ========== 1. 全面扫描所有 key ==========
issues = {
    "empty_key": [],
    "non_latin_chars": [],
    "all_punctuation": [],
    "contains_digit": [],
    "too_long": [],
    "too_short": [],
    "leading_trailing_space": [],
}

# Latin characters range: basic Latin + common Latin diacritics + hyphen
LATIN_OK = set(
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'āēīōūȳĀĒĪŌŪȲ'
    'áéíóúýÁÉÍÓÚÝ'
    'àèìòùÀÈÌÒÙ'
    'äëïöüÿÄËÏÖÜŸ'
    'âêîôûÂÊÎÔÛ'
    'ãñõÃÑÕ'
    'çÇœŒæÆ'
    '-'
)

for key, chapters in data.items():
    if key == "" or key is None:
        issues["empty_key"].append(key)
        continue

    if key != key.strip():
        issues["leading_trailing_space"].append(key)

    stripped = key.strip()
    length = len(stripped)

    if length > 30:
        issues["too_long"].append((key, length))
    if length == 1:
        issues["too_short"].append(key)

    non_latin = [c for c in stripped if c not in LATIN_OK]
    if non_latin:
        issues["non_latin_chars"].append((key, ''.join(sorted(set(non_latin)))))

    if re.fullmatch(r'[\W_]+', stripped):
        issues["all_punctuation"].append(key)

    if re.search(r'\d', stripped):
        issues["contains_digit"].append(key)

# ========== 2. 章节号范围检查 ==========
chapter_issues = {
    "not_list": [],
    "empty_list": [],
    "bad_chapter": [],
    "non_int_chapter": [],
}

for key, chapters in data.items():
    if not isinstance(chapters, list):
        chapter_issues["not_list"].append((key, type(chapters).__name__))
        continue
    if len(chapters) == 0:
        chapter_issues["empty_list"].append(key)
        continue
    for ch in chapters:
        if not isinstance(ch, int):
            chapter_issues["non_int_chapter"].append((key, ch, type(ch).__name__))
        elif ch < 1 or ch > 56:
            chapter_issues["bad_chapter"].append((key, ch))

# ========== 3. 打印全量扫描结果 ==========
print("=" * 70)
print("全量扫描结果")
print("=" * 70)

print(f"\n空字符串 key: {len(issues['empty_key'])}")
print(f"前后有空格 key: {len(issues['leading_trailing_space'])}")
if issues['leading_trailing_space']:
    for k in issues['leading_trailing_space'][:10]:
        print(f"  -> {repr(k)}")

print(f"\n含非拉丁字符 key: {len(issues['non_latin_chars'])}")
if issues['non_latin_chars']:
    for k, chars in issues['non_latin_chars'][:30]:
        print(f"  -> {repr(k)}  含字符: {chars}")

print(f"\n纯标点符号 key: {len(issues['all_punctuation'])}")
if issues['all_punctuation']:
    for k in issues['all_punctuation'][:10]:
        print(f"  -> {repr(k)}")

print(f"\n含数字 key: {len(issues['contains_digit'])}")
if issues['contains_digit']:
    for k in issues['contains_digit'][:10]:
        print(f"  -> {repr(k)}")

print(f"\n过短 (长度=1) key: {len(issues['too_short'])}")
if issues['too_short']:
    for k in issues['too_short'][:20]:
        print(f"  -> {repr(k)}")

print(f"过长 (>30) key: {len(issues['too_long'])}")
if issues['too_long']:
    for k, l in issues['too_long'][:10]:
        print(f"  -> len={l}: {repr(k[:80])}")

print(f"\n章节值非列表: {len(chapter_issues['not_list'])}")
if chapter_issues['not_list']:
    for k, t in chapter_issues['not_list'][:5]:
        print(f"  -> {repr(k)}: type={t}")
print(f"章节列表为空: {len(chapter_issues['empty_list'])}")
print(f"章节值非整数: {len(chapter_issues['non_int_chapter'])}")
if chapter_issues['non_int_chapter']:
    for k, ch, t in chapter_issues['non_int_chapter'][:5]:
        print(f"  -> {repr(k)}: ch={repr(ch)} type={t}")
print(f"章节号超出 1-56: {len(chapter_issues['bad_chapter'])}")
if chapter_issues['bad_chapter']:
    bad_counter = Counter()
    for k, ch in chapter_issues['bad_chapter']:
        bad_counter[ch] += 1
    print("  章节号分布:")
    for ch, cnt in sorted(bad_counter.items()):
        print(f"    章节 {ch}: {cnt} 次")
    for k, ch in chapter_issues['bad_chapter'][:10]:
        print(f"  -> {repr(k)}: 章节 {ch}")

# ========== 4. 随机抽样 300 条 ==========
print()
print("=" * 70)
print("随机抽样 300 条检查")
print("=" * 70)

random.seed(42)
keys = list(data.keys())
sample_keys = random.sample(keys, min(300, len(keys)))

valid_count = 0
dubious_count = 0
dubious_samples = []
non_latin_subset = set()
digit_subset = set()
punct_subset = set()
long_subset = set()
short_dubious_subset = set()

for key in sample_keys:
    stripped = key.strip()
    problems = []

    non_latin = [c for c in stripped if c not in LATIN_OK]
    if non_latin:
        problems.append(f"含非拉丁字符: {''.join(set(non_latin))}")
        non_latin_subset.add(key)

    if re.search(r'\d', stripped):
        problems.append("含数字")
        digit_subset.add(key)

    if len(stripped) > 25:
        problems.append(f"过长({len(stripped)})")
        long_subset.add(key)

    if re.fullmatch(r'[\W_]+', stripped):
        problems.append("纯标点")
        punct_subset.add(key)

    if len(stripped) == 1 and stripped.isalpha() and stripped.lower() not in 'āēīōūȳaeiou':
        problems.append(f"可疑单字符非元音")
        short_dubious_subset.add(key)

    chs = data[key]
    if isinstance(chs, list):
        if len(chs) == 0:
            problems.append("章节列表空")
        else:
            bad_chs = [c for c in chs if not isinstance(c, int) or c < 1 or c > 56]
            if bad_chs:
                problems.append(f"异常章节: {bad_chs[:5]}")

    if problems:
        dubious_count += 1
        ch_str = str(chs[:5]) + ('...' if isinstance(chs, list) and len(chs) > 5 else '')
        dubious_samples.append((key, problems, ch_str))
    else:
        valid_count += 1

print(f"\n样本量: {len(sample_keys)}")
print(f"通过 (无明显问题): {valid_count} ({valid_count/len(sample_keys)*100:.1f}%)")
print(f"可疑: {dubious_count} ({dubious_count/len(sample_keys)*100:.1f}%)")

print(f"\n--- 典型问题样本 ---")
for i, (key, problems, ch_str) in enumerate(dubious_samples[:30]):
    print(f"\n{i+1}. key = {repr(key)}")
    print(f"   问题: {'; '.join(problems)}")
    print(f"   章节: {ch_str}")

# ========== 5. 总体正确率估算 ==========
print()
print("=" * 70)
print("总体质量评估")
print("=" * 70)

# Clean key count
bad_key_set = set()
for k in issues['empty_key']:
    bad_key_set.add(k)
for k, _ in issues['non_latin_chars']:
    bad_key_set.add(k)
for k in issues['all_punctuation']:
    bad_key_set.add(k)
for k, _ in issues['too_long']:
    bad_key_set.add(k)

clean_keys = total - len(bad_key_set)
print(f"\n明确有问题的 key: {len(bad_key_set)} ({len(bad_key_set)/total*100:.2f}%)")
print(f"无明显问题的 key: {clean_keys} ({clean_keys/total*100:.2f}%)")

# Note: too_short (len=1) are mostly single Latin letters like 'a', 'e', 'i' etc.
# These are generally valid (prepositions, interjections in Latin)
# So we don't count them as "bad"
single_letter_ok = len(issues['too_short'])
print(f"单字母 key (通常有效,如 'e'=从, 'a'=从): {single_letter_ok}")

# Chapter issues (these affect values, not keys)
total_bad_chapters = len(chapter_issues['bad_chapter']) + len(chapter_issues['non_int_chapter'])
print(f"章节值异常: {total_bad_chapters} 处")

# Estimate: keys are ~99%+ good; the real question is OCR quality on the word forms themselves
# But we can't detect that without a Latin dictionary
print(f"\n--- 整体判断 ---")
print(f"结构完整性: {'正常' if len(chapter_issues['not_list']) == 0 else '有问题'}")
print(f"章节范围: {'有小量异常' if chapter_issues['bad_chapter'] else '正常'}")
print(f"Key 数据: {len(bad_key_set)} 个明显脏数据 (多为 O定扫描错误混入的标点/数字/符号)")
print(f"估算 key 层面正确率: {(total - len(bad_key_set)) / total * 100:.2f}%")
print(f"\n注意: 以上仅检测了明显的格式/字符异常。OCR 导致的拉丁字母错识")
print(f"(如把 cl 识成 d, rn 识成 m 等) 无法通过此脚本检测,需要对照拉丁语词典验证。")
