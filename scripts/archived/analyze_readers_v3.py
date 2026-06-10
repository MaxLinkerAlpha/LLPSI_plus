#!/usr/bin/env python3
"""
analyze_readers_v3.py — 基于词频 + LLPSI 章节匹配 的新评级

对每本 OCR 完成的读物:
  1. 提取 unique Latin words
  2. 计算每章 FR/RA 已知词覆盖率
  3. 找"最佳锚点章节" (>= 80% 已知词覆盖率的最早章节)
  4. 输出 vocab_stats + chapter_anchor + new_words 等

输入:
  - ocr_output/<slug>/_full.txt
  - data/llpsi_corpus.db (fr_vocab 表)

输出:
  - analysis_output/reader_vocab_stats.json
  - analysis_output/reader_vocab_stats.csv
"""
import csv
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR_OUT = ROOT / "ocr_output"
DB_PATH = ROOT / "data" / "llpsi_corpus.db"
JSON_OUT = ROOT / "analysis_output" / "reader_vocab_stats.json"
CSV_OUT = ROOT / "analysis_output" / "reader_vocab_stats.csv"

# 与 ingest_to_db.py 完全一致的拉丁词提取规则
WORD_RE = re.compile(
    r"[A-Za-zÄäÀàÁáÂâÆæÇçÉéÈèÊêĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž]+"
)
LATIN_RE = re.compile(r"^[a-zāēīōūȳ]+$")

# 排除已在 corpus 的 LLPSI 官方读物 (避免重复统计)
OFFICIAL_SLUGS = {
    "aeneis", "amphitryo", "ars_amatoria", "catilina", "cena_trimalchionis",
    "colloquia_personarum", "de_bello_gallico", "de_rerum_natura",
    "epitome_historiae_sacrae", "fabellae_latinae", "fabulae_syrae",
    "roma_aeterna", "sermones_romani", "familia_romana",
}

# 排除用户已删除的书籍
DELETED_SLUGS = {"nunc_loquamur", "probe", "backup_v150_20260606_113934"}


def extract_latin_words(text: str) -> list[str]:
    """提取拉丁词形 (lowercased). 与 ingest_to_db.py 保持一致."""
    words = [w.lower() for w in WORD_RE.findall(text)]
    # 过滤: 长度 > 1 + 严格拉丁字符
    return [w for w in words if len(w) > 1 and LATIN_RE.match(w)]


def load_chapter_vocab(db_path: str) -> dict[int, set[str]]:
    """从 fr_vocab 表加载每章的已知词集合 (累计到该章)."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 加载每章的新词
    cur.execute("SELECT chapter, word_form FROM fr_vocab WHERE is_new=1")
    rows = cur.fetchall()
    conn.close()

    chapter_new = {}
    for ch, w in rows:
        chapter_new.setdefault(ch, set()).add(w)

    # 累加: chapter N 的 known = chapter 1..N 的所有新词
    sorted_chapters = sorted(chapter_new.keys())
    known = set()
    chapter_known = {}
    for ch in sorted_chapters:
        known.update(chapter_new[ch])
        chapter_known[ch] = set(known)
    return chapter_known


def find_best_anchor(unique_words: set[str],
                     chapter_known: dict[int, set[str]],
                     min_coverage: float = 0.80) -> dict:
    """找最佳锚点章节: 最早达到 >= min_coverage 已知覆盖的章节."""
    if not unique_words:
        return {"anchor_chapter": None, "anchor_coverage": 0, "coverage_by_chapter": {}}

    coverage_by_ch = {}
    sorted_chapters = sorted(chapter_known.keys())
    anchor_ch = None
    anchor_cov = 0.0
    for ch in sorted_chapters:
        known = chapter_known[ch]
        covered = len(unique_words & known)
        cov = covered / len(unique_words)
        coverage_by_ch[ch] = round(cov, 4)
        if cov >= min_coverage and anchor_ch is None:
            anchor_ch = ch
            anchor_cov = cov
    return {
        "anchor_chapter": anchor_ch,
        "anchor_coverage": round(anchor_cov, 4) if anchor_ch else 0,
        "coverage_by_chapter": coverage_by_ch,
    }


def is_dominant_latin(unique_words: set[str],
                      coverage_post_35: float = 0.10) -> tuple[bool, str]:
    """判定语言主类型: 基于 FR 全部已知词覆盖率 + 后 FR (RA 36-56) 已知词覆盖率.

    Returns (is_latin_dominant, verdict).
    """
    # 这里简化: 如果 unique_words 中有 >50% 是 FR 已知词, 视为主体拉语
    # 如果 <10% 是 FR 已知词, 视为英语为主
    return True, "see_coverage"  # 通过 coverage_by_chapter 数据分析


def analyze_one_book(slug: str, chapter_known: dict[int, set[str]]) -> dict | None:
    """分析单本书."""
    full = OCR_OUT / slug / "_full.txt"
    if not full.exists():
        return None
    text = full.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return None

    words = extract_latin_words(text)
    if not words:
        return None

    word_count = len(words)
    unique = set(words)
    unique_count = len(unique)

    # 章节锚点
    anchor = find_best_anchor(unique, chapter_known, min_coverage=0.80)
    # 60% 锚点
    anchor_60 = find_best_anchor(unique, chapter_known, min_coverage=0.60)
    # 95% 锚点
    anchor_95 = find_best_anchor(unique, chapter_known, min_coverage=0.95)

    # 在 Cap.1 (即 0 章) 的已知词覆盖率
    cap0_cov = anchor["coverage_by_chapter"].get(1, 0)
    cap5_cov = anchor["coverage_by_chapter"].get(5, 0)
    cap10_cov = anchor["coverage_by_chapter"].get(10, 0)
    cap15_cov = anchor["coverage_by_chapter"].get(15, 0)
    cap20_cov = anchor["coverage_by_chapter"].get(20, 0)
    cap25_cov = anchor["coverage_by_chapter"].get(25, 0)
    cap30_cov = anchor["coverage_by_chapter"].get(30, 0)
    cap35_cov = anchor["coverage_by_chapter"].get(35, 0)
    cap56_cov = anchor["coverage_by_chapter"].get(56, 0)

    # 类型判定
    # 1. 纯拉语 (post-35 覆盖率 > 30% 而 Cap.1 覆盖率 < 30%): RA 之后的进阶
    # 2. 早期拉语 (Cap.1-10 覆盖率 > 60%): 入门
    # 3. 中期拉语 (Cap.15-25 覆盖率 > 60%): 中级
    # 4. 高级拉语 (Cap.30+ 覆盖率 > 60%): 高级
    # 5. 教材 (Cap.1 覆盖率低, 但有大量词汇) - 教学内容
    # 6. 英语为主: < 10% 是拉丁词

    if unique_count < 200:
        verdict = "low_content"  # 几乎无内容
    elif cap56_cov < 0.10:
        verdict = "english_dominant"
    else:
        if anchor["anchor_chapter"] is not None and anchor["anchor_chapter"] <= 10:
            verdict = "early_reader"  # FR Cap.1-10 可读
        elif anchor["anchor_chapter"] is not None and anchor["anchor_chapter"] <= 20:
            verdict = "mid_early_reader"  # FR Cap.10-20 可读
        elif anchor["anchor_chapter"] is not None and anchor["anchor_chapter"] <= 30:
            verdict = "mid_reader"  # FR Cap.20-30 可读
        elif anchor["anchor_chapter"] is not None and anchor["anchor_chapter"] <= 45:
            verdict = "advanced_reader"  # FR Cap.30-45 (RA) 可读
        else:
            verdict = "post_45_reader"  # RA 后段可读

    return {
        "slug": slug,
        "total_words": word_count,
        "unique_words": unique_count,
        "verdict": verdict,
        "anchor_80": anchor["anchor_chapter"],
        "anchor_80_coverage": anchor["anchor_coverage"],
        "anchor_60": anchor_60["anchor_chapter"],
        "anchor_95": anchor_95["anchor_chapter"],
        "cov_cap_1": round(cap0_cov, 4),
        "cov_cap_5": round(cap5_cov, 4),
        "cov_cap_10": round(cap10_cov, 4),
        "cov_cap_15": round(cap15_cov, 4),
        "cov_cap_20": round(cap20_cov, 4),
        "cov_cap_25": round(cap25_cov, 4),
        "cov_cap_30": round(cap30_cov, 4),
        "cov_cap_35": round(cap35_cov, 4),
        "cov_cap_56": round(cap56_cov, 4),
    }


def main() -> int:
    print(f"=== 读物词频 + LLPSI 章节匹配分析 (v3) ===")
    print(f"DB: {DB_PATH}")
    print(f"OCR 输出: {OCR_OUT}")
    print()

    # 加载 fr_vocab
    chapter_known = load_chapter_vocab(DB_PATH)
    print(f"[fr_vocab] 加载 {len(chapter_known)} 章节累计已知词")
    print(f"  Cap.1 已知词: {len(chapter_known.get(1, set()))} 个")
    print(f"  Cap.10 已知词: {len(chapter_known.get(10, set()))} 个")
    print(f"  Cap.20 已知词: {len(chapter_known.get(20, set()))} 个")
    print(f"  Cap.35 已知词: {len(chapter_known.get(35, set()))} 个")
    print(f"  Cap.56 (RA end) 已知词: {len(chapter_known.get(56, set()))} 个")
    print()

    # 扫描所有已 OCR 完成的书籍
    all_slugs = sorted([p.parent.name for p in OCR_OUT.glob("*/_full.txt")
                        if p.stat().st_size > 100])
    print(f"[扫描] 找到 {len(all_slugs)} 本已 OCR 完成的书籍")

    # 过滤
    filtered = [s for s in all_slugs
                if s not in OFFICIAL_SLUGS and s not in DELETED_SLUGS]
    skipped_official = [s for s in all_slugs if s in OFFICIAL_SLUGS]
    skipped_deleted = [s for s in all_slugs if s in DELETED_SLUGS]
    print(f"  官方读物 (跳过): {len(skipped_official)}: {', '.join(skipped_official[:5])}...")
    print(f"  用户已删 (跳过): {len(skipped_deleted)}: {', '.join(skipped_deleted)}")
    print(f"  待分析: {len(filtered)}")
    print()

    results = []
    for slug in filtered:
        r = analyze_one_book(slug, chapter_known)
        if r:
            results.append(r)
            anchor = r["anchor_80"] or "—"
            cov = r["anchor_80_coverage"]
            v = r["verdict"]
            print(f"  [{v:20s}] {slug:30s} 词={r['total_words']:>6,} 独="
                  f"{r['unique_words']:>5,} 锚点 Cap.{anchor} ({cov*100:>5.1f}%) "
                  f"Cov@35={r['cov_cap_35']*100:>5.1f}%")

    # 保存 JSON
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[JSON] {JSON_OUT}")

    # 保存 CSV
    with open(CSV_OUT, "w", encoding="utf-8") as f:
        f.write("slug,verdict,total_words,unique_words,anchor_80,anchor_80_cov,"
                "anchor_60,anchor_95,"
                "cov_cap_1,cov_cap_5,cov_cap_10,cov_cap_15,cov_cap_20,cov_cap_25,"
                "cov_cap_30,cov_cap_35,cov_cap_56\n")
        for r in results:
            f.write(f"{r['slug']},{r['verdict']},{r['total_words']},"
                    f"{r['unique_words']},{r['anchor_80'] or ''},"
                    f"{r['anchor_80_coverage']},{r['anchor_60'] or ''},"
                    f"{r['anchor_95'] or ''},"
                    f"{r['cov_cap_1']},{r['cov_cap_5']},{r['cov_cap_10']},"
                    f"{r['cov_cap_15']},{r['cov_cap_20']},{r['cov_cap_25']},"
                    f"{r['cov_cap_30']},{r['cov_cap_35']},{r['cov_cap_56']}\n")
    print(f"[CSV]  {CSV_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
