---
title: Hero animation — the brief (what Tony wants)
status: current, 2026-11-15
purpose: Give this file to any new chat or person working on the hero animation. It describes what the animation must be, in Tony's terms. It is not a technical plan.
---

# Hero animation: the brief

## 1. What it is

- **What:** a short looping line animation at the top of Tony's portfolio website, to the right of the intro text ("Hey, I'm Tony, a product designer from Kerala, India…").
- **Who is in it:** Tony and his dog Juhu, doing things Tony loves: jogging, swimming and underwater rugby, cycling, and playing frisbee with Juhu on the beach.
- **How it moves:** one continuous story. Each activity flows into the next with no cuts, and the loop never stops.
- **What the visitor should feel in the first 10 seconds:** trust, a smile, and "this work matters". The site must still signal serious public health work.

## 2. The feel

The brand rules for the whole site apply to the animation:

1. **Calm, not energetic**
2. **Capable, not clever**
3. **Playful, not cool**

- Nothing too fancy, no stimulating graphics, no "clever" tricks. The site is calm overall, with playful small moments. The animation is the main playful moment.
- **A little surreal, not realistic.** This is an animation, not a film. Bodies stretch, squash, arch and change size. Clothes change during a transition. One activity melts into the next. If it feels like real video, it is wrong.
- **Use the 12 principles of animation:**
  - squash and stretch
  - anticipation
  - staging
  - follow-through and overlapping action
  - slow in and slow out
  - arcs
  - secondary action
  - timing
  - exaggeration
  - solid drawing
  - appeal

  Things do not just move from A to B. They stretch, squash and overshoot, and there is a sense of motion and continuity from frame to frame.
- **Fast and short.** No long pauses. The target is about **10 seconds** for the whole loop.

## 3. The look

- **A hand-drawn, uneven pencil or ink line,** in the same style as the footer drawing on the site (`images/footer-landscape.svg`).
- **Line only.** No shading, no fills, no textures. One exception: the hair can be a small solid patch.
- **One colour:** laterite red-brown `#A4553A` on the page background `#F7F5EF`. Tony loves the red laterite rock of Goa and Kerala, with green growing from it.
- **Few strokes.** The figures are simplified, about 8 to 15 confident strokes each. The strokes are thin at the ends and fuller in the middle, with small gaps where lines meet, and a gentle "boil" (the line trembles slightly from drawing to drawing).
- **Simplified characters:** semi-realistic proportions, but no faces and no small details. Everything is small on screen and moves fast, so details cannot be seen anyway.
- **No frame** around the animation (an early idea was a circle; Tony dropped it).
- **The main reference** is the hero animation on **johnmartin.in**: bold, broken strokes, a solid head of hair, about 12 drawings a second, and a calm, alive feeling. **danielburka.com** is a reference for the site as a whole.

## 4. The characters

- **Tony:** a Malayali man, about 35, slim, short dark hair, a short beard. **No cap or hat, ever.** T-shirt and shorts on land. Keep identifying details to a minimum.
- **Juhu:** Tony's dog, a German Shepherd: pointed ears, long muzzle, bushy tail. She is a "she".

## 5. The story

This is the agreed storyboard (Miro, "Portfolio hero animation storyboard", version 2). The 25 key frames of that storyboard are stored in `hero/keyframes/`, with their timing in `hero/keyframes/timeline.json` (240 frames at 24 fps = 10 s).

1. **Jog.** Tony jogs along a simple ground line.
2. **Juhu leaps in** from behind (from the left). She is already in the air when she enters, and she has **nothing in her mouth**.
3. **She lands on Tony's back,** and he is pushed forward into a dive.
4. **Dive.** The ground line turns into water. Tony goes in head first.
5. **Under water,** Tony now has a snorkel, goggles and fins. He swims down.
6. **Underwater rugby:** Tony has the ball. He pushes it into the basket on the pool floor. Goal.
7. **The ball drops through** the basket, and Tony swims up and away.
8. **Follow the ball down:** it falls into a new, dry scene and lands on a road. It squashes, bounces up with a stretch, and bounces a second time, growing.
9. **The ball becomes a wheel.** The bicycle and Tony grow out of the wheel.
10. **Ride into the sunset:** Tony rides along a curving road towards the setting sun, getting smaller until he becomes a dot in the sun.
11. **The beach draws in:** the sun sits on the sea, and the beach is empty for a moment.
12. **Tony and Juhu walk in.** Tony holds up a frisbee and Juhu bounces. Tony winds up; Juhu crouches, tail going.
13. **Throw.** Juhu turns to chase, leaps after the frisbee, and the beach turns back into the ground line.
14. **Juhu leaves the frame on the right,** Tony is jogging again, and the loop starts: Juhu flies back in from the left with the same leap.

An earlier version (from Tony's first survey) ended differently: the cycle shrank into a frisbee that flew back, Juhu caught it, and they sat together on the sand at sunset. **The Miro version above replaced it.**

## 6. How the transitions must feel

The transitions are the most important part, and the part that has gone wrong most often. **Every join is a moment of animation, not a cut and not a cross-fade.** There is only ever one Tony on screen.

**Juhu's leap onto Tony's back, then into the water (Tony's own description):**
- Juhu's jump must not feel realistic. Her body **stretches long** in the leap, with a clear arc, then **squashes** as she lands.
- When Juhu touches Tony's back, **Tony arches much more than a real body could.** It is a surreal, rubbery bend that shows the push.
- In the same moment, **Juhu shrinks and disappears,** because the next scene has no Juhu. She does not just walk off or fade.
- **Tony's clothes change as he goes:** the shirt goes, and the **snorkel and the diving fins appear** on him, step by step, while he is diving.
- Then he goes into the water with a **small splash: a few very short lines** that show ripples, nothing big.
- There must be a sense of movement and proportion: stretch and squash, overshoot and settle, continuity from frame to frame. Going directly from "Juhu jumps" to "Tony is in the water" feels far too real.

**The same idea applies to every other join:**
- **Ground to water:** the ground line itself turns into the waves.
- **Ball to wheel:** the same circle bounces, squashes, stretches and grows. It is never a ball and a wheel at the same time. The bicycle and Tony grow out of that wheel.
- **Rider to sun:** the cyclist shrinks into a dot that becomes part of the sun. The sun stays, and the beach draws in around it.
- **Beach back to the jog:** the sea and the shore flatten back into the ground line, and Juhu's exit leap is the same leap that starts the loop.

## 7. The ride into the sunset: perspective

Tony's feedback on the drafts: the cycling looked flat and orthographic, and the bike was not in proportion. The ride must have real depth:

- **One vanishing point,** at the setting sun on the horizon.
- **The road is aligned strictly to that point:** its edges meet at the sun.
- **The bike stays on the road** and turns away from us as it rides off.
- **The size change is exaggerated:** the rider gets much smaller quickly, so it really feels like he is moving away into the sunset.

## 8. On the website

- **Where:** the animation sits in the hero slot to the right of the intro. It is a square, about 420 px on desktop and 300 px on smaller screens, and it stacks under the intro on phones.
- **Behaviour:** it just plays and loops. A very quiet pause control is acceptable for accessibility.
- **Reduced motion:** visitors who turn on reduced motion see a still drawing.
- **File size:** keep it small, so it never slows the page. Today it is a looping video of about 250–300 KB.
- **Light theme only:** the site has no dark mode.

## 9. What has been tried, and what Tony thought

- **v0, v1 and v2 (motion typed in by hand, poses built from code "bones"):** awkward and stiff. The lines looked boxy, because the motion was invented, not observed.
- **The v3 gate:** a one-second jog traced from real video, drawn in the pencil line. **Tony liked this a lot:** "much more alive", "very similar to what I want". The organic, curved lines came from tracing a real body's outline.
- **Drafts 1 and 2 (the full loop traced from stock clips):**
  - The story works, but it feels too real and assembled.
  - The joins are weak: two Tonys at once, lines breaking into dashes, a ball and a wheel drawn together.
  - Tony and Juhu change body from scene to scene.
  - The cycling perspective is flat.
  - The draft is in the hero slot on a local branch, not live.
- **ChatGPT key frames (in progress):** the first test came back too detailed (faces, fingers, clothes seams, fur). It looked like illustration, not animation drawings. The frames must be **far simpler and more minimal**, so that they are easy to make, trace and animate.

## 10. Rules that do not change

- Tony has **no cap**.
- Juhu does **not** carry the frisbee when she leaps in.
- **One colour, line only, no frame.**
- About **10 seconds**, looping, no long pauses.
- **Surreal and animated, not realistic.** Use the 12 principles.
- **One Tony and one Juhu at a time.**
- **Calm, capable, playful.**

## Related files
- Storyboard key frames: `hero/keyframes/` and `hero/keyframes/timeline.json`
- Plans: `docs/planning/round-3/hero-animation-plan.md`, `-v2.md`, `-v3.md`
- Draft notes and the draft 2 review: `docs/planning/round-3/hero-animation-draft1-notes.md`
- ChatGPT key-frame prompts (being reworked): `docs/planning/round-3/hero-chatgpt-prompts.md`
- Review page: `hero/lab/v3/` (gate proof, draft 1, draft 2)
