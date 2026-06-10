#!/usr/bin/env python3
"""
analyze_readers_v4.py — 双视角分析: 词汇量 + LLPSI 章节匹配 (v5 token级)

v5 变更:
  - 切换到 token 级覆盖率 (反映实际阅读体验)
  - 修复 LATIN_RE: 接受重音字符 áéíóúý (OCR 中常替代 macron)
  - 去重音归一化: 比较前双端 strip 所有变音符号 (DB 为纯 ASCII)
  - 大幅收紧英语过滤器 (只过滤明确的非拉丁 content words)

视角1: 书的"可读起点" - 学完哪个章节后, 学习者能读这本书
   = earliest chapter where FR Cap.N known words covers >= X% of book's running tokens

视角2: 书的"教学价值" - 这本书对哪一章的新词覆盖率最高
   = chapter N where book contains most of FR Cap.N new words

输入:
  - ocr_output/<slug>/_full.txt
  - data/llpsi_corpus.db (fr_vocab 表)

输出:
  - analysis_output/reader_vocab_stats_v4.json
  - analysis_output/reader_vocab_stats_v4.csv
  - analysis_output/reader_vocab_stats_v4.md (可读报告)
"""
import csv
import json
import re
import sqlite3
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR_OUT = ROOT / "ocr_output"
DB_PATH = ROOT / "data" / "llpsi_corpus.db"
JSON_OUT = ROOT / "analysis_output" / "reader_vocab_stats_v4.json"
CSV_OUT = ROOT / "analysis_output" / "reader_vocab_stats_v4.csv"
MD_OUT = ROOT / "analysis_output" / "reader_vocab_stats_v4.md"

# 拉丁词提取: 包含重音字符 (OCR 中常替代 macron)
WORD_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ]+"
)
# 清理后只保留纯 ASCII 字母 (去重音后)
CLEAN_RE = re.compile(r"^[a-z]+$")

# 排除已在 corpus 的 LLPSI 官方读物
OFFICIAL_SLUGS = {
    "aeneis", "amphitryo", "ars_amatoria", "catilina", "cena_trimalchionis",
    "colloquia_personarum", "de_bello_gallico", "de_rerum_natura",
    "epitome_historiae_sacrae", "fabellae_latinae", "fabulae_syrae",
    "roma_aeterna", "sermones_romani", "familia_romana",
}

DELETED_SLUGS = {"nunc_loquamur", "probe"}

def is_backup_slug(slug: str) -> bool:
    """排除备份 slug (backup_v*)."""
    return slug.startswith("backup_v")


def strip_diacritics(s: str) -> str:
    """去除所有变音符号 (macron/accent/breve → 纯 ASCII). 如 āáăà → a"""
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def extract_latin_tokens(text: str) -> list[str]:
    """提取拉丁 token — 逐词提取, 去重音, 保留纯字母.

    v5 变更: 接受重音字符, 然后统一去重音, 因为 DB 侧全是纯 ASCII.
    """
    tokens = []
    for raw in WORD_RE.findall(text):
        w = strip_diacritics(raw.lower())
        if len(w) > 1 and CLEAN_RE.match(w):
            tokens.append(w)
    return tokens


def load_fr_vocab(db_path: str) -> tuple[dict[int, set[str]], dict[int, set[str]]]:
    """从 fr_vocab 表加载每章的 (known_words累计, new_words).
    DB 中词形为纯 ASCII, 无需额外处理."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT chapter, word_form, is_new FROM fr_vocab")
    rows = cur.fetchall()
    conn.close()

    chapter_new = {}  # chapter -> set of new words
    for ch, w, is_new in rows:
        if is_new:
            chapter_new.setdefault(ch, set()).add(w)

    sorted_chapters = sorted(chapter_new.keys())
    cumulative = set()
    chapter_known = {}
    for ch in sorted_chapters:
        cumulative |= chapter_new[ch]
        chapter_known[ch] = set(cumulative)
    return chapter_known, chapter_new


# 英语判定白名单 — 保守策略, 避免误杀拉丁词
# 添加规则: 仅加入明显不是拉丁词的英语教学术语和常见英语词
# 避开的暧昧词 (同时是拉丁词) 不放: via, ante, cum, post, dum, sum, res, me, te, se, ne, si, nam, tam, vel, an, at, aut, seu, sive, unde, ut, cur
ENGLISH_LIKELY = set("""
the of and to a in is it you that he was for on are with as i his they be
at one have this from or had by but some what there we can out other
were all your when up use word how said an each she which do their time if
will way about many then them write would like so these her long make thing
see him two has look more day could go come did number sound no most people
my over know water than call first who may down side been now find any new
work part take get place made live where after back little only round man
year came show every good me give our under name very through just form
sentence great think say help low line differ turn cause much mean before
move right boy old too same tell does set three want air well also play
small end put home read hand port large spell add even land here must
big high such follow act why ask men change went light kind off need
house picture try us again animal point mother world
chapter section exercise vocabulary grammar translation english latin
preface introduction contents index review
reading answer question problem fill write page
complete missing select match true false
""".split())

# 英语教学语法术语 (v3.1新增)
GRAMMAR_ENGLISH = set("""
stage stages language languages information following examples example used
translate translating translated singular plural tense tenses
nominative genitive accusative dative ablative vocative
declension declensions conjugation conjugations
participle participles infinitive infinitives
subjunctive indicative imperative
gerund gerundive supine deponent
active passive neuter gender masculine feminine
antecedent clause clauses preposition prepositions
adverb adverbs adjective adjectives pronoun pronouns
conjunction conjunctions interjection interjections
noun nouns verb verbs meaning meanings form forms
case cases person persons number numbers
story stories lesson lessons unit units paragraph paragraphs
practice exercises exercise questions question answers answer
correct incorrect sentence sentences lines line
written writing write passage passages reading readings
about also been between both called does during
each even every first found however into just
last letter letters like made make many might
more most much must name names need next note notes
often old only other others own place places point
same seen several show shown side since some something
still such system take than their them then there
these they thing things think this those though three
through thus time times together too two under until
upon using various very was way ways well were what when
where which while who whole why will with within without
work worked world would year years book books
slave slaves town towns city cities britain glass
merchant merchants market markets temple temples
street streets bath baths kitchen dining bedroom
family families children child son daughter father
mother brother sister wife husband king kings war
""".split())

ALL_ENGLISH = ENGLISH_LIKELY | GRAMMAR_ENGLISH


def estimate_english_tokens(tokens: list[str]) -> int:
    """估计 token 列表中英语词的数量."""
    return sum(1 for t in tokens if t in ALL_ENGLISH)


def analyze_one_book(slug: str,
                     chapter_known: dict[int, set[str]],
                     chapter_new: dict[int, set[str]],
                     chapter_known_all: set[str]) -> dict | None:
    """分析单本书 (v3.1 token级覆盖 + 拉丁词频部分信任分).

    v3.1 新增: 拉丁词频部分信任分:
      - 在 chapter_known[N] 中 → 完全已知 (权重 1.0)
      - 在 chapter_known_all (LLPSI 56章总表) 但不在 chapter_known[N] → 部分已知 (权重 0.5)
        含义: 词是真实拉丁词, LLPSI 会在后续章节教, 非完全陌生
      - 不在 chapter_known_all → 未知 (权重 0.0)
    """
    full = OCR_OUT / slug / "_full.txt"
    if not full.exists():
        return None
    text = full.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return None

    # 提取所有拉丁 token (去重音后, 排除 ALL_ENGLISH 英语)
    raw_tokens = extract_latin_tokens(text)
    if not raw_tokens:
        return None
    total_token_count = len(raw_tokens)

    # 英语占比
    english_token_count = estimate_english_tokens(raw_tokens)
    english_ratio = english_token_count / total_token_count if total_token_count else 0

    # 拉丁 token (排除英语)
    latin_tokens = [t for t in raw_tokens if t not in ALL_ENGLISH]
    latin_token_count = len(latin_tokens)

    # unique Latin forms
    unique_latin = set(latin_tokens)
    unique_latin_count = len(unique_latin)

    sorted_chapters = sorted(chapter_known.keys())

    # 预计算: 书内高频词 (出现 ≥5 次 且 不在 LLPSI 总表) — 角色名/专属词
    freq = {}
    for t in latin_tokens:
        freq[t] = freq.get(t, 0) + 1
    high_freq_book_words = {w for w, c in freq.items() if c >= 5 and w not in chapter_known_all}

    # --- 视角1: token 级可读起点 + 拉丁词频混合分 ---
    token_coverage_by_ch = {}
    form_coverage_by_ch = {}
    hybrid_coverage_by_ch = {}
    starting_ch_token = {}
    starting_ch_form = {}

    for ch in sorted_chapters:
        known = chapter_known[ch]

        # token 级 (纯 LLPSI 匹配)
        known_token_count = sum(1 for t in latin_tokens if t in known)
        tok_cov = known_token_count / latin_token_count if latin_token_count else 0
        token_coverage_by_ch[ch] = round(tok_cov, 4)

        # form 级 (保留)
        form_cov = len(unique_latin & known) / unique_latin_count if unique_latin_count else 0
        form_coverage_by_ch[ch] = round(form_cov, 4)

        # 混合分 (v3.1): 全匹配 ×1.0 + 后续会学 ×0.5 + 书内高频 ×0.4
        full_hits = 0
        partial_hits = 0      # LLPSI总表但未学到
        context_hits = 0       # 书内高频但不在LLPSI
        for t in latin_tokens:
            if t in known:
                full_hits += 1
            elif t in chapter_known_all:
                partial_hits += 1
            elif t in high_freq_book_words:
                context_hits += 1
        hyb_cov = (full_hits + partial_hits * 0.5 + context_hits * 0.4) / latin_token_count if latin_token_count else 0
        hybrid_coverage_by_ch[ch] = round(hyb_cov, 4)

    # 起点 (基于混合分)
    for threshold in [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90]:
        found = None
        for ch in sorted_chapters:
            if hybrid_coverage_by_ch[ch] >= threshold:
                found = ch
                break
        starting_ch_token[threshold] = found

    # form 级起点 (保留兼容)
    for threshold in [0.30, 0.40, 0.50, 0.60]:
        found = None
        for ch in sorted_chapters:
            if form_coverage_by_ch[ch] >= threshold:
                found = ch
                break
        starting_ch_form[threshold] = found

    peak_hybrid = max(hybrid_coverage_by_ch.values()) if hybrid_coverage_by_ch else 0
    peak_token = max(token_coverage_by_ch.values()) if token_coverage_by_ch else 0
    peak_form = max(form_coverage_by_ch.values()) if form_coverage_by_ch else 0
    peak_chapter = max(hybrid_coverage_by_ch.items(), key=lambda x: x[1])[0] if hybrid_coverage_by_ch else None

    # --- 视角2: 教学价值 (不变) ---
    new_word_coverage = {}
    for ch, new_set in chapter_new.items():
        if not new_set:
            continue
        hits = len(new_set & unique_latin)
        cov = hits / len(new_set)
        new_word_coverage[ch] = round(cov, 4)
    if new_word_coverage:
        best_teach_chapter = max(new_word_coverage.items(), key=lambda x: x[1])
        best_teach_ch, best_teach_cov = best_teach_chapter
    else:
        best_teach_ch, best_teach_cov = None, 0

    # --- 类型判定 (基于混合分 peak) ---
    if latin_token_count < 500:
        verdict = "low_content"
    elif english_ratio > 0.55:
        verdict = "english_dominant"
    elif english_ratio > 0.35:
        verdict = "english_mixed"
    elif peak_hybrid >= 0.90:
        verdict = "fluent"
    elif peak_hybrid >= 0.80:
        verdict = "readable"
    elif peak_hybrid >= 0.70:
        verdict = "challenging"
    elif peak_hybrid >= 0.60:
        verdict = "selected"
    else:
        verdict = "difficult"

    return {
        "slug": slug,
        "total_extracted_tokens": total_token_count,
        "latin_token_count": latin_token_count,
        "english_token_count": english_token_count,
        "english_ratio": round(english_ratio, 4),
        "unique_latin_count": unique_latin_count,
        "verdict": verdict,

        # 混合分起点 (v3.1: LLPSI匹配 + 拉丁词频部分信任)
        "starting_ch_token_50": starting_ch_token.get(0.50),
        "starting_ch_token_60": starting_ch_token.get(0.60),
        "starting_ch_token_70": starting_ch_token.get(0.70),
        "starting_ch_token_75": starting_ch_token.get(0.75),
        "starting_ch_token_80": starting_ch_token.get(0.80),
        "starting_ch_token_85": starting_ch_token.get(0.85),
        "starting_ch_token_90": starting_ch_token.get(0.90),

        # form 级起点 (保留)
        "starting_ch_form_30": starting_ch_form.get(0.30),
        "starting_ch_form_40": starting_ch_form.get(0.40),
        "starting_ch_form_50": starting_ch_form.get(0.50),
        "starting_ch_form_60": starting_ch_form.get(0.60),

        "peak_chapter": peak_chapter,
        "peak_hybrid_coverage": round(peak_hybrid, 4),
        "peak_token_coverage": round(peak_token, 4),
        "peak_form_coverage": round(peak_form, 4),

        "best_teach_chapter": best_teach_ch,
        "best_teach_coverage": round(best_teach_cov, 4),

        # 三轨覆盖率
        "hybrid_coverage_by_chapter": hybrid_coverage_by_ch,
        "token_coverage_by_chapter": token_coverage_by_ch,
        "form_coverage_by_chapter": form_coverage_by_ch,
    }


def main() -> int:
    print(f"=== 读物词频 + LLPSI 章节双视角匹配 (v3.1 hybrid) ===")

    chapter_known, chapter_new = load_fr_vocab(DB_PATH)
    chapter_known_all = chapter_known.get(56, set())
    print(f"[fr_vocab] 56 章节累计")
    print(f"  Cap.1  已知词: {len(chapter_known.get(1, set())):,}")
    print(f"  Cap.35 已知词: {len(chapter_known.get(35, set())):,}")
    print(f"  Cap.56 已知词 (拉丁词频池): {len(chapter_known_all):,}")
    print()

    all_slugs = sorted([p.parent.name for p in OCR_OUT.glob("*/_full.txt")
                        if p.stat().st_size > 100])
    filtered = [s for s in all_slugs
                if s not in OFFICIAL_SLUGS and s not in DELETED_SLUGS and not is_backup_slug(s)]
    print(f"[扫描] {len(all_slugs)} 本, 过滤后 {len(filtered)} 本待分析")
    print()

    results = []
    for slug in filtered:
        r = analyze_one_book(slug, chapter_known, chapter_new, chapter_known_all)
        if r:
            results.append(r)
            t50 = r["starting_ch_token_50"] or "—"
            t70 = r["starting_ch_token_70"] or "—"
            t80 = r["starting_ch_token_80"] or "—"
            t90 = r["starting_ch_token_90"] or "—"
            teach = (f"Cap.{r['best_teach_chapter']} "
                     f"({r['best_teach_coverage']*100:.0f}%)") if r["best_teach_chapter"] else "—"
            v = r["verdict"]
            print(f"  [{v:14s}] {slug:30s} "
                  f"token={r['latin_token_count']:>7,} "
                  f"独={r['unique_latin_count']:>5,} "
                  f"英%={r['english_ratio']*100:>4.1f}% "
                  f"起点 h50={t50} h70={t70} h80={t80} h90={t90} "
                  f"pkH={r['peak_hybrid_coverage']*100:.0f}% "
                  f"教学={teach}")

    # 保存 JSON
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[JSON] {JSON_OUT}")

    # 保存 CSV
    with open(CSV_OUT, "w", encoding="utf-8") as f:
        f.write("slug,verdict,latin_tokens,unique_latin,english_ratio,"
                "h50,h60,h70,h75,h80,h85,h90,"
                "peak_ch,peak_hyb,peak_tok,peak_frm,teach_ch,teach_cov\n")
        for r in results:
            t = r.get
            f.write(f"{r['slug']},{r['verdict']},{r['latin_token_count']},"
                    f"{r['unique_latin_count']},{r['english_ratio']},"
                    f"{t('starting_ch_token_50') or ''},{t('starting_ch_token_60') or ''},"
                    f"{t('starting_ch_token_70') or ''},{t('starting_ch_token_75') or ''},"
                    f"{t('starting_ch_token_80') or ''},{t('starting_ch_token_85') or ''},"
                    f"{t('starting_ch_token_90') or ''},"
                    f"{r['peak_chapter'] or ''},{r['peak_hybrid_coverage']},{r['peak_token_coverage']},{r['peak_form_coverage']},"
                    f"{r['best_teach_chapter'] or ''},{r['best_teach_coverage']}\n")
    print(f"[CSV]  {CSV_OUT}")

    # Markdown 报告
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write("# 读物词频 + LLPSI 章节匹配 (v3.1 hybrid)\n\n")
        f.write(f"分析日期: 2026-06-08 | 待分析: {len(results)} 本\n\n")
        f.write("## 评级指标 (v3.1 — hybrid 混合分)\n\n")
        f.write("- **混合分 (hybrid)**: 纯LLPSI匹配 + 拉丁词频部分信任\n")
        f.write("  - token 在 `chapter_known[N]` → 权重 1.0 (完全已知)\n")
        f.write("  - token 在 LLPSI 56章总表 但不在 `chapter_known[N]` → 权重 0.5 (真实拉丁词, 后续会学)\n")
        f.write("  - token 不在 LLPSI 56章总表 → 权重 0.0\n")
        f.write("- **阅读体验类标 (基于 hybrid peak)**:\n")
        f.write("  - `fluent` (流畅泛读): peak hybrid ≥ 90%\n")
        f.write("  - `readable` (可读): peak hybrid 80-90%\n")
        f.write("  - `challenging` (挑战): peak hybrid 70-80%\n")
        f.write("  - `selected` (片段可读): peak hybrid 60-70%\n")
        f.write("  - `difficult` (困难): peak hybrid < 60%\n\n")
        f.write("## 详情\n\n")
        f.write("| slug | 拉token | 独词 | 英% | h50 | h70 | h80 | pkH% | pkT% | pkF% | 教学 |\n")
        f.write("|------|--------:|-----:|----:|----:|----:|----:|-----:|-----:|-----:|-----:|\n")
        for r in sorted(results, key=lambda x: x.get("starting_ch_token_70") or 999):
            t = r.get
            f.write(f"| {r['slug']} | {r['latin_token_count']:,} | "
                    f"{r['unique_latin_count']:,} | "
                    f"{r['english_ratio']*100:.0f}% | "
                    f"{t('starting_ch_token_50') or '—'} | {t('starting_ch_token_70') or '—'} | "
                    f"{t('starting_ch_token_80') or '—'} | "
                    f"{r['peak_hybrid_coverage']*100:.0f}% | "
                    f"{r['peak_token_coverage']*100:.0f}% | "
                    f"{r['peak_form_coverage']*100:.0f}% | "
                    f"Cap.{r['best_teach_chapter']} ({r['best_teach_coverage']*100:.0f}%) |\n")
    print(f"[MD]   {MD_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
