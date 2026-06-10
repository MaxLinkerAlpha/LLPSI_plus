# LLPSI+++ 知识文档

> **版本**: v1.0 | **2026-06-10 整合**
> **整合来源**: LLPSI_Research / Project_Plan / PRD_VISIO_ROMANA / Technical_Architecture / reader_audit_report / vocabulary_threshold_research 六份文档
> **数据基准**: 71 本 OCR 读物 + 56 章节 (FR 1-35 + RA 36-56) + 25,448 词形

---

## 目录

- [第一部分：LLPSI 教材本体研究](#第一部分llpsi-教材本体研究)
- [第二部分：学习目标 ROI 分层](#第二部分学习目标-roi-分层)
- [第三部分：算法设计与可视化方案](#第三部分算法设计与可视化方案)
- [第四部分：读物评估与可读性档案](#第四部分读物评估与可读性档案)
- [第五部分：LLPSI 关键门槛点](#第五部分llpsi-关键门槛点)
- [附录：参考文献](#附录参考文献)

---

# 第一部分：LLPSI 教材本体研究

> 整合自 [LLPSI_Research.md](LLPSI_Research.md)（原 722 行）。本部分是项目的知识基础，**几乎常青**，保留全文。

## 1. LLPSI 系列概述

### 1.1 什么是 LLPSI

**Lingua Latina Per Se Illustrata**（拉丁语：*通过自身阐释的拉丁语*）是丹麦语言学家 **Hans H. Ørberg** (1920–2010) 编著的拉丁语学习教材。其副标题 *Per Se Illustrata* 精确点明了方法的核心承诺：**完全用拉丁语教拉丁语**——没有任何母语翻译、没有任何对照表、没有任何语法元语言（至少初期不出现）。

Ørberg 任职于 Naturmetodens Sproginstitut（自然法语言学院），致力于将"直接法"（Direct Method）系统化应用于多种语言教学。LLPSI 是他毕生心血的结晶，从 1955 年的 *Lingua Latina secundum naturae rationem explicata* 逐步迭代而来，1991 年定型为目前的最终版本。

### 1.2 自然法 / 归纳法哲学

LLPSI 底层遵循**自然法**（Natural Method）/ **归纳法**（Inductive Method）：

- 母语习得过程可以（也应该）在外语学习中模拟——首先是大量可理解输入（Comprehensible Input），其次是学习者自己从上下文中归纳语法规则
- 翻译不是桥梁而是障碍：每次在脑中做"拉丁语→母语"的转换，都在固化母语思维对目标语言的干扰
- 语法不是"事先被告知"，而是"事后被命名"

### 1.3 核心两本书

| 卷次 | 书名 | 内容跨度 | 词汇量 |
|------|------|----------|--------|
| Pars I | **Familia Romana** | Cap. I – Cap. XXXV（35 章） | ~1,800 词族 |
| Pars II | **Roma Aeterna** | 从神话时代到共和国晚期/帝国早期 | ~1,700 词族 |
| **合计** | | | **~3,500 词族** |

3,500 词的词汇量覆盖了拉丁语最核心的高频词汇群，足以直接阅读凯撒、西塞罗等核心经典作家——这是 LLPSI 宣传的一个关键卖点。

## 2. 核心编写原则

### 2.1 全程拉丁语（零母语）

LLPSI 全书不使用任何现代语言。从 *Rōma in Italiā est*（Cap. I 第 1 句）到 Cap. XXXV，所有解释、注记、语法说明、练习题均以拉丁语书写。

### 2.2 可理解输入（Comprehensible Input）

Ørberg 严格遵循 **Krashen 的 i+1 假说**：

- 每个新词/新语法点的引入，必须建立在 **至少 90% 以上的已知词汇** 基础之上
- 新元素通过三种方式被"解码"：视觉线索、上下文推断、词汇重叠

### 2.3 四符号旁注系统

这是 Ørberg 教学设计的核心创新——在页边距使用四种符号，**全程用拉丁语解释拉丁语**：

| 符号 | 含义 | 示例（Cap. I） |
|------|------|----------------|
| **=** | 近义词 / 同义结构 | *parvus* = *magnus* |
| **↔** | 反义词 | *parvus* ↔ *magnus*；*procul* ↔ *prope* |
| **<** | 词源派生 / 构词关系 | *Rōmānus* < *Rōma*；*timor* < *timet* |
| **:** | 拉丁语定义 | *collis : mons parvus* |

## 3. 章节结构详解

### 3.1 FR（Cap. I – XXXV）题材分布

| 章节 | 题材 | 核心语法点 |
|------|------|-----------|
| Cap. I–VII | 罗马家庭 | 名词变格、动词现在时、形容词 |
| Cap. VIII–XIII | 日常生活 | 间接引语、关系从句、夺格句型 |
| Cap. XIV–XX | 时间/空间/旅行 | 地点/时间表达、过去时 |
| Cap. XXI–XXV | 神话与历史 | 完成时、被动态、不定式 |
| Cap. XXVI–XXXV | 罗马公共生活 | 分词、间接引语系统、条件句 |

### 3.2 RA（Cap. XXXVI – LVI）题材分布

- **Cap. XXXVI–XLIV**：共和国早期史（罗马王政→布匿战争），主要素材来自李维
- **Cap. XLV–L**：共和国晚期（凯撒、西塞罗）
- **Cap. LI–LVI**：帝国早期（奥古斯都到五贤帝）

## 4. 已有解决方案（社区生态）

| 资源 | 形式 | 适用 |
|------|------|------|
| Colloquia Personarum | 配套对话集 | 句法脚手架 |
| Fabellae Latinae | Ørberg 简写版伊索寓言 | 入门阅读 |
| Fabulae Syrae | 神话故事改写 | 中级阅读 |
| Sermones Romani | 拉英对话 | 口语训练 |
| Cambridge / Oxford Latin Course | 主流教材替代 | 并行学习 |
| Wheelock's Latin | 传统语法翻译法 | 参考工具书 |
| Ørberg 选读集（Catilina, Aeneis 等） | 原文改写 | 高级阅读 |

---

# 第二部分：学习目标 ROI 分层

> 整合自 [vocabulary_threshold_research.md](vocabulary_threshold_research.md)（原 360 行）。本部分是项目最重要的"常青"研究成果，**完整保留**。

## 〇、ROI 总览（本文档核心新内容）

### 0.1 一句话结论

> **投产比最优 ≈ 2,000 词族**。这不是数学上的 ROI 峰值（那个在 100 词），而是"实用性"与"投入成本"的纳什均衡点——再少不够用，再多不划算。

![Vocabulary ROI Curve](vocabulary_roi_curve.png)

### 0.2 数学最优 vs 实用最优

| 目标 | 词汇量 | 覆盖率 | 每千词边际收益 | 评价 |
|:-----|------:|-------:|---------------:|:-----|
| **数学 ROI 峰值** | ~100 词 | 50% | 5.0% | 极高 ROI，但覆盖率太低，不实用 |
| **实用最优甜蜜点** ★ | **~2,000 词** | **80%** | **~2-4%** | **✅ 投产比与实用性的最佳平衡** |
| 独立阅读门槛 | ~6,000-8,000 词 | 95-98% | <0.5% | 学术标准，但 ROI 极低 |

### 0.3 边际收益递减表（每千词的覆盖率提升）

| 词汇区间 | 每千词带来的覆盖率提升 | 倍数关系 |
|:---------|----------------------:|--------:|
| 0→100 词 | **5.0%** | **50× 基准** |
| 100→250 词 | 0.3% | 3× |
| 250→500 词 | 0.4% | 4× |
| 500→1000 词 | 0.1% | 1× (基准) |
| 1000→2000 词 | 0.1% | 1× |
| 2000→4000 词 | 0.1% | 1× |
| 4000→8000 词 | ~0.05% | 0.5× |

> **关键洞察**：前 100 个词（the, be, to, of…）的 ROI 是后续区间的 50 倍。但只学 100 词，你认识一半句子却看不懂任何内容——这就是"数学最优"与"实用最优"的分歧点。

### 0.4 经典研究的覆盖率-词汇量对照

| 词汇量 (词族) | 文本覆盖率 | 用途 |
|--------------:|----------:|:-----|
| 1,000 词族 | ~72% | 基础生存，但每页仍有大量生词 |
| **2,000 词族** | **~80%** | **日常交流、新闻、简单小说** |
| 3,000 词族 | ~85% | 一般对话可应对，阅读仍需猜词 |
| 4,000 词族 | ~90% | 加上学术词汇表可覆盖学术文本 90% |
| 6,000-7,000 词族 | ~95% | 独立听懂的门槛 |
| 8,000-9,000 词族 | ~98% | 独立阅读的学术标准 |

> **数据来源**: Paul Nation 基于 BNC/COCA 大型语料库的研究（Schmitt, Cobb, Horst & Schmitt, 2017 复制研究，[Cambridge Language Teaching](https://www.cambridge.org/core/journals/language-teaching/article/how-much-vocabulary-is-needed-to-use-english-replication-of-van-zeeland-schmitt-2012-nation-2006-and-cobb-2007/1D217A56A2E0056E67802A6A8360FDDE)）

## 一、按投产比分层的新学习路径

### 1.1 六层金字塔（从底到顶）

```
        ▲ Tier 5: 学术独立阅读 (8,000+ 词族, 98% 覆盖率)
       ╱ ╲
      ╱   ╲  边际收益递减陷阱
     ╱ T4  ╲  Tier 4: 听力+拓展阅读 (5,000-6,000 词族, 93-95%)
    ╱───────╲
   ╱         ╲
  ╱  T3 已知   ╲  Tier 3: LLPSI RA 末段 (3,500 词族, 85%)
 ╱─────────────╲
╱   ★ 甜蜜点    ╲  Tier 2: LLPSI FR 完成 (1,800 词族, 80%) ★
╱─────────────────╲
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    Tier 1: 入门 (1,000 词族, 72%)
    Tier 0: 数学 ROI 峰值 (100 词, 50%) — 不可达
```

### 1.2 各层详述

#### Tier 1 (1,000 词族): 入门
- **覆盖率**: 72%
- **目标**: 学完 FR Cap. I–XVI
- **教学价值**: 引入基本生活词汇
- **ROI 评价**: 合理"试水"目标

#### Tier 2 ★ 甜蜜点 (2,000 词族)
- **覆盖率**: 80%
- **目标**: 学完 FR 全 35 章（Ørberg 设计终点）
- **教学价值**: **LLPSI 设计哲学与 ROI 视角的契合点**
- **ROI 评价**: ★ **多数古典学习者应停在此层**

#### Tier 3 (3,500 词族)
- **覆盖率**: 85%
- **目标**: FR + RA 全 56 章
- **配套读物**: + Sermones Romani + Aeneis (Ørberg 版)
- **ROI 评价**: ⚠️ 已进入边际收益递减区

#### Tier 4 (5,000-6,000 词族)
- **覆盖率**: 93-95%
- **配套读物**: + Amphitryo + Bello Gallico + Cena Trimalchionis + Catilina
- **ROI 评价**: 接近 95% 听力门槛，适合学术目标

#### Tier 5 (8,000+ 词族)
- **覆盖率**: 98%
- **路径**: 完成上述所有 + 大量原文阅读 (Tacitus, Livy, Quintilian, Pliny)
- **ROI 评价**: 极致追求，符合 98% 阅读标准

## 二、ROI 视角下的"何时该停止"决策

### 2.1 自检问题

学完 FR 后（累计 1,800 词族），问自己：

1. **是否想读拉丁语原文（非 Ørberg 改写本）？**
   - 否 → **建议停止**于 FR，转而泛读 Fabulae/Colloquia，自然习得
   - 是 → 继续 RA
2. **是否有学术/教学目标？**
   - 否 → **建议停止**于 FR
   - 是 → 继续 RA + 拓展读物
3. **是否能投入每天 30-45 分钟持续 1 年以上？**
   - 否 → **强烈建议停止**于 FR，转而通过阅读巩固
   - 是 → 可继续 RA

### 2.2 常见误区

❌ **误区 1**: "不读完 RA 就不算学完 LLPSI"
✅ **真相**: FR 完成 = 80% 古典文本覆盖率 = 多数古典文本可读

❌ **误区 2**: "学得越多越好"
✅ **真相**: 边际收益递减——从 2,000 词到 8,000 词需 4 倍时间，覆盖率仅 +18%

❌ **误区 3**: "不学 8,000 词就读不了原文"
✅ **真相**: 80% 覆盖率 + 词典辅助 = 可读大部分原文；95-98% = 免词典流畅读

❌ **误区 4**: "RA 比 FR 更难"
✅ **真相**: 不是"难"，是"贵"——RA 的边际 ROI 极低，但绝对难度并非不可逾越

## 三、给本项目的行动建议（按 ROI 优先级）

### 3.1 最高优先级（Tier 1→2 跃迁辅助）
1. **完成 7 个优先章节的微阅读生成**（Cap. 8-13 语法墙 *待验证* + Cap. 25 密度墙）
2. **覆盖率达到 80% 时的"出口建议"**：学完 FR 后，引导用户去 Colloquia/Fabulae 自然习得，而非立即跳 RA
3. **可视化顶部"甜蜜点"提示**：在 LLPSI_Insights.html 顶部突出"2,000 词族甜蜜点"

### 3.2 中优先级（Tier 2 巩固）
4. **FR 完成的庆祝机制**：明确告诉用户"你已达到投产比最优解"
5. **RA 的可选性提示**：强调 RA 是为研究/学术目标用户设计，爱好者可跳过

### 3.3 低优先级（Tier 3+ 学术延伸）
6. **RA + 拓展读物的关联分析**：词频匹配度（已由 v3.1 路由表覆盖）

---

# 第三部分：算法设计与可视化方案

> 整合自 [PRD_VISIO_ROMANA.md](PRD_VISIO_ROMANA.md) + [Technical_Architecture_VISIO_ROMANA.md](Technical_Architecture_VISIO_ROMANA.md) + [Project_Plan.md](Project_Plan.md)
> **数据已大幅更新**，从 35 章 → 56 章，从 13 本读物 → 71 本读物

## 一、当前核心算法：v3.1 可读性评分 极简版

**一句话解释**：对每段拓展读物（比如 Cambridge Latin 的某一段课文），算法会问："你学过的单词占这段课文的百分之多少？"

### 1.1 评分公式

```
可读性分数(第N章) = (已学词数 + 0.5 × 未来词数 + 0.7 × 专有名词数) ÷ 总拉丁语单词数
```

### 1.2 单词类别与权重

| 类别 | 含义 | 权重 |
|------|------|------|
| ✅ 已学词 | 词在 LLPSI 第 1~第 N 章里出现过 | **1.0** |
| ⚠️ 未来词 | 词在 LLPSI 全书里有，但第 N 章你还没学到 | **0.5** |
| ⭐ 专有名词 | 人名、地名，在本书中出现 ≥5 次 | **0.7** |
| ❌ 生词 | 以上都不属于 | 0 |

### 1.3 三档推荐

| 档位 | 分数门槛 | 最短长度 |
|------|---------|---------|
| 🟢 流畅阅读 | ≥ 80% | ≥ 15 个拉丁语单词 |
| 🟡 挑战阅读 | ≥ 70% | ≥ 20 个拉丁语单词 |
| 🔵 选读 | ≥ 50% | ≥ 30 个拉丁语单词 |

### 1.4 关键算法演进

| 版本 | 主要问题 | 关键改进 |
|------|----------|----------|
| v1 | 按整本书算，太粗糙 | 改为按段落算 |
| v2 | 依赖数据库标记，不准 | 改用原文扫描重建已学词汇库；首次实现"综合评分" |
| **v3（当前）** | 专有名词权重偏低、太长段落霸榜、缺最短段落门槛 | 提升专名权重至 0.7、新增最短词数门槛、排序改由"质量×长度"共同决定 |

## 二、流水线脚本（4 个核心 + 2 个辅助）

```bash
# 阶段1: 整理每章已学过的词汇
python3 scripts/v2/build_learned_words.py

# 阶段2: 逐段计算可读性分数
python3 scripts/v2/analyze_readers_v6.py

# 阶段3: 生成"每章推荐什么"的推荐表
python3 scripts/v2/build_reader_routing_v2.py

# 阶段4: 渲染成 HTML 看板
python3 scripts/v2/build_llpsi_insights_html_v2.py
```

## 三、可视化方案：古罗马调性设计

### 3.1 设计理念

**"Roman Inscription Meets Modern Data"** — 罗马铭文的庄重 + 现代数据可视化的清晰。

### 3.2 配色方案（古罗马经典）

| 角色 | 颜色 | 色值 | 灵感来源 |
|------|------|------|---------|
| 背景 | 米色羊皮纸 | `#f4ecd8` | 古代莎草纸 |
| 文本 | 墨黑 | `#1c1917` | 罗马铭文 |
| 主色 | 庞贝红 | `#a8392e` | 罗马壁画 |
| 强调 | 帝国金 | `#b08d2b` | 镀金雕塑 |
| 装饰 | 罗马青 | `#2c3e3a` | 大理石锈斑 |
| 暗紫 | 帝王紫 | `#5a3e5c` | 提尔紫 |

### 3.3 字体

- **Display**: `Cinzel` (Trajan-inspired) — 罗马铭文大写体
- **Body Latin**: `Cormorant Garamond` — 古典衬线
- **Body CN**: `Noto Serif SC` / `Source Han Serif` — 中文衬线
- **Data/Number**: `Cormorant Infant` 或 `EB Garamond`

### 3.4 装饰元素

- 章节数字采用罗马数字 I, II, III, IV, V
- 分隔线采用百合花纹 / 月桂叶 / 简单双线
- 关键数字用衬线字体 + 微下划线（铭文效果）

## 四、两大核心可视化产物

| 产物 | 路径 | 内容 |
|------|------|------|
| 数据洞察看板 | [analysis_output/LLPSI_Insights.html](../analysis_output/LLPSI_Insights.html) | 56 章难度曲线 + 段级推荐 + 点击阅读 |
| 古罗马调性看板 | [analysis_output/LLPSI_Roman_Insights.html](../analysis_output/LLPSI_Roman_Insights.html) | FR/RA 整体走向、主题分布、词性分层 |

### 4.1 数据洞察看板内容

- 56 章节累计词汇增长曲线（FR 1-35 + RA 36-56）
- 56 章节新词密度柱状图（标记陡坡阈值线 23.1% × 1.2 = 27.7%）
- 56 章节详细数据表
- 段级三档推荐（流畅 / 挑战 / 节选）
- 点击推荐项弹出模态窗口展示原文

### 4.2 古罗马调性看板内容

- 词汇增长曲线
- 章节难度热力图
- 词性分层饼图
- FR→RA 过渡分析
- 历史/文化主题分布（战争/政治/宗教/家庭）

---

# 第四部分：读物评估与可读性档案

> 整合自 [reader_audit_report.md](reader_audit_report.md)（原 356 行）
> **数据已大幅更新**：原报告基于 v4.0 "全本聚合"，现 v3.1 段级评分（4670 段）已取代之。本节只保留**至今仍有价值的可读起点框架**与**未被覆盖的关键读物**

## 一、四档可读性分布（替代 CEFR 分级）

| 档位 | 阈值 | 数量（v3.1 段级） | 含义 |
|------|------|----------------:|------|
| 🟢 fluent 流畅 | 已知词覆盖 ≥ 80% | 数百段 | 完成 LLPSI 主线后奖励读物，可通读 |
| 🟡 challenging 挑战 | 已知词覆盖 70-80% | 数千段 | 需配合注释，适合复习扩展 |
| 🔵 selected 节选 | 已知词覆盖 50-70% | 数千段 | 仅适合节选/对照阅读 |
| ⚪ reference 查阅 | < 50% | 少量 | 词汇/语法查阅，拉语含量低 |

## 二、按学习阶段的读物分组（v3.1 实测）

| 阶段 | 章节范围 | 关键读物（首批流畅出现） |
|------|---------|--------------------------|
| FR 入门期 | Cap. 1-15 | Fabellae Latinae、Colloquia Personarum、Ecce Romani I |
| FR 初级期 | Cap. 16-25 | Oxford Latin Course 1、Cambridge Latin Stage 1 |
| FR 中级期 | Cap. 26-35 | Cambridge Latin Stage 2-3、Dooge Beginners |
| RA 高级期 | Cap. 36-45 | Hobbitus Ille、Nutting Reader、Diocles et Flora |
| RA 完成期 | Cap. 46-56 | Pugio Bruti、Via Latina Romanorum（达到 fluent 档） |

## 三、D 类教材拉语段提取（v3.1 取代）

> v3.1 段级评分已直接覆盖该功能（按段而非按 D 类提取段），**无需独立报告**。原始 v4.0 数据保留在 [archived_pre_merge_20260610/reader_audit_report.md](archived_pre_merge_20260610/reader_audit_report.md)。

---

# 第五部分：LLPSI 关键门槛点

> 整合自 [vocabulary_threshold_research.md §五](vocabulary_threshold_research.md) + [Project_Plan.md §1.3](Project_Plan.md)

## 一、关键门槛点（基于词频分析）

| 门槛 | 章节 | 类型 | 影响 |
|:-----|:----:|:-----|:----|
| **第一章墙** | Cap. 1-2 | 入门适应 | 心态 / 基础语法；Tier 0→1 跃迁 |
| **语法墙** *(待验证)* | Cap. 8-9 (FR) | 间接引语 abl. abs. | 语法结构剧变；Tier 1 中段 |
| **间接引语密集** *(待验证)* | Cap. 10-13 (FR) | 关系从句、夺格句型 | 句法复杂度跃迁；Tier 1 末段 |
| **密度墙** | Cap. 25-26 (FR) | 神话专名 / 历史人名 | 词汇量激增；Tier 1→2 关键跃迁 |
| **进阶墙** | Cap. 35-36 (FR→RA) | 罗马史专名 / 修辞 | 跨书跃迁；Tier 2→3 跃迁 |
| **罗马史适应期** | RA Cap. 36-39 | 共和国人物密集 | 词频密度最高 48.9%；Tier 3 高成本段 |
| **高级语法墙** *(待验证)* | RA Cap. 44+ | 复杂修辞 / 间接引语 | 句法结构复杂；Tier 3 末段 |

> ⚠ **标注说明**：标记 *(待验证)* 的行基于社区经验与作者先验判断，**待后续添加句法分析模块验证**（需 POS 标注 + 间接引语 / 关系从句 / 夺格句型 频率统计）。本项目当前仅有 surface-form 词频数据，无句法层数据。

> **本项目的"双脚手架"（语法墙 + 密度墙）精准对应 Tier 1→2 跃迁**，正是 ROI 投入回报最高的区间。

## 二、关键发现：第九章墙是"语法跃迁"非"词汇墙"

| 旧假设 | 数据真相 |
|------|------|
| 「第九章墙」= 第 8-9 章起**生词密度激增** | Cap. 8-13 新词密度稳定在 **22-28%**，未出现统计学意义上的"陡坡"（**词频数据已验证**） |
| 应聚焦于**高密度章节** | 56 章中**仅 Cap. XXV (30.3%)** 越过陡坡阈值（23.1% × 1.2）（**词频数据已验证**） |
| 「第九章墙」= 一个孤立的"墙" | 实际上是 LLPSI 编写者**有意为之的语法跃迁**：从描述性叙事进入间接引语、关系从句、夺格句型（**待后续添加句法分析模块验证**） |

**结论**：必须区分两类"墙"——
- **语法之墙** (Cap. VIII–XIII): 6 章，句法复杂度跃迁。**句法脚手架**。*（待验证）*
- **密度之墙** (Cap. XXV): 1 章，神话专名集中。**词汇脚手架**。✓（词频数据已验证）

**优先章节**: Cap. 8、9、10、11、12、13（语法墙 *待验证*） + Cap. 25（密度墙 ✓） = **7 个优先章节**

## 三、FR → RA 难度跃迁

| 发现 | 含义 | 行动 |
|------|------|------|
| **FR → RA 难度跃迁**：第 35 章 (22.4%) → 第 36 章 (48.9%) | 完成 FR 后立即遭遇罗马史专名爆炸 | 需在 Cap. XXXVI 前提供"RA 适应期"微阅读 |
| **RA 章节普遍更长**：平均 4,209 词 vs FR 的 1,330 词 | 单次阅读量大，需分块 | 段内切分策略 |
| **RA Cap. 36 最高密度 (48.9%)** | 共和国专有名词首次集中爆发 | 优先生成 Cap. 36 微阅读 |
| **RA Cap. 48 最高词数 (8,388 词)** | 罗马帝国扩张史的长篇叙事 | 建议按事件分块阅读 |
| **RA 末章 (Cap. 56) 累计 24,220 词形** | 远超 FR 终值的 11,019 词形 | 词汇量目标比原计划 3,500 词上调 |

---

# 附录：参考文献

## A. 拉丁语教学法

1. **Ørberg, H. H.** *Lingua Latina per se Illustrata* (1991, final version)
2. **Naturmetodens Sproginstitut** — Direct Method systematization
3. **Krashen, S.** Input Hypothesis (i+1)

## B. 词汇覆盖率研究

1. **Nation, I. S. P. (2006)**. *How large a vocabulary is needed for reading and listening?* — 8,000-9,000 词族 (98% 书面)
2. **Schmitt, N., Cobb, T., Horst, M., & Schmitt, D. (2017)**. Replication of van Zeeland & Schmitt (2012), Nation (2006) and Cobb (2007). *Language Teaching*, 50(2), 212–226.
3. **van Zeeland, H., & Schmitt, N. (2013)**. Lexical coverage in L1 and L2 viewing comprehension.
4. **Laufer, B., & Ravenhorst-Kalovski, G. C. (2010)**. Lexical threshold revisited. *Reading in a Foreign Language*, 22(1), 15–30.
5. **Hu, M., & Nation, I. S. P. (2000)**. Unknown vocabulary density and reading comprehension.
6. **Cobb, T. (2007)**. Computing the vocabulary demands of L2 reading.
7. **Xu, J. et al. (2021)**. Vocabulary Learning via Optimal Transport (ACL 2021 Best Paper) — 验证词汇量拐点

## C. Latin 专门研究

8. **Gruber-Miller & Mulligan (2022)**. Latin Vocabulary Knowledge and the Readability of Latin Texts
9. **Hackett Publishing**: Familia Romana 出版说明 (1,800 词汇)
10. **Cambridge Language Teaching**: https://www.cambridge.org/core/journals/language-teaching

## D. 项目数据源

- **OCR 文本**: `ocr_output/<slug>/_full.txt`（71 本读物）
- **已学词汇库**: `analysis_output/learned_words_v2.json`
- **段级评分数据**: `analysis_output/reader_vocab_stats_v6.json`
- **章节推荐表**: `analysis_output/llpsi_reader_routing_v2.json` / `.md`

---

# 版本

- **v1.0** (2026-06-10) — 首次合并。原 6 份文档精挑精华重组成 1 份
- **整合来源**:
  - LLPSI_Research.md（教材本体研究）— 全文保留
  - vocabulary_threshold_research.md（ROI 分层）— 全文保留
  - Project_Plan.md（项目计划）— 仅保留"第九章墙"等仍未过时的发现
  - PRD_VISIO_ROMANA.md（PRD）— 仅保留"古罗马调性设计"
  - Technical_Architecture_VISIO_ROMANA.md（技术架构）— 仅保留"古罗马调性设计"
  - reader_audit_report.md（读物审计）— 已被 v3.1 段级评分取代，仅保留"四档可读性分布"框架

> **备份**: 全部原 6 份文档 + 2 张 PNG 备份至 [archived_pre_merge_20260610/](archived_pre_merge_20260610/)
