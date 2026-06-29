#!/usr/bin/env python3
"""
fill_gaps.py v1_0_0
直接写故事 + 算法验证 + 入库，确保每篇都通过算法检验。
缺口：Cap.5(-1), Cap.7(-4), Cap.8(-8)
"""

import json
import re
import sys
import os
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = PROJECT_ROOT / "difficulty_algorithm"
REALITATES_DIR = Path(__file__).resolve().parent / "realitates"
PROGRESS_FILE = Path(__file__).resolve().parent / "progress.json"

# 导入 evaluate 函数
_orig_cwd = os.getcwd()
os.chdir(str(EVAL_DIR))
sys.path.insert(0, str(EVAL_DIR))
from evaluate_v2 import evaluate
os.chdir(_orig_cwd)

# ============================================================
# 故事定义（手工编写，严格使用前几章词汇）
# ============================================================

STORIES = {
    # === Cap.5 缺 1 篇 ===
    "cap5_11": {
        "title_la": "Puer et avis",
        "title_zh": "男孩与鸟",
        "target_chapter": 5,
        "theme": "02 爱",
        "style": "抒情",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Puer in hortō sedet. Avis in hortō cantat. Puer avem audit. Avis parva est. Avis pulchra est. Puer avem spectat. Puer avem amat. Avis ad puerum volat. Puer manum tollit. Avis in manū puerī sedet. Puer laetus est. Avis cantat. Puer rīdet."""
    },
    # === Cap.7 缺 4 篇 ===
    "cap7_11": {
        "title_la": "Duo puerī in viā",
        "title_zh": "街上的两个男孩",
        "target_chapter": 7,
        "theme": "13 孤独",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "对话体",
        "text": """Duo puerī in viā sunt. Ūnus puer: "Quis es?" Alter puer: "Mārcus sum." Ūnus: "Ego Quīntus sum. Unde venīs?" Mārcus: "Ā Graeciā veniō." Quīntus: "Cūr in Rōmā es?" Mārcus: "Pater meus hīc labōrat. Tū Rōmānus es?" Quīntus: "Ita. Amīcus meus es?" Mārcus: "Ita." Puerī rīdent. Duo puerī in viā ambulant."""
    },
    "cap7_12": {
        "title_la": "Fīlia et rosae",
        "title_zh": "女孩与玫瑰",
        "target_chapter": 7,
        "theme": "18 自然",
        "style": "抒情",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Fīlia in hortō est. Multae rosae in hortō sunt. Fīlia rosās spectat. Rosae rubrae sunt. Rosae pulchrae sunt. Fīlia rosam carpit. Māter venit. "Cūr rosam carpis?" Fīlia: "Rosam tibi dare volō." Māter rīdet. Māter fīliam amat. Fīlia mātrem amat. Hoc est bonum."""
    },
    "cap7_13": {
        "title_la": "Pater dormit",
        "title_zh": "父亲睡了",
        "target_chapter": 7,
        "theme": "25 家庭",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Pater in lectō est. Pater dormit. Fīlius in ātriō est. Fīlius clāmat. Māter: "Tacē! Pater dormit." Fīlius tacet. Sed fīlius nōn laetus est. Māter: "Pater fessus est. Pater labōrat." Fīlius mātrem spectat. "Ego quoque labōrāre volō." Māter rīdet. "Tū parvus es. Sed mox magnus eris." Fīlius laetus est. Pater dormit."""
    },
    "cap7_14": {
        "title_la": "Servus et aqua",
        "title_zh": "奴隶与水",
        "target_chapter": 7,
        "theme": "03 自由与束缚",
        "style": "冷峻",
        "genre": "M 伦理与习俗",
        "character_type": "奴隶",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Servus ad fontem it. Aquam portat. Via longa est. Servus fessus est. Dominus in vīllā est. Dominus aquam exspectat. Servus venit. "Cūr tardus es?" Dominus īrātus est. Servus: "Via longa est." Dominus servum verberat. Servus tacet. Servus in terrā est. Dominus abit. Servus sōlus est. Sed servus nōn plōrat. Servus fortis est."""
    },
    # === Cap.8 缺 8 篇 ===
    "cap8_11": {
        "title_la": "Māter et puer aeger",
        "title_zh": "母亲与生病的孩子",
        "target_chapter": 8,
        "theme": "01 生死",
        "style": "抒情",
        "genre": "A LLPSI宇宙",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Puer in lectō est. Puer aeger est. Māter ad puerum venit. "Fīlī, doletne?" Puer: "Dolet, māter." Māter aquam dat. Puer aquam bibit. Māter manum puerī tenet. Nox est. Māter nōn dormit. Māne puer oculōs aperit. "Māter, nōn jam dolet." Māter lacrimat. Māter laeta est. Puer vīvit."""
    },
    "cap8_12": {
        "title_la": "Duo amīcī",
        "title_zh": "两个朋友",
        "target_chapter": 8,
        "theme": "32 友谊与孤独",
        "style": "白话",
        "genre": "M 伦理与习俗",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "对话体",
        "text": """Duo amīcī in forō sunt. Ūnus: "Dōnum tibi habeō." Alter: "Quid est?" Ūnus: "Liber est." Alter: "Grātiās! Ego quoque dōnum habeō." Ūnus: "Quid est?" Alter: "Imāgō parva." Amīcī rīdent. Ūnus: "Amīcus vērus es." Alter: "Et tū." Amīcī in tabernā sedent. Vinum bibunt. Hoc est amīcitia."""
    },
    "cap8_13": {
        "title_la": "Fūr in nocte",
        "title_zh": "夜贼",
        "target_chapter": 8,
        "theme": "04 正义",
        "style": "冷峻",
        "genre": "C 历史与人物",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": ('Nox est. Fūr in viā est. Fūr ad domum venit. Iānuam aperit. In domō nihil est. '
                 'Fūr in ātriō est. Subitō vir venit. "Quis es?" Fūr tacet. Vir: "Fūr es!" '
                 'Fūr fugit. Sed vir fūrem capit. "Cūr hoc facis?" Fūr: "Famem habeō. Nihil habeō." '
                 'Vir tacet. Vir pānem dat. Fūr: "Cūr mihi pānem dās?" Vir: "Quia tū homō es."')
    },
    "cap8_14": {
        "title_la": "Puella et lūna",
        "title_zh": "女孩与月亮",
        "target_chapter": 8,
        "theme": "23 睡眠",
        "style": "抒情",
        "genre": "B 神话与传说",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Puella in fenestrā stat. Lūnam spectat. Lūna magna est. Lūna pulchra est. Māter: "Dormī, fīlia." Puella: "Nōn possum. Lūna mē vocat." Māter: "Lūna nōn vocat. Lūna tacet." Puella: "Sed lūna in caelō sōla est. Nēmō cum lūnā est." Māter ad puellam venit. Māter puellam tenet. "Ego cum lūnā sum," dīcit māter. "Et ego cum tē sum." Puella dormit."""
    },
    "cap8_15": {
        "title_la": "Senex et forum",
        "title_zh": "老人与广场",
        "target_chapter": 8,
        "theme": "35 城市",
        "style": "白话",
        "genre": "C 历史与人物",
        "character_type": "老人",
        "length_tier": "短篇",
        "narrative_mode": "第一人称",
        "text": """Ego senex sum. In forō sedeō. Multōs annōs videō. Multī puerī in forō sunt. Puerī clāmant, rīdent, currunt. Ego puerōs spectō. Ūnus puer ad mē venit. "Senex, cūr sōlus sedēs?" "Nōn sōlus sum," respondē. "Forum meum est. Puerī meī sunt. Rōma mea est." Puer rīdet. Puer ad aliōs puerōs currit. Ego in forō sedeō. Forum plēnum est. Ego plēnus sum."""
    },
    "cap8_16": {
        "title_la": "Epistula ad patrem",
        "title_zh": "给父亲的信",
        "target_chapter": 8,
        "theme": "30 威严与慈爱",
        "style": "古典",
        "genre": "C 历史与人物",
        "character_type": "旅人",
        "length_tier": "短篇",
        "narrative_mode": "书信体",
        "text": """Pater, salūtem. Ā Graeciā scrībō. Mare magnum vīdī. Nāvis magna erat. Multōs diēs in marī fuimus. Nunc in terrā sum. Graecī bonī sunt. Cibum dant. Aquam dant. Sed tū nōn hīc es. Ego tē dēsīderō. Mox ad Rōmam redībō. Tū mē exspectā. Valē, pater. Fīlius tuus, Mārcus."""
    },
    "cap8_17": {
        "title_la": "Cibus et vinum",
        "title_zh": "食物与酒",
        "target_chapter": 8,
        "theme": "41 财富与贫困",
        "style": "白话",
        "genre": "M 伦理与习俗",
        "character_type": "罗马人",
        "length_tier": "短篇",
        "narrative_mode": "对话体",
        "text": ('Dīves in tabernā est. Dīves: "Cibum optimum volō! Vinum optimum volō!" '
                 'Servus cibum dat. Servus vinum dat. Dīves bibit. Pauper ad tabernam venit. '
                 '"Pānem habeō. Nihil aliud habeō." Dīves pauperem videt. "Cūr nōn intrat?" '
                 'Pauper: "Nōn habeō pecūniam." Dīves tacet. Dīves: "Hīc sede. Vinum bibe." '
                 'Pauper: "Cūr mihi dās?" Dīves: "Quia tū quoque homō es."')
    },
    "cap8_18": {
        "title_la": "Nauta et puer",
        "title_zh": "水手与男孩",
        "target_chapter": 8,
        "theme": "22 旅程",
        "style": "白话",
        "genre": "A LLPSI宇宙",
        "character_type": "旅人",
        "length_tier": "短篇",
        "narrative_mode": "第三人称",
        "text": """Nauta in portū est. Puer ad nautam venit. Puer: "Unde venīs?" Nauta: "Ā multīs terrīs veniō." Puer: "Quās terrās vīdistī?" Nauta: "Graeciam vīdī. Aegyptum vīdī. Britanniam vīdī." Puer: "Ego nihil vīdī." Nauta: "Tū parvus es. Sed mox magnus eris. Mox multās terrās vidēbis." Puer rīdet. Nauta nāvem ascendit. Puer in portū sōlus est. Sed nōn trīstis."""
    },
}

# ============================================================
# 验证 + 入库
# ============================================================

def find_next_number(target_dir: Path, cap_num: int) -> int:
    max_n = 0
    for f in target_dir.glob(f"Cap{cap_num}_*_*.md"):
        m = re.search(r"_(\d{3})\.md$", f.name)
        if m:
            n = int(m.group(1))
            if n > max_n:
                max_n = n
    return max_n + 1

def title_to_slug(title_la: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9āēīōūȳĀĒĪŌŪȲ\s]", "", title_la)
    slug = slug.strip().replace(" ", "_")
    slug = re.sub(r"_+", "_", slug)
    return slug

def main():
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    results = {"pass": [], "fail": []}

    for story_id, meta in STORIES.items():
        target_ch = meta["target_chapter"]
        title_la = meta["title_la"]
        latin_text = meta["text"].strip()

        print(f"\n--- {story_id}: {title_la} (target Cap.{target_ch}) ---")

        # 算法评估
        eval_r = evaluate(latin_text, story_id)
        v2_level = eval_r.get("v2_level") or eval_r.get("v2_best_fit")
        v2_rate = eval_r.get("v2_rate", 0)
        v2_oov = eval_r.get("v2_oov", [])

        gap = (v2_level - target_ch) if v2_level else "N/A"
        passed = v2_level is not None and v2_level <= target_ch + 2  # 允许 LIGHT 级别

        print(f"  算法: v2_level={v2_level}, v2_rate={v2_rate}%, gap={gap}, oov={v2_oov[:5]}")

        if not passed:
            print(f"  [FAIL] 算法判到 Cap.{v2_level}，超出目标 Cap.{target_ch}")
            results["fail"].append((story_id, v2_level, v2_oov))
            continue

        # 入库
        cap_dir = REALITATES_DIR / f"Cap{target_ch}"
        cap_dir.mkdir(parents=True, exist_ok=True)

        nnn = find_next_number(cap_dir, target_ch)
        slug = title_to_slug(title_la)
        filename = f"Cap{target_ch}_{slug}_brevis_{nnn:03d}.md"
        filepath = cap_dir / filename

        # 构建 YAML
        yaml_lines = [
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
            f'word_count: {len(re.findall(r"[A-Za-zāēīōūȳĀĒĪŌŪȲ]{2,}", latin_text))}',
            f'macrons_status: "generated"',
            f'v2_rate: {v2_rate}',
            f'v2_oov: {json.dumps(v2_oov, ensure_ascii=False)}',
            f'created_at: "{now}"',
            f'updated_at: "{now}"',
            f'status: "active"',
            "---",
        ]

        content = "\n".join(yaml_lines) + "\n\n" + latin_text + "\n"
        filepath.write_text(content, encoding="utf-8")
        print(f"  [PASS] → {filename}")

        results["pass"].append((story_id, filename, target_ch))

    # 汇总
    print(f"\n{'='*60}")
    print(f"结果: {len(results['pass'])} 通过, {len(results['fail'])} 失败")
    if results["pass"]:
        for sid, fn, ch in results["pass"]:
            print(f"  [OK] Cap.{ch}: {fn}")
    if results["fail"]:
        print(f"\n失败:")
        for sid, lvl, oov in results["fail"]:
            print(f"  [FAIL] {sid}: algo={lvl}, oov={oov[:10]}")

    # 更新 progress.json
    chapter_counts = defaultdict(int)
    for cap_dir in sorted(REALITATES_DIR.glob("Cap*")):
        if not cap_dir.is_dir():
            continue
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
        count = chapter_counts.get(cn, 0)
        print(f"  Cap.{ch}: {count}/10")


if __name__ == "__main__":
    main()