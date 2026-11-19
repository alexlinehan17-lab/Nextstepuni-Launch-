#!/usr/bin/env python3
"""Source-pinned 2021 Higher main review; shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='examiner-reports/home-economics/papers/2021-hl-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2021-hl-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2021/LC098ALP000EV.pdf'
HASHES={PAPER_A:'06bce3bc889da9318bda7bbc69c86a39da81c94cf21bb2c93ceddd77f64a49d6',PAPER_BC:'f8317b0dea9c8d80cbad97119c7b5f8bfc082f332365c2fd43bae30dd067713c',SCHEME:'881590c9b385c78977134367c09f1241e5d113f50e5fb7845b9a2b096f6c782b'}
REVIEW='scripts/markbank/authoring/home-economics/2021-hl-main-review.json'


def page_text(doc,n):
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,730 if doc.name.endswith('LC098ALP000EV.pdf') else 760)))


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 d=dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))
 pattern=r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b'
 expected_a={1:['two','one','each'],2:['each','following'],3:['one','following'],4:['two'],5:['three','one','each'],6:['two'],7:['each','following'],8:['two','two'],9:['following'],10:['following'],11:['three','one','each'],12:['three'],13:['three'],14:['two']}
 expected_bc={2:['one','each','following','two','two'],3:['one'],4:[],5:['or','one','or','either','or','either','or','following','or','three','each','two','or','or'],6:['either','or','one','or'],7:['either','or','each','following','one','or','or'],8:['either','or','five','one','or','two']}
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
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2021,level='higher',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–39, back cover 40.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 40 pages: cover 1, guidance/rubrics 2–4, A 5–9, B 10–17, C 18–28, explicit blank 29, separate food-studies coursework 30–38, blank 39, back cover 40. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=62,expectedSectionTasks=dict(A=16,B=18,C=28),offeredPracticeMarks=749,candidateMarks=[200,240],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]
 r['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items() if not f.get('drop')]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


def build():
 d=documents();s={n:region_text(d['scheme'],r) for n,r in a_regions(d['scheme'],range(5,10),730).items()};old=originals();fixes={};added=[]
 def put(n,marks,notation,rows,**extra):
  fixes[f'he-2021-hl-sa-q{n}']=dict(reason='Full 2021 Higher A source review: independent prompts, paired table criteria and exact published partial credit.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Source-pinned full review: he_review_2021_hl_main.py. Required headings and dependent pairs remain together.',**extra))
 def split(n,suffix,prompt,marks,notation,rows):
  c=deepcopy(old[f'he-2021-hl-sa-q{n}']);c.update(id=f'he-2021-hl-sa-q{n}-{suffix}',conceptId=c['conceptId']+'-'+suffix,questionRef=f'2021 HL Section A Q{n} — {suffix}',questionText=prompt,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Separately printed prompt with an independent published tariff. See he_review_2021_hl_main.py.');added.append(c)
 def paired(n,count,first,second,steps1,steps2,table):
  rows=[]
  for i in range(1,count+1):
   rows += [criterion(f'name-{i}',first,1,steps1,f'Pair {i}: name a different {first.lower()}. '+('Complete published table: '+table if i==1 else 'Use the complete guidance in the first pair.')),criterion(f'example-{i}',second,1,steps2,f'Pair {i}: give a matching {second.lower()} for the same named item. The two entries are marked separately.')]
  return rows
 # The table's acid/enzyme/salt labels are in a different PDF text stream; retain cell pairings explicitly.
 table='Heat: hard boiled eggs; omelette; quiche; egg custard; dry heat causes meat to shrink; collagen changes to gelatine in meat; browning of meat; etc. Mechanical action (e.g. whisking, beating): sponge cake; soufflés; meringues; etc. Chemicals: acids — cheese-making; vinegar in marinade tenderises meat; sour milk lactose changes to lactic acid; etc. Enzymes — rennin coagulates casein in the stomach; cheese-making; tenderising meat; etc. Salt — cheese-making.'
 put(1,6,'2 cause/example pairs × (2 (2:0) + 1 (1:0))',paired(1,2,'Cause','Example',[0,2],[0,1],table))
 values=named_sections(s[2].split('(graded 3:2:1:0)',1)[1],['(i) Oxidative rancidity','(ii) Hydrolytic rancidity'])
 put(2,6,'2 required explanations × 3 (3:2:1:0)',[criterion(k,label,1,[0,1,2,3],'Required explanation, graded 3:2:1:0. Complete guidance: '+v) for k,label,v in zip(['oxidative','hydrolytic'],['Oxidative rancidity','Hydrolytic rancidity'],values)])
 values=named_sections(s[3].split('Deficiency disease',1)[1],['Vitamin D','Vitamin B3 (Niacin)','Iodine'])
 put(3,6,'3 required nutrients × 2 (2:0)',[criterion(f'nutrient-{i}',label,1,[0,2],'One associated deficiency condition, graded 2:0. '+('Rickets/osteomalacia are clear vitamin-D-deficiency examples. Tooth decay involves acids produced by oral bacteria; do not treat it as simply a vitamin D deficiency. ' if i==1 else '')+'Complete historical guidance: '+v) for i,(label,v) in enumerate(zip(['Vitamin D','Vitamin B3 (Niacin)','Iodine'],values),1)])
 put(4,4,'Definition 4 (4:3:2:1:0)',[criterion('definition','Basal Metabolic Rate',1,list(range(5)),'Define BMR, graded 4:3:2:1:0. Complete guidance: '+between(s[4],'(graded 4:3:2:1:0)','Give two factors'))],questionText='What is Basal Metabolic Rate (BMR)?',questionRef='2021 HL Section A Q4 — definition')
 split(4,'factors','Give two factors that determine a person’s basal metabolic rate.',2,'2 factors × 1 (1:0)',[criterion('factors','factors',2,[0,1],'Two factors, each graded 1:0. Distinguish basal energy use from additional energy expended in activity. Complete historical guidance: '+s[4].split('(graded 1:0)',1)[1].strip())])
 for n,count,first,second,table in [(5,3,'Property','Culinary use',s[5].split('Property Culinary use',1)[1].strip()),(11,3,'Classification','Example',s[11].split('Retail Outlets Example',1)[1].strip())]:
  rows=paired(n,count,first,second,[0,1],[0,1],table)
  put(n,6,'3 paired responses × (1 + 1), each entry graded 1:0',rows,taskGroups=[dict(sourceCardId=f'he-2021-hl-sa-q{n}-pair-{i}',label=f'{first} {i}',marks=2,rowIds=[f'name-{i}',f'example-{i}']) for i in range(1,4)])
 put(6,6,'2 benefits × 3 (3:2:0)',[criterion('benefits','benefits',2,[0,2,3],'Two benefits, each graded 3:2:0. Complete guidance: '+s[6].split('(graded 3:2:0)',1)[1].strip())])
 values=named_sections(s[7].split('(graded 3:2:0)',1)[1],['Canning','Dehydration'])
 put(7,6,'2 required processes × 3 (3:2:0)',[criterion(k,label,1,[0,2,3],'Explain the effects of this process, graded 3:2:0. Effects depend on food and process conditions. Complete historical guidance: '+v) for k,label,v in zip(['canning','dehydration'],['Canning','Dehydration'],values)])
 put(8,2,'2 alternatives × 1 (1:0)',[criterion('alternatives','protein alternatives',2,[0,1],'Name two vegan alternatives, each graded 1:0. Check the actual product is vegan; not all mycoprotein products are. Complete examples: '+between(s[8],'(graded 1:0)','State two advantages'))],questionText='Name two protein alternatives that can be used in a vegan diet.',questionRef='2021 HL Section A Q8 — alternatives')
 split(8,'advantages','State two advantages of including protein alternatives in the diet.',4,'2 advantages × 2 (2:1:0)',[criterion('advantages','advantages',2,[0,1,2],'Two advantages, each graded 2:1:0. These depend on the particular food; the list is not a claim that every alternative has every property. Complete guidance: '+s[8].split('(graded 2:1:0)',1)[1].strip())])
 values=named_sections(s[9].split('(graded 3:2:1:0)',1)[1],['Enzymic browning.','Non-enzymic browning.'])
 put(9,6,'2 required changes × 3 (3:2:1:0)',[criterion(k,label,1,[0,1,2,3],'Explain this change, graded 3:2:1:0. Complete historical guidance: '+v) for k,label,v in zip(['enzymic','non-enzymic'],['Enzymic browning','Non-enzymic browning'],values)])
 values=named_sections(s[10],['Thermostat:','Refrigerant:'])
 put(10,6,'2 required functions × 3 (3:2:1:0)',[criterion(k,label,1,[0,1,2,3],'State this component’s function, graded 3:2:1:0. Complete guidance: '+v.replace('0 0C','0°C').replace('5 0C','5°C')) for k,label,v in zip(['thermostat','refrigerant'],['Thermostat','Refrigerant'],values)])
 for n,heading,count,steps,grade in [(12,'consumer responsibilities',3,[0,1,2],'2:1:0'),(13,'socio-economic factors',3,[0,1,2],'2:1:0'),(14,'benefits',2,[0,1,2,3],'3:2:1:0')]:
  put(n,6,f'{count} points × {steps[-1]} ({grade})',[criterion('points',heading,count,steps,f'{count} distinct points, each graded {grade}. '+('Historical 2021 examination guidance; fees, limits and procedure are not presented as current advice. ' if n==14 else '')+'Complete wording: '+s[n].split(f'(graded {grade})',1)[1].strip())])
 assert len(fixes)==14 and len(added)==2 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==84
 return fixes,added


def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=16,marks=84,selectionDecisions='Q4 definition/factors and Q8 alternatives/advantages are independent printed prompts with distinct tariffs. Q1/Q5/Q11 retain paired responses; all scheme examples remain available and are not a finite-choice restriction. All required nutrient, process and component headings stay together.',sourceClarifications={'vitamin-d':dict(source='https://www.nidcr.nih.gov/health-info/tooth-decay',note='Tooth decay is not simply a vitamin-D deficiency; oral bacterial acids cause decay.')},checked='2026-11-01'));print('2021 Higher A: 16 reviewed tasks, 84 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
