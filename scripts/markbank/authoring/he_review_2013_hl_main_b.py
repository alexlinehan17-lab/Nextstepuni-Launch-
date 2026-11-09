#!/usr/bin/env python3
"""2013 Higher B: full source continuations, printed quotas, no invented model."""
from he_review_2013_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,14)}
 q={1:select(p[6],'1. Irish',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,**extra):
  c=card(f'sb-q{n}{part}{roman or ""}','B',f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('Department of Health and Children)',1)[0]+'Department of Health and Children)'
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 chart=guide(8,'Expect reference to 4 food shelves')+' '+s[9].split('(b)',1)[0]
 c=judged(1,'a','0-1',4,6,'food shelves',chart,questionFigureKey='home-economics-2013-hl-sb-q1-pyramid',questionFigureIncludesPrompt=False);c['rows'][0]['contextNote']='The paper asks about EACH of five shelves; the scheme explicitly expects FOUR shelf references at 6 marks each. All five original source models remain below. Apply the printed 24-mark tariff without inventing a fifth allocation. '+c['rows'][0]['contextNote']
 judged(1,'b','0-1',4,4,'factors',guide(9,'4 points @ 4 marks each','(c)'))
 judged(1,'c','0-7',2,4,'significance',guide(9,'2 points @ 4 marks each','(d)'))
 bodies=named(guide(9,'3 points @ 4 marks each','(e)'),['Cis fatty acid --','Trans fatty acids -','Omega 3 fatty acids –']);add(1,'d','0-7',12,[criterion(f'fatty-acid-{i}',head,1,[0,4],'Original structure description: '+v) for i,(head,v) in enumerate(zip(['cis fatty acids','trans fatty acids','omega 3 fatty acids'],bodies),1)],'3 required structures × 4')
 judged(1,'e','1-2',5,4,'food labelling',guide(9,'5 points @ 4 marks each'))
 choice=guide(10,'Choice -','Presentation –');presentation=guide(10,'Presentation –','(b)');add(2,'a','0-10',12,[criterion('choice','choice',1,[0,4],choice),criterion('presentation','presentation',1,[0,4],presentation),criterion('other','1 other',1,[0,4],'One ADDITIONAL point from either heading. Original choice guidance: '+choice+' Presentation: '+presentation)],'Choice4 + presentation4 + one other4')
 judged(2,'b','0-11',2,4,'uses',guide(10,'2 points @ 4 marks each','(ii)'),roman='i')
 tests=guide(10,'Name of category = 3 marks, Purpose = 3 marks','(c)');bodies=named(tests,['Preference test:','Difference test:','Descriptive test:']);rows=[];groups=[]
 for i,body in enumerate(bodies,1):
  name,purpose=body.split(':',1);rows.extend([point(f'name-{i}',name,3),criterion(f'purpose-{i}','Purpose',1,[0,3],'Purpose of the SAME category. Source: '+purpose)]);groups.append(dict(sourceCardId=f'he-2013-hl-sb-q2bii-pair-{i}',label=name,marks=6,rowIds=[f'name-{i}',f'purpose-{i}']))
 add(2,'b','0-11',18,rows,'3 categories × (name3 + purpose3)',roman='ii',taskGroups=groups)
 judged(2,'c','0-10',3,4,'reasons',select(select(s[10],'(c)'),'3 points @ 4 marks each'))
 judged(3,'a','0-4',3,5,'food spoilage',select(select(s[11],'(a)','(b)'),'3 points @ 5 marks each'))
 no_model='The original scheme gives the criteria and tariffs for this chosen bacterium, but provides NO named bacterium or model answers. Supply a coherent profile of ONE food-poisoning bacterium; no additional model has been invented. '
 rows=[criterion('name','Name',1,[0,2],no_model+'Name one type.'),criterion('growth','conditions necessary for growth',3,[0,2],no_model+'Three growth conditions for the SAME type.'),criterion('source','source',1,[0,2],no_model+'One source of the SAME type.'),criterion('reproduction','reproduction / growth of bacteria',2,[0,2],no_model+'Two points about the SAME type.'),criterion('foods','high risk foods',3,[0,2],no_model+'Three foods associated with the SAME type.')]
 add(3,'b','0-4',20,rows,'Name2 + growth3×2 + source2 + reproduction2×2 + foods3×2')
 judged(3,'c','0-3',3,5,'irradiation',select(select(s[11],'(c)'),'3 points @ 5 marks each'))
 judged(4,'a','1-0',4,5,'factors',guide(12,'4 points @ 5 marks each','(b)'))
 framework=guide(12,'(3 points @ 2 marks for each - inputs, throughputs and outputs)','(c)');heads=['Inputs:','Throughputs:','Outputs / Evaluation:'];add(4,'b','1-0',18,[criterion(f'heading-{i}',head[:-1],3,[0,2],'Three points for this required heading, applied to the SCHOOL GRADUATION COMMITTEE event. Source: '+body) for i,(head,body) in enumerate(zip(heads,named(framework,heads)),1)],'3 headings × 3 points × 2')
 judged(4,'c','1-0',3,4,'decision making',guide(12,'3 points @ 4 marks each'))
 heads=['Culture:','Norms:','Values:','Role:'];add(5,'a','2-0',12,[criterion(f'term-{i}',head[:-1],1,[0,3],body) for i,(head,body) in enumerate(zip(heads,named(guide(13,'4 points @ 3 marks each','(b)'),heads)),1)],'4 required terms × 3')
 change=guide(13,'(1 ref. to social, 1 ref. to economic, 1 ref. to technological change + 1 other)','(c)');heads=['Social:','Economic:','Technological –'];rows=[criterion(f'heading-{i}',head.rstrip(': –'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(change,heads)),1)];rows.append(criterion('other','1 other',1,[0,6],'One ADDITIONAL distinct point from any required heading. Full source: '+change));add(5,'b','2-0',24,rows,'Social6 + economic6 + technological6 + one other6')
 law=guide(13,'(Name of Act = 3mark, 1point @ 4marks) x 2');names=chosen(law,['Domestic Violence Act 1996','Childcare Act 1991','Children’s Act 1997','Family Law (Maintenance of Spouse and Children) Act 1976','Family Home Protection Act 1976','Judicial Separation or Divorce Act','Succession Act 1965']);rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'act-{i}','Name of Act',1,3,names,'Choose two DIFFERENT Acts as applicable to this historical 2013 task.'),criterion(f'protection-{i}','protection',1,[0,4],'One point on the SAME named Act. Complete original historical source: '+law)]);groups.append(dict(sourceCardId=f'he-2013-hl-sb-q5c-act-{i}',label=f'Act {i}',marks=7,rowIds=[f'act-{i}',f'protection-{i}']))
 add(5,'c','2-1',14,rows,'2 Acts × (name3 + protection4)',taskGroups=groups)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=18,marks=280,selectionDecisions='B1 four-shelf tariff discrepancy visible with complete five-shelf models. B2(b) independently8/18. Flexible quotas, required framework headings and chosen Act profiles preserved. B3(b) source criteria only, explicitly no model bacterium/answers on every priced row.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
