#!/usr/bin/env python3
"""
修复脚本 v1_0_0
功能：
  1. 移动放错文件夹的故事到正确的 best_fit_chapter 目录
  2. 删除重复故事（保留序列号最小的那篇）
用法：
  python3 _fix_audit.py           # dry-run 预览
  python3 _fix_audit.py --execute  # 实际执行
"""

import os
import re
import sys
import json
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).parent / "realitates"
DRY_RUN = '--execute' not in sys.argv


def extract_yaml_and_body(filepath: Path):
    """提取 YAML 元数据 + 拉丁正文归一化"""
    text = filepath.read_text(encoding='utf-8', errors='replace')
    text = text.lstrip('\ufeff')
    
    yaml_dict = {}
    body_raw = ''
    
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            body_raw = text[len(parts[0]) + len(parts[1]) + 6:].strip()
    else:
        body_raw = text.strip()
    
    # 解析 YAML 关键字段
    for field in ['story_id', 'title_la', 'best_fit_chapter', 'evaluated_chapter',
                   'target_chapter', 'length_tier']:
        match = re.search(rf'^{field}:\s*(.+?)$', text, re.MULTILINE)
        if match:
            val = match.group(1).strip().strip('"').strip("'")
            try:
                val = int(val) if '.' not in val else float(val)
            except (ValueError, TypeError):
                pass
            yaml_dict[field] = val
    
    # 归一化正文做去重比较
    body_norm = re.sub(r'[āēīōūȳǣ]', '', body_raw.lower()) if body_raw else ''
    body_norm = re.sub(r'[^a-z\s]', ' ', body_norm)
    words = sorted(w for w in body_norm.split() if len(w) > 1)
    
    return yaml_dict, body_raw, ' '.join(words)


def hash_body(body: str) -> str:
    return hashlib.sha256(body.encode('utf-8')).hexdigest()[:16]


def collect_all_files():
    """收集所有 .md 文件，返回 {filepath: cap_folder}"""
    all_files = {}
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        cap_num = int(re.search(r'\d+', cap_dir.name).group())
        for md_file in sorted(cap_dir.glob('*.md')):
            all_files[md_file] = cap_num
    return all_files


def main():
    mode = "DRY-RUN (预览模式)" if DRY_RUN else "EXECUTE (执行模式)"
    print("=" * 60)
    print(f"  故事修复脚本 — {mode}")
    print("=" * 60)
    
    all_files = collect_all_files()
    print(f"\n[扫描] 共 {len(all_files)} 个文件\n")
    
    # ============================================================
    # 第一步：移动放错位置的故事
    # ============================================================
    print("=" * 40)
    print("  一、移动放错章节的故事")
    print("=" * 40)
    
    moves = []  # (src_path, src_cap, dst_cap, title)
    
    for fpath, cap_folder in all_files.items():
        try:
            yaml, body, norm = extract_yaml_and_body(fpath)
        except:
            continue
        
        best_cap = yaml.get('best_fit_chapter') or yaml.get('evaluated_chapter')
        if best_cap is None:
            continue
        
        diff = abs(cap_folder - best_cap)
        if diff > 2 and cap_folder != best_cap:
            moves.append((fpath, cap_folder, best_cap, yaml.get('title_la', '?')))
    
    if moves:
        print(f"\n  共 {len(moves)} 篇需要移动：\n")
        for fpath, src_cap, dst_cap, title in sorted(moves, key=lambda x: abs(x[1] - x[2]), reverse=True):
            print(f"    [Cap{src_cap} → Cap{dst_cap}] {fpath.name}  《{title}》")
        
        if not DRY_RUN:
            print(f"\n  [执行] 开始移动...")
            moved_count = 0
            for fpath, src_cap, dst_cap, title in moves:
                dst_dir = REALITATES_DIR / f"Cap{dst_cap}"
                dst_dir.mkdir(parents=True, exist_ok=True)
                dst_path = dst_dir / fpath.name
                
                # 如果目标已存在同名文件，添加后缀
                if dst_path.exists():
                    stem = fpath.stem
                    suffix = fpath.suffix
                    counter = 1
                    while dst_path.exists():
                        dst_path = dst_dir / f"{stem}_moved{counter}{suffix}"
                        counter += 1
                
                shutil.move(str(fpath), str(dst_path))
                moved_count += 1
                print(f"    [OK] {fpath.name} → Cap{dst_cap}/")
            print(f"\n  [完成] 移动了 {moved_count} 篇故事")
    else:
        print("\n  [OK] 无需移动。")
    
    # ============================================================
    # 第二步：删除重复故事
    # ============================================================
    print("\n" + "=" * 40)
    print("  二、删除重复故事")
    print("=" * 40)
    
    # 重新收集文件（移动后可能位置变了）
    all_files = collect_all_files()
    
    # 按正文 hash 分组
    hash_groups = defaultdict(list)
    for fpath, cap in all_files.items():
        try:
            yaml, body, norm = extract_yaml_and_body(fpath)
            h = hash_body(norm)
            hash_groups[h].append((fpath, yaml, cap))
        except:
            continue
    
    # 找重复组
    to_delete = []  # (filepath, reason)
    
    for h, files in hash_groups.items():
        if len(files) <= 1:
            continue
        
        # 保留序列号最小的，删其余的
        # 序列号从文件名提取：CapN_Title_tier_NNN.md
        def extract_seq(fp):
            m = re.search(r'_(\d{3})\.md$', fp.name)
            if m:
                return int(m.group(1))
            m = re.search(r'_(\d+)\.md$', fp.name)
            if m:
                return int(m.group(1))
            return 9999
        
        sorted_files = sorted(files, key=lambda x: extract_seq(x[0]))
        keep = sorted_files[0]
        for fpath, yaml, cap in sorted_files[1:]:
            to_delete.append((fpath, f"与 {keep[0].name} 重复 (Cap{keep[2]})"))
    
    if to_delete:
        print(f"\n  共 {len(to_delete)} 篇重复需要删除：\n")
        # 汇总统计
        by_chapter = defaultdict(int)
        for fpath, reason in to_delete:
            cap = int(re.search(r'Cap(\d+)', str(fpath.parent)).group(1))
            by_chapter[cap] += 1
        
        for cap in sorted(by_chapter):
            print(f"    Cap{cap}: 删 {by_chapter[cap]} 篇")
        
        print(f"\n  详细列表（前 30 篇）：")
        for fpath, reason in to_delete[:30]:
            print(f"    [删] {fpath.name} — {reason}")
        if len(to_delete) > 30:
            print(f"    ... 还有 {len(to_delete) - 30} 篇")
        
        if not DRY_RUN:
            print(f"\n  [执行] 开始删除...")
            deleted = 0
            for fpath, reason in to_delete:
                try:
                    fpath.unlink()
                    deleted += 1
                except Exception as e:
                    print(f"    [失败] {fpath.name}: {e}")
            print(f"  [完成] 删除了 {deleted} 篇重复故事")
    else:
        print("\n  [OK] 无重复。")
    
    # ============================================================
    # 第三步：清理空目录
    # ============================================================
    if not DRY_RUN:
        print("\n" + "=" * 40)
        print("  三、清理空目录")
        print("=" * 40)
        for cap_dir in sorted(REALITATES_DIR.iterdir()):
            if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
                continue
            if not any(cap_dir.iterdir()):
                cap_dir.rmdir()
                print(f"    [清理] 空目录 {cap_dir.name}")
    
    # ============================================================
    # 第四步：重新统计
    # ============================================================
    print("\n" + "=" * 40)
    print("  四、修复后统计")
    print("=" * 40)
    
    all_files = collect_all_files()
    stats = defaultdict(lambda: {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0})
    
    for fpath, cap_folder in all_files.items():
        try:
            yaml, body, norm = extract_yaml_and_body(fpath)
        except:
            continue
        
        tier = yaml.get('length_tier', '?')
        if tier in ('短篇', 'brevis', 'B'):
            tier_key = 'brevis'
        elif tier in ('中篇', 'medius', 'M'):
            tier_key = 'medius'
        elif tier in ('长篇', 'longus', 'L'):
            tier_key = 'longus'
        else:
            tier_key = 'brevis'
        
        stats[cap_folder][tier_key] += 1
        stats[cap_folder]['total'] += 1
    
    print(f"\n  {'章':>4}  {'短篇B':>5}  {'中篇M':>5}  {'长篇L':>5}  {'总计':>5}  {'状态':>6}")
    print("  " + "-" * 48)
    
    total_all = {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0}
    
    for cap in sorted(stats.keys()):
        s = stats[cap]
        for k in total_all:
            total_all[k] += s[k]
        status = "OK" if s['total'] >= 10 else f"缺{10 - s['total']}"
        print(f"  Cap{cap:>2}  {s['brevis']:>5}  {s['medius']:>5}  {s['longus']:>5}  {s['total']:>5}  {status:>6}")
    
    print("  " + "-" * 48)
    print(f"  {'合计':>4}  {total_all['brevis']:>5}  {total_all['medius']:>5}  {total_all['longus']:>5}  {total_all['total']:>5}")
    
    gaps = [f"Cap{c}" for c in sorted(stats.keys()) if stats[c]['total'] < 10]
    if gaps:
        print(f"\n  [!!] 缺口章节: {', '.join(gaps)}")
        for c in sorted(stats.keys()):
            if stats[c]['total'] < 10:
                print(f"    Cap{c}: {stats[c]['total']} 篇 (缺{10 - stats[c]['total']})")
    else:
        print("\n  [OK] 所有章节均 ≥ 10 篇！")
    
    if DRY_RUN:
        print(f"\n  ⚠️  这是预览模式。确认无误后执行：python3 _fix_audit.py --execute")
    
    print("\n" + "=" * 60)
    print("  完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
