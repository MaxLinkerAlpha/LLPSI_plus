#!/usr/bin/env python3
"""
fill_gaps_v2.py — 用经算法验证的词汇重写故事。
Cap.1-5 可用词: puer, puella, pater, mater, filius, filia, hortus, aqua, rosa, ancilla, 
  domina, femina, oppidum, via, villa, liber, manus, fenestra, mensa, cubiculum, mare,
  sum, video, do, habeo, voco, ploro, capio, venio, amo, canto, audio, dormio, rideo, 
  taceo, disco, bonus, pulcher, laetus, iratus, parvus, magnus, meus, tuus, solus, novus
Cap.1-7 新增: curro, ambulo, specto, porta, malus, fessus
Cap.1-8 新增: sto, volo
"""

import json, re, sys, os
from pathlib import Path
from collections import defaultdict

REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
PROGRESS_FILE = Path(__file__).resolve().parent / "progress.json"
EVAL_DIR = Path(__file__).resolve().parent.parent / "difficulty_algorithm"

os.chdir(str(EVAL_DIR)); sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(str(Path(__file__).resolve().parent))

STORIES = {
    # === Cap.5: 1 篇 (只用 Cap.1-5 词) ===
    "cap5_11": {
        "title_la": "Pater et fīlius in hortō",
        "title_zh": "父与子在花园",
        "target_chapter": 5,
        "theme": "25 家庭",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "对话体",
        "text": "Pater et fīlius in hortō sunt. Pater fīlium videt. Fīlius patrem videt. Pater: 'Fīlī, tū bonus es.' Fīlius: 'Pater, tū bonus es.' Pater rīdet. Fīlius rīdet. Pater fīlium amat. Fīlius patrem amat. Fīlius laetus est. Pater laetus est."
    },

    # === Cap.7: 1 篇 (只用 Cap.1-7 词) ===
    "cap7_15": {
        "title_la": "Puerī in viā",
        "title_zh": "街上的男孩们",
        "target_chapter": 7,
        "theme": "13 孤独",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": "Duo puerī in viā sunt. Puerī currunt. Puerī rīdent. Ūnus puer ad alterum puerum venit. 'Quis es?' 'Puer sum.' 'Cūr sōlus es?' 'Amīcum nōn habeō.' 'Ego amīcus tuus sum.' Puerī rīdent. Puerī in viā ambulant. Puerī laetī sunt."
    },

    # === Cap.8: 8 篇 (只用 Cap.1-8 词) ===
    "cap8_11": {
        "title_la": "Puer ad portam",
        "title_zh": "门前的男孩",
        "target_chapter": 8,
        "theme": "22 旅程",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": "Puer ad portam stat. Porta magna est. Puer portam spectat. Puer exīre vult. Sed porta clausa est. Puer: 'Cūr porta clausa est?' Nēmō respondet. Puer manum ad portam tollit. Puer portam aperit. Puer in viā est. Puer laetus est. Puer ambulat."
    },
    "cap8_12": {
        "title_la": "Fīlia ad fenestram",
        "title_zh": "窗边的女孩",
        "target_chapter": 8,
        "theme": "18 自然",
        "style": "抒情",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": "Fīlia ad fenestram stat. Fenestra magna est. Fīlia hortum videt. In hortō rosae sunt. Rosae pulchrae sunt. Fīlia rosās amat. Māter venit. 'Quid vidēs?' 'Rosās videō.' Māter rīdet. 'Hortus pulcher est.' Fīlia: 'Ita. Hortus noster pulcher est.'"
    },
    "cap8_13": {
        "title_la": "Māter et fīlius aeger",
        "title_zh": "母亲与病儿",
        "target_chapter": 8,
        "theme": "01 生死",
        "style": "抒情",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": "Fīlius in cubiculō est. Fīlius nōn bene est. Māter ad fīlium venit. 'Fīlī, cūr nōn bene es?' Fīlius tacet. Māter fīlium videt. Māter aquam dat. Fīlius aquam bibit. Māter fīlium tenet. Māter fīlium amat. Fīlius mātrem amat."
    },
    "cap8_14": {
        "title_la": "Pater et fīlius in viā",
        "title_zh": "父与子在街上",
        "target_chapter": 8,
        "theme": "06 权力",
        "style": "白话",
        "genre": "C 历史与人物",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "对话体",
        "text": "Pater et fīlius in viā ambulant. Multī virī in viā sunt. Fīlius: 'Pater, cūr tot virī hīc sunt?' Pater: 'Rōma magna est. Multī virī in Rōmā sunt.' Fīlius: 'Ego quoque vir esse volō.' Pater rīdet. 'Tū puer es. Sed mox vir eris.' Fīlius laetus est."
    },
    "cap8_15": {
        "title_la": "Servus bonus",
        "title_zh": "好奴隶",
        "target_chapter": 8,
        "theme": "58 主人与奴隶",
        "style": "冷峻",
        "genre": "M 伦理与习俗",
        "character_type": "奴隶",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": "Servus in vīllā est. Dominus servum vocat. 'Venī!' Servus venit. Dominus: 'Aquam volō.' Servus aquam dat. Dominus bibit. 'Bonus servus es.' Servus tacet. Dominus: 'Cūr tacēs?' Servus: 'Servus sum. Servus tacet.' Dominus servum videt. Dominus tacet."
    },
    "cap8_16": {
        "title_la": "Puella in hortō",
        "title_zh": "花园里的女孩",
        "target_chapter": 8,
        "theme": "36 乡村",
        "style": "抒情",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第一人称",
        "text": "Ego puella sum. In hortō sum. Hortus magnus est. Multae rosae in hortō sunt. Ego rosās videō. Rosās amō. Ego aquam ad rosās portō. Rosae aquam amant. Ego in hortō laeta sum. Hortus meus est. Ego hortum amō."
    },
    "cap8_17": {
        "title_la": "Fīlius discit",
        "title_zh": "儿子学习",
        "target_chapter": 8,
        "theme": "28 教育",
        "style": "古典",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": "Fīlius in cubiculō est. Pater librum habet. Pater fīliō librum dat. 'Hic liber bonus est.' Fīlius librum capit. Fīlius librum legit. Fīlius multa discit. Pater fīlium videt. Pater: 'Tū discis. Hoc bonum est.' Fīlius laetus est. Pater laetus est."
    },
    "cap8_18": {
        "title_la": "Duae puellae",
        "title_zh": "两个女孩",
        "target_chapter": 8,
        "theme": "32 友谊",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "对话体",
        "text": "Duae puellae in hortō sunt. Ūna puella: 'Rōsam tibi dō.' Altera puella: 'Grātiās! Rōsa pulchra est.' Ūna: 'Amīca mea es?' Altera: 'Ita. Amīca tua sum.' Puellae rīdent. Puellae in hortō ambulant. Puellae laetae sunt. Hoc est amīcitia."
    },
}

def title_to_slug(title_la: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9āēīōūȳĀĒĪŌŪȲ\s]", "", title_la)
    return re.sub(r"_+", "_", slug.strip().replace(" ", "_"))

def find_next_number(target_dir: Path, cap_num: int) -> int:
    max_n = 0
    for f in target_dir.glob(f"Cap{cap_num}_*_*.md"):
        m = re.search(r"_(\d{3})\.md$", f.name)
        if m:
            n = int(m.group(1))
            if n > max_n: max_n = n
    return max_n + 1

def main():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    passed, failed = [], []

    for story_id, meta in STORIES.items():
        target_ch = meta["target_chapter"]
        latin_text = meta["text"].strip().replace("'", '"')
        title_la = meta["title_la"]

        print(f"\n--- {story_id}: {title_la} (target Cap.{target_ch}) ---")

        eval_r = evaluate(latin_text, story_id)
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])

        gap = (v2_level - target_ch) if v2_level else "N/A"
        ok = v2_level is not None and v2_level <= target_ch + 2

        print(f"  算法: v2_level={v2_level}, v2_rate={v2_rate}%, gap={gap}")

        if not ok:
            print(f"  [FAIL] 算法判到 Cap.{v2_level}")
            failed.append((story_id, v2_level, v2_oov))
            continue

        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)
        nnn = find_next_number(cap_dir, target_ch)
        slug = title_to_slug(title_la)
        filename = f"Cap{target_ch}_{slug}_brevis_{nnn:03d}.md"
        filepath = cap_dir / filename

        wc = len(re.findall(r"[A-Za-zāēīōūȳĀĒĪŌŪȲ]{2,}", latin_text))

        yaml = [
            "---",
            f'story_id: "{story_id}"',
            f'title_la: "{title_la}"',
            f'title_zh: "{meta["title_zh"]}"',
            f'target_chapter: {target_ch}',
            f'evaluated_chapter: {v2_level}',
            f'theme: "{meta["theme"]}"',
            f'style: "{meta["style"]}"',
            f'genre: "{meta["genre"]}"',
            f'character_type: "{meta["character_type"]}"',
            f'length_tier: "{meta["length_tier"]}"',
            f'narrative_mode: "{meta["narrative_mode"]}"',
            f'word_count: {wc}',
            f'macrons_status: "generated"',
            f'v2_rate: {v2_rate}',
            f'v2_oov: {json.dumps(v2_oov, ensure_ascii=False)}',
            f'created_at: "{now}"',
            f'updated_at: "{now}"',
            f'status: "active"',
            "---",
        ]
        filepath.write_text("\n".join(yaml) + "\n\n" + latin_text + "\n", encoding="utf-8")
        print(f"  [PASS] → {filename}")
        passed.append((story_id, filename, target_ch))

    # 汇总
    print(f"\n{'='*60}")
    print(f"结果: {len(passed)} 通过, {len(failed)} 失败")
    for sid, fn, ch in passed:
        print(f"  [OK] Cap.{ch}: {fn}")
    for sid, lvl, oov in failed:
        print(f"  [FAIL] {sid}: algo={lvl}")

    # 更新 progress.json
    chapter_counts = {}
    for cap_dir in sorted(REALITATES_DIR.glob("Cap*")):
        if cap_dir.is_dir():
            chapter_counts[cap_dir.name] = len(list(cap_dir.glob("*.md")))

    progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    for ch in ["5", "7", "8"]:
        cn = f"Cap{ch}"
        count = chapter_counts.get(cn, 0)
        if cn in progress["chapters"]:
            progress["chapters"][cn]["done"] = count
            progress["chapters"][cn]["need"] = max(0, progress["chapters"][cn]["target"] - count)
    progress["last_updated"] = now
    PROGRESS_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n当前状态:")
    for ch in ["5", "7", "8"]:
        cn = f"Cap{ch}"
        print(f"  Cap.{ch}: {chapter_counts.get(cn, 0)}/10")


if __name__ == "__main__":
    main()