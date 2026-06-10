#!/usr/bin/env python3
"""
build_reader_routing.py — 为 LLPSI 56章每章生成扩展读物路由表

对每章, 列出 4 个维度的扩展读物:
  🎯 奖励 (fluent, 学完本章后该书流畅可读)
  💪 挑战 (challenging, 学完本章后该书可挑战阅读)
  📖 复习 (best_teach_chapter = 本章, 该书适合复习本章新词)
  🧩 段   (D类拉语段, starting/teach chapter = 本章)

输入:
  - analysis_output/llpsi_chapter_stats.json
  - analysis_output/reader_vocab_stats_v4.json
  - analysis_output/d_segments_vocab.json

输出:
  - analysis_output/llpsi_reader_routing.json
  - analysis_output/llpsi_reader_routing.md
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
CHAPTER_STATS = ROOT / "analysis_output" / "llpsi_chapter_stats.json"
READERS = ROOT / "analysis_output" / "reader_vocab_stats_v4.json"
D_SEGS = ROOT / "analysis_output" / "d_segments_vocab.json"
OUT_JSON = ROOT / "analysis_output" / "llpsi_reader_routing.json"
OUT_MD = ROOT / "analysis_output" / "llpsi_reader_routing.md"

# 标题库
TITLES = {
    "pugio_bruti": "Pugio Bruti (Polis)",
    "via_latina_romanorum": "Via Latina: De Lingua et Vita Romanorum",
    "dooge_beginners_key": "D'Ooge Latin for Beginners Key",
    "diocles_flora": "Dioclēs et Flōra (Polis)",
    "regulus": "Regulus (Saint-Exupéry 拉语版)",
    "chickering": "First Latin Reader (Chickering)",
    "latin_lower_forms": "Latin Reader for Lower Forms (Hardy 1889)",
    "hobbitus": "Hobbitus Ille (Tolkien 拉语版)",
    "forum_lectiones": "Forum - Lectiones Latinitatis Vivae (Polis)",
    "conversational_latin": "Conversational Latin for Oral Proficiency",
    "intermediate_oral_cicero": "Intermediate Oral Latin Reader",
    "fabulae_faciles": "Fabulae Faciles (Ritchie 1889)",
    "nutting_reader": "A First Latin Reader (Nutting)",
    "reynolds_reader": "Latin Reader (Reynolds)",
    "via_latina_easy": "Via Latina: Easy Latin Reader (Collar 1897)",
    "septimus": "Septimus (Chambers 1910)",
    "olimpia_daedalus": "Daedalus et Icarus (Olimpi)",
    "olimpia_nichorus": "The Mysterious Traveler (Olimpi)",
    "olimpia_pyramus": "Reckless Love: Pyramus and Thisbe (Olimpi)",
    "ora_maritima": "Ora Maritima (Sonnenschein 1900)",
    "pro_patria": "Pro Patria (Sonnenschein 1907)",
    "unus_duo_tres": "Unus Duo Tres",
    "second_year_latin": "Second Year Latin (Greenough 1899)",
    "cambridge_1": "Cambridge Latin Course 1",
    "cambridge_2": "Cambridge Latin Course 2",
    "cambridge_3": "Cambridge Latin Course 3",
    "cambridge_4": "Cambridge Latin Course 4",
    "oxford_1": "Oxford Latin Course Part 1, 2e",
    "oxford_2": "Oxford Latin Course Part 2, 2e",
    "oxford_3": "Oxford Latin Course Part 3, 2e",
    "ecce_romani": "Ecce Romani I",
    "ecce_romani_2a": "Ecce Romani IIA",
    "ecce_romani_2b": "Ecce Romani IIB",
    "ecce_romani_3": "Ecce Romani III",
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
    "olimpia_nicholas": "The Mysterious Traveler (Olimpi)",
}


def title_of(slug: str) -> str:
    return TITLES.get(slug, slug)


def main() -> int:
    print("=== 生成 LLPSI 56章扩展读物路由表 ===")

    chap_data = json.loads(CHAPTER_STATS.read_text(encoding="utf-8"))
    fr_chaps = chap_data["fr_35_chapters"]
    ra_chaps = chap_data["ra_21_chapters"]
    all_chaps = fr_chaps + ra_chaps

    readers = json.loads(READERS.read_text(encoding="utf-8"))
    d_segs_data = json.loads(D_SEGS.read_text(encoding="utf-8"))
    d_segs = d_segs_data["segments"]

    def first_chapter_at_or_above(coverage_by_chapter: dict, threshold: float) -> int | None:
        """返回 coverage_by_chapter 中第一个 >= threshold 的章节 (1..56).
        若全程达不到, 返回 None.
        """
        for ch in range(1, 57):
            cov = coverage_by_chapter.get(str(ch))
            if cov is not None and cov >= threshold:
                return ch
        return None

    # 1) 为每章反向索引
    # 阈值 (v3.1 hybrid混合分):
    #   ch80: 可读 (readable)         — hybrid ≥ 80%
    #   ch70: 挑战 (challenging)      — hybrid ≥ 70%
    #   ch50: 节选 (selected)         — hybrid ≥ 50% (教材可50%起点)
    # idx_ch{N} -> [readers with starting_ch_token_{N} = ch]
    idx_ch = {80: defaultdict(list), 70: defaultdict(list),
              50: defaultdict(list)}
    idx_teach = defaultdict(list)
    idx_seg_ch60 = defaultdict(list)
    idx_seg_teach = defaultdict(list)

    for r in readers:
        if r["slug"] == "ecce_romani_combined":
            continue
        tok_cov = r.get("token_coverage_by_chapter") or {}
        for n in (80, 70, 50):
            ch_val = r.get(f"starting_ch_token_{n}")
            if ch_val is not None:
                idx_ch[n][ch_val].append(r)
        teach = r.get("best_teach_chapter")
        if teach is not None:
            idx_teach[teach].append(r)

    for seg in d_segs:
        # 段数据暂用原有 form 级 coverage_by_chapter (后续单独升级)
        cov_map = seg.get("coverage_by_chapter") or {}
        ch60 = seg.get("starting_chapter_60") or first_chapter_at_or_above(cov_map, 0.60)
        seg["starting_chapter_60_filtered"] = ch60
        if ch60:
            idx_seg_ch60[ch60].append(seg)
        teach = seg.get("best_teach_chapter")
        if teach:
            idx_seg_teach[teach].append(seg)

    # 对每章生成路由
    routing = []
    for ch_data in all_chaps:
        ch = ch_data["chapter"]
        book = ch_data["book"]
        title = ch_data.get("title_roman", str(ch))

        # 1) 可读 (readable, ch80 token == 本章, token 覆盖 ≥ 80%)
        readable = [r for r in idx_ch[80].get(ch, [])
                    if r.get("verdict") in ("readable", "fluent")]

        # 2) 挑战 (challenging, ch70 token == 本章)
        challenges = [r for r in idx_ch[70].get(ch, [])
                      if r.get("verdict") in ("challenging", "readable", "fluent")]
        challenges = [r for r in challenges if r not in readable]

        # 3) 节选 (selected, ch50 token == 本章)
        selected = [r for r in idx_ch[50].get(ch, [])]
        selected = [r for r in selected
                    if r not in readable and r not in challenges]

        # 4) 复习 (best_teach == 本章, 不变)
        reviews = idx_teach.get(ch, [])

        # 5) 段 (不变)
        segs_60 = idx_seg_ch60.get(ch, [])
        segs_teach = idx_seg_teach.get(ch, [])
        segments = []
        seg_seen = set()
        for s in segs_60 + segs_teach:
            key = (s["slug"], s["start_page"], s["end_page"])
            if key not in seg_seen:
                seg_seen.add(key)
                segments.append(s)

        # 排序
        readable.sort(key=lambda r: -r.get("unique_latin_count", 0))
        challenges.sort(key=lambda r: -r.get("unique_latin_count", 0))
        selected.sort(key=lambda r: -r.get("unique_latin_count", 0))
        reviews.sort(key=lambda r: -r.get("best_teach_coverage", 0))
        segments.sort(key=lambda s: -s.get("page_count", 0))

        # 简化输出
        def compact_reader(r: dict) -> dict:
            return {
                "slug": r["slug"],
                "title": title_of(r["slug"]),
                "verdict": r.get("verdict"),
                "t50": r.get("starting_ch_token_50"),
                "t60": r.get("starting_ch_token_60"),
                "t70": r.get("starting_ch_token_70"),
                "t75": r.get("starting_ch_token_75"),
                "t80": r.get("starting_ch_token_80"),
                "t85": r.get("starting_ch_token_85"),
                "t90": r.get("starting_ch_token_90"),
                "pkH": r.get("peak_hybrid_coverage"),
                "pkT": r.get("peak_token_coverage"),
                "pkF": r.get("peak_form_coverage"),
                "teach_ch": r.get("best_teach_chapter"),
                "teach_cov": r.get("best_teach_coverage"),
                "latin_tokens": r.get("latin_token_count"),
                "unique_latin": r.get("unique_latin_count"),
                "english_ratio": r.get("english_ratio"),
            }

        def compact_seg(s: dict) -> dict:
            return {
                "slug": s["slug"],
                "title": title_of(s["slug"]),
                "start_page": s["start_page"],
                "end_page": s["end_page"],
                "page_count": s["page_count"],
                "ch50": s.get("starting_chapter_50"),
                "ch60": s.get("starting_chapter_60") or s.get("starting_chapter_60_filtered"),
                "teach_ch": s.get("best_teach_chapter"),
                "teach_cov": s.get("best_teach_coverage"),
                "latin_words": s.get("latin_word_count"),
                "unique_latin": s.get("unique_latin_count"),
            }

        routing.append({
            "chapter": ch,
            "book": book,
            "title_roman": title,
            "chapter_data": {
                "new_word_count": ch_data.get("new_word_count_csv"),
                "new_density": ch_data.get("new_density_csv"),
                "cumulative_vocab_db": ch_data.get("cumulative_vocab_db"),
                "cumulative_vocab_csv": ch_data.get("cumulative_vocab_csv"),
            },
            "readable": [compact_reader(r) for r in readable],
            "challenges": [compact_reader(r) for r in challenges],
            "selected": [compact_reader(r) for r in selected],
            "reviews": [compact_reader(r) for r in reviews],
            "segments": [compact_seg(s) for s in segments],
        })

    # 输出
    out = {
        "total_chapters": len(routing),
        "total_recommendations": sum(
            len(r["readable"]) + len(r["challenges"]) + len(r["selected"]) +
            len(r["reviews"]) + len(r["segments"])
            for r in routing
        ),
        "routing": routing,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUT_JSON}")
    print(f"     总计: 56章 × 5维度 = {out['total_recommendations']} 条推荐")

    # Markdown
    lines = [
        "# LLPSI 56 章扩展读物路由表",
        "",
        "**生成日期**: 2026-06-08 | **覆盖**: FR Cap.1-35 + RA Cap.36-56",
        "",
        "## 路由规范 (5个维度, v3.1 hybrid混合分)",
        "",
        "| 标签 | 维度 | 含义 | hybrid 阈值 | 起点判定 |",
        "|------|------|------|-------------|----------|",
        "| 📖 可读 | readable (可读) | 学完本章后 hybrid ≥ 80% | **≥ 80%** | `starting_ch_token_80 = 本章` |",
        "| 💪 挑战 | challenging (挑战可读) | 学完本章后 hybrid ≥ 70% | **≥ 70%** | `starting_ch_token_70 = 本章` |",
        "| 📚 节选 | selected (片段可读) | 学完本章后 hybrid ≥ 50% | **≥ 50%** | `starting_ch_token_50 = 本章` |",
        "| 📖 复习 | best_teach (复习价值) | 本书覆盖本章新词最多 | 教学 | `best_teach_chapter = 本章` |",
        "| 🧩 段 | D类拉语段 | 本章对应可抽取的拉语故事段 | **≥ 60% form** | `seg.starting_ch60 = 本章` |",
        "",
        "**v3.1 关键**: 使用 **hybrid 混合分** (LLPSI直接匹配 ×1.0 + LLPSI总表但未学到 ×0.5).",
        "教材型读物(剑桥/牛津/ECCE)中大量拉丁词虽不在 LLPSI Cap.1-5 词表，但在 LLPSI 的总词表中，",
        "给予 0.5 权重后教材评级显著提升。",
        "",
    ]

    for r in routing:
        ch = r["chapter"]
        book = r["book"]
        title = r["title_roman"]
        cdata = r["chapter_data"]
        nw = cdata.get("new_word_count", "?")
        nd = cdata.get("new_density", "?")
        cv_db = cdata.get("cumulative_vocab_db", "?")
        cv_csv = cdata.get("cumulative_vocab_csv", "?")
        lines.append(f"## Cap.{ch} ({book} Cap.{title})")
        lines.append("")
        lines.append(f"**章节数据**: 新词 {nw} / 新词密度 {nd}% / "
                     f"累计 {cv_db} 词形 ({cv_csv} 词族)")
        lines.append("")

        if r["readable"]:
            lines.append(f"### 📖 可读读物 ({len(r['readable'])})")
            for x in r["readable"]:
                lines.append(
                    f"- `{x['slug']}` ({x['title']}): {x['verdict']}, "
                    f"t80 Cap.{x['t80']}, pkH={x['pkH']:.0%}, "
                    f"教学 Cap.{x['teach_ch']}({x['teach_cov']:.0%}), "
                    f"{x['unique_latin']:,}独词"
                )
            lines.append("")

        if r["challenges"]:
            lines.append(f"### 💪 挑战读物 ({len(r['challenges'])})")
            for x in r["challenges"]:
                lines.append(
                    f"- `{x['slug']}` ({x['title']}): {x['verdict']}, "
                    f"t70 Cap.{x['t70']}, pkH={x['pkH']:.0%}, "
                    f"教学 Cap.{x['teach_ch']}({x['teach_cov']:.0%}), "
                    f"{x['unique_latin']:,}独词"
                )
            lines.append("")

        if r["selected"]:
            lines.append(f"### 📚 节选读物 ({len(r['selected'])})")
            for x in r["selected"][:5]:
                lines.append(
                    f"- `{x['slug']}` ({x['title']}): {x['verdict']}, "
                    f"h50 Cap.{x['t50']}, pkH={x['pkH']:.0%}, "
                    f"教学 Cap.{x['teach_ch']}({x['teach_cov']:.0%}), "
                    f"{x['unique_latin']:,}独词"
                )
            if len(r["selected"]) > 5:
                lines.append(f"- ... ({len(r['selected']) - 5} 本省略)")
            lines.append("")

        if r["reviews"]:
            lines.append(f"### 📖 复习读物 ({len(r['reviews'])})")
            for x in r["reviews"][:3]:
                lines.append(
                    f"- `{x['slug']}` ({x['title']}): "
                    f"教学 Cap.{x['teach_ch']}({x['teach_cov']:.0%}), "
                    f"pkT={x['pkT']:.0%}, "
                    f"{x['unique_latin']:,}独词"
                )
            if len(r["reviews"]) > 3:
                lines.append(f"- ... ({len(r['reviews']) - 3} 本省略)")
            lines.append("")

        if r["segments"]:
            lines.append(f"### 🧩 拉语段 ({len(r['segments'])})")
            for x in r["segments"][:3]:
                lines.append(
                    f"- `{x['slug']}` p.{x['start_page']}-{x['end_page']} ({x['page_count']}页): "
                    f"60%起点 Cap.{x['ch60'] or '—'}, 教学 Cap.{x['teach_ch']}({x['teach_cov']:.0%}), "
                    f"{x['unique_latin']:,}独词"
                )
            if len(r["segments"]) > 3:
                lines.append(f"- ... ({len(r['segments']) - 3} 段省略)")
            lines.append("")
        else:
            lines.append("_(本章无D类拉语段推荐)_")
            lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {OUT_MD}")

    # 统计
    counts = {
        "readable": sum(len(r["readable"]) for r in routing),
        "challenges": sum(len(r["challenges"]) for r in routing),
        "selected": sum(len(r["selected"]) for r in routing),
        "reviews": sum(len(r["reviews"]) for r in routing),
        "segments": sum(len(r["segments"]) for r in routing),
    }
    print()
    print("各维度推荐数 (v3.0 token级):")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
