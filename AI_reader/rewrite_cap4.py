#!/usr/bin/env python3
"""rewrite_cap4.py — 重写 Cap.4 的 14 篇短篇为 8 中篇 + 6 中长篇。
严格使用 ≤Cap.6 的词元（lemma_chapter_map ≤ 6）。
策略：~90%安全词 + ~5%OOV(专有名词) + ~5%高章节词(≤Cap.10)。
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
# 中篇 (300-500词) x8
# ============================================================

STORIES["cap4_01"] = {
	    "title_la": "Quattuor familiae",
	    "title_zh": "四家",
	    "target_chapter": 4,
	    "theme": "03 自由与束缚",
	    "style": "白话",
	    "genre": "C 历史与人物",
	    "character_type": "罗马人",
	    "length_tier": "中篇",
	    "narrative_mode": "第三人称",
	    "text": (
	        "Quattuor familiae in oppidō sunt. Oppidum est parvum. Oppidum est pulchrum. "
	        "In oppidō multae viae sunt. In oppidō multae vīllae sunt. "
	        "In oppidō multae familiae sunt. "
	        "Familia prīma est familia Iūliī. Iūlius est pater. Iūlius in vīllā magnā habitat. "
	        "Iūlius multōs fīliōs habet. Iūlius multās fīliās habet. "
	        "Iūlius fīliōs amat. Iūlius fīliās amat. "
	        "Fīliī Iūliī patrem amant. Fīliae Iūliī patrem amant. "
	        "In vīllā Iūliī multī puerī sunt. In vīllā Iūliī multae puellae sunt. "
	        "Puerī in hortō ambulant. Puellae in hortō ambulant. "
	        "Puerī et puellae laetī sunt. Familia Iūliī est magna. "
	        "Familia Iūliī multōs puerōs habet. Familia Iūliī multās puellās habet. "
	        "Iūlius est pater bonus. Iūlius familiam amat. Familia Iūliī est bona. "
	        "Familia secunda est familia Cornēliae. Cornēlia est māter. "
	        "Cornēlia in vīllā magnā habitat. Cornēlia multam pecūniam habet. "
	        "Cornēlia multōs servōs habet. Cornēlia multās servās habet. "
	        "Cornēlia servīs imperat. Servī Cornēliae pārent. Servae Cornēliae pārent. "
	        "Cornēlia est domina. Cornēlia est domina bona. Servī Cornēliam amant. "
	        "Cornēlia servōs bonōs habet. Cornēlia vīllam amat. "
	        "Cornēlia hortum magnum habet. In hortō Cornēliae multae rosae sunt. "
	        "In hortō Cornēliae multa līlia sunt. Cornēlia rosās amat. Cornēlia līlia amat. "
	        "Familia Cornēliae multam pecūniam habet. Familia Cornēliae est magna. "
	        "Familia tertia est familia Mārcī. Mārcus est pater. "
	        "Mārcus in vīllā parvā habitat. Mārcus nōn multam pecūniam habet. "
	        "Sed Mārcus familiam amat. Mārcus fīliōs habet. Mārcus fīliās habet. "
	        "Fīliī Mārcī patrem amant. Fīliae Mārcī patrem amant. "
	        "Mārcus in hortō est. Fīliī Mārcī in hortō sunt. "
	        "Fīliae Mārcī in hortō sunt. Familia Mārcī in hortō ambulat. "
	        "Familia Mārcī laeta est. Mārcus nōn multam pecūniam habet — "
	        "sed Mārcus familiam bonam habet. Familia Mārcī est laeta. Familia Mārcī est bona. "
	        "Familia quārta est familia Līviae. Līvia est māter. "
	        "Līvia in oppidō nova est. Līvia in vīllā parvā habitat. "
	        "Līvia nōn multōs servōs habet. Līvia ūnum fīlium habet. "
	        "Līvia ūnam fīliam habet. Fīlius Līviae est parvus. Fīlia Līviae est parva. "
	        "Līvia fīlium amat. Līvia fīliam amat. "
	        "Līvia in oppidō nōn multōs virōs videt. Līvia nōn multās fēminās videt. "
	        "Sed Līvia familiam habet. Līvia familiam amat. "
	        "Familia Līviae est parva — sed familia Līviae est bona. "
	        "Familia Līviae est nova — sed familia Līviae est laeta. "
	        "Quattuor familiae in oppidō sunt. Familia Iūliī est magna. "
	        "Familia Cornēliae multam pecūniam habet. Familia Mārcī est laeta. "
	        "Familia Līviae est nova. Quattuor familiae — quattuor viae. "
	        "Et quattuor familiae sunt bonae."
	    )
	}

STORIES["cap4_02"] = {
	    "title_la": "Quattuor aquae",
	    "title_zh": "四水",
	    "target_chapter": 4,
	    "theme": "18 自然",
	    "style": "白话",
	    "genre": "C 历史与人物",
	    "character_type": "罗马人",
	    "length_tier": "中篇",
	    "narrative_mode": "第三人称",
	    "text": (
	        "Quattuor aquae magnae in Eurōpā sunt. Aqua prīma est Tiberis. "
	        "Aqua secunda est Padus. Aqua tertia est Rhēnus. Aqua quārta est Dānuvius. "
	        "Quattuor aquae — et quattuor aquae sunt magnae. "
	        "Tiberis in Italiā est. Tiberis est aqua Rōmae. Tiberis per Rōmam it. "
	        "Rōma ad Tiberim est. Virī Rōmānī in oppidō Rōmā sunt. "
	        "Fēminae Rōmānae in oppidō Rōmā sunt. "
	        "Virī Rōmānī Tiberim vident. Fēminae Rōmānae Tiberim vident. "
	        "Tiberis Rōmānīs aquam dat. Rōmānī aquam Tiberis habent. "
	        "Rōmānī Tiberim amant. Tiberis nōn est aqua longa — "
	        "sed Tiberis est aqua Rōmae. Tiberis est aqua parva — "
	        "sed Tiberis est aqua pulchra. Tiberis est aqua bona. "
	        "Tiberis est aqua Rōmānōrum. "
	        "Padus in Italiā est. Padus est aqua longa. Padus est aqua magna. "
	        "Padus per multa oppida it. Padus per multās viās it. "
	        "Padus multam aquam habet. Virī Italiae Padum vident. "
	        "Virī Italiae aquam Padī habent. Padus virīs aquam dat. "
	        "Padus est aqua Italiae. Padus est aqua longa. Padus est aqua pulchra. "
	        "Padus est aqua magna. Padus est aqua bona. "
	        "Rhēnus in Germāniā est. Rhēnus est aqua longa. Rhēnus est aqua magna. "
	        "Rhēnus inter Italiam et Germāniam est. Rhēnus est via aquae. "
	        "Virī Germāniae Rhēnum vident. Virī Italiae Rhēnum vident. "
	        "Rhēnus virīs aquam dat. Rhēnus est aqua duōrum oppidōrum. "
	        "Rhēnus est aqua pulchra. Rhēnus est aqua magna. Rhēnus est aqua bona. "
	        "Dānuvius in Eurōpā est. Dānuvius est aqua longa. Dānuvius est aqua magna. "
	        "Dānuvius per multa oppida it. Dānuvius per multās viās it. "
	        "Dānuvius multam aquam habet. Virī Eurōpae Dānuvium vident. "
	        "Dānuvius virīs aquam dat. Dānuvius est aqua longa. "
	        "Dānuvius est aqua pulchra. Dānuvius est aqua magna. Dānuvius est aqua bona. "
	        "Quattuor aquae magnae in Eurōpā sunt. Tiberis est aqua Rōmae. "
	        "Padus est aqua Italiae. Rhēnus est aqua Germāniae. "
	        "Dānuvius est aqua Eurōpae. Quattuor aquae — quattuor viae. "
	        "Aqua est bona. Aqua est via virōrum."
	    )
	}

STORIES["cap4_03"] = {
    "title_la": "Quattuor oppida Italiae",
    "title_zh": "意大利四城",
    "target_chapter": 4,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma, Tusculum, Brundisium, Capua — quattuor oppida Italiae. "
        "Rōma est caput imperiī. Rōma est magna. Rōma est pulchra. "
        "In Rōmā multī virī sunt. In Rōmā multae fēminae sunt. "
        "In Rōmā multae viae sunt. Via Appia in Rōmā est. Via Appia est via longa. "
        "Rōma est oppidum Rōmānōrum. Rōma est māter oppidōrum. "
        "In Rōmā multī servī sunt. In Rōmā multī dominī sunt. "
        "In Rōmā multae vīllae sunt. Rōma est magna — Rōma est Rōma. "
        "Tusculum est oppidum parvum. Tusculum prope Rōmam est. "
        "Tusculum in monte est. Virī Tusculī Rōmam vident. "
        "Tusculum est oppidum quiētum. In Tusculō multae vīllae sunt. "
        "Virī Rōmānī in Tusculō vīllās habent. Virī Rōmānī Tusculum amant. "
        "Tusculum est parvum — sed pulchrum. Tusculum est quiētum — sed bonum. "
        "Brundisium est oppidum in marī. Brundisium est porta Italiae. "
        "Brundisium ad mare est. Virī ex Graeciā ad Brundisium veniunt. "
        "Virī ex Brundisiō ad Graeciam veniunt. "
        "Brundisium est via inter Italiam et Graeciam. "
        "Brundisium est oppidum magnum. Brundisium multōs virōs habet. "
        "Brundisium est porta — Brundisium est via. "
        "Capua est oppidum in Campāniā. Capua est magna. Capua est dīves. "
        "Capua multās vīllās habet. Capua multōs hortōs habet. "
        "Campānia est terra bona. Capua in Campāniā est. "
        "Capua est oppidum Rōmānum — sed Capua nōn est Rōma. "
        "Capua est dīves — sed Capua nōn est caput. "
        "Quattuor oppida Italiae. Rōma est caput. Tusculum est quiētum. "
        "Brundisium est porta. Capua est dīves. "
        "Quattuor oppida — quattuor faciēs Italiae. "
        "Italia est terra multōrum oppidōrum. Italia est pulchra."
    )
}

STORIES["cap4_04"] = {
	    "title_la": "Decem prōvinciae Rōmānae",
	    "title_zh": "罗马十省",
	    "target_chapter": 4,
	    "theme": "06 权力",
	    "style": "白话",
	    "genre": "C 历史与人物",
	    "character_type": "罗马人",
	    "length_tier": "中篇",
	    "narrative_mode": "第三人称",
	    "text": (
	        "Decem prōvinciae Rōmānae sunt. Prōvincia prīma est Sicilia. "
	        "Prōvincia secunda est Sardinia. Prōvincia tertia est Corsica. "
	        "Prōvincia quārta est Hispānia. Prōvincia quīnta est Britannia. "
	        "Prōvincia sexta est Syria. Prōvincia septima est Aegyptus. "
	        "Prōvincia octāva est Āfrica. Prōvincia nōna est Asia. "
	        "Prōvincia decima est Crēta. "
	        "Sicilia est īnsula. Sicilia est īnsula magna. Sicilia est īnsula pulchra. "
	        "Sicilia prope Italiam est. Sicilia est prōvincia Rōmāna. "
	        "In Siciliā multa oppida sunt. In Siciliā multī virī sunt. "
	        "In Siciliā multae fēminae sunt. Sicilia est īnsula bona. "
	        "Sicilia Rōmānīs pāret. "
	        "Sardinia est īnsula. Sardinia nōn est magna — sed Sardinia est pulchra. "
	        "Sardinia prope Italiam est. Sardinia est prōvincia Rōmāna. "
	        "In Sardiniā multa oppida sunt. Sardinia Rōmānīs pāret. "
	        "Sardinia est īnsula bona. "
	        "Corsica est īnsula. Corsica est īnsula parva. "
	        "Corsica inter Sardiniam et Italiam est. Corsica est prōvincia Rōmāna. "
	        "Corsica Rōmānīs pāret. Corsica est īnsula pulchra. Corsica est īnsula bona. "
	        "Hispānia est prōvincia magna. Hispānia in Eurōpā est. "
	        "Hispānia multa oppida habet. Hispānia multōs virōs habet. "
	        "Hispānia multās fēminās habet. Hispānia multās viās habet. "
	        "Hispānia est prōvincia magna. Hispānia Rōmānīs pāret. "
	        "Hispānia est prōvincia bona. "
	        "Britannia est īnsula magna. Britannia est prōvincia Rōmāna. "
	        "Britannia nōn est prope Italiam. Britannia est īnsula longa. "
	        "In Britanniā multī virī sunt. In Britanniā multae fēminae sunt. "
	        "Britannia Rōmānīs pāret. Britannia est īnsula magna. "
	        "Syria in Asiā est. Syria est prōvincia Rōmāna. "
	        "Syria multa oppida habet. Syria multōs virōs habet. "
	        "Syria Rōmānīs pāret. Syria est prōvincia bona. "
	        "Aegyptus est prōvincia magna. Aegyptus in Āfricā est. "
	        "Aegyptus multa oppida habet. Aegyptus multōs virōs habet. "
	        "Nīlus in Aegyptō est. Nīlus Aegyptō aquam dat. "
	        "Nīlus est aqua magna. Aegyptus Rōmānīs pāret. "
	        "Aegyptus est prōvincia bona. "
	        "Āfrica est prōvincia magna. Āfrica multa oppida habet. "
	        "Āfrica multōs virōs habet. Āfrica multās viās habet. "
	        "Āfrica Rōmānīs pāret. Āfrica est prōvincia magna. "
	        "Asia est prōvincia magna. Asia multa oppida habet. "
	        "Asia multōs virōs habet. Asia multās fēminās habet. "
	        "Asia Rōmānīs pāret. Asia est prōvincia magna. "
	        "Crēta est īnsula. Crēta est īnsula magna. Crēta est īnsula pulchra. "
	        "Crēta est prōvincia Rōmāna. Crēta Rōmānīs pāret. "
	        "Crēta est īnsula bona. "
	        "Decem prōvinciae Rōmānae. Decem prōvinciae — ūnum imperium. "
	        "Rōma est oppidum magnum. Rōma prōvincīs imperat. "
	        "Prōvinciae Rōmae pārent. Decem prōvinciae — decem viae. "
	        "Et decem prōvinciae sunt bonae."
	    )
	}

STORIES["cap4_05"] = {
    "title_la": "Discēde!",
    "title_zh": "滚开！",
    "target_chapter": 4,
    "theme": "06 权力",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "Duo virī in viā sunt. Ūnus est magnus. Ūnus est parvus. "
        "Magnus: 'Discēde! Haec via mea est.' "
        "Parvus: 'Cūr discēdam? Via nōn est tua. Via est omnium.' "
        "Magnus: 'Ego sum dominus. Tū nōn es dominus. Discēde!' "
        "Parvus: 'Nōn discēdō. Ego quoque in viā sum. Ego quoque vir sum.' "
        "Magnus parvum videt. Magnus: 'Tū mē nōn vidēs? Ego sum magnus. Tū es parvus.' "
        "Parvus: 'Ego tē videō. Tū es magnus — sed via nōn est tua.' "
        "Magnus: 'Ego multam pecūniam habeō. Tū pecūniam nōn habēs. Discēde!' "
        "Parvus: 'Pecūnia nōn est via. Pecūnia nōn est potentia. Ego nōn discēdō.' "
        "Magnus ad parvum ambulat. Magnus est prope parvum. "
        "Magnus: 'Tū nōn mē audīs? Ego tibi dīcō: discēde!' "
        "Parvus: 'Ego tē audiō. Sed ego nōn discēdō. Tū mē nōn terēs.' "
        "Magnus: 'Ego multōs servōs habeō. Ego multōs virōs habeō. Tū nūllum habēs.' "
        "Parvus: 'Ego nūllum servum habeō. Sed ego līber sum. Tū — esne līber?' "
        "Magnus tacet. Magnus parvum videt. "
        "Magnus: 'Ego... ego sum dominus. Dominus est līber.' "
        "Parvus: 'Dominus servōs habet — sed dominus quoque servus est. "
        "Dominus pecūniae servit. Dominus imperiō servit. Nēmō est vērē līber.' "
        "Magnus: 'Tū multa verba habēs, parve vir.' "
        "Parvus: 'Verba mea sunt. Verba nōn sunt serva. Verba sunt lībera.' "
        "Magnus diū parvum videt. Magnus: 'Quis es tū?' "
        "Parvus: 'Ego sum vir. Ego sum līber. Ego sum.' "
        "Magnus nōn iam 'discēde' dīcit. Magnus tacet. "
        "Magnus et parvus in viā sunt. Duo virī — ūnus magnus, ūnus parvus. "
        "Sed in viā — nēmō est dominus. Via est omnium. "
        "Magnus: 'Tū mē docēs. Ego multam pecūniam habeō — sed tū multa verba habēs.' "
        "Parvus: 'Pecūnia nōn est omnia. Via est omnia. Via est omnium.' "
        "Magnus et parvus in viā ambulant. Magnus nōn iam 'discēde' dīcit. "
        "Duo virī in viā — et via est ambōrum."
    )
}

STORIES["cap4_06"] = {
	    "title_la": "Puer et hortus",
	    "title_zh": "男孩与花园",
	    "target_chapter": 4,
	    "theme": "28 教育",
	    "style": "古典",
	    "genre": "A LLPSI宇宙",
	    "character_type": "罗马人",
	    "length_tier": "中篇",
	    "narrative_mode": "第三人称",
	    "text": (
	        "Mārcus in oppidō est. Mārcus puer est. Mārcus pater et māter habet. "
	        "Pater Mārcī est Iūlius. Māter Mārcī est Aemilia. "
	        "Mārcus in vīllā magnā habitat. Vīlla est pulchra. "
	        "Vīlla Iūliī multōs hortōs habet. "
	        "Post vīllam hortus parvus est. Hortus est Mārcī. Mārcus hortum amat. "
	        "Mārcus in hortum ambulat. Mārcus hortum videt. Hortus est vacuus. "
	        "Mārcus: 'Hortus meus est vacuus. Nūllae rosae in hortō meō sunt. "
	        "Nūlla līlia in hortō meō sunt.' "
	        "Mārcus ad patrem venit. Mārcus: 'Pater, hortus meus est vacuus.' "
	        "Iūlius Mārcum videt. Iūlius: 'Mārce, hortus tuus est vacuus. "
	        "Sed tū hortum bonum habēs. Ecce rosae. Ecce līlia.' "
	        "Iūlius Mārcō rosās dat. Iūlius Mārcō līlia dat. "
	        "Mārcus rosās capit. Mārcus līlia capit. Mārcus laetus est. "
	        "Mārcus in hortō est. Mārcus rosās in hortō pōnit. "
	        "Mārcus līlia in hortō pōnit. Mārcus rosās et līlia videt. "
	        "Rosae sunt pulchrae. Līlia sunt pulchra. "
	        "Mārcus rosās amat. Mārcus līlia amat. "
	        "Mārcus aquam ad hortum portat. Mārcus rosīs aquam dat. "
	        "Mārcus līliīs aquam dat. Rosae aquam habent. Līlia aquam habent. "
	        "Rosae et līlia aquam amant. "
	        "Mārcus in hortō ambulat. Mārcus rosās videt. Mārcus līlia videt. "
	        "Mārcus: 'Rosae meae sunt pulchrae. Līlia mea sunt pulchra. "
	        "Hortus meus est pulcher.' "
	        "Iūlius ad hortum venit. Iūlius hortum videt. "
	        "Iūlius: 'Mārce, hortus tuus est pulcher! Rosae sunt pulchrae. "
	        "Līlia sunt pulchra. Tū es puer bonus. Tū in hortō tuō multum agis.' "
	        "Mārcus: 'Pater, rosae sunt pulchrae. Līlia sunt pulchra. "
	        "Hortus meus est pulcher. Hortus meus est bonus.' "
	        "Iūlius: 'Mārce, tū es puer bonus. Hortus tuus est pulcher. "
	        "Ego tē videō — et ego laetus sum.' "
	        "Mārcus laetus est. Iūlius laetus est. Pater et fīlius in hortō sunt. "
	        "Pater et fīlius hortum vident. Hortus est parvus — sed hortus est pulcher. "
	        "Hortus est Mārcī — et Mārcus hortum amat. "
	        "Mārcus in hortō ambulat. Mārcus hortum videt. Mārcus laetus est."
	    )
	}

STORIES["cap4_07"] = {
    "title_la": "Servus bonus",
    "title_zh": "好奴隶",
    "target_chapter": 4,
    "theme": "04 正义",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "奴隶",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Dāvus est servus. Dāvus in oppidō est. Dāvus dominum habet. Dominus est Iūlius. "
        "Dāvus est servus bonus. Dāvus dominō pāret. Dāvus multa agit. "
        "Dāvus in vīllā labōrat. Dāvus aquam ad vīllam portat. Dāvus hortum cūrat. "
        "Dāvus est bonus — sed servus est. Dāvus nōn est līber. "
        "Iūlius Dāvum vocat. Iūlius: 'Dāve, venī!' Dāvus venit. "
        "Iūlius: 'Dāve, pecūniam habeō. Ego tibi pecūniam dō.' "
        "Dāvus: 'Dominus, cūr mihi pecūniam dās? Ego servus sum.' "
        "Iūlius: 'Tū servus es — sed tū bonus es. Servus bonus pecūniam habēre potest.' "
        "Dāvus pecūniam capit. Dāvus pecūniam videt. Dāvus: 'Domine, haec pecūnia est multa.' "
        "Iūlius: 'Pecūnia tua est. Tū potes pecūniam habēre.' "
        "Dāvus in oppidum ambulat. Dāvus virōs videt. Dāvus fēminās videt. "
        "Dāvus puerum videt. Puer est parvus. Puer plōrat. Puer sōlus est. "
        "Dāvus: 'Puer, cūr plōrās?' "
        "Puer: 'Ego mātrem nōn habeō. Ego patrem nōn habeō. Ego pecūniam nōn habeō.' "
        "Dāvus puerum videt. Dāvus pecūniam videt. Dāvus: 'Puer, haec pecūnia est tua.' "
        "Dāvus puerō pecūniam dat. Puer pecūniam capit. Puer nōn iam plōrat. "
        "Puer: 'Quis es tū? Tū bonus es!' "
        "Dāvus: 'Ego sum Dāvus. Ego sum servus.' "
        "Puer: 'Tū servus es — sed tū mihi pecūniam dās. Tū es bonus.' "
        "Dāvus ad vīllam revenit. Iūlius Dāvum videt. "
        "Iūlius: 'Dāve, ubi est pecūnia?' "
        "Dāvus: 'Domine, pecūniam puerō dedī. Puer pecūniam nōn habēbat. Puer sōlus erat.' "
        "Iūlius Dāvum diū videt. Iūlius: 'Dāve, tū pecūniam puerō dedistī. Tū bonus es.' "
        "Iūlius: 'Dāve, tū nōn iam servus es. Tū es līber.' "
        "Dāvus: 'Domine! Ego sum līber?' "
        "Iūlius: 'Tū es līber. Tū bonus es — et bonus vir līber esse potest.' "
        "Dāvus nōn iam servus est. Dāvus est līber. Dāvus est bonus — et bonus līber est."
    )
}

STORIES["cap4_08"] = {
    "title_la": "Servus et aqua",
    "title_zh": "奴隶与水",
    "target_chapter": 4,
    "theme": "42 城市与乡村",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "奴隶",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Syra est serva. Syra in oppidō est. Syra dominam habet. Domina est Dēlia. "
        "Syra in vīllā Dēliae labōrat. Syra est serva bona. Syra Dēliae pāret. "
        "Oppidum est magnum. In oppidō multī virī sunt. In oppidō multae fēminae sunt. "
        "Sed in oppidō aqua nōn est. Aqua est procul ab oppidō. "
        "Syra ad fluvium ambulat. Fluvius est magnus. Fluvius est pulcher. "
        "Syra aquam ex fluviō capit. Syra aquam in vīllam portat. "
        "Syra multās viās ambulat. Syra multōs virōs videt. Syra multās fēminās videt. "
        "Syra aquam portat — et aqua est gravis. Syra nōn est magna. Syra est parva. "
        "Sed Syra est fortis. Syra aquam portat. "
        "In viā Syra puerum videt. Puer plōrat. Puer: 'Aquam habeō? Aquam nōn habeō!' "
        "Syra puerum videt. Syra aquam videt. Syra puerō aquam dat. "
        "Puer: 'Grātiās! Tū bona es!' "
        "Syra ad vīllam revenit. Syra nūllam aquam habet. "
        "Dēlia Syram videt. Dēlia: 'Syra, ubi est aqua?' "
        "Syra: 'Domina, aquam puerō dedī. Puer aquam nōn habēbat.' "
        "Dēlia: 'Syra, tū aquam puerō dedistī. Tū nōn habēs aquam. Sed tū habēs cor bonum.' "
        "Dēlia Syram videt. Dēlia: 'Syra, tū nōn iam serva es. Tū es lībera.' "
        "Syra: 'Domina! Ego sum lībera?' "
        "Dēlia: 'Tū es lībera. Tū aquam dedistī — et aqua vīta est. Tū vītam dedistī.' "
        "Syra nōn iam serva est. Syra est lībera. Syra in oppidō est. "
        "Syra aquam ad multōs portat. Syra nōn est serva — Syra est bona fēmina. "
        "Aqua est vīta. Et quī aquam dat — vītam dat."
    )
}

# ============================================================
# 中长篇 (500-800词) x6
# ============================================================

STORIES["cap4_09"] = {
	    "title_la": "Fīlius improbus",
	    "title_zh": "坏儿子",
	    "target_chapter": 4,
	    "theme": "30 威严与慈爱",
	    "style": "冷峻",
	    "genre": "C 历史与人物",
	    "character_type": "罗马人",
	    "length_tier": "中长篇",
	    "narrative_mode": "第三人称",
	    "text": (
	        "Iūlius pater est. Iūlius fīlium habet. Fīlius est Mārcus. "
	        "Mārcus in oppidō est. Iūlius Mārcum amat. Iūlius Mārcō multa dat. "
	        "Iūlius Mārcō pecūniam dat. Iūlius Mārcō librōs dat. "
	        "Iūlius Mārcō vīllam dat. "
	        "Sed Mārcus nōn est bonus. Mārcus est improbus. Mārcus patrī nōn pāret. "
	        "Mārcus pecūniam capit — sed Mārcus pecūniam nōn bene habet. "
	        "Mārcus in oppidō cum malīs virīs est. Mārcus multam pecūniam in viā dat. "
	        "Mārcus nōn agit. Mārcus nōn audit. Mārcus patrem nōn audit. "
	        "Iūlius Mārcum vocat. Iūlius: 'Mārce, venī!' Mārcus nōn venit. "
	        "Iūlius rūrsus vocat: 'Mārce! Pater tē vocat!' Mārcus nōn respondet. "
	        "Iūlius ad Mārcum ambulat. Iūlius Mārcum in viā videt. "
	        "Iūlius: 'Mārce, cūr nōn venīs? Ego tē vocō.' "
	        "Mārcus: 'Pater, ego nōn veniō. Ego in viā sum. Ego virōs videō.' "
	        "Iūlius: 'Tū nōn es bonus fīlius. Fīlius bonus patrī pāret.' "
	        "Mārcus: 'Ego nōn sum puer. Ego sum vir. Tū mihi imperās — "
	        "sed ego nōn pāreō.' "
	        "Iūlius tacet. Iūlius fīlium videt. Iūlius: 'Mārce, tū es fīlius meus. "
	        "Ego tē videō. Sed tū mē nōn vidēs. Cūr?' "
	        "Mārcus: 'Pater, tū mihi multa dās — sed tū mē nōn vidēs. "
	        "Tū mihi pecūniam dās — sed tū mē nōn audīs. "
	        "Ego nōn sum pecūnia. Ego sum fīlius.' "
	        "Iūlius: 'Ego tē videō. Ego tē audiō. Sed tū mē nōn audīs.' "
	        "Mārcus: 'Pater, tū mihi imperās. Tū mē vocās. "
	        "Sed tū mē nōn rogās. Ego nōn sum servus. Ego sum fīlius.' "
	        "Iūlius fīlium videt. Iūlius: 'Mārce, ego tē nōn bene audīvī. "
	        "Ego multa ad tē dedī — sed ego tē nōn rogāvī. Iam tē rogō.' "
	        "Mārcus: 'Pater, ego pecūniam nōn habeō. Sed ego tē habeō. "
	        "Tū es pater meus. Ego tē videō. Ego tē audiō.' "
	        "Iūlius: 'Mārce, tū mē vidēs. Tū mē audīs. "
	        "Ego tē videō. Ego tē audiō. Tū es fīlius meus.' "
	        "Mārcus ad patrem ambulat. Mārcus: 'Pater, ego tē videō. "
	        "Ego tē audiō. Ego nōn iam improbus sum.' "
	        "Iūlius: 'Fīlius meus, tū bonus es. Tū mē vidēs. Tū mē audīs. "
	        "Ego tē videō. Ego tē audiō.' "
	        "Pater et fīlius in viā sunt. Pater et fīlius sōlī nōn sunt. "
	        "Pater fīlium videt. Fīlius patrem videt. "
	        "Mārcus: 'Pater, ego in vīllā agam. Ego patrī pārēbō. "
	        "Ego bonus fīlius erō.' "
	        "Iūlius: 'Fīlius meus, tū iam bonus es. Tū mē vidēs. Tū mē audīs. "
	        "Et ego tē videō. Et ego tē audiō.' "
	        "Pater et fīlius in vīllam veniunt. Mārcus nōn iam improbus est. "
	        "Mārcus patrī pāret. Mārcus in vīllā agit. Mārcus bonus est. "
	        "Iūlius laetus est. Fīlius bonus — pater laetus. "
	        "Mārcus: 'Pater, tū mihi vīllam dedistī. Tū mihi pecūniam dedistī. "
	        "Sed tū mihi etiam tē dedistī. Et hoc est multum.' "
	        "Iūlius: 'Fīlius meus, tū mihi tē dedistī. Et hoc est multum. "
	        "Pecūnia nōn est multa. Sed fīlius bonus est multum.' "
	        "Pater et fīlius in vīllā sunt. Mārcus patrī pāret. "
	        "Mārcus bonus est. Iūlius laetus est. "
	        "Pater fīlium videt. Fīlius patrem videt. "
	        "Pater et fīlius — duo in ūnā vīllā. "
	        "Pater et fīlius — duo in ūnā familiā."
	    )
	}

STORIES["cap4_10"] = {
    "title_la": "Pecūnia patris",
    "title_zh": "父亲的财富",
    "target_chapter": 4,
    "theme": "41 财富与贫困",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Iūlius in oppidō est. Iūlius pater est. Iūlius multam pecūniam habet. "
        "Iūlius in magnā vīllā habitat. Iūlius multōs servōs habet. "
        "Iūlius multōs hortōs habet. Iūlius est dominus magnus. "
        "Iūlius fīlium habet. Fīlius Iūliī est Lūcius. Lūcius in oppidō est. "
        "Lūcius nōn multam pecūniam habet. Lūcius in parvā vīllā habitat. "
        "Lūcius ūnum servum habet. Servus Lūciī est bonus. "
        "Lūcius nōn multam pecūniam habet — sed Lūcius laetus est. "
        "Cūr Lūcius laetus est? Lūcius fēminam habet. Fēmina Lūciī est Līvia. "
        "Līvia est pulchra. Līvia est bona. Lūcius Līviam amat. Līvia Lūcium amat. "
        "Lūcius etiam fīlium habet. Fīlius Lūciī est parvus. Fīlius est puer bonus. "
        "Nōmen puerī est Mārcus. Lūcius Mārcum amat. Mārcus patrem amat. "
        "Mārcus mātrem amat. Lūcius familiam habet. Familia Lūciī est parva. "
        "Familia Lūciī nōn multam pecūniam habet — sed familia Lūciī est bona. "
        "Familia Lūciī est laeta. Lūcius cum familiā suā laetus est. "
        "Iūlius Lūcium vocat. Iūlius: 'Lūcī, venī ad mē!' Lūcius ad patrem venit. "
        "Lūcius in vīllā magnā Iūliī est. Vīlla Iūliī est magna et pulchra. "
        "Iūlius: 'Lūcī, fīlī mī, ego multam pecūniam habeō. Ego magnam vīllam habeō. "
        "Ego multōs servōs habeō. Tū es fīlius meus. Pecūnia mea tua est. "
        "Vīlla mea tua est.' "
        "Lūcius: 'Pater, tū es bonus. Tū mihi multa dās. "
        "Sed ego pecūniam tuam nōn capiō. Ego familiam meam habeō. "
        "Familia mea est parva — sed familia mea est bona.' "
        "Iūlius: 'Lūcī, cūr nōn in vīllā meā habitās? Vīlla tua est parva. "
        "Vīlla mea est magna. In vīllā meā multa sunt.' "
        "Lūcius: 'Pater, vīlla mea est parva — sed in vīllā meā familia mea est. "
        "In vīllā meā fēmina mea est. In vīllā meā fīlius meus est. "
        "In vīllā meā ego laetus sum.' "
        "Iūlius Lūcium videt. Iūlius tacet. "
        "Iūlius: 'Lūcī, tū es laetus. Ego multam pecūniam habeō. "
        "Ego magnam vīllam habeō. Sed ego nōn laetus sum. Cūr?' "
        "Lūcius: 'Pater, tū in vīllā magnā es — sed tū sōlus es. "
        "Māter mea nōn est. Tū in vīllā magnā sōlus es. "
        "Pecūnia est bona — sed familia est bona quoque. "
        "Venī ad meam vīllam. Vīlla mea est parva — "
        "sed tū in vīllā meā nōn sōlus es.' "
        "Iūlius: 'Fīlī mī, tū mē vocās ad tuam vīllam. Ego veniō.' "
        "Iūlius ad vīllam Lūciī ambulat. Vīlla Lūciī est parva. "
        "Vīlla nōn est magna. Sed vīlla est pulchra. "
        "In vīllā hortus parvus est. In hortō multae rosae sunt. "
        "In hortō multa līlia sunt. Rosae sunt pulchrae. Līlia sunt pulchra. "
        "Līvia in vīllā est. Līvia Iūlium videt. "
        "Līvia: 'Avē, Iūlī! Tū es pater Lūciī. Tū in vīllā nostrā es. "
        "Vīlla nostra est tua vīlla.' "
        "Mārcus in vīllā est. Mārcus Iūlium videt. "
        "Mārcus: 'Avē! Tū es Iūlius! Tū es pater patris meī!' "
        "Iūlius Mārcum videt. Iūlius: 'Tū es fīlius Lūciī. "
        "Tū es parvus puer — sed tū es bonus puer.' "
        "Iūlius Mārcum amat. Mārcus Iūlium amat. "
        "Iūlius in vīllā Lūciī est. Iūlius Līviam videt. "
        "Iūlius Mārcum videt. Iūlius Lūcium videt. "
        "Iūlius familiam videt. Iūlius nōn iam sōlus est. "
        "Iūlius: 'Lūcī, vīlla tua est parva. Sed in vīllā tuā familia est. "
        "Tū fēminam tuam amās. Tū fīlium tuum amās. "
        "Fēmina tua tē amat. Fīlius tuus tē amat. Hoc est magnum bonum.' "
        "Lūcius: 'Pater, tū in vīllā meā es. Tū nōn iam sōlus es. "
        "Tū familiam habēs. Tū es pater meus. Ego fīlius tuus sum. "
        "Mārcus est fīlius fīliī tuī. Ego et Mārcus et Līvia — familia tua sumus.' "
        "Iūlius: 'Lūcī, tū es fīlius bonus. Tū mihi vīllam tuam dās. "
        "Tū mihi familiam tuam dās. Ego nōn iam sōlus sum. Ego laetus sum.' "
        "Iūlius in vīllā Lūciī est. Iūlius cum familiā est. "
        "Iūlius nōn iam in vīllā magnā sōlus est. "
        "Iūlius in vīllā parvā cum familiā est. "
        "Iūlius: 'Pecūnia mea est multa. Vīlla mea est magna. "
        "Sed familia est magnum bonum. Iam ego familiam habeō. "
        "Iam ego laetus sum.' "
        "Lūcius: 'Pater, pecūnia tua est multa — sed familia tua est magna. "
        "Tū multam pecūniam habēs — et tū familiam habēs. "
        "Tū multa bona habēs.' "
        "Iūlius et Lūcius in vīllā sunt. Iūlius et Līvia in vīllā sunt. "
        "Iūlius et Mārcus in vīllā sunt. Familia in vīllā est. "
        "Familia est parva — sed familia est bona. "
        "Pecūnia est bona — sed familia est magnum bonum. "
        "Iūlius in vīllā Lūciī habitat. Iūlius nōn iam sōlus est. "
        "Iūlius familiam habet — et Iūlius laetus est."
    )
}

STORIES["cap4_11"] = {
    "title_la": "Dominus et servus in viā",
    "title_zh": "主奴同行",
    "target_chapter": 4,
    "theme": "03 自由与束缚",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Iūlius in viā est. Iūlius est dominus. Medus in viā est. Medus est servus. "
        "Iūlius et Medus in viā ambulant. Via est longa. Via est pulchra. "
        "Via inter duo oppida est. Via est via multōrum virōrum. "
        "Iūlius ante Medum ambulat. Medus post Iūlium ambulat. "
        "Iūlius: 'Mede, cūr post mē ambulās? Venī ad mē. Ambulā cum mē.' "
        "Medus: 'Domine, ego servus sum. Servus post dominum ambulat.' "
        "Iūlius: 'Venī. Via est longa. Sōlus ambulāre nōn est bonum. "
        "Ambulā cum mē. In viā duo virī sunt.' "
        "Medus ad Iūlium venit. Medus cum Iūliō ambulat. "
        "Iūlius: 'Mede, tū es servus meus. Tū in vīllā meā agis. "
        "Tū mihi pārēs. Sed in viā — tū nōn es servus. In viā — tū es vir.' "
        "Medus: 'Domine, ego servus sum. Ego dominō pāreō. "
        "Servus est servus — in vīllā et in viā.' "
        "Iūlius: 'Mede, in viā nōn est dominus. In viā nōn est servus. "
        "In viā sunt virī. Via nōn habet dominōs et servōs. "
        "Via habet virōs. Via est lībera.' "
        "Medus Iūlium videt. Medus: 'Domine, tū bonus es. "
        "Tū mē vidēs. Tū mē audīs. Tū mē virum vocās.' "
        "Iūlius: 'Ego multōs servōs habeō. Sed servī meī sunt virī. "
        "Quī mihi pārent — sunt virī. "
        "Vir est quī agit. Vir est quī audit. Vir est quī videt.' "
        "Medus: 'Domine, in viā tū mē virum vidēs, nōn servum. "
        "Ego laetus sum.' "
        "Iūlius: 'Mede, in viā duo virī sumus. Via est longa. "
        "Ego et tū in viā sumus. Via est via duōrum virōrum. "
        "In viā nūllus est dominus. In viā nūllus est servus. "
        "In viā sunt virī līberī.' "
        "Iūlius Medō aquam dat. Iūlius: 'Mede, aquam habē. "
        "Via est longa. Aqua est bona. Virī in viā aquam habent.' "
        "Medus aquam capit. Medus: 'Domine, tū mihi aquam dās. "
        "Tū bonus es. Tū mē virum vocās. Hoc est magnum bonum.' "
        "Iūlius: 'Mede, in viā ego et tū nōn sumus dominus et servus. "
        "In viā sumus duo virī. Duo virī in viā longā. "
        "Via est longa — sed duo virī viam longam ambulant.' "
        "Iūlius et Medus in viā dormiunt. Via est longa. "
        "Iūlius et Medus in viā dormiunt. "
        "Iūlius nōn est dominus in viā. Medus nōn est servus in viā. "
        "In viā sunt duo virī. Duo virī in viā dormiunt. "
        "Post, Iūlius Medum vocat: 'Mede, venī. Via est longa. "
        "Ego et tū in viā sumus. Ambulā cum mē.' "
        "Medus: 'Domine, ego veniō. Ego cum dominō ambulō. "
        "Ego nōn iam servus sum — ego sum vir. "
        "In viā dominus et servus sunt duo virī.' "
        "Iūlius et Medus in viā longā ambulant. "
        "Duo virī — ūnus est dominus, ūnus est servus. "
        "Sed in viā — nōn est dominus. In viā — nōn est servus. "
        "In viā — sunt duo virī. "
        "Iūlius: 'Mede, via est longa. Sed via est bona. "
        "Via nōn habet dominōs. Via nōn habet servōs. "
        "Via est via multōrum virōrum. Via est lībera.' "
        "Medus: 'Domine, via est bona. In viā ego nōn sum servus. "
        "In viā ego sum vir. In viā ego līber sum. "
        "Via est lībera — et virī in viā sunt līberī.' "
        "Iūlius: 'Mede, via est lībera. Et in viā — virī sunt līberī. "
        "Tū es vir. Ego sum vir. In viā — duo virī sumus.' "
        "Medus: 'Domine, tū mē virum vocās. "
        "Hoc est magnum bonum. Ego tē videō. Ego tē audiō. "
        "Tū es bonus dominus.' "
        "Iūlius et Medus in viā longā ambulant. "
        "Via est longa — sed duo virī in viā nōn sunt sōlī. "
        "In viā sunt multī virī. Multī virī in viā ambulant. "
        "Et in viā — nūllus est dominus. In viā — nūllus est servus. "
        "In viā — sunt virī. Via est via virōrum. "
        "Iūlius et Medus in viā longā sunt. "
        "Duo virī — et via est via duōrum."
    )
}

STORIES["cap4_12"] = {
    "title_la": "Puer et amīcus",
    "title_zh": "男孩与朋友",
    "target_chapter": 4,
    "theme": "18 自然",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in oppidō est. Puer est Daphnis. Daphnis in oppidō parvō habitat. "
        "Daphnis sōlus est. Daphnis patrem nōn habet. "
        "Daphnis mātrem nōn habet. Daphnis nūllam familiam habet. "
        "Daphnis in viā est. Daphnis virōs videt. Daphnis fēminās videt. "
        "Daphnis puerōs videt. Daphnis puellās videt. "
        "Puerī cum puerīs ambulant. Puellae cum puellīs ambulant. "
        "Virī cum fēminīs ambulant. Fēminae cum fīliīs ambulant. "
        "Daphnis nūllum amīcum habet. Daphnis sōlus est. "
        "Daphnis in viā plōrat. Daphnis: 'Cūr ego sōlus sum? "
        "Cūr nūllum amīcum habeō? Cūr nūlla familia mihi est?' "
        "Puer Daphnim videt. Puer est Mārcus. Mārcus ad Daphnim venit. "
        "Mārcus: 'Puer, cūr plōrās? Ego tē videō. Ego tē audiō.' "
        "Daphnis: 'Ego sōlus sum. Ego nūllum amīcum habeō. "
        "Ego nūllam familiam habeō. Ego in viā sōlus sum.' "
        "Mārcus: 'Tū nōn sōlus es. Ego tē videō. Ego tē audiō. "
        "Ego amīcus tuus sum. Venī cum mē. "
        "In vīllā meā multī puerī sunt. In vīllā meā multī amīcī sunt.' "
        "Daphnis: 'Tū es amīcus meus? Tū mē vidēs? Tū mē audīs?' "
        "Mārcus: 'Ego tē videō. Ego tē audiō. "
        "Tū es puer — et ego sum puer. Duo puerī amīcī sunt.' "
        "Daphnis cum Mārcō ambulat. Mārcus cum Daphni ad vīllam ambulat. "
        "Vīlla Mārcī est magna. Vīlla Mārcī est pulchra. "
        "In vīllā Mārcī multī puerī sunt. In vīllā Mārcī multae puellae sunt. "
        "Mārcus: 'Daphnī, haec est vīlla mea. Haec est vīlla patris meī. "
        "In vīllā meā multī puerī sunt. In vīllā meā multī amīcī sunt.' "
        "Daphnis puerōs videt. Daphnis puellās videt. "
        "Puerī Daphnim vident. Puerī: 'Quis es tū? Tū novus puer es.' "
        "Daphnis: 'Ego sum Daphnis. Ego in oppidō parvō sum. "
        "Ego nūllum amīcum habeō.' "
        "Puerī: 'Iam tū amīcum habēs. Mārcus est amīcus tuus. "
        "Et multī puerī hīc sunt amīcī. Et ego sum amīcus tuus quoque.' "
        "Daphnis nōn iam plōrat. Daphnis nōn iam sōlus est. "
        "Daphnis amīcum habet. Daphnis multōs amīcōs habet. "
        "Mārcus: 'Daphnī, tū in vīllā meā es. Tū nōn iam sōlus es. "
        "Tū amīcōs habēs. Tū familiam habēs — amīcī sunt familia.' "
        "Daphnis: 'Mārce, tū bonus es. Tū mē vidēs. Tū mē audīs. "
        "Tū es amīcus meus. Ego laetus sum. Ego nōn iam sōlus sum.' "
        "Mārcus et Daphnis in hortō ambulant. "
        "Hortus Mārcī est magnus. Hortus Mārcī est pulcher. "
        "In hortō multae rosae sunt. In hortō multa līlia sunt. "
        "Mārcus: 'Daphnī, hīc est hortus meus. In hortō meō multae rosae sunt. "
        "In hortō meō multa līlia sunt. Rosae sunt pulchrae. "
        "Līlia sunt pulchra. Hortus meus est pulcher.' "
        "Daphnis: 'Hortus tuus est pulcher. Rosae sunt pulchrae. "
        "Līlia sunt pulchra. Sed amīcus est magnum bonum. "
        "Rosae sunt pulchrae — sed amīcus est pulcher quoque.' "
        "Mārcus: 'Daphnī, tū es amīcus meus. Amīcus est magnum bonum. "
        "Ego tē videō. Ego tē audiō. Tū es bonus puer.' "
        "Daphnis in vīllā Mārcī est. Daphnis cum Mārcō est. "
        "Daphnis cum puerīs est. Daphnis nōn iam sōlus est. "
        "Daphnis laetus est. "
        "Daphnis: 'Mārce, tū mihi amīcum dās. Tū mihi vīllam tuam dās. "
        "Tū mihi hortum tuum dās. Hoc est magnum bonum. "
        "Ego tē videō. Ego tē audiō. Tū es bonus amīcus.' "
        "Mārcus: 'Daphnī, tū es bonus amīcus quoque. "
        "Amīcus amīcum videt. Amīcus amīcum audit. "
        "Amīcus amīcum amat.' "
        "Daphnis et Mārcus in hortō ambulant. "
        "Duo puerī in hortō sunt. Duo puerī laetī sunt. "
        "Duo puerī amīcī sunt. "
        "Daphnis in vīllā Mārcī habitat. Daphnis nōn iam sōlus est. "
        "Daphnis familiam habet — nōn patrem et mātrem, sed amīcōs. "
        "Amīcī sunt familia. Et familia est magnum bonum. "
        "Daphnis et Mārcus in oppidō ambulant. "
        "Duo puerī in viā sunt. Duo puerī laetī sunt. "
        "Daphnis: 'Mārce, via est longa — sed ego nōn sōlus sum. "
        "Tū cum mē ambulās. Ego cum tē ambulō. "
        "Duo amīcī in viā longā sunt.' "
        "Mārcus: 'Daphnī, amīcus est bonus. Amīcus est magnum bonum. "
        "Duo amīcī in viā sunt — et via est via amīcōrum.' "
        "Daphnis nōn iam plōrat. Daphnis nōn iam sōlus est. "
        "Daphnis amīcum habet. Daphnis laetus est. "
        "Ubi amīcus est — bonum est."
    )
}

STORIES["cap4_13"] = {
    "title_la": "Puer sōlus",
    "title_zh": "孤独的男孩",
    "target_chapter": 4,
    "theme": "13 孤独",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in oppidō est. Puer est Lūcius. Lūcius sōlus est. "
        "Lūcius patrem nōn habet. Lūcius mātrem nōn habet. Lūcius nūllam familiam habet. "
        "Lūcius in viā est. Lūcius virōs videt. Lūcius fēminās videt. "
        "Virī cum fīliīs ambulant. Fēminae cum fīliābus ambulant. "
        "Lūcius nūllum patrem videt. Lūcius nūllam mātrem videt. Lūcius sōlus est. "
        "Lūcius in viā plōrat. Nēmō Lūcium videt. Nēmō Lūcium audit. "
        "Lūcius est puer parvus — et parvus puer nōn vidētur. "
        "Sed fēmina Lūcium videt. Fēmina est Cornēlia. Cornēlia in oppidō est. "
        "Cornēlia Lūcium plōrantem videt. Cornēlia: 'Puer, cūr plōrās?' "
        "Lūcius: 'Ego sōlus sum. Ego nūllum patrem habeō. Ego nūllam mātrem habeō.' "
        "Cornēlia: 'Tū nōn sōlus es. Ego tē videō. Ego tē audiō. Venī mēcum.' "
        "Cornēlia Lūcium ad vīllam dūcit. Vīlla Cornēliae est magna. "
        "In vīllā Cornēliae multī servī sunt. In vīllā Cornēliae multī puerī sunt. "
        "Cornēlia: 'Lūcī, haec vīlla tua est. Hīc tū nōn sōlus es. "
        "Hīc multī puerī sunt. Hīc tū familiam habēs.' "
        "Lūcius puerōs videt. Puerī Lūcium vident. Puerī: 'Quis es tū?' "
        "Lūcius: 'Ego sum Lūcius. Ego nūllam familiam habeō.' "
        "Puerī: 'Tū nunc familiam habēs. Nōs sumus familia tua.' "
        "Lūcius nōn iam plōrat. Lūcius nōn iam sōlus est. "
        "Lūcius in vīllā Cornēliae est. Lūcius cum puerīs est. Lūcius familiam habet. "
        "Cornēlia Lūcium videt. Cornēlia: 'Lūcī, familia nōn est sanguis. "
        "Familia est quī tē vident. Familia est quī tē amant.' "
        "Lūcius: 'Cornēlia, tū es māter mea. Puerī sunt frātrēs meī. "
        "Ego nōn iam sōlus sum. Ego familiam habeō.' "
        "Lūcius in oppidō nōn iam sōlus est. Lūcius familiam habet. "
        "Nōn sanguine — sed amōre. Nōn nōmine — sed corde. "
        "Lūcius in vīllā Cornēliae labōrat. Lūcius in hortō labōrat. "
        "Lūcius aquam ad vīllam portat. Lūcius bonus puer est. "
        "Cornēlia Lūcium videt. Cornēlia: 'Lūcī, tū bonus puer es. Tū labōrās. Tū familiam amās.' "
        "Lūcius: 'Cornēlia, tū mihi vīllam dedistī. Tū mihi familiam dedistī. "
        "Ego tibi grātiās agō. Ego tē amō.' "
        "Cornēlia: 'Lūcī, tū nōn iam sōlus es. Tū nōn iam in viā es. "
        "Tū in vīllā es. Tū in familiā es. Tū es fīlius meus.' "
        "Lūcius nōn iam plōrat. Lūcius nōn iam sōlus est. "
        "Lūcius laetus est. Lūcius familiam habet — et familia est omnia."
    )
}

STORIES["cap4_14"] = {
    "title_la": "Puella et aqua",
    "title_zh": "女孩与水",
    "target_chapter": 4,
    "theme": "18 自然",
    "style": "抒情",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puella in oppidō est. Puella est Cornēlia. "
        "Cornēlia in oppidō parvō habitat. Cornēlia in vīllā magnā habitat. "
        "Cornēlia patrem habet. Cornēlia mātrem habet. "
        "Pater Cornēliae est Iūlius. Māter Cornēliae est Aemilia. "
        "Iūlius Cornēliam amat. Aemilia Cornēliam amat. "
        "Cornēlia patrem amat. Cornēlia mātrem amat. "
        "Cornēlia est puella bona. Cornēlia est puella laeta. "
        "Cornēlia ad aquam ambulat. Aqua est prope oppidum. "
        "Aqua est parva — sed aqua est pulchra. "
        "Aqua est via aquae. Cornēlia aquam amat. "
        "Cornēlia ad aquam venit. Cornēlia aquam videt. "
        "Cornēlia aquam videt. Aqua est pulchra. "
        "Aqua est nova. Aqua est bona. In aquā Cornēlia sē videt. "
        "Cornēlia: 'Ego in aquā sum. Aqua mē videt. "
        "Ego aquam videō. Ego et aqua — duo sumus.' "
        "Cornēlia prope aquam ambulat. "
        "Prope aquam multae rosae sunt. Prope aquam multa līlia sunt. "
        "Rosae sunt pulchrae. Līlia sunt pulchra. "
        "Cornēlia rosās videt. Cornēlia līlia videt. "
        "Cornēlia rosās amat. Cornēlia līlia amat. "
        "Cornēlia: 'Rosae sunt pulchrae. Līlia sunt pulchra. "
        "Aqua est pulchra. Hīc bonum est.' "
        "Cornēlia aquam audit. Aqua est parva — sed aqua cantat. "
        "Aqua cantat: 'Venī ad mē, puella. Ego tē videō. Ego tē audiō.' "
        "Cornēlia aquam audit. Cornēlia: 'Aqua cantat! Aqua mē vocat!' "
        "Cornēlia ad aquam venit. Cornēlia in aquā est. "
        "Aqua est parva — sed aqua est bona. "
        "Cornēlia aquam capit. Cornēlia aquam in manibus habet. "
        "Aqua est bona. Aqua est nova. "
        "Cornēlia: 'Aqua est bona. Aqua est pulchra. "
        "Aqua mē videt. Aqua mē audit. "
        "Ego aquam videō. Ego aquam audiō. "
        "Aqua est amīca mea.' "
        "Cornēlia prope aquam est. Cornēlia aquam videt. "
        "Cornēlia aquam audit. Cornēlia laeta est. "
        "Cornēlia rosās videt. Cornēlia līlia videt. "
        "Cornēlia: 'Rosae sunt pulchrae. Līlia sunt pulchra. "
        "Aqua est pulchra. Ego hīc laeta sum.' "
        "Aemilia ad aquam venit. Aemilia Cornēliam videt. "
        "Aemilia: 'Cornēlia, tū hīc es. Tū aquam vidēs. "
        "Tū rosās vidēs. Tū līlia vidēs. Tū laeta es.' "
        "Cornēlia: 'Māter, aqua est pulchra. Rosae sunt pulchrae. "
        "Līlia sunt pulchra. Ego aquam videō. Ego aquam audiō. "
        "Aqua est amīca mea. Aqua mē videt. Aqua mē audit.' "
        "Aemilia: 'Cornēlia, tū es puella bona. "
        "Tū aquam vidēs. Tū rosās vidēs. Tū līlia vidēs. "
        "Tū multa bona vidēs.' "
        "Cornēlia et Aemilia prope aquam sunt. "
        "Māter et fīlia aquam vident. "
        "Māter et fīlia rosās vident. "
        "Māter et fīlia līlia vident. "
        "Cornēlia: 'Māter, aqua est bona. Aqua est pulchra. "
        "Aqua est amīca. Aqua est via. Aqua est bonum.' "
        "Aemilia: 'Cornēlia, aqua est bona. "
        "Et tū es bona. Tū aquam vidēs — et aqua tē videt. "
        "Tū aquam audīs — et aqua tē audit.' "
        "Cornēlia: 'Māter, aqua cantat. Aqua mē vocat. "
        "Ego aquam audiō. Ego ad aquam veniō. "
        "Aqua est amīca mea. Aqua est bona amīca.' "
        "Aemilia: 'Cornēlia, tū es puella pulchra. "
        "Tū aquam amās. Aqua tē amat. "
        "Tū rosās amās. Rosae tē amant. "
        "Tū multa amās — et multa tē amant.' "
        "Cornēlia et Aemilia ad vīllam ambulant. "
        "Cornēlia aquam videt. Cornēlia: 'Valē, aqua! "
        "Ego ad tē veniō. Ego tē videō. Ego tē audiō.' "
        "Cornēlia in vīllā est. Cornēlia aquam nōn videt — "
        "sed Cornēlia aquam in corde habet. "
        "Aqua est in corde Cornēliae. "
        "Et Cornēlia laeta est. "
        "Cornēlia ad aquam venit. Cornēlia aquam videt. "
        "Cornēlia aquam audit. Cornēlia laeta est. "
        "Aqua est amīca. Aqua est bona. "
        "Et puella et aqua — duae amīcae sunt."
    )
}

# ============================================================
# 评估与输出
# ============================================================

def main():
    os.makedirs(REALITATES_DIR / "Cap4", exist_ok=True)
    results = []

    for key, story in STORIES.items():
        text = story["text"]
        name = story["title_la"]
        r = evaluate(text, name)
        wc = len(text.split())
        verdict = "PASS" if r["v2_level"] is not None and r["v2_level"] <= story["target_chapter"] + 2 else "FAIL"
        print(f"{key} {name}: wc={wc} v2_level={r['v2_level']} v2_rate={r['v2_rate']}% → {verdict}")
        if r["v2_oov"]:
            print(f"  OOV: {r['v2_oov'][:20]}")
        results.append((key, story, r, wc, verdict))

    # 生成 Markdown 文件
    for key, story, r, wc, verdict in results:
        filename = f"Cap4_{story['title_la'].replace(' ', '_')}_{'medius' if story['length_tier'] == '中篇' else 'longior'}_{key.split('_')[1]}.md"
        filepath = REALITATES_DIR / "Cap4" / filename
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
            f.write(yaml + "\n" + story["text"] + "\n")

    passed = sum(1 for _, _, _, _, v in results if v == "PASS")
    print(f"\n{passed}/{len(results)} passed")

    # 删除旧 brevis 文件
    if passed == len(results):
        print("All passed! Deleting old brevis files...")
        for f in (REALITATES_DIR / "Cap4").glob("*_brevis_*.md"):
            f.unlink()
            print(f"  Deleted: {f.name}")
    else:
        print("Some failed - old files preserved.")

if __name__ == "__main__":
    main()