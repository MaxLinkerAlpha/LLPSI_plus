#!/usr/bin/env python3
"""
LLPSI Familia Romana PDF OCR 提取脚本
=======================================
功能:
  1. 使用 PyMuPDF 将 PDF 每页渲染为高分辨率图片 (350 DPI)
  2. 使用 Tesseract OCR (lat 拉丁语) 逐页识别文字
  3. 输出整理后的纯文本文件

设计要点:
  - 350 DPI 保证拉丁语特殊字符 (ā, ē, ī, ō, ū, Ø, æ, œ) 的识别精度
  - Tesseract PSM 3 (自动) 处理混合排版的页面
  - 多进程并行加速 (利用多核 CPU)
  - 每 10 页输出进度提示
  - 保留章节标记便于后续处理
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

# ============================================================
# 配置区
# ============================================================
# 旧版脚本: 源 PDF 路径已迁移到 source/ 目录
# 推荐改用 scripts/ocr_book.py (参数化版)
PDF_PATH = "/Users/max/Downloads/Projects/LLPSI+++/source/LLPSI_core_familia_romana.pdf"
OUTPUT_DIR = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/familia_romana"
DPI = 350  # 渲染分辨率 (越高越清晰, 但越慢)
TESSERACT_LANG = "lat"  # 拉丁语语言包
TESSERACT_CONFIG = "--psm 3 -c preserve_interword_spaces=1"  # PSM 3=自动, 保留词间空格


def ocr_single_page(args):
    """
    处理单页 PDF -> 图片 -> OCR
    
    参数:
        args: (page_index, pixmap_bytes) 元组
            page_index: 页码 (0-based)
            pixmap_bytes: PNG 格式的页面图片数据
    
    返回:
        (page_index, ocr_text) 元组
    """
    page_index, img_bytes = args
    
    try:
        # 将 PNG 字节流加载为 PIL Image
        image = Image.open(io.BytesIO(img_bytes))
        
        # Tesseract OCR 识别
        text = pytesseract.image_to_string(
            image,
            lang=TESSERACT_LANG,
            config=TESSERACT_CONFIG
        )
        
        return (page_index, text)
    except Exception as e:
        print(f"  [错误] 第 {page_index + 1} 页 OCR 失败: {e}", file=sys.stderr)
        return (page_index, f"[OCR 失败: {e}]\n")


def extract_and_ocr(pdf_path: str, output_dir: str, start_page: int = 0, end_page: int | None = None):
    """
    主流程: 提取 PDF 页面图片并执行 OCR
    
    参数:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
        start_page: 起始页 (0-based, 包含)
        end_page: 结束页 (0-based, 不包含). None 表示处理到最后一页
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"打开 PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    print(f"总页数: {total_pages}")
    
    if end_page is None:
        end_page = total_pages
    
    pages_to_process = list(range(start_page, end_page))
    num_pages = len(pages_to_process)
    
    print(f"处理范围: 第 {start_page + 1} ~ {end_page} 页 (共 {num_pages} 页)")
    print(f"Tesseract 语言: {TESSERACT_LANG}, DPI: {DPI}")
    print(f"CPU 核心数: {cpu_count()}")
    print()
    
    # ========================================================
    # 阶段 1: 渲染所有页面为 PNG (内存中)
    # ========================================================
    print("阶段 1/2: 渲染 PDF 页面为图片...")
    start_time = time.time()
    
    page_images = []  # [(page_index, png_bytes), ...]
    
    for i, page_idx in enumerate(pages_to_process):
        page = doc[page_idx]
        # 渲染页面为 Pixmap, 350 DPI
        # zoom = DPI / 72 (PDF 默认 72 DPI)
        zoom = DPI / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # 转为 PNG 字节流 (压缩存储, 节省内存)
        png_bytes = pix.tobytes("png")
        page_images.append((page_idx, png_bytes))
        
        # 每处理 50 页报告一次进度
        if (i + 1) % 50 == 0:
            elapsed = time.time() - start_time
            print(f"  已渲染 {i + 1}/{num_pages} 页 (耗时 {elapsed:.1f}s)")
    
    doc.close()
    render_time = time.time() - start_time
    print(f"  渲染完成! {num_pages} 页, 耗时 {render_time:.1f}s")
    
    # 估算内存使用
    total_mb = sum(len(img[1]) for img in page_images) / (1024 * 1024)
    print(f"  图片总大小: {total_mb:.1f} MB")
    print()
    
    # ========================================================
    # 阶段 2: 多进程 OCR
    # ========================================================
    print(f"阶段 2/2: OCR 识别 (多线程, {cpu_count()} 核)...")
    start_time = time.time()
    
    # 使用线程池并行 OCR (pytesseract 调用 C 库时释放 GIL)
    num_workers = max(1, cpu_count())
    
    results = {}  # page_index -> text
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        total = len(page_images)
        completed = 0
        
        # 提交所有任务
        futures = {executor.submit(ocr_single_page, args): args for args in page_images}
        
        for future in as_completed(futures):
            page_idx, text = future.result()
            results[page_idx] = text
            completed += 1
            
            if completed % 10 == 0:
                elapsed = time.time() - start_time
                pct = completed / total * 100
                speed = completed / elapsed * 60  # 页/分钟
                eta = (total - completed) / (completed / elapsed) / 60  # 剩余分钟
                print(f"  进度: {completed}/{total} ({pct:.1f}%) | "
                      f"速度: {speed:.1f} 页/分钟 | "
                      f"预计剩余: {eta:.1f} 分钟")
    
    ocr_time = time.time() - start_time
    print(f"\n  OCR 完成! 耗时 {ocr_time:.1f}s ({ocr_time/60:.1f} 分钟)")
    
    # ========================================================
    # 阶段 3: 按页码顺序合并文本
    # ========================================================
    print()
    print("阶段 3/3: 合并文本...")
    
    all_lines = []
    for page_idx in sorted(results.keys()):
        text = results[page_idx].strip()
        if text:
            # 添加页面标记 (便于后续校对)
            all_lines.append(f"\n{'='*60}")
            all_lines.append(f"--- 第 {page_idx + 1} 页 ---")
            all_lines.append(f"{'='*60}\n")
            all_lines.append(text)
    
    full_text = "\n".join(all_lines)
    
    # 保存完整文本
    output_path = os.path.join(output_dir, "full.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    # 同时保存每页单独文件 (方便校对)
    per_page_dir = os.path.join(output_dir, "per_page_raw")
    os.makedirs(per_page_dir, exist_ok=True)
    for page_idx in sorted(results.keys()):
        text = results[page_idx].strip()
        if text:
            page_path = os.path.join(per_page_dir, f"page_{page_idx + 1:04d}.txt")
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(text)
    
    # 统计信息
    total_chars = sum(len(t) for t in results.values())
    non_empty = sum(1 for t in results.values() if t.strip())
    
    print(f"\n{'='*60}")
    print(f"处理完成!")
    print(f"  总页数: {total_pages}")
    print(f"  已处理: {num_pages}")
    print(f"  非空页: {non_empty}")
    print(f"  总字符数: {total_chars:,}")
    print(f"  完整文本: {output_path}")
    print(f"  分页文本: {per_page_dir}/")
    print(f"{'='*60}")
    
    return output_path


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    # 可选: 只处理前几页做测试
    # extract_and_ocr(PDF_PATH, OUTPUT_DIR, start_page=0, end_page=5)
    
    # 全量处理
    extract_and_ocr(PDF_PATH, OUTPUT_DIR)
