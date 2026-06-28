"""测试 simplemma 对拉丁语的准确率"""
import simplemma

tests = [
    # 名词变格
    ("puellam", "puella"), ("puellae", "puella"), ("puellarum", "puella"),
    ("servus", "servus"), ("servum", "servus"), ("servi", "servus"),
    ("regem", "rex"), ("regis", "rex"), ("regi", "rex"),
    ("civitati", "civitas"), ("civitatem", "civitas"),
    ("flumen", "flumen"), ("fluminis", "flumen"),
    # 动词变位
    ("est", "sum"), ("sunt", "sum"), ("erat", "sum"), ("erant", "sum"),
    ("amat", "amo"), ("amant", "amo"), ("amabat", "amo"),
    ("currit", "curro"), ("cucurrit", "curro"),
    ("audit", "audio"), ("audiunt", "audio"),
    ("capit", "capio"), ("cepit", "capio"),
    ("dixit", "dico"), ("dicunt", "dico"),
    ("videt", "video"), ("viderunt", "video"),
    ("fert", "fero"), ("tulit", "fero"),
    # 形容词
    ("magnus", "magnus"), ("magnam", "magnus"), ("magnum", "magnus"),
    ("omnis", "omnis"), ("omnem", "omnis"), ("omnia", "omnis"),
]

correct = 0
for word, expected in tests:
    lemma = simplemma.lemmatize(word, lang="la")
    ok = lemma == expected
    if ok:
        correct += 1
    mark = "OK" if ok else "X "
    print(f"  {mark}  {word:15s} → {lemma:12s}  (expected: {expected})")

print(f"\n准确率: {correct}/{len(tests)} = {correct/len(tests)*100:.1f}%")
