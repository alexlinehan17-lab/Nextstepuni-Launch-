#!/usr/bin/env python3
"""2015 Higher B: coherent profiles, source tariffs and complete historical models."""
from copy import deepcopy
from he_review_2015_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,16)}
 q={1:select(p[6],'1. A survey',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:
   lead=v.split('(i)',1)[0].strip();v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0];v=(lead+' '+v).strip()
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,**extra):
  c=card(f'sb-q{n}{part}{roman or ""}','B',f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 full=guide(8,'(2 references to provision, 2 references to nutritional significance + 2 others)')+' '+s[9].split('(b)',1)[0];provision,nutrition=named(full,['Provision:','Nutritional Significance:'])
 add(1,'a','0-1',24,[criterion('provision','provision',2,[0,4],provision),criterion('nutrition','nutritional significance',2,[0,4],nutrition),criterion('other','2 others',2,[0,4],'Two ADDITIONAL points from either required heading, no fixed three-per-heading quota. Original complete source: '+full)],'Provision 2×4 + nutritional significance 2×4 + two others×4',questionFigureKey='home-economics-2015-hl-sb-q1-survey',questionFigureIncludesPrompt=False)
 full=guide(9,'Sources:',include=True);sources,functions,absorption=named(full,['Sources:','Biological functions:','Factors assisting absorption:'])
 add(1,'b','0-8',18,[criterion('sources','sources',3,[0,2],sources),criterion('functions','biological functions',3,[0,2],functions),criterion('absorption','factors assisting/inhibiting absorption',3,[0,2],'Choose THREE factors across both complete original assisting/inhibiting pools; no separate count for each side is printed. '+absorption)],'Sources 3×2 + functions 3×2 + absorption 3×2')
 judged(1,'c','0-1',2,3,'osteoporosis',guide(10,'2 points @ 3 marks each','(ii)'),roman='i')
 judged(1,'c','0-1',3,4,'factors',guide(10,'3 factors @ 4 marks each','(d)'),roman='ii')
 judged(1,'d','0-1',5,4,'role of parents',guide(10,'5 points @ 4 marks each'))
 full=guide(11,'(1 reference to nutritional significance, 1 reference to contribution to the diet + 4 others)','Properties and related culinary uses (16)');nutrition,diet=named(full,['Nutritional significance -','Contribution to the diet -'])
 rows=[criterion('nutrition','nutritional significance',1,[0,4],nutrition),criterion('diet','contribution to the diet',1,[0,4],diet),criterion('other','4 others',4,[0,4],'Four ADDITIONAL points from either of the two required headings. Original source: '+full)]
 properties=guide(11,'(Name = 2 marks, Explanation = 4 marks, Culinary use = 2 marks) x 2','(b)');names=chosen(properties,['Coagulation','Aeration','Emulsification']);groups=[dict(sourceCardId='he-2015-hl-sb-q2a-nutrition',label='Nutrition and contribution to the diet',marks=24,rowIds=['nutrition','diet','other'])]
 for i in [1,2]:
  rows.extend([menu(f'property-{i}','Name',1,2,names,'Choose TWO DIFFERENT egg properties across the two profiles.'),criterion(f'explanation-{i}','Explanation',1,[0,4],'Explain the SAME named property. Complete original models: '+properties),criterion(f'use-{i}','Culinary use',1,[0,2],'Give one culinary use matching the SAME named property. Complete original models: '+properties)])
  groups.append(dict(sourceCardId=f'he-2015-hl-sb-q2a-property-{i}',label=f'Egg property {i}',marks=8,rowIds=[f'property-{i}',f'explanation-{i}',f'use-{i}']))
 add(2,'a','0-9',40,rows,'Nutrition/diet 6×4 + two property profiles × (name2/explanation4/use2)',taskGroups=groups)
 judged(2,'b','0-4',2,5,'quality',guide(11,'2 points @ 5 marks each'))
 judged(3,'a','0-4',4,4,'conditions',guide(12,'4 conditions @ 4 marks each','(b)'))
 grid=table_rows(d['scheme'][11].find_tables().tables[0],d['scheme'][11]);assert len(grid)==5,grid;general=guide(12,'Asexual reproduction:','(c)',True);asexual,sexual=named(general,['Asexual reproduction:','Sexual reproduction:']);variants=[]
 for i,(name,character,reproduction) in enumerate(grid[1:],1):
  detail=asexual+(' '+sexual if name in ['Mucor','Rhizopus'] else '')
  rows=[point('name',name,4,note='Use this SAME mould throughout the profile. Original spelling retained.'),criterion('characteristics','Description/Characteristics',2,[0,3],character),criterion('reproduction','Reproduction',4,[0,3],'Four reproduction points for this SAME mould using only the method(s) in its original row. Source row: '+reproduction+' Complete applicable source: '+detail)]
  variants.append(dict(id=f'source-{i}',label=name,rows=rows))
 variants.append(dict(id='another-mould',label='Another valid mould',rows=[criterion('name','name',1,[0,4],'One valid mould, used consistently. Four original named models remain available.'),criterion('characteristics','description/characteristics',2,[0,3],'Two matching characteristics. No additional source model is supplied.'),criterion('reproduction','reproduction',4,[0,3],'Four points using the method(s) applicable to the SAME chosen mould. The original general accounts are: '+general)]))
 add(3,'b','0-4',22,deepcopy(variants[0]['rows']),'Name4 + characteristics2×3 + reproduction4×3',answerVariants=variants,figureKey='home-economics-2015-hl-sb-q3b-moulds')
 judged(3,'c','0-11',3,4,'uses',guide(12,'3 uses @ 4 marks each'))
 judged(4,'a','1-1',3,6,'factors',guide(13,'3 factors @ 6 marks each','(b)'))
 grid=table_rows(d['scheme'][12].find_tables().tables[0],d['scheme'][12]);assert len(grid)==11,grid;model='Original complete budget: '+'; '.join(' | '.join(r) for r in grid);rows=[]
 for key in ['Housing','Food','Savings']:
  line=next(r for r in grid[1:] if r[0]==key);rows.append(criterion(key.lower(),key,1,[0,3],'Required underlined area: allocation with matching reason in the SAME €650 family budget. Source model: '+' | '.join(line)))
 rows.append(criterion('other','3 others',3,[0,3],'Three ADDITIONAL areas, each with an allocation and reason in the SAME budget; the source does not separately price amounts and reasons. '+model))
 add(4,'b','1-1',18,rows,'Required Housing/Food/Savings 3 each + three others×3',figureKey='home-economics-2015-hl-sb-q4b-budget')
 grid=table_rows(d['scheme'][13].find_tables().tables[0],d['scheme'][13]);assert len(grid)==7,grid;variants=[]
 for i,(institution,interest,access,tax) in enumerate(grid[1:],1):
  name=next(x for x in ['Post Office','Credit Union','Bank of Ireland'] if institution.startswith(x));kind=select(institution,name).rstrip(':');note='Historical 2015 original rates/conditions retained; all details must match the SAME institution and scheme.'
  rows=[point('institution',name,2,note=note),point('scheme',kind,3,note=note),criterion('interest','interest paid',1,[0,3],note+' '+interest),criterion('access','ease of access to funds',1,[0,3],note+' '+access),criterion('tax','tax payable',1,[0,3],note+' '+tax)];variants.append(dict(id=f'source-{i}',label=name+' — '+kind,rows=rows))
 variants.append(dict(id='another-scheme',label='Another valid savings scheme',rows=[criterion('institution','name of institution',1,[0,2],'Choose one institution and savings scheme consistently. Six original historical models are available.'),criterion('scheme','type of savings scheme',1,[0,3],'Name a scheme of that SAME institution. No additional source model is printed.'),criterion('interest','interest paid',1,[0,3],'State the historical interest for that SAME scheme. No additional source model is printed.'),criterion('access','ease of access to funds',1,[0,3],'State access conditions for that SAME scheme. No additional source model is printed.'),criterion('tax','tax payable',1,[0,3],'State tax treatment for that SAME scheme. No additional source model is printed.')]))
 add(4,'c','1-1',14,deepcopy(variants[0]['rows']),'Institution2 + scheme3 + interest3 + access3 + tax3',answerVariants=variants,figureKey='home-economics-2015-hl-sb-q4c-savings')
 judged(5,'a','2-1',1,5,'Definition',guide(15,'Definition: 5marks','(ii)'),roman='i')
 judged(5,'a','2-1',4,4,'requirements',guide(15,'4 requirements @ 4 marks each','(b)'),roman='ii')
 judged(5,'b','2-1',5,4,'rights and responsibilities',guide(15,'5 points @ 4 marks each','(c)'))
 judged(5,'c','2-1',3,3,'conditions',guide(15,'3 conditions @ 3 marks each'))
 for c in cards:
  if c['id'].startswith('he-2015-hl-sb-q5'):
   for row in c['rows']:row['contextNote']='Historical 2015 examination guidance and legal wording retained. '+row.get('contextNote','')
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=17,marks=280,selectionDecisions='Coherent provision/nutrition24 and egg-study40 retain required/flexible quotas. Independent osteoporosis6/12 and marriage5/16 roman asks split. Complete mould profiles and applicable reproduction accounts, required budget areas, all six historical savings models and source tables retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
