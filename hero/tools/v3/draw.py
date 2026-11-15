"""Step 3-5 of the v3 pipeline: tracked motion -> pencil strokes -> frames.

Reads work/<name>/track.npz (from extract.py), finds a clean stride cycle, retimes it to a
real-time jog, and draws every drawing as a few pencil strokes:
  - the silhouette outline, split at anatomical corners (armpit, crotch, back of the knee,
    toes...) into 8-12 strokes with small gaps and overlaps;
  - inner lines where a near limb crosses the body (the arm over the torso, leg over leg).
Strokes are pressure ribbons with coherent wobble that boils on every drawing (ported from
hero/lab/v1/engine.js), with a paper-tooth texture. Characters on twos; the ground ticks
move on every frame.

Usage: .venv/bin/python draw.py work/jog out/jog --strides 2 --stride-frames 20
"""
import argparse, os, json
import cv2, numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("work"); ap.add_argument("out")
ap.add_argument("--strides", type=int, default=2)
ap.add_argument("--stride-frames", type=int, default=20, help="output frames (24 fps) per stride")
ap.add_argument("--size", type=int, default=600)
ap.add_argument("--fig-height", type=float, default=400, help="figure height in canvas px")
ap.add_argument("--debug", action="store_true")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

INK = np.array([164, 85, 58], float) / 255
BG = np.array([247, 245, 239], float) / 255     # page background #F7F5EF
SS = 2                                          # supersampling
S = a.size

d = np.load(os.path.join(a.work, "track.npz"))
LM, MASK, mscale = d["lm"].copy(), d["mask"], float(d["scale"])
F = len(LM)

# ---------- motion: smooth, find the stride period and the best loop window ----------
def movavg(x, k=5):
    pad = np.pad(x, [(k // 2, k // 2)] + [(0, 0)] * (x.ndim - 1), mode="edge")
    return np.mean([pad[i:i + len(x)] for i in range(k)], axis=0)
LM[:, :, :3] = movavg(LM[:, :, :3], 5)

hip = (LM[:, 23, :2] + LM[:, 24, :2]) / 2
def feat(i):  # pose relative to the hips, for matching
    return (LM[i, 11:33, :2] - hip[i]).ravel()
FE = np.array([feat(i) for i in range(F)])
sig = LM[:, 27, 0] - LM[:, 28, 0]
sig = sig - sig.mean()
ac = np.correlate(sig, sig, "full")[F - 1:]
P0 = int(np.argmax(ac[30:150]) + 30)            # rough stride period in source frames
span = a.strides * P0
best = None
for s in range(5, F - span - 10):
    for L in range(span - 6, span + 7):
        if s + L >= F - 2: continue
        e = np.linalg.norm(FE[s] - FE[s + L]) + 0.5 * np.linalg.norm((FE[s + 1] - FE[s]) - (FE[s + L + 1] - FE[s + L]))
        if best is None or e < best[0]: best = (e, s, L)
_, START, LOOP = best
N = a.strides * a.stride_frames                  # output frames in the loop
print(f"stride ~{P0} src frames; loop src {START}..{START + LOOP} ({LOOP} frames) -> {N} frames at 24 fps")

# ---------- placement: source px -> canvas px ----------
hx = movavg(hip[:, 0:1], 25)[:, 0]
top = np.nanmin(LM[START:START + LOOP, [0, 2, 5, 7, 8], 1]) - 40
feet = np.median([np.nonzero(MASK[j] > 140)[0].max() for j in range(START, START + LOOP)]) / mscale
K = a.fig_height / (feet - top)
GROUND = S * 0.86
def to_canvas(pts, i):
    pts = np.asarray(pts, float)
    return np.stack([S * 0.5 + (pts[..., 0] - hx[i]) * K, GROUND + (pts[..., 1] - feet) * K], -1)

# belt speed from the stance foot: how fast the ground slides backwards (source px / src frame)
vel = np.diff(LM[:, [27, 28], 0], axis=0)
low = LM[1:, [27, 28], 1] > feet - 0.12 * (feet - top)
belt = -np.median(vel[low & (vel < 0)])

# ---------- noise ----------
rng = np.random.default_rng(7)
LAT = rng.random((256, 256))
def noise(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int); xf, yf = x - xi, y - yi
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    g = lambda i, j: LAT[(xi + i) & 255, (yi + j) & 255]
    return (g(0, 0) * (1 - u) + g(1, 0) * u) * (1 - v) + (g(0, 1) * (1 - u) + g(1, 1) * u) * v
def fbm(x, y): return 0.6 * noise(x, y) + 0.3 * noise(2.03 * x, 2.03 * y) + 0.1 * noise(4.1 * x, 4.1 * y)

# ---------- geometry helpers ----------
def resample(pts, step):
    pts = np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    if cum[-1] < step: return pts
    t = np.arange(0, cum[-1], step)
    return np.stack([np.interp(t, cum, pts[:, 0]), np.interp(t, cum, pts[:, 1])], -1)

def chaikin(p, it=2):
    for _ in range(it):
        q = np.empty((2 * len(p) - 2 + 2, 2)); q[0] = p[0]; q[-1] = p[-1]
        q[1:-1:2] = 0.75 * p[:-1] + 0.25 * p[1:]; q[2:-1:2] = 0.25 * p[:-1] + 0.75 * p[1:]
        p = q
    return p

def silhouette(fi):
    """blended mask at fractional source frame -> smoothed outer contour in source px"""
    i0 = int(np.floor(fi)); t = fi - i0
    m = (1 - t) * MASK[i0].astype(float) + t * MASK[min(i0 + 1, F - 1)].astype(float)
    m = cv2.GaussianBlur(m, (0, 0), 3.0)
    b = (m > 140).astype(np.uint8)
    cs, _ = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float) / mscale
    return c, b

def split_contour(c, nmin=7, nmax=10):
    """split a closed contour at its sharpest corners into open arcs"""
    c = resample(np.vstack([c, c[:1]]), 4.0)[:-1]
    n = len(c); w = 9
    # smooth closed
    k = np.ones(7) / 7
    c = np.stack([np.convolve(np.r_[c[-3:, j], c[:, j], c[:3, j]], k, "valid") for j in range(2)], -1)
    a1 = c - np.roll(c, w, 0); a2 = np.roll(c, -w, 0) - c
    ang = np.arctan2(a1[:, 0] * a2[:, 1] - a1[:, 1] * a2[:, 0], (a1 * a2).sum(1))
    score = np.abs(ang)
    order = np.argsort(-score); picks = []
    minsep = max(12, n // (nmax + 4))
    for i in order:
        if score[i] < 0.55 and len(picks) >= nmin: break
        if all(min(abs(i - j), n - abs(i - j)) > minsep for j in picks): picks.append(i)
        if len(picks) >= nmax: break
    picks = sorted(picks)
    arcs = []
    for a_, b_ in zip(picks, picks[1:] + [picks[0] + n]):
        idx = np.arange(a_, b_ + 1) % n
        arcs.append((c[idx], a_))
    return arcs

def limb_edges(chain, radii, inside, side_sign):
    """outline lines of a limb (one side or both) kept only where they fall inside the body mask"""
    out = []
    for sgn in side_sign:
        pts = []
        for (p, q), r in zip(zip(chain[:-1], chain[1:]), radii):
            d_ = q - p; L = np.linalg.norm(d_) + 1e-6; nrm = np.array([-d_[1], d_[0]]) / L
            for t in np.linspace(0, 1, 8, endpoint=False):
                pts.append(p + d_ * t + nrm * r * sgn * (1 - 0.15 * t))
        pts.append(chain[-1])
        pts = np.array(pts)
        keep = np.array([inside(p) for p in pts])
        run = []
        for p, k in zip(pts, keep):
            if k: run.append(p)
            elif len(run) > 4: out.append(np.array(run)); run = []
            else: run = []
        if len(run) > 4: out.append(np.array(run))
    return out

# ---------- pencil ribbon renderer ----------
YY, XX = np.mgrid[0:S * SS, 0:S * SS]
def ribbon(ink, pts, seed, drawing, weight, alpha):
    sm = resample(chaikin(np.asarray(pts, float)), 2.0)
    n = len(sm)
    if n < 4: return
    tg = np.gradient(sm, axis=0); tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-9
    nr = np.stack([-tg[:, 1], tg[:, 0]], -1)
    t = np.linspace(0, 1, n)
    press = 0.75 + 0.5 * noise(seed * 0.13, drawing * 0.21)
    prof = 0.25 + 0.75 * np.sin(np.pi * np.minimum(1, t * 1.08)) ** 0.55
    w = weight * press * prof * (0.8 + 0.4 * noise(seed + np.arange(n) * 0.09, drawing * 0.3))
    wob = (noise(seed * 0.7 + np.arange(n) * 0.045, drawing * 0.5 + 3.1) - 0.5) * 2.6
    cen = sm + nr * wob[:, None]
    L = cen + nr * w[:, None] / 2; R = cen - nr * w[:, None] / 2
    poly = (np.vstack([L, R[::-1]]) * SS).astype(np.int32)
    m = np.zeros((S * SS, S * SS), np.uint8)
    cv2.fillPoly(m, [poly], 255, lineType=cv2.LINE_AA)
    a_ = (m / 255.0) * alpha
    ink[:] = 1 - (1 - ink) * (1 - a_)

# paper tooth: graphite catches on the grain, so ink is broken by a fixed paper texture
gr = np.random.default_rng(3).random((S * SS, S * SS))
gr = cv2.GaussianBlur(gr, (0, 0), 0.9); gr = (gr - gr.min()) / (gr.max() - gr.min())
TOOTH = np.clip(0.55 + 0.7 * gr, 0, 1)

def compose(ink):
    a_ = np.clip(ink * TOOTH, 0, 1)
    a_ = cv2.resize(a_, (S, S), interpolation=cv2.INTER_AREA)
    img = BG[None, None, :] * (1 - a_[..., None]) + INK[None, None, :] * a_[..., None]
    return Image.fromarray((img * 255).round().astype(np.uint8))

# ---------- per drawing ----------
def near_side(i):
    zl = LM[i, [11, 13, 23, 25], 2].mean(); zr = LM[i, [12, 14, 24, 26], 2].mean()
    return "R" if zr < zl else "L"
IDX = {"L": dict(sh=11, el=13, wr=15, hip=23, kn=25, an=27, ft=31), "R": dict(sh=12, el=14, wr=16, hip=24, kn=26, an=28, ft=32)}

def lm_at(fi):
    i0 = int(np.floor(fi)); t = fi - i0
    return (1 - t) * LM[i0, :, :2] + t * LM[min(i0 + 1, F - 1), :, :2]

def strokes_for(drawing):
    fi = START + LOOP * (drawing * 2) / N
    i = int(round(fi))
    c, b = silhouette(fi)
    out = []
    arcs = split_contour(c)
    for k, (arc, a0) in enumerate(arcs):
        arc = to_canvas(arc, i)
        # gaps and overlaps at the joins, changing a little per drawing
        r1 = noise(a0 * 0.37, drawing * 0.8); r2 = noise(a0 * 0.37 + 9, drawing * 0.8)
        cut1 = int(r1 * 4); cut2 = int(r2 * 4)
        arc = arc[cut1: len(arc) - cut2] if len(arc) > cut1 + cut2 + 4 else arc
        if r1 > 0.62:   # overshoot the start a little, like a pencil starting early
            arc = np.vstack([arc[0] - (arc[1] - arc[0]) * 3, arc])
        seglen = np.linalg.norm(np.diff(arc, axis=0), axis=1).sum()
        if seglen > 110 and noise(a0 * 0.21 + 4, drawing * 0.45) > 0.58:   # a break in a long line
            cum = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(arc, axis=0), axis=1))])
            at = cum[-1] * (0.35 + 0.3 * noise(a0 * 0.5, drawing * 0.3)); gap = 5 + 6 * noise(a0, drawing)
            p1, p2 = arc[cum < at - gap / 2], arc[cum > at + gap / 2]
            for part in (p1, p2):
                if len(part) > 3: out.append(("outline", part, a0 * 1.0 + len(part)))
        else:
            out.append(("outline", arc, a0 * 1.0))
    # inner lines: the near arm over the torso, the near leg over the far leg
    side = near_side(i); J = IDX[side]; P = lm_at(fi)
    er = cv2.erode(b, np.ones((9, 9), np.uint8))
    def inside(p):
        x, y = int(p[0] * mscale), int(p[1] * mscale)
        return 0 <= y < er.shape[0] and 0 <= x < er.shape[1] and er[y, x] > 0
    arm = np.array([P[J["sh"]], P[J["el"]], P[J["wr"]]])
    for e in limb_edges(arm, [30, 24], inside, (1, -1)):
        out.append(("inner", to_canvas(e, i), 500 + len(out)))
    leg = np.array([P[J["hip"]], P[J["kn"]], P[J["an"]]])
    for e in limb_edges(leg, [44, 32], inside, (1, -1)):
        if len(e) > 6: out.append(("inner", to_canvas(e, i), 700 + len(out)))
    ear = (P[7] + P[8]) / 2; nose = P[0]
    hr = np.linalg.norm(nose - ear) * 1.25
    ys, xs = np.nonzero(b)
    X, Y = xs / mscale, ys / mscale
    edge = ear[1] - 0.55 * hr + 0.55 * np.clip(nose[0] - X, 0, None) + 0.12 * hr * (noise(X * 0.08, drawing * 0.7) - 0.5)   # hairline: high at the brow, low at the nape
    sel = (np.hypot(X - ear[0], Y - (ear[1] - 0.25 * hr)) < hr * 1.2) & (Y < edge) & (X < nose[0] - 0.1 * hr)
    if sel.sum() > 20:
        hm = np.zeros_like(b); hm[ys[sel], xs[sel]] = 1
        cs, _ = cv2.findContours(hm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        hc = max(cs, key=cv2.contourArea)[:, 0, :].astype(float) / mscale
        out.append(("hair", to_canvas(hc, i), 0))
    return out, i

def hair(ink, poly, drawing):
    poly = resample(np.vstack([poly, poly[:1]]), 3.0)
    j = np.arange(len(poly))
    rough = (noise(j * 0.15, drawing * 0.6) - 0.5) * 3.0
    c = poly.mean(0); v = poly - c; v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
    poly = c + (poly - c) * 0.97 + v * rough[:, None]
    m = np.zeros((S * SS, S * SS), np.uint8)
    cv2.fillPoly(m, [(poly * SS).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    a_ = m / 255.0 * 0.85
    ink[:] = 1 - (1 - ink) * (1 - a_)

meta = {"source_start": int(START), "source_frames": int(LOOP), "frames": N, "fps": 24, "drawings": N // 2, "strokes": []}
cache = {}
belt_canvas = belt * K * (LOOP / N)               # canvas px per output frame
tick_gap = belt_canvas * N / round(belt_canvas * N / 46)   # loop-exact tick spacing
for f in range(N):
    drawing = f // 2
    if drawing not in cache: cache[drawing] = strokes_for(drawing)
    strokes, i = cache[drawing]
    ink = np.zeros((S * SS, S * SS))
    # ground: one long boiling line plus short ticks sliding back with the belt, every frame
    g = np.array([[S * 0.12, GROUND + 6], [S * 0.88, GROUND + 6]])
    ribbon(ink, resample(g, 20), 11, drawing, 2.0, 0.55)
    off = (f * belt_canvas) % tick_gap
    x = S * 0.16 - off + tick_gap
    while x < S * 0.84:
        y = GROUND + 18 + 4 * noise(x * 0.01, 0)
        ribbon(ink, [[x, y], [x + 7, y], [x + 16, y + 0.5]], int(x * 13) % 97 + 20, drawing, 1.4, 0.35)
        x += tick_gap
    for kind, pts, seed in strokes:
        if kind == "outline":
            ribbon(ink, pts, 100 + seed, drawing, 3.2, 0.95)
            ribbon(ink, pts + 1.2, 900 + seed, drawing + 50, 1.3, 0.35)   # a faint second pass
        elif kind == "hair":
            hair(ink, pts, drawing)
        else: ribbon(ink, pts, seed, drawing, 2.0, 0.7)
    compose(ink).save(os.path.join(a.out, f"f{f:03d}.png"))
    if f % 2 == 0: meta["strokes"].append(len(strokes))
json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
print("strokes per drawing:", meta["strokes"])
