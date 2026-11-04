import sys,fitz
"""Text lines with their y fractions, plus image boxes, for chosen PDF pages (used to set crop regions).
usage: python3 scripts/markbank/agricultural-science-audit/lines.py <pdf> <page> [page...]"""
pdf=fitz.open(sys.argv[1])
for pn in map(int,sys.argv[2:]):
    p=pdf[pn-1];H=p.rect.height;W=p.rect.width
    print(f'--- page {pn}')
    items=[]
    for b in p.get_text('dict')['blocks']:
        if b['type']==1:
            x0,y0,x1,y1=b['bbox'];items.append((y0/H,f'[IMAGE x{x0/W:.3f}-{x1/W:.3f} y{y0/H:.3f}-{y1/H:.3f}]'))
            continue
        for l in b['lines']:
            t=''.join(s['text'] for s in l['spans']).strip()
            if not t: continue
            x0,y0,x1,y1=l['bbox'];items.append((y0/H,f'{y0/H:.3f}-{y1/H:.3f} x{x0/W:.2f} {t[:110]}'))
    for info in p.get_image_info():
        x0,y0,x1,y1=info['bbox'];items.append((y0/H,f'[IMG x{x0/W:.3f}-{x1/W:.3f} y{y0/H:.3f}-{y1/H:.3f}]'))
    for _,s in sorted(items): print(s)
