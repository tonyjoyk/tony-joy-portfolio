// Hero animation, interim version: the full storyboard (all 29 key frames, about 10 s).
// Port of hero/lab/engine.js (engine v0) from the hero session's branch (claude/vigilant-gates-9233e6),
// without the review controls. timeline.json is hero/keyframes/timeline.json with points rounded to whole pixels.
// Fills #hero-animation, pauses when the slot is off screen, and shows one still drawing for reduced motion.
// Replace this folder when the v3 animation is ready.
(function () {
  var slot = document.getElementById("hero-animation");
  if (!slot || typeof p5 === "undefined") return;

  var INK = [164, 85, 58], BG = [247, 245, 239];     // laterite on the page background
  var STILL_FRAME = 212;                               // Tony and Juhu on the beach, for reduced motion
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var data = null, kf = [], strokes = [], groups = {}, far = {};
  var frame = 0, acc = 0;

  function ease(t) { return t * t * (3 - 2 * t); }    // slow in, slow out

  // The last key at or before f, the next one (wrapping round the loop) and how far between them.
  function segment(f, group) {
    var i = kf.length - 1;
    for (var k = 0; k < kf.length; k++) if (kf[k].frame <= f) i = k;
    var a = kf[i], b = kf[(i + 1) % kf.length];
    var span = ((b.frame - a.frame) + data.loop) % data.loop || data.loop;
    var t = ((f - a.frame) + data.loop) % data.loop / span;
    if (b.cut.indexOf(group) !== -1) t = 0;           // this group jumps at b: hold a until then
    return [a, b, ease(t)];
  }

  function pointsAt(name, f) {
    var g = groups[name];
    var fq = (g === "tony" || g === "juhu" || g === "gear") ? Math.floor(f / 2) * 2 : f;   // characters on twos
    var s = segment(fq, g), pa = s[0].strokes[name], pb = s[1].strokes[name], t = s[2];
    return pa.map(function (p, i) { return [p[0] + (pb[i][0] - p[0]) * t, p[1] + (pb[i][1] - p[1]) * t]; });
  }

  function spread(pts) {
    var m = 0;
    for (var i = 0; i < pts.length; i++) m = Math.max(m, Math.abs(pts[i][0] - pts[0][0]) + Math.abs(pts[i][1] - pts[0][1]));
    return m;
  }

  new p5(function (p) {
    p.setup = function () {
      p.createCanvas(600, 600).parent(slot);
      p.pixelDensity(Math.min(2, window.devicePixelRatio || 1));
      p.noFill(); p.strokeCap(p.ROUND); p.strokeJoin(p.ROUND); p.frameRate(60);
      p.noLoop();
      fetch("hero-v1/timeline.json").then(function (r) { return r.json(); }).then(function (d) {
        data = d; kf = d.keyframes; strokes = d.strokes; groups = d.groups;
        strokes.forEach(function (n) { far[n] = n.indexOf("-f-") !== -1 || n.slice(-2) === "-f"; });
        slot.classList.add("is-live");
        if (reduce) { frame = STILL_FRAME; p.redraw(); return; }
        p.loop();
        if ("IntersectionObserver" in window) {
          new IntersectionObserver(function (entries) {
            entries[0].isIntersecting ? p.loop() : p.noLoop();
          }).observe(slot);
        }
      }).catch(function () { /* keep the still drawing */ });
    };

    p.draw = function () {
      if (!data) return;
      if (!reduce) { acc += Math.min(p.deltaTime, 100) / 1000 * data.fps; while (acc >= 1) { frame = (frame + 1) % data.loop; acc -= 1; } }
      p.background(BG[0], BG[1], BG[2]);
      var drawing = Math.floor(frame / 2);              // fresh pencil jitter for every drawing
      for (var s = 0; s < strokes.length; s++) {
        var name = strokes[s], pts = pointsAt(name, frame);
        if (spread(pts) < 1.5) continue;                // shrunk to a point: hidden
        p.randomSeed((drawing * 131 + name.length * 17 + name.charCodeAt(2) * 7) % 9973);
        for (var pass = 0; pass < 2; pass++) {
          var jx = p.random(-0.8, 0.8), jy = p.random(-0.8, 0.8);
          p.stroke(INK[0], INK[1], INK[2], 255 * p.random(0.6, 0.9) * (far[name] ? 0.5 : 1));
          p.strokeWeight(1.5 * p.random(0.8, 1.15));
          p.beginShape();
          for (var q = 0; q < pts.length; q++) p.vertex(pts[q][0] + jx + p.random(-0.4, 0.4), pts[q][1] + jy + p.random(-0.4, 0.4));
          p.endShape();
        }
      }
    };
  });
})();
