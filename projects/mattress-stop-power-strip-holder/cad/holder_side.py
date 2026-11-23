"""The strip holder: the Elworks strip on its side, sockets facing the room, cord on the left as seen
from the room (+X; the remote cup is at -X, on the right).

    uv run python cad/holder_side.py

Two flat pieces joined by a bowtie key (holder.py), because the strip is longer than the bed:
  * the saddle (over the stop): back plate, the lip resting on the bar (holder_mag.top_lip),
    magnet bosses facing the insert inside the cloth cover, a joint block at each end (cup, tail);
  * the tail (past the stop's end): back plate stiffened by a flange behind its top edge and a 45 deg
    gusset behind its bottom edge, so it does not flex when a plug is pushed in.

How the strip is held: two adapters (adapter.py) lock into the plus-shaped hanging holes in the
strip's base, with their T-feet pointing DOWN (turn the bayonet 45 deg the other way, so the foot
ends up across the strip). Each foot drops into a short vertical T-slot (rail.py profile) on the
back plate, closed at the bottom. So the strip is lowered in from above and lifts straight out:
  * weight: the feet sit on the slots' closed bottoms;
  * pulling a plug: bayonet -> adapter -> slot lips;
  * pushing a plug, and chargers hanging off the sockets: the slots' front faces and two pads
    near the strip's ends carry its back; a 20 mm foot in its slot cannot rock;
  * along the strip: the feet cannot move sideways in their slots, so no end walls are needed.
Nothing covers the strip's sides or socket face.

Print both pieces upside down (their top edge on the bed): slots, pads, joint blocks, roof and
flange all start on the bed; the key pockets' and slots' closed ends are short bridges, and the
magnet pockets and bosses are teardrops. No supports.
"""
import pathlib
import sys
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"
import holder as H
import holder_mag as M
import rail as R
import strip as S

SLACK_Z = 0.6                              # the strip sits where the old channel put it
SLOT_FLOOR = 2.5                           # closed bottom of each T-slot
PAD_W = 5.0                                # back pads near the strip's ends
TAIL_FLANGE = H.JB_T                       # tail's top flange reaches back as far as the joint blocks
TAIL_GUSSET = 8.0                          # tail's bottom 45 deg gusset, each leg

W = H.WALL
zb = H.tray_bot
y_strip = H.y_plate + R.RAIL_T             # the strip's back (= the slots' front face)
z_mid = zb + W + (S.WIDTH + SLACK_Z) / 2   # strip centreline = adapter centres
z_strip_bot = z_mid - S.WIDTH / 2
strip_x0 = -H.SADDLE_L / 2 + W + 0.5       # far end, clear of the cup's joint
x_seam = H.SADDLE_L / 2                    # saddle | tail
foot_bot = z_mid - R.FOOT_L / 2            # where each foot comes to rest


def slot(xc):
    """A vertical T-slot centred on x = xc, open at the top, closed just below the resting foot."""
    z0 = foot_bot - SLOT_FLOOR
    body = Box(R.RAIL_H, R.RAIL_T, H.z_top - z0, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(
        Location((xc, H.y_plate, z0)))
    under = Box(R.UNDER_W, R.UNDER_D, H.z_top - foot_bot + 1, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(
        Location((xc, H.y_plate + R.RAIL_BASE, foot_bot)))
    mouth = Box(R.SLOT_W, R.LIP_T + 0.02, H.z_top - foot_bot + 1, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(
        Location((xc, H.y_plate + R.RAIL_BASE + R.UNDER_D - 0.01, foot_bot)))
    return body - under - mouth


def pad(xc):
    """Full-height rib whose front face carries the strip's back."""
    return Box(PAD_W, R.RAIL_T, H.z_top - z_strip_bot - 3, align=(Align.CENTER, Align.MIN, Align.MAX)).moved(
        Location((xc, H.y_plate, H.z_top)))


def plate(x0, x1):
    return Box(x1 - x0, W, H.z_top - zb, align=(Align.MIN, Align.MIN, Align.MIN)).moved(Location((x0, H.y_back, zb)))


def plus_world():
    return [strip_x0 + S.LENGTH / 2 + px for px in S.plus_xs()]


def saddle():
    h = H.SADDLE_L / 2
    xs = plus_world()
    p = plate(-h, h) + M.top_lip(-h, h) + H.joint_block(-h, +1) + H.joint_block(h, -1)
    p += slot(xs[0]) + pad(strip_x0 + PAD_W / 2 + 2)
    bosses, pockets = M.holder_magnets()
    for b in bosses:
        p += b
    for c in pockets:
        p -= c
    return p


def tail_end():
    return strip_x0 + S.LENGTH + 2.0


def tail():
    x0, x1 = x_seam, tail_end()
    xs = plus_world()
    p = plate(x0, x1) + H.joint_block(x0, +1)
    p += Box(x1 - x0 - H.JB_L, TAIL_FLANGE, W, align=(Align.MIN, Align.MAX, Align.MAX)).moved(
        Location((x0 + H.JB_L, H.y_back, H.z_top)))
    with BuildSketch(Plane.YZ) as g:   # local (x, y) = world (Y, Z)
        Polygon((H.y_back, zb), (H.y_back - TAIL_GUSSET, zb), (H.y_back, zb + TAIL_GUSSET), align=None)
    p += extrude(g.sketch, amount=x1 - x0 - H.JB_L).moved(Location((x0 + H.JB_L, 0, 0)))
    p += slot(xs[1]) + pad(strip_x0 + S.LENGTH - PAD_W / 2 - 2)
    return p


def place_strip(local):
    """Move something from the strip's local frame (strip.py) to where the strip sits."""
    return local.rotate(Axis.X, -90).moved(Location((strip_x0 + S.LENGTH / 2, y_strip, z_mid)))


def build():
    import adapter as A
    h = H.SADDLE_L / 2
    return dict(
        saddle=saddle(), tail=tail(), cup=H.cup(-h),
        keys=[H.key().moved(Location((xk, H.jb_yc, zb + W))) for xk in (-h, h)],
        strip=place_strip(S.strip()),
        # turn=90: foot across the strip, i.e. vertical once placed
        adapters=[place_strip(A.adapter(turn=90).moved(Location((px, 0, 0)))) for px in S.plus_xs()],
    )


if __name__ == "__main__":
    b = build()
    s, t, c = b["saddle"], b["tail"], b["cup"]
    holder = s + t
    stop = H.stop_keepout(13.0)
    ads = Compound(b["adapters"])
    up = lambda d: Location((0, 0, d))
    # lowering the strip in: the adapters and strip swept down from well above
    drop = sum((ads.moved(up(dz)) & holder).volume + (b["strip"].moved(up(dz)) & (holder + c)).volume
               for dz in range(1, 40, 1))
    checks = {
        "saddle/stop 13 mm": s & stop, "tail/stop 13 mm": t & stop, "saddle/cup": s & c, "saddle/tail": s & t,
        "insert/saddle": M.insert() & s, "keys/parts": Compound(b["keys"]) & (holder + c),
        "strip/holder": b["strip"] & (holder + c), "adapters/holder": ads & holder, "adapters/strip": ads & b["strip"],
    }
    for k, v in checks.items():
        print(f"{k:26s} overlap {v.volume:8.2f} mm^3 (want 0)")
    print(f"{'lowering in, 1..39 mm up':26s} overlap {drop:8.2f} mm^3 (want 0)")
    tests = {"pull 0.5 mm to the room": Location((0, 0.5, 0)), "push 0.5 mm to the stop": Location((0, -0.5, 0)),
             "slide 1 mm to the cord end": Location((1, 0, 0)), "slide 1 mm to the cup": Location((-1, 0, 0)),
             "drop 0.5 mm": Location((0, 0, -0.5)), "tip 2 deg face-down": None}
    tip_axis = Axis((0, y_strip, z_mid), (1, 0, 0))   # along the strip, at its back
    for k, loc in tests.items():
        if "tip" in k:
            st, ad = b["strip"].rotate(tip_axis, 2), ads.rotate(tip_axis, 2)
        else:
            st, ad = b["strip"].moved(loc), ads.moved(loc)
        hit = (st & (holder + c)).volume + (ad & holder).volume
        print(f"{k:26s} blocked by {hit:7.2f} mm^3 of contact (want > 0)")
    out = EXPORTS
    for name, p in {"side_saddle": s, "side_tail": t}.items():
        bb = p.bounding_box()
        print(f"{name:12s} {bb.size.X:6.1f} x {bb.size.Y:5.1f} x {bb.size.Z:5.1f} mm  {p.volume/1000:5.1f} cm^3")
        export(name, p, out)
    export_step(Compound([s, t, c, M.insert()] + b["keys"] + b["adapters"]), str(out / "side_assembly.step"))
    export_step(b["strip"], str(out / "side_strip_placed.step"))
