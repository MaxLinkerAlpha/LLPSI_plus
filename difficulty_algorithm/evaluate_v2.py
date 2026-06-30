#!/usr/bin/env python3
"""
难度评估 v2_4_0 — 带词形还原（lemmatization）+ CLI。
- 外部文本先分词 → 剥长音 → simplemma 还原 → 查 lemma_chapter_map
- 85% 类型覆盖率阈值
- 对比 v1（无还原）和 v2（有还原）的收录率提升
- 新增：out_of_vocabulary 超纲词清单
- v2_4_0：新增 --file PATH 参数，自动识别 .md 文件并跳过 YAML frontmatter
- v2_3_0：v2 算法在 simplemma 前增加长音剥离（simplemma 不识别长音字符），
           修复 v2 率虚低 5-10% 的问题（v1 已有此预处理）
- v2_2_0：新增 CLI（--text / --json），配合 merge_yaml.py 管线使用
"""

import argparse
import json
import os
import glob
import re
from statistics import median

import simplemma

# ========== 加载映射表 ==========
with open("lemma_chapter_map.json", encoding="utf-8") as f:
    LEMMA_CHAPTER = json.load(f)  # 原形 → 最早章节号

with open("word_chapter_map.json", encoding="utf-8") as f:
    WORD_CHAPTER = json.load(f)  # 词形 → 最早章节号

# 归一化映射表（去长音 + 小写）
NORMALIZED_MAP = {}
for word, ch in WORD_CHAPTER.items():
    clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], word).lower()
    if clean not in NORMALIZED_MAP or ch < NORMALIZED_MAP[clean]:
        NORMALIZED_MAP[clean] = ch

with open("fr_lemmas.json", encoding="utf-8") as f:
    FR_LEMMAS = set(json.load(f))


def _print_loaded():
    """打印数据加载摘要（输出到 stderr，避免污染 CLI JSON 输出）"""
    import sys
    print(f"已加载: lemma_chapter={len(LEMMA_CHAPTER)}  word_chapter={len(WORD_CHAPTER)}  normalized={len(NORMALIZED_MAP)}  FR_lemmas={len(FR_LEMMAS)}", file=sys.stderr)


# ========== 分词 ==========
def tokenize(text: str) -> list:
    """简单分词：按空格和标点切分，保留长度≥2的词。"""
    tokens = []
    for w in re.split(r"[\s\.,;:\!\?\"\'\(\)\[\]\{\}—\-–/]+", text):
        w = w.strip()
        if len(w) >= 2:
            tokens.append(w)
    return tokens


# ========== 核心评估函数 ==========
def evaluate(text: str, name: str = "unnamed") -> dict:
    """对一段拉丁语文本评估难度等级。"""
    tokens = tokenize(text)
    unique_types = list(dict.fromkeys(tokens))  # 保持顺序去重
    total_types = len(unique_types)

    # --- v1: 无词形还原 ---
    v1_matched = set()
    for w in unique_types:
        if w in WORD_CHAPTER:
            v1_matched.add(w)
        else:
            clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
            if clean in NORMALIZED_MAP:
                v1_matched.add(w)

    # --- v2: 有词形还原（先剥长音，simplemma 不识别长音字符）---
    v2_matched = set()
    v2_chapters = []
    for w in unique_types:
        # 剥长音：āēīōūȳ → aeiouy
        clean = re.sub(r"[āēīōūȳĀĒĪŌŪȲ]", lambda m: "aeiouyAEIOUY"["āēīōūȳĀĒĪŌŪȲ".index(m.group(0))], w).lower()
        try:
            lemma = simplemma.lemmatize(clean, lang="la")
        except Exception:
            lemma = clean
        if lemma in LEMMA_CHAPTER:
            v2_matched.add(w)
            v2_chapters.append(LEMMA_CHAPTER[lemma])

    v1_rate = len(v1_matched) / total_types * 100 if total_types else 0
    v2_rate = len(v2_matched) / total_types * 100 if total_types else 0

    # --- v2 难度等级（85% 覆盖率阈值）---
    level = None
    level_verdict = ""
    out_of_vocabulary = [w for w in unique_types if w not in v2_matched]
    if v2_chapters:
        sorted_ch = sorted(v2_chapters)
        idx_85 = int(len(sorted_ch) * 0.85)
        if idx_85 >= len(sorted_ch):
            idx_85 = len(sorted_ch) - 1
        threshold_ch = sorted_ch[idx_85]

        if len(v2_matched) / total_types >= 0.85:
            level = threshold_ch
            level_verdict = f"第 {level} 章"
        else:
            level_verdict = f"降级（最高覆盖 {len(v2_matched)/total_types*100:.0f}%  @ 第 {threshold_ch} 章）"
    else:
        level_verdict = "降级（无可匹配词）"

    return {
        "name": name,
        "total_types": total_types,
        "v1_matched": len(v1_matched),
        "v1_rate": round(v1_rate, 1),
        "v2_matched": len(v2_matched),
        "v2_rate": round(v2_rate, 1),
        "v2_level": level,
        "v2_best_fit": threshold_ch if v2_chapters else None,
        "v2_verdict": level_verdict,
        "v2_oov": out_of_vocabulary,
        "gain": round(v2_rate - v1_rate, 1),
    }


# ========== CLI / 测试入口 ==========
if __name__ == "__main__":
    import sys

    # ========== CLI 模式（供 merge_yaml.py 等下游调用）==========
    parser = argparse.ArgumentParser(description="LLPSI 拉丁语难度评估 v2")
    parser.add_argument("--text", help="要评估的拉丁语文本")
    parser.add_argument("--file", help="要评估的 .md 文件路径（自动跳过 YAML frontmatter）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出评估结果")
    parser.add_argument("--name", default="unnamed", help="文本名称（用于 JSON 输出）")
    args_cli = parser.parse_args()

    if args_cli.text or args_cli.file:
        _print_loaded()
        if args_cli.file:
            # 自动读取 .md 文件并跳过 YAML frontmatter
            with open(args_cli.file, encoding="utf-8") as f:
                content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                text_input = parts[2].strip() if len(parts) >= 3 else content
            else:
                text_input = content
            if not args_cli.name or args_cli.name == "unnamed":
                args_cli.name = args_cli.file.split("/")[-1]
        else:
            text_input = args_cli.text
        r = evaluate(text_input, args_cli.name)
        if args_cli.json:
            # 仅输出纯 JSON——不可有任何其他打印，否则 merge_yaml.py 会解析失败
            print(json.dumps(r, ensure_ascii=False))
        else:
            print(f"v2_rate={r['v2_rate']}  v2_level={r['v2_level']}  v2_verdict={r['v2_verdict']}  oov={r['v2_oov']}")
        sys.exit(0)

    # ========== 默认：运行全量测试（向后兼容）==========
    _print_loaded()

    # ========== 交叉验证: simplemma vs FR ==========
    print("\n" + "=" * 60)
    print("[交叉验证] simplemma 原形 vs FR 单词表")
    our_lemmas = set(LEMMA_CHAPTER.keys())
    overlap = our_lemmas & FR_LEMMAS
    print(f"  FR 单词表: {len(FR_LEMMAS)}")
    print(f"  simplemma 输出: {len(our_lemmas)}")
    print(f"  交集: {len(overlap)}  ({len(overlap)/len(FR_LEMMAS)*100:.1f}% of FR)")

    # 抽样显示不匹配的 FR 词条
    fr_not_matched = FR_LEMMAS - our_lemmas
    print(f"  未匹配的 FR 条目（抽样 20）:")
    for i, w in enumerate(sorted(fr_not_matched)[:20]):
        print(f"    {w}")

    # ========== test_text  ==========
    # ========== 测试: Fabulae Syrae 手工采样故事 ==========
    print("\n" + "=" * 60)
    print("[测试] Fabulae Syrae 采样故事 — v1 vs v2 对比")

    # 手工采样的干净文本（之前从 PDF 提取的）
    FS_SAMPLES = {
        "Europa (FS Cap.26)": "Iuppiter aliquando Phoenicen pervenit. Ibi virginem pulcherrimam nomine Europam conspexit. Quae cum eam conspexisset, eius amore captus est. Sed consilium cepit quomodo eam acciperet. In taurum candidum se mutavit et ad eam accessit. Primo Europa timuit, sed postea eum tractavit. Taurus se in genua posuit, et virgo in tergum eius ascendit. Tum repente in mare se proiecit et natavit. Europa autem, cum se in mari vidisset, magnopere timuit. Sed frustra — nullus ei reditus erat. Taurus eam trans aequor ad insulam Cretam portavit. Iuppiter ibi formam suam recepit et Europae amorem suum confessus est. Europa postea nomen terrae illi dedit.",
        "Tarpeia (FS Cap.26)": "Tarpeia virgo Romana erat, quae cum patre suo in arce habitabat. Cum Titus Tatius, rex Sabinorum, Romam oppugnaret, Tarpeia ad fontem aquam petitum descendit. Ibi eam Sabini conspexerunt. Ei polliciti sunt dona quae in manibus sinistris gerebant, si eis portam arcis aperiusset. Illa vero cupiditate armillarum aurearum ducta consensit. Sabini autem, cum portam apertam invenissent, non modo armillas, sed etiam scuta in eam proiecerunt. Ita Tarpeia, quae patriam prodiderat, armis Sabinorum obruta periit.",
        "Atalanta (FS Cap.28)": "Atalanta virgo pulcherrima erat et pedibus celerrima. Huic oraculum dixerat ne nuberet. Illa igitur omnibus procis ita respondit: Nemo mihi coniunx erit, nisi me cursu vicerit. Sed qui victus erit, morte afficietur. Multi tamen iuvenes, eius pulchritudine capti, cum ea certaverunt, sed omnes victi morte affecti sunt. Tandem Hippomenes certamen iniit. Is tria mala aurea a Venere acceperat. Quae cum curreret, mala in viam proiecit. Atalanta, cupiditate malorum commota, substitit ut ea tolleret. Ita Hippomenes prior ad metam pervenit et puellam in matrimonium duxit.",
        "Orpheus et Eurydice (FS Cap.29)": "Orpheus, filius Apollinis, lyra tam pulchre canebat ut ferae ad eum accederent et arbores se moverent. Is Eurydicem nympham amabat. Quae cum in prato ambularet, serpens eam momordit, et statim mortua est. Orpheus, amore uxoris motus, ad inferos descendit. Ibi lyra tam dulce canebat ut Cerberus obmutuisset et umbrae lacrimarent. Pluto autem et Proserpina, cum eum audivissent, permoti sunt. Ei permiserunt ut uxorem in lucem reduceret, sed ea condicione ne retro respiceret. Ille vero prope exitum timens ne uxor non sequeretur, oculos retorsit. Statim Eurydice evanuit et Orpheus ingenti luctu affectus est.",
        "Daphne (FS Cap.32)": "Apollo, cum Pythonem serpentem sagittis interfecisset, superbus erat. Cum autem Cupidinem vidisset arcum parantem, ei dixit: Quid tibi cum armis, puer? Cupido respondit: Tibi forsitan non nocebunt, sed te meis sagittis figam. Duas sagittas habebat: altera amorem facit, altera fugat. Aurea Apollinem percussit; plumbea autem Daphnen, filiam Penei fluminis. Apollo igitur statim Daphnen amare coepit. Illa autem cum eum fugientem videret, ocius etiam aufugit. Apollo: Mane, Nympha, non hostis sum! Illa neque restitit neque respondit, sed cursum intendit. Cum autem fessa esset et prope esset ut caperetur, patrem Peneum oravit ut se mutaret. Statim in laurum mutata est. Apollo, etsi mutatam, tamen amavit; folia eius sibi coronam fecit.",
        "Baucis et Philemon (FS Cap.29)": "Iuppiter et Mercurius, cum hominum mores experirentur, humanam formam sumpserunt et per terras vagabantur. Cum mille domos adiissent, nemo eis hospitium dare voluit. Tandem ad parvam casam pervenerunt. Ibi Baucis et Philemon, senes pauperes, eos libenter acceperunt. Mensam cum pedibus brevibus posuerunt. Olera, ova, et vinum apposuerunt. Cum autem vini crater numquam evacuaretur, senes deos esse intellexerunt. Iuppiter eis dixit: Quia nos ita bene accepistis, optate quid vobis fieri velitis. Illi petiverunt ut sacerdotes templi fierent et ut eadem hora morerentur. Cum mors eis appropinquaret, Philemon in quercum, Baucis in tilium mutata est.",
    }

    print(f"{'故事':30s} {'类型数':>5} {'v1收录率':>8} {'v2收录率':>8} {'提升':>6} {'评级':>25}")
    print("-" * 90)

    summary = []
    for name, text in FS_SAMPLES.items():
        r = evaluate(text, name)
        summary.append(r)
        print(f"{name:30s} {r['total_types']:>5} {r['v1_rate']:>7.1f}% {r['v2_rate']:>7.1f}% {r['gain']:>+5.1f}% {r['v2_verdict']:>25}")

    # 汇总
    avg_v1 = sum(s["v1_rate"] for s in summary) / len(summary)
    avg_v2 = sum(s["v2_rate"] for s in summary) / len(summary)
    print(f"\n{'平均':30s} {'':>5} {avg_v1:>7.1f}% {avg_v2:>7.1f}% {avg_v2-avg_v1:>+5.1f}%")
    rated = [s for s in summary if s["v2_level"] is not None]
    print(f"可评级故事: {len(rated)}/{len(summary)}")

    if rated:
        print("\n评级结果:")
        for r in rated:
            print(f"  {r['name']:30s} → 第 {r['v2_level']} 章")

    # ========== 自身验证 ==========
    print("\n" + "=" * 60)
    print("[自身验证] LLPSI 章节用 v2 自测")

    project_root = os.path.join(os.path.dirname(__file__), "..")
    ocr_root = os.path.join(project_root, "OCR", "LLPSI_core")
    chapters_to_test = [1, 3, 5, 7, 10, 13, 15, 18, 20, 23, 25, 28, 30, 33, 35, 38, 40, 43, 45, 48, 50, 53, 55]

    for cap_num in chapters_to_test:
        if cap_num <= 35:
            fpath = os.path.join(ocr_root, "familia_romana", f"fr_cap{cap_num}", f"cap{cap_num}_main_macrons_final.txt")
        else:
            fpath = os.path.join(ocr_root, "roma_aeterna", f"ra_cap{cap_num}", f"cap{cap_num}_main_macrons_final.txt")
        if not os.path.exists(fpath):
            print(f"  Cap.{cap_num:02d} 文件不存在: {fpath}")
            continue
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        r = evaluate(text, f"LLPSI Cap.{cap_num}")
        deviation = (r["v2_level"] or 0) - cap_num
        mark = "✓" if r["v2_level"] == cap_num else f"偏离{deviation:+d}"
        print(f"  Cap.{cap_num:02d}  v2: {r['v2_verdict']:20s}  ({mark})")

    print("\n=== 完成 ===")
