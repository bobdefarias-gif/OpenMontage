"""Classical HD resample of the plates (no AI): Lanczos x2.4 + edge-preserving cleanup + unsharp mask.
Gives every crop enough pixels for >= 300 dpi at its printed size in the KDP books."""
import cv2, glob, os, numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f"{R}/plates_hd", exist_ok=True)
for f in sorted(glob.glob(f"{R}/plates/[0-9][0-9].jpg")):
    im = cv2.imread(f)
    im = cv2.fastNlMeansDenoisingColored(im, None, 3, 3, 7, 21)            # remove phone noise before enlarging
    h, w = im.shape[:2]
    up = cv2.resize(im, (int(w * 2.4), int(h * 2.4)), interpolation=cv2.INTER_LANCZOS4)
    blur = cv2.GaussianBlur(up, (0, 0), 2.2)
    up = cv2.addWeighted(up, 1.55, blur, -0.55, 0)                         # restore edge crispness
    cv2.imwrite(f"{R}/plates_hd/{os.path.basename(f)}", up, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print(os.path.basename(f), up.shape[1], "x", up.shape[0], flush=True)
