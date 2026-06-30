#!/usr/bin/env python3
"""验证脚本：检查拉丁语文本是否只使用 Cap.1-11 词汇。"""
import json, re, sys, os

# 加载预计算词形→章节映射表
EVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "difficulty_algorithm")
with open(os.path.join(EVAL_DIR, "form_chapter_map.json"), encoding="utf-8") as f:
    FCM = json.load(f)

def verify(text: str, name: str = "unnamed") -> dict:
    tokens = []
    for w in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", text):
        w = w.strip()
        if len(w) >= 2:
            tokens.append(w)
    
    unique = list(dict.fromkeys(tokens))
    
    high_ch = []
    oov = []
    safe = []
    
    for w in unique:
        clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]",
                       lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))],
                       w).lower()
        
        ch = FCM.get(clean)
        if ch is not None:
            if ch <= 11:
                safe.append((w, None, ch))
            else:
                high_ch.append((w, None, ch))
        else:
            oov.append((w, clean))
    
    wc = len(tokens)
    return {
        "name": name,
        "word_count": wc,
        "unique_types": len(unique),
        "safe": len(safe),
        "high_ch": high_ch,
        "oov": oov,
        "passes": len(high_ch) == 0 and len(oov) == 0,
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify_vocab.py 'Latin text here'")
        # Or read from stdin
        text = sys.stdin.read().strip()
        result = verify(text)
    else:
        text = sys.argv[1]
        result = verify(text)
    
    print(f"Name: {result['name']}")
    print(f"Word count: {result['word_count']}")
    print(f"Unique types: {result['unique_types']}")
    print(f"Safe (Ch.1-11): {result['safe']}")
    print(f"High Ch. (12+): {len(result['high_ch'])}")
    if result['high_ch']:
        for w, _, ch in result['high_ch']:
            print(f"  {w} -> Ch.{ch}")
    print(f"OOV: {len(result['oov'])}")
    if result['oov']:
        for w, clean in result['oov']:
            print(f"  {w} -> OOV (clean={clean})")
    print(f"\nPASS: {result['passes']}")