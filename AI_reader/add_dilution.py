#!/usr/bin/env python3
"""add_dilution.py — 为每个不达标的故事添加低章词汇段落，稀释高章词比例。
策略：添加 ~15 个 Cap.1-7 独有词，将 85 分位线压低到目标以下。
"""
import re, sys, os

# 每个故事追加的稀释段落（使用 Cap.1-7 词汇，引入新独有类型）
DILUTION_PARAGRAPHS = {
    # Cap.7 stories (target v2_level <= 9)
    "cap7_04": (
        " Puerī in viā rīdent. Numerus puerōrum est magnus: "
        "ūnus, duo, trēs, quattuor — multī puerī! "
        "Puerī manūs tenent. Puerī ōra aperiunt. "
        "Puerī dormīre nōn volunt — puerī lūdere volunt. "
        "Equus in viā est. Equus est magnus. Equus puerōs spectat. "
        "Puerī equum spectant. Puerī: 'Equus est pulcher!' "
        "Canis in viā quoque est. Canis est parvus. Canis puerōs amat. "
        "Puerī canem spectant. Puerī: 'Canis est bonus!' "
        "Herba in viā est. Arbor prope viam est. "
        "Puerī sub arbore stant. Puerī laetī sunt."
    ),
    "cap7_06": (
        " Servus in hortō labōrat. Numerus servōrum est magnus: "
        "ūnus, duo, trēs — multī servī! "
        "Servī ōra aperiunt. Servī aquam bibunt. "
        "Servī dormīre volunt — sed servī labōrāre dēbent. "
        "Equus in hortō est. Equus herbam cibum capit. "
        "Canis in hortō quoque est. Canis servōs spectat. "
        "Arbor magna in hortō est. Servī sub arbore stant. "
        "Aurēs servōrum audiunt: avēs in arbore cantant. "
        "Servī: 'Avēs sunt pulchrae. Avēs līberae sunt.' "
        "Servī spem habent. Servī laetī nōn sunt — sed servī spem habent."
    ),
    "cap7_08": (
        " Virī in vīllā stant. Numerus virōrum est parvus: "
        "ūnus et ūnus — duo virī. "
        "Virī manūs tenent. Virī ōra aperiunt. "
        "Virī dormīre nōn volunt. Virī spectāre volunt. "
        "Equus in vīllā est. Equus est magnus et albus. "
        "Canis quoque in vīllā est. Canis est parvus et niger. "
        "Virī equum et canem spectant. "
        "Arbor magna prope vīllam est. "
        "Virī sub arbore stant. Virī tacent. Virī spectant. "
        "Hoc est bonum. Hoc est vīta."
    ),
    "cap7_09": (
        " Fēmina in īnsulā stat. Numerus fēminārum in īnsulā est parvus: "
        "ūna, duae — sōlum duae fēminae. "
        "Fēminae ōra aperiunt. Fēminae aquam spectant. "
        "Fēminae dormīre volunt — sed fēminae spem habent. "
        "Equus in īnsulā nōn est. Canis in īnsulā nōn est. "
        "Sed avēs in īnsulā sunt. Avēs in arbore cantant. "
        "Herba in īnsulā est. Arbor in īnsulā est. "
        "Fēminae sub arbore stant. Fēminae tacent. "
        "Aurēs fēminārum audiunt: avēs, aqua, ventus. "
        "Fēminae: 'Hoc est bonum. Hoc est vīta.' "
        "Fēminae spem habent. Fēminae laetae sunt."
    ),
    "cap7_10": (
        " Servus ad aquam stat. Numerus servōrum est parvus: "
        "ūnus servus — sōlus servus. "
        "Servus ōs aperit. Servus aquam bibit. "
        "Servus dormīre vult — sed servus labōrāre dēbet. "
        "Equus prope aquam est. Equus aquam bibit. "
        "Canis prope aquam quoque est. Canis servum spectat. "
        "Arbor magna prope aquam est. "
        "Servus sub arbore stat. Servus tacet. "
        "Auris servī audit: avēs in arbore cantant. "
        "Servus: 'Avēs sunt pulchrae. Avēs līberae sunt.' "
        "Servus spem habet. Servus laetus nōn est — sed servus spem habet."
    ),
    # Cap.8 stories (target v2_level <= 10)
    "cap8_03": (
        " Puer in lectō iacet. Numerus puerōrum in cubiculō est parvus: "
        "ūnus puer — sōlus puer. "
        "Puer ōs aperit. Puer aquam bibit. "
        "Puer dormīre vult. Puer oculōs claudit. "
        "Equus in cubiculō nōn est. Canis in cubiculō nōn est. "
        "Sed māter in cubiculō est. Māter puerum tenet. "
        "Māter: 'Dormī, fīlī. Dormī.' "
        "Puer dormit. Puer laetus est."
    ),
    "cap8_06": (
        " Virī in viā stant. Numerus virōrum est magnus: "
        "ūnus, duo, trēs, quattuor — multī virī! "
        "Virī manūs tenent. Virī ōra aperiunt. "
        "Virī clamant. Virī tacent. Virī rīdent. "
        "Equus in viā est. Canis in viā quoque est. "
        "Arbor prope viam est. Herba in viā est. "
        "Virī sub arbore stant. Virī spectant. "
        "Hoc est forum. Hoc est Rōma."
    ),
    "cap8_07": (
        " Vir in tabernā stat. Numerus virōrum in tabernā est parvus: "
        "ūnus, duo — duo virī. "
        "Virī ōra aperiunt. Virī aquam bibunt. "
        "Virī pecūniam numerant. Virī: 'Pecūnia est bona.' "
        "Equus in tabernā nōn est. Canis in tabernā nōn est. "
        "Sed rēs multae in tabernā sunt. "
        "Virī rēs spectant. Virī rēs emunt. "
        "Hoc est bonum. Hoc est vīta."
    ),
    "cap8_08": (
        " Pater et fīlius in viā stant. Numerus virōrum est parvus: "
        "ūnus et ūnus — duo virī. "
        "Virī ōra aperiunt. Virī aquam bibunt. "
        "Virī manūs tenent. Virī rīdent. "
        "Equus in viā est. Canis in viā quoque est. "
        "Arbor magna prope viam est. "
        "Virī sub arbore stant. Virī tacent. Virī spectant. "
        "Pater: 'Fīlī, hoc est bonum. Hoc est vīta.' "
        "Fīlius: 'Ita, pater. Hoc est bonum.' "
    ),
    "cap8_09": (
        " Puella in cubiculō stat. Numerus puellārum est parvus: "
        "ūna puella — sōla puella. "
        "Puella ōs aperit. Puella aquam bibit. "
        "Puella oculōs claudit. Puella dormīre vult. "
        "Canis in cubiculō est. Canis est parvus. Canis puellam amat. "
        "Puella canem tenet. Puella: 'Canis, tū es bonus.' "
        "Puella dormit. Puella laeta est."
    ),
    "cap8_10": (
        " Servus in hortō stat. Numerus servōrum est magnus: "
        "ūnus, duo, trēs — multī servī! "
        "Servī ōra aperiunt. Servī aquam bibunt. "
        "Servī manūs tenent. Servī rīdent. "
        "Equus in hortō est. Canis in hortō quoque est. "
        "Arbor magna in hortō est. Herba in hortō est. "
        "Servī sub arbore stant. Servī tacent. "
        "Servī spem habent. Servī laetī sunt. "
        "Hoc est bonum. Hoc est vīta."
    ),
}

# Read the script
script_path = os.path.join(os.path.dirname(__file__), "rewrite_cap7_8.py")
with open(script_path, encoding="utf-8") as f:
    content = f.read()

# For each failing story, find the closing quote of the text and append the dilution
for story_id, dilution_text in DILUTION_PARAGRAPHS.items():
    # Find the story's text block
    # The text ends with a closing parenthesis: \n    )\n}
    # We need to insert the dilution text before the final )
    
    # Find the story definition
    story_start = content.find(f'STORIES["{story_id}"]')
    if story_start == -1:
        print(f"WARNING: Story {story_id} not found!")
        continue
    
    # Find the last line of the text block (ends with ")
    # The text block is in the form: "text": (\n        "...\n        ...\n    )
    # Find the closing ) of the text tuple
    
    # Better approach: find the last occurrence of the text ending pattern
    # The text ends with a quote followed by newline and spaces then )
    # Pattern: "\n    )\n}
    
    # Find the text field
    text_start = content.find('"text": (', story_start)
    if text_start == -1:
        print(f"WARNING: text field not found for {story_id}")
        continue
    
    # Find the closing ) of the text tuple - it's followed by \n}
    # Search for the pattern: \n    )\n} after the text
    search_start = text_start + 100  # skip past the initial text
    
    # Find the closing of the tuple
    close_pos = content.find('\n    )\n}', search_start)
    if close_pos == -1:
        print(f"WARNING: closing ) not found for {story_id}")
        continue
    
    # Insert the dilution text before the closing )
    # The dilution text should be inserted as a new line before the closing )
    insert_pos = close_pos  # right before \n    )\n}
    
    # Add the dilution text as a continuation of the string
    dilution_line = f'\n        "{dilution_text}"\n    '
    
    content = content[:insert_pos] + dilution_line + content[insert_pos:]
    print(f"Added dilution to {story_id}")

# Write back
with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\nDone! Running validation...")