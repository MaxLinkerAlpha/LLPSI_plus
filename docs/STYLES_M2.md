# LLPSI+++ M2 · product 样式规范

> **文件位置**: `m2_output/product/style.css` + `m2_output/product/theme.js`
> **版本**: v3.7 (2026-06-12)
> **母版**: `HTML/Themes_AcademicJournal.html` (Caesar DBG 注释版) — 严格遵守其所有排版规则
> **核心原则**: 单列沉浸式 + 深夜模式 (酒红色调) + 实体标注 (无视觉标记) + 边注标注 (虚线标记)

---

## 0. HTML5 解析铁律 (v3.7)

> **这一节是修过两次悬浮注释泄漏后沉淀的硬性规范, 任何修改 HTML 都必须遵守。**

### 0.1 `.tip` 内部禁止任何 block 元素

`.tip` 是 `<span>` (inline / phrasing content), **绝对不能**在内部嵌套 `<div>`、`<p>`、`<ul>`、`<table>`、`<h*>` 等任何 flow content / block 元素。

**为什么**: HTML5 解析器在遇到 inline 元素包含 block 元素时, 会**自动闭合外层 `<span>`**, 让 block 元素逃逸为外层兄弟节点。一旦逃出 `.tip { display: none }` 的控制范围, 全部内容直接渲染在正文中, 出现"悬浮注释泄漏"。

**修复模式 (强制)**:
- ✅ `<span class="tip-grid">` + `display: inline-grid`
- ❌ `<div class="tip-grid">` + `display: grid` (v3.5 旧方案, 会泄漏)
- ❌ `<div>` / `<p>` / 任何 block 元素嵌在 `.tip` 内部

**对照示例** (v3.7 之前是 bug, 现在是规范):

```html
<!-- 正确 (v3.7+) -->
<span class="tip">
  <span class="tip-key">Declinatio · 1ª</span>
  <span class="tip-grid">
    <span class="tip-key">Lemma</span>
    <span><code>Itālia, -ae</code></span>
  </span>
  <span class="tip-lat">Praepositio: <code>in Italiā</code> (ablativus).</span>
</span>

<!-- 错误 (v3.5 旧方案, 已废弃) -->
<span class="tip">
  <span class="tip-key">Declinatio · 1ª</span>
  <div class="tip-grid">  <!-- 会逃出 .tip! -->
    ...
  </div>
</span>
```

### 0.2 tooltip 内容**不需要**段前空格

> **再强调一次**: tooltip 是行内文本框, `tip-key` / `tip-lat` / `tip-grid` 的内容**直接紧贴上一行**, 中间**不加**任何 `\n` 缩进、`<br>`、`<p>` 段首空格。tooltip 内的换行/缩进是 CSS 控制 (`display: block` + `margin`) 的, 不是 HTML 写的。

```html
<!-- 正确 (紧凑) -->
<span class="tip"><span class="tip-key">LOCUS · RŌMA</span><span class="tip-lat">Urbs et caput imperii Romani.</span></span>

<!-- 错误 (HTML 里塞了换行/空格) -->
<span class="tip">
  <span class="tip-key">LOCUS · RŌMA</span>
  <span class="tip-lat">Urbs et caput imperii Romani.</span>
</span>
```

### 0.3 验证清单 (修完 .tip 必查)

- [ ] 整个 HTML 内 `class="tip"` 后面, 紧接着的子元素都是 `<span>`
- [ ] 没有任何 `<div>` / `<p>` 直接出现在 `<span class="tip">` 内部
- [ ] 浏览器中 hover 实体/边注, 弹出后**完整**消失, 无文字残留
- [ ] 复制正文 `.two-col p` 的纯文本, 不含 `Lemma` / `Gen.` / `Decl.` / `Casus` 等元信息

### 0.4 边注触发器: † 脚注符号 (v3.7 决策)

> **历史问题**: v3.5–v3.6 用 `.margin .q` 显示触发词, 但当边注挂在已有 `.ent` 的词上时 (如 Itālia), `.q` 文本会**重复显示** (Itālia Itālia), 破坏沉浸感。

**v3.7 方案 (用户决策)**:
- 边注触发器统一改为 **† 脚注符号** (拉丁脚注传统符号, 剑标 dagger)
- 渲染方式: CSS `::before` 伪元素 (不写 HTML, 零 HTML 改动)
- 样式: `font-size: 0.7em; vertical-align: super; color: var(--accent); font-weight: 700`
- 旧 `border-bottom: 1px dashed` 虚线下划线**去掉** (避免和 † 叠加视觉过载)
- `.margin .q` 视觉不可见 (CSS `position: absolute; opacity: 0`), 保留 DOM 用于可访问性

**HTML 写法 (不变)**:
```html
<span class="margin">
  <span class="q">Itālia</span>           <!-- 视觉不可见, 保留语义 -->
  <span class="tip">...tooltip 内容...</span>
</span>
```

**CSS 渲染结果**:
```
正文... Itālia est. † 正文继续...
              ↑
        红色小字上标, hover 弹 tooltip
```

**禁止写法** (v3.7 起, 任何让 .q 可见的方案):
- ❌ `.margin { border-bottom: 1px dashed; }` 虚线 (v3.6 旧方案, 与 † 叠加)
- ❌ `.margin .q { color: var(--fg); }` 让 .q 显示
- ❌ 在 HTML 里把 .q 改为其它文字 (那会重新出现重复问题)

**验证清单**:
- [ ] `.margin` 视觉上**只**显示 † 符号, 不显示 `.q` 文本
- [ ] 复制正文纯文本, 不含 `†` 之后的边注 .q 内容
- [ ] hover 边注, † 变深酒红 (`var(--accent-2)`), 弹 tooltip

---

## 1. 排版骨架

| 元素 | 类名 | 规则 |
|------|------|------|
| 主体 | `body` | 36px 20px 48px 内边距 · Georgia 衬线 · 10.5pt |
| 页面 | `.page` | max-width 800px 居中 |
| 单列正文 | `.two-col` | **max-width 660px** + `text-align: justify` + `hyphens: auto` + 12pt + line-height 1.85 |
| 段落 | `.two-col p` | text-indent 1.5em + margin-bottom 0.85em |
| 段号 | `.sec-num` | `position: absolute; right: 100%` (段落右外侧) + 7.5pt 酒红 small-caps |
| 报头 | `.masthead` | 居中, journal-name / 黑线 / 红线 / title / doi / 底线 |
| 章节标题 | `.section-heading h2` | 上下 1px 黑线 + 11.5pt small-caps |
| 导航控件 | `.nav-controls` | 上/下页按钮 + 章节下拉, max-width 800px, 统一 Georgia 字体 |
| 语法板块 | `.grammatica` | max-width 660px, 统一 Georgia 字体, 5 条语法规则 |
| 拓展卡 | `.ll-ext-block` | 浅底色 + grid 网格 |
| 底部 | `.colophon` | 1px 黑线 + 红线 + small-caps |

> **重要**: v1 母版是双栏 (column-count: 2), 本版改为单列以增强沉浸感。

---

## 2. 主题系统 (CSS 变量驱动)

### 2.1 核心变量 (13 个)

```css
:root {
  --bg          /* 主背景 */
  --fg          /* 主文字 */
  --fg-soft     /* 副文字 */
  --fg-mute     /* 静音文字 */
  --accent      /* 强调色 (酒红) */
  --accent-2    /* 暗酒红 */
  --accent-soft /* 实体 hover 底色 */
  --rule        /* 黑色线 */
  --rule-soft   /* 灰线 */
  --bg-soft     /* 拓展卡/引用块底色 */
  --bg-card     /* 卡片底色 */
  --border-soft /* 边线色 */
  --tip-bg      /* tooltip 背景 */
  --tip-fg      /* tooltip 文字 */
  --shadow      /* tooltip 阴影 */
  --nav-bg      /* 导航背景 */
  --nav-active  /* 导航激活色 */
  --margin-line /* 边注虚线色 */
}
```

### 2.2 颜色对照

| 变量 | 浅色 (Dies) | 深夜 (Nox) |
|------|-----------|-----------|
| `--bg` | `#FFFFFF` | `#1A0E0E` (深酒红黑) |
| `--fg` | `#111111` | `#F5E8E8` (微酒米白) |
| `--accent` | `#B22A2A` (酒红) | `#E85D5D` (深夜酒红) |
| `--accent-soft` | `#FFF8E1` | `#2A1414` |
| `--tip-bg` | `#1A1A1A` | `#0F0606` |
| `--nav-bg` | `#F4F0E8` | `#2A1818` |
| `--margin-line` | `#888888` | `#6A5050` |

### 2.3 切换逻辑 (theme.js)

```js
// 优先级: localStorage > 跟随系统 (prefers-color-scheme)
var stored = localStorage.getItem('llpsi-theme');  // 'light' | 'dark' | null
var initial = stored || (prefersDark ? 'dark' : 'light');
root.setAttribute('data-theme', initial);

// 按钮切换
btn.addEventListener('click', () => {
  toggle + localStorage.setItem('llpsi-theme', current);
});

// 移动端: tap .ent / .margin 触发 tooltip
if ('ontouchstart' in window) {
  el.classList.toggle('tapped');
}
```

### 2.4 按钮

右上角固定按钮 `.theme-toggle`:
- 文案 `Dies` (light) / `Nox` (dark)
- 字号 8.5pt, border 1px, 圆点指示器

---

## 3. 实体标注系统 (2 类 + CSS-only tooltip)

### 3.1 核心原则

- **无视觉标记**: 实体标注 (`.ent`) 无任何下划线、角标、颜色变化
- **仅 hover 提示**: `cursor: help` + hover 时显示 tooltip
- **全拉丁语**: tooltip 内容使用拉丁语 (tip-key 为实体类型 + 词形, tip-lat 为拉丁语解释)

### 3.2 类与类型

| 类 | 含义 | 示例 tip-key |
|----|------|-------------|
| `.ent-loc` | 地名 (LOCUS) | `LOCUS · RŌMA` |
| `.ent-feat` | 山河 (FLŪMEN) | `FLŪMEN · NĪLUS` |

### 3.3 CSS 定义

```css
.ent {
  position: relative; cursor: help;
  /* 无视觉标记 — 无下划线/角标/颜色变化 */
}
.ent:hover, .ent:focus, .ent.tapped {
  background: var(--accent-soft);  /* 仅 hover 时微亮底色 */
  border-radius: 2px;
}
```

### 3.4 Tooltip 结构

```css
.ent .tip {
  position: absolute; bottom: 130%; left: 0;
  background: var(--tip-bg); color: var(--tip-fg);
  font-size: 9pt; line-height: 1.4; padding: 6px 10px;
  min-width: 180px; max-width: 280px;
  box-shadow: var(--shadow);
}
.ent .tip::after {  /* 向下三角箭头 */
  content: ""; position: absolute; top: 100%; left: 12px;
  border: 4px solid transparent; border-top-color: var(--tip-bg);
}
```

### 3.5 HTML 结构

```html
<span class="ent ent-loc">
  <span class="q">Rōma</span>
  <span class="tip">
    <span class="tip-key">LOCUS · RŌMA</span>
    <span class="tip-lat">Urbs et caput imperii Romani. In Italia sita est.</span>
  </span>
</span>
```

---

## 4. 边注标注系统 (.margin)

### 4.1 核心原则

- **† 脚注符号触发器** (v3.7+): CSS `::before` 渲染小字上标, 酒红色 (取代 v3.6 虚线下划线)
- **左侧 accent 竖线**: tooltip 左侧 `3px solid var(--accent)` 竖线 (区别于实体 tooltip)
- **更大 tooltip**: max-width 400px (容纳长语法说明)
- **code 样式**: tooltip 内 `<code>` 元素使用 accent 色 + 半透明背景
- **.q 不可见**: `.margin .q` 视觉不可见, 保留 DOM 节点用于可访问性 (详见 §0.4)

### 4.2 CSS 定义

```css
.margin {
  position: relative; cursor: help;
  padding: 0 2px;
  /* v3.7: 去掉 border-bottom 虚线, 改用 ::before 渲染 † */
}
.margin::before {
  content: "†";
  font-size: 0.7em; vertical-align: super; line-height: 1;
  color: var(--accent); font-weight: 700;
  margin: 0 2px 0 1px;
  transition: color 0.3s ease;
}
.margin .q {  /* v3.7: 视觉不可见, 保留 DOM */
  position: absolute; width: 1px; height: 1px;
  opacity: 0; pointer-events: none; overflow: hidden;
  clip: rect(0, 0, 0, 0);
}
.margin:hover, .margin:focus, .margin.tapped {
  background: var(--accent-soft);
  border-radius: 2px;
}
.margin:hover::before { color: var(--accent-2); }
.margin .tip {
  max-width: 400px; font-size: 9pt; line-height: 1.5;
  padding: 10px 14px;
  border-left: 3px solid var(--accent);  /* 区别于 entity */
}
.margin .tip code {
  background: rgba(255,255,255,0.1);
  font-family: Georgia, serif; font-style: italic;
  color: var(--accent);
}
```

### 4.3 HTML 结构

```html
<span class="margin">
  <span class="q">Itālia</span>          <!-- 视觉不可见, 保留语义 -->
  <span class="tip">
    <span class="tip-key">-a -ae · 1ª Decl.</span>
    <span class="tip-lat"><code>Itālia, -ae</code> f. — Prima declinatio...</span>
  </span>
</span>
```

---

## 5. 导航控件 (v3.3)

```css
.nav-controls {
  max-width: 800px; margin: 0 auto 18px;
  display: flex; justify-content: space-between;
  padding: 8px 14px; background: var(--nav-bg);
  border-top: 1px solid var(--accent);
  border-bottom: 1px solid var(--accent);
  font-family: Georgia, "Times New Roman", serif;
}
```

- 上页按钮 `.nav-prev` (← PRAECEDENS)
- 下页按钮 `.nav-next` (SEQUENS →)
- 章节下拉 `.nav-chapter select` (FR 30 章 + RA 26 章)

---

## 6. Grammatica 板块 (v3.3)

```css
.grammatica {
  max-width: 660px; margin: 28px auto;
  padding: 20px 24px; background: var(--bg-soft);
  border-top: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  font-family: Georgia, "Times New Roman", serif;
}
```

- 标题 `.gram-heading`: small-caps 居中
- 规则标题 `.gram-rule-title`: accent 色 small-caps
- 规则正文 `.gram-rule-body`: 9.5pt, justify
- 边注列表 `.gram-margin-list`: 双栏 grid

### 6.1 语法示例 grid (v3.7+) — D / E 规则专用

> **用途**: 把规则 D (形容词变格 6 例) 与规则 E (in + abl. 5 例) 的密集逗号分隔示例, 拆分为可扫描的网格卡片。

**CRAP 设计依据**:
- **Proximity (邻近)**: 同组示例物理上紧密聚成一格, 一眼扫完
- **Repetition (重复)**: 单元格视觉一致, 形成"公式卡"节奏
- **Contrast (对比)**: 单元格 `var(--accent-soft)` 微底色与正文 12pt 形成层次

**CSS 定义**:
```css
.grammatica .gram-examples {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* D 规则: 3列 × 2行 */
  gap: 4px 8px;
  margin: 6px 0 4px; padding: 0; list-style: none;
}
.grammatica .gram-examples.cols-5 {
  grid-template-columns: repeat(5, 1fr);  /* E 规则: 5列 × 1行 */
}
.grammatica .gram-examples li {
  background: var(--accent-soft);
  border-radius: 2px;
  padding: 3px 6px;
  text-align: center;
  font-size: 9pt; line-height: 1.35;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.grammatica .gram-examples li code {
  background: transparent; padding: 0;
  font-family: Georgia, serif; font-style: italic;
  font-size: 9pt; color: var(--fg);
}
```

**HTML 写法 (D 规则)**:
```html
<div class="gram-rule-body">
  Adiectīva cum nōmine in genere, numerō, cāsū conveniunt:
  <ul class="gram-examples">
    <li><code>fluvius magnus</code></li>
    <li><code>fluviī magnī</code></li>
    <li><code>īnsula magna</code></li>
    <li><code>īnsulae magnae</code></li>
    <li><code>oppidum magnum</code></li>
    <li><code>oppida magna</code></li>
  </ul>
  Contrārium: <em>parvus, -a, -um</em>. Cōpia: <em>multus / multī</em>.
</div>
```

**HTML 写法 (E 规则, 5列用 .cols-5 修饰)**:
```html
<ul class="gram-examples cols-5">
  <li><code>in Itāliā</code></li>
  <li><code>in Graeciā</code></li>
  <li><code>in Eurōpā</code></li>
  <li><code>in oppidō</code></li>
  <li><code>in īnsulā</code></li>
</ul>
```

**响应式** (@media ≤ 720px): D 转 2 列, E 转 3 列 (cols-5)。

**禁止写法**:
- ❌ 在 .gram-examples 内嵌 block 元素 (违反 §0.1)
- ❌ 单元格内换行 (`<br>`) — 用 nowrap + ellipsis 让长示例自然截断
- ❌ 仍用逗号分隔长字符串 (丧失视觉扫描性)

---

## 7. 拉丁化规范

### 7.1 全拉丁语规则

HTML 中所有可见内容必须使用拉丁语:
- 正文: 带长音的标准拉丁语
- 实体 tooltip: tip-key (类型+词形) + tip-lat (拉丁语解释)
- 边注 tooltip: tip-key (语法标签) + tip-lat (拉丁语语法说明)
- 导航: PRAECEDENS / SEQUENS / Capitulum
- 语法板块: 标题 + 规则 + 示例全部拉丁语
- 拓展卡: 标题 "Capiti Coniuncta" + 按钮 "Aperire"
- 主题按钮: Dies / Nox
- 报头: 全部拉丁语

### 7.2 报头

| 元素 | 拉丁文 |
|------|--------|
| `.journal-name` | `LLPSI+++ · Familia Romana` |
| `.title` | (章节名, 如 Imperium Romanum) |
| `.doi` | `FR · Cap. I · pp. 9–14` |

### 7.3 元信息标签

- `Grammatica Latina` — 语法板块
- `Capiti Coniuncta` — 拓展阅读
- `Aperire` — 展开全文
- `PRAECEDENS` / `SEQUENS` — 上/下页
- `Capitulum` — 章节选择

---

## 8. 响应式

| 断点 | 行为 |
|------|------|
| ≤ 720px | `.two-col` 11pt, 导航换行, 拓展卡单栏, 语法边注列表单栏, 移动端 tap 替代 hover |
| ≤ 480px | body padding 18px 12px 28px, title 15pt |

---

## 9. 打印优化 (@media print)

```css
@media print {
  .theme-toggle, .nav-controls { display: none; }
  .ent .tip, .margin .tip { display: none !important; }
  .ll-ext-block, .grammatica { page-break-before: always; }
  body { background: #fff; color: #000; }
}
```

---

## 10. 不可触碰清单

如需修改以下元素, **必须**先与用户确认:

1. **报头结构** (journal-name / 黑线 / 红线 / title / doi / 底线)
2. **实体类名** (ent-loc / ent-feat) — 数据 + CSS 双向绑定
3. **CSS 变量名** (17 个) — 避免子组件失效
4. **主题切换 API** (`data-theme="dark"` + `localStorage["llpsi-theme"]`)
5. **段号位置** (右外侧 absolute)
6. **实体无标记原则** (.ent 不得有任何视觉标记)
7. **边注 † 触发器** (v3.7: `.margin::before { content: "†" }`, 已弃用 v3.6 虚线方案)
8. **全拉丁语规则** (HTML 中所有可见内容)
9. **HTML5 解析铁律** (§0.1-0.4, .tip 内禁止 block 元素, .margin .q 不可见)

---

## 11.5 OCR 待修事项 (v3.7+1 用户审查发现 · 2026-06-12)

> **状态**: 已记录, 暂未修复, 待后续修。
> **用户原话**: "有一长段正文，以及语法部分的正文是错误的内容"。

### 11.5.1 m2_master.json OCR 字符错误 (高频)

来源: `m2_output/data/m2_master.json` 中 `text_raw` 字段 (PDF OCR 输出, 未经清洗)。

| 章节 | 错误字符串 | 正确目标 | 影响 | 优先级 |
|------|------------|----------|------|--------|
| **Cap.1** | `Tibe- ris` (跨行断词) | `Tiberis` | 1 处 | 低 |
| **Cap.2** | `Ifllia`, `lfllia`, `lIilia` | `Iulia` (名) | 多处 | **高** |
| **Cap.2** | `Iflliae`, `lflliae` | `Iuliae` (属格) | 多处 | **高** |
| **Cap.3** | `Marcum` 拼写校验通过, 但缺 § 标点 | 需对照 PDF | 多处 | 中 |
| **Cap.1** | `text_clean` 字段空 (`""`) | 需 fill_clean.py 重新生成 | 全章 | **高** |

### 11.5.2 语法板块正文错误 (用户指认)

来源: `m2_output/product/cap_I.html` 中 `<section class="grammatica">` 区域。

| 规则 | 现状 | 疑点 | 优先级 |
|------|------|------|--------|
| **A. Singulāris et Plūrālis** | 手写合成, 含 lemma/gen/decl/formae 5 列表 | 表头是否完全对应 LLPSI 母版? | 中 |
| **B. Verbum esse** | 6 人称变形表 (ego sum ... eī sunt) | 拉丁原文是否完全照搬 LLPSI Cap.1 练习? | **高** |
| **C. Interrogātiō** | -ne / num / ubi-quid 三条 | LLPSI Cap.1 是否实际呈现这些公式? | **高** |
| **D. Adiectīva** | 6 个示例 (fluvius magnus ...) | **已 grid 化, 但示例与 LLPSI 母版是否一致? 待对照** | **高** |
| **E. in + ablātīvō** | 5 个示例 (in Itāliā ...) | **示例与 LLPSI 母版是否一致? 待对照** | **高** |

### 11.5.3 修复路径 (建议, 留待用户确认)

```
1. 拉取 PDF 高清版 (source/LLPSI_core_*.pdf)
2. 用 pdftotext -layout 提取 layout-aware 文本
3. 逐章校对, 输出修正版到 m2_master.json:
     - text_raw:  保留原始 OCR (含 Ifllia 等)
     - text_clean: 修正版 (Iulia, Tiberis, ...)
4. 重新跑 build.py 生成 product/cap_X.html
5. 语法板块: 优先校对 D/E 规则示例, 确认与 LLPSI 母版完全一致
6. 跑 verify.py 确认 19/19 通过
```

### 11.5.4 设计原则提示 (v3.8+)

- **设计已就绪, 内容待校**: 当前 cap_I.html 的视觉规范 (grid, 卡片, 边注, tooltip) 已达到设计基线
- **新方向 (M3)**: 转向"拓展读物作为正文", 不再电子化 LLPSI 本体 → 当前 OCR 问题影响减弱, 但仍需把已生成的 3 章校对完
- **不删除 cap_I.html**: 留作 M2 设计规范的"参考实现"

---

## 12. 验证脚本

```bash
python3 m2_output/verify.py
```

应输出 19/19 通过、100%。

---

## 13. 版本历史

| 版本 | 日期 | 关键变更 |
|------|------|---------|
| v1.0 | 2026-06-11 | 初版 (v1_academic 目录 + 双栏) |
| v2.0 | 2026-06-11 | 严格遵守母版排版规则 (双栏 + 报头 + 实体 + 底部 3 区) |
| v3.0 | 2026-06-11 | 单列沉浸式 + 深夜模式 (CSS 变量驱动) + 全拉丁化 |
| v3.1 | 2026-06-11 | 实体标注去视觉标记 + 边注虚线标记 |
| v3.2 | 2026-06-11 | 导航控件 + Grammatica 板块 + 拓展卡 |
| v3.3 | 2026-06-11 | 全部拉丁化 (tooltip/标注/语法) + nav/Grammatica 统一正文风格 |
| v3.4 | 2026-06-11 | 边注 tooltip 左侧 accent 竖线 + code/em 元素样式优化 + 全拉丁语完检 |
| v3.5 | 2026-06-12 | tooltip 内多类型排版 (`.tip-grid` grid 布局) + Grammatica 表格化 (但 `.tip-grid` 用 `<div>` 留泄漏隐患) |
| v3.6 | 2026-06-12 | 边注 1px dashed 下划线 + visibility 继承链 |
| **v3.7** | **2026-06-12** | **根绝 tooltip 泄漏 (HTML5 解析铁律): `<div class="tip-grid">` → `<span class="tip-grid">` + `display: inline-grid`. 边注触发器改 † 脚注符号 (用户决策): `.margin::before { content:"†" }`, 去掉虚线下划线, `.margin .q` 视觉不可见. 栏宽统一 / 语法正文 12pt / 底部翻页 / doi 内联 / 卡片精简. 追加 §0 规范. 拓展卡片对齐 (.ll-ext-book width:100% + .ll-ext-full-body 去左右 padding). 语法 D/E 规则 grid 化 (.gram-examples, D=3列, E=5列). 翻页控件唯一化 (删除 colophon 后的重复 nav-bottom, 保留 grammar 与 ll-ext-block 之间的版本)** |
| **v3.7+1** | **2026-06-12** | **语法示例去底色 (用户要求 #1): `.gram-examples li` background 改 transparent + 0.5px 细线替代. 红色 † 真正拉近单词 (用户要求 #3): 改 `.margin` 自身 `margin: 0 -0.12em` (而非 ::before), 抵消 HTML 文本节点空格的视觉间隙. tooltip 顶格左对齐规则 (用户要求 #2) 已自动遵守 (§0.2). 同步 §11.5 OCR 待修事项到文档 (用户要求 #4, 后续再修)** |