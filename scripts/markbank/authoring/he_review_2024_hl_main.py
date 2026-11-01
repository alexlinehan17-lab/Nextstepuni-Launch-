#!/usr/bin/env python3
"""Source-pinned 2024 Higher main review; shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='examiner-reports/home-economics/papers/2024-hl-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2024-hl-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2024/LC098ALP000EV.pdf'
HASHES={PAPER_A:'8b69f7212d16dfb0e99a86f6779631a79a43123dc9d77fd7cb1c2c5146adf1b0',PAPER_BC:'d96c7c489e029bec11fdead0572ab327ae59e93b873ab123f9de75ae639c2d91',SCHEME:'baf9dcc0aef0b7abe6b58b1327196a29a39bb6b5065f2cdd2538a060f6a9ca13'}
REVIEW='scripts/markbank/authoring/home-economics/2024-hl-main-review.json'


def page_text(doc,n):
 cutoff=(740 if n>=27 else 780) if doc.name.endswith('LC098ALP000EV.pdf') else 760
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,cutoff)))


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 d=dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))
 pattern=r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b'
 expected_a={1:[],2:['two','two'],3:['following','one','each'],4:['two'],5:[],6:['each','following'],7:['two','one','one','each'],8:['each','following'],9:['two'],10:['following','one','each'],11:['one'],12:['each','following'],13:['two'],14:['two']}
 expected_bc={2:['any','two','each','four','three','one','each'],3:['each','following'],4:['two','two'],5:['or','one','or','either','or','either','or','three','each','each','following','three','each','or','three'],6:['either','or','or','one'],7:['either','or','three','each','one','or','or'],8:['either','or','one','or']}
 for n,r in a_regions(d['a'],range(3,8),760).items():assert re.findall(pattern,region_text(d['a'],r),re.I)==expected_a[n],n
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
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2024,level='higher',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–39, back cover 40.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 42 pages: cover 1, guidance/rubrics/annotations 2–5, A 6–10, B 11–17, C 18–29, Irish-language bonus tables 30–31, separate food-studies coursework 32–40, blank 41, back cover 42. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=58,expectedSectionTasks=dict(A=15,B=16,C=27),offeredPracticeMarks=749,candidateMarks=[280,320],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]
 r['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items() if not f.get('drop')]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


CLARIFICATIONS={
 'deamination':dict(source='https://openstax.org/books/organic-chemistry/pages/29-9-catabolism-of-proteins-deamination',note='After removal of the amino group, the remaining carbon skeleton enters energy metabolism; this is not oxidation of the carboxyl group alone.'),
 'iron':dict(source='https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/',note='Haem iron is iron combined with protoporphyrin IX. Non-haem iron is absorbed, although less bioavailable; do not equate haem/non-haem simply with ferrous/ferric.'),
 'toxins':dict(source='https://www.cdc.gov/staph-food-poisoning/about/index.htmL',note='Cooking may kill Staph bacteria without destroying their preformed toxin. The scheme’s boiling/reheating statements are not universal safety instructions.'),
 'incubation':dict(source='https://www.cdc.gov/food-safety/signs-symptoms/',note='Food-poisoning onset varies by organism; the scheme’s two-hour/over-twelve-hour distinction is not universal.')}


def build():
 d=documents();s={n:region_text(d['scheme'],r) for n,r in a_regions(d['scheme'],range(6,11),780).items()};old=originals();fixes={};added=[]
 def put(n,marks,notation,rows,**extra):
  fixes[f'he-2024-hl-sa-q{n}']=dict(reason='2024 Higher A independently source-reviewed: complete required tables, exact per-point grading, independent prompt boundary and factual source clarifications.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def after(n,token):assert token in s[n];return s[n].split(token,1)[1].strip()
 put(1,6,'3 points × 2 (2:1:0)',[criterion('deamination','points',3,[0,1,2],'Three points, each graded 2:1:0. Source clarification: after the amino group is removed, the remaining carbon skeleton can enter energy metabolism; the carboxyl group alone is not the entire energy-yielding residue. Complete historical wording: '+after(1,'(graded 2:1:0)'))])
 put(2,4,'2 functions × 2 (2:1:0)',[criterion('functions','functions',2,[0,1,2],'Two functions, each graded 2:1:0. Complete guidance: '+between(s[2],'(graded 2:1:0)','Identify two dietary'))],questionText='State two biological functions of Vitamin A.',questionRef='2024 HL Section A Q2 — functions')
 c=deepcopy(old['he-2024-hl-sa-q2']);c.update(id='he-2024-hl-sa-q2-sources',conceptId='vitamin-a-dietary-sources',questionRef='2024 HL Section A Q2 — sources',questionText='Identify two dietary sources of Vitamin A.',totalMarks=2,tariffModel=dict(kind='fixed',notation='2 sources × 1 (1:0)'),rows=[criterion('sources','sources',2,[0,1],'Two sources, each graded 1:0. Complete published examples: '+after(2,'(graded 1:0)'))],notes='Independent source-identification prompt with its own 2-mark tariff. Functions retain the original Q2 ID.');added.append(c)
 rows=[]
 for i,(label,description,sources) in enumerate([
  ('Haem iron','ferrous iron; soluble; easily absorbed; etc.','offal; red meat; meat products; chicken; etc.'),
  ('Non-haem iron','ferric iron; cannot be absorbed by the body; must be changed into ferrous to be absorbed; etc.','eggs; wholegrain flour; dark green vegetables; fish; legumes; nuts; seeds; etc.')],1):
  rows += [criterion(f'description-{i}','Description',1,[0,2],label+': description graded 2:0. Clarification: haem iron is bound to a porphyrin; non-haem iron is absorbed but less bioavailable. The categories are not simply synonyms for ferrous and ferric. Complete historical cell wording: '+description),criterion(f'source-{i}','Food source',1,[0,1],label+': one source graded 1:0. Complete examples: '+sources)]
 put(3,6,'2 required forms × (description 2 (2:0) + source 1 (1:0))',rows,questionText='Describe the following forms of iron and give one food source of each.\n\nHaem iron: description; food source\nNon-haem iron: description; food source',taskGroups=[dict(sourceCardId=f'he-2024-hl-sa-q3-form-{i}',label=name,marks=3,rowIds=[f'description-{i}',f'source-{i}']) for i,name in enumerate(['Haem iron','Non-haem iron'],1)])
 for n,label,count,steps,grade in [(4,'guidelines',2,[0,2,3],'3:2:0'),(9,'underlying principles',2,[0,1,2,3],'3:2:1:0'),(13,'features',2,[0,2,3],'3:2:0'),(14,'points',2,[0,2,3],'3:2:0')]:
  note={4:'Historical examination examples, not an individual treatment plan. ',9:'These are examination principles, not a complete preservation recipe. ',13:'Housing for All is the policy named in the 2024 paper; these are historical exam examples. '}.get(n,'')
  put(n,6,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. '+note+'Complete guidance: '+after(n,f'(graded {grade})').replace('100oC','100°C'))])
 # Preserve all source/product pairings; PDF extraction separates table columns.
 plant='Soya beans — TVP; tofu; soya milk/cheese/yoghurt/flour/sauce/oil; tempeh; miso. Peas — pea protein. Wheat — seitan. Nuts — nut butter. Seeds — pumpkin; sesame; etc.'
 microbes='Bacteria; fungi; yeast; algae; etc. Products: quorn/mycoprotein; nutritional yeast; etc. Match the product to its actual organism source; fungi produce mycoprotein, yeast produces nutritional yeast.'
 rows=[]
 for i,(label,text) in enumerate([('Plant',plant),('Micro-organisms',microbes)],1):
  rows += [criterion(f'source-{i}','Source',1,[0,2],label+': source graded 2:0. Complete paired guidance: '+text),criterion(f'product-{i}','Product',1,[0,1],label+': a matching product, graded 1:0. Use the complete guidance above.')]
 put(5,6,'2 required categories × (source 2 (2:0) + product 1 (1:0))',rows,questionText='Complete the table below in relation to alternative (novel) protein foods.\n\nPlant: source; product\nMicro-organisms: source; product',taskGroups=[dict(sourceCardId=f'he-2024-hl-sa-q5-category-{i}',label=name,marks=3,rowIds=[f'source-{i}',f'product-{i}']) for i,name in enumerate(['Plant','Micro-organisms'],1)])
 values=named_sections(after(6,'(graded 3:2:0)'),['Lactic acid bacteria','Rennet'])
 put(6,6,'2 required roles × 3 (3:2:0)',[criterion(k,label,1,[0,2,3],'Explain this required role, graded 3:2:0. Complete guidance: '+text) for k,label,text in zip(['bacteria','rennet'],['Lactic acid bacteria','Rennet'],values)],questionText='Explain the role of each of the following in the production of cheese.\n\nLactic acid bacteria\nRennet')
 table='Chemical: pesticides — source: insecticides/pesticides sprayed on crops/fruit/vegetables; run off water; etc.; effects: respiratory problems; heart/circulatory problems; damages nervous system; cancer; birth defects; etc. Antibiotics — source: consuming meat containing animal antibiotics; consuming milk containing animal antibiotics; etc.; effects: build up resistance to antibiotics; allergic reactions; etc. Growth promoters/hormones — source: consuming meat containing them; consuming milk containing them; etc.; effects: allergic reactions; etc. Dioxins — source: burning of hydrocarbons; dioxins transferred to soil/water; etc.; effects: immune system damage; cancer; etc. Urea formaldehyde — source: coating on paper-based packaging material; etc.; effects: cancer; etc. Metal residues, e.g. lead, copper, cadmium — source: transferred to food from water/soil/food containers; paint; lead pipes; burning batteries/fuel; etc.; effects: liver damage; kidney damage; nervous system damage; stomach cramps; etc. Biological: micro-organisms — source: undercooked meat; undercooked eggs; unwashed hands; soil; water; etc.; effects: food poisoning; etc. Physical: foreign bodies — source: food containing them due to poor storage; preparation; cooking; etc.; effects: choking hazard; food poisoning; etc.'
 rows=[]
 for i in range(1,3):
  for k,label in [('contaminant','Contaminant'),('source','Source'),('effect','Effect on the body')]:
   rows.append(criterion(f'{k}-{i}',label,1,[0,1],f'Contaminant {i}: {label.lower()} graded 1:0. Keep the source and effect paired with that contaminant. '+('Historical table describes possible hazards, not the risk from an ordinary regulated serving; effects depend on exposure. Complete published table: '+table if i==1 and k=='contaminant' else 'Use the full paired guidance in the first row.')))
 put(7,6,'2 contaminant/source/effect triples × (1 + 1 + 1), each 1:0',rows,taskGroups=[dict(sourceCardId=f'he-2024-hl-sa-q7-triple-{i}',label=f'Contaminant {i}',marks=3,rowIds=[f'contaminant-{i}',f'source-{i}',f'effect-{i}']) for i in range(1,3)])
 values=named_sections(after(8,'(graded 3:2:1:0)'),['Infectious food poisoning','Toxic food poisoning'])
 put(8,6,'2 required explanations × 3 (3:2:1:0)',[criterion(k,label,1,[0,1,2,3],'Explain this required type, graded 3:2:1:0. Source correction: cooking/reheating does not destroy every toxin, and boiling for 30 minutes is not a universal way to make contaminated food safe. Incubation times vary by organism. Complete historical wording: '+text) for k,label,text in zip(['infection','toxic'],['Infectious food poisoning','Toxic food poisoning'],values)])
 values=named_sections(after(10,'2 examples @ 1 mark (graded 1:0)'),['Social insurance payments','Social assistance payments']);rows=[]
 for i,(label,text) in enumerate(zip(['Social insurance payments','Social assistance payments'],values),1):
  rows += [criterion(f'explanation-{i}',label,1,[0,1,2],'Explain this required category, graded 2:1:0. Historical 2024 exam wording; eligibility rules vary by payment, and the printed 39-contribution example is not universal. Complete category guidance and examples: '+text),criterion(f'example-{i}','examples',1,[0,1],'Give one example of the same category, graded 1:0. Use the complete category-specific guidance above.')]
 put(10,6,'2 required categories × (explanation 2 (2:1:0) + example 1 (1:0))',rows,taskGroups=[dict(sourceCardId=f'he-2024-hl-sa-q10-pair-{i}',label=name,marks=3,rowIds=[f'explanation-{i}',f'example-{i}']) for i,name in enumerate(['Social insurance','Social assistance'],1)])
 agencies=after(11,'Role 1 point @ 3 marks (graded 3:2:0)')
 put(11,6,'Name 3 (3:2:0); role 3 (3:2:0)',[criterion('name','Name',1,[0,2,3],'Name one voluntary agency, graded 3:2:0. Historical 2024 names and roles: '+agencies),criterion('role','Role',1,[0,2,3],'Explain the role of the same agency, graded 3:2:0. Use the full guidance above; names and role are a dependent pair, not separate cards.')])
 values=named_sections(after(12,'(graded 3:2:1:0)'),['the condenser','the evaporator'])
 put(12,6,'2 required components × 3 (3:2:1:0)',[criterion(k,label,1,[0,1,2,3],'One function, graded 3:2:1:0. Complete historical guidance: '+text) for k,label,text in zip(['condenser','evaporator'],['the condenser','the evaporator'],values)])
 assert len(fixes)==14 and len(added)==1 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==84
 return fixes,added


def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=15,marks=84,selectionDecisions='Only A2 has independent functions/source prompts with separate tariffs. All required iron forms, novel-protein categories, poison types, welfare categories and refrigerator components stay whole. Two contaminant/source/effect triples retain their pairings and all eight source examples. A11 agency name and role are dependent, so remain one open response.',sourceClarifications=CLARIFICATIONS,checked='2026-11-01'));print('2024 Higher A: 15 reviewed tasks, 84 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))


