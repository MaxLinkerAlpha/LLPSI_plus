"""verify_v3_focused.py - 精确验证 v3 算法的关键案例"""
import json
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
v6 = json.loads((ROOT / "analysis_output" / "reader_vocab_stats_v6.json").read_text(encoding="utf-8"))
v6_pre = json.loads((ROOT / "analysis_output" / "reader_vocab_stats_v6_pre_v3.json").read_text(encoding="utf-8"))
routing = json.loads((ROOT / "analysis_output" / "llpsi_reader_routing_v2.json").read_text(encoding="utf-8"))
routing_pre = json.loads((ROOT / "analysis_output" / "llpsi_reader_routing_v2_pre_v3.json").read_text(encoding="utf-8"))


def find_book(slug, data):
    for r in data:
        if r["slug"] == slug:
            return r
    return None


def chk(label, ok, detail=""):
    icon = "[PASS]" if ok else "[FAIL]"
    print(f"  {icon} {label}")
    if detail:
        print(f"        {detail}")
    return ok


# === 案例1: 6-token "Quintus est filius" 段是否被过滤 ===
print("=" * 70)
print("案例1: 6-token 段 'Quintus est filius' 是否被过滤")
print("=" * 70)
cam1_v3 = find_book("cambridge_1", v6)
cam1_pre = find_book("cambridge_1", v6_pre)

# pre-v3 中确认有 6-token 段
short_pre = [s for s in cam1_pre["segments"] if s["tokens"] < 15]
print(f"  pre-v3: cambridge_1 tokens<15 段数: {len(short_pre)}")
for s in short_pre[:3]:
    print(f"    pre #{s['idx']} tokens={s['tokens']}: {s['preview'][:80]}")

# v3 中是否还有 tokens<15 的段
short_v3 = [s for s in cam1_v3["segments"] if s["tokens"] < 15]
print(f"  v3: cambridge_1 tokens<15 段数: {len(short_v3)}")
chk("案例1: v3 后 cambridge_1 中 tokens<15 段已为 0", len(short_v3) == 0,
    f"pre={len(short_pre)} -> v3={len(short_v3)}")

# 全局: v3 后所有书的 tokens<15 段数
all_short_pre = sum(1 for b in v6_pre for s in b["segments"] if s["tokens"] < 15)
all_short_v3 = sum(1 for b in v6 for s in b["segments"] if s["tokens"] < 15)
print(f"  全局: pre={all_short_pre} 段 tokens<15, v3={all_short_v3}")
chk("案例1: 全局 tokens<15 段数大幅减少 (>=50%)",
    all_short_v3 < all_short_pre * 0.5,
    f"pre={all_short_pre} -> v3={all_short_v3} (减少 {(1 - all_short_v3/all_short_pre)*100:.1f}%)")


# === 案例2: 73-token "amicus Caecilium visitat" 进入 Cap.1 节选 ===
print("\n" + "=" * 70)
print("案例2: 'amicus Caecilium visitat' (73 tokens) 路由到哪")
print("=" * 70)
amicus = [s for s in cam1_v3["segments"]
          if "amicus" in s["preview"].lower() and s["tokens"] >= 70]
print(f"  v3 中 73+ token 含 'amicus' 的段数: {len(amicus)}")
for s in amicus[:3]:
    print(f"    #{s['idx']} tokens={s['tokens']} t80={s['t80']} t70={s['t70']} t50={s['t50']}")
    print(f"    {s['preview'][:80]}")

# Cap.1 selected 是否包含该段 (t50=1)
cap1 = [r for r in routing["routing"] if r["chapter"] == 1][0]
cap1_sel = [s for s in cap1["selected_segments"] if s["slug"] == "cambridge_1" and s["tokens"] >= 70]
print(f"  Cap.1 selected 列表中 cambridge_1 长段数 (tokens>=70): {len(cap1_sel)}")
for s in cap1_sel:
    print(f"    #{s['seg_idx']} tokens={s['tokens']} score={s['score']:.3f}")
    print(f"    {s['preview'][:80]}")

# 段 #4 (73 tokens) 的 t50=1, 所以应该进入 Cap.1 节选
target = [s for s in cam1_v3["segments"] if s["idx"] == 4 and s["tokens"] == 73]
if target:
    t = target[0]
    print(f"  目标段 #{t['idx']}: t50={t['t50']}, t70={t['t70']}, t80={t['t80']}")
    if t["t50"] == 1:
        chk("案例2: 73-token 'amicus' 段 t50=1, 进入 Cap.1 节选列表", True,
            f"出现在 Cap.1 selected_segments 中? {len(cap1_sel) > 0}")
    else:
        chk("案例2: 73-token 'amicus' 段 t50≠1, 不会进 Cap.1", False,
            f"t50={t['t50']}")


# === 案例3: "INSVLA" 段本质 (fabellae_latinae) ===
print("\n" + "=" * 70)
print("案例3: INSVLA 段本质分析")
print("=" * 70)
fab_v3 = find_book("fabellae_latinae", v6)
insvla = [s for s in fab_v3["segments"] if "INSVLA" in s["preview"]]
print(f"  v3 fabellae_latinae 含 INSVLA 段数: {len(insvla)}")
for s in insvla:
    print(f"    #{s['idx']} tokens={s['tokens']} t80={s['t80']} t70={s['t70']} t50={s['t50']} s80={s['s80']:.3f}")
    print(f"    preview: {s['preview'][:200]}")


# === 案例4: 罗马数字列表 ===
print("\n" + "=" * 70)
print("案例4: 罗马数字列表")
print("=" * 70)
roman = []
for r in routing["routing"]:
    for cat in ("fluent_segments", "challenging_segments", "selected_segments"):
        for s in r[cat]:
            prev = s["preview"].strip()
            rom = prev.replace(" ", "").replace("\n", "")
            if rom and all(c in "IVXLCDM" for c in rom) and len(rom) > 1:
                roman.append((r["chapter"], s))
print(f"  路由中纯罗马数字段数: {len(roman)}")
chk("案例4: 纯罗马数字列表段被过滤", len(roman) == 0,
    f"找到 {len(roman)} 段 (应 0)")


# === 全局统计对比 ===
print("\n" + "=" * 70)
print("全局段数对比")
print("=" * 70)
v3_total = sum(r["counts"]["fluent"] + r["counts"]["challenging"] + r["counts"]["selected"]
               for r in routing["routing"])
pre_total = sum(r["counts"]["fluent"] + r["counts"]["challenging"] + r["counts"]["selected"]
                for r in routing_pre["routing"])
v3_per_ch = [(r["chapter"], r["counts"]) for r in routing["routing"]]
pre_per_ch = [(r["chapter"], r["counts"]) for r in routing_pre["routing"]]
v3_dict = dict(v3_per_ch)
pre_dict = dict(pre_per_ch)

print(f"  v3 总段数: {v3_total} (fluent+challenge+selected, 全 56 章)")
print(f"  pre-v3 总段数: {pre_total}")
print(f"  变化: {v3_total - pre_total:+d} ({(v3_total - pre_total) / pre_total * 100:.1f}%)")
print()
print(f"  各章变化 (top 10 差异):")
diffs = sorted([(ch, sum(v3_dict[ch].values()) - sum(pre_dict[ch].values())) for ch in range(1, 57)],
               key=lambda x: x[1])
for ch, diff in diffs[:5]:
    print(f"    Cap.{ch}: {sum(pre_dict[ch].values())} -> {sum(v3_dict[ch].values())} ({diff:+d})")
print("    ...")
for ch, diff in diffs[-5:]:
    print(f"    Cap.{ch}: {sum(pre_dict[ch].values())} -> {sum(v3_dict[ch].values())} ({diff:+d})")
