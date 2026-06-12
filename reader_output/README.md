# reader_output/ — M3 拓展读物矩阵 (M3 Reader Pivot)

> **分支**: `feat/reader-pivot` (从 `dev0611` v3.7+1 拉出)
> **作者**: Max · 2026-06-12
> **状态**: 🚧 规划中, 尚未生成内容

---

## 🎯 项目转向: 不再电子化 LLPSI 本体

### 为什么转向 (2026-06-12 用户决策)

**核心痛点**: LLPSI 母版 (Ørberg) 排版哲学是"边栏大量插图 + 拉丁语注释", 而插图的准确提取与对齐是当前技术栈无法可靠解决的问题。

**原方向 (M2)**:
```
LLPSI PDF → OCR → 清洗 → 标实体 + 注边注 + 排版 → 网页
                  ↑
                  难点: 边栏插图 OCR 后丢失位置信息
```

**新方向 (M3)**:
```
拓展读物 PDF (Colloquia/Fabulae Syrae/...) → OCR 章节正文 → 抽离对应章节 → 网页
                                          ↑
                                          优势: 拓展读物以正文为主, 几乎无插图
```

### 设计原则转变

| 维度 | M2 (旧) | M3 (新) |
|------|---------|---------|
| **核心内容** | LLPSI 本体 (Cap.I, II, III) | 拓展读物章节 (Colloquia Cap.I, Fabulae Syrae Cap.I, ...) |
| **页面主体** | 单章 HTML (cap_I.html) | 单读物单章 HTML (readers/colloquia/cap_1.html) |
| **导航** | 顶部 + 底部翻页控件 | 顶部 chapter select + 拓展卡片矩阵 |
| **拓展卡片位置** | 页面底部 (在语法板块之后) | **页码选择与正文之间** (用户决策) |
| **卡片点击行为** | 弹窗/折叠 (待实现) | **跳转到对应读物的章节页** (用户决策) |
| **卡片内容来源** | 当前章节的"拓展阅读"建议 | 当前章节的"对应读物章节"矩阵 |

---

## 📁 目录结构

```
reader_output/
├── README.md              ← 本文件 (项目总览)
├── docs/                  ← 设计规范与 README 之外的文档
│   ├── DESIGN_M3.md       ← M3 设计规范 (待写)
│   └── ROUTING_MATRIX.md  ← LLPSI Cap.X ↔ 拓展读物 Cap.X 对照表 (待写)
├── readers/               ← 每本拓展读物一个子目录
│   ├── colloquia/         ← Colloquia Personarum (首选起步读物)
│   │   ├── README.md      ← 该读物的来源、页码、抽取计划
│   │   ├── cap_1.html     ← 抽离 Cap.1 章节的网页
│   │   ├── cap_2.html
│   │   └── ...
│   ├── syrae/             ← Fabulae Syrae
│   │   ├── README.md
│   │   ├── cap_1.html
│   │   └── ...
│   ├── fabellae/          ← Fabellae Latinae
│   ├── nutting/           ← Nutting Reader
│   ├── via_latina/        ← Via Latina
│   └── ...                ← 后续视用户决策新增
├── index.html             ← 主页: 顶部 chapter select + 拓展卡片矩阵 + 引导
└── shared/                ← 跨读物共享的资源 (CSS, JS, entity dict)
    ├── style.css          ← 从 m2_output/product/style.css 继承 + 适配
    ├── theme.js           ← 主题切换
    └── ent_dict.json      ← 实体词典 (从 m2_output/data/ 继承)
```

---

## 🚀 起步计划 (Phase 1)

### 步骤 1: 选第一本读物
- [ ] **Colloquia Personarum** (最贴合 LLPSI Cap.1 主题: 罗马家庭日常)
- [ ] Fabulae Syrae (神话, 适合 Cap.1 之后)
- [ ] Nutting Reader (简明, 适合入门)
- [ ] (候选) Via Latina (体系完备)

### 步骤 2: 建立路由矩阵
LLPSI Cap.I (罗马帝国) ↔ Colloquia Cap.1 (罗马家庭日常) — 主题紧贴
LLPSI Cap.I ↔ Fabulae Syrae Cap.1 (神话背景) — 主题较远

### 步骤 3: 抽取 Colloquia Cap.1 内容
- 来源: `source/colloquia_personarum/...pdf` (待用户提供)
- 抽离范围: 与 LLPSI Cap.I 主题重叠的部分
- 工具: `pdftotext -layout` + 手工校对

### 步骤 4: 套用 M2 设计规范
- 沿用 `m2_output/product/style.css` v3.7+1 (设计已稳定)
- 移除 M2 特有的 "Grammatica" 板块 (M3 强调纯阅读)
- 拓展卡片矩阵放在 chapter select 与正文之间 (用户决策)

### 步骤 5: 实现卡片跳转
- 卡片是 `<a>` 标签, `href="readers/colloquia/cap_1.html"`
- 静态 URL 跳转, 无 SPA (用户决策)
- 每本读物的章节页有面包屑: `Home > Colloquia > Cap.1`

---

## 🔄 与 M2 的关系

### 保留 (设计参考)
- `m2_output/product/style.css` v3.7+1 — 设计规范成熟
- `m2_output/data/ent_dict.json` — 实体词典可复用
- `m2_output/build.py` — HTML 生成脚本可适配

### 弃用 (方向已转)
- `m2_output/product/cap_I.html` 等 3 章 LLPSI HTML — 仅作设计参考, **不维护**
- `m2_output/scripts/fix_text_raw.py` (OCR 清洗) — 仍可用于 Colloquia 抽取
- 拓展卡片的 "弹窗" 交互 (旧设计) — 改为 URL 跳转

### 归档策略 (用户决策: 保留原位不归档)
- M2 文件留在原位, 不删除
- 本 README 在新目录 `reader_output/` 自成一派
- Git 历史保留: `dev0611` 永远可回退

---

## 📋 候选读物优先级

| 优先级 | 读物 | 来源 (待用户提供) | 主题契合度 | 难度 |
|--------|------|--------------------|------------|------|
| 🥇 P0 | **Colloquia Personarum** | TBD | 极高 (罗马家庭) | 入门 |
| 🥈 P1 | **Fabulae Syrae** | TBD | 中 (神话) | 入门 |
| 🥉 P2 | Nutting Reader | TBD | 高 (历史) | 入门 |
| P3 | Via Latina | TBD | 高 | 入门 |
| P4 | Fabellae Latinae | TBD | 中 (寓言) | 入门 |

> 等待用户确认首选读物 + 提供 PDF 来源。

---

## 🎨 设计规范 (沿用 M2 v3.7+1, 调整点如下)

### 沿用不变
- 排版: 单列 660px 居中, Georgia 衬线
- 主题: 日间/夜间 CSS 变量驱动
- 实体: `.ent .q` 不可见, `.tip` 弹层, 4 类 (loc/feat/gen/num)
- 边注: `.margin::before { content: "†" }` 触发
- 翻页: chapter select 下拉

### 新增/调整
- **拓展卡片矩阵**: 位于 chapter select 与正文之间 (用户决策)
- **卡片样式**: 与 m2_output 一致 (.ll-ext-block), 但点击后跳转 URL
- **面包屑**: `Home > 读物名 > Cap.X` (新增)
- **去除 Grammatica 板块**: M3 强调纯阅读, 语法由读物自带注释覆盖
- **去除 colophon 后重复翻页**: 沿用 M2 v3.7 唯一化方案

---

## ⚠️ 待确认事项 (请用户决策)

1. **首选读物**: Colloquia Personarum 还是其他?
2. **PDF 来源**: 用户是否已准备好 Colloquia 的 PDF (放在 `source/colloquia_personarum/`)?
3. **抽取范围**: Colloquia 全本还是只取与 LLPSI Cap.I 主题重叠的章节?
4. **实体词典复用**: 直接用 M2 的 ent_dict.json, 还是从 Colloquia 重新生成?
5. **M2 cap_I.html 处置**: 保留作为"设计参考"还是改名 `_deprecated`?

---

## 📜 版本历史

| 版本 | 日期 | 关键变更 |
|------|------|---------|
| **v0.1** | 2026-06-12 | 项目转向, 选定方向, 创建 reader_output/ 目录结构, 待用户确认首选读物 |

---

## 🛠️ 快速命令

```bash
# 切换到本分支
git checkout feat/reader-pivot

# 启动本地预览
cd reader_output && python3 -m http.server 8765

# (待实现) 生成 Colloquia Cap.1 HTML
python3 reader_output/build.py --reader colloquia --cap 1
```

---

> **M2 → M3 转向逻辑**: 让真正可解决的内容 (拓展读物纯文字) 先成熟, 让真正难解决的 (LLPSI 母版插图) 等技术栈升级后再回头。
