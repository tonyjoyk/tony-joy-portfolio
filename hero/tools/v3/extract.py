"""Step 2 of the v3 pipeline: motion extraction.

For every frame of a reference clip, get 33 body landmarks and a person mask with MediaPipe
Pose Landmarker (heavy model, video mode). Writes <out>/track.npz:
  lm    (F, 33, 4)  x, y in source pixels, z, visibility
  mask  (F, H', W') uint8 0..255, downscaled person mask
  fps, size, scale

Usage: .venv/bin/python extract.py footage/stock/pexels-32115632.mp4 work/jog --start 0 --dur 6
"""
import argparse, os
import cv2, numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

ap = argparse.ArgumentParser()
ap.add_argument("clip"); ap.add_argument("out")
ap.add_argument("--start", type=float, default=0); ap.add_argument("--dur", type=float, default=6)
ap.add_argument("--mask-scale", type=float, default=0.5)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

opts = vision.PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=os.path.join(os.path.dirname(__file__), "models/pose_landmarker_heavy.task")),
    running_mode=vision.RunningMode.VIDEO, num_poses=1, output_segmentation_masks=True,
    min_pose_detection_confidence=0.5, min_tracking_confidence=0.5)
det = vision.PoseLandmarker.create_from_options(opts)

cap = cv2.VideoCapture(a.clip)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_MSEC, a.start * 1000)
n = int(round(a.dur * fps))
lms, masks = [], []
for i in range(n):
    ok, bgr = cap.read()
    if not ok: break
    h, w = bgr.shape[:2]
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    r = det.detect_for_video(img, int((a.start + i / fps) * 1000))
    if not r.pose_landmarks:
        lms.append(np.full((33, 4), np.nan)); masks.append(np.zeros((int(h * a.mask_scale), int(w * a.mask_scale)), np.uint8)); continue
    lms.append(np.array([[p.x * w, p.y * h, p.z * w, p.visibility] for p in r.pose_landmarks[0]]))
    m = r.segmentation_masks[0].numpy_view()
    m = cv2.resize(m, None, fx=a.mask_scale, fy=a.mask_scale, interpolation=cv2.INTER_AREA)
    masks.append((np.clip(m, 0, 1) * 255).astype(np.uint8))
np.savez_compressed(os.path.join(a.out, "track.npz"), lm=np.array(lms), mask=np.array(masks),
                    fps=fps, size=(w, h), scale=a.mask_scale)
print(f"{len(lms)} frames at {fps} fps, missing: {sum(np.isnan(l[0,0]) for l in lms)}")
