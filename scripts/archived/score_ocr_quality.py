#!/usr/bin/env python3
"""OCR 文本质量评分 — 临时工具, 用于从 dooge 重复段中选质量更高的版本."""
import re
from pathlib import Path

SEG_DIR = Path("/Users/max/Downloads/Projects/LLPSI+++/analysis_output/extracted/d_class_stories")


def score_ocr_quality(text: str) -> dict:
    """OCR 文本质量评分. 各项加权汇总, 越高越好.

    评分项 (v1):
      + macron 字符数:    ā ē ī ō ū ȳ ǣ æ œ
      + 重音字符数:      á é í ó ú ý ḗ
      - 乱码字符数:      l·l, |, [unreadable], —, …, 多个 !
      + 拉丁可读词数:    \\b[a-zA-Z]{2,}\\b
    """
    # 1. 长音字符
    macrons = "āēīōūȳǣæœ"
    accents = "áéíóúýḗ"
    mac_count = sum(1 for c in text if c in macrons)
    acc_count = sum(1 for c in text if c in accents)

    # 2. 乱码字符 (OCR 误识别或破损标记)
    garbage_patterns = [
        r"l·l",          # OCR 误识
        r"\[unreadable",
        r"\[illegible",
        r"—+",           # 多破折号 (往往是 OCR 拼接断裂)
        r"…",
        r"!{2,}",        # 多 !
        r"\?{2,}",       # 多 ?
        r"l\s+l",        # 孤 l
        r"-\s*\n\s*",    # 行末连字符
    ]
    garbage_count = sum(len(re.findall(p, text)) for p in garbage_patterns)

    # 3. 可读拉丁词数
    word_count = len(re.findall(r"\b[a-zA-Z]{3,}\b", text))

    # 总分
    score = mac_count * 2.0 + acc_count * 1.0 - garbage_count * 3.0 + word_count * 0.05

    return {
        "macron": mac_count,
        "accent": acc_count,
        "garbage": garbage_count,
        "words": word_count,
        "score": round(score, 2),
    }


if __name__ == "__main__":
    pairs = [
        ("dooge_beginners_p214-219",   "dooge_beginners_2_p214-219"),
        ("dooge_beginners_p221-223",   "dooge_beginners_2_p221-223"),
    ]
    for a, b in pairs:
        fa = SEG_DIR / f"{a}.md"
        fb = SEG_DIR / f"{b}.md"
        if not fa.exists() or not fb.exists():
            print(f"  [SKIP] {a} or {b} not found")
            continue
        sa = score_ocr_quality(fa.read_text(encoding="utf-8"))
        sb = score_ocr_quality(fb.read_text(encoding="utf-8"))
        winner = a if sa["score"] >= sb["score"] else b
        print(f"\n  {a}:")
        print(f"    {sa}")
        print(f"  {b}:")
        print(f"    {sb}")
        print(f"  >> WINNER: {winner} (margin {abs(sa['score']-sb['score']):.2f})")
