import json,re,unicodedata,fitz,os
DECK='/Users/alexlinehan/Documents/Nextstepuni-Certle/scripts/markbank/authored/applied-maths.json'
PAPERS='/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/exampapers'
cards=json.load(open(DECK))
def norm(s):
    s=unicodedata.normalize('NFKC',s or '')
    s=re.sub(r'([A-Za-z])\1',r'\1',s)
    return re.sub(r'[^0-9a-zA-Z]+',' ',s).strip().lower()
paper={}
for yr in (2021,2022):
    for lvl,code in (('higher','ALP'),('ordinary','GLP')):
        fid=f'LC020{code}000EV.pdf'
        p=os.path.join(PAPERS,str(yr),fid)
        if not os.path.exists(p): print('MISSING',p); continue
        d=fitz.open(p)
        paper[(yr,lvl)]=norm('\n'.join(d.load_page(i).get_text() for i in range(d.page_count)))
        print('loaded',yr,lvl,fid,len(paper[(yr,lvl)]),'chars')
print()
found=[]
for c in cards:
    key=(c.get('year'),c.get('level'))
    if key not in paper: continue
    txt=paper[key]
    hits=[]
    for r in c.get('rows',[]):
        g=r.get('group') or {}
        opts=g.get('options') or []; steps=g.get('perOptionSteps') or []
        for i,o in enumerate(opts):
            no=norm(o)
            if len(no)<10: continue
            if no in txt:
                hits.append((i,o,steps[i] if i<len(steps) else None))
    if hits:
        sums=[sum(r['group']['perOptionSteps']) for r in c.get('rows',[]) if (r.get('group') or {}).get('perOptionSteps')]
        found.append((c['id'],c.get('questionRef'),c.get('totalMarks'),sums,hits))
print('cards whose OPTIONS contain verbatim PAPER text:',len(found))
for cid,ref,tot,sums,hits in found:
    print(f'--- {cid}  {ref}  totalMarks={tot}  stepSums={sums}')
    for i,o,m in hits: print(f'      opt{i} marks={m} :: {o[:95]}')
