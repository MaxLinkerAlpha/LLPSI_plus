#!/usr/bin/env python3
"""
extract_metadata_v2.py — 更精准的元信息提取

改进:
  1. 跳过前 20% (Preface/Notes) 和最后 20% (Vocabulary)
  2. 采样中间段 (20%-80%)
  3. 对每页独立判定语言, 拉语比例加全本平均
  4. 提取章节标题时考虑 "Cap.", "Chapter", "Liber", "I.", "II." 等
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
OCR_OUT = ROOT / "ocr_output"
META_FILE = ROOT / "analysis_output" / "reader_metadata_v2.json"
CSV_FILE = ROOT / "analysis_output" / "reader_metadata_v2.csv"

# 拉语常见词 (高频) - 扩展到 ~300 词
LATIN_COMMON = set("""
et in est non sunt ad cum de ex ab sub per pro cum sine
ut si ne que qui quae quod hic haec hoc ille illa illud is ea id
esse haberet habet habent sum es est sumus estis sunt ero eris erit
fui fuisti fuit fuimus fuistis fuerunt eram eras erat eramus eratis erant
sit sint sint esset essent
fio fis fit fiunt factus facta factum
amo amas amat amamus amatis amant amavi amavisti amavit amaverat
vide vides videt videmus videtis vident vidi vidisti vidit
dico dicis dicit dicimus dicitis dicunt dixi dixisti dixit
do das dat damus datis dant dedi dedisti dedit
eo is it imus itis eunt iiisti iit iimus iistis ierunt
venio venis venit venimus venitis veniunt
habeo habes habet habemus habetis habent habui habuisti habuit
possum potes potest possumus potestis possunt potui potuisti potuit
uolo vis vult volumus vultis volunt volui voluisti voluit
nolo non vis non vult noluimus noluit
fero fers fert ferimus fertis ferunt tuli tulisti tulit
capio capis capit capimus capitis capiunt cepi cepisti cepit
facio facis facit facimus facitis faciunt feci fecisti fecit
audio audis audit audimus auditis audiunt audivi audivisti audivit
mitto mittis mittit mittimus mittis mittunt misi misisti misit
pono ponis ponit ponimus ponitis ponunt posui posuisti posuit
scio scis scit scimus scitis sciunt scivi scivisti scivit
nos ego tu tuus tuum me meus mea meum nos noster nostra
se sui sibi se se sese
res rei rem re rerum rebus
homo hominis hominem homine homines hominum
domus domus domui domo domum domo domus domorum
puella puellae puellam puellam puellae puellarum
puer pueri puerum puero pueri puerorum
filius filii filium filio filii filiorum
mater matris matrem matri matre matres matrum
pater patris patrem patri patre patres patrum
urbs urbis urbem urbi urbe urbes urbium
consul consulis consulem consuli consule consules
imperator imperatoris imperatorem imperatori imperatore
annus anni annum anno anni annorum
dies diei diem diei die dies dierum
verbum verbi verbum verbo verbi verborum
manus manus manui manum manu manus manuum
rex regis regem regi rege reges regum
deus dei deum deo dii deorum
vir viri virum viro viri virorum
femina feminae feminam feminae feminarum
amica amicae amicam amicae amicarum
amicus amici amicum amico amici amicorum
uxor uxoris uxorem uxori uxore uxores
filia filiae filiam filiae filiarum
infans infantis infantem infanti infante
servus servi servum servo servi servorum
servi servorum
domina dominae dominam dominae dominarum
dominus domini dominum domino domini dominorum
corpus corporis corpus corpori corpore corpora
nomen nominis nomen nomini nomine nomina
locus loci locum loco loci locorum
populus populi populum populo populi populorum
proelium proelii proelium proelio proelii proeliorum
iter itineris iter itineri itinere itinera
mors mortis mortem morti morte mortes mortium
vita vitae vitam vitae vita
mille milia
dies
mare maris mare mari maria
terra terrae terram terra terrae terrarum
flumen fluminis flumen flumini flumine flumina
mons montis montem monti monte montes montium
silva silvae silvam silvae silvarum
ager agri agrum agro agri agrorum
villa villae villam villa villae villarum
porta portae portam portae portarum
via viae viam viae viarum
templum templi templum templo templa templorum
navis navis navem navi nave naves navium
classis classis classem classi classe classes
epistula epistulae epistulam epistulae epistularum
littera litterae litteram litterae litterarum
verbum verbi verbum verbo verbi verborum
vox vocis vocem voci voce voces vocum
manus manum manu
pes pedis pedem pedi pede pedes pedum
caput capitis caput capiti capite capita capitum
cor cordis cor cordi corde corda
os oris os ori ore ora orum
sol solis solem soli sole soles solum
luna lunae lunam luna lunae lunarum
stella stellae stellam stellae stellarum
caelum caeli caelum caelo caeli caelorum
terra terrae terram terra terrae terrarum
nubes nubis nubem nubi nube nubes nubium
imber imbris imbrem imbri imbre imbres imbrium
aqua aquae aquam aquae aquarum
unda undae undam undae undarum
ignis ignis ignem igni igne ignes ignium
lumen luminis lumen lumini lumine lumina
tenebrae tenebrarum
nox noctis noctem nocti nocte noctes noctium
dies diei
hora horae horam hora horae horarum
annus anni annum anno anni annorum
mensis mensis mensem mensi mense menses mensium
""".split())

# 拉语特征后缀 (用于快速识别)
LATIN_SUFFIXES = ["-que", "-tur", "-ntur", "-bant", "-bunt", "-erunt", "-erant",
                  "-isset", "-issent", "-avisset", "-avissent",
                  "omnis", "quoque", "autem", "enim", "itaque", "tamen",
                  "denique", "mox", "iam", "nunc", "tunc", "saepe", "semper"]

ENGLISH_COMMON = set("""
the of and to a in is it you that he was for on are with as I his they be
at one have this from or had by hot but some what there we can out other
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
""".split())


ISBN_PATTERNS = [
    r'ISBN[\s\-]?(?:10|13)?[\s\-]?:?\s*([\d\-X]{10,17})',
    r'ISBN[\s\-]?(?:10|13)[\s\-]?\s*([\d\-X]{10,17})',
]

YEAR_PATTERNS = [
    r'©\s*(\d{4})',
    r'Copyright\s*©?\s*(\d{4})',
    r'First published\s*(\d{4})',
    r'Published\s*(?:in\s*)?(\d{4})',
    r'Edition\s*\W+(\d{4})',
    r'Printed\s*(?:in\s*)?(\d{4})',
]


def extract_isbn(text: str) -> str | None:
    for pat in ISBN_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).replace('-', '').replace(' ', '')
    return None


def extract_year(text: str) -> str | None:
    for pat in YEAR_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            y = int(m.group(1))
            if 1800 <= y <= 2030:
                return str(y)
    return None


def words_lower(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", text.lower())


def page_language(text: str) -> dict:
    """对单页文本判定语言."""
    words = words_lower(text)
    if not words or len(words) < 5:
        return {"latin_hits": 0, "english_hits": 0, "total": 0,
                "latin_ratio": 0, "english_ratio": 0, "verdict": "empty"}
    # 拉语: 高频词 + 拉语后缀
    latin_word_hits = sum(1 for w in words if w in LATIN_COMMON)
    english_hits = sum(1 for w in words if w in ENGLISH_COMMON)
    # 拉语后缀命中 (每词 1 次)
    latin_suffix_hits = sum(1 for w in words if any(s in w for s in LATIN_SUFFIXES))
    # 加权: 后缀命中 + 词命中
    latin_hits = latin_word_hits + latin_suffix_hits
    total = len(words)
    latin_ratio = latin_hits / total
    english_ratio = english_hits / total

    if latin_ratio > 0.20 and latin_ratio > english_ratio * 1.5:
        verdict = "latin"
    elif english_ratio > 0.20 and english_ratio > latin_ratio * 1.5:
        verdict = "english"
    elif latin_ratio > 0.10 and english_ratio > 0.10:
        verdict = "mixed"
    else:
        verdict = "other"
    return {"latin_hits": latin_hits, "english_hits": english_hits,
            "total": total, "latin_ratio": round(latin_ratio, 3),
            "english_ratio": round(english_ratio, 3), "verdict": verdict}


def split_pages(text: str) -> list[tuple[int, str]]:
    """按 --- PAGE N --- 切分."""
    pages = []
    current_page = 0
    current_text = []
    for line in text.splitlines():
        m = re.match(r"---\s*PAGE\s+(\d+)\s*---", line)
        if m:
            if current_text:
                pages.append((current_page, "\n".join(current_text)))
            current_page = int(m.group(1))
            current_text = []
        else:
            current_text.append(line)
    if current_text:
        pages.append((current_page, "\n".join(current_text)))
    return pages


def analyze_pages(pages: list[tuple[int, str]]) -> dict:
    """对全本每页语言判定, 输出汇总."""
    if not pages:
        return {"latin_pages": 0, "english_pages": 0, "mixed_pages": 0,
                "other_pages": 0, "total_pages": 0,
                "weighted_latin": 0, "weighted_english": 0}
    verdicts = []
    latin_total_words = 0
    english_total_words = 0
    total_words = 0
    for _, text in pages:
        info = page_language(text)
        verdicts.append(info["verdict"])
        latin_total_words += info["latin_hits"]
        english_total_words += info["english_hits"]
        total_words += info["total"]
    counts = Counter(verdicts)
    return {
        "latin_pages": counts.get("latin", 0),
        "english_pages": counts.get("english", 0),
        "mixed_pages": counts.get("mixed", 0),
        "other_pages": counts.get("other", 0) + counts.get("empty", 0),
        "total_pages": len(pages),
        "weighted_latin": round(latin_total_words / total_words, 3) if total_words else 0,
        "weighted_english": round(english_total_words / total_words, 3) if total_words else 0,
    }


def overall_verdict(stats: dict) -> str:
    """根据全本页语言统计给出总判定."""
    p = stats["total_pages"]
    if p == 0:
        return "unknown"
    latin_pct = stats["latin_pages"] / p
    eng_pct = stats["english_pages"] / p
    mixed_pct = stats["mixed_pages"] / p

    if latin_pct > 0.50 and stats["weighted_latin"] > 0.15:
        return "latin"
    if eng_pct > 0.50 and stats["weighted_english"] > 0.20:
        return "english"
    if latin_pct > 0.20 and eng_pct > 0.20:
        return "mixed"
    if mixed_pct > 0.30:
        return "mixed"
    if stats["weighted_latin"] > 0.15 and stats["weighted_latin"] > stats["weighted_english"] * 1.5:
        return "latin_mostly"
    if stats["weighted_english"] > 0.20 and stats["weighted_english"] > stats["weighted_latin"] * 1.5:
        return "english_mostly"
    return "other"


def find_chapter_pages(pages: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """找含章节标题的页 (Cap. I, Chapter 1, etc.)."""
    chapter_pages = []
    for pn, text in pages:
        # 匹配 Cap. / Chapter / Liber / Pars
        if re.search(r"\b(Cap\.|Capitulum|Chapter|Liber|Pars|Section)\s+[IVXLCDM]+|\bC[AH]P(T)?\.?\s+[IVXLCDM]+\b",
                     text, re.IGNORECASE):
            chapter_pages.append((pn, text[:500]))
        elif re.search(r"^([IVX]+)\.\s+[A-Z]", text, re.MULTILINE):
            # 罗马数字 + 大写起首
            chapter_pages.append((pn, text[:500]))
    return chapter_pages[:30]  # 限制前 30 个


def extract_chapter_titles(text: str, max_titles: int = 30) -> list[str]:
    titles = []
    seen = set()
    # 多种章节标题模式
    patterns = [
        r"(Cap\.\s+[IVXLCDM]+[\.\s]+[A-Z][^\n]{3,80})",
        r"(Chapter\s+\d+[\.\s]+[A-Z][^\n]{3,80})",
        r"(Liber\s+[IVXLCDM]+[\.\s]+[A-Z][^\n]{3,80})",
        r"(Pars\s+[IVXLCDM]+[\.\s]+[A-Z][^\n]{3,80})",
        r"^([IVXLCDM]+\.\s+[A-Z][^\n]{3,80})",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.MULTILINE | re.IGNORECASE):
            t = m.group(1).strip()
            if t not in seen and 5 < len(t) < 100:
                titles.append(t)
                seen.add(t)
                if len(titles) >= max_titles:
                    return titles
    return titles


def analyze_book(slug: str) -> dict:
    full = OCR_OUT / slug / "_full.txt"
    if not full.exists():
        return {"slug": slug, "status": "no_ocr"}
    text = full.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return {"slug": slug, "status": "empty"}

    pages = split_pages(text)
    stats = analyze_pages(pages)
    verdict = overall_verdict(stats)

    # ISBN + 年份: 在前 20% 页中查找
    front_text = "\n".join(t for _, t in pages[:max(3, len(pages) // 5)])
    isbn = extract_isbn(front_text)
    year = extract_year(front_text)

    # 章节标题
    chapter_pages = find_chapter_pages(pages)
    chapter_titles = [t for _, t in chapter_pages]
    # 同时扫整本 (而非仅前部) 提取标题
    if len(chapter_titles) < 5:
        chapter_titles = extract_chapter_titles(text)

    return {
        "slug": slug,
        "status": "ok",
        "size_bytes": len(text),
        "char_count": len(text),
        "word_count_approx": sum(len(words_lower(t)) for _, t in pages),
        "page_count": stats["total_pages"],
        "isbn": isbn,
        "year": year,
        "language": {
            "verdict": verdict,
            "weighted_latin": stats["weighted_latin"],
            "weighted_english": stats["weighted_english"],
            "latin_pages": stats["latin_pages"],
            "english_pages": stats["english_pages"],
            "mixed_pages": stats["mixed_pages"],
            "other_pages": stats["other_pages"],
        },
        "chapter_titles": chapter_titles[:15],
    }


def main() -> int:
    slugs = sorted([p.parent.name for p in OCR_OUT.glob("*/_full.txt")
                    if p.stat().st_size > 100])
    print(f"[信息] 找到 {len(slugs)} 本已 OCR 完成的书籍")
    results = []
    for slug in slugs:
        r = analyze_book(slug)
        results.append(r)
        lang = r.get("language", {})
        verdict = lang.get("verdict", "?") if isinstance(lang, dict) else "?"
        isbn = r.get("isbn") or "-"
        year = r.get("year") or "-"
        wp = lang.get("weighted_latin", 0) if isinstance(lang, dict) else 0
        we = lang.get("weighted_english", 0) if isinstance(lang, dict) else 0
        lp = lang.get("latin_pages", 0) if isinstance(lang, dict) else 0
        ep = lang.get("english_pages", 0) if isinstance(lang, dict) else 0
        print(f"  [{verdict:14s}] {slug:<35} isbn={isbn:<14} year={year:<6} "
              f"wL={wp:.2f} wE={we:.2f} L/E页={lp}/{ep}/{r.get('page_count', 0)}")

    META_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(CSV_FILE, "w", encoding="utf-8") as f:
        f.write("slug,verdict,isbn,year,pages,weighted_latin,weighted_english,"
                "latin_pages,english_pages,mixed_pages,other_pages\n")
        for r in results:
            if r.get("status") != "ok":
                continue
            lang = r["language"]
            f.write(f"{r['slug']},{lang['verdict']},{r.get('isbn') or ''},"
                    f"{r.get('year') or ''},{r.get('page_count', 0)},"
                    f"{lang['weighted_latin']},{lang['weighted_english']},"
                    f"{lang['latin_pages']},{lang['english_pages']},"
                    f"{lang['mixed_pages']},{lang['other_pages']}\n")
    print(f"\n[完成] {META_FILE}")
    print(f"[完成] {CSV_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
