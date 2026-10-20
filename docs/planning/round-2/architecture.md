---
name: Portfolio round 2
type: architecture-spine
purpose: build-substrate
altitude: feature
paradigm: static single page, progressive enhancement (inherited)
scope: index.html, style.css, images/
status: draft
created: 2026-10-20
binds: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8]
sources: [prd.md, ux-spec.md, ../architecture.md]
---

# Architecture spine: round 2

## Inherited invariants

| Inherited | From | Binds here |
|---|---|---|
| AD-1 No build step | ../architecture.md | Plain HTML, CSS and one inline script. |
| AD-2 Motion is opt-in by JS | ../architecture.md | New motion lives under `.js-motion`. |
| AD-5 WebP at 2x display size | ../architecture.md | New thumbnails: 320 × 240 (projects) and the existing talk files. |
| AD-6 Two-part footer SVG | ../architecture.md | The frisbee float targets one group inside the inline SVG. |

## New rules

### AD-7: One media-list component
- **Binds:** FR-4, FR-5
- **Rule:** Talks and Side projects use the same markup and the same `.media-list` CSS. There are no per-section layout styles.

### AD-8: Icons are inlined Phosphor Light
- **Binds:** FR-6
- **Rule:** Copy the SVG paths from `@phosphor-icons/core@2.1.1` (Light, MIT licence). Use `fill="currentColor"`. No icon font and no CDN request. Remove the draw-on code for help icons.

### AD-9: Private links never enter the repo
- **Binds:** FR-4
- **Rule:** The VizChitra video URL is never written to any file in this repo, because the repo is public. "Video on request" is a `mailto:` link.

### AD-10: Frisbee float is CSS-only
- **Binds:** FR-8
- **Rule:** A `transform` animation on the frisbee group, which runs once after the footer is visible. The frisbee is split from the traced art by its bounding box (see `scripts/build-footer-svg.py`).

## Removed
- The help-icon draw-on JS, and `images/illustrations/` (no longer used).
- `.talk-card*` and `.side-row*` CSS (replaced by `.media-list`).
- `images/tony-joy.webp` (photo removed). `og-image.jpg` stays for link previews.

## Structural seed

```text
index.html     # nav, intro, work, talks, projects, help, contact, footer
style.css      # tokens → base → nav → work → media-list → help → footer → motion
images/        # *.webp (work, talks, projects), footer-landscape.svg, og-image.jpg
scripts/       # optimize-images.py, build-footer-svg.py
```
