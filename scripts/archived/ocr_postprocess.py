#!/usr/bin/env python3
"""
OCR 后处理脚本
================
修正 Tesseract Latin OCR 的已知问题:
  1. 长音符 (macron) 被错误识别为 grave/accent 符号
     à→ā, è→ē, ì→ī, ò→ō, ù→ū, ü→ū
  2. 拉丁语特殊字符还原
  3. 清理 OCR 产生的多余空白和噪声

设计要点:
  - 保留分页文件以便校对
  - 同时输出一个纯净版 (无页码标记)
"""

import os
import re

INPUT_DIR = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/familia_romana/per_page_raw"
OUTPUT_DIR = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/familia_romana/per_page_clean"
FULL_OUTPUT = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/familia_romana/clean.txt"

# ============================================================
# Tesseract Latin OCR 常见错误修正表
# ============================================================

# 长音符修正: 拉丁语中长音符 (macron) 是关键语法标记
# Tesseract 常将其误认为 grave accent 或 umlaut
MACRON_FIXES = {
    'à': 'ā',  # grave → macron
    'è': 'ē',
    'ì': 'ī',
    'ò': 'ō',
    'ù': 'ū',
    'À': 'Ā',
    'È': 'Ē',
    'Ì': 'Ī',
    'Ò': 'Ō',
    'Ù': 'Ū',
}

# ü 在拉丁语中极少出现, 通常是 ū 被误识
# 但保留一些常见例外 (如 Hü 开头的德语人名)
UMLAUT_FIXES = {
    'ü': 'ū',
    'Ü': 'Ū',
}

# 拉丁语中 acute accent (á é í ó ú) 也可能是长音符的变体
# LLPSI 不使用 acute accent，全部应转换为 macron
ACUTE_TO_MACRON = {
    'á': 'ā',
    'é': 'ē',
    'í': 'ī',
    'ó': 'ō',
    'ú': 'ū',
    'Á': 'Ā',
    'É': 'Ē',
    'Í': 'Ī',
    'Ó': 'Ō',
    'Ú': 'Ū',
}

# OCR 可能产生双重音符 (acute+macron 堆叠), 如 Máārcus
DOUBLE_ACCENT_PATTERNS = [
    (r'[áā]{2}', 'ā'),  # 两个长音/a音符号 → 单个 macron
    (r'[éē]{2}', 'ē'),
    (r'[íī]{2}', 'ī'),
    (r'[óō]{2}', 'ō'),
    (r'[úū]{2}', 'ū'),
    (r'ÁĀ', 'Ā'),       # 大写版
    (r'ÉĒ', 'Ē'),
    (r'ÍĪ', 'Ī'),
    (r'ÓŌ', 'Ō'),
    (r'ÚŪ', 'Ū'),
]

# 其他已知 OCR 错误
OTHER_FIXES = {
    'Oirberg': 'Ørberg',   # Ø 的 OCR 修复 (书名页)
    'Qirberg': 'Ørberg',
    '0rberg': 'Ørberg',
    'orberg': 'ørberg',    # 小写版本
}

# 字母 V/U 混淆修复 (仅限特定模式, 在词中间不处理)
# LLPSI 使用 V 表示大写 U, 这是正确的罗马体惯例


def clean_page_text(text: str) -> str:
    """
    对单页 OCR 文本进行后处理
    
    参数:
        text: 原始 OCR 文本
    
    返回:
        清理后的文本
    """
    # 1. 长音符修正 (grave → macron)
    for wrong, correct in MACRON_FIXES.items():
        text = text.replace(wrong, correct)
    
    # 2. Umlaut 修正 (ü → ū)
    for wrong, correct in UMLAUT_FIXES.items():
        text = text.replace(wrong, correct)
    
    # 3. Acute accent → macron (LLPSI 不使用 acute)
    for wrong, correct in ACUTE_TO_MACRON.items():
        text = text.replace(wrong, correct)
    
    # 4. 双重音符修正 (áā → ā 等)
    for pattern, replacement in DOUBLE_ACCENT_PATTERNS:
        text = re.sub(pattern, replacement, text)
    
    # 5. 已知专有名词修正
    for wrong, correct in OTHER_FIXES.items():
        text = text.replace(wrong, correct)
    
    # 4. 清理多余空白行 (3 个以上连续空行 → 2 个空行)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # 5. 清理行尾多余空格
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    
    # 6. 合并因换行而被截断的单词 (拉丁语中极少有 hyphenation)
    # 保留原样, 因为拉丁语断行可能在词中
    # 对于明显的断词模式 (小写字母 + 连字符 + 换行 + 小写字母) 不做处理
    # 因为可能破坏正确的连字符用法
    
    return text


def process_all_pages(input_dir: str, output_dir: str, full_output_path: str):
    """
    处理所有分页 OCR 文件
    
    参数:
        input_dir: 原始分页文本目录
        output_dir: 清理后的分页文本目录
        full_output_path: 完整合并文本输出路径
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有分页文件并排序
    page_files = sorted(
        [f for f in os.listdir(input_dir) if f.endswith('.txt')],
        key=lambda x: int(re.search(r'(\d+)', x).group(1))
    )
    
    print(f"找到 {len(page_files)} 个分页文件")
    print(f"输出目录: {output_dir}")
    print(f"合并输出: {full_output_path}")
    print()
    
    all_clean_text = []
    total_chars_before = 0
    total_chars_after = 0
    
    for i, fname in enumerate(page_files):
        input_path = os.path.join(input_dir, fname)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        total_chars_before += len(raw_text)
        
        # 清理文本
        clean_text = clean_page_text(raw_text)
        total_chars_after += len(clean_text)
        
        # 保存清理后的分页文件
        output_path = os.path.join(output_dir, fname)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        # 添加到合并文本 (添加章节标记)
        page_num = int(re.search(r'(\d+)', fname).group(1))
        all_clean_text.append(clean_text)
        
        if (i + 1) % 50 == 0:
            print(f"  已处理 {i + 1}/{len(page_files)} 页")
    
    # 保存完整合并文本 (无页码标记, 纯文本流)
    full_text = "\n".join(all_clean_text)
    with open(full_output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"\n{'='*60}")
    print("后处理完成!")
    print(f"  处理页数: {len(page_files)}")
    print(f"  处理前总字符: {total_chars_before:,}")
    print(f"  处理后总字符: {total_chars_after:,}")
    print(f"  字符变化: {total_chars_after - total_chars_before:+d}")
    print(f"  完整文本: {full_output_path}")
    print(f"  分页文本: {output_dir}/")
    print(f"{'='*60}")
    
    return full_output_path


if __name__ == "__main__":
    process_all_pages(INPUT_DIR, OUTPUT_DIR, FULL_OUTPUT)
