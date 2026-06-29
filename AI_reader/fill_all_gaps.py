#!/usr/bin/env python3
"""
fill_all_gaps.py — 批量补齐所有章节缺口（Cap21-48）。
每个章节生成 N 篇故事（N = need），通过 evaluate_v2 算法验证。
"""

import json, re, sys, os
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
PROGRESS_FILE = Path(__file__).resolve().parent / "progress.json"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

# ============================================================
# 所有故事定义（按章节分组）
# 格式: "story_id": { title_la, title_zh, target_chapter, theme, style, genre, character_type, length_tier, narrative_mode, text }
# ============================================================

STORIES = {}

# === Cap.21: 需 5 篇 ===
STORIES["cap21_06"] = {
    "title_la": "Vōx in Tenebrīs",
    "title_zh": "黑暗中的声音",
    "target_chapter": 21, "theme": "80 恐惧与勇气", "style": "冷峻",
    "genre": "J 被忽略的声音", "character_type": "奴隶", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "In tenebrīs vōcem audiō. Nēmō mē videt. Nēmō mē scit. Ego sum servus. "
        "Dominus meus multōs servōs habet. Nōn sum ūnus — sum ūnus ex multīs. "
        "Sed hanc vōcem audiō. Vōx dīcit: 'Nōn semper servus eris.' "
        "Ego rīdeō. Quis in tenebrīs loquitur? Nēmō. "
        "Sed vōx iterum loquitur: 'Audī. Tempus veniet.' "
        "Ego taceō. Ego spērō. Spēs est perīculōsa — sed spēs est mea."
    )
}

STORIES["cap21_07"] = {
    "title_la": "Duo Nāvigia",
    "title_zh": "两艘船",
    "target_chapter": 21, "theme": "84 偶然与命运", "style": "古典",
    "genre": "C 历史与人物", "character_type": "商人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duo nāvigia ex portū eōdem diē nāvigant. Ūnum ad Graeciam cursum tenet, "
        "alterum ad Āfricam. Ventus bonus est. Nautae laetī sunt. "
        "Sed post trēs diēs, tempestās oritur. Mare magnum et perīculōsum est. "
        "Nāvigium quod ad Graeciam nāvigat perit. Nautae mortuī sunt. Nēmō superest. "
        "Nāvigium quod ad Āfricam nāvigat salvum est. Nautae vīvunt. "
        "Cūr ūnum perit et alterum vīvit? Ventus idem fuit. Mare idem. "
        "Fātum nōn respondet. Fātum tacet."
    )
}

STORIES["cap21_08"] = {
    "title_la": "Imperātor Sine Exercitū",
    "title_zh": "无军之将",
    "target_chapter": 21, "theme": "06 权力", "style": "雄辩",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "独白体",
    "text": (
        "Ego imperātor sum. Sed ubi est exercitus meus? Mortuī sunt. "
        "Omnēs mortuī. In bellō mortuī. In nive mortuī. In fame mortuī. "
        "Ego super sum. Cūr ego super sum? Cūr ego nōn mortuus sum? "
        "Imperātor sine exercitū nōn est imperātor. Ego nōn sum imperātor. "
        "Ego sum senex sōlus. Senex quī meminit. Senex quī nōn potest oblīvīscī. "
        "Populus mē videt et tacet. Populus mē videt et oculōs āvertit. "
        "Imperātor sum — sed imperātor mortuōrum."
    )
}

STORIES["cap21_09"] = {
    "title_la": "Pīrātae et Puer",
    "title_zh": "海盗与男孩",
    "target_chapter": 21, "theme": "46 革命与改良", "style": "白话",
    "genre": "F 架空与虚构", "character_type": "旅人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pīrātae nāvigium parvum capiunt. In nāvigiō puer sōlus est. "
        "Pīrātae puerum rīdent. 'Quid tū facis in marī sōlus, puer?' "
        "Puer nōn respondet. Puer nōn timet. Pīrātae mīrantur. "
        "'Cūr nōn timēs?' Puer dīcit: 'Vōs nōn pīrātae estis. Vōs servī estis. "
        "Servī maris. Servī ventī. Servī fugae. Ego līber sum.' "
        "Pīrātae tacent. Pīrātae puerum in īnsulā parvā relinquunt. "
        "Puer in īnsulā sōlus est — sed līber."
    )
}

STORIES["cap21_10"] = {
    "title_la": "Lūx in Fenestrā",
    "title_zh": "窗中之光",
    "target_chapter": 21, "theme": "19 希望", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Omnī nocte lūcem videō. Lūx in fenestrā parvā est. "
        "Fenestra in monte est. Domus in monte sōla est. "
        "Quis in domō habitat? Nesciō. Sed omnī nocte lūx ārdet. "
        "Ego in valle habitō. Ego ad montem numquam ascendī. "
        "Sed lūx mē vocat. Lūx dīcit: 'Hīc sum. Nōn sōlus es.' "
        "Hodiē lūx nōn ārdet. Fenestra nigra est. "
        "Ego montem ascendō. Domus vacua est. Nēmō in domō habitat. "
        "Sed in fenestrā — candēla parva. Et ego flēvī."
    )
}

# === Cap.22: 需 3 篇 ===
STORIES["cap22_08"] = {
    "title_la": "Dē Bellō et Fīliō",
    "title_zh": "战争与儿子",
    "target_chapter": 22, "theme": "15 战争", "style": "书信",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "书信体",
    "text": (
        "Fīliō meō salūtem. Hās litterās scrībō ante proelium. "
        "Nesciō an hās litterās legēs. Nesciō an ego vīvam. "
        "Bellum nōn est glōriōsum. Bellum est caenum et sanguis et timor. "
        "Nōlī crēdere iīs quī dīcunt bellum pulchrum esse. "
        "Sī hodiē moriar, nōlī mē ulcīscī. Ulcīscendī cupiditās plūs bellī parit. "
        "Sī vīvam, domum veniam et tē amplectar. "
        "Valē, fīlī. Pater tuus tē amat."
    )
}

STORIES["cap22_09"] = {
    "title_la": "Mercātor et Simia",
    "title_zh": "商人与猴子",
    "target_chapter": 22, "theme": "41 财富与贫困", "style": "戏谑",
    "genre": "G 哲学寓言", "character_type": "商人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mercātor dīves simiam habet. Simia in caveā aureā habitat. "
        "Mercātor simiae cibum optimum dat. Simia vinum bibit. Simia in lectō dormit. "
        "Amīcī mercātōris dīcunt: 'Cūr simiae tantum dās?' "
        "Mercātor respondet: 'Simiam amō. Simia mē amat.' "
        "Ūnō diē mercātor pauper fit. Pecūniam omnem perdit. "
        "Simiam in caveā aureā relinquit. Simia mercātōrem sequitur. "
        "Mercātor dīcit: 'Cūr mē sequeris? Nōn habeō aurum. Nōn habeō cibum.' "
        "Simia mercātōris manum prehendit. Nōn respondet. Sed nōn relinquit."
    )
}

STORIES["cap22_10"] = {
    "title_la": "Tabula Rāsa",
    "title_zh": "白板",
    "target_chapter": 22, "theme": "85 故事与真实", "style": "精炼",
    "genre": "J 心理与梦境", "character_type": "学者", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Hodiē tabulam rāsam ēmī. Cēram novam. Nihil in eā scrīptum. "
        "Herī omnia combussī. Epistulās. Librōs. Tabulās. "
        "Nōmen meum vetus combussī. Nōmen novum hodiē scrībō. "
        "Sed quis sum sine memoriā? Quis sum sine praeteritō? "
        "Tabula rāsa est. Ego tabula rāsa sum. "
        "Sed hōc quoque scrībō. Hōc quoque manet."
    )
}

# === Cap.23: 需 8 篇 ===
STORIES["cap23_03"] = {
    "title_la": "Senex et Mare",
    "title_zh": "老人与海",
    "target_chapter": 23, "theme": "61 暮年与青春", "style": "精炼",
    "genre": "G 哲学寓言", "character_type": "老人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Senex omnī diē ad mare venit. Sedet. Spectat. Tacet. "
        "Puerī eum rīdent. 'Senex stultus est! Mare semper idem est!' "
        "Senex nōn respondet. Senex oculōs nōn āvertit. "
        "Quid senex in marī videt? Nēmō scit. "
        "Ūnō diē senex nōn venit. Puerī ad mare veniunt. "
        "Mare idem est. Sed aliquid dēest. "
        "Sine sene, mare nōn est mare."
    )
}

STORIES["cap23_04"] = {
    "title_la": "Fuga ex Aegyptō",
    "title_zh": "逃离埃及",
    "target_chapter": 23, "theme": "03 自由与束缚", "style": "史诗",
    "genre": "C 历史与人物", "character_type": "非罗马的古代人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Populus in Aegyptō servit. Multōs annōs servit. Multōs annōs labōrat. "
        "Mōsēs populum vocat: 'Līberī erimus! Ex Aegyptō fugiēmus!' "
        "Populus timet. Pharaō magnus est. Exercitus pharaōnis magnus est. "
        "Sed Mōsēs mare rubrum tangit. Aquae sē dīvidunt. "
        "Populus per mare ambulat. In medīs aquīs populus ambulat. "
        "Pharaō cum exercitū sequitur. Sed aquae redeunt. "
        "Pharaō in marī perit. Populus līber est. "
        "Sed lībertās in dēsertō incipit — et dēsertum longum est."
    )
}

STORIES["cap23_05"] = {
    "title_la": "Hortus in Monte",
    "title_zh": "山上的花园",
    "target_chapter": 23, "theme": "11 自然与文明", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Hortum in monte colō. Nēmō mē iuvat. Nēmō mē videt. "
        "Hortus meus parvus est. Sed pulcher est. "
        "Flōrēs variōs habeō. Rosās rubrās. Līlia alba. "
        "Hortus meus in monte sōlus est. Sed nōn sum sōlus. "
        "Avēs in hortō cantant. Ventus in foliīs loquitur. "
        "Urbem ā longē videō. Fumus. Strepitus. Clāmōrēs. "
        "Ego in monte taceō. Ego in hortō meō sum. "
        "Hortus meus — mundus meus."
    )
}

STORIES["cap23_06"] = {
    "title_la": "Iūdicium Salōmōnis",
    "title_zh": "所罗门的审判",
    "target_chapter": 23, "theme": "04 正义", "style": "古典",
    "genre": "E 跨文明", "character_type": "非罗马的古代人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duae mulierēs ad rēgem Salōmōnem veniunt. Ūnum īnfantem portant. "
        "Ūna mulier dīcit: 'Hīc īnfāns meus est!' Altera: 'Nōn! Meus est!' "
        "Salōmōn tacet. Salōmōn cōgitat. Tum dīcit: 'Gladium afferte. "
        "Īnfantem in duās partēs dīvidam. Ūna pars huic, altera illī.' "
        "Ūna mulier tacet. Altera clāmat: 'Nōlī! Īnfantem illī date! Nōlī eum occīdere!' "
        "Salōmōn rīdet. 'Tū vēra māter es. Īnfantem tibi dō.' "
        "Populus mīrātur. Sapientia rēgis magna est."
    )
}

STORIES["cap23_07"] = {
    "title_la": "Nox in Dēsertō",
    "title_zh": "沙漠之夜",
    "target_chapter": 23, "theme": "13 孤独", "style": "冷峻",
    "genre": "F 架空与虚构", "character_type": "旅人", "length_tier": "中长篇",
    "narrative_mode": "第二人称",
    "text": (
        "Tū in dēsertō sōlus es. Sōl ārdet. Aqua nūlla est. "
        "Tū ambulās. Tū cadis. Tū iterum surgis. Tū iterum ambulās. "
        "Nox venit. Stēllae in caelō sunt. Frīgus in dēsertō est. "
        "Tū in harēnā iacēs. Tū ad stēllās spectās. "
        "Stēllae tacent. Stēllae nōn respondent. "
        "Tū quoque tacēs. Tū quoque stēlla es — parva, sōla, ārdēns."
    )
}

STORIES["cap23_08"] = {
    "title_la": "Māter et Fīlia in Forō",
    "title_zh": "广场上的母女",
    "target_chapter": 23, "theme": "29 母性与自我", "style": "白话",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Māter fīliam in forō dūcit. Fīlia: 'Māter, cūr virī in forō clāmant?' "
        "Māter: 'Virī semper clāmant. Hoc est forum.' "
        "Fīlia: 'Cūr fēminae in forō tacent?' Māter tacet. "
        "Fīlia iterum: 'Māter, cūr fēminae tacent?' "
        "Māter: 'Fēminae multa dīcunt — sed nōn in forō.' "
        "Fīlia: 'Ego in forō loquī volō.' Māter fīliam spectat. "
        "Māter: 'Tū loqueris. Sed vōx tua — audītur?'"
    )
}

STORIES["cap23_09"] = {
    "title_la": "Arbor Quae Dormit",
    "title_zh": "沉睡的树",
    "target_chapter": 23, "theme": "18 自然", "style": "修辞",
    "genre": "B 神话与传说", "character_type": "拟人自然", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "In mediō campō arbor stat. Arbor magna et vetus est. "
        "Arbor nōn folia habet. Arbor nōn flōrēs habet. Arbor dormit. "
        "Avēs ad arborem veniunt. 'Arbor, cūr dormīs?' Arbor nōn respondet. "
        "Ventus ad arborem venit. 'Arbor, cūr dormīs?' Arbor nōn respondet. "
        "Imber ad arborem venit. 'Arbor, cūr dormīs?' Arbor nōn respondet. "
        "Sed sub terrā, rādīcēs crescunt. Sub terrā, arbor vīvit. "
        "Arbor nōn dormit — arbor exspectat."
    )
}

STORIES["cap23_10"] = {
    "title_la": "Piscātor et Umbra",
    "title_zh": "渔夫与影子",
    "target_chapter": 23, "theme": "22 旅程", "style": "冷峻",
    "genre": "G 哲学寓言", "character_type": "旅人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Piscātor omnī nocte in flūmine piscātur. Nēmō eum videt. "
        "Piscātor: 'Cūr in nocte piscor? Nēmō mē videt. Nēmō mē cognōscit.' "
        "Umbra in aquā: 'Ego tē videō.' Piscātor: 'Tū umbra es. Nōn es vēra.' "
        "Umbra: 'Tū quoque umbra es. Vērum nōn est.' "
        "Piscātor in aquam cadit. Umbra in aquā manet. Piscātor nōn manet. "
        "Māne, piscātor in rīpā iacet. Vivus est. Umbra in aquā nōn est. "
        "Piscātor surgit. Piscātor domum ambulat. Piscātor nōn respicit."
    )
}

# === Cap.24: 需 4 篇 ===
STORIES["cap24_07"] = {
    "title_la": "Via ad Occidentem",
    "title_zh": "西行之路",
    "target_chapter": 24, "theme": "22 旅程", "style": "史诗",
    "genre": "B 神话与传说", "character_type": "希腊人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hēraclēs ad occidentem iter facit. Sōl in oculīs eius ārdet. "
        "In viā multa perīcula sunt. Leōnēs. Serpentēs. Hostēs. "
        "Sed Hēraclēs nōn timet. Hēraclēs per omnia perīcula ambulat. "
        "Tandem ad occidentem venit. Mare magnum videt. "
        "'Hīc fīnis mundī est,' Hēraclēs dīcit. 'Hīc fīnis viae meae.' "
        "Sed mare respondet: 'Nōn est fīnis. Post mare, alius mundus.' "
        "Hēraclēs in mare spectat. Hēraclēs tacet. "
        "Fīnis nōn est fīnis — sed initium aliud."
    )
}

STORIES["cap24_08"] = {
    "title_la": "Cēna Novissima",
    "title_zh": "最后的晚餐",
    "target_chapter": 24, "theme": "10 牺牲", "style": "精炼",
    "genre": "K 宗教与灵性智慧", "character_type": "非罗马的古代人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Hodiē cum amīcīs meīs cēnō. Hodiē pānem frangō. Hodiē vinum bibō. "
        "Amīcī meī rīdent. Amīcī meī nesciunt. "
        "Hanc noctem ūnus ex vōbīs mē trādet. Hanc noctem omnēs mē relinquent. "
        "Sed ego nōn eōs relinquō. Ego prō eīs morior. "
        "Pānem frangō: 'Hoc est corpus meum.' Vinum bibō: 'Hic est sanguis meus.' "
        "Amīcī meī nōn intellegunt. Sed intellegent — posteā."
    )
}

STORIES["cap24_09"] = {
    "title_la": "Nāvis Sine Portū",
    "title_zh": "无港之船",
    "target_chapter": 24, "theme": "21 命运与自由", "style": "抒情",
    "genre": "F 架空与虚构", "character_type": "商人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nāvis in marī nāvigat. Multōs annōs nāvigat. Nāvis portum nōn invenit. "
        "Nautae: 'Ubi est portus? Quandō terram vidēbimus?' "
        "Gubernātor: 'Portus est. Sed quandō — nesciō.' "
        "Nautae: 'Nōs ad terram dūc!' Gubernātor tacet. "
        "Nāvis nāvigat. Diēs et noctēs. Annī. "
        "Nautae senēscunt. Gubernātor senēscit. Nāvis senēscit. "
        "Tandem nāvis ad terram venit. Terra vacua est. Nēmō in terrā. "
        "Portus nōn est. Portus numquam fuit. Sed nāvis nōn nāvigat."
    )
}

STORIES["cap24_10"] = {
    "title_la": "Puer Quī Nōn Flēvit",
    "title_zh": "没有哭的男孩",
    "target_chapter": 24, "theme": "79 欢愉与痛苦", "style": "冷峻",
    "genre": "J 心理与梦境", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer mātrem mortuam videt. Puer nōn flet. Puer tacet. "
        "Pater: 'Flē, fīlī. Mors mātris dolōrem magnum portat.' "
        "Puer nōn flet. Puer in cubiculum suum it. Puer iānuam claudit. "
        "Pater forīs stat. Pater audit. Puer tacet. "
        "Post multōs annōs, puer vir est. Bellum venit. Vir in bellō pugnat. "
        "Vir multōs amīcōs mortuōs videt. Vir nōn flet. "
        "Sed nocte, sōlus, vir sub caelō iacet. Et vir flēvit. "
        "Nōn propter bellum. Propter mātrem."
    )
}

# === Cap.26: 需 1 篇 ===
STORIES["cap26_10"] = {
    "title_la": "Duo Sole",
    "title_zh": "两个太阳",
    "target_chapter": 26, "theme": "12 时间", "style": "抒情",
    "genre": "B 神话与传说", "character_type": "拟人概念", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "In prīncipiō, duo sōlēs in caelō erant. Ūnus māne surgēbat, alter vesperī. "
        "Diēs duās partēs habēbat. Hominēs numquam dormiēbant. "
        "Hominēs numquam umbrās vidēbant. Nōn erat nox. Nōn erant tenebrae. "
        "Deī dīxērunt: 'Duo sōlēs nimium est. Ūnum dēlēbimus.' "
        "Ūnus sōl clāmāvit: 'Mē dēlēte! Ego frāter meus servārī volō.' "
        "Alter sōl clāmāvit: 'Nōn! Mē dēlēte! Ego frātrem meum amō.' "
        "Deī utrumque sōlem servāvērunt. Sed ūnum diē, ūnum nocte lūcēre iussērunt. "
        "Sīc nox nāta est. Sīc umbrae nātae sunt. Et frātrēs — numquam simul."
    )
}

# === Cap.27: 需 4 篇 ===
STORIES["cap27_07"] = {
    "title_la": "Verbum Ultimum",
    "title_zh": "最后的话",
    "target_chapter": 27, "theme": "01 生死", "style": "精炼",
    "genre": "M 伦理与习俗", "character_type": "老人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Moriēns sum. Nōn timeō. Nōn doleō. Verbum ultimum quaerō. "
        "Verbum quod omnia comprehendit. Verbum quod vītam meam explicat. "
        "Fīlius meus adest. Fīlia mea adest. Amīcī adsunt. "
        "Omnēs exspectant. Omnēs verbum ultimum audīre volunt. "
        "Ego ōs aperiō. Ego verbum quaerō. Verbum nōn venit. "
        "Ego ōs claudō. Ego taceō. Verbum ultimum meum — silentium."
    )
}

STORIES["cap27_08"] = {
    "title_la": "Faber et Gladius",
    "title_zh": "铁匠与剑",
    "target_chapter": 27, "theme": "34 劳动", "style": "冷峻",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Faber in officīnā labōrat. Ferrum in igne calefacit. "
        "Gladium facit. Gladius pulcher est. Gladius fortis est. "
        "Mīles in officīnam intrat. 'Hunc gladium volō. Bellum mox est.' "
        "Faber gladium dat. Mīles pecūniam dat. Mīles abit. "
        "Post multōs diēs, mīles redit. Gladius in manū rūptus est. "
        "Faber: 'Gladium frēgistī?' Mīles: 'Multōs hostēs occīdī. Gladius frāctus est.' "
        "Faber: 'Gladium facere possum. Sed hominēs quōs occīdistī — reficere nōn possum.'"
    )
}

STORIES["cap27_09"] = {
    "title_la": "Flūmen Quod Dēfluit",
    "title_zh": "流逝的河",
    "target_chapter": 27, "theme": "17 时间", "style": "抒情",
    "genre": "G 哲学寓言", "character_type": "旅人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ad flūmen sedeō. Aqua dēfluit. Aqua semper dēfluit. "
        "Eadem aqua numquam bis vidētur. Eadem aqua numquam manet. "
        "Hodiē ego ad flūmen sedeō. Herī quoque ad flūmen sedēbam. "
        "Sed ego nōn sum idem. Herī alter eram. Crās alter erō. "
        "Flūmen dēfluit. Ego dēfluō. Omnēs dēfluimus. "
        "Sed flūmen in mare intrat. Ego — quō intrō?"
    )
}

STORIES["cap27_10"] = {
    "title_la": "Mulier Sine Nōmine",
    "title_zh": "无名的女人",
    "target_chapter": 27, "theme": "70 命名与身份", "style": "冷峻",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mulier in vīllā labōrat. Nōmen eius nēmō scit. Nōmen eius nēmō quaerit. "
        "Mulier cibum parat. Mulier vestēs lavat. Mulier īnfantēs cūrat. "
        "Dominus: 'Mulier, venī!' Mulier venit. Dominus: 'Mulier, abī!' Mulier abit. "
        "Ūnō diē mulier cadit. Mulier nōn surgit. Mulier mortua est. "
        "Dominus: 'Mulier mortua est. Sepelīte eam.' "
        "In sepulcrō, nūllum nōmen scrīptum est. "
        "Sed ventus nōmen eius nōvit. Terra nōmen eius nōvit. "
        "Nōmen eius in terrā scrīptum est — sed nēmō id legit."
    )
}

# === Cap.28: 需 7 篇 ===
STORIES["cap28_04"] = {
    "title_la": "Fur et Luna",
    "title_zh": "小偷与月亮",
    "target_chapter": 28, "theme": "50 罪与罚", "style": "白话",
    "genre": "G 哲学寓言", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Fūr in nocte per urbem ambulat. Lūna plēna in caelō est. "
        "Fūr: 'Lūna, cūr mē spectās? Cūr mē prōdis?' "
        "Lūna: 'Ego omnēs spectō. Nōn tē sōlum.' "
        "Fūr: 'Nōn possum fūrārī sī tū mē spectās.' "
        "Lūna: 'Tū tē spectārī timēs — sed tē ipsum nōn spectās. Quis es tū?' "
        "Fūr tacet. Fūr in umbram fugit. Sed lūna ubīque est. "
        "Fūr: 'Ubīque mē sequeris.' Lūna: 'Ego nōn sequor — tū mē portās.'"
    )
}

STORIES["cap28_05"] = {
    "title_la": "Epistula ad Mortuum",
    "title_zh": "致死者书",
    "target_chapter": 28, "theme": "08 记忆", "style": "书信",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "书信体",
    "text": (
        "Amīcō meō mortuō salūtem. Sciō tē hanc epistulam nōn legere. "
        "Sciō tē mortuum esse. Sed scrībō. Scrībō quia tē quaerō. "
        "Scrībō quia nōn possum oblīvīscī. Scrībō quia silentium tuum mē terret. "
        "Herī in forō fuī. Vōcem tuam audīvī — sed tū nōn aderās. "
        "Hodiē in hortō fuī. Rīsum tuum audīvī — sed tū nōn aderās. "
        "Mortuī nōn sunt absentēs. Mortuī sunt ubīque — sed nōn loquuntur. "
        "Valē, amīce. Ego quoque mox veniam. Et tunc — loquēmur."
    )
}

STORIES["cap28_06"] = {
    "title_la": "Caupō et Philosophus",
    "title_zh": "店主与哲学家",
    "target_chapter": 28, "theme": "41 财富与贫困", "style": "戏谑",
    "genre": "D 讽刺", "character_type": "学者", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Philosophus in caupōnā sedet. Caupō: 'Quid bibis, philosophus?' "
        "Philosophus: 'Aquam bibō. Aqua sānitātem dat. Vīnum mentem turbat.' "
        "Caupō: 'Sed vīnum argentum dat. Argentum mihi sānitātem dat.' "
        "Philosophus: 'Pecūnia nōn est sānitās.' "
        "Caupō: 'Tū numquam pecūniam habuistī. Quōmodo scīs?' "
        "Philosophus: 'Plūrimōs dīvitēs vīdī. Nōn erant sānī.' "
        "Caupō: 'Et plūrimōs pauperēs vīdī. Nōn erant philosophī.' "
        "Philosophus tacet. Caupō rīdet. Caupō aquam philosophō dat — grātīs."
    )
}

STORIES["cap28_07"] = {
    "title_la": "Nāvis Phantasma",
    "title_zh": "幽灵船",
    "target_chapter": 28, "theme": "15 战争", "style": "冷峻",
    "genre": "B 神话与传说", "character_type": "非罗马的古代人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nāvis in marī appāret. Nāvis nigra est. Nāvis vēla nigra habet. "
        "Nautae in nāvī sunt — sed nautae mortuī sunt. "
        "Nāvis per mare sine vīvīs nāvigat. Ventus nōn flat — sed nāvis movet. "
        "Piscātōrēs nāvem vident. Piscātōrēs timent. Piscātōrēs fugiunt. "
        "Sed ūnus piscātor nōn fugit. Ūnus piscātor nāvem spectat. "
        "In nāvī, pater eius mortuus stat. Pater eum spectat. Pater tacet. "
        "Piscātor: 'Pater, cūr nōn loqueris?' Pater nōn respondet. "
        "Nāvis abīt. Pater abīt. Piscātor sōlus in rīpā manet."
    )
}

STORIES["cap28_08"] = {
    "title_la": "Fēmina Quae Numquam Rīsit",
    "title_zh": "从不笑的女人",
    "target_chapter": 28, "theme": "79 欢愉与痛苦", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Fēmina in oppidō habitat. Fēmina numquam rīdet. "
        "Oppidānī: 'Cūr numquam rīdēs? Vīta pulchra est. Sōl lūcet. Avēs cantant.' "
        "Fēmina nōn respondet. Fēmina in terrā aliquid quaerit. "
        "Oppidānī: 'Quid quaeris?' Fēmina: 'Quod perdidī.' "
        "Oppidānī: 'Quid perdidistī?' Fēmina: 'Nesciō. Sed quandō inveniam, sciam.' "
        "Multī annī trānseunt. Fēmina senēscit. Fēmina adhūc quaerit. "
        "Ūnō diē fēmina in terrā lacrimās suās invenit. "
        "Fēmina lacrimās suās spectat. Fēmina rīdet. Tandem."
    )
}

STORIES["cap28_09"] = {
    "title_la": "Gladiātor et Mūs",
    "title_zh": "角斗士与老鼠",
    "target_chapter": 28, "theme": "03 自由与束缚", "style": "精炼",
    "genre": "M 伦理与习俗", "character_type": "奴隶", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego gladiātor sum. In carcerō habitō. Mūs quoque in carcerō habitat. "
        "Mūs per parvum forāmen intrat. Mūs per parvum forāmen exit. "
        "Ego per parvum forāmen exīre nōn possum. Ego magnus sum. "
        "Mūs: 'Tū mē vides. Tū mē invidēs. Ego līber sum.' "
        "Ego: 'Tū parvus es. Ego magnus sum. Ego fortis sum.' "
        "Mūs: 'Fortitūdō tua est career tuus. Parvitās mea est lībertās mea.' "
        "Mūs exit. Ego in carcerō maneō. Ego magnus sum. Ego fortis sum. Ego sōlus sum."
    )
}

STORIES["cap28_10"] = {
    "title_la": "Hortus Clausus",
    "title_zh": "禁闭的花园",
    "target_chapter": 28, "theme": "36 乡村", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hortus in mediā urbe latet. Hortus mūrō altō clausus est. "
        "Nēmō hortum intrat. Nēmō hortum videt. Sed hortus vīvit. "
        "Rosae in hortō flōrent. Fontēs in hortō cantant. Avēs in hortō nīdificant. "
        "Puer parvus per forāmen in mūrō spectat. Puer hortum videt. "
        "Puer: 'Ō, hortus! Quis tē crēāvit? Cūr tē clausit?' "
        "Hortus: 'Quī mē clausit, mē nōn videt. Sed tū mē vidēs. Ego tibi sum.' "
        "Puer per forāmen intrat. Puer in hortō sōlus est. Puer rīdet. "
        "Hortus nōn clausus est. Hortus semper apertus fuit — sed nēmō intrāvit."
    )
}

# === Cap.29: 需 3 篇 ===
STORIES["cap29_08"] = {
    "title_la": "Vātēs Sine Deō",
    "title_zh": "无神的先知",
    "target_chapter": 29, "theme": "27 信仰与怀疑", "style": "古典",
    "genre": "K 宗教", "character_type": "非罗马的古代人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego vātēs sum. Deī per mē loquuntur. Hoc omnēs dīcunt. "
        "Sed ego vōcem deōrum numquam audīvī. Ego sōlus in templō sedeō. "
        "Populus venit. Populus ōrācula quaerit. Ego verba dīcō. "
        "Verba mea populum cōnsōlantur. Verba mea populum terrent. "
        "Ego verba fingō. Ego numquam vēra dīcō — sed populus crēdit. "
        "Cūr populus crēdit? Quia crēdere vult. Quia sine deīs — mundus vacuus est. "
        "Ego vātēs sum. Deī nōn sunt. Sed populus deīs eget. "
        "Et ego — populus meus. Ego deus eōrum sum."
    )
}

STORIES["cap29_09"] = {
    "title_la": "Vir Quī Duās Vītās Vīxit",
    "title_zh": "活了两辈子的人",
    "target_chapter": 29, "theme": "17 时间", "style": "意识流",
    "genre": "J 心理与梦境", "character_type": "商人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Duās vītās vīxī. Prīmam in urbe. Multam pecūniam habuī. Multōs amīcōs habuī. "
        "Multās fēminās amāvī. Multa vīna bibī. Multās noctēs vigilāvī. "
        "Tum omnia perdidī. Pecūniam. Amīcōs. Amōrēs. Domum. "
        "Secundam vītam in silvā vīvō. Sōlus. Nihil habeō. Nēminem amō. Nēmō mē amat. "
        "Nunc quaerō: utra vīta vēra fuit? Illa, in quā omnia habēbam? "
        "An haec, in quā nihil habeō — sed ego sum?"
    )
}

STORIES["cap29_10"] = {
    "title_la": "Ieiūnium",
    "title_zh": "斋戒",
    "target_chapter": 29, "theme": "29 信仰", "style": "电报",
    "genre": "K 宗教", "character_type": "非罗马的古代人", "length_tier": "中长篇",
    "narrative_mode": "日记体",
    "text": (
        "Diēs prīmus. Nōn edō. Nōn bibō. Dēsertum intus. "
        "Diēs secundus. Ventris dolor. Mentis lūx. Deī prope. "
        "Diēs tertius. Corpus cadit. Anima surgit. Vōx — cuius? "
        "Diēs quārtus. Nōn sum. Sum. Nōn sum. Sum. "
        "Diēs quīntus. Silentium. Deus. Ego. Nōn duo — ūnum."
    )
}

# === Cap.30: 需 7 篇 ===
STORIES["cap30_04"] = {
    "title_la": "Mātrōna et Ancilla",
    "title_zh": "女主人与女奴",
    "target_chapter": 30, "theme": "58 主人与奴隶", "style": "冷峻",
    "genre": "M 伦理与习俗", "character_type": "奴隶", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Mātrōna ancillam vocat. 'Ancilla, venī. Pecūniam meam nummōs numerā.' "
        "Ancilla venit. Ancilla nummōs numerat. Ancilla tacet. "
        "Mātrōna: 'Cūr tacēs? Cūr nōn loqueris?' Ancilla: 'Ancilla sum. Ancilla tacet.' "
        "Mātrōna: 'Ego tē bene tractō. Cibum tibi dō. Vestēs tibi dō.' "
        "Ancilla: 'Sed lībertātem nōn dās.' Mātrōna tacet. "
        "Ancilla: 'Lībertās nōn est cibus. Lībertās nōn est vestis. Lībertās est — ego.' "
        "Mātrōna ancillam spectat. Mātrōna: 'Tū mē docēs — et ego domina sum.' "
        "Ancilla: 'Domina — sed nōn lībera.'"
    )
}

STORIES["cap30_05"] = {
    "title_la": "Rēx et Mendīcus",
    "title_zh": "国王与乞丐",
    "target_chapter": 30, "theme": "06 权力", "style": "雄辩",
    "genre": "D 讽刺", "character_type": "乞丐", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Rēx per urbem ambulat. Populus rēgem salūtat. Rēx populum nōn videt. "
        "Mendīcus in viā sedet. Rēx mendīcum videt. Rēx cōnsistit. "
        "Rēx: 'Mendīce, quid tibi dēsīderās?' Mendīcus: 'Nihil, rēx.' "
        "Rēx: 'Nihil? Ego omnia habeō — et tamen aliquid dēsīderō.' "
        "Mendīcus: 'Quid tū dēsīderās, rēx?' "
        "Rēx: 'Somnum. Quot noctēs nōn dormiō. Timor. Invidia. Cūrae.' "
        "Mendīcus: 'Ego nihil habeō — sed ego dormiō. Ego nōn timeō. Ego līber sum.' "
        "Rēx tacet. Rēx mendīcō nummum dat. Mendīcus nummum accipit — sed nōn rīdet."
    )
}

STORIES["cap30_06"] = {
    "title_la": "Flūmen Immortāle",
    "title_zh": "不朽的河",
    "target_chapter": 30, "theme": "01 生死", "style": "修辞",
    "genre": "B 神话与传说", "character_type": "拟人自然", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Flūmen Styx in īnferōs fluit. Omnēs mortuī flūmen trānseunt. "
        "Nauta Charōn eōs in nāvigiō portat. Nauta nummum ab ūnōquōque poscit. "
        "Ūnus mortuus nummum nōn habet. Charōn: 'Sine nummō nōn trānsīs.' "
        "Mortuus: 'Pauper vīxī. Pauper morior. Nummum nōn habeō.' "
        "Charōn: 'Tū in rīpā manēbis. Semper hīc manēbis.' "
        "Mortuus in rīpā sedet. Mortuus flūmen spectat. Annī trānseunt. "
        "Mortuus: 'Nōn vīvus. Nōn mortuus. Inter duōs mundōs — sōlus.'"
    )
}

STORIES["cap30_07"] = {
    "title_la": "Cīvis et Exsul",
    "title_zh": "公民与流放者",
    "target_chapter": 30, "theme": "45 迁徙与流放", "style": "古典",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Cīvis in forō exsulem videt. Exsul ab urbe pulsus est. "
        "Cīvis: 'Exsul, cūr ab urbe pulsus es?' Exsul: 'Vēra dīxī.' "
        "Cīvis: 'Vēritās tē dēlēvit.' Exsul: 'Vēritās mē līberāvit.' "
        "Cīvis: 'Tū nihil habēs. Nūllam domum. Nūllam patriam.' "
        "Exsul: 'Domum habeō — in memoriā. Patriam habeō — in vēritāte.' "
        "Cīvis tacet. Cīvis in urbe manet. Exsul ab urbe abit. "
        "Cīvis in urbe — exsul in animō. Exsul in exsiliō — līber in animō. "
        "Quis vērus exsul est?"
    )
}

STORIES["cap30_08"] = {
    "title_la": "Medicus et Puer Mortuus",
    "title_zh": "医生与死去的男孩",
    "target_chapter": 30, "theme": "60 疾病与健康", "style": "精炼",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Medicus ad puerum venit. Puer nōn spīrat. Puer mortuus est. "
        "Māter puerī: 'Medice, servā eum! Tū multōs servāvistī!' "
        "Medicus puerum spectat. Medicus tacet. Medicus caput quatit. "
        "Māter: 'Cūr eum nōn servās? Cūr tū — medicus — nihil facis?' "
        "Medicus: 'Medicus sum — nōn deus. Aliquī mortem vincunt. Aliquī nōn.' "
        "Māter puerum tenet. Māter nōn flet. Māter: 'Quis nunc sum? Māter sum — sed fīlius nōn est.' "
        "Medicus mātrem spectat. Medicus: 'Māter manēs. Semper māter manēs. Fīlius mortuus — sed amor vīvit.'"
    )
}

STORIES["cap30_09"] = {
    "title_la": "Vigil in Turrī",
    "title_zh": "塔楼守望者",
    "target_chapter": 30, "theme": "13 孤独", "style": "日记",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "日记体",
    "text": (
        "Diēs CCL. In turrī sōlus sum. Mare spectō. Mare vacuum est. "
        "Diēs CCLI. Nāvis in marī! Nāvis parva est. Nāvis prope est. "
        "Diēs CCLII. Nāvis in portum nōn intrat. Nāvis abit. Nāvis nōn redit. "
        "Diēs CCLIII. Mare vacuum. Caelum vacuum. Animus vacuus. "
        "Diēs CCLIV. Nōn iam mare spectō. Nōn iam nāvēs exspectō. "
        "Ego turrim spectō. Ego mē ipsum spectō. Ego sum turris. Ego sum mare. "
        "Diēs CCLV. Nāvis appāret. Nāvis magna est. Nāvis ad portum nāvigat. "
        "Sed ego nōn iam ad portum currō. Ego in turrī sedeō. Ego exspectō — sed nōn spērō."
    )
}

STORIES["cap30_10"] = {
    "title_la": "Fīlius Quī Nōn Rediit",
    "title_zh": "未归的儿子",
    "target_chapter": 30, "theme": "25 家庭", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Māter ad portam stat. Māter viam spectat. Māter fīlium exspectat. "
        "Fīlius ad bellum abiit. Fīlius mātrem trīstem relīquit. "
        "'Māter, ego redībō. Māter, nōlī flēre.' Māter nōn flēvit — sed nōn rīsit. "
        "Multī annī trānseunt. Māter ad portam stat. Māter senēscit. "
        "Multī mīlitēs redeunt. Fīlius nōn redit. "
        "Māter: 'Fīlius meus mortuus est. Sed ego māter sum. Mātris amor nōn moritur.' "
        "Māter ad portam stat. Via vacua est. Māter tacet. "
        "Sed in corde, fīlius vīvit. In corde, fīlius semper redit."
    )
}

# === Cap.31: 需 7 篇 ===
STORIES["cap31_04"] = {
    "title_la": "Aedificātor et Ruīna",
    "title_zh": "建筑师与废墟",
    "target_chapter": 31, "theme": "35 城市", "style": "古典",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego aedificātor sum. Urbēs aedificō. Templa. Pontēs. Aquaeductūs. "
        "Opera mea magna sunt. Opera mea pulchra sunt. Opera mea — aeterna. "
        "Sed hodiē ruīnās videō. Hodiē opera mea frācta sunt. "
        "Bellum. Terrae mōtus. Ignis. Tempus. Quattuor hostēs. "
        "Ego: 'Cūr aedificāvī — sī omnia ruunt?' "
        "Lapis ruīnārum respondet: 'Aedificāre nōn est aeternum facere. Aedificāre est — amāre.'"
    )
}

STORIES["cap31_05"] = {
    "title_la": "Dēsertor",
    "title_zh": "逃兵",
    "target_chapter": 31, "theme": "09 勇气", "style": "冷峻",
    "genre": "F 战争与征服", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mīles in proeliō stat. Hostēs prope sunt. Mīles timet. "
        "Mīles gladium nōn tollit. Mīles fugit. Mīles in silvā latet. "
        "Post proelium, mīles castra quaerit. Castra vacua sunt. "
        "Commīlitōnēs mortuī sunt. Commīlitōnēs in proeliō cecidērunt. "
        "Mīles vīvit. Mīles sōlus vīvit. Cūr? Quia fugit. "
        "Mīles: 'Mors fortis est. Vīta ignāva est. Quid melius?' "
        "Mīles in silvam redit. Mīles nōn redit. Mīles nec vīvit — nec mortuus est."
    )
}

STORIES["cap31_06"] = {
    "title_la": "Senex et Puer sub Arbore",
    "title_zh": "树下的老人与男孩",
    "target_chapter": 31, "theme": "61 暮年与青春", "style": "抒情",
    "genre": "G 哲学寓言", "character_type": "老人", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Senex sub arbore sedet. Puer ad senem venit. "
        "Puer: 'Senex, quid facis sub arbore?' Senex: 'Nihil. Spectō.' "
        "Puer: 'Quid spectās?' Senex: 'Folia. Folia cadunt. Ūnum. Duo. Tria.' "
        "Puer: 'Folia semper cadunt. Cūr hoc spectās?' "
        "Senex: 'Quandō tū senex eris, puer, folia cadentia spectābis. "
        "Et intellegēs. Folia nōn cadunt — folia redeunt. In terram. In novam vītam.' "
        "Puer tacet. Puer folium cadēns spectat. Puer nōn intellegit — sed meminit."
    )
}

STORIES["cap31_07"] = {
    "title_la": "Aquaeductus",
    "title_zh": "水渠",
    "target_chapter": 31, "theme": "11 自然与文明", "style": "雄辩",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Aquaeductus per vallem ambulat. Aqua in eō fluit. Aqua ad urbem venit. "
        "In urbe, aqua in fontēs fluit. In urbe, aqua in balnea fluit. In urbe, aqua in domōs fluit. "
        "In monte, homō aquam spectat. Homō: 'Aqua nostra erat. Nunc aqua ad urbem fluit.' "
        "Fīlius: 'Pater, cūr aqua nōn nōbīs manet?' Pater: 'Urbs magna est. Urbs potēns est. Urbs aquam capit.' "
        "Fīlius: 'Nōs aquam nōn habēmus — sed urbs habet. Estne hoc iūstum?' "
        "Pater nōn respondet. Pater aquam flūentem spectat. Aqua tacet. Aqua semper tacet."
    )
}

STORIES["cap31_08"] = {
    "title_la": "Mulier in Forō",
    "title_zh": "广场上的女人",
    "target_chapter": 31, "theme": "37 性别与权力", "style": "冷峻",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mulier in forō stat. Forum virōrum est. Mulier in forō — rēs nova. "
        "Virī: 'Fēmina in forō! Quid facit? Fēminae domī esse dēbent!' "
        "Mulier: 'Virī meī frāter mortuus est. Virī meī pater mortuus est. "
        "Virī meī fīlius parvus est. Ego hīc stō — prō eīs.' "
        "Virī tacent. Virī mulierem spectant. "
        "Ūnus vir: 'Fēmina, loquere. Forum tuum est.' "
        "Mulier nōn loquitur. Mulier stat. Mulier tacet. "
        "Sed silentium eius — clāmor est."
    )
}

STORIES["cap31_09"] = {
    "title_la": "Piscātor et Stēlla",
    "title_zh": "渔夫与星",
    "target_chapter": 31, "theme": "18 自然", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Nocte in marī piscor. Stēllae in caelō sunt. Stēlla ūna in aquā cadit. "
        "Stēlla in aquā natat. Ego stēllam capere volō. "
        "Stēlla: 'Nōn mē capiēs. Ego nōn sum stēlla — ego sum imāgō.' "
        "Ego: 'Cuius imāgō?' Stēlla: 'Tua. Tū in aquam spectās. Tū tē ipsum vidēs.' "
        "Ego in aquam spectō. Ego faciem meam videō. Ego stēllam nōn videō. "
        "Stēlla abiit. Ego sōlus in marī sum. Ego sōlus sum — sed nōn tōtus."
    )
}

STORIES["cap31_10"] = {
    "title_la": "Iānua Clausa",
    "title_zh": "紧闭的门",
    "target_chapter": 31, "theme": "05 真理", "style": "精炼",
    "genre": "G 哲学寓言", "character_type": "学者", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Philosophus ad iānuam stat. Iānua clausa est. "
        "Philosophus pulsat. Nēmō aperit. Philosophus iterum pulsat. Nēmō. "
        "Philosophus: 'Aperī! Vēritātem quaerō!' Vōx ab intus: 'Vēritās nōn per iānuam intrat.' "
        "Philosophus: 'Quōmodo intrāre possum?' Vōx: 'Nōn intrās. Vēritās nōn est in domō. Vēritās est — via.' "
        "Philosophus ab iānuā discēdit. Philosophus viam spectat. Via longa est. "
        "Philosophus ambulat. Iānua post eum clausa manet. Sed philosophus nōn respicit."
    )
}

# === Cap.32: 需 3 篇 ===
STORIES["cap32_08"] = {
    "title_la": "Vīlicus et Dominus",
    "title_zh": "管家与主人",
    "target_chapter": 32, "theme": "58 主人与奴隶", "style": "冷峻",
    "genre": "C 历史与人物", "character_type": "奴隶", "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Vīlicus in vīllā labōrat. Dominus in urbe vīvit. Dominus numquam vīllam vīsitat. "
        "Vīlicus: 'Dominus nōn venit. Dominus nōn cūrat. Ego dominus sum.' "
        "Sed ūnō diē dominus venit. Dominus: 'Vīlicus, quid fēcistī? Vīlla ruīnā est!' "
        "Vīlicus: 'Domine, tū numquam vēnistī. Ego sōlus labōrāvī.' "
        "Dominus: 'Ego tē pūniō. Tū nōn bonus servus es.' "
        "Vīlicus: 'Ego servus sum — sed tū dominus. Quis nōn bonus est?' "
        "Dominus tacet. Dominus vīllam spectat. Dominus — nihil facit."
    )
}

STORIES["cap32_09"] = {
    "title_la": "Nox in Īnsulā",
    "title_zh": "岛上之夜",
    "target_chapter": 32, "theme": "13 孤独", "style": "抒情",
    "genre": "B 神话与传说", "character_type": "希腊人", "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Sōlus in īnsulā sum. Nēmō mēcum est. Nēmō mē quaerit. "
        "Īnsula parva est. Mare circum īnsulam magnum est. "
        "Nocte, stēllās spectō. Nocte, mare audiō. Nocte, taceō. "
        "Aliquandō nāvēs ad īnsulam nāvigant. Nāvēs numquam cōnsistunt. "
        "Nāvēs praeter eunt. Ego in rīpā stō. Ego manum tollō. "
        "Nautae mē nōn vident. Nautae nāvigant. Nautae abeunt. "
        "Ego: 'Nōn sum sōlus — sed sōlus videor.' Mare respondet: 'Omnēs sōlī sumus.'"
    )
}

STORIES["cap32_10"] = {
    "title_la": "Mīles et Fīlius Parvus",
    "title_zh": "士兵与幼子",
    "target_chapter": 32, "theme": "25 家庭", "style": "精炼",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mīles domum redit. Fīlius parvus ad iānuam stat. Fīlius patrem nōn cognōscit. "
        "Fīlius: 'Quis es tū?' Mīles: 'Pater tuus sum.' "
        "Fīlius: 'Pater meus mortuus est. Māter dīxit.' "
        "Mīles: 'Māter mentīta est. Pater tuus vīvit. Pater tuus — hīc est.' "
        "Fīlius patrem spectat. Fīlius oculōs patris videt. Fīlius: 'Oculī! Oculī tuī — meī sunt!' "
        "Mīles fīlium amplectitur. Mīles flet. Fīlius flet. "
        "Duo hominēs. Ūnus sanguis. Ūna domus."
    )
}

# === Cap.33: 需 9 篇 ===
STORIES["cap33_02"] = {
    "title_la": "Templum in Ruīnīs",
    "title_zh": "废墟中的神庙",
    "target_chapter": 33, "theme": "27 信仰与怀疑", "style": "古典",
    "genre": "B 神话与传说", "character_type": "希腊人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Templum in ruīnīs stat. Columnae frāctae sunt. Āra vacua est. Statuae dēlētae sunt. "
        "Sacerdōs sōlus in templō manet. Sacerdōs: 'Deī, ubi estis? Templum vestrum ruīnā est.' "
        "Deī nōn respondent. Sacerdōs in ārā ignem facit. Sacerdōs: 'Deī, sī nōn estis, ignis meus sōlus ārdet.' "
        "Ignis parvus est. Ignis in ārā ārdet. Sacerdōs ignem spectat. "
        "Sacerdōs: 'Sī deī nōn sunt — cūr ignis ārdet? Cūr ego ignem faciō?' "
        "Ignis respondet: 'Quia spēs manet. Quia spēs — deus ultimus.'"
    )
}

STORIES["cap33_03"] = {
    "title_la": "Eques et Puer",
    "title_zh": "骑士与男孩",
    "target_chapter": 33, "theme": "09 勇气", "style": "史诗",
    "genre": "F 战争与征服", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Eques in proelium equitat. Hastam tollit. Hostēs videt. Eques nōn timet. "
        "Puer in viā stat. Puer equitem spectat. Puer: 'Eques, cūr nōn timēs?' "
        "Eques: 'Mors omnibus venit. Sī hodiē, sī crās — quid interest?' "
        "Puer: 'Interest. Tū mortuus — nōn vidēbis. Tū mortuus — nōn amābis.' "
        "Eques puerum spectat. Eques hastam dēmittit. Eques: 'Quis es tū, puer?' "
        "Puer: 'Fīlius tuus sum — quem numquam vīdistī.' "
        "Eques ab equō dēscendit. Eques puerum amplectitur. Proelium — procul."
    )
}

STORIES["cap33_04"] = {
    "title_la": "Nāvis et Procella",
    "title_zh": "船与暴风雨",
    "target_chapter": 33, "theme": "84 偶然与命运", "style": "雄辩",
    "genre": "B 神话与传说", "character_type": "商人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Procella in marī oritur. Ventus magnus flat. Undae altae sunt. Nāvis in perīculō est. "
        "Nautae deōs invocant. Nautae: 'Neptūne, servā nōs! Ventōs, tacetē! Mare, placidum fī!' "
        "Gubernātor: 'Deī nōn nōs audiunt. Ventus nōs nōn audit. Mare nōs nōn audit. "
        "Nōs nōbīs ipsīs servāre dēbēmus.' "
        "Nautae: 'Quōmodo? Procella nōs superat!' Gubernātor: 'Nōn superāmus — nāvigāmus.' "
        "Nāvis per procellam nāvigat. Nāvis nōn frangitur. Nāvis in portum intrat. "
        "Nautae: 'Deī nōs servāvērunt!' Gubernātor: 'Nōn deī — nōs ipsī.'"
    )
}

STORIES["cap33_05"] = {
    "title_la": "Canticum Captīvī",
    "title_zh": "囚徒之歌",
    "target_chapter": 33, "theme": "03 自由与束缚", "style": "抒情",
    "genre": "M 伦理与习俗", "character_type": "非罗马的古代人", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "In carcere cantō. Nēmō mē audit. Nēmō cantum meum audit. "
        "Canticum meum nōn est pulchrum. Canticum meum nōn est laetum. "
        "Canticum meum est — vērum. In cantō, omnia dīcō. In cantō, ego sum. "
        "Custōdēs veniunt. Custōdēs: 'Tacē! In carcere nōn cantātur!' "
        "Ego: 'In carcere minus quam usquam cantātur — sed ego cantō. "
        "Corpus meum in carcere est — sed anima mea in cantū est.' "
        "Custōdēs tacent. Custōdēs abeunt. Ego cantō. Ego semper cantō."
    )
}

STORIES["cap33_06"] = {
    "title_la": "Hortulānus et Imperātor",
    "title_zh": "园丁与皇帝",
    "target_chapter": 33, "theme": "06 权力", "style": "戏谑",
    "genre": "D 讽刺", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Imperātor in hortum intrat. Hortulānus rosās colit. "
        "Imperātor: 'Hortulāne, ego imperātor sum. Ego urbēs et rēgna regō. Tū quid regis?' "
        "Hortulānus: 'Ego hortum regō, domine. Ego rosās et līlia regō.' "
        "Imperātor: 'Hortus parvus est. Imperium meum magnum est.' "
        "Hortulānus: 'Domine, in imperiō tuō, hominēs nōn pārent. In hortō meō, rosae pārent.' "
        "Imperātor: 'Rosae nōn loquuntur. Rosae nōn resistunt.' "
        "Hortulānus: 'Domine, neque subditī tuī — sī tū eōs ut rosās colis.' "
        "Imperātor tacet. Imperātor rosam spectat. Imperātor — rosam nōn intelligit."
    )
}

STORIES["cap33_07"] = {
    "title_la": "Faber et Fīlia",
    "title_zh": "工匠与女儿",
    "target_chapter": 33, "theme": "25 家庭", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Faber in officīnā labōrat. Fīlia parva in officīnam intrat. "
        "Fīlia: 'Pater, quid facis?' Faber: 'Mēnsam faciō. Mēnsa pulchra erit.' "
        "Fīlia: 'Pater, cūr semper labōrās? Cūr numquam mēcum lūdis?' "
        "Faber labōrem sistit. Faber fīliam spectat. Faber: 'Labōrō ut tū nōn labōrēs. Labōrō ut tū lūdās.' "
        "Fīlia: 'Sed ego tēcum lūdere volō — nōn sōla.' "
        "Faber tacet. Faber mēnsam nōn facit. Faber fīliam in hortum dūcit. "
        "Faber cum fīliā lūdit. Hodiē, mēnsa nōn facta est. Hodiē, fīlia laeta est."
    )
}

STORIES["cap33_08"] = {
    "title_la": "Senex et Umbra Sua",
    "title_zh": "老人与影子",
    "target_chapter": 33, "theme": "61 暮年与青春", "style": "精炼",
    "genre": "G 哲学寓言", "character_type": "老人", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Senex in sōle sedet. Umbra in terrā iacet. "
        "Senex: 'Umbra, tū mē semper sequeris. Quandō tū mē relinquēs?' "
        "Umbra: 'Quandō tū mē relinquēs, senex. Quandō sōl nōn lūcēbit.' "
        "Senex: 'Sōl semper lūcet. Sōl numquam mē relinquit. Sed sōl quoque senēscit.' "
        "Umbra: 'Sōl nōn senēscit — sed oculī tuī. Sōl idem est — sed tū nōn idem.' "
        "Senex: 'Quid erit quandō ego nōn erō? Umbra mea — manēbit?' "
        "Umbra: 'Umbra tua in terrā manēbit. Sed nēmō eam vidēbit. Quia nēmō tē vidēbit.'"
    )
}

STORIES["cap33_09"] = {
    "title_la": "Nūntius ex Monte",
    "title_zh": "山中来信",
    "target_chapter": 33, "theme": "19 希望", "style": "书信",
    "genre": "C 历史与人物", "character_type": "旅人", "length_tier": "长篇",
    "narrative_mode": "书信体",
    "text": (
        "Amīcīs in valle salūtem. Ex monte scrībō. Hīc aër tenuis est. Hīc caelum prope. "
        "Nūbēs sub pedibus meīs sunt. Avēs sub mē volant. "
        "Vōs in valle multa habētis. Domōs. Forum. Balnea. Turbam. "
        "Ego in monte nihil habeō — sed omnia videō. "
        "In valle, hominēs sē nōn vident. In valle, hominēs in turba sōlī sunt. "
        "In monte, ego sōlus sum — sed nōn sōlus. Hīc, ego sum. Hīc, ego mē videō. "
        "Valēte. Quandō ad vallem redībō — nesciō. Quandō ego — sciō."
    )
}

STORIES["cap33_10"] = {
    "title_la": "Mulier Quae Pugnāvit",
    "title_zh": "战斗的女人",
    "target_chapter": 33, "theme": "37 性别与权力", "style": "史诗",
    "genre": "C 历史与人物", "character_type": "非罗马的古代人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mulier in proelium intrat. Virī mulierem rīdent. 'Fēmina in proeliō! Quid faciet?' "
        "Mulier gladium tollit. Mulier clāmat. Mulier in hostēs currit. "
        "Virī tacent. Virī mulierem spectant. Mulier pugnat ut leō. Mulier nōn timet. "
        "Post proelium, virī ad mulierem veniunt. Virī: 'Quis es tū?' "
        "Mulier: 'Mulier sum. Soror. Māter. Fīlia. Quam virī occīdērunt. Quam virī nōn prōtēxērunt.' "
        "Virī tacent. Virī caput dēmittunt. Mulier gladium in terram fīgit. "
        "Mulier: 'Nōn volō proelium. Volō pācem. Sed pāx nōn venit — sī nōn pugnāmus.'"
    )
}

# === Cap.34: 需 8 篇 ===
STORIES["cap34_03"] = {
    "title_la": "Historia Sine Verbīs",
    "title_zh": "无言的历史",
    "target_chapter": 34, "theme": "08 记忆", "style": "冷峻",
    "genre": "C 历史与人物", "character_type": "学者", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Scrība in tabulāriō sedet. Multī librī circum eum sunt. "
        "Scrība: 'Omnēs historiae hīc sunt. Omnēs vōcēs scrīptae. Omnēs mortuī — nōn mortuī.' "
        "Sed ūnus liber nōn est. Ūna historia dēest. Historia mulierum. Historia servōrum. Historia pauperum. "
        "Scrība: 'Cūr haec historia nōn est? Quis eam scrībere nōn voluit?' "
        "Umbrae in tabulāriō: 'Nōs scrībere nōn potuimus. Nōs litterās nōn habuimus. "
        "Nōs vōcēs nōn habuimus. Sed nōs — vīximus.' "
        "Scrība calamum tollit. Scrība: 'Ego scrībam. Ego vōcēs vestrās scrībam.' "
        "Umbrae tacent. Umbrae exspectant. Historia — nāscitur."
    )
}

STORIES["cap34_04"] = {
    "title_la": "Aenigma Sphingis",
    "title_zh": "斯芬克斯之谜",
    "target_chapter": 34, "theme": "12 知识", "style": "古典",
    "genre": "B 神话与传说", "character_type": "希腊人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Sphinx in monte sedet. Sphinx aenigma viātōribus dat. "
        "Sphinx: 'Quid māne quattuor pedibus, merīdiē duōbus, vesperī tribus ambulat?' "
        "Multī viātōrēs aenigma nōn solvunt. Multī viātōrēs moriuntur. "
        "Oedipus ad Sphingem venit. Oedipus: 'Homo est. Māne — īnfāns. Merīdiē — adultus. Vesperī — senex.' "
        "Sphinx: 'Vērum est. Homo est.' Sphinx sē interficit. "
        "Oedipus in urbem intrat. Oedipus victor est. Sed Oedipus nescit — "
        "aenigma nōn est solūtum. Aenigma vērum — ipse est."
    )
}

STORIES["cap34_05"] = {
    "title_la": "Portus Ultimus",
    "title_zh": "最后的港口",
    "target_chapter": 34, "theme": "01 生死", "style": "抒情",
    "genre": "G 哲学寓言", "character_type": "旅人", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ad portum ultimum nāvigō. Post mē — multa maria. Post mē — multae procellae. "
        "Post mē — multī portūs. Sed hīc — portus ultimus. "
        "In portū, nāvis mea cōnsistit. In portū, ventus tacet. "
        "In portū, nēmō mē exspectat. Nēmō mē salūtat. Nēmō mē cognōscit. "
        "Ego nōn sum nauta. Ego nōn sum viātor. Ego sum — quī vēnī. "
        "Portus ultimus nōn est fīnis. Portus ultimus est — initium. "
        "Sed cuius initium? Hoc — nesciō. Hoc — sciam."
    )
}

STORIES["cap34_06"] = {
    "title_la": "Tabernārius Sapiēns",
    "title_zh": "智慧的店主",
    "target_chapter": 34, "theme": "17 智慧", "style": "白话",
    "genre": "G 哲学寓言", "character_type": "商人", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Tabernārius in tabernā sedet. Philosophus in tabernam intrat. "
        "Philosophus: 'Tabernārie, vīnum vēndis?' Tabernārius: 'Vīnum vēndō. Et sapientiam.' "
        "Philosophus: 'Sapientiam? In tabernā?' Tabernārius: 'Ubīque sapientia est — sī sapis.' "
        "Philosophus: 'Dīc mihi sapientiam tuam.' "
        "Tabernārius: 'Prīmum: omnēs hominēs vīnum volunt — sed nōn omnēs vīnum ferre possunt. "
        "Secundum: quī plūs bibunt, minus habent. Tertium: optimum vīnum nōn est quod plūrimī emunt — "
        "sed quod tū amās.' Philosophus tacet. Philosophus vīnum bibit. "
        "Philosophus: 'Hoc vīnum bonum est — et sapientia tua quoque.'"
    )
}

STORIES["cap34_07"] = {
    "title_la": "Vīlicus Novus",
    "title_zh": "新管家",
    "target_chapter": 34, "theme": "06 权力", "style": "冷峻",
    "genre": "C 历史与人物", "character_type": "奴隶", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vīlicus novus in vīllam venit. Dominus eum mīsit. Servī eum spectant. "
        "Vīlicus: 'Ego vīlicus sum. Dominus mē mīsit. Ego vōbīs imperō.' "
        "Servī tacent. Servī labōrant. Servī pārent. "
        "Sed nocte, servī in culīnā congregantur. Servī: 'Vīlicus novus — servus est. Sīcut nōs.' "
        "Servus vetus: 'Ūnus ex nōbīs — sed contrā nōs. Hoc dominus facit. Dīvide et imperā.' "
        "Vīlicus in umbrā stat. Vīlicus audit. Vīlicus: 'Ego servus sum — sed nōn sum vōbīs. "
        "Ego vōbīs imperō — sed nōn sum līber. Quis miser est?'"
    )
}

STORIES["cap34_08"] = {
    "title_la": "Fōns in Dēsertō",
    "title_zh": "沙漠中的泉水",
    "target_chapter": 34, "theme": "18 自然", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "旅人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "In mediō dēsertō, fōns est. Fōns parvus est. Fōns aquam clāram dat. "
        "Palmae circum fontem sunt. Umbra sub palmīs est. "
        "Viātōrēs ad fontem veniunt. Viātōrēs aquam bibunt. Viātōrēs in umbrā quiēscunt. "
        "Ūnus viātor: 'Quis hunc fontem fōdit? Quis hās palmās plantāvit?' "
        "Nēmō respondet. Nēmō scit. "
        "Fontis dōnum sine nōmine est. Fontis amor sine mercēde est. "
        "Fōns: 'Nōn quaerō quis mē fōdit. Nōn quaerō quis mē bibit. Ego sōlum — dō.'"
    )
}

STORIES["cap34_09"] = {
    "title_la": "Gladiātor et Fīlius",
    "title_zh": "角斗士与儿子",
    "target_chapter": 34, "theme": "30 威严与慈爱", "style": "精炼",
    "genre": "M 伦理与习俗", "character_type": "奴隶", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Gladiātor in arēnā stat. Fīlius parvus in spectāculīs sedet. "
        "Fīlius: 'Pater! Pater meus gladiātor est! Pater meus fortis est!' "
        "Gladiātor fīlium audit. Gladiātor fīlium nōn spectat. Gladiātor hostem spectat. "
        "Gladiātor: 'Prō fīliō meō pugnō. Prō fīliō meō vīvō. Prō fīliō meō — morī possum.' "
        "Gladiātor hostem vincit. Gladiātor vīvit. Fīlius clāmat: 'Pater! Pater vīcit!' "
        "Sed gladiātor nōn est laetus. Gladiātor: 'Fīlius meus gladiātōrem laudat. "
        "Fīlius meus gladiātor fierī vult. Hoc est — victōria mea? An clādēs?'"
    )
}

STORIES["cap34_10"] = {
    "title_la": "Nūbēs et Mons",
    "title_zh": "云与山",
    "target_chapter": 34, "theme": "11 自然与文明", "style": "修辞",
    "genre": "B 神话与传说", "character_type": "拟人自然", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Nūbēs ad montem venit. Nūbēs: 'Mons, tū semper hīc es. Ego semper movē. Cūr?' "
        "Mons: 'Ego hīc nātus sum. Ego hīc moriar. Tū — venīs et abīs.' "
        "Nūbēs: 'Ego multa videō. Maria. Urbēs. Flūmina. Tū — nihil vidēs.' "
        "Mons: 'Ego omnia videō — in tē. Quandō tū venīs, tū mihi narrās. "
        "Tū es oculus meus. Ego sum rādīx tua.' "
        "Nūbēs tacet. Nūbēs montem amplectitur. Nūbēs pluit. "
        "Mons aquam bibit. Flōrēs in monte nāscuntur. Duo — ūnum."
    )
}

# === Cap.35: 需 8 篇 ===
STORIES["cap35_03"] = {
    "title_la": "Nāvis et Sīrēnēs",
    "title_zh": "船与塞壬",
    "target_chapter": 35, "theme": "22 旅程", "style": "史诗",
    "genre": "B 神话与传说", "character_type": "希腊人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Nāvis Ulixis per mare nāvigat. Sīrēnēs in īnsulā cantant. "
        "Cantus Sīrēnum pulcher est. Nautae cantum audiunt. Nautae ad īnsulam nāvigāre volunt. "
        "Ulixēs: 'Nōlīte audīre! Cantus vōs necābit! Aurēs vestrās cērā claudite!' "
        "Nautae aurēs cērā claudunt. Nautae cantum nōn audiunt. Nautae nāvigant. "
        "Sed Ulixēs aurēs nōn claudit. Ulixēs cantum audīre vult. "
        "Ulixēs ad mālum sē ligat. Ulixēs: 'Cantum audīre volō — sed morī nōn volō.' "
        "Sīrēnēs cantant. Ulixēs audit. Cantus eum vocat. Ulixēs ad īnsulam īre vult. "
        "Sed vincula eum tenent. Nāvis praeterit. Cantus abest. Ulixēs vīvit — sed cantus semper in memoriā."
    )
}

STORIES["cap35_04"] = {
    "title_la": "Mulier et Lēx",
    "title_zh": "女人与法律",
    "target_chapter": 35, "theme": "49 法律与道德", "style": "雄辩",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Mulier in forō stat. Lēx in tabulā scrīpta est. Lēx: 'Fēmina nihil possidet.' "
        "Mulier: 'Lēx, tū mē nihil habēre dīcis. Sed ego corpus meum habeō. Ego mentem meam habeō. "
        "Ego lībertātem meam habeō — quam tū nōn dedistī et quam tū nōn aufērs.' "
        "Iūdex: 'Lēx est lēx. Fēmina nihil possidet.' "
        "Mulier: 'Lēx scrīpta est — sed iūstitia nōn est scrīpta. Iūstitia in corde est. "
        "Sī lēx iūstitiam nōn servat — lēx nōn est lēx.' "
        "Iūdex tacet. Iūdex mulierem spectat. Iūdex: 'Tū lēgem nōn frangis — sed lēgem interrogās. "
        "Hoc est perīculōsum.' Mulier: 'Hoc est necessārium.'"
    )
}

STORIES["cap35_05"] = {
    "title_la": "Fīlius Quī Nōn Crēdidit",
    "title_zh": "不信的儿子",
    "target_chapter": 35, "theme": "27 信仰与怀疑", "style": "冷峻",
    "genre": "K 宗教", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pater in templō deōs laudat. Fīlius in templō tacet. "
        "Pater: 'Fīlī, cūr nōn laudās? Deī omnipotentēs sunt.' "
        "Fīlius: 'Sī deī omnipotentēs sunt, cūr māter mortua est? Cūr bellum est? Cūr famēs?' "
        "Pater: 'Deī nōs probant. Deī nōs docent.' "
        "Fīlius: 'Quid docent? Dolōrem? Mortem? Silentium?' "
        "Pater: 'Fīlī, sine deīs — quis nōs servat?' "
        "Fīlius: 'Nōs ipsī. Nōs nōs ipsōs servāmus. Nōn deī — sed hominēs.' "
        "Pater fīlium spectat. Pater: 'Fortasse vērum dīcis. Sed sine deīs — ego nōn possum.' "
        "Fīlius: 'Ego possum — sed tē nōn iūdicō.'"
    )
}

STORIES["cap35_06"] = {
    "title_la": "Ānserēs Capitōliī",
    "title_zh": "卡皮托利尼的鹅",
    "target_chapter": 35, "theme": "35 城市", "style": "古典",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Galli Rōmam obsident. Nocte, Gallī Capitōlium ascendunt. "
        "Canēs dormiunt. Canēs nihil sentiunt. Sed ānserēs clāmant. "
        "Ānserēs excitantur. Ānserēs Mānlium excitant. Mānlius surgit. Mānlius Gallōs videt. "
        "Mānlius: 'Ad arma! Gallī adsunt! Rōma in perīculō est!' "
        "Rōmānī Gallōs repellunt. Capitōlium servātur. Rōma servātur. "
        "Posteā, Rōmānī dīcunt: 'Ānserēs Rōmam servāvērunt.' "
        "Sed ānserēs nōn intellegunt glōriam. Ānserēs sōlum clāmāvērunt — quia ānserēs erant."
    )
}

STORIES["cap35_07"] = {
    "title_la": "Puella Quae Librōs Amāvit",
    "title_zh": "爱书的女孩",
    "target_chapter": 35, "theme": "28 教育", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puella parvula in bibliothēcā sedet. Pater bibliothēcam habet. "
        "Puella librōs spectat. Puella: 'Pater, quid in librīs scrīptum est?' "
        "Pater: 'Multa. Historiam. Philosophiam. Poēsim.' "
        "Puella: 'Possumne legere?' Pater: 'Fēminae nōn legunt, fīlia mea.' "
        "Puella tacet — sed nocte, puella in bibliothēcam redit. Puella lūmen accendit. "
        "Puella legit. Puella multa discit. Puella multa intellegit. "
        "Multīs annīs post, puella fēmina est. Fēmina librōs scrībit. "
        "Fēmina: 'Pater, fēminae nōn legunt — sed fēminae scrībunt.'"
    )
}

STORIES["cap35_08"] = {
    "title_la": "Custōs Portae",
    "title_zh": "守门人",
    "target_chapter": 35, "theme": "75 服从与反抗", "style": "冷峻",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego custōs portae sum. Omnēs per portam intrant. Omnēs per portam exeunt. "
        "Ego omnēs videō. Ego nēminem iūdicō. Ego portam aperiō. Ego portam claudō. "
        "Herī, vir per portam intrāvit. Vir: 'Custōs, cūr portam servās? Cūr nōn fugis?' "
        "Ego: 'Quō fugerem? Hīc est portus meus. Hīc est via mea.' "
        "Vir: 'Tū est custōs portae — sed tū quoque captīvus es.' "
        "Ego: 'Omnēs custōdēs captīvī sunt. Omnēs portae portās custōdiunt.' "
        "Vir abiit. Porta aperta manet. Ego portam nōn claudō — hodiē."
    )
}

STORIES["cap35_09"] = {
    "title_la": "Mercātor et Pīrāta",
    "title_zh": "商人与海盗",
    "target_chapter": 35, "theme": "04 富与贫", "style": "白话",
    "genre": "C 历史与人物", "character_type": "商人", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Mercātor dīves in marī nāvigat. Pīrātae nāvem eius capiunt. "
        "Pīrāta: 'Pecūniam tuam nōbīs dā — aut morieris!' "
        "Mercātor: 'Pecūniam nōn habeō in nāvī. Omnis pecūnia in terrā est.' "
        "Pīrāta: 'Mentīris! Dīvitēs semper mentiuntur!' "
        "Mercātor: 'Vērum dīcō. Dīvitiae meae nōn sunt in nāvī — sed in terrā. "
        "In terrā, ego dīves sum. In marī, ego pauper sum — sīcut tū.' "
        "Pīrāta tacet. Pīrāta mercātōrem spectat. "
        "Pīrāta: 'In marī, omnēs pauperēs sumus. In marī, nōs aequālēs sumus.' "
        "Pīrāta mercātōrem nōn necat. Pīrāta mercātōrem in terrā relinquit. "
        "In terrā, mercātor dīves est. Pīrāta — in marī."
    )
}

STORIES["cap35_10"] = {
    "title_la": "Vōx ex Monte",
    "title_zh": "山中之声",
    "target_chapter": 35, "theme": "05 真理", "style": "修辞",
    "genre": "G 哲学寓言", "character_type": "旅人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vōx ex monte loquitur. Vōx: 'Quī mē audit, sapiēns fit. Quī mē sequitur, vērum invenit.' "
        "Multī hominēs vōcem audiunt. Multī hominēs in montem ascendunt. "
        "In monte, nihil est. Nēmō. Nihil. Vacuum. "
        "Hominēs: 'Vōx, ubi es? Vōx, cūr nōs fallis?' "
        "Vōx: 'Ego nōn fallō. Ego vōs dūcō. In monte, nihil est — sed vōs ascendistis. "
        "In ascēnsū, vōs vōs invēnistis. In ascēnsū, vōs sapiēntēs factī estis.' "
        "Hominēs tacent. Hominēs dē montem dēscendunt. Hominēs — aliī."
    )
}

# === Cap.42: 需 9 篇 ===
STORIES["cap42_02"] = {
    "title_la": "Magister et Discipulus",
    "title_zh": "师与徒",
    "target_chapter": 42, "theme": "28 教育", "style": "古典",
    "genre": "G 哲学寓言", "character_type": "学者", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Magister: 'Discipule, quid hodiē didicistī?' Discipulus: 'Nihil, magister.' "
        "Magister: 'Nihil? Tōtum diem in bibliothēcā fuistī.' "
        "Discipulus: 'Lēgī. Sed omnia quae lēgī, iam sciēbam.' "
        "Magister: 'Tū omnia scīs?' Discipulus: 'Sīc putō.' "
        "Magister tacet. Magister discipulum in hortum dūcit. "
        "Magister: 'Dīc mihi, quid vidēs?' Discipulus: 'Arborēs. Flōrēs. Avēs.' "
        "Magister: 'Arborēs et flōrēs et avēs — in librīs tuīs sunt? Discipule, librī nōn sunt sapientia. "
        "Librī sunt iānuae. Tū per iānuam intrāre dēbēs.'"
    )
}

STORIES["cap42_03"] = {
    "title_la": "Exsul in Urbe",
    "title_zh": "城中的流放者",
    "target_chapter": 42, "theme": "45 迁徙与流放", "style": "抒情",
    "genre": "C 历史与人物", "character_type": "非罗马的古代人", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "In urbe magnā habitō. Urbs pulchra est. Urbs dīves est. Sed urbs nōn est mea. "
        "Ego exsul sum. Ego ab meā terrā pulsus sum. Patriam meam nōn vidēbō. "
        "In urbe, omnēs mē spectant — sed nēmō mē videt. "
        "In urbe, linguam loquor — sed nēmō intellegit. "
        "Nocte, sōlus in cubiculō sedeō. Oculōs claudō. Patriam videō. "
        "Patria mea nōn est locus. Patria mea est memoria. Patria mea est — ego."
    )
}

STORIES["cap42_04"] = {
    "title_la": "Vātēs in Dēsertō",
    "title_zh": "沙漠中的先知",
    "target_chapter": 42, "theme": "29 信仰", "style": "雄辩",
    "genre": "K 宗教", "character_type": "非罗马的古代人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vātēs in dēsertō vīvit. Vātēs cum deō loquitur. Vātēs: 'Deus, quid mē vīs facere?' "
        "Deus: 'Ad urbem ī. Verbum meum dīc.' "
        "Vātēs: 'Populus nōn audiet. Populus mē rīdēbit. Populus mē lapidābit.' "
        "Deus: 'Tū verbum dīc. Populus audiat — aut nōn. Hoc nōn est tuum.' "
        "Vātēs ad urbem it. Vātēs verbum dīcit. Populus audit. Populus nōn rīdet. "
        "Populus: 'Vātēs, verbum tuum dūrum est. Sed vērum est. Quid facere dēbēmus?' "
        "Vātēs: 'Hoc nōn est meum. Deus dīxit — ego dīxī. Vōs — facite.'"
    )
}

STORIES["cap42_05"] = {
    "title_la": "Lupa et Puerī",
    "title_zh": "母狼与男孩们",
    "target_chapter": 42, "theme": "35 城市", "style": "史诗",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duo puerī ad flūmen iacent. Puerī parvī sunt. Puerī sōlī sunt. "
        "Lupa ad flūmen venit. Lupa puerōs videt. Lupa puerōs nōn dēvorat. Lupa puerōs alit. "
        "Lupa: 'Puerī, ego nōn māter vestra sum. Sed ego vōs servābō.' "
        "Pāstor Faustulus lupam videt. Pāstor puerōs invenit. Pāstor puerōs ad casam dūcit. "
        "Puerī Rōmulus et Remus sunt. Puerī urbem condent. Puerī Rōmam aedificābunt. "
        "Sed prius — lupa. Prius — amor sine verbīs. Prius — māter quae nōn māter erat."
    )
}

STORIES["cap42_06"] = {
    "title_la": "Cūria et Nox",
    "title_zh": "元老院与夜",
    "target_chapter": 42, "theme": "06 权力", "style": "冷峻",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Cūria nocte vacua est. Senātōrēs domī sunt. Senātōrēs dormiunt. "
        "Sed in cūriā, umbrae manent. Umbrae senātōrum mortuōrum. "
        "Umbra: 'Cūria eadem est. Sellae eaedem. Verba eadem. Nihil mūtātum est.' "
        "Altera umbra: 'Nōs vīximus. Nōs pugnāvimus. Nōs mortuī sumus. Et nihil mūtātum. Cūr?' "
        "Tertia umbra: 'Quia nōs mūtāre nōluimus. Quia nōs potestātem amāvimus — nōn rem pūblicam.' "
        "Māne, senātōrēs in cūriam intrant. Senātōrēs umbrās nōn vident. "
        "Senātōrēs in sellīs sedent. Senātōrēs verba eadem dīcunt. Nihil mūtātum."
    )
}

STORIES["cap42_07"] = {
    "title_la": "Agricola et Stēllae",
    "title_zh": "农夫与星辰",
    "target_chapter": 42, "theme": "18 自然", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Agricola sum. Nocte in campō sedeō. Stēllās spectō. "
        "Stēllae mihi dīcunt quandō serere, quandō metere dēbeō. "
        "Stēllae sunt librī meī. Stēllae sunt magistrī meī. "
        "Urbānī in urbe nōn stēllās vident. Urbānī in urbe sōlum mūrōs vident. "
        "Ego in campō — omnia videō. Caelum. Terram. Sēmen. Messem. "
        "Stēllae: 'Agricola, tū nōs spectās. Tū nōs intellegis. Tū nōn sōlus es.' "
        "Ego: 'Stēllae, vōs mē dūcitis. Vōs mihi viam mōnstrātis. Grātiās.'"
    )
}

STORIES["cap42_08"] = {
    "title_la": "Pīrāta et Philosophus",
    "title_zh": "海盗与哲学家",
    "target_chapter": 42, "theme": "03 自由与束缚", "style": "戏谑",
    "genre": "D 讽刺", "character_type": "学者", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Pīrātae philosophum capiunt. Pīrātae philosophum in forō vēndere volunt. "
        "Pīrāta: 'Philosophus, quid vēndis? Dīc mihi — ut tē melius vēndere possīmus.' "
        "Philosophus: 'Sapientiam vēndō. Sed nōn potes eam capere — nōn potes eam vēndere.' "
        "Pīrāta: 'Sapientia nōn est pecūnia. Sapientia nōn est cibus.' "
        "Philosophus: 'Vērum. Sed pecūnia et cibus sine sapientiā — quid prōsunt?' "
        "Pīrāta: 'Ego dīves sum. Ego nihil timeō.' "
        "Philosophus: 'Tū timēs. Tū mortem timēs. Tū captīvitātem timēs. Tū pīrāta es — sed nōn līber.' "
        "Pīrāta tacet. Pīrāta philosophum nōn vēndit. Pīrāta philosophum līberat. "
        "Pīrāta: 'Nunc — quis captīvus est?'"
    )
}

STORIES["cap42_09"] = {
    "title_la": "Māter et Fīlius in Bellō",
    "title_zh": "战火中的母子",
    "target_chapter": 42, "theme": "25 家庭", "style": "精炼",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Bellum in urbe est. Māter fīlium in bracchiīs tenet. Māter per urbem currit. "
        "Mīlitēs ubīque sunt. Ignis ubīque est. Clāmor ubīque est. "
        "Māter: 'Fīlī, nōlī timēre. Māter tēcum est. Māter tē servābit.' "
        "Fīlius nōn flet. Fīlius oculōs mātris spectat. "
        "Māter ad portam currit. Porta aperta est. Māter per portam exit. "
        "Post mūrōs, silentium. Post mūrōs, campī. Post mūrōs, pāx. "
        "Māter fīlium in terram pōnit. Māter: 'Fīlī, vīvimus. Fīlī, līberī sumus.' "
        "Fīlius: 'Māter, tū mē servāvistī. Quis tē servāvit?' Māter tacet. Māter rīdet."
    )
}

STORIES["cap42_10"] = {
    "title_la": "Senex sub Ponte",
    "title_zh": "桥下的老人",
    "target_chapter": 42, "theme": "65 安居与流离", "style": "冷峻",
    "genre": "M 伦理与习俗", "character_type": "乞丐", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Senex sub ponte habitat. Senex nūllam domum habet. Senex nūllum lectum habet. "
        "Senex super terram dormit. Senex sub caelō vīvit. "
        "Dīves vir per pontem ambulat. Dīves: 'Senex, cūr sub ponte habitās? Cūr domum nōn habēs?' "
        "Senex: 'Domum habēbam. Uxōrem habēbam. Fīliōs habēbam. Omnia perdidī.' "
        "Dīves: 'Quōmodo omnia perdidistī?' Senex: 'Bellum. Morbus. Ignis. Fātum.' "
        "Dīves: 'Nummōs tibi dō. Domum tibi eme.' "
        "Senex nummōs spectat. Senex: 'Domum emere possum — sed vītam nōn possum.' "
        "Senex nummōs in flūmen iactat. Dīves: 'Cūr?' Senex: 'Līber sum.'"
    )
}

# === Cap.46: 需 9 篇 ===
STORIES["cap46_02"] = {
    "title_la": "Philosophus et Mors",
    "title_zh": "哲学家与死神",
    "target_chapter": 46, "theme": "01 生死", "style": "古典",
    "genre": "G 哲学寓言", "character_type": "学者", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Mors ad philosophum venit. Mors: 'Philosophus, tempus tuum vēnit. Venī mēcum.' "
        "Philosophus: 'Mors, tōtam vītam tē exspectāvī. Tōtam vītam dē tē cōgitāvī. "
        "Nunc quandō tū vēnistī — nōn timeō.' "
        "Mors: 'Multī hominēs timent. Multī flent. Multī pugnant. Tū — nōn pugnās?' "
        "Philosophus: 'Pugnāre contrā mortem est pugnāre contrā nātūram. "
        "Ego philosophus sum. Ego nātūram intellegō. Ego mortem — amplexor.' "
        "Mors: 'Tū prīmus es quī mē nōn timet. Tū prīmus es quī mē — salūtat.' "
        "Philosophus cum Morte ambulat. Philosophus nōn respicit."
    )
}

STORIES["cap46_03"] = {
    "title_la": "Mulier et Ventus",
    "title_zh": "女人与风",
    "target_chapter": 46, "theme": "18 自然", "style": "抒情",
    "genre": "B 神话与传说", "character_type": "拟人自然", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Mulier in monte stat. Ventus in capillīs eius flat. "
        "Mulier: 'Ventus, tū ubīque es. Tū omnia tangis. Tū omnia movēs. Sed tū — nōn vidēris.' "
        "Ventus: 'Ego sum quod nōn vidētur — sed sentītur. Ego sum spiritus mundī.' "
        "Mulier: 'Ventus, portā mē. Portā mē ad locum ubi dolor nōn est.' "
        "Ventus: 'Nōn possum tē portāre — sed possum tēcum manēre. "
        "Quandō tū flēs, ego lacrimās tuās siccō. Quandō tū rīdēs, ego rīsum tuum portō.' "
        "Mulier tacet. Mulier ventum sentit. Mulier: 'Nōn sum sōla.'"
    )
}

STORIES["cap46_04"] = {
    "title_la": "Rēx et Somnium",
    "title_zh": "国王与梦",
    "target_chapter": 46, "theme": "72 想象与现实", "style": "意识流",
    "genre": "J 心理与梦境", "character_type": "非罗马的古代人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rēx in lectō dormit. Rēx somnium videt. In somniō, rēx nōn est rēx. "
        "In somniō, rēx pauper est. Rēx in campō labōrat. Rēx sub sōle sūdat. "
        "Rēx: 'Cūr ego hīc sum? Ego rēx sum!' Sed in somniō, vōx nōn auditur. "
        "Rēx excitātur. Rēx in lectō suō est. Rēx rēx est. Sed rēx nōn est laetus. "
        "Rēx: 'In somniō, ego pauper eram — sed ego vīvēbam. In vītā, ego rēx sum — sed ego nōn vīvō.' "
        "Rēx oculōs claudit. Rēx ad somnium redīre vult. Sed somnium nōn redit."
    )
}

STORIES["cap46_05"] = {
    "title_la": "Servus et Fīlius Dominī",
    "title_zh": "奴隶与主人之子",
    "target_chapter": 46, "theme": "58 主人与奴隶", "style": "冷峻",
    "genre": "M 伦理与习俗", "character_type": "奴隶", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Servus senex in vīllā labōrat. Fīlius dominī parvus est. Fīlius dominī servum amat. "
        "Fīlius: 'Serve, cūr tū semper trīstis es? Cūr numquam rīdēs?' "
        "Servus: 'Serve sum, domine parve. Servus nōn rīdet.' "
        "Fīlius: 'Ego tē iubeō rīdēre!' Servus rīdet — sed rīsus nōn est vērus. "
        "Fīlius: 'Cūr nōn vērus rīsus? Cūr nōn vērus rīsus?' Servus: 'Quia rīdēre nōn potest iubērī.' "
        "Multī annī trānseunt. Fīlius dominus fit. Fīlius servum līberat. "
        "Servus: 'Domine, cūr mē līberās?' Dominus: 'Ut rīdeās. Vērē.' Servus rīdet. Nunc — vērus."
    )
}

STORIES["cap46_06"] = {
    "title_la": "Nāvis Aurea",
    "title_zh": "金船",
    "target_chapter": 46, "theme": "41 财富与贫困", "style": "史诗",
    "genre": "B 神话与传说", "character_type": "商人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rēx nāvem auream aedificat. Nāvis magna est. Nāvis tōta ex aurō facta est. "
        "Rēx: 'Haec nāvis ad fīnem mundī nāvigābit. Haec nāvis rēgem ad deōs portābit.' "
        "Nāvis in mare nāvigat. Sed aurum grave est. Nāvis in marī mergitur. "
        "Rēx cum nāvī mergitur. Rēx: 'Aurum mē necāvit. Aurum — deus meus — mē dēlēvit.' "
        "In fundō maris, nāvis aurea iacet. Piscēs per nāvem natant. "
        "Piscēs: 'Hīc aurum est. Sed nōn mandūcātur. Nōn natātur. Nōn vīvitur.'"
    )
}

STORIES["cap46_07"] = {
    "title_la": "Duo Frātrēs in Exsiliō",
    "title_zh": "流放中的两兄弟",
    "target_chapter": 46, "theme": "31 手足与对手", "style": "古典",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duo frātrēs in exsiliō sunt. Ā patriā pulsī. Ā urbe pulsī. Ā familiā pulsī. "
        "Frāter maior: 'Frāter, cūr nōs pulsī sumus? Quid fēcimus?' "
        "Frāter minor: 'Vēra dīximus. Potentēs nōs timuērunt.' "
        "Frāter maior: 'In exsiliō nihil est. Nūlla domus. Nūllī amīcī. Nūlla spēs.' "
        "Frāter minor: 'Nōs habēmus. Tū mē habēs. Ego tē habeō. Hoc est — domus.' "
        "Frāter maior tacet. Frāter maior frātrem amplectitur. "
        "In exsiliō, frātrēs sedent. Sōl occidit. Stēllae surgunt. "
        "Frātrēs nōn sōlī sunt. Frātrēs — domum invēnērunt."
    )
}

STORIES["cap46_08"] = {
    "title_la": "Fēmina in Senātū",
    "title_zh": "元老院中的女人",
    "target_chapter": 46, "theme": "37 性别与权力", "style": "雄辩",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Fēmina in senātum intrat. Senātōrēs stupent. Senātōrēs: 'Fēmina in senātū! Nefās!' "
        "Fēmina: 'Senātōrēs, ego nōn hīc venī ut vōs perturbem. Ego venī ut vōs interrogem. "
        "Fīlius meus in bellō mortuus est. Marītus meus in bellō mortuus est. Frāter meus in bellō mortuus est. "
        "Vōs bellum geritis. Vōs fīliōs meōs mittitis. Vōs marītōs mittitis. Ego — nihil possum.' "
        "Senātōrēs tacent. Senātōrēs fēminam spectant. "
        "Ūnus senātor: 'Fēmina, quid vīs?' Fēmina: 'Pācem. Solum pācem.' "
        "Senātōrēs: 'Pāx nōn est in manibus nostrīs.' Fēmina: 'Tunc cuius in manibus est?' "
        "Senātus tacet. Fēmina exit. In forō, ventus flat. Ventus — pācem portat?"
    )
}

STORIES["cap46_09"] = {
    "title_la": "Canticum Cycnī",
    "title_zh": "天鹅之歌",
    "target_chapter": 46, "theme": "61 暮年与青春", "style": "抒情",
    "genre": "B 神话与传说", "character_type": "拟人动物", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego cycnus sum. Tōtam vītam tacuī. Tōtam vītam in aquīs natāvī. "
        "Tōtam vītam sōlus fuī. Sed nunc — cantō. "
        "Nunc, quandō mors prope est, vōx mea aperītur. "
        "Canticum meum trīste est. Canticum meum pulchrum est. "
        "Avēs aliae: 'Cūr nunc cantās? Cūr nōn anteā?' "
        "Ego: 'Canticum meum nōn est canticum vītae. Canticum meum est canticum vālis. "
        "Nōn cantō quia vīvō — cantō quia morior. Nōn cantō ut audiar — cantō ut—' "
        "Cycnus tacet. Cycnus in aquam cadit. Cycnus mortuus est. "
        "Sed canticum — in ventō manet. Canticum — semper."
    )
}

STORIES["cap46_10"] = {
    "title_la": "Puer et Ignis",
    "title_zh": "男孩与火",
    "target_chapter": 46, "theme": "12 知识", "style": "精炼",
    "genre": "M 伦理与习俗", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer ignem in silvā accendit. Puer ignem spectat. Flammae altae sunt. "
        "Puer: 'Ignis, tū pulcher es. Tū calidus es. Tū fortis es.' "
        "Ignis: 'Ego pulcher sum — sed ego quoque perīculōsus sum. "
        "Nōlī mē nimis prope spectāre. Nōlī mē tangere.' "
        "Puer: 'Sed ego tē amō. Ego tē tenēre volō.' "
        "Ignis: 'Sī mē tangēs, ego tē ūram. Sī mē nimis amābis, ego tē dēlēbō.' "
        "Puer ignem nōn tangit. Puer ignem ā longē spectat. Puer: 'Ignis, tū mē docēs. "
        "Quaedam amāre possumus — sed nōn tangere. Quaedam spectāre — sed nōn habēre.'"
    )
}

# === Cap.48: 需 7 篇 ===
STORIES["cap48_04"] = {
    "title_la": "Senex in Monte",
    "title_zh": "山上的老人",
    "target_chapter": 48, "theme": "61 暮年与青春", "style": "抒情",
    "genre": "G 哲学寓言", "character_type": "老人", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in monte habitō. Multōs annōs hīc habitō. Nēmō mē quaerit. Nēmō mē invenit. "
        "In monte, ego sōlus sum. Sed nōn sum sōlus — mōns mēcum est. "
        "In urbe, ego multa habēbam. Domum. Familiam. Amīcōs. Negōtium. "
        "Omnia perdidī. Nōn dolō. Nōn fleō. Nōn queror. "
        "In monte, ego nihil habeō — sed omnia videō. In urbe, omnia habēbam — sed nihil vidēbam. "
        "Quandō iuvenis eram, montem timēbam. Quandō senex sum, montem amō. "
        "Mōns: 'Tū mē ascendistī. Tū mē vīcistī. Nunc — tū mēcum manēs.' "
        "Ego: 'Mōns, tū mihi omnia docuistī. Nunc — ego taceō.'"
    )
}

STORIES["cap48_05"] = {
    "title_la": "Epistula ad Imperātōrem",
    "title_zh": "致皇帝书",
    "target_chapter": 48, "theme": "06 权力", "style": "雄辩",
    "genre": "C 历史与人物", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "书信体",
    "text": (
        "Imperātorī salūtem. Nōn tibi blandior. Nōn tē adūlor. Ego senex sum — tibi vēra dīcō. "
        "Tū Rōmam regis. Tū mundum regis. Tū exercitum habēs. Tū senātum habēs. "
        "Sed tū — amīcum nōn habēs. Tū — vēritātem nōn audīs. Tū — sōlus es. "
        "Potentēs semper sōlī sunt. Hoc ego vīdī. Hoc ego didicī. "
        "Imperātor, nōlī timēre mortem — timē sōlitūdinem. Mors omnibus venit. Sōlitūdō — paucīs. "
        "Sī hanc epistulam legis, tū adhūc vīvis. Sī nōn legis — tū iam mortuus es. "
        "Valē, imperātor. Ego tē nōn salūtō — ego tē moneō."
    )
}

STORIES["cap48_06"] = {
    "title_la": "Nox Ultima",
    "title_zh": "最后一夜",
    "target_chapter": 48, "theme": "01 生死", "style": "冷峻",
    "genre": "J 心理与梦境", "character_type": "旅人", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hospes in caupōnā pernoctat. Hospes sōlus est. Hospes nēminem cognōscit. "
        "Nocte, hospes somnium videt. In somniō, hospes mortuus est. "
        "In somniō, hospes vītam suam recēnsēt. Omnia errāta. Omnia verba nōn dicta. Omnēs amōrēs nōn amātī. "
        "Hospes: 'Sī iterum vīverem, omnia aliter facerem. Omnēs amārem. Nēminem laederem. Omnia dīcerem.' "
        "Māne, hospes excitātur. Hospes vīvit. Hospes surgit. Hospes in viam exit. "
        "Hospes: 'Hodiē — vīvō. Hodiē — omnia aliter faciam.' "
        "Sed via longa est. Et memoria brevis. Et homō — homō est."
    )
}

STORIES["cap48_07"] = {
    "title_la": "Faber et Fīlia",
    "title_zh": "工匠与女儿",
    "target_chapter": 48, "theme": "25 家庭", "style": "抒情",
    "genre": "A LLPSI宇宙", "character_type": "罗马人", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Faber in officīnā labōrat. Fīlia parvula in officīnam intrat. "
        "Fīlia: 'Pater, cūr semper labōrās? Cūr numquam mēcum lūdis?' "
        "Faber: 'Labōrō ut tū nōn labōrēs. Labōrō ut tū lūdās. Labōrō ut tū vītam meliōrem habeās.' "
        "Fīlia: 'Sed pater, vīta melior nōn est pecūnia. Vīta melior est — tū.' "
        "Faber opus sistit. Faber fīliam spectat. Faber: 'Quis tē haec docuit?' "
        "Fīlia: 'Tū, pater. Tū mē semper docuistī — etiam quandō nōn loquēbāris.' "
        "Faber fīliam amplectitur. Faber: 'Hodiē nōn labōrō. Hodiē — tēcum lūdō.'"
    )
}

STORIES["cap48_08"] = {
    "title_la": "Mare et Lūna",
    "title_zh": "海与月",
    "target_chapter": 48, "theme": "18 自然", "style": "修辞",
    "genre": "B 神话与传说", "character_type": "拟人自然", "length_tier": "长篇",
    "narrative_mode": "对话体",
    "text": (
        "Mare: 'Lūna, tū in caelō splendēs. Ego in terrā iaceō. Tū pulchra es. Ego profundus sum.' "
        "Lūna: 'Mare, tū mē reflectis. Sine tē, ego nōn videor. Sine mē, tū niger es.' "
        "Mare: 'Cūr nōs numquam convenīmus? Cūr tū in caelō, ego in terrā?' "
        "Lūna: 'Hoc est fātum nostrum. Ego lūcem dō. Tū lūcem recipis. "
        "Nōn convenīmus — sed nōs amāmus. Nōn tangimus — sed nōs sentīmus.' "
        "Mare undās tollit. Mare lūnam tangere vult. Sed lūna procul manet. "
        "Mare: 'Quandō ego tē tangam?' Lūna: 'Numquam. Sed ego semper prope tē sum. Semper.'"
    )
}

STORIES["cap48_09"] = {
    "title_la": "Servus Doctus",
    "title_zh": "博学的奴隶",
    "target_chapter": 48, "theme": "28 教育", "style": "古典",
    "genre": "M 伦理与习俗", "character_type": "奴隶", "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego servus sum — sed ego legō. Ego servus sum — sed ego cōgitō. "
        "Dominus meus multōs librōs habet. Dominus librōs nōn legit. Ego librōs legō. "
        "Dominus: 'Serve, cūr legere discis? Servī nōn legunt.' "
        "Ego: 'Domine, servī nōn legunt — sed ego legō. Servī nōn cōgitant — sed ego cōgitō.' "
        "Dominus: 'Cōgitātiō est perīculōsa. Servus quī cōgitat — nōn est servus.' "
        "Ego: 'Domine, corpus meum tuum est. Sed mēns mea — mea est. Hanc nōn potes emere. Hanc nōn potes vincere.' "
        "Dominus tacet. Dominus abit. Ego legō. Ego semper legō."
    )
}

STORIES["cap48_10"] = {
    "title_la": "Frūmentum et Circēnsēs",
    "title_zh": "面包与马戏",
    "target_chapter": 48, "theme": "35 城市", "style": "戏谑",
    "genre": "D 讽刺", "character_type": "乞丐", "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Populus in forō congregātur. Imperātor frūmentum dat. Imperātor circēnsēs dat. "
        "Populus: 'Imperātor bonus est! Imperātor nōs amat! Pānem et lūdōs habēmus!' "
        "Mendīcus in angulō sedet. Mendīcus frūmentum accipit. Mendīcus circēnsēs spectat. "
        "Mendīcus: 'Populus, cūr gaudētis? Imperātor vōbīs frūmentum dat — ut vōs taceātis. "
        "Imperātor vōbīs circēnsēs dat — ut vōs nōn cōgitētis. "
        "Vōs pānem habētis — sed lībertātem perdidistis. Vōs lūdōs habētis — sed rem pūblicam.' "
        "Populus mendīcum nōn audit. Populus frūmentum mandūcat. Populus circēnsēs spectat. "
        "Mendīcus: 'Rōma nōn est urbs — Rōma est career. Et vōs — captīvī laetī.'"
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
            if n > max_n: max_n = n
    return max_n + 1

def main():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    passed, failed = [], []

    for story_id, meta in STORIES.items():
        target_ch = meta["target_chapter"]
        latin_text = meta["text"].strip().replace("'", '"')
        title_la = meta["title_la"]

        print(f"\n--- {story_id}: {title_la} (target Cap.{target_ch}) ---")

        eval_r = evaluate(latin_text, story_id)
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])

        gap = (v2_level - target_ch) if v2_level else "N/A"
        ok = v2_level is not None and v2_level <= target_ch + 2

        print(f"  算法: v2_level={v2_level}, v2_rate={v2_rate}%, gap={gap}")

        if not ok:
            print(f"  [FAIL] 算法判到 Cap.{v2_level}, OOV: {v2_oov[:5]}")
            failed.append((story_id, v2_level, v2_oov))
            continue

        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)
        nnn = find_next_number(cap_dir, target_ch)
        slug = title_to_slug(title_la)
        filename = f"Cap{target_ch}_{slug}_longum_{nnn:03d}.md"
        filepath = cap_dir / filename

        wc = len(re.findall(r"[A-Za-zāēīōūȳĀĒĪŌŪȲ]{2,}", latin_text))

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
            "---",
        ]
        filepath.write_text("\n".join(yaml) + "\n\n" + latin_text + "\n", encoding="utf-8")
        print(f"  [PASS] → {filename}")
        passed.append((story_id, filename, target_ch))

    # 汇总
    print(f"\n{'='*60}")
    print(f"结果: {len(passed)} 通过, {len(failed)} 失败")
    for sid, fn, ch in passed:
        print(f"  [OK] Cap.{ch}: {fn}")
    for sid, lvl, oov in failed:
        print(f"  [FAIL] {sid}: algo={lvl}, oov={oov[:3]}")

    # 更新 progress.json
    chapter_counts = {}
    for cap_dir in sorted(REALITATES_DIR.glob("Cap*")):
        if cap_dir.is_dir():
            chapter_counts[cap_dir.name] = len(list(cap_dir.glob("*.md")))

    progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    target_chapters = [
        "Cap21","Cap22","Cap23","Cap24","Cap26","Cap27","Cap28","Cap29",
        "Cap30","Cap31","Cap32","Cap33","Cap34","Cap35","Cap42","Cap46","Cap48"
    ]
    for cn in target_chapters:
        count = chapter_counts.get(cn, 0)
        if cn not in progress["chapters"]:
            progress["chapters"][cn] = {"done": 0, "target": 10, "need": 10, "strategy": "standard"}
        progress["chapters"][cn]["done"] = count
        progress["chapters"][cn]["need"] = max(0, progress["chapters"][cn]["target"] - count)
    progress["last_updated"] = now
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n当前状态:")
    for cn in target_chapters:
        ch_num = cn.replace("Cap", "")
        print(f"  Cap.{ch_num}: {chapter_counts.get(cn, 0)}/10")


if __name__ == "__main__":
    main()