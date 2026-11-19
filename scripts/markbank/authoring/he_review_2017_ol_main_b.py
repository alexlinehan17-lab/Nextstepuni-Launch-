#!/usr/bin/env python3
"""2017 Ordinary B: original quotas, paired contexts and explicit roman tariffs."""
from he_review_2017_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,14)}
 q={1:select(p[6],'1.'),2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})','(ii)' if roman=='i' else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,part,topic,marks,rows,notation,roman=None,**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('Number of people',1)[0].strip()
  if n==2:stem=stem.split('Breakfast',1)[0].strip()
  c=card(f'sb-q{n}{part}{roman or ""}','B',f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,prompt(n,part,roman),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 full=guide(8,'(1 reference to each age group)','(ii)')
 rows=[criterion('comment','Comment',1,[0,3],'Comment on the original chart. Source gives one whole three-mark comment; no smaller split is printed. '+full)]
 rows += [criterion(f'reason-{i}','reasons',1,[0,4],f'Give ONE reason referring to the {age} age group. Keep all three required age references. Complete original reason pool: '+full) for i,age in enumerate(['15–34','35–54','55+'],1)]
 add(1,'a','0-1',15,rows,'Comment 3 + three age-specific reasons 4',roman='i',questionFigureKey='home-economics-2017-ol-sb-q1-chart',questionFigureIncludesPrompt=False)
 judged(1,'a','0-1',3,4,'ways',guide(8,'3 ways @ 4 marks each'),roman='ii',questionFigureKey='home-economics-2017-ol-sb-q1-chart',questionFigureIncludesPrompt=False)
 add(1,'b','0-8',28,[criterion('sources','dietary sources',4,[0,4],guide(9,'4 sources @ 4 marks each','• functions in the body')),criterion('functions','functions in the body',2,[0,4],guide(9,'2 functions @ 4 marks each','• effect of deficiency.')),criterion('deficiency','effect of deficiency',1,[0,4],guide(9,'1 effect @ 4 marks','(c)'))],'Sources 4×4 + functions 2×4 + deficiency 4')
 add(1,'c','0-8',5,[menu('nutrient','Name',1,5,semis(guide(9,'Name: 5 marks','(d)')),'Name ONE nutrient from the complete original 2017 scheme pool.')],'One nutrient 5')
 full=guide(9,'(1 reference to selecting, 1 reference to buying plus 2 other points)')
 add(1,'d','0-9',20,[criterion('selecting','selecting',1,[0,5],'One selecting factor. '+full),criterion('buying','buying',1,[0,5],'One buying factor. '+full),criterion('other','other points',2,[0,5],'Two ADDITIONAL factors from either heading; do not credit the same factor twice. '+full)],'Selecting 5 + buying 5 + two others 5')
 menu_figure=dict(questionFigureKey='home-economics-2017-ol-sb-q2-menu',questionFigureIncludesPrompt=False)
 judged(2,'a','0-1',2,4,'Comment',guide(10,'Comment: 2 points @ 4 marks each','(ii)'),roman='i',**menu_figure)
 judged(2,'a','0-1',3,4,'diet related problems',guide(10,'3 diet related problems @ 4 marks each','(b)'),roman='ii',**menu_figure)
 full=guide(10,'Morning break:','(c)',True);models=named(full,['Morning break:','Lunch:','Dinner:'])
 add(2,'b','0-10',15,[criterion(key,label,1,[0,marks],'One complete menu for this required meal. No internal allocation is printed. '+model) for key,label,marks,model in zip(['break','lunch','dinner'],['Morning break','Lunch','Dinner'],[3,6,6],models)],'Morning break 3 + lunch 6 + dinner 6',**menu_figure)
 judged(2,'c','0-10',3,5,'factors',guide(10,'3 factors @ 5 marks each'),**menu_figure)
 full=guide(11,'(1 reference to nutritive value, 1 reference to dietetic value, plus 2 others)','(b)');nutritive,dietetic=named(full,['Nutritive:','Dietetic:'])
 add(3,'a','0-9',20,[criterion('nutritive','nutritive value',1,[0,5],nutritive),criterion('dietetic','dietetic value',1,[0,5],dietetic),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points from either required heading. The original two roman asks share this four-point tariff; no separate 10/10 allocation is printed. '+full)],'Nutritive 5 + dietetic 5 + two others 5')
 judged(3,'b','0-9',2,4,'effects of cooking',guide(11,'2 effects of cooking @ 4 marks each','2 guidelines for storage'),roman='i')
 judged(3,'b','0-9',2,4,'guidelines for storage',guide(11,'2 guidelines for storage @ 4 marks each','(c)'),roman='ii')
 add(3,'c','0-9',14,[criterion('causes','causes',2,[0,4],guide(11,'2 causes @ 4 marks each','2 methods')),criterion('methods','methods',2,[0,3],guide(11,'2 methods @ 3 marks each'))],'Two causes 4 + two methods 3')
 judged(4,'a','1-3',4,5,'factors',guide(12,'4 factors @ 5 marks each.','(b)'))
 full=guide(12,'1 type @ 2 marks','• guidelines for use');add(4,'b','1-3',20,[menu('type','type of refrigeration appliance',1,2,semis(full),'Choose ONE appliance and keep the following study about that SAME appliance.'),criterion('use','guidelines for use',3,[0,4],'Three guidelines for the SAME selected appliance. '+guide(12,'3 guidelines @ 4 marks each','• modern features')),criterion('features','modern features',2,[0,3],'Two features of the SAME selected appliance. '+guide(12,'2 features @ 3 marks each','(c)'))],'Type 2 + three use guidelines 4 + two features 3')
 judged(4,'c','1-2',2,5,'sources',guide(12,'2 sources @ 5 marks each'))
 heads=['Nuclear family:','Extended family:','Blended family:'];full=guide(13,'Nuclear family:','(b)',True);add(5,'a','2-0',18,[criterion(f'family-{i}',head.rstrip(':'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)],'Three required family structures 6')
 judged(5,'b','2-0',3,5,'ways',guide(13,'3 ways @ 5 marks each','(c)'))
 add(5,'c','2-0',17,[criterion('reason','reason',1,[0,5],guide(13,'1 reason @ 5 marks','3 features')),criterion('features','features',3,[0,4],guide(13,'3 features @ 4 marks each'))],'One reason 5 + three features 4')
 for c in cards:
  if c['id'].startswith('he-2017-ol-sb-q5'):
   c['rows'][0]['contextNote']='Complete historical 2017 source wording retained. '+c['rows'][0].get('contextNote','')
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=19,marks=280,selectionDecisions='All original chart/menu inputs, age-specific reasons, required/flexible quotas, separately priced B2(a) and B3(b) roman tasks, unsplit B3(a) joint tariff, complete appliance/family/will source guidance retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
