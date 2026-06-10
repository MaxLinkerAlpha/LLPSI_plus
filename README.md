# LLPSI+++

> **Lingua Latina Per Se Illustrata — 配套阅读难度路由与可读性分析系统**
> 让每章 LLPSI 学习者都能找到「现在可以读得懂的」拓展读物。

[![Status](https://img.shields.io/badge/算法-v3.1%20可读性评分-darkred)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![可视化](https://img.shields.io/badge/HTML-ECharts%205.4.3-orange)]()
[![数据](https://img.shields.io/badge/读物-71%20本%20教材-brightgreen)]()

---

## 项目缘起

**LLPSI**（*Lingua Latina Per Se Illustrata*，俗称"Ørberg 教材"）是全球最广泛使用的纯拉丁语沉浸式教材，但学习者从 **Cap.1 罗马家庭**到 **Cap.56 罗马史**的跨越过程中，始终面临同一个问题：

> **"我现在应该读哪本补充读物？Cambridge 拉丁、Oxford 拉丁、Ecce Romani、Fabulae Faciles、Hobbitus…… 哪一本的哪一段现在我能读懂？"**

传统方式（手翻、问老师、查附录）效率极低。**LLPSI+++** 通过「**已学词汇库** × **逐段可读性分析** × **56 章节推荐**」，自动回答这个问题。

---

## 三大核心功能

| 模块 | 产出 | 适用场景 |
|------|------|----------|
| 📊 **数据洞察** | [LLPSI_Insights.html](analysis_output/LLPSI_Insights.html) (9.1MB) | 56 章难度曲线 + 段落推荐 + 点击阅读原文 |
| 🏛️ **古罗马调性看板** | [LLPSI_Roman_Insights.html](analysis_output/LLPSI_Roman_Insights.html) (79KB) | FR/RA 整体走向、主题分布、词性分层等宏观洞察 |
| 🌐 **沉浸式项目介绍** | [README.html](README.html) | 项目缘起、算法可视化、工作流图 |

---

## 快速开始

### 在线浏览（推荐）
```bash
cd /Users/max/Downloads/Projects/LLPSI+++
python3 -m http.server 8000
# 浏览器打开:
#   http://localhost:8000/README.html                          ← 项目介绍
#   http://localhost:8000/analysis_output/LLPSI_Insights.html  ← 数据洞察看板
#   http://localhost:8000/analysis_output/LLPSI_Roman_Insights.html  ← 古罗马看板
```

### 全量重跑
```bash
cd /Users/max/Downloads/Projects/LLPSI+++
python3 scripts/v2/build_learned_words.py         # 阶段1: 整理每章已学过的词汇
python3 scripts/v2/analyze_readers_v6.py          # 阶段2: 逐段计算可读性分数
python3 scripts/v2/build_reader_routing_v2.py     # 阶段3: 生成"每章推荐什么"的推荐表
python3 scripts/v2/build_llpsi_insights_html_v2.py # 阶段4: 渲染成 HTML 看板
```

### 校验某段是否可读
```bash
python3 scripts/v2/find_early_readable.py
# 会打印 oxford_1、ecce_romani 中 t50 ≤ 5 的「首章可读段」
```

---

## 算法核心（v3.1 可读性评分 极简版）

**一句话解释**：对每段拓展读物（比如 Cambridge 拉丁的某一段课文），算法会问："你学过的单词占这段课文的百分之多少？"

评分公式（N 表示你学完了 LLPSI 的第 N 章）：

```
可读性分数(第N章) = (已学词数 + 0.5 × 未来词数 + 0.7 × 专有名词数) ÷ 总拉丁语单词数
```

| 单词类别 | 含义 | 权重 |
|----------|------|------|
| ✅ **已学词** | 这个词在 LLPSI 第 1-第 N 章里已经出现过 | **1.0** |
| ⚠️ **未来词** | 这个词在 LLPSI 全书里有，但第 N 章你还没学到 | **0.5** |
| ⭐ **专有名词** | 人名、地名，在本书中出现了至少 5 次 | **0.7** |
| ❌ **生词** | 以上都不属于 | 0 分 |

**三档推荐**：
- 🟢 **流畅阅读**（分数 ≥ 80% + 至少 15 个拉丁语单词）
- 🟡 **挑战阅读**（分数 ≥ 70% + 至少 20 个拉丁语单词）
- 🔵 **选读**（分数 ≥ 50% + 至少 30 个拉丁语单词）

完整算法设计、数据流、决策记录见 [HANDOFF.md](HANDOFF.md)。

---

## 数据流

```
LLPSI 56 章课文原文
   ↓  扫描 + 去重音 + 转小写 + 去重
已学词汇库                     ← build_learned_words.py
   ↓  累加每章的已学词汇
70+ 本拓展读物原文
   ↓  按段落拆开 + 只保留故事 + 算可读性分数
可读性评分数据                 ← analyze_readers_v6.py
   ↓  按 56 章 × 三档归类
章节推荐表                     ← build_reader_routing_v2.py
   ↓  渲染成可视化页面
LLPSI_Insights.html            ← build_llpsi_insights_html_v2.py
```

---

## 覆盖的拓展读物（71 种）

| 系列 | 代表作品 | 首次流畅出现 |
|------|----------|:----------:|
| **Ørberg 配套** | Fabellae Latinae, Colloquia Personarum, Fabulae Syrae | Cap.1-2 |
| **Cambridge Latin Course** | Cambridge Latin Stage 1-5 | Cap.5 |
| **Oxford Latin Course** | Oxford Latin Cap.1-3 | Cap.6 |
| **Ecce Romani** | Ecce Romani I-II | Cap.2 |
| **Hobbitus** | Hobbitus Ille (LLPSI 改编版) | Cap.30+ |
| **Pugio Bruti** | Pugio Bruti (LLPSI 高级) | Cap.40+ |
| **Colloquia** | Colloquia Personarum | Cap.8 |
| **Fabulae Faciles** | Fabulae Faciles (LLVM 简写版) | Cap.15+ |

> 完整 71 种读物的章节分布见 [llpsi_reader_routing_v2.md](analysis_output/llpsi_reader_routing_v2.md)

---

## 项目结构

```
LLPSI+++/
├── analysis_output/          # 核心产出 (12 项, 125MB)
│   ├── LLPSI_Insights.html          9.1MB  ← v3 数据看板
│   ├── LLPSI_Roman_Insights.html    79KB   ← 古罗马洞察
│   ├── reader_vocab_stats_v6.json   6.2MB  ← v3 可读性评分数据
│   ├── learned_words_v2.json        11MB   ← 已学词汇库
│   ├── llpsi_reader_routing_v2.json 1.4MB  ← 56 章推荐表
│   ├── reader_metadata*.json         ~500KB (3 份)
│   └── ...其他 JSON/CSV/MD
├── analysis_output/archived/   # 旧版产出 (96MB)
│   ├── pre_v3_baseline/             91MB   ← 算法对比基线
│   ├── extracted/                   1.9MB  ← 历史抽取片段
│   └── backups/                     212KB  ← 版本备份
├── scripts/                   # 工具链
│   ├── v2/                          11 脚本 ← 当前 v3 流水线
│   └── archived/                    47 脚本 (旧版 v1-v5)
├── data/                      # SQLite 数据库
│   ├── llpsi_corpus.db              25MB   ← 主库
│   └── archived/                    27MB   ← 旧版备份
├── ocr_output/                # 71 本读物 OCR 文本
├── source/                    # 原始 PDF (230MB)
├── docs/                      # 9 份技术文档
├── supplements/               # 5 份补充材料
├── .trae/skills/              # IDE AI 技能 (2 项)
├── HANDOFF.md                 # 算法详细交接文档
├── README.md                  # ← 本文件
└── README.html                # 可视化项目介绍
```

---

## 技术栈

- **Python 3.11+**: 唯一编程语言
- **ECharts 5.4.3** (jsDelivr CDN): 看板可视化
- **SQLite**: 词表持久化
- **纯 UTF-8**: 全部源文件

无 npm / 无 virtualenv / 无 Docker 开箱即用。

---

## v3.1 算法版本亮点

相比 v2（依赖数据库标记 + 按单词数倒序排列），v3 的关键改进：

| 改进 | 原因 | 影响 |
|------|------|------|
| 专有名词权重 0.3 → **0.7** | 像 "Caecilius" 这种人名反复出现，懂的人自然懂 | 含人名的段落不再被低估 |
| 排序改为"可读性分数 × log(单词数)" | 光按长度排序，长段霸榜 | 短而精的高分段获得合理位置 |
| 段落长度门槛 (15/20/30) | 6 个词的段没法读 | 零碎片段不再进入推荐 |
| 去掉语法表和版权页 | 变格表不是故事 | 只推荐实际能读的内容 |
| 过滤规则统一 | 两套规则导致段错位 | 点击"阅读"弹出正确内容 |

---

## 已知边界

| 编号 | 描述 |
|------|------|
| K5 | LLPSI 下册（36–56 章）的文字识别质量不如上册。如果发现 Cap.30+ 以后所有推荐都偏难，应先检查下册的课文扫描质量 |
| K6 | 全量重跑约 3–5 分钟（M1 MacBook）；可并行加速 |

完整已知问题清单见 [HANDOFF.md §8](HANDOFF.md)。

---

## 贡献指南

修改前请先阅读：
1. [HANDOFF.md](HANDOFF.md) —— 算法与数据流总览
2. [docs/Technical_Architecture_VISIO_ROMANA.md](docs/Technical_Architecture_VISIO_ROMANA.md) —— 长期架构目标

修改 `analyze_readers_v6.py` 后必须：
- 同步更新 `HANDOFF.md §3 算法核心`
- 同步更新 `scripts/v2/find_early_readable.py`（如修改评分公式）
- 运行全量流水线验证

---

## 维护者

- 项目由 Solo + 制度性 Agent 流水线（planner → reviewer → dispatcher → executor）协作开发
- 文档版本：v1.2（与 v3.1 算法同步 + 71 本读物 + 清理后目录）
- 最近更新：2026-06-10

## Git 分支

| 分支 | 用途 | 说明 |
|:----|:-----|:-----|
| `main` | 稳定发布 | 仅存放可面向用户的稳定版本 |
| `dev` | 日常开发 | 所有开发工作推送至此（当前活跃） |

> 远程仓库: `git@github.com:MaxLinkerAlpha/LLPSI_plus.git`
