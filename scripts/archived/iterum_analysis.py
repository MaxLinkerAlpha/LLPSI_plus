#!/usr/bin/env python3
"""
LLPSI Familia Romana 词频分析脚本 (iterum_analysis.py)
======================================================
功能:
  1. 按 CAPITVLVM 切分全书文本
  2. 统计每章的新增词形、总词形、新词密度
  3. 追踪词汇复现率
  4. 输出「陡坡章节」报告 + 每章词汇表

设计要点:
  - 使用表面词形 (word forms) 而非词元 (lemmas) — 避免拉丁语 NLP 依赖
  - 仅统计正文阅读部分 (排除 Grammatica / Pensa / Vocabula 列表)
  - 输出 Markdown 格式报告, 便于阅读
"""

import re
import os
from collections import Counter, defaultdict

# ============================================================
# 配置
# ============================================================
INPUT_FILE = "/Users/max/Downloads/Projects/LLPSI+++/ocr_output/familia_romana/clean.txt"
OUTPUT_DIR = "/Users/max/Downloads/Projects/LLPSI+++/analysis_output"

# 需要排除的章节标记 (非主文本部分)
EXCLUDE_SECTIONS = [
    'GRAMMATICA LATINA',
    'PENSVM A', 'PENSVM B', 'PENSVM C',
    'PENSA', 'PENSVM',
    'Vocābula', 'VOCABVLA',
    'INDEX', 'ARS GRAMMATICA', 'ARSGRAMMATICA',
    'TABVLA', 'TABVLAE',
]

# 罗马数字 → 阿拉伯数字 映射
ROMAN_TO_INT = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20,
    'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24, 'XXV': 25,
    'XXVI': 26, 'XXVII': 27, 'XXVIII': 28, 'XXIX': 29, 'XXX': 30,
    'XXXI': 31, 'XXXII': 32, 'XXXIII': 33, 'XXXIV': 34, 'XXXV': 35,
}

# 拉丁语数字词 (也会出现在文本中)
LATIN_NUMBERS = {
    'prīmum', 'prīmus', 'secundum', 'secundus', 'tertium', 'tertius',
    'quārtum', 'quārtus', 'quīntum', 'quīntus', 'sextum', 'sextus',
    'septimum', 'septimus', 'octāvum', 'octāvus', 'nōnum', 'nōnus',
    'decimum', 'decimus',
}

# 极高频功能词 (在密度分析中可能干扰, 用于参考)
HIGH_FREQ_WORDS = {
    'est', 'sunt', 'et', 'in', 'nōn', 'sed', 'cum', 'quī', 'quae',
    'quod', 'ad', 'ab', 'ex', 'dē', 'per', 'aut', 'vel', 'iam',
    'etiam', 'quoque', 'tamen', 'enim', 'nam', 'igitur', 'ergō',
}


def split_into_chapters(text: str) -> dict[int, str]:
    """
    按 CAPITVLVM / CAP. 标记将全文切分为章节

    LLPSI 的章节标记有两种格式:
    - 第 1-17 章 (FR): "CAPITVLVM PRIMVM" ... "CAPITVLVM SEPTIMVM DECIMVM"
    - 第 18-35 章 (FR): "CAP. XVIII" ... "CAP. XXXV"
    - 第 36-56 章 (RA): "CAPITVLVM TRICESIMVM SEXTVM" ... "CAPITVLVM QVINQVAGESIMVM SEXTVM"

    返回: {章节号: 章节全文} 字典
    """
    # 复用 segment_book.py 的 LATIN_ORDINALS (已扩展到 RA 范围)
    import importlib.util
    spec = importlib.util.spec_from_file_location('segment_book', os.path.join(os.path.dirname(__file__), 'segment_book.py'))
    seg_mod = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise ImportError("can't load segment_book.py")
    spec.loader.exec_module(seg_mod)
    LATIN_ORDINALS = seg_mod.LATIN_ORDINALS
    ROMAN_MAP = seg_mod.ROMAN_MAP

    # 收集所有章节边界: (位置, 章节号)
    boundaries = []

    # 模式 1: CAPITVLVM [ORDINAL] (FR Cap. 1-17 + RA Cap. 36-56)
    # 直接用 LATIN_ORDINALS 的所有 key 构建正则
    keys_sorted = sorted(LATIN_ORDINALS.keys(), key=lambda k: -len(k))
    ordinal_alternation = '|'.join(re.escape(k).replace(r'\ ', r'\s+') for k in keys_sorted)
    ordinal_pattern = re.compile(
        r'CAPITVLVM\s+(' + ordinal_alternation + r')',
        re.IGNORECASE
    )

    for match in ordinal_pattern.finditer(text):
        ordinal_name = re.sub(r'\s+', ' ', match.group(1)).strip()
        ch_num = LATIN_ORDINALS.get(ordinal_name)
        if ch_num:
            boundaries.append((match.start(), ch_num))

    # 模式 2: CAP. [ROMAN] (FR Cap. 18-35 + RA Cap. 36-56)
    # 长模式放在前面避免被短模式截断
    roman_keys = sorted(ROMAN_MAP.keys(), key=lambda k: -len(k))
    roman_alternation = '|'.join(re.escape(k) for k in roman_keys)
    cap_pattern = re.compile(
        r'\bCAP\.\s+(' + roman_alternation + r')\b',
    )

    for match in cap_pattern.finditer(text):
        roman = match.group(1)
        ch_num = ROMAN_MAP.get(roman)
        # 不再限制 ch_num >= 18: 若 CAPITVLVM 模式漏识别 (例如 OCR 把
        # OCTAVVM 错成 OCTAWM), 这里用 CAP. VIII 兜底; seen 去重避免重复
        if ch_num:
            boundaries.append((match.start(), ch_num))
    
    # 按位置排序, 去重 (同一章节只保留第一个匹配)
    boundaries.sort()
    seen = set()
    unique_boundaries = []
    for pos, ch_num in boundaries:
        if ch_num not in seen:
            unique_boundaries.append((pos, ch_num))
            seen.add(ch_num)
    
    # 构建章节字典
    chapters = {}
    for i, (start, ch_num) in enumerate(unique_boundaries):
        end = unique_boundaries[i + 1][0] if i + 1 < len(unique_boundaries) else len(text)
        chapters[ch_num] = text[start:end]
    
    return chapters


def is_section_to_exclude(line: str) -> bool:
    """判断某行是否属于需要排除的非正文部分"""
    line_upper = line.upper().strip()
    for excl in EXCLUDE_SECTIONS:
        if excl.upper() in line_upper:
            return True
    return False


def extract_readings_from_chapter(chapter_text: str) -> str:
    """
    从章节文本中仅提取阅读正文部分
    (排除 Grammatica, Pensa, Vocabula 等非正文)
    
    策略: 找到 GRAMMATICA LATINA 行之前的所有内容作为正文
    """
    lines = chapter_text.split('\n')
    
    reading_lines = []
    in_grammar = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # 检测是否进入语法/练习/词汇表区域
        if re.search(r'GRAMMATICA\s+LATINA', line_stripped, re.IGNORECASE):
            in_grammar = True
            continue
        if re.search(r'PENSVM\s+[ABC]', line_stripped, re.IGNORECASE):
            in_grammar = True
            continue
        if re.search(r'^Vocābula', line_stripped):
            in_grammar = True
            continue
        
        if not in_grammar:
            reading_lines.append(line)
    
    return '\n'.join(reading_lines)


def tokenize(text: str) -> list[str]:
    """
    对拉丁语文本进行分词
    
    处理:
    - 去除标点符号
    - 保留长音符 (ā, ē, ī, ō, ū, ȳ)
    - 转为小写 (便于统计, 但保留大写信息做参考)
    - 滤除纯数字和单字符
    """
    # 去除标点 (保留长音符字母和连字符)
    text = re.sub(r'[\[\](){}«»""''""„"·•…,.:;!?\-\u2013\u2014\u2015\u2018\u2019\u201c\u201d\u201a\u201e]+', ' ', text)
    
    words = []
    for token in text.split():
        token = token.strip()
        # 跳过空字符串、纯数字、单字符
        if not token:
            continue
        if token.isdigit():
            continue
        if len(token) <= 1 and not token.isalpha():
            continue
        # 清理前后的连字符
        token = token.strip('-')
        if not token:
            continue
        words.append(token)
    
    return words


def analyze_book(text_path: str) -> dict:
    """
    主分析函数
    
    返回包含所有分析结果的字典
    """
    print("=" * 60)
    print("LLPSI Familia Romana 词频分析")
    print("=" * 60)
    
    # 读取文本
    print(f"\n读取文本: {text_path}")
    with open(text_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    # 清理
    full_text = re.sub(r'={3,}.*?={3,}', '', full_text)  # 去除页面分隔符
    full_text = re.sub(r'--- 第 \d+ 页 ---', '', full_text)
    full_text = re.sub(r'--- PAGE \d+ ---', '', full_text)  # 兼容 HD 提取格式
    full_text = re.sub(r'--- \d+ ---', '', full_text)        # 兜底: 裸数字分隔符
    
    print(f"  全文长度: {len(full_text):,} 字符")
    
    # 切分章节
    print("\n切分章节...")
    chapters = split_into_chapters(full_text)
    print(f"  识别到 {len(chapters)} 个章节")
    
    # 提取每章的阅读正文
    print("提取阅读正文...")
    chapter_readings = {}
    for num in sorted(chapters.keys()):
        reading_text = extract_readings_from_chapter(chapters[num])
        # 移除章节标题行
        reading_text = re.sub(r'CAPITVLVM\s+\w+.*', '', reading_text)
        reading_text = re.sub(r'CAP\.\s+[IVX]+.*', '', reading_text)
        chapter_readings[num] = reading_text
    
    # 分析每章
    print("分析词频...\n")
    
    global_vocab = set()       # 已出现的所有词形
    chapter_stats = []          # 每章统计数据
    
    for num in sorted(chapter_readings.keys()):
        text = chapter_readings[num]
        words = tokenize(text)
        
        # 转为小写统计
        words_lower = [w.lower() for w in words]
        
        total_tokens = len(words_lower)
        unique_in_chapter = set(words_lower)
        
        # 本章新增词形 (之前章节未出现过的)
        new_words = unique_in_chapter - global_vocab
        
        # 更新全局词汇
        global_vocab.update(words_lower)
        
        # 统计词频
        word_counts = Counter(words_lower)
        
        # 新词密度 = 新增词形数 / 本章总词形数 * 100
        new_word_density = (len(new_words) / total_tokens * 100) if total_tokens > 0 else 0
        
        # 新词中高频词 (本章出现 ≥3 次) 的数量
        new_high_freq = sum(1 for w in new_words if word_counts[w] >= 3)
        
        chapter_stats.append({
            'num': num,
            'total_tokens': total_tokens,
            'unique_words': len(unique_in_chapter),
            'new_words': len(new_words),
            'new_word_density': new_word_density,
            'new_high_freq_words': new_high_freq,
            'cumulative_vocab': len(global_vocab),
            'new_word_list': sorted(new_words),
            'top_new_words': sorted(
                [(w, word_counts[w]) for w in new_words if word_counts[w] >= 2],
                key=lambda x: -x[1]
            )[:15],
        })
        
        # 打印简要进度
        print(f"  Cap. {num:2d}: {total_tokens:4d} 词 | "
              f"+{len(new_words):3d} 新词 | "
              f"密度 {new_word_density:.1f}% | "
              f"累计词汇 {len(global_vocab):4d}")
    
    print(f"\n分析完成! 全书总词形 (表面): {len(global_vocab):,}")
    
    return {
        'chapter_stats': chapter_stats,
        'total_unique_forms': len(global_vocab),
    }


def generate_report(data: dict, output_dir: str):
    """生成 Markdown 格式的分析报告"""
    os.makedirs(output_dir, exist_ok=True)
    
    stats = data['chapter_stats']
    
    # ============================================================
    # 计算阈值
    # ============================================================
    densities = [s['new_word_density'] for s in stats]
    avg_density = sum(densities) / len(densities) if densities else 0
    
    # "陡坡章节" = 新词密度超过平均值 120% 的章节
    steep_threshold = avg_density * 1.2
    steep_chapters = [s for s in stats if s['new_word_density'] > steep_threshold]
    
    # ============================================================
    # 生成报告
    # ============================================================
    report = []
    report.append("# LLPSI Familia Romana 词频分析报告\n")
    report.append(f"**分析对象**: Familia Romana (Pars I) OCR 文本\n")
    report.append(f"**全书总词形 (表面形式)**: {data['total_unique_forms']:,}\n")
    report.append(f"**全书章节数**: {len(stats)}\n")
    report.append(f"**平均每章新词密度**: {avg_density:.1f}%\n")
    report.append(f"**陡坡判定阈值**: > {steep_threshold:.1f}% (平均值 × 1.2)\n")
    report.append("\n---\n\n")
    
    # ---- 1. 每章总览表 ----
    report.append("## 一、每章词频总览\n\n")
    report.append("| 章节 | 总词数 | 新词数 | 新词密度 | 累计词汇 | 高频新词 | 评级 |\n")
    report.append("|:----:|------:|------:|--------:|--------:|--------:|:----:|\n")
    
    for s in stats:
        # 评级
        if s['new_word_density'] > avg_density * 1.5:
            rating = '🔴 陡坡'
        elif s['new_word_density'] > steep_threshold:
            rating = '🟡 注意'
        elif s['new_word_density'] < avg_density * 0.6:
            rating = '🟢 平缓'
        else:
            rating = '⚪ 正常'
        
        report.append(
            f"| Cap. {s['num']:2d} | {s['total_tokens']:5d} | "
            f"{s['new_words']:4d} | {s['new_word_density']:5.1f}% | "
            f"{s['cumulative_vocab']:6d} | {s['new_high_freq_words']:5d} | "
            f"{rating} |\n"
        )
    
    report.append("\n---\n\n")
    
    # ---- 2. 陡坡章节详情 ----
    report.append("## 二、陡坡章节详情 (需要补充阅读)\n\n")
    
    if steep_chapters:
        report.append(f"共 **{len(steep_chapters)}** 个章节新词密度超过阈值 ({steep_threshold:.1f}%):\n\n")
        
        for s in steep_chapters:
            report.append(f"### Cap. {s['num']} — 新词密度 {s['new_word_density']:.1f}%\n\n")
            report.append(f"- 本章总词数: {s['total_tokens']}\n")
            report.append(f"- 新增词数: {s['new_words']}\n")
            report.append(f"- 累计已学词汇: {s['cumulative_vocab']}\n")
            report.append(f"- 高频新词 (≥3次): {s['new_high_freq_words']}\n")
            
            if s['top_new_words']:
                report.append(f"\n**本章高频新词** (出现 ≥2 次):\n\n")
                for word, count in s['top_new_words']:
                    report.append(f"- `{word}` ({count}次)\n")
            
            report.append("\n")
    else:
        report.append("未检测到明显陡坡章节。\n\n")
    
    report.append("\n---\n\n")
    
    # ---- 3. 词汇增长曲线分析 ----
    report.append("## 三、词汇增长曲线\n\n")
    
    # 找出累计词汇增长最快的区间
    report.append("### 累计词汇量变化\n\n")
    prev_cumulative = 0
    growth_spikes = []
    
    for s in stats:
        growth = s['cumulative_vocab'] - prev_cumulative
        growth_spikes.append((s['num'], growth))
        prev_cumulative = s['cumulative_vocab']
    
    # Top 5 增长最大的章节
    growth_spikes.sort(key=lambda x: -x[1])
    report.append("**新增词汇量最多的 5 个章节**:\n\n")
    report.append("| 章节 | 新增词汇 |\n")
    report.append("|:----:|--------:|\n")
    for num, growth in growth_spikes[:5]:
        report.append(f"| Cap. {num} | +{growth} |\n")
    
    report.append("\n---\n\n")
    
    # ---- 4. 低复现率词汇检测 ----
    report.append("## 四、低复现率词汇 (曝光不足)\n\n")
    
    # 重新扫描全书，追踪每个词在各章节的出现次数
    from collections import defaultdict
    word_chapter_freq = defaultdict(int)
    
    for num in sorted(data.get('_chapter_texts', {}).keys()) if '_chapter_texts' in data else []:
        pass
    
    # 简化版：在前 10 章中首次出现但在 10-20 章中再未出现的词
    report.append("> 此分析需要跨章节词汇追踪，将在后续版本中完善。\n")
    report.append("> MVP 阶段以「陡坡章节」分析作为补充阅读的主要生成依据。\n")
    
    report.append("\n---\n\n")
    
    # ---- 5. 建议 ----
    report.append("## 五、补充阅读生成建议\n\n")
    report.append("基于以上分析，建议优先生成以下章节的补充阅读:\n\n")
    
    priority = sorted(stats, key=lambda s: -s['new_word_density'])
    
    report.append("| 优先级 | 章节 | 新词密度 | 理由 |\n")
    report.append("|:------:|:----:|:--------:|------|\n")
    
    for rank, s in enumerate(priority[:10], 1):
        reasons = []
        if s['new_word_density'] > avg_density * 1.5:
            reasons.append("密度极高")
        if s['num'] >= 8 and s['num'] <= 15:
            reasons.append("\"第九章墙\"区域")
        if s['new_high_freq_words'] < 5:
            reasons.append("高频新词偏少")
        if not reasons:
            reasons.append("新词密度偏高")
        
        report.append(f"| {rank} | Cap. {s['num']} | {s['new_word_density']:.1f}% | {'; '.join(reasons)} |\n")
    
    report.append("\n---\n\n")
    
    # ---- 6. CSV 数据导出提示 ----
    report.append("## 六、原始数据\n\n")
    report.append("每章详细统计数据已导出至: `chapter_stats.csv`\n\n")
    
    # 写入报告
    report_path = os.path.join(output_dir, 'analysis_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(''.join(report))
    
    # 导出 CSV 数据
    csv_path = os.path.join(output_dir, 'chapter_stats.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("章节,总词数,新词数,新词密度(%),累计词汇,高频新词\n")
        for s in stats:
            f.write(f"{s['num']},{s['total_tokens']},{s['new_words']},"
                    f"{s['new_word_density']:.1f},{s['cumulative_vocab']},"
                    f"{s['new_high_freq_words']}\n")
    
    print(f"\n报告已生成: {report_path}")
    print(f"CSV 数据: {csv_path}")
    
    return report_path


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    # 分析
    data = analyze_book(INPUT_FILE)
    
    # 生成报告
    report_path = generate_report(data, OUTPUT_DIR)
    
    print(f"\n{'='*60}")
    print("全部完成!")
    print(f"  分析报告: {report_path}")
    print(f"  输出目录: {OUTPUT_DIR}")
    print(f"{'='*60}")
