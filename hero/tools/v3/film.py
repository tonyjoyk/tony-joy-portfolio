"""The full hero loop, first draft: every figure traced from reference footage, every prop and
world line drawn in code, joined by draw-on / draw-off and morphing lines.

Story: jog -> Juhu leaps in -> dive -> swim with the ball -> ball into the basket -> ball drops,
bounces, becomes a wheel -> the cycle grows from it -> ride into the sunset -> beach draws in ->
throw, Juhu bounces -> Juhu leaps out after the frisbee -> back to the jog.

Usage: .venv/bin/python film.py out/film [--only 0-60] [--size 600]
Frames are 24 fps; figures change on twos, the world on every frame.
"""
import argparse, os, json
import numpy as np
from pencil import Track, Canvas, figure_strokes, circle, trim, ease, lerp, noise, resample

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--only", default=None); ap.add_argument("--size", type=int, default=600)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
S = a.size; K = S / 600.0                    # timeline is authored on a 600 px canvas
GY = 470                                     # ground line
TORSO = 62                                   # Tony's shoulder-to-hip length on the canvas
TOTAL = 276

T = {n: Track(f"work/{n}") for n in ["jog", "dive", "swim", "cycle2", "dogbeach", "dogrun", "throw"]}
T["dogbeach"].has_pose = T["dogrun"].has_pose = False

def torso_len(tr, f0, f1):
    sh = (tr.lm[f0:f1, 11, :2] + tr.lm[f0:f1, 12, :2]) / 2; hp = (tr.lm[f0:f1, 23, :2] + tr.lm[f0:f1, 24, :2]) / 2
    return float(np.median(np.linalg.norm(sh - hp, axis=1)))

def body_len(tr, f0, f1):
    """dogs: nose-to-tail length from the mask's bounding box, median over a window"""
    ls = []
    for i in range(f0, f1):
        ys, xs = np.nonzero(tr.mask[i] > 128)
        if len(xs): ls.append(max(xs.max() - xs.min(), ys.max() - ys.min()) / tr.ms)
    return float(np.median(ls))

def window(f, t0, t1): return (f - t0) / max(1, (t1 - t0))

# ---------------- figure layers ----------------
class Fig:
    """a traced figure on screen between frames t0..t1.
    src(f) -> fractional source frame; pos(f) -> canvas anchor; ref(fi) -> source anchor.
    Draws on over `on` frames and off over `off` frames."""
    def __init__(self, tr, t0, t1, src, pos, ref, scale, flip=False, on=6, off=6, hair=True, weight=3.0, nmax=10, size=lambda f: 1.0):
        self.__dict__.update(locals()); del self.__dict__["self"]
    def strokes(self, f, drawing):
        fq = 2 * drawing                                  # on twos
        fi = self.src(max(self.t0, fq)); ref = np.asarray(self.ref(fi)); p = np.asarray(self.pos(fq)); s = self.scale * self.size(fq)
        fx = -1 if self.flip else 1
        def place(pts):
            q = (np.asarray(pts) - ref) * s; q[:, 0] *= fx
            return (q + p) * K
        return figure_strokes(self.tr, fi, place, drawing, hair=self.hair, nmax=self.nmax, scale_hint=s * K)
    def progress(self, f):
        a_ = ease(window(f, self.t0, self.t0 + self.on)) if self.on else 1.0
        b_ = ease(window(f, self.t1 - self.off, self.t1)) if self.off else 0.0
        return a_, b_

def jog_src(f):                      # the approved gate loop: source 193..330 over 40 frames
    return 193 + 137 * ((f % 40) / 40)
J = T["jog"]; js = TORSO / torso_len(J, 193, 330)
jog_ref = lambda fi: (J.at(J.cen, fi)[0], float(np.median(J.bot[193:330])))

D = T["dive"]; ds = TORSO / torso_len(D, 10, 60)
SW = T["swim"]; ss = TORSO / torso_len(SW, 0, 30)
C = T["cycle2"]; cs = TORSO / torso_len(C, 0, 125)
DB = T["dogbeach"]; dbs = 150 / body_len(DB, 0, 40)
DR = T["dogrun"]; drs = 150 / body_len(DR, *json.load(open("work/dogrun/window.json"))["len"])
TH = T["throw"]
_f0 = json.load(open("work/throw/window.json"))["throw"][0]
_top = np.nonzero((TH.mask[_f0] > 128).any(1))[0].min() / TH.ms
ths = 330 / (TH.bot[_f0] - _top)          # close medium shot: head to the bottom edge fills ~330 px
DRW = json.load(open("work/dogrun/window.json")); THW = json.load(open("work/throw/window.json"))

# ride-off path: from the wheel spot into the sun along an S-curve
SUN = np.array([392.0, 246.0])
def ride_t(f): return ease(window(f, 182, 220))
def ride_pos(f):
    t = ride_t(f); p0 = np.array([300.0, GY]); p1 = SUN + [0, 6]
    x = lerp(p0[0], p1[0], t) + 70 * np.sin(np.pi * 1.6 * t) * (1 - t); y = lerp(p0[1], p1[1], t ** 0.8)
    return np.array([x, y])
def ride_size(f): t = ride_t(f); return lerp(1.0, 0.05, t ** 0.7)

HIP0 = np.array([502.0, 361.0])      # cycle2 source frame 50: hip landmark, and bike points relative to it
BIKE = {"rear": (-57, 207), "front": (208, 187), "bb": (43, 209), "seat": (3, 59), "bar": (178, 24), "head": (158, 69)}
WR = 95                              # wheel radius in source px
cyc_src = lambda f: 50 + ((f - 150) * 1.05) % 70        # a steady pedalling loop from the clip
cyc_hip = lambda fi: C.at((C.lm[:, 23, :2] + C.lm[:, 24, :2]) / 2, fi)
# the cycle sits with its rear wheel exactly where the ball comes to rest
BALL_REST = np.array([255.0, GY - WR * cs])
def cyc_pos(f):
    base = BALL_REST - np.array(BIKE["rear"]) * cs          # canvas position of the hip
    if f < 182: return base
    d = ride_pos(f) - ride_pos(181); return BALL_REST + (base - BALL_REST) * ride_size(f) + d - (BALL_REST - BALL_REST)
fig_cycle = Fig(C, 150, 226, cyc_src, cyc_pos, cyc_hip, cs, on=12, off=4, weight=2.8, size=lambda f: ride_size(f) if f >= 182 else 1.0)

FIGS = [
    # 1 jog (loops; also draws back on at the end of the loop)
    Fig(J, -1, 40, jog_src, lambda f: (300, GY), jog_ref, js, on=0, off=6),
    Fig(J, TOTAL - 8, TOTAL + 1, jog_src, lambda f: (300, GY), jog_ref, js, on=8, off=0),
    # 2 Juhu runs in from the left and leaps over Tony's back, out to the right
    Fig(DR, -1, 46, lambda f: DRW["run"][0] + (f + 10) * DRW["speed"], lambda f: (lerp(-80, 700, ease(window(f, -6, 46))), GY - 150 * np.sin(np.pi * np.clip(window(f, 8, 34), 0, 1))),
        lambda fi: (DR.at(DR.cen, fi)[0], DR.at(DR.bot, fi)), drs * 0.85, flip=DRW["flip"], on=0, off=0, hair=False, weight=2.6, nmax=9),
    # 3 the dive: pushed forward, long arc into the water
    Fig(D, 34, 70, lambda f: lerp(12, 99, window(f, 34, 70)), lambda f: (300, GY), lambda fi: (D.cen[12][0], D.bot[12]), ds, flip=True, on=6, off=6),
    # 4 swim down with the ball
    Fig(SW, 66, 118, lambda f: lerp(0, 32, window(f, 66, 118)), lambda f: lerp([180, 300], [330, 250], ease(window(f, 66, 118))),
        lambda fi: SW.at(SW.cen, fi), ss, flip=True, on=8, off=10),
    # 7-8 the cycle grows from the wheel, rides into the sunset
    fig_cycle,
    # 10-11 throw on the beach, Juhu bounces, then leaps out after the frisbee
    Fig(TH, 226, 270, lambda f: lerp(THW["throw"][0], THW["throw"][1], window(f, 226, 262)), lambda f: (190, 615), lambda fi: (TH.cen[THW["throw"][0]][0], TH.bot[THW["throw"][0]]), ths, flip=THW["flip"], on=8, off=8, hair=False),
    Fig(DB, 226, 256, lambda f: lerp(84, 136, window(f, 226, 256)), lambda f: (400, GY + 8), lambda fi: (DB.at(DB.cen, fi)[0], float(np.median(DB.bot[0:40]))), dbs * 0.85, on=8, off=0, hair=False, weight=2.6, nmax=9),
    Fig(DR, 256, 276, lambda f: DRW["leap"][0] + (f - 256) * DRW["speed"], lambda f: (lerp(400, 720, ease(window(f, 256, 276))), GY + 8 - 70 * np.sin(np.pi * window(f, 256, 276))),
        lambda fi: (DR.at(DR.cen, fi)[0], DR.at(DR.bot, fi)), drs * 0.85, flip=DRW["flip"], on=0, off=0, hair=False, weight=2.6, nmax=9),
]

# ---------------- props and world, drawn in code ----------------
def swim_hand(f):
    """the swimmer's leading hand on the canvas (wrist nearest the swim direction)"""
    fig = FIGS[4]; fi = fig.src(f); P = SW.lm_at(fi); ref = SW.at(SW.cen, fi)
    w = P[[15, 16]]; k = int(np.argmin(w[:, 0]))      # source swims left; after the flip the lead hand is the left-most
    q = (w[k] - ref) * fig.scale; q[0] *= -1
    return np.asarray(fig.pos(f)) + q

BASKET = np.array([470.0, GY])       # on the pool floor
def ball_state(f):
    """(centre, radius, squash) of the ball through the swim, drop and bounce"""
    r0 = 14.0
    if f < 66: return None
    if f < 100: return swim_hand(f) + [6, 0], r0, 1.0
    if f < 112:                                         # pushed into the basket
        t = ease(window(f, 100, 112)); h = swim_hand(100) + [6, 0]; rim = BASKET + [0, -78]
        return lerp(h, rim, t) + [0, -40 * np.sin(np.pi * t)], r0, 1.0
    if f < 126:                                         # falls through and lands on the new ground
        t = window(f, 112, 126); y = lerp(GY - 78, GY - r0, t * t)
        return np.array([BASKET[0], y]), r0, 1.0 + 0.25 * t
    # bounces twice, rolling left to the wheel spot and growing into a wheel
    t = window(f, 126, 150); r = lerp(r0, WR * cs, ease(t))
    x = lerp(BASKET[0], BALL_REST[0], ease(t))
    hop = np.abs(np.sin(np.pi * 2 * t)) * 70 * (1 - t) ** 1.3
    sq = 1.0 - 0.28 * np.exp(-((t * 2) % 1) * 8) * (1 - t) if t < 1 else 1.0
    if f >= 150: return BALL_REST, WR * cs, 1.0
    return np.array([x, GY - r * sq - hop]), r, sq

def world(f):
    """world lines as (pts, seed, weight, alpha); the ground keeps one identity and changes shape"""
    L = []; xs = np.linspace(60, 540, 48)
    flat = np.stack([xs, np.full_like(xs, GY + 4)], -1)
    wave = np.stack([xs, GY + 4 + 5 * np.sin(xs * 0.05 + f * 0.25)], -1)
    # ground -> water surface (dive) -> rises out of view as we go under -> pool floor -> ground again
    if f < 40: g = flat
    elif f < 60: g = lerp(flat, wave, ease(window(f, 40, 56)))
    elif f < 84: g = wave + [0, -lerp(0, GY + 40, ease(window(f, 60, 84)))]
    else: g = None
    if g is not None: L.append((g, 11, 2.0, 0.6))
    if 72 <= f < 126:                                   # pool floor and basket
        a0, a1 = ease(window(f, 72, 86)), 1.0
        b0 = ease(window(f, 112, 126))
        L.append((trim(flat, b0, a0), 12, 2.0, 0.6))
        rim = circle(BASKET + [0, -78], 24, 30, squash=0.28)
        for k, pts in enumerate([rim, [BASKET + [-24, -78], BASKET + [-18, 0]], [BASKET + [24, -78], BASKET + [18, 0]],
                                 [BASKET + [-20, -55], BASKET + [20, -55]], [BASKET + [-19, -28], BASKET + [19, -28]],
                                 [BASKET + [-12, -80], BASKET + [-8, 0]], [BASKET + [10, -80], BASKET + [8, 0]]]):
            L.append((trim(pts, b0, a0), 40 + k, 1.8 if k < 3 else 1.2, 0.8 if k < 3 else 0.45))
        for k in range(3):                              # a few bubbles
            t = ((f * 0.03 + k * 0.33) % 1)
            c = swim_hand(min(f, 99)) + [-30 - 15 * k, -t * 120] if f < 112 else None
            if c is not None and f < 100: L.append((circle(c, 3 + k, 12), 60 + k, 1.0, 0.5))
    if 112 <= f < 182 + 0:                                  # the dry ground draws in under the falling ball
        L.append((trim(flat, 0, ease(window(f, 112, 124))), 13, 2.0, 0.6))
    if 182 <= f < 236:                                  # ground becomes a road to the horizon, then the beach
        hz = np.stack([xs, np.full_like(xs, SUN[1] + 6)], -1)
        L.append((trim(flat, ease(window(f, 182, 194)), 1), 13, 2.0, 0.6))          # the near ground draws off
        L.append((trim(hz, 0, ease(window(f, 180, 196))), 14, 1.8, 0.6))             # the horizon draws on
        # road edges: an S-curve narrowing into the sun
        u = np.linspace(0, 1, 30)
        for side, sd in ((-1, 21), (1, 22)):
            x = lerp(300, SUN[0], u) + 70 * np.sin(np.pi * 1.6 * u) * (1 - u) + side * lerp(70, 2, u)
            y = lerp(GY + 40, SUN[1] + 6, u ** 0.8)
            road = np.stack([x, y], -1)
            L.append((trim(road, 0, ease(window(f, 178, 196)) * (1 - ease(window(f, 216, 228)))), sd, 1.6, 0.55))
    if f >= 176 and f < 270:                            # the sun: draws on, sinks half under the horizon
        r = 34; a_ = ease(window(f, 176, 192)); off = ease(window(f, 262, 270))
        c = SUN + [0, lerp(0, 18, ease(window(f, 200, 236)))]
        sun = circle(c, r, 50, a0=np.pi * 0.95, sweep=-np.pi * 0.9 * 2 * a_ / 1.8)
        sun = sun[sun[:, 1] < SUN[1] + 6] if f > 200 else sun
        if len(sun) > 3: L.append((trim(sun, off, 1), 30, 2.2, 0.85))
    if 200 <= f < 272:                                  # horizon, sea and shore
        hz = np.stack([xs, np.full_like(xs, SUN[1] + 6)], -1)
        if f >= 236: L.append((trim(hz, ease(window(f, 262, 272)), 1), 14, 1.8, 0.6))
        for k in range(4):
            y = SUN[1] + 26 + k * 26; x0 = 90 + 60 * noise(k * 3.1, 0) + 25 * k; w = 70 + 30 * noise(k, 1)
            wv = np.stack([np.linspace(x0, x0 + w, 12), y + 3 * np.sin(np.linspace(0, 3, 12) + f * 0.2 + k)], -1)
            L.append((trim(wv, ease(window(f, 262, 272)), ease(window(f, 206 + 4 * k, 218 + 4 * k))), 50 + k, 1.4, 0.5))
            wv2 = wv + [250 + 30 * noise(k, 5), 8 * noise(k, 7)]
            L.append((trim(wv2, ease(window(f, 262, 272)), ease(window(f, 208 + 4 * k, 220 + 4 * k))), 55 + k, 1.4, 0.5))
        shore = np.stack([xs, GY - 40 + 12 * np.sin(xs * 0.012 + 1.2) + 3 * np.sin(xs * 0.06 + f * 0.12)], -1)
        L.append((trim(shore, ease(window(f, 262, 272)), ease(window(f, 214, 230))), 15, 1.8, 0.6))
    if f >= 226:                                        # sand line, which becomes the jog ground again
        L.append((trim(flat, 0, ease(window(f, 222, 234))), 16, 2.0, 0.6))
    return L

def props(f, cv, drawing):
    st = ball_state(f)
    if st is not None and f < 150:                      # the ball: a circle with a seam
        c, r, sq = st
        cv.pencil(circle(c, r, 36, a0=noise(f * 0.1, 3), sweep=2 * np.pi * 0.96, squash=sq) * K, 70, drawing, 2.6, 0.95, second=False)
        cv.ribbon(circle(c, r * 0.7, 16, a0=0.6 + f * 0.15, sweep=1.6, squash=sq) * K, 71, drawing, 1.2, 0.6)
    if 150 <= f < 226:                                  # the bike, from the rider's hip, in code
        fq = 2 * drawing; fi = cyc_src(fq); s = cs * (ride_size(fq) if fq >= 182 else 1.0)
        hip_c = np.asarray(cyc_pos(fq)); P = C.lm_at(fi); hip_s = cyc_hip(fi)
        pt = lambda key: hip_c + np.array(BIKE[key]) * s
        a_ = ease(window(f, 150, 162)); b_ = ease(window(f, 220, 226))
        def draw(pts, seed, w, al, second=False):
            pts = trim(np.asarray(pts, float), b_, a_)
            if len(pts) > 1: cv.pencil(pts * K, seed, drawing, max(0.8, w * min(1, s / cs * 1.4)), al, second=second)
        spin = f * 0.35
        for key, sd in (("rear", 80), ("front", 81)):
            if key == "rear" and f < 162: continue          # the ball already is the rear wheel
            draw(circle(pt(key), WR * s, 44, a0=spin * 0.1), sd, 2.8, 0.95, True)
            for k in range(3):
                ang = spin + k * np.pi / 3
                draw([pt(key) + WR * s * 0.92 * np.array([np.cos(ang), np.sin(ang)]), pt(key) - WR * s * 0.92 * np.array([np.cos(ang), np.sin(ang)])], sd + 10 + k, 0.9, 0.35)
        draw([pt("rear"), pt("bb"), pt("seat"), pt("rear")], 90, 2.0, 0.85)
        draw([pt("seat") + [0, 8 * s], pt("head")], 91, 2.0, 0.85)
        draw([pt("bb"), pt("head"), pt("front")], 92, 2.0, 0.85)
        draw([pt("head"), pt("bar"), pt("bar") + np.array([18, 14]) * s], 93, 1.8, 0.8)
        for an in (27, 28):                             # crank arms to the feet
            foot = hip_c + (P[an] - hip_s) * s
            draw([pt("bb"), lerp(pt("bb"), foot + np.array([4, 22]) * s, 0.8)], 94 + an, 1.6, 0.7)
    if f >= 150 and f < 162:                            # the ball still reads as the rear wheel while the bike draws on
        cv.pencil(circle(BALL_REST, WR * cs, 44) * K, 80, drawing, 2.8, 0.95)
    if 226 <= f < 276:                                  # the frisbee: in hand, then thrown out to the right
        fig = FIGS[6]; rel = THW["release"]
        if f < rel:
            fi = fig.src(f); P = TH.lm_at(fi); ref = fig.ref(fi)
            w = P[[15, 16]]; k = int(np.argmax(w[:, 0] * (-1 if THW["flip"] else 1)))
            q = (w[k] - ref) * fig.scale; q[0] *= (-1 if THW["flip"] else 1)
            c = np.asarray(fig.pos(f)) + q
        else:
            t = window(f, rel, 270); c = lerp([300, GY - 150], [650, GY - 250], t) + [0, -40 * np.sin(np.pi * t)]
        a_ = ease(window(f, 226, 234))
        cv.pencil(trim(circle(c, 16, 28, squash=0.35, rot=-0.2), 0, a_) * K, 95, drawing, 2.2, 0.9, second=False)

# ---------------- render ----------------
rng = range(TOTAL) if not a.only else range(*map(int, a.only.split("-")))
counts = []
cache = {}
for f in rng:
    drawing = f // 2; cv = Canvas(S)
    for pts, seed, w, al in world(f):
        pts = np.asarray(pts)
        if len(pts) > 1: cv.ribbon(pts * K, seed, drawing, w * K, al)
    props(f, cv, drawing)
    n = 0
    for k, fig in enumerate(FIGS):
        if not (fig.t0 <= f < fig.t1): continue
        key = (k, drawing)
        if key not in cache: cache[key] = fig.strokes(f, drawing)
        a_, b_ = fig.progress(f)
        for kind, pts, seed in cache[key]:
            if kind == "hair":
                if a_ > 0.6 and b_ < 0.4: cv.mass(pts, drawing)
                continue
            pts = trim(pts, b_, a_)
            if len(pts) > 1: cv.pencil(pts, 100 + seed + 50 * k, drawing, fig.weight * K * (0.55 + 0.45 * min(1, fig.size(f) * 1.5)), 0.95); n += 1
    counts.append(n)
    cv.image().save(os.path.join(a.out, f"f{f:03d}.png"))
json.dump({"frames": TOTAL, "fps": 24}, open(os.path.join(a.out, "meta.json"), "w"))
print("rendered", len(counts), "frames; strokes per frame max", max(counts))
