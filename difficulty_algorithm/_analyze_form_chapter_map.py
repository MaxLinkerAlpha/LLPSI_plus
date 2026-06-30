#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 form_chapter_map.json 的完整脚本。
检查顶层结构、条目数、格式、重复key、chapter分布、异常值等。
"""

import json
import sys
import re
from collections import Counter, defaultdict
from pathlib import Path

FILE_PATH = Path(__file__).parent / "form_chapter_map.json"

def load_json(filepath: Path):
    """安全加载 JSON 文件，显式报错"""
    print(f"[INFO] 正在读取文件: {filepath}")
    print(f"[INFO] 文件大小: {filepath.stat().st_size / 1024:.1f} KB")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("[OK] 文件加载成功\n")
        return data
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 解析失败: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {filepath}")
        sys.exit(1)


def analyze():
    data = load_json(FILE_PATH)

    # ============================================================
    # 1. 顶层结构
    # ============================================================
    print("=" * 70)
    print("1. 顶层结构")
    print("=" * 70)
    if isinstance(data, dict):
        print(f"  类型: dict (key-value 映射)")
        print(f"  key 示例 (前10个): {list(data.keys())[:10]}")
        first_val = list(data.values())[0] if data else None
        print(f"  value 类型: {type(first_val).__name__}  示例: {first_val}")
    elif isinstance(data, list):
        print(f"  类型: list (数组)")
        print(f"  元素数量: {len(data)}")
        if data:
            print(f"  第一个元素类型: {type(data[0]).__name__}  示例: {data[0]}")
    else:
        print(f"  类型: {type(data).__name__} (非预期类型!)")

    # ============================================================
    # 2. 总条目数
    # ============================================================
    print("\n" + "=" * 70)
    print("2. 总条目数")
    print("=" * 70)
    if isinstance(data, dict):
        total = len(data)
    elif isinstance(data, list):
        total = len(data)
    else:
        total = 0
    print(f"  总条目数: {total:,}")

    # ============================================================
    # 3. 每个条目格式
    # ============================================================
    print("\n" + "=" * 70)
    print("3. 每个条目格式")
    print("=" * 70)
    if isinstance(data, dict):
        keys = list(data.keys())
        vals = list(data.values())
        print(f"  格式: {{\"<form>\": <chapter>}}")
        print(f"  示例: {{\"{keys[0]}\": {vals[0]}}}")
        print(f"  示例: {{\"{keys[1]}\": {vals[1]}}}")
        print(f"  示例: {{\"{keys[2]}\": {vals[2]}}}")
        # 检查 value 的类型分布
        val_types = Counter(type(v).__name__ for v in vals)
        print(f"  value 类型分布: {dict(val_types)}")
    elif isinstance(data, list):
        if data:
            elem0 = data[0]
            print(f"  元素类型: {type(elem0).__name__}")
            if isinstance(elem0, dict):
                print(f"  格式: {elem0}")
                # 检查所有元素的 key 集合
                all_keys = set()
                for e in data:
                    if isinstance(e, dict):
                        all_keys.update(e.keys())
                print(f"  所有元素的 key 集合: {all_keys}")
            else:
                print(f"  前3个元素: {data[:3]}")

    # ============================================================
    # 4. 重复 key 检查 (同一个 form 出现多次映射到不同 chapter)
    # ============================================================
    print("\n" + "=" * 70)
    print("4. 重复 key 检查 (同一个 form 映射到不同 chapter)")
    print("=" * 70)
    if isinstance(data, dict):
        # dict 的 key 天然唯一，无法出现重复 key 到不同 value
        # 但我们要检查：同一个 form 作为 key 只出现一次，所以不会有歧义
        print("  JSON 顶层是 dict，key 天然唯一。")
        print("  每个 form 只对应一个 chapter，不存在重复 key 的问题。")
        # 但是可以检查是否有 form 出现多次（大小写变体等）
        forms_lower = [k.lower() for k in data.keys()]
        lower_counter = Counter(forms_lower)
        lower_dups = {k: v for k, v in lower_counter.items() if v > 1}
        if lower_dups:
            print(f"  [注意] 忽略大小写后有 {len(lower_dups)} 个 form 出现了多次:")
            for k, v in list(lower_dups.items())[:10]:
                originals = [orig for orig in data.keys() if orig.lower() == k]
                print(f"    '{k}' -> {v} 次: {originals}")
        else:
            print(f"  忽略大小写后也没有重复。")
    elif isinstance(data, list):
        forms = [item.get("form") if isinstance(item, dict) else item for item in data]
        form_counter = Counter(forms)
        dups = {k: v for k, v in form_counter.items() if v > 1}
        if dups:
            print(f"  发现 {len(dups)} 个重复的 form:")
            for k, v in list(dups.items())[:20]:
                # 找到所有涉及的 chapter
                if isinstance(data[0], dict):
                    chapters = [item.get("chapter") for item in data if item.get("form") == k]
                    print(f"    '{k}' 出现 {v} 次, chapters: {chapters}")
        else:
            print("  没有重复的 form。")

    # ============================================================
    # 5. chapter 值分布
    # ============================================================
    print("\n" + "=" * 70)
    print("5. chapter 值分布")
    print("=" * 70)
    if isinstance(data, dict):
        chapters = list(data.values())
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        chapters = [item.get("chapter") for item in data]
    else:
        chapters = data

    chapter_counter = Counter(chapters)
    print(f"  唯一 chapter 值数量: {len(chapter_counter)}")
    print(f"  Chapter 分布 (按 chapter 编号排序):")
    for ch in sorted(chapter_counter.keys(), key=lambda x: (str(type(x).__name__), str(x))):
        count = chapter_counter[ch]
        bar = "#" * min(count // 100, 60)
        print(f"    Chapter {ch:>4}: {count:>6,} 条  {bar}")

    # ============================================================
    # 6. chapter 值范围检查
    # ============================================================
    print("\n" + "=" * 70)
    print("6. chapter 值范围检查 (预期: 1-36 或其他合理整数)")
    print("=" * 70)
    invalid_chapters = []
    for ch in set(chapters):
        if not isinstance(ch, int) or ch < 1 or ch > 56:  # 文件中有 cap37-cap56 的 vocab，放宽检查
            entries_with_ch = sum(1 for c in chapters if c == ch)
            invalid_chapters.append((ch, entries_with_ch))
    if invalid_chapters:
        print(f"  发现 {len(invalid_chapters)} 个异常 chapter 值:")
        for ch, count in sorted(invalid_chapters, key=lambda x: (str(type(x[0]).__name__), str(x[0]))):
            print(f"    chapter={ch!r} (类型: {type(ch).__name__}), 条目数: {count}")
    else:
        print("  所有 chapter 值都在合理范围内 (1-56)。")
    
    # 也显示最小和最大 chapter
    int_chapters = [c for c in chapters if isinstance(c, int)]
    if int_chapters:
        print(f"  chapter 最小值: {min(int_chapters)}, 最大值: {max(int_chapters)}")

    # ============================================================
    # 7. form 字段异常检查
    # ============================================================
    print("\n" + "=" * 70)
    print("7. form 字段异常检查")
    print("=" * 70)
    if isinstance(data, dict):
        all_forms = list(data.keys())
    elif isinstance(data, list):
        all_forms = [item.get("form", item) if isinstance(item, dict) else item for item in data]
    else:
        all_forms = []

    empty_forms = [f for f in all_forms if not f or str(f).strip() == ""]
    if empty_forms:
        print(f"  [WARNING] 发现 {len(empty_forms)} 个空 form!")
    else:
        print(f"  空值 form: 无")

    # 非拉丁字符检查
    non_latin_pattern = re.compile(r'[^a-zA-ZāēīōūȳĀĒĪŌŪȲȳaeiouyAEIOUYæÆœŒ]')  # 允许拉丁字母+长音符
    non_latin_forms = []
    for f in all_forms:
        if f:
            # 检查是否包含非预期字符 (允许字母、空格、连字符、撇号等)
            # 拉丁扩展字符范围检查
            non_latin = re.findall(r'[^a-zA-Z\u0100-\u024F \-\'\u2019]', str(f))
            if non_latin:
                non_latin_forms.append((f, non_latin))

    if non_latin_forms:
        print(f"  [WARNING] 发现 {len(non_latin_forms)} 个含非拉丁/异常字符的 form:")
        for f, chars in non_latin_forms[:20]:
            print(f"    '{f}' -> 异常字符: {chars}")
    else:
        print(f"  非拉丁字符: 无 (所有 form 均在拉丁字符范围内)")

    # 检查 form 长度分布
    form_lengths = [len(str(f)) for f in all_forms if f]
    if form_lengths:
        print(f"  form 长度: 最短={min(form_lengths)}, 最长={max(form_lengths)}, 平均={sum(form_lengths)/len(form_lengths):.1f}")
        # 找出特别长的 form
        long_forms = [(f, len(str(f))) for f in all_forms if f and len(str(f)) > 30]
        if long_forms:
            print(f"  超长 form (>30字符): {len(long_forms)} 个")
            for f, l in sorted(long_forms, key=lambda x: -x[1])[:10]:
                print(f"    [{l}字符] '{f}'")

    # ============================================================
    # 8. form 映射到多个 chapter (歧义检查)
    # ============================================================
    print("\n" + "=" * 70)
    print("8. form 映射多 chapter 检查 (歧义)")
    print("=" * 70)
    if isinstance(data, dict):
        # dict 下每个 form 只映射一个 chapter，天然无歧义
        print("  JSON 是 dict 结构，每个 form 只映射到一个 chapter。")
        print("  本身不存在歧义问题。")
        # 但如果外部使用时有歧义（同一个 form 在不同语境中属于不同 chapter）
        # 这里文件结构上不存在
    elif isinstance(data, list):
        form_to_chapters = defaultdict(set)
        for item in data:
            if isinstance(item, dict):
                f = item.get("form")
                c = item.get("chapter")
                if f and c:
                    form_to_chapters[f].add(c)
        multi_chapter_forms = {k: v for k, v in form_to_chapters.items() if len(v) > 1}
        if multi_chapter_forms:
            print(f"  发现 {len(multi_chapter_forms)} 个 form 映射到多个 chapter:")
            for f, chs in list(multi_chapter_forms.items())[:20]:
                print(f"    '{f}' -> chapters: {chs}")
        else:
            print("  没有 form 映射到多个 chapter。")

    # ============================================================
    # 9. form 频率分布 (按首字母/长度等)
    # ============================================================
    print("\n" + "=" * 70)
    print("9. form 字段统计")
    print("=" * 70)
    if all_forms:
        # 首字母分布
        first_char_counter = Counter(str(f)[0].upper() if f and str(f) else '?' for f in all_forms)
        print(f"  首字母分布 (Top 10):")
        for char, cnt in first_char_counter.most_common(10):
            bar = "#" * max(cnt // 50, 1)
            print(f"    '{char}': {cnt:>5,} {bar}")

        # 最短/最长 form
        valid_forms = [(f, len(str(f))) for f in all_forms if f]
        shortest = sorted(valid_forms, key=lambda x: x[1])[:10]
        longest = sorted(valid_forms, key=lambda x: -x[1])[:10]
        print(f"\n  最短的 10 个 form:")
        for f, l in shortest:
            print(f"    [{l}字符] '{f}'")
        print(f"\n  最长的 10 个 form:")
        for f, l in longest:
            print(f"    [{l}字符] '{f}'")

    # ============================================================
    # 10. 样本: 前20 + 后20
    # ============================================================
    print("\n" + "=" * 70)
    print("10. 样本展示")
    print("=" * 70)
    if isinstance(data, dict):
        items = list(data.items())
        print(f"\n  前 20 个条目:")
        for i, (k, v) in enumerate(items[:20], 1):
            print(f"    {i:>3}. '{k}' -> chapter {v}")
        print(f"\n  后 20 个条目:")
        for i, (k, v) in enumerate(items[-20:], len(items) - 19):
            print(f"    {i:>3}. '{k}' -> chapter {v}")
    elif isinstance(data, list):
        print(f"\n  前 20 个条目:")
        for i, item in enumerate(data[:20], 1):
            print(f"    {i:>3}. {item}")
        print(f"\n  后 20 个条目:")
        for i, item in enumerate(data[-20:], len(data) - 19):
            print(f"    {i:>3}. {item}")

    print("\n" + "=" * 70)
    print("分析完成")
    print("=" * 70)


if __name__ == "__main__":
    analyze()
