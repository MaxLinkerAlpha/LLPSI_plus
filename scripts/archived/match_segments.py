#!/usr/bin/env python3
"""
match_segments.py — 匹配函数
================================
输入: 目标章节 (1-35) + 已知词表 (FR Cap. 1 to N-1) + 新词表 (FR Cap. N 新词)
输出: top-N 段落, 按 fit_score 排序

打分公式:
    fit_score = w1 * known_coverage
              + w2 * new_hits_normalized
              + w3 * new_density

其中:
    known_coverage        = 段中已知词数 / 段总词数      (高 = 大量用熟词)
    new_hits_normalized   = 段中新词数 / 目标新词数       (高 = 覆盖更多新词)
    new_density           = 段中新词数 / 段总词数          (高 = 新词集中)

默认权重 w1=0.4, w2=0.4, w3=0.2 (可调)

用法:
    python3 scripts/match_segments.py --chapter 10 --top-n 3
    python3 scripts/match_segments.py --chapter 10 --book colloquia_personarum
    python3 scripts/match_segments.py --chapter 8-13 25 --top-n 3
"""

import argparse
import sqlite3
import sys
from collections import Counter


DEFAULT_DB = "data/llpsi_corpus.db"


# ============================================================
# 加载目标章的已知词 + 新词
# ============================================================
def load_chapter_vocab(db_path: str, chapter: int) -> tuple[set[str], set[str]]:
    """从 fr_vocab 表加载指定章的 (known_words, new_words)。"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # known_words: chapter < N 的所有词形
    cur.execute("""
        SELECT DISTINCT word_form FROM fr_vocab
        WHERE chapter < ?
    """, (chapter,))
    known = {r[0] for r in cur.fetchall()}

    # new_words: chapter = N 且 is_new = 1
    cur.execute("""
        SELECT DISTINCT word_form FROM fr_vocab
        WHERE chapter = ? AND is_new = 1
    """, (chapter,))
    new = {r[0] for r in cur.fetchall()}

    conn.close()
    return known, new


# ============================================================
# 加载候选段落
# ============================================================
def load_candidate_segments(db_path: str, book_slug: str | None = None,
                            fr_chapter_filter: int | None = None
                            ) -> list[dict]:
    """加载所有 segments (或指定书的 segments)。

    Args:
        db_path: SQLite 数据库路径
        book_slug: 可选，限定某一本书
        fr_chapter_filter: 可选，只加载 fr_chapter == 该值的段。
                           用于 --use-fr-chapter 模式，实现精确章节匹配。
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if book_slug:
        if fr_chapter_filter is not None:
            cur.execute("""
                SELECT s.id, s.book_id, s.sequence, s.title, s.latin, s.word_count,
                       s.fr_chapter, b.slug, b.title
                FROM segments s JOIN books b ON s.book_id = b.id
                WHERE b.slug = ? AND s.fr_chapter = ?
                ORDER BY b.slug, s.sequence
            """, (book_slug, fr_chapter_filter))
        else:
            cur.execute("""
                SELECT s.id, s.book_id, s.sequence, s.title, s.latin, s.word_count,
                       s.fr_chapter, b.slug, b.title
                FROM segments s JOIN books b ON s.book_id = b.id
                WHERE b.slug = ?
                ORDER BY b.slug, s.sequence
            """, (book_slug,))
    else:
        if fr_chapter_filter is not None:
            cur.execute("""
                SELECT s.id, s.book_id, s.sequence, s.title, s.latin, s.word_count,
                       s.fr_chapter, b.slug, b.title
                FROM segments s JOIN books b ON s.book_id = b.id
                WHERE s.fr_chapter = ?
                ORDER BY b.slug, s.sequence
            """, (fr_chapter_filter,))
        else:
            cur.execute("""
                SELECT s.id, s.book_id, s.sequence, s.title, s.latin, s.word_count,
                       s.fr_chapter, b.slug, b.title
                FROM segments s JOIN books b ON s.book_id = b.id
                ORDER BY b.slug, s.sequence
            """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0], "book_id": r[1], "sequence": r[2],
            "title": r[3], "latin": r[4], "word_count": r[5],
            "fr_chapter": r[6], "book_slug": r[7], "book_title": r[8],
        }
        for r in rows
    ]


# ============================================================
# 词频加载 (从 vocab 表)
# ============================================================
def load_segment_vocab(db_path: str, seg_id: int) -> Counter:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT word_form, freq FROM vocab WHERE segment_id=?", (seg_id,))
    rows = cur.fetchall()
    conn.close()
    return Counter({w: c for w, c in rows})


# ============================================================
# 打分
# ============================================================
def score_segment(seg_words: Counter, known: set[str], new: set[str],
                  w1: float, w2: float, w3: float, w4: float = 0.0,
                  high_freq_weight: float = 2.0) -> dict:
    """对单个段落计算 fit_score 分解。

    增强 (v1.6.0):
    - 把 new_hits 拆分为 low_freq (freq<=1) 和 high_freq (freq>=2) 两部分
    - high_freq 权重 = high_freq_weight (默认 2.0)
    - 加权后: 包含"本章核心高频新词"的段得分显著提升
    - 避免某些段只靠 1 次出现的生词堆砌得分 (背景词噪声)
    """
    total = sum(seg_words.values())
    if total == 0:
        return {"score": 0, "known_cov": 0, "new_hits": 0, "new_den": 0,
                "total": 0, "known_hits": 0, "hf_new_hits": 0,
                "weighted_new_hits": 0}

    known_hits = sum(c for w, c in seg_words.items() if w in known)
    new_hits = sum(c for w, c in seg_words.items() if w in new)

    # 新增: 高频新词统计 (freq >= 2 的新词)
    hf_new_hits = sum(c for w, c in seg_words.items() if w in new and c >= 2)
    # 低频新词 = 总新词 - 高频新词
    lf_new_hits = new_hits - hf_new_hits
    # 加权新词: 低频按 1x, 高频按 high_freq_weight x
    weighted_new_hits = lf_new_hits + hf_new_hits * high_freq_weight

    known_cov = known_hits / total
    new_hits_norm = new_hits / max(1, len(new))   # coverage of target new words
    new_den = new_hits / total                    # density of new words in segment

    # w1: known_cov, w2: weighted_new_hits_norm, w3: new_density, w4: hf_new_hits_bonus
    score = (w1 * known_cov
             + w2 * (weighted_new_hits / max(1, len(new)))
             + w3 * new_den
             + w4 * (hf_new_hits / max(1, len(new))))

    return {
        "score": score,
        "known_cov": known_cov,
        "new_hits": new_hits,
        "new_hits_norm": new_hits_norm,
        "new_den": new_den,
        "total": total,
        "known_hits": known_hits,
        "hf_new_hits": hf_new_hits,
        "weighted_new_hits": weighted_new_hits,
    }


# ============================================================
# 主流程
# ============================================================
def match_for_chapter(db_path: str, chapter: int, top_n: int,
                      book_slug: str | None, weights: tuple[float, float, float, float],
                      use_fr_chapter: bool = False):
    w1, w2, w3, w4 = weights
    print(f"\n{'='*70}")
    print(f"  匹配: Familia Romana Cap. {chapter}")
    print(f"  权重: known_cov={w1}, weighted_new={w2}, new_density={w3}, hf_bonus={w4}")
    print(f"{'='*70}")

    known, new = load_chapter_vocab(db_path, chapter)
    print(f"  [输入] 已知词 (Cap. 1-{chapter-1}): {len(known)} 个")
    print(f"  [输入] 新词 (Cap. {chapter} 引入):  {len(new)} 个")
    if new:
        sample_new = sorted(list(new))[:15]
        print(f"  [输入] 新词样本: {', '.join(sample_new)}{'...' if len(new) > 15 else ''}")

    # fr_chapter 过滤：优先加载 fr_chapter 匹配的段，无结果则回退
    if use_fr_chapter:
        candidates = load_candidate_segments(db_path, book_slug, fr_chapter_filter=chapter)
        if not candidates:
            print(f"  [警告] fr_chapter={chapter} 过滤后无候选段，回退到全量搜索")
            candidates = load_candidate_segments(db_path, book_slug)
        else:
            print(f"  [fr_chapter 过滤模式] 候选段数: {len(candidates)}")
    else:
        candidates = load_candidate_segments(db_path, book_slug)
        print(f"  [候选] 候选段落总数: {len(candidates)}")

    # 打分 (v1.6.0: 高频新词加权)
    scored = []
    for seg in candidates:
        seg_words = load_segment_vocab(db_path, seg["id"])
        sc = score_segment(seg_words, known, new, w1, w2, w3, w4)
        seg_meta = {
            **seg,
            "score": sc["score"],
            "known_cov": sc["known_cov"],
            "new_hits": sc["new_hits"],
            "hf_new_hits": sc["hf_new_hits"],
            "weighted_new_hits": sc["weighted_new_hits"],
            "new_den": sc["new_den"],
        }
        scored.append(seg_meta)

    # 排序
    scored.sort(key=lambda x: x["score"], reverse=True)

    # 输出 top N
    print(f"\n  Top {top_n} 推荐段落:")
    print(f"  {'排名':<4} {'分数':<6} {'已知覆盖':<10} {'新词命中':<12} {'高频新词':<10} {'新词密度':<10} {'书名':<25} {'段名'}")
    print(f"  {'-'*4} {'-'*6} {'-'*10} {'-'*12} {'-'*10} {'-'*10} {'-'*25} {'-'*20}")
    for i, seg in enumerate(scored[:top_n], 1):
        print(f"  {i:<4} {seg['score']:.3f}  "
              f"{seg['known_cov']*100:>5.1f}%    "
              f"{seg['new_hits']:>3d}/{len(new):<3d}  "
              f"{seg['hf_new_hits']:>3d}        "
              f"{seg['new_den']*100:>5.1f}%    "
              f"{seg['book_title'][:23]:<25} "
              f"{seg['title']}")

    return scored[:top_n]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--chapter", type=int, nargs="+", required=True,
                        help="目标章号, 可多个 (e.g. --chapter 8 9 10 11 12 13 25)")
    parser.add_argument("--top-n", type=int, default=3)
    parser.add_argument("--book", help="限定某一本书的段 (默认所有书)")
    parser.add_argument("--w1", type=float, default=0.4, help="known_coverage 权重")
    parser.add_argument("--w2", type=float, default=0.4, help="new_hits 加权后权重 (高频 2x)")
    parser.add_argument("--w3", type=float, default=0.2, help="new_density 权重")
    parser.add_argument("--w4", type=float, default=0.2, help="高频新词专项加权 (推荐 0.2-0.3)")
    parser.add_argument("--use-fr-chapter", action="store_true",
                        help="启用 fr_chapter 过滤：只搜索 fr_chapter 匹配目标章的段，"
                             "过滤后无结果则自动回退到全量搜索")
    args = parser.parse_args()

    if not any([args.w1, args.w2, args.w3, args.w4]):
        print("  [错误] 权重不能全为 0", file=sys.stderr)
        sys.exit(1)

    weights = (args.w1, args.w2, args.w3, args.w4)

    for ch in args.chapter:
        match_for_chapter(args.db, ch, args.top_n, args.book, weights,
                          use_fr_chapter=args.use_fr_chapter)


if __name__ == "__main__":
    main()
