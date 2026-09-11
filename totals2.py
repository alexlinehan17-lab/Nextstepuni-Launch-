import fitz,re,os
BASE='/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/markingschemes'
CELL=re.compile(r'^\(\s*(\d{1,3})\s*\)$')
for yr in (2021,2022):
    for lvl,code in (('ordinary','GLP'),('higher','ALP')):
        p=os.path.join(BASE,str(yr),f'LC020{code}000EV.pdf'); d=fitz.open(p)
        print(f'\n##### {yr} {lvl}')
        for i in range(d.page_count):
            cells=[]
            for b in d.load_page(i).get_text('dict')['blocks']:
                if b.get('type')!=0: continue
                for l in b['lines']:
                    t=''.join(s['text'] for s in l['spans']).strip()
                    m=CELL.match(t)
                    if m and l['bbox'][0]>300: cells.append((round(l['bbox'][1],1),round(l['bbox'][0],1),int(m.group(1))))
            if not cells: continue
            cells.sort()
            mx=max(c[1] for c in cells)
            tot=[c for c in cells if c[1]>mx-8]
            stp=[c for c in cells if c[1]<=mx-8]
            if not stp:   # whole page is one column -> all steps, part closes elsewhere
                print(f'  pg{i+1:2d}: single column {[c[2] for c in cells]}'); continue
            run=[]; msgs=[]
            for y,x,v in cells:
                if x>mx-8:
                    s=sum(run); msgs.append(('OK' if s==v else 'MISMATCH',run[:],s,v)); run=[]
                else: run.append(v)
            tail=run
            for st,run_,s,v in msgs:
                flag='' if st=='OK' else '   <<<< MISMATCH'
                print(f'  pg{i+1:2d}: steps {run_} sum={s} printed=({v}){flag}')
            if tail: print(f'  pg{i+1:2d}: trailing steps {tail} (part continues)')
