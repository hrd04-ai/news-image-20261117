#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026 in six stories. Output: entry.png (1024x1024)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 58, 46)
PANEL = (255, 253, 246)
GREY = (90, 84, 72)
BLUE = (31, 78, 121)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, lines, fnt, fill, spacing=6):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


# ---------------- icons (simple flat pictograms) ----------------

def icon_bridge(d, cx, cy):
    # deck with a collapsed gap in the middle, two towers, arch
    d.line([(cx - 95, cy + 30), (cx - 18, cy + 30)], fill=INK, width=8)
    d.line([(cx + 18, cy + 30), (cx + 95, cy + 30)], fill=INK, width=8)
    # fallen span piece, tilted into the gap
    d.line([(cx - 16, cy + 30), (cx + 4, cy + 52)], fill=RED, width=7)
    for tx in (cx - 70, cx + 70):
        d.line([(tx, cy - 55), (tx, cy + 30)], fill=INK, width=7)
        d.line([(tx - 12, cy - 62), (tx + 12, cy - 62)], fill=INK, width=7)
    d.arc([cx - 95, cy - 45, cx + 95, cy + 45], start=180, end=360, fill=BLUE, width=6)
    d.line([(cx - 95, cy + 52), (cx + 95, cy + 52)], fill=BLUE, width=5)


def icon_plane(d, cx, cy):
    # fuselage
    d.ellipse([cx - 85, cy - 14, cx + 85, cy + 14], fill=INK)
    d.polygon([(cx + 55, cy - 8), (cx + 95, cy - 38), (cx + 78, cy - 4)], fill=INK)
    # main wing
    d.polygon([(cx - 10, cy - 6), (cx + 25, cy - 58), (cx + 45, cy - 58),
               (cx + 30, cy - 4)], fill=RED)
    d.polygon([(cx - 15, cy + 6), (cx + 5, cy + 48), (cx + 22, cy + 48),
               (cx + 18, cy + 6)], fill=RED)
    # tail fin
    d.polygon([(cx - 78, cy - 8), (cx - 62, cy - 48), (cx - 48, cy - 48),
               (cx - 55, cy - 8)], fill=INK)
    # windows
    for i in range(5):
        x = cx - 45 + i * 16
        d.ellipse([x, cy - 6, x + 8, cy + 2], fill=PAPER)
    # motion lines
    for i, y in enumerate((cy - 52, cy - 38)):
        d.line([(cx - 95, y), (cx - 55 - i * 8, y)], fill=BLUE, width=4)


def icon_tanker(d, cx, cy):
    # hull
    d.polygon([(cx - 95, cy - 5), (cx + 95, cy - 5), (cx + 78, cy + 38),
               (cx - 78, cy + 38)], fill=INK)
    d.rectangle([cx - 95, cy - 5, cx + 95, cy + 6], fill=RED)
    # deck cargo / tanks
    d.rectangle([cx - 70, cy - 38, cx - 28, cy - 5], fill=BLUE)
    d.rectangle([cx - 18, cy - 38, cx + 24, cy - 5], fill=BLUE)
    d.rectangle([cx + 34, cy - 30, cx + 72, cy - 5], fill=GREY)
    # funnel with flame
    d.polygon([(cx + 78, cy - 55), (cx + 88, cy - 32), (cx + 68, cy - 32)],
              fill=RED)
    d.polygon([(cx + 78, cy - 78), (cx + 90, cy - 52), (cx + 66, cy - 52)],
              fill=(232, 126, 32))
    # waves
    for i, x0 in enumerate((-95, -30, 35)):
        d.arc([cx + x0, cy + 48, cx + x0 + 60, cy + 72], start=0, end=180,
              fill=BLUE, width=5)


def icon_bank(d, cx, cy):
    # pediment
    d.polygon([(cx - 90, cy - 30), (cx, cy - 72), (cx + 90, cy - 30)], fill=RED)
    d.ellipse([cx - 14, cy - 58, cx + 14, cy - 30], fill=PAPER)
    # columns
    for x in (-72, -36, 0, 36, 72):
        d.rectangle([cx + x - 8, cy - 28, cx + x + 8, cy + 38], fill=INK)
    # base steps
    d.rectangle([cx - 95, cy + 38, cx + 95, cy + 48], fill=INK)
    d.rectangle([cx - 102, cy + 50, cx + 102, cy + 60], fill=INK)
    # crack / bug mark: small red lightning on the pediment
    d.polygon([(cx + 30, cy - 62), (cx + 18, cy - 34), (cx + 28, cy - 34),
               (cx + 16, cy - 8), (cx + 34, cy - 36), (cx + 24, cy - 36)],
              fill=(232, 190, 40))


def icon_chip(d, cx, cy):
    # pins
    for i in range(4):
        x = cx - 45 + i * 30
        d.line([(x, cy - 78), (x, cy - 58)], fill=INK, width=6)
        d.line([(x, cy + 58), (x, cy + 78)], fill=INK, width=6)
        y = cy - 45 + i * 30
        d.line([(cx - 78, y), (cx - 58, y)], fill=INK, width=6)
        d.line([(cx + 58, y), (cx + 78, y)], fill=INK, width=6)
    d.rectangle([cx - 58, cy - 58, cx + 58, cy + 58], fill=INK)
    d.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], fill=RED)
    d.text((cx - 8, cy - 12), "N", font=font(FONT_B, 26), fill=PAPER)


def icon_rocket(d, cx, cy):
    # body
    d.polygon([(cx, cy - 80), (cx + 26, cy - 30), (cx + 26, cy + 30),
               (cx - 26, cy + 30), (cx - 26, cy - 30)], fill=INK)
    d.ellipse([cx - 26, cy - 82, cx + 26, cy - 30], fill=RED)
    d.ellipse([cx - 12, cy - 55, cx + 12, cy - 31], fill=PAPER)
    # fins
    d.polygon([(cx - 26, cy + 10), (cx - 52, cy + 52), (cx - 26, cy + 42)],
              fill=RED)
    d.polygon([(cx + 26, cy + 10), (cx + 52, cy + 52), (cx + 26, cy + 42)],
              fill=RED)
    # flame
    d.polygon([(cx - 14, cy + 42), (cx + 14, cy + 42), (cx, cy + 78)],
              fill=(232, 126, 32))
    d.polygon([(cx - 7, cy + 42), (cx + 7, cy + 42), (cx, cy + 62)],
              fill=(232, 190, 40))
    # lost satellites: small dots drifting away
    for x, y in ((cx - 78, cy - 60), (cx + 80, cy - 45), (cx + 72, cy + 58)):
        d.rectangle([x - 6, y - 6, x + 6, y + 6], outline=BLUE, width=3)
        d.line([(x - 12, y), (x + 12, y)], fill=BLUE, width=3)


# ---------------- stories ----------------

STORIES = [
    ("EUROPE  ·  WAR", icon_bridge,
     "Kerch Bridge span collapses in strike",
     "Zelenskyy calls it \u201can unprecedented operation\u201d."),
    ("ASIA  ·  DIPLOMACY", icon_plane,
     "Trump lands in Manila for ASEAN summit",
     "Signs trade statement with Thailand; next stop China."),
    ("MIDDLE EAST  ·  ENERGY", icon_tanker,
     "Two tankers hit mines in Strait of Hormuz",
     "Ships catch fire, Iran\u2019s Revolutionary Guards said."),
    ("BUSINESS  ·  TECH", icon_bank,
     "Software bug slows JPMorgan banking",
     "Online banking, branches and Zelle slowed Monday."),
    ("TECH  ·  MARKETS", icon_chip,
     "Nvidia reports after Huang\u2019s exit",
     "Earnings due after Tuesday\u2019s close."),
    ("SPACE", icon_rocket,
     "Vulcan rocket fails, 40 satellites lost",
     "Amazon Leo satellites destroyed."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 208], fill=INK)
    title_f = font(FONT_B, 44)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=title_f)) / 2, 22), t,
           font=title_f, fill=PAPER)
    date_f = font(FONT_B, 62)
    dt = "TUESDAY 17 NOVEMBER 2026"
    while d.textlength(dt, font=date_f) > W - 48 and date_f.size > 40:
        date_f = font(FONT_B, date_f.size - 2)
    d.text(((W - d.textlength(dt, font=date_f)) / 2, 82), dt,
           font=date_f, fill=(232, 90, 70))
    sub_f = font(FONT_R, 22)
    s = "Six stories from around the globe \u2014 one day"
    d.text(((W - d.textlength(s, font=sub_f)) / 2, 162), s,
           font=sub_f, fill=(200, 192, 172))
    d.line([(24, 208), (W - 24, 208)], fill=RED, width=6)

    # ---- grid: 2 rows x 3 columns ----
    x0, y0, gap = 24, 224, 16
    pw = (W - 2 * x0 - 2 * gap) // 3          # 314
    ph = (H - y0 - 24 - gap) // 2             # 380
    tag_f = font(FONT_B, 17)
    head_f = font(FONT_B, 29)
    sub_f2 = font(FONT_R, 20)

    for i, (tag, icon, headline, sub) in enumerate(STORIES):
        r, c = divmod(i, 3)
        x = x0 + c * (pw + gap)
        y = y0 + r * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL, outline=INK, width=2)
        # region tag
        tw = d.textlength(tag, font=tag_f)
        d.text((x + (pw - tw) / 2, y + 16), tag, font=tag_f, fill=RED)
        d.line([(x + 30, y + 46), (x + pw - 30, y + 46)], fill=(200, 190, 165),
               width=2)
        # icon
        icon(d, x + pw // 2, y + 125)
        # headline
        lines = wrap(d, headline, head_f, pw - 36)
        hy = y + 212
        draw_centered(d, x + pw // 2, hy, lines, head_f, INK, spacing=4)
        # sublabel
        sub_lines = wrap(d, sub, sub_f2, pw - 36)
        sy = hy + len(lines) * (head_f.size + 4) + 8
        draw_centered(d, x + pw // 2, sy, sub_lines, sub_f2, GREY, spacing=4)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
