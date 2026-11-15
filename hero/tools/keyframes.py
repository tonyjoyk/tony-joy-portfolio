"""Key frames for the hero animation (storyboard v2, Tony's 2026-11-15 notes).

Writes:
  hero/keyframes/kNN-<label>.svg   one clean SVG per key frame: every stroke is a named <path>, same set and order in every frame
  hero/keyframes/timeline.json     frame numbers, labels, cuts, and every stroke as N points (what the p5 engine reads)

Rules the engine relies on:
  - 600 x 600 canvas, 24 fps, loop of 240 frames (10 s).
  - Every key frame has exactly the same stroke names; each stroke has POINTS points.
  - A stroke whose points all sit on one spot is hidden. Blending from or to it draws the line on or off.
  - "cut" lists stroke groups that jump to this key frame without blending (used when a character
    leaves on one side and comes back on the other).
Run from the repo root:  python3 hero/tools/keyframes.py
"""
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rig
from rig import tony, tony_strokes, gear_strokes, juhu, juhu_strokes

OUT = Path(__file__).resolve().parents[1] / "keyframes"
POINTS = 32
FPS, LOOP = 24, 240
G = 430                                                          # ground line on land

PROP_STROKES = ["p-ball", "p-frisbee", "p-floor", "p-basket-rim", "p-basket-bowl", "p-basket-base", "p-net-1", "p-net-2",
                "p-wheel-b", "p-frame", "p-frame-b", "p-fork", "p-seat"]
WORLD_STROKES = ["w-ground", "w-line2", "w-horizon", "w-sun", "w-wave-1", "w-wave-2", "w-splash", "w-bubble-1", "w-bubble-2", "w-bubble-3"]
ALL = WORLD_STROKES + PROP_STROKES + rig.JUHU_STROKES + rig.TONY_STROKES + rig.GEAR_STROKES
GROUPS = {"w-": "world", "p-": "props", "j-": "juhu", "t-": "tony", "g-": "gear"}
def group_of(name): return GROUPS[name[:2]]

# ---------------------------------------------------------------- geometry helpers
def resample(pts, n=POINTS):
    if len(pts) == 1 or max(math.dist(pts[0], p) for p in pts) < 1e-6:
        return [tuple(pts[0])] * n
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; total = sum(seg); out = []; i = 0; acc = 0.0
    for k in range(n):
        target = total * k / (n - 1)
        while i < len(seg) - 1 and acc + seg[i] < target: acc += seg[i]; i += 1
        t = 0 if seg[i] == 0 else (target - acc) / seg[i]
        out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t))
    return out

def dot(x, y): return [(x, y)]
def line(x0, y0, x1, y1): return [(x0, y0), (x1, y1)]
def wave(x0, x1, y, amp=0, k=3.0, ph=0.0, n=40):
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(ph + k * math.tau * i / n)) for i in range(n + 1)]
def ellipse(cx, cy, rx, ry=None, rot=0, a0=-80, a1=265):
    ry = ry if ry is not None else rx; c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot)); out = []
    for i in range(41):
        a = math.radians(a0 + (a1 - a0) * i / 40); x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out
def arc(cx, cy, r, a0, a1): return ellipse(cx, cy, r, r, 0, a0, a1)
def curve(pts, n=40):                                            # smooth curve through points (Catmull-Rom)
    P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n // (len(pts) - 1)):
            t = k / (n // (len(pts) - 1)); t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(pts[-1]); return out

def center(strokes):
    xs = [x for v in strokes.values() for x, _ in v]; ys = [y for v in strokes.values() for _, y in v]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
def hidden(names, at): return {n: dot(*at) for n in names}

# ---------------------------------------------------------------- character helpers
def grounded_tony(x, ground=G, **kw):
    """Pose Tony, then drop him so his lowest foot point touches the ground."""
    pose = tony(x, 0, **kw); st = tony_strokes(pose)
    low = max(y for n in ("t-foot-n", "t-foot-f") for _, y in st[n])
    return tony(x, ground - low, **kw)

def grounded_juhu(x, ground=G, **kw):
    pose = juhu(x, 0, **kw); st = juhu_strokes(pose)
    low = max(y for n in st if n.endswith("paw") for _, y in st[n])
    return juhu(x, ground - low, **kw)

JOG = [dict(torso=12, head=-8, an=-40, en=100, af=35, ef=95, ln=30, kn=10, lf=-32, kf=55),   # contact A
       dict(torso=12, head=-8, an=-5, en=95, af=5, ef=95, ln=2, kn=20, lf=-10, kf=95),       # passing
       dict(torso=12, head=-8, an=35, en=95, af=-40, ef=100, ln=-32, kn=55, lf=30, kf=10),   # contact B
       dict(torso=12, head=-8, an=5, en=95, af=-5, ef=95, ln=-10, kn=95, lf=2, kf=20)]       # passing B
JUHU_LEAP = dict(spine=10, neck=18, head=12, fa=78, fb=-12, ffa=64, ffb=-24, ba=-72, bk=6, bh=12, bfa=-58, bfk=10, bfh=16, ta=-8, tb=-14, mouth=.3)
JUHU_STAND = dict(spine=2, neck=38, head=22, fa=4, fb=-2, ffa=-6, ffb=0, ba=-8, bk=32, bh=28, bfa=8, bfk=36, bfh=26, ta=45, tb=30)
JUHU_TROT = dict(spine=3, neck=30, head=20, fa=28, fb=-30, ffa=-18, ffb=0, ba=-28, bk=20, bh=30, bfa=22, bfk=50, bfh=20, ta=20, tb=10, mouth=.4)
JUHU_REAR = dict(rot=-42, spine=4, neck=58, head=-4, fa=70, fb=-75, ffa=55, ffb=-70, ba=42, bk=78, bh=60, bfa=34, bfk=70, bfh=55, ta=-25, tb=-35, mouth=.6)
JUHU_CROUCH = dict(spine=-6, neck=28, head=24, fa=30, fb=-20, ffa=18, ffb=-15, ba=15, bk=75, bh=55, bfa=25, bfk=80, bfh=55, ta=0, tb=-20, mouth=.5)

def bike(R, s=1.0, crank=0.0):
    """Cycle with its rear hub at R. Returns (strokes, front hub, contact points for the rider)."""
    sc = lambda dx, dy: (R[0] + dx * s, R[1] + dy * s)
    BB, seat, head, F = sc(44, -6), sc(30, -66), sc(92, -62), sc(104, 0); bars = (head[0] + 6 * s, head[1] - 10 * s)
    st = {"p-wheel-b": ellipse(R[0], R[1], 38 * s), "p-frame": [R, BB, seat, R], "p-frame-b": [seat, head, BB],
          "p-fork": [F, head, bars, (bars[0] + 8 * s, bars[1] + 4 * s)], "p-seat": [(seat[0] - 9 * s, seat[1] - 4 * s), (seat[0] + 9 * s, seat[1] - 4 * s)]}
    c = math.radians(crank); pn = (BB[0] + 14 * s * math.cos(c), BB[1] + 14 * s * math.sin(c)); pf = (BB[0] - 14 * s * math.cos(c), BB[1] - 14 * s * math.sin(c))
    return st, F, dict(seat=seat, bars=bars, pn=pn, pf=pf)

def rider(R, s=1.0, crank=0.0):
    st, F, c = bike(R, s, crank)
    pose = tony(c["seat"][0] - 2 * s, c["seat"][1] - 12 * s, s=s, torso=48, head=-34, hand_n=c["bars"], hand_f=(c["bars"][0] - 3 * s, c["bars"][1] + 1),
                foot_n=c["pn"], foot_f=c["pf"])
    return st, F, pose

# ---------------------------------------------------------------- key frames
def base(world=None, props=None):
    """Start every key frame with all strokes hidden near the middle, then fill in what is visible."""
    k = {n: dot(300, 300) for n in ALL}
    k.update(world or {}); k.update(props or {}); return k

def put_tony(k, pose, gear=False):
    st = tony_strokes(pose); k.update(st)
    if gear: k.update(gear_strokes(pose))
    else: k.update(hidden(rig.GEAR_STROKES, pose[0]["H"]))
def put_juhu(k, pose): k.update(juhu_strokes(pose))
def hide_tony(k, at): k.update(hidden(rig.TONY_STROKES + rig.GEAR_STROKES, at))
def hide_juhu(k, at): k.update(hidden(rig.JUHU_STROKES, at))

LAND = lambda amp=0, ph=0: {"w-ground": wave(40, 560, G, amp, 2.5, ph)}
KF = []
def key(frame, label, k, cut=()):
    KF.append(dict(frame=frame, label=label, strokes=k, cut=list(cut)))

# Act 1 — land: jog, Juhu leaps in from behind
for i, (f, x) in enumerate([(0, 228), (6, 236), (12, 244), (18, 252)]):
    k = base(LAND()); put_tony(k, grounded_tony(x, **JOG[i]))
    jx = [-170, -60, 40, 140][i]; jy = [330, 320, 312, 300][i]
    put_juhu(k, juhu(jx, jy, **JUHU_LEAP))
    k.update(hidden(["p-frisbee"], (700, 200)))
    key(f, ["Jog, contact", "Jog, passing", "Jog, contact (Juhu flies in)", "Jog, passing (Juhu closing in)"][i], k,
        cut=["juhu", "props"] if f == 0 else [])

k = base(LAND()); put_tony(k, grounded_tony(262, torso=34, head=-20, an=-70, en=30, af=-45, ef=40, ln=22, kn=25, lf=-35, kf=30))
put_juhu(k, juhu(176, 380, rot=-40, spine=8, neck=20, head=10, fa=100, fb=-20, ffa=90, ffb=-30, ba=-20, bk=20, bh=30, bfa=-5, bfk=30, bfh=30, ta=-10, tb=-20, mouth=.4))
key(24, "Juhu lands on Tony's back", k)

k = base(LAND(3, .5)); put_tony(k, tony(326, 334, rot=58, torso=8, head=-10, an=165, en=8, af=155, ef=10, ln=-12, kn=12, lf=-26, kf=24))
put_juhu(k, grounded_juhu(150, **JUHU_STAND))
key(32, "Pushed forward into a dive", k)

k = base({"w-ground": wave(40, 560, 420, 6, 3, 1.2)}); put_tony(k, tony(392, 338, rot=108, torso=0, head=-5, an=178, en=0, af=176, ef=2, ln=-4, kn=3, lf=4, kf=3))
hide_juhu(k, (150, 420))
key(42, "Dive arc, ground becomes water", k)

k = base({"w-ground": wave(40, 560, 422, 6, 3, 2.0), "w-splash": arc(436, 424, 22, 200, 340)})
put_tony(k, tony(424, 372, rot=152, torso=0, head=0, an=178, en=0, af=176, ef=2, ln=-3, kn=3, lf=3, kf=3)); hide_juhu(k, (196, 420))
key(50, "Head first into the water", k)

# Act 2 — water: swim down, basket, ball
def water(surface_y=70, floor_y=None, basket_x=380):
    w = {"w-ground": wave(20, 580, surface_y, 5, 3, 0.6)}
    p = {}
    if floor_y is not None:
        p["p-floor"] = line(30, floor_y, 570, floor_y)
        bx, by = basket_x, floor_y
        p["p-basket-base"] = [(bx - 32, by - 1), (bx - 30, by - 8), (bx + 30, by - 8), (bx + 32, by - 1)]
        p["p-basket-bowl"] = curve([(bx - 34, by - 62), (bx - 26, by - 22), (bx, by - 12), (bx + 26, by - 22), (bx + 34, by - 62)])
        p["p-basket-rim"] = ellipse(bx, by - 62, 34, 7, 0, 0, 360)
        p["p-net-1"] = [(bx - 14, by - 58), (bx - 10, by - 18)]; p["p-net-2"] = [(bx + 14, by - 58), (bx + 10, by - 18)]
    return w, p

def bubbles(k, pts):
    for n, (x, y, r) in zip(("w-bubble-1", "w-bubble-2", "w-bubble-3"), pts): k[n] = ellipse(x, y, r, r, 0, 0, 360)

w, p = water(); k = base(w, p); put_tony(k, tony(250, 196, rot=135, torso=0, head=-6, an=176, en=4, af=172, ef=6, ln=10, kn=16, lf=-14, kf=6), gear=True)
bubbles(k, [(198, 150, 4), (206, 128, 3), (192, 108, 2.5)]); key(60, "Under water: snorkel, goggles, fins", k)

w, p = water(floor_y=600); k = base(w, p); put_tony(k, tony(300, 300, rot=140, torso=0, head=-6, an=176, en=4, af=170, ef=8, ln=-14, kn=6, lf=12, kf=18), gear=True)
bubbles(k, [(246, 230, 4), (240, 196, 3), (252, 168, 2.5)]); key(72, "Swim down, kick", k)

w, p = water(floor_y=520); k = base(w, p)
pose = tony(300, 318, rot=148, torso=0, head=-4, an=170, en=10, af=160, ef=16, ln=12, kn=18, lf=-12, kf=6); put_tony(k, pose, gear=True)
hn = pose[0]["htn"]; k["p-ball"] = ellipse(hn[0] + 6, hn[1] + 10, 13)
bubbles(k, [(262, 236, 4), (256, 206, 3), (270, 176, 2.5)]); key(84, "Ball in hand, basket on the pool floor", k)

w, p = water(floor_y=520); k = base(w, p)
put_tony(k, tony(334, 338, rot=166, torso=0, head=0, an=176, en=2, af=168, ef=8, ln=4, kn=10, lf=-8, kf=8), gear=True)
k["p-ball"] = ellipse(380, 446, 13); bubbles(k, [(300, 270, 4), (294, 236, 3), (306, 204, 2.5)]); key(94, "Push the ball into the basket", k)

w, p = water(floor_y=520); k = base(w, p)
put_tony(k, tony(318, 214, rot=-12, torso=0, head=-10, an=170, en=10, af=176, ef=4, ln=8, kn=12, lf=-14, kf=8), gear=True)
k["p-ball"] = ellipse(380, 500, 13); bubbles(k, [(330, 120, 4), (322, 96, 3), (336, 74, 2.5)]); key(102, "Ball drops through, Tony swims up", k)

# Act 3 — road: follow the ball, it bounces and grows into a cycle
w, p = water(surface_y=-160, floor_y=150); k = base(w, p); hide_tony(k, (318, -120)); k["p-ball"] = ellipse(380, 300, 13)
k["w-line2"] = dot(300, 640); key(110, "Follow the ball down", k)

k = base({"w-ground": dot(300, -200)}, {"p-floor": line(30, -60, 570, -60)}); hide_tony(k, (318, -120))
for n in ("p-basket-base", "p-basket-bowl", "p-basket-rim", "p-net-1", "p-net-2"): k[n] = dot(380, -80)
k["w-line2"] = line(40, 470, 560, 470); k["p-ball"] = ellipse(392, 461, 16, 9); key(118, "Ball lands on a road: squash", k)

k = base({"w-ground": dot(300, -200), "w-line2": line(40, 470, 560, 470)}); hide_tony(k, (318, -120)); k["p-ball"] = ellipse(424, 360, 11, 15)
key(126, "Bounce up: stretch", k)

k = base({"w-ground": dot(300, -200), "w-line2": line(40, 470, 560, 470)}); hide_tony(k, (318, -120)); k["p-ball"] = ellipse(452, 458, 22, 12)
key(134, "Second bounce, growing", k)

k = base({"w-ground": dot(300, -200), "w-line2": line(40, 470, 560, 470)}); F = (468, 432); k["p-ball"] = ellipse(F[0], F[1], 38)
hide_tony(k, F); k.update(hidden(["p-wheel-b", "p-frame", "p-frame-b", "p-fork", "p-seat"], F)); key(142, "The ball is a wheel", k)

k = base({"w-ground": dot(300, -200), "w-line2": line(40, 470, 560, 470)}); st, F, pose = rider((364, 432), 1.0, 30)
k.update(st); k["p-ball"] = ellipse(F[0], F[1], 38); put_tony(k, pose); key(152, "The cycle and Tony grow out of the wheel", k)

def road(vp=(430, 250)):
    return {"w-ground": curve([(40, 560), (170, 470), (330, 400), (420, 300), vp]),
            "w-line2": curve([(330, 600), (430, 500), (470, 390), (452, 300), (vp[0] + 4, vp[1])]),
            "w-horizon": line(40, vp[1], 560, vp[1]), "w-sun": arc(vp[0], vp[1], 30, 180, 360)}
k = base(road()); st, F, pose = rider((300, 420), .62, 160); k.update(st); k["p-ball"] = ellipse(F[0], F[1], 38 * .62); put_tony(k, pose)
key(166, "Ride along the curving road", k)

k = base(road()); st, F, pose = rider((418, 266), .17, 290); k.update(st); k["p-ball"] = ellipse(F[0], F[1], 38 * .17); put_tony(k, pose)
key(180, "Smaller and slower, into the sun", k)

# Act 4 — beach: the sun sets, the beach draws in, the throw
def beach(sun_y=250, sun_r=30):
    return {"w-horizon": line(40, 250, 560, 250), "w-sun": arc(430, sun_y, sun_r, 180, 360),
            "w-wave-1": wave(110, 500, 290, 2, 4, 0), "w-wave-2": wave(70, 540, 335, 2.5, 3.5, 1),
            "w-ground": curve([(20, 432), (160, 412), (330, 424), (580, 404)]), "w-line2": curve([(40, 512), (300, 500), (560, 516)])}
k = base(beach(sun_y=256)); sp = (430, 244)
k.update(hidden(["p-ball", "p-wheel-b", "p-frame", "p-frame-b", "p-fork", "p-seat"], sp)); hide_tony(k, sp); hide_juhu(k, sp)
key(188, "Cycle becomes a dot in the sun; beach draws in", k)

k = base(beach(sun_y=262)); put_tony(k, grounded_tony(-70, ground=424, torso=4, head=-4, an=-20, en=20, af=20, ef=20, ln=18, kn=6, lf=-18, kf=16))
put_juhu(k, grounded_juhu(-150, ground=420, **JUHU_TROT)); k["p-frisbee"] = dot(-40, 360)
key(194, "Beach, empty for a moment", k, cut=["tony", "gear", "juhu", "props"])

k = base(beach(sun_y=266)); pose = grounded_tony(150, ground=420, torso=4, head=-4, an=24, en=18, af=-20, ef=20, ln=-18, kn=16, lf=18, kf=6); put_tony(k, pose)
put_juhu(k, grounded_juhu(290, ground=420, **JUHU_TROT)); hn = pose[0]["htn"]; k["p-frisbee"] = ellipse(hn[0] + 6, hn[1] + 2, 16, 5, -60, 0, 360)
key(204, "Tony and Juhu walk in", k)

k = base(beach(sun_y=268)); pose = grounded_tony(170, ground=420, torso=-4, head=-12, an=150, en=12, af=-10, ef=20, ln=6, kn=4, lf=-8, kf=4); put_tony(k, pose)
put_juhu(k, grounded_juhu(322, ground=420, flip=True, **JUHU_REAR)); hn = pose[0]["htn"]; k["p-frisbee"] = ellipse(hn[0] + 2, hn[1] - 6, 16, 5, -10, 0, 360)
key(212, "Frisbee up, Juhu bounces", k)

k = base(beach(sun_y=270)); pose = grounded_tony(166, ground=420, torso=-10, head=-6, an=-70, en=20, af=40, ef=40, ln=14, kn=8, lf=-14, kf=12); put_tony(k, pose)
put_juhu(k, grounded_juhu(330, ground=420, flip=True, **JUHU_CROUCH)); hn = pose[0]["htn"]; k["p-frisbee"] = ellipse(hn[0] - 4, hn[1], 16, 5, 20, 0, 360)
key(220, "Wind-up; Juhu crouches, tail going", k)

k = base(beach(sun_y=272)); pose = grounded_tony(178, ground=420, torso=16, head=-8, an=110, en=0, af=-40, ef=30, ln=28, kn=10, lf=-26, kf=30); put_tony(k, pose)
put_juhu(k, grounded_juhu(330, ground=420, **JUHU_CROUCH)); k["p-frisbee"] = ellipse(300, 262, 16, 5, -8, 0, 360)
key(228, "Throw; Juhu turns to chase", k)

k = base({"w-horizon": line(300, 250, 300, 250), "w-sun": dot(430, 280), "w-wave-1": dot(300, 290), "w-wave-2": dot(300, 335),
          "w-ground": wave(40, 560, G - 4, 2, 2, 0), "w-line2": dot(300, 512)})
put_tony(k, grounded_tony(206, **JOG[2])); put_juhu(k, juhu(486, 330, **JUHU_LEAP)); k["p-frisbee"] = ellipse(536, 176, 16, 5, -6, 0, 360)
key(234, "Juhu leaps after it; the beach turns back into ground", k)

k = base(LAND()); put_tony(k, grounded_tony(220, **JOG[3])); put_juhu(k, juhu(700, 300, **JUHU_LEAP)); k["p-frisbee"] = ellipse(690, 150, 16, 5, -6, 0, 360)
key(239, "Juhu leaves the frame (loop: she flies back in from the left)", k)

# ---------------------------------------------------------------- write
def fmt(pts): return [[round(x, 1), round(y, 1)] for x, y in pts]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("k*.svg"): f.unlink()
    data = {"fps": FPS, "loop": LOOP, "size": [600, 600], "points": POINTS, "strokes": ALL,
            "groups": {n: group_of(n) for n in ALL}, "keyframes": []}
    for i, kf in enumerate(KF):
        missing = set(ALL) - set(kf["strokes"]); extra = set(kf["strokes"]) - set(ALL)
        assert not missing and not extra, (kf["label"], missing, extra)
        pts = {n: resample(kf["strokes"][n]) for n in ALL}
        slug = "".join(c if c.isalnum() else "-" for c in kf["label"].lower()).strip("-")[:40].strip("-")
        name = f"k{i:02d}-{slug}.svg"
        paths = []
        for n in ALL:
            vis = max(math.dist(pts[n][0], q) for q in pts[n]) >= 1.5
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts[n])
            paths.append(f'  <path id="{n}" data-group="{group_of(n)}" data-visible="{int(vis)}" d="{d}"/>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600" '
               f'data-frame="{kf["frame"]}" data-label="{kf["label"]}" data-cut="{",".join(kf["cut"])}">\n'
               f'<g fill="none" stroke="#A4553A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">\n' + "\n".join(paths) + "\n</g>\n</svg>\n")
        (OUT / name).write_text(svg)
        data["keyframes"].append({"frame": kf["frame"], "label": kf["label"], "file": name, "cut": kf["cut"], "strokes": {n: fmt(pts[n]) for n in ALL}})
    (OUT / "timeline.json").write_text(json.dumps(data, separators=(",", ":")))
    print(len(KF), "key frames,", len(ALL), "strokes each, ->", OUT)

if __name__ == "__main__":
    main()
