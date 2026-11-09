#!/usr/bin/env python3
"""2018 Higher B: original paired alternatives and required additive accounts."""
from copy import deepcopy
from he_review_2018_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,17)}
 q={1:select(p[6],'1. Calorie',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('Sample Main Course Menu',1)[0].strip()
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 c=judged(1,'a','0-1',4,6,'suitability',guide(8,'4 points @ 6 marks each'),questionFigureKey='home-economics-2018-hl-sb-q1-menu',questionFigureIncludesPrompt=False)
 c['rows'][0]['contextNote']='Comment AND elaborate on suitability and suggest modifications across four points. The source sets no separate suitability/modification quota. '+c['rows'][0]['contextNote']
 full=guide(9,'Elemental composition','(c)');elements=select(full,'Carbon(C);','Structure',True);structure=select(full,'Made up of',include=True);add(1,'b','0-7',9,[menu('elements','Elemental composition',3,1,semis(elements),'State all THREE original elements.'),criterion('structure','Structure',3,[0,2],structure)],'Three elements1 + three structure points2')
 full=guide(9,'3 points @ 6 marks each','(d)');heads=['Saturated fatty acids:','Monounsaturated fatty acids:','Polyunsaturated fatty acids (PUFA’s):'];rows=[]
 for i,(head,model) in enumerate(zip(heads,named(full,heads)),1):rows.append(criterion(f'class-{i}',head.rstrip(':'),1,[0,6],'Describe the structure AND give ONE matching example for this required class. The source awards six to the complete account without an internal split. '+model))
 add(1,'c','0-7',18,rows,'Three required structure/example accounts6')
 judged(1,'d','0-7',3,3,'significance',guide(9,'3 points @ 3 marks each'))
 judged(1,'e','0-11',5,4,'reasons',guide(10,'5 points @ 4 marks each'))
 classes=guide(11,'Vegan:','specific dietary requirements: 4 points',True);diet=guide(11,'Each meal','benefits of a vegetarian diet:',True);benefits=guide(11,'Healthier','(b)',True)
 add(2,'a','0-1',30,[criterion('classes','classes / types',3,[0,3],classes),criterion('diet','specific dietary requirements',4,[0,3],diet),criterion('benefits','benefits of a vegetarian diet',3,[0,3],benefits)],'Three classes3 + four requirements3 + three benefits3')
 full=guide(11,'Tofu:',include=True);heads=['Tofu:','Soya milk:','Soya yoghurt:','Tempeh:','Textured Vegetable Protein:','Miso:','Quorn:'];models=named(full.split('Accept:',1)[0],heads)
 add(2,'b','0-5',8,[menu('names','Name',2,2,[h.rstrip(':') for h in heads]+['soya products'],'Choose ANY TWO different novel protein foods from the complete original pool.'),criterion('descriptions','Description',2,[0,2],'Give ONE description for EACH of the SAME TWO selected foods; keep name and description matched. Complete paired source models: '+' '.join(models)+' Accept: soya products. No description model is printed for this broader accepted category.')],'Two names2 + two matching descriptions2')
 full=guide(12,'TVP:',include=True);variants=[]
 for i,(head,model) in enumerate(zip(['TVP:','Mycoprotein:'],named(full,['TVP:','Mycoprotein:'])),1):variants.append(dict(id=f'food-{i}',label=head.rstrip(':'),rows=[point('name',head.rstrip(':'),2),criterion('production','Details',5,[0,2],'Five manufacture/production points for this SAME named food. '+model)]))
 variants.append(dict(id='other-food',label='Another valid novel protein food',rows=[criterion('name','Name',1,[0,2],'Name ONE novel protein food. The original scheme supplies TVP and mycoprotein models; no additional model has been invented.'),criterion('production','Details',5,[0,2],'Five manufacture/production points for the SAME named food; no additional source model is printed.')]))
 add(2,'c','0-5',12,deepcopy(variants[0]['rows']),'Name2 + five production points2',answerVariants=variants)
 add(3,'a','0-11',20,[criterion('definition','processed food',1,[0,4],guide(13,'A processed food','Evaluate the merits',True)),criterion('merits','Merits',4,[0,4],guide(13,'Merits:','(b)',True))],'Definition4 + four merits4')
 rows=[];groups=[]
 for i,(pn,label) in enumerate([(13,'Flavourings'),(14,'Antioxidants')],1):
  grid=table_rows(d['scheme'][pn-1].find_tables().tables[0],d['scheme'][pn-1]);paired=[];current=''
  for name,example,use,function in grid[1:]:
   if name:current=name
   paired.append(current+' — Examples: '+example+' Uses: '+use+(' Functions: '+function if function else ''))
  full='Complete original class/example/use/function relationships: '+' | '.join(paired)
  if pn==13:full+=' '+guide(13,'Accept:',include=True)
  ids=[]
  for key,count,per in [('classes',2,1),('examples',2,1),('uses',2,1),('functions',2,2)]:
   rid=f'additive-{i}-{key}';ids.append(rid);rows.append(criterion(rid,key,count,[0,per],f'For {label}, give ANY TWO {key}; keep examples and uses matched to the selected classes. '+('The three printed flavouring classes Natural, Artificial and Flavour Enhancers remain available; do not force Natural/Artificial. ' if pn==13 else '')+full))
  groups.append(dict(sourceCardId=f'he-2018-hl-sb-q3b-additive-{i}',label=label,marks=10,rowIds=ids))
 add(3,'b','0-11',20,rows,'BOTH additives: two classes1 + examples1 + uses1 + functions2',taskGroups=groups)
 judged(3,'c','0-11',2,5,'regulated',guide(14,'2 points @ 5 marks each'))
 judged(4,'a','1-3',5,4,'technology',guide(15,'5 points @ 4 marks each','(b)'))
 heads=['Working principle:','Guidelines for use:','Modern features:'];full=guide(15,'Working principle:','(c)',True);add(4,'b','1-3',22,[criterion(f'heading-{i}',head.rstrip(':'),count,[0,per],model) for i,(head,count,per,model) in enumerate(zip(heads,[4,3,2],[3,2,2],named(full,heads)),1)],'Working principle4×3 + use3×2 + modern features2×2')
 c=judged(4,'c','1-3',2,4,'energy labelling',guide(15,'2 points @ 4 marks each'));c['rows'][0]['contextNote']='Historical 2018 energy-label wording and ratings are preserved. '+c['rows'][0]['contextNote']
 judged(5,'a','2-0',4,4,'rights',guide(16,'4 points @ 4 marks each','(b)'))
 add(5,'b','2-1',24,[criterion('causes','Causes',3,[0,4],guide(16,'Causes: high','Strategies: 3 points',True)),criterion('strategies','Strategies',3,[0,4],guide(16,'Strategies: identify','(c)',True))],'Three causes4 + three strategies4')
 c=judged(5,'c','2-1',2,5,'protection',guide(16,'2 points @ 5 marks each'));c['rows'][0]['contextNote']='Historical 2018 scheme account of the named 1976 Act. '+c['rows'][0]['contextNote']
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=17,marks=280,selectionDecisions='All six menu dishes; required fatty-acid class structure/example accounts without invented splits; complete vegetarian and novel-protein pools with matching descriptions/production; BOTH additive accounts and all three flavouring classes with original paired tables; full refrigeration cycle; combined causes/strategies and historical legal guidance.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
