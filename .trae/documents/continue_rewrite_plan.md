# 继续重写任务 — 执行计划

> 版本: v1_0_0 | 创建: 2026-06-30 | 基于: 437_short_rewrite_plan.md

---

## 1. 当前状态总览

| 章节 | 状态 | 旧brevis | 新medius | 新longior | 备注 |
|------|------|----------|----------|-----------|------|
| Cap.1 | 已完成 | 已清理 | 6 | 3 | — |
| Cap.2 | 已完成 | 已清理 | 6 | 4 | — |
| Cap.3 | 已完成 | 已清理 | 5 | 5 | 实际5+5，计划书要求6+4（偏差±1，可接受） |
| Cap.4 | 待验证修复 | 14个残留 | 8 | 6 | 新文件已生成但旧brevis未删除（验证未全通过） |
| Cap.5 | 未开始 | 10个 | 0 | 0 | rewrite_cap5.py 尚未创建 |

---

## 2. 执行步骤

### 步骤1：清理 Cap.4 旧 brevis 文件

**操作**：删除 `/Users/max/Downloads/Projects/LLPSI_plus/AI_reader/realitates/Cap4/` 下所有 `*_brevis_*.md` 文件（共14个）。

**理由**：新文件（8 medius + 6 longior）已全部生成，旧 brevis 文件是冗余的。即使部分新文件验证未通过，也应先清理旧文件，后续再修复新文件。

**文件列表**：
- Cap4_Decem_prōvinciae_Rōmānae_brevis_004.md
- Cap4_Quattuor_flūmina_brevis_002.md
- Cap4_Quattuor_oppida_Ītaliae_brevis_003.md
- Cap4_Quattuor_populī_brevis_001.md
- Cap4_Discēde_brevis_008.md
- Cap4_Fīlius_improbus_brevis_005.md
- Cap4_Pecūnia_patris_brevis_009.md
- Cap4_Puella_et_aqua_brevis_014.md
- Cap4_Puer_et_liber_brevis_006.md
- Cap4_Puer_et_piscis_brevis_012.md
- Cap4_Puer_sōlus_brevis_013.md
- Cap4_Servus_bonus_brevis_007.md
- Cap4_Servus_et_aqua_brevis_010.md
- Cap4_Dominus_et_servus_in_viā_brevis_011.md

### 步骤2：验证 Cap.4 重写故事

**操作**：运行 `rewrite_cap4.py` 脚本，检查14篇新故事的验证结果。

**预期**：根据之前的诊断，最多9篇可能失败（v2_level > 6）。需要逐篇检查高章节词。

**若全部通过**：步骤2完成，直接跳到步骤4。

**若有失败**：进入步骤3修复。

### 步骤3：修复 Cap.4 失败故事（按需）

**诊断方法**：对每篇失败故事，运行自定义诊断脚本，列出所有词元的章节映射，找出导致评级升高的高章节词。

**修复策略**（参照之前总结的经验）：
- 替换超章节动词：如 `legit`(Cap.18) → `videt`(Cap.3)，`ambulat`(Cap.6) → 删除或用安全词替换
- 替换超章节名词：用Cap.1-6安全名词替换
- 替换超章节副词：如 `semper`(Cap.16) → 删除
- 专有名词处理：仅保留 ≤Cap.6 的专有名词

**安全词汇参考**（≤Cap.6）：
- 动词：est/sunt, habet/habent, videt/vident, venit/veniunt, dat/dant, capit/capiunt, vocat, pāret/pārent, amat/amant, pugnat, imperat, fluit
- 名词：vir, fēmina, puer, puella, servus, dominus, oppidum, via, aqua, terra, īnsula, hortus, liber, pecūnia, populus, imperium, familia, māter, pater, fīlius, fīlia
- 形容词：magnus, parvus, bonus, malus, pulcher, multus, laetus, līber, sōlus

**修复后重新验证**：每修完一篇立即验证，通过后更新文件。

### 步骤4：创建 rewrite_cap5.py

**目标**：10篇 brevis → 6篇中篇(300-500词) + 4篇中长篇(500-800词)

**词汇约束**：严格使用 Cap.1-7 词元（lemma_chapter_map ≤ 7）。验证标准：v2_level ≤ 5+2=7。

**10篇故事元数据**（从现有 brevis 文件提取，保留原 theme/style/genre/character/narrative）：

| ID | 标题 | 主题 | 风格 | 体裁 | 角色 | 叙述 | 目标篇幅 |
|----|------|------|------|------|------|------|----------|
| cap5_01 | Quī dormit? | 23 睡眠 | 白话 | G 哲理寓言 | 罗马人 | 对话体 | 中篇 |
| cap5_02 | Via ad oppidum | 22 旅程 | 白话 | C 历史与人物 | 旅人 | 第三人称 | 中篇 |
| cap5_03 | In hortō | 18 自然 | 抒情 | A LLPSI宇宙 | 罗马人 | 第一人称 | 中篇 |
| cap5_04 | Māter et fīlia in hortō | 29 母性与自我 | 抒情 | C 历史与人物 | 罗马人 | 第一人称 | 中篇 |
| cap5_05 | Fēmina sōla | 13 孤独 | 抒情 | M 伦理与习俗 | 罗马人 | 第三人称 | 中篇 |
| cap5_06 | Fīlius discit | 28 教育 | 古典 | A LLPSI宇宙 | 罗马人 | 第三人称 | 中篇 |
| cap5_07 | Ancilla et domina | 58 主人与奴隶 | 冷峻 | M 伦理与习俗 | 罗马人 | 第三人称 | 中长篇 |
| cap5_08 | Vīlla Rōmāna | 36 乡村 | 白话 | C 历史与人物 | 罗马人 | 第三人称 | 中长篇 |
| cap5_09 | Servus et rosa | 02 爱 | 抒情 | M 伦理与习俗 | 奴隶 | 第三人称 | 中长篇 |
| cap5_10 | Pater et fīlius in hortō | 25 家庭 | 白话 | C 历史与人物 | 罗马人 | 第三人称 | 中长篇 |

**脚本结构**：参照 `rewrite_cap4.py` 模式：
1. `STORIES` 字典存储所有故事元数据和拉丁正文
2. `main()` 函数：逐篇评估 → 打印结果 → 生成 Markdown → 全部通过后删除旧 brevis

**篇幅扩充策略**（Cap.5词汇仍有限，约200词元）：
- 增加对话回合（适合对话体故事）
- 排比句和重复结构（适合描写场景）
- 感官细节展开（颜色、大小、位置）
- 人物互动扩展（增加对话人物）

### 步骤5：创建 rewrite_progress.json

**路径**：`/Users/max/Downloads/Projects/LLPSI_plus/AI_reader/rewrite_progress.json`

**内容结构**：
```json
{
  "plan": "437_short_rewrite_plan.md",
  "started": "2026-06-29",
  "last_updated": "2026-06-30",
  "phase": 1,
  "chapters": {
    "1": {"status": "done", "medius": 6, "longior": 3},
    "2": {"status": "done", "medius": 6, "longior": 4},
    "3": {"status": "done", "medius": 5, "longior": 5},
    "4": {"status": "in_progress", "medius": 8, "longior": 6, "passed": 0, "total": 14},
    "5": {"status": "pending", "target_medius": 6, "target_longior": 4}
  }
}
```

### 步骤6：更新 progress.json

在 `/Users/max/Downloads/Projects/LLPSI_plus/AI_reader/progress.json` 中新增 `rewrite_phase` 字段：
```json
"rewrite_phase": {
  "plan": "437_short_rewrite_plan.md",
  "current_phase": 1,
  "current_chapter": 4,
  "phases": {
    "1": {"chapters": "1-5", "status": "in_progress"},
    "2": {"chapters": "6-10", "status": "pending"},
    "3": {"chapters": "11-20", "status": "pending"},
    "4": {"chapters": "21-30", "status": "pending"},
    "5": {"chapters": "31+", "status": "pending"}
  }
}
```

---

## 3. 执行顺序

```
步骤1（清理Cap.4）→ 步骤2（验证Cap.4）→ 步骤3（按需修复）→ 步骤4（创建Cap.5）→ 步骤5（创建progress）→ 步骤6（更新progress.json）
```

步骤1-2可连续执行。步骤3仅在步骤2有失败时触发。步骤4-6顺序执行。

---

## 4. 验证清单

- [ ] Cap.4 目录仅剩14个文件（8 medius + 6 longior），无 brevis 残留
- [ ] Cap.4 全部14篇 v2_level ≤ 6
- [ ] Cap.5 目录有10个新文件（6 medius + 4 longior），无 brevis 残留
- [ ] Cap.5 全部10篇 v2_level ≤ 7
- [ ] rewrite_progress.json 已创建且内容准确
- [ ] progress.json 已更新 rewrite_phase 字段