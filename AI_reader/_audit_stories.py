#!/usr/bin/env python3
"""
故事文件综合审计脚本 v1_0_0
功能：
  1. 检测完全重复的故事（正文内容相同）
  2. 检查每个章节文件夹下的故事定级是否正确
  3. 全量统计故事分布
"""

import os
import re
import json
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).parent / "realitates"
REALITATES_JSON = Path(__file__).parent / "realitates.json"


def extract_yaml_and_body(filepath: Path) -> tuple[dict, str, str]:
    """提取 YAML 元数据 + 拉丁正文（去长音符号版），返回 (yaml_dict, body_raw, body_normalized)"""
    text = filepath.read_text(encoding='utf-8', errors='replace')
    # 把 BOM 和其他不可见字符清理掉
    text = text.lstrip('\ufeff')
    
    # 查找 YAML frontmatter
    yaml_dict = {}
    body_start = 0
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            yaml_text = parts[1]
            body_start = len(parts[0]) + len(parts[1]) + 6  # 两个 --- 各3字符
            body_raw = text[body_start:].strip()
    else:
        body_raw = text.strip()
    
    # 解析 YAML 核心字段
    for field in ['story_id', 'title_la', 'title_zh', 'target_chapter', 
                   'evaluated_chapter', 'best_fit_chapter', 'length_tier',
                   'coverage_rate', 'word_count', 'macrons_status']:
        match = re.search(rf'^{field}:\s*(.+?)$', text, re.MULTILINE)
        if match:
            val = match.group(1).strip().strip('"').strip("'")
            # 尝试转数字
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except (ValueError, TypeError):
                pass
            yaml_dict[field] = val
    
    # 生成正文特征指纹（去长音、去标点、小写、按词排序）
    body_norm = re.sub(r'[āēīōūȳǣ]', '', body_raw.lower()) if body_raw else ''
    body_norm = re.sub(r'[^a-z\s]', ' ', body_norm)
    words = sorted(w for w in body_norm.split() if len(w) > 1)
    
    return yaml_dict, body_raw, ' '.join(words)


def hash_body(body: str) -> str:
    """正文 SHA256"""
    return hashlib.sha256(body.encode('utf-8')).hexdigest()[:16]


def main():
    print("=" * 60)
    print("  故事文件综合审计")
    print("=" * 60)
    
    # 收集所有 .md 文件
    all_files = {}
    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir() or not cap_dir.name.startswith('Cap'):
            continue
        cap_num = int(re.search(r'\d+', cap_dir.name).group())
        for md_file in sorted(cap_dir.glob('*.md')):
            all_files[md_file] = cap_num
    
    print(f"\n[扫描] 共发现 {len(all_files)} 个 .md 文件，分布在 {len(set(all_files.values()))} 个章节文件夹\n")
    
    # ============================================================
    # 第一步：检测重复
    # ============================================================
    print("=" * 40)
    print("  一、重复检测")
    print("=" * 40)
    
    # 按正文 hash 分组
    hash_groups = defaultdict(list)  # hash -> [(filepath, yaml, body)]
    file_data = {}  # filepath -> (yaml, body, hash)
    
    for fpath, cap in all_files.items():
        try:
            yaml, body, norm = extract_yaml_and_body(fpath)
            h = hash_body(norm)
            hash_groups[h].append((fpath, yaml, cap))
            file_data[fpath] = (yaml, h)
        except Exception as e:
            print(f"  [!] 读取失败: {fpath.name} — {e}")
    
    # 找出重复组
    duplicates_found = []
    for h, files in hash_groups.items():
        if len(files) > 1:
            duplicates_found.append(files)
    
    if duplicates_found:
        print(f"\n  [!!] 发现 {len(duplicates_found)} 组重复（共 {sum(len(g)-1 for g in duplicates_found)} 篇多余）：\n")
        for i, group in enumerate(duplicates_found, 1):
            print(f"  重复组 {i} ({len(group)} 篇):")
            for fpath, yaml, cap in group:
                title = yaml.get('title_la', '?')
                length = yaml.get('length_tier', '?')
                print(f"    - [Cap{cap}] {fpath.name}  《{title}》({length})")
            print()
    else:
        print("\n  [OK] 未发现完全重复的故事。")
    
    # ============================================================
    # 第二步：章节放置检查
    # ============================================================
    print("=" * 40)
    print("  二、章节放置检查")
    print("=" * 40)
    
    misplaced = []  # (filepath, folder_cap, best_cap)
    
    for fpath, cap_folder in all_files.items():
        try:
            yaml, body, norm = extract_yaml_and_body(fpath)
        except:
            continue
        
        # 判断故事该放哪章
        best_cap = yaml.get('best_fit_chapter') or yaml.get('evaluated_chapter')
        if best_cap is None:
            misplaced.append((fpath, cap_folder, None, "无定级信息"))
            continue
        
        diff = abs(cap_folder - best_cap)
        if diff > 2 and cap_folder != best_cap:  # 允许 ±2 的容差，超过才算放错
            misplaced.append((fpath, cap_folder, best_cap, f"偏差 {diff} 章"))
    
    if misplaced:
        print(f"\n  [!!] 发现 {len(misplaced)} 篇可能放错文件夹的故事：\n")
        for fpath, folder_cap, best_cap, reason in sorted(misplaced, key=lambda x: abs((x[1] or 0) - (x[2] or 0)), reverse=True):
            title = extract_yaml_and_body(fpath)[0].get('title_la', '?')
            print(f"    - {fpath.name}  当前: Cap{folder_cap} → 应为: Cap{best_cap} ({reason})  《{title}》")
    else:
        print("\n  [OK] 所有故事放置正确（偏差 ≤ 2 章）。")
    
    # ============================================================
    # 第三步：全量统计
    # ============================================================
    print("\n" + "=" * 40)
    print("  三、全量统计")
    print("=" * 40)
    
    stats = defaultdict(lambda: {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0, 'zero_macrons': 0})
    
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
            tier_key = 'brevis'  # 默认
        
        stats[cap_folder][tier_key] += 1
        stats[cap_folder]['total'] += 1
        
        # 检查零长音
        macrons = yaml.get('macrons_status', '')
        if macrons == 'missing' or macrons == 'none':
            stats[cap_folder]['zero_macrons'] += 1
        elif not macrons:
            # 检查正文是否有长音
            if body:
                has_macron = bool(re.search(r'[āēīōūȳǣ]', body))
                if not has_macron:
                    stats[cap_folder]['zero_macrons'] += 1
    
    # 打印表格
    print(f"\n  {'章':>4}  {'短篇B':>5}  {'中篇M':>5}  {'长篇L':>5}  {'总计':>5}  {'零长音':>6}  {'状态':>6}")
    print("  " + "-" * 52)
    
    total_all = {'brevis': 0, 'medius': 0, 'longus': 0, 'total': 0, 'zero_macrons': 0}
    
    for cap in sorted(stats.keys()):
        s = stats[cap]
        for k in total_all:
            total_all[k] += s[k]
        
        status = "OK" if s['total'] >= 10 else f"缺{10 - s['total']}"
        zero_flag = f"!!{s['zero_macrons']}" if s['zero_macrons'] > 0 else "0"
        print(f"  Cap{cap:>2}  {s['brevis']:>5}  {s['medius']:>5}  {s['longus']:>5}  {s['total']:>5}  {zero_flag:>6}  {status:>6}")
    
    print("  " + "-" * 52)
    print(f"  {'合计':>4}  {total_all['brevis']:>5}  {total_all['medius']:>5}  {total_all['longus']:>5}  {total_all['total']:>5}  {total_all['zero_macrons']:>6}")
    
    # 更新 realitates.json
    print(f"\n  [*] 总故事数: {total_all['total']}")
    print(f"  [*] 零长音故事: {total_all['zero_macrons']}")
    
    # 缺口汇总
    gaps = []
    for cap in sorted(stats.keys()):
        if stats[cap]['total'] < 10:
            gaps.append(f"Cap{cap}(缺{10 - stats[cap]['total']})")
    
    if gaps:
        print(f"\n  [!!] 缺口章节: {', '.join(gaps)}")
    else:
        print("\n  [OK] 所有章节均 ≥ 10 篇！")
    
    # 导出 JSON 统计
    output = {
        "scan_time": "2026-07-01",
        "total_stories": total_all['total'],
        "duplicate_groups": len(duplicates_found),
        "duplicate_files": sum(len(g)-1 for g in duplicates_found),
        "misplaced_files": len(misplaced),
        "zero_macron_stories": total_all['zero_macrons'],
        "gaps": gaps,
        "per_chapter": {str(c): dict(stats[c]) for c in sorted(stats.keys())}
    }
    
    stats_path = Path(__file__).parent / "_audit_result.json"
    stats_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n  统计结果已写入: {stats_path.name}")
    
    print("\n" + "=" * 60)
    print("  审计完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
