"""Visible-ink KDP margin check: rasterize each page at 72 dpi (1 px = 1 pt) and look for ink inside the
band between the trim (9 pt) and the safe line (36 pt) that differs from the bleed colour on the same row/column."""
import fitz, sys, numpy as np
for f in sys.argv[1:]:
    d = fitz.open(f); bad = []
    for i, p in enumerate(d):
        pix = p.get_pixmap(dpi=72)
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)[..., :3].astype(int)
        h, w = a.shape[:2]
        n = 0
        L = np.abs(a[:, 10:35] - a[:, 3:4]).sum(2) > 60; n += L[40:h - 40].sum()
        Rr = np.abs(a[:, w - 35:w - 10] - a[:, w - 4:w - 3]).sum(2) > 60; n += Rr[40:h - 40].sum()
        T = np.abs(a[10:35] - a[3:4]).sum(2) > 60; n += T[:, 40:w - 40].sum()
        B = np.abs(a[h - 35:h - 10] - a[h - 4:h - 3]).sum(2) > 60; n += B[:, 40:w - 40].sum()
        if n > 0:
            bad.append((i + 1, int(n)))
    print(f.split("/")[-1], "OK" if not bad else bad)
