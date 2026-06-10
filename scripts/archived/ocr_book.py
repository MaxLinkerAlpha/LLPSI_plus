#!/usr/bin/env python3
"""
ocr_book.py — 参数化 OCR 脚本 (复用 ocr_familia_romana.py 的核心逻辑)
=====================================================================
对任意拉丁语 PDF 执行 PyMuPDF + Tesseract OCR, 输出按 slug 分类的逐页文本。

用法:
    python3 scripts/ocr_book.py --pdf <path> --slug <name> [--start N] [--end M] [--dpi 350]

输出:
    ocr_output/<slug>/page_NNN.txt
    ocr_output/<slug>/<slug>_full.txt  (合并版, 供后续切段使用)
"""

import argparse
import io
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


# ============================================================
# 拉丁语 OCR 配置
# ============================================================
TESSERACT_LANG = "lat"
TESSERACT_CONFIG = "--psm 3 -c preserve_interword_spaces=1"
DEFAULT_DPI = 350


def ocr_single_page(args):
    """对单页 PNG 字节流执行 OCR, 返回 (页码, 文本)."""
    page_index, img_bytes = args
    try:
        image = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(
            image,
            lang=TESSERACT_LANG,
            config=TESSERACT_CONFIG,
        )
        return (page_index, text)
    except Exception as e:
        return (page_index, f"[OCR 失败: {e}]\n")


def extract_and_ocr(pdf_path: str, output_dir: str, dpi: int,
                    start_page: int, end_page, max_workers: int) -> int:
    """对 PDF 指定页面范围执行 OCR, 写入 output_dir."""
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    total = doc.page_count
    if end_page is None or end_page > total:
        end_page = total

    print(f"  [信息] PDF 共 {total} 页, 处理范围 [{start_page}, {end_page})")
    print(f"  [信息] DPI = {dpi}, 并行 = {max_workers} 线程")

    t0 = time.time()
    page_results: dict[int, str] = {}

    # 分批处理: 一次提交一批页面, 减少内存峰值
    BATCH = 10
    for batch_start in range(start_page, end_page, BATCH):
        batch_end = min(batch_start + BATCH, end_page)

        # 1) 渲染该批 PDF 页面为图片
        batch_args = []
        for i in range(batch_start, batch_end):
            page = doc.load_page(i)
            # 放大倍率: PDF 默认 72 DPI, 350/72 ≈ 4.86
            zoom = dpi / 72.0
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            batch_args.append((i, pix.tobytes("png")))

        # 2) 并行 OCR
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(ocr_single_page, arg): arg[0] for arg in batch_args}
            for fut in as_completed(futures):
                page_idx, text = fut.result()
                page_results[page_idx] = text

        # 3) 进度
        done = len(page_results)
        elapsed = time.time() - t0
        rate = done / elapsed if elapsed > 0 else 0
        eta = (end_page - start_page - done) / rate if rate > 0 else 0
        print(f"  [进度] {done}/{end_page - start_page} 页, "
              f"已用 {elapsed:.0f}s, 剩余 ≈ {eta:.0f}s")

    doc.close()

    # 4) 按页码顺序写入文件
    full_path = os.path.join(output_dir, "_full.txt")
    with open(full_path, "w", encoding="utf-8") as f_full:
        for i in range(start_page, end_page):
            text = page_results.get(i, "")
            # 单独一页 (3 位补零, 便于排序)
            page_path = os.path.join(output_dir, f"page_{i+1:03d}.txt")
            with open(page_path, "w", encoding="utf-8") as f_p:
                f_p.write(text)
            # 合并版: 加页码标记
            f_full.write(f"\n--- PAGE {i+1} ---\n{text}")

    print(f"  [完成] 输出目录: {output_dir}")
    print(f"  [完成] 单页: page_001.txt ... page_{end_page:03d}.txt")
    print(f"  [完成] 合并: _full.txt")
    print(f"  [完成] 总耗时: {time.time() - t0:.1f}s")
    return end_page - start_page


def main():
    parser = argparse.ArgumentParser(description="OCR a Latin PDF → per-page text")
    parser.add_argument("--pdf", required=True, help="PDF 文件路径")
    parser.add_argument("--slug", required=True, help="输出目录名 (e.g. colloquia_personarum)")
    parser.add_argument("--output-root", default="ocr_output", help="输出根目录")
    parser.add_argument("--start", type=int, default=0, help="起始页 (0-based, 含)")
    parser.add_argument("--end", type=int, default=None, help="结束页 (0-based, 不含)")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI, help="渲染 DPI (默认 350)")
    parser.add_argument("--workers", type=int, default=min(4, cpu_count()),
                        help="并行线程数 (默认 min(4, CPU 数))")
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"  [错误] PDF 不存在: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.join(args.output_root, args.slug)
    print(f"  [开始] {args.pdf}")
    print(f"  [输出] {output_dir}")

    n = extract_and_ocr(
        pdf_path=args.pdf,
        output_dir=output_dir,
        dpi=args.dpi,
        start_page=args.start,
        end_page=args.end,
        max_workers=args.workers,
    )
    print(f"  [结果] 共处理 {n} 页")


if __name__ == "__main__":
    main()
