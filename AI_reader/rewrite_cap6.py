#!/usr/bin/env python3
"""rewrite_cap6.py — 重写 Cap.6 的 17 篇短篇为 9中篇 + 5中长篇 + 3长篇。
Cap.6 可用词元 926 个（Cap.1-6 累计），自由模式即可。
验证标准：v2_level ≤ 8 (target_chapter 6 + 2)
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
# 中篇 (300-500词) x9
# ============================================================

STORIES["cap6_01"] = {
    "title_la": "Sicilia et Sardinia",
    "title_zh": "西西里与撒丁",
    "target_chapter": 6,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Sicilia, Sardinia, Corsica. Trēs īnsulae in marī sunt. Trēs īnsulae in imperiō Rōmānō sunt. "
        "Trēs īnsulae prope Ītaliam sunt. "
        "Sicilia est īnsula magna. Sicilia est īnsula pulchra. Sicilia multa oppida habet. "
        "In Siciliā multī virī habitant. In Siciliā multae fēminae habitant. "
        "In Siciliā vīta bona est. In Siciliā cibus bonus est. In Siciliā vīnum bonum est. "
        "Sicilia est prōvincia Rōmāna. Sicilia est in imperiō. Sicilia Rōmae pāret. "
        "Sardinia est īnsula. Sardinia nōn est tam magna quam Sicilia. "
        "Sed Sardinia quoque pulchra est. Sardinia quoque multa oppida habet. "
        "In Sardiniā virī fortēs habitant. In Sardiniā fēminae pulchrae habitant. "
        "Sardinia est prōvincia Rōmāna. Sardinia est in imperiō. Sardinia Rōmae pāret. "
        "Corsica est īnsula parva. Corsica nōn est magna. Corsica nōn multa oppida habet. "
        "Sed Corsica est pulchra. Corsica montēs altōs habet. Corsica silvās magnās habet. "
        "Corsica est prōvincia Rōmāna. Corsica quoque in imperiō est. Corsica quoque Rōmae pāret. "
        "Trēs īnsulae — Sicilia, Sardinia, Corsica — sunt in marī. Sunt prope Ītaliam. "
        "Sunt in imperiō. Sunt Rōmānae. "
        "Sī vir Rōmānus ad Siciliam īre vult, nāvigāre dēbet. "
        "Sī vir Rōmānus ad Sardiniam īre vult, nāvigāre dēbet. "
        "Sī vir Rōmānus ad Corsicam īre vult, nāvigāre dēbet. "
        "Mare inter Ītaliam et īnsulās est. Mare est magnum. Mare est caeruleum. "
        "In marī multī piscēs sunt. Nāvēs in marī sunt. "
        "Nāvēs ā Siciliā ad Ōstiam veniunt. Nāvēs frūmentum portant. "
        "Nāvēs vinum portant. Nāvēs oleum portant. "
        "Sicilia est terra frūmentī. Sicilia est terra vīnī. Sicilia est terra oleī. "
        "Sardinia est terra frūmentī quoque. Sardinia est terra vestium. "
        "Corsica est terra lignī. Corsica est terra nāvium. "
        "Trēs īnsulae. Trēs prōvinciae. Trēs terrae in marī. "
        "Sicilia est magna et pulchra. Sardinia est magna et fortis. Corsica est parva et aspera. "
        "Sed omnēs trēs sunt Rōmānae. Omnēs trēs in imperiō sunt. Omnēs trēs Rōmae pārent."
    )
}

STORIES["cap6_02"] = {
    "title_la": "Tria oppida magnae",
    "title_zh": "三座大城",
    "target_chapter": 6,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma, Brundisium, Tusculum. Tria oppida in Ītaliā sunt. "
        "Rōma est caput imperiī. Rōma est oppidum magnum. Rōma est oppidum antīquum. "
        "In Rōmā multī virī habitant. In Rōmā multae fēminae habitant. "
        "In Rōmā multī puerī et multae puellae habitant. "
        "Rōma est in septem montibus. Montēs Rōmānī sunt: Palātīnus, Capitōlīnus, Aventīnus. "
        "In Rōmā magnum forum est. In forō virī verba faciunt. In forō mercēs vēnduntur. "
        "In Rōmā magnum Circum Maximum est. In Circō Maximō equī currunt. Virī spectant. "
        "Rōma est pulchra. Rōma est magna. Rōma est caput mundī. "
        "Brundisium est oppidum ad mare. Brundisium est porta Ītaliae. "
        "Ā Brundisiō nāvēs ad Graeciam nāvigant. Ā Brundisiō nāvēs ad Asiam nāvigant. "
        "Ā Brundisiō nāvēs ad Africam nāvigant. "
        "Brundisium est oppidum magnum — sed nōn tam magnum quam Rōma. "
        "In Brundisiō multī virī adveniunt. In Brundisiō multī virī abeunt. "
        "Brundisium est oppidum viārum. Brundisium est oppidum nāvium. "
        "Via Appia ā Rōmā ad Brundisium dūcit. Via Appia est via longa. Via Appia est via Rōmāna. "
        "Tusculum est oppidum parvum. Tusculum est prope Rōmam. "
        "Tusculum in monte est. Ā Tusculō Rōma vidērī potest. "
        "In Tusculō virī dīvitēs habitant. In Tusculō vīllae pulchrae sunt. "
        "Ā Tusculō Rōma nōn longē abest. Vir ā Tusculō Rōmam ūnō diē ambulāre potest. "
        "Tusculum est oppidum quiētum. Tusculum nōn est turbidum. "
        "In Tusculō virī in hortīs sedent. In Tusculō fēminae in hortīs cantant. "
        "Tria oppida — Rōma, Brundisium, Tusculum — tria in Ītaliā. "
        "Rōma est caput. Brundisium est porta. Tusculum est quiēs. "
        "Tria oppida. Trēs vitae. Ūna Ītalia."
    )
}

STORIES["cap6_03"] = {
    "title_la": "Sex oppida Rōmāna",
    "title_zh": "罗马六城",
    "target_chapter": 6,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma, Brundisium, Tusculum, Capua, Neapolis, Tarentum. Sex oppida in Ītaliā sunt. "
        "Rōma est caput. Rōma est in mediā Ītaliā. Rōma est magna et antīqua. "
        "In Rōmā senātus est. In Rōmā imperātor est. In Rōmā populus Rōmānus est. "
        "Brundisium est ad mare. Brundisium est in Ītaliā merīdiānā. "
        "Ā Brundisiō viae ad orientem dūcunt. Ā Brundisiō nāvēs ad Graeciam nāvigant. "
        "Brundisium est porta maris. "
        "Tusculum est in monte. Tusculum est prope Rōmam. "
        "Tusculum est parvum sed pulchrum. Ā Tusculō Rōma vidērī potest. "
        "Capua est in Campāniā. Capua est oppidum magnum. Capua est post Rōmam secundum oppidum Ītaliae. "
        "In Capuā multī virī habitant. In Capuā multae viae sunt. "
        "Capua est dīves. Capua est pulchra. Capua est Campāniae caput. "
        "Neapolis est in Campāniā quoque. Neapolis est ad mare. "
        "Neapolis est oppidum Graecum. In Neāpolī multī Graecī habitant. "
        "Neapolis est pulchra. Neapolis est ad mare. Ā Neāpolī Vesuvius mōns vidērī potest. "
        "Tarentum est in Ītaliā merīdiānā. Tarentum est ad mare. "
        "Tarentum est oppidum Graecum. Tarentum est antīquum. "
        "Tarentum ā Graecīs conditum est. In Tarentō multī Graecī habitant. "
        "Sex oppida. Omnia in Ītaliā. Omnia in imperiō Rōmānō. "
        "Rōma est in Latiō. Tusculum est in Latiō. "
        "Capua est in Campāniā. Neapolis est in Campāniā. "
        "Brundisium est in Calabriā. Tarentum est in Calabriā. "
        "Sex oppida in tribus regiōnibus. Trēs regiōnēs in ūnā Ītaliā. "
        "Et omnēs sex Rōmānae sunt. Omnēs sex Rōmae pārent."
    )
}

STORIES["cap6_04"] = {
    "title_la": "Sicilia et Corsica",
    "title_zh": "西西里与科西嘉",
    "target_chapter": 6,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Sicilia, Corsica, Sardinia. Trēs īnsulae in marī sunt. "
        "Sicilia in marī est. Corsica in marī est. Sardinia in marī est. "
        "Sicilia est magna. Corsica est parva. Sardinia est mediā. "
        "Sicilia est prope Ītaliam. Sicilia est prope Āfricam. "
        "Sicilia inter Ītaliam et Āfricam est. Sicilia est pōns inter Eurōpam et Āfricam. "
        "In Siciliā Graecī antīquī habitābant. In Siciliā templa Graeca sunt. "
        "In Siciliā Carthāginiēnsēs habitābant. In Siciliā Rōmānī nunc habitant. "
        "Sicilia multōs populōs vidit. Sicilia multās linguās audīvit. "
        "Sicilia est īnsula populōrum. Sicilia est īnsula historiārum. "
        "Corsica est īnsula parva. Corsica est in marī Ligusticō. "
        "Corsica montēs altōs habet. Corsica silvās magnās habet. "
        "In Corsicā paucī virī habitant. Corsica nōn est dīves. "
        "Sed Corsica est pulchra. Corsica est ferōx. Corsica est lībera. "
        "Corsica nōn facile Rōmae pāret. Corsicī fortēs sunt. "
        "Sardinia est inter Siciliam et Corsicam. Sardinia nōn est tam magna quam Sicilia. "
        "Sardinia nōn est tam parva quam Corsica. Sardinia est mediā. "
        "In Sardiniā virī fortēs habitant. In Sardiniā montēs sunt. "
        "Sardinia est prōvincia Rōmāna. Sardinia frūmentum mittit. "
        "Trēs īnsulae. Trēs prōvinciae. Trēs terrae in marī. "
        "Sicilia est magna et antīqua. Corsica est parva et ferōx. Sardinia est mediā et fortis. "
        "Et omnēs trēs Rōmānae sunt."
    )
}

STORIES["cap6_05"] = {
    "title_la": "Quattuor oppida",
    "title_zh": "四座城",
    "target_chapter": 6,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma, Brundisium, Capua, Neapolis. Quattuor oppida in Ītaliā sunt. "
        "Rōma est caput. Rōma est primum oppidum. Rōma est in septem montibus. "
        "In Rōmā populus magnus habitat. In Rōmā viae magnae sunt. "
        "In Rōmā templa pulchra sunt. In Rōmā forum magnum est. "
        "Rōma est caput mundī. Rōma est urbs aeterna. "
        "Brundisium est in Ītaliā merīdiānā. Brundisium est ad mare. "
        "Brundisium est porta. Ā Brundisiō viae ad orientem dūcunt. "
        "Brundisium est oppidum maris. Brundisium est oppidum nāvium. "
        "Multī virī per Brundisium iter faciunt. Multī mercātōrēs per Brundisium nāvigant. "
        "Capua est in Campāniā. Capua est post Rōmam secundum oppidum. "
        "Capua est dīves. Capua est pulchra. In Capuā multī virī dīvitēs habitant. "
        "Capua nōn est caput — sed Capua est magna. Capua est superba. "
        "Capua Rōmam spectat. Capua Rōmae invidet. "
        "Neapolis est in Campāniā quoque. Neapolis est ad mare. "
        "Neapolis est Graeca. Ā Graecīs condita est. "
        "In Neāpolī Graecī habitant. In Neāpolī lingua Graeca audītur. "
        "Neapolis est pulchra. Neapolis ad mare est. "
        "Ā Neāpolī Vesuvius mōns vidētur. Vesuvius mōns magnus est. "
        "Quattuor oppida. Rōma est caput. Brundisium est porta. Capua est dīves. Neapolis est Graeca. "
        "Quattuor oppida in ūnā Ītaliā. Quattuor oppida in ūnō imperiō."
    )
}

STORIES["cap6_06"] = {
    "title_la": "Octō flūmina",
    "title_zh": "八条河",
    "target_chapter": 6,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tiberis, Rhēnus, Dānuvius, Nīlus, Rhodanus, Dūrius, Padus, Arar. Octō flūmina sunt. "
        "Tiberis in Ītaliā est. Tiberis per Rōmam fluit. Tiberis est flūmen Rōmānum. "
        "Tiberis nōn est magnus — sed Tiberis est sacr. Rōma ad Tiberim est. "
        "Tiberis aquam ad Rōmam portat. Tiberis nāvēs ad Rōmam portat. "
        "Rhēnus est in Germāniā. Rhēnus est flūmen magnum. Rhēnus est līmes imperiī. "
        "Rhēnus inter Germāniam et Galliam fluit. Rhēnus Rōmānōs ā Germānīs dīvidit. "
        "Rhēnus longus est. Rhēnus lātus est. Rhēnus fortis est. "
        "Dānuvius est flūmen magnum. Dānuvius per multās terrās fluit. "
        "Dānuvius per Germāniam fluit. Dānuvius per Pannoniam fluit. Dānuvius per Daciam fluit. "
        "Dānuvius est longus. Dānuvius est lātus. Dānuvius est flūmen imperiī. "
        "Nīlus est in Aegyptō. Nīlus est flūmen longissimum. "
        "Nīlus per Aegyptum fluit. Nīlus aquam ad Aegyptum portat. "
        "Nīlus Aegyptō vītam dat. Sine Nīlō Aegyptus nōn est. "
        "Rhodanus est in Galliā. Rhodanus est flūmen magnum. Rhodanus ad mare fluit. "
        "Padus est in Ītaliā. Padus est flūmen magnum. Padus in Ītaliā septentriōnālī est. "
        "Dūrius est in Hispāniā. Dūrius est flūmen magnum. Dūrius ad mare fluit. "
        "Arar est in Galliā. Arar est flūmen lentum. Arar lentē fluit. "
        "Octō flūmina. Octō aquae. Octō viae per terrās. "
        "Flūmina sunt viae aquārum. Flūmina sunt vītae imperiī."
    )
}

STORIES["cap6_07"] = {
    "title_la": "Quīnque flūmina Eurōpae",
    "title_zh": "欧洲五河",
    "target_chapter": 6,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tiberis, Padus, Rhēnus, Dānuvius, Rhodanus. Quīnque flūmina in Eurōpā sunt. "
        "Tiberis est in Ītaliā. Tiberis est flūmen Rōmānum. Tiberis per Rōmam fluit. "
        "Tiberis nōn est longus — sed Tiberis est magnus. Tiberis Rōmam alit. "
        "Padus est in Ītaliā septentriōnālī. Padus est flūmen magnum. Padus est longus. "
        "Padus per Campōs Padānōs fluit. Padus aquam multam ad mare portat. "
        "Padus est flūmen Ītaliae septentriōnālis. "
        "Rhēnus est in Germāniā et Galliā. Rhēnus est flūmen longum et lātum. "
        "Rhēnus est līmes imperiī. Rhēnus Rōmānōs ā Germānīs dīvidit. "
        "Ad Rhēnum castella Rōmāna sunt. Ad Rhēnum mīlitēs Rōmānī stant. "
        "Dānuvius est flūmen longissimum Eurōpae. Dānuvius per multās terrās fluit. "
        "Dānuvius ā Germāniā ad Pontum Euxīnum fluit. "
        "Dānuvius est via aquae. Dānuvius est via commerciī. "
        "Rhodanus est in Galliā. Rhodanus ad mare Internum fluit. "
        "Rhodanus est flūmen magnum. Rhodanus est via inter Galliam et mare. "
        "Quīnque flūmina. Quīnque aquae. Quīnque viae per Eurōpam. "
        "Tiberis est parvus sed Rōmānus. Padus est magnus et Ītalicus. "
        "Rhēnus est līmes. Dānuvius est longus. Rhodanus est Gallicus. "
        "Quīnque flūmina in ūnā Eurōpā. Quīnque flūmina in ūnō imperiō."
    )
}

STORIES["cap6_08"] = {
    "title_la": "Trēs viae Rōmānae",
    "title_zh": "罗马三道",
    "target_chapter": 6,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Via Appia, Via Flāminia, Via Aurēlia. Trēs viae Rōmānae sunt. "
        "Via Appia est inter Rōmam et Brundisium. Via Appia est via longa. Via Appia est rēgīna viārum. "
        "Via Appia ā Rōmā ad Capuam dūcit. Deinde ad Brundisium dūcit. "
        "Via Appia est antīqua. Via Appia est lapidibus strāta. "
        "In Viā Appiā multī virī ambulant. In Viā Appiā multī equī currunt. "
        "In Viā Appiā mercātōrēs mercēs portant. In Viā Appiā mīlitēs ad orientem eunt. "
        "Via Appia est via imperiī. Via Appia est via victōriae. "
        "Via Flāminia est inter Rōmam et Arīminum. Via Flāminia est via longa. "
        "Via Flāminia ā Rōmā ad septentriōnem dūcit. "
        "Via Flāminia per Umbriam dūcit. Via Flāminia per Appennīnōs montēs dūcit. "
        "Via Flāminia est via ad Galliam. Via Flāminia est via ad Germāniam. "
        "Via Aurēlia est inter Rōmam et Pīsās. Via Aurēlia est via ad mare. "
        "Via Aurēlia per Etrūriam dūcit. Via Aurēlia prope mare est. "
        "In Viā Aurēliā mare vidērī potest. In Viā Aurēliā ventus maris sentīrī potest. "
        "Via Aurēlia est via ad Galliam merīdiānam. Via Aurēlia est via ad Hispāniam. "
        "Trēs viae. Trēs itinera. Trēs viae ā Rōmā ad terrās longinquās. "
        "Via Appia ad orientem. Via Flāminia ad septentriōnem. Via Aurēlia ad occidentem. "
        "Omnēs viae Rōmam dūcunt — et omnēs viae ā Rōmā incipiunt."
    )
}

STORIES["cap6_09"] = {
    "title_la": "Duae īnsulae magnae",
    "title_zh": "两座大岛",
    "target_chapter": 6,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Sicilia et Sardinia. Duae īnsulae magnae in marī sunt. "
        "Sicilia est īnsula magna. Sicilia est prope Ītaliam. Sicilia est prope Āfricam. "
        "Sicilia est in marī Internō. Sicilia est inter Ītaliam et Āfricam. "
        "Sicilia est īnsula frūmentī. Sicilia est īnsula vīnī. Sicilia est īnsula oleī. "
        "In Siciliā Graecī antīquī urbēs condidērunt. In Siciliā templa Graeca sunt. "
        "In Siciliā nunc Rōmānī habitant. Sicilia est prōvincia Rōmāna. "
        "Sardinia est īnsula magna. Sardinia est in marī Tyrrhēnō. "
        "Sardinia nōn est tam magna quam Sicilia — sed Sardinia quoque magna est. "
        "Sardinia montēs altōs habet. Sardinia silvās magnās habet. "
        "In Sardiniā virī fortēs habitant. Sardī fortēs sunt. Sardī līberī esse volunt. "
        "Sardinia est prōvincia Rōmāna. Sardinia frūmentum mittit. Sardinia metalla mittit. "
        "Duae īnsulae — Sicilia et Sardinia — sunt in marī. Sunt prope Ītaliam. "
        "Sicilia est Graeca et Rōmāna. Sardinia est ferōx et Rōmāna. "
        "Sicilia ad meridiem est. Sardinia ad occidentem est. "
        "Duae īnsulae. Duae prōvinciae. Duae terrae in marī. "
        "Et ambae Rōmānae sunt. Ambae Rōmae pārent."
    )
}

# ============================================================
# 中长篇 (500-800词) x5
# ============================================================

STORIES["cap6_10"] = {
    "title_la": "Puella in viā",
    "title_zh": "路上的女孩",
    "target_chapter": 6,
    "theme": "13 孤独",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puella in viā est. Via est longa. Via est inter oppida. "
        "Puella est sōla. Puella nōn magnum oppidum quaerit. Puella parvum oppidum quaerit. "
        "Puella per viam ambulat. Puella nōn currit. Puella lentē ambulat. "
        "Puella sōl in caelō videt. Sōl est magnus et calidus. "
        "Puella arborēs in viā videt. Arborēs sunt magnae et viridēs. "
        "Puella avēs in caelō audit. Avēs cantant. "
        "Puella ad fontem venit. Aqua in fonte est. Aqua est clāra et frigida. "
        "Puella aquam bibit. Puella in aquā faciem suam videt. "
        "Puella: 'Quis est haec puella in aquā? Ego sum. Ego puella sum. "
        "Sed cūr ego sōla sum? Cūr nūllus mēcum est?' "
        "Puella plōrat. Lacrimae in aquam cadunt. "
        "Sed puella iterum surgit. Puella iterum per viam ambulat. "
        "Puella: 'Ego nōn dēbeō plōrāre. Ego fortis sum. Ego ad oppidum veniam.' "
        "Subitō puella virum in viā videt. Vir est senex. Vir est benignus. "
        "Senex: 'Puella, cūr sōla in viā es? Ubi est pater tuus? Ubi est māter tua?' "
        "Puella: 'Pater meus mortuus est. Māter mea mortua est. Ego sōla sum.' "
        "Senex: 'Nōn dēbēs sōla esse. Venī mēcum. Ego tē ad oppidum dūcam.' "
        "Puella cum sene per viam ambulat. Senex puellae dē oppidō nārrat. "
        "Senex: 'In oppidō multī virī bonī sunt. In oppidō multae fēminae bonae sunt. "
        "Tū in oppidō familiam novam invenīre potes.' "
        "Puella: 'Ego familiam nōn habeō. Ego sōla sum.' "
        "Senex: 'Familia nōn sōlum sanguine est. Familia est ubi tū amāris. "
        "In oppidō tū amāberis.' "
        "Puella et senex ad oppidum veniunt. Oppidum est parvum sed pulchrum. "
        "In oppidō fēmina eōs videt. Fēmina est benigna. "
        "Fēmina: 'Quis est haec puella?' "
        "Senex: 'Haec puella sōla est. Parentēs eius mortuī sunt.' "
        "Fēmina: 'Puella, venī in domum meam. Ego tibi cibum dō. Ego tibi aquam dō. "
        "Ego tibi lectum dō.' "
        "Puella fēminam spectat. Puella lacrimās habet — sed nōn plōrat. "
        "Puella: 'Grātiās tibi agō. Ego nōn iam sōla sum.' "
        "Puella in oppidō manet. Puella in oppidō novam vītam incipit. "
        "Puella nōn iam sōla est. Puella familiam invēnit."
    )
}

STORIES["cap6_11"] = {
    "title_la": "Sōlus in viā",
    "title_zh": "独行路上",
    "target_chapter": 6,
    "theme": "13 孤独",
    "style": "抒情",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in viā sum. Via est longa. Ego sōlus sum. "
        "Nūllus vir in viā est. Nūlla fēmina in viā est. Ego in viā sōlus ambulō. "
        "Sōl in caelō est. Sōl est magnus. Sōl mē calefacit. "
        "Ventus per arbōrēs flat. Ventus est frigidus. Ventus mē tangit. "
        "Ego in viā multa audiō. Avēs in arbōribus cantant. "
        "Aqua in fluviō fluit. Ventus in arbōribus flat. "
        "Ego in viā multa videō. Montēs procul sunt. Montēs sunt magnī et altī. "
        "Nūbēs in caelō sunt. Nūbēs sunt albae. Nūbēs lentē moventur. "
        "Ego in viā multa cōgitō. Cūr ego sōlus sum? Cūr ego in viā sum? "
        "Cūr ego ad oppidum eō? Quid ego in oppidō quaerō? "
        "Ego in viā dē vītā cōgitō. Vīta est via. Vīta est longa. "
        "In viā vītae multī virī sunt. In viā vītae multae fēminae sunt. "
        "Sed ego sōlus sum. Ego in viā vītae sōlus ambulō. "
        "Estne hoc bonum — an malum? Sōlus esse — estne hoc bonum? "
        "Sī sōlus sum, nēmō mē videt. Sī sōlus sum, nēmō mē audit. "
        "Sī sōlus sum, nēmō mē iūdicat. Sī sōlus sum, līber sum. "
        "Sed sī sōlus sum, nēmō mē amat. Sī sōlus sum, nēmō mēcum est. "
        "Sōlus esse — estne hoc lībertās — an poena? "
        "Ego in viā subitō virum videō. Vir est senex. Vir in viā sedet. "
        "Senex: 'Quō vādis, iuvenis?' "
        "Ego: 'Ad oppidum eō. Ego in oppidō novam vītam quaerō.' "
        "Senex: 'Cūr sōlus es?' "
        "Ego: 'Nēmō mēcum est. Nēmō mē amat. Ego sōlus sum.' "
        "Senex: 'Sōlus nōn es. Ego tē videō. Ego tēcum loquor. "
        "Via tēcum est. Sōl tēcum est. Ventus tēcum est. "
        "Sōlus nōn es — sī oculōs aperīs et vidēs.' "
        "Ego senem spectō. Ego caelum spectō. Ego viam spectō. "
        "Senex vēra dīcit. Ego sōlus nōn sum. "
        "Ego iterum per viam ambulō. Sed nōn iam sōlus sum."
    )
}

STORIES["cap6_12"] = {
    "title_la": "Oppidum in nocte",
    "title_zh": "夜之城",
    "target_chapter": 6,
    "theme": "35 城市",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "旅人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Oppidum in nocte est. Nox est magna. Nox est ātra. "
        "In oppidō nūllī virī sunt. Nūllae fēminae in oppidō sunt. "
        "Oppidum est vacuum. Oppidum est mortuum. "
        "Lūna in caelō est. Lūna est magna et clāra. Lūna oppidum lūce suā tangit. "
        "Stēllae in caelō sunt. Stēllae sunt multae. Stēllae sunt parvae — sed pulchrae. "
        "Via in oppidō est. Via est vacua. Via est longa. "
        "In viā nēmō ambulat. In viā nēmō stat. In viā nēmō sedet. "
        "Domūs in oppidō sunt. Domūs sunt magnae. Domūs sunt clausae. "
        "In domibus nūlla lūx est. In domibus nūllus sonus est. "
        "Fenestrae sunt clausae. Portae sunt clausae. "
        "Subitō — sonus. Sonus in viā est. Sonus pedum est. "
        "Vir per viam ambulat. Vir est sōlus. Vir est in palliō. "
        "Vir nōn timet. Vir in nocte ambulat. Vir oppidum in nocte videt. "
        "Vir: 'Oppidum in nocte est aliud oppidum. Oppidum in nocte est vērum oppidum. "
        "In diē oppidum est turbidum. In diē oppidum est plēnum. "
        "In nocte oppidum est vacuum. In nocte oppidum est quiētum. "
        "In nocte oppidum sē ipsum videt. In nocte oppidum sē ipsum audit.' "
        "Vir per forum ambulat. Forum est vacuum. "
        "In forō in diē multī virī sunt. In forō in diē multae vōcēs sunt. "
        "In forō in nocte nūllus est. In forō in nocte silentium est. "
        "Vir: 'Hīc in diē mercātōrēs clāmant. Hīc in diē puerī rīdent. "
        "Hīc in diē fēminae loquuntur. Nunc — silentium. "
        "Ubi sunt omnēs? Ubi sunt vōcēs? Ubi est vīta?' "
        "Vir ad templum ambulat. Templum est magnum. Templum est album. "
        "In templō in nocte nūlla lūx est. Sed deus in templō est. "
        "Vir: 'Deus in templō est — etiam in nocte. Deus videt — etiam in tenebrīs.' "
        "Vir ad portam oppidī ambulat. Porta est clausa. "
        "Vir portam tangit. Vir: 'Porta est clausa — sed ego intrāvī. "
        "Oppidum in nocte est apertum — sī tū sōlus es.' "
        "Vir per portam exit. Vir in viam exit. "
        "Oppidum post eum manet. Oppidum in nocte. Oppidum vacuum. Oppidum vērum."
    )
}

STORIES["cap6_13"] = {
    "title_la": "Dominus bonus",
    "title_zh": "好主人",
    "target_chapter": 6,
    "theme": "06 权力",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Dominus in oppidō est. Dominus est Lūcius. Lūcius est vir dīves. Lūcius est vir bonus. "
        "Lūcius multōs servōs habet. Lūcius decem servōs habet. Lūcius vīgintī servōs habet. "
        "Servī Lūcium amant — nōn quia dominus est, sed quia bonus est. "
        "Lūcius servīs cibum dat. Lūcius servīs vestem dat. Lūcius servīs lībertātem prōmittit. "
        "Ūnus servus Lūciī est Dāvus. Dāvus est Graecus. Dāvus est servus bonus. "
        "Dāvus Lūcium amat. Dāvus Lūciō fidēlis est. "
        "Dāvus: 'Dominus meus est bonus. Dominus meus mē nōn verberat. "
        "Dominus meus mē nōn vincit. Dominus meus mē ut hominem videt.' "
        "Alius servus est Syrus. Syrus est Syrus. Syrus est servus novus. "
        "Syrus nōn Lūcium amat. Syrus līber esse vult. Syrus fugere vult. "
        "Syrus: 'Cūr ego servus sum? Cūr Lūcius est dominus? "
        "Nōn est iūstum. Ego līber esse volō.' "
        "Nocte Syrus fugit. Syrus ex oppidō exit. Syrus in viā est. "
        "Sed Syrus nōn longē it. Syrus in silvā est. Syrus sōlus in silvā est. "
        "Syrus timet. Syrus: 'Ubi sum? Ego in silvā sum. Nūllus mē videt. "
        "Ego nōn habeō cibum. Ego nōn habeō aquam. Ego sōlus sum. "
        "Dominus meus mihi cibum dedit. Dominus meus mihi aquam dedit. "
        "Nunc ego — quid habeō? Nihil.' "
        "Māne Lūcius Syrum nōn videt. Lūcius: 'Ubi est Syrus?' "
        "Dāvus: 'Dominus, Syrus fūgit. Syrus līber esse vult.' "
        "Lūcius: 'Syrus stultus est. Syrus mē nōn intellegit. "
        "Ego eī lībertātem dare voluī. Ego eī post decem annōs lībertātem dare voluī. "
        "Nunc Syrus in silvā est — sōlus, sine cibō, sine aquā.' "
        "Lūcius servōs mittit. Lūcius: 'Quaerite Syrum! Eum ad mē addūcite!' "
        "Servī Syrum in silvā inveniunt. Syrus est fessus. Syrus est timidus. "
        "Servī Syrum ad Lūcium addūcunt. "
        "Lūcius Syrum videt. Lūcius: 'Syre, cūr fūgistī? Cūr mē nōn rogāvistī?' "
        "Syrus: 'Domine, ego līber esse voluī. Ego servus esse nōn voluī.' "
        "Lūcius: 'Ego tē intellegō. Ego tē nōn puniō. "
        "Sed tū mē rogāre dēbēs — nōn fugere. "
        "Sī tū mē rogāvissēs, ego tibi lībertātem dedissem. "
        "Nunc tū exspectābis. Post quīnque annōs līber eris.' "
        "Syrus lacrimat. Syrus: 'Domine, tū bonus es. Ego stultus fuī. "
        "Ego tē nōn intellēxī. Nunc ego tē intellegō.' "
        "Lūcius Syrō ignōscit. Dominus bonus est. Servus discit. "
        "Post quīnque annōs Syrus līber est. Syrus Lūciō grātiās agit."
    )
}

STORIES["cap6_14"] = {
    "title_la": "Via ad Graeciam",
    "title_zh": "通往希腊之路",
    "target_chapter": 6,
    "theme": "22 旅程",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir Graecus in oppidō est. Oppidum est Rōma. Vir ad Graeciam īre vult. "
        "Vir est Aristotelēs. Aristotelēs est Graecus. Aristotelēs est philosophus. "
        "Aristotelēs in Rōmā multōs annōs habitāvit. Aristotelēs Rōmam amat. "
        "Sed Aristotelēs Graeciam quoque amat. Aristotelēs patriam suam vidēre vult. "
        "Aristotelēs: 'Rōma est magna et pulchra. Sed Graecia est patria mea. "
        "In Graeciā nātus sum. In Graeciā parentēs meī sunt. "
        "Ego ad Graeciam īre dēbeō.' "
        "Aristotelēs per viam ambulat. Via est longa. "
        "Via ā Rōmā ad Brundisium dūcit. Via Appia est. "
        "Aristotelēs: 'Via Appia est rēgīna viārum. Via Appia mē ā Rōmā ad mare dūcet.' "
        "In viā Aristotelēs multa videt. Aristotelēs oppida videt. "
        "Aristotelēs Ariciam videt. Aristotelēs Forum Appiī videt. "
        "Aristotelēs Tarracīnam videt. Aristotelēs Capuam videt. "
        "In viā Aristotelēs multōs virōs videt. Mercātōrēs cum mercibus. "
        "Mīlitēs cum armīs. Agricolae cum frūmentō. "
        "Aristotelēs cum illīs loquitur. Aristotelēs: 'Quō vādis? Unde venīs?' "
        "Mercātor: 'Ego ad Brundisium eō. Ego mercēs ad Graeciam portō.' "
        "Mīles: 'Ego ad orientem eō. Ego in legiōne pugnō.' "
        "Agricola: 'Ego ad oppidum eō. Ego frūmentum vēndō.' "
        "Aristotelēs: 'Omnēs iter faciunt. Omnēs viam habent. "
        "Via est commūnis — sed quisque suum iter habet.' "
        "Aristotelēs ad Brundisium venit. Brundisium est ad mare. "
        "In Brundisiō nāvēs sunt. Nāvēs ad Graeciam nāvigant. "
        "Aristotelēs nāvem invenit. Nāvis est magna. Nāvis ad Graeciam nāvigat. "
        "Aristotelēs in nāvem ascendit. Nāvis ā Brundisiō nāvigat. "
        "Aristotelēs in nāvī stat. Aristotelēs mare videt. "
        "Aristotelēs: 'Mare est magnum. Mare est pulchrum. "
        "Mare mē ad Graeciam portat. Mare mē ad patriam portat.' "
        "Nāvis ad Graeciam nāvigat. Aristotelēs Graeciam videt. "
        "Aristotelēs: 'Graecia! Patria mea! Tandem tē videō!' "
        "Aristotelēs in Graeciam redit. Aristotelēs domum redit. "
        "Via longa est — sed via ad patriam semper brevis est."
    )
}

# ============================================================
# 长篇 (800-1500词) x3
# ============================================================

STORIES["cap6_15"] = {
    "title_la": "Pater et Fīlius",
    "title_zh": "父与子",
    "target_chapter": 6,
    "theme": "30 威严与慈爱",
    "style": "精炼",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Pater: 'Fīlī, venī.' "
        "Fīlius: 'Pater, cūr mē vocās?' "
        "Pater: 'Tū es puer bonus. Ego tē amō.' "
        "Fīlius: 'Ego quoque tē amō, pater.' "
        "Pater: 'Fīlī, tū iam nōn parvus es. Tū iam duodecim annōs habēs. "
        "Tempus est tē discere. Tempus est tē virum fierī.' "
        "Fīlius: 'Quid ego discere dēbeō, pater?' "
        "Pater: 'Multa. Tū dēbēs discere legere et scrībere. "
        "Tū dēbēs discere dē dīs et deābus. Tū dēbēs discere dē Rōmā et imperiō. "
        "Tū dēbēs discere quid est bonum et quid est malum. "
        "Tū dēbēs discere quid est iūstum et quid est iniūstum.' "
        "Fīlius: 'Pater, haec multa sunt. Ego omnia discere nōn possum.' "
        "Pater: 'Tū omnia discere potes. Nōn ūnō diē — sed multīs diēbus. "
        "Ego tibi magister erō. Ego tē docēbō.' "
        "Fīlius: 'Grātiās, pater. Ego discere volō. Ego vir bonus fierī volō.' "
        "Pater fīlium in hortum dūcit. Hortus est magnus et pulcher. "
        "In hortō rosae sunt. In hortō līlia sunt. In hortō aqua est. "
        "Pater: 'Fīlī, vidē hortum. Hortus est pulcher. Sed hortus labōrem postulat. "
        "Sī hortum nōn cūrās, rosae nōn flōrent. Sī hortum nōn cūrās, aqua nōn fluit. "
        "Vīta tua est sīcut hortus. Sī vītam tuam nōn cūrās, nōn flōrēbit. "
        "Sī vītam tuam cūrās, pulchra erit.' "
        "Fīlius: 'Quōmodo vītam meam cūrāre possum, pater?' "
        "Pater: 'Cum sapientiā. Cum iūstitiā. Cum fortitūdine. Cum temperantiā. "
        "Hae sunt quattuor virtūtēs. Sī hās virtūtēs habēs, vīta tua flōrēbit.' "
        "Fīlius: 'Quid est sapientia, pater?' "
        "Pater: 'Sapientia est scīre quid est bonum et quid est malum. "
        "Sapientia est scīre quid facere dēbeās et quid nōn facere dēbeās.' "
        "Fīlius: 'Quid est iūstitia?' "
        "Pater: 'Iūstitia est dare cuique suum. Iūstitia est nōn nocēre. "
        "Iūstitia est omnēs hominēs aequē tractāre.' "
        "Fīlius: 'Quid est fortitūdō?' "
        "Pater: 'Fortitūdō est nōn timēre. Fortitūdō est stāre — etiam quandō timēs. "
        "Fortitūdō est facere quod rēctum est — etiam quandō difficile est.' "
        "Fīlius: 'Quid est temperantia?' "
        "Pater: 'Temperantia est moderārī. Temperantia est nōn nimium cupere. "
        "Temperantia est scīre quandō satis est.' "
        "Fīlius: 'Ego hās virtūtēs discere volō, pater. Sed difficile est.' "
        "Pater: 'Difficile est — sed tū potes. Ego tē iuvābō. "
        "Et nōn sōlum ego. Omnēs bonī virī tē iuvābunt. "
        "Rōma ipsa tē docēbit. Rōma est magistra vītae.' "
        "Fīlius: 'Pater, ego tē amō. Ego tibi grātiās agō.' "
        "Pater: 'Et ego tē amō, fīlī. Et ego tibi grātiās agō — "
        "quia tū mē patrem fēcistī. Antequam tū nātus es, ego vir eram. "
        "Postquam tū nātus es, ego pater factus sum. "
        "Tū mē maiōrem fēcistī. Tū mē meliōrem fēcistī.' "
        "Pater et fīlius in hortō sedent. Sōl occidit. Caelum est rubrum. "
        "Pater: 'Fīlī, vidē sōlem. Sōl occidit. Sed crās iterum oriētur. "
        "Sīcut sōl, vīta quoque occidit et oritur. "
        "Hodiē tū puer es. Crās vir eris. Postrīdiē pater eris. "
        "Tuus fīlius quoque discet. Tuus fīlius quoque quaeret. "
        "Et tū eī dīcēs quod ego tibi hodiē dīxī.' "
        "Fīlius: 'Pater, ego tē numquam oblivīscar.' "
        "Pater: 'Et ego tē numquam oblivīscar, fīlī.' "
        "Nox venit. Stēllae in caelō sunt. Pater et fīlius in hortō manent. "
        "Et in hortō, sub stēllīs, puer fit vir."
    )
}

STORIES["cap6_16"] = {
    "title_la": "Dominus et servus",
    "title_zh": "主与仆",
    "target_chapter": 6,
    "theme": "58 主人与奴隶",
    "style": "白话",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Dominus: 'Serve, venī!' "
        "Servus: 'Veniō, domine.' "
        "Dominus: 'Portā mēnsam!' "
        "Servus: 'Portō mēnsam.' "
        "Dominus: 'Nōn bene portās! Mēnsa est gravis?' "
        "Servus: 'Domine, mēnsa gravis est. Ego fessus sum. Ego tōtum diem labōrāvī.' "
        "Dominus: 'Tū fessus es? Ego quoque fessus sum. Ego tōtum diem in forō fuī. "
        "Ego cum mercātōribus locūtus sum. Ego cum senātōribus locūtus sum. "
        "Ego dē magnīs rēbus cōgitāvī. Tū — quid fēcistī?' "
        "Servus: 'Ego mēnsās portāvī. Ego aquam portāvī. Ego cibum parāvī. "
        "Ego hortum cūrāvī. Ego vestēs lāvī. Ego omnia fēcī quae iussistī.' "
        "Dominus: 'Et hoc est tuum officium. Tū servus es. Ego dominus sum. "
        "Tū labōrās. Ego imperō. Hic est ōrdō mundī.' "
        "Servus: 'Domine, estne ōrdō mundī iūstus? Cūr ego servus sum et tū dominus? "
        "Ego homō sum — sīcut tū. Ego duōs oculōs habeō — sīcut tū. "
        "Ego cor habeō — sīcut tū. Cūr ego servus sum?' "
        "Dominus: 'Tū audāx es, serve. Tū nōn dēbēs mē interrogāre. "
        "Tū dēbēs pārēre. Hoc est officium servī.' "
        "Servus: 'Domine, ego nōn sum audāx. Ego sōlum quaerō. Ego sōlum intellegere volō. "
        "Cūr ūnus homō est dominus et alius est servus? "
        "Nōnne omnēs hominēs ā dīs factī sunt? Nōnne omnēs hominēs aequē nātī sunt?' "
        "Dominus tacet. Dominus servum spectat. Dominus diū cōgitat. "
        "Dominus: 'Serve, tū mē interrogās — et tū mē docēs. "
        "Ego numquam dē hīs rēbus cōgitāvī. Ego semper dominus fuī. "
        "Pater meus dominus fuit. Avus meus dominus fuit. "
        "Ego semper putāvī hunc esse ōrdinem mundī. "
        "Sed tū mē interrogās — et ego nesciō respondēre.' "
        "Servus: 'Domine, ego nōn tē offendere volō. Ego sōlum līber esse volō. "
        "Ego in Graeciā nātus sum. Ego in Graeciā līber fuī. "
        "Sed Rōmānī mē cēpērunt. Rōmānī mē servum fēcērunt. "
        "Ego patriam meam āmīsī. Ego lībertātem meam āmīsī. "
        "Ego nihil habeō — nisi spem.' "
        "Dominus: 'Quam spem habēs?' "
        "Servus: 'Spem lībertātis. Spem quod aliquandō iterum līber erō. "
        "Spem quod filiī meī līberī erunt. Spem quod nōn semper servus erō.' "
        "Dominus: 'Ego tē intellegō. Ego tē nōn iam ut servum videō. Ego tē ut hominem videō. "
        "Ego tibi lībertātem dabō — sed nōn hodiē. "
        "Tū mihi decem annōs servīvistī. Tū bonus servus fuistī. "
        "Post ūnum annum līber eris. Ego tibi iūrō.' "
        "Servus lacrimat. Servus: 'Domine, tū bonus es. Ego tibi grātiās agō. "
        "Ego tē numquam oblivīscar.' "
        "Dominus: 'Et ego tē numquam oblivīscar, amīce. "
        "Tū mē docuistī quod librī nōn docent. "
        "Tū mē docuistī quod servus quoque homō est. "
        "Post ūnum annum tū nōn servus eris. Tū amīcus eris.' "
        "Annus trānsit. Dominus servum līberat. Servus līber est. "
        "Sed servus nōn discēdit. Servus cum dominō manet. "
        "Servus: 'Tū mihi lībertātem dedistī. Nunc ego līber sum. "
        "Sed ego nōn discēdō. Ego cum tē maneō. "
        "Nōn quia servus sum — sed quia amīcus sum.' "
        "Dominus: 'Et ego tē nōn ut servum, sed ut amīcum habeō. "
        "Venī, amīce. Nōn iam servus et dominus sumus. "
        "Duo hominēs sumus. Duo amīcī sumus.' "
        "Et sīc servus fit līber — et dominus fit hūmānus."
    )
}

STORIES["cap6_17"] = {
    "title_la": "In viā",
    "title_zh": "在路上",
    "target_chapter": 6,
    "theme": "27 旅行",
    "style": "抒情",
    "genre": "C 历史与人物",
    "character_type": "旅人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in viā sum. Via est longa. Ego ā Rōmā ad Brundisium eō. "
        "Via Appia est. Via Appia est rēgīna viārum. Via Appia est via antīqua. "
        "Ego multa oppida videō. Ego Ariciam videō. Aricia est oppidum parvum. "
        "Aricia in monte est. Ā Ariciā Rōma vidērī potest. "
        "Ego Ariciam relinquō. Ego ad Forum Appiī veniō. "
        "Forum Appiī est oppidum parvum. Forum Appiī ad viam est. "
        "In Forō Appiī multī virī sunt. Multī viātōrēs in Forō Appiī cōnsistunt. "
        "Ego cum viātōribus loquor. Ego: 'Quō vādis, amīce?' "
        "Viātor: 'Ego ad Brundisium eō. Ego ad Graeciam nāvigāre volō. "
        "Graecia est terra philosophiae. Graecia est terra sapientiae.' "
        "Alius viātor: 'Ego ad Capuam eō. Capua est oppidum magnum. "
        "Capua est dīves. In Capuā multae mercēs sunt.' "
        "Alius viātor: 'Ego ad Tarentum eō. Tarentum est ad mare. "
        "Tarentum est oppidum Graecum. Tarentum est pulchrum.' "
        "Ego: 'Omnēs iter facimus. Omnēs aliquid quaerimus. "
        "Sed quid ego quaerō? Ego nesciō.' "
        "Ego Forum Appiī relinquō. Ego ad Tarracīnam veniō. "
        "Tarracīna est ad mare. In Tarracīnā mare vidēre possum. "
        "Mare est caeruleum. Mare est magnum. Mare est pulchrum. "
        "In marī nāvēs sunt. Nāvēs ad Graeciam nāvigant. Nāvēs ad Africam nāvigant. "
        "Ego in portū stō. Ego mare spectō. Ego dē vītā cōgitō. "
        "Ego: 'Mare est sīcut vīta. Mare est magnum et profundum. "
        "In marī multae viae sunt — sed nūlla via est certa. "
        "Nāvēs in marī sunt — sed nōn omnēs ad portum veniunt. "
        "Sīcut nāvēs, hominēs quoque in marī vītae nāvigant. "
        "Nōn omnēs ad portum veniunt. Nōn omnēs patriam inveniunt.' "
        "Ego Tarracīnam relinquō. Ego ad Capuam veniō. "
        "Capua est magna. Capua est pulchra. Capua est dīves. "
        "In Capuā multī virī dīvitēs habitant. In Capuā multae vīllae pulchrae sunt. "
        "Ego in Capuā cōnsistō. Ego in caupōnā cēnam sūmō. "
        "Caupō: 'Unde venīs, viātor?' "
        "Ego: 'Ā Rōmā veniō.' "
        "Caupō: 'Quō vādis?' "
        "Ego: 'Ad Brundisium eō. Fortasse ad Graeciam.' "
        "Caupō: 'Graecia est terra pulchra. Graecia est terra antīqua. "
        "Sed Graecia est procul. Via est longa. Mare est perīculōsum.' "
        "Ego: 'Scio. Sed ego īre dēbeō. Ego Graeciam vidēre volō. "
        "Ego templa Graeca vidēre volō. Ego philosophōs Graecōs audīre volō. "
        "Ego patriam Homērī vidēre volō.' "
        "Caupō: 'Bene. Dī tē servent.' "
        "Ego Capuam relinquō. Ego ad Brundisium veniō. "
        "Brundisium est ad mare. Brundisium est porta ad orientem. "
        "In Brundisiō multae nāvēs sunt. Nāvēs ad Graeciam nāvigant. "
        "Ego nāvem inveniō. Nāvis est magna. Nāvis ad Graeciam nāvigat. "
        "Ego in nāvem ascendō. Nāvis ā Brundisiō nāvigat. "
        "Ego in nāvī stō. Ego mare spectō. Ego dē viā cōgitō. "
        "Ego: 'Via est longa. Via ā Rōmā ad Brundisium est longa. "
        "Sed via ā Brundisiō ad Graeciam est longior. "
        "Et via vītae est longissima. "
        "Sed ego nōn timeō. Ego iter faciō. Ego discō. Ego vīvō.' "
        "Nāvis ad Graeciam nāvigat. Mare est caeruleum. Caelum est clārum. "
        "Ego in nāvī stō — et nova terra mē exspectat."
    )
}

# ============================================================
# 执行逻辑
# ============================================================

def title_to_slug(title_la: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9āēīōūȳĀĒĪŌŪȲ\s]", "", title_la)
    return re.sub(r"_+", "_", slug.strip().replace(" ", "_"))

def find_next_number(target_dir: Path, cap_num: int) -> int:
    max_n = 0
    for f in target_dir.glob(f"Cap{cap_num}_*_*.md"):
        m = re.search(r"_(\d{3})\.md$", f.name)
        if m:
            n = int(m.group(1))
            if n > max_n:
                max_n = n
    return max_n + 1

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    passed, failed = [], []

    for story_id, meta in STORIES.items():
        target_ch = meta["target_chapter"]
        latin_text = meta["text"].strip()
        title_la = meta["title_la"]

        print(f"\n--- {story_id}: {title_la} (target Cap.{target_ch}) ---")

        eval_r = evaluate(latin_text, story_id)
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])

        wc = len(re.findall(r"[A-Za-zāēīōūȳĀĒĪŌŪȲ]{2,}", latin_text))
        ok = v2_level is not None and v2_level <= target_ch + 2

        print(f"  词汇: {wc}词, 算法: v2_level={v2_level}, v2_rate={v2_rate}%")

        if not ok:
            print(f"  [FAIL] v2_level={v2_level} > {target_ch+2}, OOV: {v2_oov[:15]}")
            failed.append((story_id, v2_level, v2_oov))
            continue

        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)
        slug = title_to_slug(title_la)
        tier_map = {"中篇": "medius", "中长篇": "longior", "长篇": "longus"}
        tier_slug = tier_map.get(meta["length_tier"], "medius")
        nnn = find_next_number(cap_dir, target_ch)
        filename = f"Cap{target_ch}_{slug}_{tier_slug}_{nnn:03d}.md"
        filepath = cap_dir / filename

        yaml = [
            "---",
            f'story_id: "{story_id}"',
            f'title_la: "{title_la}"',
            f'title_zh: "{meta["title_zh"]}"',
            f'target_chapter: {target_ch}',
            f'evaluated_chapter: {v2_level}',
            f'theme: "{meta["theme"]}"',
            f'style: "{meta["style"]}"',
            f'genre: "{meta["genre"]}"',
            f'character_type: "{meta["character_type"]}"',
            f'length_tier: "{meta["length_tier"]}"',
            f'narrative_mode: "{meta["narrative_mode"]}"',
            f'word_count: {wc}',
            f'macrons_status: "generated"',
            f'v2_rate: {v2_rate}',
            f'v2_oov: {json.dumps(v2_oov, ensure_ascii=False)}',
            f'created_at: "{now}"',
            f'updated_at: "{now}"',
            f'status: "active"',
            f'rewritten_from: "brevis"',
            "---",
        ]
        filepath.write_text("\n".join(yaml) + "\n\n" + latin_text + "\n", encoding="utf-8")
        print(f"  [PASS] → {filename} ({wc} 词)")
        passed.append((story_id, filename, target_ch, wc))

    print(f"\n{'='*60}")
    print(f"结果: {len(passed)} 通过, {len(failed)} 失败")
    for sid, fn, ch, wc in passed:
        print(f"  [OK] Cap.{ch}: {fn} ({wc}词)")
    for sid, lvl, oov in failed:
        print(f"  [FAIL] {sid}: v2_level={lvl}, OOV={oov[:10]}")

    if failed:
        print("\n!!! 有失败项，请修正后重试 !!!")
        sys.exit(1)

if __name__ == "__main__":
    main()