#!/usr/bin/env python3
"""2016 Ordinary B: complete coherent meals, budgets and historical source models."""
from copy import deepcopy
from he_review_2016_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,15)}
 q={1:select(p[6],'1. ‘Saturated',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('Pre-prepared meal',1)[0].strip() if part=='a' else stem.split('The table below',1)[0].strip()
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 full=guide(8,'Name: 2 marks, Reasons: 3 @ 6 marks each','(b)');names=['Fisherman’s pie:','Chicken curry with rice:'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(full,names)),1):
  variants.append(dict(id=f'meal-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),2),criterion('reasons','Reasons',3,[0,6],'Three reasons for the SAME meal and the young sports-person context. Both source meal models are available. The original fish-pie model says low in saturated fat; this wording is retained as printed. '+body)]))
 add(1,'a','0-10',20,deepcopy(variants[0]['rows']),'Meal name2 + reasons3×6',answerVariants=variants,questionFigureKey='home-economics-2016-ol-sb-q1-meals',questionFigureIncludesPrompt=False)
 add(1,'b','0-7',28,[criterion('classes','Classification',2,[0,4],guide(8,'2 classes @ 4 marks each')),criterion('functions','functions in the body',2,[0,4],guide(9,'2 functions @ 4 marks each','• dietary sources')),criterion('sources','dietary sources',4,[0,3],guide(9,'4 sources @ 3 marks each','(c)'))],'Classes2×4 + functions2×4 + sources4×3')
 judged(1,'c','0-7',3,4,'ways',guide(9,'3 ways @ 4 marks each','(d)'))
 judged(1,'d','1-5',4,5,'environmentally aware',guide(9,'4 ways @ 5 marks each'))
 judged(2,'a','0-10',4,5,'reasons',guide(10,'4 reasons @ 5 marks each','(b)'))
 full=guide(10,'3 menus (meals) @ 6 marks each','(c)');heads=['Breakfast','Lunch','Dinner'];add(2,'b','0-10',18,[criterion(f'meal-{i}',head,1,[0,6],'One complete meal in the SAME day’s menu. The source prints no per-course split. The original lacto-vegetarian dinner contains Egg Mayonnaise; that source anomaly is retained visibly without an invented replacement. '+body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)],'Three complete meals×6',figureKey='home-economics-2016-ol-sb-q2b-menu')
 full=guide(10,'(1 reference to preparation, 1 reference to cooking, plus 1 other)');add(2,'c','0-3',12,[criterion('preparation','preparation',1,[0,4],full),criterion('cooking','cooking',1,[0,4],full),criterion('other','1 other',1,[0,4],'One ADDITIONAL point from either required heading. '+full)],'Preparation4 + cooking4 + one other4')
 full=guide(11,'(1 reference to nutritional value, 1 reference to dietetic value, plus 2 others)','(b)');nutrition,diet=named(full,['Nutritional:','Dietetic:']);add(3,'a','0-9',20,[criterion('nutrition','nutritional value',1,[0,5],nutrition),criterion('dietetic','dietetic value',1,[0,5],diet),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points from either required heading. The printed roman asks share this flexible twenty-mark allocation; no ten/ten split is printed. '+full)],'Nutrition5 + dietetic5 + two others×5')
 full=guide(11,'(1 reference to storing, 1 reference to effects of heat, plus 2 others)','(c)');storing,heat=named(full,['Storing:','Effects of heat:']);add(3,'b','0-3',20,[criterion('storage','storing',1,[0,5],storing),criterion('heat','effects of heat',1,[0,5],heat),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points from either required heading. Both printed roman asks remain in this shared twenty-mark account. '+full)],'Storage5 + heat5 + two others×5')
 judged(3,'c','0-11',2,5,'items',guide(11,'2 items @ 5 marks each'))
 judged(4,'a','1-1',4,5,'reasons',guide(12,'4 reasons @ 5 marks each','(b)'))
 c=judged(4,'b','1-1',5,4,'weekly budget plan',guide(12,'5 points @ 4 marks each','(c)'));c['rows'][0]['contextNote']='Give ONE coherent weekly budget for Saoirse’s €220 allowance, including rent and her cycling context. Five published four-mark points; no compulsory category quota or amount/reason split is printed. Complete original percentage allocation pool: '+guide(12,'5 points @ 4 marks each','(c)')
 full=guide(12,'Name: 5 marks, Reason: 1 reason @ 5 marks');names=['An Post - deposit account:','Credit union - share account:','Bank - deposit account:','Building society:'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(full,names)),1):
  note='Use the SAME savings account for the name and reason, for Saoirse. Original historical 2016 conditions retained. '
  if i==4:note+='The source names Building society but prints no reason model; none has been invented. '
  variants.append(dict(id=f'account-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),5),criterion('reason','Reason',1,[0,5],note+body)]))
 variants.append(dict(id='another-account',label='Another valid savings account',rows=[criterion('name','Name',1,[0,5],'One suitable savings account for Saoirse; all original historical source choices remain available.'),criterion('reason','Reason',1,[0,5],'One reason for the SAME account. No additional source model is printed.')]))
 add(4,'c','1-1',10,deepcopy(variants[0]['rows']),'Name5 + reason5',answerVariants=variants)
 judged(5,'a','2-1',3,5,'marriage',guide(13,'3 points @ 5 marks each','(b)'))
 c=judged(5,'b','2-1',4,5,'rights',guide(13,'4 points @ 5 marks each','(c)'));c['rows'][0]['contextNote']='Cover BOTH rights and responsibilities within FOUR points. The source gives no separate quota or ten/ten split for the two printed roman asks. Original complete historical 2016 guidance: '+guide(13,'4 points @ 5 marks each','(c)')
 full=guide(13,'Name: 5 marks, Account: 2 points @ 5 marks each')+' '+s[14];names=['Marriage counselling:','Family mediation:','Legal separation:','Judicial separation:','Legal nullity:','Church nullity:','Divorce:'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(full,names)),1):
  variants.append(dict(id=f'option-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),5),criterion('account','Account',2,[0,5],'Two details of the SAME selected option. Complete original historical 2016 terms and legal conditions retained: '+body)]))
 variants.append(dict(id='another-option',label='Another valid option',rows=[criterion('name','Name',1,[0,5],'One option for couples experiencing marriage difficulties; all seven original models remain available.'),criterion('account','Account',2,[0,5],'Two details of the SAME option. No additional source model is printed.')]))
 add(5,'c','2-1',15,deepcopy(variants[0]['rows']),'Name5 + account2×5',answerVariants=variants)
 assert len(cards)==16 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=16,marks=280,selectionDecisions='Three roman pairs B3(a),B3(b),B5(b) remain coherent shared20 accounts. Both meal choices, whole-day menu, full lipids28 and coherent220EUR budget retained. All savings and seven marriage-option models, continuation page14 and visible original model gaps/anomalies preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
