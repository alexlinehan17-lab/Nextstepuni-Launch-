#!/usr/bin/env python3
"""2026 Higher C: required headings, full profile routes and continuation pages."""
from copy import deepcopy
import json,re,sys
from he_review_2026_hl_main import ROOT,documents,page_text,card,save_batch,criterion,between,named_sections,after,any_points
CLARIFICATIONS={'hydropower':dict(source='https://www.esbarchives.ie/generation/article/ardnacrusha',note='River hydropower is established in Ireland, including Ardnacrusha since 1929; the scheme conflates it with marine-generation limitations.'),'thermal-comfort':dict(source='https://iris.who.int/bitstream/handle/10665/277465/WHO-CED-PHE-18.10-eng.pdf?ua=1',note='WHO uses 18°C as a general-population cold-season baseline; vulnerable people may need warmer conditions. The source’s 10–16°C bedroom range is not a safe universal recommendation.')}

def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(17,29)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};cards=[]
 def group(n,part):
  text=p[n].split(f'{n}.({part})',1)[1] if f'{n}.({part})' in p[n] else p[n].split(f'{n}.({part})'.replace('.',''),1)[1]
  if part!='c':text=re.split(rf'{n}\.?\({chr(ord(part)+1)}\)',text,1)[0]
  return text
 def add(n,part,roman,topic,concept,marks,notation,rows,**extra):
  text=group(n,part)
  if roman:prompt=between(text,f'({roman})',f'({marks} marks)');stem=text.split('(i)',1)[0].strip()
  else:stem,prompt=text.split('Write a profile',1);prompt='Write a profile'+prompt.split(f'({marks} marks)',1)[0];stem=stem.strip()
  c=card(f'sc-q{n}{part}{roman}','C',(f'E{n} ' if n<4 else '')+f'Q{n}({part})'+(f'({roman})' if roman else ''),topic,concept,prompt.strip().replace(' • ','\n• '),stem,marks,notation,rows,n+4);c.update(extra);cards.append(c);return c
 def body(n,token,end=None):return after(s[n],token,end).removesuffix(' and').removesuffix(' or')
 def points(n,part,roman,topic,concept,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return add(n,part,roman,topic,concept,marks,f'{count} point'+('s' if count!=1 else '')+f' × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct point'+('s' if count!=1 else '')+f', each graded {grade}. Complete historical guidance: '+text)],**extra)
 def headings(n,part,roman,topic,concept,labels,values,count,steps,**extra):
  grade=':'.join(map(str,reversed(steps)));return add(n,part,roman,topic,concept,len(labels)*count*steps[-1],f'{len(labels)} required headings × {count} point'+('s' if count!=1 else '')+f' × {steps[-1]} ({grade})',[criterion(str(i),label,count,steps,f'{count} '+('point' if count==1 else 'points')+f' under this required heading, each graded {grade}. Complete historical guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)],**extra)
 points(1,'a','i','3-3','housing-provision-adequacy',20,4,[0,3,5],'Current refers to the 2026 examination context. '+body(17,'4 points @ 5 marks (graded 5:3:0)','(ii)'))
 points(1,'a','ii','3-3','housing-amenities-services',15,3,[0,3,5],body(17,'3 points @ 5 marks (graded 5:3:0)'))
 points(1,'a','iii','3-3','housing-styles-history',15,3,[0,3,5],'Three points are priced without a compulsory one-per-century split. '+body(18,'3 points @ 5 marks (graded 5:3:0)','and 1.(b)'))
 labels=['Family requirements','Technological developments','Aesthetic and environmental factors'];values=named_sections(body(18,'(15 marks) Family requirements'),['open-plan areas;','Technological developments','Aesthetic and environmental factors']);values[0]='open-plan areas; '+values[0]
 headings(1,'b','i','3-3','house-design-construction-factors',labels,values,1,[0,3,5])
 points(1,'b','ii','3-3','house-building-professional-services',15,3,[0,3,5],body(19,'3 services @ 5 marks (graded 5:3:0)','or 1.(c)'),label='services')
 names=['Solar power:','Hydro-power:','Wind power:','Bio energy:','Geo-thermal:'];values=named_sections(body(19,'1 advantage, 1 disadvantage & 1 other point'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  assert value.startswith('advantages:');advantage,disadvantage=[x.strip() for x in value.removeprefix('advantages:').split('disadvantages:',1)];note='Source models depend on location, installation and operating conditions. '
  if i==1:note+='Source correction: river hydropower has operated commercially in Ireland since 1929. Being surrounded by sea is not the explanation for river hydropower; the source mixes marine-energy limitations into this model. '
  variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,2,3],'Name this chosen source, graded 3:2:0.'),criterion('advantage','advantage',1,[0,3,5],'One advantage of the SAME source, graded 5:3:0. '+note+'Complete wording: '+advantage),criterion('disadvantage','disadvantage',1,[0,3,5],'One disadvantage, graded 5:3:0. '+note+'Complete wording: '+disadvantage),criterion('other','other point',1,[0,3,5],'One further distinct advantage or disadvantage for the SAME source, graded 5:3:0.')]))
 other=deepcopy(variants[0]['rows']);other[0].update(verbatim='name',contextNote='Name another valid renewable source, graded 3:2:0. The choice is open.');other[1]['contextNote']='One accurate advantage of the SAME source, graded 5:3:0. No further model is printed.';other[2]['contextNote']='One accurate disadvantage of the SAME source, graded 5:3:0. No further model is printed.';variants.append(dict(id='another',label='Another valid renewable source',rows=other))
 add(1,'c','i','3-6','renewable-energy-profile',18,'Name 3 (3:2:0); advantage 5 + disadvantage 5 + other 5 (5:3:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(1,'c','ii','3-5','thermal-comfort-control',12,3,[0,2,4],'Source clarification: the printed 10–16°C bedroom range is not a safe universal target. WHO uses 18°C as a general-population indoor baseline during cold seasons, and vulnerable people may need warmer conditions. Complete historical wording: '+body(20,'3 points @ 4 marks (graded 4:2:0)'))
 points(2,'a','i','3-8','current-fashion-trends',9,3,[0,1,2,3],'Current refers to the 2026 paper. Each point must name and describe a trend; there is no extra naming tariff. '+body(21,'3 points @ 3 marks (graded 3:2:1:0)','(ii)'))
 outfit=add(2,'a','ii','3-8','fashion-trend-outfit-sketch',9,'Sketch 5 (5:3:1:0) + description 2 × 2 (2:1:0)',[criterion('sketch','Sketch',1,[0,1,3,5],'Sketch an outfit incorporating ONE current trend, graded 5:3:1:0. The scheme prints this criterion and ladder without a model drawing; no invented drawing requirements.'),criterion('description','Description',2,[0,1,2],'Two description points for the SAME outfit, each graded 2:1:0. The scheme prints the criterion, without a developed model description.')])
 fabric,aesthetic=named_sections(body(21,'(7 marks)','and 2.(b)'),['Suitable fabrics','Aesthetic appeal'])
 add(2,'a','iii','3-8','fashion-outfit-fabric-appeal',7,'Suitable fabric 3 (3:0) + aesthetic appeal 4 (4:2:0)',[any_points('fabric','Suitable fabrics',1,3,fabric,'Choose a fabric suited to the outfit in the task context. '),criterion('aesthetic','Aesthetic appeal',1,[0,2,4],'One developed point about the SAME outfit, graded 4:2:0. Complete guidance: '+aesthetic)],stem=outfit['stem']+'\n'+outfit['questionText'])
 full=body(21,'(15 marks) Fibre production')+' '+s[22].split('or 2.(c)',1)[0];production,test,properties=named_sections('Fibre production '+full,['Fibre production','Fabric identification test','Fabric properties']);names=['Wool:','Silk:','Linen:','Cotton:'];columns=[named_sections(value,names) for value in [production,test,properties]];variants=[]
 for i,name in enumerate(names):
  variants.append(dict(id=name[:-1].lower(),label=name[:-1],rows=[dict(id='name',kind='point',verbatim=name[:-1],marks=3),criterion('production','Fibre production',2,[0,1,2],'Two points for the SAME fabric, each graded 2:1:0. Complete guidance: '+columns[0][i]),criterion('identification','Fabric identification test',2,[0,1,2],'Two identification observations for the SAME fabric, each graded 2:1:0. Source observations for a supervised practical, not directions for unsupervised flame testing: '+columns[1][i]),criterion('properties','Fabric properties',2,[0,1,2],'Two properties of the SAME fabric, each graded 2:1:0. Complete historical guidance: '+columns[2][i])]))
 other=[criterion('name','Name',1,[0,3],'Name another valid natural fabric, graded 3:0.'),criterion('production','Fibre production',2,[0,1,2],'Two accurate production points for the SAME fabric, each graded 2:1:0. No additional model is printed.'),criterion('identification','Fabric identification test',2,[0,1,2],'Two identification-test points for the SAME fabric, each graded 2:1:0. No additional model is printed.'),criterion('properties','Fabric properties',2,[0,1,2],'Two accurate properties of the SAME fabric, each graded 2:1:0.')];variants.append(dict(id='another',label='Another valid natural fabric',rows=other))
 add(2,'b','','3-7','natural-fabric-profile',15,'Name 3 (3:0) + 3 headings × 2 points × 2 (2:1:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(2,'c','i','3-8','clothing-function-choice',6,1,[0,2,4,6],'The example belongs to the same developed explanation; there is no separate example tariff. '+body(22,'1 point @ 6 marks (graded 6:4:2:0)','(ii)'))
 points(2,'c','ii','3-8','clothing-social-influences',9,3,[0,2,3],body(22,'3 points @ 3 marks (graded 3:2:0)'))
 points(3,'a','i','3-9','unemployment-extent-distribution',20,4,[0,3,5],'Statistics and regional comparisons belong to the 2026 paper, not a current labour-market report. '+body(23,'4 points @ 5 marks (graded 5:3:0)','(ii)'))
 effects=body(23,'1 point on individual, 1 point on society & 2 other points')
 add(3,'a','ii','3-9','unemployment-individual-society',20,'Individual 1 + society 1 + other 2, each 5 (5:3:0)',[criterion('individual','individual',1,[0,3,5],'One effect on the individual, graded 5:3:0. These are possible effects, not inevitable outcomes. Complete source guidance for both headings: '+effects),criterion('society','society',1,[0,3,5],'One distinct effect on society, graded 5:3:0. Use the full source guidance above.'),criterion('other','other points',2,[0,3,5],'Two further distinct effects from either heading, each graded 5:3:0.')])
 names=['Industrial Development Authority (IDA):','Enterprise Ireland:','Local Enterprise Offices (LEO):','Údarás Na Gaeltachta:'];values=named_sections(body(24,'Discussion: 2 points @ 3 marks (graded 3:2:0)','and 3.(b)'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,2,4],'Name this response, graded 4:2:0.'),criterion('discussion','Discussion',2,[0,2,3],'Two discussed points about the SAME response, each graded 3:2:0. Historical guidance: '+value)]))
 variants.append(dict(id='another',label='Another valid statutory response',rows=[criterion('name','Name',1,[0,2,4],'Name another valid statutory response, graded 4:2:0.'),criterion('discussion','Discussion',2,[0,2,3],'Two accurate discussed points about that SAME response, each graded 3:2:0. No further model is printed.')]))
 add(3,'a','iii','3-9','statutory-employment-response',10,'Name 4 (4:2:0) + discussion 2 × 3 (3:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(3,'b','i','3-11','voluntary-work-personal-benefits',15,3,[0,3,5],body(24,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 points(3,'b','ii','3-11','voluntary-work-community-benefits',15,3,[0,3,5],s[24].rsplit('3 points @ 5 marks (graded 5:3:0)',1)[1].strip())
 labels=['Physical development','Emotional development','Intellectual development','Moral development'];values=named_sections(body(25,'(20 marks)','(ii)'),[x+':' for x in labels]);headings(3,'c','i','3-10','education-child-development',labels,values,1,[0,3,5])
 names=['The Early Childhood Care and Education (ECCE) Scheme:','The Early Start Programme:'];values=named_sections(body(25,'Details: 2 points @ 3 marks (graded 3:2:0)'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,2,4],'Name this initiative, graded 4:2:0.'),criterion('details','Details',2,[0,2,3],'Two details for the SAME initiative, each graded 3:2:0. The following eligibility, entry dates and schedules are historical scheme examples, not current application guidance: '+value)]))
 variants.append(dict(id='another',label='Another valid statutory initiative',rows=[criterion('name','Name',1,[0,2,4],'Name another valid statutory pre-school initiative, graded 4:2:0.'),criterion('details','Details',2,[0,2,3],'Two accurate details about the SAME initiative, each graded 3:2:0. No further model is printed.')]))
 add(3,'c','ii','3-10','statutory-preschool-initiative',10,'Name 4 (4:2:0) + details 2 × 3 (3:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(4,'a','i','0-9','wholegrain-cereal-diet',16,4,[0,1,2,3,4],'Effects depend on the food and overall diet; historical health wording does not guarantee prevention or treatment. '+body(26,'4 points @ 4 marks (graded 4:3:2:1:0)','(ii)'))
 production=body(26,'7 points @ 2 marks (graded 2:1:0)','Packaging:');pack=body(26,'Packaging: 2 points @ 1 mark (graded 1:0)','Labelling:');label=body(26,'Labelling: 2 points @ 1 mark (graded 1:0)')
 add(4,'a','ii','0-9','flour-production-packaging',18,'Production 7 × 2 (2:1:0) + packaging 2 × 1 + labelling 2 × 1 (1:0)',[criterion('production','Stages of production',7,[0,1,2],'Seven production points, each graded 2:1:0. Complete source guidance: '+production),any_points('packaging','Packaging',2,1,pack),any_points('labelling','Labelling',2,1,label)])
 points(4,'a','iii','0-11','cereal-dietary-requirements',16,4,[0,2,4],body(27,'4 points @ 4 marks (graded 4:2:0)','and 4.(b)'))
 names=['Simple Difference Paired Comparison Test:','Directional Paired Comparison Test:','Triangle Test:','Duo-trio Test:'];values=named_sections(body(27,'(18 marks)'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  aim,implementation=named_sections(value,['Aim:','Implementation:']);variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,2,3],'Name this chosen test, graded 3:2:0.'),criterion('aim',aim,1,[0,2,3],'State the aim of the SAME test, graded 3:2:0.'),criterion('implementation','Implementation',6,[0,1,2],'Six implementation points for the SAME test, each graded 2:1:0. Complete model, including its lower-page conclusion: '+implementation)]))
 variants.append(dict(id='another',label='Another valid difference test',rows=[criterion('name','name of test',1,[0,2,3],'Name another valid difference test, graded 3:2:0.'),criterion('aim','aim',1,[0,2,3],'State that SAME test’s aim accurately, graded 3:2:0.'),criterion('implementation','implementation',6,[0,1,2],'Six accurate implementation points for that SAME test, each graded 2:1:0. No additional model is printed.')]))
 add(4,'b','i','0-2','sensory-difference-test',18,'Name 3 + aim 3 (3:2:0) + implementation 6 × 2 (2:1:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(4,'b','ii','0-2','sensory-test-controlled-conditions',12,4,[0,2,3],body(28,'4 points @ 3 marks (graded 3:2:0)','or 4.(c)'))
 points(4,'c','i','2-0','family-additional-needs-challenges',18,3,[0,2,4,6],'These are possible challenges and depend on each family’s circumstances. '+body(28,'3 points @ 6 marks (6:4:2:0)','(ii)'))
 names=['Rehab:','Enable Ireland:'];values=named_sections(body(28,'Details 3 points @ 3 marks (graded 3:2:0)'),names);second,other_names=values[1].split('Irish Wheelchair Association;',1);values[1]=second.strip();variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,2,3],'Name this organisation, graded 3:2:0.'),criterion('details','Details',3,[0,2,3],'Three details of the SAME organisation, each graded 3:2:0. Complete historical model: '+value)]))
 variants.append(dict(id='another',label='Another valid voluntary organisation',rows=[criterion('name','Name',1,[0,2,3],'Name another valid organisation, graded 3:2:0. The scheme also names Irish Wheelchair Association;'+other_names),criterion('details','Details',3,[0,2,3],'Three accurate details of that SAME organisation, each graded 3:2:0. No further developed model is printed.')]))
 add(4,'c','ii','2-0','voluntary-family-disability-support',12,'Name 3 + details 3 × 3 (3:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 assert len(cards)==27 and sum(c['totalMarks'] for c in cards)==385
 return cards

def write():
 cards=build();save_batch('C',cards,dict(tasks=27,marks=385,selectionDecisions='All required headings and dependent profiles stay whole. C2(a)(iii) carries the exact previous outfit prompt as context. Natural-fabric production continues onto page22; complete all four models. Open energy, fabric, employment, pre-school, sensory-test and support-organisation choices carry every printed model plus a valid open alternative. No invented sketch rubric or name/detail split.',sourceClarifications=CLARIFICATIONS,checked='2026-11-06'));print('2026 Higher C: 27 tasks, 385 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
