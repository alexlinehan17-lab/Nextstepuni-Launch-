#!/usr/bin/env python3
"""2011 Higher B: original source answers and printed internal allocations."""
from copy import deepcopy
from he_review_2011_hl_main import *
def build():
 d=documents();p={n:text(d['paper'],n) for n in range(6,9)};s={n:text(d['scheme'],n) for n in range(7,14)}
 q={1:select(p[6],'1.'),2:select(p[7],'2.','3.'),3:select(p[7],'3.'),4:select(p[8],'4.','5.'),5:select(p[8],'5.')};cards=[]
 def prompt(n,part):
  v=select(q[n],f'({part})',f'({chr(ord(part)+1)})' if f'({chr(ord(part)+1)})' in q[n] else None)
  return re.sub(r'\s*\(\d+\)\s*$','',v).replace('\uf0b7','•').strip()
 def add(n,part,topic,marks,rows,notation,**extra):
  c=card(f'sb-q{n}{part}','B',f'Q{n}({part})',topic,prompt(n,part),q[n].split('(a)',1)[0].strip(),marks,rows,6 if n==1 else 7 if n<=3 else 8,notation,**extra)
  if n==1:c['stem']=q[n].split('Retail Dairy Market',1)[0].strip()
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,part,topic,count,per,label,guidance,**extra):
  return add(n,part,topic,count*per,[criterion('points',label,count,[0,per],'Distinct source points at the printed value; no finer marking ladder is published. Complete source guidance: '+guidance)],f'{count} points @ {per}',**extra)
 chart=named(guide(7,'3 marks for elaboration e.g. comment on consumer consumption'),['Milk –','Yogurt –','Cheese –','Cream and Fats –']);rows=[];groups=[]
 for i,(label,percentage,body) in enumerate(zip(['Milk','Yogurts','Cheese','Cream and fats'],[39,26,18,17],chart),1):
  rows.extend([criterion(f'analysis-{i}','simple analysis of the chart',1,[0,2],f'{label}: original chart {percentage}%. This is the explicit two-mark simple-analysis component.'),criterion(f'elaboration-{i}','elaboration',1,[0,3],'Elaborate on this SAME product. Complete source guidance: '+body)])
  groups.append(dict(sourceCardId=f'he-2011-hl-sb-q1a-product-{i}',label=label,marks=5,rowIds=[f'analysis-{i}',f'elaboration-{i}']))
 add(1,'a','0-9',20,rows,'4 required products × (analysis 2 + elaboration 3)',taskGroups=groups,questionFigureKey='home-economics-2011-hl-sb-q1-dairy',questionFigureIncludesPrompt=False)
 structure=guide(8,'Structure –','x how a peptide');bond=guide(8,'Peptide bond formation =','x properties');properties=guide(8,'Properties:','(c)')
 add(1,'b','0-5',28,[criterion('structure','the structure of an amino acid',4,[0,2],structure),criterion('bond','how a peptide bond is formed',4,[0,2],bond),menu('properties','properties',4,3,[v[2:] for v in named(properties,['x Denaturation –','x Solubility –','x Maillard Reaction –','x Elasticity –','x Gel Formation –'])])],'Structure 4 × 2 + bond 4 × 2 + properties 4 × 3')
 variants=[]
 for name,process,effect in d['scheme'][7].find_tables().tables[0].extract()[1:]:
  variants.append(dict(id=name.lower(),label=name,rows=[point('name',name,2),criterion('process','how the process is carried out',3,[0,2],'Three points for the SAME selected process. Source: '+tidy(process)),criterion('effect','the effect of the process on the nutritive value of milk',2,[0,2],'Two points for this SAME process. Source: '+tidy(effect))]))
 variants.append(dict(id='another-process',label='Another valid process',rows=[criterion('name','name of process',1,[0,2],'The question allows a process of choice. The source provides six examples; no extra model has been invented.'),criterion('process','how the process is carried out',3,[0,2],'Three points for the same valid process, at the printed two marks each.'),criterion('effect','the effect of the process on the nutritive value of milk',2,[0,2],'Two points for the same process, at the printed two marks each.')]))
 add(1,'c','0-3',12,deepcopy(variants[0]['rows']),'Name 2 + process 3 × 2 + effects 2 × 2',answerVariants=variants)
 business=guide(9,'5 points @ 4 marks each');add(1,'d','0-11',20,[menu('points','Published answer points',5,4,named(business,['Wide range –','Cost & quality –','Availability –','Perceived benefits –','Value to the economy –','Uses local produce,','Good support']))],'5 points @ 4')
 types=guide(10,'Type 1 -','x symptoms',);types='Type 1 - '+types
 symptoms=examples(select(guide(10,'x symptoms','x specific dietary'),'(6)'))
 diet=guide(10,'Specific Dietary Requirements','(b)');diet=[v.strip() for v in diet.split('x ') if v.strip()]
 add(2,'a','0-1',30,[criterion('types','types',6,[0,2],'Six points across the requested types. Historical scheme guidance: '+types),menu('symptoms','symptoms',3,2,[x.strip() for x in symptoms.split(',')]),menu('diet','specific dietary requirements',4,3,diet,'The source wording is retained for this 2011 examination task.')],'Types 6 × 2 + symptoms 3 × 2 + dietary requirements 4 × 3')
 sweet=guide(10,'Artificial –','(c)');intense=select(sweet,'Intense –','Bulk –');bulk=select(sweet,'Bulk –')
 add(2,'b','0-11',12,[point('intense','Intense sweeteners',3),criterion('intense-example','Examples',1,[0,3],'One example matching Intense sweeteners. Source: '+intense),point('bulk','Bulk sweeteners',3),criterion('bulk-example','Examples',1,[0,3],'One example matching Bulk sweeteners. Original 2011 classification/examples retained: '+bulk)],'2 classifications × 3 + 2 matching examples × 3')
 uses=guide(10,'2 points @ 4 marks each');add(2,'c','0-11',8,[menu('uses','uses of sweeteners',2,4,named(uses,['To sweeten','Used in slimming','Production of diabetic','Production of soft','Used an ingredient','Used in preservation','Used as a humectant']))],'2 points @ 4')
 choice=guide(11,'5 points @ 4 marks each','(b)');add(3,'a','0-10',20,[menu('factors','factors',5,4,named(choice,['Culture –','Sensory aspects –','Nutritional awareness –','Health status –','Marketing and advertising –','Money available –','Eating patterns –','Availability –','Safety issues –']))],'5 points @ 4')
 profile=guide(11,'e..g. flour, cook chill meals','(c)')
 add(3,'b','0-11',20,[menu('name','name of product',1,2,chosen(profile,['Flour','Cook chill meals'])),criterion('production','stages of production',5,[0,2],'Five production points for ONE chosen product. Complete source models: '+profile),criterion('packaging','packaging',2,[0,2],'Two packaging points for that SAME product. Complete source models: '+profile),criterion('labelling','labelling',2,[0,2],'Two labelling points for that SAME product. Complete source models: '+profile)],'Name 2 + production 5 × 2 + packaging 2 × 2 + labelling 2 × 2')
 judged(3,'c','1-2',2,5,'protection',guide(11,'2 points @ 5 marks each'))
 family=guide(12,'2 points @ 5 marks each','(b)');add(4,'a','1-1',10,[menu('roles','role of the household/family',2,5,named(examples(family),['Family members','Spending creates','Family provides','Money Management','Many families','Pay taxes','Produces children']))],'2 points @ 5')
 social=guide(12,'4 points @ 6 marks each','(c)');add(4,'b','1-1',24,[point(f'factor-{i}',v,6,'Historical 2011 scheme wording; each of the four named factors is required.') for i,v in enumerate(named(social,['Age –','Gender –','Social class –','Cultural factors –']),1)],'4 required factors × 6')
 judged(4,'c','1-1',4,4,'factors',guide(12,'4 points @ 4 marks each'))
 definition=guide(13,'Definition (5 marks)','Universality (5 marks)');universality=guide(13,'Universality (5 marks)','(b)');whole=prompt(5,'a')
 c=add(5,'a','2-0',5,[menu('definition','Definition',1,5,named(definition,['Group of people','‘The basic unit','‘The natural,']))],'Definition 5');c.update(id='he-2011-hl-sb-q5a-definition',questionRef='2011 HL Section B Q5(a) — definition',questionText=whole.split(' and explain',1)[0])
 c=add(5,'a','2-0',5,[point('universality',universality,5)],'Universality 5');c.update(id='he-2011-hl-sb-q5a-universality',questionRef='2011 HL Section B Q5(a) — universality',questionText='explain'+whole.split(' and explain',1)[1],stem=whole)
 judged(5,'b','2-1',6,4,'roles and responsibilities',guide(13,'6 points @ 4 marks each','(c)'))
 independence=guide(13,'4 points @ 4 marks each');add(5,'c','2-3',16,[menu('factors','factors',4,4,[v.strip() for v in independence.split('x ') if v.strip()])],'4 points @ 4')
 assert len(cards)==17 and sum(c['totalMarks'] for c in cards)==280,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('B',cards,dict(tasks=17,marks=280,selectionDecisions='One separate definition and universality task at the explicit five marks each. Required protein/diabetes/food profiles and paired classifications/examples remain whole. B1 chart requires all four products with explicit analysis2 plus elaboration3 per product. Milk process variants preserve the corresponding full method-specific guidance.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
