#!/usr/bin/env python3
"""
LLPSI OCR 最终清理 — 保守修复残留问题
只修复明确是OCR错误的情况，不修复模棱两可的
"""
import re
from pathlib import Path

OCR_DIR = Path("/Users/max/Downloads/Projects/LLPSI_plus/OCR")

# 明确的camelCase修复（已知专有名词缩写被粘合）
# 如 etQ. → et Q. (et + Quintus), abI → ab I
CAMEL_FIXES = {
    'etQ': 'et Q',
    'abI': 'ab I',
    'etM': 'et M',
    'cCēt': 'c Cēt',
    'kK': 'k K',
}

# 明确的数字-单词粘合修复（数字是行号，后面是单词开头）
# 这些是数字后紧跟字母形成的粘合，如 17n → 17 n
# 排除：数字+x（如10x是"10次"简写），数字+罗马数字


def fix_ocr_file(fpath):
    """修复单个OCR文件的残留问题"""
    try:
        text = fpath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  错误: {fpath.name}: {e}")
        return 0

    changes = 0
    orig = text

    # 1. 修复已知camelCase粘合
    for old, new in CAMEL_FIXES.items():
        # 使用词边界匹配
        pattern = re.compile(r'\b' + re.escape(old) + r'\b')
        count = len(pattern.findall(text))
        if count > 0:
            text = pattern.sub(new, text)
            changes += count

    # 2. 修复数字-单词粘合（保守：只修复数字+小写字母开头）
    # 排除：数字+x（如 10x），数字+v（如 1v = 罗马数字相关）
    # 只修复明确的：数字后跟普通拉丁字母
    def fix_num_word(match):
        nonlocal changes
        num = match.group(1)
        letter = match.group(2)
        # 排除数字+x（如10x是"10次"简写）
        if letter.lower() == 'x':
            return match.group(0)
        # 排除数字+罗马数字字母（如 1v, 1i, 1l, 1c, 1d, 1m）
        if letter.lower() in {'v', 'i', 'l', 'c', 'd', 'm'} and len(letter) == 1:
            return match.group(0)
        changes += 1
        return f"{num} {letter}"

    # 匹配：数字后紧跟小写字母
    text = re.sub(
        r'\b(\d{1,4})([a-zāēīōūȳ][a-zāēīōūȳ]*)\b',
        fix_num_word, text
    )

    if text != orig:
        fpath.write_text(text, encoding="utf-8")
        print(f"  {fpath.name}: {changes} 处修复")

    return changes


def main():
    ocr_files = sorted(OCR_DIR.rglob("*.txt"))
    total = 0
    fixed = 0

    for f in ocr_files:
        c = fix_ocr_file(f)
        total += 1
        if c > 0:
            fixed += 1

    print(f"\n扫描: {total} 个文件, 修复: {fixed} 个文件")


if __name__ == "__main__":
    main()