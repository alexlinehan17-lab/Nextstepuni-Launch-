import json, re, unicodedata
P='/Users/alexlinehan/Documents/Nextstepuni-Certle/scripts/markbank/authored/applied-maths.json'
cards=json.load(open(P))
if isinstance(cards,dict):
    print('top keys',list(cards.keys())[:10]); raise SystemExit
def norm(s):
    s=unicodedata.normalize('NFKC',s or '')
    # collapse doubled maths italics
    s=re.sub(r'(.)\1',lambda m:m.group(1) if unicodedata.category(m.group(1))=='Lu' or ord(m.group(1))>0x1D400 else m.group(0),s)
    s=re.sub(r'[^0-9a-zA-Z]+',' ',s).strip().lower()
    return s
print('cards',len(cards))
reprint=[]
for c in cards:
    qt=norm(c.get('questionText','')); st=norm(c.get('stem',''))
    hits=[]
    for r in c.get('rows',[]):
        g=r.get('group') or {}
        opts=g.get('options') or []
        steps=g.get('perOptionSteps') or []
        for i,o in enumerate(opts):
            no=norm(o)
            if len(no)<8: continue
            if (no in qt and qt) or (no in st and st):
                hits.append((i,o,steps[i] if i<len(steps) else None))
    if hits:
        tot=c.get('totalMarks')
        sums=[]
        for r in c.get('rows',[]):
            g=r.get('group') or {}
            if g.get('perOptionSteps'): sums.append(sum(g['perOptionSteps']))
        reprint.append((c['id'],c.get('questionRef'),tot,sums,hits))
print('reprint cards:',len(reprint))
for r in reprint:
    print('---',r[0],r[1],'totalMarks=',r[2],'stepSums=',r[3])
    for i,o,m in r[4]:
        print(f'     opt{i} marks={m} :: {o[:90]}')
