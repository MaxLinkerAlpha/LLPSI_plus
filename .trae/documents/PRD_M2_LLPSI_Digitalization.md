# LLPSI+++ M2 PRD · v3.0（正式版路线图）

> **文档版本**: v3.0
> **创建日期**: 2026-06-11
> **对应里程碑**: M2（LLPSI 电子化）
> **状态**: 开发中（专注第一章打磨）
> **关键变化**: v2.0 的 3 版本并行策略已被废弃；v3.0 聚焦单版本（酒红主题 + 单列正文 + 实体标注 + 边注标注 + Grammatica 板块 + 拓展阅读卡片）

---

## 〇、本版（v3.0）与 v2.0 的关键差异

| 项 | v2.0 策略 | v3.0 修正 |
|----|----------|----------|
| 版本数量 | 3 个版本并行 | **单版本**（酒红主题 + 沉浸阅读） |
| 正文布局 | 双栏 `.two-col` | **单列** `.two-col`（max-width 660px + justify + hyphens） |
| 实体标注 | 4 类 `.ent-loc/.ent-gen/.ent-feat/.ent-num` + 角标 L¹/G¹/F¹/N¹ | **简化**：仅 `.ent` + 统一 tooltip，**去所有视觉标记**（无下划线/角标/fl.） |
| 边注标注 | 无独立样式 | **新增 `.margin`** 用 1px dashed underline + 独立 tooltip 样式 |
| Grammatica 板块 | 无 | **新增** 独立语法区（在正文与拓展阅读之间） |
| 拓展阅读 | 每章 5 张卡 | **37 张卡** + 2 列网格 + 紧凑布局 |
| Apparatus/Biblio | 底部 3 区独立列出 | **融入** 卡片或 tooltip（不单独列出） |
| 夜间模式 | 橙色调 | **酒红** `#1A0E0E` 深色主题 |
| 导航 | 无 | **导航控件**（上/下页 + 章节下拉 + FR/RA 连续章节） |
| 主题切换 | 无动画 | **fade 动画**（0.4s CSS transition） |
| 标题副标题 | 副标题无评估 | **原文规范** + 副标题必要性评估 |

---

## 一、设计规范：v3.0 正式版样式

### 1.1 整体规格（style.css v3.2）

```css
html, body {
  background: var(--bg);
  color: var(--fg);
  font-family: Georgia, "Times New Roman", "Iowan Old Style",
               "Source Han Serif SC", "Noto Serif CJK SC", serif;
  font-size: 10.5pt;
  line-height: 1.5;
  /* 主题切换 fade 动画 */
  transition: background 0.4s ease, color 0.4s ease;
}
.page { max-width: 800px; margin: 0 auto; }
body { padding: 36px 20px 48px; }
```

### 1.2 主题变量（CSS Variables）

```css
/* 日间模式 */
:root {
  --bg:          #FFFFFF;
  --fg:          #111111;
  --accent:      #B22A2A;          /* 酒红 */
  --accent-2:    #8B1F1F;
  --accent-soft: #FFF8E1;
  --margin-line: #888888;         /* 边注虚线色 */
  --tip-bg:      #1A1A1A;
}

/* 夜间模式（酒红黑） */
[data-theme="dark"] {
  --bg:          #1A0E0E;
  --fg:          #F5E8E8;
  --accent:      #E85D5D;          /* 深夜酒红 */
  --accent-2:    #C44848;
  --accent-soft: #2A1414;
  --margin-line: #6A5050;
  --tip-bg:      #0F0606;
}
```

### 1.3 报头（.masthead）

```
[LLPSI+++ · Familia Romana]           <- .journal-name small-caps
═══════════════════════════════      <- .rule-black (1px 黑)
───────────────────────────────      <- .rule-red (1px 酒红)
[Imperium Romanum]                   <- h1.title 22pt 居中
[FR · Cap. I · p. 9–14]              <- .doi monospace
═══════════════════════════════      <- .rule-bottom (1px 黑)
```

### 1.4 章节标题（.section-heading）

```
═══════════════════════════════
       [CAPITULUM PRIMVM]            <- small-caps 大字距
═══════════════════════════════
```

### 1.5 单列正文（核心）

```css
.two-col {
  max-width: 660px; margin: 0 auto;
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
  font-size: 12pt;
  line-height: 1.85;
}
.two-col p {
  margin: 0 0 0.85em;
  text-indent: 1.5em;
  font-size: 12pt;
  line-height: 1.85;
}
.sec-num {
  position: absolute; right: 100%; margin-right: 0.6em;
  font-weight: 700; color: var(--accent); font-size: 7.5pt;
  font-variant: small-caps;
}
```

每段：`<p><span class="sec-num">[N]</span>...正文...</p>`

### 1.6 实体标注（.ent）— v3.2 完全去视觉化

**设计原则**：侵入性最小化，避免打断沉浸阅读

```css
.ent {
  position: relative;
  cursor: help;
  /* 完全无视觉标注（无下划线/角标/fl.） */
  transition: background 0.3s ease, color 0.3s ease;
}
.ent:hover, .ent:focus, .ent.tapped {
  background: var(--accent-soft);
  border-radius: 2px;
}
```

**HTML 结构**：
```html
<span class="ent ent-loc">
  <span class="q">Roma</span>
  <span class="tip">
    <span class="tip-key">LOCUS · ROMA</span>
    <span class="tip-zh">罗马 — 罗马帝国首都</span>
  </span>
</span>
```

**实体类型**（仅 tooltip key 区分，视觉统一）：
- `.ent-loc` — 地名（LOCUS）
- `.ent-feat` — 地理特征（FLUMEN、INSULA 等）
- `.ent-gen` — 家族/民族（GENS）

### 1.7 边注标注（.margin）— 与实体区分

**设计原则**：用更轻的虚线，与实体标注视觉上可区分

```css
.margin {
  position: relative;
  cursor: help;
  border-bottom: 1px dashed var(--margin-line);
  padding-bottom: 1px;
  transition: background 0.3s ease, border-color 0.3s ease;
}
.margin:hover, .margin:focus {
  background: var(--accent-soft);
  border-bottom-color: var(--accent);
  border-radius: 2px;
}
```

**HTML 结构**（语法说明融于 tooltip）：
```html
<span class="margin">
  <span class="q">Italia</span>
  <span class="tip">
    <span class="tip-key">-a -ae · 1ª Dec.</span>
    Prima declinatio: <code>Italia, -ae</code> f.
  </span>
</span>
```

### 1.8 Grammatica 板块

```css
.grammatica {
  max-width: 700px; margin: 28px auto; padding: 20px 24px;
  background: var(--bg-soft);
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
}
```

位于**正文之后、拓展阅读之前**，包含：
- A. Singularis et Pluralis
- B. Verbum esse
- C. Interrogatio
- D. Adiectiva
- E. Praepositio in

### 1.9 拓展阅读卡片（.ll-ext-block）

```css
.ll-ext-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 6px;
}
.ll-ext-card {
  background: var(--bg-card);
  border: 1px solid var(--border-soft);
  border-left: 2px solid var(--accent);
  padding: 6px 8px; font-size: 8pt;
}
```

- 37 张卡（按相似度 score 排序）
- 2 列网格布局（响应式）
- 紧凑设计（避免占据过多空间）

### 1.10 导航控件（.nav-controls）

```css
.nav-controls {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 14px;
  background: var(--nav-bg);
  border-top: 1px solid var(--accent);
  border-bottom: 1px solid var(--accent);
}
```

- 上一页 / 下一页（small-caps + 左右箭头）
- 章节下拉（FR 30 章 + RA 26 章，连续编号）
- 当前章节高亮

### 1.11 响应式

```css
@media (max-width: 720px) {
  .two-col { font-size: 11pt; }
  .ll-ext-grid { grid-template-columns: 1fr; }
  .grammatica .gram-margin-list { grid-template-columns: 1fr; }
}
```

---

## 二、命名规范（与原文一致）

| 规范 | 说明 |
|------|------|
| 书名 | **LLPSI+++**（不要只写 LLPSI） |
| 上册 | **Familia Romana (FR)**（不要写"卷一/卷1"） |
| 下册 | **Roma Aeterna (RA)**（不要写"卷二/卷2"） |
| 副标题 | 遵照原文（评估必要性） |

---

## 三、MVP 范围（FR Cap. I）

- **数据**：FR Cap. 1 全文 + 边注 + 37 张拓展阅读卡
- **单 HTML**：`cap_I.html` + `style.css` + `theme.js`
- **导航**：FR Cap. 1-30 + RA Cap. 31-56（连续章节）
- **Grammatica**：名词/动词/疑问/形容词/介词 5 个语法点
- **验收报告**：`m2_output/verify.py`（结构验收）

---

## 四、验收清单（v3.0 必检项）

| 编号 | 项 | 状态 |
|------|------|------|
| B1 | 单列正文（max-width 660px + justify + hyphens + 1.5em indent） | ✅ |
| B2 | `.sec-num` 段号 [N] 红色加粗 | ✅ |
| B3 | `.ent` 无视觉标注（无下划线/角标/fl.） | ✅ |
| B4 | `.margin` 边注虚线 + 独立 tooltip | ✅ |
| B5 | 夜间模式酒红主题（`#1A0E0E` + `#E85D5D`） | ✅ |
| B6 | 主题切换 fade 动画（0.4s） | ✅ |
| B7 | `.masthead` 报头（期刊名/双线/标题/DOI） | ✅ |
| B8 | `.nav-controls` 导航控件（上/下页 + 章节下拉） | ✅ |
| B9 | `.grammatica` 语法板块（正文与拓展之间） | ✅ |
| B10 | `.ll-ext-block` 37 张拓展阅读卡（2 列网格） | ✅ |
| B11 | Apparatus/Biblio 融入卡片或 tooltip | ✅ |
| B12 | LLPSI+++ 命名（无 LLPSI 单独出现） | ✅ |
| B13 | FR/RA 描述正确（无"卷几"） | ✅ |
| B14 | 移动端单栏（max-width 720px） | ✅ |
| B15 | 打印样式（.theme-toggle/.nav-controls 隐藏） | ✅ |

---

## 五、后续路线

- **M2.1**：Grammatica 内容精校
- **M2.2**：FR Cap. 2-30 + RA Cap. 31-56 批量生成
- **M2.3**：重新 OCR FR 全文（长音保留 + 正文/边注分离）
- **M2.4**：实体词典扩充（200+ lemma）
- **M2.5**：响应式调优 + 移动端体验

---

## 六、版本

- PRD v3.0（正式版）· 2026-06-11
- 状态：M2 开发中（专注第一章打磨）
