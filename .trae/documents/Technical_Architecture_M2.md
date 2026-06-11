# LLPSI+++ M2 技术架构 · LLPSI 电子化

> **文档版本**: v3.0
> **创建日期**: 2026-06-11
> **对应 PRD**: [PRD_M2_LLPSI_Digitalization.md](PRD_M2_LLPSI_Digitalization.md) v3.0

---

## 〇、本版（v3.0）与 v1.1 的关键差异

| 项 | v1.1 策略 | v3.0 修正 |
|----|----------|----------|
| 版本数量 | 3 个版本并行 | **单版本**（酒红主题 + 沉浸阅读） |
| CSS 策略 | 3 套独立 CSS | **单 CSS**（style.css v3.2）+ CSS Variables |
| 正文布局 | 双栏 column-count: 2 | **单列**（max-width 660px + justify + hyphens） |
| 实体标注 | 4 类 + 上标 L¹/G¹/F¹/N¹ | **去视觉标记**：仅 `.ent` + CSS-only tooltip |
| 边注标注 | 无独立样式 | **新增 `.margin`**（1px dashed + 独立 tooltip） |
| Grammatica | 无 | **新增 Grammatica 板块**（正文与拓展之间） |
| 夜间模式 | 橙色调 | **酒红** `#1A0E0E` 深色主题 |
| 主题动画 | 无 | **fade 动画**（0.4s CSS transition） |
| 导航 | URL 参数 `?chapter=N` | **导航控件**（上/下页 + 章节下拉 + FR/RA 连续） |

---

## 一、技术选型

| 类别 | 选型 | 理由 |
|------|------|------|
| **核心栈** | 纯 HTML + CSS + 原生 JS（ES2020+） | 静态交付、零构建、与 M1 流水线一致 |
| **CSS 策略** | 单 CSS（style.css）+ CSS Variables | 简化维护，酒红/日间主题切换 |
| **夜间模式** | CSS Variables + `data-theme` 属性 | 原生支持，无 JS 框架依赖 |
| **主题动画** | CSS `transition` 0.4s ease | 平滑淡入淡出效果 |
| **字体** | Georgia + Times New Roman + CJK 衬线 | 拉丁经典 + 中文支持 |
| **图标** | Unicode 符号（☀ ☾） | 无需 CDN 依赖 |
| **数据** | 内嵌 HTML（`<script type="application/json">`） | 避免额外 HTTP 请求 |
| **构建工具** | 无 | 单文件 / 多 HTML 部署即可 |

> **为什么不选 React/Vue？** 单页静态展示 + 章节内容，零路由需求；过框架化违反 KISS 原则。

---

## 二、目录结构（v3.0）

```
LLPSI+++/
├── m2_output/
│   ├── product/                        # M2 最终交付
│   │   ├── cap_I.html                 # FR Cap. I（第一章）
│   │   ├── cap_II.html                # FR Cap. II（后续章节，待生成）
│   │   ├── ...
│   │   ├── style.css                  # 统一样式表 v3.2
│   │   └── theme.js                   # 主题切换脚本 v3.2
│   │
│   ├── reocr/                         # 重新 OCR 产出
│   │   └── fr_cap1/                   # FR Cap.1 重新 OCR
│   │       ├── method_clean_main.txt  # 清洗后的正文
│   │       └── method_clean_marg.txt # 清洗后的边注
│   │
│   └── data/                          # 数据文件
│       └── m2_master.json             # 主数据文件
│
├── analysis_output/                    # M1 产出（用于拓展阅读）
│   └── LLPSI_Insights.html             # 拓展阅读分析
│
├── scripts/                            # 构建脚本
│   └── build_m2_html.py               # HTML 生成脚本
│
├── .trae/documents/                    # 文档
│   ├── PRD_M2_LLPSI_Digitalization.md  # PRD v3.0
│   └── Technical_Architecture_M2.md    # 本文件 v3.0
│
└── ocr_output/                         # 原始 OCR（输入）
```

---

## 三、文件说明

### 3.1 style.css v3.2

**核心功能**：
- CSS Variables 主题变量（日间/夜间）
- `.ent` 实体标注（去视觉标记，仅 hover 显示 tooltip）
- `.margin` 边注标注（1px dashed 下划线）
- `.grammatica` 语法板块样式
- `.ll-ext-*` 拓展阅读卡片样式
- `.nav-controls` 导航控件样式
- 响应式布局（720px / 480px 断点）
- 打印样式（隐藏交互元素）

**CSS Variables**：
```css
:root {
  --bg: #FFFFFF;
  --fg: #111111;
  --accent: #B22A2A;       /* 酒红 */
  --accent-soft: #FFF8E1;
  --margin-line: #888888;  /* 边注虚线色 */
  --tip-bg: #1A1A1A;
}
[data-theme="dark"] {
  --bg: #1A0E0E;           /* 深酒红黑 */
  --fg: #F5E8E8;
  --accent: #E85D5D;       /* 深夜酒红 */
  --accent-soft: #2A1414;
  --margin-line: #6A5050;
  --tip-bg: #0F0606;
}
```

### 3.2 theme.js v3.2

**核心功能**：
- 主题初始化（localStorage / 系统偏好）
- 主题切换（按钮点击 + fade 动画）
- 移动端 tap 触发 tooltip

**关键代码**：
```javascript
function applyTheme(name, persist) {
  root.setAttribute('data-theme', name);
  btn.textContent = name === 'dark' ? '☾ Nox' : '☀ Dies';
  if (persist) localStorage.setItem(KEY, name);
}

// 切换动画：60ms 延迟让视觉感知过渡起点
btn.addEventListener('click', function () {
  document.body.style.transition = 'background 0.4s ease, color 0.4s ease';
  setTimeout(function () { applyTheme(next, true); }, 60);
  setTimeout(function () { document.body.style.transition = ''; }, 460);
});
```

### 3.3 cap_I.html

**HTML 结构**：
1. `<nav class="nav-controls">` — 导航控件
2. `<header class="masthead">` — 报头
3. `<div class="section-heading">` — 章节标题
4. `<article class="two-col">` — 单列正文
5. `<section class="grammatica">` — 语法板块
6. `<section class="ll-ext-block">` — 拓展阅读
7. `<footer class="colophon">` — 尾注

---

## 四、组件设计

### 4.1 实体标注（.ent）

**设计原则**：侵入性最小化，避免打断沉浸阅读

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

**CSS 样式**：
```css
.ent {
  position: relative;
  cursor: help;
  /* 完全无视觉标记 */
  transition: background 0.3s ease, color 0.3s ease;
}
.ent:hover, .ent:focus, .ent.tapped {
  background: var(--accent-soft);
  border-radius: 2px;
}
```

**Tooltip**：
```css
.ent .tip {
  visibility: hidden; opacity: 0; transition: opacity 0.2s ease;
  position: absolute; bottom: 130%; left: 0;
  background: var(--tip-bg); color: var(--tip-fg);
  font-size: 9pt; padding: 6px 10px; border-radius: 2px;
  z-index: 100; pointer-events: none;
  min-width: 180px; max-width: 280px;
}
.ent:hover .tip, .ent:focus .tip, .ent.tapped .tip {
  visibility: visible; opacity: 1;
}
```

### 4.2 边注标注（.margin）

**设计原则**：用更轻的虚线，与实体标注视觉区分

**CSS 样式**：
```css
.margin {
  position: relative; cursor: help;
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

### 4.3 Grammatica 板块

**HTML 结构**：
```html
<section class="grammatica">
  <div class="gram-heading">Grammatica Latina · Cap. I</div>
  <div class="gram-rule">
    <div class="gram-rule-title">A. Singularis et Pluralis</div>
    <div class="gram-rule-body">
      Nomen Latinum habet duos numeros...
      <ul class="gram-margin-list">
        <li><strong>fluvius</strong> — 1ª/2ª Dec. m.</li>
      </ul>
    </div>
  </div>
</section>
```

### 4.4 拓展阅读卡片

**HTML 结构**：
```html
<article class="ll-ext-card">
  <header class="ll-ext-head">
    <span class="ll-ext-score">1.00</span>
    <span class="ll-ext-book">Fabellae Latinae</span>
  </header>
  <p class="ll-ext-preview">In imperio Romano multae sunt...</p>
  <div class="ll-ext-meta">t80 Cap.1 · 72 tokens</div>
  <details class="ll-ext-toggle">
    <summary>Aperire</summary>
    <div class="ll-ext-full-body">完整内容...</div>
  </details>
</article>
```

**CSS 样式**：
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

### 4.5 导航控件

**HTML 结构**：
```html
<nav class="nav-controls">
  <a class="nav-prev" href="cap_XXX.html" aria-label="Previous chapter">PRAECEDENS</a>
  <div class="nav-chapter">
    <label for="chap-select">Capitulum</label>
    <select id="chap-select" onchange="if(this.value) window.location.href=this.value;">
      <optgroup label="Familia Romana (上册)">
        <option value="cap_I.html" selected>Cap. I — Imperium Romanum</option>
        ...
      </optgroup>
      <optgroup label="Roma Aeterna (下册)">
        ...
      </optgroup>
    </select>
  </div>
  <a class="nav-next" href="cap_II.html" aria-label="Next chapter">SEQUENS</a>
</nav>
```

---

## 五、性能策略

| 指标 | 目标 | 方案 |
|------|------|------|
| 首次加载 | < 2s | 单文件 + 内嵌样式，无额外请求 |
| 主题切换 | < 100ms | 纯 CSS transition，无 JS 计算 |
| Hover tooltip | < 50ms | 纯 CSS `:hover`，无 JS |
| 文件大小 | < 100KB/HTML | 精简 CSS，零外部依赖 |
| 拓展卡片渲染 | < 100ms | 静态 HTML，无需 JS 渲染 |

---

## 六、实施分阶段

### Phase M2.1（当前：FR Cap. I 打磨）
1. 样式表定稿（style.css v3.2 ✅）
2. 导航控件完善 ✅
3. Grammatica 内容精校
4. 主题切换动画完善 ✅

### Phase M2.2（FR Cap. 2-30）
1. HTML 批量生成（build_m2_html.py）
2. 章节链接连续化
3. 跨章实体标注一致性

### Phase M2.3（RA Cap. 31-56）
1. RA 章节接入
2. 连续编号（Cap. 1-56）
3. RA 特有内容（语法/练习）整合

### Phase M2.4（重新 OCR）
1. Tesseract hOCR 提取正文/边注坐标
2. pypdf + Tesseract 分离正文与边注
3. 长音符号保留
4. 替换现有 OCR 内容

### Phase M2.5（实体词典扩充）
1. 实体词典扩充至 200+ lemma
2. 边注内容全面补全
3. Grammatica 内容扩展

---

## 七、风险与未决项

| 项目 | 备注 | 解决时机 |
|------|------|---------|
| OCR 长音缺失 | 现有 OCR 无长音 | M2.4 升级 |
| 边注覆盖率 | Cap.1 边注基本完整 | M2.5 补全 |
| Grammatica 内容 | 仅含基础语法点 | M2.5 扩展 |
| 移动端 tooltip | tap 触发后需点击收起 | 已在 theme.js 处理 |

---

## 八、版本

- Tech Arch v3.0（正式版）· 2026-06-11
- 对应 PRD v3.0
