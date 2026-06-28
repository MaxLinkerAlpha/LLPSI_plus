#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_grammar.py v1_2_0

================================================================================
从 LLPSI OCR 文本中提取每章核心语法概念，生成 JSON 映射表。

【用途说明】
本脚本是给 AI 提示用的"语法提示器"（grammar hint extractor），
不是语法难度评估工具。它只做简单的字符串提取与中文术语归一化，
不做语法难度的硬约束评估，也不评估章节间的难度差异。

【输入】
OCR/LLPSI_core/familia_romana/fr_cap{N}/cap{N}_grammar_macrons.txt  (N = 1..35)

【输出】
difficulty_algorithm/grammar_chapter_map.json
格式：{"1": [{"la": "Singularis et plūrālis", "zh": "单数与复数"}, ...], ...}

【算法概要】
1. 在每个 cap{N}_grammar_macrons.txt 中定位 "GRAMMATICA LATINA" 标题
2. 提取其后到下一个 "PENSVM A/B/C" 之前的全部非空行
3. 先做轻度清理（去掉前后装饰符、尾页码）
4. 用启发式规则判断每行是否为"真实语法概念标题"
   - 快速拒绝：分节标记、练习标签、对话、表格行、含问号/句号/冒号等
   - 关键检查：首词必须是已知的拉丁语语法词（白名单）
5. 用去除 macrons 后的拉丁文查表，得到中文释义
6. 输出 {"la": 原串, "zh": 中文或空串} 列表

【已知限制】
- OCR 误识（如 "Vocātious" 实为 "Vocātīvus"）通过首词白名单 + 变体字典
  部分自动纠正；剩余未能映射的会保留拉丁原文（zh 为空串）。
- 不做语法难度的硬约束评估；本脚本只做提取。
================================================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


# ==============================================================================
# 路径配置
# ==============================================================================

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
OCR_DIR: Path = PROJECT_ROOT / "OCR" / "LLPSI_core" / "familia_romana"
DEFAULT_OUTPUT: Path = PROJECT_ROOT / "difficulty_algorithm" / "grammar_chapter_map.json"


# ==============================================================================
# 拉丁语术语 -> 中文 字典
# ----------------------------------------------------------------------
# key 是去除 macrons 后的标准拉丁语术语（首字母大写）。
# 查表时会对输入做同样的 macron-strip + 小写化处理。
# ==============================================================================

TERM_ZH: Dict[str, str] = {
    # ----- 数 / 性 -----
    "Singularis": "单数",
    "Pluralis": "复数",
    "Singularis et pluralis": "单数与复数",
    "Masculinum": "阳性",
    "Femininum": "阴性",
    "Neutrum": "中性",
    "Masculinum, femininum, neutrum": "阳性、阴性、中性",

    # ----- 格 (Casus) -----
    "Nominativus": "主格",
    "Vocativus": "呼格",
    "Accusativus": "宾格",
    "Genetivus": "属格",
    "Dativus": "与格",
    "Ablativus": "夺格",
    "Locativus": "位置格",
    "Nominativus et accusativus": "主格与宾格",

    # ----- 变格 (Declinatio) -----
    "Declinatio": "变格",
    "Declinatio tertia": "第三变格",
    "Declinatio quarta": "第四变格",
    "Declinatio quinta": "第五变格",
    "Declinatio vocabulorum": "词汇的变格",
    "De declinatione": "关于变格",

    # ----- 动词 (Verbum) -----
    "Verbum": "动词",
    "Verbum activum et passivum": "主动与被动语态",
    "Verba deponentia": "异态动词",
    "Verbi tempora": "动词时态",
    "Personae verbi": "动词人称",
    "Personae verbi passivi": "被动语态人称",

    # ----- 变位 (Coniugatio) -----
    "Coniugatio": "变位",
    "Coniugatio prima": "第一变位",
    "Coniugatio secunda": "第二变位",
    "Coniugatio tertia": "第三变位",
    "Coniugatio quarta": "第四变位",

    # ----- 语式 (Modus) -----
    "Imperativus": "命令式",
    "Imperativus et indicativus": "命令式与直陈式",
    "Indicativus": "直陈式",
    "Coniunctivus": "虚拟式",

    # ----- 时态 (Tempus) -----
    "Tempus": "时态",
    "Praesens": "现在时",
    "Praeteritum": "过去时",
    "Imperfectum": "未完成时",
    "Perfectum": "完成时",
    "Futurum": "将来时",
    "Plusquamperfectum": "过去完成时",
    "Futurum perfectum": "将来完成时",
    "Tempus praesens et praeteritum": "现在时与过去时",
    "Tempus futurum": "将来时",
    "Tempus imperfectum": "未完成时",
    "Tempus perfectum": "完成时",
    "Tempus plusquamperfectum": "过去完成时",
    "Praeteritum perfectum et imperfectum": "完成时与未完成时",

    # ----- 语态 (Genus) -----
    "Activum": "主动态",
    "Passivum": "被动态",

    # ----- 不定式 / 分词 / 动名词 -----
    "Infinitivus": "不定式",
    "Infinitivus historicus": "历史不定式",
    "Participium": "分词",
    "Participium et infinitivus futuri": "未来分词与不定式",
    "Supinum": "目的动名词",
    "Gerundium": "动名词",
    "Gerundivum": "动形词",

    # ----- 形容词 / 副词 / 级别 -----
    "Adiectivum": "形容词",
    "Adverbium": "副词",
    "Comparativus": "比较级",
    "Superlativus": "最高级",

    # ----- 代词 (Pronomen) -----
    "Pronomen": "代词",
    "Relativum": "关系代词",
    "Interrogativum": "疑问代词",
    "Demonstrativum": "指示代词",
    "Personale": "人称代词",
    "Reflexivum": "反身代词",
    "Pronomina 'quis', qui, is, ille": "代词 quis, qui, is, ille",
    "Pronomina": "代词（复数）",

    # ----- 介词 / 连词 -----
    "Praepositiones": "介词",
    "Ut, ne cum coniunctivo": "带 ut/ne 的虚拟式从句",

    # ----- 诗 -----
    "De versibus": "关于诗行",
}


# OCR 常见误识变体（手动维护）
# 形式：(OCR 误识别词, 标准词)
OCR_VARIANTS: Dict[str, str] = {
    # "atius" / "atious" → "ativus"（OCR 误识 "īvu" 为 "iou"）
    "vocatius": "vocativus",
    "vocatious": "vocativus",
    "imperatius": "imperativus",
    "imperatious": "imperativus",
    "nominatius": "nominativus",
    "nominatious": "nominativus",
    "accusatius": "accusativus",
    "accusatious": "accusativus",
    "ablatius": "ablativus",
    "ablatious": "ablativus",
    "indicatius": "indicativus",
    "indicatious": "indicativus",
    # infinitivus / coniunctivus 的 OCR 变体
    "infinitious": "infinitivus",
    "infinitiuus": "infinitivus",
    "infinitiuous": "infinitivus",
    "infinitiu": "infinitivus",
    "coniunctious": "coniunctivus",
    "coniuncttous": "coniunctivus",
    "coniunctiuus": "coniunctivus",
    "coniunctiuous": "coniunctivus",
    "coniunctiu": "coniunctivus",
    # declinatio 的 OCR 变体
    "deelinatio": "declinatio",
    "declinatiō": "declinatio",
    "dēclinatiō": "declinatio",
    # 多词 OCR 变体
    "deeclinatio quarta": "declinatio quarta",
    "deeclinatio tertia": "declinatio tertia",
    "deeclinatio quinta": "declinatio quinta",
    "pronomina 'quis', qui, ^is, *ille": "pronomina",
    "proonomina 'quis', qui, ^is, *ille": "pronomina",  # macron-stripped
    "ut, *n& cum coniunctivo": "ut, ne cum coniunctivo",
    "ut, *n& cum coniunctivō": "ut, ne cum coniunctivo",
    # femininum 的 OCR 变体
    "fēmininum": "femininum",
    "femininum": "femininum",
    # superlativus 的 OCR 变体
    "superlātivus": "superlativus",
    "superlatiuus": "superlativus",
    # adiectivum 的 OCR 变体
    "adiectiuum": "adiectivum",
    "adiectivum": "adiectivum",
    # 整体噪音
    "vocatiuus": "vocativus",
    "imperatiuus": "imperativus",
    "nominatiuus": "nominativus",
    "accusatiuus": "accusativus",
    "ablatiuus": "ablativus",
    "indicatiuus": "indicativus",
    "futūrum": "futurum",
    "plūsquamperfectum": "plusquamperfectum",
    "dēclīnatiōne": "declinatione",
    "pronomina": "pronomina",
    "proōnōmina": "pronomina",
    "versibus": "versibus",
    "ut": "ut",
    "de": "de",
    "dē": "de",
    "tempus": "tempus",
    "verbi": "verbi",
    "verba": "verba",
    "personae": "personae",
    "persōnae": "personae",
    "participium": "participium",
    "supinum": "supinum",
    "gerundium": "gerundium",
    "gerundīvum": "gerundivum",
    "gerundivum": "gerundivum",
    "adverbium": "adverbium",
    "praeteritum": "praeteritum",
    "singularis": "singularis",
    "singulāris": "singularis",
    "pluralis": "pluralis",
    "plūrālis": "pluralis",
    "masculinum": "masculinum",
    "neutrum": "neutrum",
}


# ==============================================================================
# 工具函数
# ==============================================================================

_MACRON_MAP: Dict[str, str] = {
    "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u", "ȳ": "y",
    "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O", "Ū": "U", "Ȳ": "Y",
}


def strip_macrons(s: str) -> str:
    """去除拉丁语长音符号（macrons），用于字典归一化匹配。"""
    return "".join(_MACRON_MAP.get(c, c) for c in s)


def _build_normalized_dict() -> Dict[str, str]:
    """构建归一化（小写 + 去 macrons）的查表字典。"""
    out: Dict[str, str] = {}
    for k, v in TERM_ZH.items():
        out[strip_macrons(k).lower().strip()] = v
    return out


_NORM_TERM_ZH: Dict[str, str] = _build_normalized_dict()


def _fuzzy_key(s: str) -> str:
    """归一化为纯小写字母（去除 macrons、数字、标点、空格、特殊字符）。"""
    return re.sub(r"[^a-z]", "", strip_macrons(s).lower())


def _build_fuzzy_dict() -> Dict[str, str]:
    """构建模糊匹配字典（纯字母键）。"""
    out: Dict[str, str] = {}
    for k, v in TERM_ZH.items():
        fk = _fuzzy_key(k)
        if fk and fk not in out:  # 避免冲突
            out[fk] = v
    return out


_FUZZY_TERM_ZH: Dict[str, str] = _build_fuzzy_dict()


def lookup_zh(la: str) -> str:
    """
    根据拉丁语术语查找中文释义。

    匹配策略（按优先级）：
    1. 标准化（去 macrons + 小写 + 去两端标点）后直接匹配字典
    2. 通过 OCR 变体纠正后再匹配
    3. 用第一个单词再做一次匹配
    4. 模糊匹配：去除所有非字母字符后匹配（兜底，处理 OCR 严重损坏）
    """
    if not la:
        return ""
    # 统一规范化
    s = la.strip().strip(" ,.;:!?\"'`*&~^")
    # OCR 修正：'&' 常误识为 'e' 或 'ē'
    s = s.replace("&", "e")
    normalized = strip_macrons(s).lower().strip().strip(" ,.;:!?\"'`*&~^")
    if not normalized:
        return ""

    if normalized in _NORM_TERM_ZH:
        return _NORM_TERM_ZH[normalized]

    corrected = OCR_VARIANTS.get(normalized, normalized)
    if corrected != normalized and corrected in _NORM_TERM_ZH:
        return _NORM_TERM_ZH[corrected]

    first = normalized.split()[0] if normalized else ""
    if first:
        first = first.strip(" ,.;:!?\"'`*&~^")
        corrected_first = OCR_VARIANTS.get(first, first)
        if corrected_first in _NORM_TERM_ZH:
            return _NORM_TERM_ZH[corrected_first]
        if first in _NORM_TERM_ZH:
            return _NORM_TERM_ZH[first]

    # 4. 模糊匹配（兜底）：去除所有非字母字符
    fuzzy = _fuzzy_key(s)
    if fuzzy and fuzzy in _FUZZY_TERM_ZH:
        return _FUZZY_TERM_ZH[fuzzy]

    return ""


# ==============================================================================
# 首词白名单（用于判断一行是否为"语法概念标题"）
# ----------------------------------------------------------------------
# 包含所有 TERM_ZH 的首词 + OCR 变体 + 通用拉丁语法词根。
# ==============================================================================

def _build_first_word_whitelist() -> Set[str]:
    """构建首词白名单（去 macrons + 小写 + 去两端标点）。"""
    out: Set[str] = set()

    def _add(word: str) -> None:
        if not word:
            return
        # 统一规范化：去 macrons + 小写 + 去两端标点
        norm = strip_macrons(word).lower().strip(" ,.;:!?\"'`*&~^")
        if norm:
            out.add(norm)

    # 1. TERM_ZH 中所有 key 的首词
    for key in TERM_ZH.keys():
        first = strip_macrons(key).split()[0]
        _add(first)
    # 2. OCR_VARIANTS 中的变体
    for k, v in OCR_VARIANTS.items():
        _add(k)
        _add(v)
    # 3. 手动补充（OCR 误识 + 通用语法词）
    for w in (
        # 案例 OCR 变体
        "nominatious", "vocatius", "vocatious", "imperatius", "imperatious",
        "nominatius", "accusatius", "accusatious", "ablatius", "ablatious",
        "indicatius", "indicatious",
        # 不定式/虚拟式 OCR 变体
        "infinitious", "infinitiuus", "infinitiuous", "infinitiu",
        "infinitīvus", "infinitīuus",
        "coniunctious", "coniuncttous", "coniunctiuus", "coniunctiuous", "coniunctiu",
        "coniūnctīvus", "coniūnctīuus", "coniunctivus",
        # declinatio OCR 变体
        "deelinatio", "deeclinatio", "declinatiō", "dēclinatiō",
        "dēeclinātio", "declinatio",
        # 通用小写连接词
        "ut", "de", "dē",
        # 通用语法词（即使不在 TERM_ZH 中也允许）
        "tempus", "verbi", "verba", "personae", "persōnae",
        "participium", "supinum", "gerundium", "gerundīvum",
        "adverbium", "praeteritum",
        "singularis", "singulāris", "pluralis", "plūrālis",
        "masculinum", "femininum", "fēmininum", "neutrum",
        # Pronomen 各种形式（Proōnōmina → proonomina, pronomina）
        "pronomina", "proōnōmina", "proonomina",
        "versibus",
        "dēclīnatiōne", "declinatione",
        "futūrum", "futurum", "plūsquamperfectum", "plusquamperfectum",
        "adiectīvum", "adiectivum", "adiectiuum",
        "superlātīvus", "superlativus", "superlatiuus",
        "vocātīvus", "vocativus", "vocatius", "vocatious",
        "imperātīvus", "imperativus",
        "accūsātīvus", "accusativus",
        "ablātīvus", "ablativus",
        "nominātīvus", "nominativus",
        "indicātīvus", "indicativus",
    ):
        _add(w)
    return out


_FIRST_WORD_WHITELIST: Set[str] = _build_first_word_whitelist()


# ==============================================================================
# 启发式：判断一行是否为"真实语法概念标题"
# ==============================================================================

# 人物名 / 对话开头（带空格确保是词首）
_DIALOGUE_PREFIXES: tuple = (
    "Ego ", "Tu ", "Nos ", "Vos ",
    "Pater ", "Mater ", "Puer ", "Puella ",
    "Aemilia ", "Aemiliam ", "Aemiliae ",
    "Quintus ", "Marcus ", "Marcum ", "Marci ", "Marco ",
    "Iulia ", "Iuliam ", "Iulius ", "Iulium ", "Iulii ", "Iulio ",
    "Iūlia ", "Iūliam ", "Iūlius ", "Iūlium ", "Iūlii ", "Iūlio ",
    "Mārcus ", "Mārcum ",
    "Magister ", "Discipulus ",
    "Sextus ", "Titus ",
    "Medus ", "Mēdus ",
    "Lydia ", "Lydiam ", "Lydiae ",
    "Syrus ", "Syra ", "Syrae ",
    "Daedalus ", "Icarus ", "Icarum ",
    "Cuius ", "Cui ",
    "Servus ", "Servi ", "Servos ",
    "Ancilla ", "Ancillae ",
    "Agricola ", "Agricolae ",
    "Pastor ", "Pastores ",
    "Nauta ", "Nautae ",
    # 疑问 / 副词 / 连词
    "Quid ", "Quae ", "Quis ", "Quem ", "Quam ",
    "Unde ", "Ubi ", "Cūr ", "Cur ", "Quare ",
    "Num ", "Estne ", "Suntne ", "Adestne ", "Habitatne ",
    "Quot ", "Quotus ",
    "Iam ", "Tum ", "Tunc ", "Itaque ", "Ita ",
    "Eum ", "Eam ", "Eos ", "Eas ",
    "Ante ", "Post ", "Postquam ", "Cum ", "Si ", "Nisi ",
    "Heri ", "Hodie ", "Cras ",
    "Inter ", "In ", "Sub ", "Super ", "Per ", "Pro ",
    "Sic ", "Satis ",
    "Tantus ", "Tanta ", "Tanti ",
    "Ille ", "Illud ", "Illa ", "Isti ", "Istud ", "Ista ",
    "Par ", "Pares ",
    "Tot ", "Totus ", "Tota ", "Totum ",
    "Multus ", "Multa ", "Multae ", "Multos ", "Multas ",
    "Omnis ", "Omnes ", "Omnium ",
    "Nemo ", "Nullus ", "Nūllus ", "Nulla ", "Nūlla ",
    "Dantur ", "Erat ", "Erant ", "Fuit ",
    "Ceteri ", "Cēteri ",
    "Paratus ", "Parata ", "Parati ",
    "Hoc ", "Haec ", "Harum ", "His ",
    "Veni ", "Veni,", "Veni.",
    "Cui ", "Quibus ",
    "Id ",
    "Omnino ",
    "Tantum ",
)

# 单个人名（行可能只是该名字，如 "Quintum"）
_PERSON_WORDS: tuple = (
    "Quintum", "Quintus", "Quinti", "Quinto",
    "Marcum", "Marcus", "Marci", "Marco", "Mārcum", "Mārcus",
    "Iulium", "Iulius", "Iulii", "Iulio", "Iūlium", "Iūlius", "Iūlii", "Iūlio",
    "Iuliam", "Iulia", "Iūliam", "Iūlia",
    "Aemiliam", "Aemilia", "Aemiliae",
    "Sextus", "Titus",
    "Magister", "Discipulus",
    "Medus", "Mēdus", "Lydia", "Lydiam", "Lydiae",
    "Syrus", "Syra", "Syrae",
    "Daedalus", "Icarus", "Icarum",
    "Servus", "Servi", "Servos",
    "Ancilla", "Ancillae",
    "Pastor", "Pastores",
    "Agricola", "Agricolae",
    "Nauta", "Nautae",
    "Pater", "Mater", "Puer", "Puella",
    "oportet",  # impersonal verb (Cap.19)
)

# 罗马数字 + 短横线 的人称行
_ROMAN_PERSON_RE = re.compile(r"^(I|II|III|IV|H|IH)\s+[-—]?\s*\S")
# Yr（OCR 误识 II / H）
_YR_RE = re.compile(r"^Yr\s+")
# 练习标签 [1] [B] (1)
_BRACKET_LABEL_RE = re.compile(r"^[\[\(][A-Za-z0-9ivxIVX]+[\]\)]\s*")
# 问号
_QUESTION_RE = re.compile(r"\?")
# 句中冒号（标签）
_MID_COLON_RE = re.compile(r":\s+\S")
# 句中句号
_MID_PERIOD_RE = re.compile(r"\.\s+\S")
# "(—" 或 "(–" 模式
_PAREN_DASH_RE = re.compile(r"\([—–-]")
# 词首 Person/Persōna（注意不匹配 "Personae"）
_PERSONA_PREFIX_RE = re.compile(r"^Pers[oōó]na\s+")
# 数字开头（带句点编号如 "4. gen. -t"）
_DIGIT_DOT_RE = re.compile(r"^\d+\s*[.)]\s*\S")

# 拉丁字母集（含 macrons）
_LATIN_LETTER_SET = set("abcdefghijklmnopqrstuvwxyz"
                        "āēīōūȳăĕĭŏŭ")


def is_grammar_concept(raw: str) -> bool:
    """
    判断一行是否为"真实语法概念标题"。

    启发式规则：
    1. 快速拒绝：分节标记、练习标签、对话、人物名、人称行
    2. 结构检查：无问号、无句中冒号/句号、无表格分隔符 (|, em-dash)
    3. 长度：4-60 字符
    4. 首词必须在拉丁语语法词白名单内
    """
    s = raw.strip()
    if not s:
        return False

    # 1. 分节标记
    if s == "GRAMMATICA LATINA":
        return False
    if re.match(r"^GRAMMATICA\s+LATINA\b", s):
        return False
    if s.startswith("PENSVM"):
        return False

    # 2. 练习标签
    if _BRACKET_LABEL_RE.match(s):
        return False

    # 3. 前导坏字符
    BAD_STARTS = set("*&«»~^€")
    if s[0] in BAD_STARTS:
        return False
    if s.startswith("&-"):
        return False
    if s.startswith("/"):
        return False

    # 4. 问号
    if _QUESTION_RE.search(s):
        return False

    # 5. 句中冒号 / 句号
    if _MID_COLON_RE.search(s):
        return False
    if _MID_PERIOD_RE.search(s):
        return False

    # 6. 表格分隔（OCR 用 | 表示词形变化分隔）
    if "|" in s:
        return False

    # 7. em-dash with spaces（变格/变位表行）
    if " — " in s or " – " in s:
        return False

    # 8. 多个 " - "（变位表行）
    if s.count(" - ") >= 2:
        return False

    # 9. "(—" 或 "(–" 等括号 + 破折号
    if _PAREN_DASH_RE.search(s):
        return False

    # 10. 罗马数字 + 短横线 的人称行
    if _ROMAN_PERSON_RE.match(s):
        return False
    if _YR_RE.match(s):
        return False

    # 11. Persona/Persōna + 空格 的 conjugation 表行
    if _PERSONA_PREFIX_RE.match(s):
        return False

    # 12. 数字开头（"4. gen. -t" 这种小节列表）
    if _DIGIT_DOT_RE.match(s):
        return False

    # 13. 小节标签（Vocabula/Exempla/Nota/Verba: 等）
    if re.match(r"^(Vocābula|Vocabula|Exempla|Nota|Notā)\b", s):
        return False
    if re.match(r"^Verba:\s", s):
        return False

    # 14. 末尾冒号
    if s.endswith(":"):
        return False

    # 15. 人物名单
    if s in _PERSON_WORDS:
        return False
    for prefix in _DIALOGUE_PREFIXES:
        if s.startswith(prefix):
            return False

    # 16. 长度
    if len(s) < 4 or len(s) > 70:
        return False

    # 17. 字母数
    letter_count = sum(1 for c in s if c in _LATIN_LETTER_SET)
    if letter_count < 3:
        return False

    # 18. 首词必须在白名单内
    first_token = s.split()[0] if s.split() else ""
    first_word = strip_macrons(first_token).lower().rstrip(" ,.;:!?\"'`")
    if not first_word or first_word not in _FIRST_WORD_WHITELIST:
        return False

    return True


def clean_term(raw: str) -> str:
    """
    清理术语字符串：
    - 去掉首尾空白
    - 去掉前后装饰符（* ' " ` ~ ^ « » € 等）
    - 去掉尾部的页码（连续数字）
    """
    s = raw.strip()
    # 去掉前后的装饰符
    s = re.sub(r"^[*'\"`~^«»€]+", "", s)
    s = re.sub(r"[*'\"`~^«»€]+$", "", s)
    # 去掉尾部页码
    s = re.sub(r"\s+\d+\s*$", "", s)
    # 去掉尾部多余标点
    s = s.strip()
    return s


# ==============================================================================
# 单章提取
# ==============================================================================

def extract_chapter(chapter: int) -> List[Dict[str, str]]:
    """
    从 cap{N}_grammar_macrons.txt 提取该章的语法概念列表。

    返回 [{"la": 拉丁原文, "zh": 中文或空串}, ...]
    """
    grammar_file = OCR_DIR / f"fr_cap{chapter}" / f"cap{chapter}_grammar_macrons.txt"
    if not grammar_file.exists():
        print(f"[WARN] 章节 {chapter} 找不到文件: {grammar_file}", file=sys.stderr)
        return []

    try:
        with open(grammar_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"[ERROR] 读取章节 {chapter} 失败: {e}", file=sys.stderr)
        return []

    # 定位 GRAMMATICA LATINA 和下一个 PENSVM
    start_idx: int | None = None
    end_idx: int = len(lines)
    for i, line in enumerate(lines):
        s = line.strip()
        if start_idx is None:
            if s == "GRAMMATICA LATINA" or re.match(
                r"^GRAMMATICA\s+LATINA\s+\d+\s*$", s
            ):
                start_idx = i + 1
        else:
            if s.startswith("PENSVM"):
                end_idx = i
                break

    if start_idx is None:
        print(
            f"[WARN] 章节 {chapter} 找不到 GRAMMATICA LATINA 标题",
            file=sys.stderr,
        )
        return []

    concepts: List[Dict[str, str]] = []
    seen: Set[str] = set()
    for line in lines[start_idx:end_idx]:
        # 先轻度清理（去掉首尾装饰）
        cleaned = clean_term(line)
        if not cleaned:
            continue
        if not is_grammar_concept(cleaned):
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        concepts.append({"la": cleaned, "zh": lookup_zh(cleaned)})

    return concepts


# ==============================================================================
# 主入口
# ==============================================================================

def _print_chapter(chapter: int, concepts: List[Dict[str, str]]) -> None:
    """打印单个章节的提取结果（调试用）。"""
    print(f"=== Cap.{chapter} ({len(concepts)} 个语法点) ===")
    if not concepts:
        print("  (无)")
        return
    for c in concepts:
        zh = c["zh"] if c["zh"] else "(无中文释义)"
        print(f"  {c['la']:45s}  {zh}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从 LLPSI OCR 文本提取每章核心语法概念。",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="只显示指定章节的提取结果（调试用，不写文件）",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help=f"输出 JSON 路径（默认: {DEFAULT_OUTPUT}）",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="起始章节（默认: 1）",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=35,
        help="结束章节（默认: 35）",
    )
    args = parser.parse_args()

    # 调试模式：只查看单章
    if args.chapter is not None:
        concepts = extract_chapter(args.chapter)
        _print_chapter(args.chapter, concepts)
        return 0

    # 全量提取
    result: Dict[str, List[Dict[str, str]]] = {}
    unmapped_terms: Set[str] = set()

    for ch in range(args.start, args.end + 1):
        concepts = extract_chapter(ch)
        result[str(ch)] = concepts
        for c in concepts:
            if not c["zh"]:
                unmapped_terms.add(c["la"])
        print(
            f"[INFO] Cap.{ch:2d}: {len(concepts)} 个语法点",
            file=sys.stderr,
        )

    # 写入 JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    total_chapters = len(result)
    total_concepts = sum(len(v) for v in result.values())
    empty_chapters = [k for k, v in result.items() if not v]

    print(
        f"[OK] 已写入 {output_path}（{total_chapters} 章节，共 {total_concepts} 个语法点）",
        file=sys.stderr,
    )
    if empty_chapters:
        print(
            f"[WARN] 以下章节未提取到任何语法点: {', '.join(empty_chapters)}",
            file=sys.stderr,
        )
    if unmapped_terms:
        sorted_unmapped = sorted(unmapped_terms)
        print(
            f"[INFO] 未在中文字典中命中的术语（{len(sorted_unmapped)} 个）:",
            file=sys.stderr,
        )
        for t in sorted_unmapped:
            print(f"  - {t}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
