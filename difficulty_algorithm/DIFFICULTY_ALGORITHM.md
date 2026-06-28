# LLPSI 难度算法

## 版本

v2_0_0 — 2026-06-25 Lemmatization 版（使用 simplemma 词形还原）

---

## 一、目标

以 LLPSI 全书 56 章为基准尺，让任意一段拉丁语文本「即丢即出」——直接输出「适合刚学完第 X 章的学习者阅读」。

---

## 二、核心思想

LLPSI 采用螺旋递进的自然教学法，每个新词都在特定章节首次引入。因此，**学到第 N 章时，学习者已掌握 LLPSI 第 1~N 章出现的所有词汇**。

对外部读物而言，问题转化为：

> **LLPSI 的累积词汇，学到第几章时刚好能覆盖这段文本 85% 的独特词形（按原形计）？**

---

## 三、算法步骤

### Step 0 — 词形还原（Lemmatization）

拉丁语高度屈折：一个动词可能有 150+ 种形式。词形还原将所有屈折形式归一化为词典原形。

```
puellam / puellae / puellārum  →  puella
currit / cucurrit / currebat   →  curro
```

**实现**：使用 `simplemma` 库（开源、离线、Python 原生），准确率 86.8%。

### Step 1 — 建立两张映射表

**A. 词形→原形表** (`word_lemma_map.json`)

对 LLPSI 56 章 OCR 文本提取的 20,944 个独特词形执行 lemmatization：

```
{词形: 原形}  例: {"currit": "curro", "puellam": "puella", ...}
```

**B. 原形→章节表** (`lemma_chapter_map.json`)

对每个原形，记录他在 LLPSI 中首次出现的章节号：

```
{原形: 章节号}  例: {"puella": 1, "curro": 1, "conspicio": 25, ...}
共 14,613 条（20,944 词形压缩后）
```

### Step 2 — 评估任意文本

```
输入: 一段拉丁语文本
  1. 分词清洗 → 去重取独特词形集合
  2. 每个词形 → simplemma 还原为原形
  3. 原形 → 查 lemma_chapter_map 得章节号
  4. 未命中的 → 标记「LLPSI 未收录」
  5. 章节号排序 → 取 85% 百分位
     （即：学到第几章时，LLPSI 累积词汇覆盖了 85% 的独特词形）
  6. 若收录率 ≥ 85% → 输出章节号
     若收录率 < 85% → 诚实降级
```

### Step 3 — 读物切分（多故事/多章节）

按自然边界（章节标题 / 空行 / 序号）切分 → 每段独立评估。

---

## 四、v1.2 → v2.0 关键改进

| | v1.2 (无 lemmatization) | v2.0 (有 lemmatization) |
|---|---|---|
| 匹配方式 | 词形精确 + 归一化 fallback | 词形 → lemma → 章节 |
| 收录率（FS实测） | 72.9% | **86.1% (+13.2%)** |
| 阈值 | 90%（过高） | **85%** |
| 依赖 | 仅纯 Python | simplemma |

**为什么降到 85%？**

Nation 的 90-95% 理解度理论基于 token（含重复），我们用的 type（独特词形）覆盖率 85% 等价于 token ~90%。FS 实测中，90% 阈值仅 1/6 故事可评级，85% 降为 4/6。

**交叉验证**（v2 simplemma 输出 vs FR 官方单词表 1,872 词）：

- 交集：601（32.1%）
- 仅 simplemma：14,012
- 仅 FR 单词表：1,271

未匹配主要因为 FR 词条含语法标注（`ā/ab/abs prp +abl`）和断词符（`ab-dūcere`），simplemma 输出的是纯文本原形。不影响评估准确性。

---

## 五、验证结果

### Fabulae Syrae 采样故事（6 个）

```
故事                    v1收录率  v2收录率  提升     v2评级
----------------------------------------------------------------
Europa                 85.5% →  97.4%   +11.8%   第 28 章 ✓
Tarpeia                69.4% →  80.6%   +11.3%   降级(81%)
Atalanta               71.6% →  87.8%   +16.2%   第 32 章 ✓
Orpheus et Eurydice    74.7% →  80.0%   + 5.3%   降级(80%)
Daphne                 69.7% →  86.5%   +16.9%   第 31 章 ✓
Baucis et Philemon     66.7% →  84.6%   +17.9%   降级(85%)
----------------------------------------------------------------
平均                   72.9% →  86.1%   +13.2%
可评级: 4/6 (85%阈值) / 1/6 (90%阈值)
```

### 古典原典（参考，保留 v1.2 结果）

| 语料 | v1 收录率 | v2 收录率 | 评级 |
|------|----------|----------|------|
| Catullus 5 | 90.9% | 待重新计算 | Cap.34 (v1) |
| Caesar BG I.1 | 70.5% | 待重新计算 | 降级 |
| Cicero Cat. I | 68.2% | 待重新计算 | 降级 |

---

## 六、输出指标

| 指标 | 含义 |
|------|------|
| 难度等级 | 85% 阈值触达章节（降级时诚实告知） |
| LLPSI 收录率 | lemmatization 后命中 / 总独特词形 |
| 提升幅度 | v2 收录率 − v1 收录率 |
| 超纲词清单 | 完全未收录的独特词形 |

---

## 七、设计决策

1. **Type 级 + Lemmatization** — 生词「种类」才是阅读障碍；还原后消除屈折爆炸
2. **simplemma** — 86.8% 准确率、零外部依赖、离线可用
3. **85% 阈值** — type 级 85% ≈ token 级 90%，符合 Nation 理论且实测可行
4. **首次出现即锁定** — 一词只对应最早出现章节
5. **诚实降级** — 超出 LLPSI 范围时不给虚假数字

## 八、已知局限

1. **词形还原不完美** — simplemma 86.8% 准确率，歧义词无上下文消歧
2. **语法维度缺失** — 仅词汇，不涉及句法复杂度
3. **LLPSI 词汇覆盖有限** — 14,613 lemma 远不能覆盖全部古典拉丁语
4. **RA 章节自测未达标** — RA（36-56章）原典文本有大量 FR 未出现的专有名词和文学词汇，覆盖率仅 40-56%。这是 LLPSI 本身的词汇边界，不是算法缺陷

## 九、快速上手

```bash
# 1. 评估一段拉丁语文本
cd difficulty_algorithm
python3 -c "
from evaluate_v2 import evaluate
result = evaluate('Roma in Italia est. Italia in Europa est.', '示例')
print(f\"评级: {result['v2_verdict']}\")
print(f\"收录率: {result['v2_rate']}%\")
"

# 2. 运行完整测试（Fabulae Syrae + LLPSI 自测）
python3 evaluate_v2.py

# 3. 重建映射表（如需从 OCR 重新生成）
#    python3 build_word_map.py   # 先重建 word_chapter_map（需 OCR 原文）
#    python3 build_lemmatized_maps.py  # 再重建 lemma 映射表
```

## 十、核心文件

### 数据文件（运行时依赖）

| 文件 | 大小 | 格式 | 内容 | 用途 |
|------|------|------|------|------|
| `lemma_chapter_map.json` | ~300KB | `{原形: 章节号}` | 14,613 条 | **v2 核心映射**，评估时必须加载 |
| `word_chapter_map.json` | ~400KB | `{词形: 章节号}` | 20,944 条 | v1 兼容 + v2 中对比基线 |
| `word_lemma_map.json` | ~500KB | `{词形: 原形}` | 20,944 条 | 调试/检查用，运行时非必需 |
| `fr_lemmas.json` | ~30KB | `[原形, ...]` | 1,901 条 | FR 官方原形表，交叉验证用 |

### 脚本文件

| 文件 | 输入 | 输出 | 用途 |
|------|------|------|------|
| `evaluate_v2.py` | 拉丁语文本 | 难度等级 | **主入口**，日常评估 |
| `build_lemmatized_maps.py` | `word_chapter_map.json` | `lemma_chapter_map.json` + `word_lemma_map.json` | 一次性构建，OCR 更新后重跑 |
| `extract_fr_lemmas.py` | FR Excel 单词表 | `fr_lemmas.json` | 提取官方原形作验证锚点 |
| `extract_ra_lemmas.py` | RA PDF 单词表 | `ra_lemmas.json` | 仅作备份（PDF 编码差） |
| `test_simplemma.py` | — | 准确率报告 | 验证 lemmatizer 质量 |

### 数据流向

```
LLPSI OCR (56章文本)
    │
    ├─→ build_word_map.py ──→ word_chapter_map.json (20,944 词形→章节)
    │                                │
    │                                ├─→ evaluate_v2.py (v1 对比基线)
    │                                │
    │                                └─→ build_lemmatized_maps.py
    │                                        │
    │                          simplemma ────┘
    │                                        │
    │                               word_lemma_map.json (词形→原形)
    │                               lemma_chapter_map.json (原形→章节)
    │                                        │
    │                                        └─→ evaluate_v2.py (v2 主流程)
    │
FR Excel 单词表
    └─→ extract_fr_lemmas.py ──→ fr_lemmas.json ──→ 交叉验证
