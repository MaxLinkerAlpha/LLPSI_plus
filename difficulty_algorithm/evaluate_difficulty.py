#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLPSI 难度评估脚本 v1_2_0
算法: 累积覆盖率阈值（type-level）+ 长音/大小写归一化 fallback
  - 「学到第几章时 LLPSI 累积词汇能覆盖文本 90% 的独特词形？」
  - 精确匹配优先，未命中时回退到去长音+小写形式匹配
  - 当 LLPSI 收录率本身不足 90% 时降级输出最高可达覆盖率
"""

import os
import re
import json
import statistics
from pathlib import Path
from collections import OrderedDict

# ============================================================
# 配置
# ============================================================

OCR_DIR = Path(__file__).parent.parent / "OCR"
TOTAL_CHAPTERS = 56
SAMPLE_CHAPTERS = [1, 3, 5, 7, 10, 13, 15, 18, 20, 23, 25,
                   28, 30, 33, 35, 38, 40, 43, 45, 48, 50, 53, 55]

# ============================================================
# 工具函数 — 章节目录名
# ============================================================

def get_chapter_dir(chapter_num: int) -> str:
    if 1 <= chapter_num <= 35:
        return f"fr_cap{chapter_num}"
    elif 36 <= chapter_num <= 56:
        return f"ra_cap{chapter_num}"
    else:
        raise ValueError(f"无效章节号: {chapter_num}")


def get_main_text_path(chapter_num: int) -> Path:
    return OCR_DIR / get_chapter_dir(chapter_num) / f"cap{chapter_num}_main_macrons_final.txt"


# ============================================================
# 文本预处理 — 分词与清洗
# ============================================================

LATIN_LETTERS_RE = re.compile(r'[a-zA-ZāēīōūĀĒĪŌŪăĕĭŏŭĂĔĬŎŬ]')
SECTION_MARKER_RE = re.compile(r'^\[\d+\]$')
CAP_MARKER_RE = re.compile(r'^CAP\.[IVXLCDM]+$')
ROMAN_NUMERAL_RE = re.compile(r'^[IVXLCDM]+$')
NON_LETTER_RE = re.compile(r'^[^a-zA-ZāēīōūĀĒĪŌŪăĕĭŏŭĂĔĬŎŬ]+$')


def clean_token(raw: str) -> str | None:
    token = raw.strip()
    if not token:
        return None
    if SECTION_MARKER_RE.match(token):
        return None
    token = token.strip('.,:;!?()「」"\'’”“—-—«»*^=+/\\|[]{}@#$%&~`…')
    token = token.replace('«', '').replace('»', '').replace('^', '')
    if not token:
        return None
    if len(token) < 2:
        return None
    if '?' in token:
        return None
    if CAP_MARKER_RE.match(token):
        return None
    if ROMAN_NUMERAL_RE.match(token) and len(token) <= 4:
        return None
    if token.isdigit():
        return None
    if not LATIN_LETTERS_RE.search(token):
        return None
    token = token.rstrip('.')
    return token


def tokenize_text(text: str) -> list[str]:
    raw_tokens = text.split()
    clean_tokens = []
    for raw in raw_tokens:
        cleaned = clean_token(raw)
        if cleaned:
            clean_tokens.append(cleaned)
    return clean_tokens


def read_main_text(chapter_num: int) -> str:
    path = get_main_text_path(chapter_num)
    if not path.exists():
        print(f"  [警告] 文件不存在: {path}")
        return ""
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


# ============================================================
# 归一化函数 — 去长音 + 小写
# ============================================================

# 长音 → 短音映射表（同时处理大小写）
MACRON_TO_SHORT = str.maketrans({
    'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u',
    'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ō': 'O', 'Ū': 'U',
    'ă': 'a', 'ĕ': 'e', 'ĭ': 'i', 'ŏ': 'o', 'ŭ': 'u',
    'Ă': 'A', 'Ĕ': 'E', 'Ĭ': 'I', 'Ŏ': 'O', 'Ŭ': 'U',
})


def normalize_word(word: str) -> str:
    """
    归一化词形：去长音符号 + 转小写。
    用于在精确匹配失败后的 fallback 查询。
    """
    return word.translate(MACRON_TO_SHORT).lower()


# ============================================================
# Step 1 — 建立词→章节映射表（精确 + 归一化双表）
# ============================================================

def build_word_chapter_map() -> tuple[dict[str, int], dict[str, int], dict]:
    """
    返回:
      (word_map, normalized_map, chapter_stats)

      word_map        — 精确词形 → 首次出现章节号
      normalized_map  — 归一化词形 → 最早首次出现章节号
                         （多词形碰撞时取最早章节）
      chapter_stats   — 每章统计信息
    """
    word_map: OrderedDict[str, int] = OrderedDict()
    normalized_map: dict[str, int] = {}    # normalized_form → earliest_chapter
    chapter_stats: dict[int, dict] = {}

    for ch in range(1, TOTAL_CHAPTERS + 1):
        text = read_main_text(ch)
        tokens = tokenize_text(text)

        total = len(tokens)
        unique = len(set(tokens))
        new_words_exact = 0
        new_words_normalized = 0

        for token in tokens:
            # 精确映射表
            if token not in word_map:
                word_map[token] = ch
                new_words_exact += 1

            # 归一化映射表（去长音+小写）
            nf = normalize_word(token)
            if nf not in normalized_map:
                normalized_map[nf] = ch
                new_words_normalized += 1

        chapter_stats[ch] = {
            'total_tokens': total,
            'unique_types': unique,
            'new_words': new_words_exact,
            'new_normalized': new_words_normalized,
            'cumulative_lexicon': len(word_map),
            'cumulative_normalized': len(normalized_map),
        }

        status = "OK" if total > 0 else "EMPTY"
        print(f"  Cap.{ch:02d} | 词数={total:4d} | 新词={new_words_exact:3d} | "
              f"累积={len(word_map):5d} | 归一化累积={len(normalized_map):4d} | {status}")

    return word_map, normalized_map, chapter_stats


# ============================================================
# Step 2 — 累积覆盖率阈值评估（v1_2_0 归一化版）
# ============================================================

def lookup_chapter(word: str, word_map: dict[str, int],
                   normalized_map: dict[str, int]) -> int | None:
    """
    两遍查询：
      1. 精确匹配（含长音、大小写）
      2. fallback → 归一化匹配（去长音 + 小写）
    返回首次出现章节号，未命中返回 None
    """
    if word in word_map:
        return word_map[word]

    nf = normalize_word(word)
    if nf in normalized_map:
        return normalized_map[nf]

    return None


def evaluate_text_coverage(tokens: list[str],
                           word_map: dict[str, int],
                           normalized_map: dict[str, int] | None = None,
                           threshold: float = 0.90) -> dict:
    """
    使用累积覆盖率阈值法评估文本难度（type-level, v1_2_0）。

    改进（v1.2）:
      - 精确匹配优先，未命中回退归一化匹配
      - 收录率不足 90% → 降级输出 max_achievable 字段

    返回字段:
      difficulty          — 90% 阈值触达章节（None = 无法触达）
      difficulty_degraded  — True 时表示降级输出
      llpsi_coverage      — LLPSI 收录率（精确+归一化合并后）
      max_achievable       — 学完全书后的最高可达覆盖率
      max_achievable_ch    — 最高覆盖率接近 0% 触达时的章节
      threshold_80/85/90/95 — 各阈值触达章节
      total_types          — 总独特词形数
      found_types_exact    — 精确匹配数
      found_types_normalized — 归一化匹配数
      unknown_types        — 完全未收录数
      sample_sufficient    — ≥ 30 独特词形
      unknown_words        — 超纲词清单（前 20）
    """
    result = {
        'difficulty': None,
        'difficulty_degraded': False,
        'llpsi_coverage': 0.0,
        'max_achievable': 0.0,
        'max_achievable_ch': None,
        'threshold_80': None,
        'threshold_85': None,
        'threshold_90': None,
        'threshold_95': None,
        'total_types': 0,
        'found_types': 0,
        'found_types_exact': 0,
        'found_types_normalized': 0,
        'unknown_types': 0,
        'sample_sufficient': False,
        'unknown_words': [],
    }

    if not tokens:
        return result

    # 无归一化映射表时，回退纯精确匹配（向后兼容）
    if normalized_map is None:
        normalized_map = {}

    # 取独特词形
    unique_types = list(dict.fromkeys(tokens))
    total_types = len(unique_types)
    result['total_types'] = total_types
    if total_types == 0:
        return result

    # 两遍查表
    type_chapters = []
    unknown_words = []
    found_exact = 0
    found_normalized = 0

    for word in unique_types:
        if word in word_map:
            # 精确命中
            type_chapters.append((word, word_map[word], 'exact'))
            found_exact += 1
        else:
            nf = normalize_word(word)
            if nf in normalized_map:
                # 归一化命中
                type_chapters.append((word, normalized_map[nf], 'normalized'))
                found_normalized += 1
            else:
                type_chapters.append((word, None, 'unknown'))
                unknown_words.append(word)

    found_types = found_exact + found_normalized
    result['found_types'] = found_types
    result['found_types_exact'] = found_exact
    result['found_types_normalized'] = found_normalized
    result['unknown_types'] = len(unknown_words)
    result['unknown_words'] = unknown_words[:20]  # 只保留前 20 以节省输出
    result['llpsi_coverage'] = round(found_types / total_types * 100, 1)
    result['sample_sufficient'] = total_types >= 30

    # 最高可达覆盖率（学完 LLPSI 全部 56 章）
    result['max_achievable'] = result['llpsi_coverage']
    if found_types == 0:
        return result

    # 按章节号排序（已收录的）
    sorted_found = sorted(ch for _, ch, _ in type_chapters if ch is not None)

    # 计算各阈值的触达章节
    thresholds = {
        'threshold_80': 0.80,
        'threshold_85': 0.85,
        'threshold_90': 0.90,
        'threshold_95': 0.95,
    }

    for key, target_pct in thresholds.items():
        needed_count = int(total_types * target_pct)
        if found_types < needed_count:
            result[key] = None
            continue
        result[key] = sorted_found[needed_count - 1]

    # 主难度等级
    if result['threshold_90'] is not None:
        result['difficulty'] = result['threshold_90']
        result['difficulty_degraded'] = False
    else:
        # 降级：输出最高可达的覆盖率和对应的最大触达章节
        result['difficulty_degraded'] = True
        # 找到能达到的最高阈值
        for key, target_pct in sorted(thresholds.items(), reverse=True):
            if result[key] is not None:
                result['difficulty'] = result[key]
                break
        # 最高覆盖率触达的章节（即使没到 90%，也告诉用户学到了第几章时覆盖了多少）
        if len(sorted_found) >= 1:
            result['max_achievable_ch'] = sorted_found[-1]  # 最后一个收录词出现需到第几章
        else:
            result['max_achievable_ch'] = None

    return result


# ============================================================
# 输出格式化 (v1_2_0)
# ============================================================

def format_coverage_result(chapter_num: int, result: dict, chapter_stats: dict) -> str:
    """格式化单章覆盖阈值评估结果"""
    ch_info = chapter_stats.get(chapter_num, {})
    warning = "" if result['sample_sufficient'] else " [样本不足!]"
    degraded = " [降级]" if result.get('difficulty_degraded') else ""

    t80 = result['threshold_80'] or '—'
    t85 = result['threshold_85'] or '—'
    t90 = result['threshold_90'] or '—'
    t95 = result['threshold_95'] or '—'

    lines = [
        f"────────────────────────────────────────────",
        f"  Cap.{chapter_num:02d} 难度评估 (覆盖阈值法 v1.2)",
        f"────────────────────────────────────────────",
        f"  Token 总数           : {ch_info.get('total_tokens', '?'):>5}",
        f"  独特词形 (types)     : {result['total_types']:>5}",
        f"  LLPSI 收录 (精确)    : {result['found_types_exact']:>5}",
        f"  LLPSI 收录 (归一化)  : {result['found_types_normalized']:>5}",
        f"  LLPSI 总收录率       : {result['llpsi_coverage']:>5.1f}%",
        f"  完全未收录           : {result['unknown_types']:>5}",
        f"────────────────────────────────────────────",
        f"  80% 触达章节         : {str(t80):>5}",
        f"  85% 触达章节         : {str(t85):>5}",
        f"  90% 触达章节         : {str(t90):>5}  ← 难度等级",
        f"  95% 触达章节         : {str(t95):>5}",
        f"────────────────────────────────────────────",
        f"  难度等级             : {result['difficulty'] or 'N/A'}{degraded}{warning}",
    ]
    if result.get('difficulty_degraded') and result.get('max_achievable'):
        lines.append(f"  最高可达覆盖率       : {result['max_achievable']:.1f}% (学完 LLPSI 全 56 章)")
        if result.get('max_achievable_ch'):
            lines.append(f"  建议参考触达章节     : {result['max_achievable_ch']}")

    return "\n".join(lines)


def format_coverage_summary(eval_results: dict, chapter_stats: dict) -> str:
    """格式化覆盖阈值法汇总对比表"""
    header = (
        f"{'章节':>5} | {'词形':>5} | {'精匹':>4} | {'归匹':>4} | {'收率':>5} | "
        f"{'80%':>4} | {'90%':>4} | {'偏离':>5} | {'备注'}"
    )
    sep = "-" * len(header)

    rows = [header, sep]
    for ch in SAMPLE_CHAPTERS:
        if ch not in eval_results:
            continue
        r = eval_results[ch]

        t80 = f"{r['threshold_80']:4d}" if r['threshold_80'] else "   —"
        t90 = f"{r['threshold_90']:4d}" if r['threshold_90'] else "   —"

        diff_val = r['difficulty'] - ch if r['difficulty'] is not None else None
        if diff_val is not None:
            diff_str = f"{diff_val:+4d}"
        else:
            diff_str = "   —"

        note = ""
        if not r['sample_sufficient']:
            note = "样本不足"
        elif r.get('difficulty_degraded'):
            note = "降级"

        row = (f"{ch:5d} | {r['total_types']:5d} | {r['found_types_exact']:4d} | "
               f"{r['found_types_normalized']:4d} | {r['llpsi_coverage']:4.1f}% | "
               f"{t80} | {t90} | {diff_str} | {note}")
        rows.append(row)

    return "\n".join(rows)


def format_external_result(name: str, result: dict) -> str:
    """格式化外部读物评估结果"""
    degraded = " [降级 — 收录率不足]" if result.get('difficulty_degraded') else ""
    warning = "" if result['sample_sufficient'] else " [样本不足]"

    t80 = result['threshold_80'] or '—'
    t85 = result['threshold_85'] or '—'
    t90 = result['threshold_90'] or '—'
    t95 = result['threshold_95'] or '—'

    lines = [
        f"  {'─' * 56}",
        f"  {name}",
        f"  {'─' * 56}",
        f"  独特词形: {result['total_types']} | "
        f"精确匹配: {result['found_types_exact']} | "
        f"归一化匹配: {result['found_types_normalized']} | "
        f"总收录率: {result['llpsi_coverage']}%{warning}",
        f"  80%→{t80} | 85%→{t85} | 90%→{t90} | 95%→{t95}",
        f"  难度等级: {result['difficulty'] or 'N/A'}{degraded}",
    ]
    if result.get('difficulty_degraded'):
        lines.append(f"  最高可达: {result['max_achievable']:.1f}% (学完全书 56 章)")
        if result.get('max_achievable_ch'):
            lines.append(f"  建议参考: 第 {result['max_achievable_ch']} 章水平 ({result['max_achievable']:.1f}% 覆盖)")

    if result['unknown_words']:
        lines.append(f"  超纲词样本: {', '.join(result['unknown_words'][:10])}")
        if result['unknown_types'] > 10:
            lines.append(f"    (+{result['unknown_types'] - 10} more)")

    return "\n".join(lines)


# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 60)
    print("  LLPSI 难度评估工具 v1_2_0 (归一化覆盖阈值法)")
    print("=" * 60)

    # ---- Step 1: 建立映射表 ----
    print("\n[Step 1] 建立词→章节映射表（精确 + 归一化）...\n")
    word_map, normalized_map, chapter_stats = build_word_chapter_map()

    # 统计归一化带来的压缩比
    compression = (1 - len(normalized_map) / len(word_map)) * 100 if word_map else 0
    print(f"\n  精确词汇量: {len(word_map)} 个词形")
    print(f"  归一化词汇量: {len(normalized_map)} 个词形")
    print(f"  归一化压缩比: {compression:.1f}% (去长音+大小写后减少的词形比例)")

    # ---- Step 2: 覆盖阈值法评估抽样章节 ----
    print(f"\n[Step 2] 覆盖阈值法评估抽样章节 ({len(SAMPLE_CHAPTERS)} 章)...\n")

    eval_results = {}
    for ch in SAMPLE_CHAPTERS:
        text = read_main_text(ch)
        tokens = tokenize_text(text)
        result = evaluate_text_coverage(tokens, word_map, normalized_map)
        eval_results[ch] = result

    # ---- 输出: 汇总表 ----
    print("\n[汇总表] 覆盖阈值法 — 各章难度对比\n")
    print(format_coverage_summary(eval_results, chapter_stats))

    # ---- 输出: 详细评估 ----
    print("\n\n[详细评估]\n")
    for ch in SAMPLE_CHAPTERS:
        if ch in eval_results:
            print(format_coverage_result(ch, eval_results[ch], chapter_stats))
            print()

    # ---- Step 3: 自身验证 ----
    print("\n[Step 3] 自身验证 — 90% 覆盖阈值 vs 实际章节号\n")
    diffs = []
    for ch, r in eval_results.items():
        if r['difficulty'] is not None and r['sample_sufficient'] and not r.get('difficulty_degraded'):
            delta = r['difficulty'] - ch
            diffs.append(abs(delta))
            flag = " ✓" if abs(delta) <= 3 else (" ⚠" if abs(delta) <= 5 else " ← 偏差较大")
            print(f"  Cap.{ch:02d}  90%阈值={r['difficulty']:3d}  偏离={delta:+3d}{flag}")
        elif r.get('difficulty_degraded'):
            print(f"  Cap.{ch:02d}  降级 → 最高覆盖率{r['max_achievable']:.0f}%")
        else:
            print(f"  Cap.{ch:02d}  N/A")

    if diffs:
        avg_diff = sum(diffs) / len(diffs)
        print(f"\n  平均偏离: {avg_diff:.1f} 章")
        within_5 = sum(1 for d in diffs if d <= 5)
        print(f"  偏离 ≤5 章的比例: {within_5}/{len(diffs)} ({within_5/len(diffs)*100:.0f}%)")

    # ---- 保存映射表 ----
    print("\n[导出] 保存映射表...")
    base = Path(__file__).parent

    # 精确映射表
    exact_path = base / "word_chapter_map.json"
    with open(exact_path, 'w', encoding='utf-8') as f:
        json.dump(word_map, f, ensure_ascii=False, indent=2)
    print(f"  精确映射表: {exact_path} ({len(word_map)} 条)")

    # 归一化映射表
    norm_path = base / "word_chapter_map_normalized.json"
    with open(norm_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_map, f, ensure_ascii=False, indent=2)
    print(f"  归一化映射表: {norm_path} ({len(normalized_map)} 条)")

    print("\n" + "=" * 60)
    print("  评估完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
