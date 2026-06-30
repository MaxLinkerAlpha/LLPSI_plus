#!/usr/bin/env bash
# archive_plan.sh — 一键归档任务型计划书到 archive/
# 用法: ./archive_plan.sh [文件名1] [文件名2] ...
#       ./archive_plan.sh --recent 7   # 归档最近 7 天修改的任务型文档
#
# 归档规则: 匹配 cleanup_*.md, continue_*.md, *_plan.md, [DONE]*.md, [OLD]*.md
# 保留规则: 核心规划书 (437_short_rewrite_plan.md 等) 不在自动归档范围
#          历史经验报告 (cap1_6_special_report.md) 不归档

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$SCRIPT_DIR/../documents"
ARCHIVE_DIR="$DOCS_DIR/archive"

mkdir -p "$ARCHIVE_DIR"

ARCHIVE_PATTERN='^(cleanup_|continue_|cap[0-9]+_[0-9]+_rewrite|\[DONE\]|\[OLD\]).*\.md$'
PROTECTED="437_short_rewrite_plan.md|cap1_6_special_report.md|Lesson.md"

archive_file() {
  local f="$1"
  local name
  name=$(basename "$f")
  if [[ "$name" =~ $PROTECTED ]]; then
    echo "  [跳过-核心] $name"
    return
  fi
  if [[ "$name" =~ $ARCHIVE_PATTERN ]]; then
    local date
    date=$(date +%Y%m%d)
    local target="$ARCHIVE_DIR/${date}_${name}"
    mv "$f" "$target"
    echo "  [已归档] $name → archive/$(basename "$target")"
  else
    echo "  [跳过-不符规则] $name"
  fi
}

if [[ "$1" == "--recent" ]]; then
  days="${2:-7}"
  echo "归档最近 ${days} 天修改的任务型文档..."
  find "$DOCS_DIR" -maxdepth 1 -name "*.md" -mtime -"$days" -type f -print0 | \
    while IFS= read -r -d '' f; do
      archive_file "$f"
    done
elif [[ $# -eq 0 ]]; then
  echo "归档所有匹配规则的任务型文档..."
  find "$DOCS_DIR" -maxdepth 1 -name "*.md" -type f -print0 | \
    while IFS= read -r -d '' f; do
      archive_file "$f"
    done
else
  echo "归档指定文件..."
  for f in "$@"; do
    archive_file "$DOCS_DIR/$f"
  done
fi

echo "完成。当前 archive 目录内容:"
ls -la "$ARCHIVE_DIR" 2>/dev/null || echo "  (空)"
