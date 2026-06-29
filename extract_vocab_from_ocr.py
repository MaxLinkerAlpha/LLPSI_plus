#!/usr/bin/env python3
"""
从 OCR 文件提取词汇，生成 capX_vocab_clean.json
支持 cap35~56（Familia Romana cap35 + Roma Aeterna cap36~56）
"""
import json
import re
import argparse
from pathlib import Path
from collections import Counter

BASE = Path("/Users/max/Downloads/Projects/LLPSI_plus")
OCR_DIR = BASE / "OCR"
VOCAB_DIR = BASE / "difficulty_algorithm" / "vocab_by_chapter"

LATIN_CHARS_PATTERN = re.compile(r'[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+')

# 章号到 OCR 路径的映射
def get_ocr_dir_for_chapter(ch):
    if 1 <= ch <= 35:
        return OCR_DIR / "LLPSI_core" / "familia_romana" / f"fr_cap{ch}"
    elif 36 <= ch <= 56:
        return OCR_DIR / "LLPSI_core" / "roma_aeterna" / f"ra_cap{ch}"
    else:
        return None


def extract_vocab_for_chapter(ch):
    """从一章的 OCR 文件提取所有拉丁词"""
    ocr_dir = get_ocr_dir_for_chapter(ch)
    if not ocr_dir or not ocr_dir.exists():
        print(f"  cap{ch}: OCR 目录不存在: {ocr_dir}")
        return []

    # 找所有 txt 文件
    txt_files = sorted(ocr_dir.glob("*.txt"))
    if not txt_files:
        print(f"  cap{ch}: 目录下无 txt 文件")
        return []

    word_counter = Counter()
    for f in txt_files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            # 移除行号标记 [1] [2] 等
            text = re.sub(r'\[\d+\]', ' ', text)
            # 提取拉丁词
            words = LATIN_CHARS_PATTERN.findall(text)
            for w in words:
                if len(w) >= 2:
                    word_counter[w.lower()] += 1
        except Exception as e:
            print(f"  警告 {f.name}: {e}")

    # 转为列表（按词频排序）
    return list(word_counter.keys())


def main():
    parser = argparse.ArgumentParser(description="从 OCR 提取词表")
    parser.add_argument("--start", type=int, default=35, help="起始章号")
    parser.add_argument("--end", type=int, default=56, help="结束章号")
    args = parser.parse_args()

    print("=" * 60)
    print(f"从 OCR 提取词表 (cap{args.start}~cap{args.end})")
    print("=" * 60)

    for ch in range(args.start, args.end + 1):
        words = extract_vocab_for_chapter(ch)
        if not words:
            print(f"  cap{ch}: 跳过（无词）")
            continue

        # 写入文件
        out_path = VOCAB_DIR / f"cap{ch}_vocab_clean.json"
        out_path.write_text(
            json.dumps(sorted(words), ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"  cap{ch}: 提取 {len(words)} 个词 → {out_path.name}")

    print("\n提取完成。下一步：运行 python3 clean_all.py 清洗。")


if __name__ == "__main__":
    main()