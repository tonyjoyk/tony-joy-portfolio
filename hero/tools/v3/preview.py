"""Contact sheet of a track's masks, labelled with source frame numbers, for picking time windows.
Usage: .venv/bin/python preview.py work/dive [n=16] -> contact/track-dive.jpg"""
import sys, numpy as np, cv2
from pencil import Track
name = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 16
tr = Track(name)
idx = np.linspace(0, tr.F - 1, n).astype(int)
tiles = []
for i in idx:
    m = cv2.cvtColor(tr.mask[i], cv2.COLOR_GRAY2BGR)
    if tr.has_pose:
        for p in tr.lm[i, [0, 7, 8, 15, 16, 27, 28], :2] * tr.ms:
            cv2.circle(m, tuple(int(v) for v in p), 3, (0, 0, 255), -1)
    h = 220; m = cv2.resize(m, (int(m.shape[1] * h / m.shape[0]), h))
    cv2.putText(m, str(i), (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
    cv2.rectangle(m, (0, 0), (m.shape[1] - 1, h - 1), (80, 80, 80), 1)
    tiles.append(m)
rows = [np.hstack(tiles[k:k + 8]) for k in range(0, len(tiles), 8)]
W = max(r.shape[1] for r in rows)
rows = [np.pad(r, ((0, 0), (0, W - r.shape[1]), (0, 0))) for r in rows]
cv2.imwrite(f"contact/track-{name.rstrip('/').split('/')[-1]}.jpg", np.vstack(rows))
print(tr.F, "frames at", tr.fps, "fps; pose:", tr.has_pose)
