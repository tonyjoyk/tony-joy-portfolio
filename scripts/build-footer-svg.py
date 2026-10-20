"""One-time build of the footer landscape SVG from the hand-drawn PNG.

Traces the drawing with potrace (brew install potrace), then adds ground-line
extensions that run far past both sides, so the line reaches the viewport edges
at any width while the figures keep their aspect ratio.

Run from the repo root:  python3 scripts/build-footer-svg.py <source.png>
Writes images/footer-landscape.svg (inlined into index.html by hand).
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

SRC = Path(sys.argv[1])
OUT = Path("images/footer-landscape.svg")
STROKE = 4    # ground stroke width in art units, measured from the drawing
REACH = 8000  # how far each extension runs past the art, in art units

im = Image.open(SRC).convert("RGBA")
bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
bg.alpha_composite(im)
gray = bg.convert("L")
gray = gray.crop(gray.point(lambda v: 255 if v < 128 else 0).getbbox())
w, h = gray.size

def ground_y(x):
    px = gray.load()
    ys = [y for y in range(h) if px[x, y] < 140]
    return (ys[0] + ys[-1]) / 2

left_y, right_y = ground_y(1), ground_y(w - 2)

with tempfile.TemporaryDirectory() as tmp:
    bmp = Path(tmp) / "art.bmp"
    gray.point(lambda v: 0 if v < 140 else 255).convert("1").save(bmp)
    traced = subprocess.run(
        ["potrace", str(bmp), "-s", "-t", "4", "-a", "1", "-O", "0.6", "-u", "1", "--flat", "-o", "-"],
        check=True, capture_output=True, text=True,
    ).stdout

FRISBEE = (1000, 500, 1240, h)  # art-unit box (potrace's flipped y) that holds only the frisbee
NUM = r"-?\d+(?:\.\d+)?"

transform = re.search(r'<g transform="([^"]*)"', traced).group(1)
d = " ".join(re.findall(r'<path d="([^"]*)"', traced, re.S))
d = re.sub(r"\s+", " ", d)

def subpaths(d):
    """Split potrace path data into subpaths with absolute starts and rough bounding boxes."""
    prev = (0.0, 0.0)
    for s in re.findall(r"[Mm][^Mm]*", d):
        body_at = next(i for i, c in enumerate(s[1:], 1) if c.isalpha())
        x, y = (float(n) for n in re.findall(NUM, s[1:body_at])[:2])
        if s[0] == "m":
            x, y = prev[0] + x, prev[1] + y
        xs, ys, cx, cy = [x], [y], x, y
        for cmd, args in re.findall(r"([clCL])([^clCLzZ]*)", s):
            v = [float(n) for n in re.findall(NUM, args)]
            step = 6 if cmd in "cC" else 2
            for k in range(0, len(v) - step + 1, step):
                ex, ey = v[k + step - 2], v[k + step - 1]
                cx, cy = (cx + ex, cy + ey) if cmd.islower() else (ex, ey)
                xs.append(cx); ys.append(cy)
        prev = (x, y)
        yield (min(xs), min(ys), max(xs), max(ys)), f"M{x:g} {y:g}{s[body_at:].rstrip()}"

def inside(b, box):
    return b[0] >= box[0] and b[1] >= box[1] and b[2] <= box[2] and b[3] <= box[3]

parts = list(subpaths(d))
art = " ".join(s for b, s in parts if not inside(b, FRISBEE))
frisbee = " ".join(s for b, s in parts if inside(b, FRISBEE))
group = (f'<g transform="{transform}" fill="currentColor"><path d="{art}"/></g>\n'
         f'  <g class="landscape__frisbee"><g transform="{transform}" fill="currentColor"><path d="{frisbee}"/></g></g>')

def extension(x0, y0, direction):
    # A few soft swells near the art, then a long flat run to the edge.
    d = [f"M{x0} {y0:.1f}"]
    x, y = x0, y0
    for dx, dy in ((260, -18), (420, 14), (520, -10), (700, 6)):
        nx, ny = x + direction * dx, y0 + dy
        d.append(f"C{x + direction * dx * 0.5:.0f} {y:.1f} {x + direction * dx * 0.5:.0f} {ny:.1f} {nx:.0f} {ny:.1f}")
        x, y = nx, ny
    d.append(f"L{x0 + direction * REACH} {y:.1f}")
    return " ".join(d)

svg = f"""<svg class="landscape" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false">
  <g class="landscape__ground" fill="none" stroke="currentColor" stroke-width="{STROKE}" stroke-linecap="round">
    <path d="{extension(1, left_y, -1)}"/>
    <path d="{extension(w - 2, right_y, 1)}"/>
  </g>
  {group}
</svg>
"""
OUT.write_text(svg)
print(f"{OUT}: {len(svg) // 1024} KB, art {w}x{h}, ground y {left_y:.1f} / {right_y:.1f}")
