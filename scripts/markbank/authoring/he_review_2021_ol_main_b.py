#!/usr/bin/env python3
"""All 2021 Ordinary Section B tasks, including three omissions and one split."""
from copy import deepcopy
import json,sys
import fitz
from he_review_2021_ol_main import ROOT,documents,page_text,originals,save_batch,card,criterion,tidy,between,named_sections

CLARIFICATIONS={
 'lipids':dict(source='https://www.ncbi.nlm.nih.gov/books/NBK9928/',note='Lipids are components of human cell membranes, not cell walls.'),
 'pregnancy':dict(source='https://www.hse.ie/pregnancy-birth/keeping-well/food-drink/what-to-avoid/',note='Avoid raw/undercooked eggs and unpasteurised dairy; the historical wording reduce intake is inadequate. HSE limits caffeine to 200 mg daily.'),
 'pate':dict(source='https://www2.hse.ie/conditions/listeriosis/',note='Pregnancy food-safety guidance advises avoiding all types of pâté.')}


def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(9,15)};p={n:page_text(d['bc'],n) for n in range(2,5)};old=originals();fixes={};added=[]
 def put(key,marks,notation,rows,**extra):
  fixes['he-2021-ol-sb-'+key]=dict(reason='Full 2021 Ordinary B review: exact published tariffs, required headings, whole dependent choices and complete guidance.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def body(n,start,end=None):
  assert start in s[n],(n,start)
  text=s[n].split(start,1)[1]
  assert end is None or end in text,(n,end)
  return (text.split(end,1)[0] if end else text).strip()
 def points(key,marks,count,steps,text,label='points',**extra):
  grade=':'.join(str(n) for n in reversed(steps));put(key,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 yogurt=named_sections(body(9,'Reasons: 4 @ 4 marks each (graded 4:2:0)'),['Full fat natural yoghurt:','Low fat natural yoghurt:','Fat free natural yoghurt:']);variants=[]
 for key,label,text in zip(['full-fat','low-fat','fat-free'],['Full fat natural yoghurt','Low fat natural yoghurt','Fat free natural yoghurt'],yogurt):
  variants.append(dict(id=key,label=label,rows=[criterion('name','Name',1,[0,4],'Name the chosen yoghurt, graded 4:0. The scheme provides guidance for each of the three printed options.'),criterion('reasons','reasons',4,[0,2,4],'Four reasons tied to the same choice and the table, each graded 4:2:0. Interpret these historical food-comparison points in the printed brief; a listed nutrient is not automatically a reason to recommend the option. Complete scheme guidance: '+text)]))
 c=card('sb-q1a','B','Q1(a)','0-1','yoghurt-comparison',between(p[2],'(a)','(20 marks)'),p[2].rsplit('Question 1',1)[1].split('Full fat',1)[0].strip(),20,'Name 4 (4:0); 4 reasons × 4 (4:2:0)',deepcopy(variants[0]['rows']),2);c.update(answerVariants=variants,questionFigureKey='home-economics-2021-ol-sb-q1a-yoghurt',questionFigureIncludesPrompt=False);added.append(c)
 points('q1b',12,3,[0,2,4],body(10,'3 causes @ 4 marks each (graded 4:2:0)','(c)'),label='causes')
 put('q1c',28,'Classification 2 × 4 (4:0); functions 2 × 4 (4:2:0); sources 4 × 3 (3:2:0)',[
  criterion('classification','classes',2,[0,4],'Two classes, each graded 4:0. '+body(10,'2 classes @ 4 marks each (graded 4:0)','• functions')),
  criterion('functions','functions',2,[0,2,4],'Two functions, each graded 4:2:0. Source correction: lipids form cell membranes; human cells do not have cell walls. Complete historical wording: '+body(10,'2 functions @ 4 marks each (graded 4:2:0)','• dietary')),
  criterion('sources','dietary sources',4,[0,2,3],'Four sources, each graded 3:2:0. '+body(10,'4 sources @ 3 marks each (graded 3:2:0)','(d)'))])
 points('q1d',20,4,[0,3,5],body(10,'4 factors @ 5 marks each (graded 5:3:0)'),label='factors')
 pregnancy='Food-safety correction: avoid raw/undercooked eggs, unpasteurised dairy and pâté during pregnancy; do not merely reduce them. Historical examination guidance follows: '
 points('q2a',20,4,[0,3,5],pregnancy+body(11,'4 requirements @ 5 marks each (graded 5:3:0)','(b)'),label='requirements')
 samples=['Breakfast Orange juice *** Porridge *** Pancakes with blueberry sauce *** Tea/coffee/water','Lunch Vegetable soup with wholemeal bread *** Strawberry yoghurt *** Apple *** Glass of milk','Dinner Carrot and lentil soup with brown bread *** Chicken and broccoli bake with mashed potato *** Fresh fruit salad *** Glass of milk/water'];rows=[]
 for i,(name,x0,x1) in enumerate([('Breakfast',75,243),('Lunch',244,381),('Dinner',382,557)],1):
  sample=tidy(d['scheme'][10].get_text(clip=fitz.Rect(x0,323,x1,477)));assert sample==samples[i-1],(name,sample)
  row=criterion(f'meal-{i}',name,3,[0,1,2],'Supply two food courses and one beverage for this meal, each graded 2:1:0, appropriate to the pregnancy brief. The sample is guidance; no extra course or beverage earns a fourth slot. Current clarification: caffeine is limited to 200 mg per day. Complete published sample: '+sample.replace(' ***',';'))
  for part,label in zip(row['parts'],['First course','Second course','Beverage']):part['verbatim']=label
  rows.append(row)
 c=card('sb-q2b','B','Q2(b)','0-10','pregnancy-day-menu',between(p[3].split('Question 3',1)[0],'(b)','(18 marks)'),between(p[3],'Question 2','(a)'),18,'3 meals × (2 courses × 2 + beverage 2), all 2:1:0',rows,3);added.append(c)
 points('q2c',12,3,[0,2,4],body(11,'3 points @ 4 marks each (graded 4:2:0)'),label='points',questionText='Explain how food labelling assist consumers when buying food.')
 nutritive,dietetic=named_sections(body(12,'(2 references to nutritive value, 2 references to dietetic value, plus 1 other)','(b)'),['Nutritive:','Dietetic:'])
 c=card('sb-q3a','B','Q3(a)','0-9','vegetable-nutritive-dietetic-value',between(p[3].split('Question 3',1)[1],'(a)','(20 marks)'),between(p[3],'Question 3','(a)'),20,'5 points × 4 (4:2:0): 2 nutritive, 2 dietetic, 1 other',[
  criterion('nutritive','Nutritive',2,[0,2,4],'Two nutritive points, each graded 4:2:0. Complete guidance: '+nutritive),criterion('dietetic','Dietetic',2,[0,2,4],'Two dietetic points, each graded 4:2:0. Food properties vary; the printed stem’s local-origin claim is not a guarantee of greater nutrition. Complete guidance: '+dietetic),criterion('other','other',1,[0,2,4],'One further distinct point under either heading, graded 4:2:0. Use the full guidance above without counting a point twice.')],3);added.append(c)
 points('q3b',9,3,[0,2,3],body(12,'Effects of cooking:','3 guidelines @'),label='effects of cooking',questionText='Outline the effects of cooking on vegetables.',questionRef='2021 OL Section B Q3(b)(i)')
 c=deepcopy(old['he-2021-ol-sb-q3b']);c.update(id='he-2021-ol-sb-q3b-storage',conceptId='vegetable-storage',questionText='Outline the guidelines for storing vegetables.',questionRef='2021 OL Section B Q3(b)(ii)',totalMarks=9,tariffModel=dict(kind='fixed',notation='3 guidelines × 3 (3:2:0)'),rows=[criterion('storage','guidelines',3,[0,2,3],'Three guidelines, each graded 3:2:0. Complete guidance: '+body(12,'Guidelines for storing:','(c)'))],notes='Independent storage prompt and nine-mark tariff; cooking remains on the original Q3b ID.');added.append(c)
 points('q3c',12,2,[0,3,6],body(12,'2 ways @ 6 marks each (graded 6:3:0)'),label='ways')
 points('q4a',20,4,[0,3,5],body(13,'4 advantages @ 5 marks each (graded 5:3:0)','(b)'),label='advantages')
 points('q4b',20,5,[0,2,4],body(13,'5 points @ 4 marks each (graded 4:2:0)','(c)'),label='points',questionText='Set out a weekly budget plan for a family (two adults and two children) with a net income of €800 a week.')
 credit=named_sections(body(13,'1 advantage, 1 disadvantage'),['Advantage:','Disadvantage:'])
 put('q4c',10,'1 advantage + 1 disadvantage, each 5 (5:3:0)',[criterion(k,label,1,[0,3,5],'Required '+label.lower()+', graded 5:3:0. Complete historical examples: '+text) for k,label,text in zip(['advantage','disadvantage'],['Advantage','Disadvantage'],credit)])
 families=named_sections(body(14,'(18 marks)','(b)'),['One parent family:','Nuclear family:','Blended family:'])
 put('q5a',18,'3 required family structures × 2 points × 3 (3:2:0)',[criterion(k,label,2,[0,2,3],'Two points about this required family structure, each graded 3:2:0. These historical social/economic examples are possible circumstances, not defining traits or assumptions about a particular family. Complete published guidance: '+text) for k,label,text in zip(['one-parent','nuclear','blended'],['One parent family','Nuclear family','Blended family'],families)])
 points('q5b',20,4,[0,3,5],body(14,'Roles and responsibilities:','(c)'),label='roles and responsibilities')
 points('q5c',12,3,[0,2,4],body(14,'3 points @ 4 marks each (graded 4:2:0)'),label='points')
 assert len(fixes)==13 and len(added)==4 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==280
 return fixes,added


def write():
 fixes,added=build();save_batch('B',fixes,added,dict(tasks=17,marks=280,sourceClarifications=CLARIFICATIONS,selectionDecisions='Recover yoghurt choice, whole-day menu and vegetable-value tasks. Cooking and storage are independently practised at their separate nine-mark boundaries. The yoghurt choice has one tariff and three routes, never one card per option. Required headings and the three-meal menu remain whole tasks.',checked='2026-11-01'));print('2021 Ordinary B: 17 reviewed tasks, 280 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
