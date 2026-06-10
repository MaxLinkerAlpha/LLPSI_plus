"""verify_v3_detail.py - 详细分析 FAIL 案例"""
import json
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
v6 = json.loads((ROOT / "analysis_output" / "reader_vocab_stats_v6.json").read_text(encoding="utf-8"))
routing = json.loads((ROOT / "analysis_output" / "llpsi_reader_routing_v2.json").read_text(encoding="utf-8"))


def find_book(slug, data):
    for r in data:
        if r["slug"] == slug:
            return r
    return None


# 详细看 fabellae_latinae
print("=" * 70)
print("fabellae_latinae 所有段 (找 INSVLA)")
print("=" * 70)
fab = find_book("fabellae_latinae", v6)
for s in fab["segments"][:15]:
    print(f"  #{s['idx']} tokens={s['tokens']} t80={s['t80']} t70={s['t70']} t50={s['t50']}")
    print(f"    {s['preview'][:100]}")


# 详细看 cambridge_1 含 "Quintus" 段
print("\n" + "=" * 70)
print("cambridge_1 含 'Quintus' 的段 (v3 后)")
print("=" * 70)
cam1 = find_book("cambridge_1", v6)
quintus = [s for s in cam1["segments"] if "Quintus" in s["preview"]]
print(f"  找到 {len(quintus)} 段")
for s in quintus[:10]:
    print(f"  #{s['idx']} tokens={s['tokens']} t80={s['t80']} t70={s['t70']} t50={s['t50']}")
    print(f"    {s['preview'][:100]}")


# 检查 Cap.1 中所有 fluent 段
print("\n" + "=" * 70)
print("Cap.1 fluent_segments 全列表")
print("=" * 70)
cap1 = [r for r in routing["routing"] if r["chapter"] == 1][0]
for s in cap1["fluent_segments"]:
    print(f"  {s['slug']} #{s['seg_idx']} tokens={s['tokens']} score={s['score']:.3f} t80={s['t80']}")
    print(f"    {s['preview'][:80]}")


print("\n" + "=" * 70)
print("Cap.1 challenging_segments 全列表")
print("=" * 70)
for s in cap1["challenging_segments"]:
    print(f"  {s['slug']} #{s['seg_idx']} tokens={s['tokens']} score={s['score']:.3f} t70={s['t70']}")
    print(f"    {s['preview'][:80]}")


print("\n" + "=" * 70)
print("Cap.1 selected_segments 全列表")
print("=" * 70)
for s in cap1["selected_segments"]:
    print(f"  {s['slug']} #{s['seg_idx']} tokens={s['tokens']} score={s['score']:.3f} t50={s['t50']}")
    print(f"    {s['preview'][:80]}")
