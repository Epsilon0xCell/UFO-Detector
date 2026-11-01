#!/usr/bin/env python3
"""UFO-Detector intro banner: a sunset watched from a pier, wordless. Pier boards
run away from the viewer, copper green rails converge from both lower corners.
Binoculars hang swaying on the right rail; a folded stool and thermos wait on the
left. Watchers stand with their backs to us along the rail, one telescope tripod
among them, a weather vane on the pier head pole. The sun sits half below the
horizon throwing a gold path on rain grey water, cloud layers stacked in violet
and copper, and on top of the sun's last segment a brief emerald flare, held.
No text, no signage, no lettering of any sort."""
import sys, random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
random.seed(29)
W, H = 1600, 900
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
VIOLET = (52, 38, 84); COPPER = (176, 102, 62); GOLD = (242, 165, 65); SEA = (96, 102, 110)
EMERALD = (16, 224, 122); RAIL = (56, 112, 92)
img = Image.new("RGB", (W, H), VIOLET); d = ImageDraw.Draw(img, "RGBA")
HZ = 520  # horizon line
# sky: violet overhead grading to gold at the horizon, cloud strips in between
for y in range(HZ):
    t = y / HZ
    r = int(52 + (242 - 52) * t ** 2.4); g = int(38 + (165 - 38) * t ** 2.4); b = int(84 + (65 - 84) * t ** 2.4)
    d.line([(0, y), (W, y)], fill=(r, g, b))
for cy, ch, col, a in ((120, 26, (74, 54, 110), 200), (218, 20, (150, 84, 84), 190), (308, 24, (96, 66, 116), 200), (392, 16, (198, 116, 70), 170)):
    d.rectangle([0, cy, W, cy + ch], fill=col + (a,))
    d.rectangle([0, cy + ch, W, cy + ch + 4], fill=(255, 190, 110, 60))
# sea in rain grey with the gold path under the sun
for y in range(HZ, H):
    t = (y - HZ) / (H - HZ)
    d.line([(0, y), (W, y)], fill=(int(104 - 26 * t), int(108 - 26 * t), int(114 - 22 * t)))
gp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gp)
gd.polygon([(716, HZ), (884, HZ), (1010, H), (590, H)], fill=(242, 176, 80, 110))
for i in range(30):
    yy = HZ + 12 + i * 12; ww = 60 + i * 9
    gd.line([(800 - ww // 2, yy), (800 + ww // 2, yy)], fill=(255, 205, 110, random.randint(50, 130)), width=3)
img = Image.alpha_composite(img.convert("RGBA"), gp.filter(ImageFilter.GaussianBlur(6))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# sun half sunk at the horizon
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sun)
sd.ellipse([712, HZ - 88, 888, HZ + 88], fill=(255, 178, 74, 255))
sd.rectangle([0, HZ + 2, W, H], fill=(0, 0, 0, 0))
mask = Image.new("L", (W, H), 255); md = ImageDraw.Draw(mask); md.rectangle([0, HZ + 3, W, H], fill=0)
img.paste(sun, (0, 0), Image.composite(sun.split()[3], Image.new("L", (W, H), 0), mask))
d = ImageDraw.Draw(img, "RGBA")
d.line([(0, HZ + 1), (W, HZ + 1)], fill=(255, 214, 130, 200), width=2)
# the green flash: a small emerald flame with a straight base on the sun's last segment
fl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fl)
fw = 40 if v != "v1" else 34
import math as _m
_fp=[]
for _i in range(13):
    _t=_i/12; _hw=fw*(_m.sin(_m.pi*(0.10+0.80*_t))**0.7); _fp.append((800-_hw, HZ-78-50*_t))
for _i in range(12,-1,-1):
    _t=_i/12; _hw=fw*(_m.sin(_m.pi*(0.10+0.80*_t))**0.7); _fp.append((800+_hw, HZ-78-50*_t))
fd.polygon(_fp, fill=EMERALD + (255,))
fd.ellipse([800 - fw - 22, HZ - 128, 800 + fw + 22, HZ - 70], fill=EMERALD + (70,))
img = Image.alpha_composite(img.convert("RGBA"), fl.filter(ImageFilter.GaussianBlur(3))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
fd2 = ImageDraw.Draw(img, "RGBA")
fd2.polygon(_fp, fill=EMERALD + (255,))
_fp2=[]
for _i in range(13):
    _t=_i/12; _hw=(fw//2)*(_m.sin(_m.pi*(0.10+0.80*_t))**0.7); _fp2.append((800-_hw, HZ-78-34*_t))
for _i in range(12,-1,-1):
    _t=_i/12; _hw=(fw//2)*(_m.sin(_m.pi*(0.10+0.80*_t))**0.7); _fp2.append((800+_hw, HZ-78-34*_t))
fd2.polygon(_fp2, fill=(190, 255, 220, 255))
# pier boards running away, converging to centre distance
d.polygon([(0, H), (560, HZ + 66), (1040, HZ + 66), (W, H)], fill=(104, 96, 88, 255))
for i in range(9):
    t = i / 8; x0 = 90 + t * 0 + i * 0; 
    lx = (i / 8) * W
    d.line([(lx, H), (560 + (i / 8) * 480, HZ + 66)], fill=(70, 62, 54, 255), width=4)
for i in range(6):
    yy = HZ + 80 + i * i * 9 + i * 26
    if yy < H: d.line([(560 - (yy - HZ) * 1.35, yy), (1040 + (yy - HZ) * 1.35, yy)], fill=(70, 62, 54, 200), width=3)
# rails entering from both lower corners, converging
for s in (-1, 1):
    x_top = 800 + s * 218; x_bot = 800 + s * 790
    d.line([(x_bot, H - 40), (x_top, HZ + 92)], fill=RAIL + (255,), width=13)
    for t in (0.25, 0.5, 0.75, 0.97):
        px_, py_ = x_bot + (x_top - x_bot) * t, (H - 40) + (HZ + 92 - (H - 40)) * t
        d.line([(px_, py_), (px_, py_ + 44 * (1 - t) + 14)], fill=(44, 92, 74, 255), width=9)
# watchers: backs to the viewer, spaced along the rail
def watcher(cx, cy, s, coat):
    d.ellipse([cx - 11 * s, cy - 96 * s, cx + 11 * s, cy - 74 * s], fill=(18, 16, 22, 255))  # head
    d.polygon([(cx - 20 * s, cy), (cx - 16 * s, cy - 76 * s), (cx + 16 * s, cy - 76 * s), (cx + 20 * s, cy)], fill=coat + (255,))
    d.rectangle([cx - 15 * s, cy, cx - 5 * s, cy + 34 * s], fill=(16, 14, 20, 255))
    d.rectangle([cx + 5 * s, cy, cx + 15 * s, cy + 34 * s], fill=(16, 14, 20, 255))
for cx, cy, s, coat in ((600, 616, 1.0, (34, 30, 44)), (700, 602, 0.88, (44, 34, 34)), (905, 600, 0.9, (30, 36, 46)), (1010, 614, 1.0, (40, 32, 40)), (352, 668, 1.25, (36, 32, 48)), (1252, 664, 1.22, (32, 38, 44))):
    watcher(cx, cy, s, coat)
# telescope tripod among them, capped
tx, ty = 786, 596
d.line([(tx, ty - 44), (tx - 22, ty + 26)], fill=(20, 18, 22, 255), width=5)
d.line([(tx, ty - 44), (tx + 22, ty + 26)], fill=(20, 18, 22, 255), width=5)
d.line([(tx - 6, ty - 66), (tx + 30, ty - 50)], fill=(24, 22, 26, 255), width=11)
d.ellipse([tx + 26, ty - 56, tx + 36, ty - 44], fill=(24, 22, 26, 255))
# weather vane on the pier head pole, arrow holding steady
d.line([(1086, 560), (1086, 452)], fill=(30, 28, 30, 255), width=5)
d.polygon([(1086, 458), (1136, 470), (1086, 482), (1096, 470)], fill=(16, 14, 18, 255))
d.polygon([(1086, 462), (1070, 470), (1086, 478)], fill=(16, 14, 18, 255))
# binoculars hanging by their strap on the right rail, swaying a degree
bx, by = 1330, 706
d.line([(1322, 640), (bx - 4, by - 40)], fill=(20, 18, 20, 255), width=4)
d.line([(1346, 644), (bx + 6, by - 40)], fill=(20, 18, 20, 255), width=4)
d.rounded_rectangle([bx - 36, by - 42, bx - 5, by + 16], 9, fill=(22, 20, 24, 255))
d.rounded_rectangle([bx + 5, by - 42, bx + 36, by + 16], 9, fill=(22, 20, 24, 255))
d.rectangle([bx - 7, by - 44, bx + 7, by - 28], fill=(22, 20, 24, 255))
d.ellipse([bx - 29, by - 2, bx - 12, by + 12], fill=(52, 66, 84, 255))
d.ellipse([bx + 12, by - 2, bx + 29, by + 12], fill=(52, 66, 84, 255))
# folded stool and thermos on the left where a watcher left them
sx, sy = 218, 756
d.line([(sx, sy), (sx + 52, sy - 40)], fill=(26, 24, 26, 255), width=6)
d.line([(sx + 52, sy), (sx, sy - 40)], fill=(26, 24, 26, 255), width=6)
d.rectangle([sx - 4, sy - 48, sx + 56, sy - 38], fill=(30, 27, 30, 255))
d.rounded_rectangle([sx + 84, sy - 44, sx + 104, sy + 2], 6, fill=(120, 128, 132, 255))
d.rectangle([sx + 88, sy - 54, sx + 100, sy - 44], fill=(90, 96, 100, 255))
vg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(vg)
vd.rectangle([0, 0, W, H], fill=(10, 6, 24, 60)); vd.ellipse([-200, -300, W + 200, H + 100], fill=(0, 0, 0, 0))
img = Image.alpha_composite(img.convert("RGBA"), vg.filter(ImageFilter.GaussianBlur(100))).convert("RGB")
rng = np.random.default_rng(7); a = np.asarray(img).astype(np.int16)
img = Image.fromarray(np.clip(a + rng.normal(0, 3, a.shape[:2])[..., None], 0, 255).astype(np.uint8))
out = "intro-banner.png" if v == "ship" else f"scratch/intro-{v}.png"
img.save(out); print(out)
