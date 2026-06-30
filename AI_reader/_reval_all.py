#!/usr/bin/env python3
"""
全量重新评估所有 .md 故事（DRY RUN）
- 使用 evaluate_v2.py 的 90th 百分位算法
- 遍历 AI_reader/realitates/ 下所有 Cap* 目录
- 输出不匹配（v2_level != current chapter）的故事
- 仅打印报告，不移动任何文件
"""

import os
import sys
import re
from collections import defaultdict

# ============================================================
# 步骤 1: 切换到 difficulty_algorithm 目录加载 evaluate_v2
# （因为 evaluate_v2 在模块顶层用相对路径加载 JSON 映射表）
# ============================================================
ALGO_DIR = "/Users/max/Downloads/Projects/LLPSI_plus/difficulty_algorithm"
PROJECT_ROOT = "/Users/max/Downloads/Projects/LLPSI_plus"
REALITATES_DIR = os.path.join(PROJECT_ROOT, "AI_reader", "realitates")

# 保存原始工作目录
orig_cwd = os.getcwd()
os.chdir(ALGO_DIR)
sys.path.insert(0, ALGO_DIR)

# 导入 evaluate 函数（JSON 映射表在此步加载）
from evaluate_v2 import evaluate

# 恢复原始工作目录
os.chdir(orig_cwd)

# ============================================================
# 步骤 2: 遍历所有 Cap* 目录，收集 .md 文件
# ============================================================
print("=" * 72)
print("[数据分析 Agent] 全量故事重新评估 — DRY RUN（不移动文件）")
print("=" * 72)

dirs = sorted(
    [d for d in os.listdir(REALITATES_DIR)
     if os.path.isdir(os.path.join(REALITATES_DIR, d)) and d.startswith("Cap")],
    key=lambda d: int(re.search(r"\d+", d).group())
)

all_stories = []  # 每一项: (rel_path, current_chapter, result_dict)

for dirname in dirs:
    match = re.search(r"(\d+)", dirname)
    if not match:
        continue
    current_chapter = int(match.group(1))
    dir_path = os.path.join(REALITATES_DIR, dirname)

    for fname in sorted(os.listdir(dir_path)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(dir_path, fname)
        rel_path = f"{dirname}/{fname}"

        # 读取 .md 文件，跳过 YAML frontmatter（--- ... ---）
        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---"):
            parts = content.split("---", 2)
            text = parts[2].strip() if len(parts) >= 3 else content
        else:
            text = content

        # 调用 evaluate_v2
        result = evaluate(text, fname)
        all_stories.append((rel_path, current_chapter, result))

# ============================================================
# 步骤 3: 分类统计
# ============================================================

# 3a. 按覆盖率分类
can_evaluate = []     # v2_level is not None（覆盖率 >= 85%）
cannot_evaluate = []  # v2_level is None（覆盖率 < 85%）

for rel_path, cur_ch, r in all_stories:
    if r["v2_level"] is None:
        cannot_evaluate.append((rel_path, cur_ch, r))
    else:
        can_evaluate.append((rel_path, cur_ch, r))

# 3b. 在可评估故事中，检查是否匹配
staying = []   # v2_level == current_chapter
mismatches = [] # v2_level != current_chapter

for rel_path, cur_ch, r in can_evaluate:
    if r["v2_level"] == cur_ch:
        staying.append((rel_path, cur_ch, r))
    else:
        mismatches.append((rel_path, cur_ch, r))

# ============================================================
# 步骤 4: 输出报告
# ============================================================

total = len(all_stories)
print(f"\n总计故事数: {total}")
print(f"可评估故事数（覆盖率 >= 85%）: {len(can_evaluate)}")
print(f"无法评估故事数（覆盖率 < 85%）: {len(cannot_evaluate)}")
print(f"  - 位置不变: {len(staying)}")
print(f"  - 位置不匹配（需要移动）: {len(mismatches)}")

# 不匹配详情
if mismatches:
    print(f"\n{'='*72}")
    print("不匹配详情（v2_level != 当前章节）:")
    print(f"{'='*72}")
    print(f"{'文件':60s} {'v2_level':>8} {'当前':>5} {'→目标':>5} {'覆盖率':>7}")
    print("-" * 72)

    # 按当前章节排序
    mismatches.sort(key=lambda x: (x[1], x[0]))
    for rel_path, cur_ch, r in mismatches:
        v2_lvl = r["v2_level"]
        rate = r["v2_rate"]
        print(f"{rel_path:60s} {v2_lvl:>8} {cur_ch:>5} → Cap{v2_lvl:<3} {rate:>6.1f}%")

# 汇总表：每个章节当前 vs v2 分布
print(f"\n{'='*72}")
print("章节级汇总: 当前存放章节 vs v2 评估章节")
print(f"{'='*72}")
print(f"{'Cap':>5} {'总数':>5} {'可评':>5} {'低覆盖':>6} {'不变':>5} {'需移出':>6} {'需移入':>6}")

# 按章节聚合
cap_current_counts = defaultdict(int)
cap_v2_counts = defaultdict(int)  # 重评估后各章节应有的故事数
cap_stay = defaultdict(int)
cap_out = defaultdict(int)    # 需要从该章节移出的
cap_in = defaultdict(int)     # 需要移入该章节的
cap_low = defaultdict(int)    # 该章节低覆盖率的

for rel_path, cur_ch, r in all_stories:
    cap_current_counts[cur_ch] += 1
    v2_lvl = r["v2_level"]
    if v2_lvl is None:
        cap_low[cur_ch] += 1
    else:
        cap_v2_counts[v2_lvl] += 1
        if v2_lvl == cur_ch:
            cap_stay[cur_ch] += 1
        else:
            cap_out[cur_ch] += 1
            cap_in[v2_lvl] += 1

all_chapters = sorted(set(list(cap_current_counts.keys()) + list(cap_v2_counts.keys())))
for ch in all_chapters:
    cur = cap_current_counts.get(ch, 0)
    ev = cap_current_counts.get(ch, 0) - cap_low.get(ch, 0)
    lo = cap_low.get(ch, 0)
    st = cap_stay.get(ch, 0)
    out_ = cap_out.get(ch, 0)
    in_ = cap_in.get(ch, 0)
    print(f"Cap{ch:<3} {cur:>5} {ev:>5} {lo:>6} {st:>5} {out_:>6} {in_:>6}")

# 重评估后各章节预期故事数
print(f"\n{'='*72}")
print("重评估后各章节预期故事数（按 v2_level 分布）:")
print(f"{'='*72}")
for ch in sorted(cap_v2_counts.keys()):
    # 加上无法评估的（保留在原位）
    low_in_this = cap_low.get(ch, 0)
    total_after = cap_v2_counts.get(ch, 0) + low_in_this
    print(f"  Cap{ch:<3}: {cap_v2_counts.get(ch, 0)} 个可评估 + {low_in_this} 个低覆盖(保留) = {total_after} 个")

# 覆盖率分布统计
print(f"\n{'='*72}")
print("覆盖率分布统计:")
print(f"{'='*72}")
buckets = defaultdict(int)
for _, _, r in all_stories:
    rate = r["v2_rate"]
    if rate >= 100:
        buckets["100%"] += 1
    elif rate >= 95:
        buckets["95-99%"] += 1
    elif rate >= 90:
        buckets["90-94%"] += 1
    elif rate >= 85:
        buckets["85-89%"] += 1
    elif rate >= 75:
        buckets["75-84%"] += 1
    elif rate >= 50:
        buckets["50-74%"] += 1
    else:
        buckets["<50%"] += 1
for bucket in ["100%", "95-99%", "90-94%", "85-89%", "75-84%", "50-74%", "<50%"]:
    print(f"  {bucket:>8}: {buckets.get(bucket, 0)}")

print(f"\n{'='*72}")
print("DRY RUN 完成 — 未移动任何文件。")
print(f"{'='*72}")
