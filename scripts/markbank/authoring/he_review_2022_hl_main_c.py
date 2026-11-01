#!/usr/bin/env python3
"""Review every C response, including the continued floor-covering table."""
from copy import deepcopy
import json
import re
import sys
import fitz
from he_review_2022_hl_main import ROOT, documents, page_text, originals, save_batch, criterion, between, named_sections


CLARIFICATIONS={
 'solar':dict(source='https://www.seai.ie/renewable-energy/solar-energy/hot-water-from-solar',note='Solar systems capture sunlight, not wind/rain energy; hot water supply is variable and does not cover every demand without backup.'),
 'insulation':dict(source='https://bsesc.energy.gov/energy-basics/building-envelope-building-science-intro-heat-flow',note='Bulk insulation slows heat flow; reflective barriers are a distinct treatment for radiant transfer.'),
 'texturing':dict(source='https://archive.nptel.ac.in/content/storage2/courses/116102005/m1-introduction/l1-introduction.htm',note='Filament yarn can be texturised for bulk/appearance. The historical scheme uses filament modification broadly and includes fabric finishes.'),
 'canning':dict(source='https://nchfp.uga.edu/how/general-canning-information/ensuring-safe-canned-foods/',note='Low-acid vegetables require a validated pressure-canning process. Short examination examples are not complete preservation recipes.'),
 'irradiation':dict(source='https://www.iaea.org/sites/default/files/publications/magazines/bulletin/bull15-1/15105701822.pdf',note='Enzyme inactivation is not guaranteed by every irradiation treatment; the IAEA source describes blanching before irradiation for enzyme control.'),
 'resistance-heating':dict(source='https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power',note='Electrical resistance converts electrical energy into thermal energy; conduction and convection describe subsequent heat transfer.'),
}


def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(18,31)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};fixes={}
 def put(n,part,roman,marks,notation,rows,**extra):
  group=p[n].split(f'{n}.({part})',1)[1]
  if part!='c':group=group.split(f'{n}.({chr(ord(part)+1)})',1)[0]
  prompt=between(group,f'({roman})',f'({marks} marks)').replace(' \uf0b7 ','\n• ')
  assert not re.search(r'\((?:i|ii|iii|iv)\)',prompt),prompt
  stem=group.split('(i)',1)[0].strip()
  if n==2 and part=='a':stem=stem.split('(www.shutterstock.com)',1)[0].strip()
  fixes[f'he-2022-hl-sc-q{n}{part}{roman}']=dict(reason='Complete 2022 Higher C source review, including all continuation pages and open alternatives.',set=dict(questionText=prompt,questionRef=f'2022 HL Section C '+(f'E{n} ' if n<4 else '')+f'Q{n}({part})({roman})',stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Full source review: he_review_2022_hl_main_c.py. Required headings and open choices remain whole responses.',**extra))
 def body(text,grade):
  value=text.split(f'(graded {grade})',1)[1].strip();assert value.endswith('etc.'),value;return value
 put(1,'a','i',15,'3 services × 5 (5:4:2:0)',[criterion('services','professional services',3,[0,2,4,5],'Name and describe three services relevant to the home-office brief, each graded 5:4:2:0. Complete published guidance: '+body(between(s[18],'(i)','(ii)'),'5:4:2:0'))])
 factors=between(s[18],'(graded 3:2:0)','• properties');table=[]
 # Extract physical table cells, preserving the second-page continuation.
 for page,top,bottom,label in [(18,600,630,'Ceramic tiles'),(18,630,658,'Flagstone / cut stone / stone carpeting'),(18,658,690,'Slate tiles'),(18,690,735,'Marble / limestone'),(18,735,765,'Mosaic tiles'),(19,57,132,'Wood'),(19,132,177,'Vinyl'),(19,177,192,'Cork'),(19,192,265,'Carpet')]:
  value=__import__('he_review_2023_hl').tidy(d['scheme'][page-1].get_text(clip=fitz.Rect(202,top,550,bottom)));assert value.endswith('etc.'),(label,value);name=__import__('he_review_2023_hl').tidy(d['scheme'][page-1].get_text(clip=fitz.Rect(80,top,201,bottom)));table.append((label,name,value))
 routes=[]
 for i,(label,name,value) in enumerate(table,1):
  routes.append(dict(id=f'floor-{i}',label=label,rows=[criterion('name','name of floor covering',1,[0,1,2],'Name a suitable covering for the home office, graded 2:1:0. Complete published names in this route: '+name),criterion('factors','factors to consider',4,[0,2,3],'Four selection factors, each graded 3:2:0. Complete guidance: '+factors),criterion('properties','properties',3,[0,2],'Three properties of that covering, each graded 2:0. Complete published guidance: '+value)]))
 routes.append(dict(id='another',label='Another suitable floor covering',rows=[criterion('name','name of floor covering',1,[0,1,2],'Name a suitable covering, graded 2:1:0. The source also accepts linoleum, concrete and other valid choices.'),criterion('factors','factors to consider',4,[0,2,3],'Four factors, each graded 3:2:0. Complete guidance: '+factors),criterion('properties','properties',3,[0,2],'Three accurate properties of the same covering, each graded 2:0. No model properties for this alternative are printed.')]))
 put(1,'a','ii',20,'Name 2 (2:1:0); factors 4 × 3 (3:2:0); properties 3 × 2 (2:0)',deepcopy(routes[0]['rows']),answerVariants=routes)
 fixes['he-2022-hl-sc-q1aii-properties']=dict(reason='Required name, selection factors and properties form one open floor-covering recommendation under Q1(a)(ii). All source material is restored on the surviving ID; the old name/properties ID is an explicit progress alias.',drop=True,replacementId='he-2022-hl-sc-q1aii')
 labels=['Colour','Pattern','Texture'];values=named_sections(s[19].split('(graded 5:3:0)',1)[1],labels)
 put(1,'a','iii',15,'3 required headings × 5 (5:3:0)',[criterion(f'heading-{i}',label,1,[0,3,5],'Required heading, graded 5:3:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 put(1,'b','i',12,'3 effects × 4 (4:2:0)',[criterion('effects','effects',3,[0,2,4],'Three effects, each graded 4:2:0. Complete guidance: '+body(between(s[20],'(i)','(ii)'),'4:2:0'))])
 ventilation=s[20].split('Artificial methods',1)[1].strip();labels=['Extractor fan','Cooker hood','Modified heat recovery ventilation system'];values=named_sections(ventilation,labels);routes=[]
 for i,(label,value) in enumerate(zip(labels,values),1):
  routes.append(dict(id=f'ventilation-{i}',label=label,rows=[criterion('name','Name',1,[0,1,2],'One method suitable for a kitchen, graded 2:1:0. Source route: '+label),criterion('principle','underlying principle',4,[0,2,4],'Four principle points for the same method, each graded 4:2:0. A recirculating cooker hood filters air but does not supply outdoor replacement air. Complete historical wording: '+value)]))
 routes.append(dict(id='another',label='Another valid ventilation method',rows=[criterion('name','Name',1,[0,1,2],'Name an artificial method suitable for a kitchen, graded 2:1:0.'),criterion('principle','underlying principle',4,[0,2,4],'Four accurate principle points for that method, each graded 4:2:0. No model for this alternative is printed.')]))
 put(1,'b','ii',18,'Name 2 (2:1:0); principle 4 × 4 (4:2:0)',deepcopy(routes[0]['rows']),answerVariants=routes)
 solar=between(s[21],'(i)','(ii)');system=solar.split('(graded 3:2:0)',1)[1].split('• merits',1)[0].strip();merits=between(solar,'Merits -','• sustainability');sustainability=solar.split('Sustainability –',1)[1].strip()
 put(1,'c','i',18,'System 2 × 3; merits 3 × 3; sustainability 3 (all 3:2:0)',[criterion('system','system used in the home',2,[0,2,3],'Two points about a solar system, each graded 3:2:0. Complete examples: '+system),criterion('merits','merits',3,[0,2,3],'Three merits, each graded 3:2:0. Source correction: solar systems use sunlight, not energy from wind or rain; solar hot water is weather-dependent and commonly needs backup. Complete historical wording: '+merits),criterion('sustainability','sustainability',1,[0,2,3],'One point, graded 3:2:0. Complete guidance: '+sustainability)])
 insulation=s[21].split('Example @ 4 marks (graded 4:0)',1)[1];principle,examples=named_sections(insulation,['Underlying Principle','Examples'])
 put(1,'c','ii',12,'Principle 2 × 4 (4:2:0) + example 4 (4:0)',[criterion('principle','Underlying Principle',2,[0,2,4],'Two principle points, each graded 4:2:0. Bulk insulation slows conductive/convective heat flow; reflective barriers reduce radiant transfer. Do not treat all insulation as reflecting heat. Complete historical wording: '+principle),criterion('example','Example',1,[0,4],'One example matching your described method, graded 4:0. Complete examples: '+examples)])

 # Textiles: the requested explanation is illustrated by two examples in one task.
 outfit=s[22].split('(graded 5:3:0)',1)[1].split('(ii)',1)[0].strip();labels=['Comfort','Aesthetic appeal','Lifestyle'];values=named_sections(outfit,labels)
 put(2,'a','i',15,'3 required headings × 5 (5:3:0)',[criterion(f'outfit-{i}',label,1,[0,3,5],'Evaluate the pictured outfits under this required heading, graded 5:3:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)],questionFigureKey='home-economics-2022-hl-sc-q2ai-outfits',questionFigureIncludesPrompt=False,figureKey='')
 put(2,'a','ii',10,'2 points × 5 (5:3:0)',[criterion('colour','colour',2,[0,3,5],'Two points, each graded 5:3:0. The source’s fashion judgements are examples, not universal rules about bodies or appearance. Complete guidance: '+body(s[22].split('(ii)',1)[1],'5:3:0'))])
 fibres=s[23].split('(graded 3:2:0)',1)[1].split('(ii)',1)[0].strip();labels=['Regenerated','Synthetic'];values=named_sections(fibres,labels)
 put(2,'b','i',6,'2 required fibre classes × 3 (3:2:0)',[criterion(f'fibre-{i}',label,1,[0,2,3],'Explain this class, graded 3:2:0. '+('Source typo: “protocol-based” means petrochemical-based in this historical description. ' if i==2 else '')+'Complete wording: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 modification=between(s[23],'Examples – 2 @ 3 marks (graded 3:0)','or 2.(c)');definition,examples=modification.split('Examples',1)
 put(2,'b','ii',9,'Explanation 3 + 2 examples × 3 (all 3:0)',[criterion('explain','Explain',1,[0,3],'Explain the process, graded 3:0. The source uses filament modification broadly, including fabric finishing; in a precise explanation distinguish changes to filaments/yarns from finishes applied to fabric. Published definition: '+definition.strip()),criterion('examples','Examples',2,[0,3],'Two examples illustrating the explanation, each graded 3:0. Texturing gives filament yarn bulk/appearance; the source also accepts a broad list of fabric treatments. Complete historical examples: '+examples.strip())])
 put(2,'c','i',9,'3 points × 3 (3:2:0)',[criterion('pattern','method of modifying',3,[0,2,3],'Three points for one method, each graded 3:2:0. This is an open method choice, not a separate card for every example. Complete guidance: '+body(between(s[23],'2.(c)','(ii)'),'3:2:0'))])
 put(2,'c','ii',6,'2 points × 3 (3:2:0)',[criterion('crafts','traditional crafts',2,[0,2,3],'Two points, each graded 3:2:0. Complete guidance: '+body(s[23].rsplit('(ii)',1)[1],'3:2:0'))])
 put(3,'a','i',6,'Definition 6 (6:3:0)',[criterion('definition','unemployment',1,[0,3,6],'One definition, graded 6:3:0. Complete guidance: '+body(between(s[24],'(i)','(ii)'),'6:3:0'))])
 causes=between(s[24],'Refer to:','(iii)');labels=['changing requirements of industry','geographical location','level of consumer demand for products and services.'];values=named_sections(causes,labels)
 put(3,'a','ii',20,'5 points × 4 (4:2:0): each heading 1 + other 2',[*[criterion(f'cause-{i}',label,1,[0,2,4],'One required point under this heading, graded 4:2:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)],criterion('other','2 other points',2,[0,2,4],'Two further distinct points under any of the required headings, each graded 4:2:0. Do not count a point twice.')])
 put(3,'a','iii',12,'3 effects × 4 (4:2:0)',[criterion('effects','effects of unemployment',3,[0,2,4],'Three effects, each graded 4:2:0. Discuss possible social effects without treating the source’s negative generalisations as facts about unemployed individuals or their families. Complete historical wording: '+body(s[24].split('(iii)',1)[1],'4:2:0'))])
 employment=s[25].split('outline 2 points @ 4 marks (graded 4:2:0)',1)[1].strip();assert employment.endswith('etc.') and 'Local Enterprise Offices' in employment
 put(3,'a','iv',12,'Name 4 + 2 details × 4 (all 4:2:0)',[criterion('name','Name',1,[0,2,4],'Name one statutory initiative, graded 4:2:0. This is an open profile. The source also describes supporting organisations; SOLAS and the National Further Education and Training Authority refer to the same body. Historical examples and details: '+employment),criterion('details','outline',2,[0,2,4],'Two details about how the same initiative enhances employment, each graded 4:2:0. Use the full published examples above; historical eligibility and programme names are not current advice.')])
 put(3,'b','i',12,'3 benefits × 4 (4:2:0)',[criterion('benefits','benefit',3,[0,2,4],'Three benefits, each graded 4:2:0. Complete guidance: '+body(between(s[26],'(i)','(ii)'),'4:2:0'))])
 facilities=s[26].split(') x2',1)[1].strip();labels=['Name –','Cost –','Value for money –','Facilities –'];values=named_sections(facilities,labels);rows=[]
 for i in range(1,3):
  for key,heading,count,steps,value in [('name','Name',1,[0,1],values[0]),('cost','cost',1,[0,1,2],values[1]),('value','value for money',1,[0,1,2],values[2]),('facilities','facilities',2,[0,1,2],values[3])]:
   rows.append(criterion(f'{key}-{i}',heading,count,steps,f'Facility {i} you choose: '+('name graded 1:0. ' if key=='name' else 'Each point graded 2:1:0. ')+'All headings refer to that same facility. Complete examples: '+value))
 put(3,'b','ii',18,'2 profiles × (name 1 + cost 2 + value 2 + facilities 2 × 2)',rows,taskGroups=[dict(sourceCardId=f'he-2022-hl-sc-q3bii-facility-{i}',label=f'Leisure facility {i}',marks=9,rowIds=[f'{key}-{i}' for key in ['name','cost','value','facilities']]) for i in range(1,3)])
 put(3,'c','i',16,'4 factors × 4 (4:2:0)',[criterion('factors','factors',4,[0,2,4],'Four factors, each graded 4:2:0. Complete guidance: '+body(between(s[27],'(i)','(ii)'),'4:2:0'))])
 education=s[27].split(') x2',1)[1].strip();assert education.endswith('etc.') and 'Youthreach' in education
 rows=[]
 for i in range(1,3):
  rows.extend([criterion(f'name-{i}','name',1,[0,2,3],f'Name initiative {i}, graded 3:2:0. '+('The examples are open, not a finite pool. Complete historical guidance: '+education if i==1 else 'Choose a different initiative from the first.')),criterion(f'description-{i}','description',1,[0,2,4],f'Evaluate the same initiative {i} in relation to early school leavers, graded 4:2:0. Use the full historical guidance above; programme names and arrangements may have changed.')])
 put(3,'c','ii',14,'2 initiatives × (name 3 (3:2:0) + detail 4 (4:2:0))',rows)

 put(4,'a','i',20,'5 points × 4 (4:3:2:1:0)',[criterion('nutrition','nutritional significance',5,list(range(5)),'Five developed points, each graded 4:3:2:1:0. The six nutrient headings are examples rather than six required slots. Nutrient amounts and protein quality depend on the vegetable; do not generalise the source’s figures to all vegetables. Complete historical guidance: '+body(between(s[28],'(i)','(ii)'),'4:3:2:1:0'))])
 preservation=s[28].split('(18 marks)',1)[1].strip();packaging=preservation.split('Packaging',1)[1].strip();labels=['Freezing','Bottling','Dehydration','Chutney/Relish','Pickling'];values=named_sections(preservation.split('Packaging',1)[0],labels);routes=[]
 for i,(label,value) in enumerate(zip(labels,values),1):
  assert value.endswith('etc.'),label
  routes.append(dict(id=f'preservation-{i}',label=label,rows=[criterion('name','name of preservation method',1,[0,3],'Name one method suitable for vegetables, graded 3:0. This route: '+label),criterion('principle','underlying principle',3,[0,2,4],'Three points, each graded 4:2:0. '+('Low-acid vegetables require a validated pressure-canning process; a simple boiling-water bath is not sufficient. ' if label=='Bottling' else '')+'These short source examples are not complete preservation recipes. Complete published guidance: '+value),criterion('packaging','suitable packaging',1,[0,2,3],'One packaging point appropriate to the same process, graded 3:2:0. Not every package suits every method. Complete guidance: '+packaging)]))
 routes.append(dict(id='another',label='Another valid preservation method',rows=[criterion('name','name of preservation method',1,[0,3],'Name a valid method suitable for vegetables, graded 3:0.'),criterion('principle','underlying principle',3,[0,2,4],'Three accurate points about the same method, each graded 4:2:0. No model for this alternative is printed.'),criterion('packaging','suitable packaging',1,[0,2,3],'One appropriate packaging point, graded 3:2:0. Complete general examples: '+packaging)]))
 put(4,'a','ii',18,'Name 3 (3:0); principle 3 × 4 (4:2:0); packaging 3 (3:2:0)',deepcopy(routes[0]['rows']),answerVariants=routes)
 irradiation=s[29].split('(graded 4:2:0)',1)[1].split('and 4.(b)',1)[0].strip();assert irradiation.endswith('etc.')
 put(4,'a','iii',12,'3 evaluation points × 4 (4:2:0)',[criterion('evaluation','Evaluate irradiation',3,[0,2,4],'Three points, each graded 4:2:0. No fixed advantages/disadvantages quota is printed. Effects depend on dose and food; do not read the source as a guarantee that any treatment destroys all enzymes or microbes. Complete historical guidance: '+irradiation)])
 coeliac=between(s[29],'(i)','(ii)').split('(15 marks)',1)[1].strip();assert coeliac.endswith('etc.')
 put(4,'b','i',15,'3 guidelines × 5 (5:3:0)',[criterion('diet','dietary guidelines',3,[0,3,5],'Three guidelines, each graded 5:3:0. Complete guidance: '+coeliac)])
 speciality=s[29].split('(ii)',1)[1].split('(15 marks)',1)[1].strip();assert speciality.endswith('etc.')
 put(4,'b','ii',15,'3 points × 5 (5:3:0)',[criterion('speciality','speciality foods',3,[0,3,5],'Three points, each graded 5:3:0. These are reasons for popularity, not guarantees about every business. Complete guidance: '+speciality)])
 kettle=between(s[30],'Kettle','Accept deep fat fryer');construction,principle,use=named_sections(kettle,['Construction –','Working principle -','Guidelines for use –']);others='deep fat fryer'+between(s[30],'Accept deep fat fryer','(ii)');assert others.endswith('etc.')
 rows=[criterion('name','Name of appliance',1,[0,2],'Name the appliance studied, graded 2:0. The paper implies the name; the scheme explicitly allocates two marks. Model: kettle. Other accepted examples: '+others),criterion('construction','construction',3,[0,1,2],'Three construction points, each graded 2:1:0. Complete kettle model: '+construction),criterion('principle','working principle',3,[0,1,2],'Three principle points, each graded 2:1:0. Source clarification: electrical resistance converts electrical energy into heat in the element; conduction transfers heat to adjacent water and convection circulates heated water. Complete historical wording: '+principle),criterion('use','guidelines for use',2,[0,1,2],'Two use guidelines, each graded 2:1:0. Complete kettle model: '+use)]
 otherrows=[criterion('name','Name of appliance',1,[0,2],'Name an appliance with a heating element, graded 2:0. Other accepted examples: '+others),criterion('construction','construction',3,[0,1,2],'Three accurate construction points for that appliance, each graded 2:1:0. No model for this alternative is printed.'),criterion('principle','working principle',3,[0,1,2],'Three accurate principle points for the same appliance, each graded 2:1:0.'),criterion('use','guidelines for use',2,[0,1,2],'Two appropriate guidelines for that appliance, each graded 2:1:0.')]
 put(4,'c','i',18,'Name 2 (2:0); construction 3 × 2; principle 3 × 2; use 2 × 2 (2:1:0)',rows,answerVariants=[dict(id='kettle',label='Kettle',rows=deepcopy(rows)),dict(id='another',label='Another heating-element appliance',rows=otherrows)])
 put(4,'c','ii',12,'3 factors × 4 (4:2:0)',[criterion('factors','factors',3,[0,2,4],'Three factors, each graded 4:2:0. Complete guidance: '+body(s[30].split('(ii)',1)[1],'4:2:0'))])
 assert len(fixes)==29 and sum(f['set']['totalMarks'] for f in fixes.values() if not f.get('drop'))==385
 return fixes,[]


def write():
 fixes,added=build();save_batch('C',fixes,added,dict(tasks=sum(not f.get('drop') for f in fixes.values()),marks=sum(f['set']['totalMarks'] for f in fixes.values() if not f.get('drop')),sourceClarifications=CLARIFICATIONS,selectionDecisions='Required floor-covering headings form one recommendation; the duplicate half becomes a progress alias. Filament modification is one explanation illustrated by two examples. Open profiles and required headings remain whole.',checked='2026-11-01'))
 print('2022 Higher C review written.')


if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
