# LLPSI 数据洞察可视化页面 - 技术架构

> **文档版本**: v1.0
> **创建日期**: 2026-06-05

---

## 一、技术选型

| 类别 | 选型 | 理由 |
|------|------|------|
| 框架 | **纯 HTML + CSS + JS** | 单文件交付，无构建依赖 |
| 图表库 | **ECharts 5.4** (CDN) | 古典主题适配好、性能优、中文文档全 |
| 字体 | **Google Fonts** | Cinzel + Cormorant Garamond + Noto Serif SC |
| 样式 | **原生 CSS (Variables)** | 罗马配色集中管理 |
| 数据 | **内嵌 JSON** | 直接写死在 `<script>` 块 |

> **为什么不选 React/Vue？** 单页静态展示，过度框架化违反 KISS 原则。

---

## 二、目录结构

```
LLPSI+++/
└── viz_output/
    └── familia_romana_insights.html   ← 唯一交付物
```

---

## 三、文件结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Familia Romana · Data Insights</title>
  
  <!-- Google Fonts: Cinzel + Cormorant Garamond + Noto Serif SC -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="...fonts...">
  
  <!-- ECharts CDN -->
  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  
  <style>
    /* CSS Variables (罗马配色) */
    :root {
      --color-parchment: #f4ecd8;
      --color-ink: #1c1917;
      --color-pompeii-red: #a8392e;
      --color-imperial-gold: #b08d2b;
      --color-roman-green: #2c3e3a;
      --color-tyrian-purple: #5a3e5c;
      --color-marble: #e8dfc4;
      --color-deep-clay: #7a2820;
    }
    
    /* 全局样式 */
    /* Hero 样式 */
    /* Chart 容器样式 */
    /* Table 样式 */
    /* 装饰元素 */
  </style>
</head>
<body>
  <main>
    <!-- I. Hero -->
    <section class="hero">...</section>
    
    <!-- II. Growth Chart -->
    <section class="chart-section">...</section>
    
    <!-- III. Steep Chapter Chart -->
    <section class="chart-section">...</section>
    
    <!-- IV. Chapter Table -->
    <section class="table-section">...</section>
    
    <!-- V. Caput IX Wall Insight -->
    <section class="insight">...</section>
    
    <!-- VI. Recommendations -->
    <section class="recommendations">...</section>
    
    <!-- VII. Colophon -->
    <footer>...</footer>
  </main>
  
  <script>
    // 35 章节数据 (内嵌)
    const data = [...];
    
    // ECharts 配置
    const growthChart = echarts.init(...);
    growthChart.setOption({...});
    
    const densityChart = echarts.init(...);
    densityChart.setOption({...});
  </script>
</body>
</html>
```

---

## 四、关键数据

### 4.1 章节统计 (内嵌)

```js
const chapterData = [
  { chapter: 1,  total: 848,  new: 214, density: 25.2, cumulative: 214,  highFreq: 77 },
  { chapter: 2,  total: 847,  new: 184, density: 21.7, cumulative: 398,  highFreq: 60 },
  // ... 35 章全部
  { chapter: 35, total: 1508, new: 338, density: 22.4, cumulative: 11019, highFreq: 19 }
];
```

### 4.2 阈值

- 平均新词密度: 23.1%
- 陡坡阈值: 27.7% (= 23.1% × 1.2)
- 陡坡章节: Cap. 25 (30.3%)
- "第九章墙" 区域: Cap. 8-13

---

## 五、图表方案

### 5.1 累计词汇增长曲线

- **类型**: 折线图 + 渐变面积
- **X 轴**: 章节 (1-35)
- **Y 轴**: 累计词汇 (0-11019)
- **样式**: 罗马红主线 + 金色渐变填充

### 5.2 新词密度柱状图

- **类型**: 柱状图
- **X 轴**: 章节 (1-35)
- **Y 轴**: 新词密度 (0-35%)
- **标记线**: 27.7% 阈值（暗赭色虚线）
- **陡坡柱**: 深红色高亮
- **正常柱**: 罗马绿 / 灰石灰

### 5.3 数据表格

- 35 行 × 6 列
- 罗马数字章节号
- 评级 emoji 或徽章
- 斑马纹 (米色 + 浅米色)

---

## 六、关键样式

### 6.1 Hero 排版

```css
.hero-title {
  font-family: 'Cinzel', serif;
  font-size: 5rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--color-ink);
  text-transform: uppercase;
}

.hero-subtitle {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 1.5rem;
  color: var(--color-pompeii-red);
}
```

### 6.2 装饰分隔符

```html
<div class="ornament">
  <span>▪</span>
  <span>——</span>
  <span>◆</span>
  <span>——</span>
  <span>▪</span>
</div>
```

### 6.3 卡片样式 (浅色大理石)

```css
.insight-card {
  background: var(--color-marble);
  border-left: 4px solid var(--color-pompeii-red);
  padding: 1.5rem 2rem;
  font-family: 'Cormorant Garamond', serif;
}
```

---

## 七、性能 & 兼容性

| 项目 | 目标 |
|------|------|
| 资源加载 | 字体预连接 (`<link rel="preconnect">`) |
| 渲染 | 同步渲染（数据已就绪） |
| 浏览器 | Chrome 90+, Safari 14+, Edge 90+ |
| 视口 | 1440px 桌面优先，1024px+ 兼容 |

---

## 八、交付前自检

- [ ] HTML 单文件可双击打开
- [ ] 35 章节数据全部呈现
- [ ] 两个图表正常渲染
- [ ] 罗马配色一致性
- [ ] 字体加载无回退异常
- [ ] 移动端基本可读（不要求完美）
