---
title: Portfolio refresh — UX spec
status: draft
created: 2026-10-20
sources: [prd.md]
---

# UX spec: portfolio refresh

*BMAD `bmad-ux`, fast path. Keeps the current visual direction. Changes only what the PRD needs.*

## 1. Design direction (kept)
- Off-white `#FAFAF9`, near-black text, no accent colour.
- Inter for text, IBM Plex Mono for labels and metadata.
- One column, max 880 px. Text 552 px + 48 px gap + 280 px media.
- Motion is quiet: short fades, line drawing. Nothing bounces.

## 2. Changes by section

| Section | Change | PRD |
|---|---|---|
| Intro | Copy edit only. | FR-9 |
| Work | Smaller images, same crops. Highlight line gets a clear label ("Current focus:"). | FR-1, FR-9 |
| Talks | Smaller thumbnails. Captions edited. | FR-1, FR-9 |
| Side projects | Add **Walking for Nothing** at the top (newest). Hide 404 GitHub links. | FR-7, FR-8 |
| Ways I can help | Icons inline, draw after fade-in, replay on hover or focus. | FR-4 |
| Contact | Copy edit. | FR-9 |
| Footer | Full-bleed line landscape in SVG. | FR-6 |

## 3. Footer landscape

```
|<------------------------------ viewport width ------------------------------>|
 ~~~~~~~~~~~~~~~ ground line (stretches) ~~~~~~[ figures, fixed ratio ]~~~~~~~~~
```

- **Layer 1 — ground:** one SVG path. Its middle part is the hand-drawn ground from the figure art. Its left and right parts are smooth, flat extensions to the viewport edges.
- **Layer 2 — figures:** the traced figures (thrower, dog, frisbee, swimmer, cyclist, hiker, runner). Centered, max width 880 px on desktop, 100% on mobile. They do not stretch.
- Stroke colour uses `currentColor`, so the art follows the text colour.
- Draw-on: the ground line draws left to right one time (about 1.2 s) when the footer comes into view. The figures fade in. Reduced motion: no animation.
- Mobile (< 720 px): figures fill the width. The ground still runs edge to edge.

## 4. Copy style: ASDSTE100 at about 70%

**We apply:**
1. One idea per sentence. Descriptive sentences ≤ 25 words. Instructions ≤ 20 words.
2. Active voice. Name the actor ("I led", "Health workers use").
3. Common words. Prefer "use" to "utilise", "help" to "facilitate", "start" to "initiate".
4. One term for one thing. For example, always "health worker", not also "nurse" or "staff".
5. No idioms, no slang, no rhetorical questions.
6. Numbers as digits with a unit: "5 million patients", not "5m patients".
7. Paragraphs ≤ 3 sentences.

**We relax (to keep it human):**
- Full sentences are not required in metadata lines (role · scale · place).
- First person ("I") is fine and wanted.
- Words outside the STE dictionary are fine when they are the plain word a reader expects (dashboard, prototype, sprint).
- A short, warm closing line is fine ("Say hi").

## 5. Accessibility
- Every motion has a reduced-motion path.
- Help items: replay on `:focus-within` too, not only on hover.
- Talk cards with `href="#"` must not look like working links. They get `aria-disabled="true"` and no play button until a URL exists. `[ASSUMPTION]`
- Text contrast stays at or above 4.5:1. The muted grey `#737373` on `#FAFAF9` is 4.6:1, which passes, but only just. Do not go lighter.
