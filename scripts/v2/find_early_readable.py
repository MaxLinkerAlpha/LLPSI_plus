"""检查oxford_1和ecce_romani中真正可读段的位置"""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
OCR_OUT = ROOT / "ocr_output"
LEARNED = ROOT / "analysis_output" / "learned_words_v2.json"

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ]+")
CLEAN_RE = re.compile(r"^[a-z]+$")


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


EN = set("""
the of and to a in is it you that he was for on are with as i his they be at one have
this from or had by but some what there we can out other were all your when up use
word how said an each she which do their time if will way about many then them
write would like so these her long make thing see him two has look more day could
go come did number sound no most people my over know water than call first who may
down side been now find any new work part take get place made live where after back
little only round man year came show every good me give our under name very through
just form sentence great think say help low line differ turn cause much mean before
move right boy old too same tell does set three want air well also play small end
put home read hand port large spell add even land here must big high such follow
act why ask men change went light kind off need house picture try us again animal
point mother world about above across after again against almost along already also
always among another answer any anyone anything appear apply area arrive ask back
bad bank base become begin behind believe below best better between black blood body
book born both bring build burn business buy call camera capital care carry case
catch cause century certain chair chance change chapter character charge check child
choose church city class clear close cold colour come common complete consider
contain continue country course cover cross crowd dark date dead deep develop die
different difficult direct distance do door draw drink drive dry early east easy
eat effect either else enjoy enough enter equal especially evening event ever
everyone example explain eye face fact fall family far fast father feel few field
fight figure fill find fire first fish five floor follow food foot force form four
free friend front full game girl give glass go gold good government great group
grow guess guide half happen happy hard hat head health hear heart heavy help here
hide high hill history hold home hope horse hospital hot hour house hundred husband
idea important indeed industry information inside instead interest island job join
judge jump just keep kill kind king kitchen know land language large last late
later laugh law lead learn leave left less let letter level life light like line
list listen little live local long look love low main make man manager many market
marry matter may mean measure meet member middle might military million mind
minute miss modern moment money month morning most mother mountain move much music
name nation natural near need never new news next nice night nine north nothing
notice number occur office often oil old once one only open operation opportunity
order other others outside over own page paper parent park part particular party
pass past pattern pay people per perhaps person phone picture place plan play
point police political popular position possible pound power present president
pressure pretty price produce program project provide public purpose push put
quality question quickly quite race radio rain raise reach read ready real
reason receive recent record red remember report represent require research
rest result return rich right rise risk river road room round rule run safe
sale same save say school season seat second section seem sell send sense
serious serve set seven several short should show similar simply since sing
single sister sit situation six skin small social society some someone something
sometimes soon sort sound south space speak special spend spring stage stand
standard start state station stay step still stop store story street strong
study such suggest summer sun support sure system table take talk teach team
tell ten term test than thank that their them themselves then theory there
these they thing think third this those though thought thousand three through
throw thus time together too total toward town trade travel tree trouble true
try turn twenty two type under unit until upon usually value various very view
village visit voice wait walk wall want war watch water way wear week well west
what when where whether which while white who whole why wide wife will win
wind window winter wish with within without woman wonder word work world worry
write wrong year yes yet you young your
vocabulary translation english latin preface introduction contents
index review reading answer question problem fill complete missing
select match true false exercise exercises practice practicing drill
quiz test exam answer key chapter chapters section sections unit
units stage stage lesson topic topics grammar explanation
explanations note notes example examples forexample remark remarks
previous next prev page pages paragraph line lines sentence sentences
word words paragraph background cultural historical
""".split())


def is_narrative(text):
    if len(text.strip()) < 30:
        return False
    words = []
    for w in WORD_RE.findall(text):
        wc = strip_accents(w.lower())
        if CLEAN_RE.match(wc) and len(wc) > 1 and wc not in EN:
            words.append(wc)
    if len(words) < 5:
        return False
    all_words = []
    for w in WORD_RE.findall(text):
        wc = strip_accents(w.lower())
        if CLEAN_RE.match(wc) and len(wc) > 1:
            all_words.append(wc)
    if not all_words:
        return False
    en_ratio = sum(1 for w in all_words if w in EN) / len(all_words)
    return en_ratio < 0.5


def main():
    lw = json.loads(LEARNED.read_text(encoding='utf-8'))
    learned_per_ch = {int(ch): lw['learned_per_chapter'][str(ch)] for ch in range(1, 57)}
    llpsi_total = set(lw['llpsi_total_words'])

    for slug in ['oxford_1', 'ecce_romani']:
        full = OCR_OUT / slug / "_full.txt"
        text = full.read_text(encoding='utf-8', errors='replace')
        pages = re.split(r'--- PAGE \d+ ---', text)
        paragraphs = re.split(r'\n\s*\n', '\n'.join(pages))
        narratives = [(i, p.strip()) for i, p in enumerate(paragraphs) if is_narrative(p)]

        # 找高频专名
        book_freq = Counter()
        for _, p in narratives:
            for w in WORD_RE.findall(p):
                wc = strip_accents(w.lower())
                if CLEAN_RE.match(wc) and len(wc) > 1 and wc not in EN:
                    book_freq[wc] += 1
        high_freq = {w for w, c in book_freq.items() if c >= 5 and w not in llpsi_total}

        # 找到最早达到t80=1/2/3/5的段
        early_segments = []
        for idx, (orig_i, p) in enumerate(narratives):
            tokens = []
            for w in WORD_RE.findall(p):
                wc = strip_accents(w.lower())
                if CLEAN_RE.match(wc) and len(wc) > 1 and wc not in EN:
                    tokens.append(wc)
            if not tokens:
                continue

            def find_chapter(th):
                for ch in range(1, 57):
                    learned_N = set(learned_per_ch[ch])
                    full_n = sum(1 for t in tokens if t in learned_N)
                    partial = sum(1 for t in tokens if t not in learned_N and t in llpsi_total)
                    char = sum(1 for t in tokens if t not in learned_N and t not in llpsi_total and t in high_freq)
                    score = (full_n + 0.5 * partial + 0.3 * char) / len(tokens)
                    if score >= th:
                        return ch
                return -1

            t80 = find_chapter(0.80)
            t70 = find_chapter(0.70)
            t50 = find_chapter(0.50)
            early_segments.append({
                'idx': idx, 'orig_i': orig_i, 'tokens': len(tokens),
                't80': t80, 't70': t70, 't50': t50,
                'preview': p[:80].replace('\n', ' ') + ('...' if len(p) > 80 else ''),
            })

        # 找最早5个有意义的段
        meaningful = [s for s in early_segments if s['tokens'] >= 5 and (s['t80'] != -1 or s['t70'] != -1 or s['t50'] != -1)]

        print(f"\n=== {slug}  共{len(early_segments)}段, 有效{len(meaningful)}段 ===")
        print(f"  最早可读段（t50<=5）:")
        for s in early_segments:
            if s['t50'] != -1 and s['t50'] <= 5 and s['tokens'] >= 5:
                print(f"  原段#{s['orig_i']:4d}  t80={s['t80']:3d} t70={s['t70']:3d} t50={s['t50']:3d}  tokens={s['tokens']}")
                print(f"    \"{s['preview']}\"")
                if s['idx'] > 50:
                    break


if __name__ == '__main__':
    main()
