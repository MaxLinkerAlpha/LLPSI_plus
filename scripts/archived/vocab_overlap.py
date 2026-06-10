#!/usr/bin/env python3
"""
vocab_overlap.py — 词汇重叠度分析 (FR+RA 56 章连贯 vs reader)
==============================================================
目标: 量化每个 reader 对 FR+RA 全 56 章的词汇覆盖度,
      输出"插入位置推荐"——在 LLPSI 主干 (FR+RA) 的哪一章
      插入某本 reader 能获得最佳语言输入。

视角: FR+RA 是 LLPSI 主干教材, 是连贯的 56 章系列 (FR 1-35 + RA 36-56)。
      不再单独分析 RA。

输出:
  1. 终端表格: 每个 reader × FR+RA 56 章 × 关键指标 (覆盖/新词命中)
  2. analysis_output/vocab_overlap_report.md: Markdown 报告
  3. analysis_output/vocab_overlap_matrix.csv: 56 章 × 13 reader 矩阵
  4. analysis_output/insertion_recommendations.md: 插入位置推荐

用法:
    python3 scripts/vocab_overlap.py
    python3 scripts/vocab_overlap.py --reader fabulae_syrae
    python3 scripts/vocab_overlap.py --chapter 36 --top 3
    python3 scripts/vocab_overlap.py --strong-threshold 0.30
"""

import argparse
import csv
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict


DEFAULT_DB = "data/llpsi_corpus.db"

# 强推荐阈值 (新词命中率)
DEFAULT_STRONG_THRESHOLD = 0.30

# FR/RA 自身不算 reader (它们是参考系, 不参与插入推荐)
EXCLUDED_SLUGS = {"familia_romana", "roma_aeterna"}

# 章节分组标签 (用于报告分组显示)
CHAPTER_GROUPS = {
    "FR 入门 (Cap. 1-7)": list(range(1, 8)),
    "FR 进阶 A (Cap. 8-13)": list(range(8, 14)),
    "FR 进阶 B (Cap. 14-20)": list(range(14, 21)),
    "FR 高阶 (Cap. 21-35)": list(range(21, 36)),
    "RA 入门 (Cap. 36-42)": list(range(36, 43)),
    "RA 高阶 (Cap. 43-56)": list(range(43, 57)),
}


# ============================================================
# 数据加载
# ============================================================
def load_fr_vocab(db_path: str) -> dict[int, set[str]]:
    """从 fr_vocab 表加载每章词表 (1-56 章连贯).
    返回 {chapter: {word_form, ...}}."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT chapter, word_form FROM fr_vocab")
    rows = cur.fetchall()
    conn.close()
    vocab: dict[int, set[str]] = {}
    for ch, w in rows:
        vocab.setdefault(ch, set()).add(w)
    return vocab


def load_segment_words(db_path: str, slug: str) -> set[str]:
    """加载某本书所有 segment 的 union 词形."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT v.word_form
        FROM vocab v
        JOIN segments s ON v.segment_id = s.id
        JOIN books b ON s.book_id = b.id
        WHERE b.slug = ?
    """, (slug,))
    words = {r[0] for r in cur.fetchall()}
    conn.close()
    return words


def load_segment_words_by_chapter(db_path: str, slug: str, fr_chapter: int) -> set[str] | None:
    """加载指定书中 fr_chapter == 目标章 的段的词形 union。

    用于精确模式 (--precise): 只取与目标 FR 章对应的段词汇，
    而非全书所有段的词形 union。例如 fabulae_syrae 的 Cap.26 段
    只包含 fr_chapter=26 的词汇。

    Args:
        db_path: SQLite 数据库路径
        slug: 书的 slug (如 "fabulae_syrae")
        fr_chapter: 目标 Familia Romana 章号 (1-56)

    Returns:
        匹配 fr_chapter 的所有段的词形集合；
        如果没有匹配的段（该书此章无对应段），返回 None。
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT v.word_form
        FROM vocab v
        JOIN segments s ON v.segment_id = s.id
        JOIN books b ON s.book_id = b.id
        WHERE b.slug = ? AND s.fr_chapter = ?
    """, (slug, fr_chapter))
    words = {r[0] for r in cur.fetchall()}
    conn.close()
    if not words:
        return None
    return words


def get_all_reader_slugs(db_path: str) -> list[str]:
    """获取所有 reader slug (排除 FR/RA 自身)."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT b.slug FROM books b JOIN segments s ON s.book_id=b.id")
    all_slugs = [r[0] for r in cur.fetchall()]
    conn.close()
    return [s for s in sorted(all_slugs) if s not in EXCLUDED_SLUGS]


# ============================================================
# 核心分析: 56 章连贯视角
# ============================================================
def compute_overlap(reader_words: set[str], fr_vocab: dict[int, set[str]],
                    chapter_reader_words: dict[int, set[str]] | None = None) -> dict:
    """对每章 (1-56) 计算 reader 覆盖度.

    关键指标:
      known_total   = 学完 ch 之前所有章后读者应已掌握的词数
      new_total     = 本章相对前面所有章的"新词"数 (is_new 累计)
      known_covered = reader ∩ known
      new_hit       = reader ∩ new
      known_cov     = known_covered / known_total
      new_cov       = new_hit / new_total      ← 核心指标 (越高越值得插入)

    Args:
        reader_words: 全书的词形集合（非精确模式或回退时使用）
        fr_vocab: FR 词汇表 {chapter: {word_form, ...}}
        chapter_reader_words: 精确模式下，{chapter: 该章对应段的词形集合}。
                              如果某章不在 dict 中，说明该书没有此章的对应段，
                              自动回退到 reader_words（全书词袋）。
                              传入 None 时行为不变（始终用全书词袋）。
    """
    all_chapters = sorted(fr_vocab.keys())

    results = {"per_chapter": {}, "overall": {}}

    for ch in all_chapters:
        # 精确模式：使用章节对应的段词表；无对应段时回退到全书词袋
        if chapter_reader_words and ch in chapter_reader_words:
            ch_reader_words = chapter_reader_words[ch]
        else:
            ch_reader_words = reader_words

        ch_words = fr_vocab[ch]
        prev_words: set[str] = set()
        for c in all_chapters:
            if c >= ch:
                break
            prev_words.update(fr_vocab[c])
        new_words = ch_words - prev_words
        known = prev_words

        hit_known = ch_reader_words & known
        hit_new = ch_reader_words & new_words
        results["per_chapter"][ch] = {
            "known_total": len(known),
            "new_total": len(new_words),
            "known_covered": len(hit_known),
            "new_hit": len(hit_new),
            "known_cov": len(hit_known) / max(1, len(known)),
            "new_cov": len(hit_new) / max(1, len(new_words)),
        }

    # 整体: reader 词表与全 56 章词表的交集（始终用全书词袋，反映 reader 总词汇覆盖力）
    all_known = set()
    for ch_words in fr_vocab.values():
        all_known.update(ch_words)
    hit = reader_words & all_known
    results["overall"] = {
        "fr_vocab_size": len(all_known),
        "covered": len(hit),
        "coverage": len(hit) / max(1, len(all_known)),
        "reader_size": len(reader_words),
        "reader_in_fr_density": len(hit) / max(1, len(reader_words)),
    }
    return results


def find_best_readers_for_chapter(db_path: str, ch: int, fr_vocab: dict[int, set[str]],
                                   top_n: int = 3, precise: bool = False) -> list[dict]:
    """找最适合某一章的 reader (新词命中率最高).

    Args:
        precise: 启用时用 load_segment_words_by_chapter 按 fr_chapter 过滤；
                 无匹配段时回退到全书词袋。
    """
    new_words = fr_vocab[ch] - set().union(*(
        fr_vocab[c] for c in sorted(fr_vocab.keys()) if c < ch
    ))
    if not new_words:
        return []

    reader_slugs = get_all_reader_slugs(db_path)

    scored = []
    for slug in reader_slugs:
        if precise:
            words = load_segment_words_by_chapter(db_path, slug, ch)
            if words is None:
                words = load_segment_words(db_path, slug)  # 回退到全书词袋
        else:
            words = load_segment_words(db_path, slug)
        new_hit = words & new_words
        if not new_hit:
            continue
        scored.append({
            "slug": slug,
            "new_hit": len(new_hit),
            "new_total": len(new_words),
            "new_cov": len(new_hit) / len(new_words),
            "reader_size": len(words),
        })
    scored.sort(key=lambda x: x["new_cov"], reverse=True)
    return scored[:top_n]


# ============================================================
# 插入位置推荐
# ============================================================
def compute_insertion_recommendations(books_overlap: dict[str, dict],
                                      fr_vocab: dict[int, set[str]],
                                      strong_threshold: float) -> dict:
    """为每个 reader 计算"适合在哪一章后插入".

    Returns:
        {
            "by_chapter": {ch: [reader_slug, ...] (强推荐)},
            "by_reader": {slug: [ch, ...] (强推荐章节)},
        }
    """
    by_chapter: dict[int, list[str]] = defaultdict(list)
    by_reader: dict[str, list[int]] = defaultdict(list)

    for slug, ov in books_overlap.items():
        for ch, data in ov["per_chapter"].items():
            if data["new_cov"] >= strong_threshold:
                by_chapter[ch].append(slug)
                by_reader[slug].append(ch)

    # 排序
    for ch in by_chapter:
        by_chapter[ch].sort(key=lambda s: -books_overlap[s]["per_chapter"][ch]["new_cov"])
    for slug in by_reader:
        by_reader[slug].sort()

    return {"by_chapter": dict(by_chapter), "by_reader": dict(by_reader)}


# ============================================================
# 报告生成
# ============================================================
def print_overall_table(books_overlap: dict[str, dict]):
    """打印每个 reader 对 FR+RA 56 章词表的总覆盖率."""
    print(f"\n{'='*80}")
    print(f"  Reader × FR+RA (56 章连贯) 词汇覆盖度 (整体)")
    print(f"{'='*80}")
    print(f"  {'Reader':<25} {'词数':<8} {'覆盖词':<8} {'覆盖率':<10} {'FR+RA词占比':<12}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*10} {'-'*12}")
    for slug, ov in sorted(books_overlap.items(),
                           key=lambda x: -x[1]["overall"]["coverage"]):
        o = ov["overall"]
        print(f"  {slug:<25} {o['reader_size']:<8} {o['covered']:<8} "
              f"{o['coverage']*100:>5.1f}%    {o['reader_in_fr_density']*100:>5.1f}%")


def print_chapter_group_table(books_overlap: dict[str, dict],
                              fr_vocab: dict[int, set[str]]):
    """按章节组打印 reader × 新词命中率 (按 6 组聚合)."""
    for group_name, chapters in CHAPTER_GROUPS.items():
        print(f"\n{'='*90}")
        print(f"  {group_name}: {chapters[0]}-{chapters[-1]}")
        print(f"{'='*90}")
        print(f"  {'Reader':<22}", end="")
        for ch in chapters:
            print(f"  Cap.{ch:<4}", end="")
        print("  Avg")
        print(f"  {'-'*22}" + "  " + "  ".join(f"{'-'*7}" for _ in chapters) + "  " + "-"*6)
        for slug, ov in sorted(books_overlap.items(),
                               key=lambda x: -x[1]["overall"]["coverage"]):
            row = f"  {slug:<22}"
            covs = []
            for ch in chapters:
                if ch in ov["per_chapter"]:
                    cov = ov["per_chapter"][ch]["new_cov"]
                    covs.append(cov)
                    row += f"  {cov*100:>5.1f}%"
                else:
                    row += f"  {'-':<7}"
            avg = sum(covs) / max(1, len(covs)) if covs else 0
            row += f"  {avg*100:>5.1f}%"
            print(row)


def print_insertion_recommendations(recommendations: dict,
                                    books_overlap: dict[str, dict],
                                    fr_vocab: dict[int, set[str]],
                                    strong_threshold: float):
    """打印插入位置推荐 (按章节顺序)."""
    by_chapter = recommendations["by_chapter"]
    by_reader = recommendations["by_reader"]

    print(f"\n{'='*80}")
    print(f"  插入位置推荐 (新词命中率 ≥ {strong_threshold*100:.0f}%)")
    print(f"{'='*80}")

    if not by_chapter:
        print("  无任何强推荐组合。考虑降低阈值。")
        return

    print(f"  {'章节':<10} {'强推荐 reader':<55} {'新词命中':<10}")
    print(f"  {'-'*10} {'-'*55} {'-'*10}")
    for ch in sorted(by_chapter.keys()):
        readers = by_chapter[ch]
        if len(readers) == 1:
            tag = readers[0]
        else:
            tag = ", ".join(readers) + f"  ({len(readers)} 本)"
        new_total = fr_vocab[ch] - set().union(*(
            fr_vocab[c] for c in sorted(fr_vocab.keys()) if c < ch
        ))
        # 显示最匹配的 reader 的命中数
        top_slug = readers[0]
        top_cov = books_overlap[top_slug]["per_chapter"][ch]
        cov_str = f"{top_cov['new_hit']}/{top_cov['new_total']} ({top_cov['new_cov']*100:.0f}%)"
        print(f"  Cap. {ch:<5} {tag:<55} {cov_str}")

    print(f"\n  按 reader 视角:")
    print(f"  {'Reader':<25} {'强推荐章节数':<12} {'章节范围':<30}")
    print(f"  {'-'*25} {'-'*12} {'-'*30}")
    for slug, chs in sorted(by_reader.items(),
                            key=lambda x: -len(x[1])):
        chs_sorted = chs
        # 把连续章节合并
        ranges = []
        start = chs_sorted[0]
        prev = chs_sorted[0]
        for c in chs_sorted[1:]:
            if c == prev + 1:
                prev = c
            else:
                ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
                start = c
                prev = c
        ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
        print(f"  {slug:<25} {len(chs_sorted):<12} {', '.join(ranges):<30}")


def generate_markdown_report(books_overlap: dict[str, dict],
                              fr_vocab: dict[int, set[str]],
                              recommendations: dict,
                              strong_threshold: float) -> str:
    """生成 Markdown 报告."""
    lines = []
    lines.append("# 词汇重叠度分析报告 (FR+RA 56 章连贯 vs Reader)")
    lines.append("")
    lines.append("> 视角: **FR+RA 是 LLPSI 主干教材的连贯系列 (1-56 章)**, "
                 f"强推荐阈值 = 新词命中率 ≥ {strong_threshold*100:.0f}%")
    lines.append("> 排除自身: `familia_romana` 和 `roma_aeterna` 不参与 reader 分析 (它们是参考系)。")
    lines.append("")

    # 1. 整体覆盖
    lines.append("## 一、整体覆盖度 (Reader 词表 vs FR+RA 56 章词表)")
    lines.append("")
    total_vocab = len(set().union(*fr_vocab.values()))
    lines.append(f"FR+RA 全 56 章词形数: **{total_vocab:,}** (FR 9,417 + RA 新增 16,031)")
    lines.append("")
    lines.append("| Reader | 词数 | 覆盖FR+RA词 | 覆盖率 | FR+RA词占比 |")
    lines.append("|:-------|-----:|------------:|-------:|------------:|")
    for slug, ov in sorted(books_overlap.items(),
                            key=lambda x: -x[1]["overall"]["coverage"]):
        o = ov["overall"]
        lines.append(f"| `{slug}` | {o['reader_size']:,} | {o['covered']:,} | "
                     f"**{o['coverage']*100:.1f}%** | {o['reader_in_fr_density']*100:.1f}% |")
    lines.append("")

    # 2. 各章节组覆盖
    lines.append("## 二、各章节组新词命中率 (按 6 组聚合)")
    lines.append("")
    lines.append("**新词命中率** = (Reader 词表 ∩ 本章新词) / 本章新词数。")
    lines.append("数值越高, 说明读完此章后立即读这本 reader, 越能高效巩固本章新词。")
    lines.append("")
    for group_name, chapters in CHAPTER_GROUPS.items():
        lines.append(f"### {group_name}")
        lines.append("")
        header = "| Reader | " + " | ".join(f"Cap.{ch}" for ch in chapters) + " | Avg |"
        sep = "|:-------|" + "|".join([":-----:"] * (len(chapters) + 1)) + "|"
        lines.append(header)
        lines.append(sep)
        for slug, ov in sorted(books_overlap.items(),
                               key=lambda x: -x[1]["overall"]["coverage"]):
            row = [f"`{slug}`"]
            covs = []
            for ch in chapters:
                if ch in ov["per_chapter"]:
                    cov = ov["per_chapter"][ch]["new_cov"]
                    covs.append(cov)
                    row.append(f"{cov*100:.1f}%")
                else:
                    row.append("-")
            avg = sum(covs) / max(1, len(covs)) if covs else 0
            row.append(f"**{avg*100:.1f}%**")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    # 3. 插入位置推荐
    lines.append("## 三、插入位置推荐 (新词命中率 ≥ {}%)".format(int(strong_threshold*100)))
    lines.append("")
    by_chapter = recommendations["by_chapter"]
    by_reader = recommendations["by_reader"]
    lines.append("> **逻辑**: 当读者学完 Cap. N 后, 如果某本 reader 对 Cap. N 的新词"
                 f"命中率 ≥ {strong_threshold*100:.0f}%, 则该 reader 是 Cap. N 结束后的"
                 "强推荐插入读物。")
    lines.append("> **多本推荐**: 允许多本 reader 同时推荐 (如果都达到阈值), "
                 "给读者提供选择空间。")
    lines.append("")

    if by_chapter:
        lines.append("### 3.1 按章节视角 (哪一章后该读什么)")
        lines.append("")
        lines.append("**有强推荐 reader 的章节** (新词命中率 ≥ 30%):")
        lines.append("")
        lines.append("| 章节 | 强推荐 reader | 最佳命中详情 |")
        lines.append("|:----:|:--------------|:-------------|")
        for ch in sorted(by_chapter.keys()):
            readers = by_chapter[ch]
            top_slug = readers[0]
            top_cov = books_overlap[top_slug]["per_chapter"][ch]
            cov_str = f"`{top_slug}` 命中 {top_cov['new_hit']}/{top_cov['new_total']} ({top_cov['new_cov']*100:.0f}%)"
            if len(readers) == 1:
                tag = f"`{readers[0]}`"
            else:
                tag = ", ".join(f"`{r}`" for r in readers)
            lines.append(f"| Cap. {ch} | {tag} | {cov_str} |")
        lines.append("")

        # 列出"无强推荐"章节 (Cap. 32+ 几乎没有)
        all_ch_set = set(fr_vocab.keys())
        no_recommend = sorted(all_ch_set - set(by_chapter.keys()))
        if no_recommend:
            lines.append(f"**无强推荐 reader 的章节** (新词命中率 < 30%, 缺少 reader 支撑):")
            lines.append("")
            # 合并连续区间
            ranges = []
            if no_recommend:
                start = no_recommend[0]
                prev = no_recommend[0]
                for c in no_recommend[1:]:
                    if c == prev + 1:
                        prev = c
                    else:
                        ranges.append((start, prev))
                        start = c
                        prev = c
                ranges.append((start, prev))
            range_strs = [f"{a}-{b}" if a != b else f"{a}" for a, b in ranges]
            lines.append(f"- 章节范围: {', '.join(range_strs)} ({len(no_recommend)} 章)")
            # 显示每个无强推荐章节的"最佳命中"作为参考
            lines.append("")
            lines.append("| 章节 | 最高命中 reader | 最高命中率 |")
            lines.append("|:----:|:----------------|:----------|")
            for ch in no_recommend:
                best = max(books_overlap.items(),
                           key=lambda x: x[1]["per_chapter"].get(ch, {}).get("new_cov", 0))
                slug, ov = best
                cov = ov["per_chapter"].get(ch, {}).get("new_cov", 0)
                hit = ov["per_chapter"].get(ch, {}).get("new_hit", 0)
                tot = ov["per_chapter"].get(ch, {}).get("new_total", 0)
                lines.append(f"| Cap. {ch} | `{slug}` | {cov*100:.1f}% ({hit}/{tot}) |")
            lines.append("")

        lines.append("### 3.2 按 Reader 视角 (这本 reader 适合在哪些章节后插入)")
        lines.append("")
        lines.append("| Reader | 强推荐章节数 | 章节范围 | 适合的 LLPSI 阶段 |")
        lines.append("|:-------|:------------:|:---------|:-----------------|")
        for slug, chs in sorted(by_reader.items(), key=lambda x: -len(x[1])):
            chs_sorted = chs
            ranges = []
            start = chs_sorted[0]
            prev = chs_sorted[0]
            for c in chs_sorted[1:]:
                if c == prev + 1:
                    prev = c
                else:
                    ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
                    start = c
                    prev = c
            ranges.append(f"{start}-{prev}" if start != prev else f"{start}")
            # 推断适合阶段 (按章节组分类)
            stages = set()
            for c in chs_sorted:
                for stage, rng in CHAPTER_GROUPS.items():
                    if c in rng:
                        stages.add(stage)
            lines.append(f"| `{slug}` | {len(chs_sorted)} | {', '.join(ranges)} | "
                         f"{', '.join(sorted(stages))} |")
        lines.append("")
    else:
        lines.append("> ⚠️ **无任何强推荐组合**。考虑降低阈值重跑。")
        lines.append("")

    # 4. 词汇缝隙
    lines.append("## 四、词汇缝隙警告")
    lines.append("")
    lines.append("> 哪些章节的「新词」几乎没有任何 reader 命中 (阈值 < 10%)?")
    lines.append("")
    gap_chapters = []
    for ch in sorted(fr_vocab.keys()):
        ch_data = []
        for slug, ov in books_overlap.items():
            if ch in ov["per_chapter"]:
                ch_data.append((slug, ov["per_chapter"][ch]["new_cov"]))
        if ch_data:
            max_cov = max(c[1] for c in ch_data)
            if max_cov < 0.1:
                gap_chapters.append((ch, max_cov, ch_data))
    if gap_chapters:
        lines.append("| 章节 | 最高新词覆盖 | 状态 | 最佳 reader |")
        lines.append("|:----:|------------:|:-----|:------------|")
        for ch, max_cov, ch_data in gap_chapters:
            best_slug = max(ch_data, key=lambda x: x[1])[0]
            status = "🔴 强缝隙" if max_cov < 0.05 else "🟡 弱覆盖"
            lines.append(f"| Cap. {ch} | {max_cov*100:.1f}% | {status} | `{best_slug}` |")
    else:
        lines.append("✅ 所有 56 章都至少有一个 reader 覆盖 ≥10% 新词")
    lines.append("")

    return "\n".join(lines)


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--reader", help="只分析某一本 reader")
    parser.add_argument("--chapter", type=int, help="只分析某一章的 top reader")
    parser.add_argument("--top", type=int, default=3, help="top N reader (default 3)")
    parser.add_argument("--strong-threshold", type=float, default=DEFAULT_STRONG_THRESHOLD,
                        help=f"强推荐新词命中率阈值 (default {DEFAULT_STRONG_THRESHOLD})")
    parser.add_argument("--precise", action="store_true",
                        help="精确模式：按 fr_chapter 过滤段词汇，"
                             "每章只用对应 fr_chapter 的段（有标注的 reader 才生效）")
    args = parser.parse_args()

    if not os.path.exists(args.db):
        print(f"  [错误] 数据库不存在: {args.db}", file=sys.stderr)
        sys.exit(1)

    fr_vocab = load_fr_vocab(args.db)
    if not fr_vocab:
        print("  [错误] fr_vocab 表为空, 请先跑 --init-all-vocab", file=sys.stderr)
        sys.exit(1)

    all_chapters = sorted(fr_vocab.keys())
    print(f"\n  [分析] FR+RA 连贯视角, 共 {len(all_chapters)} 章 (Cap. {all_chapters[0]}-{all_chapters[-1]})")
    if args.precise:
        print("  [模式] 精确模式 (按 fr_chapter 过滤段词汇)")

    # 单章查询
    if args.chapter:
        best = find_best_readers_for_chapter(args.db, args.chapter, fr_vocab,
                                              top_n=args.top, precise=args.precise)
        print(f"\n  Cap. {args.chapter} 新词命中率 Top {args.top}:")
        for i, b in enumerate(best, 1):
            print(f"  {i}. {b['slug']:<25} 命中 {b['new_hit']}/{b['new_total']} "
                  f"({b['new_cov']*100:.1f}%)")
        return

    # 获取所有 reader (排除 FR/RA 自身)
    all_slugs = get_all_reader_slugs(args.db)
    if args.reader:
        if args.reader not in all_slugs:
            print(f"  [错误] '{args.reader}' 不在 reader 列表中 (或它是 FR/RA 自身)", file=sys.stderr)
            sys.exit(1)
        slugs = [args.reader]
    else:
        slugs = all_slugs

    # 计算每本的覆盖度
    print(f"  [加载] {len(slugs)} 本 reader 的词表 (排除 FR/RA 自身)...")
    books_overlap = {}
    for slug in slugs:
        words = load_segment_words(args.db, slug)

        if args.precise:
            # 精确模式：逐章尝试加载 fr_chapter 对应的段词汇
            chapter_reader_words: dict[int, set[str]] = {}
            for ch in all_chapters:
                ch_words = load_segment_words_by_chapter(args.db, slug, ch)
                if ch_words is not None:
                    chapter_reader_words[ch] = ch_words
            if chapter_reader_words:
                # 有 fr_chapter 标注 → 精确模式生效
                ov = compute_overlap(words, fr_vocab,
                                     chapter_reader_words=chapter_reader_words)
            else:
                # 该书没有任何 fr_chapter 标注 → 回退到全书词袋
                ov = compute_overlap(words, fr_vocab)
        else:
            ov = compute_overlap(words, fr_vocab)

        books_overlap[slug] = ov

    # 计算插入推荐
    recommendations = compute_insertion_recommendations(
        books_overlap, fr_vocab, args.strong_threshold
    )

    # 输出
    print_overall_table(books_overlap)
    print_chapter_group_table(books_overlap, fr_vocab)
    print_insertion_recommendations(recommendations, books_overlap, fr_vocab, args.strong_threshold)

    # Markdown 报告
    md = generate_markdown_report(books_overlap, fr_vocab, recommendations, args.strong_threshold)
    out_md = "analysis_output/vocab_overlap_report.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\n  [完成] 报告已写入: {out_md}")

    # CSV 矩阵 (56 章 × reader)
    out_csv = "analysis_output/vocab_overlap_matrix.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        header = ["reader"] + [f"cap_{ch}_new_cov" for ch in all_chapters]
        w.writerow(header)
        for slug, ov in sorted(books_overlap.items()):
            row = [slug]
            for ch in all_chapters:
                row.append(f"{ov['per_chapter'].get(ch, {}).get('new_cov', 0)*100:.2f}")
            w.writerow(row)
    print(f"  [完成] CSV 矩阵 ({len(all_chapters)} 章 × {len(slugs)} reader): {out_csv}")

    # 插入推荐 JSON
    out_json = "analysis_output/insertion_recommendations.json"
    rec_export = {
        "threshold": args.strong_threshold,
        "by_chapter": {str(ch): recs for ch, recs in recommendations["by_chapter"].items()},
        "by_reader": recommendations["by_reader"],
    }
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(rec_export, f, ensure_ascii=False, indent=2)
    print(f"  [完成] 插入推荐 JSON: {out_json}")


if __name__ == "__main__":
    main()
