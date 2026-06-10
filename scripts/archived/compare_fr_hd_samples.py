#!/usr/bin/env python3
"""
FR HD 多个版本 PDF 的 OCR 样本对比
=====================================================
在 3 个典型页面 (p.30, p.80, p.150) 上执行 OCR,
对比 HD text_selectable vs HD color small vs 普通版
"""
import subprocess
import pypdf
from pathlib import Path
import time
import sys

VERSIONS = [
    'LLPSI_core_familia_romana.pdf',
    'LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf',
    'LLPSI_core_familia_romana_hd_color_small.pdf',
]
SAMPLE_PAGES = [30, 80, 150]
SOURCE_DIR = "/Users/max/Downloads/Projects/LLPSI+++/source"
TEMP_DIR = "/tmp/fr_ocr_samples"


def render_page(pdf_path: str, page_num: int, output: str, dpi: int = 300):
    """用 pdftoppm 渲染 PDF 单页为图片"""
    cmd = [
        "pdftoppm",
        "-f", str(page_num),
        "-l", str(page_num),
        "-r", str(dpi),
        "-png",
        pdf_path,
        output
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output + f"-{page_num:03d}.png"


def ocr_image(image_path: str, lang: str = "lat") -> str:
    """用 tesseract 对图片做 OCR - 需要在文件所在目录运行"""
    import os
    image_dir = os.path.dirname(image_path) or '.'
    image_filename = os.path.basename(image_path)
    output_base = "/tmp/_ocr_tmp"
    cmd = [
        "tesseract",
        image_filename,
        output_base,
        "-l", lang,
        "--psm", "3",
        "-c", "preserve_interword_spaces=1"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=image_dir)
    output_path = f"{output_base}.txt"
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    return ""


def extract_pypdf_page(pdf_path: str, page_num: int) -> str:
    """用 pypdf 提取单页文本"""
    r = pypdf.PdfReader(pdf_path)
    if page_num - 1 < len(r.pages):
        return r.pages[page_num - 1].extract_text() or ''
    return ''


def main():
    Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("FR HD 多版本 OCR 样本对比")
    print("=" * 80)

    results = {}
    for v in VERSIONS:
        pdf_path = f"{SOURCE_DIR}/{v}"
        print(f"\n--- {v} ---")
        results[v] = {}

        for page in SAMPLE_PAGES:
            print(f"  p.{page}:", end=" ", flush=True)
            t0 = time.time()

            # 1. OCR 渲染
            img_base = f"{TEMP_DIR}/{v.replace('.pdf','')}_p{page}"
            try:
                img_path = render_page(pdf_path, page, img_base, dpi=300)
            except subprocess.CalledProcessError as e:
                print(f"渲染失败: {e}")
                continue

            # 2. OCR
            try:
                ocr_text = ocr_image(img_path)
            except Exception as e:
                print(f"OCR 失败: {e}")
                ocr_text = ""

            # 3. pypdf 提取
            pypdf_text = extract_pypdf_page(pdf_path, page)

            # 4. 比较
            ocr_chars = len(ocr_text)
            pypdf_chars = len(pypdf_text)
            elapsed = time.time() - t0

            # 词形匹配度
            import re
            ocr_words = set(re.findall(r"\b[a-zA-Zāēīōūȳ]+\b", ocr_text.lower()))
            pypdf_words = set(re.findall(r"\b[a-zA-Zāēīōūȳ]+\b", pypdf_text.lower()))
            common = ocr_words & pypdf_words
            overlap_pct = (len(common) / len(pypdf_words) * 100) if pypdf_words else 0

            print(f"OCR {ocr_chars} 字符, pypdf {pypdf_chars} 字符, 重叠 {overlap_pct:.1f}%, 耗时 {elapsed:.1f}s")

            results[v][page] = {
                "ocr_chars": ocr_chars,
                "pypdf_chars": pypdf_chars,
                "overlap_pct": overlap_pct,
                "ocr_text_sample": ocr_text[:200],
                "pypdf_text_sample": pypdf_text[:200],
            }

    # 总结
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)
    for v, pages in results.items():
        avg_overlap = sum(p["overlap_pct"] for p in pages.values()) / max(len(pages), 1)
        total_pypdf = sum(p["pypdf_chars"] for p in pages.values())
        total_ocr = sum(p["ocr_chars"] for p in pages.values())
        print(f"\n{v}")
        print(f"  平均词形重叠率: {avg_overlap:.1f}%")
        print(f"  3 页 pypdf 总字符: {total_pypdf}")
        print(f"  3 页 OCR 总字符: {total_ocr}")
        print(f"  文本质量评估:")
        if avg_overlap > 70:
            print(f"    ★★★ pypdf 与 OCR 一致性高 - pypdf 提取可信")
        elif avg_overlap > 50:
            print(f"    ★★☆ pypdf 与 OCR 中度一致")
        else:
            print(f"    ★☆☆ 一致性偏低, 建议深入比较")

    # 保存 JSON
    import json
    out_path = "/Users/max/Downloads/Projects/LLPSI+++/analysis_output/fr_version_ocr_samples.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] 样本结果已保存: {out_path}")


if __name__ == "__main__":
    main()
