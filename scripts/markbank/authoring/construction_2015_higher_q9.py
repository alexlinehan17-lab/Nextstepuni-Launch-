from pathlib import Path
import json,hashlib,copy,re,fitz,itertools
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q9-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q9-';fp='construction-studies-2015-HL-q9-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 locs=['eaves','upper-floor','cill','ground-floor'];triples=list(itertools.combinations(locs,3));expected={'a-'+k:16 for k in locs};expected.update({'a-'+'-'.join(g):48 for g in triples});expected['b']=12;expected.update({'complete-'+'-'.join(g):60 for g in triples});groups={'a-'+'-'.join(g):['a-'+k for k in g]for g in triples};groups.update({'complete-'+'-'.join(g):['a-'+k for k in g]+['b']for g in triples})
 cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==13 and set(cards)==set(expected)and d['addedIds']==[t['card']['id']for t in d['tasks']];bs={b['cardId']:b for b in d['bindings']};assert len(bs)==13
 nodes={'a-eaves':['cons-6-2','cons-3-9','cons-3-3'],'a-upper-floor':['cons-6-2','cons-4-3','cons-3-3'],'a-cill':['cons-6-2','cons-3-6'],'a-ground-floor':['cons-6-2','cons-4-2','cons-3-3'],'b':['cons-6-2','cons-6-6']};topics={'a-eaves':['heat-loss-insulation','roofs','walls'],'a-upper-floor':['heat-loss-insulation','floors','walls'],'a-cill':['heat-loss-insulation','windows-light'],'a-ground-floor':['heat-loss-insulation','floors','walls'],'b':['heat-loss-insulation','condensation-air-tightness']}
 for k,parts in groups.items():nodes[k]=list(dict.fromkeys(n for p in parts for n in nodes[p]));topics[k]=list(dict.fromkeys(n for p in parts for n in topics[p]))
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])and c['tariffModel']=={'kind':'fixed'}
  assert(c['subjectId'],c['year'],c['level'])==('construction-studies',2015,'higher')and c['questionFigureKey']==fp+'original'and c['figureKey']==fp+'scheme'and c['sourceMaterial']['pages']==[1,5]
  for s in ['450 mm','250 mm','traditional cut roof','tongue-and-groove','insulated solid-concrete','FOUR junctions','any THREE','NOT a fifth']:assert s in c['stem']
  b=bs[c['id']];assert b['questionNumber']=='9'and b['markBankTopicId']==c['topicId']==nodes[k][0]and b['canonicalTopicIds']==nodes[k]and b['atlasTopicIds']==['construction-studies-higher-'+x for x in topics[k]]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='9'and t['requiredQuestionFigures']==[fp+'original']and t['requiredSolutionFigures']==[fp+'scheme']
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,5),(S,2),(S,24),(S,25),(S,40)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert[g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]];rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
  else:
   target=[(6,[0,2,4,6])]*2 if k=='b'else[(8,[0,8])]*2
   assert[(r['marks'],r['permittedMarks'])for r in c['rows']]==target
 assert 'CILL, not the separate window-head' in cards['a-cill']['rows'][0]['contextNote']
 assert 'airtightness alone does not' in cards['b']['rows'][0]['contextNote']
 ledger=d['routeLedger'];assert ledger['circledLocations']==locs and ledger['choose']==3 and ledger['partARoutes']==[list(g)for g in triples]and ledger['wholeRoutes']==[dict(id=prefix+'complete-'+'-'.join(g),locations=list(g),parts=['a-'+k for k in g]+['b'],marks=60)for g in triples]and len(ledger['nonChoices'])==2
 specs={'original':[(P,5,[58,49,566,288])],'scheme':[(S,24,[54,54,581,765]),(S,25,[54,54,568,262])]};assert len(d['questionFigures'])==2
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
 return dict(tasks=13,wholeQuestionRoutes=4,partARoutes=4,figures=2,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q9-draft.json').read_text()))))
