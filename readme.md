# Tony Joy — Portfolio

Static single-page portfolio. Quiet editorial layout: photo intro, work thumbnails, talks grid, side projects, help grid with animated icons, footer illustration.

Open via a local server (help icons use `fetch` for SVG injection). Fonts load from Google Fonts.

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

Open http://localhost:8080. Do not use `file://` — help icon SVGs use `fetch`.

---

## Files

| Path | Role |
|---|---|
| `index.html` | The page |
| `style.css` | Layout, typography, image crops |
| `index.md` | Plain-text content mirror |
| `images/tony-joy.jpg` | Intro portrait |
| `images/simple-app.png`, `dhis2-app.png`, `hearts360-dashboard.png` | Work thumbnails |
| `images/vizchitra-conference-thumbnail.png`, `dhis2-conference-thumbnail.png`, `user-testing-thumbnail.png` | Talk thumbnails |
| `images/footer-illustrated-image-transparent.png` | Footer illustration |
| `images/illustrations/help-*.svg` | Ways I can help icons (draw-on animation) |
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
| Intro portrait | `images/tony-joy.jpg` | 160×160 square | `cover`, face at `center 18%` |
| Work: Simple | `images/simple-app.png` | 280×210 (4:3) | `cover`, `42% 38%` |
| Work: DHIS2 | `images/dhis2-app.png` | 280×210 (4:3) | `cover`, `58% 42%` |
| Work: HEARTS360 | `images/hearts360-dashboard.png` | 280×210 (4:3) | `contain`, dark `#111` bg |
| Work: CallHub | *(missing)* | text-only row | — |
| Talk: VizChitra | `images/vizchitra-conference-thumbnail.png` | 16:9 | `cover`, `28% center` |
| Talk: DHIS2 | `images/dhis2-conference-thumbnail.png` | 16:9 | `cover`, `center 38%` |
| Talk: User testing | `images/user-testing-thumbnail.png` | 16:9 | `cover`, `72% center` |
| Footer | `images/footer-illustrated-image-transparent.png` | centered ~520px | — |
| Side projects ×3 | *(missing)* | text-only rows | — |

Crop overrides live in `style.css` under `.media-frame--*` modifiers.

---

## Missing assets

| Asset | Notes |
|---|---|
| CallHub work image | Row is text-only until added |
| Side project images | Rows are text-only until added |
| Talk video URLs | Cards link to `#` placeholders; swap when ready |

---

## Talk videos

Talk cards show thumbnails with dark overlay and play button. Each card is a link (currently `href="#"`). To wire a video:

1. Replace `href="#"` with the video URL on the `.talk-card` element.

---

## Contact

Email on site: **tonykokkad@gmail.com**

---

## Known dependencies

- `github.com/tonyjoyk/design-together` and `memorymoments` may 404 until repos are public.
- Other project URLs verified 200 when last checked.

---

## Editing

1. Copy → edit `index.html`, keep `index.md` in sync.
2. New images → add path in HTML + crop rule in `style.css` if needed.
3. New work row → copy an existing `.work-row` block with `.media-frame--work`.
