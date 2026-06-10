# LLPSI 56 章扩展读物路由表

**生成日期**: 2026-06-08 | **覆盖**: FR Cap.1-35 + RA Cap.36-56

## 路由规范 (5个维度, v3.1 hybrid混合分)

| 标签 | 维度 | 含义 | hybrid 阈值 | 起点判定 |
|------|------|------|-------------|----------|
| 📖 可读 | readable (可读) | 学完本章后 hybrid ≥ 80% | **≥ 80%** | `starting_ch_token_80 = 本章` |
| 💪 挑战 | challenging (挑战可读) | 学完本章后 hybrid ≥ 70% | **≥ 70%** | `starting_ch_token_70 = 本章` |
| 📚 节选 | selected (片段可读) | 学完本章后 hybrid ≥ 50% | **≥ 50%** | `starting_ch_token_50 = 本章` |
| 📖 复习 | best_teach (复习价值) | 本书覆盖本章新词最多 | 教学 | `best_teach_chapter = 本章` |
| 🧩 段 | D类拉语段 | 本章对应可抽取的拉语故事段 | **≥ 60% form** | `seg.starting_ch60 = 本章` |

**v3.1 关键**: 使用 **hybrid 混合分** (LLPSI直接匹配 ×1.0 + LLPSI总表但未学到 ×0.5).
教材型读物(剑桥/牛津/ECCE)中大量拉丁词虽不在 LLPSI Cap.1-5 词表，但在 LLPSI 的总词表中，
给予 0.5 权重后教材评级显著提升。

## Cap.1 (FR Cap.I)

**章节数据**: 新词 204 / 新词密度 23.6% / 累计 163 词形 (204 词族)

### 📚 节选读物 (1)
- `via_latina_romanorum` (Via Latina: De Lingua et Vita Romanorum): readable, h50 Cap.1, pkH=89%, 教学 Cap.1(63%), 6,267独词

### 📖 复习读物 (28)
- `wheelock_7e` (Wheelock's Latin 7e): 教学 Cap.1(66%), pkT=45%, 26,310独词
- `chickering` (First Latin Reader (Chickering)): 教学 Cap.1(65%), pkT=73%, 15,124独词
- `via_latina_romanorum` (Via Latina: De Lingua et Vita Romanorum): 教学 Cap.1(63%), pkT=87%, 6,267独词
- ... (25 本省略)

### 🧩 拉语段 (18)
- `latin_natural_method` p.103-109 (7页): 60%起点 Cap.—, 教学 Cap.1(17%), 577独词
- `dooge_beginners` p.214-219 (6页): 60%起点 Cap.40, 教学 Cap.1(16%), 622独词
- `dooge_beginners_2` p.214-219 (6页): 60%起点 Cap.44, 教学 Cap.1(15%), 635独词
- ... (15 段省略)

## Cap.2 (FR Cap.II)

**章节数据**: 新词 182 / 新词密度 21.2% / 累计 326 词形 (386 词族)

### 📚 节选读物 (1)
- `pugio_bruti` (Pugio Bruti (Polis)): readable, h50 Cap.2, pkH=82%, 教学 Cap.4(26%), 1,656独词

### 🧩 拉语段 (1)
- `reading_latin_text` p.315-318 (4页): 60%起点 Cap.—, 教学 Cap.2(5%), 368独词

## Cap.3 (FR Cap.III)

**章节数据**: 新词 96 / 新词密度 16.0% / 累计 416 词形 (482 词族)

### 📖 复习读物 (2)
- `cambridge_1` (Cambridge Latin Course 1): 教学 Cap.3(38%), pkT=44%, 5,922独词
- `olimpia_nicholas` (The Mysterious Traveler (Olimpi)): 教学 Cap.3(19%), pkT=66%, 1,273独词

### 🧩 拉语段 (2)
- `cambridge_1` p.54-57 (4页): 60%起点 Cap.—, 教学 Cap.3(1%), 16独词
- `dooge_beginners_2` p.221-223 (3页): 60%起点 Cap.41, 教学 Cap.3(11%), 355独词

## Cap.4 (FR Cap.IV)

**章节数据**: 新词 139 / 新词密度 19.0% / 累计 542 词形 (621 词族)

### 📖 复习读物 (9)
- `latin_lower_forms` (Latin Reader for Lower Forms (Hardy 1889)): 教学 Cap.4(53%), pkT=65%, 16,481独词
- `oxford_2` (Oxford Latin Course Part 2, 2e): 教学 Cap.4(49%), pkT=53%, 10,333独词
- `illiterati_2` (More Latin for the Illiterati (Stone)): 教学 Cap.4(48%), pkT=33%, 14,425独词
- ... (6 本省略)

### 🧩 拉语段 (10)
- `latin_natural_method` p.153-166 (14页): 60%起点 Cap.—, 教学 Cap.4(21%), 1,159独词
- `latin_natural_method` p.128-140 (13页): 60%起点 Cap.—, 教学 Cap.4(23%), 1,072独词
- `latin_natural_method` p.117-126 (10页): 60%起点 Cap.—, 教学 Cap.4(19%), 861独词
- ... (7 段省略)

## Cap.5 (FR Cap.V)

**章节数据**: 新词 187 / 新词密度 20.3% / 累计 717 词形 (808 词族)

### 📚 节选读物 (3)
- `latin_natural_method` (Latin by the Natural Method (W.G. Most 1957)): challenging, h50 Cap.5, pkH=75%, 教学 Cap.1(51%), 10,349独词
- `forum_lectiones` (Forum - Lectiones Latinitatis Vivae (Polis)): challenging, h50 Cap.5, pkH=75%, 教学 Cap.5(59%), 9,775独词
- `diocles_flora` (Dioclēs et Flōra (Polis)): challenging, h50 Cap.5, pkH=76%, 教学 Cap.5(32%), 3,723独词

### 📖 复习读物 (8)
- `forum_lectiones` (Forum - Lectiones Latinitatis Vivae (Polis)): 教学 Cap.5(59%), pkT=70%, 9,775独词
- `cambridge_4` (Cambridge Latin Course 4): 教学 Cap.5(54%), pkT=42%, 17,310独词
- `ecce_romani_2a` (Ecce Romani IIA): 教学 Cap.5(51%), pkT=47%, 11,928独词
- ... (5 本省略)

### 🧩 拉语段 (2)
- `cambridge_1` p.4-7 (4页): 60%起点 Cap.—, 教学 Cap.5(2%), 57独词
- `wileys_real_latin` p.366-368 (3页): 60%起点 Cap.43, 教学 Cap.5(6%), 242独词

## Cap.6 (FR Cap.VI)

**章节数据**: 新词 189 / 新词密度 18.2% / 累计 883 词形 (997 词族)

### 📚 节选读物 (3)
- `hobbitus` (Hobbitus Ille (Tolkien 拉语版)): challenging, h50 Cap.6, pkH=74%, 教学 Cap.11(46%), 14,830独词
- `regulus` (Regulus (Saint-Exupéry 拉语版)): challenging, h50 Cap.6, pkH=78%, 教学 Cap.4(34%), 4,207独词
- `olimpia_nicholas` (The Mysterious Traveler (Olimpi)): challenging, h50 Cap.6, pkH=73%, 教学 Cap.3(19%), 1,273独词

### 🧩 拉语段 (1)
- `dooge_beginners` p.221-223 (3页): 60%起点 Cap.42, 教学 Cap.6(10%), 362独词

## Cap.7 (FR Cap.VII)

**章节数据**: 新词 127 / 新词密度 12.9% / 累计 993 词形 (1124 词族)

### 📖 复习读物 (2)
- `teach_yourself` (Teach Yourself Beginner's Latin): 教学 Cap.7(37%), pkT=46%, 8,492独词
- `olimpia_pyramus` (Reckless Love: Pyramus and Thisbe (Olimpi)): 教学 Cap.7(24%), pkT=57%, 2,649独词

_(本章无D类拉语段推荐)_

## Cap.8 (FR Cap.VIII)

**章节数据**: 新词 216 / 新词密度 19.8% / 累计 1187 词形 (1340 词族)

### 📚 节选读物 (1)
- `chickering` (First Latin Reader (Chickering)): challenging, h50 Cap.8, pkH=74%, 教学 Cap.1(65%), 15,124独词

_(本章无D类拉语段推荐)_

## Cap.9 (FR Cap.IX)

**章节数据**: 新词 187 / 新词密度 20.0% / 累计 1355 词形 (1527 词族)

_(本章无D类拉语段推荐)_

## Cap.10 (FR Cap.X)

**章节数据**: 新词 264 / 新词密度 20.4% / 累计 1602 词形 (1791 词族)

### 📖 复习读物 (1)
- `wheelock_reader` (Wheelock's Latin Reader): 教学 Cap.10(58%), pkT=48%, 22,813独词

### 🧩 拉语段 (1)
- `cambridge_2` p.82-84 (3页): 60%起点 Cap.55, 教学 Cap.10(6%), 233独词

## Cap.11 (FR Cap.XI)

**章节数据**: 新词 224 / 新词密度 19.4% / 累计 1798 词形 (2015 词族)

### 📚 节选读物 (1)
- `unus_duo_tres` (Unus Duo Tres): selected, h50 Cap.11, pkH=66%, 教学 Cap.15(39%), 4,282独词

### 📖 复习读物 (1)
- `hobbitus` (Hobbitus Ille (Tolkien 拉语版)): 教学 Cap.11(46%), pkT=68%, 14,830独词

_(本章无D类拉语段推荐)_

## Cap.12 (FR Cap.XII)

**章节数据**: 新词 305 / 新词密度 22.7% / 累计 2057 词形 (2320 词族)

### 📖 复习读物 (2)
- `reynolds_reader` (Latin Reader (Reynolds)): 教学 Cap.12(57%), pkT=52%, 15,509独词
- `latin_made_simple` (Latin Made Simple): 教学 Cap.12(57%), pkT=47%, 11,899独词

_(本章无D类拉语段推荐)_

## Cap.13 (FR Cap.XIII)

**章节数据**: 新词 382 / 新词密度 26.2% / 累计 2375 词形 (2702 词族)

### 💪 挑战读物 (1)
- `via_latina_romanorum` (Via Latina: De Lingua et Vita Romanorum): readable, t70 Cap.13, pkH=89%, 教学 Cap.1(63%), 6,267独词

_(本章无D类拉语段推荐)_

## Cap.14 (FR Cap.XIV)

**章节数据**: 新词 255 / 新词密度 19.5% / 累计 2605 词形 (2957 词族)

### 📚 节选读物 (3)
- `latin_lower_forms` (Latin Reader for Lower Forms (Hardy 1889)): selected, h50 Cap.14, pkH=67%, 教学 Cap.4(53%), 16,481独词
- `fabulae_faciles` (Fabulae Faciles (Ritchie 1889)): selected, h50 Cap.14, pkH=66%, 教学 Cap.1(38%), 8,878独词
- `olimpia_pyramus` (Reckless Love: Pyramus and Thisbe (Olimpi)): selected, h50 Cap.14, pkH=63%, 教学 Cap.7(24%), 2,649独词

_(本章无D类拉语段推荐)_

## Cap.15 (FR Cap.XV)

**章节数据**: 新词 207 / 新词密度 20.2% / 累计 2786 词形 (3164 词族)

### 📚 节选读物 (3)
- `nutting_reader` (A First Latin Reader (Nutting)): selected, h50 Cap.15, pkH=65%, 教学 Cap.1(51%), 13,773独词
- `oxford_1` (Oxford Latin Course Part 1, 2e): english_mixed, h50 Cap.15, pkH=62%, 教学 Cap.5(42%), 6,744独词
- `olimpia_daedalus` (Daedalus et Icarus (Olimpi)): selected, h50 Cap.15, pkH=64%, 教学 Cap.1(21%), 2,388独词

### 📖 复习读物 (1)
- `unus_duo_tres` (Unus Duo Tres): 教学 Cap.15(39%), pkT=63%, 4,282独词

_(本章无D类拉语段推荐)_

## Cap.16 (FR Cap.XVI)

**章节数据**: 新词 375 / 新词密度 23.3% / 累计 3121 词形 (3539 词族)

### 📚 节选读物 (2)
- `reynolds_reader` (Latin Reader (Reynolds)): selected, h50 Cap.16, pkH=61%, 教学 Cap.12(57%), 15,509独词
- `latin_first_year_magoffin` (Latin First Year (Magoffin)): english_mixed, h50 Cap.16, pkH=61%, 教学 Cap.1(56%), 12,273独词

_(本章无D类拉语段推荐)_

## Cap.17 (FR Cap.XVII)

**章节数据**: 新词 274 / 新词密度 20.7% / 累计 3368 词形 (3813 词族)

### 📚 节选读物 (1)
- `ecce_romani` (Ecce Romani I): english_mixed, h50 Cap.17, pkH=58%, 教学 Cap.1(53%), 11,574独词

_(本章无D类拉语段推荐)_

## Cap.18 (FR Cap.XVIII)

**章节数据**: 新词 406 / 新词密度 21.7% / 累计 3690 词形 (4219 词族)

### 📚 节选读物 (4)
- `dooge_beginners_2` (Latin for Beginners (D'Ooge 另一版)): difficult, h50 Cap.18, pkH=60%, 教学 Cap.1(57%), 16,215独词
- `latin_made_simple` (Latin Made Simple): english_mixed, h50 Cap.18, pkH=60%, 教学 Cap.12(57%), 11,899独词
- `pro_patria` (Pro Patria (Sonnenschein 1907)): english_mixed, h50 Cap.18, pkH=59%, 教学 Cap.1(52%), 9,736独词
- `intermediate_oral_cicero` (Intermediate Oral Latin Reader): selected, h50 Cap.18, pkH=63%, 教学 Cap.1(44%), 9,238独词

_(本章无D类拉语段推荐)_

## Cap.19 (FR Cap.XIX)

**章节数据**: 新词 336 / 新词密度 21.7% / 累计 3981 词形 (4555 词族)

### 💪 挑战读物 (1)
- `pugio_bruti` (Pugio Bruti (Polis)): readable, t70 Cap.19, pkH=82%, 教学 Cap.4(26%), 1,656独词

### 📚 节选读物 (3)
- `dooge_beginners` (Latin for Beginners (D'Ooge)): difficult, h50 Cap.19, pkH=59%, 教学 Cap.1(58%), 16,413独词
- `oxford_2` (Oxford Latin Course Part 2, 2e): selected, h50 Cap.19, pkH=61%, 教学 Cap.4(49%), 10,333独词
- `septimus` (Septimus (Chambers 1910)): selected, h50 Cap.19, pkH=62%, 教学 Cap.4(41%), 8,701独词

_(本章无D类拉语段推荐)_

## Cap.20 (FR Cap.XX)

**章节数据**: 新词 355 / 新词密度 22.1% / 累计 4285 词形 (4910 词族)

### 📚 节选读物 (3)
- `wheelock_7e` (Wheelock's Latin 7e): english_mixed, h50 Cap.20, pkH=59%, 教学 Cap.1(66%), 26,310独词
- `conversational_latin` (Conversational Latin for Oral Proficiency): difficult, h50 Cap.20, pkH=57%, 教学 Cap.1(57%), 20,153独词
- `reading_latin_grammar` (Reading Latin: Grammar (2e)): english_mixed, h50 Cap.20, pkH=57%, 教学 Cap.4(46%), 15,208独词

_(本章无D类拉语段推荐)_

## Cap.21 (FR Cap.XXI)

**章节数据**: 新词 252 / 新词密度 19.4% / 累计 4507 词形 (5162 词族)

### 📚 节选读物 (1)
- `dooge_beginners_key` (D'Ooge Latin for Beginners Key): english_mixed, h50 Cap.21, pkH=59%, 教学 Cap.1(33%), 2,981独词

_(本章无D类拉语段推荐)_

## Cap.22 (FR Cap.XXII)

**章节数据**: 新词 312 / 新词密度 26.0% / 累计 4786 词形 (5474 词族)

### 📚 节选读物 (1)
- `oxford_3` (Oxford Latin Course Part 3, 2e): selected, h50 Cap.22, pkH=60%, 教学 Cap.1(49%), 13,139独词

_(本章无D类拉语段推荐)_

## Cap.23 (FR Cap.XXIII)

**章节数据**: 新词 270 / 新词密度 18.2% / 累计 5025 词形 (5744 词族)

_(本章无D类拉语段推荐)_

## Cap.24 (FR Cap.XXIV)

**章节数据**: 新词 245 / 新词密度 21.5% / 累计 5247 词形 (5989 词族)

_(本章无D类拉语段推荐)_

## Cap.25 (FR Cap.XXV)

**章节数据**: 新词 427 / 新词密度 27.4% / 累计 5637 词形 (6416 词族)

### 📚 节选读物 (4)
- `wheelock_reader` (Wheelock's Latin Reader): difficult, h50 Cap.25, pkH=58%, 教学 Cap.10(58%), 22,813独词
- `reading_latin_text` (Reading Latin: Text (2e)): difficult, h50 Cap.25, pkH=56%, 教学 Cap.4(46%), 18,543独词
- `second_year_latin` (Second Year Latin (Greenough 1899)): difficult, h50 Cap.25, pkH=59%, 教学 Cap.1(39%), 8,121独词
- `latin_stories_wheelock` (Latin Stories (Wheelock 配套)): difficult, h50 Cap.25, pkH=58%, 教学 Cap.1(36%), 5,684独词

_(本章无D类拉语段推荐)_

## Cap.26 (FR Cap.XXVI)

**章节数据**: 新词 360 / 新词密度 22.7% / 累计 5957 词形 (6776 词族)

### 📚 节选读物 (1)
- `wheelock_answer_key` (Wheelock's Latin 7e Answer Key): english_mixed, h50 Cap.26, pkH=56%, 教学 Cap.1(46%), 9,456独词

_(本章无D类拉语段推荐)_

## Cap.27 (FR Cap.XXVII)

**章节数据**: 新词 433 / 新词密度 23.4% / 累计 6355 词形 (7209 词族)

### 📚 节选读物 (2)
- `ecce_romani_2a` (Ecce Romani IIA): difficult, h50 Cap.27, pkH=56%, 教学 Cap.5(51%), 11,928独词
- `teach_yourself` (Teach Yourself Beginner's Latin): english_mixed, h50 Cap.27, pkH=56%, 教学 Cap.7(37%), 8,492独词

_(本章无D类拉语段推荐)_

## Cap.28 (FR Cap.XXVIII)

**章节数据**: 新词 440 / 新词密度 22.8% / 累计 6772 词形 (7649 词族)

### 📚 节选读物 (1)
- `wileys_real_latin` (Wiley's Real Latin (Maltby & Belcher)): english_mixed, h50 Cap.28, pkH=57%, 教学 Cap.1(47%), 11,867独词

_(本章无D类拉语段推荐)_

## Cap.29 (FR Cap.XXIX)

**章节数据**: 新词 434 / 新词密度 22.7% / 累计 7157 词形 (8083 词族)

_(本章无D类拉语段推荐)_

## Cap.30 (FR Cap.XXX)

**章节数据**: 新词 366 / 新词密度 22.2% / 累计 7463 词形 (8449 词族)

### 💪 挑战读物 (1)
- `diocles_flora` (Dioclēs et Flōra (Polis)): challenging, t70 Cap.30, pkH=76%, 教学 Cap.5(32%), 3,723独词

_(本章无D类拉语段推荐)_

## Cap.31 (FR Cap.XXXI)

**章节数据**: 新词 423 / 新词密度 21.8% / 累计 7815 词形 (8872 词族)

### 💪 挑战读物 (1)
- `regulus` (Regulus (Saint-Exupéry 拉语版)): challenging, t70 Cap.31, pkH=78%, 教学 Cap.4(34%), 4,207独词

### 📚 节选读物 (2)
- `cambridge_2` (Cambridge Latin Course 2): difficult, h50 Cap.31, pkH=55%, 教学 Cap.5(43%), 8,496独词
- `cambridge_1` (Cambridge Latin Course 1): english_mixed, h50 Cap.31, pkH=55%, 教学 Cap.3(38%), 5,922独词

_(本章无D类拉语段推荐)_

## Cap.32 (FR Cap.XXXII)

**章节数据**: 新词 470 / 新词密度 20.6% / 累计 8237 词形 (9342 词族)

### 📚 节选读物 (1)
- `beginners_latin_book` (Beginner's Latin Book (Textkit)): difficult, h50 Cap.32, pkH=55%, 教学 Cap.1(56%), 15,016独词

_(本章无D类拉语段推荐)_

## Cap.33 (FR Cap.XXXIII)

**章节数据**: 新词 476 / 新词密度 23.8% / 累计 8654 词形 (9818 词族)

### 💪 挑战读物 (1)
- `forum_lectiones` (Forum - Lectiones Latinitatis Vivae (Polis)): challenging, t70 Cap.33, pkH=75%, 教学 Cap.5(59%), 9,775独词

### 🧩 拉语段 (1)
- `latin_natural_method` p.70-72 (3页): 60%起点 Cap.33, 教学 Cap.1(12%), 303独词

## Cap.34 (FR Cap.XXXIV)

**章节数据**: 新词 520 / 新词密度 23.6% / 累计 9124 词形 (10338 词族)

### 📚 节选读物 (1)
- `cambridge_3` (Cambridge Latin Course 3): difficult, h50 Cap.34, pkH=55%, 教学 Cap.5(50%), 13,954独词

_(本章无D类拉语段推荐)_

## Cap.35 (FR Cap.XXXV)

**章节数据**: 新词 336 / 新词密度 20.9% / 累计 9417 词形 (10674 词族)

### 📖 可读读物 (1)
- `via_latina_romanorum` (Via Latina: De Lingua et Vita Romanorum): readable, t80 Cap.35, pkH=89%, 教学 Cap.1(63%), 6,267独词

### 🧩 拉语段 (1)
- `cambridge_2` p.77-79 (3页): 60%起点 Cap.35, 教学 Cap.4(8%), 179独词

## Cap.36 (RA Cap.XXXVI)

**章节数据**: 新词 1943 / 新词密度 48.8% / 累计 11360 词形 (12617 词族)

### 💪 挑战读物 (1)
- `latin_natural_method` (Latin by the Natural Method (W.G. Most 1957)): challenging, t70 Cap.36, pkH=75%, 教学 Cap.1(51%), 10,349独词

_(本章无D类拉语段推荐)_

## Cap.37 (RA Cap.XXXVII)

**章节数据**: 新词 1391 / 新词密度 45.3% / 累计 12751 词形 (14008 词族)

### 💪 挑战读物 (1)
- `hobbitus` (Hobbitus Ille (Tolkien 拉语版)): challenging, t70 Cap.37, pkH=74%, 教学 Cap.11(46%), 14,830独词

### 📚 节选读物 (2)
- `via_latina_easy` (Via Latina: Easy Latin Reader (Collar 1897)): difficult, h50 Cap.37, pkH=55%, 教学 Cap.1(51%), 15,737独词
- `illiterati_1` (Latin for the Illiterati (Stone)): difficult, h50 Cap.37, pkH=54%, 教学 Cap.1(48%), 14,464独词

_(本章无D类拉语段推荐)_

## Cap.38 (RA Cap.XXXVIII)

**章节数据**: 新词 811 / 新词密度 37.7% / 累计 13562 词形 (14819 词族)

### 🧩 拉语段 (1)
- `dooge_beginners_key` p.29-31 (3页): 60%起点 Cap.38, 教学 Cap.1(9%), 355独词

## Cap.39 (RA Cap.XXXIX)

**章节数据**: 新词 1241 / 新词密度 37.5% / 累计 14803 词形 (16060 词族)

### 💪 挑战读物 (1)
- `olimpia_nicholas` (The Mysterious Traveler (Olimpi)): challenging, t70 Cap.39, pkH=73%, 教学 Cap.3(19%), 1,273独词

_(本章无D类拉语段推荐)_

## Cap.40 (RA Cap.XL)

**章节数据**: 新词 1028 / 新词密度 32.9% / 累计 15831 词形 (17088 词族)

### 🧩 拉语段 (1)
- `dooge_beginners` p.214-219 (6页): 60%起点 Cap.40, 教学 Cap.1(16%), 622独词

## Cap.41 (RA Cap.XLI)

**章节数据**: 新词 842 / 新词密度 33.7% / 累计 16673 词形 (17930 词族)

### 📚 节选读物 (1)
- `ecce_romani_2b` (Ecce Romani IIB): difficult, h50 Cap.41, pkH=52%, 教学 Cap.5(50%), 14,948独词

### 🧩 拉语段 (1)
- `dooge_beginners_2` p.221-223 (3页): 60%起点 Cap.41, 教学 Cap.3(11%), 355独词

## Cap.42 (RA Cap.XLII)

**章节数据**: 新词 1258 / 新词密度 30.9% / 累计 17931 词形 (19188 词族)

### 📖 可读读物 (1)
- `pugio_bruti` (Pugio Bruti (Polis)): readable, t80 Cap.42, pkH=82%, 教学 Cap.4(26%), 1,656独词

### 🧩 拉语段 (2)
- `cambridge_2` p.2-6 (5页): 60%起点 Cap.42, 教学 Cap.4(6%), 121独词
- `dooge_beginners` p.221-223 (3页): 60%起点 Cap.42, 教学 Cap.6(10%), 362独词

## Cap.43 (RA Cap.XLIII)

**章节数据**: 新词 1055 / 新词密度 28.8% / 累计 18986 词形 (20243 词族)

### 💪 挑战读物 (1)
- `chickering` (First Latin Reader (Chickering)): challenging, t70 Cap.43, pkH=74%, 教学 Cap.1(65%), 15,124独词

### 📚 节选读物 (2)
- `cambridge_4` (Cambridge Latin Course 4): english_mixed, h50 Cap.43, pkH=52%, 教学 Cap.5(54%), 17,310独词
- `ecce_romani_3` (Ecce Romani III): difficult, h50 Cap.43, pkH=53%, 教学 Cap.1(50%), 14,197独词

### 🧩 拉语段 (1)
- `wileys_real_latin` p.366-368 (3页): 60%起点 Cap.43, 教学 Cap.5(6%), 242独词

## Cap.44 (RA Cap.XLIV)

**章节数据**: 新词 1419 / 新词密度 27.6% / 累计 20405 词形 (21662 词族)

### 🧩 拉语段 (1)
- `dooge_beginners_2` p.214-219 (6页): 60%起点 Cap.44, 教学 Cap.1(15%), 635独词

## Cap.45 (RA Cap.XLV)

**章节数据**: 新词 1222 / 新词密度 27.5% / 累计 21627 词形 (22884 词族)

_(本章无D类拉语段推荐)_

## Cap.46 (RA Cap.XLVI)

**章节数据**: 新词 1251 / 新词密度 25.6% / 累计 22878 词形 (24135 词族)

### 🧩 拉语段 (2)
- `latin_made_simple` p.83-85 (3页): 60%起点 Cap.46, 教学 Cap.1(10%), 309独词
- `oxford_2` p.149-151 (3页): 60%起点 Cap.46, 教学 Cap.4(10%), 551独词

## Cap.47 (RA Cap.XLVII)

**章节数据**: 新词 595 / 新词密度 26.5% / 累计 23473 词形 (24730 词族)

_(本章无D类拉语段推荐)_

## Cap.48 (RA Cap.XLVIII)

**章节数据**: 新词 2085 / 新词密度 24.9% / 累计 25558 词形 (26815 词族)

_(本章无D类拉语段推荐)_

## Cap.49 (RA Cap.XLIX)

**章节数据**: 新词 670 / 新词密度 23.5% / 累计 26228 词形 (27485 词族)

_(本章无D类拉语段推荐)_

## Cap.50 (RA Cap.L)

**章节数据**: 新词 1523 / 新词密度 22.6% / 累计 27751 词形 (29008 词族)

### 🧩 拉语段 (3)
- `oxford_2` p.72-75 (4页): 60%起点 Cap.50, 教学 Cap.1(8%), 404独词
- `dooge_beginners` p.226-228 (3页): 60%起点 Cap.50, 教学 Cap.1(8%), 362独词
- `latin_natural_method` p.147-149 (3页): 60%起点 Cap.50, 教学 Cap.4(12%), 395独词

## Cap.51 (RA Cap.LI)

**章节数据**: 新词 812 / 新词密度 23.1% / 累计 28563 词形 (29820 词族)

_(本章无D类拉语段推荐)_

## Cap.52 (RA Cap.LII)

**章节数据**: 新词 1458 / 新词密度 20.2% / 累计 30021 词形 (31278 词族)

### 📚 节选读物 (1)
- `ora_maritima` (Ora Maritima (Sonnenschein 1900)): english_mixed, h50 Cap.52, pkH=50%, 教学 Cap.1(42%), 7,496独词

### 🧩 拉语段 (1)
- `ecce_romani` p.205-207 (3页): 60%起点 Cap.52, 教学 Cap.4(7%), 256独词

## Cap.53 (RA Cap.LIII)

**章节数据**: 新词 832 / 新词密度 20.2% / 累计 30853 词形 (32110 词族)

_(本章无D类拉语段推荐)_

## Cap.54 (RA Cap.LIV)

**章节数据**: 新词 1170 / 新词密度 18.8% / 累计 32023 词形 (33280 词族)

_(本章无D类拉语段推荐)_

## Cap.55 (RA Cap.LV)

**章节数据**: 新词 969 / 新词密度 20.3% / 累计 32992 词形 (34249 词族)

### 🧩 拉语段 (1)
- `cambridge_2` p.82-84 (3页): 60%起点 Cap.55, 教学 Cap.10(6%), 233独词

## Cap.56 (RA Cap.LVI)

**章节数据**: 新词 778 / 新词密度 22.2% / 累计 33770 词形 (35027 词族)

### 📚 节选读物 (1)
- `gwynne` (Gwynne's Latin): english_mixed, h50 Cap.56, pkH=50%, 教学 Cap.1(34%), 7,556独词

_(本章无D类拉语段推荐)_

