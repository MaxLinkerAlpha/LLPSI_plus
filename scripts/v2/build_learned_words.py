"""build_learned_words.py - 阶段1：扫描LLPSI 56章文本建立learned_words[N]

极简版v2算法的核心数据基础：
- 直接扫描LLPSI OCR文本而非依赖DB is_new标记
- 按章节累计真实已学词集
- 解决DB is_new标记滞后/不准确问题
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
FR_DIR = ROOT / "ocr_output" / "familia_romana" / "per_page_clean"
RA_DIR = ROOT / "ocr_output" / "roma_aeterna"
OUT = ROOT / "analysis_output" / "learned_words_v2.json"

# 罗马数字 → 阿拉伯数字
ROMAN = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8,
    'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20, 'XXI': 21, 'XXII': 22,
    'XXIII': 23, 'XXIV': 24, 'XXV': 25, 'XXVI': 26, 'XXVII': 27, 'XXVIII': 28,
    'XXIX': 29, 'XXX': 30, 'XXXI': 31, 'XXXII': 32, 'XXXIII': 33, 'XXXIV': 34,
    'XXXV': 35, 'XXXVI': 36, 'XXXVII': 37, 'XXXVIII': 38, 'XXXIX': 39, 'XL': 40,
    'XLI': 41, 'XLII': 42, 'XLIII': 43, 'XLIV': 44, 'XLV': 45, 'XLVI': 46,
    'XLVII': 47, 'XLVIII': 48, 'XLIX': 49, 'L': 50, 'LI': 51, 'LII': 52,
    'LIII': 53, 'LIV': 54, 'LV': 55, 'LVI': 56,
}

# 拉丁词提取正则
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ]+")


def strip_accents(s: str) -> str:
    """去除重音符号"""
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def extract_latin_words(text: str) -> set:
    """从文本提取拉丁词集合（小写，去重音）"""
    words = set()
    for raw in WORD_RE.findall(text):
        w = strip_accents(raw.lower())
        # 过滤：长度>1，纯字母
        if len(w) > 1 and re.match(r'^[a-z]+$', w):
            words.add(w)
    return words


def detect_chapter_in_page(page_text: str) -> int:
    """检测页面是否包含章节标记，返回章节号（罗马数字）；无标记返回0"""
    # 匹配 CAP. XXX 或 CAP.XX
    for m in re.finditer(r'\bCAP\.\s*([IVXLC]+)\b', page_text, re.IGNORECASE):
        roman = m.group(1).upper()
        if roman in ROMAN:
            return ROMAN[roman]
    return 0


def scan_book_pages(pages_dir: Path, start_chapter: int) -> dict:
    """扫描一本书的所有页面，返回 {chapter: set_of_words}"""
    # 先收集每页的章节归属
    pages = sorted(pages_dir.glob("page_*.txt"),
                   key=lambda p: int(re.search(r'\d+', p.stem).group()))

    # 第一次扫描：建立 (page_index → chapter) 映射
    # 逻辑：从起始章节开始，每遇到新章节标记就切换
    page_chapter = []
    current_chapter = start_chapter
    for i, p in enumerate(pages):
        text = p.read_text(encoding='utf-8', errors='replace')
        # 如果该页有更新的章节标记
        detected = detect_chapter_in_page(text)
        if detected and detected >= start_chapter:
            current_chapter = detected
        page_chapter.append(current_chapter)

    # 第二次扫描：按章节聚合词汇
    chapter_words = {}
    for i, p in enumerate(pages):
        text = p.read_text(encoding='utf-8', errors='replace')
        ch = page_chapter[i]
        words = extract_latin_words(text)
        chapter_words.setdefault(ch, set()).update(words)

    return chapter_words


def main():
    print("扫描 familia_romana (Cap.1-35)...")
    fr_words = scan_book_pages(FR_DIR, 1)
    print(f"  找到 {len(fr_words)} 个章节")

    print("扫描 roma_aeterna (Cap.36-56)...")
    ra_words = scan_book_pages(RA_DIR, 36)
    print(f"  找到 {len(ra_words)} 个章节")

    # 合并
    all_chapter_words = {**fr_words, **ra_words}

    # 计算累计已学词集
    cumulative = set()
    learned = {}
    for ch in range(1, 57):
        cumulative |= all_chapter_words.get(ch, set())
        learned[ch] = sorted(cumulative)

    # 统计
    print("\n章节词汇增长（去重音小写）:")
    for ch in [1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 56]:
        if ch in learned:
            print(f"  Cap.{ch:2d}: {len(learned[ch]):5d} 已学词 (本章节+{len(all_chapter_words.get(ch, set()))}个新词)")

    # 找出总表词集（56章全部）
    all_words = set()
    for ch in all_chapter_words:
        all_words |= all_chapter_words[ch]
    print(f"\nLLPSI 56章总词表: {len(all_words)} 个独立词形")

    # 输出
    OUT.parent.mkdir(parents=True, exist_ok=True)
    output = {
        'learned_per_chapter': learned,        # {1: ['a', 'ab', ...], ...}
        'new_per_chapter': {ch: sorted(all_chapter_words.get(ch, set()))
                            for ch in range(1, 57)},
        'llpsi_total_words': sorted(all_words),
        'chapter_word_count': {ch: len(learned[ch]) for ch in range(1, 57)},
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n已写入: {OUT}")


if __name__ == '__main__':
    main()
