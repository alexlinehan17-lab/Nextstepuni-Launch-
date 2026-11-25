import json,glob,re
ART=re.compile(r'blank (band|gap)|empty band|large gap|opened blank|blank page',re.I)
MEDIA=re.compile(r'could not be loaded|dead video|recording|audio player|video player',re.I)
SEV={'high':0,'medium':1,'low':2}
feat={};cases=[]
for f in sorted(glob.glob('reviews/*.json')):
    r=json.load(open(f)); s=r['subject']; man={c['n']:c for c in json.load(open(f'review/{s}/manifest.json'))['cards']}
    issues=[i for i in r.get('issues',[]) if not ART.search(i['title']) and not (MEDIA.search(i['title']))]
    if s in('applied-maths',): pass
    issues.sort(key=lambda i:SEV.get(i.get('severity'),3))
    def cardof(img,cards):
        m=re.match(r'(\d+)_',img or ''); n=int(m.group(1)) if m else (cards[0] if cards else None)
        return n if n in man else None
    fi=[]
    for i in issues[:4]:
        n=cardof(i.get('best_evidence_image'),i.get('cards') or [])
        img=i.get('best_evidence_image') or ''
        kind='attached' if 'attached' in img else ('desktop' if 'desktop' in img else 'phone')
        fi.append({**i,'card':n,'evidence_kind':kind})
    ge=[]
    for g in r.get('good_examples',[])[:2]:
        n=g.get('card'); 
        if n in man: ge.append({'card':n,'why':g.get('why','')})
    feat[s]={'issues':fi,'good':ge,'more_issues':[i['title'] for i in issues[4:]]}
    need={x['card'] for x in fi if x['card'] and x['evidence_kind']!='attached'}|{g['card'] for g in ge}
    for n in sorted(need): cases.append({'subject':s,'level':man[n]['level'],'id':man[n]['id'],'n':n})
json.dump(feat,open('featured.json','w'),indent=1,ensure_ascii=False); json.dump(cases,open('featured_cases.json','w'))
print(len(cases))
