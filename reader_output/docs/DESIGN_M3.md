# DESIGN_M3.md — M3 拓展读物矩阵 设计规范

> **状态**: 🚧 占位, 详细设计待 M2 v3.7+1 样式确认复用后填充。

---

## 1. 沿用 M2 v3.7+1 样式 (直接 copy)

- `m2_output/product/style.css` v3.7+1 → 复制为 `reader_output/shared/style.css`
- 实体标注规则 (§0 HTML5 解析铁律, §0.2 tooltip 顶格左对齐)
- 主题切换 (`theme.js`)
- 实体词典 (`ent_dict.json`)

## 2. M3 调整点 (与 M2 差异)

| 元素 | M2 | M3 |
|------|----|----|
| 顶部导航 | chapter select | chapter select (沿用) |
| 拓展卡片位置 | 页面底部 (语法之后) | **chapter select 与正文之间** (用户决策) |
| 卡片交互 | 弹窗/折叠 (未实装) | **URL 跳转** (用户决策) |
| 卡片内容 | 当前章节的"拓展阅读" | 当前章节的"对应读物章节"矩阵 |
| 面包屑 | 无 | **新增** (Home > 读物 > Cap.X) |
| 语法板块 (Grammatica) | 有 | **去除** (M3 强调纯阅读) |
| 底部翻页 (重复) | 唯一化 (v3.7) | 沿用 v3.7 唯一方案 |

## 3. 新增组件

### 3.1 拓展卡片矩阵 (`.reader-matrix`)
- 位置: `<header>` (chapter select) 之后, `<article>` 之前
- 布局: CSS Grid, `auto-fill, minmax(180px, 1fr)`
- 卡片内容:
  - 读物封面缩略图 (可选, 待 PDF 截取)
  - 读物名 + Cap.X 标题
  - 一句话简介 (拉丁文)
  - 点击 → 跳转 `readers/{book}/cap_{n}.html`

### 3.2 面包屑 (`.breadcrumb`)
- 位置: `<header>` 顶部
- 格式: `LLPSI+++ > [读物名] > Cap. X`
- 样式: small-caps, 7pt, --fg-soft 色

## 4. 暂未决

- [ ] 主页 `index.html` 是否需要 LLPSI Cap.I 入口? (用户决策)
- [ ] 拓展卡片的视觉权重 (与 M2 一致? 还是更突出?)

---

> 详细规范将在首个 Colloquia 章节实装时沉淀。
