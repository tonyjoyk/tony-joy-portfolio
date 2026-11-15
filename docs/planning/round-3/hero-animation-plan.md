---
title: Hero animation — build plan (code, p5.js)
status: draft, awaiting Tony's approval
created: 2026-11-15
method: BMAD (requirements → design → architecture → stories), kept short
sources: [Miro storyboard v2 (https://miro.com/app/board/uXjVENq2ql0=/), ../round-2/ux-spec.md]
---

# Hero animation: build plan

## 1. What we are making

A short line-drawing loop at the top of the site, right of the intro. Tony and Juhu move through one continuous scene that keeps changing: jog → Juhu leaps in → dive → swim down → basket → ball bounces → becomes a cycle → ride into the sunset → beach → throw → Juhu leaps out → back to the jog.

**Decisions from Tony (2026-11-15)**
- Fast. A short loop with no long pauses.
- Everything drawn by code. No hand-drawn frames, no video files.
- p5.js.
- Tony has no cap.
- Juhu does not carry the frisbee when she leaps in.
- One colour (laterite), pencil look, no frame, semi-realistic figures (not stick figures).

## 2. Timing: about 10 seconds

Every beat flows into the next. The longest still moment is about half a second.

| # | Beat | Time (s) |
|---|---|---|
| 1 | Easy jog | 0.0 – 1.0 |
| 2 | Juhu leaps in from the left | 1.0 – 1.6 |
| 3 | Forward fall becomes a dive arc | 1.6 – 2.5 |
| 4 | Swim down: snorkel, goggles, fins | 2.5 – 3.6 |
| 5 | Ball into the basket on the pool floor | 3.6 – 4.4 |
| 6 | Ball falls into a dry frame, bounces twice | 4.4 – 5.3 |
| 7 | Ball becomes a wheel, the cycle grows out of it | 5.3 – 6.0 |
| 8 | Ride along an S-curve road into the sunset | 6.0 – 7.4 |
| 9 | The beach and sea draw in | 7.4 – 8.1 |
| 10 | Tony holds the frisbee, Juhu bounces | 8.1 – 9.0 |
| 11 | Throw; Juhu leaps out on the right | 9.0 – 9.8 |
| – | Loop: jog again, Juhu re-enters from the left in the same leap | 9.8 → 0.0 |

The timings are a first guess. We tune them in the review page (§5).

## 3. How it works (architecture)

```
timeline (0 → 9.8 s, loops)
   │  for the current time, finds the two nearest key states and eases between them
   ▼
scene state  ──►  rigs (Tony, Juhu)        joint angles  → body contours
                  props (ball, cycle, …)   shapes        → outlines
                  world lines (ground → wave → road → shore)  morphing point lists
                  camera                   pan / follow  (into the water, after the ball)
   │
   ▼
pencil renderer: thin layered strokes, small gaps, redrawn with slight jitter (line boil)
   │
   ▼
p5.js canvas, about 420 px square, laterite on the page background
```

**Characters are rigs, not stick figures.** Each body is a set of joints (hip, knee, shoulder…). Around each bone the code draws a tapered contour with real width: a thigh is thicker than a shin, the torso has a chest and a back. Proportions come from the runner, cyclist and thrower in your footer drawing, so the top and the bottom of the site match.
- **Tony:** about 7 heads tall, no cap. Swim gear (snorkel, big goggles, fins) draws on as he goes under.
- **Juhu:** a German Shepherd: tall pointed ears, long muzzle, deep chest, long bushy tail.

**Motion comes from poses, not frames.**
- Each beat has 2–3 key poses, stored as joint angles. That is about 30 poses for the whole loop.
- Code fills in every frame between poses at the screen's frame rate, up to 60 frames a second. This gives the fluid, never-still motion of John Martin's animation.
- The animation principles are built into the in-betweening:
  - **Easing:** slow in and slow out of each pose.
  - **Arcs:** joints rotate, so hands and paws travel on curves.
  - **Overlapping action:** the tail, ears and fins lag a few frames behind.
  - **Squash and stretch:** on the ball, and on Juhu's leap.

**The world morphs instead of cutting.** Each environment line is a list of points. The same line becomes ground, then wave, then water surface, then road, then horizon, then shore, by moving its points. In the same way, the ball's circle becomes the wheel.

**The pencil look.**
- Each stroke is drawn as 2–3 thin passes, with small gaps and varied darkness.
- The strokes are redrawn with tiny random offsets about 12 times a second, so the line trembles (line boil) while the motion stays smooth.
- A light paper-grain texture adds the pencil tooth.

**On the page.**
- p5.js runs in "instance mode", so it can't clash with the rest of the site.
- It starts only after the page has loaded. A still drawing shows until then.
- It pauses when it's off screen or the tab is hidden.
- With reduced motion turned on, it shows one still drawing (the beach).
- Size: p5.js itself is about 1 MB (roughly 300 KB compressed), larger than the whole site today. Mitigations:
  - load it only after everything else, from a pinned CDN version;
  - if that's still too heavy, port the finished code to plain canvas (same drawing code, about 20 KB) for the live site, and keep p5.js for building and reviewing.

## 4. Build steps (stories)

Each step ends with something you can see in a review page. Nothing goes on the live site until you approve the final loop.

| Step | What gets built | You review |
|---|---|---|
| 1 | **Review page:** a separate local page with play/pause, a time scrubber, a speed slider and frame-by-frame stepping. | Nothing yet (tooling). |
| 2 | **Pencil renderer:** the stroke style, line boil and grain, shown on simple shapes. | Does it feel like pencil? |
| 3 | **Characters:** Tony and Juhu rigs, shown as a model sheet (side, front, back, a few poses). | Do they look like you and Juhu? |
| 4 | **Rough loop (animatic):** all 11 beats with key poses only, linear timing, no polish. | Is the story and the speed right? |
| 5 | **Motion polish:** easing, arcs, overlap, squash and stretch, morphs and camera moves. | Does it flow? |
| 6 | **Loop seam and details:** a seamless join at the loop point, the swim gear, the cycle growing out of the wheel, the beach drawing in. | Any beat to fix? |
| 7 | **Performance and size:** a steady frame rate on a phone, off-screen pause, reduced motion, size check, the p5.js vs plain-canvas decision. | — |
| 8 | **On the site:** placed right of the intro, tested on desktop and phone, then pushed. | Final approval. |

## 5. How we review

The review page lets you scrub to any moment. Give feedback by beat number and time, for example "beat 3 at 2.1 s: the arc is too high". We tune the poses and timings and reload.

## 6. Risks

- **Rigs can look like puppets.** Mitigations:
  - contour strokes with uneven width and slight overlaps;
  - a slight wobble on every pose;
  - checking proportions against your footer figures at step 3.
- **Juhu is the hardest figure.** Four legs and a tail in a leap. Expect a few rounds at steps 3 and 5.
- **10 seconds is fast for 11 beats.** If it feels rushed, the first option is to merge beats 6 and 7 (the bounce and the wheel). Lengthening the loop comes after that.
- **p5.js size**, covered in §3.
