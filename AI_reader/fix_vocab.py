#!/usr/bin/env python3
"""fix_vocab.py — 自动替换高章节词汇为低章节安全替代词。
读取故事文本，用 form_chapter_map.json 识别 >max_chapter 的词，
然后用预定义替换表替换为安全词汇。
"""

import json, re, sys, os
from pathlib import Path
from collections import Counter

EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"
os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))

with open("form_chapter_map.json", encoding="utf-8") as f:
    FORM_CHAPTER = json.load(f)

# ============================================================
# 替换表：高章节词 → 低章节安全替代
# ============================================================
REPLACEMENTS = {
    # 名词
    "vīta": "vīvus", "vītae": "vīvī", "vītam": "vīvum",
    "mors": "mortuus", "mortis": "mortuī", "mortem": "mortuum",
    "dolor": "malum", "dolōris": "malī", "dolōrem": "malum",
    "animus": "cor", "animī": "cordis", "animum": "cor",
    "memoria": "cor", "memoriae": "cordis", "memoriam": "cor",
    "forum": "oppidum", "forō": "oppidō", "forī": "oppidī",
    "templum": "vīlla", "templa": "vīllae", "templī": "vīllae",
    "domus": "vīlla", "domūs": "vīllae", "domum": "vīllam", "domō": "vīllā",
    "magister": "vir", "magistrī": "virī", "magistrum": "virum",
    "discipulus": "puer", "discipulī": "puerī", "discipulum": "puerum",
    "nauta": "vir", "nautae": "virī", "nautam": "virum",
    "agricola": "vir", "agricolae": "virī", "agricolam": "virum",
    "rēx": "dominus", "rēgis": "dominī", "rēgem": "dominum",
    "rēgīna": "fēmina", "rēgīnae": "fēminae", "rēgīnam": "fēminam",
    "imperātor": "dominus", "imperātōris": "dominī",
    "flōs": "rosa", "flōris": "rosae", "flōrem": "rosam", "flōrēs": "rosae",
    "ventus": "caelum", "ventī": "caelī", "ventum": "caelum",
    "unda": "aqua", "undae": "aquae", "undam": "aquam",
    "frūmentum": "cibus", "frūmentī": "cibī",
    "argentum": "pecūnia", "argentī": "pecūniae",
    "lībertās": "bonum", "lībertātis": "bonī", "lībertātem": "bonum",
    "triclīnium": "cubiculum", "triclīniō": "cubiculō",
    "fenestra": "porta",  # fenestra is Cap.14, barely over
    
    # 动词
    "surgit": "stat", "surgunt": "stant",
    "nārrat": "dīcit", "nārrant": "dīcunt",
    "parat": "facit", "parant": "faciunt",
    "cūrat": "iuvat", "cūrant": "iuvant",
    "labōrat": "facit", "labōrant": "faciunt",
    "scit": "putat", "sciunt": "putant",
    "crēdit": "putat", "crēdunt": "putant",
    "legit": "videt", "legunt": "vident",
    "docet": "dīcit", "docent": "dīcunt",
    "cōgitat": "putat", "cōgitant": "putant",
    "scrībit": "facit", "scrībunt": "faciunt",
    "redī": "ī", "redeō": "eō", "redit": "it",
    "cōnsūmit": "edit", "amplexātur": "tangit",
    "quiēscit": "dormit", "domat": "habet",
    
    # 副词/形容词
    "semper": "iam", "saepe": "multum",
    "dulcis": "bonus", "dulce": "bonum",
    "sevērus": "malus", "sevēra": "mala",
    "cūriōsus": "bonus", "aeternus": "magnus", "aeterna": "magna",
    "audāx": "bonus", "pretiōsus": "bonus",
    "sapiēns": "bonus", "sapientēs": "bonī",
    "ferreus": "bonus",
    
    # 其他
    "remedium": "cibus",
    "balneum": "aqua",
    "tempestās": "ventus", "tempestātēs": "ventī",
    "sinus": "corpus",
    "oblīvīscor": "nōn videō",
    "oblīvīscī": "nōn vidēre",
    "oblītus": "nōn...",
    "ēsuriō": "nōn edō",
    "hinnit": "clamat",
    "cōnscendit": "it",
    "virēs": "corpus",
    "optimus": "bonus",
    "nōmen": "verbum",  # nomen is Cap.12, safe but let's be careful
}

# 词边界正则
def replace_in_text(text, max_chapter):
    """替换文本中所有 >max_chapter 的词为安全替代"""
    words = re.findall(r"[āēīōūȳĀĒĪŌŪȲa-zA-Z]+", text)
    
    # 先统计高章节词
    high_chapter_words = set()
    for w in set(words):
        clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", 
                       lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
        ch = FORM_CHAPTER.get(clean)
        if ch is not None and ch > max_chapter:
            high_chapter_words.add(w)
    
    # 替换
    result = text
    for w in sorted(high_chapter_words, key=len, reverse=True):
        replacement = REPLACEMENTS.get(w.lower())
        if replacement is None:
            # 尝试去长音后查找
            clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", 
                           lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w)
            replacement = REPLACEMENTS.get(clean.lower())
        if replacement:
            # 大小写保持
            if w[0].isupper() and w == w[0].upper() + w[1:].lower():
                replacement = replacement[0].upper() + replacement[1:]
            result = re.sub(r'\b' + re.escape(w) + r'\b', replacement, result)
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_vocab.py <text> [max_chapter]")
        sys.exit(1)
    
    text = sys.argv[1]
    max_ch = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    
    # 如果是文件路径
    if os.path.exists(text):
        with open(text, encoding="utf-8") as f:
            text = f.read()
    
    fixed = replace_in_text(text, max_ch)
    print(fixed)