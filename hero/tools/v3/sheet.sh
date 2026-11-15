#!/bin/bash
# usage: sheet.sh <group> <id>...  -> contact/<group>.jpg (8 frames/sec-spaced per clip, labelled)
g=$1; shift; mkdir -p contact/$g
for id in "$@"; do (
  u=$(curl -sIL -A "Mozilla/5.0" "https://www.pexels.com/download/video/$id/" | grep -i '^location:' | tail -1 | tr -d '\r' | awk '{print $2}')
  echo "$id $u" >> contact/$g/urls.txt
  [ -n "$u" ] && ffmpeg -v error -y -i "$u" -t 12 -vf "fps=0.75,scale=200:-2,tile=8x1" -frames:v 1 contact/$g/c$id.jpg
) & done; wait
.venv/bin/python - "$g" <<'P'
import sys, glob
from PIL import Image, ImageDraw
g=sys.argv[1]; fs=sorted(glob.glob(f'contact/{g}/c*.jpg'))
ims=[Image.open(f) for f in fs]; W=1600
ims=[i.resize((W,int(i.height*W/i.width))) for i in ims]
out=Image.new('RGB',(W,sum(i.height for i in ims)),'white'); y=0
for f,i in zip(fs,ims):
    out.paste(i,(0,y)); d=ImageDraw.Draw(out); d.rectangle((0,y,90,y+14),fill='white'); d.text((3,y+2),f.split('/c')[-1][:-4],fill='red'); y+=i.height
out.save(f'contact/{g}.jpg', quality=80)
P
