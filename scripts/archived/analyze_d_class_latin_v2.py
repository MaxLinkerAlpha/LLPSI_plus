#!/usr/bin/env python3
"""
analyze_d_class_latin_v2.py — D类教材拉语段的LLPSI章节锚点分析

对每个D类教材的拉语故事段(start_page..end_page), 提取该段OCR文本, 做:
1. 词汇量统计 (拉词数、独词数、英语过滤后)
2. LLPSI章节锚点: 学完哪章后可读 (50%/60%阈值)
3. 教学价值: 这段覆盖了哪章的新词最多

输入:
  - analysis_output/d_class_latin_stories.json (来自 extract_d_class_latin.py)
  - ocr_output/<slug>/page_NNN.txt
  - data/llpsi_corpus.db (fr_vocab 表)

输出:
  - analysis_output/d_segments_vocab.json
  - analysis_output/d_segments_vocab.md
"""
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Optional

# 复用 v4 脚本的常量与函数
sys.path.insert(0, str(Path(__file__).parent))
from analyze_readers_v4 import (
    OCR_OUT, DB_PATH,
    WORD_RE, LATIN_RE,
    extract_latin_words, filter_to_latin_only,
    load_fr_vocab,
    OFFICIAL_SLUGS, DELETED_SLUGS,
)

ROOT = Path(__file__).resolve().parent.parent
SEGMENTS_JSON = ROOT / "analysis_output" / "d_class_latin_stories.json"
OUT_JSON = ROOT / "analysis_output" / "d_segments_vocab.json"
OUT_MD = ROOT / "analysis_output" / "d_segments_vocab.md"


def get_segment_text(slug: str, start_page: int, end_page: int) -> str:
    """提取指定slug的start_page..end_page之间所有OCR文本."""
    texts = []
    slug_dir = OCR_OUT / slug
    if not slug_dir.exists():
        return ""
    for pn in range(start_page, end_page + 1):
        p = slug_dir / f"page_{pn:03d}.txt"
        if p.exists():
            texts.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(texts)


def analyze_segment(slug: str, story: dict,
                    chapter_known: dict[int, set[str]],
                    chapter_new: dict[int, set[str]]) -> dict:
    """分析单个拉语段."""
    start = story["start_page"]
    end = story["end_page"]
    page_count = story["page_count"]

    text = get_segment_text(slug, start, end)
    if not text.strip():
        return {
            "slug": slug,
            "start_page": start,
            "end_page": end,
            "page_count": page_count,
            "status": "empty_text",
        }

    all_words = extract_latin_words(text)
    if not all_words:
        return {
            "slug": slug,
            "start_page": start,
            "end_page": end,
            "page_count": page_count,
            "status": "no_latin",
        }

    latin_words, english_filtered = filter_to_latin_only(all_words)
    total_words = len(all_words)
    latin_word_count = len(latin_words)
    english_word_count = english_filtered
    unique_latin = set(latin_words)
    unique_latin_count = len(unique_latin)

    # 视角1: 起点章节 (50%/60% 阈值)
    starting_50 = None
    starting_60 = None
    coverage_by_ch = {}
    for ch in sorted(chapter_known.keys()):
        known = chapter_known[ch]
        cov = len(unique_latin & known) / unique_latin_count if unique_latin_count else 0
        coverage_by_ch[ch] = round(cov, 4)
        if starting_50 is None and cov >= 0.50:
            starting_50 = ch
        if starting_60 is None and cov >= 0.60:
            starting_60 = ch

    peak_cov = max(coverage_by_ch.values()) if coverage_by_ch else 0
    peak_ch = max(coverage_by_ch.items(), key=lambda x: x[1])[0] if coverage_by_ch else None

    # 视角2: 教学价值
    new_word_cov = {}
    for ch, new_set in chapter_new.items():
        if not new_set:
            continue
        hits = len(new_set & unique_latin)
        new_word_cov[ch] = round(hits / len(new_set), 4)
    if new_word_cov:
        best_teach_ch, best_teach_cov = max(new_word_cov.items(), key=lambda x: x[1])
    else:
        best_teach_ch, best_teach_cov = None, 0

    return {
        "slug": slug,
        "start_page": start,
        "end_page": end,
        "page_count": page_count,
        "status": "ok",
        "total_words": total_words,
        "latin_word_count": latin_word_count,
        "english_word_count": english_word_count,
        "english_ratio": round(english_word_count / total_words, 4) if total_words else 0,
        "unique_latin_count": unique_latin_count,
        "starting_chapter_50": starting_50,
        "starting_chapter_60": starting_60,
        "peak_chapter": peak_ch,
        "peak_coverage": round(peak_cov, 4),
        "best_teach_chapter": best_teach_ch,
        "best_teach_coverage": round(best_teach_cov, 4),
        "coverage_by_chapter": coverage_by_ch,
    }


def main() -> int:
    print(f"=== D类教材拉语段 LLPSI 章节锚点分析 ===")

    if not SEGMENTS_JSON.exists():
        print(f"[错误] {SEGMENTS_JSON} 不存在. 请先运行 extract_d_class_latin.py")
        return 1

    segments_data = json.loads(SEGMENTS_JSON.read_text(encoding="utf-8"))
    chapter_known, chapter_new = load_fr_vocab(str(DB_PATH))
    print(f"[词表] LLPSI 56 章节加载完成 (Cap.56 共 {len(chapter_known.get(56, set()))} 已知词)")
    print(f"[段落] {segments_data['books_with_latin_stories']} 本含拉语段, 共 {segments_data['total_latin_story_pages']} 页")
    print()

    # 汇总所有segments
    all_segments = []
    for book in segments_data["books"]:
        slug = book["slug"]
        for story in book.get("stories", []):
            if story["page_count"] < 3:
                continue
            seg = analyze_segment(slug, story, chapter_known, chapter_new)
            seg["book_title"] = book.get("slug")  # 占位, 报告里再加
            all_segments.append(seg)

    # 输出
    OUT_JSON.write_text(
        json.dumps({
            "total_segments": len(all_segments),
            "books": segments_data["books_with_latin_stories"],
            "total_pages": sum(s.get("page_count", 0) for s in all_segments),
            "segments": all_segments,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] {OUT_JSON} 已生成 ({len(all_segments)} 段)")

    # 简易md报告
    lines = ["# D类教材拉语段 LLPSI 章节锚点分析", ""]
    lines.append(f"分析日期: 2026-06-06 | 共 {len(all_segments)} 段 / {sum(s.get('page_count', 0) for s in all_segments)} 页")
    lines.append("")
    lines.append("## 评级指标")
    lines.append("")
    lines.append("- **起点50%/60%**: 学完 FR Cap.N 后, FR 已知词覆盖本段 50%/60% 拉语独词")
    lines.append("- **峰值章节**: 最高覆盖率的LLPSI章节")
    lines.append("- **教学价值**: 本段覆盖 FR Cap.N 新词最多的章节")
    lines.append("")
    lines.append("## 段汇总 (按页面数降序)")
    lines.append("")
    lines.append("| slug | 段起始页 | 页数 | 拉词 | 独词 | 英% | 起点50% | 起点60% | 峰值章节 | 教学价值 |")
    lines.append("|------|---------:|----:|-----:|----:|----:|--------:|--------:|---------:|----------|")

    for s in sorted(all_segments, key=lambda x: -x.get("page_count", 0)):
        s50 = f"Cap.{s['starting_chapter_50']}" if s.get("starting_chapter_50") else "—"
        s60 = f"Cap.{s['starting_chapter_60']}" if s.get("starting_chapter_60") else "—"
        pk = f"Cap.{s['peak_chapter']}({s['peak_coverage']:.0%})" if s.get("peak_chapter") else "—"
        tc = f"Cap.{s['best_teach_chapter']}({s['best_teach_coverage']:.0%})" if s.get("best_teach_chapter") else "—"
        en = s.get("english_ratio", 0)
        uw = s.get("unique_latin_count", 0)
        lw = s.get("latin_word_count", 0)
        lines.append(
            f"| {s['slug']} | p.{s['start_page']} | {s['page_count']} | "
            f"{lw} | {uw} | {en:.0%} | {s50} | {s60} | {pk} | {tc} |"
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {OUT_MD} 已生成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
