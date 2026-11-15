---
title: Hero animation — ChatGPT key-frame prompts
status: ready for Tony to run
created: 2026-11-15
informed_by: draft 2 review against the 12 principles of animation (joins, one Tony at a time, on-model characters, cycling perspective)
---

# Hero animation: ChatGPT key-frame prompts

Draft 2 traced stock footage. The motion inside each clip worked. These went wrong: the joins between scenes, Tony and Juhu staying on model, and the cycling perspective, which felt flat (orthographic). These prompts get ChatGPT to draw the key frames, especially the joins. We then trace them into our pencil line.

## Steps (do these first)

Use **one** ChatGPT chat for all the work. ChatGPT keeps the characters and the style from earlier messages in the same chat.

You send the **shared block** only one time, in the first message, **together with** prompt 0. You do not send the shared block alone. In the prompts below, the line "[paste the shared block]" is only for a new chat. In the same chat, you can delete that line.

### Before you start
1. Get one clear photo of Tony from the side, and one from the front.
2. Get one clear photo of Juhu from the side.
3. Make a folder for the images, for example `hero-frames`.

### Step 1: the model sheet
1. Open a new ChatGPT chat.
2. Attach the photos of Tony and Juhu.
3. Copy the shared block. Paste it into the message.
4. Copy prompt 0. Paste it under the shared block, in the same message.
5. Send the message.
6. Look at the result. Make sure that Tony has no cap and that Juhu is a German Shepherd.
7. If a pose is wrong, write: "Redo only the [pose name]. Keep everything else the same."
8. Save the image as `model-sheet.png`.

### Step 2: scene 1, sheet A
1. In the same chat, copy the scene 1 prompt. Paste it into a new message.
2. At the end of the message, write: "Make sheet A (frames 1-6) only."
3. Send the message.
4. Do the checks in the "Checklist for each sheet" section at the end of this file.
5. If one panel is wrong, write: "Redo only panel N. Keep everything else the same."
6. Save the image as `scene1-A.png`.

### Step 3: scene 1, sheet B
1. Write: "Now make sheet B (frames 7-12) of scene 1. Use the same characters, camera and layout."
2. Send the message.
3. Do the checks. Save the image as `scene1-B.png`.

### Step 4: the silhouette versions of scene 1
1. Copy prompt S. Paste it into a new message.
2. At the end, write: "Do this for sheet A of scene 1."
3. Send the message. Save the image as `scene1-A-sil.png`.
4. Copy prompt S again. At the end, write: "Do this for sheet B of scene 1."
5. Send the message. Save the image as `scene1-B-sil.png`.

### Step 5: scenes 2 to 7
1. Do steps 2, 3 and 4 again for each scene, in order: 2, 3, 4, 5, 6, 7.
2. Use the scene number in each file name, for example `scene2-A.png`.
3. Each scene starts with the last frame of the previous scene. Make sure that frame 1 looks the same as frame 12 of the previous scene.

### If the characters start to change
In a long chat, ChatGPT can slowly forget the rules. If Tony, Juhu or the line style starts to change:
1. Attach `model-sheet.png` again.
2. Paste the shared block again, at the top of your next message.
3. If this does not help, open a new chat. In the first message, attach `model-sheet.png` and the last sheet that you saved. Then paste the shared block and the next scene prompt.

### When you have all the images
1. Make sure that you have 29 images: the model sheet, plus 4 images for each of the 7 scenes.
2. Give the folder to Claude. Claude traces the silhouette images and makes the animation.

## Why the prompts are made this way

**My call as the animator: 1 model sheet + 7 scenes, 12 frames per scene, each scene delivered as two 6-panel sheets.**

Why not 12 panels in one image:
- A 12-panel grid gives each frame about 370 px.
- Image models lose consistency as panels get smaller: faces drift, Juhu changes breed, and the ground line wanders.
- A 2 × 3 grid on a 1536 × 1024 canvas gives six square 512 px panels, which is enough detail to trace a clean outline.
- Ask for the second sheet (frames 7–12) in the same chat, straight after the first, so ChatGPT keeps the characters and the camera.

Why these joins: the joins failed most in draft 2, so **every scene starts on the last frame of the scene before it**. Frame 1 of each scene repeats frame 12 of the previous one, so the cuts lock together.

**What we do with the sheets**
- We cut the panels apart and trace the silhouette versions. These are colour-coded, so tracing is exact.
- We draw the result in our own laterite pencil line.
- Each key holds for 2 frames ("on twos"), with outline morphs where a scene needs more frames.
- The line-art sheets are for timing and detail. The silhouette sheets are what we trace.

**Timing budget (10 s loop, 24 fps, on twos = 120 drawings)**

| Scene | Seconds | Drawings | ChatGPT keys | Made by us |
|---|---|---|---|---|
| 1 Run, Juhu leaps, Tony pitches forward | 1.5 | 18 | 12 | 6 in-betweens (jog cycle repeat) |
| 2 Dive into water, gear appears, swim down | 1.5 | 18 | 12 | 6 |
| 3 Underwater rugby: the goal, the ball drops out | 1.25 | 15 | 12 | 3 |
| 4 Ball bounces, becomes a wheel, the cycle grows | 1.25 | 15 | 12 | 3 |
| 5 Ride away into the sunset (perspective) | 1.75 | 21 | 12 | 9 (scale tweens) |
| 6 The beach draws in, throw, Juhu bounces | 1.5 | 18 | 12 | 6 |
| 7 Juhu leaps out, back to the run | 1.25 | 15 | 12 | 3 |

---

## Shared block: paste at the top of every scene prompt

```
STYLE AND CONTINUITY RULES (follow exactly):
- This is a key-frame sheet for a hand-drawn 2D animation, not an illustration.
- Canvas 1536 x 1024, landscape. A grid of 2 rows x 3 columns of SQUARE panels, equal size, thin light-grey gutters. Read left to right, top to bottom.
- Under each panel, in the gutter only, a small frame number (1-6 or 7-12). No other text anywhere.
- Drawing style: clean black ink outline, one even line weight, on plain white. No shading, no hatching, no colour, no gradients, no textures, no shadows except where stated.
- Simple, semi-realistic figures (not cartoon, not stick figures). Real human and dog proportions.
- LOCKED CAMERA: the camera does not move, zoom or tilt between panels unless the scene says so. Every panel is the same view.
- The ground or horizon line is at exactly the same height in every panel unless the scene says it changes.
- Characters keep the same size from panel to panel unless the scene says they move away.
- Only ONE Tony and ONE Juhu in any panel. Never draw the same character twice in a panel.
- Panels are evenly spaced in time. Show slow-in and slow-out with spacing: poses close together near holds, far apart in fast moves.
- Use the attached model sheet for how Tony and Juhu look. Tony has short dark hair and NO cap or hat.
- Juhu is a German Shepherd: tall pointed ears, long muzzle, deep chest, long bushy tail.
- Leave empty space around the action. Nothing touches the panel edges unless it is entering or leaving.
```

## Prompt 0: model sheet (run once)

```
[paste the shared block]

Make a CHARACTER MODEL SHEET instead of key frames. Canvas 1536 x 1024, white background, black clean outline.
Top row: Tony (from the attached photo) in 5 poses: side view standing, side view jogging (contact pose), side view jogging (passing pose), 3/4 back view, front view. Same scale for all 5. Tony is about 7.5 heads tall, short dark hair, no cap, T-shirt and shorts.
Bottom row: Juhu (from the attached photo), a German Shepherd, in 5 poses: side view standing, side view trotting, side view mid-gallop (all four feet off the ground), crouched to jump, front view sitting. Same scale; Juhu's back is at the height of Tony's hip.
Draw a thin horizontal ground line under each row. Label nothing.
```

## Scene 1: run, Juhu leaps onto Tony's back, Tony pitches forward

```
[paste the shared block]
Attach (only in a new chat): model sheet.

SCENE 1, sheet A (frames 1-6). Side view, camera at waist height, locked. Tony jogs in place at the centre of the panel, facing right (the world moves, not Tony). Ground line at 78% of panel height, with three small ground dashes that move a little to the left in each panel to show travel.
1: Tony, jog contact pose (right heel touching down). Juhu small at the far left edge, galloping in from the left, facing right.
2: Tony, jog passing pose. Juhu closer, mid-gallop, all four feet off the ground.
3: Tony, jog contact pose (left foot). Juhu just behind Tony, CROUCHED low on her back legs (anticipation), ears forward.
4: Tony, passing pose, unaware. Juhu LEAPS: body stretched long and diagonal, front paws reaching for Tony's shoulder blades, tail streaming behind.
5: Juhu's front paws land on Tony's upper back. Tony's upper body jolts forward (head ahead of hips), arms fly back, surprised.
6: Tony tips further forward, hips over the front foot, one leg kicking up behind. Juhu pushes off his back and starts an arc up and to the right.

SCENE 1, sheet B (frames 7-12). Same camera.
7: Tony leaning 45 degrees forward, both arms swinging forward to catch himself. Juhu above and ahead, an arc over his head, legs tucked.
8: Tony's feet leave the ground; the body becomes a shallow forward dive shape, arms reaching forward. Juhu at the top right, leaving the panel.
9: The ground line starts to ripple into gentle waves under Tony's hands. Juhu gone.
10: Tony in a full stretched dive, horizontal, arms together pointing forward and down. The line under him is now a wavy water surface.
11: Tony's hands and head break the water surface: a small crown splash (5-6 short curved strokes). Body still above, angled down.
12: Only Tony's legs above the surface, splash rising, ripples spreading. (This frame is frame 1 of scene 2.)
```

## Scene 2: under the surface, gear appears, swim down

```
[paste the shared block]
Attach (only in a new chat): model sheet, scene1-B.png.

SCENE 2, sheet A (frames 1-6). Start EXACTLY from frame 12 of the attached scene 1 sheet. The camera then sinks: the water surface line moves UP the panel in each frame. This is the only camera move, and it is smooth.
1: Same as scene 1 frame 12: legs above the surface, splash.
2: Whole body just under the surface, a trail of bubbles, the surface line now at 30% panel height.
3: Surface line at 15%. Tony angled 30 degrees down, gliding. A snorkel mask and goggles start to appear on his face (drawn half-finished).
4: Surface line at the top edge. Snorkel and goggles complete, long fins appearing on his feet. A small round ball appears in his right hand.
5: No surface visible, only a few rising bubbles. Tony kicks with the fins (one up, one down), going down to the right.
6: Fins in the opposite kick. A low pool floor line appears at 85% panel height, and a small round underwater rugby basket (metal bucket on a short stand) sits on the floor at the right.

SCENE 2, sheet B (frames 7-12). Locked camera now.
7-10: Tony swims down towards the basket with an alternating fin kick, ball held forward in the right hand, body getting more head-down. Bubbles rise from the snorkel. Spacing: a little bigger in each frame (speeding up).
11: Tony right above the basket, arm pulled back holding the ball (anticipation for the push).
12: Arm pushing forward, ball leaving his hand towards the basket opening. (Frame 1 of scene 3.)
```

## Scene 3: underwater rugby goal, the ball drops into a new dry frame

```
[paste the shared block]
Attach (only in a new chat): model sheet, scene2-B.png.

SCENE 3, sheet A (frames 1-6). Same underwater camera as scene 2 frame 12.
1: Same as scene 2 frame 12.
2: Ball in the basket opening, slightly squashed against the rim. Tony's fins kick as he pushes away.
3: GOAL: the ball drops into the basket. Tony's free arm punches up in celebration, bubbles burst around him.
4: Tony swims up and out of the top of the panel (only legs and fins visible). The ball sinks through the basket.
5: Tony gone. The ball comes out of the BOTTOM of the basket and keeps falling. The basket and pool floor start to fade (draw them with broken, dotted lines).
6: Only the ball, falling in empty white space, motion lines above it.

SCENE 3, sheet B (frames 7-12). The camera follows the ball down into a dry world.
7: The ball is falling, slightly stretched vertically. A new flat ground line draws in from the left at 78% panel height.
8: The ball just above the ground, more stretched.
9: The ball HITS the ground: strongly squashed into a wide oval.
10: The ball bounces up, stretched vertically, moving right.
11: Top of the bounce, round, at 50% of the drop height.
12: The ball coming down for the second bounce. (Frame 1 of scene 4.)
```

## Scene 4: second bounce, the ball becomes a wheel, the cycle grows out of it

```
[paste the shared block]
Attach (only in a new chat): model sheet, scene3-B.png.

SCENE 4, sheet A (frames 1-6). Locked side view, ground line at 78%.
1: Same as scene 3 frame 12.
2: Second, smaller squash on the ground.
3: A small bounce, and the ball starts to grow.
4: The ball lands and rolls to the left of centre, now three times bigger, with spokes faintly appearing inside it.
5: It is clearly a bicycle REAR wheel (tyre, hub, 6 spokes), the same size as a real bike wheel next to Tony's height.
6: From the rear hub, the bicycle frame draws itself forward: chain stay and seat tube (half-finished lines).

SCENE 4, sheet B (frames 7-12). Same camera.
7: The front wheel draws on; the complete bicycle frame, a simple road bike, side view, facing right.
8: Tony's legs appear on the pedals (drawn from the feet up), cranks at 3 o'clock / 9 o'clock.
9: Tony's whole body, seated, hands on the handlebars, cranks at 12 / 6.
10: Tony pedalling (cranks at 3 / 9, the other leg), the bike starting to move right.
11: Pedalling, rolling right, a slight lean forward.
12: Tony and the bike at the right of centre, ready to turn into the road. (Frame 1 of scene 5.)
```

## Scene 5: ride away into the sunset (strict one-point perspective)

```
[paste the shared block]
Attach (only in a new chat): model sheet, scene4-B.png.

SCENE 5. STRICT ONE-POINT PERSPECTIVE. This scene must feel DEEP, not flat.
- One vanishing point at the centre of the setting sun, which sits ON the horizon line.
- Horizon line at 40% of panel height, the same in every panel. The sun is a half circle on the horizon, at 60% of panel width.
- A road with two edges that start wide at the bottom edge of the panel and converge EXACTLY to the vanishing point, with one gentle S-bend. Both road edges and a dashed centre line meet at the vanishing point. The road is the same in every panel.
- The bicycle always sits ON the road's centre line, both wheels touching the road surface.
- SCALE: Tony and the bike shrink quickly as they ride away. Height of Tony plus bike, as a % of panel height: 1: 60%, 2: 46%, 3: 35%, 4: 27%, 5: 20%, 6: 15%, 7: 11%, 8: 8%, 9: 5.5%, 10: 3.5%, 11: 2%, 12: a dot inside the sun.
- VIEW TURNS with the road: 1-2 side view (moving right), 3-4 three-quarter back view as he turns into the road, 5-12 back view (we see Tony's back and the rear wheel), following the S-bend, always pointing at the vanishing point.
- Tony pedals in every panel (alternate the leg positions).

Sheet A = frames 1-6, sheet B = frames 7-12, same layout. Frame 1 matches scene 4 frame 12, with the road and the horizon drawing on behind him (frame 1: road edges half drawn, frame 2: complete).
```

## Scene 6: the beach draws in, Tony throws the frisbee, Juhu bounces

```
[paste the shared block]
Attach (only in a new chat): model sheet, scene5-B.png.

SCENE 6, sheet A (frames 1-6). The camera stays on the horizon and sun from scene 5 (horizon at 40%).
1: Same as scene 5 frame 12: the cyclist is a dot in the sun.
2: The road fades (broken lines). Four short wave lines appear on the sea between the horizon and 55% height.
3: A curved shoreline draws in at 62%; a flat sand line at 85%.
4: Tony walks in from the left on the sand, side view, facing right, at the SAME SCALE as in scene 1 (Tony = 55% of panel height). Juhu trots next to him, ahead and to the right.
5: Tony stops at 35% of panel width, a frisbee in his right hand. Juhu turns towards him, front paws bouncing up (excited), tail high.
6: Tony WINDS UP for a backhand throw: frisbee arm across his chest, shoulders twisted away, knees bent (anticipation). Juhu crouched, staring at the frisbee, tail wagging (draw the tail in a new position).

SCENE 6, sheet B (frames 7-12). Same camera.
7: Wind-up at its extreme: a short hold, very close to frame 6.
8: Throw: the arm whips forward, body untwisting, frisbee leaving the hand. Juhu springs up.
9: Follow-through: the throwing arm extended to the right, Tony's weight on the front foot. The frisbee flies up and right, tilted. Juhu bounces on her back legs.
10: Tony relaxing. The frisbee higher and smaller. Juhu lands, crouches deep (anticipation for the chase).
11: Juhu launches into a gallop to the right, body stretched, all four feet off the ground.
12: Juhu in full gallop at 70% of panel width; Tony watching, hand shading his eyes. (Frame 1 of scene 7.)
```

## Scene 7: Juhu leaps out after the frisbee, back to the run (the loop join)

```
[paste the shared block]
Attach: scene1-A.png (so that the last frame matches the first frame). In a new chat, also attach the model sheet and scene6-B.png.

SCENE 7, sheet A (frames 1-6). Same beach camera.
1: Same as scene 6 frame 12.
2: Juhu's gallop, gathered pose (all four legs under her body).
3: Juhu LEAPS for the frisbee: body stretched long and up, front legs reaching, tail streaming.
4: Juhu at the top right, catching the frisbee in her mouth, about to leave the panel. Tony turns to jog after her.
5: Juhu gone. Tony jogging right. The sea, shoreline and sun start to fade (broken lines).
6: Only Tony jogging, the horizon line fading, the sand line staying.

SCENE 7, sheet B (frames 7-12). The scene turns back into scene 1's camera. Tony moves to the panel centre and stays there (the world moves).
7: Tony jog contact pose at the centre; only the ground line at 78%.
8: Passing pose; ground dashes appear.
9: Contact pose (other foot).
10: Passing pose.
11: Contact pose; Juhu appears tiny at the far left edge, galloping in.
12: MUST MATCH scene 1 frame 1 exactly (same Tony pose, Juhu at the left edge) so the loop joins without a jump.
```

## Prompt S: the silhouette pass (run after every sheet, in the same chat)

```
Redraw the sheet you just made, IDENTICAL in every way: same grid, same poses, same positions, same sizes, same frame numbers. Only change the drawing style to flat colour silhouettes for tracing:
- Tony: solid pure black (#000000) filled shape, including the hair. Draw his snorkel, mask and fins as part of his black shape.
- Juhu: solid pure blue (#0040FF) filled shape.
- Props (ball, basket, bicycle, frisbee, sun): solid pure red (#FF0000) filled shapes. Bicycle wheels are red rings with white inside.
- World lines (ground, water surface, horizon, road, shore, waves, splash, bubbles, motion lines): thin pure green (#00A000) lines.
- Background pure white. No outlines, no shading, no anti-aliasing halos if possible, no text except the frame numbers in grey.
Where Tony and Juhu overlap, Juhu (blue) is in front if she is closer to the camera, otherwise Tony (black) is in front.
```

## Checklist for each sheet before saving
- 6 square panels, numbered, nothing outside the panels except the numbers.
- One Tony and one Juhu per panel. Tony has no cap. Juhu is clearly a German Shepherd.
- The ground or horizon line is at the same height across panels (except scene 2's camera sink and scene 3's drop).
- Frame 1 matches the previous scene's frame 12.
- Scene 5: the road edges really meet at the sun, and the bike is on the centre line and getting smaller each panel.
- If one panel is wrong, ask ChatGPT to "redo only panel N, keep everything else identical", rather than regenerating the whole sheet.

---

## After the sheets exist (next session, not part of this step)
1. **Slice and trace:** `hero/tools/v3/sheets.py` splits each silhouette sheet into its panels, separates the layers by colour, and traces outlines with `pencil.split_contour`.
2. **Build:** `film4.py` lays out each scene as drawings on twos, and morphs outlines where a scene needs more drawings. This reuses the morph and draw-on fixes from the draft 2 review (one Tony at a time, sequential draw-on, holds, no double circle).
3. **Encode** as in draft 2, then review on the page.
