#!/usr/bin/env python3
"""
generate_report_data.py — 为 reader_audit_report.md 准备完整数据
============================================================

数据源:
  - analysis_output/reader_vocab_stats_v4.json   (55 本 v4 词频分析)
  - analysis_output/reader_metadata_v2.csv       (元信息: ISBN/年份/作者/拉英页)
  - analysis_output/d_class_latin_stories.json   (D 类教材中提取的拉语故事段)

输出:
  - analysis_output/reader_report_data.json      (整合后数据, 供报告渲染)
  - analysis_output/reader_report_data.md        (预览, 检查用)
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V4_JSON = ROOT / "analysis_output" / "reader_vocab_stats_v4.json"
META_CSV = ROOT / "analysis_output" / "reader_metadata_v2.csv"
D_STORIES = ROOT / "analysis_output" / "d_class_latin_stories.json"
OUT_JSON = ROOT / "analysis_output" / "reader_report_data.json"
OUT_MD = ROOT / "analysis_output" / "reader_report_data.md"

# ============== 加载元信息 ==============
meta = {}
with open(META_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        meta[row["slug"]] = row

# ============== 加载 v4 词频分析 ==============
v4_data = []
with open(V4_JSON, "r", encoding="utf-8") as f:
    v4_data = json.load(f)

# ============== 加载 D 类拉语故事提取 ==============
d_class_stories = {}
if D_STORIES.exists():
    with open(D_STORIES, "r", encoding="utf-8") as f:
        d = json.load(f)
        for b in d.get("books", []):
            d_class_stories[b["slug"]] = b

# ============== 加载手工标注的 tier (来源: reclassified/ 子目录) ==============
TIER_BY_SLUG = {
    # A1_latin_story — 纯拉语入门
    "pugio_bruti": ("A1_latin_story", "Pugio Bruti / Rico & Polis", "习得法27章, 拉语为主"),
    "regulus": ("A1_latin_story", "Regulus / Saint-Exupéry 拉语版", "小王子作者拉语版, 现代小说风"),
    "diocles_flora": ("A1_latin_story", "Dioclēs et Flōra", "习得法, 罗马日常生活"),
    "forum_lectiones": ("A1_latin_story", "Forum - Lectiones Latinitatis Vivae / Polis", "习得法对话+故事, TPR 教学法"),
    "via_latina_romanorum": ("A1_latin_story", "Via Latina: De lingua et vita Romanorum", "习得法罗马生活读本"),
    "chickering": ("A1_latin_story", "First Latin Reader / Chickering", "经典初级"),
    "latin_lower_forms": ("A1_latin_story", "Latin Reader for Lower Forms / Hardy 1889", "经典初级"),
    "hobbitus": ("A2_latin_novel", "Hobbitus Ille / Tolkien 拉语版", "现代长篇拉语小说, 学完FR后可读"),
    # A1_mixed_story
    "ora_maritima": ("A1_mixed_story", "Ora Maritima / Sonnenschein 1900", "主体拉语+前后英语教学说明"),
    "pro_patria": ("A1_mixed_story", "Pro Patria / Sonnenschein 1907", "同上, Sonnenschein系列续作"),
    "unus_duo_tres": ("A1_mixed_story", "Unus Duo Tres / Polis", "习得法Vol.1, 拉语故事+图"),
    "nutting_reader": ("A1_mixed_story", "A First Latin Reader / Nutting", "经典入门, 拉英混合"),
    "olimpia_daedalus": ("A1_mixed_story", "Daedalus et Icarus / Olimpi", "分层阅读法, 难度递进"),
    "olimpia_pyramus": ("A1_mixed_story", "Pyramus and Thisbe / Olimpi", "同上"),
    "olimpia_nicholas": ("A1_mixed_story", "Mysterious Traveler / Olimpi", "中世纪题材"),
    "via_latina_easy": ("A1_mixed_story", "Via Latina: Easy Latin Reader / Collar 1897", "罗马地理, 拉英对照"),
    # B 类别
    "reynolds_reader": ("B1_mixed_story", "Latin Reader / Reynolds", "中级改写, 主体拉语+英语注解"),
    "intermediate_oral_cicero": ("B1_mixed_text", "Intermediate Oral Latin Reader", "Cicero De Senectute 改写"),
    "fabulae_faciles": ("B_mixed_text", "Fabulae Faciles / Ritchie 1889", "经典短故事"),
    "septimus": ("B_mixed_text", "Septimus / Chambers 1910", "经典入门, 主体拉语"),
    "second_year_latin": ("B2_mixed_text", "Second Year Latin / Greenough 1899", "二年级选集, 英语注释"),
    "conversational_latin": ("B_mixed_dialog", "Conversational Latin for Oral Proficiency / Traupman 2007", "对话手册, 拉英逐句对照"),
    # D 类别 (教材)
    "wheelock_7e": ("D_textbook", "Wheelock's Latin 7e / Wheelock-LaFleur", "语法教材"),
    "wheelock_reader": ("D_textbook", "Wheelock's Latin Reader", "教材配套读物"),
    "wheelock_answer_key": ("D_textbook", "Wheelock's Latin 7e Answer Key", "教材答案"),
    "cambridge_1": ("D_textbook", "Cambridge Latin Course Book 1", "CLB1 教材"),
    "cambridge_2": ("D_textbook", "Cambridge Latin Course Book 2", "CLB2 教材"),
    "cambridge_3": ("D_textbook", "Cambridge Latin Course Book 3", "CLB3 教材"),
    "cambridge_4": ("D_textbook", "Cambridge Latin Course Book 4", "CLB4 教材"),
    "oxford_1": ("D_textbook", "Oxford Latin Course Part 1, 2e", "OLC1 教材"),
    "oxford_2": ("D_textbook", "Oxford Latin Course Part 2, 2e", "OLC2 教材"),
    "oxford_3": ("D_textbook", "Oxford Latin Course Part 3, 2e", "OLC3 教材"),
    "ecce_romani": ("D_textbook", "Ecce Romani I", "ER1 教材"),
    "ecce_romani_2a": ("D_textbook", "Ecce Romani IIA (2005 Prentice Hall)", "ER2A 学生版"),
    "ecce_romani_2b": ("D_textbook", "Ecce Romani IIB (Addison Wesley)", "ER2B 学生手册"),
    "ecce_romani_3": ("D_textbook", "Ecce Romani III / Perry", "ER3 教材"),
    "reading_latin_text": ("D_textbook", "Reading Latin Text 2e", "RLT 教材"),
    "reading_latin_grammar": ("D_textbook", "Reading Latin Grammar 2e", "RLG 教材"),
    "reading_latin_study_guide": ("D_textbook", "Reading Latin Study Guide", "RLS 教材"),
    "dooge_beginners": ("D_textbook", "Latin for Beginners / D'Ooge", "D'Ooge 教材"),
    "dooge_beginners_2": ("D_textbook", "Latin for Beginners / D'Ooge (另一版)", "D'Ooge 教材"),
    "dooge_beginners_key": ("D_textbook", "Latin for Beginners Key / D'Ooge", "D'Ooge 答案"),
    "gwynne": ("D_textbook", "Gwynne's Latin", "Gwynne 教材"),
    "latin_made_simple": ("D_textbook", "Latin Made Simple", "入门教材"),
    "teach_yourself": ("D_textbook", "Teach Yourself Beginner's Latin", "自学教材"),
    "latin_natural_method": ("D_textbook", "Latin by the Natural Method / W.G. Most", "习得法教材"),
    "latin_first_year_magoffin": ("D_textbook", "Latin First Year / Magoffin", "教材"),
    "illiterati_1": ("D_textbook", "Latin for the Illiterati / Jon R. Stone", "实用词汇"),
    "illiterati_2": ("D_textbook", "More Latin for the Illiterati / Jon R. Stone", "实用词汇"),
    "revised_latin_primer": ("D_textbook", "The Revised Latin Primer / Kennedy", "语法书"),
    "new_latin_primer": ("D_textbook", "A New Latin Primer", "语法书"),
    "wileys_real_latin": ("D_textbook", "Wiley's Real Latin / Maltby-Belcher", "语法/词汇"),
    "latin_stories_wheelock": ("D_stories", "Latin Stories / Wheelock 配套", "Wheelock 配套短篇"),
}

# ============== 整合 ==============
records = []
for v4 in v4_data:
    slug = v4["slug"]
    m = meta.get(slug, {})
    tier, title, note = TIER_BY_SLUG.get(slug, ("unknown", slug, ""))

    # 拉语段提取 (D 类) / 已知混合故事的页数
    d = d_class_stories.get(slug, {})
    latin_story_pages = d.get("latin_story_pages", 0)
    latin_story_count = d.get("latin_story_count", 0)
    stories = d.get("stories", [])

    rec = {
        "slug": slug,
        "title": title,
        "tier": tier,
        "note": note,
        "isbn": m.get("isbn", ""),
        "year": m.get("year", ""),
        "total_pages": int(m.get("pages", 0) or 0),
        "latin_pages_v2": int(m.get("latin_pages", 0) or 0),
        "english_pages_v2": int(m.get("english_pages", 0) or 0),
        # v4 数据
        "latin_word_count": v4["latin_word_count"],
        "english_word_count": v4["english_word_count"],
        "unique_latin_count": v4["unique_latin_count"],
        "english_ratio": round(v4["english_ratio"], 4),
        "verdict": v4["verdict"],
        "starting_chapter_50": v4.get("starting_chapter_50"),
        "starting_chapter_60": v4.get("starting_chapter_60"),
        "starting_chapter_70": v4.get("starting_chapter_70"),
        "starting_chapter_80": v4.get("starting_chapter_80"),
        "peak_chapter": v4.get("peak_chapter"),
        "peak_coverage": v4.get("peak_coverage"),
        "best_teach_chapter": v4.get("best_teach_chapter"),
        "best_teach_coverage": v4.get("best_teach_coverage"),
        # D 类提取
        "latin_story_count": latin_story_count,
        "latin_story_pages": latin_story_pages,
        "stories": stories[:5] if stories else [],  # 最多保留5段
    }
    records.append(rec)

# ============== 排序: 按「可读起点章节」升序 ==============
# 规则:
#  1. 有 starting_chapter_60 (学完 Cap.X 后60%可读) 优先
#  2. 否则有 starting_chapter_50
#  3. 否则 peak_chapter (即峰值章节, 即最大学习价值章节)
#  4. None 排最后
def sort_key(r):
    s60 = r.get("starting_chapter_60")
    s50 = r.get("starting_chapter_50")
    peak = r.get("peak_chapter") or 999
    if s60 is not None:
        primary = s60
        tier_pri = 0
    elif s50 is not None:
        primary = s50
        tier_pri = 1
    else:
        primary = peak
        tier_pri = 2
    return (tier_pri, primary, -r["unique_latin_count"])

records.sort(key=sort_key)

# ============== 分组 (按verdict, 4类) ==============
groups = defaultdict(list)
for r in records:
    groups[r["verdict"]].append(r)

# ============== 写入 JSON ==============
OUT_JSON.write_text(
    json.dumps(records, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"[OK] {OUT_JSON.name} ({OUT_JSON.stat().st_size:,} bytes)")

# ============== 写入 Markdown 预览 ==============
md = []
md.append("# 读物报告数据预览\n")
md.append(f"总数: {len(records)} 本 | 来源: v4 词频分析 + 元信息 + D类拉语提取\n")
md.append("\n## 按可读起点章节排序 (前20本预览)\n\n")
md.append("| # | slug | 标题 | tier | 拉词 | 独词 | 英% | 起点60 | 起点50 | 峰值 | 教学 | verdict |\n")
md.append("|---|------|------|------|------:|------:|----:|-------:|-------:|-----:|-----:|---------|\n")
for i, r in enumerate(records[:20], 1):
    md.append(
        f"| {i} | `{r['slug']}` | {r['title'][:30]} | {r['tier']} | "
        f"{r['latin_word_count']:,} | {r['unique_latin_count']:,} | "
        f"{r['english_ratio']:.0%} | "
        f"{r['starting_chapter_60'] or '-'} | {r['starting_chapter_50'] or '-'} | "
        f"Cap.{r['peak_chapter']}({r['peak_coverage']:.0%}) | "
        f"Cap.{r['best_teach_chapter']}({r['best_teach_coverage']:.0%}) | "
        f"{r['verdict']} |\n"
    )

md.append("\n## verdict 分布\n\n")
from collections import Counter
vc = Counter(r["verdict"] for r in records)
for v, c in vc.most_common():
    md.append(f"- **{v}**: {c} 本\n")

OUT_MD.write_text("".join(md), encoding="utf-8")
print(f"[OK] {OUT_MD.name} ({OUT_MD.stat().st_size:,} bytes)")
print()
print("=== 分布汇总 ===")
print(f"  Total books: {len(records)}")
print(f"  Verdict: {dict(vc)}")
print(f"  Tier: {Counter(r['tier'] for r in records).most_common()}")
print()
print("=== 起点章节分布 ===")
s60_books = [r for r in records if r.get("starting_chapter_60") is not None]
s50_only = [r for r in records if r.get("starting_chapter_60") is None and r.get("starting_chapter_50") is not None]
no_anchor = [r for r in records if r.get("starting_chapter_60") is None and r.get("starting_chapter_50") is None]
print(f"  起点60%已确定: {len(s60_books)} 本")
print(f"  起点50%已确定: {len(s50_only)} 本")
print(f"  无明确起点: {len(no_anchor)} 本")
