"""Preview renderer: draws stroke dictionaries as laterite pencil (same look the p5 engine will use)."""
import math, random
INK = "#A4553A"; BG = "#F6F1E8"

def pencil_paths(strokes, seed=1, w=1.6):
    r = random.Random(seed); out = []
    for name, pts in strokes.items():
        far = "-f-" in name or name.endswith("-f")
        if len(pts) < 2 or max(math.dist(pts[0], p) for p in pts) < 1.5: continue      # collapsed = hidden
        for _ in range(2):
            jx, jy = r.uniform(-.7, .7), r.uniform(-.7, .7)
            d = "M" + " L".join(f"{x + jx + r.uniform(-.35, .35):.1f} {y + jy + r.uniform(-.35, .35):.1f}" for x, y in pts)
            out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w * r.uniform(.8, 1.15):.2f}" stroke-linecap="round" stroke-linejoin="round" opacity="{r.uniform(.62, .92) * (.5 if far else 1):.2f}"/>')
    return "".join(out)

FILTER = ('<filter id="p" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4" result="g"/>'
          '<feDisplacementMap in="SourceGraphic" in2="g" scale="1.3" result="d"/><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="1" seed="8" result="g2"/>'
          '<feColorMatrix in="g2" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.5 1.6" result="m"/><feComposite in="d" in2="m" operator="in"/></filter>')

def svg(strokes, w=600, h=600, seed=1, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{FILTER}</defs>'
            f'<rect width="{w}" height="{h}" fill="{BG}"/><g filter="url(#p)">{pencil_paths(strokes, seed)}</g>{extra}</svg>')
