---
title: Hero animation — plan v3 (realistic motion from real reference)
status: proposal for Tony
created: 2026-11-15
replaces: the "pose by numbers" approach of v0 and v1
---

# Hero animation plan v3: realistic motion

## 1. Why it still looks awkward

The problem is not the drawing library. **The motion is made up.** Every pose in v0 and v1 is a set of joint angles typed in by hand. People and dogs move in ways that are very hard to invent: weight shifts, timing differences between joints, how a dog's spine flexes in a gallop. Animators solve this with **reference**: they film the action and draw over it (rotoscoping), or use motion capture. John Martin's work feels real because the timing and poses come from observation.

So the plan changes from "write better poses" to "**take motion from real footage, then draw it as pencil**".

## 2. The suggested tools, judged

| Tool | What it is good for | Does it fix the awkwardness? |
|---|---|---|
| **Rough.js** | Sketchy, hand-drawn versions of shapes: lines, circles, curves. | No. It makes shapes look hand-drawn, but it doesn't make poses or motion realistic. It's useful for the scenery and props (waves, sun, basket, wheel). |
| **GSAP** | Timelines and easing for motion on a web page. | No. It is a very good timing tool, but it only moves between poses you give it. That's what v1 already does. Useful only if parts stay live on the page. |
| **FFmpeg** | Joining rendered frames into a video. | Not on its own, but it's the right final step. Export **MP4 and WebM** (about 300–600 KB for 10 seconds), not GIF. |
| **gif-encoder-2** | Making GIFs. | No. A 10-second, 600 px GIF would be several MB, with banding in the pencil texture. Use it only for review previews you share, not for the site. |
| **A different model (Fable)** | Possibly a fresh chat with more room for this one task. | The model isn't the bottleneck: no model can invent believable dog and human motion as numbers. A **new chat** is still a good idea, because this conversation is very long. |

## 3. The new pipeline: real motion, pencil look

```
1. Reference video        Tony and Juhu filmed on a phone (plus stock clips for the dive, swim and cycle)
        │
2. Motion extraction      Per frame: body keypoints and a cut-out silhouette
        │                   - Tony: MediaPipe Pose and segmentation (free, runs locally)
        │                   - Juhu: DeepLabCut "SuperAnimal" quadruped model (free) and SAM 2 for the outline
        │
3. Line drawing           Silhouette outline and key inner lines, simplified into a few pencil strokes per frame:
        │                   pressure, gaps, line boil. Our v1 pencil renderer; Rough.js for scenery
        │
4. Staging and joins      Characters placed and scaled per scene. Ground, then wave, road, horizon, shore:
        │                   2D lines with draw-on and morphs (our engine, with GSAP-style easing)
        │
5. Render                 Every frame drawn headless (Chrome) to PNG, at 24 fps, characters on twos
        │
6. Encode                 FFmpeg: WebM (VP9) and MP4 (H.264) loops, plus a poster still; GIF only for previews
        │
7. On the site            <video autoplay muted loop playsinline> right of the intro, poster first,
                          a still image for reduced motion, and a small pause control (WCAG 2.2.2)
```

**Why this works:**
- Every frame comes from a real body moving in real time, so the weight, timing and overlap are right automatically.
- The pencil look is applied over the motion, the way an animator traces reference.
- Simplifying hard to a few strokes keeps it calm and in John Martin's spirit, and stops it looking like a traced video.
- One video file is lighter and smoother on the page than live drawing code. p5.js is no longer needed on the live site.

## 4. Reference to film (Tony's part)

Use a phone at 60 fps, filmed from the side, at waist height, held still, against a plain background, with good light. 5–10 seconds per clip.

| Clip | Who | Needed for |
|---|---|---|
| Easy jog, left to right | Tony | Beat 1 |
| Juhu running and jumping up at someone (for example, at Tony's back) | Juhu (and Tony) | Beats 2–3 |
| A stumble forward into a dive onto a soft surface or into a pool (or stock footage) | Tony or stock | Beat 3 |
| Snorkel or fins swimming under water (stock is fine) | Stock | Beats 4–5 |
| Riding a bicycle past the camera | Tony or stock | Beats 7–8 |
| Holding up and throwing a frisbee | Tony | Beats 10–11 |
| Juhu bouncing for a frisbee, then leaping after it | Juhu | Beats 10–11 |
| Juhu walking and trotting on the beach | Juhu | Beat 9 |

Stock clips: free sources such as Pexels or Pixabay, with licences that allow use. They are only traced as reference; nothing from them appears directly.

## 5. Steps and review gates

1. **One-second proof (the gate):** your jog clip becomes about 1 second of pencil animation, compared side by side with v1 and with John Martin. If it doesn't clearly feel more alive, we stop and rethink.
2. **Juhu proof:** her run and jump. Dogs are the hardest part of the pipeline.
3. **Line style lock:** stroke count, pressure, boil and texture, agreed on one still and one moving shot.
4. **All 11 beats,** each from its reference, staged and timed to about 10 seconds.
5. **Joins and scenery:** the ground becoming water, then road, then shore, with draw-ons.
6. **Encode and add to the site:** size budget, poster, reduced motion, pause control, phone test.

## 6. Setup this needs on your Mac
- Python packages: `mediapipe`, `opencv-python`, and `deeplabcut` (or its lighter SuperAnimal inference), plus SAM 2 for clean outlines.
- `ffmpeg` (via Homebrew).
- Everything runs locally. No footage leaves your machine.

## 7. Risks
- **Juhu's pose tracking may need manual fixes** on fast frames. Mitigation: track at 60 fps, smooth the motion, and fix a few frames by hand.
- **Too much detail from real outlines.** Mitigation: simplify hard, with roughly 8–15 strokes per figure.
- **Underwater and cycling reference** depends on finding good stock footage.
- **Effort:** this is more work than v1, but each step produces something you can see and judge.
