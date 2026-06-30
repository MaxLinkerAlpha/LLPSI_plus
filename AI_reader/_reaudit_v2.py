#!/usr/bin/env python3
"""
严格双重审计 v2_0_0
铁律：文件名前缀 CapN_ 必须与所在文件夹 CapN/ 一致。
     不一致时以 best_fit_chapter 为准决定目标文件夹。
用法：
  python3 _reaudit_v2.py           # dry-run
  python3 _reaudit_v2.py --execute  # 执行
"""

import os, re, sys, shutil
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).parent / "realitates"
DRY_RUN = '--execute' not in sys.argv


def read_meta(filepath: Path):
    """读取核心字段"""
    text = filepath.read_text(encoding='utf-8', errors='replace')
    text = text.lstrip('\ufeff')
    
    fname_match = re.match(r'Cap(\d+)_', filepath.name)
    fname_cap = int(fname_match.group(1)) if fname_match else None
    folder_cap = int(re.search(r'Cap(\d+)', filepath.parent.name).group(1))
    
    yaml = {}
    for field in ['best_fit_chapter', 'evaluated_chapter', 'target_chapter', 'title_la', 'length_tier']:
        m = re.search(rf'^{field}:\s*"?(\d+[\.\d]*|\w+)"?', text, re.MULTILINE)
        if m:
            val = m.group(1)
            try:
                val = int(val) if '.' not in str(val) else float(val)
            except:
                pass
            yaml[field] = val
    
    best = yaml.get('best_fit_chapter') or yaml.get('evaluated_chapter')
    return fname_cap, folder_cap, best, yaml


def main():
    mode = "DRY-RUN" if DRY_RUN else "EXECUTE"
    print("=" * 60)
    print(f"  严格双重审计 v2 — {mode}")
    print("  铁律: 文件名前缀 = 文件夹章号")
    print("=" * 60)
    
    all_files = []
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        for md_file in sorted(cap_dir.glob('*.md')):
            all_files.append(md_file)
    
    print(f"\n[扫描] {len(all_files)} 个文件\n")
    
    # 分类
    rename_only = []   # (fpath, old_name, new_name) — 同文件夹改前缀
    move_files = []    # (fpath, src_cap, dst_cap, reason, title)
    ok_count = 0
    
    for fpath in all_files:
        fname_cap, folder_cap, best_cap, yaml = read_meta(fpath)
        title = yaml.get('title_la', '?')
        
        if fname_cap is None:
            ok_count += 1
            continue
        
        # 文件名前缀 == 文件夹 → OK
        if fname_cap == folder_cap:
            ok_count += 1
            continue
        
        # 不一致。决定去向：以 best_fit_chapter 为准
        if best_cap is None:
            # 无算法定级 → 以文件名前缀为准，移动到对应文件夹
            move_files.append((fpath, folder_cap, fname_cap, 
                f"无best_fit，以文件名Cap{fname_cap}为准", title))
        elif best_cap == folder_cap:
            # 算法说放这里对，但文件名前缀错了 → 改名
            new_name = fpath.name.replace(f'Cap{fname_cap}_', f'Cap{best_cap}_', 1)
            rename_only.append((fpath, fpath.name, new_name, best_cap))
        else:
            # 算法说应该去别处 → 移动
            move_files.append((fpath, folder_cap, best_cap,
                f"best_fit=Cap{best_cap}, fname=Cap{fname_cap}", title))
    
    print(f"  [OK] 正确: {ok_count} 篇")
    print(f"  [改名] 前缀修正: {len(rename_only)} 篇")
    print(f"  [移动] 搬家: {len(move_files)} 篇")
    
    need_action = rename_only or move_files
    if not need_action:
        print(f"\n  [OK] 全部正确！")
        print_stats()
        return
    
    # 打印待改名
    if rename_only:
        print(f"\n  --- 仅改前缀（同文件夹）---")
        for fpath, old, new, cap in rename_only[:20]:
            print(f"    {old} → {new}")
        if len(rename_only) > 20:
            print(f"    ... 还有 {len(rename_only)-20} 篇")
    
    # 打印待移动
    if move_files:
        print(f"\n  --- 搬家到正确文件夹 ---")
        for fpath, src, dst, reason, title in sorted(move_files, key=lambda x: abs(x[1]-x[2]), reverse=True)[:30]:
            print(f"    Cap{src} → Cap{dst}  {fpath.name}  《{title}》  ({reason})")
        if len(move_files) > 30:
            print(f"    ... 还有 {len(move_files)-30} 篇")
    
    # 执行
    if not DRY_RUN:
        print(f"\n[执行] 开始修复...")
        
        # 先改名
        for fpath, old, new, cap in rename_only:
            new_path = fpath.with_name(new)
            if new_path.exists():
                # 避免覆盖
                stem = fpath.stem
                counter = 1
                while new_path.exists():
                    new_path = fpath.with_name(f"{stem}_rn{counter}.md")
                    counter += 1
            fpath.rename(new_path)
        print(f"  [改名] {len(rename_only)} 篇")
        
        # 再移动
        moved = 0
        for fpath, src, dst, reason, title in move_files:
            dst_dir = REALITATES_DIR / f"Cap{dst}"
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst_path = dst_dir / fpath.name
            if dst_path.exists():
                stem = fpath.stem
                counter = 1
                while dst_path.exists():
                    dst_path = dst_dir / f"{stem}_mv{counter}.md"
                    counter += 1
            shutil.move(str(fpath), str(dst_path))
            moved += 1
        print(f"  [移动] {moved} 篇")
        
        # 清理空目录
        for cap_dir in sorted(REALITATES_DIR.iterdir()):
            if cap_dir.is_dir() and cap_dir.name.startswith('Cap') and not any(cap_dir.iterdir()):
                cap_dir.rmdir()
                print(f"  [清理] 空目录 {cap_dir.name}")
    
    # 重新统计
    print_stats()
    
    if DRY_RUN:
        print(f"\n  ⚠️ DRY-RUN。执行: python3 _reaudit_v2.py --execute")


def print_stats():
    stats = defaultdict(lambda: {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0})
    
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        cap_num = int(re.search(r'\d+', cap_dir.name).group())
        for md_file in cap_dir.glob('*.md'):
            name = md_file.name.lower()
            if 'longus' in name:
                stats[cap_num]['longus'] += 1
            elif 'medius' in name:
                stats[cap_num]['medius'] += 1
            else:
                stats[cap_num]['brevis'] += 1
            stats[cap_num]['total'] += 1
    
    print(f"\n{'='*50}")
    print(f"  章节分布")
    print(f"{'='*50}")
    print(f"  {'章':>4}  {'短篇':>5}  {'中篇':>5}  {'长篇':>5}  {'总计':>5}  {'状态':>6}")
    print(f"  {'-'*42}")
    
    total_all = {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0}
    for cap in sorted(stats.keys()):
        s = stats[cap]
        for k in total_all:
            total_all[k] += s[k]
        status = "OK" if s['total'] >= 10 else f"缺{10-s['total']}"
        print(f"  Cap{cap:>2}  {s['brevis']:>5}  {s['medius']:>5}  {s['longus']:>5}  {s['total']:>5}  {status:>6}")
    
    print(f"  {'-'*42}")
    print(f"  {'合计':>4}  {total_all['brevis']:>5}  {total_all['medius']:>5}  {total_all['longus']:>5}  {total_all['total']:>5}")
    
    gaps = [f"Cap{c}" for c in sorted(stats.keys()) if stats[c]['total'] < 10]
    if gaps:
        print(f"\n  [!!] 缺口: {', '.join(gaps)}")
    print()


if __name__ == '__main__':
    main()
