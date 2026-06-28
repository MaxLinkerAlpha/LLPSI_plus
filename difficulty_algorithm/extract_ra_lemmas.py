#!/usr/bin/env python3
"""
从 RA PDF (拉丁语-英语词汇表) 提取可用的原形词条目。
pdftotext 输出了字面量八进制转义（如 \303\252），需要解码修复。
"""

import json
import re


def fix_octal_escapes(text: str) -> str:
    """将文本中字面量的八进制转义序列（\\NNN）转为真实字节，再按 UTF-8 解码。"""
    def replace_octal(m):
        octal_str = m.group(1)
        byte_val = int(octal_str, 8)
        return bytes([byte_val])

    # 匹配 \ 后跟 3 位八进制数字
    result = re.sub(rb'\\([0-7]{3})', replace_octal, text.encode('latin-1'))
    return result.decode('utf-8', errors='replace')


def extract_lemmas(text: str) -> list:
    """从 RA 词汇表文本中提取拉丁语原形词条目。"""
    lemmas = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 4:
            continue
        
        # 跳过明显的非词汇行
        skip_prefixes = ('LATIN-', 'VOCABULARY', 'PARS', 'INDICES', 'COLLOQVIA',
                         'GRAMMATICA', 'EXERCITIA', 'PLAVTVS', 'PETRONIVS',
                         'Domus', 'Focus', 'Skovvangen', 'P.O.Box', 'www.',
                         'ISBN', 'Copyright', 'HANS', 'LINGVA', 'PER SE',
                         'by Hans', 'MMI', 'DOMVS')
        if any(line.startswith(p) for p in skip_prefixes):
            continue
        
        # 取第一个空格前的部分作为原形词
        # 格式: "ab-dūcere (verb)" 或 "ā/ab/abs prp +abl  from, of"
        first_word = line.split()[0]
        
        # 清理：去除括号、逗号、右括号
        first_word = first_word.strip('.,;:()[]')
        
        # 有效条目: 至少2个字符，包含字母
        if len(first_word) >= 2 and re.search(r'[a-zA-Z\u00C0-\u024F]', first_word):
            lemmas.append(first_word)
    
    return lemmas


def main():
    # 读取 pdftotext 输出
    with open('/tmp/ra_raw.txt', 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()
    
    print(f"原始文本长度: {len(raw_text)} 字符")
    
    # 修复八进制转义
    fixed_text = fix_octal_escapes(raw_text)
    
    # 展示修复后的前 1000 字符
    print("\n=== 修复后前 1000 字符 ===")
    print(fixed_text[:1000])
    
    # 提取原形词
    lemmas = extract_lemmas(fixed_text)
    
    # 去重
    unique_lemmas = list(dict.fromkeys(lemmas))  # 保持顺序去重
    
    print(f"\n=== 统计 ===")
    print(f"提取词条（含重复）: {len(lemmas)}")
    print(f"唯一原形词: {len(unique_lemmas)}")
    print(f"示例前 30: {unique_lemmas[:30]}")
    print(f"示例后 20: {unique_lemmas[-20:]}")
    
    # 保存
    dst = "ra_lemmas.json"
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(unique_lemmas, f, ensure_ascii=False, indent=2)
    print(f"\n已保存 → {dst}")


if __name__ == '__main__':
    main()
