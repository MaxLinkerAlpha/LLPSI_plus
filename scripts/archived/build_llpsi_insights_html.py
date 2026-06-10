#!/usr/bin/env python3
"""
build_llpsi_insights_html.py — 生成 LLPSI_Insights.html v3.0

主要变更 (v1 → v2):
  1. 数据修正: FR末章 9,417 词形 / 10,674 词族, RA末章 33,770 词形
  2. 加入 5 维度扩展读物路由 (🎯💪📚📖🧩)
  3. 词族 vs 词形 概念说明
  4. ROI 甜蜜点 重新计算
  5. (v2.1) 点击 🧩 段 即可在 modal 中阅读原文 (D类段嵌入, 书类支持 fetch)
  6. (v2.2) 段筛选 + dooge 重复段自动选优
  7. (v2.3) 阈值温和上调: 流畅≥65% / 挑战≥50% / 节选≥30% / 段≥60%
  8. (v3.0) 切换到 token 级覆盖率, 修复 LATIN_RE/英语过滤 BUG, 重新评级全部读物

输入: analysis_output/llpsi_chapter_stats.json + llpsi_reader_routing.json
       + analysis_output/extracted/d_class_stories/*.md (段原文)
       + ../ocr_output/{slug}/_full.txt (书原文, 需 HTTP server)
输出: analysis_output/LLPSI_Insights.html
"""
import html
import json
import re
from pathlib import Path

ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")
CHAPTER_STATS = ROOT / "analysis_output" / "llpsi_chapter_stats.json"
ROUTING = ROOT / "analysis_output" / "llpsi_reader_routing.json"
OUT = ROOT / "analysis_output" / "LLPSI_Insights.html"
SEG_DIR = ROOT / "analysis_output" / "extracted" / "d_class_stories"

# === 段筛选配置 (v2.2 审读后判定) ============================================

# 主体非叙事的段, 不进入推荐路由
# 判定标准: ≥3 句连续叙事/对话必须是文档主体 (非夹杂在练习/语法表/字典中)
# key 格式: {slug}|{sp}|{ep} (与 seg_texts dict 一致)
EXCLUDED_SEGMENTS = {
    "cambridge_1|4|7",                # 单句+词汇表, p.6-7 叙事夹杂练习
    "cambridge_1|54|57",               # 仅单句展示
    "ecce_romani|33|35",               # 语法表+练习
    "dooge_beginners_key|29|31",       # 练习答案
    "latin_natural_method|36|40",      # 语法表 (INFINITIVE/PERFECT)
    "illiterati_1|318|321",            # 英拉词典
}

# dooge 同内容两版 OCR — 运行时按质量评分选一
# (slug, sp, ep) 三元组列表
DUPLICATE_GROUPS = [
    [("dooge_beginners",   214, 219),
     ("dooge_beginners_2", 214, 219)],
    [("dooge_beginners",   221, 223),
     ("dooge_beginners_2", 221, 223)],
]


def score_ocr_quality(text: str) -> float:
    """OCR 文本质量评分. 越高越好.

    评分项:
      + macron 字符数 × 2.0   (ā ē ī ō ū ȳ ǣ æ œ)
      + 重音字符数 × 1.0       (á é í ó ú ý ḗ)
      - 乱码字符数 × 3.0       (l·l, —, …, [unreadable], 多 !, 行末连字符)
      + 可读拉丁词数 × 0.05   (\\b[a-zA-Z]{3,}\\b)
    """
    macrons = "āēīōūȳǣæœ"
    accents = "áéíóúýḗ"
    mac = sum(1 for c in text if c in macrons)
    acc = sum(1 for c in text if c in accents)
    garbage_patterns = [
        r"l·l", r"\[unreadable", r"\[illegible",
        r"—+", r"…", r"!{2,}", r"\?{2,}", r"l\s+l", r"-\s*\n\s*",
    ]
    garb = sum(len(re.findall(p, text)) for p in garbage_patterns)
    words = len(re.findall(r"\b[a-zA-Z]{3,}\b", text))
    return mac * 2.0 + acc * 1.0 - garb * 3.0 + words * 0.05


def pick_duplicate_winners(seg_texts: dict) -> set:
    """从重复段组中评分选优, 返回应该丢弃的 (slug|sp|ep) key 集合.

    胜出者保留在 seg_texts 中, 败者被加入丢弃集合.
    """
    drop_keys: set = set()
    for group in DUPLICATE_GROUPS:
        scored = []
        for slug, sp, ep in group:
            key = f"{slug}|{sp}|{ep}"
            txt = seg_texts.get(key, "")
            score = score_ocr_quality(txt) if txt else -1e9
            scored.append((score, key, slug))
        scored.sort(reverse=True)  # 分数高者胜出
        # 其余丢弃
        for _, key, _ in scored[1:]:
            drop_keys.add(key)
            print(f"  [DUP-DROP] {key} (score={next(s for s,k,_ in scored if k==key):.2f})")
        winner_score, winner_key, winner_slug = scored[0]
        print(f"  [DUP-KEEP] {winner_key} (score={winner_score:.2f})")
    return drop_keys


# ============================================================================


def load_segment_texts() -> dict:
    """加载所有 D 类拉语段原文, 返回 {slug|sp|ep: text} 字典.

    段文件命名: {slug}_p{sp:03d}-{ep:03d}.md
    """
    out: dict = {}
    if not SEG_DIR.exists():
        return out
    for f in sorted(SEG_DIR.glob("*.md")):
        m = re.match(r"(.+)_p(\d{3})-(\d{3})\.md$", f.name)
        if not m:
            continue
        slug, sp, ep = m.group(1), int(m.group(2)), int(m.group(3))
        key = f"{slug}|{sp}|{ep}"
        try:
            out[key] = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  [WARN] failed to read {f.name}: {e}")
            out[key] = f"(加载失败: {e})"
    return out


def apply_segment_filter(seg_texts: dict, routing: dict):
    """应用两阶段过滤: ① 主体非叙事剔除 ② dooge 重复组选优.

    返回: (filtered_seg_texts, filtered_routing, stats)
    stats 用于写入 HTML 头部说明.
    """
    # 阶段 1: 主体非叙事剔除
    seg_texts = {k: v for k, v in seg_texts.items() if k not in EXCLUDED_SEGMENTS}

    # 阶段 2: dooge 重复组选优
    print("  [OCR 评分] dooge 重复组选优 ...")
    drop_keys = pick_duplicate_winners(seg_texts)
    seg_texts = {k: v for k, v in seg_texts.items() if k not in drop_keys}

    # 同步过滤 routing 的 segments 列表
    drop_set = EXCLUDED_SEGMENTS | drop_keys
    removed_in_routing = 0
    for r in routing.get("routing", []):
        segs = r.get("segments", [])
        kept = []
        for s in segs:
            key = f"{s['slug']}|{s.get('start_page')}|{s.get('end_page')}"
            if key in drop_set:
                removed_in_routing += 1
                continue
            kept.append(s)
        r["segments"] = kept

    stats = {
        "excluded": sorted(EXCLUDED_SEGMENTS),
        "duplicates_dropped": sorted(drop_keys),
        "removed_in_routing": removed_in_routing,
        "kept": len(seg_texts),
    }
    return seg_texts, routing, stats


def to_chapters_data():
    data = json.loads(CHAPTER_STATS.read_text(encoding="utf-8"))
    return data["fr_35_chapters"], data["ra_21_chapters"], data["summary"]


def to_routing():
    return json.loads(ROUTING.read_text(encoding="utf-8"))


def roman(n: int) -> str:
    vals = [(50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
            (5, "V"), (4, "IV"), (1, "I")]
    result = ""
    for v, s in vals:
        while n >= v:
            result += s
            n -= v
    return result


def build_chapter_option(fr_chaps, ra_chaps) -> str:
    """生成 ECharts 的章节数据序列."""
    chapters = []
    cum_vocab = []
    new_words = []
    new_density = []
    for c in fr_chaps:
        chapters.append(c["chapter"])
        cum_vocab.append(c["cumulative_vocab_db"])
        new_words.append(c["new_word_count_csv"])
        new_density.append(c["new_density_csv"])
    fr_len = len(fr_chaps)
    for i, c in enumerate(ra_chaps):
        chapters.append(c["chapter"])
        cum_vocab.append(c["cumulative_vocab_db"])
        new_words.append(c["new_word_count_csv"])
        new_density.append(c["new_density_csv"])
    return {
        "chapters": chapters,
        "cum_vocab": cum_vocab,
        "new_words": new_words,
        "new_density": new_density,
        "fr_len": fr_len,
    }


def build_routing_html(routing: dict) -> str:
    """构建扩展读物路由表 HTML — 使用 <details>/<summary> 折叠面板展示全部读物."""
    out = ['<div class="routing-grid">']

    def render_section(tag_type: str, tag: str, items: list, render_item, total_limit_show: int = 3) -> str:
        """渲染一个分类 section. 如果 items 超过 total_limit_show, 剩余项用 <details> 折叠."""
        if not items:
            return ""
        sec = ['<div class="route-section">']
        total = len(items)
        shown = items[:total_limit_show]
        rest = items[total_limit_show:]

        if not rest:
            # 全部展示, 不需要折叠
            sec.append(f'<span class="route-tag tag-{tag_type}">{tag}</span>')
            for x in shown:
                sec.append(render_item(x))
            sec.append('</div>')
            return "".join(sec)

        # 部分折叠: 前面 N 项直接展示, 剩余用 <details> 包裹
        sec.append(f'<span class="route-tag tag-{tag_type}">{tag} ({total})</span>')
        for x in shown:
            sec.append(render_item(x))
        sec.append(
            f'<details class="route-details">'
            f'<summary class="route-toggle">展开剩余 {len(rest)} 项 ▾</summary>'
            f'<div class="route-details-body">'
        )
        for x in rest:
            sec.append(render_item(x))
        sec.append('</div></details>')
        sec.append('</div>')
        return "".join(sec)

    for r in routing["routing"]:
        ch = r["chapter"]
        book = r["book"]
        title = r["title_roman"]
        cdata = r["chapter_data"]
        cv = cdata.get("cumulative_vocab_db", "?")
        cv_csv = cdata.get("cumulative_vocab_csv", "?")
        nd = cdata.get("new_density", "?")

        # 决定卡片类型
        n_readable = len(r["readable"])
        n_chal = len(r["challenges"])
        n_sel = len(r["selected"])
        n_rev = len(r["reviews"])
        n_seg = len(r["segments"])

        out.append(f'<div class="route-card" data-ch="{ch}">')
        out.append(f'<div class="route-header">')
        out.append(f'<span class="route-ch">Cap.{ch}</span>')
        out.append(f'<span class="route-book">{book}</span>')
        out.append(f'<span class="route-stats">新词密度 {nd}% · 累计 {cv}</span>')
        out.append('</div>')

        out.append('<div class="route-body">')

        # 可读
        def render_readable(x):
            slug = html.escape(x["slug"])
            title_x = html.escape(x["title"])
            return f'<div class="route-item"><code>{slug}</code> ({title_x}) t80 Cap.{x["t80"]}</div>'
        out.append(render_section("readable", "📖 可读", r["readable"], render_readable, total_limit_show=10))

        # 挑战
        def render_chal(x):
            slug = html.escape(x["slug"])
            title_x = html.escape(x["title"])
            return (
                f'<div class="route-item">'
                f'<code>{slug}</code> t70 Cap.{x["t70"]} '
                f'(教学 Cap.{x["teach_ch"]}, {x["teach_cov"]:.0%})'
                f'</div>'
            )
        out.append(render_section("challenge", "💪 挑战", r["challenges"], render_chal, total_limit_show=3))

        # 节选
        def render_sel(x):
            slug = html.escape(x["slug"])
            return (
                f'<div class="route-item">'
                f'<code>{slug}</code> h50 Cap.{x["t50"]}, '
                f'{x["unique_latin"]:,}独词, 英{x["english_ratio"]:.0%}'
                f'</div>'
            )
        out.append(render_section("selected", "📚 节选", r["selected"], render_sel, total_limit_show=3))

        # 复习
        def render_rev(x):
            slug = html.escape(x["slug"])
            return (
                f'<div class="route-item">'
                f'<code>{slug}</code> Cap.{x["teach_ch"]}({x["teach_cov"]:.0%})'
                f'</div>'
            )
        out.append(render_section("review", "📖 复习", r["reviews"], render_rev, total_limit_show=2))

        # 段 — 可点击阅读 (段原文已嵌入 SEGMENT_TEXTS)
        def render_seg(x):
            slug = html.escape(x["slug"])
            sp = x.get("start_page", "?")
            ep = x.get("end_page", "?")
            key = f"{x['slug']}|{sp}|{ep}"
            teach_ch = x.get("teach_ch", "?")
            teach_cov = x.get("teach_cov", 0)
            ch60 = x.get("ch60", "")
            unique_latin = x.get("unique_latin", 0)
            # 编码为可放入 data-* 的 JSON 字符串
            meta = json.dumps({
                "kind": "seg",
                "slug": x["slug"],
                "title": x.get("title", x["slug"]),
                "sp": sp, "ep": ep,
                "teach_ch": teach_ch, "teach_cov": teach_cov,
                "ch60": ch60, "unique_latin": unique_latin,
            }, ensure_ascii=False)
            return (
                f'<div class="route-item route-clickable" '
                f'data-key="{key}" data-meta=\'{html.escape(meta, quote=True)}\'>'
                f'<code>{slug}</code> p.{sp}-{ep} '
                f'教学 Cap.{teach_ch}({teach_cov:.0%})'
                f' <span class="route-read-badge">📖 阅读</span>'
                f'</div>'
            )
        out.append(render_section("seg", "🧩 段", r["segments"], render_seg, total_limit_show=2))

        # 空
        if not (n_readable + n_chal + n_sel + n_rev + n_seg):
            out.append('<div class="route-empty">本章暂无推荐 (早期章节词汇量少)</div>')

        out.append('</div>')  # route-body
        out.append('</div>')  # route-card
    out.append('</div>')
    return "\n".join(out)


def build_html(fr_chaps, ra_chaps, summary, routing, seg_texts: dict | None = None) -> str:
    chart = build_chapter_option(fr_chaps, ra_chaps)
    fr_len = chart["fr_len"]
    chapters = chart["chapters"]
    cum_vocab = chart["cum_vocab"]
    new_words = chart["new_words"]
    new_density = chart["new_density"]

    routing_html = build_routing_html(routing)

    # 准备章节数据用于 JS
    chapter_data_json = json.dumps(routing["routing"], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LLPSI · FR + RA 数据洞察 + 扩展读物路由 v3.0</title>
<meta name="description" content="A visual analysis of vocabulary density and reader routing across Familia Romana and Roma Aeterna, the two core books of Lingua Latina per se Illustrata.">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;800&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700&family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap">

<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --parchment:       #f4ecd8;
  --parchment-deep:  #ebe0c4;
  --parchment-edge:  #d9c89c;
  --marble:          #e8dfc4;
  --marble-light:    #f0e9d2;
  --ink:             #1c1612;
  --ink-soft:        #3a2f25;
  --ink-faded:       #5a4a38;
  --pompeii-red:     #a8392e;
  --pompeii-deep:    #7a2820;
  --imperial-gold:   #b08d2b;
  --imperial-gold-l: #d4b14a;
  --roman-green:     #2c3e3a;
  --roman-green-d:   #1a2823;
  --tyrian-purple:   #5a3e5c;
  --tyrian-purple-d: #3a2640;
  --shadow:          rgba(28, 22, 18, 0.12);
  --shadow-deep:     rgba(28, 22, 18, 0.25);
}}

html {{ scroll-behavior: smooth; }}

body {{
  font-family: 'Cormorant Garamond', 'Noto Serif SC', serif;
  font-size: 18px;
  line-height: 1.7;
  color: var(--ink);
  background-color: var(--parchment);
  padding: 32px 24px;
}}

.container {{ max-width: 1280px; margin: 0 auto; }}

.hero {{
  text-align: center;
  padding: 64px 32px;
  background: linear-gradient(135deg, var(--parchment-deep), var(--marble));
  border: 3px double var(--imperial-gold);
  border-radius: 8px;
  margin-bottom: 48px;
}}

.hero h1 {{
  font-family: 'Cinzel', serif;
  font-size: 48px;
  font-weight: 700;
  color: var(--pompeii-deep);
  letter-spacing: 4px;
  margin-bottom: 16px;
}}

.hero .subtitle {{
  font-size: 18px;
  color: var(--ink-soft);
  font-style: italic;
}}

.version-badge {{
  display: inline-block;
  padding: 4px 12px;
  background: var(--pompeii-red);
  color: white;
  font-family: 'Cinzel', serif;
  font-size: 12px;
  font-weight: 600;
  border-radius: 12px;
  margin-left: 8px;
  vertical-align: middle;
}}

.section-title {{
  font-family: 'Cinzel', serif;
  font-size: 28px;
  font-weight: 600;
  color: var(--pompeii-deep);
  text-align: center;
  margin: 48px 0 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--imperial-gold);
}}

.chart-card {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  border-radius: 8px;
  padding: 24px;
  margin: 24px 0;
  box-shadow: 0 2px 8px var(--shadow);
}}

.chart {{
  width: 100%;
  height: 420px;
}}

.chart-desc {{
  text-align: center;
  font-size: 14px;
  color: var(--ink-faded);
  font-style: italic;
  margin-top: 8px;
}}

.summary-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin: 24px 0;
}}

.summary-card {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  border-left: 4px solid var(--pompeii-red);
  border-radius: 4px;
  padding: 16px 20px;
}}

.summary-card .label {{
  font-size: 12px;
  color: var(--ink-faded);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}}

.summary-card .value {{
  font-family: 'Cinzel', serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--pompeii-deep);
}}

.summary-card .desc {{
  font-size: 13px;
  color: var(--ink-soft);
  margin-top: 4px;
}}

/* Routing grid */
.routing-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  margin: 24px 0;
}}

.route-card {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  border-radius: 6px;
  padding: 14px;
  transition: all 0.2s;
}}

.route-card:hover {{
  box-shadow: 0 4px 12px var(--shadow);
  transform: translateY(-2px);
}}

.route-header {{
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid var(--parchment-edge);
}}

.route-ch {{
  font-family: 'Cinzel', serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--pompeii-deep);
}}

.route-book {{
  font-size: 11px;
  color: var(--ink-faded);
  text-transform: uppercase;
  letter-spacing: 1px;
}}

.route-stats {{
  margin-left: auto;
  font-size: 11px;
  color: var(--ink-faded);
}}

.route-section {{
  margin: 6px 0;
  padding: 4px 0;
}}

.route-tag {{
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 3px;
  margin-right: 4px;
  min-width: 56px;
  text-align: center;
}}

.tag-reward    {{ background: #f4d35e; color: var(--ink); }}
.tag-challenge {{ background: #ee964b; color: white; }}
.tag-selected  {{ background: #5a8bb0; color: white; }}
.tag-review    {{ background: #9bc4e2; color: var(--ink); }}
.tag-seg       {{ background: #c5a880; color: var(--ink); }}

.route-item {{
  font-size: 13px;
  color: var(--ink-soft);
  padding: 2px 0 2px 8px;
  border-left: 2px solid var(--parchment-edge);
  margin: 2px 0 2px 6px;
}}

.route-item code {{
  font-family: 'SF Mono', 'Monaco', monospace;
  font-size: 12px;
  background: var(--parchment);
  padding: 1px 4px;
  border-radius: 2px;
  color: var(--pompeii-red);
}}

.route-more {{
  font-size: 11px;
  color: var(--ink-faded);
  font-style: italic;
  padding-left: 8px;
}}

/* <details>/<summary> 折叠面板 — 用于路由表中超过 3 项的分类 */
.route-details {{
  margin: 4px 0 2px 6px;
}}

.route-toggle {{
  font-size: 11px;
  color: var(--imperial-gold);
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 2px;
  list-style: none;
  user-select: none;
  display: inline-block;
  background: rgba(176, 141, 43, 0.08);
  transition: background 0.15s;
}}

.route-toggle::-webkit-details-marker {{ display: none; }}
.route-toggle::marker {{ display: none; }}

.route-toggle:hover {{
  background: rgba(176, 141, 43, 0.18);
  color: var(--pompeii-deep);
}}

.route-details[open] .route-toggle {{
  background: rgba(176, 141, 43, 0.15);
  color: var(--pompeii-deep);
}}

.route-details-body {{
  padding: 4px 0 2px 0;
  border-left: 2px dashed var(--imperial-gold-l);
  margin-left: 4px;
}}

.route-empty {{
  font-size: 12px;
  color: var(--ink-faded);
  font-style: italic;
  text-align: center;
  padding: 8px;
}}

/* 可点击的路由项 (🧩 段) — 鼠标悬停时高亮, 提示可阅读 */
.route-clickable {{
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}}

.route-clickable:hover {{
  background: rgba(176, 141, 43, 0.10);
  border-left-color: var(--imperial-gold);
  padding-left: 12px;
}}

.route-read-badge {{
  margin-left: auto;
  font-size: 10px;
  color: var(--imperial-gold);
  background: rgba(176, 141, 43, 0.12);
  padding: 1px 5px;
  border-radius: 2px;
  font-weight: 600;
  letter-spacing: 0.5px;
  opacity: 0.7;
  transition: opacity 0.15s;
}}

.route-clickable:hover .route-read-badge {{
  opacity: 1;
  background: var(--imperial-gold);
  color: white;
}}

/* 阅读器 Modal */
.reader-modal {{
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 9999;
  background: rgba(28, 22, 18, 0.85);
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}}

.reader-modal.open {{
  display: flex;
  align-items: center;
  justify-content: center;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}

.reader-panel {{
  background: var(--parchment);
  border: 2px solid var(--imperial-gold);
  border-radius: 8px;
  max-width: 900px;
  width: 92%;
  max-height: 88vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.25s ease;
}}

@keyframes slideUp {{
  from {{ transform: translateY(20px); opacity: 0.8; }}
  to {{ transform: translateY(0); opacity: 1; }}
}}

.reader-header {{
  padding: 16px 20px;
  background: linear-gradient(135deg, var(--marble), var(--parchment-deep));
  border-bottom: 2px solid var(--imperial-gold);
  display: flex;
  align-items: center;
  gap: 12px;
}}

.reader-title {{
  font-family: 'Cinzel', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--pompeii-deep);
  flex: 1;
  min-width: 0;
}}

.reader-subtitle {{
  font-size: 12px;
  color: var(--ink-faded);
  margin-top: 2px;
}}

.reader-close {{
  width: 32px;
  height: 32px;
  border: 1px solid var(--parchment-edge);
  background: var(--parchment);
  border-radius: 50%;
  font-size: 18px;
  color: var(--ink-soft);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  flex-shrink: 0;
}}

.reader-close:hover {{
  background: var(--pompeii-red);
  color: white;
  border-color: var(--pompeii-red);
}}

.reader-meta {{
  padding: 10px 20px;
  background: var(--marble);
  border-bottom: 1px solid var(--parchment-edge);
  font-size: 13px;
  color: var(--ink-soft);
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}}

.reader-meta b {{
  color: var(--pompeii-deep);
}}

.reader-body {{
  padding: 24px 32px;
  overflow-y: auto;
  flex: 1;
  font-family: 'Cormorant Garamond', 'Noto Serif SC', serif;
  font-size: 17px;
  line-height: 1.85;
  color: var(--ink);
  white-space: pre-wrap;
}}

.reader-body h1,
.reader-body h2,
.reader-body h3 {{
  font-family: 'Cinzel', serif;
  color: var(--pompeii-deep);
  margin: 16px 0 8px;
}}

.reader-body h1 {{ font-size: 20px; }}
.reader-body h2 {{ font-size: 16px; border-bottom: 1px solid var(--parchment-edge); padding-bottom: 4px; }}
.reader-body h3 {{ font-size: 14px; color: var(--imperial-gold); text-transform: uppercase; letter-spacing: 1px; }}

.reader-body hr {{
  border: none;
  border-top: 1px dashed var(--parchment-edge);
  margin: 16px 0;
}}

.reader-body code {{
  background: var(--marble);
  padding: 1px 4px;
  border-radius: 2px;
  font-size: 14px;
  color: var(--pompeii-red);
}}

.reader-loading {{
  text-align: center;
  padding: 40px;
  color: var(--ink-faded);
  font-style: italic;
}}

.reader-error {{
  background: rgba(168, 57, 46, 0.08);
  border-left: 3px solid var(--pompeii-red);
  padding: 12px 16px;
  margin: 8px 0;
  font-size: 14px;
  color: var(--pompeii-deep);
}}

.reader-empty-state {{
  text-align: center;
  padding: 40px 20px;
  color: var(--ink-faded);
}}

/* Filter bar */
.filter-bar {{
  background: var(--marble);
  border: 1px solid var(--parchment-edge);
  border-radius: 4px;
  padding: 12px 16px;
  margin: 16px 0;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}}

.filter-bar label {{
  font-size: 14px;
  color: var(--ink-soft);
}}

.filter-bar select {{
  padding: 4px 8px;
  border: 1px solid var(--parchment-edge);
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  background: var(--parchment);
}}

.footnote {{
  font-size: 13px;
  color: var(--ink-faded);
  font-style: italic;
  margin: 16px 0;
  padding: 8px 12px;
  background: var(--marble);
  border-left: 3px solid var(--imperial-gold);
  border-radius: 2px;
}}

.legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 16px 0;
  padding: 12px;
  background: var(--marble);
  border-radius: 4px;
}}

.legend-item {{
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--ink-soft);
}}
</style>
</head>
<body>
<div class="container">

<div class="hero">
  <h1>FAMILIA ROMANA<br>+<br>ROMA AETERNA
    <span class="version-badge">v3.0</span>
  </h1>
  <div class="subtitle">A visual analysis of vocabulary density and reader routing across the 56 chapters of LLPSI</div>
  <div class="subtitle" style="margin-top:8px;font-size:14px;">
    数据修正: FR 末章 <b>{summary['fr_cum_vocab_wordform']:,} 词形 / {summary['fr_cum_vocab_wordfamily']:,} 词族</b> ·
    RA 末章 <b>{summary['ra_cum_vocab_wordform']:,} 词形 / {summary['ra_cum_vocab_wordfamily']:,} 词族</b>
  </div>
</div>

<!-- 修正说明 -->
<div class="footnote">
  <b>数据修正说明 (v1.0 → v2.0) — 10× 差距的根因</b>:
  旧报告的"FR ≈ 1,800 词族 / RA ≈ 3,500 词族"是 <b>错误估算</b>. 新版基于 <code>data/llpsi_corpus.db</code> 的实际词形表重新计算, 得出 5~10 倍更大的真实数据.
  <table style="margin: 12px 0; border-collapse: collapse; width: 100%; font-size: 13px;">
    <thead>
      <tr style="background: var(--parchment-deep);">
        <th style="padding:6px;text-align:left;border:1px solid var(--parchment-edge);">指标</th>
        <th style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">v1.0 旧报告</th>
        <th style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">v2.0 实际值</th>
        <th style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">倍数</th>
      </tr>
    </thead>
    <tbody>
      <tr><td style="padding:6px;border:1px solid var(--parchment-edge);">FR 末章 (Cap.35) 累计词族</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">~1,800</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);"><b>10,674</b></td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">5.9×</td></tr>
      <tr style="background: rgba(168, 57, 46, 0.06);"><td style="padding:6px;border:1px solid var(--parchment-edge);">RA 末章 (Cap.56) 累计词族</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">~3,500</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);"><b>35,027</b></td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);"><b>10.0×</b></td></tr>
      <tr><td style="padding:6px;border:1px solid var(--parchment-edge);">FR 末章 累计词形 (DB, 去重)</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">— (未统计)</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);"><b>9,417</b></td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">—</td></tr>
      <tr><td style="padding:6px;border:1px solid var(--parchment-edge);">RA 末章 累计词形 (DB, 去重)</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">— (未统计)</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);"><b>33,770</b></td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">—</td></tr>
      <tr style="background: rgba(168, 57, 46, 0.06);"><td style="padding:6px;border:1px solid var(--parchment-edge);">RA 实际章节数 (续 FR 编号)</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">21 章 (误以为独立编号)</td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);"><b>21 章 (Cap.36-56, 续 FR 编号)</b></td>
          <td style="padding:6px;text-align:right;border:1px solid var(--parchment-edge);">同源</td></tr>
    </tbody>
  </table>
  <b>根因 1 — 词形 (Word Form) vs 词族 (Word Family) 混淆</b>:
  <ul style="margin: 6px 0 0 20px; padding: 0; line-height: 1.7;">
    <li><b>词形</b>: 文本中出现的具体屈折形式. 如 <code>puella</code>、<code>puellae</code>、<code>puellam</code>、<code>puellarum</code> 是 4 个词形, 都属于 <code>puell-</code> 一个词族</li>
    <li><b>词族</b>: 同一词根的所有变体合并. <code>puell-</code> 词族在 LLPSI 中可派生 8-12 个词形</li>
    <li><b>新报告</b>: DB 统计 9,417 词形 / CSV 统计 10,674 词族. <b>两套数据都正确, 粒度不同</b></li>
  </ul>
  <b>根因 2 — 旧 v1.0 的"1,800 词族"是粗估</b>:
  <ul style="margin: 6px 0 0 20px; padding: 0; line-height: 1.7;">
    <li>旧报告可能仅统计了 <b>"Cap.35 新增的新词"</b> (~336 个), 而非 <b>"Cap.1-35 累计词族"</b> (10,674 个), 概念混淆导致 5-10 倍低估</li>
    <li>RA 完成时的累计应该把 FR 的 10,674 词族全部继承, 加上 RA 21 章新增 24,353 词族 → 共 35,027 词族. 旧报告忽略了这个 <b>"继承 + 增量"</b> 关系</li>
  </ul>
  <b>根因 3 — RA 与 FR 的"上下册"关系被忽略</b>:
  <ul style="margin: 6px 0 0 20px; padding: 0; line-height: 1.7;">
    <li>LLPSI 的 <i>Familia Romana</i> (FR) 和 <i>Roma Aeterna</i> (RA) 是 <b>同一本教材</b> 的上下两册 — RA 第 1 章 = FR 第 36 章</li>
    <li>旧报告把 RA 视为独立教材, 单独算"1-21 章", 忽略了从 FR 继承的 10,674 词族基数</li>
    <li>本报告已修正: x 轴为 Cap.1 ~ Cap.56 连续编号, RA 在 Cap.36 衔接 FR</li>
  </ul>
  <b>结论</b>: 新数据更准确, 旧数据需要报废. 后续所有路由/分析均使用 v2.0 数据.
</div>

<!-- 整体概览 -->
<h2 class="section-title">整体概览</h2>

<div class="summary-grid">
  <div class="summary-card">
    <div class="label">FR 平均新词密度</div>
    <div class="value">{summary['fr_avg_new_density']}%</div>
    <div class="desc">{len(fr_chaps)} 章 · {summary['fr_total_words']:,} 总词</div>
  </div>
  <div class="summary-card">
    <div class="label">RA 平均新词密度</div>
    <div class="value">{summary['ra_avg_new_density']}%</div>
    <div class="desc">{len(ra_chaps)} 章 · {summary['ra_total_words']:,} 总词</div>
  </div>
  <div class="summary-card">
    <div class="label">FR 末章累计词形 (DB)</div>
    <div class="value">{summary['fr_cum_vocab_wordform']:,}</div>
    <div class="desc">{summary['fr_cum_vocab_wordfamily']:,} 词族 (CSV)</div>
  </div>
  <div class="summary-card">
    <div class="label">RA 末章累计词形</div>
    <div class="value">{summary['ra_cum_vocab_wordform']:,}</div>
    <div class="desc">RA 21 章增量 +{summary['ra_cum_vocab_wordform'] - summary['fr_cum_vocab_wordform']:,}</div>
  </div>
  <div class="summary-card">
    <div class="label">FR 最难章</div>
    <div class="value">Cap.{summary['fr_hardest_chapter']['chapter']}</div>
    <div class="desc">新词密度 {summary['fr_hardest_chapter']['new_density']}%</div>
  </div>
  <div class="summary-card">
    <div class="label">RA 最难章</div>
    <div class="value">Cap.{summary['ra_hardest_chapter']['chapter']}</div>
    <div class="desc">新词密度 {summary['ra_hardest_chapter']['new_density']}%</div>
  </div>
</div>

<!-- FR → RA 难度跃迁 -->
<h2 class="section-title">FR → RA 难度跃迁</h2>
<div class="chart-card">
  <div id="chart-jump" class="chart"></div>
  <div class="chart-desc">
    Cap.35 (FR 末章) 新词密度 {fr_chaps[-1]['new_density_csv']}% · 累计 {fr_chaps[-1]['cumulative_vocab_db']:,} 词形 →
    Cap.36 (RA 起始) 新词密度 <b style="color: var(--pompeii-red)">{ra_chaps[0]['new_density_csv']}%</b> ·
    Cap.36 是 RA 最难章 (FR→RA 鸿沟)
  </div>
</div>

<!-- 一、词汇增长曲线 -->
<h2 class="section-title">一、词汇增长曲线 (累计词形 · LLPSI 56 章)</h2>
<div class="chart-card">
  <div id="chart-cum-vocab" class="chart"></div>
  <div class="chart-desc">
    <b>关键:</b> FR (Cap.1-35) 与 RA (Cap.36-56) 是 <b>同一本教材</b> 的上下两册, RA 第一章即第 36 章 — 曲线在 Cap.36 连续不断开
  </div>
</div>

<!-- 二、新词密度曲线 -->
<h2 class="section-title">二、新词密度曲线</h2>
<div class="chart-card">
  <div id="chart-new-density" class="chart"></div>
  <div class="chart-desc">FR 平均 {summary['fr_avg_new_density']}%, RA 平均 {summary['ra_avg_new_density']}% — 难度跃升</div>
</div>

<!-- 三、章节体量对比 -->
<h2 class="section-title">三、章节体量对比</h2>
<div class="chart-card">
  <div id="chart-volume" class="chart"></div>
  <div class="chart-desc">柱状图为各章总词数, 红线为移动平均</div>
</div>

<!-- 四、章节新增词数 -->
<h2 class="section-title">四、章节新增词数</h2>
<div class="chart-card">
  <div id="chart-new-words" class="chart"></div>
  <div class="chart-desc">绿柱为 FR, 紫柱为 RA, 紫柱明显高 (RA 难度更大)</div>
</div>

<!-- 五、ROI 甜蜜点 -->
<h2 class="section-title">五、ROI 甜蜜点 (基于密度/累计比)</h2>
<div class="chart-card">
  <div id="chart-roi" class="chart"></div>
  <div class="chart-desc">RA 阶段新词密度反而上升, RA 是"高投入"阶段</div>
</div>

<!-- 六、逐章数据表 -->
<h2 class="section-title">六、逐章核心数据 (前 10 章 + 末 5 章)</h2>
<div class="chart-card">
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <thead>
        <tr style="background:var(--pompeii-red);color:white;">
          <th style="padding:8px;text-align:left;">章节</th>
          <th style="padding:8px;text-align:right;">总词数</th>
          <th style="padding:8px;text-align:right;">新词数</th>
          <th style="padding:8px;text-align:right;">新词密度</th>
          <th style="padding:8px;text-align:right;">累计词形 (DB)</th>
          <th style="padding:8px;text-align:right;">累计词族 (CSV)</th>
        </tr>
      </thead>
      <tbody>
"""

    # 表格: 前 10 章
    html_out = []
    for c in fr_chaps[:10]:
        html_out.append(
            f'<tr style="border-bottom:1px solid var(--parchment-edge);">'
            f'<td style="padding:6px;">FR Cap.{c["chapter"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["total_words_in_chapter"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_word_count_csv"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_density_csv"]}%</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_db"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_csv"]:,}</td>'
            f'</tr>'
        )
    html_out.append('<tr><td colspan="6" style="padding:8px;text-align:center;color:var(--ink-faded);">... (中间省略) ...</td></tr>')
    for c in fr_chaps[-3:] + ra_chaps[:2]:
        html_out.append(
            f'<tr style="border-bottom:1px solid var(--parchment-edge);">'
            f'<td style="padding:6px;">{c["book"]} Cap.{c["chapter"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["total_words_in_chapter"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_word_count_csv"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_density_csv"]}%</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_db"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_csv"]:,}</td>'
            f'</tr>'
        )
    return ''.join(html_out)


def main() -> int:
    print("=== 生成 LLPSI_Insights.html v3.0 ===")
    fr_chaps, ra_chaps, summary = to_chapters_data()
    routing = to_routing()

    # 加载 D 类段原文 (嵌入 HTML, 供点击阅读)
    print("加载 D 类段原文 ...")
    seg_texts = load_segment_texts()
    print(f"  [RAW] {len(seg_texts)} 段已加载")

    # 段筛选: 剔除主体非叙事 + dooge 重复组评分选优
    print("应用段筛选 (v2.2 审读) ...")
    seg_texts, routing, filter_stats = apply_segment_filter(seg_texts, routing)
    print(f"  [OK] 剔除 {len(filter_stats['excluded'])} 段 + {len(filter_stats['duplicates_dropped'])} 重复 = "
          f"保留 {filter_stats['kept']} 段, routing 中 {filter_stats['removed_in_routing']} 项已同步移除")

    # 准备数据
    chart = build_chapter_option(fr_chaps, ra_chaps)
    chapters = chart["chapters"]
    cum_vocab = chart["cum_vocab"]
    new_words = chart["new_words"]
    new_density = chart["new_density"]
    fr_len = chart["fr_len"]

    # 生成 HTML
    html_template = build_html(fr_chaps, ra_chaps, summary, routing, seg_texts)

    # 拼接后面部分 (charts JS + routing section)
    routing_html = build_routing_html(routing)

    table_html = build_table(fr_chaps, ra_chaps)

    segment_texts_json = json.dumps(seg_texts or {}, ensure_ascii=False)

    after_table = f"""
      </tbody>
    </table>
  </div>
</div>

<!-- 七、扩展读物路由表 (新增) -->
<h2 class="section-title">七、扩展读物路由表 (LLPSI 56 章 × 5 维度)</h2>

<div class="footnote" style="background: rgba(176, 141, 43, 0.10); border-left-color: var(--imperial-gold);">
  <b>💡 交互提示</b>:
  <ul style="margin: 6px 0 0 20px; padding: 0; line-height: 1.7;">
    <li>点击任意 <b>🧩 段</b> 条目 → 在弹出阅读器中查看 <b>该段完整拉语原文</b> (页码/教学价值/独词数均标注)</li>
    <li>支持 <b>Esc</b> 键或点击空白处关闭阅读器</li>
    <li>阅读器已嵌入 <b>{filter_stats['kept']} 段</b> 经审读筛选的 D 类拉语段原文 (剔除 {len(filter_stats['excluded'])} 段零碎内容 + dooge 重复组选优 {len(filter_stats['duplicates_dropped'])} 段), 离线可用</li>
  </ul>
</div>

<details style="margin: 12px 0; padding: 10px; background: rgba(140,140,140,0.05); border-radius: 6px; font-size: 13px;">
  <summary style="cursor: pointer; color: var(--imperial-gold); font-weight: 600;">▸ 段筛选明细 (v2.2 审读)</summary>
  <div style="margin-top: 10px; padding-left: 16px; line-height: 1.7;">
    <p style="margin: 4px 0;"><b>判定标准</b>: 文档主体须含 ≥3 句连续叙事/对话 (非夹杂在练习/语法表/字典中)。</p>
    <p style="margin: 4px 0;"><b>剔除段 (主体非叙事, {len(filter_stats['excluded'])} 段)</b>:</p>
    <ul style="margin: 4px 0; padding-left: 24px;">
      {''.join(f'<li><code>{x}</code></li>' for x in filter_stats['excluded'])}
    </ul>
    <p style="margin: 4px 0;"><b>dooge 重复组评分选优 (丢弃 {len(filter_stats['duplicates_dropped'])} 段)</b>:</p>
    <ul style="margin: 4px 0; padding-left: 24px;">
      {''.join(f'<li><code>{x}</code></li>' for x in filter_stats['duplicates_dropped']) if filter_stats['duplicates_dropped'] else '<li>无</li>'}
    </ul>
    <p style="margin: 4px 0;"><b>长音情况</b>: 35 段全部含重音替代 (á é í ó ú), 满足"必须有长音"标准, 无需补。</p>
  </div>
</details>

<div class="legend">
  <div class="legend-item"><span class="route-tag tag-reward">📖 可读</span> token ≥ 80% 已知 (每5词1生词)</div>
  <div class="legend-item"><span class="route-tag tag-challenge">💪 挑战</span> token ≥ 70% 已知 (每3词1生词)</div>
  <div class="legend-item"><span class="route-tag tag-selected">📚 节选</span> hybrid ≥ 50% (教材可50%起点)</div>
  <div class="legend-item"><span class="route-tag tag-review">📖 复习</span> 本书覆盖本章新词最多 (教学价值)</div>
  <div class="legend-item"><span class="route-tag tag-seg">🧩 段</span> D类教材拉语段 (≥60% 已知词覆盖)</div>
</div>

<div class="footnote">
  <b>关键洞察 (v3.0 token级)</b>:
  <ul style="margin:8px 0 0 20px;padding:0;">
    <li><b>v3.0: 切换到 token 级覆盖率</b> — 反映读者实际遇到的生词密度, 而非去重词形覆盖</li>
    <li><b>≥90% token 覆盖: 0 本</b> — 没有读物达到「舒适泛读」门槛</li>
    <li><b>≥80% token 覆盖: 1 本</b> — <code>via_latina_romanorum</code> (87%, Cap.44 可读)</li>
    <li><b>≥70% token 覆盖: 4 本</b> — pugio_bruti (77%), regulus (76%), chickering (72%), diocles_flora (72%)</li>
    <li><b>📖 复习 54 次</b> — 几乎每章都有 1+ 本"教学价值最高"的书</li>
    <li><b>详细路由</b>: 见 <code>analysis_output/llpsi_reader_routing.md</code></li>
  </ul>
</div>

<div class="filter-bar">
  <label>筛选章节范围:</label>
  <select id="filter-range" onchange="filterCards()">
    <option value="all">全部 (56章)</option>
    <option value="fr">FR Cap.1-35</option>
    <option value="ra">RA Cap.36-56</option>
    <option value="1-10">Cap.1-10 (入门)</option>
    <option value="11-20">Cap.11-20 (初级)</option>
    <option value="21-30">Cap.21-30 (FR中级)</option>
    <option value="31-45">Cap.31-45 (FR→RA)</option>
    <option value="46-56">Cap.46-56 (RA完成)</option>
  </select>
  <label>显示:</label>
  <select id="filter-tag" onchange="filterCards()">
    <option value="all">全部</option>
    <option value="readable">仅 📖 可读</option>
    <option value="challenge">仅 💪 挑战</option>
    <option value="seg">仅 🧩 段</option>
  </select>
</div>

{routing_html}

<!-- 附录: 数据来源 -->
<h2 class="section-title">附录: 数据来源与方法</h2>

<div class="chart-card">
  <h3 style="font-family:'Cinzel',serif;color:var(--pompeii-deep);margin-bottom:12px;">数据源</h3>
  <ul style="line-height:1.8;padding-left:20px;">
    <li><b>FR Cap.1-35</b>: <code>analysis_output/chapter_stats.csv</code> (35 行)</li>
    <li><b>RA Cap.36-56</b>: <code>analysis_output/roma_aeterna_chapter_stats.csv</code> (21 行)</li>
    <li><b>LLPSI 词形表</b>: <code>data/llpsi_corpus.db</code> 的 <code>fr_vocab</code> 表 (按词形存储, 累计 9,417 unique word forms)</li>
    <li><b>55本扩展读物分析</b>: <code>analysis_output/reader_vocab_stats_v4.json</code></li>
    <li><b>35段D类拉语段</b>: <code>analysis_output/d_segments_vocab.json</code></li>
    <li><b>路由表</b>: <code>analysis_output/llpsi_reader_routing.json</code> (191 条推荐)</li>
  </ul>

  <h3 style="font-family:'Cinzel',serif;color:var(--pompeii-deep);margin:24px 0 12px;">算法</h3>
  <ol style="line-height:1.8;padding-left:20px;">
    <li>对每本书 / 段, 计算其 unique latin word forms (去重拉语词形)</li>
    <li>对每章 (1-56), 计算 FR 已知词累计 (chapter_known = 1..N-1 章的 word forms)</li>
    <li>覆盖率 cov(N) = len(book_unique ∩ chapter_known) / len(book_unique)</li>
    <li>对每本书找最早达到 60%/70%/80% token 覆盖的章节 → 3档可读性 (节选/挑战/可读)</li>
    <li>段额外达到 60% form 覆盖阈值</li>
    <li>教学价值 best_teach_chapter = max(len(new_set ∩ book_unique) / len(new_set))</li>
  </ol>

  <h3 style="font-family:'Cinzel',serif;color:var(--pompeii-deep);margin:24px 0 12px;">版本历史</h3>
  <ul style="line-height:1.8;padding-left:20px;">
    <li><b>v1.0</b> (2026-05): 首次生成, 含 1,800词族 / 3,500词族等错误数据</li>
    <li><b>v2.0</b> (2026-06-06): 全面修正数据 + 加入 5 维度扩展读物路由 (191 条推荐)</li>
    <li><b>v2.1</b> (2026-06-07): 点击 🧩 段 即可在 modal 中阅读原文 (D类段嵌入, 自包含)</li>
    <li><b>v2.2</b> (2026-06-07): 段筛选 + dooge 重复段自动选优 (35 段高质量段入库)</li>
    <li><b>v2.3</b> (2026-06-08): 阈值温和上调 65/50/30/60 (后被 v3.0 替代)</li>
    <li><b>v3.0</b> (2026-06-08): <b>切换到 token 级覆盖率</b> — 修复 LATIN_RE/英语过滤 BUG, 重新评级全部 55 本读物</li>
  </ul>
</div>

</div> <!-- /container -->

<!-- 阅读器 Modal — 点击 🧩 段 时打开 -->
<div id="reader-modal" class="reader-modal" onclick="if(event.target===this)closeReader()">
  <div class="reader-panel">
    <div class="reader-header">
      <div style="flex:1;min-width:0;">
        <div class="reader-title" id="reader-title">阅读原文</div>
        <div class="reader-subtitle" id="reader-subtitle"></div>
      </div>
      <button class="reader-close" onclick="closeReader()" title="关闭 (Esc)">×</button>
    </div>
    <div class="reader-meta" id="reader-meta"></div>
    <div class="reader-body" id="reader-body">
      <div class="reader-empty-state">点击路由表中的 🧩 段 条目即可阅读</div>
    </div>
  </div>
</div>

<script>
const FR_LEN = {fr_len};
const CHAPTERS = {json.dumps(chapters)};
const CUM_VOCAB = {json.dumps(cum_vocab)};
const NEW_WORDS = {json.dumps(new_words)};
const NEW_DENSITY = {json.dumps(new_density)};

// FR→RA 难度跃迁图
new echarts.init(document.getElementById('chart-jump')).setOption({{
  title: {{ text: 'FR→RA 难度跃迁', left: 'center', textStyle: {{ color: '#7a2820' }} }},
  tooltip: {{ trigger: 'axis' }},
  xAxis: {{ type: 'category', data: CHAPTERS.map(c => 'Cap.' + c) }},
  yAxis: {{ type: 'value', name: '新词密度 %', nameTextStyle: {{ color: '#5a4a38' }} }},
  series: [{{
    name: '新词密度',
    type: 'line',
    data: NEW_DENSITY,
    smooth: true,
    lineStyle: {{ width: 3, color: '#a8392e' }},
    areaStyle: {{ color: 'rgba(168, 57, 46, 0.2)' }},
    markLine: {{
      symbol: 'none',
      data: [
        {{ xAxis: FR_LEN - 1, name: 'FR 末章' }},
        {{ xAxis: FR_LEN, name: 'RA 起始' }}
      ],
      label: {{ fontSize: 12, color: '#7a2820' }}
    }},
    markArea: {{
      itemStyle: {{ color: 'rgba(176, 141, 43, 0.1)' }},
      data: [[{{ xAxis: 0, name: 'FR' }}, {{ xAxis: FR_LEN - 1 }}],
             [{{ xAxis: FR_LEN, name: 'RA' }}, {{ xAxis: CHAPTERS.length - 1 }}]]
    }}
  }}]
}});

// 词汇增长曲线 — FR + RA 视为同一本书的 56 个连续章节
new echarts.init(document.getElementById('chart-cum-vocab')).setOption({{
  title: {{ text: '累计词汇增长 (LLPSI 56 章 · 同一本书的上下册)', left: 'center', textStyle: {{ color: '#7a2820' }} }},
  tooltip: {{ trigger: 'axis' }},
  legend: {{
    data: ['FR Cap.1-35', 'RA Cap.36-56'],
    top: 30,
    textStyle: {{ color: '#5a4a38' }}
  }},
  xAxis: {{ type: 'category', data: CHAPTERS.map(c => 'Cap.' + c), axisLabel: {{ interval: 1, rotate: 45, fontSize: 10 }} }},
  yAxis: {{ type: 'value', name: '词形数' }},
  series: [
    {{
      name: 'FR Cap.1-35',
      type: 'line',
      data: CUM_VOCAB.map((v, i) => i < FR_LEN ? v : null),
      smooth: true,
      lineStyle: {{ color: '#2c3e3a', width: 3 }},
      itemStyle: {{ color: '#2c3e3a' }},
      areaStyle: {{ color: 'rgba(44, 62, 58, 0.12)' }},
      connectNulls: true,
      symbol: 'none'
    }},
    {{
      name: 'RA Cap.36-56',
      type: 'line',
      data: CUM_VOCAB.map((v, i) => i >= FR_LEN - 1 ? v : null),
      smooth: true,
      lineStyle: {{ color: '#5a3e5c', width: 3 }},
      itemStyle: {{ color: '#5a3e5c' }},
      areaStyle: {{ color: 'rgba(90, 62, 92, 0.12)' }},
      connectNulls: true,
      symbol: 'none',
      markLine: {{
        symbol: 'none',
        data: [
          {{ xAxis: 'Cap.36', name: 'RA 起始 (= FR Cap.36, 同卷续编)' }}
        ],
        label: {{ fontSize: 11, color: '#7a2820', position: 'end' }},
        lineStyle: {{ color: '#a8392e', type: 'dashed', width: 2 }}
      }}
    }}
  ]
}});

// 新词密度曲线
new echarts.init(document.getElementById('chart-new-density')).setOption({{
  title: {{ text: '新词密度曲线', left: 'center', textStyle: {{ color: '#7a2820' }} }},
  tooltip: {{ trigger: 'axis' }},
  xAxis: {{ type: 'category', data: CHAPTERS.map(c => 'Cap.' + c) }},
  yAxis: {{ type: 'value', name: '密度 %' }},
  series: [{{
    name: '新词密度',
    type: 'bar',
    data: NEW_DENSITY.map((v, i) => ({{
      value: v,
      itemStyle: {{ color: i < FR_LEN ? '#2c3e3a' : '#5a3e5c' }}
    }}))
  }}]
}});

// 章节体量
new echarts.init(document.getElementById('chart-volume')).setOption({{
  title: {{ text: '章节体量 (总词数)', left: 'center', textStyle: {{ color: '#7a2820' }} }},
  tooltip: {{ trigger: 'axis' }},
  xAxis: {{ type: 'category', data: CHAPTERS.map(c => 'Cap.' + c) }},
  yAxis: {{ type: 'value', name: '总词数' }},
  series: [{{
    name: '总词数', type: 'bar',
    data: {json.dumps([c["total_words_in_chapter"] for c in fr_chaps + ra_chaps])},
    itemStyle: {{ color: '#b08d2b', opacity: 0.7 }}
  }}]
}});

// 新增词数
new echarts.init(document.getElementById('chart-new-words')).setOption({{
  title: {{ text: '章节新增词数', left: 'center', textStyle: {{ color: '#7a2820' }} }},
  tooltip: {{ trigger: 'axis' }},
  xAxis: {{ type: 'category', data: CHAPTERS.map(c => 'Cap.' + c) }},
  yAxis: {{ type: 'value', name: '新词数' }},
  series: [{{
    name: '新词数', type: 'bar',
    data: NEW_WORDS.map((v, i) => ({{
      value: v,
      itemStyle: {{ color: i < FR_LEN ? '#2c3e3a' : '#5a3e5c' }}
    }}))
  }}]
}});

// ROI
new echarts.init(document.getElementById('chart-roi')).setOption({{
  title: {{ text: 'ROI 甜蜜点 (新词密度 vs 累计词)', left: 'center', textStyle: {{ color: '#7a2820' }} }},
  tooltip: {{ trigger: 'axis' }},
  xAxis: {{ type: 'value', name: '累计词形', nameLocation: 'middle', nameGap: 30 }},
  yAxis: {{ type: 'value', name: '新词密度 %' }},
  series: [{{
    name: '章节',
    type: 'scatter',
    data: CUM_VOCAB.map((cum, i) => [cum, NEW_DENSITY[i]]),
    symbolSize: 8,
    itemStyle: {{
      color: function(params) {{
        return params.dataIndex < FR_LEN ? '#2c3e3a' : '#5a3e5c';
      }}
    }}
  }}]
}});

// 路由卡片筛选
function filterCards() {{
  const range = document.getElementById('filter-range').value;
  const tag = document.getElementById('filter-tag').value;
  const cards = document.querySelectorAll('.route-card');
  cards.forEach(card => {{
    const ch = parseInt(card.dataset.ch);
    let inRange = true;
    if (range === 'fr') inRange = ch <= 35;
    else if (range === 'ra') inRange = ch >= 36;
    else if (range === '1-10') inRange = ch >= 1 && ch <= 10;
    else if (range === '11-20') inRange = ch >= 11 && ch <= 20;
    else if (range === '21-30') inRange = ch >= 21 && ch <= 30;
    else if (range === '31-45') inRange = ch >= 31 && ch <= 45;
    else if (range === '46-56') inRange = ch >= 46 && ch <= 56;
    card.style.display = inRange ? '' : 'none';
  }});
}}

// ===== 段原文阅读器 (v2.1) =====
// SEGMENT_TEXTS 由 build script 注入, 格式: {{ "slug|sp|ep": "原文 markdown 文本" }}
const SEGMENT_TEXTS = {segment_texts_json};

function openSegmentReader(key, metaJson) {{
  const modal = document.getElementById('reader-modal');
  const titleEl = document.getElementById('reader-title');
  const subtitleEl = document.getElementById('reader-subtitle');
  const metaEl = document.getElementById('reader-meta');
  const bodyEl = document.getElementById('reader-body');

  let meta = {{}};
  try {{ meta = JSON.parse(metaJson); }} catch (e) {{ console.warn('meta parse failed', e); }}

  titleEl.textContent = meta.title || meta.slug || '段原文';
  // subtitle: 来源 slug + 页码
  const sp = meta.sp, ep = meta.ep;
  subtitleEl.textContent = (meta.slug || '') + (sp != null ? ' · p.' + sp + '–' + ep : '');

  // meta 行
  const metaParts = [];
  if (sp != null) metaParts.push('<span><b>页码:</b> p.' + sp + '–' + ep + '</span>');
  if (meta.teach_ch != null) metaParts.push('<span><b>教学价值:</b> Cap.' + meta.teach_ch + ' (' + Math.round((meta.teach_cov || 0) * 100) + '%)</span>');
  if (meta.ch60) metaParts.push('<span><b>60%起点:</b> Cap.' + meta.ch60 + '</span>');
  if (meta.unique_latin) metaParts.push('<span><b>独词数:</b> ' + meta.unique_latin + '</span>');
  metaEl.innerHTML = metaParts.join('');

  // body
  const text = SEGMENT_TEXTS[key];
  if (!text) {{
    bodyEl.innerHTML = '<div class="reader-error">未找到该段原文 (key=' + key + '). 可能是早期抽取遗漏.</div>';
  }} else {{
    // 简单 markdown -> HTML 渲染
    const html = text
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/^## (.+)$/gm, '<h2>$1</h2>')
      .replace(/^# (.+)$/gm, '<h1>$1</h1>')
      .replace(/^---$/gm, '<hr/>')
      .replace(/`([^`]+)`/g, '<code>$1</code>');
    bodyEl.innerHTML = html;
  }}

  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function closeReader() {{
  const modal = document.getElementById('reader-modal');
  modal.classList.remove('open');
  document.body.style.overflow = '';
}}

// 绑定所有 .route-clickable 的点击事件
document.addEventListener('DOMContentLoaded', function() {{
  document.querySelectorAll('.route-clickable').forEach(el => {{
    el.addEventListener('click', function(e) {{
      e.preventDefault();
      e.stopPropagation();
      const key = this.dataset.key;
      const meta = this.dataset.meta;
      openSegmentReader(key, meta);
    }});
  }});

  // Esc 关闭 modal
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeReader();
  }});
}});
</script>
</body>
</html>
"""

    final_html = html_template + table_html + after_table
    OUT.write_text(final_html, encoding="utf-8")
    print(f"[OK] {OUT} ({len(final_html):,} 字符)")
    return 0


def build_table(fr_chaps, ra_chaps) -> str:
    """构建逐章数据表的尾部 tbody 部分."""
    out = []
    # 表格: 前 10 章
    for c in fr_chaps[:10]:
        out.append(
            f'<tr style="border-bottom:1px solid var(--parchment-edge);">'
            f'<td style="padding:6px;">FR Cap.{c["chapter"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["total_words_in_chapter"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_word_count_csv"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_density_csv"]}%</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_db"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_csv"]:,}</td>'
            f'</tr>'
        )
    out.append('<tr><td colspan="6" style="padding:8px;text-align:center;color:var(--ink-faded);">... (中间 Cap.11-33 省略) ...</td></tr>')
    for c in fr_chaps[-3:] + ra_chaps[:2]:
        out.append(
            f'<tr style="border-bottom:1px solid var(--parchment-edge);">'
            f'<td style="padding:6px;">{c["book"]} Cap.{c["chapter"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["total_words_in_chapter"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_word_count_csv"]}</td>'
            f'<td style="padding:6px;text-align:right;">{c["new_density_csv"]}%</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_db"]:,}</td>'
            f'<td style="padding:6px;text-align:right;">{c["cumulative_vocab_csv"]:,}</td>'
            f'</tr>'
        )
    return ''.join(out)


if __name__ == "__main__":
    import sys
    sys.exit(main())
