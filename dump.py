import fitz,sys,re
path,idxs=sys.argv[1],sys.argv[2]
d=fitz.open(path)
for i in [int(x) for x in idxs.split(',')]:
    pg=d.load_page(i)
    print(f'===== {path.split("/")[-1]} pdfindex {i} =====')
    for b in pg.get_text('dict')['blocks']:
        if b.get('type')!=0: continue
        for l in b['lines']:
            t=''.join(s['text'] for s in l['spans'])
            if t.strip(): print(f"  x0={l['bbox'][0]:6.1f} y={l['bbox'][1]:6.1f} | {t}")
