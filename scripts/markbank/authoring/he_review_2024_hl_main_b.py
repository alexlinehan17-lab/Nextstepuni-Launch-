#!/usr/bin/env python3
"""Full 2024 Higher B review, recovering sugar strategies and payment methods."""
from copy import deepcopy
import json,re,sys
from he_review_2024_hl_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections

CLARIFICATIONS={
 'folate':dict(source='https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/',note='The historical cancer/heart-attack/depression examples are not established universal prevention or treatment effects. Preserve the scheme, distinguish it from current health guidance.'),
 'pregnancy':dict(source='https://www.hse.ie/pregnancy-birth/keeping-well/food-drink/what-to-avoid/',note='The printed nutrient list is not a supplement prescription; avoid high-retinol vitamin A supplements and liver in pregnancy.')}


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1].split('63 52 36',1)[0],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(11,18)};old=originals();fixes={};added=[]
 def put(n,part,marks,notation,rows,new=False,**extra):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' • ','\n• ');assert not re.search(r'\([a-e]\)',prompt)
  cid=f'he-2024-hl-sb-q{n}{part}';value=dict(questionText=prompt,questionRef=f'2024 HL Section B Q{n}({part})',stem=q[n].split('(a)',1)[0].strip(),totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Full source-pinned paper/scheme review: he_review_2024_hl_main_b.py. Required headings and open choices remain whole responses.',**extra)
  if new:
   c=deepcopy(old[f'he-2024-hl-sb-q{n}a']);c.update(value,id=cid,conceptId='sugar-reduction-strategies' if n==1 else 'in-store-payment-methods');c.pop('questionFigureKey',None);c.pop('questionFigureIncludesPrompt',None);c['figureKey']='';added.append(c)
  else:fixes[cid]=dict(reason='2024 Higher B complete source review: all continuations, exact tariffs and whole choices.',set=value)
 def body(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1]
  assert end is None or end in t,(n,end)
  return (t.split(end,1)[0] if end else t).strip()
 def points(n,part,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));put(n,part,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 points(1,'a',20,4,list(range(6)),body(11,'(graded 5:4:3:2:1:0)','63 52 36'),label='factors',questionFigureKey='home-economics-2024-hl-sb-q1a-chart',questionFigureIncludesPrompt=False,figureKey='')
 put(1,'b',22,'Monosaccharide 8 (8–0); disaccharide 4 × 2; functions 3 × 2 (2:1:0)',[
  criterion('monosaccharide','basic structure of a monosaccharide',1,list(range(9)),'Required structure, graded 8:7:6:5:4:3:2:1:0. Original chemical drawing is retained in the solution figure. Complete guidance: '+body(12,'(graded 8:7:6:5:4:3:2:1:0)','• formation')),
  criterion('disaccharide','formation of disaccharides',4,[0,1,2],'Four formation points, each graded 2:1:0. Original condensation drawing retained in the solution figure. Complete guidance: '+body(12,'4 points @ 2 marks (graded 2:1:0)','• biological')),
  criterion('functions','biological functions',3,[0,1,2],'Three functions, each graded 2:1:0. Complete guidance: '+body(12,'3 points @ 2 marks (graded 2:1:0)','(c)'))],figureKey='home-economics-2024-hl-sb-q1b-chemistry',labelKey=[])
 properties=body(12,'x3')+' '+s[13].split('(d)',1)[0].removeprefix('13 ').strip();assert 'culinary application sponge cake' in properties and 'hydrolysis and inversion' in properties
 rows=[];groups=[]
 for i in range(1,4):
  rows += [criterion(f'name-{i}','Name',1,[0,2],f'Name sugar property {i}, graded 2:0. '+('Choose three distinct properties. Complete guidance for all seven properties, including the continued aeration example: '+properties if i==1 else 'Use the full seven-property guidance above.')),criterion(f'description-{i}','Description',1,[0,1,2],f'Describe your property {i}, graded 2:1:0.'),criterion(f'application-{i}','Culinary application',1,[0,1,2],f'Give one culinary example of the same property {i}, graded 2:1:0.')]
  groups.append(dict(sourceCardId=f'he-2024-hl-sb-q1c-property-{i}',label=f'Chosen property {i}',marks=6,rowIds=[f'name-{i}',f'description-{i}',f'application-{i}']))
 put(1,'c',18,'3 properties × (name 2 (2:0) + description 2 + application 2 (2:1:0))',rows,taskGroups=groups)
 purchasing,preparing=named_sections(body(13,'(1 point relating to purchasing, 1 point relating to preparing & 2 other points)'),['purchasing','preparing'])
 put(1,'d',20,'Purchasing 1 + preparing 1 + other 2, each 5 (5:3:0)',[criterion('purchasing','purchasing',1,[0,3,5],'One purchasing strategy, graded 5:3:0. Complete examples: '+purchasing),criterion('preparing','preparing',1,[0,3,5],'One preparing strategy, graded 5:3:0. Complete examples: '+preparing),criterion('other','other points',2,[0,3,5],'Two further distinct strategies under either heading, each graded 5:3:0; do not count a point twice.')],new=True,topicId='home-economics-0-1')
 points(2,'a',20,5,[0,2,4],'The printed list is historical exam guidance, not a supplement prescription: avoid high-retinol vitamin A supplements and liver during pregnancy. '+body(14,'5 dietary guidelines @ 4 marks (graded 4:2:0)','(b)'),label='dietary guidelines')
 put(2,'b',18,'Sources 3 × 2 (2:0); functions 3 × 2 (2:1:0); properties 3 × 2 (2:0)',[
  criterion('sources','sources',3,[0,2],'Three sources, each graded 2:0. Complete guidance: '+body(14,'3 sources @ 2 marks (graded 2:0)','• biological')),
  criterion('functions','biological functions',3,[0,1,2],'Three functions, each graded 2:1:0. Source clarification: the scheme’s cancer, heart-attack and depression examples are not established universal prevention or treatment effects. Complete historical wording: '+body(14,'3 functions @ 2 marks (graded 2:1:0)','• properties')),
  criterion('properties','properties',3,[0,2],'Three properties, each graded 2:0. Complete guidance: '+body(14,'3 properties @ 2 marks (graded 2:0)','(c)'))])
 points(2,'c',12,3,[0,2,4],body(14,'3 points @ 4 marks (graded 4:2:0)'))
 points(3,'a',20,5,[0,2,4],body(15,'5 points @ 4 marks (graded 4:2:0)','(b)'))
 points(3,'b',20,10,[0,1,2],'Cover production, packaging and labelling as required by the prompt. These are exam process examples, not a validated domestic recipe. '+body(15,'10 points @ 2 marks (graded 2:1:0)','(c)'))
 points(3,'c',10,2,[0,3,5],'The question explicitly asks about the historical 1950–1989 regulations; this is not a statement of current law. '+body(15,'2 points @ 5 marks (graded 5:3:0)'))
 points(4,'a',20,5,[0,2,4],'Interpret “the last decade” relative to the 2024 paper. '+body(16,'5 points @ 4 marks (graded 4:2:0)','(b)'))
 guidance=body(16,'[Name 3 marks (graded 3:2:0), 2 points @ 3 marks (graded 3:2:0)] x2','(c)');rows=[];groups=[]
 for i in range(1,3):
  rows += [criterion(f'name-{i}','name',1,[0,2,3],f'Name payment method {i}, graded 3:2:0. '+('Choose two different methods; complete historical examples and evaluation criteria: '+guidance if i==1 else 'Use the full examples above.')),criterion(f'evaluate-{i}','evaluate',2,[0,2,3],f'Two evaluations of the same method {i}, each graded 3:2:0. Refer to availability, ease of use, cost or safety; examples are not current product or fee advice.')]
  groups.append(dict(sourceCardId=f'he-2024-hl-sb-q4b-method-{i}',label=f'Chosen payment method {i}',marks=9,rowIds=[f'name-{i}',f'evaluate-{i}']))
 put(4,'b',18,'2 methods × (name 3 + 2 evaluations × 3), all 3:2:0',rows,new=True,taskGroups=groups)
 points(4,'c',12,3,[0,2,4],'Historical scheme summary of the Act named in the paper, not current legal guidance. '+body(16,'3 points @ 4 marks (graded 4:2:0)'))
 physical,psychological=named_sections(body(17,'(1 point relating to physical, 1 point relating to psychological & 2 other points)','(b)'),['physical food','psychological love']);physical='food '+physical;psychological='love '+psychological
 put(5,'a',20,'Physical 1 + psychological 1 + other 2, each 5 (5:3:1:0)',[criterion('physical','physical',1,[0,1,3,5],'One physical need, graded 5:3:1:0. Complete guidance: '+physical),criterion('psychological','psychological',1,[0,1,3,5],'One psychological need, graded 5:3:1:0. Complete guidance: '+psychological),criterion('other','other points',2,[0,1,3,5],'Two additional distinct needs under either heading, each graded 5:3:1:0.')])
 values=named_sections(body(17,'(1 point relating to social, economic & technological changes)','(c)'),['social decline','economic increased','technological automated']);values=[prefix+value for prefix,value in zip(['decline ','increased ','automated '],values)]
 put(5,'b',18,'3 required changes × 6 (6:4:2:0)',[criterion(k,k,1,[0,2,4,6],'Analyse this required category, graded 6:4:2:0. Complete guidance: '+v) for k,v in zip(['social','economic','technological'],values)])
 points(5,'c',12,2,[0,2,4,6],'Each response must identify a support and explain how it maintains independence; no separate name tariff is printed. These are historical examples and availability varies. '+body(17,'2 points @ 6 marks (graded 6:4:2:0)'))
 assert len(fixes)==14 and len(added)==2 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==280
 return fixes,added


def write():
 fixes,added=build();save_batch('B',fixes,added,dict(tasks=16,marks=280,sourceClarifications=CLARIFICATIONS,selectionDecisions='Recover the omitted sugar strategies and payment methods. Four of five chart factors, three sugar properties and two named payment methods each stay one choice response with all guidance. Preserve property/name/application and payment/name/evaluation pairings. Carbohydrate and folate bullet headings are required parts of one account. All original chart and chemical diagrams retained.',checked='2026-11-01'));print('2024 Higher B: 16 reviewed tasks, 280 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
