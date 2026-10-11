"""Source-pinned review of the 2015 Higher entrance and external-wall tasks."""
import copy,hashlib,json,re
from pathlib import Path
import fitz
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3]
REVIEW=R/'scripts/markbank/authored/construction-studies-2015-higher-reviewed.json'
P='paper-trail-corpus/exampapers/2015/LC029ALP000EV.pdf'
S='paper-trail-corpus/markingschemes/2015/LC029ALP000EV.pdf'
def validate(d,images=True):
 assert {'1','2'}<=set(d['questionsReviewed'])
 assert set(d['unreviewedQuestions'])==set(map(str,range(1,11)))-set(d['questionsReviewed'])
 d=copy.deepcopy(d)
 d['tasks']=[t for t in d['tasks']if t['questionNumber']in ['1','2']]
 d['bindings']=[b for b in d['bindings']if b['questionNumber']in ['1','2']]
 d['questionFigures']=[f for f in d['questionFigures']if f['key'].startswith(('construction-studies-2015-HL-q1-','construction-studies-2015-HL-q2-'))]
 hashes={P:'08976c01caaf916102e5f9f0aa18a512a5bf6aa2cad2ce5320208a63970fdc13',S:'9558f06c3c50cb7c858d0b4fb299b437277c0efcd182e0811c6aff0bb7dab3ef'}
 assert d['sourceHashes']==hashes
 for f,h in hashes.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h
 cards={t['card']['id']:t['card']for t in d['tasks']};prefix='cons-2015-hl-'
 expected={'q1-a':52,'q1-b':8,'q1-complete':60,'q2-a':24,'q2-b':24,'q2-c':12,'q2-complete':60}
 assert set(cards)=={prefix+k for k in expected}and len(d['tasks'])==len(d['bindings'])==7
 bindings={b['cardId']:b for b in d['bindings']};assert set(bindings)==set(cards)
 a_topics=['question-1-drawing-questions','doors','walls','floors','heat-loss-insulation']
 for key,marks in expected.items():
  c=cards[prefix+key];b=bindings[c['id']];q=key[1]
  assert c['totalMarks']==marks==sum(r['marks']for r in c['rows'])
  assert (c['year'],c['level'],c['subjectId'])==(2015,'higher','construction-studies')
  assert c['tariffModel']=={'kind':'fixed'}and not c.get('calculationDeductions')
  assert b['questionNumber']==q and b['markBankTopicId']==c['topicId']
  topics=['doors']if key=='q1-b'else a_topics if q=='1'else ['walls']
  assert b['atlasTopicIds']==['construction-studies-higher-'+t for t in topics]
  nodes=['cons-3-7']if key=='q1-b'else ['cons-1-5','cons-3-7','cons-3-3','cons-4-2','cons-6-2']if q=='1'else ['cons-3-2']if key=='q2-a'else ['cons-3-2','cons-3-3']
  assert b['canonicalTopicIds']==nodes
  assert c['questionFigureKey']==f'construction-studies-2015-HL-q{q}-original'
  assert c['sourceMaterial']['pages']==[1,2]
  if q=='1':assert all(x in c['stem']for x in ['150 mm × 70 mm','100 mm','200 mm','60 mm','20 mm','500 mm','300 mm','1:10'])
  else:assert all(x in c['stem']for x in ['three different','two of your own','materials','dimensions'])
  t=next(t for t in d['tasks']if t['card']['id']==c['id'])
  expected_checks={(P,1),(P,2)}|{(S,p)for p in ([2,4,5,6,32]if q=='1'else [2,6,7,8,33])}
  assert {(x['file'],x['page'])for x in t['sourceChecks']}==expected_checks
  for x in t['sourceChecks']:
   with fitz.open(R/x['file'])as pdf:assert hashlib.sha256(' '.join(pdf[x['page']-1].get_text().split()).encode()).hexdigest()==x['textSha256']
  assert t['requiredQuestionFigures']==[c['questionFigureKey']]
  assert t['requiredSolutionFigures']==([c['figureKey']]if q=='1'else [])
 def card(k):return cards[prefix+k]
 assert [r['marks']for r in card('q1-a')['rows']]==[44,8]
 assert card('q1-a')['rows'][0]['permittedMarks']==list(range(45))
 assert card('q1-a')['rows'][1]['permittedMarks']==[0,2,3,4,6,7,8]
 assert card('q1-b')['rows'][0]['permittedMarks']==[0,8]
 assert card('q2-a')['rows'][0]['permittedMarks']==list(range(0,25,4))
 assert card('q2-b')['rows'][0]['permittedMarks']==list(range(25))
 assert card('q2-c')['rows'][0]['permittedMarks']==list(range(0,13,3))
 checks={'q1-a':['best eleven','drawing 3 plus annotation 1','standard uninsulated door earns 2','standard frame earns 2','Foundations are not required'],'q1-b':['sloped threshold and upstand','no separate 4+4','not award'],'q2-a':['notes 4 and sketches 4','not earn all 24'],'q2-b':['DISTINCT','materials 1','dimensions 1','not an exhaustive finite pool'],'q2-c':['Evaluate first wall 3','evaluate second wall 3','justify recommendation 3','two of the student-selected']}
 for key,phrases in checks.items():
  notes=' '.join(r['contextNote']for r in card(key)['rows'])
  assert all(s in notes for s in phrases),(key,[s for s in phrases if s not in notes])
 for q,parts in [('1',['a','b']),('2',['a','b','c'])]:
  c=card('q'+q+'-complete');assert [g['sourceCardId']for g in c['taskGroups']]==[prefix+'q'+q+'-'+s for s in parts]
  allrows=[]
  for s,g in zip(parts,c['taskGroups']):
   child=card('q'+q+'-'+s);rows=copy.deepcopy(child['rows'])
   for r in rows:r['id']=s+'-'+r['id']
   assert g['rowIds']==[r['id']for r in rows]and g['marks']==child['totalMarks'];allrows+=rows
  assert allrows==c['rows']
 specs={'construction-studies-2015-HL-q1-original':(P,2,[58,54,565,252],False),'construction-studies-2015-HL-q1-scheme':(S,4,[60,104,558,767],True),'construction-studies-2015-HL-q1-access-scheme':(S,5,[27,460,573,627],True),'construction-studies-2015-HL-q2-original':(P,2,[58,267,565,421],False)}
 assert len(d['questionFigures'])==4
 for f in d['questionFigures']:
  assert (f['source'],f['page'],f['rect'],f['solution'])==specs[f['key']]and f['visuallyInspected']
  path=R/'public/exam-figures/construction-studies/markbank'/(f['key']+'.png');assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256']
  if images:
   with fitz.open(R/f['source'])as pdf:px=pdf[f['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(f['rect']),alpha=False)
   original=Image.frombytes('RGB',(px.width,px.height),px.samples);saved=Image.open(path).convert('RGB');assert original.size==saved.size and ImageChops.difference(original,saved).getbbox()is None
 ledger=d['selectionLedger'];observed=[]
 with fitz.open(R/P)as pdf:
  for i,p in enumerate(pdf):observed.extend((i+1,m.start(),m.group())for m in re.finditer(ledger['pattern'],' '.join(p.get_text().split()),re.I))
 assert observed==[(r['page'],r['start'],r['match'])for r in ledger['rows']]and len(observed)==15 and ledger['unclassified']==0
 assert all(r['classification']for r in ledger['rows'])
 return {'tasks':7,'sourceFigures':4,'sourceSelectionCandidates':15,'paperComplete':False}
if __name__=='__main__':print(json.dumps(validate(json.loads(REVIEW.read_text()))))
