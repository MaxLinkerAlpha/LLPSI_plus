#!/usr/bin/env python3
"""rewrite_cap10.py — 重写 Cap.10 的 33 篇短篇为扩展篇。
16 中篇 + 10 中长篇 + 7 长篇 (v2_level <= 12)
极简词汇策略：只用 Cap.1-10 确认安全的词汇，避免 simplemma 错误映射。
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
# 安全词汇策略：
# 只使用 simplemma 能正确还原到 Cap.1-12 的词汇。
# 大量重复核心词汇，每句5-8词。
# ============================================================

# ============================================================
# 中篇 (300-500 words) x16
# ============================================================

STORIES["cap10_01"] = {
    "title_la": "Imperium",
    "title_zh": "权力",
    "target_chapter": 10,
    "theme": "06 权力",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第二人称",
    "text": (
        "Tu es dominus. Tu magnam domum habes. Tu multos servos habes. "
        "Servi tui te timent. Pater tuus te timet. Mater tua te timet. "
        "Filius tuus te timet. Tu magnus es. Sed tu solus es. "
        "In mensa tua multus cibus est. In cubiculo tuo magnus lectus est. "
        "Sed tu dormire non potes. Cur dormire non potes? "
        "Quia tu solus es. Dominus solus est. "
        "Servi te non amant. Servi te timent. "
        "Pater tuus te non amat. Pater tuus te timet. "
        "Filius tuus te timet. Filius tuus non ridet. "
        "Filius tuus cum servo parvo in horto est. "
        "Servus cum filio tuo ridet. Servus cum filio tuo ludit. "
        "Filius tuus cum servo ridet. Sed tecum non ridet. "
        "Tu magnum imperium habes. Tu multas terras habes. "
        "Tu multa oppida habes. Sed filius tuus cum servo ridet. "
        "Et tu — tu solus in cubiculo iaces. "
        "Tu de imperio cogitas. Tu de terris cogitas. "
        "Sed tu de filio non cogitas. "
        "Filius tuus de te non cogitat. Filius tuus de servo cogitat. "
        "Servus cum filio tuo ludit. Tu numquam cum filio ludis. "
        "Tu solum de imperio cogitas. "
        "Quid est imperium? Imperium est res mala. "
        "Imperium te solum facit. "
        "Imperium est magnum. Sed cor tuum est parvum. "
        "Tu es dominus. Sed quis est dominus tuus? "
        "Imperium tuum est dominus tuus. "
        "Tu servus imperii tui es. "
        "Nocte, tu in cubiculo iaces. "
        "Tu oculos claudis. Sed quies non venit. "
        "Tu de filio cogitas. Tu de servo cogitas. "
        "Et tu, solus, in magno cubiculo, dormire non potes."
    ),
}

STORIES["cap10_02"] = {
    "title_la": "Insula et Mors",
    "title_zh": "岛与死亡",
    "target_chapter": 10,
    "theme": "01 生死",
    "style": "精炼",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Insula in mari est. Insula est parva. Insula est sola. "
        "Nulla alia insula prope est. Nullum oppidum in insula est. "
        "Nulla via in insula est. Arbor est in insula. Herba est in insula. "
        "In insula vir est. Vir solus est. Vir nomen non habet. "
        "Vir in insula habitat. Vir solus habitat. "
        "Vir in insula sedet. Vir mare videt. Mare est magnum. "
        "Mare est altum. Mare est sine fine. "
        "Vir nihil videt. Nulla insula. Nullum oppidum. "
        "Nullus fluvius. Mare solum est. Caelum solum est. "
        "Vir de vita cogitat. Vir de morte cogitat. "
        "Vir multos annos in insula est. Vir solus multos annos est. "
        "Nullus amicus venit. Nulla navis venit. "
        "Vir pisces capit. Vir aquam bibit. Vir in herba dormit. "
        "Sed vir fessus est. Vir fessus est vitae. "
        "Vir ad aquam it. Vir in aqua stat. Aqua est frigida. "
        "Vir mare spectat. Mare eum vocat. "
        "Mare: 'Veni ad me. Ego te accipiam.' "
        "Vir mare audit. Vir nihil dicit. "
        "Vir se in mare dat. Vir in aqua est. "
        "Aqua eum trahit. Vir non iam in insula est. "
        "Vir in mari est. Vir oculos claudit. "
        "Vir de insula cogitat. De arbore. De herba. De caelo. "
        "Vita viri fuit parva. Vita viri fuit sola. "
        "Sed vita viri fuit sua. "
        "Mare eum trahit. Vir non iam sentit. "
        "Vir non iam cogitat. Vir non iam est. "
        "Insula parva est. Insula vacua est. "
        "Nullus vir in insula est. "
        "Arbor sola est. Herba sola est. "
        "Mare magnum est. Insula parva est. "
        "Et mors — mors est sicut mare: magnum, altum, sine fine."
    ),
}

STORIES["cap10_03"] = {
    "title_la": "Quid Est Iustitia",
    "title_zh": "什么是正义",
    "target_chapter": 10,
    "theme": "04 正义",
    "style": "古典",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "Puer ad patrem venit. Puer: 'Pater, quid est iustitia?' "
        "Pater tacet. Pater ad fenestram it. "
        "Pater: 'Veni, fili. Quid vides?' "
        "Puer: 'Oppidum video. Romam video. Multos viros video.' "
        "Pater: 'Quid viri faciunt?' "
        "Puer: 'Non video. Viri parvi sunt. Longe sunt.' "
        "Pater: 'Iustitia quoque est parva. Non vides eam, sed est. "
        "Sicut viri in oppido. Longe sunt, sed ibi sunt.' "
        "Puer: 'Sed pater, ubi est iustitia? In foro est?' "
        "Pater: 'Iustitia non est in loco. Iustitia in corde est.' "
        "Puer: 'Quomodo eam video?' "
        "Pater: 'Non oculis vides. Corde vides. "
        "Si vir bonus malum punit, iustitia est. "
        "Si vir malus bonum laedit, iustitia non est.' "
        "Puer: 'Sed quomodo scimus quid est bonum?' "
        "Pater: 'Bonum est quod alios iuvat. "
        "Si panem habes et amico das, bonum est. "
        "Si panem amici capis, malum est.' "
        "Puer: 'Et si malus vir panem meum capit, quid facio?' "
        "Pater: 'Iustitia dicit: malum puniendum est. "
        "Omnes homines sub iustitia aequi sunt.' "
        "Puer: 'Etiam dominus et servus aequi sunt?' "
        "Pater tacet. Pater diu cogitat. "
        "Pater: 'Hoc est difficile, fili. "
        "Homines non sunt aequi in rebus. "
        "Sed in iustitia, omnes aequi esse debent.' "
        "Puer: 'Sed non sunt. Servus in horto laborat. "
        "Dominus in domo sedet.' "
        "Pater: 'Recte dicis, fili. "
        "Sed iustitia est id quod mundum meliorem facit. "
        "Iustitia est lux. Iustitia est via. "
        "Sine iustitia, oppidum non est oppidum. "
        "Sine iustitia, homines mali sunt.' "
        "Puer: 'Mali sunt? Quomodo?' "
        "Pater: 'Sine iustitia, nemo alium iuvat. "
        "Sine iustitia, omnes solum de se cogitant.' "
        "Puer ad fenestram it. Puer oppidum videt. "
        "Puer: 'Pater, ego iustitiam facere volo.' "
        "Pater filium tangit. "
        "Pater: 'Hoc est initium, fili. "
        "Qui iustitiam facere vult, iam iustitiam in corde habet.' "
        "Et puer ad fenestram stat — et cogitat."
    ),
}

STORIES["cap10_04"] = {
    "title_la": "Finis Viae",
    "title_zh": "路之尽头",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "史诗",
    "genre": "C 历史与人物",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir in via ambulat. Via est longa. Via est pulchra. "
        "Vir a Graecia ad Romam it. Vir multos dies ambulat. "
        "Vir multas terras videt. Vir multa oppida videt. "
        "In Graecia, vir iuvenis fuit. "
        "In Graecia, vir familiam habuit. "
        "Sed vir Romam videre voluit. "
        "Vir de Roma multa audivit. "
        "Roma est caput mundi. Roma est maxima. "
        "Vir per multas terras ambulat. "
        "Vir per montes ambulat. Vir per silvas ambulat. "
        "Vir multos homines videt. "
        "Alii eum iuvant. Alii eum non vident. "
        "Vir in via fessus est. Vir in via solus est. "
        "Sed vir non cessat. Vir ambulat. Vir semper ambulat. "
        "Tandem, vir in Italia est. Italia est terra pulchra. "
        "In Italia, viae sunt bonae. In Italia, oppida sunt pulchra. "
        "Roma prope est. Vir Romam videre potest. "
        "Vir: 'Roma! Roma est prope! Ego Romam video!' "
        "Vir ad Romam currit. Vir laetus est. "
        "Sed vir fessus est. Vir multos dies non dormivit. "
        "Vir in via cadit. Vir in terra iacet. "
        "Vir Romam videre non potest. Oculi eius clauduntur. "
        "Vir de Graecia cogitat. De matre. De patre. De amicis. "
        "Vir de vita sua cogitat. Vita fuit longa. Vita fuit bona. "
        "Vir oculos aperit. Roma procul est. "
        "Vir surgere vult. Vir ambulare vult. "
        "Sed corpus non vult. Corpus fessum est. "
        "Vir: 'Roma, ego te videre volui. "
        "Sed via mea hic finitur.' "
        "Vir oculos claudit. Vir non iam sentit. "
        "Via viri finita est. Sed Roma manet. "
        "Alii viri ad Romam veniunt. "
        "Aliae viae incipiunt. Aliae viae finiuntur. "
        "Una via finitur — alia via incipit. "
        "Et vir, in terra, requiem invenit."
    ),
}

STORIES["cap10_05"] = {
    "title_la": "Somnum Aeternum",
    "title_zh": "永恒之眠",
    "target_chapter": 10,
    "theme": "23 睡眠",
    "style": "抒情",
    "genre": "G 哲理寓言",
    "character_type": "拟人概念",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quies in terra ambulat. Quies est bona. Quies est amica. "
        "Quies non est mala. Quies homines iuvat. "
        "Quies ad primum hominem it. "
        "Primus homo in lecto iacet. "
        "Homo dormire non potest. "
        "Quies ad eum venit. Quies manum in oculos eius ponit. "
        "Homo oculos claudit. Homo dormit. "
        "Quies ad alterum hominem it. "
        "Alter homo in via ambulat. Homo fessus est. "
        "Homo in via cadit. Quies ad eum venit. "
        "Quies eum in terra ponit. Homo in terra dormit. "
        "Caelum est tectum eius. "
        "Quies ad tertium hominem it. "
        "Tertius homo est puer. Puer in horto ludit. "
        "Puer fessus est. Quies ad eum venit. "
        "Puer sub arbore dormit. "
        "Mater puerum invenit. Mater puerum in domum portat. "
        "Quies ad quartum hominem it. "
        "Quartus homo est senex. Senex multos annos habet. "
        "Senex fessus est vitae. Quies ad eum venit. "
        "Senex: 'Quies, tu es amica mea. Tu me in requiem ducis.' "
        "Quies manum in oculos senis ponit. Senex dormit. "
        "Senex non iam surgit. Quies senem tenet. "
        "Quies ad alios homines it. "
        "Quies omnes homines quaerit. "
        "Quies ad divites it. Quies ad pauperes it. "
        "Quies ad bonos it. Quies ad malos it. "
        "Quies non eligit. Quies omnes aequos facit. "
        "Quies et mors similes sunt. "
        "Sed quies est bona. Mors est dura. "
        "Quies homines ad mortem ducit. "
        "Quies: 'Noli timere. Ego te tenebo. Ego te in requiem ducam.' "
        "Et homo quietem accipit. "
        "Quies in terra ambulat. Quies semper ambulat. "
        "Omnes homines quietem inveniunt."
    ),
}

STORIES["cap10_06"] = {
    "title_la": "Quattuor terrae",
    "title_zh": "四方之地",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quattuor terrae in Europa sunt. "
        "Italia est in medio. Graecia est ad orientem. "
        "Hispania est ad occidentem. Germania est ad septentrionem. "
        "Romani in Italia sunt. Roma est in Italia. "
        "Italia est patria Romanorum. Italia est terra bona. "
        "In Italia, multi montes sunt. In Italia, multa oppida sunt. "
        "Italia est pulchra. Italia est caput imperii. "
        "Romani in Graeciam venerunt. Graecia est terra antiqua. "
        "Graeci multa sciunt. Graeci multa scripserunt. "
        "Romani a Graecis multa didicerunt. "
        "Graecia est terra bona. Graecia est terra docta. "
        "Romani in Hispaniam venerunt. Hispania est terra magna. "
        "In Hispania, multi montes sunt. "
        "In Hispania, multa flumina sunt. "
        "Hispania est terra pulchra. Viri Hispaniae sunt fortes. "
        "Hispania est terra bona. "
        "Germania est ad septentrionem. Germania est terra fera. "
        "Romani in Germaniam non venerunt. "
        "Germania non est Romana. "
        "Rhenus est inter Germaniam et imperium. "
        "Rhenus est limes. Germani sunt fortes. "
        "Germania est terra libera. Germania est terra magna. "
        "Quattuor terrae — quattuor res. "
        "Italia est patria. Graecia est magistra. "
        "Hispania est pulchra. Germania est libera. "
        "Imperium Romanum est magnum. "
        "Sed non omnes terrae sunt Romanae. "
        "Et hoc est bonum. Mundus est magnus. "
        "Et in mundo, multae terrae sunt."
    ),
}

STORIES["cap10_07"] = {
    "title_la": "Mare et terra",
    "title_zh": "海与陆",
    "target_chapter": 10,
    "theme": "11 自然与文明",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mare est magnum. Terra est magna. "
        "Mare tangit terram. Terra finit mare. "
        "Ubi mare est, non est terra. "
        "Ubi terra est, non est mare. "
        "Mare et terra semper una sunt. "
        "Romani in terra sunt. Romani terram amant. "
        "Romani vias in terra faciunt. "
        "Romani oppida in terra aedificant. "
        "Sed Romani mare quoque amant. "
        "Naves Romanae per mare eunt. "
        "Naves multas res portant. "
        "Mare est via. Mare terras coniungit. "
        "Per mare, Romani ad Graeciam eunt. "
        "Per mare, Romani ad Hispaniam eunt. "
        "Per mare, Romani ad Africam eunt. "
        "Mare Nostrum est magnum. Mare Nostrum est Romanum. "
        "Mare Nostrum multas terras tangit. "
        "In mari, multae insulae sunt. "
        "Sicilia est insula magna. "
        "Sardinia est insula. Corsica est insula. "
        "Creta est insula. Rhodos est insula. "
        "Multae insulae in mari sunt. "
        "Multae insulae Romanae sunt. "
        "Terra est domus. Mare est via. "
        "Terra dat cibum. Mare dat viam. "
        "Sine terra, homines non vivunt. "
        "Sine mari, homines non eunt. "
        "Mare et terra — duo res. "
        "Mare et terra — una vita. "
        "Romani in terra ambulant. "
        "Romani in mari navigant. "
        "Romani terram et mare amant."
    ),
}

STORIES["cap10_08"] = {
    "title_la": "Flumina Romana",
    "title_zh": "罗马诸河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tiberis est in Italia. Tiberis est fluvius Romanus. "
        "Tiberis per Romam fluit. Roma ad Tiberim est. "
        "Tiberis aquam Romae dat. Tiberis naves portat. "
        "Tiberis est pater Romae. "
        "Sine Tiberi, Roma non est. "
        "Rhenus est in Germania. Rhenus est fluvius magnus. "
        "Rhenus est limes imperii. "
        "Rhenus Germaniam ab imperio dividit. "
        "Romani ad Rhenum stant. Romani Rhenum custodiunt. "
        "Trans Rhenum, Germania est. "
        "Trans Rhenum, Germani sunt. "
        "Rhenus est porta. Rhenus est murus. "
        "Danuvius est in imperio. Danuvius est fluvius longus. "
        "Danuvius per multas terras fluit. "
        "Danuvius multas gentes tangit. "
        "Danuvius est limes. Danuvius imperium defendit. "
        "Nilus est in Aegypto. Nilus est fluvius magnus. "
        "Nilus Aegypto aquam dat. "
        "Sine Nilo, Aegyptus non est. "
        "Nilus omni anno crescit. "
        "Nilus terram bonam facit. "
        "Nilus est pater Aegypti. "
        "Quattuor flumina — quattuor vitae. "
        "Tiberis est pater Romae. "
        "Rhenus est custos. "
        "Danuvius est limes. "
        "Nilus est vita. "
        "Flumina sunt magnae viae aquae. "
        "Flumina terras dividunt. "
        "Flumina terras coniungunt. "
        "Flumina semper fluunt. "
        "Ab montibus ad mare — flumina currunt. "
        "Et Romani flumina amant."
    ),
}

STORIES["cap10_09"] = {
    "title_la": "Duodecim insulae",
    "title_zh": "十二座岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duodecim insulae in mari sunt. "
        "Omnes insulae sunt pulchrae. Omnes insulae sunt notae. "
        "Sicilia est insula magna. Sicilia est prope Italiam. "
        "In Sicilia, multi montes sunt. "
        "In Sicilia, multae arbores sunt. "
        "Sicilia est terra bona. "
        "Sardinia est insula. Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "Corsica est insula parva. Corsica est prope Sardiniam. "
        "Corsica est pulchra. In Corsica, multi montes sunt. "
        "Creta est insula antiqua. Creta est magna. "
        "Creta est in Graecia. In Creta, multi dei fuerunt. "
        "Creta est insula nota. "
        "Rhodos est insula. Rhodos est in Graecia. "
        "Rhodos est pulchra. In Rhodo, multi flores sunt. "
        "Lesbos est insula. Lesbos est in Graecia. "
        "Lesbos est pulchra. "
        "Euboea est insula. Euboea est prope Graeciam. "
        "Euboea est longa. "
        "Chios est insula. Samos est insula. "
        "Lemnos est insula. Naxus est insula. "
        "Melita est insula. "
        "Omnes duodecim insulae sunt in imperio. "
        "Omnes sunt Romanae. Omnes sunt notae. "
        "Nautae ad has insulas navigant. "
        "Mercatores ad has insulas eunt. "
        "Duodecim insulae — duodecim portae ad mare. "
        "Et omnes sunt pulchrae. Et omnes sunt bonae."
    ),
}

STORIES["cap10_10"] = {
    "title_la": "Quattuor maria",
    "title_zh": "四海",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quattuor maria sunt. "
        "Mare Nostrum est primum. Oceanus est secundus. "
        "Tiberis est tertius. Nilus est quartus. "
        "Mare Nostrum est magnum. Mare Nostrum est Romanum. "
        "Mare Nostrum Italiam tangit. "
        "Mare Nostrum Graeciam tangit. "
        "Mare Nostrum Hispaniam tangit. "
        "Mare Nostrum Africam tangit. "
        "Mare Nostrum est in medio imperii. "
        "Romani Mare Nostrum amant. "
        "Romani in Mari Nostro navigant. "
        "Naves Romanae per Mare Nostrum eunt. "
        "Mare Nostrum multas terras coniungit. "
        "Oceanus est maximus. Oceanus est extra imperium. "
        "Oceanus Britanniam tangit. "
        "Oceanus est sine fine. Oceanus est altus. "
        "Romani Oceanum timent. Oceanus non est bonus. "
        "Tiberis est fluvius Romanus. "
        "Tiberis Romam tangit. "
        "Tiberis est parvus — sed est magnus Romae. "
        "Tiberis aquam dat. Tiberis naves portat. "
        "Tiberis est cor Romae. "
        "Nilus est in Aegypto. Nilus est fluvius magnus. "
        "Nilus Aegyptum tangit. Nilus Aegypto aquam dat. "
        "Sine Nilo, Aegyptus est nihil. "
        "Nilus omni anno crescit. "
        "Nilus terras bonas facit. "
        "Quattuor maria — quattuor aquae. "
        "Mare Nostrum est imperium. "
        "Oceanus est finis. "
        "Tiberis est patria. "
        "Nilus est vita. "
        "Et omnes aquae sunt bonae."
    ),
}

STORIES["cap10_11"] = {
    "title_la": "Britannia et Hibernia",
    "title_zh": "不列颠与爱尔兰",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Britannia et Hibernia sunt duae insulae. "
        "Sunt in septentrione. Sunt in Oceano. "
        "Britannia est magna. Britannia est insula magna. "
        "Britannia est prope Galliam. "
        "Britannia est in imperio. "
        "Romani in Britanniam venerunt. "
        "Romani Britanniam vicerunt. "
        "In Britannia, multi montes sunt. "
        "In Britannia, multae silvae sunt. "
        "Britanni sunt fortes. Britanni sunt feri. "
        "Sed nunc Britanni sunt Romani. "
        "Britannia est terra Romana. "
        "Hibernia est parva. Hibernia est insula parva. "
        "Hibernia est prope Britanniam. "
        "Hibernia non est in imperio. "
        "Romani in Hiberniam non venerunt. "
        "Hibernia est libera. "
        "Hiberni sunt fortes. "
        "Hibernia est terra viridis. "
        "In Hibernia, multae herbae sunt. "
        "In Hibernia, multa aqua est. "
        "Duae insulae — duae res. "
        "Britannia est Romana. Hibernia est libera. "
        "Britannia est magna. Hibernia est parva. "
        "Sed ambae sunt pulchrae. "
        "Mare inter Britanniam et Hiberniam est. "
        "Mare est parvum. Mare est ferum. "
        "Naves inter duas insulas navigant. "
        "Mercatores inter duas insulas eunt. "
        "Britannia et Hibernia — sorores in mari. "
        "Una est capta. Una est libera. "
        "Sed ambae in Oceano sunt. "
        "Et ambae sunt pulchrae."
    ),
}

STORIES["cap10_12"] = {
    "title_la": "In foro",
    "title_zh": "在市集",
    "target_chapter": 10,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "In foro multi homines sunt. "
        "Forum est magnum. Forum est pulchrum. "
        "In foro, multae tabernae sunt. "
        "In tabernis, multae res sunt. "
        "Mercatores in foro sunt. Mercatores res vendunt. "
        "Alius mercator panem vendit. "
        "Panis est bonus. Panis est novus. "
        "Alius mercator vinum vendit. "
        "Alius mercator vestes vendit. "
        "Vestes sunt pulchrae. "
        "Alius mercator libros vendit. "
        "Libri sunt antiqui. "
        "Vir ad forum venit. Vir panem emit. "
        "Vir pecuniam numerat. Vir mercatori pecuniam dat. "
        "Femina ad forum venit. Femina vestes emit. "
        "Femina vestem pulchram videt. "
        "Femina vestem tangit. "
        "Femina: 'Haec vestis est pulchra. "
        "Quanti haec vestis est?' "
        "Mercator: 'Haec vestis decem nummos constat.' "
        "Femina pecuniam dat. Femina vestem accipit. "
        "Puer ad forum venit. Puer libros videt. "
        "Puer: 'Quanti hic liber est?' "
        "Mercator: 'Hic liber quinque nummos constat.' "
        "Puer pecuniam non habet. Puer est tristis. "
        "Senex puerum videt. "
        "Senex: 'Cur tristis es, puer?' "
        "Puer: 'Librum videre volo. Sed pecuniam non habeo.' "
        "Senex: 'Ego tibi librum dabo.' "
        "Senex librum emit. Senex puero librum dat. "
        "Puer: 'Gratias tibi ago!' "
        "Puer laetus est. Puer librum legit. "
        "In foro, multi clamores sunt. "
        "Mercatores clamant. Homines loquuntur. "
        "Servi currunt. Canes in foro sunt. "
        "Forum est cor oppidi. "
        "In foro, vita est."
    ),
}

STORIES["cap10_13"] = {
    "title_la": "In via",
    "title_zh": "在街上",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "In via homo ambulat. Via est longa. "
        "Homo solus est. Homo de vita cogitat. "
        "Canis cum homine ambulat. "
        "Canis est parvus. Canis est niger. "
        "Homo canem amat. Canis hominem amat. "
        "Homo: 'Canis, veni! Curre mecum!' "
        "Canis currit. Canis caudam movet. "
        "Canis laetus est. "
        "Homo et canis per viam ambulant. "
        "Alii homines in via sunt. "
        "Alius homo equum habet. "
        "Equus est magnus. Equus est albus. "
        "Homo: 'Salve, amice! Quo vadis?' "
        "Alius: 'Ad forum eo. Res emere volo.' "
        "Homo: 'Et ego ad forum eo. Ambulemus una!' "
        "Duo homines et canis ad forum eunt. "
        "In via, pueri ludunt. "
        "Pueri pilam habent. Pueri pilam iaciunt. "
        "Pueri rident. "
        "Canis ad pueros currit. "
        "Canis cum pueris ludit. "
        "Pueri canem tangunt. "
        "Homo: 'Canis, veni! Ad me veni!' "
        "Canis ad hominem redit. "
        "Femina in via est. Femina aquam portat. "
        "Homo feminam iuvat. Homo aquam portat. "
        "Femina: 'Gratias tibi ago. Tu es bonus vir.' "
        "Homo: 'Nihil est. Omnes se iuvare debent.' "
        "Homo et canis ad forum veniunt. "
        "Forum est magnum. "
        "Homo: 'Canis, hic est forum. "
        "Hic, multae res sunt.' "
        "Canis latrat. Canis caudam movet. "
        "Homo et canis in foro sunt. "
        "Et ambo sunt laeti."
    ),
}

STORIES["cap10_14"] = {
    "title_la": "Insula parva",
    "title_zh": "小岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Insula est parva. Insula in mari est. "
        "Insula sola est. "
        "In insula, unus homo habitat. "
        "Homo est piscator. Homo solus est. "
        "Nulla femina in insula est. "
        "Nulli amici sunt. "
        "Homo pisces capit. Homo aquam bibit. "
        "Homo in casa parva habitat. "
        "Casa est parva. Casa ex ligno est. "
        "In casa, unus lectus est. "
        "In casa, una mensa est. "
        "Homo in casa dormit. "
        "Homo in casa comedit. "
        "Homo omni die surgit. "
        "Homo omni die ad mare it. "
        "Homo in mari pisces quaerit. "
        "Mare est magnum. Mare est bonum. "
        "Mare homini pisces dat. "
        "Mare homini vitam dat. "
        "Homo: 'Mare, tu es amicus meus. "
        "Tu mihi omnia das.' "
        "Homo in mari natat. "
        "Aqua est frigida. Aqua est bona. "
        "Homo in aqua laetus est. "
        "Aliquando, navis ad insulam venit. "
        "Nautae in insula sunt. "
        "Nautae hominem vident. "
        "Nauta: 'Cur hic solus habitas? "
        "Cur non in oppidum venis?' "
        "Homo: 'Oppidum est magnum. "
        "In oppido, multi homines sunt. "
        "Sed hic, ego sum meus.' "
        "Nauta: 'Sed in oppido, multae res sunt.' "
        "Homo: 'Hic quoque vita est bona. "
        "Hic, mare mihi loquitur. "
        "Hic, ventus mihi cantat. "
        "Hic, sol mihi lucet.' "
        "Nautae abeunt. Navis in mari abit. "
        "Homo solus in insula manet. "
        "Homo laetus est. "
        "Insula est parva. Sed insula est domus. "
        "Et homo in insula sua laetus habitat."
    ),
}

STORIES["cap10_15"] = {
    "title_la": "Puer et avis",
    "title_zh": "男孩与鸟",
    "target_chapter": 10,
    "theme": "03 自由与束缚",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in horto est. Puer avem in manu tenet. "
        "Avis est parva. Avis est alba. Avis est pulchra. "
        "Puer avem in terra invenit. "
        "Avis volare non poterat. "
        "Puer avem in domum portavit. "
        "Puer avi aquam dedit. "
        "Puer avi cibum dedit. Puer avem curavit. "
        "Nunc avis est sana. Nunc avis potest volare. "
        "Puer avem in manu tenet. "
        "Puer avem spectat. "
        "Puer: 'Avis, tu es pulchra. "
        "Tu es amica mea. Ego te amo.' "
        "Avis puerum spectat. "
        "Puer avem in manu tenet. "
        "Puer cum avi in horto ambulat. "
        "Puer: 'Avis, hic est hortus meus. "
        "Hic sunt rosae. Hic sunt arbores. "
        "Hic est domus mea.' "
        "Avis ad caelum spectat. Avis alas movet. "
        "Puer: 'Avis, tu volare vis? "
        "Sed ego te tenere volo.' "
        "Puer avem tenet. Puer avem non mittit. "
        "Pater pueri ad hortum venit. "
        "Pater: 'Fili, cur avem tenes? "
        "Avis non est tua. Avis est libera.' "
        "Puer: 'Sed pater, ego avem amo. "
        "Ego avem dare non volo.' "
        "Pater: 'Fili, amor non est tenere. "
        "Si avem vere amas, eam liberam facies.' "
        "Puer cogitat. Puer avem spectat. "
        "Puer: 'Avis, ego te amo. "
        "Et quia te amo, ego te mitto.' "
        "Puer manum aperit. Avis in caelum volat. "
        "Avis est libera. Avis in caelo est. "
        "Puer avem spectat. "
        "Puer est tristis — sed etiam laetus. "
        "Puer: 'Vola, avis! Vola ad caelum!' "
        "Avis in caelo est. Avis non redit. "
        "Sed puer scit: avis est libera. "
        "Et hoc est bonum."
    ),
}

STORIES["cap10_16"] = {
    "title_la": "Canis et puer",
    "title_zh": "狗与男孩",
    "target_chapter": 10,
    "theme": "32 友谊与孤独",
    "style": "白话",
    "genre": "A 童话",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer canem habet. Canis est parvus. "
        "Canis est niger. Canis est amicus pueri. "
        "Puer canem amat. Canis puerum amat. "
        "Puer et canis in via ambulant. "
        "Puer: 'Canis, veni! Curre mecum!' "
        "Canis currit. Canis caudam movet. "
        "Canis laetus est. "
        "Puer: 'Canis, sede!' Canis sedet. "
        "Puer: 'Canis, sta!' Canis stat. "
        "Puer: 'Bonus canis es! Tu es optimus canis!' "
        "Canis latrat. Canis salit. "
        "Puer ridet. Puer canem tangit. "
        "Puer et canis in horto ludunt. "
        "Puer pilam iacit. Canis ad pilam currit. "
        "Canis pilam capit. Canis ad puerum redit. "
        "Canis pilam dat. "
        "Puer: 'Bonus canis! Tu es celer! Tu es fortis!' "
        "Puer et canis in herba sedent. "
        "Sol est calidus. "
        "Puer: 'Canis, tu es amicus meus. "
        "Alii pueri me non amant. Sed tu me amas.' "
        "Canis puerum spectat. Canis caudam movet. "
        "Puer: 'Canis, ego te semper amabo. "
        "Tu es canis meus. Et ego sum puer tuus.' "
        "Nocte, puer in lecto est. "
        "Canis prope lectum est. "
        "Puer: 'Canis, dormi mecum.' "
        "Canis in lectum salit. "
        "Canis prope puerum dormit. "
        "Puer canem tangit. "
        "Canis est calidus. Canis est bonus. "
        "Puer: 'Canis, tu es optimus. "
        "Cum te, ego non sum solus.' "
        "Puer oculos claudit. Puer dormit. "
        "Canis quoque dormit. "
        "Et ambo sunt laeti. Et ambo sunt una."
    ),
}

# ============================================================
# 中长篇 (500-800 words) x10
# ============================================================

STORIES["cap10_17"] = {
    "title_la": "Duodecim insulae maris",
    "title_zh": "海中十二岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum nauta. Ego in mari navigo. "
        "Ego multas insulas vidi. Ego duodecim insulas novi. "
        "Prima insula est Sicilia. Sicilia est magna. "
        "Sicilia est prope Italiam. "
        "In Sicilia, mons magnus est. "
        "Mons ignem habet. Mons fumum dat. "
        "Sicilia est terra bona. "
        "Secunda insula est Sardinia. "
        "Sardinia est in mari. Sardinia est prope Corsicam. "
        "In Sardinia, multi pastores sunt. "
        "Pastores oves habent. "
        "Tertia insula est Corsica. "
        "Corsica est parva. Corsica est pulchra. "
        "In Corsica, multi montes sunt. "
        "In Corsica, multae silvae sunt. "
        "Quarta insula est Creta. "
        "Creta est antiqua. Creta est magna. "
        "Creta est in Graecia. "
        "In Creta, viri antiqui habitaverunt. "
        "Creta est insula nota. "
        "Quinta insula est Rhodos. "
        "Rhodos est in Graecia. Rhodos est pulchra. "
        "In Rhodo, multi flores sunt. "
        "In Rhodo, sol semper lucet. "
        "Sexta insula est Lesbos. "
        "Lesbos est in Graecia. "
        "Lesbos est terra poetarum. "
        "In Lesbo, multi libri scripti sunt. "
        "Septima insula est Euboea. "
        "Euboea est prope Graeciam. "
        "Euboea est longa. Euboea est ferax. "
        "Octava insula est Chios. "
        "Chios est parva. Chios est in Graecia. "
        "Nona insula est Samos. "
        "Samos est parva. Samos est in Graecia. "
        "Decima insula est Lemnos. "
        "Lemnos est parva. Lemnos est in Graecia. "
        "Undecima insula est Naxus. "
        "Naxus est parva. Naxus est in mari. "
        "Duodecima insula est Melita. "
        "Melita est minima. Melita est in mari. "
        "Omnes duodecim insulae sunt in imperio. "
        "Omnes sunt pulchrae. Omnes sunt notae. "
        "Ego ad has insulas navigo. "
        "Ego has insulas amo. "
        "Mare inter insulas est magnum. "
        "Mare inter insulas est pulchrum. "
        "Duodecim insulae — duodecim sorores. "
        "Et ego, nauta, eas semper in corde habeo."
    ),
}

STORIES["cap10_18"] = {
    "title_la": "Tria flumina",
    "title_zh": "三条河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum vir Romanus. Ego tria flumina vidi. "
        "Ego de tribus fluminibus dicam. "
        "Primum flumen est Rhenus. "
        "Rhenus est in Germania. "
        "Rhenus est flumen magnum. "
        "Rhenus est limes imperii. "
        "Rhenus Germaniam ab imperio dividit. "
        "Ego ad Rhenum veni. "
        "Ego Rhenum vidi. Rhenus est magnus. "
        "Rhenus est altus. Rhenus est ferus. "
        "Romani ad Rhenum stant. "
        "Romani Rhenum custodiunt. "
        "Trans Rhenum, Germania est. "
        "Trans Rhenum, Germani sunt. "
        "Germani sunt fortes. Germani sunt feri. "
        "Rhenus est porta imperii. "
        "Rhenus est murus imperii. "
        "Secundum flumen est Danuvius. "
        "Danuvius est in imperio. "
        "Danuvius est flumen longum. "
        "Danuvius per multas terras fluit. "
        "Danuvius multas gentes tangit. "
        "Ego ad Danuvium veni. "
        "Ego Danuvium vidi. "
        "Danuvius est limes. "
        "Danuvius imperium defendit. "
        "Ad Danuvium, multae gentes sunt. "
        "Ad Danuvium, multi milites sunt. "
        "Danuvius est magnus. Danuvius est fortis. "
        "Tertium flumen est Tiberis. "
        "Tiberis est in Italia. "
        "Tiberis est flumen Romanum. "
        "Tiberis per Romam fluit. "
        "Roma ad Tiberim est. "
        "Tiberis aquam Romae dat. "
        "Tiberis naves portat. "
        "Tiberis est pater Romae. "
        "Ego ad Tiberim veni. "
        "Ego Tiberim vidi. "
        "Tiberis non est maximus. "
        "Sed Tiberis est carus Romanis. "
        "Tiberis est cor Romae. "
        "Tria flumina — tres res. "
        "Rhenus est custos. "
        "Danuvius est limes. "
        "Tiberis est pater. "
        "Et omnia flumina sunt bona. "
        "Et omnia flumina sunt Romana."
    ),
}

STORIES["cap10_19"] = {
    "title_la": "Quinque flumina",
    "title_zh": "五条河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quinque flumina in imperio sunt. "
        "Omnia flumina sunt magna. Omnia flumina sunt nota. "
        "Tiberis est primum flumen. "
        "Tiberis est in Italia. Tiberis est Romanus. "
        "Tiberis per Romam fluit. "
        "Roma ad Tiberim est. "
        "Tiberis aquam Romae dat. "
        "Tiberis est pater Romae. "
        "Sine Tiberi, Roma non est. "
        "Rhenus est secundum flumen. "
        "Rhenus est in Germania. "
        "Rhenus est flumen magnum. "
        "Rhenus est limes imperii. "
        "Rhenus Germaniam ab imperio dividit. "
        "Romani ad Rhenum stant. "
        "Romani Rhenum custodiunt. "
        "Trans Rhenum, Germani sunt. "
        "Rhenus est porta. Rhenus est murus. "
        "Danuvius est tertium flumen. "
        "Danuvius est in imperio. "
        "Danuvius est flumen longum. "
        "Danuvius per multas terras fluit. "
        "Danuvius multas gentes tangit. "
        "Danuvius est limes. "
        "Danuvius imperium defendit. "
        "Nilus est quartum flumen. "
        "Nilus est in Aegypto. "
        "Nilus est flumen magnum. "
        "Nilus Aegypto aquam dat. "
        "Sine Nilo, Aegyptus non est. "
        "Nilus omni anno crescit. "
        "Nilus terram bonam facit. "
        "Nilus est pater Aegypti. "
        "Rhodanus est quintum flumen. "
        "Rhodanus est in Gallia. "
        "Rhodanus est flumen magnum. "
        "Rhodanus per Galliam fluit. "
        "Rhodanus ad mare it. "
        "Gallia est terra Romana. "
        "Rhodanus est flumen Romanum. "
        "Quinque flumina — quinque vitae. "
        "Tiberis est pater Romae. "
        "Rhenus est custos. "
        "Danuvius est limes. "
        "Nilus est vita Aegypti. "
        "Rhodanus est via Galliae. "
        "Flumina sunt magnae viae. "
        "Flumina terras dividunt. "
        "Flumina terras coniungunt. "
        "Flumina semper fluunt. "
        "Et Romani flumina amant."
    ),
}

STORIES["cap10_20"] = {
    "title_la": "Novem insulae",
    "title_zh": "九座岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum mercator. Ego per mare navigo. "
        "Ego multas insulas vidi. "
        "Ego novem insulas bene novi. "
        "Prima insula est Sicilia. "
        "Sicilia est maxima insula. "
        "Sicilia est prope Italiam. "
        "In Sicilia, multi montes sunt. "
        "In Sicilia, multae arbores sunt. "
        "Sicilia multum frumentum dat. "
        "Ego ad Siciliam saepe eo. "
        "In Sicilia, mercatores multi sunt. "
        "Secunda insula est Sardinia. "
        "Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "In Sardinia, multi pastores sunt. "
        "Pastores oves habent. "
        "Sardinia est terra bona. "
        "Tertia insula est Corsica. "
        "Corsica est parva. Corsica est pulchra. "
        "In Corsica, multi montes sunt. "
        "In Corsica, multae silvae sunt. "
        "Corsica est terra fera. "
        "Quarta insula est Creta. "
        "Creta est antiqua. Creta est magna. "
        "Creta est in Graecia. "
        "In Creta, dei antiqui fuerunt. "
        "Creta est insula sacra. "
        "Quinta insula est Rhodos. "
        "Rhodos est in Graecia. "
        "Rhodos est pulchra. "
        "In Rhodo, multi flores sunt. "
        "In Rhodo, sol semper lucet. "
        "Sexta insula est Lesbos. "
        "Lesbos est in Graecia. "
        "Lesbos est terra poetarum. "
        "In Lesbo, multi libri scripti sunt. "
        "Septima insula est Euboea. "
        "Euboea est prope Graeciam. "
        "Euboea est longa. Euboea est ferax. "
        "Octava insula est Chios. "
        "Chios est parva. Chios est in Graecia. "
        "Nona insula est Samos. "
        "Samos est parva. Samos est in Graecia. "
        "Samos est pulchra. "
        "Novem insulae — novem portae. "
        "Omnes sunt in imperio. "
        "Omnes sunt Romanae. "
        "Ego ad has insulas navigo. "
        "Ego res in his insulis emo et vendo. "
        "Mare inter insulas est magnum. "
        "Mare inter insulas est pulchrum. "
        "Et ego, mercator, has insulas amo."
    ),
}

STORIES["cap10_21"] = {
    "title_la": "Septem insulae parvae",
    "title_zh": "七座小岛",
    "target_chapter": 10,
    "theme": "13 孤独",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum viator. Ego per mare navigo. "
        "Ego septem insulas parvas vidi. "
        "Prima insula est Lemnos. "
        "Lemnos est parva. Lemnos est in mari. "
        "In Lemno, unus mons est. "
        "In Lemno, pauca arbores sunt. "
        "Lemnos est sola. Lemnos est pulchra. "
        "Secunda insula est Naxus. "
        "Naxus est parva. Naxus est in mari. "
        "In Naxo, multi flores sunt. "
        "In Naxo, multae herbae sunt. "
        "Naxus est pulchra. Naxus est nota. "
        "Tertia insula est Melita. "
        "Melita est minima. Melita est in mari. "
        "In Melita, unus homo habitat. "
        "Homo solus est. Homo pisces capit. "
        "Melita est parva — sed est domus. "
        "Quarta insula est Chios. "
        "Chios est parva. Chios est in Graecia. "
        "In Chio, multi viri habitant. "
        "Chios est nota. Chios est pulchra. "
        "Quinta insula est Samos. "
        "Samos est parva. Samos est in Graecia. "
        "In Samo, multi viri habitant. "
        "Samos est pulchra. Samos est nota. "
        "Sexta insula est Delos. "
        "Delos est parva. Delos est sacra. "
        "In Delo, templum dei est. "
        "Delos est insula dei. "
        "Multi homines ad Delum veniunt. "
        "Septima insula est Cyprus. "
        "Cyprus est magna. Cyprus est in mari. "
        "In Cypro, multi montes sunt. "
        "Cyprus est terra bona. "
        "Septem insulae — septem sorores. "
        "Omnes sunt in mari. "
        "Omnes sunt in imperio. "
        "Ego has insulas vidi. "
        "Ego has insulas in corde habeo. "
        "Et quando in terra sum, "
        "ego de his insulis cogito."
    ),
}

STORIES["cap10_22"] = {
    "title_la": "Octo insulae",
    "title_zh": "八座岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Octo insulae in mari sunt. "
        "Omnes insulae sunt pulchrae. "
        "Omnes insulae sunt notae. "
        "Sicilia est prima insula. "
        "Sicilia est magna. Sicilia est in mari. "
        "Sicilia est prope Italiam. "
        "In Sicilia, mons magnus est. "
        "Mons ignem et fumum dat. "
        "Sicilia est terra bona. "
        "Sardinia est secunda insula. "
        "Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "In Sardinia, multi pastores sunt. "
        "Pastores oves habent. "
        "Sardinia est terra ferax. "
        "Corsica est tertia insula. "
        "Corsica est parva. Corsica est pulchra. "
        "In Corsica, multi montes sunt. "
        "In Corsica, multae silvae sunt. "
        "Creta est quarta insula. "
        "Creta est antiqua. Creta est magna. "
        "Creta est in Graecia. "
        "In Creta, dei antiqui fuerunt. "
        "Iuppiter in Creta puer fuit. "
        "Creta est insula sacra. "
        "Rhodos est quinta insula. "
        "Rhodos est in Graecia. "
        "Rhodos est pulchra. "
        "In Rhodo, multi flores sunt. "
        "In Rhodo, sol semper lucet. "
        "Lesbos est sexta insula. "
        "Lesbos est in Graecia. "
        "Lesbos est terra poetarum. "
        "In Lesbo, multi libri scripti sunt. "
        "Euboea est septima insula. "
        "Euboea est prope Graeciam. "
        "Euboea est longa. Euboea est ferax. "
        "Chios est octava insula. "
        "Chios est parva. Chios est in Graecia. "
        "Chios est pulchra. "
        "Octo insulae — octo portae. "
        "Omnes sunt in imperio. "
        "Omnes sunt Romanae. "
        "Nautae ad has insulas navigant. "
        "Mercatores ad has insulas eunt. "
        "Et omnes insulae sunt bonae."
    ),
}

STORIES["cap10_23"] = {
    "title_la": "Quattuor insulae Graecae",
    "title_zh": "四座希腊岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum Graecus. Ego in Graecia habito. "
        "Ego quattuor insulas Graecas bene novi. "
        "Prima insula est Creta. "
        "Creta est magna. Creta est antiqua. "
        "Creta est in mari. Creta est prope Graeciam. "
        "In Creta, multi montes sunt. "
        "In Creta, multae arbores sunt. "
        "Creta est terra bona. "
        "In Creta, dei antiqui habitaverunt. "
        "Iuppiter in Creta puer fuit. "
        "Iuppiter in Creta crevit. "
        "Creta est insula sacra. "
        "Creta est insula Iovis. "
        "Secunda insula est Rhodos. "
        "Rhodos est in mari. Rhodos est in Graecia. "
        "Rhodos est pulchra. In Rhodo, sol semper lucet. "
        "In Rhodo, multi flores sunt. "
        "In Rhodo, rosae multae sunt. "
        "Rhodos est insula solis. "
        "Multi homines ad Rhodon veniunt. "
        "Multi nautae ad Rhodon navigant. "
        "Tertia insula est Lesbos. "
        "Lesbos est in mari. Lesbos est in Graecia. "
        "Lesbos est pulchra. "
        "Lesbos est terra poetarum. "
        "In Lesbo, multi libri scripti sunt. "
        "In Lesbo, multi poetae habitaverunt. "
        "Lesbos est insula carminum. "
        "Quarta insula est Euboea. "
        "Euboea est in mari. Euboea est prope Graeciam. "
        "Euboea est longa. Euboea est ferax. "
        "In Euboea, multi montes sunt. "
        "In Euboea, multae silvae sunt. "
        "Euboea est insula magna. "
        "Quattuor insulae — quattuor sorores. "
        "Omnes sunt Graecae. Omnes sunt pulchrae. "
        "Omnes sunt in mari. Omnes sunt in imperio. "
        "Ego has insulas amo. "
        "Et quando in terra sum, "
        "ego de his insulis cogito."
    ),
}

STORIES["cap10_24"] = {
    "title_la": "Tria flumina Europae",
    "title_zh": "欧洲三河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tria flumina in Europa sunt. "
        "Omnia flumina sunt magna. "
        "Omnia flumina sunt nota. "
        "Rhenus est primum flumen. "
        "Rhenus est in Germania. "
        "Rhenus est flumen magnum. "
        "Rhenus est limes imperii. "
        "Rhenus Germaniam ab imperio dividit. "
        "Romani ad Rhenum stant. "
        "Romani Rhenum custodiunt. "
        "Trans Rhenum, Germania est. "
        "Trans Rhenum, Germani sunt. "
        "Germani sunt fortes. Germani sunt feri. "
        "Rhenus est porta. Rhenus est murus. "
        "Danuvius est secundum flumen. "
        "Danuvius est in imperio. "
        "Danuvius est flumen longum. "
        "Danuvius per multas terras fluit. "
        "Danuvius multas gentes tangit. "
        "Danuvius est limes. "
        "Danuvius imperium defendit. "
        "Ad Danuvium, multae gentes sunt. "
        "Ad Danuvium, multi milites sunt. "
        "Rhodanus est tertium flumen. "
        "Rhodanus est in Gallia. "
        "Rhodanus est flumen magnum. "
        "Rhodanus per Galliam fluit. "
        "Rhodanus ad mare it. "
        "Gallia est terra Romana. "
        "Rhodanus est flumen Romanum. "
        "In Gallia, multi montes sunt. "
        "In Gallia, multae silvae sunt. "
        "Rhodanus per Galliam currit. "
        "Rhodanus aquam multam portat. "
        "Tria flumina — tres vitae. "
        "Rhenus est custos. "
        "Danuvius est limes. "
        "Rhodanus est via. "
        "Omnia flumina sunt magna. "
        "Omnia flumina sunt Romana. "
        "Et flumina semper fluunt. "
        "Et flumina semper currunt."
    ),
}

STORIES["cap10_25"] = {
    "title_la": "Servus in horto",
    "title_zh": "园中奴隶",
    "target_chapter": 10,
    "theme": "58 主人与奴隶",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "奴隶",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego servus sum. Ego in horto laboro. "
        "Dominus meus in domo est. "
        "Dominus me non videt. "
        "Ego aquam porto. Ego herbas carpo. "
        "Sol est calidus. Ego multum sudo. "
        "Dominus non venit. Dominus non videt. "
        "Ego solus in horto sum. "
        "Nemo me vocat. Nemo me videt. "
        "Ego sum servus. Ego non sum liber. "
        "Dominus meus magnam domum habet. "
        "Dominus multos servos habet. "
        "Dominus multum cibum habet. "
        "Ego parum cibi habeo. "
        "Sed ego non sum malus. "
        "Ego bonus servus sum. "
        "Ego bene laboro. Ego domino pareo. "
        "Sed ego de libertate cogito. "
        "Ego liber esse volo. "
        "Ego in Graecia natus sum. "
        "In Graecia, ego liber fui. "
        "In Graecia, ego familiam habui. "
        "Sed Romani me ceperunt. "
        "Romani me servum fecerunt. "
        "Nunc ego in Italia sum. "
        "Nunc ego in horto laboro. "
        "Ego de Graecia cogito. "
        "De matre. De patre. De fratre. "
        "Ego eos videre volo. Sed non possum. "
        "Ego servus sum. Ego hinc ire non possum. "
        "Sed ego non despero. "
        "Aliquando, ego liber ero. "
        "Aliquando, ego ad Graeciam redibo. "
        "Aliquando, ego familiam meam videbo. "
        "Interim, ego in horto laboro. "
        "Ego aquam porto. Ego herbas carpo. "
        "Sol calidus est. Ego sudo. "
        "Sed in corde meo, ego liber sum. "
        "In corde meo, ego Graecus sum. "
        "Et hoc nemo mihi capere potest."
    ),
}

STORIES["cap10_26"] = {
    "title_la": "Forum Romanum",
    "title_zh": "罗马广场",
    "target_chapter": 10,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in foro sum. Forum est magnum. "
        "Forum est pulchrum. Forum est cor Romae. "
        "In foro, multi homines sunt. "
        "In foro, multae res sunt. "
        "Ego in foro ambulo. Ego multa video. "
        "Mercatores in foro sunt. "
        "Mercatores res vendunt. "
        "Alius mercator panem vendit. "
        "Panis est bonus. Panis est novus. "
        "Alius mercator vinum vendit. "
        "Vinum est bonum. Vinum est rubrum. "
        "Alius mercator vestes vendit. "
        "Vestes sunt pulchrae. "
        "Alius mercator libros vendit. "
        "Libri sunt antiqui. Libri sunt boni. "
        "Ego ad mercatorem eo. "
        "Ego librum video. Liber est pulcher. "
        "Ego: 'Quanti hic liber est?' "
        "Mercator: 'Hic liber decem nummos constat.' "
        "Ego pecuniam numero. Ego pecuniam do. "
        "Mercator librum mihi dat. "
        "Ego librum accipio. Ego laetus sum. "
        "In foro, multi viri sunt. "
        "Viri de rebus publicis loquuntur. "
        "Viri de imperio loquuntur. "
        "Alii viri tacent. Alii viri clamant. "
        "In foro, templa sunt. "
        "Templa sunt magna. Templa sunt pulchra. "
        "In templis, dei sunt. "
        "Homines ad templa eunt. "
        "Homines deos orant. "
        "In foro, statuae sunt. "
        "Statuae virorum magnorum sunt. "
        "Statuae sunt pulchrae. "
        "Ego in foro sto. Ego circum specto. "
        "Forum est magnum. Forum est pulchrum. "
        "Forum est cor Romae. "
        "In foro, vita Romae est. "
        "Ego forum amo. Ego Romam amo. "
        "Et ego in foro laetus sum."
    ),
}

# ============================================================
# 长篇 (800-1500 words) x7
# ============================================================

STORIES["cap10_27"] = {
    "title_la": "Mendicus ad portam",
    "title_zh": "门前的乞丐",
    "target_chapter": 10,
    "theme": "04 富与贫",
    "style": "冷峻",
    "genre": "M 伦理与习俗",
    "character_type": "乞丐",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego mendicus sum. Ego ad portam sto. "
        "Ego nihil habeo. Ego solus sum. "
        "Ego in via habito. Ego in via dormio. "
        "Ego panem non habeo. Ego aquam non habeo. "
        "Ego ad portam divitis viri sto. "
        "Ego manum extendo. Ego: 'Da mihi panem!' "
        "Dominus portam aperit. Dominus me videt. "
        "Dominus: 'Quis es tu? Cur hic stas?' "
        "Ego: 'Ego sum mendicus. Ego panem volo. "
        "Ego multos dies non comedi.' "
        "Dominus: 'Ego panem non habeo. "
        "Abi! Noli hic stare!' "
        "Dominus portam claudit. "
        "Ego iterum manum extendo. "
        "Ego alium virum video. "
        "Vir est dives. Vir multas vestes habet. "
        "Ego: 'Domine, da mihi panem! Ego fessus sum.' "
        "Vir dives me videt. Vir dives non respondet. "
        "Vir dives abit. Vir dives me non videt. "
        "Ego solus sum. Ego in via sedeo. "
        "Ego de vita mea cogito. "
        "Ego fui vir bonus. Ego familiam habui. "
        "Ego in oppido parvo habitavi. "
        "Ego uxorem habui. Ego filium habui. "
        "Sed bellum venit. Bellum omnia cepit. "
        "Domus mea deleta est. "
        "Familia mea mortua est. "
        "Ego solus remansi. "
        "Nunc ego mendicus sum. "
        "Nunc ego in via dormio. "
        "Nunc ego panem quaero. "
        "Ego ad multas portas sto. "
        "Multi viri me non vident. "
        "Multi viri abeunt. "
        "Sed aliquando, vir bonus venit. "
        "Vir bonus me videt. Vir bonus mihi panem dat. "
        "Vir bonus: 'Accipe panem, amice.' "
        "Ego: 'Gratias tibi ago. Gratias magnas!' "
        "Vir bonus: 'Noli desperare. "
        "Dei te vident. Dei te amant.' "
        "Ego panem consumo. Panis est bonus. "
        "Ego de viro bono cogito. "
        "In mundo, multi mali sunt. "
        "Sed etiam boni sunt. "
        "Et ego spero: aliquando, vita mea melior erit. "
        "Aliquando, ego non mendicus ero. "
        "Aliquando, ego domum habebo. "
        "Interim, ego ad portam sto. "
        "Ego manum extendo. Ego panem quaero. "
        "Et ego spero."
    ),
}

STORIES["cap10_28"] = {
    "title_la": "Mercator Graecus",
    "title_zh": "希腊商人",
    "target_chapter": 10,
    "theme": "41 财富与贫困",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "希腊人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum mercator. Ego Graecus sum. "
        "Ego in oppido magno habito. "
        "Ego multas res habeo. Ego multas res vendo. "
        "Ego ad forum eo. Ego in foro sto. "
        "Viri ad me veniunt. Viri res meas emunt. "
        "Ego pecuniam habeo. Ego dives sum. "
        "Sed ego non sum laetus. "
        "Ego solus sum. Ego amicos non habeo. "
        "Ego in Graecia natus sum. "
        "In Graecia, ego puer fui. "
        "In Graecia, ego multos amicos habui. "
        "Cum amicis, ego ludebam. "
        "Cum amicis, ego ad mare ibam. "
        "Sed pater meus mortuus est. "
        "Mater mea quoque mortua est. "
        "Ego Graeciam reliqui. "
        "Ego ad Italiam veni. "
        "Ego in Italia negotium coepi. "
        "Ego res emo et vendo. "
        "Ego pecuniam facio. Multam pecuniam. "
        "Sed pecunia non est omnia. "
        "Pecunia amicos non dat. "
        "Pecunia laetitiam non dat. "
        "Ego multas res habeo — sed cor meum vacuum est. "
        "Ego de Graecia cogito. "
        "De mari. De monte. De amicis. "
        "Ego Graeciam videre volo. "
        "Sed ego hinc ire non possum. "
        "Negotium meum me tenet. "
        "Aliquando, vir ad me venit. "
        "Vir est Graecus. Vir quoque mercator est. "
        "Vir: 'Salve, amice! Ego te novi. "
        "Tu es de Graecia, nonne?' "
        "Ego: 'Ita. Ego de Graecia sum. "
        "Ego Graeciam desidero.' "
        "Vir: 'Et ego. Graecia est pulchra terra. "
        "Sed hic, in Italia, vita est bona. "
        "Nos Graeci sumus — sed etiam Romani sumus. "
        "Nos duas terras in corde habemus.' "
        "Ego: 'Recte dicis. Graecia est mater. "
        "Roma est pater. Nos ambo sumus.' "
        "Ego et vir loquimur. "
        "Ego et vir amici sumus. "
        "Nunc ego non sum solus. "
        "Ego amicum habeo. "
        "Amicus meus Graecus est. "
        "Nos de Graecia loquimur. "
        "Nos de patria cogitamus. "
        "Et nunc ego laetus sum. "
        "Non quod dives sum — sed quod amicum habeo. "
        "Amicus est plus quam pecunia. "
        "Amicus est plus quam omnes res. "
        "Et ego hoc didici: "
        "pecunia non est omnia. "
        "Amor est omnia. Amicitia est omnia."
    ),
}

STORIES["cap10_29"] = {
    "title_la": "Duodecim insulae",
    "title_zh": "十二座岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum nauta Graecus. Ego multos annos in mari sum. "
        "Ego multas insulas vidi. Ego multa maria vidi. "
        "Nunc ego de duodecim insulis dicam. "
        "Haec est historia mea. "
        "Prima insula est Sicilia. "
        "Sicilia est maxima insula. "
        "Sicilia est prope Italiam. "
        "In Sicilia, mons magnus est. "
        "Mons ignem et fumum dat. "
        "Mons deus est. Mons sacer est. "
        "Sicilia multum frumentum dat. "
        "Sicilia est terra bona. "
        "Secunda insula est Sardinia. "
        "Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "In Sardinia, multi pastores sunt. "
        "Pastores oves habent. "
        "Pastores in montibus habitant. "
        "Sardinia est terra ferax. "
        "Tertia insula est Corsica. "
        "Corsica est parva. Corsica est pulchra. "
        "In Corsica, multi montes sunt. "
        "In Corsica, multae silvae sunt. "
        "Corsica est terra fera. "
        "Quarta insula est Creta. "
        "Creta est antiqua. Creta est magna. "
        "Creta est in Graecia. "
        "In Creta, dei antiqui fuerunt. "
        "Iuppiter in Creta puer fuit. "
        "Iuppiter in Creta crevit. "
        "Creta est insula sacra. "
        "Creta est insula Iovis. "
        "Quinta insula est Rhodos. "
        "Rhodos est in Graecia. "
        "Rhodos est pulchra. "
        "In Rhodo, sol semper lucet. "
        "In Rhodo, multi flores sunt. "
        "In Rhodo, rosae multae sunt. "
        "Rhodos est insula solis. "
        "Sexta insula est Lesbos. "
        "Lesbos est in Graecia. "
        "Lesbos est terra poetarum. "
        "In Lesbo, multi libri scripti sunt. "
        "In Lesbo, multi poetae habitaverunt. "
        "Lesbos est insula carminum. "
        "Septima insula est Euboea. "
        "Euboea est prope Graeciam. "
        "Euboea est longa. Euboea est ferax. "
        "In Euboea, multi montes sunt. "
        "In Euboea, multae silvae sunt. "
        "Octava insula est Chios. "
        "Chios est parva. Chios est in Graecia. "
        "Chios est pulchra. "
        "Nona insula est Samos. "
        "Samos est parva. Samos est in Graecia. "
        "Samos est pulchra. Samos est nota. "
        "Decima insula est Lemnos. "
        "Lemnos est parva. Lemnos est in mari. "
        "In Lemno, unus mons est. "
        "Lemnos est sola. Lemnos est pulchra. "
        "Undecima insula est Naxus. "
        "Naxus est parva. Naxus est in mari. "
        "In Naxo, multi flores sunt. "
        "Naxus est pulchra. "
        "Duodecima insula est Melita. "
        "Melita est minima. Melita est in mari. "
        "In Melita, pauci homines habitant. "
        "Melita est parva insula. "
        "Duodecim insulae — duodecim sorores. "
        "Omnes sunt in mari. Omnes sunt in imperio. "
        "Omnes sunt notae. Omnes sunt pulchrae. "
        "Ego ad has insulas navigavi. "
        "Ego has insulas vidi. "
        "Ego has insulas in corde habeo. "
        "Et quando in terra sum, "
        "ego de his insulis cogito. "
        "Et ego illas desidero. "
        "Mare est magnum. Insulae sunt multae. "
        "Sed hae duodecim sunt in corde meo. "
        "Et semper erunt."
    ),
}

STORIES["cap10_30"] = {
    "title_la": "Quattuor insulae Graecae",
    "title_zh": "四座希腊岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quattuor insulae Graecae in mari sunt. "
        "Omnes sunt pulchrae. Omnes sunt notae. "
        "Omnes sunt in imperio Romano. "
        "Prima insula est Samos. "
        "Samos est parva. Samos est in Graecia. "
        "Samos est in mari. Samos est pulchra. "
        "In Samo, multi viri habitant. "
        "In Samo, multae arbores sunt. "
        "In Samo, multae herbae sunt. "
        "Samos est terra bona. "
        "Samos est nota. Multi nautae ad Samum navigant. "
        "Multi mercatores ad Samum eunt. "
        "Secunda insula est Chios. "
        "Chios est parva. Chios est in Graecia. "
        "Chios est in mari. Chios est pulchra. "
        "In Chio, multi viri habitant. "
        "In Chio, multae arbores sunt. "
        "Chios est terra bona. "
        "Chios est nota. "
        "Multi nautae ad Chium navigant. "
        "Tertia insula est Rhodos. "
        "Rhodos est in Graecia. Rhodos est in mari. "
        "Rhodos est pulchra. "
        "In Rhodo, sol semper lucet. "
        "In Rhodo, multi flores sunt. "
        "In Rhodo, rosae multae sunt. "
        "Rhodos est insula solis. "
        "Deus solis Rhodon amat. "
        "Rhodos est insula dei. "
        "Multi homines ad Rhodon veniunt. "
        "Multi nautae ad Rhodon navigant. "
        "Rhodos est nota in toto imperio. "
        "Quarta insula est Creta. "
        "Creta est magna. Creta est antiqua. "
        "Creta est in mari. Creta est in Graecia. "
        "In Creta, multi montes sunt. "
        "In Creta, multae arbores sunt. "
        "Creta est terra bona. "
        "In Creta, dei antiqui habitaverunt. "
        "Iuppiter in Creta puer fuit. "
        "Iuppiter in Creta crevit. "
        "Iuppiter in Creta a matre sua celatus est. "
        "Pater Iovis eum quaerebat. "
        "Sed Iuppiter in Creta tutus fuit. "
        "Creta est insula sacra. "
        "Creta est insula Iovis. "
        "Multi homines ad Cretam veniunt. "
        "Multi nautae ad Cretam navigant. "
        "Quattuor insulae — quattuor sorores. "
        "Samos, Chios, Rhodos, Creta. "
        "Omnes sunt Graecae. Omnes sunt pulchrae. "
        "Omnes sunt in mari. Omnes sunt in imperio. "
        "Et omnes sunt notae. "
        "Et omnes sunt bonae."
    ),
}

STORIES["cap10_31"] = {
    "title_la": "Duodecim insulae",
    "title_zh": "十二座岛",
    "target_chapter": 10,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duodecim insulae in mari sunt. "
        "Omnes sunt pulchrae. Omnes sunt notae. "
        "Omnes sunt in imperio Romano. "
        "Sicilia est prima insula. "
        "Sicilia est maxima. Sicilia est prope Italiam. "
        "In Sicilia, mons magnus est. "
        "Mons ignem et fumum dat. "
        "Mons est sacer. Mons deus est. "
        "Sicilia multum frumentum dat. "
        "Sicilia est terra bona. "
        "Sardinia est secunda insula. "
        "Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "In Sardinia, multi pastores sunt. "
        "Pastores oves habent. "
        "Pastores in montibus habitant. "
        "Sardinia est terra ferax. "
        "Corsica est tertia insula. "
        "Corsica est parva. Corsica est pulchra. "
        "In Corsica, multi montes sunt. "
        "In Corsica, multae silvae sunt. "
        "Corsica est terra fera. "
        "Creta est quarta insula. "
        "Creta est antiqua. Creta est magna. "
        "Creta est in Graecia. "
        "In Creta, dei antiqui fuerunt. "
        "Iuppiter in Creta puer fuit. "
        "Creta est insula sacra. "
        "Rhodos est quinta insula. "
        "Rhodos est in Graecia. "
        "Rhodos est pulchra. "
        "In Rhodo, sol semper lucet. "
        "In Rhodo, multi flores sunt. "
        "Rhodos est insula solis. "
        "Lesbos est sexta insula. "
        "Lesbos est in Graecia. "
        "Lesbos est terra poetarum. "
        "In Lesbo, multi libri scripti sunt. "
        "Lesbos est insula carminum. "
        "Euboea est septima insula. "
        "Euboea est prope Graeciam. "
        "Euboea est longa. Euboea est ferax. "
        "In Euboea, multi montes sunt. "
        "Chios est octava insula. "
        "Chios est parva. Chios est in Graecia. "
        "Chios est pulchra. "
        "Samos est nona insula. "
        "Samos est parva. Samos est in Graecia. "
        "Samos est pulchra. Samos est nota. "
        "Lemnos est decima insula. "
        "Lemnos est parva. Lemnos est in mari. "
        "In Lemno, unus mons est. "
        "Lemnos est sola. Lemnos est pulchra. "
        "Naxus est undecima insula. "
        "Naxus est parva. Naxus est in mari. "
        "In Naxo, multi flores sunt. "
        "Naxus est pulchra. "
        "Melita est duodecima insula. "
        "Melita est minima. Melita est in mari. "
        "In Melita, pauci homines habitant. "
        "Melita est parva insula. "
        "Duodecim insulae — duodecim sorores. "
        "Omnes sunt in mari. Omnes sunt in imperio. "
        "Omnes sunt notae. Omnes sunt pulchrae. "
        "Nautae ad has insulas navigant. "
        "Mercatores ad has insulas eunt. "
        "Et omnes insulae sunt bonae. "
        "Et omnes insulae sunt Romanae."
    ),
}

STORIES["cap10_32"] = {
    "title_la": "Sex insulae parvae",
    "title_zh": "六座小岛",
    "target_chapter": 10,
    "theme": "13 孤独",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego sum viator. Ego per mare navigo. "
        "Ego multas terras vidi. Ego multa maria vidi. "
        "Nunc ego de sex insulis parvis dicam. "
        "Prima insula est Lemnos. "
        "Lemnos est parva. Lemnos est in mari. "
        "In Lemno, unus mons est. "
        "In Lemno, pauca arbores sunt. "
        "In Lemno, pauci homines habitant. "
        "Lemnos est sola. Lemnos est pulchra. "
        "Ego ad Lemnum veni. "
        "Ego in Lemno ambulavi. "
        "Ego montem vidi. Ego mare vidi. "
        "Lemnos est parva — sed est bona. "
        "Secunda insula est Naxus. "
        "Naxus est parva. Naxus est in mari. "
        "In Naxo, multi flores sunt. "
        "In Naxo, multae herbae sunt. "
        "In Naxo, multi homines habitant. "
        "Naxus est pulchra. Naxus est nota. "
        "Ego ad Naxum veni. "
        "Ego in Naxo ambulavi. "
        "Ego flores vidi. Ego herbas vidi. "
        "Naxus est pulchra — et est bona. "
        "Tertia insula est Melita. "
        "Melita est minima. Melita est in mari. "
        "In Melita, unus homo habitat. "
        "Homo solus est. Homo pisces capit. "
        "Homo in casa parva habitat. "
        "Melita est parva — sed est domus. "
        "Ego ad Melitam veni. "
        "Ego hominem vidi. "
        "Homo: 'Salve, viator! Cur hic es?' "
        "Ego: 'Ego insulas videre volo. "
        "Ego de mundo scire volo.' "
        "Homo: 'Mundus est magnus. "
        "Sed haec insula est meus mundus. "
        "Hic, ego sum liber. Hic, ego sum meus.' "
        "Ego cum homine loquor. "
        "Homo mihi de vita sua dicit. "
        "Homo est laetus. Homo est liber. "
        "Ego Melitam relinquo. "
        "Sed verba hominis in corde meo manent. "
        "Quarta insula est Chios. "
        "Chios est parva. Chios est in Graecia. "
        "In Chio, multi viri habitant. "
        "Chios est nota. Chios est pulchra. "
        "Ego ad Chium veni. "
        "Ego in Chio ambulavi. "
        "Chios est pulchra — et est bona. "
        "Quinta insula est Samos. "
        "Samos est parva. Samos est in Graecia. "
        "In Samo, multi viri habitant. "
        "Samos est pulchra. Samos est nota. "
        "Ego ad Samum veni. "
        "Ego in Samo ambulavi. "
        "Samos est pulchra — et est bona. "
        "Sexta insula est Delos. "
        "Delos est parva. Delos est sacra. "
        "In Delo, templum dei est. "
        "Delos est insula dei. "
        "Multi homines ad Delum veniunt. "
        "Multi homines deum orant. "
        "Ego ad Delum veni. "
        "Ego templum vidi. Ego deum oravi. "
        "Delos est sacra — et est bona. "
        "Sex insulae — sex sorores. "
        "Omnes sunt parvae. Omnes sunt pulchrae. "
        "Omnes sunt in mari. Omnes sunt in imperio. "
        "Ego has insulas vidi. "
        "Ego has insulas in corde habeo. "
        "Et quando in terra sum, "
        "ego de his insulis cogito. "
        "Et ego illas desidero."
    ),
}

STORIES["cap10_33"] = {
    "title_la": "Septem flumina Asiae",
    "title_zh": "亚洲七河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Septem flumina in Asia sunt. "
        "Omnia flumina sunt magna. "
        "Omnia flumina sunt nota. "
        "Tigris est primum flumen. "
        "Tigris est in Asia. Tigris est flumen magnum. "
        "Tigris per multas terras fluit. "
        "Tigris aquam multam portat. "
        "Ad Tigrim, multae gentes habitant. "
        "Ad Tigrim, multa oppida sunt. "
        "Tigris est flumen notum. "
        "Euphrates est secundum flumen. "
        "Euphrates est in Asia. "
        "Euphrates est flumen magnum. "
        "Euphrates prope Tigrim fluit. "
        "Tigris et Euphrates fratres sunt. "
        "Inter Tigrim et Euphratem, terra bona est. "
        "Ibi, multae gentes habitant. "
        "Ibi, multa oppida sunt. "
        "Indus est tertium flumen. "
        "Indus est in Asia. Indus est flumen magnum. "
        "Indus per multas terras fluit. "
        "Indus aquam multam portat. "
        "Ad Indum, multae gentes habitant. "
        "Indus est flumen notum. "
        "Ganges est quartum flumen. "
        "Ganges est in Asia. Ganges est flumen magnum. "
        "Ganges per multas terras fluit. "
        "Ganges aquam multam portat. "
        "Ad Gangem, multae gentes habitant. "
        "Ganges est flumen sacrum. "
        "Multi homines ad Gangem veniunt. "
        "Nilus est quintum flumen. "
        "Nilus est in Aegypto. Nilus est flumen magnum. "
        "Nilus Aegypto aquam dat. "
        "Sine Nilo, Aegyptus non est. "
        "Nilus omni anno crescit. "
        "Nilus terram bonam facit. "
        "Nilus est pater Aegypti. "
        "Iordanes est sextum flumen. "
        "Iordanes est in Asia. "
        "Iordanes est flumen parvum. "
        "Iordanes per terram sacram fluit. "
        "Iordanes aquam dat. "
        "Iordanes est flumen notum. "
        "Orontes est septimum flumen. "
        "Orontes est in Asia. "
        "Orontes est flumen parvum. "
        "Orontes per Syriam fluit. "
        "Orontes aquam dat. "
        "Orontes est flumen notum. "
        "Septem flumina — septem vitae. "
        "Tigris et Euphrates sunt fratres. "
        "Indus et Ganges sunt magni. "
        "Nilus est pater. "
        "Iordanes et Orontes sunt parvi. "
        "Sed omnia flumina sunt bona. "
        "Omnia flumina aquam dant. "
        "Omnia flumina terras coniungunt. "
        "Et flumina semper fluunt. "
        "Et flumina semper currunt."
    ),
}

# ============================================================
# 评估与输出
# ============================================================

def main():
    os.makedirs(REALITATES_DIR / "Cap10", exist_ok=True)
    results = []

    for key, story in STORIES.items():
        text = story["text"]
        name = story["title_la"]
        r = evaluate(text, name)
        wc = len(text.split())
        target = story["target_chapter"]
        verdict = "PASS" if r["v2_level"] is not None and r["v2_level"] <= target + 2 else "FAIL"
        print(f"{key} {name}: wc={wc} v2_level={r['v2_level']} v2_rate={r['v2_rate']}% -> {verdict}")
        if r["v2_oov"]:
            print(f"  OOV: {r['v2_oov'][:20]}")
        results.append((key, story, r, wc, verdict))

    # 生成 Markdown 文件
    for key, story, r, wc, verdict in results:
        story_text = story["text"]
        cap = story["target_chapter"]
        tier_en = {"中篇": "medius", "中长篇": "longior", "长篇": "longus"}[story["length_tier"]]
        title_slug = story["title_la"].replace(" ", "_")
        cap_dir = REALITATES_DIR / f"Cap{cap}"
        existing_nums = set()
        for f in cap_dir.glob("*.md"):
            parts = f.stem.split("_")
            for p in parts:
                if p.isdigit() and len(p) == 3:
                    existing_nums.add(int(p))
        nnn = 1
        while nnn in existing_nums:
            nnn += 1
        filename = f"Cap{cap}_{title_slug}_{tier_en}_{nnn:03d}.md"
        filepath = cap_dir / filename
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

    if passed == len(results):
        print("All passed!")
    else:
        print("Some failed - review and fix vocabulary.")

if __name__ == "__main__":
    main()