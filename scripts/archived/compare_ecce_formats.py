#!/usr/bin/env python3
"""Compare Ecce Romani I PDF and EPUB content quality."""
import os
import sys
import zipfile
import re
from pathlib import Path

EPUB_DIR = Path("source/Other_Readers/拉英-快看罗马人EcceRomani")
epub_path = EPUB_DIR / "Ecce Romani I&II Combined A Latin Reading Program (Scottish Classics Group).epub"
pdf_path = EPUB_DIR / "Ecce Romani I .pdf"

print(f"=== EPUB Inspection ===")
print(f"File: {epub_path.name}")
print(f"Size: {epub_path.stat().st_size:,} bytes")

with zipfile.ZipFile(epub_path, 'r') as z:
    names = z.namelist()
    print(f"Total entries: {len(names)}")

    text_files = [n for n in names if n.endswith(('.xhtml', '.html', '.htm', '.xml', '.ncx', '.opf'))]
    image_files = [n for n in names if re.search(r'\.(jpe?g|png|gif|svg|webp)$', n, re.IGNORECASE)]
    other_files = [n for n in names if n not in text_files and n not in image_files]

    print(f"  Text content: {len(text_files)}")
    print(f"  Images: {len(image_files)}")
    print(f"  Other (style/font/metadata): {len(other_files)}")

    # Total text size vs image size
    total_text = sum(z.getinfo(n).file_size for n in text_files)
    total_image = sum(z.getinfo(n).file_size for n in image_files)
    print(f"  Total text bytes: {total_text:,}")
    print(f"  Total image bytes: {total_image:,}")
    print(f"  Text:Image ratio: {total_text/max(total_image,1):.2f}:1")

    print()
    print("First 15 files:")
    for n in names[:15]:
        info = z.getinfo(n)
        kind = "TEXT" if n in text_files else ("IMG" if n in image_files else "META")
        print(f"  [{kind:4s}] {n}  ({info.file_size:,} bytes)")

    # Try to extract Latin text from first chapter
    print()
    print("=== First 3 text file contents (excerpt) ===")
    for n in text_files[:3]:
        info = z.getinfo(n)
        if info.file_size < 100:
            continue
        try:
            with z.open(n) as f:
                content = f.read().decode('utf-8', errors='replace')
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f"\n--- {n} ({info.file_size:,} bytes) ---")
            print(text[:500])
        except Exception as e:
            print(f"\n--- {n} (error: {e}) ---")

# Compare with existing PDF OCR
print()
print("=== Existing PDF OCR for ecce_romani ===")
ocr_dir = Path("ocr_output/ecce_romani")
if ocr_dir.exists():
    full = ocr_dir / "_full.txt"
    if full.exists():
        text = full.read_text(encoding='utf-8', errors='replace')
        # Word count
        words = text.split()
        latin_words = sum(1 for w in words if re.match(r'^[a-zA-Z]+$', w))
        print(f"  _full.txt size: {full.stat().st_size:,} bytes")
        print(f"  Word count (any): {len(words):,}")
        print(f"  Latin-like words: {latin_words:,}")
        print()
        print("First 1000 chars:")
        print(text[:1000])
