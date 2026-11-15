"""Pencil toolkit shared by draw.py (the gate) and film.py (the full loop).

- Track: a tracked clip (masks + pose landmarks from extract.py) with helpers to get a smoothed
  outline at any fractional source frame.
- figure_strokes(): outline split at anatomical corners into a few strokes, with gaps,
  plus a solid hair mass for people.
- Canvas: accumulates pressure-ribbon strokes (coherent wobble that boils per drawing), with a
  paper-tooth texture, and composes laterite on the page colour.
"""
import os
import cv2, numpy as np
from PIL import Image

INK = np.array([164, 85, 58], float) / 255
BG = np.array([247, 245, 239], float) / 255     # page background #F7F5EF
SS = 2                                          # supersampling

# ---------- noise ----------
_LAT = np.random.default_rng(7).random((256, 256))
def noise(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int); xf, yf = x - xi, y - yi
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    g = lambda i, j: _LAT[(xi + i) & 255, (yi + j) & 255]
    return (g(0, 0) * (1 - u) + g(1, 0) * u) * (1 - v) + (g(0, 1) * (1 - u) + g(1, 1) * u) * v

# ---------- geometry ----------
def resample(pts, step):
    pts = np.asarray(pts, float)
    if len(pts) < 2: return pts
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    if cum[-1] < step: return pts
    t = np.append(np.arange(0, cum[-1], step), cum[-1])
    return np.stack([np.interp(t, cum, pts[:, 0]), np.interp(t, cum, pts[:, 1])], -1)

def chaikin(p, it=2):
    p = np.asarray(p, float)
    for _ in range(it):
        if len(p) < 3: return p
        q = np.empty((2 * len(p), 2)); q[0] = p[0]; q[-1] = p[-1]
        q[1:-1:2] = 0.75 * p[:-1] + 0.25 * p[1:]; q[2:-1:2] = 0.25 * p[:-1] + 0.75 * p[1:]
        p = q
    return p

def trim(pts, a, b):
    """keep the part of a polyline between fractions a and b of its length (for draw-on / draw-off)"""
    pts = np.asarray(pts, float)
    if a <= 0 and b >= 1: return pts
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); cum = np.concatenate([[0], np.cumsum(seg)])
    L = cum[-1]; t0, t1 = a * L, b * L
    if t1 - t0 < 1: return pts[:0]
    t = np.concatenate([[t0], cum[(cum > t0) & (cum < t1)], [t1]])
    return np.stack([np.interp(t, cum, pts[:, 0]), np.interp(t, cum, pts[:, 1])], -1)

def circle(c, r, n=40, a0=0.0, sweep=2 * np.pi, squash=1.0, rot=0.0):
    a = a0 + np.linspace(0, sweep, n)
    x, y = r * np.cos(a), r * squash * np.sin(a)
    cr, sr = np.cos(rot), np.sin(rot)
    return np.stack([c[0] + x * cr - y * sr, c[1] + x * sr + y * cr], -1)

def ease(t): t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)
def lerp(a, b, t): return np.asarray(a, float) * (1 - t) + np.asarray(b, float) * t

# ---------- tracked clips ----------
def movavg(x, k=5):
    pad = np.pad(x, [(k // 2, k // 2)] + [(0, 0)] * (x.ndim - 1), mode="edge")
    return np.mean([pad[i:i + len(x)] for i in range(k)], axis=0)

class Track:
    def __init__(self, path, blur=3.0):
        d = np.load(os.path.join(path, "track.npz"))
        self.lm = d["lm"].copy(); self.mask = d["mask"]; self.ms = float(d["scale"]); self.fps = float(d["fps"])
        ok = ~np.isnan(self.lm[:, 0, 0])
        if ok.any():  # fill gaps, then smooth
            idx = np.arange(len(self.lm))
            for j in range(33):
                for k in range(3):
                    self.lm[:, j, k] = np.interp(idx, idx[ok], self.lm[ok, j, k])
            self.lm[:, :, :3] = movavg(self.lm[:, :, :3], 5)
        self.has_pose = ok.mean() > 0.5
        area = np.array([(m > 128).sum() for m in self.mask]); self.valid = np.nonzero(area > 0.25 * np.median(area[area > 0]))[0] if (area > 0).any() else np.arange(len(self.mask))
        self.F = len(self.mask); self.blur = blur
        # per-frame mask centroid and bottom (source px), smoothed: used to stabilise or place figures
        cen, bot = [], []
        for m in self.mask:
            ys, xs = np.nonzero(m > 128)
            cen.append([xs.mean(), ys.mean()] if len(xs) else [np.nan, np.nan]); bot.append(ys.max() if len(ys) else np.nan)
        cen = np.array(cen) / self.ms; bot = np.array(bot) / self.ms
        g = ~np.isnan(cen[:, 0]); idx = np.arange(self.F)
        if g.any():
            cen = np.stack([np.interp(idx, idx[g], cen[g, 0]), np.interp(idx, idx[g], cen[g, 1])], -1); bot = np.interp(idx, idx[g], bot[g])
        self.cen = movavg(cen, 9); self.bot = movavg(bot[:, None], 9)[:, 0]

    def clampf(self, fi): return float(np.clip(fi, 0, self.F - 1.001))

    def outline(self, fi):
        fi = self.clampf(fi)
        if int(fi) not in self.valid or min(int(fi) + 1, self.F - 1) not in self.valid:
            fi = float(self.valid[np.argmin(np.abs(self.valid - fi))])
        i0 = int(fi); t = fi - i0
        m = (1 - t) * self.mask[i0].astype(float) + t * self.mask[min(i0 + 1, self.F - 1)].astype(float)
        m = cv2.GaussianBlur(m, (0, 0), self.blur)
        b = (m > 140).astype(np.uint8)
        cs, _ = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not cs: return None, b
        c = max(cs, key=cv2.contourArea)
        if cv2.contourArea(c) < 30: return None, b
        return c[:, 0, :].astype(float) / self.ms, b

    def lm_at(self, fi):
        fi = self.clampf(fi); i0 = int(fi); t = fi - i0
        return (1 - t) * self.lm[i0, :, :2] + t * self.lm[min(i0 + 1, self.F - 1), :, :2]

    def at(self, arr, fi):
        fi = self.clampf(fi); i0 = int(fi); t = fi - i0
        return (1 - t) * arr[i0] + t * arr[min(i0 + 1, self.F - 1)]

def split_contour(c, nmin=7, nmax=10, step=4.0):
    """split a closed contour at its sharpest corners into open arcs; returns [(arc, key)]"""
    c = resample(np.vstack([c, c[:1]]), step)[:-1]
    n = len(c)
    if n < 12: return [(c, 0)]
    w = max(3, min(9, n // 12))
    k = np.ones(7) / 7
    c = np.stack([np.convolve(np.r_[c[-3:, j], c[:, j], c[:3, j]], k, "valid") for j in range(2)], -1)
    a1 = c - np.roll(c, w, 0); a2 = np.roll(c, -w, 0) - c
    score = np.abs(np.arctan2(a1[:, 0] * a2[:, 1] - a1[:, 1] * a2[:, 0], (a1 * a2).sum(1)))
    picks = []; minsep = max(6, n // (nmax + 4))
    for i in np.argsort(-score):
        if score[i] < 0.55 and len(picks) >= nmin: break
        if all(min(abs(i - j), n - abs(i - j)) > minsep for j in picks): picks.append(i)
        if len(picks) >= nmax: break
    picks = sorted(picks)
    return [(c[np.arange(a_, b_ + 1) % n], a_) for a_, b_ in zip(picks, picks[1:] + [picks[0] + n])]

def _off_edge(arc, shape, ms, pad=6):
    H, W = shape[0] / ms, shape[1] / ms
    ok = (arc[:, 0] > pad / ms) & (arc[:, 0] < W - pad / ms) & (arc[:, 1] > pad / ms) & (arc[:, 1] < H - pad / ms)
    parts, run = [], []
    for p, k in zip(arc, ok):
        if k: run.append(p)
        else:
            if len(run) > 3: parts.append(np.array(run))
            run = []
    if len(run) > 3: parts.append(np.array(run))
    return parts

def figure_strokes(tr, fi, place, drawing, hair=True, nmax=10, scale_hint=1.0):
    """strokes for one drawing of a tracked figure. place(src_pts) -> canvas pts.
    Returns list of (kind, pts, seed): kind in outline | hair"""
    c, b = tr.outline(fi)
    if c is None: return []
    out = []
    arcs = [(p, a0 + 31 * k) for arc, a0 in split_contour(c, nmax=nmax, step=4.0 / max(scale_hint, 0.25)) for k, p in enumerate(_off_edge(arc, b.shape, tr.ms))]
    for arc, a0 in arcs:
        arc = place(arc)
        r1 = noise(a0 * 0.37, drawing * 0.8); r2 = noise(a0 * 0.37 + 9, drawing * 0.8)
        cut1, cut2 = int(r1 * 4), int(r2 * 4)
        if len(arc) > cut1 + cut2 + 4: arc = arc[cut1: len(arc) - cut2]
        if r1 > 0.62 and len(arc) > 2: arc = np.vstack([arc[0] - (arc[1] - arc[0]) * 3, arc])
        L = np.linalg.norm(np.diff(arc, axis=0), axis=1).sum()
        if L > 70 and noise(a0 * 0.21 + 4, drawing * 0.45) > 0.58:   # a break in a long line
            cum = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(arc, axis=0), axis=1))])
            at = L * (0.35 + 0.3 * noise(a0 * 0.5, drawing * 0.3)); gap = 3 + 5 * noise(a0, drawing)
            for part in (arc[cum < at - gap / 2], arc[cum > at + gap / 2]):
                if len(part) > 3: out.append(("outline", part, a0 + len(part)))
        else:
            out.append(("outline", arc, a0))
    if hair and tr.has_pose:
        P = tr.lm_at(fi); ear = (P[7] + P[8]) / 2; nose = P[0]
        hr = np.linalg.norm(nose - ear) * 1.25
        fwd = np.sign(nose[0] - ear[0]) or 1.0       # which way the face points in the source
        ys, xs = np.nonzero(b); X, Y = xs / tr.ms, ys / tr.ms
        if abs(nose[0] - ear[0]) < 0.35 * hr:        # facing the camera: a cap of hair above the brow
            ew = np.linalg.norm(P[7] - P[8]); hr = max(hr, ew * 0.9)
            edge = ear[1] - 0.45 * hr + 0.1 * hr * (noise(X * 0.08, drawing * 0.7) - 0.5) + 0.25 * hr * (np.abs(X - ear[0]) / hr) ** 2
            sel = (np.hypot(X - ear[0], Y - (ear[1] - 0.3 * hr)) < hr * 1.3) & (Y < edge)
        else:
            edge = ear[1] - 0.55 * hr + 0.55 * np.clip((nose[0] - X) * fwd, 0, None) + 0.12 * hr * (noise(X * 0.08, drawing * 0.7) - 0.5)
            sel = (np.hypot(X - ear[0], Y - (ear[1] - 0.25 * hr)) < hr * 1.2) & (Y < edge) & ((X - nose[0]) * fwd < -0.1 * hr)
        if sel.sum() > 20:
            hm = np.zeros_like(b); hm[ys[sel], xs[sel]] = 1
            cs, _ = cv2.findContours(hm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            hc = max(cs, key=cv2.contourArea)[:, 0, :].astype(float) / tr.ms
            out.append(("hair", place(hc), 0))
    return out

# ---------- canvas ----------
class Canvas:
    tooth = {}
    def __init__(self, S):
        self.S = S; self.ink = np.zeros((S * SS, S * SS))
        if S not in Canvas.tooth:
            gr = np.random.default_rng(3).random((S * SS, S * SS))
            gr = cv2.GaussianBlur(gr, (0, 0), 0.9); gr = (gr - gr.min()) / (gr.max() - gr.min())
            Canvas.tooth[S] = np.clip(0.55 + 0.7 * gr, 0, 1)

    def _fill(self, poly, alpha):
        m = np.zeros_like(self.ink, dtype=np.uint8)
        cv2.fillPoly(m, [(np.asarray(poly) * SS).astype(np.int32)], 255, lineType=cv2.LINE_AA)
        self.ink[:] = 1 - (1 - self.ink) * (1 - m / 255.0 * alpha)

    def ribbon(self, pts, seed, drawing, weight=3.0, alpha=0.95, wob=2.6, smooth=True):
        pts = np.asarray(pts, float)
        if len(pts) < 2: return
        sm = resample(chaikin(pts) if smooth else pts, 2.0); n = len(sm)
        if n < 3: return
        tg = np.gradient(sm, axis=0); tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-9
        nr = np.stack([-tg[:, 1], tg[:, 0]], -1); t = np.linspace(0, 1, n)
        press = 0.75 + 0.5 * noise(seed * 0.13, drawing * 0.21)
        prof = 0.25 + 0.75 * np.sin(np.pi * np.minimum(1, t * 1.08)) ** 0.55
        w = weight * press * prof * (0.8 + 0.4 * noise(seed + np.arange(n) * 0.09, drawing * 0.3))
        wb = (noise(seed * 0.7 + np.arange(n) * 0.045, drawing * 0.5 + 3.1) - 0.5) * wob
        cen = sm + nr * wb[:, None]
        self._fill(np.vstack([cen + nr * w[:, None] / 2, (cen - nr * w[:, None] / 2)[::-1]]), alpha)

    def pencil(self, pts, seed, drawing, weight=3.2, alpha=0.95, second=True):
        """a main stroke plus a faint second pass, like a pencil line gone over twice"""
        self.ribbon(pts, seed, drawing, weight, alpha)
        if second: self.ribbon(np.asarray(pts) + 1.2, 900 + seed, drawing + 50, weight * 0.4, alpha * 0.37)

    def mass(self, poly, drawing, alpha=0.85):
        poly = resample(np.vstack([poly, poly[:1]]), 3.0); j = np.arange(len(poly))
        rough = (noise(j * 0.15, drawing * 0.6) - 0.5) * 3.0
        c = poly.mean(0); v = poly - c; v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-9
        self._fill(c + (poly - c) * 0.97 + v * rough[:, None], alpha)

    def image(self):
        a = np.clip(self.ink * Canvas.tooth[self.S], 0, 1)
        a = cv2.resize(a, (self.S, self.S), interpolation=cv2.INTER_AREA)
        img = BG[None, None, :] * (1 - a[..., None]) + INK[None, None, :] * a[..., None]
        return Image.fromarray((img * 255).round().astype(np.uint8))
