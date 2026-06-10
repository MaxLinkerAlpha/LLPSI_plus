"""debug_cap1_cambridge1.py - 调试 cambridge_1 段在 Cap.1 的实际表现"""
import json
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
v6 = json.loads((ROOT / "analysis_output" / "reader_vocab_stats_v6.json").read_text(encoding="utf-8"))


def find_book(slug, data):
    for r in data:
        if r["slug"] == slug:
            return r
    return None


cam1 = find_book("cambridge_1", v6)
# 找所有 t50=1 的 cambridge_1 段
cap1_segs = [s for s in cam1["segments"] if s["t50"] == 1]
print(f"cambridge_1 中 t50=1 段数: {len(cap1_segs)}")
for s in cap1_segs:
    print(f"  #{s['idx']} tokens={s['tokens']} t80={s['t80']} t70={s['t70']} t50={s['t50']} s50={s['s50']:.3f}")
    print(f"    {s['preview'][:80]}")


print(f"\ncambridge_1 中 tokens>=15 且 t50=1 段数 (应进入 Cap.1 selected):")
cap1_filtered = [s for s in cap1_segs if s["tokens"] >= 30]
print(f"  满足 tokens>=30 词数硬限制: {len(cap1_filtered)}")
for s in cap1_filtered[:5]:
    print(f"    #{s['idx']} tokens={s['tokens']} t50={s['t50']} s50={s['s50']:.3f}")


# 检查 Cap.1 路由
routing = json.loads((ROOT / "analysis_output" / "llpsi_reader_routing_v2.json").read_text(encoding="utf-8"))
cap1 = [r for r in routing["routing"] if r["chapter"] == 1][0]
print(f"\nCap.1 路由中 cambridge_1 段:")
print(f"  fluent: {len([s for s in cap1['fluent_segments'] if s['slug'] == 'cambridge_1'])}")
print(f"  challenging: {len([s for s in cap1['challenging_segments'] if s['slug'] == 'cambridge_1'])}")
print(f"  selected: {len([s for s in cap1['selected_segments'] if s['slug'] == 'cambridge_1'])}")
