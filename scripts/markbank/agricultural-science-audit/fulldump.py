"""Full dump (rows, accepts, variants, notes) of authored cards with an id prefix.
usage: python3 scripts/markbank/agricultural-science-audit/fulldump.py scripts/markbank/authored/agricultural-science.json <id-prefix>"""
import json,sys
d=json.load(open(sys.argv[1])); pre=sys.argv[2]
for c in d:
    if not c['id'].startswith(pre): continue
    print(f"===== {c['id']} | {c['questionRef']} | {c['totalMarks']} | {json.dumps(c['tariffModel'])} | fig={c.get('figureKey')} labels={bool(c.get('labelKey'))} qfig={c.get('questionFigureKey')}")
    if c.get('stem'): print('  S:',c['stem'][:600])
    print('  Q:',c['questionText'])
    def rows(rs,ind='   '):
        for r in rs:
            g=r.get('group')
            line=f"{ind}- {r.get('kind')} {r.get('marks')} {r.get('verbatim','')!r}"
            if g: line+=f" GROUP{ {k:v for k,v in g.items() if k!='options'} } OPTS="+' || '.join(o if isinstance(o,str) else o.get('verbatim','') for o in g.get('options',[]))
            print(line)
            if r.get('accepts'): print(ind+'   acc: '+' || '.join(r['accepts']))
    rows(c['rows'])
    for v in c.get('answerVariants') or []:
        print('  VARIANT',v['id'],v.get('label')); rows(v['rows'],'     ')
    if c.get('notes'): print('  N:',c['notes'][:300])
