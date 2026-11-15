"""Hero loop, draft 2 (10 s, 240 frames at 24 fps).

Changes from draft 1 (film.py):
- 10 s instead of 11.5 s; every beat is shorter.
- Figures hide the world lines and props behind them.
- Juhu is shepherd-type in every beat: a German Shepherd trot (Pexels 4166357) and a shepherd's
  jump-up from the beach clip (10665038).
- The swim is a freediver with fins (37236357); goggles and snorkel are drawn in code.
- The ball stays in the swimmer's hand, stays small through the bounces, then grows into the wheel.
- A side-on frisbee throw with the whole body (10398424).

Usage: .venv/bin/python film2.py out/film2 [--only 0-60] [--size 600]
"""
import argparse, os, json
import numpy as np
from pencil import Track, Canvas, figure_strokes, circle, trim, ease, lerp, noise

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--only", default=None); ap.add_argument("--size", type=int, default=600)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
S = a.size; K = S / 600.0
GY = 470; TORSO = 62; TOTAL = 240
W = json.load(open("windows2.json"))           # source windows picked from the contact sheets

T = {n: Track(f"work/{n}") for n in ["jog", "dive", "swim2", "cycle2", "dogbeach", "gsd", "throw2"]}
for n in ("dogbeach", "gsd"): T[n].has_pose = False

def torso_len(tr, f0, f1):
    sh = (tr.lm[f0:f1, 11, :2] + tr.lm[f0:f1, 12, :2]) / 2; hp = (tr.lm[f0:f1, 23, :2] + tr.lm[f0:f1, 24, :2]) / 2
    return float(np.median(np.linalg.norm(sh - hp, axis=1)))
def body_len(tr, f0, f1):
    ls = []
    for i in range(f0, f1):
        ys, xs = np.nonzero(tr.mask[i] > 128)
        if len(xs): ls.append((xs.max() - xs.min()) / tr.ms)
    return float(np.median(ls))
def window(f, t0, t1): return (f - t0) / max(1, (t1 - t0))
def span(f, t0, t1, s0, s1): return lerp(s0, s1, np.clip(window(f, t0, t1), 0, 1))

class Fig:
    def __init__(self, tr, t0, t1, src, pos, ref, scale, flip=False, on=6, off=6, hair=True, weight=3.0, nmax=10, size=lambda f: 1.0):
        self.__dict__.update(locals()); del self.__dict__["self"]
    def placer(self, f):
        fi = self.src(f); ref = np.asarray(self.ref(fi), float); p = np.asarray(self.pos(f), float); s = self.scale * self.size(f)
        fx = -1 if self.flip else 1
        def place(pts):
            q = (np.asarray(pts, float) - ref) * s
            if q.ndim == 1: q[0] *= fx
            else: q[:, 0] *= fx
            return (q + p) * K
        return fi, place
    def strokes(self, drawing):
        fq = max(self.t0, 2 * drawing); fi, place = self.placer(fq)
        return figure_strokes(self.tr, fi, place, drawing, hair=self.hair, nmax=self.nmax, scale_hint=self.scale * self.size(fq) * K)
    def progress(self, f):
        a_ = ease(window(f, self.t0, self.t0 + self.on)) if self.on else 1.0
        b_ = ease(window(f, self.t1 - self.off, self.t1)) if self.off else 0.0
        return a_, b_

# ---- scales and anchors ----
J = T["jog"]; js = TORSO / torso_len(J, 193, 330)
def jog_src(f): return 193 + 137 * ((f % 40) / 40)
jog_ref = lambda fi: (J.at(J.cen, fi)[0], float(np.median(J.bot[193:330])))
D = T["dive"]; ds = TORSO / torso_len(D, 10, 60)
SW = T["swim2"]; sws = TORSO / torso_len(SW, *W["swim"]["len"])
C = T["cycle2"]; cs = TORSO / torso_len(C, 0, 125)
DB = T["dogbeach"]; G = T["gsd"]
DOG = 128                                            # Juhu nose-to-tail on the canvas
gs = DOG / body_len(G, *W["gsd"]["len"]); dbs = DOG / body_len(DB, 0, 40)
TH = T["throw2"]; ths = TORSO / torso_len(TH, *W["throw"]["len"])
dbg = float(np.median(DB.bot[0:40]))

TONY_X = 300
# ---- beats (output frames) ----
B = dict(jog=(0, 34), dive=(30, 58), swim=(56, 100), drop=(96, 118), bounce=(118, 136), grow=(134, 142),
         cyc_on=(138, 150), ride=(158, 190), beach=(186, 202), throw=(198, 230), leap=(222, 240))

# Juhu: trots in from the left, jumps up at Tony's back
juhu_in = Fig(G, -1, 22, lambda f: W["gsd"]["trot"][0] + (f + 2) * W["gsd"]["speed"],
              lambda f: (lerp(-90, TONY_X - 120, ease(window(f, -2, 22))), GY), lambda fi: (G.at(G.cen, fi)[0], G.at(G.bot, fi)),
              gs, flip=W["gsd"]["flip"], on=0, off=0, hair=False, weight=2.6, nmax=9)
juhu_up = Fig(DB, 20, 40, lambda f: span(f, 20, 40, 88, 118), lambda f: (TONY_X - 95 + 30 * ease(window(f, 20, 40)), GY),
              lambda fi: (DB.at(DB.cen, fi)[0], dbg), dbs, flip=True, on=2, off=8, hair=False, weight=2.6, nmax=9)
jog = Fig(J, -1, 36, jog_src, lambda f: (TONY_X, GY), jog_ref, js, on=0, off=6)
jog_back = Fig(J, TOTAL - 8, TOTAL + 1, jog_src, lambda f: (TONY_X, GY), jog_ref, js, on=8, off=0)
dive = Fig(D, B["dive"][0], B["dive"][1] + 6, lambda f: span(f, *B["dive"], 12, 99), lambda f: (TONY_X - 10, GY),
           lambda fi: (D.cen[12][0], D.bot[12]), ds, flip=True, on=4, off=6)
sw0, sw1 = W["swim"]["src"]
swim = Fig(SW, B["swim"][0], B["swim"][1], lambda f: span(f, *B["swim"], sw0, sw1),
           lambda f: lerp([230, 250], [330, 300], ease(window(f, *B["swim"]))), lambda fi: SW.at(SW.cen, fi), sws,
           flip=W["swim"]["flip"], on=8, off=8)

# cycle: bike drawn in code from the rider's hip (cycle2 source frame 50)
BIKE = {"rear": (-57, 207), "front": (208, 187), "bb": (43, 209), "seat": (3, 59), "bar": (178, 24), "head": (158, 69)}
WR = 95
SUN = np.array([392.0, 246.0])
BALL_REST = np.array([255.0, GY - WR * cs])
def ride_t(f): return ease(window(f, *B["ride"]))
def ride_pos(f):
    t = ride_t(f); p0 = np.array([BALL_REST[0] + 50, GY]); p1 = SUN + [0, 6]
    return np.array([lerp(p0[0], p1[0], t) + 70 * np.sin(np.pi * 1.6 * t) * (1 - t), lerp(p0[1], p1[1], t ** 0.8)])
def ride_size(f): return float(lerp(1.0, 0.05, ride_t(f) ** 0.7))
cyc_src = lambda f: 50 + ((f - B["cyc_on"][0]) * 1.05) % 70
cyc_hip = lambda fi: C.at((C.lm[:, 23, :2] + C.lm[:, 24, :2]) / 2, fi)
HIP_C = BALL_REST - np.array(BIKE["rear"]) * cs
def cyc_pos(f):
    if f < B["ride"][0]: return HIP_C
    s = ride_size(f); anchor = ride_pos(f)                          # the bike's ground point follows the road
    ground_rel = np.array([BALL_REST[0] + 50, GY]) - HIP_C
    return anchor - ground_rel * s
cycle = Fig(C, B["cyc_on"][0], B["ride"][1] + 4, cyc_src, cyc_pos, cyc_hip, cs, on=12, off=4, weight=2.8, size=lambda f: ride_size(f))

# beach: the throw, Juhu bounces and leaps out after the frisbee
t0_, t1_ = W["throw"]["src"]
_top = np.nonzero((TH.mask[t0_] > 128).any(1))[0].min() / TH.ms
ths_close = (612 - 370) / (TH.bot[t0_] - _top)      # the clip is cut at the knees: a close shot, cut by the bottom of the picture
thrower = Fig(TH, B["throw"][0], B["throw"][1] + 6, lambda f: span(f, B["throw"][0], B["throw"][1], t0_, t1_), lambda f: (210, 612),
              lambda fi: (TH.cen[t0_][0], TH.bot[t0_]), ths_close, flip=W["throw"]["flip"], on=8, off=8)
thrower.hair_alpha = 0.45
juhu_bounce = Fig(DB, B["throw"][0], B["leap"][0] + 2, lambda f: span(f, B["throw"][0], B["leap"][0], 0, 46),
                  lambda f: (430, GY - 20 - 26 * abs(np.sin(np.pi * 3 * window(f, B["throw"][0] + 6, B["leap"][0])))), lambda fi: (DB.at(DB.cen, fi)[0], dbg), dbs * 0.75, flip=False, on=8, off=0, hair=False, weight=2.6, nmax=9)
juhu_out = Fig(DB, B["leap"][0], B["leap"][1], lambda f: span(f, *B["leap"], 112, 130),
               lambda f: (lerp(430, 700, ease(window(f, *B["leap"]))), GY - 20 - 50 * np.sin(np.pi * window(f, *B["leap"]))),
               lambda fi: (DB.at(DB.cen, fi)[0], dbg), dbs * 0.75, flip=False, on=0, off=0, hair=False, weight=2.6, nmax=9)

FIGS = [jog, jog_back, juhu_in, juhu_up, dive, swim, cycle, thrower, juhu_bounce, juhu_out]

# ---------------- props ----------------
def lm_canvas(fig, f, idx):
    fi, place = fig.placer(f); P = fig.tr.lm_at(fi)
    return np.array([place(P[i]) / K for i in idx])

def swim_hand(f):
    hands = lm_canvas(swim, f, [15, 16]); head = lm_canvas(swim, f, [0])[0]
    k = int(np.argmin(np.linalg.norm(hands - head, axis=1) * 0 + (-hands[:, 0])))   # the hand furthest forward (right)
    return hands[k]

BASKET = np.array([465.0, GY])
R0 = 13.0
def ball_state(f):
    if f < B["swim"][0] + 6: return None
    if f < B["drop"][0]: return swim_hand(f) + [8, 2], R0, 1.0
    rim = BASKET + [0, -78]
    if f < B["drop"][0] + 8:
        t = ease(window(f, B["drop"][0], B["drop"][0] + 8)); h = swim_hand(B["drop"][0]) + [8, 2]
        return lerp(h, rim, t) + [0, -36 * np.sin(np.pi * t)], R0, 1.0
    if f < B["bounce"][0]:
        t = window(f, B["drop"][0] + 8, B["bounce"][0]); return np.array([BASKET[0], lerp(rim[1], GY - R0, t * t)]), R0, 1.0
    if f < B["grow"][0]:                          # two bounces, rolling left, still a ball
        t = window(f, *B["bounce"]); x = lerp(BASKET[0], BALL_REST[0], ease(t))
        ph = (t * 2) % 1; hop = np.sin(np.pi * ph) * 60 * (1 - 0.45 * (t >= 0.5))
        sq = 1 - 0.3 * max(0, 1 - ph * 6) - 0.3 * max(0, (ph - 0.85) * 6.6)
        return np.array([x, GY - R0 * sq - hop]), R0, sq
    t = ease(window(f, *B["grow"])); r = lerp(R0, WR * cs, t)       # lands, then grows into the wheel
    return np.array([BALL_REST[0], GY - r]), r, 1.0

def world(f):
    L = []; xs = np.linspace(60, 540, 48)
    flat = np.stack([xs, np.full_like(xs, GY + 4)], -1)
    wave = np.stack([xs, GY + 4 + 5 * np.sin(xs * 0.05 + f * 0.25)], -1)
    d0, d1 = B["dive"]
    if f < d0 + 6: g = flat
    elif f < d1: g = lerp(flat, wave, ease(window(f, d0 + 6, d1 - 6)))
    elif f < d1 + 18: g = wave + [0, -lerp(0, GY + 40, ease(window(f, d1, d1 + 18)))]
    else: g = None
    if g is not None: L.append((g, 11, 2.0, 0.6))
    s0 = B["swim"][0]; dr0 = B["drop"][0]
    if s0 + 6 <= f < B["bounce"][0]:                     # pool floor and basket, then they draw off
        a0 = ease(window(f, s0 + 6, s0 + 18)); b0 = ease(window(f, dr0 + 10, B["bounce"][0]))
        L.append((trim(flat, b0, a0), 12, 2.0, 0.6))
        R = BASKET + [0, -78]
        for k, pts in enumerate([circle(R, 24, 30, squash=0.28), [R + [-24, 0], BASKET + [-18, 0]], [R + [24, 0], BASKET + [18, 0]],
                                 [BASKET + [-21, -52], BASKET + [21, -52]], [BASKET + [-19, -26], BASKET + [19, -26]],
                                 [R + [-10, -2], BASKET + [-7, 0]], [R + [10, -2], BASKET + [7, 0]]]):
            L.append((trim(pts, b0, a0), 40 + k, 1.8 if k < 3 else 1.2, 0.8 if k < 3 else 0.45))
        if f < dr0:
            for k in range(3):                           # bubbles from the snorkel
                t = (f * 0.04 + k * 0.33) % 1; head = lm_canvas(swim, f, [0])[0]
                L.append((circle(head + [-10 - 8 * k, -30 - t * 110], 2.5 + k, 12), 60 + k, 1.0, 0.5))
    if dr0 + 8 <= f < B["ride"][0] + 12:                 # the dry ground draws in under the falling ball, then off
        L.append((trim(flat, ease(window(f, B["ride"][0], B["ride"][0] + 12)), ease(window(f, dr0 + 8, dr0 + 18))), 13, 2.0, 0.6))
    r0, r1 = B["ride"]; hz = np.stack([xs, np.full_like(xs, SUN[1] + 6)], -1)
    if r0 - 4 <= f < TOTAL:                              # horizon: draws on with the ride, stays for the beach, off at the end
        L.append((trim(hz, ease(window(f, TOTAL - 14, TOTAL - 4)), ease(window(f, r0 - 4, r0 + 12))), 14, 1.8, 0.6))
    if r0 - 6 <= f < B["beach"][1]:                      # the road, an S-curve into the sun
        u = np.linspace(0, 1, 30)
        for side, sd in ((-1, 21), (1, 22)):
            x = lerp(BALL_REST[0] + 50, SUN[0], u) + 70 * np.sin(np.pi * 1.6 * u) * (1 - u) + side * lerp(70, 2, u)
            road = np.stack([x, lerp(GY + 40, SUN[1] + 6, u ** 0.8)], -1)
            L.append((trim(road, ease(window(f, B["beach"][0], B["beach"][1])), ease(window(f, r0 - 6, r0 + 8))), sd, 1.6, 0.55))
    if r0 - 8 <= f < TOTAL - 6:                          # the sun, sinking half under the horizon
        a_ = ease(window(f, r0 - 8, r0 + 6)); off = ease(window(f, TOTAL - 16, TOTAL - 6))
        c = SUN + [0, lerp(0, 16, ease(window(f, r1 - 6, B["beach"][1])))]
        sun = circle(c, 34, 50, a0=np.pi * 0.95, sweep=-2 * np.pi * 0.98 * a_)
        if f > r1 - 6: sun = sun[sun[:, 1] < SUN[1] + 6]
        if len(sun) > 3: L.append((trim(sun, off, 1), 30, 2.2, 0.85))
    b0_, b1_ = B["beach"]
    if b0_ <= f < TOTAL:                                 # sea, shore and sand
        off = ease(window(f, TOTAL - 14, TOTAL - 4))
        for k in range(4):
            y = SUN[1] + 24 + k * 24; x0 = 80 + 60 * noise(k * 3.1, 0) + 25 * k; w = 70 + 30 * noise(k, 1)
            wv = np.stack([np.linspace(x0, x0 + w, 12), y + 3 * np.sin(np.linspace(0, 3, 12) + f * 0.2 + k)], -1)
            L.append((trim(wv, off, ease(window(f, b0_ + 2 * k, b0_ + 8 + 2 * k))), 50 + k, 1.4, 0.5))
            L.append((trim(wv + [250 + 30 * noise(k, 5), 8 * noise(k, 7)], off, ease(window(f, b0_ + 3 + 2 * k, b0_ + 9 + 2 * k))), 55 + k, 1.4, 0.5))
        shore = np.stack([xs, GY - 50 + 12 * np.sin(xs * 0.012 + 1.2) + 3 * np.sin(xs * 0.06 + f * 0.12)], -1)
        L.append((trim(shore, off, ease(window(f, b0_ + 4, b1_))), 15, 1.8, 0.6))
        L.append((trim(flat, 0, ease(window(f, b0_ + 6, b1_ + 4))), 16, 2.0, 0.6))   # sand line, which stays as the jog ground
    return L

def back_props(f, cv, drawing):
    c0 = B["cyc_on"][0]
    if c0 <= f < B["ride"][1] + 4:                      # the bike, in code, from the rider's hip
        fq = 2 * drawing; fi, place = cycle.placer(max(c0, fq)); s = cs * ride_size(fq)
        hip_c = np.asarray(cyc_pos(fq)); P = C.lm_at(fi); hip_s = cyc_hip(fi)
        pt = lambda key: hip_c + np.array(BIKE[key]) * s
        a_ = ease(window(f, c0, c0 + 12)); b_ = ease(window(f, B["ride"][1], B["ride"][1] + 4))
        def draw(pts, seed, w, al, second=False):
            pts = trim(np.asarray(pts, float), b_, a_)
            if len(pts) > 1: cv.pencil(pts * K, seed, drawing, max(0.8, w * min(1, s / cs * 1.4)), al, second=second)
        spin = f * 0.35
        for key, sd in (("rear", 80), ("front", 81)):
            if key == "rear" and f < c0 + 10:
                cv.pencil(circle(pt("rear"), WR * s, 44) * K, 80, drawing, 2.8, 0.95); continue
            draw(circle(pt(key), WR * s, 44, a0=spin * 0.1), sd, 2.8, 0.95, True)
            for k in range(3):
                ang = spin + k * np.pi / 3; v = WR * s * 0.92 * np.array([np.cos(ang), np.sin(ang)])
                draw([pt(key) + v, pt(key) - v], sd + 10 + k, 0.9, 0.35)
        draw([pt("rear"), pt("bb"), pt("seat"), pt("rear")], 90, 2.0, 0.85)
        draw([pt("seat") + [0, 8 * s], pt("head")], 91, 2.0, 0.85)
        draw([pt("bb"), pt("head"), pt("front")], 92, 2.0, 0.85)
        draw([pt("head"), pt("bar"), pt("bar") + np.array([18, 14]) * s], 93, 1.8, 0.8)
        for an in (27, 28):
            foot = hip_c + (P[an] - hip_s) * s
            draw([pt("bb"), lerp(pt("bb"), foot + np.array([4, 22]) * s, 0.8)], 94 + an, 1.6, 0.7)

def front_props(f, cv, drawing):
    st = ball_state(f)
    if st is not None and f < B["grow"][1] + 8:
        c, r, sq = st
        cv.erase(circle(c, r, 24, squash=sq) * K, 1.0, 0)
        cv.pencil(circle(c, r, 36, a0=noise(f * 0.1, 3), sweep=2 * np.pi * 0.96, squash=sq) * K, 70, drawing, 2.6, 0.95, second=False)
        if r < 30: cv.ribbon(circle(c, r * 0.7, 16, a0=0.6 + f * 0.15, sweep=1.6, squash=sq) * K, 71, drawing, 1.2, 0.6)
    s0, s1 = B["swim"]
    if s0 + 4 <= f < s1 - 4:                            # goggles and snorkel on the swimmer
        fq = max(s0, 2 * drawing); eye, nose, ear, mouth = lm_canvas(swim, fq, [2, 0, 7, 9])
        fwd = nose - ear; fwd /= np.linalg.norm(fwd) + 1e-6; up = np.array([fwd[1], -fwd[0]])
        if up[1] > 0: up = -up
        a_ = ease(window(f, s0 + 4, s0 + 12)); b_ = ease(window(f, s1 - 10, s1 - 4))
        g = (eye + nose) / 2 + fwd * 2
        cv.pencil(trim(circle(g, 7, 20, squash=0.6, rot=np.arctan2(fwd[1], fwd[0])), b_, a_) * K, 74, drawing, 2.0, 0.9, second=False)
        cv.ribbon(trim(np.array([g - fwd * 6, ear + up * 2]), b_, a_) * K, 75, drawing, 1.4, 0.7)
        tube = np.array([mouth + fwd * 3, mouth + fwd * 6 + up * 4, ear + fwd * 4 + up * 10, ear + fwd * 2 + up * 34])
        cv.pencil(trim(tube, b_, a_) * K, 76, drawing, 2.0, 0.9, second=False)
    t0, t1 = B["throw"]
    if t0 <= f < B["leap"][1]:                          # the frisbee: in hand, then thrown out to the right
        rel = t0 + W["throw"]["release_frac"] * (t1 - t0)
        if f < rel:
            hands = lm_canvas(thrower, max(t0, 2 * drawing), [15, 16]); c = hands[int(np.argmax(hands[:, 0]))]
        else:
            t = window(f, rel, B["leap"][1]); hh = lm_canvas(thrower, int(rel), [15, 16]); h = hh[int(np.argmax(hh[:, 0]))]
            c = lerp(h, [660, GY - 240], t) + [0, -50 * np.sin(np.pi * t)]
        a_ = ease(window(f, t0, t0 + 8))
        cv.pencil(trim(circle(c, 15, 28, squash=0.35, rot=-0.2), 0, a_) * K, 95, drawing, 2.2, 0.9, second=False)

# ---------------- render ----------------
rng = range(TOTAL) if not a.only else range(*map(int, a.only.split("-")))
cache = {}; counts = []
for f in rng:
    drawing = f // 2; cv = Canvas(S)
    for pts, seed, w, al in world(f):
        pts = np.asarray(pts)
        if len(pts) > 1: cv.ribbon(pts * K, seed, drawing, w * K, al)
    back_props(f, cv, drawing)
    n = 0
    for k, fig in enumerate(FIGS):
        if not (fig.t0 <= f < fig.t1): continue
        key = (k, drawing)
        if key not in cache: cache[key] = fig.strokes(drawing)
        a_, b_ = fig.progress(f)
        hide = min(a_, 1 - b_)
        for kind, pts, seed in cache[key]:
            if kind == "fill":
                if hide > 0.05: cv.erase(pts, hide)
            elif kind == "hair":
                if a_ > 0.6 and b_ < 0.4: cv.mass(pts, drawing, getattr(fig, 'hair_alpha', 0.85))
            else:
                pts = trim(pts, b_, a_)
                if len(pts) > 1: cv.pencil(pts, 100 + seed + 50 * k, drawing, fig.weight * K * (0.55 + 0.45 * min(1, fig.size(f) * 1.5)), 0.95); n += 1
    front_props(f, cv, drawing)
    counts.append(n)
    cv.image().save(os.path.join(a.out, f"f{f:03d}.png"))
json.dump({"frames": TOTAL, "fps": 24}, open(os.path.join(a.out, "meta.json"), "w"))
print("rendered", len(counts), "frames; strokes per frame max", max(counts))
