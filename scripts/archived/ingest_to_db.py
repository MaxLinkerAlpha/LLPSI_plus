#!/usr/bin/env python3
"""
ingest_to_db.py — 把 segments.json 写入 SQLite 数据库
======================================================
表结构 (见 SKILL.md):
- books       (id, slug, title, author, fr_range, segment_kind)
- segments    (id, book_id, sequence, title, latin, word_count, fr_chapter)
- vocab       (segment_id, word_form, freq)   ← 反向索引
- fr_vocab    (chapter, word_form, is_new)    ← Familia Romana 各章词表

用法:
    python3 scripts/ingest_to_db.py --slug colloquia_personarum
    python3 scripts/ingest_to_db.py --init-fr-vocab
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter


# ============================================================
# 路径配置
# ============================================================
DEFAULT_DB = "data/llpsi_corpus.db"


# ============================================================
# 拉丁语单词提取 (与 segment_book.py 保持一致)
# ============================================================
WORD_RE = re.compile(
    r"[A-Za-zÄäÀàÁáÂâÆæÇçÉéÈèÊêĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž]+"
)


def extract_words(text: str) -> list[str]:
    """提取拉丁语词形 (lowercased, 保留 macron 字符)。"""
    return [w.lower() for w in WORD_RE.findall(text)]


# ============================================================
# Schema 初始化
# ============================================================
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS books (
    id           INTEGER PRIMARY KEY,
    slug         TEXT UNIQUE NOT NULL,
    title        TEXT NOT NULL,
    author       TEXT,
    fr_range     TEXT,
    segment_kind TEXT
);

CREATE TABLE IF NOT EXISTS segments (
    id          INTEGER PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    sequence    INTEGER NOT NULL,
    title       TEXT,
    latin       TEXT NOT NULL,
    word_count  INTEGER NOT NULL,
    fr_chapter  INTEGER,
    UNIQUE(book_id, sequence),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE TABLE IF NOT EXISTS vocab (
    segment_id  INTEGER NOT NULL,
    word_form   TEXT NOT NULL,
    freq        INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (segment_id, word_form),
    FOREIGN KEY (segment_id) REFERENCES segments(id)
);

CREATE INDEX IF NOT EXISTS idx_vocab_word ON vocab(word_form);

CREATE TABLE IF NOT EXISTS fr_vocab (
    chapter     INTEGER NOT NULL,
    word_form   TEXT NOT NULL,
    is_new      INTEGER NOT NULL,
    PRIMARY KEY (chapter, word_form)
);
"""


def init_schema(db_path: str):
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"  [Schema] {db_path} 初始化完成")


# ============================================================
# 已知 LLPSI 教材元数据 (FR 范围)
# ============================================================
BOOKS_META = {
    "colloquia_personarum": {
        "title": "Colloquia Personarum",
        "author": "Hans H. Ørberg",
        "fr_range": "1-24",
        "segment_kind": "dialogue",
    },
    "fabulae_personarum": {
        "title": "Fabulae Personarum",
        "author": "Hans H. Ørberg",
        "fr_range": "1-35",
        "segment_kind": "narrative",
    },
    "fabulae_syrae": {
        "title": "Fabulae Syrae",
        "author": "Luigi Miraglia",
        "fr_range": "25-34",
        "segment_kind": "narrative",
    },
    "fabellae_latinae": {
        "title": "Fabellae Latinae",
        "author": "Various",
        "fr_range": "1-25",
        "segment_kind": "narrative",
    },
    "sermones_romani": {
        "title": "Sermones Romani",
        "author": "Hans H. Ørberg (ed.)",
        "fr_range": "post-35",
        "segment_kind": "narrative",
    },
    "de_bello_gallico": {
        "title": "De Bello Gallico",
        "author": "C. Iulius Caesar (ed. Ørberg)",
        "fr_range": "post-35",
        "segment_kind": "narrative",
    },
    "cena_trimalchionis": {
        "title": "Cena Trimalchionis",
        "author": "Petronius (ed. Ørberg)",
        "fr_range": "45-47",
        "segment_kind": "narrative",
    },
    "aeneis": {
        "title": "Aeneis (Liber I & IV)",
        "author": "Vergilius (ed. Ørberg)",
        "fr_range": "40",
        "segment_kind": "verse",
    },
    "ars_amatoria": {
        "title": "Ars Amatoria",
        "author": "Ovidius (ed. Ørberg)",
        "fr_range": "40",
        "segment_kind": "verse",
    },
    "catilina": {
        "title": "In Catilinam (Sallust & Cicero)",
        "author": "Sallustius & Cicero (ed. Ørberg)",
        "fr_range": "56",
        "segment_kind": "narrative",
    },
    "amphitryo": {
        "title": "Amphitryo",
        "author": "Plautus (ed. Ørberg)",
        "fr_range": "post-35",
        "segment_kind": "drama",
    },
    "epitome_historiae_sacrae": {
        "title": "Epitome Historiae Sacrae",
        "author": "Lhomond",
        "fr_range": "post-35",
        "segment_kind": "narrative",
    },
    "de_rerum_natura": {
        "title": "De Rerum Natura",
        "author": "Lucretius (ed. Miraglia et al.)",
        "fr_range": "45",
        "segment_kind": "verse",
    },
    "roma_aeterna": {
        "title": "Roma Aeterna",
        "author": "Hans H. Ørberg",
        "fr_range": "post-35",
        "segment_kind": "narrative",
    },
}


# ============================================================
# Ingest segments.json → SQLite
# ============================================================
def ingest(slug: str, db_path: str, ocr_root: str = "ocr_output"):
    if slug not in BOOKS_META:
        print(f"  [警告] '{slug}' 不在 BOOKS_META, 写入通用元数据")
        meta = {"title": slug, "author": None, "fr_range": None, "segment_kind": None}
    else:
        meta = BOOKS_META[slug]

    segments_path = os.path.join(ocr_root, slug, "segments.json")
    if not os.path.exists(segments_path):
        print(f"  [错误] 找不到 {segments_path}", file=sys.stderr)
        sys.exit(1)

    with open(segments_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1) 写入 books 表 (idempotent)
    cur.execute("""
        INSERT INTO books (slug, title, author, fr_range, segment_kind)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            title=excluded.title,
            author=excluded.author,
            fr_range=excluded.fr_range,
            segment_kind=excluded.segment_kind
    """, (slug, meta["title"], meta["author"], meta["fr_range"], meta["segment_kind"]))

    cur.execute("SELECT id FROM books WHERE slug=?", (slug,))
    book_id = cur.fetchone()[0]

    # 2) 清空旧 segments/vocab (re-ingest)
    cur.execute("DELETE FROM segments WHERE book_id=?", (book_id,))

    # 3) 解析 Colloquia 的 fr_chapter (Colloquium N → FR Cap. N)
    fr_map = None
    if meta["fr_range"] and re.match(r"^\d+-\d+$", meta["fr_range"]):
        a, b = meta["fr_range"].split("-")
        fr_map = (int(a), int(b))

    # 4) 插入每段
    inserted = 0
    total_words = 0
    for seg in segments:
        # fr_chapter 解析优先级:
        #   1) 优先使用 segments.json 中已记录的值 (segment_book.py 解析过的最准确)
        #   2) Colloquia: 番外 idx == fr_chapter (Cap. 1-24)
        #   3) 否则 None
        seg_fr_ch = seg.get("fr_chapter")
        if seg_fr_ch is None and fr_map and fr_map[0] <= seg["arabic"] <= fr_map[1]:
            seg_fr_ch = seg["arabic"]

        cur.execute("""
            INSERT INTO segments (book_id, sequence, title, latin, word_count, fr_chapter)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (book_id, seg["sequence"], seg["title"], seg["text"], seg["word_count"], seg_fr_ch))

        seg_id = cur.lastrowid

        # 5) 词频统计 → 插入 vocab
        words = extract_words(seg["text"])
        counter = Counter(words)
        for w, c in counter.most_common():
            cur.execute("""
                INSERT OR REPLACE INTO vocab (segment_id, word_form, freq)
                VALUES (?, ?, ?)
            """, (seg_id, w, c))

        inserted += 1
        total_words += len(words)

    conn.commit()

    # 6) 统计
    cur.execute("SELECT COUNT(*) FROM vocab WHERE segment_id IN (SELECT id FROM segments WHERE book_id=?)",
                (book_id,))
    vocab_rows = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT word_form) FROM vocab WHERE segment_id IN (SELECT id FROM segments WHERE book_id=?)",
                (book_id,))
    unique_words = cur.fetchone()[0]

    conn.close()

    print(f"  [完成] 写入 {inserted} 段到 '{slug}'")
    print(f"  [完成] 词条行数: {vocab_rows} (不同词形: {unique_words})")
    print(f"  [完成] 总词数: {total_words}")


# ============================================================
# 初始化 fr_vocab (通用: FR 1-35 + RA 36-56)
# ============================================================
# 严格的拉丁词过滤规则: 与 vocab 表 (extract_words) 保持完全一致
LATIN_RE = re.compile(r"^[a-zāēīōūȳ]+$")


def _load_iterum_module():
    """动态加载 iterum_analysis.py 复用 split/tokenize 逻辑."""
    import importlib.util
    iterum_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iterum_analysis.py")
    spec = importlib.util.spec_from_file_location("iterum_analysis", iterum_path)
    if spec is None or spec.loader is None:
        print(f"  [错误] 找不到 {iterum_path}", file=sys.stderr)
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tokenize_chapter(mod, body: str) -> list[str]:
    """单章 tokenize + 噪声剔除 (与 init_fr_vocab 旧版保持完全一致)."""
    body_clean = mod.extract_readings_from_chapter(body)
    body_clean = re.sub(r'CAPITVLVM\s+\w+.*', '', body_clean)
    body_clean = re.sub(r'CAP\.\s+[IVX]+.*', '', body_clean)
    tokens = mod.tokenize(body_clean)
    tokens_clean: list[str] = []
    for t in tokens:
        t_low = t.lower()
        if len(t_low) <= 1:
            continue
        if not LATIN_RE.match(t_low):
            continue
        tokens_clean.append(t_low)
    return tokens_clean


def _load_chapter_words_from_db(cur, chapter_range: tuple[int, int]) -> set[str]:
    """从 fr_vocab 表加载指定章节范围的累计词表 (用于 RA 模式衔接 FR)."""
    cur.execute("""
        SELECT DISTINCT word_form FROM fr_vocab
        WHERE chapter BETWEEN ? AND ?
    """, chapter_range)
    return {r[0] for r in cur.fetchall()}


def _populate_vocab_from_text(db_path: str, text_path: str, label: str,
                              clear_existing: bool = True,
                              skip_chapters_before: int = 0) -> int:
    """从文本填充 fr_vocab 表. 通用化: 可处理 FR 文本 / RA 文本.

    Args:
        db_path: 数据库路径
        text_path: 拉丁语全文 (FR full.txt 或 RA _full.txt)
        label: 输出标签 (如 "FR 1-35" 或 "RA 36-56")
        clear_existing: 是否 DELETE fr_vocab (FR 模式=True, RA 模式=False 保留)
        skip_chapters_before: 跳过 chapter 编号 <= 此值的章 (RA 模式跳过 1-35)
    Returns:
        写入的章节数
    """
    if not os.path.exists(text_path):
        print(f"  [错误] 找不到 {text_path}", file=sys.stderr)
        sys.exit(1)

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 清理页码标记, 防止 page/cap/裸数字等噪声词进入 fr_vocab
    text = re.sub(r'={3,}.*?={3,}', '', text)
    text = re.sub(r'--- 第 \d+ 页 ---', '', text)
    text = re.sub(r'--- PAGE \d+ ---', '', text)
    text = re.sub(r'--- \d+ ---', '', text)

    mod = _load_iterum_module()
    chapters = mod.split_into_chapters(text)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if clear_existing:
        cur.execute("DELETE FROM fr_vocab")
        cumulative: set[str] = set()
    else:
        # RA 模式: 从数据库中已存在的 FR 累计词表开始, 让 is_new 累计逻辑跨 FR+RA 连贯
        cumulative = _load_chapter_words_from_db(cur, (1, skip_chapters_before))
        print(f"  [衔接] 从 fr_vocab[1-{skip_chapters_before}] 加载 {len(cumulative)} 个累计词形")

    written = 0
    for ch_num in sorted(chapters.keys()):
        if ch_num <= skip_chapters_before:
            continue
        body = chapters[ch_num]
        tokens_clean = _tokenize_chapter(mod, body)
        new = set(tokens_clean) - cumulative
        for w in tokens_clean:
            cur.execute("""
                INSERT OR REPLACE INTO fr_vocab (chapter, word_form, is_new)
                VALUES (?, ?, ?)
            """, (ch_num, w, 1 if w in new else 0))
        cumulative.update(tokens_clean)
        written += 1
        print(f"  [Cap. {ch_num}] tokens={len(tokens_clean)}, new={len(new)}, "
              f"cumulative={len(cumulative)}")

    conn.commit()
    conn.close()
    print(f"  [完成] {label}: 写入 {written} 章, fr_vocab 累计 {len(cumulative)} 词形")
    return written


def init_fr_vocab(db_path: str, analysis_dir: str = "analysis_output"):
    """从 iterum_analysis.py 输入文本 (FR 1-35) 填充 fr_vocab 表. 清空旧表."""
    mod = _load_iterum_module()
    _populate_vocab_from_text(db_path, mod.INPUT_FILE, "FR 1-35", clear_existing=True)


def init_ra_vocab(db_path: str, ra_text_path: str = "ocr_output/roma_aeterna/_full.txt"):
    """从 Roma Aeterna 全文填充 fr_vocab 表 (章 36-56). 不清空 FR 数据, 从 FR 35 累计衔接."""
    if not os.path.exists(ra_text_path):
        print(f"  [错误] 找不到 {ra_text_path}", file=sys.stderr)
        sys.exit(1)
    _populate_vocab_from_text(db_path, ra_text_path, "RA 36-56",
                              clear_existing=False, skip_chapters_before=35)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="书 slug (= ocr_output 目录名)")
    parser.add_argument("--ingest-all", action="store_true", dest="ingest_all",
                        help="一次性入库 BOOKS_META 中所有 slug (跳过缺失 segments.json 的)")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--init-schema", action="store_true", help="只初始化 schema")
    parser.add_argument("--init-fr-vocab", action="store_true", help="从 iterum_analysis 填充 fr_vocab (FR 1-35)")
    parser.add_argument("--init-ra-vocab", action="store_true", dest="init_ra_vocab",
                        help="从 RA 全文填充 fr_vocab (RA 36-56, 衔接 FR 累计)")
    parser.add_argument("--init-all-vocab", action="store_true", dest="init_all_vocab",
                        help="依次跑 --init-fr-vocab + --init-ra-vocab (推荐)")
    args = parser.parse_args()

    init_schema(args.db)

    if args.init_fr_vocab:
        init_fr_vocab(args.db)
        return

    if args.init_ra_vocab:
        init_ra_vocab(args.db)
        return

    if args.init_all_vocab:
        init_fr_vocab(args.db)
        init_ra_vocab(args.db)
        return

    if args.ingest_all:
        ok, fail, skip = 0, 0, 0
        for slug in BOOKS_META.keys():
            seg_path = os.path.join("ocr_output", slug, "segments.json")
            if not os.path.exists(seg_path):
                print(f"  [跳过] {slug} (无 segments.json)")
                skip += 1
                continue
            try:
                ingest(slug, args.db)
                ok += 1
            except SystemExit:
                fail += 1
        print(f"\n[汇总] 成功: {ok}, 失败: {fail}, 跳过: {skip}")
        return

    if not args.slug:
        parser.error("需要 --slug, --ingest-all 或 --init-fr-vocab")

    ingest(args.slug, args.db)


if __name__ == "__main__":
    main()
