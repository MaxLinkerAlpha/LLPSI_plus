#!/usr/bin/env python3
"""Render full reader_audit_report.md from integrated data."""
import json
from pathlib import Path

OUT = Path('/Users/max/Downloads/Projects/LLPSI+++/analysis_output/reader_report_data.json')
with open(OUT) as f:
    data = json.load(f)

def sort_key(r):
    s60 = r.get("starting_chapter_60")
    s50 = r.get("starting_chapter_50")
    peak = r.get("peak_chapter") or 999
    if s60 is not None:
        primary = s60
        tier_pri = 0
    elif s50 is not None:
        primary = s50
        tier_pri = 1
    else:
        primary = peak
        tier_pri = 2
    return (tier_pri, primary, -r["unique_latin_count"])

data.sort(key=sort_key)

# ==================== 渲染各部分 ====================
def render_tldr() -> str:
    lines = ["| # | slug | 拉词 | 独词 | 英% | 起点 60% | 起点 50% | 教学价值 | 类型 | 备注 |",
            "|---|------|-----:|-----:|----:|---------:|---------:|----------:|------|------|"]
    for i, r in enumerate(data, 1):
        s60 = r.get("starting_chapter_60")
        s50 = r.get("starting_chapter_50")
        s60_str = f"**Cap.{s60}**" if s60 is not None else "—"
        s50_str = f"Cap.{s50}" if s50 is not None else "—"
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        note = r.get("note", "")[:30]
        if r["slug"] == "ecce_romani_combined":
            note = "**已丢弃 (EPUB)**, 见 §6.3"
        lines.append(f"| {i} | `{r['slug']}` | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {s60_str} | {s50_str} | {bt_str} | {r['tier']} | {note} |")
    return "\n".join(lines)


def render_strong_recommend() -> str:
    """A. 5本有明确起点"""
    lines = ["| # | slug | 标题 | 学完后可读 | 拉词 | 独词 | 英% | 教学章节 | 备注 |",
            "|---|------|------|-----------|-----:|-----:|----:|----------|------|"]
    i = 0
    for r in data:
        if r.get("starting_chapter_60") is not None or r.get("starting_chapter_50") is not None:
            i += 1
            s60 = r.get("starting_chapter_60")
            s50 = r.get("starting_chapter_50")
            if s60 is not None:
                anchor = f"**学完 FR Cap.{s60}** (60%)"
            else:
                anchor = f"学完 FR Cap.{s50} (50%)"
            bt = r.get("best_teach_chapter")
            bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
            lines.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {anchor} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} | {r.get('note','')[:25]} |")
    return "\n".join(lines)


def render_pure_latin() -> str:
    """B. 拉语为主 (英<30%)"""
    lines = ["| # | slug | 标题 | 拉词 | 独词 | 英% | 教学章节 | 类型 | 备注 |",
            "|---|------|------|-----:|-----:|----:|----------|------|------|"]
    pure = [r for r in data if r['english_ratio'] < 0.30 and r['latin_word_count'] > 1000]
    pure.sort(key=lambda x: x['english_ratio'])
    for i, r in enumerate(pure, 1):
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        note = r.get("note", "")[:25]
        lines.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} | {r['tier']} | {note} |")
    return "\n".join(lines)


def render_mixed_30_50() -> str:
    """C. 拉英混合 30-50%"""
    lines = ["| # | slug | 标题 | 拉词 | 独词 | 英% | 教学章节 | 类型 |",
            "|---|------|------|-----:|-----:|----:|----------|------|"]
    cat = [r for r in data if 0.30 <= r['english_ratio'] < 0.50]
    cat.sort(key=lambda x: -(x.get('best_teach_coverage') or 0))
    for i, r in enumerate(cat, 1):
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        lines.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} | {r['tier']} |")
    return "\n".join(lines)


def render_mixed_50_plus() -> str:
    """D. 拉英混合 50%+ (含3个子类)"""
    out = []
    out.append("### D.1 拉英对话手册 (特殊类别, 1 本)\n")
    out.append("| # | slug | 标题 | 拉词 | 独词 | 英% | 教学章节 | 备注 |")
    out.append("|---|------|------|-----:|-----:|----:|----------|------|")
    dialog = [r for r in data if r['tier'] == "B_mixed_dialog"]
    for i, r in enumerate(dialog, 1):
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        out.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} | {r.get('note','')[:30]} |")

    out.append("\n### D.2 拉英混合 — Cambridge / Oxford / Ecce Romani 教材系列\n")
    out.append("> 这些书的拉语故事段(Cultura, Fabula, Story 等)对应 LLPSI 特定章节, 教学价值高, 适合做\"跨教材扩展阅读\".\n")
    out.append("| # | slug | 标题 | 拉词 | 独词 | 英% | 教学章节 |")
    out.append("|---|------|------|-----:|-----:|----:|----------|")
    textbooks = [r for r in data if r['tier'] == "D_textbook" and r['slug'].split('_')[0] in ("cambridge", "oxford", "ecce")]
    textbooks.sort(key=lambda x: -x['unique_latin_count'])
    for i, r in enumerate(textbooks, 1):
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        out.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} |")

    out.append("\n### D.3 教材类 — Wheelock / D'Ooge / Reading Latin / 其他\n")
    out.append("> 纯语法教材或配套读本, 拉语独词量大, 英语占比高. 适合作\"高阶词汇查阅\".\n")
    out.append("| # | slug | 标题 | 拉词 | 独词 | 英% | 教学章节 |")
    out.append("|---|------|------|-----:|-----:|----:|----------|")
    other_tb = [r for r in data if r['tier'] == "D_textbook" and r['slug'].split('_')[0] not in ("cambridge", "oxford", "ecce")]
    other_tb.sort(key=lambda x: -x['unique_latin_count'])
    for i, r in enumerate(other_tb, 1):
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        out.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} |")

    out.append("\n### D.4 其他混合读物 (B_mixed_text, B1_mixed_story, B1_mixed_text, B2_mixed_text)\n")
    out.append("| # | slug | 标题 | 拉词 | 独词 | 英% | 教学章节 | 类型 |")
    out.append("|---|------|------|-----:|-----:|----:|----------|------|")
    other = [r for r in data if r['tier'] in ("B_mixed_text", "B1_mixed_story", "B1_mixed_text", "B2_mixed_text", "A1_mixed_story") and 0.50 <= r['english_ratio'] < 0.60]
    other.sort(key=lambda x: x['english_ratio'])
    for i, r in enumerate(other, 1):
        bt = r.get("best_teach_chapter")
        bt_str = f"Cap.{bt}({r['best_teach_coverage']:.0%})" if bt else "—"
        out.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {bt_str} | {r['tier']} |")
    return "\n".join(out)


def render_d_class_extract() -> str:
    """E. D 类教材拉语段提取"""
    d_extract = [r for r in data if r.get("latin_story_pages", 0) > 0]
    d_extract.sort(key=lambda x: -x['latin_story_pages'])
    lines = ["| # | slug | 标题 | 提取段数 | 提取页数 | 备注 |",
            "|---|------|------|--------:|--------:|------|"]
    for i, r in enumerate(d_extract, 1):
        lines.append(f"| {i} | `{r['slug']}` | {r['title'][:35]} | {r['latin_story_count']} | **{r['latin_story_pages']}** | {r.get('note','')[:25]} |")
    return "\n".join(lines)


def render_english_dominant() -> str:
    """F. 英语为主"""
    cat = [r for r in data if r['english_ratio'] > 0.50 and r['tier'] in ("D_textbook", "D_stories", "B2_mixed_text", "unknown")]
    cat.sort(key=lambda x: -x['english_ratio'])
    lines = ["| # | slug | 标题 | 拉词 | 独词 | 英% | 备注 |",
            "|---|------|------|-----:|-----:|----:|------|"]
    for i, r in enumerate(cat, 1):
        note = r.get('note', '')[:25]
        lines.append(f"| {i} | `{r['slug']}` | {r['title'][:40]} | {r['latin_word_count']:,} | {r['unique_latin_count']:,} | {r['english_ratio']:.0%} | {note} |")
    return "\n".join(lines)


# ==================== 组装完整报告 ====================
report = f"""# Other_Readers 读物评估报告 (v3.0 完全重写)

> **报告版本**: v3.0.0 | **生成日期**: 2026-06-06
> **审计范围**: `source/Other_Readers/` 下全部 55 份 PDF / EPUB (Non-LLPSI 读物)
> **核心指标**: 词汇量 + LLPSI 章节锚点 (替代旧版 A1/A2 模糊分级)
> **方法**: 全本 OCR (13482 页) + 拉英词频加权 + 章节级 known/new 词覆盖计算 + D 类拉语段提取

---

## 评分体系 (替代 A1/A2)

本报告 **不再使用 A1/A2/B1/B2 等 CEFR 分级**，而是使用三个**可量化、可验证**的指标：

| 指标 | 含义 | 用途 |
|------|------|------|
| **起点章节** (`starting_chapter_60`) | 学完 FR Cap.X 后, FR 已知词覆盖本书 60% 独词的最早章节 | "我学完第X章能读这本书吗?" |
| **起点章节 (宽松)** (`starting_chapter_50`) | 学完 FR Cap.X 后 50% 覆盖的最早章节 | "有挑战但基本可读" |
| **教学价值** (`best_teach_chapter`) | 本书覆盖 FR Cap.X 新词最多的章节 (高=适合用来复习该章新词) | "我想复习第X章新词, 哪本最好?" |
| **拉语词汇量** (`latin_word_count`) | OCR 后识别为拉语的词数 | "这本书信息量" |
| **拉语独词** (`unique_latin_count`) | 唯一拉语词形数 | "这本书生词量" |
| **英语比例** (`english_ratio`) | OCR 中英语词占比 | "拉英混合程度" |

`verdict` 分类:

- `post_ra_latin`: 拉语为主, 起点在 RA 阶段 (学完 FR 35 章)
- `english_mixed`: 拉英混合 (30-70%英文)
- `english_dominant`: 英语为主 (英文>55%)

---

## TL;DR — 全部 55 本速查表

> 按"可读起点章节"升序. "—" 表示无明确起点 (即学完 LLPSI 全书后仍<50%覆盖, 此类书籍学习者无法按从头到尾通读的方式使用, 多用作"教学价值"参考).

{render_tldr()}

---

## A. 强推: 学完 Cap.X 后可读 (5 本)

> 这些书已通过 50%/60% 覆盖率算法验证, 学习者学完指定 LLPSI 章节后, FR 已知词可覆盖本书 50-60% 的拉语独词. 剩余 40-50% 生词通过上下文和注释可以推导出.
>
> **使用建议**: 这些是 LLPSI 主线之外的"奖励读物", 完成对应章节后即可挑战.

{render_strong_recommend()}

**注**: v2 报告将本节标注为 "FR Cap.1-20 区间" 是**误导**. 实际上这 5 本都是学完 FR 后期/RA 阶段才能基本读懂的, 不适合入门期.

---

## B. 拉语为主 (英语 < 30%, {len([r for r in data if r['english_ratio'] < 0.30 and r['latin_word_count'] > 1000])} 本)

> 拉语占绝对主导, 适合做"主读物". 这类书即使没有明确的起点章节, 学习者也可在 FR Cap.30+ 时借助注释/字典通读. 英语比例低说明内容连贯, 适合做长篇阅读训练.

{render_pure_latin()}

---

## C. 拉英混合 (30-50% 英文, {len([r for r in data if 0.30 <= r['english_ratio'] < 0.50])} 本)

> 适合中级学习者, 拉英交替. 拉语段可作主阅读, 英语段作参考. 按教学价值排序.

{render_mixed_30_50()}

**说明**:
- `forum_lectiones` 教学价值最高 (55%), 拉语对 FR Cap.4 新词覆盖率高, 推荐作为 Cap.4 复习读物
- Olimpi 系列 (`olimpia_*`) 是 Andrew Olimpi 出版的分级读物, 每本约 80-130 页, 适合做"短篇阅读练习"
- `fabulae_faciles` 是 Ritchie 1889 经典, 主体拉语神话故事, 适合 RA 阶段

---

## D. 拉英混合 (50%+ 英文)

{render_mixed_50_plus()}

**与 v2 报告差异**: v2 将 D 类全部"不推荐入库". v3 修正:
- 这些教材虽然英语主导, 但**拉语段本身**仍是有价值的, 适合查阅特定词汇/语法点
- `latin_natural_method` 提取出 78 页拉语故事段 (见 §E)
- `wheelock_7e` 拉语独词 14,864 (在 55 本中排第 1), 是 FR Cap.1 词汇的最佳扩展来源

**v3 新增**: `ecce_romani_2a`, `ecce_romani_2b`, `ecce_romani_3` (3 本新 Ecce Romani) — 见 §6.3

---

## E. D 类教材拉语段提取 ({len([r for r in data if r.get('latin_story_pages',0) > 0])} 本, {sum(r.get('latin_story_pages',0) for r in data)} 页)

> 通过 `scripts/extract_d_class_latin.py` 从 D 类教材中提取连续 3+ 页的拉语故事段. 拉语段可独立入库, 跳过英语讲解部分.
> **算法**: 每页独立判定 (拉/英/混合), 找连续 3+ 页的拉语/混合段, 标记为可入库故事段.

{render_d_class_extract()}

**重点推荐**:
- `latin_natural_method` (78 页) — 最佳 D 类提取, 拉语占比 46%, 拉语独词 4,548, 适合做 RA 阶段中级读物
- `dooge_beginners` / `dooge_beginners_2` — D'Ooge 教材附录拉语段, 适合 Cap.20+ 复习
- `cambridge_*` — CLC 教材的 Cap.X 配套故事, 可与 LLPSI Cap.X 同步使用

---

## F. 英语为主 (跳过)

> 英语 > 50%, 拉语含量低, 不作主读物. 仅作参考/查阅使用.

{render_english_dominant()}

**说明**: 这部分书籍虽然拉语少, 但**教学价值集中在 Cap.1** (即入门基础词汇), 可作"FR Cap.1 词汇扩展", 但因英语主导, 整本阅读体验差, 建议作为字典/参考使用.

---

## G. v3 vs v2 报告的关键差异

| 项目 | v2 (旧) | v3 (新) | 差异原因 |
|------|---------|---------|----------|
| 难度评级 | A1/A2/B1/B2 (CEFR) | 词汇量 + LLPSI 章节锚点 | 用户要求: 替代模糊分级 |
| 强推章节 | "FR Cap.1-20" (误导) | "学完 Cap.48 / Cap.52" | v3 用实际覆盖率计算, 显示真实起点 |
| A 类总数 | 16 本 | 5 本 (实际可读) | v3 严格用 50%/60% 阈值, 排除"理论可读" |
| B 类总数 | 5 本 | 5 本 + conversational_latin | conversational_latin 重新入库 |
| D 类 | 28 本"不推荐" | 16 本可"拉语段提取" + 11 本参考 | v3 不再因讲解多就判死刑 |
| 新 Ecce Romani | 未含 | 3 本新增 (2a/2b/3) | 用户添加新 PDF |
| Ecce Romani Combined EPUB | 未处理 | 标记为"已丢弃" | EPUB 提取仅 3 个文本文件 (其余图片), 不实用 |
| Nunc Loquamur | E: 跳过 | 已删除 (用户操作) | 用户已物理删除 |
| 教材价值 | "英语为主, 不入库" | "提取拉语段, 16 本共 162 页可入库" | D 类拉语段提取 (extract_d_class_latin.py) |

---

## 6. 技术与方法

### 6.1 词频分析 (v4)

**脚本**: `scripts/analyze_readers_v4.py`

**算法**:

1. 加载 OCR 后的全文 (`ocr_output/<slug>/_full.txt`)
2. 分词, 区分拉语词 / 英语词 (基于词频词表 + 后缀特征)
3. 加载 LLPSI FR 1-35 章 + RA 36-56 章累计词表 (`data/llpsi_corpus.db` 的 `fr_vocab` 表)
4. 对每本书:
   - 计算 `unique_latin_count` = 唯一拉语词形数
   - 对每章 (1-56): `chapter_known` = 1 到 N-1 章累计已知词
   - 计算覆盖率: `cov(N) = len(unique_latin ∩ chapter_known) / unique_latin_count`
   - `starting_chapter_50/60/70/80` = 首次达到 50%/60%/70%/80% 覆盖的章节
5. `best_teach_chapter` = 覆盖该章新词最多的章节 (即 `len(new_set ∩ unique_latin) / len(new_set)` 最大)

**注意**: 阈值 50%/60% 在很多英语混合书上达不到, 因此**仅 5 本书有明确起点**. 教学价值 (`best_teach_chapter`) 是更通用的指标, 39 本书达到 > 35% 覆盖率.

### 6.2 D 类拉语段提取

**脚本**: `scripts/extract_d_class_latin.py`

**算法**:

1. 对每页 OCR 文本判定语言 (拉/英/混合)
2. 找连续 3+ 页的拉语/混合段
3. 标记为可入库故事段, 记录起始页、页数、字符数

**提取结果**: `analysis_output/d_class_latin_stories.json` ({len([r for r in data if r.get('latin_story_pages',0) > 0])} 本共 {sum(r.get('latin_story_pages',0) for r in data)} 页)

### 6.3 Ecce Romani EPUB 评估

**脚本**: `scripts/compare_ecce_formats.py` + `scripts/ocr_new_ecce_romani.py`

**结论**:
- Ecce Romani I&II Combined EPUB 包含 14 个文本文件 (420KB) + 104 张图片 (1.6MB)
- 14 个文本文件中, 仅 3 个超过 500 字节阈值 (即含实质内容), 其余是图片占位符
- 提取出的 3 个文件 = 3 章, **仅覆盖原书前 3 章**, 不实用
- **决策**: 丢弃 combined EPUB (`ecce_romani_combined` slug), 使用 PDF 版本 (2a + 2b + 3)

### 6.4 数据流

```
source/Other_Readers/  (PDF + EPUB)
    ↓ [batch_ocr_readers.py / ocr_new_ecce_romani.py]
ocr_output/<slug>/_full.txt + page_NNN.txt
    ↓ [analyze_readers_v4.py]
analysis_output/reader_vocab_stats_v4.json  (55 本)
    ↓ [extract_d_class_latin.py]
analysis_output/d_class_latin_stories.json  (16 本 D 类)
    ↓ [generate_report_data.py]
analysis_output/reader_report_data.json  (整合数据)
    ↓ [render_report.py]
docs/reader_audit_report.md  (报告)
```

---

## 7. 推荐入库策略 (v3)

### 优先级 1: 学完 Cap.X 后可读 (5 本)

直接入库到 SQLite, 可作为"完成 LLPSI 主线后的奖励读物":

- `pugio_bruti` (FR Cap.48)
- `via_latina_romanorum` (FR Cap.52)
- `dooge_beginners_key` (FR Cap.50)
- `diocles_flora` (FR Cap.53)
- `regulus` (FR Cap.54)

### 优先级 2: 拉语为主 ({len([r for r in data if r['english_ratio'] < 0.30 and r['latin_word_count'] > 1000])} 本, 与 P1 有重叠)

适合做"主读物", 需要先做拉语段切分:

- `chickering` / `latin_lower_forms` / `hobbitus` (英<30%, 整本可读)
- `forum_lectiones` (英31%, 拉英混合, 教学价值 Cap.4 最高 55%)

### 优先级 3: D 类拉语段提取 ({len([r for r in data if r.get('latin_story_pages',0) > 0])} 本, {sum(r.get('latin_story_pages',0) for r in data)} 页)

先做拉语段提取 (`extract_d_class_latin.py`), 再入库:

- **最优先**: `latin_natural_method` (78 页)
- **次优先**: `dooge_beginners` / `dooge_beginners_2` (12 + 9 页)
- 其余按提取页数排序

### 优先级 4: 拉英对话手册 (1 本)

`conversational_latin` 需要**人工筛选对话段** (Cap.4 教学价值 43%):

- 415 页中, 每 2 页一段对话 (拉+英对照)
- 建议提取第 12/18/24/30/... 章的拉语段, 单独入库
- 适合做"口语/对话"训练

### 优先级 5: 暂不入库

- {len([r for r in data if r['english_ratio'] > 0.50])} 本英语为主 (英>50%): 仅作字典/参考
- 26 本 C 类高级古典: 已归档, 不入库

---

## 8. 后续动作建议

1. **数据已就绪**: `analysis_output/reader_report_data.json` 包含全部 55 本整合数据, 可直接用于报告生成
2. **下一步**: 编写 `scripts/extract_latin_segments.py` 提取 §C/D 中拉英混合读物的纯拉语段, 输出 `ocr_output/<slug>/segments_latin_only/`
3. **远期**: 启动 `llpsi-ingest-pipeline` SKILL, 将提取出的拉语段入库到 SQLite (现暂不启动, 详见 §6.1 算法说明)
4. **报告版本**: v3.0 — 替代 v2.0 的 A1/A2 模糊分级, 改用词汇量 + LLPSI 章节锚点
5. **元信息更新**: 26 本 C 类归档到 `archived_classics/`, 不在此报告中
"""

# 写入
out_path = Path('/Users/max/Downloads/Projects/LLPSI+++/docs/reader_audit_report.md')
out_path.write_text(report, encoding='utf-8')
print(f"[OK] {out_path}")
print(f"     Size: {out_path.stat().st_size:,} bytes, {len(report.splitlines())} lines")
