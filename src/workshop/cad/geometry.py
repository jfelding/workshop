"""Small solid primitives that read like the drawing: boxes by extents, slots, nut pockets.

Axes are named 'x', 'y' or 'z'. Nothing here holds a dimension; callers pass measured values.
"""
import math

from build123d import Axis, Box, Cylinder, Face, RegularPolygon, Wire, extrude


def cylinder(radius, height, axis, center):
    p = Cylinder(radius, height)
    if axis == 'x': p = p.rotate(Axis.Y, 90)
    if axis == 'y': p = p.rotate(Axis.X, 90)
    return p.translate(center)


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from its extents; easier to read than size + centre."""
    return Box(x1-x0, y1-y0, z1-z0).translate(((x0+x1)/2, (y0+y1)/2, (z0+z1)/2))


def prism_yz(points, x0, x1):
    """Extrude a (y, z) outline along X between x0 and x1."""
    wire = Wire.make_polygon([(x0, y, z) for y, z in points], close=True)
    return extrude(Face(wire), amount=x1-x0, dir=(1, 0, 0))


def slot(diameter, travel, depth, axis, along, center):
    """Elongated hole: two cylinders joined by a box. `axis` is the hole's axis, `along` the slot direction."""
    c = list(center); ends = []
    i = 'xyz'.index(along)
    for s in (-1, 1):
        p = c.copy(); p[i] += s*travel/2
        ends.append(cylinder(diameter/2, depth, axis, p))
    size = [diameter]*3
    size['xyz'.index(axis)] = depth
    size[i] = travel
    return ends[0] + ends[1] + Box(*size).translate(center)


def hex_pocket(across_flats, depth, axis, center):
    """Hex nut pocket, `depth` each side of `center`, with a flat at +Z (a short bridge when printed Z up)."""
    hexagon = RegularPolygon(across_flats/2, 6, major_radius=False, rotation=0)
    solid = extrude(hexagon, amount=depth, both=True)
    if axis == 'x': solid = solid.rotate(Axis.Y, 90)
    if axis == 'y': solid = solid.rotate(Axis.X, 90)
    return solid.translate(center)


def teardrop(diameter, depth, axis, center, up='z'):
    """Horizontal hole that prints without support: a circle with a 45° roof toward `up`.

    Use for any hole whose axis lies in the bed plane and whose roof would otherwise be a
    flat-ish arc bridge. The point reaches diameter/√2 above the centre.
    """
    r = diameter/2
    i, j = 'xyz'.index(axis), 'xyz'.index(up)
    if i == j:
        raise ValueError('teardrop: `up` must be across the hole axis')
    # A square of side r turned 45° about the hole axis, its lower corner at the centre:
    # its side corners lie on the circle at ±45° and its upper sides are the tangents there.
    size = [r]*3
    size[i] = depth
    roof = Box(*size).rotate(Axis((0, 0, 0), tuple(1 if k == i else 0 for k in range(3))), 45)
    lift = [0.0, 0.0, 0.0]
    lift[j] = r/math.sqrt(2)
    return cylinder(r, depth, axis, center) + roof.translate(tuple(c + d for c, d in zip(center, lift)))


def radial_box(width, r0, r1, x0, x1, angle_deg, origin):
    """Box in the YZ plane from radius r0 to r1 along `angle_deg` (0° = +Y, 90° = +Z)."""
    b = box(x0, x1, r0, r1, -width/2, width/2)
    return b.rotate(Axis.X, angle_deg).translate((0, origin[1], origin[2]))


def arc_slot(diameter, depth, centre, radius, angle_mid, half_sweep, steps=9):
    """A slot that follows an arc about a vertical axis through `centre` (x, y, z).

    A clamped rotary joint wants its bolts to run along the arc they actually travel on;
    a straight slot binds at the ends. Built as overlapping cylinders, which is exact
    enough at these radii and prints the same.
    """
    cx, cy, cz = centre
    out = None
    for i in range(steps):
        a = math.radians(angle_mid - half_sweep + 2*half_sweep*i/(steps - 1))
        c = cylinder(diameter/2, depth, 'z', (cx + radius*math.sin(a), cy - radius*math.cos(a), cz))
        out = c if out is None else out + c
    return out
