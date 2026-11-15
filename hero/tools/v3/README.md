# Hero v3 pipeline: real motion → pencil

```
.venv/bin/python extract.py <clip.mp4> work/<name> --start 0 --dur 20   # MediaPipe pose + mask per frame
.venv/bin/python draw.py work/<name> out/<name> --strides 2 --stride-frames 20   # loop, strokes, PNG frames
```
Then encode with ffmpeg (see the commands in the gate hand-over note). Setup:
```
uv venv --python 3.11 .venv && uv pip install --python .venv/bin/python mediapipe opencv-python numpy pillow scipy
curl -L -o models/pose_landmarker_heavy.task https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task
```
`.venv`, `models`, `footage`, `work`, `out`, `contact` are git-ignored.
