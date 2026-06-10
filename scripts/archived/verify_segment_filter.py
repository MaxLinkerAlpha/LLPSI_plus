#!/usr/bin/env python3
"""验证 HTML 中可点击段是否被正确过滤."""
import re
from pathlib import Path

HTML = Path("/Users/max/Downloads/Projects/LLPSI+++/analysis_output/LLPSI_Insights.html")
html_text = HTML.read_text(encoding="utf-8")

data_keys = re.findall(r'data-key="([^"]+)"', html_text)
unique = set(data_keys)
print(f"实际可点击 data-key 数: {len(data_keys)}")
print(f"唯一 key 数: {len(unique)}")
print()

# 验证剔除段不在 data-key 中
excluded = [
    "cambridge_1|4|7",
    "cambridge_1|54|57",
    "ecce_romani|33|35",
    "dooge_beginners_key|29|31",
    "latin_natural_method|36|40",
    "illiterati_1|318|321",
]
print("=== 剔除段检查 (期望 0) ===")
for ex in excluded:
    cnt = data_keys.count(ex)
    status = "OK" if cnt == 0 else "FAIL"
    print(f"  [{status}] {ex}: {cnt}")

print()
print("=== dooge 重复段检查 (期望 0) ===")
duplicates = ["dooge_beginners_2|214|219", "dooge_beginners_2|221|223"]
for d in duplicates:
    cnt = data_keys.count(d)
    status = "OK" if cnt == 0 else "FAIL"
    print(f"  [{status}] {d}: {cnt}")

print()
print("=== 胜出者检查 (期望 ≥1) ===")
winners = [
    "dooge_beginners|214|219",
    "dooge_beginners|221|223",
    "cambridge_2|2|6",
    "oxford_2|72|75",
    "wileys_real_latin|366|368",
]
for w in winners:
    cnt = data_keys.count(w)
    status = "OK" if cnt >= 1 else "FAIL"
    print(f"  [{status}] {w}: {cnt}")

print()
# 列出所有 unique key
print("=== 所有唯一段 (按字母排序) ===")
for k in sorted(unique):
    print(f"  {k}")
