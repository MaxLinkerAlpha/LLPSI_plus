# LLPSI+++ 交接文档

> 本文档面向后续接手者，说明 LLPSI+++ 项目 **v3.1 算法** 的设计思路与使用方法。
> 适用范围：70+ 本拓展读物（如 Cambridge Latin、Oxford Latin、Ecce Romani 等）相对于 LLPSI 56 个章节的**难度匹配与阅读推荐**。
>
> **快速入口**：
> - 📖 项目介绍：[README.md](README.md) / [README.html](README.html)（浏览器沉浸式）
> - 📊 数据洞察看板：[analysis_output/LLPSI_Insights.html](analysis_output/LLPSI_Insights.html) (9.1MB)
> - 🏛️ 古罗马调性看板：[analysis_output/LLPSI_Roman_Insights.html](analysis_output/LLPSI_Roman_Insights.html) (79KB)

---
## 1. 项目概述——一句话说明

**LLPSI+++ 要解决什么问题？**

学完 LLPSI 教材第 N 章之后，学习者最关心一个问题：**"我现在能读懂哪本补充读物？"**

LLPSI+++ 的工作方式（对小白友好的比喻）：
1. 把你学过 LLPSI 各章的所有拉丁语单词整理成一份"已学词汇清单"。
2. 把剑桥拉丁、牛津拉丁等 70 多本拓展读物按段落拆开，逐段检查：这些单词你学过多少？
3. 把"你学过 80% 单词的段落"推荐为**流畅阅读**，"学过 70% 的"推荐为**挑战阅读**，"学过 50% 的"推荐为**选读**。
4. 最后做成一个可视化 HTML 页面，让你点开就能读。

### 1.1 算法演进（技术背景）

| 版本 | 主要问题 | 关键改进 |
|------|----------|----------|
| v1 | 按整本书算，太粗糙 | 改为按段落算 |
| v2 | 依赖数据库标记，不准 | 改用原文扫描重建已学词汇库；首次实现"综合评分"(hybrid) |
| **v3（当前）** | 专有名词权重偏低、太长段落霸榜、缺最短段落门槛 | 提升专名权重、新增最短词数门槛、排序改由"质量×长度"共同决定 |

---

## 2. 数据流总览

```
┌──────────────────────────┐
│ LLPSI 56 章 OCR 文本     │
│  - familia_romana/_full  │
│  - roma_aeterna/_full    │
└────────────┬─────────────┘
             │ 扫描 + 重音剥离 + 小写 + 词形去重
             ▼
┌──────────────────────────┐
│ learned_words_v2.json    │  ← 阶段 1：build_learned_words.py
│  - learned_per_chapter   │
│  - new_per_chapter       │
│  - llpsi_total_words     │
└────────────┬─────────────┘
             │ 累计 union(Cap.1..Cap.N)
             ▼
┌──────────────────────────┐
│ 扩展读物 OCR（_full.txt）│  ← 阶段 2：analyze_readers_v6.py
│  - 段级切分（按空行）    │
│  - 叙事过滤              │
│  - 高频专名识别（≥5次）  │
│  - hybrid 评分 + 56 章路由│
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ reader_vocab_stats_v6    │
│ llpsi_reader_routing_v2  │  ← 阶段 3：build_reader_routing_v2.py
│  - 流畅 / 挑战 / 节选    │
│  - 56 章路由表（MD + JSON）│
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ LLPSI_Insights.html      │  ← 阶段 4：build_llpsi_insights_html_v2.py
│  - 可视化看板            │
└──────────────────────────┘
```

---

## 3. v3.1 核心算法

> **小白版解释**：算法要回答一个简单问题——"一段拉丁语文章里，你学过的单词占多少？"
> 对每个单词分三类：✅ **已经学过的**（满分 1 分）、⚠️ **教材里将来才出现的**（0.5 分）、⭐ **人名地名等专有名词**（0.7 分）。
> 把三类分数加起来除以总单词数，就算出了这段文章对你来说的"可读性分数"。

### 3.1 可读性评分公式（hybrid 分数）

对每段拓展读物，先**提取其中所有的拉丁语单词**（去除重音符号、转小写、去掉纯英语词和太短的词），记作 `单词列表`。

然后对 LLPSI 教材的**每个章节 N（第 1 章到第 56 章）**，分别计算这段文章的可读性：

| 单词类别 | 含义 | 权重 |
|----------|------|------|
| ✅ **已学词** | 这个词在 LLPSI 第 1 章到第 N 章里出现过 | **1.0** |
| ⚠️ **未来词** | 这个词在 LLPSI 全书中出现过，但第 N 章你还没学到 | **0.5** |
| ⭐ **专有名词** | 人名、地名，在本书中出现了至少 5 次（不在 LLPSI 词汇表里）| **0.7** |
| ❌ **生词** | 上面都不属于 | 0 分 |

> ⭐ **v3 关键调整**：专有名词权重从 0.3 提升到 0.7。
> 为什么呢？因为像 "Clemens"、"Caecilius" 这样的人名在故事里反复出现，学习者很快就熟悉了。0.3 分会让包含这些名字的段落被严重低估，实际上它们根本不影响阅读流畅度。

```
可读性分数(第N章) = (已学词数 + 0.5 × 未来词数 + 0.7 × 专有名次数) ÷ 总拉丁单词数
```

举例：一段 20 个单词的 Cambridge 拉丁语课文，15 个词你学过，3 个是未来词，2 个是人名。
分数 = (15 × 1.0 + 3 × 0.5 + 2 × 0.7) ÷ 20 = (15 + 1.5 + 1.4) ÷ 20 = 89.5%
→ ✅ 这已经是"流畅阅读"的水平（门槛 80%）。

### 3.2 段落长度门槛（v3 新增）

并不是所有高分的段落都有阅读价值。一段只有 5 个单词的课文就算 100% 都学过，也没法读。
所以我们对三个档分别设立了**最低段落长度**：

| 难度档 | 可读性分数 ≥ | 最少拉丁语单词数 |
|--------|--------------|------------------|
| 流畅阅读 | 80% | **至少 15 个** |
| 挑战阅读 | 70% | **至少 20 个** |
| 选读 | 50% | **至少 30 个** |

### 3.3 只保留故事段落（叙事过滤）

教材里有三类内容，不是所有都适合推荐：

- ✅ **叙事性段落**：故事、人物对话、情节 → **保留**
- ❌ **语法表格**：变位表、变格表（Nominative mágnus...）→ **过滤**
- ❌ **出版信息**：版权页、目录、参考文献 → **过滤**
- ❌ **词汇列表**：生词表、索引 → **过滤**

过滤规则在 `scripts/v2/analyze_readers_v6.py` 的 `is_narrative()` 函数中，主要检查：
1. 拉丁语单词占比 ≥ 50%（排除英语为主的段落）
2. 拉丁语单词 ≥ 15 个（排除简短标注）
3. 没有语法术语（Nominative/Genitive/acc. 等）
4. 不是全大写（排除标题页）
5. 不包含出版信息关键词（ISBN、www、Domus Latina 等）

### 3.4 排序方式（v3 变动）

v2：**按单词数倒序**（最长的段落排最前）
v3：**按"可读性分数 × log(单词数)"排**（兼顾质量与长度）

```
排序值 = 可读性分数 × log(单词数 + 1)
```

> 为什么改？纯按单词数排序会让"很长、但生词很多"的段落排在前面。
> 改成可读性分数 × log(单词数) 后，**短而精的高分段**和**长而稳的中分段**都能得到合理位置。

每个难度档取排名前 30 的段落。

### 3.5 56 章阅读推荐（路由）

对每一段文章，算法会计算它在第 1 章到第 56 章分别的可读性分数。然后这样决定推荐时机：

- **流畅档** → 可读性首次达到 80% 的第 N 章起，推荐为"流畅阅读"
- **挑战档** → 可读性首次达到 70%（且未达到 80%）的第 N 章起，推荐为"挑战阅读"
- **选读档** → 可读性首次达到 50%（且未达到 70%）的第 N 章起，推荐为"选读"

同一段文章可能会被推荐到多个章节——比如一段中等难度的内容，可能在 Cap.10 是"流畅"，Cap.7 是"挑战"，Cap.5 是"选读"。

---

## 4. 关键脚本

| 脚本 | 阶段 | 一句话说明 |
|------|------|-----------|
| `scripts/v2/build_learned_words.py` | 1 | 扫描 LLPSI 全部 56 章的课文，整理出每章已学过的单词清单 |
| `scripts/v2/analyze_readers_v6.py` | 2 | 把拓展读物按段落拆开，去掉语法表/版权页，逐段计算可读性分数 |
| `scripts/v2/build_reader_routing_v2.py` | 3 | 把评分结果整理成"每章推荐什么"的推荐表 |
| `scripts/v2/build_llpsi_insights_html_v2.py` | 4 | 把推荐表渲染成可以直接在浏览器中打开的 HTML 页面 |
| `scripts/v2/find_early_readable.py` | 辅助 | 查找 Oxford 拉丁、Ecce Romani 中"第 1-5 章就能读的段落"，用于人工核验 |
| `scripts/v2/analyze_v6_quick.py` | 辅助 | 快速模式，跳过大型读物，用于开发调试 |

执行顺序：

```bash
python3 scripts/v2/build_learned_words.py
python3 scripts/v2/analyze_readers_v6.py
python3 scripts/v2/build_reader_routing_v2.py
python3 scripts/v2/build_llpsi_insights_html_v2.py
```

---

## 5. 关键文件路径

### 5.1 输入
| 用途 | 路径 |
|------|------|
| Familia Romana OCR（按页） | `ocr_output/familia_romana/per_page_clean/page_NNN.txt` |
| Familia Romana 全文 | `ocr_output/familia_romana/_full.txt` |
| Roma Aeterna OCR | `ocr_output/roma_aeterna/*.txt` |
| Roma Aeterna 全文 | `ocr_output/roma_aeterna/_full.txt` |
| 扩展读物 OCR | `ocr_output/<slug>/_full.txt`（slug 如 `oxford_1`、`ecce_romani`） |
| 主数据库（fr_vocab 表） | `data/llpsi_corpus.db` |

### 5.2 中间产物
| 用途 | 路径 |
|------|------|
| 已学词集（v3 直接消费）| `analysis_output/learned_words_v2.json` |
| 段级 hybrid 评分 | `analysis_output/reader_vocab_stats_v6.json` |
| 56 章路由表（JSON） | `analysis_output/llpsi_reader_routing_v2.json` |
| 56 章路由表（Markdown） | `analysis_output/llpsi_reader_routing_v2.md` |

### 5.3 输出
| 用途 | 路径 |
|------|------|
| 可视化看板 | `analysis_output/LLPSI_Insights.html` |

---
## 6. 项目文件组织

```
LLPSI+++/
├── analysis_output/           # (核心产出) 路由数据、HTML、统计数据
│   ├── LLPSI_Insights.html        # v3 可视化看板（路由+阅读）· 9.1MB
│   ├── LLPSI_Roman_Insights.html  # 古罗马调性数据洞察页 · 79KB
│   ├── learned_words_v2.json      # 56 章已学词汇库
│   ├── llpsi_chapter_stats.json   # 56 章统计（词数/新词占比）
│   ├── llpsi_reader_routing_v2.json  # 56 章节推荐表（JSON）
│   ├── llpsi_reader_routing_v2.md    # 推荐表可读版
│   ├── reader_metadata*.json/csv     # 读物元数据（3 份）
│   ├── reader_report_data.json       # 报告数据
│   ├── reader_vocab_stats_v6.json    # 可读性评分数据
│   └── archived/                  # 旧版备份 & 算法对比基线
├── scripts/                  # (工具链)
│   ├── v2/                       # 当前流水线（11 个脚本）
│   └── archived/                 # 旧版脚本（47 个）
├── data/                     # (数据库)
│   ├── llpsi_corpus.db             # 主数据库（25MB）
│   └── archived/                  # 旧版备份（27MB）
├── ocr_output/               # 71 本读物的 OCR 识别文本
├── source/                   # 原始 PDF 文档（仅供查阅）
├── docs/                     # 9 份技术文档
├── supplements/              # 补充阅读材料
├── .trae/skills/             # IDE AI 技能配置
├── HANDOFF.md                # ← 本文档
├── README.md                 # 项目说明
└── README.html               # 可视化项目介绍
```

---
## 7. 使用方法

### 7.1 全量重跑
```bash
cd /Users/max/Downloads/Projects/LLPSI+++
python3 scripts/v2/build_learned_words.py
python3 scripts/v2/analyze_readers_v6.py
python3 scripts/v2/build_reader_routing_v2.py
python3 scripts/v2/build_llpsi_insights_html_v2.py
open analysis_output/LLPSI_Insights.html
```

### 7.2 仅校验某段的可读章节
```bash
python3 scripts/v2/find_early_readable.py
```
会打印 `oxford_1`、`ecce_romani` 中 `t50 ≤ 5` 的「首章可读段」。

### 7.3 v3 实施位置（实际代码定位）
- `analyze_readers_v6.py` L158：`0.5 * new_partial + 0.7 * new_char`（v3 character 权重已生效）
- `analyze_readers_v6.py` L126-167：返回 `s80/s70/s50` 分数字段，供路由层直接消费
- `build_reader_routing_v2.py` L133-145：`MIN_TOKENS = {80: 15, 70: 20, 50: 30}` + `hybrid_key()` 函数
- `build_reader_routing_v2.py` L170-183：三档路由均先 `MIN_TOKENS` 过滤、再 `hybrid_key` 排序

---

## 8. 已知问题与待办项

| 编号 | 状态 | 说明 |
|------|------|------|
| K1 | ✅ 已实现 | 专有名词权重 0.3 → 0.7 |
| K2 | ✅ 已实现 | 排序改为"可读性分数 × log(单词数+1)" |
| K3 | ✅ 已实现 | 三段门槛：流畅 ≥15 词 / 挑战 ≥20 词 / 选读 ≥30 词 |
| K4 | 待确认 | 英语排除词表约 500 个词，覆盖常见英语和教学场景词。如果读物含**拉丁化的英语专名**（如 Londinium），需要手动确认 |
| K5 | 待确认 | LLPSI 下册（Roma Aeterna 36–56 章）文字识别质量较差，可能导致后半部分已学词汇库偏小。如果发现 Cap.30+ 以后所有推荐都变成"挑战"或"选读"，应优先核查下册的识别质量 |
| K6 | 性能 | 全量重跑在 M1 MacBook 上约 3–5 分钟；如需提速，可以并行处理多个读物 |
| K7 | 输出 | HTML 看板对超过 5MB 的大数据存在卡顿；建议在生成器中按章节折叠渲染 |
| K8 | ✅ 已修复 | ECharts 图表库加载顺序不对导致页面空白；已修正为先加载库再初始化图表 |
| **K9** | ✅ 已修复 | HTML 生成器与评分脚本各自维护了一份"过滤规则"，两套规则不一致导致点击"阅读"弹出错误段落。**修复：统一只用一个过滤函数。教训：凡是过滤逻辑必须只有一个地方定义。** |

---

## 9. 关键决策记录（为什么这样做？）

- **为什么不再依赖数据库，改用原文扫描来建立已学词汇库？** 数据库里的词汇标记依赖于词法分析程序自动判断，经常判错。直接扫描 LLPSI 课文原文是最直接、最准确的方式。
- **为什么要把专有名词权重从 0.3 提到 0.7？** 因为像 "Caecilius"、"Clemens" 这样的人名，在故事里反复出现，学完 Cap.1 就认识了。权重 0.3 会让包含这些名字的段落被错误判为"很难"，实际上它们是很简单的。
- **为什么排序不用"单词数"，改用"可读性分数 × log(单词数)"？** 纯按单词数排，超长但生词很多的段落会排在最前。新的算法让"短而精"的段落和"长而稳"的段落得到均衡。
- **为什么过滤规则只能有一个来源？**（K9 教训）之前 HTML 生成器和评分脚本各有一份过滤规则，两套规则不完全一样，导致推荐 ID 对应的内容错位，点击"阅读"弹出了错误段落。后来改为两个脚本共用同一个过滤函数才彻底解决。

---

## 10. 版本

- 文档版本：v1.2（简化术语、同步 71 本读物、清理后目录）
- 最近更新：2026-06-10
