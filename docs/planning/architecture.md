---
name: Portfolio refresh
type: architecture-spine
purpose: build-substrate
altitude: feature
paradigm: static single page, progressive enhancement
scope: index.html, style.css, images/
status: draft
created: 2026-10-20
updated: 2026-10-20
binds: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-9]
sources: [prd.md, ux-spec.md]
---

# Architecture spine: portfolio refresh

## Design paradigm
Static single page with progressive enhancement. HTML carries all content. CSS carries layout and motion. One inline script adds motion only. If the script fails, the page is complete.

## Invariants and rules

### AD-1: No build step [ADOPTED]
- **Binds:** all
- **Prevents:** tooling drift on a one-page site.
- **Rule:** Files in the repo are the files GitHub Pages serves. Image processing is a one-time script run by hand, not part of deploy.

### AD-2: Motion is opt-in by JavaScript
- **Binds:** FR-3, FR-5
- **Prevents:** content that stays hidden when the script fails.
- **Rule:** The script adds class `js` to `<html>` first. Hidden-before-reveal styles apply only under `.js`. Elements above the viewport at load time, or after a jump, get `is-visible` at once.

### AD-3: Icons and footer art are inline SVG
- **Binds:** FR-4, FR-6
- **Prevents:** `fetch` failures on `file://` and an extra network request per icon.
- **Rule:** Help icons and the footer landscape live inline in `index.html`. Strokes use `currentColor`. The `images/illustrations/*.svg` files stay as sources only.

### AD-4: Draw-on is chained to reveal
- **Binds:** FR-4
- **Prevents:** an icon that draws while its parent is still at 0 opacity.
- **Rule:** One IntersectionObserver handles reveal. When a help item becomes visible, its icon draws after the fade (480 ms). A per-icon `busy` flag blocks replay until the draw ends.

### AD-5: Images are WebP at 2x display size
- **Binds:** FR-1, FR-2
- **Prevents:** multi-megabyte thumbnails.
- **Rule:** One `.webp` per image, width = 2x the largest CSS width (work 560 px, talk 880 px, portrait 320 px). Quality 78. Large originals are removed from the served tree (they stay in git history).

### AD-6: Footer is two SVG layers
- **Binds:** FR-6
- **Prevents:** stretched figures, or a ground line that stops short.
- **Rule:** Layer 1 is a full-width SVG with `preserveAspectRatio="none"` and `vector-effect: non-scaling-stroke`, which holds only the ground line. Layer 2 is the figure SVG, centered, with the default aspect ratio. The ground in layer 1 meets layer 2's ground at the same y within the band.

## Consistency conventions

| Concern | Convention |
|---|---|
| CSS naming | BEM, as today (`block__element--modifier`). |
| New tokens | Add to `:root`. No raw hex outside `:root`, except image backdrops. |
| Script | ES5-safe, IIFE, no dependencies, as today. |
| Images | `images/<name>.webp`, with `width`/`height` attributes that match the aspect ratio. |

## Stack

| Name | Version |
|---|---|
| HTML / CSS / JS | browser-native |
| GitHub Pages | `.nojekyll`, deploys from `main` |
| Pillow (one-time image script) | 11.3 |
| potrace (one-time vector trace) | 1.16 |

## Structural seed

```text
index.html          # page, inline SVG, inline script
style.css           # layout, motion
images/*.webp       # served images
scripts/            # one-time tools: optimize-images.py, trace-footer.sh (not served at runtime)
docs/planning/      # PRD, UX, architecture, epics, audit report
```

## Deferred
- Responsive `srcset`: one 2x file per image is enough at these sizes.
- Dark mode: out of scope per PRD.
