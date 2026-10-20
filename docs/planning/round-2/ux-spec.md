---
title: Round 2 — UX plan
status: draft
created: 2026-10-20
method: BMAD bmad-ux (Update, fast path)
sources: [prd.md, ../ux-spec.md]
---

# UX plan: round 2

## 1. What makes it feel like Tony (and not like someone else)
- **Voice:** first person and warm ("Hey, I'm Tony"). Simplified technical English, at about 70%.
- **Line drawing as the signature.** The footer landscape is Tony's own drawing, so its thin black line becomes the visual motif. The two placeholder tiles use the same line style. No colour, no gradients.
- **Kerala and the outdoors.** The Walking for Nothing frame (a Kerala field) is the warmest image on the page. It goes first in Side projects.
- **Restraint.** Monochrome, two fonts, one column. The polish is in spacing and consistency, not in decoration.

## 2. Page structure (single column, 880 px)

```
[Tony Joy]                         Work  Talks  Projects  Email  LinkedIn  GitHub
Hey, I'm Tony, a product designer from Kerala, India.          ← lede, 28px
I lead design at Resolve to Save Lives, a public health
nonprofit where I design tools and services for healthcare staff.

WORK
Simple ↗                                              [image 280]
Design lead · 5 million patients · 5 countries
Simple is an app that…
───────────────
… (4 rows)

TALKS                          (list: thumb 160×90 · title · event · Watch ↗)
SIDE PROJECTS                  (list: thumb 160×120 · title · links · 1–2 lines)
WAYS I CAN HELP                (2×2, Phosphor Light 28px icons)
Say hi: email →
[footer landscape, full width]
```

## 3. Components

**Top bar.** Name in 15 px semibold. Links in 14 px, muted, with the hover going to full text colour. Not sticky. On mobile, the name sits on its own row and the links wrap below it in one row.

**Work row.** Title link `Simple ↗` (20 px semibold, the underline shows on hover only). One mono meta line, then the description. Padding 40 px.

**Media list (Talks, Side projects).** Grid: thumbnail | text. Gap 24 px, rows 24 px apart, no rules. The thumbnail has a 4 px radius, a 1 px inset hairline, and a placeholder colour behind it.
- Talk text: title (17 px semibold) / event (mono meta) / `Watch at 8:40 ↗` or `Video on request ↗`.
- Project text: title / links (mono meta) / 1–2 sentences.

**Help grid.** Icon 28 px, stroke "Light", in text colour. Title + one line. No draw-on.

## 4. Copy changes
- Lede: "Hey, I'm Tony, a product designer from Kerala, India."
- Remove: "Most of these tools run in busy clinics…"
- Talks:
  - "Building dashboards for hypertension and diabetes care" — VizChitra — Video on request
  - "Designing health programmes around their users" — DHIS2 conference — Watch from 8:40
  - "Fast and simple user testing for digital health tools" — Watch
- Side project descriptions: 1–2 sentences each.

## 5. Delight (small, and Tony's own)
1. **Settle-in reveal.** Rows fade up 8 px over 400 ms. Items in a list stagger by 60 ms.
2. **Thumbnail hover.** The image scales to 1.03 inside its frame over 300 ms. Only on devices that can hover.
3. **The landscape moves once.** The footer wipe from the centre stays. Then the frisbee floats up 6 px and settles, one time only. It is a wink, not a loop.

Reduced motion: no reveal, no zoom, no float. Everything is static and visible.

## 6. Accessibility
- The top bar is a `<nav aria-label="Main">`.
- Every thumbnail has alt text, or `alt=""` when it repeats the title next to it.
- Focus rings are visible on all links (2 px, text colour).
- The muted text colour stays `#737373` (4.6:1).
