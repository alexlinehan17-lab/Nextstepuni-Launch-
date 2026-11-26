import json,glob,os,collections,random,re
random.seed(11)
ts=json.load(open('textsamples.json'))
PRI=['a:pipe_table','q:pipe_table','a:slash_sep','q:repl_char','a:newline_heavy','q:sibling_parts','q:spaced_nums','a:multi_slash','q:newline_heavy','a:flat_fraction','q:dash_run','a:dot_leader','q:dot_leader','q:double_space','a:sibling_parts','a:dash_run']
topq=lambda ref:(re.search(r'Q(\d+)',ref) or [None,None])[1]
cases=[];plan={}
subs=sorted({os.path.basename(f).split('__')[0] for f in glob.glob('decks/*__*.json')})
for s in subs:
    cards=[c for f in sorted(glob.glob(f'decks/{s}__*.json')) for c in json.load(open(f))]
    byid={c['id']:c for c in cards}
    big=len(cards)>=500
    N=12 if big else (8 if len(cards)>=300 else 5)
    def shape(c):
        r=c.get('rubric') or {}
        return (c['kind'],bool(c.get('figure')),bool(c.get('questionFigure')),bool(c.get('sourceMaterial')),bool(c.get('audioMaterial') or c.get('videoMaterial')),bool(c.get('mathematicsScale')),r.get('kind') or r.get('family') or r.get('type') or ('rubric' if r else ''),bool(c.get('questionChoices')),bool(c.get('answerVariants')), min(len(c.get('rows') or []),6)//3)
    groups=collections.defaultdict(list)
    for c in cards: groups[shape(c)].append(c)
    picked=[];why={}
    # suspects
    nsus=4 if big else 1
    for p in PRI:
        if len(picked)>=nsus: break
        for cid,_ in ts.get(s,{}).get(p,[])[:1]:
            if cid in byid and cid not in why: picked.append(byid[cid]); why[cid]='suspect:'+p
    # multi-topic shared page
    pages=collections.defaultdict(list)
    for c in cards:
        sm=c.get('sourceMaterial')
        if sm and not sm.get('regions'):
            for p in sm.get('pages',[]): pages[(sm.get('sourceFileid') or c['paperFileid'],c['year'],c['level'],p)].append(c)
    multi=[cs for cs in pages.values() if len({c['topicId'] for c in cs})>1 and len({topq(c['questionRef']) for c in cs})>1]
    random.shuffle(multi)
    for cs in multi[:2 if big else 1]:
        c=random.choice(cs)
        if c['id'] not in why: picked.append(c); why[c['id']]='shared-page'
    # stratified by shape, biggest shapes first, recent+old mix
    order=sorted(groups.values(),key=len,reverse=True)
    i=0
    while len(picked)<N and i<200:
        g=order[i%len(order)]; i+=1
        c=random.choice(g)
        if c['id'] not in why: picked.append(c); why[c['id']]='shape'
    plan[s]=[]
    for c in picked:
        sm=c.get('sourceMaterial')
        case={'subject':s,'level':c['level'],'id':c['id'],'why':why[c['id']]}
        if sm and sm.get('title') and sm['kind'] not in ('linked-reading','supplementary-text'): case['src']=sm['title']
        cases.append(case); plan[s].append(case)
json.dump(cases,open('cases.json','w')); json.dump(plan,open('plan.json','w'),indent=1)
print(len(cases), sum(1 for c in cases if c.get('src')), {s:len(v) for s,v in plan.items()})
bad=[c['id'] for c in cases if re.search(r'[/\\?%*:|"<>]',c['id'])]; print('awkward ids',bad[:10],len(bad))
