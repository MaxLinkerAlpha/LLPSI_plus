#!/usr/bin/env python3
"""
macronize.py v1_0_0 — Latin Macronizer（长音标注器）

原理：
  1. 从所有已有长音的故事中提取词形→长音词形对照表
  2. 对缺少长音的故事逐词替换
  3. 一个无长音词可能对应多个长音版本（不同语法形式），取最常见的一个

用法：
  python macronize.py                    # 自动处理所有零长音故事  
  python macronize.py --dry-run           # 只预览不写入
  python macronize.py --file <path>       # 只处理指定文件
"""

import os, re, sys, argparse
from collections import defaultdict, Counter

MACRON_PATTERN = re.compile(r"[āēīōūȳĀĒĪŌŪȲ]")
UNMACRONED_PATTERN = re.compile(r"\b[a-zāēīōūȳ]+", re.IGNORECASE)

REALITATES_DIR = os.path.join(os.path.dirname(__file__), "realitates")


def extract_macron_map(realitates_dir: str) -> dict[str, str]:
    """从已有长音的故事中建立 '无长音词 → 有长音词' 的对照表。"""
    raw_map: dict[str, Counter[str]] = defaultdict(Counter)

    for root, dirs, fnames in os.walk(realitates_dir):
        for fname in fnames:
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            parts = content.split("---", 2)
            if len(parts) < 3:
                continue
            body = parts[2]

            if not MACRON_PATTERN.search(body):
                continue

            words = UNMACRONED_PATTERN.findall(body.lower())
            for w in words:
                if MACRON_PATTERN.search(w):
                    unaccented = w.translate(str.maketrans({
                        "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u", "ȳ": "y",
                        "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U", "Ȳ": "Y",
                    }))
                    raw_map[unaccented][w] += 1

    macron_map: dict[str, str] = {}
    for unaccented, counter in raw_map.items():
        macron_map[unaccented] = counter.most_common(1)[0][0]

    return macron_map


def add_macrons_to_body(body: str, macron_map: dict[str, str]) -> str:
    """对拉丁正文逐词替换长音。"""
    def replace_word(match):
        word = match.group(0)
        lower = word.lower()
        if lower in macron_map:
            replacement = macron_map[lower]
            if word[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            if word.isupper():
                replacement = replacement.upper()
            return replacement
        return word

    return UNMACRONED_PATTERN.sub(replace_word, body)


def process_file(filepath: str, macron_map: dict[str, str], dry_run: bool = False) -> bool:
    """处理单个文件，返回是否做了修改。"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  [跳过] 格式异常: {filepath}")
        return False

    front_matter = parts[1]
    body = parts[2]

    if MACRON_PATTERN.search(body):
        return False

    new_body = add_macrons_to_body(body, macron_map)

    if new_body == body:
        print(f"  [无变化] {filepath}")
        return False

    new_content = f"---{front_matter}---{new_body}"

    if dry_run:
        old_words = UNMACRONED_PATTERN.findall(body)
        new_words = UNMACRONED_PATTERN.findall(new_body.lower())
        changes = sum(1 for o, n in zip(old_words, new_words) if o.lower() != n.lower())
        print(f"  [预览] {os.path.relpath(filepath, REALITATES_DIR)} — 将修改 {changes} 个词")
        return True

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    if MACRON_PATTERN.search(new_body):
        print(f"  [完成] {os.path.relpath(filepath, REALITATES_DIR)}")
        return True
    else:
        print(f"  [警告] 写入后仍无长音: {filepath}")
        return False


def main():
    parser = argparse.ArgumentParser(description="给拉丁语故事自动添加长音")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不实际写入")
    parser.add_argument("--file", type=str, help="只处理指定文件")
    args = parser.parse_args()

    realitates_dir = REALITATES_DIR

    print("=" * 60)
    print("步骤 1: 从已有长音的故事中提取词形对照表...")
    macron_map = extract_macron_map(realitates_dir)
    print(f"  提取到 {len(macron_map)} 条词形映射")

    print()
    print("步骤 2: 处理缺少长音的故事...")
    print()

    count_modified = 0
    count_total = 0

    if args.file:
        filepath = args.file
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)
        count_total = 1
        if process_file(filepath, macron_map, args.dry_run):
            count_modified += 1
    else:
        for root, dirs, fnames in os.walk(realitates_dir):
            for fname in sorted(fnames):
                if not fname.endswith(".md"):
                    continue
                filepath = os.path.join(root, fname)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue
                body = parts[2]
                if MACRON_PATTERN.search(body):
                    continue
                count_total += 1
                if process_file(filepath, macron_map, args.dry_run):
                    count_modified += 1

    print()
    print("=" * 60)
    if args.dry_run:
        print(f"[预览完成] 共 {count_total} 篇无长音，{count_modified} 篇可修改")
    else:
        print(f"[完成] 共 {count_total} 篇无长音，{count_modified} 篇已添加长音")
    print("=" * 60)


if __name__ == "__main__":
    main()
