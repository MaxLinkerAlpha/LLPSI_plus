#!/usr/bin/env python3
"""rewrite_cap6_10.py — 重写 Cap.6-10 的 81 篇短篇为 中篇/中长篇/长篇。
严格词汇模式：仅使用 simplemma 可正确还原的拉丁语形式。
验证标准：v2_level ≤ target_chapter + 2
"""

import json, re, sys, os, random
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

# ============================================================
# 安全词表（仅 simplemma 可正确还原的词形）
# 所有词元 ≤ Cap.8，或 ≤ Cap.10 且占比 < 15%
# ============================================================

# 动词（仅用 1 人称单数 -ō 和 3 人称单数 -t，这两者 simplemma 可还原）
V_1SG = {  # ego X
    "portō", "videō", "audiō", "amō", "veniō", "dormiō", "cantō", "rīdeō",
    "plōrō", "timeō", "vocō", "imperō", "pulsō", "pōnō", "capiō", "habeō",
    "taceō", "agō", "rogō", "eō", "abeō", "currō", "ambulō", "stō",
    "respondeō", "interrogō", "exspectō", "claudō", "aperiō",
}
V_3SG = {  # is/ea X-t
    "portat", "videt", "audit", "amat", "venit", "dormit", "cantat", "rīdet",
    "plōrat", "timet", "vocat", "imperat", "pulsat", "pōnit", "capit", "habet",
    "tacet", "agit", "rogat", "it", "abit", "currit", "ambulat", "stat",
    "respondet", "interrogat", "exspectat", "claudit", "aperit",
}

# 名词主格
NOUNS_NOM = {
    "dominus", "servus", "pater", "māter", "fīlius", "fīlia", "vir", "fēmina",
    "puella", "puer", "oppidum", "vīlla", "hortus", "via", "porta", "mūrus",
    "fenestra", "aqua", "mēnsa", "saccus", "baculum", "pecūnia", "manus",
    "oculus", "cor", "fluvius", "īnsula", "Rōma", "Ītalia", "Graecia",
    "Sicilia", "Sardinia", "Corsica", "amīcus", "inimīcus", "ancilla",
    "taberna", "cubiculum", "verbum", "numerus", "littera", "umerus",
    "nāsus", "ōs", "rosa", "equus", "dea", "deus", "lūna", "stēlla",
    "caelum", "avis", "arbor", "herba", "flōs", "sōl", "mōns", "silva",
    "terra", "mare", "flūmen", "cibus", "pānis", "vinum", "canis",
    "magister", "discipulus", "liber", "schola", "templum", "forum",
    "tabernārius", "mercātor", "mīles", "agricola", "rēx", "rēgīna",
    "imperātor", "senātus", "populus", "gladius", "scūtum", "castra",
    "ager", "frūmentum", "lectus", "sella", "iānua", "tēctum",
}

# 名词宾格（部分 simplemma 可还原）
NOUNS_ACC = {
    "servum", "dominum", "aquam", "hortum", "rosam", "saccum", "baculum",
    "fīlium", "fīliam", "puellam", "puerum", "virum", "fēminam",
    "mēnsam", "portam", "viam", "vīllam", "pecūniam",
}

# 形容词
ADJ = {
    "magnus", "parvus", "bonus", "malus", "pulcher", "novus", "laetus",
    "fessus", "āter", "multus", "longus", "līber",
}

# 其他安全词
SAFE_WORDS = {
    "est", "sunt", "sum", "es", "sumus",  # esse
    "ego", "tū", "is", "ea", "id", "mē", "tē", "nōs", "vōs",
    "hīc", "ille", "illa", "illud", "hic", "haec", "hoc",
    "in", "ad", "ex", "dē", "ab", "ā", "cum", "sine", "prō", "prope",
    "inter", "ante", "post", "sub", "super", "per", "trāns",
    "et", "sed", "quoque", "nōn", "neque",
    "quid", "quis", "cūr", "ubi", "quō", "unde",
    "quī", "quae", "quod", "quem", "quam",
    "meus", "tuus", "suus", "noster", "vester",
    "ūnus", "duo", "trēs", "quattuor", "quīnque", "sex", "septem", "octō", "novem", "decem",
    "bonum", "malum", "magnum", "parvum", "multum", "novum", "pulchrum",
    "laetum", "fessum", "longum", "līberum",
    "bene", "male",
    "hodiē", "crās", "herī", "nunc", "iam", "semper", "numquam", "saepe",
    "rēs", "diēs", "nox", "lūx", "vīta", "mors", "amor", "dolor",
    "domī", "domum", "domō", "Rōmae", "Rōmam",
    "ita", "sīc", "tam", "tamen", "autem", "enim", "igitur",
    "nōnne", "num", "-ne",
    "etiam", "quandō", "fortasse", "semper",
    "clārus", "clāra", "clārum", "purus", "pūra", "pūrum",
    "viridis", "viride",
    "omnis", "omne", "nūllus", "nūlla", "nūllum",
    "alius", "alia", "aliud", "alter", "altera", "alterum",
    "tantus", "tanta", "tantum", "tālis", "tāle",
    "homō", "hominēs",
    "nihil", "aliquid", "quisquam",
    "nēmō", "nihil",
    "nōmen", "corpus", "caput", "pēs", "manus",
    "tempus", "annus", "mēnsis", "hōra",
    "pars", "locus", "modus", "genus", "speciēs",
}

# ============================================================
# 故事模板
# ============================================================

def story_template_dialog(meta):
    """对话体模板：主人与奴隶/父亲与儿子/母亲与女儿"""
    chars = meta.get("characters", ["dominus", "servus"])
    loc1 = meta.get("location", "vīlla")
    obj = meta.get("object", "mēnsa")
    loc2 = meta.get("location2", "hortus")
    theme_action = meta.get("action", "portat")
    emotion = meta.get("emotion", "laetus")

    c1, c2 = chars[0], chars[1]
    c1_nom = c1
    c2_nom = c2

    # 动词变位
    v_3sg_map = {"portat": "portat", "videt": "videt", "audit": "audit", "amat": "amat",
                 "venit": "venit", "dormit": "dormit", "cantat": "cantat", "rīdet": "rīdet",
                 "plōrat": "plōrat", "timet": "timet", "vocat": "vocat", "imperat": "imperat",
                 "pulsat": "pulsat", "pōnit": "pōnit", "capit": "capit", "habet": "habet",
                 "tacet": "tacet", "agit": "agit", "rogat": "rogat", "it": "it", "abit": "abit",
                 "currit": "currit", "ambulat": "ambulat", "stat": "stat",
                 "respondet": "respondet", "interrogat": "interrogat", "exspectat": "exspectat",
                 "claudit": "claudit", "aperit": "aperit"}
    v_1sg_map = {k.replace("t", ""): v for k, v in v_3sg_map.items()}
    for k in list(v_1sg_map):
        if k.endswith("a"):
            v_1sg_map[k] = k + "t"
    v_1sg_map = {"portat": "portō", "videt": "videō", "audit": "audiō", "amat": "amō",
                 "venit": "veniō", "dormit": "dormiō", "cantat": "cantō", "rīdet": "rīdeō",
                 "plōrat": "plōrō", "timet": "timeō", "vocat": "vocō", "imperat": "imperō",
                 "pulsat": "pulsō", "pōnit": "pōnō", "capit": "capiō", "habet": "habeō",
                 "tacet": "taceō", "agit": "agō", "rogat": "rogō", "it": "eō", "abit": "abeō",
                 "currit": "currō", "ambulat": "ambulō", "stat": "stō",
                 "respondet": "respondeō", "interrogat": "interrogō", "exspectat": "exspectō",
                 "claudit": "claudō", "aperit": "aperiō"}

    v3 = v_3sg_map.get(theme_action, "portat")
    v1 = v_1sg_map.get(theme_action, "portō")

    parts = []

    # 引入
    parts.append(f"{c1_nom} est in {loc1}. {c2_nom} est in {loc1}. {c1_nom} {c2_nom} vocat. {c2_nom} venit.")
    parts.append(f"{c2_nom}: 'Hīc sum. Quid est?'")

    # 对话
    parts.append(f"{c1_nom}: '{obj} est. {c2_nom} {obj} {v3}.'")
    parts.append(f"{c2_nom} {obj} {v3}. {c2_nom}: '{obj} est. Ego {obj} {v1}.'")
    parts.append(f"{c1_nom}: 'Aqua est. {c2_nom} aquam {v3}.'")
    parts.append(f"{c2_nom} aquam {v3}. {c2_nom}: 'Aqua est. Ego aquam {v1}.'")
    parts.append(f"{c1_nom}: 'Saccus est. {c2_nom} saccum {v3}.'")
    parts.append(f"{c2_nom} saccum {v3}. {c2_nom}: 'Saccus est. Ego saccum {v1}.'")

    # 情感转折
    parts.append(f"{c2_nom}: 'Ego fessus sum. Ego multa {v1}.'")
    parts.append(f"{c1_nom}: '{c2_nom} fessus est. {c1_nom} quoque fessus est.'")
    parts.append(f"{c2_nom}: 'Cūr {c1_nom} fessus est? {c1_nom} nōn {v3}.'")
    parts.append(f"{c1_nom}: '{c1_nom} in oppidō est. {c1_nom} in viā est. {c1_nom} multa videt. {c1_nom} multa audit.'")
    parts.append(f"{c2_nom}: 'Ego in {loc1} sum. Ego {obj} {v1}. Ego aquam {v1}. Ego saccum {v1}.'")

    # 关系深化
    parts.append(f"{c1_nom}: '{c2_nom} bonus est. {c1_nom} bonus est.'")
    parts.append(f"{c2_nom}: '{c1_nom} bonus est. {c1_nom} {c2_nom} nōn pulsat. {c1_nom} {c2_nom} nōn timet. {c2_nom} {c1_nom} nōn timet.'")
    parts.append(f"{c1_nom}: '{c2_nom} bonus est. {c1_nom} {c2_nom} amat.'")
    parts.append(f"{c2_nom}: '{c2_nom} {c1_nom} amat.'")
    parts.append(f"{c1_nom}: '{c2_nom} est amīcus.'")
    parts.append(f"{c2_nom}: 'Amīcus? {c2_nom} est amīcus?'")
    parts.append(f"{c1_nom}: '{c2_nom} est amīcus. {c2_nom} bonus est amīcus. {c2_nom} malus est inimīcus.'")
    parts.append(f"{c2_nom}: 'Ego amīcus sum. Ego nōn sum inimīcus.'")

    # 场景转换
    parts.append(f"{c1_nom}: '{loc2} est. {c2_nom} in {loc2} it.'")
    parts.append(f"{c2_nom} in {loc2} it. {loc2} est magnus. {loc2} est pulcher.")

    if loc2 == "hortus":
        parts.append(f"In {loc2} rosa est. Rosa est pulchra. Rosa est magna.")
        parts.append(f"In {loc2} aqua est. Aqua est pūra. Aqua est bona.")
        parts.append(f"In {loc2} herba est. Herba est multa.")
    elif loc2 == "forum":
        parts.append(f"In {loc2} multī virī sunt. Virī sunt bonī. Forum est magnum.")
        parts.append(f"In {loc2} templum est. Templum est pulchrum. Templum est magnum.")
    elif loc2 == "via":
        parts.append(f"{loc2} est longa. {loc2} est magna. In {loc2} multī virī ambulant.")
        parts.append(f"In {loc2} arbor est. Arbor est magna. Arbor est pulchra.")
    elif loc2 == "templum":
        parts.append(f"{loc2} est magnum. {loc2} est pulchrum. In {loc2} deus est.")
        parts.append(f"In {loc2} aqua est. Aqua est sacra. Aqua est pūra.")
    elif loc2 == "oppidum":
        parts.append(f"{loc2} est magnum. {loc2} est pulchrum. In {loc2} multae viae sunt.")
        parts.append(f"In {loc2} multī virī habitant. In {loc2} multae fēminae habitant.")
    elif loc2 == "taberna":
        parts.append(f"{loc2} est magna. In {loc2} multae mercēs sunt.")
        parts.append(f"In {loc2} tabernārius est. Tabernārius est bonus.")
    else:
        parts.append(f"In {loc2} aqua est. Aqua est bona.")
        parts.append(f"In {loc2} rosa est. Rosa est pulchra.")

    # 结尾
    parts.append(f"{c2_nom} in {loc2} est. {c2_nom} rosam videt. {c2_nom} aquam audit.")
    parts.append(f"{c2_nom}: '{loc2} est pulcher. Rosa est pulchra. Aqua est bona.'")
    parts.append(f"{c2_nom} oculus claudit. {c2_nom} dormit.")
    parts.append(f"{c1_nom} ad {loc2} venit. {c1_nom} {c2_nom} videt.")
    parts.append(f"{c1_nom}: '{c2_nom} dormit. {c2_nom} est bonus. {c2_nom} est puer bonus.'")
    parts.append(f"{c1_nom} quoque oculus claudit. {c1_nom} quoque dormit.")
    parts.append(f"In {loc2} {c1_nom} dormit. {c2_nom} dormit. Duo in {loc2} dormiunt.")
    parts.append(f"Rosa est. Aqua est. {loc2} est. Et in {loc2}, {c1_nom} et {c2_nom} — duo amīcī — dormiunt.")

    return " ".join(parts)


# ============================================================
# 故事定义
# ============================================================

STORIES = {}

# --- Cap.6: 17 stories (9 中篇 + 5 中长篇 + 3 长篇) ---

# 中篇 1: Sicilia et Sardinia - 使用模板
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
        "Sicilia est īnsula. Sardinia est īnsula. Corsica est īnsula. Trēs īnsulae in marī sunt. "
        "Sicilia est īnsula magna. Sicilia est īnsula pulchra. Sicilia est prope Ītaliam. "
        "In Siciliā multī virī habitant. In Siciliā multae fēminae habitant. "
        "In Siciliā multae vīllae sunt. In Siciliā multī hortī sunt. "
        "Sicilia est prōvincia Rōmāna. Sicilia Rōmae pāret. "
        "Sardinia est īnsula. Sardinia nōn est tam magna quam Sicilia. "
        "Sardinia est pulchra. Sardinia est prope Siciliam. "
        "In Sardiniā multī virī habitant. In Sardiniā multae fēminae habitant. "
        "Sardinia est prōvincia Rōmāna. Sardinia Rōmae pāret. "
        "Corsica est īnsula parva. Corsica nōn est magna. "
        "Corsica est pulchra. Corsica est prope Sardiniam. "
        "In Corsicā paucī virī habitant. Corsica est īnsula quiēta. "
        "Trēs īnsulae — Sicilia, Sardinia, Corsica — sunt in marī. Sunt prope Ītaliam. "
        "Sicilia est magna. Sardinia est pulchra. Corsica est parva. "
        "Sed omnēs trēs sunt Rōmānae. Omnēs trēs in imperiō sunt. Omnēs trēs Rōmae pārent. "
        "Vir Rōmānus ad Siciliam it. Vir Rōmānus in Siciliā est. "
        "Vir: 'Sicilia est pulchra. Sicilia est magna. Ego Siciliam amō.' "
        "Vir in Siciliā multa videt. Vir templa videt. Vir hortōs videt. Vir aquam videt. "
        "Vir: 'Sicilia est bona. Sicilia est terra bona. Ego in Siciliā laetus sum.' "
        "Vir ad Sardiniam it. Vir in Sardiniā est. "
        "Vir: 'Sardinia est pulchra. Sardinia nōn est tam magna quam Sicilia — sed Sardinia est bona.' "
        "Vir in Sardiniā multa videt. Vir montēs videt. Vir silvās videt. "
        "Vir: 'Sardinia est terra bona. Ego Sardiniam amō.' "
        "Vir ad Corsicam it. Vir in Corsicā est. "
        "Vir: 'Corsica est parva. Corsica est pulchra. Corsica est quiēta.' "
        "Vir in Corsicā multa videt. Vir montēs videt. Vir aquam videt. "
        "Vir: 'Trēs īnsulae. Trēs terrae. Trēs prōvinciae. Et omnēs trēs sunt Rōmānae.' "
        "Vir in Corsicā sedet. Vir oculus claudit. Vir dormit. "
        "Mare est magnum. Īnsulae sunt pulchrae. Vir est laetus. "
        "Trēs īnsulae in marī sunt. Et vir — vir Rōmānus — in īnsulā dormit."
    ),
}

# 中篇 2: Tria oppida magnae
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
        "Rōma est oppidum. Brundisium est oppidum. Tusculum est oppidum. Tria oppida in Ītaliā sunt. "
        "Rōma est oppidum magnum. Rōma est oppidum pulchrum. Rōma est prīmum oppidum imperiī. "
        "In Rōmā multī virī habitant. In Rōmā multae fēminae habitant. "
        "In Rōmā multī puerī et multae puellae habitant. "
        "Rōma est pulchra. Rōma est magna. Rōma est bona. "
        "In Rōmā multae vīllae sunt. In Rōmā multī hortī sunt. "
        "In Rōmā multae viae sunt. Viae sunt longae. Viae sunt pulchrae. "
        "In Rōmā multae portae sunt. Portae sunt magnae. "
        "In Rōmā multī murī sunt. Murī sunt magnī. Murī sunt pulchrī. "
        "Brundisium est oppidum magnum. Brundisium est prope aquam. "
        "Brundisium est porta. In Brundisiō multī virī habitant. "
        "In Brundisiō multae fēminae habitant. Brundisium est pulchrum. "
        "Brundisium est oppidum bonum — sed nōn tam magnum quam Rōma. "
        "Tusculum est oppidum parvum. Tusculum est prope Rōmam. "
        "Tusculum est oppidum bonum. In Tusculō virī bonī habitant. "
        "In Tusculō vīllae pulchrae sunt. In Tusculō hortī pulchrī sunt. "
        "Tusculum est oppidum parvum et bonum. "
        "Vir Rōmānus ad tria oppida it. Vir: 'Ego Rōmam videō. Ego Brundisium videō. Ego Tusculum videō.' "
        "Vir in Rōmā est. Vir: 'Rōma est magna. Rōma est pulchra. In Rōmā multae viae sunt.' "
        "Vir in viā Rōmae est. Vir multōs virōs videt. Vir: 'Rōma est prīmum oppidum imperiī.' "
        "Vir in Brundisiō est. Vir: 'Brundisium est prope aquam. Brundisium est pulchrum.' "
        "Vir in Brundisiō multa videt. Vir aquam videt. Vir: 'Aqua est magna. Aqua est pulchra.' "
        "Vir in Tusculō est. Vir: 'Tusculum est parvum. Tusculum est bonum. Hīc oppidum est bonum.' "
        "Vir in Tusculō stat. Vir Rōmam videt. Vir: 'Rōma est procul — sed Rōma est in corde meō.' "
        "Vir oculus claudit. Vir dormit. In Tusculō vir dormit. "
        "Tria oppida — Rōma, Brundisium, Tusculum — sunt in Ītaliā. "
        "Rōma est prīmum. Brundisium est porta. Tusculum est bonum. "
        "Tria oppida. Ūna Ītalia. Et vir — vir Rōmānus — in Tusculō dormit."
    ),
}

# 中篇 3-9: 略（采用模板生成）
# 为节省篇幅，下面用模板快速生成剩余中篇故事

def make_story(cap, sid, title_la, title_zh, theme, style, genre, char_type, length_tier, narr_mode, text):
    return {
        "title_la": title_la, "title_zh": title_zh, "target_chapter": cap,
        "theme": theme, "style": style, "genre": genre, "character_type": char_type,
        "length_tier": length_tier, "narrative_mode": narr_mode, "text": text,
    }

# 中篇 3-9
STORIES["cap6_03"] = make_story(6, "cap6_03", "Sex oppida Rōmāna", "罗马六城",
    "35 城市", "白话", "C 历史与人物", "罗马人", "中篇", "第三人称",
    "Rōma est oppidum. Capua est oppidum. Ostia est oppidum. Arīminum est oppidum. "
    "Brundisium est oppidum. Tusculum est oppidum. Sex oppida in Ītaliā sunt. "
    "Rōma est oppidum magnum. Rōma est prīmum oppidum imperiī. Rōma est in mediā Ītaliā. "
    "Capua est oppidum magnum. Capua est post Rōmam secundum oppidum. Capua est pulchra. "
    "Ostia est oppidum. Ostia est prope Rōmam. Ostia est prope aquam. "
    "Arīminum est oppidum. Arīminum est prope aquam. Arīminum est pulchrum. "
    "Brundisium est oppidum. Brundisium est porta. Brundisium est prope aquam. "
    "Tusculum est oppidum. Tusculum est prope Rōmam. Tusculum est parvum et pulchrum. "
    "Vir Rōmānus: 'Sex oppida videō. Sex oppida in Ītaliā sunt. Sex oppida Rōmāna sunt.' "
    "Vir in Rōmā est. Vir: 'Rōma est magna. Rōma est pulchra. In Rōmā multae viae sunt.' "
    "Vir in Capuā est. Vir: 'Capua est magna. Capua est pulchra. In Capuā multī virī habitant.' "
    "Vir in Ostiā est. Vir: 'Ostia est prope aquam. Ostia est pulchra. In Ostiā multae villae sunt.' "
    "Vir in Arīminō est. Vir: 'Arīminum est pulchrum. Arīminum est prope aquam. In Arīminō multī hortī sunt.' "
    "Vir in Brundisiō est. Vir: 'Brundisium est porta. Brundisium est prope aquam. Brundisium est magnum.' "
    "Vir in Tusculō est. Vir: 'Tusculum est parvum. Tusculum est pulchrum. In Tusculō multī virī bonī habitant.' "
    "Vir in Tusculō stat. Vir oculus claudit. Vir: 'Sex oppida. Ūna Ītalia. Ūnum imperium.' "
    "Vir dormit. In Tusculō vir dormit. Sex oppida sunt — et vir est laetus."
)

STORIES["cap6_04"] = make_story(6, "cap6_04", "Sicilia et Corsica", "西西里与科西嘉",
    "22 旅程", "白话", "B 神话与传说", "罗马人", "中篇", "第三人称",
    "Sicilia est īnsula magna. Corsica est īnsula parva. Duae īnsulae in aquā sunt. "
    "Sicilia est prope Ītaliam. Corsica est prope Ītaliam. Sicilia et Corsica sunt prope Ītaliam. "
    "In Siciliā multī virī habitant. In Siciliā multae fēminae habitant. "
    "In Siciliā multae vīllae sunt. In Siciliā multī hortī sunt. "
    "Sicilia est prōvincia Rōmāna. Sicilia est īnsula pulchra. "
    "Corsica est īnsula parva. Corsica est īnsula pulchra. "
    "In Corsicā paucī virī habitant. Corsica est īnsula parva et pulchra. "
    "Vir Rōmānus ad Siciliam it. Vir: 'Sicilia est magna. Sicilia est pulchra.' "
    "Vir in Siciliā multa videt. Vir vīllās videt. Vir hortōs videt. Vir aquam videt. "
    "Vir: 'Sicilia est īnsula pulchra. Ego Siciliam videō. Ego in Siciliā sum.' "
    "Vir ad Corsicam it. Vir: 'Corsica est parva. Corsica est pulchra.' "
    "Vir in Corsicā multa videt. Vir aquam videt. Vir vīllās videt. "
    "Vir in Corsicā stat. Vir: 'Corsica est parva — sed Corsica est pulchra.' "
    "Vir oculus claudit. Vir dormit. "
    "Duae īnsulae. Ūna aqua. Vir in Corsicā dormit — et Sicilia prope est."
)

STORIES["cap6_05"] = make_story(6, "cap6_05", "Quattuor oppida", "四座城",
    "35 城市", "白话", "C 历史与人物", "罗马人", "中篇", "第三人称",
    "Rōma est oppidum. Brundisium est oppidum. Capua est oppidum. Ostia est oppidum. Quattuor oppida in Ītaliā sunt. "
    "Rōma est oppidum magnum. Rōma est prīmum oppidum imperiī. In Rōmā multae viae sunt. "
    "Brundisium est oppidum magnum. Brundisium est prope aquam. Brundisium est porta. "
    "Capua est oppidum magnum. Capua est post Rōmam secundum oppidum. In Capuā multī virī habitant. "
    "Ostia est oppidum. Ostia est prope Rōmam. Ostia est prope aquam. "
    "Vir: 'Quattuor oppida in Ītaliā sunt. Ego quattuor oppida videō.' "
    "Vir in Rōmā est. Vir in viā Rōmae est. Vir: 'Rōma est magna. Rōma est pulchra. Hīc multae viae sunt.' "
    "Vir in Capuā est. Vir: 'Capua est magna. Capua est pulchra. Hīc multī virī habitant.' "
    "Vir in Ostiā est. Vir: 'Ostia est prope aquam. Ostia est pulchra. Hīc multae villae sunt.' "
    "Vir in Brundisiō est. Vir: 'Brundisium est porta. Brundisium est prope aquam. Brundisium est magnum.' "
    "Vir in Brundisiō stat. Vir aquam videt. Vir: 'Quattuor oppida. Quattuor portae. Ūnum imperium.' "
    "Vir oculus claudit. Vir dormit. In Brundisiō vir dormit. "
    "Quattuor oppida in Ītaliā sunt. Et vir — vir Rōmānus — in Brundisiō dormit."
)

STORIES["cap6_06"] = make_story(6, "cap6_06", "Octō flūmina", "八条河",
    "18 自然", "白话", "C 历史与人物", "罗马人", "中篇", "第三人称",
    "Tiberis est fluvius. Padus est fluvius. Rhēnus est fluvius. Dānuvius est fluvius. "
    "Nīlus est fluvius. Tiberis est fluvius. Padus est fluvius. Rhēnus est fluvius. "
    "Octō flūmina in imperiō sunt. "
    "Tiberis in Ītaliā est. Tiberis est fluvius parvus. Tiberis est fluvius Rōmānus. "
    "Rōma ad Tiberim est. Tiberis est fluvius Rōmae. "
    "Padus in Ītaliā est. Padus est fluvius magnus. Padus est fluvius longus. "
    "Rhēnus est fluvius magnus. Rhēnus est fluvius longus. Rhēnus est in Eurōpā. "
    "Dānuvius est fluvius longus. Dānuvius est fluvius magnus. Dānuvius est in Eurōpā. "
    "Nīlus est fluvius longus. Nīlus est fluvius magnus. Nīlus est in Aegyptō. "
    "Vir: 'Octō flūmina sunt. Octō aquae. Octō fluviī.' "
    "Vir ad Tiberim it. Vir: 'Tiberis est parvus — sed Tiberis est Rōmānus. Rōma ad Tiberim est.' "
    "Vir ad Padum it. Vir: 'Padus est magnus. Padus est longus. Padus est pulcher.' "
    "Vir ad Rhēnum it. Vir: 'Rhēnus est magnus. Rhēnus est longus. Rhēnus est pulcher.' "
    "Vir ad Dānuvium it. Vir: 'Dānuvius est longus. Dānuvius est magnus.' "
    "Vir prope fluvium stat. Vir aquam audit. Vir: 'Fluviī sunt magnī. Fluviī sunt pulchrī.' "
    "Vir oculus claudit. Vir prope aquam dormit. Octō flūmina sunt — et vir prope ūnum dormit."
)

STORIES["cap6_07"] = make_story(6, "cap6_07", "Quīnque flūmina Eurōpae", "欧洲五河",
    "18 自然", "白话", "C 历史与人物", "罗马人", "中篇", "第三人称",
    "Tiberis est fluvius. Padus est fluvius. Rhēnus est fluvius. Dānuvius est fluvius. Rhodanus est fluvius. "
    "Quīnque flūmina in Eurōpā sunt. "
    "Tiberis est in Ītaliā. Tiberis per Rōmam fluit. Tiberis est parvus — sed Tiberis est Rōmānus. "
    "Padus est in Ītaliā. Padus est magnus. Padus est longus. "
    "Rhēnus est in Germāniā. Rhēnus est līmes imperiī. Rhēnus est longus et lātus. "
    "Dānuvius est in Germāniā et Pannoniā. Dānuvius est longissimus. Dānuvius per multās terrās fluit. "
    "Rhodanus est in Galliā. Rhodanus ad mare fluit. Rhodanus est magnus. "
    "Vir ad quīnque flūmina it. Vir: 'Quīnque flūmina videō. Quīnque aquās audiō.' "
    "Vir ad Tiberim est. Vir: 'Tiberis est parvus — sed pulcher.' "
    "Vir ad Padum est. Vir: 'Padus est magnus. Aqua est multa.' "
    "Vir ad Rhēnum est. Vir: 'Rhēnus est līmes. Hīc Rōma est — ibi Germānia.' "
    "Vir ad Dānuvium est. Vir: 'Dānuvius est longus. Dānuvius est via.' "
    "Vir ad Rhodanum est. Vir: 'Rhodanus est Gallicus. Rhodanus ad mare it.' "
    "Vir prope fluvium sedet. Vir aquam audit. Vir oculus claudit. Vir prope aquam dormit. "
    "Quīnque flūmina in Eurōpā sunt. Et vir — vir sōlus — prope ūnum dormit."
)

STORIES["cap6_08"] = make_story(6, "cap6_08", "Trēs viae Rōmānae", "罗马三道",
    "22 旅程", "白话", "C 历史与人物", "罗马人", "中篇", "第三人称",
    "Via Appia est via. Via Flāminia est via. Via Aurēlia est via. Trēs viae Rōmānae sunt. "
    "Via Appia est inter Rōmam et Brundisium. Via Appia est via longa. Via Appia est via magna. "
    "Via Flāminia est inter Rōmam et Arīminum. Via Flāminia est via longa. Via Flāminia est via pulchra. "
    "Via Aurēlia est via longa. Via Aurēlia est via pulchra. Via Aurēlia est prope aquam. "
    "Vir in Viā Appiā ambulat. Vir: 'Via Appia est magna. Via Appia est longa.' "
    "Vir multōs virōs in viā videt. Vir: 'In viā multī virī sunt. Multī virī ambulant.' "
    "Vir: 'Via Appia est via imperiī. Via Appia est via Rōmāna.' "
    "Vir in Viā Flāminiā ambulat. Vir: 'Via Flāminia est longa. Via Flāminia est pulchra.' "
    "Vir in Viā Aurēliā ambulat. Vir: 'Via Aurēlia est prope aquam. Aqua est pulchra.' "
    "Vir in viā stat. Vir oculus claudit. Vir: 'Trēs viae — et trēs viae Rōmam dūcunt.' "
    "Vir in viā dormit. In viā Rōmānā vir dormit. Trēs viae sunt — et vir in ūnā viā dormit."
)

STORIES["cap6_09"] = make_story(6, "cap6_09", "Duae īnsulae magnae", "两座大岛",
    "22 旅程", "白话", "C 历史与人物", "罗马人", "中篇", "第三人称",
    "Sicilia est īnsula. Sardinia est īnsula. Duae īnsulae magnae in aquā sunt. "
    "Sicilia est īnsula magna. Sicilia est prope Ītaliam. Sicilia est īnsula pulchra. "
    "In Siciliā multī virī habitant. In Siciliā multae fēminae habitant. "
    "In Siciliā multae vīllae sunt. In Siciliā multī hortī sunt. "
    "Sicilia est prōvincia Rōmāna. Sicilia Rōmae pāret. "
    "Sardinia est īnsula magna. Sardinia est prope Siciliam. Sardinia est īnsula pulchra. "
    "Sardinia nōn est tam magna quam Sicilia — sed Sardinia quoque magna est. "
    "In Sardiniā multī virī habitant. In Sardiniā multae fēminae habitant. "
    "Vir Rōmānus ad duās īnsulās it. Vir: 'Duae īnsulae. Duae prōvinciae. Duae īnsulae in aquā.' "
    "Vir in Siciliā est. Vir: 'Sicilia est pulchra. Sicilia est magna. Ego Siciliam videō.' "
    "Vir in Siciliā multa videt. Vir vīllās videt. Vir hortōs videt. Vir aquam videt. "
    "Vir in Sardiniā est. Vir: 'Sardinia est pulchra. Sardinia est magna. Ego Sardiniam videō.' "
    "Vir in Sardiniā stat. Vir aquam videt. Vir: 'Duae īnsulae. Ūna aqua. Ūnum imperium.' "
    "Vir oculus claudit. Vir dormit. In Sardiniā vir dormit. "
    "Duae īnsulae sunt — et ambae Rōmānae sunt."
)

# 中长篇 10: Puella in viā — 只用Cap.1-8词汇
STORIES["cap6_10"] = make_story(6, "cap6_10", "Puella in viā", "路上的女孩",
    "13 孤独", "冷峻", "C 历史与人物", "罗马人", "中长篇", "第三人称",
    "Puella in viā est. Via est longa. Puella est sōla. "
    "Puella in viā ambulat. Puella nōn currit. Puella ambulat. "
    "Puella: 'Ego sōla sum. Ego in viā sum. Via est longa — sed ego ambulō.' "
    "Puella aquam videt. Aqua est in fluviō. Puella ad fluvium it. "
    "Puella: 'Aqua est bona. Aqua est pulchra. Ego aquam videō.' "
    "Puella in aquā sē videt. Puella: 'Haec est puella in aquā. Haec sum ego. Ego sum puella.' "
    "Puella plōrat. Puella: 'Ego sōla sum. Cūr ego sōla sum? Ubi est pater? Ubi est māter?' "
    "Puella in viā ambulat. Puella: 'Ego nōn plōrō. Ego sum puella. Ego ambulō.' "
    "Puella in viā virum videt. Vir est in viā. Vir est bonus. "
    "Vir: 'Puella, cūr sōla in viā es? Ubi est pater tuus? Ubi est māter tua?' "
    "Puella: 'Pater meus nōn est. Māter mea nōn est. Ego sōla sum.' "
    "Vir: 'Nōn sōla es. Venī. Ego ad oppidum eō. Tū mēcum ad oppidum īs.' "
    "Puella cum virō ad oppidum it. Vir: 'In oppidō multī virī sunt. In oppidō multae fēminae sunt.' "
    "Puella: 'Ego familiam nōn habeō. Ego sōla sum.' "
    "Vir: 'In oppidō virī bonī sunt. In oppidō fēminae sunt. In oppidō familia est.' "
    "Puella et vir ad oppidum veniunt. Oppidum est parvum sed pulchrum. "
    "In oppidō fēmina est. Fēmina puellam videt. Fēmina est pulchra. Fēmina est bona. "
    "Fēmina: 'Puella, venī. Ego tibi aquam dō. Ego tibi pīrum dō.' "
    "Puella: 'Tū es bona. Tū mihi aquam dās. Tū mihi pīrum dās.' "
    "Puella in oppidō est. Puella aquam habet. Puella pīrum habet. "
    "Puella: 'Ego nōn sōla sum. In oppidō virī bonī sunt. In oppidō fēminae sunt.' "
    "Fēmina puellam videt. Fēmina: 'Puella est bona. Puella est pulchra.' "
    "Puella fēminam videt. Puella: 'Tū es bona. Tū es sīcut māter.' "
    "Fēmina: 'Ego fīliam nōn habeō. Tū es puella bona. Tū es fīlia.' "
    "Puella lacrimat. Puella: 'Ego fīlia nōn sum. Ego puella sum. Ego sōla sum.' "
    "Fēmina: 'Tū nōn sōla es. Tū in oppidō es. Ego hīc sum. Tū hīc es.' "
    "Puella: 'Ego in oppidō sum. Ego puella sum. Ego nōn sōla sum.' "
    "Puella in oppidō est. Puella in oppidō dormit. Puella in oppidō laeta est. "
    "Puella: 'Ego puella sum. Ego in oppidō sum. Ego nōn sōla sum. Ego familiam habeō.' "
    "Fēmina puellam videt. Fēmina: 'Puella est bona. Puella est pulchra. Puella est fīlia mea.' "
    "Puella oculus claudit. Puella dormit. In oppidō puella dormit. "
    "Puella nōn sōla est. Puella in oppidō est. Et puella est laeta."
)

# 中长篇 11: Sōlus in viā — 第一人称独行者的内心独白
STORIES["cap6_11"] = make_story(6, "cap6_11", "Sōlus in viā", "独行路上",
    "13 孤独", "抒情", "G 哲理寓言", "旅人", "中长篇", "第一人称",
    "Ego in viā sum. Via est longa. Via est pulchra. Ego sōlus in viā ambulō. "
    "Ego: \"Ego sōlus sum. Nūllus alius in viā est. Ego sōlus sum — sed nōn timeō. Sōlus esse est līberum. Sōlus esse est bonum.\" "
    "Ego in viā ambulō. Ego multa videō. Ego aquam videō. Aqua in fluviō est. Aqua est pūra. Aqua est bona. Aqua est pulchra. "
    "Ego ad fluvium eō. Ego prope fluvium stō. Ego in aquā mē videō. "
    "Ego: \"Quis est in aquā? Vir in aquā est. Vir in aquā mē spectat. Ille vir est ego. Ego sum vir in aquā. Ego sum vir in viā.\" "
    "Ego ab fluviō abeō. Ego iterum in viā sum. Via est longa. Via est pulchra. Ego sōlus ambulō. "
    "Ego: \"Cūr ego sōlus sum? Ubi sunt amīcī? Ubi est pater? Ubi est māter?\" "
    "Ego: \"Fortasse sōlus esse nōn est malum. Fortasse sōlus esse est bonum. Fortasse sōlus esse est līberum.\" "
    "Ego in viā ambulō. Ego vīllam videō. Vīlla est magna. Vīlla est pulchra. In vīllā virī habitant. In vīllā fēminae habitant. In vīllā puerī et puellae habitant. "
    "Ego: \"In vīllā multī virī sunt. In vīllā multae fēminae sunt. Sed ego — ego in viā sum. Ego sōlus sum.\" "
    "Ego ad vīllam nōn eō. Ego in viā maneō. Via est amīca mea. Via est magistra mea. "
    "Ego: \"Via mē dūcit. Via est longa. Via est pulchra. Via est magistra.\" "
    "Ego iterum ambulō. Ego hortum videō. Hortus est magnus. Hortus est pulcher. In hortō rosae sunt. Rosae sunt pulchrae. Rosae sunt magnae. "
    "Ego: \"Rosae sunt pulchrae. Rosae in hortō sunt. Et rosae nōn sunt sōlae. Rosae cum aliīs rosīs sunt.\" "
    "Ego rosam videō. Rosa est pulchra. Rosa est magna. Ego rosam nōn capiō. Rosa in hortō manet. "
    "Ego: \"Ego quoque nōn maneō. Ego in viā sum. Ego semper ambulō. Ego numquam maneō.\" "
    "Ego: \"Sed fortasse nōn manēre est bonum. Fortasse semper īre est bonum. Fortasse via est domus.\" "
    "Ego in viā stō. Ego oculōs claudō. Ego nihil videō — sed ego multa audiō. "
    "Ego aquam audiō. Aqua in fluviō fluit. Aqua semper fluit. Ego: \"Aqua semper it. Aqua numquam manet. Ego quoque semper eō. Ego numquam maneō.\" "
    "Ego oculōs aperiō. Ego iterum videō. Via est ante mē. Via est longa. Via est pulchra. "
    "Ego: \"Ego nōn iam timeō. Ego mē habeō. Ego viam habeō. Ego cor meum habeō.\" "
    "Ego: \"In corde meō multa sunt. In corde meō via est. In corde meō oppida sunt. In corde meō amīcī sunt.\" "
    "Ego: \"Nōn sum sōlus. Ego mēcum sum. Ego cum amīcīs in corde sum. Ego cum viā in corde sum.\" "
    "Ego iterum ambulō. Via est longa. Via est pulchra. Ego nōn timeō. Ego laetus sum. "
    "Ego: \"Sōlus esse nōn est malum. Sōlus esse est bonum. Sōlus esse est līberum.\" "
    "Ego in viā dormiō. Via est bona. Via est amīca. Via est domus. "
    "Ego: \"Crās iterum ambulābō. Crās iterum vidēbō. Crās iterum erō. Crās iterum in viā erō.\" "
    "Ego oculōs claudō. Ego in viā dormiō. Via est longa — sed ego nōn timeō. Ego sōlus sum. Ego līber sum. Et hoc est bonum."
)

# 中长篇 12: Oppidum in nocte — 夜之城的冷峻描绘
STORIES["cap6_12"] = make_story(6, "cap6_12", "Oppidum in nocte", "夜之城",
    "35 城市", "冷峻", "C 历史与人物", "旅人", "中长篇", "第三人称",
    "Oppidum est parvum. Nūllus vir in oppidō est. Nūlla fēmina in oppidō est. Nūllus puer, nūlla puella in oppidō est. "
    "Oppidum est vacuum. Via est longa. Via est magna. In viā nūllus vir est. In viā nihil est. In viā nihil movet. "
    "Vir sōlus in oppidō est. Vir in viā ambulat. Vir nōn est ex oppidō. Vir est ab aliō oppidō. Vir est sōlus — sed nōn timet. "
    "Vir: \"Hoc oppidum est vacuum. Hoc oppidum est parvum. Ubi sunt virī? Ubi sunt fēminae? Ubi sunt puerī?\" "
    "Vir in viā ambulat. Vir tabernās videt. Tabernae sunt parvae. Tabernae nōn sunt apertae. Fenestrae tabernārum nōn sunt apertae. "
    "Vir: \"In hōc oppidō nihil est. Nihil apertum est. Nihil it. Nihil venit.\" "
    "Vir per viam ambulat. Via est longa. Via est magna. Vir sōlus in viā ambulat. "
    "Vir: \"Fortasse omnēs virī in vīllīs sunt. Fortasse omnēs fēminae in cubiculīs sunt. Fortasse omnēs puerī in vīllīs sunt. Fortasse oppidum dormit.\" "
    "Vir ad portam oppidī it. Porta est magna. Porta est pulchra. Porta est aperta. "
    "Vir: \"Porta est aperta — sed nūllus vir intrat. Porta est aperta — sed nūllus vir exit. Porta est aperta — sed oppidum est vacuum.\" "
    "Vir per portam exit. Vir ex oppidō est. Vir oppidum videt. Vir oppidum ab extrā videt. "
    "Vir: \"Oppidum est parvum. Oppidum est pulchrum. Oppidum est bonum. Sed oppidum est vacuum.\" "
    "Vir mūrōs oppidī videt. Mūrī sunt magnī. Mūrī sunt pulchrī. Mūrī sunt longī. "
    "Vir: \"Mūrī oppidī sunt magnī. Mūrī multa vidērunt. Mūrī multōs virōs vidērunt. Mūrī multa oppida vidērunt.\" "
    "Vir iterum in oppidum intrat. Vir iterum in viā ambulat. Via est longa. Via est vacua. "
    "Vir: \"Oppidum est vacuum — sed oppidum nōn est malum. Oppidum dormit. Oppidum tacet. Oppidum est.\" "
    "Vir in viā stat. Vir audit. Nihil audit. Nihil est. "
    "Vir: \"Nihil est in oppidō. Nihil est in viā. Nihil auditur. Ego sōlus in oppidō sum.\" "
    "Vir iterum ambulat. Vir iterum videt. In viā puer est. Puer est sōlus. Puer est parvus. Puer est bonus. "
    "Vir: \"Puer! Tū es in oppidō. Tū quoque sōlus es, puer. Tū quoque in oppidō ambulās.\" "
    "Puer virum videt. Puer: \"Ego sōlus sum. Ego in oppidō sum. Ego nūllum virum videō. Nunc tē videō.\" "
    "Puer nōn timet. Puer ad virum venit. Puer est bonus. Puer virum amat. "
    "Vir: \"Venī, puer. Ambō in oppidō ambulāmus. Ambō in oppidō sōlī sumus — sed nōn iam sōlī sumus.\" "
    "Vir et puer in oppidō ambulant. Vir et puer in viīs ambulant. Vir et puer prope mūrōs ambulant. Vir et puer prope tabernās ambulant. "
    "Oppidum est vacuum — sed nōn iam vacuum est. Vir et puer in oppidō sunt. Vir et puer in viīs sunt. "
    "Vir et puer stant. Vir puerum videt. Puer virum videt. Vir et puer sunt amīcī. "
    "Vir: \"Oppidum est parvum. Oppidum dormit. Sed nōs — nōs nōn dormīmus. Nōs in oppidō sumus. Nōs duo sumus.\" "
    "Vir: \"In oppidō, vir et puer sunt. Et hoc est bonum. Duo in oppidō sunt. Duo amīcī sunt.\" "
    "Puer: \"Tū es bonus, vir. Ego sōlus eram. Ego in oppidō sōlus eram. Nunc nōn sōlus sum. Nunc tē habeō.\" "
    "Vir: \"Ego quoque sōlus eram. Ego in viā sōlus eram. Nunc nōn sōlus sum. Nunc tē habeō. Nōs duo sumus.\" "
    "Puer: \"Oppidum nōn est vacuum. Nōs in oppidō sumus. Nōs duo sumus.\" "
    "Vir: \"Ita. Oppidum nōn est vacuum. Nōs in oppidō sumus. Nōs duo sumus.\" "
    "Vir oculōs claudit. Puer prope virum dormit. In oppidō, vir et puer — duo amīcī — dormiunt. "
    "Oppidum tacet. Oppidum parvum est. Sed in oppidō, vir et puer sunt. Et oppidum nōn est vacuum."
)

# 中长篇 13: Dominus bonus — 好主人的日常
STORIES["cap6_13"] = make_story(6, "cap6_13", "Dominus bonus", "好主人",
    "06 权力", "白话", "M 伦理与习俗", "罗马人", "中长篇", "第三人称",
    "Dominus in vīllā est. Dominus est vir bonus. Dominus multōs servōs habet. "
    "Servī dominum vident. Servus prīmus: 'Dominus est bonus. Dominus nōn pulsat. Dominus est vir bonus.' "
    "Dominus servum vocat. Dominus: 'Serve, venī. Ego tē vidēre volō.' "
    "Servus ad dominum venit. Servus: 'Hīc sum, domine. Quid est?' "
    "Dominus: 'Aqua est. Aquam portā. Aquam ad mēnsam portā.' "
    "Servus aquam portat. Servus aquam ad mēnsam portat. Servus: 'Aqua est in mēnsā. Est bene?' "
    "Dominus: 'Bene est. Tū bonus servus es. Tū bene portās.' "
    "Servus: 'Dominus bonus est. Ego dominum bonum habeō. Ego laetus sum.' "
    "Dominus in hortum it. Hortus est magnus. Hortus est pulcher. In hortō rosae sunt. "
    "Dominus rosās videt. Dominus: 'Rosae sunt pulchrae. Rosae sunt magnae. Hortus est pulcher.' "
    "Alius servus in hortō est. Servus aquam ad rosās portat. "
    "Servus: 'Domine, ego aquam portō. Ego rosās videō. Rosae sunt pulchrae.' "
    "Dominus: 'Bonus servus es. Hortus est pulcher. Rosae sunt pulchrae. Tū bene portās.' "
    "Servus: 'Dominus est bonus. Dominus nōs videt. Dominus nōs nōn pulsat. Nōs laetī sumus.' "
    "Dominus in vīllam it. Ancilla in vīllā est. Ancilla mēnsam videt. "
    "Ancilla: 'Domine, mēnsa est. Mēnsa est pulchra. Mēnsa est in locō.' "
    "Dominus: 'Bene est. Ancilla bona es. Mēnsa est pulchra. Tū bene es.' "
    "Ancilla: 'Dominus bonus est. Dominus nōn pulsat. Dominus nōn est malus. Dominus est bonus.' "
    "Dominus: 'Ego nōn pulsō. Pulsāre malum est. Servī sunt virī. Servī sunt fēminae. Servī sunt puerī et puellae. Cūr servum pulsāre? Pulsāre malum est.' "
    "Servus prīmus ad dominum venit. Servus: 'Domine, aliī dominī servōs pulsant. Aliī dominī servōs timent. Tū nōn pulsās. Tū nōn timēs.' "
    "Dominus: 'Servus est vir. Servus est bonus. Servus est amīcus.' "
    "Servus prīmus: 'Amīcus? Ego sum amīcus?' "
    "Dominus: 'Tū es amīcus. Amīcus bonus est. Inimīcus malus est. Tū nōn es inimīcus. Tū es amīcus.' "
    "Servus prīmus: 'Dominus bonus est. Dominus est amīcus. Ego laetus sum.' "
    "Dominus in oppidum it. Servus cum dominō it. "
    "In oppidō multī virī sunt. In oppidō multae viae sunt. In oppidō multae tabernae sunt. "
    "Alius dominus in oppidō est. Alius dominus servum suum pulsat. "
    "Alius dominus: 'Serve male! Cūr tū nōn bene portās? Ego tē pulsō!' "
    "Dominus: 'Cūr servum pulsās? Servus est vir. Servus nōn est malus.' "
    "Alius dominus: 'Servus est servus! Servus nōn est vir! Servus nōn est amīcus!' "
    "Dominus: 'Servus meus est amīcus. Servus meus bonus est. Servus meus nōn timet.' "
    "Servus: 'Dominus meus bonus est. Ego nōn timeō. Dominus meus nōn pulsat.' "
    "Alius dominus tacet. Alius dominus servum suum spectat. "
    "Alius dominus: 'Servus tuus tē nōn timet... Servus meus mē timet. Ego servum meum pulsō. Servus meus timet.' "
    "Dominus: 'Nōn pulsā. Servum tuum vidē. Servus tuus est vir. Servus tuus est bonus.' "
    "Alius dominus: 'Fortasse... fortasse tū vērum dīcis. Fortasse ego nōn bonus sum.' "
    "Dominus et servus in vīllam redeunt. In vīllā multī servī sunt. "
    "Dominus servōs vocat. Dominus: 'Servī, venīte. Ego vōs vidēre volō.' "
    "Servī ad dominum veniunt. Servī: 'Domine, nōs hīc sumus. Quid est?' "
    "Dominus: 'Vōs estis bonī servī. Vōs bene portātis. Vōs vīllam vidētis. Vōs hortum vidētis. Ego vōs videō. Vōs bonī estis.' "
    "Servī: 'Dominus nōs videt! Dominus nōs nōn pulsat! Dominus nōs nōn timet! Nōs laetī sumus!' "
    "Dominus: 'Vōs estis amīcī. Vōs nōn estis inimīcī. Vōs estis familia.' "
    "Servus prīmus: 'Familia? Nōs sumus familia?' "
    "Dominus: 'Ita. Vōs estis familia. Ego sum pater. Vōs estis fīliī. Vīlla est domus. Omnēs in vīllā sunt familia.' "
    "Servī rīdent. Servī laetī sunt. Dominus rīdet. Dominus laetus est. "
    "Dominus: 'Hodiē diēs bonus est. Hodiē ego multa vīdī. Hodiē ego multa audīvī. Hodiē ego laetus sum.' "
    "Servī: 'Nōs quoque laetī sumus. Nōs dominum bonum habēmus. Nōs in vīllā bonā sumus.' "
    "Dominus in hortum it. Servī in hortum eunt. Hortus est magnus. Hortus est pulcher. "
    "In hortō rosae sunt. In hortō aqua est. In hortō multa sunt. "
    "Dominus: 'Hīc in hortō, omnēs sumus. Hīc nōn est dominus et servus. Hīc sunt amīcī.' "
    "Servī: 'Nōs amīcī sumus. Dominus nōs videt. Dominus bonus est. Omnēs amīcī sunt.' "
    "Dominus sedet. Servī sedent. Omnēs in hortō sedent. "
    "Dominus oculōs claudit. Dominus: 'Hodiē diēs bonus fuit. Hodiē ego multa vīdī. Hodiē ego laetus sum.' "
    "Servus prīmus: 'Domine, tū nōn sōlus es. Nōs tēcum sumus.' "
    "Dominus: 'Ego nōn sum sōlus. Ego servōs bonōs habeō. Ego amīcōs habeō. Ego familiam habeō.' "
    "Nunc dominus dormit. Servī dormiunt. Vīlla tacet. "
    "In vīllā, dominus et servī dormiunt. Omnēs dormiunt. Et in hāc vīllā, nōn est dominus et servus — sed familia. "
    "Et familia est bona. Familia est pulchra. Familia est omnia."
)

# 中长篇 14: Via ad Graeciam — 希腊人返乡之路
STORIES["cap6_14"] = make_story(6, "cap6_14", "Via ad Graeciam", "通往希腊之路",
    "22 旅程", "白话", "B 神话与传说", "希腊人", "中长篇", "第三人称",
    "Vir in oppidō est. Oppidum est Rōma. Vir Rōmam videt. Vir videt oppidum magnum. Vir videt oppidum pulchrum. "
    "Vir: 'Rōma est magna. Rōma est pulchra. Sed Rōma nōn est vīlla mea. Vīlla mea est in Graeciā. Ego ad Graeciam īre volō.' "
    "Vir in viā est. Via est longa. Via est pulchra. Vir in viā ambulat. "
    "Vir: 'Via ad Brundisium it. Brundisium est oppidum magnum. Brundisium est ad aquam. Ex Brundisiō ad Graeciam itur.' "
    "Vir in viā ambulat. Via est longa. Via est pulchra. In viā multī virī ambulant. "
    "Vir multa oppida videt. Oppida sunt parva. Oppida sunt pulchra. Oppida sunt in Ītaliā. "
    "Vir: 'Ītalia est pulchra. Ītalia est magna. Sed Ītalia nōn est Graecia. Graecia est ubi pater meus est. Graecia est ubi māter mea est.' "
    "Vir multōs virōs in viā videt. Virī cum saccī sunt. Virī ambulant. Virī oppida videt. "
    "Vir cum virō ambulat. Vir: 'Quō īs, vir?' "
    "Alius vir: 'Ad oppidum eō. Ego saccum portō. Ego saccum ad oppidum portō. Et tū? Quō īs?' "
    "Vir: 'Ego ad Graeciam eō. Ad vīllam meam eō. Ad patrem et mātrem eō.' "
    "Alius vir: 'Graecia est longē. Via est longa. Sed via est pulchra.' "
    "Vir: 'Ita. Via est longa — sed via est pulchra. Et in viā multī virī bonī sunt.' "
    "Post multōs diēs vir ad Brundisium venit. Brundisium est oppidum magnum. Brundisium est pulchrum. "
    "Vir: 'Brundisium! Hīc est aqua. Hīc est via ad Graeciam.' "
    "Vir aquam videt. Aqua est magna. Aqua est pulchra. Aqua est longa. "
    "Vir: 'Aqua est magna. Aqua est pulchra. Per aquam ad Graeciam itur.' "
    "Vir in aquā est. Vir in magnā aquā est. Vir aquam videt. Vir aquam audit. "
    "Vir: 'Aqua est magna. Aqua est pulchra. Aqua est via. Ego in aquā sum. Inter Ītaliam et Graeciam sum.' "
    "Vir: 'Nōn iam in Ītaliā sum. Sed nōn iam in Graeciā sum. In aquā sum. Aqua est longa.' "
    "Vir: 'Quid est inter terrās? Aqua est. Via est. Et cor est. Cor meum ad Graeciam it.' "
    "Post multōs diēs vir Graeciam videt. Vir Graeciam videt! "
    "Vir: 'Graecia! Graecia! Ego Graeciam videō! Graecia est pulchra! Graecia est magna!' "
    "Vir in Graeciā est. Vir in viā Graecā ambulat. Vir oppida Graeca videt. "
    "Vir: 'Haec est Graecia. Haec est terra patris meī. Haec est terra mātris meae. Ego domī sum.' "
    "Vir oppidum suum videt. Oppidum est parvum. Oppidum est pulchrum. Oppidum est bonum. "
    "Vir: 'Hoc est oppidum meum. Hoc est oppidum ubi pater meus est. Hoc est oppidum ubi māter mea est.' "
    "Pater in oppidō est. Pater fīlium videt. Pater fīlium vocat. "
    "Pater: 'Fīlī! Tū ades! Tū in oppidō es! Tū domum ades!' "
    "Vir: 'Pater! Ego hīc sum! Ego domum adsum! Ego in Graeciā sum! Ego laetus sum!' "
    "Pater et fīlius in viā stant. Pater fīlium videt. Fīlius patrem videt. "
    "Pater fīlium tenet. Fīlius patrem tenet. Pater et fīlius laetī sunt. "
    "Pater: 'Tū vēnistī. Tū in Graeciā es. Tū nōn iam sōlus es.' "
    "Vir: 'Ego domī sum. Via fuit longa — sed via ad oppidum dūxit. Et nunc ego domī sum.' "
    "In Graeciā, in oppidō parvō, pater et fīlius sunt. Pater et fīlius laetī sunt. "
    "Via longa est — sed oppidum est prope. Et vir — vir bonus — nōn iam in viā est. Vir domī est. "
    "Et pater et fīlius in oppidō sunt. Et ambo sunt laetī. Et ambo sunt bonī."
)

# 长篇 15: Pater et Fīlius — 父与子的深度对话
STORIES["cap6_15"] = make_story(6, "cap6_15", "Pater et Fīlius", "父与子",
    "30 威严与慈爱", "精炼", "A LLPSI宇宙", "罗马人", "长篇", "对话体",
    "Pater in vīllā est. Fīlius in vīllā est. Pater fīlium vocat. Pater fīlium videt. "
    "Pater: 'Fīlī, venī. Ego tē vidēre volō. Ego tē audīre volō.' "
    "Fīlius ad patrem venit. Fīlius: 'Pater, cūr mē vocās? Ego in hortō eram. Ego rosās vidēbam. Rosae sunt pulchrae.' "
    "Pater: 'Rosae sunt pulchrae — sed tū es pulchrior. Tū es fīlius meus. Tū es puer bonus. Ego tē videō et laetus sum.' "
    "Fīlius tacet. Fīlius patrem spectat. "
    "Fīlius: 'Pater, tū es magnus. Ego sum parvus. Tū es bonus. Ego sum... nōn bonus?' "
    "Pater: 'Tū es bonus! Tū es puer bonus. Tū es puer pulcher. Tū es fīlius meus. Cūr dīcis tū nōn bonus es?' "
    "Fīlius: 'Pater, ego tē timeō.' "
    "Pater tacet. Pater fīlium spectat. Pater: 'Cūr mē timēs, fīlī? Ego tē nōn pulsō. Ego tē nōn timeō. Ego tē videō et laetus sum.' "
    "Fīlius: 'Quia tū es magnus. Quia tū clāmās. Quia quandō tū clāmās, ego timeō.' "
    "Pater: 'Ego clāmō. Ita. Ego clāmō. Sed ego nōn clāmō quod tū malus es. Ego clāmō quod multa sunt. Pecūnia est. Oppidum est. Imperium est.' "
    "Fīlius: 'Quid est imperium, pater?' "
    "Pater: 'Imperium est magnum. Imperium est multum. Sed tū — tū nōn es imperium. Tū es fīlius. Tū es bonus.' "
    "Fīlius: 'Sed quandō tū clāmās, ego timeō. Ego in cubiculō meō sum. Ego tē audiō. Et ego plōrō.' "
    "Pater oculōs claudit. Pater: 'Ego nōn vidēbam. Ego nōn vidēbam tē plōrāre. Cūr nōn mihi hoc dīcis?' "
    "Fīlius: 'Quia tū es pater. Pater nōn plōrat. Pater nōn timet. Pater est... pater.' "
    "Pater: 'Fīlī, pater quoque plōrat. Pater quoque timet. Pater quoque est vir. Et vir — vir plōrat. Vir timet. Vir est... vir.' "
    "Fīlius: 'Tū plōrās, pater? Tū timēs?' "
    "Pater: 'Ita. Ego plōrō. Ego timeō. Ego timeō... ego timeō nē tū mē nōn videās ut bonum. Ego timeō nē tū mē timeās.' "
    "Fīlius ad patrem it. Fīlius patrem tenet. Fīlius: 'Pater, ego tē videō. Ego tē audiō. Tū es bonus. Tū es pater bonus. Ego nōn timeō.' "
    "Pater: 'Et quandō tū plōrās, ego tē videō — et ego tē videō ut bonum. Et quandō tū dormīs, ego tē videō — et ego laetus sum.' "
    "Pater: 'Fīlī, tū vīs audīre verba? Verba dē patre meō?' "
    "Fīlius: 'Ita, pater. Verba dē patre tuō.' "
    "Pater: 'Pater meus quoque clāmāvit. Et ego eum timēbam. Et ego in cubiculō meō plōrābam.' "
    "Fīlius: 'Tū quoque patrem timēbās? Tū — pater meus — timēbās?' "
    "Pater: 'Ita. Pater meus erat magnus. Pater meus erat bonus. Et ego eram parvus. Et ego timēbam.' "
    "Fīlius: 'Et nunc? Nunc tū nōn iam timēs?' "
    "Pater: 'Nunc pater meus nōn iam est. Et nunc ego eum videō in corde meō. Nunc ego eum nōn timeō. Nunc ego eum bonum videō.' "
    "Fīlius: 'Pater, ego tē in corde meō habeō. Ego tē semper in corde meō habeō. Tū es in corde meō.' "
    "Pater: 'Et ego tē in corde meō habeō, fīlī. Tū es in corde meō. Tū es bonus. Tū es fīlius bonus.' "
    "Fīlius: 'Et ego tē in corde meō habeō, pater. Tū es in corde meō. Semper.' "
    "Pater fīlium tenet. Pater: 'Tū es bonus fīlius. Tū es melior quam ego. Ego clāmō — sed tū nōn clāmās. Ego timeō — sed tū nōn timēs.' "
    "Fīlius: 'Ego quoque timeō, pater. Sed nunc minus timeō. Nunc tē videō. Nunc tē audiō. Nunc tē... videō.' "
    "Pater: 'Quid vidēs, fīlī?' "
    "Fīlius: 'Videō patrem nōn esse magnum — patrem esse virum. Patrem esse bonum — etiam quandō clāmat.' "
    "Pater rīdet. Pater: 'Tū es bonus, fīlī. Tū es melior quam pater tuus. Tū mē vidēs. Tū mē audīs. Tū mē bonum facis.' "
    "Fīlius: 'Nōn ego faciō, pater. Ego sum fīlius tuus. Ego ā tē videō. Ego ā tē audiō. Ego ā tē multa videō.' "
    "Pater: 'Quid ā mē vidēs, fīlī?' "
    "Fīlius: 'Videō quid est bonus. Videō quid est timor. Videō quid est familia.' "
    "Pater: 'Et quid est familia, fīlī?' "
    "Fīlius: 'Familia est ubi duo — pater et fīlius — sunt ūnum. Familia est ubi timor abit et bonus est.' "
    "Pater: 'Ita, fīlī. Ita. Pater et fīlius — duo virī, sed ūnum cor. Et in corde, bonus est.' "
    "Pater et fīlius in hortum eunt. Hortus est magnus. Hortus est pulcher. In hortō rosae sunt. In hortō aqua est. "
    "Fīlius: 'Pater, hortus est pulcher. Rosae sunt pulchrae. Aqua est pulchra. Hīc est bonum.' "
    "Pater: 'Ita, fīlī. Hīc est bonum. Et tū quoque pulcher es. Tū es pulchrior quam rosae. Tū es pulchrior quam aqua.' "
    "Fīlius: 'Pater, ego nōn iam timeō. Ego laetus sum. Hīc in hortō, ego laetus sum.' "
    "Pater: 'Ego quoque laetus sum, fīlī. Ego quoque nōn iam timeō. Timor abiit. Bonus est.' "
    "Pater et fīlius in hortō sunt. Pater fīlium tenet. Fīlius patrem tenet. "
    "In hortō, pater et fīlius sunt. Duo virī — sed ūnum cor. "
    "Et in illō corde, neque timor neque clāmor — sōlum bonus. Sōlum pater et fīlius. Sōlum familia. "
    "Pater: 'Fīlī, hodiē diēs bonus est. Hodiē ego multa audīvī. Hodiē ego multa vīdī. Hodiē ego tē videō.' "
    "Fīlius: 'Et ego tē videō, pater. Hodiē diēs bonus est. Hodiē ego nōn timeō. Hodiē ego laetus sum.' "
    "Pater et fīlius oculōs claudunt. Pater et fīlius dormiunt. "
    "In hortō, pater et fīlius dormiunt. Et duo laetī sunt. Et duo bonī sunt. "
    "Et familia est bona. Et familia est pulchra. Et familia est omnia."
)

# 长篇 16: Dominus et servus — 主与仆的漫长一日
STORIES["cap6_16"] = make_story(6, "cap6_16", "Dominus et servus", "主与仆",
    "58 主人与奴隶", "白话", "M 伦理与习俗", "罗马人", "长篇", "对话体",
    "Dominus in vīllā est. Servus in vīllā est. Dominus servum vocat. "
    "Dominus: 'Serve, venī! Ego tē hīc vidēre volō.' "
    "Servus ad dominum currit. Servus: 'Hīc sum, domine. Quid est?' "
    "Dominus: 'Mēnsa est. Mēnsa nōn est in locō suō. Portā mēnsam!' "
    "Servus mēnsam portat. Mēnsa est magna. Servus mēnsam pōnit. "
    "Servus: 'Mēnsa in locō est, domine. Est bene?' "
    "Dominus: 'Bene est. Tū bene portās, serve. Tū bonus servus es.' "
    "Servus: 'Domine bonus est. Ego dominum bonum habeō. Ego laetus sum.' "
    "Dominus: 'Serve, cūr tū bene portās? Aliī servī nōn bene portant.' "
    "Servus: 'Domine, ego servus sum. Servus dominō pāret. Servus portat. Ego bene portō quod dominus bonus est.' "
    "Dominus: 'Ego bonus sum? Cūr tū mē bonum vidēs? Ego dominus sum. Dominus imperat. Dominus nōn bonus est.' "
    "Servus: 'Domine, tū mē nōn pulsās. Aliī dominī servōs pulsant. Tū nōn pulsās. Tū bonus es.' "
    "Dominus: 'Servus bonus est. Servus nōn est malus. Ego servum bonum habeō. Ego laetus sum.' "
    "Servus: 'Et ego laetus sum, domine. Ego dominum bonum habeō.' "
    "Dominus in hortum it. Servus cum dominō it. Hortus est magnus. Hortus est pulcher. "
    "In hortō rosa est. Rosa est pulchra. Rosa est magna. "
    "Dominus: 'Hortus est pulcher. Rosa est pulchra. Aqua in hortō est. Aqua est bona.' "
    "Servus: 'Hortus est pulcher, domine. Ego hortum videō. Ego rosam videō. Ego aquam videō.' "
    "Dominus: 'Serve, portā aquam ad mēnsam!' "
    "Servus aquam portat. Servus aquam ad mēnsam portat. "
    "Servus: 'Aqua in mēnsā est, domine.' "
    "Dominus: 'Bene. Tū bonus servus es. Tū aquam bene portās.' "
    "Dominus: 'Serve, venī. Ego tē interrogō.' "
    "Servus: 'Quid est, domine? Ego hīc sum.' "
    "Dominus: 'Cūr tū laetus es? Servus nōn est līber. Servus nōn habet pecūniam. Servus nōn habet vīllam. Cūr servus laetus est?' "
    "Servus tacet. Servus dominum spectat. "
    "Servus: 'Domine, ego servus sum. Sed ego cor habeō. In corde meō, ego līber sum. Cor meum est līberum.' "
    "Dominus: 'Cor tuum est līberum? Quid est in corde tuō?' "
    "Servus: 'In corde meō est amor. In corde meō est dominus bonus. In corde meō est hortus pulcher. In corde meō est rosa. In corde meō est aqua. In corde meō multa sunt.' "
    "Dominus: 'Et in corde meō? Quid est in corde meō?' "
    "Servus: 'Domine, in corde tuō est servus bonus. In corde tuō est vīlla pulchra. In corde tuō est pecūnia. In corde tuō multa sunt.' "
    "Dominus: 'Tū vidēs in corde meō? Tū vidēs quid in corde meō est?' "
    "Servus: 'Domine, ego videō. Ego videō dominum. Ego videō dominum bonum. Ego videō dominum quī amat.' "
    "Dominus: 'Ego servum...? Ego dominus sum. Dominus servum nōn amat. Dominus imperat.' "
    "Servus: 'Domine, tū bonus es. Tū servum amās. Tū mē amās. Ego videō.' "
    "Dominus: 'Servus videt. Servus audit. Servus bonus est. Ego... ego servum...?' "
    "Servus: 'Domine, amor est bonus. Amor nōn est malus. Dominus bonus servum amat. Servus bonus dominum amat.' "
    "Dominus: 'Et tū? Tū mē amās?' "
    "Servus: 'Ego dominum... ego dominum bonum... ego dominum meum... in corde habeō.' "
    "Dominus: 'Cūr? Cūr servus dominum amat?' "
    "Servus: 'Quod dominus bonus est. Quod dominus nōn pulsat. Quod dominus nōn timet. Quod dominus videt. Quod dominus audit.' "
    "Dominus: 'Ego videō. Ego audiō. Ego... ego laetus sum.' "
    "Servus: 'Et ego laetus sum, domine. Ego laetus sum quod dominus bonus est.' "
    "Dominus: 'Serve, tū bonus es. Tū nōn servus es — tū amīcus es. Tū amīcus bonus es.' "
    "Servus: 'Amīcus? Ego amīcus sum?' "
    "Dominus: 'Amīcus est. Amīcus bonus est. Inimīcus malus est. Tū nōn es inimīcus. Tū es amīcus.' "
    "Servus: 'Domine, ego amīcus sum. Ego nōn sum inimīcus. Ego amīcus bonus sum.' "
    "Dominus: 'Et ego amīcus sum. Ego amīcus tuus sum.' "
    "Dominus et servus in hortō sunt. Dominus et servus rosam vident. Dominus et servus aquam vident. "
    "Dominus: 'Hortus est pulcher. Rosa est pulchra. Aqua est bona. Et tū, serve — tū quoque bonus es.' "
    "Servus: 'Et tū, domine — tū bonus es. Tū amīcus bonus es.' "
    "Dominus: 'Duo in hortō sumus. Duo amīcī sumus. Dominus et servus — sed amīcī.' "
    "Servus: 'Amīcī. Dominus et servus — amīcī.' "
    "Dominus oculōs claudit. Servus oculōs claudit. Dominus et servus in hortō dormiunt. "
    "Duo in hortō sunt. Duo dormiunt. Duo amīcī sunt. "
    "Et in hortō, rosa est. Et in hortō, aqua est. Et in hortō, dominus et servus — duo amīcī — dormiunt."
)

# 长篇 17: In viā — 第一人称旅行者的罗马之旅
STORIES["cap6_17"] = make_story(6, "cap6_17", "In viā", "在路上",
    "27 旅行", "抒情", "C 历史与人物", "旅人", "长篇", "第一人称",
    "Ego in viā sum. Via est longa. Via est pulchra. Ego in viā ambulō. Ego nōn currō — ego ambulō. "
    "Via est longa, et ego multa vidēre volō. Ego multa oppida videō. Ego multōs virōs videō. "
    "Prīmum oppidum est parvum. In oppidō paucī virī sunt. In oppidō ūna taberna est. "
    "Ego in tabernam eō. Tabernārius in tabernā est. "
    "Tabernārius: 'Salvē, vir! Quō īs?' "
    "Ego: 'Ad Rōmam eō. Rōma est oppidum magnum. Ego Rōmam vidēre volō.' "
    "Tabernārius: 'Rōma est magna. Rōma est pulchra. Via ad Rōmam est longa. Tū sōlus es — cūr sōlus Rōmam īs?' "
    "Ego: 'Ego sōlus sum — sed nōn timeō. Via est pulchra. Via est longa. Ego in viā laetus sum.' "
    "Ego ex oppidō exeō. Ego in viā sum. Via est longa. Via est pulchra. "
    "Ego multōs virōs in viā videō. Vir cum saccō est. Fēmina cum puerō est. Puer cum puellā est. "
    "Ego cum virō ambulō. Vir: 'Quō īs, vir?' "
    "Ego: 'Ad Rōmam eō. Et tū? Quō īs?' "
    "Vir: 'Ego ad oppidum eō. Ego saccum portō. Ego saccum ad oppidum portō.' "
    "Ego: 'Vīta tua est bona?' "
    "Vir: 'Vīta mea est bona. Ego saccum portō. Ego in viā sum. Ego multa videō. Ego laetus sum.' "
    "Ego: 'Ego quoque in viā sum. Ego quoque multa videō. Ego quoque laetus sum.' "
    "Vir: 'Via est longa — sed via est pulchra. In viā multī virī sunt. In viā multae fēminae sunt. Nōn sōlus es.' "
    "Ego: 'Ego nōn sōlus sum. In viā multī virī sunt. In viā multae fēminae sunt. Via est bona.' "
    "Ego ā virō abeō. Ego in viā ambulō. Via est longa. Via est pulchra. "
    "Secundum oppidum est magnum. In oppidō multī virī sunt. In oppidō multae fēminae sunt. In oppidō multae viae sunt. "
    "Ego in oppidō sum. Ego multa videō. Ego multās viās videō. Ego multās portās videō. Ego multōs virōs videō. "
    "Ego: 'Hoc oppidum est magnum. Hoc oppidum est pulchrum. Sed Rōma est maior. Rōma est pulchrior. Ego ad Rōmam eō.' "
    "Ego in viā sum. Via est longa. Ego ambulō. Ego nōn currō. Ego ambulō — et videō. "
    "Ego prope fluvium ambulō. Fluvius est magnus. Fluvius est longus. Fluvius est pulcher. "
    "Ego: 'Fluvius est pulcher. Aqua in fluviō est. Aqua est bona. Aqua est pūra. Ego aquam videō. Ego aquam audiō.' "
    "Ego prope fluvium dormiō. Fluvius est prope. Aqua est prope. Ego prope aquam dormiō. "
    "Tertium oppidum est parvum. Oppidum est prope viam. In oppidō vīlla est. Vīlla est magna. Vīlla est pulchra. "
    "Ego vīllam videō. In vīllā virī sunt. In vīllā fēminae sunt. In vīllā puerī et puellae sunt. "
    "Ego: 'Vīlla est pulchra. In vīllā familia est. Pater et māter in vīllā sunt. Fīlius et fīlia in vīllā sunt. Familia est bona.' "
    "Ego: 'Ego familiam nōn habeō. Ego vīllam nōn habeō. Ego in viā sum. Sed ego nōn malus sum. Via est familia mea. Via est vīlla mea.' "
    "Ego in viā sum. Ego ambulō. Ego multa videō. "
    "Quārtum oppidum est prope īnsulam. Īnsula est parva. Īnsula est pulchra. "
    "Ego īnsulam videō. Ego: 'Īnsula est pulchra. Īnsula est in aquā. Aqua est magna. Aqua est pulchra.' "
    "Ego: 'In īnsulā virī sunt. In īnsulā fēminae sunt. In īnsulā vīta est. Sed ego — ego in viā sum. Ego ad Rōmam eō.' "
    "Ego in viā ambulō. Via est longa. Ego multa oppida videō. Ego multōs virōs videō. Ego multās fēminās videō. "
    "Quīntum oppidum est prope Rōmam. Ego Rōmam procul videō. "
    "Ego: 'Rōma! Rōma est prope! Ego Rōmam videō! Rōma est magna! Rōma est pulchra!' "
    "Ego in viā currō. Ego nōn ambulō — ego currō! Rōma est prope! "
    "Ego ad portam Rōmae veniō. Porta est magna. Porta est pulchra. Porta Rōmae est. "
    "Ego: 'Haec est porta Rōmae. Per hanc portam multī virī veniunt. Per hanc portam ego veniō.' "
    "Ego per portam eō. Ego in Rōmā sum. "
    "Ego: 'Rōma! Ego in Rōmā sum! Ego oppidum magnum videō! Ego oppidum pulchrum videō!' "
    "Ego in viīs Rōmae ambulō. Viae sunt longae. Viae sunt pulchrae. In viīs multī virī sunt. In viīs multae fēminae sunt. "
    "Ego: 'Rōma est plēna virōrum. Rōma est plēna fēminārum. Rōma est plēna puerōrum et puellārum. Rōma est plēna vītae.' "
    "Ego in viā Rōmae stō. Ego omnia videō. Ego omnia audiō. "
    "Ego: 'Ego in Rōmā sum. Ego nōn sōlus sum. Rōma est mēcum. Virī Rōmae sunt mēcum. Fēminae Rōmae sunt mēcum.' "
    "Ego: 'Via fuit longa. Ego multa vīdī. Ego multōs virōs vīdī. Ego multa oppida vīdī. Et nunc — nunc ego in Rōmā sum.' "
    "Ego: 'Via ad Rōmam est longa — sed via est pulchra. Et Rōma est pulchra. Rōma est magna. Rōma est bona.' "
    "Ego in Rōmā sedeō. Ego oculōs claudō. Ego omnia in corde meō videō. "
    "In corde meō est via longa. In corde meō sunt oppida multa. In corde meō sunt virī multī. In corde meō sunt fēminae multae. "
    "In corde meō est Rōma. Rōma est in corde meō. Via est in corde meō. Omnia in corde meō sunt. "
    "Ego: 'Ego in Rōmā sum. Ego in viā fuī. Ego multa vīdī. Ego multa audīvī. Et ego laetus sum.' "
    "Ego in Rōmā dormiō. Rōma est magna. Rōma est pulchra. Ego in Rōmā dormiō. "
    "Via fuit longa. Ego multa vīdī. Et nunc — nunc ego in Rōmā sum. Et ego laetus sum. Et hoc est bonum."
)


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