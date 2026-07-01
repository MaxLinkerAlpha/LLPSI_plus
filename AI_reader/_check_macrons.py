"""检查所有故事文件是否有长音"""
import os, re

total = 0
no_macron = []
cap_counts = {}
threshold = 3  # 少于 3 个长音字符 = 基本没有长音

root = os.path.dirname(os.path.abspath(__file__))
realitates = os.path.join(root, "realitates")
dirs = sorted(d for d in os.listdir(realitates) if d.startswith("Cap"))

for cap in dirs:
    cap_path = os.path.join(realitates, cap)
    if not os.path.isdir(cap_path):
        continue
    files = sorted(f for f in os.listdir(cap_path) if f.endswith(".md"))
    cap_counts[cap] = len(files)
    for fname in files:
        total += 1
        fpath = os.path.join(cap_path, fname)
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        # 只检查正文（front matter 之后）
        parts = content.split("---", 2)
        body = parts[2] if len(parts) >= 3 else (parts[0] if parts else "")
        macrons = re.findall(r"[āēīōūȳĀĒĪŌŪȲ]", body)
        if len(macrons) < threshold:
            no_macron.append((cap, fname, len(macrons)))

print(f"总文件: {total}")
print(f"缺少长音 (< {threshold}): {len(no_macron)}")
print()

if no_macron:
    by_cap = {}
    for cap, fname, cnt in no_macron:
        by_cap.setdefault(cap, []).append((fname, cnt))
    for cap in sorted(by_cap):
        files = by_cap[cap]
        print(f"{cap}: {len(files)} 个/共 {cap_counts.get(cap, 0)} 个")
        for fname, cnt in files:
            print(f"    {fname} (长音: {cnt})")
else:
    print("所有故事文件都有长音。")
