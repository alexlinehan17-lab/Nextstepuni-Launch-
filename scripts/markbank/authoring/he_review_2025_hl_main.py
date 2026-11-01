#!/usr/bin/env python3
"""Source-pinned 2025 Higher main review; shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='examiner-reports/home-economics/papers/2025-hl-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2025-hl-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2025/LC098ALP000EV.pdf'
HASHES={'examiner-reports/home-economics/papers/2025-hl-014-paper.pdf': 'ba1c8a8406190cfdad6fa5a727477d06605d1f31c1bb9b3d309fa1ce6f39a779', 'examiner-reports/home-economics/papers/2025-hl-039-paper.pdf': '0e736bbcd3fec699c6383fa2edb6b0f61370cb30d7fecfc0860df40754e1a956', 'paper-trail-corpus/markingschemes/2025/LC098ALP000EV.pdf': '00ee82fb17ba14cbbfd1d36cfbcce58e61685510f4986fb328d97891b3f0abee'}
REVIEW='scripts/markbank/authoring/home-economics/2025-hl-main-review.json'


def page_text(doc,n):
 cutoff=780 if doc.name.endswith('LC098ALP000EV.pdf') else (760 if doc.name.endswith('2025-hl-039-paper.pdf') else 740)
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,cutoff)))


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 d=dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))
 pattern=r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b'
 expected_a={1: ['two'], 2: [], 3: ['two', 'two'], 4: ['Each', 'following', 'one', 'each'], 5: ['three'], 6: ['or', 'each'], 7: ['following'], 8: ['one'], 9: ['two', 'each'], 10: ['one'], 11: ['one', 'each'], 12: ['each', 'following'], 13: ['two'], 14: []}
 expected_bc={2: ['any', 'two', 'each', 'four', 'one', 'each', 'following'], 3: ['one'], 4: ['one', 'three', 'each'], 5: ['or', 'one', 'or', 'either', 'or', 'either', 'or', 'each', 'following', 'or', 'each'], 6: ['either', 'or', 'one', 'either', 'two', 'one', 'or', 'three'], 7: ['either', 'or', 'one', 'or', 'each', 'following'], 8: ['either', 'or', 'two', 'four', 'one', 'or', 'three']}
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
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2025,level='higher',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–39, back cover 40.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 44 pages: cover 1, guidance/rubrics/annotations 2–5, A 6–10, B 11–18, C 19–30, separate food-studies coursework 31–42, blank 43, back cover 44. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=61,expectedSectionTasks=dict(A=15,B=18,C=28),offeredPracticeMarks=749,candidateMarks=[280,320],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]
 r['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items() if not f.get('drop')]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


def build():
 d=documents();s={n:region_text(d['scheme'],r) for n,r in a_regions(d['scheme'],range(6,11),780).items()};old=originals();fixes={};added=[]
 def put(n,marks,notation,rows,**extra):
  fixes[f'he-2025-hl-sa-q{n}']=dict(reason='2025 Higher A full source review: complete prompts and tables, exact published tariffs and every model route.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def after(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 put(1,6,'2 functions × 3 (3:2:0)',[criterion('functions','functions',2,[0,2,3],'Two developed functions, each graded 3:2:0. Complete guidance: '+after(1,'(graded 3:2:0)'))])
 put(2,6,'3 required cells × 2 (2:1:0)',[criterion(k,label,1,[0,1,2],note) for k,label,note in [('enzyme','Enzyme','Pancreas enzyme: Trypsin, Tripsin, Proteinase, etc. Graded 2:1:0.'),('substrate','Substrate','Substrate: Peptones. Graded 2:1:0.'),('product','Product/Result','Product/result: Peptides. Graded 2:1:0.')]],questionText='Complete the table below in relation to the digestion of protein.\nOrgan: Pancreas. Complete: Enzyme; Substrate; Product/Result.')
 put(3,4,'2 functions × 2 (2:1:0)',[criterion('functions','functions',2,[0,1,2],'Two functions, each graded 2:1:0. Source examples describe biological roles, not a recommendation to increase sodium intake. Complete wording: '+after(3,'(graded 2:1:0)','Identify two'))],questionText='State two biological functions of sodium.',questionRef='2025 HL Section A Q3 — functions')
 c=deepcopy(old['he-2025-hl-sa-q3']);c.update(id='he-2025-hl-sa-q3-sources',conceptId=c['conceptId']+'-sources',questionText='Identify two dietary sources of sodium.',questionRef='2025 HL Section A Q3 — sources',totalMarks=2,tariffModel=dict(kind='fixed',notation='2 sources × 1 (1:0)'),rows=[criterion('sources','sources',2,[0,1],'Two sources, each graded 1:0. Complete examples: '+after(3,'(graded 1:0)'))],notes='Independent source prompt and tariff; original ID retains the functions prompt.');added.append(c)
 put(4,6,'3 required vitamins × 2 (2:1:0)',[
  criterion('night','Night blindness',1,[0,1,2],'Vitamin A (retinol); the source also accepts beta-carotene, a precursor. Graded 2:1:0.'),
  criterion('rickets','Rickets',1,[0,1,2],'Vitamin D (cholecalciferol/ergocalciferol). Graded 2:1:0. Source clarification: vitamin D deficiency is the standard vitamin-deficiency cause of rickets. The historical table additionally lists B12 (cobalamin), K and C; do not present these as interchangeable causes of vitamin-D-deficiency rickets.'),
  criterion('beriberi','Beriberi',1,[0,1,2],'Vitamin B1 (thiamine), graded 2:1:0.')],questionText=old['he-2025-hl-sa-q4']['questionText']+'\nNight blindness: ____\nRickets: ____\nBeri-beri: ____')
 put(5,6,'3 guidelines × 2 (2:1:0)',[criterion('guidelines','guidelines',3,[0,1,2],'Three distinct guidelines, each graded 2:1:0. Complete source guidance: '+after(5,'(graded 2:1:0)'))])
 labels=['Cold smoking','Hot smoking'];values=named_sections(after(6,'(graded 3:2:1:0)'),labels)
 put(6,6,'2 required methods × 3 (3:2:1:0)',[criterion(str(i),label,1,[0,1,2,3],'Explain this required method, graded 3:2:1:0. Historical industrial examples, not a validated home-preservation recipe. Cold smoking does not cook fish, but some products are sold ready to eat; follow product instructions. People who are pregnant or immunocompromised should avoid ready-to-eat cold-smoked fish unless cooked until steaming hot. Complete historical wording: '+value) for i,(label,value) in enumerate(zip(labels,values))])
 labels=['Added value foods','Functional foods'];values=named_sections(after(7,'(graded 3:2:1:0)'),labels)
 put(7,6,'2 required explanations × 3 (3:2:1:0)',[criterion(str(i),label,1,[0,1,2,3],'Explain the required term, graded 3:2:1:0. Source examples are not guarantees of a health effect for every product. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values))])
 # Read the two independent columns separately: PDF reading order interleaves them.
 variants=[]
 for name,top,bottom in [('Conduction',151,210),('Convection',210,298.5),('Radiation',298.5,358.2)]:
  page=d['scheme'][7];desc=tidy(page.get_text(clip=fitz.Rect(160,top,392,bottom)));examples=tidy(page.get_text(clip=fitz.Rect(394,top,550,bottom)))
  assert desc.startswith('transfer of heat') and examples,(name,desc,examples)
  variants.append(dict(id=name.lower(),label=name,rows=[criterion('name','Name of method',1,[0,1,2],'Name '+name+', graded 2:1:0.'),criterion('description','Description of method of heat transfer',1,[0,1,2,3],'One developed description, graded 3:2:1:0. Accept a labelled diagram. Complete guidance: '+desc),criterion('example','Example',1,[0,1],'Give an example that demonstrates the SAME chosen method, graded 1:0. A cooking process can involve several modes; explain the relevant transfer. Complete source examples: '+examples)]))
 put(8,6,'Name 2 (2:1:0) + description 3 (3:2:1:0) + matched example 1 (1:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 rows=[];groups=[];guidance=after(9,'Function @ 1 mark (graded 1:0) x 2')
 for i in [1,2]:
  rows += [criterion(f'name-{i}','Name',1,[0,1,2],f'Name distinct physical conditioning agent {i}, graded 2:1:0. '+('All ten printed agents and functions: '+guidance if i==1 else 'Refer to the complete guidance above.')),criterion(f'function-{i}','Function',1,[0,1],f'Give the function of the SAME agent {i}, graded 1:0.')];groups.append(dict(sourceCardId=f'he-2025-hl-sa-q9-pair-{i}',label=f'Agent and function {i}',marks=3,rowIds=[f'name-{i}',f'function-{i}']))
 put(9,6,'2 pairs × (name 2 (2:1:0) + function 1 (1:0))',rows,taskGroups=groups)
 names=['Term life assurance','Whole of life assurance','Endowment life assurance','Mortgage protection policy','Convertible term assurance'];values=named_sections(after(10,'1 point @ 3 marks (graded 3:2:0)'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  variants.append(dict(id=str(i),label=name,rows=[criterion('name','type',1,[0,2,3],'Name the chosen type, graded 3:2:0. Model: '+name),criterion('description','point',1,[0,2,3],'One developed description of the SAME type, graded 3:2:0. Historical policy examples: payouts, surrender rights, exclusions and mortgage-protection requirements depend on contract and applicable rules. Complete wording: '+value)]))
 other=deepcopy(variants[0]['rows']);other[0]['contextNote']='Name another valid life-assurance type, graded 3:2:0.';other[1]['contextNote']='Describe that same type accurately, graded 3:2:0. No additional model is printed.';variants.append(dict(id='another',label='Another valid type',rows=other))
 put(10,6,'Name 3 (3:2:0) + description 3 (3:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 labels=['Essential expenditure','Discretionary expenditure'];values=named_sections(after(11,'2 examples @ 1 mark (graded 1:0)'),labels);rows=[];groups=[]
 for i,(label,value) in enumerate(zip(labels,values),1):
  desc,examples=value.split('example ',1);rows += [criterion(f'definition-{i}',label,1,[0,2],'Explain the required category, graded 2:0. '+desc),criterion(f'example-{i}','example',1,[0,1],'Example for the SAME category, graded 1:0. '+examples)];groups.append(dict(sourceCardId=f'he-2025-hl-sa-q11-pair-{i}',label=label,marks=3,rowIds=[f'definition-{i}',f'example-{i}']))
 put(11,6,'2 required pairs × (definition 2 (2:0) + example 1 (1:0))',rows,taskGroups=groups)
 labels=['Desk research','Field research'];values=named_sections(after(12,'(graded 3:2:1:0)'),labels)
 put(12,6,'2 required descriptions × 3 (3:2:1:0)',[criterion(str(i),label,1,[0,1,2,3],'Describe this required research type, graded 3:2:1:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values))])
 put(13,6,'2 techniques × 3 (3:2:1:0)',[criterion('points','points',2,[0,1,2,3],'Describe how two different techniques influence buying behaviour, each graded 3:2:1:0. Naming alone does not answer the prompt. Complete source examples: '+after(13,'(graded 3:2:1:0)'))])
 put(14,6,'2 points × 3 (3:2:0)',[criterion('points','points',2,[0,2,3],'Two discussed points, each graded 3:2:0. Answer about the Act named in the historical examination; this is not a current legal checklist. Complete guidance: '+after(14,'(graded 3:2:0)'))])
 assert len(fixes)==14 and len(added)==1 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==84
 return fixes,added


def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=15,marks=84,selectionDecisions='Sodium functions and sources have separate printed prompts/tariffs. All required table cells, disease rows, terms, smoking methods, budget categories and research types remain whole. Heat transfer and life assurance keep one open profile each, with dependent examples. Physical-conditioning agents keep two paired slots and all ten source models.',sourceClarifications={'rickets':dict(source='https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/',note='Vitamin D deficiency causes nutritional rickets; distinguish the extra historical table acceptances.'),'smoked-fish':dict(source='https://www2.hse.ie/conditions/listeriosis/',note='Cold-smoked fish may be sold ready to eat; pregnancy/immunocompromise advice and product cooking instructions remain relevant.')},checked='2026-11-01'));print('2025 Higher A: 15 reviewed tasks, 84 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))

