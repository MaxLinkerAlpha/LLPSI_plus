#!/usr/bin/env python3
"""
segment_book.py — 切段脚本 (v3: 支持多模式)
=====================================================
按 segmentation_rules.yaml 中的规则, 把 _full.txt 切成多个 segment,
输出 segments.json (每段带文本 + 元数据)。

支持的模式 (通过捕获组数量自动识别):
- 1 group:  (序数词)              - 适用于 Colloquia, Fabulae (旧)
- 2 groups: (序号, 标题)         - 适用于 Sermones (I. TITLE), Fabulae Syrae (1. NAME)
- 3 groups: (序号, 标题, 章节)   - 适用于 Fabellae (1. Title (cap. X))

附加:
- chapter_marker: 在切段过程中,持续追踪 "AD CAPITVLVM X" 这类行,
  把当前的 FR 章节写到 segment 的 fr_chapter 字段。
- skip_pages: 跳过前 N 个 PAGE 标记 (用于跳过扉页/目录)

用法:
    python3 scripts/segment_book.py --slug <name>
"""

import argparse
import json
import os
import re
import sys

import yaml


# ============================================================
# 罗马数字 / 序数词解析
# ============================================================
ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20,
    'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24, 'XXV': 25,
    'XXVI': 26, 'XXVII': 27, 'XXVIII': 28, 'XXIX': 29, 'XXX': 30,
    'XXXI': 31, 'XXXII': 32, 'XXXIII': 33, 'XXXIV': 34, 'XXXV': 35,
}

LATIN_ORDINALS = {
    'PRIMVM': 1, 'PRIMUM': 1,
    'SECVNDVM': 2, 'SECUNDUM': 2,
    'TERTIVM': 3, 'TERTIUM': 3,
    'QVARTVM': 4, 'QUARTUM': 4,
    'QVINTVM': 5, 'QUINTUM': 5,
    'SEXTVM': 6, 'SEXTUM': 6,
    'SEPTIMVM': 7, 'SEPTIMUM': 7,
    'OCTAVVM': 8, 'OCTAVUM': 8,
    'NONVM': 9, 'NONUM': 9,
    'DECIMVM': 10, 'DECIMUM': 10,
    'VNDECIMVM': 11, 'UNDECIMUM': 11,
    'DVODECIMVM': 12, 'DUODECIMUM': 12,
    'TERTIVM DECIMVM': 13, 'TERTIUM DECIMUM': 13,
    'QVARTVM DECIMVM': 14, 'QUARTUM DECIMUM': 14,
    'QVINTVM DECIMVM': 15, 'QUINTUM DECIMUM': 15,
    'SEXTVM DECIMVM': 16, 'SEXTUM DECIMUM': 16,
    'SEPTIMVM DECIMVM': 17, 'SEPTIMUM DECIMUM': 17,
    'DVODEVICESIMVM': 18, 'DUODEVICESIMUM': 18,
    'VNDEVICESIMVM': 19, 'UNDEVICESIMUM': 19,
    'VICESIMVM': 20, 'VICESIMUM': 20,
    'VNVM ET VICESIMVM': 21, 'UNUM ET VICESIMUM': 21,
    'ALTERVM ET VICESIMVM': 22, 'ALTERUM ET VICESIMUM': 22,
    'VICESIMVM TERTIVM': 23, 'VICESIMUM TERTIUM': 23,
    'VICESIMVM QVARTVM': 24, 'VICESIMUM QUARTUM': 24,
    'VICESIMVM QVINTVM': 25, 'VICESIMUM QUINTUM': 25,
    'VICESIMVM SEXTVM': 26, 'VICESIMUM SEXTUM': 26,
    'VICESIMVM SEPTIMVM': 27, 'VICESIMUM SEPTIMUM': 27,
    # Pars II (Roma Aeterna) Cap. 36-56
    'TRICESIMVM SEXTVM': 36, 'TRICESIMUM SEXTUM': 36,
    'TRICESIMVM SEPTIMVM': 37, 'TRICESIMUM SEPTIMUM': 37,
    'DVODEQVADRAGESIMVM': 38, 'DUODEQUADRAGESIMUM': 38,
    'VNDEQVADRAGESIMVM': 39, 'UNDEQUADRAGESIMUM': 39,
    'QVADRAGESIMVM': 40, 'QUADRAGESIMUM': 40,
    'VNVM ET QVADRAGESIMVM': 41, 'UNUM ET QUADRAGESIMUM': 41,
    'ALTERVM ET QVADRAGESIMVM': 42, 'ALTERUM ET QUADRAGESIMUM': 42,
    'QVADRAGESIMVM TERTIVM': 43, 'QUADRAGESIMUM TERTIUM': 43,
    'QVADRAGESIMVM QVARTVM': 44, 'QUADRAGESIMUM QUARTUM': 44,
    'QVADRAGESIMVM QVINTVM': 45, 'QUADRAGESIMUM QUINTUM': 45,
    'QVADRAGESIMVM SEXTVM': 46, 'QUADRAGESIMUM SEXTUM': 46,
    'QVADRAGESIMVM SEPTIMVM': 47, 'QUADRAGESIMUM SEPTIMUM': 47,
    'DVODEQVINQVAGESIMVM': 48, 'DUODEQUINQUAGESIMUM': 48,
    'VNDEQVINQVAGESIMVM': 49, 'UNDEQUINQUAGESIMUM': 49,
    'QVINQVAGESIMVM': 50, 'QUINQUAGESIMUM': 50,
    'VNVM ET QVINQVAGESIMVM': 51, 'UNUM ET QUINQUAGESIMUM': 51,
    'ALTERVM ET QVINQVAGESIMVM': 52, 'ALTERUM ET QUINQUAGESIMUM': 52,
    'QVINQVAGESIMVM TERTIVM': 53, 'QUINQUAGESIMUM TERTIUM': 53,
    'QVINQVAGESIMVM QVARTVM': 54, 'QUINQUAGESIMUM QUARTUM': 54,
    'QVINQVAGESIMVM QVINTVM': 55, 'QUINQUAGESIMUM QUINTUM': 55,
    'QVINQVAGESIMVM SEXTVM': 56, 'QUINQUAGESIMUM SEXTUM': 56,
}


def parse_ordinal(text: str) -> int | None:
    """解析任意序数词表示 → 整数。容忍 OCR 噪声 (l→I, O→V 等)。"""
    # OCR 噪声修复: 在 upper 之前先把小写 l 替换为 I
    t = text.strip().replace('l', 'I').replace('|', 'I').upper()
    if t in ROMAN_MAP:
        return ROMAN_MAP[t]
    if t in LATIN_ORDINALS:
        return LATIN_ORDINALS[t]
    # Fallback: 主格 (S 结尾, e.g. PRIMVS) → 宾格 (M 结尾, PRIMVM)
    # 覆盖 De Bello Gallico / Aeneis 等使用主格的文本
    if t.endswith('VS') or t.endswith('OS'):
        t_acc = t[:-1] + 'M'
        if t_acc in LATIN_ORDINALS:
            return LATIN_ORDINALS[t_acc]
    return None


def parse_cap_range(text: str) -> int | None:
    """解析 (cap. I-VII) / (cap. I-VIIT) / (cap. I-X X) 这种范围,返回起始章。

    内部预处理 OCR 噪声:
      - 移除空格 (罗马数字没有空格: X X → XX, X XIII → XXIII)
      - 修复常见 OCR 错误 (VIIT→VIII, XVIT→XVII, XVIIT→XVIII, XXIITI→XXIII)
    """
    t = text.strip()
    # ── OCR 噪声修复 ──
    # 1) 移除所有空格 (罗马数字内不应有空格)
    t = t.replace(' ', '')
    # 2) 修复常见错误字符 (T 被 OCR 混入, 长模式优先避免部分替换)
    t = t.replace('XXIITI', 'XXIII')   # cap. XXIII
    t = t.replace('XVIIT', 'XVIII')     # cap. XVIII
    t = t.replace('XVIT', 'XVII')       # cap. XVII
    t = t.replace('VIIT', 'VIII')       # cap. VIII
    # ── 解析范围: 取起始章号 ──
    m = re.match(r'^([IVXLC]+)(?:-[IVXLC]+)?$', t)
    if m:
        return ROMAN_MAP.get(m.group(1))
    return None


# ============================================================
# 文本清洗
# ============================================================
def clean_text(text: str) -> str:
    text = re.sub(r'--- PAGE \d+ ---', '', text)
    text = re.sub(r'^\s*\d{1,3}\s*$', '', text, flags=re.MULTILINE)
    # 常见页眉
    for header in ['COLLOQVIA PERSONARVM', 'FABELLAE LATINAE',
                   'SERMONES ROMANI', 'FABVLAE SYRAE']:
        text = re.sub(rf'^{header}\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ============================================================
# 拉丁语单词提取
# ============================================================
WORD_RE = re.compile(
    r"[A-Za-zÄäÀàÁáÂâÆæÇçÉéÈèÊêĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž]+"
)


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


# ============================================================
# 切段主函数
# ============================================================
def segment_book(slug: str, ocr_root: str = "ocr_output",
                 rules_path: str = "assets/segmentation_rules.yaml"):
    ocr_dir = os.path.join(ocr_root, slug)
    full_path = os.path.join(ocr_dir, "_full.txt")
    if not os.path.exists(full_path):
        print(f"  [错误] 找不到 {full_path}", file=sys.stderr)
        sys.exit(1)

    with open(rules_path, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)["books"]

    if slug not in rules:
        print(f"  [错误] segmentation_rules.yaml 中没有 '{slug}' 的规则", file=sys.stderr)
        sys.exit(1)

    rule = rules[slug]
    # 严格匹配大小写: 主体章节 "LIBER I" 不应匹配词汇表 "Liber -i n" 词条
    # 如果 rule 中显式 no_ignorecase=true, 才使用 IGNORECASE
    no_ic = bool(rule.get("no_ignorecase", False))
    pattern = re.compile(rule["segment_pattern"]) if no_ic else re.compile(rule["segment_pattern"], re.IGNORECASE)
    title_tpl = rule["title_template"]
    skip_pages = rule.get("skip_pages", 0)
    chapter_pat = re.compile(rule["chapter_marker"], re.IGNORECASE) if rule.get("chapter_marker") else None
    chapter_tpl = rule.get("chapter_title_template", "Cap. {ch}")
    segment_whole = bool(rule.get("segment_whole", False))  # 整段模式

    with open(full_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    if skip_pages > 0:
        # Bug 修复: 之前是 `full_text = full_text[m.end():]` 跳过的只是 PAGE 标记本身,
        # 仍保留了 PAGE N 内部内容. 正确做法是: 跳到下一个 PAGE 标记的位置, 然后
        # 把 PAGE N+1 标记本身也保留 (后续会被 clean_text 清理).
        # 实际策略: 每次 search 找到 PAGE N 标记, 把 full_text 截断到 PAGE N+1 标记开始.
        skipped_pages: list[int] = []
        for _ in range(skip_pages):
            m = re.search(r'--- PAGE (\d+) ---', full_text)
            if not m:
                break
            n = int(m.group(1))
            skipped_pages.append(n)
            # 找下一个 PAGE 标记的开始位置
            next_m = re.search(r'--- PAGE (\d+) ---', full_text[m.end():])
            if next_m:
                # 截断到下一个 PAGE 标记之前
                full_text = full_text[:m.start()] + full_text[m.end() + next_m.start():]
            else:
                # 没有下一个 PAGE 标记了, 说明 skip_pages 设大了
                full_text = full_text[:m.start()]
                break
        # 初始化 current_start_page 为跳过后的下一页
        if skipped_pages:
            current_start_page = skipped_pages[-1] + 1
        else:
            current_start_page = 1
    else:
        current_start_page = 1  # 默认 1,避免 unbound

    # ============================================================
    # 整段模式: 把整个 _full.txt 作为 1 段
    # ============================================================
    if segment_whole:
        # 整段入库: 跳过扉页/目录/词汇表后, 剩余所有正文作为 1 段
        body = clean_text(full_text)
        if not body:
            print(f"  [错误] 整段模式但清理后无内容", file=sys.stderr)
            sys.exit(1)
        # 兼容 title_template 用 {n} 或 {t}: 整段模式只填充 n
        try:
            title = title_tpl.format(n=1)
        except KeyError:
            # 如果模板用 {t}, 退化为只用 n 的简化模板
            try:
                title = title_tpl.format(n=1, t="(整段)")
            except KeyError:
                title = f"{title_tpl} 1"
        seg = {
            "roman": None,
            "arabic": 1,
            "title": title,
            "start_page": current_start_page,
            "fr_chapter": None,
            "sequence": 1,
            "text": body,
            "word_count": count_words(body),
        }
        segments = [seg]
        out_path = os.path.join(ocr_dir, "segments.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
        print(f"  [完成] 整段模式: 切出 1 段 ({seg['word_count']:,} 词)")
        print(f"  [完成] 输出: {out_path}")
        return

    lines = full_text.split("\n")
    segments: list[dict] = []
    current: dict | None = None
    current_lines: list[str] = []
    if skip_pages <= 0:
        current_start_page: int | None = None
    # 否则保留 if skip_pages>0 块中设置的 current_start_page
    current_chapter: int | None = None
    seq = 0

    page_re = re.compile(r"--- PAGE (\d+) ---")

    def flush():
        nonlocal current, current_lines, current_start_page, seq
        if current is None or not current_lines:
            return
        body = clean_text("\n".join(current_lines))
        if not body:
            current = None
            current_lines = []
            return
        seq += 1
        current["sequence"] = seq
        current["text"] = body
        current["word_count"] = count_words(body)
        # 如果本段没有 fr_chapter 但有追踪到的当前章节
        if current.get("fr_chapter") is None and current_chapter is not None:
            current["fr_chapter"] = current_chapter
        segments.append(current)
        current = None
        current_lines = []

    for line in lines:
        pm = page_re.search(line)
        if pm:
            current_start_page = int(pm.group(1))
            continue

        # 优先检查 chapter marker (用于追踪 FR 章节)
        if chapter_pat is not None:
            cm = chapter_pat.match(line.strip())
            if cm:
                ch_n = parse_ordinal(cm.group(1))
                if ch_n is not None:
                    current_chapter = ch_n
                # 不要 flush,继续 (因为本行不算段开头)

        m = pattern.match(line.strip())
        if m:
            flush()
            groups = m.groups()

            if len(groups) == 1:
                # 单 group: 序数词
                ordinal_part = groups[0].strip()
                n_int = parse_ordinal(ordinal_part)
                if n_int is None:
                    continue
                title = title_tpl.format(n=n_int)
                current = {
                    "roman": ordinal_part,
                    "arabic": n_int,
                    "title": title,
                    "start_page": current_start_page,
                    "fr_chapter": current_chapter,
                }
            elif len(groups) == 2:
                # 两 group: (序号, 标题)
                seq_str, title_str = groups
                n_int = parse_ordinal(seq_str) if seq_str.isalpha() else int(seq_str)
                title = title_tpl.format(n=n_int, t=title_str.strip())
                current = {
                    "roman": seq_str,
                    "arabic": n_int,
                    "title": title,
                    "start_page": current_start_page,
                    "fr_chapter": current_chapter,
                }
            elif len(groups) == 3:
                # 三 group: (序号, 标题, 章节范围/或注释)
                seq_str, title_str, cap_str = groups
                n_int = parse_ordinal(seq_str) if seq_str.isalpha() else int(seq_str)
                # cap_str 可能为 None (可选的第三组未匹配)
                fr_ch = parse_cap_range(cap_str) if cap_str else None
                title = title_tpl.format(n=n_int, t=title_str.strip())
                current = {
                    "roman": seq_str,
                    "arabic": n_int,
                    "title": title,
                    "start_page": current_start_page,
                    "fr_chapter": fr_ch if fr_ch is not None else current_chapter,
                }
            else:
                continue
            current_lines = []
        else:
            if current is not None or current_lines:
                current_lines.append(line)

    flush()

    out_path = os.path.join(ocr_dir, "segments.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"  [完成] 切出 {len(segments)} 段")
    print(f"  [完成] 输出: {out_path}")
    if segments:
        total_words = sum(s["word_count"] for s in segments)
        print(f"  [统计] 总词数: {total_words}")
        print(f"  [统计] 平均每段: {total_words // max(1, len(segments))} 词")
        print(f"  [样例] 前 5 段:")
        for s in segments[:5]:
            ch = s.get("fr_chapter")
            ch_str = f" → FR Cap. {ch}" if ch else ""
            print(f"          - {s['title']} (p.{s.get('start_page','?')}, "
                  f"{s['word_count']} 词{ch_str})")
        arabs = sorted(s["arabic"] for s in segments if s.get("arabic") is not None)
        # 缺失号
        if arabs:
            all_set = set(arabs)
            missing = set(range(min(arabs), max(arabs) + 1)) - all_set
            if missing:
                print(f"  [警告] 序号缺失: {sorted(missing)[:10]}{'...' if len(missing) > 10 else ''}")
        else:
            print(f"  [警告] 没有可解析的 arabic 序号")


def main():
    parser = argparse.ArgumentParser(description="Segment OCR output into colloquium/fabula/etc units")
    parser.add_argument("--slug", required=True, help="OCR 输出目录名 (= 书 slug)")
    parser.add_argument("--ocr-root", default="ocr_output")
    parser.add_argument("--rules", default="assets/segmentation_rules.yaml")
    args = parser.parse_args()
    segment_book(args.slug, args.ocr_root, args.rules)


if __name__ == "__main__":
    main()
