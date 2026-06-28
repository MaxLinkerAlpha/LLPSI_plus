#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fabulae Syrae 手工采样干净故事文本 + 难度评估
从 PDF 中逐页提取，手工选取正文部分（跳过边注）
"""

import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'difficulty_algorithm'))
import evaluate_difficulty as ed

# ============================================================
# 手工清洗后的 Fabulae Syrae 故事文本
# 来源: 从 PDF 原文去除了边注/词汇注释/页码
# ============================================================

CLEAN_STORIES = [
    {
        "name": "Europa (LLPSI Cap.26)",
        "text": """
Europa bona et pulchra virgo Graeca fuit. Quae, dum cum aliis puellis in campo
ludit, currit, pilam iacit floresque carpendo delectatur, subito magnum et album
taurum vidit. Quem cum primum conspexerunt, amicae eius perterritae fugerunt
clamantes. Taurus autem non saevus esse videbatur: itaque Europa, quae minime
metuebat et taurum propius videndi cupida erat, ad eum accedens manu sua tetigit.
Taurus mugivit; Europa vero herbas ex campo carptas tauro dedit, qui eas edendo
laetabatur. Deinde Europa, audacior facta, latum tauri tergum spectabat atque
manu sua tangebat. Tandem in eius tergum ascendens consedit et, "Amicae, venite
et me spectate!" inquit, "Videte me in tauri tergo sedentem!"
Statim autem taurus, qui humi iacebat, surgens ad maris oram currere coepit.
Europa clamavit perterrita; amicae eius flentes et lacrimantes ad litus ad
adiuvandum cucurrerunt, neque vero Europam, quae tauro vehebatur, consequi
potuerunt: taurus enim, campo relicto, Oceanum petivit atque in magnos maris
fluctus se immisit. Tandem in Cretam insulam pervenit, ubi Iuppiter, qui in
taurum se mutaverat, Europam in uxorem duxit.
"""
    },
    {
        "name": "Tarpeia (LLPSI Cap.26)",
        "text": """
Tarpeia virgo Romana, Tarpei filia, cum patre suo in Capitolio habitabat. Eo
tempore Titus Tatius, rex Sabinorum, bellum Romanis inferebat. Sabini enim, iam
diu irati quod Romani filias eorum rapuerant, Capitolium vi capere volebant. Cum
autem Sabini Tarpeiam vidissent, quae aquam e fonte hauriebat, ad eam accesserunt
et "Si nos in Capitolium clam duxeris, magna tibi praemia dabimus." Tarpeia, quae
praemiorum cupida erat, respondit: "Date mihi quod in sinistris bracchiis geritis,
et viam vobis monstrabo." Sabini autem in sinistris bracchiis armillas aureas
gerebant. Tarpeia igitur eos in Capitolium clam duxit. Cum autem Sabini Capitolium
cepissent, Tarpeia praemia poposcit. Tum Sabini, promissorum memores, non solum
armillas sed etiam scuta, quae in sinistris bracchiis gerebant, in eam iecerunt.
Ita Tarpeia, quae urbem prodiderat, sub multitudine armillarum et scutorum necata
est.
"""
    },
    {
        "name": "Atalanta (LLPSI Cap.28)",
        "text": """
Atalanta virgo pulcherrima et pedibus velocissima erat. Haec cum a patre, qui
filios tantum cupiebat, in silva relicta esset, a cerva nutrita est. Cum autem
adolevisset, multis procis petebatur. Atalanta autem nubere nolebat, nisi ei
vir inveniretur qui se cursu superaret. Ei autem, qui victus esset, mors
proponebatur. Multi iuvenes, formae eius cupidi, certamen susceperunt, sed
omnes ab Atalanta victi et necati sunt. Tandem Hippomenes, Neptuni nepos, auxilio
Veneris usus, tria mala aurea in terram iactavit. Atalanta, quae haec mala vidit,
cupida eorum colligendorum substitit, et ita Hippomenes eam cursu superavit.
Sic Hippomenes Atalantam in matrimonium duxit.
"""
    },
    {
        "name": "Orpheus et Eurydice (LLPSI Cap.29)",
        "text": """
Orpheus poeta clarissimus uxorem pulcherrimam habebat, nomine Eurydicen. Aliquando
cum Eurydice per prata ambularet, ab Aristeo, qui eam amabat, petita est. Eurydice
autem fugiens serpentem in herba latentem non vidit, qui eam monordit. Statim
Eurydice mortua est. Orpheus vero, dolore affectus, uxorem suam etiam apud inferos
quaerere constituit. Descendit igitur ad inferos et ibi cithara sua tam dulciter
cecinit ut Cerberus ipse mitesceret et omnes umbrae tacerent. Plutonem et
Proserpinam his verbis oravit: "O domini inferorum, reddite mihi uxorem meam!
Sinite me eam in lucem reducere." Illi autem, cantu eius commoti, Eurydicen ei
reddiderunt, sed hac condicione: ne, antequam ad superos perveniret, uxorem
aspiceret. Orpheus igitur ad superos ascendit, sed prope exitum, amore victus,
oculos ad uxorem vertit. Statim Eurydice in tenebras relapsa est. Orpheus frustra
uxorem retinere conatus est.
"""
    },
    {
        "name": "Daphne (LLPSI Cap.32)",
        "text": """
Daphne, fluminis Penei filia, virgo pulcherrima erat. Apollo, qui Pythona
serpentem nuper sagittis interfecerat, eam vidit et statim amavit. Daphne autem
nubere nolebat; itaque Apollinem fugiebat. Apollo, cum eam fugientem videret,
celerius cucurrit et prope eam accessit. "Noli fugere, Daphne!" clamavit, "Non
sum hostis tuus: deus sum, Apollo!" Sed Daphne, perterrita, magis magisque
accelerabat. Tandem Daphne ad ripam fluminis Penei pervenit et patrem suum, qui
ibi habitabat, auxilio vocavit: "Fer opem, pater, si flumina numen habetis!
Perde figuram meam, quae nimium placuit!" Vix precem finierat, et eius membra
torpescunt, pectus cingitur tenui libro, capilli in folia crescunt, bracchia in
ramos abeunt. Daphne, quae modo puella erat, arbor facta est, laurus. Apollo
autem, quamquam puellam vivam amiserat, arborem tamen amavit, et, ramis eius
caput cingens, "Laurus" inquit, "eris semper arbor mea!"
"""
    },
    {
        "name": "Baucis et Philemon (LLPSI Cap.29)",
        "text": """
Iuppiter et Mercurius, forma humana sumpta, in terras descenderunt ut hominum
animos probarent. Cum ad mille domos accessissent et nemo eos reciperet, tandem
ad parvam casam pervenerunt, ubi Baucis et Philemon, senes pauperrimi sed
benignissimi, habitabant. Ii senes, cum deos vidissent, eos in casam suam
invitaverunt et, quamquam pauperes erant, omnia quae habebant eis obtulerunt.
Dei autem, cum horum senum pietatem et benignitatem vidissent, eis mercedem dare
constituerunt. Eis dixerunt ut secum in montem ascenderent. Cum senes in montem
ascendissent et respexissent, omnem regionem circum casam aquis opertam viderunt;
sola casa eorum intacta remanserat. Casa autem eorum, dum senes spectant, in
templum mutata est. Tum Iuppiter dixit eis ut unum donum peterent. Baucis et
Philemon hoc unum petiverunt: ut ne alter sine altero viveret aut moreretur.
Voto senum Iuppiter annuit. Itaque Baucis et Philemon, cum ad summam senectutem
pervenissent, in arbores mutati sunt: Baucis in tiliam, Philemon in quercum;
arborum rami simul crescebant et ventos una ferebant.
"""
    },
]

def main():
    base = Path(__file__).parent / 'difficulty_algorithm'
    with open(base / 'word_chapter_map.json', encoding='utf-8') as f:
        exact_map = json.load(f)
    with open(base / 'word_chapter_map_normalized.json', encoding='utf-8') as f:
        norm_map = json.load(f)

    print("=" * 80)
    print("  Fabulae Syrae 手工采样干净文本 — 难度评级 (v1_2_0)")
    print("=" * 80)
    
    header = (f"{'故事名':<37s} | {'词形':>5s} | {'收录率':>5s} | "
              f"{'80%':>4s} | {'85%':>4s} | {'90%':>4s} | {'难度':>4s}")
    print(f"\n{header}")
    print("-" * len(header))
    
    for s in CLEAN_STORIES:
        tokens = ed.tokenize_text(s['text'])
        result = ed.evaluate_text_coverage(tokens, exact_map, norm_map)
        
        t80 = str(result['threshold_80'] or '—')
        t85 = str(result['threshold_85'] or '—')
        t90 = str(result['threshold_90'] or '—')
        
        if result['difficulty'] is not None and not result.get('difficulty_degraded'):
            diff = str(result['difficulty'])
            note = ""
        elif result.get('difficulty_degraded') and result['difficulty']:
            diff = f"{result['difficulty']}*"
            note = f" (最高{result['max_achievable']:.0f}%)"
        else:
            diff = "—"
            note = ""
        
        print(f"  {s['name']:<35s} | {result['total_types']:5d} | "
              f"{result['llpsi_coverage']:4.1f}% | {t80:>4s} | {t85:>4s} | "
              f"{t90:>4s} | {diff:>4s}{note}")
    
    print()
    print("=" * 80)
    print("  解读:")
    print("   - Fabulae Syrae 是 LLPSI 的官方配套读物，面向 Cap.26 起的学习者")
    print("   - 它用已学词汇叙事，理论上新词率很低")
    print("   - 如果算法对 FF 收录率仍然 < 80%，说明拉丁语词形爆炸是根本瓶颈")
    print("=" * 80)

if __name__ == '__main__':
    main()
