# Cut a sprite out of a flat-colour background (e.g. sunset orange) into a transparent PNG.
# usage: python3 key_out.py input.png output.png
# The background colour is sampled from the top/bottom rows. Edges are soft and colour-decontaminated,
# and background-coloured details enclosed by the figure (e.g. orange stripes on clothes) are kept.
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src = np.array(Image.open(sys.argv[1]).convert("RGB")).astype(float)
bg = np.median(np.concatenate([src[:40].reshape(-1, 3), src[-40:].reshape(-1, 3)]), axis=0)
dist = np.sqrt(((src - bg) ** 2).sum(-1))
alpha = np.clip((dist - 18) / (45 - 18), 0, 1)                      # soft key

fg = alpha > 0.5                                                    # drop specks, keep big parts
lab, n = ndimage.label(fg)
sizes = ndimage.sum(fg, lab, range(1, n + 1))
alpha *= ndimage.binary_dilation(np.isin(lab, [i + 1 for i, v in enumerate(sizes) if v > 3000]), iterations=3)

A = np.clip(alpha, 1e-3, 1)[..., None]                              # remove background tint from edges
rgb = np.where(alpha[..., None] > 0.98, src, np.clip((src - (1 - A) * bg) / A, 0, 255))

holes = ndimage.binary_fill_holes(alpha > 0.5) & (alpha <= 0.5)    # bg-coloured areas enclosed by the figure
lab, n = ndimage.label(holes)
sizes = ndimage.sum(holes, lab, range(1, n + 1))
small = np.isin(lab, [i + 1 for i, v in enumerate(sizes) if v < 2500])   # small = clothing details; big = gaps (between legs)
small = ndimage.binary_dilation(small, iterations=3) & (alpha < 0.98)
rgb[small], alpha[small] = src[small], 1

Image.fromarray(np.dstack([rgb.astype(np.uint8), (alpha * 255).astype(np.uint8)]), "RGBA").save(sys.argv[2])
print("bg", bg.astype(int).tolist())
