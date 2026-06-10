#!/usr/bin/env python3
"""
rename_source.py — 重命名 source/ 下所有文件
==============================================
按 RENAME_MAP 字典, 将旧名映射为新名, 支持 --dry-run 预览。
"""

import argparse
import os
import sys


RENAME_MAP = {
    # ----- core: 核心教材 -----
    "LLPSI_Part I, Familia Romana.pdf":
        "LLPSI_core_familia_romana.pdf",
    "LLPSI_Part I Familia Romana可复制版.pdf":
        "LLPSI_core_familia_romana_text_selectable.pdf",
    "LLPSI_Pars_II_Roma_Aeterna.pdf":
        "LLPSI_core_roma_aeterna.pdf",
    "LLPSI_Pars II Roma Aeterna高清二版彩插.pdf":
        "LLPSI_core_roma_aeterna_hd_2nd_color.pdf",
    "LLPSI_Pars_II_Indices.pdf":
        "LLPSI_core_indices.pdf",

    # ----- grammar: 语法书与说明 -----
    "LLPSI_Pars_I_Grammatica_Latina.pdf":
        "LLPSI_grammar_grammatica_latina.pdf",
    "LLPSI_Pars_II_Instructions.pdf":
        "LLPSI_grammar_instructions.pdf",

    # ----- exercitia: 练习册 -----
    "LLPSI_Pars_I_Exercitia_Latina_I.pdf":
        "LLPSI_exercitia_latina_I.pdf",
    "LLPSI_Pars_II_Exercitia_Latina_II.pdf":
        "LLPSI_exercitia_latina_II.pdf",

    # ----- vocab: 词汇表 -----
    "LLPSI_Pars_I_Latin-English_Vocabulary_I.pdf":
        "LLPSI_vocab_latine_anglicus_I.pdf",
    "LLPSI_Pars_II_Latin-English_Vocabulary_I-II.pdf":
        "LLPSI_vocab_latine_anglicus_I_II.pdf",
    "LLPSI_Pars_I_Vocabulaire_latin-francais_I.pdf":
        "LLPSI_vocab_latine_gallicus_I.pdf",
    "LLPSI_Pars_I_Vocabulario_Latino-Espanol_I.pdf":
        "LLPSI_vocab_latine_hispanicus_I.pdf",
    "LLPSI_vocabula_multilingue.pdf":
        "LLPSI_vocab_multilingue.pdf",
    "LLPSI_vocabula_multilingue.xlsx":
        "LLPSI_vocab_multilingue.xlsx",
    "LLPSI_Supplementa_Colloquia_Personarum_Vocabulary.pdf":
        "LLPSI_vocab_colloquia_personarum.pdf",
    "LLPSI_Supplementa_Sermones_Romani_Vocabulary.pdf":
        "LLPSI_vocab_sermones_romani.pdf",
    "LLPSI_Supplementa_Petronii_Cena_Trim._Vocabulary.pdf":
        "LLPSI_vocab_cena_trimalchionis.pdf",
    "LLPSI_Supplementa_Vergilii_Aeneis_Vocabulary.pdf":
        "LLPSI_vocab_aeneis.pdf",
    "LLPSI_Supplementa_Caesaris_De_Bello_Gall_Vocabulary.pdf":
        "LLPSI_vocab_bello_gallico.pdf",

    # ----- multimedia: 多媒体 -----
    "LLPSI_Pars_I_Latine_Disco.pdf":
        "LLPSI_multimedia_latine_disco.pdf",

    # ----- reader: 补充读物 -----
    # 新的 2nd edition HD 是主版本 (新)
    "LLPSI_Colloquia Personarum, Second Edition (Hans H. Ørberg) .pdf":
        "LLPSI_reader_colloquia_personarum.pdf",
    # 旧 1st edition scan 归档
    "LLPSI_Supplementa_Colloquia_Personarum.pdf":
        "LLPSI_reader_colloquia_personarum_v1_scan.pdf",
    "LLPSI_Fabulae Syrae (Luigi Miraglia) 可复制.pdf":
        "LLPSI_reader_fabulae_syrae.pdf",
    "LLPSI_Supplementa_Fabellae_Latinae.pdf":
        "LLPSI_reader_fabellae_latinae.pdf",
    "LLPSI_Supplementa_Sermones_Romani.pdf":
        "LLPSI_reader_sermones_romani.pdf",
    "LLPSI_Supplementa_Caesaris_De_Bello_Gallico.pdf":
        "LLPSI_reader_bello_gallico.pdf",
    "LLPSI_Supplementa_Catilina.pdf":
        "LLPSI_reader_catilina.pdf",
    "LLPSI_Supplementa_Petronii_Cena_Trimalchionis.pdf":
        "LLPSI_reader_cena_trimalchionis.pdf",
    "LLPSI_Supplementa_Plauti_Amphitryo.pdf":
        "LLPSI_reader_amphitryo.pdf",
    "LLPSI_Supplementa_Vergilii_Aeneis_I_IV.pdf":
        "LLPSI_reader_aeneis.pdf",
    "LLPSI_Supplementa_Ovidii_Ars_Amatoria.pdf":
        "LLPSI_reader_ars_amatoria.pdf",
    "LLPSI_Epitome Historiae Sacrae Brevi Christi Vitae Narr.pdf":
        "LLPSI_reader_epitome_historiae_sacrae.pdf",
    "LLPSI_T. Lucretii Cari De rerum natura_I. Armella, J.A. Cepelak, L.Miraglia, E. M. Smith.pdf":
        "LLPSI_reader_de_rerum_natura.pdf",

    # ----- teacher: 教师资源 -----
    "LLPSI_Teacher_s_Materials_and_Answer_Key.pdf":
        "LLPSI_teacher_materials_and_answer_key.pdf",
    "LLPSI_Teacher_s_Materials__Conseils_au_prof.pdf":
        "LLPSI_teacher_conseils_au_prof.pdf",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", default="source")
    parser.add_argument("--dry-run", action="store_true", help="只打印, 不执行")
    args = parser.parse_args()

    src = args.source_dir
    if not os.path.isdir(src):
        print(f"  [错误] {src} 不是有效目录", file=sys.stderr)
        sys.exit(1)

    actual_files = set(os.listdir(src))
    expected_olds = set(RENAME_MAP.keys())

    # 检查缺失
    missing = expected_olds - actual_files
    if missing:
        print(f"  [警告] 预期要重命名的文件不存在:")
        for m in sorted(missing):
            print(f"          - {m}")
        print()

    # 检查新增
    extras = actual_files - expected_olds
    if extras:
        print(f"  [提示] source/ 中有 RENAME_MAP 未覆盖的文件 (将被忽略):")
        for e in sorted(extras):
            print(f"          - {e}")
        print()

    # 执行重命名
    renamed = 0
    for old_name, new_name in sorted(RENAME_MAP.items()):
        old_path = os.path.join(src, old_name)
        new_path = os.path.join(src, new_name)
        if not os.path.exists(old_path):
            continue
        if old_path == new_path:
            continue
        if os.path.exists(new_path):
            print(f"  [跳过] 目标已存在: {new_name}")
            continue
        if args.dry_run:
            print(f"  [预览] {old_name}")
            print(f"       → {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"  [完成] {old_name} → {new_name}")
            renamed += 1

    print()
    if args.dry_run:
        print(f"  [DRY RUN] 预览完成, 实际未执行")
    else:
        print(f"  [汇总] 共重命名 {renamed} 个文件")


if __name__ == "__main__":
    main()
