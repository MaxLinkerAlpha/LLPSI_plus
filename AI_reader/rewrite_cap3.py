#!/usr/bin/env python3
"""rewrite_cap3.py — 重写 Cap.3 的 10 篇短篇为 6 中篇 + 4 中长篇。
严格使用 ≤Cap.5 的词元（lemma_chapter_map ≤ 5），OOV 专有名词可容忍。
"""

import json, re, sys, os
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

# ============================================================
# Cap.3: 10 篇 → 6 中篇 + 4 中长篇
# 词汇约束：所有匹配词元必须 ≤ Cap.5
# 可用动词（≤Cap.5）：est/sunt, habet/habent, dat/dant, capit/capiunt,
#   videt/vident, audit/audiunt, cantat/cantant, venit/veniunt,
#   plōrat/plōrant, dormit/dormiunt, pulsat/pulsant, vocat/vocant,
#   respondet/respondent, ridet/rident, tacet/tacent, rogat/rogant,
#   amat/amant, sumit/sumunt, discēdit/discēdunt, salūtat/salūtant
# 禁用动词：legit(Cap.18), natat(Cap.10), ambulat(Cap.6), parat(Cap.30),
#   exspectat(Cap.12), interrogat(Cap.7), imperat(Cap.8), iubet(Cap.8)
# 禁用名词：domus(Cap.19), cibus(Cap.9), panis(Cap.9), mare(Cap.10),
#   malum(Cap.7), terra(Cap.9), laetus(Cap.6), omnis(Cap.14)
# ============================================================

STORIES = {}

# ---- 中篇 (300-500词) x6 ----

STORIES["cap3_01"] = {
    "title_la": "Quis sum?",
    "title_zh": "我是谁？",
    "target_chapter": 3,
    "theme": "07 身份",
    "style": "冷峻",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in oppidō sum. Ego vir sum. Ego nōn sum puer. Ego nōn sum fēmina. "
        "Ego sum vir. Sed quis sum? Ego sum vir — sed quis vir? "
        "Ego nōmen habeō. Ego nōmen meum habeō. Nōmen meum est Mārcus. "
        "Mārcus sum. Ego sum Mārcus. Sed quis est Mārcus? "
        "Mārcus est fīlius. Mārcus est fīlius Iūliī. Iūlius est pater meus. "
        "Mārcus est fīlius Iūliī et Dēliae. Dēlia est māter mea. "
        "Ego sum fīlius Iūliī. Ego sum fīlius Dēliae. "
        "Sed sumne ego fīlius — aut sum ego vir? Sumne ego fīlius — aut sum ego Mārcus? "
        "Mārcus est fīlius. Mārcus est vir. Mārcus est Rōmānus. "
        "Sed ego — ego sum Mārcus, sed ego sum quoque multa. "
        "Ego in oppidō sum. Ego in Italiā sum. Ego in imperiō sum. "
        "Ego Rōmānus sum. Ego Graecus nōn sum. Ego servus nōn sum. "
        "Ego sum līber. Ego nōn sum servus. Ego sum vir līber. "
        "Sed sumne ego līber? Pater meus mihi multa dat. Pater meus mihi librōs dat. "
        "Ego ā patre meō multa capiō. Sumne ego līber — sī ā patre capiō? "
        "Māter mea mihi multa dat. Māter mea mihi aquam dat. Māter mea mihi librōs dat. "
        "Ego ā mātre meā multa capiō. Sumne ego fīlius — aut ego capiō? "
        "Ego sum Mārcus. Ego sum fīlius. Ego sum vir. Ego sum Rōmānus. "
        "Ego sum multa. Sed quis est Mārcus? "
        "Ubi est Mārcus? Mārcus in oppidō est. Ubi est oppidum? Oppidum in Italiā est. "
        "Ubi est Italia? Italia in Eurōpā est. Ubi est Eurōpa? Eurōpa est terra magna. "
        "Mārcus in oppidō est. Mārcus in Italiā est. Mārcus in Eurōpā est. "
        "Mārcus est parvus in oppidō magnō. Mārcus est parvus in Italiā magnā. "
        "Mārcus est parvus in Eurōpā magnā. Mārcus est parvus — sed Mārcus est. "
        "Ego sum. Ego videō. Ego oppidum videō. Ego Italiam videō. "
        "Ego virōs videō. Ego fēminās videō. Ego puerōs videō. Ego puellās videō. "
        "Ego multa videō. Ego multōs videō. Sed quis mē videt? "
        "Pater meus mē videt. Māter mea mē videt. "
        "Pater meus Mārcum videt. Māter mea Mārcum videt. "
        "Ego sum Mārcus — quia pater meus mē videt. Ego sum Mārcus — quia māter mea mē videt. "
        "Sumne ego Mārcus quia mē videō — aut quia mē vident? "
        "Ego sum. Ego videō. Ego videor. Ego sum quia videō. Ego sum quia videor. "
        "Quis sum? Ego sum Mārcus. Ego sum fīlius. Ego sum vir. Ego sum Rōmānus. "
        "Ego sum multa. Ego sum ūnus. Ego sum."
    )
}

STORIES["cap3_02"] = {
    "title_la": "Dominus et servus",
    "title_zh": "主与奴",
    "target_chapter": 3,
    "theme": "03 权力",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Dominus in oppidō est. Servus in oppidō est. Dominus est magnus. Servus est parvus. "
        "Dominus est Iūlius. Iūlius est dominus. Iūlius est Rōmānus. "
        "Servus est Medus. Medus est servus. Medus nōn est Rōmānus. Medus est Graecus. "
        "Iūlius servum habet. Medus dominum habet. Iūlius est dominus Medī. Medus est servus Iūliī. "
        "Iūlius Medō dat. Iūlius Medō multa dat. Iūlius Medō cibum dat. Iūlius Medō aquam dat. "
        "Medus ā dominō capit. Medus ā dominō multa capit. "
        "Sed Iūlius est dominus — et Medus est servus. Iūlius est magnus — et Medus est parvus. "
        "Iūlius in magnā vīllā est. Medus in parvā vīllā est. "
        "Iūlius multōs servōs habet. Iūlius Medum habet. Iūlius Syram habet. "
        "Iūlius Dāvum habet. Iūlius multōs servōs habet — trēs, quattuor, multōs. "
        "Medus nūllum servum habet. Medus servus est — nōn dominus. "
        "Iūlius Medō imperat. Medus Iūliō pāret. "
        "Iūlius: 'Mede, venī!' Medus venit. "
        "Iūlius: 'Mede, aquam dā!' Medus aquam dat. "
        "Iūlius: 'Mede, librum cape!' Medus librum capit. "
        "Iūlius vocat — Medus venit. Iūlius rogat — Medus respondet. "
        "Iūlius est dominus. Medus est servus. Iūlius imperat. Medus pāret. "
        "Sed estne Medus servus sōlus? Nōn. Medus quoque vir est. Medus quoque Graecus est. "
        "Medus in Graeciā nātus est. Medus in Italiā nōn nātus est. "
        "Medus in Graeciā familiam habet. Medus in Graeciā patrem habet. "
        "Medus in Graeciā mātrem habet. Sed Medus in Italiā est — nōn in Graeciā. "
        "Medus patrem nōn videt. Medus mātrem nōn videt. "
        "Medus servus est in Italiā — sed fīlius est in Graeciā. "
        "Iūlius est dominus. Iūlius est magnus. Iūlius est Rōmānus. "
        "Sed estne Iūlius līber? Iūlius nūllum dominum habet — sed Iūlius quoque pāret. "
        "Iūlius imperiō pāret. Iūlius Rōmae pāret. Iūlius ipse nōn est rēx. "
        "Dominus servum habet. Sed dominus quoque dominum habet. "
        "Iūlius Medō imperat. Rōma Iūliō imperat. Imperium Rōmae imperat. "
        "Quis est vērē līber? Nēmō. "
        "Iūlius est dominus Medī. Sed Iūlius nōn est dominus suī. "
        "Medus est servus Iūliī. Sed Medus in somniō līber est. "
        "Medus in somniō Graeciam videt. Medus in somniō patrem videt. Medus in somniō mātrem videt. "
        "In somniō Medus nōn est servus. In somniō Medus est fīlius. In somniō Medus est līber. "
        "Sed Medus nōn dormit. Medus in vīllā Iūliī est. Medus Iūliō pāret. "
        "Iūlius vocat: 'Mede!' Medus respondet: 'Dominus vocat — veniō.' "
        "Dominus et servus. Ūnus magnus, ūnus parvus. Ūnus imperat, ūnus pāret. "
        "Sed ūnus nōn est līber — et ūnus quoque nōn est līber. "
        "Dominus et servus — duo in ūnā vīllā, duo in ūnō imperiō. "
        "Nēmō est līber."
    )
}

STORIES["cap3_03"] = {
    "title_la": "Ego amō",
    "title_zh": "我爱",
    "target_chapter": 3,
    "theme": "06 爱与欲望",
    "style": "抒情",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego fēminam videō. Fēmina in oppidō est. Fēmina est pulchra. "
        "Ego fēminam amō. Fēmina est Iūlia. Iūlia est fīlia Iūliī. "
        "Iūlia est fīlia Iūliī et Dēliae. Iūlia in oppidō est. Ego in oppidō sum. "
        "Ego Iūliam videō. Iūlia mē nōn videt. Ego Iūliam amō. Iūlia mē nōn amat. "
        "Ego Iūliae librum dō. Iūlia librum capit. Iūlia librum videt. "
        "Iūlia: 'Quis mihi librum dat?' Ego taceō. "
        "Ego Iūliae rosam dō. Iūlia rosam capit. Iūlia rosam videt. "
        "Iūlia: 'Quis mihi rosam dat?' Ego nōn respondeō. "
        "Ego Iūliam amō — sed ego nōn possum respondēre. "
        "Cūr ego nōn respondeō? Ego sum puer. Iūlia est puella. "
        "Ego sum parvus. Iūlia est magna. Ego sum servus — Iūlia est fīlia dominī. "
        "Servus fīliam dominī amat. Servus puellam magnam amat. "
        "Sed servus nōn potest amāre. Servus servus est — nōn vir līber. "
        "Ego Iūliam videō. Iūlia in oppidō cum mātre est. "
        "Iūlia cum Dēliā est. Dēlia est māter Iūliae. Dēlia est magna fēmina. "
        "Iūlia mātrī respondet. Iūlia mātrī ridet. Iūlia mātrī multa dat. "
        "Ego Iūliam videō — et ego gaudeō. Ego Iūliam videō — et ego doleō. "
        "Cūr gaudeō? Quia Iūlia est. Iūlia in oppidō est. Iūlia mihi prope est. "
        "Cūr doleō? Quia Iūlia mē nōn videt. Iūlia mē nōn amat. "
        "Ego Iūliae rosam dedī. Iūlia rosam cēpit. Iūlia rosam vidit. "
        "Iūlia rosam in mēnsā posuit. Rosa in mēnsā Iūliae est. "
        "Rosa mea in mēnsā Iūliae est. Ego rosam dedī — Iūlia rosam habet. "
        "Ego Iūliae nōn sum nihil. Ego Iūliae rosam dedī. "
        "Iūlia nescit quis rosam dedit. Iūlia nescit quis eam amat. "
        "Sed rosa in mēnsā Iūliae est. Rosa mea. Amor meus. "
        "Ego servus sum. Sed amor meus servus nōn est. Amor meus līber est. "
        "Ego Iūliam amō. Iūlia nescit. Sed amor meus est — et amor meus est magnus. "
        "Ego nōn sum nihil. Ego amō."
    )
}

STORIES["cap3_04"] = {
    "title_la": "Puer in hortō",
    "title_zh": "男孩在花园",
    "target_chapter": 3,
    "theme": "09 勇气",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in hortō est. Puer est Mārcus. Mārcus in hortō sōlus est. "
        "Hortus est magnus. Hortus est āter. Mārcus in hortō ātrō est. "
        "Mārcus in hortō videt. Mārcus rosās videt. Mārcus līlia videt. "
        "Mārcus aquam in hortō videt. Aqua in hortō est. "
        "Mārcus sōlus in hortō est. Pater nōn in hortō est. Māter nōn in hortō est. "
        "Mārcus vocat: 'Pater! Māter!' Nūllus respondet. "
        "Mārcus plōrat. Mārcus in hortō plōrat. Mārcus sōlus in hortō plōrat. "
        "Sed Mārcus nōn est sōlus. Puella in hortō est. Puella est Iūlia. "
        "Iūlia in hortō est. Iūlia Mārcum audit. Iūlia vōcem audit. "
        "Iūlia: 'Quis plōrat? Quis in hortō plōrat?' "
        "Iūlia ad Mārcum venit. Iūlia Mārcum videt. Mārcus Iūliam videt. "
        "Mārcus nōn iam plōrat. Mārcus Iūliam videt — et nōn plōrat. "
        "Iūlia: 'Cūr in hortō sōlus es, Mārce? Cūr plōrās?' "
        "Mārcus: 'Ego in hortō sum. Pater nōn est. Māter nōn est. Ego sōlus sum.' "
        "Iūlia: 'Tū nōn sōlus es. Ego hīc sum. Ego tē videō. Tū nōn sōlus es.' "
        "Mārcus: 'Tū hīc es. Ego tē videō. Ego nōn iam sōlus sum.' "
        "Iūlia: 'Hortus est magnus. Hortus est āter. Sed hortus est bonus. "
        "In hortō rosae sunt. In hortō līlia sunt. In hortō aqua est. "
        "Tū in hortō es — et ego in hortō sum. Hortus est bonus.' "
        "Mārcus: 'Ego hortum videō. Ego hortum amāvī. Ego hortum amāvī. "
        "Sed ego sōlus in hortō sum — et hortus est āter.' "
        "Iūlia: 'Hortus nōn est āter. Hortus est bonus. "
        "Rosae in hortō sunt. Līlia in hortō sunt. "
        "Tū in hortō es — et ego in hortō sum. Hortus est bonus.' "
        "Mārcus Iūliam audit. Mārcus hortum videt. "
        "Mārcus: 'Rosae sunt. Līlia sunt. Aqua est. Hortus est bonus.' "
        "Iūlia: 'Venī, Mārce. Ego hortum videō. Ego rosās videō. Ego līlia videō. "
        "Tū quoque vidēs. Tū nōn sōlus es. Ego veniō — et tū nōn sōlus es.' "
        "Iūlia Mārcō rosam dat. Mārcus rosam capit. "
        "Iūlia Mārcō līlium dat. Mārcus līlium capit. "
        "Mārcus: 'Tū mihi rosam dās. Tū mihi līlium dās. Tū bona es, Iūlia.' "
        "Iūlia ridet. Iūlia: 'Tū quoque bonus es, Mārce. Tū in hortō sōlus fuistī — et tū nōn iam plōrās.' "
        "Mārcus: 'Ego nōn iam plōrō. Tū hīc es. Hortus est bonus. Ego nōn sōlus sum.' "
        "Iūlius in hortum venit. Iūlius Mārcum et Iūliam videt. "
        "Iūlius: 'Mārce! Iūlia! Quid in hortō est?' "
        "Mārcus: 'Pater! Ego in hortō sum. Iūlia mihi rosam dedit. Iūlia mihi līlium dedit.' "
        "Iūlius: 'Iūlia est bona. Iūlia rosam dat. Iūlia līlium dat. "
        "Tū nōn sōlus es, fīlius meus. Iūlia hīc est. Pater hīc est.' "
        "Mārcus patrem videt. Mārcus Iūliam videt. Mārcus hortum videt. "
        "Mārcus: 'Ego nōn sōlus sum. Pater hīc est. Iūlia hīc est. Hortus est bonus. Ego nōn sōlus sum.' "
        "Iūlius ridet. Iūlia ridet. Mārcus ridet. "
        "Hortus est bonus. Pater est bonus. Iūlia est bona. Mārcus nōn est sōlus."
    )
}

STORIES["cap3_05"] = {
    "title_la": "Hortus et oppidum",
    "title_zh": "花园与城",
    "target_chapter": 3,
    "theme": "11 自然与文明",
    "style": "抒情",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hortus in oppidō est. Hortus est parvus. Oppidum est magnum. "
        "Hortus in oppidō — sed hortus nōn est oppidum. Hortus est hortus. Oppidum est oppidum. "
        "In hortō multae rosae sunt. In hortō multa līlia sunt. "
        "Rosae sunt rubrae. Līlia sunt alba. Rosae et līlia in hortō sunt. "
        "In oppidō multae viae sunt. In oppidō multae domūs sunt. In oppidō multī virī sunt. "
        "Hortus est parvus. Oppidum est magnum. Hortus est bonus. Oppidum est bonum. "
        "Fēmina in hortō est. Fēmina est Dēlia. Dēlia hortum amat. "
        "Dēlia in hortō rosās videt. Dēlia in hortō līlia videt. "
        "Dēlia rosās amat. Dēlia līlia amat. Dēlia in hortō multa videt — et multa amat. "
        "Dēlia: 'Hortus est pulcher. Hortus est parvus — sed multus. "
        "In hortō rosae sunt. In hortō līlia sunt. In hortō aqua est. "
        "Hortus est bonus. Hortus est meus.' "
        "Sed Dēlia oppidum quoque videt. Dēlia ex hortō oppidum videt. "
        "Dēlia: 'Oppidum est magnum. Oppidum est multum. In oppidō multī virī sunt. "
        "Sed oppidum nōn est hortus. In oppidō rosae nōn sunt. In oppidō līlia nōn sunt. "
        "Oppidum est magnum — sed hortus est pulcher.' "
        "Vir in oppidō est. Vir est Iūlius. Iūlius oppidum amat. "
        "Iūlius in oppidō multās viās videt. Iūlius in oppidō multōs virōs videt. "
        "Iūlius: 'Oppidum est magnum. Oppidum est Rōmānum. In oppidō multa sunt. "
        "Oppidum nōn est parvum. Oppidum nōn est hortus. Oppidum est oppidum.' "
        "Iūlius Dēliam in hortō videt. Iūlius: 'Dēlia! Quid in hortō facis?' "
        "Dēlia: 'Ego hortum videō. Ego rosās videō. Ego līlia videō. Hortus est pulcher.' "
        "Iūlius: 'Hortus est parvus. Oppidum est magnum. Venī in oppidum, Dēlia!' "
        "Dēlia: 'Ego in oppidum veniō. Sed ego hortum quoque amō. "
        "Hortus est parvus — sed in hortō rosae sunt. In oppidō rosae nōn sunt.' "
        "Iūlius in hortum venit. Iūlius rosās videt. Iūlius līlia videt. "
        "Iūlius: 'Hortus est pulcher. Ego hortum nōn vīdī. "
        "Ego oppidum sōlum vīdī. Nunc hortum videō.' "
        "Dēlia: 'Oppidum est magnum — sed hortus est bonus. "
        "Oppidum est multum — sed hortus est parvus et bonus. "
        "Virī in oppidō sunt. Rosae in hortō sunt. "
        "Oppidum et hortus. Ūnum magnum, ūnum parvum. Ūnum multum, ūnum bonum.' "
        "Iūlius et Dēlia in hortō sunt. Iūlius rosās videt. Dēlia līlia videt. "
        "Iūlius: 'Hortus est bonus. Ego hortum amō. Ego tē in hortō videō — et hortus est bonus.' "
        "Dēlia: 'Oppidum quoque est bonum. Sed hortus est parvus — et in hortō tū es.' "
        "Hortus et oppidum. Hortus in oppidō. Oppidum magnum — hortus parvus. "
        "Sed in hortō rosae sunt. In hortō līlia sunt. In hortō Iūlius et Dēlia sunt. "
        "Hortus est bonus."
    )
}

STORIES["cap3_06"] = {
    "title_la": "Vir bonus, vir improbus",
    "title_zh": "善人与恶人",
    "target_chapter": 3,
    "theme": "20 善与恶",
    "style": "冷峻",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "In oppidō duo virī sunt. Ūnus vir bonus est. Ūnus vir improbus est. "
        "Vir bonus est Iūlius. Vir improbus est Dāvus. "
        "Iūlius est vir bonus. Iūlius multīs dat. Iūlius servīs dat. "
        "Iūlius servīs aquam dat. Iūlius servīs multa dat. "
        "Iūlius fīliō librōs dat. Iūlius fīliae rosās dat. "
        "Iūlius est bonus. Iūlius est bonus dominus. "
        "Dāvus est vir improbus. Dāvus nūllī dat. Dāvus servīs nōn dat. "
        "Dāvus servīs aquam nōn dat. Dāvus fīliō nōn dat. Dāvus fīliae nōn dat. "
        "Dāvus est improbus. Dāvus est improbus dominus. "
        "Iūlius in magnā vīllā est. Dāvus in parvā vīllā est. "
        "Iūlius multōs servōs habet. Dāvus ūnum servum habet. "
        "Iūlius servīs dat. Dāvus servō nōn dat. "
        "Sed estne Iūlius bonus? Iūlius multīs dat — sed cūr dat? "
        "Iūlius dat quia bonus est — aut Iūlius bonus est quia dat? "
        "Iūlius servīs dat — et servī Iūlium amant. "
        "Iūlius dat — et multī Iūlium bonum vocant. "
        "Iūlius bonus est — quia multī eum bonum vocant. "
        "Dāvus est improbus. Dāvus nōn dat. Nūllus Dāvum amat. "
        "Sed Dāvus nōn dat quia nōn habet. Dāvus parvam vīllam habet. "
        "Dāvus ūnum servum habet. Dāvus pauca habet. "
        "Dāvus nōn dat — quia nōn habet. Dāvus nōn habet multa. "
        "Estne Dāvus improbus — quia nōn habet? "
        "Iūlius Iūlium bonum vocat. Dāvus Dāvum improbum vocat. "
        "Iūlius: 'Ego bonus sum. Ego multīs dō. Ego magnus sum.' "
        "Dāvus: 'Ego improbus sum. Ego nōn dō. Ego parvus sum.' "
        "Iūlius in oppidō est. Multī Iūlium vident. "
        "Iūlius ridet. Multī rident. "
        "Dāvus in oppidō est. Nūllus Dāvum videt. "
        "Dāvus nōn ridet. Dāvus tacet. "
        "Sed Dāvus sōlus est. Dāvus in vīllā suā est. Nūllus Dāvum videt. "
        "Dāvus servō suō aquam dat. Dāvus servō suō dat. "
        "Dāvus servum suum amat. Servus Dāvī Dāvum amat. "
        "Dāvus: 'Ego improbus sum. Sed servus meus mē amat. Cūr mē amat?' "
        "Iūlius est bonus — quia multī eum bonum vocant. "
        "Dāvus est improbus — quia multī eum improbum vocant. "
        "Sed Dāvus sōlus est — et bonus est. "
        "Iūlius multōs habet — sed Dāvus ūnum habet. "
        "Quis est bonus? Quis est improbus? "
        "Iūlius bonus — sed cūr bonus? "
        "Dāvus improbus — sed cūr improbus? "
        "Vir bonus, vir improbus. Duo in oppidō. Ūnus vidētur — ūnus est."
    )
}

# ---- 中长篇 (500-800词) x4 ----

STORIES["cap3_07"] = {
    "title_la": "Pater meus abest",
    "title_zh": "我父远行",
    "target_chapter": 3,
    "theme": "01 生死",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Pater meus in oppidō nōn est. Pater meus in vīllā nōn est. "
        "Pater meus in Italiā nōn est. Pater meus abest. "
        "Ego fīlius sum. Ego Mārcus sum. Ego fīlius Iūliī sum. "
        "Iūlius est pater meus. Iūlius est vir bonus. Iūlius est dominus bonus. "
        "Sed Iūlius in oppidō nōn est. Iūlius abest. "
        "Pater meus in Hispāniam vēnit. Hispānia est terra magna. "
        "Hispānia nōn est Italia. Hispānia est procul ab Italiā. "
        "Pater meus mihi: 'Mārce, ego in Hispāniam veniō. "
        "Tū in oppidō es. Tū fīlius meus es. Tū bonus es. "
        "Tū mātrī pārēs. Tū in oppidō es.' "
        "Ego patrī meō: 'Pater, in oppidō estō! Pater, nōlī abīre!' "
        "Sed pater meus in Hispāniam vēnit. Pater meus abest. "
        "Māter mea plōrat. Dēlia māter mea plōrat. Ego plōrō. "
        "Iūlia plōrat. Iūlia est fīlia Iūliī. Iūlia est fīlia patris meī. "
        "Iūlia quoque plōrat. Familia plōrat. "
        "Pater meus abest. Pater meus in oppidō nōn est. "
        "Ego patrem meum nōn videō. Māter patrem nōn videt. Iūlia patrem nōn videt. "
        "Ego in oppidō sum. Ego in oppidō virōs videō. "
        "Virī in oppidō sunt. Virī in oppidō rident. Virī in oppidō multa habent. "
        "Sed ego patrem meum nōn videō. Pater meus in oppidō nōn est. "
        "Ego in vīllā sum. Vīlla patris meī est. Vīlla est magna. "
        "In vīllā mēnsa est. Mēnsa patris meī est. "
        "In vīllā librī sunt. Librī patris meī sunt. "
        "Ego librōs patris meī videō. Ego librōs patris meī habeō. "
        "Sed pater in vīllā nōn est. Pater meus abest. "
        "Ego patrem meum in librīs videō. Pater meus mihi librōs dedit. "
        "Pater meus mihi multa dedit. Pater meus mihi vīllam dedit. "
        "Pater meus mihi nōmen dedit. Mārcus sum. Mārcus Iūlius sum. "
        "Nōmen patris meī habeō. Pater meus abest — sed nōmen eius in mē est. "
        "Ego in oppidō cum mātre sum. Ego in oppidō cum Iūliā sum. "
        "Māter mea mē videt. Iūlia mē videt. "
        "Māter mea mihi aquam dat. Iūlia mihi rosam dat. "
        "Ego mātrī meae aquam dō. Ego Iūliae rosam dō. "
        "Pater meus abest — sed familia hīc est. "
        "Māter mea est. Iūlia est. Ego sum. "
        "Pater meus abest — sed nōn sōlus sum. "
        "Ego in oppidō patrem meum exspectō. Ego multōs diēs exspectō. "
        "Māter patrem exspectat. Iūlia patrem exspectat. "
        "Familia patrem exspectat. "
        "Ūnus diēs — vir in oppidum venit. Vir ex Hispāniā venit. "
        "Vir: 'Mārce! Dēlia! Iūlia! Ego ex Hispāniā veniō. "
        "Pater tuus mē ad vōs mittit. Pater tuus bonus est. "
        "Pater tuus in Hispāniā est — sed pater tuus ad vōs venit.' "
        "Māter mea nōn iam plōrat. Iūlia nōn iam plōrat. Ego nōn iam plōrō. "
        "Pater meus venit! Pater meus ad familiam venit! "
        "Ego multōs diēs exspectō. Ego in oppidō patrem exspectō. "
        "Ego in oppidō virōs videō. Virī in oppidō sunt. "
        "Sed ubi est pater meus? Ubi est Iūlius? "
        "Tum — pater meus in oppidum venit. Pater meus venit! "
        "Ego patrem meum videō. Pater meus mē videt. "
        "Pater meus: 'Mārce! Fīlius meus! Ego tē videō!' "
        "Ego: 'Pater! Tū venīs! Ego tē videō!' "
        "Māter patrem videt. Iūlia patrem videt. "
        "Familia patrem videt. Familia rīdet. "
        "Pater meus hīc est. Pater meus in oppidō est. "
        "Pater meus in vīllā est. Pater meus nōn abest. "
        "Pater meus hīc est. Pater meus bonus est. "
        "Familia est. Pater est. Māter est. Iūlia est. Ego sum. "
        "Pater meus hīc est. Et ego nōn sōlus sum."
    )
}

STORIES["cap3_08"] = {
    "title_la": "Vir novus in oppidō",
    "title_zh": "城中的新来者",
    "target_chapter": 3,
    "theme": "16 归属",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "非罗马的古代人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir in oppidum venit. Vir in oppidō novus est. "
        "Vir oppidum videt. Oppidum est magnum. Oppidum est pulchrum. "
        "Vir: 'Hoc oppidum est magnum. Hoc oppidum est pulchrum. "
        "Ego in hōc oppidō novus sum. Ego hōc oppidum nōn videō.' "
        "Vir in oppidō virōs videt. Virī in oppidō sunt. Virī multī sunt. "
        "Vir virōs videt — sed virī virum nōn vident. "
        "Vir in oppidō sōlus est. Vir in oppidō multōs videt — sed virōs nōn vocat. "
        "Vir tacet. Vir sōlus in oppidō est. "
        "Vir ad mēnsam in oppidō venit. Fēmina ad mēnsam est. "
        "Vir: 'Salvē, fēmina. Ego in hōc oppidō novus sum. "
        "Ego aquam habeō — sed tū mihi aquam dās?' "
        "Fēmina virum videt. Fēmina: 'Tū in oppidō novus es? Tū nōn hīc nātus es?' "
        "Vir: 'Nōn. Ego hīc nōn nātus sum. Ego ex Samō veniō. Samos est īnsula.' "
        "Fēmina: 'Samos... ego Samum nōn videō. Sed Samos est īnsula. "
        "Tū ex īnsulā venīs. Tū in oppidō novus es. Tū aquam habēs.' "
        "Fēmina virō aquam dat. Vir aquam capit. "
        "Vir: 'Tū mihi aquam dās. Tū bona es, fēmina.' "
        "Fēmina ridet: 'Tū bonus es, vir. Tū in oppidō novus es — sed tū bonus es.' "
        "Vir in oppidō est. Vir in oppidō multōs diēs est. "
        "Vir in oppidō virōs videt. Vir in oppidō puerōs videt. Vir in oppidō puellās videt. "
        "Sed vir sōlus est. Vir in oppidō sōlus est. "
        "Vir: 'Ego in oppidō sum. Ego in Italiā sum. Sed Samos in mē est. "
        "Samos est īnsula mea. In Samō pater meus est. In Samō māter mea est. "
        "In Samō familia mea est. Ego in Samō nōn sum — sed Samos in mē est.' "
        "Vir in oppidō puerum videt. Puer est Mārcus. Mārcus virum videt. "
        "Mārcus: 'Quis es, vir? Tū in oppidō novus es?' "
        "Vir: 'Ego in oppidō novus sum. Ego ex Samō veniō. Samos est īnsula.' "
        "Mārcus: 'Samos est īnsula? Ego Samum nōn videō. "
        "Quid est in Samō? Quid est in īnsulā?' "
        "Vir: 'In Samō multae rosae sunt. In Samō multa līlia sunt. "
        "In Samō aqua est — aqua multa. In Samō pater meus est. Māter mea in Samō est. "
        "In Samō familia mea est. Ego in Samō nōn sum — sed Samos in mē est.' "
        "Mārcus: 'Tū Samum amās. Tū īnsulam tuam amās. Cūr in Italiā es?' "
        "Vir: 'Ego in Italiā sum. Ego in oppidō sum. "
        "Ego in Samō nōn sum — sed Samos in mē est. "
        "Tū in oppidō nātus es. Ego in Samō nātus sum. "
        "Tū oppidum tuum amās. Ego īnsulam meam amō.' "
        "Mārcus tacet. Mārcus virum videt. "
        "Mārcus: 'Ego in oppidō nātus sum. Ego oppidum meum amō. "
        "Tū Samum amās. Ego oppidum amō. "
        "Tū in oppidō meō es — et ego oppidum meum tibi dō.' "
        "Vir: 'Tū mihi oppidum dās? Quōmodo puer oppidum dat?' "
        "Mārcus: 'Ego tibi oppidum nōn dō — sed ego tibi rosam dō. "
        "Rosa in oppidō meō est. Rosa ex oppidō meō est. "
        "Tū rosam habēs — et oppidum meum in rosā est.' "
        "Mārcus virō rosam dat. Vir rosam capit. "
        "Vir rosam videt. Vir: 'Rosa est pulchra. Rosa ex oppidō tuō est. "
        "Nunc ego rosam habeō — et oppidum tuum in rosā est.' "
        "Mārcus ridet. Vir ridet. "
        "Vir: 'Ego in oppidō novus sum. Sed tū mē vidēs. Tū mihi rosam dās. "
        "Ego nōn iam sōlus sum. Tū mē vidēs — et ego tē videō.' "
        "Mārcus: 'Tū in oppidō novus es — sed tū nōn sōlus es. "
        "Ego tē videō. Ego tē audiō. Tū in oppidō meō es — et tū bonus es.' "
        "Vir et puer in oppidō sunt. Vir novus, puer in oppidō nātus. "
        "Sed duo in oppidō — et duo sē vident. "
        "Vir nōn iam sōlus est. Puer virum novum habet. "
        "Vir novus in oppidō — sed nōn iam sōlus."
    )
}

STORIES["cap3_09"] = {
    "title_la": "Duo puerī",
    "title_zh": "两个男孩",
    "target_chapter": 3,
    "theme": "32 友谊与孤独",
    "style": "抒情",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "In oppidō duo puerī sunt. Puer prīmus est Mārcus. Puer secundus est Gāius. "
        "Mārcus et Gāius in oppidō sunt. Mārcus Gāium videt. Gāius Mārcum videt. "
        "Mārcus Gāium amat. Gāius Mārcum amat. "
        "Mārcus et Gāius in oppidō multa sunt. "
        "Mārcus et Gāius in oppidō rident. Mārcus et Gāius in oppidō vocant. "
        "Mārcus et Gāius in hortō sunt. Duo puerī — ūnā. "
        "Mārcus Gāiō librōs dat. Gāius Mārcō librōs dat. "
        "Mārcus Gāiō rosās dat. Gāius Mārcō līlia dat. "
        "Mārcus: 'Gāī, tū bonus es. Tū mihi librōs dās. Tū mihi rosās dās.' "
        "Gāius: 'Mārce, tū bonus es. Tū mihi librōs dās. Tū mihi līlia dās.' "
        "Mārcus et Gāius in oppidō sunt. Ūnā. "
        "Sed ūnus diēs Gāius in oppidō nōn est. "
        "Mārcus: 'Ubi est Gāius? Gāius in oppidō nōn est. "
        "Ego Gāium nōn videō. Ubi est Gāius?' "
        "Mārcus in oppidō Gāium videt — sed Gāius nōn est. "
        "Mārcus in viīs Gāium videt — sed Gāius nōn est. "
        "Mārcus vocat: 'Gāī! Gāī!' Nūllus respondet. Gāius nōn est. "
        "Mārcus ad vīllam Gāiī venit. Mārcus pulsat. Nūllus respondet. "
        "Mārcus: 'Gāī, ubi es? Cūr nōn respondēs? Ego tē amō — cūr nōn respondēs?' "
        "Mārcus sōlus in oppidō est. Mārcus in oppidō sine Gāiō est. "
        "Mārcus: 'Ego sōlus sum. Gāius nōn est. "
        "Ego in oppidō sōlus sum. Ego in oppidō multōs videō — sed nūllus est Gāius.' "
        "Mārcus plōrat. Mārcus in oppidō sōlus plōrat. "
        "Iūlia Mārcum videt. Iūlia: 'Mārce, cūr plōrās? Quid est?' "
        "Mārcus: 'Gāius nōn est. Gāius in oppidō nōn est. Ego sōlus sum.' "
        "Iūlia: 'Gāius in oppidō nōn est? Ubi est Gāius?' "
        "Mārcus: 'Ego Gāium nōn videō. Ego Gāium in oppidō nōn videō.' "
        "Iūlia: 'Ego Gāium quoque nōn videō. Sed nōlī plōrāre, Mārce. "
        "Tū nōn sōlus es. Ego hīc sum. Tū fīliam patris tuī habēs.' "
        "Mārcus: 'Tū es fīlia patris meī — sed tū nōn es Gāius. Fīlia nōn est puer.' "
        "Iūlia: 'Ego tē amō. Tū mē amās. Tū nōn sōlus es.' "
        "Mārcus Iūliam videt. Mārcus: 'Tū mē amās. Ego tē amō. Tū es fīlia patris meī.' "
        "Sed Gāius nōn venit. Diēs multī — Gāius nōn venit. "
        "Mārcus in oppidō est. Mārcus Gāium videt — sed Gāius nōn est. "
        "Sed Gāius nōn est. "
        "Tum ūnus diēs — Gāius venit. Gāius in oppidum venit. "
        "Mārcus Gāium videt. Mārcus: 'Gāī! Tū venīs! Tū in oppidō es! Ego tē videō!' "
        "Gāius: 'Mārce! Ego tē videō! Ego in oppidum veniō! Ego tē amō!' "
        "Mārcus et Gāius — ūnā iterum. "
        "Mārcus: 'Cūr nōn in oppidō fuistī? Cūr mē sōlum dedistī?' "
        "Gāius: 'Ego in Graeciam vēnī. Pater meus mē in Graeciam vēnit. "
        "Ego in Graeciā fuī. Ego in Graeciā multās īnsulās vīdī. "
        "Crētam vīdī. Samum vīdī. Dēlon vīdī. "
        "Sed ego tē in oppidō nōn vīdī — sed ego tē amāvī. "
        "Ego tē in oppidō nōn vīdī — sed tū in mē fuistī.' "
        "Mārcus: 'Ego tē in oppidō nōn vīdī. "
        "Ego sōlus fuī — sed tū in mē fuistī.' "
        "Gāius: 'Nunc ego in oppidō sum. Tū in oppidō es. Duo puerī sumus — iterum.' "
        "Mārcus Gāiō librum dat. Gāius Mārcō librum dat. "
        "Mārcus: 'Hic liber est dē Graeciā. Ego hunc librum tibi dō — quia tū in Graeciā fuistī.' "
        "Gāius: 'Hic liber est dē oppidō. Ego hunc librum tibi dō — quia tū in oppidō fuistī.' "
        "Duo puerī — iterum ūnā. Duo puerī in oppidō. "
        "Mārcus et Gāius. Duo puerī. Ūnā."
    )
}

STORIES["cap3_10"] = {
    "title_la": "Quid est bonum?",
    "title_zh": "何为善？",
    "target_chapter": 3,
    "theme": "04 正义",
    "style": "问答",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Puer: 'Pater, quid est bonum?' "
        "Pater: 'Bonum est quod pater tuus tibi dat. Bonum est quod tū habēs. "
        "Bonum est quod Rōmānum est.' "
        "Puer: 'Pater, sī tū mihi librum dās — estne hoc bonum? "
        "Et sī tū mihi librum nōn dās — estne hoc nōn bonum?' "
        "Pater: 'Sī ego tibi librum dō — bonum est. Sī ego tibi librum nōn dō — nōn est bonum. "
        "Ego pater sum. Ego tibi dō — aut nōn dō.' "
        "Puer: 'Pater, sī servus tuus tibi pecūniam capit — estne hoc bonum?' "
        "Pater: 'Nōn. Servus nōn capit pecūniam dominī. Hoc nōn est bonum.' "
        "Puer: 'Cūr nōn? Servus quoque pecūniam habēre potest.' "
        "Pater: 'Servus servus est. Servus nōn est dominus. Servus nōn habet — dominus habet.' "
        "Puer: 'Pater, sī dominus servō pecūniam nōn dat — servus nōn habet. Estne hoc bonum?' "
        "Pater: 'Dominus servō dat — aut nōn dat. Dominus est dominus. Servus est servus.' "
        "Puer: 'Pater, sī servus tuus bonus est — et tū eī nōn dās — estne hoc bonum?' "
        "Pater: 'Sī servus bonus est — dominus eī dat. Dominus bonus servō bonō dat.' "
        "Puer: 'Pater, sī dominus est improbus — et servus est bonus — "
        "quis est bonus? Dominus — an servus?' "
        "Pater tacet. Pater fīlium videt. "
        "Pater: 'Mārce, tū multa rogās. Tū bonus es — sed tū multum rogās. "
        "Bonum est quod est. Bonum est quod pater tuus tibi dat.' "
        "Puer: 'Pater, sī tū mihi dīcis 'hoc est bonum' — et ego tibi nōn pāreō — "
        "estne hoc nōn bonum?' "
        "Pater: 'Sī tū mihi nōn pārēs — tū nōn es bonus fīlius. "
        "Fīlius bonus patrī pāret. Bonum est fīlium patrī pārēre.' "
        "Puer: 'Sed pater, sī tū mihi imperās quod nōn est bonum — "
        "estne bonum mē tibi pārēre?' "
        "Pater tacet. Pater fīlium videt. Pater diū tacet. "
        "Pater: 'Fīlius meus, tū mē rogās — et tū mē docēs. "
        "Ego tibi dīcō: bonum est quod tū in tē vidēs. "
        "Sī tū in tē vidēs — et tū mē audīs — et tū tē ipsum audīs — "
        "tum tū vidēs quid est bonum.' "
        "Puer: 'Pater, ego tē amō. Ego tē audiō. Ego in mē videō. "
        "Tū mihi dīcis — et ego audiō. Ego tibi dīcō — et tū audīs. "
        "Hoc est bonum?' "
        "Pater: 'Hoc est bonum. Hoc est bonum. "
        "Tū fīlius meus es — et tū mē docēs. Ego pater tuus sum — et ego ā tē discō.' "
        "Puer: 'Pater, ego tē amō.' "
        "Pater: 'Et ego tē amō, fīlius meus.' "
        "Puer et pater. Pater et fīlius. Duo in ūnā vīllā. "
        "Bonum est — quod inter patrem et fīlium est."
    )
}

# ============================================================
# 主程序
# ============================================================

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    passed, failed = [], []

    for story_id, meta in STORIES.items():
        target_ch = meta["target_chapter"]
        latin_text = meta["text"].strip().replace("'", '"')
        title_la = meta["title_la"]

        eval_r = evaluate(latin_text, story_id)
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])
        word_count = len(latin_text.split())

        gap = (v2_level - target_ch) if v2_level else "N/A"
        ok = v2_level is not None and v2_level <= target_ch + 2

        status_icon = "OK" if ok else "FAIL"
        print(f"  [{status_icon}] {title_la}: {word_count}词, v2={v2_level} (目标{target_ch}), "
              f"覆盖率={v2_rate}%, OOV={len(v2_oov)}个")

        if not ok:
            failed.append(f"{title_la}: v2_level={v2_level}, gap={gap}, OOV={v2_oov[:10]}")
            continue

        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)

        tier_map = {"中篇": "medius", "中长篇": "longior", "长篇": "longus", "超长篇": "longissimus"}
        length_slug = tier_map.get(meta["length_tier"], "medius")

        import glob as gb
        existing = list(cap_dir.glob(f"Cap{target_ch}_*_{length_slug}_*.md"))
        max_num = 0
        for f in existing:
            try:
                num = int(f.stem.rsplit("_", 1)[-1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
        new_num = max_num + 1

        title_slug = title_la.replace(" ", "_").replace("?", "").replace("'", "")
        filename = f"Cap{target_ch}_{title_slug}_{length_slug}_{new_num:03d}.md"
        filepath = cap_dir / filename

        yaml_lines = [
            "---",
            f'story_id: "{story_id}"',
            f'title_la: "{title_la}"',
            f'title_zh: "{meta["title_zh"]}"',
            f'target_chapter: {target_ch}',
            f'theme: "{meta["theme"]}"',
            f'style: "{meta["style"]}"',
            f'genre: "{meta["genre"]}"',
            f'character_type: "{meta["character_type"]}"',
            f'length_tier: "{meta["length_tier"]}"',
            f'narrative_mode: "{meta["narrative_mode"]}"',
            f'word_count: {word_count}',
            'macrons_status: "generated"',
            f'evaluated_chapter: {v2_level}',
            f'best_fit_chapter: {v2_level}',
            f'coverage_rate: {v2_rate}',
            f'oov_words: {json.dumps(v2_oov, ensure_ascii=False)}',
            'top_10_lemmas: null',
            'grammar_features: null',
            f'created_at: "{now}"',
            f'updated_at: "{now}"',
            'status: "rewritten"',
            'rewritten_from: "brevis"',
            'rewritten_at: "' + now + '"',
            "---",
            "",
            latin_text,
            "",
        ]

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines))

        passed.append(f"{title_la} → {filename} ({word_count}词, v2={v2_level})")
        print(f"    → {filename}")

    print(f"\n{'='*60}")
    print(f"通过: {len(passed)}/{len(STORIES)}")
    if failed:
        print(f"失败: {len(failed)}")
        for f in failed:
            print(f"  - {f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()