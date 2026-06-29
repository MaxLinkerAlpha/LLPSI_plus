# 200 Stories 续跑计划 v4

**Created**: 2026-06-29
**Status**: Plan Mode — waiting for user approval
**Goal**: 续跑 200 篇 LLPSI 故事（Cap.1-20 各 10 篇），考虑上下文压缩与长时中断

---

## 1. 关键发现（探索阶段）

### 1.1 真实进度（progress.json + 磁盘双源核对）

| 来源 | Cap.1-20 总计 | 说明 |
|------|--------------|------|
| progress.json `done` 求和 | 82 | 含 Cap.9=5（疑似虚高）和 Cap.19=15（疑似低估） |
| `realitates.json` Cap.1-20 条目 | 78 | 不含 Cap.9（Cap.9 目录下 5 个文件以 `Cap1_` 开头） |
| 磁盘 `realitates/Cap*/` 真实文件数 | 91（含 Cap.21-29） | Cap.1-6 全空，Cap.9 有 5 个错命名文件 |

**Cap.1-20 实际状态**（取 `realitates.json` 为准）：

| Cap | 已生成 | 需补 | 备注 |
|-----|--------|------|------|
| 1-6 | 0 | 60 | 全部为空，Cap.1-6 目录已创建 |
| 7 | 1 | 9 | |
| 8 | 1 | 9 | |
| 9 | 5 | 5 | 磁盘有 5 个 `Cap1_*.md` 文件（错命名），暂不动 |
| 10 | 5 | 5 | |
| 11 | 4 | 6 | |
| 12 | 2 | 8 | |
| 13 | 6 | 4 | |
| 14 | 9 | 1 | |
| 15 | 2 | 8 | |
| 16 | 10 | **0（已满）** | |
| 17 | 7 | 3 | |
| 18 | 9 | 1 | |
| 19 | 16 | 0（超额 6） | 超额篇数可视为"超量库存" |
| 20 | 6 | 4 | |
| **合计** | **85** | **115** | 200 目标还差 115 篇 |

**progress.json 数据失真**：
- Cap.9 记录 done=5 但 realitates 无 Cap.9 记录
- Cap.19 记录 done=15 但 realitates 有 16 条
- `batches` 数组只记录了 3 批（实际已跑 6+ 批）

**结论**：第一件事必须跑 `calibrate_progress.py` 重建真实状态。

### 1.2 流水线脚本能力摘要

| 脚本 | 版本 | 关键能力 | CLI 标志 |
|------|------|---------|---------|
| `generate_prompt.py` | v1_6_0 | 生成完整 AI 提示词（模板 + 词表 + 语法 + 历史排除） | `-c`, `-o`, `-V` vocab, `-G` grammar, `-H` history, `-s` show-history |
| `merge_yaml.py` | v2_11_0 | 拆分 → 评估 → AI审查（可选）→ 合并 → 写文件 → 更新索引 → OOV日志 | `-f`, `-o`, `--review`, `--review-ai-command` |
| `evaluate_v2.py` | v2_3_0 | 难度评估（85% 分位数，simplemma 还原） | `--text`, `--json`, `--name` |
| `calibrate_progress.py` | 无版本 | 扫描磁盘 → 重建 progress.json | 无参数 |

**关键约束**：
- 一次只跑 1 个 generate_prompt + 1 个 merge_yaml（前一个必须等后一个返回）
- 但 AI 创作 + 评估 + 审查环节可与 IO 操作并行
- 词表超大（Cap.34 ≈ 84KB），与 `--output` 同时使用 prompt 极长
- 每批 5 篇最稳，1 篇失败不影响其他

### 1.3 中断风险评估

| 风险 | 概率 | 后果 | 对策 |
|------|------|------|------|
| 上下文压缩 | 高（5+ 批后必发生） | 丢失批次细节 | progress.json 是 SSOT |
| 长时任务被中止 | 中 | 写到一半的批次丢失 | 每批写完即落盘 |
| AI 调用超时 | 中 | 提示词半截 | 重发即可，generate_prompt 是确定性的 |
| 评估失败（OOV=0） | 低 | 该篇跳过 | merge_yaml 已有 `continue` 处理 |
| Cap.9 文件错命名 | 已存在 | progress.json 与磁盘不一致 | 校准时单独处理 |

---

## 2. 执行阶段（6 阶段，1 MVP + 4 主力 + 1 收尾）

### Phase 0：校准（必须最先做）
1. 跑 `python3 calibrate_progress.py`
2. 对比校准前后 progress.json
3. Cap.9 的 5 个 `Cap1_*.md` 文件：检查 YAML front matter → 决定保留（视作 Cap.9 库存）还是重命名
4. 校准后写一份"快照"到文档（仅当有意外）

### Phase 1 MVP：Cap.17 续跑 3 篇
- 目标：补 Cap.17（need=3）+ 顺手补 Cap.18（need=1）+ Cap.20（need=4）
- 实际：跑 1 批 5 篇，target=Cap.17
- 验证：进度正常后再开 Phase 2

### Phase 2：Cap.16-20 收尾（高章节）
- 缺口：Cap.17=3, Cap.18=1, Cap.20=4，共 8 篇
- 需要 2 批（5+5），其中一批可顺便填 Cap.19（虽然满额但可作"超量"）
- target=Cap.18-20，词汇约束最松，创作最快

### Phase 3：Cap.11-15（中章节）
- 缺口：Cap.11=6, Cap.12=8, Cap.13=4, Cap.14=1, Cap.15=8，共 27 篇
- 需要 6 批（每批 5 篇 = 30，多 3 篇给 Cap.12/Cap.15）
- target=Cap.12-15
- 中等难度，prompt 词表约 30-50KB

### Phase 4：Cap.7-10（低章节）
- 缺口：Cap.7=9, Cap.8=9, Cap.9=5（暂不动错命名文件）, Cap.10=5，共 28 篇
- 需要 6 批
- target=Cap.8-10，词表 5-15KB，创作空间小

### Phase 5：Cap.1-6（超短篇强制策略）
- 缺口：Cap.1-6 各 10，共 60 篇
- 需要 12 批
- 每篇 30-50 词超短篇，严格只用 `cap{N}_vocab_clean.json`
- 算法判到 Cap.10+ 没关系，**手动放置**到目标章
- YAML front matter 增字段：`evaluated_chapter: 算法判定`, `best_fit_chapter: 实际放置章`

**总批次数：1+2+6+6+12 = 27 批 × 5 篇 = 135 篇**
**当前已有 85 篇（Cap.1-20 范围），需新生成 115 篇 = 23 批**
**余量 12 篇可在 Phase 5 给 Cap.1-6 各 1-2 篇超量**

---

## 3. 每批标准工作流（5 步）

```
Step 1: 生成提示词
  python3 generate_prompt.py --chapter N --vocab --history --output /tmp/prompt_N.txt

Step 2: AI 创作
  阅读 /tmp/prompt_N.txt → 创作 5 篇 → 输出 YAML+正文 → /tmp/stories_N.txt

Step 3: 入库（评估+合并+写盘+索引）
  python3 merge_yaml.py --file /tmp/stories_N.txt
  → 自动 evaluate_v2.py → 写 Cap 目录 → 更新 realitates.json

Step 4: 人工抽查（每 2 批 1 次）
  - 抽查 1-2 篇的 YAML 字段完整性
  - 检查长音（macron）准确性
  - 抽查词汇是否在 cap{N}_vocab_clean.json 范围内

Step 5: 更新 progress.json
  - chapters.{N}.done += 实际入库数
  - chapters.{N}.need = target - done
  - used_dimensions 新增 5 个维度
  - batches 追加新批次记录
```

**每批 5 篇预计耗时**：3-5 分钟（不含人工抽查）

---

## 4. 上下文压缩与中断恢复协议

### 4.1 外部 SSOT（Single Source of Truth）

**`progress.json` 是唯一可信源**：
- 重新打开会话时，第一步：`Read /Users/max/Downloads/Projects/LLPSI_plus/AI_reader/progress.json`
- 根据 `chapters.{N}.need` 找到下一个缺口
- 根据 `batches[].target_chapter` 找到上一批的目标章节
- 直接续跑，无需重读历史

### 4.2 每批落盘清单

每完成 1 批必须立即更新 3 个文件：
1. `AI_reader/realitates/Cap{N}/*.md` — 5 个新故事（merge_yaml 自动写）
2. `AI_reader/realitates.json` — 索引追加（merge_yaml 自动写）
3. `AI_reader/progress.json` — 进度推进（人工写）

**这三者必须同步**。任一缺失都视为该批未完成。

### 4.3 主动摘要（每 3 批）

每完成 3 批，主动写一份简短摘要到对话（仅 200 字内）：
- 已完成 X 批，剩余 Y 批
- 下一批目标章节 Z
- 当前 phase 进度 N/M
- 是否有异常

### 4.4 中断后的"快速重启"指令模板

如果上下文被压缩，新会话第一句应该是：
> "继续跑 200 故事任务。先 Read progress.json，告诉我下一批应该跑哪个章节。"

我会读取 progress.json → 找到 next batch → 直接开跑。

### 4.5 单批隔离

每批 5 篇的输出文件命名：`/tmp/stories_batch_{batch_id}.txt`
- 即使 AI 中途崩溃，提示词已落盘
- 重新读 `/tmp/prompt_batch_{batch_id}.txt` 即可续创作
- 已入库的批次永不重跑（`calibrate_progress.py` 会跳过已有）

---

## 5. 风险与对策

| 风险 | 对策 |
|------|------|
| Cap.9 错命名文件 | 校准后决定：保留（视为 Cap.9 库存，5 篇够 10 篇的一半）或重命名到 Cap.9 |
| 算法把 Cap.1-6 故事判到 Cap.10+ | 手动放置，YAML 增 `evaluated_chapter` / `best_fit_chapter` 字段（merge_yaml 暂不支持，需先扩展或后期批量改 YAML） |
| 词表超出 token 限制 | Cap.7+ 词表 ≤ 30KB，可控；Cap.6 词表 8KB，没问题 |
| 5 篇中 1 篇评估失败 | merge_yaml 自动 skip，4 篇入库 |
| 同章 5 篇主题撞车 | `--history` 强制排除已用维度 |
| `merge_yaml.py` 写入失败 | 文件名冲突时自动递增 _NNN |

### 5.1 Cap.1-6 特殊处理（待评估）

`merge_yaml.py` 当前会用**算法判定章节**覆盖 `target_chapter`。这意味着 Cap.1-6 故事写完后，merge_yaml 会把它们放到 Cap.10+ 目录，而不是 Cap.1-6。

**两种解决方案**：
- **方案 A（推荐）**：写一个小脚本 `relocate_story.py`，把 merge_yaml 写错位置的故事从 Cap.N 移到 Cap.M，并更新 realitates.json 和 progress.json
- **方案 B**：扩展 `merge_yaml.py` 增加 `--force-chapter M` 参数，让 AI 生成的 YAML 中带 `target_chapter: 1`，merge_yaml 跳过算法覆盖

**第一阶段先采用方案 A**（更稳，不动核心代码）。`relocate_story.py` 大约 30 行 Python。

---

## 6. 验收标准

每阶段结束验证：

- [ ] `realitates.json` 条目数 = 磁盘 `realitates/Cap1-20/*.md` 文件数
- [ ] `progress.json` `done` 计数 = 磁盘实际文件数
- [ ] 每章 done = 10
- [ ] 每章 A/B/B+/C 维度不重复
- [ ] 所有故事 YAML 12 字段完整（含 `evaluated_chapter`、`best_fit_chapter` for Cap.1-6）
- [ ] `batches[]` 记录 ≥ 23 批

**最终交付**：200 篇 `.md` 故事，分布在 `realitates/Cap1` 到 `realitates/Cap20`，每章正好 10 篇。

---

## 7. 关键决策汇总

| 决策 | 理由 |
|------|------|
| 先校准再开跑 | progress.json 数据失真，不校准会乱套 |
| 每批 5 篇 | 1 篇失败不影响其他，比 10 篇更稳 |
| Cap.1-6 方案 A（relocate 脚本） | 不动 merge_yaml.py 核心，1 个 30 行脚本搞定 |
| Cap.9 错命名文件暂不处理 | 5 篇已够，超量可丢；命名错误不影响阅读 |
| phase 顺序：高 → 中 → 低 → 极低 | 词汇量越大创作越自由，先易后难 |
| 每 3 批主动摘要 | 减少上下文压力，方便用户介入 |
| progress.json 是唯一 SSOT | 上下文压缩后能 100% 恢复 |

---

## 8. 待用户确认

1. **Cap.9 错命名文件**如何处理？
   - A. 保留（视作 Cap.9 库存，剩 5 篇）
   - B. 重命名为 `Cap9_*.md`
   - C. 暂时不动

2. **是否需要"先 Cap.16-20 收尾 → 跑 Cap.11-15 → 跑 Cap.7-10 → 跑 Cap.1-6"这种从高到低的顺序？**还是希望从 Cap.1 开始（虽然更难）？

3. **是否需要 AI 审查（`--review`）每批？**目前人工抽查已足够，但加上 AI 审查会更稳（多 2-3 分钟/批）。
