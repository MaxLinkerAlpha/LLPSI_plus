#!/usr/bin/env python3
"""
generate_prompt.py v1_6_0 — 一行命令生成AI提示词（增强版 · 方案C词表 + 评估打标 grammar）。

读取 STRATEGY.md 模板，替换 {{CHAPTER}} 占位符，输出完整的AI提示词。

v1_6_0 变更（相对 v1_5_0）：
  - 路径重命名：realites → realitates（修正拉丁语拼写错误）

v1_5_0 变更（相对 v1_4_0）：
  - load_vocab_section() 优先读取 cap{N}_vocab_clean.json（vocab_clean.py 清洗版），
    fallback 到原版 cap{N}_vocab.json
  - load_grammar_section() 措辞改「必须用 3 项」→「建议自由使用 + 评估打标」，
    配合 evaluate_v2.py 的 grammar_features_used 自动检测
  - 采纳第一性原理：释放 AI 创造力，事后打标签比硬约束更自然

v1_4_0 变更（相对 v1_3_0）：
  - 新增 --vocab / -V 参数：从 vocab_by_chapter/cap{N}_vocab.json 注入本章允许词汇到 prompt 末尾
  - 新增函数 load_vocab_section()、format_vocab_block()
  - 方案C核心组件：以数据约束替代算法事后检测，从源头控制难度

v1_2_0 变更（相对 v1_1_0）：
  - 新增 --history / -H 参数：自动读 realitates.json，在 prompt 末尾追加「避免使用以下组合」
  - 新增 --exclude-dim 参数：手动指定要排除的维度组合（多个逗号分隔）
  - 新增 --show-history / -s 参数：仅打印历史已用维度清单，不输出 prompt
  - 函数 load_history()、format_exclusion() 暴露为可复用

用法：
    # 基本用法（向后兼容）
    python AI_reader/generate_prompt.py --chapter 10

    # 启用历史追踪（推荐）：避免重复已用组合
    python AI_reader/generate_prompt.py --chapter 10 --history

    # 查看当前章节已用维度
    python AI_reader/generate_prompt.py --chapter 10 --show-history

    # 手动排除某些组合
    python AI_reader/generate_prompt.py --chapter 10 \
        --exclude-dim "theme=09 勇气, style=精炼, genre=A LLPSI宇宙"

    # 输出到文件
    python AI_reader/generate_prompt.py --chapter 10 --history --output /tmp/p.txt

输出：完整AI提示词文本（STRATEGY.md中{{CHAPTER}}已替换为目标章节）。
      若启用 --history，末尾会追加「避免使用以下组合」段。
"""

import argparse
import json
import sys
from pathlib import Path


# ============================================================
# 常量
# ============================================================

HISTORY_DIMS = ("theme", "style", "genre", "character_type", "narrative_mode")


# ============================================================
# 模板解析
# ============================================================

def resolve_prompt(chapter: int, template_path: Path) -> str:
    """读取模板文件，替换 {{CHAPTER}} 占位符，返回完整提示词。

    Args:
        chapter: 目标 LLPSI 章节号（1-34）
        template_path: STRATEGY.md 模板文件路径

    Returns:
        替换后的完整提示词文本

    Raises:
        ValueError: 章节号超出有效范围
        FileNotFoundError: 模板文件不存在
    """
    if not 1 <= chapter <= 56:
        raise ValueError(
            f"章节号必须在 1-56 之间，当前输入: {chapter}。"
        )

    if not template_path.exists():
        raise FileNotFoundError(
            f"模板文件不存在: {template_path}\n"
            f"请确保 STRATEGY.md 与 generate_prompt.py 在同一目录，"
            f"或通过 --template 指定路径。"
        )

    raw = template_path.read_text(encoding="utf-8")
    return raw.replace("{{CHAPTER}}", str(chapter))


# ============================================================
# 历史追踪
# ============================================================

def load_history(index_path: Path) -> list:
    """从 realitates.json 加载已生成故事的索引。

    Returns:
        索引列表（可能为空）。读取失败时返回空列表 + stderr 警告。
    """
    if not index_path.exists():
        return []
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        print(f"[generate_prompt] 警告：{index_path.name} 顶层不是数组，忽略。",
              file=sys.stderr)
        return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"[generate_prompt] 警告：{index_path.name} 读取失败（{e}），忽略。",
              file=sys.stderr)
        return []


def get_used_dimensions(history: list, chapter: int, index_path: Path = None) -> dict:
    """从 history 中提取指定章节已使用的维度值。

    Args:
        history: realitates.json 加载的索引列表
        chapter: 目标章节
        index_path: realitates.json 路径（用于解析相对路径）

    Returns:
        {dim_name: [used_value1, used_value2, ...]} 字典，仅包含有数据的维度。

    Note:
        realitates.json 索引仅含 path/chapter/title_zh，不含主题/风格/题材。
        因此本函数对每条记录尝试从对应 MD 文件读取 Front Matter。
        找不到 MD 或 Front Matter 缺字段时跳过该条。
    """
    used: dict = {d: [] for d in HISTORY_DIMS}
    for entry in history:
        if entry.get("chapter") != chapter:
            continue
        # 尝试从 MD Front Matter 读字段
        rel_path = entry.get("path", "")
        if not rel_path:
            continue
        md_path = index_path_to_md(rel_path, index_path=index_path)
        if not md_path or not md_path.exists():
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError:
            continue
        # 提取 Front Matter 内的 key: value
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        fm = text[3:end]
        for line in fm.splitlines():
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key in HISTORY_DIMS and val and val not in used[key]:
                used[key].append(val)
    return {k: v for k, v in used.items() if v}


def index_path_to_md(rel_path: str, index_path: Path = None) -> Path:
    """将 realitates.json 里的相对路径解析为绝对 MD 文件路径。"""
    p = Path(rel_path)
    if p.is_absolute():
        return p
    # 默认：相对 AI_reader/ 目录
    if index_path:
        return (index_path.parent / p).resolve()
    return p.resolve()


def format_exclusion(used: dict, manual_exclude: list) -> str:
    """生成「避免使用以下组合」指令文本，追加到 prompt 末尾。

    Args:
        used: get_used_dimensions() 返回的 dict
        manual_exclude: 手动排除的维度列表，格式 ["dim=value", "dim=value", ...]

    Returns:
        完整的指令段（多行文本）。如果两个来源都为空，返回空字符串。
    """
    lines = ["\n\n---\n", "## 多样性约束（来自历史追踪）\n"]
    has_content = False

    if used:
        lines.append("本章已使用过以下维度组合，请避免重复：\n")
        for dim, values in used.items():
            lines.append(f"- **{dim}**：{', '.join(values)}\n")
        has_content = True

    if manual_exclude:
        lines.append("\n本轮手动排除的维度：\n")
        for spec in manual_exclude:
            lines.append(f"- {spec}\n")
        has_content = True

    if not has_content:
        return ""

    lines.append(
        "\n> 创作时**优先从每个维度的其他选项中选 1 个**，与已用值错开。"
        "若必须使用某个已用值（如章节题材太特殊），则须从其他维度做出明显差异化。\n"
    )
    return "".join(lines)


# ============================================================
# 方案C：分章节词表注入
# ============================================================

# vocab JSON 存储目录（相对于 difficulty_algorithm/）
VOCAB_DIR_NAME = "vocab_by_chapter"


def find_vocab_dir(script_dir: Path) -> Path:
    """定位 vocab_by_chapter/ 目录。"""
    candidate = script_dir.parent / "difficulty_algorithm" / VOCAB_DIR_NAME
    if candidate.exists():
        return candidate
    cwd_candidate = Path.cwd() / "difficulty_algorithm" / VOCAB_DIR_NAME
    if cwd_candidate.exists():
        return cwd_candidate
    raise FileNotFoundError(
        f"找不到 {VOCAB_DIR_NAME}/ 目录。"
        f"尝试了：{candidate}、{cwd_candidate}"
    )


def load_vocab_section(chapter: int, vocab_dir: Path) -> str:
    """加载 Cap.1 至 Cap.N 的累积词表，拼接为 prompt 追加段。

    优先读取 cap{N}_vocab_clean.json（vocab_clean.py 输出），
    找不到时 fallback 到 cap{N}_vocab.json。这样保证 OCR 残片已被剔除。

    Args:
        chapter: 目标章节（1-34）
        vocab_dir: vocab_by_chapter/ 目录路径

    Returns:
        完整的「本章节允许词汇」指令文本。词表按字母序排列。
    """
    import json
    vocab = []
    # 累积加载：Cap.8 需要 cap1 到 cap8 的并集
    for c in range(1, chapter + 1):
        # 优先 _clean，回退原版
        for suffix in ("_vocab_clean.json", "_vocab.json"):
            fpath = vocab_dir / f"cap{c}{suffix}"
            if fpath.exists():
                with open(fpath, "r", encoding="utf-8") as f:
                    lemma_list = json.load(f)
                vocab.extend(lemma_list)
                break  # 找到就停
    # 去重 + 排序
    vocab = sorted(set(vocab))
    return format_vocab_block(chapter, vocab)


def format_vocab_block(chapter: int, vocab: list) -> str:
    """生成词表注入段的 Markdown 文本。

    Args:
        chapter: 目标章节
        vocab: 去重排序后的词形列表

    Returns:
        追加到 prompt 末尾的词表段。
    """
    if not vocab:
        return ""

    lines = [
        "\n\n---\n",
        "## 方案C — 本章节允许词汇（Cap.1 ~ Cap.{} 累计词表）\n".format(chapter),
        "",
        "以下为 LLPSI Cap.1 至 Cap.{} 已学词汇的词形列表（{} 个）。".format(chapter, len(vocab)),
        "创作时严格约束：",
        "",
        "- **优先使用表内词汇** — 至少 85% 的独特词形应出自下表",
        "- **超纲词 ≤15%** — 每个超纲词必须能从上下文推断含义（边注推理原则）",
        "- **不堆砌、不凑数** — 用已有词汇自然表达，不为追求「高级感」引入生词",
        "",
        "```",
    ]
    # 每行 8 个词形，便于 AI 扫描
    for i in range(0, len(vocab), 8):
        lines.append(", ".join(vocab[i:i + 8]))
    lines.append("```")
    return "\n".join(lines)


# ============================================================
# 语法重点注入（--grammar）
# ============================================================

GRAMMAR_MAP_NAME = "grammar_chapter_map.json"


def find_grammar_map(script_dir: Path) -> Path:
    """定位 grammar_chapter_map.json 路径。"""
    candidate = script_dir.parent / "difficulty_algorithm" / GRAMMAR_MAP_NAME
    if candidate.exists():
        return candidate
    cwd_candidate = Path.cwd() / "difficulty_algorithm" / GRAMMAR_MAP_NAME
    if cwd_candidate.exists():
        return cwd_candidate
    raise FileNotFoundError(
        f"找不到 {GRAMMAR_MAP_NAME}。尝试了：{candidate}、{cwd_candidate}"
    )


def load_grammar_section(chapter: int, script_dir: Path) -> str:
    """从 grammar_chapter_map.json 读本章语法点，生成注入段。"""
    map_path = find_grammar_map(script_dir)
    with open(map_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    key = str(chapter)
    items = data.get(key)
    if not items:
        return ""

    lines = [
        "\n\n---\n",
        f"## 本章可参考的语法结构（Cap.{chapter}）\n",
        "以下是 LLPSI Cap.{} 系统教学过的语法点。**仅作参考**，不强制使用：\n".format(chapter),
    ]
    for it in items:
        la = it.get("la", "")
        zh = it.get("zh", "")
        if la and zh:
            lines.append(f"- **{la}**（{zh}）")
        elif la:
            lines.append(f"- {la}")
    lines.append(
        "\n> **采用「评估打标」而非「约束生成」策略**。\n"
        "> 你可以**自由**选用任何 Cap.{} 及之后章节的语法结构来讲述故事，"
        "不必强行塞入本章语法点。\n"
        "> 写完后算法会**自动检测**并给故事打上 `grammar_features_used` 标签，"
        "如实记录你实际用了哪些语法。\n"
        "> 这种方式比硬性『必须用 3 项』更自然，"
        "故事的语法选择由内容驱动，不由硬性规定。\n".format(chapter)
    )
    return "\n".join(lines) + "\n"


# ============================================================
# 主入口
# ============================================================

def parse_exclude_dim(specs: list) -> list:
    """解析 --exclude-dim 参数。specs 形如 ['theme=09 勇气', 'style=精炼']。

    Returns:
        保留的 spec 列表（去空白、去空值）。
    """
    return [s.strip() for s in specs if s and s.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="生成 LLPSI 扩展读物 AI 提示词（替换 {{CHAPTER}} 占位符，可选追加历史排除）。"
    )
    parser.add_argument(
        "--chapter", "-c",
        type=int, required=True, metavar="N",
        help="目标 LLPSI 章节号（1-34）"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path, default=None,
        help="输出文件路径。不指定则输出到 stdout。"
    )
    parser.add_argument(
        "--template", "-t",
        type=Path,
        default=Path(__file__).resolve().parent / "STRATEGY.md",
        help="模板路径（默认：脚本同目录下的 STRATEGY.md）"
    )
    parser.add_argument(
        "--history", "-H",
        action="store_true",
        help="启用历史追踪：自动从 realitates.json 读已用维度，追加到 prompt 末尾"
    )
    parser.add_argument(
        "--exclude-dim",
        type=str, default="",
        help="手动排除的维度组合，逗号分隔，如 'theme=09 勇气,style=精炼'"
    )
    parser.add_argument(
        "--show-history", "-s",
        action="store_true",
        help="仅打印当前章节已用维度清单到 stdout，然后退出（不输出 prompt）"
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=Path(__file__).resolve().parent / "realitates.json",
        help="realitates.json 路径（默认：脚本同目录下的 realitates.json）"
    )
    parser.add_argument(
        "--vocab", "-V",
        action="store_true",
        help="启用方案C词表注入：从 vocab_by_cap/ 加载 Cap.1-N 累计词表，追加到 prompt 末尾"
    )
    parser.add_argument(
        "--grammar", "-G",
        action="store_true",
        help="启用语法重点注入：从 grammar_chapter_map.json 读本章语法点，追加到 prompt 末尾"
    )
    args = parser.parse_args()

    # 1. 解析提示词
    prompt = resolve_prompt(args.chapter, args.template)

    # 1.5 方案C：词表注入（在历史排除之前，作为标准 prompt 的一部分）
    # 注意：词表可能很大（Cap.34 有 7443 词），如果同时启用 --vocab 和 --output，prompt 会很长
    script_dir = Path(__file__).resolve().parent
    if args.vocab:
        try:
            vocab_dir = find_vocab_dir(script_dir)
            vocab_section = load_vocab_section(args.chapter, vocab_dir)
            if vocab_section:
                prompt = prompt + vocab_section
                print(
                    f"[generate_prompt] 方案C词表已注入：Cap.{args.chapter} 累计词表 "
                    f"({vocab_section.count(chr(10))} 行)。",
                    file=sys.stderr
                )
        except FileNotFoundError as e:
            print(f"[generate_prompt] 警告：词表加载失败（{e}），跳过方案C。",
                  file=sys.stderr)
        except Exception as e:
            print(f"[generate_prompt] 警告：词表注入异常（{e}），跳过方案C。",
                  file=sys.stderr)

    # 1.6 语法重点注入（--grammar 启用）
    if args.grammar:
        try:
            grammar_section = load_grammar_section(args.chapter, script_dir)
            if grammar_section:
                prompt = prompt + grammar_section
                print(
                    f"[generate_prompt] 语法重点已注入：Cap.{args.chapter} "
                    f"({grammar_section.count(chr(10))} 行)。",
                    file=sys.stderr
                )
        except FileNotFoundError as e:
            print(f"[generate_prompt] 警告：语法映射加载失败（{e}），跳过 --grammar。",
                  file=sys.stderr)
        except Exception as e:
            print(f"[generate_prompt] 警告：语法注入异常（{e}），跳过 --grammar。",
                  file=sys.stderr)

    # 2. 加载历史
    manual_exclude = parse_exclude_dim(
        [s for s in args.exclude_dim.split(",") if s.strip()]
    ) if args.exclude_dim else []

    if args.show_history:
        history = load_history(args.index)
        used = get_used_dimensions(history, args.chapter, args.index)
        if not used and not manual_exclude:
            print(f"Cap.{args.chapter} 暂无历史记录。")
        else:
            print(f"Cap.{args.chapter} 已用维度：")
            for dim, values in used.items():
                print(f"  {dim}: {', '.join(values)}")
            if manual_exclude:
                print(f"\n本轮手动排除：")
                for spec in manual_exclude:
                    print(f"  {spec}")
        return

    if args.history or manual_exclude:
        history = load_history(args.index)
        used = get_used_dimensions(history, args.chapter, args.index)
        exclusion = format_exclusion(used, manual_exclude)
        if exclusion:
            prompt = prompt + exclusion
            if args.history:
                print(
                    f"[generate_prompt] 已追踪历史：Cap.{args.chapter} "
                    f"已用 {sum(len(v) for v in used.values())} 个维度值。",
                    file=sys.stderr
                )

    # 3. 输出
    if args.output:
        args.output.write_text(prompt, encoding="utf-8")
        print(
            f"[generate_prompt] 提示词已写入: {args.output}  "
            f"(章节=Cap.{args.chapter}{', 含历史追踪' if (args.history or manual_exclude) else ''})",
            file=sys.stderr
        )
    else:
        sys.stdout.write(prompt)


if __name__ == "__main__":
    main()
