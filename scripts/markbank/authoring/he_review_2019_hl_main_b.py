#!/usr/bin/env python3
"""2019 Higher B: source allocations, full choices and explicit unresolved tariff conflict."""
from copy import deepcopy
from he_review_2019_hl_main import *
AMBIGUITY='Unresolved numeric source ambiguity: scheme physical page 12 prints 2:1:0 for conditions, source and high-risk foods; the corresponding page 13 table headers print 2:0. Neither establishes precedence. Only common 0/2 awards are offered here. Leave a response that may merit the disputed 1 mark unassessed pending authoritative clarification; do not force it to 0 or 2.'
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,16)}
 q={1:select(p[6],'1. Over',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def part(n,letter):return select(q[n],f'({letter})',f'({chr(ord(letter)+1)})' if f'({chr(ord(letter)+1)})' in q[n] else None)
 def prompt(n,letter,roman=''):
  v=part(n,letter)
  if roman:v=re.split(r'\((?:i|ii)\)',select(v,f'({roman})'),1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,topic,marks,rows,notation,roman='',**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('Low sugar',1)[0].strip()
  c=card(f'sb-q{n}{letter}{roman}','B',f'Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,topic,count,steps,label,guidance,**extra):return add(n,letter,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; printed steps '+str(steps),**extra)
 fig=dict(questionFigureKey='home-economics-2019-hl-sb-q1-survey',questionFigureIncludesPrompt=False)
 judged(1,'a','0-10',4,[0,2,3],'factors',guide(8,'(graded 3:2:0)','(b)'),**fig)
 judged(1,'b','0-1',4,[0,1,2,3],'benefits','Discuss motivations for FOUR benefits from the original chart. The source gives assessor guidance, not model benefit explanations: '+guide(8,'(graded 3:2:1:0)'),**fig)
 snacks=guide(9,'(6)','Merits: 4 points');merits=guide(9,'(12)','(d)')
 add(1,'c','0-10',18,[criterion('snacks','Description',2,[0,2,3],'Describe TWO healthy snacks. These are source suggestions; naming alone is not a complete description: '+snacks),criterion('merits','Merits',4,[0,1,2,3],'Four merits of the SAME TWO chosen snacks. The source requires four points overall, with no fixed two-per-snack split. '+merits)],'Two snack descriptions3 + four matching merits3')
 full=guide(9,'Sources:','(e)',True);heads=['Sources:','Biological functions:','Effects of deficiency:'];add(1,'d','0-8',18,[criterion(f'heading-{i}',head.rstrip(':'),3,steps,model) for i,(head,steps,model) in enumerate(zip(heads,[[0,1,2],[0,2],[0,2]],named(full,heads)),1)],'Three sources2 + three functions2 + three deficiency effects2')
 full=guide(9,'Attracts: visual',include=True);heads=['Attracts:','Informs:'];models=named(full,heads)
 add(1,'e','0-11',20,[criterion('attracts','Attracts',1,[0,3,5],models[0]),criterion('informs','Informs',1,[0,3,5],models[1]),criterion('other','2 other points',2,[0,3,5],'TWO additional points from either category; no repeated credit. '+full)],'One attracts5 + one informs5 + two additional5')
 judged(2,'a','0-9',5,[0,1,2,3],'nutritional significance','Assess FIVE points with a MAXIMUM of TWO mineral references and TWO vitamin references. Do not award a third reference within either restricted category. '+guide(10,'Protein:','(b)',True))
 judged(2,'b','0-10',4,[0,1,2],'strategies',guide(10,'(8)','4 guidelines'),roman='i')
 judged(2,'b','0-3',4,[0,2,3],'guidelines',guide(10,'(12)','(c)'),roman='ii')
 add(2,'c','0-8',15,[criterion('properties','Properties',3,[0,1],guide(10,'Properties: white',include=True)),criterion('sources','sources',3,[0,1],guide(11,'(graded 1:0)','3 functions')),criterion('functions','Biological functions',3,[0,2,3],guide(11,'Biological functions:',include=True))],'Three properties1 + three sources1 + three functions3')
 judged(3,'a','0-4',4,[0,2,3,5],'causes',guide(12,'(graded 5:3:2:0)','(b)'))
 grid=table_rows(d['scheme'][12].find_tables().tables[0],d['scheme'][12]);assert len(grid)==5
 variants=[]
 for i,(name,conditions,source,reproduction,foods) in enumerate(grid[1:],1):
  rows=[point('name',name,2),criterion('conditions','conditions necessary for growth',3,[0,2],AMBIGUITY+' For the SAME '+name+' profile: '+conditions),criterion('source','source',1,[0,2],AMBIGUITY+' For the SAME '+name+' profile: '+source),criterion('reproduction','reproduction/growth of bacteria',3,[0,2],'Use the SAME '+name+' profile. Original scientific wording is reproduced: '+reproduction),criterion('foods','high risk foods',2,[0,2],AMBIGUITY+' For the SAME '+name+' profile: '+foods)]
  variants.append(dict(id=f'bacterium-{i}',label=name,rows=rows))
 for i,name in enumerate(['Staphylococcus Aureus','Clostridium Perfringens','Campylobacter'],5):
  rows=[point('name',name,2)]
  for key,label,count in [('conditions','conditions necessary for growth',3),('source','source',1),('reproduction','reproduction/growth of bacteria',3),('foods','high risk foods',2)]:rows.append(criterion(key,label,count,[0,2],(AMBIGUITY+' ' if key!='reproduction' else '')+'Use the SAME '+name+' throughout. This bacterium is accepted by name only in the original source; no '+label+' model is printed or invented.'))
  variants.append(dict(id=f'bacterium-{i}',label=name,rows=rows))
 rows=[criterion('name','Name of food poisoning bacteria',1,[0,2],'Name ONE valid food-poisoning bacterium. The original source ends its named alternatives with “etc.”; this open alternative preserves that scope without inventing another model.')]
 for key,label,count in [('conditions','conditions necessary for growth',3),('source','source',1),('reproduction','reproduction/growth of bacteria',3),('foods','high risk foods',2)]:rows.append(criterion(key,label,count,[0,2],(AMBIGUITY+' ' if key!='reproduction' else '')+'Use the SAME selected bacterium throughout. No additional source model is printed or invented.'))
 variants.append(dict(id='other-bacterium',label='Another valid food-poisoning bacterium',rows=rows))
 add(3,'b','0-4',20,deepcopy(variants[0]['rows']),'Name2 + conditions3×2 + source2 + reproduction3×2 + high-risk foods2×2; disputed one-mark case held',answerVariants=variants)
 judged(3,'c','0-4',2,[0,3,5],'role',guide(13,'(graded 5:3:0)'))
 judged(4,'a','1-1',5,[0,2,4],'factors',select(s[14].split('(b)',1)[0],'(graded 4:2:0)'))
 judged(4,'b','1-1',5,[0,2,4],'strategies',select(select(s[14],'(b)','(c)'),'(graded 4:2:0)'))
 judged(4,'c','1-1',2,[0,3,5],'role',guide(14,'(graded 5:3:0)'))
 full=guide(15,'Socialisation:','(b)',True);heads=['Socialisation:','Socio economic group:','Social mobility:','Social change:','Kinship:'];add(5,'a','2-0',14,[criterion(f'term-{i}',head.rstrip(':'),1,[0,2,3] if i<5 else [0,1,2],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Four required terms3 + required kinship2')
 judged(5,'b','2-0',4,[0,1,2,3],'characteristics','Describe characteristics across FOUR points. The original source only names these structures; no characteristic model is printed or invented, and names alone do not complete the task. '+select(select(s[15],'(b)','(c)'),'(graded 3:2:1:0)'))
 full=guide(15,'Social: decline',include=True);heads=['Social:','Economic:','Technological:'];add(5,'c','2-0',24,[criterion(f'category-{i}',head.rstrip(':'),2,[0,2,4],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Two REQUIRED references each to social/economic/technological4')
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=18,marks=280,selectionDecisions='Original survey/choice pools, paired snack merits, calcium and Vitamin C headings, exact packaging quotas, vegetable category caps, both separately priced B2(b) romans, seven coherent bacterium alternatives, all five sociology definitions and three compulsory change categories. Source gaps visible; no model answers invented.',unresolvedNumericSourceAmbiguity=AMBIGUITY))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
