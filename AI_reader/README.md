# AI_reader — LLPSI 拉丁语扩展读物 AI 生成与管线

> 版本：v3_0_0 · 2026-06-30
> 算法引擎：difficulty_algorithm/ v3_0_0（预计算33K词形表 + simplemma兜底）
> 父项目：LLPSI_plus

## 这是什么

AI_reader 是 LLPSI（Lingua Latina Per Se Illustrata）拉丁语教科书的 AI 扩展读物系统。
为 LLPSI 每一章生成难度匹配、风格多样的拉丁语原创故事。

## 核心目标

- 让学习者在每章主课之后，能读到 1-5 篇同章节难度的扩展读物
- 通过故事巩固已学词汇、复现已学语法
- 通过永恒主题（85条哲学母题）让拉丁语成为思考世界的工具

## 一行命令入口

```bash
# 1. 生成 AI 提示词（替换 {{CHAPTER}}；可加 --vocab 注入词表，--history 避开已用维度）
python AI_reader/generate_prompt.py --chapter 10 --vocab --history

# 2. AI 输出后，校验（可选） + 合并评估并写入 MD 文件
python AI_reader/merge_yaml.py validate -f <ai_output.txt>   # 仅校验
python AI_reader/merge_yaml.py -f <ai_output.txt>            # 合并+写入
```

## 方案C：生成冗余 + 自动筛选

**适用场景**：单次生成难以精准命中目标章节（如要求 Cap.8 但实际生成在 Cap.11-24）。

**做法**：
1. 一次生成 N 篇（推荐 N=5）
2. `merge_yaml.py` 自动评估每篇真实难度章节
3. 每篇自动归入 `realitates/Cap{X}/`（X 由算法决定）
4. 人工从同章节多篇中择优保留（删除其余）

**示例**（Cap.8 目标，一次生成 5 篇）：

| 生成序号 | 实际章节 | 文件 | 人工决策 |
|---------|---------|------|---------|
| 1 | Cap.8 | realitates/Cap8/.../001.md | ✅ 保留 |
| 2 | Cap.11 | realitates/Cap11/.../007.md | ✅ 保留（也是好故事）|
| 3 | Cap.13 | realitates/Cap13/.../005.md | ❌ 删除（Cap.13 已有 2 篇）|
| 4 | Cap.17 | realitates/Cap17/.../008.md | ✅ 保留 |
| 5 | Cap.24 | realitates/Cap24/.../004.md | ❌ 删除（Cap.24 已 1 篇，且过难）|

**优点**：不动 prompt/算法/映射表，**靠冗余换取精准性**。
**前提**：OOV 日志自动累积（`oov_corrections.jsonl`），供后续方案D（映射表补全）使用。

## 文件清单

| 文件 | 用途 |
|------|------|
| `STRATEGY.md` v3_0_0 | **核心策略文档**，既是人类参考也是 AI 操作提示词。包含：5条硬约束+7条软约束、6张选择表（85主题/14风格/12题材/7主角/5篇幅+叙事模式）、参考手册、附录 |
| `generate_prompt.py` v1_3_0 | 注入章节号 + 方案C词表注入（`--vocab`）→ 输出完整 AI 提示词；支持 `--history` 自动追踪已用维度 |
| `merge_yaml.py` v2_15_0 | 解析 AI 输出 → 调用难度评估 → 输出 MD Front Matter → 维护 realitates.json；支持 `validate` 子命令预校验 + 多篇批量 + target_chapter 自动校准 + **篇幅自动纠正（基于实际词数，不信任AI声明）** + OOV 日志（自动分析已暂停，靠人工触发） |
| `difficulty_algorithm/evaluate_v2.py` v2_3_0 | 难度评估（v2算法已剥离长音再lemmatize） |
| `difficulty_algorithm/auto_supplement_map.py` v1_0_0 | OOV 增量分析（手动触发）：读 oov_corrections.jsonl，生成补全建议到 supplement_suggestions.jsonl（不直接修改映射表） |
| `logic.md` | 概念引擎的深层展开，供人类参考或选择引用 |
| `realitates/` | 已生成的故事（MD 格式，Front Matter + 拉丁语正文），按难度分文件夹 realitates/Cap{N}/ |
| `realitates.json` | 故事索引（自动维护，供 HTML 筛选使用） |
| `oov_corrections.jsonl` | 每次入库自动追加 OOV 词（方案D 数据闭环用） |
| `supplement_suggestions.jsonl` | OOV 增量分析产出（供人工审核，不直接修改映射表） |
| `_archived/` | 已归档的旧文件（PROMPT.md 等） |
| `GENERATION_QUEUE.md` v1_0_0 | **篇幅缺口填补清单**：当前每章故事分布 + 待生成缺口 + 执行流程。本文档即进度追踪器（逐篇 ✅） |

## 相关项目

- `../difficulty_algorithm/` — 难度评估引擎（`evaluate_v2.py`）+ 语法映射（`extract_grammar.py`）
- `../OCR/LLPSI_core/` — LLPSI 教材原文 OCR 文本（已带长音）
- `../LLPSI_Insights.html` — 最终读者面向的阅读浏览界面

## 完整管线（4 阶段）

```
1. AI 生成阶段
   └─ generate_prompt.py --chapter N → AI 读取 → 输出 YAML头+拉丁语正文

2. 合并与评估阶段
   └─ merge_yaml.py -f <output> → 解析 → evaluate_v2.py v3 评估
      → 预计算33K词形表 O(1)查表 → 未命中才调 simplemma 兜底（减少86%调用）
      → 输出 realitates/Cap{N}/Cap{N}_{title_slug}_{length_la}_{NNN}.md → 维护 realitates.json

3. 语法映射辅助（按需）
   └─ 一次性：difficulty_algorithm/extract_grammar.py
      → 输出 grammar_chapter_map.json
   └─ 提示词注入：generate_prompt.py --chapter N --grammar

4. 浏览与筛选
   └─ LLPSI_Insights.html 加载 realitates.json → 客户端筛选 → fetch MD
```

## 主题（85条）

题材表 A 涵盖 85 条永恒哲学母题（生死/自由/权力/正义/...），所有故事从其中选 1 条展开。
详见 STRATEGY.md §2 表A。

## 命名规范

故事文件统一使用拉丁文命名，格式为：

```
realitates/Cap{N}/{Cap{N}_{title_slug}_{length_la}_{NNN}.md}
```

**四要素（均拉丁文）**：

| 要素 | 含义 | 示例 | 来源 |
|------|------|------|------|
| `Cap{N}` | 算法评估难度章节 | `Cap8` | `evaluate_v2.py` 的 `v2_level` / `v2_best_fit` |
| `title_slug` | 拉丁语标题（空格→下划线） | `Taberna_Spei` | YAML 的 `title_la` 字段 |
| `length_la` | 篇幅拉丁标识（**v2_15_0起由实际词数决定，非AI声明**） | `brevis` | 实际词数：<350→brevis, 350-699→medius, ≥700→longus |
| `NNN` | 三位递增序号 | `001` | 同目录自动编号 |

**篇幅映射**：短篇→`brevis` / 中篇→`medius` / 长篇→`longus`

**示例**：`realitates/Cap19/Cap19_Taberna_Spei_brevis_001.md`

## 维护

- 备份策略：每次重大修改前自动生成 .v{version}_backup_{timestamp} 文件
- 保留最近 3 轮备份
- 已归档文件统一放入 _archived/ 目录

## 版本历史

- v3_0_0 (2026-06-30)：难度算法升级到 v3（预计算33K词形查表 + simplemma兜底，收录率87.7%）+ build_form_map.py 新合成脚本 + word_chapter_map 脏数据清理72条
- v2_9_0 (2026-06-28)：方案C 启用（生成冗余 + 自动归到真实章节文件夹 + 人工从同章节择优）+ 暂停入库后自动 OOV 分析（准确率仅 50%，改人工触发）
- v2_8_0 (2026-06-28)：入库后自动触发 OOV 增量分析（auto_supplement_map.py v1_0_0）+ 补全建议文件
- v2_7_0 (2026-06-28)：target_chapter 自动校准（用算法实测覆盖 AI 声明）+ OOV 日志（oov_corrections.jsonl，方案D 雏形）+ 长音剥离修复（evaluate_v2 v2_3_0）
- v2_6_0 (2026-06-28)：命名规范全面拉丁化（Cap{N}_{title_slug}_{length_la}_{NNN}.md）+ 方案C词表注入 + v2_best_fit + 多篇批量处理
- v2_3_0 (2026-06-28)：输出目录 stories/  →  realitates/，索引 stories.json  →  realitates.json
- v2_2_0 (2026-06-28)：硬/软约束统一 → 谱系化题材（12类） → 语法映射 → merge_yaml 输出MD
- v2_0_0-v2_1_0：约束重构 + 表E不设上限 + H5新增
- v1_5_0-v1_8_0：6次迭代，含双文件拆分尝试后回滚
- 更早：见各备份文件头
