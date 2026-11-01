#!/usr/bin/env python3
"""Full B review, including the missing eggs/HACCP tasks and continued table."""
from copy import deepcopy
import json,sys,re,fitz
from he_review_2021_hl_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections,tidy
CLARIFICATIONS={
 'iron':dict(source='https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/',note='Vitamin C enhances non-haem iron absorption; it does not convert it into haem iron.'),
 'temperature':dict(source='https://www.fsai.ie/business-advice/running-a-food-business/caterers/temperature-control',note='FSAI cooking guidance is 75°C core or a validated equivalent; reheating at least 70°C. The historical scheme’s above-100°C reheating instruction is not the correct general target.'),
 'toxins':dict(source='https://www.safefood.net/getmedia/38eb7981-237a-4919-9a18-9373013363fe/IssuingTemperatureGuidanceToConsumersOnTheCookingAndStorageOfFood.pdf',note='Reheating does not necessarily eliminate toxins formed during unsafe cooling/storage; the scheme’s blanket toxin-destruction claims must not be used as safety instructions.'),
}
SAFETY='Source correction: FSAI recommends cooking to a 75°C core or a validated time/temperature equivalent and reheating to at least 70°C, not a general requirement to exceed 100°C. Keep chilled food at 0–5°C and hot-held food above 63°C. Historical examples below are not a complete food-safety procedure. '


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(10,18)};fixes={};added=[];old=originals()
 def put(n,part,marks,notation,rows,new=False,**extra):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' • ','\n• ');assert not re.search(r'\([a-e]\)',prompt)
  value=dict(questionText=prompt,questionRef=f'2021 HL Section B Q{n}({part})',stem=q[n].split('(a)',1)[0].strip(),totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Full source review: he_review_2021_hl_main_b.py. Required headings and open choices remain whole responses.',**extra);cid=f'he-2021-hl-sb-q{n}{part}'
  if new:
   c=deepcopy(old[f'he-2021-hl-sb-q{n}'+('b' if n==2 else 'a')]);c.update(value,id=cid,conceptId='eggs-nutritional-significance' if n==2 else 'haccp-hot-main-course');added.append(c)
  else:fixes[cid]=dict(reason='Full 2021 Higher B paper/scheme review, including every continuation and published tariff.',set=value)
 def body(t,grade):return t.split(f'(graded {grade})',1)[1].strip()
 v=named_sections(s[10].split('(graded 5:3:1:0)',1)[1],['(i) Health and wellbeing','(ii) Responsible living']);v[1]=v[1].removesuffix('42% 27%').strip()
 put(1,'a',20,'2 required headings × 2 points × 5 (5:3:1:0)',[criterion(f'heading-{i}',label,2,[0,1,3,5],'Two points under this required heading, each graded 5:3:1:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(['Health and wellbeing','Responsible living'],v),1)],questionFigureKey='home-economics-2021-hl-sb-q1a-chart',questionFigureIncludesPrompt=False,figureKey='')
 put(1,'b',12,'3 trends × 4 (4:2:0)',[criterion('trends','trends',3,[0,2,4],'Three trends, each graded 4:2:0. Historical 2021 question. Complete guidance: '+body(s[11].split('(c)',1)[0],'4:2:0'))])
 iron=between(s[11],'(c)','(d)');sources=between(iron,'Haem iron found','• biological functions');functions=between(iron,'3 functions @ 2 marks (graded 2:0)','• effects of deficiency');deficiency=iron.split('3 deficiencies @ 2 marks (graded 2:0)',1)[1].strip()
 put(1,'c',18,'Sources 3 × 2; functions 3 × 2; deficiency 3 × 2 (all 2:0)',[criterion('haem','haem iron',1,[0,2],'One haem source. Full source guidance: Haem iron found '+sources),criterion('non-haem','non-haem iron',1,[0,2],'One non-haem source, graded 2:0. Use the full source list above.'),criterion('other-source','1 other',1,[0,2],'A third different source from either class, graded 2:0.'),criterion('functions','biological functions',3,[0,2],'Three functions, each graded 2:0. Complete guidance: '+functions),criterion('deficiency','effects of deficiency',3,[0,2],'Three effects, each graded 2:0. Complete guidance: '+deficiency)])
 absorption=s[11].split('Factors that assist iron absorption',1)[1]+' Factors that inhibit iron absorption '+s[12].split('(e)',1)[0].split('Factors that inhibit iron absorption',1)[1]
 put(1,'d',10,'2 factors × 5 (5:4:3:2:1:0)',[criterion('factors','factors',2,list(range(6)),'Two explained factors, each graded 5:4:3:2:1:0. Source correction: vitamin C improves absorption of non-haem iron; it does not turn it into haem iron. The historical wording confuses these forms. Complete published assistance/inhibition guidance: '+absorption.strip())])
 purchasing,planning=named_sections(s[12].split('(graded 4:2:0)',1)[1],['Purchasing:','Planning:'])
 put(1,'e',20,'Purchasing 2 + planning 2 + other 1, each × 4 (4:2:0)',[criterion('purchasing','Purchasing',2,[0,2,4],'Two purchase strategies, each graded 4:2:0. Complete guidance: '+purchasing),criterion('planning','Planning',2,[0,2,4],'Two planning strategies, each graded 4:2:0. Complete guidance: '+planning),criterion('other','1 other point',1,[0,2,4],'One additional distinct strategy under either heading, graded 4:2:0. Do not count a point twice.')])
 put(2,'a',20,'5 points × 4 (4:3:2:1:0)',[criterion('nutrition','nutritional significance',5,list(range(5)),'Five developed points, each graded 4:3:2:1:0. The six nutrient headings are guidance, not six compulsory responses. Eggs suit ovo-/ovo-lacto-vegetarian diets; the scheme’s “lacto-vegetarians” wording is inaccurate. Complete historical guidance: '+body(between(s[13],'(a)','(b)'),'4:3:2:1:0'))],new=True,topicId='home-economics-0-9')
 emulsion=between(s[13],'An emulsifier lecithin','Culinary application:');application=between(s[13],'Culinary application:','(c)')
 put(2,'b',18,'Explanation 5 × 3 (3:2:0) + application 3 (3:0)',[criterion('emulsifier','emulsifier',5,[0,2,3],'Five explanation points, each graded 3:2:0. Complete guidance: An emulsifier lecithin '+emulsion),criterion('application','Culinary application',1,[0,3],'One matching application, graded 3:0. The example illustrates the explanation; retain this as one task. Complete examples: '+application)])
 put(2,'c',12,'3 points × 4 (4:2:0)',[criterion('labelling','food labelling',3,[0,2,4],'Three points, each graded 4:2:0. Historical scheme examples are not a statement of current labelling law. A quality mark is not an absolute guarantee of pathogen absence. Complete wording: '+body(s[13].split('(c)',1)[1],'4:2:0'))])
 storage,cooking=named_sections(between(s[14],'(a)','(b)'),['Storage:','Cooking/Reheating:'])
 put(3,'a',16,'Storage 2 + cooking/reheating 2, each × 4 (4:2:0)',[criterion('storage','Storage',2,[0,2,4],'Two storage points, each graded 4:2:0. '+SAFETY+'Complete historical guidance: '+storage),criterion('cooking','Cooking/Reheating',2,[0,2,4],'Two cooking/reheating points, each graded 4:2:0. '+SAFETY+'Complete historical guidance: '+cooking)])
 # Read the three table columns separately and join the Preparation continuation.
 stages=[]
 for name,regions in [('Purchase',[(14,423,523)]),('Transportation',[(14,524,595)]),('Storage',[(14,596,693)]),('Preparation',[(14,694,724),(15,54,264)]),('Cooking',[(15,265,349)]),('Serving',[(15,350,393)]),('Reheating / hot holding',[(15,394,494)])]:
  cells=[' '.join(tidy(d['scheme'][page-1].get_text(clip=fitz.Rect(left,top,right,bottom))) for page,top,bottom in regions) for left,right in [(66,152),(153,265),(266,559)]]
  assert tidy(cells[0])==name,(name,cells);assert cells[1] and cells[2]
  stages.append(f'{name} — hazards: {cells[1]} Control measures: {cells[2]}')
 table='\n\n'.join(stages);assert 'Hands washed' in table and 'after handling food' in table and 'Hold cooked food' in table
 rows=[];groups=[]
 for i in range(1,5):
  rows.extend([criterion(f'stage-{i}','Stages',1,[0,1],f'Name stage {i} of your HACCP plan, graded 1:0. '+('All seven published stage examples follow; choose four relevant stages. '+SAFETY+'Complete two-page table: '+table if i==1 else 'Use the complete source table in Stage 1.')),criterion(f'hazard-{i}','Hazards',1,[0,1,2],f'Potential hazard for your stage {i}, graded 2:1:0.'),criterion(f'control-{i}','Control Measures',1,[0,1,2,3],f'Corresponding control for the same hazard and stage {i}, graded 3:2:1:0.')]);groups.append(dict(sourceCardId=f'he-2021-hl-sb-q3b-stage-{i}',label=f'HACCP stage {i}',marks=6,rowIds=[f'stage-{i}',f'hazard-{i}',f'control-{i}']))
 put(3,'b',24,'4 stages × (name 1 + hazard 2 + control 3)',rows,new=True,taskGroups=groups)
 infectious,toxic=named_sections(s[15].split('(c)',1)[1],['Infectious food poisoning -','Toxic food poisoning -'])
 put(3,'c',10,'2 required distinctions × 5 (5:3:2:0)',[criterion(k,label,1,[0,2,3,5],'Explain this side of the distinction, graded 5:3:2:0. Infection involves ingesting pathogens; intoxication involves toxins in food. Organisms, toxins and incubation times differ; reheating cannot reliably make mishandled food safe. The scheme’s general claims about destroying toxins and fixed onset times are inaccurate. Complete historical wording: '+v) for k,label,v in zip(['infection','intoxication'],['Infectious food poisoning','Toxic food poisoning'],[infectious,toxic])])
 put(4,'a',16,'4 points × 4 (4:2:0)',[criterion('management','management systems',4,[0,2,4],'Four points, each graded 4:2:0. Complete guidance: '+body(between(s[16],'(a)','(b)'),'4:2:0'))])
 v=named_sections(between(s[16],'(b)','(c)'),['Inputs –','Throughputs –','Outputs –'])
 put(4,'b',18,'3 required headings × 2 points × 3 (3:2:1:0)',[criterion(f'heading-{i}',label,2,[0,1,2,3],'Two points for this heading applied to the family holiday, each graded 3:2:1:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(['Inputs','Throughputs','Outputs'],v),1)])
 put(4,'c',16,'4 evaluation points × 4 (4:2:0)',[criterion('credit','credit',4,[0,2,4],'Four evaluation points, each graded 4:2:0. No compulsory advantages/disadvantages quota is printed. Historical examples; fees and charges are not presented as current rules. Complete guidance: '+body(s[16].split('(c)',1)[1],'4:2:0'))])
 definition,universality=named_sections(between(s[17],'(a)','(b)'),['Definition @ 5 marks (graded 5:3:0)','Universality @ 5 marks (graded 5:3:0)'])
 put(5,'a',10,'Definition 5 + universality 5 (5:3:0)',[])
 fixes['he-2021-hl-sb-q5a']['set'].update(questionText='Define the term ‘family’.',questionRef='2021 HL Section B Q5(a) — definition',totalMarks=5,tariffModel=dict(kind='fixed',notation='Definition 5 (5:3:0)'),rows=[criterion('definition','Definition',1,[0,3,5],'Define family, graded 5:3:0. The source definitions are historical examples and do not exhaust the forms families can take. Complete guidance: '+definition)])
 c=deepcopy(old['he-2021-hl-sb-q5a']);c.update(id='he-2021-hl-sb-q5a-universality',conceptId='family-universality',questionText='Explain the concept of the universality of the family.',questionRef='2021 HL Section B Q5(a) — universality',stem=q[5].split('(a)',1)[0].strip(),totalMarks=5,tariffModel=dict(kind='fixed',notation='Explanation 5 (5:3:0)'),rows=[criterion('universality','Universality',1,[0,3,5],'Explain universality, graded 5:3:0. Complete guidance: '+universality)],notes='Independent explanation with a separate published tariff; original Q5(a) identity retains the definition.');added.append(c)
 v=named_sections(between(s[17],'(b)','(c)'),['Physical -','Emotional -','Economic -','Social -'])
 put(5,'b',24,'4 required needs × 6 (6:4:2:0)',[criterion(f'need-{i}',label,1,[0,2,4,6],'Explain this required need, graded 6:4:2:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(['Physical','Emotional','Economic','Social'],v),1)])
 put(5,'c',16,'4 challenges × 4 (4:2:0)',[criterion('challenges','challenges',4,[0,2,4],'Four possible challenges, each graded 4:2:0. Individual families’ circumstances vary; these are examples, not assumptions about every disabled child or family. Complete guidance: '+body(s[17].split('(c)',1)[1],'4:2:0'))])
 assert len(fixes)==15 and len(added)==3 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==280
 return fixes,added


def write():
 fixes,added=build();save_batch('B',fixes,added,dict(tasks=18,marks=280,sourceClarifications=CLARIFICATIONS,selectionDecisions='Egg nutrition and HACCP were absent. The whole four-stage HACCP response retains stage/hazard/control pairings and all seven model stages, including the Preparation continuation. Family definition and universality are independently practicable, separately priced concepts. Required headings and the emulsification explanation with its illustrative application remain whole tasks.',checked='2026-11-01'));print('2021 Higher B: 18 reviewed tasks, 280 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
