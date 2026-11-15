---
title: Brand refresh — build plan (everything except the hero animation)
status: ready for an agent, pending Tony's assets and the open decisions in §9
created: 2026-11-15
method: BMAD (requirements → UX → architecture → epics and stories)
sources: [brand survey answers (https://claude.ai/artifact/WZEaaKH4LjD2Q1H8D7wND2), ../round-2/*, ../experience-review.md]
---

# Brand refresh: build plan

This plan is for a separate agent. **The hero animation is out of scope.** It is being built in another session (see §8 for how the two pieces of work stay apart).

## 1. Brand rules (decided by Tony)

1. **Calm, not energetic**
2. **Capable, not clever**
3. **Playful, not cool**

Working rule: calm overall, playful in small moments. Nothing fancy. Navigation stays very easy. The site must still signal serious public health work.

## 2. Survey decisions to implement

| Area | Decision |
|---|---|
| Palette | Kerala, muted. Accent: **laterite red**. Subtle touches of the green that grows on laterite rock, used rarely. |
| Type | Friendly sans: **Figtree** for headings and body. Keep IBM Plex Mono for section labels and meta lines. |
| Theme | **Light only.** No dark-mode CSS, no toggle. |
| Top bar | **Sticky.** Stays at the top while scrolling. |
| Pages | **One page**, as now. No new pages. |
| Spacing | As now. |
| Personal vs work | Mostly work (2 of 5). Personal items only where an employer would care. |
| First 10 seconds | "I can trust this person", "That made me smile", "This work matters". |
| Photos | Sprint photos as **loose prints** (slightly tilted, like photos on a table). Lead with the people: it should feel like everyone had a good time. |
| AI work | **Its own section.** Practical tone. Hackathon role "team first" ("We run a monthly AI hackathon. I helped start it."). Comics as a cover image that opens the full comic. |

## 3. Requirements

| ID | Requirement | Done when |
|---|---|---|
| BR-1 | New colour tokens (§5.1). Laterite replaces black only for links, hover, focus and small accents. Body text stays near-black. | All colours come from `:root` tokens. Text contrast is 4.5:1 or more. |
| BR-2 | Figtree replaces Inter. Plex Mono stays for labels and meta. | No Inter left in CSS or the font link. |
| BR-3 | Sticky top bar with a soft background, so text never shows through. | The bar stays visible while scrolling. Anchor jumps do not hide headings under it (`scroll-padding-top`). |
| BR-4 | New section "Working with AI", placed after Work (§4). | The section shows the hackathon, comics, the AI-made report, and one line on BMAD and multi-agent building. |
| BR-5 | Indonesia design sprints, shown with loose-print photos (§4). | It reads as 4 sprints, not 1. Photos lead with people. |
| BR-6 | Keep the page simple. | At most 1 new section. The top bar gets at most 1 new link ("AI"). Page height grows by 900 px or less at 1440 × 900. |
| BR-7 | Light only. | No `prefers-color-scheme: dark` rules. `color-scheme: light`. |
| BR-8 | Reserve the hero slot (§8). | An empty `<div id="hero-animation">` sits right of the intro, about 420 px square on desktop and stacked on phones. It shows a still image until the animation lands. |
| BR-9 | Copy follows the house style (§6). | Reviewed against §6 before showing Tony. |

## 4. Content and page structure

```
Top bar (sticky):  Tony Joy    Work  AI  Talks  Projects | Email  LinkedIn  GitHub
Intro:             lede + RTSL line           [hero animation slot, right]
Work:              Simple · DHIS2 · HEARTS360 · CallHub   (+ sprints, see options)
Working with AI:   hackathon · comics · AI-made report · how we build (BMAD)
Talks
Side projects
Ways I can help
Footer landscape
```

**Working with AI** (new section). This is a draft structure; Tony supplies the facts and assets.
- **Monthly AI hackathon:** 2–3 photos as loose prints. Copy: team first.
- **Comics made with AI:** cover image, and clicking opens the full comic. Two comics, from Tony's Google Drive links. Check that they are shared with "anyone with the link", or ask Tony to download them.
- **A report made with AI:** a title, one line on what it is, and a link or PDF.
- **How we build:** one line on introducing the BMAD method and building with multiple AI agents. Keep it small, and confirm the term "P stack" with Tony before using it.
- Use the media-list pattern (thumbnail + title + one line), like Talks and Side projects. Do not invent a new layout.

**Indonesia design sprints** (Tony to choose):
- **Option A (recommended):** a fifth Work row, with a 3–4 photo loose-print cluster in place of the single image. The meta line says "4 sprints in 1 week · Indonesia".
- **Option B:** inside "Ways I can help" under "Running design sprints", as a small photo strip.

## 5. Design details

### 5.1 Colour tokens (starting point; check contrast)

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#F7F5EF` | Page background (warm, muted) |
| `--text` | `#1F1D1A` | Body text |
| `--muted` | `#6E6A63` | Meta, secondary text (check 4.5:1 on `--bg`) |
| `--laterite` | `#A4553A` | Links, hover underline, focus ring, small accents, the hero animation line |
| `--moss` | `#5E7D5A` | Very rare detail only, for example a tiny "new" mark. Never for text blocks. |
| `--hairline` | `#E3DED3` | Rules and thumbnail borders |
| `--placeholder` | `#ECE6DA` | Image placeholders |

The laterite touches stay subtle and professional: link underlines, the focus ring, section-label colour if it reads calmly, and the animation. No laterite backgrounds or large blocks.

### 5.2 Type
- Figtree 400 / 500 / 700 from Google Fonts. Keep the current five-size scale.
- Mono labels stay uppercase, small and muted.

### 5.3 Loose prints
- 3–4 photos, each with a white border (about 6 px) and a soft shadow, rotated −3° to +3°, slightly overlapping.
- On hover, a print straightens and rises a little (one small playful moment). Turn this off for reduced motion.
- Each photo is WebP at 2× display size and under 60 KB.

### 5.4 Sticky top bar
- The background is `--bg` at about 90 % opacity with a light blur. It gets a hairline bottom border only after scrolling.
- Height about 56 px. On phones, the two link rows stay as they are now.

## 6. Copy rules
- ASDSTE100 simplified technical English at about 60–80 %. Short sentences, active voice, one idea per sentence, common words.
- Use "healthcare staff", never "health workers".
- Write "Kerala, India", in British spelling.
- "Ways I can help" lines start with a verb and contain no "I".
- **Never** put the VizChitra video URL in the repo. It stays "Video on request". (The repo is public.)

## 7. Epics and stories

**Epic A: Foundations**
- A1 Colour tokens and contrast check (BR-1, BR-7).
- A2 Switch fonts to Figtree (BR-2).
- A3 Sticky top bar, plus an "AI" link (BR-3).
- A4 Hero slot, with a still placeholder image (BR-8).

**Epic B: New content**
- B1 Working with AI section using the media list (BR-4).
- B2 Comics: cover thumbnails that open the full comic (link, or a simple lightbox with no new library).
- B3 Loose-print photo component (§5.3).
- B4 Indonesia sprints, as option A or B (BR-5).

**Epic C: Polish and check**
- C1 Copy pass (BR-9).
- C2 Page height and performance check: page weight stays under about 600 KB without the animation.
- C3 Review on desktop and phone, then show Tony on localhost.
- C4 Push only after Tony approves.

## 8. Working alongside the hero animation session

- **The animation session owns:** `hero/` (all files inside it) and the `docs/planning/round-3/hero-*` files.
- **This agent owns:** everything else, including `index.html`, `style.css`, `index.md` and `images/`.
- **The slot:** this agent creates `<div id="hero-animation" class="hero-animation" aria-hidden="true"></div>` right of the intro, with layout CSS only (size, position, stacking on phones). The animation session later adds one `<script>` tag that fills it.
- Work on your own branch or worktree. Do not push to `main` without Tony's approval.

## 9. Needed from Tony before or during the work
1. Hackathon photos (3–5).
2. Comic files, or Drive links shared with "anyone with the link".
3. The AI-made report: title, one line, and a link or PDF.
4. Indonesia sprint photos (6–10 to choose from), and option A or B.
5. What "P stack" means, or the right name to use.
6. Any facts to state: hackathon start date, number of people, what the sprints were about.
