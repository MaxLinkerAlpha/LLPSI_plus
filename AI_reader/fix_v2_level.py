#!/usr/bin/env python3
"""fix_v2_level.py — 针对每个故事，找出超过 85 分位线的词并提出替换方案。
只替换那些真正推高 v2_level 的词（约 15%），其余保留。
"""
import json, re, sys, os

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

def get_word_info(word: str):
    clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]",
                   lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))],
                   word).lower()
    try:
        lemma = simplemma.lemmatize(clean, lang="la")
    except Exception:
        lemma = clean
    ch = LEMMA_CHAPTER.get(lemma, None)
    return word, lemma, ch

def find_words_to_replace(text: str, target_level: int) -> list:
    """找出需要替换的词（章节号超过 target_level 且位置在 85 分位以上）。"""
    tokens = tokenize(text)
    unique_types = list(dict.fromkeys(tokens))
    
    # 获取每个词的章节
    word_chapters = []
    for w in unique_types:
        _, lemma, ch = get_word_info(w)
        if ch is not None:
            word_chapters.append((w, lemma, ch))
    
    # 按章节排序
    word_chapters.sort(key=lambda x: x[2])
    
    total = len(word_chapters)
    idx_85 = int(total * 0.85)
    
    # 85 分位处的章节
    if idx_85 < total:
        current_level = word_chapters[idx_85][2]
    else:
        current_level = word_chapters[-1][2] if word_chapters else 0
    
    if current_level <= target_level:
        return [], current_level  # 已经达标
    
    # 找出所有章节 > target_level 且在 85 分位以上的词
    # 实际上，只需要替换足够多的词使 85 分位降到 target_level 以下
    # 需要替换的词数 = (idx_85 + 1) - (第一个章节 <= target_level 的位置)
    
    # 找到从 idx_85 往前，所有章节 > target_level 的词
    to_replace = []
    for i in range(idx_85, -1, -1):
        w, lemma, ch = word_chapters[i]
        if ch > target_level:
            to_replace.append((w, lemma, ch))
        else:
            break
    
    to_replace.reverse()  # 按章节升序
    return to_replace, current_level

# 加载 STORIES
sys.path.insert(0, os.path.dirname(__file__))
from rewrite_cap7_8 import STORIES

# 构建低章词库（章节 <= target 的词）
def build_low_chapter_vocab(max_chapter: int) -> dict:
    """构建 {lemma: chapter} 的低章词库。"""
    return {lemma: ch for lemma, ch in LEMMA_CHAPTER.items() if ch <= max_chapter}

print("=" * 70)
print("TARGETED FIX: Words to replace to bring v2_level down")
print("=" * 70)

for story_id, story in STORIES.items():
    target = story["target_chapter"]
    max_level = target + 2  # Cap.7 -> 9, Cap.8 -> 10
    
    to_replace, current_level = find_words_to_replace(story["text"], max_level)
    
    if not to_replace:
        print(f"\n{story_id} {story['title_la']}: PASS (level={current_level})")
        continue
    
    print(f"\n{story_id} {story['title_la']} (current={current_level}, target={max_level})")
    print(f"  Need to replace {len(to_replace)} words:")
    
    # 按章节分组
    by_chapter = {}
    for w, lemma, ch in to_replace:
        if ch not in by_chapter:
            by_chapter[ch] = []
        by_chapter[ch].append((w, lemma))
    
    for ch in sorted(by_chapter.keys()):
        words = by_chapter[ch]
        for w, lemma in words[:5]:
            print(f"    Cap.{ch:02d}: {w} → {lemma}")
        if len(words) > 5:
            print(f"    ... and {len(words)-5} more from Cap.{ch}")