#!/usr/bin/env python3
"""
LLPSI OCR & 词表 综合清洗脚本
Phase 1: 清洗 capX_vocab_clean.json
Phase 2: 清洗 OCR 正文文件
Phase 3: 重新生成派生文件
"""

import json
import re
import os
from pathlib import Path
from collections import Counter, OrderedDict

BASE = Path("/Users/max/Downloads/Projects/LLPSI_plus")
VOCAB_DIR = BASE / "difficulty_algorithm" / "vocab_by_chapter"
OCR_DIR = BASE / "OCR"
PLAN_FILE = BASE / "CLEAN_TASK_PLAN.md"

# ─── 拉丁字符集（含长音） ───
LATIN_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZāēīōūȳĀĒĪŌŪȲ")
LATIN_LOWER = set("abcdefghijklmnopqrstuvwxyzāēīōūȳ")

# ─── 罗马数字 ───
ROMAN_NUMERALS = {
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
    "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx",
    "l", "c", "d", "m",
}

# ─── 已知拉丁语法术语（必须保留） ───
GRAMMAR_TERMS = {
    "ablativus", "accusativus", "singularis", "pluralis", "nominativus",
    "genetivus", "dativus", "vocativus", "masculinus", "femininus", "neutrum",
    "indicativus", "imperativus", "coniunctivus", "infinitivus", "participium",
    "gerundium", "gerundivum", "supinum", "activum", "passivum", "deponens",
    "comparativus", "superlativus", "indeclinabilis", "declinatio",
    "praepositio", "pronomen", "adiectivum", "substantivum", "verbum",
    "coniugatio", "persona", "numerus", "genus", "casus", "tempus", "modus",
    "exemplum", "exempla", "regula", "pensum", "pensa", "grammatica",
    "vocabulum", "vocabula", "capitulum", "syllaba", "littera",
    "participium", "infinitus", "passivum", "activum",
    # 序数词（章节标题用）
    "primum", "secundum", "tertium", "quartum", "quintum",
    "sextum", "septimum", "octavum", "nonum", "decimum",
    "undecimum", "duodecimum", "tertiumdecimum", "quartumdecimum",
    "quintumdecimum", "sextumdecimum", "septimumdecimum",
    "duodevicesimum", "undevicesimum", "vicesimum",
    # 变格相关
    "nominativus", "genetivus", "dativus", "accusativus", "vocativus", "ablativus",
    "singularis", "pluralis",
}

# ─── 已知截断词根（非完整词形，必须删除） ───
TRUNCATED_ROOTS = {
    # 常见形容词词根
    "magn", "parv", "mult", "pauc", "bon", "mal", "nov", "alt",
    "long", "brev", "lat", "pulchr", "foed", "calid", "frigid",
    "grav", "lev", "crass", "tenu", "facil", "difficil",
    "aegr", "laet", "irat", "fess", "pulcher", "niger", "ruber",
    "celer", "acer", "fort", "omn", "tot", "null",
    # 名词词根
    "insul", "oppid", "fluv", "fluvi", "domin", "puell", "femin",
    "serv", "ancill", "numer", "vocabul", "litter", "capitul",
    "puer", "vir", "homin", "corpor", "anim", "besti",
    "arbor", "hort", "mont", "mar", "terr", "aqu",
    "cael", "vent", "nub", "ign", "umbr", "silv",
    "ros", "lun", "sol", "stell", "mund",
    "pastor", "mercator", "pisc", "can", "equ", "leon",
    "ov", "porc", "gall", "pull",
    "ocul", "aur", "nas", "dent", "man", "ped", "cap",
    "brach", "crur", "cor", "lingu", "capill",
    "tabern", "mens", "sell", "lect", "ianu", "fenestr",
    "vill", "urb", "vi", "port", "mur", "templ",
    "anim", "corpor", "nom", "vest",
    # 动词词根
    "am", "hab", "vid", "aud", "dic", "duc", "fac",
    "ven", "pon", "ten", "mov", "ag", "ger", "fer",
    "curr", "scrib", "leg", "viv", "dorm", "spir",
    "ambul", "nat", "vol", "clam", "cant", "rid",
    "plor", "lud", "pugn", "labor", "port",
    "voc", "interrog", "respond", "exspect",
    "spect", "tang", "iung", "vert", "mitt",
    "capi", "accipi", "fugi", "iac",
    # 其他碎片
    "insu", "lae", "iae", "liae", "nia", "sium", "tium",
    "lium", "bris", "bus", "cis", "cus", "dus", "gus",
    "lis", "lus", "mus", "nus", "pus", "ris", "rus",
    "sus", "tus", "vus", "xus",
    "brun", "brundi", "del", "grae", "ger", "tuscu",
    "rom", "aemi", "iuli", "medi", "davi", "syr",
    "dav", "mar", "marc", "quint", "servi",
    "ancil", "accu", "decl", "genet", "nominat",
    "imper", "compar", "superl", "indic",
    "infinit", "particip", "praeposit",
    "tibe", "pad", "ost", "flum", "riv",
    "sept", "oct", "nov", "dec", "ian", "febr",
    "apr", "mai", "iun", "iul", "aug",
    "kal", "non", "id",
    "fem", "masc", "neutr", "sing", "plur",
    "nom", "gen", "dat", "acc", "abl", "voc",
    "imp", "ind", "inf", "pass", "act",
    "pers", "praes", "imperf", "perf", "plusq", "fut",
    "mon", "reg", "capi", "audi",
    "sacc", "saccu", "peristyl", "impluv", "cubicu",
    "ost", "osti", "tabern", "fenestr",
    "mar", "mer", "ocean", "atlant",
    "lect", "sell", "mens", "ianu",
    "ros", "lili", "viol",
    "gemm", "margarit", "ornament",
    "pecun", "numm", "preti",
    "vestiment", "tunic", "tog", "calce",
    "cib", "pan", "vin", "aqu", "lac",
    "pir", "mal", "pom",
    "exercit", "milit", "castr", "bell",
    "provinc", "imperi", "reg",
    "urb", "oppid", "vic",
    "templ", "sacerdot", "de",
    "poet", "carm", "vers",
    "ann", "mens", "di", "hor",
    "noct", "vesper", "mane",
    "aest", "hiem", "autumn", "ver",
    "somn", "mort",
    "pat", "matr", "fratr", "soror",
    "fili", "liber", "marit", "uxor",
    "amic", "inimic", "host",
    "discipul", "magistr",
    "Rom", "Roman", "Graec", "German", "Gall",
    "Hispan", "Aegypt", "Syri", "Arabi",
    "Britann", "Ital", "Sicil", "Sard",
    "Cors", "Cret", "Rhod", "Del",
    "Spart", "Athen", "Corinth",
    "Theb", "Troi", "Carthag",
    "Brundis", "Tuscul", "Osti",
    "Pompe", "Capu", "Neapol",
    "Pad", "Rhen", "Danuv", "Nil", "Tiber",
    "Tiber", "Rhen", "Danuvi", "Nil",
    "Aemili", "Iuli", "Corneli", "Semproni",
    "Claudi", "Valeri", "Fab",
    "ceter", "reliqu", "al",
    "ips", "idem", "e", "eo", "ei",
    "ill", "ist", "hic", "haec",
    "qu", "cu", "aliqu", "quidam",
    "tam", "tam", "adeo", "ita",
    "caus", "grat", "fin",
    "temp", "loc", "mod",
    "soci", "comit", "greg",
    "pler", "plerum", "nonnull",
    "uter", "utr", "neut",
    "alter", "sol", "un",
    "du", "tri", "quadr", "quinqu",
    "sex", "sept", "oct", "novem", "decem",
    "cent", "mill",
    "plur", "complur",
    "pro", "prae", "sub", "super", "inter",
    "circum", "ante", "post", "trans", "per",
    "ad", "in", "ex", "de", "ab", "cum", "sine",
    "ob", "propter", "contra", "apud", "extra", "intra",
    "supra", "infra", "ultra", "citra", "circa",
    "erga", "penes", "secundum", "praeter",
    "ve", "aut", "vel", "sive", "seu",
    "nam", "enim", "etenim", "quod", "quia", "quoniam",
    "quando", "si", "nisi", "etsi", "etiamsi", "tametsi",
    "ut", "ne", "quo", "quominus", "quin",
    "cum", "dum", "donec", "antequam", "priusquam", "postquam",
    "ubi", "simul", "simulatque",
    "quamvis", "quamquam", "licet",
    "quasi", "tamquam", "velut", "ceu",
    "itaque", "igitur", "ergo", "ideo", "idcirco", "propterea",
}

# 粘合词检测用算法处理，不需要手动列表

# ─── 已知乱码/噪音 ───
KNOWN_GIBBERISH = {
    "ztz", "mumy", "ssst", "uhuhu", "cucucurru", "cucurru",
    "hahae", "hahahae", "tuxtax", "baba", "baubau",
    "hhhhhhhh", "xxx", "xxix", "xxvi", "xxl", "ccc",
    "uhu", "lalla", "mammoa", "ealilla",
    "a——d", "b'be", "c\"c", "d)es", "h'ha",
    "xunt", "xvs", "xii", "xiii", "xiiilia", "xicaput",
    "xii exempla", "xv tem", "xvsextus",
    "qw", "qm", "wm", "wf", "sx", "rr", "bw", "ca", "cc",
    "mumy", "ztz", "ssst",
}

# ─── 已知OCR拼写错误（明显变形，不是任何拉丁词的正确拼写） ───
KNOWN_OCR_ERRORS = {
    # 语法术语的OCR错误变形
    "accusdtious", "accusatitous", "genetious",
    "nominatious", "vocatious", "imperatious",
    "nominatmvus", "plurialis", "plvincia",
    "infecrum",
    # 变性/变格表的OCR碎片
    "ovjes", "ovles", "vocles", "voclum",
    "brevle", "corporle", "pastorle", "pastorlem",
    "pedle", "voclem", "voclis",
    "diclere", "vigilazs", "altjo",
    "iectivum", "humiani",
    "declinatcanis",
    # 人名/地名的OCR错误
    "lulia", "lulium", "lulius", "tulia", "tuliam", "tulius",
    "ialius", "ial", "iulir", "iulit", "iuliz",
    "lean", "leandr", "laucius",
    "ttusculo", "tuscul",  # 但 "tus" 可能太短，不单独加入
    "tiulia", "tiulio",
    "brundisiz", "brundisiumnon",
    "sumxit",  # sumpsit 的OCR错误
}


# ═══════════════════════════════════════════════════════════
# Step 0: 构建拉丁词参考词典
# ═══════════════════════════════════════════════════════════

def extract_words_from_ocr():
    """从所有OCR文本文件中提取单词，构建参考词典"""
    word_counter = Counter()
    ocr_files = list(OCR_DIR.rglob("*.txt"))
    print(f"  扫描 {len(ocr_files)} 个OCR文本文件...")
    
    for fpath in ocr_files:
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
            # 清洗：移除行号标记 [1] [2] 等
            text = re.sub(r'\[\d+\]', ' ', text)
            # 提取单词（只保留拉丁字符+长音）
            words = re.findall(r'[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+', text)
            for w in words:
                if len(w) >= 2:
                    word_counter[w.lower()] += 1
        except Exception as e:
            print(f"    警告: {fpath}: {e}")
    
    # 只取出现次数 >= 2 的词（过滤OCR噪音）
    valid_words = {w for w, c in word_counter.items() if c >= 2}
    print(f"  提取到 {len(valid_words)} 个唯一单词（出现>=2次）")
    return valid_words, word_counter


# ═══════════════════════════════════════════════════════════
# Phase 1: 清洗 capX_vocab_clean.json
# ═══════════════════════════════════════════════════════════

def is_valid_latin_word(word, ref_dict, ref_counter):
    """判断一个词条是否为合法的拉丁词"""
    w = word.strip()
    if not w or len(w) < 2:
        return False
    
    lower = w.lower()
    
    # 1. 检查是否全是拉丁字符（含长音）
    if not all(c in LATIN_CHARS for c in w):
        return False
    
    # 2. 罗马数字（保留）
    if lower in ROMAN_NUMERALS:
        return True
    
    # 3. 语法术语（保留）
    if lower in GRAMMAR_TERMS:
        return True
    
    # 4. 已知乱码（删除）
    if lower in KNOWN_GIBBERISH:
        return False
    
    # 5. 已知OCR拼写错误（删除）
    if lower in KNOWN_OCR_ERRORS:
        return False
    
    # 6. 已知截断词根（无条件删除，>=3字符）
    # 注意：参考词典也可能被OCR污染，所以不依赖ref_dict判断
    if len(w) >= 3 and lower in TRUNCATED_ROOTS:
        return False
    
    # 7. 单字母（删除，除非是罗马数字）
    if len(w) == 1:
        return w.lower() in ROMAN_NUMERALS
    
    # 8. 粘合词检测
    if len(w) > 3:
        # 8a. 大小写混合（如 oppidumBrundisium）
        inner = w[1:]
        if any(c.isupper() for c in inner):
            return False
        # 8b. 小写粘合词：尝试分割为两个已知词
        if len(w) >= 5:
            lower_w = w.lower()
            for split_pos in range(3, len(lower_w) - 2):
                part1 = lower_w[:split_pos]
                part2 = lower_w[split_pos:]
                if part1 in ref_dict and part2 in ref_dict:
                    return False  # 两个独立词粘在一起，无效
    
    # 9. 纯数字（删除）
    if w.isdigit():
        return len(w) == 1 and w.lower() in ROMAN_NUMERALS
    
    # 10. 在参考词典中出现过（保留）
    if lower in ref_dict:
        return True
    
    # 11. 长度 >= 4 且在参考词典中作为独立词形出现（保留）
    # 注意：不在参考词典中的词，除非是明显的完整词形，否则删除
    if len(w) >= 4:
        # 检查是否是参考词典中某个词的完整形式
        # 只有在参考词典中以该词为前缀或后缀时（即它是某个词的变体），才保留
        found_in_dict = False
        for ref_word in ref_dict:
            if ref_word == lower:
                found_in_dict = True
                break
            # 检查该词是否是参考词典中某个词的弯曲形式
            # 例如 "puella" 在词典中，那么 "puellam", "puellae" 等也应该保留
            if len(ref_word) >= 4 and len(lower) >= 4:
                if ref_word.startswith(lower[:-1]) and len(ref_word) <= len(lower) + 2:
                    found_in_dict = True
                    break
                if lower.startswith(ref_word[:-1]) and len(lower) <= len(ref_word) + 2:
                    found_in_dict = True
                    break
        
        if found_in_dict:
            return True
        
        # 检查是否是已知的拉丁词尾模式（-us, -a, -um, -i, -ae, -is, -es, -em, -am, -os, -as, -orum, -arum, -ibus, -re, -ere, -are, -ire）
        # 这是最后的宽松检查
        latin_endings = ['us', 'um', 'a', 'ae', 'i', 'is', 'es', 'em', 'am', 'os', 'as',
                        'orum', 'arum', 'ibus', 're', 'ere', 'are', 'ire', 'nt', 'ntur',
                        'tur', 'mus', 'tis', 'bat', 'bant', 'bit', 'bunt', 'vit', 'verunt']
        has_latin_ending = any(lower.endswith(e) for e in latin_endings)
        if has_latin_ending and len(w) >= 5:
            return True
        if has_latin_ending and len(w) == 4 and lower in ref_dict:
            return True
    
    # 12. 不在参考词典中且不匹配拉丁词尾 → 删除
    return False


def clean_vocab_file(fpath, ref_dict, ref_counter):
    """清洗单个 vocab_clean.json 文件"""
    try:
        data = json.loads(fpath.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"    错误: {fpath}: {e}")
        return 0, 0
    
    original_count = len(data)
    cleaned = []
    seen = set()
    
    for word in data:
        if not is_valid_latin_word(word, ref_dict, ref_counter):
            continue
        
        # 去重（大小写不敏感）
        lower = word.lower()
        if lower in seen:
            continue
        
        # 专有名词保留大写，其他用小写
        if word[0].isupper() and word.lower() in ref_dict:
            # 检查是否作为专有名词出现在参考词典中
            if word in ref_counter or word.lower() == word:
                # 不是专有名词，小写化
                cleaned.append(word.lower())
            else:
                cleaned.append(word)
        else:
            cleaned.append(word.lower())
        
        seen.add(lower)
    
    # 排序
    cleaned.sort(key=str.lower)
    
    fpath.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
    return original_count, len(cleaned)


def phase1_clean_vocab(ref_dict, ref_counter):
    """Phase 1: 清洗所有 capX_vocab_clean.json"""
    print("\n" + "=" * 60)
    print("Phase 1: 清洗 capX_vocab_clean.json")
    print("=" * 60)
    
    vocab_files = sorted(VOCAB_DIR.glob("cap*_vocab_clean.json"))
    total_orig = 0
    total_clean = 0
    results = []
    
    for fpath in vocab_files:
        chapter = re.search(r'cap(\d+)', fpath.name)
        ch = chapter.group(1) if chapter else "?"
        orig, clean = clean_vocab_file(fpath, ref_dict, ref_counter)
        removed = orig - clean
        pct = (removed / orig * 100) if orig > 0 else 0
        print(f"  cap{ch}: {orig} → {clean} (删除 {removed} 条, {pct:.0f}%)")
        total_orig += orig
        total_clean += clean
        results.append((ch, orig, clean))
    
    total_removed = total_orig - total_clean
    print(f"\n  总计: {total_orig} → {total_clean} (删除 {total_removed} 条, {total_removed/total_orig*100:.0f}%)")
    return results


# ═══════════════════════════════════════════════════════════
# Phase 2: 清洗 OCR 正文文件
# ═══════════════════════════════════════════════════════════

def clean_ocr_text_file(fpath, ref_dict):
    """清洗单个 OCR 文本文件"""
    try:
        text = fpath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"    错误: {fpath}: {e}")
        return 0
    
    changes = 0
    original_text = text
    
    # 1. 修复行间断词：扫描所有相邻单词对，尝试合并
    # 使用 token 扫描而非 regex，避免边界冲突
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        # 保留行号标记 [N]
        prefix = ''
        rest = line
        m = re.match(r'^(\[\d+\]\s*)', line)
        if m:
            prefix = m.group(1)
            rest = line[m.end():]
        
        # 分词
        tokens = re.findall(r'[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+|[^a-zA-ZāēīōūȳĀĒĪŌŪȲ]+', rest)
        if not tokens:
            new_lines.append(line)
            continue
        
        # 扫描相邻的纯拉丁词token，尝试合并
        i = 0
        merged = []
        while i < len(tokens):
            tok = tokens[i]
            # 跳过非词token
            if not re.match(r'^[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+$', tok):
                merged.append(tok)
                i += 1
                continue
            
            # 当前是拉丁词，看下一个是否也是拉丁词
            if i + 1 < len(tokens) and re.match(r'^[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+$', tokens[i+1]):
                next_tok = tokens[i+1]
                # 跳过中间的非词token
                joined = (tok + next_tok).lower()
                # 检查合并后是否在参考词典中
                if joined in ref_dict and len(tok) <= 6 and len(next_tok) <= 6:
                    # 合并两个词
                    if tok[0].isupper():
                        merged.append(tok + next_tok.lower())
                    else:
                        merged.append(tok + next_tok)
                    changes += 1
                    i += 2
                    continue
            
            merged.append(tok)
            i += 1
        
        new_lines.append(prefix + ''.join(merged))
    
    text = '\n'.join(new_lines)
    
    # 2. 修复大小写混合的粘合词（如 oppidumBrundisium）
    def fix_camel_glued(match):
        nonlocal changes
        word = match.group(0)
        parts = re.findall(r'[a-zāēīōūȳ]+|[A-ZĀĒĪŌŪȲ][a-zāēīōūȳ]*', word)
        if len(parts) >= 2:
            all_valid = all((p.lower() in ref_dict or len(p) <= 2) for p in parts)
            if all_valid:
                changes += 1
                return ' '.join(parts)
        return word
    
    text = re.sub(r'\b[a-zA-ZāēīōūȳĀĒĪŌŪȲ]{5,30}\b', fix_camel_glued, text)
    
    # 3. 修复小写粘合词（尝试按字典分割）
    def fix_lower_glued(match):
        nonlocal changes
        word = match.group(0)
        lower_w = word.lower()
        # 只在词长 >= 5 时尝试分割
        if len(lower_w) < 5:
            return word
        # 尝试在每个位置分割
        for split_pos in range(3, len(lower_w) - 2):
            part1 = lower_w[:split_pos]
            part2 = lower_w[split_pos:]
            if part1 in ref_dict and part2 in ref_dict:
                # 确保两个部分都是合理的拉丁词（至少3个字符）
                if len(part1) >= 3 and len(part2) >= 3:
                    changes += 1
                    return f"{part1} {part2}"
        return word
    
    text = re.sub(r'\b[a-zāēīōūȳ]{5,20}\b', fix_lower_glued, text)
    
    # 4. 修复行号混入词中（数字+字母粘在一起）
    def fix_number_word(match):
        nonlocal changes
        num = match.group(1)
        word = match.group(2)
        if word.lower() in ref_dict or len(word) >= 3:
            changes += 1
            return f"{num} {word}"
        return match.group(0)
    
    text = re.sub(r'\b(\d+)([a-zA-ZāēīōūȳĀĒĪŌŪȲ]+)\b', fix_number_word, text)
    
    # 5. 清理多余的引号转义
    text = text.replace('\\"', '"')
    text = text.replace("\\'", "'")
    
    # 6. 清理多余的空格
    text = re.sub(r' {2,}', ' ', text)
    
    fpath.write_text(text, encoding="utf-8")
    return changes


def phase2_clean_ocr(ref_dict):
    """Phase 2: 清洗所有 OCR 文本文件"""
    print("\n" + "=" * 60)
    print("Phase 2: 清洗 OCR 正文文件")
    print("=" * 60)
    
    ocr_files = list(OCR_DIR.rglob("*.txt"))
    # 排除 INDEX.md
    ocr_files = [f for f in ocr_files if f.name != "INDEX.md"]
    print(f"  共 {len(ocr_files)} 个txt文件")
    
    total_changes = 0
    sections = {
        "Familia Romana": [],
        "Roma Aeterna": [],
        "Fabulae Syrae": [],
    }
    
    for fpath in sorted(ocr_files):
        rel = str(fpath.relative_to(OCR_DIR))
        changes = clean_ocr_text_file(fpath, ref_dict)
        total_changes += changes
        
        if "familia_romana" in rel:
            sections["Familia Romana"].append((rel, changes))
        elif "roma_aeterna" in rel:
            sections["Roma Aeterna"].append((rel, changes))
        else:
            sections["Fabulae Syrae"].append((rel, changes))
    
    for section, files in sections.items():
        ch_count = len(files)
        ch_changes = sum(c for _, c in files)
        print(f"  {section}: {ch_count} 文件, {ch_changes} 处修复")
    
    print(f"\n  总计: {total_changes} 处修复")
    return total_changes


# ═══════════════════════════════════════════════════════════
# Phase 3: 重新生成派生文件
# ═══════════════════════════════════════════════════════════

def phase3_regenerate():
    """Phase 3: 从清洗后的词表重新生成派生文件"""
    print("\n" + "=" * 60)
    print("Phase 3: 重新生成派生文件")
    print("=" * 60)
    
    # 3.1 重新生成 word_chapter_map.json
    # 从所有 capX_vocab_clean.json 构建
    word_chapter_map = {}
    vocab_files = sorted(VOCAB_DIR.glob("cap*_vocab_clean.json"))
    
    for fpath in vocab_files:
        chapter = re.search(r'cap(\d+)', fpath.name)
        if not chapter:
            continue
        ch = int(chapter.group(1))
        try:
            words = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception:
            continue
        for word in words:
            w = word.lower()
            if w not in word_chapter_map:
                word_chapter_map[w] = []
            if ch not in word_chapter_map[w]:
                word_chapter_map[w].append(ch)
    
    wcm_path = BASE / "difficulty_algorithm" / "word_chapter_map.json"
    wcm_path.write_text(
        json.dumps(word_chapter_map, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"  word_chapter_map.json: {len(word_chapter_map)} 个词条")
    
    # 3.2 检查 lemma_chapter_map.json 是否存在
    lcm_path = BASE / "difficulty_algorithm" / "lemma_chapter_map.json"
    if lcm_path.exists():
        print(f"  lemma_chapter_map.json: 保留（需单独更新）")
    
    # 3.3 检查 word_lemma_map.json 是否存在
    wlm_path = BASE / "difficulty_algorithm" / "word_lemma_map.json"
    if wlm_path.exists():
        print(f"  word_lemma_map.json: 保留（需单独更新）")
    
    print("  Phase 3 完成")


# ═══════════════════════════════════════════════════════════
# 更新计划书进度
# ═══════════════════════════════════════════════════════════

def update_plan(results):
    """更新 CLEAN_TASK_PLAN.md 中的进度表"""
    plan_content = PLAN_FILE.read_text(encoding="utf-8")
    
    # 更新 Phase 1 进度
    for ch, orig, clean in results:
        # 匹配 "| cap{ch} | ? | — | 待做 |" 并更新
        old = f"| cap{ch} | ? | — | 待做 |"
        new = f"| cap{ch} | {orig} | {clean} | 已完成 |"
        plan_content = plan_content.replace(old, new)
    
    PLAN_FILE.write_text(plan_content, encoding="utf-8")
    print(f"\n  计划书已更新: {PLAN_FILE}")


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("LLPSI OCR & 词表 综合清洗")
    print("=" * 60)
    
    # Step 0: 构建参考词典
    print("\nStep 0: 构建拉丁词参考词典...")
    ref_dict, ref_counter = extract_words_from_ocr()
    
    # Phase 1: 清洗词表
    results = phase1_clean_vocab(ref_dict, ref_counter)
    
    # Phase 2: 清洗 OCR
    phase2_clean_ocr(ref_dict)
    
    # Phase 3: 重新生成
    phase3_regenerate()
    
    # 更新计划书
    update_plan(results)
    
    print("\n" + "=" * 60)
    print("全部清洗完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()