#!/usr/bin/env python3
"""
extract_hd_text.py — 用 pypdf 直接提取 HD 2nd color 版本的文本
=====================================================
本项目建议版本: HD 2nd color (含可选中文字层)
- FR: LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf
- RA: LLPSI_core_roma_aeterna_hd_2nd_color.pdf

替代原来的 OCR 输出,文本质量更高,与 OCR 一致性 79% (FR) / 100% (RA)
"""
import argparse
import os
import re
import sys
import time
import pypdf
from pathlib import Path


def extract_pdf_text(pdf_path: str) -> tuple[str, int, int]:
    """
    用 pypdf 提取 PDF 全部文本, 每页之间插入分隔符
    返回: (full_text, total_chars, total_pages)

    注: pypdf 在某些 PDF (ToUnicode CMap 异常) 中会输出 octal escape 序列
    如 '\\303\\234' 表示 UTF-8 字节 0xC3 0x9C (= 'Ü').
    这里在拼接时实时解码为正常字符。
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"  PDF: {pdf_path}")
    print(f"  总页数: {total_pages}")

    octal_re = re.compile(r"\\(\d{2,3})")
    multi_re = re.compile(r"(?:\\\d{2,3})+")
    def decode_octal_escapes(s: str) -> str:
        """解码 pypdf 输出的 octal escape 序列为正常字符 (UTF-8 字节序列)。

        背景: 部分 PDF (如 Aeneis) 的 ToUnicode CMap 异常, pypdf 会输出
        `\\303\\234` 这样的字面反斜杠 + 3 位数字序列, 表示 UTF-8 字节
        0xC3 0x9C = 'Ü'。必须把连续多个 octal 合并解码 (UTF-8 多字节),
        不能逐个单独解码 (会因不完整 UTF-8 序列变 U+FFFD)。
        """
        def _sub(m):
            oct_strs = re.findall(r"\\(\d{2,3})", m.group(0))
            try:
                byte_vals = [int(o, 8) for o in oct_strs]
                return bytes(byte_vals).decode("utf-8", errors="replace")
            except Exception:
                return m.group(0)
        return multi_re.sub(_sub, s)

    chunks = []
    total_chars = 0
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        text = decode_octal_escapes(text)
        total_chars += len(text)
        # 用 --- PAGE N --- 分隔 (兼容 iterum_analysis.py 和 analyze_book.py 的清理正则)
        chunks.append(f"--- PAGE {i} ---\n{text}")

        if i % 50 == 0 or i == total_pages:
            pct = i / total_pages * 100
            print(f"  进度: {i}/{total_pages} ({pct:.1f}%) 累计 {total_chars:,} 字符", flush=True)

    return "\n".join(chunks), total_chars, total_pages


def main():
    parser = argparse.ArgumentParser(description="用 pypdf 提取 HD 2nd color PDF 文本")
    parser.add_argument('--pdf', required=True, help='HD PDF 路径')
    parser.add_argument('--output', required=True, help='输出文本文件路径')
    parser.add_argument('--book-name', default='', help='书籍名称(用于日志)')
    args = parser.parse_args()

    print("=" * 60)
    print(f"提取 HD 文本: {args.book_name or args.pdf}")
    print("=" * 60)

    t0 = time.time()
    text, chars, pages = extract_pdf_text(args.pdf)
    elapsed = time.time() - t0

    # 写入文件
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(text)

    print()
    print("=" * 60)
    print("[OK] 提取完成")
    print(f"  输出文件: {args.output}")
    print(f"  页数:     {pages}")
    print(f"  字符数:   {chars:,}")
    print(f"  文件大小: {os.path.getsize(args.output):,} bytes")
    print(f"  耗时:     {elapsed:.1f}s")
    print("=" * 60)


if __name__ == '__main__':
    main()
