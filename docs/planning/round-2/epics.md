---
title: Round 2 — epics and stories
status: done (local, awaiting review)
created: 2026-10-20
method: BMAD bmad-create-epics-and-stories
sources: [prd.md, ux-spec.md, architecture.md]
---

# Epics and stories: round 2

## Epic 7: Intro and navigation (FR-1, FR-2)
- **7.1 New intro.** Remove the photo and the "busy clinics" line. Add the lede.
  *Done when:* the intro is the lede + 1 paragraph, and there is no `<img>` in the header.
- **7.2 Top bar.** `<nav>` with the name, Work, Talks, Projects, Email, LinkedIn and GitHub.
  *Done when:* every link works. At 375 px the bar has no horizontal scroll.

## Epic 8: Less scrolling, one list system (FR-3, FR-4, FR-5, FR-7)
- **8.1 Work rows.** The title is the link. Remove the URL line and "Current focus". Padding 40 px.
- **8.2 Talks list.** `.media-list` with 3 items. Two YouTube links (timestamped), one "Video on request" mailto.
  *Done when:* the VizChitra video URL appears nowhere in the repo (checked before each commit against the private note).
- **8.3 Side projects list.** 4 items with thumbnails: 2 screenshots from the live sites, 2 drawn placeholder tiles.
- **8.4 Rhythm.** Section gap 96 px.
  *Done when:* page height at 1440 × 900 is ≤ 3,400 px.

## Epic 9: Visual polish (FR-6)
- **9.1 Phosphor Light icons.** Timer, Eye, CursorClick, ArrowsIn at 28 px. Remove the draw-on code and the old SVG files.
- **9.2 Links and focus.** One hover style and visible focus rings.

## Epic 10: Delight (FR-8)
- **10.1 Calmer reveal with stagger.**
- **10.2 Thumbnail hover zoom.**
- **10.3 Frisbee float, once.**
- ~~10.4 Sign-off line~~ — removed at Tony's request.
  *Done when:* reduced motion shows a static page with everything visible.
