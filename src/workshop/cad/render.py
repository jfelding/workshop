"""Render CAD solids into the assembly guides' drawing style: flat fills plus black outlines.

Fills come from a small z-buffer rasteriser (embedded as a PNG), outlines from OpenCASCADE
hidden-line removal (vector). Both use the same orthographic projection, so they line up.
Each solid belongs to a group that sets its fill, matching the guides' key:
'hi' = this step (yellow), 'done' = already fitted (grey), 'other' = other parts (white).
Nothing here is a dimension of any part; see methods/assembly-guides.md.
"""
import base64
import io

import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepLib import BRepLib
from OCP.GeomAbs import GeomAbs_Line
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS_Edge, TopoDS
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt

FILL = {'hi': (255, 210, 63), 'done': (214, 214, 208), 'other': (255, 255, 255)}
LINE = {'hi': 2.0, 'done': 1.3, 'other': 1.1}


def _unit(v):
    v = np.asarray(v, float)
    return v/np.linalg.norm(v)


class View:
    """Orthographic view. `d` points from the scene toward the viewer; `up` is roughly up on
    the page. Page x = right, page y = up (flipped to SVG y at output)."""
    def __init__(self, d, up=(0, 0, 1)):
        self.d = _unit(d)
        self.X = _unit(np.cross(up, self.d))
        self.Y = np.cross(self.d, self.X)

    def xy(self, p):
        p = np.asarray(p, float)
        return np.array([p @ self.X, p @ self.Y])


def _edges(compound):
    out = []
    if compound is None or compound.IsNull():
        return out
    BRepLib.BuildCurves3d_s(compound)
    ex = TopExp_Explorer(compound, TopAbs_EDGE)
    while ex.More():
        e = TopoDS.Edge(ex.Current()) if hasattr(TopoDS, "Edge") else TopoDS.Edge_s(ex.Current())
        c = BRepAdaptor_Curve(e)
        a, b = c.FirstParameter(), c.LastParameter()
        n = 2 if c.GetType() == GeomAbs_Line else 24
        pts = [c.Value(a + (b - a)*i/(n - 1)) for i in range(n)]
        out.append(np.array([[p.X(), p.Y()] for p in pts]))
        ex.Next()
    return out


def hlr(shapes, view):
    """Visible and hidden 2D polylines of the shapes, as seen together."""
    algo = HLRBRep_Algo()
    for s in shapes:
        algo.Add(s.wrapped)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*view.d), gp_Dir(*view.X))))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    vis = _edges(h.VCompound()) + _edges(h.OutLineVCompound())
    hid = _edges(h.HCompound()) + _edges(h.OutLineHCompound())
    return vis, hid


def _near(points, polys, tol):
    """For each point, is it within tol of any segment of polys?"""
    if not polys:
        return np.zeros(len(points), bool)
    a = np.concatenate([p[:-1] for p in polys])
    b = np.concatenate([p[1:] for p in polys])
    ab = b - a
    L2 = np.maximum((ab**2).sum(1), 1e-12)
    out = np.zeros(len(points), bool)
    for i, q in enumerate(points):
        t = np.clip(((q - a)*ab).sum(1)/L2, 0, 1)
        dist = np.linalg.norm(a + ab*t[:, None] - q, axis=1)
        out[i] = dist.min() < tol
    return out


def _mid(poly):
    seg = np.linalg.norm(np.diff(poly, axis=0), axis=1)
    if seg.sum() == 0:
        return poly[0]
    half, acc = seg.sum()/2, 0.0
    for i, s in enumerate(seg):
        if acc + s >= half:
            t = (half - acc)/s if s else 0
            return poly[i] + (poly[i+1] - poly[i])*t
        acc += s
    return poly[-1]


def raster(items, view, x0, y1, k, w, h):
    """RGBA image of the filled solids. items = [(shape, group)]."""
    zb = np.full((h, w), -np.inf)
    img = np.zeros((h, w, 4))
    light = _unit(view.d*0.8 + view.Y*0.5 + view.X*0.3)
    for shape, group in items:
        verts, tris = shape.tessellate(0.15, 0.3)
        if not tris:
            continue
        V = np.array([[v.X, v.Y, v.Z] for v in verts])
        T = np.array(tris)
        u = (V @ view.X - x0)*k
        v = (y1 - V @ view.Y)*k
        z = V @ view.d
        P = V[T]
        n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
        n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        shade = 0.80 + 0.20*np.abs(n @ light)
        base = np.array(FILL.get(group, group) if isinstance(group, str) else group)/255
        for (i, j, m), s in zip(T, shade):
            us, vs, zs = u[[i, j, m]], v[[i, j, m]], z[[i, j, m]]
            ua, ub = max(int(us.min()), 0), min(int(us.max()) + 1, w - 1)
            va, vb = max(int(vs.min()), 0), min(int(vs.max()) + 1, h - 1)
            if ua > ub or va > vb:
                continue
            det = (vs[1] - vs[2])*(us[0] - us[2]) + (us[2] - us[1])*(vs[0] - vs[2])
            if abs(det) < 1e-9:
                continue
            gx, gy = np.meshgrid(np.arange(ua, ub + 1) + 0.5, np.arange(va, vb + 1) + 0.5)
            l0 = ((vs[1] - vs[2])*(gx - us[2]) + (us[2] - us[1])*(gy - vs[2]))/det
            l1 = ((vs[2] - vs[0])*(gx - us[2]) + (us[0] - us[2])*(gy - vs[2]))/det
            l2 = 1 - l0 - l1
            inside = (l0 >= -1e-6) & (l1 >= -1e-6) & (l2 >= -1e-6)
            if not inside.any():
                continue
            zz = l0*zs[0] + l1*zs[1] + l2*zs[2]
            sub = zb[va:vb+1, ua:ub+1]
            upd = inside & (zz > sub)
            sub[upd] = zz[upd]
            col = img[va:vb+1, ua:ub+1]
            col[upd, :3] = base*s
            col[upd, 3] = 1
    return img


def _png(img, ss):
    import matplotlib.image as mpimg
    h, w = img.shape[0]//ss, img.shape[1]//ss
    small = img[:h*ss, :w*ss].reshape(h, ss, w, ss, 4).mean(axis=(1, 3))
    buf = io.BytesIO()
    mpimg.imsave(buf, np.clip(small, 0, 1), format='png')
    return base64.b64encode(buf.getvalue()).decode()


def render(items, view, width=640, hidden=(), notes=(), label=''):
    """SVG of the solids. items = [(shape, group)]; groups in `hidden` also show hidden edges
    dashed. notes = callables taking (to_svg) and returning SVG markup (labels, arrows)."""
    from build123d import Compound
    items = [(s if hasattr(s, 'wrapped') else Compound(list(s)), g) for s, g in items]
    shapes = [s for s, _ in items]
    vis, hid = hlr(shapes, view)
    pts = np.concatenate(vis + hid) if vis or hid else np.zeros((1, 2))
    x0, y0 = pts.min(0)
    x1, y1 = pts.max(0)
    k = width/(x1 - x0)                       # svg units per mm
    W, H = width, (y1 - y0)*k
    ss = 3                                    # supersampling for the fills
    img = raster(items, view, x0, y1, k*ss, int(W*ss) + 1, int(H*ss) + 1)

    def to_svg(p3):
        x, y = view.xy(p3)
        return (x - x0)*k, (y1 - y)*k

    # Which group owns each visible edge: test its midpoint against each group seen alone.
    groups = {}
    for s, g in items:
        groups.setdefault(g, []).append(s)
    solo = {g: sum(hlr(ss_, view), []) for g, ss_ in groups.items() if g in ('hi', 'done')}
    order = [g for g in ('hi', 'done') if g in solo]

    def owner(polys):
        mids = np.array([_mid(p) for p in polys]) if polys else np.zeros((0, 2))
        own = np.array(['other']*len(polys), dtype=object)
        free = np.ones(len(polys), bool)
        for g in order:
            hit = _near(mids, solo[g], 0.02) & free
            own[hit] = g
            free &= ~hit
        return own

    def path(poly):
        return 'M' + ' L'.join(f'{(x - x0)*k:.1f} {(y1 - y)*k:.1f}' for x, y in poly)

    body = f'<image x="0" y="0" width="{W:.1f}" height="{H:.1f}" href="data:image/png;base64,{_png(img, ss)}"/>'
    own = owner(vis)
    for g in ('other', 'done', 'hi'):
        d = ' '.join(path(p) for p, o in zip(vis, own) if o == g)
        if d:
            body += f'<path d="{d}" fill="none" stroke="#111" stroke-width="{LINE[g]}" stroke-linejoin="round" stroke-linecap="round"/>'
    if hidden:
        hown = owner(hid)
        d = ' '.join(path(p) for p, o in zip(hid, hown) if o in hidden)
        if d:
            body += f'<path d="{d}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="4 3"/>'
    for n in notes:
        body += n(to_svg)
    return body, (W, H)


# --- Annotation helpers (svg units; anchors are 3D points in mm) ---------------------------

def callout(p3, dx, dy, text, small=False, anchor=None):
    """Leader from a 3D point to text placed dx, dy away on the page."""
    def f(to_svg):
        x, y = to_svg(p3)
        tx, ty = x + dx, y + dy
        a = anchor or ('start' if dx >= 0 else 'end')
        cls = 'lbl s' if small else 'lbl'
        lines = text.split('\n')
        out = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#111"/>'
        out += f'<path class="o t" d="M{x:.1f} {y:.1f} L{tx:.1f} {ty:.1f}"/>'
        ox = 4 if a == 'start' else -4
        for i, s in enumerate(lines):
            out += f'<text class="{cls}" x="{tx + ox:.1f}" y="{ty + 5 + i*17:.1f}" text-anchor="{a}">{s}</text>'
        return out
    return f


def move(a3, b3, dashed=False):
    """Arrow (or dashed guide line) from one 3D point to another."""
    def f(to_svg):
        (x, y), (u, v) = to_svg(a3), to_svg(b3)
        if dashed:
            return f'<path class="o d" d="M{x:.1f} {y:.1f} L{u:.1f} {v:.1f}"/>'
        return f'<path class="o a" d="M{x:.1f} {y:.1f} L{u:.1f} {v:.1f}" marker-end="url(#ah)"/>'
    return f


def outline(points3, cls='o', fill=None, dash=False):
    """A polygon through 3D points (for things with no solid, such as a board outline)."""
    def f(to_svg):
        pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in (to_svg(p) for p in points3))
        st = f' style="fill:{fill}"' if fill else ''
        d = ' stroke-dasharray="5 4"' if dash else ''
        return f'<polygon class="{cls}" points="{pts}"{st}{d}/>'
    return f


def text_at(p3, s, small=False, anchor='middle', dy=0):
    def f(to_svg):
        x, y = to_svg(p3)
        return f'<text class="lbl{" s" if small else ""}" x="{x:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{s}</text>'
    return f
