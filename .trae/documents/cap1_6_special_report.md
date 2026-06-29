# Cap.1-6 特殊定制报告

**Created**: 2026-06-29
**Status**: 留档待后续会话处理
**Related**: 200_stories_plan_v3.md（Phase 4）

---

## 1. 问题陈述

LLPSI Cap.1-6 是入门阶段，词汇极少（Cap.1 仅 158 词，其中大量 OCR 残片）。计划中要生成 60 篇 Cap.1-6 故事（每章 10 篇），但实际生成 5 批次（25 篇）后，仅 1 篇（4%）落入 Cap.1-6 范围。其余 96% 全部溢出到 Cap.10+，其中多数溢出到 Cap.16+。

**目标**：Cap.1-6 各 10 篇 = 60 篇
**现状**：1 篇 Cap.2，0 篇其余 = 缺口 59 篇

---

## 2. 实验结果（5 批 25 篇）

| 批次 | 目标 | 策略 | 实际命中章节 | Cap.1-6 命中 |
|------|------|------|------------|------------|
| 13 | Cap.1 | 5 篇混合（4 故事 + 1 对话列举） | 2, 9, 27, 10, 16 | **1** (Cap.2) |
| 14 | Cap.3 | 5 篇正常短篇（含具体动词） | 20, 16, 26, 17, 32 | 0 |
| 15 | Cap.4 | 5 篇混合（2 对话 + 3 正常） | 16, 17, 20, 28, 27 | 0 |
| 16 | Cap.5 | 5 篇混合（2 极简 + 3 抒情） | 29, 19, 28, 22, 16 | 0 |
| 17 | Cap.1 | 5 篇**极端专名**（20-30 词，纯罗马地理） | 13, 10, 13, 10, 14 | 0 |

**关键发现**：
- **唯一命中**：batch 13 第 1 篇"Quid est in Eurōpā?"（42 词，对话列举罗马地理名）
- **失败模式**：
  - 用 familia/anus/iuvenis/senex → Cap.20+（这些是 Cap.5+ 词汇）
  - 用 ambulō/portō/videō → Cap.15+（这些是 Cap.5+ 动词）
  - 写任何"故事性"内容必溢出 Cap.10+
- **专名策略的副产品**：5 篇 100% 落入 Cap.10-14，**高效补 Cap.7-15 缺口**！

---

## 3. 根因分析

### 3.1 算法下限问题
`evaluate_v2.py` 的核心逻辑：
- 85% unique lemmas 必须在 Cap.1-N 之内
- 算法用 85th percentile lemma 决定章节
- 故事越短，少数高级词的影响越大（5 个 Cap.20+ 词在 30 词中 = 17% 占比，但只算 1 个 lemma）

### 3.2 Cap.1-3 真实可用词汇极少

**Cap.1**（158 词 clean，但去 OCR 残片后约 50 个真实词）：
- 罗马/希腊地理名：Roma, Italia, Graecia, Gallia, Hispānia, Britannia, Africa, Asia, Aegyptus, Syria, Germania, Rhenus, Danuvius, Tiberis, Oceanus, Europa, Sicilia, Sardinia, Corsica, Creta, Brundisium, Tusculum, Latium, Sparta, Chios, Rhodos, Samos, Lemnos, Naxus, Lesbos, Euboea, Insula
- 基础判断词：est, sunt, non, et, in, ubi, sed, magnus, parvus, multus, unus, duo, tres, mille
- **可数动词：0 个**（amare/ire/venire/videre/audire 等都是 Cap.3+）

**Cap.2-3** 累计 377 词，新增少量动词（esse, habere）和基础名词（puer, senex, vir, femina, māter, pater, porta, casa, via, mōns, silva），但仍无"故事性"动词（ambulō, portō, fugiō, quaerō, etc.）。

**Cap.4-6** 累计 758 词，开始有"故事性"动词（ambulō, intrō, exeō, redeō, dīcō, rogō, respondeō, audiō, videō, portō, ferō, veniō），但这些动词**已经是 Cap.5-6 才学**。

### 3.3 AI 写作倾向
即使明确告知"只用 Cap.1-N 词汇"，AI 倾向：
- 写有故事性的句子（带动作动词）
- 使用"自然叙事"风格（混合判断句和动作句）
- 避免"机械列举"（纯 X est Y 句式）

**结果**：AI 总是溢出 Cap.6+。

---

## 4. 候选解决方案

### 方案 A：prompt 强约束（推荐 · 中等工作量）
**思路**：在 `generate_prompt.py` 末尾追加"硬约束段"，明确要求：
- 只用 Cap.1-N 词表内的词形
- 句式限于：X est Y / X sunt Y / X est in Y / Estne X Y / X non est Y
- 不能用任何动词（Cap.5+ 才有具体动词）
- 30-50 词超短篇

**实现**：
1. 在 `STRATEGY.md` 中新增 `§3.5 Cap.1-6 超短篇专章`
2. 修改 `generate_prompt.py` 接受 `--micro` 标志，追加极简指令
3. 调 `merge_yaml.py` 添加 `--target-chapter` 强制覆盖 target_chapter

**预期效果**：命中率 60-80%

### 方案 B：人工校准（最直接但最慢）
**思路**：让 AI 自由写（接受溢出），评估后**人工**用 sed/cp 命令把 Cap.7-15 中"风格 + 词汇最简单"的故事搬到 Cap.1-6 目录。

**实现**：
1. 写 `relocate_story.py` 工具：
   - 输入：目标章节（如 Cap.1）+ 故事文件
   - 操作：移动文件到 Cap.1，更新 YAML 的 `best_fit_chapter` 字段
   - 更新 `realitates.json` 和 `progress.json`

**预期效果**：直接且可控，但 60 篇需要 60 次手动操作

### 方案 C：词表+算法联合约束（最彻底 · 工作量大）
**思路**：
1. 用 `vocab_clean.py` 重新清洗 Cap.1-6 词表（去除 OCR 残片）
2. 写 `micro_story_generator.py` 专用工具：
   - 输入：目标章节 N
   - 加载 Cap.1-N 真实可用词表
   - 强制从词表随机抽取名词+主语，生成 30-50 词 X est Y 句型
3. 不依赖 AI（确定性生成）

**预期效果**：100% 命中，但故事性差（机械列举）

### 方案 D：降低 Cap.1-6 目标
**思路**：现实接受 Cap.1-6 极难命中，把目标调整为：
- Cap.1-3: 各 5 篇（30 篇）
- Cap.4-6: 维持 10 篇（30 篇）
- 实际只需 30 篇 Cap.1-6

**实现**：修改 `200_stories_plan_v3.md` 计划

**预期效果**：工作减半，剩余 30 篇仍有困难但可解

---

## 5. 推荐路径

**短期**（本次会话）：
- 不再尝试 Cap.1-6
- 专注跑 5-10 批"极端专名策略"填 Cap.7-15 缺口（每批 5 篇，10 分钟）
- 预计本会话可补 25-50 篇 Cap.7-15 缺口

**中期**（下次会话）：
- 实施方案 A（prompt 强约束）解决 Cap.1-6
- 估计 3-5 批（20-30 篇 Cap.1-6）

**长期**：
- 若需要高质量 Cap.1-6 故事，方案 C（自动化工具）值得投入

---

## 6. 关键文件状态（截至 2026-06-29 02:45）

- `progress.json`: 5 个 batch 记录，Cap.1-6: 1/60, Cap.7-15: 47/100
- `realitates.json`: 116 个条目（实际 121 个文件，5 个未索引）
- `oov_corrections.jsonl`: 已累积约 20 条 OOV 记录

---

## 7. 备查清单

- [ ] 实施方案 A（修改 generate_prompt.py 加 --micro 标志）
- [ ] 创建 `micro_story_generator.py`（方案 C）
- [ ] 创建 `relocate_story.py`（方案 B 辅助）
- [ ] 重新清洗 Cap.1-6 词表（vocab_clean.py）
- [ ] 在 STRATEGY.md 加 §3.5 Cap.1-6 超短篇专章
