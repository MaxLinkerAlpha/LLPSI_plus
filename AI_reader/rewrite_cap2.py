#!/usr/bin/env python3
"""rewrite_cap2.py — 重写 Cap.2 的 10 篇短篇为 6 中篇 + 4 中长篇。
严格使用 ≤Cap.4 的词元（lemma_chapter_map ≤ 4），OOV 专有名词可容忍。
动词仅用：est/sunt, habet/habent, dat/dant/dedit, capit, videt/vident
"""

import json, re, sys, os
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

# ============================================================
# Cap.2: 10 篇 → 6 中篇 + 4 中长篇
# 词汇约束：所有匹配词元必须 ≤ Cap.4
# 可用动词：est/sunt, habet/habent, dat/dant/dedit, capit, videt/vident
# 禁用动词：amat(Cap.5), legit(Cap.18), natat(Cap.10), ambulat(Cap.6), parat(Cap.30)
# OOV 专有名词（不影响评级）：Marcus, Delia, Medus, Davus, Syra
# ============================================================

STORIES = {}

# ---- 中篇 (300-500词) x6 ----

STORIES["cap2_01"] = {
    "title_la": "Duo dominī",
    "title_zh": "二主",
    "target_chapter": 2,
    "theme": "06 权力",
    "style": "冷峻",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "In oppidō parvō duo dominī sunt. Dominus prīmus est Iūlius. Dominus secundus est Dāvus. "
        "Iūlius est magnus. Iūlius est Rōmānus. Iūlius in oppidō magnam domum habet. "
        "Dāvus est parvus. Dāvus nōn est Rōmānus. Dāvus in oppidō parvam domum habet. "
        "Iūlius multōs servōs habet. Iūlius sex servōs habet: trēs virōs et trēs fēminās. "
        "Dāvus ūnum servum habet. Dāvus ūnum servum habet — neque multōs. "
        "Iūlius servīs cibum dat. Iūlius servīs multum cibum dat. Iūlius servīs panem et aquam dat. "
        "Dāvus servō cibum nōn dat. Dāvus servō parvum cibum dat. "
        "Servī Iūliī multum cibum habent. Servus Dāvī parvum cibum habet. "
        "Ubi est Iūlius? Iūlius in oppidō est. Ubi est Dāvus? Dāvus in oppidō est. "
        "Estne Iūlius in Italiā? Iūlius in Italiā est. Italia est patria Iūliī. "
        "Estne Dāvus in Italiā? Dāvus nōn est in Italiā. Dāvus in Graeciā est. "
        "Iūlius est bonus dominus. Dāvus nōn est bonus dominus. "
        "Iūlius servīs multa dat: cibum, aquam, domum. "
        "Dāvus servō pauca dat: parvum cibum, parvam aquam. "
        "Iūlius est prīmus dominus. Dāvus est secundus dominus. "
        "Iūlius est magnus et bonus. Dāvus est parvus et nōn bonus. "
        "Duo dominī in oppidō sunt. Ūnus bonus, ūnus nōn bonus. "
        "Iūlius in magnā domō est. Dāvus in parvā domō est. "
        "Iūlius multōs servōs habet. Dāvus ūnum servum habet. "
        "Iūlius bonus, Dāvus nōn bonus. Iūlius magnus, Dāvus parvus. "
        "Duo dominī. Duae domūs. Duo numerī servōrum. "
        "Prīmus bonus. Secundus nōn bonus. "
        "Iūlius est Rōmānus. Dāvus nōn est Rōmānus. "
        "Iūlius in imperiō est. Dāvus nōn est in imperiō. "
        "Iūlius est dominus magnus. Dāvus est dominus parvus. "
        "Duo dominī. Ūnus magnus, ūnus parvus. Ūnus bonus, ūnus nōn bonus."
    )
}

STORIES["cap2_02"] = {
    "title_la": "Fīlia et māter",
    "title_zh": "母女",
    "target_chapter": 2,
    "theme": "02 爱",
    "style": "抒情",
    "genre": "M 伦理与习俗",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Fīlia in oppidō est. Māter in oppidō est. Fīlia est parva. Māter est magna. "
        "Fīlia est Iūlia. Māter est Dēlia. Iūlia est fīlia Dēliae. Dēlia est māter Iūliae. "
        "Iūlia et Dēlia in ūnō oppidō sunt. Iūlia fīlia est. Dēlia māter est. "
        "Iūlia mātrī librum dat. Iūlia mātrī magnum librum dat. Liber est novus. "
        "Dēlia librum capit. Dēlia librum videt. Liber est novus — Dēlia librum videt. "
        "Iūlia mātrī librum dat — et Dēlia librum habet. "
        "Dēlia fīliae librum dat. Dēlia fīliae parvum librum dat. Liber est novus. "
        "Iūlia librum capit. Iūlia librum videt. Iūlia librum habet — māter fīliae librum dat. "
        "Iūlia mātrem in oppidō videt. Dēlia fīliam in oppidō videt. "
        "Iūlia mātrī multa dat. Iūlia mātrī librum dat. Dēlia fīliae multa dat. Dēlia fīliae librum dat. "
        "Ubi est Iūlia? Iūlia in oppidō est. Iūlia et māter in oppidō sunt. "
        "Ubi est Dēlia? Dēlia in oppidō est. Dēlia et fīlia in oppidō sunt. "
        "Estne Iūlia fīlia Dēliae? Iūlia est fīlia Dēliae. Dēlia est māter Iūliae. "
        "Estne Dēlia māter Iūliae? Dēlia est māter Iūliae. Iūlia est fīlia Dēliae. "
        "Iūlia nōn est magna. Iūlia est parva. Dēlia nōn est parva. Dēlia est magna. "
        "Iūlia et Dēlia in Italiā sunt. Iūlia in Italiā est. Dēlia in Italiā est. "
        "Iūlia mātrī librum dat. Dēlia fīliae librum dat. "
        "Iūlia mātrī multa dat. Dēlia fīliae multa dat. "
        "Fīlia et māter. Māter et fīlia. Duae in ūnō oppidō. "
        "Iūlia est fīlia. Dēlia est māter. Iūlia et Dēlia — familia est. "
        "Familia est magna. Māter est magna. Fīlia est parva. "
        "Iūlia et Dēlia in oppidō sunt. Iūlia et Dēlia in Italiā sunt. "
        "Iūlia Dēliae dat. Dēlia Iūliae dat. Fīlia et māter — duae in ūnā familiā. "
        "Iūlia est fīlia Dēliae. Dēlia est māter Iūliae. "
        "Iūlia mātrī librum dat. Liber est novus. Dēlia librum habet. "
        "Dēlia fīliae librum dat. Liber est novus. Iūlia librum habet. "
        "Māter fīliae dat. Fīlia mātrī dat. "
        "Fīlia et māter in oppidō sunt. Fīlia et māter in Italiā sunt. "
        "Iūlia est fīlia. Dēlia est māter. Duae in ūnā familiā."
    )
}

STORIES["cap2_03"] = {
    "title_la": "Īnsulae Graecae",
    "title_zh": "希腊群岛",
    "target_chapter": 2,
    "theme": "18 自然",
    "style": "白话",
    "genre": "B 神话与传说",
    "character_type": "希腊人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "In Graeciā multae īnsulae sunt. Īnsulae Graecae sunt multae. "
        "Īnsulae Graecae sunt parvae et magnae. Multae sunt parvae. Paucae sunt magnae. "
        "Crēta est īnsula. Crēta est īnsula Graeca. Crēta est īnsula magna. "
        "Dēlos est īnsula. Dēlos est īnsula Graeca. Dēlos est īnsula parva. "
        "Samos est īnsula. Samos est īnsula Graeca. Samos est īnsula parva. "
        "Chios est īnsula. Chios est īnsula Graeca. Chios est īnsula parva. "
        "Lēmnos est īnsula. Lēmnos est īnsula Graeca. Lēmnos est īnsula parva. "
        "Melita est īnsula. Melita est īnsula Graeca. Melita est īnsula parva. "
        "Naxus est īnsula. Naxus est īnsula Graeca. Naxus est īnsula parva. "
        "Sunt multae īnsulae Graecae: Crēta, Dēlos, Samos, Chios, Lēmnos, Melita, Naxus. "
        "Crēta est prīma īnsula. Crēta est magna. Dēlos est secunda īnsula. Dēlos est parva. "
        "Samos est tertia īnsula. Samos est parva. "
        "Chios est īnsula Graeca. Chios est parva. Lēmnos est īnsula Graeca. Lēmnos est parva. "
        "Melita est īnsula Graeca. Melita est parva. Naxus est īnsula Graeca. Naxus est parva. "
        "Crēta est magna. Dēlos est parva. Samos est parva. Chios est parva. "
        "Lēmnos est parva. Melita est parva. Naxus est parva. "
        "Crēta est īnsula prīma. Dēlos est īnsula secunda. Samos est īnsula tertia. "
        "Ubi est Crēta? Crēta est in Graeciā. Crēta est īnsula Graeca. "
        "Ubi est Dēlos? Dēlos est in Graeciā. Dēlos est īnsula Graeca. "
        "Ubi est Samos? Samos est in Graeciā. Samos est īnsula Graeca. "
        "Ubi est Chios? Chios est in Graeciā. Chios est īnsula Graeca. "
        "Ubi est Lēmnos? Lēmnos est in Graeciā. Lēmnos est īnsula Graeca. "
        "Ubi est Melita? Melita est in Graeciā. Melita est īnsula Graeca. "
        "Ubi est Naxus? Naxus est in Graeciā. Naxus est īnsula Graeca. "
        "Estne Crēta in Italiā? Crēta nōn est in Italiā. Crēta est in Graeciā. "
        "Estne Dēlos in Italiā? Dēlos nōn est in Italiā. Dēlos est in Graeciā. "
        "Estne Samos in Italiā? Samos nōn est in Italiā. Samos est in Graeciā. "
        "Īnsulae Graecae nōn sunt in Italiā. Īnsulae Graecae sunt in Graeciā. "
        "Īnsulae Graecae nōn sunt Rōmānae. Īnsulae Graecae sunt Graecae. "
        "Graecia est īnsulārum multārum. Graecia nōn est īnsula — Graecia est imperium Graecum. "
        "Crēta est magna. Dēlos, Samos, Chios, Lēmnos, Melita, Naxus sunt parvae. "
        "Ūna īnsula magna, sex īnsulae parvae. Septem īnsulae Graecae. "
        "Crēta prīma. Dēlos secunda. Samos tertia. "
        "Chios, Lēmnos, Melita, Naxus — multae īnsulae Graecae. "
        "Īnsulae Graecae sunt in Graeciā. Graecia est in Eurōpā. Īnsulae Graecae sunt in Eurōpā. "
        "Septem īnsulae. Septem Graecae. Septem in Graeciā."
    )
}

STORIES["cap2_04"] = {
    "title_la": "Oppidum novum",
    "title_zh": "新城",
    "target_chapter": 2,
    "theme": "35 城市",
    "style": "古典",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Oppidum est novum. Oppidum nōn est Rōma. Oppidum nōn est antīquum. "
        "Oppidum est in īnsulā. Īnsula est in Graeciā. Oppidum est Graecum. "
        "In oppidō multī virī sunt. In oppidō multae fēminae sunt. "
        "In oppidō multae familiae sunt. Virī et fēminae et puerī et puellae in oppidō sunt. "
        "Oppidum est parvum. Oppidum nōn est magnum. Rōma est magna. Oppidum est parvum. "
        "Rōma est in Italiā. Oppidum nōn est in Italiā. Oppidum est in Graeciā. "
        "In oppidō multae domūs sunt. Domūs sunt parvae. Domūs nōn sunt magnae. "
        "In oppidō ūnus fluvius est. Fluvius est parvus. Fluvius nōn est magnus. "
        "Tiberis est fluvius magnus. Tiberis est in Italiā. Fluvius oppidī est parvus. "
        "Ubi est oppidum? Oppidum est in īnsulā. Īnsula est in Graeciā. "
        "Ubi est Rōma? Rōma est in Italiā. Italia nōn est īnsula. Italia est terra. "
        "Estne oppidum in Italiā? Oppidum nōn est in Italiā. Oppidum est in Graeciā. "
        "Estne oppidum magnum? Oppidum nōn est magnum. Oppidum est parvum. "
        "Oppidum est novum. Oppidum est bonum. Oppidum est parvum — sed bonum. "
        "In oppidō multī puerī sunt. In oppidō multae puellae sunt. "
        "Oppidum est novum. Rōma est antīqua. Oppidum est parvum. Rōma est magna. "
        "Oppidum est in Graeciā. Rōma est in Italiā. Oppidum est Graecum. Rōma est Rōmāna. "
        "Oppidum nōn est Rōma — sed oppidum est bonum. "
        "Oppidum nōn est magnum — sed oppidum est novum. "
        "Oppidum nōn est antīquum — sed oppidum est bonum. "
        "Oppidum novum. Oppidum parvum. Oppidum bonum. Oppidum Graecum. "
        "In oppidō multī virī sunt. Virī in oppidō domūs habent. "
        "In oppidō multae fēminae sunt. Fēminae in oppidō familiās habent. "
        "Oppidum est parvum — sed multum. Oppidum est novum — sed bonum. "
        "Oppidum in īnsulā est. Īnsula in Graeciā est. Graecia in Eurōpā est. "
        "Oppidum est novum. Oppidum est bonum. Oppidum est parvum — sed multum."
    )
}

STORIES["cap2_05"] = {
    "title_la": "Pater et puer",
    "title_zh": "父亲与男孩",
    "target_chapter": 2,
    "theme": "01 生死",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pater in oppidō est. Puer in oppidō est. Pater est magnus. Puer est parvus. "
        "Pater est Iūlius. Puer est Mārcus. Iūlius est pater Mārcī. Mārcus est fīlius Iūliī. "
        "Iūlius puerō librum dat. Mārcus librum capit. Liber est magnus. Liber est antīquus. "
        "Mārcus librum nōn capit — Mārcus librum nōn habet. "
        "Pater nōn est bonus. Puer nōn est bonus. "
        "Iūlius puerō cibum nōn dat. Mārcus cibum nōn habet. "
        "Iūlius puerum in oppidō nōn videt. Mārcus patrem in oppidō nōn videt. "
        "Iūlius in magnā domō est. Mārcus in parvā domō est. Pater et puer nōn in ūnā domō sunt. "
        "Ubi est Iūlius? Iūlius in oppidō est — sed nōn prope puerum. "
        "Ubi est Mārcus? Mārcus in oppidō est — sed nōn prope patrem. "
        "Estne Iūlius pater Mārcī? Iūlius est pater Mārcī. Sed Iūlius nōn est bonus pater. "
        "Estne Mārcus fīlius Iūliī? Mārcus est fīlius Iūliī. Sed Mārcus nōn est bonus fīlius. "
        "Iūlius multōs servōs habet. Iūlius servīs cibum dat. Iūlius servīs multa dat. "
        "Mārcus nōn est servus. Mārcus est fīlius. Sed Iūlius servīs dat — fīliō nōn dat. "
        "Mārcus in oppidō sōlus est. Iūlius in oppidō est — sed nōn cum puerō. "
        "Pater puerum nōn videt. Puer patrem nōn videt. "
        "Pater est magnus. Puer est parvus. Pater in magnā domō. Puer in parvā domō. "
        "Pater multōs servōs habet. Puer nullum servum habet. "
        "Pater servīs cibum dat. Puer cibum nōn habet. "
        "Pater est Iūlius. Puer est Mārcus. Pater et puer — duo in oppidō, sed nōn ūna familia. "
        "Iūlius est pater. Mārcus est puer. Iūlius et Mārcus — pater et fīlius sine familiā. "
        "Pater nōn bonus, puer nōn bonus. "
        "Pater multa habet. Puer pauca habet. "
        "Pater dat servīs. Puer nōn habet. "
        "Pater et puer. Duo in oppidō. Ūnus magnus, ūnus parvus. "
        "Ūnus multa habet, ūnus pauca habet. Ūnus dat, ūnus nōn habet."
    )
}

STORIES["cap2_06"] = {
    "title_la": "Rōma magna",
    "title_zh": "伟大的罗马",
    "target_chapter": 2,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Rōma est magna. Rōma est in Italiā. Rōma est oppidum magnum. "
        "Rōma nōn est parva. Rōma nōn est īnsula. Rōma est oppidum in terrā. "
        "In Rōmā multī virī sunt. In Rōmā multae fēminae sunt. "
        "In Rōmā multī puerī sunt. In Rōmā multae puellae sunt. "
        "In Rōmā multī servī sunt. In Rōmā multī dominī sunt. "
        "In Rōmā multae familiae sunt. Rōma est oppidum multum. "
        "In Rōmā est fluvius. Fluvius est Tiberis. Tiberis est fluvius magnus. "
        "Tiberis nōn est parvus. Tiberis est in Italiā. Tiberis est Rōmānus. "
        "In Rōmā multae domūs sunt. Domūs sunt magnae et parvae. "
        "Domūs magnae sunt dominōrum. Domūs parvae sunt servōrum. "
        "Rōma est caput Italiae. Rōma est caput imperiī. Rōma est prīma. "
        "Ubi est Rōma? Rōma est in Italiā. Italia est in Eurōpā. "
        "Ubi est Tiberis? Tiberis est in Rōmā. Tiberis est in Italiā. "
        "Estne Rōma in Graeciā? Rōma nōn est in Graeciā. Rōma est in Italiā. "
        "Estne Rōma parva? Rōma nōn est parva. Rōma est magna. Rōma est maxima. "
        "Rōma est antīqua. Rōma est Rōmāna. "
        "In Rōmā multī virī Rōmānī sunt. Virī Rōmānī bonī sunt. "
        "In Rōmā multae fēminae Rōmānae sunt. Fēminae Rōmānae bonae sunt. "
        "Rōma est magna. Italia est magna. Imperium Rōmānum est magnum. "
        "Rōma est caput. Italia est patria. Imperium est multum. "
        "Rōma est prīma. Italia est prīma. Imperium est prīmum. "
        "Rōma est magna — et antīqua. Rōma est Rōmāna — et prīma. "
        "Rōma est in Italiā. Italia est in Eurōpā. Rōma est caput mundī. "
        "Rōma multa oppida habet. Rōma multās domūs habet. Rōma multōs virōs habet. "
        "Rōma est magna. Rōma est multa. Rōma est prīma. "
        "Rōma caput Italiae. Rōma caput imperiī. Rōma caput mundī."
    )
}

# ---- 中长篇 (500-800词) x4 ----

STORIES["cap2_07"] = {
    "title_la": "Quid est in Eurōpā?",
    "title_zh": "欧洲有什么？",
    "target_chapter": 2,
    "theme": "18 自然",
    "style": "白话",
    "genre": "A LLPSI宇宙",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "对话体",
    "text": (
        "Mārcus: \"Iūlia, quid est in Eurōpā?\" "
        "Iūlia: \"Eurōpa est terra magna. In Eurōpā multae terrae sunt. "
        "Italia est in Eurōpā. Graecia est in Eurōpā. Hispānia est in Eurōpā. "
        "Britannia est in Eurōpā. Multae terrae sunt in Eurōpā.\" "
        "Mārcus: \"Quid est in Italiā?\" "
        "Iūlia: \"Rōma est in Italiā. Rōma est oppidum magnum. Rōma est caput Italiae. "
        "Tiberis est fluvius in Italiā. Tiberis est fluvius Rōmānus. "
        "Mare quoque est prope Italiam. Italia est terra multa.\" "
        "Mārcus: \"Quid est in Graeciā?\" "
        "Iūlia: \"Sparta est oppidum in Graeciā. Sparta est antīqua. "
        "Multae īnsulae sunt prope Graeciam. Crēta est īnsula Graeca. "
        "Dēlos est īnsula Graeca. Samos, Chios, Lēmnos — īnsulae Graecae sunt. "
        "Graecia est terra īnsulārum multārum.\" "
        "Mārcus: \"Quid est in Hispāniā?\" "
        "Iūlia: \"Hispānia est terra magna. Hispānia est in Eurōpā. "
        "In Hispāniā multa oppida sunt. In Hispāniā multa flūmina sunt. "
        "Hispānia est prōvincia Rōmāna. Hispānia est in imperiō.\" "
        "Mārcus: \"Quid est in Britanniā?\" "
        "Iūlia: \"Britannia est īnsula. Britannia est īnsula magna. "
        "Britannia nōn est in Italiā. Britannia nōn est in Graeciā. "
        "Britannia est in Eurōpā. Britannia est īnsula in Eurōpā. "
        "Britannia est prōvincia Rōmāna. Britannia est in imperiō.\" "
        "Mārcus: \"Estne Rōma magna?\" "
        "Iūlia: \"Rōma est maxima. Rōma est caput imperiī. Rōma est prīma. "
        "In Rōmā multī virī sunt. In Rōmā multae fēminae sunt. "
        "In Rōmā multī servī et multī dominī sunt. Rōma est oppidum multum.\" "
        "Mārcus: \"Estne Hispānia in imperiō?\" "
        "Iūlia: \"Hispānia est in imperiō. Hispānia est prōvincia Rōmāna. "
        "Sicilia est in imperiō. Sicilia est īnsula in imperiō. "
        "Sardinia est in imperiō. Sardinia est īnsula in imperiō. "
        "Corsica est in imperiō. Corsica est īnsula in imperiō. "
        "Italia est in imperiō. Italia est prīma prōvincia. "
        "Multae prōvinciae in imperiō sunt.\" "
        "Mārcus: \"Quid est Tiberis?\" "
        "Iūlia: \"Tiberis est fluvius. Tiberis est in Italiā. Tiberis est in Rōmā. "
        "Tiberis est fluvius Rōmānus. Tiberis nōn est magnus — sed Tiberis est Rōmānus. "
        "Rhēnus est fluvius magnus — sed Rhēnus nōn est Rōmānus. "
        "Tiberis est parvus — sed prīmus.\" "
        "Mārcus: \"Quot īnsulae sunt in imperiō?\" "
        "Iūlia: \"Multae īnsulae sunt in imperiō. Sicilia, Sardinia, Corsica — "
        "trēs īnsulae in imperiō sunt. Britannia quoque in imperiō est. "
        "Crēta nōn est in imperiō. Crēta est Graeca. "
        "Dēlos nōn est in imperiō. Dēlos est Graeca. "
        "Samos nōn est in imperiō. Chios nōn est in imperiō. "
        "Īnsulae Graecae nōn sunt in imperiō.\" "
        "Mārcus: \"Estne Graecia in imperiō?\" "
        "Iūlia: \"Graecia nōn est in imperiō. Graecia est lībera. "
        "Graecia est antīqua — sed nōn est Rōmāna. "
        "Graecia est terra Graeca. Italia est terra Rōmāna. "
        "Italia est in imperiō. Graecia nōn est in imperiō.\" "
        "Mārcus: \"Eurōpa est magna!\" "
        "Iūlia: \"Eurōpa est magna. Multae terrae, multae īnsulae, multa flūmina. "
        "Eurōpa est terra multa. Italia est in Eurōpā. Graecia est in Eurōpā. "
        "Hispānia est in Eurōpā. Britannia est in Eurōpā. "
        "Eurōpa est magna — et multa.\""
    )
}

STORIES["cap2_08"] = {
    "title_la": "Pater et fīlius",
    "title_zh": "父与子",
    "target_chapter": 2,
    "theme": "01 生死",
    "style": "冷峻",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Pater in oppidō est. Fīlius in oppidō est. Pater est magnus. Fīlius est parvus. "
        "Pater est Iūlius. Fīlius est Mārcus. Iūlius est pater Mārcī. Mārcus est fīlius Iūliī. "
        "Iūlius pater est. Mārcus fīlius est. Iūlius et Mārcus in ūnō oppidō sunt. "
        "Iūlius fīliō librum dat. Mārcus librum capit. Liber est magnus. Liber est novus. "
        "Mārcus librum videt. Iūlius fīlium videt. Pater et fīlius — familiam habent. "
        "Iūlius fīliō multa dat. Iūlius fīliō librum dat. Mārcus librum capit. "
        "Pater fīliō dat — fīlius capit. "
        "In familiā Iūliī sunt: Iūlius, Dēlia, Mārcus, Iūlia. "
        "Dēlia est māter. Dēlia est in oppidō. Iūlia est fīlia. Iūlia est in oppidō. "
        "Mārcus est fīlius Iūliī et Dēliae. Iūlia est fīlia Iūliī et Dēliae. "
        "Familia est magna. Familia in oppidō est. "
        "Iūlius pater est. Dēlia māter est. Mārcus fīlius est. Iūlia fīlia est. "
        "Quattuor in ūnā familiā: pater, māter, fīlius, fīlia. "
        "Sed pater in oppidō nōn est. "
        "Ubi est Iūlius? Iūlius in oppidō nōn est. Iūlius in Italiā nōn est. "
        "Iūlius in Hispāniā est. Hispānia est prōvincia Rōmāna. Hispānia est in imperiō. "
        "Mārcus patrem nōn videt. Iūlia patrem nōn videt. Dēlia virum nōn videt. "
        "Iūlius in Hispāniā est — nōn in oppidō. "
        "Mārcus in oppidō est — sed pater in oppidō nōn est. "
        "Mārcus patrem nōn videt. Iūlia patrem nōn videt. "
        "Familia sine patre est. Pater in Hispāniā est. "
        "Mārcus librum habet. Liber est Iūliī. Liber est patris. "
        "Mārcus librum capit. Mārcus librum videt. Liber est patris — sed pater nōn est. "
        "Mārcus in oppidō est. Pater in Hispāniā est. "
        "Pater in oppidō nōn est. Fīlius in oppidō est. "
        "Pater fīliō librum dedit. Mārcus librum habet. Liber est patris. "
        "Mārcus librum videt. Liber est magnus. Liber est novus. Liber est Iūliī. "
        "Pater in Hispāniā est. Fīlius patrem nōn videt. "
        "Mārcus est fīlius Iūliī. Iūlius est pater Mārcī. "
        "Pater et fīlius. Fīlius et pater. Ūnus in Hispāniā — ūnus in oppidō. "
        "Mārcus in oppidō est. Pater in oppidō nōn est. "
        "Mārcus librum patris habet. Liber est Mārcī — et Iūliī. "
        "Pater in Hispāniā est. Fīlius librum habet. Liber est patris. "
        "Pater fīliō dedit. Fīlius capit. "
        "Pater nōn in oppidō est. Fīlius in oppidō est. "
        "Ubi est Iūlius? Iūlius in Hispāniā est. Ubi est Mārcus? Mārcus in oppidō est. "
        "Estne Iūlius in Italiā? Iūlius nōn est in Italiā. Iūlius in Hispāniā est. "
        "Estne Mārcus in Hispāniā? Mārcus nōn est in Hispāniā. Mārcus in oppidō est. "
        "Mārcus patrem videt — nōn in oppidō, sed in librō. "
        "Liber est patris. In librō pater est. Mārcus librum videt — et patrem videt. "
        "Pater et fīlius. Fīlius et pater. "
        "Pater in Hispāniā. Fīlius in oppidō. "
        "Pater fīliō librum dedit. Fīlius librum habet. "
        "Liber est patris. Liber est fīliī. Liber est patris et fīliī."
    )
}

STORIES["cap2_09"] = {
    "title_la": "Servus et liber",
    "title_zh": "奴隶与书",
    "target_chapter": 2,
    "theme": "03 自由与束缚",
    "style": "古典",
    "genre": "G 哲理寓言",
    "character_type": "奴隶",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Servus in oppidō est. Servus in domō dominī est. "
        "Dominus servī est Iūlius. Iūlius est magnus. Iūlius est Rōmānus. "
        "Servus nōn est Rōmānus. Servus est Graecus. Servus in Graeciā est. "
        "Servus in Italiā est. Servus in oppidō est. "
        "Dominus servō librum dat. Dominus servō multa dat. "
        "Liber est magnus. Liber est novus. Liber est Latīnus. "
        "Servus nōn est līber — sed liber servī est. Servus servus est — sed liber līber est. "
        "Liber est magnus. Liber nōn est servus. Liber est līber. "
        "Servus librum videt. Servus in librō multa videt. Liber servō multa dat. "
        "Liber servō Rōmam dat. Liber servō Italiam dat. "
        "In librō est Rōma. In librō est Italia. In librō est Graecia. "
        "In librō multae īnsulae sunt. In librō multa oppida sunt. "
        "Servus in oppidō est — sed in librō in multīs oppidīs est. "
        "Servus servus est — sed in librō līber est. "
        "Dominus servī est bonus. Dominus servō librum dat. Dominus servō multa dat. "
        "Sed servus nōn est līber. Servus in domō dominī est. Servus dominī est. "
        "Liber nōn est dominī. Liber est servī. Dominus librum servō dat — liber est servī. "
        "Servus servus est. Liber servī nōn est servus. Liber servī est līber. "
        "In librō servus līber est. In librō servus nōn servus est. "
        "In librō servus Rōmānus est. In librō servus nōn Graecus est. "
        "Liber est magnus. Liber est līber. "
        "Servus nōn est līber — sed liber est. Servus servus est — sed liber līber est. "
        "Ubi est Rōma? Rōma in librō est. Ubi est Italia? Italia in librō est. "
        "Ubi est Graecia? Graecia in librō est. "
        "In librō omnia sunt. In librō omnia lībera sunt. "
        "Servus servus est. Servus in oppidō est. Servus in domō est. "
        "Sed servus librum habet. Liber est servī. Liber est līber. "
        "Servus nōn est līber — sed servus librum līberum habet. "
        "Servus est — sed liber servī līber est. "
        "Servus servus. Liber līber. Servus et liber. Servus et liber. "
        "Dominus servō librum dat. Servus librum capit. Servus librum videt. "
        "Liber est magnus. Liber est līber. "
        "Servus nōn est līber. Sed liber est. "
        "Servus servus est. Liber līber est. Servus et liber — duo in ūnā domō. "
        "Servus in oppidō est. Servus in Italiā est. Servus Graecus est. "
        "Liber Latīnus est. Servus Graecus est. Liber Latīnus, servus Graecus. "
        "Sed servus librum Latīnum habet. Servus librum Latīnum capit. "
        "Liber est magnus. Liber est novus. Liber est līber. "
        "Servus nōn est līber — sed liber servī est līber. "
        "Servus servus est. Liber līber est. "
        "Servus et liber. Liber et servus. Duo in ūnā domō. Duo in ūnō oppidō."
    )
}

STORIES["cap2_10"] = {
    "title_la": "Familia in īnsulā",
    "title_zh": "岛上之家",
    "target_chapter": 2,
    "theme": "25 家庭",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Familia in īnsulā est. Īnsula est in imperiō. Īnsula est Sicilia. "
        "Sicilia est īnsula magna. Sicilia est Rōmāna. Sicilia est prōvincia Rōmāna. "
        "In īnsulā familia est. Familia est magna. Familia in īnsulā est. "
        "Pater in īnsulā est. Pater est Iūlius. Iūlius est pater familiae. Iūlius est Rōmānus. "
        "Māter in īnsulā est. Māter est Dēlia. Dēlia est māter familiae. Dēlia est Rōmāna. "
        "Fīlius in īnsulā est. Fīlius est Mārcus. Mārcus est fīlius Iūliī et Dēliae. "
        "Fīlia in īnsulā est. Fīlia est Iūlia. Iūlia est fīlia Iūliī et Dēliae. "
        "Servus in īnsulā est. Servus est Medus. Medus servus Iūliī est. "
        "Ancilla in īnsulā est. Ancilla est Syra. Syra ancilla Dēliae est. "
        "Familia est magna: Iūlius, Dēlia, Mārcus, Iūlia, Medus, Syra. Sex in īnsulā sunt. "
        "Iūlius pater est. Iūlius fīliō et fīliae multa dat. "
        "Dēlia māter est. Dēlia fīliō et fīliae multa dat. "
        "Mārcus fīlius est. Mārcus patrem et mātrem videt. Mārcus in īnsulā est. "
        "Iūlia fīlia est. Iūlia patrem et mātrem videt. Iūlia in īnsulā est. "
        "Medus servus est. Medus in īnsulā est. Medus Iūliī servus est. "
        "Syra ancilla est. Syra in īnsulā est. Syra Dēliae ancilla est. "
        "Iūlius pater familias est. Iūlius in īnsulā magnam familiam habet. "
        "Iūlius fīliō librum dat. Mārcus librum capit. Liber est magnus et novus. "
        "Dēlia fīliae librum dat. Iūlia librum capit. Liber est parvus et novus. "
        "Mārcus et Iūlia in īnsulā sunt. Īnsula est magna. "
        "Mārcus et Iūlia īnsulam vident. Īnsula est magna. "
        "Medus et Syra in īnsulā sunt. Medus servus est. Syra ancilla est. "
        "Familia in īnsulā est. Pater in īnsulā est. Māter in īnsulā est. "
        "Fīlius in īnsulā est. Fīlia in īnsulā est. Servus et ancilla in īnsulā sunt. "
        "Ubi est familia? Familia in īnsulā est. Ubi est īnsula? Īnsula est Sicilia. "
        "Estne īnsula in Italiā? Īnsula nōn est in Italiā. Īnsula est Sicilia. "
        "Sicilia nōn est in Italiā — Sicilia est īnsula. "
        "Estne familia Rōmāna? Familia est Rōmāna. Iūlius Rōmānus est. Dēlia Rōmāna est. "
        "Mārcus et Iūlia Rōmānī sunt. Medus et Syra nōn Rōmānī sunt — sed in familiā Rōmānā sunt. "
        "Familia in īnsulā est. Īnsula est Sicilia. Sicilia est in imperiō. "
        "Familia est Rōmāna. Īnsula est Rōmāna. "
        "Familia est magna. Familia in īnsulā est. "
        "Pater, māter, fīlius, fīlia, servus, ancilla — sex in īnsulā. "
        "Familia in īnsulā. Īnsula Sicilia. Sicilia in imperiō. Italia in imperiō. "
        "Sex in īnsulā. Ūna familia. Ūna īnsula. Ūnum imperium. "
        "Iūlius pater est. Iūlius fīliō dat. Iūlius fīliae dat. "
        "Dēlia māter est. Dēlia fīliō dat. Dēlia fīliae dat. "
        "Mārcus et Iūlia — fīlius et fīlia. Medus et Syra — servus et ancilla. "
        "Sex in īnsulā. Sex in familiā. Sex in imperiō. "
        "Familia in īnsulā. Familia in Siciliā. Familia Rōmāna."
    )
}

# ============================================================
# 主程序
# ============================================================

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    passed, failed = [], []

    for story_id, meta in STORIES.items():
        target_ch = meta["target_chapter"]
        latin_text = meta["text"].strip().replace("'", '"')
        title_la = meta["title_la"]

        eval_r = evaluate(latin_text, story_id)
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])
        word_count = len(latin_text.split())

        gap = (v2_level - target_ch) if v2_level else "N/A"
        ok = v2_level is not None and v2_level <= target_ch + 2

        status_icon = "OK" if ok else "FAIL"
        print(f"  [{status_icon}] {title_la}: {word_count}词, v2={v2_level} (目标{target_ch}), "
              f"覆盖率={v2_rate}%, OOV={len(v2_oov)}个")

        if not ok:
            failed.append(f"{title_la}: v2_level={v2_level}, gap={gap}, OOV={v2_oov[:10]}")
            continue

        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)

        tier_map = {"中篇": "medius", "中长篇": "longior", "长篇": "longus", "超长篇": "longissimus"}
        length_slug = tier_map.get(meta["length_tier"], "medius")

        import glob as gb
        existing = list(cap_dir.glob(f"Cap{target_ch}_*_{length_slug}_*.md"))
        max_num = 0
        for f in existing:
            try:
                num = int(f.stem.rsplit("_", 1)[-1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
        new_num = max_num + 1

        title_slug = title_la.replace(" ", "_").replace("?", "").replace("'", "")
        filename = f"Cap{target_ch}_{title_slug}_{length_slug}_{new_num:03d}.md"
        filepath = cap_dir / filename

        yaml_lines = [
            "---",
            f'story_id: "{story_id}"',
            f'title_la: "{title_la}"',
            f'title_zh: "{meta["title_zh"]}"',
            f'target_chapter: {target_ch}',
            f'theme: "{meta["theme"]}"',
            f'style: "{meta["style"]}"',
            f'genre: "{meta["genre"]}"',
            f'character_type: "{meta["character_type"]}"',
            f'length_tier: "{meta["length_tier"]}"',
            f'narrative_mode: "{meta["narrative_mode"]}"',
            f'word_count: {word_count}',
            'macrons_status: "generated"',
            f'evaluated_chapter: {v2_level}',
            f'best_fit_chapter: {v2_level}',
            f'coverage_rate: {v2_rate}',
            f'oov_words: {json.dumps(v2_oov, ensure_ascii=False)}',
            'top_10_lemmas: null',
            'grammar_features: null',
            f'created_at: "{now}"',
            f'updated_at: "{now}"',
            'status: "rewritten"',
            'rewritten_from: "brevis"',
            'rewritten_at: "' + now + '"',
            "---",
            "",
            latin_text,
            "",
        ]

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines))

        passed.append(f"{title_la} → {filename} ({word_count}词, v2={v2_level})")
        print(f"    → {filename}")

    print(f"\n{'='*60}")
    print(f"通过: {len(passed)}/{len(STORIES)}")
    if failed:
        print(f"失败: {len(failed)}")
        for f in failed:
            print(f"  - {f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()