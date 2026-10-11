from pathlib import Path
import json,hashlib,copy,re
import fitz
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q3-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q3-';fp='construction-studies-2015-HL-q3-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 expected={'a':24,'c':6};groups={}
 for o in ['A','B']:
  for k in ['advantages','disadvantages']:expected[f'a-{o}-{k}']=6
  expected['a-'+o]=12;groups['a-'+o]=[f'a-{o}-advantages',f'a-{o}-disadvantages']
  for k in ['external-design','internal-layout']:expected[f'b-{o}-{k}']=12
  expected['b-'+o+'-garden-link']=6;expected['b-'+o]=30;expected['complete-'+o]=60
  groups['b-'+o]=[f'b-{o}-external-design',f'b-{o}-internal-layout',f'b-{o}-garden-link'];groups['complete-'+o]=['a','b-'+o,'c']
 groups['a']=['a-A','a-B']
 cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==18 and set(cards)==set(expected)
 bs={b['cardId']:b for b in d['bindings']};assert set(bs)=={c['id']for c in cards.values()}
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])
  assert (c['subjectId'],c['year'],c['level'],c['tariffModel'])==('construction-studies',2015,'higher',{'kind':'fixed'})
  assert not c.get('calculationDeductions')and c['questionFigureKey']==fp+'original'
  for context in ['400 mm','M–M faces south','5.0 m × 3.0 m','BOTH options','selects ONE option']:assert context in c['stem']
  assert c['sourceMaterial']['pages']==[1,2]
  b=bs[c['id']];assert b['questionNumber']=='3'and b['markBankTopicId']==c['topicId']and b['atlasTopicIds']==['construction-studies-higher-planning-sustainability-environment']
  assert b['canonicalTopicIds']==(['cons-1-2']if k=='c'else ['cons-1-3','cons-1-2']if k.startswith('b-')and not k.endswith('garden-link')else ['cons-1-2','cons-1-3'])
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='3'and t['requiredQuestionFigures']==[fp+'original']
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,2),(S,2),(S,9),(S,10),(S,34)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert [g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]];rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
  else:
   assert len(c['rows'])==1
   wanted=[0,6]if k.endswith('garden-link')else [0,6,12]if k.startswith('b-')else [0,3,6]
   assert c['rows'][0]['permittedMarks']==wanted
  solution = ('scheme' if k.startswith('complete-') or k in ['b-A','b-B'] else ('attached-exterior' if k.startswith('b-A') else 'detached-exterior') if k.endswith('external-design') else ('attached-layout' if k.startswith('b-A') else 'detached-layout') if k.endswith('internal-layout') else 'garden-link' if k.endswith('garden-link') else None)
  assert c.get('figureKey')==(fp+solution if solution else None)
  assert t['requiredSolutionFigures']==([fp+solution]if solution else [])
  if k.startswith('b-'):
   o=k.split('-')[1];assert 'option '+o in c['questionText']or 'For option '+o in c['questionText']
  if k.endswith('external-design'):assert 'notes 6 and sketches 6' in c['rows'][0]['contextNote']and 'not compulsory' in c['rows'][0]['contextNote']
  if k.endswith('internal-layout'):assert 'notes 6 and sketches 6' in c['rows'][0]['contextNote']and 'exact furniture arrangement' in c['rows'][0]['contextNote']
  if k.endswith('garden-link'):assert 'No separate notes/sketch split' in c['rows'][0]['contextNote']
 assert 'numbering error' in cards['a-B-disadvantages']['rows'][0]['contextNote']
 assert d['routeLedger']['aMustInclude']==['A','B']and d['routeLedger']['bChooseOne']==['A','B']
 assert d['routeLedger']['wholeRoutes']==[dict(option=o,parts=['a','b-'+o,'c'],marks=60)for o in ['A','B']]
 specs={'original':(P,2,[58,444,565,780],False),'attached-exterior':(S,9,[403,64,568,207],True),'attached-layout':(S,10,[427,607,566,792],True),'detached-exterior':(S,9,[388,473,572,589],True),'detached-layout':(S,10,[440,220,543,368],True),'garden-link':(S,10,[366,416,569,550],True),'scheme':(S,10,[54,52,577,793],True)}
 assert len(d['questionFigures'])==7
 for f in d['questionFigures']:
  assert (f['source'],f['page'],f['rect'],f['solution'])==specs[f['key'].removeprefix(fp)]and f['visuallyInspected']
  p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
  if images:
   with fitz.open(R/f['source'])as pdf:px=pdf[f['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(f['rect']),alpha=False)
   a=Image.frombytes('RGB',(px.width,px.height),px.samples);b=Image.open(p).convert('RGB');assert a.size==b.size and ImageChops.difference(a,b).getbbox()is None
 ledger=d['selectionLedger'];observed=[]
 with fitz.open(R/P)as pdf:
  for i,p in enumerate(pdf):observed.extend((i+1,m.start(),m.group())for m in re.finditer(ledger['pattern'],' '.join(p.get_text().split()),re.I))
 assert observed==[(r['page'],r['start'],r['match'])for r in ledger['rows']]and len(observed)==15 and ledger['unclassified']==0 and all(r['classification']for r in ledger['rows'])
 return dict(tasks=18,wholeQuestionRoutes=2,figures=7,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q3-draft.json').read_text()))))
