import sys
from PIL import Image, ImageDraw
d, a, b, step = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
fs = list(range(a, b, step)); cols = 8; t = 220
W = Image.new('RGB', (cols * t, ((len(fs) + cols - 1) // cols) * t), 'white')
for k, f in enumerate(fs):
    im = Image.open(f'{d}/f{f:03d}.png').resize((t, t)); ImageDraw.Draw(im).text((4, 4), str(f), fill='blue')
    W.paste(im, ((k % cols) * t, (k // cols) * t))
W.save('contact/film.png')
