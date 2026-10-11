from pathlib import Path
import json,hashlib,copy,re,itertools,fitz
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q6-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q6-';fp='construction-studies-2015-HL-q6-';ap='construction-studies-higher-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 pool=['compact-form','flexible-design','low-maintenance'];pairs=list(itertools.combinations(pool,2));expected={'a':30,'c':10}|{'b-'+k:10 for k in pool};groups={};solutions={'a':'compact','b-compact-form':'compact','b-flexible-design':'flexible-maintenance','b-low-maintenance':'flexible-maintenance'};routes=[]
 for pair in pairs:
  b='b-'+'-and-'.join(pair);expected[b]=20;groups[b]=['b-'+x for x in pair];solutions[b]='scheme'if'compact-form'in pair else 'flexible-maintenance';k='complete-'+'-and-'.join(pair);expected[k]=60;groups[k]=['a',b,'c'];solutions[k]='scheme';routes.append(dict(id=prefix+k,b=list(pair),parts=groups[k],marks=60))
 cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==11 and set(cards)==set(expected)and d['addedIds']==[t['card']['id']for t in d['tasks']]
 bs={b['cardId']:b for b in d['bindings']};assert set(bs)=={c['id']for c in cards.values()}
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])and c['tariffModel']=={'kind':'fixed'}
  assert (c['subjectId'],c['year'],c['level'])==('construction-studies',2015,'higher')and c['questionFigureKey']==fp+'original'and c['sourceMaterial']['pages']==[1,4]
  for x in ['elevation and ground-floor plan','three bedrooms and a bathroom upstairs','timber-frame','rendered concrete-block','maximise solar energy','THREE design features','any TWO','notes and freehand sketches','nearly zero energy buildings']:assert x in c['stem']
  compound=k=='a'or k.startswith('complete-');b=bs[c['id']];nodes=['cons-1-2','cons-6-2','cons-6-4']if compound else ['cons-1-2'];topics=['planning-sustainability-environment','passive-design','heat-loss-insulation']if compound else ['planning-sustainability-environment']
  assert b['questionNumber']=='6'and b['markBankTopicId']==c['topicId']==nodes[0]and b['canonicalTopicIds']==nodes and b['atlasTopicIds']==[ap+x for x in topics]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='6'and t['requiredQuestionFigures']==[fp+'original']
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,4),(S,2),(S,18),(S,19),(S,20),(S,37)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert [g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]]and c['questionText']=='\n\n'.join(cards[s]['questionText']for s in groups[k]);rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
  else:
   assert len(c['rows'])==(3 if k=='a'else 1)
   assert all(r['marks']==10 and r['permittedMarks']==([0,4,6,10]if k=='c'else[0,5,10])for r in c['rows'])
   if k.startswith('b-'):assert 'notes 5 and relevant freehand sketches 5' in c['rows'][0]['contextNote']
  assert c.get('figureKey')==(fp+solutions[k]if k in solutions else None)and t['requiredSolutionFigures']==([fp+solutions[k]]if k in solutions else [])
 for r in cards['a']['rows']:
  for text in ['notes 5','sketch 5','open choices','same feature twice','carbon neutral is not a universal conclusion','kW (power)']:assert text in r['contextNote']
 for s in ['4 marks for a relevant point and 6','not current legal guidance','does not require every building to be off-grid']:assert s in cards['c']['rows'][0]['contextNote']
 assert d['routeLedger']['aOpenFeatures']==3 and d['routeLedger']['bPool']==pool and d['routeLedger']['bChoose']==2 and d['routeLedger']['bPairs']==[list(p)for p in pairs]and d['routeLedger']['wholeRoutes']==routes
 specs={'original':[(P,4,[58,54,568,354])],'compact':[(S,18,[54,54,570,701])],'flexible-maintenance':[(S,19,[54,54,574,450])]};specs['scheme']=specs['compact']+specs['flexible-maintenance'];assert len(d['questionFigures'])==4 and {f['key']for f in d['questionFigures']}=={fp+k for k in specs}
 for f in d['questionFigures']:
  name=f['key'].removeprefix(fp);assert f['panels']==[dict(source=s,page=p,rect=r)for s,p,r in specs[name]]and f['visuallyInspected']and f['renderScale']==2 and f['panelGap']==24 and f['solution']==(name!='original');p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
  if images:
   ims=[]
   for s,page,rect in specs[name]:
    with fitz.open(R/s)as pdf:px=pdf[page-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(rect),alpha=False)
    ims.append(Image.frombytes('RGB',(px.width,px.height),px.samples))
   a=Image.new('RGB',(max(i.width for i in ims),sum(i.height for i in ims)+24*(len(ims)-1)),'white');y=0
   for im in ims:a.paste(im,(0,y));y+=im.height+24
   b=Image.open(p).convert('RGB');assert a.size==b.size and ImageChops.difference(a,b).getbbox()is None
 ledger=d['selectionLedger'];observed=[]
 with fitz.open(R/P)as pdf:
  for i,p in enumerate(pdf):observed.extend((i+1,m.start(),m.group())for m in re.finditer(ledger['pattern'],' '.join(p.get_text().split()),re.I))
 assert observed==[(r['page'],r['start'],r['match'])for r in ledger['rows']]and len(observed)==15 and ledger['unclassified']==0 and all(r['classification']for r in ledger['rows'])
 return dict(tasks=11,wholeQuestionRoutes=3,figures=4,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q6-draft.json').read_text()))))
