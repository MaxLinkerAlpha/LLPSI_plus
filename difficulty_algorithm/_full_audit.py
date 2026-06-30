#!/usr/bin/env python3
"""
全量重评审计 v1_1_0 — 适配恢复后的 33K 词表
遍历 realitates/ 下所有故事，对每篇：
  1. 提取拉丁正文
  2. 调用 evaluate_v2.evaluate() 重新评级
  3. 对比：文件名前缀 / YAML best_fit / 算法评级 / 文件夹
  4. 输出完整对照表
"""

import sys, os, re, json
from pathlib import Path
from collections import defaultdict, Counter

# 从 difficulty_algorithm 目录运行
SCRIPT_DIR = Path(__file__).parent
REALITATES_DIR = SCRIPT_DIR.parent / "AI_reader" / "realitates"

# 导入 evaluate_v2
sys.path.insert(0, str(SCRIPT_DIR))
from evaluate_v2 import evaluate as eval_text


def extract_body(path: Path) -> str:
    """提取 .md 文件的拉丁正文（跳过 YAML frontmatter）"""
    text = path.read_text(encoding='utf-8', errors='replace')
    text = text.lstrip('\ufeff')
    if text.startswith('---'):
        parts = text.split('---', 2)
        return parts[2].strip() if len(parts) >= 3 else text
    return text.strip()


def extract_meta(text: str) -> dict:
    """提取 YAML 元数据"""
    meta = {}
    for field in ['best_fit_chapter', 'evaluated_chapter', 'target_chapter',
                  'title_la', 'title_zh', 'length_tier', 'coverage_rate',
                  'macrons_status', 'word_count']:
        m = re.search(rf'^{field}:\s*"?([^"\n]+)"?', text, re.MULTILINE)
        if m:
            val = m.group(1).strip()
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    pass
            meta[field] = val
    return meta


def main():
    print("=" * 70)
    print("  全量重评审计")
    print("  加载 evaluate_v2 映射表...")
    print("=" * 70)

    # 收集所有文件
    files = []
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        for md_file in sorted(cap_dir.glob('*.md')):
            files.append(md_file)

    total = len(files)
    print(f"\n[扫描] {total} 个文件，开始评估...\n")

    # 统计
    stats = {
        'ok': 0,           # 全部一致
        'fname_vs_folder': 0,  # 文件名前缀与文件夹不一致
        'algo_vs_folder': 0,   # 算法评级与文件夹不一致(>2)
        'algo_vs_yaml': 0,     # 算法评级与 YAML 不一致(>2)
        'low_coverage': 0,     # 覆盖率 < 85%
        'errors': 0,
    }
    
    issues = []  # 所有不符项

    for i, fpath in enumerate(files):
        if i % 50 == 0:
            print(f"  处理中... {i}/{total}", file=sys.stderr, flush=True)
        
        try:
            raw_text = fpath.read_text(encoding='utf-8', errors='replace')
            body = extract_body(fpath)
            meta = extract_meta(raw_text)
        except Exception as e:
            stats['errors'] += 1
            issues.append({
                'file': fpath.name,
                'folder': fpath.parent.name,
                'error': str(e),
            })
            continue

        # 提取各维度章节号
        folder_cap = int(re.search(r'Cap(\d+)', fpath.parent.name).group(1))
        fname_match = re.match(r'Cap(\d+)_', fpath.name)
        fname_cap = int(fname_match.group(1)) if fname_match else None
        yaml_best = meta.get('best_fit_chapter') or meta.get('evaluated_chapter')
        title = meta.get('title_la', '?')

        # 重新评级
        result = eval_text(body, fpath.name)
        algo_level = result.get('v2_level')
        algo_rate = result.get('v2_rate', 0)
        algo_oov = result.get('v2_oov', [])

        # 判断各项是否一致
        fname_ok = (fname_cap is None) or (fname_cap == folder_cap)
        algo_ok = (algo_level is not None) and (abs(algo_level - folder_cap) <= 2)
        yaml_ok = (yaml_best is not None) and (abs(int(yaml_best) - folder_cap) <= 2)
        coverage_ok = algo_rate >= 85

        if fname_ok and algo_ok and yaml_ok and coverage_ok:
            stats['ok'] += 1
            continue

        # 记录问题
        problem = {
            'file': fpath.name,
            'folder': f'Cap{folder_cap}',
            'fname_cap': fname_cap,
            'yaml_best': yaml_best,
            'algo_level': algo_level,
            'algo_rate': round(algo_rate, 1),
            'title': title,
            'issues': [],
        }
        if not fname_ok:
            problem['issues'].append(f'文件名Cap{fname_cap}≠文件夹')
            stats['fname_vs_folder'] += 1
        if not algo_ok and algo_level is not None:
            problem['issues'].append(f'算法Cap{algo_level}≠文件夹Cap{folder_cap}')
            stats['algo_vs_folder'] += 1
        if not yaml_ok and yaml_best is not None:
            problem['issues'].append(f'YAML Cap{yaml_best}≠文件夹Cap{folder_cap}')
            stats['algo_vs_yaml'] += 1
        if not coverage_ok:
            problem['issues'].append(f'覆盖率{algo_rate}%<85%')
            stats['low_coverage'] += 1
        
        issues.append(problem)

    print(f"\n[完成] 评估 {total} 篇\n")

    # ============================================================
    # 汇总
    # ============================================================
    print("=" * 70)
    print("  汇总")
    print("=" * 70)
    print(f"  全部一致:        {stats['ok']} 篇")
    print(f"  文件名≠文件夹:   {stats['fname_vs_folder']} 篇")
    print(f"  算法≠文件夹(>2): {stats['algo_vs_folder']} 篇")
    print(f"  YAML≠文件夹(>2): {stats['algo_vs_yaml']} 篇")
    print(f"  覆盖率<85%:       {stats['low_coverage']} 篇")
    print(f"  读取错误:         {stats['errors']} 篇")
    print(f"  问题总数:         {len(issues)} 篇")

    if not issues:
        print("\n  [OK] 全部正确！")
        return

    # ============================================================
    # 按文件夹分组打印问题表
    # ============================================================
    print(f"\n{'='*70}")
    print(f"  问题明细（按文件夹分组）")
    print(f"{'='*70}")

    by_folder = defaultdict(list)
    for p in issues:
        by_folder[p['folder']].append(p)

    for folder in sorted(by_folder.keys()):
        group = by_folder[folder]
        print(f"\n  [{folder}] {len(group)} 篇问题：")
        print(f"  {'文件名':<55} {'标题':<25} {'算法':>5} {'YAML':>5} {'覆盖率':>6}  {'问题'}")
        print(f"  {'-'*110}")
        for p in group:
            algo_str = f"Cap{p['algo_level']}" if p['algo_level'] else '?'
            yaml_str = f"Cap{p['yaml_best']}" if p['yaml_best'] is not None else '?'
            title_short = p['title'][:22] if p['title'] else '?'
            issues_str = ' | '.join(p['issues'])
            print(f"  {p['file']:<55} {title_short:<25} {algo_str:>5} {yaml_str:>5} {p['algo_rate']:>5}%  {issues_str}")

    # ============================================================
    # 按问题类型统计
    # ============================================================
    print(f"\n{'='*70}")
    print(f"  章节分布变化（算法重评后）")
    print(f"{'='*70}")
    
    algo_dist = Counter()
    folder_dist = Counter()
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        cap_num = int(re.search(r'\d+', cap_dir.name).group())
        for md_file in cap_dir.glob('*.md'):
            folder_dist[cap_num] += 1
            try:
                body = extract_body(md_file)
                result = eval_text(body, md_file.name)
                lvl = result.get('v2_level')
                if lvl:
                    algo_dist[lvl] += 1
            except:
                pass

    print(f"  {'章':>4}  {'文件夹':>6}  {'算法定级':>8}  {'偏差':>4}")
    print(f"  {'-'*28}")
    all_caps = sorted(set(list(folder_dist.keys()) + list(algo_dist.keys())))
    for c in all_caps:
        f = folder_dist.get(c, 0)
        a = algo_dist.get(c, 0)
        diff = a - f if a and f else ''
        marker = ''
        if f < 10:
            marker = f' ⚠️ 缺{10-f}'
        print(f"  Cap{c:>2}  {f:>6}  {a:>8}  {diff:>4}{marker}")


if __name__ == '__main__':
    main()
