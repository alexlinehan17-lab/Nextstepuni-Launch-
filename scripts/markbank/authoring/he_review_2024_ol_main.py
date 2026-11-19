#!/usr/bin/env python3
"""Source-pinned 2024 Ordinary main review; shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='examiner-reports/home-economics/papers/2024-ol-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2024-ol-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2024/LC098GLP000EV.pdf'
HASHES={PAPER_A:'bb3203d5a58a3ba377ad3cf90e332d15797214e9a57e2b447cc7b88f29525499',PAPER_BC:'5e304e9af0e873c3c5b79923d04399c488bbe12da4a1d15046cda4799bbc87fb',SCHEME:'ff68e9eda1be40ee7756b7cc1e62399031a99038f5919d93945cd8976167346d'}
REVIEW='scripts/markbank/authoring/home-economics/2024-ol-main-review.json'


def page_text(doc,n):
 cutoff=780 if doc.name.endswith('LC098GLP000EV.pdf') else (760 if doc.name.endswith('2024-ol-039-paper.pdf') else 740)
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,cutoff)))


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 d=dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))
 pattern=r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b'
 expected_a={1: ['each', 'following', 'or'], 2: ['two', 'one'], 3: ['following'], 4: ['two', 'two'], 5: ['each', 'following', 'or'], 6: ['three'], 7: ['two', 'each'], 8: ['three'], 9: ['following', 'or', 'or'], 10: ['three'], 11: ['three'], 12: ['following'], 13: ['two'], 14: ['three']}
 expected_bc={2: ['any', 'two', 'each', 'choose', 'five', 'each', 'following', 'three', 'four'], 3: ['following', 'one', 'three', 'four', 'three', 'one', 'each', 'each', 'following'], 4: ['four', 'or', 'each', 'following', 'three'], 5: ['or', 'one', 'or', 'either', 'or', 'either', 'or', 'four', 'following', 'following', 'or', 'three', 'one'], 6: ['either', 'or', 'each', 'following', 'or', 'two', 'two', 'three'], 7: ['either', 'or', 'following', 'three', 'or', 'each', 'following', 'or', 'following'], 8: ['either', 'or', 'one', 'three', 'three', 'three', 'or', 'three']}
 for n,r in a_regions(d['a'],range(3,8),740).items():assert re.findall(pattern,region_text(d['a'],r),re.I)==expected_a[n],n
 for n,tokens in expected_bc.items():assert re.findall(pattern,page_text(d['bc'],n),re.I)==tokens,n
 return d


def originals():return {c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/home-economics.json').read_text())}


def save_batch(section,fixes,added,review_data):
 p=ROOT/'scripts/markbank/card-corrections.json';data=json.loads(p.read_text());data['home-economics'].update(fixes);p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text())
 for c in added:
  i=next((i for i,v in enumerate(data) if v['id']==c['id']),None)
  if i is None:data.append(c)
  else:data[i]=c
 p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2024,level='ordinary',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 32 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–31, back cover 32.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 38 pages: cover 1, guidance/rubrics/annotations 2–5, A 6–9, B 10–15, C 16–25, Irish-language bonus tables 26–27, separate food-studies coursework 28–36, blank 37, back cover 38. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=58,expectedSectionTasks=dict(A=16,B=16,C=26),offeredPracticeMarks=749,candidateMarks=[280,320],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]
 r['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items() if not f.get('drop')]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


def build():
 d=documents();s={n:region_text(d['scheme'],r) for n,r in a_regions(d['scheme'],range(6,10),780).items()};old=originals();fixes={};added=[]
 def put(n,marks,notation,rows,**extra):
  fixes[f'he-2024-ol-sa-q{n}']=dict(reason='2024 Ordinary A independent paper/scheme review: complete prompts, exact tariffs and required pairings.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def after(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def split(n,suffix,prompt,marks,notation,rows):
  c=deepcopy(old[f'he-2024-ol-sa-q{n}']);c.update(id=f'he-2024-ol-sa-q{n}-{suffix}',conceptId=c['conceptId']+'-'+suffix,questionText=prompt,questionRef=f'2024 OL Section A Q{n} — {suffix}',totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Independent printed prompt with its own published tariff; original identity retains the first prompt.');added.append(c)
 for n,items in {1:[('Meat contains fibres and connective tissue',True),('1 g of protein provides 4 kilocalories of energy to the body',True),('Eggs are a low biological value food',False)],5:[('The bran layer of cereals is high in fibre',True),('Heat causes starch grains to swell and burst',True),('A roux sauce contains different amounts of fat and flour',False)]}.items():
  put(n,6,'3 statements × 2 (2:0)',[criterion(f'statement-{i}',text+' — '+('True' if correct else 'False'),1,[0,2],'Published answer, graded 2:0; no partial credit.') for i,(text,correct) in enumerate(items,1)],questionText='Indicate with a tick (✓) whether each of the following statements is true or false.\n\n'+'\n'.join(t for t,_ in items))
 put(2,4,'2 functions × 2 (2:1:0)',[criterion('functions','functions',2,[0,1,2],'Two functions, each graded 2:1:0. Source correction: vitamin C enhances absorption of non-haem iron; it does not convert it into haem iron. Historical prevention claims are not guarantees. Complete source wording: '+after(2,'(graded 2:1:0)','Name one dietary'))],questionText='State two functions of Vitamin C in the body.',questionRef='2024 OL Section A Q2 — functions')
 split(2,'source','Name one dietary source of Vitamin C.',2,'1 source × 2 (2:0)',[criterion('source','dietary source',1,[0,2],'One source, graded 2:0. Complete examples: '+after(2,'(graded 2:0)'))])
 put(3,6,'3 statements × 2 (2:0)',deepcopy(old['he-2024-ol-sa-q3']['rows']),questionText='Using the terms listed below, complete the following statements in relation to energy.\n\nempty kilocalories    energy balance    obesity\n\nOver indulgence in sugar-based foods can cause ______________________.\n______________________ are calories that have little nutritional value.\nEnergy input equals energy output is known as ______________________.')
 put(4,4,'2 factors × 2 (2:1:0)',[criterion('factors','factors',2,[0,1,2],'Two factors, each graded 2:1:0. Complete guidance: '+after(4,'(graded 2:1:0)','List two ways'))],questionText='Outline two factors that affect the tenderness of meat.',questionRef='2024 OL Section A Q4 — factors')
 split(4,'methods','List two ways of tenderising meat.',2,'2 ways × 1 (1:0)',[criterion('methods','ways',2,[0,1],'Two ways, each graded 1:0. The before-slaughter treatment is a historical industrial example, not a domestic preparation instruction. Complete wording: '+after(4,'(graded 1:0)'))])
 for n,label in [(6,'lifestyle changes'),(8,'guidelines'),(10,'consumer rights'),(11,'advantages'),(14,'guidelines')]:
  note={6:'Historical examination examples, not an individual weight-management plan. ',8:'Freezing capacity and fast-freeze timings depend on the appliance; follow its instructions. Cool cooked food promptly and maintain safe storage before freezing. ',10:'Historical examination summary, not current legal guidance. ',14:'Use cookware approved for the microwave and follow the appliance instructions. '}.get(n,'')
  put(n,6,'3 points × 2 (2:1:0)',[criterion('points',label,3,[0,1,2],'Three points, each graded 2:1:0. '+note+'Complete guidance: '+after(n,'(graded 2:1:0)').replace('-18oC','−18°C'))])
 examples='Types: choux; shortcrust; rough puff; puff; flaky; filo; suet; rich shortcrust; etc. Dishes: eclairs; profiteroles; apple tart; quiche; sausage rolls; steak and kidney pie; croissants; vol au vents; mince pies; spring rolls; steamed puddings; samosas; etc. Match each dish to an appropriate pastry type; the two table rows are illustrative lists, not prescribed combinations.';rows=[];groups=[]
 for i in range(1,3):
  rows += [criterion(f'type-{i}','Type of pastry',1,[0,2],f'Name pastry type {i}, graded 2:0. '+(examples if i==1 else 'Choose a different type.')),criterion(f'dish-{i}','Dish',1,[0,1],f'Name a different dish made from the same pastry type {i}, graded 1:0.')];groups.append(dict(sourceCardId=f'he-2024-ol-sa-q7-pair-{i}',label=f'Pastry and dish {i}',marks=3,rowIds=[f'type-{i}',f'dish-{i}']))
 put(7,6,'2 pairs × (type 2 (2:0) + dish 1 (1:0))',rows,taskGroups=groups)
 put(9,6,'3 matches × 2 (2:0)',deepcopy(old['he-2024-ol-sa-q9']['rows']),questionText='Match the following methods of heat transfer with the correct definition.\n\nConduction    Convection    Radiation\n\nHeat travels in straight lines and heats/cooks the first solid object it touches\nHeat travels through a liquid or gas, causing it to rise, cold liquid or gas moves in to take its place\nHeat travels through the molecules of a solid object until it is fully heated')
 values=named_sections(after(12,'(graded 2:1:0)'),['Suitability for purpose','Personal choice','Cost'])
 put(12,6,'3 required criteria × 2 (2:1:0)',[criterion(k,label,1,[0,1,2],'Explain this required criterion, graded 2:1:0. Complete guidance: '+value) for k,label,value in zip(['purpose','choice','cost'],['Suitability for purpose','Personal choice','Cost'],values)],questionText='Explain how the following criteria influence the consumer when selecting textiles for the household.\n\nSuitability for purpose\nPersonal choice\nCost')
 put(13,6,'2 benefits × 3 (3:2:0)',[criterion('benefits','benefits',2,[0,2,3],'Two benefits, each graded 3:2:0. Historical examples: savings and surrender value depend on policy type; not every policy can be cashed in. Complete wording: '+after(13,'(graded 3:2:0)'))])
 assert len(fixes)==14 and len(added)==2 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==84
 return fixes,added


def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=16,marks=84,selectionDecisions='Vitamin C functions/source and meat-tenderness factors/methods have independent printed prompts and tariffs. True/false grids, word bank, heat-transfer definitions, required textile headings and both pastry/dish pairs stay whole. All source examples retained.',sourceClarifications={'vitamin-c-iron':dict(source='https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/',note='Vitamin C enhances non-haem iron absorption; it does not change it into haem iron.')},checked='2026-11-01'));print('2024 Ordinary A: 16 reviewed tasks, 84 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))


