---
title: Portfolio refresh — epics and stories
status: done (local, awaiting review)
created: 2026-10-20
sources: [prd.md, ux-spec.md, architecture.md]
---

# Epics and stories

## Epic 1: Fast page (FR-1, FR-2)

### Story 1.1: Convert and resize images
As a visitor on a slow phone, I see images in about 2 seconds.
**Acceptance:**
- Every raster image is a `.webp` at 2x display width (AD-5).
- Total image bytes < 600 KB. No image > 150 KB.
- Crops look the same as before at 1x and 2x.
- `index.html` points to the new files. The old PNGs are removed from the tree.

## Epic 2: Reliable motion (FR-3, FR-4, FR-5)

### Story 2.1: Progressive-enhancement reveal
**Acceptance:**
- Without JS, all content is visible (AD-2).
- After a jump to `#contact`, every row above is visible.
- Reduced motion: no transforms, no transitions.

### Story 2.2: Inline help icons, chained draw-on
**Acceptance:**
- Icons are inline SVG and work on `file://` (AD-3).
- Draw starts after the item fade (AD-4).
- Hover or keyboard focus replays the draw. No replay while a draw runs.

## Epic 3: Footer landscape in code (FR-6)

### Story 3.1: Trace the figures to SVG
**Acceptance:**
- The figure art is a vector SVG, ≤ 60 KB, with no visible loss of detail at 2x.

### Story 3.2: Full-bleed ground line and draw-on
**Acceptance:**
- The ground line touches both viewport edges at 360, 768, 1440 and 2560 px (AD-6).
- Figures keep their aspect ratio.
- The ground draws one time on view. Reduced motion: static.

## Epic 4: Content (FR-7, FR-8, FR-9)

### Story 4.1: Add Walking for Nothing
**Acceptance:**
- New side project row with live site and GitHub links. Both links return 200.

### Story 4.2: Fix dead links
**Acceptance:**
- No link on the page returns 404. Private repos show "Private repo" in place of a link.

### Story 4.3: Copy pass in simplified technical English
**Acceptance:**
- All copy follows `ux-spec.md` §4.
- `index.md` matches `index.html`.

## Epic 5: Audit report (FR-10)

### Story 5.1: Write the audit report
**Acceptance:**
- Covers copy, layout, visuals, motion, speed and accessibility.
- Lists what works well, what was fixed, and what still needs work, with before/after numbers.

## Epic 6: Polish from the audit (audit report items 4, 6, 7, 9, 10)

Keep it simple: CSS and `<head>` changes only. No new scripts, no new sections.

### Story 6.1: Stronger help icons (item 4)
**Acceptance:**
- Icon strokes render at about 1 px or more at 44 px size (`stroke-width` 3 in a 120 viewBox).
- Icons still draw on and replay on hover.

### Story 6.2: Tighter space before the footer (item 6)
**Acceptance:**
- The gap between "Say hi" and the footer is smaller on desktop, but the footer still has room to breathe.

### Story 6.3: No orphan separator on mobile (item 7)
**Acceptance:**
- At 480 px and below, each link in a side project row sits on its own line, and the "·" separator is hidden.

### Story 6.4: Social preview (item 9)
**Acceptance:**
- Open Graph and Twitter card tags with title, description, URL and an image.
- The image is a JPEG (best support across Slack, WhatsApp, LinkedIn), under 100 KB.

### Story 6.5: Favicon (item 10)
**Acceptance:**
- An SVG favicon that matches the site: near-black on off-white, no new colour.

### Not in this epic
- Items 1–3 (current-focus lines, talk videos, which animation failed): need Tony's answers.
- Item 5 (images for CallHub and side projects): needs images from Tony.
- Item 8 (self-host fonts): real gain is small for one page. Deferred to keep the round simple.
