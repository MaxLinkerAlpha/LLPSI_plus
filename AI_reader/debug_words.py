#!/usr/bin/env python3
"""调试脚本：找出故事中哪些词把章节评级推高了"""
import json, re, sys, os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = PROJECT_ROOT / "difficulty_algorithm"

os.chdir(str(EVAL_DIR))
sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate, LEMMA_CHAPTER, tokenize
os.chdir(str(Path(__file__).resolve().parent))

# 测试故事
test_texts = {
    "cap5_puer_avis": "Puer in hortō sedet. Avis in hortō cantat. Puer avem audit. Avis parva est. Avis pulchra est. Puer avem spectat. Puer avem amat. Avis ad puerum volat. Puer manum tollit. Avis in manū puerī sedet. Puer laetus est. Avis cantat. Puer rīdet.",
    "cap7_pater_dormit": "Pater in lectō est. Pater dormit. Fīlius in ātriō est. Fīlius clāmat. Māter: 'Tacē! Pater dormit.' Fīlius tacet. Sed fīlius nōn laetus est. Māter: 'Pater fessus est. Pater labōrat.' Fīlius mātrem spectat. 'Ego quoque labōrāre volō.' Māter rīdet. 'Tū parvus es. Sed mox magnus eris.' Fīlius laetus est. Pater dormit.",
}

for name, text in test_texts.items():
    print(f"\n=== {name} ===")
    r = evaluate(text, name)
    print(f"v2_level={r.get('v2_level')}, v2_rate={r.get('v2_rate')}%")

    # 找出每个不重复词对应的章节
    import simplemma
    tokens = tokenize(text)
    unique = list(dict.fromkeys(tokens))
    word_chapters = []
    for w in unique:
        clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
        try:
            lemma = simplemma.lemmatize(clean, lang="la")
        except:
            lemma = clean
        ch = LEMMA_CHAPTER.get(lemma, "OOV")
        word_chapters.append((w, lemma, ch))
    
    # 按章节排序
    word_chapters.sort(key=lambda x: (isinstance(x[2], int), x[2] if isinstance(x[2], int) else 999))
    for w, lemma, ch in word_chapters:
        if isinstance(ch, int) and ch > 7:
            print(f"  {w:20s} -> {lemma:20s} -> Cap.{ch} ***")
        elif ch == "OOV":
            print(f"  {w:20s} -> {lemma:20s} -> OOV")
        else:
            print(f"  {w:20s} -> {lemma:20s} -> Cap.{ch}")