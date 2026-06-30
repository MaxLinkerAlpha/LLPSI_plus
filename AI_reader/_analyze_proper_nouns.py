#!/usr/bin/env python3
"""分析 form_chapter_map 中地名/人名/月份等封闭类词汇的章节分布"""
import json, sys, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'difficulty_algorithm'))

with open('form_chapter_map.json', encoding='utf-8') as f:
    form_ch = json.load(f)

# 一批明显是地名/人名的词
places = ['hispania', 'hispaniae', 'graecia', 'graeciae', 'aegyptus', 'aegypti', 
          'asia', 'asiae', 'arabia', 'arabiae',
          'italia', 'italiae', 'gallia', 'galliae', 'britannia', 'britanniae', 
          'sicilia', 'siciliae', 'creta', 'cretae',
          'cyprus', 'cypri', 'athenae', 'athenis', 'carthago', 
          'romanus', 'romani', 'romam', 'romae', 'roma',
          'tiberis', 'nilus', 'nili', 'oceanus', 'oceani', 
          'mare', 'maris', 'rubrum', 'rubri',
          'ianuarius', 'februarius', 'martius', 'aprilis', 'maius', 'iunius', 
          'iulius', 'augustus', 'september', 'october', 'november', 'december',
          'mercurius', 'iuppiter', 'iovis', 'iuno', 'iunonis', 'mars', 'martis', 
          'venus', 'veneris', 'apollo', 'diana', 'minerva', 'neptunus', 'pluto',
          'greece', 'greecia', 'aegypto', 'aegyptum', 'hispaniam', 'galli', 'gallos',
          'romanorum', 'athenarum', 'carthaginis', 'africa', 'africae', 'syrus', 'syria',
          'indus', 'indi', 'indos', 'seres', 'serum', 'phoenicia', 'phoenices',
          'hiberus', 'rhenus', 'danuvius', 'euphrates', 'tigris',
          'capitolium', 'palatium', 'forum', 'via', 'appia',
          'macedonia', 'macedoniae', 'epirus', 'epiri', 'thracia', 'thraciae',
          'alexander', 'caesar', 'pompeius', 'cicero', 'catilina', 'augustus',
          'medicus', 'medici', 'medicum']

print('=== 地名/人名/月份/文化专名词汇的章节分布 ===')
print('  (🔴 = Cap>15, 🟢 = Cap<=15, ⚪ = not found)')
print()
for w in places:
    ch = form_ch.get(w)
    if ch is not None:
        marker = '🔴' if ch > 15 else '🟢'
        print(f'  {marker} {w:25s} → Cap.{ch}')
    else:
        print(f'  ⚪ {w:25s} → NOT FOUND')

# 统计：Cap>15 的专名词根
print()
print('=== Cap>15 专名词根清单（去变位） ===')
high_pn = {}
for w, ch in form_ch.items():
    if ch > 15 and ch <= 56:
        # 判断是不是专有名词（大写开头、或是已知的封闭类）
        known_pn_stems = [
            'hispani', 'graec', 'aegypt', 'asi', 'arabi', 
            'itali', 'gall', 'britanni', 'sicili', 'cret', 'cypr', 'athen', 'carthag',
            'roman', 'roma', 'tiber', 'nil', 'ocean', 'rubr',
            'mercuri', 'iuppiter', 'iov', 'iunon', 'iuno', 'mart', 'ven', 'apoll', 'dian', 
            'minerv', 'neptun', 'pluton', 'cerer', 'bacch', 'vulcan',
            'ianuari', 'februari', 'marti', 'aprili', 'mai', 'iuni', 'iuli', 'august',
            'septemb', 'octob', 'novemb', 'decemb',
            'afric', 'syr', 'ind', 'ser', 'phoenic',
            'hiber', 'rhen', 'danuvi', 'euphrat', 'tigr',
            'capitoli', 'palati', 'appi',
            'macedoni', 'epir', 'thraci',
            'alexand', 'caesar', 'pompei', 'ciceron', 'catilin',
            'medic', 'philosoph', 'stoic', 'epicur',
        ]
        is_pn = False
        for stem in known_pn_stems:
            if w.startswith(stem):
                is_pn = True
                break
        if is_pn:
            print(f'  {w:25s} → Cap.{ch}')

print()
print(f'完成分析')
