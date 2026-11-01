#!/usr/bin/env python3
"""2024 Ordinary B: full source review including the omitted nutrition/menu tasks."""
from copy import deepcopy
import json,re,sys
from he_review_2024_ol_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(10,16)};old=originals();fixes={};added=[]
 def put(n,part,marks,notation,rows,new=False,**extra):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' • ','\n• ');assert not re.search(r'\([a-e]\)',prompt)
  cid=f'he-2024-ol-sb-q{n}{part}';value=dict(questionText=prompt,questionRef=f'2024 OL Section B Q{n}({part})',stem=q[n].split('(a)',1)[0].strip(),totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Full independent source review: he_review_2024_ol_main_b.py. Preserve open choices, required headings and paired tasks.',**extra)
  if new:
   c=deepcopy(old['he-2024-ol-sb-q2c']);c.update(value,id=cid,conceptId='fruit-vegetable-nutritive-dietetic-value' if part=='a' else 'vegetarian-day-menu');added.append(c)
  else:fixes[cid]=dict(reason='2024 Ordinary B complete source review: exact partial credit, full headings and all guidance.',set=value)
 def body(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def points(n,part,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));put(n,part,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 points(1,'a',20,5,[0,2,4],body(10,'5 @ 4 marks (graded 4:2:0)','Factors affecting food choice'),label='factors',questionFigureKey='home-economics-2024-ol-sb-q1a-food-choice',questionFigureIncludesPrompt=False,figureKey='')
 put(1,'b',28,'Classification 3 × 2 (2:0); functions 2 × 5 (5:3:0); sources 3 × 4 (4:2:0)',[
  criterion('classification','classification',3,[0,2],'Three classes, each graded 2:0. Complete examples: '+body(11,'3 classes @ 2 marks (graded 2:0)','• functions')),
  criterion('functions','functions in the body',2,[0,3,5],'Two functions, each graded 5:3:0. Complete guidance: '+body(11,'2 functions @ 5 marks (graded 5:3:0)','• dietary')),
  criterion('sources','dietary sources',3,[0,2,4],'Three sources, each graded 4:2:0. Complete guidance: '+body(11,'3 sources @ 4 marks (graded 4:2:0)','(c)'))])
 points(1,'c',12,3,[0,2,4],body(11,'3 points @ 4 marks (graded 4:2:0)','(d)'))
 planning,purchasing=named_sections(body(11,'(1 reference to planning, 1 reference to purchasing, & 2 other points)'),['planning check','purchasing buy']);planning='check '+planning;purchasing='buy '+purchasing
 put(1,'d',20,'Planning 1 + purchasing 1 + other 2, each 5 (5:4:3:0)',[criterion('planning','planning',1,[0,3,4,5],'One planning point, graded 5:4:3:0. Complete guidance: '+planning),criterion('purchasing','purchasing',1,[0,3,4,5],'One purchasing point, graded 5:4:3:0. Complete guidance: '+purchasing),criterion('other','other points',2,[0,3,4,5],'Two further distinct points under either heading, each graded 5:4:3:0.')])
 nutrition,diet=named_sections(body(12,'(1 reference to nutritive value, 1 reference to dietetic value, & 2 other points)','(b)'),['nutritive LBV','dietetic used']);nutrition='LBV '+nutrition;diet='used '+diet
 put(2,'a',20,'Nutritive 1 + dietetic 1 + other 2, each 5 (5:4:3:2:0)',[criterion('nutrition','nutritive',1,[0,2,3,4,5],'One nutritive point, graded 5:4:3:2:0. Composition varies by food. Complete guidance: '+nutrition),criterion('dietetic','dietetic',1,[0,2,3,4,5],'One dietetic point, graded 5:4:3:2:0. Historical diet and disease examples are not an individual treatment plan or guaranteed prevention effects. Complete wording: '+diet),criterion('other','other points',2,[0,2,3,4,5],'Two further distinct points under either heading, each graded 5:4:3:2:0.')],new=True,topicId='home-economics-0-9')
 samples=['Orange juice *** Porridge with milk *** Tea/coffee/water/milk','Vegetable soup with wholemeal bread *** Strawberry yoghurt *** Glass of milk/water','Carrot and lentil soup with brown bread *** Vegetarian Lasagne with green salad *** Glass of milk/water'];rows=[];groups=[]
 for i,(label,sample) in enumerate(zip(['Breakfast','Lunch','Dinner'],samples),1):
  assert sample in s[12],sample
  rows += [criterion(f'courses-{i}','courses',2,[0,1,2],f'{label}: two suitable vegetarian food courses, each graded 2:1:0. Complete published sample for this meal (two courses plus one beverage): '+sample.replace(' ***',';')),criterion(f'beverage-{i}','beverage',1,[0,2],f'{label}: one suitable beverage, graded 2:0, not 2:1:0. The paper asks for a whole day of three meals; no extra course earns another slot.')]
  groups.append(dict(sourceCardId=f'he-2024-ol-sb-q2b-meal-{i}',label=label,marks=6,rowIds=[f'courses-{i}',f'beverage-{i}']))
 put(2,'b',18,'3 meals × (2 courses × 2 (2:1:0) + beverage 2 (2:0))',rows,new=True,taskGroups=groups,topicId='home-economics-0-10')
 points(2,'c',12,3,[0,2,4],'Apply storage conditions to the specific fruit or vegetable; the source lists different examples, not one temperature/humidity for every food. '+body(12,'3 ways @ 4 marks (graded 4:2:0)'),label='ways')
 points(3,'a',20,4,[0,3,5],body(13,'4 points @ 5 marks (graded 5:3:0)','(b)'))
 guidance=body(13,'(1 food @ 2 marks (graded 2:1:0)) X3','(c)');rows=[];groups=[]
 for i in range(1,4):
  rows += [criterion(f'sector-{i}','sectors',1,[0,2,3],f'Identify sector {i}, graded 3:2:0. '+('All six published sector/product examples: '+guidance if i==1 else 'Choose a different sector.')),criterion(f'food-{i}','food',1,[0,1,2],f'Give a product from the same sector {i}, graded 2:1:0.')];groups.append(dict(sourceCardId=f'he-2024-ol-sb-q3b-sector-{i}',label=f'Sector and product {i}',marks=5,rowIds=[f'sector-{i}',f'food-{i}']))
 put(3,'b',15,'3 pairs × (sector 3 (3:2:0) + product 2 (2:1:0))',rows,taskGroups=groups)
 labels=['suitability for purpose','environmental impact','as a source of consumer information'];values=named_sections(s[13].rsplit('(15 marks)',1)[1],labels)
 put(3,'c',15,'3 required roles × 5 (5:3:0)',[criterion(f'role-{i}',label,1,[0,3,5],'Evaluate this required role, graded 5:3:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 points(4,'a',20,4,[0,3,5],body(14,'4 factors @ 5 marks (graded 5:3:0)','(b)'),label='factors')
 points(4,'b',20,4,[0,3,5],'The fee, limits and deadlines below are historical 2024 scheme examples, not current legal advice. '+body(14,'4 points @ 5 marks (graded 5:3:0)','(c)'))
 points(4,'c',10,2,[0,3,5],'Answer about the Act named in the historical question; this is not a statement of current consumer law. '+body(14,'2 points @ 5 marks (graded 5:3:0)'))
 labels=['physical','emotional','social','economic'];heads=['physical provides','emotional safe','social teaches','economic support'];values=named_sections(body(15,'(20 marks)','(b)'),heads);values=[h.split(' ',1)[1]+' '+v for h,v in zip(heads,values)]
 put(5,'a',20,'4 required family functions × 5 (5:3:0)',[criterion(k,k,1,[0,3,5],'Describe this required function, graded 5:3:0. Historical examples, not assumptions about a particular family or a complete statement of legal duties. Complete guidance: '+value) for k,value in zip(labels,values)])
 values=named_sections(body(15,'3 points @ 5 marks (graded 5:3:0)','(c)'),['physical social welfare','social Early','economic social welfare']);values=[a+b for a,b in zip(['social welfare ','Early ','social welfare '],values)]
 put(5,'b',15,'3 required functions × 5 (5:3:0)',[criterion(k,k,1,[0,3,5],'Explain state support for this required function, graded 5:3:0. Historical examples; availability and eligibility vary. Complete guidance: '+value) for k,value in zip(['physical','social','economic'],values)])
 points(5,'c',15,3,[0,3,5],s[15].rsplit('3 points @ 5 marks (graded 5:3:0)',1)[1].strip())
 assert len(fixes)==14 and len(added)==2 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==280
 return fixes,added


def write():
 fixes,added=build();save_batch('B',fixes,added,dict(tasks=16,marks=280,selectionDecisions='Recover the whole fruit/vegetable nutritive-and-dietetic account with its 1/1/2 quota and the entire three-meal vegetarian menu. Menu food courses allow 2:1:0; beverages allow 2:0. Five of seven diagram factors remain one choice card. Sector/product pairs and required packaging and family headings remain whole.',checked='2026-11-01'));print('2024 Ordinary B: 16 reviewed tasks, 280 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
