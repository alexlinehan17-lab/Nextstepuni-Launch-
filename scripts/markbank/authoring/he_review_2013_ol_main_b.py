#!/usr/bin/env python3
"""2013 Ordinary B: original source accounts, separate actions and exact tariffs."""
from he_review_2013_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,14)}
 q={1:select(p[6],'1. Following',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,suffix='',**extra):
  c=card(f'sb-q{n}{part}{roman or ""}{suffix}','B',f'Q{n}({part})'+(f'({roman})' if roman else '')+(' — '+suffix[1:] if suffix else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if roman:
   lead=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None).split('(i)',1)[0].strip();c['questionText']=lead+' '+re.sub(r'\s+and$','',c['questionText'])
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','0-1',4,4,'healthy eating',guide(8,'4 points @ 4 marks each','(b)'),questionFigureKey='home-economics-2013-ol-sb-q1-pyramid',questionFigureIncludesPrompt=False)
 composition=guide(8,'4 elements @ 1 mark each');classes=guide(9,'2 classes @ 4 marks each','• dietary sources');sources=guide(9,'4 sources @ 3 marks each','• functions');functions=guide(9,'2 functions @ 4 marks each','(c)')
 add(1,'b','0-5',32,[menu('elements','composition',4,1,chosen(composition.split('protein only',1)[0],['carbon','hydrogen','oxygen','nitrogen']),'Four source elements. Full original composition guidance: '+composition),criterion('classes','classification',2,[0,4],classes),criterion('sources','dietary sources',4,[0,3],sources),criterion('functions','functions in the body',2,[0,4],functions)],'Four required headings: 4 + 8 + 12 + 8')
 properties=select(s[9],'(c)','(d)');bodies=named(properties,['• denaturation','• coagulation.']);rows=[];groups=[]
 for i,(name,body) in enumerate(zip(['denaturation','coagulation'],bodies),1):
  value=select(body,'explanation 3 marks, example 3 marks');meaning,example=value.split('Example:',1);rows.extend([criterion(f'explanation-{i}',name,1,[0,3],meaning),criterion(f'example-{i}','example',1,[0,3],'Example of the SAME property: '+example)]);groups.append(dict(sourceCardId=f'he-2013-ol-sb-q1c-{name}',label=name,marks=6,rowIds=[f'explanation-{i}',f'example-{i}']))
 add(1,'c','0-5',12,rows,'Two required property profiles: explanation3/example3 each',taskGroups=groups)
 judged(1,'d','0-5',4,5,'protein foods',guide(9,'4 points @ 5 marks each'))
 judged(2,'a','0-1',3,4,'factors',guide(10,'3 factors @ 4 marks each','(b)'))
 b=prompt(2,'b');intro,rest=b.split('•',1);planning,menu_prompt=rest.split('•',1)
 c=judged(2,'b','0-10',4,3,'guidelines',guide(10,'4 guidelines @ 3 marks each','• a menu'),suffix='-guidelines');c['questionText']=intro.strip()+' '+planning.strip().removesuffix('and').strip()
 meal=guide(10,'3 meals @ 6 marks each to include snacks','(c)');meal_parts=named(meal,['Breakfast','Lunch','Dinner']);c=add(2,'b','0-10',18,[criterion(f'meal-{i}',name,1,[0,6],'One coherent HIGH-ENERGY day: include snacks with the three meals, as the source requires. No separate snack allocation is printed. Original meal/snack example: '+body) for i,(name,body) in enumerate(zip(['Breakfast','Lunch','Dinner'],meal_parts),1)],'Three meals × 6, to include snacks',suffix='-menu');c['questionText']=intro.strip()+' '+menu_prompt.strip()
 judged(2,'c','0-8',2,4,'food supplements',guide(10,'2 points @ 4 marks each'))
 judged(3,'a','1-3',4,4,'factors',guide(11,'4 points @ 4 marks each','(b)'))
 description=guide(11,'description = 2 marks','• modern features');modern=guide(11,'3 modern features @ 3 marks each','• guidelines').replace('\uf0fb','°');use=guide(11,'3 guidelines @ 3 marks each','• energy');energy=guide(11,'1 point @ 4 marks','(c)')
 add(3,'b','1-3',24,[criterion('description','description',1,[0,2],'Describe the SAME refrigeration appliance used throughout this profile. Source examples: '+description),criterion('features','modern features',3,[0,3],'For the SAME appliance: '+modern),criterion('use','guidelines for use',3,[0,3],'For the SAME appliance: '+use),criterion('energy','energy efficiency rating',1,[0,4],'Original 2013 energy-label guidance for the SAME appliance: '+energy)],'Description2 + features9 + use9 + rating4')
 heads=['Advantages –','Disadvantages –'];add(3,'c','1-1',10,[criterion(f'side-{i}',head.rstrip(' –'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(11,'(1 advantage, 1 disadvantage)'),heads)),1)],'One advantage5 and one disadvantage5')
 judged(4,'a','1-2',2,5,'money back',guide(12,'2 points @ 5 marks each','(b)'))
 judged(4,'b','1-2',3,4,'procedure',guide(12,'3 points @ 4 marks each','(c)'))
 c=judged(4,'c','1-2',4,4,'rights',guide(12,'4 rights @ 4 marks each','(d)'));c['rows'][0]['contextNote']='Name AND explain four rights. The original source lists rights and gives a safety example, but does not print a model explanation for every right; no missing explanations have been invented. '+c['rows'][0]['contextNote']
 judged(4,'d','1-5',3,4,'environment',guide(12,'3 ways @ 4 marks each'))
 heads=['nuclear family:','extended family:','blended family:'];add(5,'a','2-0',15,[criterion(f'family-{i}',head[:-1],1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(13,'3 points @ 5 marks each','(b)'),heads)),1)],'Three required family structures × 5')
 b=select(s[13],'(b)','(c)');first,second=b.split('(ii)',1);judged(5,'b','2-3',2,5,'independence',re.sub(r'\s+and$','',select(first,'2 points @ 5 marks each')),roman='i');judged(5,'b','2-3',2,5,'state supports',select(second,'2 points @ 5 marks each'),roman='ii')
 ctext=prompt(5,'c');meaning,ways=ctext.split(' and state ',1);c=add(5,'c','2-0',5,[criterion('explanation','generation conflict',1,[0,5],guide(13,'explanation:','2 ways @ 5 marks each'))],'Explanation5',suffix='-definition');c['questionText']=meaning.strip()+'.'
 c=judged(5,'c','2-0',2,5,'dealing with conflict',guide(13,'dealing with conflict:'),suffix='-ways');c['stem']+='\n\n'+meaning.strip()+'.';c['questionText']='State '+ways.strip()
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=20,marks=280,selectionDecisions='Independent planning/menu12/18 and conflict explanation/ways5/10 split. Protein account32 and linked property/example profiles12 stay coherent. Required/flexible source quotas, complete profiles and original missing-rights explanations visible.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
