import sys
from PIL import Image, ImageDraw
"""Stack horizontal bands of rendered pages with 0.01 tick marks, to read exact crop boundaries.
usage: python3 scripts/markbank/agricultural-science-audit/band.py out.png img:y0:y1 [img:y0:y1 ...]"""
parts=[]
for spec in sys.argv[2:]:
    path,y0,y1=spec.rsplit(':',2); y0=float(y0); y1=float(y1)
    im=Image.open(path).convert('RGB'); W,H=im.size
    c=im.crop((0,int(y0*H),W,int(y1*H)))
    d=ImageDraw.Draw(c)
    k=int(round(y0*100))
    while k/100<=y1:
        yy=int((k/100-y0)*H)
        d.line([(0,yy),(25,yy)],fill=(255,0,0),width=2); d.text((28,yy-6),f'{k/100:.2f}',fill=(255,0,0))
        k+=1
    parts.append(c)
W=max(p.size[0] for p in parts); H=sum(p.size[1]+10 for p in parts)
out=Image.new('RGB',(W,H),(200,200,200)); y=0
for p in parts: out.paste(p,(0,y)); y+=p.size[1]+10
out.save(sys.argv[1])
