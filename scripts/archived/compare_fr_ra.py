#!/usr/bin/env python3
"""FR 多版本完整文本提取对比"""
import pypdf
import os

versions = [
    'LLPSI_core_familia_romana.pdf',
    'LLPSI_core_familia_romana_hd_2nd_color_text_selectable.pdf',
    'LLPSI_core_familia_romana_hd_color_small.pdf',
    'LLPSI_core_familia_romana_v1_scan.pdf',
]

for v in versions:
    path = f'/Users/max/Downloads/Projects/LLPSI+++/source/{v}'
    if not os.path.exists(path):
        continue
    r = pypdf.PdfReader(path)
    print(f'\n=== {v} ===')
    print(f'总页数: {len(r.pages)}')
    text_p11 = r.pages[10].extract_text() or '' if len(r.pages) > 10 else ''
    text_p51 = r.pages[50].extract_text() or '' if len(r.pages) > 50 else ''
    print(f'  p.11 字符数: {len(text_p11)}')
    print(f'  p.51 字符数: {len(text_p51)}')
    total_chars = 0
    pages_with_text = 0
    for p in r.pages:
        t = p.extract_text() or ''
        if t.strip():
            pages_with_text += 1
        total_chars += len(t)
    print(f'  全文可提取字符: {total_chars:,}')
    print(f'  含文本的页数: {pages_with_text}/{len(r.pages)}')
    # 检测长音符号
    full_text = ''.join((p.extract_text() or '') for p in r.pages[:30])
    has_macrons = any(c in full_text for c in 'āēīōūȳ')
    print(f'  前30页含长音符号: {has_macrons}')

# 同样对比 RA 多版本
print('\n' + '='*80)
print('Roma Aeterna 多版本对比')
print('='*80)
ra_versions = [
    'LLPSI_core_roma_aeterna.pdf',
    'LLPSI_core_roma_aeterna_hd_2nd_color.pdf',
    'LLPSI_core_roma_aeterna_hd_2nd_color_alt.pdf',
    'LLPSI_core_roma_aeterna_v1_scan.pdf',
    'LLPSI_core_roma_aeterna_v1_bw.pdf',
]

for v in ra_versions:
    path = f'/Users/max/Downloads/Projects/LLPSI+++/source/{v}'
    if not os.path.exists(path):
        continue
    r = pypdf.PdfReader(path)
    print(f'\n=== {v} ===')
    print(f'总页数: {len(r.pages)}')
    total_chars = 0
    pages_with_text = 0
    for p in r.pages:
        t = p.extract_text() or ''
        if t.strip():
            pages_with_text += 1
        total_chars += len(t)
    print(f'  全文可提取字符: {total_chars:,}')
    print(f'  含文本的页数: {pages_with_text}/{len(r.pages)}')
    # 检测长音符号
    full_text = ''.join((p.extract_text() or '') for p in r.pages[:30])
    has_macrons = any(c in full_text for c in 'āēīōūȳ')
    print(f'  前30页含长音符号: {has_macrons}')
