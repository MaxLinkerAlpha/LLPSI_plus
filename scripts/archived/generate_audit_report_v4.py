#!/usr/bin/env python3
"""
generate_audit_report_v4.py — 完全重写 reader_audit_report.md

报告结构 (按学习阶段分章):
  0. TL;DR
  1. 评价体系 (替代 A1/A2)
  2. 按学习阶段分章(主体)
     2.1 FR Cap.1-15 入门期
     2.2 FR Cap.16-25 初级期
     2.3 FR Cap.26-35 中级期
     2.4 RA Cap.36-45 高级期
     2.5 RA Cap.46-56 完成期
     2.6 查阅使用
  3. D类教材拉语段 (35段/162页)
  4. 数据/方法
  5. 附录
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
DATA = ROOT / "analysis_output" / "reader_vocab_stats_v4.json"
D_SEGS = ROOT / "analysis_output" / "d_segments_vocab.json"
D_SEGS_MD = ROOT / "analysis_output" / "d_segments_vocab.md"
OUT = ROOT / "docs" / "reader_audit_report.md"

# 标题映射(常用slug)
TITLES = {
    "pugio_bruti": "Pugio Bruti (Rico & Polis)",
    "via_latina_romanorum": "Via Latina: De Lingua et Vita Romanorum",
    "dooge_beginners_key": "D'Ooge Latin for Beginners Key",
    "diocles_flora": "Dioclēs et Flōra",
    "regulus": "Regulus (Saint-Exupéry 拉语版)",
    "chickering": "First Latin Reader (Chickering)",
    "latin_lower_forms": "Latin Reader for Lower Forms (Hardy 1889)",
    "hobbitus": "Hobbitus Ille (Tolkien 拉语版)",
    "forum_lectiones": "Forum - Lectiones Latinitatis Vivae (Polis)",
    "conversational_latin": "Conversational Latin for Oral Proficiency (Traupman 2007)",
    "intermediate_oral_cicero": "Intermediate Oral Latin Reader (Cicero De Senectute)",
    "fabulae_faciles": "Fabulae Faciles (Ritchie 1889)",
    "nutting_reader": "A First Latin Reader (Nutting)",
    "reynolds_reader": "Latin Reader (Reynolds)",
    "via_latina_easy": "Via Latina: Easy Latin Reader (Collar 1897)",
    "septimus": "Septimus (Chambers 1910)",
    "olimpia_daedalus": "Daedalus et Icarus (Olimpi)",
    "olimpia_nicholas": "The Mysterious Traveler (Olimpi)",
    "olimpia_pyramus": "Reckless Love: Pyramus and Thisbe (Olimpi)",
    "ora_maritima": "Ora Maritima (Sonnenschein 1900)",
    "pro_patria": "Pro Patria (Sonnenschein 1907)",
    "unus_duo_tres": "Unus Duo Tres: Latine Loquamur per Scaenas",
    "second_year_latin": "Second Year Latin (Greenough 1899)",
    "cambridge_1": "Cambridge Latin Course 1",
    "cambridge_2": "Cambridge Latin Course 2",
    "cambridge_3": "Cambridge Latin Course 3",
    "cambridge_4": "Cambridge Latin Course 4",
    "oxford_1": "Oxford Latin Course Part 1, 2e",
    "oxford_2": "Oxford Latin Course Part 2, 2e",
    "oxford_3": "Oxford Latin Course Part 3, 2e",
    "ecce_romani": "Ecce Romani I",
    "ecce_romani_2a": "Ecce Romani IIA (2005 Prentice Hall)",
    "ecce_romani_2b": "Ecce Romani IIB (Addison Wesley)",
    "ecce_romani_3": "Ecce Romani III (Perry)",
    "ecce_romani_combined": "Ecce Romani I&II Combined (EPUB, 已丢弃)",
    "wheelock_7e": "Wheelock's Latin 7e",
    "wheelock_reader": "Wheelock's Latin Reader",
    "wheelock_answer_key": "Wheelock's Latin 7e Answer Key",
    "dooge_beginners": "Latin for Beginners (D'Ooge)",
    "dooge_beginners_2": "Latin for Beginners (D'Ooge 另一版)",
    "gwynne": "Gwynne's Latin",
    "latin_made_simple": "Latin Made Simple",
    "teach_yourself": "Teach Yourself Beginner's Latin",
    "latin_natural_method": "Latin by the Natural Method (W.G. Most 1957)",
    "latin_first_year_magoffin": "Latin First Year (Magoffin)",
    "illiterati_1": "Latin for the Illiterati (Stone)",
    "illiterati_2": "More Latin for the Illiterati (Stone)",
    "revised_latin_primer": "The Revised Latin Primer (Kennedy)",
    "new_latin_primer": "A New Latin Primer",
    "wileys_real_latin": "Wiley's Real Latin (Maltby & Belcher)",
    "reading_latin_text": "Reading Latin: Text (2e)",
    "reading_latin_grammar": "Reading Latin: Grammar (2e)",
    "reading_latin_study_guide": "Reading Latin: Study Guide",
    "beginners_latin_book": "Beginner's Latin Book (Textkit)",
    "latin_stories_wheelock": "Latin Stories (Wheelock 配套)",
    "probe": "Probe (已删除)",
    "nunc_loquamur": "Nunc Loquamur (已删除)",
}

STAGE_INFO = [
    ("FR Cap.1-15 入门期", "0_cap1-15_入门", 1, 15),
    ("FR Cap.16-25 初级期", "1_cap16-25_初级", 16, 25),
    ("FR Cap.26-35 中级期", "2_cap26-35_FR中级", 26, 35),
    ("RA Cap.36-45 高级期", "3_cap36-45_RA前", 36, 45),
    ("RA Cap.46-56 完成期", "4_cap46-56_RA后", 46, 56),
    ("查阅使用", "5_reference_查阅", None, None),
]

LEVEL_DESC = {
    "fluent": "顺畅可读 (≥60%)",
    "challenging": "有挑战 (40-60%)",
    "selected": "节选可读 (20-40%)",
    "reference": "查阅使用 (<20%)",
}


def title_of(slug: str) -> str:
    return TITLES.get(slug, slug)


def short(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n - 1] + "…"


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    d_segs = json.loads(D_SEGS.read_text(encoding="utf-8"))

    # 准备按阶段分组 (排除已丢弃的 ecce_romani_combined)
    EXCLUDED_SLUGS = {"ecce_romani_combined"}
    by_stage = {s[0]: [] for s in STAGE_INFO}
    for d in data:
        if d["slug"] in EXCLUDED_SLUGS:
            continue
        stage = d.get("stage", "未达(查阅使用)")
        if stage not in by_stage:
            by_stage["查阅使用"] = by_stage.get("查阅使用", [])
            by_stage["查阅使用"].append(d)
        else:
            by_stage[stage].append(d)

    # 排序: 每阶段内, 按reading_level(优先级) + 起点章节 + 拉词量
    LEVEL_ORDER = {"fluent": 0, "challenging": 1, "selected": 2, "reference": 3}
    for s in by_stage:
        by_stage[s].sort(key=lambda x: (
            LEVEL_ORDER.get(x.get("reading_level"), 9),
            x.get("reading_level_chapter") or 999,
            -x.get("unique_latin_count", 0),
        ))

    # 统计
    level_counts = Counter(d["reading_level"] for d in data if d["slug"] not in EXCLUDED_SLUGS)
    stage_counts = {s[0]: len(by_stage[s[0]]) for s in STAGE_INFO}

    out = []
    out.append("# Other_Readers 读物评估报告 (v4.0 完全重写)")
    out.append("")
    out.append("> **报告版本**: v4.0.0 | **生成日期**: 2026-06-06")
    out.append("> **审计范围**: `source/Other_Readers/` 下全部 55 份 PDF / EPUB (Non-LLPSI 读物)")
    out.append("> **核心指标**: **可读起点** (学完LLPSI Cap.X) + **教学价值** (复习哪章新词)")
    out.append("> **方法**: 全本 OCR (13482 页) + 拉英词频加权 + 章节级 known/new 词覆盖计算 + D 类拉语段提取")
    out.append("")
    out.append("---")
    out.append("")

    # 0. TL;DR
    out.append("## 0. TL;DR — 一图速览")
    out.append("")
    out.append("### 4 档可读性分布 (替代 A1/A2/B1/B2)")
    out.append("")
    out.append("| 档位 | 阈值 | 数量 | 含义 |")
    out.append("|------|------|----:|------|")
    for level in ("fluent", "challenging", "selected", "reference"):
        n = level_counts.get(level, 0)
        out.append(f"| **{level}** | {LEVEL_DESC[level]} | {n} | { _level_meaning(level)} |")
    out.append("")
    out.append("### 按学习阶段分组 (按 reading_level_chapter 划分)")
    out.append("")
    out.append("| 阶段 | 章节范围 | 数量 | 典型读物 |")
    out.append("|------|---------|----:|---------|")
    for stage, _, lo, hi in STAGE_INFO:
        n = stage_counts.get(stage, 0)
        # 该阶段第一本
        first = by_stage[stage][0]["slug"] if by_stage[stage] else "—"
        rng = f"Cap.{lo}-{hi}" if lo else "—"
        out.append(f"| {stage} | {rng} | {n} | `{first}` |")
    out.append("")
    out.append("### 核心推荐")
    out.append("")
    out.append("1. **完成 FR 后奖励读物 (2 本)**: `pugio_bruti` (学完 Cap.48) / `via_latina_romanorum` (学完 Cap.52)")
    out.append("2. **FR 后期挑战阅读 (13 本)**: 大部分是 `challenging` 级别, 教学价值集中在 FR Cap.1-4 基础词汇")
    out.append("3. **D 类教材拉语段 (16 本/162 页)**: 详见 §3, 适合做 LLPSI 章节的扩展阅读")
    out.append("4. **拉英对话手册**: `conversational_latin` (415 页), 适合口语训练")
    out.append("")

    out.append("---")
    out.append("")

    # 1. 评价体系
    out.append("## 1. 评价体系 (替代 A1/A2)")
    out.append("")
    out.append("本报告 **彻底抛弃 A1/A2/B1/B2 CEFR 分级**, 使用三个**可量化、可验证**的指标:")
    out.append("")
    out.append("| 指标 | 含义 | 用途 |")
    out.append("|------|------|------|")
    out.append("| **可读起点** (`reading_level_chapter`) | 学完 LLPSI Cap.N 后, FR 已知词覆盖本书拉语独词达到 X% 的最早章节 | \"我学完第X章能读这本书吗?\" |")
    out.append("| **教学价值** (`best_teach_chapter`) | 本书覆盖 LLPSI Cap.M 新词最多的章节 (高=适合复习该章) | \"我想复习第X章新词, 哪本最好?\" |")
    out.append("| **4 档可读性** | fluent / challenging / selected / reference, 基于 FR 已知词覆盖率 | 一眼看出\"能不能读\" |")
    out.append("")

    out.append("### 1.1 4 档可读性详解")
    out.append("")
    out.append("| 档位 | 覆盖率阈值 | 学习含义 | 推荐用法 |")
    out.append("|------|-----------|---------|---------|")
    out.append("| **fluent** (顺畅) | ≥60% | 通读无压力, 仅需少量注释 | 奖励读物 / 通读训练 |")
    out.append("| **challenging** (挑战) | 40-60% | 需配合注释/字典 | 复习扩展 / 课外训练 |")
    out.append("| **selected** (节选) | 20-40% | 不适合通读, 适合节选/对照 | 对照阅读 / 词汇扩展 |")
    out.append("| **reference** (查阅) | <20% | 拉语含量太低 | 词汇/语法查阅 |")
    out.append("")

    out.append("### 1.2 学习阶段分组")
    out.append("")
    out.append("| 阶段 | 章节范围 | 推荐读物类型 |")
    out.append("|------|---------|-------------|")
    out.append("| **FR Cap.1-15 入门期** | 入门对话+生活 | 短小对话/初级故事 |")
    out.append("| **FR Cap.16-25 初级期** | 语法加深 | 中篇故事/分级读物 |")
    out.append("| **FR Cap.26-35 中级期** | 罗马历史/文化 | 长篇经典 (Nutting, LLPSI 风格的) |")
    out.append("| **RA Cap.36-45 高级期** | 古典散文/历史 | Cicero 改写, Ecce Romani 3, 习得法短篇 |")
    out.append("| **RA Cap.46-56 完成期** | 高级古典/诗歌 | Pugio Bruti, Via Latina Romanorum |")
    out.append("| **查阅使用** | 不适合通读 | 教材/字典/参考 |")
    out.append("")

    out.append("---")
    out.append("")

    # 2. 按学习阶段分章
    out.append("## 2. 按学习阶段分章")
    out.append("")
    out.append("> 每章内按可读性 (`fluent` > `challenging` > `selected`) → 起点章节 → 拉词量 升序排列.")
    out.append("> \"起点 Cap.X\" 指学完该章后, FR 已知词可覆盖本书拉语独词达到 4 档中的某一档.")
    out.append("")

    for stage, dir_name, lo, hi in STAGE_INFO:
        books = by_stage[stage]
        if not books:
            continue
        out.append(f"### 2.{STAGE_INFO.index((stage, dir_name, lo, hi)) + 1} {stage} ({len(books)} 本)")
        out.append("")
        if dir_name:
            out.append(f"**目录**: `source/Other_Readers/reclassified_v2/{dir_name}/`")
        out.append("")

        out.append("| # | slug | 标题 | 拉词 | 独词 | 英% | 档位 | 起点 Cap. | 教学 Cap. (覆盖) | 峰值 Cap. (覆盖) |")
        out.append("|---|------|------|----:|----:|----:|------|----------:|-----------------:|----------------:|")
        for i, d in enumerate(books, 1):
            level = d.get("reading_level", "—")
            ch = d.get("reading_level_chapter")
            s_ch = f"Cap.{ch}" if ch else "—"
            tc = d.get("best_teach_chapter")
            s_tc = f"Cap.{tc} ({d['best_teach_coverage']:.0%})" if tc else "—"
            pk = d.get("peak_chapter")
            s_pk = f"Cap.{pk} ({d['peak_coverage']:.0%})" if pk else "—"
            en = d.get("english_ratio", 0)
            uw = d.get("unique_latin_count", 0)
            lw = d.get("latin_word_count", 0)
            slug = d["slug"]
            title = short(title_of(slug), 35)
            out.append(
                f"| {i} | `{slug}` | {title} | {lw:,} | {uw:,} | {en:.0%} | "
                f"{level} | {s_ch} | {s_tc} | {s_pk} |"
            )
        out.append("")

        # 重点读物
        highlights = [d for d in books if d.get("reading_level") in ("fluent", "challenging")]
        if highlights:
            out.append("**重点读物**:")
            for d in highlights[:3]:
                slug = d["slug"]
                level = d.get("reading_level")
                ch = d.get("reading_level_chapter")
                tc = d.get("best_teach_chapter")
                tcv = d.get("best_teach_coverage", 0)
                out.append(
                    f"- `{slug}` ({title_of(slug)}): **{level}** 起点 Cap.{ch}, "
                    f"教学价值 Cap.{tc} ({tcv:.0%})"
                )
            out.append("")

    out.append("---")
    out.append("")

    # 3. D类教材拉语段
    out.append("## 3. D 类教材拉语段提取 (16 本 / 35 段 / 162 页)")
    out.append("")
    out.append("> 通过 `scripts/extract_d_class_latin.py` 从 D 类教材中提取连续 3+ 页的拉语故事段, "
               "再通过 `scripts/analyze_d_class_latin_v2.py` 计算每段的 LLPSI 章节锚点.")
    out.append("> 这些段是\"黄金拉语段\"——从英语讲解为主的教材中挖出的连续拉语故事, 适合做 LLPSI 扩展阅读.")
    out.append("")

    # 按book聚合
    by_book = {}
    for seg in d_segs["segments"]:
        by_book.setdefault(seg["slug"], []).append(seg)
    for slug in by_book:
        by_book[slug].sort(key=lambda x: x.get("start_page", 0))

    out.append("### 3.1 按教材汇总")
    out.append("")
    out.append("| # | slug | 段数 | 总页 | 拉词(总) | 独词(总) | 起点 Cap.范围 | 教学 Cap.范围 |")
    out.append("|---|------|----:|----:|--------:|--------:|-------------|-------------|")
    for slug in sorted(by_book.keys(), key=lambda s: -sum(x.get("page_count", 0) for x in by_book[s])):
        segs = by_book[slug]
        total_pages = sum(s.get("page_count", 0) for s in segs)
        total_words = sum(s.get("latin_word_count", 0) for s in segs)
        total_unique = sum(s.get("unique_latin_count", 0) for s in segs)
        starts = [s.get("starting_chapter_50") for s in segs if s.get("starting_chapter_50")]
        start_range = f"Cap.{min(starts)}-{max(starts)}" if starts else "—"
        teaches = [(s.get("best_teach_chapter"), s.get("best_teach_coverage", 0)) for s in segs if s.get("best_teach_chapter")]
        if teaches:
            tch = Counter(t[0] for t in teaches).most_common(1)[0][0]
            tcovs = [t[1] for t in teaches if t[0] == tch]
            teach_range = f"Cap.{tch} ({max(tcovs):.0%})"
        else:
            teach_range = "—"
        out.append(
            f"| | `{slug}` | {len(segs)} | {total_pages} | {total_words:,} | {total_unique:,} | "
            f"{start_range} | {teach_range} |"
        )
    out.append("")

    out.append("### 3.2 段级详表 (按 page_count 降序)")
    out.append("")
    out.append("| # | slug | 起始页 | 页数 | 拉词 | 独词 | 英% | 起点50% | 起点60% | 教学 Cap. (覆盖) | 用途 |")
    out.append("|---|------|------:|----:|-----:|----:|----:|--------:|--------:|----------------:|------|")
    segs_sorted = sorted(d_segs["segments"], key=lambda x: -x.get("page_count", 0))
    for i, seg in enumerate(segs_sorted, 1):
        slug = seg["slug"]
        s50 = f"Cap.{seg['starting_chapter_50']}" if seg.get("starting_chapter_50") else "—"
        s60 = f"Cap.{seg['starting_chapter_60']}" if seg.get("starting_chapter_60") else "—"
        tc = seg.get("best_teach_chapter")
        s_tc = f"Cap.{tc} ({seg['best_teach_coverage']:.0%})" if tc else "—"
        en = seg.get("english_ratio", 0)
        uw = seg.get("unique_latin_count", 0)
        lw = seg.get("latin_word_count", 0)
        # 推荐用途
        if seg.get("starting_chapter_50") and seg["starting_chapter_50"] <= 35:
            usage = "FR扩展阅读"
        elif seg.get("starting_chapter_50") and seg["starting_chapter_50"] <= 50:
            usage = "RA扩展阅读"
        else:
            usage = "高级扩展"
        out.append(
            f"| {i} | `{slug}` | p.{seg['start_page']} | {seg['page_count']} | "
            f"{lw:,} | {uw:,} | {en:.0%} | {s50} | {s60} | {s_tc} | {usage} |"
        )
    out.append("")
    out.append("**详细分析**: `analysis_output/d_segments_vocab.md` (35 段完整列表)")
    out.append("")

    out.append("---")
    out.append("")

    # 4. 数据/方法
    out.append("## 4. 数据与方法")
    out.append("")
    out.append("### 4.1 词频 + 章节锚点算法 (v5)")
    out.append("")
    out.append("**脚本**: `scripts/analyze_readers_v5.py`")
    out.append("")
    out.append("**算法**:")
    out.append("")
    out.append("1. 加载 OCR 全文 (`ocr_output/<slug>/_full.txt`)")
    out.append("2. 拉英分词 (基于词频词表 + 后缀特征, 复用 v4 算法)")
    out.append("3. 加载 LLPSI FR 1-35 章 + RA 36-56 章累计词表 (`data/llpsi_corpus.db` 的 `fr_vocab` 表)")
    out.append("4. 对每本书:")
    out.append("   - 计算 `unique_latin_count` = 唯一拉语词形数")
    out.append("   - 对每章 (1-56): `chapter_known` = 1 到 N-1 章累计已知词")
    out.append("   - `cov(N) = len(unique_latin ∩ chapter_known) / unique_latin_count`")
    out.append("   - 找最早达到 60% / 40% / 20% 的章节 → 分配 4 档可读性")
    out.append("   - `best_teach_chapter` = `len(new_set ∩ unique_latin) / len(new_set)` 最大的章节")
    out.append("")
    out.append("### 4.2 D 类拉语段提取 (v2)")
    out.append("")
    out.append("**脚本**: `scripts/extract_d_class_latin.py` + `scripts/analyze_d_class_latin_v2.py`")
    out.append("")
    out.append("**算法**:")
    out.append("1. 对每页 OCR 文本判定语言 (拉/英/混合)")
    out.append("2. 找连续 3+ 页的拉语/混合段, 标记为可入库故事段")
    out.append("3. 对每段单独做词频 + 章节锚点分析")
    out.append("")
    out.append("### 4.3 Ecce Romani EPUB 评估")
    out.append("")
    out.append("**脚本**: `scripts/compare_ecce_formats.py` + `scripts/ocr_new_ecce_romani.py`")
    out.append("")
    out.append("**结论**:")
    out.append("- Ecce Romani I&II Combined EPUB 含 14 个文本文件 (420KB) + 104 张图片 (1.6MB)")
    out.append("- 14 个文本文件中, 仅 3 个超过 500 字节阈值 (含实质内容)")
    out.append("- 提取出的 3 个文件 = 3 章, **仅覆盖原书前 3 章**, 不实用")
    out.append("- **决策**: 丢弃 combined EPUB, 使用 PDF 版本 (I + IIA + IIB + III)")
    out.append("")
    out.append("### 4.4 数据流")
    out.append("")
    out.append("```")
    out.append("source/Other_Readers/  (PDF + EPUB)")
    out.append("    ↓ [batch_ocr_readers.py / ocr_new_ecce_romani.py]")
    out.append("ocr_output/<slug>/_full.txt + page_NNN.txt  (55 本 × ~250 页)")
    out.append("    ↓ [analyze_readers_v5.py]")
    out.append("analysis_output/reader_vocab_stats_v4.json  (55 本, 含 4 档可读性)")
    out.append("    ↓ [extract_d_class_latin.py]")
    out.append("analysis_output/d_class_latin_stories.json  (16 本 D 类, 35 段, 162 页)")
    out.append("    ↓ [analyze_d_class_latin_v2.py]")
    out.append("analysis_output/d_segments_vocab.json  (35 段 + LLPSI 章节锚点)")
    out.append("    ↓ [restructure_reclassified.py]")
    out.append("source/Other_Readers/reclassified_v2/  (按学习阶段分章)")
    out.append("    ↓ [generate_audit_report_v4.py] (本脚本)")
    out.append("docs/reader_audit_report.md  (报告)")
    out.append("```")
    out.append("")
    out.append("---")
    out.append("")

    # 5. 附录
    out.append("## 5. 附录")
    out.append("")
    out.append("### 5.1 版本历史")
    out.append("")
    out.append("| 版本 | 日期 | 主要变化 |")
    out.append("|------|------|---------|")
    out.append("| v1 | 2026-05 | 首次批量审计, A1/A2/B1/B2 评级 |")
    out.append("| v2 | 2026-06-05 | 加入 OCR 词频统计 |")
    out.append("| v3 | 2026-06-06 | 引入 LLPSI 章节锚点, D 类拉语段提取, 加入 conversational_latin |")
    out.append("| **v4** | **2026-06-06** | **完全重写: 抛弃 A1/A2 标签, 改用「可读起点+教学价值」+ 4 档可读性, 按学习阶段分章** |")
    out.append("")
    out.append("### 5.2 关键变更 (v3 → v4)")
    out.append("")
    out.append("| 维度 | v3 | v4 | 变更原因 |")
    out.append("|------|----|----|---------|")
    out.append("| 难度标签 | A1/A2/B1/B2 | **拉词量 + LLPSI 章节** | 用户要求抛弃 CEFR |")
    out.append("| 目录结构 | `A1_latin_story/` 等 9 个 | `0_cap1-15_入门/` 等 6 个 | 按学习阶段而非等级 |")
    out.append("| 可读性 | 二元 (可读/不可读) | **4 档 fluent/challenging/selected/reference** | 解决\"很多书不可达\"问题 |")
    out.append("| 评级算法 | 仅 50%/60% 阈值 | **60%/40%/20% 三档阈值** | 39 本书达到 selected 档 |")
    out.append("| D 类段 | 仅 16 本, 无章节分析 | **35 段, 每段都有 LLPSI 章节锚点** | 用户要求\"D 类段也做章节分析\" |")
    out.append("| Ecce Romani | 3 本新加, EPUB 评估后丢弃 | 保留, 增加 `ecce_romani_2a/2b/3` | 用户新加 3 本 |")
    out.append("| conversational_latin | D 类\"重新入库\" | **selected 档, 起点 Cap.48, 教学 Cap.4 (43%)** | 用户要求重新入库 |")
    out.append("")

    out.append("### 5.3 物理删除 / 丢弃项")
    out.append("")
    out.append("| 项 | 处理 | 原因 |")
    out.append("|----|------|------|")
    out.append("| `nunc_loquamur` | 已物理删除 (用户操作) | 质量不高 |")
    out.append("| `ecce_romani_combined` (EPUB) | OCR 输出保留但不入库 | EPUB 仅 3 章, 不实用 |")
    out.append("| D 类 17 本 (含 5 本 D 类中无可提取段) | 归入 `5_reference_查阅` (暂空) | 拉语含量低, 仅作字典 |")
    out.append("")

    out.append("### 5.4 关键文件索引")
    out.append("")
    out.append("| 文件 | 用途 |")
    out.append("|------|------|")
    out.append("| `docs/reader_audit_report.md` | **本报告** |")
    out.append("| `analysis_output/reader_vocab_stats_v4.json` | 55 本书的 v5 详细数据 (4 档可读性) |")
    out.append("| `analysis_output/reader_vocab_stats_v4.md` | v5 词频数据 Markdown 视图 |")
    out.append("| `analysis_output/d_segments_vocab.json` | 35 个 D 类拉语段详细数据 |")
    out.append("| `analysis_output/d_segments_vocab.md` | D 类拉语段 Markdown 视图 |")
    out.append("| `analysis_output/d_class_latin_stories.json` | 16 本 D 类的拉语段位置 (start_page..end_page) |")
    out.append("| `source/Other_Readers/reclassified_v2/README.md` | 新目录结构说明 |")
    out.append("| `scripts/analyze_readers_v5.py` | v5 词频分析 (含 4 档) |")
    out.append("| `scripts/extract_d_class_latin.py` | D 类拉语段位置提取 |")
    out.append("| `scripts/analyze_d_class_latin_v2.py` | D 类拉语段章节锚点分析 |")
    out.append("| `scripts/restructure_reclassified.py` | 重命名 reclassified 目录 |")
    out.append("| `scripts/compare_ecce_formats.py` | Ecce Romani PDF vs EPUB 对比 |")
    out.append("")

    # Write
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[OK] {OUT} 已生成 ({len(data)} 本 + {d_segs['total_segments']} 段)")
    return 0


def _level_meaning(level: str) -> str:
    return {
        "fluent": "完成LLPSI主线后的奖励读物, 可通读",
        "challenging": "需配合注释, 适合复习扩展",
        "selected": "仅适合节选/对照阅读, 不通读",
        "reference": "词汇/语法查阅, 拉语含量低",
    }.get(level, "—")


if __name__ == "__main__":
    import sys
    sys.exit(main())
