---
name: "llpsi-scaffolding-database"
description: "Builds a content database from LLPSI supplementary materials (Colloquia, Fabulae Syrae, etc.) and matches Latin text excerpts to specific Familia Romana chapters by vocabulary profile. Invoke when the user wants to OCR a new LLPSI book, populate the database, segment it, run word-frequency analysis, or find excerpts matching a target chapter's known-words / new-words profile."
---

# LLPSI Scaffolding Database Pipeline

A **database-first** approach to solving the LLPSI "Chapter 9 Wall" problem: instead of generating Latin text with AI as the primary content source, this skill builds a queryable database of authoritative LLPSI supplementary readings and matches excerpts to specific Familia Romana chapters based on vocabulary fit.

> **Design principle**: Authority > AI. The database grows more valuable with every book added. AI generation is only a fallback when the database has no suitable excerpt.

---

## When to Use This Skill

Invoke this skill when the user:

1. Wants to **add a new LLPSI book** (or any Latin reader) to the content pool
2. Asks to **OCR a PDF** from the `source/` folder
3. Wants to **run word-frequency analysis** on a book or chapter
4. Wants to **find excerpts** matching a specific target chapter (e.g., "what should a Cap. 10 learner read?")
5. Asks to **extend the database** with new metadata, new segmentation rules, or new matching algorithms
6. Wants to **verify** whether a given excerpt is suitable for a given chapter

Do **not** invoke for: AI text generation as the primary task (that's `ampliata_generate.py`'s job), web UI, or non-Latin content.

---

## Core Architecture

```
┌────────────────────────────────────────────────────┐
│  source/  (PDFs - authoritative Latin readers)     │
└────────────┬───────────────────────────────────────┘
             │ OCR (Tesseract, lat)
             ▼
┌────────────────────────────────────────────────────┐
│  ocr_output/<book_slug>/page_NNN.txt               │
│  (per-page clean text, macrons corrected)          │
└────────────┬───────────────────────────────────────┘
             │ Segment (rule-based per book)
             ▼
┌────────────────────────────────────────────────────┐
│  data/llpsi_corpus.db (SQLite)                     │
│  ┌──────────┬──────────┬──────────────────┐         │
│  │ books    │ segments │ vocab (M2M)      │         │
│  │ id,slug, │ id,book, │ segment_id,      │         │
│  │ title,   │ sequence,│ word_form,       │         │
│  │ type,    │ latin,   │ freq_in_segment  │         │
│  │ fr_range │ word_cnt │                  │         │
│  └──────────┴──────────┴──────────────────┘         │
└────────────┬───────────────────────────────────────┘
             │ Match query: target chapter + known_words + new_words
             ▼
┌────────────────────────────────────────────────────┐
│  Top-N ranked excerpts with fit scores             │
│  (coverage of known + hit-rate of new)             │
└────────────────────────────────────────────────────┘
```

---

## Database Schema (Single Source of Truth)

```sql
-- One row per source book
CREATE TABLE books (
    id           INTEGER PRIMARY KEY,
    slug         TEXT UNIQUE NOT NULL,    -- e.g. "colloquia_personarum"
    title        TEXT NOT NULL,           -- "Colloquia Personarum"
    author       TEXT,                    -- "Hans H. Ørberg"
    fr_range     TEXT,                    -- "1-24" | "25-34" | "1-25" | "post-35"
    segment_kind TEXT                     -- "dialogue" | "narrative" | "verse" | "drama"
);

-- One row per excerpt (the matching unit)
CREATE TABLE segments (
    id          INTEGER PRIMARY KEY,
    book_id     INTEGER NOT NULL,
    sequence    INTEGER NOT NULL,         -- order within the book
    title       TEXT,                     -- "Colloquium 1" or auto-generated
    latin       TEXT NOT NULL,            -- full Latin text
    word_count  INTEGER NOT NULL,
    fr_chapter  INTEGER,                  -- FR chapter this segment targets (if known)
    UNIQUE(book_id, sequence),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Reverse index: every (segment, word) pair the segment contains
CREATE TABLE vocab (
    segment_id  INTEGER NOT NULL,
    word_form   TEXT NOT NULL,            -- surface form, lowercased, macrons kept
    freq        INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (segment_id, word_form),
    FOREIGN KEY (segment_id) REFERENCES segments(id)
);

-- Index for fast reverse lookup
CREATE INDEX idx_vocab_word ON vocab(word_form);

-- Cached FR chapter vocabulary (loaded once from analysis_output)
CREATE TABLE fr_vocab (
    chapter     INTEGER NOT NULL,         -- 1..35
    word_form   TEXT NOT NULL,
    is_new      INTEGER NOT NULL,         -- 1 = introduced in this chapter, 0 = already known
    PRIMARY KEY (chapter, word_form)
);
```

**Why this shape**:
- `segments` is the matching unit (a dialogue, a paragraph, a chapter — depends on book)
- `vocab` is a flat M2M table — fast to query "which segments contain word X?" via the index
- `fr_vocab` decouples the matching function from any re-OCR of the FR text
- All word forms are **surface forms** (no lemmatization dependency) — keeps the pipeline zero-NLP

**fr_chapter resolution priority** (when ingesting a segment):
1. Use the value already set in `segments.json` (parsed by `segment_book.py` from explicit annotations)
2. For Colloquia Personarum: the colloquium number == FR chapter (1-24)
3. Otherwise `NULL`

---

## The 5-Step Pipeline

### Step 1 — OCR a book

**Script**: `scripts/ocr_book.py` (parameterized version of `ocr_familia_romana.py`)

```bash
python3 scripts/ocr_book.py \
    --pdf "source/LLPSI_Supplementa_Colloquia_Personarum.pdf" \
    --slug colloquia_personarum \
    --dpi 350
```

Output: `ocr_output/colloquia_personarum/page_001.txt ... page_NNN.txt`

### Step 2 — Segment & clean

**Script**: `scripts/segment_book.py`

Each book needs a **segmentation rule** (declared in `assets/segmentation_rules.yaml`):

| Book | Segment on | Title pattern |
|:----|:----------|:--------------|
| Colloquia Personarum | "Colloquium N" markers | `Colloquium {N}` |
| Fabellae Latinae | "Fabula N" markers | `Fabula {N}` |
| Fabulae Syrae | "Fabula N" markers | `Fabula Syra {N}` |
| Sermones Romani | "Sermo N" markers | `Sermo {N}` |
| De Bello Gallico | Book/Chapter markers | `Liber {N}` |
| Cena Trimalchionis | Continuous prose, split at scene breaks | auto |
| Aeneis | Book numbers | `Liber {N}` |

The script:
1. Concatenates per-page text
2. Applies the segmentation regex
3. Strips page numbers, headers/footers
4. Normalizes whitespace and macrons
5. Computes `word_count` per segment

### Step 3 — Ingest to SQLite

**Script**: `scripts/ingest_to_db.py`

```bash
python3 scripts/ingest_to_db.py \
    --slug colloquia_personarum \
    --segment-rule "colloquium_n"
```

Inserts rows into `books`, `segments`, and `vocab`. Idempotent — re-runs replace the book's data.

### Step 4 — Build the matching function

**Script**: `scripts/match_segments.py`

The matching function takes:
- `target_chapter` (1..35)
- `known_words` (set of word forms in Cap. 1 to N-1)
- `new_words` (set of word forms newly introduced in Cap. N)
- `top_n` (default 5)

For each segment in the database, it computes:

```
fit_score = w1 * known_coverage
          + w2 * new_hits_normalized
          + w3 * new_density
```

Where:
- `known_coverage`      = (known hits) / (segment word count)         high →大量用熟词,可读性强
- `new_hits_normalized` = (new hits) / |target new words|            high →覆盖更多本章新词
- `new_density`         = (new hits) / (segment word count)          high →新词集中,聚焦本章

Default weights: `w1=0.4, w2=0.4, w3=0.2` (tune via `--w1 --w2 --w3`).

```bash
python3 scripts/match_segments.py \
    --chapter 8 9 10 11 12 13 25 \
    --top-n 5
```

Output: top N segments sorted by fit, with per-segment score breakdown.

### Step 5 — Human verification

For each priority chapter (8, 9, 10, 11, 12, 13, 25), run matching and check:
- Does the recommended excerpt actually fit the chapter's topic?
- Are there unknown words sneaking in (vocab check)?

This step is **the only manual loop** — and it's fast: 7 chapters × 30 seconds each = ~5 min.

---

## File Layout

```
LLPSI+++/
├── source/                          # 35 输入 PDFs (按 LLPSI_<category>_<title>.ext 命名)
│   ├── LLPSI_core_*                 # 核心教材: familia_romana, roma_aeterna, indices
│   │                               #   ├ _text_selectable (可选中文字,无需 OCR)
│   │                               #   └ _hd_2nd_color (高清 2 版,优先使用)
│   ├── LLPSI_grammar_*              # 语法书: grammatica_latina, instructions
│   ├── LLPSI_exercitia_*            # 练习册: latina_I, latina_II
│   ├── LLPSI_vocab_*                # 词汇表: latine_anglicus, gallicus, hispanicus, multilingue
│   ├── LLPSI_multimedia_*           # 多媒体: latine_disco
│   ├── LLPSI_reader_*               # 补充读物: colloquia_personarum, fabulae_syrae, ...
│   │                               #   └ _v1_scan (旧版扫描件,仅作备用)
│   ├── LLPSI_companion_*            # 配套教师手册 (neumann 等)
│   └── LLPSI_teacher_*              # 教师资源: materials_and_answer_key, conseils_au_prof
├── ocr_output/
│   ├── familia_romana/              # FR 全书 OCR
│   │   ├── clean.txt                # 清洗后全文 (用于切段)
│   │   ├── full.txt                 # 原始全文
│   │   ├── per_page_raw/            # 原始每页 OCR
│   │   └── per_page_clean/          # 长音符合修正后的每页文本
│   ├── roma_aeterna/                # RA 全书 OCR
│   │   ├── _full.txt
│   │   └── page_NNN.txt
│   ├── colloquia_personarum/        # 配套读物 (Cap. 1-24 配套)
│   ├── fabulae_syrae/               # 神话故事 (Cap. 26-34 配套)
│   ├── fabellae_latinae/            # 短篇故事 (Cap. 1-25)
│   └── sermones_romani/             # 罗马风情短文 (Post-Cap. 35)
├── assets/
│   ├── segmentation_rules.yaml      # one rule per book (含 OCR 噪声修复正则)
│   ├── style_guide.md               # LLPSI writing principles (extracted from LLPSI_Research.md)
│   └── chapter_meta.yaml            # per-chapter wall_type, focus words, etc.
├── data/
│   └── llpsi_corpus.db              # SQLite database (the asset)
├── scripts/
│   ├── ocr_book.py                  # parameterised OCR
│   ├── ocr_familia_romana.py        # FR 专用 OCR (旧版, 建议改用 ocr_book.py)
│   ├── ocr_postprocess.py           # 长音符合修正 (macron fixes)
│   ├── segment_book.py              # rule-based segmentation (v3, 多模式切段)
│   ├── ingest_to_db.py              # populate SQLite (idempotent)
│   ├── match_segments.py            # the matching function
│   ├── rename_source.py             # bulk-rename source PDFs
│   ├── cleanup_source.py            # 重复文件清理
│   ├── analyze_book.py              # 通用词频分析 (FR/RA 通用)
│   ├── iterum_analysis.py           # FR 词频分析 (核心实现)
│   ├── merge_analysis.py            # FR+RA 数据合并
│   ├── generate_combined_viz.py     # 合并 HTML 可视化生成
│   └── ampliata_generate.py         # AI 微阅读生成 (Phase 1 MVP)
├── analysis_output/                 # 词频分析产出物
│   ├── chapter_stats.csv            # FR 35 章统计
│   ├── analysis_report.md           # FR 词频分析报告
│   ├── roma_aeterna_chapter_stats.csv
│   ├── roma_aeterna_analysis_report.md
│   ├── combined_stats.csv           # FR+RA 合并 (宽格式)
│   ├── combined_long.csv            # FR+RA 合并 (长格式, 供可视化)
│   └── combined_priority_report.md  # 合并后的学习优先级建议
├── supplements/                     # AI-generated drafts (fallback)
├── viz_output/                      # HTML 可视化
│   ├── familia_romana_insights.html # FR 单独词频可视化
│   ├── llpsi_fr_ra_insights.html    # FR+RA 合并难度曲线 (主)
│   └── _archive/                    # 历史 debug 截图
└── docs/                            # 全部项目文档
    ├── Project_Plan.md              # 主项目计划
    ├── LLPSI_Research.md            # LLPSI 方法论研究报告
    ├── LLPSI精读项目研判成本.md       # 中文成本研判
    ├── PRD_VISIO_ROMANA.md          # 可视化页面 PRD
    └── Technical_Architecture_VISIO_ROMANA.md
```

### Naming convention for `source/`

| Prefix | Meaning | Examples |
|:-------|:--------|:---------|
| `LLPSI_core_*` | Core textbooks | `LLPSI_core_familia_romana.pdf`, `LLPSI_core_roma_aeterna_hd_2nd_color.pdf` |
| `LLPSI_grammar_*` | Grammar & instructions | `LLPSI_grammar_grammatica_latina.pdf` |
| `LLPSI_exercitia_*` | Exercise books | `LLPSI_exercitia_latina_I.pdf`, `LLPSI_exercitia_nova_I_soluta.pdf` |
| `LLPSI_vocab_*` | Vocabulary lists | `LLPSI_vocab_latine_anglicus_I.pdf`, `LLPSI_vocab_multilingue.pdf` |
| `LLPSI_multimedia_*` | Multimedia | `LLPSI_multimedia_latine_disco.pdf` |
| `LLPSI_companion_*` | Companion/teachers' guides | `LLPSI_companion_familia_romana_neumann.pdf` |
| `LLPSI_reader_*` | Supplementary readers | `LLPSI_reader_fabulae_syrae.pdf`, `LLPSI_reader_aeneis.pdf` |
| `LLPSI_teacher_*` | Teacher materials | `LLPSI_teacher_materials_and_answer_key.pdf` |
| `LLPSI_indices_*` | Indices | `LLPSI_core_indices.pdf` |

Rules:
- All lowercase, underscore-separated (no spaces, no author names)
- All files carry the `LLPSI_` prefix for easy filtering
- `_v1_scan` suffix marks archived/legacy editions
- `_text_selectable` suffix marks PDFs with selectable text (no OCR needed)
- `_hd_2nd_color` suffix marks the 2nd-edition high-definition color version (preferred)
- `_alt` suffix marks an alternative edition of the same book (e.g. different scan)

### Complete Source Inventory (v1.2.0, 2026-06-06)

**Core textbooks** (LLPSI_core_*):
- `familia_romana.pdf` (latest, text-selectable)
- `familia_romana_hd_2nd_color_text_selectable.pdf`
- `familia_romana_hd_color_small.pdf` (compact HD)
- `familia_romana_v1_scan.pdf`, `familia_romana_2003_v1_scan.pdf` (legacy scans)
- `roma_aeterna.pdf` (latest, text-selectable)
- `roma_aeterna_hd_2nd_color.pdf`, `roma_aeterna_hd_2nd_color_alt.pdf` (HD scans, used for OCR)
- `roma_aeterna_v1_bw.pdf`, `roma_aeterna_v1_scan.pdf`, `roma_aeterna_v1_scan_sm.pdf`, `roma_aeterna_1990_v1_scan.pdf` (legacy)
- `indices.pdf`, `indices_v1.pdf`

**Grammar & instructions** (LLPSI_grammar_*):
- `grammatica_latina.pdf`, `grammatica_latina_v1.pdf`
- `instructions.pdf`, `instructions_v1.pdf`, `instructions_v1_sm.pdf`

**Exercise books** (LLPSI_exercitia_*):
- `latina_I.pdf` (1st Ed. companion to FR)
- `latina_II.pdf`, `latina_II_v1.pdf` (companion to RA)
- `nova_I_soluta.pdf` (Nova Exercitia Latina — worked solutions)
- `nova_I_answers.pdf` (answer key only)

**Vocabulary lists** (LLPSI_vocab_*):
- `latine_anglicus_I.pdf` (English vocabulary for FR)
- `latine_anglicus_I_II.pdf`, `latine_anglicus_I_II_v1.pdf` (English vocab for FR+RA combined)
- `latine_gallicus_I.pdf` (French vocab for FR)
- `latine_hispanicus_I.pdf` (Spanish vocab for FR)
- `multilingue.pdf`, `multilingue.xlsx` (multilingual wordlist)

**Multimedia** (LLPSI_multimedia_*):
- `latine_disco.pdf`

**Companion / Teacher's guides** (LLPSI_companion_*):
- `familia_romana_neumann.pdf` (Heinrich Neumann, comprehensive FR guide)
- `familia_romana_2007_v1.djvu` (legacy 2007 DjVu version)
- `roma_aeterna_neumann.pdf` (Heinrich Neumann, RA guide)

**Supplementary readers** (LLPSI_reader_*):
- `aeneis.pdf` — Virgil's Aeneid (adapted, Cap. 35+)
- `amphitryo.pdf` — Plautus' Amphitruo (comedy, Post-Cap. 35)
- `ars_amatoria.pdf` — Ovid's Art of Love (excerpts, Post-Cap. 35)
- `bello_gallico.pdf` — Caesar's Gallic War (excerpts)
- `catilina.pdf` — Sallust's Bellum Catilinae
- `cena_trimalchionis.pdf` — Petronius' Satyricon excerpt
- `colloquia_personarum.pdf` — 24 Colloquia dialogues (Cap. 1-24) **[INGESTED]**
- `colloquia_personarum_v1_scan.pdf` — legacy scan
- `de_rerum_natura.pdf` — Lucretius (excerpts)
- `epitome_historiae_sacrae.pdf` — Sacred History (Bible stories in Latin)
- `fabellae_latinae.pdf` — 22 short fables **[INGESTED]**
- `fabulae_syrae.pdf` — 27 Greek myths (Cap. 26-34) **[INGESTED]**
- `fabulae_syrae_1st_ed.pdf` — 1st edition variant
- `sermones_romani.pdf` — 11 Roman-themed readings **[INGESTED]**

**Teacher materials** (LLPSI_teacher_*):
- `materials_and_answer_key.pdf` (combined)
- `conseils_au_prof.pdf` (French)
- `nova_via_latine_doceo.pdf` (Italian)

**Vocabulary lists per reader** (LLPSI_vocab_*):
- `aeneis.pdf`, `bello_gallico.pdf`, `cena_trimalchionis.pdf`, `colloquia_personarum.pdf`, `sermones_romani.pdf`

### Current Pipeline State (v1.6.0)

**Database `data/llpsi_corpus.db`** contains 13 ingested books (197 segments, ~408k words, ~118k unique word forms):

| Book slug | Segments | Words | fr_chapter coverage | Mode | Source |
|:----------|---------:|------:|:--------------------|:-----|:-------|
| `colloquia_personarum` | 45 | 17,249 | Cap. 1-24 (each split into ~2 parts) | segment | 2nd Ed. (Ørberg, 2026-06) |
| `fabulae_syrae` | 27 | 37,544 | Cap. 26-34 (exact mapping) | segment | 1st Ed. (Miraglia) |
| `fabellae_latinae` | 22 | 9,170 | Cap. 1-25 (range notation, lower bound stored) | segment | 1st Ed. |
| `sermones_romani` | 11 | 26,550 | Post-Cap. 35 (all NULL) | segment | 1st Ed. (Ørberg) |
| `aeneis` | 4 | 1,443 | Post-Cap. 35 | segment | 2nd Ed. (Ørberg) |
| `de_bello_gallico` | 3 | 35,322 | Post-Cap. 35 | segment | 2nd Ed. (Ørberg) |
| `amphitryo` | 56 | 19,456 | Post-Cap. 35 | segment | 2nd Ed. (Ørberg) |
| `cena_trimalchionis` | 1 | 23,143 | Cap. 45-47 | whole | 2nd Ed. (Ørberg) |
| `ars_amatoria` | 3 | 19,844 | Post-Cap. 35 | segment | 2nd Ed. (Ørberg) |
| `catilina` | 1 | 23,955 | Cap. 56 | whole | 2nd Ed. (Ørberg) |
| `epitome_historiae_sacrae` | 1 | 48,673 | Post-Cap. 35 | whole | 2nd Ed. (Lhomond) |
| `de_rerum_natura` | 1 | 36,531 | Cap. 45 | whole | (Lucretius) |
| `roma_aeterna` | 21 | 110,311 | Cap. 36-56 (FR后接RA) | segment | HD 2nd color |

**Matching verified on priority chapters 1, 2, 5, 8, 15, 25, 33** with default weights (w1=0.4, w2=0.4, w3=0.2, w4=0.2).

**Whole-segment mode** (`segment_whole: true`): 4 books (Cena / Catilina / DRN / Epitome) have no consistent chapter markers in their source PDFs, so the entire cleaned full-text is ingested as a single segment. Future enhancement: split these on topic anchors (De Rerum Natura has SECTION markers; Catilina has [De ...] brackets).

---

## Key Design Decisions

1. **Surface forms, not lemmas** — avoid Latin NLP dependencies. `quī` and `quae` count as different words. This is acceptable because Ørberg's vocabulary IS surface-form-controlled (he repeats exact forms).

2. **Segments, not chapters** — Colloquia dialogues, Fabulae stories, Cena scenes are all natural matching units. Don't force one segmentation scheme across all books.

3. **Reverse index on `vocab`** — the M2M shape is the secret sauce. Querying "which segments contain `quī`?" is O(log n) thanks to `idx_vocab_word`.

4. **AI as fallback, not primary** — when no segment hits the new-words threshold, log it as a "gap" and consider AI generation (existing `ampliata_generate.py`) only for that gap.

5. **SQLite, not Postgres** — the dataset is small (<100k segments), single-writer, no network needs. SQLite is the right size.

---

## Quick-Start (MVP)

To run the full pipeline on one book (Colloquia Personarum 2nd Ed.):

```bash
# 1. OCR (skip if file is _text_selectable variant)
python3 scripts/ocr_book.py --pdf source/LLPSI_reader_colloquia_personarum.pdf --slug colloquia_personarum

# 2. Segment
python3 scripts/segment_book.py --slug colloquia_personarum

# 3. Ingest
python3 scripts/ingest_to_db.py --slug colloquia_personarum

# 4. Match for priority chapters
python3 scripts/match_segments.py --chapter 8 9 10 11 12 13 25 --top-n 5
```

---

## Known Issues & Workarounds

1. **Sermones Romani Sermo 11 (IVDICIVM) is oversized (22,916 words)** — The segmentation rule did not detect the transition to "MENAECHMI" and "Ex Plauti comoedia prologus et scaena ultima" appendix, so all post-Sermo-11 content (including maps) is absorbed into Sermo 11. **Impact**: This segment dominates the matching score for ALL chapters because `new_hits_normalized` saturates. **Workaround**: Either fix the segmentation rule to split on "MENAECHMI" / "Ex Plauti" markers, or filter by `fr_chapter IS NULL AND word_count > 5000` in the matching function.

2. **Fabellae Latinae fr_chapter is always 1** — The `parse_cap_range` function captures only the LOWER bound of the chapter range annotation (e.g., `cap. I-XIV` → 1). Fabulae that introduce vocabulary for chapters 5+ are still labeled as `fr_chapter=1`, making them look like Cap. 1 content. **Workaround**: Store the chapter range as a `fr_chapter_range` field (future enhancement); for now, accept the lower-bound approximation.

3. **OCR noise in Roman numerals** — Tesseract often misreads `I` as `l` or `|`. The `parse_ordinal` function in `segment_book.py` already handles this via `replace('l', 'I').replace('|', 'I')`. **Caveat**: A small number of titles may still slip through (e.g., `IIl` for `III`), leading to one missing segment in some books.

4. **Colloquia Personarum: each chapter is split into 2 parts** — The 2nd Ed. has 24 colloquiums, each split into ~2 scene-parts. This means the colloquium-level `arabic` repeats (e.g., `arabic=3` appears twice for Colloquium 3 parts 1 and 2). The `sequence` field remains unique (1-45).

---

## Extending With New Books

1. Drop the PDF into `source/`
2. Add a segmentation rule to `assets/segmentation_rules.yaml`
3. Run the 4 scripts above
4. Re-run the matching function — the new book is now in the candidate pool

No code changes needed. The schema, segmenter, and matcher are book-agnostic.

---

## What This Skill Does NOT Do

- Does not generate Latin text (use `ampliata_generate.py` for that)
- Does not modify the original `Familia Romana` text
- Does not lemmatize or run any Latin NLP
- Does not provide translations or annotations
- Does not train any model

This skill is **content selection**, not content creation.

---

## Version History

- **v1.6.0** (2026-06-06):
  - **HD text extraction as authoritative baseline**: New `extract_hd_text.py` uses pypdf to re-extract FR + RA HD 2nd color editions, replacing noisy OCR. Includes octal-escape decoder for partial-PDF edge cases.
  - **Bug fix — RA cumulative inflation (~20%)**: Old `merge_analysis.py` didn't subtract FR+RA word-form overlap. New `--precise` mode recomputes RA new-words and cumulative vocab against a true FR vocabulary baseline. See `analysis_output/ra_precision_comparison.md`.
  - **Algorithm enhancement — high-freq new word weighting (w4 + 2x)**: `match_segments.py` now splits new-words into low-freq (×1) and high-freq (×2) buckets. Default weight w4=0.2 added. Distinguishes "core new vocabulary" from "background noise".
  - **SQLite ingest (`--ingest-all` flag)**: Single command populates the database for all BOOKS_META entries. Idempotent. Re-ingest overwrites segments/vocab.
  - **Whole-segment mode (`segment_whole: true`)**: 4 books (De Rerum Natura, Cena Trimalchionis, Catilina, Epitome Historiae Sacrae) lack standard chapter markers — the entire cleaned text becomes a single segment. Enables Phase 2 ingestion for these books.
  - **Bug fixes**:
    - `segment_book.py`: skip_pages now correctly skips the entire PAGE block (not just the marker).
    - `segment_book.py`: title_template is now {n}/{t}-safe via try-except.
    - `init_fr_vocab`: lowercases all tokens + filters non-alphabetic noise (was causing size mismatch with `vocab` table).
    - `merge_analysis.py`: --precise parameter is now wired into main().
    - `generate_combined_viz.py`: RA starting-chapter new-words are no longer hard-coded; read from `ra_data`.
  - **Full Phase 2 ingest**: 13 books / 197 segments / 408k words. RA (Roma Aeterna) is the largest at 110k words / 21 segments.
  - **Visualization renamed**: `viz_output/` removed, `analysis_output/LLPSI_Insights.html` is now the single source of truth. `familia_romana_insights.html` and `llpsi_fr_ra_insights.html` deleted.

- **v1.2.0** (2026-06-06):
  - **Added Roma Aeterna (Pars II) to the analysis pipeline**: OCR'd HD 2nd color edition, segmented 21 chapters (Cap. XXXVI-LVI), computed word-frequency statistics.
  - **New scripts**: `analyze_book.py` (book-agnostic word-freq analyzer), `merge_analysis.py` (FR+RA merger), `generate_combined_viz.py` (combined HTML visualization), `cleanup_source.py` (duplicate detection & reorg).
  - **New analysis outputs**: `roma_aeterna_chapter_stats.csv`, `roma_aeterna_analysis_report.md`, `combined_stats.csv`, `combined_long.csv`, `combined_priority_report.md`.
  - **New visualization**: `viz_output/llpsi_fr_ra_insights.html` (FR+RA combined difficulty curve with 5 charts: cumulative vocab, density, tokens, new words, FR/RA radar comparison).
  - **Reorganized project layout**:
    - All `ocr_output/per_page*` and `familia_romana_*.txt` consolidated under `ocr_output/familia_romana/`
    - `_full.txt` (RA) and `page_*.txt` outputs preserved in their own slug subdirectory
    - PRD + Technical_Architecture documents moved from `.trae/documents/` → `docs/`
    - Debug PNGs from `viz_output/` moved to `viz_output/_archive/`
    - macOS `.DS_Store` files removed; `__pycache__` cleaned
  - **Expanded source inventory**: 11 new readers + 3 vocabulary lists + 2 companion guides + 1 new exercise book documented (see "Complete Source Inventory" above).
  - **Updated path references** in `iterum_analysis.py`, `analyze_book.py`, `ampliata_generate.py`, `ocr_familia_romana.py`, `ocr_postprocess.py`, `Project_Plan.md`.
  - **Updated database state note** in `iterum_analysis.py` for RA chapters 36-56 (LATIN_ORDINALS extended).

- **v1.1.0** (2026-06-06):
  - Renamed 35 source PDFs to `LLPSI_<category>_<title>.<ext>` convention (added `rename_source.py`).
  - OCR'd 4 high-priority readers: Colloquia Personarum 2nd Ed. (Ørberg), Fabulae Syrae, Fabellae Latinae, Sermones Romani.
  - Ingested 4 books into SQLite (105 segments, ~91k words, 17.6k unique word forms).
  - Refactored `ingest_to_db.py` to prefer `segments.json`'s `fr_chapter` over heuristic derivation.
  - Verified matching on priority chapters 8, 9, 10, 11, 12, 13, 25.
  - Documented known issues (Sermones Sermo 11 oversize, Fabellae fr_chapter lower-bound limitation).

- **v1.0.0** (2026-06-05): Initial design. Authoritative-content-first pipeline with SQLite reverse index.
