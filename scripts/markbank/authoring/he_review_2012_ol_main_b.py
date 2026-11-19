#!/usr/bin/env python3
"""2012 Ordinary Section B: original source selections and explicit tariffs."""
from he_review_2012_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n).replace('\uf0b7','•') for n in range(7,13)}
 q={1:select(p[6],'1. The',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,suffix='',custom=None,**extra):
  c=card(f'sb-q{n}{part}{roman or ""}{suffix}','B',f'Q{n}({part})'+(f'({roman})' if roman else '')+(' — '+suffix[1:] if suffix else ''),topic,custom or prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('(Irish Universities Nutrition Alliance)',1)[0]+'(Irish Universities Nutrition Alliance)'
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} × {per}',**extra)
 factors=named(guide(7,'6 factors @ 4 marks each','(b)'),['Taste:','Health & Nutrition:','Cost:','Convenience:','Weight Control:','Mood:'])
 add(1,'a','0-1',24,[criterion(f'factor-{i}',v.split(':',1)[0],1,[0,4],'Use the ORIGINAL chart and comment/elaborate on this factor. Source: '+v) for i,v in enumerate(factors,1)],'6 required factors × 4',questionFigureKey='home-economics-2012-ol-sb-q1-choice',questionFigureIncludesPrompt=False)
 add(1,'b','0-8',24,[criterion('sources','main food sources',2,[0,4],guide(7,'2 sources @ 4 marks')),criterion('functions','biological functions',2,[0,4],guide(8,'2 functions @ 4 marks','• effect of deficiency')),criterion('deficiency','effect of deficiency',1,[0,4],guide(8,'1 effect @ 4 marks','• role in mineral absorption.')),criterion('absorption','role in mineral absorption',1,[0,4],guide(8,'1 role @ 4 marks','(c)'))],'Sources 2×4 + functions 2×4 + deficiency4 + absorption4')
 preparation=guide(8,'Preparation:','Cooking:');cooking=guide(8,'Cooking:','(d)')
 add(1,'c','0-3',12,[criterion('preparation','preparing',1,[0,4],preparation),criterion('cooking','cooking',1,[0,4],cooking),criterion('other','one other',1,[0,4],'One additional distinct method from EITHER heading; the source requires one reference to each plus one other. Preparation: '+preparation+' Cooking: '+cooking)],'One preparation4 + one cooking4 + one other4')
 labels=['list of ingredients','weight','nutritional information','best before date','country of origin.'];body=guide(8,'5 items @ 4 marks')+' '+s[9].split('2.',1)[0]
 bodies=named(body,['• '+v for v in labels]);add(1,'d','1-2',20,[criterion(f'item-{i}',label,1,[0,4],v[2:]) for i,(label,v) in enumerate(zip(labels,bodies),1)],'5 required items × 4')
 full=prompt(2,'a');sources_prompt=full.split(' and state',1)[0];reasons_prompt='state'+full.split(' and state',1)[1]
 judged(2,'a','0-9',3,4,'sources',guide(9,'Sources:','2 reasons @ 4 marks'),suffix='-sources',custom=sources_prompt)
 judged(2,'a','0-9',2,4,'reasons',guide(9,'Reasons:','(b)'),suffix='-reasons',custom=reasons_prompt)
 judged(2,'b','0-9',3,5,'nutritive value',guide(9,'3 points @ 5 marks','(c)'))
 full=prompt(2,'c');definition=full.split('Comment',1)[0].strip();consumption='Comment'+full.split('Comment',1)[1]
 judged(2,'c','0-11',1,5,'explanation',guide(9,'explanation = 5 marks','2 points @ 5 marks'),suffix='-definition',custom=definition)
 judged(2,'c','0-11',2,5,'increased consumption',guide(9,'2 points @ 5 marks'),suffix='-consumption',custom=consumption)
 judged(3,'a','0-1',4,4,'factors',guide(10,'4 factors @ 4 marks','(b)'))
 table=d['scheme'][9].find_tables().tables[0].extract();assert table[0]==['Breakfast','Lunch','Dinner'],table
 add(3,'b','0-10',18,[criterion(f'meal-{i}',head,1,[0,6],'Plan this meal as part of the complete daily menu for teenagers. Original example: '+tidy(' '.join(row[i] or '' for row in table[1:]))) for i,head in enumerate(table[0])],'3 meals × 6; no per-food split')
 judged(3,'c','0-1',4,4,'changes',guide(10,'4 changes @ 4 marks'))
 judged(4,'a','1-1',4,5,'guidelines',guide(11,'4 guidelines @ 5 marks','(b)'))
 judged(4,'b','1-1',4,3,'ways',guide(11,'4 ways @ 3 marks','(c)'))
 full=prompt(4,'c');judged(4,'c','1-1',3,4,'reasons',guide(11,'3 reasons @ 4 marks','2 saving schemes @ 3 marks'),suffix='-reasons',custom=full.split(' and name',1)[0])
 judged(4,'c','1-1',2,3,'saving schemes',guide(11,'2 saving schemes @ 3 marks'),suffix='-schemes',custom='name'+full.split(' and name',1)[1])
 judged(5,'a','2-0',4,5,'functions',guide(12,'4 functions @ 5 marks','(ii)'),roman='i')
 c=judged(5,'a','2-0',2,4,'examples',guide(12,'2 examples @ 4 marks','(b)'),roman='ii');c['stem']=prompt(5,'a','i')
 judged(5,'b','2-0',3,4,'changes',guide(12,'3 changes @ 4 marks','(c)'))
 c=judged(5,'c','2-1',2,5,'protection',guide(12,'2 points @ 5 marks'));c['rows'][0]['contextNote']='Historical 2012 examination guidance for the named Act. '+c['rows'][0]['contextNote']
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=20,marks=280,selectionDecisions='Three independently priced companion pairs split at B2(a) 12/8, B2(c) 5/10 and B4(c) 12/6. B1 required headings, flexible preparation/cooking third point, all five labelling headings and dependent daily menu preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
