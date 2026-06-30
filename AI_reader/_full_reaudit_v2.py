#!/usr/bin/env python3
"""
全量重评 v1_2_0 — 清理后重新评级所有故事
"""
import re, sys, subprocess
from pathlib import Path
from collections import Counter

AI_DIR = Path(__file__).resolve().parent
EVAL_DIR = AI_DIR.parent / "difficulty_algorithm"
REALITATES = AI_DIR / "realitates"

def evaluate_story(md_path):
    try:
        result = subprocess.run(
            ["python3", "evaluate_v2.py", "--file", str(md_path)],
            capture_output=True, text=True, timeout=30, cwd=str(EVAL_DIR)
        )
        output = result.stdout + result.stderr
        v2_level = None
        v2_rate = None
        m = re.search(r'v2_level=(\d+)', output)
        if m: v2_level = int(m.group(1))
        m = re.search(r'v2_rate=([\d.]+)', output)
        if m: v2_rate = float(m.group(1))
        return v2_level, v2_rate
    except:
        return None, None

stories = []
for cap_dir in sorted(REALITATES.iterdir()):
    if not cap_dir.is_dir() or not cap_dir.name.startswith("Cap"):
        continue
    cap_num = int(cap_dir.name[3:])
    for md in sorted(cap_dir.glob("*.md")):
        stories.append((cap_num, md))

print(f"共 {len(stories)} 篇故事，开始评估...")

results = []
chapter_dist = Counter()
folder_dist = Counter()
consistent = 0
misplaced = 0
low_coverage = 0

for i, (folder_cap, md) in enumerate(stories):
    v2_level, v2_rate = evaluate_story(md)
    if v2_level is None:
        continue
    chapter_dist[v2_level] += 1
    folder_dist[folder_cap] += 1
    diff = abs(v2_level - folder_cap)
    if diff <= 2:
        consistent += 1
    else:
        misplaced += 1
    if v2_rate is not None and v2_rate < 85:
        low_coverage += 1
    results.append((folder_cap, v2_level, v2_rate, md.name))
    if (i+1) % 100 == 0:
        print(f"  进度: {i+1}/{len(stories)}")

print(f"\n{'='*60}")
print(f"全量重评结果（清理后）")
print(f"{'='*60}")
print(f"总故事: {len(results)}")
print(f"一致 (差≤2): {consistent} ({consistent/len(results)*100:.1f}%)")
print(f"错位 (差>2): {misplaced} ({misplaced/len(results)*100:.1f}%)")
print(f"低覆盖率 (<85%): {low_coverage}")

print(f"\n文件夹 vs 算法定级对比:")
print(f"  {'章':>4}  {'文件夹':>6}  {'算法':>6}  {'差值':>6}")
for ch in sorted(set(folder_dist) | set(chapter_dist)):
    f = folder_dist.get(ch, 0)
    a = chapter_dist.get(ch, 0)
    diff = a - f
    mark = "⚠️" if abs(diff) > 10 else ""
    print(f"  Cap{ch:>2}  {f:>6}  {a:>6}  {diff:>+6} {mark}")
