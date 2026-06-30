# LLPSI 难度算法

## 版本

v3_0_0 — 2026-06-30 预计算查表 + simplemma 兜底版

---

## 一、目标

以 LLPSI 全书 56 章为基准尺，让任意一段拉丁语文本「即丢即出」——直接输出「适合刚学完第 X 章的学习者阅读」。

---

## 二、核心思想

LLPSI 采用螺旋递进的自然教学法，每个新词都在特定章节首次引入。因此，**学到第 N 章时，学习者已掌握 LLPSI 第 1~N 章出现的所有词汇**。

对外部读物而言，问题转化为：

> **LLPSI 的累积词汇，学到第几章时刚好能覆盖这段文本 85% 的独特词形（按原形计），且 80% 累积百分位对应的章节？**

---

## 三、算法步骤

### Step 0 — 词形还原（Lemmatization）

拉丁语高度屈折：一个动词可能有 150+ 种形式。词形还原将所有屈折形式归一化为词典原形。

```
puellam / puellae / puellārum  →  puella
currit / cucurrit / currebat   →  curro
```

**实现（v3）**：预计算 33K 词形→章节映射表（`form_chapter_map.json`）作为主查表，`simplemma` 仅作兜底。90%+ 的词形直接命中预计算表，无需运行时还原。

### Step 1 — 建立映射表

**主表：词形→章节表** (`form_chapter_map.json`)

合并两条来源：
- `word_lemma_map.json`（20,944 条词形→原形，simplemma 离线计算）× `lemma_chapter_map.json`（14,613 条原形→章节）
- `word_chapter_map.json`（16,665 条词形→章节，OCR 直接观测）

```
{词形: 章节号}  例: {"currit": 1, "puellam": 1, ...}
共 33,047 条
```

**兜底表：原形→章节表** (`lemma_chapter_map.json`)

```
{原形: 章节号}  例: {"puella": 1, "curro": 1, "conspicio": 25, ...}
共 14,613 条
```

### Step 2 — 评估任意文本

```
输入: 一段拉丁语文本
  1. 分词清洗 → 去重取独特词形集合
  2. 剥长音+小写 → 查 form_chapter_map.json（33K 条目，O(1)）
  3. 未命中 → simplemma 还原 → 查 lemma_chapter_map.json
  4. 仍未命中 → 标记「LLPSI 未收录」
  5. 章节号排序 → 取 80% 百分位
  6. 若收录率 ≥ 85% → 输出章节号（80th 百分位章节）
     若收录率 < 85% → 诚实降级
```

### Step 3 — 读物切分

按自然边界（章节标题 / 空行 / 序号）切分 → 每段独立评估。

---

## 四、v2.0 → v3.0 关键改进

| | v2.0 (simplemma 全量) | v3.0 (预计算 + 兜底) |
|---|---|---|
| 匹配方式 | 每次调 simplemma 还原 | 优先查预计算表，仅 OOV 调 simplemma |
| 收录率（FS实测） | 86.1% | **87.7% (+1.6%)** |
| 运行时 simplemma 调用 | 每次评估 ~70 次 | 仅 10-20% 词形，~10 次 |
| 百分位 | 85% | 80%（更宽松） |
| 收录率阈值 | 85% | 85%（不变） |
| 依赖 | simplemma | simplemma（仅兜底，未来可替换） |

**核心改进**：预计算 33K 词形→章节映射表，运行时 90%+ 词形直接命中。收录率提升 1.6%，因为预计算表合并了 OCR 直接观测的词形，弥补了 simplemma 的部分误还原。

---

## 五、验证结果

### Fabulae Syrae 采样故事（6 个）

```
故事                    v1收录率  v3收录率  提升     v3评级
----------------------------------------------------------------
Europa                 86.8% →  96.1%   + 9.2%   第 27 章 ✓
Tarpeia                77.4% →  83.9%   + 6.5%   降级(84%)
Atalanta               78.4% →  87.8%   + 9.5%   第 32 章 ✓
Orpheus et Eurydice    77.3% →  84.0%   + 6.7%   降级(84%)
Daphne                 78.7% →  89.9%   +11.2%   第 35 章 ✓
Baucis et Philemon     73.1% →  84.6%   +11.5%   降级(85%)
----------------------------------------------------------------
平均                   78.6% →  87.7%   + 9.1%
可评级: 3/6 (85%收录率阈值)
```

### 古典原典（参考）

| 语料 | v1 收录率 | v3 收录率 | 评级 |
|------|----------|----------|------|
| Catullus 5 | 90.9% | 待重新计算 | Cap.34 (v1) |
| Caesar BG I.1 | 70.5% | 待重新计算 | 降级 |
| Cicero Cat. I | 68.2% | 待重新计算 | 降级 |

---

## 六、输出指标

| 指标 | 含义 |
|------|------|
| 难度等级 | 80% 百分位触达章节（降级时诚实告知） |
| LLPSI 收录率 | lemmatization 后命中 / 总独特词形 |
| 提升幅度 | v3 收录率 − v1 收录率 |
| 超纲词清单 | 完全未收录的独特词形 |

---

## 七、设计决策

1. **Type 级 + 预计算查表** — 生词「种类」才是阅读障碍；33K 预计算表覆盖 90%+ 场景
2. **simplemma 兜底** — 仅对预计算表未覆盖的 10-20% 词形调用，未来可替换为规则引擎
3. **80% 百分位 / 85% 覆盖率双阈值** — 收录率≥85% 方可评级；难度取 80th 百分位章节号。type 级 85% ≈ token 级 90%，符合 Nation 理论且实测可行
4. **首次出现即锁定** — 一词只对应最早出现章节
5. **诚实降级** — 超出 LLPSI 范围时不给虚假数字

## 八、已知局限

1. **词形还原不完美** — simplemma 86.8% 准确率（仅影响 ~10% 兜底词）
2. **语法维度缺失** — 仅词汇，不涉及句法复杂度
3. **LLPSI 词汇覆盖有限** — 14,613 lemma 远不能覆盖全部古典拉丁语
4. **RA 章节自测未达标** — RA（36-56章）原典文本有大量专有名词和文学词汇

## 九、快速上手

```bash
cd difficulty_algorithm

# 评估一段拉丁语文本
python3 -c "
from evaluate_v2 import evaluate
result = evaluate('Roma in Italia est. Italia in Europa est.', '示例')
print(f\"评级: {result['v2_verdict']}\")
print(f\"收录率: {result['v2_rate']}%\")
"

# 运行完整测试
python3 evaluate_v2.py

# 重建映射表（OCR 更新后）
# python3 build_word_map.py
# python3 build_lemmatized_maps.py
# python3 build_form_map.py
```

## 十、核心文件

### 数据文件（运行时依赖）

| 文件 | 大小 | 格式 | 内容 | 用途 |
|------|------|------|------|------|
| `form_chapter_map.json` | ~521KB | `{词形: 章节号}` | 33,047 条 | **v3 核心**，运行时主查表 |
| `lemma_chapter_map.json` | ~300KB | `{原形: 章节号}` | 14,613 条 | simplemma 兜底查表 |
| `word_chapter_map.json` | ~400KB | `{词形: 章节号}` | 16,665 条 | v1 兼容 |
| `word_chapter_map_normalized.json` | ~400KB | `{归一化词形: 章节号}` | 17,536 条 | v1 归一化匹配 |
| `word_lemma_map.json` | ~500KB | `{词形: 原形}` | 20,944 条 | 构建 form_chapter_map 的来源 |
| `fr_lemmas.json` | ~30KB | `[原形, ...]` | 1,901 条 | 交叉验证用 |

### 脚本文件

| 文件 | 用途 |
|------|------|
| `evaluate_v2.py` | **主入口**，日常评估 |
| `build_form_map.py` | 合成 form_chapter_map.json |
| `build_lemmatized_maps.py` | 构建 lemma_chapter_map + word_lemma_map |
| `extract_fr_lemmas.py` | 提取 FR 官方原形表 |
| `test_simplemma.py` | 验证 lemmatizer 质量 |

### 数据流向

```
LLPSI OCR (56章文本)
    │
    ├─→ build_word_map.py ──→ word_chapter_map.json
    │                                │
    │                                ├─→ evaluate_v2.py (v1 基线)
    │                                │
    │                                └─→ build_lemmatized_maps.py
    │                                        │
    │                          simplemma ────┘
    │                                        │
    │                               word_lemma_map.json
    │                               lemma_chapter_map.json
    │                                        │
    │                                        └─→ build_form_map.py
    │                                              │
    │                              word_chapter_map.json ──┘
    │                                              │
    │                                     form_chapter_map.json (33K)
    │                                              │
    │                                              └─→ evaluate_v2.py (v3 主流程)
    │                                                    │
    │                                     simplemma ────┘ (仅兜底)
    │
FR Excel 单词表
    └─→ extract_fr_lemmas.py ──→ fr_lemmas.json ──→ 交叉验证
```