#!/usr/bin/env python3
"""rewrite_cap5.py — 重写 Cap.5 的 10 篇短篇为 6 中篇 + 4 中长篇。
严格使用 <=Cap.7 的词元（lemma_chapter_map <= 7）。
策略：~90%安全词 + ~5%OOV(专有名词) + ~5%高章节词(<=Cap.10)。
"""

import json, re, sys, os
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

STORIES = {}

# ============================================================
# 中篇 (300-500词) x6
# ============================================================

STORIES["cap5_01"] = {
    "title_la": "Quī dormit?",
    "title_zh": "谁在睡？",
    "target_chapter": 5,
    "theme": "13 孤独",
    "style": "冷峻",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "In vīllā pater et fīlius sunt. Pater oculōs claudit. Pater fessus est. "
        "Fīlius patrem spectat. Fīlius: 'Pater, cūr oculōs claudis?' "
        "Pater oculōs aperit. Pater: 'Fīlī, oculōs claudō quod fessus sum. "
        "Ego dormīre eō.' "
        "Fīlius: 'Quid est dormīre, pater?' "
        "Pater: 'Dormīre est oculōs claudere. Dormīre est bonum. "
        "Post dormīre, ego nōn iam fessus sum.' "
        "Fīlius: 'Sed pater, ego nōn fessus sum. Cūr tū fessus es?' "
        "Pater: 'Fīlī, ego multa agō. Ego in hortō ambulō. Ego aquam portō. "
        "Ego multōs virōs videō. Post multa, ego fessus sum.' "
        "Māter ad eōs venit. Māter fīlium videt. Māter patrem videt. "
        "Māter: 'Pater tuus fessus est. Pater tuus dormit. "
        "Tū quoque dormīre... tū quoque dormīs.' "
        "Fīlius: 'Sed ego nōn fessus sum! Ego dormīre nōn... ego nōn dormiō!' "
        "Māter: 'Fīlī, multī dormiunt. Puerī parvī dormiunt. "
        "Puellae parvae dormiunt. Etiam magnī virī dormiunt.' "
        "Fīlius: 'Cūr dormīmus, māter?' "
        "Māter: 'Dormīmus quod multī fessī sunt. "
        "Oculī sē claudunt. Et post dormīre, laetī sumus.' "
        "Fīlius: 'Sed quandō dormiō, ubi sum ego?' "
        "Pater oculōs aperit. Pater: 'Tū es hīc, fīlī. Tū es in vīllā. "
        "Tū es prope mē. Tū es prope mātrem. Tū nōn sōlus es.' "
        "Fīlius: 'Ego nōn sōlus sum quandō dormiō?' "
        "Māter: 'Nōn, fīlī. Quandō tū dormīs, ego tē videō. "
        "Pater tē videt. Tū es in corde meō.' "
        "Fīlius: 'Quid est in corde, māter?' "
        "Māter: 'In corde sunt quī tē amant. In corde sunt quī tē vident. "
        "In corde sunt pater et māter et fīlius.' "
        "Fīlius tacet. Fīlius mātrem spectat. Fīlius patrem spectat. "
        "Fīlius: 'Pater, māter, ego fessus sum. Ego dormīre eō.' "
        "Pater fīlium spectat. Pater: 'Venī, fīlī. Dormī prope mē.' "
        "Fīlius prope patrem est. Fīlius oculōs claudit. "
        "Pater fīlium spectat. Māter fīlium spectat. "
        "Pater: 'Bonus puer es. Dormī, fīlī.' "
        "Māter: 'Dormī, fīlī. Pater et māter tē vident.' "
        "Fīlius dormit. Pater fīlium spectat. Māter fīlium spectat. "
        "Pater: 'Fīlius dormit. Fīlius bonus est.' "
        "Māter: 'Ita. Fīlius dormit — et in cordibus est.' "
        "Pater quoque oculōs claudit. Māter quoque oculōs claudit. "
        "In vīllā, pater et māter et fīlius dormiunt. "
        "Trēs in vīllā — et trēs in cordibus sunt."
    )
}

STORIES["cap5_02"] = {
    "title_la": "Via ad oppidum",
    "title_zh": "通往城镇的路",
    "target_chapter": 5,
    "theme": "42 城市与乡村",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir in viā est. Vir est Lūcius. Lūcius ad oppidum ambulat. "
        "Via est longa. Via est pulchra. Lūcius sōlus in viā est. "
        "Lūcius multa videt. Lūcius multa audit. "
        "Lūcius ad dextram spectat. Ad dextram multī hortī sunt. "
        "In hortīs multae rosae sunt. In hortīs multa līlia sunt. "
        "Rosae sunt pulchrae. Līlia sunt pulchra. "
        "Lūcius ad sinistram spectat. Ad sinistram aqua est. "
        "Aqua est parva. Aqua est via aquae. "
        "Aqua cantat. Aqua dīcit: 'Venī, venī ad mē.' "
        "Lūcius aquam audit. Lūcius aquam spectat. "
        "Lūcius: 'Aqua est pulchra. Aqua cantat. Ego aquam libenter audiō.' "
        "Lūcius in viā ambulat. Via nōn est vacua. "
        "Alius vir in viā est. Vir est Gāius. "
        "Gāius ad Lūcium venit. Gāius: 'Salvē! Quō vādis?' "
        "Lūcius: 'Salvē! Ego ad oppidum eō. Et tū?' "
        "Gāius: 'Ego quoque ad oppidum eō. Via est longa. "
        "Duo virī in viā — melius est quam ūnus.' "
        "Lūcius et Gāius in viā ambulant. "
        "Lūcius: 'Unde venīs, Gāī?' "
        "Gāius: 'Ex vīllā meā veniō. Vīlla mea est prope aquam. "
        "Vīlla mea est parva — sed pulchra.' "
        "Lūcius: 'Quid in oppidō agis?' "
        "Gāius: 'Ego ad oppidum eō quod multōs virōs vidēre volō. "
        "In oppidō multa videō. In oppidō multa audiō. "
        "Oppidum est plēnum vītae.' "
        "Lūcius et Gāius prope oppidum sunt. "
        "Lūcius: 'Ecce! Oppidum videō! Portās oppidī videō!' "
        "Gāius: 'Ita! Portae sunt magnae. Portae sunt pulchrae. "
        "Post portās — oppidum est.' "
        "Lūcius et Gāius ad portās veniunt. "
        "In portīs multī virī sunt. Multae fēminae sunt. "
        "Multī puerī sunt. Multae puellae sunt. "
        "Lūcius: 'Oppidum est magnum! Oppidum est plēnum!' "
        "Gāius: 'Oppidum est magnum — et pulchrum. "
        "In oppidō multae viae sunt. In oppidō multae vīllae sunt. "
        "In oppidō multae familiae sunt.' "
        "Lūcius in oppidum intrat. Gāius in oppidum intrat. "
        "Lūcius: 'Grātiās, Gāī. Via fuit longa — sed cum amīcō, via est bona.' "
        "Gāius: 'Grātiās, Lūcī. Via fuit longa — sed duo virī viam fēcērunt.' "
        "Lūcius: 'Valē, Gāī!' "
        "Gāius: 'Valē, Lūcī!' "
        "Lūcius in oppidō est. Oppidum est magnum. Oppidum est pulchrum. "
        "Via fuit longa — sed oppidum est bonum. "
        "Et Lūcius laetus est."
    )
}

STORIES["cap5_03"] = {
    "title_la": "In hortō",
    "title_zh": "在花园中",
    "target_chapter": 5,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in hortō sum. Hortus meus est parvus — sed hortus meus est pulcher. "
        "Ego in hortō ambulō. Ego multa videō. Ego multa audiō. "
        "In hortō meō rosae sunt. Rosae sunt pulchrae. Rosae sunt multae. "
        "Rosae sunt magnae. Rosae sunt parvae. Rosae sunt pulchrae. "
        "Ego rosās spectō. Ego rosās videō. Ego rosās numerō: "
        "ūna rosa, duae rosae, trēs rosae, quattuor rosae, multae rosae! "
        "Ego rosās amō — sed rosae mē nōn amant. Rosae sunt rosae. "
        "Līlia in hortō meō sunt. Līlia sunt pulchra. Līlia sunt multa. "
        "Līlia sunt parva — sed pulchra. Ego līlia spectō. Ego līlia videō. "
        "Ego līlia numerō: ūnum līlium, duo līlia, tria līlia, multa līlia! "
        "Rosae et līlia in hortō meō sunt. Rosae sunt pulchrae, līlia sunt pulchra. "
        "Aqua in hortō meō est. Aqua est parva. Aqua est via. "
        "Aqua cantat. Aqua cantat. Aqua cantat. Ego aquam audiō. "
        "Ego aquam spectō. Ego ad aquam veniō. Aqua est bona. Aqua est nova. "
        "In aquā ego mē videō. Ego in aquā sum. "
        "Ego in aquā faciem videō — faciēs mea in aquā est. "
        "Ego in aquā oculōs videō — oculī meī in aquā sunt. "
        "Ego in aquā nāsum videō — nāsus meus in aquā est. "
        "Ego in aquā ōs videō — ōs meum in aquā est. "
        "Ego sum in aquā. Ego in aquā mē videō — et ego sum. "
        "Rosae in aquā sunt. Līlia in aquā sunt. Hortus in aquā est. "
        "Ego aquam manibus capiō. Aqua est bona. Aqua est nova. "
        "Ego aquam in manibus habeō. Aqua in manibus meīs est. "
        "In hortō meō multa sunt. Rosae sunt pulchrae. "
        "Līlia sunt pulchra. Aqua est pulchra. "
        "Ego in hortō ambulō. Ego rosās videō. Ego līlia videō. "
        "Ego aquam videō. Ego aquam audiō. "
        "Ego oculōs claudō. Ego aquam audiō. "
        "Aqua cantat. Aqua cantat et cantat. "
        "Ego in hortō meō laetus sum. Ego in hortō meō sōlus sum. "
        "Sed nōn sōlus. Rosae hīc sunt. Līlia hīc sunt. Aqua hīc est. "
        "Hortus meus est parvus — sed hortus meus est magnum bonum. "
        "In hortō meō ego multa videō. In hortō meō ego multa audiō. "
        "Hortus est bonus. Hortus est pulcher. "
        "Ego in hortō sum — et hortus in mē est. "
        "Ego in hortō ambulō. Ego in hortō sum. "
        "Cum in hortō sum, ego laetus sum. "
        "Hortus meus est parvus — sed in hortō parvō multa sunt. "
        "Rosae, līlia, aqua — et ego. Ego in hortō sum. Hortus in mē est."
    )
}

STORIES["cap5_04"] = {
    "title_la": "Māter et fīlia in hortō",
    "title_zh": "母女在花园",
    "target_chapter": 5,
    "theme": "30 威严与慈爱",
    "style": "古典",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Māter et fīlia in hortō sunt. Māter est Cornēlia. Fīlia est Iūlia. "
        "Hortus est magnus. Hortus est pulcher. "
        "In hortō multae rosae sunt. In hortō multa līlia sunt. "
        "Cornēlia rosās spectat. Iūlia līlia spectat. "
        "Cornēlia: 'Iūlia, venī. Ecce rosae. Rosae sunt pulchrae.' "
        "Iūlia ad mātrem venit. Iūlia rosās spectat. "
        "Iūlia: 'Māter, rosae sunt pulchrae. Ego rosās videō — et laeta sum.' "
        "Cornēlia: 'Fīlia mea, rosae sunt pulchrae. "
        "Et tū es pulchra — et tū es pulchra, ut rosae pulchrae sunt.' "
        "Iūlia: 'Māter, tū mihi rosās dās. Tū mihi hortum dās. "
        "Tū mihi multa bona dās.' "
        "Cornēlia fīliam spectat. Cornēlia: 'Fīlia mea, tū es rosa mea. "
        "Tū es līlium meum. Tū es pulchra — et ego tē videō.' "
        "Iūlia: 'Māter, tū mihi rosās dās. Ego rosās habeō. "
        "Ego rosās in hortō meō pōnam.' "
        "Cornēlia: 'Ita, fīlia mea. Rosae sunt tuae. "
        "Hortus est tuus. Ego rosās dō — quod tū es fīlia mea.' "
        "Iūlia: 'Māter, rosae sunt pulchrae. Ego rosās videō. "
        "Et ego mātrem meam videō. Et ego laeta sum.' "
        "Cornēlia: 'Fīlia mea, ego quoque tē videō. Ego quoque laeta sum. "
        "Māter laeta est quandō fīlia laeta est.' "
        "Iūlia ad rosās venit. Iūlia rosās spectat. "
        "Iūlia: 'Māter, hae rosae sunt pulchrae. Hae rosae sunt tuae.' "
        "Cornēlia: 'Nōn, fīlia mea. Hae rosae sunt tuae. "
        "Multae rosae in hōc hortō sunt tuae.' "
        "Iūlia: 'Māter, cūr mihi multās rosās dās?' "
        "Cornēlia: 'Quod tū es fīlia mea. Quod tū es bona. "
        "Quod tū es magnum bonum in vītā... in corde meō.' "
        "Iūlia mātrem spectat. Iūlia: 'Māter, tū es māter bona. "
        "Ego tē videō. Ego tē audiō. Ego laeta sum.' "
        "Cornēlia fīliam spectat. Cornēlia: 'Fīlia mea, tū es fīlia bona. "
        "Ego tē videō. Ego tē audiō. Ego laeta sum.' "
        "Māter et fīlia in hortō ambulant. "
        "Māter fīliae rosās dat. Fīlia mātrī lacrimās laetās dat. "
        "Māter et fīlia — duae in hortō. "
        "Rosae sunt pulchrae. Līlia sunt pulchra. "
        "Et māter et fīlia sunt pulchrae."
    )
}

STORIES["cap5_05"] = {
    "title_la": "Fēmina sōla",
    "title_zh": "独处的女人",
    "target_chapter": 5,
    "theme": "13 孤独",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in vīllā sōla sum. Vir meus nōn est. Fīlius meus nōn est. "
        "Vīlla est vacua. Vīlla est quiēta. Ego sōla in vīllā sum. "
        "Ego ad fenestram eō. Ego per fenestram spectō. "
        "In viā multī virī sunt. In viā multae fēminae sunt. "
        "Sed vir meus nōn est in viā. Fīlius meus nōn est in viā. "
        "Ego virum meum exspectō. Ego fīlium meum exspectō. "
        "Vir meus est bonus. Vir meus est Lūcius. Lūcius mē curat. "
        "Lūcius mē amat. Ego quoque Lūcium... Ego laeta sum cum Lūciō. "
        "Fīlius meus est parvus. Fīlius meus est Mārcus. Mārcus est puer bonus. "
        "Mārcus mē amat. Ego quoque Mārcum... Ego laeta sum cum Mārcō. "
        "Ubi sunt vir meus et fīlius meus? "
        "Lūcius in oppidō est. Lūcius multa agit. Lūcius multōs virōs videt. "
        "Lūcius ad vīllam reveniet. Mārcus in hortō est. Mārcus cum puerīs ludit. "
        "Mārcus ad vīllam reveniet. "
        "Ego in vīllā sōla sum — sed ego nōn sum sōla in corde. "
        "In corde meō, Lūcius est. In corde meō, Mārcus est. "
        "Ego multa cōgitō. Ego cōgitō dē Lūciō. Ego cōgitō dē Mārcō. "
        "Ego cōgitō dē vīllā. Ego cōgitō dē hortō. Ego cōgitō dē multīs rēbus. "
        "Ego in hortum eō. Hortus meus est pulcher. "
        "In hortō rosae sunt. In hortō līlia sunt. "
        "Rosae sunt pulchrae — sed rosae Lūcium nōn vident. "
        "Līlia sunt pulchra — sed līlia Mārcum nōn audiunt. "
        "Ego rosīs aquam dō. Ego līliīs aquam dō. "
        "Rosae aquam habent. Līlia aquam habent. "
        "Ego quoque aquam volō — sed aqua cordis nōn est in hortō. "
        "Aqua cordis est familia. "
        "Post, ego Lūcium videō! Lūcius ad vīllam venit! "
        "Lūcius: 'Salvē, mea fēmina! Ego ad tē veniō!' "
        "Ego: 'Salvē, Lūcī! Ego tē exspectō. Ego tē videō. Ego laeta sum!' "
        "Lūcius mē videt. Lūcius mē amat. Ego Lūcium... Ego laeta sum. "
        "Post, Mārcus ad vīllam venit! "
        "Mārcus: 'Māter! Ego in hortō fuī! Ego cum puerīs lūsī!' "
        "Ego: 'Mārce! Fīlī mī! Ego tē videō. Ego laeta sum!' "
        "Iam vīlla nōn est vacua. Iam vīlla nōn est quiēta. "
        "Lūcius in vīllā est. Mārcus in vīllā est. Ego in vīllā sum. "
        "Familia in vīllā est. Et familia est omnia. "
        "Ego nōn iam sōla sum. Ego familiam habeō. "
        "Et ubi familia est — ibi bonum est."
    )
}

STORIES["cap5_06"] = {
    "title_la": "Fīlius discit",
    "title_zh": "儿子在学习",
    "target_chapter": 5,
    "theme": "28 教育",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pater et fīlius in vīllā sunt. Pater est Iūlius. Fīlius est parvus. "
        "Fīlius in hortō cum patre est. Fīlius multa discit. "
        "Iūlius fīlium spectat. Iūlius: 'Fīlī, tū hodiē multa discēs. "
        "Ego tē multa docēbō.' "
        "Fīlius: 'Pater, quid discam?' "
        "Iūlius: 'Tū discēs dē hortō. Tū discēs dē rosīs. Tū discēs dē aquā.' "
        "Iūlius et fīlius in hortum veniunt. "
        "Iūlius: 'Fīlī, ecce rosae. Rosae sunt pulchrae. "
        "Cūr rosae sunt pulchrae? Rosae sunt pulchrae quod rosae in hortō sunt. "
        "Quod rosae aquam habent. Quod rosae in hortō bonō sunt.' "
        "Fīlius rosās spectat. Fīlius rosās bene videt. "
        "Fīlius: 'Pater, rosae sunt pulchrae. Ego rosās videō — et ego laetus sum.' "
        "Iūlius: 'Fīlī, rosae sunt pulchrae. "
        "Rosae tibi respondent: «Pulchrae sumus. Bonae sumus. "
        "Nōs in hortō sumus — et hortus est pulcher.»' "
        "Fīlius līlia spectat. Fīlius: 'Pater, quid respondent līlia?' "
        "Iūlius: 'Līlia respondent: «Alba sumus. Bona sumus. "
        "Nōs in hortō sumus — et hortus est pulcher.»' "
        "Iūlius et fīlius ad aquam veniunt. "
        "Iūlius: 'Fīlī, ecce aqua. Aqua in hortō est. Aqua cantat. "
        "Aqua est bona hortī.' "
        "Fīlius aquam spectat. Fīlius aquam audit. "
        "Fīlius: 'Pater, aqua cantat. Ego aquam audiō. "
        "Aqua respondet: «Venī, venī ad mē.» Ego ad aquam veniō.' "
        "Iūlius fīliō aquam dat. Fīlius aquam manibus capit. "
        "Fīlius: 'Aqua est bona! Aqua est bona hortī! "
        "Aqua est bona rosārum! Aqua est bona līliōrum!' "
        "Iūlius: 'Bene, fīlī. Aqua est bona. Aqua est bona hortī. "
        "Aqua est bona rosārum. Aqua est bona līliōrum. "
        "Et aqua est bona nostra. Nōs aquam habēmus — et nōs laetī sumus.' "
        "Fīlius: 'Pater, hodiē ego multa didicī. Ego didicī dē rosīs. "
        "Ego didicī dē līliīs. Ego didicī dē aquā. "
        "Ego didicī quod hortus est bonus.' "
        "Iūlius: 'Fīlī, tū es puer bonus. Tū vidēs. Tū audīs. Tū discis. "
        "Hortus est bonus — et tū in hortō discis. "
        "Puer bonus videt. Puer bonus audit. Puer bonus discit.' "
        "Fīlius: 'Pater, ego multa discere volō. Ego multa vidēre volō. "
        "Ego multa audīre volō.' "
        "Iūlius: 'Fīlī, tū multa discēs. Nam quī videt — discit. "
        "Quī audit — discit. Quī rogat — discit. "
        "Tū vidēs. Tū audīs. Tū rogās. Tū discēs multa.' "
        "Pater et fīlius in hortō sunt. "
        "Pater et fīlius rosās spectant. Pater et fīlius aquam audiunt. "
        "Fīlius: 'Pater, hortus est pulcher. Et ego laetus sum quod hodiē didicī.' "
        "Iūlius: 'Fīlī, ego quoque laetus sum. Nam pater laetus est quandō fīlius discit.' "
        "Pater et fīlius ad vīllam veniunt. "
        "Fīlius multa didicit. Et fīlius laetus est."
    )
}

# ============================================================
# 中长篇 (500-800词) x4
# ============================================================

STORIES["cap5_07"] = {
    "title_la": "Ancilla et domina",
    "title_zh": "女奴与女主人",
    "target_chapter": 5,
    "theme": "03 自由与束缚",
    "style": "冷峻",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Syra est ancilla. Syra in vīllā magnā est. "
        "Syra dominae pāret. Domina est Dēlia. Dēlia est domina magna. "
        "Dēlia multam pecūniam habet. Dēlia multōs servōs habet. "
        "Syra est ancilla Dēliae. Syra in vīllā multa agit. "
        "Syra aquam portat. Syra hortum videt. Syra multa agit. "
        "Syra est ancilla bona. Syra dominae pāret. "
        "Sed Syra nōn est laeta. Syra lībera esse vult. "
        "Syra multa cōgitat. Syra: 'Cūr ego ancilla sum? Cūr Dēlia domina est? "
        "Num Dēlia melior mē est? Num ego peior Dēliā sum?' "
        "Dēlia Syram vocat. Dēlia: 'Syra, venī! Aquam portā!' "
        "Syra venit. Syra aquam portat. Syra: 'Domina, ecce aqua.' "
        "Dēlia: 'Syra, tū es ancilla bona. Tū mihi pārēs. Tū multa agis.' "
        "Syra: 'Domina, ego ancilla sum. Ego tibi pāreō. Sed cūr ego ancilla sum?' "
        "Dēlia Syram spectat. Dēlia: 'Tū ancilla es quod ita est. "
        "Ego domina sum quod ita est. Nōnne ita est bonum?' "
        "Syra: 'Domina, estne bonum? Tū es lībera. Ego nōn sum lībera. "
        "Tū habēs multa. Ego nōn habeō multa. "
        "Tū in hortō ambulāre potes. Ego in hortō ambulō quandō tū sinis.' "
        "Dēlia tacet. Dēlia Syram spectat. "
        "Dēlia: 'Syra, tū bene loqueris. Ego nōn multa cōgitāvī dē hōc.' "
        "Syra: 'Domina, tū nōn cōgitāvistī quod tū es domina. "
        "Dominī nōn cōgitant dē servīs. Servī sunt — servī sunt.' "
        "Dēlia ad fenestram ambulat. Dēlia hortum spectat. "
        "Dēlia: 'Syra, tū hortum vidēs. Tū rosās vidēs. Tū līlia vidēs. "
        "Hortus meus est pulcher — quod tū eum vidēs. "
        "Tū mihi multa dās, Syra. Ego tibi nōn multa dō.' "
        "Syra: 'Domina, tū mihi aquam dās. Tū mihi tēctum dās. "
        "Sed tū mihi lībertātem nōn dās.' "
        "Dēlia: 'Syra, quid est lībertās? "
        "Lībertās est quod in corde est — nōn in corpore. "
        "Tū potes lībera esse in corde — etiam sī ancilla es.' "
        "Syra: 'Domina, verba tua sunt pulchra. Sed ego lībera in corpore esse volō. "
        "Ego ex hāc vīllā exīre volō. Ego meam vītam habēre volō.' "
        "Dēlia Syram spectat. "
        "Dēlia: 'Syra, tū es ancilla — sed tū quoque es fēmina. "
        "Tū quoque es homō. Tū quoque es... amīca.' "
        "Syra: 'Domina, tū mē amīcam vocās?' "
        "Dēlia: 'Ita, Syra. Tū mihi multa dās. Tū mē bene vidēs. "
        "Tū mē audīs quandō ego sōla sum. "
        "Tū mē vidēs quandō ego sōla sum. "
        "Tū nōn es sōlum ancilla — tū es amīca.' "
        "Syra: 'Domina, haec verba sunt bona. Sed ego lībertātem volō.' "
        "Dēlia: 'Syra, ego tibi lībertātem dō. "
        "Tū nōn iam ancilla es. Tū lībera es. "
        "Tū potes exīre. Tū potes quod tū vīs.' "
        "Syra nōn verbīs respondet. Syra lacrimās habet. "
        "Syra: 'Domina, tū mihi lībertātem dās. Ego tē bene videō. "
        "Ego tē amīcam meam vocō. "
        "Ego in hāc vīllā esse volō — nōn ut ancilla, sed ut amīca.' "
        "Dēlia: 'Syra, tū es amīca mea. Tū nōn iam ancilla es. "
        "Tū es fēmina lībera. Et amīca lībera est.' "
        "Syra et Dēlia in hortō ambulant. "
        "Syra rosās spectat. Dēlia līlia spectat. "
        "Syra: 'Rosae sunt pulchrae. Et ego rosās videō — "
        "nōn ut ancilla, sed ut lībera.' "
        "Dēlia: 'Syra, ancilla et domina — duae sumus. "
        "Sed in corde — duae fēminae sumus. Duae amīcae sumus.' "
        "Syra: 'Dēlia, amīca mea, tū mihi lībertātem dedistī. "
        "Et ego tibi bonum cordis dō.' "
        "Duae fēminae in hortō sunt. "
        "Ūna fuit domina. Ūna fuit ancilla. "
        "Iam — duae amīcae sunt. "
        "Et hortus est pulcher — nam in hortō duae amīcae sunt."
    )
}

STORIES["cap5_08"] = {
    "title_la": "Vīlla Rōmāna",
    "title_zh": "罗马庄园",
    "target_chapter": 5,
    "theme": "42 城市与乡村",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vīlla Rōmāna in campō est. Vīlla est magna. Vīlla est pulchra. "
        "Vīlla est Iūliī. Iūlius est dominus vīllae. "
        "Iūlius multam pecūniam habet. Iūlius multōs servōs habet. "
        "Vīlla Iūliī multa habet. "
        "Prīmum est ātrium. Ātrium est magnum. Ātrium est pulchrum. "
        "In ātriō impluvium est. Impluvium aquam habet. "
        "Aqua in impluvium venit. Aqua est bona. "
        "In ātriō Iūlius amīcōs videt. In ātriō Iūlius cum amīcīs est. "
        "Ātrium est cor vīllae. "
        "Secundum est hortus. Hortus est magnus. Hortus est pulcher. "
        "In hortō multae rosae sunt. In hortō multa līlia sunt. "
        "In hortō aqua est. Aqua in hortō cantat. "
        "Aemilia in hortō ambulat. Aemilia est uxor Iūliī. "
        "Aemilia rosās videt. Aemilia līlia videt. "
        "Aemilia hortum amat. Hortus Aemiliae est pulcher. "
        "Aemilia in hortō cum amīcīs est. Aemilia cum amīcīs rīdet. "
        "Aemilia amīcīs rosās dat. Amīcae Aemiliae laetae sunt. "
        "Tertium est cubiculum. Cubiculum est magnum. "
        "In cubiculō Iūlius et Aemilia sunt. "
        "In cubiculō fenestrae sunt. Fenestrae sunt magnae. "
        "Per fenestrās hortus vidētur. Per fenestrās rosae videntur. "
        "Per fenestrās līlia videntur. Per fenestrās multa videntur. "
        "Quārtum est cubiculum parvum. In cubiculō parvō fīlius est. "
        "Fīlius est parvus. Fīlius in cubiculō suō est. "
        "Fīlius in cubiculō suō bonus est. Fīlius in cubiculō suō quiētus est. "
        "Quīntum est cubiculum fīliae. Fīlia in cubiculō suō est. "
        "Fīlia in cubiculō suō est. Fīlia est parva. "
        "Fīlia in cubiculō suō bona est. "
        "Sextum est hortus magnus. Hortus magnus post vīllam est. "
        "Hortus magnus est multō maiōr quam hortus prīmus. "
        "In hortō magnō multae rosae sunt. In hortō magnō multa līlia sunt. "
        "In hortō magnō etiam aqua est. Aqua est magna. "
        "Iūlius et Aemilia in aquā sunt. Aqua est bona. "
        "Fīlius in hortō magnō ambulat. "
        "Fīlius cum puerīs ambulat. Fīlius cum puellīs ambulat. "
        "Fīlius laetus est. Puerī laetī sunt. Puellae laetae sunt. "
        "Fīlius: 'Hortus est magnus! Hortus est pulcher! "
        "Ego in hortō cum amīcīs sum. Ego laetus sum!' "
        "Fīlia in hortō magnō est. "
        "Fīlia cum puellīs ambulat. Fīlia rosās spectat. Fīlia līlia spectat. "
        "Fīlia: 'Rosae sunt pulchrae. Līlia sunt pulchra. Hortus est pulcher. "
        "Ego in hortō laeta sum. Ego rosās amō.' "
        "Iūlius in hortō magnō ambulat. Iūlius vīllam suam spectat. "
        "Iūlius: 'Vīlla mea est magna. Vīlla mea est pulchra. "
        "Sed vīlla nōn est sōlum magnum aedificium. "
        "Vīlla est domus. Vīlla est familia. "
        "Sine familiā, vīlla est vacua. Cum familiā, vīlla est plēna.' "
        "Aemilia ad Iūlium venit. Aemilia: 'Iūlī, vīlla tua est pulchra. "
        "Sed tū es bonus dominus. Tū servōs bene vidēs. Tū familiam bene vidēs. "
        "Tū vīllam bonam facis.' "
        "Iūlius: 'Aemilia, vīlla est bona quod tū in eā es. "
        "Tū es cor vīllae. Tū es domina vīllae. "
        "Sine tē, vīlla nōn esset domus.' "
        "Vesperī est. In vīllā omnēs quiētī sunt. "
        "Iūlius et Aemilia in hortō sunt. "
        "Fīlius et fīlia in hortō sunt. Puerī et puellae in hortō sunt. "
        "Servī in vīllā quiētī sunt. Ancillae in vīllā quiētae sunt. "
        "Vīlla est plēna. Vīlla est plēna bonī. "
        "Vīlla Rōmāna est magna. Vīlla Rōmāna est pulchra. "
        "Sed vīlla Rōmāna est domus — et domus est ubi familia est. "
        "Et familia est magnum bonum. "
        "Iūlius vīllam suam spectat. Iūlius familiam suam spectat. "
        "Iūlius: 'Vīlla est bona. Familia est bona. Ego sum laetus.' "
        "Et in vīllā omnēs laetī sunt."
    )
}

STORIES["cap5_09"] = {
    "title_la": "Servus et rosa",
    "title_zh": "奴隶与玫瑰",
    "target_chapter": 5,
    "theme": "04 正义",
    "style": "冷峻",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "旁观者视角",
    "text": (
        "Servus in vīllā est. Servus est Dāvus. Dāvus est servus bonus. "
        "Dāvus dominō pāret. Dominus est Philō. Philō est dominus malus. "
        "Philō multōs servōs habet. Philō servīs imperat. "
        "Philō nōn est bonus dominus. Philō servōs nōn bene videt. "
        "Dāvus in hortō multa agit. "
        "Dāvus aquam portat. Dāvus rosās videt. Dāvus līlia videt. "
        "Dāvus hortum pulchrum facit. "
        "In hortō ūna rosa est pulchra. Rosa est magna. "
        "Rosa est bona. Dāvus hanc rosam bene videt. "
        "Dāvus huic rosae aquam dat. Dāvus hanc rosam spectat. "
        "Dāvus: 'Ō rosa, tū es pulchra. Tū es mihi bona. "
        "Tū es bona hortī. Ego tē bene videō.' "
        "Dāvus rosam amat. Rosa est bonum in corde Dāvī. "
        "Philō in hortum venit. Philō hortum spectat. "
        "Philō: 'Hortus est pulcher. Quis hortum videt?' "
        "Dāvus: 'Ego, domine. Ego hortum videō.' "
        "Philō rosam pulchram videt. Philō: 'Haec rosa est pulchra! "
        "Haec rosa est bona hortī. Ego hanc rosam volō!' "
        "Dāvus: 'Domine, haec rosa est... haec rosa est...' "
        "Philō: 'Haec rosa est mea! Ego sum dominus! Multa in hōc hortō mea sunt. "
        "Tū es servus meus. Tū nōn habēs rosam. Ego habeō rosam.' "
        "Philō rosam capit. Philō rosam ex hortō portat. "
        "Dāvus rosam suam abīre videt. Dāvus lacrimās habet. "
        "Dāvus: 'Rosa mea... rosa mea abiit.' "
        "Philō rosam in vīllā pōnit. Rosa in vīllā est — "
        "sed rosa in vīllā nōn est laeta. "
        "Rosa in vīllā nōn est pulchra. "
        "Post paucōs diēs, rosa nōn iam pulchra est. "
        "Rosa nōn iam pulchra est. "
        "Philō rosam nōn iam pulchram videt. Philō: 'Cūr rosa nōn iam pulchra est? "
        "Ego rosae aquam dedī! Ego rosam in bonō locō posuī!' "
        "Dāvus: 'Domine, rosa nōn iam pulchra est quod rosa in hortō esse volēbat. "
        "Rosa in hortō nāta est. Rosa in hortō laeta erat. "
        "Tū rosam ex hortō cēpistī — et rosa nōn iam pulchra est.' "
        "Philō Dāvum spectat. Philō: 'Tū putās quod ego rosam malē ēgī?' "
        "Dāvus: 'Domine, tū rosam ex hortō cēpistī. "
        "Rosa nōn erat tua — rosa erat hortī. "
        "Tū rosam cēpistī — et rosa nōn iam pulchra est.' "
        "Philō tacet. Philō rosam nōn iam pulchram spectat. "
        "Philō: 'Dāve, tū hanc rosam bene vidēbās. Tū hanc rosam amāvistī. "
        "Ego hanc rosam tibi cēpī. Ego nōn bene ēgī.' "
        "Dāvus: 'Domine, rosa nōn est mea. Rosa nōn est tua. "
        "Rosa est rosae. Rosa est hortī.' "
        "Philō: 'Dāve, tū mē bene facis. Ego rosam cēpī — et ego rosam nōn iam habeō. "
        "Ego iam videō: pulchrum nōn potest capī. "
        "Pulchrum est videndum — nōn capiendum.' "
        "Philō Dāvum spectat. Philō: 'Dāve, tū es servus — sed tū habēs cor magnum. "
        "Tū hortum vidēs. Tū rosās vidēs. "
        "Ego tē bene videō.' "
        "Dāvus: 'Domine, servus sum. Ego hortum videō. Ego rosās videō. "
        "Ego nōn multa habeō — sed ego rosās videō. Et rosae sunt pulchrae.' "
        "Philō: 'Dāve, tū nōn nihil habēs. Tū habēs cor. Tū habēs oculōs. "
        "Tū habēs manūs. Tū habēs multa. "
        "Et ego tibi novam rosam dō — nōn ut capiās, sed ut videās.' "
        "Philō Dāvō novam rosam dat. Rosa est parva — sed rosa est pulchra. "
        "Dāvus rosam capit. Dāvus rosam in hortō pōnit. "
        "Dāvus rosae aquam dat. Dāvus rosam bene videt. "
        "Rosa est pulchra. Dāvus rosam spectat. Dāvus laetus est. "
        "Philō Dāvum spectat. Philō quoque laetus est. "
        "Philō: 'Dāve, iam ego videō. Rosa nōn est mea. Rosa nōn est tua. "
        "Rosa est rosae. Et pulchrum est multōrum.' "
        "Dāvus: 'Domine, ita est. Pulchrum est multōrum — "
        "et pulchrum est in oculīs.' "
        "Servus et dominus in hortō sunt. "
        "Rosa in hortō est. Rosa est pulchra. "
        "Et rosa est laeta — nam rosa in hortō suō est."
    )
}

STORIES["cap5_10"] = {
    "title_la": "Pater et fīlius in hortō",
    "title_zh": "父子在花园",
    "target_chapter": 5,
    "theme": "30 威严与慈爱",
    "style": "古典",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Pater et fīlius in hortō sunt. Pater est Iūlius. Fīlius est parvus. "
        "Hortus est magnus. Hortus est pulcher. "
        "Avēs cantant. Aqua in hortō cantat. "
        "Iūlius: 'Fīlī, venī. Hodiē in hortō ambulāre volō. "
        "Hortus est bonus. Hortus multa habet.' "
        "Fīlius ad patrem venit. Fīlius: 'Pater, quid hortus habet?' "
        "Iūlius: 'Hortus habet rosās. Hortus habet aquam. "
        "Hortus habet multa. Ecce — rosās vidēs?' "
        "Fīlius rosās spectat. Fīlius: 'Rosās videō. Rosae sunt pulchrae.' "
        "Iūlius: 'Bene, rosae sunt pulchrae. "
        "Rosae sē aperuērunt. Iam rosae sunt pulchrae. "
        "Rosae sunt pulchrae hodiē — et rosae pulchrae erunt.' "
        "Fīlius: 'Pater, rosae sunt pulchrae. Ego rosās videō — et ego laetus sum.' "
        "Iūlius: 'Fīlī, tū bene vidēs. Hortus est bonus. "
        "Hortus hodiē rosās habet. Et hortus rosās habēbit.' "
        "Fīlius: 'Pater, quid est bonum in hortō?' "
        "Iūlius: 'Bonum est quod tū vidēs. Bonum est quod tū audīs. "
        "Bonum est quod tū in hortō es. "
        "Hic hortus est bonus. Hic diēs est bonus. "
        "Hoc bonum est: tū et ego in hortō sumus.' "
        "Fīlius patrem spectat. Fīlius: 'Pater, tū es bonus mihi.' "
        "Iūlius fīlium spectat. Iūlius: 'Fīlī, tū quoque es bonus mihi. "
        "Tū es fīlius meus. Tū es magnum bonum in corde meō.' "
        "Pater et fīlius ad aquam veniunt. "
        "Iūlius: 'Fīlī, aquam vidēs? Aqua cantat. "
        "Aqua est bona. Aqua in hortō cantat. "
        "Tū aquam vidēs. Tū aquam audīs. "
        "Aqua in hortō est — et aqua est bona hortī.' "
        "Fīlius aquam spectat. Fīlius aquam manibus tangit. "
        "Fīlius: 'Aqua est bona. Ego aquam audiō. Ego aquam videō.' "
        "Iūlius: 'Bene, fīlī. Aqua est bona. "
        "In hortō, aqua est rēs rosārum. Aqua est rēs līliōrum. "
        "Aqua est rēs hortī. Et aqua est rēs mea et tua.' "
        "Fīlius: 'Pater, tū mihi multa hodiē dīcis. "
        "Tū mihi multa dē rosīs dīcis. Tū mihi multa dē aquā dīcis. "
        "Ego multa videō. Ego multa audiō.' "
        "Iūlius: 'Fīlī, pater fīlium docet. "
        "Et fīlius ā patre discit. "
        "Pater et fīlius — hoc est bonum.' "
        "Fīlius: 'Pater, ego quoque fīlium habēbō — quandō vir erō. "
        "Et ego fīlium meum docēbō, sīcut tū mē docēs.' "
        "Iūlius: 'Fīlī, hoc est bonum. Tū fīlium habēbis. "
        "Tū fīlium docēbis. Et fīlius tuus fīlium suum docēbit. "
        "Ita sunt rēs — ut aqua in hortō cantat.' "
        "Fīlius: 'Pater, quandō ego vir erō, tūne mē vidēbis?' "
        "Iūlius: 'Fīlī, ego tē vidēbō. "
        "Ego tē amābō. "
        "Nam pater est pater. Et fīlius est fīlius.' "
        "Fīlius patrem tenet. Fīlius: 'Pater, tū es bonus pater. "
        "Ego tē videō. Ego laetus sum.' "
        "Iūlius fīlium tenet. Iūlius: 'Fīlī, tū es bonus fīlius. "
        "Ego tē videō. Ego tē audiō. Ego laetus sum.' "
        "Pater et fīlius in hortō sunt. "
        "Rosae in hortō sunt. Aqua in hortō cantat. "
        "Iūlius: 'Fīlī, hīc in hortō — ego et tū sumus. "
        "Et hoc est magnum bonum.' "
        "Fīlius: 'Pater, hīc in hortō — ego et tū sumus. "
        "Et hoc est magnum bonum.' "
        "Pater et fīlius in hortō ambulant. "
        "Pater fīlium docet. Fīlius ā patre discit. "
        "Pater et fīlius — duo in ūnō hortō. "
        "Pater et fīlius — duo in ūnā familiā. "
        "Et hortus est pulcher — nam in hortō pater et fīlius sunt. "
        "Et hoc est magnum bonum."
    )
}

# ============================================================
# 评估与输出
# ============================================================

def main():
    os.makedirs(REALITATES_DIR / "Cap5", exist_ok=True)
    results = []

    for key, story in STORIES.items():
        text = story["text"]
        name = story["title_la"]
        r = evaluate(text, name)
        wc = len(text.split())
        verdict = "PASS" if r["v2_level"] is not None and r["v2_level"] <= story["target_chapter"] + 2 else "FAIL"
        print(f"{key} {name}: wc={wc} v2_level={r['v2_level']} v2_rate={r['v2_rate']}% -> {verdict}")
        if r["v2_oov"]:
            print(f"  OOV: {r['v2_oov'][:20]}")
        results.append((key, story, r, wc, verdict))

    # 生成 Markdown 文件
    for key, story, r, wc, verdict in results:
        story_text = story["text"]
        filename = f"Cap5_{story['title_la'].replace(' ', '_')}_{'medius' if story['length_tier'] == '中篇' else 'longior'}_{key.split('_')[1]}.md"
        filepath = REALITATES_DIR / "Cap5" / filename
        yaml = f"""---
story_id: "{key}"
title_la: "{story['title_la']}"
title_zh: "{story['title_zh']}"
target_chapter: {story['target_chapter']}
theme: "{story['theme']}"
style: "{story['style']}"
genre: "{story['genre']}"
character_type: "{story['character_type']}"
length_tier: "{story['length_tier']}"
narrative_mode: "{story['narrative_mode']}"
word_count: {wc}
macrons_status: "generated"
evaluated_chapter: {r['v2_level']}
best_fit_chapter: {r['v2_best_fit']}
coverage_rate: {r['v2_rate']}
oov_words: {json.dumps(r['v2_oov'])}
rewritten_from: "brevis"
rewritten_at: "{datetime.now(timezone.utc).isoformat()}"
status: "rewritten"
---
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(yaml + "\n" + story_text + "\n")

    passed = sum(1 for _, _, _, _, v in results if v == "PASS")
    print(f"\n{passed}/{len(results)} passed")

    # 删除旧 brevis 文件
    if passed == len(results):
        print("All passed! Deleting old brevis files...")
        for f in (REALITATES_DIR / "Cap5").glob("*_brevis_*.md"):
            f.unlink()
            print(f"  Deleted: {f.name}")
    else:
        print("Some failed - old files preserved.")

if __name__ == "__main__":
    main()