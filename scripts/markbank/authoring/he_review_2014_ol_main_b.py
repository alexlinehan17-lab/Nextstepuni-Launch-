#!/usr/bin/env python3
"""2014 Ordinary B: source-only choices, coherent accounts and separate roman tariffs."""
from copy import deepcopy
from he_review_2014_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,15)}
 q={1:select(p[6],'1. The table',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,**extra):
  c=card(f'sb-q{n}{part}{roman or ""}','B',f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('(FSAI website)',1)[0]+'(FSAI website)'
  if roman:
   lead=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None).split('(i)',1)[0].strip();c['questionText']=(lead+' '+c['questionText']).strip()
  cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 meal=guide(8,'Name: 3 marks, 3 reasons @ 5 marks each','(b)');heads=['Beef Lasagne:','Sweet & Sour Chicken & Rice:','Cheese Burger:'];variants=[]
 for i,(head,body) in enumerate(zip(heads,named(meal,heads)),1):variants.append(dict(id=f'meal-{i}',label=head[:-1],rows=[point('name',head[:-1],3),criterion('reasons','reasons',3,[0,5],'Three reasons for the SAME chosen meal using the original data table. Original model: '+body)]))
 add(1,'a','0-1',18,deepcopy(variants[0]['rows']),'Name 3 + reasons 3×5',answerVariants=variants,questionFigureKey='home-economics-2014-ol-sb-q1-nutrients',questionFigureIncludesPrompt=False)
 classes=guide(8,'3 classes @ 3 marks each','• dietary sources');sources=guide(8,'3 sources @ 3 marks each','• functions');functions=guide(8,'2 functions @ 4 marks each');properties=guide(9,'2 properties @ 2 marks each','(c)')
 add(1,'b','0-6',30,[criterion('classes','classification',3,[0,3],'Three classes, using either original classification wording; not all six labels. Original source: '+classes),criterion('sources','dietary sources',3,[0,3],'Three sources from the complete original source guidance: '+sources),criterion('functions','functions in the body',2,[0,4],functions),criterion('properties','properties',2,[0,2],'The original carbohydrate-property pool includes “assists aeration/foaming (denatures egg protein)”; this source wording is retained without an invented replacement. Original source: '+properties)],'Classification 9 + sources 9 + functions 8 + properties 4')
 judged(1,'c','0-6',3,4,'ways',guide(9,'3 ways @ 4 marks each','(d)'))
 heads=['• cost','• skills','• time available for preparation','• storage space.'];add(1,'d','1-2',20,[criterion(f'heading-{i}',head.removeprefix('• ').rstrip('.'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(9,'4 points @ 5 marks each'),heads)),1)],'4 required headings × 5')
 milk=guide(10,'(1 reference to each + 2 others)','(b)');add(2,'a','0-9',20,[criterion('nutritive','nutritive value',1,[0,5],'One nutritive point. Original shared guidance: '+milk),criterion('dietetic','dietetic value',1,[0,5],'One dietetic point. Original shared guidance: '+milk),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points from either heading, with no extra per-heading quota. Original source: '+milk)],'Nutritive 5 + dietetic 5 + two others × 5')
 heads=['Whole milk:','Skimmed milk:','Fortified milk:'];add(2,'b','0-9',12,[criterion(f'type-{i}',head[:-1],1,[0,4],body) for i,(head,body) in enumerate(zip(heads,named(guide(10,'3 points @ 4 marks each','(c)'),heads)),1)],'3 required types × 4')
 heads=['Breakfast','Lunch','Dinner'];add(2,'c','0-10',18,[criterion(f'meal-{i}',head,1,[0,6],'One meal in the SAME balanced day for a teenage girl, with the original calcium requirement. Complete original example: '+body) for i,(head,body) in enumerate(zip(heads,named(guide(10,'3 meals @ 6 marks each'),heads)),1)],'3 meals × 6')
 grid=table_rows(d['scheme'][10].find_tables().tables[0],d['scheme'][10]);options=[r[0] for r in grid[1:]];full='; '.join(a+' — '+b for a,b in grid[1:]);rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'class-{i}','Class',1,4,options,'Choose TWO different classes in total.'),criterion(f'example-{i}','Example',1,[0,3],'One example of the SAME chosen class. Original matching source: '+full)]);groups.append(dict(sourceCardId=f'he-2014-ol-sb-q3a-class-{i}',label=f'Class {i}',marks=7,rowIds=[f'class-{i}',f'example-{i}']))
 add(3,'a','0-3',14,rows,'2 pairs × (class 4 + example 3)',taskGroups=groups)
 types=guide(11,'3 types @ 4 marks each','(ii)');options=[v.strip().removesuffix(' etc.').strip() for v in types.split(',') if v.strip()!='etc.'];add(3,'b','0-3',12,[menu('types','types',3,4,options)],'3 types × 4',roman='i')
 evaluation=select(select(s[11],'(ii)','(c)'),'3 points @ 4 marks each');adv,dis=named(evaluation,['Advantages:','Disadvantages:']);add(3,'b','0-3',12,[criterion('advantage','Advantages',1,[0,4],adv),criterion('disadvantage','Disadvantages',1,[0,4],dis),criterion('other','points',1,[0,4],'One ADDITIONAL point from either side. Both sides required within THREE total points; no two-per-side quota. Complete source: '+evaluation)],'Advantage 4 + disadvantage 4 + one other 4',roman='ii')
 judged(3,'c','1-2',3,4,'food labelling',select(select(s[11],'(c)'),'3 points @ 4 marks each'))
 heads=['• cost','• size and type of house / apartment','• location / environment','• trends in housing developments.'];add(4,'a','3-3',20,[criterion(f'heading-{i}',head.removeprefix('• ').rstrip('.'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(12,'4 points @ 5 marks each','(b)'),heads)),1)],'4 required headings × 5')
 types=guide(12,'2 types of pollution @ 5 marks each','(ii)');options=[v.strip().removesuffix(' etc.').strip() for v in types.split(',') if v.strip()!='etc.'];add(4,'b','1-5',10,[menu('types','types of pollution',2,5,options,'Choose TWO different types.')],'2 names × 5',roman='i')
 effects=guide(12,'2 effects @ 5 marks each');c=add(4,'b','1-5',10,[criterion(f'effect-{i}','effect',1,[0,5],f'ONE effect for chosen type {i}; use two DIFFERENT pollution types from the preceding original naming task. Each effect must match its own type. Naming is already priced in part(i), with no second name charge here. Complete original source: '+effects) for i in [1,2]],'1 effect for each of 2 chosen types × 5',roman='ii');c['stem']+='\n\n'+prompt(4,'b','i')
 green=guide(13,'Name: 5 marks, Details: 5 marks');options=chosen(green,['Reduce, Reuse, Recycle','Green Dot','WEEE','Blue Flower Symbol','Plastic Bag Levy','Green Flags','Blue Flags','Tidy Towns']);add(4,'c','1-5',10,[menu('name','Name',1,5,options),criterion('details','Details',1,[0,5],'One detail for the SAME chosen initiative. Complete original historical source: '+green)],'Name 5 + detail 5')
 judged(5,'a','2-1',3,6,'ways',guide(14,'3 ways @ 6 marks each','(b)'))
 c=judged(5,'b','2-1',4,5,'conditions',guide(14,'4 conditions @ 5 marks each','(c)'));c['rows'][0]['contextNote']='Original historical 2014 marriage-condition guidance is retained for this examination task. '+c['rows'][0]['contextNote']
 heads=['• the school','• marriage preparation courses.'];add(5,'c','2-1',12,[criterion(f'role-{i}',head.removeprefix('• ').rstrip('.'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(guide(14,'2 points @ 6 marks each'),heads)),1)],'2 required roles × 6')
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=18,marks=280,selectionDecisions='All three meal variants, coherent carbohydrate30 and milk20 accounts, complete calcium menu and two soup pairs retained. Independent soup12/12 and pollution10/10 roman tasks, with original naming context for matching pollution effects. Required/flexible quotas and all original source choices preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
