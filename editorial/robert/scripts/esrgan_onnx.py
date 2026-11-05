"""Convert Real-ESRGAN 'realesr-general-x4v3' (SRVGGNetCompact) .pth -> ONNX WITHOUT PyTorch,
then upscale images with onnxruntime (CPU, tiled). Usage:
  python esrgan_onnx.py convert <model.pth> <model.onnx>
  python esrgan_onnx.py run <model.onnx> <in.jpg> <out.jpg> [scale_keep]
"""
import sys, zipfile, pickle, numpy as np


class _Storage:
    def __init__(self, key, dtype):
        self.key, self.dtype = key, dtype


def load_pth(path):
    zf = zipfile.ZipFile(path)
    root = zf.namelist()[0].split("/")[0]
    DT = {"FloatStorage": np.float32, "HalfStorage": np.float16}

    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == "_rebuild_tensor_v2":
                def rebuild(storage, offset, size, stride, *a):
                    buf = np.frombuffer(zf.read(f"{root}/data/{storage.key}"), dtype=storage.dtype)
                    n = int(np.prod(size)) if size else 1
                    arr = np.lib.stride_tricks.as_strided(buf[offset:], shape=size, strides=[s * buf.itemsize for s in stride]) if size else buf[offset:offset + 1]
                    return np.array(arr, dtype=np.float32).reshape(size)
                return rebuild
            if name in DT:
                return name
            if mod == "collections" and name == "OrderedDict":
                import collections
                return collections.OrderedDict
            return super().find_class(mod, name)

        def persistent_load(self, pid):
            _, stype, key, loc, numel = pid
            return _Storage(key, DT.get(stype if isinstance(stype, str) else stype.__name__, np.float32))

    sd = U(zf.open(f"{root}/data.pkl")).load()
    return sd.get("params_ema", sd.get("params", sd))


def convert(pth, onnx_path):
    import onnx
    from onnx import helper, TensorProto, numpy_helper
    sd = load_pth(pth)
    idx = sorted({int(k.split(".")[1]) for k in sd})
    nodes, inits = [], []
    x = "input"
    for i in idx:
        w = sd[f"body.{i}.weight"]
        name = f"b{i}"
        if w.ndim == 4:  # conv
            inits += [numpy_helper.from_array(w, f"{name}_w"), numpy_helper.from_array(sd[f"body.{i}.bias"], f"{name}_b")]
            nodes.append(helper.make_node("Conv", [x, f"{name}_w", f"{name}_b"], [name], pads=[1, 1, 1, 1], kernel_shape=[3, 3]))
        else:            # prelu (per channel)
            inits.append(numpy_helper.from_array(w.reshape(-1, 1, 1), f"{name}_a"))
            nodes.append(helper.make_node("PRelu", [x, f"{name}_a"], [name]))
        x = name
    # pixel shuffle x4 : DepthToSpace (CRD mode == torch pixel_shuffle)
    nodes.append(helper.make_node("DepthToSpace", [x], ["ps"], blocksize=4, mode="CRD"))
    inits.append(numpy_helper.from_array(np.array([1, 1, 4, 4], np.float32), "scales"))
    nodes.append(helper.make_node("Resize", ["input", "", "scales"], ["up"], mode="nearest"))
    nodes.append(helper.make_node("Add", ["ps", "up"], ["output"]))
    g = helper.make_graph(nodes, "srvgg", [helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 3, None, None])],
                          [helper.make_tensor_value_info("output", TensorProto.FLOAT, [1, 3, None, None])], inits)
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 13)])
    onnx.save(m, onnx_path)
    print("saved", onnx_path, len(nodes), "nodes")


def run(onnx_path, src, dst, keep=3, tile=384, pad=12):
    import onnxruntime as ort, cv2, os
    so = ort.SessionOptions(); so.intra_op_num_threads = os.cpu_count()
    s = ort.InferenceSession(onnx_path, so, providers=["CPUExecutionProvider"])
    img = cv2.imread(src)
    x = img[..., ::-1].astype(np.float32).transpose(2, 0, 1)[None] / 255
    _, _, h, w = x.shape
    out = np.zeros((1, 3, h * 4, w * 4), np.float32)
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            ya, xa, yb, xb = max(y0 - pad, 0), max(x0 - pad, 0), min(y0 + tile + pad, h), min(x0 + tile + pad, w)
            o = s.run(None, {"input": x[..., ya:yb, xa:xb]})[0]
            th, tw = (min(y0 + tile, h) - y0) * 4, (min(x0 + tile, w) - x0) * 4
            oy, ox = (y0 - ya) * 4, (x0 - xa) * 4
            out[..., y0 * 4:y0 * 4 + th, x0 * 4:x0 * 4 + tw] = o[..., oy:oy + th, ox:ox + tw]
    o = (np.clip(out[0].transpose(1, 2, 0), 0, 1)[..., ::-1] * 255).round().astype(np.uint8)
    if keep != 4:
        o = cv2.resize(o, (w * keep, h * keep), interpolation=cv2.INTER_AREA)
    cv2.imwrite(dst, o, [cv2.IMWRITE_JPEG_QUALITY, 93])


if __name__ == "__main__":
    if sys.argv[1] == "convert":
        convert(sys.argv[2], sys.argv[3])
    else:
        run(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 3)
