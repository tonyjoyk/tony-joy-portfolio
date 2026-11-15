"""Rigs for Tony and Juhu: joint skeletons that output named contour strokes (not stick figures).

Conventions (screen coords, y down, characters face +x):
  dirv(a): unit vector for a limb at angle a degrees, 0 = straight down, +90 = forward (+x), 180 = up.
  rot (body pitch) turns the whole body clockwise around its root: +rot pitches forward / head-down.
Every stroke is returned as a list of points; tools/keyframes.py resamples them to a fixed count.
"""
import math

def dirv(a):
    r = math.radians(a); return (math.sin(r), math.cos(r))

def add(p, v, k=1.0): return (p[0] + v[0] * k, p[1] + v[1] * k)
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
def norm(v):
    l = math.hypot(*v) or 1; return (v[0] / l, v[1] / l)
def perp(v): return (-v[1], v[0])                       # rotate +90 (for a downward bone, points to -x... see side())
def rotp(p, c, deg):
    r = math.radians(deg); x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r))

def contour(a, b, ra, rb, side, bulge=0.12, n=9):
    """One side of a tapered body part from a to b. side=+1 / -1. Slight muscle bulge mid-way."""
    d = norm(sub(b, a)); nv = (d[1] * side, -d[0] * side)
    out = []
    for i in range(n):
        t = i / (n - 1); r = ra + (rb - ra) * t; r *= 1 + bulge * math.sin(math.pi * t)
        out.append(add(lerp(a, b, t), nv, r))
    return out

def ik2(root, target, l1, l2, bend):
    """2-bone IK: returns middle joint. bend=+1 bends the joint toward +x side of the root->target line."""
    dx, dy = target[0] - root[0], target[1] - root[1]; d = min(math.hypot(dx, dy), l1 + l2 - 0.01)
    a = math.atan2(dy, dx); cos1 = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d); cos1 = max(-1, min(1, cos1))
    ang = a - bend * math.acos(cos1)
    return (root[0] + l1 * math.cos(ang), root[1] + l1 * math.sin(ang))

# ---------------------------------------------------------------- Tony
TONY_STROKES = ["t-head", "t-hair", "t-ear", "t-neck-a", "t-neck-b", "t-torso-a", "t-torso-b", "t-hem", "t-shorts",
    "t-arm-f-up-a", "t-arm-f-up-b", "t-arm-f-lo-a", "t-arm-f-lo-b", "t-hand-f",
    "t-leg-f-thigh-a", "t-leg-f-thigh-b", "t-leg-f-shin-a", "t-leg-f-shin-b", "t-foot-f",
    "t-leg-n-thigh-a", "t-leg-n-thigh-b", "t-leg-n-shin-a", "t-leg-n-shin-b", "t-foot-n",
    "t-arm-n-up-a", "t-arm-n-up-b", "t-arm-n-lo-a", "t-arm-n-lo-b", "t-hand-n"]
GEAR_STROKES = ["g-goggle", "g-snorkel", "g-fin-n", "g-fin-f"]

TL = dict(torso=56, neck=8, head=11, up=30, lo=27, hand=9, thigh=43, shin=41, foot=15)

def tony(x, y, s=1.0, rot=0, torso=8, head=0, an=-20, en=80, af=20, ef=80,
         ln=15, kn=10, fn=0, lf=-15, kf=30, ff=0, hand_n=None, hand_f=None, foot_n=None, foot_f=None, gear=False, flip=False):
    """Pelvis at (x, y). Angles in degrees (see module doc). Optional IK targets (world coords, before rot) for hands/feet."""
    L = {k: v * s for k, v in TL.items()}
    P = (0.0, 0.0)
    up = (math.sin(math.radians(torso)), -math.cos(math.radians(torso)))
    fwd = (-up[1], up[0])                                  # forward normal of the torso (+x when upright)
    N = add(P, up, L["torso"]); S = add(P, up, L["torso"] - 6 * s)
    hd = (math.sin(math.radians(torso + head)), -math.cos(math.radians(torso + head)))
    H = add(N, hd, L["neck"] + L["head"])
    j = {"P": P, "N": N, "S": S, "H": H}
    def local(pt): return None if pt is None else rotp((pt[0] - x, pt[1] - y), (0, 0), -rot)
    for side, a, e, tgt in (("n", an, en, local(hand_n)), ("f", af, ef, local(hand_f))):
        sh = add(S, fwd, (2 if side == "n" else -2) * s)
        if tgt is not None:
            el = ik2(sh, tgt, L["up"], L["lo"], -1); wr = tgt if math.dist(sh, tgt) < L["up"] + L["lo"] else add(el, norm(sub(tgt, el)), L["lo"])
            ang = math.degrees(math.atan2(wr[0] - el[0], wr[1] - el[1]))
        else:
            el = add(sh, dirv(a), L["up"]); ang = a + e; wr = add(el, dirv(ang), L["lo"])
        j["sh" + side], j["el" + side], j["wr" + side] = sh, el, wr
        j["ht" + side] = add(wr, dirv(ang + 8), L["hand"])
    for side, l, k, f, tgt in (("n", ln, kn, fn, local(foot_n)), ("f", lf, kf, ff, local(foot_f))):
        hp = add(P, fwd, (3 if side == "n" else -1) * s)
        if tgt is not None:
            kn_ = ik2(hp, tgt, L["thigh"], L["shin"], 1); an_ = tgt if math.dist(hp, tgt) < L["thigh"] + L["shin"] else add(kn_, norm(sub(tgt, kn_)), L["shin"])
            sa = math.degrees(math.atan2(an_[0] - kn_[0], an_[1] - kn_[1]))
        else:
            kn_ = add(hp, dirv(l), L["thigh"]); sa = l - k; an_ = add(kn_, dirv(sa), L["shin"])
        j["hp" + side], j["kn" + side], j["an" + side] = hp, kn_, an_
        j["to" + side] = add(an_, dirv(sa + 90 + f), L["foot"])
        j["sa" + side] = sa
    # world transform
    W = {k: (rotp(v, (0, 0), rot)[0] + x, rotp(v, (0, 0), rot)[1] + y) if isinstance(v, tuple) else v for k, v in j.items()}
    return W, s, rot + torso, rot + torso + head, (x if flip else None)

def mirror(strokes, cx):
    return {k: [(2 * cx - x, y) for x, y in v] for k, v in strokes.items()} if cx is not None else strokes

def tony_strokes(pose):
    return mirror(_tony_strokes(pose), pose[4])

def _tony_strokes(pose):
    W, s, trs, hdang, _ = pose
    out = {}
    # torso contours with chest and back shapes
    P, N = W["P"], W["N"]; ax = norm(sub(N, P)); fw = (-ax[1], ax[0])
    def torso_side(sign, prof):
        pts = []
        for i, r in enumerate(prof):
            t = i / (len(prof) - 1); pts.append(add(lerp(P, N, t), fw, sign * r * s))
        return pts
    out["t-torso-a"] = torso_side(+1, [13, 12, 12.5, 15, 16, 13.5, 8])          # belly -> chest -> throat
    out["t-torso-b"] = torso_side(-1, [14, 12, 11, 12, 14, 12.5, 7])         # lower back -> shoulder blade
    out["t-hem"] = [add(lerp(P, N, .22), fw, 13 * s), add(lerp(P, N, .2), fw, 0), add(lerp(P, N, .22), fw, -14 * s)]
    # head: skull + face profile, facing the head direction
    H = W["H"]; hu = (math.sin(math.radians(hdang)), -math.cos(math.radians(hdang))); hf = (-hu[1], hu[0]); R = 11 * s
    def hp(fx, fy): return (H[0] + hf[0] * fx * R + hu[0] * fy * R, H[1] + hf[1] * fx * R + hu[1] * fy * R)
    head = []
    for k in range(13):                                  # from back of neck over the crown to the brow
        a = math.radians(200 - 140 * k / 12); head.append(hp(math.cos(a) * .95, math.sin(a) * 1.08))
    head += [hp(.98, .2), hp(1.12, -.08), hp(.98, -.28), hp(.95, -.5), hp(.82, -.82), hp(.45, -1.0), hp(.1, -.9)]   # nose, mouth, chin, jaw
    out["t-head"] = head
    out["t-hair"] = [hp(-.95, .2), hp(-.9, .75), hp(-.45, 1.2), hp(.2, 1.22), hp(.75, .95), hp(.95, .55)]
    out["t-ear"] = [hp(-.05, .2), hp(-.28, .25), hp(-.32, -.05), hp(-.12, -.2)]
    out["t-neck-a"] = [hp(.3, -.92), lerp(W["N"], add(W["N"], fw, 5 * s), 1)]
    out["t-neck-b"] = [hp(-.6, -.75), add(W["N"], fw, -5 * s)]
    th = norm(sub(W["knn"], W["hpn"])); thp = perp(th)          # shorts hem across the near thigh
    out["t-shorts"] = [add(lerp(W["hpn"], W["knn"], .42), thp, 12.5 * s), add(lerp(W["hpn"], W["knn"], .46), thp, -12.5 * s)]
    for sd in ("n", "f"):
        out[f"t-arm-{sd}-up-a"] = contour(W["sh" + sd], W["el" + sd], 6.5 * s, 5 * s, 1)
        out[f"t-arm-{sd}-up-b"] = contour(W["sh" + sd], W["el" + sd], 6.5 * s, 5 * s, -1)
        out[f"t-arm-{sd}-lo-a"] = contour(W["el" + sd], W["wr" + sd], 5 * s, 3.8 * s, 1)
        out[f"t-arm-{sd}-lo-b"] = contour(W["el" + sd], W["wr" + sd], 5 * s, 3.8 * s, -1)
        wr, ht = W["wr" + sd], W["ht" + sd]; d = norm(sub(ht, wr)); p = perp(d)
        out[f"t-hand-{sd}"] = [add(wr, p, 3 * s), add(lerp(wr, ht, .6), p, 3.5 * s), add(ht, d, 1 * s), add(lerp(wr, ht, .6), p, -3 * s), add(wr, p, -2.5 * s)]
        out[f"t-leg-{sd}-thigh-a"] = contour(W["hp" + sd], W["kn" + sd], 11.5 * s, 7.5 * s, 1)
        out[f"t-leg-{sd}-thigh-b"] = contour(W["hp" + sd], W["kn" + sd], 11.5 * s, 7.5 * s, -1)
        out[f"t-leg-{sd}-shin-a"] = contour(W["kn" + sd], W["an" + sd], 7.5 * s, 4.5 * s, 1, .18)
        out[f"t-leg-{sd}-shin-b"] = contour(W["kn" + sd], W["an" + sd], 7.5 * s, 4.5 * s, -1, .18)
        an_, to = W["an" + sd], W["to" + sd]; d = norm(sub(to, an_)); p = perp(d)
        heel = add(an_, d, -4 * s)
        out[f"t-foot-{sd}"] = [add(heel, p, 3 * s), add(heel, p, -3.5 * s), add(to, p, -3 * s), add(to, d, 2 * s), add(lerp(an_, to, .5), p, 4.5 * s), add(an_, p, 4 * s)]
    return out

def gear_strokes(pose):
    return mirror(_gear_strokes(pose), pose[4])

def _gear_strokes(pose):
    W, s, trs, hdang, _ = pose
    H = W["H"]; hu = (math.sin(math.radians(hdang)), -math.cos(math.radians(hdang))); hf = (-hu[1], hu[0]); R = 11 * s
    def hp(fx, fy): return (H[0] + hf[0] * fx * R + hu[0] * fy * R, H[1] + hf[1] * fx * R + hu[1] * fy * R)
    gog = [hp(.55 + .5 * math.cos(math.radians(a)), .25 + .38 * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    out = {"g-goggle": gog, "g-snorkel": [hp(.7, -.6), hp(.2, -.9), hp(-.55, -.6), hp(-.75, .6), hp(-.6, 1.6)]}
    for sd in ("n", "f"):
        an_, to = W["an" + sd], W["to" + sd]; d = norm(sub(to, an_)); p = perp(d)
        tip = add(to, d, 26 * s)
        out[f"g-fin-{sd}"] = [add(an_, p, 4 * s), add(tip, p, 9 * s), add(tip, p, -9 * s), add(an_, p, -4 * s)]
    return out

# ---------------------------------------------------------------- Juhu (German Shepherd)
JUHU_STROKES = ["j-ear-f", "j-bl-f-a", "j-bl-f-b", "j-bl-f-paw", "j-fl-f-a", "j-fl-f-b", "j-fl-f-paw",
    "j-tail-a", "j-tail-b", "j-back", "j-belly", "j-chest", "j-head", "j-jaw", "j-ear-n",
    "j-bl-n-a", "j-bl-n-b", "j-bl-n-paw", "j-fl-n-a", "j-fl-n-b", "j-fl-n-paw"]

def juhu(x, y, s=1.0, rot=0, spine=0, neck=35, head=20, fa=10, fb=-5, ffa=-10, ffb=0,
         ba=-10, bk=35, bh=25, bfa=10, bfk=35, bfh=25, ta=40, tb=25, mouth=0, flip=False):
    """Hip at (x, y). spine: chest-up angle. neck: degrees above forward. head: muzzle tilt down.
    Front legs fa/fb, back legs ba (thigh) bk (stifle bend) bh (hock bend). Tail ta, tb: droop below backward-horizontal."""
    L = lambda v: v * s
    Hp = (0.0, 0.0)
    C = (L(66) * math.cos(math.radians(spine)), -L(66) * math.sin(math.radians(spine)))
    sp = norm(sub(C, Hp)); top = (sp[1], -sp[0])                 # 'up' normal of the spine
    wit = add(C, top, L(22)); crp = add(Hp, top, L(17))
    nb = add(wit, (math.cos(math.radians(neck)), -math.sin(math.radians(neck))), L(26))
    md = (math.cos(math.radians(head)), math.sin(math.radians(head)))
    nose = add(nb, md, L(32))
    j = {"Hp": Hp, "C": C, "wit": wit, "crp": crp, "nb": nb, "nose": nose}
    for sd, a, b in (("n", fa, fb), ("f", ffa, ffb)):
        r = add(C, top, -L(10)); el = add(r, dirv(a), L(22)); pw = add(el, dirv(a + b), L(24))
        j["fr" + sd], j["fe" + sd], j["fp" + sd] = r, el, pw
    for sd, a, k, h in (("n", ba, bk, bh), ("f", bfa, bfk, bfh)):
        r = add(Hp, top, -L(2)); st = add(r, dirv(a), L(25)); hk = add(st, dirv(a - k), L(22)); pw = add(hk, dirv(a - k + h), L(16))
        j["br" + sd], j["bs" + sd], j["bh" + sd], j["bp" + sd] = r, st, hk, pw
    back = (-sp[0], -sp[1])                                     # tail droops below the backward direction
    bdir = rotp(back, (0, 0), -ta); t1 = add(crp, bdir, L(20))
    bdir2 = rotp(back, (0, 0), -tb); t2 = add(t1, bdir2, L(22))
    j["t1"], j["t2"] = t1, t2
    j["mouth"] = mouth
    W = {k: ((rotp(v, (0, 0), rot)[0] + x, rotp(v, (0, 0), rot)[1] + y) if isinstance(v, tuple) else v) for k, v in j.items()}
    return W, s, (x if flip else None)

def juhu_strokes(pose):
    return mirror(_juhu_strokes(pose), pose[2])

def _juhu_strokes(pose):
    W, s, _ = pose
    L = lambda v: v * s
    out = {}
    C, Hp, wit, crp, nb, nose = W["C"], W["Hp"], W["wit"], W["crp"], W["nb"], W["nose"]
    sp = norm(sub(C, Hp)); top = (sp[1], -sp[0])
    md = norm(sub(nose, nb)); mu = (md[1], -md[0]) if md[0] >= 0 else (-md[1], md[0])
    skull = add(nb, md, L(6))
    out["j-back"] = [add(nb, mu, L(5)), lerp(wit, nb, .45), wit, add(lerp(wit, crp, .5), top, -L(2)), crp, add(crp, sp, -L(6))]
    chest_front = add(add(C, sp, L(12)), top, -L(4))
    out["j-chest"] = [add(nb, mu, -L(6)), lerp(add(nb, mu, -L(6)), chest_front, .5), chest_front, add(add(C, sp, L(4)), top, -L(22)), add(C, top, -L(24))]
    out["j-belly"] = [add(C, top, -L(24)), add(lerp(C, Hp, .4), top, -L(19)), add(lerp(C, Hp, .75), top, -L(9)), add(add(Hp, sp, L(8)), top, -L(5))]
    stop = add(skull, mu, L(9))
    out["j-head"] = [add(nb, mu, L(4)), add(skull, mu, L(10)), stop, add(lerp(stop, nose, .5), mu, L(3)), add(nose, mu, L(2)), add(nose, md, L(2))]
    mo = W["mouth"]
    jaw_open = add(lerp(skull, nose, .9), mu, -L(4 + mo * 8))
    out["j-jaw"] = [add(nose, mu, -L(1)), jaw_open, add(lerp(skull, nose, .35), mu, -L(7)), add(nb, mu, -L(6))]
    for sd, off in (("n", 0), ("f", -L(5))):
        b = add(add(skull, md, -L(4) + off), mu, L(8)); tip = add(add(b, mu, L(17)), md, -L(5)); b2 = add(b, md, L(8))
        out[f"j-ear-{sd}"] = [b, tip, b2]
        out[f"j-fl-{sd}-a"] = contour(W["fr" + sd], W["fe" + sd], L(7), L(4.5), 1) + contour(W["fe" + sd], W["fp" + sd], L(4.5), L(3.2), 1)[1:]
        out[f"j-fl-{sd}-b"] = contour(W["fr" + sd], W["fe" + sd], L(7), L(4.5), -1) + contour(W["fe" + sd], W["fp" + sd], L(4.5), L(3.2), -1)[1:]
        p = W["fp" + sd]; d = norm(sub(W["fp" + sd], W["fe" + sd])); f = perp(d)
        out[f"j-fl-{sd}-paw"] = [add(p, f, L(3.5)), add(add(p, d, L(3)), f, L(6)), add(p, d, L(4)), add(p, f, -L(3))]
        out[f"j-bl-{sd}-a"] = contour(W["br" + sd], W["bs" + sd], L(11), L(6), 1) + contour(W["bs" + sd], W["bh" + sd], L(6), L(3.5), 1)[1:] + contour(W["bh" + sd], W["bp" + sd], L(3.5), L(3), 1)[1:]
        out[f"j-bl-{sd}-b"] = contour(W["br" + sd], W["bs" + sd], L(11), L(6), -1) + contour(W["bs" + sd], W["bh" + sd], L(6), L(3.5), -1)[1:] + contour(W["bh" + sd], W["bp" + sd], L(3.5), L(3), -1)[1:]
        p = W["bp" + sd]; d = norm(sub(W["bp" + sd], W["bh" + sd])); f = perp(d)
        out[f"j-bl-{sd}-paw"] = [add(p, f, L(3.5)), add(add(p, d, L(3)), f, L(6)), add(p, d, L(4)), add(p, f, -L(3))]
    t1, t2 = W["t1"], W["t2"]
    out["j-tail-a"] = contour(crp, t1, L(4), L(6), 1, .3) + contour(t1, t2, L(6), L(1.5), 1, .2)[1:]
    out["j-tail-b"] = contour(crp, t1, L(4), L(6), -1, .3) + contour(t1, t2, L(6), L(1.5), -1, .2)[1:]
    return out

FAR = lambda name: "-f-" in name or name.endswith("-f") or name in ("j-ear-f",)
