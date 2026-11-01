#!/usr/bin/env python3
"""UFO-Detector logo: a pier railing head on at sunset, two posts and one rail in
weathered copper green, binoculars resting on the rail pointing out of the
picture. Behind it the sea as flat bands: rain grey water, a narrowing band of
sunset gold, and at the line where sun meets water a short bright emerald
segment flaring upward. That segment is the mark. Title underneath in Arbutus
Slab, lightning white on thunderhead violet, like wording cast into a plaque.
At small size the binoculars drop and rail, horizon, and flare carry it."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W = H = 1024
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
VIOLET = (52, 38, 84); WHITE = (248, 247, 255); EMERALD = (16, 224, 122); RAIL = (58, 116, 94)
img = Image.new("RGB", (W, H), VIOLET); d = ImageDraw.Draw(img, "RGBA")
HZ = 400
for y in range(HZ):
    t = y / HZ
    d.line([(0, y), (W, y)], fill=(int(52 + 150 * t ** 2), int(38 + 104 * t ** 2), int(84 - 10 * t)))
for y in range(HZ, 560):
    d.line([(0, y), (W, y)], fill=(100, 106, 112))
d.rectangle([0, HZ - 26, W, HZ], fill=(242, 165, 65, 255))  # narrowing gold band at the line
# emerald segment at the exact line, taller than the band around it
fw = 92
d.polygon([(512 - fw, HZ - 24), (512 - fw // 3, HZ - 96), (512, HZ - 122), (512 + fw // 3, HZ - 96), (512 + fw, HZ - 24)], fill=EMERALD + (255,))
d.polygon([(512 - fw // 2, HZ - 24), (512 - fw // 6, HZ - 70), (512, HZ - 88), (512 + fw // 6, HZ - 70), (512 + fw // 2, HZ - 24)], fill=(190, 255, 220, 255))
# railing head on: two posts, one horizontal rail
d.rectangle([196, 420, 240, 560], fill=RAIL + (255,)); d.rectangle([784, 420, 828, 560], fill=RAIL + (255,))
d.rectangle([150, 436, 874, 480], fill=RAIL + (255,))
d.rectangle([150, 436, 874, 452], fill=(84, 142, 116, 255))
for px_ in (205, 793):
    d.ellipse([px_ + 8, 444, px_ + 24, 460], fill=(30, 62, 50, 255))
# binoculars resting on the rail, pointing out of the picture (drawn from behind)
bx, by = 300, 440
d.rounded_rectangle([bx - 74, by - 62, bx - 10, by + 8], 14, fill=(20, 18, 22, 255))
d.rounded_rectangle([bx + 10, by - 62, bx + 74, by + 8], 14, fill=(20, 18, 22, 255))
d.rectangle([bx - 14, by - 56, bx + 14, by - 20], fill=(20, 18, 22, 255))
d.ellipse([bx - 62, by - 54, bx - 22, by - 14], fill=(52, 66, 84, 255))
d.ellipse([bx + 22, by - 54, bx + 62, by - 14], fill=(52, 66, 84, 255))
# plaque ground below, title cast into it
d.rectangle([0, 560, W, H], fill=VIOLET + (255,))
d.rectangle([0, 560, W, 566], fill=(84, 142, 116, 255))
f = ImageFont.truetype("fonts/ArbutusSlab.ttf", 96 if v != "v1" else 78)
txt = "UFO-Detector"
tw = d.textlength(txt, font=f)
d.text(((W - tw) / 2, 700), txt, font=f, fill=WHITE)
for bx_ in (70, W - 70):
    d.ellipse([bx_ - 11, 726, bx_ + 11, 748], fill=(150, 150, 160, 255))
rng = np.random.default_rng(6); a = np.asarray(img).astype(np.int16)
img = Image.fromarray(np.clip(a + rng.normal(0, 3, a.shape[:2])[..., None], 0, 255).astype(np.uint8))
out = "logo.png" if v == "ship" else f"scratch/logo-{v}.png"
img.save(out)
img.resize((64, 64), Image.LANCZOS).save("scratch/logo64-ship.png" if v == "ship" else f"scratch/logo64-{v}.png")
print(out)
