"""Checks on the exported STL itself, the mesh the slicer will see.

`workshop.cad.checks.overhangs` looks at the CAD solid's faces. These look at the triangles:

- :func:`mesh_check`: watertight, no degenerate faces, positive volume, the expected number of
  separate parts, every part's bottom on the bed (z = 0).
- :func:`layers`: slices the mesh into print layers and checks that each layer stands on the one
  below. Reports new islands with nothing under them (asserted absent), area outside the 45° cone of
  the previous layer, and the worst sideways step between layers.

Footprint geometry only: it does not simulate beads, cooling, infill or adhesion.

    from workshop.cad.printability import layers, mesh_check
    mesh_check('exports/holder.stl')
    summary, rows = layers('exports/holder.stl')
    assert summary['max_area_outside_45deg_layer_envelope_mm2'] < 0.01
"""
from pathlib import Path

import numpy as np
from shapely import get_parts
from shapely.geometry import LineString, Point
from shapely.ops import polygonize, unary_union
from stl import mesh

LAYER = 0.20
LINE_WIDTH = 0.42   # nominal 0.4 mm nozzle line, for the overlap estimate


def load(path):
    """STL triangles as an (n, 3, 3) float array, mm."""
    return mesh.Mesh.from_file(str(path)).vectors.astype(float)


def footprint(triangles, height):
    """Material cross-section at z = `height`: a shapely (Multi)Polygon, kept by even-odd parity.

    Pass ``t[:, :, [1, 2, 0]]`` to cut across X instead (a section in the YZ plane).
    """
    segments = []
    active = triangles[(triangles[:, :, 2].min(axis=1) < height) & (triangles[:, :, 2].max(axis=1) > height)]
    for tri in active:
        pts = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a, b = tri[i], tri[j]
            if (a[2] - height) * (b[2] - height) < 0:
                # Interpolate shared edges in the same direction: reversed endpoints can round
                # differently at a half step and leave gaps in finely tessellated lettering.
                if a[2] > b[2]:
                    a, b = b, a
                f = (height - a[2]) / (b[2] - a[2])
                pts.append(np.round((a + f * (b - a))[:2], 6))
        if len(pts) == 2 and np.linalg.norm(pts[1] - pts[0]) > 1e-7:
            segments.append(pts)
    if not segments:
        return unary_union([])
    seg = np.array(segments)
    material = []
    for polygon in polygonize(unary_union([LineString(s) for s in segments])):
        p = polygon.representative_point()
        a, b = seg[:, 0], seg[:, 1]
        crosses = (a[:, 1] > p.y) != (b[:, 1] > p.y)
        a, b = a[crosses], b[crosses]
        x = a[:, 0] + (p.y - a[:, 1]) * (b[:, 0] - a[:, 0]) / (b[:, 1] - a[:, 1])
        if np.count_nonzero(x > p.x) % 2:
            material.append(polygon)
    result = unary_union(material)
    assert not result.is_empty, f'unclosed section at {height} mm'
    assert result.is_valid
    return result


def layers(path, layer_height=LAYER, first_layer_height=None):
    """(summary, per-layer rows) for the STL at `path`, in its print orientation.

    Asserts that no layer starts an island with nothing beneath it.
    """
    t = load(path)
    first = first_layer_height or layer_height
    heights = np.r_[first / 2, np.arange(first + layer_height / 2, t[:, :, 2].max(), layer_height)]
    rows, detached, previous = [], [], None
    for n, h in enumerate(heights):
        current = footprint(t, float(h))
        islands = [p for p in get_parts(current) if p.area > 1e-5]
        row = {'layer': n + 1, 'mid_height_mm': round(float(h), 3), 'area_mm2': round(current.area, 3),
               'islands': len(islands)}
        if previous is not None:
            outside = current.difference(previous.buffer(float(h - previous_h), quad_segs=16))
            row['area_outside_45deg_envelope_mm2'] = round(outside.area, 6)
            offset = 0.
            for p in islands:
                offset = max([offset, *(previous.distance(Point(c)) for c in p.exterior.coords)])
                if not p.intersects(previous):
                    detached.append({'layer': n + 1, 'height_mm': round(float(h), 3), 'area_mm2': round(p.area, 6)})
            row['maximum_vertex_offset_from_previous_layer_mm'] = round(offset, 6)
        rows.append(row)
        previous, previous_h = current, h
    normals = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    normals /= np.linalg.norm(normals, axis=1)[:, None]
    below = (normals[:, 2] < -1e-7) & (t[:, :, 2].mean(axis=1) > .05)
    angles = np.rad2deg(np.arcsin(np.clip(-normals[below, 2], 0, 1)))
    worst = max(rows[1:], key=lambda r: r['maximum_vertex_offset_from_previous_layer_mm']) if len(rows) > 1 \
        else {'maximum_vertex_offset_from_previous_layer_mm': 0., 'layer': 1}
    step = worst['maximum_vertex_offset_from_previous_layer_mm']
    summary = {
        'stl': Path(path).name, 'layer_height_mm': layer_height, 'first_layer_height_mm': first,
        'reference_line_width_mm': LINE_WIDTH, 'layers_sampled': len(rows),
        'first_layer_material_area_mm2': rows[0]['area_mm2'], 'first_layer_connected_regions': rows[0]['islands'],
        'new_islands_without_previous_layer_overlap': detached,
        'max_downward_surface_angle_from_vertical_deg': round(float(angles.max()), 3) if len(angles) else 0,
        'worst_layer_boundary_offset_mm': step, 'worst_offset_layer': worst['layer'],
        'approx_line_overlap_at_worst_offset_percent': round(100 * (1 - step / LINE_WIDTH), 1),
        'max_area_outside_45deg_layer_envelope_mm2': max(r.get('area_outside_45deg_envelope_mm2', 0) for r in rows),
        'limits': 'Footprint geometry only; does not simulate beads, cooling, infill or adhesion.',
    }
    assert not detached, summary
    return summary, rows


def mesh_check(path, expected_parts=1):
    """Mesh facts for the STL at `path`; asserts it is printable as `expected_parts` parts on the bed."""
    t = load(path)
    vertices, ids = np.unique(np.round(t.reshape(-1, 3), 5), axis=0, return_inverse=True)
    faces = ids.reshape(-1, 3)
    edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    _, counts = np.unique(np.sort(edges, axis=1), axis=0, return_counts=True)
    parents = np.arange(len(vertices))

    def root(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i
    for a, b in edges:
        parents[root(a)] = root(b)
    roots = np.array([root(i) for i in range(len(vertices))])
    groups = np.unique(roots)
    bottoms = [float(vertices[roots == g, 2].min()) for g in groups]
    area2 = np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1)
    volume = float(np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6)
    row = {'triangles': len(t), 'watertight': bool(np.all(counts == 2)),
           'nonmanifold_edges': int(np.count_nonzero(counts != 2)),
           'degenerate_faces': int(np.count_nonzero(area2 < 1e-9)),
           'connected_components': len(groups), 'signed_volume_mm3': round(volume, 3),
           'component_bottoms_mm': bottoms}
    assert row['watertight'] and row['degenerate_faces'] == 0 and volume > 0, (path, row)
    assert len(groups) == expected_parts and np.allclose(bottoms, 0, atol=1e-5), (path, row)
    return row
