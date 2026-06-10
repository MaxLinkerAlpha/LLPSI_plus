"""build_llpsi_insights_html_v2.py - 阶段5：使用v2段级路由数据生成HTML

数据流:
- analysis_output/learned_words_v2.json (已学词集)
- analysis_output/reader_vocab_stats_v6.json (段级评估)
- analysis_output/llpsi_reader_routing_v2.json (段级路由)
- analysis_output/llpsi_chapter_stats.json (LLPSI章节数据)
- analysis_output/d_segments_vocab.json (D类拉语段)

输出: analysis_output/LLPSI_Insights.html
"""
import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/Downloads/Projects/LLPSI+++")
if not ROOT.exists():
    ROOT = Path("/Users/max/Downloads/Projects/LLPSI+++")

CHAPTER_STATS = ROOT / "analysis_output" / "llpsi_chapter_stats.json"
ROUTING = ROOT / "analysis_output" / "llpsi_reader_routing_v2.json"
LEARNED = ROOT / "analysis_output" / "learned_words_v2.json"
READERS = ROOT / "analysis_output" / "reader_vocab_stats_v6.json"
OUT = ROOT / "analysis_output" / "LLPSI_Insights.html"


def to_chapters_data():
    """加载LLPSI 56章基础数据"""
    data = json.loads(CHAPTER_STATS.read_text(encoding="utf-8"))
    fr = data["fr_35_chapters"]
    ra = data["ra_21_chapters"]
    return fr, ra


def load_segment_texts_from_full(slugs):
    """从_full.txt加载段文本（用于嵌入）—— 与 analyze_readers_v6.py v3.1 is_narrative 对齐"""
    import sys
    sys.path.insert(0, str(ROOT / "scripts" / "v2"))
    import analyze_readers_v6 as av6

    seg_texts = {}

    for slug in slugs:
        full = ROOT / "ocr_output" / slug / "_full.txt"
        if not full.exists():
            continue
        text = full.read_text(encoding='utf-8', errors='replace')
        # 与 analyze_readers_v6.py 一致的段落切分方式: 按空行
        paragraphs = re.split(r'\n\s*\n', text)
        idx = 0
        for p in paragraphs:
            p = p.strip()
            if av6.is_narrative(p):
                seg_texts[f"{slug}|{idx}"] = p
                idx += 1

    return seg_texts


def build_charts_js(fr_chaps, ra_chaps, learned_data):
    """构建 ECharts 词汇增长曲线"""
    chart_chapters = []
    chart_cum = []
    chart_new = []
    for ch_data in (fr_chaps + ra_chaps):
        ch = ch_data["chapter"]
        chart_chapters.append(f'FR {ch}' if ch <= 35 else f'RA {ch}')
        cum = learned_data["chapter_word_count"].get(str(ch), 0)
        chart_cum.append(cum)
        new = len(learned_data["new_per_chapter"].get(str(ch), []))
        chart_new.append(new)

    return chart_chapters, chart_cum, chart_new


def build_routing_html(routing_data, seg_texts):
    """构建扩展读物路由表 HTML（段级版）"""
    out = ['<div class="routing-grid">']

    for r in routing_data["routing"]:
        ch = r["chapter"]
        book = r["book"]
        title = r["title_roman"]
        cdata = r["chapter_data"]
        cv = cdata.get("cumulative_vocab_db", "?")
        nd = cdata.get("new_density", "?")
        cnts = r["counts"]

        out.append(f'<div class="route-card" data-ch="{ch}">')
        out.append(f'<div class="route-header">')
        out.append(f'<span class="route-ch">Cap.{ch}</span>')
        out.append(f'<span class="route-book">{book} Cap.{title}</span>')
        out.append(f'<span class="route-stats">新词密度 {nd}% · 累计 {cv} 词形</span>')
        out.append('</div>')

        out.append('<div class="route-body">')

        def render_section_html(tag, label, items, render_fn, show_n=5):
            if not items:
                return ""
            sec = [f'<div class="route-section">']
            total = len(items)
            sec.append(f'<span class="route-tag tag-{tag}">{label} ({total})</span>')
            shown = items[:show_n]
            rest = items[show_n:]
            for x in shown:
                sec.append(render_fn(x))
            if rest:
                sec.append(f'<details class="route-details">')
                sec.append(f'<summary class="route-toggle">展开剩余 {len(rest)} 项 ▾</summary>')
                sec.append('<div class="route-details-body">')
                for x in rest:
                    sec.append(render_fn(x))
                sec.append('</div></details>')
            sec.append('</div>')
            return "".join(sec)

        def render_fluent(x):
            key = f"{x['slug']}|{x['seg_idx']}"
            meta = json.dumps({
                "kind": "seg_v2",
                "slug": x["slug"],
                "title": x["title"],
                "seg_idx": x["seg_idx"],
                "tokens": x["tokens"],
            }, ensure_ascii=False)
            return (
                f'<div class="route-item route-clickable" '
                f'data-key="{html.escape(key)}" data-meta=\'{html.escape(meta, quote=True)}\'>'
                f'<code>{html.escape(x["slug"])}</code> #{x["seg_idx"]} '
                f'<span class="route-meta">t80 Cap.{x["t80"]} · {x["tokens"]} tokens</span>'
                f'<div class="route-preview">"{html.escape(x["preview"][:60])}..."</div>'
                f'<span class="route-read-badge">📖 阅读</span>'
                f'</div>'
            )

        def render_challenge(x):
            key = f"{x['slug']}|{x['seg_idx']}"
            meta = json.dumps({
                "kind": "seg_v2",
                "slug": x["slug"],
                "title": x["title"],
                "seg_idx": x["seg_idx"],
                "tokens": x["tokens"],
            }, ensure_ascii=False)
            return (
                f'<div class="route-item route-clickable" '
                f'data-key="{html.escape(key)}" data-meta=\'{html.escape(meta, quote=True)}\'>'
                f'<code>{html.escape(x["slug"])}</code> #{x["seg_idx"]} '
                f'<span class="route-meta">t70 Cap.{x["t70"]} · {x["tokens"]} tokens</span>'
                f'<div class="route-preview">"{html.escape(x["preview"][:60])}..."</div>'
                f'<span class="route-read-badge">📖 阅读</span>'
                f'</div>'
            )

        def render_selected(x):
            key = f"{x['slug']}|{x['seg_idx']}"
            meta = json.dumps({
                "kind": "seg_v2",
                "slug": x["slug"],
                "title": x["title"],
                "seg_idx": x["seg_idx"],
                "tokens": x["tokens"],
            }, ensure_ascii=False)
            return (
                f'<div class="route-item route-clickable" '
                f'data-key="{html.escape(key)}" data-meta=\'{html.escape(meta, quote=True)}\'>'
                f'<code>{html.escape(x["slug"])}</code> #{x["seg_idx"]} '
                f'<span class="route-meta">t50 Cap.{x["t50"]} · {x["tokens"]} tokens</span>'
                f'<div class="route-preview">"{html.escape(x["preview"][:60])}..."</div>'
                f'<span class="route-read-badge">📖 阅读</span>'
                f'</div>'
            )

        out.append(render_section_html("readable", "📖 流畅 (≥80%)",
                                        r["fluent_segments"], render_fluent, show_n=5))
        out.append(render_section_html("challenge", "💪 挑战 (≥70%)",
                                        r["challenging_segments"], render_challenge, show_n=5))
        out.append(render_section_html("selected", "📚 节选 (≥50%)",
                                        r["selected_segments"], render_selected, show_n=5))

        if cnts['fluent'] + cnts['challenging'] + cnts['selected'] == 0:
            out.append('<div class="route-empty">本章暂无段级推荐</div>')

        out.append('</div>')  # route-body
        out.append('</div>')  # route-card
    out.append('</div>')
    return "\n".join(out)


def build_html(fr_chaps, ra_chaps, routing_data, learned_data, seg_texts):
    chart_chapters, chart_cum, chart_new = build_charts_js(fr_chaps, ra_chaps, learned_data)

    # JavaScript: 章节选项数据
    chart_data = {
        "chapters": chart_chapters,
        "cum": chart_cum,
        "new": chart_new,
    }

    # Routing HTML
    routing_html = build_routing_html(routing_data, seg_texts)

    # 段文本（用于modal reader）
    seg_texts_json = json.dumps(seg_texts, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>LLPSI+++ v2 段级路由报告</title>
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; background: #faf8f3; color: #2c2c2c; }}
  h1 {{ color: #8b1a1a; border-bottom: 3px solid #b08d2b; padding-bottom: 10px; }}
  h2 {{ color: #5d0e0e; margin-top: 30px; }}
  .container {{ background: white; border-radius: 8px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .routing-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 16px; margin-top: 20px; }}
  .route-card {{ background: linear-gradient(135deg, #fff 0%, #faf6ed 100%); border: 1px solid #e0d8c0; border-radius: 8px; padding: 14px; }}
  .route-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px dashed #d4cba8; }}
  .route-ch {{ font-weight: 700; color: #8b1a1a; font-size: 16px; }}
  .route-book {{ color: #5d0e0e; font-size: 13px; font-style: italic; }}
  .route-stats {{ color: #888; font-size: 11px; }}
  .route-section {{ margin-bottom: 8px; }}
  .route-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-bottom: 4px; }}
  .tag-readable {{ background: #2d5a2d; color: white; }}
  .tag-challenge {{ background: #8b6914; color: white; }}
  .tag-selected {{ background: #5a4a8b; color: white; }}
  .route-item {{ background: #f8f4ea; border: 1px solid #e0d8c0; border-radius: 4px; padding: 6px 8px; margin: 4px 0; font-size: 12px; cursor: pointer; transition: all 0.15s; }}
  .route-item:hover {{ background: #f0e8d4; border-color: #b08d2b; transform: translateX(2px); }}
  .route-item code {{ color: #5d0e0e; font-weight: 600; background: #fff5e0; padding: 0 4px; border-radius: 2px; }}
  .route-meta {{ color: #888; font-size: 10px; margin-left: 6px; }}
  .route-preview {{ color: #555; font-style: italic; margin: 2px 0; font-size: 11px; }}
  .route-read-badge {{ float: right; color: #2d5a2d; font-size: 10px; }}
  .route-details {{ margin-top: 4px; }}
  .route-toggle {{ cursor: pointer; color: #b08d2b; font-size: 11px; padding: 4px 0; }}
  .route-empty {{ color: #aaa; font-style: italic; font-size: 12px; }}
  /* Modal */
  #modal {{ display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }}
  #modal.active {{ display: flex; }}
  .modal-content {{ background: #fdfaf0; border-radius: 8px; max-width: 800px; max-height: 80vh; overflow: auto; padding: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); }}
  .modal-close {{ position: absolute; top: 12px; right: 16px; cursor: pointer; font-size: 24px; color: #888; }}
  .modal-text {{ white-space: pre-wrap; font-family: 'Iowan Old Style', Georgia, serif; font-size: 16px; line-height: 1.8; padding: 20px; background: #fff; border: 1px solid #e0d8c0; border-radius: 4px; }}
  .modal-title {{ color: #5d0e0e; border-bottom: 1px solid #b08d2b; padding-bottom: 8px; margin-bottom: 16px; }}
  /* Charts */
  .chart-container {{ width: 100%; height: 360px; margin: 20px 0; }}
  .footnote {{ background: rgba(140,140,140,0.08); border-left: 3px solid #b08d2b; padding: 12px 16px; margin: 16px 0; border-radius: 4px; font-size: 13px; line-height: 1.7; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }}
  .legend-item {{ font-size: 12px; color: #555; }}
  .filter-bar {{ background: #f0e8d4; padding: 10px; border-radius: 4px; margin: 12px 0; }}
</style>
</head>
<body>
  <h1>LLPSI+++ 扩展读物段级路由报告 (v2.0)</h1>

  <div class="container">

    <h2>📊 词汇增长曲线 (基于LLPSI 56章真实文本扫描)</h2>
    <div class="footnote">
      <b>数据来源</b>: 直接扫描LLPSI OCR文本（familia_romana Cap.1-35 + roma_aeterna Cap.36-56），按章节累计已学词。
      解决了DB <code>is_new</code>标记滞后问题，<b>FR末章</b>真实累计 <b>{chart_cum[34]:,}</b> 词形，
      <b>RA末章</b>累计 <b>{chart_cum[-1]:,}</b> 词形。
    </div>
    <div id="chart-main" class="chart-container"></div>

    <h2>🎯 v2 段级路由算法说明</h2>
    <div class="footnote">
      <b>核心算法</b>:
      <ol style="margin: 6px 0 0 20px; padding: 0;">
        <li><b>段级切片</b>: 按空行切分文本为段落，识别并过滤非叙事内容（标题、练习题、词汇表、文化介绍）</li>
        <li><b>叙事过滤</b>: 拉语词占比≥50%、必须≥5个有效拉语词</li>
        <li><b>三类token加权评分 (hybrid)</b>:
          <ul style="margin: 4px 0 0 20px;">
            <li><code>full = 1.0</code>: 在 LLPSI Cap.N 已学词集 <code>learned_words[N]</code> 中</li>
            <li><code>partial = 0.5</code>: 在 LLPSI 56章总词表但 Cap.N 未学到（后续会学）</li>
            <li><code>character = 0.3</code>: 在本段所属书的高频专名（出现≥5次，识别专名+人名+地名）</li>
            <li><code>score = (full + 0.5*partial + 0.3*character) / total_latin_tokens</code></li>
          </ul>
        </li>
        <li><b>首达章节判定</b>: 找到该段 hybrid 首次达到 80%/70%/50% 的章节号</li>
      </ol>
    </div>

    <div class="legend">
      <div class="legend-item"><span class="route-tag tag-readable">📖 流畅 ≥80%</span></div>
      <div class="legend-item"><span class="route-tag tag-challenge">💪 挑战 ≥70%</span></div>
      <div class="legend-item"><span class="route-tag tag-selected">📚 节选 ≥50%</span></div>
    </div>

    <div class="footnote">
      <b>💡 交互提示</b>:
      <ul style="margin: 6px 0 0 20px; padding: 0;">
        <li>点击任意条目 → 在弹出阅读器中查看该段完整拉语原文</li>
        <li>支持 <b>Esc</b> 键或点击空白处关闭阅读器</li>
        <li>共分析 <b>63本</b>读物, 累计 <b>{sum(sum(r["counts"].values()) for r in routing_data["routing"]):,}</b> 条段级路由</li>
      </ul>
    </div>

    <div class="filter-bar">
      <label><b>筛选章节范围</b>:</label>
      <input type="number" id="filter-start" value="1" min="1" max="56" style="width:60px;"> -
      <input type="number" id="filter-end" value="56" min="1" max="56" style="width:60px;">
      <button onclick="filterRouting()">应用</button>
      <button onclick="document.getElementById('filter-start').value=1; document.getElementById('filter-end').value=56; filterRouting();">重置</button>
    </div>

    <h2>📚 56章扩展读物路由表 (段级)</h2>
    {routing_html}

  </div>

  <!-- Modal reader -->
  <div id="modal">
    <div class="modal-content">
      <span class="modal-close" onclick="closeModal()">×</span>
      <h3 class="modal-title" id="modal-title">段原文</h3>
      <div class="modal-text" id="modal-text"></div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  <script>
    const CHART_DATA = {json.dumps(chart_data)};
    const SEG_TEXTS = {seg_texts_json};

    // ECharts 词汇增长曲线
    const chart = echarts.init(document.getElementById('chart-main'));
    const option = {{
      title: {{ text: 'LLPSI 56章 已学词汇增长曲线' }},
      tooltip: {{ trigger: 'axis' }},
      legend: {{ data: ['累计已学', '本章新增'] }},
      grid: {{ left: 60, right: 30, bottom: 60 }},
      xAxis: {{
        type: 'category',
        data: CHART_DATA.chapters,
        axisLabel: {{ rotate: 45, fontSize: 10 }},
      }},
      yAxis: {{ type: 'value', name: '词数' }},
      series: [
        {{
          name: '累计已学',
          type: 'line',
          data: CHART_DATA.cum,
          smooth: true,
          itemStyle: {{ color: '#8b1a1a' }},
          areaStyle: {{ color: 'rgba(139, 26, 26, 0.1)' }},
        }},
        {{
          name: '本章新增',
          type: 'bar',
          data: CHART_DATA.new,
          itemStyle: {{ color: '#b08d2b' }},
        }},
      ],
    }};
    chart.setOption(option);

    // 段级路由交互
    function openSegmentReader(key, meta) {{
      const m = JSON.parse(meta);
      const segText = SEG_TEXTS[key] || '(段原文未加载)';
      const title = m.title + ' #' + m.seg_idx + ' (' + m.tokens + ' tokens)';
      document.getElementById('modal-title').innerText = title;
      document.getElementById('modal-text').innerText = segText;
      document.getElementById('modal').classList.add('active');
    }}
    function closeModal() {{
      document.getElementById('modal').classList.remove('active');
    }}
    document.getElementById('modal').addEventListener('click', function(e) {{
      if (e.target === this) closeModal();
    }});
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeModal();
    }});
    document.querySelectorAll('.route-clickable').forEach(el => {{
      el.addEventListener('click', function() {{
        openSegmentReader(this.dataset.key, this.dataset.meta);
      }});
    }});

    // 章节范围筛选
    function filterRouting() {{
      const s = parseInt(document.getElementById('filter-start').value);
      const e = parseInt(document.getElementById('filter-end').value);
      document.querySelectorAll('.route-card').forEach(card => {{
        const ch = parseInt(card.dataset.ch);
        card.style.display = (ch >= s && ch <= e) ? '' : 'none';
      }});
    }}
  </script>
</body>
</html>"""
    return html_content


def main():
    print("=== 生成 LLPSI_Insights.html v2 ===")
    fr_chaps, ra_chaps = to_chapters_data()
    print(f"  FR: {len(fr_chaps)}章, RA: {len(ra_chaps)}章")

    print("加载v2路由数据...")
    routing_data = json.loads(ROUTING.read_text(encoding="utf-8"))
    print(f"  {routing_data['total_chapters']}章路由")

    print("加载learned_words_v2.json...")
    learned_data = json.loads(LEARNED.read_text(encoding="utf-8"))

    print("加载段文本（嵌入HTML）...")
    readers_data = json.loads(READERS.read_text(encoding="utf-8"))
    slugs = [r["slug"] for r in readers_data]
    seg_texts = load_segment_texts_from_full(slugs)
    print(f"  共 {len(seg_texts)} 段已加载")

    # 生成HTML
    html_content = build_html(fr_chaps, ra_chaps, routing_data, learned_data, seg_texts)
    OUT.write_text(html_content, encoding='utf-8')
    print(f"\n[OK] {OUT}")


if __name__ == '__main__':
    main()
