import json, re, unicodedata
P='/Users/alexlinehan/Documents/Nextstepuni-Certle/scripts/markbank/authored/applied-maths.json'
cards=json.load(open(P))
def fold(ch):
    # map maths-italic / bold letters back to ASCII
    n=unicodedata.normalize('NFKC',ch)
    return n
def norm(s):
    s=''.join(fold(c) for c in (s or ''))
    s=re.sub(r'([A-Za-z])\1',r'\1',s)          # collapse the doubled-italic wreckage
    s=re.sub(r'[^0-9a-zA-Z]+',' ',s).strip().lower()
    return s
tot_with_groups=0
reprint=[]
for c in cards:
    qt=norm(c.get('questionText','')); st=norm(c.get('stem',''))
    both=(qt+' || '+st)
    hits=[]
    has=False
    for r in c.get('rows',[]):
        g=r.get('group') or {}
        opts=g.get('options') or []
        steps=g.get('perOptionSteps') or []
        if opts: has=True
        for i,o in enumerate(opts):
            no=norm(o)
            if len(no)<6: continue
            if no in both:
                hits.append((i,o,steps[i] if i<len(steps) else None))
    if has: tot_with_groups+=1
    if hits:
        sums=[sum(r['group']['perOptionSteps']) for r in c.get('rows',[]) if (r.get('group') or {}).get('perOptionSteps')]
        reprint.append((c['id'],c.get('questionRef'),c.get('totalMarks'),sums,hits))
print('cards',len(cards),'cards with option groups',tot_with_groups)
print('REPRINT cards:',len(reprint))
for cid,ref,tot,sums,hits in reprint:
    print(f'--- {cid}  {ref}  totalMarks={tot} stepSums={sums}')
    for i,o,m in hits:
        print(f'      opt{i} marks={m} :: {o[:100]}')
