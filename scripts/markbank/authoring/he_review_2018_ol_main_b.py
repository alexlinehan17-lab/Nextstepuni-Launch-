#!/usr/bin/env python3
"""2018 Ordinary B: source-only shared tariffs and separately priced conflict asks."""
from he_review_2018_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,14)}
 q={1:select(p[6],'1. Dietary',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def part(n,letter):return select(q[n],f'({letter})',f'({chr(ord(letter)+1)})' if f'({chr(ord(letter)+1)})' in q[n] else None)
 def prompt(n,letter,roman=None):
  v=part(n,letter)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('Pre‐prepared Beef Lasagne',1)[0].strip()
  c=card(f'sb-q{n}{letter}{roman or ""}','B',f'Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','i','0-5',5,4,'nutritional value',guide(8,'5 points @ 4 marks each','(ii)'),questionFigureKey='home-economics-2018-ol-sb-q1-lasagne',questionFigureIncludesPrompt=False)
 full=guide(8,'Accompaniment: 2 marks, Reason: 3 marks','(b)');add(1,'a','ii','0-10',5,[criterion('accompaniment','Accompaniment',1,[0,2],'Choose ONE suitable accompaniment consistently. Complete paired source guidance: '+full),criterion('reason','Reason',1,[0,3],'Give the matching reason for the SAME accompaniment. '+full)],'Accompaniment2 + matching reason3')
 classes=guide(8,'2 classes @ 4 marks each');sources=guide(9,'3 sources @ 4 marks each','functions in the body');functions=guide(9,'2 functions @ 3 marks each','(c)');add(1,'b',None,'0-5',26,[criterion('classes','classification',2,[0,4],classes),criterion('sources','dietary sources',3,[0,4],'ANY THREE sources across the complete animal/vegetable pools; no fixed heading quota. '+sources),criterion('functions','functions in the body',2,[0,3],functions)],'Two classes4 + three sources4 + two functions3')
 judged(1,'c',None,'0-5',3,3,'effects of heat',guide(9,'3 effects @ 3 marks each','(d)'))
 full=guide(9,'Advantages:',include=True);heads=['Advantages:','Disadvantages:'];add(1,'d',None,'1-2',20,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,5],v) for i,(head,v) in enumerate(zip(heads,named(full,heads)),1)],'Two advantages5 + two disadvantages5')
 full=guide(10,'(2 causes, 2 effects + 1 other)','(b)');causes,effects=named(full,['Causes:','Effects:']);add(2,'a',None,'0-1',20,[criterion('causes','causes',2,[0,4],causes),criterion('effects','effects',2,[0,4],effects),criterion('other','1 other',1,[0,4],'One ADDITIONAL cause or effect. Original roman(i)/(ii) asks share20 marks; no10/10 split. '+full)],'Two causes4 + two effects4 + one other4')
 full=guide(10,'Sample menus','(c)');heads=['Breakfast:','Lunch:','Dinner:'];add(2,'b',None,'0-10',18,[criterion(f'meal-{i}',head.rstrip(':'),1,[0,6],'Plan this complete meal for the SAME one-day osteoporosis menu. The source awards whole meals6, with no per-food allocation. Complete original model: '+v) for i,(head,v) in enumerate(zip(heads,named(full,heads)),1)],'Three whole meals6')
 c=judged(2,'c',None,'0-1',3,4,'changes',guide(10,'3 points @ 4 marks each'));c['rows'][0]['contextNote']='Choose ANY THREE dietary and/or lifestyle changes across both complete source pools; no fixed heading quota. '+c['rows'][0]['contextNote']
 full=guide(11,'(2 references to nutritive value, 2 references to dietetic value, plus 1 other)','(b)');heads=['Nutritive:','Dietetic:'];add(3,'a',None,'0-9',20,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,4],v) for i,(head,v) in enumerate(zip(heads,named(full,heads)),1)]+[criterion('other','1 other',1,[0,4],'One ADDITIONAL nutritive or dietetic point. Original inline roman(i)/(ii) asks share20 marks; no10/10 split. '+full)],'Two nutritive4 + two dietetic4 + one other4')
 names=semis(guide(11,'Cereal:','3 products @ 2 marks each'));full=guide(11,'Wheat:','(c)',True);add(3,'b',None,'0-9',12,[menu('cereals','cereals',3,2,names,'Choose ANY THREE different cereals from the full printed pool.'),criterion('products','products',3,[0,2],'Give a DIFFERENT product matching EACH of the SAME THREE selected cereals. Complete original paired source pools: '+full)],'Three cereals2 + three matching products2')
 full=select(guide(11,'(c)'),'2 points @ 3 marks each','(ii)');c=judged(3,'c','i','0-9',2,3,'difference',full);c['rows'][0]['contextNote']='Explain the difference using both full flour profiles. Two3 points are printed; no independent3-mark award is attached to a specific flour. '+c['rows'][0]['contextNote']
 judged(3,'c','ii','0-4',3,4,'guidelines',guide(11,'3 guidelines @ 4 marks each'))
 c=judged(4,'a',None,'1-2',3,5,'reasons',guide(12,'3 points @ 5 marks each','(b)'));c['rows'][0]['contextNote']='Original historical2018 account of the faulty-sale-item scenario. '+c['rows'][0]['contextNote']
 full=guide(12,'Name: 5 marks','(ii)');add(4,'b','i','1-2',5,[menu('name','Name',1,5,semis(full),'Name ONE reliable source from the full original historical agency/magazine/website pool.')],'One name5')
 judged(4,'b','ii','1-2',5,3,'procedure',guide(12,'5 points @ 3 marks each','(c)'))
 c=judged(4,'c',None,'1-2',3,5,'benefits',guide(12,'3 benefits @ 5 marks each'));c['rows'][0]['contextNote']='Historical2018 Small Claims fee and maximum award retained. '+c['rows'][0]['contextNote']
 judged(5,'a',None,'2-3',4,5,'support',guide(13,'4 ways @ 5 marks each','(b)'))
 judged(5,'b',None,'2-3',3,5,'independence',guide(13,'3 ways @ 5 marks each','(c)'))
 c=add(5,'c',None,'2-1',5,[criterion('definition','generation conflict',1,[0,5],guide(13,'1 point @ 5 marks','Outline two ways'))],'Definition5');c['id']+='-definition';c['conceptId']+='-definition';c['questionRef']+=' — definition';c['questionText']=prompt(5,'c').split('Outline two ways',1)[0].strip()
 c=add(5,'c',None,'2-1',10,[criterion('ways','ways',2,[0,5],guide(13,'2 ways @ 5 marks each'))],'Two ways5');c['id']+='-ways';c['conceptId']+='-ways';c['questionRef']+=' — ways';c['questionText']=select(prompt(5,'c'),'Outline two ways',include=True)
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=20,marks=280,selectionDecisions='Full lasagne source table; matched accompaniment/reason; protein guidance across pages8–9; shared osteoporosis and cereal20 tariffs; whole meals6; paired cereal/product pools; separately printed advice5/procedure15; all historical consumer guidance; B5c definition5 and ways10 are distinct priced tasks under one original anchor.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
