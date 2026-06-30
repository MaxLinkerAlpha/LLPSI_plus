#!/usr/bin/env python3
"""快速摘要（复用 _reval_all.py 的完整输出）"""
import os, sys, re

ALGO_DIR = "/Users/max/Downloads/Projects/LLPSI_plus/difficulty_algorithm"
orig_cwd = os.getcwd()
os.chdir(ALGO_DIR)
sys.path.insert(0, ALGO_DIR)
from evaluate_v2 import evaluate
os.chdir(orig_cwd)

REALITATES_DIR = os.path.join("/Users/max/Downloads/Projects/LLPSI_plus", "AI_reader", "realitates")
dirs = sorted(
    [d for d in os.listdir(REALITATES_DIR)
     if os.path.isdir(os.path.join(REALITATES_DIR, d)) and d.startswith("Cap")],
    key=lambda d: int(re.search(r"\d+", d).group())
)

total = 0
can_eval = 0
cannot_eval = 0
stay = 0
mismatch = 0

for dirname in dirs:
    m = re.search(r"(\d+)", dirname)
    if not m:
        continue
    cur_ch = int(m.group(1))
    dp = os.path.join(REALITATES_DIR, dirname)
    for fn in os.listdir(dp):
        if not fn.endswith(".md"):
            continue
        total += 1
        with open(os.path.join(dp, fn), encoding="utf-8") as f:
            content = f.read()
        if content.startswith("---"):
            parts = content.split("---", 2)
            text = parts[2].strip() if len(parts) >= 3 else content
        else:
            text = content
        r = evaluate(text, fn)
        if r["v2_level"] is None:
            cannot_eval += 1
        elif r["v2_level"] == cur_ch:
            can_eval += 1
            stay += 1
        else:
            can_eval += 1
            mismatch += 1

print(f"Total stories evaluated: {total}")
print(f"Stories staying in place: {stay}")
print(f"Stories needing to move: {mismatch}")
print(f"Cannot evaluate (low coverage): {cannot_eval}")
print(f"Can evaluate (coverage >= 85%): {can_eval}")
