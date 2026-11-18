"""Render an STL to a PNG so a model can be eyeballed before printing.

    uv run ws-preview cad/exports/bracket.stl [more.stl ...]

Not a substitute for opening the file in the slicer: a fast check that the geometry is
roughly what was intended, with no scale or orientation surprises.
"""
import pathlib
import sys

import matplotlib
import numpy as np
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from stl import mesh as stlmesh  # noqa: E402


BASE = np.array([0.66, 0.76, 0.88])   # part colour; shading scales it
INK = np.array([0.13, 0.18, 0.25])     # outline colour
VIEWS = (("from above", (1.0, -1.0, 0.8)), ("from below", (1.0, -1.0, -0.8)))


def _axes(d):
    d = np.asarray(d, float) / np.linalg.norm(d)
    x = np.cross((0, 0, 1), d)
    x /= np.linalg.norm(x)
    return d, x, np.cross(d, x)


def _raster(tris, d, px, ss=2):
    """Per-pixel depth test of the triangles seen along -d (orthographic). Returns an RGB image:
    shaded faces, dark outlines where the visible surface folds (>25°) or steps in depth."""
    d, X, Y = _axes(d)
    pts = tris.reshape(-1, 3)
    u_all, v_all = pts @ X, pts @ Y
    k = (px * ss - 8 * ss) / max(np.ptp(u_all), np.ptp(v_all))
    w = int(np.ptp(u_all) * k) + 8 * ss
    h = int(np.ptp(v_all) * k) + 8 * ss
    u = (tris @ X - u_all.min()) * k + 4 * ss
    v = (v_all.max() - tris @ Y) * k + 4 * ss
    z = tris @ d
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    zb = np.full((h, w), -np.inf)
    face = np.full((h, w), -1)
    for f in np.flatnonzero(n @ d > 1e-9):   # front faces only
        us, vs, zs = u[f], v[f], z[f]
        ua, ub = max(int(us.min()), 0), min(int(us.max()) + 1, w - 1)
        va, vb = max(int(vs.min()), 0), min(int(vs.max()) + 1, h - 1)
        det = (vs[1] - vs[2]) * (us[0] - us[2]) + (us[2] - us[1]) * (vs[0] - vs[2])
        if ua > ub or va > vb or abs(det) < 1e-12:
            continue
        gx, gy = np.meshgrid(np.arange(ua, ub + 1) + 0.5, np.arange(va, vb + 1) + 0.5)
        l0 = ((vs[1] - vs[2]) * (gx - us[2]) + (us[2] - us[1]) * (gy - vs[2])) / det
        l1 = ((vs[2] - vs[0]) * (gx - us[2]) + (us[0] - us[2]) * (gy - vs[2])) / det
        l2 = 1 - l0 - l1
        zz = l0 * zs[0] + l1 * zs[1] + l2 * zs[2]
        sub = zb[va:vb + 1, ua:ub + 1]
        upd = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6) & (zz > sub)
        sub[upd] = zz[upd]
        face[va:vb + 1, ua:ub + 1][upd] = f
    light = d * 0.6 + Y * 0.6 + X * 0.3
    light /= np.linalg.norm(light)
    shade = 0.55 + 0.45 * np.clip(n @ light, 0, 1)
    img = np.ones((h, w, 3))
    hit = face >= 0
    img[hit] = BASE * shade[face[hit], None]
    zb[~hit] = 0
    nf = np.where(hit[..., None], n[np.maximum(face, 0)], 0)
    edge = np.zeros((h, w), bool)
    for dy, dx in ((0, 1), (1, 0)):
        a = (slice(0, h - dy), slice(0, w - dx))
        b = (slice(dy, h), slice(dx, w))
        differ = hit[a] != hit[b]
        both = hit[a] & hit[b] & (face[a] != face[b])
        fold = both & ((nf[a] * nf[b]).sum(-1) < np.cos(np.radians(25)))
        jump = both & (np.abs(zb[a] - zb[b]) > 0.6)   # a 0.6 mm step in depth
        e = differ | fold | jump
        edge[a] |= e
    img[edge] = INK
    return img[:h - h % ss, :w - w % ss].reshape(h // ss, ss, w // ss, ss, 3).mean(axis=(1, 3))


def preview(src, dst=None, px=520):
    """Two views of the STL, from above and from below, titled with its name and size."""
    src = pathlib.Path(src)
    tris = stlmesh.Mesh.from_file(str(src)).vectors.astype(float)
    pts = tris.reshape(-1, 3)
    size = pts.max(axis=0) - pts.min(axis=0)
    fig, axes = plt.subplots(1, 2, figsize=(2 * px / 100, px / 100 + 0.8), dpi=100)
    for ax, (title, d) in zip(axes, VIEWS):
        ax.imshow(_raster(tris, d, px), interpolation="none")
        ax.set_title(title, fontsize=10, color="#555")
        ax.set_axis_off()
    fig.suptitle(f"{src.stem}   {size[0]:.1f} × {size[1]:.1f} × {size[2]:.1f} mm", fontsize=14)
    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.88, wspace=0.04)
    dst = pathlib.Path(dst) if dst else src.with_suffix(".png")
    fig.savefig(dst)
    plt.close(fig)
    print(f"wrote {dst}")
    return dst


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        preview(p)


if __name__ == "__main__":
    main()
