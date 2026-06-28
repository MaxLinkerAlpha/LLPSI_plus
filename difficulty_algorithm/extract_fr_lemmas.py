#!/usr/bin/env python3
"""从 FR 多语词汇表 Excel 提取干净的原形词列表。"""

import json
import re
import openpyxl

SRC = "../source/LLPSI/vocab/LLPSI_vocab_core_multilingue_I.xlsx"
DST = "fr_lemmas.json"

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["Sheet1"]

lemmas = []
for row in ws.iter_rows(min_row=2, values_only=True):
    latine = str(row[0]).strip() if row[0] else ""
    if not latine or latine.startswith("-"):
        continue
    # 取第一个词为主原形，跳过变异形式说明（如 -iō -iēcisse）
    lemma = latine.split()[0]
    lemma = re.sub(r"^~", "", lemma)          # 去 ~tulisse 前缀
    lemma = re.sub(r"\(.*?\)", "", lemma)      # 去除括号内注解
    lemmas.append(lemma)

print(f"FR 提取原形词: {len(lemmas)}")
print(f"示例: {lemmas[:12]}")

with open(DST, "w", encoding="utf-8") as f:
    json.dump(lemmas, f, ensure_ascii=False, indent=2)
print(f"已保存 → {DST}")
