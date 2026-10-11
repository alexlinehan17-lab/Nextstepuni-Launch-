from pathlib import Path
import json,hashlib,copy,re,fitz
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q7-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q7-';fp='construction-studies-2015-HL-q7-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 expected={'a':52,'b-eaves':4,'b-ridge':4,'b':8,'complete':60};groups={'b':['b-eaves','b-ridge'],'complete':['a','b']};cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==5 and set(cards)==set(expected)and d['addedIds']==[t['card']['id']for t in d['tasks']];bs={b['cardId']:b for b in d['bindings']};assert set(bs)=={c['id']for c in cards.values()}
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])and c['tariffModel']=={'kind':'fixed'}
  assert (c['subjectId'],c['year'],c['level'])==('construction-studies',2015,'higher')and c['questionFigureKey']==fp+'original'and c['figureKey']==fp+'roof-section'and c['sourceMaterial']['pages']==[1,4]
  for s in ['traditional cut roof','45°','6.0 m','400 mm','225 mm × 40 mm','100 mm','25 mm','1:10','500 mm','three courses','four typical','BOTH eaves and roof/ridge']:assert s in c['stem']
  nodes=['cons-3-8','cons-3-9','cons-3-3','cons-4-3','cons-6-2']if k in ['a','complete']else ['cons-3-9','cons-6-5'];topics=['roofs','walls','floors','heat-loss-insulation']if k in ['a','complete']else ['roofs','wood-rot-ventilation']
  if k=='complete':nodes+=['cons-6-5'];topics+=['wood-rot-ventilation']
  b=bs[c['id']];assert b['questionNumber']=='7'and b['markBankTopicId']==c['topicId']==nodes[0]and b['canonicalTopicIds']==nodes and b['atlasTopicIds']==['construction-studies-higher-'+x for x in topics]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='7'and t['requiredQuestionFigures']==[fp+'original']and t['requiredSolutionFigures']==[fp+'roof-section']
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,4),(S,2),(S,21),(S,38)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert [g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]]and c['questionText']=='\n\n'.join(cards[s]['questionText']for s in groups[k]);rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
 assert [(r['marks'],r['permittedMarks'])for r in cards['a']['rows']]==[(40,list(range(41))),(4,[0,4]),(8,[0,2,3,4,6,7,8])]
 for text in ['best TEN','drawing 3 plus annotation 1','TWO of these for ONE 4-mark criterion','all 16','225×40 mm FLOOR joists','200×40 mm ceiling-joist']:assert text in cards['a']['rows'][0]['contextNote']
 for k in ['b-eaves','b-ridge']:assert len(cards[k]['rows'])==1 and cards[k]['rows'][0]['marks']==4 and cards[k]['rows'][0]['permittedMarks']==[0,4]
 assert d['routeLedger']['requiredVentilationLocations']==['eaves','roof/ridge']and d['routeLedger']['wholeRoutes']==[dict(id=prefix+'complete',parts=['a','b'],marks=60)]
 assert len(d['routeLedger']['nonChoices'])==2 and any('fascia/soffit/gutter'in x for x in d['routeLedger']['nonChoices'])
 specs={'original':(P,4,[58,364,571,559],False),'roof-section':(S,21,[92,397,513,787],True)};assert len(d['questionFigures'])==2
 for f in d['questionFigures']:
  assert (f['source'],f['page'],f['rect'],f['solution'])==specs[f['key'].removeprefix(fp)]and f['visuallyInspected'];p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
  if images:
   with fitz.open(R/f['source'])as pdf:px=pdf[f['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(f['rect']),alpha=False)
   a=Image.frombytes('RGB',(px.width,px.height),px.samples);b=Image.open(p).convert('RGB');assert a.size==b.size and ImageChops.difference(a,b).getbbox()is None
 ledger=d['selectionLedger'];observed=[]
 with fitz.open(R/P)as pdf:
  for i,p in enumerate(pdf):observed.extend((i+1,m.start(),m.group())for m in re.finditer(ledger['pattern'],' '.join(p.get_text().split()),re.I))
 assert observed==[(r['page'],r['start'],r['match'])for r in ledger['rows']]and len(observed)==15 and ledger['unclassified']==0
 return dict(tasks=5,wholeQuestionRoutes=1,figures=2,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q7-draft.json').read_text()))))
