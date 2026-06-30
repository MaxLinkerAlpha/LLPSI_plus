#!/usr/bin/env python3
"""rewrite_cap10_missing.py — 补充 Cap.10 缺失的 6 篇故事。
策略：只用 Cap.1-10 安全词汇，确保 v2_level ≤ 12。
"""

import json, re, sys, os
from pathlib import Path
from datetime import datetime, timezone

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

STORIES = {}

# ============================================================
# 中篇 (medius) x4
# ============================================================

STORIES["cap10_31"] = {
    "title_la": "Britannia et Hibernia",
    "title_zh": "不列颠与爱尔兰",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Duae insulae magnae in mari sunt. "
        "Britannia est prima insula. Hibernia est secunda insula. "
        "Britannia est magna. Hibernia est magna. "
        "Britannia est prope terram. Hibernia est prope Britanniam. "
        "In Britannia, multi montes sunt. In Britannia, multae silvae sunt. "
        "In Britannia, multae aquae sunt. "
        "Viri in Britannia sunt fortes. Viri in Britannia in silvis habitant. "
        "In Hibernia, multi montes sunt. In Hibernia, multae silvae sunt. "
        "In Hibernia, multae herbae sunt. Hibernia est viridis. "
        "Viri in Hibernia sunt fortes. Viri in Hibernia in silvis habitant. "
        "Vir Romanus de his insulis audit. "
        "Vir: 'Britannia et Hibernia — duae insulae magnae. "
        "Ego has insulas videre volo.' "
        "Vir ad Britanniam it. Vir in Britannia est. "
        "Vir montes videt. Vir silvas videt. "
        "Vir: 'Britannia est magna. Britannia est pulchra. "
        "Montes sunt magni. Silvae sunt pulchrae.' "
        "Vir in Britannia ambulat. Vir multa videt. "
        "Vir viros in Britannia videt. "
        "Viri sunt boni. Viri virum Romanum vident. "
        "Vir: 'Salve, viri! Ego ex Italia venio.' "
        "Viri: 'Salve, vir! Italia est terra pulchra.' "
        "Vir: 'Britannia quoque est pulchra.' "
        "Vir de Hibernia audit. Vir: 'Hibernia est prope Britanniam.' "
        "Vir ad Hiberniam it. Vir in Hibernia est. "
        "Vir montes videt. Vir silvas videt. Vir herbas videt. "
        "Vir: 'Hibernia est viridis. Hibernia est pulchra. "
        "Herbae sunt multae. Terra est bona.' "
        "Vir viros in Hibernia videt. "
        "Viri sunt boni. Viri virum Romanum vident. "
        "Vir: 'Britannia et Hibernia — duae insulae pulchrae. "
        "Duae insulae in mari. Duae portae ad alias terras.' "
        "Et vir in Hibernia laetus est."
    ),
}

STORIES["cap10_32"] = {
    "title_la": "Canis et puer",
    "title_zh": "狗与男孩",
    "target_chapter": 10,
    "theme": "20 友谊",
    "style": "白话",
    "genre": "A 日常生活",
    "character_type": "男孩",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer parvus est. Puer in villa habitat. "
        "Puer canem habet. Canis est parvus. Canis est niger. "
        "Puer canem amat. Canis puerum amat. "
        "Puer et canis amici sunt. "
        "Omni die, puer et canis in horto ludunt. "
        "Puer baculum iactat. Canis baculum capit. "
        "Canis ad puerum currit. Canis baculum dat. "
        "Puer ridet. Canis caudam movet. "
        "Puer: 'Tu es bonus canis. Ego te amo.' "
        "Canis puerum spectat. Canis non dicit — sed canis amat. "
        "Aliquando, puer tristis est. "
        "Puer in horto sedet. Puer non ridet. "
        "Canis ad puerum venit. Canis puerum spectat. "
        "Canis caput in pueri manu ponit. "
        "Puer canem tangit. Puer: 'Tu es amicus meus.' "
        "Puer non iam tristis est. Puer ridet. "
        "Aliquando, canis aeger est. "
        "Canis in terra iacet. Canis non ludit. "
        "Puer ad canem venit. Puer: 'Quid est, amice?' "
        "Puer cani aquam dat. Puer cani cibum dat. "
        "Puer prope canem sedet. Puer canem tangit. "
        "Puer: 'Ego te non relinquam. Ego te semper amabo.' "
        "Post tres dies, canis bonus est. Canis surgit. "
        "Canis ad puerum currit. Canis caudam movet. "
        "Puer ridet. Puer: 'Tu es bonus! Tu es amicus meus!' "
        "Puer et canis in horto ludunt. "
        "Puer baculum iactat. Canis baculum capit. "
        "Puer: 'Canis est amicus. Canis est bonus. "
        "Canis semper me amat. Et ego semper canem amo.' "
        "Et puer et canis in horto laeti sunt."
    ),
}

STORIES["cap10_33"] = {
    "title_la": "Mare et terra",
    "title_zh": "海与陆",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "精炼",
    "genre": "G 哲理寓言",
    "character_type": "旅人",
    "length_tier": "中篇",
    "narrative_mode": "对话体",
    "text": (
        "Mare et terra sunt duo. "
        "Mare est magnum. Terra est magna. "
        "Mare est aqua. Terra est terra. "
        "Mare et terra non sunt idem. Sed mare et terra sunt una. "
        "Vir ad mare venit. Vir mare spectat. "
        "Vir: 'Mare, tu es magnum. Ego te video. "
        "Tu es altum. Tu es longum. Tu es pulchrum.' "
        "Mare non respondet. Mare undas movet. "
        "Vir ad terram venit. Vir terram spectat. "
        "Vir: 'Terra, tu es magna. Ego te video. "
        "Tu es bona. Tu es patria. Tu es pulchra.' "
        "Terra non respondet. Terra arbores movet. "
        "Vir inter mare et terram stat. "
        "Vir: 'Mare et terra — duo et una. "
        "Mare terram tangit. Terra mare tangit. "
        "Ubi mare est, terra non est. Ubi terra est, mare non est. "
        "Sed mare et terra sunt una.' "
        "Alius vir venit. Alius vir est senex. "
        "Senex: 'Quid vides, vir?' "
        "Vir: 'Mare et terram video. Duo et una.' "
        "Senex: 'Mare et terra sunt sicut vita et mors. "
        "Vita est terra — solida, certa. "
        "Mors est mare — profunda, magna. "
        "Sed vita et mors sunt una.' "
        "Vir: 'Quomodo sunt una?' "
        "Senex: 'Sine terra, mare non est. Sine mari, terra non est. "
        "Sine vita, mors non est. Sine morte, vita non est. "
        "Omnia sunt una. Omnia sunt partes unius.' "
        "Vir tacet. Vir mare et terram spectat. "
        "Vir: 'Ego video. Mare et terra sunt una. "
        "Vita et mors sunt una. Omnia sunt una.' "
        "Et vir inter mare et terram laetus est."
    ),
}

STORIES["cap10_34"] = {
    "title_la": "Puer et avis",
    "title_zh": "男孩与鸟",
    "target_chapter": 10,
    "theme": "21 自由",
    "style": "白话",
    "genre": "G 哲理寓言",
    "character_type": "男孩",
    "length_tier": "中篇",
    "narrative_mode": "第三人称",
    "text": (
        "Puer in horto est. Puer avem videt. "
        "Avis est parva. Avis est pulchra. "
        "Avis in terra est. Avis non volat. "
        "Puer ad avem it. Avis non timet. "
        "Puer avem capit. Puer avem in manu tenet. "
        "Puer: 'Avis parva, tu es pulchra. Ego te servabo.' "
        "Puer avem in villa portat. "
        "Puer avem in parva casa ponit. "
        "Puer avi cibum dat. Puer avi aquam dat. "
        "Avis cibum edit. Avis aquam bibit. "
        "Puer laetus est. Puer: 'Ego avem habeo. Avis est mea.' "
        "Puer omni die ad avem it. Puer avi cibum dat. "
        "Avis puerum videt. Avis non timet. "
        "Sed avis non cantat. Avis tristis est. "
        "Puer: 'Cur non cantas, avis? Cur tristis es?' "
        "Avis puerum spectat. Avis non dicit. "
        "Puer ad patrem it. Puer: 'Pater, avis mea est tristis. "
        "Cur avis tristis est?' "
        "Pater: 'Avis in caelo habitat. Avis libera est. "
        "Avis in casa non est laeta.' "
        "Puer: 'Sed ego avem amo. Ego avem servare volo.' "
        "Pater: 'Amor non est servare. Amor est liberare. "
        "Si avem amas, avem libera.' "
        "Puer tacet. Puer putat. "
        "Puer ad avem it. Puer avem spectat. "
        "Puer: 'Avis, ego te amo. Ego te liberabo.' "
        "Puer avem capit. Puer ad hortum it. "
        "Puer manus aperit. Avis in manu stat. "
        "Avis puerum spectat. Tum avis volat. "
        "Avis in caelo est. Avis cantat. "
        "Puer avem in caelo videt. "
        "Puer tristis est — sed puer quoque laetus est. "
        "Puer: 'Avis est libera. Avis est laeta. Et ego sum laetus.' "
        "Puer ad patrem it. Puer: 'Pater, ego avem liberavi.' "
        "Pater: 'Bene, fili. Tu avem amavisti. "
        "Verus amor est liberare.' "
        "Et puer in horto laetus est."
    ),
}

# ============================================================
# 中长篇 (longior) x1
# ============================================================

STORIES["cap10_35"] = {
    "title_la": "Tria flumina Europae",
    "title_zh": "欧洲的三条河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "中长篇",
    "narrative_mode": "第三人称",
    "text": (
        "Tria flumina magna in Europa sunt. "
        "Primum flumen est Rhenus. Rhenus est magnum. "
        "Rhenus in terra quarta est. Rhenus est limes imperii. "
        "Rhenus terram quartam ab aliis terris dividit. "
        "Rhenus per multa oppida fluit. "
        "Rhenus aquam multis terris dat. "
        "Rhenus est flumen altum. Rhenus est flumen longum. "
        "Secundum flumen est Danuvius. Danuvius est magnum. "
        "Danuvius per multas terras fluit. "
        "Danuvius in monte magno incipit. "
        "Danuvius ad mare it. Danuvius est longum. "
        "Danuvius multa oppida tangit. "
        "Danuvius aquam multis terris dat. "
        "Tertium flumen est Rhodanus. Rhodanus est magnum. "
        "Rhodanus in terra quarta est. "
        "Rhodanus per montes fluit. Rhodanus ad mare it. "
        "Rhodanus est flumen pulchrum. "
        "Rhodanus aquam multis oppidis dat. "
        "Vir Romanus de his fluminibus putat. "
        "Vir: 'Tria flumina — tres viae. "
        "Rhenus est limes. Danuvius est longum. "
        "Rhodanus est pulchrum. "
        "Omnia flumina sunt magna. Omnia sunt bona.' "
        "Vir ad Rhenum it. Vir Rhenum spectat. "
        "Vir: 'Rhenus est magnum. Rhenus terras dividit. "
        "Sed Rhenus quoque terras coniungit. "
        "Per Rhenum, viri ad alias terras eunt.' "
        "Vir ad Danuvium it. Vir Danuvium spectat. "
        "Vir: 'Danuvius est longum. Danuvius per multas terras fluit. "
        "Danuvius est via magna aquae.' "
        "Vir ad Rhodanum it. Vir Rhodanum spectat. "
        "Vir: 'Rhodanus est pulchrum. Rhodanus per montes fluit. "
        "Rhodanus est donum terrae.' "
        "Vir: 'Tria flumina — tria dona. "
        "Flumina sunt venae terrae. "
        "Sine fluminibus, terrae non sunt bonae. "
        "Flumina sunt vitae.' "
        "Et vir prope flumen laetus est."
    ),
}

# ============================================================
# 长篇 (longus) x1
# ============================================================

STORIES["cap10_36"] = {
    "title_la": "Tria flumina Europae",
    "title_zh": "欧洲的三条河",
    "target_chapter": 10,
    "theme": "18 自然",
    "style": "白话",
    "genre": "C 历史与人物",
    "character_type": "罗马人",
    "length_tier": "长篇",
    "narrative_mode": "第一人称",
    "text": (
        "Ego vir sum. Ego multas terras vidi. "
        "Ego multa flumina vidi. "
        "Iam, ego de tribus fluminibus dico. "
        "Primum flumen est Rhenus. Rhenus est magnum. "
        "Rhenus in terra quarta est. "
        "Rhenus est limes imperii Romani. "
        "Rhenus terram quartam ab aliis terris dividit. "
        "Rhenus per multa oppida fluit. "
        "Rhenus aquam multis terris dat. "
        "Rhenus est flumen altum. Rhenus est flumen longum. "
        "Ego ad Rhenum eo. Ego Rhenum specto. "
        "Rhenus est magnus. Aqua est pura. "
        "Ego: 'Rhenus est magnus. Rhenus terras dividit. "
        "Sed Rhenus quoque terras coniungit. "
        "Per Rhenum, viri ad alias terras eunt. "
        "Per Rhenum, res ex una terra ad aliam terram eunt.' "
        "Ego aquam Rheni bibo. Aqua est bona. "
        "Secundum flumen est Danuvius. Danuvius est magnum. "
        "Danuvius per multas terras fluit. "
        "Danuvius in monte magno incipit. "
        "Danuvius ad mare it. "
        "Danuvius est longum. Danuvius multa oppida tangit. "
        "Ego ad Danuvium eo. Ego Danuvium specto. "
        "Danuvius est longus. Danuvius est pulcher. "
        "Ego: 'Danuvius est longum. Danuvius per multas terras fluit. "
        "Danuvius est via magna aquae. "
        "Per Danuvium, viri ad multas terras eunt.' "
        "Ego aquam Danuvii bibo. Aqua est bona. "
        "Tertium flumen est Rhodanus. Rhodanus est magnum. "
        "Rhodanus in terra quarta est. "
        "Rhodanus per montes fluit. Rhodanus ad mare it. "
        "Rhodanus est flumen pulchrum. "
        "Rhodanus aquam multis oppidis dat. "
        "Ego ad Rhodanum eo. Ego Rhodanum specto. "
        "Rhodanus est pulcher. Aqua est clara. "
        "Ego: 'Rhodanus est pulchrum. Rhodanus per montes fluit. "
        "Rhodanus est donum terrae. "
        "Montes et flumen sunt pulchri.' "
        "Ego aquam Rhodani bibo. Aqua est bona. "
        "Ego de tribus fluminibus puto. "
        "Ego: 'Tria flumina — tria dona. "
        "Rhenus est limes. Danuvius est longum. "
        "Rhodanus est pulchrum. "
        "Omnia flumina sunt magna. Omnia sunt bona. "
        "Flumina sunt venae terrae. "
        "Sine fluminibus, terrae non sunt bonae. "
        "Flumina sunt vitae. Flumina sunt res.' "
        "Et ego, prope flumen, laetus sum."
    ),
}

# ============================================================
# 测试与写入
# ============================================================

if __name__ == "__main__":
    print(f"共 {len(STORIES)} 篇故事待测试\n")

    passed = 0
    failed = 0

    for story_id, story in STORIES.items():
        title = story["title_la"]
        text = story["text"]
        tier = story["length_tier"]

        result = evaluate(text, title)
        level = result["v2_level"]
        rate = result["v2_rate"]

        status = "PASS" if level is not None and level <= 12 else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"  {status} | v2={level} | rate={rate:.1f}% | {tier:4s} | {title}")

        if status == "FAIL" and result["v2_oov"]:
            print(f"         OOV ({len(result['v2_oov'])}): {result['v2_oov'][:10]}")

    print(f"\n{'='*60}")
    print(f"通过: {passed}/{len(STORIES)}  失败: {failed}/{len(STORIES)}")

    if failed == 0:
        print("\n全部通过！开始写入文件...")
        for story_id, story in STORIES.items():
            title_slug = story["title_la"].lower().replace(" ", "_").replace("?", "").replace("!", "")
            tier_map = {"中篇": "medius", "中长篇": "longior", "长篇": "longus"}
            tier_slug = tier_map.get(story["length_tier"], "medius")

            cap_dir = REALITATES_DIR / "Cap10"
            existing = sorted(cap_dir.glob(f"Cap10_{title_slug}_{tier_slug}_*.md"))
            if existing:
                nums = [int(f.stem.split("_")[-1]) for f in existing]
                next_num = max(nums) + 1
            else:
                next_num = 1

            fname = f"Cap10_{title_slug}_{tier_slug}_{next_num:03d}.md"
            fpath = cap_dir / fname

            now = datetime.now(timezone.utc).isoformat()
            yaml = f"""---
story_id: "{story_id}"
title_la: "{story['title_la']}"
title_zh: "{story['title_zh']}"
target_chapter: {story['target_chapter']}
theme: "{story['theme']}"
style: "{story['style']}"
genre: "{story['genre']}"
character_type: "{story['character_type']}"
length_tier: "{story['length_tier']}"
narrative_mode: "{story['narrative_mode']}"
word_count: {len(story['text'].split())}
macrons_status: "generated"
evaluated_chapter: {result['v2_level']}
best_fit_chapter: {result['v2_best_fit']}
coverage_rate: {result['v2_rate']}
oov_words: {result['v2_oov']}
rewritten_from: "brevis"
rewritten_at: "{now}"
status: "rewritten"
---
"""
            content = yaml + "\n" + story["text"] + "\n"

            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"  已写入: {fname}")

        print("\n全部完成！")
    else:
        print(f"\n还有 {failed} 篇未通过，需要调整。")