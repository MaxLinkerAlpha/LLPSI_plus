#!/usr/bin/env python3
"""diagnose_v2_level.py — 诊断每个故事中哪些词导致 v2_level 过高。
输出每个故事的高章词（超过目标章节的词），并按章节排序。
"""
import json, re, sys, os

# 加载章节映射
EVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "difficulty_algorithm")
with open(os.path.join(EVAL_DIR, "lemma_chapter_map.json"), encoding="utf-8") as f:
    LEMMA_CHAPTER = json.load(f)

import simplemma

def tokenize(text: str) -> list:
    tokens = []
    for w in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/«»]+", text):
        w = w.strip()
        if len(w) >= 2:
            tokens.append(w)
    return tokens

def get_word_chapter(word: str) -> tuple:
    """返回 (word, lemma, chapter)。"""
    clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", 
                   lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], 
                   word).lower()
    try:
        lemma = simplemma.lemmatize(clean, lang="la")
    except Exception:
        lemma = clean
    ch = LEMMA_CHAPTER.get(lemma, None)
    return (word, lemma, ch)

def diagnose(text: str, target_chapter: int) -> dict:
    """诊断一段文本，找出所有超过 target_chapter 的词。"""
    tokens = tokenize(text)
    unique_types = list(dict.fromkeys(tokens))
    
    word_info = []
    high_chapter_words = []
    chapters = []
    
    for w in unique_types:
        word, lemma, ch = get_word_chapter(w)
        if ch is not None:
            chapters.append(ch)
            if ch > target_chapter:
                high_chapter_words.append((word, lemma, ch))
        word_info.append((word, lemma, ch))
    
    # 按章节排序
    high_chapter_words.sort(key=lambda x: (x[2], x[0]))
    
    # 计算 v2_level
    if chapters:
        sorted_ch = sorted(chapters)
        idx_85 = int(len(sorted_ch) * 0.85)
        if idx_85 >= len(sorted_ch):
            idx_85 = len(sorted_ch) - 1
        v2_level = sorted_ch[idx_85]
    else:
        v2_level = None
    
    return {
        "total_types": len(unique_types),
        "v2_level": v2_level,
        "high_chapter_words": high_chapter_words,
        "chapter_distribution": sorted(chapters),
    }

# 从 rewrite_cap7_8.py 动态加载 STORIES
sys.path.insert(0, os.path.dirname(__file__))
from rewrite_cap7_8 import STORIES

print("=" * 70)
print("DIAGNOSIS: High-chapter words causing v2_level > target")
print("=" * 70)

for story_id, story in STORIES.items():
    target = story["target_chapter"]
    max_level = target + 2  # Cap.7 -> 9, Cap.8 -> 10
    result = diagnose(story["text"], max_level)
    
    status = "PASS" if result["v2_level"] is not None and result["v2_level"] <= max_level else "FAIL"
    
    print(f"\n--- {story_id} {story['title_la']} (target={max_level}, actual={result['v2_level']}) [{status}] ---")
    
    if result["high_chapter_words"]:
        # 按章节分组显示
        by_chapter = {}
        for word, lemma, ch in result["high_chapter_words"]:
            if ch not in by_chapter:
                by_chapter[ch] = []
            by_chapter[ch].append((word, lemma))
        
        for ch in sorted(by_chapter.keys()):
            words = by_chapter[ch]
            word_list = ", ".join([f"{w}→{l}" for w, l in words[:10]])
            if len(words) > 10:
                word_list += f" ... (+{len(words)-10} more)"
            print(f"  Cap.{ch:02d}: {word_list}")
    else:
        print("  (no high-chapter words)")