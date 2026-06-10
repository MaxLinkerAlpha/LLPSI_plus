---
name: "llpsi-ingest-pipeline"
description: "Ingests a new Latin reader into the LLPSI corpus, segments it, updates the database, and regenerates insertion recommendations. Invoke when the user provides a new book (PDF/text) to add to the LLPSI reading recommendation system."
---

# LLPSI Ingest Pipeline

## When to Invoke

Invoke this skill when the user:
- Provides a new Latin reader PDF or text file to add to the corpus
- Wants to see where a new book fits in the FR/RA reading sequence
- Asks "add this book to the database" or "process this reader"
- Wants to regenerate the insertion guide after adding new books

## Pipeline Overview

```
                     ┌─→ has chapter markers? ─→ add rule to segmentation_rules.yaml
                     │
New Book (PDF/text) ─┤
                     │
                     └─→ no chapter markers? ─→ use segment_whole: true in rules
                              │
                              ▼
                     segment_book.py --slug <name>
                              │
                              ▼
                     ingest_to_db.py --slug <name>
                              │
                              ▼
                     (If LLPSI-official: update fr_chapter in DB)
                              │
                              ▼
                     generate_insertion_guide.py  (regenerates reader_insertion_guide.md)
```

## Step-by-Step

### Step 0: Prepare the Text

- If the book is a **PDF**: Use `scripts/extract_hd_text.py` to extract text, or OCR if the PDF is not text-selectable.
- Save the full text as `ocr_output/<slug>/_full.txt`.
- If the book has page-level text, save each page as `ocr_output/<slug>/page_NNN.txt`.

### Step 1: Add Segmentation Rules

Edit `assets/segmentation_rules.yaml` and add a new entry under `books:`:

```yaml
<slug>:
  segment_pattern: '^CHAPTER\s+([IVXLC]+)'   # regex matching chapter headers
  title_template: 'Chapter {n}'               # naming pattern: {n}=number, {t}=title
  skip_pages: 3                               # pages to skip (front matter)
```

**Rules of thumb**:
- For books **without** standard chapter markers (e.g., epic poems, orations): add `segment_whole: true` — the entire text becomes one segment.
- For books with Roman numeral chapters: use `LIBER X`, `ACTVS X`, `CAPVT X` patterns.
- For books with Arabic number + title: use `(\d+)\.\s+(.+)` (2 capture groups).
- For books with cap range annotations: use `(\d+)\.\s+(.+?)\s+\(cap\.\s+([IVXLC\-]+)\)` (3 capture groups).

**Important**: YAML strings containing backslash `\` should use single quotes (not double quotes) to avoid escape issues.

### Step 2: Segment the Book

```bash
python3 scripts/segment_book.py --slug <slug>
```

This reads `ocr_output/<slug>/_full.txt` and outputs `ocr_output/<slug>/segments.json`.

**Verify**: Check terminal output for segment count, total words, and any missing sequence warnings.

### Step 3: Ingest to Database

```bash
python3 scripts/ingest_to_db.py --slug <slug>
```

This writes books, segments, and vocab tables to `data/llpsi_corpus.db`.

**Verify**: 
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('data/llpsi_corpus.db')
cur = conn.cursor()
cur.execute('SELECT b.slug, COUNT(s.id) FROM books b JOIN segments s ON s.book_id=b.id WHERE b.slug=\"<slug>\"')
print(f'段数: {cur.fetchone()[1]}')
"
```

### Step 4: Mark fr_chapter (LLPSI-official readers only)

If the new book is a LLPSI ecosystem reader with **explicit chapter correspondence** (e.g., "AD CAPITVLVM XXVI"), update the `fr_chapter` column in the segments table. This can be done by:

- **If segment_book.py already parsed it**: The `fr_chapter` field in `segments.json` is automatically read by `ingest_to_db.py`. Only if that failed, manually update.

- **Manual update via SQL**:
```sql
UPDATE segments SET fr_chapter = <N> WHERE book_id = (SELECT id FROM books WHERE slug='<slug>') AND sequence = <seq>;
```

**fr_chapter semantics**: "The FR/RA chapter AFTER which this segment can be read." For Colloquia Personarum, Colloquium N = fr_chapter N.

### Step 5: Regenerate Everything

```bash
# Regenerate insertion guide (this is the only mandatory step):
python3 scripts/generate_insertion_guide.py

# Optional: regenerate coverage analysis:
python3 scripts/vocab_overlap.py --precise

# Optional: regenerate the HTML visualization:
python3 scripts/generate_combined_viz.py
```

### Step 6: Review Results

Open `analysis_output/reader_insertion_guide.md` and check:
- **Part 1 (Exact Mapping)**: If fr_chapter was set, the new book should appear here.
- **Part 2 (Algorithmic Matching)**: If no fr_chapter, the new book appears with algorithm-calculated recommendations per chapter.
- **Part 3 (Coverage Gaps)**: Check if the new book filled any gaps.

## Key Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/extract_hd_text.py` | Extract text from text-selectable PDFs |
| `scripts/segment_book.py --slug <name>` | Split full text into segments |
| `scripts/ingest_to_db.py --slug <name>` | Write segments to SQLite |
| `scripts/generate_insertion_guide.py` | Regenerate insertion recommendations |
| `scripts/vocab_overlap.py --precise` | Per-chapter vocabulary overlap analysis |
| `scripts/match_segments.py --chapter N --use-fr-chapter` | Find best matching segments for a chapter |

## Database Schema (for reference)

```sql
-- Books: one row per reader
CREATE TABLE books (id, slug, title, author, fr_range, segment_kind);

-- Segments: one row per chapter/section
CREATE TABLE segments (id, book_id, sequence, title, latin, word_count, fr_chapter);

-- Vocab: word frequency per segment
CREATE TABLE vocab (segment_id, word_form, freq);

-- FR Vocab: Familia Romana + Roma Aeterna chapter vocabulary
CREATE TABLE fr_vocab (chapter, word_form, is_new);
```

## Important Notes

- **fr_chapter = NULL is normal** for most non-LLPSI readers (e.g., Aeneis, De Bello Gallico). They are matched algorithmically.
- **Always regenerate `reader_insertion_guide.md`** after adding any book — it reads the DB fresh each time.
- **The pipeline is idempotent**: running ingest multiple times overwrites existing data for the same slug.
- **For books without chapter markers**: `segment_whole: true` + `ingest_to_db` → 1 segment in DB → Part 2 matching.
- **Colloquia Personarum** and **Fabulae Syrae** are the gold standard for fr_chapter correspondence.
