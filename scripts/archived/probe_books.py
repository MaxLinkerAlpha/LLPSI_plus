#!/usr/bin/env python3
"""
快速 OCR 探测: 对 source/Other_Readers/ 下指定 PDF/EPUB 抽取前 N 页文本,
输出到 ocr_output/_probe/<slug>/page_NNN.txt 便于快速识别书的内容和难度。
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBE_DIR = ROOT / "ocr_output" / "_probe"
PROBE_DIR.mkdir(parents=True, exist_ok=True)

# (slug, pdf_path) 列表 - 仅探测模糊/关键的
PROBE_TARGETS = [
    # ----- 不确定/模糊 -----
    ("latin_stories_de", "source/Other_Readers/Latin_Stories_De.pdf"),
    ("reynolds_reader", "source/Other_Readers/其他读物/Latin reader (Alphaeus Bruce Reynolds) (z-lib.org).pdfLatin reader (Alphaeus Bruce Reynolds) (z-lib.org).pdf"),
    ("intermediate_oral_cicero", "source/Other_Readers/其他读物/Intermediate Oral Latin Reader Based On Ciceros... (z-lib.org).pdfIntermediate Oral Latin Reader Based On Ciceros... (z-lib.org).pdf"),
    ("second_year_latin", "source/Other_Readers/Second Year Latin – Part 1 – Selections of Easy Latin, J. B. Greenough.pdf"),
    ("illiterati_1", "source/Other_Readers/Latin For The Illiterati A Modern Guide To An Ancient Language (Jon R. Stone) (z-.pdf"),
    ("illiterati_2", "source/Other_Readers/More Latin for the Illiterati A Guide to Everyday Medical, Legal and Religious La.pdf"),
    ("fabulae_faciles", "source/Other_Readers/其他读物/Fabulae faciles  a first Latin reader  containi... (z-lib.org).pdfFabulae faciles  a first Latin reader  containi... (z-lib.org).pdf"),
    ("pro_patria", "source/Other_Readers/其他读物/Pro patria a Latin story for beginners  being a... (z-lib.org).pdfPro patria a Latin story for beginners  being a... (z-lib.org).pdf"),
    ("ora_maritima", "source/Other_Readers/其他读物/无长音/Ora Maritima A Latin Story For Beginners  With... (z-lib.org).pdfOra Maritima A Latin Story For Beginners  With... (z-lib.org).pdf"),
    ("septimus", "source/Other_Readers/其他读物/Septimus A First Latin Reader (Richard Lionel.pdf"),
    ("nutting_reader", "source/Other_Readers/其他读物/A first Latin reader (Nutting  Herbert C.pdf.pdf"),
    ("chickering", "source/Other_Readers/其他读物/First Latin reader (Chickering  Edward C. (Edwa... (z-lib.org).pdfFirst Latin reader (Chickering  Edward C. (Edwa... (z-lib.org).pdf"),
    ("forum_lectiones", "source/Other_Readers/习得法读物/Forum_ Lectiones Latinitatis Vivae_ Speaking Latin as a Living Language.pdf"),
    ("nunc_loquamur", "source/Other_Readers/其他读物/Nunc Loquamur_ Guided Conversations for Latin (Latin Edition)_Thomas McCarthy_21809997_zhelper-search.pdf"),
    ("conversational_latin", "source/Other_Readers/Conversational Latin for Oral Proficiency.pdf"),
    ("pugio_bruti", "source/Other_Readers/习得法读物/Pugio Bruti .pdf"),
    ("diocles_flora", "source/Other_Readers/Dioclēs et Flōra Full Text and Glossary.pdf"),
    ("regulus", "source/Other_Readers/习得法读物/Regulus.pdf"),
    ("via_latina_romanorum", "source/Other_Readers/习得法读物/Via latina de lingua et vita romanorum.pdf"),
    ("olimpia_daedalus", "source/Other_Readers/习得法读物/已读/Andrew Olimpi 分级读物（一部分/Daedalus et Icarus .pdf"),
    ("olimpia_pyramus", "source/Other_Readers/习得法读物/已读/Andrew Olimpi 分级读物（一部分/Reckless Love_ The Story of Pyramus and Thisbe _ .pdf"),
    ("olimpia_nicholas", "source/Other_Readers/习得法读物/已读/Andrew Olimpi 分级读物（一部分/The Mysterious Traveler_ A Medieval Play about Saint Nicholas  .pdf"),
    ("unus_duo_tres", "source/Other_Readers/习得法读物/Unus  Duo  Tres Latine loquamur per scaenas.pdf.pdf"),
    # ----- 系统教材 (用于参照对比, 不入库) -----
    ("cambridge_1", "source/Other_Readers/Cambridge latin/剑桥拉丁语北美版第一册[Cambridge_Latin_Course 1, 5e 2.pdf"),
    ("oxford_1", "source/Other_Readers/Oxford Latin Course,  2e /Oxford Latin Course, Part 1, 2e  .pdf"),
    ("ecce_romani", "source/Other_Readers/Ecce Romani I .pdf"),
    # ----- 古典原典 (确认是原典) -----
    ("caesar_interlinear", "source/Other_Readers/Caesar_Interlinear.pdf"),
    ("caesar_mondon", "source/Other_Readers/Caesar’s Dē Bellō Gallicō_ A Syntactically Parsed Reader_Jean-François R. Mondon.pdf"),
    ("cicero_dyck", "source/Other_Readers/Cicero Catilinarians_Dyck, Andrew R._3629087.pdf"),
    ("o_tempora", "source/Other_Readers/O Tempora! O Mores!_ Cicero's Catilinarian Orations, A Student Edition with Historical Essays_Susan O. Shapiro, Cicero_5697385_zhelper-search.pdf"),
    ("select_orations_interlinear", "source/Other_Readers/Select Orations of Cicero – Interlinear, Thomas Clark.pdf"),
    ("catiline_literal", "source/Other_Readers/Catiline Orations of Cicero – Literal Translation, Rev. Dr. Giles.pdf"),
    # ----- 教材配套 -----
    ("wheelock_7e", "source/Other_Readers/Wheelocks Latin, 7e.pdf"),
    ("wheelock_reader", "source/Other_Readers/韦洛克文选Wheelock's Latin Reader. Selections from Latin Literature.pdf"),
    ("reading_latin_text", "source/Other_Readers/其他读物/Reading Latin 2e/Reading Latin Text and Vocabulary (2nd Edition) (Peter Jones) .pdf"),
    ("dooge_beginners", "source/Other_Readers/其他读物/Latin for beginners/Latin For Beginners, Benjamin L. D'Ooge.pdf"),
    ("latin_made_simple", "source/Other_Readers/其他读物/无长音/Latin Made Simple_ A complete introductory course with practice readings and exercises, plus a handy Latin English vocabulary ( PDFDrive ).pdf"),
    ("teach_yourself", "source/Other_Readers/其他读物/无长音/Teach Yourself Beginner's Latin ( PDFDrive ).pdf"),
    ("beginners_latin_book", "source/Other_Readers/其他读物/BEGINNER’S LATIN BOOK - Textkit _ Greek and Latin  ( PDFDrive ).pdf"),
    ("latin_natural_method", "source/Other_Readers/Latin by the Natural Method First Year (William George Most) .pdf"),
    ("latin_first_year_magoffin", "source/Other_Readers/Latin-first year (The climax series) (Ralph Van Deman Magoffin) (z-lib.org).pdf"),
    # ----- 诗歌/特殊 -----
    ("beginner_poetry_reader", "source/Other_Readers/其他读物/Beginning Latin Poetry Reader 70 Passages from... (z-lib.org).pdfBeginning Latin Poetry Reader 70 Passages from... (z-lib.org).pdf"),
    ("how_to_read_poem", "source/Other_Readers/其他读物/无长音/How to Read a Latin Poem_ If You Can't Read Latin Yet ( PDFDrive ).pdf"),
    ("latin_erotic_elegy", "source/Other_Readers/其他读物/无长音/Latin Erotic Elegy An Anthology and Reader (Pau... (z-lib.org).pdfLatin Erotic Elegy An Anthology and Reader (Pau... (z-lib.org).pdf"),
    ("hobbitus", "source/Other_Readers/其他读物/无长音/Hobbitus Ille The Latin Hobbit - J. R. R. Tolkien.pdf"),
    # ----- 高级/学术 -----
    ("millennium", "source/Other_Readers/其他读物/无长音/Millennium_ A Latin Reader (A.D. 374-1374) ( PDFDrive ).pdf"),
    ("orbis_terrarum", "source/Other_Readers/其他读物/无长音/Orbis terrarum A Senior Latin Reader (Edgar Hen... (z-lib.org).pdfOrbis terrarum A Senior Latin Reader (Edgar Hen... (z-lib.org).pdf"),
    ("latin_lower_forms", "source/Other_Readers/其他读物/无长音/A Latin reader for the lower forms in schools (... (z-lib.org).pdfA Latin reader for the lower forms in schools (... (z-lib.org).pdf"),
    ("gwynne", "source/Other_Readers/其他读物/无长音/Gwynne's Latin_ The Ultimate Introduction to Latin Including the Latin in Everyday English ( PDFDrive ).epub"),
    ("via_latina_easy", "source/Other_Readers/其他读物/Via latina An Easy Latin Reader.pdf"),
    ("wileys_real_latin", "source/Other_Readers/Wileys real Latin learning Latin from the source (Maltby, RobertBelcher, Kenneth) (z-lib.org).epub"),
    # ----- 其它 -----
    ("ovids_metamorphoses_reader", "source/Other_Readers/其他读物/Ovids Metamorphoses A Reader for Students.pdf"),
    ("learning_ancient_way", "source/Other_Readers/其他读物/无长音/Learning Latin the Ancient Way_ Latin Textbooks from the Ancient World ( PDFDrive ).pdf"),
    ("our_mythical_childhood", "source/Other_Readers/其他读物/无长音/Our Mythical Childhood... The Classics and Lite... (z-lib.org).pdfOur Mythical Childhood... The Classics and Lite... (z-lib.org).pdf"),
    ("phormio_terence", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/The Phormio of Terence in Latin, Fairclough and Richardson.pdf"),
    ("civwar_caesar", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Caesar's Civil War in Latin, Charles E. Moberly.pdf"),
    ("cicero_select_d_ooge", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Cicero Select Orations, Benjamin L. D'Ooge.pdf"),
    ("extracts_cicero", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Extracts From Cicero – Sections I & II in Latin, Henry Walford.pdf"),
    ("livy_xxi", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Livy Book XXI in Latin, W. W. Capes.pdf"),
    ("livy_i_ii", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Livy Books I & II in Latin, J. B. Greenough.pdf"),
    ("ovid_selections", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Selections From Ovid, Allen & Greenough.pdf"),
    ("gallic_war_literal", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Caesar's Gallic War Commentaries – Literal Translation, Rev. Dr. Giles.pdf"),
    ("apuleius_cupid", "source/Other_Readers/其他读物/无长音/Apuleius Cupid and Psyche An Intermediate Latin... (z-lib.org).pdfApuleius Cupid and Psyche An Intermediate Latin... (z-lib.org).pdf"),
    ("delphi_caesar", "source/Other_Readers/其他读物/无长音/Delphi Complete Works of Julius Caesar (Illustrated) (Delphi Ancient Classics Book 7) ( PDFDrive ).epub"),
    ("ovid_metamorphoses_literal", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Ovid's Metamorphoses – Literal Translation, Rev. Dr. Giles.pdf"),
    ("latin_prose_comp_cicero", "source/Other_Readers/其他读物/Textkit网希腊语拉丁语/Textkit希腊语拉丁语  2 of 4 -Latin-拉丁语（21）/Textkit-Library-Latin Books-Latin Reading Text（12）/Latin Prose Composition Based on Cicero, Henry Carr Pearson.pdf"),
    # ----- 完整三册 -----
    ("cambridge_2", "source/Other_Readers/Cambridge latin/剑桥拉丁语北美版第二册[Cambridge_Latin_Course 3.pdf"),
    ("cambridge_3", "source/Other_Readers/Cambridge latin/剑桥拉丁语北美版第三册[Cambridge_Latin_Course 4.pdf"),
    ("cambridge_4", "source/Other_Readers/Cambridge latin/剑桥拉丁语北美版第四册[Cambridge_Latin_Course 4.pdf"),
    ("oxford_2", "source/Other_Readers/Oxford Latin Course,  2e /Oxford Latin Course, Part 2, 2e.pdf"),
    ("oxford_3", "source/Other_Readers/Oxford Latin Course,  2e /Oxford Latin Course, Part 3, 2e.pdf"),
]

def probe_one(slug: str, pdf_rel: str, pages: int = 3) -> bool:
    """OCR PDF 的前 N 页 (跳过封面, 从 page 1 开始)."""
    pdf_path = ROOT / pdf_rel
    if not pdf_path.exists():
        print(f"  [SKIP] {slug}: 找不到 {pdf_rel}")
        return False

    out_dir = PROBE_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    if (out_dir / f"page_{pages:03d}.txt").exists():
        print(f"  [CACHED] {slug}")
        return True

    cmd = [
        "python3", str(ROOT / "scripts" / "ocr_book.py"),
        "--pdf", str(pdf_path),
        "--slug", f"_probe/{slug}",
        "--start", "1", "--end", str(1 + pages),
        "--dpi", "200",
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            print(f"  [OK] {slug}")
            return True
        else:
            print(f"  [ERR] {slug}: {r.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  [EXC] {slug}: {e}")
        return False


def main() -> int:
    only = sys.argv[1:]  # 可选: 仅探测指定 slug 列表
    targets = PROBE_TARGETS
    if only:
        only_set = set(only)
        targets = [t for t in PROBE_TARGETS if t[0] in only_set]

    print(f"[信息] 探测 {len(targets)} 本书的前 3 页…")
    ok = 0
    fail = 0
    for slug, pdf in targets:
        if probe_one(slug, pdf, pages=3):
            ok += 1
        else:
            fail += 1
    print(f"\n[汇总] 成功 {ok}, 失败 {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
