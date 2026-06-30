#!/usr/bin/env python3
"""快速检查特定词的章节"""
import json, re, sys, os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = PROJECT_ROOT / "difficulty_algorithm"
os.chdir(str(EVAL_DIR))
sys.path.insert(0, str(EVAL_DIR))

with open(EVAL_DIR / "form_chapter_map.json", encoding="utf-8") as f:
    FCM = json.load(f)
os.chdir(str(Path(__file__).resolve().parent))

words_to_check = ["video", "bibo", "capio", "do", "venio", "eo", "habeo", "voco", "ploro", 
                  "disco", "lego", "curro", "fugio", "ambulo", "sedeo", "sto",
                  "liber", "cibus", "panis", "vinum", "navis", "mare", "porta",
                  "ianua", "fenestra", "mensa", "cubiculum", "tectum", "terra",
                  "caelum", "luna", "sol", "stella", "nox", "dies",
                  "bonus", "malus", "pulcher", "laetus", "iratus", "fessus", "aeger",
                  "sanus", "novus", "antiquus", "multus", "paucus", "omnis"]

for w in words_to_check:
    clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
    ch = FCM.get(clean, "OOV")
    print(f"  {w:15s} -> Cap.{ch}")