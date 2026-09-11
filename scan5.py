import json,re,unicodedata,fitz,os
DECK='/Users/alexlinehan/Documents/Nextstepuni-Certle/scripts/markbank/authored/applied-maths.json'
PAPERS='/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/exampapers'
cards=json.load(open(DECK))
MARK=re.compile(r'\(\s*(?:i{1,3}|iv|vi{0,3}|ix|x|[a-h])\s*\)',re.I)
def norm(s):
    s=unicodedata.normalize('NFKC',s or ''); s=MARK.sub(' ',s)
    s=re.sub(r'([A-Za-z])\1',r'\1',s)
    return re.sub(r'[^0-9a-zA-Z]+',' ',s).strip().lower()
def tri(s):
    w=s.split(); return {tuple(w[i:i+3]) for i in range(len(w)-2)}
paper={}
for yr in (2021,2022):
    for lvl,code in (('higher','ALP'),('ordinary','GLP')):
        d=fitz.open(os.path.join(PAPERS,str(yr),f'LC020{code}000EV.pdf'))
        paper[(yr,lvl)]=tri(norm('\n'.join(d.load_page(i).get_text() for i in range(d.page_count))))
rows=[]
for c in cards:
    key=(c.get('year'),c.get('level'))
    if key not in paper: continue
    ptri=paper[key]
    for r in c.get('rows',[]):
        g=r.get('group') or {}
        opts=g.get('options') or []; steps=g.get('perOptionSteps') or []
        for i,o in enumerate(opts):
            t=tri(norm(o))
            if len(t)<2: continue
            ov=len(t&ptri)/len(t)
            if ov>=0.5:
                rows.append((ov,c['id'],c.get('questionRef'),c.get('totalMarks'),
                             sum(steps) if steps else None,i,steps[i] if i<len(steps) else None,o))
rows.sort(reverse=True)
print('option/paper trigram overlap >= 0.5  -> ',len(rows),'options across',len({r[1] for r in rows}),'cards')
for ov,cid,ref,tot,ssum,i,m,o in rows:
    print(f'  {ov:.2f}  {cid:18s} {ref:16s} total={tot} stepsum={ssum} opt{i} marks={m} :: {o[:80]}')
