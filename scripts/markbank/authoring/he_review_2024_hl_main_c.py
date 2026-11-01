#!/usr/bin/env python3
"""Full 2024 Higher elective/core review with source-backed identity consolidation."""
from copy import deepcopy
import json,re,sys
from he_review_2024_hl_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections
CLARIFICATIONS={
 'cholesterol':dict(source='https://www.canada.ca/en/health-canada/services/nutrients/cholesterol.html',note='Plant oils do not contain dietary cholesterol; the scheme’s HDL-in-plant-oils wording is incorrect.'),
 'lipoproteins':dict(source='https://www.cdc.gov/cholesterol/about/ldl-and-hdl-cholesterol-and-triglycerides.html',note='LDL and HDL carry cholesterol in blood; they are not categories of cholesterol contained in animal and plant fats.'),
 'insulin':dict(source='https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-2-diabetes',note='Insulin helps glucose enter cells; it does not break sugar down into glucose.'),
 'saturated-fat':dict(source='https://www.cdc.gov/cholesterol/prevention/index.html',note='High saturated-fat intake can contribute to high cholesterol and heart disease. Other outcomes in the source are not inevitable direct effects of saturated fat.')}


def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(18,30)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};old=originals();fixes={};added=[]
 def put(n,part,roman,marks,notation,rows,suffix='',**extra):
  group=p[n].split(f'{n}.({part})',1)[1]
  if part!='c':group=group.split(f'{n}.({chr(ord(part)+1)})',1)[0]
  if roman:prompt=between(group,f'({roman})',f'({marks} marks)');stem=group.split('(i)',1)[0].strip()
  else:stem,prompt=group.split('Write a profile',1);prompt='Write a profile'+prompt.split(f'({marks} marks)',1)[0];stem=stem.strip()
  prompt=prompt.replace(' • ','\n• ');assert not re.search(r'\((?:i|ii|iii|iv)\)',prompt),prompt
  cid=f'he-2024-hl-sc-q{n}{part}{roman}{suffix}';fixes[cid]=dict(reason='Full 2024 Higher C source review: complete required prompts, all continued guidance, exact allocations and whole open profiles.',set=dict(questionText=prompt,questionRef=f'2024 HL Section C '+(f'E{n} ' if n<4 else '')+f'Q{n}({part})'+(f'({roman})' if roman else ''),stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Full source review: he_review_2024_hl_main_c.py. Required headings and paired name/detail responses remain whole.',**extra));return cid
 def body(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end)
  return (t.split(end,1)[0] if end else t).strip()
 def points(n,part,roman,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return put(n,part,roman,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 v=named_sections(body(18,'1 point on each factor & 2 other points','(ii)'),['cost budget','family stage and circumstances number','ergonomics design']);v=[a+b for a,b in zip(['budget ','number ','design '],v)]
 put(1,'a','i',20,'Cost 1 + family 1 + ergonomics 1 + other 2, each 4 (4:2:0)',[criterion(k,label,1,[0,2,4],'One required factor, graded 4:2:0. '+('The paper says family size and circumstances; the scheme says stage. Retain the paper wording. ' if k=='family' else '')+'Complete guidance: '+value) for k,label,value in zip(['cost','family','ergonomics'],['cost','family stage and circumstances','ergonomics'],v)]+[criterion('other','other points',2,[0,2,4],'Two further distinct points under any of the three required headings, each graded 4:2:0.')])
 design=body(18,'[Name 2 marks (graded 2:0), description 4 marks (graded 4:2:0)] x3');rows=[];groups=[]
 for i in range(1,4):
  rows += [criterion(f'name-{i}','Name',1,[0,2],f'Name principle {i}, graded 2:0. '+('Complete guidance for all four examples: '+design if i==1 else 'Choose another principle.')),criterion(f'application-{i}','description',1,[0,2,4],f'Describe application of the same principle {i}, graded 4:2:0.')];groups.append(dict(sourceCardId=f'he-2024-hl-sc-q1aii-principle-{i}',label=f'Chosen principle {i}',marks=6,rowIds=[f'name-{i}',f'application-{i}']))
 put(1,'a','ii',18,'3 principles × (name 2 (2:0) + application 4 (4:2:0))',rows,taskGroups=groups)
 points(1,'a','iii',12,3,[0,2,4],body(19,'3 points @ 4 marks (graded 4:2:0)','and 1.(b)'))
 values=named_sections(body(19,'2 points @ 6 marks (graded 6:4:2:0)','(ii)'),['miniature circuit breaker will','earth wire is']);values=['will '+values[0],'is '+values[1]]
 put(1,'b','i',12,'2 required devices × 6 (6:4:2:0)',[criterion(k,label,1,[0,2,4,6],'Explain this required safety function, graded 6:4:2:0. Labelled diagrams are accepted. These historical descriptions are not installation or repair instructions. Complete guidance: '+v) for k,label,v in zip(['mcb','earth'],['miniature circuit breaker','earth wire'],values)])
 energy=body(19,'3 inefficiencies @ 2 marks (graded 2:0), 3 strategies @ 4 marks (graded 4:2:0)').removesuffix(' or');rows=[];groups=[]
 for i in range(1,4):
  rows += [criterion(f'inefficiency-{i}','inefficiencies',1,[0,2],f'Identify inefficiency {i}, graded 2:0. '+('Complete paired guidance for all seven examples: '+energy if i==1 else 'Choose a different inefficient use.')),criterion(f'strategy-{i}','strategies',1,[0,2,4],f'Assess a matching strategy for your inefficiency {i}, graded 4:2:0.')];groups.append(dict(sourceCardId=f'he-2024-hl-sc-q1bii-case-{i}',label=f'Inefficiency and strategy {i}',marks=6,rowIds=[f'inefficiency-{i}',f'strategy-{i}']))
 put(1,'b','ii',18,'3 paired responses × (inefficiency 2 (2:0) + strategy 4 (4:2:0))',rows,taskGroups=groups)
 cid=put(1,'c','i',18,'Principle 3 × 2 + methods 3 × 4',[]);v=fixes[cid]['set'];v.update(questionText='Explain the underlying principle of insulation used in the home.',questionRef='2024 HL Section C E1 Q1(c)(i) — principle',totalMarks=6,tariffModel=dict(kind='fixed',notation='3 points × 2 (2:1:0)'),rows=[criterion('principle','underlying principle',3,[0,1,2],'Three explanation points, each graded 2:1:0. Complete guidance: '+body(20,'3 points @ 2 marks (graded 2:1:0)','methods of home insulation'))])
 c=deepcopy(old[cid]);c.update(id=cid+'-methods',conceptId='home-insulation-methods',questionText='Identify and describe three different methods of home insulation.',questionRef='2024 HL Section C E1 Q1(c)(i) — methods',stem=v['stem'],totalMarks=12,tariffModel=dict(kind='fixed',notation='3 methods × 4 (4:3:2:1:0)'),rows=[criterion('methods','methods of home insulation',3,[0,1,2,3,4],'Three identified and described methods, each graded 4:3:2:1:0. No separate naming tariff is printed. Complete guidance, including labelled-diagram acceptance: '+body(20,'3 points @ 4 marks (graded 4:3:2:1:0)','(ii)'))],notes='Independent second prompt, with a separately published 12-mark tariff; the original ID retains the 6-mark underlying principle.');added.append(c)
 points(1,'c','ii',12,3,[0,2,4],body(20,'3 points @ 4 marks (graded 4:2:0)'))
 values=named_sections(body(21,'(15 marks)','(ii)'),['comfort loose','aesthetic appeal relaxed','current fashion trends fashionable']);values=[a+b for a,b in zip(['loose ','relaxed ','fashionable '],values)]
 put(2,'a','i',15,'3 required headings × 5 (5:3:0)',[criterion(k,label,1,[0,3,5],'Evaluate the pictured outfits under this required heading, graded 5:3:0. Complete guidance: '+value) for k,label,value in zip(['comfort','aesthetic','trends'],['comfort','aesthetic appeal','current fashion trends'],values)],questionFigureKey='home-economics-2024-hl-sc-q2ai-summer-outfits',questionFigureIncludesPrompt=False,figureKey='')
 values=named_sections(body(21,'1 point on each heading'),['social factors','economic factors']);values[-1]=values[-1].removesuffix(' and')
 put(2,'a','ii',10,'Social 1 + economic 1, each 5 (5:3:0)',[criterion(k,label,1,[0,3,5],'Discuss this required heading, graded 5:3:0. Complete guidance: '+value) for k,label,value in zip(['social','economic'],['social factors','economic factors'],values)])
 production,properties,identification=named_sections(body(22,'(15 marks)','or 2.(c)'),['fibre production wool','fabric properties wool','identification test wool']);columns=[]
 for value,heads in [(production,['wool fleece','silk silkworms','cotton comes','linen made']),(properties,['wool durable','silk strong','cotton strong','linen strong']),(identification,['wool doesn’t','silk doesn’t','cotton burns','linen burns'])]:
  columns.append([head.split(' ',1)[1]+' '+text for head,text in zip(heads,named_sections('wool '+value,heads))])
 routes=[]
 for i,name in enumerate(['Wool','Silk','Cotton','Linen']):
  routes.append(dict(id=name.lower(),label=name,rows=[criterion('name','Name',1,[0,2],'Name the natural-fibre fabric, graded 2:0. This model: '+name),criterion('production','fibre production',3,[0,1,2],'Three production points, each graded 2:1:0. Complete guidance: '+columns[0][i]),criterion('properties','fabric properties',3,[0,1],'Three properties, each graded 1:0. Complete guidance: '+columns[1][i]),criterion('identification','identification test',2,[0,1,2],'Two identification-test points, each graded 2:1:0. Source observations for supervised practical work: '+columns[2][i])]))
 other=deepcopy(routes[0]['rows']);notes=['Name another valid natural-fibre fabric, graded 2:0; the choice is open.','Three accurate production points for your chosen fabric, each graded 2:1:0. No model for this alternative is printed.','Three accurate properties, each graded 1:0.','Two accurate identification-test points, each graded 2:1:0.']
 for row,note in zip(other,notes):row['contextNote']=note
 routes.append(dict(id='another',label='Another natural-fibre fabric',rows=other))
 put(2,'b','',15,'Name 2; production 3 × 2 (2:1:0); properties 3 × 1; identification 2 × 2 (2:1:0)',deepcopy(routes[0]['rows']),suffix='-wool',answerVariants=routes,conceptId='natural-fibre-fabric-profile')
 for name in ['silk','cotton','linen']:fixes[f'he-2024-hl-sc-q2b-{name}']=dict(reason='One open natural-fibre profile shares one grid and topic. All four published routes and another valid choice are retained on the original wool ID; the withdrawn identity remains an explicit progress alias.',drop=True,replacementId='he-2024-hl-sc-q2b-wool')
 points(2,'c','i',6,2,[0,2,3],body(22,'2 points @ 3 marks (graded 3:2:0)'))
 designer=body(23,'work 2 points @ 3 marks (graded 3:2:0)')
 put(2,'c','ii',9,'Name 3 + 2 work points × 3 (3:2:0)',[criterion('name','Name of designer',1,[0,2,3],'Name one Irish designer, graded 3:2:0. Complete continued guidance (the printed “Philip Tracey” refers to Philip Treacy): '+designer),criterion('work','work',2,[0,2,3],'Two points about the work of the same chosen designer, each graded 3:2:0. The source examples do not restrict the open choice.')])
 social,work=named_sections(body(24,'(2 points on method of socialisation, 2 points on preparation for work + 1 other point)','(ii)'),['as a method of socialisation','as preparation for work'])
 put(3,'a','i',20,'Socialisation 2 + work 2 + other 1, each 4 (4:2:0)',[criterion('socialisation','socialisation',2,[0,2,4],'Two points, each graded 4:2:0. Complete guidance: '+social),criterion('work','preparation for work',2,[0,2,4],'Two points, each graded 4:2:0. Complete guidance: '+work),criterion('other','other point',1,[0,2,4],'One further distinct point under either heading, graded 4:2:0.')])
 points(3,'a','ii',15,3,[0,2,3,4,5],body(24,'3 supports @ 5 marks (graded 5:4:3:2:0)','(iii)'),label='supports')
 points(3,'a','iii',15,3,[0,3,5],'Historical examples of structural opportunities and barriers, not assumptions about any individual pupil or family. '+body(24,'3 factors @ 5 marks (graded 5:3:0)').removesuffix(' and'),label='factors')
 points(3,'b','i',18,3,[0,2,4,6],'For each of three groups, connect identification with an explanation; the scheme publishes one six-mark allocation per response, not a separate name tariff. The examples describe possible barriers and discrimination, not inherent traits of everyone in the group. '+body(25,'3 points @ 6 marks (graded 6:4:2:0)','(ii)'))
 initiative=body(25,'explain 2 points @ 4 marks (graded 4:2:0)').removesuffix(' or')
 put(3,'b','ii',12,'Name 4 + 2 details × 4 (4:2:0)',[criterion('name','Name',1,[0,2,4],'Name one community initiative, graded 4:2:0. Complete historical examples: '+initiative),criterion('details','explain',2,[0,2,4],'Two details about the same initiative, each graded 4:2:0. Quality claims in examples are possible characteristics, not guarantees.')])
 values=named_sections(body(26,'(1 reference to physical development, 1 reference to social development, 1 reference to emotional development)','(ii)'),['physical development','social development','emotional development'])
 put(3,'c','i',18,'3 required areas × 6 (6:4:2:0)',[criterion(k,label,1,[0,2,4,6],'Evaluate this required area, graded 6:4:2:0. Benefits depend on the activity and circumstances; they are not guaranteed medical outcomes. Complete guidance: '+value) for k,label,value in zip(['physical','social','emotional'],['physical development','social development','emotional development'],values)])
 social,cultural=named_sections(body(26,'1 reference to social factors, 1 reference to cultural factors & 1 other point'),['social factors','cultural factors'])
 put(3,'c','ii',12,'Social 1 + cultural 1 + other 1, each 4 (4:2:0)',[criterion('social','social factors',1,[0,2,4],'One social factor, graded 4:2:0. Complete guidance: '+social),criterion('cultural','cultural factors',1,[0,2,4],'One cultural factor, graded 4:2:0. Complete guidance: '+cultural),criterion('other','other point',1,[0,2,4],'One further distinct point under either heading, graded 4:2:0.')])
 points(4,'a','i',20,5,[0,1,2,3,4],'Source correction: plant oils do not contain dietary cholesterol. HDL/LDL are blood lipoproteins, not types of cholesterol contained respectively in plant/animal fats. Composition varies by food. '+body(27,'5 points @ 4 marks (graded 4:3:2:1:0)','(ii)'),label='nutritional significance')
 process=body(27,'Packaging and labelling 5 points @ 1 mark (graded 1:0)');production,packaging=process.split('weighed retail',1)
 put(4,'a','ii',15,'Hydrogenation 1 + other production 4, each 2 (2:1:0); packaging/labelling 5 × 1',[
  criterion('hydrogenation','hydrogenation',1,[0,1,2],'The scheme explicitly requires hydrogenation as one of five production points, graded 2:1:0. This is the historical process asked about, not a claim that all modern margarines follow it. Complete production guidance: '+production),
  criterion('production','production',4,[0,1,2],'Four further distinct production points, each graded 2:1:0. Use the complete production guidance above; do not count hydrogenation twice.'),
  criterion('packaging','Packaging and labelling',5,[0,1],'Five points covering packaging and labelling, each graded 1:0. Complete guidance: weighed retail'+packaging)])
 points(4,'a','iii',15,3,[0,1,2,3,4,5],'Source correction: insulin helps glucose enter cells; it does not break sugar down into glucose. High saturated-fat intake can raise LDL and cardiovascular risk. Other outcomes in this historical list involve multiple risk factors and are not inevitable direct effects of saturated fat. '+body(28,'3 health implications @ 5 marks (graded 5:4:3:2:1:0)','and 4.(b)'),label='health implications')
 points(4,'b','i',12,3,[0,2,4],body(28,'3 points @ 4 marks (graded 4:2:0)','(ii)'))
 put(4,'b','ii',18,'Name 2 (2:0); working 3 × 2; use 3 × 2; efficiency 2 × 2 (2:1:0)',[
  criterion('name','Name',1,[0,2],'Name one household electrical appliance with a motor, graded 2:0. The name and required study headings form one open profile.'),
  criterion('working','working principle',3,[0,1,2],'Three points about the chosen appliance, each graded 2:1:0; labelled diagrams accepted. Apply the generic examples only where correct for that appliance. Complete guidance: '+body(28,'• working principle 3 points @ 2 marks (graded 2:1:0)','• guidelines')),
  criterion('use','guidelines for use',3,[0,1,2],'Three relevant use guidelines, each graded 2:1:0. Complete guidance: '+body(28,'• guidelines for use 3 points @ 2 marks (graded 2:1:0)','• energy')),
  criterion('efficiency','energy efficiency',2,[0,1,2],'Two relevant efficiency points, each graded 2:1:0. Historical rating example; apply only to a suitable appliance. Complete guidance: '+body(28,'• energy efficiency 2 points @ 2 marks (graded 2:1:0)').removesuffix(' or'))],suffix='-study')
 points(4,'c','i',15,5,[0,2,3],body(29,'5 points @ 3 marks (graded 3:2:0)','(ii)'))
 points(4,'c','ii',15,3,[0,3,5],body(29,'3 points @ 5 marks (graded 5:3:0)'))
 live=[f for f in fixes.values() if not f.get('drop')];assert len(live)==26 and len(added)==1 and sum(f['set']['totalMarks'] for f in live)+sum(c['totalMarks'] for c in added)==385
 assert all(cid in old for cid in fixes)
 return fixes,added


def write():
 fixes,added=build();save_batch('C',fixes,added,dict(tasks=27,marks=385,sourceClarifications=CLARIFICATIONS,selectionDecisions='Insulation principle and methods have independent prompts and tariffs (6/12). The natural-fibre profile is one open response with four published models and another choice; three duplicate IDs are retained as explicit progress aliases to the original wool ID. Restore the omitted 2-mark appliance name to its dependent 18-mark study. All required headings, paired examples, community initiatives and Irish designer profiles remain whole. Preserve the designer continuation on page 23.',progressAliases={cid:f['replacementId'] for cid,f in fixes.items() if f.get('drop')},checked='2026-11-01'));print('2024 Higher C: 27 reviewed tasks, 385 offered marks; three duplicate identities aliased.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
