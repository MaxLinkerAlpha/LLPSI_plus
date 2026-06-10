#!/usr/bin/env python3
"""Cleanup and rename new LLPSI files. Move readers to source/.

Per user decisions:
- Delete A-class duplicates (clear B套装 reprints of existing source/)
- Keep all HD versions
- Keep some old/alternative versions (per user "保留所有 HD + 部分旧版")
- Delete Chinese tutorial files
- Delete 5.1MB Companion duplicate, keep 2.8MB
- Rename new categories: companion, exercitia_nova
"""
import os
import shutil
import sys

PROJECT = "/Users/max/Downloads/Projects/LLPSI+++"
NEW_DIR = os.path.join(PROJECT, "source/拉拉自然习得法推荐Lingua Latina per se Illustrata LLPSI")
SOURCE = os.path.join(PROJECT, "source")

# (old_path, new_name_or_None_if_delete)
# None for new_name means DELETE
# Same path means RENAME only
PLAN = [
    # ============ A-class: delete (clear duplicates) ============
    # B套装/Pars_I/ duplicates
    ("B套装（推荐）/Pars_I/LLPSI_Pars_I_Familia_Romana.pdf", None),
    ("B套装（推荐）/Pars_I/LLPSI_Pars_I_Grammatica_Latina.pdf", None),
    ("B套装（推荐）/Pars_I/LLPSI_Pars_I_Latine_Disco.pdf", None),
    ("B套装（推荐）/Pars_I/LLPSI_Pars_I_Exercitia_Latina_I.pdf", None),
    # B套装/Pars_II/ duplicates
    ("B套装（推荐）/Pars_II/LLPSI_Pars_II_Indices.pdf", None),
    ("B套装（推荐）/Pars_II/LLPSI_Pars_II_Instructions.pdf", None),
    ("B套装（推荐）/Pars_II/LLPSI_Pars_II_Latin-English_Vocabulary_I-II.pdf", None),
    ("B套装（推荐）/Pars_II/LLPSI_Pars_II_Exercitia_Latina_II.pdf", None),
    # B套装/Supplementa/ duplicates
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Caesaris_De_Bello_Gallico.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Catilina.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Colloquia_Personarum_Vocabulary.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Ovidii_Ars_Amatoria.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Petronii_Cena_Trimalchionis.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Plauti_Amphitryo.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Sermones_Romani.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Vergilii_Aeneis_I_IV.pdf", None),
    ("B套装（推荐）/Supplementa/LLPSI_Supplementa_Petronii_Cena_Trim.pdf", None),  # Will be re-added below as excerpt
    # B套装 root
    ("B套装（推荐）/LLPSI_Teacher_s_Materials_and_Answer_Key.pdf", None),
    # ============ HD versions: keep and rename ============
    ("其他版本（彩图高清等建议看看）/推荐LLPSI_Pars I Familia Romana彩插2版高清可复制.pdf",
     "LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf"),
    ("其他版本（彩图高清等建议看看）/LLPSI_Pars I Familia Romana高清彩插小体积.pdf",
     "LLPSI_core_familia_romana_hd_color_small.pdf"),
    ("其他版本（彩图高清等建议看看）/LLPSI_Pars II Roma Aeterna高清彩插2版.pdf",
     "LLPSI_core_roma_aeterna_hd_2nd_color_alt.pdf"),
    # ============ Old versions to keep (per "部分旧版") ============
    ("其他版本（彩图高清等建议看看）/Lingva Latina Pars I Familia Romana  2003.pdf",
     "LLPSI_core_familia_romana_2003_v1_scan.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingua Latina Pars I Familia Romana.pdf",
     "LLPSI_core_familia_romana_v1_scan.pdf"),
    ("B套装（推荐）/Pars_II/LLPSI_Pars_II_Roma_Aeterna.pdf",
     "LLPSI_core_roma_aeterna_v1_scan.pdf"),
    ("B套装（推荐）/Pars_II/LLPSI_Pars_II_Roma_Aeterna_sm.pdf",
     "LLPSI_core_roma_aeterna_v1_scan_sm.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingua Latina, Pars II Roma Aeterna .pdf",
     "LLPSI_core_roma_aeterna_1990_v1_scan.pdf"),
    ("其他版本（彩图高清等建议看看）/拉拉习得LLPSI_Pars II Roma Aeterna黑白清晰.pdf",
     "LLPSI_core_roma_aeterna_v1_bw.pdf"),
    # ============ Lingua/Lingva old versions to keep ============
    ("其他版本（彩图高清等建议看看）/Lingua Latina Pars I Grammatica Latina .pdf",
     "LLPSI_grammar_grammatica_latina_v1.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingua LatinaPars I Latine Disco Student's Manual.pdf",
     "LLPSI_multimedia_latine_disco_v1.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingua Latina Pars II Indices.pdf",
     "LLPSI_core_indices_v1.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingua Latina Pars II Roma Aeterna Instructions II .pdf",
     "LLPSI_grammar_instructions_v1.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingua Latina Latin-English Vocabulary II  Pars II .pdf",
     "LLPSI_vocab_latine_anglicus_I_II_v1.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingva Latina Pars II Exercitia Latina II.pdf",
     "LLPSI_exercitia_latina_II_v1.pdf"),
    ("其他版本（彩图高清等建议看看）/Lingva Latina Pars II Instructions .pdf",
     "LLPSI_grammar_instructions_v1_sm.pdf"),
    ("其他版本（彩图高清等建议看看）/LLPSI_vocabula_multilingue.pdf",
     "LLPSI_vocab_multilingue_v1.pdf"),
    # ============ TRULY NEW CONTENT (new categories) ============
    ("其他版本（彩图高清等建议看看）/Fabulae Syrae (Luigi Miraglia) .pdf",
     "LLPSI_reader_fabulae_syrae_1st_ed.pdf"),
    ("其他版本（彩图高清等建议看看）/推荐Nova exercitia Latina I soluta扩充练习册答案.pdf",
     "LLPSI_exercitia_nova_I_answers.pdf"),
    ("其他版本（彩图高清等建议看看）/推荐nova exercitia latina练习册扩充.pdf",
     "LLPSI_exercitia_nova_I_soluta.pdf"),
    ("其他版本（彩图高清等建议看看）/拉西注释-LLPSI教师-Nova_via_Latine_doceo.pdf",
     "LLPSI_teacher_nova_via_latine_doceo.pdf"),
    ("教辅类/新版伴侣Lingua Latina - A Companion to Familia Romana - Based on Hans Ørberg’s Latine Disco, with Vocabulary and Grammar (Jeanne Marie Neumann).pdf",
     "LLPSI_companion_familia_romana_neumann.pdf"),
    ("教辅类/新版伴侣Lingua Latina - A Companion to Roma Aeterna - Based on Hans Ørberg’s Instructions, with Vocabulary and Grammar (Jeanne Marie Neumann) .pdf",
     "LLPSI_companion_roma_aeterna_neumann.pdf"),
    ("教辅类/新版伴侣Lingua Latina - A Companion to Roma Aeterna- Based on Hans Ørbergs Instructions, with Vocabulary and Grammar (Jeanne Marie Neumann).pdf",
     None),  # DELETE 5.1MB duplicate
    ("教辅类/旧版伴侣Lingua Latina A College Companion based on Hans Ørbergs Latine Disco, with Vocabulary and Grammar 2007.djvu",
     "LLPSI_companion_familia_romana_2007_v1.djvu"),
    # ============ Chinese files: DELETE ============
    ("教辅类/拉英-LLPSI未知拉丁语短期班讲义STAGE 20 MEDICUS.docx", None),
    ("教辅类/拉英-LLPSI未知拉丁语短训班讲义.pdf", None),
    ("其他版本（彩图高清等建议看看）/拉丁语综合教程1课本.pdf", None),
]

def main():
    deleted = []
    moved = []
    errors = []
    for rel, new_name in PLAN:
        old = os.path.join(NEW_DIR, rel)
        if not os.path.exists(old):
            errors.append(f"  NOT FOUND: {old}")
            continue
        if new_name is None:
            # DELETE
            os.remove(old)
            deleted.append(rel)
        else:
            # MOVE to source/
            new = os.path.join(SOURCE, new_name)
            if os.path.exists(new):
                # Don't overwrite existing - skip
                errors.append(f"  ALREADY EXISTS in source/: {new_name}")
                continue
            shutil.move(old, new)
            moved.append((rel, new_name))
    print(f"\n[完成] 移动 {len(moved)} 个文件:")
    for rel, new in moved:
        print(f"  {rel[-60:]:60s}  →  {new}")
    print(f"\n[完成] 删除 {len(deleted)} 个文件:")
    for rel in deleted:
        print(f"  {rel}")
    if errors:
        print(f"\n[警告] {len(errors)} 个错误:")
        for e in errors:
            print(e)

if __name__ == "__main__":
    main()
