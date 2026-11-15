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
ap.add_argument("--mode", choices=["pose", "deeplab", "yolo"], default="pose", help="pose: MediaPipe pose mask (people); deeplab: PASCAL classes (dog, bicycle...)")
ap.add_argument("--classes", default="15", help="deeplab class ids to keep, e.g. 12 for dog, 2,15 for bicycle+person")
ap.add_argument("--maxw", type=int, default=1920, help="downscale wide sources first")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

opts = vision.PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=os.path.join(os.path.dirname(__file__), "models/pose_landmarker_heavy.task")),
    running_mode=vision.RunningMode.VIDEO, num_poses=1, output_segmentation_masks=True,
    min_pose_detection_confidence=0.5, min_tracking_confidence=0.5)
det = vision.PoseLandmarker.create_from_options(opts)
seg = None
if a.mode == "deeplab":
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(os.path.dirname(__file__), "models/deeplab_v3.tflite")),
        output_category_mask=True))
    keep = [int(c) for c in a.classes.split(",")]
yolo = None
if a.mode == "yolo":   # COCO instance masks: 0 person, 1 bicycle, 16 dog, 29 frisbee
    from ultralytics import YOLO
    yolo = YOLO(os.path.join(os.path.dirname(__file__), "models/yolo11x-seg.pt"))
    keep = [int(c) for c in a.classes.split(",")]
    prev = None

cap = cv2.VideoCapture(a.clip)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_MSEC, a.start * 1000)
n = int(round(a.dur * fps))
lms, masks = [], []
for i in range(n):
    ok, bgr = cap.read()
    if not ok: break
    if bgr.shape[1] > a.maxw: bgr = cv2.resize(bgr, None, fx=a.maxw / bgr.shape[1], fy=a.maxw / bgr.shape[1], interpolation=cv2.INTER_AREA)
    h, w = bgr.shape[:2]
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    r = det.detect_for_video(img, int((a.start + i / fps) * 1000))
    if yolo is not None:
        res = yolo(bgr, retina_masks=True, verbose=False, conf=0.25)[0]
        m = np.zeros((h, w), np.float32)
        if res.masks is not None:
            cls = res.boxes.cls.cpu().numpy().astype(int); ms = res.masks.data.cpu().numpy()
            cand = [k for k in range(len(cls)) if cls[k] in keep]
            # per class keep the instance nearest the previous subject (largest on the first frame)
            for c in set(cls[cand]):
                ks = [k for k in cand if cls[k] == c]
                def cen(k): yy, xx = np.nonzero(ms[k]); return np.array([xx.mean(), yy.mean()]) if len(xx) else np.array([1e9, 1e9])
                k = min(ks, key=lambda k: np.linalg.norm(cen(k) - prev)) if prev is not None else max(ks, key=lambda k: ms[k].sum())
                m = np.maximum(m, ms[k])
        if m.sum() > 0: yy, xx = np.nonzero(m); prev = np.array([xx.mean(), yy.mean()])
        m = cv2.resize(m, None, fx=a.mask_scale, fy=a.mask_scale, interpolation=cv2.INTER_AREA)
        masks.append((m * 255).astype(np.uint8))
        lms.append(np.array([[p.x * w, p.y * h, p.z * w, p.visibility] for p in r.pose_landmarks[0]]) if r.pose_landmarks else np.full((33, 4), np.nan))
        continue
    if seg is not None:
        cm = seg.segment(img).category_mask.numpy_view()
        m = np.isin(cm, keep).astype(np.float32)
        m = cv2.resize(m, None, fx=a.mask_scale, fy=a.mask_scale, interpolation=cv2.INTER_AREA)
        masks.append((m * 255).astype(np.uint8))
        lms.append(np.array([[p.x * w, p.y * h, p.z * w, p.visibility] for p in r.pose_landmarks[0]]) if r.pose_landmarks else np.full((33, 4), np.nan))
        continue
    if not r.pose_landmarks:
        lms.append(np.full((33, 4), np.nan)); masks.append(np.zeros((int(h * a.mask_scale), int(w * a.mask_scale)), np.uint8)); continue
    lms.append(np.array([[p.x * w, p.y * h, p.z * w, p.visibility] for p in r.pose_landmarks[0]]))
    m = r.segmentation_masks[0].numpy_view()
    m = cv2.resize(m, None, fx=a.mask_scale, fy=a.mask_scale, interpolation=cv2.INTER_AREA)
    masks.append((np.clip(m, 0, 1) * 255).astype(np.uint8))
np.savez_compressed(os.path.join(a.out, "track.npz"), lm=np.array(lms), mask=np.array(masks),
                    fps=fps, size=(w, h), scale=a.mask_scale)
print(f"{len(lms)} frames at {fps} fps, missing: {sum(np.isnan(l[0,0]) for l in lms)}")
