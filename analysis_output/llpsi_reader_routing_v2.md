# LLPSI 56 章扩展读物路由表 (v3 段级 hybrid 版)

**生成日期**: 2026-06-09 | **覆盖**: FR Cap.1-35 + RA Cap.36-56

## 算法 (v3 极简段级 hybrid)

- **段级切片**: 按空行切分文本为段落
- **叙事过滤**: 拉语词占比≥50%、**token≥15 (v3 新增)**、非标题/非练习题/非词汇表
- **极简评分 (hybrid)**:
  - `full = 1.0`: 在 LLPSI Cap.N 已学词集 `learned_words[N]` 中
  - `partial = 0.5`: 在 LLPSI 56章总词表但未学到
  - `character = 0.7`: 在本段所属书的高频专名(出现≥5次, v3 由 0.3 提升)
  - `score = (full + 0.5*partial + 0.7*character) / total_latin_tokens`
- **已学词集**: 直接扫描 LLPSI OCR 文本重建（而非依赖DB is_new标记）
- **v3 排序键**: `score * log(tokens + 1)` (兼顾分数与长度, 取代纯 token 数)
- **v3 词数硬限制** (确保推荐内容"完整可读"):
  - 📖 流畅: 拉语 token ≥ **15**
  - 💪 挑战: 拉语 token ≥ **20**
  - 📚 节选: 拉语 token ≥ **30**

## 路由规范 (4个维度)

| 标签 | 含义 | 阈值 | 最小词数 |
|------|------|------|----------|
| 📖 流畅 | 学完本章后该段可流畅阅读 | hybrid ≥ 80% | 15 |
| 💪 挑战 | 学完本章后该段可挑战阅读 | hybrid ≥ 70% | 20 |
| 📚 节选 | 学完本章后该段可节选阅读 | hybrid ≥ 50% | 30 |
| 🧩 D段  | D类拉语段 (OCR抽取) | form ≥ 60% | - |

## Cap.1 (FR Cap.I)

**数据**: 新词 204 / 累计 204 词族 | 📖流畅 7 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #1 (tokens=72): `In imperio Romano multae sunt provinciae. Hispania et Gallia sunt provinciae Rom`
- **Fabellae Latinae** #2 (tokens=58): `Quid est Brundisium? Brundisium oppidum est. Quid est Dànuvius? Dànuvius est flu`
- **Via Latina: De Lingua et Vita Romanorum** #5 (tokens=63): `Ecce Làrentia. Larentia femina est. Larentia in Italia habitat. Ea fémina Itala `
- **Fabellae Latinae** #3 (tokens=23): `Quid est Tüsculum? Tüsculum est oppidum Romanum. Estne magnum oppidum? Tüsculum `
- **Via Latina: De Lingua et Vita Romanorum** #6 (tokens=29): `In Európà sunt multa oppida. Alba Longa in Ita- lia est: Alba Longa oppidum Ital`
- *...还有 2 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Fabellae Latinae** #1 (tokens=72): `In imperio Romano multae sunt provinciae. Hispania et Gallia sunt provinciae Rom`
- **Fabellae Latinae** #2 (tokens=58): `Quid est Brundisium? Brundisium oppidum est. Quid est Dànuvius? Dànuvius est flu`
- **Via Latina: De Lingua et Vita Romanorum** #5 (tokens=63): `Ecce Làrentia. Larentia femina est. Larentia in Italia habitat. Ea fémina Itala `
- **Latin by the Natural Method (W.G. Most 1957)** #19 (tokens=100): `Ubi sunt Románi? Románi sunt in urbe Romána. Suntne plebs in urbe Romána? Non. P`
- **Fabellae Latinae** #3 (tokens=23): `Quid est Tüsculum? Tüsculum est oppidum Romanum. Estne magnum oppidum? Tüsculum `
- *...还有 25 段*

## Cap.2 (FR Cap.II)

**数据**: 新词 182 / 累计 386 词族 | 📖流畅 20 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Ecce Romani I** #18 (tokens=53): `Vir quoque est in pictüra, nomine Davus, qui est servus. In Italia sunt multi se`
- **ecce_romani_combined** #7 (tokens=50): `Vir quoque est in pictura, nomine Davus; qui est servus. In Italia sunt 5 multi `
- **Fabellae Latinae** #6 (tokens=24): `Aemilia: "Duo filii et üna filia. Filii mei sunt Màrcus et Quintus, filia mea es`
- **Fabellae Latinae** #8 (tokens=33): `Cornelius: "Duo: ünus filius, Sextus, et üna filia, Cornelia. Parvus est numerus`
- **Fabellae Latinae** #72 (tokens=41): `In villa Iülii multa sunt cubicula parva et magna. Magnum est cubiculum Iülii et`
- *...还有 15 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: De Lingua et Vita Romanorum** #484 (tokens=95): `concitàre 12[II].58 concordia -ae f^ 9[I1].67 condere 3[II].43 condicio -ónis f^`
- **Ecce Romani I** #18 (tokens=53): `Vir quoque est in pictüra, nomine Davus, qui est servus. In Italia sunt multi se`
- **ecce_romani_combined** #7 (tokens=50): `Vir quoque est in pictura, nomine Davus; qui est servus. In Italia sunt 5 multi `
- **Via Latina: De Lingua et Vita Romanorum** #74 (tokens=68): `Ut Làrentia et Faustulus, Romulus Remusque, féminae et viri, puellae et pueri no`
- **Via Latina: De Lingua et Vita Romanorum** #16 (tokens=73): `Larentia nón in oppido, sed in campo habitat. Casa Larentiae nón in oppido est: `
- *...还有 25 段*

## Cap.3 (FR Cap.III)

**数据**: 新词 96 / 累计 482 词族 | 📖流畅 18 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #9 (tokens=42): `Iülia, filia Iülii et Aemiliae, est parva puella laeta quae cantat et ridet. Sed`
- **Fabellae Latinae** #29 (tokens=49): `Medus laetus est et cantat, quia ad amicam suam ambulat. Sed iam tacet Medus. Cü`
- **Fabellae Latinae** #11 (tokens=21): `Aemilia respondet: "Marcus ridet, quia Iülia plorat, et Iülia plorat et té vocat`
- **Fabellae Latinae** #12 (tokens=18): `Iulius Màrcum vocat. Marcus venit et Iülium iratum videt, neque iam ridet puer. `
- **Fabellae Latinae** #10 (tokens=18): `Aemilia Iülium non videt et Syram ancillam interrogat: "Ubi est vir meus? Iülia `
- *...还有 13 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #3 (tokens=87): `Colámbus non fuit puélla. María fuit puélla. Colámbus non fuit planus. Fuit Colá`
- **Dioclēs et Flōra (Polis)** #2 (tokens=83): `Salve! Mihi nomen est Diocles. Puer Graecus sum. Non in Graecià habito. In Graec`
- **Via Latina: De Lingua et Vita Romanorum** #483 (tokens=82): `certus -a -um 6([III].84 cessare S[II].41 céteri -ae -a 10[II].83 cibus -1 »» 7 `
- **ecce_romani_combined** #0 (tokens=62): `Ecce! In pictura est puella, nomine Cornelia. Cornelia est puella Romana quae in`
- **Ecce Romani I** #8 (tokens=64): `Ecce In pictürà est puella, nomine Cornelia. Cornelia est puella Romana quae in `
- *...还有 25 段*

## Cap.4 (FR Cap.IV)

**数据**: 新词 139 / 累计 621 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #32 (tokens=38): `Medus, qui amicum Iülii timet, nüllum verbum respondet, et Romam ad amicam suam `
- **Fabellae Latinae** #15 (tokens=25): `Iülius: ^Ecce sacculus meus. Iam nón centum, sed tantum decem nummi in sacculo m`
- **Fabellae Latinae** #50 (tokens=46): `Iulius et Cornelius sunt domini Romani. Iülius est dominus pecüniósus, qui magna`
- **Fabellae Latinae** #19 (tokens=41): `Iülius, qui magnam pecüniam habet, in magnà et pulchra villa habitat cum familia`
- **Fabellae Latinae** #16 (tokens=19): `Tülius pecüniam numerat: "Unus, duo, trés, quattuor, quinque, sex, septem, octó,`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: De Lingua et Vita Romanorum** #51 (tokens=99): `Romulus Faustulum et Làrentiam vocat. Ii Ro- mulum sólum vident et interrogant: `
- **Dioclēs et Flōra (Polis)** #11 (tokens=77): `Hic Romae, si puellae pater fügit, et non est alius vir qui custodire eam possit`
- **Dioclēs et Flōra (Polis)** #10 (tokens=77): `Salvete! Mihi nomen est Flora. Sum puella sedecim annorum. Romae habito in domo `
- **Regulus (Saint-Exupéry 拉语版)** #93 (tokens=55): `NEGOTIATOR. — Tres et duo fiunt quinque. Quinque et septem duodecim. Duodecim et`
- **Latin by the Natural Method (W.G. Most 1957)** #199 (tokens=62): `Tribünis Roma expülsis, senátus ad bellum parávit. Meridionáli in parte provínci`
- *...还有 25 段*

## Cap.5 (FR Cap.V)

**数据**: 新词 187 / 累计 808 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #18 (tokens=65): `Cornelius est dominus Romanus, qui in oppido Tüsculo habitat. Cornelius duos lib`
- **Via Latina: De Lingua et Vita Romanorum** #11 (tokens=65): `Suntne casae in oppido? Casae in oppido non sunt, sed in campo. In eó quoque mul`
- **Via Latina: De Lingua et Vita Romanorum** #16 (tokens=73): `Larentia nón in oppido, sed in campo habitat. Casa Larentiae nón in oppido est: `
- **Fabellae Latinae** #27 (tokens=65): `Lydia est femina pulchra quae Romae habitat. Estne femina Romana? Non Romana est`
- **ecce_romani_combined** #0 (tokens=62): `Ecce! In pictura est puella, nomine Cornelia. Cornelia est puella Romana quae in`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Oxford Latin Course Part 2, 2e** #59 (tokens=116): `cotidie Flaccus filium ad lüdum Orbilii dücébat. Quintus celeriter discébat, et `
- **Via Latina: De Lingua et Vita Romanorum** #42 (tokens=104): `Romulus Remusque in casa Larentiae et Faus- tuli habitant. Ii in campo Albano la`
- **Fabellae Latinae** #112 (tokens=83): `Nox est. Villa Iülii obscüra et quieta est. Omnes dormiunt. Parentes in magno cu`
- **Latin Made Simple** #42 (tokens=87): `Servi 1. Romani servos multos in bello occupant. 2. Ex oppidis Graeciae ad Itali`
- **Oxford Latin Course Part 1, 2e** #205 (tokens=92): `dum parvus est, Marcus plerumque in villa habitat. máter paterque saepe absunt; `
- *...还有 25 段*

## Cap.6 (FR Cap.VI)

**数据**: 新词 189 / 累计 997 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #21 (tokens=53): `Faustulus in campo ambulat et... Quid?! Est lupa in campo! Duo parvi pueri cum e`
- **Fabellae Latinae** #51 (tokens=29): `Ex decem equis Iülii Syrus sümit illum nigrum quem dominus ante alios amat eumqu`
- **Ecce Romani I** #34 (tokens=38): `Nondum lücet, sed Cornelia surgit et per villam ambulat. Adhüc dormiunt pater et`
- **Latin First Year (Magoffin)** #25 (tokens=38): `do mi nà/crum bo nà'rum nón erant mi'/se rae. 3. Cu'ius (whose) pa/'tria est T t`
- **Fabellae Latinae** #34 (tokens=17): `Ecce Medus per portam Capenam Romam intrat et laetus ad ostium Lydiae ambulat. M`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #38 (tokens=191): `Marcus vóluit amáre Maríam. María vóluit cápere Marcum. Isabélla pótuit dare pec`
- **Latin by the Natural Method (W.G. Most 1957)** #335 (tokens=115): `Cain et Abel fuérunt fílii Adam et Evae. Nati sunt in primis diébus mundi. Sed é`
- **Via Latina: De Lingua et Vita Romanorum** #318 (tokens=106): `Post exilium Tarquinii Róma iam nón est rég- num, sed 'rés püblica'. In regno ré`
- **Latin for Beginners (D'Ooge)** #34 (tokens=88): `T. r. Màrcus amico Sexto consilium suum nüntiat 2. Est copia frümenti in agris n`
- **Latin for Beginners (D'Ooge 另一版)** #34 (tokens=88): `I. i. Màrcus amicó Sexto consilium suum nüntiat. 2. Est cópia frümenti in agris `
- *...还有 25 段*

## Cap.7 (FR Cap.VII)

**数据**: 新词 127 / 累计 1124 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: De Lingua et Vita Romanorum** #30 (tokens=54): `Làrentia ridet, etiam pueri rident! Ii iam nón plorant, sed laeti sunt et in lec`
- **Fabellae Latinae** #120 (tokens=54): `Ergo Medus et Lydia Romà égrediuntur et Ostiam ambulàre incipiunt. Medus saccum `
- **Forum - Lectiones Latinitatis Vivae (Polis)** #506 (tokens=44): `Est liber qui ... ?                Est mulier quae ... ?            Est templum `
- **Fabellae Latinae** #65 (tokens=43): `Iulius rürsus in equum ascendit et à tabernà Grümionis it ad aliam tabernam suam`
- **Via Latina: De Lingua et Vita Romanorum** #10 (tokens=42): `Larentia in oppido nón habitat. Nec in silva ha- bitat, sed in campo. Larentia i`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin 7e** #818 (tokens=139): `8. À quó liber parátus est (parátus erat, parabatur)? 9. Magister à quó liber pa`
- **Latin by the Natural Method (W.G. Most 1957)** #371 (tokens=130): `Diffícile est bonus esse inter malos. Sed Abram, cum esset in médio tam multórum`
- **Latin by the Natural Method (W.G. Most 1957)** #150 (tokens=126): `Sed primo saéculo ante Christum fuérunt multi viri magni. Inter hos erat Gaius I`
- **ecce_romani_combined** #15 (tokens=110): `Sextus, ubi in hortum mane exit, Davum conspicit et furtim appropinquat. Subito,`
- **Latin by the Natural Method (W.G. Most 1957)** #306 (tokens=105): `Diébus antíquis Romae, Románi multa gessérunt bella. Sed non solum antíquis diéb`
- *...还有 25 段*

## Cap.8 (FR Cap.VIII)

**数据**: 新词 216 / 累计 1340 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Ecce Romani I** #385 (tokens=45): `(illum/illorum/illud) (illo/illà/illae) (illum/illud/illo) (illas/illis/illos) (`
- **Ecce Romani I** #384 (tokens=42): `(horum/hunc/hoc) (hoc/hae/hàc) (hoc/hunc/hoc) (has/hos/his) (hunc/hanc/hoc) (hos`
- **Via Latina: De Lingua et Vita Romanorum** #74 (tokens=68): `Ut Làrentia et Faustulus, Romulus Remusque, féminae et viri, puellae et pueri no`
- **Fabellae Latinae** #43 (tokens=28): `Aemilia: "Tanta gemma ad tam parvum ànulum non convenit. Neque pretium illius ge`
- **Via Latina: De Lingua et Vita Romanorum** #20 (tokens=57): `Ubi est Larentia? Ea in casa est. Estne Faustulus quoque in casa cum Larentia? N`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Ecce Romani I** #385 (tokens=45): `(illum/illorum/illud) (illo/illà/illae) (illum/illud/illo) (illas/illis/illos) (`
- **Latin by the Natural Method (W.G. Most 1957)** #448 (tokens=157): `domus magna. Nemo enim in persóna secünda loqui potest huic regi. Semper dícimus`
- **Latin Made Simple** #143 (tokens=88): `Practice Exercises No. 110. Translate these phrases which use hic and ille: l. h`
- **Latin by the Natural Method (W.G. Most 1957)** #440 (tokens=127): `Sed ecce— vir Aegjptius ad nos venit. Interrogémus eum de terra hac. Amice! (fri`
- **Latin by the Natural Method (W.G. Most 1957)** #148 (tokens=131): `Románam cápere vóluit. Mithradátes erat rex qui mag- nam potestátem hábuit. Sull`
- *...还有 25 段*

## Cap.9 (FR Cap.IX)

**数据**: 新词 187 / 累计 1527 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #53 (tokens=73): `Amici duo oppidum relinquunt et per vallem ad silvam eunt. Equi laeti per campum`
- **Fabellae Latinae** #112 (tokens=83): `Nox est. Villa Iülii obscüra et quieta est. Omnes dormiunt. Parentes in magno cu`
- **Latin Made Simple** #143 (tokens=88): `Practice Exercises No. 110. Translate these phrases which use hic and ille: l. h`
- **First Latin Reader (Chickering)** #570 (tokens=65): `PRAEPOSITIONES QUAE ACCUSATIVUM POSTULANT Ad (i), ante (vii), apud (vi), circum `
- **Fabellae Latinae** #60 (tokens=52): `Grümio est tabernàárius qui Tüsculi panem vendit. Qui ipsi pànem suum facere nón`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #36 (tokens=210): `Románi fere semper bellum habuérunt. Quando bellum cum áliis natióni- bus non ha`
- **Latin by the Natural Method (W.G. Most 1957)** #514 (tokens=168): `Post haec, Ioséphus dedit münera bona síngulis frátribus suis, et profi- ciscént`
- **Latin by the Natural Method (W.G. Most 1957)** #12 (tokens=136): `Status Foederáti Américae fuérunt boni et magni. Colümbus fuit primus vir albus `
- **Cambridge Latin Course 1** #22 (tokens=141): `Caecilius ad portum ambulat. Caecilius portum circumspectat.                    `
- **First Latin Reader (Chickering)** #41 (tokens=137): `populo Rómam dedit. Roma: haec eadem urbs est nunc prima inter omnes totius Ital`
- *...还有 25 段*

## Cap.10 (FR Cap.X)

**数据**: 新词 264 / 累计 1791 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Dioclēs et Flōra (Polis)** #2 (tokens=83): `Salve! Mihi nomen est Diocles. Puer Graecus sum. Non in Graecià habito. In Graec`
- **Fabellae Latinae** #99 (tokens=56): `Marcus et Quintus campum petunt cum cane, cui nomen est Cerberus. Pueri pilà lüd`
- **Dioclēs et Flōra (Polis)** #11 (tokens=77): `Hic Romae, si puellae pater fügit, et non est alius vir qui custodire eam possit`
- **First Latin Reader (Chickering)** #519 (tokens=70): `Réx Thü-lae pi - à cü - rà Co - lé- bat au - re - um Nec ul-trà cà - ri-0 - ra N`
- **Via Latina: De Lingua et Vita Romanorum** #24 (tokens=65): `ET                                                                emini 13. Verb`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #487 (tokens=260): `Deínde Ptáhotep rem novam dixit, *Re vera, unus ex régibus nostris olim factus e`
- **Latin by the Natural Method (W.G. Most 1957)** #508 (tokens=243): `Ex his verbis Iudae, et étiam ex eis quae álii fratres fécerant, Ioséphus pótera`
- **Latin by the Natural Method (W.G. Most 1957)** #304 (tokens=194): `In princípio enim, solus Deus erat; nulla creatára adhuc facta erat. Scriptor hu`
- **Latin by the Natural Method (W.G. Most 1957)** #42 (tokens=172): `étiam misérunt naves in multa mária. Carthaginiénses boni mercatüra fuérunt. Sed`
- **Latin by the Natural Method (W.G. Most 1957)** #326 (tokens=138): `Deus étiam primum hóminem, cuius nomen erat Adam, fecit. Étiam féminam, uxórem p`
- *...还有 25 段*

## Cap.11 (FR Cap.XI)

**数据**: 新词 224 / 累计 2015 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Fabellae Latinae** #109 (tokens=62): `Post horam servus cum medico ad villam Iülii redit. Medicus Marcum linguam osten`
- **Latin Made Simple** #42 (tokens=87): `Servi 1. Romani servos multos in bello occupant. 2. Ex oppidis Graeciae ad Itali`
- **Oxford Latin Course Part 1, 2e** #35 (tokens=59): `céteri pueri iam adsunt.  magister : e jianuà exit et eos iubet intrare et sedér`
- **First Latin Reader (Chickering)** #520 (tokens=69): `Quod de-dit mo-ri-tü - ra A-mi-ca, po- cu - lum. Po- to - ris hü-ment o - ra Pro`
- **Latin by the Natural Method (W.G. Most 1957)** #337 (tokens=58): `Adam et Eva habuérunt multos fílios et fílias. Et fílii eórum habuérunt étiam mu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #34 (tokens=156): `fuérunt in urbe, plebs non pugnávit cum patríciis. Et patrícii non pugnavérunt c`
- **Latin by the Natural Method (W.G. Most 1957)** #365 (tokens=155): `Sed non omnes hómines péssimi facti sunt. Quidam viri adhuc servi Dei erant. Int`
- **Via Latina: Easy Latin Reader (Collar 1897)** #121 (tokens=147): `Superbum régem adiit, novem libros ferens, quos esse dicebat divina oracula: eos`
- **Hobbitus Ille (Tolkien 拉语版)** #502 (tokens=144): `"pro deum fidem, minime, minime, minime, MINIME! Gandalphus inquit. *noli stultu`
- **Via Latina: De Lingua et Vita Romanorum** #156 (tokens=123): `Dum Ancus regnat, Lucumo, vir diligens atque audáx, à patria discedit —erat enim`
- *...还有 25 段*

## Cap.12 (FR Cap.XII)

**数据**: 新词 305 / 累计 2320 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #440 (tokens=127): `Sed ecce— vir Aegjptius ad nos venit. Interrogémus eum de terra hac. Amice! (fri`
- **Fabellae Latinae** #79 (tokens=58): `Avunculus Marci, cui nomen est Aemilius, in Germania militat. Illic exercitus Ro`
- **Latin by the Natural Method (W.G. Most 1957)** #335 (tokens=115): `Cain et Abel fuérunt fílii Adam et Evae. Nati sunt in primis diébus mundi. Sed é`
- **Via Latina: De Lingua et Vita Romanorum** #51 (tokens=99): `Romulus Faustulum et Làrentiam vocat. Ii Ro- mulum sólum vident et interrogant: `
- **Via Latina: De Lingua et Vita Romanorum** #484 (tokens=95): `concitàre 12[II].58 concordia -ae f^ 9[I1].67 condere 3[II].43 condicio -ónis f^`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #65 (tokens=169): `Románus exércitus victus est ab Hannibále ad flumen Trébiam. In próximo anno, Há`
- **Wheelock's Latin 7e** #819 (tokens=165): `6. Quis ad nós eó tempore venit? 7. Senex magnae fámae ex patrià suà ad senàtum `
- **Latin by the Natural Method (W.G. Most 1957)** #28 (tokens=141): `In rebus humánis, perículum non e:            Románi bellum habuérunt in multis `
- **Latin by the Natural Method (W.G. Most 1957)** #400 (tokens=193): `Abraham ergo surréxit et parávit ómnia quae necessária erant ad hoc sacrifícium.`
- **Latin Stories (Wheelock 配套)** #66 (tokens=132): `Degressus Appennino Hannibal ad Placentiam castra movit et decem milia passuum p`
- *...还有 25 段*

## Cap.13 (FR Cap.XIII)

**数据**: 新词 382 / 累计 2702 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #304 (tokens=194): `In princípio enim, solus Deus erat; nulla creatára adhuc facta erat. Scriptor hu`
- **Latin by the Natural Method (W.G. Most 1957)** #448 (tokens=157): `domus magna. Nemo enim in persóna secünda loqui potest huic regi. Semper dícimus`
- **Unus Duo Tres** #40 (tokens=57): `Mensis Ianuarius             Primus mensis            I Mensis Februarius       `
- **Latin by the Natural Method (W.G. Most 1957)** #150 (tokens=126): `Sed primo saéculo ante Christum fuérunt multi viri magni. Inter hos erat Gaius I`
- **ecce_romani_combined** #15 (tokens=110): `Sextus, ubi in hortum mane exit, Davum conspicit et furtim appropinquat. Subito,`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Unus Duo Tres** #40 (tokens=57): `Mensis Ianuarius             Primus mensis            I Mensis Februarius       `
- **Latin by the Natural Method (W.G. Most 1957)** #551 (tokens=200): `Quaedam máülier Hebraeórum ausa erat serváre fílium suum párvulum tres menses et`
- **Second Year Latin (Greenough 1899)** #102 (tokens=187): `2. Ab illo igitur! pàstore Cyrus educatus est. Brevi tem- pore et robore? et ani`
- **Latin by the Natural Method (W.G. Most 1957)** #268 (tokens=169): `Clódius, olim patrícius, iam plebéíus et tribánus plebis, accusábat Ciceró- nem `
- **Latin by the Natural Method (W.G. Most 1957)** #16 (tokens=152): `(against) Romam. Etrüsci paravérunt exércitum mag- num. Románi étiam paravérunt `
- *...还有 25 段*

## Cap.14 (FR Cap.XIV)

**数据**: 新词 255 / 累计 2957 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Reading Latin: Study Guide** #28 (tokens=81): `*Declined in full; omnis res, omnem rem, omnis rei, omni rei, omni re, omnes res`
- **Oxford Latin Course Part 1, 2e** #143 (tokens=95): `immemores. sed Gàáius *veni mécum, Quinte,' inquit, 'nox adest. domum recurrere `
- **Latin by the Natural Method (W.G. Most 1957)** #368 (tokens=92): `Sed postquam omnes hómines péssimi facti sunt, Deus étiam Noe vocávit. Noe enim `
- **Via Latina: De Lingua et Vita Romanorum** #63 (tokens=79): `Quid nunc faciunt gemini? Manentne ii cum avó in oppido? Minime! Num ii campum p`
- **Latin by the Natural Method (W.G. Most 1957)** #375 (tokens=79): `Abram, quid facis nunc? "Multas res paro ut discédam ex hac terra. Deus enim mih`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #582 (tokens=231): `mannos omnibus prouisurum esse, et equum Gandalpho, iter ad siluam faciendi caus`
- **Epitome Historiae Sacrae** #166 (tokens=188): `Sic igitur factum est ut Iosephus dixerat. Septem annos übertatis secuti sunt to`
- **Latin for Beginners (D'Ooge)** #280 (tokens=211): `lamque Püblius, !quindecim annós nàtus, ?primüs litteràrum ele- mentis confectis`
- **Latin by the Natural Method (W.G. Most 1957)** #595 (tokens=198): `enim dixi, in terram nostram venérunt tempóribus malórum regum. Sed ínsuper, hi `
- **Wheelock's Latin 7e** #863 (tokens=182): `4. Magnopere vereor ut imperátor nóbis satis auxilii mittat. 5. Fuit fémina maxi`
- *...还有 25 段*

## Cap.15 (FR Cap.XV)

**数据**: 新词 207 / 累计 3164 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Cambridge Latin Course 1** #31 (tokens=108): `Caecilius est in foro. Caecilius in foro argentariam habet. Hermogenes ad forum `
- **ecce_romani_combined** #19 (tokens=87): `Tum Flavia, “Sed Marcus est semper sollicitus. Sextum nihil terret.” Subito lupu`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #51 (tokens=86): `Salvéte discipuli. Avé magister. Valesne bene ? Optime valeo. Grátiàs tibi ago, `
- **Forum - Lectiones Latinitatis Vivae (Polis)** #119 (tokens=73): `Exemplum Vides sellam?                       Vides calamum?                    V`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #54 (tokens=95): `quaerite verba quae desunt                Lingua Latina nón difficilis, sed faci`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #133 (tokens=184): `busto; neque ülla dies adimet nobis e pectore aeter- num maerorem. Ergo illud qu`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #54 (tokens=95): `quaerite verba quae desunt                Lingua Latina nón difficilis, sed faci`
- **De Rerum Natura (Lucretius 拉语版)** #124 (tokens=182): `rit, sicut nunc posita sunt, atque rürsum lüx vitae concessa fuerit nobis; non e`
- **catilina** #74 (tokens=175): `atque odissent tui neque eos ratione üllà placare posses, ut opinor, ab eorum oc`
- **Latin by the Natural Method (W.G. Most 1957)** #583 (tokens=162): `Phárao, videns ranas abiísse, íterum indurávit cor suum, nec permísit Hebraeís u`
- *...还有 25 段*

## Cap.16 (FR Cap.XVI)

**数据**: 新词 375 / 累计 3539 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 26 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #487 (tokens=260): `Deínde Ptáhotep rem novam dixit, *Re vera, unus ex régibus nostris olim factus e`
- **Latin by the Natural Method (W.G. Most 1957)** #38 (tokens=191): `Marcus vóluit amáre Maríam. María vóluit cápere Marcum. Isabélla pótuit dare pec`
- **Latin by the Natural Method (W.G. Most 1957)** #28 (tokens=141): `In rebus humánis, perículum non e:            Románi bellum habuérunt in multis `
- **Latin by the Natural Method (W.G. Most 1957)** #326 (tokens=138): `Deus étiam primum hóminem, cuius nomen erat Adam, fecit. Étiam féminam, uxórem p`
- **Latin by the Natural Method (W.G. Most 1957)** #371 (tokens=130): `Diffícile est bonus esse inter malos. Sed Abram, cum esset in médio tam multórum`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin for Beginners (D'Ooge 另一版)** #276 (tokens=211): `lamque Püblius, "quindecim annós nàtus, ?primis litteràrum ele- mentis confectis`
- **Latin by the Natural Method (W.G. Most 1957)** #620 (tokens=211): `Et nuntiátum est regi Aegyptiórum quod fugísset pópulus; immutatüm- que est cor `
- **Oxford Latin Course Part 1, 2e** #92 (tokens=165): `prócédere.' ünó cum amicó collem ascendit et prospicit. multós         próspicit`
- **Hobbitus Ille (Tolkien 拉语版)** #574 (tokens=163): `mihi licet dicere ursos paruos, ursos magnos, ursos usitatos, et ursos ingentes `
- **Reading Latin: Text (2e)** #204 (tokens=159): `multas horas equites fortiter pugnauerunt; alii mortui sunt, alit fügerunt. sed `
- *...还有 25 段*

## Cap.17 (FR Cap.XVII)

**数据**: 新词 274 / 累计 3813 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Gwynne's Latin** #43 (tokens=139): `B. 1. Ab initio hunc librum legere facile fuit. 2. Ipse me in speculo videre non`
- **Latin by the Natural Method (W.G. Most 1957)** #217 (tokens=133): `Quodam die Marcus erat in schola. Agnus non venit in scholam, sed quid áccidit? `
- **Latin by the Natural Method (W.G. Most 1957)** #410 (tokens=90): `*Ubi sumus?" dixérunt quinque porci. "Sumus in foro," respóndit unus ex eis. "Vó`
- **Latin for Beginners (D'Ooge 另一版)** #24 (tokens=84): `i. Longae nón sunt tuae viae. 2. Suntne tubae novae in meà casá? NOn sunt. 3. Qu`
- **Via Latina: De Lingua et Vita Romanorum** #483 (tokens=82): `certus -a -um 6([III].84 cessare S[II].41 céteri -ae -a 10[II].83 cibus -1 »» 7 `
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Stories (Wheelock 配套)** #59 (tokens=164): `MENEDEMUS: Filium ünum adulescentem habeo. Ah, cür dixi me habere? Immo habui, C`
- **Wheelock's Latin Reader** #200 (tokens=153): `modestia omnisque sedatio perturbationum animi et rerum mo- dus cernitur. Hoc lo`
- **Latin Stories (Wheelock 配套)** #50 (tokens=149): `Roma regebatur à tyranno superbo, cuius filius erat Sextus Tarquinius. Quadam no`
- **De Rerum Natura (Lucretius 拉语版)** #242 (tokens=138): `Deinde ubi praepararunt sibi domos, et pelles et ignem, et ubi femina iüncta vir`
- **Cambridge Latin Course 3** #16 (tokens=138): `habent. Salvius: Lüci Marci Memor, vir summae prüdentiae es. volo               `
- *...还有 25 段*

## Cap.18 (FR Cap.XVIII)

**数据**: 新词 406 / 累计 4219 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 27 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **First Latin Reader (Chickering)** #41 (tokens=137): `populo Rómam dedit. Roma: haec eadem urbs est nunc prima inter omnes totius Ital`
- **Latin by the Natural Method (W.G. Most 1957)** #502 (tokens=106): `Omnes térriti sunt. Revérsi sunt ad domum Ioséphi. Cumque vidíssent eum, se in t`
- **Pugio Bruti (Polis)** #7 (tokens=91): `ERENTIA AB OBSCÜRÀ vià abiit et caupónam intràvit. Ad ministrum caupónae accessi`
- **First Latin Reader (Chickering)** #37 (tokens=93): `pater tuus fuit Màrs. Quis fuit Mars? Fuit 170 belli deus, ac armorum exercituum`
- **Latin by the Natural Method (W.G. Most 1957)** #473 (tokens=96): `Viri Hebraíci duo, amíci nostri, quodam die in terra Aegypti ambulábant (were wa`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #36 (tokens=230): `aves, tuà vi intrà corda commotae, praenüntiant te, 0 dea, tuumque adventum; dei`
- **Latin Reader (Reynolds)** #274 (tokens=184): `afferebantur, itemque per mercátórés certior factus est Helvetiis esse in animo `
- **Latin Stories (Wheelock 配套)** #62 (tokens=175): `Ibam Via Sacrá, ut soleo, cogitans de rebus meis. Occurrit quidam notus mihi nom`
- **De Rerum Natura (Lucretius 拉语版)** #140 (tokens=164): `Demum, si Nàtüra rerum edat hanc vocem subito et ita aliquem nostrum  reprehenda`
- **Wheelock's Latin Reader** #132 (tokens=157): `tum et acerbas litteras miserat, et erat adhuc impudens qui exer- citum et provi`
- *...还有 25 段*

## Cap.19 (FR Cap.XIX)

**数据**: 新词 336 / 累计 4555 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #36 (tokens=210): `Románi fere semper bellum habuérunt. Quando bellum cum áliis natióni- bus non ha`
- **Wheelock's Latin 7e** #819 (tokens=165): `6. Quis ad nós eó tempore venit? 7. Senex magnae fámae ex patrià suà ad senàtum `
- **Via Latina: De Lingua et Vita Romanorum** #85 (tokens=126): `Itaque socii geminos monent: «Rogate deos at- que signum eórum exspectàáte». Gem`
- **Via Latina: De Lingua et Vita Romanorum** #152 (tokens=128): `Inter populós Indoeurópaeós magnus est numerus deorum. Rómàni, ut Graeci, nón ün`
- **Latin by the Natural Method (W.G. Most 1957)** #490 (tokens=119): `Cum eos vidísset, Ioséphus mandávit servis suis ut cenam parárent. Fratres autem`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #264 (tokens=246): `ceteros homines admoneat? Sed potius innoxius vir neque üllius rei nefandae sibi`
- **Hobbitus Ille (Tolkien 拉语版)** #589 (tokens=197): `contendentes ubicumque terra erat graminea atque plana, cum montibus tenebrosis `
- **Latin Reader (Reynolds)** #329 (tokens=180): `sécum sine suà pernicié contendisse. Cum Caesar. vellet, congrederétur; intelléc`
- **Latin Reader (Reynolds)** #351 (tokens=168): `in castris aut in itinere tenéret, et quod constábat paucis ménsibus patrem M. C`
- **Fabulae Faciles (Ritchie 1889)** #156 (tokens=167): `Postridie ejus diei, Ulysses in animo habebat ex insula quam celerrime discedére`
- *...还有 25 段*

## Cap.20 (FR Cap.XX)

**数据**: 新词 355 / 累计 4910 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 22 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #514 (tokens=168): `Post haec, Ioséphus dedit münera bona síngulis frátribus suis, et profi- ciscént`
- **Gwynne's Latin** #40 (tokens=149): `B. 1. Caesar hostes principio anni oppugnaverat, et (eos) una mense superaverat `
- **Wheelock's Latin 7e** #818 (tokens=139): `8. À quó liber parátus est (parátus erat, parabatur)? 9. Magister à quó liber pa`
- **Wheelock's Latin 7e** #658 (tokens=129): `*Nón est ita," inquit ille. "Nisi enim deus is, cuius hoc templum? est omne quod`
- **Reading Latin: Grammar (2e)** #70 (tokens=123): `mé pater meus, rex deorum, officium magnum perficere iubet. quando patrem meum c`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #610 (tokens=229): `Et dixit Dóminus ad Moysen, "Adhuc una plaga tangam Pharaónem et Aegfptum, et po`
- **catilina** #1 (tokens=195): `[De famá quaerenda] ] Omnes homines qui sese student praestare ceteris animà- li`
- **Wheelock's Latin Reader** #528 (tokens=183): `Diligite inimicos vestros; bene facite his qui vos oderunt; be- nedicite maledic`
- **Latin by the Natural Method (W.G. Most 1957)** #461 (tokens=171): `Rex ergo praecépit ut Ioséphus adducerétur ad se. Cum Ioséphus staret coram rege`
- **Fabulae Faciles (Ritchie 1889)** #151 (tokens=144): `Tum Circe, quae artis magicae summam peritiam habebat, bacülo aureo, quem gereba`
- *...还有 25 段*

## Cap.21 (FR Cap.XXI)

**数据**: 新词 252 / 累计 5162 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 17 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #34 (tokens=156): `fuérunt in urbe, plebs non pugnávit cum patríciis. Et patrícii non pugnavérunt c`
- **Latin by the Natural Method (W.G. Most 1957)** #42 (tokens=172): `étiam misérunt naves in multa mária. Carthaginiénses boni mercatüra fuérunt. Sed`
- **Latin by the Natural Method (W.G. Most 1957)** #100 (tokens=128): `Sed quid dixit senátus Románus? Postquam viri Cartháginis deposué- runt arma, se`
- **Latin by the Natural Method (W.G. Most 1957)** #12 (tokens=136): `Status Foederáti Américae fuérunt boni et magni. Colümbus fuit primus vir albus `
- **De Rerum Natura (Lucretius 拉语版)** #123 (tokens=143): `Mors nihil est ad nos, neque quidquam pertinet, quandoquidem nàtüra animi est mo`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin by the Natural Method (W.G. Most 1957)** #13 (tokens=162): `Postquam Románi expulérunt Tarquínium bellum habuérunt. Tarquínius          post`
- **Wheelock's Latin Reader** #47 (tokens=217): `Quid? signum Paeanis ex aede Aesculapi praeclare factum, sacrum ac religiosum, n`
- **Latin by the Natural Method (W.G. Most 1957)** #54 (tokens=180): `Sagüntum cécidit. Mílites Pánici venérunt in urbem. In urbe cepérunt multum auru`
- **Wheelock's Latin Reader** #231 (tokens=193): `Sed, ut laudandus Regulus in conservando 1ure, sic decem illi quos post Cannense`
- **Wheelock's Latin Reader** #559 (tokens=192): `Quod dum tempore quodam faceret, et relicta domu con- vivii egressus esset ad st`
- *...还有 25 段*

## Cap.22 (FR Cap.XXII)

**数据**: 新词 312 / 累计 5474 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 12 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #65 (tokens=169): `Románus exércitus victus est ab Hannibále ad flumen Trébiam. In próximo anno, Há`
- **Wheelock's Latin 7e** #829 (tokens=147): `14. Sció té hoc fécisse (factürum esse, facere). 15. Scivi té hoc fécisse (factü`
- **Latin by the Natural Method (W.G. Most 1957)** #310 (tokens=123): `Sacer scríptor docet nos quod Deus ómnia fecit. Narratiónem suam divísit in sex `
- **Latin by the Natural Method (W.G. Most 1957)** #308 (tokens=127): `remánsit máximo afféctus est dolóre. Dixit enim, '*O! O! Necésse est timére. Sed`
- **Latin by the Natural Method (W.G. Most 1957)** #333 (tokens=110): `Deus díxerat ad Adam et Evam: Ne comedátis ex fructu ligni sciéntiae boni et mal`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **catilina** #68 (tokens=210): `audaciae satellitem atque administrum tuae'? Num me fefellit, Catilina, non modo`
- **Latin Reader (Reynolds)** #209 (tokens=205): `nón modo videt sed etiam perspicit plàneque sentit. Reliqui omnés clàrissimam fo`
- **Latin Reader (Reynolds)** #311 (tokens=198): `véra: Ipsum esse Dumnorigem, summà& audácià, magn& apud plebem propter liberalit`
- **Wheelock's Latin Reader** #249 (tokens=179): `intuetur sui. Quocirca et absentes adsunt et egentes abundant et imbecilli valen`
- **Wheelock's Latin Reader** #87 (tokens=175): `Si haec non ad cives Romanos, non ad aliquos amicos nos- trae civitatis, non ad `
- *...还有 25 段*

## Cap.23 (FR Cap.XXIII)

**数据**: 新词 270 / 累计 5744 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 11 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #508 (tokens=243): `Ex his verbis Iudae, et étiam ex eis quae álii fratres fécerant, Ioséphus pótera`
- **Hobbitus Ille (Tolkien 拉语版)** #502 (tokens=144): `"pro deum fidem, minime, minime, minime, MINIME! Gandalphus inquit. *noli stultu`
- **Latin by the Natural Method (W.G. Most 1957)** #271 (tokens=133): `Amíci Catilínae in cárcerem ibant. In cárcere mori- éntur. Ergo magno affécti su`
- **Latin Made Simple** #210 (tokens=123): `Aeneas in Igni Troiae l. Aeneas in vias Troiae una nocte cucurrit et multitudine`
- **Latin by the Natural Method (W.G. Most 1957)** #183 (tokens=104): `Hic est modus quo Pompéius vóluit delére Caésarem: vóluit cógere eum redíre in u`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #574 (tokens=246): `Moralitas: Carissimi, imperator est Deus, qui diu guerram cum homine habuit in t`
- **Hobbitus Ille (Tolkien 拉语版)** #9 (tokens=210): `aut supra Collem aut trans Aquam inueniri potuit, aedificauit, et ibi ad supremo`
- **catilina** #72 (tokens=206): `némo qui nón oderit! Quae nota domesticae turpitüdinis non inusta vitae tuae est`
- **De Rerum Natura (Lucretius 拉语版)** #150 (tokens=176): `Praeterea, alere perpetuo ingratam naturam animi et replere illam optimis rebus,`
- **Wheelock's Latin Reader** #541 (tokens=144): `Homo quidam erat dives, et induebatur purpura et bysso, et epulabatur cotidie sp`
- *...还有 25 段*

## Cap.24 (FR Cap.XXIV)

**数据**: 新词 245 / 累计 5989 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 13 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Pugio Bruti (Polis)** #152 (tokens=167): `quoque adulescentem capillo nigró quaerere. Itaque té nunc rogo: Repperistine eu`
- **Wheelock's Latin 7e** #856 (tokens=121): `11. Paucis horis Rómam ibimus. 12. Nós ad urbem imus; illi domum eunt. 13. Ut sa`
- **Latin by the Natural Method (W.G. Most 1957)** #402 (tokens=112): `Non enim re vera vóluit Deus sacrifícium humánum. Deus enim sacrifícia humána pr`
- **Latin by the Natural Method (W.G. Most 1957)** #372 (tokens=107): `Sed Abram non semper remánsit in Aegfpto. Revérsus est in terram Chánaan. Lot ét`
- **Latin by the Natural Method (W.G. Most 1957)** #560 (tokens=109): `Abscóndit Moyses fáciem suam; non enim audébat spectáre Deum. Cui ait Dóminus, *`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #818 (tokens=207): `gubernatoribus loquentibus auscultans et ex fragmentis patefactis certior factus`
- **Latin Reader (Reynolds)** #327 (tokens=188): `in Lingonibus tenéret, nondum perspexerat; et cuius ab- sentis amicitià ante& ni`
- **De Rerum Natura (Lucretius 拉语版)** #173 (tokens=182): `pereunt, et fiunt anademata, mitrae; heredes, amore cuiusdam feminae flagrantes,`
- **Wheelock's Latin Reader** #327 (tokens=159): `Missus Hannibal in Hispaniam primo statim adventu om- nem exercitum in se conver`
- **Epitome Historiae Sacrae** #473 (tokens=162): `t ecce homo quidam iüris peritus surrexit dicens: *Magi- E. quid faciendo vitam `
- *...还有 25 段*

## Cap.25 (FR Cap.XXV)

**数据**: 新词 427 / 累计 6416 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 26 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #595 (tokens=198): `enim dixi, in terram nostram venérunt tempóribus malórum regum. Sed ínsuper, hi `
- **Wheelock's Latin 7e** #805 (tokens=164): `8. Caesar eós servàvit. 9. Caesar eum servàbat. 10. Caesar sé servàvit. 11. Rómà`
- **Latin by the Natural Method (W.G. Most 1957)** #200 (tokens=172): `Quia non hábuit naves in quibus posset (Ae could) sequi Pompeium, Caesar discéss`
- **Latin by the Natural Method (W.G. Most 1957)** #365 (tokens=155): `Sed non omnes hómines péssimi facti sunt. Quidam viri adhuc servi Dei erant. Int`
- **Latin by the Natural Method (W.G. Most 1957)** #511 (tokens=153): `Próximo die Phárao íterum cum amíco nostro Iosépho loquebátur: "Ioséphe, iam nar`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Oxford Latin Course Part 3, 2e** #29 (tokens=258): `discessit; Brütum in Asiam secütus est.' Flaccus 'quid dicis, carissima?' inquit`
- **Intermediate Oral Latin Reader** #110 (tokens=232): `mortem omni aetüti esse commünem. — At sperat adules- cens diü sé victürum, quod`
- **Latin Reader (Reynolds)** #343 (tokens=192): `aut nàvis nacti trünsiére aut viribus confisi tránüre con- tendérunt. In his fui`
- **Second Year Latin (Greenough 1899)** #155 (tokens=169): `Afloat Again. . 20. Postridie eius di&i Ulixés in animó habébat ex insulà quam c`
- **First Latin Reader (Chickering)** #184 (tokens=159): `locum omnium civium nómina, primum nómen ex- tractum vocàri iussit. Ubi aduléscé`
- *...还有 25 段*

## Cap.26 (FR Cap.XXVI)

**数据**: 新词 360 / 累计 6776 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 9 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #400 (tokens=193): `Abraham ergo surréxit et parávit ómnia quae necessária erant ad hoc sacrifícium.`
- **Latin by the Natural Method (W.G. Most 1957)** #551 (tokens=200): `Quaedam máülier Hebraeórum ausa erat serváre fílium suum párvulum tres menses et`
- **Wheelock's Latin 7e** #863 (tokens=182): `4. Magnopere vereor ut imperátor nóbis satis auxilii mittat. 5. Fuit fémina maxi`
- **Latin by the Natural Method (W.G. Most 1957)** #16 (tokens=152): `(against) Romam. Etrüsci paravérunt exércitum mag- num. Románi étiam paravérunt `
- **Latin Made Simple** #198 (tokens=138): `Proelium Thermopylarum 1. Post decem annos Persae ad Graeciam navibus suos redux`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #268 (tokens=227): `Sed (saepe enim redeo ad Scipionem cuius omnis sermo erat de amicitia) querebatu`
- **De Rerum Natura (Lucretius 拉语版)** #119 (tokens=217): `nos carpimus et gustamus omnes tuas sententias aureds; aureas, inquam, et quae s`
- **Hobbitus Ille (Tolkien 拉语版)** #97 (tokens=200): `gemmasque hominibus et dryadibus et nanis subripiunt, ut intellegis, ubicumque e`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #535 (tokens=193): `NICOLAUS: Alexander esne mihi amicus? ALEXANDER : Quid tibi cürae est, Nicolae? `
- **Hobbitus Ille (Tolkien 拉语版)** #96 (tokens=180): `expulsa, cum diuitiis omnibus atque instrumentis suis, ad hunc Montem in tabula `
- *...还有 25 段*

## Cap.27 (FR Cap.XXVII)

**数据**: 新词 433 / 累计 7209 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 20 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **De Rerum Natura (Lucretius 拉语版)** #124 (tokens=182): `rit, sicut nunc posita sunt, atque rürsum lüx vitae concessa fuerit nobis; non e`
- **Pro Patria (Sonnenschein 1907)** #31 (tokens=156): `22. Sed iam prope finem ambulationis nostrae eramus, cum Alexander ' Ecce, Rutup`
- **Latin Reader (Reynolds)** #188 (tokens=149): `Suis subridens Paulus tabulas cónféstim ad sé ferri iubet. Quibus látis scribit `
- **Latin Made Simple** #194 (tokens=132): `Proelium Marathonium 1. Anno XD Ante Christum, Graecis ab exercitu Persarum grav`
- **Pugio Bruti (Polis)** #50 (tokens=113): `"Cür venter tuus vini maculas habet?" "Quid," inquit Clodius, "dixisti?" "Cür nü`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #105 (tokens=218): `rauco sonitü terrent, eosdemque tibia cava sono Phrygio agitat: et sacerdotes po`
- **Latin Reader (Reynolds)** #256 (tokens=206): `erat grátià apud Suebam uxorem et filiam novem annórum, eui nomen erat Velaeda. `
- **Wheelock's Latin Reader** #350 (tokens=155): `Dictator, exercitu consulis accepto, in viam Latinam est egressus, unde itinerib`
- **Wheelock's Latin 7e** #522 (tokens=156): `. Régi persuási ut soróri frátrique tuó grátióra praemia libenter daret. . Deind`
- **A First Latin Reader (Nutting)** #229 (tokens=137): `occidentem navigantes interdum videbant; tum, € portibus liburnicis celerrime ve`
- *...还有 25 段*

## Cap.28 (FR Cap.XXVIII)

**数据**: 新词 440 / 累计 7649 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 17 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Epitome Historiae Sacrae** #166 (tokens=188): `Sic igitur factum est ut Iosephus dixerat. Septem annos übertatis secuti sunt to`
- **Reading Latin: Text (2e)** #99 (tokens=161): `EVC.        heus tü, quis es?                                                   `
- **Latin by the Natural Method (W.G. Most 1957)** #55 (tokens=157): `Hánnibal hábuit ódium acre contra Romános. Románi vícerant Cartháginem in primo `
- **A First Latin Reader (Nutting)** #13 (tokens=130): `Cum multa milia passuum Columbus nàvigàsset neque sterram vidisset üllam, nautae`
- **Via Latina: De Lingua et Vita Romanorum** #211 (tokens=132): `Post Servium Tullium régnat in urbe Tarqui- nius Superbus, septimus rex Romae. À`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader (Reynolds)** #255 (tokens=204): `rum auxilio Aedui victi et coácti sunt Sequanis obsidés dare et iüráre sésé nequ`
- **Ecce Romani III** #206 (tokens=188): `"Sed, ut coeperam dicere, ad hanc me fortünam frügalitas mea perdüxit. "Tam magn`
- **Wheelock's Latin 7e** #503 (tokens=186): `1. Dehinc petet à frátre meo et soróre ut occásiónem carpant et in urbem quam ce`
- **Wheelock's Latin Reader** #60 (tokens=154): `Gavius hic, quem dico, Consanus, cum in illo numero civi- um Romanorum ab isto i`
- **Wheelock's Latin Reader** #246 (tokens=144): `Talis igitur inter viros amicitia tantas opportunitates habet quantas vix queo d`
- *...还有 25 段*

## Cap.29 (FR Cap.XXIX)

**数据**: 新词 434 / 累计 8083 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 12 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **De Rerum Natura (Lucretius 拉语版)** #133 (tokens=184): `busto; neque ülla dies adimet nobis e pectore aeter- num maerorem. Ergo illud qu`
- **Epitome Historiae Sacrae** #91 (tokens=188): `Cum in matrimonium eam Isaacus düxisset, üno                     duo fili1 nàti `
- **Latin by the Natural Method (W.G. Most 1957)** #268 (tokens=169): `Clódius, olim patrícius, iam plebéíus et tribánus plebis, accusábat Ciceró- nem `
- **De Rerum Natura (Lucretius 拉语版)** #167 (tokens=159): `Sthomines possentcognoscere ex quibus causis, et unde tanta moles malorum insit `
- **Latin by the Natural Method (W.G. Most 1957)** #609 (tokens=145): `maióres sunt quam dei Aegypti!" Sed íterum cogitávi non oportére hoc modo loqui.`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #266 (tokens=221): `Quis est—pro deorum fidem atque hominum!— qui velit, ut neque diligat quemquam n`
- **Latin Reader (Reynolds)** #300 (tokens=176): `Helvétii eorum finis populàrentur: ita sé omni tempore dé populo Rómánó meritos `
- **Latin Reader (Reynolds)** #288 (tokens=162): `ire nón possent; alterum per provinciam Romànam, multo facilius atque expeditius`
- **Wheelock's Latin 7e** #633 (tokens=154): `Principio, ut? Catilina paucis ante diébus? érüpit? ex urbe, cum sceleris sui so`
- **catilina** #127 (tokens=141): `Principio, ut Catilina paucis ante diebus érüpit ex urbe, cum sceleris sui socio`
- *...还有 25 段*

## Cap.30 (FR Cap.XXX)

**数据**: 新词 366 / 累计 8449 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 18 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin 7e** #858 (tokens=176): `5. Amicus meus qui consulem deéfendit ipse erat vir clàrissimus. 6. At némó erat`
- **Latin by the Natural Method (W.G. Most 1957)** #517 (tokens=161): `Cum patrem suum vidísset, Ioséphus laetus erat, et cucürrit ad eum vidéndum. Phá`
- **Latin for Beginners (D'Ooge 另一版)** #295 (tokens=149): `Hoc iter in Germàniam Püblius quoque fécit et, *cum ibi moràárétur, multa mirábi`
- **Latin for Beginners (D'Ooge)** #299 (tokens=146): `Hoc iter in Germàniam Püblius quoque fécit et, 5cum ibi moràrétur, multa mirábil`
- **Via Latina: Easy Latin Reader (Collar 1897)** #73 (tokens=131): `Brevi intermisso spatio, Ulixes ad omnia pericula sub- eunda paratus ostium puls`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader for Lower Forms (Hardy 1889)** #285 (tokens=258): `statim agnovit hunc inter omnes. Quum instaret ille, tandem hie, Venalis est, in`
- **De Rerum Natura (Lucretius 拉语版)** #70 (tokens=225): `Ergo videmus paucás res necessarias esse ad corpoream nàtüram, ut detrahant homi`
- **De Rerum Natura (Lucretius 拉语版)** #193 (tokens=183): `Nisi excitaremus fecundam terram ad früges gignendas, vertentes vomere fertiles `
- **Latin Reader (Reynolds)** #366 (tokens=148): `prius visi sunt, quam castris appropinquàrent üsque eo, uti puer et puella, qui `
- **Latin by the Natural Method (W.G. Most 1957)** #549 (tokens=130): `Véniunt in silvas (forest) cédrinas (cedar) occi- dentáles. Ibi terríbile invéni`
- *...还有 25 段*

## Cap.31 (FR Cap.XXXI)

**数据**: 新词 423 / 累计 8872 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 14 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Second Year Latin (Greenough 1899)** #102 (tokens=187): `2. Ab illo igitur! pàstore Cyrus educatus est. Brevi tem- pore et robore? et ani`
- **Latin by the Natural Method (W.G. Most 1957)** #48 (tokens=188): `Post bellum Pünicum primum pax fuit. Sed Carthaginiénses non habuérunt pecániam `
- **De Rerum Natura (Lucretius 拉语版)** #140 (tokens=164): `Demum, si Nàtüra rerum edat hanc vocem subito et ita aliquem nostrum  reprehenda`
- **A First Latin Reader (Nutting)** #353 (tokens=159): `magna vis frümenti ab eis integra in agris relicta est. Quo cognito, imperátor c`
- **De Rerum Natura (Lucretius 拉语版)** #242 (tokens=138): `Deinde ubi praepararunt sibi domos, et pelles et ignem, et ubi femina iüncta vir`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: Easy Latin Reader (Collar 1897)** #195 (tokens=208): `miserant, qui eum certiorem facerent, nisi Alcibiadem sus- tulisset, nihil earum`
- **Via Latina: Easy Latin Reader (Collar 1897)** #17 (tokens=144): `Hoc facto, Phineus, ut pro tanto beneficio meritas grátiás referret, Iasoni démo`
- **Latin by the Natural Method (W.G. Most 1957)** #580 (tokens=141): `Prima fácie (at first sight) narrátio Babylónica simíl- lima vidétur esse narrat`
- **Ora Maritima (Sonnenschein 1900)** #37 (tokens=134): `29. "'Britanni pácem non violàverant, sed Ro- màni pücis nón cupidi erant. Itaqu`
- **Latin Stories (Wheelock 配套)** #51 (tokens=130): `O nimium fortünatos agricolas, quibus facilem victum divitissima terra volens fu`
- *...还有 25 段*

## Cap.32 (FR Cap.XXXII)

**数据**: 新词 470 / 累计 9342 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 17 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Cambridge Latin Course 3** #223 (tokens=154): `ex carcere, ubi captivi custodiebantur, tristes clàmores audiebantur. duae enim `
- **Pro Patria (Sonnenschein 1907)** #21 (tokens=136): `I4. Postquam hoc caput in vita Agricolae lectitavimus, patruus meus  *'Haec narr`
- **Latin for Beginners (D'Ooge)** #179 (tokens=140): `I. i. Trés ex légátis, contrá Caesaris opmionem, iter facere per hostum finis ve`
- **Hobbitus Ille (Tolkien 拉语版)** #753 (tokens=144): `miserum dominum Bagginsem! — qui per tempus longum fessumque in illo loco habita`
- **Wheelock's Latin Reader** #297 (tokens=136): `capessit fugam, ita ratus secuturos ut quemque vulnere adfec- tum corpus sineret`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #7 (tokens=177): `taciti et cito se auferant quandocumque talis ingens et stulta gens qualis tu et`
- **Latin Reader (Reynolds)** #350 (tokens=181): `Primo autem vére tempestüs caléscebat. Omnia longo 5rigore hiemis solvuntur. Ini`
- **Epitome Historiae Sacrae** #122 (tokens=176): `Iosephum interea à mercatoribus emerat Pütiphar, vir Aegyptius, qui eum praefeci`
- **Pro Patria (Sonnenschein 1907)** #9 (tokens=156): `T5. Post mortem Cunobelini, Claudius, quartus princeps Romanorum, expeditionem c`
- **De Rerum Natura (Lucretius 拉语版)** #102 (tokens=136): `Tellus continet in se primordia illa, quibus fit ut fontes, qui fluviorum frigid`
- *...还有 25 段*

## Cap.33 (FR Cap.XXXIII)

**数据**: 新词 476 / 累计 9818 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 7 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #54 (tokens=180): `Sagüntum cécidit. Mílites Pánici venérunt in urbem. In urbe cepérunt multum auru`
- **First Latin Reader (Chickering)** #205 (tokens=169): `Victus caesusque est Itómünus exercitus; numquam graviore volnere afflicta est r`
- **catilina** #74 (tokens=175): `atque odissent tui neque eos ratione üllà placare posses, ut opinor, ab eorum oc`
- **Hobbitus Ille (Tolkien 拉语版)** #343 (tokens=160): `"donum diei natalis! quod ad me aduenit die natali, mi pretiose." ita semper sib`
- **Latin for Beginners (D'Ooge)** #287 (tokens=145): `studére incepit et praesertim üsü* armorum se diligenter exercuit. Magis magisqu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader (Reynolds)** #167 (tokens=195): `ternus liberis est avunculus. Fràter paternus eis patruus est. Liberi Roómàni pa`
- **First Latin Reader (Chickering)** #476 (tokens=178): `Gallia est omnis divisa in partes trés, quàrum ünam incolunt Belgae, aliam Aquit`
- **Reading Latin: Text (2e)** #138 (tokens=154): `ALC.         immo post mecum illa7nocte cenauisti et cubuisti et. . .           `
- **First Latin Reader (Chickering)** #441 (tokens=146): `omnium maxime diligeret, respondit, '" Fratrem." Iterum rogaátus, quem secundum `
- **Second Year Latin (Greenough 1899)** #164 (tokens=128): `illa Cimbrórum multitüdó; caesa! tráduntur centum octó- gintà hominum milia. Nec`
- *...还有 25 段*

## Cap.34 (FR Cap.XXXIV)

**数据**: 新词 520 / 累计 10338 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 10 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin 7e** #840 (tokens=170): `8. Ubi dux est (fuit)? 9. Rogant ubi dux sit (fuerit). 10. Rogàbant ubi dux esse`
- **Second Year Latin (Greenough 1899)** #136 (tokens=148): `1i. His rébus ita cónfectis,? Ulix&s cum sociis máximé veri- tus?né Polyphémus f`
- **Latin Stories (Wheelock 配套)** #12 (tokens=129): `Post bellum Troianum venit Ulixes cum XII viris ad terram Cyclopum. In caverna b`
- **Via Latina: De Lingua et Vita Romanorum** #259 (tokens=116): `Ab illà nocte Sextus Tarquinius uxorem suam ve- hementer contemnébat atque Lucré`
- **Septimus (Chambers 1910)** #85 (tokens=110): `lissimus. Romani bellum acre illó tempore cum Aequis gerebant. legatos, ut in ma`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin 7e** #847 (tokens=186): `6. Si ratió dücit, felix es. 7. Si ratió dücet, felix eris. 8. Si ratio dücat, f`
- **Wheelock's Latin Reader** #366 (tokens=149): `^Haec una salutis est via, L. Paule, quam difficilem in- festamque cives tibi ma`
- **Wheelock's Latin 7e** #307 (tokens=128): `1. "Quisque; inquit, "semper putat suàs rés esse magnàs"              ; 2. Poste`
- **Pro Patria (Sonnenschein 1907)** #25 (tokens=104): `I7. Tum Marcus * Num filii principum  Bri- tannicorum studio linguae Latinae del`
- **Reading Latin: Grammar (2e)** #143 (tokens=111): `audio apud Catinensis esse Cereris sacrarium. in sacrárium illud uiris intrare n`
- *...还有 25 段*

## Cap.35 (FR Cap.XXXV)

**数据**: 新词 336 / 累计 10674 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 12 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Hobbitus Ille (Tolkien 拉语版)** #582 (tokens=231): `mannos omnibus prouisurum esse, et equum Gandalpho, iter ad siluam faciendi caus`
- **catilina** #1 (tokens=195): `[De famá quaerenda] ] Omnes homines qui sese student praestare ceteris animà- li`
- **Oxford Latin Course Part 1, 2e** #92 (tokens=165): `prócédere.' ünó cum amicó collem ascendit et prospicit. multós         próspicit`
- **Hobbitus Ille (Tolkien 拉语版)** #1238 (tokens=141): `itaque proelium ab omnibus inopinatum inierunt; quod Proelium Quinque Exercituum`
- **Epitome Historiae Sacrae** #342 (tokens=137): `Sicut facere coeperat ab ineunte aetate, etiam in captivitate Tobias legem divin`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: Easy Latin Reader (Collar 1897)** #187 (tokens=158): `Haec Alcibiadi laetitia non nimis fuit diüturna. Nam cum ei omnés essent honores`
- **Regulus (Saint-Exupéry 拉语版)** #54 (tokens=155): `EGO VERO DE flore illo plura perquam cito cognovi. Flores in stella reguli sempe`
- **Wheelock's Latin 7e** #831 (tokens=120): `8. Nüntiàvérunt ducem quam fortissimum vénisse. 9. Lüce clarissima ab quattuor v`
- **ars_amatoria** #15 (tokens=102): `(sagittà) figere 7 percutere, laedere violentus -a -um 7 vi üténs; adv vio- lent`
- **Latin Reader for Lower Forms (Hardy 1889)** #134 (tokens=100): `Thebanus quidam, qui Athenas nuper venerat, ad cenam ab hospite invitatus asinum`
- *...还有 25 段*

## Cap.36 (RA Cap.XXXVI)

**数据**: 新词 1943 / 累计 12617 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 30 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader (Reynolds)** #209 (tokens=205): `nón modo videt sed etiam perspicit plàneque sentit. Reliqui omnés clàrissimam fo`
- **Latin by the Natural Method (W.G. Most 1957)** #17 (tokens=148): `cónsules duos (rwo). Cónsules fuérunt viri boni. Reges Etrüsci fuérunt mali. Sed`
- **Latin Reader (Reynolds)** #329 (tokens=180): `sécum sine suà pernicié contendisse. Cum Caesar. vellet, congrederétur; intelléc`
- **Latin by the Natural Method (W.G. Most 1957)** #13 (tokens=162): `Postquam Románi expulérunt Tarquínium bellum habuérunt. Tarquínius          post`
- **Latin Stories (Wheelock 配套)** #62 (tokens=175): `Ibam Via Sacrá, ut soleo, cogitans de rebus meis. Occurrit quidam notus mihi nom`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #196 (tokens=172): `(d) Political leaders should serve the interests of state and not merely those o`
- **Ecce Romani III** #169 (tokens=163): `Marcus Ulpius Traianus rem püblicam ita administravit ut omnibus principibus mer`
- **Second Year Latin (Greenough 1899)** #85 (tokens=161): `Ubi coepit advesperáscere, iubet sterni sibi primà domüs parte, poscit pugillàri`
- **Reading Latin: Text (2e)** #53 (tokens=157): `sed furcifer. SERVVS ego otiosus non sum, Pamphila. nam hodie Démaenetus, dominu`
- **Latin Reader for Lower Forms (Hardy 1889)** #290 (tokens=134): `Maecum ad cenam, et numeravit calceario pretium. Simile quiddam accidit Daventri`
- *...还有 25 段*

## Cap.37 (RA Cap.XXXVII)

**数据**: 新词 1391 / 累计 14008 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 14 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader (Reynolds)** #274 (tokens=184): `afferebantur, itemque per mercátórés certior factus est Helvetiis esse in animo `
- **Wheelock's Latin Reader** #217 (tokens=164): `Fabricius and Pyrrhus. Id quidem cum saepe alias, tum Pyr- rhi bello a C. Fabric`
- **Pro Patria (Sonnenschein 1907)** #61 (tokens=147): `T4606. *Silentio noctis per tenebras et imbrem Caledones agmine quadrato ad locu`
- **Second Year Latin (Greenough 1899)** #148 (tokens=140): `16. Tum Circé, quae artis magicae summam scientiam habébat, baculó aureo quod ge`
- **Via Latina: Easy Latin Reader (Collar 1897)** #56 (tokens=134): `At Polyphémus, ubi socios suos abiisse sensit, furore atque àmentià impulsus Uli`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #295 (tokens=171): `Quamquam autem plüres homines mortui suprà alios inhumata in terrà iacebant, tam`
- **Via Latina: Easy Latin Reader (Collar 1897)** #182 (tokens=155): `Neque véro his rébus tam amici Alcibiadi sunt facti quam timore ab eo alienati. `
- **Epitome Historiae Sacrae** #32 (tokens=137): `Cum hominum vitia validiores fierent, Deus eorum generem pluvia de caelo cadente`
- **Pro Patria (Sonnenschein 1907)** #17 (tokens=122): `Ir. Primo anno imperii sui Agricola in Cam- bria bellavit, ubi magnam victoriam `
- **Via Latina: Easy Latin Reader (Collar 1897)** #185 (tokens=122): `His cum obviam üniversa civitas in Piraeum déscendis- set, tanta fuit omnium exs`
- *...还有 25 段*

## Cap.38 (RA Cap.XXXVIII)

**数据**: 新词 811 / 累计 14819 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 6 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **De Rerum Natura (Lucretius 拉语版)** #36 (tokens=230): `aves, tuà vi intrà corda commotae, praenüntiant te, 0 dea, tuumque adventum; dei`
- **Latin for Beginners (D'Ooge)** #280 (tokens=211): `lamque Püblius, !quindecim annós nàtus, ?primüs litteràrum ele- mentis confectis`
- **Latin for Beginners (D'Ooge 另一版)** #276 (tokens=211): `lamque Püblius, "quindecim annós nàtus, ?primis litteràrum ele- mentis confectis`
- **De Rerum Natura (Lucretius 拉语版)** #150 (tokens=176): `Praeterea, alere perpetuo ingratam naturam animi et replere illam optimis rebus,`
- **First Latin Reader (Chickering)** #184 (tokens=159): `locum omnium civium nómina, primum nómen ex- tractum vocàri iussit. Ubi aduléscé`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #556 (tokens=154): `tum baa — baa — baa! audiebatur, et nonnullae oues niueae magno ariete colore ca`
- **ars_amatoria** #78 (tokens=115): `[Cera blanditiàs ferat] Céra vadum temptet rasis infüsa tabellis, céra tuae prim`
- **Reading Latin: Grammar (2e)** #7 (tokens=114): `Démaenetus coquos et tibicinas uidet. ad nüptias filiae ueniunt. in aedis Démaen`
- **Latin Reader for Lower Forms (Hardy 1889)** #212 (tokens=101): `imaginem Zariadrae, qui inter Caspias portas fluviumque Tanain dominabatur, dorm`
- **Fabulae Faciles (Ritchie 1889)** #98 (tokens=96): `Postquam manes Stygem hoc modo transierant, ad altér- um veniebant flumen, quod `
- *...还有 25 段*

## Cap.39 (RA Cap.XXXIX)

**数据**: 新词 1241 / 累计 16060 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 14 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **De Rerum Natura (Lucretius 拉语版)** #264 (tokens=246): `ceteros homines admoneat? Sed potius innoxius vir neque üllius rei nefandae sibi`
- **Hobbitus Ille (Tolkien 拉语版)** #736 (tokens=173): `fuit quoque captiuorum eius carcer. itaque Thorinum ad antrum traxerunt — nequaq`
- **Wheelock's Latin Reader** #235 (tokens=163): `Tum Scaevola exposuit nobis sermonem Laeli de amicitia habitum ab illo secum et `
- **Wheelock's Latin Reader** #322 (tokens=156): `pendium militibus forte daretur, et scriba cum rege sedens pari fere ornatu mult`
- **Teach Yourself Beginner's Latin** #110 (tokens=146): `Adhuc abbas in ecclesia praedicabat:    Hic, in ecclesia, ubi sedemus, ubí oramu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Epitome Historiae Sacrae** #239 (tokens=207): `Madianitis superatis, Philistae1 coeperant multa incommoda Hebraeis affligere, q`
- **Wheelock's Latin Reader** #332 (tokens=169): `Gallisque ad visenda loca praemissis, castra quam extentissima potest valle loca`
- **catilina** #125 (tokens=132): `Rem püblicam, Quirités, vitamque omnium vestrum, bona, fortünas, coniuges libero`
- **Cambridge Latin Course 4** #123 (tokens=132): `protinus Aeoliis Aquilonem claudit in antris.* emittitque Notum; madidis Notus e`
- **ars_amatoria** #160 (tokens=117): `Nec grave t& tempus sitiensque Canicula tardet nec via per iactas candida facta `
- *...还有 25 段*

## Cap.40 (RA Cap.XL)

**数据**: 新词 1028 / 累计 17088 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 10 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #559 (tokens=192): `Quod dum tempore quodam faceret, et relicta domu con- vivii egressus esset ad st`
- **Fabulae Faciles (Ritchie 1889)** #156 (tokens=167): `Postridie ejus diei, Ulysses in animo habebat ex insula quam celerrime discedére`
- **Intermediate Oral Latin Reader** #132 (tokens=157): `ei docti saepe fecerunt, neque mé vixisse paenitet, quóniam ita vixi, ut nón frü`
- **De Rerum Natura (Lucretius 拉语版)** #83 (tokens=149): `Illud non est mirum, cür scilicet, cum omnia primordia r&rum sint in mótü, summa`
- **Wheelock's Latin Reader** #115 (tokens=142): `De Quinto fratre nihil ego te accusavi, sed vos, cum praeser- tim tam pauci siti`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #303 (tokens=157): `Ac nescio an, nimis undique eam minimisque rebus muni- endo, modum excesserint. `
- **Latin Reader for Lower Forms (Hardy 1889)** #253 (tokens=121): `Caesar ad flumen Tamesim in fines Casivellauni exerci- tum duxit; quod flumen un`
- **First Latin Reader (Chickering)** #0 (tokens=96): `Introduetion . ...... eee  ut Fàábulae: L Ecce Aenégs in [talia ... 5... ss. IL,`
- **Hobbitus Ille (Tolkien 拉语版)** #604 (tokens=116): `"ja est, si ducenta milia passuum e uia ad septentrionem, et bis tantum ad merid`
- **Oxford Latin Course Part 3, 2e** #198 (tokens=112): `vivere artem colendi causa. multàs tamen puellas amàverat, à               marri`
- *...还有 25 段*

## Cap.41 (RA Cap.XLI)

**数据**: 新词 842 / 累计 17930 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 6 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #47 (tokens=217): `Quid? signum Paeanis ex aede Aesculapi praeclare factum, sacrum ac religiosum, n`
- **Pro Patria (Sonnenschein 1907)** #74 (tokens=150): `54. Altera victoria cius diei in Terra Natali reportata est, ubi Fabius ille nos`
- **Fabulae Faciles (Ritchie 1889)** #143 (tokens=145): `His rebus ita confectis, Ulysses cum sociis, maxime veritus ne Polyphemus fraude`
- **Fabulae Faciles (Ritchie 1889)** #155 (tokens=141): `Ulysses autem, ubi sensit eam timore perterritam esse, postulavit, ut socios sin`
- **First Latin Reader (Chickering)** #274 (tokens=143): `multitüdo à tribünis avertit et secüta Scipionem est, nec quisquam omnino cum il`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Wheelock's Latin Reader** #201 (tokens=182): `(a) The dual nature of the soul: (1) appetite; (2) reason, to govern the appetit`
- **ars_amatoria** #187 (tokens=131): `invenit, et làümen quod fuit ante redit: sic, ubi pigra sitü sécüraque pectora t`
- **Latin Reader for Lower Forms (Hardy 1889)** #135 (tokens=109): `Augusto post Áctiacam victoriam Romam reverso inter gratulantes occurrit opifex `
- **Latin Reader for Lower Forms (Hardy 1889)** #204 (tokens=100): `Sertorius corporis robore atque animi consilio eximius, dux Lusitanorum factus, `
- **Second Year Latin (Greenough 1899)** #27 (tokens=93): `superábant Corinthios. Artem bellicam contemnébant,! con- trà summo cum studio o`
- *...还有 25 段*

## Cap.42 (RA Cap.XLII)

**数据**: 新词 1258 / 累计 19188 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 10 | 🧩D段 2

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #228 (tokens=189): `M. Atilius Regulus, cum consul iterum in Africa ex insidiis captus esset, iuratu`
- **Wheelock's Latin Reader** #87 (tokens=175): `Si haec non ad cives Romanos, non ad aliquos amicos nos- trae civitatis, non ad `
- **Hobbitus Ille (Tolkien 拉语版)** #574 (tokens=163): `mihi licet dicere ursos paruos, ursos magnos, ursos usitatos, et ursos ingentes `
- **Hobbitus Ille (Tolkien 拉语版)** #823 (tokens=139): `non procul ab ora Fluminis Siluestris erat oppidum insolitum de quo dryades in a`
- **Second Year Latin (Greenough 1899)** #68 (tokens=131): `1. Imperátor Rómànus olim spectaculum splendidum para- vit ut populum délectáret`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Cambridge Latin Course 4** #306 (tokens=148): `decurrere ad litus. hi moles, hi proximas scaphàs conscendere; alit, quantum cor`
- **Wheelock's Latin Reader** #336 (tokens=130): `Ventum deinde ad multo angustiorem rupem atque ita rectis saxis ut aegre expedit`
- **Wheelock's Latin Reader** #11 (tokens=131): `Huic ego causae, iudices, cum summa voluntate et exspec- tatione populi Romani, `
- **ars_amatoria** #63 (tokens=116): `Illa leget tempus (medici quoque tempora servant) quo facilis dominae mens sit e`
- **Latin Reader for Lower Forms (Hardy 1889)** #158 (tokens=117): `Saevi mores et crudeles inter eos, qui nec iura divina nec humana cognoverunt, r`
- *...还有 25 段*

## Cap.43 (RA Cap.XLIII)

**数据**: 新词 1055 / 累计 20243 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 5 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Epitome Historiae Sacrae** #423 (tokens=180): `Antiochus enim, Syriae rex, aras falsis diis per universam Iüdaeam exstrui, atqu`
- **Latin Reader (Reynolds)** #326 (tokens=177): `Hi paulátim cónsuéscébant Rhenum trànsire et in Galliam venire optimósque agros `
- **Intermediate Oral Latin Reader** #87 (tokens=168): `Venió nune ad voluptátés agricolarum, quibus ego in- crédíbiliter déléctor, quae`
- **Epitome Historiae Sacrae** #473 (tokens=162): `t ecce homo quidam iüris peritus surrexit dicens: *Magi- E. quid faciendo vitam `
- **Wheelock's Latin Reader** #350 (tokens=155): `Dictator, exercitu consulis accepto, in viam Latinam est egressus, unde itinerib`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Cambridge Latin Course 1** #118 (tokens=119): `Theodorus, postquam hanc sententiam audivit, respondit,                 10 sente`
- **Latin Reader for Lower Forms (Hardy 1889)** #213 (tokens=103): `* Odati cireumspice, auream phialam vini plenam ei, quemcunque maritum optas, tu`
- **First Latin Reader (Chickering)** #1 (tokens=104): `XXI. Gali Superantur .. ..........   44 XXII. T. Manlius Torquàtus . . ........ `
- **Regulus (Saint-Exupéry 拉语版)** #145 (tokens=102): `VUL. — Aetatem nimis aequabiliter ago. Ego venor gallinas, homines me. Omnes aut`
- **Wheelock's Latin Reader** #182 (tokens=102): `(c) Motives for injustice. Atque illae quidem iniuriae quae nocendi causa de ind`
- *...还有 25 段*

## Cap.44 (RA Cap.XLIV)

**数据**: 新词 1419 / 累计 21662 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 9 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #231 (tokens=193): `Sed, ut laudandus Regulus in conservando 1ure, sic decem illi quos post Cannense`
- **De Rerum Natura (Lucretius 拉语版)** #173 (tokens=182): `pereunt, et fiunt anademata, mitrae; heredes, amore cuiusdam feminae flagrantes,`
- **Latin Reader (Reynolds)** #351 (tokens=168): `in castris aut in itinere tenéret, et quod constábat paucis ménsibus patrem M. C`
- **De Rerum Natura (Lucretius 拉语版)** #202 (tokens=160): `eam propagando. Nam omnia quae vides aere vitàli frui, vel dolus, vel fortitudo,`
- **Wheelock's Latin Reader** #327 (tokens=159): `Missus Hannibal in Hispaniam primo statim adventu om- nem exercitum in se conver`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader for Lower Forms (Hardy 1889)** #292 (tokens=232): `involare. Atque in hoc genere reperiuntur quidam mire dextri; dicas esse Mercuri`
- **Second Year Latin (Greenough 1899)** #90 (tokens=142): `Tandem cum adpararétur prandium faeneràátori, deside- ráta* est olla. Hic iürgiu`
- **ars_amatoria** #132 (tokens=113): `magicus -a -um; ars magica: quà res contrà nàtüram fieri videntur dé-currere — c`
- **Wheelock's Latin Reader** #497 (tokens=108): `Iam dies alibi, illic nox omnibus noctibus nigrior densi- orque; quam tamen face`
- **ars_amatoria** #236 (tokens=107): `140 ut pateant aures, ora rotunda volunt. Alterius crines umero iactentur utroqu`
- *...还有 25 段*

## Cap.45 (RA Cap.XLV)

**数据**: 新词 1222 / 累计 22884 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 13 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #249 (tokens=179): `intuetur sui. Quocirca et absentes adsunt et egentes abundant et imbecilli valen`
- **Intermediate Oral Latin Reader** #60 (tokens=140): `Vidétisne, u& apud Homérum saepissimé Nestor! dé virtütibus suis praedicet? Tert`
- **Wheelock's Latin Reader** #468 (tokens=137): `Mirum est quam singulis diebus in urbe ratio aut constet aut constare videatur, `
- **ars_amatoria** #148 (tokens=127): `Lite fugent nuptaeque viros nuptasque mariti inque vicem credant res sibi semper`
- **Second Year Latin (Greenough 1899)** #110 (tokens=133): `5. Eratautem Babylon urbs opulentissima * et potentissima ad Euphrátem flümen si`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Second Year Latin (Greenough 1899)** #64 (tokens=142): `làris cum virginali verécundià. Ut illa patris cervicibus! inhaerébat! Ut nós am`
- **Latin Made Simple** #132 (tokens=98): `Omnia tempus habent, et suis spatiis transeunt universa sub caelo. Tempus nascen`
- **Latin Reader for Lower Forms (Hardy 1889)** #142 (tokens=91): `Homo quidam cum Satyro amicitiam habuit. Apud quem quum edendi causa homo sedere`
- **First Latin Reader (Chickering)** #485 (tokens=81): `Issa (e)st passere néquior Catulli, Issa (e)st pürior osculo columbae, Issa (e)s`
- **Teach Yourself Beginner's Latin** #71 (tokens=72): `(Nero) ut erat reclinis et nescio similis solitum ita ait per comitialem morbum `
- *...还有 25 段*

## Cap.46 (RA Cap.XLVI)

**数据**: 新词 1251 / 累计 24135 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 11 | 🧩D段 2

### 📖 流畅 (hybrid ≥ 80%)
- **Oxford Latin Course Part 3, 2e** #29 (tokens=258): `discessit; Brütum in Asiam secütus est.' Flaccus 'quid dicis, carissima?' inquit`
- **catilina** #72 (tokens=206): `némo qui nón oderit! Quae nota domesticae turpitüdinis non inusta vitae tuae est`
- **First Latin Reader (Chickering)** #189 (tokens=156): `pácem petere coegit. Hanc autem Ttégulus noluit nisi dürissimis condicionibus da`
- **Latin Reader (Reynolds)** #327 (tokens=188): `in Lingonibus tenéret, nondum perspexerat; et cuius ab- sentis amicitià ante& ni`
- **Latin by the Natural Method (W.G. Most 1957)** #461 (tokens=171): `Rex ergo praecépit ut Ioséphus adducerétur ad se. Cum Ioséphus staret coram rege`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Via Latina: Easy Latin Reader (Collar 1897)** #167 (tokens=123): `Bellis civilibus confectis, conversus iam ad Ordinan- dum rei püblicae statum, f`
- **Cambridge Latin Course 4** #295 (tokens=127): `placuit Neroni calliditas Aniceti; praeterea occasio optima rei temptandae adera`
- **Wheelock's Latin Reader** #15 (tokens=120): `socii fidelissimi in hostium numero existimati; cives Romani servilem in modum c`
- **catilina** #148 (tokens=103): `cum sé praetüra abdicasset, in cüstodiam tràderétur'; itemque *uti C. Cethegus, `
- **ars_amatoria** #244 (tokens=113): `Aurea quae splendent ornàto signa theàtro Inspice quam tenuis brattea ligna tega`
- *...还有 25 段*

## Cap.47 (RA Cap.XLVII)

**数据**: 新词 595 / 累计 24730 词族 | 📖流畅 30 | 💪挑战 29 | 📚节选 2 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Second Year Latin (Greenough 1899)** #101 (tokens=160): `i. Réx inlüstrissimus Persàrum Cyrus fuit. historiae mirábilées dé pueritià eius`
- **Latin by the Natural Method (W.G. Most 1957)** #361 (tokens=140): `Quodam die magíster in schola nos interrogávit, *Ubi est terra Sénaar?" Díximus `
- **Wheelock's Latin Reader** #161 (tokens=118): `Sed cum statuissem scribere ad te aliquid hoc tempore (multa posthac), ab eo ord`
- **Hobbitus Ille (Tolkien 拉语版)** #448 (tokens=112): `tibi dicam illa, quae Gandalphus audiuit, quamquam Bilbo illa non intellexit. wa`
- **De Rerum Natura (Lucretius 拉语版)** #224 (tokens=109): `Id genus hominum in agris errantium multo dürius fuit (ut necesse erat, cum dura`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Ecce Romani IIB** #312 (tokens=128): `quártus, -a, -um, fourtb (38) quártus décimus, -a, -um, fourteentb (38) quási, a`
- **Latin Made Simple** #346 (tokens=121): `His ego nec metas rerum nec tempora pono; imperium sine fine dedi. Quin aspera J`
- **Cambridge Latin Course 2** #203 (tokens=118): `multus sanguis ex vulnere Barbilli efflu&bat. Phormio, qui servos        vulnere`
- **Ecce Romani III** #215 (tokens=103): `Angit me Fanniae valétüdo. Contráxit hanc dum assidet Tüniae virgini, sponte pri`
- **Pugio Bruti (Polis)** #1 (tokens=56): `Capitulum sextum decimum... Capitulum septimum decimum . Capitulum duodévicésimu`
- *...还有 24 段*

## Cap.48 (RA Cap.XLVIII)

**数据**: 新词 2085 / 累计 26815 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 13 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #268 (tokens=227): `Sed (saepe enim redeo ad Scipionem cuius omnis sermo erat de amicitia) querebatu`
- **De Rerum Natura (Lucretius 拉语版)** #119 (tokens=217): `nos carpimus et gustamus omnes tuas sententias aureds; aureas, inquam, et quae s`
- **catilina** #68 (tokens=210): `audaciae satellitem atque administrum tuae'? Num me fefellit, Catilina, non modo`
- **Latin Reader (Reynolds)** #255 (tokens=204): `rum auxilio Aedui victi et coácti sunt Sequanis obsidés dare et iüráre sésé nequ`
- **Wheelock's Latin Reader** #381 (tokens=134): `Nulla profecto alia gens tanta mole cladis non obruta esset. P. Furius Philus et`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Reading Latin: Grammar (2e)** #152 (tokens=186): `ad Ianitorem, uirum summae grauitatis, Lampsaceni eum dedüxerunt. iste autem — 5`
- **Ora Maritima (Sonnenschein 1900)** #22 (tokens=123): `20. * Multi mortuos cremabant, sicut Graeci et Rómàni: exstant in Cantio sepulch`
- **Latin Reader for Lower Forms (Hardy 1889)** #237 (tokens=102): `Caesar adit reliquos ; cohortatur ne labori succumbant ; omnium superiorum dimic`
- **Ecce Romani III** #231 (tokens=101): `Tam nàvibus cinis incidébat, quo propius accéderent, calidior et densior; iam 16`
- **Second Year Latin (Greenough 1899)** #163 (tokens=104): `4. Déleétis? Teutonibus C. Marius in Cimbros sé convertit. Qui cum ex alià parte`
- *...还有 25 段*

## Cap.49 (RA Cap.XLIX)

**数据**: 新词 670 / 累计 27485 词族 | 📖流畅 30 | 💪挑战 27 | 📚节选 5 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader for Lower Forms (Hardy 1889)** #216 (tokens=119): `Rex studiosus iocorum prope pontem, quo flumen multi transibant, omnes, quieunqu`
- **Via Latina: Easy Latin Reader (Collar 1897)** #166 (tokens=114): `Deinde Caesar in Epirum profectus Pompéium Phar- salico proelio füdit, et fugien`
- **Hobbitus Ille (Tolkien 拉语版)** #289 (tokens=113): `post tempus nonnullum fumisugium temptauit. quod non est fractum, quod aliquantu`
- **Via Latina: Easy Latin Reader (Collar 1897)** #189 (tokens=111): `Neque tamen à càáritàte patriae potuit recedere. Nam cum apud Aegos flümen Philo`
- **Latin Stories (Wheelock 配套)** #31 (tokens=109): `Nunc aetas magna atque nova incipit. Puer nascitur ac gens aurea venit. Mundus g`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Teach Yourself Beginner's Latin** #240 (tokens=78): `1 (a) Si illi discipuli Danos non timerent, stulti essent; if those students wer`
- **Latin Reader for Lower Forms (Hardy 1889)** #211 (tokens=75): `Daphitas eius studii erat, quod qui profitentur sophistae vocantur, homo ineptae`
- **Ecce Romani IIB** #49 (tokens=72): `Lydia Arachneé, peritissima omnium puellàrum quae telas texebant, per urbes Lydi`
- **Beginner's Latin Book (Textkit)** #261 (tokens=61): `I. 1. Remus irridóüs mürum trünsiliit. 9. Abi hine, oblita! frütrum, oblita! pat`
- **Latin for Beginners (D'Ooge)** #71 (tokens=48): `Cowj.  PREs. STEM      Pass, Drums          Pars ImpueirivE I        ama-       `
- *...还有 22 段*

## Cap.50 (RA Cap.L)

**数据**: 新词 1523 / 累计 29008 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 14 | 🧩D段 3

### 📖 流畅 (hybrid ≥ 80%)
- **Latin by the Natural Method (W.G. Most 1957)** #620 (tokens=211): `Et nuntiátum est regi Aegyptiórum quod fugísset pópulus; immutatüm- que est cor `
- **Wheelock's Latin 7e** #522 (tokens=156): `. Régi persuási ut soróri frátrique tuó grátióra praemia libenter daret. . Deind`
- **Via Latina: Easy Latin Reader (Collar 1897)** #177 (tokens=139): `qui in oppido erant Athenis déicerentur praeter ünum, qui ante iànuam erat Andoc`
- **Wheelock's Latin Reader** #246 (tokens=144): `Talis igitur inter viros amicitia tantas opportunitates habet quantas vix queo d`
- **Wheelock's Latin Reader** #183 (tokens=123): `(d) Justice in special cases: (1) Promises. Sed incidunt saepe tempora cum ea qu`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Latin Reader for Lower Forms (Hardy 1889)** #227 (tokens=119): `Cum M. Antonius, quidquid mari aut terra aut etiam aere gigneretur, ad satiandam`
- **Hobbitus Ille (Tolkien 拉语版)** #572 (tokens=115): `demum Gandalphus, patella urceoque expulsis — duos panes totos (butyro multo et `
- **Ecce Romani III** #198 (tokens=91): `"Té rogo ut nàvés etiam in monumento meo facias plenis velis euntes, et mé in tr`
- **Intermediate Oral Latin Reader** #71 (tokens=82): `1. Tertia vituperátio senectütis est quod omnibus volup- tàtibus careat. 2. Itaq`
- **Hobbitus Ille (Tolkien 拉语版)** #3 (tokens=81): `quod ianuam omnino rotundam, fenestrae nauis similem, uiridem pictam cum "bulla `
- *...还有 25 段*

## Cap.51 (RA Cap.LI)

**数据**: 新词 812 / 累计 29820 词族 | 📖流畅 30 | 💪挑战 27 | 📚节选 1 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Via Latina: Easy Latin Reader (Collar 1897)** #195 (tokens=208): `miserant, qui eum certiorem facerent, nisi Alcibiadem sus- tulisset, nihil earum`
- **Latin Reader (Reynolds)** #343 (tokens=192): `aut nàvis nacti trünsiére aut viribus confisi tránüre con- tendérunt. In his fui`
- **Wheelock's Latin Reader** #303 (tokens=157): `Ac nescio an, nimis undique eam minimisque rebus muni- endo, modum excesserint. `
- **Latin Stories (Wheelock 配套)** #48 (tokens=145): `Oratores veroó Romani éloquentiam Latinam Graecae parem facere possunt; nam Cice`
- **Latin by the Natural Method (W.G. Most 1957)** #320 (tokens=134): `Cum creavísset primos hómines, Adam et Evam, Deus imperávit eis ne        Obedív`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #451 (tokens=113): `coepisset, etiamsi magus fuit, atque sentire se ipsos esse in loco pessimo et ne`
- **Hobbitus Ille (Tolkien 拉语版)** #785 (tokens=111): `mox tredecim inuenerunt, quaque ad nanum habili. re uera, aliquae fuerunt spatio`
- **Wheelock's Latin 7e** #925 (tokens=95): `Aug., St. Augustine Conf., Confessions Caes., Caesar B Civ, Bellum Civile B Gall`
- **Latin Reader for Lower Forms (Hardy 1889)** #183 (tokens=93): `Apis quum quondam, ut diis sacra faceret, Olympum accessisset, Iovi mellis donum`
- **Wheelock's Latin Reader** #331 (tokens=71): `Hannibal a Druentia campestri maxime itinere ad Alpes cum bona pace incolentium `
- *...还有 22 段*

## Cap.52 (RA Cap.LII)

**数据**: 新词 1458 / 累计 31278 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 4 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader (Reynolds)** #256 (tokens=206): `erat grátià apud Suebam uxorem et filiam novem annórum, eui nomen erat Velaeda. `
- **Latin Reader (Reynolds)** #311 (tokens=198): `véra: Ipsum esse Dumnorigem, summà& audácià, magn& apud plebem propter liberalit`
- **Latin Reader (Reynolds)** #300 (tokens=176): `Helvétii eorum finis populàrentur: ita sé omni tempore dé populo Rómánó meritos `
- **Latin Reader (Reynolds)** #366 (tokens=148): `prius visi sunt, quam castris appropinquàrent üsque eo, uti puer et puella, qui `
- **De Rerum Natura (Lucretius 拉语版)** #102 (tokens=136): `Tellus continet in se primordia illa, quibus fit ut fontes, qui fluviorum frigid`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **First Latin Reader (Chickering)** #634 (tokens=136): `F fabula, fabulae, f. (i)............(vide dériv.). FACILIS, facile (xxi). .....`
- **Second Year Latin (Greenough 1899)** #34 (tokens=126): `etiam," respondet lupus, "pater tuus contuméliosé quondam 15 dixit dé avià meà" `
- **First Latin Reader (Chickering)** #704 (tokens=119): `püblic&tum (lxviii)............(vidé deriv.). PÜBLICUS, pübliea, püblieum (ix). `
- **De Rerum Natura (Lucretius 拉语版)** #243 (tokens=99): `V. 1011-1027 Inde casas postquam ac pelles ignemque pararunt et mulier coniüncta`
- **Hobbitus Ille (Tolkien 拉语版)** #610 (tokens=85): `res uidere assuescebant, aliquando e uia festinantes et post truncos arborum dis`
- *...还有 25 段*

## Cap.53 (RA Cap.LIII)

**数据**: 新词 832 / 累计 32110 词族 | 📖流畅 30 | 💪挑战 26 | 📚节选 2 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Latin Reader (Reynolds)** #288 (tokens=162): `ire nón possent; alterum per provinciam Romànam, multo facilius atque expeditius`
- **Via Latina: Easy Latin Reader (Collar 1897)** #193 (tokens=147): `At Alcibiades, victis Athéniensibus non satis tüta eadem loca sibi arbitráàns, p`
- **Pro Patria (Sonnenschein 1907)** #48 (tokens=118): `incolunt, Coloniam nostram Africanam quondam incolebant. Í Sed abhinc annos quin`
- **catilina** #35 (tokens=116): `Postquam accépére ea hominés, quibus mala abundé omnia erant, sed neque res nequ`
- **Intermediate Oral Latin Reader** #66 (tokens=112): `At minus habeo virium quam vestrum utervis  N8& vos quidem 'T. Pontii centurioni`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **De Rerum Natura (Lucretius 拉语版)** #296 (tokens=127): `Deinde etiam pàstor et armentarius quisque et eodem modo robustus agricola regen`
- **Pro Patria (Sonnenschein 1907)** #102 (tokens=35): `Sb m        habu-i                habu-eram                 habu-eró 2        ha`
- **Second Year Latin (Greenough 1899)** #88 (tokens=106): `Antónius sacrificus invitàrat ünum atque alterum bellum homunculum forte obvios `
- **Latin Reader for Lower Forms (Hardy 1889)** #150 (tokens=86): `Protagoras sophista acerrimus cum Evathlo discipulo simultatem gessit: super pac`
- **Reading Latin: Grammar (2e)** #175 (tokens=61): `ita prima Haluntinorum nàuis capitur, cui praeerat Haluntinus homo nobilis, Phyl`
- *...还有 21 段*

## Cap.54 (RA Cap.LIV)

**数据**: 新词 1170 / 累计 33280 词族 | 📖流畅 30 | 💪挑战 30 | 📚节选 3 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Intermediate Oral Latin Reader** #110 (tokens=232): `mortem omni aetüti esse commünem. — At sperat adules- cens diü sé victürum, quod`
- **Hobbitus Ille (Tolkien 拉语版)** #9 (tokens=210): `aut supra Collem aut trans Aquam inueniri potuit, aedificauit, et ibi ad supremo`
- **Wheelock's Latin Reader** #45 (tokens=132): `aedem Felicitatis, ad monumentum Catuli, in porticum Metelli; det operam ut admi`
- **Fabulae Faciles (Ritchie 1889)** #129 (tokens=128): `Dum filiae regis hoc miraculum stupentes intuentur, Medea ita locuta est. *''Vid`
- **Via Latina: Easy Latin Reader (Collar 1897)** #38 (tokens=128): `Dum filiae régis hoc miraculum stupentées intuentur, Médéa ita locüta est.  * Vi`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Cambridge Latin Course 4** #209 (tokens=139): `interim legatus provinciae tres latrones iussit crucibus affigi                 `
- **Wheelock's Latin Reader** #493 (tokens=122): `Interim e Vesuvio monte pluribus locis latissimae flammae altaque incendia reluc`
- **Latin Reader for Lower Forms (Hardy 1889)** #147 (tokens=91): `E quibus unus, qui socios retinuerat, rogavit, quamobrem tanta celeritate domum `
- **Beginner's Latin Book (Textkit)** #282 (tokens=83): `Rüsticus in agrós exiit ad opus suum.  Filiolum, qui in cinis jacebat, reliquit `
- **Hobbitus Ille (Tolkien 拉语版)** #850 (tokens=81): `alii cantus fuerunt ueteres; sed alii fuerunt nouiores, qui fidenter de repente `
- *...还有 25 段*

## Cap.55 (RA Cap.LV)

**数据**: 新词 969 / 累计 34249 词族 | 📖流畅 30 | 💪挑战 11 | 📚节选 9 | 🧩D段 1

### 📖 流畅 (hybrid ≥ 80%)
- **Wheelock's Latin Reader** #266 (tokens=221): `Quis est—pro deorum fidem atque hominum!— qui velit, ut neque diligat quemquam n`
- **Pro Patria (Sonnenschein 1907)** #27 (tokens=133): `T 18. Postridie inter ientaculum amita mea: * Caelum hodie serenissimum est"' in`
- **catilina** #84 (tokens=126): `Ibis tandem aliquando quó té iam pridem tua ista cupiditas effrenata ac furiosa `
- **Wheelock's Latin Reader** #134 (tokens=125): `Lippitudinis meae signum tibi sit librari manus et eadem causa brevitatis, etsi `
- **Wheelock's Latin 7e** #831 (tokens=120): `8. Nüntiàvérunt ducem quam fortissimum vénisse. 9. Lüce clarissima ab quattuor v`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #439 (tokens=116): `quam umquam ramis confidere potuerunt. tu riseris (a distantia tuta), si nanos i`
- **Second Year Latin (Greenough 1899)** #43 (tokens=112): `dam asinum! condüxerat, quó Athenis Megaram veherétur. Media fere? vià cum aestu`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #429 (tokens=100): `1. Audimus optimam cantátricem.              Jl ———— 2. Quam partem agis ?      `
- **First Latin Reader (Chickering)** #588 (tokens=84): `tionum, f. (xli)...........Luu.(vidé deriv.). ADOLESCO, adolescere, adolévi, adu`
- **Wheelock's Latin 7e** #450 (tokens=61): `1. Eum patientem haec mala hortàti sunt. They encouraged him (as he was) sufferi`
- *...还有 6 段*

## Cap.56 (RA Cap.LVI)

**数据**: 新词 778 / 累计 35027 词族 | 📖流畅 30 | 💪挑战 19 | 📚节选 1 | 🧩D段 0

### 📖 流畅 (hybrid ≥ 80%)
- **Hobbitus Ille (Tolkien 拉语版)** #874 (tokens=138): `nunc, mirabile dictu, plus Domino Bagginsi quam ceteris fuit. saepe tabulam geog`
- **Cambridge Latin Course 4** #261 (tokens=110): `nam vehicula, quae prodüct iusseramus, quamquam in plànissimoó campo, in contrar`
- **Intermediate Oral Latin Reader** #31 (tokens=95): `urbium expugnaàtionés, ut pedestrés! nàvàlés-ve pugnis, ut bella à sé gesta, ut `
- **Sermones Romani (Menaechmi 选段)** #89 (tokens=90): `-             "ZU      [a]         -           .          - 5 vulpes hunc vidit,`
- **Hobbitus Ille (Tolkien 拉语版)** #650 (tokens=85): `re uera, ut tibi dixi, non procul a margine siluae afuerunt; et si Bilboni ingen`
- *...还有 25 段*

### 💪 挑战 (hybrid ≥ 70%)
- **Hobbitus Ille (Tolkien 拉语版)** #467 (tokens=77): `gobelini irati atque attoniti ululauerunt. magna uoce Dominus Aquilarum, cui Gan`
- **Forum - Lectiones Latinitatis Vivae (Polis)** #280 (tokens=75): `l. Propone vinum magistro tuo.             A ——M M 2. Studet fábulae mirae. e — `
- **Latin Reader (Reynolds)** #118 (tokens=57): `Solida in longitüdinem, in látitüdinem, et in crassitüdinem métimur. Circuli in `
- **De Rerum Natura (Lucretius 拉语版)** #317 (tokens=49): `R radius -1 7 10.3; 38. I1,60 rancidus -a -um 126. VI,1155 rapax -àacis 19. 1,17`
- **Cambridge Latin Course 3** #391 (tokens=36): `loquor loqueris loquitur loquimur loquimini loquuntur loquebar loquebaris loqueb`
- *...还有 14 段*
