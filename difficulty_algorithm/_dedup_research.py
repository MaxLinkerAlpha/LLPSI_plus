#!/usr/bin/env python3
"""
算法文件重复词 + 进一步清理潜力调研 v1_0_0
检查 4 个 JSON 算法文件：
  1. 完全重复键（含大小写/长音变体）
  2. 还能清理的残留
只报告，不修改。
"""

import json, re, unicodedata
from collections import defaultdict, Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent

FILES = [
    "form_chapter_map.json",
    "lemma_chapter_map.json",
    "word_lemma_map.json",
    "word_chapter_map_normalized.json",
]

def strip_macrons(w):
    return re.sub(r"[āēīōūȳĀĒĪŌŪȲǣǞ]", lambda m: "aeiouyAEIOUYæÆ"[ "āēīōūȳĀĒĪŌŪȲǣǞ".index(m.group(0)) ], w)

def is_pure_latin(w):
    latin = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\u0101\u0113\u012B\u014D\u016B\u0233\u01E2\u0100\u0112\u012A\u014C\u016A\u0232")
    return all(c in latin for c in w) and len(w) >= 2

print("=" * 70)
print("算法文件重复词 + 清理潜力调研")
print("=" * 70)

for fname in FILES:
    path = DIR / fname
    if not path.exists():
        print(f"\n[{fname}] 文件不存在，跳过")
        continue
    with open(path, encoding="utf-8") as f:
        # 检查原始文件中的重复键（JSON 解析会自动去重，需用原始方式检测）
        f.seek(0)
        raw = f.read()
    
    # 重新加载（json 会保留最后一个键）
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"\n{'='*70}")
    print(f"[{fname}]  总条目: {len(data):,}")
    print(f"{'='*70}")
    
    # === 1. 检测 JSON 重复键（raw 文本层面）===
    # JSON 标准下重复键行为未定义，Python json 默认保留最后一个
    # 我们用正则提取所有顶层键，看是否有重复
    key_pattern = re.compile(r'^\s*"([^"]+)"\s*:', re.MULTILINE)
    all_keys_raw = key_pattern.findall(raw)
    key_counts = Counter(all_keys_raw)
    true_dupes = {k: c for k, c in key_counts.items() if c > 1}
    print(f"\n[1] JSON 原始重复键: {len(true_dupes)} 个")
    if true_dupes:
        for k, c in list(true_dupes.items())[:10]:
            print(f'    "{k}" 出现 {c} 次')
    
    # === 2. 大小写变体重复（Roma vs roma）===
    lower_map = defaultdict(list)
    for k in data:
        lower_map[k.lower()].append(k)
    case_dupes = {k: vs for k, vs in lower_map.items() if len(vs) > 1}
    print(f"\n[2] 大小写变体重复: {len(case_dupes)} 组")
    sample_count = 0
    for k, vs in list(case_dupes.items())[:15]:
        if sample_count >= 10: break
        vals = [(v, data[v]) for v in vs]
        print(f'    {vs} → {vals}')
        sample_count += 1
    
    # === 3. 长音变体重复（amō vs amo）===
    macron_map = defaultdict(list)
    for k in data:
        stripped = strip_macrons(k).lower()
        macron_map[stripped].append(k)
    macron_dupes = {k: vs for k, vs in macron_map.items() if len(vs) > 1}
    print(f"\n[3] 长音/大小写变体重复: {len(macron_dupes)} 组")
    sample_count = 0
    for k, vs in list(macron_dupes.items())[:15]:
        if sample_count >= 10: break
        vals = [(v, data[v]) for v in vs]
        # 只显示有差异的
        if len(set(str(v) for _, v in vals)) > 1 or len(vs) > 1:
            print(f'    "{k}": {vals}')
            sample_count += 1
    
    # === 4. 还能清理的残留 ===
    print(f"\n[4] 还能清理的残留:")
    
    # 4a. 单字符键
    single_char = [k for k in data if len(k) == 1]
    print(f"    单字符键: {len(single_char)} 条  样例: {single_char[:10]}")
    
    # 4b. 含空格的键
    with_space = [k for k in data if " " in k]
    print(f"    含空格键: {len(with_space)} 条  样例: {with_space[:5]}")
    
    # 4c. 含特殊字符（非拉丁字母、非连字符）
    special = []
    for k in data:
        if not is_pure_latin(k) and "-" not in k:
            special.append(k)
    print(f"    含非拉丁字符键: {len(special)} 条  样例: {special[:10]}")
    
    # 4d. 含连字符但非管道/斜杠
    hyphen_only = [k for k in data if "-" in k and "|" not in k and "/" not in k]
    print(f"    含连字符键: {len(hyphen_only)} 条  样例: {hyphen_only[:10]}")
    
    # 4e. 2字符词（可能是碎片）
    two_char = [k for k in data if len(k) == 2 and is_pure_latin(k)]
    print(f"    2字符拉丁键: {len(two_char)} 条  样例: {two_char[:20]}")
    
    # 4f. 超长词（>20字符，可能是粘连）
    too_long = [k for k in data if len(k) > 20]
    print(f"    超长键 (>20字符): {len(too_long)} 条  样例: {too_long[:5]}")
    
    # 4g. 纯数字
    pure_num = [k for k in data if k.isdigit()]
    print(f"    纯数字键: {len(pure_num)} 条  样例: {pure_num[:5]}")

print("\n" + "=" * 70)
print("调研完成 — 未修改任何文件")
print("=" * 70)
