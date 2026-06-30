#!/usr/bin/env python3
"""fix_generated.py — 修复已生成的 .md 文件中的高章节词汇，只处理拉丁正文不碰YAML"""
import json, re, sys, os
from pathlib import Path

BASE = Path(__file__).resolve().parent
EVAL_DIR = BASE.parent / "difficulty_algorithm"

with open(str(EVAL_DIR / "form_chapter_map.json"), encoding="utf-8") as f:
    FORM_CHAPTER = json.load(f)

REPLACEMENTS = {
    'vīta': 'vīvus', 'vītae': 'vīvī', 'vītam': 'vīvum',
    'mors': 'mortuus', 'mortis': 'mortuī', 'mortem': 'mortuum',
    'dolor': 'malum', 'dolōris': 'malī', 'dolōrem': 'malum',
    'animus': 'cor', 'animī': 'cordis', 'animum': 'cor',
    'memoria': 'cor', 'memoriae': 'cordis', 'memoriam': 'cor',
    'forum': 'oppidum', 'forō': 'oppidō', 'forī': 'oppidī',
    'templum': 'vīlla', 'templa': 'vīllae', 'templī': 'vīllae',
    'domus': 'vīlla', 'domūs': 'vīllae', 'domum': 'vīllam', 'domō': 'vīllā',
    'magister': 'vir', 'magistrī': 'virī', 'magistrum': 'virum',
    'discipulus': 'puer', 'discipulī': 'puerī', 'discipulum': 'puerum',
    'nauta': 'vir', 'nautae': 'virī', 'nautam': 'virum',
    'agricola': 'vir', 'agricolae': 'virī', 'agricolam': 'virum',
    'rēx': 'dominus', 'rēgis': 'dominī', 'rēgem': 'dominum',
    'rēgīna': 'fēmina', 'rēgīnae': 'fēminae', 'rēgīnam': 'fēminam',
    'imperātor': 'dominus', 'imperātōris': 'dominī',
    'flōs': 'rosa', 'flōris': 'rosae', 'flōrem': 'rosam', 'flōrēs': 'rosae',
    'ventus': 'caelum', 'ventī': 'caelī', 'ventum': 'caelum',
    'unda': 'aqua', 'undae': 'aquae', 'undam': 'aquam',
    'frūmentum': 'cibus', 'frūmentī': 'cibī',
    'argentum': 'pecūnia', 'argentī': 'pecūniae',
    'lībertās': 'bonum', 'lībertātis': 'bonī', 'lībertātem': 'bonum',
    'triclīnium': 'cubiculum', 'triclīniō': 'cubiculō',
    'fenestra': 'porta',
    'surgit': 'stat', 'surgunt': 'stant',
    'nārrat': 'dīcit', 'nārrant': 'dīcunt',
    'parat': 'facit', 'parant': 'faciunt',
    'cūrat': 'iuvat', 'cūrant': 'iuvant',
    'labōrat': 'facit', 'labōrant': 'faciunt',
    'scit': 'putat', 'sciunt': 'putant',
    'crēdit': 'putat', 'crēdunt': 'putant',
    'legit': 'videt', 'legunt': 'vident',
    'docet': 'dīcit', 'docent': 'dīcunt',
    'cōgitat': 'putat', 'cōgitant': 'putant',
    'scrībit': 'facit', 'scrībunt': 'faciunt',
    'redī': 'ī', 'redeō': 'eō', 'redit': 'it',
    'cōnsūmit': 'edit', 'amplexātur': 'tangit',
    'quiēscit': 'dormit', 'domat': 'habet',
    'semper': 'iam', 'saepe': 'multum',
    'dulcis': 'bonus', 'dulce': 'bonum',
    'sevērus': 'malus', 'sevēra': 'mala',
    'cūriōsus': 'bonus', 'aeternus': 'magnus', 'aeterna': 'magna',
    'audāx': 'bonus', 'pretiōsus': 'bonus',
    'sapiēns': 'bonus', 'sapientēs': 'bonī',
    'ferreus': 'bonus',
    'remedium': 'cibus',
    'balneum': 'aqua',
    'tempestās': 'ventus', 'tempestātēs': 'ventī',
    'sinus': 'corpus',
    'oblīvīscor': 'nōn videō',
    'oblīvīscī': 'nōn vidēre',
    'oblītus': 'nōn...',
    'ēsuriō': 'nōn edō',
    'hinnit': 'clamat',
    'cōnscendit': 'it',
    'virēs': 'corpus',
    'optimus': 'bonus',
    'nōmen': 'verbum',
}

def replace_in_text(text, max_chapter):
    words = re.findall(r'[āēīōūȳĀĒĪŌŪȲa-zA-Z]+', text)
    high_chapter_words = set()
    for w in set(words):
        clean = re.sub(r'[āēīōūȳĀĒĪŌŪȲ]',
                       lambda m: 'aeiouyAEIOUY'['āēīōūȳĀĒĪŌŪȲ'.index(m.group(0))], w).lower()
        ch = FORM_CHAPTER.get(clean)
        if ch is not None and ch > max_chapter:
            high_chapter_words.add(w)

    result = text
    for w in sorted(high_chapter_words, key=len, reverse=True):
        replacement = REPLACEMENTS.get(w.lower())
        if replacement is None:
            clean = re.sub(r'[āēīōūȳĀĒĪŌŪȲ]',
                           lambda m: 'aeiouyAEIOUY'['āēīōūȳĀĒĪŌŪȲ'.index(m.group(0))], w)
            replacement = REPLACEMENTS.get(clean.lower())
        if replacement:
            if w[0].isupper() and w == w[0].upper() + w[1:].lower():
                replacement = replacement[0].upper() + replacement[1:]
            result = re.sub(r'\b' + re.escape(w) + r'\b', replacement, result)
    return result

def fix_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    # 分离 YAML 头和正文
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print(f"  SKIP: no valid YAML frontmatter")
        return
    
    yaml_header = parts[1]
    body = parts[2]
    
    # 只修复正文
    fixed_body = replace_in_text(body, 13)
    
    # 重新组合
    new_content = '---\n' + yaml_header + '---\n' + fixed_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    cap11_dir = BASE / "realitates" / "Cap11"
    for f in sorted(cap11_dir.glob("Cap11_*_medius_*.md")):
        print(f"Fixing {f.name}...")
        fix_file(str(f))
    for f in sorted(cap11_dir.glob("Cap11_*_longior_*.md")):
        print(f"Fixing {f.name}...")
        fix_file(str(f))
    for f in sorted(cap11_dir.glob("Cap11_*_longus_*.md")):
        print(f"Fixing {f.name}...")
        fix_file(str(f))
    print("Done!")