# Fit a cut-out sprite (768x1344 generation, transparent) to the engine format: crop to the figure,
# scale with one fixed factor so all characters keep the same size, height 1000, figure standing on the bottom.
# usage: prep_sprite.py in.png out.png [--flip]
import sys
from PIL import Image

STANDING_H = 1260          # height of a standing full-body figure in a 768x1344 generation -> 1000 px in the engine
K = 1000 / STANDING_H

im = Image.open(sys.argv[1]).convert("RGBA")
if "--flip" in sys.argv: im = im.transpose(Image.FLIP_LEFT_RIGHT)          # engine expects sprites facing RIGHT
fig = im.crop(im.getbbox())
fig = fig.resize((round(fig.width * K), round(fig.height * K)), Image.LANCZOS)
if fig.height > 1000:                                                       # taller than standard: fit height
    fig = fig.resize((round(fig.width * 1000 / fig.height), 1000), Image.LANCZOS)
out = Image.new("RGBA", (fig.width + 20, 1000), (0, 0, 0, 0))
out.alpha_composite(fig, (10, 1000 - fig.height))
out.save(sys.argv[2], optimize=True)
print(sys.argv[2], out.size)
