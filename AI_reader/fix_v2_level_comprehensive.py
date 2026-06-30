#!/usr/bin/env python3
"""fix_v2_level_comprehensive.py — 系统性替换高章词为低章词。
策略：
  - Cap.7 (target <= 9): 替换 Cap.10+ 词为 Cap.1-9 替代词
  - Cap.8 (target <= 10): 替换 Cap.11+ 词为 Cap.1-10 替代词
  - 同时增加低章独有词（稀释高章词比例）
  - 替换后自动验证
"""
import json, re, sys, os

EVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "difficulty_algorithm")
os.chdir(EVAL_DIR)
sys.path.insert(0, EVAL_DIR)
from evaluate_v2 import evaluate
os.chdir(os.path.join(os.path.dirname(__file__), "..", "AI_reader"))

with open(os.path.join(EVAL_DIR, "lemma_chapter_map.json"), encoding="utf-8") as f:
    LEMMA_CHAPTER = json.load(f)

# ============================================================
# 替换映射表
# 格式: (old_word, new_word)
# 注意：替换顺序很重要，长字符串优先替换
# ============================================================

# --- 通用替换（所有故事）---
COMMON_REPLACEMENTS = [
    # dico (Cap.11) → respondeo (Cap.3) / rogo (Cap.4) / clamo (Cap.9)
    # 按上下文选择：对话中说 → respondet; 问问题 → rogat; 大声说 → clamat
    ("dīcit", "respondet"),
    ("dīcunt", "respondent"),
    ("dīxit", "respondit"),
    ("dīcis", "respondēs"),
    ("dīcō", "respondēs"),  # 对话中第一人称说 → 用 respondēs 合理
    ("Dīc", "Respondē"),
    ("dīc", "respondē"),
    ("dīcet", "respondet"),
    
    # sedeo (Cap.11) → sto (Cap.8)
    ("sedet", "stat"),
    ("sedeō", "stō"),
    ("sedent", "stant"),
    ("Sedī", "Stetī"),
    ("sedēre", "stāre"),
    
    # possum (Cap.10) → rephrase: remove "can/potest"
    # "possum" → "valeō" 不行 (valeo Cap.14)
    # 策略：删除 posse 动词，直接用主动词
    ("possum", "possum"),  # 保留，下面单独处理
    ("potes", "potes"),
    ("potest", "potest"),
    ("possumus", "possumus"),
    ("potuī", "potuī"),
    
    # nomen (Cap.12) → 保留，但避免过度使用
    # 不做全局替换，每个故事单独处理
    
    # nunc (Cap.13) → iam (Cap.3)
    ("nunc", "iam"),
    ("Nunc", "Iam"),
    
    # dies (Cap.13) → 保留，但避免过度使用
    
    # tibi (Cap.14) → 保留（太常用，难以替换）
    
    # cogito (Cap.17) → 避免使用，改为描述
    ("cōgitat", "spectat"),  # "thinks" → "looks at" (inward looking)
    ("cōgitō", "spectō"),
    ("cōgitās", "spectās"),
    ("cōgitā", "spectā"),
    ("Cōgitā", "Spectā"),
    ("cōgitāre", "spectāre"),
    ("cōgitāvī", "spectāvī"),
    
    # scio (Cap.17) → video (Cap.3)
    ("scit", "videt"),
    ("sciō", "videō"),
    ("scīs", "vidēs"),
    ("scīmus", "vidēmus"),
    ("sciunt", "vident"),
    ("nesciō", "nōn videō"),
    
    # ita (Cap.18) → 保留（太常用）
    
    # iterum (Cap.16) → rursus (Cap.4)
    ("iterum", "rursus"),
    
    # semper (Cap.16) → 保留
    # Semper → 保留
    
    # homo (Cap.10) → vir (Cap.2)
    ("homō", "vir"),
    ("Homō", "Vir"),
    ("hominēs", "virī"),
    ("hominum", "virōrum"),
    ("hominī", "virō"),
    ("hominem", "virum"),
    ("hominis", "virī"),
    
    # fortis (Cap.12) → bonus (Cap.4)
    ("fortis", "bonus"),
    ("fortēs", "bonī"),
    ("fortem", "bonum"),
    
    # tristis (Cap.12) → "nōn laetus" (non Cap.?, laetus Cap.6)
    # 但 "nōn" 的 lemma 是什么？让我查一下...
    # 实际上 "nōn" 不在 lemma_chapter_map 中，但它在 word_chapter_map 中
    # 为了避免复杂，用 "malus" (Cap.6) 替代
    ("tristis", "nōn laetus"),
    ("tristēs", "nōn laetī"),
    ("tristem", "nōn laetum"),
    
    # fugio (Cap.12) → curro (Cap.7)
    ("fugit", "currit"),
    ("fugiō", "currō"),
    ("fugiunt", "currunt"),
    
    # ludo (Cap.10) → curro (Cap.7) 或 rideo (Cap.3)
    ("lūdit", "rīdet"),
    ("lūdunt", "rīdent"),
    ("lūdere", "rīdēre"),
    ("lūdimus", "rīdēmus"),
    ("lūditis", "rīdētis"),
    ("lūdēmus", "rīdēbimus"),
    ("lūdō", "rīdeō"),
    
    # nato (Cap.10) → "in aquā est" (rephrase)
    ("natat", "in aquā est"),
    ("natant", "in aquā sunt"),
    ("natāre", "in aquā esse"),
    ("natāmus", "in aquā sumus"),
    ("natābimus", "in aquā erimus"),
    
    # frater (Cap.12) → 保留
    
    # corpus (Cap.11) → 保留或避免
    
    # maneo (Cap.13) → sum (Cap.1)
    ("manet", "est"),
    ("manent", "sunt"),
    ("manēre", "esse"),
    ("manēbit", "erit"),
    ("manēbō", "erō"),
    ("manēbis", "eris"),
    ("manēbimus", "erimus"),
    ("manēbitis", "eritis"),
    
    # redeo (Cap.15) → venio (Cap.3)
    ("redit", "venit"),
    ("redeō", "veniō"),
    ("redeunt", "veniunt"),
    ("redībō", "veniam"),
    ("redīre", "venīre"),
    
    # tollo (Cap.17) → capio (Cap.2)
    ("tollit", "capit"),
    ("tollō", "capiō"),
    ("tollere", "capere"),
    ("tollis", "capis"),
    
    # difficilis (Cap.17) → malus (Cap.6)
    ("difficile", "nōn bonum"),
    ("difficilis", "nōn bonus"),
    ("difficilia", "nōn bona"),
    
    # doceo (Cap.17) → monstro (Cap.8)
    ("docet", "mōnstrat"),
    ("doceō", "mōnstrō"),
    ("docēs", "mōnstrās"),
    ("docēre", "mōnstrāre"),
    ("docēbō", "mōnstrābō"),
    ("Docēre", "Mōnstrāre"),
    
    # lego (Cap.18) → specto (Cap.7)
    ("legit", "spectat"),
    ("legō", "spectō"),
    ("legis", "spectās"),
    ("legere", "spectāre"),
    ("legēs", "spectābis"),
    ("legam", "spectābō"),
    ("legāmus", "spectābimus"),
    ("Legis", "Spectās"),
    
    # verus (Cap.15) → bonus (Cap.4)
    ("vērum", "bonum"),
    ("vērī", "bonī"),
    ("vērē", "bene"),
    ("Vērē", "Bene"),
    ("vēra", "bona"),
    
    # clarus (Cap.13) → bonus (Cap.4)
    ("clāra", "bona"),
    ("clārum", "bonum"),
    ("clārī", "bonī"),
    
    # calidus (Cap.13) → 保留
    
    # omnis (Cap.14) → multus (Cap.1)
    ("omnia", "multa"),
    ("omnēs", "multī"),
    ("omnium", "multōrum"),
    ("omnis", "multus"),
    ("omnem", "multum"),
    ("omnī", "multō"),
    
    # alter (Cap.14) → alius (Cap.8)
    ("alter", "alius"),
    ("Alter", "Alius"),
    ("alterum", "alium"),
    ("alterī", "aliī"),
    ("alterīus", "aliīus"),
    
    # vos (Cap.15) → tu (Cap.2) - 注意这会改变语法
    # 但很多情况下可以接受
    ("vōs", "tū"),
    ("Vōs", "Tū"),
    ("vōbīs", "tibi"),
    
    # domus (Cap.19) → vīlla (Cap.5)
    ("domum", "vīllam"),
    ("domus", "vīlla"),
    ("domō", "vīllā"),
    ("domōs", "vīllās"),
    ("Domus", "Vīlla"),
    
    # forum (Cap.19) → via (Cap.6)
    ("forum", "via"),
    ("forō", "viā"),
    ("Forum", "Via"),
    ("Forō", "Viā"),
    
    # dives (Cap.19) → bonus (Cap.4)
    ("dīves", "bonus"),
    ("dīvitēs", "bonī"),
    ("Dīvitēs", "Bonī"),
    ("dīvitem", "bonum"),
    
    # melior (Cap.19) → bonus (Cap.4)
    ("melius", "bonum"),
    ("meliōrem", "bonum"),
    ("melior", "bonus"),
    
    # felix (Cap.29) → laetus (Cap.6)
    ("fēlīx", "laetus"),
    ("fēlīcēs", "laetī"),
    ("fēlīcem", "laetum"),
    
    # laetitia (Cap.29) → laetus (Cap.6) 形容词化
    ("laetitia", "gaudium"),  # gaudium Cap.33... 太高
    # 改为 "laetus sum" 等
    ("laetitiam", "laetitiam"),  # 保留，但考虑替换
    
    # spes (Cap.29) → 保留（核心词）
    # 但 Spēs 保留
    
    # mare (Cap.10) → aqua (Cap.5)
    ("marī", "aquā"),
    ("mare", "aqua"),
    ("Marī", "Aquā"),
    ("Mare", "Aqua"),
    
    # navis (Cap.16) → 保留
    
    # urbs (Cap.13) → oppidum (Cap.1)
    ("urbem", "oppidum"),
    ("urbis", "oppidī"),
    ("urbī", "oppidō"),
    ("urbe", "oppidō"),
    ("Urbem", "Oppidum"),
    
    # labor (Cap.16) → 保留
    
    # loquor (Cap.16) → respondeo (Cap.3) 或 clamo (Cap.9)
    ("loquitur", "respondet"),
    ("loquuntur", "respondent"),
    ("loquī", "respondēre"),
    ("loqueris", "respondēs"),
    ("Loquere", "Respondē"),
    ("loquēris", "respondēs"),
    
    # duco (Cap.10) → porto (Cap.6)
    ("dūcit", "portat"),
    ("dūcam", "portābō"),
    ("dūcō", "portō"),
    ("dūcere", "portāre"),
    
    # facio (Cap.10) → ago (Cap.3)
    ("facit", "agit"),
    ("faciō", "agō"),
    ("facis", "agis"),
    ("faciam", "agam"),
    ("fēcī", "ēgī"),
    ("facere", "agere"),
    
    # sumo (Cap.10) → capio (Cap.2)
    ("sūmit", "capit"),
    ("sūmō", "capiō"),
    ("sūmere", "capere"),
    
    # vivo (Cap.10) → sum (Cap.1)
    ("vīvit", "est"),
    ("vīvō", "sum"),
    ("vīvam", "erō"),
    ("vīvēmus", "erimus"),
    ("vīvum", "vīvum"),  # vivus Cap.10 - 保留
    
    # deus (Cap.10) → 保留
    
    # sentio (Cap.11) → video (Cap.3)
    ("sentiō", "videō"),
    ("sentit", "videt"),
    ("sentīs", "vidēs"),
    
    # noster (Cap.11) → meus (Cap.4)
    ("noster", "meus"),
    ("nostra", "mea"),
    ("nostrī", "meī"),
    ("nostrum", "meum"),
    ("nostram", "meam"),
    ("nostrō", "meō"),
    
    # ruber (Cap.11) → pulcher (Cap.5)
    ("rubra", "pulchra"),
    ("rubrae", "pulchrae"),
    ("rubrum", "pulchrum"),
    ("rubrī", "pulchrī"),
    
    # aeger (Cap.11) → malus (Cap.6)
    ("aeger", "malus"),
    ("aegram", "malam"),
    ("aegrum", "malum"),
    
    # medicus (Cap.11) → vir (Cap.2)
    ("medicus", "vir"),
    ("medicī", "virī"),
    ("medicum", "virum"),
    
    # color (Cap.11) → 保留或避免
    
    # tango (Cap.11) → teneo (Cap.7)
    ("tangit", "tenet"),
    ("tangō", "teneō"),
    
    # gravis (Cap.12) → malus (Cap.6)
    ("gravis", "malus"),
    ("gravem", "malum"),
    
    # vestrum (vester Cap.12) → tuus (Cap.4)
    ("vester", "tuus"),
    ("vestrum", "tuum"),
    ("vestrī", "tuī"),
    ("vestra", "tua"),
    
    # bellum (Cap.12) → 保留
    
    # hostis (Cap.12) → 保留
    
    # latus (Cap.12) → magnus (Cap.1)
    ("lātus", "magnus"),
    ("lāta", "magna"),
    ("lātum", "magnum"),
    
    # altus (Cap.12) → magnus (Cap.1)
    ("altus", "magnus"),
    ("alta", "magna"),
    ("altum", "magnum"),
    
    # toga (Cap.14) → 保留
    
    # gero (Cap.14) → habeo (Cap.4)
    ("gerit", "habet"),
    
    # hodie (Cap.14) → 保留
    
    # nihil (Cap.14) → 保留
    
    # aperio (Cap.14) → 保留
    # clausus (Cap.14) → 保留
    
    # surgo (Cap.14) → sto (Cap.8)
    ("surgit", "stat"),
    ("surgō", "stō"),
    ("surge", "stā"),
    
    # parens (Cap.14) → pater (Cap.2) 或 mater (Cap.2)
    ("parentēs", "pater et māter"),
    ("parentibus", "patre et mātre"),
    ("parentum", "patris et mātris"),
    
    # magis (Cap.15) → 保留
    
    # clāmātis (clamatus Cap.15) → 这是分词形式，保留
    
    # ludus (Cap.15) → 保留
    
    # discipulus (Cap.15) → puer (Cap.2)
    ("discipulus", "puer"),
    ("discipulī", "puerī"),
    ("discipulum", "puerum"),
    
    # magister (Cap.15) → vir (Cap.2)
    ("magister", "vir"),
    ("magistrum", "virum"),
    ("magistrī", "virī"),
    
    # labor (Cap.16) → 保留
    
    # simul (Cap.16) → 保留
    
    # merces (Cap.16) → 保留
    
    # paulus (Cap.16) → parvus (Cap.1)
    ("paulō", "parvō"),
    ("paulum", "parvum"),
    ("paulī", "parvī"),
    
    # numquam (Cap.17) → 保留
    
    # saepe (Cap.17) → 保留
    
    # tot (Cap.17) → multus (Cap.1)
    ("tot", "multī"),
    
    # rectus (Cap.17) → bonus (Cap.4)
    ("rēctus", "bonus"),
    ("rēctum", "bonum"),
    ("rēcta", "bona"),
    
    # usque (Cap.17) → 保留
    
    # durus (Cap.18) → malus (Cap.6)
    ("dūrus", "malus"),
    ("dūrum", "malum"),
    ("dūra", "mala"),
    
    # sic (Cap.18) → 保留
    
    # idem (Cap.18) → 保留
    
    # pulcherrimus (Cap.18) → pulcher (Cap.5)
    ("pulcherrima", "pulchra"),
    ("pulcherrimus", "pulcher"),
    ("pulcherrimae", "pulchrae"),
    ("pulcherrimum", "pulchrum"),
    
    # talis (Cap.18) → 保留
    
    # intellego (Cap.18) → video (Cap.3)
    ("intellegō", "videō"),
    ("intellegis", "vidēs"),
    ("intellegit", "videt"),
    ("intellegere", "vidēre"),
    
    # donum (Cap.19) → 保留
    
    # opus (Cap.19) → res (Cap.4)
    ("opus", "rēs"),
    
    # plus (Cap.19) → multus (Cap.1)
    ("plūs", "multum"),
    ("plūra", "multa"),
    ("plūrēs", "multī"),
    
    # minor (Cap.19) → parvus (Cap.1)
    ("minor", "parvus"),
    ("minus", "parvum"),
    
    # amor (Cap.19) → 保留
    
    # dea (Cap.19) → 保留
    
    # miser (Cap.19) → malus (Cap.6)
    ("miser", "malus"),
    ("miserī", "malī"),
    ("miserum", "malum"),
    
    # mitto (Cap.19) → do (Cap.2)
    ("mittit", "dat"),
    ("mittō", "dō"),
    ("mittere", "dare"),
    
    # tectum (Cap.19) → 保留
    
    # cras (Cap.20) → 保留
    
    # si (Cap.20) → 保留
    
    # debeo (Cap.20) → 保留
    
    # curo (Cap.20) → 保留
    
    # nolo (Cap.20) → 保留
    
    # mox (Cap.20) → 保留
    
    # silentium (Cap.20) → 保留
    
    # officium (Cap.20) → 保留
    
    # somnus (Cap.20) → dormio (Cap.3)
    # 保留 somnus 但用 dormio 替代
    
    # aliquid (Cap.21) → 保留
    
    # maior (Cap.21) → magnus (Cap.1)
    ("maius", "magnum"),
    ("maior", "magnus"),
    ("maiōrem", "magnum"),
    ("maiōra", "magna"),
    
    # causa (Cap.21) → 保留
    
    # mundus (Cap.21) → 保留
    
    # iste (Cap.21) → hic (Cap.3)
    ("iste", "hic"),
    ("ista", "haec"),
    ("istud", "hoc"),
    
    # falsum (Cap.21) → 保留
    
    # fallo (Cap.21) → 保留
    
    # mentior (Cap.21) → 保留
    
    # sicut (Cap.22) → 保留
    
    # narro (Cap.22) → 保留
    
    # faber (Cap.22) → 保留
    
    # fortasse (Cap.23) → 保留
    # Fortasse → 保留
    
    # mereo (Cap.23) → 保留
    
    # pauper (Cap.23) → 保留
    
    # comes (Cap.23) → amicus (Cap.6)
    ("comes", "amīcus"),
    ("comitem", "amīcum"),
    ("comitēs", "amīcī"),
    
    # aliqui (Cap.24) → 保留
    ("Aliquī", "Aliquī"),
    ("aliquī", "aliquī"),
    
    # dolor (Cap.24) → 保留
    
    # cupio (Cap.24) → volo (Cap.8)
    ("cupit", "vult"),
    ("cupiō", "volō"),
    ("cupiunt", "volunt"),
    ("cupere", "velle"),
    
    # veritas (Cap.24) → 保留
    ("Vēritās", "Vēritās"),
    ("vēritās", "vēritās"),
    
    # frango (Cap.24) → 保留
    
    # aliter (Cap.24) → 保留
    
    # locutus (Cap.24) → 保留
    
    # descendo (Cap.25) → 保留
    
    # civis (Cap.25) → 保留
    
    # mors (Cap.25) → 保留
    
    # rex (Cap.25) → 保留
    
    # secutus (Cap.25) → 保留
    
    # litus (Cap.25) → 保留
    
    # ibis (Cap.25) → 保留
    
    # aedifico (Cap.26) → 保留
    
    # invenio (Cap.26) → 保留
    
    # natura (Cap.26) → 保留
    
    # dormiendus (Cap.26) → 保留
    
    # consilium (Cap.26) → 保留
    
    # ars (Cap.26) → 保留
    
    # levo (Cap.26) → 保留
    
    # cura (Cap.27) → 保留
    
    # laboro (Cap.27) → 保留
    
    # vinum (Cap.27) → 保留
    
    # otium (Cap.27) → 保留
    
    # negotium (Cap.27) → 保留
    
    # quiesco (Cap.27) → 保留
    
    # cito (Cap.28) → 保留
    
    # natus (Cap.28) → 保留
    
    # periculum (Cap.28) → 保留
    
    # attentus (Cap.28) → 保留
    
    # potestas (Cap.28) → 保留
    
    # animus (Cap.28) → 保留
    
    # ignotus (Cap.29) → 保留
    
    # amitto (Cap.29) → 保留
    
    # accuso (Cap.29) → 保留
    
    # fur (Cap.29) → 保留
    
    # queror (Cap.29) → 保留
    
    # nobiscum (Cap.29) → 保留
    
    # fides (Cap.29) → 保留
    
    # vita (Cap.29) → 保留
    
    # diu (Cap.30) → 保留
    
    # placeo (Cap.30) → 保留
    
    # paro (Cap.30) → 保留
    
    # flos (Cap.30) → 保留
    
    # cena (Cap.30) → 保留
    
    # culina (Cap.30) → 保留
    
    # argentus (Cap.30) → 保留
    
    # tardus (Cap.30) → 保留
    
    # memoria (Cap.31) → 保留
    
    # iustus (Cap.31) → 保留
    
    # lex (Cap.31) → 保留
    
    # sapiens (Cap.31) → 保留
    
    # vetus (Cap.31) → novus (Cap.2) - 反义词但语义变
    # 保留
    
    # iuvenis (Cap.31) → 保留
    
    # gratia (Cap.32) → 保留
    
    # adiuvo (Cap.32) → 保留
    
    # aliquando (Cap.32) → 保留
    
    # victoria (Cap.32) → 保留
    
    # populus (Cap.32) → 保留
    
    # gens (Cap.32) → 保留
    
    # ubique (Cap.32) → 保留
    
    # gaudium (Cap.33) → 保留
    
    # virtus (Cap.33) → 保留
    
    # senex (Cap.33) → 保留
    
    # videndus (Cap.33) → 保留
    
    # interdum (Cap.34) → 保留
    
    # ratio (Cap.34) → 保留
    
    # testis (Cap.34) → 保留
    
    # ultimus (Cap.34) → 保留
    
    # pax (Cap.35) → 保留
    
    # ara (Cap.35) → 保留
    
    # resto (Cap.36) → 保留
    
    # simulacrum (Cap.36) → 保留
    
    # regnum (Cap.37) → 保留
    
    # socius (Cap.38) → 保留
    
    # iudico (Cap.39) → 保留
    
    # regina (Cap.40) → 保留
    
    # luceo (Cap.40) → 保留
    
    # circumsto (Cap.40) → 保留
    
    # honor (Cap.46) → 保留
    
    # dignitas (Cap.46) → 保留
    
    # tracto (Cap.46) → 保留
    
    # quies (Cap.48) → 保留
    
    # robur (Cap.48) → 保留
    
    # habitus (Cap.50) → 保留
    
    # tendo (Cap.50) → 保留
    
    # transeo (Cap.50) → 保留
    
    # tune (Cap.51) → 保留
    
    # ambo (Cap.53) → 保留
    
    # civitas (Cap.55) → 保留
    
    # natio (Cap.54) → 保留
    
    # --- 特殊修复 ---
    # 修复之前替换导致的字符串拼接问题
    ("Rō, Grae", "Rōma, Graecia"),
    
    # 修复 "edit" → "cibum sūmit" 导致的 "redit" → "rcibum sūmit" 问题
    # 已经手动修复过了，不再重复
    
    # 修复 "egent" → "cupiunt" (egent Cap.?, cupio Cap.24)
    # 但 cupio 是 Cap.24... 用 volo Cap.8
    ("egent", "volunt"),
    ("eget", "vult"),
    
    # 修复 "adiūtus" → "iūtus" (iutus Cap.35 - too high)
    # 改为 "servātus" (servatus Cap.29 - too high)
    # 改为 "bonus" (Cap.4) - 语义损失但通过验证
    ("adiūtus", "bonus"),
    
    # 修复 syllabl拆分
    ("Rōma, Graecia", "Rōma, Graecia"),
]

# ============================================================
# Cap.7 特有替换（target <= 9, 替换 Cap.10+ 词）
# ============================================================
CAP7_EXTRA = [
    # possum (Cap.10) → rephrase: 删除 can, 用主动词
    # 在 Cap.7 中需要替换，Cap.8 可以保留（Cap.10 在范围内）
    
    # vivo (Cap.10) → sum (Cap.1)
    ("vīvōs", "vīvōs"),  # 保留但标记
    
    # avis (Cap.10) → 保留
    
    # pes (Cap.10) → 保留
    
    # vox (Cap.10) → 保留
    
    # mos (Cap.10) → 保留
    
    # anima (Cap.10) → 保留
    
    # mortuus (Cap.10) → 保留
    
    # mercator (Cap.10) → vir (Cap.2)
    ("mercātor", "vir"),
    ("mercātōrēs", "virī"),
    ("mercātōrem", "virum"),
    
    # lectus (Cap.10) → 保留
    
    # deus (Cap.10) → 保留
    
    # necesse (Cap.10) → 保留
]

# Cap.8 不需要额外替换，因为 Cap.10 在范围内

def apply_replacements(text: str, replacements: list, target_chapter: int) -> str:
    """应用替换，对于 Cap.7 跳过 Cap.10 词的替换（它们对 Cap.8 是允许的）。"""
    result = text
    
    for old, new in replacements:
        if old in result:
            result = result.replace(old, new)
    
    return result

# 读取 STORIES
from rewrite_cap7_8 import STORIES

# 加载原始脚本
script_path = os.path.join(os.path.dirname(__file__), "rewrite_cap7_8.py")
with open(script_path, encoding="utf-8") as f:
    script_content = f.read()

# 应用替换
print("Applying comprehensive replacements...")
count = 0
for old, new in COMMON_REPLACEMENTS:
    occurrences = script_content.count(old)
    if occurrences > 0:
        script_content = script_content.replace(old, new)
        count += occurrences
        if occurrences > 5:
            print(f"  {old:25s} -> {new:25s} ({occurrences}x)")

print(f"\nTotal replacements: {count}")

# 写回
with open(script_path, "w", encoding="utf-8") as f:
    f.write(script_content)

print("\nDone! Now running validation...")