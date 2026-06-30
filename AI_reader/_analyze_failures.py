#!/usr/bin/env python3
"""分析 Cap.13 失败故事中哪些词在抬高 v2_level，区分专有名词 vs 普通词"""
import json, re, sys, os
from collections import defaultdict

FORM_CH_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 
                           'difficulty_algorithm', 'form_chapter_map.json')
CAP13_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         'realitates', 'Cap13')

with open(FORM_CH_MAP, encoding='utf-8') as f:
    form_ch = json.load(f)

# 找到所有非brevis的Cap.13文件
files = sorted([f for f in os.listdir(CAP13_DIR) 
                if f.endswith('.md') and not 'brevis' in f])
print(f'找到 {len(files)} 个非brevis文件\n')

total_results = []

for fname in files:
    with open(os.path.join(CAP13_DIR, fname), encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---', 2)
    text = parts[2].strip() if len(parts) >= 3 else content
    
    tokens = []
    for w in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", text):
        w = w.strip()
        if len(w) >= 2:
            tokens.append(w)
    unique = list(dict.fromkeys(tokens))
    total_tokens = len(unique)
    
    # 分类每个独特词形的章节
    cap_entries = []  # (orig, clean, chapter)
    for w in unique:
        clean = re.sub(r'[āēīōūȳĀĒĪŌŪȲ]', 
                       lambda m: 'aeiouyAEIOUY'['āēīōūȳĀĒĪŌŪȲ'.index(m.group(0))], 
                       w).lower()
        ch = form_ch.get(clean)
        if ch is not None:
            cap_entries.append((w, clean, ch))
    
    matched = len(cap_entries)
    cap_entries.sort(key=lambda x: x[2])
    
    # 85th percentile
    idx85 = int(len(cap_entries) * 0.85)
    if idx85 >= len(cap_entries):
        idx85 = len(cap_entries) - 1
    v2_level = cap_entries[idx85][2] if cap_entries else None
    coverage = matched / total_tokens * 100 if total_tokens else 0
    
    # 找出 Cap > 15 的词
    high_tokens = [(orig, clean, ch) for orig, clean, ch in cap_entries if ch > 15]
    
    # 判断是否专有名词
    pn_stems = [
        'hispani', 'graec', 'aegypt', 'asi', 'arabi',
        'itali', 'gall', 'britanni', 'sicili', 'cret', 'cypr', 'athen', 'carthag',
        'roman', 'roma', 'tiber', 'nil', 'ocean', 'rubr', 'mare',
        'mercuri', 'iuppiter', 'iov', 'iunon', 'iuno', 'mart', 'ven', 'apoll', 'dian',
        'minerv', 'neptun', 'pluton', 'cerer', 'bacch', 'vulcan',
        'afric', 'syr', 'ind', 'ser', 'phoenic',
        'hiber', 'rhen', 'danuvi', 'euphrat', 'tigr',
        'macedoni', 'epir', 'thraci',
        'alexand', 'caesar', 'pompei', 'ciceron', 'catilin',
        'medic', 'philosoph', 'stoic', 'epicur',
    ]
    
    proper_n = []
    regular_n = [] 
    for orig, clean, ch in high_tokens:
        is_pn = any(clean.startswith(s) for s in pn_stems)
        if is_pn:
            proper_n.append((orig, clean, ch))
        else:
            regular_n.append((orig, clean, ch))
    
    status = 'PASS' if v2_level and v2_level <= 15 else 'FAIL'
    
    title = fname.replace('Cap13_', '').rsplit('_', 2)[0].replace('_', ' ')
    print(f'{status} v2={v2_level} cov={coverage:.1f}%  {title}')
    if proper_n:
        print(f'  专有名词 (Cap>15): {", ".join(f"{o}({c})" for o,_,c in proper_n)}')
    if regular_n:
        print(f'  普通词汇 (Cap>15): {", ".join(f"{o}({c})" for o,_,c in regular_n)}')
    print()

    total_results.append({
        'title': title, 'status': status, 'v2_level': v2_level,
        'proper_n': proper_n, 'regular_n': regular_n
    })

# 汇总
failed = [r for r in total_results if r['status'] == 'FAIL']
print(f'=== 汇总 ===')
print(f'通过: {sum(1 for r in total_results if r["status"]=="PASS")}/{len(total_results)}')
print(f'失败: {len(failed)}')
print()

# 分类失败
pn_only = [r for r in failed if r['regular_n'] == [] and r['proper_n'] != []]
mixed = [r for r in failed if r['regular_n'] != [] and r['proper_n'] != []]
reg_only = [r for r in failed if r['regular_n'] != [] and r['proper_n'] == []]
neither = [r for r in failed if r['regular_n'] == [] and r['proper_n'] == []]

print(f'纯专有名词导致失败: {len(pn_only)} 篇')
for r in pn_only:
    chs = [c for _,_,c in r['proper_n']]
    print(f'  {r["title"]:40s} v2={r["v2_level"]}  专名章:{chs}')

print(f'\n混合（专有名词+普通词）: {len(mixed)} 篇')
for r in mixed:
    pn_chs = [c for _,_,c in r['proper_n']]
    reg_chs = [c for _,_,c in r['regular_n']]
    print(f'  {r["title"]:40s} v2={r["v2_level"]}  专名:{pn_chs}  普通:{reg_chs}')

print(f'\n纯普通词导致失败: {len(reg_only)} 篇')
for r in reg_only:
    chs = [c for _,_,c in r['regular_n']]
    print(f'  {r["title"]:40s} v2={r["v2_level"]}  普通词章:{chs}')

print(f'\n无Cap>15词但仍失败（可能是匹配率不足85%）: {len(neither)} 篇')
for r in neither:
    print(f'  {r["title"]:40s} v2={r["v2_level"]}')

# 统计专有名词 vs 普通词 — 在 form_chapter_map 中的整体分布
print('\n\n=== form_chapter_map 中专有名词按章节统计 ===')
pn_by_chapter = defaultdict(list)
for w, ch in form_ch.items():
    is_pn = any(w.startswith(s) for s in pn_stems)
    if is_pn and ch > 15:
        pn_by_chapter[ch].append(w)

for ch in sorted(pn_by_chapter):
    words = sorted(set(pn_by_chapter[ch]))
    print(f'  Cap.{ch:2d} ({len(words):3d}): {", ".join(words[:15])}{"..." if len(words)>15 else ""}')
