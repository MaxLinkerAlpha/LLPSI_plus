#!/usr/bin/env python3
"""
analyze_book.py — 通用 LLPSI 词频分析 (FR + RA)
================================================================
与 iterum_analysis.py 相同的核心算法, 但参数化输入/输出文件路径和书名,
支持任何按 CAPITVLVM / CAP. 切分的拉丁语教材。

用法:
    python3 scripts/analyze_book.py --input <full.txt> --output-dir <dir> --name <short>
    python3 scripts/analyze_book.py --input ocr_output/familia_romana/clean.txt --output-dir analysis_output --name familia_romana
    python3 scripts/analyze_book.py --input ocr_output/roma_aeterna/_full.txt --output-dir analysis_output --name roma_aeterna
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict


# ============================================================
# 复用 iterum_analysis.py 的核心函数 (避免代码重复)
# ============================================================
def _import_iterum():
    import importlib.util
    spec = importlib.util.spec_from_file_location('iterum_analysis', 'scripts/iterum_analysis.py')
    mod = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise ImportError("can't load iterum_analysis.py")
    spec.loader.exec_module(mod)
    return mod


_ITERUM = None
def _iterum():
    global _ITERUM
    if _ITERUM is None:
        _ITERUM = _import_iterum()
    return _ITERUM


# ============================================================
# 主分析 (使用 iterum 的 split/tokenize)
# ============================================================
def analyze(input_path: str, output_dir: str, book_name: str) -> dict:
    """运行分析并写出 chapter_stats.csv + report markdown"""
    mod = _iterum()

    with open(input_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # 清理
    full_text = re.sub(r'={3,}.*?={3,}', '', full_text)
    full_text = re.sub(r'--- 第 \d+ 页 ---', '', full_text)   # 兼容旧 OCR 中文页码
    full_text = re.sub(r'--- PAGE \d+ ---', '', full_text)
    full_text = re.sub(r'--- \d+ ---', '', full_text)

    chapters = mod.split_into_chapters(full_text)
    print(f"[{book_name}] 识别到 {len(chapters)} 章")

    # 提取阅读正文 + 统计
    chapter_readings = {}
    for num in sorted(chapters.keys()):
        reading_text = mod.extract_readings_from_chapter(chapters[num])
        reading_text = re.sub(r'CAPITVLVM\s+\w+.*', '', reading_text)
        reading_text = re.sub(r'CAP\.\s+[IVX]+.*', '', reading_text)
        chapter_readings[num] = reading_text

    global_vocab = set()
    chapter_stats = []

    for num in sorted(chapter_readings.keys()):
        text = chapter_readings[num]
        words = mod.tokenize(text)
        words_lower = [w.lower() for w in words]
        total = len(words_lower)
        unique = set(words_lower)
        new_words = unique - global_vocab
        global_vocab.update(words_lower)
        word_counts = Counter(words_lower)
        density = (len(new_words) / total * 100) if total else 0
        high_freq_new = sum(1 for w in new_words if word_counts[w] >= 3)
        chapter_stats.append({
            'num': num,
            'total_tokens': total,
            'unique_words': len(unique),
            'new_words': len(new_words),
            'new_word_density': density,
            'new_high_freq_words': high_freq_new,
            'cumulative_vocab': len(global_vocab),
            'new_word_list': sorted(new_words),
            'top_new_words': sorted(
                [(w, word_counts[w]) for w in new_words if word_counts[w] >= 2],
                key=lambda x: -x[1]
            )[:15],
        })
        print(f"  Cap. {num:3d}: {total:4d} 词 | +{len(new_words):3d} 新词 | 密度 {density:.1f}%")

    os.makedirs(output_dir, exist_ok=True)

    # CSV
    csv_path = os.path.join(output_dir, f'{book_name}_chapter_stats.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("章节,总词数,新词数,新词密度(%),累计词汇,高频新词\n")
        for s in chapter_stats:
            f.write(f"{s['num']},{s['total_tokens']},{s['new_words']},"
                    f"{s['new_word_density']:.1f},{s['cumulative_vocab']},"
                    f"{s['new_high_freq_words']}\n")
    print(f"\n  CSV: {csv_path}")

    # Markdown report
    densities = [s['new_word_density'] for s in chapter_stats]
    avg_density = sum(densities) / len(densities) if densities else 0
    threshold = avg_density * 1.2
    steep = [s for s in chapter_stats if s['new_word_density'] > threshold]

    report = []
    report.append(f"# {book_name} 词频分析报告\n")
    report.append(f"**分析对象**: {book_name}\n")
    report.append(f"**章节数**: {len(chapter_stats)}\n")
    report.append(f"**全书累计词形**: {len(global_vocab):,}\n")
    report.append(f"**平均新词密度**: {avg_density:.1f}%\n")
    report.append(f"**陡坡阈值**: > {threshold:.1f}%\n\n")
    report.append("---\n\n")

    report.append(f"## 1. 每章词频总览\n\n")
    report.append("| 章节 | 总词数 | 新词数 | 密度 | 累计 | 高频新词 | 评级 |\n")
    report.append("|:--:|--:|--:|--:|--:|--:|:--:|\n")
    for s in chapter_stats:
        d = s['new_word_density']
        if d > avg_density * 1.5:
            r = 'STEEP'
        elif d > threshold:
            r = 'CAUTION'
        elif d < avg_density * 0.6:
            r = 'GENTLE'
        else:
            r = 'NORMAL'
        report.append(
            f"| Cap. {s['num']:2d} | {s['total_tokens']:5d} | {s['new_words']:4d} | "
            f"{d:5.1f}% | {s['cumulative_vocab']:6d} | {s['new_high_freq_words']:5d} | {r} |\n"
        )
    report.append("\n---\n\n")
    report.append(f"## 2. 陡坡章节 (>{threshold:.1f}%)\n\n")
    if steep:
        for s in steep:
            report.append(f"### Cap. {s['num']} — {s['new_word_density']:.1f}%\n")
            report.append(f"- 新词数: {s['new_words']}, 高频新词: {s['new_high_freq_words']}\n")
            if s['top_new_words']:
                report.append("\n高频新词:\n")
                for w, c in s['top_new_words']:
                    report.append(f"- `{w}` ({c}次)\n")
            report.append("\n")
    else:
        report.append("未检测到陡坡章节。\n\n")

    md_path = os.path.join(output_dir, f'{book_name}_analysis_report.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(''.join(report))
    print(f"  Report: {md_path}")

    return {
        'book_name': book_name,
        'chapter_stats': chapter_stats,
        'total_unique_forms': len(global_vocab),
        'avg_density': avg_density,
        'threshold': threshold,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='OCR 后的 _full.txt')
    parser.add_argument('--output-dir', default='analysis_output')
    parser.add_argument('--name', required=True, help='书的短名 (e.g. familia_romana, roma_aeterna)')
    args = parser.parse_args()
    analyze(args.input, args.output_dir, args.name)


if __name__ == '__main__':
    main()
