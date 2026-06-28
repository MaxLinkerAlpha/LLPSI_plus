#!/usr/bin/env python3
"""
ai_review.py v1_0_0 — 入库前对故事做 AI 质量审查（macrons / 用词 / 语法 / 古典性）。

设计哲学（v1_0_0）：
  - 完整把整篇故事喂给 AI（用户明确说不在乎 token）
  - AI 后端可配置：默认 ollama，也支持任意 shell 命令（如 curl、python 等）
  - 输出结构化 JSON（含 critical_issues / suggestions / verdict）
  - merge_yaml.py 加 --review 参数即可调用

AI 后端：
  --ai-command "ollama run llama3"   # 本地 ollama
  --ai-command "curl ..."            # 任意 HTTP API
  不传 --ai-command → 只生成 prompt 文件，提示用户手工运行

用法：
    # 1. 手工模式：只生成 prompt 文件
    python AI_reader/ai_review.py --story /path/to/story.md --chapter 8 --write-prompt

    # 2. 自动化：调用 ollama
    python AI_reader/ai_review.py --story /path/to/story.md --chapter 8 \
        --ai-command "ollama run llama3.1" --output review.json

    # 3. 喂给 merge_yaml.py 一气呵成
    cat story.md | python AI_reader/merge_yaml.py --file story.md --review
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# ============================================================
# Prompt 模板
# ============================================================

REVIEW_SYSTEM_PROMPT = """你是一位资深的拉丁语文学教师，正在审阅一篇 LLPSI（Familia Romana）扩展读物。

你的任务是**严格但不机械**地审查整篇拉丁语故事，给出 4 个维度的评分 + 详细问题清单。

## 审查维度

### 1. 长音标注（Macrons）— 极其重要
古典拉丁语的长元音必须用 macron 标注（ā/ē/ī/ō/ū/ȳ）。
- 错误示例：videt 应为 vīdet；amicus 应为 amīcus
- 检查全文，列出所有长音错误（行号 + 词 + 正确形式 + 错误形式）

### 2. 用词准确性（Vocabulary）
- 是否存在不存在的拉丁词（OCR 残留 / 拼写错 / 拼凑词）
- 是否存在不地道的英式 / 现代用法
- 是否存在明显的中世纪拉丁或教会拉丁特征（不适合 LLPSI 教学语域）

### 3. 古典性（Classical Style）
- 句式是否符合古典拉丁语规范（不是英语化拉丁）
- 时态/人称/数的搭配是否正确
- 词序是否符合拉丁语习惯（SOV 倾向）
- 介词宾格/与格搭配是否符合古典用法

### 4. Cap.{chapter} 难度匹配
- 词汇是否主要来自 LLPSI Cap.1~Cap.{chapter} 已学范围
- 语法结构是否以 Cap.{chapter} 范围内为主
- **不要为了"必须用 Cap.{chapter} 语法"而批评**——本系统采用"评估打标"策略，
  AI 可以自由使用 Cap.{chapter} 之后的高级语法，只要用法正确

## 输出格式（严格 JSON）

```json
{{
  "macrons_issues": [
    {{"word": "videt", "line": 3, "correct": "vīdet", "reason": "vīdēre 的现在时主动直陈第三人称单数"}}
  ],
  "vocabulary_issues": [
    {{"word": "xxx", "issue": "不是有效拉丁词 / 不属古典 / 拼写错", "suggestion": "替换为 yyy"}}
  ],
  "classical_issues": [
    {{"sentence": "原文...", "issue": "不自然 / 错误", "suggestion": "改为..."}}
  ],
  "chapter_fit": "on_target | above_target | below_target | mixed",
  "chapter_fit_notes": "详细说明",
  "critical_issues": [ "阻塞入库的严重问题" ],
  "suggestions": [ "非阻塞的改进建议" ],
  "verdict": "pass | needs_fixes | fail"
}}
```

## 判定标准

- **verdict = "pass"**：无长音错误（macrons_issues 空）+ 无 critical_issues
- **verdict = "needs_fixes"**：1-3 处 macrons_issues 或 1-2 个 critical_issues
- **verdict = "fail"**：≥4 处 macrons_issues 或 ≥3 个 critical_issues

## 注意

- 完整阅读整篇故事后**一次性**输出 JSON，不要分多次
- 严格基于拉丁语事实判断，不要"为了好评"放水
- 宁可多报不要漏报（macrons 错标最致命）
- 输出**只用 JSON**，不要任何额外文字
"""


REVIEW_USER_PROMPT_TEMPLATE = """## 待审查故事（Cap.{chapter} 目标难度）

```markdown
{story_body}
```

请按照系统指令中定义的 4 个维度（macrons / 用词 / 古典性 / Cap.{chapter} 匹配）逐项审查，
**严格输出 JSON**（含 macrons_issues / vocabulary_issues / classical_issues / critical_issues / verdict）。
"""


# ============================================================
# 核心逻辑
# ============================================================

def extract_story_body(story_path: Path) -> tuple:
    """从 MD 文件提取 YAML Front Matter + 拉丁语正文。

    Returns:
        (yaml_block, latin_text, full_text)
    """
    text = story_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            yaml_block = text[3:end].strip()
            latin_text = text[end+4:].strip()
            return yaml_block, latin_text, text
    return "", text, text


def build_review_prompt(chapter: int, story_body: str) -> str:
    """构造完整 review prompt（system + user）。"""
    system = REVIEW_SYSTEM_PROMPT.format(chapter=chapter)
    user = REVIEW_USER_PROMPT_TEMPLATE.format(
        chapter=chapter, story_body=story_body
    )
    return f"{system}\n\n{'-'*60}\n\n{user}"


def parse_review_output(ai_output: str) -> dict:
    """从 AI 输出中提取 JSON。

    容错：AI 经常在 JSON 前后加废话。优先找 ```json 块，否则找第一个 { 到最后一个 }。
    """
    ai_output = ai_output.strip()

    # 策略 1：找 ```json ... ``` 块
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", ai_output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # 策略 2：找第一个 { 到最后一个 }（贪婪匹配）
    start = ai_output.find("{")
    end = ai_output.rfind("}")
    if start >= 0 and end > start:
        candidate = ai_output[start:end+1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # 策略 3：失败，返回 raw
    return {
        "parse_error": True,
        "raw_output": ai_output[:5000],
        "verdict": "needs_fixes",
        "critical_issues": ["AI 输出无法解析为 JSON，请检查 prompt 或后端"],
    }


def call_ai(ai_command: str, prompt: str, timeout: int = 180) -> str:
    """调用 AI 后端（通过 shell 命令），返回 stdout。

    约定：命令的最后 stdin 接收 prompt（用 echo pipe），
          或用 {{prompt}} 占位符（更明确）。
    """
    if "{prompt}" in ai_command:
        cmd = ai_command.replace("{prompt}", prompt)
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
    else:
        # 默认行为：echo 喂 stdin
        result = subprocess.run(
            ai_command, shell=True, input=prompt,
            capture_output=True, text=True, timeout=timeout
        )

    if result.returncode != 0:
        raise RuntimeError(
            f"AI 命令失败（exit={result.returncode}）。\n"
            f"stderr: {result.stderr[:500]}"
        )
    return result.stdout


def render_review_md(review: dict, story_path: str = None) -> str:
    """把 JSON 评审结果渲染为可读 Markdown。"""
    lines = [f"## AI 审查报告\n"]
    lines.append(f"**verdict**: `{review.get('verdict', '?')}`\n")
    lines.append(f"**chapter_fit**: `{review.get('chapter_fit', '?')}`\n")
    if review.get("chapter_fit_notes"):
        lines.append(f"  {review['chapter_fit_notes']}\n")

    if review.get("macrons_issues"):
        lines.append(f"\n### 长音错误（{len(review['macrons_issues'])} 处）\n")
        for issue in review["macrons_issues"]:
            lines.append(
                f"- L{issue.get('line', '?')}: **{issue.get('word', '?')}** → "
                f"`{issue.get('correct', '?')}` — {issue.get('reason', '')}\n"
            )

    if review.get("vocabulary_issues"):
        lines.append(f"\n### 用词问题（{len(review['vocabulary_issues'])} 处）\n")
        for issue in review["vocabulary_issues"]:
            lines.append(
                f"- **{issue.get('word', '?')}**: {issue.get('issue', '')}"
                + (f" → 建议: `{issue.get('suggestion', '?')}`"
                   if issue.get("suggestion") else "")
                + "\n"
            )

    if review.get("classical_issues"):
        lines.append(f"\n### 古典性问题（{len(review['classical_issues'])} 处）\n")
        for issue in review["classical_issues"]:
            lines.append(
                f"- `{issue.get('sentence', '?')}`: {issue.get('issue', '')}"
                + (f" → 建议: `{issue.get('suggestion', '?')}`"
                   if issue.get("suggestion") else "")
                + "\n"
            )

    if review.get("critical_issues"):
        lines.append(f"\n### 阻塞性问题（{len(review['critical_issues'])} 项）\n")
        for ci in review["critical_issues"]:
            lines.append(f"- {ci}\n")

    if review.get("suggestions"):
        lines.append(f"\n### 改进建议\n")
        for s in review["suggestions"]:
            lines.append(f"- {s}\n")

    return "".join(lines)


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI 审查脚本：长音、用词、古典性、Cap.N 匹配"
    )
    parser.add_argument("--story", "-s", type=Path, required=True,
                        help="待审查的故事 MD 文件路径")
    parser.add_argument("--chapter", "-c", type=int, required=True,
                        help="目标章节（1-34）")
    parser.add_argument("--ai-command", default="",
                        help="AI 后端 shell 命令（默认空 = 只生成 prompt 文件）")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="审查 JSON 输出路径（不指定则 stdout）")
    parser.add_argument("--write-prompt", action="store_true",
                        help="把 prompt 写到 {story}.review_prompt.txt")
    parser.add_argument("--timeout", type=int, default=180,
                        help="AI 调用超时（秒）")
    args = parser.parse_args()

    if not args.story.exists():
        print(f"[ai_review] 错误：{args.story} 不存在。", file=sys.stderr)
        sys.exit(1)

    yaml_block, latin_text, full_text = extract_story_body(args.story)
    if not latin_text:
        print(f"[ai_review] 错误：{args.story} 没有正文。", file=sys.stderr)
        sys.exit(1)

    # 构造 prompt（包含完整正文）
    story_body = latin_text
    prompt = build_review_prompt(args.chapter, story_body)

    if args.write_prompt or not args.ai_command:
        prompt_path = args.story.with_suffix(args.story.suffix + ".review_prompt.txt")
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"[ai_review] Prompt 已写入：{prompt_path}")
        print(f"[ai_review] 字数：{len(prompt)} 字符 / 约 {len(prompt)//4} tokens")
        if not args.ai_command:
            print(f"[ai_review] 未指定 --ai-command，"
                  f"请手工把 prompt 喂给 AI 后端，输出保存为 JSON。")
            sys.exit(0)

    # 调用 AI
    print(f"[ai_review] 正在调用 AI: {args.ai_command[:60]}...")
    ai_output = call_ai(args.ai_command, prompt, timeout=args.timeout)
    review = parse_review_output(ai_output)

    # 输出
    if args.output:
        args.output.write_text(
            json.dumps(review, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"[ai_review] 审查 JSON 已写入：{args.output}")
    else:
        print(json.dumps(review, ensure_ascii=False, indent=2))

    # stderr 输出可读版本
    print("\n" + "="*60, file=sys.stderr)
    print(render_review_md(review, str(args.story)), file=sys.stderr)
    print("="*60, file=sys.stderr)

    # 退出码：pass=0, needs_fixes=1, fail=2
    verdict = review.get("verdict", "needs_fixes")
    sys.exit({"pass": 0, "needs_fixes": 1, "fail": 2}.get(verdict, 1))


if __name__ == "__main__":
    main()
