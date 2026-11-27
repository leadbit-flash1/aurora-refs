# save_bg.py <src.png> <bg_name>: keeps the PNG in aurora-refs/outputs/bg and writes the engine JPG to v3/newtex
import sys, shutil
from PIL import Image
src, name = sys.argv[1], sys.argv[2]
shutil.copy(src, f"/home/claude/aurora-refs/outputs/bg/{name}.png")
im = Image.open(src).convert("RGB"); assert im.size == (768, 1344), im.size
im.save(f"/home/claude/aurora_full_v3/newtex/{name}.jpg", quality=88, optimize=True)
print(name, "saved")
