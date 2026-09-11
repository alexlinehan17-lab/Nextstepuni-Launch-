import fitz,re,os
BASE='/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/markingschemes'
CELL=re.compile(r'^\(\s*(\d{1,3})\s*\)$')
for yr in (2021,2022):
    for lvl,code in (('ordinary','GLP'),('higher','ALP')):
        p=os.path.join(BASE,str(yr),f'LC020{code}000EV.pdf')
        d=fitz.open(p)
        # locate the two column bands from the data itself
        xs=[]
        for i in range(d.page_count):
            for b in d.load_page(i).get_text('dict')['blocks']:
                if b.get('type')!=0: continue
                for l in b['lines']:
                    t=''.join(s['text'] for s in l['spans']).strip()
                    if CELL.match(t): xs.append(round(l['bbox'][0]))
        xs.sort()
        print(f'\n##### {yr} {lvl}  mark-cell x positions: min={xs[0]} max={xs[-1]}  distinct={sorted(set(xs))[:14]}...')
        TOTCOL=470
        bad=[]
        for i in range(d.page_count):
            cells=[]
            for b in d.load_page(i).get_text('dict')['blocks']:
                if b.get('type')!=0: continue
                for l in b['lines']:
                    t=''.join(s['text'] for s in l['spans']).strip()
                    m=CELL.match(t)
                    if m: cells.append((round(l['bbox'][1],1),round(l['bbox'][0],1),int(m.group(1))))
            cells.sort()
            run=[]
            for y,x,v in cells:
                if x>=TOTCOL:
                    s=sum(run)
                    if s!=v: bad.append((i+1,run[:],s,v,y))
                    run=[]
                else: run.append(v)
            if run: bad.append((i+1,run[:],sum(run),None,None))
        for pg,run,s,v,y in bad:
            print(f'   pdfpage {pg}: steps {run} sum={s}  printed total={v}   <-- MISMATCH' if v is not None and s!=v
                  else f'   pdfpage {pg}: trailing steps {run} sum={s} (part continues / no total on page)')
