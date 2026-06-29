#!/usr/bin/env python3
"""检查 realitates 中是否有重复生成的故事（标题+内容都相同）。"""

import json
from pathlib import Path
from collections import defaultdict

realitates = Path(__file__).resolve().parent / "realitates"

# 按 (章节, 标题) 分组
title_files = defaultdict(list)
for f in sorted(realitates.rglob("*.md")):
    lines = f.read_text(encoding="utf-8").split("\n")
    for l in lines:
        if l.startswith("title_la:"):
            title = l.split(":", 1)[1].strip().strip('"')
            title_files[(f.parent.name, title)].append(f)
            break

total_duplicates = 0
for (cap, title), files in sorted(title_files.items()):
    if len(files) < 2:
        continue

    # 提取正文（YAML后的内容）
    contents = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        body = parts[2].strip() if len(parts) > 2 else parts[-1].strip()
        contents[f.name] = body

    bodies = list(contents.values())
    all_same = all(b == bodies[0] for b in bodies)

    fnames = ", ".join(contents.keys())
    if all_same:
        print(f"[完全重复] {cap}/{title}: {fnames}")
        total_duplicates += len(files) - 1
    else:
        print(f"[标题相同但内容不同] {cap}/{title}: {fnames}")

if total_duplicates == 0:
    print("\n没有完全重复的文件（标题相同且内容相同）→ 0 可删除")
else:
    print(f"\n共 {total_duplicates} 篇可删除的完全重复文件")