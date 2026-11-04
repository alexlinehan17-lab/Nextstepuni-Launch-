"""Render only the named tasks' crop pairs.
usage: python3 scripts/markbank/agricultural-science-audit/render_subset.py <module> <year> <fileid> <out.png> <ref> [ref...]"""
import sys, importlib, fitz, json
from PIL import Image, ImageDraw
sys.path.insert(0,'scripts/markbank/authoring')
mod,year,fileid,out=sys.argv[1:5]; refs=sys.argv[5:]
m=importlib.import_module(mod)
try:
    _,tasks=m.reviewed_tasks()
except TypeError:
    _,tasks,_c=m.reviewed_tasks({c['id']:c for c in json.load(open('scripts/markbank/authored/agricultural-science.json'))})
pdfs={k:fitz.open(f'paper-trail-corpus/{k}/{year}/{fileid}') for k in ['exampapers','markingschemes']}
def strip(regions,kind):
    pieces=[]
    for r in regions:
        p=pdfs[kind][r['p']-1];a,b,c,d=r['r']
        pix=p.get_pixmap(matrix=fitz.Matrix(1.2,1.2),clip=fitz.Rect(a*p.rect.width,b*p.rect.height,c*p.rect.width,d*p.rect.height))
        pieces.append(Image.frombytes('RGB',[pix.width,pix.height],pix.samples))
    cv=Image.new('RGB',(720,sum(x.height for x in pieces)+6*len(pieces)),'white');y=0
    for im in pieces: cv.paste(im,(0,y)); y+=im.height+6
    return cv
rows=[];seen=set()
for t in tasks:
    if not any(t['questionRef'].endswith(' '+r) or (' '+r+' —') in t['questionRef'] for r in refs): continue
    k=json.dumps([t['paperRegions'],t['schemeRegions']])
    if k in seen: continue
    seen.add(k)
    a=strip(t['paperRegions'],'exampapers');b=strip(t['schemeRegions'],'markingschemes');h=max(a.height,b.height)+30
    row=Image.new('RGB',(1460,h),'white');ImageDraw.Draw(row).text((10,5),t['questionRef'],fill='black');row.paste(a,(0,25));row.paste(b,(740,25));rows.append(row)
cv=Image.new('RGB',(1460,sum(r.height+10 for r in rows)),'#ccc');y=0
for r in rows: cv.paste(r,(0,y)); y+=r.height+10
cv.save(out);print(len(rows))
