#!/usr/bin/env python3
"""Fix corrupted words from the over-aggressive ōra→manūs replacement.
Also fix any other issues from the lemmatization fixes."""
import re

with open('rewrite_cap7_8.py', encoding='utf-8') as f:
    content = f.read()

# Fix corrupted words from ōra→manūs substring matching
fixes = [
    # labōrat → labmanūst (from "ōra" matching inside "labōrat")
    ("labmanūst", "labōrat"),
    ("labmanūsnt", "labōrant"),
    ("plmanūsnt", "plōrant"),
    # Check for other corrupted words
    ("in vīllā sumt", "habitat"),  # if habitō→in vīllā sum broke habitat
]

for old, new in fixes:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f"Fixed: '{old}' -> '{new}' ({count} occurrences)")

# Also check: did ōrae→manūs break anything? ōrae would become manūs which is grammatically wrong
# "ōrae" → "manūs" (genitive singular "of the mouth" → "hands" - wrong)
# Fix: "manūs" as genitive → "manūs" is already correct for plural "hands"

# Check for "manūs" appearing in context where it should be "ōrae"
# "ōrae" → "manūs" would be wrong in genitive context
# But this is hard to detect automatically. Let me just check manually.

with open('rewrite_cap7_8.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nCorruption fixes applied.")
print("Now re-running evaluation...")