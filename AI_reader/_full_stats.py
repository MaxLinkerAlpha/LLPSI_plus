#!/usr/bin/env python3
"""
全量统计 v1_1_0 — 快速版，直接 import evaluate_v2
"""
import re, sys, os
from pathlib import Path
from collections import Counter, defaultdict

AI_DIR = Path(__file__).resolve().parent
EVAL_DIR = AI_DIR.parent / "difficulty_algorithm"
REALITATES = AI_DIR / "realitates"
sys.path.insert(0, str(EVAL_DIR))
os.chdir(str(EVAL_DIR))  # evaluate_v2.py 用相对路径加载 JSON

from evaluate_v2 import evaluate

def count_latin_words(text):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    return len(re.findall(r"[A-Za-z\u0100-\u0233]+", text))

def get_tier(wc):
    if wc < 350: return "brevis"
    elif wc < 700: return "medius"
    else: return "longus"

stories = []
for cap_dir in sorted(REALITATES.iterdir()):
    if not cap_dir.is_dir() or not cap_dir.name.startswith("Cap"):
        continue
    cap_num = int(cap_dir.name[3:])
    for md in sorted(cap_dir.glob("*.md")):
        stories.append((cap_num, md))

print(f"共 {len(stories)} 篇故事，开始统计...")

folder_dist = Counter()
algo_dist = Counter()
tier_by_folder = defaultdict(Counter)
tier_by_algo = defaultdict(Counter)
consistent = 0
misplaced = 0
low_cov = 0
total_words = 0

for i, (folder_cap, md) in enumerate(stories):
    text = md.read_text(encoding="utf-8")
    latin = text
    if latin.startswith("---"):
        parts = latin.split("---", 2)
        if len(parts) >= 3:
            latin = parts[2]
    wc = count_latin_words(text)
    tier = get_tier(wc)

    result = evaluate(latin, md.name)
    v2_level = result.get("v2_level")
    v2_rate = result.get("v2_rate", 0)

    folder_dist[folder_cap] += 1
    tier_by_folder[folder_cap][tier] += 1
    total_words += wc

    if v2_level is not None:
        algo_dist[v2_level] += 1
        tier_by_algo[v2_level][tier] += 1
        if abs(v2_level - folder_cap) <= 2:
            consistent += 1
        else:
            misplaced += 1
    else:
        misplaced += 1

    if v2_rate < 85:
        low_cov += 1

    if (i+1) % 200 == 0:
        print(f"  进度: {i+1}/{len(stories)}")

print(f"\n{'='*70}")
print(f"全量统计报告（清理后）")
print(f"{'='*70}")
print(f"\n[总览]")
print(f"  总故事数: {len(stories)}")
print(f"  总词数: {total_words:,}")
print(f"  平均篇幅: {total_words//len(stories)} 词/篇")
print(f"  一致率 (差≤2): {consistent}/{len(stories)} ({consistent/len(stories)*100:.1f}%)")
print(f"  错位率 (差>2): {misplaced}/{len(stories)} ({misplaced/len(stories)*100:.1f}%)")
print(f"  低覆盖率 (<85%): {low_cov}")

print(f"\n[篇幅分布]")
all_tiers = Counter()
for cap, tiers in tier_by_folder.items():
    for t, c in tiers.items():
        all_tiers[t] += c
total = sum(all_tiers.values())
for t in ["brevis", "medius", "longus"]:
    c = all_tiers.get(t, 0)
    print(f"  {t:<8}: {c:>4} 篇 ({c/total*100:.1f}%)")

print(f"\n[按文件夹章的分布]")
print(f"  {'章':>4}  {'总':>4}  {'B':>4}  {'M':>4}  {'L':>4}  {'算法':>4}  {'差':>4}")
for ch in sorted(folder_dist):
    f = folder_dist[ch]
    b = tier_by_folder[ch].get("brevis", 0)
    m = tier_by_folder[ch].get("medius", 0)
    l = tier_by_folder[ch].get("longus", 0)
    a = algo_dist.get(ch, 0)
    diff = a - f
    mark = "⚠️" if abs(diff) > 5 else ""
    print(f"  Cap{ch:>2}  {f:>4}  {b:>4}  {m:>4}  {l:>4}  {a:>4}  {diff:>+4} {mark}")

print(f"\n[按算法定级的分布]")
print(f"  {'章':>4}  {'总':>4}  {'B':>4}  {'M':>4}  {'L':>4}")
for ch in sorted(algo_dist):
    a = algo_dist[ch]
    b = tier_by_algo[ch].get("brevis", 0)
    m = tier_by_algo[ch].get("medius", 0)
    l = tier_by_algo[ch].get("longus", 0)
    print(f"  Cap{ch:>2}  {a:>4}  {b:>4}  {m:>4}  {l:>4}")

print(f"\n[缺口分析（目标每章≥10篇）]")
print(f"  {'章':>4}  {'现存':>4}  {'缺口':>4}  {'状态'}")
total_gap = 0
for ch in range(1, 36):
    current = folder_dist.get(ch, 0)
    gap = max(0, 10 - current)
    total_gap += gap
    if gap > 0:
        print(f"  Cap{ch:>2}  {current:>4}  {gap:>+4}  ❌ 缺 {gap} 篇")
    elif current < 15:
        print(f"  Cap{ch:>2}  {current:>4}  {gap:>+4}  ⚠️ 偏少")
print(f"\n  总缺口: {total_gap} 篇")
