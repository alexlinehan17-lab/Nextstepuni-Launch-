from pathlib import Path
import json,hashlib,copy,re,fitz
from decimal import Decimal as N,getcontext
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q5-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q5-';fp='construction-studies-2015-HL-q5-';ap='construction-studies-higher-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 expected={'a':30,'b-new':10,'b-existing':10,'b':20,'c':10,'complete':60};groups={'b':['b-new','b-existing'],'complete':['a','b-new','b-existing','c']};cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==6 and set(cards)==set(expected)
 bs={b['cardId']:b for b in d['bindings']};assert set(bs)=={c['id']for c in cards.values()}and d['addedIds']==[t['card']['id']for t in d['tasks']]
 nodes={'a':['cons-6-1'],'b-new':['cons-6-3'],'b-existing':['cons-6-3'],'b':['cons-6-3'],'c':['cons-3-4','cons-3-6'],'complete':['cons-6-1','cons-6-3','cons-3-4','cons-3-6']}
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])and c['tariffModel']=={'kind':'fixed'}
  assert (c['subjectId'],c['year'],c['level'])==('construction-studies',2015,'higher')and c['questionFigureKey']==fp+'original'
  for text in ['16 mm','100 mm outer','250 mm cavity FULLY filled','100 mm inner','12 mm','0.048','0.122','0.720','1.440','0.031','0.220','150 m²','20 °C','6 °C','8 hours/day','35 weeks/year','€0.95/litre','37,350 kJ/litre','BOTH','0.21']:assert text in c['stem']
  assert ('reference answer from part (a)'in c['stem'])==(k in ['b','b-new'])
  assert '0.11834078'not in c['questionText']and ('0.11834078'not in c['stem']if k in ['a','complete']else True)
  assert c['sourceMaterial']['pages']==[1,3]and not c.get('calculationDeductions')
  b=bs[c['id']];assert b['questionNumber']=='5'and b['markBankTopicId']==c['topicId']==nodes[k][0]and b['canonicalTopicIds']==nodes[k]
  topics=['walls','windows-light']if k=='c'else ['heat-u-value-calculations','walls','windows-light']if k=='complete'else ['heat-u-value-calculations'];assert b['atlasTopicIds']==[ap+x for x in topics]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='5'and t['requiredQuestionFigures']==[fp+'original']
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,3),(S,2),(S,15),(S,16),(S,17),(S,36)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert [g['sourceCardId']for g in c['taskGroups']]==[prefix+x for x in groups[k]]and c['questionText']=='\n\n'.join(cards[x]['questionText']for x in groups[k]);rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
  else:assert len(c['rows'])<=5
  solution=fp+'window-head'if k in ['c','complete']else None;assert c.get('figureKey')==solution and t['requiredSolutionFigures']==([solution]if solution else [])
 assert [(r['id'],r['marks'],r['permittedMarks'])for r in cards['a']['rows']]==[('method',3,[0,3]),('surfaces',6,[0,3,6]),('material-layers',15,[0,3,6,9,12,15]),('total-resistance',3,[0,3]),('u-value',3,[0,1,3])]
 arows={r['id']:r for r in cards['a']['rows']}
 for x in ['Rse = 0.048','Rsi = 0.122']:assert x in arows['surfaces']['contextNote']
 for x in ['0.016/0.720','0.100/1.440','0.250/0.031','0.012/0.220','second leaf','do not add a separate air-cavity resistance']:assert x in arows['material-layers']['contextNote']
 assert 'ground floor' in arows['method']['contextNote']and 'source error' in arows['method']['contextNote']
 assert 'formula alone within this 3-mark criterion' in arows['u-value']['contextNote']
 for h in ['new','existing']:
  rows=cards['b-'+h]['rows'];assert [r['id']for r in rows]==['heat-rate','heating-time','annual-energy','oil','annual-cost']and all(r['marks']==2 and r['permittedMarks']==[0,2]for r in rows)
  assert '1,960 hours = 7,056,000 seconds' in rows[1]['contextNote']and 'that parenthetical hours figure is an error' in rows[1]['contextNote']
  assert 'do not invent an unstated boiler-efficiency factor' in rows[3]['contextNote']
 assert all(s in cards['b-new']['rows'][-1]['contextNote']for s in ['€44.60','€44.58','€44.59','coherent rounding'])
 assert all(s in cards['b-existing']['rows'][-1]['contextNote']for s in ['€79.15','€79.14','€79.13','coherent rounding'])
 assert [(r['id'],r['marks'],r['permittedMarks'])for r in cards['c']['rows']]==[('annotations',5,[0,5]),('sketches',5,[0,5])]
 assert d['routeLedger']['requiredHouseCalculations']==['new','existing']and d['routeLedger']['wholeRoutes']==[dict(id=prefix+'complete',parts=['a','b-new','b-existing','c'],marks=60)]
 getcontext().prec=28;res=[N('.048'),N('.016')/N('.720'),N('.100')/N('1.440'),N('.250')/N('.031'),N('.100')/N('1.440'),N('.012')/N('.220'),N('.122')];ar=d['arithmeticReview'];assert list(map(N,ar['resistances']))==res and N(ar['totalResistance'])==sum(res)and N(ar['uValue'])==1/sum(res)and ar['heatingHours']==8*7*35 and ar['heatingSeconds']==8*7*35*3600
 for h,u in [('new',1/sum(res)),('existing',N('.21'))]:
  a=ar['houses'][h];w=u*150*(20-6);e=w*(8*7*35*3600)/1000;l=e/N(37350)
  assert {k:N(a[k])for k in a}==dict(u=u,watts=w,kJ=e,litres=l,cost=l*N('.95'))
 assert len(d['sourceErrata'])==3
 specs={'original':(P,3,[58,319,568,793],False),'window-head':(S,17,[54,33,573,315],True)};assert len(d['questionFigures'])==2
 for f in d['questionFigures']:
  assert (f['source'],f['page'],f['rect'],f['solution'])==specs[f['key'].removeprefix(fp)]and f['visuallyInspected'];p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
  if images:
   with fitz.open(R/f['source'])as pdf:px=pdf[f['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(f['rect']),alpha=False)
   a=Image.frombytes('RGB',(px.width,px.height),px.samples);b=Image.open(p).convert('RGB');assert a.size==b.size and ImageChops.difference(a,b).getbbox()is None
 ledger=d['selectionLedger'];observed=[]
 with fitz.open(R/P)as pdf:
  for i,p in enumerate(pdf):observed.extend((i+1,m.start(),m.group())for m in re.finditer(ledger['pattern'],' '.join(p.get_text().split()),re.I))
 assert observed==[(r['page'],r['start'],r['match'])for r in ledger['rows']]and len(observed)==15 and ledger['unclassified']==0
 return dict(tasks=6,wholeQuestionRoutes=1,figures=2,arithmeticRecalculated=True,sourceErrata=3)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q5-draft.json').read_text()))))
