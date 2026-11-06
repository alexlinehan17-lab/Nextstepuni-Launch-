#!/usr/bin/env python3
"""2026 Ordinary Section B: full original prompts, quotas and menu tariff."""
from copy import deepcopy
import json,re,sys
from he_review_2026_ol_main import ROOT,documents,page_text,card,save_batch,criterion,between,named_sections,after,tidy

def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(9,15)};cards=[]
 def add(n,part,topic,concept,marks,notation,rows,**extra):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' • ','\n• ');assert not re.search(r'\([a-e]\)',prompt)
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,concept,prompt,q[n].split('(a)',1)[0].strip() if n!=1 or part=='a' else '',marks,notation,rows,2 if n==1 else (3 if n<4 else 4));c.update(extra);cards.append(c);return c
 def body(n,token,end=None):return after(s[n],token,end)
 def points(n,part,topic,concept,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return add(n,part,topic,concept,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 points(1,'a','0-1','vegetarian-lasagne-nutrition',20,4,[0,2,3,4,5],'Evaluate using the complete original table. The source prints iron as 1.0 g per 100 g; this is a source unit anomaly, preserved without inventing a corrected numeric value. Source health statements do not guarantee suitability or prevention of a condition. '+body(9,'4 @ 5 marks (graded 5:4:3:2:0)','(b)'),questionFigureKey='home-economics-2026-ol-sb-q1a-lasagne',questionFigureIncludesPrompt=False)
 accompaniment=body(9,'1 @ 4 marks (graded 4:2:0)','Give one reason');reason=s[9].rsplit('1 @ 4 marks (graded 4:2:0)',1)[1].strip()
 add(1,'b','0-10','lasagne-accompaniment-reason',8,'Accompaniment 4 + reason 4 (4:2:0)',[criterion('accompaniment',accompaniment,1,[0,2,4],'Recommend one suitable accompaniment from these published examples or another valid choice, graded 4:2:0.'),criterion('reason','reason',1,[0,2,4],'Give a reason for the SAME accompaniment, graded 4:2:0. Complete source examples: '+reason)])
 add(1,'c','0-8','iron-sources-functions-deficiency',24,'Sources 3 × 4 + functions 2 × 4 + deficiency 4 (4:2:0)',[criterion('sources','dietary sources',3,[0,2,4],'Three sources, each graded 4:2:0. Complete guidance: '+body(10,'3 sources @ 4 marks (graded 4:2:0)','• functions')),criterion('functions','functions in the body',2,[0,2,4],'Two functions, each graded 4:2:0. Complete guidance: '+body(10,'2 functions @ 4 marks (graded 4:2:0)','• effect')),criterion('deficiency','effect of deficiency',1,[0,2,4],'One effect, graded 4:2:0. Complete guidance: '+body(10,'1 deficiency @ 4 marks (graded 4:2:0)','(d)'))])
 points(1,'d','0-8','iron-absorption-factors',8,2,[0,2,4],body(10,'2 factors @ 4 marks (graded 4:2:0)','(e)'),label='factors')
 points(1,'e','0-11','food-label-consumer-benefits',20,4,[0,3,4,5],body(10,'4 @ 5 marks (graded 5:4:3:0)'),label='ways')
 nutrition,diet=named_sections(body(11,'(1 reference to nutritive value, 1 reference to dietetic value, plus 2 others)','(b)'),['Nutritive value:','Dietetic value:'])
 add(2,'a','0-9','cheese-nutritive-dietetic-value',20,'Nutritive 1 + dietetic 1 + other 2, each 5 (5:4:3:2:0)',[criterion('nutritive','nutritive value',1,[0,2,3,4,5],'One nutritive point, graded 5:4:3:2:0. Complete guidance: '+nutrition),criterion('dietetic','dietetic value',1,[0,2,3,4,5],'One dietetic point, graded 5:4:3:2:0. Suitability depends on the specific cheese, person and preparation. Complete historical guidance: '+diet),criterion('other','others',2,[0,2,3,4,5],'Two further distinct points from either required heading, each graded 5:4:3:2:0.')])
 table=d['scheme'][10].find_tables().tables[0].extract();labels=['Breakfast','Lunch','Dinner'];cells=table[3][1:4];assert [c.split('\n')[0] for c in cells]==labels;samples=[tidy(c.split('\n',1)[1]).replace(' ***',';') for c in cells];rows=[];groups=[]
 for i,(label,sample) in enumerate(zip(labels,samples),1):
  rows += [criterion(f'courses-{i}','courses',2,[0,1,2],f'{label}: two suitable courses, each graded 2:1:0. Full printed sample: '+sample),criterion(f'beverage-{i}','beverage',1,[0,2],f'{label}: suitable beverage, graded 2:0.')];groups.append(dict(sourceCardId=f'he-2026-ol-sb-q2b-meal-{i}',label=label,marks=6,rowIds=[f'courses-{i}',f'beverage-{i}']))
 add(2,'b','0-10','healthy-day-menu-cheese',18,'3 meals × (courses 2 × 2 (2:1:0) + beverage 2 (2:0))',rows,taskGroups=groups,notes='Paper requires cheese in the main meal. The published detailed tariff is 18 meal marks; no separately priced cheese component or invented deduction is added. Complete source sample menu retained.')
 points(2,'c','0-9','farmhouse-cheese-popularity',12,3,[0,2,4],body(11,'3 reasons @ 4 marks (graded 4:2:0)'),label='reasons')
 points(3,'a','0-1','food-pyramid-meal-planning',20,4,[0,3,5],body(12,'4 points @ 5 marks (graded 5:3:0)','(b)'),questionFigureKey='home-economics-2026-ol-sb-q3a-food-pyramid',questionFigureIncludesPrompt=False)
 points(3,'b','0-10','healthy-lifestyle-guidelines',15,3,[0,3,5],body(12,'3 @ 5 marks (graded 5:3:0)','(c)'),label='guidelines')
 points(3,'c','0-1','adult-energy-requirement-factors',15,3,[0,3,5],s[12].rsplit('3 @ 5 marks (graded 5:3:0)',1)[1].strip(),label='factors')
 add(4,'a','1-3','microwave-oven-study',20,'Modern features 2 × 3 (3:2:0) + use 2 × 4 (4:2:0) + care 2 × 3 (3:2:0)',[criterion('features','modern features',2,[0,2,3],'Two features, each graded 3:2:0. Complete source guidance: '+body(13,'2 modern features @ 3 marks (graded 3:2:0)','• guidelines')),criterion('use','guidelines for use',2,[0,2,4],'Two guidelines, each graded 4:2:0. Complete source guidance: '+body(13,'2 guidelines @ 4 marks (graded 4:2:0)','• care')),criterion('care','care and cleaning',2,[0,2,3],'Two points, each graded 3:2:0. Complete source guidance: '+body(13,'2 points @ 3 marks (graded3:2:0)','(b)'))],questionFigureKey='home-economics-2026-ol-sb-q4a-microwave',questionFigureIncludesPrompt=False)
 points(4,'b','1-2','faulty-microwave-complaint',20,4,[0,3,5],'Answer the historical examination task; this is not a current individual consumer-rights checklist. '+body(13,'4 points @ 5 marks (graded 5:3:0)','(c)'))
 points(4,'c','1-5','electrical-appliance-disposal',10,2,[0,3,5],body(13,'2 @ 5 marks (graded 5:3:0)'))
 points(5,'a','2-0','older-person-independence',15,3,[0,3,5],'Benefit eligibility and rates below belong to the historical source. '+body(14,'3 points @ 5 marks (graded 5:3:0)','(b)'))
 points(5,'b','2-1','older-person-family-roles',20,4,[0,3,5],body(14,'4 points @ 5 marks (graded 5:3:0)','(c)'))
 points(5,'c','2-1','family-communication',15,3,[0,3,5],s[14].rsplit('3 points @ 5 marks (graded 5:3:0)',1)[1].strip())
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280
 return cards

def write():
 cards=build();save_batch('B',cards,dict(tasks=17,marks=280,selectionDecisions='All seventeen separately priced parts. Lasagne accompaniment/reason, iron headings, cheese quota and microwave study remain whole. Menu follows its exact eighteen-mark tariff: three meals, two two-mark courses and a binary two-mark beverage per meal. No extra cheese-component tariff is printed. Full original table and images retained.',sourceClarifications={'iron-unit':'The table in both paper and scheme prints 1.0 g iron per 100 g; retained as a source unit anomaly, without inventing a corrected value.'},checked='2026-11-06'));print('2026 Ordinary B: 17 tasks, 280 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
