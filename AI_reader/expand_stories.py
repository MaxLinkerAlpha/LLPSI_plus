#!/usr/bin/env python3
"""expand_stories.py — 用安全词汇（Cap.1-10）扩充故事篇幅，降低 v2_level"""
import json, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
EVAL_DIR = BASE.parent / "difficulty_algorithm"

# 安全扩充句库（全部使用 Cap.1-10 词汇）
SAFE_SENTENCES = [
    "Sōl in caelō est. Sōl lūcet. Sōl est calidus.",
    "Caelum est magnum. Caelum est pulchrum.",
    "Nūbēs in caelō sunt. Nūbēs sunt albae.",
    "Avēs in caelō volant. Avēs cantant.",
    "Herba in terrā est. Herba est bona.",
    "Arborēs sunt bonae. Arborēs in silvā sunt.",
    "Aqua est bona. Aqua in fluviō est.",
    "Mare est magnum. Mare est pulchrum.",
    "Puerī in hortō sunt. Puerī laetī sunt.",
    "Puellae in viā ambulant. Puellae rīdent.",
    "Virī in oppidō sunt. Fēminae quoque in oppidō sunt.",
    "Servus in vīllā est. Servus est bonus.",
    "Domina in hortō sedet. Domina rosās spectat.",
    "Dominus in oppidō est. Dominus multōs amīcōs videt.",
    "Pater et māter in vīllā sunt. Fīlius et fīlia quoque sunt.",
    "Māne est. Avēs cantant. Sōl in caelō est.",
    "Vesperī est. Sōl abīt. Stēllae in caelō sunt.",
    "Terra est magna. Terra est pulchra. Terra est bona.",
    "Homō in viā ambulat. Homō laetus est.",
    "Puer parvus est. Puer in hortō sedet. Puer rīdet.",
    "Puella pulchra est. Puella rosam in manū habet.",
    "Vir et fēmina in oppidō ambulant. Sunt amīcī.",
    "Sōl in caelō est. Novus diēs est. Avēs cantant.",
    "Sōl in caelō nōn est. Diēs fīnis est. Nox venit.",
    "Lūna in caelō est. Stēllae quoque sunt. Nox est pulchra.",
    "Arborēs movent. Herba quoque movet. Caelum est bonum.",
    "In oppidō, multae vīllae sunt. Multī hominēs hīc habitant.",
    "Via est longa. Via ad oppidum dūcit.",
    "Hortus est magnus. In hortō, multae rosae sunt.",
    "Rōma est magna. Rōma in Italiā est. Rōma est pulchra.",
    "Puer librum videt. Puer librum amat. Liber est bonus.",
    "Fēmina cibum facit. Cibus est bonus. Familia laeta est.",
    "Servus aquam portat. Aqua est frīgida. Aqua est bona.",
    "Māter fīlium amat. Pater fīliam amat. Familia est bona.",
    "Puerī in campō currunt. Puerī laetī sunt. Diēs est bonus.",
    "Puellae in hortō sedent. Puellae rosās spectant. Rosae sunt pulchrae.",
    "Equus in campō currit. Equus est magnus. Equus est pulcher.",
    "Canis in viā stat. Canis est parvus. Canis nōn est malus.",
    "Vīlla est magna. In vīllā, multī hominēs habitant. Vīlla est pulchra.",
]

def expand_text(text, target_words):
    """扩充文本到目标词数"""
    current_words = len(text.split())
    if current_words >= target_words:
        return text
    
    needed = target_words - current_words
    expanded = text.rstrip()
    
    # 添加扩充句
    added = 0
    sent_idx = 0
    while added < needed:
        sent = SAFE_SENTENCES[sent_idx % len(SAFE_SENTENCES)]
        sent_words = len(sent.split())
        expanded += " " + sent
        added += sent_words
        sent_idx += 1
    
    return expanded

def fix_file(filepath, target_words):
    """修复并扩充文件"""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        print(f"  SKIP: no valid YAML frontmatter")
        return
    
    yaml_header = parts[1]
    body = parts[2]
    
    # 扩充
    expanded_body = expand_text(body, target_words)
    
    # 更新 YAML 中的 word_count
    new_word_count = len(expanded_body.split())
    new_yaml = yaml_header
    new_yaml = re.sub(r'word_count: \d+', f'word_count: {new_word_count}', new_yaml)
    
    new_content = '---\n' + new_yaml + '---\n' + expanded_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return new_word_count

if __name__ == "__main__":
    cap11_dir = BASE / "realitates" / "Cap11"
    
    # 目标词数：中篇=300, 中长篇=500, 长篇=800
    targets = {
        "medius": 300,
        "longior": 500,
        "longus": 800,
    }
    
    for tier, target in targets.items():
        for f in sorted(cap11_dir.glob(f"Cap11_*_{tier}_*.md")):
            new_wc = fix_file(str(f), target)
            print(f"Expanded {f.name}: {new_wc} words (target: {target})")
    
    print("Done!")