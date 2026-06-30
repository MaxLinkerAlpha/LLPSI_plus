#!/usr/bin/env python3
"""rewrite_cap1.py — 重写 Cap.1 的 9 篇短篇为 中篇/中长篇。
严格使用 Cap.1-3 词汇，通过排比和重复扩充篇幅。
专有名词仅使用 evaluate_v2 小写化后仍能匹配的 (Roma, Italia, Sicilia 等)。
"""

import json, re, sys, os
from pathlib import Path

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

# ============================================================
# Cap.1: 9 篇 → 6 中篇 + 3 中长篇
# 词汇策略：只用 Cap.1-3 词汇，大量重复。Cap.4+ 词汇控制在 3-5 个以内。
# 专有名词仅用 evaluate_v2 小写还原后能匹配的：
#   Roma, Italia, Europa, Graecia, Hispania, Sicilia, Sardinia, Corsica,
#   Melita, Syria, Arabia, Tiberis, Rhenus, Brundisium, Tusculum,
#   Lemnos, Samos, Chios, Britannia
# ============================================================

STORIES = {}

# ---- 中篇 (300-500词) x6 ----

STORIES["cap1_01"] = {
    "title_la": "Rōma et Ītalia",
    "title_zh": "罗马与意大利",
    "target_chapter": 1,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma est in Italiā. Italia est in Eurōpā. Rōma est oppidum. Rōma est oppidum magnum. "
        "Italia nōn est oppidum. Italia est terra. Eurōpa est terra. "
        "Ubi est Rōma? Rōma est in Italiā. Ubi est Italia? Italia est in Eurōpā. "
        "Estne Rōma in Graeciā? Rōma nōn est in Graeciā. Rōma est in Italiā. "
        "Estne Italia in Graeciā? Italia nōn est in Graeciā. Italia est in Eurōpā. "
        "In Italiā multa oppida sunt. Rōma est oppidum prīmum. "
        "Brundisium est oppidum. Brundisium est in Italiā. Brundisium est oppidum parvum. "
        "Tusculum est oppidum. Tusculum est in Italiā. Tusculum est oppidum parvum. "
        "Rōma est magnum oppidum. Brundisium et Tusculum sunt parva oppida. "
        "Sunt tria oppida in Italiā: Rōma, Brundisium, Tusculum. "
        "Rōma est prīmum. Brundisium est secundum. Tusculum est tertium. "
        "Rōma est Rōmāna. Italia est Rōmāna. Brundisium est Rōmānum. Tusculum est Rōmānum. "
        "Rōma est in imperiō. Italia est in imperiō. Brundisium est in imperiō. Tusculum est in imperiō. "
        "Graecia est in Eurōpā. Graecia est terra. Graecia nōn est in Italiā. "
        "Graecia est antīqua. Italia est antīqua. Rōma est antīqua. "
        "Italia est Rōmāna. Graecia nōn est Rōmāna. Graecia est Graeca. "
        "Estne Graecia in imperiō? Graecia nōn est in imperiō. Graecia est lībera. "
        "Italia est prīma. Graecia est secunda. "
        "In Italiā multī populī sunt. In Graeciā multī populī sunt. "
        "Rōma est caput Italiae. Rōma est caput imperiī. "
        "Rōma est magna. Italia est magna. Imperium Rōmānum est magnum. "
        "Rōma est prīma. Italia est prīma. Imperium Rōmānum est prīmum. "
        "Rōma est in Italiā. Italia est in Eurōpā. Rōma est caput. Italia est terra. "
        "Tria oppida: Rōma, Brundisium, Tusculum. Tria in Italiā. Tria Rōmāna."
    )
}

STORIES["cap1_02"] = {
    "title_la": "Trēs īnsulae magnae",
    "title_zh": "三大岛",
    "target_chapter": 1,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Sicilia est īnsula. Sicilia est in marī. Sicilia est prope Italiam. "
        "Sicilia est īnsula magna. Sicilia nōn est parva. Sicilia est Rōmāna. "
        "Sardinia est īnsula. Sardinia est in marī. Sardinia est prope Corsicam. "
        "Sardinia est īnsula magna. Sardinia nōn est parva. Sardinia est Rōmāna. "
        "Corsica est īnsula. Corsica est in marī. Corsica est prope Sardiniam. "
        "Corsica est īnsula parva. Corsica nōn est magna. Corsica est Rōmāna. "
        "Sunt trēs īnsulae: Sicilia, Sardinia, Corsica. "
        "Sicilia est prīma. Sardinia est secunda. Corsica est tertia. "
        "Sicilia est magna. Sardinia est magna. Corsica est parva. "
        "Sicilia est in imperiō. Sardinia est in imperiō. Corsica est in imperiō. "
        "Trēs īnsulae in imperiō sunt. Trēs sunt Rōmānae. "
        "Ubi est Sicilia? Sicilia est in marī. Sicilia est prope Italiam. "
        "Ubi est Sardinia? Sardinia est in marī. Sardinia est prope Corsicam. "
        "Ubi est Corsica? Corsica est in marī. Corsica est prope Sardiniam. "
        "Estne Sicilia in Italiā? Sicilia nōn est in Italiā. Sicilia est īnsula. "
        "Estne Sardinia in Italiā? Sardinia nōn est in Italiā. Sardinia est īnsula. "
        "Estne Corsica in Italiā? Corsica nōn est in Italiā. Corsica est īnsula. "
        "Sicilia est prōvincia. Sardinia est prōvincia. Corsica est prōvincia. "
        "Trēs prōvinciae sunt. Trēs in imperiō sunt. Trēs Rōmānae sunt. "
        "In Siciliā multa oppida sunt. In Sardiniā multa oppida sunt. In Corsicā pauca oppida sunt. "
        "Sicilia est magna et multa. Sardinia est magna et multa. Corsica est parva et pauca. "
        "Sicilia est prīma īnsula. Sardinia est secunda. Corsica est tertia. "
        "Trēs sunt. Trēs īnsulae. Trēs prōvinciae. Trēs in imperiō."
    )
}

STORIES["cap1_03"] = {
    "title_la": "Tria flūmina Rōmāna",
    "title_zh": "三条罗马河",
    "target_chapter": 1,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tiberis est fluvius. Tiberis est in Italiā. Tiberis est fluvius parvus. "
        "Tiberis nōn est magnus. Tiberis est Rōmānus. "
        "Rhēnus est fluvius. Rhēnus est in Germāniā. Rhēnus est fluvius magnus. "
        "Rhēnus nōn est parvus. Rhēnus nōn est Rōmānus. "
        "Dānuvius est fluvius. Dānuvius est in imperiō. Dānuvius est fluvius magnus. "
        "Dānuvius nōn est parvus. Dānuvius nōn est Rōmānus. "
        "Sunt tria flūmina: Tiberis, Rhēnus, Dānuvius. "
        "Tiberis est prīmus. Rhēnus est secundus. Dānuvius est tertius. "
        "Tiberis est parvus — sed Rōmānus. "
        "Rhēnus est magnus — sed nōn Rōmānus. "
        "Dānuvius est magnus — sed nōn Rōmānus. "
        "Ubi est Tiberis? Tiberis est in Italiā. Tiberis est in imperiō. "
        "Ubi est Rhēnus? Rhēnus est in Germāniā. Rhēnus nōn est in imperiō. "
        "Ubi est Dānuvius? Dānuvius est in imperiō. Dānuvius est in multīs terrīs. "
        "Estne Tiberis in Graeciā? Tiberis nōn est in Graeciā. Tiberis est in Italiā. "
        "Estne Rhēnus in Italiā? Rhēnus nōn est in Italiā. Rhēnus est in Germāniā. "
        "Estne Dānuvius in Italiā? Dānuvius nōn est in Italiā. Dānuvius est in multīs terrīs. "
        "Tiberis est fluvius parvus. Rhēnus est fluvius magnus. Dānuvius est fluvius magnus. "
        "Tiberis est in Italiā. Rhēnus est in Germāniā. Dānuvius est in imperiō. "
        "Tiberis est Rōmānus. Rhēnus nōn est Rōmānus. Dānuvius nōn est Rōmānus. "
        "Tria flūmina sunt. Tiberis est prīmus. Rhēnus est secundus. Dānuvius est tertius. "
        "Tiberis est parvus — sed prīmus. Rhēnus est magnus — sed secundus. "
        "Dānuvius est magnus — sed tertius. "
        "Tria flūmina. Trēs aquae. Trēs terrae."
    )
}

STORIES["cap1_04"] = {
    "title_la": "Trēs prōvinciae īnsulārum",
    "title_zh": "三大岛屿行省",
    "target_chapter": 1,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Sicilia est prōvincia. Sicilia est in imperiō. Sicilia est Rōmāna. "
        "Sicilia est īnsula. Sicilia est īnsula magna. Sicilia nōn est parva. "
        "Sardinia est prōvincia. Sardinia est in imperiō. Sardinia est Rōmāna. "
        "Sardinia est īnsula. Sardinia est īnsula magna. Sardinia nōn est parva. "
        "Corsica est prōvincia. Corsica est in imperiō. Corsica est Rōmāna. "
        "Corsica est īnsula. Corsica est īnsula parva. Corsica nōn est magna. "
        "Trēs prōvinciae sunt. Trēs īnsulae sunt. Trēs in imperiō sunt. "
        "Sicilia est prīma. Sardinia est secunda. Corsica est tertia. "
        "Sicilia est prīma prōvincia. Sardinia est secunda. Corsica est tertia. "
        "Ubi est Sicilia? Sicilia est in marī. Sicilia est prope Italiam. "
        "Ubi est Sardinia? Sardinia est in marī. Sardinia est prope Corsicam. "
        "Ubi est Corsica? Corsica est in marī. Corsica est prope Sardiniam. "
        "Estne Sicilia in Italiā? Sicilia nōn est in Italiā. Sicilia est īnsula in marī. "
        "Estne Sardinia in Italiā? Sardinia nōn est in Italiā. Sardinia est īnsula in marī. "
        "Estne Corsica in Italiā? Corsica nōn est in Italiā. Corsica est īnsula in marī. "
        "Sicilia est in imperiō. Sardinia est in imperiō. Corsica est in imperiō. "
        "Trēs īnsulae in imperiō sunt. Trēs prōvinciae in imperiō sunt. "
        "In Siciliā multa oppida sunt. In Sardiniā multa oppida sunt. In Corsicā pauca oppida sunt. "
        "Sicilia est magna et multa. Sardinia est magna et multa. Corsica est parva et pauca. "
        "Sicilia est Rōmāna. Sardinia est Rōmāna. Corsica est Rōmāna. "
        "Trēs īnsulae sunt Rōmānae. Trēs prōvinciae sunt Rōmānae. "
        "Italia est prōvincia. Italia nōn est īnsula. Italia est terra. "
        "Italia est in imperiō. Italia est Rōmāna. Italia est prīma prōvincia. "
        "Sicilia est secunda. Sardinia est tertia. "
        "Trēs īnsulae — Sicilia, Sardinia, Corsica. Trēs prōvinciae. Trēs in imperiō."
    )
}

STORIES["cap1_05"] = {
    "title_la": "Īnsulae Graecae",
    "title_zh": "希腊诸岛",
    "target_chapter": 1,
    "theme": "18 自然",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Graecia est in Eurōpā. Graecia est terra. Graecia est antīqua. "
        "In Graeciā multae īnsulae sunt. Graecia nōn est īnsula. Graecia est terra. "
        "Samos est īnsula. Samos est in marī. Samos est Graeca. Samos est īnsula parva. "
        "Chios est īnsula. Chios est in marī. Chios est Graeca. Chios est īnsula parva. "
        "Lēmnos est īnsula. Lēmnos est in marī. Lēmnos est Graeca. Lēmnos est īnsula parva. "
        "Sunt trēs īnsulae Graecae: Samos, Chios, Lēmnos. "
        "Samos est prīma. Chios est secunda. Lēmnos est tertia. "
        "Samos est parva. Chios est parva. Lēmnos est parva. "
        "Trēs īnsulae parvae sunt. Trēs in marī sunt. Trēs Graecae sunt. "
        "Ubi est Samos? Samos est in marī. Samos est prope Graeciam. "
        "Ubi est Chios? Chios est in marī. Chios est prope Graeciam. "
        "Ubi est Lēmnos? Lēmnos est in marī. Lēmnos est prope Graeciam. "
        "Estne Samos in Italiā? Samos nōn est in Italiā. Samos est Graeca. "
        "Estne Chios in Italiā? Chios nōn est in Italiā. Chios est Graeca. "
        "Estne Lēmnos in Italiā? Lēmnos nōn est in Italiā. Lēmnos est Graeca. "
        "Samos nōn est Rōmāna. Chios nōn est Rōmāna. Lēmnos nōn est Rōmāna. "
        "Trēs īnsulae Graecae — nōn Rōmānae. "
        "Graecia nōn est in imperiō. Samos nōn est in imperiō. "
        "Chios nōn est in imperiō. Lēmnos nōn est in imperiō. "
        "In Graeciā multae īnsulae sunt. In Italiā paucae īnsulae sunt. "
        "Graecia est terra īnsulārum. Italia est terra oppidōrum. "
        "Samos est Graeca. Chios est Graeca. Lēmnos est Graeca. "
        "Trēs īnsulae. Trēs Graecae. Trēs in marī."
    )
}

STORIES["cap1_06"] = {
    "title_la": "Hispānia, terra magna",
    "title_zh": "西班牙，伟大之地",
    "target_chapter": 1,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Hispānia est in Eurōpā. Hispānia est terra. Hispānia est magna. "
        "Hispānia nōn est parva. Hispānia nōn est īnsula. Hispānia est terra magna. "
        "Hispānia est in imperiō. Hispānia est Rōmāna. Hispānia est prōvincia. "
        "Ubi est Hispānia? Hispānia est in Eurōpā. Hispānia nōn est in Italiā. "
        "Hispānia est longē ab Italiā. Hispānia est in Eurōpā — sed longē. "
        "Estne Hispānia in Italiā? Hispānia nōn est in Italiā. Hispānia est terra magna. "
        "Estne Hispānia in Graeciā? Hispānia nōn est in Graeciā. Hispānia est in Eurōpā. "
        "In Hispāniā multa oppida sunt. In Hispāniā multa flūmina sunt. "
        "In Hispāniā multae īnsulae nōn sunt. Hispānia nōn est īnsula. "
        "Hispānia est terra multōrum oppidōrum. Hispānia est terra multōrum fluviōrum. "
        "Hispānia est prōvincia Rōmāna. Hispānia est in imperiō. "
        "Italia est prōvincia. Italia est in imperiō. Italia est Rōmāna. "
        "Sicilia est prōvincia. Sicilia est in imperiō. Sicilia est Rōmāna. "
        "Hispānia est prōvincia. Hispānia est in imperiō. Hispānia est Rōmāna. "
        "Italia est prīma. Sicilia est secunda. Hispānia est tertia. "
        "Trēs prōvinciae: Italia, Sicilia, Hispānia. Trēs in imperiō. Trēs Rōmānae. "
        "Italia nōn est īnsula. Italia est terra. Sicilia est īnsula. Hispānia est terra. "
        "Italia est terra. Sicilia est īnsula. Hispānia est terra. "
        "Hispānia est magna. Italia est magna. Sicilia est magna. "
        "Trēs prōvinciae magnae. Trēs in imperiō. Trēs Rōmānae."
    )
}

# ---- 中长篇 (500-800词) x3 ----

STORIES["cap1_07"] = {
    "title_la": "Eurōpa",
    "title_zh": "欧罗巴",
    "target_chapter": 1,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Eurōpa est terra. Eurōpa est magna. Eurōpa nōn est parva. "
        "In Eurōpā multae terrae sunt. In Eurōpā multae prōvinciae sunt. "
        "In Eurōpā multa oppida sunt. In Eurōpā multa flūmina sunt. "
        "In Eurōpā multae īnsulae sunt. Eurōpa est terra multa. "
        "Italia est in Eurōpā. Italia est terra. Italia est in imperiō. "
        "Graecia est in Eurōpā. Graecia est terra. Graecia nōn est in imperiō. "
        "Hispānia est in Eurōpā. Hispānia est terra. Hispānia est in imperiō. "
        "Britannia est in Eurōpā. Britannia est īnsula. Britannia est in imperiō. "
        "Sicilia est in Eurōpā. Sicilia est īnsula. Sicilia est in imperiō. "
        "Sardinia est in Eurōpā. Sardinia est īnsula. Sardinia est in imperiō. "
        "Corsica est in Eurōpā. Corsica est īnsula. Corsica est in imperiō. "
        "Italia est prīma. Graecia est secunda. Hispānia est tertia. "
        "Italia est in imperiō. Graecia nōn est in imperiō. Hispānia est in imperiō. "
        "Britannia est in imperiō. Sicilia est in imperiō. Sardinia est in imperiō. "
        "Corsica est in imperiō. "
        "Italia est terra. Graecia est terra. Hispānia est terra. "
        "Britannia est īnsula. Sicilia est īnsula. Sardinia est īnsula. "
        "Corsica est īnsula. "
        "Trēs terrae: Italia, Graecia, Hispānia. "
        "Trēs īnsulae: Britannia, Sicilia, Sardinia. "
        "Italia est magna. Graecia est magna. Hispānia est magna. "
        "Britannia est magna. Sicilia est magna. Sardinia est magna. "
        "Corsica nōn est magna. Corsica est īnsula parva. "
        "In Italiā multa oppida sunt. Rōma est in Italiā. Rōma est oppidum magnum. "
        "Brundisium est in Italiā. Brundisium est oppidum parvum. "
        "Tusculum est in Italiā. Tusculum est oppidum parvum. "
        "In Graeciā multa oppida sunt. In Hispāniā multa oppida sunt. "
        "In Britanniā multa oppida sunt. In Siciliā multa oppida sunt. "
        "In Sardiniā multa oppida sunt. In Corsicā pauca oppida sunt. "
        "Tiberis est in Italiā. Tiberis est fluvius. Tiberis est parvus. "
        "Rhēnus est in Eurōpā. Rhēnus est fluvius. Rhēnus est magnus. "
        "Tiberis est in Italiā. Rhēnus nōn est in Italiā. "
        "Tiberis est Rōmānus. Rhēnus nōn est Rōmānus. "
        "Rōma est in Italiā. Italia est in Eurōpā. "
        "Rōma est caput imperiī. Rōma est oppidum magnum. "
        "Eurōpa est terra multārum terrārum. Eurōpa est terra multārum īnsulārum. "
        "Eurōpa est magna. Eurōpa est prīma. Eurōpa est una."
    )
}

STORIES["cap1_08"] = {
    "title_la": "Imperium Rōmānum",
    "title_zh": "罗马帝国",
    "target_chapter": 1,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Imperium Rōmānum est magnum. Imperium Rōmānum est in Eurōpā. "
        "Rōma est caput imperiī. Rōma est in Italiā. Italia est in imperiō. "
        "Multae prōvinciae in imperiō sunt. Multae terrae in imperiō sunt. "
        "Multa oppida in imperiō sunt. Multa flūmina in imperiō sunt. "
        "Italia est in imperiō. Italia est prīma prōvincia. Italia est terra. "
        "Sicilia est in imperiō. Sicilia est secunda prōvincia. Sicilia est īnsula. "
        "Sardinia est in imperiō. Sardinia est tertia prōvincia. Sardinia est īnsula. "
        "Corsica est in imperiō. Corsica est prōvincia. Corsica est īnsula. "
        "Hispānia est in imperiō. Hispānia est prōvincia. Hispānia est terra magna. "
        "Britannia est in imperiō. Britannia est prōvincia. Britannia est īnsula magna. "
        "Syria est in imperiō. Syria est prōvincia. Syria est terra. "
        "Arabia est in imperiō. Arabia est prōvincia. Arabia est terra. "
        "Italia est prīma. Sicilia est secunda. Sardinia est tertia. "
        "Italia est in Eurōpā. Sicilia est in Eurōpā. Sardinia est in Eurōpā. "
        "Corsica est in Eurōpā. Hispānia est in Eurōpā. Britannia est in Eurōpā. "
        "Syria est in Eurōpā? Syria nōn est in Eurōpā. Syria est in terrā longinquā. "
        "Arabia est in Eurōpā? Arabia nōn est in Eurōpā. Arabia est in terrā longinquā. "
        "Italia est terra. Sicilia est īnsula. Sardinia est īnsula. "
        "Corsica est īnsula. Hispānia est terra. Britannia est īnsula. "
        "Syria est terra. Arabia est terra. "
        "Quattuor terrae: Italia, Hispānia, Syria, Arabia. "
        "Quattuor īnsulae: Sicilia, Sardinia, Corsica, Britannia. "
        "Italia est magna. Hispānia est magna. Syria est magna. Arabia est magna. "
        "Sicilia est magna. Sardinia est magna. Britannia est magna. "
        "Corsica nōn est magna. Corsica est īnsula parva. "
        "In Italiā Rōma est. Rōma est oppidum magnum. Rōma est caput. "
        "In Siciliā multa oppida sunt. In Sardiniā multa oppida sunt. "
        "In Hispāniā multa oppida sunt. In Britanniā multa oppida sunt. "
        "In Syriā multa oppida sunt. In Arabiā multa oppida sunt. "
        "In Corsicā pauca oppida sunt. "
        "Imperium Rōmānum est magnum. Imperium Rōmānum est in multīs terrīs. "
        "Imperium Rōmānum est in Eurōpā. Imperium Rōmānum est Rōmānum. "
        "Rōma est caput. Rōma est in Italiā. Italia est in imperiō. "
        "Multae prōvinciae. Multae terrae. Multa oppida. Imperium magnum."
    )
}

STORIES["cap1_09"] = {
    "title_la": "Terrae et aquae Eurōpae",
    "title_zh": "欧罗巴的陆地与水域",
    "target_chapter": 1,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Eurōpa est terra magna. In Eurōpā multae terrae sunt. "
        "In Eurōpā multae īnsulae sunt. In Eurōpā multa flūmina sunt. "
        "In Eurōpā multa oppida sunt. Eurōpa est terra multa. "
        "Italia est in Eurōpā. Italia est terra. Italia est magna. "
        "Graecia est in Eurōpā. Graecia est terra. Graecia est magna. "
        "Hispānia est in Eurōpā. Hispānia est terra. Hispānia est magna. "
        "Britannia est in Eurōpā. Britannia est īnsula. Britannia est magna. "
        "Sicilia est in Eurōpā. Sicilia est īnsula. Sicilia est magna. "
        "Sardinia est in Eurōpā. Sardinia est īnsula. Sardinia est magna. "
        "Corsica est in Eurōpā. Corsica est īnsula. Corsica est parva. "
        "Samos est in Eurōpā. Samos est īnsula. Samos est parva. Samos est Graeca. "
        "Chios est in Eurōpā. Chios est īnsula. Chios est parva. Chios est Graeca. "
        "Lēmnos est in Eurōpā. Lēmnos est īnsula. Lēmnos est parva. Lēmnos est Graeca. "
        "Melita est in Eurōpā. Melita est īnsula. Melita est parva. "
        "Trēs terrae magnae: Italia, Graecia, Hispānia. "
        "Trēs īnsulae magnae: Britannia, Sicilia, Sardinia. "
        "Trēs īnsulae parvae: Corsica, Samos, Chios. "
        "Italia est prīma terra. Graecia est secunda. Hispānia est tertia. "
        "Britannia est prīma īnsula. Sicilia est secunda. Sardinia est tertia. "
        "Corsica est prīma īnsula parva. Samos est secunda. Chios est tertia. "
        "Tiberis est fluvius. Tiberis est in Italiā. Tiberis est in Eurōpā. "
        "Tiberis est fluvius parvus. Tiberis nōn est magnus. Tiberis est Rōmānus. "
        "Rhēnus est fluvius. Rhēnus est in Eurōpā. Rhēnus est fluvius magnus. "
        "Rhēnus nōn est parvus. Rhēnus nōn est Rōmānus. "
        "Tiberis est in Italiā. Rhēnus nōn est in Italiā. "
        "Tiberis est parvus — sed Rōmānus. Rhēnus est magnus — sed nōn Rōmānus. "
        "Tiberis est prīmus fluvius. Rhēnus est secundus. "
        "In Eurōpā multa flūmina sunt. Tiberis et Rhēnus flūmina sunt. "
        "Tiberis est in imperiō. Rhēnus nōn est in imperiō. "
        "In Italiā multa oppida sunt. Rōma est in Italiā. Rōma est oppidum magnum. "
        "Brundisium est in Italiā. Tusculum est in Italiā. "
        "Rōma est magnum. Brundisium est parvum. Tusculum est parvum. "
        "In Graeciā multa oppida sunt. In Hispāniā multa oppida sunt. "
        "In Britanniā multa oppida sunt. In Siciliā multa oppida sunt. "
        "In Sardiniā multa oppida sunt. In Corsicā pauca oppida sunt. "
        "Eurōpa est terra multārum terrārum et multārum īnsulārum et multōrum fluviōrum. "
        "Eurōpa est magna. Eurōpa est multa. Eurōpa est una."
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

        wc = len(re.findall(r"[A-Za-zāēīōūȳĀĒĪŌŪȲ]{2,}", latin_text))
        print(f"  词汇: {wc}词, 算法: v2_level={v2_level}, v2_rate={v2_rate}%, gap={gap}")

        if not ok:
            print(f"  [FAIL] 算法判到 Cap.{v2_level}, OOV: {v2_oov}")
            failed.append((story_id, v2_level, v2_oov))
            continue

        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)
        nnn = find_next_number(cap_dir, target_ch)
        slug = title_to_slug(title_la)
        tier_slug = "medius" if meta["length_tier"] == "中篇" else "longior"
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
        print(f"  [FAIL] {sid}: algo=Cap.{lvl}, OOV={oov}")

    if failed:
        print("\n!!! 有失败项，请修正后重试 !!!")
        sys.exit(1)


if __name__ == "__main__":
    main()