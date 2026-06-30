#!/usr/bin/env python3
"""fix_cap10.py — 修复25个失败的Cap.10故事，只使用通过故事验证过的安全词汇。"""
import json, re, sys, os
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

# 从8个通过的故事中提取的安全词汇
# 这些词已经验证simplemma能正确还原到Cap.1-12

FIXES = {}

# ============================================================
# cap10_03: Quid Est Iustitia (v2=17 → target ≤12)
# 原问题: iustitia OOV, punit→?, 以及其他高章节词
# 策略: 重写为父子对话，关于"对与错"，用安全词汇
# ============================================================
FIXES["cap10_03"] = (
    "Puer ad patrem venit. Puer: 'Pater, quid est bonum?' "
    "Pater tacet. Pater puerum spectat. "
    "Pater: 'Veni, fili. Quid vides per fenestram?' "
    "Puer: 'Oppidum video. Viros video. Feminas video.' "
    "Pater: 'Quid viri faciunt?' "
    "Puer: 'Alii ambulant. Alii sedent. Alii laborant.' "
    "Pater: 'Bene. Nunc audi. Si vir panem habet et panem amico dat, hoc est bonum. "
    "Si vir panem amici capit, hoc est malum.' "
    "Puer: 'Bonum est dare. Malum est capere.' "
    "Pater: 'Ita, fili. Bonum est aliis dare. Malum est aliis nocere.' "
    "Puer: 'Sed pater, cur viri mali sunt?' "
    "Pater: 'Non omnes viri mali sunt. Multi viri boni sunt. "
    "Sed aliqui viri solum de se cogitant.' "
    "Puer: 'Et servi? Servi sunt boni an mali?' "
    "Pater: 'Servi quoque boni et mali sunt — sicut domini. "
    "Homo bonus est qui alios iuvat. Homo malus est qui alios laedit.' "
    "Puer: 'Pater, ego bonus esse volo.' "
    "Pater: 'Tum, fili, semper alios iuva. "
    "Si panem habes, da ei qui non habet. "
    "Si amicus tuus est tristis, eum iuva.' "
    "Puer: 'Faciam, pater. Ego bonus puer ero.' "
    "Pater filium tangit. Pater: 'Tu es bonus puer, fili. "
    "Et pater tuus te amat.' "
    "Puer ad fenestram it. Puer viros et feminas in oppido videt. "
    "Puer: 'Mundus est magnus. Sed ego parvus sum. "
    "Potestne puer parvus mundum iuvare?' "
    "Pater: 'Omnis magnus vir fuit puer parvus. "
    "Incipe cum parvo. Da amico tuo panem. Da matri tuae rosam. "
    "Da patri tuo laetitiam. Et mundus erit melior.' "
    "Puer ridet. Puer laetus est. "
    "Et puer scit: bonum in corde incipit."
)

# ============================================================
# cap10_04: Finis Viae (v2=13 → target ≤12)
# 原问题: finita→?, requiem→?
# 策略: 重写为旅程故事，用安全词汇
# ============================================================
FIXES["cap10_04"] = (
    "Vir in via ambulat. Via est longa. Via est pulchra. "
    "Vir a Graecia ad Romam it. Vir multos dies ambulat. "
    "Vir multas terras videt. Vir multa oppida videt. "
    "In Graecia, vir iuvenis fuit. "
    "In Graecia, vir familiam habuit. "
    "Sed vir Romam videre voluit. "
    "Vir de Roma multa audivit. "
    "Roma est caput mundi. Roma est maxima. "
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
    "Sed via mea hic manet.' "
    "Vir oculos claudit. Vir non iam sentit. "
    "Via viri hic est. Sed Roma manet. "
    "Alii viri ad Romam veniunt. "
    "Aliae viae incipiunt. Aliae viae manent. "
    "Una via hic est — alia via ibi est. "
    "Et vir, in terra, in pace iacet."
)

# ============================================================
# cap10_05: Somnum Aeternum (v2=20)
# 原问题: requiem→?, aequos→?, dura→? 很多高章节词
# 策略: 重写为简单的睡眠故事
# ============================================================
FIXES["cap10_05"] = (
    "Nox est. Caelum est nigrum. Stellae in caelo sunt. "
    "Luna in caelo est. Luna est pulchra. "
    "In oppido, homines dormiunt. "
    "Puer in lecto est. Puer oculos claudit. Puer dormit. "
    "Mater puerum spectat. Mater laeta est. "
    "Pater in lecto est. Pater fessus est. Pater dormit. "
    "Servus in casa parva est. Servus in lecto dormit. "
    "Canis prope ianuam dormit. Canis fessus est. "
    "Avis in arbore dormit. Avis caput sub ala ponit. "
    "In silva, lupus non dormit. Lupus ambulat. "
    "Lupus cibum quaerit. Sed lupus solus est. "
    "In mari, pisces non dormiunt. Pisces in aqua natant. "
    "Mare est magnum. Mare est altum. "
    "In villa, dominus non dormit. Dominus in cubiculo est. "
    "Dominus de multis rebus cogitat. "
    "Dominus de pecunia cogitat. Dominus de servis cogitat. "
    "Sed dominus dormire non potest. "
    "Cur dominus dormire non potest? "
    "Quia dominus multum cogitat. "
    "Servus in casa dormit. Dominus in villa non dormit. "
    "Servus nihil habet — sed dormit bene. "
    "Dominus multa habet — sed dormire non potest. "
    "Quid est melius: multa habere et non dormire, "
    "an parva habere et bene dormire? "
    "Nox est. Homines dormiunt. "
    "Et sol, in caelo, surgit. Novus dies venit. "
    "Homines surgunt. Homines ambulant. Homines laborant. "
    "Sed nox redit. Et iterum homines dormiunt. "
    "Somnus est bonus. Somnus homines iuvat. "
    "Sine somno, homo non est bonus. "
    "Cum somno, homo est laetus et fortis."
)

# ============================================================
# cap10_06: Quattuor terrae (v2=16)
# 原问题: Germania, Germani → OOV，但其他词也映射到高章节
# 策略: 只用安全地名（Roma, Italia, Graecia, Hispania, Gallia, Sicilia, Sardinia, Corsica）
# ============================================================
FIXES["cap10_06"] = (
    "Italia est in medio. Graecia est ad orientem. "
    "Hispania est ad occidentem. Gallia est ad septentrionem. "
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
    "Gallia est ad septentrionem. Gallia est terra magna. "
    "Romani in Galliam venerunt. "
    "Gallia est Romana. "
    "In Gallia, multi montes sunt. "
    "In Gallia, multae silvae sunt. "
    "Galli sunt fortes. Galli sunt feri. "
    "Gallia est terra libera. Gallia est terra magna. "
    "Quattuor terrae — quattuor res. "
    "Italia est patria. Graecia est magistra. "
    "Hispania est pulchra. Gallia est libera. "
    "Imperium Romanum est magnum. "
    "Sed non omnes terrae sunt Romanae. "
    "Et hoc est bonum. Mundus est magnus. "
    "Et in mundo, multae terrae sunt."
)

# ============================================================
# cap10_08: Flumina Romana (v2=14)
# 原问题: Germania, custodiunt, Germani, Danuvius, Nilus, Aegypto, etc. → OOV
# 策略: 只用安全河流名（Tiberis, Rhenus）+ 简单词汇
# ============================================================
FIXES["cap10_08"] = (
    "Tiberis est in Italia. Tiberis est fluvius Romanus. "
    "Tiberis per Romam fluit. Roma ad Tiberim est. "
    "Tiberis aquam Romae dat. Tiberis naves portat. "
    "Tiberis est pater Romae. "
    "Sine Tiberi, Roma non est. "
    "Rhenus est in Gallia. Rhenus est fluvius magnus. "
    "Rhenus est limes imperii. "
    "Rhenus Galliam ab imperio dividit. "
    "Romani ad Rhenum stant. Romani Rhenum spectant. "
    "Trans Rhenum, terra libera est. "
    "Rhenus est porta. Rhenus est murus. "
    "Tiberis et Rhenus sunt duo flumina magna. "
    "Tiberis est in Italia. Rhenus est in Gallia. "
    "Tiberis Romae aquam dat. "
    "Rhenus imperium defendit. "
    "Duo flumina — duae res. "
    "Tiberis est pater Romae. "
    "Rhenus est murus imperii. "
    "Flumina sunt magnae viae aquae. "
    "Flumina terras dividunt. "
    "Flumina terras coniungunt. "
    "Flumina semper fluunt. "
    "Ab montibus ad mare — flumina currunt. "
    "Et Romani flumina amant."
)

# ============================================================
# cap10_09: Duodecim insulae (v2=13)
# 原问题: Creta, Euboea, Naxus → OOV (太多OOV)
# 策略: 只用安全岛名（Sicilia, Sardinia, Corsica, Rhodos, Britannia, Hibernia）
# ============================================================
FIXES["cap10_09"] = (
    "Multae insulae in mari sunt. "
    "Omnes insulae sunt pulchrae. Omnes insulae sunt notae. "
    "Sicilia est insula magna. Sicilia est prope Italiam. "
    "In Sicilia, multi montes sunt. "
    "In Sicilia, multae arbores sunt. "
    "Sicilia est terra bona. "
    "Sardinia est insula. Sardinia est in mari. "
    "Sardinia est prope Corsicam. "
    "Corsica est insula parva. Corsica est prope Sardiniam. "
    "Corsica est pulchra. In Corsica, multi montes sunt. "
    "Rhodos est insula. Rhodos est in Graecia. "
    "Rhodos est pulchra. In Rhodo, multi flores sunt. "
    "Britannia est insula magna. Britannia est in Oceano. "
    "In Britannia, multi montes sunt. "
    "In Britannia, multae silvae sunt. "
    "Hibernia est insula parva. Hibernia est prope Britanniam. "
    "Hibernia est terra viridis. "
    "In Hibernia, multae herbae sunt. "
    "Omnes insulae sunt in imperio. "
    "Omnes sunt Romanae — vel una non est. "
    "Nautae ad has insulas navigant. "
    "Mercatores ad has insulas eunt. "
    "Multae insulae — multae portae ad mare. "
    "Et omnes sunt pulchrae. Et omnes sunt bonae."
)

# ============================================================
# cap10_10: Quattuor maria (v2=14)
# 原问题: Nilus, Aegyptus 等 → OOV
# 策略: 只用安全水体名（Mare Nostrum, Oceanus, Tiberis）+ 简单词汇
# ============================================================
FIXES["cap10_10"] = (
    "Quattuor aquae sunt. "
    "Mare Nostrum est primum. Oceanus est secundus. "
    "Tiberis est tertius. Rhenus est quartus. "
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
    "Rhenus est in Gallia. Rhenus est fluvius magnus. "
    "Rhenus Galliam tangit. Rhenus aquam dat. "
    "Rhenus est limes imperii. "
    "Rhenus terras bonas facit. "
    "Quattuor aquae — quattuor res. "
    "Mare Nostrum est imperium. "
    "Oceanus est finis. "
    "Tiberis est patria. "
    "Rhenus est murus. "
    "Et omnes aquae sunt bonae."
)

# ============================================================
# cap10_12: In foro (v2=14)
# 原问题: forum→19, templum→19, statuae→?
# 策略: 完全避免forum/templum/statuae，用via/taberna等替代
# ============================================================
FIXES["cap10_12"] = (
    "In via multi homines sunt. "
    "Via est magna. Via est pulchra. "
    "In via, multae tabernae sunt. "
    "In tabernis, multae res sunt. "
    "Mercatores in via sunt. Mercatores res vendunt. "
    "Alius mercator panem vendit. "
    "Panis est bonus. Panis est novus. "
    "Alius mercator vinum vendit. "
    "Alius mercator vestes vendit. "
    "Vestes sunt pulchrae. "
    "Alius mercator libros vendit. "
    "Libri sunt antiqui. "
    "Vir ad viam venit. Vir panem emit. "
    "Vir pecuniam numerat. Vir mercatori pecuniam dat. "
    "Femina ad viam venit. Femina vestes emit. "
    "Femina vestem pulchram videt. "
    "Femina vestem tangit. "
    "Femina: 'Haec vestis est pulchra. "
    "Quanti haec vestis est?' "
    "Mercator: 'Haec vestis decem nummos constat.' "
    "Femina pecuniam dat. Femina vestem accipit. "
    "Puer ad viam venit. Puer libros videt. "
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
    "In via, multi clamores sunt. "
    "Mercatores clamant. Homines loquuntur. "
    "Servi currunt. Canes in via sunt. "
    "Via est cor oppidi. "
    "In via, vita est."
)

# ============================================================
# cap10_13: In via (v2=14)
# 原问题: equus→equa OOV, vadis→vado OOV
# 策略: 避免equus和vadis，用其他安全词
# ============================================================
FIXES["cap10_13"] = (
    "In via homo ambulat. Via est longa. "
    "Homo solus est. Homo de vita cogitat. "
    "Canis cum homine ambulat. "
    "Canis est parvus. Canis est niger. "
    "Homo canem amat. Canis hominem amat. "
    "Homo: 'Canis, veni! Curre!' "
    "Canis currit. Canis caudam movet. "
    "Canis laetus est. "
    "Homo et canis per viam ambulant. "
    "Alii homines in via sunt. "
    "Alius homo cum filio est. "
    "Filius est parvus. Filius est laetus. "
    "Homo: 'Salve, amice! Quo is?' "
    "Alius: 'Ad viam eo. Res emere volo.' "
    "Homo: 'Et ego ad viam eo. Ambulemus una!' "
    "Duo homines et canis ad viam eunt. "
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
    "Homo et canis ad viam veniunt. "
    "Via est magna. "
    "Homo: 'Canis, hic est via. "
    "Hic, multae res sunt.' "
    "Canis latrat. Canis caudam movet. "
    "Homo et canis in via sunt. "
    "Et ambo sunt laeti."
)

# ============================================================
# cap10_14: Insula parva (v2=16)
# 原问题: comedit→comedo OOV, 以及一些高章节词
# 策略: 用bibit/consumit等安全词替代
# ============================================================
FIXES["cap10_14"] = (
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
    "Homo in casa cibum consumit. "
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
)

print(f"定义完成 {len(FIXES)} 个修复")
print("FIXES keys:", list(FIXES.keys()))