from pathlib import Path
import json,hashlib,copy,re,fitz
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q8-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q8-';fp='construction-studies-2015-HL-q8-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 expected={'a':40,'b':8,'c-chimney':6,'c-hotpress':6,'c':12,'complete':60};groups={'c':['c-chimney','c-hotpress'],'complete':['a','b','c']};cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==6 and set(cards)==set(expected)and d['addedIds']==[t['card']['id']for t in d['tasks']];bs={b['cardId']:b for b in d['bindings']};assert len(bs)==6
 wanted={'a':(['cons-5-3','cons-5-2'],['hot-water-space-heating'],'system'),'b':(['cons-5-2','cons-5-3'],['hot-water-space-heating'],'collector'),'c-chimney':(['cons-5-7'],['fireplaces-fire-prevention'],'locations'),'c-hotpress':(['cons-5-2','cons-5-3'],['hot-water-space-heating'],'locations'),'c':(['cons-5-7','cons-5-2','cons-5-3'],['fireplaces-fire-prevention','hot-water-space-heating'],'locations'),'complete':(['cons-5-3','cons-5-2','cons-5-7'],['hot-water-space-heating','fireplaces-fire-prevention'],'scheme')}
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])and c['tariffModel']=={'kind':'fixed'}
  nodes,topics,fig=wanted[k];assert(c['subjectId'],c['year'],c['level'])==('construction-studies',2015,'higher')and c['questionFigureKey']==fp+'original'and c['figureKey']==fp+fig and c['sourceMaterial']['pages']==[1,4]
  for s in ['wood-burning stove combined with a solar collector','central heating AND hot water','two independently controlled heating zones','three radiators on EACH floor','BOTH the chimney and the hot press','solar thermal']:assert s in c['stem']
  b=bs[c['id']];assert b['questionNumber']=='8'and b['markBankTopicId']==c['topicId']==nodes[0]and b['canonicalTopicIds']==nodes and b['atlasTopicIds']==['construction-studies-higher-'+x for x in topics]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='8'and t['requiredQuestionFigures']==[fp+'original']and t['requiredSolutionFigures']==[fp+fig]
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,4),(S,2),(S,22),(S,23),(S,39)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert[g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]];rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
 assert[(r['marks'],r['permittedMarks'])for r in cards['a']['rows']]==[(36,list(range(37))),(4,[0,2,4])]
 assert[(r['marks'],r['permittedMarks'])for r in cards['b']['rows']]==[(4,[0,4]),(4,[0,4])]
 for k in ['c-chimney','c-hotpress']:assert[(r['marks'],r['permittedMarks'])for r in cards[k]['rows']]==[(3,[0,3]),(3,[0,3])]
 for s in ['best NINE','sketch 3 plus annotation 1','ONE detail','six radiators']:assert s in cards['a']['rows'][0]['contextNote']
 for s in ['22 mm','15 mm','28 mm','NOT pipe diameters']:assert s in cards['a']['rows'][1]['contextNote']
 assert 'do not substitute photovoltaic'in cards['b']['rows'][0]['contextNote']and 'BOTH the chimney and the hot press'in cards['c']['questionText']
 assert cards['complete']['questionText']=='\n\n'.join(cards[k]['questionText']for k in ['a','b','c'])
 assert d['routeLedger']['wholeRoutes']==[dict(id=prefix+'complete',parts=['a','b','c'],marks=60)]and d['routeLedger']['requiredHeatingZones']==2 and d['routeLedger']['requiredRadiatorsPerFloor']==3 and d['routeLedger']['requiredLocations']==['chimney','hotpress']and len(d['routeLedger']['nonChoices'])==4
 specs={'original':[(P,4,[58,569,572,783])],'system':[(S,22,[40,54,568,779])],'collector':[(S,22,[40,54,568,779]),(S,23,[57,54,567,327])],'locations':[(S,23,[55,333,568,779])]};specs['scheme']=specs['system']+specs['collector'][1:]+specs['locations'];assert len(d['questionFigures'])==5 and {f['key'].removeprefix(fp)for f in d['questionFigures']}==set(specs)
 for f in d['questionFigures']:
  name=f['key'].removeprefix(fp);assert[(p['source'],p['page'],p['rect'])for p in f['panels']]==specs[name]and f['solution']==(name!='original')and f['visuallyInspected']and f['panelGap']==24 and f['renderScale']==2;p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
  if images:
   panels=[]
   for pp in f['panels']:
    with fitz.open(R/pp['source'])as pdf:px=pdf[pp['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(pp['rect']),alpha=False)
    panels.append(Image.frombytes('RGB',(px.width,px.height),px.samples))
   canvas=Image.new('RGB',(max(i.width for i in panels),sum(i.height for i in panels)+24*(len(panels)-1)),'white');y=0
   for im in panels:canvas.paste(im,(0,y));y+=im.height+24
   im=Image.open(p).convert('RGB');assert canvas.size==im.size and ImageChops.difference(canvas,im).getbbox()is None
 ledger=d['selectionLedger'];observed=[]
 with fitz.open(R/P)as pdf:
  for i,p in enumerate(pdf):observed.extend((i+1,m.start(),m.group())for m in re.finditer(ledger['pattern'],' '.join(p.get_text().split()),re.I))
 assert observed==[(r['page'],r['start'],r['match'])for r in ledger['rows']]and len(observed)==15 and ledger['unclassified']==0
 return dict(tasks=6,wholeQuestionRoutes=1,figures=5,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q8-draft.json').read_text()))))
