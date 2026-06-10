#!/usr/bin/env python3
"""
organize_readers.py — 按推荐层级整理 source/Other_Readers/ 下的所有读物

策略: 使用符号链接（避免重复占用磁盘）将原文件软链到
       source/Other_Readers/curated/ 下的分级目录中。

层级:
  A1_入门_强烈推荐/   FR Cap. 1-15 区间
  A2_初级_推荐/       FR Cap. 15-25 区间
  B1_中级_可考虑/     FR Cap. 25-35 / RA 36-42 区间
  B2_中高级_谨慎/     RA 43-50 区间
  C_高级_不推荐/      RA 50+ / 古典原典
  D_教材_不推荐入库/  教材/语法书/参考
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "source" / "Other_Readers"
CURATED = SRC_DIR / "curated"

# 完整清单: (slug, 原文件相对路径, 推荐层级, 难度评级, 建议理由)
# 难度评级: 1=入门, 2=初级, 3=中级, 4=中高级, 5=高级
ENTRIES = [
    # ============== A1: 入门 (FR Cap. 1-15) ==============
    ("pugio_bruti", "习得法读物/Pugio Bruti .pdf", "A1_入门_强烈推荐", 1,
     "Polis 习得法入门故事, 27 章, 自然语境故事流, 适合 FR Cap. 1-15 区间"),
    ("forum_lectiones", "习得法读物/Forum_ Lectiones Latinitatis Vivae_ Speaking Latin as a Living Language.pdf", "A1_入门_强烈推荐", 1,
     "Polis 习得法 Vol.1, 对话+故事, TPR 教学法, 适合 Cap. 1-15"),
    ("diocles_flora", "Dioclēs et Flōra Full Text and Glossary.pdf", "A1_入门_强烈推荐", 1,
     "习得法故事, 18 章, 罗马日常生活, 适合 Cap. 1-20"),
    ("regulus", "习得法读物/Regulus.pdf", "A1_入门_强烈推荐", 1,
     "Antonio de Saint-Exupéry 小王子拉语版 'Regulus', 习得法, 适合 Cap. 5-20"),
    ("fabulae_faciles", "其他读物/Fabulae faciles  a first Latin reader  containi... (z-lib.org).pdfFabulae faciles  a first Latin reader  containi... (z-lib.org).pdf", "A1_入门_强烈推荐", 1,
     "Ritchie 经典入门故事集, 1889 年, 适合 Cap. 1-20, 质量极高"),
    ("ora_maritima", "其他读物/无长音/Ora Maritima A Latin Story For Beginners  With... (z-lib.org).pdfOra Maritima A Latin Story For Beginners  With... (z-lib.org).pdf", "A1_入门_强烈推荐", 1,
     "Sonnenschein 入门故事, 1890s 经典, 适合 Cap. 1-20"),
    ("pro_patria", "其他读物/Pro patria a Latin story for beginners  being a... (z-lib.org).pdfPro patria a Latin story for beginners  being a... (z-lib.org).pdf", "A1_入门_强烈推荐", 1,
     "Ora Maritima 续作, Sonnenschein 入门故事, 适合 Cap. 1-20"),
    ("septimus", "其他读物/Septimus A First Latin Reader (Richard Lionel.pdf", "A1_入门_强烈推荐", 1,
     "Chambers 入门故事, 经典, 适合 Cap. 1-15"),
    ("nutting_reader", "其他读物/A first Latin reader (Nutting  Herbert C.pdf.pdf", "A1_入门_强烈推荐", 1,
     "Nutting 入门读物, 配合 Primer 入门, 目标 Caesar 前, 适合 Cap. 1-20"),
    ("unus_duo_tres", "习得法读物/Unus  Duo  Tres Latine loquamur per scaenas.pdf.pdf", "A1_入门_强烈推荐", 1,
     "Polis 习得法 Vol.1 (对话+图), 适合 Cap. 1-10"),

    # ============== A2: 初级 (FR Cap. 15-25) ==============
    ("olimpia_daedalus", "习得法读物/已读/Andrew Olimpi 分级读物（一部分/Daedalus et Icarus .pdf", "A2_初级_推荐", 2,
     "Olimpi 分层读物, 难度递进从改编到 Ovid/Hyginus 原文, 适合 Cap. 15-25"),
    ("olimpia_pyramus", "习得法读物/已读/Andrew Olimpi 分级读物（一部分/Reckless Love_ The Story of Pyramus and Thisbe _ .pdf", "A2_初级_推荐", 2,
     "Olimpi 分层读物, 适合 Cap. 15-25"),
    ("olimpia_nicholas", "习得法读物/已读/Andrew Olimpi 分级读物（一部分/The Mysterious Traveler_ A Medieval Play about Saint Nicholas  .pdf", "A2_初级_推荐", 2,
     "Olimpi 分层读物, 中世纪题材, 适合 Cap. 15-25"),
    ("via_latina_romanorum", "习得法读物/Via latina de lingua et vita romanorum.pdf", "A2_初级_推荐", 2,
     "Cultura Clásica 出品, 习得法罗马生活读本, 适合 Cap. 10-25"),
    ("chickering", "其他读物/First Latin reader (Chickering  Edward C. (Edwa... (z-lib.org).pdfFirst Latin reader (Chickering  Edward C. (Edwa... (z-lib.org).pdf", "A2_初级_推荐", 2,
     "Chickering 经典初级读物, 适合 Cap. 15-25"),
    ("latin_lower_forms", "其他读物/无长音/A Latin reader for the lower forms in schools (... (z-lib.org).pdfA Latin reader for the lower forms in schools (... (z-lib.org).pdf", "A2_初级_推荐", 2,
     "Hardy 1889 经典初级故事, 适合 Cap. 15-25"),

    # ============== B1: 中级 (FR Cap. 25-35 / RA 36-42) ==============
    ("reynolds_reader", "其他读物/Latin reader (Alphaeus Bruce Reynolds) (z-lib.org).pdfLatin reader (Alphaeus Bruce Reynolds) (z-lib.org).pdf", "B1_中级_可考虑", 3,
     "Reynolds 经典中级读物, 适合 Cap. 25-35 区间"),
    ("intermediate_oral_cicero", "其他读物/Intermediate Oral Latin Reader Based On Ciceros... (z-lib.org).pdfIntermediate Oral Latin Reader Based On Ciceros... (z-lib.org).pdf", "B1_中级_可考虑", 3,
     "基于 Cicero De Senectute 改写, 中级, 适合 Cap. 25-35"),
    ("via_latina_easy", "其他读物/Via latina An Easy Latin Reader.pdf", "B1_中级_可考虑", 3,
     "罗马古迹介绍, 'Easy Latin Reader' 实际中级, 适合 Cap. 25-35"),
    ("conversational_latin", "Conversational Latin for Oral Proficiency.pdf", "B1_中级_可考虑", 3,
     "短语书+对话, 4th ed. 2007 Bolchazy, 适合作为口语补充 Cap. 20+"),
    ("nunc_loquamur", "其他读物/Nunc Loquamur_ Guided Conversations for Latin (Latin Edition)_Thomas McCarthy_21809997_zhelper-search.pdf", "B1_中级_可考虑", 3,
     "Hackett 出品引导式对话, 适合所有级别, 作为 Cap. 15+ 口语补充"),

    # ============== B2: 中高级 (RA 43-50) ==============
    ("hobbitus", "其他读物/无长音/Hobbitus Ille The Latin Hobbit - J. R. R. Tolkien.pdf", "B2_中高级_谨慎", 4,
     "Tolkien 霍比特人拉语版, 现代小说风格, 适合 RA 阶段后期"),
    ("second_year_latin", "Second Year Latin – Part 1 – Selections of Easy Latin, J. B. Greenough.pdf", "B2_中高级_谨慎", 4,
     "Greenough 1899 二年级教材, 90 页简易拉语 + Caesar 选段, 适合 RA 阶段"),

    # ============== C: 高级 (古典原典) ==============
    ("caesar_interlinear", "Caesar_Interlinear.pdf", "C_高级_不推荐", 5,
     "Caesar 高卢战记逐字对照, 古典原典, 不适合 FR 学习者"),
    ("caesar_mondon", "Caesar’s Dē Bellō Gallicō_ A Syntactically Parsed Reader_Jean-François R. Mondon.pdf", "C_高级_不推荐", 5,
     "Caesar 句法分析版, 古典原典, 难度极高"),
    ("cicero_dyck", "Cicero Catilinarians_Dyck, Andrew R._3629087.pdf", "C_高级_不推荐", 5,
     "Cicero Catilinarians 学术版, 古典原典, 不适合"),
    ("o_tempora", "O Tempora! O Mores!_ Cicero's Catilinarian Orations, A Student Edition with Historical Essays_Susan O. Shapiro, Cicero_5697385_zhelper-search.pdf", "C_高级_不推荐", 5,
     "Cicero Catilinarians 学生版, 古典原典, 不适合"),
    ("select_orations_interlinear", "Select Orations of Cicero – Interlinear, Thomas Clark.pdf", "C_高级_不推荐", 5,
     "Cicero 演讲集逐字版, 古典原典, 不适合"),
    ("catiline_literal", "Catiline Orations of Cicero – Literal Translation, Rev. Dr. Giles.pdf", "C_高级_不推荐", 5,
     "Cicero 原典字面翻译, 不适合"),
    ("phormio_terence", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/The Phormio of Terence in Latin, Fairclough and Richardson.pdf", "C_高级_不推荐", 5,
     "Terence 罗马喜剧原典, 古典作家, 不适合"),
    ("civwar_caesar", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Caesar's Civil War in Latin, Charles E. Moberly.pdf", "C_高级_不推荐", 5,
     "Caesar 内战记原典, 不适合"),
    ("gallic_war_literal", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Caesar's Gallic War Commentaries – Literal Translation, Rev. Dr. Giles.pdf", "C_高级_不推荐", 5,
     "Caesar 高卢战记原典, 不适合"),
    ("cicero_select_d_ooge", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Cicero Select Orations, Benjamin L. D'Ooge.pdf", "C_高级_不推荐", 5,
     "Cicero 演讲选, 原典, 不适合"),
    ("extracts_cicero", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Extracts From Cicero – Sections I & II in Latin, Henry Walford.pdf", "C_高级_不推荐", 5,
     "Cicero 选段, 原典, 不适合"),
    ("livy_xxi", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Livy Book XXI in Latin, W. W. Capes.pdf", "C_高级_不推荐", 5,
     "Livy 罗马史原典, 不适合"),
    ("livy_i_ii", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Livy Books I & II in Latin, J. B. Greenough.pdf", "C_高级_不推荐", 5,
     "Livy 罗马史原典, 不适合"),
    ("ovid_selections", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Selections From Ovid, Allen & Greenough.pdf", "C_高级_不推荐", 5,
     "Ovid 变形记选段, 古典诗歌, 不适合"),
    ("ovid_metamorphoses_literal", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Ovid's Metamorphoses – Literal Translation, Rev. Dr. Giles.pdf", "C_高级_不推荐", 5,
     "Ovid 变形记原典, 不适合"),
    ("apuleius_cupid", "其他读物/无长音/Apuleius Cupid and Psyche An Intermediate Latin... (z-lib.org).pdfApuleius Cupid and Psyche An Intermediate Latin... (z-lib.org).pdf", "C_高级_不推荐", 5,
     "Apuleius 丘比特与普赛克, 古典小说, 不适合"),
    ("delphi_caesar", "其他读物/无长音/Delphi Complete Works of Julius Caesar (Illustrated) (Delphi Ancient Classics Book 7) ( PDFDrive ).epub", "C_高级_不推荐", 5,
     "Caesar 全集 (Delphi 版), 学术合集, 不适合"),
    ("latin_erotic_elegy", "其他读物/无长音/Latin Erotic Elegy An Anthology and Reader (Pau... (z-lib.org).pdfLatin Erotic Elegy An Anthology and Reader (Pau... (z-lib.org).pdf", "C_高级_不推荐", 5,
     "拉丁爱情挽歌选, 古典诗歌, 难度极高, 不适合"),
    ("ovids_metamorphoses_reader", "其他读物/Ovids Metamorphoses A Reader for Students.pdf", "C_高级_不推荐", 5,
     "Ovid 变形记学生版, 古典诗歌, 不适合"),
    ("beginner_poetry_reader", "其他读物/Beginning Latin Poetry Reader 70 Passages from... (z-lib.org).pdfBeginning Latin Poetry Reader 70 Passages from... (z-lib.org).pdf", "C_高级_不推荐", 5,
     "拉丁诗歌入门, 70 段选, 适合 RA 阶段后期, 标注为 C 而非 A"),
    ("millennium", "其他读物/无长音/Millennium_ A Latin Reader (A.D. 374-1374) ( PDFDrive ).pdf", "C_高级_不推荐", 5,
     "中世纪拉丁读本 (AD 374-1374), 远超出 FR 范围, 极难"),
    ("orbis_terrarum", "其他读物/无长音/Orbis terrarum A Senior Latin Reader (Edgar Hen... (z-lib.org).pdfOrbis terrarum A Senior Latin Reader (Edgar Hen... (z-lib.org).pdf", "C_高级_不推荐", 5,
     "Senior Latin Reader, 高年级, 远超 FR 适合范围"),
    ("how_to_read_poem", "其他读物/无长音/How to Read a Latin Poem_ If You Can't Read Latin Yet ( PDFDrive ).pdf", "C_高级_不推荐", 5,
     "拉丁诗歌导读, 学术工具, 难度高, 不直接适合"),
    ("our_mythical_childhood", "其他读物/无长音/Our Mythical Childhood... The Classics and Lite... (z-lib.org).pdfOur Mythical Childhood... The Classics and Lite... (z-lib.org).pdf", "C_高级_不推荐", 5,
     "学术论文集, 古典神话与文学, 不适合"),
    ("learning_ancient_way", "其他读物/无长音/Learning Latin the Ancient Way_ Latin Textbooks from the Ancient World ( PDFDrive ).pdf", "C_高级_不推荐", 5,
     "古代拉丁语教材史, 学术, 不适合"),
    ("latin_prose_comp_cicero", "其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Latin Prose Composition Based on Cicero, Henry Carr Pearson.pdf", "C_高级_不推荐", 5,
     "Cicero 风格的拉语写作教材, 高难, 不适合"),

    # ============== D: 教材/语法书/参考 ==============
    ("wheelock_7e", "Wheelocks Latin, 7e.pdf", "D_教材_不推荐入库", 0,
     "Wheelock 教材 7e, 语法教材, 体系与 LLPSI 完全不同, 仅作参考"),
    ("wheelock_reader", "韦洛克文选Wheelock's Latin Reader. Selections from Latin Literature.pdf", "D_教材_不推荐入库", 0,
     "Wheelock Reader 古典文学选集, 配合 Wheelock 教材, 难度高"),
    ("wheelock_answer_key", "Wheelocks Latin, 7e, Answer Key.pdf", "D_教材_不推荐入库", 0,
     "Wheelock 7e 答案, 不入库"),
    ("reading_latin_text", "其他读物/Reading Latin 2e/Reading Latin Text and Vocabulary (2nd Edition) (Peter Jones) .pdf", "D_教材_不推荐入库", 0,
     "Reading Latin 2e 课文+词汇, 体系教材, 不入库"),
    ("reading_latin_grammar", "其他读物/Reading Latin 2e/Reading Latin Grammar and Exercises (2nd Edition) (Peter Jones) .pdf", "D_教材_不推荐入库", 0,
     "Reading Latin 2e 语法+练习, 教材配套, 不入库"),
    ("reading_latin_study_guide", "其他读物/Reading Latin 2e/Reading Latin An Independent Study Guide to Reading Latin (Peter V. Jones, Keith C. Sidwell) .pdf", "D_教材_不推荐入库", 0,
     "Reading Latin 2e 自学指南, 教材配套, 不入库"),
    ("dooge_beginners", "其他读物/Latin for beginners/Latin For Beginners, Benjamin L. D'Ooge.pdf", "D_教材_不推荐入库", 0,
     "D'Ooge 1909 入门教材, 语法路线, 不入库"),
    ("dooge_beginners_2", "其他读物/Latin for beginners/Latin For Beginners, Benjamin L. D'Ooge 2.pdf", "D_教材_不推荐入库", 0,
     "D'Ooge 入门教材 (另一版), 不入库"),
    ("dooge_beginners_key", "其他读物/Latin for beginners/Latin for Beginner's Key, Benjamin L. D'Ooge.pdf", "D_教材_不推荐入库", 0,
     "D'Ooge 入门教材答案, 不入库"),
    ("latin_made_simple", "其他读物/无长音/Latin Made Simple_ A complete introductory course with practice readings and exercises, plus a handy Latin English vocabulary ( PDFDrive ).pdf", "D_教材_不推荐入库", 0,
     "Latin Made Simple 入门教材, 不入库"),
    ("teach_yourself", "其他读物/无长音/Teach Yourself Beginner's Latin ( PDFDrive ).pdf", "D_教材_不推荐入库", 0,
     "Teach Yourself 入门教材, 不入库"),
    ("beginners_latin_book", "其他读物/BEGINNER’S LATIN BOOK - Textkit _ Greek and Latin  ( PDFDrive ).pdf", "D_教材_不推荐入库", 0,
     "Beginner's Latin Book Textkit 版, 不入库"),
    ("latin_natural_method", "Latin by the Natural Method First Year (William George Most) .pdf", "D_教材_不推荐入库", 0,
     "Most 自然教学法第一年, 教材, 不入库"),
    ("latin_first_year_magoffin", "Latin-first year (The climax series) (Ralph Van Deman Magoffin) (z-lib.org).pdf", "D_教材_不推荐入库", 0,
     "Magoffin 第一年教材, 不入库"),
    ("gwynne", "其他读物/无长音/Gwynne's Latin_ The Ultimate Introduction to Latin Including the Latin in Everyday English ( PDFDrive ).epub", "D_教材_不推荐入库", 0,
     "Gwynne 入门语法教材, 不入库"),
    ("wileys_real_latin", "Wileys real Latin learning Latin from the source (Maltby, RobertBelcher, Kenneth) (z-lib.org).epub", "D_教材_不推荐入库", 0,
     "Wiley's Real Latin 教材, 语法+原文, 不入库"),
    ("illiterati_1", "Latin For The Illiterati A Modern Guide To An Ancient Language (Jon R. Stone) (z-.pdf", "D_教材_不推荐入库", 0,
     "Latin for the Illiterati, 医疗法律宗教短语, 参考工具, 不入库"),
    ("illiterati_2", "More Latin for the Illiterati A Guide to Everyday Medical, Legal and Religious La.pdf", "D_教材_不推荐入库", 0,
     "More Latin for the Illiterati, 医疗法律宗教短语, 不入库"),
    ("cambridge_1", "Cambridge latin/剑桥拉丁语北美版第一册[Cambridge_Latin_Course 1, 5e 2.pdf", "D_教材_不推荐入库", 0,
     "Cambridge Latin Course Book 1, 体系与 LLPSI 完全不同, 仅参考"),
    ("cambridge_2", "Cambridge latin/剑桥拉丁语北美版第二册[Cambridge_Latin_Course 3.pdf", "D_教材_不推荐入库", 0,
     "Cambridge Latin Course Book 2, 不入库"),
    ("cambridge_3", "Cambridge latin/剑桥拉丁语北美版第三册[Cambridge_Latin_Course 4.pdf", "D_教材_不推荐入库", 0,
     "Cambridge Latin Course Book 3, 不入库"),
    ("cambridge_4", "Cambridge latin/剑桥拉丁语北美版第四册[Cambridge_Latin_Course 4.pdf", "D_教材_不推荐入库", 0,
     "Cambridge Latin Course Book 4, 不入库"),
    ("oxford_1", "Oxford Latin Course,  2e /Oxford Latin Course, Part 1, 2e  .pdf", "D_教材_不推荐入库", 0,
     "Oxford Latin Course 1, 不入库"),
    ("oxford_2", "Oxford Latin Course,  2e /Oxford Latin Course, Part 2, 2e.pdf", "D_教材_不推荐入库", 0,
     "Oxford Latin Course 2, 不入库"),
    ("oxford_3", "Oxford Latin Course,  2e /Oxford Latin Course, Part 3, 2e.pdf", "D_教材_不推荐入库", 0,
     "Oxford Latin Course 3, 不入库"),
    ("ecce_romani", "Ecce Romani I .pdf", "D_教材_不推荐入库", 0,
     "Ecce Romani I, 体系教材, 不入库"),
    ("revised_latin_primer", "The Revised Latin Primer (Benjamin Hall Kennedy) (z-lib.org).pdf", "D_教材_不推荐入库", 0,
     "Kennedy 修订拉丁语语法书, 经典语法书, 不入库"),
    ("new_latin_primer", "a new latin primer.pdf", "D_教材_不推荐入库", 0,
     "New Latin Primer 语法书, 不入库"),
    ("latin_stories_wheelock", "Latin_Stories_De.pdf", "D_教材_不推荐入库", 0,
     "38 Latin Stories 配合 Wheelock 6e, 教材配套, 不入库"),
]


def main() -> int:
    if CURATED.exists():
        print(f"[信息] 删除已存在的 {CURATED}")
        shutil.rmtree(CURATED)
    CURATED.mkdir(parents=True)

    # 创建分级目录
    tiers = sorted(set(e[2] for e in ENTRIES))
    for tier in tiers:
        (CURATED / tier).mkdir(parents=True, exist_ok=True)

    created = 0
    missing = []
    for slug, rel, tier, level, reason in ENTRIES:
        src = SRC_DIR / rel
        if not src.exists():
            missing.append((slug, rel))
            print(f"  [MISS] {slug}: {rel}")
            continue
        # 目标: 短横线连接的命名 (避免特殊字符)
        ext = src.suffix
        dst = CURATED / tier / f"{slug}{ext}"
        # 用符号链接
        os.symlink(str(src.resolve()), str(dst))
        created += 1
        print(f"  [OK]   [{tier}] {slug}{ext}")

    print(f"\n[汇总] 创建符号链接 {created}/{len(ENTRIES)}")
    if missing:
        print(f"[警告] 缺失文件 {len(missing)} 个:")
        for s, r in missing:
            print(f"   - {s}: {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
