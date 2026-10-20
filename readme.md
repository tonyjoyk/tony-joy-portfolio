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
| `index.html` | The page |
| `style.css` | Layout, typography, image crops |
| `index.md` | Plain-text content mirror |
| `images/tony-joy.webp` | Intro portrait |
| `images/simple-app.webp`, `dhis2-app.webp`, `hearts360-dashboard.webp` | Work thumbnails |
| `images/vizchitra-conference-thumbnail.webp`, `dhis2-conference-thumbnail.webp`, `user-testing-thumbnail.webp` | Talk thumbnails |
| `favicon.svg` | Tab icon (TJ monogram) |
| `images/og-image.jpg` | Social preview image (600×600) |
| `images/footer-landscape.svg` | Footer landscape (source; inlined in `index.html`) |
| `images/illustrations/help-*.svg` | Help icon sources (inlined in `index.html`) |
| `scripts/optimize-images.py` | Resizes images to 2x display width, saves WebP |
| `scripts/build-footer-svg.py` | Traces the footer drawing and adds the full-width ground line |
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
| Intro portrait | `images/tony-joy.webp` | 160×160 square | `cover`, face at `center 18%` |
| Work: Simple | `images/simple-app.webp` | 280×210 (4:3) | `cover`, `42% 38%` |
| Work: DHIS2 | `images/dhis2-app.webp` | 280×210 (4:3) | `cover`, `58% 42%` |
| Work: HEARTS360 | `images/hearts360-dashboard.webp` | 280×210 (4:3) | `contain`, dark `#111` bg |
| Work: CallHub | *(missing)* | text-only row | — |
| Talk: VizChitra | `images/vizchitra-conference-thumbnail.webp` | 16:9 | `cover`, `28% center` |
| Talk: DHIS2 | `images/dhis2-conference-thumbnail.webp` | 16:9 | `cover`, `center 38%` |
| Talk: User testing | `images/user-testing-thumbnail.webp` | 16:9 | `cover`, `72% center` |
| Footer | inline SVG | figures max 880px, ground line full width | — |
| Side projects ×3 | *(missing)* | text-only rows | — |

Crop overrides live in `style.css` under `.media-frame--*` modifiers.

---

## Missing assets

| Asset | Notes |
|---|---|
| CallHub work image | Row is text-only until added |
| Side project images | Rows are text-only until added |
| Talk video URLs | Cards show "Video coming soon" until a URL exists |

---

## Talk videos

Talk cards are plain `<div class="talk-card talk-card--pending">` until a video exists. To wire a video:

1. Change the `div` to `<a class="talk-card" href="VIDEO_URL">` (drop `talk-card--pending`).
2. Add `<span class="talk-card__play" aria-hidden="true"></span>` inside the figure and remove the `talk-card__status` line.

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
