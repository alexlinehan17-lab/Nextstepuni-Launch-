#!/usr/bin/env python3
"""2011 Ordinary B: source-specific rows, original context and published tariffs."""
from he_review_2011_ol_main import *
from paper import strip_set_lines
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,15)}
 # Original page7 is strip-set: rebuild each printed line by glyph position.
 p[7]=tidy(' '.join(t for _,t in strip_set_lines(d['paper'][6]) if not t.startswith('Page ')))
 q={1:select(p[6],'1. The table',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,**extra):
  c=card(f'sb-q{n}{part}{roman or ""}','B',f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('Protein',1)[0].strip()
  if n==2:c['stem']=q[n].split('More portions',1)[0].strip()
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,label,guidance,**extra):
  return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Distinct points at the source’s printed value; no finer ladder is published. Complete original guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','0-9',6,3,'dietetic value',guide(8,'6 points @ 3 marks','(b)'),questionFigureKey='home-economics-2011-ol-sb-q1-fish',questionFigureIncludesPrompt=False)
 classes=examples(guide(8,'2 classes @ 4 marks','x sources'));sources=guide(8,'4 sources @ 3 marks','x functions in the body');functions=guide(8,'2 functions @ 4 marks')
 add(1,'b','0-7',28,[menu('classes','classification',2,4,chosen(classes,['saturated / animal','unsaturated / vegetable','polyunsaturated / marine'])),criterion('sources','sources',4,[0,3],sources),criterion('functions','functions in the body',2,[0,4],functions)],'2 classes × 4 + 4 sources × 3 + 2 functions × 4')
 essential=select(guide(9,'x essential fatty acids','x the benefit'),'7 marks');omega=select(guide(9,'x the benefit','(d)'),'7 marks')
 c=add(1,'c','0-7',7,[point('explanation',essential,7,'This source explanation carries seven marks; no smaller marking ladder is printed.')],'Essential fatty acids7');c.update(id='he-2011-ol-sb-q1c-essential',questionRef='2011 OL Section B Q1(c) — essential fatty acids',questionText='Explain each of the following: • essential fatty acids')
 c=add(1,'c','0-7',7,[point('benefit',omega,7,'This source explanation carries seven marks; no smaller marking ladder is printed.')],'Omega-3 benefit7');c.update(id='he-2011-ol-sb-q1c-omega3',questionRef='2011 OL Section B Q1(c) — omega-3 benefit',questionText='Explain each of the following: • the benefit of including omega-3 fatty acids in the diet.')
 adv=guide(9,'Advantages:','Disadvantages:');dis=guide(9,'Disadvantages:');add(1,'d','1-2',20,[criterion('advantages','advantages',2,[0,5],adv),criterion('disadvantages','disadvantages',2,[0,5],dis)],'2 advantages × 5 + 2 disadvantages × 5')
 judged(2,'a','0-1',4,5,'consumption',guide(10,'4 points @ 5 marks','(b)'),questionFigureKey='home-economics-2011-ol-sb-q2-fruit',questionFigureIncludesPrompt=False)
 table=d['scheme'][9].find_tables().tables[0].extract();assert table[0]==['Breakfast','Packed Lunch','Dinner'],table
 rows=[criterion(f'meal-{i}',heading,1,[0,6],'Include fruit/vegetables in this meal. Full source model: '+tidy(table[1][i])) for i,heading in enumerate(table[0])]
 add(2,'b','0-10',18,rows,'3 meals × 6')
 judged(2,'c','0-3',3,4,'guidelines',guide(10,'3 guidelines @ 4 marks'))
 judged(3,'a','0-9',4,5,'nutritive value',guide(11,'4 points @ 5 marks','(b)'))
 egg=guide(11,'Examples: 3 @ 3 marks','(c)');rows=[];groups=[]
 for i in [1,2,3]:
  rows.extend([criterion(f'use-{i}','Uses',1,[0,3],'Choose a different culinary use in each pair. Source: '+egg),criterion(f'example-{i}','Examples',1,[0,3],'One example matching the SAME use. Source: '+egg)])
  groups.append(dict(sourceCardId=f'he-2011-ol-sb-q3b-pair-{i}',label=f'Egg use / example {i}',marks=6,rowIds=[f'use-{i}',f'example-{i}']))
 add(3,'b','0-3',18,rows,'3 pairs × (use3 + example3)',taskGroups=groups)
 judged(3,'c','1-2',3,4,'consumer information',guide(11,'3 points @ 4 marks each'))
 resources=guide(12,'3 explanations @ 4 marks','(b)');rows=[];groups=[]
 for i in [1,2,3]:
  rows.extend([criterion(f'resource-{i}','resources',1,[0,4],'A different non-money resource for Tony’s family in each pair. Source: '+resources),criterion(f'explanation-{i}','explanations',1,[0,4],'Explain the SAME resource’s contribution. Source: '+resources)])
  groups.append(dict(sourceCardId=f'he-2011-ol-sb-q4a-pair-{i}',label=f'Resource / contribution {i}',marks=8,rowIds=[f'resource-{i}',f'explanation-{i}']))
 add(4,'a','1-0',24,rows,'3 resources × 4 + 3 explanations × 4',taskGroups=groups)
 welfare=examples(guide(12,'2 payments @ 4 marks','(c)'));add(4,'b','1-1',8,[menu('payments','payments',2,4,[v.strip() for v in welfare.split(',') if v.strip()],'Retain Tony and Julie’s original family context and the printed exclusions of job seeker’s benefit and children’s allowance.')],'2 payments × 4')
 headings=['x stage in life cycle','x employment patterns','x sex / gender roles.'];factor_rows=[]
 for i,body in enumerate(named(select(s[12],'(c)'),headings)):
  guidance=select(body,'2 points @ 3 marks');factor_rows.append(criterion(f'factor-{i}',headings[i][2:],2,[0,3],guidance))
 add(4,'c','1-0',18,factor_rows,'3 required factors × 2 points × 3')
 options=guide(13,'3 options @ 5 marks each','(ii)');labels=['marriage counselling','legal separation','divorce.'];bodies=named(options,['x '+v for v in labels])
 add(5,'a','2-1',15,[criterion(f'option-{i}',label,1,[0,5],'Historical 2011 procedure. Source: '+body[2:]) for i,(label,body) in enumerate(zip(labels,bodies),1)],'3 required options × 5',roman='i')
 pros=guide(13,'3 advantages, 3 disadvantages @ 3 marks each');rows=[];groups=[]
 for i,(label,body) in enumerate(zip(['Marriage counselling','Legal separation','Divorce'],named(pros,['x Marriage counselling','x Legal separation','x Divorce'])),1):
  adv=select(body,'Advantages:','Disadvantages:');dis=select(body,'Disadvantages:');rows.extend([criterion(f'advantage-{i}','Advantages',1,[0,3],label+' — '+adv),criterion(f'disadvantage-{i}','Disadvantages',1,[0,3],label+' — '+dis)]);groups.append(dict(sourceCardId=f'he-2011-ol-sb-q5aii-option-{i}',label=label,marks=6,rowIds=[f'advantage-{i}',f'disadvantage-{i}']))
 c=add(5,'a','2-1',18,rows,'3 options × (advantage3 + disadvantage3)',roman='ii',taskGroups=groups);c['stem']+='\n\n'+prompt(5,'a','i')
 judged(5,'b','2-1',1,5,'important',guide(14,'1 point @ 5 marks','(ii)'),roman='i')
 judged(5,'b','2-1',3,4,'features',guide(14,'3 features @ 4 marks each'),roman='ii')
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=18,marks=280,selectionDecisions='B1(c) has two independently priced seven-mark explanations. Profiles, three-meal menu and paired egg/resource tasks stay whole. B5(a)(ii) requires one advantage/disadvantage for each named option. Full will continuation on scheme14 retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
