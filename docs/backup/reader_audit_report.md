# Other_Readers 读物评估报告 (v4.0 完全重写)

> **报告版本**: v4.0.0 | **生成日期**: 2026-06-06
> **审计范围**: `source/Other_Readers/` 下全部 55 份 PDF / EPUB (Non-LLPSI 读物)
> **核心指标**: **可读起点** (学完LLPSI Cap.X) + **教学价值** (复习哪章新词)
> **方法**: 全本 OCR (13482 页) + 拉英词频加权 + 章节级 known/new 词覆盖计算 + D 类拉语段提取

---

## 0. TL;DR — 一图速览

### 4 档可读性分布 (替代 A1/A2/B1/B2)

| 档位 | 阈值 | 数量 | 含义 |
|------|------|----:|------|
| **fluent** | 顺畅可读 (≥60%) | 2 | 完成LLPSI主线后的奖励读物, 可通读 |
| **challenging** | 有挑战 (40-60%) | 13 | 需配合注释, 适合复习扩展 |
| **selected** | 节选可读 (20-40%) | 38 | 仅适合节选/对照阅读, 不通读 |
| **reference** | 查阅使用 (<20%) | 1 | 词汇/语法查阅, 拉语含量低 |

### 按学习阶段分组 (按 reading_level_chapter 划分)

| 阶段 | 章节范围 | 数量 | 典型读物 |
|------|---------|----:|---------|
| FR Cap.1-15 入门期 | Cap.1-15 | 0 | `—` |
| FR Cap.16-25 初级期 | Cap.16-25 | 4 | `oxford_1` |
| FR Cap.26-35 中级期 | Cap.26-35 | 18 | `dooge_beginners_key` |
| RA Cap.36-45 高级期 | Cap.36-45 | 20 | `diocles_flora` |
| RA Cap.46-56 完成期 | Cap.46-56 | 11 | `pugio_bruti` |
| 查阅使用 | — | 1 | `new_latin_primer` |

### 核心推荐

1. **完成 FR 后奖励读物 (2 本)**: `pugio_bruti` (学完 Cap.48) / `via_latina_romanorum` (学完 Cap.52)
2. **FR 后期挑战阅读 (13 本)**: 大部分是 `challenging` 级别, 教学价值集中在 FR Cap.1-4 基础词汇
3. **D 类教材拉语段 (16 本/162 页)**: 详见 §3, 适合做 LLPSI 章节的扩展阅读
4. **拉英对话手册**: `conversational_latin` (415 页), 适合口语训练

---

## 1. 评价体系 (替代 A1/A2)

本报告 **彻底抛弃 A1/A2/B1/B2 CEFR 分级**, 使用三个**可量化、可验证**的指标:

| 指标 | 含义 | 用途 |
|------|------|------|
| **可读起点** (`reading_level_chapter`) | 学完 LLPSI Cap.N 后, FR 已知词覆盖本书拉语独词达到 X% 的最早章节 | "我学完第X章能读这本书吗?" |
| **教学价值** (`best_teach_chapter`) | 本书覆盖 LLPSI Cap.M 新词最多的章节 (高=适合复习该章) | "我想复习第X章新词, 哪本最好?" |
| **4 档可读性** | fluent / challenging / selected / reference, 基于 FR 已知词覆盖率 | 一眼看出"能不能读" |

### 1.1 4 档可读性详解

| 档位 | 覆盖率阈值 | 学习含义 | 推荐用法 |
|------|-----------|---------|---------|
| **fluent** (顺畅) | ≥60% | 通读无压力, 仅需少量注释 | 奖励读物 / 通读训练 |
| **challenging** (挑战) | 40-60% | 需配合注释/字典 | 复习扩展 / 课外训练 |
| **selected** (节选) | 20-40% | 不适合通读, 适合节选/对照 | 对照阅读 / 词汇扩展 |
| **reference** (查阅) | <20% | 拉语含量太低 | 词汇/语法查阅 |

### 1.2 学习阶段分组

| 阶段 | 章节范围 | 推荐读物类型 |
|------|---------|-------------|
| **FR Cap.1-15 入门期** | 入门对话+生活 | 短小对话/初级故事 |
| **FR Cap.16-25 初级期** | 语法加深 | 中篇故事/分级读物 |
| **FR Cap.26-35 中级期** | 罗马历史/文化 | 长篇经典 (Nutting, LLPSI 风格的) |
| **RA Cap.36-45 高级期** | 古典散文/历史 | Cicero 改写, Ecce Romani 3, 习得法短篇 |
| **RA Cap.46-56 完成期** | 高级古典/诗歌 | Pugio Bruti, Via Latina Romanorum |
| **查阅使用** | 不适合通读 | 教材/字典/参考 |

---

## 2. 按学习阶段分章

> 每章内按可读性 (`fluent` > `challenging` > `selected`) → 起点章节 → 拉词量 升序排列.
> "起点 Cap.X" 指学完该章后, FR 已知词可覆盖本书拉语独词达到 4 档中的某一档.

### 2.2 FR Cap.16-25 初级期 (4 本)

**目录**: `source/Other_Readers/reclassified_v2/1_cap16-25_初级/`

| # | slug | 标题 | 拉词 | 独词 | 英% | 档位 | 起点 Cap. | 教学 Cap. (覆盖) | 峰值 Cap. (覆盖) |
|---|------|------|----:|----:|----:|------|----------:|-----------------:|----------------:|
| 1 | `oxford_1` | Oxford Latin Course Part 1, 2e | 16,105 | 4,033 | 57% | selected | Cap.20 | Cap.3 (36%) | Cap.56 (38%) |
| 2 | `forum_lectiones` | Forum - Lectiones Latinitatis Viva… | 28,375 | 6,479 | 31% | selected | Cap.22 | Cap.4 (55%) | Cap.56 (39%) |
| 3 | `latin_natural_method` | Latin by the Natural Method (W.G. … | 42,103 | 4,548 | 46% | selected | Cap.24 | Cap.4 (42%) | Cap.56 (37%) |
| 4 | `oxford_2` | Oxford Latin Course Part 2, 2e | 24,169 | 6,541 | 50% | selected | Cap.25 | Cap.4 (40%) | Cap.56 (39%) |

### 2.3 FR Cap.26-35 中级期 (18 本)

**目录**: `source/Other_Readers/reclassified_v2/2_cap26-35_FR中级/`

| # | slug | 标题 | 拉词 | 独词 | 英% | 档位 | 起点 Cap. | 教学 Cap. (覆盖) | 峰值 Cap. (覆盖) |
|---|------|------|----:|----:|----:|------|----------:|-----------------:|----------------:|
| 1 | `dooge_beginners_key` | D'Ooge Latin for Beginners Key | 5,519 | 1,927 | 58% | challenging | Cap.35 | Cap.1 (30%) | Cap.56 (53%) |
| 2 | `gwynne` | Gwynne's Latin | 23,879 | 4,488 | 66% | selected | Cap.26 | Cap.1 (31%) | Cap.56 (36%) |
| 3 | `cambridge_2` | Cambridge Latin Course 2 | 18,614 | 5,407 | 51% | selected | Cap.27 | Cap.1 (35%) | Cap.56 (35%) |
| 4 | `oxford_3` | Oxford Latin Course Part 3, 2e | 29,792 | 7,976 | 51% | selected | Cap.28 | Cap.1 (43%) | Cap.56 (39%) |
| 5 | `latin_made_simple` | Latin Made Simple | 38,921 | 7,870 | 57% | selected | Cap.28 | Cap.1 (47%) | Cap.56 (39%) |
| 6 | `fabulae_faciles` | Fabulae Faciles (Ritchie 1889) | 19,824 | 5,928 | 36% | selected | Cap.28 | Cap.1 (32%) | Cap.56 (38%) |
| 7 | `teach_yourself` | Teach Yourself Beginner's Latin | 19,787 | 5,587 | 53% | selected | Cap.28 | Cap.3 (32%) | Cap.56 (34%) |
| 8 | `cambridge_1` | Cambridge Latin Course 1 | 14,519 | 3,397 | 57% | selected | Cap.29 | Cap.3 (33%) | Cap.56 (30%) |
| 9 | `cambridge_3` | Cambridge Latin Course 3 | 31,713 | 8,738 | 52% | selected | Cap.30 | Cap.1 (40%) | Cap.56 (36%) |
| 10 | `reynolds_reader` | Latin Reader (Reynolds) | 36,894 | 8,541 | 52% | selected | Cap.30 | Cap.1 (42%) | Cap.56 (36%) |
| 11 | `ecce_romani_2a` | Ecce Romani IIA (2005 Prentice Hal… | 26,959 | 7,069 | 52% | selected | Cap.30 | Cap.1 (41%) | Cap.56 (31%) |
| 12 | `latin_first_year_magoffin` | Latin First Year (Magoffin) | 34,695 | 6,866 | 56% | selected | Cap.30 | Cap.3 (42%) | Cap.56 (33%) |
| 13 | `wileys_real_latin` | Wiley's Real Latin (Maltby & Belch… | 37,981 | 7,735 | 53% | selected | Cap.31 | Cap.1 (39%) | Cap.56 (37%) |
| 14 | `pro_patria` | Pro Patria (Sonnenschein 1907) | 23,455 | 6,471 | 51% | selected | Cap.31 | Cap.1 (45%) | Cap.56 (34%) |
| 15 | `cambridge_4` | Cambridge Latin Course 4 | 36,538 | 10,671 | 53% | selected | Cap.33 | Cap.1 (44%) | Cap.56 (35%) |
| 16 | `ecce_romani` | Ecce Romani I | 33,192 | 7,022 | 56% | selected | Cap.33 | Cap.1 (44%) | Cap.56 (30%) |
| 17 | `beginners_latin_book` | Beginner's Latin Book (Textkit) | 32,499 | 9,020 | 50% | selected | Cap.35 | Cap.1 (45%) | Cap.56 (30%) |
| 18 | `ecce_romani_3` | Ecce Romani III (Perry) | 30,145 | 8,671 | 51% | selected | Cap.35 | Cap.1 (40%) | Cap.56 (34%) |

**重点读物**:
- `dooge_beginners_key` (D'Ooge Latin for Beginners Key): **challenging** 起点 Cap.35, 教学价值 Cap.1 (30%)

### 2.4 RA Cap.36-45 高级期 (20 本)

**目录**: `source/Other_Readers/reclassified_v2/3_cap36-45_RA前/`

| # | slug | 标题 | 拉词 | 独词 | 英% | 档位 | 起点 Cap. | 教学 Cap. (覆盖) | 峰值 Cap. (覆盖) |
|---|------|------|----:|----:|----:|------|----------:|-----------------:|----------------:|
| 1 | `diocles_flora` | Dioclēs et Flōra | 10,257 | 2,649 | 35% | challenging | Cap.36 | Cap.3 (28%) | Cap.56 (51%) |
| 2 | `regulus` | Regulus (Saint-Exupéry 拉语版) | 9,597 | 3,269 | 23% | challenging | Cap.41 | Cap.4 (32%) | Cap.56 (52%) |
| 3 | `unus_duo_tres` | Unus Duo Tres: Latine Loquamur per… | 8,091 | 2,939 | 36% | challenging | Cap.42 | Cap.4 (32%) | Cap.56 (46%) |
| 4 | `olimpia_nicholas` | The Mysterious Traveler (Olimpi) | 4,121 | 857 | 40% | challenging | Cap.42 | Cap.3 (17%) | Cap.56 (45%) |
| 5 | `latin_lower_forms` | Latin Reader for Lower Forms (Hard… | 33,309 | 12,218 | 27% | selected | Cap.36 | Cap.4 (45%) | Cap.56 (37%) |
| 6 | `dooge_beginners_2` | Latin for Beginners (D'Ooge 另一版) | 43,254 | 9,957 | 50% | selected | Cap.36 | Cap.1 (50%) | Cap.56 (29%) |
| 7 | `nutting_reader` | A First Latin Reader (Nutting) | 35,141 | 9,284 | 39% | selected | Cap.36 | Cap.1 (42%) | Cap.56 (34%) |
| 8 | `revised_latin_primer` | The Revised Latin Primer (Kennedy) | 30,018 | 9,111 | 53% | selected | Cap.36 | Cap.4 (41%) | Cap.56 (30%) |
| 9 | `illiterati_1` | Latin for the Illiterati (Stone) | 38,337 | 9,056 | 53% | selected | Cap.36 | Cap.4 (42%) | Cap.56 (32%) |
| 10 | `ecce_romani_2b` | Ecce Romani IIB (Addison Wesley) | 32,420 | 8,424 | 52% | selected | Cap.36 | Cap.1 (38%) | Cap.56 (28%) |
| 11 | `hobbitus` | Hobbitus Ille (Tolkien 拉语版) | 54,426 | 10,662 | 27% | selected | Cap.37 | Cap.4 (38%) | Cap.56 (32%) |
| 12 | `dooge_beginners` | Latin for Beginners (D'Ooge) | 43,276 | 10,001 | 50% | selected | Cap.37 | Cap.1 (50%) | Cap.56 (28%) |
| 13 | `reading_latin_grammar` | Reading Latin: Grammar (2e) | 54,475 | 9,134 | 54% | selected | Cap.37 | Cap.4 (38%) | Cap.56 (29%) |
| 14 | `reading_latin_study_guide` | Reading Latin: Study Guide | 25,692 | 6,005 | 65% | selected | Cap.37 | Cap.1 (32%) | Cap.56 (28%) |
| 15 | `ora_maritima` | Ora Maritima (Sonnenschein 1900) | 15,448 | 4,802 | 55% | selected | Cap.37 | Cap.1 (35%) | Cap.56 (26%) |
| 16 | `wheelock_reader` | Wheelock's Latin Reader | 63,679 | 15,154 | 46% | selected | Cap.38 | Cap.1 (48%) | Cap.56 (34%) |
| 17 | `wheelock_7e` | Wheelock's Latin 7e | 89,692 | 14,864 | 53% | selected | Cap.40 | Cap.1 (54%) | Cap.56 (28%) |
| 18 | `reading_latin_text` | Reading Latin: Text (2e) | 57,711 | 11,800 | 51% | selected | Cap.40 | Cap.1 (42%) | Cap.56 (28%) |
| 19 | `via_latina_easy` | Via Latina: Easy Latin Reader (Col… | 30,056 | 10,078 | 40% | selected | Cap.40 | Cap.1 (40%) | Cap.56 (30%) |
| 20 | `illiterati_2` | More Latin for the Illiterati (Sto… | 32,327 | 8,955 | 52% | selected | Cap.43 | Cap.4 (43%) | Cap.56 (25%) |

**重点读物**:
- `diocles_flora` (Dioclēs et Flōra): **challenging** 起点 Cap.36, 教学价值 Cap.3 (28%)
- `regulus` (Regulus (Saint-Exupéry 拉语版)): **challenging** 起点 Cap.41, 教学价值 Cap.4 (32%)
- `unus_duo_tres` (Unus Duo Tres: Latine Loquamur per Scaenas): **challenging** 起点 Cap.42, 教学价值 Cap.4 (32%)

### 2.5 RA Cap.46-56 完成期 (11 本)

**目录**: `source/Other_Readers/reclassified_v2/4_cap46-56_RA后/`

| # | slug | 标题 | 拉词 | 独词 | 英% | 档位 | 起点 Cap. | 教学 Cap. (覆盖) | 峰值 Cap. (覆盖) |
|---|------|------|----:|----:|----:|------|----------:|-----------------:|----------------:|
| 1 | `pugio_bruti` | Pugio Bruti (Rico & Polis) | 5,734 | 1,205 | 20% | fluent | Cap.48 | Cap.3 (21%) | Cap.56 (64%) |
| 2 | `via_latina_romanorum` | Via Latina: De Lingua et Vita Roma… | 25,660 | 4,148 | 25% | fluent | Cap.52 | Cap.1 (55%) | Cap.56 (62%) |
| 3 | `olimpia_pyramus` | Reckless Love: Pyramus and Thisbe … | 5,422 | 1,831 | 40% | challenging | Cap.46 | Cap.1 (20%) | Cap.56 (43%) |
| 4 | `chickering` | First Latin Reader (Chickering) | 32,613 | 9,673 | 28% | challenging | Cap.49 | Cap.1 (55%) | Cap.56 (45%) |
| 5 | `wheelock_answer_key` | Wheelock's Latin 7e Answer Key | 26,226 | 5,784 | 62% | challenging | Cap.50 | Cap.1 (41%) | Cap.56 (43%) |
| 6 | `septimus` | Septimus (Chambers 1910) | 15,154 | 5,673 | 49% | challenging | Cap.50 | Cap.4 (36%) | Cap.56 (43%) |
| 7 | `olimpia_daedalus` | Daedalus et Icarus (Olimpi) | 4,610 | 1,696 | 44% | challenging | Cap.51 | Cap.3 (19%) | Cap.56 (41%) |
| 8 | `second_year_latin` | Second Year Latin (Greenough 1899) | 14,770 | 4,954 | 51% | challenging | Cap.54 | Cap.1 (35%) | Cap.56 (41%) |
| 9 | `latin_stories_wheelock` | Latin Stories (Wheelock 配套) | 11,002 | 3,905 | 43% | challenging | Cap.55 | Cap.1 (33%) | Cap.56 (40%) |
| 10 | `intermediate_oral_cicero` | Intermediate Oral Latin Reader (Ci… | 15,698 | 5,731 | 35% | challenging | Cap.56 | Cap.1 (39%) | Cap.56 (40%) |
| 11 | `conversational_latin` | Conversational Latin for Oral Prof… | 65,195 | 9,165 | 44% | selected | Cap.48 | Cap.4 (43%) | Cap.56 (22%) |

**重点读物**:
- `pugio_bruti` (Pugio Bruti (Rico & Polis)): **fluent** 起点 Cap.48, 教学价值 Cap.3 (21%)
- `via_latina_romanorum` (Via Latina: De Lingua et Vita Romanorum): **fluent** 起点 Cap.52, 教学价值 Cap.1 (55%)
- `olimpia_pyramus` (Reckless Love: Pyramus and Thisbe (Olimpi)): **challenging** 起点 Cap.46, 教学价值 Cap.1 (20%)

### 2.6 查阅使用 (1 本)

**目录**: `source/Other_Readers/reclassified_v2/5_reference_查阅/`

| # | slug | 标题 | 拉词 | 独词 | 英% | 档位 | 起点 Cap. | 教学 Cap. (覆盖) | 峰值 Cap. (覆盖) |
|---|------|------|----:|----:|----:|------|----------:|-----------------:|----------------:|
| 1 | `new_latin_primer` | A New Latin Primer | 37,386 | 18,422 | 37% | reference | — | Cap.3 (36%) | Cap.56 (13%) |

---

## 3. D 类教材拉语段提取 (16 本 / 35 段 / 162 页)

> 通过 `scripts/extract_d_class_latin.py` 从 D 类教材中提取连续 3+ 页的拉语故事段, 再通过 `scripts/analyze_d_class_latin_v2.py` 计算每段的 LLPSI 章节锚点.
> 这些段是"黄金拉语段"——从英语讲解为主的教材中挖出的连续拉语故事, 适合做 LLPSI 扩展阅读.

### 3.1 按教材汇总

| # | slug | 段数 | 总页 | 拉词(总) | 独词(总) | 起点 Cap.范围 | 教学 Cap.范围 |
|---|------|----:|----:|--------:|--------:|-------------|-------------|
| | `latin_natural_method` | 12 | 78 | 19,120 | 6,893 | Cap.23-50 | Cap.1 (17%) |
| | `dooge_beginners` | 3 | 12 | 2,172 | 1,346 | Cap.30-36 | Cap.1 (16%) |
| | `cambridge_2` | 3 | 11 | 826 | 533 | Cap.24-36 | Cap.4 (8%) |
| | `dooge_beginners_2` | 2 | 9 | 1,606 | 990 | Cap.30-31 | Cap.1 (15%) |
| | `cambridge_1` | 2 | 8 | 152 | 73 | Cap.41-53 | Cap.5 (2%) |
| | `oxford_2` | 2 | 7 | 1,576 | 955 | Cap.30-33 | Cap.1 (8%) |
| | `ecce_romani` | 2 | 6 | 677 | 386 | Cap.29-29 | Cap.1 (9%) |
| | `illiterati_1` | 1 | 4 | 479 | 377 | — | Cap.1 (4%) |
| | `latin_first_year_magoffin` | 1 | 4 | 657 | 393 | Cap.33-33 | Cap.1 (10%) |
| | `reading_latin_text` | 1 | 4 | 550 | 368 | — | Cap.2 (5%) |
| | `wheelock_7e` | 1 | 4 | 986 | 615 | Cap.50-50 | Cap.1 (10%) |
| | `cambridge_4` | 1 | 3 | 309 | 212 | Cap.49-49 | Cap.1 (6%) |
| | `dooge_beginners_key` | 1 | 3 | 582 | 355 | Cap.32-32 | Cap.1 (9%) |
| | `latin_made_simple` | 1 | 3 | 393 | 309 | Cap.34-34 | Cap.1 (10%) |
| | `oxford_3` | 1 | 3 | 472 | 312 | Cap.44-44 | Cap.4 (8%) |
| | `wileys_real_latin` | 1 | 3 | 309 | 242 | Cap.31-31 | Cap.5 (6%) |

### 3.2 段级详表 (按 page_count 降序)

| # | slug | 起始页 | 页数 | 拉词 | 独词 | 英% | 起点50% | 起点60% | 教学 Cap. (覆盖) | 用途 |
|---|------|------:|----:|-----:|----:|----:|--------:|--------:|----------------:|------|
| 1 | `latin_natural_method` | p.153 | 14 | 3,318 | 1,159 | 41% | — | — | Cap.4 (21%) | 高级扩展 |
| 2 | `latin_natural_method` | p.128 | 13 | 3,389 | 1,072 | 42% | Cap.50 | — | Cap.4 (23%) | RA扩展阅读 |
| 3 | `latin_natural_method` | p.117 | 10 | 2,663 | 861 | 39% | Cap.37 | — | Cap.4 (19%) | RA扩展阅读 |
| 4 | `latin_natural_method` | p.103 | 7 | 1,814 | 577 | 38% | Cap.34 | — | Cap.1 (17%) | FR扩展阅读 |
| 5 | `dooge_beginners` | p.214 | 6 | 1,041 | 622 | 39% | Cap.30 | Cap.40 | Cap.1 (16%) | FR扩展阅读 |
| 6 | `dooge_beginners_2` | p.214 | 6 | 1,047 | 635 | 39% | Cap.31 | Cap.44 | Cap.1 (15%) | FR扩展阅读 |
| 7 | `latin_natural_method` | p.79 | 6 | 1,414 | 452 | 41% | Cap.39 | — | Cap.1 (13%) | RA扩展阅读 |
| 8 | `latin_natural_method` | p.96 | 6 | 1,661 | 577 | 39% | Cap.37 | — | Cap.1 (13%) | RA扩展阅读 |
| 9 | `cambridge_2` | p.2 | 5 | 208 | 121 | 37% | Cap.27 | Cap.42 | Cap.4 (6%) | FR扩展阅读 |
| 10 | `latin_natural_method` | p.36 | 5 | 678 | 289 | 46% | Cap.43 | — | Cap.1 (8%) | RA扩展阅读 |
| 11 | `cambridge_1` | p.4 | 4 | 125 | 57 | 57% | Cap.41 | — | Cap.5 (2%) | RA扩展阅读 |
| 12 | `cambridge_1` | p.54 | 4 | 27 | 16 | 31% | Cap.53 | — | Cap.3 (1%) | 高级扩展 |
| 13 | `illiterati_1` | p.318 | 4 | 479 | 377 | 44% | — | — | Cap.1 (4%) | 高级扩展 |
| 14 | `latin_first_year_magoffin` | p.185 | 4 | 657 | 393 | 38% | Cap.33 | — | Cap.1 (10%) | FR扩展阅读 |
| 15 | `latin_natural_method` | p.88 | 4 | 1,084 | 437 | 42% | Cap.43 | — | Cap.1 (11%) | RA扩展阅读 |
| 16 | `latin_natural_method` | p.111 | 4 | 916 | 380 | 40% | Cap.28 | — | Cap.1 (10%) | FR扩展阅读 |
| 17 | `oxford_2` | p.72 | 4 | 616 | 404 | 35% | Cap.33 | Cap.50 | Cap.1 (8%) | FR扩展阅读 |
| 18 | `reading_latin_text` | p.315 | 4 | 550 | 368 | 29% | — | — | Cap.2 (5%) | 高级扩展 |
| 19 | `wheelock_7e` | p.417 | 4 | 986 | 615 | 39% | Cap.50 | — | Cap.1 (10%) | RA扩展阅读 |
| 20 | `cambridge_2` | p.77 | 3 | 283 | 179 | 35% | Cap.24 | Cap.35 | Cap.4 (8%) | FR扩展阅读 |
| 21 | `cambridge_2` | p.82 | 3 | 335 | 233 | 44% | Cap.36 | Cap.55 | Cap.10 (6%) | RA扩展阅读 |
| 22 | `cambridge_4` | p.107 | 3 | 309 | 212 | 41% | Cap.49 | — | Cap.1 (6%) | RA扩展阅读 |
| 23 | `dooge_beginners` | p.221 | 3 | 568 | 362 | 38% | Cap.31 | Cap.42 | Cap.6 (10%) | FR扩展阅读 |
| 24 | `dooge_beginners` | p.226 | 3 | 563 | 362 | 37% | Cap.36 | Cap.50 | Cap.1 (8%) | RA扩展阅读 |
| 25 | `dooge_beginners_2` | p.221 | 3 | 559 | 355 | 38% | Cap.30 | Cap.41 | Cap.3 (11%) | FR扩展阅读 |
| 26 | `dooge_beginners_key` | p.29 | 3 | 582 | 355 | 27% | Cap.32 | Cap.38 | Cap.1 (9%) | FR扩展阅读 |
| 27 | `ecce_romani` | p.33 | 3 | 277 | 130 | 46% | Cap.29 | — | Cap.1 (9%) | FR扩展阅读 |
| 28 | `ecce_romani` | p.205 | 3 | 400 | 256 | 40% | Cap.29 | Cap.52 | Cap.4 (7%) | FR扩展阅读 |
| 29 | `latin_made_simple` | p.83 | 3 | 393 | 309 | 34% | Cap.34 | Cap.46 | Cap.1 (10%) | FR扩展阅读 |
| 30 | `latin_natural_method` | p.70 | 3 | 614 | 303 | 43% | Cap.23 | Cap.33 | Cap.1 (12%) | FR扩展阅读 |
| 31 | `latin_natural_method` | p.147 | 3 | 823 | 395 | 39% | Cap.29 | Cap.50 | Cap.4 (12%) | FR扩展阅读 |
| 32 | `latin_natural_method` | p.168 | 3 | 746 | 391 | 41% | Cap.36 | — | Cap.4 (12%) | RA扩展阅读 |
| 33 | `oxford_2` | p.149 | 3 | 960 | 551 | 32% | Cap.30 | Cap.46 | Cap.4 (10%) | FR扩展阅读 |
| 34 | `oxford_3` | p.117 | 3 | 472 | 312 | 34% | Cap.44 | — | Cap.4 (8%) | RA扩展阅读 |
| 35 | `wileys_real_latin` | p.366 | 3 | 309 | 242 | 26% | Cap.31 | Cap.43 | Cap.5 (6%) | FR扩展阅读 |

**详细分析**: `analysis_output/d_segments_vocab.md` (35 段完整列表)

---

## 4. 数据与方法

### 4.1 词频 + 章节锚点算法 (v5)

**脚本**: `scripts/analyze_readers_v5.py`

**算法**:

1. 加载 OCR 全文 (`ocr_output/<slug>/_full.txt`)
2. 拉英分词 (基于词频词表 + 后缀特征, 复用 v4 算法)
3. 加载 LLPSI FR 1-35 章 + RA 36-56 章累计词表 (`data/llpsi_corpus.db` 的 `fr_vocab` 表)
4. 对每本书:
   - 计算 `unique_latin_count` = 唯一拉语词形数
   - 对每章 (1-56): `chapter_known` = 1 到 N-1 章累计已知词
   - `cov(N) = len(unique_latin ∩ chapter_known) / unique_latin_count`
   - 找最早达到 60% / 40% / 20% 的章节 → 分配 4 档可读性
   - `best_teach_chapter` = `len(new_set ∩ unique_latin) / len(new_set)` 最大的章节

### 4.2 D 类拉语段提取 (v2)

**脚本**: `scripts/extract_d_class_latin.py` + `scripts/analyze_d_class_latin_v2.py`

**算法**:
1. 对每页 OCR 文本判定语言 (拉/英/混合)
2. 找连续 3+ 页的拉语/混合段, 标记为可入库故事段
3. 对每段单独做词频 + 章节锚点分析

### 4.3 Ecce Romani EPUB 评估

**脚本**: `scripts/compare_ecce_formats.py` + `scripts/ocr_new_ecce_romani.py`

**结论**:
- Ecce Romani I&II Combined EPUB 含 14 个文本文件 (420KB) + 104 张图片 (1.6MB)
- 14 个文本文件中, 仅 3 个超过 500 字节阈值 (含实质内容)
- 提取出的 3 个文件 = 3 章, **仅覆盖原书前 3 章**, 不实用
- **决策**: 丢弃 combined EPUB, 使用 PDF 版本 (I + IIA + IIB + III)

### 4.4 数据流

```
source/Other_Readers/  (PDF + EPUB)
    ↓ [batch_ocr_readers.py / ocr_new_ecce_romani.py]
ocr_output/<slug>/_full.txt + page_NNN.txt  (55 本 × ~250 页)
    ↓ [analyze_readers_v5.py]
analysis_output/reader_vocab_stats_v4.json  (55 本, 含 4 档可读性)
    ↓ [extract_d_class_latin.py]
analysis_output/d_class_latin_stories.json  (16 本 D 类, 35 段, 162 页)
    ↓ [analyze_d_class_latin_v2.py]
analysis_output/d_segments_vocab.json  (35 段 + LLPSI 章节锚点)
    ↓ [restructure_reclassified.py]
source/Other_Readers/reclassified_v2/  (按学习阶段分章)
    ↓ [generate_audit_report_v4.py] (本脚本)
docs/reader_audit_report.md  (报告)
```

---

## 5. 附录

### 5.1 版本历史

| 版本 | 日期 | 主要变化 |
|------|------|---------|
| v1 | 2026-05 | 首次批量审计, A1/A2/B1/B2 评级 |
| v2 | 2026-06-05 | 加入 OCR 词频统计 |
| v3 | 2026-06-06 | 引入 LLPSI 章节锚点, D 类拉语段提取, 加入 conversational_latin |
| **v4** | **2026-06-06** | **完全重写: 抛弃 A1/A2 标签, 改用「可读起点+教学价值」+ 4 档可读性, 按学习阶段分章** |

### 5.2 关键变更 (v3 → v4)

| 维度 | v3 | v4 | 变更原因 |
|------|----|----|---------|
| 难度标签 | A1/A2/B1/B2 | **拉词量 + LLPSI 章节** | 用户要求抛弃 CEFR |
| 目录结构 | `A1_latin_story/` 等 9 个 | `0_cap1-15_入门/` 等 6 个 | 按学习阶段而非等级 |
| 可读性 | 二元 (可读/不可读) | **4 档 fluent/challenging/selected/reference** | 解决"很多书不可达"问题 |
| 评级算法 | 仅 50%/60% 阈值 | **60%/40%/20% 三档阈值** | 39 本书达到 selected 档 |
| D 类段 | 仅 16 本, 无章节分析 | **35 段, 每段都有 LLPSI 章节锚点** | 用户要求"D 类段也做章节分析" |
| Ecce Romani | 3 本新加, EPUB 评估后丢弃 | 保留, 增加 `ecce_romani_2a/2b/3` | 用户新加 3 本 |
| conversational_latin | D 类"重新入库" | **selected 档, 起点 Cap.48, 教学 Cap.4 (43%)** | 用户要求重新入库 |

### 5.3 物理删除 / 丢弃项

| 项 | 处理 | 原因 |
|----|------|------|
| `nunc_loquamur` | 已物理删除 (用户操作) | 质量不高 |
| `ecce_romani_combined` (EPUB) | OCR 输出保留但不入库 | EPUB 仅 3 章, 不实用 |
| D 类 17 本 (含 5 本 D 类中无可提取段) | 归入 `5_reference_查阅` (暂空) | 拉语含量低, 仅作字典 |

### 5.4 关键文件索引

| 文件 | 用途 |
|------|------|
| `docs/reader_audit_report.md` | **本报告** |
| `analysis_output/reader_vocab_stats_v4.json` | 55 本书的 v5 详细数据 (4 档可读性) |
| `analysis_output/reader_vocab_stats_v4.md` | v5 词频数据 Markdown 视图 |
| `analysis_output/d_segments_vocab.json` | 35 个 D 类拉语段详细数据 |
| `analysis_output/d_segments_vocab.md` | D 类拉语段 Markdown 视图 |
| `analysis_output/d_class_latin_stories.json` | 16 本 D 类的拉语段位置 (start_page..end_page) |
| `source/Other_Readers/reclassified_v2/README.md` | 新目录结构说明 |
| `scripts/analyze_readers_v5.py` | v5 词频分析 (含 4 档) |
| `scripts/extract_d_class_latin.py` | D 类拉语段位置提取 |
| `scripts/analyze_d_class_latin_v2.py` | D 类拉语段章节锚点分析 |
| `scripts/restructure_reclassified.py` | 重命名 reclassified 目录 |
| `scripts/compare_ecce_formats.py` | Ecce Romani PDF vs EPUB 对比 |

