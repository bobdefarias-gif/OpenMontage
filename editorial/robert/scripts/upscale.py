"""4x AI upscale of the plates (Real-ESRGAN x4plus, RRDBNet, CPU, tiled) -> plates_hd/NN.jpg

The drawing is not altered: the model only reconstructs edge/texture detail lost by the phone photo,
so pages reach >= 300 dpi at their printed size (KDP requirement).
"""
import os, sys, glob, numpy as np, cv2, torch, torch.nn as nn, torch.nn.functional as F

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.environ.get("ESRGAN", "/home/user/models/RealESRGAN_x4plus.pth")


class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__()
        s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1)
        s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1); s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)

    def forward(s, x):
        x1 = s.l(s.conv1(x)); x2 = s.l(s.conv2(torch.cat((x, x1), 1)))
        x3 = s.l(s.conv3(torch.cat((x, x1, x2), 1))); x4 = s.l(s.conv4(torch.cat((x, x1, x2, x3), 1)))
        return s.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x


class RRDB(nn.Module):
    def __init__(s, nf=64):
        super().__init__(); s.rdb1 = RDB(nf); s.rdb2 = RDB(nf); s.rdb3 = RDB(nf)

    def forward(s, x):
        return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x


class Net(nn.Module):
    def __init__(s, nf=64, nb=23):
        super().__init__()
        s.conv_first = nn.Conv2d(3, nf, 3, 1, 1)
        s.body = nn.Sequential(*[RRDB(nf) for _ in range(nb)])
        s.conv_body = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_up1 = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_up2 = nn.Conv2d(nf, nf, 3, 1, 1)
        s.conv_hr = nn.Conv2d(nf, nf, 3, 1, 1); s.conv_last = nn.Conv2d(nf, 3, 3, 1, 1)
        s.l = nn.LeakyReLU(0.2, True)

    def forward(s, x):
        f = s.conv_first(x); f = f + s.conv_body(s.body(f))
        f = s.l(s.conv_up1(F.interpolate(f, scale_factor=2, mode="nearest")))
        f = s.l(s.conv_up2(F.interpolate(f, scale_factor=2, mode="nearest")))
        return s.conv_last(s.l(s.conv_hr(f)))


def load():
    m = Net(); sd = torch.load(W, map_location="cpu")
    m.load_state_dict(sd.get("params_ema", sd.get("params", sd)), strict=True)
    return m.eval()


@torch.no_grad()
def upscale(m, img, tile=256, pad=16):
    x = torch.from_numpy(img[..., ::-1].astype(np.float32) / 255).permute(2, 0, 1)[None]
    _, _, h, w = x.shape
    out = torch.zeros(1, 3, h * 4, w * 4)
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            ya, xa = max(y0 - pad, 0), max(x0 - pad, 0)
            yb, xb = min(y0 + tile + pad, h), min(x0 + tile + pad, w)
            o = m(x[..., ya:yb, xa:xb])
            oy, ox = (y0 - ya) * 4, (x0 - xa) * 4
            th, tw = (min(y0 + tile, h) - y0) * 4, (min(x0 + tile, w) - x0) * 4
            out[..., y0 * 4:y0 * 4 + th, x0 * 4:x0 * 4 + tw] = o[..., oy:oy + th, ox:ox + tw]
    o = (out[0].clamp(0, 1).permute(1, 2, 0).numpy()[..., ::-1] * 255).round().astype(np.uint8)
    return o


if __name__ == "__main__":
    torch.set_num_threads(os.cpu_count())
    os.makedirs(f"{R}/plates_hd", exist_ok=True)
    m = load()
    keys = sys.argv[1:] or [os.path.basename(f)[:-4] for f in sorted(glob.glob(f"{R}/plates/[0-9][0-9].jpg"))]
    for k in keys:
        dst = f"{R}/plates_hd/{k}.jpg"
        if os.path.exists(dst):
            continue
        img = cv2.imread(f"{R}/plates/{k}.jpg")
        up = upscale(m, img)
        # keep x3 (≈ 5600 px wide): plenty for 300 dpi at full page width, lighter files
        h, w = img.shape[:2]
        up = cv2.resize(up, (w * 3, h * 3), interpolation=cv2.INTER_AREA)
        cv2.imwrite(dst, up, [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(k, up.shape, flush=True)
