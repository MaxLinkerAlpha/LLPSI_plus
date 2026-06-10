#!/usr/bin/env python3
"""
generate_insertion_guide.py — 生成「读者章节→主教材章节」插入推荐指南
===================================================================

产出: analysis_output/reader_insertion_guide.md

三部分:
  1. 设计级精确映射 (Colloquia Personarum, Fabulae Syrae, Fabellae Latinae, Roma Aeterna)
  2. 算法匹配推荐 (9 本 fr_chapter=NULL 的读物, 逐章匹配)
  3. 覆盖缺口 (无设计级映射 + 算法新词命中 < 20%)

用法:
    python3 scripts/generate_insertion_guide.py
"""

import os
import re
import sqlite3
import sys
from collections import defaultdict

# 将 scripts/ 加入 sys.path, 以便导入 match_segments 和 vocab_overlap
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

import match_segments
import vocab_overlap

# ============================================================
# 配置
# ============================================================
DEFAULT_DB = "data/llpsi_corpus.db"
OUTPUT_MD = "analysis_output/reader_insertion_guide.md"

# 算法匹配读物 (fr_chapter=NULL)
# 注意: famila_romana 不在 DB segments 中 (它是教材)
ALGO_BOOKS = [
    "aeneis", "amphitryo", "ars_amatoria", "catilina",
    "cena_trimalchionis", "de_bello_gallico", "de_rerum_natura",
    "epitome_historiae_sacrae", "sermones_romani",
]


# ============================================================
# 辅助函数
# ============================================================
def get_db_path() -> str:
    db_path = os.path.join(PROJECT_DIR, DEFAULT_DB)
    if not os.path.exists(db_path):
        print(f"  [错误] 数据库不存在: {db_path}", file=sys.stderr)
        sys.exit(1)
    return db_path


def roman_to_int(roman: str) -> int:
    """将罗马数字转换为阿拉伯数字 (I → 1, XXV → 25).

    容错: OCR 经常将 'I' 误识别为 'T', 此处将 'T' 视为 'I'.
    """
    roman = roman.strip().upper().replace('T', 'I')
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(roman):
        v = values.get(ch, 0)
        if v >= prev:
            total += v
        else:
            total -= v
        prev = v
    return total


def parse_fabellae_cap_ranges(full_text_path: str) -> dict[int, tuple[int, int]]:
    """从 Fabellae Latinae _full.txt 的目录页解析每段的 cap 适配范围.

    Returns:
        {sequence: (min_cap, max_cap)}  例如 {1: (1, 1), 2: (1, 2), ...}
    """
    ranges: dict[int, tuple[int, int]] = {}

    # 目录页在 PAGE 2, 格式如:
    #   1. Provinciae Romanae (cap. I)
    #   2. Liberi et libri (cap. I-II)
    #   ...
    with open(full_text_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    # 匹配模式: 数字序号. 故事名 (cap. I-VII) 或 (I-XII)
    # 注意: OCR 可能有瑕疵, 如 "cap. I-VIIT" (OCR 将 'I' 误识别为 'T')
    # 正则中 [IVXLCT] 接受 T 以容错 OCR
    pattern = re.compile(
        r'^\s*(\d{1,2})[.\)]?\s*.*?\(?(?:cap\.\s*)?([IVXLCT]+)(?:\s*-\s*([IVXLCT]+))?\)',
        re.MULTILINE | re.IGNORECASE
    )

    for m in pattern.finditer(text):
        seq = int(m.group(1))
        roman_start = m.group(2)
        roman_end = m.group(3)
        min_cap = roman_to_int(roman_start)
        max_cap = roman_to_int(roman_end) if roman_end else min_cap
        # 只保留首次匹配（目录页在正文之前, 目录版本更准确）
        # 正文中的 OCR 可能有额外空格导致错误匹配 (如 "I-X X" 匹配为 "X")
        if seq not in ranges:
            ranges[seq] = (min_cap, max_cap)

    return ranges


# ============================================================
# Part 1: 设计级精确映射
# ============================================================
def build_design_mappings(db_path: str) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """从 DB 读取设计级映射数据.

    Returns:
        (colloquia_mappings, fabulae_syrae_mappings, fabellae_mappings, ra_mappings)
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # --- Colloquia Personarum: fr_chapter 1-24 ---
    cur.execute("""
        SELECT s.sequence, s.title, s.word_count, s.fr_chapter
        FROM segments s JOIN books b ON s.book_id = b.id
        WHERE b.slug = 'colloquia_personarum'
        ORDER BY s.fr_chapter, s.sequence
    """)
    colloquia = []
    for seq, title, wc, fr_ch in cur.fetchall():
        colloquia.append({
            "sequence": seq, "title": title, "word_count": wc, "fr_chapter": fr_ch,
        })

    # --- Fabulae Syrae: fr_chapter 26-34 ---
    cur.execute("""
        SELECT s.sequence, s.title, s.word_count, s.fr_chapter
        FROM segments s JOIN books b ON s.book_id = b.id
        WHERE b.slug = 'fabulae_syrae'
        ORDER BY s.fr_chapter, s.sequence
    """)
    fabulae_syrae = []
    for seq, title, wc, fr_ch in cur.fetchall():
        fabulae_syrae.append({
            "sequence": seq, "title": title, "word_count": wc, "fr_chapter": fr_ch,
        })

    # --- Roma Aeterna: fr_chapter 36-56 ---
    cur.execute("""
        SELECT s.sequence, s.title, s.word_count, s.fr_chapter
        FROM segments s JOIN books b ON s.book_id = b.id
        WHERE b.slug = 'roma_aeterna'
        ORDER BY s.fr_chapter
    """)
    ra_mappings = []
    for seq, title, wc, fr_ch in cur.fetchall():
        ra_mappings.append({
            "sequence": seq, "title": title, "word_count": wc, "fr_chapter": fr_ch,
        })

    # --- Fabellae Latinae: 从 _full.txt 解析 cap 范围 ---
    fl_full_path = os.path.join(PROJECT_DIR, "ocr_output", "fabellae_latinae", "_full.txt")
    cap_ranges = parse_fabellae_cap_ranges(fl_full_path)

    cur.execute("""
        SELECT s.sequence, s.title, s.word_count
        FROM segments s JOIN books b ON s.book_id = b.id
        WHERE b.slug = 'fabellae_latinae'
        ORDER BY s.sequence
    """)
    fabellae = []
    for seq, title, wc in cur.fetchall():
        cr = cap_ranges.get(seq, (1, 1))
        fabellae.append({
            "sequence": seq, "title": title, "word_count": wc,
            "cap_min": cr[0], "cap_max": cr[1],
        })

    conn.close()
    return colloquia, fabulae_syrae, fabellae, ra_mappings


# ============================================================
# Part 2: 算法匹配推荐
# ============================================================
def build_algo_recommendations(db_path: str) -> list[dict]:
    """对 fr_chapter=NULL 的 9 本读物, 对 56 章逐一跑匹配, 每章取 top-1.

    核心指标说明:
    - new_hit: 段中命中目标新词的 distinct word forms 数 (不是 token 计数)
    - new_cov: new_hit / len(new_words), 即有多少比例的新词在段中出现过
    - score: match_segments 综合评分 (含 token 级加权, 用于排序)

    Returns:
        [{chapter: int, slug: str, title: str, seg_title: str,
          new_hit: int, new_total: int, new_cov: float, score: float, ...}, ...]
    """
    conn = sqlite3.connect(db_path)
    fr_vocab = vocab_overlap.load_fr_vocab(db_path)
    all_chapters = sorted(fr_vocab.keys())

    results = []

    # 为每章运行匹配
    for ch in all_chapters:
        known, new_words = match_segments.load_chapter_vocab(db_path, ch)
        if not new_words:
            continue

        # 加载所有 fr_chapter=NULL 的段
        candidates = []
        for slug in ALGO_BOOKS:
            segs = match_segments.load_candidate_segments(db_path, book_slug=slug)
            # 只保留 fr_chapter IS NULL 的段
            segs = [s for s in segs if s["fr_chapter"] is None]
            candidates.extend(segs)

        if not candidates:
            continue

        # 打分 (使用 match_segments 默认权重), 同时统计 distinct new word forms
        scored = []
        for seg in candidates:
            seg_words = match_segments.load_segment_vocab(db_path, seg["id"])
            sc = match_segments.score_segment(
                seg_words, known, new_words,
                w1=0.4, w2=0.4, w3=0.2, w4=0.2
            )
            # distinct new word forms: 段中出现了多少种 distinct 新词
            distinct_new_hits = len(set(seg_words.keys()) & new_words)
            scored.append({
                "seg": seg,
                "score": sc["score"],
                "known_cov": sc["known_cov"],
                "distinct_new_hits": distinct_new_hits,      # distinct word forms
                "token_new_hits": sc["new_hits"],             # token 计数 (展示用)
                "new_hits_norm": sc["new_hits_norm"],
                "new_den": sc["new_den"],
                "hf_new_hits": sc["hf_new_hits"],
            })

        # 排序取 top-1
        scored.sort(key=lambda x: x["score"], reverse=True)
        if scored:
            best = scored[0]
            s = best["seg"]
            results.append({
                "chapter": ch,
                "slug": s["book_slug"],
                "book_title": s["book_title"],
                "seg_title": s["title"],
                "word_count": s["word_count"],
                "score": best["score"],
                "new_hit": best["distinct_new_hits"],
                "new_total": len(new_words),
                "new_cov": best["distinct_new_hits"] / max(1, len(new_words)),
                "known_cov": best["known_cov"],
                "new_den": best["new_den"],
                "hf_new_hits": best["hf_new_hits"],
            })

    conn.close()
    return results


# ============================================================
# Part 3: 覆盖缺口
# ============================================================
def find_gaps(design_chapters: set[int], algo_results: list[dict]) -> list[dict]:
    """找出无设计级映射 + 算法新词命中 < 20% 的章节.

    Returns:
        [{chapter: int, highest_new_cov: float, best_slug: str, ...}, ...]
    """
    # 算法最高命中 (每章)
    algo_best: dict[int, dict] = {}
    for r in algo_results:
        ch = r["chapter"]
        if ch not in algo_best or r["new_cov"] > algo_best[ch]["new_cov"]:
            algo_best[ch] = r

    gaps = []
    for ch in range(1, 57):
        if ch in design_chapters:
            continue
        if ch in algo_best:
            best = algo_best[ch]
            if best["new_cov"] < 0.20:
                gaps.append({
                    "chapter": ch,
                    "highest_new_cov": best["new_cov"],
                    "best_slug": best["slug"],
                    "best_book_title": best["book_title"],
                    "best_new_hit": best["new_hit"],
                    "best_new_total": best["new_total"],
                })
        else:
            gaps.append({
                "chapter": ch,
                "highest_new_cov": 0.0,
                "best_slug": "N/A",
                "best_book_title": "N/A",
                "best_new_hit": 0,
                "best_new_total": 0,
            })

    return gaps


# ============================================================
# Markdown 报告生成
# ============================================================
def _int_to_roman(n: int) -> str:
    """将整数转换为罗马数字 (1 → I, 25 → XXV)."""
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman = ""
    for i in range(len(val)):
        count = n // val[i]
        roman += syms[i] * count
        n -= val[i] * count
    return roman


def _recommendation_label(new_cov: float) -> str:
    """根据新词命中率返回推荐标签."""
    if new_cov >= 0.30:
        return ":star: 强推荐"
    elif new_cov >= 0.10:
        return ":leftwards_arrow_with_hook: 弱推荐"
    elif new_cov > 0:
        return ":small_blue_diamond: 微推荐"
    else:
        return ":white_small_square: 无覆盖"


def generate_report(db_path: str) -> str:
    """生成完整 Markdown 报告."""
    L = []  # lines accumulator

    L.append("# LLPSI 扩展读物插入推荐指南")
    L.append("")
    L.append("> 本指南为 Familia Romana (Cap. 1-35) 和 Roma Aeterna (Cap. 36-56) 共 56 章教材")
    L.append("> 提供扩展读物的插入建议。分为三部分：设计级精确映射、算法匹配推荐、覆盖缺口。")
    L.append("")
    L.append("**生成日期**: 2026-06-06 | **数据源**: `data/llpsi_corpus.db`")
    L.append("")

    # ---- Part 1 ----
    L.append("---")
    L.append("")
    L.append("## 第一部分：设计级精确映射")
    L.append("")
    L.append("以下四本读物与主教材有明确的章节对应关系，由作者/编者设计。")
    L.append("")

    # 加载数据
    colloquia, fabulae_syrae, fabellae, ra_mappings = build_design_mappings(db_path)

    # ----- Colloquia Personarum -----
    L.append("### Colloquia Personarum (Cap. 1-24)")
    L.append("")
    L.append("Colloquia Personarum 是 Familia Romana 的官方配套对话读物。")
    L.append("每个 Colloquium 精确对应 FR 的一个章节 (Colloquium N = FR Cap. N)。")
    L.append("")
    L.append("| FR 章节 | Colloquium 标题 | 词数 |")
    L.append("|:-------:|:----------------|-----:|")

    # 按 fr_chapter 聚合
    cp_by_ch: dict[int, list[dict]] = defaultdict(list)
    for c in colloquia:
        cp_by_ch[c["fr_chapter"]].append(c)

    for ch in sorted(cp_by_ch.keys()):
        items = cp_by_ch[ch]
        for i, item in enumerate(items):
            if i == 0:
                L.append(f"| Cap. {ch} | {item['title']} | {item['word_count']:,} |")
            else:
                L.append(f"|  | {item['title']} | {item['word_count']:,} |")

    # 快速概览
    total_cp_segs = len(colloquia)
    total_cp_words = sum(c["word_count"] for c in colloquia)
    L.append("")
    L.append(f"> 共 {total_cp_segs} 个 Colloquium, 总词数 {total_cp_words:,}。")
    L.append("")

    # ----- Fabulae Syrae -----
    L.append("### Fabulae Syrae (Cap. 26-34)")
    L.append("")
    L.append("Fabulae Syrae 是 Luigi Miraglia 编写的希腊罗马神话扩展读物，")
    L.append("原文中以 `AD CAPITVLVM XXVI` 等标记明确指示对应 FR 章节。")
    L.append("")

    # 按 fr_chapter 聚合
    fs_by_ch: dict[int, list[dict]] = defaultdict(list)
    for fs in fabulae_syrae:
        fs_by_ch[fs["fr_chapter"]].append(fs)

    L.append("| FR 章节 | Fabulae Syrae 标题 | 词数 |")
    L.append("|:-------:|:-------------------|-----:|")
    for ch in sorted(fs_by_ch.keys()):
        items = fs_by_ch[ch]
        for i, item in enumerate(items):
            if i == 0:
                L.append(f"| Cap. {ch} | {item['title']} | {item['word_count']:,} |")
            else:
                L.append(f"|  | {item['title']} | {item['word_count']:,} |")

    total_fs_segs = len(fabulae_syrae)
    total_fs_words = sum(f["word_count"] for f in fabulae_syrae)
    L.append("")
    L.append(f"> 共 {total_fs_segs} 个神话故事, 总词数 {total_fs_words:,}。")
    L.append("")

    # ----- Fabellae Latinae -----
    L.append("### Fabellae Latinae (Cap. 1-25)")
    L.append("")
    L.append("Fabellae Latinae 是 30 个简短叙事故事，全部设计从 Cap. 1 起即可阅读，")
    L.append("但每个故事标注了其词汇对应的最大适配章号 (如 `cap. I-VII` 表示最多用到 Cap. 7 的词汇)。")
    L.append("读者可以学到对应章节后阅读该故事来巩固所学词汇。")
    L.append("")

    L.append("| 序号 | 故事标题 | 适配范围 | 最大适配章 | 词数 |")
    L.append("|:----:|:---------|:---------|:----------:|-----:|")
    for fl in fabellae:
        min_c = fl["cap_min"]
        max_c = fl["cap_max"]
        if min_c == max_c:
            cap_str = f"cap. {_int_to_roman(min_c)}"
        else:
            cap_str = f"cap. {_int_to_roman(min_c)}-{_int_to_roman(max_c)}"
        L.append(f"| {fl['sequence']} | {fl['title']} | {cap_str} | Cap. {max_c} | {fl['word_count']:,} |")

    total_fl_words = sum(f["word_count"] for f in fabellae)
    L.append("")
    L.append(f"> 共 {len(fabellae)} 个故事, 总词数 {total_fl_words:,}。全部从 Cap. 1 起可读。")
    L.append("")

    # ----- Roma Aeterna -----
    L.append("### Roma Aeterna (Cap. 36-56)")
    L.append("")
    L.append("Roma Aeterna 是 LLPSI 教材下册，每章对应自身 (Cap. 36-56)。")
    L.append("此处列出各章作为自参照, RA 自身即是最好的读物 (读完 FR 后衔接)。")
    L.append("")

    L.append("| RA 章节 | 章节标题 | 词数 |")
    L.append("|:-------:|:---------|-----:|")
    for ra in ra_mappings:
        L.append(f"| Cap. {ra['fr_chapter']} | {ra['title']} | {ra['word_count']:,} |")

    total_ra_words = sum(r["word_count"] for r in ra_mappings)
    L.append("")
    L.append(f"> 共 {len(ra_mappings)} 章 (Cap. 36-56), 总词数 {total_ra_words:,}。")
    L.append("")

    # ---- Part 2 ----
    L.append("---")
    L.append("")
    L.append("## 第二部分：算法匹配推荐")
    L.append("")
    L.append("以下 9 本读物没有精确的 fr_chapter 标注（在数据库中都为 `NULL`），")
    L.append("因此通过词汇重叠度算法 (match_segments.py) 对每章逐一匹配最合适的段落。")
    L.append("")
    L.append("**评分机制**: 综合已知词覆盖率 (0.4)、加权新词命中率 (0.4)、新词密度 (0.2)、高频新词奖励 (0.2)。")
    L.append("")
    L.append("**推荐强度分级**:")
    L.append("")
    L.append("| 标签 | 说明 |")
    L.append("|:-----|:-----|")
    L.append("| :star: 强推荐 | 新词命中率 >= 30% |")
    L.append("| :leftwards_arrow_with_hook: 弱推荐 | 10% <= 新词命中率 < 30% |")
    L.append("| :small_blue_diamond: 微推荐 | 0% < 新词命中率 < 10% |")
    L.append("| :white_small_square: 无覆盖 | 新词命中率 = 0% |")
    L.append("")

    # 运行算法匹配
    print("  [Part 2] 正在运行算法匹配 (逐章 × 9 本书 × 多段)...")
    algo_results = build_algo_recommendations(db_path)

    # 按章节范围分组
    chapter_groups = [
        ("FR 入门 (Cap. 1-7)", range(1, 8)),
        ("FR 进阶 A (Cap. 8-13)", range(8, 14)),
        ("FR 进阶 B (Cap. 14-20)", range(14, 21)),
        ("FR 高阶 (Cap. 21-35)", range(21, 36)),
        ("RA 入门 (Cap. 36-42)", range(36, 43)),
        ("RA 高阶 (Cap. 43-56)", range(43, 57)),
    ]

    # 建立快速查找
    algo_by_ch: dict[int, dict] = {r["chapter"]: r for r in algo_results}

    for group_name, chapters in chapter_groups:
        L.append(f"### {group_name}")
        L.append("")
        L.append("| FR 章节 | 推荐读物 | 段名 | 段词数 | 新词命中 | 命中率 | 推荐度 |")
        L.append("|:-------:|:---------|:-----|------:|:--------:|:------:|:------:|")
        for ch in chapters:
            if ch in algo_by_ch:
                r = algo_by_ch[ch]
                label = _recommendation_label(r["new_cov"])
                L.append(
                    f"| Cap. {ch} | `{r['slug']}` | {r['seg_title']} | "
                    f"{r['word_count']:,} | {r['new_hit']}/{r['new_total']} | "
                    f"{r['new_cov']*100:.1f}% | {label} |"
                )
            else:
                L.append(f"| Cap. {ch} | - | - | - | - | - | :white_small_square: 无覆盖 |")
        L.append("")

    # 汇总统计
    strong_count = sum(1 for r in algo_results if r["new_cov"] >= 0.30)
    weak_count = sum(1 for r in algo_results if 0.10 <= r["new_cov"] < 0.30)
    micro_count = sum(1 for r in algo_results if 0 < r["new_cov"] < 0.10)
    zero_count = sum(1 for r in algo_results if r["new_cov"] == 0)
    L.append("**算法匹配汇总**:")
    L.append("")
    L.append(f"- :star: 强推荐 (>30%): {strong_count} 章")
    L.append(f"- :leftwards_arrow_with_hook: 弱推荐 (10-30%): {weak_count} 章")
    L.append(f"- :small_blue_diamond: 微推荐 (<10%): {micro_count} 章")
    L.append(f"- :white_small_square: 无覆盖 (0%): {zero_count} 章")
    L.append("")

    # 按读物汇总
    L.append("### 按读物汇总")
    L.append("")
    L.append("以下列出每本算法匹配读物的基本信息和在 56 章中的表现。")
    L.append("")
    L.append("| 读物 | 段数 | 总词数 | 作为 Top-1 章数 | 平均新词命中率 | 最高命中率 |")
    L.append("|:-----|:----:|------:|:--------------:|:------------:|:---------:|")

    # 一次性预计算每本书在每章的 distinct new word 命中率
    conn2 = sqlite3.connect(db_path)
    fr_vocab2 = vocab_overlap.load_fr_vocab(db_path)
    all_chapters2 = sorted(fr_vocab2.keys())

    # book_slug -> {chapter: best_cov}
    book_chapter_covs: dict[str, dict[int, float]] = {}
    for slug in ALGO_BOOKS:
        segs = match_segments.load_candidate_segments(db_path, book_slug=slug)
        segs = [s for s in segs if s["fr_chapter"] is None]
        if not segs:
            book_chapter_covs[slug] = {}
            continue
        ch_covs: dict[int, float] = {}
        for ch in all_chapters2:
            _, new_words = match_segments.load_chapter_vocab(db_path, ch)
            if not new_words:
                continue
            best_cov = 0.0
            for seg in segs:
                seg_words = match_segments.load_segment_vocab(db_path, seg["id"])
                distinct_hits = len(set(seg_words.keys()) & new_words)
                cov = distinct_hits / len(new_words)
                if cov > best_cov:
                    best_cov = cov
            ch_covs[ch] = best_cov
        book_chapter_covs[slug] = ch_covs

    for slug in ALGO_BOOKS:
        # 获取该书的基本信息
        cur = conn2.cursor()
        cur.execute("""
            SELECT COUNT(*) as seg_count, SUM(s.word_count) as total_wc
            FROM segments s JOIN books b ON s.book_id = b.id
            WHERE b.slug = ? AND s.fr_chapter IS NULL
        """, (slug,))
        seg_info = cur.fetchone()
        seg_count = seg_info[0] or 0
        total_wc = seg_info[1] or 0

        if seg_count == 0:
            L.append(f"| `{slug}` | 0 | 0 | 0 | N/A | N/A |")
            continue

        ch_covs = book_chapter_covs.get(slug, {})
        covs_list = list(ch_covs.values())
        avg_cov = sum(covs_list) / len(covs_list) if covs_list else 0
        max_cov = max(covs_list) if covs_list else 0
        top1_count = sum(1 for r in algo_results if r["slug"] == slug)

        L.append(
            f"| `{slug}` | {seg_count} | {total_wc:,} | "
            f"{top1_count} | {avg_cov*100:.1f}% | {max_cov*100:.1f}% |"
        )
    conn2.close()
    L.append("")

    # ---- Part 3 ----
    L.append("---")
    L.append("")
    L.append("## 第三部分：覆盖缺口")
    L.append("")
    L.append("以下章节没有设计级精确映射 (无 Colloquia Personarum / Fabulae Syrae / Fabellae Latinae / Roma Aeterna 对应)，")
    L.append("且算法匹配的最高新词命中率 < 20%，建议通过 AI 生成微阅读来覆盖。")
    L.append("")

    # 确定设计级覆盖章节
    design_chapters: set[int] = set()
    # Colloquia: 1-24
    design_chapters.update(range(1, 25))
    # Fabulae Syrae: 26-34
    design_chapters.update(range(26, 35))
    # Fabellae Latinae: 1-25 (所有故事都有 cap 范围)
    design_chapters.update(range(1, 26))
    # Roma Aeterna: 36-56
    design_chapters.update(range(36, 57))

    gaps = find_gaps(design_chapters, algo_results)

    if gaps:
        L.append("| 章节 | 最高新词命中 | 最佳读物 | 新词命中详情 | 建议 |")
        L.append("|:----:|:-----------:|:---------|:------------|:-----|")
        for g in gaps:
            if g["highest_new_cov"] < 0.10:
                suggestion = "需 AI 生成微阅读"
            elif g["highest_new_cov"] < 0.20:
                suggestion = "勉强可用, 建议 AI 生成微阅读补充"
            else:
                suggestion = "基本可用"
            L.append(
                f"| Cap. {g['chapter']} | {g['highest_new_cov']*100:.1f}% | "
                f"`{g['best_slug']}` | "
                f"{g['best_new_hit']}/{g['best_new_total']} | "
                f"{suggestion} |"
            )
        L.append("")
    else:
        L.append(":white_check_mark: 所有章节都有设计级映射, 无需额外 AI 生成覆盖。")
        L.append("")

    # ---- 附录 ----
    L.append("---")
    L.append("")
    L.append("## 附录")
    L.append("")
    L.append("### A. 算法匹配 Top-3 详情 (每章)")
    L.append("")
    L.append("以下列出每章算法匹配的前 3 名段落, 供参考选择。")
    L.append("")
    L.append("| 章节 | 排名 | 读物 | 段名 | 分数 | 新词命中 | 已知覆盖 |")
    L.append("|:----:|:----:|:-----|:-----|:----:|:--------:|:--------:|")

    # 重新计算 top-3
    conn = sqlite3.connect(db_path)
    fr_vocab = vocab_overlap.load_fr_vocab(db_path)
    all_chapters = sorted(fr_vocab.keys())

    # 预加载所有候选段
    all_candidates = []
    for slug in ALGO_BOOKS:
        segs = match_segments.load_candidate_segments(db_path, book_slug=slug)
        segs = [s for s in segs if s["fr_chapter"] is None]
        all_candidates.extend(segs)

    for ch in all_chapters:
        known, new_words = match_segments.load_chapter_vocab(db_path, ch)
        if not new_words:
            continue

        scored = []
        for seg in all_candidates:
            seg_words = match_segments.load_segment_vocab(db_path, seg["id"])
            sc = match_segments.score_segment(
                seg_words, known, new_words,
                w1=0.4, w2=0.4, w3=0.2, w4=0.2
            )
            distinct_new_hits = len(set(seg_words.keys()) & new_words)
            scored.append({
                "seg": seg,
                "score": sc["score"],
                "known_cov": sc["known_cov"],
                "new_hits": distinct_new_hits,
                "new_total": len(new_words),
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        for rank, s in enumerate(scored[:3], 1):
            seg = s["seg"]
            L.append(
                f"| Cap. {ch} | {rank} | `{seg['book_slug']}` | "
                f"{seg['title']} | {s['score']:.3f} | "
                f"{s['new_hits']}/{s['new_total']} ({s['new_hits']/max(1,s['new_total'])*100:.0f}%) | "
                f"{s['known_cov']*100:.0f}% |"
            )
        L.append("| | | | | | | |")

    conn.close()

    # 尾部说明
    L.append("")
    L.append("---")
    L.append("")
    L.append("*本报告由 `scripts/generate_insertion_guide.py` 自动生成。*")
    L.append("")

    return "\n".join(L)


# ============================================================
# Main
# ============================================================
def main():
    db_path = get_db_path()

    print("  正在生成 LLPSI 扩展读物插入推荐指南...")
    print(f"  数据库: {db_path}")

    # 验证数据完整性
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM fr_vocab")
    fr_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM segments")
    seg_count = cur.fetchone()[0]
    conn.close()

    print(f"  fr_vocab 表: {fr_count:,} 行")
    print(f"  segments 表: {seg_count:,} 行")
    print()

    report = generate_report(db_path)

    # 确保输出目录存在
    output_path = os.path.join(PROJECT_DIR, OUTPUT_MD)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"  [完成] 报告已写入: {output_path}")
    print(f"  [完成] 报告大小: {len(report):,} 字符")


if __name__ == "__main__":
    main()
