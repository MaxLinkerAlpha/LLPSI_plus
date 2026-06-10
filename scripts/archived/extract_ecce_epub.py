#!/usr/bin/env python3
"""Extract Latin text from Ecce Romani EPUB and compare quality."""
import zipfile
import re
import json
from pathlib import Path
from html import unescape

EPUB = Path("source/Other_Readers/拉英-快看罗马人EcceRomani/Ecce Romani I&II Combined A Latin Reading Program (Scottish Classics Group).epub")

def html_to_text(html: str) -> str:
    # Remove style/script
    html = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Replace block elements with newlines
    html = re.sub(r'</(p|div|h[1-6]|li|tr|br)>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<br[^>]*>', '\n', html, flags=re.IGNORECASE)
    # Strip remaining tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Decode entities
    text = unescape(text)
    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()

print(f"=== Extracting {EPUB.name} ===")
with zipfile.ZipFile(EPUB, 'r') as z:
    # Find all part*.html and any sizable text files
    text_files = [n for n in z.namelist() if n.endswith('.html') and not n.endswith('toc.ncx')]
    text_files.sort()

    all_text = []
    for n in text_files:
        info = z.getinfo(n)
        if info.file_size < 1000:
            continue  # skip leaf*.html placeholders
        with z.open(n) as f:
            content = f.read().decode('utf-8', errors='replace')
        text = html_to_text(content)
        if len(text) > 100:
            all_text.append((n, text))
            print(f"\n--- {n} ({info.file_size:,} bytes) ---")
            print(text[:300])

    print()
    print(f"=== Summary: {len(all_text)} substantial text files ===")
    total_chars = sum(len(t) for _, t in all_text)
    print(f"Total extracted text: {total_chars:,} chars")

    # Word analysis
    full_text = "\n".join(t for _, t in all_text)
    words = re.findall(r"[A-Za-z']+", full_text)
    print(f"Total words: {len(words):,}")
    unique_words = set(w.lower() for w in words)
    print(f"Unique words: {len(unique_words):,}")

    # Latin vs English ratio (very rough)
    common_english = {"the", "is", "and", "a", "to", "of", "in", "that", "it", "with", "as", "for", "was", "are", "be", "this", "have", "from", "or", "by", "an", "they", "which", "their", "but", "not", "has", "his", "her", "she", "he", "we", "you", "i", "do", "can", "will", "would", "could", "should", "may", "might", "look", "see", "make", "made", "go", "going", "come", "came", "take", "took", "give", "gave", "two", "girls", "look", "says", "said"}
    english_hits = sum(1 for w in words if w.lower() in common_english)

    # Latin feature suffixes
    latin_suffix = re.compile(r'\b\w*(que|tur|ntur|mus|ris|re|ri|nt|net|tis|te)\b', re.IGNORECASE)
    latin_hits = sum(1 for w in words if latin_suffix.search(w))

    print(f"  Common English hits: {english_hits}")
    print(f"  Latin-suffix hits: {latin_hits}")

    # Save extracted text
    out = Path("analysis_output/ecce_romani_combined_epub.txt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(full_text, encoding='utf-8')
    print(f"\nSaved: {out} ({out.stat().st_size:,} bytes)")
