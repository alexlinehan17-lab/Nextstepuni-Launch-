from pathlib import Path
import json,hashlib,copy,re,fitz,itertools
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];F=R/'public/exam-figures/construction-studies/markbank';T=R/'docs/markbank-audit/2026-09-28/drafts/construction-2015-higher-q10-draft';P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf';S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf';prefix='cons-2015-hl-q10-';fp='construction-studies-2015-HL-q10-'
def validate(d,images=True):
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'};assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 choices=['airtightness','space-heating','indoor-air'];pairs=list(itertools.combinations(choices,2));expected={'a-'+k:16 for k in choices};expected.update({'a-'+'-'.join(g):32 for g in pairs});expected.update({'b':14,'c':14});expected.update({'complete-'+'-'.join(g):60 for g in pairs});expected.update({'alt-discussion':24,'alt-glazing':6,'alt-guidelines':30,'alt-complete':60})
 groups={'a-'+'-'.join(g):['a-'+k for k in g]for g in pairs};groups.update({'complete-'+'-'.join(g):['a-'+k for k in g]+['b','c']for g in pairs});groups['alt-complete']=['alt-discussion','alt-glazing','alt-guidelines']
 cards={t['card']['id'].removeprefix(prefix):t['card']for t in d['tasks']};assert len(d['tasks'])==len(d['bindings'])==15 and set(cards)==set(expected)and d['addedIds']==[t['card']['id']for t in d['tasks']];bs={b['cardId']:b for b in d['bindings']};assert len(bs)==15
 nodes={'a-airtightness':['cons-6-5','cons-6-6'],'a-space-heating':['cons-5-3','cons-6-2'],'a-indoor-air':['cons-6-5'],'b':['cons-6-4'],'c':['cons-6-4','cons-7-3'],'alt-discussion':['cons-7-4','cons-3-5'],'alt-glazing':['cons-3-6'],'alt-guidelines':['cons-7-4','cons-3-5','cons-1-3']}
 topics={'a-airtightness':['passive-design','condensation-air-tightness'],'a-space-heating':['hot-water-space-heating','passive-design'],'a-indoor-air':['passive-design','wood-rot-ventilation'],'b':['passive-design'],'c':['passive-design','windows-light'],'alt-discussion':['windows-light'],'alt-glazing':['windows-light'],'alt-guidelines':['windows-light','planning-sustainability-environment']}
 for k,parts in groups.items():nodes[k]=list(dict.fromkeys(n for p in parts for n in nodes[p]));topics[k]=list(dict.fromkeys(n for p in parts for n in topics[p]))
 for k,c in cards.items():
  alt=k.startswith('alt-');assert c['id']==prefix+k and c['totalMarks']==expected[k]==sum(r['marks']for r in c['rows'])and c['tariffModel']=={'kind':'fixed'}
  assert(c['subjectId'],c['year'],c['level'])==('construction-studies',2015,'higher')and c['questionFigureKey']==fp+('alternative'if alt else'original')and c.get('figureKey')==(None if alt else fp+'scheme')and c['sourceMaterial']['pages']==[1,5]
  assert c['questionRef'].startswith('2015 HL Q10-alt'if alt else'2015 HL Q10')
  if alt:
   for s in ['Dermot Bannon','2014','9780717164486','complete passage','THREE','single 60-mark route','rather than eliminating']:assert s in c['stem']
  else:
   for s in ['PRIMARY','any TWO of three','airtight building envelope','space heating demand','indoor air quality','thermal mass','solar shading','different 60-mark route']:assert s in c['stem']
  b=bs[c['id']];assert b['questionNumber']=='10'and b['markBankTopicId']==c['topicId']==nodes[k][0]and b['canonicalTopicIds']==nodes[k]and b['atlasTopicIds']==['construction-studies-higher-'+x for x in topics[k]]
  t=next(t for t in d['tasks']if t['card']['id']==c['id']);assert t['questionNumber']=='10'and t['requiredQuestionFigures']==[c['questionFigureKey']]and t['requiredSolutionFigures']==([]if alt else[fp+'scheme'])
  ps=[2,29,30,42]if alt else[2,25,26,27,28,41];assert {(x['file'],x['page'])for x in t['sourceChecks']}=={(P,1),(P,5),*((S,n)for n in ps)}
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  if k in groups:
   assert[g['sourceCardId']for g in c['taskGroups']]==[prefix+s for s in groups[k]];rows=[]
   for sub,g in zip(groups[k],c['taskGroups']):
    rs=copy.deepcopy(cards[sub]['rows'])
    for r in rs:r['id']=sub+'-'+r['id']
    assert g['rowIds']==[r['id']for r in rs]and g['marks']==cards[sub]['totalMarks'];rows+=rs
   assert rows==c['rows']and c['questionText']=='\n\n'.join(cards[sub]['questionText']for sub in groups[k])
  else:
   target=[(8,[0,8])]*2 if k.startswith('a-')else[(7,[0,7])]*2 if k in ['b','c']else[(8,[0,3,5,8])]*3 if k=='alt-discussion'else[(6,[0,6])]if k=='alt-glazing'else[(10,[0,4,6,10])]*3
   assert[(r['marks'],r['permittedMarks'])for r in c['rows']]==target
 assert 'does not eliminate conductive heat loss'in cards['a-airtightness']['rows'][0]['contextNote']
 assert 'historical scheme figures'in cards['a-space-heating']['rows'][0]['contextNote']and 'blower-door leakage test'in cards['a-indoor-air']['rows'][0]['contextNote']
 assert 'not the same as thermal insulation'in cards['b']['rows'][0]['contextNote']
 assert 'low iron content itself reduces conductivity is not used'in cards['alt-glazing']['rows'][0]['contextNote']
 routes=[dict(id=prefix+'complete-'+'-'.join(g),alternative=False,choices=list(g),parts=['a-'+k for k in g]+['b','c'],marks=60)for g in pairs]+[dict(id=prefix+'alt-complete',alternative=True,choices=[],parts=groups['alt-complete'],marks=60)]
 ledger=d['routeLedger'];assert ledger['primaryChoices']==choices and ledger['choose']==2 and ledger['partARoutes']==[list(g)for g in pairs]and ledger['wholeRoutes']==routes and ledger['alternativeOriginalQuestionNumber']=='10'and len(ledger['nonChoices'])==3
 specs={'original':[(P,5,[58,302,572,486])],'alternative':[(P,5,[58,560,572,771])],'scheme':[(S,25,[54,264,570,776]),(S,26,[54,54,574,785]),(S,27,[54,54,571,778]),(S,28,[43,54,575,786])]};assert len(d['questionFigures'])==3
 for f in d['questionFigures']:
  name=f['key'].removeprefix(fp);assert[(p['source'],p['page'],p['rect'])for p in f['panels']]==specs[name]and f['solution']==(name=='scheme')and f['visuallyInspected']and f['panelGap']==24 and f['renderScale']==2;p=F/(f['key']+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
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
 return dict(tasks=15,wholeQuestionRoutes=4,primaryRoutes=3,alternativeRoutes=1,figures=3,sourcePagesChecked=True)
if __name__=='__main__':print(json.dumps(validate(json.loads((T/'q10-draft.json').read_text()))))
