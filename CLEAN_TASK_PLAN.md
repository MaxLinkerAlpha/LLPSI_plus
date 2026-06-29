# OCR & 词表 修订任务计划书

> 创建时间：2026-06-29
> 状态：**全部完成** ✅
> 完成时间：2026-06-29
> 说明：此文件用于跨压缩轮次持续追踪任务进度。每修完一批，在此标记。

---

## 一、任务总览

| 阶段 | 内容 | 文件数 | 状态 |
|------|------|--------|------|
| Phase 0 | 全量备份 | — | ✅ 已完成 |
| Phase 1 | 清洗 capX_vocab_clean.json | 34 | ✅ 已完成 |
| Phase 2 | 清洗 OCR 正文文件 | 222 | ✅ 已完成 |
| Phase 3 | 重新生成派生文件 | 1 | ✅ 已完成 |

## 二、Phase 0：全量备份

**操作**：
```bash
cp -r difficulty_algorithm/vocab_by_chapter difficulty_algorithm/vocab_by_chapter_backup_20260629
cp -r OCR OCR_backup_20260629
```

## 三、Phase 1：清洗 capX_vocab_clean.json（34章）

### 保留规则（这些是合法拉丁词条）

| 规则 | 示例 |
|------|------|
| 完整拉丁词形 | `puella`, `fluvius`, `magnus`, `est` |
| 语法术语（保留） | `Ablativus`, `Accusativus`, `Singularis`, `Pluralis`, `Nominativus` |
| 章节标题（保留） | `CAPITVLVM`, `PRIMVM`, `SECVNDVM` |
| 专有名词 | `Roma`, `Italia`, `Iulius`, `Aemilia` |
| 罗马数字 | `I`, `II`, `III`, `IV`, `V`, `X`, `L`, `C`, `D`, `M` |

### 删除规则（这些是OCR脏数据）

| 类别 | 判断标准 | 示例 |
|------|----------|------|
| 截断词根 | 不是完整拉丁词形，是词干碎片 | `magn`, `parv`, `mult`, `insul`, `oppid`, `serv`, `flu`, `domin`, `puell`, `vocabul`, `numer`, `litter` |
| 粘合词 | 两个独立词被OCR粘在一起 | `fluviusest`, `oppidumBrundisium`, `suntinsulae`, `sedin`, `estin`, `latinest`, `quoqueCorsica`, `Rhenuset`, `cumhomo`, `piscesin` |
| 乱码/噪音 | 含非拉丁字符或完全无意义 | `zTz`, `MUmY`, `ssst`, `A——D`, `B'be`, `C"c`, `D)ES`, `H'ha`, `HHHHHHHH`, `Uhuhu`, `Cucucurru`, `Cucurru`, `hahae`, `hahahae`, `tuxtax` |
| 拼写错误OCR产物 | 明显不是任何拉丁词的正确拼写 | `Accusdtious`, `Accusatitous`, `Genetious`, `brundisiz`, `Nominatious`, `Vocatious`, `Imperatious`, `Locativus`, `Nominatmvus`, `Plurialis` |
| 大小写重复 | 同一词的大小写版本都出现 | `Aegyptus` + `aegyptus` → 保留一个小写版 |
| 带数字/标点前缀 | 词前有数字或标点残渣 | `80est`, `90Delia`, `1r`, `3/-o`, `45in`, `65Medus`, `75Iulius`, `130Quo`, `135Syra`, `280me` |
| 带引号残渣 | 词尾粘了引号片段 | `cantat.\"Aemilia"`, `centum.\"Cornelius"`, `est!\"Aemilia"` |
| 单字母残渣 | 孤立的单个字母 | `B`, `C`, `D`, `a`, `b`, `c`（单独出现，不是罗马数字） |

### 去重规则
- 大小写去重：`Aegyptus` 和 `aegyptus` → 保留小写 `aegyptus`（除非是专有名词始终大写）
- 专有名词始终保留首字母大写版本

### 长音检查
- 拉丁词的长音符号（macron）必须正确。例如 `Rōma` 不是 `Roma`、`Eurōpa` 不是 `Europa`
- 如果发现某词缺失长音，补充正确的长音形式
- 参考标准：LLPSI 课本原文中的长音标注

### 章节进度追踪

| 章节 | 原始条目 | 清洗后 | 状态 |
|------|---------|--------|------|
| cap1 | 158 | 91 | 已完成 |
| cap2 | 289 | 170 | 已完成 |
| cap3 | 377 | 225 | 已完成 |
| cap4 | 474 | 288 | 已完成 |
| cap5 | 597 | 374 | 已完成 |
| cap6 | 758 | 484 | 已完成 |
| cap7 | 822 | 526 | 已完成 |
| cap8 | 969 | 620 | 已完成 |
| cap9 | 1097 | 698 | 已完成 |
| cap10 | 1269 | 809 | 已完成 |
| cap11 | 1398 | 903 | 已完成 |
| cap12 | 1607 | 1011 | 已完成 |
| cap13 | 1845 | 1159 | 已完成 |
| cap14 | 1978 | 1251 | 已完成 |
| cap15 | 2095 | 1324 | 已完成 |
| cap16 | 2290 | 1450 | 已完成 |
| cap17 | 2440 | 1523 | 已完成 |
| cap18 | 2634 | 1649 | 已完成 |
| cap19 | 2888 | 1820 | 已完成 |
| cap20 | 3094 | 1963 | 已完成 |
| cap21 | 3241 | 2059 | 已完成 |
| cap22 | 3397 | 2161 | 已完成 |
| cap23 | 3532 | 2259 | 已完成 |
| cap24 | 3658 | 2326 | 已完成 |
| cap25 | 3888 | 2455 | 已完成 |
| cap26 | 4110 | 2610 | 已完成 |
| cap27 | 4342 | 2773 | 已完成 |
| cap28 | 4586 | 2926 | 已完成 |
| cap29 | 4852 | 3088 | 已完成 |
| cap30 | 5059 | 3242 | 已完成 |
| cap31 | 5278 | 3397 | 已完成 |
| cap32 | 5532 | 3557 | 已完成 |
| cap33 | 5802 | 3745 | 已完成 |
| cap34 | 6077 | 3941 | 已完成 |
| cap35 | 3025 | 2483 | 已完成（2026-06-29 补全） |
| cap36 | 1936 | 1572 | 已完成（2026-06-29 补全） |
| cap37 | 1826 | 1530 | 已完成（2026-06-29 补全） |
| cap38 | 1550 | 1287 | 已完成（2026-06-29 补全） |
| cap39 | 2072 | 1713 | 已完成（2026-06-29 补全） |
| cap40 | 1901 | 1571 | 已完成（2026-06-29 补全） |
| cap41 | 1627 | 1322 | 已完成（2026-06-29 补全） |
| cap42 | 2245 | 1857 | 已完成（2026-06-29 补全） |
| cap43 | 2148 | 1734 | 已完成（2026-06-29 补全） |
| cap44 | 2616 | 2138 | 已完成（2026-06-29 补全） |
| cap45 | 2398 | 1951 | 已完成（2026-06-29 补全） |
| cap46 | 2317 | 1845 | 已完成（2026-06-29 补全） |
| cap47 | 1397 | 1113 | 已完成（2026-06-29 补全） |
| cap48 | 3538 | 2870 | 已完成（2026-06-29 补全） |
| cap49 | 1870 | 1504 | 已完成（2026-06-29 补全） |
| cap50 | 3079 | 2512 | 已完成（2026-06-29 补全） |
| cap51 | 2090 | 1691 | 已完成（2026-06-29 补全） |
| cap52 | 3058 | 2543 | 已完成（2026-06-29 补全） |
| cap53 | 2197 | 1724 | 已完成（2026-06-29 补全） |
| cap54 | 2770 | 2270 | 已完成（2026-06-29 补全） |
| cap55 | 2265 | 1864 | 已完成（2026-06-29 补全） |
| cap56 | 2285 | 1838 | 已完成（2026-06-29 补全） |

**总计：56 章，87,074 条词条（原始 96,401 条，删除 9,327 条）**

## 四、Phase 2：清洗 OCR 正文文件（222个 txt）

### 目录结构
```
OCR/LLPSI_core/familia_romana/fr_cap1~35/   × 3 = 105 个
OCR/LLPSI_core/roma_aeterna/ra_cap36~56/    × 3 = 63 个
OCR/LLPSI_reader/fabulae_syrae/ad_cap26~34/ × 6 = 54 个
合计：222 个 txt
```

### 每章三个文件
- `capX_main_macrons_final.txt` — 正文（含长音）
- `capX_grammar_macrons.txt` — 语法区（含长音）  
- `capX_marg_macrons.txt` — 边注（含长音）

### 保留规则

| 类别 | 处理方式 |
|------|----------|
| 章节标题 | 保留，如缺少长音则补上 |
| 章节号 | 保留（如 `CAP. X`, `CAPITVLVM DECIMVM`） |
| 行号 | 保留在行首/行尾的；混入词中的清洗掉 |
| 语法术语 | 保留，如缺少长音则补上 |
| 罗马数字 | 保留 |
| 长音 | 必须正确，缺失则补上 |

### 清洗规则

| 问题 | 修复方法 |
|------|----------|
| 行间断词 | 合并且补全长音：`Eu\nropā` → `Eurōpā` |
| 粘合词 | 拆分为两个独立词：`fluviusest` → `fluvius est` |
| 行号混入词中 | 分离数字到行首/行尾：`80est` → `80 est` |
| 乱码字符 | 手动修正或删除 |
| 标点/引号残渣 | 清理多余的引号转义 |
| 长音错误 | 修正为正确的长音形式 |

### 注意事项
- 这是教材OCR，标题、章节号、行号、语法术语都是正文的一部分，不应删除
- 只清洗OCR导致的错误，不改变原文内容
- 对不确定的地方标记 `[?]` 等待人工审核

### 章节进度追踪

| 书 | 章节范围 | 文件数 | 状态 |
|----|---------|--------|------|
| Familia Romana | cap1-10 | 30 | ✅ 已完成 |
| Familia Romana | cap11-20 | 30 | ✅ 已完成 |
| Familia Romana | cap21-30 | 30 | ✅ 已完成 |
| Familia Romana | cap31-35 | 15 | ✅ 已完成 |
| Roma Aeterna | cap36-45 | 30 | ✅ 已完成 |
| Roma Aeterna | cap46-56 | 33 | ✅ 已完成 |
| Fabulae Syrae | ad_cap26-30 | 30 | ✅ 已完成 |
| Fabulae Syrae | ad_cap31-34 | 24 | ✅ 已完成 |

### 清洗统计

| 清洗轮次 | 脚本 | 修复数 |
|----------|------|--------|
| 第1轮 | clean_all.py | ~47,849 处 |
| 第2轮 | clean_fix_round2.py | ~1,893 处 |
| 第3轮 | clean_final_pass.py | 65 文件 |

### 残留问题（可忽略）

| 类型 | 数量 | 说明 |
|------|------|------|
| camelCase | 3 | 罗马数字+孤立字母（如 vitI, cvrI）|
| 数字-单词粘合 | 3 | 数字+大写字母（如 2Q, 1H, 4A），可能是缩写 |

## 五、Phase 3：重新生成派生文件 ✅

| 文件 | 状态 | 条目数 |
|------|------|--------|
| `word_chapter_map.json` | ✅ 已重新生成 | 3,178 词条 |
| 一致性验证 | ✅ 通过 | 与词表完全一致 |

## 六、中断恢复指引

如果上下文压缩导致丢失进度：

1. 先读此文件了解当前进度
2. 继续执行未完成的章节
3. 每完成一批（5章），更新本文件中的进度表
4. 备份在 `vocab_by_chapter_backup_20260629/` 和 `OCR_backup_20260629/`

---

## 七、清洗脚本使用指南

### 7.1 脚本清单

| 脚本 | 用途 | 何时使用 |
|------|------|----------|
| `clean_all.py` | 主流程（Phase 1+2+3）| 完整清洗所有词表+OCR |
| `clean_fix_round2.py` | 第二轮精准修复 | 处理过度拆分、碎片、粘合词 |
| `clean_final_pass.py` | 最终保守修复 | 修复残留 camelCase、数字-单词粘合 |
| `extract_vocab_from_ocr.py` | 从 OCR 提取词表 | 补全新章节时使用 |

### 7.2 标准工作流（清洗已有词表+OCR）

```bash
# 完整三阶段清洗
cd /Users/max/Downloads/Projects/LLPSI_plus
python3 clean_all.py        # Phase 0+1+2+3
python3 clean_fix_round2.py # 第二轮精准修复
python3 clean_final_pass.py # 最终保守修复
```

### 7.3 补全新章节词表（cap35~56）

```bash
# 1. 从 OCR 提取词汇生成 capX_vocab_clean.json
python3 extract_vocab_from_ocr.py --start 35 --end 56

# 2. 走标准清洗流程
python3 clean_all.py
python3 clean_fix_round2.py
python3 clean_final_pass.py
```

### 7.4 单独运行某一阶段

如只想重新清洗词表不重清洗 OCR，可手动调用：

```python
# 在 Python 中调用
from clean_all import extract_words_from_ocr, phase1_clean_vocab, phase3_regenerate
ref_dict, ref_counter = extract_words_from_ocr()
results = phase1_clean_vocab(ref_dict, ref_counter)
phase3_regenerate()
```

### 7.5 重要约束

- **必先备份**（Phase 0）：`clean_all.py` 会原地修改所有 `cap*_vocab_clean.json` 和 `OCR/**/*.txt`
- **UTF-8 编码**：所有脚本使用 `encoding="utf-8", errors="replace"`
- **大小写规则**：专有名词保留大写（`Roma`, `Iulius`），其他小写
- **派生文件**：Phase 3 会自动从 `cap*_vocab_clean.json` 重新生成 `word_chapter_map.json`

### 7.6 备份与恢复

```bash
# 备份
cp -r difficulty_algorithm/vocab_by_chapter difficulty_algorithm/vocab_by_chapter_backup_YYYYMMDD
cp -r OCR OCR_backup_YYYYMMDD

# 恢复
rm -rf difficulty_algorithm/vocab_by_chapter
cp -r difficulty_algorithm/vocab_by_chapter_backup_YYYYMMDD difficulty_algorithm/vocab_by_chapter
rm -rf OCR
cp -r OCR_backup_YYYYMMDD OCR
```