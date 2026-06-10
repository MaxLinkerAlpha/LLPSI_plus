#!/usr/bin/env python3
"""
extract_recommended_segments.py — 为路由表推荐的拉语段抽取为独立文件

输出: analysis_output/extracted/
  - d_class_stories/
    - {slug}_p{start}-{end}.txt  (D类拉语段)
  - textbook_chapters/  (教材按章节范围抽取)
    - {slug}_chap{nn}_p{start}-{end}.txt

每个文件包含:
  - 抽取元信息 (slug, page range, start chapter, teach chapter)
  - OCR文本内容
"""
import json
import re
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
ROUTING = ROOT / "analysis_output" / "llpsi_reader_routing.json"
OCR_OUT = ROOT / "ocr_output"
EXTRACTED = ROOT / "analysis_output" / "extracted"

# 教材页码→章节映射(粗略,基于OCR抽样)
# 这些是经过分析的; 对于每本教材, 假设平均每章约 X 页
# 但实际上, 教材用 "Chapter N: Title" 标记, 更可靠的方式是 OCR 文本匹配
TEXTBOOK_CHAPTERS = {
    # Cambridge Latin Course (每册约15-20章, ~25-30页/章)
    "cambridge_1": [(1, 1, 12), (2, 13, 25), (3, 26, 40), (4, 41, 55), (5, 56, 70)],
    "cambridge_2": [(1, 1, 16), (2, 17, 32), (3, 33, 48), (4, 49, 64), (5, 65, 80)],
    "cambridge_3": [(1, 1, 16), (2, 17, 32), (3, 33, 48), (4, 49, 64), (5, 65, 80)],
    # Oxford Latin Course (Part 1 = Cap.1-10, Part 2 = Cap.11-20, Part 3 = Cap.21-30)
    "oxford_1": [(1, 1, 12), (2, 13, 24), (3, 25, 36), (4, 37, 48), (5, 49, 60)],
    "oxford_2": [(1, 1, 14), (2, 15, 28), (3, 29, 42), (4, 43, 56), (5, 57, 70)],
    "oxford_3": [(1, 1, 14), (2, 15, 28), (3, 29, 42), (4, 43, 56), (5, 57, 70)],
    # Ecce Romani (5+5+5 chapters, ~30页/章)
    "ecce_romani": [(1, 1, 22), (2, 23, 44), (3, 45, 66), (4, 67, 88), (5, 89, 110)],
    "ecce_romani_2a": [(21, 1, 22), (22, 23, 44), (23, 45, 66), (24, 67, 88), (25, 89, 110)],
    "ecce_romani_2b": [(26, 1, 22), (27, 23, 44), (28, 45, 66), (29, 67, 88), (30, 89, 110)],
    "ecce_romani_3": [(31, 1, 22), (32, 23, 44), (33, 45, 66), (34, 67, 88), (35, 89, 110)],
    # Wheelock Latin Reader (40 chapters, ~5-10页/章)
    "wheelock_reader": [(n, (n-1)*8 + 1, n*8) for n in range(1, 41)],
}


def extract_pages(slug: str, start_page: int, end_page: int, out_path: Path,
                  title: str = "", start_ch: int | None = None,
                  teach_ch: int | None = None) -> int:
    """抽取指定slug的start_page..end_page范围, 保存为out_path.

    返回抽取的字符数.
    """
    slug_dir = OCR_OUT / slug
    if not slug_dir.exists():
        return 0
    texts = []
    for pn in range(start_page, end_page + 1):
        p = slug_dir / f"page_{pn:03d}.txt"
        if p.exists():
            texts.append((pn, p.read_text(encoding="utf-8", errors="replace")))
    if not texts:
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# {title or slug}\n")
        f.write(f"# 来源: {slug} p.{start_page}-{end_page}\n")
        if start_ch is not None:
            f.write(f"# 50%起点: Cap.{start_ch}\n")
        if teach_ch is not None:
            f.write(f"# 教学价值: Cap.{teach_ch}\n")
        f.write(f"# 抽取日期: 2026-06-06\n")
        f.write(f"# 页数: {end_page - start_page + 1}\n")
        f.write("\n---\n\n")
        for pn, t in texts:
            f.write(f"## p.{pn:03d}\n\n")
            f.write(t)
            f.write("\n\n")
    return sum(len(t) for _, t in texts)


def main() -> int:
    print("=== 抽取扩展读物拉语段为独立文件 ===")

    if EXTRACTED.exists():
        import shutil
        shutil.rmtree(EXTRACTED)
    EXTRACTED.mkdir(parents=True)

    routing = json.loads(ROUTING.read_text(encoding="utf-8"))

    # 1) 抽取 D类拉语段 (35 段)
    d_dir = EXTRACTED / "d_class_stories"
    d_dir.mkdir(exist_ok=True)
    n_d = 0
    chars_d = 0
    seen = set()
    for r in routing["routing"]:
        for seg in r["segments"]:
            key = (seg["slug"], seg["start_page"], seg["end_page"])
            if key in seen:
                continue
            seen.add(key)
            slug = seg["slug"]
            sp = seg["start_page"]
            ep = seg["end_page"]
            title = seg.get("title", slug)
            out = d_dir / f"{slug}_p{sp:03d}-{ep:03d}.md"
            n = extract_pages(slug, sp, ep, out, title, seg.get("ch50"), seg.get("teach_ch"))
            if n:
                n_d += 1
                chars_d += n
    print(f"[1/2] D类拉语段: {n_d} 段, {chars_d:,} 字符 -> {d_dir}")

    # 2) 抽取教材的指定章节 (每本前 3-5 章)
    t_dir = EXTRACTED / "textbook_chapters"
    t_dir.mkdir(exist_ok=True)
    n_t = 0
    chars_t = 0
    for slug, chapters in TEXTBOOK_CHAPTERS.items():
        # 只抽前5章
        for ch_num, sp, ep in chapters[:5]:
            out = t_dir / f"{slug}_chap{ch_num:02d}_p{sp:03d}-{ep:03d}.md"
            title = f"{slug} Chapter {ch_num}"
            n = extract_pages(slug, sp, ep, out, title)
            if n:
                n_t += 1
                chars_t += n
    print(f"[2/2] 教材章节: {n_t} 段, {chars_t:,} 字符 -> {t_dir}")

    # 写 README
    readme = ["# 扩展读物抽取文件索引", ""]
    readme.append("**生成日期**: 2026-06-06")
    readme.append("")
    readme.append("## 目录结构")
    readme.append("")
    readme.append("```")
    readme.append("extracted/")
    readme.append("├── d_class_stories/    # D类教材的拉语故事段 (35段, 来自路由表)")
    readme.append("└── textbook_chapters/  # 教材章节抽取 (Cambridge/Oxford/Ecce Romani/Wheelock)")
    readme.append("```")
    readme.append("")
    readme.append(f"## 统计")
    readme.append("")
    readme.append(f"- **D类拉语段**: {n_d} 段, {chars_d:,} 字符")
    readme.append(f"- **教材章节**: {n_t} 段, {chars_t:,} 字符")
    readme.append("")
    readme.append("## 使用方法")
    readme.append("")
    readme.append("每个 `.md` 文件包含:")
    readme.append("- 元信息头 (slug, 页码, LLPSI章节锚点)")
    readme.append("- 抽取的拉语原文 (按页组织)")
    readme.append("")
    readme.append("学习者可根据路由表的 `🧩 段` 推荐, 直接打开对应文件阅读.")
    (EXTRACTED / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"[OK] {EXTRACTED / 'README.md'}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
