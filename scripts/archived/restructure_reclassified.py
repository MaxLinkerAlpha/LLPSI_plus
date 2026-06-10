#!/usr/bin/env python3
"""
restructure_reclassified.py — 抛弃 A1/A2/B1/B2 标签, 改为按"学完LLPSI哪章可读"分章

新结构:
  source/Other_Readers/reclassified_v2/
    0_cap1-15_入门/      (FR入门期后可用, 0本)
    1_cap16-25_初级/     (FR初级后可用, 5本)
    2_cap26-35_FR中级/   (FR中级后可用, 18本)
    3_cap36-45_RA前/     (RA前段后可用, 20本)
    4_cap46-56_RA后/     (RA后段后可用, 11本)
    5_reference_查阅/    (查阅使用, 1本)
    6_d_segments_D类拉语段/  (D类教材拉语段, 35段/162页)

每本书按其 reading_level_chapter 决定归属:
  - fluent / challenging / selected 级别都按起点章节归到对应目录
  - reference 级别归到 5_reference_查阅
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
OLD = ROOT / "source" / "Other_Readers" / "reclassified"
NEW = ROOT / "source" / "Other_Readers" / "reclassified_v2"
DATA = ROOT / "analysis_output" / "reader_vocab_stats_v4.json"
D_SEGS = ROOT / "analysis_output" / "d_segments_vocab.json"

STAGE_DIRS = {
    "FR Cap.1-15 入门期":   "0_cap1-15_入门",
    "FR Cap.16-25 初级期":  "1_cap16-25_初级",
    "FR Cap.26-35 中级期":  "2_cap26-35_FR中级",
    "RA Cap.36-45 高级期":  "3_cap36-45_RA前",
    "RA Cap.46-56 完成期":  "4_cap46-56_RA后",
    "未达(查阅使用)":       "5_reference_查阅",
}


def find_pdf_for_slug(slug: str) -> Path | None:
    """在 source/Other_Readers/ 下递归查找与slug匹配的PDF/EPUB文件."""
    base = ROOT / "source" / "Other_Readers"
    # 1. 直接匹配文件名
    for ext in (".pdf", ".epub"):
        direct = base / f"{slug}{ext}"
        if direct.exists():
            return direct
    # 2. 在 reclassified/ 中找旧软链
    if OLD.exists():
        for sub in OLD.iterdir():
            if not sub.is_dir():
                continue
            for ext in (".pdf", ".epub"):
                link = sub / f"{slug}{ext}"
                if link.is_symlink():
                    target = link.resolve()
                    if target.exists():
                        return target
    # 3. 模糊匹配
    candidates = []
    for p in base.rglob("*.*"):
        if p.suffix.lower() not in (".pdf", ".epub"):
            continue
        if slug.replace("_", " ").lower() in p.name.lower().replace("_", " "):
            candidates.append(p)
        first = slug.split("_")[0]
        if len(first) >= 4 and first in p.name.lower():
            candidates.append(p)
    if candidates:
        return sorted(candidates, key=lambda p: len(p.name))[0]
    return None


def main() -> int:
    if NEW.exists():
        shutil.rmtree(NEW)
    NEW.mkdir(parents=True)

    data = json.loads(DATA.read_text(encoding="utf-8"))
    by_slug = {d["slug"]: d for d in data}

    # 创建所有阶段目录
    for stage, dir_name in STAGE_DIRS.items():
        (NEW / dir_name).mkdir(parents=True, exist_ok=True)

    # 处理所有55本
    moved = 0
    missing = []
    stage_counts = {}
    for d in sorted(data, key=lambda x: (x.get("reading_level_chapter") or 999, x["slug"])):
        slug = d["slug"]
        stage = d.get("stage", "未达(查阅使用)")
        dir_name = STAGE_DIRS.get(stage, "5_reference_查阅")

        target = find_pdf_for_slug(slug)
        if not target:
            missing.append(slug)
            continue
        # 跳过 ecce_romani_combined (EPUB, 已丢弃)
        if slug == "ecce_romani_combined":
            continue

        dest_dir = NEW / dir_name
        dest_link = dest_dir / f"{slug}.pdf"
        if dest_link.exists() or dest_link.is_symlink():
            dest_link.unlink()
        # 相对软链
        try:
            rel = target.relative_to(ROOT)
            dest_link.symlink_to(Path("..") / ".." / ".." / rel)
        except ValueError:
            dest_link.symlink_to(target)
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
        moved += 1

    # D类拉语段目录
    segs_dir = NEW / "6_d_segments_D类拉语段"
    segs_dir.mkdir(parents=True, exist_ok=True)
    if D_SEGS.exists():
        segs = json.loads(D_SEGS.read_text(encoding="utf-8"))
        (segs_dir / "d_segments_index.json").write_text(
            json.dumps(segs, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # 输出统计
    print(f"=== 重新分类完成 ===")
    print(f"已移动: {moved} 本")
    if missing:
        print(f"未找到PDF: {missing}")
    print(f"输出目录: {NEW}")
    print()
    print("各阶段数量:")
    for stage, dir_name in STAGE_DIRS.items():
        count = stage_counts.get(stage, 0)
        print(f"  {dir_name}: {count} 本")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
