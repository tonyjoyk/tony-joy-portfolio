---
title: Portfolio audit report
created: 2026-10-20
status: local changes, not pushed
---

# Portfolio audit report

This report covers the site at tonyjoyk.github.io/tony-joy-portfolio. It says what works well, what this round fixed, and what still needs work. All changes are local on branch `claude/website-access-links-242f2e`. Nothing is pushed.

## Summary

| Area | Before | After |
|---|---|---|
| Page weight (HTML + CSS + images) | about 18.2 MB | about 270 KB |
| Largest image | 8.7 MB (DHIS2 talk thumbnail) | 60 KB |
| Footer art | 486 KB PNG, 520 px wide, centred | 23 KB inline SVG, ground line runs edge to edge |
| Broken links | 2 (private GitHub repos) | 0 |
| Content hidden if the script fails | Yes, all rows | No |
| Help icons without a server (`file://`) | Grey boxes | Work |
| Side projects | 3 | 4 (Walking for Nothing added) |

## What works well

- **Clear structure.** One column, one idea per section. A reader knows who you are and what you do in the first screen.
- **Strong evidence.** Every Work row has role, scale and place. "5 million patients" and "12 screens to 4" are specific and memorable.
- **Quiet visual system.** Two fonts, one grey, no accent colour, hairline rules. Nothing fights the content.
- **Good motion manners.** Motion is short and soft, and it respects reduced-motion settings.
- **Mobile layout.** The grid collapses well at 375 px. There is no horizontal scroll.
- **Contrast.** Body text is near-black on off-white. The muted grey `#737373` passes WCAG AA at 4.6:1.

## What this round fixed

### Speed (Epic 1)
- All 7 photos and screenshots are now WebP at 2x their display size. Total image weight dropped from 17.7 MB to about 210 KB.
- The portrait loads first (`fetchpriority="high"`). The other images load when they come near the view.
- The script is in `scripts/optimize-images.py`. Run it again when you add an image.

### Motion (Epic 2)
I found four problems in the old code. Each one can make an animation look broken:
1. **Hidden content.** CSS hid every row before the script ran. If the script failed or was slow, the rows stayed invisible. Now rows hide only when the script is ready (`.js-motion`).
2. **Rows above a jump stayed hidden.** After an anchor jump or a fast scroll, rows that you skipped stayed invisible when you scrolled back. Now any row above the view shows at once.
3. **Icons drew while invisible.** An icon started to draw while its row was still fading in. Most of the draw happened at low opacity. Now the draw starts after the fade.
4. **Hover restarted a draw.** Pointing at an item during its first draw reset it and caused a stutter. Now a replay waits until the current draw ends.

Also, the icons are now inline SVG. They no longer depend on `fetch`, so they work on `file://`, with no extra requests.

### Footer landscape (Epic 3)
- The PNG drawing is now traced vector code (potrace), filled with `currentColor`.
- The figures keep their shape at every width. The ground line continues with soft swells past both sides of the drawing, to the edges of the screen at any width.
- When the footer comes into view, it opens from the centre to both edges.
- Rebuild it with `scripts/build-footer-svg.py` if you change the drawing.

### Content (Epic 4)
- **Walking for Nothing** is now the first side project, with live site and GitHub links.
- Design Together and MemoryMoments linked to private repos (404). They now say "Private repo".
- Talk cards linked to `#`, which jumped to the top of the page. They now show "Video coming soon" with no play button until a link exists.

### Copy (ASDSTE100, about 70%)
Rules used: one idea per sentence, active voice with a named actor, common words, one term for one thing, numbers as digits. Relaxed: first person, warm closing line, and fragments in metadata lines.

| Before | After |
|---|---|
| Mostly the screens a health worker taps through to register a patient and start treatment. | Most of my work is the screens that health workers use to register a patient and start treatment. |
| …patchy internet, and five minutes per patient. That constraint is the interesting part. | …slow internet, and five minutes for each patient. These limits are the interesting part of the work. |
| 5m patients managed | 5 million patients |
| Cut the patient registration flow from 12 screens to 4, with RTSL and the University of Oslo. | With RTSL and the University of Oslo, I cut patient registration from 12 screens to 4. |
| Built for untrained volunteers in the field, short on time, often in noisy places. | The users were volunteers in the field. Many had no training, little time, and a lot of noise around them. |
| A week to go from a vague problem to something you can test with users. | In one week, we go from an unclear problem to something you can test with users. |
| Aligning product, design and engineering teams / Getting product, design and engineering to agree on what we are building before we build it. | Aligning teams / Product, design and engineering agree on what to build before they build it. (The old title and description said the same thing twice.) |

**Update after review:** Tony rewrote the intro in a warmer, first-person voice ("Hey, I'm Tony…"). The Work descriptions now follow that voice and open by saying what each product is. "Healthcare staff" is now the one term used everywhere, and the location is Kerala.

Spelling is now British throughout ("programmes", "centre"), to match "mobilisation" and "centred".

## What still needs work

**Needs your input**
1. **"Current focus" lines.** Under Simple and DHIS2, the old line ("Reducing risk of heart attack and stroke with statins") had no label, so it read as loose text. I added "Current focus:". If these are case studies, make them links.
2. **Talk videos.** Three talks have no video link. This section is the weakest part of the page until the links exist. The readme has the steps to add them.
3. **Which animation did you see fail?** I fixed the four problems above. If you saw a different one, tell me the browser and what you did.

**Visual**
4. ✅ *Fixed in Epic 6: stroke is now 3.* **Help icons are thin.** At 44 px, the 2-unit stroke renders under 1 px, so the icons look grey and faint next to the text. Try `stroke-width="3"`.
5. **CallHub and side projects have no image.** The page goes text-only for its second half. One small image for Walking for Nothing (a still frame) would add life.
6. ✅ *Fixed in Epic 6: gap reduced.* **Space before the footer.** On desktop there is a large empty gap between "Say hi" and the footer. You can reduce it, or keep it as breathing room.
7. ✅ *Fixed in Epic 6: one link per line under 480 px.* **Link separator wraps on mobile.** On a 375 px phone, the "·" between two links can sit alone at the end of a line. A fix is to put each link on its own line on small screens.

**Technical**
8. **Fonts.** Google Fonts needs two hops before text renders in Inter: first the CSS from one host, then the font files from another. Self-hosting the fonts would remove that chain and the third-party call.
9. ✅ *Fixed in Epic 6: Open Graph tags plus a 600×600 portrait (56 KB JPEG). Check it after the push, because the image URL only works on the live site.* **No social preview.** There are no Open Graph tags, so a shared link shows no image or summary in Slack, WhatsApp or LinkedIn.
10. ✅ *Fixed in Epic 6: "TJ" monogram, near-black on off-white.* **No favicon.**

## How to review locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080. When you are happy, ask me to commit and push. A push to `main` deploys the site.
