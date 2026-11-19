#!/usr/bin/env python3
"""Recover five missing tasks after a complete 81-page source sweep."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred_c1 import after, named_sections
from he_review_2023_ol import card as previous_card

PAPER_A='examiner-reports/home-economics/papers/2022-ol-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2022-ol-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2022/LC098GLP000EV.pdf'
HASHES={PAPER_A:'d37643ef21753607e255f0afae544a1af0df497c8ed9e9795b33901547eb2354',PAPER_BC:'6fd83dce9dc39044b6284a9f16814c05c31b0dd9b6ed11c7b311e25ffc42b608',SCHEME:'5eed036a64a77bd7d9b68d47827bd21a81e385d751c82bab133a8cacc33e5286'}
REVIEW='scripts/markbank/authoring/home-economics/2022-ol-main-review.json'
FIGURES={
 'home-economics-2022-ol-sa-q14-symbols':dict(source=PAPER_A,page=7,bounds=[53,315,202,599],sha256='90d8c2d6644c2a27fa8adc091140bb44171917dadf0007a42cc84b77e2927197',alt='Two care symbols, in vertical order. Top: a crossed-out triangle. Bottom: a square containing one horizontal line.'),
 'home-economics-2022-ol-sb-q1a-milk':dict(source=PAPER_BC,page=2,bounds=[59,216,533,345],sha256='1b36e8fdb3b37bfcb8ffb59c9c9611b621fd4121bd4751b2dd0d2425592b5007',alt='Nutrition per 100 ml. Whole milk: 64 kcal, protein 3.4 g, carbohydrates 4.7 g, fat 3.5 g, calcium 119 mg, vitamin B12 0.4 µg. Super Milk Fat-free: 35 kcal, protein 3.3 g, carbohydrates 5.0 g, fat 0.2 g, calcium 160 mg, vitamin B12 0.4 µg.'),
}
CLARIFICATIONS={
 'milk-data':dict(source='Original paper table, B/C page 2',note='Super Milk Fat-free has more carbohydrate (5.0 g versus 4.7 g), not less as the scheme says. Vitamin B12 values are equal.'),
 'coeliac':dict(source='https://www.niddk.nih.gov/health-information/digestive-diseases/celiac-disease/definition-facts',note='Coeliac disease is an immune disorder triggered by gluten, not simply an inability to digest it.'),
 'bottling':dict(source='https://nchfp.uga.edu/how/general-canning-information/ensuring-safe-canned-foods/',note='Water-bath processing is not suitable for all vegetables: low-acid foods require a validated pressure-canning process. The source’s short examples are examination guidance, not complete preservation recipes.'),
}


def documents():
 for p,sha in HASHES.items(): assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 return dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))


def page_text(doc,n):
 p=doc[n-1];return tidy(p.get_text(clip=fitz.Rect(0,0,p.rect.width,810 if doc.page_count==37 else 760)))


def card(key,section,ref,topic,concept,question,stem,marks,notation,rows,page):
 c=previous_card(key,section,ref,topic,concept,question,stem,marks,notation,rows,page)
 c['id']=c['id'].replace('2023','2022');c['year']=2022;c['questionRef']=c['questionRef'].replace('2023','2022');c['sourceMaterial']['attribution']=c['sourceMaterial']['attribution'].replace('2023','2022');c['notes']='Independently checked against the 2022 Ordinary paper and full scheme. he_review_2022_ol.py records source hashes, response boundaries and source corrections.'
 return c


def build():
 d=documents();p2,p3=[page_text(d['bc'],n) for n in [2,3]];s10,s11,s13,s14=[page_text(d['scheme'],n) for n in [10,11,13,14]]
 q1=p2.rsplit('Question 1',1)[1];q2=between(p3,'Question 2','Question 3');q3=after(p3,'Question 3')
 prompts=[between(page_text(d['a'],7),'14.','(www.persilproclean.com)'),between(q1,'(a)','(20 marks)'),between(q2,'(a)','(20 marks)'),between(q2,'(b)','(18 marks)'),between(q3,'(a)','(24 marks)')]
 expected=[['each','following'],['four'],[],['one'],['one']]
 for prompt,tokens in zip(prompts,expected): assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b',prompt,re.I)==tokens,(prompt,tokens)
 assert '2 @ 3 marks (graded 3:2:0)' in s10 and 'Do not bleach.' in s10 and 'Dry flat.' in s10
 symbols=card('sa-q14','A','Q14','1-4','fabric-care-symbols',prompts[0],'',6,'2 symbols × 3 (3:2:0)',[criterion('top','Do not bleach',1,[0,2,3],'Meaning of the top symbol, graded 3:2:0.'),criterion('bottom','Dry flat',1,[0,2,3],'Meaning of the bottom symbol, graded 3:2:0.')],7);symbols.update(questionFigureKey='home-economics-2022-ol-sa-q14-symbols',questionFigureIncludesPrompt=False)
 milk=after(between(s11,'(a)','(b)'),'4 reasons @ 4 marks (graded 4:2:0)');whole,skim=named_sections(milk,['Whole milk:','Super milk fat-free:']);variants=[]
 for key,label,body in [('whole','Whole milk',whole),('fat-free','Super Milk Fat-free',skim)]:
  variants.append(dict(id=key,label=label,rows=[criterion('name','Name',1,[0,4],'Choose one of the two printed milks, graded 4:0. Selected route: '+label),criterion('reasons','reasons',4,[0,2,4],'Four distinct reasons for your choice, each graded 4:2:0. Source correction: Super Milk Fat-free has more carbohydrate (5.0 g versus 4.7 g), not less; both have 0.4 µg vitamin B12. Use the table values. Complete published guidance: '+body)]))
 bars=card('sb-q1a','B','Q1(a)','0-1','milk-comparison',prompts[1],'‘Milk is a staple food in the diets of Irish children.’ (www.nationaldairycouncil.ie)\n\nThe table below shows the nutritional content of whole milk and super milk fat-free per 100 ml.',20,'Name 4 (4:0); reasons 4 × 4 (4:2:0)',deepcopy(variants[0]['rows']),2);bars.update(answerVariants=variants,questionFigureKey='home-economics-2022-ol-sb-q1a-milk',questionFigureIncludesPrompt=False)
 nutritive,dietetic=named_sections(between(s13,'(a)','(b)'),['Nutritive:','Dietetic:'])
 cereals=card('sb-q2a','B','Q2(a)','0-9','cereals-nutritive-dietetic-value',prompts[2],q2.split('(a)',1)[0].strip(),20,'4 points × 5 (5:3:0): nutritive 1, dietetic 1, other 2',[
 criterion('nutritive','Nutritive',1,[0,3,5],'One required nutritive point, graded 5:3:0. Published guidance: '+nutritive),criterion('dietetic','Dietetic',1,[0,3,5],'One required dietetic point, graded 5:3:0. Source clarification: coeliac disease is an immune disorder triggered by gluten, not simply an inability to digest it. Published wording: '+dietetic),criterion('other','plus 2 others',2,[0,3,5],'Two further distinct points on either heading, each graded 5:3:0. Use the full guidance above without counting the same point twice.')],3)
 assert '2 courses @ 2 marks + 1 beverage @ 2 marks (graded 2:1:0)' in s13
 rows=[]
 samples=['Orange juice; Wholegrain cereal with milk; Strawberry yoghurt; Glass of milk','Brown roll with chicken and cheese; Apple; Bottle of water','Vegetable soup with brown bread; Spaghetti Bolognese with brown pasta; Glass of milk']
 for i,(name,x0,x1) in enumerate([('Breakfast',75,223),('Packed lunch',224,372),('Dinner',373,521)],1):
  sample=tidy(d['scheme'][12].get_text(clip=fitz.Rect(x0,399,x1,506))).replace(' ***',';')
  assert sample == samples[i-1], (name, sample)
  row=criterion(f'meal-{i}','Menu',3,[0,1,2],name+': provide two suitable food courses and one beverage; each element graded 2:1:0. Preserve the high-fibre, school-going-child brief. Complete published example: '+sample+(' The sample lists both orange juice and milk; the tariff still awards one beverage slot, not two.' if i==1 else ''))
  for part,label in zip(row['parts'],['First course','Second course','Beverage']):part['verbatim']=label
  rows.append(row)
 assert 'Strawberry yoghurt' in rows[0]['contextNote'] and 'Brown roll' in rows[1]['contextNote'] and 'brown pasta' in rows[2]['contextNote']
 menu=card('sb-q2b','B','Q2(b)','0-10','high-fibre-child-menu',prompts[3],q2.split('(a)',1)[0].strip(),18,'3 meals × (2 courses × 2 + beverage 2), all 2:1:0',rows,3)
 preserve=between(s14,'Name of preservation method:','(b)');names=between(preserve,'Name of preservation method:','Suitable foods:') if preserve.startswith('Name of preservation method:') else preserve.split('Suitable foods:',1)[0]
 foods=between(preserve,'Suitable foods:','Steps to carry out method of preservation:');steps=after(preserve,'Steps to carry out method of preservation:')
 labels=['jam/chutney making:','Bottling:','Drying:','Freezing:'];methods=named_sections(steps,labels);routes=[]
 for key,label,body in zip(['jam','bottling','drying','freezing'],['Jam / chutney making','Bottling','Drying','Freezing'],methods):
  note='Source clarification: boiling-water bottling is not suitable for all vegetables. Low-acid foods require a validated pressure-canning process. ' if key=='bottling' else ''
  routes.append(dict(id=key,label=label,rows=[criterion('name','Name',1,[0,2,3],'One named method, graded 3:2:0. Published method examples: '+names),criterion('foods','suitable foods',3,[0,3],'Three foods suitable for your chosen method, each graded 3:0. The source supplies one general list, not a claim that every food suits every process: '+foods),criterion('steps','steps',4,[0,2,3],'Four appropriate steps, each graded 3:2:0. '+note+'This is examination guidance, not a complete preservation recipe. Complete published process: '+body)]))
 routes.append(dict(id='another',label='Another valid method',rows=[criterion('name','Name',1,[0,2,3],'Name one valid method, graded 3:2:0. The paper leaves the choice open. Published names: '+names),criterion('foods','suitable foods',3,[0,3],'Three foods suitable for that method, each graded 3:0. General source examples: '+foods),criterion('steps','steps',4,[0,2,3],'Four accurate steps for the same method, each graded 3:2:0. The source prints no model for this alternative.')]))
 preservation=card('sb-q3a','B','Q3(a)','0-4','home-food-preservation-profile',prompts[4].replace(' \uf0b7 ','\n• '),q3.split('(a)',1)[0].strip(),24,'Name 3 (3:2:0); 3 foods × 3 (3:0); 4 steps × 3 (3:2:0)',deepcopy(routes[0]['rows']),3);preservation['answerVariants']=routes
 return [symbols,bars,cereals,menu,preservation]


def write():
 cards=build();p=ROOT/'scripts/markbank/authored/home-economics.json';saved=json.loads(p.read_text())
 for c in cards:
  i=next((i for i,old in enumerate(saved) if old['id']==c['id']),None)
  if i is None:saved.append(c)
  else:saved[i]=c
 p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text());figures={}
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';fitz.open(ROOT/spec['source'])[spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);sha=hashlib.sha256(target.read_bytes()).hexdigest();assert sha == spec['sha256'], 'Inspected crop changed';figures[key]=dict(spec)
  manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2022 Ordinary Level examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source crop, bounds {spec["bounds"]}, rendered at 2×; visually checked. SHA256 {sha}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 p=ROOT/REVIEW;old=json.loads(p.read_text()) if p.exists() else {}
 review=dict(schemaVersion=1,year=2022,level='ordinary',sitting='main',language='ev',status=old.get('status','partial-review; all-source-pages-visually-reviewed; browser-QA-pending'),sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 32 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–31, back cover 32.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 37 pages: cover 1, guidance/rubric/annotations 2–5, A 6–10, B 11–16, C 17–25, separate practical-coursework scheme 26–35, blank 36 and back cover 37. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=60,expectedSectionTasks=dict(A=16,B=16,C=28),offeredPracticeMarks=749,candidateMarks=[200,240],boundaryDecisions=['A2: separately marked lipid functions 4 and dietary source 2.', 'A11: credit advantages 4 and car-credit example 2 are independent.', 'C3(a)(i): poverty definition 4 is independent of the two required poverty terms (12).', 'A14: both required original care symbols remain one six-mark task.', 'B1(a): one choice card with two routes, original milk table and all published reasons.', 'B2(a): preserve one nutritive point, one dietetic point and two others.', 'B2(b): one whole-day menu with three meals; each has two food courses and one beverage, all graded 2:1:0.', 'B3(a): one open preservation profile; foods must match the selected process; retain all source steps.'],recoveryReview=dict(ids=[c['id'] for c in cards],figures=figures,sourceClarifications=CLARIFICATIONS,checked='2026-11-01'),tasks=old.get('tasks',[]))
 ids={c['id'] for c in cards};review['tasks']=[t for t in review['tasks'] if t['id'] not in ids]+[dict(id=c['id'],status='source-reviewed',section=c['section'],marks=c['totalMarks']) for c in cards]
 for key,value in old.items():
  if key.startswith('section') or key=='completion':review[key]=value
 p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');print('2022 Ordinary: five missing tasks restored; full source sweep recorded; existing cards still under review.')


if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
