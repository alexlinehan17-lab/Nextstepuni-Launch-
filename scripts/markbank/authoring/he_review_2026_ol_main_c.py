#!/usr/bin/env python3
"""2026 Ordinary C: complete figure context, profiles and asymmetric allocations."""
from copy import deepcopy
import json,re,sys
from he_review_2026_ol_main import ROOT,documents,page_text,card,save_batch,criterion,between,named_sections,after,tidy

def build():
 d=documents();s={n:re.sub(r'@\s*','@ ',page_text(d['scheme'],n)) for n in range(15,23)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};cards=[]
 def group(n,part):
  token=next(t for t in [f'{n}.({part})',f'{n}. ({part})'] if t in p[n]);text=p[n].split(token,1)[1]
  if part!='c':text=re.split(rf'{n}\.\s*\({chr(ord(part)+1)}\)',text,1)[0]
  return text
 def add(n,part,roman,topic,concept,marks,notation,rows,**extra):
  text=group(n,part)
  if roman:prompt=between(text,f'({roman})',f'({marks} marks)');stem=text.split('(i)',1)[0].strip()
  else:stem,prompt=text.split('Name and describe',1);prompt='Name and describe'+prompt.split(f'({marks} marks)',1)[0];stem=stem.strip()
  c=card(f'sc-q{n}{part}{roman}','C',(f'E{n} ' if n<4 else '')+f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,concept,prompt.strip().replace(' • ','\n• '),stem,marks,notation,rows,n+4);c.update(extra);cards.append(c);return c
 def body(n,token,end=None):return after(s[n],token,end).removesuffix(' and').removesuffix(' or')
 def points(n,part,roman,topic,concept,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return add(n,part,roman,topic,concept,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 figure1=dict(questionFigureKey='home-economics-2026-ol-sc-q1-house-plan',questionFigureIncludesPrompt=False)
 points(1,'a','i','3-3','family-house-layout-evaluation',20,4,[0,3,5],body(15,'4 points @ 5 marks (graded 5:3:0)','(ii)'),**figure1)
 modifications=body(15,'2 modifications @ 5 marks (graded 5:3:0)','2 reasons');reasons=body(15,'2 reasons @ 5 marks (graded 5:3:0)','(iii)');rows=[];groups=[]
 for i in [1,2]:
  rows += [criterion(f'modification-{i}','modifications',1,[0,3,5],'One distinct proposed modification, graded 5:3:0. Complete source examples: '+modifications),criterion(f'reason-{i}','reasons',1,[0,3,5],'One reason for the SAME modification, graded 5:3:0. Complete source examples: '+reasons)];groups.append(dict(sourceCardId=f'he-2026-ol-sc-q1aii-pair-{i}',label=f'Modification and reason {i}',marks=10,rowIds=[f'modification-{i}',f'reason-{i}']))
 add(1,'a','ii','3-3','house-future-needs-modifications',20,'2 paired modifications × (modification 5 + reason 5), graded 5:3:0',rows,taskGroups=groups,**figure1)
 adv=body(15,'1 advantage @ 5 marks (graded 5:3:0)','1 disadvantage');dis=body(15,'1 disadvantage @ 5 marks (graded 5:3:0)')
 add(1,'a','iii','3-3','interior-designer-advantages-disadvantages',10,'Advantage 5 + disadvantage 5 (5:3:0)',[criterion('advantage','advantage',1,[0,3,5],'One advantage, graded 5:3:0. Complete guidance: '+adv),criterion('disadvantage','disadvantage',1,[0,3,5],'One disadvantage, graded 5:3:0. Complete guidance: '+dis)])
 points(1,'b','i','3-4','heating-system-selection',20,4,[0,3,5],body(16,'4 points @ 5 marks (graded 5:3:0)','(ii)'))
 points(1,'b','ii','3-4','heating-thermostats-timers',10,2,[0,3,5],'Explain the controls asked for in the paper. The scheme prices two points without a separate naming tariff. '+body(16,'2 points @ 5 marks (graded 5:3:0)','or 1.(c)'))
 points(1,'c','i','3-3','wall-finish-selection',15,3,[0,3,5],body(16,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 points(1,'c','ii','3-3','bathroom-wall-finishes',15,3,[0,3,5],s[16].rsplit('3 points @ 5 marks (graded 5:3:0)',1)[1].strip())
 labels=['comfort','function','design'];values=named_sections(body(17,'(18 marks)','(ii)'),[x+':' for x in labels])
 add(2,'a','i','3-8','healthcare-uniform-suitability',18,'3 required headings × 2 points × 3 (3:2:0)',[criterion(str(i),label,2,[0,2,3],'Two points under this required heading, each graded 3:2:0. Complete source guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)],questionFigureKey='home-economics-2026-ol-sc-q2-uniforms',questionFigureIncludesPrompt=False)
 crest=body(17,'1 point @ 4 marks (graded 4:2:0), 1 point @ 3 marks (graded 3:2:0)','and 2.(b)')
 add(2,'a','ii','3-7','hospital-crest-application',7,'1 point × 4 (4:2:0) + 1 point × 3 (3:2:0)',[criterion('first','point',1,[0,2,4],'First description point, graded 4:2:0. The scheme prints these method examples only, with no developed application steps: '+crest),criterion('second','point',1,[0,2,3],'Second distinct description point for the SAME application, graded 3:2:0. No invented model procedure or additional criterion.')],questionFigureKey='home-economics-2026-ol-sc-q2-uniforms',questionFigureIncludesPrompt=False)
 colour=body(17,'Description: 3 points @ 3 marks (graded 3:2:0)')
 add(2,'b','','3-7','clothing-colour-application-methods',15,'2 names × 3 + 3 description points × 3 (3:2:0)',[criterion('names',colour,2,[0,2,3],'Name TWO different methods from the actual published alternatives shown here or other valid methods. Each name graded 3:2:0.'),criterion('description','Description',3,[0,2,3],'Three total description points across the SAME two chosen methods, each graded 3:2:0. The scheme does not allocate three description points per method. Full published guidance is in the methods row; no further process model is supplied.')])
 points(2,'c','i','3-8','social-media-fashion-trends',9,3,[0,2,3],body(18,'3 points @ 3 marks (graded 3:2:0)','(ii)'))
 points(2,'c','ii','3-8','preloved-vintage-clothing',6,2,[0,2,3],body(18,'2 points @ 3 marks (graded 3:2:0)'))
 figure3=dict(questionFigureKey='home-economics-2026-ol-sc-q3-workers',questionFigureIncludesPrompt=False)
 points(3,'a','i','3-10','education-work-preparation',20,4,[0,3,5],body(19,'4 ways @ 5 marks (graded 5:3:0)','(ii)'),label='ways',**figure3)
 points(3,'a','ii','3-9','women-workforce-participation',15,3,[0,3,5],body(19,'3 reasons @ 5 marks (graded 5:3:0)','(iii)'),label='reasons',**figure3)
 names=['Protection of Young Persons (Employment) Act, 1996:','Safety, Health and Welfare at Work Act 2005:','Employment Equality Acts:','Organisation of Working Time Act 1997:','Employee Rights and Entitlements:'];values=named_sections(body(19,'description 2 points @ 5 marks (graded 5:3:0)','and 3.(b)'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,3,5],'Name the selected legislation, graded 5:3:0. The final source heading is a general rights/entitlements category; identify an appropriate actual law when using that route.'),criterion('description','description',2,[0,3,5],'Two points about the SAME law, each graded 5:3:0. Historical source examples, not current individual legal advice: '+value)]))
 variants.append(dict(id='another',label='Another valid employment law',rows=[criterion('name','name',1,[0,3,5],'Name another valid law protecting workers, graded 5:3:0.'),criterion('description','description',2,[0,3,5],'Two accurate points about the SAME law, each graded 5:3:0. No additional model is printed.')]))
 add(3,'a','iii','3-9','worker-protection-legislation',15,'Name 5 + description 2 × 5 (5:3:0)',deepcopy(variants[0]['rows']),answerVariants=variants,**figure3)
 points(3,'b','i','3-11','leisure-participation-benefits',15,3,[0,3,5],body(19,'3 benefits @ 5 marks (graded 5:3:0)'),label='benefits')
 points(3,'b','ii','3-11','family-leisure-choice-factors',15,3,[0,3,5],body(20,'3 factors @ 5 marks (graded 5:3:0)','or 3.(c)'),label='factors')
 labels=['changing attitudes to marriage','reduction in working hours','changing attitudes to parenting'];values=named_sections(body(20,'(15 marks)','(ii)'),[x+':' for x in labels])
 add(3,'c','i','2-0','social-change-family-life',15,'3 required headings × 5 (5:3:0)',[criterion(str(i),label,1,[0,3,5],'One developed point under this required heading, graded 5:3:0. Complete historical guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 points(3,'c','ii','3-3','urban-living-reasons',15,3,[0,3,5],body(20,'3 reasons @ 5 marks (graded 5:3:0)'),label='reasons')
 figure4=dict(questionFigureKey='home-economics-2026-ol-sc-q4-pregnancy',questionFigureIncludesPrompt=False)
 points(4,'a','i','0-10','pregnancy-dietary-requirements',20,4,[0,3,5],body(21,'4 points @ 5 marks (graded 5:3:0)','(ii)'),**figure4)
 table=d['scheme'][20].find_tables().tables[0].extract();assert [c.split('\n')[0] for c in table[0]]==['Breakfast','Lunch','Dinner'];rows=[];groups=[]
 for i,label in enumerate(['Breakfast','Lunch','Dinner'],1):
  sample=tidy(table[0][i-1].split('\n',1)[1]).replace(' ***',';')
  if i<3:
   rows += [criterion(f'courses-{i}','courses',2,[0,1,2],f'{label}: two suitable courses, each graded 2:1:0. Complete published sample: '+sample),criterion(f'beverage-{i}','beverage',1,[0,2],f'{label}: suitable beverage, graded 2:0.')];ids=[f'courses-{i}',f'beverage-{i}'];marks=6
  else:
   rows += [criterion('starter','starter/dessert',1,[0,1,2],'Dinner: starter or dessert, graded 2:1:0. Complete published sample: '+sample),criterion('main','main course',1,[0,2,4],'Dinner: main course, graded 4:2:0.'),criterion('beverage-3','beverage',1,[0,2],'Dinner: suitable beverage, graded 2:0.')];ids=['starter','main','beverage-3'];marks=8
  groups.append(dict(sourceCardId=f'he-2026-ol-sc-q4aii-meal-{i}',label=label,marks=marks,rowIds=ids))
 add(4,'a','ii','0-10','pregnancy-day-menu',20,'Breakfast 6 + lunch 6 + dinner 8: exact course/beverage tariffs',rows,taskGroups=groups,**figure4)
 points(4,'a','iii','0-8','pregnancy-water-intake',10,2,[0,3,5],body(21,'2 points @ 5 marks (graded 5:3:0)','and 4.(b)'),**figure4)
 adv,dis=named_sections(body(21,'one advantage & one disadvantage and two others'),['Advantages:','Disadvantages:'])
 add(4,'b','i','1-2','online-purchase-advantages-disadvantages',20,'Advantage 1 + disadvantage 1 + other 2, each 5 (5:3:0)',[criterion('advantage','advantage',1,[0,3,5],'One advantage, graded 5:3:0. Complete guidance: '+adv),criterion('disadvantage','disadvantage',1,[0,3,5],'One disadvantage, graded 5:3:0. Complete guidance: '+dis),criterion('other','others',2,[0,3,5],'Two further distinct points from either heading, each graded 5:3:0.')])
 points(4,'b','ii','1-1','consumer-credit-act-protection',10,2,[0,3,5],'Answer the historical Act named by the paper; not current individual credit advice. '+body(22,'2 points @ 5 marks (graded 5:3:0)','or 4.(c)'))
 labels=['income','location','trends in housing development'];values=named_sections(body(22,'(15 marks)','(ii)'),[x+':' for x in labels])
 add(4,'c','i','3-3','home-choice-influences',15,'3 required factors × 5 (5:3:0)',[criterion(str(i),label,1,[0,3,5],'One explained point about this required factor, graded 5:3:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 points(4,'c','ii','1-1','home-insurance-benefits',15,3,[0,3,5],body(22,'3 points @ 5 marks (graded 5:3:0)'),label='benefits')
 assert len(cards)==26 and sum(c['totalMarks'] for c in cards)==385
 return cards

def write():
 cards=build();save_batch('C',cards,dict(tasks=26,marks=385,selectionDecisions='All required headings and dependent modification/reason or legislation profiles remain whole. Colour application uses two names plus THREE total description points, not three per method. Crest application has an asymmetric 4/3 tariff and only the source’s method names, without invented process instructions. Pregnancy menu preserves 6/6/8 meal allocation with all original samples. Complete original floor plan and uniforms retained.',checked='2026-11-06'));print('2026 Ordinary C: 26 tasks, 385 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
