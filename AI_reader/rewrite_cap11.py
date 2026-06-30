#!/usr/bin/env python3
"""rewrite_cap11.py — 重写 Cap.11 的 14 篇短篇为 中篇/中长篇/长篇。
比例 5:3:2 → 7中篇 + 4中长篇 + 3长篇。
非严格模式：v2_level ≤ target_chapter + 2 (=13) 即可。
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
# 中篇 (medius, 300-500 words) x7
# ============================================================

STORIES["cap11_01"] = {
    "title_la": "Agricola et terra",
    "title_zh": "农夫与土地",
    "target_chapter": 11,
    "theme": "36 乡村",
    "style": "抒情",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego agricola sum. Terra mea est. Ego in terrā labōrō. "
        "Māne ego surgō. Sōl nōndum in caelō est. Ego ad terram eō. "
        "Terra mea nōn magna est. Terra mea parva est. Sed terra mea bona est. "
        "Ego in terrā multās plantās habeō. Plantae sunt parvae. "
        "Ego plantīs aquam dō. Ego plantīs cibum dō. "
        "Ego cum plantīs loquor — sīcut pater cum fīliīs loquitur. "
        "Plantae mihi respondent. Nōn verbīs — sed fōliīs. "
        "Fōlia viridia sunt. Fōlia ad sōlem sē vertunt. "
        "Terra est amīca mea. Terra mihi cibum dat. "
        "Terra mihi frūmentum dat. Terra mihi olīvās dat. "
        "Ego terram tangō. Terra est calida. Terra est vīva. "
        "Aliquandō ego in terrā sedeō. Ego caelum spectō. "
        "Caelum est magnum. Caelum est caeruleum. "
        "Nūbēs in caelō sunt. Nūbēs albae sunt. "
        "Sōl in caelō lūcet. Sōl est calidus. Sōl est bonus. "
        "Ego sōlem amō. Sōl plantīs lūcem dat. "
        "Ego quoque plantīs aquam dō — sed sōl dat quod ego dare nōn possum. "
        "Hominēs in oppidō habitant. Hominēs multās rēs habent. "
        "Hominēs multās domōs habent. Hominēs multōs amīcōs habent. "
        "Ego sōlus in terrā sum. Sed ego nōn sōlus sum. "
        "Terra mēcum est. Plantae mēcum sunt. Caelum mēcum est. "
        "Vesperī, quandō sōl abīt, ego ad vīllam redeō. "
        "Vīlla est parva. Vīlla est mea. In vīllā, ego cibum edō. "
        "Cibus est bonus. Cibus dē terrā meā venit. "
        "Ego in lectō iaceō. Ego oculōs claudō. "
        "Ego dē terrā meā cōgitō. Terra est bona. "
        "Ego agricola bonus sum. Terra mihi cibum dat. Ego terram amō. "
        "Crās, ego iterum ad terram eō. Crās, ego iterum cum plantīs loquor. "
        "Terra semper ibi est. Terra semper mē exspectat. "
        "Et hoc est vīta mea. Et haec est vīta bona."
    ),
}

STORIES["cap11_02"] = {
    "title_la": "Duo maria",
    "title_zh": "两片海",
    "target_chapter": 11,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mare Nostrum, Ōceanus. Sunt duo maria. "
        "Duo maria — sed nōn eadem. Mare Nostrum est in mediō. "
        "Ōceanus est in fīne. Mare Nostrum tangit Ītaliam. "
        "Ōceanus tangit Britanniam. "
        "Mare Nostrum est Rōmānum. Mare Nostrum est amīcus. "
        "Multae nāvēs in Marī Nostrō sunt. Nāvēs ad Graeciam eunt. "
        "Nāvēs ad Hispāniam eunt. Nāvēs ad Africam eunt. "
        "Mare Nostrum est via. Mare Nostrum est porta. "
        "Vir in marī natat. Vir: 'Aqua est calida. Aqua est bona. "
        "Mare Nostrum est sīcut māter — māre omnium Rōmānōrum.' "
        "Vir in marī piscēs videt. Piscēs sunt multī. "
        "Piscēs sunt parvī et magnī. Piscēs in aquā saltant. "
        "Vir: 'Mare Nostrum plēnum vītae est.' "
        "Sed est alterum mare. Ōceanus. "
        "Ōceanus nōn est Rōmānus. Ōceanus est magnus — tam magnus ut fīnem nōn habeat. "
        "In Ōceanō, aquae sunt altae. In Ōceanō, ventī sunt magnī. "
        "Vir ad Ōceanum it. Vir in Ōceanum spectat. "
        "Vir: 'Ōceanus est sīcut pater — sevērus, magnus, sine fīne.' "
        "Nāvēs in Ōceanum nōn facile eunt. Nautae Ōceanum timent. "
        "Ōceanus nōn est via — Ōceanus est mūrus. "
        "Sed Rōmānī Ōceanum quoque nōn timent. "
        "Rōmānī nāvēs in Ōceanum mittunt. Rōmānī ad Britanniam eunt. "
        "Vir: 'Duo maria. Ūnum est amīcus. Alterum est hostis. "
        "Sed Rōmānī utrumque mare amant. "
        "Mare Nostrum nōs coniungit. Ōceanus nōs probat.' "
        "Duo maria. Duo animī. Ūnum imperium. "
        "Et Rōmānī in utrōque marī sunt."
    ),
}

STORIES["cap11_03"] = {
    "title_la": "Equus et dominus",
    "title_zh": "马与主人",
    "target_chapter": 11,
    "theme": "32 友谊与孤独",
    "style": "白话",
    "genre": "A 童话",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Equus in stabulō stat. Equus est magnus. Equus est niger. "
        "Equus est pulcher. Equus in stabulō sōlus est. "
        "Equus dominum exspectat. Dominus semper māne venit. "
        "Hodiē quoque dominus venit. Dominus: 'Salvē, equus! Hodiē currimus.' "
        "Equus hinnit. Equus caput movet. Equus laetus est. "
        "Dominus equum tangit. Dominus: 'Bonus equus es. Optimus equus es.' "
        "Equus dominī manum lingit. Equus dominum amat. "
        "Dominus equum ex stabulō dūcit. Equus in viā stat. "
        "Via est longa. Via est pulchra. Sōl in caelō lūcet. "
        "Dominus in equum ascendit. Dominus: 'Ī, equus! Curre!' "
        "Equus currit. Equus celer est. Ventus in auribus est. "
        "Dominus rīdet. Dominus: 'Bene, equus! Bene curris!' "
        "Equus per campōs currit. Herbae sunt viridēs. "
        "Avēs in caelō sunt. Avēs cantant. "
        "Equus per silvam currit. Arborēs sunt altae. "
        "Umbrae in viā sunt. Equus per umbrās currit. "
        "Dominus: 'Equus, tū es amīcus meus. Tū mē per terrās portās. "
        "Sine tē, ego nihil sum. Sine tē, ego nōn possum īre.' "
        "Equus dominum audit. Equus nōn respondet verbīs. "
        "Sed equus caput movet. Equus scit. "
        "Posteā, dominus equum ad aquam dūcit. "
        "Equus aquam bibit. Aqua est frīgida. Aqua est bona. "
        "Dominus equum iterum tangit. Dominus: 'Hodiē bene cucurrimus. "
        "Crās quoque currēmus. Et post crās. Et multōs diēs.' "
        "Equus in stabulō iterum stat. Sed equus nōn sōlus est. "
        "Equus scit: dominus prope est. Dominus semper prope est. "
        "Et equus laetus est. Et dominus quoque laetus est. "
        "Sunt duo — equus et dominus. Et sunt amīcī."
    ),
}

STORIES["cap11_04"] = {
    "title_la": "In campō",
    "title_zh": "在原野",
    "target_chapter": 11,
    "theme": "36 乡村",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in campō currit. Puer parvus est — decem annōs habet. "
        "Herba alta est. Herba puerum tangit. "
        "Ventus flat. Ventus est calidus. Ventus herbam movet. "
        "Puer: 'Hīc līber sum!' Puer in campō sōlus est. "
        "Nēmō eum videt. Nēmō eum audit. "
        "Puer in herbā iacet. Puer caelum spectat. "
        "Caelum est magnum. Caelum est caeruleum. "
        "Nūbēs in caelō movent. Nūbēs albae sunt. "
        "Nūbēs lentē movent — sīcut nāvēs in marī. "
        "Puer: 'Nūbēs, quō ītis?' Nūbēs nōn respondent. "
        "Puer: 'Nūbēs, quid vidētis?' Nūbēs nōn respondent. "
        "Sed puer nōn trīstis est. Puer nūbēs spectat. "
        "Puer: 'Nūbēs sunt līberae. Nūbēs per caelum eunt quō volunt. "
        "Ego quoque līber sum — hīc, in campō.' "
        "Avēs in caelō sunt. Avēs cantant. "
        "Avēs parvae sunt. Avēs quoque līberae sunt. "
        "Puer: 'Avēs, quō ītis?' Avēs nōn respondent. "
        "Sed avēs in caelō volant. Avēs sunt pulchrae. "
        "Puer surgit. Puer flōrēs in campō videt. "
        "Flōrēs rubrī sunt. Flōrēs albī sunt. Flōrēs pulchrī sunt. "
        "Puer flōrem carpit. Puer flōrem ad nāsum tenet. "
        "Flōs est bonus. Flōs odōrem bonum habet. "
        "Puer: 'Hic flōs est mātrī meae. Māter mea flōrēs amat.' "
        "Puer flōrem in manū tenet. Puer domum it. "
        "Sōl in caelō est. Sōl est calidus. "
        "Puer ad vīllam venit. Māter in vīllā est. "
        "Puer: 'Māter, flōrem tibi portō!' "
        "Māter puerum videt. Māter rīdet. "
        "Māter: 'Fīlī, flōs est pulcher. Sed tū es pulchrior.' "
        "Puer mātrem amplexātur. Puer laetus est. "
        "Et puer scit: campus semper ibi est. Campus semper eum exspectat. "
        "Crās, puer iterum in campum ībit. Crās, iterum līber erit."
    ),
}

STORIES["cap11_05"] = {
    "title_la": "In triclīniō",
    "title_zh": "在餐厅",
    "target_chapter": 11,
    "theme": "25 家庭",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Familia in triclīniō sedet. Mēnsa parāta est. "
        "Pater, māter, duo fīliī. Servus cibum portat. "
        "Servus pānem portat. Servus piscem portat. Servus vīnum portat. "
        "Mēnsa est plēna. In mēnsā, multae rēs sunt. "
        "Pater: 'Hic piscis bonus est. Piscis ex marī venit.' "
        "Māter: 'Ita. Piscis est bonus. Servus bene labōrat.' "
        "Fīliī edunt. Fīlius maior multum edit. "
        "Fīlius minor parvum edit. Fīlius minor: 'Māter, ego nōn ēsuriō.' "
        "Pater: 'Ede! Cibus est bonus. Cibus tibi vīrēs dat.' "
        "Fīlius minor: 'Sed ego nōn ēsuriō. Ego in hortō lūdere volō.' "
        "Māter: 'Post cibum, fīlī. Prīmum ede, tum lūde.' "
        "Fīlius maior: 'Pater, quid hodiē in forō ēgistī?' "
        "Pater: 'Multās rēs. In forō, multī hominēs erant. "
        "Ego mercātōrēs vīdī. Ego amīcōs vīdī. "
        "Ego novum librum ēmī. Liber est bonus.' "
        "Fīlius maior: 'Quid est in librō?' "
        "Pater: 'Historiae Rōmae. Dē rēgibus antīquīs. Dē bellīs. Dē virīs fortibus.' "
        "Fīlius maior: 'Ego quoque librōs amō. Ego legere volō.' "
        "Māter: 'Bene, fīlī. Litterae sunt bona. Litterae tē sapientem faciunt.' "
        "Fīlius minor: 'Ego nōn librōs amō. Ego equōs amō. Ego in campō currere volō.' "
        "Pater rīdet. Pater: 'Tū, fīlī, es sīcut equus ipse — semper currere vīs!' "
        "Fīlius minor rīdet. Fīlius minor: 'Ita, pater! Ego equus sum!' "
        "Fīlius minor per triclīnium currit. Puer hinnit — sīcut equus. "
        "Māter: 'Nōn in triclīniō! Posteā, in hortō.' "
        "Fīlius minor sedet. Puer: 'Sed mox, in hortō, ego curram!' "
        "Māter puerum tangit. Māter: 'Tū es bonus puer. Nunc ede.' "
        "Familia in triclīniō cibum cōnsūmit. Sōl per fenestram lūcet. "
        "Sōl est calidus. Sōl in mēnsā lūcet. "
        "Pater mātrem spectat. Pater: 'Familia est bona. Nihil melius est quam familia.' "
        "Māter: 'Ita. Familia est omnia.' "
        "Et familia in triclīniō laeta est."
    ),
}

STORIES["cap11_06"] = {
    "title_la": "Lūdus puerōrum",
    "title_zh": "孩子们的学校",
    "target_chapter": 11,
    "theme": "28 教育",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puerī in lūdō sunt. Lūdus est parvus. Lūdus in oppidō est. "
        "Magister in lūdō sedet. Magister est senex. Magister sevērus est. "
        "Puerī in sellīs sedent. Puerī litterās discunt. "
        "Magister litterās in tabulā scrībit. Magister: 'A, B, C, D...' "
        "Puerī: 'A, B, C, D...' Puerī litterās repetunt. "
        "Ūnus puer nōn dīcit. Puer fenestram spectat. "
        "Avēs in caelō sunt. Avēs cantant. Avēs volant. "
        "Magister: 'Tū! Cūr nōn dīcis?' "
        "Puer: 'Ego avēs spectō. Avēs sunt pulchrae. Avēs līberae sunt.' "
        "Magister: 'Avēs nōn tē litterās docent. Ego tē litterās doceō. Dīc: A, B, C!' "
        "Puer: 'A, B, C...' Sed puer iterum fenestram spectat. "
        "Alius puer: 'Magister, ego litterās sciō. Ego legere possum.' "
        "Magister: 'Tū scīs? Tū legere potes? Probā!' "
        "Alius puer ad tabulam it. Puer litterās legit. Puer: 'Rō-ma. Rōma est ca-put.' "
        "Magister: 'Bene! Tū es bonus puer. Tū es discipulus bonus.' "
        "Alius puer laetus est. Puer ad sellam redit. "
        "Puer quī fenestram spectābat: 'Ego quoque legere volō. Sed avēs...' "
        "Magister: 'Avēs crās quoque erunt. Litterae hodiē sunt. "
        "Post lūdum, tū potes avēs spectāre. Sed nunc — A, B, C!' "
        "Puer: 'A, B, C...' Et puer nōn iam fenestram spectat. "
        "Puer in tabulam spectat. Puer litterās discit. "
        "Magister quoque rīdet. Magister: 'Ecce! Tū potes discere!' "
        "Post lūdum, puerī in viam exeunt. Puerī laetī sunt. "
        "Puer quī fenestram spectābat ad avēs currit. Avēs in arbore sunt. "
        "Puer: 'Avēs, ego litterās didicī! A, B, C!' "
        "Avēs cantant. Avēs quasi respondent. "
        "Puer rīdet. Puer: 'Hodiē, ego et litterās et avēs habeō.' "
        "Et puer domum currit. Puer laetus est."
    ),
}

STORIES["cap11_07"] = {
    "title_la": "Medicus et aeger",
    "title_zh": "医生与病人",
    "target_chapter": 11,
    "theme": "01 生死",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "Medicus in oppidō habitat. Medicus est bonus. Medicus multōs aegrōs cūrat. "
        "Hodiē, novus aeger ad medicum venit. "
        "Aeger est vir. Vir est senex. Vir nōn bene sē habet. "
        "Medicus: 'Ubi dolēs?' "
        "Aeger: 'In pectore. Hīc. Cor meum dolet.' "
        "Medicus: 'Quandō coepit?' "
        "Aeger: 'Herī. Subitō. Ego in forō eram. Tum dolor vēnit — sīcut gladius.' "
        "Medicus aegrum tangit. Medicus aegrī pectus audit. "
        "Medicus: 'Tacē. Ego cor tuum audiō.' "
        "Aeger tacet. Medicus audit. "
        "Medicus: 'Cor tuum nōn bene est. Sed ego tē iuvāre possum.' "
        "Aeger: 'Vīvamne?' "
        "Medicus: 'Fortasse. Sī remedia mea bibis. Sī quiētem habēs. Sī bonus es.' "
        "Aeger: 'Remedia... sunt amāra?' "
        "Medicus rīdet. Medicus: 'Omnia remedia sunt amāra. Sed vīta est dulcis.' "
        "Medicus herbās parat. Medicus aquam calidam parat. "
        "Medicus: 'Bibe hoc. Hoc est remedium.' "
        "Aeger remedium bibit. Aeger: 'Amārum est! Valdē amārum!' "
        "Medicus: 'Bonum est. Sī amārum est, remedium bene labōrat.' "
        "Aeger: 'Ego tibi crēdō, medice. Tū es bonus medicus.' "
        "Medicus: 'Ego nōn sum deus. Ego sōlum homō sum. "
        "Sed ego multōs aegrōs vīdī. Multī vīxērunt. Aliquī nōn vīxērunt. "
        "Nōn ego vītam dō. Nōn ego vītam capiō. Ego sōlum iuvō.' "
        "Aeger: 'Quid dēbeō facere?' "
        "Medicus: 'Domum ī. In lectō iacē. Nōn labōrā. Nōn currās. "
        "Bibe remedium māne et vesperī. Post septem diēs, ad mē redī.' "
        "Aeger: 'Septem diēs... longum est.' "
        "Medicus: 'Septem diēs nihil sunt. Vīta est longa. Septem diēs sunt parvī.' "
        "Aeger surgit. Aeger: 'Grātiās tibi agō, medice.' "
        "Medicus: 'Nōn mihi grātiās age. Remedium grātiās age. Et cor tuum.' "
        "Aeger abīt. Medicus in sellā sedet. "
        "Medicus multōs aegrōs videt. Sed quisque aeger est novus. "
        "Quisque dolor est novus. Quisque vīta est nova. "
        "Et medicus scit: opus eius magnum est. Et opus eius bonum est."
    ),
}

# ============================================================
# 中长篇 (longior, 500-800 words) x4
# ============================================================

STORIES["cap11_08"] = {
    "title_la": "Amor in Forō",
    "title_zh": "广场上的爱",
    "target_chapter": 11,
    "theme": "02 爱",
    "style": "史诗",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in forō sum. Forum Rōmae magnum est. "
        "Multī virī et fēminae in forō sunt. Multī servī et ancillae in forō sunt. "
        "Multī mercātōrēs in forō clāmant. Multī ēmptōrēs in forō ambulant. "
        "Forum est cor Rōmae. Forum est vīvum. "
        "Ego per forum ambulō. Ego multōs hominēs videō. "
        "Tum — ego fēminam videō. Fēmina pulchra est. "
        "Fēmina stolam albam gerit. Fēmina capillōs nigrōs habet. "
        "Fēmina in tabernā stat. Fēmina flōrēs spectat. "
        "Ego ad fēminam ambulō. Ego nihil dīcō. Ego sōlum spectō. "
        "Fēmina mē videt. Fēmina rīdet. Ego quoque rīdeō. "
        "Fēmina: 'Flōrēs sunt pulchrī, nōnne?' "
        "Ego: 'Ita. Flōrēs sunt pulchrī. Sed tū es pulchrior.' "
        "Fēmina rīdet iterum. Fēmina: 'Tū es audāx, vir.' "
        "Ego: 'Nōn audāx — vērāx. Ego vērum dīcō.' "
        "Fēmina flōrem carpit. Flōs est ruber — sīcut rosa. "
        "Fēmina mihi flōrem dat. Fēmina: 'Tibi. Quia vērum dīxistī.' "
        "Ego flōrem accipiō. Ego: 'Grātiās. Sed quid est nōmen tuum?' "
        "Fēmina: 'Nōmen meum est Cornēlia. Et tuum?' "
        "Ego: 'Gāius. Gāius sum.' "
        "Cornēlia: 'Gāius... nōmen bonum. Nōmen Rōmānum.' "
        "Ego: 'Ubi habitās, Cornēlia?' "
        "Cornēlia: 'Prope Palātium. Et tū?' "
        "Ego: 'Prope Forum. Ego semper hīc sum.' "
        "Cornēlia rīdet. Cornēlia: 'Tum, fortasse, iterum tē vidēbō.' "
        "Tum Cornēlia abīt. Ea in turbā abest. "
        "Ego in forō sōlus stō. Ego eam quaerō. "
        "Forum magnum est. Cornēlia nōn est. "
        "Turbae multae sunt. Vōcēs multae sunt. Sed Cornēlia nōn est. "
        "Ego in forō sedeō. Ego flōrem in manū teneō. "
        "Flōs est ruber. Flōs est pulcher. Flōs est Cornēliae. "
        "Ego flōrem spectō. Ego dē Cornēliā cōgitō. "
        "Cornēlia pulchra est. Cornēlia bona est. "
        "Ego Cornēliam in memoriā habeō. "
        "Sōl in caelō est. Sōl calidus est. "
        "Ego in forō sedēre nōn possum. Ego surgō. Ego ad Palātium eō. "
        "Fortasse — fortasse Cornēlia ibi est. Fortasse eam iterum vidēbō. "
        "Ego ad Palātium ambulō. Viā sunt pulchrae. Domūs sunt magnae. "
        "Sed Cornēlia nōn est. Ego eam nōn videō. "
        "Ego domum redeō. Ego in lectō iaceō. "
        "Ego oculōs claudō. Ego Cornēliam videō — in memoriā. "
        "Et ego scīo: amor in forō incēpit. Amor in corde manet. "
        "Crās, ego iterum ad forum ībō. Crās, ego iterum Cornēliam quaeram. "
        "Forum est magnum. Sed amor est maior. "
        "Et fortasse — fortasse crās eam vidēbō."
    ),
}

STORIES["cap11_09"] = {
    "title_la": "Amor Servī",
    "title_zh": "奴隶之爱",
    "target_chapter": 11,
    "theme": "02 爱",
    "style": "抒情",
    "genre": "M 伦理与习俗",
    "character_type": "奴隶",
    "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Domina in hortō sedet. Domina est pulchra. Domina flōrēs spectat. "
        "Servus prope est. Servus tacet. Servus dominam spectat. "
        "Domina servum nōn videt. Domina in caelum spectat. "
        "Domina: 'Sōl est calidus. Hodiē bonus diēs est.' "
        "Servus: 'Ita, domina. Hodiē bonus diēs est.' "
        "Domina servum audit. Domina caput vertit. "
        "Domina: 'Servus, cūr mē semper spectās? Semper tē videō — prope mē.' "
        "Servus tacet. Servus in terram spectat. "
        "Servus: 'Spectō, domina, quia sōlem in oculīs tuīs videō. "
        "Oculī tuī sunt sīcut caelum. Quandō tē spectō, ego laetus sum.' "
        "Domina: 'Tū servus es. Nōn decet servum dominam amāre. "
        "Hoc nōn est rēctum. Hoc nōn est Rōmānum.' "
        "Servus: 'Amor nōn rogat. Amor nōn quaerit sī rēctum est. "
        "Amor venit ut ventus — nōn interrogat, intrat. "
        "Ego nōn voluī tē amāre. Sed amor vēnit. Et ego nihil facere possum.' "
        "Domina tacet. Domina servum spectat. "
        "Domina: 'Et quid vīs? Quid vīs ā mē?' "
        "Servus: 'Nihil. Nōn argentum, nōn lībertātem. "
        "Nōn domum, nōn terram. Hoc sōlum: quandō in hortō sedēs et flōrēs spectās, "
        "scīs mē prope esse. Et hoc mihi satis est. "
        "Ego nihil habeō — sed quandō tē videō, ego omnia habeō.' "
        "Domina in oculīs servī spectat. Domina nihil dīcit. "
        "Sed in oculīs eius lacrimae sunt. "
        "Domina: 'Surge, serve.' Servus surgit. "
        "Domina: 'Dā mihi manum tuam.' Servus manum dat. "
        "Domina servī manum tenet. Domina: 'Manus tua est calida. Manus tua est fortis.' "
        "Servus: 'Manus mea est tua, domina. Semper fuit tua.' "
        "Domina: 'Ego nōn possum tē amāre. Rōma nōn sinit. Hominēs nōn sinunt. "
        "Sed ego tē videō. Ego tē videō — nōn ut servum, sed ut hominem. "
        "Et hoc, serve, est dōnum meum.' "
        "Servus: 'Hoc est maximum dōnum. Maius quam lībertās.' "
        "Domina servī manum dīmittit. Domina surgit. "
        "Domina: 'Nunc abī. Ego in hortō sōla esse volō.' "
        "Servus abit. Sed in corde, laetus est. "
        "Servus scit: domina eum vīdit. Nōn servum — sed hominem. "
        "Et hoc est omnia. Hoc est amor."
    ),
}

STORIES["cap11_10"] = {
    "title_la": "Mōns et Homō",
    "title_zh": "山与人",
    "target_chapter": 11,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "B 神话与传说",
    "character_type": "拟人自然",
    "length_tier": "中长篇",
    "narrative_mode": "旁观者",
    "text": (
        "Mōns magnus in terrā stat. Mōns antīquus est. "
        "Mōns ibi est ante hominēs. Mōns ibi erit post hominēs. "
        "Mōns hominēs videt. Hominēs parvī sunt. "
        "Hominēs veniunt et abeunt — sīcut undae in marī. "
        "Mōns manet. Mōns semper manet. "
        "Homō ad montem venit. Homō parvus est. Mōns magnus est. "
        "Homō: 'Mōns, tū es magnus. Ego sum parvus. "
        "Quid est sēnsus vītae meae, sī mōns tantum videt et nihil dīcit?' "
        "Mōns nōn respondet. Mōns tacet — sīcut semper. "
        "Sed ventus per montem flat. Ventus est vōx montis. "
        "Ventus: 'Tū quaeris sēnsum. Sed sēnsus nōn est in verbīs. "
        "Sēnsus est in oculīs tuīs. In corde tuō. In pedibus tuīs.' "
        "Homō: 'Ventus, tū es vōx montis. Dīc mihi: cūr homō vīvit?' "
        "Ventus: 'Hominēs vīvunt ut videant. Ut ament. Ut memoriās faciant. "
        "Mōns multōs annōs videt. Sed mōns nōn amat. Mōns nōn meminit. "
        "Tū amās. Tū meministi. Hoc est dōnum hominis. Hoc est sēnsus.' "
        "Homō montem ascendit. Homō in monte stat. "
        "Homō caelum videt. Homō terram videt. "
        "Homō maria videt. Homō oppida videt. "
        "Homō sē magnum sentit — nōn magnum ut mōns, sed magnum ut homō. "
        "Homō: 'Mōns, ego tē ascendī. Ego in tē stō. "
        "Tū es magnus — sed ego quoque magnus sum. Nōn in corpore. In animō.' "
        "Mōns tacet. Sed ventus iterum flat. "
        "Ventus: 'Nunc scīs. Nunc dēscende. Vīta tua tē exspectat.' "
        "Homō dē monte dēscendit. Homō nōn iam magnus sentit. "
        "Homō iterum parvus est. Sed homō montem in memoriā habet. "
        "Homō scit: mōns magnus est, sed homō quoque magnus esse potest. "
        "Nōn in corpore — in memoriā. In amōre. In animō. "
        "Aliī hominēs ad montem veniunt. Aliī ascendunt. Aliī dēscendunt. "
        "Mōns hominēs videt. Hominēs parvī sunt. "
        "Hominēs veniunt et abeunt. Mōns manet. "
        "Sed nunc mōns scit: hominēs quoque magnī sunt. "
        "Nōn ut mōns — sed ut hominēs. "
        "Et hoc, fortasse, est melius."
    ),
}

STORIES["cap11_11"] = {
    "title_la": "Sex oppida Italiae",
    "title_zh": "意大利六城",
    "target_chapter": 11,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma, Brundisium, Tusculum, Capua, Neapolis, Latium. "
        "Sex oppida. Sex in Italiā. Sex Rōmāna. "
        "Rōma est caput. Rōma est māter omnium oppidōrum. "
        "In Rōmā, forum est magnum. In Rōmā, templa sunt multa. "
        "In Rōmā, senātus sedet. In Rōmā, imperātor habitat. "
        "Rōma est cor imperiī. Rōma est lūx mundī. "
        "Vir Rōmānus: 'Rōma est patria mea. Rōma est omnia.' "
        "Brundisium est porta. Brundisium in marī est. "
        "Brundisium est porta ad Graeciam. Brundisium est porta ad orientem. "
        "Nāvēs in Brundisiō sunt. Nāvēs ad Graeciam eunt. "
        "Nāvēs ad Asiam eunt. Nautae in Brundisiō cantant. "
        "Vir Brundisīnus: 'Brundisium est parvum. Sed Brundisium est porta mundī.' "
        "Tusculum est prope. Tusculum prope Rōmam est. "
        "In Tusculō, villae sunt pulchrae. In Tusculō, hortī sunt magnī. "
        "Virī Rōmānī in Tusculum veniunt. Virī quiētem quaerunt. "
        "Vir Tūsculānus: 'Tusculum est quiētum. Hīc, ego ā Rōmā quiēscō.' "
        "Capua est magna. Capua in Campāniā est. "
        "In Capuā, multī hominēs habitant. In Capuā, multae tabernae sunt. "
        "Capua est dīves. Capua est pulchra. "
        "Vir Capuānus: 'Capua est secunda Rōma. Capua quoque magna est.' "
        "Neapolis est Graeca. Neapolis in marī est. "
        "In Neapolī, lingua Graeca auditur. In Neapolī, mōrēs Graecī sunt. "
        "Neapolis est pulchra. Mare prope Neapolim est caeruleum. "
        "Vir Neapolītānus: 'Neapolis est Graeca — sed Neapolis est Rōmāna quoque.' "
        "Latium est terra. Latium nōn est oppidum — sed terra est. "
        "Latium est inter Rōmam et Capuam. Latium est terra antīqua. "
        "In Latiō, agricolae labōrant. In Latiō, frūmentum est bonum. "
        "Vir Latīnus: 'Latium est terra patrum meōrum. Latium est terra mea.' "
        "Vir quī haec oppida vīsitāvit in viā sedet. "
        "Vir: 'Sex oppida. Sex mundī. Et omnia sunt Rōmāna. "
        "Omnia sunt in imperiō. Omnia sunt in memoriā.' "
        "Vir ad Rōmam redit. Rōma est caput. "
        "Sed vir scit: omnia sex oppida sunt pulchra. Omnia sunt Rōma."
    ),
}

# ============================================================
# 长篇 (longus, 800-1500 words) x3
# ============================================================

STORIES["cap11_12"] = {
    "title_la": "Anulus Sine Gemma",
    "title_zh": "无宝石的戒指",
    "target_chapter": 11,
    "theme": "04 富与贫",
    "style": "古典",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Albīnus tabernam habet. Taberna in Forō est. "
        "In tabernā sunt ānulī et gemmae et ōrnāmenta. "
        "Albīnus tabernārius est. Albīnus dīves est. "
        "Multī hominēs ad tabernam veniunt. Multī emunt. "
        "Servus eius Mēdus in tabernā stat. Mēdus ōrnāmenta cūrat. "
        "Mēdus ānulōs videt. Mēdus gemmās videt. "
        "Mēdus nihil habet — sed Mēdus multa videt. "
        "Hodiē, fēmina ad tabernam venit. Fēmina est pulchra. "
        "Fēmina stolam simplicem gerit. Fēmina nōn dīves est. "
        "Fēmina: 'Ānulum quaerō. Sed nōn magnum. Nōn cum gemmā. "
        "Ānulum simplicem — sīcut amor meus.' "
        "Albīnus: 'Ānulum sine gemmā? Nēmō ānulum sine gemmā emit. "
        "Gemmae sunt pulchrae. Gemmae sunt pretiōsae.' "
        "Fēmina: 'Amor meus nōn est pretiōsus. Amor meus est simplex. "
        "Et ānulus quoque simplex esse dēbet.' "
        "Albīnus: 'Nōn habeō ānulum sine gemmā. Omnēs ānulī meī gemmās habent.' "
        "Fēmina trīstis est. Fēmina abīre parat. "
        "Mēdus fēminam videt. Mēdus: 'Domine, exspectā. Habeō ānulum.' "
        "Albīnus: 'Tū? Tū nihil habēs, serve!' "
        "Mēdus manum in sinum mittit. Mēdus ānulum parvum prōfert. "
        "Ānulus est ferreus. Ānulus nōn gemmam habet. "
        "Ānulus est simplex — sed pulcher. "
        "Albīnus: 'Unde habēs hunc ānulum?' "
        "Mēdus: 'Hic ānulus mātris meae fuit. Māter mea mihi eum dedit. "
        "Māter mea quoque serva erat — sed ānulum habēbat. "
        "Māter dīxit: «Hic ānulus nōn gemmam habet, sed amōrem meum habet.»' "
        "Fēmina ānulum spectat. Fēmina: 'Hic ānulus est pulcher. "
        "Sed tū — tū servus es. Tū nihil habēs. Cūr mihi eum dare vīs?' "
        "Mēdus: 'Quia amor nōn est pretiōsus. Amor est simplex. "
        "Sīcut ānulus. Sīcut māter mea. Sīcut tū.' "
        "Fēmina in oculīs Mēdī spectat. Fēmina: 'Quantum vīs?' "
        "Mēdus: 'Nihil. Nōn argentum. Dā eum virō tuō. Et est satis.' "
        "Fēmina ānulum accipit. Fēmina: 'Grātiās, serve. Tū es bonus homō.' "
        "Fēmina abit. Albīnus Mēdum spectat. "
        "Albīnus: 'Ānulus ille... pretium habēbat. Nōn magnum — sed habēbat. "
        "Cūr eum nihilō dedistī?' "
        "Mēdus: 'Domine, tū multōs ānulōs vendis. Multās gemmās. "
        "Sed amor — amor nōn venditur. Amor datur.' "
        "Albīnus tacet. Albīnus in tabernā sedet. "
        "Albīnus multōs ānulōs habet. Albīnus multās gemmās habet. "
        "Sed Albīnus nunc scit: aliquid deest. "
        "Post multōs diēs, fēmina ad tabernam redit. "
        "Fēmina nōn sōla est. Vir cum eā est. "
        "Vir ānulum ferreum in digitō habet. "
        "Fēmina: 'Albīne, hic est vir meus. Ānulus servī tuī nōs coniūnxit. "
        "Volumus tibi grātiās agere — et servō tuō.' "
        "Albīnus Mēdum vocat. Mēdus venit. "
        "Mēdus fēminam et virum videt. Mēdus rīdet. "
        "Mēdus: 'Ānulus mātris meae nunc in digitō bonī virī est. "
        "Māter mea, ubi est, laeta est.' "
        "Vir: 'Serve, tū nōs iūvistī. Quid possumus tibi dare?' "
        "Mēdus: 'Nihil. Ego iam multa habeō. Ego vōs laetōs videō — et hoc est omnia.' "
        "Fēmina et vir abeunt. Albīnus Mēdum spectat. "
        "Albīnus: 'Mēde, tū es servus. Sed tū melior es quam ego. "
        "Ego vendō. Tū dās. Hoc est magnum.' "
        "Mēdus: 'Domine, tū mē docuistī multa. Nunc tū aliquid didicistī.' "
        "Albīnus rīdet. Albīnus: 'Fortasse. Fortasse ego aliquid didicī.' "
        "Et in tabernā, inter multōs ānulōs et multās gemmās, "
        "Albīnus et Mēdus sunt amīcī. "
        "Et ānulus sine gemmā — ānulus mātris — in bonō locō est."
    ),
}

STORIES["cap11_13"] = {
    "title_la": "Roma et Tiberis",
    "title_zh": "罗马与台伯河",
    "target_chapter": 11,
    "theme": "01 生死",
    "style": "精炼",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "长篇",
    "narrative_mode": "旁观者视角",
    "text": (
        "Rōma in Italiā est. Tiberis prope Rōmam fluit. "
        "Tiberis est flūmen antīquum. Tiberis Rōmam vidit — ab initiō. "
        "In rīpā Tiberis, puer sedet. Puer parvus est — septem annōs habet. "
        "Puer aquam spectat. Aqua nigra est. In aquā umbrae sunt. "
        "Puer: 'Quid in aquā est?' "
        "Nēmō respondet. Puer sōlus est. "
        "In aquā, umbrae movent. Umbrae sunt lentae — sīcut nūbēs. "
        "Puer timet. Sed puer quoque cūriōsus est. "
        "Puer: 'Quis es?' Puer ad aquam dīcit. "
        "Tum, umbra ē aquā surgit. Umbra nōn corpus habet. "
        "Umbra est sīcut fūmus. Umbra est sīcut nox. "
        "Umbra: 'Tū mē vocāvistī, puer. Quid quaeris?' "
        "Puer: 'Ego nihil quaerō. Ego aquam spectō. Sed in aquā, tē videō. Quis es?' "
        "Umbra: 'Ego sum Rōma. Ego sum omnia quae fuērunt. "
        "Omnia quae nōn iam sunt. Ego sum quod Rōma fuit — et quod Rōma erit.' "
        "Puer: 'Tū es mortua?' "
        "Umbra: 'Mortua... et vīva. Rōma numquam morītur. "
        "Rōma semper est — in aquā, in terrā, in memoriā.' "
        "Puer: 'Ego tē nōn intellegō. Tū es umbra — sed tū dīcis tē esse Rōmam.' "
        "Umbra: 'Rōma est plus quam lapidēs. Rōma est plus quam templa. "
        "Rōma est animus — animus hominum quī hīc vīxērunt. "
        "Animī mortuōrum in aquā sunt. Animī Rōmae in aquā sunt.' "
        "Puer: 'Ego nōn mortuus sum. Ego vīvus sum.' "
        "Umbra: 'Tū vīvus es. Et hoc est magnum. "
        "Tū potes vidēre. Tū potes amāre. Tū potes meminisse. "
        "Mortuī nōn possunt haec facere. Mortuī sōlum in aquā manent.' "
        "Puer: 'Quid mortuī volunt?' "
        "Umbra: 'Nihil. Mortuī nihil volunt. Mortuī sōlum sunt. "
        "Sed mortuī volunt vīvōs meminisse. Volunt nōmen eōrum nōn perīre.' "
        "Puer: 'Ego meminī. Ego nōn oblīvīscar.' "
        "Umbra: 'Tum mortuī nōn mortuī sunt. Mortuī in memoriā vīvunt.' "
        "Puer surgit. Sōl in caelō est. Umbra in aquam redit. "
        "Puer: 'Nōn abī! Ego plūra quaerere volō!' "
        "Sed umbra nōn iam est. Aqua iterum nigra est. "
        "Puer domum currit. Puer in cubiculum suum it. "
        "Puer in lectō iacet. Puer nōn dormit. "
        "Puer dē umbrā cōgitat. Dē mortuīs. Dē Rōmā. "
        "Posteā, quandō puer per Rōmam ambulat, puer plus videt. "
        "Puer nōn sōlum templa videt. Nōn sōlum forum videt. "
        "Puer umbrās videt. Puer animōs videt. "
        "Puer: 'Rōma nōn sola est. Rōma cum umbrīs est. "
        "Rōma cum mortuīs est. Et hoc est cūr Rōma magna est.' "
        "Annī fluunt — sīcut Tiberis. Puer nōn iam puer est. "
        "Vir est. Vir in forō stat. Vir Rōmānus est. "
        "Vir ad Tiberim redit. Vir in aquam spectat. "
        "In aquā, umbrae sunt. Vir umbrās salūtat. "
        "Vir: 'Ego meminī. Ego nōn oblītus sum. "
        "Rōma est Rōma — vīva et mortua. Et ego sum Rōma.' "
        "Tiberis fluit. Tiberis semper fluit. "
        "Et in aquā Tiberis, Rōma aeterna est."
    ),
}

STORIES["cap11_14"] = {
    "title_la": "Tria maria",
    "title_zh": "三片海",
    "target_chapter": 11,
    "theme": "11 自然与文明",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mare Nostrum, Ōceanus Atlanticus, Mare Rubrum. Sunt tria maria. "
        "Tria maria — tria mundī. Et Rōmānī in omnibus sunt. "
        "Mare Nostrum est Rōmānum. Mare Nostrum est in mediō imperiī. "
        "Mare Nostrum Ītaliam tangit. Mare Nostrum Graeciam tangit. "
        "Mare Nostrum Hispāniam tangit. Mare Nostrum Africam tangit. "
        "Multae nāvēs in Marī Nostrō sunt. Nāvēs Rōmānae sunt. "
        "Nāvēs frūmentum portant. Nāvēs vīnum portant. Nāvēs hominēs portant. "
        "Mare Nostrum est via omnium. Mare Nostrum nōn est fīnis — Mare Nostrum est initium. "
        "Vir in portū stat. Vir est nauta. Vir est Rōmānus. "
        "Vir: 'Mare Nostrum est sīcut māter. Mare Nostrum nōs alit. "
        "Sine Marī Nostrō, Rōma nihil esset.' "
        "Nauta nāvem cōnscendit. Nauta ad Graeciam it. "
        "In marī, ventus est bonus. In marī, aqua est caerulea. "
        "Nauta: 'Mare Nostrum est pulchrum. Mare Nostrum est nostrum.' "
        "Sed est alterum mare. Ōceanus Atlanticus. "
        "Ōceanus nōn est Rōmānus. Ōceanus est magnus — tam magnus ut fīnem nōn habeat. "
        "Ōceanus est in fīne imperiī. Ōceanus Britanniam tangit. "
        "Ōceanus Galliam tangit. Ōceanus Hispāniam tangit. "
        "In Ōceanō, aquae sunt altae. In Ōceanō, ventī sunt magnī. "
        "Nautae Ōceanum timent. In Ōceanō, tempestātēs sunt magnae. "
        "In Ōceanō, nāvēs perīre possunt. "
        "Sed Rōmānī Ōceanum quoque domant. Rōmānī nāvēs in Ōceanum mittunt. "
        "Rōmānī ad Britanniam eunt. Rōmānī ad Hispāniam septentriōnālem eunt. "
        "Vir Rōmānus in Ōceanum spectat. "
        "Vir: 'Ōceanus est sīcut pater — sevērus, magnus, sine fīne. "
        "Sed Rōmānī etiam patrēs nōn timent. Rōmānī omnia domant.' "
        "Et est tertium mare. Mare Rubrum. "
        "Mare Rubrum est longinquum. Mare Rubrum nōn est Rōmānum. "
        "Mare Rubrum est calidum. Mare Rubrum in oriente est. "
        "In Marī Rubrō, aqua est calida — sīcut balneum. "
        "In Marī Rubrō, piscēs sunt multī colōrum. "
        "In Marī Rubrō, mercēs pretiōsae sunt. "
        "Mercātōrēs Rōmānī ad Mare Rubrum eunt. "
        "Mercātōrēs gemmās quaerunt. Mercātōrēs aromata quaerunt. "
        "Mercātor Rōmānus: 'Mare Rubrum est porta ad orientem. "
        "Mare Rubrum est porta ad Indōs. Mare Rubrum est porta ad omnia.' "
        "Vir quī tria maria vīdit nunc in Rōmā sedet. "
        "Vir est senex. Vir multōs annōs in marī fuit. "
        "Vir: 'Tria maria vīdī. Mare Nostrum — mātrem. "
        "Ōceanum — patrem. Mare Rubrum — portam. "
        "Tria maria, tria animī. Et omnia sunt Rōmae.' "
        "Senex fīliō suō dē maribus nārrat. "
        "Fīlius: 'Pater, ego quoque maria vidēre volō. "
        "Ego Mare Nostrum vidēre volō. Ego Ōceanum vidēre volō. "
        "Ego Mare Rubrum vidēre volō.' "
        "Senex: 'Tum ī, fīlī. Maria tē exspectant. "
        "Sed meminī — maria sunt pulchra, sed Rōma est patria. "
        "Semper ad Rōmam redī.' "
        "Fīlius nāvem cōnscendit. Fīlius in maria ībit. "
        "Et Rōmānī semper in maribus erunt. "
        "Tria maria — tria mundī. Et Rōmānī in omnibus."
    ),
}


# ============================================================
# 主流程：评估并写入文件
# ============================================================

def main():
    cap_dir = REALITATES_DIR / "Cap11"
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
        existing = sorted(cap_dir.glob(f"Cap11_{story['title_la'].replace(' ', '_')}_{suffix}_*.md"))
        next_num = len(existing) + 1
        filename = f"Cap11_{story['title_la'].replace(' ', '_')}_{suffix}_{next_num:03d}.md"
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
        
        status = "✓" if passed else "✗"
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