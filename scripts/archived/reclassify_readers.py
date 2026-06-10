#!/usr/bin/env python3
"""
reclassify_readers.py — 基于 OCR 元信息 + ISBN 查询结果重新分类读物

输入:
  - analysis_output/reader_metadata.json (extract_metadata 输出)
  - analysis_output/reader_metadata_enriched.json (query_isbn 输出, 可选)
  - ocr_output/<slug>/_full.txt (用于章节标题采样)
  - source/Other_Readers/curated/<tier>/<slug>.<ext> (原软链)

输出:
  - source/Other_Readers/reclassified/<new_tier>/<slug>.<ext> (新软链)
  - analysis_output/reclassification_decisions.json (决策依据)
  - docs/reader_audit_report.md v2.0

新分类维度:
  1. 内容语言 (latin / mixed / english / classics)
  2. 难度区间 (A1 入门 / A2 初级 / B1 中级 / B2 中高级 / C 高级古典)
  3. 内容类型 (故事 / 对话 / 教材配套 / 学术 / 工具 / 古典原典)
  4. 入库建议 (强烈推荐 / 可入库 / 不入库)
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 优先使用 v2 (改进语言判定), 兼容 v1
META_FILE = ROOT / "analysis_output" / "reader_metadata_v2.json"
if not META_FILE.exists():
    META_FILE = ROOT / "analysis_output" / "reader_metadata.json"
ENRICHED_FILE = ROOT / "analysis_output" / "reader_metadata_enriched.json"
OCR_OUT = ROOT / "ocr_output"
CURATED = ROOT / "source" / "Other_Readers" / "curated"
RECLASSIFIED = ROOT / "source" / "Other_Readers" / "reclassified"
DECISIONS_FILE = ROOT / "analysis_output" / "reclassification_decisions.json"

# 已入库的 LLPSI / 古典原典 — 跳过重新分类
SKIP_SLUGS = {
    "aeneis", "amphitryo", "ars_amatoria", "catilina", "cena_trimalchionis",
    "colloquia_personarum", "de_bello_gallico", "de_rerum_natura",
    "epitome_historiae_sacrae", "fabellae_latinae", "fabulae_syrae",
    "roma_aeterna", "sermones_romani", "backup_v150_20260606_113934",
    "probe",  # 探测残留
}

# D 系列: 体系教材 (即使含文章, 教材配套也不入库)
D_TIER_BOOKS = {
    # Wheelock / Cambridge / Oxford / Reading Latin / D'Ooge / Ecce Romani / Gwynne
    "wheelock_7e", "wheelock_reader", "wheelock_answer_key",
    "cambridge_1", "cambridge_2", "cambridge_3", "cambridge_4",
    "oxford_1", "oxford_2", "oxford_3",
    "reading_latin_text", "reading_latin_grammar", "reading_latin_study_guide",
    "dooge_beginners", "dooge_beginners_2", "dooge_beginners_key",
    "ecce_romani", "gwynne",
    "teach_yourself", "beginners_latin_book", "latin_made_simple",
    "latin_natural_method", "latin_first_year_magoffin",
    "wileys_real_latin",
    "new_latin_primer", "revised_latin_primer",
    "illiterati_1", "illiterati_2",
}

# 工具/参考/语法书 → D 工具
D_TOOL_BOOKS = {
    "latin_stories_wheelock",  # 配合 Wheelock 教材
}


def find_tier_link(slug: str) -> tuple[str, Path] | None:
    """在 curated/ 下找到 slug 对应的 (tier, link_path)."""
    for tier_dir in CURATED.iterdir():
        if not tier_dir.is_dir():
            continue
        for link in tier_dir.iterdir():
            if link.is_symlink() and link.stem == slug:
                return tier_dir.name, link
    return None


def classify(slug: str, meta: dict) -> dict:
    """对单本书输出重新分类决策."""
    lang = meta.get("language", {})
    verdict = lang.get("verdict", "?")
    # v2 字段: weighted_latin/weighted_english (按词频加权, 0-1)
    latin_r = lang.get("weighted_latin", 0)
    english_r = lang.get("weighted_english", 0)
    latin_pages = lang.get("latin_pages", 0)
    english_pages = lang.get("english_pages", 0)
    isbn = meta.get("isbn") or "-"
    year = meta.get("year") or "-"
    word_count = meta.get("word_count_approx", 0)

    # 跳过已入库
    if slug in SKIP_SLUGS:
        return {"slug": slug, "action": "skip_already_indexed",
                "reason": "已入库到 corpus, 不再重新分类"}

    # D 体系教材: 即使含文章也不入库 (用户原意: "打散"指文章部分可考虑,
    # 但体系教材即使有文章, 段落选取难度也偏离 LLPSI 风格)
    if slug in D_TIER_BOOKS:
        # 但记录其"是否含可用文章"作为参考
        return {"slug": slug, "action": "skip_grammar_textbook",
                "tier": "D_textbook", "language": verdict,
                "latin_ratio": latin_r, "english_ratio": english_r,
                "isbn": isbn, "year": year,
                "reason": f"体系教材 ({'英语' if verdict == 'english' else '其他'}), 不论文章是否优质, 不入库"}

    if slug in D_TOOL_BOOKS:
        return {"slug": slug, "action": "skip_tool_book",
                "tier": "D_tool", "language": verdict,
                "latin_ratio": latin_r, "english_ratio": english_r,
                "isbn": isbn, "year": year,
                "reason": "工具/参考/语法书, 不入库"}

    # === 按 verdict 分类 ===
    if verdict in ("latin", "latin_mostly"):
        # 纯/主拉语: 强烈推荐入库
        if "conversational" in slug or "nunc_loquamur" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "B1_mixed_dialogue", "language": "latin",
                    "reason": "对话型入门拉语书, 适合 B1 口语补充"}
        if "pugio_bruti" in slug or "regulus" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin",
                    "reason": "纯拉语故事, 适合 A1 入门"}
        if "diocles_flora" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin",
                    "reason": "纯拉语故事, 适合 A1 入门"}
        if "fabulae_faciles" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin",
                    "reason": "经典拉语故事集, A1"}
        if "septimus" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin",
                    "reason": "经典拉语故事, A1"}
        if "nutting" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin",
                    "reason": "经典拉语故事, A2"}
        if "ora_maritima" in slug or "pro_patria" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin",
                    "reason": "经典 Sonnenschein 拉语故事, A1"}
        if "hobbitus" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "B2_latin_novel", "language": "latin",
                    "reason": "Tolkien 霍比特人拉语版, 纯拉语长篇小说, B2"}
        if "forum_lectiones" in slug or "unus_duo_tres" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin",
                    "reason": "Polis 习得法 Vol.1, 拉语为主, A1"}
        if "via_latina_romanorum" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin",
                    "reason": "Via Latina 拉语, A2 故事型"}
        if "chickering" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin",
                    "reason": "Chickering 经典初级拉语, A2"}
        if "latin_lower_forms" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin",
                    "reason": "Hardy 1889 经典拉语, A2"}
        if "sermones" in slug or "olimpia" in slug or "nunc" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "A2_mixed_story", "language": "latin_mostly",
                    "reason": "以拉语为主, 含少量英语教学说明"}
        # 默认
        return {"slug": slug, "action": "import_recommended",
                "new_tier": "A_latin_story", "language": "latin",
                "reason": "纯拉语, 适合 LLPSI 风格"}

    if verdict == "mixed":
        # 混合型: 检查是否以拉语为主, 还是有大量英语教学
        if "hobbitus" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B2_latin_novel", "language": "mixed",
                    "reason": "拉英混合小说 (Tolkien 拉语版), RA 后期文学性阅读"}
        if "nunc_loquamur" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B1_mixed_dialogue", "language": "mixed",
                    "reason": "引导式对话, 拉英对照, 可作口语补充"}
        if "olimpia" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_mixed_story", "language": "mixed",
                    "reason": "Olimpi 分层读物, 拉英对照适合 A2"}
        if "via_latina_easy" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B1_mixed_text", "language": "mixed",
                    "reason": "罗马地理介绍, 拉英对照 B1"}
        if "intermediate_oral_cicero" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B1_mixed_text", "language": "mixed",
                    "reason": "Cicero De Senectute 改写, B1"}
        if "second_year_latin" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B2_mixed_text", "language": "mixed",
                    "reason": "二年级选集 (Greenough), B2"}
        if "latin_stories" in slug:
            return {"slug": slug, "action": "skip_tool_book",
                    "new_tier": "D_tool", "language": "mixed",
                    "reason": "38 Latin Stories, 配合 Wheelock 教材"}
        if "forum_lectiones" in slug or "unus_duo_tres" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "A1_mixed_story", "language": "mixed",
                    "reason": "Polis 习得法, 拉语故事+英语教学说明, 适合 A1 但需预处理过滤英语部分"}
        if "reynolds" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B1_mixed_text", "language": "mixed",
                    "reason": "Reynolds 中级读物, 拉英对照 B1"}
        if "nutting" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "mixed",
                    "reason": "Nutting 拉语为主, 经典入门 A2"}
        if "via_latina_romanorum" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "mixed",
                    "reason": "Via Latina 拉语为主, A2"}
        # 默认 mixed
        return {"slug": slug, "action": "import_optional",
                "new_tier": "B_mixed_text", "language": "mixed",
                "reason": "拉英混合文本, 需人工筛选拉语段"}

    if verdict in ("english", "english_mostly", "other", "mixed"):
        # === 已知主体为拉语故事的"英语教学+拉语故事"型书籍 (OCR 误判) ===
        # 这些书的特征: 前后是英语教学说明, 中间是拉语故事, 但 OCR 整体扫描后
        # 英语比例高于拉语. 实际上主体内容是经典拉语故事, 应入库 A1_mixed_story
        LATIN_STORY_BOOKS = {
            "ora_maritima": "Sonnenschein 1900 经典拉语故事, A1",
            "pro_patria": "Sonnenschein 1907 经典拉语故事, A1",
            "fabulae_faciles": "Ritchie 1889 经典拉语故事集, A1",
            "septimus": "Chambers 1910 经典拉语故事, A1",
            "reynolds_reader": "Reynolds 经典中级拉语故事, B1",
            "via_latina_easy": "Collar 1897 Via Latina 拉语故事, A2",
            "nutting_reader": "Nutting 入门拉语故事, A1",
        }
        if slug in LATIN_STORY_BOOKS:
            # 只要有少量拉语 (latin_pages >= 10) 就归为 mixed_story
            # reynolds 比较特殊: 全书 400 页, 仅 20 页纯拉, 但混合页多
            if latin_pages >= 10 or "reynolds" in slug:
                tier = "B1_mixed_story" if "reynolds" in slug else "A1_mixed_story"
                if "via_latina_easy" in slug or "nutting" in slug:
                    tier = "A2_mixed_story"
                return {"slug": slug, "action": "import_recommended",
                        "new_tier": tier, "language": "latin_story_with_english_notes",
                        "reason": f"主体为拉语故事 ({LATIN_STORY_BOOKS[slug]}), "
                                  f"但含英语教学/注解, 需预处理提取拉语故事段"}

        # === Polis 习得法系列 (含英语教学说明, 拉语故事为主) ===
        POLIS_BOOKS = {"forum_lectiones", "unus_duo_tres", "pugio_bruti", "regulus"}
        if slug in POLIS_BOOKS:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_mixed_story", "language": "latin_with_english_notes",
                    "reason": "Polis 习得法 Vol.1, 拉语故事+英语教学说明, A1"}

        # === Olimpi 分层读物 ===
        OLIMPIA_BOOKS = {"olimpia_daedalus", "olimpia_pyramus", "olimpia_nicholas"}
        if slug in OLIMPIA_BOOKS:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_mixed_story", "language": "mixed",
                    "reason": "Olimpi 分层读物, 拉英对照适合 A2"}

        # === 中级/高级读本 ===
        if "intermediate_oral_cicero" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B1_mixed_text", "language": "english",
                    "reason": "Cicero De Senectute 改写, 英语为主, B1 补充"}
        if "second_year_latin" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B2_mixed_text", "language": "english",
                    "reason": "二年级选集 (Greenough), 英语注释, B2"}
        if "via_latina_romanorum" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin_mostly",
                    "reason": "Via Latina 拉语, A2 故事型"}
        if "chickering" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin",
                    "reason": "Chickering 经典初级拉语, A2"}
        if "latin_lower_forms" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin",
                    "reason": "Hardy 1889 经典拉语, A2"}

        # === 真正的英语为主, 跳过 ===
        if "conversational" in slug:
            return {"slug": slug, "action": "skip_english_dominant",
                    "tier": "skip", "language": "english",
                    "reason": "英语为主, 短语手册+少量对话, 拉语含量过低"}
        if "nunc_loquamur" in slug:
            return {"slug": slug, "action": "skip_english_dominant",
                    "tier": "skip", "language": "english",
                    "reason": "引导式对话, 英语教学说明占多, 拉语对话短"}

        # 其他英语为主的默认
        return {"slug": slug, "action": "skip_english_dominant",
                "tier": "skip", "language": "english",
                "reason": "英语为主, 不适合 LLPSI 风格入库"}

    if verdict == "other":
        # 拉语/英语都不显著 — 可能是古典拉语或专业文本
        if "fabulae_faciles" in slug or "septimus" in slug or "nutting" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A_latin_story", "language": "latin_mostly",
                    "reason": "经典拉语故事, 词表覆盖度因 OCR 噪声被低估, 实际是拉语"}
        if "pugio_bruti" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin_mostly",
                    "reason": "Pugio Bruti 习得法故事, 实际拉语为主"}
        if "intermediate_oral_cicero" in slug or "second_year_latin" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B_mixed_text", "language": "latin_mostly",
                    "reason": "中级读物, 拉语为主, 可能有英语词汇表"}
        if "via_latina_romanorum" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A2_latin_story", "language": "latin_mostly",
                    "reason": "Via Latina 拉语, A2 故事型"}
        if "latin_lower_forms" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "A2_mixed_story", "language": "latin_mostly",
                    "reason": "Hardy 1889, 拉语句子+英语注释"}
        if "new_latin_primer" in slug:
            return {"slug": slug, "action": "skip_grammar_textbook",
                    "tier": "D_textbook", "language": "other",
                    "reason": "语法书, 不入库"}
        if "pro_patria" in slug:
            return {"slug": slug, "action": "import_recommended",
                    "new_tier": "A1_latin_story", "language": "latin_mostly",
                    "reason": "Sonnenschein 1907, 拉语故事 A1"}
        if "via_latina_easy" in slug:
            return {"slug": slug, "action": "import_optional",
                    "new_tier": "B1_mixed_text", "language": "mixed",
                    "reason": "罗马地理, 拉英混合"}

        return {"slug": slug, "action": "import_optional",
                "new_tier": "B_other_text", "language": "other",
                "reason": "拉语/英语都不显著, 需人工审视"}

    return {"slug": slug, "action": "skip_unknown", "tier": "skip",
            "language": verdict, "reason": f"未知分类 ({verdict})"}


def main() -> int:
    if not META_FILE.exists():
        print(f"[错误] 找不到 {META_FILE}")
        return 1
    data = json.loads(META_FILE.read_text(encoding="utf-8"))
    enriched = {}
    if ENRICHED_FILE.exists():
        enriched_list = json.loads(ENRICHED_FILE.read_text(encoding="utf-8"))
        enriched = {e["slug"]: e.get("openlibrary") for e in enriched_list}

    # 删除旧 reclassified
    if RECLASSIFIED.exists():
        import shutil
        shutil.rmtree(RECLASSIFIED)
    RECLASSIFIED.mkdir(parents=True)

    decisions = []
    for entry in data:
        slug = entry["slug"]
        if slug not in SKIP_SLUGS and slug not in D_TIER_BOOKS and slug not in D_TOOL_BOOKS:
            tier_link = find_tier_link(slug)
            if tier_link is None:
                decisions.append({"slug": slug, "action": "skip_no_link",
                                 "reason": "未在 curated/ 下找到软链"})
                continue

        d = classify(slug, entry)
        # 加 enriched 信息
        if slug in enriched and enriched[slug]:
            d["openlibrary"] = enriched[slug]
        decisions.append(d)

        # 执行软链
        tier_link = find_tier_link(slug)
        if tier_link and d.get("action", "").startswith("import"):
            old_tier, link = tier_link
            new_tier = d["new_tier"]
            (RECLASSIFIED / new_tier).mkdir(parents=True, exist_ok=True)
            target = RECLASSIFIED / new_tier / link.name
            if not target.exists():
                import os
                os.symlink(str(link.resolve()), str(target))

    DECISIONS_FILE.write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2),
        encoding="utf-8")

    # 汇总
    actions = Counter(d.get("action", "?") for d in decisions)
    print(f"[分类决策] 总数 {len(decisions)}:")
    for act, n in actions.most_common():
        print(f"  {act}: {n}")
    print(f"\n[输出] {RECLASSIFIED}/")
    print(f"[决策] {DECISIONS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
