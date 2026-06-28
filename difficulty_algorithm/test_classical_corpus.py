#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用古典拉丁语 + 配套读物盲测归一化版算法 v1_2_0
"""

import json
import evaluate_difficulty as ed
from pathlib import Path

# 加载双映射表
base = Path(__file__).parent
with open(base / 'word_chapter_map.json') as f:
    exact_map = json.load(f)
with open(base / 'word_chapter_map_normalized.json') as f:
    norm_map = json.load(f)

# ============================================================
# 语料：古典原典 + LLPSI 配套读物
# ============================================================

PASSAGES = {
    # --- 古典原典 ---
    "Caesar - BG I.1": """
Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae,
aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur.
Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab
Aquitani Garumna flumen, a Belgis Matrona et Sequana dividit. Horum
omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate
provinciae longissime absunt, minimeque ad eos mercatores saepe commeant
atque ea quae ad effeminandos animos important inferunt, proximique
sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum
gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt,
quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis
finibus eos prohibent aut ipsi in eorum finibus bellum gerunt.
""",

    "Cicero - In Catilinam I (开头)": """
Quo usque tandem abutere, Catilina, patientia nostra? Quam diu etiam
furor iste tuus nos eludet? Quem ad finem sese effrenata iactabit
audacia? Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae,
nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus
habendi senatus locus, nihil horum ora voltusque moverunt?
""",

    "Catullus - Carmen 5": """
Vivamus, mea Lesbia, atque amemus,
rumoresque senum severiorum
omnes unius aestimemus assis.
Soles occidere et redire possunt:
nobis cum semel occidit brevis lux,
nox est perpetua una dormienda.
Da mi basia mille, deinde centum,
dein mille altera, dein secunda centum,
deinde usque altera mille, deinde centum.
Dein, cum milia multa fecerimus,
conturbabimus illa, ne sciamus,
aut ne quis malus invidere possit,
cum tantum sciat esse basiorum.
""",

    "Vergilius - Aeneis I.1": """
Arma virumque cano, Troiae qui primus ab oris
Italiam, fato profugus, Laviniaque venit
litora, multum ille et terris iactatus et alto
vi superum saevae memorem Iunonis ob iram;
multa quoque et bello passus, dum conderet urbem,
inferretque deos Latio, genus unde Latinum,
Albanique patres, atque altae moenia Romae.
Musa, mihi causas memora, quo numine laeso,
quidue dolens, regina deum tot volvere casus
insignem pietate virum, tot adire labores
impulerit.
""",

    "Ovidius - Metamorphoses I.1": """
In nova fert animus mutatas dicere formas
corpora; di, coeptis (nam vos mutastis et illas)
adspirate meis primaque ab origine mundi
ad mea perpetuum deducite tempora carmen.
Ante mare et terras et quod tegit omnia caelum
unus erat toto naturae vultus in orbe,
quem dixere Chaos: rudis indigestaque moles
nec quicquam nisi pondus iners, congestaque eodem
non bene iunctarum discordia semina rerum.
""",

    "Sallustius - Bellum Catilinae 1": """
Omnis homines, qui sese student praestare ceteris animalibus, summa
ope niti decet ne vitam silentio transeant veluti pecora, quae natura
prona atque ventri oboedientia finxit. Sed nostra omnis vis in anima
et corpore sita est; animi imperio vero, corporis servitio magis utimur;
alterum nobis cum dis, alterum cum beluis commune est.
""",

    # --- LLPSI 配套读物 Fabulae Faciles ---
    "FF - Prometheus (基础)": """Prometheus autem, qui prior, quamquam graviter offensus, tamen legem Iovis ferendam censuit. Sed postquam Prometheus a Iove in Caucasum montem religatus est, Epimetheus, fratris monitu oblitus, uxorem duxit Pandoram, quae primam feminam Iuppiter finxerat. Pandora autem animum Iunonis referens, quod Iuppiter eam ad perniciem mortalium finxerat, vasculum quoddam in omnium conspectu aperuit, unde morbi et senectus in mundum effusa sunt; sola spes in fundo vasculi mansit.""",

    "FF - Hercules (中等)": """Hercules, Alcmenae filius, qui Iove patre natus virtute multos superabat, ab Apoline doctus, multorumque bonorum compos, ab Eunomio praeceptore suo cantu fidibusque eruditus, Thebas profectus, Thebano regi Creonti opem tulit. Ab eo Megaram, Creontis filiam, in matrimonium accepit, ex qua liberos sustulit. Sed Hercules postea, Iunonis impulsu, insania percitus, in liberos suos temere grassatus, uxorem interfecit, ipsum se telo voluit excutere, sed ab Amphytrione retentus est.""",
}


def run():
    print("=" * 70)
    print("  古典语料 + 配套读物盲测 — 归一化覆盖阈值法 v1_2_0")
    print("=" * 70)

    header = (f"{'语料':<42s} | {'词形':>4} | {'精收':>4} | {'归收':>4} | "
              f"{'率%':>4} | {'80%':>4} | {'85%':>4} | {'90%':>4} | {'95%':>4} | 难度")
    print(f"\n{header}")
    print("-" * len(header))

    for name, text in PASSAGES.items():
        tokens = ed.tokenize_text(text)
        result = ed.evaluate_text_coverage(tokens, exact_map, norm_map)

        def s(val, w=4):
            if val is None:
                return "   —"
            return f"{val:>{w}d}"

        diff = ""
        if result.get('difficulty_degraded'):
            diff = f"降级({result['difficulty'] or 'N/A'})"
        elif result['difficulty'] is not None:
            diff = str(result['difficulty'])
        else:
            diff = "N/A"

        print(f"  {name:<40s} | {result['total_types']:4d} | "
              f"{result['found_types_exact']:4d} | {result['found_types_normalized']:4d} | "
              f"{result['llpsi_coverage']:3.0f}% | "
              f"{s(result['threshold_80'])} | {s(result['threshold_85'])} | "
              f"{s(result['threshold_90'])} | {s(result['threshold_95'])} | {diff}")

    print()
    print("=" * 70)
    print("  各语料详情")
    print("=" * 70)
    for name, text in PASSAGES.items():
        tokens = ed.tokenize_text(text)
        result = ed.evaluate_text_coverage(tokens, exact_map, norm_map)
        print(ed.format_external_result(name, result))
        print()

    # --- 对比 v1.1 vs v1.2 的收录率提升 ---
    print()
    print("=" * 70)
    print("  v1.1 (纯精确) vs v1.2 (精确+归一化) 收录率对比")
    print("=" * 70)
    print(f"  {'语料':<42s} | {'v1.1%':>5} | {'v1.2%':>5} | {'提升':>5}")
    print("  " + "-" * 60)
    for name, text in PASSAGES.items():
        tokens = ed.tokenize_text(text)
        r_old = ed.evaluate_text_coverage(tokens, exact_map, {})  # 纯精确
        r_new = ed.evaluate_text_coverage(tokens, exact_map, norm_map)
        improvement = r_new['llpsi_coverage'] - r_old['llpsi_coverage']
        print(f"  {name:<40s} | {r_old['llpsi_coverage']:4.1f}% | "
              f"{r_new['llpsi_coverage']:4.1f}% | {'+' if improvement > 0 else ''}{improvement:.1f}%")


if __name__ == '__main__':
    run()
