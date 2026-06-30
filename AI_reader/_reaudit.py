#!/usr/bin/env python3
"""
双重审计脚本 v1_0_0
检查两个维度：
  1. 文件名前缀 CapN_ 是否与所在文件夹 CapN/ 一致
  2. YAML best_fit_chapter 是否与所在文件夹一致
然后自动修复（移动）
用法：
  python3 _reaudit.py           # dry-run
  python3 _reaudit.py --execute  # 执行移动
"""

import os, re, sys, shutil
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).parent / "realitates"
DRY_RUN = '--execute' not in sys.argv


def extract_caps(filepath: Path):
    """从文件和 YAML 中提取章节信息"""
    text = filepath.read_text(encoding='utf-8', errors='replace')
    text = text.lstrip('\ufeff')
    
    # 文件名中的章节号
    fname_match = re.match(r'Cap(\d+)_', filepath.name)
    fname_cap = int(fname_match.group(1)) if fname_match else None
    
    # YAML 中的章节号
    yaml_caps = {}
    for field in ['best_fit_chapter', 'evaluated_chapter', 'target_chapter']:
        m = re.search(rf'^{field}:\s*(\d+)', text, re.MULTILINE)
        if m:
            yaml_caps[field] = int(m.group(1))
    
    # 文件夹的章节号
    folder_cap = int(re.search(r'Cap(\d+)', filepath.parent.name).group(1))
    
    return fname_cap, yaml_caps, folder_cap


def main():
    mode = "DRY-RUN" if DRY_RUN else "EXECUTE"
    print("=" * 60)
    print(f"  双重审计 — {mode}")
    print("=" * 60)
    
    # 收集所有文件
    all_files = []
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        for md_file in sorted(cap_dir.glob('*.md')):
            all_files.append(md_file)
    
    print(f"\n[扫描] {len(all_files)} 个文件\n")
    
    # ============================================================
    # 分析每个文件
    # ============================================================
    issues = []  # (filepath, folder_cap, fname_cap, yaml_best_cap, problem_desc)
    correct = 0
    
    for fpath in all_files:
        try:
            fname_cap, yaml_caps, folder_cap = extract_caps(fpath)
        except Exception as e:
            print(f"  [!] 读取失败: {fpath.name} — {e}")
            continue
        
        # 最佳章节：优先 best_fit_chapter，fallback evaluated_chapter
        best_cap = yaml_caps.get('best_fit_chapter') or yaml_caps.get('evaluated_chapter')
        
        # 判断文件应该去哪个文件夹
        target_folder = None
        
        # 规则1：文件名前缀优先（通常是最后写入时的算法结果）
        # 规则2：如果 YAML best_fit 和 fname 一致，用那个
        # 规则3：否则用 YAML best_fit
        
        if fname_cap and best_cap and fname_cap == best_cap:
            target_folder = best_cap
        elif best_cap and fname_cap and abs(best_cap - fname_cap) <= 2:
            target_folder = best_cap  # 信任算法
        elif best_cap:
            target_folder = best_cap
        elif fname_cap:
            target_folder = fname_cap
        
        if target_folder is None:
            issues.append((fpath, folder_cap, fname_cap, best_cap, "无法确定目标章节"))
            continue
        
        # 检查是否放对
        if folder_cap == target_folder:
            correct += 1
            continue
        
        # 偏差 ≤ 2 也接受（算法容差）
        if abs(folder_cap - target_folder) <= 2:
            correct += 1
            continue
        
        # 需要移动
        if fname_cap and fname_cap != folder_cap:
            problem = f"文件名Cap{fname_cap} ≠ 文件夹Cap{folder_cap}"
        else:
            problem = f"YAML定级Cap{target_folder} ≠ 文件夹Cap{folder_cap}"
        
        issues.append((fpath, folder_cap, fname_cap, target_folder, problem))
    
    print(f"  [OK] 正确放置: {correct} 篇")
    
    if not issues:
        print(f"  [OK] 全部正确，无需移动！")
        # 仍然统计
        print_stats()
        return
    
    print(f"\n  [!!] 需移动: {len(issues)} 篇\n")
    
    # 按目标章节分组统计
    by_target = defaultdict(list)
    for fpath, folder_cap, fname_cap, target_cap, problem in issues:
        by_target[target_cap].append((fpath, folder_cap, fname_cap, problem))
    
    for target_cap in sorted(by_target):
        group = by_target[target_cap]
        print(f"  → Cap{target_cap} ({len(group)} 篇):")
        for fpath, folder_cap, fname_cap, problem in group:
            title = fpath.stem
            print(f"      {fpath.name}  [当前在 Cap{folder_cap}]  {problem}")
    
    # 执行移动
    if not DRY_RUN:
        print(f"\n  [执行] 开始移动...")
        moved = 0
        for fpath, folder_cap, fname_cap, target_cap, problem in issues:
            dst_dir = REALITATES_DIR / f"Cap{target_cap}"
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst_path = dst_dir / fpath.name
            
            if dst_path.exists():
                # 添加后缀避免覆盖
                stem = fpath.stem
                counter = 1
                while dst_path.exists():
                    dst_path = dst_dir / f"{stem}_mv{counter}.md"
                    counter += 1
            
            shutil.move(str(fpath), str(dst_path))
            moved += 1
        
        # 清理空目录
        for cap_dir in sorted(REALITATES_DIR.iterdir()):
            if cap_dir.is_dir() and cap_dir.name.startswith('Cap') and not any(cap_dir.iterdir()):
                cap_dir.rmdir()
        
        print(f"  [完成] 移动了 {moved} 篇")
    
    # 最终统计
    print_stats()
    
    if DRY_RUN:
        print(f"\n  ⚠️ DRY-RUN 模式。执行: python3 _reaudit.py --execute")


def print_stats():
    """打印最终统计"""
    stats = defaultdict(lambda: {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0})
    
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        cap_num = int(re.search(r'\d+', cap_dir.name).group())
        for md_file in cap_dir.glob('*.md'):
            # 从文件名判断篇幅
            name = md_file.name.lower()
            if 'longus' in name:
                stats[cap_num]['longus'] += 1
            elif 'medius' in name:
                stats[cap_num]['medius'] += 1
            else:
                stats[cap_num]['brevis'] += 1
            stats[cap_num]['total'] += 1
    
    print(f"\n{'='*50}")
    print(f"  最终统计")
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
