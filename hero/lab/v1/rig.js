// Rigs for Tony and Juhu (JavaScript port of hero/tools/rig.py).
// Screen coords, y down, characters face +x. dirv(a): 0 = down, +90 = forward, 180 = up.
// rot pitches the whole body clockwise around its root (+rot = forward / head-down).
const Rig = (function () {
  const R = d => d * Math.PI / 180;
  const dirv = a => [Math.sin(R(a)), Math.cos(R(a))];
  const add = (p, v, k = 1) => [p[0] + v[0] * k, p[1] + v[1] * k];
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  const norm = v => { const l = Math.hypot(v[0], v[1]) || 1; return [v[0] / l, v[1] / l]; };
  const perp = v => [-v[1], v[0]];
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
  const rotp = (p, c, deg) => {
    const r = R(deg), x = p[0] - c[0], y = p[1] - c[1];
    return [c[0] + x * Math.cos(r) - y * Math.sin(r), c[1] + x * Math.sin(r) + y * Math.cos(r)];
  };

  function contour(a, b, ra, rb, side, bulge = 0.12, n = 9) {
    const d = norm(sub(b, a)), nv = [d[1] * side, -d[0] * side], out = [];
    for (let i = 0; i < n; i++) {
      const t = i / (n - 1); let r = ra + (rb - ra) * t; r *= 1 + bulge * Math.sin(Math.PI * t);
      out.push(add(lerp(a, b, t), nv, r));
    }
    return out;
  }

  function ik2(root, target, l1, l2, bend) {
    const dx = target[0] - root[0], dy = target[1] - root[1], d = Math.min(Math.hypot(dx, dy), l1 + l2 - 0.01);
    const a = Math.atan2(dy, dx);
    const c1 = Math.max(-1, Math.min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)));
    const ang = a - bend * Math.acos(c1);
    return [root[0] + l1 * Math.cos(ang), root[1] + l1 * Math.sin(ang)];
  }

  const mirror = (st, cx) => {
    if (cx == null) return st;
    const o = {}; for (const k in st) o[k] = st[k].map(p => [2 * cx - p[0], p[1]]); return o;
  };

  // ---------------------------------------------------------------- Tony
  const TL = { torso: 56, neck: 8, head: 11, up: 30, lo: 27, hand: 9, thigh: 43, shin: 41, foot: 15 };

  function tony(o) {
    const q = Object.assign({ x: 0, y: 0, s: 1, rot: 0, torso: 8, head: 0, an: -20, en: 80, af: 20, ef: 80,
      ln: 15, kn: 10, fn: 0, lf: -15, kf: 30, ff: 0, flip: false }, o);
    const s = q.s, L = {}; for (const k in TL) L[k] = TL[k] * s;
    const P = [0, 0], up = [Math.sin(R(q.torso)), -Math.cos(R(q.torso))], fwd = [-up[1], up[0]];
    const N = add(P, up, L.torso), S = add(P, up, L.torso - 6 * s);
    const hd = [Math.sin(R(q.torso + q.head)), -Math.cos(R(q.torso + q.head))];
    const H = add(N, hd, L.neck + L.head);
    const j = { P, N, S, H };
    for (const [sd, a, e] of [["n", q.an, q.en], ["f", q.af, q.ef]]) {
      const sh = add(S, fwd, (sd === "n" ? 2 : -2) * s), el = add(sh, dirv(a), L.up), ang = a + e, wr = add(el, dirv(ang), L.lo);
      j["sh" + sd] = sh; j["el" + sd] = el; j["wr" + sd] = wr; j["ht" + sd] = add(wr, dirv(ang + 8), L.hand);
    }
    for (const [sd, l, k, f] of [["n", q.ln, q.kn, q.fn], ["f", q.lf, q.kf, q.ff]]) {
      const hp = add(P, fwd, (sd === "n" ? 3 : -1) * s), kn = add(hp, dirv(l), L.thigh), sa = l - k, an = add(kn, dirv(sa), L.shin);
      j["hp" + sd] = hp; j["kn" + sd] = kn; j["an" + sd] = an; j["to" + sd] = add(an, dirv(sa + 90 + f), L.foot);
    }
    const W = {}; for (const k in j) { const r = rotp(j[k], [0, 0], q.rot); W[k] = [r[0] + q.x, r[1] + q.y]; }
    return { W, s, hdang: q.rot + q.torso + q.head, flip: q.flip ? q.x : null };
  }

  function tonyStrokes(pose) {
    const { W, s, hdang } = pose, out = {};
    const P = W.P, N = W.N, ax = norm(sub(N, P)), fw = [-ax[1], ax[0]];
    const side = (sg, prof) => prof.map((r, i) => add(lerp(P, N, i / (prof.length - 1)), fw, sg * r * s));
    out["t-torso-a"] = side(+1, [13, 12, 12.5, 15, 16, 13.5, 8]);
    out["t-torso-b"] = side(-1, [14, 12, 11, 12, 14, 12.5, 7]);
    out["t-hem"] = [add(lerp(P, N, .22), fw, 13 * s), add(lerp(P, N, .2), fw, 0), add(lerp(P, N, .22), fw, -14 * s)];
    const H = W.H, hu = [Math.sin(R(hdang)), -Math.cos(R(hdang))], hf = [-hu[1], hu[0]], Rh = 11 * s;
    const hp = (fx, fy) => [H[0] + hf[0] * fx * Rh + hu[0] * fy * Rh, H[1] + hf[1] * fx * Rh + hu[1] * fy * Rh];
    const head = [];
    for (let k = 0; k < 13; k++) { const a = R(200 - 140 * k / 12); head.push(hp(Math.cos(a) * .95, Math.sin(a) * 1.08)); }
    head.push(hp(.98, .2), hp(1.12, -.08), hp(.98, -.28), hp(.95, -.5), hp(.82, -.82), hp(.45, -1.0), hp(.1, -.9));
    out["t-head"] = head;
    out["t-hair"] = [hp(-.95, .2), hp(-.9, .75), hp(-.45, 1.2), hp(.2, 1.22), hp(.75, .95), hp(.95, .55)];
    out["t-ear"] = [hp(-.05, .2), hp(-.28, .25), hp(-.32, -.05), hp(-.12, -.2)];
    out["t-neck-a"] = [hp(.3, -.92), add(W.N, fw, 5 * s)];
    out["t-neck-b"] = [hp(-.6, -.75), add(W.N, fw, -5 * s)];
    const th = norm(sub(W.knn, W.hpn)), thp = perp(th);
    out["t-shorts"] = [add(lerp(W.hpn, W.knn, .42), thp, 12.5 * s), add(lerp(W.hpn, W.knn, .46), thp, -12.5 * s)];
    for (const sd of ["n", "f"]) {
      out[`t-arm-${sd}-up-a`] = contour(W["sh" + sd], W["el" + sd], 6.5 * s, 5 * s, 1);
      out[`t-arm-${sd}-up-b`] = contour(W["sh" + sd], W["el" + sd], 6.5 * s, 5 * s, -1);
      out[`t-arm-${sd}-lo-a`] = contour(W["el" + sd], W["wr" + sd], 5 * s, 3.8 * s, 1);
      out[`t-arm-${sd}-lo-b`] = contour(W["el" + sd], W["wr" + sd], 5 * s, 3.8 * s, -1);
      const wr = W["wr" + sd], ht = W["ht" + sd], d = norm(sub(ht, wr)), p = perp(d);
      out[`t-hand-${sd}`] = [add(wr, p, 3 * s), add(lerp(wr, ht, .6), p, 3.5 * s), add(ht, d, 1 * s), add(lerp(wr, ht, .6), p, -3 * s), add(wr, p, -2.5 * s)];
      out[`t-leg-${sd}-thigh-a`] = contour(W["hp" + sd], W["kn" + sd], 11.5 * s, 7.5 * s, 1);
      out[`t-leg-${sd}-thigh-b`] = contour(W["hp" + sd], W["kn" + sd], 11.5 * s, 7.5 * s, -1);
      out[`t-leg-${sd}-shin-a`] = contour(W["kn" + sd], W["an" + sd], 7.5 * s, 4.5 * s, 1, .18);
      out[`t-leg-${sd}-shin-b`] = contour(W["kn" + sd], W["an" + sd], 7.5 * s, 4.5 * s, -1, .18);
      const an = W["an" + sd], to = W["to" + sd], d2 = norm(sub(to, an)), p2 = perp(d2), heel = add(an, d2, -4 * s);
      out[`t-foot-${sd}`] = [add(heel, p2, 3 * s), add(heel, p2, -3.5 * s), add(to, p2, -3 * s), add(to, d2, 2 * s), add(lerp(an, to, .5), p2, 4.5 * s), add(an, p2, 4 * s)];
    }
    return mirror(out, pose.flip);
  }

  // ---------------------------------------------------------------- Juhu (German Shepherd)
  function juhu(o) {
    const q = Object.assign({ x: 0, y: 0, s: 1, rot: 0, spine: 0, neck: 35, head: 20, fa: 10, fb: -5, ffa: -10, ffb: 0,
      ba: -10, bk: 35, bh: 25, bfa: 10, bfk: 35, bfh: 25, ta: 40, tb: 25, mouth: 0, flip: false }, o);
    const L = v => v * q.s;
    const Hp = [0, 0], C = [L(66) * Math.cos(R(q.spine)), -L(66) * Math.sin(R(q.spine))];
    const sp = norm(sub(C, Hp)), top = [sp[1], -sp[0]];
    const wit = add(C, top, L(22)), crp = add(Hp, top, L(17));
    const nb = add(wit, [Math.cos(R(q.neck)), -Math.sin(R(q.neck))], L(26));
    const md = [Math.cos(R(q.head)), Math.sin(R(q.head))], nose = add(nb, md, L(32));
    const j = { Hp, C, wit, crp, nb, nose };
    for (const [sd, a, b] of [["n", q.fa, q.fb], ["f", q.ffa, q.ffb]]) {
      const r = add(C, top, -L(10)), el = add(r, dirv(a), L(22)), pw = add(el, dirv(a + b), L(24));
      j["fr" + sd] = r; j["fe" + sd] = el; j["fp" + sd] = pw;
    }
    for (const [sd, a, k, h] of [["n", q.ba, q.bk, q.bh], ["f", q.bfa, q.bfk, q.bfh]]) {
      const r = add(Hp, top, -L(2)), st = add(r, dirv(a), L(25)), hk = add(st, dirv(a - k), L(22)), pw = add(hk, dirv(a - k + h), L(16));
      j["br" + sd] = r; j["bs" + sd] = st; j["bh" + sd] = hk; j["bp" + sd] = pw;
    }
    const back = [-sp[0], -sp[1]];
    j.t1 = add(crp, rotp(back, [0, 0], -q.ta), L(20)); j.t2 = add(j.t1, rotp(back, [0, 0], -q.tb), L(22));
    const W = {}; for (const k in j) { const r = rotp(j[k], [0, 0], q.rot); W[k] = [r[0] + q.x, r[1] + q.y]; }
    return { W, s: q.s, mouth: q.mouth, flip: q.flip ? q.x : null };
  }

  function juhuStrokes(pose) {
    const { W, s, mouth } = pose, L = v => v * s, out = {};
    const { C, Hp, wit, crp, nb, nose } = W;
    const sp = norm(sub(C, Hp)), top = [sp[1], -sp[0]];
    const md = norm(sub(nose, nb)), mu = md[0] >= 0 ? [md[1], -md[0]] : [-md[1], md[0]];
    const skull = add(nb, md, L(6));
    out["j-back"] = [add(nb, mu, L(5)), lerp(wit, nb, .45), wit, add(lerp(wit, crp, .5), top, -L(2)), crp, add(crp, sp, -L(6))];
    const cf = add(add(C, sp, L(12)), top, -L(4));
    out["j-chest"] = [add(nb, mu, -L(6)), lerp(add(nb, mu, -L(6)), cf, .5), cf, add(add(C, sp, L(4)), top, -L(22)), add(C, top, -L(24))];
    out["j-belly"] = [add(C, top, -L(24)), add(lerp(C, Hp, .4), top, -L(19)), add(lerp(C, Hp, .75), top, -L(9)), add(add(Hp, sp, L(8)), top, -L(5))];
    const stop = add(skull, mu, L(9));
    out["j-head"] = [add(nb, mu, L(4)), add(skull, mu, L(10)), stop, add(lerp(stop, nose, .5), mu, L(3)), add(nose, mu, L(2)), add(nose, md, L(2))];
    out["j-jaw"] = [add(nose, mu, -L(1)), add(lerp(skull, nose, .9), mu, -L(4 + mouth * 8)), add(lerp(skull, nose, .35), mu, -L(7)), add(nb, mu, -L(6))];
    for (const [sd, off] of [["n", 0], ["f", -L(5)]]) {
      const b = add(add(skull, md, -L(4) + off), mu, L(8)), tip = add(add(b, mu, L(17)), md, -L(5)), b2 = add(b, md, L(8));
      out[`j-ear-${sd}`] = [b, tip, b2];
      out[`j-fl-${sd}-a`] = contour(W["fr" + sd], W["fe" + sd], L(7), L(4.5), 1).concat(contour(W["fe" + sd], W["fp" + sd], L(4.5), L(3.2), 1).slice(1));
      out[`j-fl-${sd}-b`] = contour(W["fr" + sd], W["fe" + sd], L(7), L(4.5), -1).concat(contour(W["fe" + sd], W["fp" + sd], L(4.5), L(3.2), -1).slice(1));
      let p = W["fp" + sd], d = norm(sub(W["fp" + sd], W["fe" + sd])), f = perp(d);
      out[`j-fl-${sd}-paw`] = [add(p, f, L(3.5)), add(add(p, d, L(3)), f, L(6)), add(p, d, L(4)), add(p, f, -L(3))];
      out[`j-bl-${sd}-a`] = contour(W["br" + sd], W["bs" + sd], L(11), L(6), 1).concat(contour(W["bs" + sd], W["bh" + sd], L(6), L(3.5), 1).slice(1), contour(W["bh" + sd], W["bp" + sd], L(3.5), L(3), 1).slice(1));
      out[`j-bl-${sd}-b`] = contour(W["br" + sd], W["bs" + sd], L(11), L(6), -1).concat(contour(W["bs" + sd], W["bh" + sd], L(6), L(3.5), -1).slice(1), contour(W["bh" + sd], W["bp" + sd], L(3.5), L(3), -1).slice(1));
      p = W["bp" + sd]; d = norm(sub(W["bp" + sd], W["bh" + sd])); f = perp(d);
      out[`j-bl-${sd}-paw`] = [add(p, f, L(3.5)), add(add(p, d, L(3)), f, L(6)), add(p, d, L(4)), add(p, f, -L(3))];
    }
    out["j-tail-a"] = contour(crp, W.t1, L(4), L(6), 1, .3).concat(contour(W.t1, W.t2, L(6), L(1.5), 1, .2).slice(1));
    out["j-tail-b"] = contour(crp, W.t1, L(4), L(6), -1, .3).concat(contour(W.t1, W.t2, L(6), L(1.5), -1, .2).slice(1));
    return mirror(out, pose.flip);
  }

  // Drop a pose so its lowest foot or paw touches the ground line.
  function grounded(make, strokesOf, footNames, o, ground) {
    const st = strokesOf(make(Object.assign({}, o, { y: 0 })));
    let low = -1e9; for (const n of footNames(st)) for (const p of st[n]) low = Math.max(low, p[1]);
    return Object.assign({}, o, { y: ground - low });
  }
  const tonyFeet = () => ["t-foot-n", "t-foot-f"];
  const juhuPaws = st => Object.keys(st).filter(n => n.endsWith("paw"));

  return { tony, tonyStrokes, juhu, juhuStrokes, grounded, tonyFeet, juhuPaws, lerp, dist };
})();
