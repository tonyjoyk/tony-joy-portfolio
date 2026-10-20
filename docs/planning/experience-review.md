---
title: Experience review and polish plan
status: draft, awaiting Tony's decisions
created: 2026-10-20
method: BMAD bmad-ux (Update, fast path) → bmad-create-epics-and-stories
sources: [prd.md, ux-spec.md, audit-report.md, danielburka.com]
---

# Experience review and polish plan

**Goal:** make the site feel like a lead designer with 10+ years of experience made it. That means simple, intentional, with one or two moments of delight. It is a refinement, not a redesign: same one-page structure, same fonts, same quiet palette.

**Rollback point:** commit `05aacb7` on `main` (pushed 2026-10-20). Everything below comes after it.

---

## 1. What we can learn from danielburka.com

| What it does | Why it feels polished | Use it here? |
|---|---|---|
| A big, calm lede under the name ("Product manager and designer who focuses on…") | One clear statement before any detail. The scale contrast makes the page feel confident. | **Yes.** Make your first sentence the lede. |
| Organisations are inline links in the bio (Hard Problems, Loop Health, MSF) | The bio shows the network and proves it at the same time. | **Yes.** RTSL already does this. Simple and DHIS2 can too. |
| One compact pattern for every list: small thumbnail, bold title, one grey line | Everything feels part of one system. Lists are dense but easy to scan. | **Yes.** Use it for Talks and Side projects. |
| Thumbnails share one visual treatment (pale, light, same size) | No single image shouts. Consistency reads as care. | **Yes.** One tile size and one treatment for all thumbnails. |
| A second column carries the secondary content (writing, interview, books) | Desktop shows twice the content per screen, so there is less scrolling. | **Maybe later.** It is a bigger layout change. See option B in §4. |
| Social icons top right (Medium, Instagram, LinkedIn, Dribbble) | You can reach Daniel from the first screen, without scrolling. | **Yes.** Your site has no LinkedIn or GitHub link today. |
| A "Story" timeline with years | Personality and a career arc in one place. | **Optional.** It needs content from you. |
| One accent colour (sage green) on everything | Memorable, but it is Daniel's signature. | **No copy.** If you want an accent, choose your own (see decision D3). |

What not to take: the very long page (6,700 px) and the serif body text. Your two-font system is already cleaner.

---

## 2. Review of the current site

### Navigation
- **N1. No way to move around.** There are six sections and no navigation. A visitor who wants the talks must scroll past four work rows.
- **N2. No way to reach you until the end.** Email shows only in the last section. There is no LinkedIn or GitHub link at all.
- **N3. Talk cards do nothing.** They say "Video coming soon". You now have two links, and the third can be "on request".

### Scrolling
The page is **4,540 px tall on a 1440 × 900 screen**, which is about 5 screens. Where the height goes:

| Section | Height | Main cause |
|---|---|---|
| Intro | 450 px | 160 px photo, then the bio *below* it |
| Work | 1,150 px | 4 rows, each with a separate URL line and a "Current focus" line |
| Talks | 700 px | 3 large 16:9 cards in a 2-column grid (one card sits alone on row 2) |
| Side projects | 860 px | 4 text rows with long descriptions and wide padding |
| Ways I can help | 300 px | — |
| Gaps between sections | 640 px | 128 px × 5 |

### Polish
- **P1. Too much monospace.** Each work row has two mono lines (URL and meta) before the description. Small mono text in grey reads as noise.
- **P2. The URL line repeats the title.** "Simple" then "simple.org ↗". The title itself can be the link.
- **P3. Icons look hand-drawn and playful.** Stick figures and a lightning bolt at 44 px do not match the calm type. The draw-on motion makes this stronger.
- **P4. Uneven Talks grid.** 3 cards in 2 columns leave a hole.
- **P5. "Current focus" lines.** They are still unclear (open question since the audit).
- **P6. The intro has no lede.** All three bio paragraphs are the same size, so nothing leads.

### What already works (keep)
- The quiet palette, Inter + Plex Mono, the 880 px grid.
- Specific numbers in Work ("5 million patients", "12 screens to 4").
- The footer landscape. It is the one moment of character, and it should stay the signature.
- Fast load (about 270 KB).

---

## 3. Your requests, mapped

| You asked | Plan |
|---|---|
| Remove the photo (optional) | Remove it. The name and lede carry the intro (Story 7.1). |
| Remove the "busy clinics…" line | Remove it (Story 7.1). |
| Less scrolling | Compact lists, merged URL lines, smaller gaps. Target: about 3,200 px, which is about 30% less (Epic 8). |
| Link the talks | DHIS2 and user testing link to YouTube at your timestamps. VizChitra shows "Video on request" and opens an email to you. The VizChitra URL is never published (Story 8.2). |
| Keep private-repo rows | Keep them. They show "Private repo" with no link until you make the repos public (Story 8.3). |
| Images for the 4 side projects | Small thumbnails in one tile style (Story 8.3). I can capture Walking for Nothing and Medicine Tracker from their live sites. Design Together and MemoryMoments need a screenshot from you. |
| Icons less childish | Replace them with a refined line-icon set (Story 9.1). |
| More polish, intention and delight | Epics 7–10 below. |

---

## 4. The plan

### Layout options

**Option A — Refined single column (recommended).** Keep the current layout. Make every section tighter and use one shared list pattern. Lowest risk, biggest polish gain per hour.

**Option B — Two columns on desktop (like Burka).** Intro and Work on the left. Talks, Side projects and Help in a narrower right rail. Even less scrolling (about 2,400 px), but it is a real layout change, and the mobile order needs thought. Do it later, only if A still feels long.

### Epic 7: Intro and navigation
- **7.1 New intro.** Remove the photo and the "busy clinics" line. Line 1 is the lede at about 26 px: *"Hey, I'm Tony, a product designer from Kerala, India."* Line 2, in body size: *"I lead design at Resolve to Save Lives, a public health nonprofit where I design tools and services for healthcare staff."*
- **7.2 Top bar.** Your name on the left. On the right: Work · Talks · Projects · Email · LinkedIn · GitHub, in one quiet row of small text links. It is not sticky. A small "back to top" link goes in the footer.
- **7.3 Section anchors.** Smooth scroll to each section. The heading offsets so it is not hidden at the top of the screen.

### Epic 8: Less scrolling, one list system
- **8.1 Work rows.** The title becomes the link (`Simple ↗`), and the separate URL line goes. One meta line stays in mono. The "Current focus" lines are removed, or folded into the description (decision D4). Row padding goes from 48 to 40 px.
- **8.2 Talks as a list.** A 160 × 90 thumbnail, title, event and year, and a "Watch ↗" link. DHIS2 and user testing open YouTube at the timestamp. VizChitra shows "Video on request ↗" and opens a mailto with a subject line.
- **8.3 Side projects as a list.** The same pattern as Talks: a 120 × 90 tile, title, one-line description, links. Descriptions are cut to one or two short sentences.
- **8.4 Rhythm.** Section gap 128 → 96 px. All thumbnails share the same radius, border hairline and treatment.

### Epic 9: Visual polish
- **9.1 New icons.** Replace the hand-drawn icons with [Phosphor Icons](https://phosphoricons.com) in the "Light" weight (MIT licence, inlined as SVG, 24 px, text colour). Candidates: Timer (sprints), Eye (user testing), CursorClick (prototyping), ArrowsIn (aligning teams). The draw-on motion goes. Option: no icons, with quiet numerals 01–04 in mono instead (decision D2).
- **9.2 Type scale.** Five sizes stay. The lede becomes the largest text after the name. Mono is used only for section labels and meta lines.
- **9.3 Links.** One consistent hover: the underline colour moves from hairline grey to full text colour, and the ↗ nudges. Today, colour changes and underlines differ between rows.
- **9.4 Image treatment.** Thumbnails get a 1 px inner hairline, so pale screenshots don't bleed into the background.

### Epic 10: Delight, kept small
- **10.1 Calmer reveal.** Fade up 8 px over 400 ms, not 12 px over 480 ms. Rows in the same section stagger by 60 ms. The motion feels like settling, not sliding.
- **10.2 Thumbnail hover.** A 2% zoom inside the frame, plus a slightly brighter image. Only on devices that can hover.
- **10.3 Footer as signature.** Keep the centre-out wipe. Add a small touch: on hover over the drawing, the frisbee drifts a few pixels and settles back. Optional, and only if it stays subtle.
- ~~**10.4 Last line.**~~ *Excluded by Tony.* Under the footer drawing, add one small mono line: *"Designed and built by Tony · 2026"*. It is a quiet sign-off. Wording to confirm.

### Expected result

| | Now | After plan A |
|---|---|---|
| Page height at 1440 × 900 | 4,540 px (about 5 screens) | about 3,200 px (about 3.5 screens) |
| Ways to reach you from the first screen | 0 | 3 (Email, LinkedIn, GitHub) |
| Talks that open a video | 0 | 2, plus 1 on request |
| Side projects with an image | 0 | 4 |
| Font families | 2 | 2 |
| Page weight | about 270 KB | about 330 KB (4 small thumbnails added) |

---

## 5. Decisions needed from you

| # | Decision | My recommendation |
|---|---|---|
| D1 | Layout option A or B? | **A** now. Revisit B later. |
| D2 | Icons: Phosphor Light, or no icons with numerals? | **Phosphor Light**. It keeps a visual anchor, with a professional finish. |
| D3 | Add one accent colour? | **No**, stay monochrome. The footer drawing gives the character. If yes, choose a colour with meaning to you (for example the gold of a kasavu border). |
| D4 | "Current focus" lines: remove, or fold into the description? | **Remove**. They add a line per row and nobody has asked about them. |
| D5 | Your LinkedIn URL, and GitHub (github.com/tonyjoyk) for the top bar? | Send the LinkedIn URL. |
| D6 | Screenshots for Design Together and MemoryMoments | Send one image each, any size. I will crop and compress them. |
| D7 | Add the "Story" timeline? | **Not now.** Add it later if you want more personality. |

## 6. Order of work
1. Epic 7 (intro + top bar): fast, and it changes the first impression the most.
2. Epic 8 (lists + less scrolling): the biggest structural gain.
3. Epic 9 (icons, type, links): polish.
4. Epic 10 (delight): last, and only what still feels right.

Each epic ends with a local review on http://localhost:8080 before the next one starts. Nothing is pushed until you approve.
