#!/usr/bin/env python3
"""
extract_d_class_latin.py — 从 D 类教材中提取纯拉语故事段落

策略:
  1. 对每页文本进行语言判定
  2. 连续 N 页 (>= 3) 都是"拉语为主" → 标记为故事段
  3. 提取段首/段尾的英语讲解内容自动跳过
  4. 输出 analysis_output/d_class_latin_stories.json

D 类目标书籍 (English 主导但有可提取的拉语故事):
  cambridge_1/2/3/4, oxford_1/2/3, reading_latin_text/grammar/study_guide,
  wheelock_7e/reader, dooge_beginners/2, gwynne, ecce_romani/2a/2b/3/combined,
  illiterati_1/2, beginners_latin_book, latin_first_year_magoffin,
  latin_made_simple, latin_natural_method, teach_yourself, revised_latin_primer,
  new_latin_primer, wileys_real_latin, wheelock_answer_key
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR_OUT = ROOT / "ocr_output"
OUT_FILE = ROOT / "analysis_output" / "d_class_latin_stories.json"

# 与 extract_metadata_v2.py 一致的拉/英判定
LATIN_COMMON = set("""
et in est non sunt ad cum de ex ab sub per pro cum sine ut si ne que qui quae
quod hic haec hoc ille illa illud is ea id esse sumus estis sunt habet habent
habebat habebant habeo habes habemus habetis habent habui habuisti habuit
amo amas amat amamus amatis amant amavi amavisti amavit amaverat
vide vides videt videmus videtis vident vidi vidisti vidit
dico dicis dicit dicimus dicitis dicunt dixi dixisti dixit
do das dat damus datis dant dedi dedisti dedit
eo is it imus itis eunt iiisti iit iimus iistis ierunt
venio venis venit venimus venitis veniunt
habeo habes habet habemus habetis habent
possum potes potest possumus possunt potui
res rei rem re rerum rebus homo hominis hominem homine homines hominum
domus domus domui domo domum domo domus domorum puella puellae puellam puellae
puer pueri puerum puero pueri puerorum filius filii filium filio filii filiorum
mater matris matrem matri matre matres matrum pater patris patrem patri patre
urbs urbis urbem urbi urbe urbes urbium annus anni annum anno anni annorum
dies diei diem diei die dies dierum verbum verbi verbum verbo verbi verborum
manus manus manui manum manu manus manuum rex regis regem regi rege reges regum
deus dei deum deo dii deorum vir viri virum viro viri virorum femina feminae
amica amicae amicam amicae amicarum amicus amici amicum amico amicorum
uxor uxoris uxorem uxori uxore uxores filia filiae filiam filiae filiarum
infans infantis infantem infanti infante servus servi servum servo servorum
domina dominae dominam dominae dominarum dominus domini dominum domino
nomen nominis nomen nomini nomine nomina locus loci locum loco locorum
populus populi populum populo populorum proelium proelii proelium proelio
iter itineris iter itineri itinere itinera mors mortis mortem morti morte
vita vitae vitam vitae vita mille milia mare maris mare mari maria
terra terrae terram terra terrae terrarum flumen fluminis flumen flumini
mons montis montem monti monte montes montium silva silvae silvam silvae
ager agri agrum agro agri agrorum villa villae villam villa villae villarum
porta portae portam portae portarum via viae viam viae viarum templum templi
navis navis navem navi nave naves navium epistula epistulae epistulam epistulae
verbum verbi verbum verbo verbi verborum vox vocis vocem voci voce voces vocum
caput capitis caput capiti capite capita capitum cor cordis cor cordi corde
os oris os ori ore ora orum sol solis solem soli sole soles solum
luna lunae lunam luna lunae lunarum stella stellae stellam stellae stellarum
caelum caeli caelum caelo caeli caelorum nubes nubis nubem nubi nube
imber imbris imbrem imbri imbre imbres aqua aquae aquam aquae aquarum
unda undae undam undae undarum ignis ignis ignem igni igne ignes ignium
nox noctis noctem nocti nocte noctes noctium dies diei hora horae horam
annus anni annum anno anni annorum mensis mensis mensem mensi mense
ecce inquit ait dixit respondit videt vident ambulat ambulant sedent sedet
rogat rogat interrogat respondit respondet petit poscit dat accipit
dum cum sine per de ad in ex ab sub super sub inter trans
""".split())

ENGLISH_TOP = set("""
the of and to a in is it you that he was for on are with as i his they be
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
preface introduction contents index review answer question problem fill write
""".split())


def page_lang(text: str) -> tuple[str, float]:
    """对单页文本判定语言."""
    words = re.findall(r"[A-Za-z']+", text.lower())
    if not words or len(words) < 5:
        return "empty", 0.0
    latin_hits = sum(1 for w in words if w in LATIN_COMMON)
    english_hits = sum(1 for w in words if w in ENGLISH_TOP)
    total = len(words)
    latin_ratio = latin_hits / total
    english_ratio = english_hits / total
    if latin_ratio > 0.20 and latin_ratio > english_ratio * 1.2:
        return "latin", latin_ratio
    if english_ratio > 0.20 and english_ratio > latin_ratio * 1.2:
        return "english", english_ratio
    if latin_ratio > 0.10 and english_ratio > 0.10:
        return "mixed", max(latin_ratio, english_ratio)
    return "other", max(latin_ratio, english_ratio)


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


def extract_stories(slug: str) -> dict:
    """提取单本书的拉语故事段."""
    full = OCR_OUT / slug / "_full.txt"
    if not full.exists():
        return {"slug": slug, "status": "no_ocr"}
    text = full.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return {"slug": slug, "status": "empty"}

    pages = split_pages(text)
    if not pages:
        return {"slug": slug, "status": "no_pages"}

    # 判定每页语言
    page_langs = []
    for pn, pt in pages:
        lang, ratio = page_lang(pt)
        page_langs.append((pn, lang, ratio, len(pt)))

    # 找连续 3+ 页都是 latin/mixed 的段
    stories = []
    current_run = []
    for pn, lang, ratio, plen in page_langs:
        if lang in ("latin", "mixed"):
            current_run.append((pn, lang, ratio, plen, pt if False else ""))  # 暂存页码
        else:
            if len(current_run) >= 3:
                stories.append(current_run)
            current_run = []
    if len(current_run) >= 3:
        stories.append(current_run)

    # 合并 stories 中相同/相邻的段
    merged = []
    for run in stories:
        start_pn = run[0][0]
        end_pn = run[-1][0]
        # 重新提取实际内容
        run_pages = [pt for pn2, pt in pages if start_pn <= pn2 <= end_pn]
        body = "\n\n".join(run_pages)
        # 简单去噪: 删除明显英语词占比 > 50% 的页
        body_lines = body.split("\n")
        body_filtered = [ln for ln in body_lines if page_lang(ln)[0] in ("latin", "mixed") or len(ln.split()) < 5]
        merged.append({
            "start_page": start_pn,
            "end_page": end_pn,
            "page_count": end_pn - start_pn + 1,
            "content_chars": len(body),
        })

    total_latin_pages = sum(1 for _, l, _, _ in page_langs if l == "latin")
    total_mixed_pages = sum(1 for _, l, _, _ in page_langs if l == "mixed")
    total_english_pages = sum(1 for _, l, _, _ in page_langs if l == "english")

    return {
        "slug": slug,
        "status": "ok",
        "total_pages": len(pages),
        "latin_pages": total_latin_pages,
        "mixed_pages": total_mixed_pages,
        "english_pages": total_english_pages,
        "latin_story_count": len(merged),
        "latin_story_pages": sum(s["page_count"] for s in merged),
        "stories": merged,
    }


def main() -> int:
    print(f"=== D 类教材拉语故事提取 ===")

    # D 类目标 (根据之前的 vocab_stats_v4 判定 english_mixed/dominant)
    target_slugs = [
        "beginners_latin_book",
        "cambridge_1", "cambridge_2", "cambridge_3", "cambridge_4",
        "conversational_latin",
        "dooge_beginners", "dooge_beginners_2", "dooge_beginners_key",
        "ecce_romani", "ecce_romani_2a", "ecce_romani_2b", "ecce_romani_3",
        "ecce_romani_combined",
        "gwynne",
        "illiterati_1", "illiterati_2",
        "latin_first_year_magoffin", "latin_made_simple", "latin_natural_method",
        "new_latin_primer", "oxford_1", "oxford_2", "oxford_3",
        "reading_latin_grammar", "reading_latin_study_guide", "reading_latin_text",
        "revised_latin_primer", "teach_yourself",
        "wheelock_7e", "wheelock_answer_key", "wheelock_reader",
        "wileys_real_latin",
    ]

    results = []
    for slug in target_slugs:
        r = extract_stories(slug)
        if r.get("status") != "ok":
            continue
        results.append(r)
        print(f"  [{slug:30s}] 拉语页={r['latin_pages']:>3d} 混合={r['mixed_pages']:>3d} "
              f"英语={r['english_pages']:>3d} 故事段={r['latin_story_count']:>2d} "
              f"故事总页={r['latin_story_pages']:>3d}")

    # 汇总
    total_latin_pages = sum(r["latin_pages"] for r in results)
    total_mixed_pages = sum(r["mixed_pages"] for r in results)
    total_story_pages = sum(r["latin_story_pages"] for r in results)
    total_books = len(results)
    books_with_stories = sum(1 for r in results if r["latin_story_pages"] >= 5)

    summary = {
        "total_d_class_books": total_books,
        "books_with_latin_stories": books_with_stories,
        "total_latin_pages": total_latin_pages,
        "total_mixed_pages": total_mixed_pages,
        "total_latin_story_pages": total_story_pages,
        "books": results,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print()
    print(f"=== 汇总 ===")
    print(f"  D 类目标书籍: {total_books}")
    print(f"  含可提取拉语故事: {books_with_stories}")
    print(f"  拉语主页面总数: {total_latin_pages}")
    print(f"  拉英混合页总数: {total_mixed_pages}")
    print(f"  故事段总页数: {total_story_pages}")
    print(f"\n输出: {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
