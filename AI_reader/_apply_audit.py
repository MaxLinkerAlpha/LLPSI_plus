#!/usr/bin/env python3
"""
应用全量重评结果 v1_1_0
读 _full_audit.py 输出日志，对每篇不符项做最小改动：
  1. 文件名前缀 ≠ 文件夹 → 改名（不动内容）
  2. 算法定级 ≠ 文件夹 (>2章) → 移动到 best_fit 决定的文件夹
  3. 覆盖率 < 85% → 不动（数据问题，非结构问题）
"""

import re, sys, shutil
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).parent / "realitates"


def main():
    if not REALITATES_DIR.exists():
        print(f"[ERROR] 目录不存在: {REALITATES_DIR}")
        sys.exit(1)

    # 收集所有文件
    all_files = list(REALITATES_DIR.rglob("Cap*_*.md"))
    print(f"[扫描] {len(all_files)} 个文件")

    renamed = 0
    moved = 0
    skipped = 0

    for fpath in all_files:
        text = fpath.read_text(encoding='utf-8', errors='replace')
        # 文件名章号
        fname_match = re.match(r'Cap(\d+)_', fpath.name)
        if not fname_match:
            skipped += 1
            continue
        fname_cap = int(fname_match.group(1))
        # 文件夹章号
        folder_cap = int(re.search(r'Cap(\d+)', fpath.parent.name).group(1))

        # 优先级：YAML best_fit > 文件名前缀
        yaml_best = None
        for field in ['best_fit_chapter', 'evaluated_chapter']:
            m = re.search(rf'^{field}:\s*(\d+)', text, re.MULTILINE)
            if m:
                yaml_best = int(m.group(1))
                break

        # 决定最终目标章号
        # 规则：YAML best_fit 优先；YAML 无值则用文件名前缀
        target_cap = yaml_best if yaml_best is not None else fname_cap

        # 一致：跳过
        if fname_cap == target_cap and folder_cap == target_cap:
            continue

        # 容差：算法与文件夹差 ≤ 2 时不动（保护 Cap2-4 这类边缘章）
        if abs(folder_cap - target_cap) <= 2:
            continue

        # 文件夹就是低章（Cap1-4）：除非算法判得很离谱（>4），否则保护
        if folder_cap <= 4 and target_cap - folder_cap <= 4:
            continue

        # 仅文件名前缀错（文件夹对）：改名
        if fname_cap != target_cap and folder_cap == target_cap:
            new_name = fpath.name.replace(f'Cap{fname_cap}_', f'Cap{target_cap}_', 1)
            new_path = fpath.with_name(new_name)
            if new_path.exists():
                stem = fpath.stem
                counter = 1
                while new_path.exists():
                    new_path = fpath.with_name(f"{stem}_rn{counter}.md")
                    counter += 1
            fpath.rename(new_path)
            renamed += 1
            continue

        # 文件夹不对（可能前缀也对、也可能不对）：移动
        dst_dir = REALITATES_DIR / f"Cap{target_cap}"
        dst_dir.mkdir(parents=True, exist_ok=True)
        # 移动时同时修正前缀
        if fname_cap != target_cap:
            dst_name = fpath.name.replace(f'Cap{fname_cap}_', f'Cap{target_cap}_', 1)
        else:
            dst_name = fpath.name
        dst_path = dst_dir / dst_name
        if dst_path.exists():
            stem = dst_path.stem
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
            print(f"  [清理] 空目录 {cap_dir.name}")

    print(f"\n[完成] 改名 {renamed} 篇，移动 {moved} 篇，跳过 {skipped} 篇")


if __name__ == '__main__':
    main()
