// Engine v1: poses -> strokes -> pencil.
// Characters are drawn on twos (12 drawings a second); the world moves on every frame (24).
// Each stroke is a pressure ribbon: thin at the ends, fuller in the middle, with a smooth wobble that
// changes on every drawing (line boil). A paper-tooth texture breaks the line like graphite.
(function () {
  const INK = [164, 85, 58], BG = [246, 241, 232], FPS = 24;
  let frame = 0, playing = true, speed = 1, acc = 0, onion = false, grain;
  const qf = new URLSearchParams(location.search).get("f");               // ?f=52 opens paused on that frame
  if (qf !== null) { frame = +qf; playing = false; }

  // Chaikin smoothing, then resample to roughly even spacing
  function smooth(pts, it = 2) {
    let p = pts;
    for (let k = 0; k < it; k++) {
      const o = [p[0]];
      for (let i = 0; i < p.length - 1; i++) {
        const a = p[i], b = p[i + 1];
        o.push([a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25], [a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75]);
      }
      o.push(p[p.length - 1]); p = o;
    }
    return p;
  }
  function resample(pts, step) {
    const out = [pts[0]]; let carry = 0;
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1], d = Math.hypot(b[0] - a[0], b[1] - a[1]); let t = step - carry;
      while (t <= d) { out.push([a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d]); t += step; }
      carry = (carry + d) % step;
    }
    out.push(pts[pts.length - 1]); return out;
  }

  function ribbon(p, pts, seed, drawing, weight, alpha) {
    const sm = resample(smooth(pts), 2.5); if (sm.length < 3) return;
    const n = sm.length, left = [], right = [];
    const press = 0.75 + 0.5 * p.noise(seed * 0.13, drawing * 0.21);          // pressure varies per drawing
    for (let i = 0; i < n; i++) {
      const a = sm[Math.max(0, i - 1)], b = sm[Math.min(n - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1]; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
      const nx = -ty, ny = tx, t = i / (n - 1);
      const profile = 0.25 + 0.75 * Math.pow(Math.sin(Math.PI * Math.min(1, t * 1.08)), 0.55);   // thin start, light flick at the end
      const w = weight * press * profile * (0.8 + 0.4 * p.noise(seed + i * 0.09, drawing * 0.3));
      const wob = (p.noise(seed * 0.7 + i * 0.045, drawing * 0.5) - 0.5) * 2.4;                   // coherent wobble, boils each drawing
      const cx = sm[i][0] + nx * wob, cy = sm[i][1] + ny * wob;
      left.push([cx + nx * w / 2, cy + ny * w / 2]); right.push([cx - nx * w / 2, cy - ny * w / 2]);
    }
    p.fill(...INK, 255 * alpha); p.noStroke(); p.beginShape();
    for (const q of left) p.vertex(q[0], q[1]);
    for (let i = right.length - 1; i >= 0; i--) p.vertex(right[i][0], right[i][1]);
    p.endShape(p.CLOSE);
  }

  function headScribble(p, pose, seed, drawing) {
    // a loose graphite scribble inside Tony's head: the pencil version of a solid head
    const H = pose.W.H, r = 9.5 * pose.s; p.randomSeed(seed + drawing);
    p.noFill(); p.stroke(...INK, 120); p.strokeWeight(1.1);
    p.beginShape();
    for (let i = 0; i < 26; i++) {
      const a = i * 2.35 + p.random(-.3, .3), rr = r * (0.25 + 0.7 * ((i * 37) % 10) / 10);
      p.curveVertex(H[0] + Math.cos(a) * rr, H[1] + Math.sin(a) * rr * 1.05);
    }
    p.endShape();
  }

  function drawScene(p, f, ghost) {
    const drawing = Math.floor(f / 2);                       // characters on twos
    const fq = drawing * 2;
    const mult = ghost ? 0.18 : 1;
    // world
    const w = Act1.world(f);
    ribbon(p, w["w-ground"], 11, Math.floor(f / 2), 2.2, 0.85 * mult);
    if (w["w-splash-1"]) { ribbon(p, w["w-splash-1"], 21, drawing, 1.8, 0.8 * w._fade * mult); ribbon(p, w["w-splash-2"], 22, drawing, 1.5, 0.8 * w._fade * mult); }
    // Juhu, then Tony (Tony in front)
    const jp = Rig.juhu(Act1.juhuPose(fq)), js = Rig.juhuStrokes(jp);
    let i = 0; for (const n in js) { const far = n.includes("-f-") || n.endsWith("-f"); ribbon(p, js[n], 100 + i++, drawing, far ? 1.5 : 2.1, (far ? .45 : .9) * mult); }
    const tp = Rig.tony(Act1.tonyPose(fq)), ts = Rig.tonyStrokes(tp);
    if (w._water) {                                          // under the surface Tony is hidden: clip him to the air above the wave
      p.drawingContext.save(); p.drawingContext.beginPath(); p.drawingContext.moveTo(0, 0);
      for (const q of w["w-ground"]) p.drawingContext.lineTo(q[0], q[1] - 1);
      p.drawingContext.lineTo(600, w["w-ground"][w["w-ground"].length - 1][1]); p.drawingContext.lineTo(600, 0); p.drawingContext.closePath();
      p.drawingContext.rect(0, 0, 40, 600); p.drawingContext.clip();
    }
    i = 0; for (const n in ts) { const far = n.includes("-f-") || n.endsWith("-f"); ribbon(p, ts[n], 300 + i++, drawing, far ? 1.5 : 2.1, (far ? .45 : .9) * mult); }
    if (!ghost) headScribble(p, tp, 7, drawing);
    if (w._water) p.drawingContext.restore();
  }

  new p5(function (p) {
    p.setup = function () {
      p.createCanvas(600, 600).parent("stage");
      p.pixelDensity(Math.min(2, window.devicePixelRatio || 1));
      p.frameRate(60); p.noiseDetail(3, 0.45);
      grain = p.createGraphics(600, 600); grain.pixelDensity(1); grain.noStroke();          // paper tooth: specks of paper colour over the lines
      for (let k = 0; k < 14000; k++) { grain.fill(...BG, p.random(50, 120)); grain.rect(p.random(600), p.random(600), 1, 1); }
    };
    p.draw = function () {
      if (playing) { acc += p.deltaTime / 1000 * FPS * speed; while (acc >= 1) { frame = (frame + 1) % Act1.LEN; acc -= 1; } }
      p.background(...BG);
      if (onion) { drawScene(p, (frame + Act1.LEN - 4) % Act1.LEN, true); drawScene(p, (frame + 4) % Act1.LEN, true); }
      drawScene(p, frame, false);
      p.image(grain, 0, 0);
      document.getElementById("scrub").value = frame;
      document.getElementById("readout").textContent = `frame ${frame} · ${(frame / FPS).toFixed(2)} s`;
    };
  });

  const playBtn = document.getElementById("play");
  const stop = () => { playing = false; playBtn.textContent = "Play"; };
  playBtn.onclick = () => { playing = !playing; playBtn.textContent = playing ? "Pause" : "Play"; };
  document.getElementById("back").onclick = () => { stop(); frame = (frame + Act1.LEN - 1) % Act1.LEN; };
  document.getElementById("fwd").onclick = () => { stop(); frame = (frame + 1) % Act1.LEN; };
  document.getElementById("speed").oninput = e => { speed = +e.target.value; };
  document.getElementById("onion").onchange = e => { onion = e.target.checked; };
  const scrub = document.getElementById("scrub"); scrub.max = Act1.LEN - 1;
  scrub.oninput = e => { stop(); frame = +e.target.value; };
  window.__lab = { setFrame: f => { stop(); frame = f; } };
})();
