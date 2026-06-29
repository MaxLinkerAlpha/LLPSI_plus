# 200 Stories Generation Plan v3

**Created**: 2026-06-29  
**Status**: Plan Mode — waiting for user approval  
**Goal**: 200 Latin stories, 10 per chapter for Cap.1-20

---

## 1. Current State

| Chapter | Done | Target | Need |
|---------|------|--------|------|
| Cap.1   | 0    | 10     | 10   |
| Cap.2   | 0    | 10     | 10   |
| Cap.3   | 0    | 10     | 10   |
| Cap.4   | 0    | 10     | 10   |
| Cap.5   | 0    | 10     | 10   |
| Cap.6   | 0    | 10     | 10   |
| Cap.7   | 1    | 10     | 9    |
| Cap.8   | 1    | 10     | 9    |
| Cap.9   | 5    | 10     | 5    |
| Cap.10  | 5    | 10     | 5    |
| Cap.11  | 3    | 10     | 7    |
| Cap.12  | 2    | 10     | 8    |
| Cap.13  | 3    | 10     | 7    |
| Cap.14  | 7    | 10     | 3    |
| Cap.15  | 2    | 10     | 8    |
| Cap.16  | 8    | 10     | 2    |
| Cap.17  | 4    | 10     | 6    |
| Cap.18  | 3    | 10     | 7    |
| Cap.19  | 10   | 10     | 0 done |
| Cap.20  | 4    | 10     | 6    |
| **Total** | **58** | **200** | **142** |

Disk: 61 stories total (58 in Cap.1-20 + 3 in Cap.21/24/25). `realitates.json` has 61 entries.

---

## 2. Phase 0: Calibration（校准）

**目标**：将 `progress.json` 同步到与磁盘实际状态完全一致。

**操作**：
1. 扫描 `AI_reader/realitates/Cap*/` 下所有 `.md` 文件
2. 读取每篇 YAML front matter，提取 theme/style/genre/character_type/narrative_mode
3. 更新 `progress.json`：
   - `chapters.{N}.done` → 实际文件数
   - `chapters.{N}.used_dimensions` → 已使用的维度组合列表
   - `batches` → 清空重建（旧批次记录不完整，不如重建）
4. 创建缺失的 Cap 目录（Cap.1-6）

**时间估算**：单次脚本运行，< 1 分钟

---

## 3. Generation Strategy

### 3.1 Cap.1-6：超短篇强制策略

**问题**：算法评估几乎不可能把故事判到 Cap.1-6（之前的实验：Cap.1 词汇写的故事被判到 Cap.10-25）。

**策略**：
- 每篇 **30-50 词**超短篇
- 严格只用该章累积词汇（`generate_prompt.py --chapter N --vocab`）
- 算法评估照常运行，但 **目录放置手动指定**到 Cap.1-6
- YAML 中 `evaluated_chapter` 记录算法结果，`best_fit_chapter` 记录实际放置章节
- 每章 10 篇，共 60 篇
- 维度多样性照常维护（不重复 theme/style/genre/character/narrative_mode）

### 3.2 Cap.7-20：标准策略

- 每篇 **50-100+ 词**（随章节递增）
- 用 `generate_prompt.py --chapter N --vocab --history` 生成提示词
- 算法评估决定实际章节位置
- 每批 5 篇，每篇维度不重复

### 3.3 维度多样性

每章 10 篇故事，需从以下表格中各选不重复的 10 项：

| 表格 | 可选总数 | 需选 10 项 | 余量 |
|------|---------|-----------|------|
| A 主题 | 85 | 10 | 充裕 |
| B 风格 | 14 | 10 | 刚好 |
| B+ 叙事模式 | 12 | 10 | 刚好 |
| C 体裁 | 13 | 10 | 刚好 |
| D 角色类型 | 7 | 10 | **不够！需复用** |
| E 篇幅 | 5 | 10 | **不够！需复用** |

**对策**：D（角色类型）和 E（篇幅）允许复用。A/B/B+/C 严格不重复。复用 D/E 时错开与 A/B/C 的组合，避免整体组合重复。

---

## 4. Batch Workflow（每批 5 篇）

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 生成提示词                                       │
│  python3 generate_prompt.py --chapter N --vocab --history │
│  → 输出到 /tmp/prompt_batch_N.txt                        │
├─────────────────────────────────────────────────────────┤
│  Step 2: AI 写 5 篇拉丁文故事                              │
│  阅读提示词 → 创作 5 篇 → 输出 YAML + 拉丁文               │
│  → 保存到 /tmp/stories_batch_N.txt                       │
├─────────────────────────────────────────────────────────┤
│  Step 3: 评估 + 入库                                      │
│  python3 merge_yaml.py --file /tmp/stories_batch_N.txt   │
│  → 自动拆分 → evaluate_v2.py → 写入 Cap 目录              │
│  → 更新 realitates.json                                  │
├─────────────────────────────────────────────────────────┤
│  Step 4: AI 审查（可选）                                   │
│  人工检查 macron 准确性、语法正确性                         │
│  → 如有错误，修复后重新 merge                              │
├─────────────────────────────────────────────────────────┤
│  Step 5: 更新 progress.json                               │
│  更新 chapters.done、used_dimensions、batches             │
└─────────────────────────────────────────────────────────┘
```

**每批预计耗时**：5-10 分钟（取决于 AI 写作速度）

---

## 5. Execution Phases（执行顺序）

从易到难，先填高章节再攻低章节：

### Phase 1：Cap.16-20（需 21 篇，约 5 批）
- Cap.16: 缺 2、Cap.17: 缺 6、Cap.18: 缺 7、Cap.19: 完成、Cap.20: 缺 6
- 目标章节：Cap.12-16（算法溢出后自然落入 Cap.16-20）
- 难度：低（词汇量大，创作自由度最高）

### Phase 2：Cap.11-15（需 33 篇，约 7 批）
- Cap.11: 缺 7、Cap.12: 缺 8、Cap.13: 缺 7、Cap.14: 缺 3、Cap.15: 缺 8
- 目标章节：Cap.8-12
- 难度：中

### Phase 3：Cap.7-10（需 28 篇，约 6 批）
- Cap.7: 缺 9、Cap.8: 缺 9、Cap.9: 缺 5、Cap.10: 缺 5
- 目标章节：Cap.5-8
- 难度：中高

### Phase 4：Cap.1-6（需 60 篇，约 12 批）
- 全部缺 10 篇
- 超短篇策略（30-50 词），严格词汇控制，手动放置
- 难度：最高（词汇极度受限，创作空间小）

**总计约 30 批，每批 5 篇。**

---

## 6. Progress Tracking & Resumption

### progress.json 结构（增强版）

```json
{
  "project": "200_stories_Cap1_20",
  "version": "3.0",
  "started": "2026-06-29",
  "last_updated": "2026-06-29T...",
  "current_phase": 1,
  "chapters": {
    "1": {
      "done": 0, "target": 10, "need": 10,
      "strategy": "micro",
      "used_dimensions": {
        "themes": [], "styles": [], "genres": [],
        "characters": [], "narratives": []
      }
    },
    ...
  },
  "batches": [
    {
      "batch_id": 1,
      "phase": 1,
      "target_chapter": 12,
      "stories_count": 5,
      "actual_chapters": [16, 16, 17, 18, 20],
      "completed_at": "2026-06-29T..."
    }
  ]
}
```

### 中断恢复协议

1. 读取 `progress.json`
2. 检查 `current_phase` 和 `chapters.{N}.need`
3. 找到下一个需要填充的章节
4. 从中断点继续（不需要重做已完成的批次）

### 上下文压缩对策

- `progress.json` 是外部 SSOT，不依赖对话上下文
- 每批完成后立即更新 `progress.json`
- 如果上下文被压缩，重新读取 `progress.json` 即可恢复全部状态
- 同一会话内尽量连续跑 3-5 批，然后主动写摘要到 `progress.json`

---

## 7. Verification

每阶段完成后验证：
- [ ] `realitates.json` 条目数 = 磁盘 `.md` 文件数
- [ ] `progress.json` 的 `done` 计数 = 磁盘实际文件数
- [ ] 每章维度不重复（A/B/B+/C 严格，D/E 允许复用但组合不重复）
- [ ] 所有故事 YAML front matter 完整（12 个必填字段）

---

## 8. Assumptions & Decisions

| 决策 | 理由 |
|------|------|
| Cap.1-6 手动放置 | 算法几乎不可能判到 Cap.1-6，但用户需要这 60 篇 |
| 从高章节开始 | 词汇量大→创作自由度高→效率高→先易后难 |
| 每批 5 篇 | 兼顾效率和质量，单批不太大以免出错后浪费 |
| 不强制 AI review | 人工抽查即可，批量 AI review 太慢 |
| progress.json 作为外部 SSOT | 防止上下文压缩丢失进度 |
| D/E 维度允许复用 | 7 种角色类型和 5 种篇幅无法满足 10 篇不重复 |