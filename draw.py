"""Draw the 25 November 2026 world-news poster (1024x1024, PNG).

Pure Pillow drawing: no network, no external assets, no randomness
except a fixed-seed star field, so two runs produce identical bytes.
All six stories were reported on Wednesday 25 November 2026
(sources: Reuters, CNN, AP, AFP, WHO via the wires).
"""

import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# --- palette -------------------------------------------------------------
NAVY_TOP = (10, 17, 40)
NAVY_BOTTOM = (16, 28, 63)
PANEL = (22, 34, 74)
PANEL_EDGE = (48, 66, 120)
WHITE = (245, 247, 255)
MUTED = (178, 190, 220)
GOLD = (232, 184, 72)
GOLD_DIM = (180, 142, 52)

# One accent colour per story, reused for its globe dot and card bar.
STORIES = [
    {
        "num": "1",
        "tag": "USA  ·  CYBER",
        "headline": "CIA & ODNI HACKED",
        "fact": "Open-source spy network breached; unclassified data exposed.",
        "color": (94, 180, 255),
    },
    {
        "num": "2",
        "tag": "WAR AT SEA",
        "headline": "UKRAINE SINKS WARSHIP",
        "fact": "Zelenskyy confirms strikes off Libya and in the Gulf of Finland.",
        "color": (255, 107, 107),
    },
    {
        "num": "3",
        "tag": "MIDDLE EAST",
        "headline": "RIYADH TOWER HIT AGAIN",
        "fact": "Houthi drone hits 385 m PIF Tower; 11 wounded in a second strike.",
        "color": (255, 196, 66),
    },
    {
        "num": "4",
        "tag": "TECH  ·  US-CHINA",
        "headline": "HUAWEI FOUND GUILTY",
        "fact": "US jury convicts on 10 of 12 counts: trade-secret theft and bank fraud.",
        "color": (120, 220, 160),
    },
    {
        "num": "5",
        "tag": "AFRICA  ·  HEALTH",
        "headline": "EBOLA STAFF EVACUATED",
        "fact": "WHO pulls staff from a Congo hospital after 3 days of fighting.",
        "color": (196, 160, 255),
    },
    {
        "num": "6",
        "tag": "USA  ·  POLITICS",
        "headline": "GIULIANI GETS TOP MEDAL",
        "fact": "Trump awards Rudy Giuliani the Presidential Medal of Freedom.",
        "color": (255, 150, 200),
    },
]

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def _font(path, size):
    return ImageFont.truetype(path, size)


def _wrap(draw, text, font, max_width, max_lines=2):
    """Greedy word wrap; truncate with an ellipsis if it still overflows."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " …", font=font) > max_width:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] += " …"
    return lines


def _text_center(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


def _draw_globe(draw, cx, cy, r):
    """Stylised globe: deep-blue disc, gold rim, meridians and parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(27, 58, 107), outline=GOLD, width=4)
    # parallels
    for dy, w in ((-52, 150), (-26, 176), (26, 176), (52, 150)):
        draw.arc([cx - w // 2, cy + dy - 14, cx + w // 2, cy + dy + 14],
                 start=15, end=165, fill=(120, 160, 220), width=2)
    # meridians
    for w in (60, 120):
        draw.ellipse([cx - w // 2, cy - r + 4, cx + w // 2, cy + r - 4],
                     outline=(120, 160, 220), width=2)
    draw.line([cx, cy - r + 4, cx, cy + r - 4], fill=(120, 160, 220), width=2)
    # story dots on the rim, in card order, matched by colour
    import math
    for i, story in enumerate(STORIES):
        ang = math.radians(-150 + i * 48)
        px = cx + int((r - 2) * math.cos(ang))
        py = cy + int((r - 2) * math.sin(ang))
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=story["color"],
                     outline=WHITE, width=2)


def _draw_icon(draw, cx, cy, kind, color):
    """Tiny geometric glyph for a story card (drawn, not an emoji)."""
    if kind == 1:  # shield
        draw.polygon([(cx, cy - 16), (cx + 13, cy - 9), (cx + 13, cy + 4),
                      (cx, cy + 16), (cx - 13, cy + 4), (cx - 13, cy - 9)],
                     outline=color, width=3)
        draw.line([cx - 5, cy, cx - 1, cy + 5, cx + 6, cy - 5], fill=color, width=3)
    elif kind == 2:  # ship
        draw.polygon([(cx, cy - 14), (cx, cy + 4), (cx - 14, cy + 4)], fill=color)
        draw.line([cx, cy - 14, cx, cy + 4], fill=color, width=2)
        draw.polygon([(cx - 16, cy + 6), (cx + 16, cy + 6), (cx + 10, cy + 14),
                      (cx - 10, cy + 14)], fill=color)
    elif kind == 3:  # tower
        draw.rectangle([cx - 8, cy - 8, cx + 8, cy + 16], outline=color, width=3)
        draw.line([cx, cy - 18, cx, cy - 8], fill=color, width=3)
        for yy in (-2, 6):
            draw.line([cx - 8, cy + yy, cx + 8, cy + yy], fill=color, width=2)
    elif kind == 4:  # chip
        draw.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], outline=color, width=3)
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)
        for dx in (-10, 0, 10):
            draw.line([cx + dx, cy - 16, cx + dx, cy - 10], fill=color, width=2)
            draw.line([cx + dx, cy + 10, cx + dx, cy + 16], fill=color, width=2)
    elif kind == 5:  # medical cross
        draw.rectangle([cx - 4, cy - 15, cx + 4, cy + 15], fill=color)
        draw.rectangle([cx - 15, cy - 4, cx + 15, cy + 4], fill=color)
    else:  # medal
        draw.ellipse([cx - 11, cy - 4, cx + 11, cy + 16], outline=color, width=3)
        draw.polygon([(cx - 8, cy - 16), (cx - 2, cy - 4), (cx + 2, cy - 4),
                      (cx + 8, cy - 16)], fill=color)
        draw.text((cx - 4, cy + 2), "1", font=_font(FONT_BOLD, 13), fill=color)


def build_poster():
    img = Image.new("RGB", (W, H), NAVY_TOP)
    draw = ImageDraw.Draw(img)

    # vertical gradient background
    for y in range(H):
        t = y / (H - 1)
        draw.line([(0, y), (W, y)],
                  fill=tuple(int(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t)
                             for i in range(3)))

    # faint fixed-seed stars in the header area
    rng = random.Random(20261125)
    for _ in range(70):
        x = rng.randint(8, W - 8)
        y = rng.randint(8, 360)
        a = rng.randint(40, 110)
        draw.point((x, y), fill=(a + 60, a + 70, a + 120))

    f_kicker = _font(FONT_BOLD, 26)
    f_title = _font(FONT_BOLD, 74)
    f_sub = _font(FONT_REG, 25)
    f_side_big = _font(FONT_BOLD, 64)
    f_side_small = _font(FONT_BOLD, 22)
    f_tag = _font(FONT_BOLD, 17)
    f_head = _font(FONT_BOLD, 24)
    f_fact = _font(FONT_REG, 18)
    f_foot = _font(FONT_REG, 16)

    # --- header ----------------------------------------------------------
    _text_center(draw, W // 2, 30, "T H E   W O R L D   I N   O N E   D A Y",
                 f_kicker, GOLD)
    _text_center(draw, W // 2, 62, "25 NOVEMBER 2026", f_title, WHITE)
    draw.line([(W // 2 - 180, 152), (W // 2 + 180, 152)], fill=GOLD_DIM, width=2)
    _text_center(draw, W // 2, 162,
                 "Wednesday  ·  Six stories that defined the day",
                 f_sub, MUTED)

    # --- hero: globe flanked by "6 STORIES" / "1 DAY" -------------------
    _draw_globe(draw, W // 2, 284, 86)
    _text_center(draw, 200, 248, "6", f_side_big, GOLD)
    _text_center(draw, 200, 316, "STORIES", f_side_small, WHITE)
    _text_center(draw, W - 200, 248, "1", f_side_big, GOLD)
    _text_center(draw, W - 200, 316, "DAY", f_side_small, WHITE)

    # --- story cards: 2 columns x 3 rows --------------------------------
    margin, gap = 36, 20
    card_w = (W - 2 * margin - gap) // 2
    card_h = 186
    top = 388
    for idx, story in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        x0 = margin + col * (card_w + gap)
        y0 = top + row * (card_h + 16)
        x1, y1 = x0 + card_w, y0 + card_h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PANEL,
                               outline=PANEL_EDGE, width=1)
        # accent bar
        draw.rounded_rectangle([x0, y0, x0 + 9, y1], radius=4, fill=story["color"])
        # number badge
        bx, by = x0 + 30, y0 + 30
        draw.ellipse([bx, by, bx + 46, by + 46], fill=story["color"])
        num_font = _font(FONT_BOLD, 26)
        tw = draw.textlength(story["num"], font=num_font)
        draw.text((bx + 23 - tw / 2, by + 8), story["num"], font=num_font,
                  fill=(10, 17, 40))
        # icon, top right
        _draw_icon(draw, x1 - 34, y0 + 34, idx + 1, story["color"])
        # tag + headline + fact
        tx = x0 + 92
        draw.text((tx, y0 + 22), story["tag"], font=f_tag, fill=story["color"])
        head_lines = _wrap(draw, story["headline"], f_head, card_w - 92 - 56)
        hy = y0 + 48
        for line in head_lines:
            draw.text((tx, hy), line, font=f_head, fill=WHITE)
            hy += 30
        fact_lines = _wrap(draw, story["fact"], f_fact, card_w - 92 - 24)
        fy = hy + 6
        for line in fact_lines:
            draw.text((tx, fy), line, font=f_fact, fill=MUTED)
            fy += 25

    # --- footer ----------------------------------------------------------
    _text_center(draw, W // 2, 990,
                 "Sources: Reuters  ·  CNN  ·  AP  ·  AFP  ·  WHO  —  all reported 25 Nov 2026",
                 f_foot, MUTED)
    return img


def render(path):
    img = build_poster()
    img.save(path, format="PNG")
    return path
