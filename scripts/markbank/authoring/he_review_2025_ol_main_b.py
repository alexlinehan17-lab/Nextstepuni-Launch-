#!/usr/bin/env python3
"""2025 Ordinary B: original questions, all model choices and exact scoring."""
from copy import deepcopy
import json,re,sys
from he_review_2025_ol_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections,source_material

def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(10,16)};old=originals();fixes={};added=[]
 def put(n,part,marks,notation,rows,new=False,**extra):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' • ','\n• ');assert not re.search(r'\([a-e]\)',prompt)
  cid=f'he-2025-ol-sb-q{n}{part}';value=dict(questionText=prompt,questionRef=f'2025 OL Section B Q{n}({part})',stem=q[n].split('(a)',1)[0].strip(),totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,sourceMaterial=source_material(2 if n==1 else (3 if n<4 else 4)),notes='Independent paper/scheme review: he_review_2025_ol_main_b.py.');value.update(extra)
  if new:
   c=deepcopy(old['he-2025-ol-sb-q2c']);c.update(value,id=cid,conceptId={"1a":"convenience-soup-comparison","2a":"egg-nutritive-dietetic-value","2b":"healthy-day-menu-eggs"}[str(n)+part]);added.append(c)
  else:fixes[cid]=dict(reason='2025 Ordinary B full source review: complete prompts, exact partial credit and all published guidance.',set=value)
 def body(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def points(n,part,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));put(n,part,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete source guidance: '+text)],**extra)
 soup=named_sections(body(10,'Reasons: 4 @ 5 marks (graded 5:3:2:0)'),['Soup A:','Soup B:']);variants=[]
 for name,value in zip(['Soup A','Soup B'],soup):
  variants.append(dict(id=name[-1].lower(),label=name,rows=[criterion('name',name,1,[0,4],'Recommend this soup, graded 4:0.'),criterion('reasons','Reasons',4,[0,2,3,5],'Four distinct reasons for the SAME selected soup, each graded 5:3:2:0. Use the original table. Source correction: A has LESS carbohydrate (4.3 g versus 5.6 g), contrary to the scheme’s “higher in carbohydrates” wording. Printed health claims are not guarantees that a soup prevents or treats a condition. Complete historical model: '+value)]))
 put(1,'a',24,'Name 4 (4:0) + 4 reasons × 5 (5:3:2:0)',deepcopy(variants[0]['rows']),new=True,answerVariants=variants,topicId='home-economics-0-1',questionFigureKey='home-economics-2025-ol-sb-q1a-soups',questionFigureIncludesPrompt=False,figureKey='')
 put(1,'b',24,'Sources 3 × 4; functions 2 × 4; deficiency 1 × 4 (4:2:0)',[criterion('sources','dietary sources',3,[0,2,4],'Three sources, each graded 4:2:0. Complete guidance: '+body(11,'3 sources @ 4 marks (graded 4:2:0)','• functions')),criterion('functions','functions in the body',2,[0,2,4],'Two functions, each graded 4:2:0. Complete guidance: '+body(11,'2 functions @ 4 marks (graded 4:2:0)','• effect')),criterion('deficiency','effect of deficiency',1,[0,2,4],'One deficiency effect, graded 4:2:0. Complete guidance: '+body(11,'1 deficiency @ 4 marks (graded 4:2:0)','(c)'))],stem='')
 points(1,'c',12,3,[0,2,4],body(11,'3 ways @ 4 marks (graded 4:2:0)','(d)'),label='ways',stem='')
 points(1,'d',20,4,[0,3,5],body(11,'4 factors @ 5 marks (graded 5:3:0)'),label='factors',stem='')
 nutrition,diet=named_sections(body(12,'(1 reference to nutritive value, 1 reference to dietetic value, + 2 others points)','(b)'),['Nutritive:','Dietetic:'])
 put(2,'a',20,'Nutritive 1 + dietetic 1 + other 2, each 5 (5:4:3:2:0)',[criterion('nutritive','nutritive value',1,[0,2,3,4,5],'One nutritive point, graded 5:4:3:2:0. Complete guidance: '+nutrition),criterion('dietetic','dietetic value',1,[0,2,3,4,5],'One dietetic point, graded 5:4:3:2:0. Suitability depends on the individual and preparation. Complete guidance: '+diet),criterion('other','others points',2,[0,2,3,4,5],'Two further distinct points from either heading, each graded 5:4:3:2:0.')],new=True,topicId='home-economics-0-9')
 labels=['Breakfast','Lunch','Dinner'];samples=named_sections(body(12,'Sample menus','(c)'),labels);rows=[];groups=[]
 for i,(label,sample) in enumerate(zip(labels,samples),1):
  rows += [criterion(f'courses-{i}','courses',2,[0,1,2],f'{label}: two suitable food courses, each graded 2:1:0. Published sample: '+sample.replace(' ***',';')),criterion(f'beverage-{i}','beverage',1,[0,1],f'{label}: one suitable beverage, graded 1:0.')]
  groups.append(dict(sourceCardId=f'he-2025-ol-sb-q2b-meal-{i}',label=label,marks=5,rowIds=[f'courses-{i}',f'beverage-{i}']))
 rows.append(criterion('egg','egg component',1,[0,3],'Include eggs in one meal, graded 3:0. Use current healthy-eating guidelines in the paper’s 2025 context. The scheme’s “3 meals @ 6 marks” heading is resolved by its explicit detailed allocation: three 5-mark meals plus this 3-mark egg component, total 18; do not add 3 marks to an 18-mark meal total.'))
 groups.append(dict(sourceCardId='he-2025-ol-sb-q2b-eggs',label='Egg component',marks=3,rowIds=['egg']))
 put(2,'b',18,'3 × (courses 2 × 2 (2:1:0) + beverage 1 (1:0)) + eggs 3 (3:0)',rows,new=True,taskGroups=groups,topicId='home-economics-0-10')
 points(2,'c',12,3,[0,2,4],body(12,'3 effects @ 4 marks (graded 4:2:0)'),label='effects')
 points(3,'a',15,3,[0,3,5],body(13,'3 causes @ 5 marks (graded 5:3:0)','(b)'),label='causes')
 names=['jam/chutney making:','bottling/aseptic canning/in container canning:','drying:','freezing:','commercial freezing:','commercial drying:'];raw=body(13,'Method of preservation 4 points @ 5 marks (graded 5:3:0)','(c)');matches=list(re.finditer('|'.join(map(re.escape,names)),raw));assert [m.group() for m in matches]==names;values=[raw[m.end():matches[i+1].start() if i+1<len(matches) else len(raw)].strip() for i,m in enumerate(matches)];variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,3,5],'Name the chosen method, graded 5:3:0.'),criterion('method','Method of preservation',4,[0,3,5],'Four details of the SAME method, each graded 5:3:0. Historical process descriptions are not validated domestic preservation recipes. Complete model: '+value)]))
 names_guidance=body(13,'Name 1 point @ 5 marks (graded 5:3:0)','Method of preservation')
 variants.append(dict(id='another',label='Another valid method',rows=[criterion('name','Name',1,[0,3,5],'Name another valid method, graded 5:3:0. Complete printed acceptance: '+names_guidance),criterion('method','Method of preservation',4,[0,3,5],'Four accurate process details for that same method, each graded 5:3:0. No further developed model is printed; do not invent marking criteria.')]))
 put(3,'b',25,'Name 5 + method 4 × 5 (5:3:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(3,'c',10,2,[0,3,5],body(13,'2 advantages @ 5 marks (graded 5:3:0)'),label='advantages')
 points(4,'a',20,4,[0,3,5],body(14,'4 advantages @ 5 marks (graded 5:3:0)','(b)'),label='advantages')
 points(4,'b',20,5,[0,2,4],body(14,'5 points @ 4 marks (graded 4:2:0)','(c)'))
 points(4,'c',10,2,[0,3,5],body(14,'2 points @ 5 marks (graded 5:3:0)'))
 points(5,'a',20,4,[0,3,5],body(15,'4 ways @ 5 marks (graded 5:3:0)','(b)'),label='ways')
 points(5,'b',20,4,[0,3,5],'Explain both rights and responsibilities. Four points are priced; the scheme does not impose a two-plus-two quota. These are historical examination examples, not a current legal checklist. '+body(15,'4 points @ 5 marks (graded 5:3:0)','(c)'))
 points(5,'c',10,2,[0,3,5],body(15,'2 points @ 5 marks (graded 5:3:0)'))
 assert len(fixes)==13 and len(added)==3 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==280
 return fixes,added

def write():
 fixes,added=build();save_batch('B',fixes,added,dict(tasks=16,marks=280,selectionDecisions='Recover soup recommendation, egg nutritive/dietetic account and complete three-meal menu. Soup and preservation keep one open choice with model variants; required vitamin and nutrition headings remain whole. Menu follows the detailed printed tariff: 15 meal marks plus 3 egg-component marks. Rights/responsibilities has four flexible points, not an invented 2/2 quota.',sourceClarifications={'soup-carbohydrates':'The printed table gives A 4.3 g and B 5.6 g, contrary to the A-model claim of higher carbohydrate.'},checked='2026-11-06'));print('2025 Ordinary B: 16 tasks, 280 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
