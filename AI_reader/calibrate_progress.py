#!/usr/bin/env python3
"""校准 progress.json — 扫描磁盘所有故事，重建准确的进度数据。

用法: python3 calibrate_progress.py
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).parent / "realitates"
PROGRESS_FILE = Path(__file__).parent / "progress.json"


def extract_yaml_front_matter(filepath: Path) -> dict:
    """从 .md 文件中提取 YAML front matter。"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配 --- ... --- 之间的内容
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print(f"  [WARN] 无 YAML front matter: {filepath}")
        return {}

    yaml_text = match.group(1)
    result = {}
    for line in yaml_text.strip().split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value
    return result


def scan_all_stories() -> dict:
    """扫描所有 Cap 目录，返回 {chapter_num: {count, dimensions}}。"""
    chapters = {}

    if not REALITATES_DIR.exists():
        print(f"[ERROR] 目录不存在: {REALITATES_DIR}")
        sys.exit(1)

    for cap_dir in sorted(REALITATES_DIR.iterdir()):
        if not cap_dir.is_dir():
            continue
        match = re.match(r"Cap(\d+)", cap_dir.name)
        if not match:
            continue
        chapter_num = int(match.group(1))

        md_files = sorted(cap_dir.glob("*.md"))
        if not md_files:
            chapters[chapter_num] = {
                "done": 0,
                "themes": [],
                "styles": [],
                "genres": [],
                "characters": [],
                "narratives": [],
            }
            continue

        themes = []
        styles = []
        genres = []
        characters = []
        narratives = []

        for md_file in md_files:
            yaml_data = extract_yaml_front_matter(md_file)

            theme = yaml_data.get("theme", "")
            style = yaml_data.get("style", "")
            genre = yaml_data.get("genre", "")
            char_type = yaml_data.get("character_type", "")
            narrative = yaml_data.get("narrative_mode", "")

            if theme:
                themes.append(theme)
            if style:
                styles.append(style)
            if genre:
                genres.append(genre)
            if char_type:
                characters.append(char_type)
            if narrative:
                narratives.append(narrative)

        chapters[chapter_num] = {
            "done": len(md_files),
            "themes": themes,
            "styles": styles,
            "genres": genres,
            "characters": characters,
            "narratives": narratives,
        }

    return chapters


def build_progress_json(chapters_data: dict) -> dict:
    """根据扫描结果构建新的 progress.json 内容。"""
    # 读旧 progress.json 以保留 project/started 等元信息
    old_progress = {}
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            old_progress = json.load(f)

    # 构建新的 chapters 数据
    new_chapters = {}
    for n in range(1, 21):
        ch_key = str(n)
        if n in chapters_data:
            cd = chapters_data[n]
            new_chapters[ch_key] = {
                "done": cd["done"],
                "target": 10,
                "need": max(0, 10 - cd["done"]),
                "strategy": "micro" if n <= 6 else "standard",
                "used_dimensions": {
                    "themes": cd["themes"],
                    "styles": cd["styles"],
                    "genres": cd["genres"],
                    "characters": cd["characters"],
                    "narratives": cd["narratives"],
                },
            }
        else:
            new_chapters[ch_key] = {
                "done": 0,
                "target": 10,
                "need": 10,
                "strategy": "micro" if n <= 6 else "standard",
                "used_dimensions": {
                    "themes": [],
                    "styles": [],
                    "genres": [],
                    "characters": [],
                    "narratives": [],
                },
            }

    progress = {
        "project": old_progress.get("project", "200_stories_Cap1_20"),
        "version": "3.0",
        "started": old_progress.get("started", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "current_phase": 1,
        "chapters": new_chapters,
        "batches": [],  # 清空重建，旧批次记录不完整
    }

    return progress


def create_missing_dirs():
    """创建缺失的 Cap.1-6 目录。"""
    for n in range(1, 7):
        cap_dir = REALITATES_DIR / f"Cap{n}"
        if not cap_dir.exists():
            cap_dir.mkdir(parents=True, exist_ok=True)
            print(f"  [CREATE] {cap_dir}")


def main():
    print("=" * 60)
    print("Phase 0: 校准 progress.json")
    print("=" * 60)

    # 1. 扫描
    print("\n[1/4] 扫描所有故事文件...")
    chapters_data = scan_all_stories()

    total_stories = sum(cd["done"] for cd in chapters_data.values())
    total_chapters = len(chapters_data)
    print(f"  找到 {total_stories} 篇故事，分布在 {total_chapters} 个章节中")

    # 打印每章详情
    print("\n  章节详情:")
    for ch_num in sorted(chapters_data.keys()):
        cd = chapters_data[ch_num]
        print(f"    Cap.{ch_num}: {cd['done']} 篇")

    # 2. 创建缺失目录
    print("\n[2/4] 创建缺失目录...")
    create_missing_dirs()

    # 3. 构建 progress.json
    print("\n[3/4] 构建 progress.json...")
    progress = build_progress_json(chapters_data)

    # 4. 写入
    print("\n[4/4] 写入 progress.json...")
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    print(f"\n  完成! progress.json 已更新:")
    print(f"    版本: {progress['version']}")
    print(f"    更新时间: {progress['last_updated']}")
    print(f"    当前阶段: Phase {progress['current_phase']}")

    # 汇总
    need_total = sum(ch["need"] for ch in progress["chapters"].values())
    print(f"    还需生成: {need_total} 篇")
    print("=" * 60)


if __name__ == "__main__":
    main()