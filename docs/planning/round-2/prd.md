---
title: Portfolio round 2 — navigation, polish, delight
status: draft
created: 2026-10-20
method: BMAD bmad-prd (Update, fast path)
sources: [../prd.md, ../experience-review.md]
---

# PRD: Round 2

## 1. Vision
The site should feel like Tony made it: a lead designer with 10+ years of work in public health. It should be calm, exact and warm, with one or two small surprises. It must not look like a copy of another designer's site. Tony's own signals lead: the first-person voice, Kerala, the line-drawn landscape, and the side projects.

## 2. Journeys
- **UJ-1. Asha, a hiring manager, opens the link between meetings.** In the first screen, Asha reads who Tony is and where Tony works, and sees how to make contact. Asha jumps to Work from the top bar.
- **UJ-2. Ravi, a programme lead, wants to see Tony speak.** Ravi clicks Talks in the top bar and opens the DHIS2 talk at the right minute.
- **UJ-3. A designer friend scrolls to the end.** The side projects show small pictures. The footer landscape opens and gives a small surprise.

## 3. Requirements

| ID | Requirement | Test |
|---|---|---|
| FR-1 | Remove the photo and the "busy clinics" line. The first sentence is the lede. | The intro is 2 short paragraphs. The lede is the largest text after the name. |
| FR-2 | A quiet top bar: name, section links, email, LinkedIn, GitHub. | Each link works. It is visible in the first screen at 375 px and 1440 px. |
| FR-3 | The work title is the link. Remove the separate URL line and the "Current focus" lines. | No work row has a URL line. |
| FR-4 | Talks show as a compact list. DHIS2 and user testing link to YouTube at Tony's timestamps. VizChitra shows "Video on request". | The VizChitra YouTube URL is not in the repo. |
| FR-5 | Side projects show as the same list, each with a small image. Private repos stay listed as "Private repo". | 4 thumbnails. Private rows have no dead links. |
| FR-6 | Replace the hand-drawn help icons with a refined icon set. | The icons are from one set, one weight, one size. |
| FR-7 | Less scrolling. | Page height at 1440 × 900 is ≤ 3,400 px (now 4,540). |
| FR-8 | Small, intentional delight that is Tony's own. | See UX §5. Every motion has a reduced-motion path. |

## 4. Non-goals
- No two-column layout (option B). Revisit later.
- No accent colour, no new fonts, no dark mode.
- No "Story" timeline.

## 5. Assumptions (Tony did not decide these yet; the recommended choices are used)
- D1: single column. D2: Phosphor Light icons. D3: no accent colour. D4: remove "Current focus". D7: no timeline.
- Design Together and MemoryMoments get drawn placeholder tiles until Tony sends screenshots.
