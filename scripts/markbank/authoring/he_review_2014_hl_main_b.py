#!/usr/bin/env python3
"""2014 Higher B: original paired guidance, complete profiles and printed tariffs."""
from he_review_2014_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,19)}
 q={1:select(p[6],'1. Shown',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,suffix='',**extra):
  c=card(f'sb-q{n}{part}{roman or ""}{suffix}','B',f'Q{n}({part})'+(f'({roman})' if roman else '')+(f' — {suffix[1:]}' if suffix else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('using three different grocery store outlets.',1)[0]+'using three different grocery store outlets.'
  cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 chart=guide(8,'3 points @ 4 marks each','(b)');heads=['multiples were cheaper','low cost shop was the least expensive','local shop was the most expensive'];general=chart.split('multiples',1)[0]
 add(1,'a','0-1',12,[criterion(f'outlet-{i}',head,1,[0,4],general+' '+body) for i,(head,body) in enumerate(zip(heads,named(chart,heads)),1)],'3 required outlets × 4',questionFigureKey='home-economics-2014-hl-sb-q1-costs',questionFigureIncludesPrompt=False)
 judged(1,'b','0-1',3,4,'reasons',guide(8,'3 reasons @ 4 marks each')+' '+s[9].split('(c)',1)[0],questionFigureKey='home-economics-2014-hl-sb-q1-costs',questionFigureIncludesPrompt=False)
 judged(1,'c','0-5',3,3,'Protein rich foods',guide(9,'3 points @ 3 marks each','(d)'))
 grid=table_rows(d['scheme'][8].find_tables().tables[0],d['scheme'][8]);classification='Original table, read in its printed columns: '+'; '.join(' | '.join(r).rstrip(' |') for r in grid)
 complementary=guide(10,'2 points @ 4 marks each','• structure');structures=guide(10,'3 points @ 5 marks each');heads=['Primary Structure','Secondary Structure','Tertiary Structure']
 rows=[criterion('classification-groups','classification groups',3,[0,4],classification),criterion('classification-points','classification',6,[0,2],classification),criterion('complementary','supplementary value / complementary role',2,[0,4],complementary)]
 rows += [criterion(f'structure-{i}',head,1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(structures,heads)),1)]
 add(1,'d','0-5',47,rows,'Classification 3×4 + 6×2; complementary 2×4; three structures 5 each',figureKey='home-economics-2014-hl-sb-q1d-protein')
 judged(2,'a','0-9',5,4,'nutritional significance',guide(11,'5 points @ 4 marks each','(b)'))
 c=judged(2,'b','0-3',3,3,'factors',guide(11,'3 factors @ 3 marks each','2 methods @ 3 marks each'),suffix='-factors');c['questionText']=clean(select(prompt(2,'b'),'Describe each of the following:', '• two methods',include=True)).rstrip('• ').replace('Describe each of the following:','Describe the following:')
 c=judged(2,'b','0-3',2,3,'methods',guide(11,'2 methods @ 3 marks each','(c)'),suffix='-methods');c['questionText']='Describe '+select(prompt(2,'b'),'two methods',include=True)
 process=guide(11,'Process – Freezing, Refrigeration.',include=True)+' '+s[12]
 names=[v.strip() for v in select(process,'Process – Freezing, Refrigeration.',include=True)[:len('Process – Freezing, Refrigeration.')].removeprefix('Process – ').removesuffix('.').split(',')]+[select(process,token,include=True)[len(prefix):].split(':',1)[0] for token,prefix in [('Process - Vacuum Packing / Modified Atmospheric Packaging:','Process - '),('Process – Curing/Salting:','Process – '),('Process: Canning:','Process: '),('Process - Dehydration:','Process - ')]]
 add(2,'c','0-3',15,[menu('name','Name of process',1,2,names,'Choose ONE process; all remaining details must refer to that same process.'),criterion('process','underlying principle',3,[0,3],process),criterion('effect','effect of the process on meat',1,[0,4],process)],'Name 2 + process/principle 3×3 + effect 4')
 grid=table_rows(d['scheme'][12].find_tables().tables[0],d['scheme'][12]);assert len(grid)==3,grid
 linked=[f'{r[0]}: Potential hazards — {r[1]} Corresponding control measures — {r[2]}' for r in grid[1:]]
 rows=[criterion('preparation','preparation',1,[0,4],linked[0]),criterion('cooking','cooking',1,[0,4],linked[1]),criterion('other','4 others',4,[0,4],'Four ADDITIONAL points from either stage, linking potential hazards to corresponding controls. Complete original source: '+' '.join(linked))]
 add(3,'a','0-4',24,rows,'Preparation 4 + cooking 4 + four others × 4')
 cooking=select(select(s[14],'(b)','(c)'),'Cooking / underlying principle', '3 points @ 3 marks each',True);guidelines=select(select(s[14],'(b)','(c)'),'Guidelines -','1 point @ 2 marks',True);effect=select(select(s[14],'(b)','(c)'),'Effect -',include=True)
 add(3,'b','0-3',20,[criterion('principle','cooking / underlying principle',3,[0,3],cooking),criterion('guidelines','guidelines',3,[0,3],guidelines),criterion('effect','effect',1,[0,2],effect)],'Principle 3×3 + guidelines 3×3 + effect 2')
 heads=['Toxic food poisoning','Infectious food poisoning'];add(3,'c','0-4',6,[criterion(f'type-{i}',head,1,[0,3],body) for i,(head,body) in enumerate(zip(heads,named(guide(14,'2 points @ 3 marks each'),heads)),1)],'2 required types × 3')
 heads=['Sourcing consumer information','Design –','Value for money'];add(4,'a','1-3',12,[criterion(f'factor-{i}',head.rstrip(' –'),1,[0,4],body) for i,(head,body) in enumerate(zip(heads,named(select(select(s[15],'(a)','(b)'),'3 points @ 4 marks each'),heads)),1)],'3 required factors × 4')
 construction=guide(15,'Construction –','3 points @ 4 marks each');working=guide(15,'Working principle -','• guidelines for use.');use=guide(15,'Guidelines for use -')
 add(4,'b','1-3',26,[criterion('construction','construction',4,[0,2],construction),criterion('working','working principle',3,[0,4],working),criterion('use','guidelines for use',3,[0,2],use)],'Construction 4×2 + working principle 3×4 + use 3×2')
 heads=['Choosing','Using','Disposing'];add(4,'c','1-5',12,[criterion(f'stage-{i}',head,1,[0,4],body) for i,(head,body) in enumerate(zip(heads,named(guide(16,'3 points @ 4 marks each'),heads)),1)],'3 required stages × 4')
 judged(5,'a','2-0',4,4,'historical development',guide(17,'4 points @ 4 marks each','(b)'))
 heads=['Economic','Socialisation','Educational'];add(5,'b','2-0',15,[criterion(f'function-{i}',head,1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(17,'3 points @ 5 marks each'),heads)),1)],'3 required functions × 5',roman='i')
 c=judged(5,'b','2-0',2,5,'different state interventions',guide(18,'2 points @ 5 marks each','(c)'),roman='ii');c['stem']+=' '+prompt(5,'b','i')
 judged(5,'c','2-0',3,3,'role of grandparents',guide(18,'3 points @ 3 marks each'))
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=18,marks=280,selectionDecisions='Separate toughness factors9 and tenderising methods6. Coherent protein47, preservation15, grilling20 and microwave26 profiles retain all priced headings. Original complete cost/protein/HACCP tables, source continuations, required/flexible quotas and two distinct state interventions retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
