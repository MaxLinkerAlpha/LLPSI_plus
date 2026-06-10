#!/usr/bin/env python3
"""
build_chapter_stats_unified.py — 全面重算LLPSI 56章核心数据

输出: analysis_output/llpsi_chapter_stats.json
  {
    "fr_35_chapters": [...],   // FR Cap.1-35
    "ra_21_chapters": [...],   // RA Cap.36-56
    "summary": {...},
  }
"""
import csv
import json
import sqlite3
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
DB = ROOT / "data" / "llpsi_corpus.db"
FR_CSV = ROOT / "analysis_output" / "chapter_stats.csv"
RA_CSV = ROOT / "analysis_output" / "roma_aeterna_chapter_stats.csv"
OUT = ROOT / "analysis_output" / "llpsi_chapter_stats.json"


def load_csv(p: Path) -> list[dict]:
    rows = []
    with p.open(encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            r["章节"] = int(r["章节"])
            r["总词数"] = int(r["总词数"])
            r["新词数"] = int(r["新词数"])
            r["新词密度(%)"] = float(r["新词密度(%)"])
            r["累计词汇"] = int(r["累计词汇"])
            r["高频新词"] = int(r["高频新词"])
            rows.append(r)
    return rows


def load_fr_vocab_stats() -> dict[int, dict]:
    """直接从数据库查 fr_vocab, 统计每章 unique_words / new_words."""
    conn = sqlite3.connect(str(DB))
    cur = conn.cursor()
    cur.execute("""
        SELECT chapter,
               COUNT(*) as n_total,
               SUM(is_new) as n_new
        FROM fr_vocab
        GROUP BY chapter
        ORDER BY chapter;
    """)
    out = {}
    for ch, n_total, n_new in cur.fetchall():
        out[ch] = {
            "n_total": n_total,
            "n_new": n_new or 0,
        }
    conn.close()
    return out


def main() -> int:
    print("=== LLPSI 56 章核心数据重算 (DB为主, CSV为参考) ===")

    fr_csv = load_csv(FR_CSV)
    ra_csv = load_csv(RA_CSV)
    fr_db = load_fr_vocab_stats()

    # 以 DB 数据为主: unique word_form (词形)
    # CSV 数据为参考: unique word family (词族, 含变体)
    # 这两个数都是正确的, 只是统计粒度不同, 需在报告中说明

    # 合并 FR Cap.1-35
    fr_chapters = []
    db_cum = 0
    for r in fr_csv:
        ch = r["章节"]
        db_data = fr_db.get(ch, {})
        db_cum += db_data.get("n_new", 0)
        fr_chapters.append({
            "chapter": ch,
            "book": "FR",
            "title_roman": roman(ch),
            # 来自CSV (含未去重)
            "total_words_in_chapter": r["总词数"],   # 课文中该章的总词数 (含已学)
            "new_word_count_csv": r["新词数"],       # CSV统计的新词数
            "new_density_csv": r["新词密度(%)"],     # CSV新词密度
            "cumulative_vocab_csv": r["累计词汇"],   # CSV累计词族
            "high_freq_new": r["高频新词"],
            # 来自DB (去重)
            "db_total_records": db_data.get("n_total", 0),
            "db_new_records": db_data.get("n_new", 0),
            "cumulative_vocab_db": db_cum,           # DB累计unique word_form
        })

    # 校正: 优先使用 DB 的累计作为"FR末章词汇量"基准
    # 因为 reader analysis (analyze_readers_v5.py) 用的是 DB 的 fr_vocab
    fr_final_db = fr_chapters[-1]["cumulative_vocab_db"] if fr_chapters else 0
    fr_final_csv = fr_chapters[-1]["cumulative_vocab_csv"] if fr_chapters else 0

    # 合并 RA Cap.36-56
    ra_chapters = []
    for i, r in enumerate(ra_csv):
        ch = r["章节"]
        ra_chapters.append({
            "chapter": ch,
            "book": "RA",
            "title_roman": roman(ch),
            "total_words_in_chapter": r["总词数"],
            "new_word_count_csv": r["新词数"],
            "new_density_csv": r["新词密度(%)"],
            "cumulative_vocab_csv": fr_final_csv + sum(c["new_word_count_csv"] for c in ra_chapters[:i]) + r["新词数"],
            "cumulative_vocab_db": fr_final_db + sum(c.get("new_word_count_csv", 0) for c in ra_chapters[:i]) + r["新词数"],  # 用CSV新词数近似
            "high_freq_new": r["高频新词"],
        })

    # 汇总
    summary = {
        "fr_total_chapters": len(fr_chapters),
        "ra_total_chapters": len(ra_chapters),
        "fr_total_words": sum(c["total_words_in_chapter"] for c in fr_chapters),
        "ra_total_words": sum(c["total_words_in_chapter"] for c in ra_chapters),
        # 主要数据: 词形 (DB)
        "fr_cum_vocab_wordform": fr_final_db,
        "ra_cum_vocab_wordform": ra_chapters[-1]["cumulative_vocab_db"] if ra_chapters else 0,
        # 参考数据: 词族 (CSV)
        "fr_cum_vocab_wordfamily": fr_final_csv,
        "ra_cum_vocab_wordfamily": ra_chapters[-1]["cumulative_vocab_csv"] if ra_chapters else 0,
        # 平均密度
        "fr_avg_new_density": round(sum(c["new_density_csv"] for c in fr_chapters) / len(fr_chapters), 2) if fr_chapters else 0,
        "ra_avg_new_density": round(sum(c["new_density_csv"] for c in ra_chapters) / len(ra_chapters), 2) if ra_chapters else 0,
        # 最难章
        "fr_hardest_chapter": max(fr_chapters, key=lambda c: c["new_density_csv"]),
        "ra_hardest_chapter": max(ra_chapters, key=lambda c: c["new_density_csv"]),
    }
    summary["fr_hardest_chapter"] = {
        "chapter": summary["fr_hardest_chapter"]["chapter"],
        "new_density": summary["fr_hardest_chapter"]["new_density_csv"],
    }
    summary["ra_hardest_chapter"] = {
        "chapter": summary["ra_hardest_chapter"]["chapter"],
        "new_density": summary["ra_hardest_chapter"]["new_density_csv"],
    }

    out = {
        "fr_35_chapters": fr_chapters,
        "ra_21_chapters": ra_chapters,
        "summary": summary,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUT}")
    print()
    print("=== 汇总 ===")
    print(f"FR: {summary['fr_total_chapters']}章, {summary['fr_total_words']:,}总词, "
          f"末章累计 {summary['fr_cum_vocab_wordform']:,} 词形 / {summary['fr_cum_vocab_wordfamily']:,} 词族")
    print(f"RA: {summary['ra_total_chapters']}章, {summary['ra_total_words']:,}总词, "
          f"末章累计 {summary['ra_cum_vocab_wordform']:,} 词形 / {summary['ra_cum_vocab_wordfamily']:,} 词族")
    print(f"FR平均新词密度: {summary['fr_avg_new_density']}%")
    print(f"RA平均新词密度: {summary['ra_avg_new_density']}%")
    print(f"FR最难章: Cap.{summary['fr_hardest_chapter']['chapter']} (密度 {summary['fr_hardest_chapter']['new_density']}%)")
    print(f"RA最难章: Cap.{summary['ra_hardest_chapter']['chapter']} (密度 {summary['ra_hardest_chapter']['new_density']}%)")


def roman(n: int) -> str:
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    result = ""
    for v, s in vals:
        while n >= v:
            result += s
            n -= v
    return result


if __name__ == "__main__":
    import sys
    sys.exit(main())
