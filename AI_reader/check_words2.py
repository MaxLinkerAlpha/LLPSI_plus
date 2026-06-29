#!/usr/bin/env python3
import json, re, sys, os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = PROJECT_ROOT / "difficulty_algorithm"
os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import LEMMA_CHAPTER
import simplemma
os.chdir(str(Path(__file__).resolve().parent))

words = ["clausus", "exeo", "aperio", "bene", "tot", "amicitia", "porto", "lego", 
         "teneo", "noster", "alter", "gratia", "amicus", "nemo", "ita"]
for w in words:
    clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
    try: lemma = simplemma.lemmatize(clean, lang="la")
    except: lemma = clean
    ch = LEMMA_CHAPTER.get(lemma, "OOV")
    print(f"  {w:15s} -> {lemma:15s} -> Cap.{ch}")