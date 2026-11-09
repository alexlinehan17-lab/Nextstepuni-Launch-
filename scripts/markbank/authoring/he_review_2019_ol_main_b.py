#!/usr/bin/env python3
"""2019 Ordinary B: exact partial ladders, paired choices and shared roman tariffs."""
from he_review_2019_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,15)}
 q={1:select(p[6],'1. Bread',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def part(n,letter):return select(q[n],f'({letter})',f'({chr(ord(letter)+1)})' if f'({chr(ord(letter)+1)})' in q[n] else None)
 def prompt(n,letter,roman=''):
  v=part(n,letter)
  if roman:
   prefix=v.split('(i)',1)[0].strip();v=prefix+' '+re.split(r'\((?:i|ii)\)',select(v,f'({roman})'),1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,topic,marks,rows,notation,roman='',**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('Types of Baked Goods Purchased Weekly',1)[0].strip()
  c=card(f'sb-q{n}{letter}{roman}','B',f'Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,topic,count,steps,label,guidance,**extra):return add(n,letter,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; original steps '+str(steps),**extra)
 full=guide(8,'Comment: comparison','(ii)',True);rows=[];groups=[]
 for i in range(1,5):
  ids=[f'comment-{i}',f'reason-{i}'];rows += [criterion(ids[0],'Comment',1,[0,1,2],f'Choose FOUR different baked goods from the original five-bar chart. Comment on selected item {i}; all original models: '+full),criterion(ids[1],'Reasons',1,[0,2,3],f'Give a popularity reason for the SAME selected baked good {i}; no separate naming mark is printed. '+full)];groups.append(dict(sourceCardId=f'he-2019-ol-sb-q1ai-item-{i}',label=f'Baked good {i}',marks=5,rowIds=ids))
 fig=dict(questionFigureKey='home-economics-2019-ol-sb-q1-bread',questionFigureIncludesPrompt=False)
 add(1,'a','0-9',20,rows,'Four matching comment2/reason3 accounts',roman='i',taskGroups=groups,**fig)
 full=guide(8,'Use brown flour',include=True)
 add(1,'a','0-9',5,[criterion('modification','Modification',1,[0,1,2,3],'Choose ONE modification to ONE baked good from the original chart. '+full),criterion('reason','Reason',1,[0,2],'Give a reason matching the SAME modification. Source examples, without invented additional explanations: '+full)],'Modification3 + matching reason2',roman='ii',**fig)
 b=select(s[9],'(b)','(c)');add(1,'b','0-6',26,[criterion('classes','classification',3,[0,2],select(b,'(graded 2:0)','• dietary sources')),criterion('sources','dietary sources',3,[0,4],select(select(b,'• dietary sources','• functions'),'(graded 4:0)')),criterion('functions','functions in the body',2,[0,4],select(select(b,'• functions'),'(graded 4:0)'))],'Three classes2 + three sources4 + two functions4')
 judged(1,'c','0-1',3,[0,2,3],'ways',guide(9,'(graded 3:2:0)','(d)'))
 full=guide(9,'Additives:',include=True);heads=['Additives:','Nutritional information:','List of ingredients:','Storage instructions:'];add(1,'d','0-11',20,[criterion(f'item-{i}',head.rstrip(':'),1,[0,3,5],'Explain this REQUIRED item. '+model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'All four required consumer-information accounts5')
 judged(2,'a','0-1',4,[0,3,5],'factors',guide(10,'(graded 5:3:0)','(b)'))
 page=d['scheme'][9];boxes=sorted([fitz.Rect(v['rect']) for v in page.get_drawings() if 350<v['rect'].y0<400 and 100<v['rect'].height<150],key=lambda r:r.x0);assert len(boxes)==3;rows=[];groups=[]
 for i,(label,box) in enumerate(zip(['Breakfast','Lunch','Dinner'],boxes),1):
  model=tidy(page.get_text(clip=box+(-1,-1,1,1),sort=True));ids=[f'courses-{i}',f'beverage-{i}']
  rows += [criterion(ids[0],'2 courses',2,[0,1,2],f'{label}: provide TWO suitable courses for this meal, not every suggested course. Full original {label.lower()} model: '+model),criterion(ids[1],'beverage',1,[0,2],f'{label}: provide ONE suitable beverage for the SAME meal. Full original paired model: '+model)]
  groups.append(dict(sourceCardId=f'he-2019-ol-sb-q2b-meal-{i}',label=label,marks=6,rowIds=ids))
 add(2,'b','0-10',18,rows,'Three meals×(two courses2 + beverage2)',taskGroups=groups)
 full=guide(10,'Balancing energy intake and energy output:',include=True);models=named(full,['Balancing energy intake and energy output:','Basal metabolic rate:']);add(2,'c','0-1',12,[criterion('balance','balancing energy',1,[0,2,4],models[0]),criterion('bmr','BMR',1,[0,2,4],models[1]),criterion('other','1 other point',1,[0,2,4],'One ADDITIONAL point from either required category. Both printed roman asks share this single tariff; no 6/6 split is printed. '+full)],'Balancing energy4 + BMR4 + one additional4')
 full=guide(11,'Nutritive value:','(b)',True);heads=['Nutritive value:','Dietetic value:'];models=named(full,heads);add(3,'a','0-9',20,[criterion('nutritive','nutritive value',2,[0,2,4],models[0]),criterion('dietetic','dietetic value',2,[0,2,4],models[1]),criterion('other','1 other',1,[0,2,4],'One ADDITIONAL point from either category. The two original roman asks share 20 marks; no fixed 10/10 split. '+full)],'Two nutritive4 + two dietetic4 + one additional4')
 judged(3,'b','0-3',3,[0,2,3],'culinary uses',guide(11,'Culinary uses:','3 effects',True),roman='i')
 judged(3,'b','0-3',3,[0,2,3],'effects of heat',guide(11,'Effects of heat:','(c)',True),roman='ii')
 judged(3,'c','0-9',3,[0,2,4],'reasons',select(select(s[11],'(c)'),'(graded 4:2:0)'))
 full=guide(12,'Availability:','(b)',True);heads=['Availability:','Location:','Trends in housing development:'];add(4,'a','1-0',18,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,4,6],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Three required housing influences6 [0,4,6]')
 full=select(s[12],'(b)','(c)');judged(4,'b','1-1',3,[0,2,4],'advantages',select(select(full,'3 advantages','2 factors'),'(graded 4:2:0)'),roman='i');judged(4,'b','1-1',2,[0,2,4],'factors',select(select(full,'2 factors'),'(graded 4:2:0)'),roman='ii')
 judged(4,'c','1-5',3,[0,2,4],'ways',select(select(s[12],'(c)'),'(graded 4:2:0)'))
 full=select(s[13].split('(ii)',1)[0],'Economic:',include=True);heads=['Economic:','Educational:','Physical:','Social:'];add(5,'a','2-0',16,[criterion(f'function-{i}',head.rstrip(':'),1,[0,2,4],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'All FOUR required family functions4',roman='i')
 judged(5,'a','2-0',1,[0,1,2,4],'state assists',select(select(s[13],'(ii)','(b)'),'(graded 4:2:1:0)'),roman='ii')
 judged(5,'b','2-0',3,[0,2,5],'communication',select(select(s[13],'(b)'),'(graded 5:2:0)'))
 judged(5,'c','2-1',3,[0,2,5],'ways',guide(14,'(graded 5:2:0)'))
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=20,marks=280,selectionDecisions='All five chart choices, four linked comment/reason accounts, matching modification/reason, complete carbohydrate classes/sources/functions and all packaging headings; three menus with separately priced two courses/beverage each; flexible shared energy/BMR and cheese tariffs; separately priced culinary/heat, insurance and family-function roman asks; exact [0,2,5] communication/conflict ladders and full page-14 continuation.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
