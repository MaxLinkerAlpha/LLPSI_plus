#!/usr/bin/env python3
"""检查可清洗条目中，清洗后是否已在词表中"""
import json, re

with open("form_chapter_map.json") as f:
    data = json.load(f)

stats = {"hyphen_already": 0, "hyphen_new": 0,
         "pipe_already": 0, "pipe_new": 0,
         "slash_already": 0, "slash_new": 0,
         "ellipsis": 0}

for k, v in data.items():
    if "-" in k:
        clean = k.replace("-", "").lower()
        if clean in data:
            stats["hyphen_already"] += 1
        else:
            stats["hyphen_new"] += 1
            if stats["hyphen_new"] <= 3:
                print(f"  连字符 新增: {k} -> {clean} (Cap{v})")
    if "|" in k:
        clean = k.replace("|", "").lower()
        if clean in data:
            stats["pipe_already"] += 1
        else:
            stats["pipe_new"] += 1
            if stats["pipe_new"] <= 3:
                print(f"  管道 新增: {k} -> {clean} (Cap{v})")
    if "/" in k and k.count("/") == 1:
        for p in k.split("/"):
            p = p.strip().lower()
            if p and len(p) >= 2:
                if p in data:
                    stats["slash_already"] += 1
                else:
                    stats["slash_new"] += 1
                    if stats["slash_new"] <= 3:
                        print(f"  斜杠 新增: {p} (源={k}, Cap{v})")
    if "..." in k:
        stats["ellipsis"] += 1

print()
print("=" * 50)
print(f"连字符: 已有={stats['hyphen_already']}, 可新增={stats['hyphen_new']}")
print(f"管道:   已有={stats['pipe_already']},   可新增={stats['pipe_new']}")
print(f"斜杠:   已有={stats['slash_already']},   可新增={stats['slash_new']}")
print(f"省略号: {stats['ellipsis']} 条 (语法模式)")
print(f"真正能新增的独立词条: {stats['hyphen_new'] + stats['pipe_new'] + stats['slash_new']}")
