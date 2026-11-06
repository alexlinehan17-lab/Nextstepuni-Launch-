#!/usr/bin/env python3
"""2026 Higher B: every original prompt, complete source tables and partial ladders."""
from copy import deepcopy
import json,re,sys
from he_review_2026_hl_main import ROOT,documents,page_text,card,save_batch,criterion,between,named_sections,after,any_points,tidy

def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(10,17)};cards=[]
 def add(n,part,topic,concept,marks,notation,rows,suffix='',**extra):
  printed=14 if n==5 and part=='c' else marks;prompt=between(q[n],f'({part})',f'({printed} marks)').replace(' • ','\n• ');assert not re.search(r'\([a-e]\)',prompt)
  c=card(f'sb-q{n}{part}{suffix}','B',f'Q{n}({part})'+(' — '+suffix[1:] if suffix else ''),topic,concept,prompt,q[n].split('(a)',1)[0].strip() if n!=1 or part=='a' else '',marks,notation,rows,2 if n==1 else (3 if n<4 else 4));c.update(extra);cards.append(c);return c
 def body(n,token,end=None):return after(s[n],token,end)
 def points(n,part,topic,concept,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return add(n,part,topic,concept,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete source guidance: '+text)],**extra)
 points(1,'a','0-1','protein-snack-comparison',20,4,[0,1,2,3,4,5],body(10,'Evaluation point may refer to:','(b)'),questionFigureKey='home-economics-2026-hl-sb-q1a-protein-snacks',questionFigureIncludesPrompt=False)
 ess,non=named_sections(body(10,'(8 marks)'),['Essential amino acids','Non-essential amino acid']);rows=[];groups=[]
 for i,(label,value) in enumerate(zip(['Essential amino acids','Non-essential amino acid'],[ess,non]),1):
  definition=after(value,'(graded 2:1:0)','Example');examples=after(value,'(graded 2:0)');short=definition.split(';',1)[0]
  note='One definition, graded 2:1:0. '+('Source correction: nine amino acids are essential for humans; the printed eight-adult/ten-child count is historical. ' if i==1 else '')+'Complete historical wording: '+definition
  rows += [criterion(f'definition-{i}',short,1,[0,1,2],note),any_points(f'example-{i}','Example',1,2,examples,'Give an example of the SAME category, graded 2:0. '+('Histidine is essential for adults too; arginine is conditionally essential. ' if i==1 else ''))];groups.append(dict(sourceCardId=f'he-2026-hl-sb-q1b-category-{i}',label=label,marks=4,rowIds=[f'definition-{i}',f'example-{i}']))
 add(1,'b','0-5','essential-nonessential-amino-acids',8,'2 required categories × (definition 2 (2:1:0) + example 2 (2:0))',rows,taskGroups=groups)
 text=body(11,'7 points @ 2 marks (graded 2:0)','(d)').split('Accept labelled flow chart/diagram.',1)[0].strip()
 add(1,'c','0-5','protein-deamination',14,'7 points × 2 (2:0)',[any_points('deamination','deamination',7,2,text,'A labelled flow chart/diagram is accepted. ')])
 names=['Heat','Mechanical action','Enzymes'];values=named_sections(body(11,'(18 marks)','(e)'),names)
 add(1,'d','0-5','protein-denaturation',18,'3 required mechanisms × 3 points × 2 (2:1:0)',[criterion(str(i),label,3,[0,1,2],'Three points about this required mechanism, each graded 2:1:0. Culinary/practical application is accepted. Complete historical guidance: '+after(value,'(graded 2:1:0)')) for i,(label,value) in enumerate(zip(names,values),1)])
 safety,value=named_sections(body(11,'1 point on safety, 1 point on value for money & 2 other points'),['Safety:','Value for money:'])
 add(1,'e','0-10','protein-food-safety-value',20,'Safety 1 + value 1 + other 2, each 5 (5:4:3:0)',[criterion('safety','Safety',1,[0,3,4,5],'One safety point, graded 5:4:3:0. Complete historical guidance: '+safety),criterion('value','Value for money',1,[0,3,4,5],'One value-for-money point, graded 5:4:3:0. Complete guidance: '+value),criterion('other','other points',2,[0,3,4,5],'Two further distinct points from either heading, each graded 5:4:3:0.')])
 points(2,'a','0-9','vegetables-nutritional-significance',20,5,[0,1,2,3,4],'Composition varies by vegetable; historical health effects are not guaranteed outcomes for an individual. '+body(12,'5 points @ 4 marks (graded 4:3:2:1:0)','(b)'))
 prep,cooking=named_sections(body(12,'1 point on preparation, 1 point on cooking & 2 other points','(c)'),['Preparation:','Cooking:'])
 add(2,'b','0-3','vegetable-nutrient-retention',12,'Preparation 1 + cooking 1 + other 2, each 3 (3:2:1:0)',[criterion('preparation','Preparation',1,[0,1,2,3],'One preparation guideline, graded 3:2:1:0. Complete guidance: '+prep),criterion('cooking','Cooking',1,[0,1,2,3],'One cooking guideline, graded 3:2:1:0. Complete guidance: '+cooking),criterion('other','other points',2,[0,1,2,3],'Two further distinct guidelines from either heading, each graded 3:2:1:0.')])
 labels=['Enzymes','Moisture loss','Microbial contamination'];values=named_sections(body(12,'(18 marks)'),labels)
 add(2,'c','0-4','vegetable-spoilage-causes',18,'3 required causes × 2 points × 3 (3:2:0)',[criterion(str(i),label,2,[0,2,3],'Two points on this required cause, each graded 3:2:0. Complete guidance: '+after(value,'(graded 3:2:0)')) for i,(label,value) in enumerate(zip(labels,values),1)])
 labels=['Advantages','Disadvantages'];values=named_sections(body(13,'(16 marks)','(b)'),labels)
 add(3,'a','0-11','processed-food-advantages-disadvantages',16,'2 required headings × 2 points × 4 (4:2:0)',[criterion(str(i),label,2,[0,2,4],'Two points under this required heading, each graded 4:2:0. Effects depend on the specific food and diet. Complete guidance: '+after(value,'(graded 4:2:0)')) for i,(label,value) in enumerate(zip(labels,values),1)])
 table=d['scheme'][12].find_tables().tables[0].extract();assert table[0]==['Types / classes','Examples','Uses'];rows=[];groups=[]
 for i,cells in enumerate(table[1:],1):
  definition,examples,uses=map(tidy,cells);name='Intense sweeteners' if i==1 else 'Bulk sweeteners';assert definition.startswith(name)
  rows += [criterion(f'type-{i}',name,1,[0,2,3],'Describe this required class, graded 3:2:0. Complete historical guidance: '+definition[len(name):].strip()),dict(id=f'example-{i}',kind='alt',verbatim=examples,marks=3,openList=True,contextNote='One example from the SAME class, graded 3:0.'),dict(id=f'use-{i}',kind='alt',verbatim=uses,marks=3,openList=True,contextNote='One use of the SAME class, graded 3:0.')];groups.append(dict(sourceCardId=f'he-2026-hl-sb-q3b-class-{i}',label=name,marks=9,rowIds=[f'type-{i}',f'example-{i}',f'use-{i}']))
 add(3,'b','0-11','artificial-sweetener-classes',18,'2 classes × (description 3 (3:2:0) + example 3 (3:0) + use 3 (3:0))',rows,taskGroups=groups)
 labelling=body(13,'4 points @ 4 marks (graded 4:3:0)');assert labelling.endswith('ease of use; etc.')
 points(3,'c','0-11','processed-food-labelling',16,4,[0,3,4],labelling)
 points(4,'a','1-2','consumer-shopping-patterns',20,5,[0,2,4],'Recent refers to the 2026 examination context. '+body(14,'5 changes @ 4 marks (graded 4:2:0)','(b)'),label='changes')
 labels=['Income','Family stage','Personal values'];values=named_sections(body(14,'(graded 6:4:2:0) Income:','(c)'),['higher incomes','Family stage:','Personal values:']);values[0]='higher incomes'+values[0]
 add(4,'b','1-1','household-spending-influences',18,'3 required factors × 6 (6:4:2:0)',[criterion(str(i),label,1,[0,2,4,6],'One developed point about this required factor, graded 6:4:2:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 points(4,'c','1-1','household-budgeting-advantages',12,3,[0,2,4],body(14,'3 points @ 4 marks (graded 4:2:0)'))
 economic,social=named_sections(body(15,'2 Economic points, 2 Social points & 1 other point','(b)'),['Economic:','Social:'])
 add(5,'a','2-0','economic-social-family-change',20,'Economic 2 + social 2 + other 1, each 4 (4:2:0)',[criterion('economic','Economic',2,[0,2,4],'Two economic points, each graded 4:2:0. Complete guidance: '+economic),criterion('social','Social',2,[0,2,4],'Two social points, each graded 4:2:0. Complete guidance: '+social),criterion('other','other point',1,[0,2,4],'One further distinct point under either heading, graded 4:2:0.')])
 labels=['Role of parent','Role of children'];values=named_sections(body(15,'(16 marks)'),labels);assert 'role reversal as adult children become older' in values[1]
 add(5,'b','2-1','family-life-cycle-roles',16,'2 required roles × 2 points × 4 (4:2:0)',[criterion(str(i),label,2,[0,2,4],'Two discussed points under this required heading, each graded 4:2:0. Complete guidance, including the lower-page continuation: '+after(value,'(graded 4:2:0)')) for i,(label,value) in enumerate(zip(labels,values),1)])
 full=between(q[5],'(c)','(14 marks)');importance,procedure=full.split(' and outline the procedure involved.',1);assert not procedure
 add(5,'c','2-1','importance-making-will',6,'2 importance points × 3 (3:2:0)',[criterion('importance','importance',2,[0,2,3],'Two importance points, each graded 3:2:0. Historical examination context, not advice on making an individual will. Complete guidance: '+body(16,'2 points on importance @ 3 marks (graded 3:2:0)','4 points on procedure'))],questionText=importance+'.')
 add(5,'c','2-1','making-will-procedure',8,'4 procedure points × 2 (2:1:0)',[criterion('procedure','procedure',4,[0,1,2],'Four procedure points, each graded 2:1:0. Historical examination summary, not a current legal checklist. Complete source guidance: '+body(16,'4 points on procedure @ 2 marks (graded 2:1:0)'))],suffix='-procedure',questionText='Outline the procedure involved.',stem=importance+'.')
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280
 return cards

def write():
 cards=build();save_batch('B',cards,dict(tasks=18,marks=280,selectionDecisions='Will importance and procedure are independent 6/8-mark prompts. All other required headings, amino-acid example pairs and two sweetener classes stay whole. Nutrition comparisons keep the original table. Preserve every quota, exact partial ladder, and B3(c)/B5(b) lower-page continuation.',sourceClarifications={'essential-amino-acids':dict(source='https://www.canada.ca/en/health-canada/services/food-nutrition/legislation-guidelines/guidance-documents/supplemented-foods-regulations.html',note='Nine amino acids are essential for humans; the eight-adult count is historical.')},checked='2026-11-06'));print('2026 Higher B: 18 tasks, 280 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
