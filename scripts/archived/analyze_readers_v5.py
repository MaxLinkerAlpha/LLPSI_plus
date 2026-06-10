#!/usr/bin/env python3
"""
analyze_readers_v5.py — 在 v4 基础上加入 4 档可读性分级

新增指标:
  - reading_level: 4档可读性
    - "fluent"        60%+ 覆盖 (可通读, 仅需少量注释)
    - "challenging"   40-60% 覆盖 (需配合注释/字典)
    - "selected"      20-40% 覆盖 (仅节选/对照可读)
    - "reference"     <20% 覆盖 (查阅/参考使用)
  - reading_level_chapter: 该档达到的LLPSI章节

按用户要求: 不使用 A1/A2,改用"拉词量 + LLPSI章节锚点"
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from analyze_readers_v4 import (
    ROOT, OCR_OUT, JSON_OUT, CSV_OUT, MD_OUT, OFFICIAL_SLUGS, DELETED_SLUGS,
    analyze_one_book, load_fr_vocab, DB_PATH,
)


# 4档可读性: 基于"学完LLPSI Cap.N后, FR已知词能覆盖X%独词"
# 60%+: 顺畅可读; 40-60%: 有挑战; 20-40%: 节选; <20%: 查阅
# 注意: 返回 (threshold, name, desc) 与 v4 保持一致
THRESHOLDS = [
    (0.60, "fluent",      "顺畅可读 (FR已知词覆盖≥60%拉语独词)"),
    (0.40, "challenging", "有挑战可读 (覆盖40-60%, 需注释)"),
    (0.20, "selected",    "节选可读 (覆盖20-40%, 适合对照阅读)"),
    (0.00, "reference",   "查阅使用 (覆盖<20%, 适合词汇/语法查阅)"),
]


def assign_reading_level(book: dict) -> tuple[str, int | None, str, str]:
    """根据 coverage_by_chapter 找最早达到各档的章节.

    返回: (level_name, level_chapter, level_desc, level_range)
    """
    cov_by_ch = book.get("coverage_by_chapter", {})
    if not cov_by_ch:
        return ("reference", None,
                THRESHOLDS[-1][2],
                "N/A")

    for thresh, name, desc in THRESHOLDS[:-1]:  # 跳过 reference 档
        for ch in sorted(cov_by_ch.keys()):
            if cov_by_ch[ch] >= thresh:
                # 描述该档对应的覆盖率区间
                if thresh == 0.60:
                    range_str = f"≥60%"
                elif thresh == 0.40:
                    range_str = "40-60%"
                elif thresh == 0.20:
                    range_str = "20-40%"
                else:
                    range_str = "<20%"
                return (name, ch, desc, range_str)
    return ("reference", None, THRESHOLDS[-1][2], "<20%")


# 学习阶段分组 (用户核心需求: "学完LLPSI哪章可读")
STAGE_BOUNDARIES = [
    (1,  15, "FR Cap.1-15 入门期",  "入门"),
    (16, 25, "FR Cap.16-25 初级期", "初级"),
    (26, 35, "FR Cap.26-35 中级期", "FR中级"),
    (36, 45, "RA Cap.36-45 高级期", "RA前"),
    (46, 56, "RA Cap.46-56 完成期", "RA后"),
]


def assign_stage(chapter: int | None) -> str:
    """根据章节号返回学习阶段."""
    if chapter is None:
        return "未达(查阅使用)"
    for lo, hi, label, _ in STAGE_BOUNDARIES:
        if lo <= chapter <= hi:
            return label
    return f"Cap.{chapter}(超范围)"


def main() -> int:
    print(f"=== 读物词频 + LLPSI 章节锚点 v5 (4档可读性) ===")

    chapter_known, chapter_new = load_fr_vocab(str(DB_PATH))
    all_slugs = sorted([p.parent.name for p in OCR_OUT.glob("*/_full.txt")
                        if p.stat().st_size > 100])
    filtered = [s for s in all_slugs
                if s not in OFFICIAL_SLUGS and s not in DELETED_SLUGS]
    print(f"[扫描] {len(all_slugs)} 本, 过滤后 {len(filtered)} 本待分析")
    print()

    results = []
    for slug in filtered:
        r = analyze_one_book(slug, chapter_known, chapter_new)
        if r is None:
            continue
        # 4档可读性
        level, level_ch, level_desc, level_range = assign_reading_level(r)
        r["reading_level"] = level
        r["reading_level_chapter"] = level_ch
        r["reading_level_desc"] = level_desc
        r["reading_level_range"] = level_range
        r["stage"] = assign_stage(level_ch)
        # 各档起点章节 (用于路由表)
        r["ch20"] = r.get("starting_chapter_20")
        r["ch40"] = r.get("starting_chapter_40")
        r["ch50"] = r.get("starting_chapter_50")
        r["ch60"] = r.get("starting_chapter_60")
        r["ch70"] = r.get("starting_chapter_70")
        r["ch80"] = r.get("starting_chapter_80")
        results.append(r)

    # 输出 JSON
    JSON_OUT.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] {JSON_OUT} ({len(results)} 本)")

    # 输出 CSV
    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "slug", "level", "level_ch", "stage", "latin_words", "unique_latin",
            "english_pct", "peak_ch", "peak_cov", "teach_ch", "teach_cov",
            "start50", "start60",
        ])
        for r in sorted(results, key=lambda x: (
            x.get("reading_level_chapter") or 999,
            -x.get("unique_latin_count", 0))):
            w.writerow([
                r["slug"], r["reading_level"], r.get("reading_level_chapter"),
                r["stage"], r["latin_word_count"], r["unique_latin_count"],
                f"{r['english_ratio']:.0%}", r.get("peak_chapter"),
                f"{r['peak_coverage']:.0%}", r.get("best_teach_chapter"),
                f"{r['best_teach_coverage']:.0%}",
                r.get("starting_chapter_50") or "—",
                r.get("starting_chapter_60") or "—",
            ])
    print(f"[OK] {CSV_OUT}")

    # 输出 MD 报告
    lines = [
        "# 读物词频 + LLPSI 章节匹配 (v5 · 4档可读性)",
        "",
        f"分析日期: 2026-06-06 | 待分析: {len(results)} 本",
        "",
        "## 评价体系 (替代 A1/A2)",
        "",
        "**不**再使用 CEFR 的 A1/A2/B1/B2 分级. 改用**两个量化指标**:",
        "",
        "1. **可读起点** (`reading_level_chapter`): 学完 FR Cap.N 后, FR 已知词覆盖本书 X% 拉语独词的最早章节",
        "2. **教学价值** (`best_teach_chapter`): 本书覆盖 FR Cap.M 新词最多的章节 (高=适合复习该章新词)",
        "",
        "### 4 档可读性分级",
        "",
        "| 级别 | 覆盖率阈值 | 学习含义 |",
        "|------|-----------|---------|",
    ]
    for thresh, name, desc in THRESHOLDS:
        if thresh == 0.60:
            range_str = "≥60%"
        elif thresh == 0.40:
            range_str = "40-60%"
        elif thresh == 0.20:
            range_str = "20-40%"
        else:
            range_str = "<20%"
        lines.append(f"| **{name}** | {range_str} | {desc} |")
    lines += [
        "",
        "### 学习阶段分组",
        "",
        "| 阶段 | 章节范围 |",
        "|------|---------|",
    ]
    for lo, hi, label, _ in STAGE_BOUNDARIES:
        lines.append(f"| {label} | Cap.{lo}-Cap.{hi} |")
    lines.append("")

    # 统计
    from collections import Counter
    level_counts = Counter(r["reading_level"] for r in results)
    stage_counts = Counter(r["stage"] for r in results)

    lines += [
        "## 总体分布",
        "",
        "### 按可读性级别",
        "",
        "| 级别 | 数量 |",
        "|------|----:|",
    ]
    for _, name, _ in THRESHOLDS:
        lines.append(f"| {name} | {level_counts.get(name, 0)} |")
    lines += [
        "",
        "### 按学习阶段",
        "",
        "| 阶段 | 数量 |",
        "|------|----:|",
    ]
    for _, _, label, _ in STAGE_BOUNDARIES:
        lines.append(f"| {label} | {stage_counts.get(label, 0)} |")
    lines.append(f"| 未达 (查阅使用) | {stage_counts.get('未达(查阅使用)', 0)} |")
    lines.append("")

    # 详细表: 按可读性级别 + 起点章节排序
    lines += [
        "## 详细表 (按可读性级别 → 起点章节 → 拉词量 排序)",
        "",
        "| slug | 拉词 | 独词 | 英% | 级别 | 起点 | 教学价值 | 峰值 | 备注 |",
        "|------|----:|----:|----:|------|----:|---------|----:|------|",
    ]
    for r in sorted(results, key=lambda x: (
        ["fluent", "challenging", "selected", "reference"].index(x["reading_level"]),
        x.get("reading_level_chapter") or 999,
        -x.get("unique_latin_count", 0))):
        level_ch = r.get("reading_level_chapter")
        s_ch = f"Cap.{level_ch}" if level_ch else "—"
        tc = r.get("best_teach_chapter")
        s_tc = f"Cap.{tc}({r['best_teach_coverage']:.0%})" if tc else "—"
        pk = r.get("peak_chapter")
        s_pk = f"Cap.{pk}({r['peak_coverage']:.0%})" if pk else "—"
        en = r.get("english_ratio", 0)
        uw = r.get("unique_latin_count", 0)
        lw = r.get("latin_word_count", 0)
        lines.append(
            f"| `{r['slug']}` | {lw:,} | {uw:,} | {en:.0%} | "
            f"{r['reading_level']} | {s_ch} | {s_tc} | {s_pk} | {r['stage']} |"
        )

    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {MD_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
