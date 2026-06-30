#!/usr/bin/env python3
"""rewrite_cap12.py — 重写 Cap.12 的 12 篇短篇为 中篇/中长篇/长篇。
比例 5:3:2 → 6中篇 + 4中长篇 + 2长篇。
非严格模式：v2_level ≤ target_chapter + 2 (=14) 即可。
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
# 中篇 (medius, 300-500 words) x6
# ============================================================

STORIES["cap12_01"] = {
    "title_la": "Mīles Fortis",
    "title_zh": "勇敢的士兵",
    "target_chapter": 12,
    "theme": "09 勇气",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第二人称",
    "text": (
        "Tū es mīles Rōmānus. Tū in castrīs es. "
        "Nox est. Caelum est nigrum. Stēllae in caelō sunt. "
        "Tū sōlus es. Tū in lectō iacēs. Somnum nōn habēs. "
        "Crās erit bellum. Crās erit diēs magnus. "
        "Tū dē bellō cōgitās. Tū dē hostibus cōgitās. "
        "Tū dē comitibus cōgitās. Tū timēs. "
        "Nēmō nōn timet. Omnēs timent — sed tū es mīles. "
        "Māne venit. Sōl in caelō surgit. Tū surgis. "
        "Tū arma tua capis. Gladius est gravis. Scūtum est magnum. "
        "Tū cum comitibus in aciem īs. "
        "Multī mīlitēs sunt. Multī equī sunt. "
        "Clāmor est magnus. Dux clāmat: 'Prō Rōmā!' "
        "Tū quoque clāmās: 'Prō Rōmā!' "
        "Tum pugna incipit. Hostēs currunt. Tū quoque curris. "
        "Gladius tuus lūcet in sōle. Scūtum tuum tē tegit. "
        "Hostis ad tē venit. Hostis est magnus. Hostis clāmat. "
        "Tū nōn movēs. Tū stās. Tū: 'Nōn timeō. Ego mīles Rōmānus sum.' "
        "Ferrum cum ferrō iungitur. Gladius tuus hostem tangit. "
        "Hostis cadit. Tū vīvus es. Tū vīcistī. "
        "Sed bellum nōn fīnītum est. Aliī hostēs veniunt. "
        "Tū iterum pugnās. Tū iterum stās. "
        "Tū comitēs tuōs vidēs — alius cadit, alius stat. "
        "Tū plōrāre nōn potes. Tū pugnāre dēbēs. "
        "Sōl in caelō movētur. Diēs longus est. "
        "Tū multās hōrās pugnās. Tū in aquā stās. "
        "Aqua est rubra. Aqua est calida. "
        "Tandem, hostēs fugiunt. Tandem, clāmor cessat. "
        "Tū stās in campō. Circum tē, corpora sunt. "
        "Tū vīvus es. Tū nōn intellegis cūr. "
        "Comitēs tuī aliī vīvī sunt, aliī mortuī. "
        "Tū ad castra redīs. Tū in lectō iacēs. "
        "Tū nōn es laetus. Tū nōn es trīstis. "
        "Tū nihil sentīs. Tū sōlum fessus es. "
        "Sed tū es mīles. Tū es fortis. "
        "Crās iterum pugnābis. Crās iterum stābis. "
        "Tū es Rōma. Tū numquam cadēs."
    ),
}

STORIES["cap12_02"] = {
    "title_la": "Tū, Mīles",
    "title_zh": "你，士兵",
    "target_chapter": 12,
    "theme": "09 勇气",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第二人称",
    "text": (
        "Tū in Galliā es. Tū mīles Rōmānus es. "
        "Castra magna sunt. Tū in castrīs es. "
        "Hiemps est. Caelum est griseum. Ventus flat. "
        "Tū prope ignem sedēs. Comitēs tuī circum tē sunt. "
        "Aliī dormiunt. Aliī loquuntur. Aliī arma cūrant. "
        "Tū nihil facis. Tū ignem spectās. "
        "Tū dē urbe tuā cōgitās. Dē domō. Dē familiā. "
        "Tū longē ā domō es. Tū in terrā aliēnā es. "
        "Tū Gallōs nōn intellegis. Tū linguam eōrum nōn scīs. "
        "Tū mōrēs eōrum nōn amās. Sed tū hīc es. "
        "Hodiē tū prīmam pugnam vidēs. Tū nōn fortis es. "
        "Tū timēs. Omnēs timent. "
        "Dux tūbam audīrī iubet. Tūba sonat — longa, magna. "
        "Tū surgis. Tū arma capis. Manus tuae trement. "
        "Tū ad pugnam īs. Tū curris. "
        "Tū nōn sōlus curris. Multī mīlitēs currunt. "
        "Tū clāmās. Multī clāmant. "
        "Tū prīmum hostem vidēs. Hostis magnus est. "
        "Hostis barbam longam habet. Hostis in linguā aliēnā clāmat. "
        "Tū parvus es. Tū nōn fortis es. "
        "Tū tamen nōn fugis. Tū stās. "
        "Gladius tuus in manū tuā est. Tū hostem spectās. "
        "Momentum longum est — sīcut aeternitās. "
        "Tum ferrum tangit ferrum. Tū pugnās. "
        "Tū nōn cōgitās. Corpus tuum movet. Gladius tuus ferit. "
        "Tū hostem vincis — aut hostis tē vincit? Tū nescīs. "
        "Post pugnam tū in castrīs es. Tū vīvus es. "
        "Tū corpus tuum spectās. Sanguis in manibus tuīs est. "
        "Sanguis tuus? Sanguis hostis? Tū nescīs. "
        "Tū nōn fortis es. Sed tū hīc es. "
        "Tū prīmam pugnam vīdistī. Et tū nōn fugistī. "
        "Comitēs tuī tē spectant. Aliī rīdent. Aliī tacent. "
        "Tū nōn rīdēs. Tū nōn plōrās. "
        "Tū sōlum in ignem spectās — sīcut ante pugnam. "
        "Sed tū nōn iam idem es. Tū mīles factus es. "
        "Et hoc est fortitūdō."
    ),
}

STORIES["cap12_03"] = {
    "title_la": "Mare unum",
    "title_zh": "唯一之海",
    "target_chapter": 12,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mare Nostrum, Ōceanus, Nīlus, Tiberis. Sunt quattuor aquae. "
        "Quattuor aquae — et tamen ūnum est imperium. "
        "Vir in portū stat. Vir est nauta. Vir multās terrās vīdit. "
        "Nauta: 'Ego quattuor aquās vīdī. Et ego dīcō: omnia sunt Rōmae.' "
        "Mare Nostrum est Rōmānum. Mare Nostrum in mediō imperiī est. "
        "Mare Nostrum Ītaliam et Graeciam et Hispāniam et Africam tangit. "
        "In Marī Nostrō, nāvēs multae sunt. Nāvēs frūmentum, vīnum, oleum portant. "
        "Nauta: 'Mare Nostrum est via. Mare Nostrum est vīta. "
        "Sine Marī Nostrō, Rōma nōn esset.' "
        "Ōceanus est magnus. Ōceanus in fīne imperiī est. "
        "Ōceanus Britanniam tangit. Ōceanus Galliam tangit. "
        "In Ōceanō, aquae sunt altae et nigrae. "
        "In Ōceanō, ventī sunt magnī et perīculōsī. "
        "Nautae Ōceanum timent. Sed Rōmānī Ōceanum nōn timent. "
        "Nauta: 'Ōceanus est mūrus. Sed Rōmānī mūrōs trānsīre possunt.' "
        "Nīlus est longus. Nīlus in Aegyptō est. "
        "Nīlus est pater Aegyptī. Nīlus terram fertilem facit. "
        "In Nīlō, aqua est nigra et bona. "
        "In Nīlō, multī piscēs sunt. Multae avēs in rīpīs Nīlī sunt. "
        "Nauta: 'Nīlus est vīta Aegyptī. Nīlus est dōnum deōrum.' "
        "Tiberis est brevis. Tiberis Rōmam tangit. "
        "Tiberis est flūmen Rōmānum. Tiberis urbem alit. "
        "In Tiberī, puerī natant. In Tiberī, nāviculae sunt. "
        "Nauta: 'Tiberis est parvus — sed Tiberis est Rōmānus. "
        "Tiberis est initium omnium.' "
        "Nauta quattuor aquās vīdit. Et nauta dīcit: "
        "'Quattuor aquae — sed ūnum imperium. "
        "Mare Nostrum, Ōceanus, Nīlus, Tiberis. "
        "Omnia sunt Rōmae. Omnia sunt in ūnō imperiō.' "
        "Et nauta ad nāvem suam redit. "
        "Nauta iterum in marī erit. "
        "Quattuor aquae — et ūnus nauta. Et Rōma."
    ),
}

STORIES["cap12_04"] = {
    "title_la": "Tria maria",
    "title_zh": "三片海",
    "target_chapter": 12,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mare Nostrum, Ōceanus, Mare Rubrum. Sunt tria maria. "
        "Tria maria — tria mundī. Et Rōmānī in omnibus sunt. "
        "Mare Nostrum in mediō est. Mare Nostrum est Rōmānum. "
        "Mare Nostrum est via inter terrās. "
        "Nāvēs ex Hispāniā ad Ītaliam veniunt. "
        "Nāvēs ex Ītaliā ad Graeciam eunt. "
        "Nāvēs ex Graeciā ad Asiam eunt. "
        "Mare Nostrum est plēnum nāvium. Plēnum vītae. "
        "In Marī Nostrō, īnsulae multae sunt: Sicilia, Crēta, Cyprus. "
        "Īnsulae sunt pulchrae. Īnsulae sunt fēcundae. "
        "Mercātor in nāve stat. Mercātor: "
        "'Mare Nostrum est nostrum. Hīc ego mercēs meās portō. "
        "Hīc ego pecūniam faciō. Mare Nostrum mihi omnia dat.' "
        "Ōceanus in fīne est. Ōceanus est magnus — sīne fīne. "
        "Ōceanus nōn est Rōmānus. Ōceanus est hostis. "
        "In Ōceanō, tempestātēs sunt magnae. "
        "In Ōceanō, nāvēs perīre possunt. "
        "Sed Ōceanus quoque est via. Ōceanus ad Britanniam dūcit. "
        "Ōceanus ad Hispāniam septentriōnālem dūcit. "
        "Nauta quī Ōceanum trānsit: "
        "'Ōceanus est sevērus — sed pulcher. "
        "Ōceanus nōs probat. Et Rōmānī probantur.' "
        "Mare Rubrum in oriente est. Mare Rubrum est calidum. "
        "Mare Rubrum est longē — prope Aegyptum et Arabiam. "
        "In Marī Rubrō, aqua est calida — sīcut aqua in balneō. "
        "In Marī Rubrō, piscēs multī colōrum sunt. "
        "In Marī Rubrō, mercēs pretiōsae veniunt: "
        "gemmae, aromata, vestēs pulchrae. "
        "Mercātor: 'Mare Rubrum est porta ad orientem. "
        "Mare Rubrum est porta ad Indōs. Ad Seres.' "
        "Senex in Rōmā sedet. Senex tria maria vīdit. "
        "Senex: 'Mare Nostrum est māter. Ōceanus est pater. "
        "Mare Rubrum est porta. Tria maria — ūnum imperium.' "
        "Et Rōmānī in omnibus maribus sunt. "
        "Tria maria. Tria mundī. Rōma ūna."
    ),
}

STORIES["cap12_05"] = {
    "title_la": "Duo frātrēs",
    "title_zh": "两兄弟",
    "target_chapter": 12,
    "theme": "32 友谊与孤独",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mārcus et Quīntus sunt frātrēs. Mārcus est magnus. Quīntus est parvus. "
        "Mārcus duodecim annōs habet. Quīntus septem annōs habet. "
        "Mārcus et Quīntus in eādem vīllā habitant. "
        "Mārcus semper in hortō labōrat. Quīntus semper in hortō lūdit. "
        "Pater dīcit: 'Mārce, tū es fīlius bonus. Tū labōrās. Tū mē iuvās.' "
        "Māter dīcit: 'Quīnte, tū es parvus. Tū lūdis. Sed tū quoque bonus es.' "
        "Quīntus frātrem suum spectat. Quīntus: 'Mārce, cūr semper labōrās? "
        "Lūde mēcum! Hīc pila est. Lūdāmus!' "
        "Mārcus: 'Nōn possum, Quīnte. Pater mē in hortō labōrāre iubet. "
        "Tū es parvus — tū potes lūdere. Ego nōn possum.' "
        "Quīntus trīstis est. Quīntus: 'Tū numquam mēcum lūdis. "
        "Tū semper labōrās. Ego sōlus lūdō.' "
        "Mārcus nihil dīcit. Mārcus labōrat. "
        "Sed Mārcus frātrem suum amat. "
        "Aliquandō, quandō pater nōn videt, Mārcus cum Quīntō lūdit. "
        "Mārcus pilam iacit. Quīntus pilam capit. "
        "Quīntus rīdet. Mārcus quoque rīdet. "
        "Sed tum pater venit. Pater: 'Mārce! Cūr nōn labōrās?' "
        "Mārcus iterum labōrat. Quīntus iterum sōlus lūdit. "
        "Vesperī, quandō sōl in caelō cadit, frātrēs in cubiculō sunt. "
        "Quīntus: 'Mārce, tū mē amās?' "
        "Mārcus: 'Ita, Quīnte. Ego tē amō. Tū es frāter meus.' "
        "Quīntus: 'Cūr tum nōn mēcum lūdis?' "
        "Mārcus: 'Quia ego sum magnus. Magnī puerī labōrant. "
        "Sed quandō tū magnus eris, ego quoque tēcum labōrābō. "
        "Et tum, amīcī erimus — nōn sōlum frātrēs.' "
        "Quīntus: 'Amīcī? Sīcut comitēs in bellō?' "
        "Mārcus: 'Ita. Sīcut comitēs. Sed melius — frātrēs.' "
        "Quīntus rīdet. Quīntus oculōs claudit. "
        "Mārcus frātrem parvum spectat. "
        "Mārcus: 'Ego semper tē cūrābō, Quīnte. Semper.' "
        "Et frātrēs in eōdem lectō dormiunt. "
        "Duo frātrēs. Duo corpora. Sed ūnum cor."
    ),
}

STORIES["cap12_06"] = {
    "title_la": "Mīles et dux",
    "title_zh": "兵与将",
    "target_chapter": 12,
    "theme": "06 权力",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "Dux in castrīs stat. Dux est magnus. Dux est sevērus. "
        "Mīlitēs ante ducem stant. Mīlitēs silent. "
        "Dux: 'Hodiē pugnāmus. Hostēs in colle sunt. "
        "Nōs in valle sumus. Collem capere dēbēmus.' "
        "Mīles ūnus: 'Dux, collis est altus. Hostēs sunt multī. "
        "Cūr nōn exspectāmus? Cūr nōn nocte pugnāmus?' "
        "Dux: 'Nocte nōn vidēmus. Nocte nōs vulnerāmur. "
        "Nunc sōl in caelō est. Nunc pugnāmus.' "
        "Mīles: 'Sed hostēs...' "
        "Dux: 'Tacē! Ego dux sum. Tū mīles es. "
        "Tū nōn cōgitās. Tū pugnās. Intellegis?' "
        "Mīles tacet. Mīles caput movet. "
        "Dux: 'Tū es bonus mīles. Ego tē in multīs pugnīs vīdī. "
        "Sed hodiē nōn est diēs ad cōgitandum. Hodiē est diēs ad pugnandum.' "
        "Mīles: 'Dux, ego nōn timeō mortem. Ego timeō nihil. "
        "Sed ego comitēs meōs cūrō. Ego nōlō eōs morī — sīne causā.' "
        "Dux mīlitem spectat. Dux diū silet. "
        "Dux: 'Tū cūrās comitēs tuōs. Hoc est bonum. "
        "Sed ego cūrō exercitum. Exercitus est magnus. "
        "Aliquandō, ūnus mīles morī dēbet — ut multī vīvant. Intellegis?' "
        "Mīles: 'Intellegō, dux. Sed...' "
        "Dux: 'Nōn est 'sed.' Aut pugnās, aut nōn. "
        "Sī nōn pugnās, tū nōn es mīles.' "
        "Mīles: 'Ego sum mīles, dux. Ego semper mīles fuī. Ego pugnābō.' "
        "Dux mīlitem tangit. Dux: 'Bene. Tū es bonus. "
        "Nunc ī ad comitēs tuōs. Dīc eīs: dux nōs dūcit. "
        "Dux scit quid facit. Dux nōs nōn dēserit.' "
        "Mīles abit. Mīles ad comitēs suōs it. "
        "Mīles: 'Dux nōs in collem dūcet. Nōs pugnābimus. "
        "Nōs vincēmus — aut moriēmur. Sed nōs nōn fugiēmus.' "
        "Comitēs silent. Tum ūnus: 'Nōs nōn fugimus. Nōs sumus Rōmānī.' "
        "Tuba sonat. Mīlitēs in collem currunt. "
        "Dux in summō stat. Dux mīlitēs suōs spectat. "
        "Dux nihil dīcit. Sed dux omnia videt. "
        "Post pugnam, mīlitēs in castra redeunt. "
        "Multī nōn redeunt. Sed mīles noster vīvus est. "
        "Mīles ducem videt. Dux mīlitem videt. "
        "Nūllī verbīs opus est. "
        "Mīles scit: dux nōs nōn dēseruit. "
        "Dux scit: mīles nōn fugit. "
        "Hoc est inter ducem et mīlitem — tacitum, sed magnum."
    ),
}

# ============================================================
# 中长篇 (longior, 500-800 words) x4
# ============================================================

STORIES["cap12_07"] = {
    "title_la": "Epistula ad amīcum",
    "title_zh": "致友人书",
    "target_chapter": 12,
    "theme": "32 友谊与孤独",
    "style": "书信",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "书信体",
    "text": (
        "Gāius Marcō amīcō suō salūtem dīcit. "
        "Amīce, multī diēs sunt quod tē nōn vīdī. "
        "Ego hīc in vīllā meā sum. Tū in urbe es. "
        "Inter nōs sunt multa mīlia passuum. "
        "Sed epistula mea ad tē volat — sīcut avis per caelum. "
        "Ego tē vidēre volō. Ego tēcum loquī volō. "
        "Memoria tuī semper in corde meō est. "
        "Quid agis? Quid in urbe novī est? "
        "Quid dē nostrīs amīcīs — dē Lūciō, dē Sextō? "
        "Lūcius nōbīs epistulam scrīpsit? "
        "Ego hīc in vīllā bene sum. Vīlla est pulchra. "
        "Hortus meus plēnus rosārum est. "
        "Rosae sunt rubrae, albae, roseae. "
        "Māne in hortō ambulō. Avēs in arboribus cantant. "
        "Vesperī in lectō legō — librōs veterēs, librōs bonōs. "
        "Sed sine amīcīs, haec omnia nōn sunt tanta. "
        "Sōl in caelō est pulcher — sed magis pulcher est quandō cum amīcō spectātur. "
        "Cibus est bonus — sed magis bonus quandō cum amīcō editur. "
        "Tū, Marce, es amīcus meus optimus. "
        "Meministīne diēs nostrōs in lūdō? "
        "Ego et tū in eādem sellā sedēbāmus. "
        "Magister nōs sevērus erat — sed nōs semper rīdēbāmus. "
        "Ego litterās nōn amābam — tū mē litterās amāre docuistī. "
        "Ego librōs nōn legēbam — tū mihi librōs dedistī. "
        "Propter tē, ego legere didicī. Propter tē, ego cōgitāre didicī. "
        "Nunc ego in vīllā meā librōs legō — et dē tē cōgitō. "
        "Tē invītō. Venī ad mē. Vīlla mea tē exspectat. "
        "Hīc est cubiculum parātum. Hīc est cibus bonus. "
        "Hīc est hortus pulcher. Hīc est amīcus quī tē amat. "
        "Venī. In hortō meō sub arbore sedēbimus. "
        "Vīnum bibēmus. Dē omnibus rēbus loquēmur. "
        "Dē lūdō, dē urbe, dē amīcīs, dē librīs, dē vītā. "
        "Sī potes, venī mox. Diēs sunt longī sine tē. "
        "Sī nōn potes, scrībe mihi epistulam. "
        "Verbīs tuīs ego nōn minus gaudeō quam praesentiā tuā. "
        "Valē, amīce. Valē, frāter animī meī. "
        "Cum tē videō, vīta mea plēna erit. "
        "Cum tē nōn videō, vīta mea vacua est. "
        "Scrībe mihi. Nōn oblīvīscere amīcī tuī. "
        "Ego semper tuī memor sum. "
        "Dat. in vīllā meā, Kalendīs Septembribus. "
        "Iterum valē. Gāius tuus tē salūtat."
    ),
}

STORIES["cap12_08"] = {
    "title_la": "Mīles sōlus",
    "title_zh": "孤独的士兵",
    "target_chapter": 12,
    "theme": "13 孤独",
    "style": "冷峻",
    "genre": "F 战争与征服",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Mīles sum. Sōlus in castrīs sum. "
        "Nox est. Nox est longa. Nox est nigra. "
        "Lūna in caelō est — sed lūna nōn mē iuvat. "
        "Stēllae in caelō sunt — sed stēllae longē sunt. "
        "Ego in lectō iaceō. Oculī meī apertī sunt. "
        "Somnum nōn habeō. Somnum numquam habeō — post bellum. "
        "Comitēs meī mortuī sunt. Herī vīvī erant. Hodiē nōn sunt. "
        "Ego eōs in campō vīdī. Ego eōs cadere vīdī. "
        "Ego nihil facere potuī. Ego sōlum spectāre potuī. "
        "Nunc in castrīs sōlus sum. "
        "Aliī mīlitēs in aliīs tabernāculīs dormiunt. "
        "Aliī rīdent. Aliī loquuntur. Ego sileō. "
        "Hostēs procul sunt. Sed in corde meō prope sunt. "
        "Ego eōs in somnīs videō. Ego eōs in umbrīs videō. "
        "In nocte, quandō ventus per castra flat, ego vōcēs audiō. "
        "Vōcēs comitum meōrum. "
        "Ūnus: 'Cūr ego mortuus sum?' "
        "Alius: 'Cūr tū vīvus es?' "
        "Ego nōn respondēre possum. Ego nescīō. "
        "Ego nōn melior sum quam illī. Ego nōn fortior sum. "
        "Fortūna mē servāvit. Nōn virtūs. Nōn deus. Fortūna. "
        "Aliquandō, ego in nocte surgō. Ego per castra ambulō. "
        "Ego ignem videō. Ego mīlitēs circum ignem videō. "
        "Illī mē vident — sed nōn mē vident. "
        "Oculī eōrum per mē eunt — sīcut ego iam mortuus sim. "
        "Fortasse ego iam mortuus sum. "
        "Fortasse ego mortuus sum in illō campō — cum comitibus meīs. "
        "Fortasse hoc quod nunc sum nōn est vīta — sed umbra. "
        "Umbra mea per castra ambulat. Umbra mea ignem spectat. "
        "Umbra nihil sentit. Umbra nihil cupit. "
        "Bellum mē mutāvit. Bellum omnia mutat. "
        "Puer quī Rōmā vēnit nōn iam est. "
        "Puer quī rīdēbat, quī currēbat, quī amābat — mortuus est. "
        "In locō eius, mīles stat. Mīles quī nōn rīdet. "
        "Mīles quī nōn currit — nisi ad pugnam. "
        "Mīles quī nōn amat. "
        "Sed herī, quandō pugnābāmus, ego aliquid sēnsī. "
        "Inter ferrum et sanguinem, ego aliquid sēnsī. "
        "Ego sēnsī comitēs meōs — etiam mortuōs. "
        "Illī mēcum erant. Illī mēcum pugnābant. "
        "Nōn corporibus — sed animīs. "
        "Fortasse mortuī nōn vērē mortuī sunt. "
        "Fortasse mortuī in nōbīs vīvunt. "
        "Ego nōn sōlus sum. Comitēs meī mēcum sunt. "
        "In corde meō, in memoriā meā, in animō meō. "
        "Et quandō ego quoque cadam — "
        "fortasse alius mīles mē in corde suō portābit. "
        "Et sīc bellum nōn fīnem habet. "
        "Et sīc mīlitēs nōn vērē moriuntur. "
        "Nunc dormīre possum. Valēte, comitēs. Valēte."
    ),
}

STORIES["cap12_09"] = {
    "title_la": "Mīles et bellum",
    "title_zh": "勇者与战争",
    "target_chapter": 12,
    "theme": "09 勇气",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mīles in oppidō est. Mīles est magnus. Mīles est fortis. "
        "Oppidum est parvum. Oppidum in monte est. "
        "Mīles in oppidō nātus est. Mīles in oppidō vīvit. "
        "Pater mīlitis quoque mīles fuit. "
        "Et pater patris quoque mīles fuit. "
        "Familia mīlitis semper Rōmam servāvit. "
        "Nunc bellum est. Hostēs ad oppidum veniunt. "
        "Hostēs sunt multī — sīcut undae maris. "
        "Hostēs ā septentriōne veniunt. "
        "Mīlitēs oppidī sunt paucī. Sed mīlitēs sunt fortēs. "
        "Mīles noster in mūrō stat. Mīles noster arma sua habet. "
        "Gladius in manū eius est. Scūtum in bracchiō eius est. "
        "Mīles nōn timet. Mīles numquam timet. "
        "Comitēs eius timent. Sed mīles eōs cōnfirmat. "
        "Mīles: 'Nōlīte timēre. Nōs sumus Rōmānī. "
        "Nōs in oppidō nostrō sumus. Nōs familiās nostrās servāmus. "
        "Nōs nōn fugimus. Nōs pugnāmus.' "
        "Hostēs prope sunt. Clāmor hostium auditur. "
        "Tum porta oppidī aperītur. Mīlitēs Rōmānī exeunt. "
        "Mīles noster prīmus exit. Mīles noster prīmus pugnat. "
        "Gladius eius per hostēs it — sīcut fulmen per caelum. "
        "Scūtum eius hostēs repellit — sīcut mūrus. "
        "Hostēs cadunt. Hostēs fugiunt. "
        "Sed mīles noster vulnera habet. "
        "Sanguis ex bracchiō eius fluit. "
        "Sanguis ex latere eius fluit. "
        "Sed mīles nōn cadit. Mīles stat. "
        "Comitēs: 'Redī! Vulnera tua sunt multa! Medicus tē exspectat!' "
        "Mīles: 'Nōn. Nōndum. Hostēs nōndum omnēs fugērunt. "
        "Dum hostis in terrā nostrā est, ego nōn redeō.' "
        "Mīles iterum pugnat. Iterum et iterum. "
        "Tandem, hostēs fugiunt. Tandem, victōria est. "
        "Mīles in terram cadit. Vulnera eius sunt gravia. "
        "Comitēs eum ad oppidum portant. "
        "Māter et pater eum vident. "
        "Māter plōrat. Pater silet. "
        "Mīles oculōs aperit. Mīles: 'Nōn plōrāte. Ego vīvō. "
        "Oppidum est salvum. Familia est salva. Hoc est magnum.' "
        "Medicus vulnera cūrat. Mīles in lectō manet. "
        "Sed mīles iterum surgit. Mīles iterum fortis est. "
        "Mīles in oppidō est. Mīles est magnus. Mīles est fortis. "
        "Et mīles in oppidō suō semper erit."
    ),
}

STORIES["cap12_10"] = {
    "title_la": "Frātrēs duo",
    "title_zh": "手足之间",
    "target_chapter": 12,
    "theme": "31 手足与对手",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duo frātrēs in oppidō sunt. Frāter prīmus est magnus. "
        "Frāter secundus est parvus. "
        "Frāter prīmus nōmen 'Gāius' habet. "
        "Frāter secundus nōmen 'Titus' habet. "
        "Gāius et Titus in eādem domō habitant. "
        "In eādem domō — sed in aliīs mundīs. "
        "Gāius est bonus puer. Gāius semper patrem et mātrem audit. "
        "Gāius in lūdō bene discit. Gāius librōs amat. "
        "Titus nōn est bonus puer. Titus nōn audit. "
        "Titus in lūdō nōn bene discit. Titus nōn librōs amat. "
        "Pater: 'Gāī, tū es fīlius bonus. Ecce liber — tibi dō.' "
        "Gāius librum capit. Gāius laetus est. "
        "Titus: 'Pater, cūr Gāius librum habet et ego nihil?' "
        "Pater: 'Quia Gāius bonus est. Tū nōn bonus es.' "
        "Titus īrātus est. Titus in cubiculum suum currit. "
        "Titus: 'Pater Gāium magis amat quam mē. "
        "Semper Gāius omnia bona habet. Ego nihil habeō.' "
        "In nocte, Titus Gāium in lectō videt. "
        "Gāius librum suum novum legit. "
        "Titus: 'Gāī, ostende mihi librum.' "
        "Gāius: 'Nōn. Pater mihi dedit. Liber est meus.' "
        "Titus: 'Tū semper omnia bona habēs. Ego nōn tē amō.' "
        "Gāius: 'Ego quoque nōn tē amō. Tū es malus frāter.' "
        "Frātrēs nōn iam loquuntur. "
        "Gāius in sellā suā sedet et librum legit. "
        "Titus in hortō sōlus lūdit. "
        "Māter hoc videt. Māter trīstis est. "
        "Māter Titum vocat. Māter: 'Tite, cūr trīstis es?' "
        "Titus: 'Gāius omnia habet. Ego nihil habeō. "
        "Pater Gāium amat. Mē nōn amat.' "
        "Māter: 'Tite, pater tē amat. Ego tē amō. "
        "Sed tū nōn es bonus puer. Sī bonus eris, pater tibi quoque librum dabit.' "
        "Titus: 'Ego bonus esse nōn possum. Ego nōn sum sīcut Gāius.' "
        "Māter: 'Nōn est necesse tē esse sīcut Gāium. "
        "Tū es Titus. Gāius est Gāius. "
        "Sed tū potes esse bonus Titus. Nōn bonus Gāius.' "
        "Titus mātrem spectat. Titus: 'Possumne?' "
        "Māter: 'Potes. Semper potes.' "
        "Titus ad Gāium it. Titus: 'Gāī, ego... ego nōn bonus fuī. "
        "Sed ego bonus esse volō. Tū mē iuvāre potes?' "
        "Gāius Titum spectat. Gāius diū silet. "
        "Tum Gāius: 'Tite, tū es frāter meus. "
        "Ego tē semper amāvī — etiam quandō nōn bonus fuistī.' "
        "Gāius Titō librum ostendit. "
        "Gāius: 'Ecce. In hōc librō, dē duōbus frātribus legitur. "
        "Illī quoque nōn semper amīcī erant. Sed posteā, amīcī factī sunt. "
        "Sīcut nōs.' "
        "Titus rīdet. Gāius rīdet. "
        "Frātrēs in eādem sellā sedent. "
        "Frātrēs eundem librum legunt. "
        "Nōn iam duo frātrēs. Nōn iam adversāriī. "
        "Sed frātrēs — vērē frātrēs."
    ),
}

# ============================================================
# 长篇 (longus, 800-1500 words) x2
# ============================================================

STORIES["cap12_11"] = {
    "title_la": "Nāvis in marī",
    "title_zh": "船在海上",
    "target_chapter": 12,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "旅人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nāvis in marī est. Nāvis est magna. Nāvis Rōmāna est. "
        "Nāvis ex Ōstiā ad Graeciam nāvigat. "
        "In nāve, multī virī sunt. Virī ad Graeciam eunt. "
        "Aliī mercātōrēs sunt. Aliī mīlitēs sunt. Aliī viātōrēs sunt. "
        "Inter eōs, ūnus vir est. Vir nōmen 'Lūcius' habet. "
        "Lūcius est iuvenis. Lūcius Rōmā venit. "
        "Lūcius numquam in marī fuit. Lūcius numquam longē ā domō fuit. "
        "Lūcius: 'Hoc est mare? Mare est tam magnum! "
        "Ego nōn crēdēbam mare esse tam magnum. "
        "In urbe, ego Tiberim vidēbam. Tiberis est parvus. "
        "Sed hoc — hoc est sīne fīne!' "
        "Nauta senex prope Lūcium stat. Nauta multōs annōs in marī est. "
        "Nauta: 'Tū prīmum in marī es, puer?' "
        "Lūcius: 'Ita. Ego prīmum in marī sum. Ego ad Graeciam eō. "
        "Ego Athēnās vidēre volō. Ego philosophōs audīre volō.' "
        "Nauta rīdet. Nauta: 'Philosophōs! Tū librōs legere potes in urbe. "
        "Cūr in Graeciam īs?' "
        "Lūcius: 'Quia in Graeciā philosophī sunt. In Graeciā sapientia est. "
        "Ego sapientiam quaerō.' "
        "Nauta: 'Sapientia nōn in Graeciā est, puer. Sapientia in marī est. "
        "Mare est magister optimus. Mare tē omnia docet.' "
        "Nāvis in marī movētur. Ventus vēla implet. "
        "Nāvis est pulchra — sīcut avis alba in aquā caeruleā. "
        "Lūcius in prōrā stat. Lūcius mare spectat. "
        "Aqua est caerulea. Aqua est clāra. "
        "In aquā, piscēs sunt. Piscēs saltant. "
        "Dēlphīnī prope nāvem natant. "
        "Lūcius: 'Dēlphīnī! Ecce — dēlphīnī!' "
        "Nauta: 'Dēlphīnī sunt amīcī nautārum. "
        "Dēlphīnī nōs dūcunt. Dēlphīnī sunt bonī.' "
        "Diēs in marī sunt longī. "
        "Lūcius in nāve ambulat. Lūcius cum nautīs loquitur. "
        "Nautae eī dē marī nārrant. "
        "Ūnus nauta: 'Ego multās terrās vīdī — Hispāniam, Africam, Graeciam, Asiam. "
        "Mare est via ad omnia. Mare nōs coniungit.' "
        "Alius nauta: 'Sed mare est perīculōsum. Mare est amīcus et hostis. "
        "Mare tē portat — sed mare tē quoque capere potest.' "
        "Lūcius: 'Vōs nōn timētis?' "
        "Nauta: 'Nōs timēmus — sed nōs in marī vīvimus. "
        "Mare est domus nostra. Domum nōn timēmus.' "
        "Nocte, quandō sōl in mare cadit, Lūcius in caelum spectat. "
        "Stēllae sunt multae. Stēllae sunt clārae. "
        "Lūcius: 'Stēllae nōs dūcunt?' "
        "Nauta: 'Ita. Stēllae sunt via nostra. "
        "Nautae stēllās spectant et sciunt quō eant. "
        "Stēllae numquam nōs dēserunt.' "
        "Subitō, tempestās venit. Ventus est magnus. "
        "Nūbēs nigrae in caelō sunt. Mare nōn iam caeruleum est — mare est nigrum. "
        "Undae sunt altae — sīcut montēs. "
        "Nāvis in undīs movētur — sīcut folium in ventō. "
        "Lūcius timet. Lūcius: 'Nōs perībimus!' "
        "Nauta senex: 'Nōn. Tacē et tenē. Mare nōs nōn capiet hodiē. "
        "Ego hanc tempestātem cognōscō. Mare nōs probat — nihil aliud.' "
        "Nautae labōrant. Nautae vēla contrahunt. Nautae nāvem regunt. "
        "Lūcius nautās spectat. Lūcius: 'Nautae sunt fortēs. "
        "Nautae nōn timent — vel sī timent, nōn ostendunt.' "
        "Tempestās per noctem dūrat. "
        "Māne, sōl iterum in caelō surgit. "
        "Mare iterum caeruleum est. Undae iterum parvae sunt. "
        "Nāvis est salva. Virī sunt salvī. "
        "Lūcius nautam senem spectat. "
        "Lūcius: 'Tū dīxistī mare esse magistrum. Nunc intellegō. "
        "Mare mē humilitātem docuit. Mare mē timōrem docuit. "
        "Et mare mē fortitūdinem docuit.' "
        "Nauta: 'Bene, puer. Tū didicistī. "
        "Nunc tū potes ad Graeciam īre — et philosophōs audīre. "
        "Sed mementō: mare tibi plūs dīxit quam philosophī.' "
        "Tandem, post multōs diēs, terra in caelō vidētur. "
        "Nauta: 'Graecia! Ecce — Graecia!' "
        "Lūcius terram spectat. Oculī eius plēnī sunt. "
        "Lūcius: 'Graecia. Tandem. "
        "Sed mare — mare erit semper in corde meō. "
        "Mare est magister. Mare est amīcus. Mare est vīta.' "
        "Nāvis in portum intrat. Lūcius in terram exit. "
        "Lūcius nautās salūtat. Lūcius: 'Grātiās vōbīs agō. "
        "Vōs mē docuistis. Ego nōn oblīvīscar.' "
        "Nauta senex: 'Valē, puer. Et quandō Rōmam redībis — "
        "nāvigā nōbīscum iterum.' "
        "Lūcius in Graeciā est. Lūcius Athēnās vidēbit. "
        "Lūcius philosophōs audiet. "
        "Sed Lūcius scit: vēra sapientia in marī est. "
        "Vēra sapientia in undīs, in ventīs, in stēllīs est. "
        "Et Lūcius semper nautārum memor erit."
    ),
}

STORIES["cap12_12"] = {
    "title_la": "Mīles et mors",
    "title_zh": "士兵与死亡",
    "target_chapter": 12,
    "theme": "01 生死",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mīles in bellō est. Bellum est magnum. Bellum est longum. "
        "Mīles in campō stat. Circum eum, corpora sunt. "
        "Corpora hostium. Corpora comitum. "
        "Mīles nōn timet. Mīles numquam timet. "
        "Pater eius mīles fuit. Pater patris mīles fuit. "
        "In familiā eius, omnēs virī mīlitēs fuērunt. "
        "Et omnēs in bellō mortuī sunt. "
        "Mīles noster hoc scit. Mīles noster hoc accipit. "
        "Mīles multōs hostēs necat. Gladius eius rubrum est. "
        "Manus eius sanguinem habent. Sed mīles nōn sentit. "
        "Mīles sōlum pugnat. Mīles sōlum vivit — ut pugnet. "
        "In pugnā, mīles nōn cōgitat. "
        "Cōgitāre est perīculōsum. Cōgitāre mortem fert. "
        "Mīles sōlum facit. Gladius movet. Corpus movet. "
        "Hostis cadit. Alius hostis venit. Et alius. "
        "Mīles nōn numerat. Numerus nōn est magnus. "
        "Ūnus, duo, decem, centum — quid interest? "
        "Post pugnam, mīles in campō stat. "
        "Sōl in caelō est. Sed sōl nōn calidus est. "
        "Mīles nihil sentit. "
        "Mīles vulnera habet. In bracchiō, in latere, in crūre. "
        "Sanguis fluit — lentē, sed certē. "
        "Mīles hoc scit. Mīles hoc videt. "
        "Sed mīles nōn plōrat. Mīles nōn clāmat. "
        "Mīles in terrā sedet. "
        "Mīles caelum spectat. Caelum est caeruleum. "
        "Nūbēs in caelō sunt — albae, lentae. "
        "Mīles: 'Nūbēs sunt pulchrae. Nūbēs nōn pugnant. "
        "Nūbēs nōn moriuntur. Nūbēs sōlum sunt.' "
        "Comēs ad mīlitem venit. Comēs est amīcus. "
        "Comēs: 'Amīce, vulnera tua sunt gravia. Medicum vocābō.' "
        "Mīles: 'Nōn. Medicus nōn mē iuvāre potest. "
        "Ego hoc sciō. Ego mortem meam videō.' "
        "Comēs: 'Nōn dīcās hoc! Tū vīvēs. Tū semper vīvēs.' "
        "Mīles: 'Nōn est malum morī. Mors est pars bellī. "
        "Mors est pars vītae. Ego nōn timeō.' "
        "Comēs plōrat. Comēs: 'Tū es amīcus meus. Tū es frāter meus. "
        "Quid faciam sine tē?' "
        "Mīles comitem spectat. "
        "Mīles: 'Tū vīvēs. Tū pugnābis. Tū Rōmam servābis. "
        "Et quandō tū quoque mortem vidēbis — "
        "mementō mē. Ego tē exspectābō.' "
        "Comēs mīlitem tangit. Comēs: 'Ubi tē exspectābis?' "
        "Mīles: 'Nescīō. Sed aliquō. "
        "Mīlitēs semper aliquō eunt. "
        "Mors nōn est fīnis — mors est porta.' "
        "Mīles oculōs claudit. "
        "Mīles patriam suam videt — Rōmam. "
        "Mīles urbem videt — templa, forum, Tiberim. "
        "Mīles mātrem suam videt — in vīllā, prope ignem. "
        "Mīles patrem suum videt — in armīs, fortem. "
        "Mīles: 'Māter... Pater... Ego veniō.' "
        "Comēs: 'Quid dīcis? Quid vidēs?' "
        "Sed mīles nōn respondet. "
        "Mīles in terrā iacet. Mīles nōn movet. "
        "Mīles mortuus est. "
        "Comēs mīlitem spectat. Comēs plōrat. "
        "Comēs: 'Valē, amīce. Valē, frāter. "
        "Ego tē numquam oblīvīscar. "
        "Ego nōmen tuum in corde meō portābō. "
        "Et quandō ego quoque cadam — "
        "nōmen tuum cum meō cadet. "
        "Et nōmina nostra simul in memoriā Rōmae manēbunt.' "
        "Comēs surgit. Comēs gladium suum capit. "
        "Bellum nōn fīnītum est. Bellum numquam fīnītur. "
        "Comēs iterum in pugnam it. "
        "Sed in corde eius, mīles vīvit. "
        "In memoriā eius, mīles stat. "
        "Mīles nōn est mortuus. "
        "Mīles est fortis. Mīles est Rōma. "
        "Et Rōma numquam morītur."
    ),
}


# ============================================================
# 主流程：评估并写入文件
# ============================================================

def main():
    cap_dir = REALITATES_DIR / "Cap12"
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
        existing = sorted(cap_dir.glob(f"Cap12_{story['title_la'].replace(' ', '_')}_{suffix}_*.md"))
        next_num = len(existing) + 1
        filename = f"Cap12_{story['title_la'].replace(' ', '_')}_{suffix}_{next_num:03d}.md"
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