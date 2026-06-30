#!/usr/bin/env python3
"""用 80th 百分位算法重评 Cap.13"""
import os, sys, re

ROOT = os.path.dirname(os.path.abspath(__file__))
CAP_DIR = os.path.join(ROOT, 'realitates', 'Cap13')
EVAL_DIR = os.path.join(ROOT, '..', 'difficulty_algorithm')

os.chdir(EVAL_DIR)
sys.path.insert(0, EVAL_DIR)
from evaluate_v2 import evaluate
os.chdir(ROOT)

files = sorted([f for f in os.listdir(CAP_DIR) if f.endswith('.md') and 'brevis' not in f])

passed = 0
failed_list = []

for fname in files:
    with open(os.path.join(CAP_DIR, fname), encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---', 2)
    text = parts[2].strip() if len(parts) >= 3 else content
    
    title = fname.replace('Cap13_', '').rsplit('_', 2)[0].replace('_', ' ')
    r = evaluate(text, title)
    v2 = r['v2_level']
    rate = r['v2_rate']
    oov = r['v2_oov']
    wc = len(text.split())
    
    ok = v2 is not None and v2 <= 15
    status = 'PASS' if ok else 'FAIL'
    
    if ok:
        passed += 1
        print(f'  {status} {title:40s} v2={v2:2d}  rate={rate:.1f}%  words={wc}')
    else:
        failed_list.append((title, v2, rate, wc, len(oov)))

total = len(files)
print(f'\n=== 结果 ===')
print(f'通过: {passed}/{total} ({passed/total*100:.0f}%)')
print(f'失败: {len(failed_list)}')
print()
for title, v2, rate, wc, oov_n in failed_list:
    print(f'  FAIL  {title:40s} v2={v2:2d}  rate={rate:.1f}%  words={wc}  oov={oov_n}')
