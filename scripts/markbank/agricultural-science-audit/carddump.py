"""One-line-per-row dump of authored cards with an id prefix.
usage: python3 scripts/markbank/agricultural-science-audit/carddump.py scripts/markbank/authored/agricultural-science.json <id-prefix>"""
import json,sys
d=json.load(open(sys.argv[1]))
for c in d:
    if not c['id'].startswith(sys.argv[2]): continue
    extra=[]
    if c.get('figureKey'): extra.append('fig')
    if c.get('labelKey'): extra.append('labels')
    if c.get('answerVariants'): extra.append('variants:'+','.join(v['id'] for v in c['answerVariants']))
    print(f"===== {c['id']} | {c['questionRef']} | {c['totalMarks']} | {json.dumps(c['tariffModel'])} | {' '.join(extra)}")
    print('  S:',json.dumps(c.get('stem',''),ensure_ascii=False)[:400])
    print('  Q:',json.dumps(c['questionText'],ensure_ascii=False)[:400])
    for r in c['rows']:
        kind=r.get('kind'); 
        if r.get('group'):
            g=r['group']; print(f"   - {kind} {r.get('marks')} GROUP {g.get('kind')} pick={g.get('pick') or g.get('limit')} n={len(g.get('options',[]))} :: "+' / '.join(o.get('verbatim','') if isinstance(o,dict) else str(o) for o in g.get('options',[]))[:300])
        else:
            print(f"   - {kind} {r.get('marks')}  {json.dumps(r.get('verbatim',''),ensure_ascii=False)[:250]} | acc {len(r.get('accept',[]) or [])}")
