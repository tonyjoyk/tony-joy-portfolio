// Hero animation, interim version (from hero/lab/v1, the pose-space engine built from plan v2).
// rig.js and act1.js are copied unchanged from the hero session's branch (claude/vigilant-gates-9233e6).
// This player is the lab's engine.js without the review controls. It fills #hero-animation,
// pauses when the slot is off screen, and shows one still drawing for reduced motion.
// Replace this folder when the v3 animation is ready.
(function () {
  var slot = document.getElementById("hero-animation");
  if (!slot || typeof p5 === "undefined" || typeof Act1 === "undefined" || typeof Rig === "undefined") return;

  var INK = [164, 85, 58], BG = [247, 245, 239], FPS = 24, SIZE = 600;   // laterite on the page background
  var STILL_FRAME = 12;                                                   // jog with Juhu leaping in
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var frame = reduce ? STILL_FRAME : 0, acc = 0, grain;

  // Chaikin smoothing, then resample to roughly even spacing
  function smooth(pts, it) {
    var p = pts;
    for (var k = 0; k < (it || 2); k++) {
      var o = [p[0]];
      for (var i = 0; i < p.length - 1; i++) {
        var a = p[i], b = p[i + 1];
        o.push([a[0] * .75 + b[0] * .25, a[1] * .75 + b[1] * .25], [a[0] * .25 + b[0] * .75, a[1] * .25 + b[1] * .75]);
      }
      o.push(p[p.length - 1]); p = o;
    }
    return p;
  }
  function resample(pts, step) {
    var out = [pts[0]], carry = 0;
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1], d = Math.hypot(b[0] - a[0], b[1] - a[1]), t = step - carry;
      while (t <= d) { out.push([a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d]); t += step; }
      carry = (carry + d) % step;
    }
    out.push(pts[pts.length - 1]); return out;
  }

  // Pressure ribbon: thin at the ends, fuller in the middle, with a wobble that boils on every drawing.
  function ribbon(p, pts, seed, drawing, weight, alpha) {
    var sm = resample(smooth(pts), 2.5); if (sm.length < 3) return;
    var n = sm.length, left = [], right = [];
    var press = 0.75 + 0.5 * p.noise(seed * 0.13, drawing * 0.21);
    for (var i = 0; i < n; i++) {
      var a = sm[Math.max(0, i - 1)], b = sm[Math.min(n - 1, i + 1)];
      var tx = b[0] - a[0], ty = b[1] - a[1], l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
      var nx = -ty, ny = tx, t = i / (n - 1);
      var profile = 0.25 + 0.75 * Math.pow(Math.sin(Math.PI * Math.min(1, t * 1.08)), 0.55);
      var w = weight * press * profile * (0.8 + 0.4 * p.noise(seed + i * 0.09, drawing * 0.3));
      var wob = (p.noise(seed * 0.7 + i * 0.045, drawing * 0.5) - 0.5) * 2.4;
      var cx = sm[i][0] + nx * wob, cy = sm[i][1] + ny * wob;
      left.push([cx + nx * w / 2, cy + ny * w / 2]); right.push([cx - nx * w / 2, cy - ny * w / 2]);
    }
    p.fill(INK[0], INK[1], INK[2], 255 * alpha); p.noStroke(); p.beginShape();
    for (var j = 0; j < left.length; j++) p.vertex(left[j][0], left[j][1]);
    for (var k = right.length - 1; k >= 0; k--) p.vertex(right[k][0], right[k][1]);
    p.endShape(p.CLOSE);
  }

  // A loose graphite scribble inside Tony's head.
  function headScribble(p, pose, seed, drawing) {
    var H = pose.W.H, r = 9.5 * pose.s; p.randomSeed(seed + drawing);
    p.noFill(); p.stroke(INK[0], INK[1], INK[2], 120); p.strokeWeight(1.1);
    p.beginShape();
    for (var i = 0; i < 26; i++) {
      var a = i * 2.35 + p.random(-.3, .3), rr = r * (0.25 + 0.7 * ((i * 37) % 10) / 10);
      p.curveVertex(H[0] + Math.cos(a) * rr, H[1] + Math.sin(a) * rr * 1.05);
    }
    p.endShape();
  }

  function strokes(p, set, base, drawing) {
    var i = 0;
    for (var n in set) {
      var far = n.indexOf("-f-") !== -1 || n.slice(-2) === "-f";
      ribbon(p, set[n], base + i++, drawing, far ? 1.5 : 2.1, far ? .45 : .9);
    }
  }

  function drawScene(p, f) {
    var drawing = Math.floor(f / 2), fq = drawing * 2;      // characters on twos
    var w = Act1.world(f);
    ribbon(p, w["w-ground"], 11, drawing, 2.2, 0.85);
    if (w["w-splash-1"]) { ribbon(p, w["w-splash-1"], 21, drawing, 1.8, 0.8 * w._fade); ribbon(p, w["w-splash-2"], 22, drawing, 1.5, 0.8 * w._fade); }
    strokes(p, Rig.juhuStrokes(Rig.juhu(Act1.juhuPose(fq))), 100, drawing);
    var tp = Rig.tony(Act1.tonyPose(fq)), ctx = p.drawingContext;
    if (w._water) {                                          // under the surface, clip Tony to the air above the wave
      ctx.save(); ctx.beginPath(); ctx.moveTo(0, 0);
      for (var q = 0; q < w["w-ground"].length; q++) ctx.lineTo(w["w-ground"][q][0], w["w-ground"][q][1] - 1);
      ctx.lineTo(SIZE, w["w-ground"][w["w-ground"].length - 1][1]); ctx.lineTo(SIZE, 0); ctx.closePath();
      ctx.rect(0, 0, 40, SIZE); ctx.clip();
    }
    strokes(p, Rig.tonyStrokes(tp), 300, drawing);
    headScribble(p, tp, 7, drawing);
    if (w._water) ctx.restore();
  }

  new p5(function (p) {
    p.setup = function () {
      p.createCanvas(SIZE, SIZE).parent(slot);
      p.pixelDensity(Math.min(2, window.devicePixelRatio || 1));
      p.frameRate(60); p.noiseDetail(3, 0.45);
      grain = p.createGraphics(SIZE, SIZE); grain.pixelDensity(1); grain.noStroke();   // paper tooth over the lines
      for (var k = 0; k < 14000; k++) { grain.fill(BG[0], BG[1], BG[2], p.random(50, 120)); grain.rect(p.random(SIZE), p.random(SIZE), 1, 1); }
      slot.classList.add("is-live");
      if (reduce) p.noLoop();
      else if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (entries) {
          entries[0].isIntersecting ? p.loop() : p.noLoop();
        }).observe(slot);
      }
    };
    p.draw = function () {
      if (!reduce) { acc += Math.min(p.deltaTime, 100) / 1000 * FPS; while (acc >= 1) { frame = (frame + 1) % Act1.LEN; acc -= 1; } }
      p.background(BG[0], BG[1], BG[2]);
      drawScene(p, frame);
      p.image(grain, 0, 0);
    };
  });
})();
