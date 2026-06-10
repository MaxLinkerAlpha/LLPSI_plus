# LLPSI+++ 项目计划

> **版本**: v1.8.0 | **更新**: 2026-06-06
> **状态**: Phase 1 MVP 进行中（优先现有读物匹配） + RA 全书数据已就绪 + ROI 分层完成 + 段级精确分析完成
> **数据库**: 13 本书 / 205 段 / 410K 词 已入库 `data/llpsi_corpus.db`

---

## 项目目标

为 LLPSI *Familia Romana* 自学者解决「语法跃迁区间」问题——Cap. 8-13 区间语法复杂度急剧上升，导致大量自学者放弃。

**核心原则**：不破坏 LLPSI 方法论（全程拉丁语、零翻译、语境推导）。

---

## ⚠️ 词频分析后的认知更新 (v1.3.0)

数据驱动的新发现重塑了项目方向。详见 [analysis_output/analysis_report.md](../analysis_output/analysis_report.md) 与 [analysis_output/LLPSI_Insights.html](../analysis_output/LLPSI_Insights.html)。

### 关键发现

| 旧假设 | 数据真相 |
|------|------|
| 「第九章墙」= 第 8-9 章起**生词密度激增** | Cap. 8-13 新词密度稳定在 **22-28%**，未出现统计学意义上的"陡坡" |
| 应聚焦于**高密度章节** | 35 章中**仅 Cap. XXV (30.3%)** 越过陡坡阈值（23.1% × 1.2） |
| 「第九章墙」= 一个孤立的"墙" | 实际上是 LLPSI 编写者**有意为之的语法跃迁**：从描述性叙事进入间接引语、关系从句、夺格句型 |

### 结论：必须区分两类「墙」

| 类型 | 章节 | 难度性质 | 解决方案 |
|------|------|---------|---------|
| **语法之墙** (Cap. VIII–XIII) | 6 章 | 句法复杂度跃迁，不是词汇问题 | **句法脚手架**：用熟悉词汇反复展示新句法 |
| **密度之墙** (Cap. XXV) | 1 章 | 神话专名集中 (Theseus, Ariadne, Labyrinthus) | **词汇脚手架**：在 Cap. XXIV–XXV 区间插入神话背景微阅读 |

**修订后 MVP 目标章节**: Cap. 8、9、10、11、12、13（语法墙） + Cap. 25（密度墙） = **7 个优先章节**

---

## 总体路线

```
Phase 1 (MVP)              Phase 2                  Phase 3
LLPSI 读物精准匹配 + 插入   AI 生成微阅读（覆盖        社区协作 + 长期维护
推荐引擎                    现有读物空白）
──────────────── →        ──────────────── →       ──────────────────
2-3 天完成                 补充覆盖                  长期维护
```

---

## 方案对比

| | 方案一：权威读物路线 | 方案二：AI 生成路线 |
|------|------|------|
| **内容来源** | LLPSI 系列拓展读物 (Colloquia Personarum, Fabulae Syrae 等) + 外部分级读物 | LLM 生成拉丁语微阅读 |
| **优点** | 零语法错误，完全权威，数据驱动精准匹配 | 快速产出，精准匹配难度 |
| **缺点** | 需获取读物 + OCR + 词频匹配，前置工作量大 | 可能有拉丁语语法错误，仅用于现有读物无法覆盖的章节 |
| **定位** | **首选方案** | **补充覆盖（末选方案）** |

---

## Phase 1: MVP（现有读物精准匹配 + 插入推荐 + AI 补充）

### 核心思路

1. **先分析（已完成）**：扫描 OCR 文本 → 统计每章新词密度 → 定位两类陡坡章节
2. **再匹配（进行中）**：对 7 个优先章节，首先从现有 LLPSI 扩展读物中匹配对应段（Colloquia Personarum + Fabulae Syrae + Fabellae Latinae），无法覆盖时再用 LLM 生成
   - 语法墙章节：句法脚手架（用 Cap. 1-7 词汇反复展示间接引语/从句）
   - 密度墙章节：词汇脚手架（Cap. 24 词汇预热 + Cap. 25 词汇多次复现）
3. **输出**：每章插入推荐指南 + 补充阅读 + 阅读建议

### MVP 具体步骤

```
Step 1: 数据准备（已完成 ✅）
  ✅ Familia Romana 完整 OCR 文本 (ocr_output/familia_romana/clean.txt)
  ✅ 分页清洗文本 (ocr_output/familia_romana/per_page_clean/)

Step 2: 词频分析脚本 ([scripts/iterum_analysis.py](../scripts/iterum_analysis.py)) （已完成 ✅）
  ✅ 按 CAPITVLVM / CAP. 切分文本
  ✅ 统计每章新增词汇数
  ✅ 标记「陡坡章节」(新词密度 > 27.7%)
  ✅ 输出报告: [analysis_report.md](./analysis_output/analysis_report.md)
  ✅ 数据可视化: [LLPSI_Insights.html](../analysis_output/LLPSI_Insights.html) (FR+RA 合并,主)

Step 3: 读物匹配引擎 + 插入推荐指南 ([scripts/generate_insertion_guide.py](../scripts/generate_insertion_guide.py)) （进行中 ⏳）
  □ 输入: 7 个目标章节 + 现有读物段数据库 (data/llpsi_corpus.db)
  □ 匹配逻辑:
    ┌─────────────────────────────────────────────────┐
    │ [语法墙章节] Cap. 8-13                           │
    │  - 从 Colloquia Personarum 匹配对应章节段         │
    │  - 从 Fabellae Latinae 匹配对应章节段             │
    │  - 从 Fabulae Syrae 按词频相似度匹配最佳段        │
    │  - 若均无法覆盖 → 降级使用 LLM 生成               │
    ├─────────────────────────────────────────────────┤
    │ [密度墙章节] Cap. 25                              │
    │  - 优先从 Fabulae Syrae (神话主题) 匹配           │
    │  - 其次从其他读物按词频匹配                       │
    │  - 若均无法覆盖 → 降级使用 LLM 生成               │
    └─────────────────────────────────────────────────┘
  □ 输出: reader_insertion_guide.md (每章插入建议：读物段 + 阅读顺序)
  □ 降级覆盖: 匹配空白的章节用 LLM 生成微阅读 → ampliata_generate.py

Step 4: 交付
  □ supplements/ 目录: 7 章 × 1-3 篇 = 7-21 个微阅读
  □ reading_guide.md: 阅读路线图
```

### MVP 优先章节 (修订后)

| 优先级 | 章节 | 类型 | 新词密度 | 理由 |
|:------:|:----:|:----:|:--------:|------|
| 1 | Cap. VIII  | 语法墙 | 22.2% | 间接引语首次系统出现 |
| 1 | Cap. IX    | 语法墙 | 22.6% | 从句大量引入 |
| 1 | Cap. X     | 语法墙 | 22.5% | 关系从句扩展 |
| 2 | Cap. XI    | 语法墙 | 21.2% | 句法继续复杂化 |
| 2 | Cap. XII   | 语法墙 | 25.5% | 夺格句型进入 |
| 2 | Cap. XIII  | 语法墙 | 27.6% | 逼近密度阈值 |
| 3 | Cap. XXV   | 密度墙 | **30.3%** | 全书唯一密度越线 |

> 备注: 优先级 1 = 必修,优先级 2 = 推荐,优先级 3 = 补充

### MVP 产出物

```
supplements/
├── reader_insertion_guide.md   插入推荐指南（每章读物匹配结果 + 阅读顺序）
├── supplement_08.txt    "Mārcus Nārrat"  (Cap.VIII 间接引语脚手架)
├── supplement_09.txt    "Quod Dīxit Mārcus" (Cap.IX 从句脚手架)
├── supplement_10.txt    "Familia Loquitur" (Cap.X 关系从句)
├── supplement_11.txt    ...
├── supplement_12.txt    ...
├── supplement_13.txt    ...
├── supplement_25.txt    "Theseus in Labyrinthō" (Cap.XXV 神话背景)
└── reading_guide.md     阅读路线图
```

### 不做的（留给后续）

- [x] LLPSI 拓展读物 OCR (13 本书已入库)
- [ ] Web 界面 / 阅读器
- [ ] 拉丁语对话 AI（Cicerō）
- [ ] 可视化插图

---

## Phase 2: AI 生成微阅读（覆盖现有读物空白）

当现有读物无法覆盖的章节（如 Cap.32-35 区间、RA 后半段）出现裂缝时：

1. LLM 生成微阅读 → 按目标章节词汇约束
2. 人工抽查审核语法质量
3. 纳入 reader_insertion_guide.md 推荐体系

---

## Phase 3: 社区协作

长期目标——动员其他 LLPSI 学习者参与：

- **分工模式**: 每人认领 1-2 个章节的补充阅读创作/校对
- **审核流程**: AI 生成 → 拉丁语能力者审核 → 发布
- **输出格式**: 纯文本 + 简单排版,不依赖平台

---

## 技术选型

| 组件 | 选择 | 原因 |
|------|------|------|
| OCR 文本 | 已有 | 已完成 |
| 词频分析 | Python 脚本 | 简单直接 |
| 数据可视化 | ECharts (单 HTML) | 已在 analysis_output/LLPSI_Insights.html 交付 |
| 内容生成 | LLM API (Claude / GPT-4) | 拉丁语能力强 |
| 输出格式 | 纯文本 .txt | 零依赖,易分发 |

---

## 当前进度

- [x] Familia Romana PDF OCR 提取完成 (331页, 55万字符)
- [x] **Roma Aeterna PDF OCR 提取完成** (高清单彩2版, Cap. XXXVI–LVI, 21 章)
- [x] LLPSI 方法论与生态系统研究完成 → [LLPSI_Research.md](./LLPSI_Research.md)
- [x] 方案选定: 方案一 (权威读物匹配) 做首选, 方案二 (AI生成) 作补充覆盖
- [x] **Step 2: 词频分析脚本** → [scripts/iterum_analysis.py](../scripts/iterum_analysis.py) + [scripts/analyze_book.py](../scripts/analyze_book.py) + 报告
- [x] **FR+RA 数据合并** → [scripts/merge_analysis.py](../scripts/merge_analysis.py) → [analysis_output/combined_long.csv](../analysis_output/combined_long.csv)
- [x] **数据可视化页面** → [analysis_output/LLPSI_Insights.html](../analysis_output/LLPSI_Insights.html) (FR+RA 合并,主)
- [x] **项目结构整理** → 所有 .trae/documents 移入 docs/;ocr_output/familia_romana/ 整合;debug 截图归档
- [x] **Source 文件清理** → 24 个重复文件已删,3 个高清版保留,新增 11 个拓展读物
- [ ] Step 3: 读物匹配引擎 + 插入推荐指南 — `generate_insertion_guide.py` + `reader_insertion_guide.md`
- [ ] Step 4: 交付物 (7 章节补充阅读 + 阅读指南)

### v1.4.0 新增的关键发现 (基于 FR + RA 56 章数据)

| 发现 | 含义 | 行动 |
|------|------|------|
| **FR → RA 难度跃迁**: 第 35 章 (22.4%) → 第 36 章 (48.9%) | 完成 FR 后立即遭遇罗马史专名爆炸 | 需在 Cap. XXXVI 前提供"RA 适应期"微阅读 |
| **RA 章节普遍更长**: 平均 4,209 词 vs FR 的 1,330 词 | 单次阅读量大,需分块 | 段内切分策略 |
| **RA Cap. 36 最高密度 (48.9%)** | 共和国专有名词首次集中爆发 | 优先生成 Cap. 36 微阅读 (RA 优先章节 #1) |
| **RA Cap. 48 最高词数 (8,388 词)** | 罗马帝国扩张史的长篇叙事 | 建议按事件分块阅读 |
| **RA 末章 (Cap. 56) 累计 24,220 词形** | 远超 FR 终值的 11,019 词形 (RA 自身贡献 ~13,000) | 词汇量目标比原计划 3,500 词上调 |

详见 [analysis_output/combined_priority_report.md](../analysis_output/combined_priority_report.md)。

### v1.5.0 新增 (ROI 分层 + FR HD 版本验证)

| 决策 | 含义 | 行动 |
|------|------|------|
| **学习目标重构为 ROI 分层** | 从"目标越高越好"转向"投产比最优" — 2,000 词族甜蜜点 | [vocabulary_threshold_research.md](./vocabulary_threshold_research.md) v2.0 已重构,加入 ROI 曲线、6 层金字塔、4 大误区澄清 |
| **FR HD 首选方案确认** | HD 2nd color text-selectable 仍是首选,与 OCR 输出一致性 79% | [source_version_comparison_report.md §1.1](../analysis_output/source_version_comparison_report.md) 已补充 OCR 样本对比数据 |
| **FR 普通版降级** | 在含变格表/介词表的页面 pypdf 失真明显 (p.30 重叠率仅 58.9%) | 不再依赖普通版,OCR 输出可作脚注补充 |
| **Ørberg 设计哲学与 ROI 视角契合** | FR 完成 (1,800 词族) ≈ 甜蜜点的 90%,RA (3,500) = 学术延伸 | 大多数学习者建议停在 FR,本项目"分级读物匹配"应优先支持 Tier 1-2 用户 |

### 当前 Todo (按 ROI 优先级)

- [x] FR HD 三个版本 OCR 样本对比
- [x] ROI 曲线生成 (PIL 替代 matplotlib)
- [x] vocabulary_threshold_research.md 重构为 ROI 分层版
- [x] source_version_comparison_report.md 补充 FR OCR 样本
- [x] **用 pypdf 重新提取 FR + RA 首选版本文本** (HD 2nd color) — v1.6.0
- [x] **重跑 FR + RA 词频分析** (使用 HD 文本) — v1.6.0
- [x] **重生成两册合并 HTML 可视化** (顶层加"甜蜜点"标注) — v1.6.0
- [x] **bug 修复 (segment_book / merge_analysis / extract_hd_text / init_fr_vocab)** — v1.6.0
- [x] **精确词频计算 (--precise)** — v1.6.0
- [x] **高频新词加权算法 (w4)** — v1.6.0
- [x] **SQLite 数据库设计 + 全量入库 (13 本书 / 197 段 / 408K 词)** — v1.6.0
- [x] **整段模式 (segment_whole) 支持 4 本无标准章节的书** — v1.6.0
- [x] 插入推荐指南 → [generate_insertion_guide.py](../scripts/generate_insertion_guide.py) → [reader_insertion_guide.md](../analysis_output/reader_insertion_guide.md)
- [x] 词汇重叠度分析 (FR/RA vs reader) — 精确模式已上线

---

### v1.7.0 新增 (段级精确分析 + fr_chapter 修复 + 匹配过滤)

| 决策 | 含义 | 产出 |
|------|------|------|
| **精确模式 (`--precise`) 上线** | `vocab_overlap.py` 新增段级精确过滤，摒弃全书词袋 | Colloquia 命中率从全词袋虚高 58%→精确值 9-32%，fabellae_latinae 恢复 30 段完整数据 |
| **fr_chapter 匹配过滤** | `match_segments.py` 新增 `--use-fr-chapter`，仅从对应章节段中搜索 | Cap.8 无过滤 Top-1=Epitome(23%已知覆盖)→过滤后 Top-1=Colloquium 8(76%) |
| **fabellae_latinae OCR 噪声修复** | `parse_cap_range()` 修复 `VIIT→VIII` 等 OCR 错误；`segmentation_rules.yaml` 容错增强 | 段数 22→**30**（恢复 8 个缺失段），词数 7,146→9,127 |
| **算法评估完成** | 全面梳理当前算法 vs 项目需求，确认 3 项改进方向已全部落地 | `vocab_overlap_report.md` 精确版、`match_segments.py --use-fr-chapter` |

#### Phase 2 段数更新 (v1.7.0)

| 书名 | slug | 段数变化 | 词数变化 |
|------|------|---------|---------|
| Fabellae Latinae | fabellae_latinae | 22 → **30** | 7,146 → **9,127** |
| **总计** | - | 197 → **205** | 408,191 → **410,172** |

#### Phase 2 全量入库覆盖

| 书名 | slug | 段数 | 词数 | 模式 |
|------|------|-----:|-----:|------|
| Colloquia Personarum | colloquia_personarum | 45 | 17,249 | 章节切分 (COLLOQVIVM N) |
| Fabellae Latinae | fabellae_latinae | 30 | 9,127 | 章节切分 (N. Title (cap. X)) |
| Fabulae Syrae | fabulae_syrae | 27 | 37,544 | 章节切分 (N. NAME) |
| Sermones Romani | sermones_romani | 11 | 26,550 | 章节切分 (I. TITLE) |
| Aeneis (Liber I & IV) | aeneis | 4 | 1,443 | 章节切分 (LIBER X) |
| De Bello Gallico | de_bello_gallico | 3 | 35,322 | 章节切分 (LIBER X) |
| Amphitryo | amphitryo | 56 | 19,456 | 章节切分 (ACTVS X) |
| Cena Trimalchionis | cena_trimalchionis | 1 | 23,143 | 整段 (无章节标记) |
| Ars Amatoria | ars_amatoria | 3 | 19,844 | 章节切分 (LIBER X) |
| In Catilinam | catilina | 1 | 23,955 | 整段 ([De ...] 主题锚点) |
| Epitome Historiae Sacrae | epitome_historiae_sacrae | 1 | 48,673 | 整段 (AETAS 子标号复杂) |
| De Rerum Natura | de_rerum_natura | 1 | 36,531 | 整段 (LIBER 标头重复) |
| **Roma Aeterna** | roma_aeterna | **21** | **110,311** | 章节切分 (CAPITVLVM X) |
| **总计** | - | **205** | **410,172** | - |

#### 算法 bug 修复 (v1.6.0)

| bug | 修复 | 影响 |
|------|------|------|
| RA 累计虚高 (估高 ~20%) | 引入 --precise, 基于 FR 词形基线计算 | 之前所有基于"估算"的优先级排序需重新校准 |
| segment_book.py skip_pages 逻辑错误 | 截断到下一个 PAGE 标记, 跳过整个 PAGE | 之前扉页/目录/词汇表可能未完全清除 |
| segment_book.py title_template KeyError | try-except 兼容 {n}/{t} | 整段模式不再崩溃 |
| extract_hd_text.py 八进制转义 (\303\234) | 新增 decode_octal_escapes 函数, 多字节合并 | Aeneis 等部分 PDF 提取不再乱码 |
| init_fr_vocab 大小写不一致 | tokens 统一转小写, 过滤噪声字符 | match_segments.py 已知词匹配正确 |
| merge_analysis.py 精确模式未生效 | main() 增加 --precise/--fr-text/--ra-text 参数 | 精确计算可一键运行 |
| generate_combined_viz.py RA 起始硬编码 | 改为动态读取 ra_data | 起始章节新词数与精确计算一致 |
| segmentation_rules.yaml 重复键 | YAML 取最后值, 整段模式生效, 但仍需清理 | (已验证功能正确, 建议清理) |

---

> **版本历史**:
> - v1.2.0 (2025-06-04) — 初始方案,聚焦密度陡坡
> - v1.3.0 (2026-06-05) — **重大修订**: 词频分析揭示「第九章墙」本质是语法而非词汇问题;MVP 范围从 1 章扩展到 7 章;引入双脚手架策略
> - v1.4.0 (2026-06-06) — **拓展至上册**: OCR RA 全书 21 章;FR+RA 56 章合并难度曲线;项目结构整理;新增 11 个拓展读物
> - v1.5.0 (2026-06-06) — **ROI 分层 + FR HD 验证**: 重构学习目标为投产比视角,2,000 词族甜蜜点定位;FR HD 3 个版本 OCR 样本对比,确认首选;Ørberg 设计哲学与 ROI 视角契合分析
> - v1.6.0 (2026-06-06) — **HD 文本基线 + 精确算法 + 全量入库**: pypdf 重提取 FR/RA HD 文本;修复 RA 累计虚高 bug (--precise);高频新词加权 (w4);SQLite 数据库设计 + 13 本书 / 197 段 / 408K 词全量入库;整段模式 (segment_whole) 支持 4 本无标准章节的书;可视化重命名为 LLPSI_Insights.html;familia_romana_insights.html 已删
> - v1.7.0 (2026-06-06) — **段级精确分析 + fr_chapter 修复**: vocab_overlap.py 新增 --precise 模式(按 fr_chapter 过滤段), 修正全书词袋虚高 30-53pp; match_segments.py 新增 --use-fr-chapter 过滤; fabellae_latinae OCR 噪声修复, 恢复 8 个缺失段 (22→30 段); 全面的算法评估报告
> - v1.8.0 (2026-06-06) — **策略优先级调整**: 首选现有读物匹配 → AI 生成作为补充；「第九章墙」修正为语法跃迁而非词汇墙；读者插入推荐指南 MVP
