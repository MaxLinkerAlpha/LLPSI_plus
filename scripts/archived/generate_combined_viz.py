#!/usr/bin/env python3
"""
生成 LLPSI FR + RA 合并的难度曲线 HTML 可视化
=====================================================
基于 analysis_output/combined_long.csv 数据,
生成包含两册数据的难度曲线、新词密度、累计词汇等图表。
"""

import csv
import argparse
import os


def load_combined(csv_path: str) -> list[dict]:
    """读取长格式合并 CSV"""
    data = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 从 chapter_label (如 "FR Cap. 1" 或 "RA Cap. 36") 中提取章节号
            label = row["chapter_label"]
            num = int(label.split("Cap.")[-1].strip())
            data.append({
                "book": row["book"],
                "chapter": num,
                "label": label,
                "total_tokens": int(row["total_tokens"]),
                "new_words": int(row["new_words"]),
                "new_density": float(row["new_density"]),
                "cumulative_vocab": int(row["cumulative_vocab"]),
            })
    return data


def classify_density(density: float, avg: float) -> tuple[str, str]:
    """根据密度分类"""
    if density > avg * 1.5:
        return ("steep", "陡坡")
    elif density > avg * 1.2:
        return ("caution", "注意")
    elif density < avg * 0.6:
        return ("gentle", "平缓")
    else:
        return ("normal", "正常")


def build_chapter_data_js(combined: list[dict]) -> str:
    """构建 JS 数组,用于 ECharts 数据绑定"""
    avg = sum(c["new_density"] for c in combined) / len(combined)
    lines = ["const chapterData = ["]
    for c in combined:
        rating, label = classify_density(c["new_density"], avg)
        lines.append(
            f"  ['{c['book']}', {c['chapter']}, {c['total_tokens']}, "
            f"{c['new_words']}, {c['new_density']:.1f}, {c['cumulative_vocab']}, "
            f"'{rating}', '{label}'],"
        )
    lines.append("];")
    lines.append(f"const avgDensity = {avg:.2f};")
    return "\n".join(lines)


# ============================================================
# ROI 甜蜜点 (基于 vocabulary_threshold_research.md v2.0.0)
# 词族 (word family) ≈ 词形 (word form) / 5~6 (经验比)
# ============================================================
ROI_TIERS = [
    # (tier 标签, 词族数, 覆盖率%, 颜色, 含义)
    ("Tier 0",  100,  50, "#9ca3af", "数学 ROI 峰值 (不可达)"),
    ("Tier 1",  1000, 72, "#b08d2b", "入门门槛"),
    ("Tier 2 ★", 2000, 80, "#a8392e", "★ 实用最优甜蜜点"),
    ("Tier 3",  3500, 85, "#7a2820", "RA 完成 / 一般对话"),
    ("Tier 4",  6000, 95, "#5a3e5c", "独立听力"),
    ("Tier 5",  8000, 98, "#2c3e3a", "独立阅读 (学术)"),
]
# 词形/词族 转换系数 (基于实际数据: FR Cap. 35 累计 10,675 词形 ≈ 1,800 词族)
# 来源: vocabulary_threshold_research.md "FR 完成 = 1,800 词族 ≈ 甜蜜点"
# 校准: 10,675 / 1,800 ≈ 5.93 (1 词族 ≈ 5.93 词形)
FORM_TO_FAMILY = 5.93


def family_to_forms(family_count: int) -> int:
    return int(family_count * FORM_TO_FAMILY)


def find_sweet_spot_chapter(combined: list[dict], target_forms: int) -> dict | None:
    """找到累计词形首次>= target_forms 的章节"""
    for c in combined:
        if c["cumulative_vocab"] >= target_forms:
            return c
    return None


def generate_html(combined: list[dict], output_path: str):
    """生成 HTML 文件"""
    chapter_data_js = build_chapter_data_js(combined)
    fr_data = [c for c in combined if c["book"] == "FR"]
    ra_data = [c for c in combined if c["book"] == "RA"]

    # 找出 FR->RA 跃迁点
    fr_last = fr_data[-1] if fr_data else None
    ra_first = ra_data[0] if ra_data else None

    # 找出 Top 5 陡坡章节
    sorted_data = sorted(combined, key=lambda c: -c["new_density"])
    top5 = sorted_data[:5]

    avg = sum(c["new_density"] for c in combined) / len(combined)
    fr_avg = sum(c["new_density"] for c in fr_data) / len(fr_data) if fr_data else 0
    ra_avg = sum(c["new_density"] for c in ra_data) / len(ra_data) if ra_data else 0

    # ROI 甜蜜点对应章节
    sweet_spot_forms = family_to_forms(2000)  # ~11,000 词形
    sweet_spot_ch = find_sweet_spot_chapter(combined, sweet_spot_forms)
    sweet_spot_str = (
        f"{sweet_spot_ch['book']} Cap. {sweet_spot_ch['chapter']}"
        if sweet_spot_ch else "—"
    )
    # 每个 ROI tier 对应章节
    tier_chapters = {}
    for tier_name, family_count, _cov, _color, _desc in ROI_TIERS:
        target_forms = family_to_forms(family_count)
        ch = find_sweet_spot_chapter(combined, target_forms)
        tier_chapters[tier_name] = (ch, target_forms)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LLPSI · FR + RA 难度曲线与数据洞察</title>
<meta name="description" content="A visual analysis of vocabulary density and growth across Familia Romana and Roma Aeterna, the two core books of Lingua Latina per se Illustrata.">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;800&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Cormorant+Infant:ital,wght@0,400;0,500;0,600;1,400&family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">

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
  font-family: 'Cormorant Garamond', 'Noto Serif SC', 'Source Han Serif SC', serif;
  font-size: 18px;
  line-height: 1.7;
  color: var(--ink);
  background-color: var(--parchment);
  background-image:
    radial-gradient(ellipse at top left, rgba(176, 141, 43, 0.08), transparent 50%),
    radial-gradient(ellipse at bottom right, rgba(168, 57, 46, 0.06), transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(122, 40, 32, 0.04), transparent 30%),
    radial-gradient(circle at 80% 20%, rgba(44, 62, 58, 0.04), transparent 30%);
  min-height: 100vh;
  overflow-x: hidden;
}}

body::before {{
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background-image:
    repeating-linear-gradient(0deg, transparent 0, transparent 3px, rgba(122, 40, 32, 0.012) 3px, rgba(122, 40, 32, 0.012) 4px),
    repeating-linear-gradient(90deg, transparent 0, transparent 5px, rgba(28, 22, 18, 0.008) 5px, rgba(28, 22, 18, 0.008) 6px);
}}

body::after {{
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background:
    radial-gradient(ellipse at top left, var(--parchment-edge) 0%, transparent 25%),
    radial-gradient(ellipse at top right, var(--parchment-edge) 0%, transparent 25%),
    radial-gradient(ellipse at bottom left, var(--parchment-edge) 0%, transparent 25%),
    radial-gradient(ellipse at bottom right, var(--parchment-edge) 0%, transparent 25%);
  opacity: 0.25;
  mix-blend-mode: multiply;
}}

.page-frame {{
  position: relative;
  z-index: 2;
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 60px;
}}

main, header, footer {{ position: relative; z-index: 2; }}
section {{ margin-bottom: 100px; }}

/* HERO */
.hero {{ padding: 80px 0 60px; text-align: center; }}
.hero-ornament {{
  font-family: 'Cinzel', serif;
  font-size: 0.95rem;
  letter-spacing: 0.4em;
  color: var(--pompeii-red);
  margin-bottom: 24px;
  font-weight: 500;
}}
.hero-ornament .dot {{ color: var(--imperial-gold); margin: 0 0.5em; }}
.hero-spqr {{
  display: inline-block;
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  letter-spacing: 0.6em;
  color: var(--ink-soft);
  border: 1.5px solid var(--ink-soft);
  padding: 8px 28px;
  margin-bottom: 30px;
}}
.hero h1 {{
  font-family: 'Cinzel', serif;
  font-size: 3.6rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 8px;
  letter-spacing: 0.05em;
  line-height: 1.15;
}}
.hero .subtitle {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 1.4rem;
  color: var(--ink-soft);
  margin-bottom: 30px;
}}
.hero .meta {{
  font-family: 'Cormorant Infant', serif;
  font-size: 1.05rem;
  color: var(--ink-faded);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}}
.hero .meta .dot {{ color: var(--imperial-gold); margin: 0 1em; }}

/* SECTIONS */
.section-title {{
  font-family: 'Cinzel', serif;
  font-size: 2.2rem;
  color: var(--ink);
  text-align: center;
  margin-bottom: 12px;
  font-weight: 600;
  letter-spacing: 0.03em;
}}
.section-subtitle {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-size: 1.1rem;
  color: var(--ink-faded);
  text-align: center;
  margin-bottom: 40px;
}}
.divider {{
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--imperial-gold), transparent);
  margin: 0 auto 40px;
}}

/* CARDS */
.cards {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 50px;
}}
.card {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  border-left: 4px solid var(--imperial-gold);
  padding: 24px 28px;
  box-shadow: 0 2px 8px var(--shadow);
  position: relative;
}}
.card.fr {{ border-left-color: var(--roman-green); }}
.card.ra {{ border-left-color: var(--tyrian-purple); }}
.card.combined {{ border-left-color: var(--pompeii-red); }}
.card .label {{
  font-family: 'Cinzel', serif;
  font-size: 0.85rem;
  letter-spacing: 0.2em;
  color: var(--ink-faded);
  text-transform: uppercase;
  margin-bottom: 8px;
}}
.card .value {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.4rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.1;
}}
.card .unit {{
  font-size: 1.1rem;
  color: var(--ink-soft);
  font-weight: 400;
  margin-left: 4px;
}}
.card .desc {{
  font-size: 0.95rem;
  color: var(--ink-soft);
  margin-top: 6px;
  font-style: italic;
}}

/* CHART CONTAINERS */
.chart-container {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px var(--shadow);
}}
.chart-title {{
  font-family: 'Cinzel', serif;
  font-size: 1.2rem;
  color: var(--ink);
  margin-bottom: 6px;
  letter-spacing: 0.05em;
}}
.chart-desc {{
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  color: var(--ink-faded);
  font-size: 1rem;
  margin-bottom: 16px;
}}
.chart {{
  width: 100%;
  height: 460px;
}}
.chart.tall {{ height: 560px; }}

/* TABLE */
table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--marble-light);
  font-family: 'Cormorant Infant', serif;
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--parchment-edge);
}}
thead {{
  background: var(--ink-soft);
  color: var(--marble-light);
}}
thead th {{
  font-family: 'Cinzel', serif;
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  padding: 14px 10px;
  text-align: left;
  font-weight: 600;
}}
tbody td {{
  padding: 12px 10px;
  border-bottom: 1px solid var(--parchment-edge);
  font-size: 1rem;
}}
tbody tr.steep {{
  background: rgba(168, 57, 46, 0.06);
}}
tbody tr:hover {{
  background: rgba(176, 141, 43, 0.08);
}}
.book-tag {{
  display: inline-block;
  font-family: 'Cinzel', serif;
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  padding: 2px 8px;
  margin-right: 4px;
  color: var(--marble-light);
  vertical-align: middle;
}}
.book-tag.fr {{ background: var(--roman-green); }}
.book-tag.ra {{ background: var(--tyrian-purple); }}
.rating {{
  display: inline-block;
  padding: 2px 8px;
  font-size: 0.85rem;
  font-family: 'Cinzel', serif;
  letter-spacing: 0.05em;
}}
.rating.steep   {{ background: var(--pompeii-deep); color: var(--marble-light); }}
.rating.caution {{ background: var(--imperial-gold); color: var(--ink); }}
.rating.normal  {{ background: var(--roman-green); color: var(--marble-light); }}
.rating.gentle  {{ background: var(--parchment-edge); color: var(--ink-soft); }}

/* REC GRID */
.rec-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}}
.rec {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  padding: 18px 22px;
  position: relative;
  box-shadow: 0 2px 6px var(--shadow);
}}
.rec.p1 {{ border-left: 4px solid var(--pompeii-deep); }}
.rec.p2 {{ border-left: 4px solid var(--imperial-gold); }}
.rec.p3 {{ border-left: 4px solid var(--roman-green); }}
.rec .rank {{
  font-family: 'Cinzel', serif;
  font-size: 0.85rem;
  color: var(--pompeii-red);
  letter-spacing: 0.1em;
}}
.rec .chapter {{
  font-family: 'Cinzel', serif;
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--ink);
  margin: 4px 0;
}}
.rec .pct {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.8rem;
  color: var(--pompeii-red);
  font-weight: 600;
  margin: 6px 0;
}}
.rec .reason {{
  font-size: 0.95rem;
  color: var(--ink-soft);
  font-style: italic;
}}

/* JUMP BOX */
.jump-box {{
  background: linear-gradient(135deg, var(--marble-light) 0%, var(--parchment-deep) 100%);
  border: 2px solid var(--pompeii-deep);
  padding: 30px 36px;
  margin: 30px 0;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 16px var(--shadow-deep);
}}
.jump-box::before, .jump-box::after {{
  content: '❦';
  position: absolute;
  font-size: 1.5rem;
  color: var(--imperial-gold);
}}
.jump-box::before {{ top: 12px; left: 16px; }}
.jump-box::after {{ bottom: 12px; right: 16px; }}
.jump-box h3 {{
  font-family: 'Cinzel', serif;
  font-size: 1.4rem;
  color: var(--pompeii-deep);
  margin-bottom: 12px;
  letter-spacing: 0.1em;
}}
.jump-box p {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.15rem;
  color: var(--ink-soft);
  line-height: 1.6;
}}
.jump-box .arrow {{
  font-family: 'Cinzel', serif;
  font-size: 2.2rem;
  color: var(--imperial-gold);
  margin: 14px 0;
}}

/* FOOTER */
footer {{
  text-align: center;
  padding: 40px 0;
  font-family: 'Cormorant Infant', serif;
  font-size: 0.95rem;
  color: var(--ink-faded);
  border-top: 1px solid var(--parchment-edge);
  margin-top: 60px;
}}
footer .spqr {{
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  color: var(--pompeii-red);
  letter-spacing: 0.4em;
  margin-bottom: 8px;
}}

/* ROI SWEET SPOT */
.roi-hero {{
  background: linear-gradient(135deg, var(--marble-light) 0%, var(--parchment-deep) 100%);
  border: 2px solid var(--pompeii-deep);
  padding: 36px 40px;
  margin-bottom: 40px;
  text-align: center;
  box-shadow: 0 4px 18px var(--shadow-deep);
  position: relative;
}}
.roi-hero::before, .roi-hero::after {{
  content: '✦';
  position: absolute;
  font-size: 1.6rem;
  color: var(--imperial-gold);
}}
.roi-hero::before {{ top: 14px; left: 18px; }}
.roi-hero::after {{ bottom: 14px; right: 18px; }}
.roi-hero-label {{
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  letter-spacing: 0.3em;
  color: var(--pompeii-red);
  margin-bottom: 12px;
  text-transform: uppercase;
}}
.roi-hero-value {{
  font-family: 'Cinzel', serif;
  font-size: 4.5rem;
  font-weight: 700;
  color: var(--pompeii-deep);
  line-height: 1.1;
  margin-bottom: 14px;
  letter-spacing: 0.02em;
}}
.roi-hero-unit {{
  font-size: 1.6rem;
  color: var(--ink-soft);
  font-weight: 400;
}}
.roi-hero-desc {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.1rem;
  color: var(--ink-soft);
  line-height: 1.7;
  max-width: 720px;
  margin: 0 auto;
}}

.roi-tier {{ border-left-width: 4px; }}
.roi-tier.roi-sweet {{
  border-left-color: var(--pompeii-deep);
  border-left-width: 6px;
  background: linear-gradient(90deg, rgba(168, 57, 46, 0.08) 0%, var(--marble-light) 100%);
  box-shadow: 0 4px 12px rgba(168, 57, 46, 0.15);
}}
.roi-tier.roi-sweet .value {{ color: var(--pompeii-deep); }}
.roi-chapter {{
  font-family: 'Cormorant Infant', serif;
  font-size: 0.9rem;
  color: var(--ink-soft);
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed var(--parchment-edge);
}}

.roi-table-wrap {{
  margin: 30px 0;
  overflow-x: auto;
}}
.roi-table {{
  width: 100%;
  border-collapse: collapse;
  background: var(--marble-light);
  box-shadow: 0 2px 8px var(--shadow);
  border: 1px solid var(--parchment-edge);
}}
.roi-table th {{
  background: var(--ink-soft);
  color: var(--marble-light);
  font-family: 'Cinzel', serif;
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  padding: 12px 10px;
  text-align: left;
  font-weight: 600;
}}
.roi-table td {{
  padding: 11px 10px;
  border-bottom: 1px solid var(--parchment-edge);
  font-family: 'Cormorant Infant', serif;
  font-size: 0.98rem;
}}
.roi-table tr.roi-row-sweet {{
  background: linear-gradient(90deg, rgba(168, 57, 46, 0.08) 0%, rgba(168, 57, 46, 0.02) 100%);
  border-left: 3px solid var(--pompeii-deep);
}}
.roi-table tr.roi-row-sweet td {{ color: var(--ink); }}

.roi-insight {{
  background: var(--marble-light);
  border: 1px solid var(--parchment-edge);
  border-left: 4px solid var(--imperial-gold);
  padding: 24px 30px;
  margin-top: 20px;
  box-shadow: 0 2px 8px var(--shadow);
}}
.roi-insight h3 {{
  font-family: 'Cinzel', serif;
  font-size: 1.1rem;
  color: var(--ink);
  margin-bottom: 12px;
  letter-spacing: 0.05em;
}}
.roi-insight p {{
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.05rem;
  color: var(--ink-soft);
  line-height: 1.7;
  margin-bottom: 10px;
}}
.roi-insight p:last-child {{ margin-bottom: 0; }}
</style>
</head>

<body>
<div class="page-frame">

<header class="hero">
  <div class="hero-ornament">
    <span>LINGUA LATINA</span> <span class="dot">·</span> <span>PER SE ILLVSTRATA</span>
  </div>
  <div class="hero-spqr">SPQR · DATA INSIGHTS</div>
  <h1>FAMILIA ROMANA<br>+<br>ROMA AETERNA</h1>
  <div class="subtitle">A continuous difficulty curve across the 56 chapters of the core curriculum</div>
  <div class="meta">
    <span>{len(fr_data)} CHAPTERS · FAMILIA ROMANA</span>
    <span class="dot">◆</span>
    <span>{len(ra_data)} CHAPTERS · ROMA AETERNA</span>
    <span class="dot">◆</span>
    <span>{len(combined)} CHAPTERS · TOTAL</span>
  </div>
</header>

<main>

<section id="overview">
  <h2 class="section-title">整体概览</h2>
  <div class="divider"></div>
  <div class="section-subtitle">Core metrics across the two books</div>

  <div class="cards">
    <div class="card fr">
      <div class="label">FR · Familia Romana</div>
      <div class="value">{len(fr_data)}<span class="unit">章</span></div>
      <div class="desc">Cap. I — Cap. XXXV</div>
    </div>
    <div class="card ra">
      <div class="label">RA · Roma Aeterna</div>
      <div class="value">{len(ra_data)}<span class="unit">章</span></div>
      <div class="desc">Cap. XXXVI — Cap. LVI</div>
    </div>
    <div class="card combined">
      <div class="label">两册合计</div>
      <div class="value">{len(combined)}<span class="unit">章</span></div>
      <div class="desc">连续 56 课核心课程</div>
    </div>
    <div class="card combined">
      <div class="label">RA 末章累计词汇</div>
      <div class="value">{ra_data[-1]['cumulative_vocab']:,}<span class="unit"></span></div>
      <div class="desc">(含 FR 基线 {fr_data[-1]['cumulative_vocab']:,} 词形)</div>
    </div>
  </div>

  {f'''
  <div class="jump-box">
    <h3>FR → RA 难度跃迁</h3>
    <p>第 35 章(FR 末章)新词密度 <b>{fr_last['new_density']:.1f}%</b> · 累计 {fr_last['cumulative_vocab']:,} 词形</p>
    <div class="arrow">⇣</div>
    <p>第 36 章(RA 起始)新词密度骤升至 <b>{ra_first['new_density']:.1f}%</b> · 本章即涌现 {ra_first['new_words']} 新词</p>
  </div>
  ''' if fr_last and ra_first else ''}

  <div class="cards">
    <div class="card fr">
      <div class="label">FR 平均新词密度</div>
      <div class="value">{fr_avg:.1f}<span class="unit">%</span></div>
      <div class="desc">稳步上升 · 约 25% 峰值</div>
    </div>
    <div class="card ra">
      <div class="label">RA 平均新词密度</div>
      <div class="value">{ra_avg:.1f}<span class="unit">%</span></div>
      <div class="desc">初期高 · 后期回落</div>
    </div>
    <div class="card combined">
      <div class="label">两册平均新词密度</div>
      <div class="value">{avg:.1f}<span class="unit">%</span></div>
      <div class="desc">陡坡阈值 = {avg*1.2:.1f}% (×1.2)</div>
    </div>
  </div>
</section>

<section id="roi-sweet-spot">
  <h2 class="section-title">ROI 甜蜜点 (按投产比分层)</h2>
  <div class="divider"></div>
  <div class="section-subtitle">The "Practical Sweet Spot" · 2,000 词族 (≈ 11,860 词形) · 80% 古典文本覆盖率</div>

  <div class="roi-hero">
    <div class="roi-hero-label">★ 实用最优甜蜜点 ★</div>
    <div class="roi-hero-value">2,000<span class="roi-hero-unit"> 词族</span></div>
    <div class="roi-hero-desc">
      80% 古典文本覆盖率 · 每 5 词仅遇 1 生词 · 边际收益递减前最后的高性价比段<br/>
      <b>在 LLPSI 中: {sweet_spot_str}</b>
      (累计词形 ≈ {sweet_spot_forms:,})
    </div>
  </div>

  <div class="cards">
    {''.join(f'''
    <div class="card roi-tier {('roi-sweet' if '★' in tier_name else '')}">
      <div class="label" style="color: {color}">{tier_name}</div>
      <div class="value">{family:,}<span class="unit"> 词族</span></div>
      <div class="desc">{desc} · 覆盖率 {cov}%</div>
      <div class="roi-chapter">
        {f"对应章节: <b>{ch['book']} Cap. {ch['chapter']}</b>" if ch else "本课程未覆盖"}
      </div>
    </div>
    ''' for tier_name, family, cov, color, desc in ROI_TIERS)}
  </div>

  <div class="roi-table-wrap">
    <table class="roi-table">
      <thead>
        <tr>
          <th>层级</th>
          <th>词族</th>
          <th>对应词形 (×{FORM_TO_FAMILY})</th>
          <th>覆盖率</th>
          <th>LLPSI 章节</th>
          <th>每千词边际收益</th>
          <th>评价</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Tier 0</td>
          <td>100</td>
          <td>~{family_to_forms(100):,}</td>
          <td>50%</td>
          <td>不可达</td>
          <td><b>5.0%</b> (50×)</td>
          <td>数学 ROI 峰值,实用性差</td>
        </tr>
        <tr>
          <td>Tier 1</td>
          <td>1,000</td>
          <td>~{family_to_forms(1000):,}</td>
          <td>72%</td>
          <td>{tier_chapters.get('Tier 1', (None, 0))[0] and f"{tier_chapters['Tier 1'][0]['book']} Cap. {tier_chapters['Tier 1'][0]['chapter']}" or "—"}</td>
          <td>0.4% (4×)</td>
          <td>入门门槛</td>
        </tr>
        <tr class="roi-row-sweet">
          <td><b>★ Tier 2</b></td>
          <td><b>2,000</b></td>
          <td>~{family_to_forms(2000):,}</td>
          <td><b>80%</b></td>
          <td><b>{sweet_spot_str}</b></td>
          <td>0.1% (1× 基准)</td>
          <td><b>★ 实用最优甜蜜点</b></td>
        </tr>
        <tr>
          <td>Tier 3</td>
          <td>3,500</td>
          <td>~{family_to_forms(3500):,}</td>
          <td>85%</td>
          <td>{tier_chapters.get('Tier 3', (None, 0))[0] and f"{tier_chapters['Tier 3'][0]['book']} Cap. {tier_chapters['Tier 3'][0]['chapter']}" or "本课程未覆盖"}</td>
          <td>0.1% (1×)</td>
          <td>RA 完成,边际收益递减</td>
        </tr>
        <tr>
          <td>Tier 4</td>
          <td>6,000</td>
          <td>~{family_to_forms(6000):,}</td>
          <td>95%</td>
          <td>本课程未覆盖</td>
          <td>0.05% (0.5×)</td>
          <td>独立听力门槛</td>
        </tr>
        <tr>
          <td>Tier 5</td>
          <td>8,000</td>
          <td>~{family_to_forms(8000):,}</td>
          <td>98%</td>
          <td>本课程未覆盖</td>
          <td>~0%</td>
          <td>学术独立阅读</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="roi-insight">
    <h3>💡 关键洞察</h3>
    <p>前 100 词 (功能词 + 高频实词) 的边际收益是后续区间的 <b>50 倍</b>。但只学 100 词,你认识一半句子却看不懂任何内容——这就是"数学最优"与"实用最优"的分歧点。</p>
    <p>FR 完成 (Cap. 35) ≈ 1,800 词族,正好踩在甜蜜点;RA 完成 (Cap. 56) ≈ 3,500 词族,已进入边际收益递减区。 <b>对于大多数学习者,FR 完结即甜蜜点</b>,RA 之后的投入是"奢侈品"。</p>
  </div>
</section>

<section id="chart-vocab-growth">
  <h2 class="section-title">一、词汇增长曲线</h2>
  <div class="divider"></div>
  <div class="section-subtitle">Cumulative vocabulary · 从第 1 章到第 56 章的累计词形增长</div>

  <div class="chart-container">
    <div class="chart-title">Cumulative Vocabulary Growth · 累计词汇曲线</div>
    <div class="chart-desc">绿线为 FR(35 章),紫线为 RA(21 章),整体呈 S 形上升</div>
    <div id="growth-chart" class="chart tall"></div>
  </div>
</section>

<section id="chart-density">
  <h2 class="section-title">二、新词密度曲线</h2>
  <div class="divider"></div>
  <div class="section-subtitle">Per-chapter new-word density · 每章新词占本章总词数的比例</div>

  <div class="chart-container">
    <div class="chart-title">New-Word Density · 新词密度</div>
    <div class="chart-desc">虚线 = 平均密度阈值 ({avg:.1f}%);柱体颜色: 暗赭=陡坡,金=注意,绿=正常,米=平缓</div>
    <div id="density-chart" class="chart tall"></div>
  </div>
</section>

<section id="chart-tokens">
  <h2 class="section-title">三、章节体量对比</h2>
  <div class="divider"></div>
  <div class="section-subtitle">Total tokens per chapter · 每章总词数(RA 普遍更长,反映罗马史的复杂度)</div>

  <div class="chart-container">
    <div class="chart-title">Chapter Size · 章节长度</div>
    <div class="chart-desc">柱高 = 章节总词形数;RA 章节平均 {sum(c['total_tokens'] for c in ra_data)//len(ra_data):,} 词,FR 章节平均 {sum(c['total_tokens'] for c in fr_data)//len(fr_data):,} 词</div>
    <div id="tokens-chart" class="chart"></div>
  </div>
</section>

<section id="chart-new-words">
  <h2 class="section-title">四、章节新增词数</h2>
  <div class="divider"></div>
  <div class="section-subtitle">New words per chapter · 每章涌现的全新词形数</div>

  <div class="chart-container">
    <div class="chart-title">New Words Per Chapter · 新增词数</div>
    <div class="chart-desc">RA 起始章节新词激增 (Cap. 36-38 共 {ra_data[0]['new_words']} / {ra_data[1]['new_words']} / {ra_data[2]['new_words']} 词,精确算法),反映罗马史/文学/修辞学新概念大量涌入</div>
    <div id="newwords-chart" class="chart tall"></div>
  </div>
</section>

<section id="chart-book-compare">
  <h2 class="section-title">五、两册难度对比</h2>
  <div class="divider"></div>
  <div class="section-subtitle">FR vs RA · 上下两册关键指标对比</div>

  <div class="chart-container">
    <div class="chart-title">Book-level comparison · 两册对比</div>
    <div class="chart-desc">左侧: 平均新词密度;右侧: 章节平均总词数;下方: 高密度章节数(>阈值)</div>
    <div id="book-compare-chart" class="chart"></div>
  </div>
</section>

<section id="table">
  <h2 class="section-title">六、逐章数据</h2>
  <div class="divider"></div>
  <div class="section-subtitle">Per-chapter data · 全部 {len(combined)} 章节的完整指标</div>

  <table>
    <thead>
      <tr>
        <th>分册</th>
        <th>章节</th>
        <th style="text-align:right">总词数</th>
        <th style="text-align:right">新词数</th>
        <th style="text-align:right">新词密度</th>
        <th>密度条</th>
        <th style="text-align:right">累计词汇</th>
        <th>评级</th>
      </tr>
    </thead>
    <tbody id="chapter-tbody"></tbody>
  </table>
</section>

<section id="recommendations">
  <h2 class="section-title">七、补充阅读优先级</h2>
  <div class="divider"></div>
  <div class="section-subtitle">Top steep chapters · 最需要补充语料的章节</div>
  <div class="rec-grid" id="rec-grid"></div>
</section>

<footer>
  <div class="spqr">SPQR</div>
  <div>LLPSI+++ · Data Insights · 2026</div>
  <div style="margin-top:8px">Data: Familia Romana (Cap. I-XXXV) + Roma Aeterna (Cap. XXXVI-LVI) · OCR processed</div>
</footer>

</main>
</div>

<script>
/* DATA (injected from combined_long.csv) */
{chapter_data_js}

/* COLORS */
const COLORS = {{
  ink: '#1c1612',
  inkSoft: '#3a2f25',
  inkFaded: '#5a4a38',
  parchment: '#f4ecd8',
  marble: '#e8dfc4',
  marbleLight: '#f0e9d2',
  pompeiiRed: '#a8392e',
  pompeiiDeep: '#7a2820',
  imperialGold: '#b08d2b',
  imperialGoldL: '#d4b14a',
  romanGreen: '#2c3e3a',
  romanGreenD: '#1a2823',
  tyrianPurple: '#5a3e5c',
  parchmentDeep: '#ebe0c4',
  parchmentEdge: '#d9c89c',
}};

const SHARED_AXIS = {{
  axisLine: {{ lineStyle: {{ color: COLORS.inkFaded, width: 1 }} }},
  axisTick: {{ lineStyle: {{ color: COLORS.inkFaded }} }},
  axisLabel: {{
    color: COLORS.inkSoft,
    fontFamily: 'Cormorant Infant, serif',
    fontSize: 12,
  }},
  splitLine: {{
    lineStyle: {{ color: COLORS.parchmentEdge, type: 'dashed', opacity: 0.5 }}
  }}
}};

/* ============================================================
   CHART 1: Cumulative Vocab Growth
   ============================================================ */
const growthChart = echarts.init(document.getElementById('growth-chart'));
const frData = chapterData.filter(c => c[0] === 'FR');
const raData = chapterData.filter(c => c[0] === 'RA');

growthChart.setOption({{
  tooltip: {{
    trigger: 'axis',
    backgroundColor: COLORS.marbleLight,
    borderColor: COLORS.parchmentEdge,
    borderWidth: 1,
    textStyle: {{ color: COLORS.ink, fontFamily: 'Cormorant Infant, serif' }},
    formatter: function(params) {{
      const c = params[0];
      return `<b>${{c.data.book}} Cap. ${{c.data.chapter}}</b><br/>` +
             `累计词汇: ${{c.value.toLocaleString()}} 词形<br/>` +
             `本章新词: ${{c.data.newWords}} 词`;
    }}
  }},
  legend: {{
    data: ['FR 累计词汇', 'RA 累计词汇', 'ROI 甜蜜点 (2,000 词族 ≈ 11,000 词形)'],
    top: 10,
    textStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
  }},
  grid: {{ left: 80, right: 40, top: 60, bottom: 60 }},
  xAxis: {{
    type: 'category',
    name: 'Chapter',
    nameLocation: 'middle',
    nameGap: 32,
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13, letterSpacing: 2 }},
    data: chapterData.map(c => c[0] === 'FR' ? c[1] : `+${{c[1]}}`),
    ...SHARED_AXIS,
  }},
  yAxis: {{
    type: 'value',
    name: 'Cumulative Vocab',
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13, letterSpacing: 1 }},
    ...SHARED_AXIS,
  }},
  series: [
    {{
      name: 'FR 累计词汇',
      type: 'line',
      data: chapterData.map((c, i) => ({{
        value: c[0] === 'FR' ? c[5] : null,
        book: c[0], chapter: c[1], newWords: c[3]
      }})),
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      itemStyle: {{ color: COLORS.romanGreen }},
      lineStyle: {{ width: 3, color: COLORS.romanGreen }},
      areaStyle: {{
        color: {{
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            {{ offset: 0, color: 'rgba(44, 62, 58, 0.3)' }},
            {{ offset: 1, color: 'rgba(44, 62, 58, 0.05)' }}
          ]
        }}
      }},
      connectNulls: false,
    }},
    {{
      name: 'RA 累计词汇',
      type: 'line',
      data: chapterData.map((c, i) => ({{
        value: c[0] === 'RA' ? c[5] : null,
        book: c[0], chapter: c[1], newWords: c[3]
      }})),
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      itemStyle: {{ color: COLORS.tyrianPurple }},
      lineStyle: {{ width: 3, color: COLORS.tyrianPurple }},
      areaStyle: {{
        color: {{
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            {{ offset: 0, color: 'rgba(90, 62, 92, 0.3)' }},
            {{ offset: 1, color: 'rgba(90, 62, 92, 0.05)' }}
          ]
        }}
      }},
      connectNulls: false,
    }},
    {{
      name: 'ROI 甜蜜点 (2,000 词族 ≈ 11,000 词形)',
      type: 'line',
      data: [],
      showSymbol: false,
      markLine: {{
        silent: false,
        symbol: ['none', 'none'],
        lineStyle: {{ color: COLORS.pompeiiRed, type: 'solid', width: 2 }},
        label: {{
          show: true,
          position: 'insideEndTop',
          fontFamily: 'Cinzel, serif',
          fontSize: 12,
          color: COLORS.pompeiiRed,
          fontWeight: 600,
          formatter: '★ ROI 甜蜜点 · 2,000 词族 ≈ 11,860 词形 · 80% 覆盖率'
        }},
        data: [
          {{ yAxis: 11860, name: 'ROI 甜蜜点' }},
          {{ yAxis: 10700, name: 'FR 完结 (1,800 词族)', lineStyle: {{ type: 'dashed', color: COLORS.romanGreen, width: 1.5 }} }},
        ]
      }}
    }}
  ]
}});

/* ============================================================
   CHART 2: New-Word Density
   ============================================================ */
const densityChart = echarts.init(document.getElementById('density-chart'));
densityChart.setOption({{
  tooltip: {{
    trigger: 'axis',
    backgroundColor: COLORS.marbleLight,
    borderColor: COLORS.parchmentEdge,
    borderWidth: 1,
    textStyle: {{ color: COLORS.ink, fontFamily: 'Cormorant Infant, serif' }},
    formatter: function(params) {{
      const c = params[0];
      return `<b>${{c.data.book}} Cap. ${{c.data.chapter}}</b><br/>` +
             `新词密度: ${{c.data.density}}%<br/>` +
             `本章新词: ${{c.data.newWords}} / ${{c.data.total}} 词<br/>` +
             `累计: ${{c.data.cumulative.toLocaleString()}} 词形`;
    }}
  }},
  grid: {{ left: 80, right: 40, top: 40, bottom: 60 }},
  xAxis: {{
    type: 'category',
    name: 'Chapter',
    nameLocation: 'middle',
    nameGap: 32,
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
    data: chapterData.map(c => c[0] === 'FR' ? c[1] : `+${{c[1]}}`),
    ...SHARED_AXIS,
  }},
  yAxis: {{
    type: 'value',
    name: 'Density (%)',
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
    ...SHARED_AXIS,
  }},
  series: [{{
    name: '新词密度',
    type: 'bar',
    barWidth: '70%',
    data: chapterData.map(c => {{
      const book = c[0], num = c[1], total = c[2], newWords = c[3], density = c[4], cum = c[5], rating = c[6];
      let color = COLORS.romanGreen;
      if (rating === 'steep') color = COLORS.pompeiiDeep;
      else if (rating === 'caution') color = COLORS.imperialGold;
      else if (rating === 'gentle') color = COLORS.parchmentDeep;
      const isRA = book === 'RA';
      return {{
        value: density,
        book, num, total, newWords, density, cumulative: cum,
        itemStyle: {{
          color: {{
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              {{ offset: 0, color: isRA ? COLORS.tyrianPurple : color }},
              {{ offset: 1, color: isRA ? COLORS.tyrianPurple : color, opacity: 0.7 }}
            ]
          }},
          borderColor: isRA ? COLORS.tyrianPurpleD : color,
          borderWidth: isRA ? 1 : 0,
        }}
      }};
    }}),
    markLine: {{
      silent: true,
      symbol: 'none',
      lineStyle: {{ color: COLORS.pompeiiDeep, type: 'dashed', width: 2 }},
      label: {{
        fontFamily: 'Cinzel, serif', fontSize: 11, color: COLORS.pompeiiDeep,
        formatter: `Limen · ${{avgDensity.toFixed(1)}}%`, position: 'insideEndTop'
      }},
      data: [{{ yAxis: avgDensity * 1.2 }}]
    }},
    markArea: {{
      silent: true,
      itemStyle: {{ color: 'rgba(168, 57, 46, 0.04)' }},
      data: [[
        {{ name: 'FR→RA 跃迁', xAxis: 'XXXV' }},
        {{ xAxis: '+38' }}
      ]]
    }}
  }}]
}});

/* ============================================================
   CHART 3: Total Tokens
   ============================================================ */
const tokensChart = echarts.init(document.getElementById('tokens-chart'));
tokensChart.setOption({{
  tooltip: {{
    trigger: 'axis',
    backgroundColor: COLORS.marbleLight,
    borderColor: COLORS.parchmentEdge,
    borderWidth: 1,
    textStyle: {{ color: COLORS.ink, fontFamily: 'Cormorant Infant, serif' }},
  }},
  grid: {{ left: 80, right: 40, top: 40, bottom: 60 }},
  xAxis: {{
    type: 'category',
    name: 'Chapter',
    nameLocation: 'middle',
    nameGap: 32,
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
    data: chapterData.map(c => c[0] === 'FR' ? c[1] : `+${{c[1]}}`),
    ...SHARED_AXIS,
  }},
  yAxis: {{
    type: 'value',
    name: 'Tokens',
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
    ...SHARED_AXIS,
  }},
  series: [{{
    name: '本章总词数',
    type: 'bar',
    barWidth: '70%',
    data: chapterData.map(c => ({{
      value: c[2],
      itemStyle: {{
        color: c[0] === 'FR'
          ? new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: 'rgba(44, 62, 58, 0.85)' }},
              {{ offset: 1, color: 'rgba(44, 62, 58, 0.55)' }}
            ])
          : new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: 'rgba(90, 62, 92, 0.85)' }},
              {{ offset: 1, color: 'rgba(90, 62, 92, 0.55)' }}
            ])
      }}
    }})),
  }}]
}});

/* ============================================================
   CHART 4: New Words Per Chapter
   ============================================================ */
const newwordsChart = echarts.init(document.getElementById('newwords-chart'));
newwordsChart.setOption({{
  tooltip: {{
    trigger: 'axis',
    backgroundColor: COLORS.marbleLight,
    borderColor: COLORS.parchmentEdge,
    borderWidth: 1,
    textStyle: {{ color: COLORS.ink, fontFamily: 'Cormorant Infant, serif' }},
  }},
  grid: {{ left: 80, right: 40, top: 40, bottom: 60 }},
  xAxis: {{
    type: 'category',
    name: 'Chapter',
    nameLocation: 'middle',
    nameGap: 32,
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
    data: chapterData.map(c => c[0] === 'FR' ? c[1] : `+${{c[1]}}`),
    ...SHARED_AXIS,
  }},
  yAxis: {{
    type: 'value',
    name: 'New Words',
    nameTextStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
    ...SHARED_AXIS,
  }},
  series: [{{
    name: '本章新词数',
    type: 'bar',
    barWidth: '70%',
    data: chapterData.map(c => ({{
      value: c[3],
      itemStyle: {{
        color: c[0] === 'FR'
          ? new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: 'rgba(168, 57, 46, 0.9)' }},
              {{ offset: 1, color: 'rgba(168, 57, 46, 0.5)' }}
            ])
          : new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {{ offset: 0, color: 'rgba(176, 141, 43, 0.9)' }},
              {{ offset: 1, color: 'rgba(176, 141, 43, 0.5)' }}
            ])
      }}
    }})),
  }}]
}});

/* ============================================================
   CHART 5: Book Comparison (Radar)
   ============================================================ */
const bookCompareChart = echarts.init(document.getElementById('book-compare-chart'));
const frMax = frData.length ? Math.max(...frData.map(c => c[4])) : 0;
const raMax = raData.length ? Math.max(...raData.map(c => c[4])) : 0;
const frAvgT = frData.length ? frData.reduce((s, c) => s + c[2], 0) / frData.length : 0;
const raAvgT = raData.length ? raData.reduce((s, c) => s + c[2], 0) / raData.length : 0;
const frSteep = frData.filter(c => c[6] === 'steep').length;
const raSteep = raData.filter(c => c[6] === 'steep').length;
const frCaution = frData.filter(c => c[6] === 'caution').length;
const raCaution = raData.filter(c => c[6] === 'caution').length;

bookCompareChart.setOption({{
  tooltip: {{
    backgroundColor: COLORS.marbleLight,
    borderColor: COLORS.parchmentEdge,
    textStyle: {{ color: COLORS.ink, fontFamily: 'Cormorant Infant, serif' }},
  }},
  legend: {{
    data: ['FR · Familia Romana', 'RA · Roma Aeterna'],
    top: 10,
    textStyle: {{ color: COLORS.inkSoft, fontFamily: 'Cinzel, serif', fontSize: 13 }},
  }},
  radar: {{
    indicator: [
      {{ name: '平均新词密度(%)', max: Math.max(frAvgT, raAvgT, 30) }},
      {{ name: '章节平均总词数', max: Math.max(frAvgT, raAvgT) * 1.2 }},
      {{ name: '最高单章新词数', max: Math.max(...chapterData.map(c => c[3])) * 1.1 }},
      {{ name: '陡坡章节数', max: Math.max(frSteep, raSteep, 5) * 1.2 }},
      {{ name: '注意章节数', max: Math.max(frCaution, raCaution, 5) * 1.2 }},
    ],
    axisName: {{
      color: COLORS.inkSoft,
      fontFamily: 'Cinzel, serif',
      fontSize: 12,
    }},
    splitLine: {{ lineStyle: {{ color: COLORS.parchmentEdge, type: 'dashed' }} }},
    splitArea: {{ areaStyle: {{ color: ['rgba(244, 236, 216, 0.4)', 'rgba(235, 224, 196, 0.4)'] }} }},
  }},
  series: [{{
    type: 'radar',
    data: [
      {{
        name: 'FR · Familia Romana',
        value: [
          {fr_avg:.1f},
          frAvgT,
          Math.max(...frData.map(c => c[3])),
          frSteep,
          frCaution
        ],
        areaStyle: {{ color: 'rgba(44, 62, 58, 0.4)' }},
        lineStyle: {{ color: COLORS.romanGreen, width: 2 }},
        itemStyle: {{ color: COLORS.romanGreen }},
      }},
      {{
        name: 'RA · Roma Aeterna',
        value: [
          {ra_avg:.1f},
          raAvgT,
          Math.max(...raData.map(c => c[3])),
          raSteep,
          raCaution
        ],
        areaStyle: {{ color: 'rgba(90, 62, 92, 0.4)' }},
        lineStyle: {{ color: COLORS.tyrianPurple, width: 2 }},
        itemStyle: {{ color: COLORS.tyrianPurple }},
      }}
    ]
  }}]
}});

/* ============================================================
   TABLE
   ============================================================ */
const tbody = document.getElementById('chapter-tbody');
const maxDensity = Math.max(...chapterData.map(c => c[4]));
chapterData.forEach(c => {{
  const [book, num, total, newWords, density, cum, rating, ratingLabel] = c;
  const widthPct = (density / maxDensity) * 100;
  const isSteep = rating === 'steep';
  const tr = document.createElement('tr');
  if (isSteep) tr.classList.add('steep');
  tr.innerHTML = `
    <td><span class="book-tag ${{book.toLowerCase()}}">${{book}}</span></td>
    <td><b>${{num}}</b></td>
    <td style="text-align:right">${{total.toLocaleString()}}</td>
    <td style="text-align:right">${{newWords}}</td>
    <td style="text-align:right"><b>${{density}}%</b></td>
    <td><div class="bar-cell${{isSteep ? ' steep' : ''}}">
          <span class="bar-cell-bg"><span class="bar-cell-fill" style="width:${{widthPct}}%"></span></span>
        </div></td>
    <td style="text-align:right">${{cum.toLocaleString()}}</td>
    <td><span class="rating ${{rating}}">${{ratingLabel}}</span></td>
  `;
  tbody.appendChild(tr);
}});

/* ============================================================
   RECOMMENDATIONS
   ============================================================ */
const top10 = [...chapterData].sort((a, b) => b[4] - a[4]).slice(0, 10);
const recGrid = document.getElementById('rec-grid');
top10.forEach((c, idx) => {{
  const [book, num, total, newWords, density, cum, rating, ratingLabel] = c;
  const reasons = [];
  if (density > avgDensity * 1.5) reasons.push('密度极高');
  if (book === 'RA' && num >= 36 && num <= 42) reasons.push('RA 初期适应期');
  if (book === 'FR' && num >= 8 && num <= 15) reasons.push('FR 第九章墙区域');
  if (newWords >= 1000) reasons.push('新词量爆表');
  if (!reasons.length) reasons.push('新词密度偏高');
  const p = idx < 3 ? 'p1' : (idx < 7 ? 'p2' : 'p3');
  const rec = document.createElement('div');
  rec.className = `rec ${{p}}`;
  rec.innerHTML = `
    <div class="rank">No. ${{idx + 1}}</div>
    <div class="chapter"><span class="book-tag ${{book.toLowerCase()}}">${{book}}</span> Cap. ${{num}}</div>
    <div class="pct">${{density}}%</div>
    <div class="reason">${{reasons.join(' · ')}}</div>
  `;
  recGrid.appendChild(rec);
}});

/* Resize */
window.addEventListener('resize', () => {{
  growthChart.resize();
  densityChart.resize();
  tokensChart.resize();
  newwordsChart.resize();
  bookCompareChart.resize();
}});
</script>

<style>
.bar-cell {{ position: relative; height: 14px; background: var(--parchment-edge); border-radius: 2px; overflow: hidden; }}
.bar-cell.steep {{ background: rgba(168, 57, 46, 0.15); }}
.bar-cell-bg {{ display: block; height: 100%; }}
.bar-cell-fill {{ display: block; height: 100%; background: linear-gradient(90deg, var(--imperial-gold), var(--pompeii-red)); transition: width 0.6s ease; }}
.bar-cell.steep .bar-cell-fill {{ background: linear-gradient(90deg, var(--pompeii-deep), var(--pompeii-red)); }}
</style>

</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] 合并 HTML 已生成: {output_path}")
    print(f"  文件大小: {os.path.getsize(output_path):,} bytes")


def main():
    parser = argparse.ArgumentParser(description="生成 LLPSI FR+RA 合并 HTML")
    parser.add_argument("--input", required=True, help="combined_long.csv 路径")
    parser.add_argument("--output", required=True, help="输出 HTML 路径")
    args = parser.parse_args()

    combined = load_combined(args.input)
    print(f"读取 {len(combined)} 章节数据")
    generate_html(combined, args.output)


if __name__ == "__main__":
    main()
