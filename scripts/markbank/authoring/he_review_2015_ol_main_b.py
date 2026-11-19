#!/usr/bin/env python3
"""2015 Ordinary B: full original choices and independently reconciled tariffs."""
from copy import deepcopy
from he_review_2015_ol_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(7,13)}
 q={1:select(p[6],'1. ‘Iron',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part,roman=None):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0];v=re.sub(r'\s+and\s*$','',v)
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,roman=None,keySuffix='',**extra):
  c=card(f'sb-q{n}{part}{roman or ""}{keySuffix}','B',f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,prompt(n,part,roman),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if keySuffix:c['questionRef']+=' — '+keySuffix.lstrip('-')
  if n==1:c['stem']=q[n].split('The table below',1)[0].strip()
  if roman:
   lead=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None).split('(i)',1)[0].strip();c['questionText']=(lead+' '+c['questionText']).strip()
  cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','0-8',2,4,'points',guide(7,'2 points @ 4 marks each','(b)'))
 judged(1,'b','0-9',4,6,'points',guide(7,'4 points @ 6 marks each','(c)'),questionFigureKey='home-economics-2015-ol-sb-q1-meats',questionFigureIncludesPrompt=False)
 add(1,'c','0-8',24,[criterion('sources','dietary sources',3,[0,4],guide(7,'3 sources @ 4 marks each','• functions')),criterion('functions','functions in the body',2,[0,4],guide(7,'2 functions @ 4 marks')),criterion('deficiency','effect of deficiency',1,[0,4],guide(8,'1 effect @ 4 marks','(ii)'))],'Sources12 + functions8 + deficiency4',roman='i')
 add(1,'c','0-8',4,[point('nutrient',guide(8,'1 nutrient @ 4 marks','(d)'),4)],'1 nutrient × 4',roman='ii')
 full=guide(8,'(1 reference to fresh meat, 1 reference to meat products + 2 others)');add(1,'d','1-2',20,[criterion('fresh','fresh meat',1,[0,5],'One reference to fresh meat. Original shared guidance: '+full),criterion('products','meat products',1,[0,5],'One reference to meat products. Original shared guidance: '+full),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points across either heading, with no fixed two-per-heading quota. Original source: '+full)],'Fresh meat5 + meat products5 + two others×5')
 judged(2,'a','0-1',2,5,'causes',guide(9,'2 causes @ 5 marks each','2 health risks @ 5 marks each'),roman='i')
 judged(2,'a','0-1',2,5,'health risks',guide(9,'2 health risks @ 5 marks each','(b)'),roman='ii')
 heads=['Breakfast','Lunch','Dinner'];add(2,'b','0-10',18,[criterion(f'meal-{i}',head,1,[0,6],'One meal in the SAME day for the specified person. Original model: '+body) for i,(head,body) in enumerate(zip(heads,named(guide(9,'3 menus (meals) @ 6 marks each','(c)'),heads)),1)],'3 meals × 6')
 judged(2,'c','0-1',3,4,'changes',guide(9,'3 points @ 4 marks each'))
 full=guide(10,'(1 reference to nutritional value, 1 reference to dietetic value, + 2 others)','(b)');add(3,'a','0-9',24,[criterion('nutrition','nutritional value',1,[0,6],'One nutritional point. Complete original source: '+full),criterion('dietetic','dietetic value',1,[0,6],'One dietetic point. Complete original source: '+full),criterion('other','2 others',2,[0,6],'Two ADDITIONAL points across either heading; the printed romans share this flexible 24 tariff, without a fabricated 12/12 split. Original source: '+full)],'Nutritional6 + dietetic6 + two others×6')
 methods=guide(10,'3 methods @ 4 marks each','2 points @ 4 marks each');options=chosen(methods,['Baking','grilling','roasting','frying - shallow','deep frying','stir frying','steaming','microwave cooking','poaching','stewing/casserole cooking','barbecuing'])
 c=add(3,'b','0-3',12,[menu('methods','methods',3,4,options,'Name THREE different methods; the separate explanation must use ONE of these named methods.')],'3 methods × 4',keySuffix='-methods');c['questionText']=prompt(3,'b').split(' and explain how ',1)[0]
 full=guide(10,'Cooking method:','(c)');heads=['Baking:','Barbecuing:','Grilling:','Roasting:','Steaming:','Microwave:','Poaching:','Stewing/Casserole:','Frying:'];variants=[]
 for i,(head,body) in enumerate(zip(heads,named(full,heads)),1):variants.append(dict(id=f'method-{i}',label=head[:-1],rows=[criterion('explanation','Cooking method',2,[0,4],'Explain ONE of the THREE methods named in the preceding task. No additional naming marks here. Original model for the SAME chosen method: '+body)]))
 variants.append(dict(id='other-valid-method',label='Another valid cooking method',rows=[criterion('explanation','Cooking method',2,[0,4],'Explain ONE of the THREE methods named in the preceding task. Original open list; no unprinted method-specific model is invented. Source criteria: '+prompt(3,'b'))]))
 c=add(3,'b','0-3',8,deepcopy(variants[0]['rows']),'2 explanation points × 4',keySuffix='-explanation',answerVariants=variants);c['questionText']='explain how '+prompt(3,'b').split(' and explain how ',1)[1];c['stem']+='\n\n'+prompt(3,'b')
 judged(3,'c','0-7',1,6,'benefit',guide(10,'1 point @ 6 marks'))
 types=guide(11,'Type:','1 reason @ 4 marks');reasons=guide(11,'1 reason @ 4 marks','factors to be considered');factors=guide(11,'3 factors @ 3 marks each','guidelines for use');uses=guide(11,'3 guidelines @ 3 marks each','(b)')
 add(4,'a','1-3',26,[menu('type','type',1,4,semis(types),'Choose ONE small electrical household appliance.'),criterion('reason','reason',1,[0,4],'One reason matching the SAME chosen appliance. All original model choices: '+reasons),criterion('factors','factors',3,[0,3],'Three factors for the SAME appliance. Original source: '+factors),criterion('use','guidelines',3,[0,3],'Three use guidelines for the SAME appliance. Original source: '+uses)],'Type4 + reason4 + factors3×3 + guidelines3×3')
 full=guide(11,'1 method @ 6 marks, 1 point @ 6 marks','(c)');heads=['Cash:','Cheque:','Debit card (Laser Card):','Credit card:','On line banking/Paypal:'];variants=[]
 for i,(head,body) in enumerate(zip(heads,named(full,heads)),1):variants.append(dict(id=f'payment-{i}',label=head[:-1],rows=[point('method',head[:-1],6),criterion('suitability','point',1,[0,6],'Suitability of the SAME chosen method. Original historical 2015 model: '+body)]))
 variants.append(dict(id='other-valid-payment',label='Another valid payment method',rows=[criterion('method','method',1,[0,6],'One other valid method under the original open list.'),criterion('suitability','point',1,[0,6],'Explain suitability of the SAME chosen method. No unprinted model is invented.')]))
 add(4,'b','1-1',12,deepcopy(variants[0]['rows']),'Method6 + suitability6',answerVariants=variants)
 judged(4,'c','1-2',3,4,'procedure',guide(11,'3 points @ 4 marks'))
 heads=['Physical:','Emotional:','Educational:','Socialisation:'];add(5,'a','2-0',28,[criterion(f'function-{i}',head[:-1],1,[0,7],body) for i,(head,body) in enumerate(zip(heads,named(guide(12,'4 functions @ 7 marks each','(b)'),heads)),1)],'4 required functions × 7')
 judged(5,'b','2-0',2,6,'ways',guide(12,'2 ways @ 6 marks each','(c)'))
 judged(5,'c','2-0',2,5,'communication',guide(12,'2 points @ 5 marks each'))
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=19,marks=280,selectionDecisions='Separate iron24/4, obesity10/10 and fish cooking12/8 tariffs. Fish nutrition/diet24 retains one-each-plus-two-others. All original cooking-method models, three menu meals, six appliances, five payment models and four required family functions retained. Linked explanation context and historical source terms render.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
