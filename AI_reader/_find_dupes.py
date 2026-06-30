#!/usr/bin/env python3
"""查重：找出 realitates 目录下大小完全相同的文件，检查尾部内容确认重复"""
import os, hashlib
from collections import defaultdict

REALITATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'realitates')

# Step 1: 按文件大小分组
size_map = defaultdict(list)
for root, dirs, files in os.walk(REALITATES):
    for fname in files:
        if fname.endswith('.md'):
            fpath = os.path.join(root, fname)
            size = os.path.getsize(fpath)
            size_map[size].append(fpath)

# Step 2: 找出有多个文件的大小组
duplicates_found = []
for size, paths in size_map.items():
    if len(paths) > 1:
        # 检查尾部内容是否相同（读最后500字节）
        tails = {}
        for p in paths:
            with open(p, encoding='utf-8', errors='replace') as f:
                f.seek(max(0, size - 500))
                tail = f.read()
            tail_hash = hashlib.md5(tail.encode()).hexdigest()
            tails[p] = tail_hash
        
        # 按 tail_hash 分组
        hash_groups = defaultdict(list)
        for p, h in tails.items():
            hash_groups[h].append(p)
        
        for h, group in hash_groups.items():
            if len(group) > 1:
                for p in group:
                    duplicates_found.append(p)

if duplicates_found:
    print(f'发现 {len(duplicates_found)} 个重复文件（尾部内容相同）：')
    for p in duplicates_found:
        size = os.path.getsize(p)
        print(f'  {p}  ({size} bytes)')
else:
    print('未发现重复文件')

print(f'\n总文件数: {sum(len(v) for v in size_map.values())}')
print(f'不同大小组数: {len(size_map)}')
