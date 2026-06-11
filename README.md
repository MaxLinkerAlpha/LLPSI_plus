# LLPSI+++

> **Lingua Latina Per Se Illustrata — 配套阅读难度路由与可读性分析系统**
> 让每章 LLPSI 学习者都能找到「现在可以读得懂的」拓展读物。

[![Status](https://img.shields.io/badge/M2%20%E7%94%B5%E5%AD%90%E5%8C%96-%E8%BF%9B%E8%A1%8C%E4%B8%AD-yellow)]()
[![Algorithm](https://img.shields.io/badge/%E7%AE%97%E6%B3%95-v3.1%20%E5%8F%AF%E8%AF%BB%E6%80%A7%E8%AF%84%E5%88%86-darkred)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![Visualization](https://img.shields.io/badge/HTML-ECharts%205.4.3-orange)]()
[![Readers](https://img.shields.io/badge/%E8%AF%BB%E7%89%A9-71%20%E6%9C%AC%20%E8%AF%BE%E6%9C%AC-brightgreen)]()

---

## 项目缘起

**LLPSI**（*Lingua Latina Per Se Illustrata*，俗称"Ørberg 教材"）是全球最广泛使用的纯拉丁语沉浸式教材，但学习者从 **Cap.1 罗马家庭**到 **Cap.56 罗马史**的跨越过程中，始终面临同一个问题：

> **"我现在应该读哪本补充读物？Cambridge 拉丁、Oxford 拉丁、Ecce Romani、Fabulae Faciles、Hobbitus…… 哪一本的哪一段现在我能读懂？"**

传统方式（手翻、问老师、查附录）效率极低。**LLPSI+++** 通过「**已学词汇库** × **逐段可读性分析** × **56 章节推荐**」，自动回答这个问题。

---

## 项目里程碑（M1–M4 路线图）

> 本节为项目长期路线图，记录每个里程碑的目标、状态、关键技术决策。
> 旧版 Phase 1/2/3 路线已归档于 `docs/backup/Project_Plan.md` (v1.8.0) **不再更新**。

### 状态总览

| 阶段 | 名称 | 状态 | 关键交付物 |
|:----:|------|:----:|------------|
| **M1** | 拓展读物 OCR + 难度路由 | [OK] 已完成 | 71 本读物 OCR · 56 章推荐表 · LLPSI_Insights.html |
| **M2** | LLPSI 电子化 + 边注融合 | [IN PROGRESS] 进行中 | 数字版 LLPSI 56 章 · hover 边注 · M1 内容无缝接入 |
| **M3** | 发音融合 + AI 补全 | [TODO] 待启动 | 浏览器 TTS · Forvo 备选 · AI 生成微阅读 |
| **M4** | 语法融合 | [TODO] 占位 | 语法块嵌入或附录（形式待定） |

---

### M1: 拓展读物 OCR + 难度路由（已完成）

**目标**：把 70+ 本拓展读物（Cambridge 拉丁、Oxford 拉丁、Ecce Romani、Fabulae Faciles、Hobbitus 等）按段拆开，逐段计算"学习完 LLPSI 第 N 章后能读懂多少"，最终做成可点击阅读的 HTML 看板。

**已交付**：
- 71 本读物 OCR 文本（`ocr_output/<slug>/_full.txt`）
- 56 章已学词汇库（`analysis_output/learned_words_v2.json`）
- 段级 hybrid 可读性评分（`analysis_output/reader_vocab_stats_v6.json`）
- 56 章路由表（`analysis_output/llpsi_reader_routing_v2.json` / `.md`）
- 可视化看板（`analysis_output/LLPSI_Insights.html`，9.1MB）
- 古罗马调性看板（`analysis_output/LLPSI_Roman_Insights.html`，79KB）
- v3.1 可读性评分算法（专名权重 0.7 · 段长门槛 · hybrid 排序）

**算法与数据流细节**：参见 [HANDOFF.md](HANDOFF.md)。

---

### M2: LLPSI 电子化 + 边注融合（进行中）

**目标**：把 LLPSI 上下两册（Familia Romana 35 章 + Roma Aeterna 21 章 = 56 章）电子化，在线阅读，**还原原著的边注风格**，并把 M1 的每章拓展读物推荐**无缝接入**——读者在电子版 LLPSI 中点击某个词/章节时，可以直接跳转到匹配的拓展段落。

**关键技术决策**：

#### 2.1 视觉样式 — 学术期刊风（无分栏）

样式参考 [HTML/Themes_AcademicJournal.html](HTML/Themes_AcademicJournal.html)（TLPA 学术期刊风格），**采用**：
- Georgia 衬线字体 + 学术小写大写（small-caps）
- 顶部 masthead 装饰线、DOI 注释、卷期信息
- **实体标注系统**：
  - `.ent-loc` = 地名（斜体 + 引号 + 上标索引）
  - `.ent-gen` = 人名/家族名（小写大写 + 引号 + 上标索引）
  - `.ent-feat` = 山河/地形（斜体 + 引号 + 缩写）
- 卷期式章节标题 + 段落首行缩进
- 引用块（pull-quote）样式

**不采用** Themes_AcademicJournal 的**两栏布局**（`column-count: 2`），因为：(a) LLPSI 原书是单栏流式排版，(b) 两栏在长段落阅读中容易丢失阅读焦点，(c) 移动端不友好。

#### 2.2 边注交互 — 鼠标悬浮触发

边注（grammatical notes、cultural notes、词源解释）**默认隐藏**，鼠标**悬浮**到对应词/术语上时**即时弹出**说明卡片。

理由（与其他方案对比）：
- **悬浮弹窗**（选中）：与 LLPSI 原书"鼠标点词查义"的使用直觉一致；移动端友好（可改为点击）
- ~~侧边栏（默认显示）~~：占用屏幕宽度，桌面端尚可但移动端体验差
- ~~脚注式（页面底部）~~：与"边注"语义不符，且需要滚动跳转
- 移动端 fallback：第一次点击展开，第二次点击进入详细页

#### 2.3 M1 内容接入 — 待探索

把 `llpsi_reader_routing_v2.json` 中"每章推荐段落"嵌入电子版 LLPSI。**当前未确定具体实现**，候选方案：

| 方案 | 描述 | 优点 | 缺点 |
|------|------|------|------|
| **A. 章节末尾侧边卡片** | 每章底部自动生成"本章推荐拓展"卡片网格 | 强提示，不打断阅读 | 占版面 |
| **B. 悬浮高亮词跳转** | 文中某些关键词悬浮后显示"本词出现在 N 本读物中" | 上下文关联 | 实现复杂 |
| **C. 顶部 Tab 切换** | LLPSI 原文 / 拓展内容 Tab 切换 | 实现简单 | 强割裂感 |
| **D. 行内斜体插入** | 在 LLPSI 原文行末用小字号斜体插入一段拓展引用 | 最贴近"读书读累了旁边就有延伸" | 排版需精细 |

> **M2 阶段任务**：先实现基础电子化（hover 边注 + 学术期刊样式），再在 4 个候选方案中选定 M1 接入方式。

#### 2.4 OCR 长音重做（关键子任务）

M1 阶段 OCR 输出的拉丁语**长音（macron）几乎全部丢失**。M2 电子化要求"读物尽量带长音"，必须重做。

**调研结论（2026-06）**：传统 Tesseract 对 macron 支持差（CER 8-13%），需切换到现代模型。

**推荐技术路线**：

| 步骤 | 工具/模型 | 说明 |
|------|----------|------|
| **1. 重 OCR** | [Kraken](https://kraken.re/4.0/) + Ciaconna | 历史/古典文献首选，CER 7-8%，可针对拉丁微调 |
| 备选 1 | [LightOnOCR-2-1B](https://lighton.ai/) | 1B 参数多语言模型，明确支持 ō/ū 等长音，OlmOCR 77.2% |
| 备选 2 | Qwen3.5-35B-VL | 通用 VLLM，文本提取 73.5%，配合后处理最强 |
| **2. LLM 后处理** | Claude / GPT-4o / Mistral | 对照参考电子版修复 OCR 残缺 + macron |
| **3. 词典强制校验** | Wiktionary 拉丁词典 / Latin lemmatizer | 对已知词条强制标注长音，剔除误识 |

**学术参考**：
- [AAAI 2025 — Reference-Based Post-OCR with LLM](https://arxiv.org/abs/2410.13305) — 用参考电子版 + LLM 修复 diacritic 文本
- [MDPI 2025 — Kraken + ByT5 后处理](https://www.mdpi.com/2079-9292/14/15/3083) — CER 从 38% → 15%
- [KBLab 2025 — Kraken 古典拉丁测试](https://kb-labb.github.io/posts/2025-06-11-from-parchment-to-pixel/) — 实务对比

**优先级**：LLPSI 上册（FR 1-35 章）→ 拓展读物高频段落 → RA 36-56 章

---

### M3: 发音融合 + AI 补全（待启动）

**目标**：在 M2 电子化 LLPSI 基础上，实现"**点击哪里读哪里**"的发音功能；同时考虑用 AI 生成微阅读，参考 `supplements/` 目录现有 4 份样例（`supplement_08.txt`、`supplement_10_lex.txt`、`supplement_10_syntax.txt`、`supplement_25.txt`）。

#### 3.1 发音方案：浏览器内置 TTS（默认）

**首选**：[Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)（`window.speechSynthesis`），浏览器原生、零成本、即时。

- **优点**：零依赖、零费用、所有现代浏览器都支持
- **缺点**：不同浏览器的拉丁语发音质量参差不齐（Edge/Azure 较好，Safari 一般，Chrome 拉丁语支持差）
- **优化**：可指定具体 TTS 引擎（如 `speechSynthesis.getVoices()` 中筛选 `lang: 'la'` 的声音）

**备选**：如果浏览器 TTS 质量不达标，再考虑：
- 预生成 .mp3（按章节批量生成，质量稳定但首次生成耗时，需云 API 费用）
- 预生成 + 词级对齐（最完整体验，需要强制对齐算法）

#### 3.2 Forvo 真人发音（待评估）

[Forvo](https://forvo.com/) 是全球最大的真人发音社区，**430+ 种语言、6 百万+ 词条**，包含拉丁语（Latin, ISO 639-1: `la`）。

**API 调研（2026-06）**：

| 计划 | 价格 | 请求量 | 限制 | 适合度 |
|------|------|--------|------|--------|
| **Non-Profit** | $2/月 | 500 请求/天 | **禁止商业用途** | 个人学习者最佳 |
| **Commercial Small** | $28.95/月 | 10,000 请求/天 | 可商用 | 本项目规模偏大 |
| RapidAPI 第三方 | $0 / $10 / $25 / $55 | 500/月免费 / 10K / 100K / 不限 | - | 灵活但有中间商风险 |

**关键不确定性**（**留待 M3 启动时验证**）：
1. **拉丁语发音词条数量**：Forvo 是众包的，Latin 词条可能远少于英语/西语。需要先抽样测试 `https://forvo.com/word/mater/#la` 是否返回结果
2. **音频 URL 有效期**：Forvo MP3 链接是临时签名（通常数小时），需要缓存到本地
3. **非商用条款**：本项目为非商业教育用途，$2/月 Non-Profit 计划合规；但若未来开放给机构使用，需要切换到商业计划
4. **用户体验**：直接跳 Forvo 网站需手动操作，体验差；只有 API 内嵌才顺畅

**实际建议**：
- 短期：**浏览器 TTS 上线即可**，不依赖 Forvo
- 中期：M3 后半段根据"点击 → 朗读"的用户反馈决定是否引入 Forvo
- 长期：若引入，作为可选增强（在朗读按钮旁加 🎙️ 切换按钮，由用户选 TTS 或 Forvo）

#### 3.3 AI 生成微阅读

参考 `supplements/` 现有样例风格（详见 `supplements/reading_guide.md`），按目标章节的"已学词汇 + 主题约束"由 LLM 生成微阅读。

**生成流程**（与 M1 算法协同）：
1. 找出该章已学词汇（`learned_words_v2.json`）
2. 从语法/词汇角度确定脚手架类型（句法 / 词汇）
3. 用 LLM 生成 200-400 词的微阅读，**强制词汇约束**（每个新词只允许出现 1-2 次）
4. 人工抽查（拉丁语能力者）
5. 入库到 `supplements/`

**M3 与 M1 的关系**：M1 算法评分（`reader_vocab_stats_v6.json`）可直接复用，作为"新词密度是否超阈值"的自动校验器。

---

### M4: 语法融合（占位）

**当前状态**：占位，形式待定。

**候选方案**：
- **A. 嵌入正文**：在 LLPSI 课文中遇到新语法点时，行内弹出语法说明
- **B. 章节末尾附录**：每章底部自动追加"本章语法小结"
- **C. 独立语法手册**：单独一份"LLPSI 56 章语法进度手册"，与电子版双向链接

**待 M2/M3 稳定后启动**。

---

## 三大核心功能

| 模块 | 产出 | 适用场景 |
|------|------|----------|
| **数据洞察** | [LLPSI_Insights.html](analysis_output/LLPSI_Insights.html) (9.1MB) | 56 章难度曲线 + 段落推荐 + 点击阅读原文 |
| **古罗马调性看板** | [LLPSI_Roman_Insights.html](analysis_output/LLPSI_Roman_Insights.html) (79KB) | FR/RA 整体走向、主题分布、词性分层等宏观洞察 |
| **沉浸式项目介绍** | README.html | 项目缘起、算法可视化、工作流图 |

> **未来扩展**（M2/M3 完成后）：M2 电子化 LLPSI + M3 朗读 + M4 语法 将整合为统一的"LLPSI+++ Reader"单页应用，替代当前的"看板 + 原始 PDF"模式。

---

## 快速开始

### 在线浏览（推荐）
```bash
cd /Users/max/Downloads/Projects/LLPSI+++
python3 -m http.server 8000
# 浏览器打开:
#   http://localhost:8000/README.html                          <- 项目介绍
#   http://localhost:8000/analysis_output/LLPSI_Insights.html  <- 数据洞察看板
#   http://localhost:8000/analysis_output/LLPSI_Roman_Insights.html  <- 古罗马看板
```

### M1 全量重跑
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
# 会打印 oxford_1、ecce_romani 中 t50 <= 5 的「首章可读段」
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
| **已学词** | 这个词在 LLPSI 第 1-第 N 章里已经出现过 | **1.0** |
| **未来词** | 这个词在 LLPSI 全书里有，但第 N 章你还没学到 | **0.5** |
| **专有名词** | 人名、地名，在本书中出现了至少 5 次 | **0.7** |
| **生词** | 以上都不属于 | 0 分 |

**三档推荐**：
- **流畅阅读**（分数 >= 80% + 至少 15 个拉丁语单词）
- **挑战阅读**（分数 >= 70% + 至少 20 个拉丁语单词）
- **选读**（分数 >= 50% + 至少 30 个拉丁语单词）

完整算法设计、数据流、决策记录见 [HANDOFF.md](HANDOFF.md)。

---

## 数据流（M1 流水线）

```
LLPSI 56 章课文原文
   ↓  扫描 + 去重音 + 转小写 + 去重
已学词汇库                     <- build_learned_words.py
   ↓  累加每章的已学词汇
70+ 本拓展读物原文
   ↓  按段落拆开 + 只保留故事 + 算可读性分数
可读性评分数据                 <- analyze_readers_v6.py
   ↓  按 56 章 × 三档归类
章节推荐表                     <- build_reader_routing_v2.py
   ↓  渲染成可视化页面
LLPSI_Insights.html            <- build_llpsi_insights_html_v2.py
```

> **M2 扩展数据流**（待实现）：M1 章节推荐表 → 注入到 LLPSI 数字版每章末尾（4 种候选方案见 M2.3 节）。

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
│   ├── LLPSI_Insights.html          9.1MB  <- v3 数据看板
│   ├── LLPSI_Roman_Insights.html    79KB   <- 古罗马洞察
│   ├── reader_vocab_stats_v6.json   6.2MB  <- v3 可读性评分数据
│   ├── learned_words_v2.json        11MB   <- 已学词汇库
│   ├── llpsi_reader_routing_v2.json 1.4MB  <- 56 章推荐表
│   ├── reader_metadata*.json         ~500KB (3 份)
│   └── ...其他 JSON/CSV/MD
├── analysis_output/archived/   # 旧版产出 (96MB)
│   ├── pre_v3_baseline/             91MB   <- 算法对比基线
│   ├── extracted/                   1.9MB  <- 历史抽取片段
│   └── backups/                     212KB  <- 版本备份
├── scripts/                   # 工具链
│   ├── v2/                          11 脚本 <- 当前 v3 流水线
│   └── archived/                    47 脚本 (旧版 v1-v5)
├── data/                      # SQLite 数据库
│   ├── llpsi_corpus.db              25MB   <- 主库
│   └── archived/                    27MB   <- 旧版备份
├── ocr_output/                # 71 本读物 OCR 文本
├── source/                    # 原始 PDF (230MB)
├── docs/                      # 技术文档
│   └── backup/
│       └── Project_Plan.md          <- 旧版 Phase 1/2/3 路线（v1.8.0，**只读**）
├── HTML/                      # 3 套主题样式原型
│   ├── Themes_AcademicJournal.html  <- M2 主样式（实体标注系统）
│   ├── Themes_ChineseScroll.html
│   └── Themes_EditorialMagazine.html
├── supplements/               # 4 份 AI 生成的脚手架阅读（已含长音）
│   ├── supplement_08.txt            <- Cap. VIII 间接引语脚手架
│   ├── supplement_10_lex.txt        <- Cap. X 词汇脚手架
│   ├── supplement_10_syntax.txt     <- Cap. X 句法脚手架
│   ├── supplement_25.txt            <- Cap. XXV 神话密度墙
│   └── reading_guide.md
├── .trae/skills/              # IDE AI 技能 (2 项)
├── HANDOFF.md                 # M1 算法详细交接文档
├── README.md                  # <- 本文件
└── README.html                # 可视化项目介绍（M2 将替换为电子化 LLPSI）
```

---

## 技术栈

- **Python 3.11+**: M1 流水线唯一编程语言
- **ECharts 5.4.3** (jsDelivr CDN): 看板可视化
- **SQLite**: 词表持久化
- **Kraken + LLM**: M2 OCR 长音重做（详见 M2.4 节）
- **Web Speech API / Forvo API**: M3 发音方案
- **纯 UTF-8**: 全部源文件

无 npm / 无 virtualenv / 无 Docker 开箱即用（M1 阶段）。M2 引入前端栈后会重新评估。

---

## v3.1 算法版本亮点（M1）

相比 v2（依赖数据库标记 + 按单词数倒序排列），v3 的关键改进：

| 改进 | 原因 | 影响 |
|------|------|------|
| 专有名词权重 0.3 -> **0.7** | 像 "Caecilius" 这种人名反复出现，懂的人自然懂 | 含人名的段落不再被低估 |
| 排序改为"可读性分数 × log(单词数)" | 光按长度排序，长段霸榜 | 短而精的高分段获得合理位置 |
| 段落长度门槛 (15/20/30) | 6 个词的段没法读 | 零碎片段不再进入推荐 |
| 去掉语法表和版权页 | 变格表不是故事 | 只推荐实际能读的内容 |
| 过滤规则统一 | 两套规则导致段错位 | 点击"阅读"弹出正确内容 |

---

## 已知边界

| 编号 | 描述 |
|------|------|
| K1 | **OCR 长音丢失**（M1 已发现问题，M2 修复中）：当前 71 本读物 OCR 输出中 macron 几乎全部丢失，长音识别需要切换到 Kraken + LLM 后处理方案 |
| K2 | LLPSI 下册（36–56 章）的文字识别质量不如上册。如果发现 Cap.30+ 以后所有推荐都偏难，应先检查下册的课文扫描质量 |
| K3 | 全量重跑约 3–5 分钟（M1 MacBook）；可并行加速 |

完整已知问题清单见 [HANDOFF.md §8](HANDOFF.md)。

---

## 经验教训库（按时间倒序）

### 2026-06-11 · M2 启动

**教训 1：OCR 长音问题被 M1 算法"过滤"掉了**
M1 算法依赖 `build_learned_words.py` 中的"去重音 → 转小写 → 去重"步骤，这个步骤**主动丢弃了 macron**。算法评分对长音不敏感（因为拉丁语词汇判定不依赖长音），所以 K1 一直没暴露。直到 M2 准备电子化、要求"读物带长音还原原著风格"时才发现。

**预防措施**：今后任何数据处理脚本都要保留"原始层"（raw 文本），不要在主流程中 destructive 转换原始信息；如需去重音，应在副本上操作并保留原文件。

**教训 2：Forvo 调研发现"API 免费 ≠ 体验可用"**
Forvo Non-Profit 计划仅 $2/月 500 请求/天，但 500 请求对 56 章 LLPSI 全部词汇（~5,600 词）**只够 1 轮完整试听**。同时拉丁语词条是众包的，**实际可用词条数远少于英语/西语**，需要先抽样验证。

**预防措施**：外部 API 选型时，"价格"和"功能"之外要加上"**数据覆盖率**"和"**配额 × 实际数据量**"两个维度。

### 2026-06-10 · M1 完成

**教训 3（K9 续）：HTML 生成器与评分脚本两套过滤规则不一致**
修复：统一只用一个过滤函数。教训：凡是过滤逻辑必须只有一个地方定义。

---

## 贡献指南

修改前请先阅读：
1. [HANDOFF.md](HANDOFF.md) —— M1 算法与数据流总览
2. 本 README **M2 / M3 / M4** 章节 —— 后续里程碑规划
3. [docs/backup/Project_Plan.md](docs/backup/Project_Plan.md) —— 旧版 Phase 1/2/3 路线（只读，仅供参考）

修改 `analyze_readers_v6.py` 后必须：
- 同步更新 `HANDOFF.md §3 算法核心`
- 同步更新 `scripts/v2/find_early_readable.py`（如修改评分公式）
- 运行全量流水线验证

M2 阶段新增文件建议放在 `scripts/v3/` 目录（**待 M2 启动时建**），与 `v2/` 共存。

---

## 维护者

- 项目由 Solo + 制度性 Agent 流水线（planner → reviewer → dispatcher → executor）协作开发
- 文档版本：v1.3（M2 路线图 + OCR/Forvo 调研结论 + 经验教训库 v1）
- 最近更新：2026-06-11
- 旧版 Project_Plan.md (v1.8.0) 已归档至 `docs/backup/`，**严禁修改**

## Git 分支

| 分支 | 用途 | 说明 |
|:----|:-----|:-----|
| `main` | 稳定发布 | 仅存放可面向用户的稳定版本 |
| `dev` | 日常开发 | 所有开发工作推送至此（当前活跃） |

> 远程仓库: `git@github.com:MaxLinkerAlpha/LLPSI_plus.git`
