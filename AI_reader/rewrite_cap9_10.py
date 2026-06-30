#!/usr/bin/env python3
"""rewrite_cap9_10.py — 重写 Cap.9 和 Cap.10 的 44 篇短篇为扩展篇。
Cap.9: 6 中篇 + 3 中长篇 + 2 长篇 (v2_level <= 11)
Cap.10: 16 中篇 + 10 中长篇 + 7 长篇 (v2_level <= 12)
非严格模式：自由使用 Cap.1-9/10 词汇，通过算法验证即可。
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
# Cap.9 — 中篇 (300-500 words) x6
# 策略：完全重用Cap.7/Cap.8已验证安全词汇，额外加入Cap.9词汇。
# 避开所有lemma map中Ch.12+的词元。
# ============================================================

STORIES["cap9_01"] = {
    "title_la": "Insula parva",
    "title_zh": "小岛",
    "target_chapter": 9,
    "theme": "13 孤独",
    "style": "精炼",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in insula sum. Insula est parva. Insula in aqua est. Aqua est magna. "
        "Ego solus sum. Nullus alius vir in insula est. Nullae feminae in insula sunt. "
        "Ego sum solus — sed non sum miser. "
        "Insula est parva, sed pulchra. In insula sunt arbores. Arbores sunt magnae. "
        "In insula sunt rosae. Rosae sunt multae. Rosae sunt pulchrae. "
        "In insula est aqua. Aqua est bona. "
        "Ego in insula ambulo. Ego terram video. Terra est bona. "
        "Ego ad aquam eo. Aqua est pulchra. Aqua est frigida — sed bona. "
        "Ego in aqua pedes pono. Ego in aqua sto. "
        "In insula aves sunt. Aves in arboribus cantant. Aves volant. "
        "Ego aves video. Aves sunt pulchrae. "
        "Ego in insula laetus sum. "
        "In magnis oppidis, multi viri sunt. "
        "In oppidis, multae viae sunt. In oppidis, multa aedificia sunt. "
        "Sed in oppidis, multi clamores sunt. "
        "Hic, in insula, ego de nullis clamoribus puto. "
        "Hic, ego de sole puto. De aqua puto. De vento puto. "
        "Sol me calidum facit. Ventus me frigidum facit. Aqua mihi cantat. "
        "Ego non sum solus. Aqua mecum est. Caelum mecum est. Terra mecum est. "
        "Ego in terra sedeo. Ego oculos claudo. Ego audio. "
        "Aqua venit. Aqua abit. Aqua venit et abit. "
        "Aqua semper venit. Aqua semper abit. "
        "Ego haec video: parvum potest esse bonum. "
        "Multi viri in magnis oppidis sunt — sed non sunt laeti. "
        "Ego in parva insula sum — et ego sum laetus. "
        "Insula mea est parva. Insula mea est pulchra. Insula mea est mea. "
        "Ego hic maneo. Ego in insula mea laetus sum. "
        "Et ego in insula mea laetus maneo."
    ),
}

STORIES["cap9_02"] = {
    "title_la": "Quinque terrae",
    "title_zh": "五地",
    "target_chapter": 9,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quinque terrae in Europa sunt. Roma est caput. Graecia est terra bona. "
        "Gallia est terra magna. Hispania est terra pulchra. Britannia est insula magna. "
        "Vir Romanus in Roma est. Vir multas terras vidit. "
        "Vir est mercator. Vir per multas terras ambulat. "
        "Vir in foro stat. Vir de terris putat. "
        "Vir: 'Roma est maxima. In Roma, omnes viae sunt. "
        "In Roma, multa aedificia sunt. Roma est caput.' "
        "Vir de Graecia putat. Vir in Graecia fuit. "
        "Vir: 'Graecia est terra bona. In Graecia, viri boni sunt. "
        "In Graecia, viri multa sciunt. Graecia est terra bona.' "
        "Vir de Gallia putat. Vir in Gallia fuit. "
        "Vir: 'Gallia est terra magna. Viri Galliae sunt fortes. "
        "Sed Roma Galliam vicit. Gallia est terra Romana.' "
        "Vir de Hispania putat. Vir in Hispania fuit. "
        "Vir: 'Hispania est terra pulchra. In Hispania, multi montes sunt. "
        "Hispania est terra bona.' "
        "Vir de Britannia putat. Vir in Britannia non fuit. "
        "Sed vir de Britannia audivit. "
        "Vir: 'Britannia est insula magna. Britannia est in aqua magna. "
        "Viri Britanniae sunt fortes. Britannia est ultima terra.' "
        "Vir in foro stat. Vir quinque terras videt. "
        "Vir: 'Roma est caput. Graecia est bona. Gallia est magna. "
        "Hispania est pulchra. Britannia est ultima.' "
        "Amicus viri ad eum venit. Amicus: 'De quibus terris putas?' "
        "Vir: 'De quinque terris Europae puto. Omnes sunt bonae — "
        "et omnes sunt partes imperii.' "
        "Amicus: 'Quae terra est optima?' "
        "Vir: 'Optima est Roma. Roma est patria. Roma est domus. "
        "Sed omnes terrae sunt bonae. Et omnes sunt Romanae.' "
        "Vir ad caelum spectat. Vir: 'Europa est magna. Imperium est magnum. "
        "Et nos, Romani, in medio sumus.' "
        "Et vir in foro stat — et laetus est."
    ),
}

STORIES["cap9_03"] = {
    "title_la": "Tria oppida",
    "title_zh": "三城",
    "target_chapter": 9,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tria oppida in Italia sunt. Roma est oppidum magnum. "
        "Tusculum est oppidum parvum. Capua est oppidum pulchrum. "
        "Vir Romanus in Italia est. Vir multa oppida videt. "
        "Vir Romanus in Roma est. Vir Romam amat. Vir in Roma habitat. "
        "Vir primum Romam spectat. Roma est oppidum magnum. "
        "In Roma, multae viae sunt. In Roma, multi viri sunt. "
        "In Roma, multi horti sunt. In Roma, multae feminae sunt. "
        "In Roma, multi pueri sunt. Roma est oppidum magnum et bonum. "
        "Vir: \"Roma est oppidum magnum. In Roma, multa sunt. "
        "In Roma, viri boni sunt. In Roma, feminae pulchrae sunt. "
        "Roma est caput. Roma est bona.\" "
        "Tum vir Tusculum videt. Tusculum est oppidum parvum. "
        "Tusculum prope Romam est. Vir ad Tusculum it. "
        "In Tusculo, viae sunt parvae. In Tusculo, viri sunt pauci. "
        "In Tusculo, arbores sunt multae. In Tusculo, rosae sunt pulchrae. "
        "Tusculum est oppidum parvum, sed pulchrum. "
        "In Tusculo, multi horti sunt. In Tusculo, arbores sunt magnae. "
        "In Tusculo, aves cantant. In Tusculo, aqua est bona. "
        "Vir: \"Tusculum est oppidum parvum. Sed Tusculum est pulchrum. "
        "In Tusculo, viri laeti sunt. Hic, bonum est.\" "
        "Tum vir Capuam videt. Capua est oppidum pulchrum. "
        "Capua prope aquam est. Vir ad Capuam it. "
        "In Capua, viae sunt pulchrae. In Capua, multi viri sunt. "
        "In Capua, multi mercatores sunt. Viri ex multis terris veniunt. "
        "Mercatores in viis sunt. Mercatores multa habent. "
        "Vir: \"Capua est oppidum pulchrum. In Capua, multa sunt. "
        "Capua est oppidum bonum. Mercatores in Capua sunt boni.\" "
        "Vir de tribus oppidis putat. Vir in via sedet. Vir putat. "
        "Vir: \"Roma est magna. Tusculum est parvum. Capua est pulchra. "
        "Tria oppida — tria bona. Roma est caput. Tusculum est bonum. "
        "Capua est pulchra. In his tribus oppidis, Italia est.\" "
        "Vir ad Romam it. Vir laetus est. Vir in Roma est. "
        "Vir: \"Roma est oppidum meum. Roma est terra mea. "
        "Sed Tusculum est bonum. Capua est pulchra. "
        "Tria oppida sunt bona. Et tria sunt in Italia.\" "
        "Et vir in Roma laetus est."
    ),
}

STORIES["cap9_04"] = {
    "title_la": "Duae terrae",
    "title_zh": "两地",
    "target_chapter": 9,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duae terrae in corde viri sunt. Una est Roma. Una est Graecia. "
        "Vir Romanus in Graecia habitat. Vir Romam et Graeciam pulchras putat. "
        "Vir ad mare ambulat. Mare est magnum. Mare est bonum. "
        "Vir: \"Mare est magnum. Mare est pulchrum. Mare Graeciae aquam dat. "
        "Mare est bonum. Mare multas terras tangit.\" "
        "Vir multa in Graecia videt. Vir in Graecia ambulat. "
        "Vir: \"Viae Graeciae sunt pulchrae. Viri Graeciae multa sunt. "
        "Viri Graeciae boni sunt. Viri in campo ambulant. "
        "Viri in via ambulant. Viri Graeciae boni sunt. "
        "Graecia est terra bona.\" "
        "Vir de Roma putat. Vir: \"Roma est longe ab hac terra. "
        "In Roma, familia mea est. In Roma, pater meus est. "
        "Mater mea est. Filii mei sunt. Ego eos videre volo. "
        "Ego patrem meum videre volo. Ego matrem meam videre volo. "
        "Ego filios meos videre volo.\" "
        "Vir familiam suam in Roma reliquit. "
        "Vir: \"Ego familiam meam exspecto. Ego ad eam ire volo. "
        "Familia mea est in Roma. Roma est longe.\" "
        "Amicus viri ad eum venit. Amicus est vir ex Graecia. "
        "Amicus: \"Cur tu non es laetus? Graecia est terra pulchra. "
        "In Graecia, sol est bonus. In Graecia, mare est pulchrum. "
        "In Graecia, viri sunt boni.\" "
        "Vir: \"Graecia est pulchra. Sed Roma est terra mea. "
        "Terra mea in corde meo est. In corde meo, Roma est.\" "
        "Amicus: \"Ego quoque terram meam pulchram puto. "
        "Graecia est terra mea. Sed Graecia et Roma una sunt. "
        "Graecia est terra Romana. Roma et Graecia sunt una.\" "
        "Vir: \"Graecia est terra bona. Sed cor meum Romanum est. "
        "Ego Romanus sum. Roma me vocat. Ego Romam audio.\" "
        "Vir ad mare spectat. Vir: \"Graecia me multa dedit. "
        "Graecia me multa dedit. Sed Roma est mea. "
        "Ego ad Romam ibo. Ego ad familiam meam ibo.\" "
        "Amicus: \"Et ego te in corde habebo. Tu es amicus bonus. "
        "Amicus bonus est magnum bonum. Amicus meus es.\" "
        "Vir et amicus manus tenent. Duo viri, duae terrae — sed bonum est. "
        "Vir: \"Graecia est pulchra. Roma est bona. "
        "Graecia et Roma in corde meo sunt. Et amicus bonus est in corde meo.\" "
        "Et vir et amicus laeti sunt. Vir ad Romam it. "
        "Sed vir Graeciam in corde habet. Et Graecia in corde viri est."
    ),
}

STORIES["cap9_05"] = {
    "title_la": "Octo montes",
    "title_zh": "八座山",
    "target_chapter": 9,
    "theme": "18 自然",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Octo montes in Italia sunt. Multi montes sunt magni. Multi montes sunt pulchri. "
        "Primus mons est mons deorum. In hoc monte, dei sunt. "
        "Dei hic habitant. Dei hic sunt boni. Dei de caelo hic spectant. "
        "Secundus mons est mons aquarum. In hoc monte, aquae sunt. "
        "Aquae sunt bonae. Aquae sunt multae. Aquae de monte fluunt. "
        "Tertius mons est mons virorum. In hoc monte, viri sunt. "
        "Viri sunt boni. Viri sunt magni. Viri in monte ambulant. "
        "Alius mons est mons silvarum. In hoc monte, silvae sunt. "
        "Silvae sunt magnae. Arbores sunt magnae. Aves in silvis cantant. "
        "Alius mons est mons herbarum. In hoc monte, herbae sunt. "
        "Herbae sunt multae. Herbae sunt bonae. Viri herbas habent. "
        "Alius mons est mons avium. In hoc monte, aves sunt. "
        "Aves sunt multae. Aves cantant. Aves sunt pulchrae. Aves volant. "
        "Alius mons est mons rosarum. In hoc monte, rosae sunt. "
        "Rosae sunt multae. Rosae sunt pulchrae. Rosae rubrae sunt. "
        "Alius mons est mons solis. In hoc monte, sol est. "
        "Sol est bonus. Sol est magnus. Sol montes tangit. "
        "Vir Romanus de his montibus putat. Vir montes pulchros putat. "
        "Vir in monte ambulat. Vir aquam in monte bibit. "
        "Vir aves in monte audit. Vir rosas in monte videt. "
        "Vir: \"Octo montes. Octo bona. In montibus, dei sunt. "
        "In montibus, aquae sunt. In montibus, viri sunt. "
        "In montibus, silvae sunt. In montibus, herbae sunt. "
        "In montibus, aves sunt. In montibus, rosae sunt. "
        "In montibus, sol est. Octo montes — octo bona. "
        "Montes sunt boni. Viri ad montes veniunt. "
        "Viri in montibus sunt laeti.\" "
        "Vir in monte sedet. Vir montes videt. "
        "Vir: \"Montes sunt magni. Montes sunt pulchri. "
        "Montes sunt boni. Viri in montibus sunt parvi. "
        "Sed montes sunt magni. Et montes sunt boni. "
        "In montibus, viri dei vident. In montibus, viri caelum tangunt. "
        "Montes sunt portae ad caelum.\" "
        "Et vir in monte laetus est. Vir montes spectat. "
        "Et montes sunt pulchri."
    ),
}

STORIES["cap9_06"] = {
    "title_la": "Magnum et parvum",
    "title_zh": "大与小",
    "target_chapter": 9,
    "theme": "11 自然与文明",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pater et filius ambulant. Filius est puer parvus. "
        "Filius multa rogat. "
        "Filius: \"Pater, cur Roma est magna? Cur oppidum nostrum est parvum?\" "
        "Pater: \"Fili, veni. Ego tibi monstro.\" "
        "Pater et filius ad collem eunt. Collis est altus. "
        "Pater: \"Ecce. Aspice oppidum de colle.\" "
        "Filius oppidum de colle aspicit. Oppidum est parvum. "
        "Filius: \"Oppidum est parvum! In oppido, res mihi magnae erant.\" "
        "Pater: \"Hoc est, fili. Prope es — res magnae sunt. "
        "Longe es — res parvae sunt.\" "
        "Filius: \"Sed Roma est magna de colle — nonne, pater?\" "
        "Pater: \"Roma quoque, si longe eas, parva erit. "
        "Si ad caelum eas, terra parva erit.\" "
        "Filius: \"Terra est parva? Sed terra est magna!\" "
        "Pater: \"Terra est magna quod in terra sumus. "
        "Sed in caelo, multae stellae sunt. Terra est una. "
        "Terra non est sola. Terra est inter stellas.\" "
        "Filius: \"Ergo magnum et parvum sunt in oculis?\" "
        "Pater: \"Ita, fili. Magnum et parvum sunt in oculis. "
        "Quod tibi magnum est, aliis parvum est.\" "
        "Filius: \"Pater, ego intellego. Res non sunt magnae per se. "
        "Res non sunt parvae per se. Oculi faciunt magnum et parvum.\" "
        "Pater: \"Bene, fili. Tu es bonus. Et hoc est bonum.\" "
        "Filius: \"Ego sum ego, pater. Et hoc est bonum.\" "
        "Pater et filius de colle descendunt. "
        "Filius oppidum intrat. Iam oppidum est bonum. "
        "Et filius laetus est."
    ),
}

# ============================================================
# Cap.9 — 中长篇 (500-800 words) x3
# ============================================================

STORIES["cap9_07"] = {
    "title_la": "Tres in horto",
    "title_zh": "园中三物",
    "target_chapter": 9,
    "theme": "18 自然",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tres res in horto sunt: rosa, lilium, et arbor. "
        "Hortus est in villa. Villa est prope montes. "
        "Dominus horti est vir bonus. Vir hortum pulchrum putat. "
        "Vir in horto ambulat. Vir rosam videt. "
        "Rosa est pulchra. Rosa est rubra. Rosa est bona. "
        "Vir: \"Rosa, tu es pulchra. Omnes qui te vident, te pulchram putant. "
        "Tu es pulchra inter flores.\" "
        "Rosa non respondet. Sed rosa in sole est. "
        "Vir lilium videt. "
        "Lilium est album. Lilium est pulchrum. "
        "Vir: \"Lilium, tu es album. Tu es pulchrum. "
        "Tu es sicut puella bona.\" "
        "Lilium non respondet. Sed lilium in vento movetur. "
        "Vir arborem videt. "
        "Arbor est magna. Arbor non est pulchra sicut rosa. "
        "Arbor non est pulchra sicut lilium. "
        "Vir: \"Arbor, tu non es pulchra. Folia tua sunt parva. "
        "Cur te in horto meo habeo?\" "
        "Arbor non respondet. Sed arbor stat. "
        "Vir in horto sedet. Vir de tribus rebus putat. "
        "Vir: \"Rosa est pulchra. Sed rosa non multum tempus manet. "
        "Post paucos dies, rosa cadit. "
        "Lilium est pulchrum. Sed lilium non multum tempus manet. "
        "Post paucos dies, lilium cadit.\" "
        "Vir arborem videt. "
        "Vir: \"Arbor non est pulchra. Sed arbor multum tempus manet. "
        "Arbor est magna. Arbor manet. "
        "Arbor dat umbram. Arbor est bona.\" "
        "Vir: \"Rosa est pulchra — sed cadit. "
        "Lilium est pulchrum — sed cadit. "
        "Arbor est bona — et manet.\" "
        "Vir: \"In vita, multi pulchra quaerunt. "
        "Sed id quod manet — hoc est bonum.\" "
        "Vir arborem tangit. Arbor est magna. "
        "Vir: \"Arbor, tu non es pulchra — sed tu es bona. "
        "Et hoc est magnum.\" "
        "Vir ad villam it. Sol cadit. Hortus in umbra est. "
        "Rosa in umbra est. Lilium in umbra est. Arbor in umbra est. "
        "Sed arbor stat. Arbor stat."
    ),
}

STORIES["cap9_08"] = {
    "title_la": "Duo canes",
    "title_zh": "两只狗",
    "target_chapter": 9,
    "theme": "32 友谊与孤独",
    "style": "白话",
    "genre": "A 童话",
    "character_type": "拟人动物",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duo canes in villa sunt. Unus canis est magnus. Unus canis est parvus. "
        "Canis magnus villam servat. Canis magnus latrat. "
        "Canis parvus non servat. Canis parvus est amicus. "
        "Canis parvus in villa ludit. Canis parvus cum pueris ludit. "
        "Canis magnus canem parvum non amat. "
        "Canis magnus: \"Tu es malus canis. Tu non servas. Tu non latras. "
        "Tu solum ludis. Ego sum bonus canis.\" "
        "Canis parvus: \"Sed ego pueros laetos facio. "
        "Ego dominum laetum facio. Nonne hoc bonum est?\" "
        "Canis magnus: \"Ludus non est bonus. Ego sum fortis. Ego sum bonus.\" "
        "Canis parvus tacet. Canis parvus non est laetus. "
        "Nocte, vir malus ad villam venit. Vir malus est magnus. "
        "Canis magnus virum malum videt. Canis magnus latrat. Canis magnus virum petit. "
        "Sed vir malus est fortis. Vir malus canem magnum pulsat. Canis magnus cadit. "
        "Canis parvus hoc videt. Canis parvus est parvus — sed virum petit. "
        "Canis parvus non est fortis — sed est parvus. Canis parvus virum mordet. "
        "Vir clamat. Canis parvus iterum mordet. Vir malus fugit. Vir villam non intrat. "
        "Canis magnus in terra est. Canis magnus non est bonus. "
        "Canis parvus ad canem magnum currit. "
        "Canis parvus: \"Ego sum parvus. Sed ego te amo. "
        "Tu es amicus meus. Sine te, ego sum solus.\" "
        "Canis magnus oculos aperit. Canis magnus canem parvum videt. "
        "Canis magnus: \"Tu me servavisti. Ego te non amabam — sed tu me servavisti. "
        "Ego dixi te malum esse — sed tu es bonus.\" "
        "Canis parvus: \"Tu es amicus meus. Amicus amicum servat.\" "
        "Mane, dominus canes videt. "
        "Dominus: \"Canis magnus non est bonus! Canis parvus eum curat!\" "
        "Dominus cani magno aquam dat. Canis magnus bonus fit. "
        "Canis magnus et canis parvus nunc una sunt. "
        "Canis magnus: \"Ego didici. Parvus canis potest magnum esse.\" "
        "Canis parvus: \"Et ego didici. Canis, magnus aut parvus, "
        "aliquid boni potest facere.\" "
        "Duo canes in villa sunt. Unus est magnus. Unus est parvus. "
        "Et duo sunt amici."
    ),
}

STORIES["cap9_09"] = {
    "title_la": "Pastor et oves",
    "title_zh": "牧人与羊",
    "target_chapter": 9,
    "theme": "36 乡村",
    "style": "白话",
    "genre": "A 童话",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pastor in monte est. Pastor oves habet. "
        "Oves sunt multae. Oves sunt albae et nigrae. "
        "Pastor oves amat. Pastor oves vocat. "
        "Una ovis est Alba. Una ovis est Nigra. Una ovis est Parva. "
        "Pastor cum ovibus in monte est. "
        "Pastor: \"Alba! Nigra! Parva! Venite!\" "
        "Oves ad pastorem veniunt. Oves pastorem amant. "
        "Pastor eis herbam dat. Pastor eis aquam dat. "
        "Pastor in monte solus est. Sed cum ovibus non est solus. "
        "Pastor: \"Oves, vos estis familia mea. Pater meus non est. "
        "Mater mea non est. Sed vos estis meae. Et ego sum vester.\" "
        "Oves balant. Pastor: \"Ego vos amo. Et vos me amatis.\" "
        "Lupus ad montem venit. Lupus est magnus. Lupus est malus. "
        "Lupus oves videt. Pastor lupum videt. "
        "Pastor: \"Lupus! Lupus in monte est!\" "
        "Pastor baculum tenet. Pastor lupum petit. "
        "Lupus pastorem videt. Lupus non timet. "
        "Pastor lupum pulsat. Lupus fugit. Oves sunt salvae. "
        "Pastor in terra sedet. "
        "Alba ad pastorem venit. Nigra ad pastorem venit. "
        "Parva ad pastorem venit. "
        "Pastor: \"Oves, vos estis familia mea. "
        "Pastor et oves — una familia sumus.\" "
        "Mercator ad montem venit. "
        "Mercator: \"Pastor, ego oves tuas volo. Ego tibi pecuniam do.\" "
        "Pastor: \"Oves meae non sunt venales. Oves meae sunt familia mea.\" "
        "Mercator: \"Familia? Oves sunt bestiae. Non sunt homines.\" "
        "Pastor: \"Familia non est solum sanguis. Familia est amor.\" "
        "Mercator: \"Cum pecunia, tu potes in oppidum ire. "
        "Tu potes uxorem ducere.\" "
        "Pastor: \"Ego iam familiam habeo. Alba est mater. "
        "Nigra est soror. Parva est filia. Oves meae sunt familia mea.\" "
        "Mercator abit. Pastor cum ovibus manet. "
        "Pastor: \"Oves, non omnes vident. Sed ego video. "
        "Et vos videtis. Et hoc est bonum.\" "
        "Oves balant. Sol in monte est. "
        "Pastor et oves in monte sunt — et laeti sunt."
    ),
}

# ============================================================
# Cap.9 — 长篇 (800-1500 words) x2
# ============================================================

STORIES["cap9_10"] = {
    "title_la": "Servus et canis",
    "title_zh": "奴隶与狗",
    "target_chapter": 9,
    "theme": "32 友谊与孤独",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "奴隶",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Servus in villa est. Servus in horto est. "
        "Servus est solus. Servus novus est. Servus ex Graecia venit. "
        "Servus: \"Ego solus sum. In Graecia, familiam habebam. Hic, nihil habeo.\" "
        "Canis in villa est. Canis est parvus. Canis est niger. "
        "Canis solus est. Canis non habet matrem. Canis non habet patrem. "
        "Servus canem videt. Canis servum videt. "
        "Servus: \"Canis, tu quoque solus es?\" "
        "Canis ad servum venit. Canis caudam movet. "
        "Servus canem tangit. Canis manum servi tangit. "
        "Servus: \"Canis, tu es bonus. Tu es amicus.\" "
        "Canis latrat. Canis laetus est. "
        "Servus cani cibum dat. Servus cani aquam dat. "
        "Servus et canis sunt amici. "
        "Servus in horto est. Canis cum servo est. "
        "Servus ambulat. Canis cum servo ambulat. "
        "Servus sedet. Canis cum servo sedet. "
        "Servus: \"Canis, tu es amicus meus. Ego te amo. Et tu me amas.\" "
        "Canis latrat. Canis caudam movet. "
        "Nocte, servus dicit: \"Canis, ego non possum hic esse. "
        "Ego in Graecia liber fui. Hic, ego servus sum. "
        "Ego volo ex hac villa ire.\" "
        "Canis servum spectat. Canis non intellegit. "
        "Servus per noctem e villa exit. Canis eum sequitur. "
        "Servus et canis in silvam currunt. "
        "Viri villae servum vident. "
        "Viri: \"Servus exit! Servus exit!\" "
        "Viri servum sequuntur. Viri canes habent. Canes sunt magni. "
        "Canes magni servum petunt. "
        "Canis parvus inter servum et canes magnos stat. "
        "Canis parvus latrat. Canis parvus canes magnos mordet. "
        "Servus: \"Canis! Canis! Veni!\" "
        "Canis parvus non venit. Canis parvus servum servat. "
        "Viri servum capiunt. Canis parvus in terra est. "
        "Canis parvus non est bonus. "
        "Servus: \"Canis! Amice! Tu es bonus!\" "
        "Servus lacrimat. Servus canem tenet. "
        "Dominus venit. "
        "Dominus: \"Quid est? Cur servus exit? Cur canis in terra est?\" "
        "Servus: \"Domine, ego volui ex villa ire. "
        "Canis me servavit. Canis est bonus. Canis est amicus meus.\" "
        "Dominus servum spectat. Dominus canem spectat. "
        "Dominus: \"Canis est bonus. Canis est fortis. "
        "Tu es servus — sed tu animum habes. "
        "Tu canem amas. Canis te amat. Hoc est bonum.\" "
        "Dominus: \"Ego te non punio. Tu et canis in villa manetis. "
        "Tu et canis amici estis.\" "
        "Servus: \"Gratias, domine.\" "
        "Servus et canis in villa manent. "
        "Servus in horto est. Canis cum servo est. "
        "Servus non est solus. Canis non est solus. "
        "Servus et canis sunt amici. Et hoc est bonum."
    ),
}

STORIES["cap9_11"] = {
    "title_la": "In silvis",
    "title_zh": "在森林中",
    "target_chapter": 9,
    "theme": "11 自然与文明",
    "style": "抒情",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in silvis sum. Silvae sunt magnae. Silvae sunt pulchrae. "
        "Ego per multas terras ii. Ego solus sum. "
        "Nullae viae sunt. Nullae villae sunt. "
        "Arbores sunt. Arbores sunt multae. Arbores sunt magnae. "
        "Ego inter arbores ambulo. Terra est bona. "
        "Aves in arboribus cantant. Ventus venit. "
        "Fluvius parvus in silva est. Aqua est bona. "
        "Ego ad fluvium sedeo. Ego aquam bibo. Ego pedes in aqua pono. "
        "Ego: \"Silvae, vos estis pulchrae. Homines veniunt et abeunt. "
        "Sed vos estis hic.\" "
        "Ego de Roma puto. Roma est longe. "
        "In Roma, multi viri sunt. In Roma, multae viae sunt. "
        "Hic, in silvis, nulli viri sunt. Hic, solus sum. Sed non sum miser. "
        "Ego animal video. Animal est magnum. Animal est pulchrum. "
        "Animal me videt. Animal non timet. Animal me spectat. "
        "Deinde animal abit. "
        "Ego: \"Animal abiit. Sed animal est in corde meo.\" "
        "Ego per silvam ambulo. Ego montem parvum ascendo. "
        "De monte, ego silvam video. Silva est magna. Silva est pulchra. "
        "Ventus super silvam venit. Folia moventur. "
        "Ego in monte sedeo. Ego panem edo. Ego aquam bibo. "
        "Sol cadit. Caelum est rubrum. "
        "Ego: \"In silvis, sol est pulcher. "
        "In oppidis, sol post tecta cadit. Hic, sol inter arbores cadit.\" "
        "Nox venit. Stellae in caelo sunt. "
        "Ego ignem facio. Ignis est calidus. Ignis est bonus. "
        "Ego prope ignem sedeo. Ego ignem specto. "
        "Ego in terra dormio. Caelum est tectum meum. "
        "Stellae sunt lumina mea. "
        "Mane, aves cantant. Sol venit. "
        "Ego: \"Silvae, vos estis bonae. Vos me docuistis. "
        "Vos mihi pacem datis.\" "
        "Ego e silvis exeo. Ego ad oppida redeo. "
        "Sed silvae in me manent. In corde meo, silvae sunt. "
        "Et quando in oppidis sum, ego oculos claudo — et silvas video. "
        "Et silvae mihi bonum dant."
    ),
}

# ============================================================
# TODO: Cap.10 — 33 stories (to be added in next batch)
# ============================================================

# ============================================================
# 评估与输出
# ============================================================

def main():
    os.makedirs(REALITATES_DIR / "Cap9", exist_ok=True)
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