#!/usr/bin/env python3
"""快速检查拉丁语文本的 v2_level"""
import json, re, sys, os
import simplemma

EVAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "difficulty_algorithm")
with open(os.path.join(EVAL_DIR, "lemma_chapter_map.json"), encoding="utf-8") as f:
    LCM = json.load(f)

def check(text):
    tokens = list(dict.fromkeys([t for t in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", text) if len(t) >= 2]))
    v2_chapters = []
    for w in tokens:
        clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
        try:
            lemma = simplemma.lemmatize(clean, lang="la")
        except:
            lemma = clean
        if lemma in LCM:
            v2_chapters.append(LCM[lemma])
    sorted_ch = sorted(v2_chapters)
    total = len(tokens)
    matched = len(v2_chapters)
    idx_85 = int(matched * 0.85)
    if idx_85 >= matched: idx_85 = matched - 1
    threshold = sorted_ch[idx_85] if sorted_ch else None
    over = sum(1 for ch in sorted_ch if ch > 11)
    wc = len([t for t in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", text) if len(t) >= 2])
    return wc, total, threshold, over

if __name__ == "__main__":
    text = sys.stdin.read()
    wc, types, v2, over = check(text)
    print(f"wc={wc} types={types} v2_level={v2} over11={over} PASS={v2 is not None and v2 <= 11}")