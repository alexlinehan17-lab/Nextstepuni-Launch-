#!/usr/bin/env python3
"""2010 Higher B: exact printed tariffs; full source contexts and answer pools."""
import json,re,sys
from copy import deepcopy
from he_review_2010_hl_main import *

def build():
 d=documents();p={n:text(d['paper'],n) for n in [6,7,8]};s={n:text(d['scheme'],n) for n in range(7,13)}
 q={1:p[6].split('1.',1)[1],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('Breakdown of',1)[0].strip()
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def simple(n,part,topic,count,per,guidance,options=None,**extra):
  rows=[menu('answers','Published answer points',count,per,options or semis(guidance),'Only the printed full-credit point value is offered; the scheme gives no finer ladder.')]
  return add(n,part,topic,count*per,rows,f'{count} points @ {per} marks each',**extra)
 # B1: independent 20/4 tasks inside (a), as explicitly priced on scheme pp7–8.
 sectors=named(guide(7,'(20)'),['Dairy products –','Beef –','Prepared foods –','Beverages –','Seafood –','Pig meat –','Other –'])
 c=add(1,'a','0-11',20,[menu('sectors','Four sectors',4,5,sectors,'Comment and elaborate on four different sectors using the original graph.')],'4 points @ 5 marks each',questionFigureKey='home-economics-2010-hl-sb-q1-exports',questionFigureIncludesPrompt=False)
 c.update(id='he-2010-hl-sb-q1ai',questionRef='2010 HL Section B Q1(a)(i)',questionText=select(prompt(1,'a'),'(i)','(ii)'))
 careers=guide(8,'(4)','(b)');opts=[v.strip() for v in re.sub(r'\s*etc\.?$','',careers).split(',')]
 c=add(1,'a','0-11',4,[menu('careers','Career opportunities',2,2,opts,'Two source points within one chosen sector; retain the paper’s sector context.')],'2 points @ 2 marks each',questionFigureKey='home-economics-2010-hl-sb-q1-exports',questionFigureIncludesPrompt=False)
 c.update(id='he-2010-hl-sb-q1aii',questionRef='2010 HL Section B Q1(a)(ii)',questionText=select(prompt(1,'a'),'(ii)'))
 iron=guide(8,'(21)','(c)');sources=select(iron,'Sources','Functions');functions=select(iron,'Functions','RDA adults');rda=select(iron,'RDA adults',include=True)
 source_options=[v.strip() for v in re.split(r',|\betc\.?',sources) if v.strip()];source_options=[re.sub(r'^Non-haem iron in ','',v) if i else v for i,v in enumerate(source_options)]
 add(1,'b','0-8',21,[menu('sources','Sources',3,3,source_options),menu('functions','Functions',3,3,semis(functions)),point('rda',rda,3,'Historical source RDA, as printed in the 2010 scheme.')],'3 sources × 3 + 3 functions × 3 + RDA 3')
 absorption=guide(8,'3 points @ 5 marks each','(d)');assist,decrease=named(absorption,['Factors that assist iron absorption','Factors that decrease iron absorption']);opts=semis(assist.split('absorption',1)[1])+semis(decrease.split('absorption',1)[1]);simple(1,'c','0-8',3,5,absorption,opts)
 factors=guide(8,'4 points @ 5 marks each');simple(1,'d','0-9',4,5,factors,named(factors,['Financial –','Convenience –','Environmental –','Health –','Flavour –','Trace ability –','Advertising –','Meat products –']))
 # B2(a) requires at least two of each type, with the fifth from either type.
 fish=guide(9,'(Expect two nutritional and two dietetic and one other point)','(b)');nut=semis(select(fish,'Nutritional','Dietetic'));diet=semis(select(fish,'Dietetic'))
 def fish_rows(nn,nd):return [menu('nutritional','Nutritional',nn,4,nut),menu('dietetic','Dietetic',nd,4,diet)]
 c=add(2,'a','0-9',20,fish_rows(3,2),'5 points @ 4; at least two nutritional and two dietetic')
 c['answerVariants']=[dict(id='nutritional-three',label='Three nutritional + two dietetic',rows=fish_rows(3,2)),dict(id='dietetic-three',label='Two nutritional + three dietetic',rows=fish_rows(2,3))]
 cooking=guide(9,'(method- 2 marks; principle- 2 points @ 3 marks each, palatability- 2 marks) x 2','(c)');dry=select(cooking,'Dry Methods','Moist Methods');moist=select(cooking,'Moist Methods');rows=[];groups=[]
 for key,label,body,methods in [('dry','Dry Methods',dry,['Baking','Grilling / Barbecuing','Roasting','Smoking','Microwave cooking']),('moist','Moist Methods',moist,['Poaching','Steaming','Stewing','Braising','Microwave cooking'])]:
  names=[]
  for word in methods:
   source=cooking if word=='Microwave cooking' else body
   assert word in source;names.append(select(source,word,include=True)[:len(word)])
  rows += [menu(key+'-name',label,1,2,names),criterion(key+'-principle','principle',2,[0,3],'Two principles for the SAME method. Full source guidance: '+body),criterion(key+'-palatability','palatability',1,[0,2],'Comment on the SAME cooked fish. Full source guidance: '+body)]
  groups.append(dict(sourceCardId=f'he-2010-hl-sb-q2b-{key}',label=label,marks=10,rowIds=[key+'-name',key+'-principle',key+'-palatability']))
 add(2,'b','0-3',20,rows,'(method 2 + principle 2 × 3 + palatability 2) × 2',taskGroups=groups)
 simple(2,'c','0-10',2,5,guide(9,'2 points @ 5 marks each'))
 # B3(a) remains one comparative evaluation with one food and two methods.
 preservation=guide(10,'(26)','(b)');method_names=[]
 for name in ['Freezing','Bottling/canning','Dehydration','Chemical','Irradiation','Pasteurisation','UHT','Sterilisation','Freeze-drying']:
  assert name in preservation;method_names.append(select(preservation,name,include=True)[:len(name)])
 add(3,'a','0-3',26,[criterion('food','name of food',1,[0,2],'The printed tariff names a food but supplies no model food; no example has been invented.'),menu('methods','suitable methods of preservation',2,3,method_names),criterion('principle-1','the underlying principle of each method',2,[0,3],'Two points for the first chosen method. Complete source guidance: '+preservation),criterion('principle-2','the underlying principle of each method',2,[0,3],'Two points for the second chosen method. Complete source guidance: '+preservation),criterion('spoilage','risk of food spoilage.',2,[0,3],'Two risk points across the chosen methods. Complete source guidance: '+preservation)],'Food 2 + methods 2 × 3 + principles 4 × 3 + spoilage 2 × 3')
 plastics=guide(10,'(16)','(c)');types=select(plastics,'Types –','Suitability for purpose –');purpose=select(plastics,'Suitability for purpose –','Environmental impact –');impact=select(plastics,'Environmental impact –')
 purpose_options=[v.strip() for v in purpose.replace('weights, thickness','weights\u0001 thickness').split(',')]
 purpose_options=[v.replace('\u0001',',') for v in purpose_options]
 add(3,'b','0-11',16,[menu('types','Types',2,2,[v.strip() for v in types.split(',')]),menu('suitability','Suitability for purpose',2,3,purpose_options),criterion('impact','Environmental impact',2,[0,3],'Two distinct points. Complete source guidance: '+impact)],'Types 2 × 2 + suitability 2 × 3 + environmental impact 2 × 3')
 simple(3,'c','1-2',2,4,guide(10,'2 points @ 4 marks each'))
 budget=guide(11,'5 points @ 4 marks each','(b)');options=named(budget,['List all sources of net income.','List planned expenditure','Calculate weekly/monthly expenditure','allow for discretionary spending','account for some possible changes in circumstances','incorporate long term and short term savings','allocate some money for personal expenses','keep copies of bills and receipts','evaluate and review budgets regularly'])
 simple(4,'a','1-1',5,4,budget,options)
 savings=guide(11,'4 points @ 5 marks each','(c)');options=named(savings,['Security of savings –','Interest payable –','Access to funds –','Tax payable –']);add(4,'b','1-1',20,[point(f'factor-{i}',v,5,'This is the 2010 scheme’s historical financial context.') for i,v in enumerate(options,1)],'4 required points @ 5 marks each')
 simple(4,'c','1-1',2,5,guide(11,'2 points @ 5 marks each'))
 family=guide(12,'4 points @ 6 marks each','(b)');functions=select(family,'Nurturing, rearing, emotional function','How the State supports the family:',True);support=select(family,'How the State supports the family:');fo=named(functions,['Nurturing, rearing, emotional function','Economic function','Education/Intellectual function','Socialisation','Protective/ Physical function']);so=named(support,['Emotional -','Economic -','Educational-','Social function -','Protective / Physical function -'])
 add(5,'a','2-0',24,[menu('functions','Family function and matching State support',4,6,[a+' — '+b for a,b in zip(fo,so)],'Each six-mark point includes the family function AND corresponding State support; no separate price for either half is printed.')],'4 points @ 6 marks each')
 simple(5,'b','2-1',3,4,guide(12,'3 points @ 4 marks each','(c)'))
 why=guide(12,'Why it is important','5 points @ 2 marks each');procedure=guide(12,'Procedure');whole=prompt(5,'c');assert ' and outline the procedure involved.' in whole
 c=add(5,'c','2-1',4,[menu('importance','Why it is important',2,2,semis(why))],'2 points @ 2 marks each');c.update(id='he-2010-hl-sb-q5c-importance',questionRef='2010 HL Section B Q5(c) — importance',questionText=whole.split(' and outline the procedure involved.',1)[0])
 scope='The original combined prompt is retained as context. This independently priced task asks only for the procedure: five points at two marks each; importance is the companion four-mark card.'
 c=add(5,'c','2-1',10,[menu('procedure','Procedure',5,2,semis(procedure),scope)],'5 points @ 2 marks each');c.update(id='he-2010-hl-sb-q5c-procedure',questionRef='2010 HL Section B Q5(c) — procedure',questionText=whole.split(' and ',1)[1],stem=whole)
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 c=build()
 if '--write' in sys.argv:write_section('B',c,dict(tasks=18,marks=280,selectionDecisions='B1(a)20/4 and B5(c)4/10 are separate published task boundaries. Required cooking profiles, preservation comparison, family/support pairs and fish nutritional/dietetic quotas remain whole. Only published per-point values, no inferred partial ladders.'))
 else:print(json.dumps(c,ensure_ascii=False,indent=2))
