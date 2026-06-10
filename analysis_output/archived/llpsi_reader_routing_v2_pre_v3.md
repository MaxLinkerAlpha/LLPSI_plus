# LLPSI 56 章扩展读物路由表 (v2 段级版)

**生成日期**: 2026-06-09 | **覆盖**: FR Cap.1-35 + RA Cap.36-56

## 算法 (v2 极简段级)

- **段级切片**: 按空行切分文本为段落
- **叙事过滤**: 拉语词占比≥50%、非标题/非练习题/非词汇表
- **极简评分 (hybrid)**:
  - `full = 1.0`: 在 LLPSI Cap.N 已学词集 `learned_words[N]` 中
  - `partial = 0.5`: 在 LLPSI 56章总词表但未学到
  - `character = 0.3`: 在本段所属书的高频专名(出现≥5次)
  - `score = (full + 0.5*partial + 0.3*character) / total_latin_tokens`
- **已学词集**: 直接扫描 LLPSI OCR 文本重建（而非依赖DB is_new标记）

## 路由规范 (4个维度)

| 标签 | 含义 | 阈值 |
|------|------|------|
| 📖 流畅 | 学完本章后该段可流畅阅读 | hybrid ≥ 80% |
| 💪 挑战 | 学完本章后该段可挑战阅读 | hybrid ≥ 70% |
| 📚 节选 | 学完本章后该段可节选阅读 | hybrid ≥ 50% |
| 🧩 D段  | D类拉语段 (OCR抽取) | form ≥ 60% |

## Cap.1 (FR Cap.I)

**数据**: 新词 204 / 累计 204 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #20 (tokens=72): `In imperio Romano multae sunt provinciae. Hispania et Gallia sunt provinciae Rom`
- **Via Latina: De Lingua et Vita Romanorum** #105 (tokens=71): `Villa magna est                    Campus magnus est               Oppidum magnu`
- **Fabellae Latinae** #21 (tokens=58): `Quid est Brundisium? Brundisium oppidum est. Quid est Dànuvius? Dànuvius est flu`
- **Via Latina: De Lingua et Vita Romanorum** #32 (tokens=29): `In Európà sunt multa oppida. Alba Longa in Ita- lia est: Alba Longa oppidum Ital`
- **Fabellae Latinae** #22 (tokens=25): `INSVLA et OPPIDVM vocabula Latina sunt. In vocabulo INSVLA sunt sex litterae: li`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: De Lingua et Vita Romanorum** #1603 (tokens=87): `máteria -ae f^ 10[III].97 mátrimónium -i 7 2[II].74 mátróna -ae f^ 7(II].43 maxi`
- **Fabellae Latinae** #20 (tokens=72): `In imperio Romano multae sunt provinciae. Hispania et Gallia sunt provinciae Rom`
- **Via Latina: De Lingua et Vita Romanorum** #105 (tokens=71): `Villa magna est                    Campus magnus est               Oppidum magnu`
- **Via Latina: De Lingua et Vita Romanorum** #40 (tokens=65): `Suntne casae in oppido? Casae in oppido non sunt, sed in campo. In eó quoque mul`
- **Via Latina: De Lingua et Vita Romanorum** #31 (tokens=63): `Ecce Làrentia. Larentia femina est. Larentia in Italia habitat. Ea fémina Itala `
- *...还有 25 段*

## Cap.2 (FR Cap.II)

**数据**: 新词 182 / 累计 386 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #31 (tokens=63): `Ecce Làrentia. Larentia femina est. Larentia in Italia habitat. Ea fémina Itala `
- **Ecce Romani I** #96 (tokens=53): `Vir quoque est in pictüra, nomine Davus, qui est servus. In Italia sunt multi se`
- **ecce_romani_combined** #21 (tokens=50): `Vir quoque est in pictura, nomine Davus; qui est servus. In Italia sunt 5 multi `
- **Fabellae Latinae** #201 (tokens=41): `In villa Iülii multa sunt cubicula parva et magna. Magnum est cubiculum Iülii et`
- **Fabellae Latinae** #75 (tokens=38): `Sextus Corneliam vocat: "Veni, Cornelia! Ecce liber novus. Titulus eius est GRAM`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: De Lingua et Vita Romanorum** #90 (tokens=139): `b. Qui habitant nunc cum Láàrentià et Faustulo?                         Masculin`
- **Via Latina: De Lingua et Vita Romanorum** #1565 (tokens=95): `concitàre 12[II].58 concordia -ae f^ 9[I1].67 condere 3[II].43 condicio -ónis f^`
- **Via Latina: De Lingua et Vita Romanorum** #250 (tokens=68): `Ut Làrentia et Faustulus, Romulus Remusque, féminae et viri, puellae et pueri no`
- **Fabellae Latinae** #66 (tokens=65): `Cornelius est dominus Romanus, qui in oppido Tüsculo habitat. Cornelius duos lib`
- **Fabellae Latinae** #106 (tokens=65): `Lydia est femina pulchra quae Romae habitat. Estne femina Romana? Non Romana est`
- *...还有 25 段*

## Cap.3 (FR Cap.III)

**数据**: 新词 96 / 累计 482 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #108 (tokens=49): `Medus laetus est et cantat, quia ad amicam suam ambulat. Sed iam tacet Medus. Cü`
- **Fabellae Latinae** #40 (tokens=42): `Iülia, filia Iülii et Aemiliae, est parva puella laeta quae cantat et ridet. Sed`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #1661 (tokens=24): `et paulum laetiórés... * Quid sibi vult « quin » ? « Quin » significat « quidni `
- **Fabellae Latinae** #48 (tokens=21): `Aemilia respondet: "Marcus ridet, quia Iülia plorat, et Iülia plorat et té vocat`
- **Fabellae Latinae** #85 (tokens=21): `Iam Cornelius ridet neque iràtus est. Pater, quem libri et litterae delectant, l`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: De Lingua et Vita Romanorum** #1564 (tokens=82): `certus -a -um 6([III].84 cessare S[II].41 céteri -ae -a 10[II].83 cibus -1 »» 7 `
- **Via Latina: De Lingua et Vita Romanorum** #341 (tokens=77): `Masculinum Nóm sg -us ^ Voc sg -e                                Nóm sg -er ^ Vo`
- **Reading Latin: Grammar (2e)** #1668 (tokens=66): `S. nom.  utér-que               ütr-a-que            utr-üm-que acc. utr-üm-que `
- **Via Latina: De Lingua et Vita Romanorum** #1620 (tokens=64): `Proca -ae »» 2[II].50 prócédere 11 [III].100 pródigium -i 7 5[II].48 proeliari 1`
- **Via Latina: De Lingua et Vita Romanorum** #469 (tokens=52): `35. Ecce puer Rómànus. Is pugnam trigeminórum videt et eam nàrrat: «Trés sunt Ró`
- *...还有 25 段*

## Cap.4 (FR Cap.IV)

**数据**: 新词 139 / 累计 621 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 3, 2e** #1304 (tokens=66): `singular — m.                     f.                       s                    `
- **Wiley's Real Latin (Maltby & Belcher)** #139 (tokens=55): `m.                    f.                      n.                     m.         `
- **Latin Reader (Reynolds)** #906 (tokens=52): `meus, mea, meum my, mine      pàr, pár, pár; Gen. paris equal SiNaULAR M.       `
- **Fabellae Latinae** #154 (tokens=46): `Iulius et Cornelius sunt domini Romani. Iülius est dominus pecüniósus, qui magna`
- **Oxford Latin Course Part 2, 2e** #992 (tokens=45): `dt.           bon-ó                   bon-ae                  bon-ó             `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: De Lingua et Vita Romanorum** #182 (tokens=99): `Romulus Faustulum et Làrentiam vocat. Ii Ro- mulum sólum vident et interrogant: `
- **First Latin Reader (Chickering)** #876 (tokens=97): `Quid fé - ci ho- mi- ni- bus, quod mé se-quun-tur ca - ni - bus? Quid fe - ci ho`
- **Dioclēs et Flōra (Polis)** #7 (tokens=83): `Salve! Mihi nomen est Diocles. Puer Graecus sum. Non in Graecià habito. In Graec`
- **Dioclēs et Flōra (Polis)** #16 (tokens=77): `Salvete! Mihi nomen est Flora. Sum puella sedecim annorum. Romae habito in domo `
- **Dioclēs et Flōra (Polis)** #17 (tokens=77): `Hic Romae, si puellae pater fügit, et non est alius vir qui custodire eam possit`
- *...还有 25 段*

## Cap.5 (FR Cap.V)

**数据**: 新词 187 / 累计 808 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #66 (tokens=65): `Cornelius est dominus Romanus, qui in oppido Tüsculo habitat. Cornelius duos lib`
- **Fabellae Latinae** #106 (tokens=65): `Lydia est femina pulchra quae Romae habitat. Estne femina Romana? Non Romana est`
- **Via Latina: De Lingua et Vita Romanorum** #40 (tokens=65): `Suntne casae in oppido? Casae in oppido non sunt, sed in campo. In eó quoque mul`
- **Via Latina: De Lingua et Vita Romanorum** #79 (tokens=57): `Ecce Làrentia in casa est. lam Faustulus venit, sed nón solus venit, nam duo pue`
- **Wiley's Real Latin (Maltby & Belcher)** #140 (tokens=55): `Nom. pulcher           pulchr-a         pulchr-um —— pulchr-i              pulch`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **First Latin Reader (Chickering)** #877 (tokens=97): `L4 Quid fé - cf. ho- mi - ni- bus, quod mé se-quun-tur ca - ni - bus? Quid fé - `
- **Oxford Latin Course Part 1, 2e** #640 (tokens=92): `dum parvus est, Marcus plerumque in villa habitat. máter paterque saepe absunt; `
- **Wheelock's Latin 7e** #3657 (tokens=92): `8. Otium est bonum. 9. Multa bella otium nón conservant. 10. Periculum est magnu`
- **Latin Made Simple** #220 (tokens=87): `Servi 1. Romani servos multos in bello occupant. 2. Ex oppidis Graeciae ad Itali`
- **Fabellae Latinae** #273 (tokens=83): `Nox est. Villa Iülii obscüra et quieta est. Omnes dormiunt. Parentes in magno cu`
- *...还有 25 段*

## Cap.6 (FR Cap.VI)

**数据**: 新词 189 / 累计 997 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #853 (tokens=72): `MEMORANDVM II: Ubi? Unde? Quo? Qua? * In linguà Latinà sunt praepositiones quae `
- **Fabellae Latinae** #289 (tokens=54): `Ergo Medus et Lydia Romà égrediuntur et Ostiam ambulàre incipiunt. Medus saccum `
- **Wiley's Real Latin (Maltby & Belcher)** #555 (tokens=54): `m.          f.           n.           m.            f.             n. Nom. — ama`
- **Via Latina: De Lingua et Vita Romanorum** #66 (tokens=53): `Faustulus in campo ambulat et... Quid?! Est lupa in campo! Duo parvi pueri cum e`
- **ecce_romani_combined** #265 (tokens=39): `Ego sum Davus, vllicus GaiI Cornelii. Gaius Cornelius est senator Romanus. Quod `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Reading Latin: Grammar (2e)** #1210 (tokens=127): `114                                                                             `
- **Oxford Latin Course Part 2, 2e** #159 (tokens=116): `cotidie Flaccus filium ad lüdum Orbilii dücébat. Quintus celeriter discébat, et `
- **Via Latina: De Lingua et Vita Romanorum** #999 (tokens=106): `Post exilium Tarquinii Róma iam nón est rég- num, sed 'rés püblica'. In regno ré`
- **Via Latina: De Lingua et Vita Romanorum** #183 (tokens=92): `Nunc Faustulus nàrrat: «Ecce Amülius Silviam rapit et in templo occultat. Hic Si`
- **Latin for Beginners (D'Ooge)** #199 (tokens=88): `T. r. Màrcus amico Sexto consilium suum nüntiat 2. Est copia frümenti in agris n`
- *...还有 25 段*

## Cap.7 (FR Cap.VII)

**数据**: 新词 127 / 累计 1124 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #189 (tokens=43): `Iulius rürsus in equum ascendit et à tabernà Grümionis it ad aliam tabernam suam`
- **Via Latina: De Lingua et Vita Romanorum** #39 (tokens=42): `Larentia in oppido nón habitat. Nec in silva ha- bitat, sed in campo. Larentia i`
- **Fabellae Latinae** #242 (tokens=40): `Cornelius: "In familiis antiquis magnus numerus erat liberorum, ergo filio quint`
- **Wheelock's Latin 7e** #211 (tokens=39): `Puella mea mé nón amat. Val, puella! Catullus obdürat: poéta puellam nón amat, p`
- **Beginner's Latin Book (Textkit)** #600 (tokens=37): `SINGULAR.                      PLÜRAL. N. is    ea    ia      ei, ii    eae     `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Made Simple** #2059 (tokens=161): `Nouns First Declension:                                                    Third`
- **Wheelock's Latin 7e** #3719 (tokens=139): `8. À quó liber parátus est (parátus erat, parabatur)? 9. Magister à quó liber pa`
- **backup_v150_20260606_113934** #4 (tokens=130): `Lingua Latina Pars II Roma Aeterna © 1990 Hans Ørberg Distributed by Hackett Pub`
- **Reading Latin: Grammar (2e)** #2152 (tokens=127): `(e)           ipse ípsa ipsum 'very, 'actual; 'self' s.                         `
- **Oxford Latin Course Part 2, 2e** #1018 (tokens=96): `m.          f            n.                 m.            £              n.     `
- *...还有 25 段*

## Cap.8 (FR Cap.VIII)

**数据**: 新词 216 / 累计 1340 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 3, 2e** #1328 (tokens=198): `n.      m.    f.    n. nom.   hic    haec   hoc (this)   ille     illa     illud`
- **Wheelock's Latin 7e** #4050 (tokens=147): `PRONOUNS Demonstrative hic, this                                                `
- **Oxford Latin Course Part 2, 2e** #1018 (tokens=96): `m.          f            n.                 m.            £              n.     `
- **Oxford Latin Course Part 1, 2e** #677 (tokens=94): `m.           f.             n.                    m            f.             n.`
- **Latin Made Simple** #2067 (tokens=90): `l. hic Singular Masc.             Fem. Nom. hic                haec Gen. huius  `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Oxford Latin Course Part 3, 2e** #1328 (tokens=198): `n.      m.    f.    n. nom.   hic    haec   hoc (this)   ille     illa     illud`
- **Wheelock's Latin 7e** #4050 (tokens=147): `PRONOUNS Demonstrative hic, this                                                `
- **Latin Made Simple** #2069 (tokens=137): `Plural Masc.              Fem.               Neut. Nom. ipsi                 ips`
- **Latin by the Natural Method (W.G. Most 1957)** #343 (tokens=131): `Románam cápere vóluit. Mithradátes erat rex qui mag- nam potestátem hábuit. Sull`
- **Latin by the Natural Method (W.G. Most 1957)** #346 (tokens=126): `Sed primo saéculo ante Christum fuérunt multi viri magni. Inter hos erat Gaius I`
- *...还有 25 段*

## Cap.9 (FR Cap.IX)

**数据**: 新词 187 / 累计 1527 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #273 (tokens=83): `Nox est. Villa Iülii obscüra et quieta est. Omnes dormiunt. Parentes in magno cu`
- **Via Latina: De Lingua et Vita Romanorum** #341 (tokens=77): `Masculinum Nóm sg -us ^ Voc sg -e                                Nóm sg -er ^ Vo`
- **Fabellae Latinae** #158 (tokens=73): `Amici duo oppidum relinquunt et per vallem ad silvam eunt. Equi laeti per campum`
- **Oxford Latin Course Part 1, 2e** #678 (tokens=73): `m.           y.             n.                    m.           LE             n.`
- **Via Latina: De Lingua et Vita Romanorum** #57 (tokens=73): `Larentia nón in oppido, sed in campo habitat. Casa Larentiae nón in oppido est: `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #630 (tokens=127): `remánsit máximo afféctus est dolóre. Dixit enim, '*O! O! Necésse est timére. Sed`
- **Latin by the Natural Method (W.G. Most 1957)** #865 (tokens=127): `Sed ecce— vir Aegjptius ad nos venit. Interrogémus eum de terra hac. Amice! (fri`
- **Reading Latin: Study Guide** #215 (tokens=112): `2 pulchro: masc./neut., dat./abl. sing.: oneris (neut. gen. sing); *scelere (neu`
- **First Latin Reader (Chickering)** #1239 (tokens=111): `Antonio se vertit...(ab-4- abl.) Corpore animum deus circumdedit. .........vidé `
- **Wheelock's Latin 7e** #3673 (tokens=109): `5. Hi totam civitátem dücent (dücunt, dücébant). 6. Ille haec in illà terrà vide`
- *...还有 25 段*

## Cap.10 (FR Cap.X)

**数据**: 新词 264 / 累计 1791 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #90 (tokens=139): `b. Qui habitant nunc cum Láàrentià et Faustulo?                         Masculin`
- **Latin Made Simple** #2069 (tokens=137): `Plural Masc.              Fem.               Neut. Nom. ipsi                 ips`
- **Reading Latin: Grammar (2e)** #2152 (tokens=127): `(e)           ipse ípsa ipsum 'very, 'actual; 'self' s.                         `
- **Latin Reader (Reynolds)** #66 (tokens=108): `4                          The Sun DE SOLE Lümen magnum in caelo vidémus. Id lüm`
- **First Latin Reader (Chickering)** #876 (tokens=97): `Quid fé - ci ho- mi- ni- bus, quod mé se-quun-tur ca - ni - bus? Quid fe - ci ho`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #418 (tokens=295): `CAP. LVI  vestigiis (dat) ingredi  = vestigia sequi  menscuiusqueisestquis­ que:`
- **Latin by the Natural Method (W.G. Most 1957)** #951 (tokens=260): `Deínde Ptáhotep rem novam dixit, *Re vera, unus ex régibus nostris olim factus e`
- **Latin by the Natural Method (W.G. Most 1957)** #107 (tokens=210): `Románi fere semper bellum habuérunt. Quando bellum cum áliis natióni- bus non ha`
- **Latin by the Natural Method (W.G. Most 1957)** #621 (tokens=194): `In princípio enim, solus Deus erat; nulla creatára adhuc facta erat. Scriptor hu`
- **Latin by the Natural Method (W.G. Most 1957)** #113 (tokens=191): `Marcus vóluit amáre Maríam. María vóluit cápere Marcum. Isabélla pótuit dare pec`
- *...还有 25 段*

## Cap.11 (FR Cap.XI)

**数据**: 新词 224 / 累计 2015 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Made Simple** #220 (tokens=87): `Servi 1. Romani servos multos in bello occupant. 2. Ex oppidis Graeciae ad Itali`
- **First Latin Reader (Chickering)** #869 (tokens=69): `Quod de-dit mo-ri-tü - ra A-mi-ca, po- cu - lum. Po- to - ris hü-ment o - ra Pro`
- **Fabellae Latinae** #267 (tokens=62): `Post horam servus cum medico ad villam Iülii redit. Medicus Marcum linguam osten`
- **Oxford Latin Course Part 1, 2e** #108 (tokens=59): `céteri pueri iam adsunt.  magister : e jianuà exit et eos iubet intrare et sedér`
- **Reading Latin: Study Guide** #405 (tokens=59): `4        uiri, patres (nom. pl.), feminae, exercitui, puero (dat. sing.). ei is `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #419 (tokens=250): `CAP. LVI  275 tur. Id autem nec nasci: potest nec mori (vel concidat vel: aliter`
- **Latin for Beginners (D'Ooge)** #1197 (tokens=153): `234                     APPENDIX I pulcher, j7e//£y  SrEMs pulchro- m. and n., p`
- **Latin for Beginners (D'Ooge 另一版)** #1171 (tokens=151): `f |              pulcher, j7e//y  SrEMs pulchro- m. and n., pulchrà- f. Bass pul`
- **Via Latina: Easy Latin Reader (Collar 1897)** #197 (tokens=147): `Superbum régem adiit, novem libros ferens, quos esse dicebat divina oracula: eos`
- **Gwynne's Latin** #139 (tokens=139): `B. 1. Ab initio hunc librum legere facile fuit. 2. Ipse me in speculo videre non`
- *...还有 25 段*

## Cap.12 (FR Cap.XII)

**数据**: 新词 305 / 累计 2320 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #1565 (tokens=95): `concitàre 12[II].58 concordia -ae f^ 9[I1].67 condere 3[II].43 condicio -ónis f^`
- **Latin for Beginners (D'Ooge)** #199 (tokens=88): `T. r. Màrcus amico Sexto consilium suum nüntiat 2. Est copia frümenti in agris n`
- **Latin for Beginners (D'Ooge 另一版)** #203 (tokens=88): `I. i. Màrcus amicó Sexto consilium suum nüntiat. 2. Est cópia frümenti in agris `
- **Latin Made Simple** #829 (tokens=88): `Practice Exercises No. 110. Translate these phrases which use hic and ille: l. h`
- **Via Latina: De Lingua et Vita Romanorum** #1603 (tokens=87): `máteria -ae f^ 10[III].97 mátrimónium -i 7 2[II].74 mátróna -ae f^ 7(II].43 maxi`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #131 (tokens=278): `PENSVM C sos - [ = oppugnarent].  Cum duo RomanI - [ = morientes] concidissent, `
- **backup_v150_20260606_113934** #400 (tokens=272): `CAP. LV  quo(+ com)= uteo(uteo  modo)  visum esse R. in eo colle  qui.. . vocatu`
- **backup_v150_20260606_113934** #372 (tokens=270): `CAP. LIV  (se periculo ) committere  = obicere  hos-ce = hos  praesidio (dat ) e`
- **backup_v150_20260606_113934** #182 (tokens=269): `CAP. XLVI  singularis -e: certamen  s.e = c . inter singulos  torquatus -a -um =`
- **backup_v150_20260606_113934** #363 (tokens=266): `Quid? quod salus sociorum summum in periculum ac  95 discrimen vocatur, quo id t`
- *...还有 25 段*

## Cap.13 (FR Cap.XIII)

**数据**: 新词 382 / 累计 2702 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader (Reynolds)** #264 (tokens=324): `Dates given in full                        Abbreviated On Dec. 1.               `
- **Latin Made Simple** #2059 (tokens=161): `Nouns First Declension:                                                    Third`
- **Latin by the Natural Method (W.G. Most 1957)** #346 (tokens=126): `Sed primo saéculo ante Christum fuérunt multi viri magni. Inter hos erat Gaius I`
- **Latin by the Natural Method (W.G. Most 1957)** #673 (tokens=115): `Cain et Abel fuérunt fílii Adam et Evae. Nati sunt in primis diébus mundi. Sed é`
- **ecce_romani_combined** #46 (tokens=110): `Sextus, ubi in hortum mane exit, Davum conspicit et furtim appropinquat. Subito,`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader (Reynolds)** #264 (tokens=324): `Dates given in full                        Abbreviated On Dec. 1.               `
- **backup_v150_20260606_113934** #411 (tokens=290): `CAP. LVI  quid moror in terris? Quin hiic ad vos venire propero?"  "Non est ita"`
- **backup_v150_20260606_113934** #397 (tokens=287): `multorum, nec una hominis vita, sed aliquot constituta  saeculis et aetatibus. N`
- **backup_v150_20260606_113934** #388 (tokens=275): `CAP. LV  Q.Aeliuslùbero  Quid tu venis ...  facultas = occasio  litteras explica`
- **backup_v150_20260606_113934** #269 (tokens=270): `Id iugum, sicut Appennini dorso Italia dividitur, ita  mediam Graeciam dirimit. `
- *...还有 25 段*

## Cap.14 (FR Cap.XIV)

**数据**: 新词 255 / 累计 2957 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #621 (tokens=194): `In princípio enim, solus Deus erat; nulla creatára adhuc facta erat. Scriptor hu`
- **Latin by the Natural Method (W.G. Most 1957)** #865 (tokens=127): `Sed ecce— vir Aegjptius ad nos venit. Interrogémus eum de terra hac. Amice! (fri`
- **Ecce Romani I** #1043 (tokens=89): `Case Masc. — Fem. — Neut Singular Nom. |magnus X magna    magnum  |omnis    omni`
- **Ecce Romani I** #77 (tokens=84): `Cornatia est puella Roómàna. Flàvia quoque est puella Romana. Cornelia et Flàvia`
- **Reading Latin: Study Guide** #312 (tokens=81): `*Declined in full; omnis res, omnem rem, omnis rei, omni rei, omni re, omnes res`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #118 (tokens=289): `CAP. XLIII  (fratres ) tri-geminI = tres  eodem die nati  morte : ob mortem  ( c`
- **backup_v150_20260606_113934** #141 (tokens=286): `tus locus est. Loca divisa patribus equitibusque ubi  spectacula sibi facerent, `
- **backup_v150_20260606_113934** #125 (tokens=280): `nos castra sua Romanis castris iungere iubet; sacrifi- 230 cium in diem posterum`
- **backup_v150_20260606_113934** #361 (tokens=277): `40 suscepit, sed ab illo tempore annum iam tertium et vi:ce- simum regnat - et i`
- **backup_v150_20260606_113934** #126 (tokens=276): `CAP. XLIII  servare<--> rumpere  in-sanabilis -e= qui  sanari non potest  at = t`
- *...还有 25 段*

## Cap.15 (FR Cap.XV)

**数据**: 新词 207 / 累计 3164 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #883 (tokens=157): `domus magna. Nemo enim in persóna secünda loqui potest huic regi. Semper dícimus`
- **Via Latina: De Lingua et Vita Romanorum** #182 (tokens=99): `Romulus Faustulum et Làrentiam vocat. Ii Ro- mulum sólum vident et interrogant: `
- **Oxford Latin Course Part 2, 2e** #174 (tokens=93): `Cicero ad pueros se vertit. 'veni hüc, Marce,' inquit, 'et amicum tuum mihi comm`
- **ecce_romani_combined** #59 (tokens=87): `Tum Flavia, “Sed Marcus est semper sollicitus. Sextum nihil terret.” Subito lupu`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #236 (tokens=86): `Salvéte discipuli. Avé magister. Valesne bene ? Optime valeo. Grátiàs tibi ago, `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #104 (tokens=295): `CAP. XLII  aegre = magno cum  labore, vix  e-vadere  iniiiria mulierum = i.  mul`
- **backup_v150_20260606_113934** #161 (tokens=289): `54 Inde Sex. Tarquinius cònsiliis publicis interesse coe- pit. Ibi, cum 'de alii`
- **backup_v150_20260606_113934** #45 (tokens=288): `CAP. XXXVIII  constituerunt. Ergo uhi primum ventus secundus fuit,  iterum in al`
- **backup_v150_20260606_113934** #134 (tokens=288): `CAP. XLIV  regnum agere = regnare  memor : simile  in populò cum novò  tum feròc`
- **backup_v150_20260606_113934** #364 (tokens=285): `CAP. LIV  Quare, si propter socios, nulla ipsi iniuria lacessiti, 14  maiores no`
- *...还有 25 段*

## Cap.16 (FR Cap.XVI)

**数据**: 新词 375 / 累计 3539 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #90 (tokens=141): `In rebus humánis, perículum non e:            Románi bellum habuérunt in multis `
- **Cambridge Latin Course 1** #110 (tokens=108): `Caecilius est in foro. Caecilius in foro argentariam habet. Hermogenes ad forum `
- **Via Latina: De Lingua et Vita Romanorum** #1227 (tokens=97): `Ad Alpés posteà venit, qui montés nón solum maxime alti erant, sed etiam pericul`
- **Oxford Latin Course Part 1, 2e** #640 (tokens=92): `dum parvus est, Marcus plerumque in villa habitat. máter paterque saepe absunt; `
- **Latin by the Natural Method (W.G. Most 1957)** #523 (tokens=86): `Sed Catilína ipse non erat in cárcere. Erat cum exércitu suo. Catilína sperábat `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #354 (tokens=302): `CAP. LIII  impunitas -atisf( < im- fluentes iuvenilI quadam dicendi impunita te `
- **backup_v150_20260606_113934** #160 (tokens=297): `CAP.XLV  talentum: Graecorum  pondus statiitum max­ imum [26 kg]  lentius spe: l`
- **backup_v150_20260606_113934** #313 (tokens=295): `mantia meque regnumque meum gloria honoravistI tua­ que virtute nobis Romanos ex`
- **backup_v150_20260606_113934** #8 (tokens=284): `CAP.XXXVI  magnificus , comp-fic en­ tior , sup -ficentissimus  Palatinus -a -um`
- **backup_v150_20260606_113934** #64 (tokens=282): `CAP. XXXIX  extrema loca  si in (ali)quibus silvis aut  urbibus  e-rigere (animu`
- *...还有 25 段*

## Cap.17 (FR Cap.XVII)

**数据**: 新词 274 / 累计 3813 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Gwynne's Latin** #139 (tokens=139): `B. 1. Ab initio hunc librum legere facile fuit. 2. Ipse me in speculo videre non`
- **Wheelock's Latin 7e** #3657 (tokens=92): `8. Otium est bonum. 9. Multa bella otium nón conservant. 10. Periculum est magnu`
- **Latin for Beginners (D'Ooge)** #140 (tokens=84): `i. Longae nón sunt tuae viae. 2. Suntne tubae novae in mea casá? NOn sunt. 3. Qu`
- **Latin for Beginners (D'Ooge 另一版)** #137 (tokens=84): `i. Longae nón sunt tuae viae. 2. Suntne tubae novae in meà casá? NOn sunt. 3. Qu`
- **Via Latina: De Lingua et Vita Romanorum** #721 (tokens=74): `In oraculo Delphico filii Tarquinii dé prodigio anguis Pythiam primum interrogan`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #56 (tokens=290): `CAP. XXXIX  haec secum dfxit  me-nenonposse? = non­ ne ego possum?  dis-icere-ie`
- **backup_v150_20260606_113934** #254 (tokens=270): `CAP. XLIX  palam facere = pate­ facere  publicare = publicum  facere  dis-icere `
- **backup_v150_20260606_113934** #57 (tokens=261): `saxa latentia abripiuntur, tres ab alto in vada feruntur,  unam ante ipsius Aene`
- **backup_v150_20260606_113934** #393 (tokens=254): `150 saepe te cum Panaetio disserere solitum coram Polybio,  duobus Graecis vel p`
- **backup_v150_20260606_113934** #329 (tokens=253): `87 Sed consul in agrum fertilem proficiscitur, omnia ibi  530 capta militibus do`
- *...还有 25 段*

## Cap.18 (FR Cap.XVIII)

**数据**: 新词 406 / 累计 4219 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #418 (tokens=295): `CAP. LVI  vestigiis (dat) ingredi  = vestigia sequi  menscuiusqueisestquis­ que:`
- **First Latin Reader (Chickering)** #78 (tokens=137): `populo Rómam dedit. Roma: haec eadem urbs est nunc prima inter omnes totius Ital`
- **Oxford Latin Course Part 2, 2e** #159 (tokens=116): `cotidie Flaccus filium ad lüdum Orbilii dücébat. Quintus celeriter discébat, et `
- **Latin First Year (Magoffin)** #1601 (tokens=94): `THE PRONOUN IDEM                          365 Singular                          `
- **First Latin Reader (Chickering)** #74 (tokens=93): `pater tuus fuit Màrs. Quis fuit Mars? Fuit 170 belli deus, ac armorum exercituum`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #63 (tokens=290): `QuI postquam ad reginam adductI sunt, Ilioneus,  maximus eorum, sic orsus est: "`
- **backup_v150_20260606_113934** #78 (tokens=278): `CAP. XL  quin + imp = age  avene : prohibe  discessus -us m  < discedere  Quin m`
- **backup_v150_20260606_113934** #200 (tokens=277): `CAP.XLVII  coniectiiram facere =  intellegere id quod  non palam dicitur  Homeru`
- **backup_v150_20260606_113934** #62 (tokens=273): `CAP. XXXIX  quis locus = quf locus  Achates, voc -e  laudi: factis laudandis,  g`
- **backup_v150_20260606_113934** #367 (tokens=268): `CAP. LIV  regis omnibus rebus ornata ac referta, ceterasque urbes  Ponti et Capp`
- *...还有 25 段*

## Cap.19 (FR Cap.XIX)

**数据**: 新词 336 / 累计 4555 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #484 (tokens=128): `Inter populós Indoeurópaeós magnus est numerus deorum. Rómàni, ut Graeci, nón ün`
- **Reading Latin: Grammar (2e)** #1210 (tokens=127): `114                                                                             `
- **Via Latina: De Lingua et Vita Romanorum** #281 (tokens=126): `Itaque socii geminos monent: «Rogate deos at- que signum eórum exspectàáte». Gem`
- **Oxford Latin Course Part 3, 2e** #1327 (tokens=117): `m.             £               n.         "         m             f.            `
- **Reading Latin: Study Guide** #215 (tokens=112): `2 pulchro: masc./neut., dat./abl. sing.: oneris (neut. gen. sing); *scelere (neu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #260 (tokens=307): `PENSVM B CAP. XLIX  Vocabula nuva:  natio  heredita s  suspicio  puerulus  obitu`
- **backup_v150_20260606_113934** #59 (tokens=298): `95 arborum occultat; ipse uno Achate comitatus graditur  duo tela manu gerens. C`
- **backup_v150_20260606_113934** #103 (tokens=280): `120 Curtius, Romanos Hostius Hosti:lius. Hic mi:lites suos  iniquo loco pugnante`
- **backup_v150_20260606_113934** #351 (tokens=279): `cens M. Antonium et Q. Hortensium, qui tum arte oratoria  excellebant, assidue a`
- **backup_v150_20260606_113934** #91 (tokens=277): `educati erant urbem condere. Deinde ob cupiditatem  regnI foedum certamen ortum `
- *...还有 25 段*

## Cap.20 (FR Cap.XX)

**数据**: 新词 355 / 累计 4910 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #424 (tokens=194): `INDEX GRAMMATICVS NOTAE Cap. XXXVI. De casu genetivo .  XXXVII. De casu dativo .`
- **Oxford Latin Course Part 1, 2e** #679 (tokens=171): `Ist conj.                      2nd conj.                     3rd conj.          `
- **Wheelock's Latin 7e** #3723 (tokens=165): `6. Quis ad nós eó tempore venit? 7. Senex magnae fámae ex patrià suà ad senàtum `
- **Gwynne's Latin** #132 (tokens=149): `B. 1. Caesar hostes principio anni oppugnaverat, et (eos) una mense superaverat `
- **Latin by the Natural Method (W.G. Most 1957)** #736 (tokens=130): `Diffícile est bonus esse inter malos. Sed Abram, cum esset in médio tam multórum`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #149 (tokens=307): `CAP. XLIV  ipsae longe dispares moribus. Ferox Tullia, quae Ar- runti Tarquinio `
- **backup_v150_20260606_113934** #42 (tokens=304): `CAP. XXXVII  famulus  ras  aura  socius  niimen  fèstus  profugu s  benignus  di`
- **backup_v150_20260606_113934** #310 (tokens=304): `CAP. LII  per-manere  Masi nissa  Micipsa Gulussa Masta- h nati  Adher- Hiem- Iu`
- **Oxford Latin Course Part 2, 2e** #1026 (tokens=297): `Imperative singular       para                     moné                      reg`
- **backup_v150_20260606_113934** #32 (tokens=295): `CAP.XXXVII  complectl -plexum  tener -a -um = mollis et  tenuis , invalidus  cor`
- *...还有 25 段*

## Cap.21 (FR Cap.XXI)

**数据**: 新词 252 / 累计 5162 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #951 (tokens=260): `Deínde Ptáhotep rem novam dixit, *Re vera, unus ex régibus nostris olim factus e`
- **backup_v150_20260606_113934** #244 (tokens=258): `PENSVM A CAP. XLVIII  Vocabula nova:  praetòrium  assensus  vitium  hiberna  opp`
- **Latin by the Natural Method (W.G. Most 1957)** #107 (tokens=210): `Románi fere semper bellum habuérunt. Quando bellum cum áliis natióni- bus non ha`
- **Latin by the Natural Method (W.G. Most 1957)** #113 (tokens=191): `Marcus vóluit amáre Maríam. María vóluit cápere Marcum. Isabélla pótuit dare pec`
- **Wheelock's Latin 7e** #3719 (tokens=139): `8. À quó liber parátus est (parátus erat, parabatur)? 9. Magister à quó liber pa`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Oxford Latin Course Part 2, 2e** #1024 (tokens=369): `Active Ist conjugation         2nd conjugation       3rd conjugation        4th `
- **Oxford Latin Course Part 3, 2e** #1335 (tokens=369): `Active Indicative -—            Ist conjugation           2nd conjugation       `
- **backup_v150_20260606_113934** #245 (tokens=306): `PENSVM B Hannibal puer, cum patri - ut se duceret in Hispaniam, iure  iurando - `
- **backup_v150_20260606_113934** #174 (tokens=283): `PENSVM C CAP. XLV  manifestus  pròmptus  imperfectus  anxrns  bn1tus  expers  ca`
- **backup_v150_20260606_113934** #107 (tokens=280): `CAP. XLII  armatos ad ciistodiam corporis, quos Celeres appellavit, equùesarmato`
- *...还有 25 段*

## Cap.22 (FR Cap.XXII)

**数据**: 新词 312 / 累计 5474 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #305 (tokens=254): `GRAMMATICA LATINA Igitur ea victoria nobilitas ex libidine sua usa multos  morta`
- **backup_v150_20260606_113934** #7 (tokens=172): `ROMA AETERNA CAPITVLVM TRICESIMVM SEXTVM  Paliitium et Capitolium  Urbs Roma in `
- **Latin by the Natural Method (W.G. Most 1957)** #182 (tokens=169): `Románus exércitus victus est ab Hannibále ad flumen Trébiam. In próximo anno, Há`
- **De Rerum Natura (Lucretius 拉语版)** #649 (tokens=143): `Mors nihil est ad nos, neque quidquam pertinet, quandoquidem nàtüra animi est mo`
- **Latin Made Simple** #1228 (tokens=131): `Cupido et Psyche (cont'd) 1. Locus, quem oraculum demonstraverat et in quo marit`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #147 (tokens=293): `centuriae, quae sine armis stipendia facerent. Secunda  classis intra centum usq`
- **backup_v150_20260606_113934** #110 (tokens=281): `CAP. XLII  [anno 235 a. C.]  Punicus -a -um = Kar- thaginiensi s  Actiacus -a -u`
- **backup_v150_20260606_113934** #362 (tokens=277): `CAP. LIV  singulari s = cui par non  est  initia praeclara: expugna­ tio Cyzici,`
- **backup_v150_20260606_113934** #304 (tokens=274): `CAP. LI  abs-trahere  faccione: quia factione  iiinctaerat  pollere = valere  di`
- **backup_v150_20260606_113934** #203 (tokens=263): `95 est). Eoque ipso anno, quI erat post reciperatam urbem  septimus, Aristotelem`
- *...还有 25 段*

## Cap.23 (FR Cap.XXIII)

**数据**: 新词 270 / 累计 5744 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin 7e** #3755 (tokens=147): `14. Sció té hoc fécisse (factürum esse, facere). 15. Scivi té hoc fécisse (factü`
- **Latin by the Natural Method (W.G. Most 1957)** #630 (tokens=127): `remánsit máximo afféctus est dolóre. Dixit enim, '*O! O! Necésse est timére. Sed`
- **Latin Made Simple** #1148 (tokens=123): `Aeneas in Igni Troiae l. Aeneas in vias Troiae una nocte cucurrit et multitudine`
- **Reading Latin: Grammar (2e)** #647 (tokens=123): `mé pater meus, rex deorum, officium magnum perficere iubet. quando patrem meum c`
- **Latin by the Natural Method (W.G. Most 1957)** #790 (tokens=120): `*Cur vis interfícere me?" rogávit fsaac. "Hódie enim tecum egréssus sum ut sacri`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #201 (tokens=296): `mam conditam, aut non longe amplius, victos esse ab  Atheniensibus Persas memori`
- **backup_v150_20260606_113934** #138 (tokens=295): `CAP. XLIV  Demaratus -im  Corinthius -a -um < Co­ rinthus; m civis C.  sediti6 -`
- **backup_v150_20260606_113934** #153 (tokens=289): `PENSVM A PENSVM B De adverbiis  Tullus legatos Albanos bland- ac benign- recepit`
- **backup_v150_20260606_113934** #215 (tokens=277): `pus ab apparatu operum ac munitionum nihil cessatum.  ltaque acrius de integro c`
- **backup_v150_20260606_113934** #295 (tokens=266): `CAP. LI  ampia mano saltum iniquum insèderat), suasit primo Scipio suasit  consu`
- *...还有 25 段*

## Cap.24 (FR Cap.XXIV)

**数据**: 新词 245 / 累计 5989 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #447 (tokens=133): `Quodam die Marcus erat in schola. Agnus non venit in scholam, sed quid áccidit? `
- **Latin by the Natural Method (W.G. Most 1957)** #556 (tokens=133): `Amíci Catilínae in cárcerem ibant. In cárcere mori- éntur. Ergo magno affécti su`
- **Latin Made Simple** #1070 (tokens=108): `Equus Troiae l. Graeci novem annos Troiam oppugnaverunt et iam domi esse cupieba`
- **Latin by the Natural Method (W.G. Most 1957)** #395 (tokens=104): `Hic est modus quo Pompéius vóluit delére Caésarem: vóluit cógere eum redíre in u`
- **Latin by the Natural Method (W.G. Most 1957)** #826 (tokens=104): `* Esau, cur locütus es haec verba contra Iacob fratrem tuum?" "Quia ille malus e`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #257 (tokens=295): `larem cenarent, atque ibi de Hannibale mentione facta  ex iis fmus diceret 'eum `
- **backup_v150_20260606_113934** #121 (tokens=269): `Amor immatiirus  26 Priusquam inde digrederentur, Tullus Mettio impe- rat uti iu`
- **backup_v150_20260606_113934** #88 (tokens=262): `CAP. XLI  disii= forte  pro-creare = gignere  ortus = natus , genitus  Atys -yis`
- **backup_v150_20260606_113934** #333 (tokens=259): `CAP. LII  104 Marius, postquam Cirtam rediit, mandata Bocchi:  cognoscit. Legati`
- **Wheelock's Latin Reader** #1889 (tokens=246): `Moralitas: Carissimi, imperator est Deus, qui diu guerram cum homine habuit in t`
- *...还有 25 段*

## Cap.25 (FR Cap.XXV)

**数据**: 新词 427 / 累计 6416 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #998 (tokens=168): `Post haec, Ioséphus dedit münera bona síngulis frátribus suis, et profi- ciscént`
- **Wheelock's Latin 7e** #3691 (tokens=164): `8. Caesar eós servàvit. 9. Caesar eum servàbat. 10. Caesar sé servàvit. 11. Rómà`
- **backup_v150_20260606_113934** #11 (tokens=161): `Maxima'. Postremus siccatus est locus in medio foro  qui 'lacus Curtius' dicitur`
- **Gwynne's Latin** #149 (tokens=138): `B. 1. [Nos] qui linguam Latinam didicimus et latine nunc bene loquimur omnes cet`
- **Via Latina: De Lingua et Vita Romanorum** #653 (tokens=132): `Post Servium Tullium régnat in urbe Tarqui- nius Superbus, septimus rex Romae. À`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #114 (tokens=293): `PENSVM B Ct\l'. XLII  columba  agna  commodum  tubicen  pignus  socer  agrestis `
- **backup_v150_20260606_113934** #96 (tokens=286): `PENSVM C CAP. XLI  stabulum  saltus  latro  Insidiae  necessitas  concilium  avu`
- **backup_v150_20260606_113934** #173 (tokens=282): `PENSVM A PENSVM B De pronominibus  Qu- fuit rex ili- feròx qu- Roma exactus est?`
- **backup_v150_20260606_113934** #41 (tokens=281): `PENSVM A PENSVM B De ctisu dativo  Aedes Castoris sacrata est di- Castor- et Pol`
- **backup_v150_20260606_113934** #210 (tokens=278): `CAP. XLVIII  ad-igere-egisse-acturn =  cogere; iure iurando a.  = ad ius iurandu`
- *...还有 25 段*

## Cap.26 (FR Cap.XXVI)

**数据**: 新词 360 / 累计 6776 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #60 (tokens=266): `CAP.XXXIX  thesaurus -i m = auri et  argenti copia occulta  (fugam ) parare = fa`
- **backup_v150_20260606_113934** #306 (tokens=212): `PENSVM A CAP. LI  co-igere > c6gere  sed: circum- , per-agere,  ante-capere  de-`
- **Wheelock's Latin 7e** #3843 (tokens=182): `4. Magnopere vereor ut imperátor nóbis satis auxilii mittat. 5. Fuit fémina maxi`
- **Latin by the Natural Method (W.G. Most 1957)** #126 (tokens=172): `étiam misérunt naves in multa mária. Carthaginiénses boni mercatüra fuérunt. Sed`
- **Latin by the Natural Method (W.G. Most 1957)** #104 (tokens=156): `fuérunt in urbe, plebs non pugnávit cum patríciis. Et patrícii non pugnavérunt c`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #164 (tokens=287): `CAP.XLV  prae-poten s -entis = prae  aliis potens, potentissi­ mus  ditare=divit`
- **backup_v150_20260606_113934** #167 (tokens=261): `Cultrum, quem sub veste abditum habebat, eum in  corde defigit, prolapsaque in v`
- **backup_v150_20260606_113934** #34 (tokens=251): `CAP. XXXVII  summa : ultima "Venir summa dies et ineluctabile tempus 324  in-élu`
- **backup_v150_20260606_113934** #266 (tokens=233): `CAP. L  re-petere = iterare  raptim = celeriter  prae-occupare  sensus -us m < s`
- **Intermediate Oral Latin Reader** #191 (tokens=232): `mortem omni aetüti esse commünem. — At sperat adules- cens diü sé victürum, quod`
- *...还有 25 段*

## Cap.27 (FR Cap.XXVII)

**数据**: 新词 433 / 累计 7209 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #372 (tokens=270): `CAP. LIV  (se periculo ) committere  = obicere  hos-ce = hos  praesidio (dat ) e`
- **backup_v150_20260606_113934** #413 (tokens=266): `det illa quam in terris 'Saturniam' nominant. Deinde est  125 hominum generi pro`
- **backup_v150_20260606_113934** #16 (tokens=246): `CAP. XXXVI  con-stituere -uisse -utum  = locare (rem novam),  primum facere  [Fa`
- **Latin by the Natural Method (W.G. Most 1957)** #989 (tokens=243): `Ex his verbis Iudae, et étiam ex eis quae álii fratres fécerant, Ioséphus pótera`
- **Latin by the Natural Method (W.G. Most 1957)** #1140 (tokens=198): `enim dixi, in terram nostram venérunt tempóribus malórum regum. Sed ínsuper, hi `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #300 (tokens=269): `CAP. LI  luxuria -aef = luxus  disciplina<-> Iicentia  re-cidere = adimere  (cae`
- **backup_v150_20260606_113934** #256 (tokens=264): `CAP. XLIX  -undum = -endum  venenatus -a -um =  venenum gerens  serpens-entisf =`
- **backup_v150_20260606_113934** #208 (tokens=246): `PENSVM C CAP. XLVII  sacrarium  quindecimvirI  iiis iiirandum  scriptum  incònsp`
- **backup_v150_20260606_113934** #242 (tokens=240): `CAP. XLVIII  perfuga-aem= milesqui quosque agros ante bellum tenuissent, teneren`
- **backup_v150_20260606_113934** #283 (tokens=240): `fortii.nae ad ultimum finem centum quinquaginta annos  stetit.  CAP.L  16 Q. Ael`
- *...还有 25 段*

## Cap.28 (FR Cap.XXVIII)

**数据**: 新词 440 / 累计 7649 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #411 (tokens=290): `CAP. LVI  quid moror in terris? Quin hiic ad vos venire propero?"  "Non est ita"`
- **backup_v150_20260606_113934** #8 (tokens=284): `CAP.XXXVI  magnificus , comp-fic en­ tior , sup -ficentissimus  Palatinus -a -um`
- **backup_v150_20260606_113934** #125 (tokens=280): `nos castra sua Romanis castris iungere iubet; sacrifi- 230 cium in diem posterum`
- **backup_v150_20260606_113934** #388 (tokens=275): `CAP. LV  Q.Aeliuslùbero  Quid tu venis ...  facultas = occasio  litteras explica`
- **backup_v150_20260606_113934** #17 (tokens=272): `ea urbis parte quae est post Comitium, multis domibus  privatis destructis, novu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #137 (tokens=265): `mam tradiixit. Et cum circa Palatium, sedem veterum  70 Romanorum, Sabini Capito`
- **backup_v150_20260606_113934** #284 (tokens=264): `CAP. L  praeses-idis mlf = ciistos  excidium: Corinthusxxr  annrs post a Romanrs`
- **Oxford Latin Course Part 3, 2e** #58 (tokens=254): `festinàvit cum Pompeio ut locum sacrum spectaret ubi Apollo r nátus erat. cum om`
- **Oxford Latin Course Part 3, 2e** #1338 (tokens=243): `Subjunctive Ist conjugation          2nd conjugation          Jrd conjugation   `
- **backup_v150_20260606_113934** #338 (tokens=239): `PENSVM C CAP. LII  obtestari  quire  dìlabi  observare  eniti  disceptare  molir`
- *...还有 25 段*

## Cap.29 (FR Cap.XXIX)

**数据**: 新词 434 / 累计 8083 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #50 (tokens=267): `CAP. XXXVIII  e-dere -didisse -ditum  <e+ dare  ni-mirum adv = scilicet,  certe `
- **backup_v150_20260606_113934** #113 (tokens=256): `PENSVM A et quasi sentirent, blando clamore nepotes  tendebant ad avos bracchia `
- **backup_v150_20260606_113934** #49 (tokens=243): `potenti maxima sacrificia fac! Sic denique, Sicilia re­ licta, tiitus in Italiam`
- **backup_v150_20260606_113934** #36 (tokens=236): `CAP. XXXVII  vitam effundere = mori  caelestis -e < caelum  nequiquam = frustra `
- **backup_v150_20260606_113934** #72 (tokens=194): `CAP. XL  in-cumbere lecto (dat)  = in lecto cubant em  se ponere  Dido et Aeneas`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #246 (tokens=275): `PENSVM C CAP. XLVIII  quassare  procidere  irritare  gratificari  succingere  ci`
- **backup_v150_20260606_113934** #265 (tokens=267): `milia armatorum haberet neve elephantum ullum; bel- 45 lum extra Macedoniae fine`
- **backup_v150_20260606_113934** #65 (tokens=228): `Haec memorans Aeneam in regiam diicit. lnterea ad  sociòs in litore relictòs mii`
- **backup_v150_20260606_113934** #238 (tokens=224): `CAP. XLVIII  procos. = proconsul,  p/procoss .  mortem sibi consciscere  = se in`
- **Wheelock's Latin Reader** #865 (tokens=221): `Quis est—pro deorum fidem atque hominum!— qui velit, ut neque diligat quemquam n`
- *...还有 25 段*

## Cap.30 (FR Cap.XXX)

**数据**: 新词 366 / 累计 8449 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #313 (tokens=295): `mantia meque regnumque meum gloria honoravistI tua­ que virtute nobis Romanos ex`
- **backup_v150_20260606_113934** #109 (tokens=282): `Numa Pompilius rex  18 Eo tempore Numa Pompilius Curibus habitabat, vir  prudent`
- **backup_v150_20260606_113934** #39 (tokens=274): `Creiisa eos sequebatur. lta per tenebras vadunt, et  245 Aeneam, quem diidum neq`
- **backup_v150_20260606_113934** #231 (tokens=256): `tor in Capitolio epulaberis! Sequere! Cum equite - ut  prius venisse quam ventur`
- **backup_v150_20260606_113934** #9 (tokens=182): `marmore pulcherrimo factis sustinetur; intus in cella,  post fores auro opertas,`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #166 (tokens=289): `CAP. XLV  adulterium -in = facinus  coniugii violandi  pudicitia -aef < pudicus `
- **backup_v150_20260606_113934** #406 (tokens=257): `PENSVM C CAP. LV  deterior  deterrimus  pronu s  stabilis  sempit ernu s  ventit`
- **De Rerum Natura (Lucretius 拉语版)** #343 (tokens=225): `Ergo videmus paucás res necessarias esse ad corpoream nàtüram, ut detrahant homi`
- **backup_v150_20260606_113934** #336 (tokens=223): `GRAMMATICA LATINA PENSVM A CAP. LII  Q. S ervflius Caepio:  cos. anno 106a . C. `
- **Wheelock's Latin 7e** #2456 (tokens=186): `1. Dehinc petet à frátre meo et soróre ut occásiónem carpant et in urbem quam ce`
- *...还有 25 段*

## Cap.31 (FR Cap.XXXI)

**数据**: 新词 423 / 累计 8872 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #59 (tokens=298): `95 arborum occultat; ipse uno Achate comitatus graditur  duo tela manu gerens. C`
- **backup_v150_20260606_113934** #64 (tokens=282): `CAP. XXXIX  extrema loca  si in (ali)quibus silvis aut  urbibus  e-rigere (animu`
- **backup_v150_20260606_113934** #400 (tokens=272): `CAP. LV  quo(+ com)= uteo(uteo  modo)  visum esse R. in eo colle  qui.. . vocatu`
- **backup_v150_20260606_113934** #334 (tokens=271): `CAP. LII  'uti fortem animum gererent: saepe antea a paucis stre­ nuis adversum `
- **backup_v150_20260606_113934** #416 (tokens=268): `CAP. LVI  tanto nomine : etsitant6  nomineappellatur  Caucasus -i m: mons  Asiae`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader for Lower Forms (Hardy 1889)** #467 (tokens=258): `statim agnovit hunc inter omnes. Quum instaret ille, tandem hie, Venalis est, in`
- **backup_v150_20260606_113934** #402 (tokens=235): `CAP. LV  invenire = excogitare,  instituere  caerimonia -ae f = ritus  celebrita`
- **backup_v150_20260606_113934** #308 (tokens=208): `PENSVM C CAP. LI  eloquens  perniciosu s  friimentarius  seditiosus  modestus  a`
- **Latin Reader (Reynolds)** #604 (tokens=176): `Helvétii eorum finis populàrentur: ita sé omni tempore dé populo Rómánó meritos `
- **Wheelock's Latin 7e** #2985 (tokens=152): `atque amantissimós rei püblicae* viros, ad mé vocàvi, rem exposui, quid fieri? p`
- *...还有 25 段*

## Cap.32 (FR Cap.XXXII)

**数据**: 新词 470 / 累计 9342 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 2, 2e** #1026 (tokens=297): `Imperative singular       para                     moné                      reg`
- **backup_v150_20260606_113934** #118 (tokens=289): `CAP. XLIII  (fratres ) tri-geminI = tres  eodem die nati  morte : ob mortem  ( c`
- **backup_v150_20260606_113934** #397 (tokens=287): `multorum, nec una hominis vita, sed aliquot constituta  saeculis et aetatibus. N`
- **backup_v150_20260606_113934** #141 (tokens=286): `tus locus est. Loca divisa patribus equitibusque ubi  spectacula sibi facerent, `
- **Oxford Latin Course Part 3, 2e** #1337 (tokens=282): `Passive Indicative Ist conjugation          2nd conjugation         3rd conjugat`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #303 (tokens=253): `CIVITAS DILACERATA 270 tantum virium in senatii haberet. Et continuato in alte­ `
- **Oxford Latin Course Part 3, 2e** #460 (tokens=213): `appellaret Caesarem Augustum. tandem precibus senàtorum cessit ^ precibus... ces`
- **Via Latina: Easy Latin Reader (Collar 1897)** #336 (tokens=208): `miserant, qui eum certiorem facerent, nisi Alcibiadem sus- tulisset, nihil earum`
- **Latin Reader (Reynolds)** #536 (tokens=204): `rum auxilio Aedui victi et coácti sunt Sequanis obsidés dare et iüráre sésé nequ`
- **backup_v150_20260606_113934** #382 (tokens=164): `CAP. LIV  Caesar vacuam urbem ingressus dictatorem se fecit. 20  Inde Hispanias `
- *...还有 25 段*

## Cap.33 (FR Cap.XXXIII)

**数据**: 新词 476 / 累计 9818 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 2, 2e** #1024 (tokens=369): `Active Ist conjugation         2nd conjugation       3rd conjugation        4th `
- **backup_v150_20260606_113934** #104 (tokens=295): `CAP. XLII  aegre = magno cum  labore, vix  e-vadere  iniiiria mulierum = i.  mul`
- **backup_v150_20260606_113934** #134 (tokens=288): `CAP. XLIV  regnum agere = regnare  memor : simile  in populò cum novò  tum feròc`
- **backup_v150_20260606_113934** #91 (tokens=277): `educati erant urbem condere. Deinde ob cupiditatem  regnI foedum certamen ortum `
- **backup_v150_20260606_113934** #163 (tokens=273): `committere ausus, duòs filios per ignotas ea tempestate  175 terras, ignòtiòra m`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #130 (tokens=290): `PENSVM A PENSVM B CAP. XLIII  Vociibula nova:  spatium  dictator  stativa  indol`
- **backup_v150_20260606_113934** #290 (tokens=281): `PENSVM B CAP.L  navalia  miseratio  clementia  mercatura  lembus  posticum  mace`
- **backup_v150_20260606_113934** #301 (tokens=276): `Gracchi et légés agriiriae  58 Tib. Sempronius Gracchus tribunus plebis, cum le-`
- **Latin Reader (Reynolds)** #382 (tokens=195): `ternus liberis est avunculus. Fràter paternus eis patruus est. Liberi Roómàni pa`
- **Latin Reader (Reynolds)** #684 (tokens=181): `Primo autem vére tempestüs caléscebat. Omnia longo 5rigore hiemis solvuntur. Ini`
- *...还有 25 段*

## Cap.34 (FR Cap.XXXIV)

**数据**: 新词 520 / 累计 10338 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #56 (tokens=290): `CAP. XXXIX  haec secum dfxit  me-nenonposse? = non­ ne ego possum?  dis-icere-ie`
- **backup_v150_20260606_113934** #161 (tokens=289): `54 Inde Sex. Tarquinius cònsiliis publicis interesse coe- pit. Ibi, cum 'de alii`
- **backup_v150_20260606_113934** #86 (tokens=278): `CAP. XLI  nòbilitas -atisf < nòbilis  bello (dat) paratus = ad  bellum paratus  `
- **backup_v150_20260606_113934** #417 (tokens=274): `redierint eandemque t6tius caeli discripti6nem longis  intervallis rettulerint, `
- **backup_v150_20260606_113934** #62 (tokens=273): `CAP. XXXIX  quis locus = quf locus  Achates, voc -e  laudi: factis laudandis,  g`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **catilina** #254 (tokens=181): `infestam rei püblicae pestem toties iam effügimus. Non est saepius in üno homine`
- **Wheelock's Latin Reader** #1199 (tokens=149): `^Haec una salutis est via, L. Paule, quam difficilem in- festamque cives tibi ma`
- **Hobbitus Ille (Tolkien 拉语版)** #988 (tokens=144): `tunc magna aranea, quae eum dormitantem alligando occupata erat, a tergo eius ue`
- **Latin Reader for Lower Forms (Hardy 1889)** #261 (tokens=123): `Honorius, inclinante Romana potestate, imperator factus est. Hie autem summo loc`
- **Reading Latin: Text (2e)** #425 (tokens=121): `utrimque igitur nunc grauida est Alcumena — et e uiro et €é summo Ioue. mox tame`
- *...还有 25 段*

## Cap.35 (FR Cap.XXXV)

**数据**: 新词 336 / 累计 10674 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 3, 2e** #1335 (tokens=369): `Active Indicative -—            Ist conjugation           2nd conjugation       `
- **backup_v150_20260606_113934** #45 (tokens=288): `CAP. XXXVIII  constituerunt. Ergo uhi primum ventus secundus fuit,  iterum in al`
- **backup_v150_20260606_113934** #131 (tokens=278): `PENSVM C sos - [ = oppugnarent].  Cum duo RomanI - [ = morientes] concidissent, `
- **backup_v150_20260606_113934** #275 (tokens=263): `thracam traiecisse', profectus a Pella consul quartis cas­ tris Amphipolim perve`
- **backup_v150_20260606_113934** #250 (tokens=261): `CAP. XLIX  obitus -us m ( < obire )  =mors  suf-ficere-fecisse-fectum  = loco al`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Oxford Latin Course Part 3, 2e** #1336 (tokens=313): `Subjunctive Ist conjugation           2nd conjugation        3rd conjugation    `
- **backup_v150_20260606_113934** #82 (tokens=224): `PENSVM A PENSVM B CAP. XL  Vocabula nova:  coniugium  fulmen  cinis  potentia  v`
- **backup_v150_20260606_113934** #423 (tokens=211): `PENSVM C Qui rem horribilem videt-. - est amor deorum, patriae,  parentum. Annus`
- **Hobbitus Ille (Tolkien 拉语版)** #27 (tokens=210): `aut supra Collem aut trans Aquam inueniri potuit, aedificauit, et ibi ad supremo`
- **backup_v150_20260606_113934** #384 (tokens=197): `PENSVM B CAP. LIV  desiderium  pr6gressi6  misericordia  offènsio  incommodum  d`
- *...还有 25 段*

## Cap.36 (RA Cap.XXXVI)

**数据**: 新词 1943 / 累计 12617 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #160 (tokens=297): `CAP.XLV  talentum: Graecorum  pondus statiitum max­ imum [26 kg]  lentius spe: l`
- **backup_v150_20260606_113934** #63 (tokens=290): `QuI postquam ad reginam adductI sunt, Ilioneus,  maximus eorum, sic orsus est: "`
- **backup_v150_20260606_113934** #68 (tokens=290): `PENSVM B CAP.XXXIX  pomus  tridens  cervus  praeda  rabies  discrimen  rupes  ap`
- **backup_v150_20260606_113934** #364 (tokens=285): `CAP. LIV  Quare, si propter socios, nulla ipsi iniuria lacessiti, 14  maiores no`
- **backup_v150_20260606_113934** #110 (tokens=281): `CAP. XLII  [anno 235 a. C.]  Punicus -a -um = Kar- thaginiensi s  Actiacus -a -u`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #154 (tokens=304): `CAP. XLIV  senectiis  parricidium  furor  praec6  suffragium  fautor  licentia  `
- **backup_v150_20260606_113934** #357 (tokens=249): `PENSVM B PENSVM C (10) urbs > -; lùsculum >-;Troia> -; Alba>-;  (11) vicus > -; `
- **backup_v150_20260606_113934** #292 (tokens=208): `SCIPIO AEMILIANVS CAPITVLVM VNVM ET QVINQVAGESIMVM CAP. LI  Cn. f. = Gnaei filiu`
- **backup_v150_20260606_113934** #405 (tokens=195): `GRAMMATICA LATINA PENSVM A PENSVM B De vocabulis f aciendis  (D) Nomina Jeminina`
- **backup_v150_20260606_113934** #383 (tokens=184): `GRAMMATICA LATINA PENSVM A De vocabulis f aciendis  620 (C) Nomina e verbis  Nom`
- *...还有 25 段*

## Cap.37 (RA Cap.XXXVII)

**数据**: 新词 1391 / 累计 14008 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #42 (tokens=304): `CAP. XXXVII  famulus  ras  aura  socius  niimen  fèstus  profugu s  benignus  di`
- **backup_v150_20260606_113934** #32 (tokens=295): `CAP.XXXVII  complectl -plexum  tener -a -um = mollis et  tenuis , invalidus  cor`
- **backup_v150_20260606_113934** #168 (tokens=282): `CAP. XLV  profecti sunt  qua-cumque = ubi­ cumque  simuiatque  tribiinus -i m: t`
- **backup_v150_20260606_113934** #41 (tokens=281): `PENSVM A PENSVM B De ctisu dativo  Aedes Castoris sacrata est di- Castor- et Pol`
- **backup_v150_20260606_113934** #78 (tokens=278): `CAP. XL  quin + imp = age  avene : prohibe  discessus -us m  < discedere  Quin m`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #1587 (tokens=171): `Quamquam autem plüres homines mortui suprà alios inhumata in terrà iacebant, tam`
- **Via Latina: Easy Latin Reader (Collar 1897)** #317 (tokens=155): `Neque véro his rébus tam amici Alcibiadi sunt facti quam timore ab eo alienati. `
- **Reading Latin: Grammar (2e)** #1598 (tokens=125): `— 168                                                                           `
- **Pro Patria (Sonnenschein 1907)** #54 (tokens=122): `Ir. Primo anno imperii sui Agricola in Cam- bria bellavit, ubi magnam victoriam `
- **Via Latina: Easy Latin Reader (Collar 1897)** #320 (tokens=122): `His cum obviam üniversa civitas in Piraeum déscendis- set, tanta fuit omnium exs`
- *...还有 25 段*

## Cap.38 (RA Cap.XXXVIII)

**数据**: 新词 811 / 累计 14819 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #99 (tokens=278): `15 Civitate ita aucta, Ròmulus centum senatòres creavit,  sive quia is numerus s`
- **backup_v150_20260606_113934** #204 (tokens=267): `CAP. XLVII  Zéno-onism  Citiénsis -e< Citium,  oppidum CyprI  censorés ad nomen `
- **backup_v150_20260606_113934** #202 (tokens=260): `CAP. XLVII  dictum : imperium  Sophocles -is m  Euripides -is m  tragicus -a -um`
- **backup_v150_20260606_113934** #223 (tokens=259): `torum foede cìvium dabo!" subditisque calcaribus equo  per confertissimam hostiu`
- **backup_v150_20260606_113934** #414 (tokens=255): `CAP. LVI  stelli-fer-era-erum ex altera autem acuté sonent. Quam ob causam summu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #875 (tokens=197): `contendentes ubicumque terra erat graminea atque plana, cum montibus tenebrosis `
- **Second Year Latin (Greenough 1899)** #221 (tokens=167): `6. Sediterum tumultibus? eàrundem gentium dé quibus nàr- ràvimus Cyrus in illás `
- **Reading Latin: Text (2e)** #580 (tokens=154): `ALC.         immo post mecum illa7nocte cenauisti et cubuisti et. . .           `
- **Wheelock's Latin Reader** #625 (tokens=131): `Ex quattuor autem locis in quos honesti naturam vimque divisimus, primus ille, q`
- **Latin Reader for Lower Forms (Hardy 1889)** #169 (tokens=112): `Croesus rex Lydorum, beneficiis ab Alemaeone Athen- iensi acceptis, eum ad se Sa`
- *...还有 25 段*

## Cap.39 (RA Cap.XXXIX)

**数据**: 新词 1241 / 累计 16060 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #149 (tokens=307): `CAP. XLIV  ipsae longe dispares moribus. Ferox Tullia, quae Ar- runti Tarquinio `
- **backup_v150_20260606_113934** #310 (tokens=304): `CAP. LII  per-manere  Masi nissa  Micipsa Gulussa Masta- h nati  Adher- Hiem- Iu`
- **backup_v150_20260606_113934** #215 (tokens=277): `pus ab apparatu operum ac munitionum nihil cessatum.  ltaque acrius de integro c`
- **backup_v150_20260606_113934** #143 (tokens=276): `les collibus interiectas cloacis in Tiberim ductis siccat,  et aedis in Capitoli`
- **backup_v150_20260606_113934** #378 (tokens=263): `CAP. LIV  Q. Fabio Maximo Cunctii­ ton  M. ClaudioMarcello ,qui  spoliaopima III`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #1096 (tokens=169): `Gallisque ad visenda loca praemissis, castra quam extentissima potest valle loca`
- **Cambridge Latin Course 3** #1245 (tokens=143): `SINGULAR              masculine — feminine — neuter       masculine — feminine  `
- **Cambridge Latin Course 4** #348 (tokens=132): `protinus Aeoliis Aquilonem claudit in antris.* emittitque Notum; madidis Notus e`
- **catilina** #464 (tokens=132): `Rem püblicam, Quirités, vitamque omnium vestrum, bona, fortünas, coniuges libero`
- **Latin by the Natural Method (W.G. Most 1957)** #1054 (tokens=130): `Véniunt in silvas (forest) cédrinas (cedar) occi- dentáles. Ibi terríbile invéni`
- *...还有 25 段*

## Cap.40 (RA Cap.XL)

**数据**: 新词 1028 / 累计 17088 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #245 (tokens=306): `PENSVM B Hannibal puer, cum patri - ut se duceret in Hispaniam, iure  iurando - `
- **backup_v150_20260606_113934** #354 (tokens=302): `CAP. LIII  impunitas -atisf( < im- fluentes iuvenilI quadam dicendi impunita te `
- **backup_v150_20260606_113934** #96 (tokens=286): `PENSVM C CAP. XLI  stabulum  saltus  latro  Insidiae  necessitas  concilium  avu`
- **backup_v150_20260606_113934** #174 (tokens=283): `PENSVM C CAP. XLV  manifestus  pròmptus  imperfectus  anxrns  bn1tus  expers  ca`
- **backup_v150_20260606_113934** #210 (tokens=278): `CAP. XLVIII  ad-igere-egisse-acturn =  cogere; iure iurando a.  = ad ius iurandu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Epitome Historiae Sacrae** #507 (tokens=176): `Iosephum interea à mercatoribus emerat Pütiphar, vir Aegyptius, qui eum praefeci`
- **Wheelock's Latin Reader** #1000 (tokens=157): `Ac nescio an, nimis undique eam minimisque rebus muni- endo, modum excesserint. `
- **ars_amatoria** #1925 (tokens=128): `Nec mora, per medias passis furibunda capillis 710 ÁAvolat, ut thyrso concita Ba`
- **Hobbitus Ille (Tolkien 拉语版)** #382 (tokens=125): `"aestas in locis inferioribus praeterit," Bilbo secum cogitauit, "et faenisicia `
- **Latin Reader for Lower Forms (Hardy 1889)** #323 (tokens=121): `Caesar ad flumen Tamesim in fines Casivellauni exerci- tum duxit; quod flumen un`
- *...还有 25 段*

## Cap.41 (RA Cap.XLI)

**数据**: 新词 842 / 累计 17930 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #201 (tokens=296): `mam conditam, aut non longe amplius, victos esse ab  Atheniensibus Persas memori`
- **backup_v150_20260606_113934** #164 (tokens=287): `CAP.XLV  prae-poten s -entis = prae  aliis potens, potentissi­ mus  ditare=divit`
- **backup_v150_20260606_113934** #304 (tokens=274): `CAP. LI  abs-trahere  faccione: quia factione  iiinctaerat  pollere = valere  di`
- **backup_v150_20260606_113934** #311 (tokens=258): `vim neque insidii:s opprimi: posse hominem tam accep­ tum populàribus, quod erat`
- **backup_v150_20260606_113934** #322 (tokens=249): `CAP. LII  ltalicus -a -um < Italia;  plincolae  defensare = defendere  confidere`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #169 (tokens=197): `325 exsecrantibus quacumque incedebat invocantibusque  parentum Furias viris mul`
- **Wheelock's Latin Reader** #687 (tokens=182): `(a) The dual nature of the soul: (1) appetite; (2) reason, to govern the appetit`
- **Via Latina: Easy Latin Reader (Collar 1897)** #287 (tokens=142): `Plürima indicia futüri periculi obtulerant dii immor- talés. Uxor Calpurnia, ter`
- **Reading Latin: Text (2e)** #2439 (tokens=131): `aut ubi nox abiit nec tamen orta dies. illa uerecundis! lüx est praebenda ! puel`
- **Latin Reader for Lower Forms (Hardy 1889)** #158 (tokens=109): `Augusto post Áctiacam victoriam Romam reverso inter gratulantes occurrit opifex `
- *...还有 25 段*

## Cap.42 (RA Cap.XLII)

**数据**: 新词 1258 / 累计 19188 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 2

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #138 (tokens=295): `CAP. XLIV  Demaratus -im  Corinthius -a -um < Co­ rinthus; m civis C.  sediti6 -`
- **backup_v150_20260606_113934** #257 (tokens=295): `larem cenarent, atque ibi de Hannibale mentione facta  ex iis fmus diceret 'eum `
- **backup_v150_20260606_113934** #114 (tokens=293): `PENSVM B Ct\l'. XLII  columba  agna  commodum  tubicen  pignus  socer  agrestis `
- **backup_v150_20260606_113934** #147 (tokens=293): `centuriae, quae sine armis stipendia facerent. Secunda  classis intra centum usq`
- **backup_v150_20260606_113934** #153 (tokens=289): `PENSVM A PENSVM B De adverbiis  Tullus legatos Albanos bland- ac benign- recepit`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #337 (tokens=272): `PENSVM B (2) comes > -; minae > -; gloria > -; dominus > -;  mora > -; testis > `
- **Epitome Historiae Sacrae** #972 (tokens=207): `Madianitis superatis, Philistae1 coeperant multa incommoda Hebraeis affligere, q`
- **Hobbitus Ille (Tolkien 拉语版)** #169 (tokens=200): `gemmasque hominibus et dryadibus et nanis subripiunt, ut intellegis, ubicumque e`
- **Hobbitus Ille (Tolkien 拉语版)** #167 (tokens=180): `expulsa, cum diuitiis omnibus atque instrumentis suis, ad hunc Montem in tabula `
- **Cambridge Latin Course 4** #1077 (tokens=148): `decurrere ad litus. hi moles, hi proximas scaphàs conscendere; alit, quantum cor`
- *...还有 25 段*

## Cap.43 (RA Cap.XLIII)

**数据**: 新词 1055 / 累计 20243 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #130 (tokens=290): `PENSVM A PENSVM B CAP. XLIII  Vociibula nova:  spatium  dictator  stativa  indol`
- **backup_v150_20260606_113934** #284 (tokens=264): `CAP. L  praeses-idis mlf = ciistos  excidium: Corinthusxxr  annrs post a Romanrs`
- **backup_v150_20260606_113934** #167 (tokens=261): `Cultrum, quem sub veste abditum habebat, eum in  corde defigit, prolapsaque in v`
- **backup_v150_20260606_113934** #270 (tokens=258): `CAP. L  circu-ire = circumire  vertex -icis m = pars  summa, culmen  ne qua = ne`
- **backup_v150_20260606_113934** #368 (tokens=252): `CAP. LIV  re-creare = riirsusvigen - tum erexit perditumque recreavit. Cuius in `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #25 (tokens=177): `taciti et cito se auferant quandocumque talis ingens et stulta gens qualis tu et`
- **Reading Latin: Text (2e)** #118 (tokens=157): `sed furcifer. SERVVS ego otiosus non sum, Pamphila. nam hodie Démaenetus, dominu`
- **Latin by the Natural Method (W.G. Most 1957)** #1114 (tokens=141): `Prima fácie (at first sight) narrátio Babylónica simíl- lima vidétur esse narrat`
- **Epitome Historiae Sacrae** #156 (tokens=137): `Cum hominum vitia validiores fierent, Deus eorum generem pluvia de caelo cadente`
- **Hobbitus Ille (Tolkien 拉语版)** #385 (tokens=118): `numquam Bilbo aliquid talis generis aut uiderat aut mente conceperat. fuerunt in`
- *...还有 25 段*

## Cap.44 (RA Cap.XLIV)

**数据**: 新词 1419 / 累计 21662 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #154 (tokens=304): `CAP. XLIV  senectiis  parricidium  furor  praec6  suffragium  fautor  licentia  `
- **backup_v150_20260606_113934** #351 (tokens=279): `cens M. Antonium et Q. Hortensium, qui tum arte oratoria  excellebant, assidue a`
- **backup_v150_20260606_113934** #158 (tokens=275): `CAP. XLV  quidspei(gen): quaro  spero  "simeauditis,dorouro  orones hinc abibimu`
- **backup_v150_20260606_113934** #300 (tokens=269): `CAP. LI  luxuria -aef = luxus  disciplina<-> Iicentia  re-cidere = adimere  (cae`
- **backup_v150_20260606_113934** #295 (tokens=266): `CAP. LI  ampia mano saltum iniquum insèderat), suasit primo Scipio suasit  consu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader for Lower Forms (Hardy 1889)** #480 (tokens=232): `involare. Atque in hoc genere reperiuntur quidam mire dextri; dicas esse Mercuri`
- **backup_v150_20260606_113934** #152 (tokens=207): `FILIA IMPIA CAP. XLIV  mercede : praemio  solere solitum esse  ex-stimuliire = s`
- **Wheelock's Latin Reader** #1109 (tokens=130): `Ventum deinde ad multo angustiorem rupem atque ita rectis saxis ut aegre expedit`
- **Hobbitus Ille (Tolkien 拉语版)** #1092 (tokens=121): `die quodam, Bilbo inquirens atque errans rem utilissimam inuenit: portas magnas `
- **First Latin Reader (Chickering)** #1780 (tokens=119): `trueidàtum (xx)..............massacre (caedo, crüdéliter in- *erficio). tü, tui `
- *...还有 25 段*

## Cap.45 (RA Cap.XLV)

**数据**: 新词 1222 / 累计 22884 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #260 (tokens=307): `PENSVM B CAP. XLIX  Vocabula nuva:  natio  heredita s  suspicio  puerulus  obitu`
- **backup_v150_20260606_113934** #166 (tokens=289): `CAP. XLV  adulterium -in = facinus  coniugii violandi  pudicitia -aef < pudicus `
- **backup_v150_20260606_113934** #333 (tokens=259): `CAP. LII  104 Marius, postquam Cirtam rediit, mandata Bocchi:  cognoscit. Legati`
- **backup_v150_20260606_113934** #226 (tokens=253): `CAP. XLVIII  [anno 216 a. C.]  alicui succedere = in  locum alicuius s.  callidu`
- **backup_v150_20260606_113934** #266 (tokens=233): `CAP. L  re-petere = iterare  raptim = celeriter  prae-occupare  sensus -us m < s`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Second Year Latin (Greenough 1899)** #146 (tokens=142): `làris cum virginali verécundià. Ut illa patris cervicibus! inhaerébat! Ut nós am`
- **Conversational Latin for Oral Proficiency** #6247 (tokens=119): `war (against or with) bell-um -i1n (contrà or advérsus (4 acc) or cum (* abl); b`
- **Reading Latin: Grammar (2e)** #155 (tokens=114): `Démaenetus coquos et tibicinas uidet. ad nüptias filiae ueniunt. in aedis Démaen`
- **Latin Reader for Lower Forms (Hardy 1889)** #156 (tokens=108): `Asinos igitur utribus vino plenis instructos per viam publicam agitabat; quum pr`
- **Oxford Latin Course Part 3, 2e** #435 (tokens=105): `Cleopàtrae persuadere ut sé dederet. cum Cleopátra noluisset turrem relinquere, `
- *...还有 25 段*

## Cap.46 (RA Cap.XLVI)

**数据**: 新词 1251 / 累计 24135 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 2

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #301 (tokens=276): `Gracchi et légés agriiriae  58 Tib. Sempronius Gracchus tribunus plebis, cum le-`
- **backup_v150_20260606_113934** #277 (tokens=263): `erunt. Renovataque laetitia, cum consul edixisset 'ut  omnes aedes sacrae aperir`
- **backup_v150_20260606_113934** #307 (tokens=256): `PENSVM B cadere >-;con- + loquI > -; con-+ponere >-;con- +  regere > -; con- + o`
- **backup_v150_20260606_113934** #208 (tokens=246): `PENSVM C CAP. XLVII  sacrarium  quindecimvirI  iiis iiirandum  scriptum  incònsp`
- **backup_v150_20260606_113934** #353 (tokens=246): `vocis et commutato genere dicendI me et periculum  vitare posse et temperatius d`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Forum - Lectiones Latinitatis Vivae (Polis)** #2449 (tokens=193): `NICOLAUS: Alexander esne mihi amicus? ALEXANDER : Quid tibi cürae est, Nicolae? `
- **backup_v150_20260606_113934** #420 (tokens=171): `INTEGER VITAE CAP. LVI  imegervitae: quivitam  integram (: innocentem)  agit [Ex`
- **backup_v150_20260606_113934** #198 (tokens=153): `RES GRAECAE SCRIPTORES  GRAECI SCRIPTORES  ROMANI RES ROMANAEanno  a.e.  750 Rom`
- **Second Year Latin (Greenough 1899)** #183 (tokens=142): `Tandem cum adpararétur prandium faeneràátori, deside- ráta* est olla. Hic iürgiu`
- **Cambridge Latin Course 4** #1047 (tokens=127): `placuit Neroni calliditas Aniceti; praeterea occasio optima rei temptandae adera`
- *...还有 25 段*

## Cap.47 (RA Cap.XLVII)

**数据**: 新词 595 / 累计 24730 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Hobbitus Ille (Tolkien 拉语版)** #1073 (tokens=129): `neque, dum captiuos in siluam deducunt, eum, qui longe post lucem facum suarum a`
- **Wheelock's Latin Reader** #536 (tokens=129): `Mihi autem amissis ornamentis iis, quae ipse commemoras, quaeque eram maximis la`
- **Wheelock's Latin Reader** #589 (tokens=118): `Sed cum statuissem scribere ad te aliquid hoc tempore (multa posthac), ab eo ord`
- **Pro Patria (Sonnenschein 1907)** #182 (tokens=116): `S.V.B.E.E.V. Litterae tuae me magnopere delectaverunt. De Adamantopoli obsidione`
- **Wheelock's Latin 7e** #3770 (tokens=107): `5. Facillima saepe nón sunt optima. 6. Difficilia saepe sunt maxima. 7. Meliora `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin 7e** #1275 (tokens=77): `6. Itaque id genus lüdórum levium, quod à multis familiis laudabàtur, nós ipsi n`
- **ars_amatoria** #468 (tokens=68): `dominus agri — qui dgrum possidet sterilis -e €» fertilis sic lüsor, né pecimiam`
- **Pugio Bruti (Polis)** #3 (tokens=56): `Capitulum sextum decimum... Capitulum septimum decimum . Capitulum duodévicésimu`
- **A First Latin Reader (Nutting)** #1472 (tokens=54): `armis signisque militàribus, magis dé reliqua fuga quam dé castrorum defensione `
- **The Revised Latin Primer (Kennedy)** #170 (tokens=50): `Stem . flos-               ópüs-                 erüs- fior-               ópér-`
- *...还有 25 段*

## Cap.48 (RA Cap.XLVIII)

**数据**: 新词 2085 / 累计 26815 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #246 (tokens=275): `PENSVM C CAP. XLVIII  quassare  procidere  irritare  gratificari  succingere  ci`
- **backup_v150_20260606_113934** #265 (tokens=267): `milia armatorum haberet neve elephantum ullum; bel- 45 lum extra Macedoniae fine`
- **backup_v150_20260606_113934** #256 (tokens=264): `CAP. XLIX  -undum = -endum  venenatus -a -um =  venenum gerens  serpens-entisf =`
- **Oxford Latin Course Part 3, 2e** #77 (tokens=258): `discessit; Brütum in Asiam secütus est.' Flaccus 'quid dicis, carissima?' inquit`
- **Wheelock's Latin Reader** #873 (tokens=227): `Sed (saepe enim redeo ad Scipionem cuius omnis sermo erat de amicitia) querebatu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Made Simple** #1737 (tokens=121): `His ego nec metas rerum nec tempora pono; imperium sine fine dedi. Quin aspera J`
- **Hobbitus Ille (Tolkien 拉语版)** #896 (tokens=116): `"ja est, si ducenta milia passuum e uia ad septentrionem, et bis tantum ad merid`
- **ars_amatoria** #856 (tokens=113): `magicus -a -um; ars magica: quà res contrà nàtüram fieri videntur dé-currere — c`
- **Hobbitus Ille (Tolkien 拉语版)** #1022 (tokens=107): `se minimum temporis habere sciuit, antequam araneae, taedio affectae, ad arbores`
- **Second Year Latin (Greenough 1899)** #317 (tokens=104): `4. Déleétis? Teutonibus C. Marius in Cimbros sé convertit. Qui cum ex alià parte`
- *...还有 25 段*

## Cap.49 (RA Cap.XLIX)

**数据**: 新词 670 / 累计 27485 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #402 (tokens=235): `CAP. LV  invenire = excogitare,  instituere  caerimonia -ae f = ritus  celebrita`
- **De Rerum Natura (Lucretius 拉语版)** #600 (tokens=217): `nos carpimus et gustamus omnes tuas sententias aureds; aureas, inquam, et quae s`
- **Epitome Historiae Sacrae** #372 (tokens=188): `Cum in matrimonium eam Isaacus düxisset, üno                     duo fili1 nàti `
- **catilina** #254 (tokens=181): `infestam rei püblicae pestem toties iam effügimus. Non est saepius in üno homine`
- **Pro Patria (Sonnenschein 1907)** #91 (tokens=151): `litore portus stabat. Intra muros castelli est area lata. In media area fundamen`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **backup_v150_20260606_113934** #259 (tokens=179): `GRAMMATICA LATINA PENSVM A neminem loca elegantius cepisse, praesidia disposuiss`
- **Latin Reader (Reynolds)** #875 (tokens=118): `SiNGULAR a. Masculine or Feminine            b. Neuter Base                  Ste`
- **Latin for Beginners (D'Ooge 另一版)** #1395 (tokens=99): `ADJECTIVES FIRST AND SECOND DECLENSIONS               THIRD DECLENSION dénsus   `
- **Latin Reader for Lower Forms (Hardy 1889)** #242 (tokens=83): `Tradunt Aterium Rufum equitem Romanum somnio singulari admonitum esse de rebus f`
- **Latin Reader for Lower Forms (Hardy 1889)** #244 (tokens=75): `Daphitas eius studii erat, quod qui profitentur sophistae vocantur, homo ineptae`
- *...还有 25 段*

## Cap.50 (RA Cap.L)

**数据**: 新词 1523 / 累计 29008 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 3

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #290 (tokens=281): `PENSVM B CAP.L  navalia  miseratio  clementia  mercatura  lembus  posticum  mace`
- **Hobbitus Ille (Tolkien 拉语版)** #867 (tokens=231): `mannos omnibus prouisurum esse, et equum Gandalpho, iter ad siluam faciendi caus`
- **De Rerum Natura (Lucretius 拉语版)** #59 (tokens=203): `Incipit Lucretius opus suum mirabili quodam carmine, cuius versibus Venerem, alm`
- **De Rerum Natura (Lucretius 拉语版)** #1240 (tokens=183): `et capiebant multa, et fugiebant pauca, quaerentes latebras: et similes apris hi`
- **Wheelock's Latin Reader** #1000 (tokens=157): `Ac nescio an, nimis undique eam minimisque rebus muni- endo, modum excesserint. `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #1166 (tokens=207): `gubernatoribus loquentibus auscultans et ex fragmentis patefactis certior factus`
- **Pro Patria (Sonnenschein 1907)** #62 (tokens=138): `quam rebelliones populorum barbarorum. Pax ila Romana etiam populis subiectis ut`
- **Hobbitus Ille (Tolkien 拉语版)** #97 (tokens=136): `purgabantur et tute suis locis ponebantur quam celerrime, dum Mhobbitus se in me`
- **Ecce Romani IIB** #1408 (tokens=128): `quártus, -a, -um, fourtb (38) quártus décimus, -a, -um, fourteentb (38) quási, a`
- **Latin Reader for Lower Forms (Hardy 1889)** #265 (tokens=119): `Cum M. Antonius, quidquid mari aut terra aut etiam aere gigneretur, ad satiandam`
- *...还有 25 段*

## Cap.51 (RA Cap.LI)

**数据**: 新词 812 / 累计 29820 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #303 (tokens=253): `CIVITAS DILACERATA 270 tantum virium in senatii haberet. Et continuato in alte­ `
- **backup_v150_20260606_113934** #395 (tokens=227): `commiini ac potestate careat; et cum omnia per popu- lum geruntur quamvis iiistu`
- **backup_v150_20260606_113934** #292 (tokens=208): `SCIPIO AEMILIANVS CAPITVLVM VNVM ET QVINQVAGESIMVM CAP. LI  Cn. f. = Gnaei filiu`
- **backup_v150_20260606_113934** #383 (tokens=184): `GRAMMATICA LATINA PENSVM A De vocabulis f aciendis  620 (C) Nomina e verbis  Nom`
- **Pro Patria (Sonnenschein 1907)** #134 (tokens=146): `36. Magnum periculum belli esse magister noster dicit. * In litteris" inquit **q`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Second Year Latin (Greenough 1899)** #99 (tokens=112): `dam asinum! condüxerat, quó Athenis Megaram veherétur. Media fere? vià cum aestu`
- **Latin Reader for Lower Forms (Hardy 1889)** #215 (tokens=93): `Apis quum quondam, ut diis sacra faceret, Olympum accessisset, Iovi mellis donum`
- **Hobbitus Ille (Tolkien 拉语版)** #438 (tokens=71): `nec quicquam aliud agi potuit; quod gobelinis non placuit. festinantes magnis uo`
- **Wheelock's Latin Reader** #1093 (tokens=71): `Hannibal a Druentia campestri maxime itinere ad Alpes cum bona pace incolentium `
- **Hobbitus Ille (Tolkien 拉语版)** #1282 (tokens=64): `Smaug iacebat, alis replicatis sicut uespertilio immensus, in latus unum partim `
- *...还有 25 段*

## Cap.52 (RA Cap.LII)

**数据**: 新词 1458 / 累计 31278 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #337 (tokens=272): `PENSVM B (2) comes > -; minae > -; gloria > -; dominus > -;  mora > -; testis > `
- **backup_v150_20260606_113934** #406 (tokens=257): `PENSVM C CAP. LV  deterior  deterrimus  pronu s  stabilis  sempit ernu s  ventit`
- **backup_v150_20260606_113934** #336 (tokens=223): `GRAMMATICA LATINA PENSVM A CAP. LII  Q. S ervflius Caepio:  cos. anno 106a . C. `
- **Via Latina: Easy Latin Reader (Collar 1897)** #336 (tokens=208): `miserant, qui eum certiorem facerent, nisi Alcibiadem sus- tulisset, nihil earum`
- **Latin Reader (Reynolds)** #674 (tokens=192): `aut nàvis nacti trünsiére aut viribus confisi tránüre con- tendérunt. In his fui`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Second Year Latin (Greenough 1899)** #84 (tokens=126): `etiam," respondet lupus, "pater tuus contuméliosé quondam 15 dixit dé avià meà" `
- **Via Latina: De Lingua et Vita Romanorum** #26 (tokens=119): `I. Methodus et via, quibus ütimur, linguae üsü nituntur: lingua enim Latina Lati`
- **Hobbitus Ille (Tolkien 拉语版)** #942 (tokens=100): `circum quattuor dies e flumine incantato ad partem quamdam aduenerunt in qua arb`
- **Hobbitus Ille (Tolkien 拉语版)** #590 (tokens=95): `Gollum se retrorsum iecit et, dum hobbitus superuolat, eum prehendit, sed tardiu`
- **Hobbitus Ille (Tolkien 拉语版)** #171 (tokens=92): `"pauci nostri qui foris longe afuimus abditi consedimus atque  lacrimauimus, et `
- *...还有 25 段*

## Cap.53 (RA Cap.LIII)

**数据**: 新词 832 / 累计 32110 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 3, 2e** #58 (tokens=254): `festinàvit cum Pompeio ut locum sacrum spectaret ubi Apollo r nátus erat. cum om`
- **backup_v150_20260606_113934** #357 (tokens=249): `PENSVM B PENSVM C (10) urbs > -; lùsculum >-;Troia> -; Alba>-;  (11) vicus > -; `
- **backup_v150_20260606_113934** #384 (tokens=197): `PENSVM B CAP. LIV  desiderium  pr6gressi6  misericordia  offènsio  incommodum  d`
- **backup_v150_20260606_113934** #342 (tokens=163): `CAP. LIII  Samos  •Adramyttium  •Pcrgamum  Mg;nesia  • Asia  •Ephesus  Mare Pont`
- **Pro Patria (Sonnenschein 1907)** #132 (tokens=118): `incolunt, Coloniam nostram Africanam quondam incolebant. Í Sed abhinc annos quin`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Reading Latin: Grammar (2e)** #1146 (tokens=186): `ad Ianitorem, uirum summae grauitatis, Lampsaceni eum dedüxerunt. iste autem — 5`
- **Cambridge Latin Course 2** #643 (tokens=118): `multus sanguis ex vulnere Barbilli efflu&bat. Phormio, qui servos        vulnere`
- **Wheelock's Latin 7e** #4978 (tokens=95): `Aug., St. Augustine Conf., Confessions Caes., Caesar B Civ, Bellum Civile B Gall`
- **Latin Reader for Lower Forms (Hardy 1889)** #178 (tokens=86): `Protagoras sophista acerrimus cum Evathlo discipulo simultatem gessit: super pac`
- **Hobbitus Ille (Tolkien 拉语版)** #1175 (tokens=85): `cum primum ratis cuparum aspecta erat, lintres remis e molibus oppidi egressae s`
- *...还有 25 段*

## Cap.54 (RA Cap.LIV)

**数据**: 新词 1170 / 累计 33280 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader (Reynolds)** #621 (tokens=198): `véra: Ipsum esse Dumnorigem, summà& audácià, magn& apud plebem propter liberalit`
- **Latin Reader (Reynolds)** #604 (tokens=176): `Helvétii eorum finis populàrentur: ita sé omni tempore dé populo Rómánó meritos `
- **Via Latina: Easy Latin Reader (Collar 1897)** #332 (tokens=147): `At Alcibiades, victis Athéniensibus non satis tüta eadem loca sibi arbitráàns, p`
- **Fabulae Faciles (Ritchie 1889)** #329 (tokens=141): `Postridie ejus diei, Jason cum sociis suis, ortà luce, navem deduxit, et tempest`
- **De Rerum Natura (Lucretius 拉语版)** #505 (tokens=136): `Tellus continet in se primordia illa, quibus fit ut fontes, qui fluviorum frigid`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin for Beginners (D'Ooge)** #511 (tokens=123): `BaAsES OR    f princip-                      milit-                       lapid-`
- **Wheelock's Latin Reader** #1618 (tokens=122): `Interim e Vesuvio monte pluribus locis latissimae flammae altaque incendia reluc`
- **Latin Reader for Lower Forms (Hardy 1889)** #173 (tokens=91): `E quibus unus, qui socios retinuerat, rogavit, quamobrem tanta celeritate domum `
- **Ora Maritima (Sonnenschein 1900)** #27 (tokens=83): `7. Inangulohorti sunt ulmi. In ulmis corvi nidificant. Corvos libenter specto, c`
- **Latin for Beginners (D'Ooge)** #517 (tokens=77): `cónsul, m.,    legió, f.,      Ordo, m.,     pater, m., consul       Jegion     `
- *...还有 25 段*

## Cap.55 (RA Cap.LV)

**数据**: 新词 969 / 累计 34249 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #865 (tokens=221): `Quis est—pro deorum fidem atque hominum!— qui velit, ut neque diligat quemquam n`
- **backup_v150_20260606_113934** #405 (tokens=195): `GRAMMATICA LATINA PENSVM A PENSVM B De vocabulis f aciendis  (D) Nomina Jeminina`
- **backup_v150_20260606_113934** #421 (tokens=176): `GRAMMATICA LATINA pone sub curru nimium propinquI  solis, in terra domibus negat`
- **catilina** #316 (tokens=126): `Ibis tandem aliquando quó té iam pridem tua ista cupiditas effrenata ac furiosa `
- **Wheelock's Latin Reader** #506 (tokens=125): `Lippitudinis meae signum tibi sit librari manus et eadem causa brevitatis, etsi `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #1608 (tokens=127): `Deinde etiam pàstor et armentarius quisque et eodem modo robustus agricola regen`
- **Second Year Latin (Greenough 1899)** #179 (tokens=106): `Antónius sacrificus invitàrat ünum atque alterum bellum homunculum forte obvios `
- **Forum - Lectiones Latinitatis Vivae (Polis)** #1975 (tokens=100): `1. Audimus optimam cantátricem.              Jl ———— 2. Quam partem agis ?      `
- **Ecce Romani I** #1005 (tokens=83): `Clusium                                    13 stupeo, -ére, -ui, to be amazed fa`
- **Hobbitus Ille (Tolkien 拉语版)** #1488 (tokens=76): `ut descendebat et praeteribat et iterum circumibat, ignis a textis stramento uel`
- *...还有 25 段*

## Cap.56 (RA Cap.LVI)

**数据**: 新词 778 / 累计 35027 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **backup_v150_20260606_113934** #422 (tokens=220): `PENSVM A PENSVM B CAP. LVI  strophe -aef  Vocabula nooa:  caelites  anfractus  a`
- **De Rerum Natura (Lucretius 拉语版)** #522 (tokens=218): `rauco sonitü terrent, eosdemque tibia cava sono Phrygio agitat: et sacerdotes po`
- **backup_v150_20260606_113934** #423 (tokens=211): `PENSVM C Qui rem horribilem videt-. - est amor deorum, patriae,  parentum. Annus`
- **backup_v150_20260606_113934** #420 (tokens=171): `INTEGER VITAE CAP. LVI  imegervitae: quivitam  integram (: innocentem)  agit [Ex`
- **Hobbitus Ille (Tolkien 拉语版)** #1698 (tokens=141): `itaque proelium ab omnibus inopinatum inierunt; quod Proelium Quinque Exercituum`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Second Year Latin (Greenough 1899)** #82 (tokens=119): `i2. The Wolf and the Lamb.                                dam certàmen! institu&`
- **First Latin Reader (Chickering)** #1519 (tokens=83): `perus). infestus, infesta, infestum (xv)...unsafe (el inimicus). ingenium, ingen`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #1850 (tokens=82): `l. Habet librum in manü suà                             FERREA 2. Cupimus concen`
- **Hobbitus Ille (Tolkien 拉语版)** #1274 (tokens=82): `paulo post Balinus Bilboni "feliciter tibi!" dixit et stetit ubi lineamentum heb`
- **Reading Latin: Text (2e)** #459 (tokens=82): `*ut recordor — nam nihil obliuiscor — nos in otio et pace sumus, sed Téeleboae, `
- *...还有 25 段*
