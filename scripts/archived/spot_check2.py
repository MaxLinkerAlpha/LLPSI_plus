#!/usr/bin/env python3
"""spot check reynolds_reader 和 unus_duo_tres 的内容"""
import re
from pathlib import Path

LATIN_HINTS = {'et','est','in','cum','ad','non','sunt','qui','sed','ut','si',
               'rex','puella','puer','filius','amat','habet','videt','dicit',
               '-que','-tur','-ntur','-bant','-bunt','-erunt'}
ENGLISH_HINTS = {'the','and','of','to','a','in','is','it','you','that','he',
                 'was','for','on','are','with','as','i','his','they','be','at',
                 'one','have','this','from','or','had','by','chapter','section',
                 'preface','introduction'}

def split_pages(text):
    pages = []
    cur_pg, cur = 0, []
    for line in text.splitlines():
        m = re.match(r"---\s*PAGE\s+(\d+)\s*---", line)
        if m:
            if cur:
                pages.append((cur_pg, "\n".join(cur)))
            cur_pg = int(m.group(1))
            cur = []
        else:
            cur.append(line)
    if cur:
        pages.append((cur_pg, "\n".join(cur)))
    return pages

for slug in ['reynolds_reader', 'nunc_loquamur', 'conversational_latin', 'via_latina_easy']:
    p = Path(f'ocr_output/{slug}/_full.txt')
    if not p.exists():
        print(f'{slug}: NOT FOUND')
        continue
    text = p.read_text(encoding='utf-8', errors='replace')
    pages = split_pages(text)
    print(f'\n===== {slug} ({len(pages)} pages) =====')
    for tgt in [5, 10, 20, 30, 50, 80, 100, 130, 150, 200, 250, 300, 350]:
        if tgt < len(pages):
            pg, txt = pages[tgt]
            words = re.findall(r"[A-Za-z']+", txt.lower())
            sample_words = words[:300]
            L = sum(1 for w in sample_words if w in LATIN_HINTS)
            E = sum(1 for w in sample_words if w in ENGLISH_HINTS)
            preview = re.sub(r'\s+', ' ', txt)[:200]
            print(f'  p.{pg} L={L} E={E}: {preview}')
