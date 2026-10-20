# Tony Joy — Portfolio

Static single-page portfolio. Quiet editorial layout: photo intro, work thumbnails, talks grid, side projects, help grid with animated icons, full-width footer landscape.

No build step. Icons and the footer landscape are inline SVG, so the page also works from `file://`. Fonts load from Google Fonts.

Planning docs (BMAD PRD, UX spec, architecture, epics, audit report) are in `docs/planning/`.

---

## Live site

https://tonyjoyk.github.io/tony-joy-portfolio/

Deployed via GitHub Pages from `main`. Updates automatically on push.

---

## How to view locally

```bash
cd portfolio
python3 -m http.server 8080
```

Open http://localhost:8080.

---

## Files

| Path | Role |
|---|---|
| `index.html` | The page (icons and footer landscape are inline SVG) |
| `style.css` | Layout, typography, motion |
| `index.md` | Plain-text content mirror |
| `favicon.svg` | Tab icon (TJ monogram) |
| `images/simple-app.webp`, `dhis2-app.webp`, `hearts360-dashboard.webp` | Work images |
| `images/*-thumbnail.webp` | Talk thumbnails |
| `images/walking-for-nothing.webp`, `medicine-tracker.webp` | Side project thumbnails (captured from the live sites) |
| `images/design-together.webp`, `memorymoments.webp` | Side project thumbnails (captured from local runs of the private repos) |
| `images/footer-landscape.svg` | Footer landscape source (the frisbee is its own group, so it can float) |
| `images/og-image.jpg` | Social preview image (600×600) |
| `scripts/optimize-images.py` | Resizes images to 2x display width, saves WebP |
| `scripts/build-footer-svg.py` | Traces the footer drawing, adds the full-width ground line, splits out the frisbee |
| `docs/planning/` | BMAD docs: round 1 at the top level, round 2 in `round-2/` |
| `docs/reference/` | Archived design mockups (not loaded by site) |


---

## Design direction

Single content column, max 880px, centered with 32px viewport gutters.

**Grid:** Text column 552px + 48px gap + 280px media column = 880px. Side projects and help grid cap at 552px text measure.

**Type:** Inter for text; IBM Plex Mono for section labels, URLs and metadata. Five sizes, three weights.

**Motion:** Help icons draw on scroll and replay on hover. Light fade-in on rows. Respects `prefers-reduced-motion`.

**Colour:** Off-white `#FAFAF9`, near-black text, warm beige `#EDE9E3` placeholders. No accent colour.

---

## Image mapping

| Section | File | Frame | Crop / fit |
|---|---|---|---|
| Work: Simple | `images/simple-app.webp` | 280×210 (4:3) | `cover`, `42% 38%` |
| Work: DHIS2 | `images/dhis2-app.webp` | 280×210 (4:3) | `cover`, `58% 42%` |
| Work: HEARTS360 | `images/hearts360-dashboard.webp` | 280×210 (4:3) | `contain`, dark `#111` bg |
| Work: CallHub | `images/callhub-app.webp` | 280×210 (4:3) | `cover`, white bg |
| Talks | `images/*-thumbnail.webp` | 160×90 (16:9) | `cover`, `object-position` inline per item |
| Side projects | `images/walking-for-nothing.webp` etc. | 160×120 (4:3) | `cover` |

---

## Adding a talk or side project

Copy an existing `<li class="media-list__item">` in Talks or Side projects. Use the thumbnail `<a>` for the main link (it carries `tabindex="-1"` and `aria-hidden`, because the text link below is the accessible one). A private item uses a `<div>` for the thumbnail and `<span class="meta">Private repo</span>` in place of links.

The VizChitra talk video is private: keep it as "Video on request" (mailto). Do not add its URL to this public repo.

---

## Contact

Email on site: **tonykokkad@gmail.com**

---

## Known dependencies

- `design-together` and `memorymoments` repos are private, so the page shows "Private repo" in place of a link.
- Other project URLs verified 200 when last checked.

---

## Editing

1. Copy → edit `index.html`, keep `index.md` in sync.
2. New images → add the source to `scripts/optimize-images.py`, run it, then add the `.webp` path in HTML + a crop rule in `style.css` if needed.
3. New work row → copy an existing `.work-row` block with `.media-frame--work`.
