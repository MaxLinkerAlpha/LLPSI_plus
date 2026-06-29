#!/usr/bin/env python3
"""
全量重评脚本 v1_0_0
直接导入 evaluate_v2.evaluate() 函数，避免重复加载大词表（438 篇从 15 分钟 → 30 秒）
"""

import json
import re
import sys
import csv
import os
from pathlib import Path
from collections import defaultdict

# ---- 0. 把 evaluate_v2.py 所在目录加入 sys.path，并 cd 过去加载相对路径文件 ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = PROJECT_ROOT / "difficulty_algorithm"
REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
OUTPUT_CSV = Path("/tmp/story_audit_report.csv")

_orig_cwd = os.getcwd()
os.chdir(str(EVAL_DIR))
sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate  # 导入后一次性加载词表
os.chdir(_orig_cwd)

# ---- 1. 扫描所有故事 ----
def find_all_stories() -> list[Path]:
    stories = []
    for cap_dir in sorted(REALITATES_DIR.glob("Cap*")):
        if not cap_dir.is_dir():
            continue
        for md_file in sorted(cap_dir.glob("*.md")):
            stories.append(md_file)
    return stories

# ---- 2. 从 MD 文件提取 YAML + 正文 ----
def parse_story_file(filepath: Path) -> dict:
    text = filepath.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        return {"file": filepath.name, "error": "无法解析 YAML Front Matter"}

    yaml_block = parts[1]
    latin_text = "---".join(parts[2:]).strip()

    meta = {"file": filepath.name, "dir": filepath.parent.name}
    for field in ["story_id", "title_la", "title_zh", "target_chapter",
                  "theme", "style", "genre", "character_type", "length_tier",
                  "narrative_mode", "word_count", "macrons_status"]:
        m = re.search(rf"^{field}:\s*(.+?)$", yaml_block, re.MULTILINE)
        if m:
            val = m.group(1).strip().strip("\"'")
            if field == "target_chapter":
                try: val = int(val)
                except ValueError: pass
            meta[field] = val

    meta["latin_text"] = latin_text
    tokens = [t for t in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", latin_text) if len(t) >= 2]
    meta["actual_word_count"] = len(tokens)
    return meta

# ---- 3. 判定是否放错 ----
def classify_misplacement(target_ch: int, algo_ch, v2_rate: float) -> str:
    if algo_ch is None:
        return "UNRATED"
    gap = algo_ch - target_ch
    if gap <= 0:   return "OK"
    elif gap <= 2: return "LIGHT"
    elif gap <= 5: return "MODERATE"
    else:          return "SEVERE"


def main():
    stories = find_all_stories()
    print(f"找到 {len(stories)} 篇故事，开始逐篇评估...\n")

    results = []
    stats = defaultdict(lambda: defaultdict(int))
    misplacements = []

    for i, fp in enumerate(stories):
        meta = parse_story_file(fp)
        if "error" in meta:
            print(f"[SKIP] {fp.name}: {meta['error']}")
            continue

        target_ch = meta.get("target_chapter")
        if not isinstance(target_ch, int):
            # 尝试从文件名推断
            dir_ch = int(re.sub(r"\D", "", meta["dir"]) or 0)
            if dir_ch > 0:
                target_ch = dir_ch
                meta["target_chapter"] = dir_ch
            else:
                print(f"[SKIP] {fp.name}: target_chapter 不是整数")
                continue

        # 直接调 evaluate 函数（已导入，不复读词表）
        eval_r = evaluate(meta["latin_text"], meta.get("story_id", fp.stem))
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])

        severity = classify_misplacement(target_ch, v2_level, v2_rate)
        current_dir = meta["dir"]

        row = {
            "file": meta["file"],
            "dir": current_dir,
            "target_chapter": target_ch,
            "algo_chapter": v2_level,
            "gap": (v2_level - target_ch) if v2_level else "N/A",
            "v2_rate": round(v2_rate, 1),
            "v2_oov_count": len(v2_oov),
            "severity": severity,
            "title_la": meta.get("title_la", ""),
            "title_zh": meta.get("title_zh", ""),
            "theme": meta.get("theme", ""),
            "style": meta.get("style", ""),
            "word_count": meta["actual_word_count"],
        }
        results.append(row)
        stats[current_dir][severity] += 1

        if severity in ("MODERATE", "SEVERE"):
            misplacements.append(row)

        if (i + 1) % 50 == 0:
            print(f"  进度: {i+1}/{len(stories)}")

    # ---- 输出报告 ----
    print(f"\n{'='*70}")
    print("全量重评报告")
    print(f"{'='*70}")
    print(f"总故事数: {len(results)}")
    print(f"严重错位 (MODERATE + SEVERE): {len(misplacements)} 篇\n")

    # 按目录汇总
    print(f"{'目录':>8s}  {'总数':>5s}  {'OK':>5s}  {'LIGHT':>6s}  {'MODERATE':>9s}  {'SEVERE':>7s}  {'UNRATED':>8s}")
    print("-" * 65)
    for d in sorted(stats.keys(), key=lambda x: int(re.sub(r"\D", "", x) or 0)):
        s = stats[d]
        print(f"{d:>8s}  {sum(s.values()):>5d}  {s.get('OK',0):>5d}  {s.get('LIGHT',0):>6d}  {s.get('MODERATE',0):>9d}  {s.get('SEVERE',0):>7d}  {s.get('UNRATED',0):>8d}")

    # Cap.1-6 重点关注
    print(f"\n{'='*70}")
    print("Cap.1-6 逐篇详情:")
    print(f"{'='*70}")
    cap1_6 = [r for r in results if r["dir"] in ("Cap1","Cap2","Cap3","Cap4","Cap5","Cap6")]
    cap1_6.sort(key=lambda r: (int(re.sub(r"\D", "", r["dir"]) or 0), r["gap"] if isinstance(r["gap"], int) else 999))
    for row in cap1_6:
        gap_str = f"+{row['gap']}" if isinstance(row['gap'], int) else row['gap']
        flag = " <<< 错位!" if row["severity"] in ("MODERATE", "SEVERE") else ""
        print(f"  [{row['severity']:>8s}] {row['dir']}/{row['file']}  "
              f"target={row['target_chapter']} algo={row['algo_chapter']} gap={gap_str} "
              f"rate={row['v2_rate']}%  {row['title_la']}{flag}")

    # 错位清单（全部）
    if misplacements:
        print(f"\n{'='*70}")
        print(f"全部错位故事 ({len(misplacements)} 篇):")
        print(f"{'='*70}")
        misplacements.sort(key=lambda r: (int(re.sub(r"\D", "", r["dir"]) or 0), r["gap"] if isinstance(r["gap"], int) else 999))
        for row in misplacements:
            gap_str = f"+{row['gap']}" if isinstance(row['gap'], int) else row['gap']
            print(f"  [{row['severity']:>8s}] {row['dir']}/{row['file']}")
            print(f"    target={row['target_chapter']}, algo={row['algo_chapter']}, gap={gap_str}, rate={row['v2_rate']}%")
            print(f"    {row['title_la']} ({row['title_zh']}) | {row['theme']} | {row['style']} | {row['word_count']}词")

    # 写 CSV
    if results:
        fieldnames = ["file","dir","target_chapter","algo_chapter","gap","v2_rate",
                      "v2_oov_count","severity","title_la","title_zh","theme","style","word_count"]
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\n详细 CSV 已写入: {OUTPUT_CSV}")

    summary = {
        "total": len(results),
        "misplacements_count": len(misplacements),
        "per_dir": {d: dict(s) for d, s in stats.items()},
    }
    print("\n--- JSON_SUMMARY ---")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
