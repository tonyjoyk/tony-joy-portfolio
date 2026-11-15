"""Turn Tony's hand-made hero GIF into the site's hero video.

- Flattens the paper texture to white and redraws the lines in laterite, keeping their soft edges.
  On the page the video uses mix-blend-mode: multiply, so it has no visible box (see style.css).
- Removes small stray marks near the bottom edge (frame numbers left over from the key-frame sheets).
- Keeps each frame's own duration (the GIF has holds), and writes WebM + MP4 (BT.709) + a poster.

Usage: .venv/bin/python gif_to_hero.py ~/Downloads/tony-juhu-calm-playful-v3-12fps.gif ../../ --poster 6
"""
import argparse, os, subprocess, tempfile
import cv2, numpy as np
from PIL import Image, ImageSequence

ap = argparse.ArgumentParser()
ap.add_argument("gif"); ap.add_argument("outdir")
ap.add_argument("--poster", type=int, default=6, help="frame index for the still (reduced motion and poster)")
a = ap.parse_args()

# The video is drawn on WHITE and shown with CSS mix-blend-mode: multiply, so white becomes exactly the
# page colour (#F7F5EF) on every screen. The ink is pre-divided by the page colour, so that after the
# multiply it lands on laterite (#A4553A).
PAGE = np.array([247, 245, 239], float); LATERITE = np.array([164, 85, 58], float)
BG = np.array([255, 255, 255], float); INK = np.clip(LATERITE / (PAGE / 255), 0, 255)
L_INK = 0.299 * INK[0] + 0.587 * INK[1] + 0.114 * INK[2]

def clean(rgb):
    px = rgb.astype(float)
    L = 0.299 * px[..., 0] + 0.587 * px[..., 1] + 0.114 * px[..., 2]
    paper = np.percentile(L, 60)                         # most of the frame is paper
    ink = np.clip((paper - L) / (paper - L_INK), 0, 1)   # 0 = paper, 1 = full laterite
    ink = np.clip((ink - 0.12) / 0.78, 0, 1)             # drop the paper grain
    # stray marks: small blobs in the bottom 26% of the frame that are not part of a long line
    H, W = ink.shape
    n, lab, st, _ = cv2.connectedComponentsWithStats((ink > 0.3).astype(np.uint8), 8)
    for k in range(1, n):
        x, y, w, h, area = st[k]
        if y > H * 0.74 and w < W * 0.06 and h < H * 0.08:
            m = cv2.dilate((lab == k).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
            ink[m] = 0
    out = BG * (1 - ink[..., None]) + INK * ink[..., None]
    return out.round().astype(np.uint8)

im = Image.open(a.gif)
tmp = tempfile.mkdtemp()
lines = ["ffconcat version 1.0"]
for i, f in enumerate(ImageSequence.Iterator(im)):
    rgb = np.array(f.convert("RGB"))
    p = os.path.join(tmp, f"f{i:03d}.png"); Image.fromarray(clean(rgb)).save(p)
    lines += [f"file '{p}'", f"duration {f.info.get('duration', 83) / 1000:.3f}"]
    if i == a.poster: Image.open(p).save(os.path.join(a.outdir, "hero-poster.png"))
lines.append(f"file '{p}'")                              # concat demuxer needs the last file twice
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lines) + "\n")

common = ["-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-vf",
          "fps=24,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
          "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
subprocess.run(["ffmpeg", "-v", "error", "-y", *common, "-c:v", "libx264", "-crf", "24", "-preset", "slow",
                "-movflags", "+faststart", os.path.join(a.outdir, "hero-loop.mp4")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *common, "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0",
                os.path.join(a.outdir, "hero-loop.webm")], check=True)
print("frames:", i + 1, "->", a.outdir, "| frames kept in", tmp)
