#!/usr/bin/env python3
"""2016 Higher B: original complete choices, linked profiles and published quotas."""
from copy import deepcopy
from he_review_2016_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(9,18)}
 q={1:select(p[6],'1. Current',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:
   # The original input table is shown as a complete figure on part(a),
   # never flattened into disconnected numbers in the shared text stem.
   stem=stem.split('18 - 64 years',1)[0].strip() if part=='a' else stem.split('The chart below',1)[0].strip()
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 # Preserve coordinate-read table cells; whole-page extraction interleaves columns.
 first=table_rows(d['scheme'][8].find_tables().tables[1],d['scheme'][8]);second=table_rows(d['scheme'][9].find_tables().tables[0],d['scheme'][9]);assert len(first)==3 and len(second)==4
 models='; '.join(' — '.join(r) for r in first+second)
 full=guide(9,'4 points @ 6 marks each','Bread and rolls')+' '+models
 c=judged(1,'a','0-6',4,6,'contribution',full,questionFigureKey='home-economics-2016-hl-sb-q1-fibre',questionFigureIncludesPrompt=False)
 c['rows'][0]['contextNote']='Choose FOUR foods and comment/elaborate with reference to BOTH age categories. The original six food groups and the complete models are retained; no four-food combination is imposed. '+c['rows'][0]['contextNote']
 judged(1,'b','0-6',3,4,'strategies',guide(10,'3 points @ 4 marks each'))
 judged(1,'c','0-6',3,5,'benefits',guide(11,'3 points @ 5 marks each','(d)'))
 grid=table_rows(d['scheme'][10].find_tables().tables[0],d['scheme'][10]);assert len(grid)==6;variants=[]
 for i,(name,account,symptoms) in enumerate(grid[1:],1):
  variants.append(dict(id=f'source-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),1,note='Use this SAME bowel disease throughout.'),criterion('account','Account',1,[0,4],account),criterion('symptoms','Symptoms / effects',2,[0,2],symptoms)]))
 for i,name in enumerate(['colitis','coeliac','Crohn’s disease','Another valid bowel disease'],1):
  note='The original scheme explicitly accepts colitis, coeliac and Crohn’s disease but supplies no accounts or symptom models for them. No additional model has been invented. Keep every detail about the SAME chosen disease.'
  rows=[criterion('name','Name',1,[0,1],note) if i==4 else point('name',name,1,note=note),criterion('account','Account',1,[0,4],note),criterion('symptoms','Symptoms / effects',2,[0,2],note)]
  variants.append(dict(id=f'additional-{i}',label=name,rows=rows))
 add(1,'d','0-1',9,deepcopy(variants[0]['rows']),'Name1 + account4 + symptoms/effects2×2',answerVariants=variants,figureKey='home-economics-2016-hl-sb-q1d-diseases')
 full=guide(12,'(1 reference to lifestyle, 1 references to dietary practices, plus 3 other points)');lifestyle,diet=named(full,['Lifestyle:','Dietary practices:'])
 add(1,'e','0-1',20,[criterion('lifestyle','lifestyle',1,[0,4],lifestyle),criterion('diet','dietary practices',1,[0,4],diet),criterion('other','3 other points',3,[0,4],'Three ADDITIONAL points from either heading. Historical 2016 wording is retained, including the source’s printed 12pm–6am period. Complete original source: '+full)],'Lifestyle4 + dietary practice4 + three others×4')
 full=guide(13,'(2 references to nutritive value, 2 references to contribution to the diet plus 1 other)','(b)');nutrition,diet=named(full,['Nutritive value:','Contribution to the Diet:'])
 add(2,'a','0-9',20,[criterion('nutrition','nutritive value',2,[0,4],nutrition),criterion('diet','contribution to the diet',2,[0,4],'Original wording, including “low in unsaturated fat”, retained as printed. '+diet),criterion('other','1 other',1,[0,4],'One ADDITIONAL point from either required heading. '+full)],'Nutrition2×4 + contribution2×4 + one other4')
 judged(2,'b','0-4',3,5,'causes',guide(13,'3 points @ 5 marks each','(c)'))
 full=guide(13,'Type / form:');types=select(full,'D3 – cholecalciferol,', 'Properties:',True);properties,deficiency=named(select(full,'Properties:',include=True),['Properties:','Effects of deficiency:']);variants=[]
 for i,(name,detail) in enumerate(zip(['D3 – cholecalciferol','D2 – ergocalciferol'],named(types,['D3 – cholecalciferol,','D2 – ergocalciferol,'])),1):
  variants.append(dict(id=f'type-{i}',label=name,rows=[point('name',name,1),criterion('detail','detail',1,[0,2],'Use the SAME named form of vitamin D. '+detail),criterion('properties','properties',3,[0,2],properties),criterion('deficiency','effects of deficiency',2,[0,3],deficiency)]))
 add(2,'c','0-8',15,deepcopy(variants[0]['rows']),'Type name1/detail2 + properties3×2 + deficiency2×3',answerVariants=variants)
 judged(3,'a','0-10',4,3,'benefits',guide(14,'4 points @ 3 marks each','(b)'))
 full=guide(14,'Description of method:');methods=select(full,'Home freezing:','Underlying principle:',True);principle=select(full,'Underlying principle:','Effect of the process:');effects=select(full,'Effect of the process:');names=['Home freezing:','Air Blast Freezing:','Plate or Contact Freezing:','Flow Freezing/Fluidised Bed Freezing:'];variants=[]
 for i,(name,detail) in enumerate(zip(names,named(methods,names)),1):
  variants.append(dict(id=f'method-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),2),criterion('description','Description',3,[0,3],'Three description points for the SAME selected freezing method. '+detail),criterion('principle','underlying principle',2,[0,3],'Two principles appropriate to the SAME selected method. Original shared source: '+principle),criterion('effect','effect of freezing',1,[0,3],'One effect appropriate to the SAME selected method. Complete original quick/slow/freezer-burn guidance: '+effects)]))
 variants.append(dict(id='another-method',label='Another valid freezing method',rows=[criterion('name','Name',1,[0,2],'Name ONE method consistently; four original models remain available.'),criterion('description','Description',3,[0,3],'Describe the SAME method. No additional model is printed.'),criterion('principle','underlying principle',2,[0,3],'Apply relevant principles to the SAME method. '+principle),criterion('effect','effect of freezing',1,[0,3],'Give an effect relevant to the SAME method. '+effects)]))
 add(3,'b','0-11',20,deepcopy(variants[0]['rows']),'Name2 + description3×3 + principle2×3 + effect3',answerVariants=variants)
 heads=['Suitability for purpose:','Environmental impact:','Source of consumer information:'];add(3,'c','0-11',18,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,3],body) for i,(head,body) in enumerate(zip(heads,named(guide(15,'Suitability for purpose:',include=True),heads)),1)],'Three required headings×two points×3')
 c=judged(4,'a','1-2',5,4,'shopping patterns',guide(16,'5 points @ 4 marks each','(b)'));c['rows'][0]['contextNote']='Cover BOTH changed shopping patterns and reasons within FIVE points. No separate quota is printed for either heading. Historical 2016 context retained. '+c['rows'][0]['contextNote']
 judged(4,'b','1-2',4,5,'merchandising techniques',guide(16,'4 points @ 5 marks each','(c)'))
 full=guide(16,'Name: 2 marks Details: 2 points @ 4 marks each');names=['Competition and Consumer protection Commission / National Consumer Agency (NCA):','Ombudsman:','Citizens’ Information Centres:','National Standards Authority of Ireland (NSAI):','Small Claims Procedure:'];variants=[]
 for i,(name,detail) in enumerate(zip(names,named(full,names)),1):
  note='Original historical 2016 names, classifications and conditions are retained. Give TWO details of the SAME selected body/procedure.'
  variants.append(dict(id=f'agency-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),2,note=note),criterion('details','Details',2,[0,4],note+' '+detail)]))
 variants.append(dict(id='another-agency',label='Another valid statutory agency',rows=[criterion('name','Name',1,[0,2],'Choose ONE statutory agency consistently. All five original historical source models remain available.'),criterion('details','Details',2,[0,4],'Give two details of that SAME agency. No additional source model is printed.')]))
 add(4,'c','1-2',10,deepcopy(variants[0]['rows']),'Name2 + details2×4',answerVariants=variants)
 full=guide(17,'(2 references to social, 2 references to economic plus 1 other)','(b)');social,economic=named(full,['Social:','Economic:']);add(5,'a','2-0',20,[criterion('social','social',2,[0,4],social),criterion('economic','economic',2,[0,4],economic),criterion('other','1 other',1,[0,4],'One ADDITIONAL point from either required heading. '+full)],'Social2×4 + economic2×4 + one other4')
 full=guide(17,'(2 references to physical, 2 references to psychological plus 2 others)','(c)');physical,psychological=named(full,['Physical:','Psychological:']);add(5,'b','2-0',18,[criterion('physical','physical',2,[0,3],physical),criterion('psychological','psychological',2,[0,3],psychological),criterion('other','2 others',2,[0,3],'Two ADDITIONAL points from either required heading. '+full)],'Physical2×3 + psychological2×3 + two others×3')
 judged(5,'c','2-0',3,4,'challenges',guide(17,'3 points @ 4 marks each'))
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=17,marks=280,selectionDecisions='Complete six-food fibre pool; five disease models and explicitly named model gaps; linked vitamin D forms, four freezing methods and all five historical consumer models. Required/flexible heading quotas retained without invented allocations.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
