import sys, glob, os, subprocess
from PIL import Image, ImageDraw
pdf, outdir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
tmp = f"{outdir}/_tmp"; os.makedirs(tmp, exist_ok=True)
for f in glob.glob(f"{tmp}/*"): os.remove(f)
subprocess.run(["pdftoppm", "-r", "30", "-jpeg", pdf, f"{tmp}/p"], check=True)
fs = sorted(glob.glob(f"{tmp}/p-*.jpg")); ims = [Image.open(f) for f in fs]; w, h = ims[0].size
for part in range(4):
    sub = ims[part*24:(part+1)*24]; cols = 8
    S = Image.new("RGB", (cols*(w+4), 3*(h+14)), (60, 60, 60)); d = ImageDraw.Draw(S)
    for i, im in enumerate(sub):
        x, y = (i % cols)*(w+4), (i//cols)*(h+14); S.paste(im, (x, y+12)); d.text((x+2, y), str(part*24+i+1), fill="white")
    S.save(f"{outdir}/{prefix}-{part*24+1:02d}-{part*24+24:02d}.jpg", quality=85)
for f in fs: os.remove(f)
os.rmdir(tmp)
