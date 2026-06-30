# LLPSI_plus 项目经验教训库

> 本文件由 AI 在每次任务完成后追加更新，沉淀错误、踩坑、成功经验。
> 更新时间: 2026-06-30

---

## L01. evaluate_v2.py 误把 YAML 元数据算成 OOV 词

**发生时间**: 2026-06-30
**场景**: 验证 Cap.1/2 的 9+10=19 篇重写故事，全部 FAIL (v2_rate 仅 50-67%)
**根因**:
- 故事文件以 YAML frontmatter (`---` 包围) 开头，后接拉丁正文
- `evaluate_v2.py` 直接 `text = content` 把整个文件内容喂入分词
- "story_id", "target_chapter", "罗马人" 等元数据被当成 OOV，拉低 v2_rate

**修复**:
- 在调用方手动 `extract_latin_text()` 剥 YAML 前置块
- 已在 `evaluate_v2.py` 新增 `--file PATH` 参数，自动识别 `.md` 后跳过 YAML 块
- 版本升级到 v2_4_0

**预防**:
- 所有 .md 故事文件评估必须用 `evaluate_v2.py --file <path>` 或带 `extract_latin_text()` 预处理
- 不要直接对全文做 evaluate

---

## L02. Cap.4 文件命名后缀不一致导致清理混乱

**发生时间**: 2026-06-30
**场景**: 清理 Cap.4 时发现有 4 个 medius 文件名后缀未补零（如 `01` 而非 `001`），需要保留
**根因**:
- 旧版脚本用 `{n}` 格式（1-9 不补零）
- 新版要求补零 `{n:03d}`
- 导致同一目录有混合格式（01/02/.../09/10/11/12/13/14）

**修复**:
- 全部统一为 `{n:03d}` 格式
- 在 `rewrite_capN.py` 中统一使用 `find_next_number` 保留 3 位补零

**预防**:
- 所有生成文件名的脚本必须用 `{n:03d}` 格式
- 写新的 rewrite 脚本前先看现有命名格式

---

## L03. 计划书版本爆炸——阶段性文档无人清理

**发生时间**: 2026-06-30
**场景**: `.trae/documents/` 累积 9 份计划书，其中 7 份是已完成的任务型文档
**根因**:
- 每个会话都会新建 `cleanup_*.md` / `continue_*.md` / `*_plan.md`
- 完成后没人归档，全部堆在 documents 根目录

**手动清理**:
- 之前已归档 7 份过时计划书（commit `2f438ca`）
- 通过 `git log --diff-filter=D -- .trae/documents/` 可找回历史

**用户决定（2026-06-30）**:
- **不创建自动归档脚本**——会打断工作心流
- 清理/移动等操作必须人工确认
- 已删除 `.trae/scripts/archive_plan.sh`
- `.trae/documents/archive/` 目录保留为空，仅作占位

**预防**:
- 任务型文档（一次性任务清单）由用户在方便时手动归档或删除
- AI 不得自动执行任何清理/移动/删除操作
- 核心规划书（长期参考）保留在根目录，命名 `*_plan.md` 即可
- 历史经验报告（如 `cap1_6_special_report.md`）保留，不要归档


---

## L04. Cap.1-5 短篇重写必须用"严格词汇"模式

**发生时间**: 2026-06-30（Cap.1-5 重写实战）
**场景**: 53 篇 Cap.1-5 短篇重写为中篇/中长篇
**经验**:
- Cap.1-5 词汇极少（每章 100-180 词元），自由发挥模式下命中率极低（cap1_6_special_report: 4%）
- 必须用"严格筛选 + 排比扩充"模式：
  1. 从 `cap{N}_vocab_clean.json` 拉取允许词
  2. 严筛超章节动词（ambulō→Cap.6, redeō→Cap.15, exspectō→Cap.7）
  3. 严筛超章节专名（Quīntus→Cap.13, Graecus→Cap.46）
  4. 用排比句（"Rōma est magna. Italia est magna. ..."）和重复结构填充篇幅
  5. 通过 `evaluate_v2.py` 验证 85% 分位 ≤ 目标+2
- 当前 53 篇全部通过（Cap.1 v2_level=1, Cap.5 v2_level=5-7）

**应用**:
- 阶段 2 (Cap.6-10) 仍用此模式
- 阶段 3+ (Cap.11+) 词汇 > 500 时可切换回"自由发挥"模式

---

## L05. 长音剥离 (macron stripping) 是 simplemma 的前置必要步骤

**发生时间**: 历史
**场景**: evaluate_v2.py v2 算法
**根因**:
- `simplemma.lemmatize("amō", lang="la")` 不识别长音字符，会把 amō 还原为不存在的原形
- 必须先 `re.sub(r"[āēīōūȳ]", lambda m: "aeiouy"[...], w).lower()` 剥长音

**当前状态**: 已在 evaluate_v2.py v2_3_0 实现
**预防**: 任何新写的拉丁语处理工具，必须在 simplemma 之前先剥长音

---

## L06. 篇幅扩充的有效手段（Cap.1-5 实战）

**发生时间**: 2026-06-30
**场景**: 用 200 词元扩充到 300-800 词的中篇/中长篇
**有效手段**（按效果排序）:
1. **重复核心句**: "Rōma est magna. Italia est magna. Hispānia est magna." —— 简单有效，每篇基础工具
2. **排比结构**: "Trēs terrae: ... Trēs īnsulae: ... Trēs flūmina: ..." —— 自然扩展
3. **问答对话体**: "Ubi est Rōma? Rōma est in Italiā. Estne Rōma in Graeciā? ..." —— 适合地理介绍
4. **反转/对比**: "Tiberis est parvus — sed Rōmānus. Rhēnus est magnus — sed nōn Rōmānus." —— 加深度
5. **感官细节**: 颜色（rubra, alba）、位置（prope, longē）、大小（magna, parva）—— 适合抒情/描写

**失败手段**:
- 强行堆砌生词（命中率 < 5%）
- 编造复杂情节（容易用到超章节词）

---

## L07. 工具/规则版本号必须同步

**发生时间**: 2026-06-30
**场景**: evaluate_v2.py v2_3_0 → v2_4_0 升级
**根因**: 修改工具但忘记更新 manifest.json / STRATEGY.md / README.md 的版本号
**预防**:
- 每次工具升级后必须同步更新：
  - `evaluate_v2.py` docstring 顶部版本号
  - `STRATEGY.md` 末尾版本号
  - `AGENTS.md` / `README.md` 工具版本表
  - `progress.json` 时间戳

---

## L08. 上下文压缩时必须保留可恢复引用

**发生时间**: 2026-06-30（本会话）
**场景**: SOLO 主 Agent 上下文压缩后，新会话必须靠 summary + 文件快速恢复
**经验**:
- 把核心规划书放 `.trae/documents/` 而非项目根
- 关键脚本放 `AI_reader/` 根目录，命名规范 `rewrite_cap{N}.py`
- 每个脚本的 STORIES 字典就是可恢复的"知识备份"
- tierlist 放 `AI_reader/realitates_tierlist.jsonl` 一份就够，不要放多份

---

## 待补充类别

- [ ] 阶段 2 (Cap.6-10) 重写经验
- [ ] AI 自动生成的"严格词汇"模式实际效果
- [ ] OCR 数据处理经验
- [ ] 文档归档脚本长期效果观察
