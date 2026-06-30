# 清理与继续执行计划

## 当前状态

| 目录 | 文件数 | 目标 | 旧文件残留 | 状态 |
|------|--------|------|-----------|------|
| Cap.3 | 10 | 10 (6中篇+4中长篇) | 0 | 已完成 |
| Cap.4 | 18 | 14 (8中篇+6中长篇) | 4 | 需清理+验证 |
| Cap.5 | 10 | 10 (6中篇+4中长篇) | 0 | 待验证 |

Stage 0 准备工作：
- `realitates_tierlist.jsonl`：尚未创建
- `progress.json` 中 `rewrite_phase` 字段：尚未添加

## 执行步骤

### Step 1: 清理 Cap.4 旧文件

删除 4 个残留旧文件（与 rewrite_cap4.py 当前脚本中的标题冲突）：

- `Cap4_Quattuor_populī_medius_01.md`（旧版标题"四族"，当前为"Quattuor_familiae 四家"）
- `Cap4_Quattuor_flūmina_medius_02.md`（旧版标题"四条河"，当前为"Quattuor_aquae 四水"）
- `Cap4_Puer_et_liber_medius_06.md`（旧版标题"男孩与书"，当前为"Puer_et_hortus 男孩与花园"）
- `Cap4_Puer_et_piscis_longior_12.md`（旧版标题"男孩与鱼"，当前为"Puer_et_amīcus 男孩与朋友"）

### Step 2: 运行难度验证

对 Cap.4 和 Cap.5 现有故事文件运行 `evaluate_v2.py` 验证，确认哪些通过、哪些失败。

### Step 3: 修复 Cap.4 失败故事

根据验证结果，修复未通过的故事（target: v2_level ≤ 6）。参考 `Cap4_Cap5_rewrite_plan.md` 中已列出的禁用词替换表。

### Step 4: 完成 Stage 0 准备工作

- 创建 `realitates_tierlist.jsonl`（列出所有故事文件的篇幅、难度等元数据）
- 在 `progress.json` 中新增 `rewrite_phase` 字段

### Step 5: 验证 Cap.5 故事

确保 Cap.5 的 10 篇故事通过难度验证（v2_level ≤ 7）。

## 注意事项

- 清理前先备份 Cap.4 目录（用户要求）
- 不修改 `rewrite_cap4.py` 和 `rewrite_cap5.py` 的清理逻辑（那是后续优化问题）
- 验证通过即视为完成，无需重新生成