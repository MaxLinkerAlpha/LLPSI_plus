#!/usr/bin/env python3
"""rewrite_cap13.py — 重写 Cap.13 的 33 篇短篇为 中篇/中长篇/长篇。
比例 5:3:2 → 17中篇 + 10中长篇 + 6长篇。
非严格模式：v2_level ≤ target_chapter + 2 (=15) 即可。
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
# 中篇 (medius, 300-500 words) x17
# ============================================================

STORIES["cap13_01"] = {
    "title_la": "Hōrologium et Senex",
    "title_zh": "钟与老人",
    "target_chapter": 13,
    "theme": "12 时间",
    "style": "精炼",
    "genre": "G 哲理寓言",
    "character_type": "老人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Senex in hortō sedet. Senex est antīquus. Senex multōs annōs vīdit. "
        "Hōrologium in mūrō est. Hōrologium quoque antīquum est. "
        "Hōrologium tacet. Tempus nōn movētur. "
        "Senex hōrologium spectat. Senex: 'Tū et ego, amīce, similes sumus. "
        "Tū numerās hōrās. Ego numerō diēs. Sed quis numerat annōs?' "
        "Hōrologium nihil respondet. Hōrologium tacet. "
        "Senex aquam bibit. Aqua est frīgida. Aqua est bona. "
        "Sōl in caelō movētur. Umbra in terrā movētur. "
        "Senex umbram spectat. Umbra longa est. Umbra lenta est. "
        "Senex: 'Umbra quoque similis est. Umbra nōn manet. Umbra semper movētur. "
        "Sīcut vita. Sīcut tempus.' "
        "Senex oculōs claudit. Senex sōlem in cute sentit. "
        "Sōl est calidus. Ventus est levis. "
        "Senex audit: avēs in arboribus cantant. Aqua in fluviō fluit. "
        "Puerī in viā rīdent. Puellae in viā currunt. "
        "Senex: 'Omnia moventur. Omnia vīvunt. Sōlus ego... maneō.' "
        "Tum senex oculōs aperit. Hōrologium nōn iam tacet. "
        "Hōrologium movētur. Hōrologium sonat. "
        "Senex: 'Tū quoque movēris, amīce?' "
        "Sed hōrologium nōn respondet. Hōrologium sōlum hōrās dīcit. "
        "Senex surgit. Senex ad hōrologium it. "
        "Senex manum ad hōrologium extendit. Hōrologium est frīgidum. "
        "Senex: 'Frīgidus es. Sīcut ego. Sed tū semper movēris. "
        "Ego... nōn semper.' "
        "Senex iterum in hortō sedet. Sōl nunc in caelō altus est. "
        "Umbra nunc brevis est. Senex umbram brevem spectat. "
        "Senex: 'Brevī, umbra iterum longa erit. Et tum... nox veniet.' "
        "Senex hōrologium spectat. Hōrologium nunc movētur. "
        "Senex: 'Movēre, amīce. Movēre. Ego hīc maneō. "
        "Et quandō tū cessābis — ego quoque cessābō.' "
        "Sōl in caelō descendit. Umbra longa fit. "
        "Senex oculōs claudit. Hōrologium tacet. "
        "Nox venit. Stēllae in caelō sunt. "
        "Et senex et hōrologium — ambō quiēscunt."
    ),
}

STORIES["cap13_02"] = {
    "title_la": "Alter Ego",
    "title_zh": "另一个我",
    "target_chapter": 13,
    "theme": "33 自我与他人",
    "style": "史诗",
    "genre": "C 历史与人物",
    "character_type": "非罗马的古代人",
    "length_tier": "中篇",
    "narrative_mode": "第二人称",
    "text": (
        "Tū in aquā faciem tuam vidēs. Sed haec nōn est faciēs tua. Alius est. "
        "'Quis es?' rogās. "
        "Ille: 'Ego sum tū — tū quem numquam fuistī. "
        "Tū quem semper esse voluistī.' "
        "Tū manum ad aquam extendis. Ille quoque manum extendit. "
        "Digitī vestrī nōn tangunt — aqua inter vōs est. "
        "'Possumne tē tangere?' rogās. "
        "Ille: 'Nōn. Sed tū potes mē fierī.' "
        "Tū surgis. Tū nōn iam in aquam spectās. "
        "Tū in viā ambulās — nōn sōlus, sed cum alterō tē. "
        "Tū in oppidum īs. Virī in oppidō sunt. Fēminae sunt. Puerī sunt. "
        "Tū virōs spectās. Tū fēminās spectās. "
        "Tū: 'Quis est ille? Quis est illa? Quis sum ego?' "
        "Alter tū: 'Nōn spectā illōs. Spectā mē. Ego sum via.' "
        "Tū in vīllam tuam īs. Māter tua in vīllā est. "
        "Māter: 'Fīlī, tū hodiē alius vidēris.' "
        "Tū: 'Māter, quis sum ego?' "
        "Māter tacet. Māter tē spectat. Māter: 'Tū es fīlius meus.' "
        "Tū: 'Sed quis est fīlius tuus?' Māter nōn respondet. "
        "Nocte, tū in cubiculō tuō es. Stēllae in caelō sunt. "
        "Alter tū prope tē stat. Ille: 'Tū vīdistī. Māter tua mē quoque videt. "
        "Māter tua nescit quis tū sīs. Nēmō scit.' "
        "Tū: 'Cūr mē sequeris?' "
        "Ille: 'Quia tū mē vocāvistī. Tū mē semper vocāvistī. "
        "Ex quō puer parvus fuistī — tū mē vocāvistī.' "
        "Tū: 'Quid vīs?' "
        "Ille: 'Nōn ego volō. Tū vīs. Tū vīs mē fierī. "
        "Tū vīs esse fortis. Tū vīs esse bonus. Tū vīs esse... alter.' "
        "Tū tacet. Tū in caelum spectās. Stēllae sunt multae. "
        "Tū: 'Et sī ego tē fīō — quid manet dē mē?' "
        "Ille: 'Nihil. Sed tū iam nihil es. Tū es sōlum quod nōn es.' "
        "Māne venit. Sōl in caelō surgit. "
        "Tū ad aquam redīs. Tū in aquam spectās. "
        "Duae faciēs in aquā sunt. Tua et altera. "
        "Tū: 'Ego tē nōn fugiō. Sed ego tē nōn fīō. "
        "Ego sum quī sum. Et tū — tū es via quam nōn īvī.' "
        "Ille in aquā tacet. Ille nōn movētur. "
        "Tū aquam tangis. Aqua movētur. Faciēs altera nōn iam est. "
        "Tū sōlus in aquā es. Tū tē ipsum vidēs. "
        "Tū: 'Ego sum. Hoc est satis.'"
    ),
}

STORIES["cap13_03"] = {
    "title_la": "Dēspērātiō in Urbe",
    "title_zh": "城中的绝望",
    "target_chapter": 13,
    "theme": "20 绝望",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir in urbe ambulat. Urbs est magna. Urbs est Rōma. "
        "Vir est pauper. Vir nihil habet. "
        "Māne est. Sōl in caelō est. Sed vir sōlem nōn videt. "
        "Vir in viā ambulat. Multī hominēs in viā sunt. "
        "Aliī rīdent. Aliī dīcunt. Aliī cibum edunt. "
        "Vir nihil habet. Vir nihil edit. Vir nihil dīcit. "
        "Vir ad forum it. In forō, multī virī sunt. "
        "Aliī mercēs vēndunt. Aliī pecūniam numerant. "
        "Vir nihil vēndit. Vir nihil emit. Vir nihil habet. "
        "Vir in terrā sedet. Vir caput in manibus ponit. "
        "Homō ad eum venit. Homō: 'Cūr hīc sedēs? Cūr nōn labōrās?' "
        "Vir: 'Nōn habeō labōrem. Nēmō mē vult.' "
        "Homō: 'Semper est aliquid. Tū potes aquam portāre. Tū potes...' "
        "Vir: 'Ego omnia temptāvī. Nēmō mē vult. Nēmō mē videt.' "
        "Homō tacet. Homō abit. "
        "Vir sōlus in forō sedet. Sōl in caelō movētur. "
        "Diēs longus est. Diēs calidus est. "
        "Vir nōn movētur. Vir nōn edit. Vir nōn bibit. "
        "Fēmina ad eum venit. Fēmina panem in manū habet. "
        "Fēmina: 'Accipe. Tū es miser. Ego videō.' "
        "Vir: 'Cūr? Cūr mē iuvās?' "
        "Fēmina: 'Quia ego quoque fuī ubi tū es. "
        "Ego quoque nihil habuī. Et aliquis mē iūvit.' "
        "Vir panem capit. Vir panem spectat. "
        "Vir: 'Hic panis... est parvus. Sed... est magnus.' "
        "Fēmina: 'Semper est aliquid. Semper est aliquis.' "
        "Fēmina abit. Vir sōlus manet. Sed nōn iam sōlus est. "
        "Vir panem edit. Panis est bonus. "
        "Vir in caelum spectat. Sōl adhūc in caelō est. "
        "Vir surgit. Vir in viā ambulat. "
        "Vir: 'Fortasse... fortasse hodiē nōn est fīnis. "
        "Fortasse crās... aliquid erit.' "
        "Vir in viā ambulat. Urbs est magna. Urbs est Rōma. "
        "Vir est pauper. Sed vir iam nōn est nihil."
    ),
}

STORIES["cap13_04"] = {
    "title_la": "Diarium Medici",
    "title_zh": "医生日志",
    "target_chapter": 13,
    "theme": "19 希望",
    "style": "冷峻",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "日记体",
    "text": (
        "Diēs prīmus. Hodiē trēs aegrōs vīdī. "
        "Ūnus mortuus est. Duo vīvunt. "
        "Nōn sciō cūr. Ego medicus sum — sed nōn omnia sciō. "
        "Diēs secundus. Hodiē fēmina ad mē vēnit. "
        "Fēmina fīlium parvum habet. Puer aeger est. "
        "Puer nōn edit. Puer nōn bibit. Puer nōn dormit. "
        "Fēmina: 'Medice, iuvā fīlium meum!' "
        "Ego puerum spectō. Ego nihil videō. "
        "Nūllum vulnus. Nūllus sanguis. Sed puer aeger est. "
        "Ego: 'Nōn sciō. Dēbēs... dēbēs eum tenēre. Dēbēs eī aquam dare.' "
        "Fēmina plōrat. Ego nihil facere possum. "
        "Diēs tertius. Puer mortuus est. Fēmina nōn vēnit. "
        "Ego sōlus in cubiculō sedeō. Ego nihil facere possum. "
        "Ego medicus sum — sed medicus nōn est deus. "
        "Diēs quārtus. Hodiē vir ad mē vēnit. "
        "Vir vulnus in bracchiō habet. Vulnus est magnum. "
        "Ego vulnus lavō. Ego vulnus ligō. "
        "Vir: 'Dolōrem sentiō. Sed ego vīvus sum.' "
        "Ego: 'Tū vīvus es. Hoc est bonum.' "
        "Vir: 'Tū mē iūvistī. Ego tibi grātiās agō.' "
        "Diēs quīntus. Hodiē senex ad mē vēnit. "
        "Senex: 'Ego multōs annōs vīxī. Ego mortem nōn timeō. "
        "Sed ego dolōrem timeō. Potesne mē iuvāre?' "
        "Ego: 'Possum. Ego tē iuvābō.' "
        "Ego senī medicīnam dō. Senex nōn iam dolet. "
        "Senex: 'Grātiās. Tū es bonus medicus.' "
        "Diēs sextus. Hodiē multōs aegrōs vīdī. "
        "Aliī vīvunt. Aliī moriuntur. "
        "Ego nōn omnia facere possum. Sed ego aliquid facere possum. "
        "Ego medicus sum. Ego nōn sum deus. "
        "Sed ego cum aegrīs sum. Ego eōs teneō. Ego eōs iuvō. "
        "Hoc est satis."
    ),
}

STORIES["cap13_05"] = {
    "title_la": "Fīlius et Umbra Patris",
    "title_zh": "儿子与父影",
    "target_chapter": 13,
    "theme": "25 家庭",
    "style": "抒情",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Patrem meum semper in umbrā vīdī. Pater meus magnus vir fuit. "
        "In urbe, nōmen eius omnēs sciēbant. "
        "Ego parvus puer eram. Ego patrem meum in forō vidēbam. "
        "Virī ad eum veniēbant. Virī eum salūtābant. "
        "Ego post eum ambulābam — in umbrā eius. "
        "Pater: 'Fīlī, tū quoque magnus eris. Tū nōmen meum portābis.' "
        "Ego: 'Ego nōn sum tū, pater. Ego sum parvus.' "
        "Pater: 'Nunc parvus es. Sed tempus veniet.' "
        "Annī iērunt. Ego crevī. Pater meus senex fit. "
        "Nunc ego in forō ambulō. Nunc virī mē salūtant. "
        "Sed nōn propter mē — propter patrem meum. "
        "Ego: 'Pater, ego nōn sum tū. Ego nōmen tuum habeō — sed ego ipse nōn sum.' "
        "Pater: 'Nōmen est via. Via ad tē dūcit.' "
        "Ego: 'Sed via tua nōn est via mea. Ego nōn volō esse umbra.' "
        "Pater tacet. Pater mē spectat. "
        "Pater: 'Tū nōn es umbra, fīlī. Tū es fīlius meus. "
        "Et fīlius nōn est umbra — fīlius est nova lūx.' "
        "Nunc intellegō. Pater meus mē nōn in umbrā tenēbat. "
        "Pater meus mē ad sōlem dūcēbat. "
        "Nunc ego in forō ambulō. Nunc virī mē salūtant. "
        "Nōn propter patrem. Propter mē. "
        "Et quandō pater meus oculōs claudit — ego nōn in umbrā manēbō. "
        "Ego lūcem meam habēbō. Sīcut pater voluit."
    ),
}

STORIES["cap13_06"] = {
    "title_la": "Hortus Post Pluviam",
    "title_zh": "雨后花园",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pluvia per noctem vēnit. Pluvia multa fuit. "
        "Māne, sōl in caelō surgit. Caelum est clārum. "
        "Puella in hortum exit. Puella rosās spectat. "
        "Rosae post pluviam sunt pulchrae. "
        "Aqua in foliīs rosārum est. Aqua lūcet in sōle. "
        "Puella: 'Quam pulchrae sunt rosae post pluviam!' "
        "Puella in hortō ambulat. Herba est umida. "
        "Puella pedēs nūdōs in herbā ponit. Herba est mollis. "
        "Puella: 'Terra post pluviam est nova. Terra post pluviam est vīva.' "
        "Avēs in arboribus cantant. Avēs quoque post pluviam laetae sunt. "
        "Puella in caelum spectat. Caelum est caeruleum. "
        "Nūbēs sunt albae. Nūbēs lentē moventur. "
        "Puella: 'Pluvia abiit. Sed pluvia omnia mūtāvit.' "
        "Puer ex vīllā venit. Puer: 'Quid facis in hortō?' "
        "Puella: 'Venī! Vidē! Hortus post pluviam est pulcher!' "
        "Puer in hortum venit. Puer rosās spectat. "
        "Puer: 'Ita. Rosae sunt pulchrae. Sed cūr?' "
        "Puella: 'Quia pluvia eās lavat. Pluvia eās novās facit. "
        "Sīcut lacrimae — lacrimae quoque nōs lavant. "
        "Post lacrimās, nōs novī sumus.' "
        "Puer puellam spectat. Puer: 'Tū sapientior es quam ego.' "
        "Puella rīdet. Puella: 'Nōn sum sapiēns. Ego sōlum videō.' "
        "Puella et puer in hortō sedent. "
        "Sōl in caelō est. Rosae in hortō sunt. "
        "Puella: 'Post pluviam, semper sōl venit. Hoc est bonum.' "
        "Puer: 'Hoc est vērum. Post noctem, semper diēs venit.' "
        "Puella: 'Et post trīstitiam, semper gaudium venit.' "
        "Puer et puella tacent. Sōl in caelō lūcet. "
        "Hortus post pluviam est pulcher. Et puella laeta est."
    ),
}

STORIES["cap13_07"] = {
    "title_la": "Hostis in Portīs",
    "title_zh": "敌在门前",
    "target_chapter": 13,
    "theme": "15 战争",
    "style": "冷峻",
    "genre": "F 战争与征服",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hostēs ad portās urbis sunt. Hostēs sunt multī. "
        "In urbe, virī timent. Fēminae timent. Puerī timent. "
        "Dux in forō stat. Dux: 'Nōn timēte! Urbs nostra fortis est! "
        "Mūrī nostrī altī sunt! Portae nostrae firmae sunt!' "
        "Sed virī timent. Virī hostēs vident. "
        "Hostēs sunt multī — sīcut undae maris. "
        "Hostēs ignem in manibus habent. Hostēs clāmant. "
        "Senex in forō: 'Ego iuvenis eram quandō hostēs prius vēnērunt. "
        "Tum quoque dīxērunt: nōn timēte. Sed multī mortuī sunt.' "
        "Vir: 'Quid facere possumus? Nōs nōn sumus mīlitēs. "
        "Nōs sumus virī, fēminae, puerī.' "
        "Fēmina: 'Nōs pugnāre nōn possumus. Sed nōs iuvāre possumus. "
        "Nōs aquam portāre possumus. Nōs cibum facere possumus.' "
        "Puer: 'Ego quoque iuvāre possum! Ego parvus sum — sed ego currere possum!' "
        "Dux puerum spectat. Dux: 'Tū es parvus. Sed tū es fortis. "
        "Tū potes nūntium ad mīlitēs portāre.' "
        "Puer: 'Ego portābō!' "
        "Nox venit. Hostēs prope mūrōs sunt. "
        "In urbe, omnēs labōrant. Virī arma faciunt. "
        "Fēminae cibum faciunt. Puerī aquam portant. "
        "Senex: 'Ego nihil facere possum. Ego sum senex.' "
        "Puer: 'Tū potes nārāre. Nārrā nōbīs dē prioribus bellīs. "
        "Nārrā nōbīs quōmodō urbs semper vīxit.' "
        "Senex: 'Bene. Ego nārrābō.' "
        "Senex nārrat. Omnēs audiunt. "
        "Et in nocte, quandō hostēs clāmant — "
        "in urbe, virī et fēminae et puerī nōn timent. "
        "Urbs nōn cadit. Urbs nōn cadet. "
        "Quia urbs nōn est mūrī. Urbs est hominēs."
    ),
}

STORIES["cap13_08"] = {
    "title_la": "In Stabulō",
    "title_zh": "在马厩里",
    "target_chapter": 13,
    "theme": "36 乡村",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Servus in stabulō est. Stabulum est magnum. "
        "In stabulō, multī equī sunt. Equī sunt magnī et pulchrī. "
        "Servus equōs cūrat. Servus equīs cibum dat. Servus equōs lavat. "
        "Servus: 'Vōs estis pulchrī, equī. Vōs estis fortēs. "
        "Ego sum servus — sed vōs nōn estis servī. Vōs estis līberī.' "
        "Equus niger caput movet. Equus servum spectat. "
        "Servus equum tangit. Servus: 'Tū mē intellegis, amīce?' "
        "Dominus in stabulum intrat. Dominus: 'Servus, equī sunt parātī?' "
        "Servus: 'Ita, domine. Equī sunt parātī.' "
        "Dominus: 'Bene. Hodiē ad urbem ībō. Equum nigrum parā.' "
        "Servus equum nigrum parat. Servus equō aquam dat. "
        "Servus: 'Dominus ad urbem it. Tū eum portābis. Tū es bonus equus.' "
        "Equus nihil dīcit. Sed equus servum spectat. "
        "Dominus in equō ad urbem it. Servus in stabulō manet. "
        "Servus aliōs equōs cūrat. Servus stabulum lavat. "
        "Servus: 'Dominus abiit. Nunc stabulum est meum. "
        "Nunc equī sunt meī. Ego sum dominus hīc.' "
        "Servus in stabulō sedet. Servus equōs spectat. "
        "Servus: 'In stabulō, ego nōn sum servus. In stabulō, ego sum... ego.' "
        "Vesperī venit. Dominus ex urbe redit. "
        "Dominus: 'Servus, equum cape. Equus fessus est.' "
        "Servus equum capit. Servus equum lavat. Servus equō cibum dat. "
        "Servus: 'Bene vēnistī, amīce. Tū multum labōrāvistī hodiē.' "
        "Equus servum spectat. Equus caput ad servum movet. "
        "Servus rīdet. Servus: 'Nōs sumus similēs, tū et ego. "
        "Nōs ambō servī sumus. Sed nōs ambō... vīvimus.' "
        "Nox venit. Stabulum tacet. Equī dormiunt. Servus quoque dormit. "
        "Et in stabulō, omnia sunt bona."
    ),
}

STORIES["cap13_09"] = {
    "title_la": "Īnsulae Graeciae",
    "title_zh": "希腊群岛",
    "target_chapter": 13,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nāvis in marī est. Nāvis inter īnsulās Graeciae nāvigat. "
        "In nāve, vir Graecus est. Vir multās terrās vīdit. "
        "Vir: 'Īnsulae Graeciae sunt multae — sīcut stēllae in caelō. "
        "Quaeque īnsula suam fābulam habet.' "
        "Nauta: 'Quam fābulam nārrābis hodiē?' "
        "Vir: 'Ego nārrābō dē Crētā — īnsulā magnā. "
        "In Crētā, rēx Mīnōs vīxit. Mīnōs magnum palātium habuit. "
        "In palātiō, multae viae erant — sīcut labyrinthus.' "
        "Nauta: 'Dē labyrinthō audīvī. Ibi mōnstrum fuit.' "
        "Vir: 'Ita. Mōnstrum nōmine Mīnōtaurus. "
        "Sed fābula nōn est dē mōnstrō — fābula est dē homine. "
        "Homō nōmine Daedalus. Daedalus labyrinthum fēcit. "
        "Daedalus volāre voluit. Daedalus ālās fēcit — ex cērā et pennīs.' "
        "Nauta: 'Et volāvit?' "
        "Vir: 'Ita. Daedalus volāvit — ex Crētā ad Siciliam. "
        "Sed fīlius eius, Īcarus, nōn ad terram vēnit. "
        "Īcarus in mare cadit. Mare nunc nōmen eius habet — Mare Īcarium.' "
        "Nauta: 'Tristis fābula est.' "
        "Vir: 'Ita. Sed fābula docet: nōlī nimis altum volāre. "
        "Sed etiam docet: homō potest volāre — sī vult.' "
        "Nāvis ad aliam īnsulam nāvigat. Īnsula est parva. "
        "Vir: 'Haec est īnsula Naxos. Hīc, fēmina nōmine Ariadna relicta est. "
        "Ariadna Thēseum iūvit — et Thēseus eam relīquit.' "
        "Nauta: 'Cūr omnēs fābulae sunt trīstēs?' "
        "Vir: 'Fortasse quia vīta est trīstis. "
        "Sed fābulae nōs docent: etiam in trīstitiā, pulchrum est.' "
        "Sōl in mare cadit. Mare est rubrum. "
        "Nāvis inter īnsulās nāvigat. Vir fābulās nārrat. "
        "Et nautae audiunt — et īnsulae tacent."
    ),
}

STORIES["cap13_10"] = {
    "title_la": "Lūna et Puer",
    "title_zh": "月亮与男孩",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "A 童话",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in hortō sedet. Nox est. Lūna in caelō est. "
        "Lūna est magna. Lūna est pulchra. Lūna est alba. "
        "Puer lūnam spectat. Puer: 'Lūna, tū es tam pulchra. "
        "Cūr tū sōla in caelō es?' "
        "Lūna: 'Ego nōn sum sōla. Stēllae mēcum sunt.' "
        "Puer: 'Stēllae sunt parvae. Tū es magna. "
        "Tū es rēgīna caelī.' "
        "Lūna: 'Ego nōn sum rēgīna. Ego sum sōlum lūna. "
        "Ego lūcem meam ā sōle habeō.' "
        "Puer: 'Ā sōle? Sed sōl nōn est hīc. Sōl abiit.' "
        "Lūna: 'Sōl semper est — etiam quandō nōn vidēs. "
        "Ego lūcem eius ad tē portō in nocte.' "
        "Puer: 'Tū es bona, lūna. Tū mē nōn dēseris in nocte.' "
        "Lūna: 'Nēmō tē dēserit, puer. Sōl in diē tē videt. "
        "Stēllae in nocte tē spectant. Ego inter diem et noctem sum. "
        "Ego tē semper videō.' "
        "Puer: 'Et quandō ego dormiō?' "
        "Lūna: 'Tum quoque ego tē videō. Ego tē in somnīs custōdiō.' "
        "Puer oculōs claudit. Puer dormit. "
        "Lūna in caelō manet. Lūna puerum spectat. "
        "Māne venit. Sōl in caelō surgit. Lūna abīt. "
        "Puer oculōs aperit. Puer: 'Lūna abiit. Sed lūna redībit. "
        "Lūna semper redit.' "
        "Puer in hortō sedet. Sōl in caelō est. "
        "Puer: 'Sōl, tū quoque es bonus. Tū mihi lūcem dās in diē.' "
        "Sōl nihil dīcit. Sed sōl calidus est. "
        "Puer laetus est. Puer: 'Diēs et nox — ambō sunt bonī. "
        "Sōl et lūna — ambō mē custōdiunt.' "
        "Et puer in hortō lūdit. Et diēs bonus est."
    ),
}

STORIES["cap13_11"] = {
    "title_la": "Mercātor et Via",
    "title_zh": "商人与路",
    "target_chapter": 13,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "商人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mercātor in viā est. Via est longa. Via ad urbem dūcit. "
        "Mercātor multās mercēs portat. In sacculīs, multae rēs sunt. "
        "Mercātor: 'Via est longa. Sed in urbe, mercēs meās vēndam. "
        "Pecūniam habēbō. Tum ad vīllam redībō.' "
        "Mercātor per campōs it. Per silvās it. Per flūmina it. "
        "In viā, aliī viātōrēs sunt. "
        "Ūnus: 'Quō īs, mercātor?' "
        "Mercātor: 'Ad urbem eō. Mercēs meās vēndam.' "
        "Alius: 'Urbs est longē. Via est perīculōsa. Cūr īs?' "
        "Mercātor: 'Quia necesse est. Familia mea mē exspectat.' "
        "Mercātor in viā ambulat. Diēs est calidus. "
        "Mercātor sub arbore sedet. Mercātor aquam bibit. "
        "Mercātor: 'Via est longa. Sed via est pulchra. "
        "Caelum est caeruleum. Avēs cantant. Herba est bona.' "
        "Mercātor surgit. Mercātor iterum ambulat. "
        "Vesperī venit. Sōl in caelō descendit. "
        "Mercātor: 'Nox venit. Dēbeō locum invenīre.' "
        "Mercātor parvam vīllam videt. In vīllā, vir et fēmina habitant. "
        "Vir: 'Tū es fessus. Venī in vīllam. Hīc dormīre potes.' "
        "Mercātor: 'Grātiās. Ego multās hōrās ambulāvī.' "
        "Mercātor in vīllā dormit. "
        "Māne, mercātor surgit. Mercātor: 'Grātiās vōbīs agō. Ego nunc eō.' "
        "Fēmina: 'Valē, mercātor. Via tūta sit.' "
        "Mercātor iterum in viā est. Post multōs diēs, urbem videt. "
        "Mercātor: 'Urbs! Ecce — urbs!' "
        "Mercātor in urbem intrat. Mercātor mercēs vēndit. "
        "Mercātor: 'Nunc pecūniam habeō. Nunc ad vīllam redīre possum.' "
        "Sed mercātor intellegit: via nōn est fīnis. "
        "Via est vīta. Et mercātor semper in viā erit."
    ),
}

STORIES["cap13_12"] = {
    "title_la": "Noctū in Oppidō",
    "title_zh": "夜间在镇上",
    "target_chapter": 13,
    "theme": "21 沉默",
    "style": "抒情",
    "genre": "C 历史与人物",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Noctū in oppidō ambulō. Oppidum est parvum. Oppidum tacet. "
        "Nēmō in viīs est. Omnēs in vīllīs dormiunt. "
        "Ego sōlus ambulō. Lūna in caelō est. "
        "Lūna mihi viam ostendit. Stēllae mihi comitēs sunt. "
        "Ego in viā ambulō. Via est angusta. Via est nigra. "
        "Ego sonum pedum meōrum audiō. Sōlus sonus in nocte. "
        "Ego ante portam vīllae stō. In vīllā, lūx est. "
        "Per fenestram, familiam videō. Pater et māter et puerī. "
        "Puerī rīdent. Māter cibum in mēnsā pōnit. "
        "Ego eōs spectō — sed ego nōn sum in vīllā. "
        "Ego sum in viā. Ego sum viātor. "
        "Ego: 'Cūr ego in viā sum? Cūr nōn in vīllā?' "
        "Nēmō respondet. Oppidum tacet. "
        "Ego iterum ambulō. Ego ad forum veniō. "
        "Forum est vacuum. Nēmō in forō est. "
        "In forō, statuae sunt. Statuae virōrum magnōrum. "
        "Statuae tacent — sīcut oppidum. "
        "Ego: 'Vōs quoque fuistis in viā, nōnne? "
        "Vōs quoque in nocte ambulāvistis?' "
        "Statuae nihil dīcunt. Sed ego intellegō. "
        "Omnēs sumus viātōrēs. Omnēs in nocte ambulāmus. "
        "Ego in oppidō ambulō. Nox est longa. "
        "Sed ego nōn timeō. Oppidum mēcum est. "
        "Et māne, quandō sōl surgit — ego iterum in viā erō. "
        "Sed hanc noctem, hanc silentiōsam noctem — "
        "ego semper in corde habēbō."
    ),
}

STORIES["cap13_13"] = {
    "title_la": "Nox in Vīllā",
    "title_zh": "别墅之夜",
    "target_chapter": 13,
    "theme": "36 乡村",
    "style": "抒情",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nox in vīllā est. Vīlla tacet. Omnēs dormiunt. "
        "Sed dominus nōn dormit. Dominus in hortō sedet. "
        "Dominus: 'Nox est tam quiēta. Nox est tam pulchra. "
        "In diē, multī hominēs in vīllā sunt. Servī labōrant. "
        "Puerī currunt. Fēminae dīcunt. "
        "Sed in nocte — sōlus sum.' "
        "Dominus in caelum spectat. Stēllae sunt multae. "
        "Dominus: 'Stēllae semper in caelō sunt — etiam in diē. "
        "Sed in diē, nōs eās nōn vidēmus. Sōl eās tegit.' "
        "Lūna in caelō est. Lūna lūcet in hortō. "
        "Dominus rosās in hortō videt. Rosae in nocte sunt albae. "
        "Dominus: 'In diē, rosae sunt rubrae. In nocte, rosae sunt albae. "
        "Fortasse omnia in nocte alia sunt.' "
        "Dominus servum videt. Servus in hortō est. "
        "Dominus: 'Cūr nōn dormīs?' "
        "Servus: 'Domine, ego quoque noctem amō. "
        "In nocte, nōn sum servus. In nocte, sum sōlum homo.' "
        "Dominus servum spectat. Dominus: 'Intellegō. "
        "In nocte, nōn sum dominus. In nocte, sum sōlum homo.' "
        "Dominus et servus in hortō sedent. Ambō tacent. "
        "Ambō stēllās spectant. Ambō noctem audiunt. "
        "In nocte, nōn est dominus et servus. "
        "In nocte, sunt sōlum duo hominēs. "
        "Et quandō sōl surgit — diēs iterum venit. "
        "Sed ambo meminērunt: in nocte, fuimus amīcī."
    ),
}

STORIES["cap13_14"] = {
    "title_la": "Pōns in Fluviō",
    "title_zh": "河上之桥",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "C 历史与人物",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pōns in fluviō est. Pōns est antīquus. Pōns est lapideus. "
        "Multī hominēs in ponte ambulant. Aliī ad urbem eunt. "
        "Aliī ex urbe veniunt. Omnēs in ponte sunt — sed nēmō pontem spectat. "
        "Vir senex in ponte stat. Vir pontem spectat. "
        "Vir: 'Hic pōns multōs annōs hīc est. "
        "Multī hominēs in ponte ambulāvērunt. "
        "Mīlitēs, mercātōrēs, viātōrēs, puerī, puellae. "
        "Omnēs trans fluvium iērunt — per hunc pontem.' "
        "Puer ad senem venit. Puer: 'Cūr pontem spectās? "
        "Pōns est sōlum pōns.' "
        "Senex: 'Pōns est plūs quam pōns. "
        "Pōns est via — via inter duās terrās. "
        "Pōns coniungit quod fluvius sēparat.' "
        "Puer: 'Fluvius nōn est magnus. Sine ponte, possum natāre.' "
        "Senex: 'Ita. Tū potes natāre. Sed mercātor cum mercibus? "
        "Māter cum parvō puerō? Senex — sīcut ego? "
        "Pōns nōn est pro tē — pōns est pro omnibus.' "
        "Puer pontem spectat. Puer: 'Nunc intellegō. "
        "Pōns nōn est sōlum lapidēs. Pōns est... bonum.' "
        "Senex: 'Ita, puer. Pōns est dōnum. "
        "Dōnum ab illīs quī ante nōs fuērunt. "
        "Et nōs dēbēmus pontem servāre — pro illīs quī post nōs venient.' "
        "Puer: 'Ego quoque pontem servābō!' "
        "Senex rīdet. Senex: 'Bene, puer. Nunc ī. "
        "Et quandō tū trans pontem ībis — meminī: "
        "pōns est plūs quam lapidēs. Pōns est amor.' "
        "Puer trans pontem currit. Senex in ponte manet. "
        "Fluvius sub ponte fluit. Sōl in caelō est. "
        "Et pōns — pōns semper hīc est."
    ),
}

STORIES["cap13_15"] = {
    "title_la": "Porta Urbis",
    "title_zh": "城门",
    "target_chapter": 13,
    "theme": "35 城市",
    "style": "精炼",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Porta urbis magna est. Porta ex lapide facta est. "
        "Per portam, multī intrant. Per portam, multī exeunt. "
        "Mīles ad portam stat. Mīles omnēs spectat. "
        "Māne, agricola per portam intrat. Agricola holera portat. "
        "Mīles: 'Quid portās?' Agricola: 'Holera ex agrīs. "
        "In forō ea vēndam.' Mīles: 'Ī.' "
        "Mercātor per portam intrat. Mercātor multās rēs portat. "
        "Mīles: 'Quid portās?' Mercātor: 'Mercēs ex Graeciā. "
        "In forō eās vēndam.' Mīles: 'Ī.' "
        "Puer per portam currit. Puer nihil portat. "
        "Mīles: 'Quō curris?' Puer: 'Ad forum! Pater mē exspectat!' "
        "Mīles: 'Ī.' "
        "Senex per portam lentē ambulat. Senex nihil portat. "
        "Mīles: 'Quō īs?' Senex: 'Nusquam. Ego sōlum ambulō. "
        "Ego hanc portam multōs annōs videō. "
        "Per hanc portam, ego iuvenis intrāvī. "
        "Per hanc portam, ego fīliam meam ad nūptiās dūxī. "
        "Per hanc portam, ego fīlium meum ad bellum mīsī.' "
        "Mīles tacet. Mīles senem spectat. "
        "Senex: 'Porta videt omnia. Porta nihil dīcit. "
        "Sed porta meminit. Porta semper meminit.' "
        "Mīles: 'Tū quoque meminī?' "
        "Senex: 'Ego meminī. Et quandō ego nōn iam erō — "
        "porta adhūc hīc erit. Et porta meminerit.' "
        "Senex per portam exit. Mīles ad portam stat. "
        "Mīles portam spectat. Mīles: 'Porta videt omnia. "
        "Et ego — ego sōlum hīc stō. Sed ego quoque videō.' "
        "Nox venit. Porta clauditur. Mīles domum it. "
        "Sed porta manet. Porta semper manet."
    ),
}

STORIES["cap13_16"] = {
    "title_la": "Puer et Liber",
    "title_zh": "男孩与书",
    "target_chapter": 13,
    "theme": "09 勇气",
    "style": "雄辩",
    "genre": "D 中国",
    "character_type": "奴隶",
    "length_tier": "中篇",
    "narrative_mode": "第二人称",
    "text": (
        "Tū es puer. Tū servus es. Tū in vīllā magnā labōrās. "
        "Dominus tuus est dīves. Dominus tuus multōs librōs habet. "
        "Tū librōs vidēs — sed tū legere nōn potes. "
        "Tū: 'Quid est in librīs? Cūr dominus eōs amat?' "
        "Nēmō tibi respondet. Servī nōn legunt. "
        "Sed tū scīre vīs. Tū semper scīre voluistī. "
        "Nocte, quandō omnēs dormiunt, tū in bibliothēcam īs. "
        "Tū librum tangis. Tū librum aperīs. "
        "Tū: 'Hae litterae — quid significant?' "
        "Tū nihil intellegis. Sed tū nōn dēsistis. "
        "Tū ad fīlium dominī īs. Fīlius dominī est puer — sīcut tū. "
        "Fīlius: 'Cūr mē spectās?' "
        "Tū: 'Tū legere potes. Ego nōn. Dīc mihi — quid sunt litterae?' "
        "Fīlius: 'Cūr servus legere vult?' "
        "Tū: 'Quia ego quoque homō sum. Ego quoque scīre volō.' "
        "Fīlius tē spectat. Fīlius: 'Nēmō mē hoc rogāvit. "
        "Ego tē docēbō. Sed nēmō scīre dēbet.' "
        "Tū: 'Nēmō sciet.' "
        "Sīc incipit. Nocte, quandō omnēs dormiunt, fīlius tē docet. "
        "Prīmum, litterae: A, B, C. Tum verba: puer, liber, vīta. "
        "Tū legere discis. Tū legere incipis. "
        "Tū: 'Nunc intellegō. Nunc videō.' "
        "Post multās noctēs, tū librum sōlus aperīs. "
        "Tū: 'Ego possum legere. Ego possum intellegere.' "
        "Sed dominus intrat. Dominus tē videt. "
        "Dominus: 'Quid facis? Servus nōn legit!' "
        "Tū: 'Domine, ego... ego nihil faciō.' "
        "Dominus: 'Tū librum habēs! Tū legere scīs!' "
        "Tū: 'Domine, ita. Ego legere possum. "
        "Ego servus sum — sed ego quoque homō sum.' "
        "Dominus tacet. Dominus tē spectat. "
        "Dominus: 'Ego nōn sciēbam. Ego nōn putābam servum velle legere.' "
        "Tū: 'Omnēs volunt legere, domine. Omnēs volunt scīre.' "
        "Dominus: 'Tū... tū potes legere. Sed cum labōre fīnītō.' "
        "Tū: 'Grātiās, domine.' "
        "Nunc tū in hortō sedēs. Nunc tū librum in manibus habēs. "
        "Tū servus es — sed tū līber es. In corde — līber es."
    ),
}

STORIES["cap13_17"] = {
    "title_la": "Quattuor in Aquā",
    "title_zh": "水中四物",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quattuor rēs in aquā sunt: piscis, rāna, serpēns aquae, et puer. "
        "Piscis in aquā natat. Piscis est parvus. Piscis est argenteus. "
        "Piscis: 'Aqua est domus mea. In aquā, ego līber sum. "
        "In aquā, ego omnia videō. Aqua est mundus meus.' "
        "Rāna in aquā et in terrā est. Rāna: 'Ego in duōbus mundīs vīvō. "
        "In aquā, ego natō. In terrā, ego saliō. "
        "Duo mundī sunt melius quam ūnus.' "
        "Serpēns aquae in aquā natat. Serpēns: 'Aqua est domus mea. "
        "Sed ego quoque sōlem amō. Ego in rīpā in sōle dormiō.' "
        "Puer in aquā natat. Puer: 'Aqua est frīgida. Aqua est bona. "
        "In aquā, ego lūdō. In aquā, ego rīdeō. "
        "Sed ego nōn in aquā vīvō. Ego in terrā vīvō.' "
        "Piscis puerum spectat. Piscis: 'Cūr tū nōn in aquā vīvīs?' "
        "Puer: 'Quia ego homō sum. Homō in terrā vīvit.' "
        "Rāna: 'Ego in utrōque vīvō. Hoc est melius.' "
        "Serpēns: 'Ego in utrōque dormiō. Hoc est bonum.' "
        "Puer: 'Vōs omnia potestis. Ego sōlum in aquā natāre possum. "
        "Sed quandō in aquā sum — ego laetus sum.' "
        "Piscis: 'Aqua nōs coniungit. In aquā, nōn est piscis aut rāna aut serpēns aut puer. "
        "In aquā, omnēs sumus... aqua.' "
        "Puer rīdet. Puer: 'Tū es sapiēns, piscis.' "
        "Sōl in caelō est. Aqua lūcet. "
        "Quattuor in aquā sunt — et omnēs sunt laetī."
    ),
}

# ============================================================
# 中长篇 (longior, 500-800 words) x10
# ============================================================

STORIES["cap13_18"] = {
    "title_la": "Quattuor Īnsulae",
    "title_zh": "四岛",
    "target_chapter": 13,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nāvis in marī est. Nāvis quattuor īnsulās petit. "
        "In nāve, senex et iuvenis sunt. Senex est nauta. Iuvenis est discipulus. "
        "Iuvenis: 'Magister, cūr quattuor īnsulās petimus?' "
        "Senex: 'Quia quaeque īnsula aliquid docet. "
        "Prīma īnsula: Crēta. Ibi rēx Mīnōs vīxit. "
        "Mīnōs magnum labyrinthum habuit. "
        "In labyrinthō, mōnstrum fuit. Sed mōnstrum nōn est magnum. "
        "Magnum est quod homō facit — labyrinthum.' "
        "Iuvenis: 'Quid labyrinthus docet?' "
        "Senex: 'Labyrinthus docet: viae multae sunt. "
        "Sed via ad cor — ūna est.' "
        "Nāvis ad Crētam nāvigat. Īnsula est magna. "
        "Iuvenis: 'Crēta est pulchra. Sed ego labyrinthum nōn videō.' "
        "Senex: 'Labyrinthus nōn in terrā est — labyrinthus in corde est.' "
        "Nāvis ad secundam īnsulam nāvigat: Rhodus. "
        "Senex: 'Rhodus est īnsula sōlis. Hīc, Colossus stetit — "
        "statua magna, inter septem mīrācula mundī.' "
        "Iuvenis: 'Ubi est Colossus nunc?' "
        "Senex: 'Cadit. Terra mōvit — et Colossus cadit. "
        "Hoc docet: etiam magna cadunt.' "
        "Nāvis ad tertiam īnsulam nāvigat: Delos. "
        "Senex: 'Delos est īnsula sacra. Hīc, deus nātus est. "
        "Sed nunc Delos est vacua. Nēmō hīc vīvit. "
        "Hoc docet: etiam sacra loca vacua fiunt.' "
        "Iuvenis: 'Tristis est.' "
        "Senex: 'Vīta est trīstis. Sed vīta est quoque pulchra.' "
        "Nāvis ad quārtam īnsulam nāvigat: īnsula parva sine nōmine. "
        "Senex: 'Haec īnsula nōn est in librīs. Nēmō dē eā scrībit. "
        "Sed hīc hominēs vīvunt. Hīc puerī rīdent. Hīc fēminae canunt. "
        "Hoc docet: etiam parvae rēs sunt magnae.' "
        "Iuvenis: 'Intellegō, magister. Quattuor īnsulae — quattuor verba.' "
        "Senex: 'Dīc mihi.' "
        "Iuvenis: 'Crēta: via. Rhodus: cadit. Delos: vacua. "
        "Īnsula sine nōmine: vīta.' "
        "Senex: 'Bene, discipule. Nunc tū es nauta. "
        "Nunc tū potes sōlus nāvigāre.' "
        "Nāvis in mare redit. Senex et iuvenis in caelum spectant. "
        "Stēllae in caelō sunt. Mare est magnum. "
        "Et nāvis — nāvis semper nāvigat."
    ),
}

STORIES["cap13_19"] = {
    "title_la": "Quattuor Partēs Annī",
    "title_zh": "四季",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Annus quattuor partēs habet: vēr, aestās, autumnus, hiems. "
        "Agricola in agrō stat. Agricola terram spectat. "
        "Agricola: 'Vēr venit. Terra est nova. Sēmen in terrā est. "
        "In vēre, omnia incipiunt. In vēre, omnia sunt possibilia.' "
        "Agricola in terrā labōrat. Agricola terram vertit. "
        "Agricola sēmen in terrā pōnit. "
        "Agricola: 'Sēmen est parvum. Sed in sēmine, magnum est. "
        "In sēmine, herba est, frūctus est, vīta est.' "
        "Pluvia venit. Sōl in caelō est. Sēmen crescit. "
        "Aestās venit. Sōl est calidus. Agrī sunt aureī. "
        "Agricola: 'Aestās est tempus labōris. "
        "In aestāte, multum labōrō. Sed labōr meus nōn est vacuus. "
        "In aestāte, videō quod in vēre posuī.' "
        "Agricola frūctūs colligit. Frūctūs sunt multī. "
        "Agricola: 'Terra mihi dat. Terra est bona māter.' "
        "Autumnus venit. Folia in arboribus rubra fiunt. "
        "Agricola: 'Autumnus est tempus colligendī. "
        "In autumnō, omnia quae in annō crevērunt nunc colligō. "
        "Autumnus est tempus grātiārum.' "
        "Agricola in agrō sedet. Agricola frūctūs spectat. "
        "Agricola: 'In autumnō, labōr meus fīnem habet. "
        "Sed terra — terra numquam fīnem habet.' "
        "Hiems venit. Terra est alba. Nix in terrā est. "
        "Agricola: 'Hiems est tempus quiētis. "
        "In hieme, terra dormit. Et ego quoque dormiō. "
        "Sed in terrā, sub nive, sēmen manet. "
        "Sēmen exspectat — exspectat vēr.' "
        "Agricola in vīllā sedet. Agricola ignem spectat. "
        "Agricola: 'Annus quattuor partēs habet. "
        "Vēr: incipiō. Aestās: labōrō. Autumnus: grātiās agō. Hiems: quiēscō. "
        "Et post hiemem — iterum vēr venit. "
        "Vīta semper redit. Vīta semper incipit.' "
        "Agricola in ignem spectat. Extra, nix cadit. "
        "Sed in corde agricolae — vēr iam est."
    ),
}

STORIES["cap13_20"] = {
    "title_la": "Quattuor Partēs Diēī",
    "title_zh": "一日四时",
    "target_chapter": 13,
    "theme": "12 时间",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Diēs quattuor partēs habet: māne, merīdiēs, vesper, nox. "
        "Senex in vīllā sedet. Senex diem spectat. "
        "Māne est. Sōl in caelō surgit. Avēs cantant. "
        "Senex: 'Māne est tempus incipiendī. "
        "In māne, puerī ad ludum eunt. Virī ad labōrem eunt. "
        "In māne, omnia sunt nova. In māne, omnia sunt possibilia.' "
        "Senex in hortum exit. Senex rosās spectat. "
        "Senex: 'Rosae in māne sunt pulchrae. "
        "Rosae in māne sunt novae — sīcut diēs ipse.' "
        "Merīdiēs venit. Sōl in caelō altus est. "
        "Sōl est calidus. Umbrae sunt brevēs. "
        "Senex: 'Merīdiēs est tempus labōris. "
        "In merīdiē, sōl fortis est. Omnēs labōrant. "
        "Sed in merīdiē, nōs nōn vidēmus umbrās. "
        "Fortasse hoc est bonum — nōn vidēre umbrās.' "
        "Senex in hortō sedet. Senex sōlem in cute sentit. "
        "Senex: 'Merīdiēs est fortis. Sed merīdiēs nōn manet. "
        "Sōl semper movētur. Nihil manet.' "
        "Vesper venit. Sōl in caelō descendit. "
        "Caelum est rubrum. Umbrae sunt longae. "
        "Senex: 'Vesper est tempus redeundī. "
        "In vespere, omnēs ad vīllās redeunt. "
        "Labōr fīnem habet. Quiēs venit.' "
        "Senex in caelum spectat. Caelum est pulchrum. "
        "Senex: 'In vespere, sōl valē dīcit. "
        "Sōl nōn trīstis est — sōl scit sē reditūrum esse.' "
        "Nox venit. Stēllae in caelō sunt. Lūna lūcet. "
        "Senex: 'Nox est tempus somnī. "
        "In nocte, omnēs dormiunt. In nocte, mundus tacet. "
        "Sed in nocte, nōs somniāmus. In nocte, alia vīta est.' "
        "Senex in cubiculum it. Senex in lectō iacet. "
        "Senex: 'Māne, merīdiēs, vesper, nox — quattuor partēs diēī. "
        "Et quaeque pars est bona. Quaeque pars est dōnum. "
        "Et post noctem — iterum māne venit. "
        "Diēs semper redit. Diēs semper novus est.' "
        "Senex oculōs claudit. Senex dormit. "
        "Et extra — stēllae in caelō lūcent."
    ),
}

STORIES["cap13_21"] = {
    "title_la": "Quattuor Portae Rōmae",
    "title_zh": "罗马四门",
    "target_chapter": 13,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma multās portās habet. Sed quattuor sunt maximae. "
        "Vir ad prīmam portam stat. Porta est magna. "
        "Vir: 'Haec est porta ad septentriōnem. Per hanc portam, "
        "mīlitēs ad Galliam eunt. Per hanc portam, Caesar exīvit. "
        "Per hanc portam, multī iērunt — et nōn rediērunt.' "
        "Vir per portam spectat. Via est longa. "
        "Vir: 'Porta septentriōnis est porta bellī. "
        "Sed porta septentriōnis est quoque porta fortitūdinis.' "
        "Vir ad secundam portam it. Porta ad orientem est. "
        "Vir: 'Haec est porta ad orientem. Per hanc portam, "
        "mercātōrēs ad Graeciam et Asiam eunt. "
        "Per hanc portam, multae rēs intrant — sīricum, aromata, gemmae.' "
        "Vir mercātōrēs spectat. Vir: 'Porta orientis est porta dīvitiārum. "
        "Sed porta orientis est quoque porta cupiditātis.' "
        "Vir ad tertiam portam it. Porta ad merīdiem est. "
        "Vir: 'Haec est porta ad merīdiem. Per hanc portam, "
        "agricolae ad agrōs eunt. Per hanc portam, "
        "frūmentum in urbem intrat. Pānis Rōmae per hanc portam venit.' "
        "Vir agricolās spectat. Vir: 'Porta merīdiēī est porta vītae. "
        "Sine hāc portā, Rōma nōn edit. "
        "Porta merīdiēī est porta labōris.' "
        "Vir ad quārtam portam it. Porta ad occidentem est. "
        "Vir: 'Haec est porta ad occidentem. Per hanc portam, "
        "viātōrēs ad Hispāniam eunt. Per hanc portam, "
        "sōl in mare cadit.' "
        "Vir in caelum spectat. Sōl descendit. "
        "Vir: 'Porta occidentis est porta fīnis. "
        "Sed porta occidentis est quoque porta quiētis.' "
        "Vir in mediā urbe stat. Vir: 'Quattuor portae — "
        "septentriō, oriēns, merīdiēs, occidēns. "
        "Bellum, dīvitiae, vīta, quiēs. "
        "Rōma omnia habet. Rōma est mundus.' "
        "Nox venit. Portae clauduntur. "
        "Sed Rōma — Rōma numquam clauditur."
    ),
}

STORIES["cap13_22"] = {
    "title_la": "Quīnque Oppida Hispāniae",
    "title_zh": "西班牙五城",
    "target_chapter": 13,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mercātor ex Hispāniā Rōmam redit. Mercātor multās terrās vīdit. "
        "Amīcus: 'Dīc mihi dē Hispāniā! Quālēs sunt oppida eius?' "
        "Mercātor: 'Quīnque oppida vīdī. Quīnque oppida — quīnque mundī. "
        "Prīmum: Tarracō. Tarracō in marī est. "
        "In Tarracōne, portus magnus est. Nāvēs ex omnibus terrīs veniunt. "
        "In forō, mercēs ex Āfricā et Hispāniā et Italiā sunt. "
        "Tarracō est porta Hispāniae.' "
        "Amīcus: 'Estne pulchra?' "
        "Mercātor: 'Pulchra est. Sed Tarracō est multa — "
        "multī hominēs, multae linguae, multae rēs. "
        "Secundum: Corduba. Corduba in mediā terrā est. "
        "Corduba est urbs flūminis. Flūmen magnum per urbem fluit. "
        "In Cordubā, multī philosophī sunt. Multī librī. "
        "Corduba est urbs sapientiae.' "
        "Amīcus: 'Philosophī in Hispāniā?' "
        "Mercātor: 'Ita. Hispānia nōn est sōlum terra bellī. "
        "Hispānia est quoque terra mentis. "
        "Tertium: Hispalis. Hispalis prope flūmen magnum est. "
        "In Hispale, multum frūmentum est. "
        "Agrī circum urbem sunt aureī. "
        "Hispalis est urbs cibī — Hispalis Rōmam alit.' "
        "Amīcus: 'Et quārtum?' "
        "Mercātor: 'Quārtum: Nova Carthāgō. "
        "Nova Carthāgō est urbs antīqua. "
        "Hīc, Poenī fuērunt — ante Rōmānōs. "
        "Nunc Rōmānī hīc sunt. Sed memoria Poenōrum manet. "
        "Nova Carthāgō est urbs memoriae.' "
        "Amīcus: 'Et quīntum?' "
        "Mercātor: 'Quīntum: parvum oppidum in montibus. "
        "Nōmen eius nōn meminī. Sed in hōc oppidō, "
        "virī et fēminae in viīs rīdent. Puerī in forō lūdunt. "
        "In hōc oppidō, vīta est simplicior — sed bona.' "
        "Amīcus: 'Quod oppidum tibi placet maximē?' "
        "Mercātor: 'Omnia. Quia in omnibus — hominēs sunt. "
        "Et hominēs, ubīque, sunt similēs.' "
        "Mercātor tacet. Mercātor in caelum spectat. "
        "Mercātor: 'Hispānia est longē. Sed Hispānia est in corde meō.'"
    ),
}

STORIES["cap13_23"] = {
    "title_la": "Quīnque Terrae Asiae",
    "title_zh": "亚洲五地",
    "target_chapter": 13,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Dux Rōmānus ex Asiā redit. Dux multās terrās vīdit. "
        "In forō, virī eum rogant: 'Dīc nōbīs dē Asiā! Quālēs sunt terrae eius?' "
        "Dux: 'Quīnque terrās vīdī. Quīnque terrae — quīnque rēgēs. "
        "Prīma: Asia Minor. Asia Minor est terra antīqua. "
        "Hīc, Graecī fuērunt. Hīc, Trōia fuit. Hīc, Alexander Magnus pugnāvit. "
        "Nunc Rōmānī hīc sunt. Sed terra meminit. "
        "Terra semper meminit omnēs quī in eā fuērunt.' "
        "Vir: 'Estne dīves?' "
        "Dux: 'Dīves est. In Asiā Minōre, multae urbēs sunt — "
        "Ephesus, Pergamum, Milētus. "
        "In hīs urbibus, multum aurum est. Multī mercātōrēs. "
        "Sed dīvitiae nōn sunt omnia.' "
        "Dux: 'Secunda: Syria. Syria est terra inter duo maria. "
        "In Syriā, multae linguae sunt. Multī deī. "
        "In Syriā, mercēs ex oriente veniunt — "
        "sīricum, aromata, gemmae. "
        "Syria est porta ad orientem.' "
        "Dux: 'Tertia: Iūdaea. Iūdaea est terra parva. Sed Iūdaea est terra magna. "
        "In Iūdaeā, ūnus deus est. Populus Iūdaeōrum ūnum deum colit. "
        "Hoc est mīrum — sed hoc est pulchrum. "
        "Iūdaea est terra fideī.' "
        "Dux: 'Quārta: Aegyptus. Aegyptus est terra Nīlī. "
        "Nīlus est pater Aegyptī. Sine Nīlō, Aegyptus nōn est. "
        "In Aegyptō, multae pyrāmidēs sunt — monumenta antīqua. "
        "Aegyptus est terra aeternitātis.' "
        "Dux: 'Quīnta: terra longē in oriente. "
        "Nōmen eius nōn sciō. Sed ibi hominēs sīricum faciunt. "
        "Ibi hominēs pācem amant. Ibi hominēs nōn bellum volunt. "
        "Haec terra est terra pācis.' "
        "Vir: 'Quae terra tibi placet maximē?' "
        "Dux: 'Omnēs. Quia in omnibus terrīs, hominēs vīvunt. "
        "Et in omnibus terrīs, hominēs eadem volunt — "
        "pānem, pācem, amōrem. "
        "Asiam vīdī — et Rōmam melius intellegō.'"
    ),
}

STORIES["cap13_24"] = {
    "title_la": "Quīnque Terrae",
    "title_zh": "五片土地",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Agricola quīnque terrās habet. Agricola in colle stat. "
        "Agricola: 'Quīnque terrae — quīnque fīliī. "
        "Quaeque terra suam fābulam habet.' "
        "Fīlius prīmus: 'Pater, dīc nōbīs dē terrīs!' "
        "Agricola: 'Prīma terra est in valle. Terra est nigra. "
        "In hāc terrā, frūmentum crescit. Frūmentum est altum. "
        "In hāc terrā, multum labōrāvī. Sed terra mihi multum dat. "
        "Haec terra est terra labōris.' "
        "Fīlius secundus: 'Et secunda terra?' "
        "Agricola: 'Secunda terra est in colle. Terra est rubra. "
        "In hāc terrā, vīneae sunt. Ūvae in sōle crescunt. "
        "Ex hīs ūvīs, vīnum facimus. "
        "Haec terra est terra gaudiī.' "
        "Fīlius tertius: 'Et tertia terra?' "
        "Agricola: 'Tertia terra est prope fluvium. Terra est umida. "
        "In hāc terrā, holera crescunt. In hāc terrā, herbae sunt. "
        "Haec terra est terra cibī.' "
        "Fīlius quārtus: 'Et quārta terra?' "
        "Agricola: 'Quārta terra est in silvā. Terra est sub arboribus. "
        "In hāc terrā, porcī sunt. In hāc terrā, avēs sunt. "
        "Haec terra est terra animālium.' "
        "Fīlius quīntus: 'Et quīnta terra?' "
        "Agricola tacet. Agricola in caelum spectat. "
        "Agricola: 'Quīnta terra est parva. Quīnta terra est in colle altō. "
        "In hāc terrā, nihil crescit. Terra est sicca. "
        "Sed in hāc terrā, sōl pulcher est. "
        "In hāc terrā, ego sedeō et caelum spectō. "
        "Haec terra nōn dat cibum. Sed haec terra dat... pācem.' "
        "Fīliī tacent. Fīliī patrem spectant. "
        "Fīlius prīmus: 'Intellegō, pater. "
        "Nōn omnēs terrae sunt ad labōrem. "
        "Aliquae terrae sunt ad cor.' "
        "Agricola: 'Ita, fīlī. Quīnque terrae — quīnque dōna. "
        "Et quandō ego nōn iam erō — vōs hās terrās habēbitis. "
        "Servāte eās. Amāte eās. Sīcut ego amāvī.' "
        "Sōl in caelō descendit. Agricola et fīliī in colle stant. "
        "Quīnque terrae sub eīs sunt. Et omnia sunt bona."
    ),
}

STORIES["cap13_25"] = {
    "title_la": "Senātor et Populus",
    "title_zh": "元老与人民",
    "target_chapter": 13,
    "theme": "06 权力",
    "style": "雄辩",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Senātor in forō stat. Senātor ad populum dīcit. "
        "Senātor: 'Populus Rōmānus! Ego vōs convocāvī quia magnum est quod dīcō. "
        "Urbs nostra in perīculō est. Hostēs ad portās sunt. "
        "Sed nōn hostēs externī — hostēs internī. "
        "Hostēs in cordibus nostrīs sunt.' "
        "Populus tacet. Populus senātōrem spectat. "
        "Senātor: 'Nōs dīvitiās amāmus plūs quam virtūtem. "
        "Nōs potentiās amāmus plūs quam populum. "
        "Nōs nōs ipsōs amāmus plūs quam Rōmam. "
        "Et hoc est perīculum.' "
        "Vir ex populō: 'Tū ipse es senātor! Tū ipse dīves es! "
        "Cūr tū nōbīs dē hīs rēbus dīcis?' "
        "Senātor: 'Bene rogās. Ego quoque in hōc perīculō sum. "
        "Ego quoque dīvitiās amō. Ego quoque potentiam amō. "
        "Sed ego videō — et ego dīcō. "
        "Melius est vidēre et dīcere quam nōn vidēre et tacēre.' "
        "Fēmina ex populō: 'Quid dēbēmus facere?' "
        "Senātor: 'Nōn est facile. Nōn est 'fac hoc, fac illud.' "
        "Sed prīmum: vidēte. Vidēte quod in urbe fit. "
        "Vidēte pauperēs in viīs. Vidēte puerōs sine cibō. "
        "Vidēte senēs sine vīllīs. "
        "Et quandō vidētis — nōn potestis nōn facere.' "
        "Senex ex populō: 'Ego multōs annōs in urbe vīvō. "
        "Ego multōs senātōrēs audīvī. Omnēs dīcunt — paucī faciunt.' "
        "Senātor: 'Vērum dīcis. Sed ego nōn sōlum dīcō. "
        "Ego hodiē in forō dō. Ego frūmentum meum ad pauperēs dō. "
        "Ego pecūniam meam ad puerōs dō. "
        "Ego nōn omnia possum — sed ego aliquid possum.' "
        "Populus movētur. Aliquī rīdent. Aliquī plōrant. "
        "Senātor: 'Rōma nōn est mūrī. Rōma nōn est templa. "
        "Rōma est populus. Et quandō populus stat — Rōma stat. "
        "Et quandō populus cadit — Rōma cadit.' "
        "Senātor in forō manet. Populus lentē abit. "
        "Sed in cordibus — verba senātōris manent. "
        "Et fortasse — fortasse aliquid mūtātur."
    ),
}

STORIES["cap13_26"] = {
    "title_la": "Septem Diēs Hebdomadis",
    "title_zh": "一周七日",
    "target_chapter": 13,
    "theme": "12 时间",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hebdomas septem diēs habet. Vir in vīllā suā sedet. "
        "Vir: 'Septem diēs — septem dōna. Quisque diēs suum dōnum habet.' "
        "Diēs prīmus: diēs Sōlis. Vir: 'Hodiē est diēs Sōlis. "
        "Sōl in caelō altus est. Sōl est dōnum lūcis. "
        "In hōc diē, nōs quiēscimus. In hōc diē, nōs ad templum īmus. "
        "In hōc diē, nōs nōn labōrāmus — sed vīvimus.' "
        "Diēs secundus: diēs Lūnae. Vir: 'Hodiē est diēs Lūnae. "
        "Lūna in nocte lūcet. Lūna est dōnum noctis. "
        "In hōc diē, nōs incipimus. Labōr incipit. Via incipit. "
        "Diēs Lūnae est diēs incipiendī.' "
        "Diēs tertius: diēs Mārtis. Vir: 'Hodiē est diēs Mārtis. "
        "Mārs est deus bellī. Sed bellum nōn est dōnum. "
        "Fortitūdō est dōnum. In hōc diē, nōs fortēs sumus. "
        "Nōs difficilia facimus. Nōs nōn fugimus.' "
        "Diēs quārtus: diēs Mercuriī. Vir: 'Hodiē est diēs Mercuriī. "
        "Mercurius est deus mercātōrum. "
        "In hōc diē, nōs mercēs vēndimus et emimus. "
        "In hōc diē, nōs cum aliīs hominibus loquimur. "
        "Diēs Mercuriī est diēs commerciī.' "
        "Diēs quīntus: diēs Iovis. Vir: 'Hodiē est diēs Iovis. "
        "Iuppiter est deus caelī. Iuppiter est dōnum magnitūdinis. "
        "In hōc diē, nōs magna cōgitāmus. "
        "Nōs nōn sōlum parva vidēmus — nōs caelum spectāmus.' "
        "Diēs sextus: diēs Veneris. Vir: 'Hodiē est diēs Veneris. "
        "Venus est dea amōris. Amor est dōnum. "
        "In hōc diē, nōs amāmus. Nōs familiās nostrās amāmus. "
        "Nōs amīcōs nostrōs amāmus. Nōs vītam amāmus.' "
        "Diēs septimus: diēs Sāturnī. Vir: 'Hodiē est diēs Sāturnī. "
        "Sāturnus est deus temporis. Tempus est dōnum. "
        "In hōc diē, nōs quiēscimus. In hōc diē, nōs ad hortum īmus. "
        "In hōc diē, nōs meminimus — septem diēs iērunt. "
        "Sed septem diēs iterum venient.' "
        "Vir: 'Septem diēs — septem dōna. "
        "Lūx, initium, fortitūdō, commercium, magnitūdō, amor, quiēs. "
        "Et haec est vīta.' "
        "Sōl in caelō descendit. Diēs fīnem habet. "
        "Sed crās — novus diēs veniet."
    ),
}

STORIES["cap13_27"] = {
    "title_la": "Trēs Flūmina",
    "title_zh": "三条河流",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Trēs flūmina sunt in imperiō Rōmānō: Tiberis, Padus, Rhēnus. "
        "Vir in viā est. Vir trēs flūmina vīdit. "
        "Amīcus: 'Dīc mihi dē flūminibus! Quālēs sunt?' "
        "Vir: 'Tiberis est parvus. Tiberis per Rōmam fluit. "
        "Tiberis est flūmen Rōmānum. In Tiberī, puerī natant. "
        "In Tiberī, nāviculae sunt. "
        "Tiberis nōn est magnus — sed Tiberis est Rōmānus. "
        "Tiberis est initium. Sine Tiberī, Rōma nōn esset.' "
        "Amīcus: 'Et Padus?' "
        "Vir: 'Padus est longus. Padus per Italiam septentriōnālem fluit. "
        "Padus est pater Italiae. Agrī circum Padum sunt pulchrī. "
        "In agrīs, frūmentum crescit. In agrīs, vīneae sunt. "
        "Padus est flūmen vītae.' "
        "Amīcus: 'Et Rhēnus?' "
        "Vir: 'Rhēnus est magnus. Rhēnus est līmes imperiī. "
        "In ūnā rīpā, Rōmānī sunt. In alterā rīpā, Germānī sunt. "
        "Rhēnus est mūrus — sed mūrus aquae. "
        "Rhēnus dīcit: 'Hūc usque Rōma. Nōn longius.' "
        "Sed Rhēnus est quoque via. Nāvēs in Rhēnō nāvigant. "
        "Mercēs in Rhēnō portantur. "
        "Rhēnus est flūmen līmitis.' "
        "Amīcus: 'Quod flūmen tibi placet maximē?' "
        "Vir: 'Tiberis. Tiberis est parvus — sed Tiberis est meus. "
        "In Tiberī, ego puer natābam. In rīpīs Tiberis, ego cum amīcīs lūdēbam. "
        "Tiberis nōn est maximus — sed Tiberis est in corde meō.' "
        "Amīcus: 'Intellegō. Flūmen nōn est sōlum aqua. "
        "Flūmen est memoria. Flūmen est amor.' "
        "Vir: 'Ita. Trēs flūmina — trēs mundī. "
        "Sed ūnum flūmen est in corde meō.' "
        "Sōl in caelō est. Aqua in flūminibus fluit. "
        "Et flūmina — flūmina semper ad mare eunt."
    ),
}

# ============================================================
# 长篇 (longus, 800+ words) x6
# ============================================================

STORIES["cap13_28"] = {
    "title_la": "Tria Oppida Italiae",
    "title_zh": "意大利三城",
    "target_chapter": 13,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tria oppida in Italiā sunt: Rōma, Capua, Pompēiī. "
        "Tria oppida — trēs faciēs Italiae. "
        "Vir Rōmānus ex urbe in urbem it. Vir: 'Ego tria oppida vidēbō. "
        "Ego faciem Italiae inveniam.' "
        "Prīmum: Rōma. Rōma est caput mundī. "
        "In Rōmā, multī hominēs sunt. Multae vīllae, multa templa, multae viae. "
        "In forō Rōmānō, virī dīcunt, mercēs vēnduntur, lēgēs fīunt. "
        "Vir: 'Rōma est magna. Rōma est fortis. Rōma est aeterna. "
        "Sed Rōma est quoque multa — nimis multa. "
        "In Rōmā, homō potest sē perdere.' "
        "Vir in viīs Rōmae ambulat. Vir: 'In Rōmā, omnēs currunt. "
        "Nēmō stat. Nēmō spectat. Nēmō audit. "
        "Rōma est urbs quae numquam dormit — sed numquam vīvit.' "
        "Vir ex urbe exit. Vir ad Capuam it. "
        "Capua est in merīdiē. Capua est urbs campōrum. "
        "In Capuā, agrī sunt magnī. In Capuā, equī sunt pulchrī. "
        "Vir: 'Capua est alia. In Capuā, hominēs nōn currunt. "
        "In Capuā, hominēs sedent. In Capuā, hominēs vīvunt.' "
        "Vir in forō Capuae sedet. Vir hominēs spectat. "
        "Vir: 'In Capuā, vita est lentior. Sed lentus nōn est malus. "
        "Lentus est... bonus.' "
        "Vir ex Capuā exit. Vir ad Pompēiōs it. "
        "Pompēiī prope mare sunt. Pompēiī sub monte sunt. "
        "Mōns est magnus. Mōns est Vesuvius. "
        "Vir: 'Pompēiī sunt pulchrī. Mare est caeruleum. Caelum est clārum. "
        "Sed mōns... mōns est perīculōsus.' "
        "In Pompēiīs, hominēs in viīs ambulant. Puerī in forō lūdunt. "
        "Fēminae in hortīs sedent. Omnēs rīdent. "
        "Vir: 'Pompēiī sunt urbēs gaudiī. Sed sub monte... "
        "semper est perīculum.' "
        "Vir senem in forō videt. Senex: 'Cūr trīstis es, viātor?' "
        "Vir: 'Mōns... mōns mē terret.' "
        "Senex: 'Mōns est mōns. Mōns semper hīc fuit. "
        "Mōns nōs terret — sed mōns nōs quoque alit. "
        "Terra circum montem est fertilis propter montem. "
        "Quod nōs terret, idem nōs alit.' "
        "Vir: 'Intellegō. Tria oppida — trēs faciēs. "
        "Rōma: potentia. Capua: quiēs. Pompēiī: gaudium cum perīculō. "
        "Et omnia sunt Italia. Et omnia sunt vīta.' "
        "Vir in viā est. Vir ad Rōmam redit. "
        "Sed in corde, tria oppida manent. "
        "Et vir intellegit: nōn est ūnum oppidum. "
        "Vīta est multa — sīcut Italiae oppida."
    ),
}

STORIES["cap13_29"] = {
    "title_la": "Via ad Urbem",
    "title_zh": "通往城市之路",
    "target_chapter": 13,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Via ad urbem longa est. Via per campōs, per silvās, per flūmina dūcit. "
        "Puer in viā est. Puer sōlus est. Pater eius in urbe est. "
        "Puer: 'Pater meus in urbe labōrat. Pater meus mē numquam videt. "
        "Ego ad urbem eō. Ego patrem meum vidēbō.' "
        "Puer in viā ambulat. Diēs est calidus. Sōl in caelō est. "
        "Puer parvus aquam bibit. Puer pānem edit. "
        "Puer: 'Via est longa. Sed ego nōn dēsistō. "
        "Pater meus mē exspectat — etsī nescit.' "
        "Puer per campōs it. In campīs, herbae sunt altae. "
        "Puer herbās tangit. Puer: 'Herbae sunt mollēs. "
        "Herbae sunt sīcut manus mātris — mollēs et bonae.' "
        "Puer per silvam it. In silvā, arborēs sunt altae. "
        "Puer: 'Arborēs sunt magnae. Arborēs ad caelum spectant. "
        "Fortasse arborēs quoque aliquid volunt — sed nōn possunt īre.' "
        "Puer per flūmen it. Pōns in fluviō est. "
        "Puer in ponte stat. Puer aquam spectat. "
        "Puer: 'Aqua semper fluit. Aqua numquam manet. "
        "Aqua semper ad mare it — sīcut ego ad urbem eō.' "
        "Vesperī venit. Sōl in caelō descendit. "
        "Puer fessus est. Puer sub arbore sedet. "
        "Puer: 'Nox venit. Dēbeō dormīre.' "
        "Puer in terrā dormit. Stēllae in caelō sunt. "
        "Puer in somnīs patrem videt. Pater: 'Fīlī, cūr hīc es?' "
        "Puer: 'Pater, ego ad tē veniō.' "
        "Pater: 'Via est longa. Via est perīculōsa. Cūr vēnistī?' "
        "Puer: 'Quia tū mē numquam vidēs. Quia ego tē vidēre volō.' "
        "Pater: 'Fīlī... ego semper tē videō. In corde meō — tū semper es.' "
        "Māne venit. Puer oculōs aperit. Puer surgit. "
        "Puer iterum in viā est. Puer: 'Pater meus in urbe est. "
        "Ego eum vidēbō.' "
        "Post multōs diēs, puer urbem videt. "
        "Puer: 'Urbs! Ecce — urbs!' "
        "Puer in urbem currit. Urbs est magna. Urbs est multa. "
        "Puer patrem quaerit. Puer: 'Ubi est pater meus?' "
        "Puer in viīs urbis ambulat. Multī hominēs in viīs sunt. "
        "Sed nēmō puerum spectat. Nēmō puerum audit. "
        "Puer: 'Pater! Ubi es?' "
        "Tum — puer patrem videt. Pater in viā stat. "
        "Pater puerum videt. Pater: 'Fīlī! Tū hīc es!' "
        "Puer ad patrem currit. Puer patrem tangit. "
        "Puer: 'Pater, ego vēnī. Via longa fuit — sed ego vēnī.' "
        "Pater: 'Fīlī... tū vēnistī. Tū mē invēnistī.' "
        "Pater et fīlius in viā stant. Circum eōs, urbs est magna. "
        "Sed inter eōs — nihil est magnum. Sōlum amor."
    ),
}

STORIES["cap13_30"] = {
    "title_la": "Via Sine Fīne",
    "title_zh": "无尽之路",
    "target_chapter": 13,
    "theme": "27 旅行",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "商人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mercātor in viā est. Mercātor multōs annōs in viā est. "
        "Mercātor: 'Ego multās terrās vīdī. Ego multās urbēs vīdī. "
        "Ego multōs hominēs vīdī. Sed via — via numquam fīnem habet.' "
        "Mercātor in viā ambulat. Via est longa. Via est pulchra. "
        "Mercātor: 'Quandō ego iuvenis eram, putābam viam habēre fīnem. "
        "Putābam post ultimum collem esse urbem, post ultimum flūmen esse mare. "
        "Sed nunc videō: post omnem collem est alius collis. "
        "Post omne flūmen est aliud flūmen. Via numquam fīnitur.' "
        "Mercātor sub arbore sedet. Mercātor aquam bibit. "
        "Mercātor: 'Via est magistra. Via docet: nōn est fīnis. "
        "Fīnis est sōlum in corde. Quandō cor dīcit 'satis' — tum via fīnitur.' "
        "Viātor ad mercātōrem venit. Viātor: 'Quō īs, mercātor?' "
        "Mercātor: 'Nesciō. Ego sōlum eō.' "
        "Viātor: 'Cūr īs, sī nescīs quō?' "
        "Mercātor: 'Quia via est vīta. Stāre est morī. Īre est vīvere.' "
        "Viātor: 'Sed nōnne fessus es?' "
        "Mercātor: 'Fessus sum. Sed fessus nōn est malus. "
        "Fessus significat tē vīxisse.' "
        "Viātor cum mercātōre it. Viātor: 'Dīc mihi dē terrīs quās vīdistī.' "
        "Mercātor: 'Vīdī Graeciam — terram sapientiae. "
        "Vīdī Aegyptum — terram aeternitātis. "
        "Vīdī Hispāniam — terram fortitūdinis. "
        "Vīdī Galliam — terram bellī. "
        "Vīdī Asiam — terram mīrāculōrum. "
        "Sed omnēs terrae sunt similēs. In omnibus terrīs, hominēs sunt. "
        "In omnibus terrīs, hominēs amant, timent, spērant, plōrant. "
        "Terrae sunt differentēs — sed hominēs sunt iīdem.' "
        "Viātor: 'Et tū? Quis es tū?' "
        "Mercātor: 'Ego sum mercātor. Ego mercēs portō. "
        "Sed nunc videō: mercēs nōn sunt magnae. "
        "Magnum est via. Magnum est vidēre. Magnum est vīvere.' "
        "Viātor: 'Quid est maximum quod vīdistī?' "
        "Mercātor: 'Mare. Mare est magnum. Mare est sine fīne. "
        "Mare est sīcut via — numquam fīnitur. "
        "Sed mare est quoque sīcut cor — semper movētur, semper vīvit.' "
        "Mercātor et viātor in viā ambulant. Sōl in caelō descendit. "
        "Mercātor: 'Nox venit. Nōs dormiēmus. Crās iterum ībimus.' "
        "Viātor: 'Quō ībimus?' "
        "Mercātor: 'Nesciō. Sed via nōs dūcet. Via semper dūcit.' "
        "Mercātor et viātor sub arbore dormiunt. "
        "Stēllae in caelō sunt. Via sub stēllīs iacet. "
        "Et crās — via iterum eōs vocābit."
    ),
}

STORIES["cap13_31"] = {
    "title_la": "Viātor et Nox",
    "title_zh": "旅人与夜",
    "target_chapter": 13,
    "theme": "22 旅程",
    "style": "抒情",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Nox est. Ego in viā sum. Ego sōlus sum. "
        "Ego multās noctēs in viā fuī. Sed haec nox est alia. "
        "Haec nox est nigra. Nūlla lūna in caelō est. Nūllae stēllae. "
        "Ego: 'Caelum hodiē est nigrum. Caelum hodiē nihil dat. "
        "Sed fortasse hoc est bonum. Fortasse in nigrō, plūs videō.' "
        "Ego in viā ambulō. Ego nōn videō quō eam. "
        "Sed ego eō. Ego semper eō. "
        "Ego: 'Via est sīcut vīta. Nōn semper vidēs quō īs. "
        "Sed tū īs. Tū semper īs.' "
        "Ego sonōs noctis audiō. Ventus in arboribus. "
        "Aqua in fluviō. Canis longē lātrat. "
        "Ego: 'Nox nōn tacet. Nox habet suam vōcem. "
        "Sed nōs in diē nōn audīmus — quia nōs nimis multa facimus. "
        "In nocte, nōs audīmus. In nocte, nōs sumus.' "
        "Ego in terrā sedeō. Ego in caelum spectō. "
        "Caelum est nigrum. Sed nōn est vacuum. "
        "Post nūbēs, stēllae sunt. Ego hoc sciō. "
        "Ego: 'Stēllae semper in caelō sunt — etiam quandō nōn vidēs. "
        "Sīcut amor. Sīcut spēs. Sīcut vīta.' "
        "Ego dē vītā meā cōgitō. Ego dē viīs quās īvī. "
        "Ego dē hominibus quōs vīdī. Ego dē terrīs quās vīdī. "
        "Ego: 'Omnia sunt via. Omnia sunt nox. "
        "Et in nocte, in viā — ego sum. Ego sōlus sum. "
        "Sed sōlus nōn est vacuus. Sōlus est... plēnus.' "
        "Ego in terrā iaceō. Ego oculōs claudō. "
        "Ego: 'Fortasse in nocte, nōs nōn dormīmus — sed vigilāmus. "
        "Fortasse nox est vērum tempus — et diēs est somnium.' "
        "Ego nihil videō. Sed ego omnia sentiō. "
        "Terram sub mē. Ventum in cute. Cor in pectore. "
        "Ego: 'Vīvus sum. Hoc est magnum. Hoc est satis.' "
        "Māne venit. Prīma lūx in caelō est. "
        "Nūbēs aperiuntur. Stēllae abeunt. Sōl venit. "
        "Ego surgō. Ego iterum in viā sum. "
        "Ego: 'Nox abiit. Sed nox mē mūtāvit. "
        "Nox mē docuit: etiam in nigrō, est lūx. "
        "Etiam in silentiō, est vōx. Etiam in sōlitūdine, est amor.' "
        "Ego in viā ambulō. Diēs est novus. Via est nova. "
        "Ego quoque novus sum. "
        "Et ego sciō: quandō nox iterum veniet — ego nōn timēbō. "
        "Quia nox nōn est hostis. Nox est amīca."
    ),
}

STORIES["cap13_32"] = {
    "title_la": "Vōx Arboris",
    "title_zh": "树之声",
    "target_chapter": 13,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "B 神话与传说",
    "character_type": "拟人自然",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum arbor. Ego in silvā stō. Ego multōs annōs hīc stō. "
        "Ego multa vīdī. Ego multa audīvī. Ego multa meminī. "
        "Ego: 'Hominēs veniunt et abeunt. Sed ego maneō. "
        "Ego videō omnēs — sed nēmō mē videt.' "
        "Ego in caelum spectō. Ego folia mea ad sōlem extendō. "
        "Ego: 'Sōl est amīcus meus. Sōl mihi cibum dat. "
        "Sōl mē calidum facit. Sōl mē vivum tenet.' "
        "Ego in terram spectō. Ego rādīcēs meās in terrā habeō. "
        "Ego: 'Terra est māter mea. Terra mē tenet. Terra mē alit. "
        "Sine terrā, ego nōn stārem. Sine terrā, ego nōn vīverem.' "
        "Avēs in rāmīs meīs nīdōs faciunt. Avēs in rāmīs meīs cantant. "
        "Ego: 'Avēs sunt fīliae meae. Avēs mihi cārmen dant. "
        "Avēs mē nōn relinquunt.' "
        "Ventus per folia mea flat. Ventus mē movet. "
        "Ego: 'Ventus est frāter meus. Ventus mihi fābulās nārrat. "
        "Ventus mihi dē terrīs longinquīs dīcit. "
        "Ventus omnia videt — et omnia mihi dīcit.' "
        "Pluvia venit. Pluvia mē lavat. Pluvia mihi aquam dat. "
        "Ego: 'Pluvia est soror mea. Pluvia mē novam facit. "
        "Pluvia terram meam umidam facit. Pluvia est vīta.' "
        "Hominēs ad mē veniunt. Hominēs sub mē sedent. "
        "Hominēs in umbrā meā quiēscunt. "
        "Ego: 'Hominēs sunt parvī. Hominēs sunt brevēs. "
        "Hominēs veniunt et abeunt — sīcut folia in autumnō. "
        "Sed hominēs sunt pulchrī. Hominēs amant, rīdent, plōrant. "
        "Hominēs vīvunt — breviter, sed fortiter.' "
        "Puer ad mē venit. Puer in trunco meō nōmen scrībit. "
        "Ego: 'Puer, cūr nōmen tuum in mē scrībis?' "
        "Puer: 'Ut nōn moriar. Ut aliquis meminerit.' "
        "Ego: 'Ego meminī. Ego semper meminī. "
        "Omnia nōmina in mē scrīpta — ego meminī. "
        "Omnēs hominēs sub mē sedentēs — ego meminī.' "
        "Puer abit. Puer crescit. Puer senex fit. "
        "Senex ad mē redit. Senex nōmen suum in trunco meō videt. "
        "Senex: 'Nōmen meum adhūc hīc est. Ego adhūc hīc sum.' "
        "Ego: 'Tū adhūc hīc es. Et quandō tū nōn iam eris — "
        "nōmen tuum in mē manēbit. Ego meminerō.' "
        "Senex sub mē sedet. Senex oculōs claudit. "
        "Senex nōn iam surgit. "
        "Ego senem in umbrā meā teneō. Ego senem custōdiō. "
        "Ego: 'Quiēsce, amīce. Ego tē teneō. Ego tē meminī. "
        "Et in foliīs meīs, in rāmīs meīs, in rādīcibus meīs — "
        "tū semper eris. Quia ego sum arbor. Et ego semper meminī.' "
        "Ventus flat. Folia mea moventur. Sōl in caelō est. "
        "Et ego stō. Ego semper stō."
    ),
}

STORIES["cap13_33"] = {
    "title_la": "Ancilla et Lūna",
    "title_zh": "女奴与月亮",
    "target_chapter": 13,
    "theme": "02 爱与欲望",
    "style": "抒情",
    "genre": "B 神话与传说",
    "character_type": "奴隶",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Ancilla in vīllā est. Ancilla est serva. Ancilla in vīllā labōrat. "
        "In diē, ancilla aquam portat. Ancilla cibum facit. Ancilla vīllam lavat. "
        "Ancilla: 'In diē, ego sum serva. In diē, ego sum nihil. "
        "Sed in nocte — in nocte, ego sum... ego.' "
        "Nocte, quandō omnēs dormiunt, ancilla in hortum exit. "
        "Ancilla in caelum spectat. Lūna in caelō est. "
        "Lūna est magna. Lūna est pulchra. Lūna est alba. "
        "Ancilla: 'Lūna, tū sōla in caelō es — sīcut ego. "
        "Sed tū es lībera. Tū in caelō nāvigās. "
        "Ego in terrā sum — et ego serva sum.' "
        "Ancilla in hortō sedet. Ancilla lūnam spectat. "
        "Ancilla: 'Lūna, tū mē vidēs? Tū mē amās?' "
        "Lūna nihil dīcit. Sed lūna lūcet. "
        "Ancilla: 'Lūx tua est mollis. Lūx tua est bona. "
        "Lūx tua mē tangit — sīcut nēmō mē tangit.' "
        "Ancilla ad lūnam manūs extendit. "
        "Ancilla: 'Lūna, tū es longē. Sed tū es prope. "
        "Tū es in caelō — sed tū es in corde meō.' "
        "Sīc multae noctēs eunt. Ancilla omni nocte ad hortum exit. "
        "Ancilla omni nocte lūnam spectat. "
        "Ancilla: 'Lūna, tū mē nōn dēseris. "
        "In diē, dominus mē verberat. Domina mē maledīcit. "
        "Sed in nocte, tū mē cōnsōlāris. Tū mē amās.' "
        "Ūnā nocte, ancilla in hortō lacrimat. "
        "Ancilla: 'Lūna, ego nōn iam possum. "
        "Ego nōn iam possum serva esse. "
        "Ego volō lībera esse — sīcut tū.' "
        "Tum, aliquid mīrum fit. Lūna venit. "
        "Lūna ex caelō descendit. Lūna in hortō stat. "
        "Lūna est fēmina. Fēmina est alba. Fēmina est pulchra. "
        "Lūna: 'Ancilla, tū mē multās noctēs vocāvistī. "
        "Tū mē amāvistī. Et ego tē amō.' "
        "Ancilla: 'Lūna! Tū vēnistī! Tū mē audīvistī!' "
        "Lūna: 'Ego tē semper audiō. Ego tē semper videō. "
        "Et nunc — ego tē līberō.' "
        "Lūna ancillam tangit. Ancilla lūcem sentit. "
        "Ancilla: 'Ego... ego nōn iam serva sum. Ego lībera sum!' "
        "Lūna: 'Tū es lībera. Sed nunc tū dēbēs mēcum venīre. "
        "In caelō, tū stēlla eris. In caelō, tū semper lūcēbis.' "
        "Ancilla: 'In caelō? Cum tē?' "
        "Lūna: 'Ita. In caelō, nōn est servus neque līber. "
        "In caelō, omnēs sunt stēllae. Omnēs lūcent.' "
        "Ancilla lūnam spectat. Ancilla: 'Ego veniam.' "
        "Lūna ancillam capit. Lūna ancillam ad caelum portat. "
        "Māne venit. Ancilla nōn in vīllā est. "
        "Dominus: 'Ubi est ancilla?' Nēmō scit. "
        "Sed in caelō, prope lūnam, nova stēlla lūcet. "
        "Stēlla est parva — sed stēlla est pulchra. "
        "Et quandō nox venit, ancilla et lūna simul in caelō sunt. "
        "Et ancilla tandem lībera est."
    ),
}


# ============================================================
# 主流程：评估并写入文件
# ============================================================

def main():
    cap_dir = REALITATES_DIR / "Cap13"
    cap_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for key, story in STORIES.items():
        text = story["text"]
        tier = story["length_tier"]

        # 评估
        result = evaluate(text, story["title_la"])
        v2_level = result["v2_level"]
        v2_rate = result["v2_rate"]
        oov = result["v2_oov"]

        passed = v2_level is not None and v2_level <= story["target_chapter"] + 2

        # 确定文件后缀
        if tier == "中篇":
            suffix = "medius"
        elif tier == "中长篇":
            suffix = "longior"
        elif tier == "长篇":
            suffix = "longus"
        else:
            suffix = "medius"

        # 找下一个可用编号
        existing = sorted(cap_dir.glob(f"Cap13_{story['title_la'].replace(' ', '_').replace(',', '')}_{suffix}_*.md"))
        next_num = len(existing) + 1
        filename = f"Cap13_{story['title_la'].replace(' ', '_').replace(',', '')}_{suffix}_{next_num:03d}.md"
        filepath = cap_dir / filename

        # 构建 YAML
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        word_count = len(text.split())

        yaml_lines = [
            "---",
            f"title_la: \"{story['title_la']}\"",
            f"title_zh: \"{story['title_zh']}\"",
            f"target_chapter: {story['target_chapter']}",
            f"theme: \"{story['theme']}\"",
            f"style: \"{story['style']}\"",
            f"genre: \"{story['genre']}\"",
            f"character_type: \"{story['character_type']}\"",
            f"length_tier: \"{story['length_tier']}\"",
            f"narrative_mode: \"{story['narrative_mode']}\"",
            f"word_count: {word_count}",
            "macrons_status: \"generated\"",
            f"evaluated_chapter: {v2_level}",
            f"v2_rate: {v2_rate}",
            f"v2_oov: {json.dumps(oov)}",
            f"created_at: \"{now}\"",
            f"updated_at: \"{now}\"",
            "status: \"active\"",
            "rewritten_from: \"brevis\"",
            "---",
            "",
        ]

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines))
            f.write(text)
            f.write("\n")

        status = "PASS" if passed else "FAIL"
        print(f"{status} {filename}  v2={v2_level}  rate={v2_rate}%  words={word_count}  oov={len(oov)}")
        results.append((passed, story["title_la"], v2_level, v2_rate, word_count, len(oov)))

    # 汇总
    passed_count = sum(1 for r in results if r[0])
    total = len(results)
    print(f"\n通过: {passed_count}/{total}")
    if passed_count < total:
        print("失败:")
        for r in results:
            if not r[0]:
                print(f"  {r[1]}: v2={r[2]} rate={r[3]}% words={r[4]} oov={r[5]}")


if __name__ == "__main__":
    main()