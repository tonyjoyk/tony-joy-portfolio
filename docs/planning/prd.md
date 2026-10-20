---
title: Tony Joy portfolio — audit and refresh
status: draft
created: 2026-10-20
updated: 2026-10-20
---

# PRD: Portfolio audit and refresh

*Fast path (BMAD `bmad-prd`). Hobby/solo stakes, so this is about two pages. Items marked `[ASSUMPTION]` need Tony's confirmation.*

## 0. Document purpose

This PRD defines one round of work on tonyjoyk.github.io/tony-joy-portfolio. Inputs: Tony's request (2026-10-20), the current `index.html` / `style.css`, and a browser audit of the live page. The UX spec (`ux-spec.md`), the architecture spine (`architecture.md`) and the epics (`epics.md`) build on this file.

## 1. Vision

The portfolio is a quiet, one-page site. It tells a hiring manager or a partner what Tony designs, for whom, and how to reach Tony. The page must load fast on a slow phone connection, because that is the world the work is about. Every part of the page must work: images, animations, links and copy.

## 2. Target user

### 2.1 Jobs to be done
- **Recruiter / hiring manager:** in under a minute, see the type of work, the scale, and the role Tony had.
- **Programme partner (public health, NGO):** see if Tony can help with a sprint, testing or a prototype, and send an email.
- **Tony:** show the side projects that show Tony's taste and curiosity.

### 2.2 Key user journeys
- **UJ-1. Asha, a hiring manager on a train, opens the link on her phone over 4G.** The text shows at once. The work images show in about two seconds, not twenty. She reads the Work rows, taps one talk, and goes back to the email link.
- **UJ-2. Ravi, a programme lead, scrolls to "Ways I can help" on a laptop.** Each icon draws itself one time as Ravi arrives. When Ravi points at an item, the icon draws again. Ravi clicks the email link.
- **UJ-3. A visitor reaches the end of the page.** A line drawing of people and a dog (frisbee, swim, ride, hike, run) goes across the full width of the screen. It ends the page with a light touch.

## 3. Glossary
- **Section** — one of: Intro, Work, Talks, Side projects, Ways I can help, Contact, Footer.
- **Work row** — one project in Work: title, link, role and scale line, description, optional image.
- **Side project row** — one project in Side projects: title, links, one or two sentences.
- **Help item** — one item in Ways I can help: icon, title, one sentence.
- **Reveal** — the fade-up motion that shows a row when it comes into view.
- **Draw-on** — the motion that draws the strokes of a line icon.
- **Footer landscape** — the line drawing at the end of the page.
- **Page weight** — total bytes the browser downloads for one full page view.

## 4. Features

### 4.1 Fast images
**Description:** All raster images are resized to at most 2x their display size and saved in a modern format. Realizes UJ-1.

#### FR-1: Right-sized images
The site serves each image at no more than 2x its largest display width.
- Total image bytes for one full page view are below **600 KB** (now about 18 MB).
- No single image is larger than **150 KB**.
- Images below the first screen load lazily. The portrait loads at once.

#### FR-2: Original files stay safe
The original high-resolution files are not deleted. They move out of the deployed folder or stay in git history. `[ASSUMPTION: git history is enough as the archive; we can delete the large originals from the working tree.]`

### 4.2 Reliable motion
**Description:** Reveal and draw-on run every time, in every way a visitor reaches content. Realizes UJ-2.

#### FR-3: Content is never stuck hidden
- If JavaScript fails or is off, all content is visible.
- If a visitor jumps (anchor link, back button, fast scroll), content above the current view is visible.
#### FR-4: Help icons draw after their item shows
- The icon starts to draw when its help item has faded in, not before.
- Pointing at a help item replays the draw. A replay never starts while a draw is still running.
- Icons work when the file is opened without a server (`file://`).
#### FR-5: Reduced motion is respected
With `prefers-reduced-motion: reduce`, all content shows at once with no motion.

### 4.3 Footer landscape in code
**Description:** The footer PNG becomes vector code (SVG). The ground line runs edge to edge at every screen width. The figures keep their shape and do not stretch. Realizes UJ-3.

#### FR-6: Full-width footer landscape
- The ground line touches the left and right edges of the viewport at 360 px, 768 px, 1440 px and 2560 px wide.
- The figures keep their aspect ratio and stay sharp at every zoom level.
- The footer landscape weighs less than the current PNG (486 KB).
- Optional: the line draws itself one time when the footer comes into view. `[ASSUMPTION: Tony wants a draw-on here, matching the help icons.]`

### 4.4 Side projects update
#### FR-7: Add Walking for Nothing
Add a side project row for Walking for Nothing with its live link and GitHub link.
#### FR-8: No broken links
Every link on the page returns 200, or is removed, or is clearly marked. Today `design-together` and `memorymoments` return 404 (private repos). `[ASSUMPTION: hide the GitHub link but keep the row until the repos are public.]`

### 4.5 Copy in simplified technical English
#### FR-9: Copy follows the house style
All page copy follows ASDSTE100 at about 60–80% strictness (rules in `ux-spec.md` §4). Short sentences, active voice, one idea per sentence, common words, the same term for the same thing. Tony's voice and warmth stay.

### 4.6 Audit report
#### FR-10: Audit report
A written report says what works well and what needs work, across copy, layout, visuals, motion, speed and accessibility, with numbers from before and after.

## 5. Non-goals
- No build tools, frameworks or bundlers. The site stays plain HTML, CSS and a small script.
- No redesign of the visual direction (colour, type, grid stay).
- No new sections beyond the side project.
- No push to `main` until Tony approves the local version.

## 6. MVP scope
**In:** FR-1 to FR-10.
**Out:** talk video links (no URLs yet), CallHub image, side project images, dark mode.

## 7. Success metrics
- **SM-1:** Page weight below 700 KB in total (fonts included). Validates FR-1.
- **SM-2:** Lighthouse performance score of 95+ on mobile. Validates FR-1, FR-6.
- **SM-3:** Zero broken links. Validates FR-8.
- **SM-C1 (counter):** Do not lower image quality until faces or screen text look soft at 2x. Counterbalances SM-1.

## 8. Open questions
1. Which animation did Tony see fail, and on which device or browser?
2. Is the "highlight" line under Simple and DHIS2 (for example "Reducing risk of heart attack and stroke with statins") a link to a case study, or a note? Today it reads as a loose label.
3. Should the talk cards stay as "play" cards with `href="#"` until video links exist?

## 9. Assumptions index
- §4.1 FR-2: git history is enough as the archive for original images.
- §4.3 FR-6: a draw-on for the footer is wanted.
- §4.4 FR-8: keep private-repo rows, hide their dead links.
