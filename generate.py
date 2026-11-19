#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261118 (v2).

A magazine-cover poster of Wednesday 18 November 2026, drawn entirely
by code with PIL. Design goal vs v1 (a newspaper front page, 97.9552%):
much bigger type everywhere, one dominant hero scene, far fewer words,
so the image still reads at ~300px across. Fully deterministic: fixed
seed, no clock, no network, no timestamps.
Run: python3 generate.py [out.png]
"""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SEED = 20261118

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = DEJAVU + "DejaVuSerif-Bold.ttf"
SERIF = DEJAVU + "DejaVuSerif.ttf"
SANS_B = DEJAVU + "DejaVuSans-Bold.ttf"
SANS = DEJAVU + "DejaVuSans.ttf"

PAPER = (246, 241, 231)
INK = (18, 22, 30)
NAVY = (14, 26, 46)
RED = (178, 34, 34)
DARKRED = (150, 26, 26)
GOLD = (212, 160, 60)
GREY = (110, 108, 100)

rng = random.Random(SEED)


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def glow(img, cx, cy, radius, color, alpha=160):
    """Soft radial glow on an RGBA overlay."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    steps = 24
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(alpha * (1 - i / steps) ** 1.5) + 8
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=color + (a,))
    img.alpha_composite(ov)


def stars(draw, box, n, size_max=2):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rng.randint(x0, x1)
        y = rng.randint(y0, y1)
        s = rng.randint(1, size_max)
        b = rng.randint(170, 255)
        draw.ellipse([x, y, x + s, y + s], fill=(b, b, b))


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(draw, box, fill=PAPER, border=INK, width=2):
    draw.rectangle(box, fill=fill, outline=border, width=width)


def kicker(draw, x, y, text, color=RED, size=15):
    draw.text((x, y), text, font=font(SANS_B, size), fill=color)


def headline_block(draw, x, y, width, head, sub, head_size=30,
                   sub_size=18, head_font=SERIF_B,
                   sub_color=(60, 60, 60)):
    """Headline (wrapped, bold serif) + sub (wrapped, sans). Returns end y."""
    hf = font(head_font, head_size)
    sf = font(SANS, sub_size)
    hy = y
    for line in wrap(draw, head, hf, width):
        draw.text((x, hy), line, font=hf, fill=INK)
        hy += head_size + 4
    sy = hy + 2
    for line in wrap(draw, sub, sf, width):
        draw.text((x, sy), line, font=sf, fill=sub_color)
        sy += sub_size + 4
    return sy


def fit_text(draw, text, fnt_path, size, max_width, bold=True):
    """Shrink font until text fits max_width; return (font, size)."""
    path = fnt_path if bold else SANS
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f, size
        size -= 1
    return font(path, size), size


# ---------------------------------------------------------------- masthead + date
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 96], fill=NAVY)
    tf = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 14), title, font=tf, fill=(250, 247, 240))
    draw.rectangle([0, 96, W, 146], fill=RED)
    df = font(SANS_B, 30)
    date = "WEDNESDAY  ·  18 NOVEMBER 2026"
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 106), date, font=df, fill=(255, 255, 255))


# ---------------------------------------------------------------- hero: Gulf
def draw_hero(img, draw):
    x0, y0, x1, y1 = 8, 146, 1016, 400
    panel(draw, (x0, y0, x1, y1), fill=NAVY)
    vgrad(draw, (x0 + 2, y0 + 2, x1 - 2, y1 - 2),
          (10, 18, 38), (30, 54, 88))
    stars(draw, (x0 + 6, y0 + 6, x1 - 6, y0 + 150), 70, 2)
    # moon, top right
    draw.ellipse([x1 - 108, y0 + 20, x1 - 62, y0 + 66],
                 fill=(235, 230, 200))
    draw.ellipse([x1 - 98, y0 + 16, x1 - 58, y0 + 58], fill=(16, 28, 50))
    # sea
    sea_y = y0 + 168
    draw.rectangle([x0 + 2, sea_y, x1 - 2, y1 - 2], fill=(14, 34, 58))
    for _ in range(24):
        sx = rng.randint(x0 + 10, x1 - 60)
        sy = rng.randint(sea_y + 4, y1 - 14)
        ln = rng.randint(18, 70)
        draw.line([(sx, sy), (sx + ln, sy)], fill=(70, 110, 150), width=2)
    # Qeshm island silhouette (right): missile site + rising missile
    draw.polygon([(x1 - 330, sea_y), (x1 - 300, sea_y - 34),
                  (x1 - 240, sea_y - 52), (x1 - 180, sea_y - 30),
                  (x1 - 130, sea_y - 44), (x1 - 60, sea_y - 12),
                  (x1 - 2, sea_y - 20), (x1 - 2, sea_y)],
                 fill=(8, 14, 26))
    draw.rectangle([x1 - 220, sea_y - 52, x1 - 208, sea_y - 30],
                   fill=(30, 40, 55))
    draw.line([(x1 - 214, sea_y - 52), (x1 - 150, y0 + 58)],
              fill=(255, 190, 90), width=3)
    glow(img, x1 - 150, y0 + 58, 26, (255, 170, 60), 200)
    draw.ellipse([x1 - 156, y0 + 52, x1 - 144, y0 + 64],
                 fill=(255, 230, 170))
    # base buildings (left, Kuwait side) with lit windows
    for bx, bw, bh in [(x0 + 24, 64, 46), (x0 + 96, 44, 34),
                       (x0 + 148, 56, 40)]:
        draw.rectangle([bx, sea_y - bh, bx + bw, sea_y], fill=(8, 14, 26))
        for wx in range(bx + 8, bx + bw - 6, 14):
            draw.rectangle([wx, sea_y - bh + 8, wx + 6, sea_y - bh + 16],
                           fill=(255, 210, 110))
    # one big explosion over the base, smoke drifting up-left first
    ex, ey = x0 + 120, sea_y - 78
    for i, r in enumerate((12, 9, 6)):
        sx, sy = ex - 26 - i * 4, ey - 34 - i * 12
        draw.ellipse([sx - r, sy - r, sx + r, sy + r],
                     fill=(96, 96, 102))
    glow(img, ex, ey, 95, (255, 120, 40), 220)
    glow(img, ex, ey, 42, (255, 220, 130), 230)
    for ang in range(0, 360, 30):
        r1 = rng.randint(14, 36)
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        draw.line([(ex, ey), (ex + dx * r1, ey + dy * r1)],
                  fill=(255, 200, 90), width=3)
    # drone silhouettes with red dots
    for dx, dy in [(x0 + 330, y0 + 60), (x0 + 560, y0 + 104),
                   (x0 + 700, y0 + 44)]:
        draw.line([(dx - 12, dy - 6), (dx + 12, dy + 6)], fill=(5, 8, 14),
                  width=4)
        draw.line([(dx - 12, dy + 6), (dx + 12, dy - 6)], fill=(5, 8, 14),
                  width=4)
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 60, 60))
    # headline block on paper, below the scene
    kicker(draw, 16, 414, "GULF WAR  ·  THE LEAD STORY", size=18)
    hf = font(SERIF_B, 70)
    draw.text((16, 436), "GULF WAR ESCALATES", font=hf, fill=INK)
    sub = ("U.S. hit a missile site on Qeshm — Iran struck back "
           "in Kuwait and Bahrain")
    sf, _ = fit_text(draw, sub, SANS_B, 24, W - 32, bold=False)
    draw.text((16, 514), sub, font=sf, fill=(60, 60, 60))
    return draw


# ------------------------------------------------------- mid: summit
def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.28
    r = h * 0.16
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.12), (0.68, 0.28), (0.55, 0.48)]:
        draw.ellipse([x + w * sx - 3, y + h * sy - 3,
                      x + w * sx + 3, y + h * sy + 3], fill=(255, 222, 0))


def flag_russia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(250, 250, 250))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def flag_usa(draw, x, y, w, h):
    for i in range(7):
        c = (179, 25, 66) if i % 2 == 0 else (250, 250, 250)
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=c)
    draw.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill=(10, 49, 97))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 9, y + 4 + r * 8,
                          x + 7 + c * 9, y + 7 + r * 8], fill=(255, 255, 255))


def draw_summit(img, draw):
    box = (8, 552, 504, 764)
    panel(draw, box)
    x0, y0, x1, y1 = box
    art_h = 92
    vgrad(draw, (x0 + 2, y0 + 2, x1 - 2, y0 + art_h),
          (150, 190, 220), (225, 232, 238))
    # Shenzhen skyline
    sky = [(x0 + 10, 56), (x0 + 44, 38), (x0 + 78, 68), (x0 + 116, 44),
           (x0 + 150, 78), (x0 + 186, 50), (x0 + 224, 62), (x0 + 258, 40),
           (x0 + 292, 60), (x0 + 330, 44), (x0 + 366, 70), (x0 + 400, 48),
           (x0 + 436, 56)]
    for bx, bh in sky:
        draw.rectangle([bx, y0 + art_h - bh, bx + 30, y0 + art_h],
                       fill=(90, 110, 130))
    draw.polygon([(x0 + 150, y0 + art_h - 78), (x0 + 165, y0 + art_h - 102),
                  (x0 + 180, y0 + art_h - 78)], fill=(90, 110, 130))
    # three flags on poles (labels tucked inside the art band,
    # clear of the kicker below it)
    fy = y0 + 8
    for i, fl in enumerate((flag_china, flag_russia, flag_usa)):
        fx = x0 + 120 + i * 96
        draw.line([(fx, fy), (fx, fy + 62)], fill=(40, 40, 40), width=3)
        fl(draw, fx + 3, fy + 2, 62, 36)
    lf = font(SANS_B, 11)
    for i, name in enumerate(("CHINA", "RUSSIA", "U.S.A.")):
        draw.text((x0 + 120 + i * 96, fy + 62), name, font=lf, fill=INK)
    draw.line([(x0 + 2, y0 + art_h), (x1 - 2, y0 + art_h)], fill=INK, width=2)
    kicker(draw, x0 + 14, y0 + art_h + 8, "APEC  ·  SHENZHEN", size=15)
    headline_block(draw, x0 + 14, y0 + art_h + 30, x1 - x0 - 28,
                   "XI & PUTIN MEET IN SHENZHEN",
                   "Three-way summit with Trump set for Thursday.",
                   head_size=30, sub_size=18)


# ------------------------------------------------------- mid: bridge
def draw_bridge(img, draw):
    box = (520, 552, 1016, 764)
    panel(draw, box)
    x0, y0, x1, y1 = box
    art_h = 92
    vgrad(draw, (x0 + 2, y0 + 2, x1 - 2, y0 + art_h),
          (240, 190, 140), (200, 170, 150))
    # strait
    wy = y0 + 72
    draw.rectangle([x0 + 2, wy, x1 - 2, y0 + art_h], fill=(70, 110, 140))
    for _ in range(10):
        sx = rng.randint(x0 + 10, x1 - 50)
        draw.line([(sx, wy + rng.randint(4, 18)),
                   (sx + rng.randint(14, 40), wy + rng.randint(4, 18))],
                  fill=(150, 190, 215), width=2)
    # bridge deck: left span intact, right span broken
    deck_y = y0 + 48
    draw.line([(x0 + 8, deck_y), (x0 + 250, deck_y)], fill=(60, 60, 66),
              width=10)
    draw.line([(x0 + 250, deck_y), (x0 + 300, deck_y + 22)],
              fill=(60, 60, 66), width=10)
    draw.line([(x0 + 380, deck_y), (x1 - 8, deck_y)], fill=(60, 60, 66),
              width=10)
    # piers into the water
    for px in (x0 + 60, x0 + 200, x0 + 430):
        draw.rectangle([px - 5, deck_y, px + 5, wy + 2], fill=(60, 60, 66))
    # intact arch (left) with hangers
    draw.arc([x0 + 40, deck_y - 34, x0 + 210, deck_y + 8], 180, 360,
             fill=(60, 60, 66), width=8)
    for hx in range(x0 + 70, x0 + 200, 26):
        draw.line([(hx, deck_y - 22), (hx, deck_y)], fill=(60, 60, 66),
                  width=3)
    # broken arch stub (right)
    draw.arc([x0 + 330, deck_y - 34, x0 + 470, deck_y + 8], 180, 300,
             fill=(60, 60, 66), width=8)
    # falling deck segment + splash
    draw.polygon([(x0 + 300, deck_y + 22), (x0 + 340, deck_y + 26),
                  (x0 + 330, wy - 2), (x0 + 305, wy - 2)], fill=(80, 80, 88))
    for sx in range(x0 + 296, x0 + 350, 8):
        draw.line([(sx, wy), (sx + 4, wy - 9)], fill=(230, 240, 250),
                  width=2)
    # smoke first, then the blast glow at the break
    for i, r in enumerate((13, 10, 7)):
        draw.ellipse([x0 + 300 - r, deck_y - 22 - i * 12 - r,
                      x0 + 300 + r, deck_y - 22 - i * 12 + r],
                     fill=(120, 116, 110))
    glow(img, x0 + 310, deck_y - 4, 44, (255, 130, 50), 210)
    glow(img, x0 + 310, deck_y - 4, 20, (255, 220, 130), 230)
    # drones
    for dx, dy in [(x0 + 90, y0 + 18), (x0 + 430, y0 + 22)]:
        draw.line([(dx - 9, dy - 5), (dx + 9, dy + 5)], fill=(30, 30, 34),
                  width=3)
        draw.line([(dx - 9, dy + 5), (dx + 9, dy - 5)], fill=(30, 30, 34),
                  width=3)
    draw.line([(x0 + 2, y0 + art_h), (x1 - 2, y0 + art_h)], fill=INK, width=2)
    kicker(draw, x0 + 14, y0 + art_h + 8, "UKRAINE  ·  CRIMEA", size=15)
    headline_block(draw, x0 + 14, y0 + art_h + 30, x1 - x0 - 28,
                   "KERCH BRIDGE HIT",
                   "Ukraine drops a road span into the strait.",
                   head_size=30, sub_size=18)


# ------------------------------------------------------- small: senate
def draw_senate(img, draw):
    box = (8, 776, 340, 960)
    panel(draw, box)
    x0, y0, x1, y1 = box
    art_h = 80
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + art_h], fill=(24, 44, 84))
    stars(draw, (x0 + 6, y0 + 6, x1 - 6, y0 + 52), 20, 1)
    # capitol dome silhouette
    cx = (x0 + x1) // 2
    base = y0 + art_h
    draw.rectangle([cx - 90, base - 20, cx + 90, base], fill=(235, 235, 228))
    draw.rectangle([cx - 60, base - 30, cx + 60, base - 20],
                   fill=(235, 235, 228))
    draw.pieslice([cx - 32, base - 68, cx + 32, base - 8], 180, 360,
                  fill=(235, 235, 228))
    draw.rectangle([cx - 3, base - 80, cx + 3, base - 64],
                   fill=(235, 235, 228))
    draw.ellipse([cx - 5, base - 86, cx + 5, base - 76], fill=GOLD)
    for col in range(-4, 5):
        draw.rectangle([cx + col * 18 - 3, base - 18, cx + col * 18 + 3,
                        base - 2], fill=(24, 44, 84))
    # big score
    bf = font(SERIF_B, 38)
    draw.text((x0 + 14, y0 + 10), "56", font=bf, fill=(120, 180, 255))
    draw.text((x1 - 82, y0 + 10), "44", font=bf, fill=(255, 130, 130))
    draw.line([(x0 + 2, y0 + art_h), (x1 - 2, y0 + art_h)], fill=INK, width=2)
    kicker(draw, x0 + 14, y0 + art_h + 6, "U.S. SENATE  ·  ALASKA", size=13)
    headline_block(draw, x0 + 14, y0 + art_h + 24, x1 - x0 - 28,
                   "PELTOLA FLIPS ALASKA",
                   "Democrats take 56–44 control.",
                   head_size=25, sub_size=16)


# ------------------------------------------------------- small: measles
def draw_measles(img, draw):
    box = (356, 776, 688, 960)
    panel(draw, box)
    x0, y0, x1, y1 = box
    art_h = 80
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + art_h],
                   fill=(250, 238, 232))
    # virus blobs (left and centre)
    for vx, vy, vr in [(x0 + 52, y0 + 48, 22), (x0 + 128, y0 + 40, 16),
                       (x0 + 170, y0 + 58, 16), (x0 + 94, y0 + 66, 10)]:
        for i in range(12):
            a = i * math.pi / 6
            draw.line([(vx + vr * math.cos(a), vy + vr * math.sin(a)),
                       (vx + (vr + 8) * math.cos(a),
                        vy + (vr + 8) * math.sin(a))],
                      fill=(190, 50, 50), width=3)
            draw.ellipse([vx + (vr + 8) * math.cos(a) - 3,
                          vy + (vr + 8) * math.sin(a) - 3,
                          vx + (vr + 8) * math.cos(a) + 3,
                          vy + (vr + 8) * math.sin(a) + 3],
                         fill=(190, 50, 50))
        draw.ellipse([vx - vr, vy - vr, vx + vr, vy + vr],
                     fill=(214, 80, 70))
        draw.ellipse([vx - vr * 0.55, vy - vr * 0.55,
                      vx + vr * 0.55, vy + vr * 0.55], fill=(235, 130, 120))
    # big number, top right, clear of the viruses
    bf = font(SERIF_B, 28)
    num = "5,412"
    draw.text((x1 - 14 - draw.textlength(num, font=bf), y0 + 4), num,
              font=bf, fill=(160, 30, 30))
    sf = font(SANS_B, 11)
    lab = "CASES IN 2026"
    draw.text((x1 - 14 - draw.textlength(lab, font=sf), y0 + 36), lab,
              font=sf, fill=(120, 40, 40))
    draw.line([(x0 + 2, y0 + art_h), (x1 - 2, y0 + art_h)], fill=INK, width=2)
    kicker(draw, x0 + 14, y0 + art_h + 6, "HEALTH  ·  UNITED STATES", size=13)
    headline_block(draw, x0 + 14, y0 + art_h + 24, x1 - x0 - 28,
                   "MEASLES-FREE STATUS LOST",
                   "5,412 cases in 2026, after 26 years.",
                   head_size=25, sub_size=16)


# ------------------------------------------------------- small: voyager
def draw_voyager(img, draw):
    box = (704, 776, 1016, 960)
    panel(draw, box)
    x0, y0, x1, y1 = box
    art_h = 80
    draw.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + art_h], fill=(5, 8, 18))
    stars(draw, (x0 + 6, y0 + 6, x1 - 6, y0 + art_h - 4), 36, 2)
    # earth (small, bottom-left) + dashed trajectory to spacecraft
    ex, ey = x0 + 30, y0 + art_h - 20
    draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(70, 130, 200))
    draw.ellipse([ex - 5, ey - 7, ex + 2, ey - 1], fill=(120, 190, 120))
    sx, sy = x0 + 252, y0 + 36
    steps = 14
    for i in range(steps):
        t0, t1 = i / steps, (i + 0.55) / steps
        if i % 2 == 0:
            draw.line([(ex + (sx - ex) * t0, ey + (sy - ey) * t0),
                       (ex + (sx - ex) * t1, ey + (sy - ey) * t1)],
                      fill=(180, 180, 200), width=2)
    # spacecraft: gold body + white dish + boom
    draw.rectangle([sx - 9, sy - 7, sx + 9, sy + 7], fill=(212, 160, 60))
    draw.pieslice([sx + 7, sy - 20, sx + 40, sy + 13], 270, 90,
                  fill=(230, 230, 225))
    draw.line([(sx - 9, sy), (sx - 44, sy - 20)], fill=(200, 200, 200),
              width=3)
    draw.line([(sx, sy + 7), (sx - 7, sy + 32)], fill=(200, 200, 200),
              width=3)
    glow(img, sx + 22, sy - 3, 24, (255, 230, 150), 140)
    bf = font(SERIF_B, 24)
    draw.text((x0 + 14, y0 + 6), "1 LIGHT-DAY", font=bf, fill=(250, 240, 200))
    draw.line([(x0 + 2, y0 + art_h), (x1 - 2, y0 + art_h)], fill=INK, width=2)
    kicker(draw, x0 + 14, y0 + art_h + 6, "SPACE  ·  NASA", size=13)
    headline_block(draw, x0 + 14, y0 + art_h + 24, x1 - x0 - 28,
                   "VOYAGER 1: ONE LIGHT-DAY OUT",
                   "16 billion miles from Earth.",
                   head_size=25, sub_size=16)


# ---------------------------------------------------------------- ticker + footer
def draw_ticker_footer(img, draw):
    draw.rectangle([8, 968, 1016, 1006], fill=NAVY)
    tf = font(SANS_B, 20)
    draw.text((20, 976), "ALSO TODAY:", font=tf, fill=GOLD)
    ticker = ("Ebola in DR Congo passes 11,000 cases  ·  Nvidia: record "
              "$115.8B quarter  ·  Israel elects Kahana speaker")
    size = 20
    sf = font(SANS, size)
    while draw.textlength(ticker, font=sf) > 1016 - 178 - 16 and size > 10:
        size -= 1
        sf = font(SANS, size)
    draw.text((178, 976), ticker, font=sf, fill=(235, 235, 230))
    ff = font(SANS, 12)
    draw.text((8, 1010),
              "Sources: Reuters · Associated Press · AFP · NASA · WHO.  "
              "Every scene drawn by code — no photographs.",
              font=ff, fill=GREY)
    rf = font(SANS_B, 12)
    tag = "ONE IMAGE · ONE DAY · 18 NOV 2026"
    draw.text((W - 8 - draw.textlength(tag, font=rf), 1010), tag,
              font=rf, fill=GREY)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw = draw_hero(img, draw)
    draw_summit(img, draw)
    draw_bridge(img, draw)
    draw_senate(img, draw)
    draw_measles(img, draw)
    draw_voyager(img, draw)
    draw_ticker_footer(img, draw)
    img.convert("RGB").save(out, "PNG", optimize=True)


if __name__ == "__main__":
    main()
