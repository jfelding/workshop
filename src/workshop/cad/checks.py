"""Checks against the solid, not the picture (methods/cad-in-code.md, "Checking a part").

The render and the STL preview hide exactly the mistakes that matter. These answer with
numbers: overlap volume with a keep-out, material thickness at a named thin place, overhang
area in print orientation, whether a part fits the bed, and a solid of revolution that
contains a part at every angle of a joint, for clearance checks over a whole rotation.
"""
import math

import numpy as np
from build123d import Edge, ShapeList, Vector

from .geometry import box, cylinder

VOLUME_TOL = 1e-5   # mm³; below this an intersection is a touching face, not an overlap


def volume(shape):
    """Solid volume of a shape, list of shapes or None (faces and edges count zero)."""
    if shape is None:
        return 0.0
    if isinstance(shape, (ShapeList, list, tuple)):
        return sum(volume(s) for s in shape)
    return sum(abs(s.volume) for s in shape.solids())


def boxes_touch(a, b):
    """Cheap pre-test: do the bounding boxes overlap? Skip the boolean when they do not."""
    aa, bb = a.bounding_box(), b.bounding_box()
    return all(x1 >= y0 and y1 >= x0 for x0, x1, y0, y1 in zip(aa.min, aa.max, bb.min, bb.max))


def overlap(part, keepout):
    """Volume (mm³) of `part` inside `keepout`. Zero is the only passing answer for a clearance."""
    if not boxes_touch(part, keepout):
        return 0.0
    v = volume(part.intersect(keepout))
    return 0.0 if v < VOLUME_TOL else v


def assert_clear(pairs):
    """`pairs` = [(label, part, keepout), ...]. Raises listing every overlap, or returns quietly."""
    bad = [(label, v) for label, a, b in pairs if (v := overlap(a, b)) > 0]
    if bad:
        raise AssertionError('overlaps: ' + '; '.join(f'{label} {v:.3f} mm³' for label, v in bad))


def probe(part, p0, p1):
    """Material thickness along the line from p0 (inside a hole or just outside a face) toward p1.

    Quote the number with the probe's name; it is the wall the printer actually has to make.
    """
    hit = Edge.make_line(p0, p1).intersect(part)
    edges = [] if hit is None else (hit.edges() if hasattr(hit, 'edges') else [e for h in hit for e in h.edges()])
    if not edges:
        return 0.0
    start = Vector(*p0)
    first = min(edges, key=lambda e: min((v - start).length for v in (e.position_at(0), e.position_at(1))))
    return first.length


def overhangs(part, z_bed=None):
    """Down-facing area steeper than 45° from vertical, above the bed, in mm² (print orientation).

    `flat_ceilings_mm2` is the part of it that is nearly horizontal: bridges.
    """
    verts, tris = part.tessellate(0.05, 0.2)
    V = np.array([[v.X, v.Y, v.Z] for v in verts]); T = np.array(tris)
    n = np.cross(V[T[:, 1]]-V[T[:, 0]], V[T[:, 2]]-V[T[:, 0]])
    area = np.linalg.norm(n, axis=1)/2
    nz = n[:, 2]/np.maximum(np.linalg.norm(n, axis=1), 1e-12)
    z0 = part.bounding_box().min.Z if z_bed is None else z_bed
    above = V[T].mean(axis=1)[:, 2] > z0 + 0.05
    down = above & (nz < -math.sqrt(0.5))
    return {'steeper_than_45_mm2': float(area[down].sum()), 'flat_ceilings_mm2': float(area[down & (nz < -0.98)].sum())}


def fits_bed(part, bed):
    """True if the part fits `bed` = (x, y, z) mm in its current orientation, turned freely on the bed."""
    s = part.bounding_box().size
    return all(a <= b for a, b in zip(sorted([s.X, s.Y]) + [s.Z], sorted(bed[:2]) + [bed[2]]))


def revolution_envelope(shape, axis, center, slab=1.0):
    """Stacked cylinders about `axis` through `center` that contain `shape` at every angle.

    For a part on a rotary joint: intersect these with the fixed parts and every angle is
    checked at once. Each slab's radius is the farthest sampled point on any of its edges,
    so arcs count (bounding-box corners would overstate a disc by √2). Returns a list of
    (solid, (a0, a1, radius)).
    """
    i = 'xyz'.index(axis)
    b = shape.bounding_box()
    lo, hi = list(b.min)[i], list(b.max)[i]
    slabs, a = [], lo
    while a < hi - 1e-6:
        a1 = min(a+slab, hi)
        ext = [[v-1 for v in b.min], [v+1 for v in b.max]]
        ext[0][i], ext[1][i] = a, a1
        piece = shape.intersect(box(ext[0][0], ext[1][0], ext[0][1], ext[1][1], ext[0][2], ext[1][2]))
        edges = piece.edges() if hasattr(piece, 'edges') else [e for p in piece for e in p.edges()]
        if edges and volume(piece) > 0:
            r = 0.0
            for e in edges:
                for k in range(9):
                    p = list(e.position_at(k/8))
                    r = max(r, math.hypot(*[p[j]-center[j] for j in range(3) if j != i]))
            if slabs and abs(slabs[-1][2]-r) < 0.05 and abs(slabs[-1][1]-a) < 1e-6:
                slabs[-1] = (slabs[-1][0], a1, max(r, slabs[-1][2]))
            else:
                slabs.append((a, a1, r))
        a = a1
    out = []
    for a, a1, r in slabs:
        c = list(center); c[i] = (a+a1)/2
        out.append((cylinder(r, a1-a, axis, tuple(c)), (a, a1, r)))
    return out


def sweep_angles(lo, hi, step):
    """Sample a joint from lo to hi inclusive. Contact between samples is possible when
    step × (largest moving radius) exceeds the clearance you are checking for: say so."""
    n = max(1, math.ceil((hi - lo)/step))
    return [lo + (hi - lo)*k/n for k in range(n + 1)]
