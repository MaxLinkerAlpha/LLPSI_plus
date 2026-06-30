#!/usr/bin/env python3
"""Quick test: evaluate a single Latin story for Cap.6."""
import json, re, sys, os

EVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "difficulty_algorithm")
sys.path.insert(0, EVAL_DIR)
os.chdir(EVAL_DIR)
from evaluate_v2 import evaluate
os.chdir(os.path.dirname(__file__))

text = sys.stdin.read().strip()
r = evaluate(text, "test")
print(f"words={len(re.findall(r'[A-Za-zāēīōūȳĀĒĪŌŪȲ]{2,}', text))}")
print(f"v2_rate={r['v2_rate']}%  v2_level={r['v2_level']}  oov={r['v2_oov']}")
if r['v2_level'] is not None and r['v2_level'] <= 8:
    print("PASS")
else:
    print("FAIL")