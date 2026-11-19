#!/usr/bin/env python3
"""2017 Higher B: source-pinned open choices, unequal ladder and linked profiles."""
from copy import deepcopy
from he_review_2017_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(8,18)}
 q={1:select(p[6],'1. Rising',include=True)[3:],2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5. Marriage'),5:select(p[8],'5. Marriage',include=True)[3:]};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('BMI of the Irish population',1)[0].strip()
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),stem,marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,part,topic,count,per,label,guidance,**extra):return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 c=judged(1,'a','0-1',4,5,'Body Mass Index',guide(8,'4 points @ 5 marks each'),questionFigureKey='home-economics-2017-hl-sb-q1-bmi',questionFigureIncludesPrompt=False)
 c['rows'][0]['contextNote']='Comment AND elaborate on variations between the original age groups within four points. All four original BMI-category models remain available; no one-per-category quota is printed. '+c['rows'][0]['contextNote']
 table=table_rows(d['scheme'][8].find_tables().tables[0],d['scheme'][8]);assert len(table)==4
 example_lists=[['Glucose','Fructose','Galactose'],['Sucrose','Lactose','Maltose'],['Starch','Pectin','Cellulose']];food_lists=[['Fruit','Honey/fruit','Digested milk'],['Table sugar','Milk','Barley'],['Potatoes, cereals','Fruit']];rows=[];groups=[]
 for i,((name,formula,example_pool,food_pool),examples_,foods) in enumerate(zip(table[1:],example_lists,food_lists),1):
  assert all(v in example_pool for v in examples_) and all(v in food_pool for v in foods)
  rows += [point(f'class-{i}',name,1),point(f'formula-{i}',formula,1,note='Chemical formula for the SAME carbohydrate class; original subscripted formula is shown in the source table.'),menu(f'examples-{i}','Examples',2,1,examples_,'Choose ANY TWO examples of this SAME carbohydrate class.'),menu(f'source-{i}','Food Source',1,1,foods,'ONE source of this SAME carbohydrate class. The complete original table preserves the example/source relationships.')]
  groups.append(dict(sourceCardId=f'he-2017-hl-sb-q1b-class-{i}',label=name,marks=5,rowIds=[f'class-{i}',f'formula-{i}',f'examples-{i}',f'source-{i}']))
 add(1,'b','0-6',15,rows,'Three classes × (name1 + formula1 + two examples1 + source1)',taskGroups=groups,figureKey='home-economics-2017-hl-sb-q1b-carbohydrates')
 c=judged(1,'c','0-6',3,5,'properties',guide(9,'3 properties @ 5 marks each'));c['rows'][0]['contextNote']='Explain THREE properties and the related use of EACH. Each complete property/use pair earns five marks; no name/explanation/use split is printed. Hydrolysis and Inversion are named without worked accounts in the original; none is invented. '+c['rows'][0]['contextNote']
 full=guide(10,'1 effect @ 4 marks, 2 effects @ 3 marks each','(e)');heads=['Obesity:','High blood pressure:','Heart disease:','Type 2 diabetes:','Dental disease:','Nutritional deficiency:'];r=menu('effects','effects',3,4,named(full,heads),'Choose ANY THREE distinct effects from the complete original pool. The first credited effect earns4, the next3, the next3; no fixed effect receives the four-mark award. Original 2017 scientific wording retained.');r['group']['perOptionSteps']=[4,3,3];r['marks']=10;add(1,'d','0-1',10,[r],'Three effects:4+3+3')
 full=guide(10,'(1 strategy purchasing, 1 strategy preparation + 3 others)');purchase,preparing=named(full,['Purchasing:','Preparing:']);add(1,'e','0-1',20,[criterion('purchase','Purchasing',1,[0,4],purchase),criterion('prepare','Preparing',1,[0,4],preparing),criterion('other','3 others',3,[0,4],'Three ADDITIONAL strategies from either required heading. '+full)],'Purchasing4 + preparing4 + three others4')
 full=guide(11,'(2 references to nutritional value; 2 references to dietetic contribution + 1 other)','(b)');nutrition,diet=named(full,['Nutritional value:','Dietetic contribution:']);add(2,'a','0-9',20,[criterion('nutrition','nutritional value',2,[0,4],nutrition),criterion('diet','dietetic contribution',2,[0,4],diet),criterion('other','1 other',1,[0,4],'One ADDITIONAL point from either required heading. '+full)],'Nutrition2×4 + dietetic2×4 + one other4')
 full=guide(11,'Stages of production:',include=True);production,packaging,labelling=named(full,['Stages of production:','Packaging:','Labelling:']);add(2,'b','0-11',18,[criterion('production','stages of production',7,[0,2],production),criterion('packaging','packaging',1,[0,2],packaging),criterion('labelling','labelling',1,[0,2],labelling)],'Seven production stages2 + packaging2 + labelling2')
 judged(2,'c','0-10',4,3,'artisan producers / small businesses',guide(12,'4 points @ 3 marks each'))
 full=guide(13,'(1 reference to choosing, cooking, eating + 1 other)','(b)');heads=['Choosing:','Cooking:','Eating:'];add(3,'a','0-11',16,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,4],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)]+[criterion('other','1 other',1,[0,4],'One ADDITIONAL point from any of the three required headings. '+full)],'Choosing4 + cooking4 + eating4 + other4')
 judged(3,'b','0-11',4,4,'conditions',guide(13,'4 conditions @ 4 marks each','(c)'))
 grid=table_rows(d['scheme'][13].find_tables().tables[0],d['scheme'][13]);assert len(grid)==5;models=guide(14,'Simple difference paired comparison test:',include=True);heads=['Simple difference paired comparison test:','Directional paired comparison test:','Triangle test:','Duo-trio test:'];variants=[]
 for i,((name,aim),detail) in enumerate(zip(grid[1:],named(models,heads)),1):variants.append(dict(id=f'test-{i}',label=name,rows=[point('name',name,3),point('aim',aim,3,note='Aim of the SAME selected difference test.'),criterion('implementation','Implementation',6,[0,2],'Six implementation points for the SAME difference test. '+detail)]))
 variants.append(dict(id='other-test',label='Another valid difference test',rows=[criterion('name','Name',1,[0,3],'Choose ONE difference test consistently; all four original models remain available.'),criterion('aim','Aim',1,[0,3],'Aim of the SAME selected test; no additional source model is printed.'),criterion('implementation','Implementation',6,[0,2],'Six implementation points for the SAME selected test; no additional source model is printed.')]))
 add(3,'c','0-11',18,deepcopy(variants[0]['rows']),'Name3 + aim3 + implementation6×2',answerVariants=variants)
 heads=['Socio-economic factors:','Availability of housing –','National housing policy:'];full=guide(15,'Socio-economic factors:','(b)',True);add(4,'a','3-3',18,[criterion(f'heading-{i}',head.rstrip(':–').strip(),2,[0,3],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)],'Three required headings×two factors3')
 c=judged(4,'b','1-1',4,4,'mortgage approval',guide(15,'4 conditions @ 4 marks each','(c)'));c['rows'][0]['contextNote']='Historical 2017 mortgage rules and original amounts apply to this source task. '+c['rows'][0]['contextNote']
 full=guide(15,'Name: 4 marks; Description: 3 points @ 4 marks each')+' '+s[16];heads=['Annuity / Repayment Mortgage:','Endowment:','Pension linked:','Local authority mortgage / Home Choice Loan:'];described=full.split('Tracker;',1)[0];variants=[]
 for i,(name,detail) in enumerate(zip(heads,named(described,heads)),1):variants.append(dict(id=f'mortgage-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),4),criterion('description','Description',3,[0,4],'Three details of the SAME mortgage. Original historical 2017 conditions and figures retained. '+detail)]))
 for i,name in enumerate(semis(select(full,'Tracker;',include=True))+['Another valid mortgage'],1):
  note='The original scheme names Tracker, Current account / Offset mortgage and Deferred start / Interest only mortgage without description models. No model is invented. Describe the SAME selected mortgage.'
  variants.append(dict(id=f'other-{i}',label=name,rows=[criterion('name','Name',1,[0,4],note) if name=='Another valid mortgage' else point('name',name,4,note=note),criterion('description','Description',3,[0,4],note)]))
 add(4,'c','1-1',16,deepcopy(variants[0]['rows']),'Name4 + three description points4',answerVariants=variants)
 judged(5,'a','2-1',4,4,'variations',guide(17,'4 points @ 4 marks each','(b)'))
 judged(5,'b','2-1',4,4,'benefits',guide(17,'4 benefits @ 4 marks each','(c)'))
 heads=['Marriage counselling:','Family mediation:','Legal separation:'];full=guide(17,'Marriage counselling:',include=True);add(5,'c','2-1',18,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,3],'Historical 2017 source account. '+body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)],'Three required options×two points3')
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=17,marks=280,selectionDecisions='Complete original BMI/carbohydrate inputs, descending4/3/3 sugar-effect awards, required/flexible heading quotas, full four sensory-test models and all described/name-only mortgage alternatives. Historical source guidance and all continuations retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
