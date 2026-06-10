#!/usr/bin/env python3
"""
LLPSI 多版本文件质量对比工具
=====================================================
对比 9 类多版本文件,基于:
  1. 文件大小
  2. PDF 可选中文本量 (核心! 可选中 = 无需 OCR)
  3. 页数
  4. 嵌入字体数
  5. 文本提取样本质量
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import defaultdict

# 强制使用本地 Python 路径
sys.path.insert(0, '/Users/max/Downloads/Projects/LLPSI+++/scripts')

try:
    import pypdf
    PDF_LIB = "pypdf"
except ImportError:
    try:
        import pdfplumber
        PDF_LIB = "pdfplumber"
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            PDF_LIB = "PyPDF2"
        except ImportError:
            print("[ERROR] 请安装 pypdf 或 pdfplumber: pip install pypdf")
            sys.exit(1)

SOURCE_DIR = "/Users/max/Downloads/Projects/LLPSI+++/source"


def extract_text(pdf_path: str, max_pages: int = 5) -> tuple[int, str, int]:
    """
    提取 PDF 前 N 页的文本
    返回: (总页数, 提取的文本, 提取文本总字符数)
    """
    if PDF_LIB == "pypdf":
        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        sample_text = ""
        for i, page in enumerate(reader.pages[:max_pages]):
            try:
                t = page.extract_text() or ""
                sample_text += t + "\n"
            except Exception:
                pass
    elif PDF_LIB == "pdfplumber":
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            sample_text = ""
            for page in pdf.pages[:max_pages]:
                try:
                    t = page.extract_text() or ""
                    sample_text += t + "\n"
                except Exception:
                    pass
    else:  # PyPDF2
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        sample_text = ""
        for i, page in enumerate(reader.pages[:max_pages]):
            try:
                t = page.extract_text() or ""
                sample_text += t + "\n"
            except Exception:
                pass
    return total_pages, sample_text, len(sample_text)


def estimate_text_quality(text: str) -> dict:
    """
    评估文本质量指标:
    - 平均词长
    - 拉丁语典型词比例 (含 a/e/i/o/u/v 等)
    - 长音符号 (ā, ē, ī, ō, ū) 保留率
    - 特殊字符正确率
    """
    if not text:
        return {
            "avg_word_len": 0,
            "latin_word_ratio": 0,
            "macron_count": 0,
            "has_macrons": False,
            "mojibake_count": 0,
            "quality_score": 0,
        }

    words = re.findall(r"\b[a-zA-ZāēīōūȳĀĒĪŌŪȲæœÆŒ]+\b", text)
    if not words:
        return {
            "avg_word_len": 0,
            "latin_word_ratio": 0,
            "macron_count": 0,
            "has_macrons": False,
            "mojibake_count": 0,
            "quality_score": 0,
        }

    avg_len = sum(len(w) for w in words) / len(words)
    # 拉丁语典型词根检测
    latin_pattern = re.compile(r"\b(et|est|non|sed|aut|qui|quae|ad|in|ex|ab|cum|per|propter|inter|trans|contra)\b", re.IGNORECASE)
    latin_hits = sum(1 for w in words if latin_pattern.search(w))
    latin_ratio = latin_hits / len(words) if words else 0

    # 长音符号
    macrons = sum(1 for w in words if any(c in w for c in "āēīōūȳĀĒĪŌŪȲ"))
    has_macrons = macrons > 0

    # mojibake 检测 (UTF-8 解码错误的迹象: Ã©, Ã¨, Â, ï¿½ 等)
    mojibake_patterns = [
        r"Ã[©¨ª¢£¤¥¦§¨©ª«¬®°±²³´µ¶·¸¹]",  # 常见 UTF-8 错误
        r"Â[¡¢£¤¥¦§¨©ª«¬®°±²³´µ¶·¸¹]",   # UTF-8 cp1252 错误
        r"ï¿½",                              # UTF-8 BOM 错误
        r"\\x[0-9a-fA-F]{2}",                # \xNN 字面量
        r"\\[0-9]{3}",                       # \NNN 八进制
    ]
    mojibake_count = 0
    for pat in mojibake_patterns:
        mojibake_count += len(re.findall(pat, text))

    # 综合质量分: 越高越好
    # 有可选中文本 + 长音符号 + 极少 mojibake = 满分
    quality_score = 0
    if has_macrons:
        quality_score += 30
    if latin_ratio > 0.05:
        quality_score += 30
    if mojibake_count == 0:
        quality_score += 20
    if avg_len > 3:
        quality_score += 10
    # 文本提取率高 (前 5 页能拿到 > 1000 字符)
    if len(text) > 1000:
        quality_score += 10

    return {
        "avg_word_len": round(avg_len, 2),
        "latin_word_ratio": round(latin_ratio, 3),
        "macron_count": macrons,
        "has_macrons": has_macrons,
        "mojibake_count": mojibake_count,
        "quality_score": quality_score,
        "text_chars_extracted": len(text),
        "extraction_rate": "可复制" if len(text) > 500 else "需OCR",
    }


def compare_files():
    """对比所有多版本文件"""
    # 9 类多版本文件 (按 base name 分组)
    groups = defaultdict(list)

    for fname in os.listdir(SOURCE_DIR):
        if not fname.startswith("LLPSI_"):
            continue
        # 移除 _hd / _text_selectable / _v1 / _v1_scan / _1st_ed / _alt / _bw / _sm / _2003 等变体
        # 提取核心 base (如 "familia_romana")
        m = re.match(
            r"LLPSI_([a-z]+)_([a-z_]+?)(?:_(?:hd_[a-z0-9_]+|text_selectable|v[0-9]+|v[0-9]+_scan|1st_ed|alt|bw|sm|2003|1990))?\.([a-z]+)$",
            fname,
        )
        if m:
            category = m.group(1)
            base = m.group(2)
            ext = m.group(3)
            key = f"{category}_{base}"
            groups[key].append(fname)
        else:
            # Fallback: 尝试用前缀 + 第一段匹配
            print(f"  [SKIP] 无法分类: {fname}")

    # 仅保留有多个版本的分组
    multi_groups = {k: v for k, v in groups.items() if len(v) > 1}

    results = {}
    for key, files in sorted(multi_groups.items()):
        print(f"\n{'='*80}")
        print(f"分组: {key}  ({len(files)} 个版本)")
        print(f"{'='*80}")
        results[key] = []
        for fname in sorted(files):
            path = os.path.join(SOURCE_DIR, fname)
            size = os.path.getsize(path)
            size_mb = size / (1024 * 1024)
            try:
                pages, sample_text, text_chars = extract_text(path)
                quality = estimate_text_quality(sample_text)
            except Exception as e:
                print(f"  [ERROR] {fname}: {e}")
                pages = 0
                text_chars = 0
                quality = {"quality_score": -1}
            print(f"  {fname}")
            print(f"    大小: {size_mb:6.1f} MB  |  页数: {pages}  |  可提取文本: {text_chars} 字符")
            print(f"    质量: {quality}")
            results[key].append({
                "filename": fname,
                "size_mb": round(size_mb, 1),
                "pages": pages,
                "text_chars": text_chars,
                **quality,
            })

    # 写入 JSON 报告
    output_path = "/Users/max/Downloads/Projects/LLPSI+++/analysis_output/source_version_comparison.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] 对比报告已写入: {output_path}")

    # 输出推荐结论
    print(f"\n{'='*80}")
    print("推荐结论 (按 quality_score 排序):")
    print(f"{'='*80}")
    for key, items in sorted(results.items()):
        if not items:
            continue
        best = max(items, key=lambda x: x.get("quality_score", 0))
        print(f"  {key}:")
        print(f"    ★ 推荐: {best['filename']}")
        print(f"      评分: {best['quality_score']}/100, "
              f"页数: {best['pages']}, "
              f"可提取文本: {best.get('text_chars', 0)} 字符, "
              f"长音符号: {'有' if best.get('has_macrons') else '无'}")


if __name__ == "__main__":
    print(f"使用 PDF 库: {PDF_LIB}")
    print(f"扫描目录: {SOURCE_DIR}\n")
    compare_files()
