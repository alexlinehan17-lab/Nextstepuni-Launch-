#!/usr/bin/env python3
"""2020 Ordinary B: source-lifted choices and separately printed tariffs."""
from he_review_2020_ol_main import *
def build():
 d=documents();p={n:text(d['bc'],n) for n in range(2,5)};s={n:text(d['scheme'],n) for n in range(8,14)}
 q={1:p[2].rsplit('Question 1',1)[1].strip(),2:select(p[3],'Question 2','Question 3'),3:select(p[3],'Question 3'),4:select(p[4],'Question 4','Question 5'),5:select(p[4],'Question 5')};cards=[]
 def part(n,l,r=None):
  body=select(q[n],f'({l})',f'({chr(ord(l)+1)})' if f'({chr(ord(l)+1)})' in q[n] else None)
  if r:body=select(body,f'({r})','(ii)' if r=='i' else None)
  return body
 def add(n,l,topic,marks,rows,notation,r=None,**extra):
  prompt=re.sub(r'\s*\(\d+ marks\)\s*$','',part(n,l,r)).strip();stem=q[n].split('(a)',1)[0].strip()
  if n==1:
   stem=stem.split('The table below',1)[0].strip()
  key=f'sb-q{n}{l}'+(r or '');ref=f'Q{n}({l})'+(f'({r})' if r else '')
  c=card(key,'B',ref,topic,prompt,stem,marks,rows,2 if n==1 else 3 if n<=3 else 4,notation,**extra);cards.append(c);return c
 def source(page,l):return select(s[page],f'({l})',f'({chr(ord(l)+1)})' if f'({chr(ord(l)+1)})' in s[page] else None)
 def judged(n,l,topic,count,steps,label,guidance,r=None,**extra):return add(n,l,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; original steps '+str(steps),r,**extra)
 full=select(s[8],'Media influence:',include=True)
 judged(1,'a','0-1',4,[0,2,4,6],'reasons','Choose FOUR different reasons from all six original chart categories; complete original guidance: '+full,'i',questionFigureKey='home-economics-2020-ol-sb-q1-red-meat',questionFigureIncludesPrompt=False)
 judged(1,'a','0-5',1,[0,6],'protein food',select(s[9],'(graded 6:0)','(b)'),'ii')
 full=source(9,'b');heads=['• functions in the body','• dietary sources','• effect of deficiency.'];models=named(full,heads)
 specs=[('functions','functions in the body',2,[0,2,4]),('sources','dietary sources',3,[0,4]),('deficiency','effect of deficiency',1,[0,4])]
 add(1,'b','0-8',24,[criterion(key,label,count,steps,select(model,'(graded '+':'.join(map(str,reversed(steps)))+')')) for (key,label,count,steps),model in zip(specs,models)],'TWO functions4 + THREE sources4 + ONE deficiency4')
 judged(1,'c','0-8',2,[0,2,3],'ways',select(source(9,'c'),'(graded 3:2:0)'))
 full=select(source(9,'d'),'Selecting:',include=True);models=named(full,['Selecting:','Buying:'])
 add(1,'d','0-9',20,[criterion('selecting','Selecting',1,[0,3,5],models[0]),criterion('buying','Buying',1,[0,3,5],models[1]),criterion('other','2 other points',2,[0,3,5],'TWO additional distinct points from either category; no repeated credit. '+full)],'ONE selecting5 + ONE buying5 + TWO other5')
 full=source(10,'a');first=select(full,'(i)','(ii)');second=select(full,'(ii)')
 judged(2,'a','0-1',1,[0,2,4],'Explanation',select(first,'(graded 4:2:0)'),'i')
 judged(2,'a','0-1',3,[0,2,4],'factors',select(second,'(graded 4:2:0)'),'ii')
 judged(2,'b','0-1',4,[0,2,4],'guidelines',select(source(10,'b'),'(graded 4:2:0)'))
 # Read each original sample-menu column in its bounded table cell.
 grid=table_rows(d['scheme'][9].find_tables().tables[0],d['scheme'][9]);cells=[v for row in grid for v in row if v.startswith(('Breakfast ','Lunch ','Dinner '))];assert len(cells)==3,cells
 rows=[];groups=[]
 for i,(label,model) in enumerate(zip(['Breakfast','Lunch','Dinner'],cells),1):
  ids=[f'meal-{i}-courses',f'meal-{i}-drink'];rows += [criterion(ids[0],'2 courses',2,[0,1,2],f'TWO appropriate courses for this REQUIRED {label} meal. Full original sample menu, read as a single column: '+model),criterion(ids[1],'beverage',1,[0,2],f'ONE suitable beverage for the SAME {label} meal. '+model)];groups.append(dict(sourceCardId=f'he-2020-ol-sb-q2c-meal-{i}',label=label,marks=6,rowIds=ids))
 add(2,'c','0-10',18,rows,'THREE meals EACH two courses2 + beverage2',taskGroups=groups)
 full=select(source(11,'a'),'Nutritional value:',include=True);models=named(full,['Nutritional value:','Dietetic value:'])
 add(3,'a','0-9',20,[criterion('nutritive','nutritive value',2,[0,2,4],models[0]),criterion('dietetic','dietetic value',2,[0,2,4],models[1]),criterion('other','1 other',1,[0,2,4],'ONE additional distinct point from either category, no repeated credit. '+full)],'TWO nutritive4 + TWO dietetic4 + ONE other4; whole shared roman task')
 full=select(source(11,'b'),'Advantages:',include=True);models=named(full,['Advantages:','Disadvantages:'])
 add(3,'b','0-9',16,[criterion('advantages','Advantages',2,[0,2,4],models[0]),criterion('disadvantages','Disadvantages',2,[0,2,4],models[1])],'TWO advantages4 + TWO disadvantages4')
 full=select(source(11,'c'),'Metal:',include=True);rows=[];groups=[]
 for i in [1,2]:
  ids=[f'material-{i}',f'impact-{i}'];rows += [criterion(ids[0],'Food packaging material',1,[0,3],f'Name material {i} of TWO DIFFERENT materials. Full original paired pool (valid alternatives remain open): '+full),criterion(ids[1],'Impact',1,[0,2,4],f'ONE impact point about the SAME material {i}; use its matching original profile above. No further model is invented for an unprinted valid alternative.')];groups.append(dict(sourceCardId=f'he-2020-ol-sb-q3c-material-{i}',label=f'Packaging material {i}',marks=7,rowIds=ids))
 add(3,'c','0-11',14,rows,'TWO material profiles EACH name3 + impact4',taskGroups=groups)
 judged(4,'a','1-3',4,[0,2,4],'factors',select(source(12,'a'),'(graded 4:2:0)'))
 judged(4,'b','1-2',3,[0,2,4],'responsibilities',select(source(12,'b'),'(graded 4:2:0)'))
 full=source(12,'c');use=select(full,'• guidelines for use','• modern features');features=select(full,'• modern features','• care and cleaning.');care=select(full,'1 reference to care + 1 reference to cleaning')
 add(4,'c','1-3',22,[criterion('use','guidelines for use',3,[0,2,4],select(use,'(graded 4:2:0)')),criterion('features','modern features',2,[0,2],select(features,'(graded 2:0)')),criterion('care','care',1,[0,2,3],'ONE required reference to care. Complete original care/cleaning pool: '+care),criterion('cleaning','cleaning',1,[0,2,3],'ONE required reference to cleaning, distinct from care. '+care)],'THREE use4 + TWO features2 + ONE care3 + ONE cleaning3')
 full=source(13,'a');first=select(full,'(i)','(ii)');second=select(full,'(ii)')
 judged(5,'a','2-1',1,[0,2,3,5],'Definition',select(first,'(graded 5:3:2:0)'),'i')
 judged(5,'a','2-1',4,[0,3,5],'conditions','Historical 2020 scheme wording retained for this examination task. '+select(second,'(graded 5:3:0)'),'ii')
 judged(5,'b','2-1',3,[0,3,5],'benefits',select(source(13,'b'),'(graded 5:3:0)'))
 full=select(source(13,'c'),'Marriage counselling:',include=True);models=named(full,['Marriage counselling:','Legal separation:'])
 add(5,'c','2-1',10,[criterion('counselling','marriage counselling',1,[0,3,5],models[0]),criterion('separation','legal separation',1,[0,3,5],'Historical source account, including its full Judicial Separation continuation: '+models[1])],'ONE required counselling5 + ONE separation5')
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==280
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=19,marks=280,selectionDecisions='All six red-meat reasons; iron quotas; exact CHD/menu allocations and independently read menu columns; full fish flexible/shared roman task; paired environmental profiles; use/features/care/cleaning requirements; full historical marriage and separation guidance.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
