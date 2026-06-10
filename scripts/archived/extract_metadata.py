#!/usr/bin/env python3
"""
extract_metadata.py — 从 OCR 文本中提取元信息:
  1. ISBN 编号
  2. 出版年份
  3. 章节标题（从目录页）
  4. **主语言判断** (拉语为主 / 英语为主 / 混合)
  5. 拉语/英语词频统计

输出: analysis_output/reader_metadata.json + reader_metadata.csv
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR_OUT = ROOT / "ocr_output"
META_FILE = ROOT / "analysis_output" / "reader_metadata.json"
CSV_FILE = ROOT / "analysis_output" / "reader_metadata.csv"

# 拉语常见词 (前 100 高频) — 用于判断拉语占比
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
annum annum
verbum verbi verbum verbo verbi verborum
manus manus manui manum manu manus manuum
rex regis regem regi rege reges regum
deus dei deum deo dii deorum
vir viri virum viro viri virorum
femina feminae feminam feminae feminarum
""".split())

# 英语常见词 (前 100 高频)
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


def detect_language(text: str, sample_size: int = 5000) -> dict:
    """
    采样前 sample_size 词, 计算拉语/英语词占比.
    判定规则:
      - 拉语占比 > 50% → 拉语为主
      - 英语占比 > 50% → 英语为主
      - 双方各 30-50% → 混合
    """
    # 提取单词 (简单分词, 仅字母)
    words = re.findall(r"[A-Za-z']+", text[:50000].lower())
    words = words[:sample_size]
    if not words:
        return {"latin_ratio": 0, "english_ratio": 0, "verdict": "unknown",
                "total": 0, "latin_hits": 0, "english_hits": 0}
    latin_hits = sum(1 for w in words if w in LATIN_COMMON)
    english_hits = sum(1 for w in words if w in ENGLISH_COMMON)
    total = len(words)
    # 归一化（除以各自词表大小）后比较
    latin_ratio = latin_hits / total  # 原始命中率
    english_ratio = english_hits / total

    # 判定: 拉语词常见度 100/5000=0.02, 英语 100/5000=0.02 同样
    # 真实拉语书拉丁词命中 > 25%, 英语书英语词命中 > 30%
    if latin_ratio > 0.20 and latin_ratio > english_ratio * 1.5:
        verdict = "latin"
    elif english_ratio > 0.20 and english_ratio > latin_ratio * 1.5:
        verdict = "english"
    elif latin_ratio > 0.10 and english_ratio > 0.10:
        verdict = "mixed"
    else:
        verdict = "other"

    return {
        "latin_ratio": round(latin_ratio, 3),
        "english_ratio": round(english_ratio, 3),
        "verdict": verdict,
        "total": total,
        "latin_hits": latin_hits,
        "english_hits": english_hits,
    }


def extract_chapter_titles(text: str, max_titles: int = 20) -> list[str]:
    """
    提取目录/章节标题.
    启发: 行首单词 + 数字编号模式, 或短行 (<80 字符) 且大写起首.
    """
    titles = []
    seen = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or len(line) > 100:
            continue
        # 排除页码和页眉
        if re.fullmatch(r'\d{1,4}', line):
            continue
        # 含罗马数字 → 可能是章节
        if re.search(r'\b(Cap\.|Capitulum|Chapter|Liber|Chapter\s+\d+|Cap\.\s*\d+)', line, re.I):
            if line not in seen and len(line) > 3:
                titles.append(line)
                seen.add(line)
                if len(titles) >= max_titles:
                    break
    return titles


def analyze_book(slug: str) -> dict:
    full = OCR_OUT / slug / "_full.txt"
    if not full.exists():
        return {"slug": slug, "status": "no_ocr"}
    text = full.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return {"slug": slug, "status": "empty"}

    # 只取前 30% 作为元信息采样 (前几页有版权页, 后面是正文章节)
    # 实际上 ISBN 一定在前 5%, 章节标题在前 30%
    front = text[: int(len(text) * 0.30)]
    body_sample = text[:50000]  # 全文前 50K 用于语言判断

    return {
        "slug": slug,
        "status": "ok",
        "size_bytes": len(text),
        "char_count": len(text),
        "word_count_approx": len(re.findall(r"[A-Za-z']+", text)),
        "isbn": extract_isbn(text[:5000]),
        "year": extract_year(front),
        "language": detect_language(body_sample),
        "chapter_titles": extract_chapter_titles(front),
    }


def main() -> int:
    # 仅扫描已完成的 _full.txt
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
        print(f"  [{verdict:6s}] {slug:<35} isbn={isbn:<14} year={year:<6} "
              f"chars={r.get('char_count', 0):>8,} "
              f"L={lang.get('latin_ratio', 0):.2f} "
              f"E={lang.get('english_ratio', 0):.2f}")

    META_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # CSV 简要
    with open(CSV_FILE, "w", encoding="utf-8") as f:
        f.write("slug,verdict,isbn,year,char_count,word_count_approx,latin_ratio,english_ratio\n")
        for r in results:
            if r.get("status") != "ok":
                continue
            lang = r["language"]
            f.write(f"{r['slug']},{lang['verdict']},{r.get('isbn') or ''},"
                    f"{r.get('year') or ''},{r.get('char_count', 0)},"
                    f"{r.get('word_count_approx', 0)},{lang['latin_ratio']},"
                    f"{lang['english_ratio']}\n")

    print(f"\n[完成] JSON: {META_FILE}")
    print(f"[完成] CSV:  {CSV_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
