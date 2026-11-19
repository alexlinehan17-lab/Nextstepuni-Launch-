#!/usr/bin/env python3
"""2010 Ordinary B: source tariffs, paired responses and complete guidance."""
from he_review_2010_ol_main import *

def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,14)}
 q={1:'‘'+select(p[6],'1. ‘'),2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('Whole Milk',1)[0].strip()
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,guide,label='Published answer points',**extra):
  return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Use distinct points at the source’s printed value. No smaller marking steps are published. Complete source guidance: '+guide)],f'{count} points × {per}',**extra)
 judged(1,'a','0-9',3,3,guide(8,'(9)','(b)'),'differences',questionFigureKey='home-economics-2010-ol-sb-q1-milk',questionFigureIncludesPrompt=False)
 judged(1,'b','0-9',3,5,guide(8,'(15)'),'dietetic value',questionFigureKey='home-economics-2010-ol-sb-q1-milk',questionFigureIncludesPrompt=False)
 calcium=select(s[9],'• sources in the diet');labels=['• functions in the body','• effects of deficiency','• factors that affect absorption'];sources=select(calcium,'(12)',labels[0]);functions=select(calcium,'(8)',labels[1]) if calcium.count('(8)')==1 else select(calcium.split(labels[1],1)[0],'(8)');effects=select(select(calcium,labels[1],labels[2]),'(8)');absorption=select(select(calcium,labels[2],'(d)'),'(8)')
 add(1,'c','0-8',36,[criterion('sources','sources in the diet',3,[0,4],'Three sources. Complete printed list: '+sources),criterion('functions','functions in the body',2,[0,4],functions),criterion('deficiency','effects of deficiency',2,[0,4],effects),criterion('absorption','factors that affect absorption',2,[0,4],absorption)],'Sources 3 × 4 + functions 2 × 4 + deficiency 2 × 4 + absorption 2 × 4')
 judged(1,'d','0-11',4,5,guide(9,'(20)'),'food industry')
 judged(2,'a','0-9',4,5,guide(10,'(20)','(b)'),'nutritive value')
 menu_body=guide(10,'Menu: 2 courses @ 4 marks each','2 reasons @ 3 marks each');reasons=guide(10,'2 reasons @ 3 marks each','(c)')
 add(2,'b','0-10',14,[criterion('courses','Menu',2,[0,4],'Two courses in the same menu; use meat as the main ingredient and retain the low-income family context. Complete source model: '+menu_body),criterion('reasons','reasons',2,[0,3],'Two reasons supporting this menu. Complete source guidance: '+reasons)],'2 courses × 4 + 2 reasons × 3')
 names=guide(10,'Name: 2 @ 4 marks each','2 advantages @ 4 marks each');advantages=guide(10,'2 advantages @ 4 marks each');rows=[];groups=[]
 for i in range(1,3):
  rows += [criterion(f'type-{i}','Name',1,[0,4],'Choose a different processed meat in each pair. Source examples: '+names),criterion(f'advantage-{i}','advantage',1,[0,4],'One advantage of this SAME processed meat. Source examples: '+advantages)]
  groups.append(dict(sourceCardId=f'he-2010-ol-sb-q2c-pair-{i}',label=f'Processed meat {i}',marks=8,rowIds=[f'type-{i}',f'advantage-{i}']))
 add(2,'c','0-9',16,rows,'2 pairs × (name 4 + advantage 4)',taskGroups=groups)
 judged(3,'a','0-4',4,4,guide(11,'(16)','(b)'),'causes')
 preservation=select(s[11],'• method of preservation','(c)');method=select(preservation,'–','• suitable foods');foods=select(preservation,'• suitable foods','• how this method');process=select(preservation,'• how this method of preservation is carried out','• packaging');packaging=select(preservation,'• packaging')
 add(3,'b','0-3',24,[menu('method','method of preservation',1,4,[v.strip() for v in method.split(',')]),criterion('foods','suitable foods',1,[0,4],'Give TWO suitable foods for the selected method. The source prints four marks for this pair, with no separate per-food allocation. Complete examples: '+foods),criterion('process','how this method of preservation is carried out',3,[0,4],'Three points for the SAME chosen method. Complete printed method guidance: '+process),criterion('packaging','packaging',1,[0,4],'Packaging appropriate to the SAME method. Complete source examples: '+packaging)],'Method 4 + pair of foods 4 + process 3 × 4 + packaging 4')
 micro=guide(11,'2 points @ 5 marks each');judged(3,'c','0-4',2,5,micro,'uses of micro-organisms')
 judged(4,'a','1-3',4,5,guide(12,'(20)','(b)'),'factors')
 c=judged(4,'b','1-2',3,4,guide(12,'(12)','(c)'),'Small Claims Procedure');c['rows'][0]['contextNote']+=' Historical procedure and amounts are retained exactly from the 2010 marking scheme.'
 income=guide(12,'2 sources @ 3 marks each','4 areas @ 3 marks each');spending=guide(12,'4 areas @ 3 marks each')
 add(4,'c','1-1',18,[criterion('income','sources of income',2,[0,3],income),criterion('expenditure','areas of expenditure',4,[0,3],spending)],'2 sources × 3 + 4 areas × 3')
 needs=guide(13,'(1 reference to physical, 1 reference to psychological and 1 other)','(b)');physical=select(needs,'physical:','psychological:');psychological=select(needs,'psychological:')
 add(5,'a','2-0',15,[criterion('physical','physical',1,[0,5],physical),criterion('psychological','psychological',1,[0,5],psychological),criterion('other','1 other',1,[0,5],'One further distinct physical OR psychological need. Complete source guidance: '+needs)],'3 needs × 5; at least one physical and one psychological')
 judged(5,'b','2-1',4,5,guide(13,'4 rights @ 5 marks each','(c)'),'rights')
 judged(5,'c','2-1',3,5,guide(13,'3 examples @ 5 marks each'),'support')
 assert len(cards)==16 and sum(c['totalMarks'] for c in cards)==280
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=16,marks=280,selectionDecisions='Menus, processed-meat pairs, preservation profiles and same-family income/expenditure remain whole. Suitable foods retain the source’s four-mark pair with no inferred per-food tariff. Child-needs minimum headings and flexible third point explicitly retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
