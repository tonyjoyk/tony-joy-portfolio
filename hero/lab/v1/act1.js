// Act 1 dope sheet: jog, Juhu leaps in from behind, the push, the dive into the water.
// Frames at 24 fps. Poses are blended joint by joint (pose space), never point by point.
const Act1 = (function () {
  const G = 430, LEN = 64;                                   // ground line; slice length in frames (loops for review)

  // ---- smooth curve through keys (Catmull-Rom on each channel), with an optional per-channel delay
  function channel(keys, name, f) {
    const ks = keys.filter(k => k.pose[name] !== undefined);
    if (!ks.length) return undefined;
    if (f <= ks[0].f) return ks[0].pose[name];
    if (f >= ks[ks.length - 1].f) return ks[ks.length - 1].pose[name];
    let i = 0; while (ks[i + 1].f < f) i++;
    const p0 = ks[Math.max(0, i - 1)], p1 = ks[i], p2 = ks[i + 1], p3 = ks[Math.min(ks.length - 1, i + 2)];
    const t = (f - p1.f) / (p2.f - p1.f);
    const v0 = p0.pose[name], v1 = p1.pose[name], v2 = p2.pose[name], v3 = p3.pose[name];
    const m1 = (v2 - v0) / Math.max(1, (p2.f - p0.f)) * (p2.f - p1.f) * 0.5;   // tangents scaled to the segment
    const m2 = (v3 - v1) / Math.max(1, (p3.f - p1.f)) * (p2.f - p1.f) * 0.5;
    const t2 = t * t, t3 = t2 * t;
    return (2 * t3 - 3 * t2 + 1) * v1 + (t3 - 2 * t2 + t) * m1 + (-2 * t3 + 3 * t2) * v2 + (t3 - t2) * m2;
  }
  function sample(keys, f, delays) {
    const out = {}, names = new Set(); keys.forEach(k => Object.keys(k.pose).forEach(n => names.add(n)));
    for (const n of names) {
      const v = channel(keys, n, f - (delays[n] || 0));
      if (typeof v === "number") out[n] = v;
    }
    return out;
  }

  // ---- Tony: a generated jog, then keyed acting
  function jog(f) {
    const ph = f / 16 * Math.PI * 2, s = Math.sin(ph);
    return { x: 214 + f * 1.8, torso: 13, head: -8, rot: 0,
      ln: 30 * s, lf: -30 * s,
      kn: 14 + 62 * Math.max(0, -Math.sin(ph + 0.55)), kf: 14 + 62 * Math.max(0, Math.sin(ph + 0.55)),
      fn: -10 * Math.max(0, -s), ff: -10 * Math.max(0, s),
      an: -36 * s, en: 92 + 10 * s, af: 36 * s, ef: 92 - 10 * s };
  }
  const groundTony = o => Rig.grounded(Rig.tony, Rig.tonyStrokes, Rig.tonyFeet, o, G);
  const TONY_KEYS = [
    { f: 20, pose: groundTony(jog(20)) },
    { f: 25, pose: groundTony({ x: 258, rot: 0, torso: 30, head: -18, an: -78, en: 28, af: -52, ef: 40, ln: 24, kn: 26, fn: 0, lf: -36, kf: 30, ff: 0 }) },
    { f: 29, pose: Object.assign(groundTony({ x: 278, rot: 22, torso: 18, head: -14, an: 40, en: 40, af: 25, ef: 50, ln: -20, kn: 12, fn: 0, lf: -38, kf: 22, ff: 0 }), {}) },
    { f: 35, pose: { x: 340, y: 300, rot: 68, torso: 6, head: -10, an: 165, en: 8, af: 155, ef: 10, ln: -10, kn: 12, fn: 0, lf: -24, kf: 22, ff: 0 } },
    { f: 41, pose: { x: 392, y: 334, rot: 110, torso: 0, head: -6, an: 178, en: 0, af: 176, ef: 2, ln: -4, kn: 3, fn: 0, lf: 4, kf: 3, ff: 0 } },
    { f: 47, pose: { x: 424, y: 372, rot: 150, torso: 0, head: 0, an: 178, en: 0, af: 176, ef: 2, ln: -3, kn: 3, fn: 0, lf: 3, kf: 3, ff: 0 } },
    { f: 54, pose: { x: 446, y: 446, rot: 166, torso: 0, head: 0, an: 178, en: 0, af: 176, ef: 2, ln: 6, kn: 8, fn: 0, lf: -6, kf: 10, ff: 0 } },
  ];
  // overlap: arms trail the body by 2 frames, legs by 1, head by 1
  const TONY_DELAY = { an: 2, en: 2.5, af: 2, ef: 2.5, ln: 1, kn: 1.5, lf: 1, kf: 1.5, head: 1 };

  function tonyPose(f) {
    if (f <= 20) return groundTony(jog(f));
    return sample(TONY_KEYS, f, TONY_DELAY);
  }

  // ---- Juhu: the gallop leap (gather, stretch, reach), the landing, then standing with a wagging tail
  const GATHER = { spine: -8, neck: 25, head: 15, fa: 25, fb: -70, ffa: 15, ffb: -60, ba: 45, bk: 80, bh: 60, bfa: 35, bfk: 75, bfh: 55, ta: -5, tb: -20, mouth: .3 };
  const STRETCH = { spine: 10, neck: 15, head: 10, fa: 82, fb: -10, ffa: 70, ffb: -20, ba: -75, bk: 5, bh: 10, bfa: -60, bfk: 10, bfh: 15, ta: -10, tb: -15, mouth: .3 };
  const groundJuhu = o => Rig.grounded(Rig.juhu, Rig.juhuStrokes, Rig.juhuPaws, o, G);
  const STAND = { spine: 2, neck: 38, head: 22, fa: 4, fb: -2, ffa: -6, ffb: 0, ba: -8, bk: 32, bh: 28, bfa: 8, bfk: 36, bfh: 26, ta: 45, tb: 30, mouth: .2 };
  const JUHU_KEYS = [
    { f: 0, pose: Object.assign({ x: -230, y: 330, rot: 0 }, GATHER) },
    { f: 6, pose: Object.assign({ x: -150, y: 336, rot: 4 }, GATHER) },
    { f: 11, pose: Object.assign({ x: -40, y: 300, rot: -4 }, STRETCH) },
    { f: 16, pose: Object.assign({ x: 72, y: 290, rot: 0 }, STRETCH, { fa: 96, fb: -26, ffa: 86, ffb: -36, ba: -62, bk: 14, ta: -16 }) },
    { f: 21, pose: { x: 150, y: 322, rot: -18, spine: 8, neck: 20, head: 12, fa: 106, fb: -30, ffa: 96, ffb: -40, ba: -30, bk: 24, bh: 26, bfa: -16, bfk: 30, bfh: 26, ta: -12, tb: -20, mouth: .4 } },
    { f: 25, pose: { x: 176, y: 380, rot: -40, spine: 8, neck: 20, head: 10, fa: 100, fb: -20, ffa: 90, ffb: -30, ba: -20, bk: 20, bh: 30, bfa: -5, bfk: 30, bfh: 30, ta: -10, tb: -20, mouth: .4 } },
    { f: 31, pose: groundJuhu(Object.assign({ x: 150, rot: 0 }, { spine: -6, neck: 26, head: 26, fa: 30, fb: -20, ffa: 18, ffb: -15, ba: 15, bk: 75, bh: 55, bfa: 25, bfk: 80, bfh: 55, ta: 0, tb: -20, mouth: .5 })) },
    { f: 38, pose: groundJuhu(Object.assign({ x: 150, rot: 0 }, STAND)) },
  ];
  const JUHU_DELAY = { ta: 2, tb: 3.5, neck: 1, head: 1.5, fa: 1, fb: 1.5, ffa: 1, ffb: 1.5 };

  function juhuPose(f) {
    const q = sample(JUHU_KEYS, f, JUHU_DELAY);
    if (f > 36) { q.ta += 16 * Math.sin((f - 36) * 0.85); q.tb += 22 * Math.sin((f - 36) * 0.85 - 0.9); }   // happy tail
    return q;
  }

  // ---- the ground line softens into water as Tony dives
  function world(f) {
    const k = Math.min(1, Math.max(0, (f - 28) / 16)), e = k * k * (3 - 2 * k);
    const amp = 6 * e, y = G, pts = [];                         // water stays level with the bank Juhu stands on
    for (let i = 0; i <= 60; i++) { const x = 40 + 520 * i / 60; pts.push([x, y + amp * Math.sin(1.2 + i / 60 * Math.PI * 2 * 3 + f * 0.12 * e)]); }
    const out = { "w-ground": pts, _water: e > 0.5 };
    if (f >= 45) {                                                // splash: two small arcs, drawn on then fading
      const t = Math.min(1, (f - 45) / 6), fade = Math.max(0, 1 - (f - 52) / 8);
      const arc = (cx, cy, r, a0, a1) => { const p = []; for (let i = 0; i <= 12; i++) { const a = (a0 + (a1 - a0) * t * i / 12) * Math.PI / 180; p.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return p; };
      if (fade > 0) { out["w-splash-1"] = arc(430, 422, 18, 200, 330); out["w-splash-2"] = arc(452, 418, 10, 210, 330); out._fade = fade; }
    }
    return out;
  }

  return { LEN, G, tonyPose, juhuPose, world, cuts: { juhu: [0] } };
})();
