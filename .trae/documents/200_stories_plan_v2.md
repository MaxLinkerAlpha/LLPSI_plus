# 200 篇故事批量生成计划 v2

> 更新日期：2026-06-29
> 状态：Plan Mode — 等待用户批准后执行

---

## 一、当前状态（已确认）

34 篇成品故事分布在 Cap.1-20 范围内。各章节实际数量：

| 章节 | 已有 | 目标 | 尚缺 |
|------|------|------|------|
| Cap.1 | 0 | 10 | 10 |
| Cap.2 | 0 | 10 | 10 |
| Cap.3 | 0 | 10 | 10 |
| Cap.4 | 0 | 10 | 10 |
| Cap.5 | 0 | 10 | 10 |
| Cap.6 | 0 | 10 | 10 |
| Cap.7 | 1 | 10 | 9 |
| Cap.8 | 1 | 10 | 9 |
| Cap.9 | 5 | 10 | 5 |
| Cap.10 | 1 | 10 | 9 |
| Cap.11 | 1 | 10 | 9 |
| Cap.12 | 1 | 10 | 9 |
| Cap.13 | 1 | 10 | 9 |
| Cap.14 | 2 | 10 | 8 |
| Cap.15 | 0 | 10 | 10 |
| Cap.16 | 5 | 10 | 5 |
| Cap.17 | 3 | 10 | 7 |
| Cap.18 | 1 | 10 | 9 |
| Cap.19 | 8 | 10 | 2 |
| Cap.20 | 4 | 10 | 6 |

**合计：尚缺 166 篇。**（34 批 × 5 篇 = 170 篇，含 4 篇冗余）

---

## 二、核心风险与应对

| 风险 | 应对 |
|------|------|
| **上下文压缩** | progress.json 是唯一真相源。每批完成后立即更新。新会话读此文件即可恢复。 |
| **多天中断** | 每批 5 篇是独立原子操作。任一批完成后中断，下次从下一批继续。 |
| **质量失控** | 每批必经评估+审查+修复三步。不跳过。 |
| **维度重复** | generate_prompt.py --history 自动追踪已用维度，同章不重复。 |
| **算法溢出** | 低章词汇生成的故事会被算法归入高章，这是预期行为（方案C）。 |

---

## 三、执行前准备（Step 0）

**只需做一次：**

1. 更新 `progress.json`，将各章的 `done` 字段同步为实际文件数（见上表）
2. 清空旧的 `batches` 记录，重新开始计数
3. 验证：`ls AI_reader/realitates/Cap{N}/ | wc -l` 与 progress.json 一致

---

## 四、批量流水线（每批 5 篇，约 20-25 分钟）

每批执行的固定步骤：

```
Step A: 生成 Prompt
  python AI_reader/generate_prompt.py --chapter {N} --vocab --history --output /tmp/prompt_batch_{X}.txt

Step B: AI 写 5 篇故事
  将 prompt 发给 AI，AI 输出 5 篇完整故事（含 YAML front matter）
  保存到 /tmp/stories_batch_{X}.md

Step C: 评估难度
  python difficulty_algorithm/evaluate_v2.py --file /tmp/stories_batch_{X}.md

Step D: 合并 YAML + 入库
  python AI_reader/merge_yaml.py --file /tmp/stories_batch_{X}.md --eval-result /tmp/eval_batch_{X}.json

Step E: AI 审查（人工）
  抽查每篇的长音、用词、语法，修复错误

Step F: 更新索引
  progress.json 更新对应章节的 done 计数
  追加 batch 记录
```

**注意**：merge_yaml.py 会自动将故事按算法评估结果放入正确章节，并更新 realitates.json。

---

## 五、执行顺序

从低章到高章，每次 target 当前最缺的章节：

```
Phase 1:  Cap.1-5   (50 篇，10 批) — 全部空白，优先填充
Phase 2:  Cap.6-10  (46 篇，10 批) — Cap.9 已有 5 篇
Phase 3:  Cap.11-15 (45 篇， 9 批) — 多数章节零星已有
Phase 4:  Cap.16-20 (25 篇， 5 批) — Cap.16/19/20 接近满
```

**每个 Phase 内，按章节号从小到大执行。** 例如 Phase 1：先 target Cap.1 生成 10 篇（2 批），再 target Cap.2 生成 10 篇，以此类推。

**算法溢出处理**：target Cap.1 的故事可能被算法归入 Cap.7-19，这是正常的。继续 target Cap.1 直到 Cap.1 实际有 10 篇，或所有低章词汇组合已穷尽。

---

## 六、断点恢复协议

新会话开始时：

```
1. cat AI_reader/progress.json          # 读进度
2. ls AI_reader/realitates/Cap{N}/ | wc -l  # 抽查几个章节验证
3. 找到下一个 need > 0 的章节，从该章继续
4. 如果当前批次中断（Step C/D 中途），检查 /tmp/ 下临时文件
```

---

## 七、每批完成后的验证清单

- [ ] `ls AI_reader/realitates/Cap{N}/ | wc -l` 与预期一致
- [ ] progress.json 已更新
- [ ] realitates.json 条目数增加 5
- [ ] 抽查 1 篇：YAML 字段完整、拉丁语无明显错误
- [ ] 确认本批 5 篇的维度（主题/风格/题材/角色/叙事）互不相同

---

## 八、文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `AI_reader/progress.json` | 更新 | 每批后更新 done 计数和 batch 记录 |
| `AI_reader/realitates/Cap{N}/*.md` | 新建 ~166 个 | 故事文件 |
| `AI_reader/realitates.json` | 更新 | merge_yaml.py 自动维护 |
| `/tmp/prompt_batch_{X}.txt` | 临时 | 每批 prompt，可清理 |
| `/tmp/stories_batch_{X}.md` | 临时 | 每批 AI 输出，可清理 |

---

## 九、不做的优化

- **不新建脚本**：progress.json 手动维护，避免过度工程化
- **不自动清理 /tmp**：每轮工作完成后询问用户是否清理
- **不并行生成**：串行批处理，每批 5 篇，保证质量和可控性
- **不预设维度分配表**：generate_prompt.py --history 自动追踪，无需手写 200 行表格

---

## 十、时间预估

- 每批 5 篇：约 20-25 分钟（含 AI 生成 + 评估 + 审查 + 修复）
- 34 批总计：约 11-14 小时
- 建议分多天执行，每天 5-8 批