#!/usr/bin/env python3
"""Check specific lemmas in lemma_chapter_map.json."""
import json

with open('../difficulty_algorithm/lemma_chapter_map.json') as f:
    lcm = json.load(f)

checks = [
    'os', 'oro', 'sum', 'er', 'erus', 'habito', 'habitus', 'hama', 'amo',
    'vito', 'vita', 'tune', 'equa', 'equus', 'iulus', 'Iulius',
    'Gaius', 'Titus', 'Aemilius', 'Syrus', 'Iulia',
    'laboro', 'curo', 'cura', 'narro', 'debeo', 'nolo',
    'possum', 'volo', 'ludo', 'rideo', 'dico', 'respondeo',
    'habeo', 'teneo', 'servo', 'capio', 'facio', 'ago',
    'spes', 'spero', 'vesper', 'maneo', 'nox', 'dies',
    'luna', 'stella', 'sol', 'caelum', 'lux', 'luceo',
    'corpus', 'toga', 'via', 'fluvius',
    'mercator', 'puer', 'vir', 'femina',
    'frater', 'soror', 'pater', 'mater', 'filius', 'filia',
    'dominus', 'servus', 'amicus', 'inimicus',
    'calidus', 'calidior', 'frigidus', 'frigidior',
    'albus', 'albior', 'niger', 'pulcher', 'bonus', 'malus',
    'magnus', 'parvus', 'multus', 'pauci',
    'hodie', 'mecum', 'tecum', 'tibi', 'mihi',
    'semper', 'numquam', 'saepe',
    'nihil', 'aliquid', 'aliquis', 'omnis',
    'ita', 'sic', 'fortasse', 'aliquando', 'gratia',
    'labor', 'somnus', 'dormio', 'dormiendus',
    'narro', 'faber', 'aedifico', 'invenio',
    'placeo', 'queror', 'gaudium', 'dignitas', 'tracto', 'tractum', 'ambo',
    'tendo', 'ambulo', 'curro', 'sto', 'sedeo',
    'clamo', 'lacrimo', 'canto', 'doceo',
    'quaero', 'porto', 'fero', 'duco',
    'paro', 'rogo', 'scribo',
    'lego', 'audio', 'video', 'specto',
    'bibo', 'edo', 'sumo', 'cibus', 'cena',
    'intro', 'exeo', 'venio', 'abeo', 'redeo',
    'iudico', 'iustus', 'testis', 'accuso', 'fur',
    'amitto', 'fallo', 'mentior', 'falsum',
    'navis', 'navus', 'litus', 'mare', 'insula',
    'vinum', 'oleum', 'aqua', 'terra',
    'hortus', 'villa', 'domus', 'forum', 'tectum',
    'donum', 'pauper', 'pauperior', 'amor', 'dea',
    'currus', 'canis', 'avis',
    'sicut', 'videsne',
    'aliter', 'locutus', 'quies', 'quiesco',
    'culina', 'cado', 'vivo', 'vivus', 'aveo',
    'revenio', 'obscurus', 'affor',
    'vel', 'tunc', 'uterque', 'clamatus',
    'scio', 'circumsto', 'mereo', 'piscor', 'piscator',
    'veritus', 'verus', 'dolor', 'frango',
    'impleo', 'causa', 'facilior',
    'tardior', 'tardus', 'stultior', 'stultus',
    'natus', 'attentus', 'sero',
    'Claudius', 'Claudia',
    'talis', 'intellego', 'idem',
    'loco', 'locus', 'si', 'cras',
    'argenteus', 'luceo', 'transeo',
    'adiuvo',
]

for word in sorted(set(checks)):
    if word in lcm:
        print(f'{word:20s} -> Cap.{lcm[word]}')
    else:
        print(f'{word:20s} -> NOT FOUND')