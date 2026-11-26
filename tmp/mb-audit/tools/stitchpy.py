import json,glob,os,sys
from PIL import Image
OUT='feat'; os.makedirs(OUT,exist_ok=True)
for j in sorted(glob.glob('shots/feat/*.json')):
    base=j[:-5]; name=os.path.basename(base); dst=f'{OUT}/{name}.png'
    if os.path.exists(dst): continue
    d=json.load(open(j)); info=d['info']; segs=d['segs']
    try: first=Image.open(segs[0]['f']).convert('RGB')
    except Exception: continue
    if not info or len(segs)==1: first.save(dst); continue
    W,H=first.size; cssH=844 if '__m_' in name else 800; k=H/cssH
    top=round(info['top']*k); bot=round(info['bottom']*k); sh=round(info['sh']*k)
    out=Image.new('RGB',(W,top+sh+(H-bot)),(255,255,255))
    out.paste(first.crop((0,0,W,bot)),(0,0))
    for s in segs[1:]:
        im=Image.open(s['f']).convert('RGB'); out.paste(im.crop((0,top,W,bot)),(0,top+round(s['y']*k)))
    out.paste(first.crop((0,bot,W,H)),(0,top+sh))
    out.save(dst)
print(len(glob.glob(OUT+'/*.png')))
