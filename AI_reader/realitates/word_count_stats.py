#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 realitates 目录下所有 .md 文件，统计词数（排除 YAML frontmatter）。
输出：
  1. 词数 < 150 的文件总数
  2. 这些文件按 chapter 目录的分布
  3. 其中所有后缀为 medius 或 longus 的文件列表
"""

import os
import re
from collections import Counter

BASE_DIR = "/Users/max/Downloads/Projects/LLPSI_plus/AI_reader/realitates"

def strip_yaml_frontmatter(text: str) -> str:
    """移除 YAML frontmatter（首两个 --- 之间的内容），返回正文。"""
    if text.startswith("---"):
        # 找到第二个 --- 的位置
        second = text.find("---", 3)
        if second != -1:
            return text[second + 3:]  # 跳过第二个 ---
    return text

def count_words(text: str) -> int:
    """统计文本中的词数（按空白分割）。"""
    return len(text.split())

def get_suffix_from_filename(filename: str) -> str:
    """
    从文件名中提取后缀标签（brevis/medius/longus）。
    文件名格式示例: Cap1_Terrae_et_aquae_Eurōpae_medius_024.md
    """
    # 去掉 .md 扩展名
    base = filename[:-3] if filename.endswith(".md") else filename
    parts = base.split("_")
    for p in parts:
        if p in ("brevis", "medius", "longus"):
            return p
    return "unknown"

def main():
    all_files_under_150 = []  # (chapter, filename, word_count, suffix)
    
    # 遍历所有 Cap* 目录（排除 backup 目录）
    for entry in sorted(os.listdir(BASE_DIR)):
        dirpath = os.path.join(BASE_DIR, entry)
        if not os.path.isdir(dirpath):
            continue
        if not entry.startswith("Cap"):
            continue
        if "backup" in entry.lower():
            continue
        
        chapter = entry  # e.g. "Cap1", "Cap10"
        
        for fname in os.listdir(dirpath):
            if not fname.endswith(".md"):
                continue
            
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                print(f"[WARN] 无法读取 {fpath}: {e}")
                continue
            
            body = strip_yaml_frontmatter(content)
            wc = count_words(body)
            suffix = get_suffix_from_filename(fname)
            
            if wc < 150:
                all_files_under_150.append((chapter, fname, wc, suffix))
    
    total_under_150 = len(all_files_under_150)
    
    # --- 统计 1: 总数 ---
    print("=" * 60)
    print(f"词数 < 150 的文件总数: {total_under_150}")
    print("=" * 60)
    
    # --- 统计 2: 按 chapter 分布 ---
    chapter_counter = Counter(item[0] for item in all_files_under_150)
    print(f"\n{'=' * 60}")
    print(f"按 chapter 目录分布（共 {len(chapter_counter)} 个目录有 <150 词文件）:")
    print(f"{'=' * 60}")
    # 按目录名自然排序（Cap1, Cap2, ..., Cap10, ...）
    for chap in sorted(chapter_counter.keys(), key=lambda x: (len(x), x)):
        count = chapter_counter[chap]
        bar = "#" * count
        print(f"  {chap:12s}: {count:3d}  {bar}")
    
    # --- 统计 3: 后缀为 medius 或 longus 的文件 ---
    med_long_files = [item for item in all_files_under_150 if item[3] in ("medius", "longus")]
    if med_long_files:
        print(f"\n{'=' * 60}")
        print(f"其中后缀为 medius 或 longus 的文件（共 {len(med_long_files)} 个，这些不应 <150 词）:")
        print(f"{'=' * 60}")
        for chap, fname, wc, suffix in sorted(med_long_files, key=lambda x: (x[0], x[1])):
            print(f"  {chap}/{fname:60s}  词数={wc:3d}  [suffix={suffix}]")
    else:
        print(f"\n{'=' * 60}")
        print("没有后缀为 medius 或 longus 且词数 < 150 的文件。")
        print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
