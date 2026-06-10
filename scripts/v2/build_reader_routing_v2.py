"""build_reader_routing_v2.py - 阶段4：基于段级分析的路由表生成 (v3 算法)

v3 关键改进 (2026-06-09):
1. 排序键: score*log(tokens+1) 而非 token 数 (兼顾分数与长度)
2. 词数硬限制:
   - 流畅 (80%): 拉语 token 数 >= 15
   - 挑战 (70%): 拉语 token 数 >= 20
   - 节选 (50%): 拉语 token 数 >= 30
3. 复用 analyze_readers_v6.py v3 输出的 s80/s70/s50 字段

输入: analysis_output/reader_vocab_stats_v6.json
输出: analysis_output/llpsi_reader_routing_v2.json + .md
"""
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
CHAPTER_STATS = ROOT / "analysis_output" / "llpsi_chapter_stats.json"
READERS = ROOT / "analysis_output" / "reader_vocab_stats_v6.json"
D_SEGS = ROOT / "analysis_output" / "d_segments_vocab.json"
OUT_JSON = ROOT / "analysis_output" / "llpsi_reader_routing_v2.json"
OUT_MD = ROOT / "analysis_output" / "llpsi_reader_routing_v2.md"

# 标题库（与v1相同）
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
    "epitome_historiae_sacrae": "Epitome Historiae Sacrae",
    "de_rerum_natura": "De Rerum Natura (Lucretius 拉语版)",
    "sermones_romani": "Sermones Romani (Menaechmi 选段)",
    "fabellae_latinae": "Fabellae Latinae",
    "fabulae_faciles": "Fabulae Faciles (Ritchie 1889)",
}


def title_of(slug):
    return TITLES.get(slug, slug)


def main():
    print("=== 生成 LLPSI 56章扩展读物路由表 (v2 段级版) ===")

    chap_data = json.loads(CHAPTER_STATS.read_text(encoding="utf-8"))
    fr_chaps = chap_data["fr_35_chapters"]
    ra_chaps = chap_data["ra_21_chapters"]
    all_chaps = fr_chaps + ra_chaps

    readers_data = json.loads(READERS.read_text(encoding="utf-8"))
    d_segs_data = json.loads(D_SEGS.read_text(encoding="utf-8"))
    d_segs = d_segs_data.get("segments", [])

    # === 建立段级反向索引 ===
    # 索引: idx_ch[threshold][chapter] = [段对象, ...]
    # 含义: 学完 chapter 后, 该段 first reaches threshold
    idx_ch = {80: defaultdict(list), 70: defaultdict(list), 50: defaultdict(list)}

    total_segs = 0
    for r in readers_data:
        slug = r["slug"]
        for seg in r["segments"]:
            for th in (80, 70, 50):
                ch = seg[f"t{th}"]
                if 1 <= ch <= 56:
                    idx_ch[th][ch].append({
                        "slug": slug,
                        "title": title_of(slug),
                        "seg_idx": seg["idx"],
                        "tokens": seg["tokens"],
                        # v3: 阈值首达章节处的实际分数 (由 analyze v3 输出)
                        "score": seg.get(f"s{th}", 0.0),
                        "preview": seg["preview"],
                        f"t{th}": ch,
                    })
            total_segs += 1

    # v3 词数硬限制 (确保推荐内容"完整可读", 避免碎片化)
    MIN_TOKENS = {80: 15, 70: 20, 50: 30}

    # v3 排序键: score * log(tokens+1) (兼顾分数与长度)
    def hybrid_key(s):
        return s["score"] * math.log(s["tokens"] + 1)

    print(f"段级索引建立: 总段数 {total_segs}")
    for th in (80, 70, 50):
        # 应用词数硬限制
        kept = sum(1 for ch_segs in idx_ch[th].values()
                   for s in ch_segs if s["tokens"] >= MIN_TOKENS[th])
        total = sum(len(idx_ch[th][ch]) for ch in range(1, 57))
        print(f"  t{th}: 总{total}条, 词数>={MIN_TOKENS[th]}保留 {kept}条")

    # D类段索引（保留原有）
    idx_seg_ch60 = defaultdict(list)
    for seg in d_segs:
        cov_map = seg.get("coverage_by_chapter") or {}
        ch60 = None
        for ch in range(1, 57):
            cov = cov_map.get(str(ch))
            if cov is not None and cov >= 0.60:
                ch60 = ch
                break
        if ch60:
            idx_seg_ch60[ch60].append(seg)

    # === 生成路由 ===
    routing = []
    for ch_data in all_chaps:
        ch = ch_data["chapter"]
        book = ch_data["book"]
        title = ch_data.get("title_roman", str(ch))

        # v3: 应用词数硬限制 + hybrid 分数排序
        # 流畅（80%）段: tokens >= 15
        fluent_pool = [s for s in idx_ch[80].get(ch, [])
                       if s["tokens"] >= MIN_TOKENS[80]]
        fluent = sorted(fluent_pool, key=hybrid_key, reverse=True)[:30]

        # 挑战（70%）段: tokens >= 20, 排除已入 fluent
        challenging_pool = [s for s in idx_ch[70].get(ch, [])
                            if s["tokens"] >= MIN_TOKENS[70]
                            and s not in fluent]
        challenging = sorted(challenging_pool, key=hybrid_key, reverse=True)[:30]

        # 节选（50%）段: tokens >= 30, 排除 fluent/challenging
        selected_pool = [s for s in idx_ch[50].get(ch, [])
                         if s["tokens"] >= MIN_TOKENS[50]
                         and s not in fluent and s not in challenging]
        selected = sorted(selected_pool, key=hybrid_key, reverse=True)[:30]

        # D类拉语段
        d_segs_for_ch = idx_seg_ch60.get(ch, [])
        d_compact = [{
            "slug": s["slug"],
            "title": title_of(s["slug"]),
            "start_page": s["start_page"],
            "end_page": s["end_page"],
            "page_count": s["page_count"],
        } for s in d_segs_for_ch[:10]]

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
            "fluent_segments": fluent,
            "challenging_segments": challenging,
            "selected_segments": selected,
            "d_segments": d_compact,
            "counts": {
                "fluent": len(fluent),
                "challenging": len(challenging),
                "selected": len(selected),
                "d_segments": len(d_compact),
            },
        })

    # 输出
    out = {
        "version": "v3-hybrid-min-tokens",
        "total_chapters": len(routing),
        "routing": routing,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] {OUT_JSON}")

    # Markdown
    lines = [
        "# LLPSI 56 章扩展读物路由表 (v3 段级 hybrid 版)",
        "",
        "**生成日期**: 2026-06-09 | **覆盖**: FR Cap.1-35 + RA Cap.36-56",
        "",
        "## 算法 (v3 极简段级 hybrid)",
        "",
        "- **段级切片**: 按空行切分文本为段落",
        "- **叙事过滤**: 拉语词占比≥50%、**token≥15 (v3 新增)**、非标题/非练习题/非词汇表",
        "- **极简评分 (hybrid)**:",
        "  - `full = 1.0`: 在 LLPSI Cap.N 已学词集 `learned_words[N]` 中",
        "  - `partial = 0.5`: 在 LLPSI 56章总词表但未学到",
        "  - `character = 0.7`: 在本段所属书的高频专名(出现≥5次, v3 由 0.3 提升)",
        "  - `score = (full + 0.5*partial + 0.7*character) / total_latin_tokens`",
        "- **已学词集**: 直接扫描 LLPSI OCR 文本重建（而非依赖DB is_new标记）",
        "- **v3 排序键**: `score * log(tokens + 1)` (兼顾分数与长度, 取代纯 token 数)",
        "- **v3 词数硬限制** (确保推荐内容\"完整可读\"):",
        "  - 📖 流畅: 拉语 token ≥ **15**",
        "  - 💪 挑战: 拉语 token ≥ **20**",
        "  - 📚 节选: 拉语 token ≥ **30**",
        "",
        "## 路由规范 (4个维度)",
        "",
        "| 标签 | 含义 | 阈值 | 最小词数 |",
        "|------|------|------|----------|",
        "| 📖 流畅 | 学完本章后该段可流畅阅读 | hybrid ≥ 80% | 15 |",
        "| 💪 挑战 | 学完本章后该段可挑战阅读 | hybrid ≥ 70% | 20 |",
        "| 📚 节选 | 学完本章后该段可节选阅读 | hybrid ≥ 50% | 30 |",
        "| 🧩 D段  | D类拉语段 (OCR抽取) | form ≥ 60% | - |",
        "",
    ]

    for r in routing:
        ch = r["chapter"]
        book = r["book"]
        title = r["title_roman"]
        cdata = r["chapter_data"]
        nw = cdata.get("new_word_count", "?")
        cv = cdata.get("cumulative_vocab_csv", "?")
        cnts = r["counts"]
        lines.append(f"## Cap.{ch} ({book} Cap.{title})")
        lines.append("")
        lines.append(f"**数据**: 新词 {nw} / 累计 {cv} 词族 | "
                     f"📖流畅 {cnts['fluent']} | 💪挑战 {cnts['challenging']} | "
                     f"📚节选 {cnts['selected']} | 🧩D段 {cnts['d_segments']}")
        lines.append("")

        # 流畅段示例
        if r["fluent_segments"]:
            lines.append("### 📖 流畅 (hybrid ≥ 80%)")
            for s in r["fluent_segments"][:5]:
                lines.append(f"- **{s['title']}** #{s['seg_idx']} (tokens={s['tokens']}): "
                             f"`{s['preview'][:80]}`")
            if len(r["fluent_segments"]) > 5:
                lines.append(f"- *...还有 {len(r['fluent_segments']) - 5} 段*")
            lines.append("")

        # 挑战段示例
        if r["challenging_segments"]:
            lines.append("### 💪 挑战 (hybrid ≥ 70%)")
            for s in r["challenging_segments"][:5]:
                lines.append(f"- **{s['title']}** #{s['seg_idx']} (tokens={s['tokens']}): "
                             f"`{s['preview'][:80]}`")
            if len(r["challenging_segments"]) > 5:
                lines.append(f"- *...还有 {len(r['challenging_segments']) - 5} 段*")
            lines.append("")

    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')
    print(f"[OK] {OUT_MD}")


if __name__ == '__main__':
    main()
