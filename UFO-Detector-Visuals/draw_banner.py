#!/usr/bin/env python3
"""UFO-Detector wordmark banner: evening on a long pier, camera low, facing out
to sea along the boards. Watchers line both rails in silhouette, one seated on a
folding stool, a child on a parent's shoulders at the right, all facing away
toward the sun. The sun sits half sunk, sky graded gold at the horizon through
copper to thunderhead violet, thin cloud layers in horizontal strips. A capped
telescope stands at the left foreground rail, owner beside it with arms folded.
A wind sock on the pier head pole hangs nearly limp. Title painted in Arbutus
Slab along the pier side board in the lower foreground, lightning white,
weathered at the edges. The green flash has not happened yet: everyone waits."""
import sys, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
random.seed(53)
W, H = 2560, 640
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
HZ = 356
img = Image.new("RGB", (W, H), (52, 38, 84)); d = ImageDraw.Draw(img, "RGBA")
for y in range(HZ):
    t = y / HZ
    d.line([(0, y), (W, y)], fill=(int(52 + 190 * t ** 2.4), int(38 + 127 * t ** 2.4), int(84 - 19 * t)))
for cy, ch, col, a in ((70, 20, (74, 54, 110), 200), (140, 15, (150, 84, 84), 185), (212, 18, (96, 66, 116), 195), (272, 12, (198, 116, 70), 165)):
    d.rectangle([0, cy, W, cy + ch], fill=col + (a,))
for y in range(HZ, H):
    t = (y - HZ) / (H - HZ)
    d.line([(0, y), (W, y)], fill=(int(102 - 22 * t), int(106 - 22 * t), int(112 - 18 * t)))
gp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gp)
gd.polygon([(1190, HZ), (1370, HZ), (1520, H), (1040, H)], fill=(242, 176, 80, 100))
img = Image.alpha_composite(img.convert("RGBA"), gp.filter(ImageFilter.GaussianBlur(8))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# sun half sunk, no flash yet
sd = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sdd = ImageDraw.Draw(sd)
sdd.ellipse([1196, HZ - 84, 1364, HZ + 84], fill=(255, 178, 74, 255))
mask = Image.new("L", (W, H), 255); md = ImageDraw.Draw(mask); md.rectangle([0, HZ + 2, W, H], fill=0)
img.paste(sd, (0, 0), Image.composite(sd.split()[3], Image.new("L", (W, H), 0), mask))
d = ImageDraw.Draw(img, "RGBA")
# pier boards along the bottom, side board in the lower foreground
d.polygon([(0, H), (940, HZ + 40), (1620, HZ + 40), (W, H)], fill=(100, 92, 84, 255))
for i in range(11):
    lx = (i / 10) * W
    d.line([(lx, H), (940 + (i / 10) * 680, HZ + 40)], fill=(68, 60, 52, 255), width=4)
# rails along both sides converging
for s in (-1, 1):
    xt, xb = 1280 + s * 330, 1280 + s * 1240
    d.line([(xb, H - 96), (xt, HZ + 58)], fill=(56, 112, 92, 255), width=11)
    for t in (0.3, 0.6, 0.9):
        px_, py_ = xb + (xt - xb) * t, (H - 96) + (HZ + 58 - (H - 96)) * t
        d.line([(px_, py_), (px_, py_ + 36 * (1 - t) + 12)], fill=(44, 92, 74, 255), width=8)
def watcher(cx, cy, s, child=False):
    d.ellipse([cx - 10 * s, cy - 88 * s, cx + 10 * s, cy - 68 * s], fill=(16, 14, 20, 255))
    d.polygon([(cx - 18 * s, cy), (cx - 14 * s, cy - 68 * s), (cx + 14 * s, cy - 68 * s), (cx + 18 * s, cy)], fill=(18, 16, 22, 255))
    d.rectangle([cx - 13 * s, cy, cx - 4 * s, cy + 30 * s], fill=(14, 12, 18, 255))
    d.rectangle([cx + 4 * s, cy, cx + 13 * s, cy + 30 * s], fill=(14, 12, 18, 255))
    if child:  # small figure on the shoulders, legs either side of the head
        hy = cy - 92 * s
        d.ellipse([cx - 8 * s, hy - 34 * s, cx + 8 * s, hy - 16 * s], fill=(16, 14, 20, 255))
        d.polygon([(cx - 11 * s, hy), (cx - 9 * s, hy - 18 * s), (cx + 9 * s, hy - 18 * s), (cx + 11 * s, hy)], fill=(20, 17, 24, 255))
        d.line([(cx - 10 * s, hy - 2 * s), (cx - 16 * s, hy + 16 * s)], fill=(14, 12, 18, 255), width=int(5 * s))
        d.line([(cx + 10 * s, hy - 2 * s), (cx + 16 * s, hy + 16 * s)], fill=(14, 12, 18, 255), width=int(5 * s))
for cx, cy, s in ((1010, 442, 0.95), (1150, 428, 0.85), (1420, 430, 0.86), (1560, 444, 0.97)):
    watcher(cx, cy, s)
watcher(1990, 486, 1.3, child=True)   # parent with child on shoulders, right
watcher(560, 490, 1.3)
# seated watcher on a folding stool, left of centre
sx, sy = 830, 470
d.ellipse([sx - 11, sy - 84, sx + 11, sy - 62], fill=(16, 14, 20, 255))
d.polygon([(sx - 17, sy - 20), (sx - 14, sy - 62), (sx + 14, sy - 62), (sx + 17, sy - 20)], fill=(18, 16, 22, 255))
d.line([(sx - 12, sy - 22), (sx - 26, sy + 8)], fill=(14, 12, 18, 255), width=8)
d.line([(sx + 12, sy - 22), (sx + 24, sy + 8)], fill=(14, 12, 18, 255), width=8)
d.line([(sx - 22, sy + 22), (sx + 22, sy - 2)], fill=(22, 20, 22, 255), width=5)
d.line([(sx + 22, sy + 22), (sx - 22, sy - 2)], fill=(22, 20, 22, 255), width=5)
# capped telescope at left foreground rail, owner beside it, arms folded
tx, ty = 300, 430
d.line([(tx, ty - 30), (tx - 30, ty + 52)], fill=(18, 16, 20, 255), width=6)
d.line([(tx, ty - 30), (tx + 30, ty + 52)], fill=(18, 16, 20, 255), width=6)
d.line([(tx - 14, ty - 62), (tx + 44, ty - 38)], fill=(22, 20, 24, 255), width=15)
d.ellipse([tx + 38, ty - 48, tx + 52, ty - 32], fill=(22, 20, 24, 255))  # cap on
watcher(408, 452, 1.15)
d.line([(392, 408), (430, 424)], fill=(16, 14, 20, 255), width=9)  # folded arms
d.line([(430, 408), (394, 426)], fill=(16, 14, 20, 255), width=9)
# wind sock on the pier head pole, nearly limp
d.line([(2240, 470), (2240, 250)], fill=(26, 24, 26, 255), width=6)
d.polygon([(2240, 258), (2296, 268), (2292, 282), (2240, 276)], fill=(196, 120, 60, 255))
# side board with the painted title, lower foreground
d.rectangle([330, 548, 2230, 632], fill=(74, 66, 58, 255))
d.rectangle([330, 548, 2230, 556], fill=(56, 112, 92, 255))
f = ImageFont.truetype("fonts/ArbutusSlab.ttf", 62)
txt = "UFO-Detector"
tw = d.textlength(txt, font=f)
d.text(((W - tw) / 2, 560), txt, font=f, fill=(243, 242, 248, 235))
rng = np.random.default_rng(3)
for i in range(260):  # weathering flecks over the paint
    x, y = random.randint(340, 2220), random.randint(552, 628)
    d.point((x, y), fill=(74, 66, 58, 255))
a = np.asarray(img).astype(np.int16)
img = Image.fromarray(np.clip(a + rng.normal(0, 3, a.shape[:2])[..., None], 0, 255).astype(np.uint8))
out = "banner.png" if v == "ship" else f"scratch/banner-{v}.png"
img.save(out); print(out)
