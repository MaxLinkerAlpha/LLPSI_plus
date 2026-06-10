#!/usr/bin/env python3
"""
ROI 曲线生成器 - 词汇量 vs 文本覆盖率
基于 Paul Nation (2006) / van Zeeland & Schmitt (2013) / Cobb (2007) 等研究
无 matplotlib 环境,用 PIL 画图
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 数据点: (词族数, 覆盖率%)
# 来源: Nation 2006, van Zeeland & Schmitt 2013, Schmitt et al. 2017 复制研究
COVERAGE_DATA = [
    (0, 0),
    (50, 25),
    (100, 50),
    (250, 53),
    (500, 57),
    (1000, 72),
    (1500, 76),
    (2000, 80),    # 实用最优甜蜜点
    (3000, 85),
    (4000, 90),
    (5000, 93),
    (6000, 95),    # 听力门槛
    (7000, 96.5),
    (8000, 98),    # 独立阅读门槛
    (9000, 98.5),
    (10000, 99),
]

# LLPSI 进度标注
LLPSI_MARKS = [
    (600, "FR Cap. 1-15", "#5b8def"),
    (1800, "FR Cap. 35", "#3a6fcf"),
    (3500, "FR+RA 56", "#1f4f9c"),
    (5500, "+拓展读物", "#0f2e6a"),
]

# 颜色定义
COLOR_BG = (255, 255, 255)
COLOR_AXIS = (50, 50, 50)
COLOR_CURVE = (60, 130, 220)
COLOR_CURVE_FILL = (60, 130, 220, 50)
COLOR_SWEET = (255, 80, 80)
COLOR_SWEET_LINE = (255, 180, 180)
COLOR_HEARING = (255, 165, 0)
COLOR_READING = (139, 69, 19)
COLOR_LLPSI = (90, 158, 90)
COLOR_TEXT = (40, 40, 40)
COLOR_GRID = (230, 230, 230)


def get_font(size: int, bold: bool = False):
    """尝试加载系统字体,失败则用默认字体"""
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def get_cjk_font(size: int):
    """中文字体"""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Apple LiGothic Medium.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return get_font(size)


def draw_roi_curve(output_path: str):
    W, H = 1600, 1000
    img = Image.new("RGB", (W, H), COLOR_BG)
    d = ImageDraw.Draw(img, "RGBA")

    # 边距
    M_L, M_R, M_T, M_B = 130, 80, 110, 130
    plot_w = W - M_L - M_R
    plot_h = H - M_T - M_B

    # 坐标范围
    x_max = 10500
    y_max = 100

    def to_xy(x, y):
        px = M_L + (x / x_max) * plot_w
        py = M_T + (1 - y / y_max) * plot_h
        return px, py

    # 标题
    title_font = get_font(34, bold=True)
    subtitle_font = get_font(20)
    d.text((W // 2, 30), "Vocabulary ROI Curve: Word Families vs Text Coverage",
           font=title_font, fill=COLOR_TEXT, anchor="mm")
    d.text((W // 2, 70), "基于 Paul Nation (2006), van Zeeland & Schmitt (2013), Cobb (2007)",
           font=subtitle_font, fill=(120, 120, 120), anchor="mm")

    # 网格
    for x in range(0, int(x_max) + 1, 1000):
        px, py = to_xy(x, 0)
        d.line([(px, M_T), (px, M_T + plot_h)], fill=COLOR_GRID, width=1)
    for y in range(0, 101, 10):
        px, py = to_xy(0, y)
        d.line([(M_L, py), (M_L + plot_w, py)], fill=COLOR_GRID, width=1)

    # 填充曲线下方 (浅色)
    points_filled = [to_xy(0, 0)] + [to_xy(x, y) for x, y in COVERAGE_DATA] + [to_xy(COVERAGE_DATA[-1][0], 0)]
    d.polygon(points_filled, fill=(60, 130, 220, 30))

    # 主曲线
    points = [to_xy(x, y) for x, y in COVERAGE_DATA]
    d.line(points, fill=COLOR_CURVE, width=4)

    # 数据点
    for x, y in COVERAGE_DATA:
        px, py = to_xy(x, y)
        d.ellipse([(px - 5, py - 5), (px + 5, py + 5)], fill=COLOR_CURVE, outline=COLOR_AXIS, width=1)

    # ===== 关键阈值线 =====
    # 1. 数学 ROI 峰值 (~100 词, 50% 覆盖率)
    px, py = to_xy(100, 50)
    d.ellipse([(px - 8, py - 8), (px + 8, py + 8)], fill=(200, 100, 200), outline=(80, 0, 80), width=2)
    d.line([(px, M_T), (px, M_T + plot_h)], fill=(200, 100, 200, 100), width=2)

    # 2. 实用最优甜蜜点 (2,000 词, 80% 覆盖率) ★ 重点
    px, py = to_xy(2000, 80)
    d.ellipse([(px - 14, py - 14), (px + 14, py + 14)], fill=COLOR_SWEET, outline=(150, 0, 0), width=3)
    d.line([(px, M_T), (px, M_T + plot_h)], fill=COLOR_SWEET_LINE, width=3)
    d.line([(M_L, py), (M_L + plot_w, py)], fill=COLOR_SWEET_LINE, width=3)

    # 3. 听力门槛 (6,500 词, 95%)
    px2, py2 = to_xy(6500, 95)
    d.ellipse([(px2 - 10, py2 - 10), (px2 + 10, py2 + 10)], fill=COLOR_HEARING, outline=(150, 100, 0), width=2)
    d.line([(px2, M_T), (px2, M_T + plot_h)], fill=(255, 220, 150, 200), width=2)

    # 4. 独立阅读门槛 (8,500 词, 98%)
    px3, py3 = to_xy(8500, 98)
    d.ellipse([(px3 - 10, py3 - 10), (px3 + 10, py3 + 10)], fill=COLOR_READING, outline=(80, 40, 0), width=2)
    d.line([(px3, M_T), (px3, M_T + plot_h)], fill=(220, 180, 150, 200), width=2)

    # ===== LLPSI 进度标注 =====
    cjk = get_cjk_font(16)
    for x, label, color in LLPSI_MARKS:
        # 找到对应 y
        y = None
        for px_, py_ in COVERAGE_DATA:
            if px_ == x or (x > 0 and abs(px_ - x) < 500):
                y = py_
                break
        if y is None:
            y = 0
            for i, (px_, _) in enumerate(COVERAGE_DATA):
                if px_ <= x:
                    y = COVERAGE_DATA[i][1]
        px, py = to_xy(x, y)
        # 竖虚线
        for ty in range(int(M_T), int(M_T + plot_h), 10):
            d.line([(px, ty), (px, ty + 5)], fill=color, width=2)
        # 标注框
        text_bbox = d.textbbox((0, 0), label, font=cjk)
        tw, th = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        box_x, box_y = px - tw / 2 - 6, M_T - th - 4
        d.rectangle([(box_x, box_y), (box_x + tw + 12, box_y + th + 8)],
                    fill=(255, 255, 255), outline=color, width=2)
        d.text((px, box_y + th / 2 + 2), label, font=cjk, fill=color, anchor="mm")

    # 关键点标签 (英文)
    label_font = get_font(15, bold=True)
    cjk_small = get_cjk_font(14)

    # 数学 ROI 峰值
    px, py = to_xy(100, 50)
    d.text((px + 16, py - 30), "Math ROI Peak", font=label_font, fill=(150, 50, 150), anchor="lm")
    d.text((px + 16, py - 12), "100 词", font=cjk_small, fill=(150, 50, 150), anchor="lm")
    d.text((px + 16, py + 2), "50%", font=label_font, fill=(150, 50, 150), anchor="lm")

    # 甜蜜点
    px, py = to_xy(2000, 80)
    sweet_label_box = d.textbbox((0, 0), "★ Practical Sweet Spot ★", font=label_font)
    slw, slh = sweet_label_box[2] - sweet_label_box[0], sweet_label_box[3] - sweet_label_box[1]
    d.rectangle([(px - slw / 2 - 10, py - 60), (px + slw / 2 + 10, py - 60 + slh + 6)],
                fill=(255, 240, 240), outline=COLOR_SWEET, width=2)
    d.text((px, py - 60 + slh / 2 + 3), "★ Practical Sweet Spot ★", font=label_font, fill=COLOR_SWEET, anchor="mm")
    d.text((px + 20, py + 18), "2,000 词族", font=cjk_small, fill=COLOR_SWEET, anchor="lm")
    d.text((px + 20, py + 36), "80% 覆盖率", font=cjk_small, fill=COLOR_SWEET, anchor="lm")

    # 听力门槛
    px, py = to_xy(6500, 95)
    d.text((px + 14, py - 6), "Listening 95%", font=label_font, fill=(150, 100, 0), anchor="lm")

    # 阅读门槛
    px, py = to_xy(8500, 98)
    d.text((px + 14, py - 6), "Reading 98%", font=label_font, fill=(100, 50, 0), anchor="lm")

    # ===== 边际收益区域 (右上角阴影) =====
    # 暗色: 边际收益递减陷阱
    dim_zone = [to_xy(2000, 80), to_xy(x_max, 80), to_xy(x_max, y_max), to_xy(2000, y_max)]
    d.polygon(dim_zone, fill=(100, 100, 100, 25))
    cjk_18 = get_cjk_font(18)
    d.text((M_L + plot_w * 0.62, M_T + plot_h * 0.18), "Diminishing Returns Zone", font=label_font, fill=(100, 100, 100), anchor="mm")
    d.text((M_L + plot_w * 0.62, M_T + plot_h * 0.13), "边际收益递减区", font=cjk_18, fill=(100, 100, 100), anchor="mm")
    d.text((M_L + plot_w * 0.62, M_T + plot_h * 0.08), "(2,000→10,000 词", font=cjk_small, fill=(100, 100, 100), anchor="mm")
    d.text((M_L + plot_w * 0.62, M_T + plot_h * 0.045), " 仅 +18% 覆盖率)", font=cjk_small, fill=(100, 100, 100), anchor="mm")

    # ===== 坐标轴 =====
    d.line([(M_L, M_T), (M_L, M_T + plot_h)], fill=COLOR_AXIS, width=2)
    d.line([(M_L, M_T + plot_h), (M_L + plot_w, M_T + plot_h)], fill=COLOR_AXIS, width=2)

    # X 轴刻度
    axis_font = get_font(16)
    for x in range(0, int(x_max) + 1, 1000):
        px, py = to_xy(x, 0)
        d.line([(px, M_T + plot_h), (px, M_T + plot_h + 6)], fill=COLOR_AXIS, width=2)
        d.text((px, M_T + plot_h + 12), f"{x}", font=axis_font, fill=COLOR_TEXT, anchor="mt")

    # Y 轴刻度
    for y in range(0, 101, 10):
        px, py = to_xy(0, y)
        d.line([(M_L - 6, py), (M_L, py)], fill=COLOR_AXIS, width=2)
        d.text((M_L - 10, py), f"{y}%", font=axis_font, fill=COLOR_TEXT, anchor="rm")

    # 坐标轴标签
    label_font_x = get_font(22, bold=True)
    cjk_label = get_cjk_font(22)
    d.text((M_L + plot_w / 2, M_T + plot_h + 70), "Word Families (词族数)", font=cjk_label, fill=COLOR_TEXT, anchor="mm")
    d.text((50, M_T + plot_h / 2), "Text Coverage\n文本覆盖率", font=cjk_label, fill=COLOR_TEXT, anchor="mm", align="center")

    # 图例
    legend_y = M_T + 20
    legend_x = M_L + 20
    legend_items = [
        (COLOR_CURVE, "Coverage curve 覆盖率曲线"),
        (COLOR_SWEET, "Practical sweet spot 实用甜蜜点 (2,000)"),
        ((200, 100, 200), "Math ROI peak 数学 ROI 峰值 (100)"),
        (COLOR_HEARING, "Listening 95% threshold 听力门槛"),
        (COLOR_READING, "Reading 98% threshold 阅读门槛"),
    ]
    legend_font = get_cjk_font(14)
    for i, (col, txt) in enumerate(legend_items):
        ly = legend_y + i * 26
        d.rectangle([(legend_x, ly), (legend_x + 22, ly + 16)], fill=col, outline=COLOR_AXIS, width=1)
        d.text((legend_x + 30, ly + 8), txt, font=legend_font, fill=COLOR_TEXT, anchor="lm")

    # 副标题提示 - 背景说明
    note_y = M_T + plot_h - 50
    cjk_14 = get_cjk_font(14)
    notes = [
        "Source: Nation (2006); van Zeeland & Schmitt (2013); Cobb (2007); VOLT (Xu et al., 2021)",
        "LLPSI 完成 FR ≈ 1,800 词族, FR+RA ≈ 3,500 词族",
    ]
    for i, note in enumerate(notes):
        d.text((M_L + plot_w / 2, note_y + i * 18), note, font=cjk_14, fill=(100, 100, 100), anchor="mm")

    img.save(output_path, "PNG", quality=95)
    print(f"[OK] ROI 曲线已保存: {output_path}")


if __name__ == "__main__":
    out = "/Users/max/Downloads/Projects/LLPSI+++/docs/vocabulary_roi_curve.png"
    draw_roi_curve(out)
