"""verify_v3.py - 验证 v3 算法的关键案例

检查项:
1. cambridge_1 Stage 1 "Quintus est filius" (6 tokens) -> 应被过滤 (tokens<15)
2. cambridge_1 Stage 2 "amicus Caecilium visitat" (73 tokens) -> 应进入 Cap.2 流畅
3. "INSVLA et OPPIDVM vocabula Latina" -> vocab 表, 不应出现
4. 罗马数字列表 "XI XII XIII" -> 不应出现
"""
import json
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")

# 加载 v3 数据
v6 = json.loads((ROOT / "analysis_output" / "reader_vocab_stats_v6.json").read_text(encoding="utf-8"))
routing = json.loads((ROOT / "analysis_output" / "llpsi_reader_routing_v2.json").read_text(encoding="utf-8"))

# 加载 v3 pre 备份做对比
v6_pre = json.loads((ROOT / "analysis_output" / "reader_vocab_stats_v6_pre_v3.json").read_text(encoding="utf-8"))
routing_pre = json.loads((ROOT / "analysis_output" / "llpsi_reader_routing_v2_pre_v3.json").read_text(encoding="utf-8"))


def find_book(slug, data):
    for r in data:
        if r["slug"] == slug:
            return r
    return None


def find_book_in_routing(slug, routing_data):
    for r in routing_data["routing"]:
        for s in r["fluent_segments"] + r["challenging_segments"] + r["selected_segments"]:
            if s["slug"] == slug:
                yield r["chapter"], s


def check(label, ok, detail=""):
    icon = "[PASS]" if ok else "[FAIL]"
    print(f"  {icon} {label}: {detail}")
    return ok


print("=" * 70)
print("案例1: cambridge_1 'Quintus est filius' (6 tokens) -> 应被过滤")
print("=" * 70)
cam1 = find_book("cambridge_1", v6)
# 找含 "Quintus est filius" 的段
hits_v3 = [s for s in cam1["segments"] if "Quintus" in s["preview"] or "quintus" in s["preview"].lower()]
cam1_pre = find_book("cambridge_1", v6_pre)
hits_pre = [s for s in cam1_pre["segments"] if "Quintus" in s["preview"] or "quintus" in s["preview"].lower()]
print(f"  v3 含 'Quintus' 的段数: {len(hits_v3)}")
print(f"  pre-v3 含 'Quintus' 的段数: {len(hits_pre)}")
if hits_pre:
    print(f"  pre-v3 样例: tokens={hits_pre[0]['tokens']}, preview={hits_pre[0]['preview'][:100]}")
check("案例1: 6-token 段被过滤", len(hits_v3) == 0,
      f"v3 有 {len(hits_v3)} 段 (应 0), pre-v3 有 {len(hits_pre)} 段 (过滤前存在)")


print("\n" + "=" * 70)
print("案例2: cambridge_1 'amicus Caecilium visitat' (73 tokens) -> Cap.2 流畅")
print("=" * 70)
# 找含 "amicus" 且 tokens>30 的段
hits = [s for s in cam1["segments"] if "amicus" in s["preview"].lower() and s["tokens"] > 30]
print(f"  v3 找到 {len(hits)} 个含 'amicus' 的长段")
for h in hits[:3]:
    print(f"    idx={h['idx']} tokens={h['tokens']} t80={h['t80']} t70={h['t70']} t50={h['t50']}")
    print(f"    preview: {h['preview'][:80]}")
# 路由中 Cap.2 是否有 cambridge_1 fluent
cap2 = [r for r in routing["routing"] if r["chapter"] == 2][0]
cam1_fluent_cap2 = [s for s in cap2["fluent_segments"] if s["slug"] == "cambridge_1"]
print(f"  Cap.2 fluent 列表中 cambridge_1 段数: {len(cam1_fluent_cap2)}")
cam1_challenge_cap2 = [s for s in cap2["challenging_segments"] if s["slug"] == "cambridge_1"]
print(f"  Cap.2 challenge 列表中 cambridge_1 段数: {len(cam1_challenge_cap2)}")
cam1_selected_cap2 = [s for s in cap2["selected_segments"] if s["slug"] == "cambridge_1"]
print(f"  Cap.2 selected 列表中 cambridge_1 段数: {len(cam1_selected_cap2)}")
check("案例2: cambridge_1 至少一段在 Cap.2 推荐池",
      len(cam1_fluent_cap2) + len(cam1_challenge_cap2) + len(cam1_selected_cap2) > 0,
      f"fluent={len(cam1_fluent_cap2)} challenge={len(cam1_challenge_cap2)} selected={len(cam1_selected_cap2)}")


print("\n" + "=" * 70)
print("案例3: 'INSVLA et OPPIDVM vocabula Latina' (vocab 表) -> 不应在 Cap.1 fluent")
print("=" * 70)
cap1 = [r for r in routing["routing"] if r["chapter"] == 1][0]
insvla = [s for s in cap1["fluent_segments"] + cap1["challenging_segments"] + cap1["selected_segments"]
          if "INSVLA" in s["preview"] or "insvla" in s["preview"].lower() or "OPPIDVM" in s["preview"]]
print(f"  Cap.1 推荐池中含 INSVLA/OPPIDVM 段数: {len(insvla)}")
for s in insvla[:3]:
    print(f"    {s['slug']} #{s['seg_idx']} tokens={s['tokens']}: {s['preview'][:80]}")
check("案例3: vocab 表 INSVLA 段未进入 Cap.1 推荐", len(insvla) == 0,
      f"找到 {len(insvla)} 段 (应 0)")


print("\n" + "=" * 70)
print("案例4: 罗马数字列表 'XI XII XIII' -> 不应出现")
print("=" * 70)
# 检查所有路由的 fluent 段, 找纯罗马数字的
roman = []
for r in routing["routing"]:
    for s in r["fluent_segments"] + r["challenging_segments"] + r["selected_segments"]:
        prev = s["preview"].strip()
        # 罗马数字检测: 全部由罗马数字字符组成, 且较短
        rom = prev.replace(" ", "").replace("\n", "")
        if rom and all(c in "IVXLCDM" for c in rom) and len(rom) > 1:
            roman.append((r["chapter"], s))
print(f"  路由中纯罗马数字段数: {len(roman)}")
for ch, s in roman[:5]:
    print(f"    Cap.{ch} {s['slug']} #{s['seg_idx']} tokens={s['tokens']}: {s['preview'][:80]}")
check("案例4: 纯罗马数字列表段被过滤", len(roman) == 0, f"找到 {len(roman)} 段 (应 0)")


print("\n" + "=" * 70)
print("对比 Cap.1-3 路由前后 cambridge_1/oxford_1/ecce_romani 出现次数")
print("=" * 70)
for slug in ["cambridge_1", "oxford_1", "ecce_romani"]:
    print(f"\n  [{slug}]")
    for ch in [1, 2, 3]:
        r_v3 = [r for r in routing["routing"] if r["chapter"] == ch][0]
        r_pre = [r for r in routing_pre["routing"] if r["chapter"] == ch][0]
        v3_f = sum(1 for s in r_v3["fluent_segments"] if s["slug"] == slug)
        v3_c = sum(1 for s in r_v3["challenging_segments"] if s["slug"] == slug)
        v3_s = sum(1 for s in r_v3["selected_segments"] if s["slug"] == slug)
        pre_f = sum(1 for s in r_pre["fluent_segments"] if s["slug"] == slug)
        pre_c = sum(1 for s in r_pre["challenging_segments"] if s["slug"] == slug)
        pre_s = sum(1 for s in r_pre["selected_segments"] if s["slug"] == slug)
        print(f"    Cap.{ch}: "
              f"v3=(F:{v3_f} C:{v3_c} S:{v3_s}) "
              f"pre=(F:{pre_f} C:{pre_c} S:{pre_s})")


print("\n" + "=" * 70)
print("全局段数统计")
print("=" * 70)
v3_total = sum(r["counts"]["fluent"] + r["counts"]["challenging"] + r["counts"]["selected"]
               for r in routing["routing"])
pre_total = sum(r["counts"]["fluent"] + r["counts"]["challenging"] + r["counts"]["selected"]
                for r in routing_pre["routing"])
print(f"  v3 总段数: {v3_total}")
print(f"  pre-v3 总段数: {pre_total}")
print(f"  变化: {v3_total - pre_total:+d} ({(v3_total - pre_total) / pre_total * 100:.1f}%)")
