#!/usr/bin/env python3
"""
LLPSI+++ Step 3: 补充阅读生成脚本 (ampliata_generate.py)
======================================================
功能:
  对"陡坡章节"生成拉丁语微阅读,使用双 Prompt 策略:
    - 语法墙版本: 句法脚手架 (用熟悉词汇反复展示新句法)
    - 密度墙版本: 词汇脚手架 (多次复现目标章新词)

输入:
  - OCR 全文 (ocr_output/familia_romana/clean.txt)
  - 目标章节 + 章节类型

输出:
  - supplements/supplement_NN.txt (每章一个微阅读)

设计原则 (来自词频分析):
  - 仅用 ≤ 目标章词汇 (避免引入新词)
  - 角色/世界观延续 Familia Romana (Mārcus, Iūlia, familia Iūlia)
  - 200-300 词 (3-4 段)
  - 句法模式 ≥ 5 次 / 关键词复现 ≥ 4 次
"""

import os
import re
import sys
from collections import Counter

# 复用 Step 2 的分析函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iterum_analysis import (
    split_into_chapters,
    extract_readings_from_chapter,
    tokenize,
)

# ============================================================
# 配置
# ============================================================
INPUT_FILE = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/familia_romana/clean.txt"
OUTPUT_DIR = "/Users/max/Downloads/Projects/LLPSI+++/supplements"

# MVP 优先章节表 (来自 Project_Plan.md v1.3.0)
# 格式: 章节号 -> (类型, 描述)
PRIORITY_CHAPTERS = {
    8:  ("syntax",  "Cap. VIII  · 间接引语 (oratiō oblīqua) 首次系统出现"),
    9:  ("syntax",  "Cap. IX    · 从句大量引入"),
    10: ("syntax",  "Cap. X     · 关系从句扩展"),
    11: ("syntax",  "Cap. XI    · 句法继续复杂化"),
    12: ("syntax",  "Cap. XII   · 夺格句型进入"),
    13: ("syntax",  "Cap. XIII  · 逼近密度阈值"),
    25: ("density", "Cap. XXV   · 密度墙 (30.3%) - 神话专名集中"),
}


# ============================================================
# 词汇提取
# ============================================================
def get_chapters_text(ocr_path: str) -> dict[int, str]:
    """读取 OCR 文本并切分为章节阅读正文"""
    with open(ocr_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # 清理
    full_text = re.sub(r'={3,}.*?={3,}', '', full_text)
    full_text = re.sub(r'--- 第 \d+ 页 ---', '', full_text)
    full_text = re.sub(r'--- PAGE \d+ ---', '', full_text)
    full_text = re.sub(r'--- \d+ ---', '', full_text)

    chapters = split_into_chapters(full_text)
    chapter_readings = {}
    for num in sorted(chapters.keys()):
        reading = extract_readings_from_chapter(chapters[num])
        # 移除章节标题行
        reading = re.sub(r'CAPITVLVM\s+\w+.*', '', reading)
        reading = re.sub(r'CAP\.\s+[IVX]+.*', '', reading)
        chapter_readings[num] = reading
    return chapter_readings


def get_vocab_up_to(chapter_readings: dict[int, str], target: int) -> set[str]:
    """获取 ≤ target 章已出现的所有词形 (小写)"""
    vocab = set()
    for ch in range(1, target + 1):
        if ch in chapter_readings:
            vocab.update(w.lower() for w in tokenize(chapter_readings[ch]))
    return vocab


def get_new_words_in(chapter_readings: dict[int, str], target: int) -> set[str]:
    """获取 target 章新引入的词形"""
    if target not in chapter_readings:
        return set()

    prev_vocab = get_vocab_up_to(chapter_readings, target - 1)
    chapter_vocab = set(w.lower() for w in tokenize(chapter_readings[target]))
    return chapter_vocab - prev_vocab


def get_top_new_words(chapter_readings: dict[int, str], target: int, top_n: int = 15) -> list[tuple[str, int]]:
    """获取 target 章出现频次最高的 N 个新词"""
    if target not in chapter_readings:
        return []

    prev_vocab = get_vocab_up_to(chapter_readings, target - 1)
    words = [w.lower() for w in tokenize(chapter_readings[target])]
    counts = Counter(words)

    new_word_counts = [
        (w, c) for w, c in counts.items()
        if w not in prev_vocab and c >= 1
    ]
    new_word_counts.sort(key=lambda x: -x[1])
    return new_word_counts[:top_n]


# ============================================================
# Prompt 模板 (双版本)
# ============================================================
def to_roman(num: int) -> str:
    """1-35 转罗马数字"""
    map_ = [
        (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    result = ''
    for v, s in map_:
        while num >= v:
            result += s
            num -= v
    return result


def build_syntax_prompt(chapter: int, vocab: set[str], new_words: list[tuple[str, int]],
                        description: str) -> str:
    """
    [语法墙版本 Prompt]
    用于 Cap. 8-13: 用 Cap. 1-N 已知词汇反复展示目标章新句法结构
    """
    vocab_sample = sorted(list(vocab))[:80]  # 截取样本避免 prompt 过长
    new_words_str = ", ".join(f"{w}({c}次)" for w, c in new_words[:10])

    return f"""你是一位精通 LLPSI 教学法的拉丁语作家,正在为《Familia Romana》Cap. {to_roman(chapter)} 写一篇"句法脚手架"微阅读。

## 教学目标
{description}

目标章的难度**不在词汇**而在**句法复杂度**。本阅读的目的:
- 用 ≤ Cap. {to_roman(chapter)} 已学词汇 ({len(vocab)} 个)
- 反复展示 Cap. {to_roman(chapter)} 新出现的句法模式 (≥ 5 次)
- 让学习者通过"熟悉词汇 + 新句法"的组合,跨过句法障碍

## 句法重点 (必须反复出现 ≥ 5 次)
1. **Oratiō oblīqua (间接引语)**: dīcō + acc + inf, putō + acc + inf
   - 例: pater dīxit sē fēlīcem esse. (父亲说他很幸福)
   - 例: māter putat fīlium dormīre. (母亲认为儿子在睡觉)
2. **从句**: quod, cum, ut 引导
3. **其他目标章新句法** (请自行识别)

## 内容约束
- 长度: 200-300 词
- 仅用 Cap. 1-{chapter} 词汇 (见下方样本)
- 角色沿用 Familia Romana: Mārcus, Iūlia, pater, māter
- 风格贴近 LLPSI 原文: 第三人称叙述、简单句为主、靠句法重复而非华丽修辞
- **不要翻译成中文** (用户会自己读)
- 输出格式: 纯拉丁语,分 3-4 段,段间空行

## 已知词汇样本 (供参考,非穷尽)
{', '.join(vocab_sample)}

## 输出示例 (仅供风格参考,不要照抄)
"Mārcus Mātrem Audit" 中的句法结构: pater dīxit sē..., māter putat eum..., servus nārrāvit eum...

## 你的任务
现在,请写出 Cap. {to_roman(chapter)} 的微阅读。开头可以以 Mārcus/Iūlia/pater/māter 中任一角色为视角。
"""


def build_density_prompt(chapter: int, vocab: set[str], new_words: list[tuple[str, int]],
                         description: str) -> str:
    """
    [密度墙版本 Prompt]
    用于 Cap. 25: 在已有词汇基础上预热 + 反复复现新词
    """
    new_words_str = ", ".join(f"{w}({c}次)" for w, c in new_words[:15])
    vocab_sample = sorted(list(vocab))[:80]

    return f"""你是一位精通 LLPSI 教学法的拉丁语作家,正在为《Familia Romana》Cap. {to_roman(chapter)} 写一篇"词汇脚手架"微阅读。

## 教学目标
{description}

本章新词密度高达 30.3%,主要为希腊罗马神话专名,需要多次复现才能记忆。

## 词汇重点 (必须复现 ≥ 4 次)
**本章高频新词**: {new_words_str}

**复现策略**:
- 这些神话专名应在文本中出现 **≥ 4 次**
- 优先用角色对话/动作重复,不要简单列举
- 适度使用 Cap. {chapter - 1} 已知词汇作铺垫,降低首次阅读门槛

## 内容约束
- 长度: 200-300 词
- 角色可用 Familia Romana 原角色 (Mārcus 等) 或本章新角色 (Thēseus, Ariadna, Mīnoēs)
- 故事围绕本章新词展开: 一个完整的微型神话场景
- **不要翻译成中文**
- 输出格式: 纯拉丁语,分 3-4 段,段间空行

## 已知词汇样本 (供参考)
{', '.join(vocab_sample)}

## 你的任务
请围绕"Thēseus 与 Labyrinthus"主题写一篇微阅读,让学习者通过故事自然习得这些神话专名。
"""


# ============================================================
# 演示样章 (用于 MVP 阶段,人工校对后由真实 LLM 批量生成)
# ============================================================
DEMO_SAMPLES = {
    8: {
        "title": "Mārcus Mātrem Audit",
        "subtitle": "Cap. VIII  · 句法脚手架: oratiō oblīqua",
        "latin": """\
Mārcus, fīlius Iūliī, hodiē ex scholā rediit. In viā Mārcum Iūlia cōnspēxit et eum rogāvit: "Cūr tardē vēnistī, Mārce?" Mārcus respondēbat: "Magister noster multa nōbīs nārrāvit. Dīxit sē crās Rōmam īre. Putō eum iter facere velle. Ego autem intellegō eum fessum esse, nam diū in scholā labōrāvit."

Mārcus domum vēnit. Māter eum in vestibulō exspectābat. Māter Mārcō dīxit: "Pater tuus hodiē in oppidum iīsse putō. Servus nārrāvit eum mercēs ēmisse. Ego putō patrem tuum crās domum redire. Nōlī timēre, fīli mī!"

Mārcus rogāvit: "Māter, cūr pater nōn iam vēnit?" Māter respondēbat: "Pater mihi dīxit sē hodiē serō ventūrum esse. Intellegō eum in viā morātum esse." Mārcus intellexit mātrem paulum trīstem esse, sed dīxit: "Māter, audiō patrem in viā esse. Vīsus est mihi eum cōnspicere!" Māter respondit: "Vērum dīcis, Mārce! Pater noster adest!"

Pater in vestibulō stābat et fīlium suum vīdit. Pater Mārcō dīxit: "Fīli mī, magister tuus mihi nārrāvit tē hodiē bene labōrāvisse. Putō tē fēlīcem esse!" Mārcus laetus erat. Scīvit patrem suum sē amāre.""",
    },
    25: {
        "title": "Thēseus in Labyrinthō",
        "subtitle": "Cap. XXV  · 词汇脚手架: 神话专名复现",
        "latin": """\
Thēseus fīlius rēgis Athēnārum erat. Is puer fortis et pulcher erat. Multī virī eum laudābant. Thēseus diū cupidus erat Crētam eūndī. Crēta īnsula magna in marī erat. In Crētā Labyrinthus aedificium mirum erat.

Labyrinthus domus Monstrī erat. Monstrum Mīnotaurus appellābātur. Mīnotaurus in Labyrinthō habitābat et hominēs vorābat. Rēx Crētae, Mīnoēs, Athēniēnsibus imperāvit ut septem iuvenēs quotannīs mitterent. Thēseus hoc audīvit et dīxit: "Ego ipse Crētam ibō et Monstrum necābō!"

Thēseus nāvem cōnscendit et in Crētam vēnit. Ibi Ariadna, fīlia Mīnois, eum vīdit. Ariadna pulchra puella erat. Ea Thēseō dīxit: "Tibi auxilium dabō. Hoc filum cape. Cum Mīnotaurum necāveris, iterum ad portam sequere." Thēseus Ariadnae grātiās ēgit.

Thēseus Labyrinthum intrāvit et Mīnotaurum occīdit. Turn, sicut Ariadna docuerat, filum tractāvit et ex Labyrinthō ēvāsit. Ariadna eum exspectābat. Laetī in patriam revertērunt. Sed, pro trīstiōre fābulā, Thēseus in viā ad Naxum Ariadnae oblītus est et sine eā rediit. Pater Thēseī gaudenter eum excepit, sed Ariadna misera in Naxō remānsit.""",
    },
    10: {
        "title": "Mārcus Ferās Observat",
        "subtitle": "Cap. X    · 句法脚手架: prōnōmen relātīvum (quī, quae, quod)",
        "latin": """\
Mārcus hodiē in macellum cum mātre iit. In viā Mārcus dīxit: "Māter, cūr hodiē in macellum īmus?" Māter respondit: "Eō, ut piscem optimum, quem coquāmus, emāmus. Pater noster crās ad cēnam multōs virōs vocāvit, quī nōbīscum cēnam edent."

In macellō Mārcus multa animālia, quae in tabernīs iacebant, vīdit. Mārcus mātrem suam rogāvit: "Māter, quae sunt haec animālia, quae hīc iacent?" Māter respondit: "Sunt piscēs, quī in aquā vīvunt, et avēs, quae in caelō volāre solent." Mārcus attonitus erat et rogāvit: "Quid est animal, quod in aquā habitat et nōn volat?" Māter dīxit: "Piscis est animal, quod in aquā habitat et nāre scit. Piscis, quī mortuus est, ēmitur. Piscis, quī vīvit, in aquā natat."

Mārcus dīxit: "Cūr hīc tot piscēs mortuī iacent?" Māter respondit: "Mercātor piscēs, quī mortuī sunt, vēndit. Eōs, quī recentissimī sunt, emere volumus." Mārcus intellexit et mercātōrem rogāvit: "Quis est piscis, quem optimissimum habēs?" Mercātor dīxit: "Hic piscis, quem ostendō, recentissimus est. Hunc eme, fīlī!"

Mārcus avem, quae in caveā pendēbat, audiit. Avis cantābat "Tū, tū, tū!" Mārcus rogāvit: "Cūr avis haec, quae cantat, in caveā est?" Māter respondit: "Avis, quae in caveā vīvit, ā mercātōre vēnditur. Avis, quae in silvā habitat, libera est et in caelō volāre potest. Avis, quae libera est, melius cantat. Avis, quae clausa est, misera esse vidētur."

Mārcus attonitus dīxit: "Eheu! Avēs, quae in silvīs vīvunt, meliōrem vītam habent! Avēs, quae in caveīs clauduntur, dolent!" Māter dīxit: "Vērum dīcis, fīlī mī. Sed hominēs, quī in urbe vīvunt, avēs capere volunt, quia cibus delīcātus sunt. Est trīste."

Mārcus tunc aquilam, quae in tabulā picta erat, vīdit. Mārcus dīxit: "Māter, quae est illa avis magna, quae in tabulā pingitur?" Māter respondit: "Aquila est fera, quae in altissimīs montibus habitat. Aquila, quae regīna avium appellātur, in caelō altissimō volat." Mārcus dīxit: "Aquila, quae in montibus habitat, pulcherrima esse vidētur!"

Mārcus piscem optimum, quem mercātor dedit, ēmit. Māter, quae laeta erat, dīxit: "Fīlī mī, hodiē multa dīdicistī! Piscem, quem ēmistī, crās in cēnā coquēmus. Pater noster, quī multōs virōs vocāvit, piscem optimum habēbit." Sīc Mārcus, quī multa didicit, cum mātre domum revertit.""",
    },
    "10_lex": {
        "title": "Piscis, Avis, Bestia",
        "subtitle": "Cap. X    · 词汇脚手架: 动植物与能力词 (potest, volat, mortuus)",
        "latin": """\
Hodiē Mārcus in macellum iit. Mārcus, quī multa vidēre amat, in macellō piscēs, avēs et bestiās cōnspexit. Piscis est animal, quod in aquā habitat. Piscis in aquā nāre potest. Avēs in caelō volāre possunt. Avis in caelō volat. Bestia in silvā ambulat. Mēns Mārcī excitāta est.

Mārcus mercātōrem rogāvit: "Cūr piscēs, quī mortuī sunt, hīc iacent?" Mercātor respondet: "Piscis, quī mortuus est, emī nōn potest. Enim necesse est, ut piscēs, quī vīvunt, emās." Mārcus intellexit et rogāvit: "Estne avis mortua etiam ēsse nōn potest?" Mercātor dīxit: "Eadem ratiō est! Avis mortua etiam emī nōn potest."

Mārcus, quī erat puer cupidus, avem, quae cantat, in caveā audiit. Avis haec cantat: "Tū, tū, tū!" Mārcus dīxit: "Avis, quae cantat, laeta esse vidētur!" Mercātor dīxit: "Avēs, quae in caveīs vīvunt, cantant, sed avēs, quae in silvīs vīvunt, melius cantant. Avēs, quae liberae sunt, in caelō volāre possunt; avēs, quae in caveīs clausae sunt, volāre nōn possunt."

Mārcus dīxit: "Tum avēs, quae in silvīs vīvunt, meliōrem vītam habent!" Mercātor respondit: "Vērum dīcis! Sed hominēs, quī in urbe Rōmae vīvunt, avēs capere volunt, nam avēs cibus bonus sunt." Mārcus putāvit et dīxit: "Hominēs avēs, quae vīvunt, in caveīs claudunt, ut eās edere possint. Estne hoc iūstum?"

Mercātor dīxit: "Fīlī, nōn omnia, quae hominēs faciunt, iūsta sunt, sed necesse est, ut hominēs edant. Enim sine cibō hominēs vīvere nōn possunt. Bestiae quoque edere necesse habent. Bestia, quae nōn edit, mortua fit."

Tum Mārcus bestiam, quae in macellō iacebat, vīdit. Bestia haec mortua erat. Mārcus dīxit: "Haec bestia mortua est; emī nōn potest." Mercātor respondit: "Vērum dīcis! Bestia, quae vīvit, emī potest. Enim bestiam, quae mortua est, edere nōn possumus. Sed feram, quae vīvit, necāre necesse est, ut eam edere possīmus." Mārcus intellexit.

Mārcus dīxit: "Avēs, quae in caelō volāre possunt, pulcherrimae sunt. Piscēs, quī in aquā nāre possunt, taciti sunt. Sed bestia, quae in silvā ambulat, fera est et hominem, quem cōnspicit, necāre potest." Mercātor subrīsit et dīxit: "Bene dīcis, fīlī mī!"

Mārcus domum revertit et mātrī suae omnia nārrāvit. Māter dīxit: "Fīlī mī, hodiē multa dīdicistī! Piscis, quem emimus, in cēnā edēmus. Avis, quae vīvit, crās emēmus. Nunc necesse est, ut piscem coquāmus." Mārcus laetē mātrem adiuvit et cēnam parāvērunt. Familia tota piscem optimum in cēnā ēdit et laeta erat.""",
    },
}


# ============================================================
# 生成与输出
# ============================================================
def build_supplement_header(chapter: int, chap_type: str, description: str,
                            new_words: list[tuple[str, int]]) -> str:
    """生成补充阅读文件的元数据头"""
    type_zh = "句法脚手架" if chap_type == "syntax" else "词汇脚手架"
    new_words_str = ", ".join(f"{w}({c}次)" for w, c in new_words[:10])

    header = f"""\
# Supplementum Cap. {to_roman(chapter)}
## {description}
## 脚手架类型: {type_zh}

**本章新词** (前 10): {new_words_str}

**使用建议**:
- 推荐在读完《Familia Romana》Cap. {to_roman(chapter)} **之后** 立即阅读
- 重点关注脚手架目标: 句法模式 / 关键词复现
- 遇到生词请回到原章节对应位置重读上下文

---

"""
    return header


def write_supplement(chapter: int, chap_type: str, description: str,
                     new_words: list[tuple[str, int]], latin_text: str,
                     file_suffix: str = "") -> str:
    """写入单个补充阅读文件

    Args:
        file_suffix: 变体后缀,如 "syntax" / "lex"
            - 空字符串 → supplement_NN.txt
            - "syntax" → supplement_NN_syntax.txt
            - "lex"    → supplement_NN_lex.txt
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    header = build_supplement_header(chapter, chap_type, description, new_words)
    full_text = header + latin_text + "\n"

    suffix_part = f"_{file_suffix}" if file_suffix else ""
    output_path = os.path.join(OUTPUT_DIR, f"supplement_{chapter:02d}{suffix_part}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    return output_path


def write_reading_guide(generated: list[dict]) -> str:
    """生成阅读路线图"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    guide = ["# 阅读路线图 · Supplementa Lectionum\n"]
    guide.append("本目录包含《Familia Romana》重点章节的补充阅读材料。\n\n")
    guide.append("## 使用顺序\n\n")
    guide.append("**推荐**: 在读完《Familia Romana》对应章节**之后**立即阅读对应 supplement,趁热打铁。\n\n")
    guide.append("| 章节 | 类型 | 文件 | 推荐度 |\n")
    guide.append("|:----:|:----:|:----:|:------:|\n")

    priority_map = {8: 1, 9: 1, 10: 1, 11: 2, 12: 2, 13: 2, 25: 3}
    priority_zh = {1: "⭐⭐⭐ 必修", 2: "⭐⭐ 推荐", 3: "⭐ 补充"}

    for item in generated:
        ch = item['chapter']
        variant = item.get('variant')
        # 文件名: 有 variant 时补上后缀
        fname = f"supplement_{ch:02d}" + (f"_{variant}" if variant else "") + ".txt"
        guide.append(
            f"| Cap. {to_roman(ch)} | {item['type_zh']} | "
            f"[{fname}](./{fname}) | "
            f"{priority_zh[priority_map.get(ch, 2)]} |\n"
        )

    guide.append("\n## 脚手架类型说明\n\n")
    guide.append("### 句法脚手架 (Cap. 8-13)\n")
    guide.append("针对「第九章墙」—— 这些章节的难度不在词汇,而在句法复杂度跃迁 (间接引语/从句/夺格句型)。\n")
    guide.append("微阅读用 Cap. 1-7 熟悉词汇反复展示新句法,**让学习者通过熟悉度消解陌生感**。\n\n")
    guide.append("### 词汇脚手架 (Cap. 25, Cap. 10 *lex* 变体)\n")
    guide.append("针对「密度之墙」—— 本章新词密度 30.3% (全书最高),主要为希腊罗马神话专名 (Thēseus, Ariadna, Labyrinthus 等)。\n")
    guide.append("微阅读通过故事化复现,让学习者在情节中自然习得这些专名。\n\n")
    guide.append("---\n\n")
    guide.append("> **生成方法**: `ampliata_generate.py` | 详见 [Project_Plan.md](../Project_Plan.md) v1.3.0\n")

    output_path = os.path.join(OUTPUT_DIR, "reading_guide.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(guide))
    return output_path


# ============================================================
# 主入口
# ============================================================
def generate_demo() -> list[dict]:
    """
    MVP 演示模式:
    - 复用 OCR 文本提取目标章新词
    - 调用 LLM Prompt 模板构建 (实际生成时由 Claude/GPT-4 完成)
    - MVP 阶段先用 DEMO_SAMPLES 样章展示效果
    """
    print("=" * 60)
    print("LLPSI+++ Step 3 · 补充阅读生成 (MVP 演示模式)")
    print("=" * 60)

    # 读取 OCR 文本
    print(f"\n[1/4] 读取 OCR 文本: {INPUT_FILE}")
    chapter_readings = get_chapters_text(INPUT_FILE)
    print(f"      识别到 {len(chapter_readings)} 个章节")

    # 对每个优先章节: 提取新词 + 构建 Prompt + 写入文件
    print(f"\n[2/4] 处理 {len(PRIORITY_CHAPTERS)} 个优先章节...")
    generated = []

    for chapter, (chap_type, description) in PRIORITY_CHAPTERS.items():
        new_words = get_top_new_words(chapter_readings, chapter)
        vocab = get_vocab_up_to(chapter_readings, chapter)

        # 构建 Prompt (供真实 LLM 调用时使用,此处仅打印验证)
        if chap_type == "syntax":
            prompt = build_syntax_prompt(chapter, vocab, new_words, description)
        else:
            prompt = build_density_prompt(chapter, vocab, new_words, description)

        # MVP 演示: 使用预生成的样章
        # 支持同章节多变体 (例如 Cap. 10 同时有 syntax 与 lex 两个变体)
        variants = []
        if chapter in DEMO_SAMPLES:
            variants.append((chapter, DEMO_SAMPLES[chapter]))
        if f"{chapter}_lex" in DEMO_SAMPLES:
            variants.append((f"{chapter}_lex", DEMO_SAMPLES[f"{chapter}_lex"]))

        for variant_key, sample in variants:
            # 文件命名: 单一变体 → supplement_NN.txt; 多变体 → supplement_NN_variant.txt
            is_multi = len(variants) > 1
            if is_multi:
                variant_suffix = "syntax" if sample["title"].endswith("Observat") or "prōnōmen" in sample.get("subtitle", "").lower() or "relātīvum" in sample.get("subtitle", "") else "lex"
                # 更可靠: 从 subtitle 解析 variant 名
                if "句法" in sample["subtitle"]:
                    variant_suffix = "syntax"
                elif "词法" in sample["subtitle"] or "词汇" in sample["subtitle"]:
                    variant_suffix = "lex"
                else:
                    variant_suffix = "lex" if variant_key == f"{chapter}_lex" else "syntax"
                # header 类型需要同步切换: lex 变体的 header 应该是"词汇脚手架"
                header_chap_type = "lex" if variant_suffix == "lex" else chap_type
                output_path = write_supplement(
                    chapter, header_chap_type, description, new_words,
                    sample["latin"], file_suffix=variant_suffix
                )
            else:
                output_path = write_supplement(
                    chapter, chap_type, description, new_words, sample["latin"]
                )

            type_zh = "句法脚手架" if chap_type == "syntax" else "词汇脚手架"
            word_count = len(sample["latin"].split())

            print(f"  ✓ Cap. {to_roman(chapter):5s} ({chap_type:6s}) | "
                  f"新词 {len(new_words):3d} | {word_count:3d} 词 → {output_path}")

            generated.append({
                'chapter': chapter,
                'chap_type': chap_type,
                'type_zh': type_zh,
                'title': sample["title"],
                'word_count': word_count,
                'prompt': prompt,
                'variant': variant_suffix if is_multi else None,
            })

    # 生成 Prompt 预览 (供调试)
    print(f"\n[3/4] 生成的 Prompt 样例 (供 LLM API 调试):\n")
    if generated:
        sample_item = generated[0]
        print(f"--- Cap. {to_roman(sample_item['chapter'])} Prompt ---")
        print(sample_item['prompt'][:600] + "...\n[truncated]\n")

    # 生成阅读路线图
    print(f"[4/4] 生成阅读路线图...")
    guide_path = write_reading_guide(generated)
    print(f"      → {guide_path}")

    print(f"\n{'=' * 60}")
    print(f"✓ 全部完成! 共生成 {len(generated)} 篇样章")
    print(f"  输出目录: {OUTPUT_DIR}")
    print(f"{'=' * 60}")

    return generated


if __name__ == "__main__":
    generate_demo()
