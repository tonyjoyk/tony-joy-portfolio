"""One-time image optimizer. Resizes each source image to 2x its display width and saves WebP.

Run from the repo root:  python3 scripts/optimize-images.py
"""
from pathlib import Path
from PIL import Image

QUALITY = 78
# source file -> target width in px (2x the largest CSS width)
TARGETS = {
    "tony-joy.jpg": 320,
    "simple-app.png": 560,
    "dhis2-app.png": 560,
    "hearts360-dashboard.png": 560,
    "vizchitra-conference-thumbnail.png": 880,
    "dhis2-conference-thumbnail.png": 880,
    "user-testing-thumbnail.png": 880,
}

images = Path("images")
for name, width in TARGETS.items():
    src = images / name
    img = Image.open(src)
    img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    out = src.with_suffix(".webp")
    img.save(out, "WEBP", quality=QUALITY, method=6)
    print(f"{name:40} {src.stat().st_size // 1024:>6} KB -> {out.name:40} {out.stat().st_size // 1024:>4} KB  {img.width}x{img.height}")
