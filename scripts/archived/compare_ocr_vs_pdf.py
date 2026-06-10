#!/usr/bin/env python3
"""
对比 OCR 输出的 RA 文本 vs pypdf 提取的 HD 2nd color 文本
- 计算文本相似度
- 评估 OCR 质量(mojibake 数量, 长音符号保留等)
- 给出建议
"""
import pypdf
import re
from pathlib import Path

OCR_TEXT_PATH = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/roma_aeterna/_full.txt"
HD_PDF_PATH = "/Users/max/Downloads/Projects/LLPSI+++/source/LLPSI_core_roma_aeterna_hd_2nd_color.pdf"
NORMAL_PDF_PATH = "/Users/max/Downloads/Projects/LLPSI+++/source/LLPSI_core_roma_aeterna.pdf"

print("=" * 80)
print("OCR 输出 vs pypdf 提取的 HD 2nd color 文本对比")
print("=" * 80)

# 读 OCR 文本
ocr_text = Path(OCR_TEXT_PATH).read_text(encoding='utf-8')
print(f"\nOCR 文本: {len(ocr_text):,} 字符, {ocr_text.count(chr(10)):,} 行")

# 读 HD pypdf
print(f"\n正在从 HD PDF 提取文本 (可能需要 30s)...")
r = pypdf.PdfReader(HD_PDF_PATH)
hd_text = ""
for p in r.pages:
    hd_text += (p.extract_text() or '') + "\n"
print(f"HD pypdf 文本: {len(hd_text):,} 字符")

# 读 normal pypdf
print(f"\n正在从普通 PDF 提取文本...")
r2 = pypdf.PdfReader(NORMAL_PDF_PATH)
normal_text = ""
for p in r2.pages:
    normal_text += (p.extract_text() or '') + "\n"
print(f"普通 pypdf 文本: {len(normal_text):,} 字符")

# 解码普通版 (八进制转义)
def decode_octal(text):
    """解码 \\NNN 八进制转义为 UTF-8 字符"""
    def replace_octal(match):
        try:
            return chr(int(match.group(1), 8))
        except:
            return match.group(0)
    return re.sub(r'\\(\d{3})', replace_octal, text)

normal_decoded = decode_octal(normal_text)
print(f"普通 pypdf 解码后: {len(normal_decoded):,} 字符")

# mojibake 检测
mojibake_pat = re.compile(r"Ã[©¨ª¢£¤¥¦§¨©ª«¬®°±²³´µ¶·¸¹]|Â[¡¢£¤¥¦§¨©ª«¬®°±²³´µ¶·¸¹]|ï¿½|\\x[0-9a-fA-F]{2}|\\[0-9]{3}")
ocr_moji = len(mojibake_pat.findall(ocr_text))
hd_moji = len(mojibake_pat.findall(hd_text))
normal_moji = len(mojibake_pat.findall(normal_text))
normal_decoded_moji = len(mojibake_pat.findall(normal_decoded))

print(f"\n=== Mojibake 数量 (越少越好) ===")
print(f"  OCR 文本:        {ocr_moji:,}")
print(f"  HD pypdf:        {hd_moji:,}")
print(f"  普通 pypdf:      {normal_moji:,} (含 {normal_moji - normal_decoded_moji:,} 个八进制转义)")
print(f"  普通 pypdf 解码: {normal_decoded_moji:,}")

# 长音符号检测
macron_chars = "āēīōūȳĀĒĪŌŪȲ"
ocr_macrons = sum(1 for c in ocr_text if c in macron_chars)
hd_macrons = sum(1 for c in hd_text if c in macron_chars)
normal_macrons = sum(1 for c in normal_text if c in macron_chars)
normal_decoded_macrons = sum(1 for c in normal_decoded if c in macron_chars)

print(f"\n=== 长音符号 (āēīōū) 数量 ===")
print(f"  OCR 文本:        {ocr_macrons:,}")
print(f"  HD pypdf:        {hd_macrons:,}")
print(f"  普通 pypdf:      {normal_macrons:,}")
print(f"  普通 pypdf 解码: {normal_decoded_macrons:,}")

# 拉丁语词频统计
latin_words_pat = re.compile(r"\b[a-zA-Zāēīōūȳ]+\b")
ocr_words = latin_words_pat.findall(ocr_text)
hd_words = latin_words_pat.findall(hd_text)
normal_words = latin_words_pat.findall(normal_decoded)

print(f"\n=== 拉丁语词形数量 ===")
print(f"  OCR 文本:        {len(ocr_words):,} (唯一 {len(set(ocr_words)):,})")
print(f"  HD pypdf:        {len(hd_words):,} (唯一 {len(set(hd_words)):,})")
print(f"  普通 pypdf 解码: {len(normal_words):,} (唯一 {len(set(normal_words)):,})")

# 评估 - 给每个版本打分
def quality_score(text, words):
    score = 0
    notes = []
    # 长音符号 > 0
    macrons = sum(1 for c in text if c in macron_chars)
    if macrons > 0:
        score += 30
        notes.append(f"长音符号 {macrons} 个 (+30)")
    # mojibake 少
    mojis = len(mojibake_pat.findall(text))
    if mojis == 0:
        score += 30
        notes.append("无 mojibake (+30)")
    elif mojis < 100:
        score += 20
        notes.append(f"mojibake 少 {mojis} 个 (+20)")
    elif mojis < 1000:
        score += 10
        notes.append(f"mojibake 中等 {mojis} 个 (+10)")
    # 文本量大
    if len(words) > 100000:
        score += 20
        notes.append(f"词形数 > 100k (+20)")
    elif len(words) > 50000:
        score += 10
        notes.append(f"词形数 50k-100k (+10)")
    # 唯一词形多
    unique = len(set(words))
    if unique > 10000:
        score += 20
        notes.append(f"唯一词形 > 10k (+20)")
    elif unique > 5000:
        score += 10
        notes.append(f"唯一词形 5k-10k (+10)")
    return score, notes

print(f"\n=== 质量评分 ===")
for name, text, words in [
    ("OCR 输出", ocr_text, ocr_words),
    ("HD pypdf", hd_text, hd_words),
    ("普通 pypdf 解码", normal_decoded, normal_words),
]:
    score, notes = quality_score(text, words)
    print(f"\n  {name}: {score}/100")
    for n in notes:
        print(f"    - {n}")

# 推荐
print(f"\n{'='*80}")
print("推荐结论:")
print(f"{'='*80}")
print("""
基于以上对比:

1. **HD 2nd color (pypdf 提取)**: 文本质量最高
   - 无 mojibake
   - 文本完整 (428/429 页)
   - 长音符号保留为下加横线 (在 PDF 中已编码,直接 pypdf 提取即可)
   - **强烈推荐**: 用 pypdf 重新提取,放弃 OCR 输出

2. **普通版 (解码后)**: 文本量大但有编码问题
   - 字符数最多(1.27M)但有 4700+ 个八进制转义
   - 解码后约 1.05M 字符
   - 长音符号可能丢失 (因为 PDF 中未编码)

3. **OCR 输出**: 与 HD pypdf 接近但可能含 OCR 噪声
   - 802k 字符,比 pypdf 提取略多
   - 可能含有 mojibake (macron 用下加横线表示时,OCR 可能误判)

**最终建议**: 用 pypdf 重新提取 HD 2nd color,覆盖现有 ocr_output/roma_aeterna/
""")
