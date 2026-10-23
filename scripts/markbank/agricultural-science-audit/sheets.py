import sys,glob,os
from PIL import Image
"""Pair every rendered page of one kind into sheet-<kind>-NN-MM.png for visual review.
usage: python3 scripts/markbank/agricultural-science-audit/sheets.py <dir> exampapers|markingschemes"""
d,kind=sys.argv[1],sys.argv[2]
files=sorted(glob.glob(f'{d}/{kind}-[0-9][0-9].png'))
for i in range(0,len(files),2):
    pair=files[i:i+2]; ims=[Image.open(p) for p in pair]
    H=min(x.height for x in ims); ims=[x.resize((int(x.width*H/x.height),H)) for x in ims]
    c=Image.new('RGB',(sum(x.width for x in ims)+10*(len(ims)-1),H),'#888');x0=0
    for x in ims: c.paste(x,(x0,0)); x0+=x.width+10
    n=[os.path.basename(p)[-6:-4] for p in pair]
    c.save(f'{d}/sheet-{kind}-{"-".join(n)}.png')
print(len(files))
