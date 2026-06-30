#!/usr/bin/env python3
"""
format_story.py v1_0_0 — 段落格式化（最小修改版）

只插入空白（换行/空行），不动任何文本内容。

规则：
  1. front matter `---` 后插入 1 个空行（统一格式）
  2. 句号 . + 空格 → 换行（每句一行）
  3. 检测到对话（"X: '...'" / "X: '...'."）时，前面加 1 个空行
  4. 检测到场景转换词（Nocte. / Mane. / Tum. / Deinde. / Subito. / Posteā. / Tandem. / Nunc. / Interim. / Sed.）开头时，前面加 1 个空行
  5. 文件末尾加 1 个换行
  6. 不合并已有的空行（保留现有分段）

用法：
  python format_story.py --dry-run            # 预览
  python format_story.py --file <path>         # 处理单个文件
  python format_story.py --files f1 f2 ...     # 处理多个文件
  python format_story.py --all                 # 处理全部 375 个
"""

import os, re, sys, argparse
from pathlib import Path

REALITATES_DIR = Path(__file__).parent / "realitates"

# 场景/时间转换词（句首大写）
SCENE_MARKERS = [
    "Nocte.", "Mane.", "Vespere.", "Subito.", "Tum.", "Deinde.",
    "Posteā.", "Postea.", "Tandem.", "Interim.", "Intereā.",
    "Nunc.", "Prīmō.", "Primo.", "Denuo.", "Iterum.",
    "Postrīdiē.", "Postridie.",
    "Hodiē.", "Hodie.",
    "Crās.", "Cras.",
    "Nondum.",
    "Sēd.",  # 实际拼写
]

# 对话模式: X: "..." 或 X: '...'
DIALOGUE_PATTERN = re.compile(
    r'([.!?…]["\u201c\u201d\u2018\u2019]?\s*)([A-ZĀĒĪŌŪȲ][a-zāēīōūȳ]+):\s*["\u201c\u201d]'
)


def split_front_matter(content: str) -> tuple[str, str, str]:
    """分离 front matter 和正文。返回 (pre, front_matter, body)。"""
    if not content.startswith("---"):
        return "", "", content

    # 找到第二个 ---
    end_match = re.search(r"^---\s*$", content[3:], re.MULTILINE)
    if not end_match:
        return "", "", content

    front_matter = content[3:3 + end_match.start()]
    body = content[3 + end_match.end():]
    return "", front_matter, body


def format_body(body: str) -> str:
    """对正文做最小分段。前提：调用方已确认 body 无空行。"""
    # 1. 句号后换行：处理 ". " → ".\n"（句号+空格+大写起头）
    body = re.sub(r'\.\s+(?=[A-ZĀĒĪŌŪȲ])', '.\n', body)

    # 2. 问号/感叹号 + 引号后换行（处理对话边界）
    body = re.sub(r'([!?])\s+(?=[A-ZĀĒĪŌŪȲ])', r'\1\n', body)
    body = re.sub(r'([!?][\u201c\u201d"\u2018\u2019])\s+(?=[A-ZĀĒĪŌŪȲ])', r'\1\n', body)

    # 3. 场景转换词前面加空行（避免与上面冲突：用行首匹配）
    # 将形如 "\nNocte. ..." 转为 "\n\nNocte. ..."
    for marker in SCENE_MARKERS:
        # 只在行首出现时加空行（不在句中）
        body = re.sub(
            rf'(^|\n)({re.escape(marker)}\s)',
            rf'\1\n\2',
            body
        )

    # 4. 对话前面加空行
    # 匹配行首是 "X: '..."  的模式
    # 注意：先 split 成行再处理
    lines = body.split('\n')
    out = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i > 0 and stripped and re.match(r'^[A-ZĀĒĪŌŪȲ][a-zāēīōūȳ]+:\s*["\u201c]', stripped):
            # 这一行是对话，且上一行不是空行
            if out and out[-1].strip() != '':
                out.append('')
        out.append(line)
    body = '\n'.join(out)

    # 5. 清理连续 3+ 个空行 → 最多 2 个
    body = re.sub(r'\n{3,}', '\n\n', body)

    return body


def format_file(filepath: Path, dry_run: bool = False) -> dict:
    """处理单个文件，返回变更统计。

    严格规则：已有分段的文件（正文含 \\n\\n）完全不动。
    只处理完全无空行的文件。
    """
    original = filepath.read_text(encoding="utf-8")
    pre, front, body = split_front_matter(original)

    # 解析失败，跳过
    if not front and not body and not original.startswith("---"):
        return {"file": str(filepath), "changed": False, "orig_lines": 0, "new_lines": 0, "added_lines": 0}

    # 关键：已有空行的文件完全不动
    # 忽略 body 开头的连续换行（这些是 front matter 后的空行，不是正文段落）
    body_stripped_lead = body.lstrip("\n")
    if "\n\n" in body_stripped_lead:
        return {"file": str(filepath.relative_to(filepath.parents[1])), "changed": False,
                "orig_lines": original.count("\n"), "new_lines": original.count("\n"), "added_lines": 0}

    # 只有无空行文件才走后面的处理
    new_body = format_body(body)

    # 重新组装
    stripped_body = new_body.lstrip("\n")
    if front or body:
        new_content = "---" + front + "---\n\n" + stripped_body
    else:
        new_content = new_body

    # 文件末尾保证换行
    if not new_content.endswith("\n"):
        new_content += "\n"

    orig_lines = original.count("\n")
    new_lines = new_content.count("\n")
    orig_len = len(original)
    new_len = len(new_content)

    stats = {
        "file": str(filepath.relative_to(filepath.parents[1])),
        "changed": original != new_content,
        "orig_lines": orig_lines,
        "new_lines": new_lines,
        "added_lines": new_lines - orig_lines,
    }

    if not dry_run and original != new_content:
        filepath.write_text(new_content, encoding="utf-8")

    return stats


def main():
    parser = argparse.ArgumentParser(description="为拉丁语故事做最小段落格式化（不改正文内容）")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    parser.add_argument("--file", type=str, help="处理单个文件")
    parser.add_argument("--files", nargs="+", help="处理多个文件")
    parser.add_argument("--all", action="store_true", help="处理全部 .md 文件")
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    elif args.files:
        files = [Path(f) for f in args.files]
    elif args.all:
        files = list(REALITATES_DIR.rglob("*.md"))
    else:
        print("请指定 --file/--files/--all")
        return

    files = sorted(files)
    total = len(files)
    changed = 0
    total_added = 0

    for i, fp in enumerate(files, 1):
        if not fp.exists():
            print(f"[{i}/{total}] [跳过] 不存在: {fp}")
            continue
        stats = format_file(fp, args.dry_run)
        if stats["changed"]:
            changed += 1
            total_added += stats["added_lines"]
            marker = "[预览]" if args.dry_run else "[完成]"
            print(f"[{i}/{total}] {marker} {stats['file']}  +{stats['added_lines']} 行")

    print()
    print("=" * 60)
    suffix = "（预览）" if args.dry_run else "（已写入）"
    print(f"{suffix}: 处理 {total} 个文件，{changed} 个有变化，共增加 {total_added} 行")
    print("=" * 60)


if __name__ == "__main__":
    main()
