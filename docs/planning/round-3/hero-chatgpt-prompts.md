---
title: Hero animation — ChatGPT key-frame prompts
status: ready for Tony to run
created: 2026-11-15
updated: 2026-11-15 (no photos, low-fidelity line frames, one image of 12 frames per scene, frames matched to the Miro storyboard v2 keys)
informed_by: Tony's brief (survey, Miro storyboard v2 in hero/keyframes/, decisions) and the draft 2 review against the 12 principles of animation
---

# Hero animation: ChatGPT key-frame prompts

## Steps (do these first)

You use **one** ChatGPT chat for all the work. ChatGPT keeps the style and the characters from earlier messages in the same chat. You do not attach photos or images.

1. Open a new ChatGPT chat.
2. Copy the **shared block** and **prompt 0**. Paste both into **one** message. Send it.
3. Look at the result. If the line style is too detailed, write: "Simpler. Fewer lines. Looser." Send it again until the style is correct.
4. Save the image as `style.png`.
5. Copy the **scene 1** prompt. Paste it into a new message. Send it.
6. Do the checks in the "Checklist" section at the end of this file.
7. If one frame is wrong, write: "Redo only frame N. Keep all other frames the same." Send it.
8. Save the image as `scene1.png`.
9. Do steps 5 to 8 for scenes 2, 3, 4, 5, 6 and 7, in this order.
10. If the style or the characters start to change, paste the shared block again at the top of your next message.
11. When you have the 8 images (`style.png` and `scene1.png` to `scene7.png`), give the folder to Claude. Claude traces the lines and makes the animation.

Do not send the shared block alone. Send it one time, together with prompt 0. Send it again only if the style changes.

---

## Why the prompts are made this way

- **The frames follow the storyboard you approved.** These are the 25 keys of the Miro storyboard v2, stored in `hero/keyframes/`. Each scene prompt gives every frame the position, size, direction and pose from those keys. Positions are given as a share of the frame (for example "40% from the left"), so ChatGPT has less to guess.
- **Key frames, not illustrations.** Each image shows one scene as 12 small frames. We trace the lines, redraw them in our pencil line, and add in-between frames. Each frame shows for a fraction of a second at about 300 px, so detail does not matter. **Pose, position, timing and line style matter.**
- **Low fidelity on purpose.** A loose line drawing with few strokes is easier for ChatGPT to keep the same across 12 frames. It is also the style we want, like the footer drawing on the site and John Martin's animation.
- **The joins are written in full.** In draft 2 the joins went wrong: two Tonys on screen, lines breaking into dashes, and a ball and a wheel drawn at the same time. Every scene starts with the last frame of the scene before it.
- **The cycling scene has real depth.** In draft 2 the bike slid up the screen in side view, which looked flat. Scene 5 uses a strict one-point perspective: the road edges meet at the sun, the bike stays on the road, turns away from us, and gets much smaller in every frame.
- **The 12 principles are in the frame lists:**
  - squash and stretch on the ball
  - a crouch before Juhu's chase
  - a wind-up before the throw
  - a splash when Tony hits the water
  - follow-through on the tail and the arms
  - slow in and slow out shown through the spacing between frames

**The loop: 10 s, 240 frames at 24 fps.** Storyboard frame numbers are in brackets in each scene title.

| Scene | Storyboard frames | Seconds |
|---|---|---|
| 1 Jog, Juhu flies in and lands on Tony's back, pushed into a dive | 0–32 | 1.4 |
| 2 Dive arc, ground becomes water, head first, under water with gear | 32–60 | 1.2 |
| 3 Swim down, ball into the basket, the ball drops through, Tony swims up | 60–102 | 1.75 |
| 4 Follow the ball down, it lands on a road, bounces, becomes a wheel, the cycle grows | 102–152 | 2.1 |
| 5 Ride along the curving road into the sun | 152–188 | 1.5 |
| 6 The beach draws in, Tony and Juhu walk in, frisbee up, wind-up, throw | 188–228 | 1.7 |
| 7 Juhu leaps after the frisbee and leaves, the beach turns back into ground, the jog | 228–239, then 0–12 again | 0.5 + loop check |

---

## Shared block (paste once, with prompt 0)

```
I am making a short hand-drawn 2D loop animation for my portfolio website. You will draw KEY FRAMES for it, one scene per image. Follow these rules in every image in this chat.

LINE STYLE
- Loose, hand-drawn pencil line drawing. Few strokes: about 8 to 15 strokes per figure.
- Strokes are uneven: a little thicker in the middle, thin at the ends, with small gaps where lines meet, like a quick confident sketch.
- ONE colour only: laterite red-brown (#A4553A) on a warm off-white background (#F7F5EF).
- Line only: no shading, no hatching, no fill, no texture. One exception: the hair is a small solid patch of the same red-brown.
- No faces: no eyes, no mouth, no facial details. Simple, semi-realistic body shapes with real proportions (not cartoon, not stick figures).
- Calm and playful, not busy. Lots of empty space.

CHARACTERS (keep them the same in every frame)
- Tony: a Malayali man, about 35, slim, average height, short dark hair, a short beard, NO cap or hat. T-shirt and shorts. When he stands, he is about 1/3 of the frame height.
- Juhu: Tony's dog, a German Shepherd: tall pointed ears, long muzzle, long bushy tail. Her back is about level with Tony's hip.

LAYOUT OF EVERY SCENE IMAGE
- Landscape image with 12 SQUARE frames: 4 columns x 3 rows, read left to right, top to bottom.
- All frames are the same size, separated by thin light gaps. No borders around the frames.
- A small frame number (1 to 12) under each frame. No other text.
- Positions in my instructions are measured inside one frame: "40% from the left" and "78% from the top".

ANIMATION RULES
- The camera is LOCKED unless the scene says it moves. Every frame shows the same view.
- The ground line stays at the same height in every frame unless the scene says it changes.
- Characters keep the same size in every frame unless they move away from the camera.
- Only ONE Tony and ONE Juhu in a frame. Never draw the same character twice in one frame.
- Frames are evenly spaced in time. Show speed with spacing: poses close together when slow, far apart when fast.
- Everything moves left to right unless I say otherwise. Tony and Juhu face right.
- Frame 1 of each scene repeats the last frame of the scene before it.
```

## Prompt 0: style and character check (send with the shared block)

```
Before the scenes, make one test image to fix the style. Landscape, 4 columns x 2 rows of square frames, same line style as above.
Top row, Tony (side view, facing right): standing; jogging with one foot on the ground; jogging with both feet off the ground; holding a frisbee across his chest ready for a backhand throw.
Bottom row, Juhu (side view, facing right): standing; trotting; leaping with her body stretched long and all four legs off the ground; crouched low, ready to run.
Draw a short ground line under each figure. Keep it very simple: few strokes, no faces.
```

## Scene 1: jog, Juhu flies in and lands on Tony's back, pushed into a dive (storyboard 0–32)

```
SCENE 1 (12 frames). Side view, camera at waist height, locked. Ground line: a flat line across the whole frame at 78% from the top. Tony jogs to the right but stays near 40% from the left: the world moves, not Tony. Three short dashes on the ground move a little to the left in each frame.
Juhu is ALREADY IN THE AIR when she enters: one long leap from the left, body stretched, front legs reaching forward, back legs stretched back, tail streaming. She has NOTHING in her mouth.
1: Tony, jog contact pose (front heel touching the ground, arms swinging). Juhu only half visible at the left edge, high in her leap (her body at 55% from the top).
2: Tony, jog passing pose (one knee up, the other foot pushing). Juhu fully in the frame at 10% from the left, same leap pose, a little lower.
3: Tony, contact pose on the other foot. Juhu at 25% from the left, coming down towards Tony's back.
4: Tony, passing pose; he has not seen her. Juhu right behind him, front paws reaching for his shoulder blades.
5: CONTACT: Juhu's front paws land on Tony's upper back. Her body is angled up behind him, back legs reaching for the ground. Tony's chest and head jolt forward, arms fly back.
6: Tony leaning forward 30 degrees, one leg kicking back. Juhu's back paws touch the ground behind him; her front paws still on his back.
7: Juhu pushes off his back. Tony tipping further forward (45 degrees), arms swinging forward to catch himself.
8: Tony's arms reach forward and down, like starting a dive. Juhu standing on the ground behind him, at 25% from the left, watching.
9: Tony's feet leave the ground. His body is a forward dive shape at about 60 degrees, arms straight out in front. The ground line under his hands starts to ripple. Juhu standing.
10: Tony's body almost straight, heading forward and down. The ground line becomes gentle waves under him. Juhu starts to fade (broken lines).
11: Same dive, a little further right (50% from the left). The line is now clearly a wavy water surface. Juhu gone.
12: Tony in a long, stretched dive, arms together pointing forward, body 30 degrees down, above the waves.
```

## Scene 2: dive arc, the ground becomes water, head first, under water with gear (storyboard 32–60)

```
SCENE 2 (12 frames). Frame 1 = scene 1 frame 12. A wavy water surface across the frame at 70% from the top.
1: Same as scene 1 frame 12.
2: Top of the dive arc: Tony almost flat, at 60% from the left, 55% from the top. Arms together forward.
3: Tony starts to tip head-down (about 40 degrees), arms pointing at the water.
4: Head-down at about 60 degrees, hands just above the water at 70% from the left.
5: Hands and head go into the water: a small crown splash (5 or 6 short curved strokes) around his arms.
6: Only his hips and legs above the water. Splash at its highest. Ripples spreading on the surface.
7: Only his feet above the water. Splash falling.
8: CAMERA GOES UNDER THE WATER: the water surface line jumps up to 12% from the top. Tony under it, head-down at 45 degrees, at 45% from the left, 35% from the top. A trail of bubbles above him.
9: Same view. A snorkel and goggles start to appear on his face (half drawn).
10: Snorkel and goggles complete. Long swim fins start to appear on his feet.
11: Fins complete. Tony gliding down to the right at 45 degrees, three small bubbles rising from the snorkel.
12: Tony under water at 42% from the left, 33% from the top, head-down at 45 degrees, with snorkel, goggles and fins, legs together. Three bubbles above his head.
```

## Scene 3: swim down, the ball into the basket, the ball drops through, Tony swims up (storyboard 60–102)

```
SCENE 3 (12 frames). Under water. The water surface line at 12% from the top. Frame 1 = scene 2 frame 12.
1: Same as scene 2 frame 12.
2: Tony kicks (one fin up, one fin down), moving down to the right. Bubbles rising.
3: Opposite kick. A pool floor line starts to appear at 87% from the top.
4: Tony at 50% from the left, 50% from the top, more head-down (about 60 degrees). A small ball (about the size of his head) appears in his front hand. The pool floor moves up to 87% and an underwater rugby basket appears on the floor at 63% from the left: a round bucket on a short stand, about as tall as Tony's arm, with an open top.
5: Kicking, the ball held forward, Tony getting closer to the basket.
6: Tony right above the basket, head-down at 75 degrees, arm with the ball pulled back (getting ready).
7: Arm pushes forward: the ball leaves his hand and drops into the basket opening.
8: GOAL: the ball inside the basket, slightly squashed. Tony's free arm punches up; a burst of bubbles.
9: Tony turns to swim up: his body turns upright, fins kicking down. The ball falls through the bottom of the basket.
10: Tony swimming straight up at 53% from the left, 35% from the top, arms by his sides. The ball under the basket, at 83% from the top.
11: Tony higher (25% from the top), only fins kicking. The ball falling further, at the bottom edge.
12: Tony nearly out of the top of the frame. The ball half out of the bottom edge.
```

## Scene 4: follow the ball down, it lands on a road, bounces, becomes a wheel, the cycle grows (storyboard 102–152)

```
SCENE 4 (12 frames). Side view. Frame 1 = scene 3 frame 12. In frames 2 to 4 the CAMERA FOLLOWS THE BALL DOWN: the water, the pool floor and the basket move up and out of the top of the frame.
1: Same as scene 3 frame 12.
2: Tony gone. The pool floor line and the basket at 25% from the top (moving up). The ball at 63% from the left, 50% from the top, falling.
3: The pool floor and the basket leave through the top edge (draw them broken). The ball at 63% from the left, 55% from the top, a little stretched up and down. A flat road line draws in from the left at 78% from the top.
4: The ball just above the road, more stretched.
5: The ball HITS the road at 65% from the left: squashed into a wide flat oval.
6: The ball bounces up and to the right: stretched up and down, at 70% from the left, 60% from the top.
7: Top of the bounce, round.
8: Second bounce at 75% from the left: squashed again, and the ball is now TWICE as big.
9: The ball rolls a little and grows into a bicycle wheel: a circle about 1/8 of the frame wide, with a hub and a few spokes, touching the road at 78% from the left. Only ONE circle in this frame.
10: This wheel is the FRONT wheel. The bicycle frame draws itself backwards (to the left) from its hub, half finished.
11: The back wheel and the frame complete: a simple bicycle facing right, front wheel at 78% from the left. Tony starts to appear on the saddle, drawn from his feet on the pedals upwards.
12: Tony complete, seated, hands on the handlebars, pedalling. The bicycle and Tony together are about 1/3 of the frame high.
```

## Scene 5: ride along the curving road into the sun (storyboard 152–188)

```
SCENE 5 (12 frames). This scene must feel DEEP, not flat. Use a strict ONE-POINT PERSPECTIVE.
- The VANISHING POINT is the centre of the setting sun. The sun is a half circle sitting ON the horizon line, at 72% from the left. The horizon line is a flat line across the frame at 42% from the top. Both stay the same in every frame.
- THE ROAD: two edges that start wide at the bottom of the frame (left edge at 7% from the left, right edge at 55% from the left), bend in one gentle S-curve, and meet EXACTLY at the vanishing point. The road is the same in every frame from frame 3.
- The bicycle is always ON the road, in the middle between the two edges, both wheels on the road.
- SIZE: Tony and the bicycle get much smaller in every frame. Their height as a share of the frame height: 1: 33%, 2: 33%, 3: 26%, 4: 20%, 5: 15%, 6: 11%, 7: 8%, 8: 6%, 9: 4%, 10: 3%, 11: 2%, 12: a tiny dot at the vanishing point, inside the sun.
- THE VIEW TURNS with the road: frames 1 and 2, side view facing right; frames 3 and 4, three-quarter back view as he turns into the road; frames 5 to 12, back view (we see his back and the back wheel), always pointing at the vanishing point.
- Tony pedals in every frame (change the leg positions each frame).
1: Same as scene 4 frame 12. Behind him, the horizon line and the sun start to draw in (half finished), and the flat road line starts to bend.
2: The road edges complete, from the bottom of the frame to the vanishing point. Tony in side view at 60% from the left, on the road near the bottom.
3 to 12: Tony rides along the road into the distance, following the S-curve, getting smaller as above, until he is a dot in the sun.
```

## Scene 6: the beach draws in, Tony and Juhu walk in, frisbee up, wind-up, throw (storyboard 188–228)

```
SCENE 6 (12 frames). Same horizon (42% from the top) and sun (72% from the left) as scene 5. The sun sinks a little lower in each frame.
1: Same as scene 5 frame 12: the cyclist is a dot inside the sun.
2: The road fades away (broken lines). Two long, gently wavy sea lines appear below the horizon, at 48% and 56% from the top.
3: A gently curved shoreline draws in at about 70% from the top, and a softer sand line at 85% from the top. Empty beach.
4: Empty beach, a short hold (almost the same as frame 3).
5: Tony walks in from the left edge, side view, facing right, feet on the shoreline. A frisbee in his hand. Juhu trots in ahead of him.
6: Tony walking at 25% from the left. Juhu trotting at 48% from the left, tail up.
7: Tony stops at 28% from the left and holds the frisbee UP over his head. Juhu turns round to face Tony and BOUNCES up on her back legs, front paws in the air.
8: Juhu lands, facing Tony, looking at the frisbee, tail wagging.
9: WIND-UP: Tony brings the frisbee across his chest for a backhand throw, shoulders twisted away from the throw, knees bent. Juhu CROUCHES low, facing Tony, tail wagging (a different tail position).
10: The wind-up at its extreme, almost the same as frame 9 (a short hold).
11: THROW: Tony's arm whips forward, the body untwists, the frisbee leaves his hand and flies up to the right (at 50% from the left, 44% from the top). Juhu turns to face right, ready to chase.
12: Follow-through: Tony's throwing arm stretched out to the right, his weight on the front foot. The frisbee higher, at 65% from the left, 35% from the top. Juhu starts to run right.
```

## Scene 7: Juhu leaps after the frisbee and leaves, the beach turns back into ground, the jog (storyboard 228–239, then the start of the loop)

```
SCENE 7 (12 frames). Frame 1 = scene 6 frame 12. This scene joins the end of the loop to the start.
1: Same as scene 6 frame 12.
2: Juhu LEAPS after the frisbee: body stretched long, all four legs off the ground, tail streaming, at 70% from the left, 55% from the top. The frisbee at 85% from the left, 28% from the top. Tony starts to jog (same jog as scene 1) at 34% from the left. The sea lines and the sun start to fade (broken lines).
3: Juhu at 90% from the left in the same leap pose, the frisbee leaving the top-right corner. The horizon and the shoreline fade. The sand line flattens into a straight ground line at 78% from the top. Tony jogging.
4: Juhu leaves through the right edge (only her tail visible). The beach is gone: only the flat ground line. Tony jogging at 37% from the left.
5: Only Tony jogging (passing pose) at 40% from the left; ground dashes appear.
6 to 12: THESE MUST BE THE SAME AS SCENE 1, FRAMES 1 TO 7: Juhu flies in again from the left in the same leap (with NO frisbee in her mouth), Tony jogging, and so on. This shows that the loop joins without a jump.
```

## Checklist (look at every image before you save it)
- 12 square frames, numbered 1 to 12, in a 4 × 3 grid.
- One colour (red-brown) on off-white. Line only, few strokes, the hair as a small solid patch, no faces.
- Only one Tony and one Juhu in each frame. Tony has a beard and no cap. Juhu has pointed ears and a bushy tail.
- The ground line or horizon stays at the same height across the frames (except where the scene says it moves).
- Frame 1 looks like frame 12 of the previous scene.
- Scene 1: Juhu is already in the air when she enters, with nothing in her mouth.
- Scene 4: never a ball and a wheel at the same time.
- Scene 5: the road edges meet at the sun, the bicycle stays on the road, turns away from us, and is much smaller in every frame.
- If one frame is wrong, write "Redo only frame N. Keep all other frames the same."

## After the images exist (Claude, next session)
1. `hero/tools/v3/sheets.py`: cut each scene image into its 12 frames, find the red-brown lines, and trace them into strokes.
2. `film4.py`: place each key frame at its storyboard frame number (`hero/keyframes/timeline.json`), add in-between frames by blending outlines, and redraw everything in our pencil line. Keep the fixes from the draft 2 review: one Tony at a time, strokes draw on in order, short holds on key poses, no double circle.
3. Encode as in draft 2 (BT.709, WebM and MP4), and review on the page.
