from pathlib import Path
import json,hashlib,copy,re,itertools,fitz
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q4-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q4-';fp='construction-studies-2015-HL-q4-';ap='construction-studies-higher-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 aa=['local-character','breathable-structure','reuse-materials'];bb=['roof','windows','floor'];aps=list(itertools.combinations(aa,2));bps=list(itertools.combinations(bb,2));expected={'a-'+k:10 for k in aa}|{'b-'+k:20 for k in bb};groups={};solutions={'b-'+k:k for k in bb};routes=[]
 for a in aps:
  k='a-'+'-and-'.join(a);expected[k]=20;groups[k]=['a-'+x for x in a]
 for b in bps:
  k='b-'+'-and-'.join(b);expected[k]=40;groups[k]=['b-'+x for x in b];solutions[k]='windows'if tuple(b)==('windows','floor')else '-'.join(b)
 for a,b in itertools.product(aps,bps):
  k='complete-'+'-and-'.join(a)+'--'+'-and-'.join(b);expected[k]=60;groups[k]=['a-'+'-and-'.join(a),'b-'+'-and-'.join(b)];solutions[k]='windows'if tuple(b)==('windows','floor')else '-'.join(b);routes.append(dict(id=prefix+k,a=list(a),b=list(b),parts=groups[k],marks=60))
 cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==21 and set(cards)==set(expected)
 assert d['addedIds']==[t['card']['id']for t in d['tasks']]
 bs={b['cardId']:b for b in d['bindings']};assert set(bs)=={c['id']for c in cards.values()}
 nodes={'a-local-character':['cons-1-1','cons-1-2'],'a-breathable-structure':['cons-6-6','cons-6-2','cons-1-1'],'a-reuse-materials':['cons-1-1','cons-1-2'],'b-roof':['cons-3-8','cons-3-9','cons-6-2','cons-1-1'],'b-windows':['cons-3-5','cons-3-6','cons-1-1'],'b-floor':['cons-4-2','cons-4-3','cons-6-2','cons-1-1']}
 topics={'a-local-character':['conservation-restoration'],'a-breathable-structure':['condensation-air-tightness','heat-loss-insulation','conservation-restoration'],'a-reuse-materials':['conservation-restoration'],'b-roof':['roofs','heat-loss-insulation','conservation-restoration'],'b-windows':['windows-light','conservation-restoration'],'b-floor':['floors','heat-loss-insulation','conservation-restoration']}
 for k,parts in groups.items():
  nodes[k]=list(dict.fromkeys(n for x in parts for n in nodes[x]));topics[k]=list(dict.fromkeys(n for x in parts for n in topics[x]))
 for k,c in cards.items():
  assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])
  assert (c['subjectId'],c['year'],c['level'],c['tariffModel'])==('construction-studies',2015,'higher',{'kind':'fixed'})
  assert not c.get('calculationDeductions')and c['questionFigureKey']==fp+'original'
  for context in ['vernacular tradition','any TWO','single-storey cottages','traditional cut roof with natural slates','single-glazed with sliding sash','suspended timber floor','selections in (a) and (b) are independent']:assert context in c['stem']
  assert c['sourceMaterial']['pages']==[1,3]
  b=bs[c['id']];assert b['questionNumber']=='4'and b['markBankTopicId']==c['topicId']==nodes[k][0]and b['canonicalTopicIds']==nodes[k]and b['atlasTopicIds']==[ap+t for t in topics[k]]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='4'and t['requiredQuestionFigures']==[fp+'original']
  assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,3),(S,2),(S,11),(S,12),(S,13),(S,14),(S,35)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert [g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]];rows=[]
   assert c['questionText']=='\n\n'.join(cards[s]['questionText']for s in groups[k])
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']
  else:
   assert len(c['rows'])==1 and c['rows'][0]['permittedMarks']==([0,10]if k.startswith('a-')else [0,10,20])
   if k.startswith('a-'):assert 'does not divide it' in c['rows'][0]['contextNote']
   else:assert 'notes 10 and freehand sketches 10' in c['rows'][0]['contextNote']
  assert c.get('figureKey')==(fp+solutions[k]if k in solutions else None)
  assert t['requiredSolutionFigures']==([fp+solutions[k]]if k in solutions else [])
 assert 'alternative coherent designs' in cards['b-roof']['rows'][0]['contextNote']
 assert 'not additional choose-one card routes' in cards['b-floor']['rows'][0]['contextNote']
 assert d['routeLedger']['aPool']==aa and d['routeLedger']['bPool']==bb and d['routeLedger']['aChoose']==d['routeLedger']['bChoose']==2 and d['routeLedger']['wholeRoutes']==routes
 specs={'original':[(P,3,[57,54,568,302])],'roof':[(S,12,[54,242,568,768]),(S,13,[54,54,568,158])],'windows':[(S,13,[54,267,568,776]),(S,14,[54,54,573,792])],'floor':[(S,14,[54,54,573,792])]}
 for a,b in bps:specs[a+'-'+b]=list({(f,p,tuple(r)):(f,p,r)for f,p,r in specs[a]+specs[b]}.values())
 specs.pop('windows-floor')
 assert len(d['questionFigures'])==6 and {f['key']for f in d['questionFigures']}=={fp+k for k in specs}
 for f in d['questionFigures']:
  name=f['key'].removeprefix(fp);assert f['panels']==[dict(source=s,page=p,rect=r)for s,p,r in specs[name]]and f['visuallyInspected']and f['renderScale']==2 and f['panelGap']==24 and f['solution']==(name!='original')
  p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
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
 return dict(tasks=21,partARoutes=3,partBRoutes=3,wholeQuestionRoutes=9,figures=6,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q4-draft.json').read_text()))))
