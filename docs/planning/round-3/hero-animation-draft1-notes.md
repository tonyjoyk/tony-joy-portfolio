---
title: Hero animation — first draft notes and next steps
status: draft 2 is in the hero slot (local branch, not pushed)
created: 2026-11-15
---

# Hero animation: draft notes

## Draft 2 (2026-11-15)
Built by `hero/tools/v3/film2.py`. The source windows are in `hero/tools/v3/work/windows2.json`. The loop is 240 frames, 10 s. Files: WebM 246 KB, MP4 263 KB.

Fixed since draft 1:
- **Length:** the loop is now 10 s.
- **Lines through figures:** each figure now hides the world lines and props behind it.
- **Juhu:** she is a shepherd in every beat. She trots in (Pexels 4166357), jumps up at Tony's back (10665038), bounces on four legs and leaps out (10665038).
- **Swim:** the swimmer is a freediver with real fins (37236357). The goggles, snorkel and bubbles are drawn in code.
- **Ball:** it stays in the hand, stays small through the bounces, lands, and then grows into the wheel.
- **Colour:** the video is tagged with BT.709 colour. Its background is within 1 shade of the page colour.

Still open from the list below: 2 (the throw clip is cut at the knees, so the thrower is a close shot), 5 (Juhu jumps up next to Tony, not onto his back), 7 (smaller), 9 (backpack and beanie), 11 (the thrower's hair is a light mass), 12.

## Draft 1 notes

## What is in draft 1
- One loop of 276 frames at 24 fps (11.5 s). The figures change on twos.
- Files: `hero/hero-loop.webm` (290 KB), `hero/hero-loop.mp4` (313 KB), `hero/hero-poster.png`.
- The video goes into `#hero-animation` after the page loads. Reduced motion shows the still frame. A small "Pause" button stops the loop (WCAG 2.2.2).
- How it was made:
  - Each person and dog is traced from free Pexels clips. The clips are listed in `hero/tools/v3/SOURCES.md`.
  - The tracing uses MediaPipe pose and YOLO11 segmentation.
  - The ball, basket, bike, sun, sea, road and frisbee are drawn in code.
  - Build steps: `extract.py`, then `film.py`, then ffmpeg. See `hero/tools/v3/README.md`.
- Review page: `hero/lab/v3/`.

## Known problems to fix (in order)
1. **Too long.** The loop is 11.5 s. The target was about 10 s. Shorten the swim (66–118) and the beach (226–276) first.
2. **The thrower faces the camera and his legs are cut off.** This clip is a close shot, so he looks different from the rest. Find a side-view frisbee throw with the full body, or film Tony.
3. **Lines cross the figures.** The sea lines and the horizon go through the thrower and the cyclist. Mask the world lines behind each figure: erase them inside the figure outline.
4. **Juhu does not look like one dog.** Three clips are used (a border collie running, a shepherd on a beach, the collie leaping). Use one German Shepherd clip, or Tony's footage of Juhu, for every dog beat.
5. **Juhu does not land on Tony's back.** She jumps over him. Film or find a dog jumping up at a person's back.
6. **Underwater, Tony does not look like Tony.** The swim clip is cut at the frame edge, and the mask is soft. Add the snorkel, goggles and fins in code (the storyboard needs them). Use a full-body swim clip.
7. **The ball does not stay in the hand.** The wrist landmark is noisy underwater. Smooth it, or fix the ball to the front of the outline.
8. **Ball to wheel.** The ball grows during the bounces. It should stay small until it lands, then grow into the wheel in one move.
9. **The cyclist wears a beanie and a backpack.** Remove the backpack bump from the outline, or use another clip. Tony has no cap, so the beanie must read as hair.
10. **The video box.** The video background can look a little different from the page colour on some screens. Encode with full-range colour, or make the page colour match the video.
11. **Hair on side views** sometimes covers the face. Tune the hair edge per clip.
12. **Size.** 300 KB is acceptable. Check on a slow phone connection, and add `preload="none"` if needed.

## Plan for the next session
1. Tony reviews draft 1 on the page and in `hero/lab/v3/`, and marks the beats he wants to change.
2. Get footage of Tony (jog, frisbee throw) and of Juhu (run, jump at Tony's back, bounce, leap). Film from the side, at 60 fps, with the phone held still. Then run the same pipeline on it.
3. Fix problems 1, 3 and 4, then the others.
4. Encode again, check on a phone, then push. Pushing also publishes the brand-refresh changes. That branch still has open items (see its hand-over note). Tony must approve them first.
