"""analyze_readers_v6.py - 阶段2-3：完整极简版段级分析 (v3.1 算法)

v3.1 关键改进 (2026-06-09):
1. is_narrative 强化: 过滤全大写标题/语法表格/变位表/版权页/词表
2. 排除 backup_* 目录
3. character 权重 0.3 -> 0.7 (人物名/专名更重要)
4. 词数硬限制: 流畅≥15, 挑战≥20, 节选≥30 (在 build_reader_routing_v2 中实施)

极简版v2算法完整版:
1. 段级切片: 按空行切分
2. 叙事过滤: 拉语词占比≥50%、非标题/非练习题/非词汇表、token>=15
3. 极简评分: find_chapter_for_threshold (高效版)
   - full = 1.0
   - partial (LLPSI总表词但未学到) = 0.5
   - character (本段所属书的高频专名) = 0.7
"""
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
OCR_OUT = ROOT / "ocr_output"
LEARNED = ROOT / "analysis_output" / "learned_words_v2.json"
JSON_OUT = ROOT / "analysis_output" / "reader_vocab_stats_v6.json"

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ]+")
CLEAN_RE = re.compile(r"^[a-z]+$")


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


# 紧凑但完整的英语白名单
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


# 非叙事黑名单: 版权页/出版信息/语法术语/变位标记
NON_NARRATIVE_LATIN = {
    'vocabula', 'vocabulum', 'litterae', 'littera',
    'declinatio', 'coniugatio', 'coniugationis',
}

CASEMARKERS = {
    'nominative', 'nominativus', 'genitive', 'genetivus',
    'accusative', 'accusativus', 'dative', 'dativus',
    'ablative', 'ablativus', 'vocative', 'vocativus',
    'singular', 'singularis', 'plural', 'pluralis',
    'masculine', 'masculinum', 'feminine', 'femininum',
    'neuter', 'neutrum', 'declension', 'conjugation',
    'indicative', 'indicativus', 'subjunctive', 'coniunctivus',
    'imperative', 'imperativus', 'participle', 'participium',
    'gerund', 'gerundium', 'supine', 'supinum', 'deponent',
    # 缩略形式 (常见于语法表格)
    'acc.', 'gen.', 'dat.', 'abl.', 'nom.', 'voc.',
    'sing.', 'pl.', 'masc.', 'fem.', 'neut.',
}

PUB_MARKERS = [
    'domus latina', 'hans h', 'hans orberg', 'h. orberg',
    'www.lingua', 'skovvangen', 'lingva latina per se',
    'second edition', 'first edition', 'all rights reserved',
    'printed in', 'isbn', 'copyright', 'published by',
    'publishing', 'press', 'university press',
]


def is_narrative(text):
    """判断段落是否为叙事性拉语段落 (v3.1: 增强过滤)

    过滤: 全大写标题/语法表格/变位表/版权页/出版信息
    """
    if len(text.strip()) < 30:
        return False

    text_lower = text.lower()

    # 1. 全大写标题页 (>50% 字母大写)
    letters = [c for c in text if c.isalpha()]
    if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.5:
        return False

    # 2. 出版/版权信息
    if any(m in text_lower for m in PUB_MARKERS):
        return False

    # 3. 变位表标记 (bracket-gloss: *[ ... " )
    if '*[' in text:
        return False

    # 3b. 变位表变体: 星号英语注释后跟拉丁词形
    if re.search(r'\*\s*(?:I|you|he|she|we|they|have|had|will|shall|been|being)', text):
        return False

    # 4. 提取拉丁词
    lat_words = []
    for w in WORD_RE.findall(text):
        wc = strip_accents(w.lower())
        if CLEAN_RE.match(wc) and len(wc) > 1 and wc not in EN:
            lat_words.append(wc)

    # v3: 词数硬过滤
    if len(lat_words) < 15:
        return False

    # 5. 语法表格检测: 形式标记或唯一词比 < 0.3
    if any(m in text_lower for m in CASEMARKERS):
        return False

    unique_ratio = len(set(lat_words)) / len(lat_words)
    if unique_ratio < 0.3:
        return False

    # 6. 拉丁元词汇
    if any(w in NON_NARRATIVE_LATIN for w in lat_words):
        return False

    # 7. 英语占比
    all_words = []
    for w in WORD_RE.findall(text):
        wc = strip_accents(w.lower())
        if CLEAN_RE.match(wc) and len(wc) > 1:
            all_words.append(wc)
    if not all_words:
        return False
    en_ratio = sum(1 for w in all_words if w in EN) / len(all_words)
    return en_ratio < 0.5


def find_chapters_for_thresholds(lat_tokens, learned_per_ch_sets, llpsi_total,
                                  high_freq, thresholds=(0.80, 0.70, 0.50)):
    """对单个段一次性找3个阈值的首达章节（高效版）

    v3 改进: 同时返回阈值章节处的实际分数, 用于路由层做 score*log(tokens+1) 排序
    """
    if not lat_tokens:
        return {th: -1 for th in thresholds}, {th: 0.0 for th in thresholds}

    # 预计算每个token在每章的类别
    # cat[ch] = {0: full, 1: partial, 2: character, 3: unknown}
    # 优化：增量计算
    full_n = 0
    partial_n = 0
    char_n = 0
    total = len(lat_tokens)

    # 按章节累计得分
    score_by_ch = {}  # ch → score

    for ch in range(1, 57):
        learned_N = learned_per_ch_sets[ch]
        # 增量更新
        new_full = 0
        new_partial = 0
        new_char = 0
        for t in lat_tokens:
            if t in learned_N:
                new_full += 1
            elif t in llpsi_total:
                new_partial += 1
            elif t in high_freq:
                new_char += 1
        score = (new_full + 0.5 * new_partial + 0.7 * new_char) / total
        score_by_ch[ch] = score

    # 找各阈值首达
    result = {}
    score_at = {}  # th → 该阈值首达章节处的实际分数
    for th in thresholds:
        result[th] = -1
        score_at[th] = 0.0
        for ch in range(1, 57):
            if score_by_ch[ch] >= th:
                result[th] = ch
                score_at[th] = score_by_ch[ch]
                break
    return result, score_at


def analyze_book(slug, learned_per_ch_sets, llpsi_total, llpsi_total_set):
    """分析一本书"""
    full = OCR_OUT / slug / "_full.txt"
    if not full.exists():
        return None
    text = full.read_text(encoding='utf-8', errors='replace')
    pages = re.split(r'--- PAGE \d+ ---', text)

    paragraphs = re.split(r'\n\s*\n', '\n'.join(pages))
    narratives = [p.strip() for p in paragraphs if is_narrative(p)]

    if not narratives:
        return None

    # 高频专名
    book_freq = Counter()
    for p in narratives:
        for w in WORD_RE.findall(p):
            wc = strip_accents(w.lower())
            if CLEAN_RE.match(wc) and len(wc) > 1 and wc not in EN:
                book_freq[wc] += 1
    high_freq = {w for w, c in book_freq.items() if c >= 5 and w not in llpsi_total_set}

    # 评估每段
    segments = []
    for idx, p in enumerate(narratives):
        tokens = []
        for w in WORD_RE.findall(p):
            wc = strip_accents(w.lower())
            if CLEAN_RE.match(wc) and len(wc) > 1 and wc not in EN:
                tokens.append(wc)
        if not tokens:
            continue

        thresholds, scores = find_chapters_for_thresholds(
            tokens, learned_per_ch_sets, llpsi_total, high_freq,
            thresholds=(0.80, 0.70, 0.50))

        segments.append({
            'idx': idx,
            'tokens': len(tokens),
            'preview': p[:100].replace('\n', ' '),
            't80': thresholds[0.80],
            't70': thresholds[0.70],
            't50': thresholds[0.50],
            # v3: 阈值首达章节处的实际分数, 用于路由层做 hybrid 排序
            's80': round(scores[0.80], 4),
            's70': round(scores[0.70], 4),
            's50': round(scores[0.50], 4),
        })

    return {
        'slug': slug,
        'n_segments': len(segments),
        'n_high_freq_chars': len(high_freq),
        'segments': segments,
    }


def main():
    print("加载learned_words_v2.json...")
    lw = json.loads(LEARNED.read_text(encoding='utf-8'))
    learned_per_ch = {int(ch): set(lw['learned_per_chapter'][str(ch)]) for ch in range(1, 57)}
    llpsi_total = set(lw['llpsi_total_words'])
    print(f"  LLPSI总词表: {len(llpsi_total)} 词")

    # 读物列表
    EXCLUDE = {'familia_romana', 'roma_aeterna', 'colloquia_personarum',
               'amphitryo', 'cena_trimalchionis', 'aeneis',
               'de_bello_gallico', 'fabulae_syrae'}
    slugs = sorted([d.name for d in OCR_OUT.iterdir()
                    if d.is_dir() and (d / "_full.txt").exists()
                    and d.name not in EXCLUDE
                    and not d.name.startswith('backup_')])
    print(f"\n分析 {len(slugs)} 本读物")

    all_results = []
    for i, slug in enumerate(slugs, 1):
        result = analyze_book(slug, learned_per_ch, llpsi_total, llpsi_total)
        if result is None:
            print(f"  [{i:2d}/{len(slugs)}] {slug:30s} 无叙事段")
            continue
        n80 = sum(1 for s in result['segments'] if 1 <= s['t80'] <= 56)
        n70 = sum(1 for s in result['segments'] if 1 <= s['t70'] <= 56)
        n50 = sum(1 for s in result['segments'] if 1 <= s['t50'] <= 56)
        print(f"  [{i:2d}/{len(slugs)}] {slug:30s} 段={result['n_segments']:4d}  "
              f"80%={n80:3d} 70%={n70:3d} 50%={n50:3d} 专名={result['n_high_freq_chars']}")
        all_results.append(result)

    # 输出
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(all_results, ensure_ascii=False, indent=2),
                        encoding='utf-8')
    print(f"\n已写入: {JSON_OUT}")

    # 统计
    total80 = sum(sum(1 for s in r['segments'] if 1 <= s['t80'] <= 56) for r in all_results)
    total70 = sum(sum(1 for s in r['segments'] if 1 <= s['t70'] <= 56) for r in all_results)
    total50 = sum(sum(1 for s in r['segments'] if 1 <= s['t50'] <= 56) for r in all_results)
    print(f"\n总计: 80%可读={total80}段, 70%={total70}段, 50%={total50}段")


if __name__ == '__main__':
    main()
