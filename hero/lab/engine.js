// Hero animation engine v0: blends the key frames in hero/keyframes/timeline.json.
// Points are blended directly (point space). Characters and gear step on twos (12 drawings a second);
// world lines and props move on every frame (24). The pencil line is redrawn with fresh jitter each drawing.
(function () {
  const INK = [164, 85, 58];
  const BG = [246, 241, 232];
  let data = null, kf = [], strokes = [], groups = {}, far = {};
  let frame = 0, playing = true, speed = 1, keysOnly = false, acc = 0;

  const ease = t => t * t * (3 - 2 * t);                           // slow in, slow out

  function segment(f, group) {
    // last key at or before f, and the next one (wrapping round the loop)
    let i = kf.length - 1;
    for (let k = 0; k < kf.length; k++) if (kf[k].frame <= f) i = k;
    const a = kf[i], b = kf[(i + 1) % kf.length];
    const span = ((b.frame - a.frame) + data.loop) % data.loop || data.loop;
    let t = ((f - a.frame) + data.loop) % data.loop / span;
    if (b.cut.includes(group)) t = 0;                             // this group jumps at b: hold a until then
    return [a, b, keysOnly ? 0 : ease(t)];
  }

  function pointsAt(name, f) {
    const g = groups[name];
    const fq = (g === "tony" || g === "juhu" || g === "gear") ? Math.floor(f / 2) * 2 : f;
    const [a, b, t] = segment(fq, g);
    const pa = a.strokes[name], pb = b.strokes[name];
    return pa.map((p, i) => [p[0] + (pb[i][0] - p[0]) * t, p[1] + (pb[i][1] - p[1]) * t]);
  }

  function spread(pts) {
    let m = 0;
    for (const p of pts) m = Math.max(m, Math.abs(p[0] - pts[0][0]) + Math.abs(p[1] - pts[0][1]));
    return m;
  }

  new p5(function (p) {
    p.setup = function () {
      const c = p.createCanvas(600, 600); c.parent("stage");
      p.pixelDensity(Math.min(2, window.devicePixelRatio || 1));
      p.noFill(); p.strokeCap(p.ROUND); p.strokeJoin(p.ROUND); p.frameRate(60);
      fetch("../keyframes/timeline.json").then(r => r.json()).then(d => {
        data = d; kf = d.keyframes; strokes = d.strokes; groups = d.groups;
        for (const n of strokes) far[n] = n.includes("-f-") || n.endsWith("-f");
      });
    };

    p.draw = function () {
      p.background(...BG);
      if (!data) return;
      if (playing) { acc += p.deltaTime / 1000 * 24 * speed; while (acc >= 1) { frame = (frame + 1) % data.loop; acc -= 1; } }
      document.getElementById("scrub").value = frame;
      const [a] = segment(frame, "world");
      document.getElementById("readout").textContent = `frame ${frame} · ${(frame / 24).toFixed(2)} s · after ${a.label}`;
      const drawing = Math.floor(frame / 2);                      // new pencil jitter for every drawing
      for (const name of strokes) {
        const pts = pointsAt(name, frame);
        if (spread(pts) < 1.5) continue;                          // shrunk to a point: hidden
        const seed = (drawing * 131 + name.length * 17 + name.charCodeAt(2) * 7) % 9973;
        p.randomSeed(seed);
        for (let pass = 0; pass < 2; pass++) {
          const jx = p.random(-0.8, 0.8), jy = p.random(-0.8, 0.8);
          p.stroke(...INK, 255 * p.random(0.6, 0.9) * (far[name] ? 0.5 : 1));
          p.strokeWeight(1.5 * p.random(0.8, 1.15));
          p.beginShape();
          for (const q of pts) p.vertex(q[0] + jx + p.random(-0.4, 0.4), q[1] + jy + p.random(-0.4, 0.4));
          p.endShape();
        }
      }
    };
  });

  document.getElementById("play").onclick = e => { playing = !playing; e.target.textContent = playing ? "Pause" : "Play"; };
  document.getElementById("back").onclick = () => { playing = false; document.getElementById("play").textContent = "Play"; frame = (frame + 239) % 240; };
  document.getElementById("fwd").onclick = () => { playing = false; document.getElementById("play").textContent = "Play"; frame = (frame + 1) % 240; };
  document.getElementById("speed").oninput = e => { speed = +e.target.value; };
  document.getElementById("keys").onchange = e => { keysOnly = e.target.checked; };
  document.getElementById("scrub").oninput = e => { playing = false; document.getElementById("play").textContent = "Play"; frame = +e.target.value; };
})();
