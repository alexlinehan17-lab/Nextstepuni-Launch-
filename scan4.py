import json,re,unicodedata,fitz,os
DECK='/Users/alexlinehan/Documents/Nextstepuni-Certle/scripts/markbank/authored/applied-maths.json'
PAPERS='/Users/alexlinehan/Documents/Nextstepuni-Launch-/paper-trail-corpus/exampapers'
cards=json.load(open(DECK))
MARK=re.compile(r'\(\s*(?:i{1,3}|iv|vi{0,3}|ix|x|[a-h])\s*\)',re.I)
def norm(s):
    s=unicodedata.normalize('NFKC',s or '')
    s=MARK.sub(' ',s)                                   # drop (i) (ii) (a) markers
    s=re.sub(r'([A-Za-z])\1',r'\1',s)                   # collapse doubled italics
    return re.sub(r'[^0-9a-zA-Z]+',' ',s).strip().lower()
paper={}
for yr in (2021,2022):
    for lvl,code in (('higher','ALP'),('ordinary','GLP')):
        p=os.path.join(PAPERS,str(yr),f'LC020{code}000EV.pdf')
        d=fitz.open(p)
        paper[(yr,lvl)]=norm('\n'.join(d.load_page(i).get_text() for i in range(d.page_count)))
found=[]
for c in cards:
    key=(c.get('year'),c.get('level'))
    if key not in paper: continue
    txt=paper[key]; own=norm(c.get('questionText',''))+' || '+norm(c.get('stem',''))
    hits=[]
    for r in c.get('rows',[]):
        g=r.get('group') or {}
        opts=g.get('options') or []; steps=g.get('perOptionSteps') or []
        for i,o in enumerate(opts):
            no=norm(o)
            if len(no)<10: continue
            src=[]
            if no in txt: src.append('PAPER')
            if no in own: src.append('own-stem/qtext')
            if src: hits.append((i,o,steps[i] if i<len(steps) else None,'+'.join(src)))
    if hits:
        sums=[sum(r['group']['perOptionSteps']) for r in c.get('rows',[]) if (r.get('group') or {}).get('perOptionSteps')]
        found.append((c['id'],c.get('questionRef'),c.get('totalMarks'),sums,hits))
print('2021/2022 cards carrying reprinted QUESTION text as a priced option:',len(found))
for cid,ref,tot,sums,hits in found:
    print(f'--- {cid}  {ref}  totalMarks={tot} stepSums={sums}')
    for i,o,m,src in hits: print(f'      opt{i} marks={m} [{src}] :: {o[:95]}')
