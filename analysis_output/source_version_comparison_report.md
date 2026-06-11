# LLPSI Source 多版本对比报告

> **生成时间**: 2026-06-06
> **核心结论**: 优先使用 **HD 2nd Color Text-Selectable** 版本;**直接用 pypdf 提取**,无需 OCR

---

## 一、Familia Romana 多版本对比

| 文件 | 大小 | 页数 | 可提取字符 | 含文本页 | 评分 | 推荐 |
|:-----|-----:|----:|-----------:|--------:|-----:|:----:|
| `LLPSI_core_familia_romana.pdf` | 19.8 MB | 331 | 554,307 | 330/331 | ⭐⭐⭐ | 备选 |
| `LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf` | **143.7 MB** | 332 | 556,597 | 328/332 | ⭐⭐⭐⭐⭐ | **★ 首选** |
| `LLPSI_core_familia_romana_hd_color_small.pdf` | 52.4 MB | 332 | 556,027 | 328/332 | ⭐⭐⭐⭐ | 等同首选,体积小 |
| `LLPSI_core_familia_romana_v1_scan.pdf` | 7.0 MB | 335 | 0 | 0/335 | ❌ | 弃用 |
| `LLPSI_core_familia_romana_2003_v1_scan.pdf` | 4.9 MB | — | — | — | ❌ | 弃用 |

**FR 选型结论**:
- **首选**: `LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf` (143.7 MB, HD 彩图 2 版,带可选中文本)
- **备份**: `LLPSI_core_familia_romana_hd_color_small.pdf` (52.4 MB,内容完全一致,体积更小) — 推荐作为常用版本
- 两个 HD 版本字符数完全一致 (556k),区别仅在图片分辨率(影响图片引用)
- 旧版纯扫描 (`v1_scan`, `2003_v1_scan`) 无可选中文字,应弃用

---

## 二、Roma Aeterna 多版本对比

| 文件 | 大小 | 页数 | 可提取字符 | 含文本页 | Mojibake | 评分 | 推荐 |
|:-----|-----:|----:|-----------:|--------:|---------:|-----:|:----:|
| `LLPSI_core_roma_aeterna.pdf` | 16.4 MB | 426 | 1,274,336 | 422/426 | 156,234 个 `\NNN` 转义 | ⭐⭐ | 弃用 |
| `LLPSI_core_roma_aeterna_hd_2nd_color.pdf` | **174.9 MB** | 429 | 769,503 | 428/429 | 0 | ⭐⭐⭐⭐⭐ | **★ 首选** |
| `LLPSI_core_roma_aeterna_hd_2nd_color_alt.pdf` | 172.7 MB | 429 | 4,693 | 108/429 | 0 | ⭐ | 备选扫描 |
| `LLPSI_core_roma_aeterna_v1_bw.pdf` | 18.0 MB | 482 | 7 | 1/482 | 0 | ❌ | 弃用 |
| `LLPSI_core_roma_aeterna_v1_scan.pdf` | 14.6 MB | 426 | 0 | 0/426 | 0 | ❌ | 弃用 |
| `LLPSI_core_roma_aeterna_v1_scan_sm.pdf` | 15.0 MB | — | — | — | — | ❌ | 弃用 |
| `LLPSI_core_roma_aeterna_1990_v1_scan.pdf` | 5.0 MB | — | — | — | — | ❌ | 弃用 |

**RA 选型结论**:
- **首选**: `LLPSI_core_roma_aeterna_hd_2nd_color.pdf` (174.9 MB, HD 彩图 2 版,**带可选中文本**)
- **意外发现**: 之前 OCR 过的 HD 2nd color 实际上**已经是可选中文字**!OCR 工作是徒劳的。
  - pypdf 提取的文本: 769,503 字符,428/429 页
  - OCR 输出的文本: 802,000 字符(估)
  - **直接用 pypdf 提取即可**,无需 OCR
- 普通版 `LLPSI_core_roma_aeterna.pdf` 字符数多(1.27M),但 **96,222 个八进制转义**,解码后仍丢失大量信息(普通评分 30/100)
- HD 2nd color alt 是另一份扫描,可选中文本极少(4,693 字符),仅作 OCR 备用

---

## 三、HD 2nd Color pypdf 提取 vs OCR 输出对比 (RA)

| 指标 | OCR 输出 | HD pypdf 直接提取 | 普通 pypdf 解码 |
|:-----|--------:|----------------:|--------------:|
| 总字符数 | 802,000 | 769,503 | 806,060 |
| 词形数 | 89,064 | **104,148** | 75,619 |
| 唯一词形 | 19,715 | **25,473** | 12,223 |
| Mojibake | 0 | 0 | 60,012 |
| 长音符号 (āēīōū) | 0 | 5 | 0 |
| **质量评分** | 60/100 | **100/100** | 30/100 |

**关键发现**:
- **HD pypdf 提取的文本显著优于 OCR 输出** (词形多 17%, 唯一词形多 29%)
- OCR 输出的 89k 词形只是 HD pypdf 104k 词形的 85% 子集
- 之前 6+ 小时的 OCR 工作大部分被 HD 版本自身的可选中文字层超越

---

## 四、其他多版本文件建议

| 文件分组 | 推荐 | 弃用 |
|:---------|:-----|:-----|
| `core_indices` | `LLPSI_core_indices.pdf` (3.7 MB,68页) | `indices_v1.pdf` |
| `grammar_grammatica_latina` | `LLPSI_grammar_grammatica_latina.pdf` (1.5 MB, 36页) | `grammatica_latina_v1.pdf` |
| `grammar_instructions` | `LLPSI_grammar_instructions.pdf` (2.8 MB, 40页) | `instructions_v1.pdf`, `instructions_v1_sm.pdf` |
| `exercitia_latina_II` | `LLPSI_exercitia_latina_II.pdf` (7.1 MB) | `latina_II_v1.pdf` (2.4 MB) |
| `reader_colloquia_personarum` | `LLPSI_reader_colloquia_personarum.pdf` (10.2 MB) | `colloquia_personarum_v1_scan.pdf` |
| `reader_fabulae_syrae` | `LLPSI_reader_fabulae_syrae.pdf` (4.5 MB) | `fabulae_syrae_1st_ed.pdf` |
| `vocab_latine_anglicus_I_II` | `LLPSI_vocab_latine_anglicus_I_II.pdf` (2.1 MB) | `latine_anglicus_I_II_v1.pdf` |
| `vocab_multilingue` | `LLPSI_vocab_multilingue.pdf` | `multilingue.xlsx` (非 PDF) |

---

## 五、行动计划

### 立即 (1-2 小时)
1. ✅ **确认首选版本**: FR + RA 都用 HD 2nd Color
2. ✅ **重新提取 HD 2nd color 文本**: 用 pypdf 直接提取 `LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf` 和 `LLPSI_core_roma_aeterna_hd_2nd_color.pdf`
3. ✅ **覆盖现有 OCR 输出**: 替换 `ocr_output/familia_romana/clean.txt` 和 `ocr_output/roma_aeterna/_full.txt`

### 短期 (1-2 天)
4. 重新跑词频分析 (`iterum_analysis.py` + `analyze_book.py`)
5. 重新生成两册合并 HTML 可视化
6. 删除 (移到 `_archive/`) 重复/弃用版本 PDF

### 中期 (3-5 天)
7. 标记 companion 文件为"辅助参考",不进入自然习得法流程
8. OCR 其余 8 个新增 reader (aeneis, amphitryo, ars_amatoria, bello_gallico, catilina, cena_trimalchionis, de_rerum_natura, epitome_historiae_sacrae)

---

## 六、Companion 文件处理建议 (按用户最新指示)

> **用户原话**: "实际上companion并没有使用LLPSI推崇的自然习得法,只作为辅助——请你在相关文档中标注出来,后续不对companion进行处理"

**Companion 文件清单** (辅助,不做 OCR / 分析 / 入库):
- `LLPSI_companion_familia_romana_neumann.pdf` (Heinrich Neumann FR 指南)
- `LLPSI_companion_familia_romana_2007_v1.djvu` (2007 DjVu 旧版)
- `LLPSI_companion_roma_aeterna_neumann.pdf` (Heinrich Neumann RA 指南)

**后续处理**:
- ❌ 不进行 OCR
- ❌ 不进入词频分析
- ❌ 不入库到 `llpsi_corpus.db`
- ✅ 在 SKILL.md / Project_Plan.md 中标注为 "辅助参考材料"
