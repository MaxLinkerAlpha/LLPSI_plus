"Check Cap3 OCR issues"
import json

with open("word_chapter_map.json") as f:
    wc = json.load(f)

cap3 = [k for k, v in wc.items() if (isinstance(v, int) and v == 3) or (isinstance(v, list) and 3 in v)]
print(f"Cap3 entries: {len(cap3)}")

# OCR artifacts
pipes = [k for k in cap3 if '|' in k]
digits = [k for k in cap3 if any(c.isdigit() for c in k)]
v_words = [k for k in cap3 if 'v' in k]
special = [k for k in cap3 if any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\xE0\xE1\xE8\xE9\xEC\xED\xF2\xF3\xF9\xFA' for c in k)]
long_stuck = [k for k in cap3 if len(k) > 15]
short = [k for k in cap3 if len(k) <= 2]

print(f"\nPipes '|': {len(pipes)}")
for k in pipes:
    print(f"  {k!r}")

print(f"\nDigits: {len(digits)}")
for k in digits:
    print(f"  {k!r}")

print(f"\nV-instead-of-U: {len(v_words)}")
# Show only obvious OCR V→U issues (lowercase v)
obvious_v = [k for k in v_words if 'v' in k and not k.isupper()]
print(f"  lowercase v: {len(obvious_v)}")
for k in sorted(obvious_v)[:30]:
    print(f"    {k!r}")

print(f"\nLong stuck (>15): {len(long_stuck)}")
for k in long_stuck:
    print(f"  {k!r}")

print(f"\nVery short (<=2): {len(short)}")
for k in short:
    print(f"  {k!r}")

print(f"\nNon-latin chars: {len(special)}")
for k in special[:20]:
    print(f"  {k!r}")

# Also check the actual OCR source dir
print(f"\n\nOverall quality: cap3 has {len(cap3)} entries")
print(f"  Clean: {len(cap3) - len(pipes) - len(digits) - len(special) - len(short) - len(long_stuck)}")
print(f"  Problematic: {len(set(pipes+digits+special+short+long_stuck))}")
