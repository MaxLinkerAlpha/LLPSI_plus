---
name: vocab-constrained-story
version: v1_0_0
created: 2026-06-30
status: active
description: |
  严格词汇约束的拉丁语故事生成器。用于 Cap.1-10 词汇稀少的低章节阶段。
  强制只使用 ≤ 目标章节的词元（lemma_chapter_map ≤ N），通过排比/重复扩充篇幅，
  自动调用 evaluate_v2.py --file 验证 85% 分位 ≤ 目标+2。
trigger_keywords:
  - "重写短篇"
  - "低章节故事"
  - "严格词汇"
  - "vocab constrained"
  - "Cap.1-10 重写"
related_files:
  - AI_reader/rewrite_cap1.py (Cap.1 重写实战)
  - AI_reader/rewrite_cap3.py (Cap.3 重写实战，含失败修复)
  - difficulty_algorithm/evaluate_v2.py (难度评估)
  - difficulty_algorithm/vocab_by_chapter/cap{N}_vocab_clean.json (允许词表)
---

# Vocab-Constrained Story — 严格词汇模式故事生成器

## 适用场景

- **Cap.1-10 重写任务**（每章 ≤ 200 词元可用）
- 当 STRATEGY.md §1.2 的"自由发挥"模式命中率 < 10% 时
- 需要保证 v2_level ≤ 目标+2 的硬约束

## 与 STRATEGY.md §1.2 默认模式的区别

| 维度 | 默认（自由发挥） | 严格词汇（本 skill） |
|------|-----------------|---------------------|
| 词源约束 | 软约束（≤15% 超纲） | 硬约束（≤5% 超纲，仅专名） |
| 篇幅扩充 | 自然扩展 | 强制排比/重复 |
| 命中率（Cap.1-5） | 4% | 100% |
| 适合章节 | Cap.10+ | Cap.1-10 |
| 故事自然度 | 高 | 中（可能稍僵硬） |

## 工作流程

### Step 1: 加载允许词表

```python
import json
from pathlib import Path

def load_vocab(target_chapter: int) -> set:
    allowed = set()
    for n in range(1, target_chapter + 1):
        path = Path(f"difficulty_algorithm/vocab_by_chapter/cap{n}_vocab_clean.json")
        with open(path) as f:
            allowed.update(json.load(f))
    return allowed
```

### Step 2: 黑名单（已知超章节词）

预定义每章禁用的常见超章节词，生成时主动避免：

```python
# Cap.1-5 通用禁用动词（实际章节 > 5）
BANNED_VERBS = {
    "ambulō": 6, "natō": 10, "legō": 18, "redeō": 15, "exspectō": 7,
    "imperō": 8, "iubeō": 8, "interrogō": 7, "parō": 30, "salūtō": 7,
    "exclāmō": 12, "timeō": 6, "gaudeō": 8, "tollō": 13, "cōnspiciō": 18,
}

# 禁用专有名词（章节 > 5）
BANNED_PROPER_NOUNS = {
    "Quīntus": 13, "Graecus": 46, "Crēta": 5,  # 慎用
    "Asia": 14, "Gallia": 18, "Germania": 19, "Aegyptus": 19,
}

# 禁用普通名词
BANNED_NOUNS = {
    "domus": 19, "cibus": 9, "panis": 9, "mare": 10, "nox": 13,
    "terra": 9, "laetus": 6, "omnis": 14, "semper": 16, "nunc": 13,
}
```

### Step 3: 生成故事（带 OOV 检测）

```python
def generate_story(target_chapter, story_meta, llm_or_human) -> str:
    allowed = load_vocab(target_chapter)
    draft = llm_or_human.generate(story_meta, vocab_constraint=list(allowed))

    # 自动 OOV 扫描
    oov = find_oov(draft, target_chapter)
    if oov:
        # 反馈给 LLM/作者重写
        print(f"  OOV ({len(oov)}): {oov[:10]}")
        return None
    return draft
```

### Step 4: 算法验证（必须通过 v2_level ≤ target+2）

```bash
python difficulty_algorithm/evaluate_v2.py --file AI_reader/realitates/Cap{N}/<file>.md --json
```

判定：
- `v2_rate >= 85%` AND `v2_level <= target+2` → PASS
- 否则 → 反馈 OOV 词列表，进入 Step 3 重写循环

## 篇幅扩充模板

按 §1.2 默认模式生成的基础稿往往只有 100-200 词，需要扩充到目标长度。**严格词汇**模式下用以下模板（**5 个经过实战验证**）：

### 模板 1: 重复核心句（最稳）

```
Rōma est magna. Italia est magna. Hispānia est magna.
Sicilia est magna. Sardinia est magna. Trēs terrae magnae.
```

**适用**: 地理介绍、人物描写
**扩展效率**: 每条 +20-30 词

### 模板 2: 排比结构

```
Trēs terrae: Italia, Graecia, Hispānia.
Trēs īnsulae: Sicilia, Sardinia, Britannia.
Trēs flūmina: Tiberis, Rhēnus, Dānuvius.
```

**适用**: 列举主题
**扩展效率**: 每条 +30-50 词

### 模板 3: 问答对话体

```
Ubi est Rōma? Rōma est in Italiā.
Estne Rōma in Graeciā? Rōma nōn est in Graeciā.
Ubi est Italia? Italia est in Eurōpā.
```

**适用**: Cap.1 地理介绍
**扩展效率**: 每条 +50-100 词

### 模板 4: 反转/对比

```
Tiberis est parvus — sed Rōmānus.
Rhēnus est magnus — sed nōn Rōmānus.
Dānuvius est magnus — sed nōn Rōmānus.
```

**适用**: 加深度
**扩展效率**: 每条 +20-40 词

### 模板 5: 感官细节

```
Rosae sunt rubrae. Līlia sunt alba. Aqua est clara.
Hortus est pulcher. Hortus est magnus. Hortus est bonus.
```

**适用**: 抒情/描写（Cap.5+）
**扩展效率**: 每条 +30-50 词

## 实战案例

### 案例 1: Cap.1 Quattuor populi → Quattuor familiae
- **问题**: populus 在 Cap.1 词表里，但 "Quattuor populi" 与 Cap.4+ 词汇冲突
- **修复**: 改为 "Quattuor familiae"（familia 在 Cap.1）
- **效果**: v2_rate 100%

### 案例 2: Cap.3 Pater meus nōn est → Pater meus abest
- **问题**: 原文用 mortuus（Cap.10+）, ambulō（Cap.6）, exspectāvī（Cap.7+）
- **修复**: 标题改为 "abest"（Cap.5），删除 ambulō，保留 exspectō（Cap.7 可接受）
- **效果**: v2_level=3, v2_rate=95%

### 案例 3: Cap.3 Quid est iūstum → Quid est bonum
- **问题**: iūstus 在 Cap.31，标题直接导致 v2_level=5+
- **修复**: 改为 bonum（Cap.5），调整主题为伦理讨论
- **效果**: v2_level=4, v2_rate=92%

## 工具/参考

- `difficulty_algorithm/evaluate_v2.py --file` — 算法验证（v2_4_0+ 支持 .md 直读）
- `difficulty_algorithm/lemma_chapter_map.json` — 词元章节映射
- `difficulty_algorithm/vocab_by_chapter/cap{N}_vocab_clean.json` — 各章允许词表
- `Lesson.md L04` — Cap.1-5 重写实战经验

## 版本

- v1_0_0 (2026-06-30): 初始版本，基于 Cap.1-5 重写实战经验
