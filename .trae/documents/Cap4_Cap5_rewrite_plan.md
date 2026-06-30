# Cap.4 + Cap.5 重写 + Stage 0 准备 执行计划

> 版本: v1\_0\_0 | 创建: 2026-06-30 | 状态: 待批准

***

## 背景

Cap.4 有 9/14 篇重写故事验证失败（v2\_level 远超目标 6），Cap.5 尚未开始，Stage 0 准备工作也未做。

### 失败根因

9 篇故事使用了大量章节 >6 的词汇，如 `terra`(9), `volo`(8), `tibi`(14), `nihil`(14), `amor`(19), `vita`(29), `populus`(32), `graecus`(46), `lego`(18) 等。这些词在拉丁语中很常见，但在 LLPSI 教材中引入较晚，拉高了难度评级。

### 成功模式（5 篇通过的故事）

* Cap.1-2 词汇占 50-60%（主力）

* Cap.3-4 词汇占 20-30%

* Cap.5-6 词汇占 10-15%

* 几乎不用 Cap.7+ 词汇

* OOV 词汇仅限于专有名词（人名地名）

***

## 执行顺序

```
Stage 0.1 (git 备份) ──┐
Stage 0.2 (清单文件)  ──┤── 并行执行
Stage 0.3 (进度追踪)  ──┘
         │
         ▼
Stage 1A: 修复 Cap.4 的 9 篇失败故事
         │
         ▼
Stage 1B: 创建 Cap.5 重写脚本（10 篇）
         │
         ▼
最终验证 + git commit
```

***

## Stage 0: 准备工作

### 0.1 Git 备份

```bash
cd /Users/max/Downloads/Projects/LLPSI_plus
git add AI_reader/realitates/
git commit -m "backup: realitates before Cap.4/5 rewrite"
```

### 0.2 创建 realitates\_tierlist.jsonl

遍历 `realitates/CapN/` 所有 .md 文件，提取 YAML 元数据，输出一行一个 JSON 对象到 `AI_reader/realitates_tierlist.jsonl`。

### 0.3 新增 rewrite\_phase 字段

在 `AI_reader/progress.json` 中添加 `rewrite_phase` 字段追踪各阶段进度。

***

## Stage 1A: 修复 Cap.4（9 篇）

### 词汇约束

* 目标章节: 4，容忍度: +2，即 v2\_level ≤ 6

* 仅使用 lemma\_chapter\_map 中章节 ≤6 的词汇

### 关键禁用词及替换方案

| 禁用词         | 原章节 | 替换方案                                   |
| ----------- | --- | -------------------------------------- |
| terra       | 9   | 用具体地名（Italia, Graecia）或 oppidum/insula |
| volo/vis    | 8   | 用 amat/habet 或换说法                      |
| tibi        | 14  | 用 te 或换说法                              |
| nihil       | 14  | 用 nullum 或 non...ullum                 |
| amor        | 19  | 用动词 amat                               |
| vita        | 29  | 用 aqua 或换说法                            |
| populus     | 32  | 用 viri 或具体族名                           |
| graecus     | 46  | 用 OOV 专有名词 Graecus                     |
| lego/legere | 18  | 用 videt litteras 或 discit              |
| nunc        | 13  | 用 iam                                  |
| semper      | 16  | 省略或用重复句式                               |
| deus        | 10  | 用专有名词（Iuppiter 等）                      |
| mare        | 10  | 用 aqua magna                           |
| flumen      | 10  | 用 fluvius（Cap.1 安全词）                   |
| caput       | 11  | 用 primum oppidum                       |
| dives       | 19  | 用 multam pecuniam habet                |
| pauper      | 23  | 用 pecuniam non habet                   |

### 9 篇故事逐一策略

1. **cap4\_01 Quattuor populi**（中篇）— 四族对比，用简单词描述各族特征
2. **cap4\_02 Quattuor flumina**（中篇）— 四条河，用 fluvius 替代 flumen
3. **cap4\_04 Decem provinciae**（中篇）— 十省，省名作为 OOV 专有名词可接受
4. **cap4\_06 Puer et liber**（中篇）— 男孩与书，用 videt litteras 替代 legit
5. **cap4\_09 Filius improbus**（中长篇）— 坏儿子悔改，情感用简单词表达
6. **cap4\_10 Pecunia patris**（中长篇）— 富父贫子，用"有钱/没钱"替代"富/穷"
7. **cap4\_11 Dominus et servus**（中长篇）— 主奴同行，回避 Graecus/animus 等
8. **cap4\_12 Puer et piscis**（中长篇）— 男孩与鱼，回避 deus/mare 等
9. **cap4\_14 Puella et aqua**（中长篇）— 瑙西卡与奥德修斯，回避 amor/deus 等

### 实施方式

直接编辑 `AI_reader/rewrite_cap4.py`，替换 9 篇故事的 STORIES 条目，然后运行验证。

***

## Stage 1B: 创建 Cap.5 重写脚本

### 词汇约束

* 目标章节: 5，容忍度: +2，即 v2\_level ≤ 7

* 比 Cap.4 多出 Cap.7 词汇可用（amicus, lacrima, teneo 等）

### 10 篇分配（6 中篇 + 4 中长篇）

| #  | 原文件                      | 标题     | 篇幅  |
| -- | ------------------------ | ------ | --- |
| 1  | Qui dormit               | 谁在睡觉？  | 中篇  |
| 2  | Via ad oppidum           | 通往城镇之路 | 中篇  |
| 3  | In horto                 | 在花园里   | 中篇  |
| 4  | Mater et filia in horto  | 母女在花园  | 中篇  |
| 5  | Femina sola              | 孤独的女人  | 中篇  |
| 6  | Filius discit            | 儿子学习   | 中篇  |
| 7  | Ancilla et domina        | 女奴与女主人 | 中长篇 |
| 8  | Villa Romana             | 罗马庄园   | 中长篇 |
| 9  | Servus et rosa           | 奴隶与玫瑰  | 中长篇 |
| 10 | Pater et filius in horto | 父与子在花园 | 中长篇 |

### 实施方式

创建新文件 `AI_reader/rewrite_cap5.py`，参照 `rewrite_cap4.py` 的格式。

***

## 验证步骤

1. 运行 `python3 rewrite_cap4.py`，确认 14/14 PASS
2. 运行 `python3 rewrite_cap5.py`，确认 10/10 PASS
3. 抽查 2-3 篇拉丁文质量
4. 确认旧 brevis 文件已自动清理
5. git commit 保存进度

