#!/usr/bin/env python3
"""清理质量验证 v1_0_0 — 对比 form_chapter_map.json vs form_chapter_map_cleaned.json"""

import json, random

with open("form_chapter_map.json") as f: orig = json.load(f)
with open("form_chapter_map_cleaned.json") as f: clean = json.load(f)

print(f"原始: {len(orig):,} → 清理: {len(clean):,}  ({len(clean)/len(orig)*100:.1f}%)")
print()

# === 1. 100 常用词测试 ===
test_words = [
    "est","et","in","non","sed","sum","ego","tu","ille","hic",
    "puer","puella","vir","femina","dominus","servus","mater","pater",
    "bonus","malus","magnus","parvus","multus","unus","duo","tres",
    "iam","nunc","semper","ubi","cur","quis","quid","quod","quia",
    "aqua","terra","mare","caelum","sol","luna","stella","flumen",
    "insula","mons","via","domus","hortus","oppidum","urbs","roma",
    "italia","graecia","hispania","germania","gallia","aegyptus",
    "manus","oculus","caput","corpus","pes","digitus","auris",
    "amo","video","audio","dico","facio","venio","eo","habeo",
    "do","sto","pono","lego","scribo","cano","curro","navigo",
    "porta","fenestra","lectus","mensa","sella",
]
missing = [w for w in test_words if w not in clean]
print(f"[1] 100 常用词测试: 缺失 {len(missing)}/100")
if missing:
    print(f"    缺失: {missing}")
else:
    print("    ✅ 全部保留")

# === 2. 被删条目抽样 ===
deleted_keys = [k for k in orig if k not in clean]
random.seed(42)
samples = random.sample(deleted_keys, min(80, len(deleted_keys)))

# 检查是否有"看起来像真拉丁词"的被误删
false_positives = []
for k in samples:
    latin_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\u0101\u0113\u012B\u014D\u016B\u0233\u01E2")
    is_latin = all(c in latin_chars for c in k)
    if is_latin and len(k) >= 3:
        false_positives.append((k, orig[k]))

print(f"\n[2] 被删条目抽样 ({len(samples)} 条): 疑似拉丁真词被误删: {len(false_positives)}")
for k, v in false_positives[:10]:
    print(f"    \"{k}\" → Cap{v}")

# === 3. 抢救的新增词 ===
rescue_new = [k for k in clean if k not in orig]
print(f"\n[3] 抢救新增词: {len(rescue_new)} 条")
rescue_sample = random.sample(rescue_new, min(20, len(rescue_new)))
for k in sorted(rescue_sample):
    print(f"    \"{k}\" → Cap{clean[k]}")

# === 4. 整体统计 ===
print(f"\n[4] 清洗统计:")
print(f"    删除: {len(deleted_keys):,} 条 ({len(deleted_keys)/len(orig)*100:.1f}%)")
print(f"    保留: {len(orig)-len(deleted_keys):,} 条")
print(f"    新增: {len(rescue_new):,} 条 (从管道/斜杠抢救)")
print(f"    最终: {len(clean):,} 条")
