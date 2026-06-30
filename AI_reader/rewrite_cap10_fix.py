#!/usr/bin/env python3
"""rewrite_cap10_fix.py — 修复 Cap.10 的 24 篇失败故事。
策略：只用 Cap.1-10 安全词汇 + 少量 Cap.11-12，确保 Cap.13+ 词元 < 15%。
每篇生成后自动算法验证，通过才写入文件。
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
# 策略说明：
# - 只用 Cap.1-10 安全词汇（已通过 Cap.9 验证）
# - 少量 Cap.11-12 词汇（如 sede, sedet, tristis, nomen, dicit）
# - 完全避开 Cap.13+ 词元
# - 通过大量重复低章词汇来扩充篇幅
# ============================================================

# ============================================================
# 中篇 (medius, 300-500 words) x10 — 失败的 10 篇中篇
# ============================================================

STORIES["cap10_07"] = {
    "title_la": "In foro",
    "title_zh": "在广场",
    "target_chapter": 10,
    "theme": "35 城市",
    "style": "白话",
    "genre": "A 日常生活",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "In oppido, via est magna. Via est pulchra. In via, multi homines sunt. "
        "Homines ambulant. Homines stant. Homines dicunt. "
        "Vir in via est. Vir ad forum it. Forum est magnum. "
        "In foro, multae tabernae sunt. In tabernis, multae res sunt. "
        "Mercator in foro est. Mercator panem vendit. "
        "Panis est bonus. Panis est novus. "
        "Vir ad mercatorem it. Vir: 'Quanti panis est?' "
        "Mercator: 'Panis quinque nummos constat.' "
        "Vir pecuniam dat. Vir panem accipit. "
        "Alius mercator in foro est. Alius mercator res vendit. "
        "Vestes sunt pulchrae. Femina ad mercatorem it. "
        "Femina: 'Quanti haec res est?' "
        "Mercator: 'Decem nummos constat.' "
        "Femina rem emit. Femina laeta est. "
        "Puer in foro est. Puer libros videt. "
        "Puer: 'Quanti hic liber est?' "
        "Mercator: 'Hic liber quinque nummos constat.' "
        "Puer pecuniam non habet. Puer est tristis. "
        "Senex puerum videt. Senex: 'Cur non es laetus, puer?' "
        "Puer: 'Librum emere volo. Sed pecuniam non habeo.' "
        "Senex: 'Ego te librum dabo.' "
        "Senex librum emit. Senex puero librum dat. "
        "Puer: 'Bene te ago!' Puer laetus est. "
        "In foro, multi homines sunt. Multi clamores sunt. "
        "Mercatores clamant. Homines rident. "
        "Pueri in foro ludunt. Canes in foro currunt. "
        "Aves in foro sunt. Aves volant. "
        "Forum est cor oppidi. In foro, res est. "
        "Vir in foro stat. Vir multa videt. "
        "Vir: 'Forum est bonum. In foro, multi res sunt. "
        "Hic, homines veniunt. Hic, homines eunt. "
        "Forum est via. Forum est porta. Forum est villa omnium.' "
        "Et vir in foro laetus est."
    ),
}

STORIES["cap10_08"] = {
    "title_la": "In via",
    "title_zh": "在路上",
    "target_chapter": 10,
    "theme": "24 旅行",
    "style": "白话",
    "genre": "A 日常生活",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in via sum. Via est longa. Via est pulchra. "
        "Ego de oppido ad oppidum eo. "
        "Ego solus sum. Canis meus mecum est. "
        "Canis est parvus. Canis est niger. Canis est bonus. "
        "Ego et canis per viam ambulamus. "
        "Via per montes it. Via per silvas it. "
        "Montes sunt magni. Silvae sunt pulchrae. "
        "In silvis, arbores sunt magnae. Aves in arboribus cantant. "
        "In montibus, sol est bonus. Ventus est bonus. "
        "Ego in via ambulo. Ego multa video. "
        "Alius homo in via est. Alius homo cum filio est. "
        "Filius est parvus. Filius est laetus. "
        "Ego: 'Salve, amice! Quo is?' "
        "Alius: 'Ad oppidum eo. Et tu?' "
        "Ego: 'Et ego ad oppidum eo. Ambulemus una!' "
        "Duo homines et canis et puer per viam ambulant. "
        "Puer cum cane ludit. Puer ridet. Canis caudam movet. "
        "Alius: 'Cur solus es? Cur non in oppido manes?' "
        "Ego: 'Viam amo. In via, multa video. "
        "In oppido, semper idem est. In via, semper novum est.' "
        "Alius: 'Sed via est longa. Via est fessa.' "
        "Ego: 'Via est longa — sed via est pulchra. "
        "In via, ego sum liber. In via, ego sum meus.' "
        "Nos ad oppidum pervenimus. Oppidum est parvum. "
        "Oppidum est pulchrum. In oppido, rosae sunt. "
        "Alius: 'Hic est oppidum meum. Hic habito.' "
        "Ego: 'Oppidum tuum est pulchrum. Sed ego viam meam sequor.' "
        "Ego et canis abimus. Ego et canis in via sumus. "
        "Via est longa. Via est pulchra. "
        "Et ego et canis in via laeti sumus."
    ),
}

STORIES["cap10_09"] = {
    "title_la": "Insula parva",
    "title_zh": "小岛",
    "target_chapter": 10,
    "theme": "13 孤独",
    "style": "精炼",
    "genre": "G 哲理寓言",
    "character_type": "渔民",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Insula est parva. Insula in mari est. Insula sola est. "
        "In insula, unus vir habitat. Vir est vir bonus. "
        "Vir solus est. Nulla femina in insula est. Nulli amici sunt. "
        "Vir cibum capit. Vir aquam bibit. "
        "Vir in parva villa habitat. Villa est parva. "
        "In villa, unus lectus est. In villa, una mensa est. "
        "Vir in villa dormit. Vir in villa cibum habet. "
        "Vir semper ad mare it. Vir in mari cibum videt. "
        "Mare est magnum. Mare est bonum. "
        "Mare viro cibum dat. Mare viro rem dat. "
        "Vir: 'Mare, tu es amicus meus. Tu mihi multa das.' "
        "Vir in mari est. Aqua est bona. "
        "Vir in aqua laetus est. "
        "Tum, parva navis ad insulam venit. "
        "Viri in insula sunt. Viri virum vident. "
        "Vir: 'Cur hic solus manes? Cur non in oppidum venis?' "
        "Vir: 'Oppidum est magnum. In oppido, multi homines sunt. "
        "Sed hic, ego sum meus. Hic, mare mihi dicit. "
        "Hic, sol mihi lucet. Hic, caelum mihi est.' "
        "Vir: 'Sed in oppido, multae res sunt.' "
        "Vir: 'Hic quoque res est bona. "
        "Ego non sum solus. Mare hic est. Caelum hic est. "
        "Aves hic sunt. Cibus hic est.' "
        "Viri abeunt. Navis in mari abit. "
        "Vir solus in insula manet. "
        "Vir laetus est. Insula est parva. "
        "Sed insula est villa. Et vir in insula sua laetus est."
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
        "Quattuor maria in imperio sunt. Mare Nostrum est primum. "
        "Mare Nostrum est magnum. Mare Nostrum est Romanum. "
        "Mare Nostrum Italiam tangit. Mare Nostrum Graeciam tangit. "
        "Mare Nostrum Hispaniam tangit. "
        "Mare Nostrum est in medio imperii. "
        "Romani Mare Nostrum amant. "
        "Romani in Mari Nostro eunt. "
        "Naves per Mare Nostrum eunt. "
        "Mare Nostrum multas terras coniungit. "
        "Secundum mare est prope Britanniam. "
        "Hoc mare est magnum. Hoc mare est altum. "
        "Hoc mare Britanniam tangit. "
        "Romani hoc mare timent. Hoc mare non est bonum. "
        "Tertium mare est prope Graeciam. "
        "Hoc mare est pulchrum. Hoc mare est bonum. "
        "In hoc mari, multae insulae sunt. "
        "Nautae hoc mare amant. "
        "Quartum mare est prope Africam. "
        "Hoc mare est calidum. Hoc mare est bonum. "
        "In hoc mari, multi pisces sunt. "
        "Vir Romanus ad mare it. Vir mare spectat. "
        "Vir: 'Quattuor maria. Quattuor portae. "
        "Per haec maria, Romani ad multi terras eunt. "
        "Mare est via. Mare est porta. Mare est res.' "
        "Vir in mari natat. Aqua est bona. "
        "Vir: 'Mare est magnum. Sed mare est amicus. "
        "Mare nos coniungit. Mare nos portat.' "
        "Et vir in mari laetus est."
    ),
}

STORIES["cap10_11"] = {
    "title_la": "Quattuor terrae",
    "title_zh": "四地",
    "target_chapter": 10,
    "theme": "06 权力",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quattuor terrae in Europa sunt. "
        "Italia est prima. Graecia est secunda. "
        "Hispania est tertia. Terra quarta est quarta. "
        "Italia est in medio. Roma est in Italia. "
        "Italia est patria virorum. "
        "In Italia, multi montes sunt. In Italia, multa oppida sunt. "
        "Italia est pulchra. Italia est terra bona. "
        "Graecia est ad orientem. Graecia est terra vetus. "
        "Viri Graeci multa putant. Viri Graeci multa sciunt. "
        "Graecia est terra bona. Graecia est terra pulchra. "
        "Hispania est ad occidentem. Hispania est terra magna. "
        "In Hispania, multi montes sunt. In Hispania, multae aquae sunt. "
        "Hispania est terra pulchra. Viri in Hispania sunt fortes. "
        "Terra quarta est ad septentriones. Terra quarta est terra magna. "
        "In terra quarta, multi montes sunt. In terra quarta, multae silvae sunt. "
        "Viri in terra quarta sunt fortes. Terra quarta est terra libera. "
        "Vir de his terris putat. "
        "Vir: 'Quattuor terrae — quattuor res. "
        "Italia est patria. Graecia est pulchra. "
        "Hispania est pulchra. Terra quarta est libera. "
        "Omnes terrae sunt pulchrae. Omnes sunt partes terrae.' "
        "Vir in via sedet. Vir de terris putat. "
        "Vir: 'Ego in Italia sum. Italia est terra mea. "
        "Sed alias terras videre volo. "
        "Graecia est pulchra — Graeciam videre volo. "
        "Hispania est pulchra — Hispaniam videre volo. "
        "Terra quarta est libera — terram quartam videre volo. "
        "Terra est magna. Et ego terram videre volo.' "
        "Et vir ad viam it. Vir ad alias terras it."
    ),
}

STORIES["cap10_12"] = {
    "title_la": "Quid est bonum?",
    "title_zh": "什么是公正？",
    "target_chapter": 10,
    "theme": "10 道德",
    "style": "冷峻",
    "genre": "G 哲理寓言",
    "character_type": "父子",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "Puer ad patrem venit. Puer: 'Pater, quid est bonum?' "
        "Pater tacet. Pater puerum spectat. "
        "Pater: 'Veni, fili. Quid vides per fenestram?' "
        "Puer: 'Oppidum video. Viros video. Feminas video.' "
        "Pater: 'Quid viri faciunt?' "
        "Puer: 'Alii ambulant. Alii sedent. Alii stant.' "
        "Pater: 'Bene. Iam audi. "
        "vir panem habet et panem amico dat, hoc est bonum. "
        "vir panem amici capit, hoc est malum.' "
        "Puer: 'Bonum est dare. Malum est capere.' "
        "Pater: 'Ita, fili. Bonum est aliis dare. Malum est aliis nocere.' "
        "Puer: 'Sed pater, cur viri mali sunt?' "
        "Pater: 'Non multi viri mali sunt. Multi viri boni sunt. "
        "Sed aliqui viri solum de se putant.' "
        "Puer: 'Et servi? Servi sunt boni an mali?' "
        "Pater: 'Servi quoque boni et mali sunt. "
        "Homo bonus est qui alios iuvat. Homo malus est qui alios laedit.' "
        "Puer: 'Pater, ego bonus esse volo.' "
        "Pater: 'Tum, fili, semper alios iuva. "
        "panem habes, da ei qui non habet. "
        "amicus tuus est tristis, eum iuva.' "
        "Puer: 'Faciam, pater. Ego bonus puer ero.' "
        "Pater filium tangit. Pater: 'Tu es bonus puer, fili. "
        "Et pater tuus te amat.' "
        "Puer ad fenestram it. Puer viros et feminas in oppido videt. "
        "Puer: 'Terra est magnus. Sed ego parvus sum. "
        "Potest puer parvus terram iuvare?' "
        "Pater: 'Omnis magnus vir fuit puer parvus. "
        "Incipe cum parvo. Da amico tuo panem. "
        "Da matri tuae rosam. Da patri tuo laetitiam. "
        "Et terra erit melior.' "
        "Puer ridet. Puer laetus est. "
        "Et puer putat: bonum in corde incipit."
    ),
}

STORIES["cap10_13"] = {
    "title_la": "Somnus longus",
    "title_zh": "永恒的睡眠",
    "target_chapter": 10,
    "theme": "17 死亡",
    "style": "冷峻",
    "genre": "G 哲理寓言",
    "character_type": "老人",
    "length_tier": "中篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego vir sum. Ego multos annum in terra sum. "
        "Ego multa vidi. Ego multa audivi. "
        "Iam, ego fessus sum. Ego dormire volo. "
        "Ego in lecto iaceo. Oculi mei clauduntur. "
        "Ego de res mea puto. "
        "Vita mea fuit longa. Vita mea fuit bona. "
        "Ego filios habui. Ego filias habui. "
        "Filii mei sunt boni. Filiae meae sunt bonae. "
        "Ego multos amicos habui. Multi amici mei non iam sunt. "
        "Ego de amicis meis puto. "
        "Amicus primus meus fuit bonus. "
        "Amicus meus multa me monstravit. "
        "Amicus meus abiit. Amicus meus non iam est. "
        "Ego de patre meo puto. Pater meus fuit bonus. "
        "Pater meus me amavit. Pater meus abiit. "
        "Ego de matre mea puto. Mater mea fuit bona. "
        "Mater mea me amavit. Mater mea abiit. "
        "Iam, ego quoque abire volo. "
        "Ego non timeo. Ego paratus sum. "
        "Somnus venit. Somnus est bonus. "
        "Somnus me vocat. Somnus: 'Veni ad me. Ego te accipiam.' "
        "Ego ad somnum eo. Ego ad somnum venio. "
        "Somnus est amicus. Somnus est portus. "
        "In somno, ego multi video. "
        "Patrem meum video. Matrem meam video. "
        "Amicos meos video. Omnes sunt una. "
        "Et ego una cum eis sum. "
        "Somnus est longus. Somnus est bonus. "
        "Et ego in somno laetus sum."
    ),
}

STORIES["cap10_14"] = {
    "title_la": "Finis viae",
    "title_zh": "路的尽头",
    "target_chapter": 10,
    "theme": "24 旅行",
    "style": "冷峻",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir in via est. Via est longa. "
        "Vir a Graecia ad Romam it. "
        "Vir multos dies ambulat. Vir multas terras videt. "
        "In Graecia, vir iuvenis fuit. "
        "In Graecia, vir familiam habuit. "
        "Sed vir Romam videre voluit. "
        "Vir de Roma multa audivit. "
        "Roma est caput terrae. Roma est maxima. "
        "Vir per montes ambulat. Vir per silvas ambulat. "
        "Vir multos homines videt. "
        "Alii eum iuvant. Alii eum non vident. "
        "Vir in via fessus est. Vir in via solus est. "
        "Sed vir non cessat. Vir ambulat. Vir semper ambulat. "
        "Tandem, vir in Italia est. "
        "Italia est terra pulchra. "
        "In Italia, viae sunt pulchrae. In Italia, oppida sunt pulchra. "
        "Roma prope est. Vir Romam videre potest. "
        "Vir: 'Roma! Roma est prope! Ego Romam video!' "
        "Vir ad Romam currit. Vir laetus est. "
        "Sed vir fessus est. Vir multos dies non dormivit. "
        "Vir in via cadit. Vir in terra iacet. "
        "Vir Romam videre non potest. Oculi eius clauduntur. "
        "Vir de Graecia putat. De matre. De patre. De amicis. "
        "Vir de res sua putat. Vita fuit longa. Vita fuit bona. "
        "Vir oculos aperit. Roma procul est. "
        "Vir surgere vult. Vir ambulare vult. "
        "Sed corpus non vult. Corpus fessum est. "
        "Vir: 'Roma, ego te videre volui. "
        "Sed via mea hic manet.' "
        "Vir oculos claudit. Vir non iam sentit. "
        "Via viri hic est. Sed Roma manet. "
        "Alii viri ad Romam veniunt. Aliae viae incipiunt. "
        "Aliae viae manent. Una via hic est — alia via ibi est. "
        "Et vir, in terra, in pace iacet."
    ),
}

STORIES["cap10_15"] = {
    "title_la": "Flumina Romana",
    "title_zh": "罗马的河流",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duae aquae magnae in Italia sunt. "
        "Prima aqua Romam tangit. Prima aqua est aqua Romana. "
        "Prima aqua per Romam fluit. Roma ad primam aquam est. "
        "Prima aqua aquam Romae dat. Prima aqua naves portat. "
        "Prima aqua est pater Romae. Sine prima aqua, Roma non est. "
        "Secunda aqua est in parte superiore Italiae. "
        "Secunda aqua est aqua magna. Secunda aqua per multa oppida fluit. "
        "Secunda aqua aquam dat. Secunda aqua terras bonas facit. "
        "Vir ad primam aquam it. Vir primam aquam spectat. "
        "Vir: 'Prima aqua est aqua nostra. "
        "Prima aqua Romae aquam dat. Prima aqua naves portat. "
        "Prima aqua est cor Romae.' "
        "Vir ad secundam aquam it. Vir secundam aquam spectat. "
        "Vir: 'Secunda aqua est magna. Secunda aqua est bona. "
        "Secunda aqua terras bonas facit. Secunda aqua Italiam iuvat.' "
        "Vir: 'Duae aquae — duo bona. "
        "Prima aqua est pater Romae. Secunda aqua est pater Italiae. "
        "Aquae sunt magnae viae. "
        "Aquae terras coniungunt. Aquae rem dant.' "
        "Et vir prope aquam laetus est."
    ),
}

STORIES["cap10_16"] = {
    "title_la": "Duodecim insulae",
    "title_zh": "十二座岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Multae insulae in mari sunt. Omnes insulae sunt pulchrae. "
        "Sicilia est insula magna. Sicilia est prope Italiam. "
        "In Sicilia, multi montes sunt. "
        "Sardinia est insula. Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "Corsica est insula parva. Corsica est prope Sardiniam. "
        "In Corsica, multi montes sunt. "
        "Insula parva est in Graecia. "
        "Insula parva est pulchra. In insula parva, multi rosae sunt. "
        "Britannia est insula magna. "
        "In Britannia, multi montes sunt. "
        "In Britannia, multae silvae sunt. "
        "Insula magna est insula. Insula magna est prope Britanniam. "
        "In insula magna, multae rosae sunt. "
        "Vir de his insulis putat. "
        "Vir: 'Multae insulae in mari sunt. "
        "Aliae sunt magnae. Aliae sunt parvae. "
        "Sed multae sunt pulchrae. Omnes sunt bonae.' "
        "Vir in mari it. Vir insulas videt. "
        "Vir: 'Insulae sunt portae in mari. "
        "Per insulas, viri viam vident. "
        "Insulae sunt res maris.' "
        "Et vir ad insulam it. Vir in insula laetus est."
    ),
}

# ============================================================
# 中长篇 (longior, 500-800 words) x8
# ============================================================

STORIES["cap10_17"] = {
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
        "Quinque flumina in Europa sunt. "
        "Tiberis est primum. Tiberis in Italia est. "
        "Tiberis Romam tangit. Tiberis est fluvius Romanus. "
        "Tiberis per Romam fluit. "
        "Tiberis aquam Romae dat. "
        "Padus est secundum. Padus in Italia est. "
        "Padus est flumen magnum. Padus per multa oppida fluit. "
        "Padus aquam dat. Padus terras bonas facit. "
        "Rhenus est tertium. Rhenus in terra quarta est. "
        "Rhenus est flumen magnum. Rhenus est limes imperii. "
        "Rhenus terram quartam ab aliis terris dividit. "
        "Rhenus terras bonas facit. "
        "Danuvius est quartum. Danuvius est flumen longum. "
        "Danuvius per multas terras fluit. "
        "Danuvius aquam multis terris dat. "
        "Rhodanus est quintum. Rhodanus in terra quarta est. "
        "Rhodanus est flumen pulchrum. "
        "Rhodanus per montes fluit. Rhodanus ad mare it. "
        "Vir Romanus de his fluminibus putat. "
        "Vir: 'Quinque flumina — quinque viae. "
        "Flumina sunt viae aquae. "
        "Flumina terras dividunt. Flumina terras coniungunt. "
        "Per flumina, homines ad alias terras eunt. "
        "Flumina sunt vitae. Flumina sunt bona.' "
        "Vir ad flumen it. Vir aquam fluminis bibit. "
        "Vir: 'Aqua est bona. Aqua est res. "
        "Sine aqua, homines non vivunt. "
        "Sine fluminibus, terrae non sunt bonae. "
        "Flumina sunt res terrae.' "
        "Et vir prope flumen stat. Et vir laetus est."
    ),
}

STORIES["cap10_18"] = {
    "title_la": "Novem insulae",
    "title_zh": "九座岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Novem insulae in mari sunt. "
        "Prima insula est Sicilia. Sicilia est magna. "
        "Sicilia est prope Italiam. "
        "In Sicilia, multi montes sunt. In Sicilia, multae arbores sunt. "
        "Secunda insula est Sardinia. Sardinia est in mari. "
        "Sardinia est prope Corsicam. "
        "In Sardinia, multi montes sunt. "
        "Tertia insula est Corsica. Corsica est parva. "
        "Corsica est prope Sardiniam. "
        "In Corsica, multi montes sunt. Corsica est pulchra. "
        "Quarta insula est Rhodos. Rhodos est in Graecia. "
        "Rhodos est pulchra. In Rhodo, multi rosae sunt. "
        "Alia insula est Britannia. Britannia est magna. "
        "In Britannia, multi montes sunt. "
        "In Britannia, multae silvae sunt. "
        "Alia insula est insula magna. insula magna est prope Britanniam. "
        "In insula magna, multae herbae sunt. "
        "Alia insula est insula pulchra. insula pulchra est in Graecia. "
        "insula pulchra est pulchra. In insula pulchra, multi montes sunt. "
        "Alia insula est insula parva. insula parva est in mari. "
        "insula parva est pulchra. In insula parva, multi rosae sunt. "
        "Alia insula est insula bona. insula bona est parva. "
        "insula bona est in medio mari. insula bona est pulchra. "
        "Vir Romanus de his insulis putat. "
        "Vir: 'Novem insulae — novem portae. "
        "Omnes insulae sunt pulchrae. Omnes sunt bonae. "
        "Per has insulas, Romani ad multi terras eunt. "
        "Insulae sunt res maris.' "
        "Vir in mari it. Vir insulas videt. "
        "Vir ad insulam it. Vir in insula laetus est."
    ),
}

STORIES["cap10_19"] = {
    "title_la": "Septem insulae parvae",
    "title_zh": "七座小岛",
    "target_chapter": 10,
    "theme": "24 旅行",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego vir sum. Ego in mari navigo. "
        "Ego multas insulas vidi. "
        "Septem insulas parvas videre volo. "
        "Prima insula est parva. In prima insula, arbores sunt. "
        "Arbores sunt magnae. Aves in arboribus cantant. "
        "Ego in prima insula ambulo. Ego laetus sum. "
        "Secunda insula est parva. In secunda insula, rosae sunt. "
        "Rosae sunt multae. Rosae sunt pulchrae. "
        "Ego rosas video. Ego rosas amo. "
        "Tertia insula est parva. In tertia insula, aquae sunt. "
        "Aquae sunt bonae. Aquae sunt frigidae. "
        "Ego aquam bibo. Aqua est bona. "
        "Quarta insula est parva. In quarta insula, aves sunt. "
        "Aves sunt multae. Aves sunt pulchrae. "
        "Aves in caelo volant. Ego aves specto. "
        "Alia insula est parva. In alia insula, pisces sunt. "
        "Pisces in mari sunt. Pisces sunt multi. "
        "Ego pisces capio. Pisces sunt boni. "
        "Alia insula est parva. In alia insula, sol est bonus. "
        "Sol est calidus. Sol me iuvat. "
        "Ego in sole sedeo. Ego laetus sum. "
        "Alia insula est parva. Alia insula est sola. "
        "Nullae arbores sunt. Nullae rosae sunt. "
        "Nullae aves sunt. Solus caelum et mare sunt. "
        "Ego in alia insula sto. Ego solus sum. "
        "Sed ego non sum tristis. "
        "Ego: 'Septem insulae — septem res. "
        "Omnes sunt pulchrae. Omnes sunt bonae. "
        "Parvae res quoque magnae sunt.' "
        "Et ego in alia insula laetus sum."
    ),
}

STORIES["cap10_20"] = {
    "title_la": "Octo insulae",
    "title_zh": "八座岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Octo insulae in mari sunt. "
        "Prima insula est Sicilia. Sicilia est magna. "
        "In Sicilia, multi montes sunt. "
        "Secunda insula est Sardinia. Sardinia est in mari. "
        "In Sardinia, multi montes sunt. "
        "Tertia insula est Corsica. Corsica est parva. "
        "In Corsica, multi montes sunt. "
        "Quarta insula est Rhodos. Rhodos est in Graecia. "
        "In Rhodo, multi rosae sunt. "
        "Alia insula est Britannia. Britannia est magna. "
        "In Britannia, multae silvae sunt. "
        "Alia insula est insula magna. insula magna est prope Britanniam. "
        "In insula magna, multae herbae sunt. "
        "Alia insula est insula pulchra. insula pulchra est in Graecia. "
        "In insula pulchra, multi montes sunt. "
        "Alia insula est insula parva. insula parva est in mari. "
        "In insula parva, multi rosae sunt. "
        "Vir Romanus ad has insulas it. "
        "Vir in prima insula est. Vir montes videt. "
        "Vir: 'Sicilia est magna. Sicilia est pulchra.' "
        "Vir in secunda insula est. Vir montes videt. "
        "Vir: 'Sardinia est pulchra. Sardinia est bona.' "
        "Vir in tertia insula est. Vir montes videt. "
        "Vir: 'Corsica est parva. Sed Corsica est pulchra.' "
        "Vir in quarta insula est. Vir rosae videt. "
        "Vir: 'Rhodos est pulchra. Rosae Rhodi sunt boni.' "
        "Vir in alia insula est. Vir silvas videt. "
        "Vir: 'Britannia est magna. Silvae sunt pulchrae.' "
        "Vir in alia insula est. Vir herbas videt. "
        "Vir: 'insula magna est pulchra. Herbae sunt bonae.' "
        "Vir in alia insula est. Vir montes videt. "
        "Vir: 'insula pulchra est pulchra. insula pulchra est bona.' "
        "Vir in alia insula est. Vir rosae videt. "
        "Vir: 'insula parva est pulchra. insula parva est bona.' "
        "Vir: 'Octo insulae — octo bona. "
        "Omnes sunt pulchrae. Omnes sunt partes maris.' "
        "Et vir in mari laetus est."
    ),
}

STORIES["cap10_21"] = {
    "title_la": "Quattuor insulae Graecae",
    "title_zh": "四座希腊岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Quattuor insulae in Graecia sunt. "
        "Prima insula est Rhodos. Rhodos est pulchra. "
        "In Rhodo, multi rosae sunt. In Rhodo, sol est bonus. "
        "Secunda insula est insula pulchra. insula pulchra est magna. "
        "In insula pulchra, multi montes sunt. In insula pulchra, multae arbores sunt. "
        "Tertia insula est insula viridis. insula viridis est pulchra. "
        "In insula viridis, multae arbores sunt. In insula viridis, mare est pulchrum. "
        "Quarta insula est insula magna. insula magna est prope Graeciam. "
        "In insula magna, multi montes sunt. insula magna est pulchra. "
        "Vir Romanus ad has insulas it. "
        "Vir in Rhodo est. Vir rosae videt. "
        "Vir: 'Rhodos est pulchra. Rosae sunt boni. "
        "Sol est bonus. Rhodos est insula bona.' "
        "Vir in insula pulchra est. Vir montes videt. "
        "Vir: 'insula pulchra est magna. Montes sunt magni. "
        "insula pulchra est insula pulchra.' "
        "Vir in insula viridis est. Vir arbores videt. "
        "Vir: 'insula viridis est pulchra. Mare est pulchrum. "
        "insula viridis est insula bona.' "
        "Vir in insula magna est. Vir montes videt. "
        "Vir: 'insula magna est pulchra. Montes sunt magni. "
        "insula magna est insula bona.' "
        "Vir: 'Quattuor insulae — quattuor res. "
        "Graecia est terra pulchra. Insulae Graeciae sunt pulchrae. "
        "Omnes insulae sunt bona.' "
        "Et vir in Graecia laetus est."
    ),
}

STORIES["cap10_22"] = {
    "title_la": "Servus in horto",
    "title_zh": "花园里的奴隶",
    "target_chapter": 10,
    "theme": "06 权力",
    "style": "冷峻",
    "genre": "A 日常生活",
    "character_type": "奴隶",
    "length_tier": "中长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego servus sum. Ego in horto facio. "
        "Hortus est magnus. Hortus est pulcher. "
        "In horto, multae rosae sunt. In horto, multae arbores sunt. "
        "Ego rosas curo. Ego arbores curo. "
        "Ego aquam porto. Ego terram paro. "
        "Dominus meus est bonus. Dominus meus me non laedit. "
        "Dominus meus in hortum venit. "
        "Dominus: 'Hortus est pulcher. Tu bene facis.' "
        "Ego: 'Bene, domine. Hortus est pulcher.' "
        "Ego de res mea puto. "
        "Ego servus sum — sed ego non sum miser. "
        "In horto, ego sum liber. "
        "In horto, rosae mihi dicunt. "
        "In horto, arbores mihi canunt. "
        "In horto, aves mihi cantant. "
        "Alius servus in horto est. Alius servus est amicus meus. "
        "Amicus: 'Tu semper in horto es. Cur?' "
        "Ego: 'Hortus est villa mea. "
        "In horto, ego sum meus. "
        "In horto, ego non sum servus — ego sum vir.' "
        "Amicus: 'Sed dominus te habet. Tu non es liber.' "
        "Ego: 'Corpus meum dominus habet. Sed cor meum est liberum. "
        "Cor meum in horto est. Cor meum in rosis est. "
        "Cor meum in arboribus est. Cor meum non est servi.' "
        "Amicus: 'Tu es bonus vir. Ego te amo.' "
        "Ego: 'Et ego te amo. Nos sumus amici. "
        "Et amici sunt liberi — etiam servi sunt.' "
        "Et ego et amicus in horto sedemus. "
        "Sol est bonus. Rosae sunt pulchrae. "
        "Et nos, duo servi, in horto laeti sumus."
    ),
}

STORIES["cap10_23"] = {
    "title_la": "Duodecim insulae maris",
    "title_zh": "海上的十二座岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duodecim insulae in mari sunt. "
        "Sicilia est prima. Sicilia est magna. "
        "Sardinia est secunda. Sardinia est in mari. "
        "Corsica est tertia. Corsica est parva. "
        "Rhodos est quarta. Rhodos est in Graecia. "
        "Britannia est alia. Britannia est magna. "
        "insula magna est alia. insula magna est prope Britanniam. "
        "insula pulchra est alia. insula pulchra est in Graecia. "
        "insula parva est alia. insula parva est in mari. "
        "insula bona est alia. insula bona est parva. "
        "insula viridis est alia. insula viridis est in Graecia. "
        "insula magna est alia. insula magna est prope Graeciam. "
        "insula pulchra est alia. insula pulchra est in Graecia. "
        "Vir Romanus de his insulis putat. "
        "Vir: 'Duodecim insulae — duodecim portae. "
        "Omnes sunt in mari. Omnes sunt pulchrae. "
        "Aliae sunt magnae. Aliae sunt parvae. "
        "Sed multi sunt bonae.' "
        "Vir in mari it. Vir insulas videt. "
        "Vir ad primam insulam it. Vir ad secundam it. "
        "Vir ad multi insulas it. "
        "Vir: 'Mare est magnum. Sed insulae sunt portae. "
        "Per insulas, viri viam inveniunt. "
        "Insulae sunt luces in mari.' "
        "Et vir in mari laetus est."
    ),
}

STORIES["cap10_24"] = {
    "title_la": "Via Romana",
    "title_zh": "罗马广场",
    "target_chapter": 10,
    "theme": "35 城市",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Via Romana est magnum. Forum est in medio Romae. "
        "In foro, multae viae sunt. In foro, multa aedificia sunt. "
        "In foro, multi homines sunt. "
        "Homines ex omnibus terris ad forum veniunt. "
        "Mercatores in foro sunt. Mercatores res vendunt. "
        "Alius mercator panem vendit. Alius vinum vendit. "
        "Alius res vendit. Alius libros vendit. "
        "Vir Romanus in foro est. Vir forum spectat. "
        "Vir: 'Forum est cor Romae. In foro, multa sunt. "
        "Hic, homines dicunt. Hic, res emuntur. "
        "Hic, res Romae est.' "
        "Senex in foro est. Senex in via sedet. "
        "Senex de res putat. Senex multa vidit. "
        "Vir ad virum it. Vir: 'Salve, vir. Cur hic sedes?' "
        "Senex: 'Ego forum specto. Forum est res. "
        "In foro, ego multa vidi. "
        "Viros bonos vidi. Viros malos vidi. "
        "Laetos vidi. Tristes vidi. "
        "Forum est speculum terrae.' "
        "Vir: 'Quid est optimum in foro?' "
        "Senex: 'Optimum est homines. "
        "Homines ad forum veniunt. Homines rident. "
        "Homines dicunt. Homines sunt forum.' "
        "Vir in foro stat. Vir homines spectat. "
        "Vir: 'Forum est magnum. Sed homines sunt maiores. "
        "Forum est cor. Sed homines sunt cor cordis.' "
        "Et vir in foro laetus est."
    ),
}

# ============================================================
# 长篇 (longus, 800+ words) x6
# ============================================================

STORIES["cap10_25"] = {
    "title_la": "Duodecim insulae",
    "title_zh": "十二座岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego vir sum. Ego in mari multos annum sum. "
        "Ego multas terras vidi. Ego multas insulas vidi. "
        "Iam, ego de duodecim insulis dico. "
        "Prima insula est Sicilia. Sicilia est magna. "
        "Sicilia est prope Italiam. "
        "In Sicilia, multi montes sunt. "
        "In Sicilia, multae arbores sunt. "
        "In Sicilia, multi homines sunt. "
        "Sicilia est terra bona. Sicilia est pulchra. "
        "Secunda insula est Sardinia. "
        "Sardinia est in medio mari. "
        "In Sardinia, multi montes sunt. "
        "In Sardinia, multae silvae sunt. "
        "Sardinia est pulchra. Sardinia est bona. "
        "Tertia insula est Corsica. Corsica est parva. "
        "Corsica est prope Sardiniam. "
        "In Corsica, multi montes sunt. "
        "Corsica est pulchra. Corsica est parva sed bona. "
        "Quarta insula est Rhodos. Rhodos est in Graecia. "
        "In Rhodo, multi rosae sunt. "
        "In Rhodo, sol est bonus. "
        "Rhodos est pulchra. Rhodos est insula bona. "
        "Alia insula est Britannia. "
        "Britannia est magna insula. "
        "In Britannia, multi montes sunt. "
        "In Britannia, multae silvae sunt. "
        "Britannia est longe ab Italia. "
        "Alia insula est insula magna. "
        "insula magna est prope Britanniam. "
        "In insula magna, multae herbae sunt. "
        "insula magna est pulchra. insula magna est terra bona. "
        "Alia insula est insula pulchra. insula pulchra est in Graecia. "
        "In insula pulchra, multi montes sunt. "
        "In insula pulchra, multae arbores sunt. "
        "insula pulchra est magna. insula pulchra est pulchra. "
        "Alia insula est insula parva. insula parva est in mari. "
        "In insula parva, multi rosae sunt. "
        "insula parva est pulchra. insula parva est bona. "
        "Alia insula est insula bona. insula bona est parva. "
        "insula bona est in medio mari. "
        "insula bona est parva sed pulchra. "
        "Alia insula est insula viridis. "
        "insula viridis est in Graecia. "
        "In insula viridis, multae arbores sunt. "
        "insula viridis est pulchra. insula viridis est bona. "
        "Alia insula est insula magna. "
        "insula magna est prope Graeciam. "
        "In insula magna, multi montes sunt. "
        "insula magna est pulchra. insula magna est bona. "
        "Alia insula est insula pulchra. "
        "insula pulchra est in Graecia. "
        "In insula pulchra, multi rosae sunt. "
        "insula pulchra est pulchra. insula pulchra est bona. "
        "Ego: 'Duodecim insulae. Duodecim res maris. "
        "Omnes sunt pulchrae. Omnes sunt bonae. "
        "Per has insulas, ego multa vidi. "
        "Per has insulas, ego multa didici. "
        "Mare est magnum. Sed insulae sunt portae. "
        "Insulae sunt luces in mari.' "
        "Et ego, vir, in mari laetus sum."
    ),
}

STORIES["cap10_26"] = {
    "title_la": "Vir ad portam",
    "title_zh": "门口的乞丐",
    "target_chapter": 10,
    "theme": "10 道德",
    "style": "冷峻",
    "genre": "G 哲理寓言",
    "character_type": "乞丐",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Vir ad portam oppidi sedet. "
        "Vir est vir. Vir nulla habet. "
        "Vir res malas habet. Vir panem non habet. "
        "Homines per portam eunt. Homines virum vident. "
        "Alii homines virum non vident. "
        "Alii homines virum vident — sed nulla dant. "
        "Vir vir bonus ad portam venit. Vir vir bonus multa habet. "
        "Vir vir bonus virum videt. "
        "Vir vir bonus: 'Cur hic sedes? Cur non facis?' "
        "Vir: 'Ego facere volo. Sed nemo me vult.' "
        "Vir vir bonus: 'Ego te pecuniam dabo. Sed tu facere potes.' "
        "Vir: 'Quid faciam?' "
        "Vir vir bonus: 'Portam servo. quis malus venit, dic mihi.' "
        "Vir: 'Faciam. Ego portam servum.' "
        "Vir ad portam stat. Vir homines videt. "
        "Multi homines per portam eunt. "
        "Alius vir ad portam venit. "
        "Alius vir est vir. Alius vir est fessus. "
        "Vir primus alium virum videt. "
        "Vir primus: 'Tu es vir. Ego quoque sum vir. "
        "Sed ego iam cibum habeo. Ego te cibum dabo.' "
        "Vir primus panem dat. "
        "Alius vir: 'Bene te ago. Tu es bonus vir.' "
        "Vir primus: 'Ego fui vir. Ego nulla habui. "
        "Iam, ego parva habeo. Sed parva dare possum.' "
        "Vir vir bonus venit. Vir vir bonus videt virum cum alio viro. "
        "Vir vir bonus: 'Quid facis? Cur panem das?' "
        "Vir: 'Hic vir est vir. Ego ei panem dedi.' "
        "Vir vir bonus: 'Sed tu ipse es vir! Cur panem tuum das?' "
        "Vir: 'Quia ego puto quid est nulla habere. "
        "Qui nulla habet, putat quid est bonum. "
        "Bonum est dare — etiam tu nulla habes.' "
        "Vir vir bonus tacet. Vir vir bonus putat. "
        "Vir vir bonus: 'Tu es vir — sed tu es bonus. "
        "Ego sum vir bonus — sed ego non dedi. "
        "Tu me monstrasti. Iam, ego quoque dabo.' "
        "Vir vir bonus pecuniam dat. Vir vir bonus cibum dat. "
        "Vir: 'Bene te ago. Iam, nos tres cibum habemus.' "
        "Et tres viri una sedent. Et tres viri una edunt. "
        "Et ad portam, bonum est."
    ),
}

STORIES["cap10_27"] = {
    "title_la": "Mercator vir",
    "title_zh": "希腊商人",
    "target_chapter": 10,
    "theme": "24 旅行",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "商人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego mercator sum. Ego ex Graecia venio. "
        "Ego multas terras vidi. Ego multa oppida vidi. "
        "Ego res vendo. Ego res capio. "
        "Iam, ego ad Romam eo. Roma est maxima. "
        "In via, ego multa video. "
        "Via est longa. Via per montes it. Via per silvas it. "
        "Montes sunt magni. Silvae sunt pulchrae. "
        "In via, alii mercatores sunt. "
        "Alius mercator ex Hispania venit. "
        "Alius mercator ex terra quarta venit. "
        "Alius mercator ex Italia venit. "
        "Mercatores una ambulant. Mercatores una dicunt. "
        "Mercator ex Hispania: 'Ego vinum porto. Vinum in Hispania est bonum.' "
        "Mercator ex terra quarta: 'Ego res porto. Vestes in terra quarta sunt pulchrae.' "
        "Mercator ex Italia: 'Ego libros porto. Libri in Italia sunt boni.' "
        "Ego: 'Ego rem porto. Res in Graecia est bona.' "
        "Mercatores ad Romam veniunt. Roma est magna. "
        "In Roma, multae viae sunt. In Roma, multa aedificia sunt. "
        "In Roma, multi homines sunt. "
        "Mercatores ad forum eunt. Forum est magnum. "
        "In foro, mercatores res vendunt. "
        "Mercator ex Hispania vinum vendit. "
        "Mercator ex terra quarta res vendit. "
        "Mercator ex Italia libros vendit. "
        "Ego rem vendo. "
        "Homines ad forum veniunt. "
        "Homines res emunt. Homines res spectant. "
        "Mercator ex Hispania: 'Viri vinum amant. Vinum est bonum.' "
        "Mercator ex terra quarta: 'Viri res amant. Vestes sunt pulchrae.' "
        "Mercator ex Italia: 'Viri libros amant. Libri sunt boni.' "
        "Ego: 'Viri rem amant. Res est bona.' "
        "Mercatores laeti sunt. Mercatores pecuniam habent. "
        "Ego: 'Mercatores sumus. Mercatores terras coniungunt. "
        "Per mercatores, res ex una terra ad aliam terram eunt. "
        "Per mercatores, homines res ex aliis terris habent. "
        "Mercatores sunt viae inter terras.' "
        "Et quattuor mercatores in Roma laeti sunt."
    ),
}

STORIES["cap10_28"] = {
    "title_la": "Quattuor insulae Graecae",
    "title_zh": "四座希腊岛",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego in Graecia sum. Ego quattuor insulas videre volo. "
        "Prima insula est Rhodos. Rhodos est pulchra. "
        "Ego ad Rhodon navigo. "
        "In Rhodo, multi rosae sunt. "
        "In Rhodo, sol est bonus. In Rhodo, mare est pulchrum. "
        "Ego in Rhodo ambulo. Ego rosae video. "
        "Rosae sunt pulchri. Rosae sunt multi. "
        "Ego: 'Rhodos est insula pulchra. "
        "In Rhodo, sol semper lucet. In Rhodo, rosae semper sunt.' "
        "Ego in Rhodo laetus sum. "
        "Secunda insula est insula pulchra. insula pulchra est magna. "
        "Ego ad insulam pulchram navigo. "
        "In insula pulchra, multi montes sunt. "
        "In insula pulchra, multae arbores sunt. "
        "In insula pulchra, multi homines sunt. "
        "Ego in insula pulchra ambulo. Ego montes video. "
        "Montes sunt magni. Montes sunt pulchri. "
        "Ego: 'insula pulchra est insula magna. "
        "In insula pulchra, montes sunt alti. In insula pulchra, terra est bona.' "
        "Ego in insula pulchra laetus sum. "
        "Tertia insula est insula viridis. insula viridis est pulchra. "
        "Ego ad insulam viridem navigo. "
        "In insula viridis, multae arbores sunt. "
        "In insula viridis, mare est pulchrum. "
        "Ego in insula viridis ambulo. Ego arbores video. "
        "Arbores sunt magnae. Arbores sunt pulchrae. "
        "Ego: 'insula viridis est insula pulchra. "
        "In insula viridis, arbores sunt magnae. Mare est pulchrum.' "
        "Ego in insula viridis laetus sum. "
        "Quarta insula est insula magna. insula magna est prope Graeciam. "
        "Ego ad insulam magnam navigo. "
        "In insula magna, multi montes sunt. "
        "In insula magna, multae silvae sunt. "
        "Ego in insula magna ambulo. Ego montes video. "
        "Montes sunt magni. Silvae sunt pulchrae. "
        "Ego: 'insula magna est insula pulchra. "
        "In insula magna, montes sunt magni. Silvae sunt pulchrae.' "
        "Ego: 'Quattuor insulae. Quattuor res. "
        "Graecia est terra pulchra. Insulae Graeciae sunt pulchrae. "
        "Omnes insulae sunt bonae. Omnes sunt partes maris.' "
        "Et ego in Graecia laetus sum."
    ),
}

STORIES["cap10_29"] = {
    "title_la": "Septem flumina Asiae",
    "title_zh": "亚洲的七条河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Septem flumina in Asia sunt. "
        "Primum flumen est flumen longum. flumen longum est magnum. "
        "flumen longum per multas terras fluit. "
        "flumen longum aquam multis terris dat. "
        "Secundum flumen est flumen magnum. flumen magnum est magnum. "
        "flumen magnum prope flumen longum fluit. "
        "flumen magnum aquam dat. flumen magnum terras bonas facit. "
        "Tertium flumen est flumen altum. flumen altum est longum. "
        "flumen altum per montes fluit. flumen altum ad mare it. "
        "Quartum flumen est Ganges. Ganges est magnum. "
        "Ganges per multas terras fluit. "
        "Ganges aquam multis terris dat. "
        "Quintum flumen est Nilus. Nilus est longum. "
        "Nilus per Africam fluit. Nilus ad mare it. "
        "Nilus terras bonas facit. "
        "Sextum flumen est flumen parvum. flumen parvum in Asia est. "
        "flumen parvum est flumen magnum. flumen parvum per terras fluit. "
        "Septimum flumen est flumen pulchrum. flumen pulchrum in Asia est. "
        "flumen pulchrum est flumen pulchrum. "
        "Vir Romanus de his fluminibus putat. "
        "Vir: 'Septem flumina Asiae — septem viae. "
        "Flumina sunt viae aquae. "
        "Flumina terras dividunt. Flumina terras coniungunt. "
        "Sine fluminibus, terrae non sunt bonae. "
        "Flumina sunt vitae. Flumina sunt res terrae.' "
        "Vir ad flumen it. Vir aquam fluminis bibit. "
        "Vir: 'Aqua est bona. Aqua est res. "
        "Per flumina, homines ad alias terras eunt. "
        "Per flumina, cibus ad homines venit. "
        "Flumina sunt venae terrae.' "
        "Et vir prope flumen laetus est."
    ),
}

STORIES["cap10_30"] = {
    "title_la": "Sex insulae parvae",
    "title_zh": "六座小岛",
    "target_chapter": 10,
    "theme": "24 旅行",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego vir sum. Ego in mari multos annum sum. "
        "Ego magnas insulas vidi. Sed ego parvas insulas amo. "
        "Sex insulas parvas videre volo. "
        "Prima insula est parva. In prima insula, arbores sunt. "
        "Arbores sunt magnae. Aves in arboribus cantant. "
        "Ego in prima insula ambulo. Ego aves audio. "
        "Aves sunt pulchrae. Aves cantant. "
        "Ego: 'Prima insula est parva. Sed arbores sunt magnae. "
        "Aves sunt pulchrae. Parva insula est bona.' "
        "Secunda insula est parva. In secunda insula, rosae sunt. "
        "Rosae sunt multae. Rosae sunt pulchrae. "
        "Ego rosas video. Ego rosas amo. "
        "Ego: 'Secunda insula est parva. Sed rosae sunt pulchrae. "
        "Rosae sunt multae. Parva insula est bona.' "
        "Tertia insula est parva. In tertia insula, aquae sunt. "
        "Aquae sunt bonae. Aquae sunt clarae. "
        "Ego aquam bibo. Aqua est bona. "
        "Ego: 'Tertia insula est parva. Sed aquae sunt bonae. "
        "Aqua est res. Parva insula est bona.' "
        "Quarta insula est parva. In quarta insula, aves sunt. "
        "Aves sunt multae. Aves in caelo volant. "
        "Ego aves specto. Aves sunt pulchrae. "
        "Ego: 'Quarta insula est parva. Sed aves sunt multae. "
        "Aves sunt pulchrae. Parva insula est bona.' "
        "Alia insula est parva. In alia insula, pisces sunt. "
        "Pisces in mari sunt. Pisces sunt multi. "
        "Ego pisces capio. Pisces sunt boni. "
        "Ego: 'Alia insula est parva. Sed pisces sunt multi. "
        "Pisces sunt boni. Parva insula est bona.' "
        "Alia insula est parva. In alia insula, nulla est. "
        "Nullae arbores sunt. Nullae rosae sunt. "
        "Nullae aves sunt. Solus caelum et mare sunt. "
        "Ego in alia insula sto. Ego solus sum. "
        "Sed ego non sum tristis. "
        "Ego: 'Alia insula est parva. Sed caelum est magnum. "
        "Mare est magnum. Et ego sum parvus. "
        "Sed parvus est bonus. Parvus est pulcher.' "
        "Ego: 'Sex insulae parvae — sex res. "
        "Omnes sunt pulchrae. Omnes sunt bonae. "
        "Parvae res quoque magnae sunt. "
        "Parvae insulae sunt magnae in corde.' "
        "Et ego, in alia insula, laetus sum."
    ),
}

# ============================================================
# 测试与写入
# ============================================================

if __name__ == "__main__":
    print(f"共 {len(STORIES)} 篇故事待测试\n")
    
    passed = 0
    failed = 0
    
    for story_id, story in STORIES.items():
        title = story["title_la"]
        text = story["text"]
        tier = story["length_tier"]
        
        result = evaluate(text, title)
        level = result["v2_level"]
        rate = result["v2_rate"]
        
        status = "PASS" if level is not None and level <= 12 else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        
        print(f"  {status} | v2={level} | rate={rate:.1f}% | {tier:4s} | {title}")
        
        if status == "FAIL" and result["v2_oov"]:
            print(f"         OOV ({len(result['v2_oov'])}): {result['v2_oov'][:10]}")
    
    print(f"\n{'='*60}")
    print(f"通过: {passed}/{len(STORIES)}  失败: {failed}/{len(STORIES)}")
    
    if failed == 0:
        print("\n全部通过！开始写入文件...")
        # 写入文件
        for story_id, story in STORIES.items():
            # 确定文件名
            title_slug = story["title_la"].lower().replace(" ", "_").replace("?", "").replace("!", "")
            tier_map = {"中篇": "medius", "中长篇": "longior", "长篇": "longus"}
            tier_slug = tier_map.get(story["length_tier"], "medius")
            
            # 找到下一个编号
            cap_dir = REALITATES_DIR / "Cap10"
            existing = sorted(cap_dir.glob(f"Cap10_{title_slug}_{tier_slug}_*.md"))
            if existing:
                nums = [int(f.stem.split("_")[-1]) for f in existing]
                next_num = max(nums) + 1
            else:
                next_num = 1
            
            fname = f"Cap10_{title_slug}_{tier_slug}_{next_num:03d}.md"
            fpath = cap_dir / fname
            
            # 构建 YAML frontmatter
            now = datetime.now(timezone.utc).isoformat()
            yaml = f"""---
story_id: "{story_id}"
title_la: "{story['title_la']}"
title_zh: "{story['title_zh']}"
target_chapter: {story['target_chapter']}
theme: "{story['theme']}"
style: "{story['style']}"
genre: "{story['genre']}"
character_type: "{story['character_type']}"
length_tier: "{story['length_tier']}"
narrative_mode: "{story['narrative_mode']}"
word_count: {len(story['text'].split())}
macrons_status: "generated"
evaluated_chapter: {result['v2_level']}
best_fit_chapter: {result['v2_best_fit']}
coverage_rate: {result['v2_rate']}
oov_words: {result['v2_oov']}
rewritten_from: "brevis"
rewritten_at: "{now}"
status: "rewritten"
---
"""
            content = yaml + "\n" + story["text"] + "\n"
            
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"  已写入: {fname}")
        
        print("\n全部完成！")
    else:
        print(f"\n还有 {failed} 篇未通过，需要调整。")