#!/usr/bin/env python3
"""Complete B guidance, restore the whole mould profile and split the will task."""
from copy import deepcopy
import json
import re
import sys
from he_review_2022_hl_main import ROOT, documents, page_text, originals, save_batch, criterion, between, named_sections

CLARIFICATIONS={
 'tooth-decay':dict(source='https://www.nidcr.nih.gov/health-info/tooth-decay',note='Tooth decay is driven by acids produced by oral bacteria acting on sugars/starches, not simply vitamin D deficiency.'),
 'vitamin-d-stability':dict(source='https://pubmed.ncbi.nlm.nih.gov/24262542/',note='Vitamin D retention varies with food and processing conditions; the source’s absolute claim that it is unaffected by cooking is inaccurate.'),
 'marriage-notification':dict(source='https://www2.hse.ie/services/births-deaths-and-marriages/getting-married/how/',note='Notification goes to the civil registration service for religious as well as civil/secular marriages, not solely to a church.'),
 'marriage-age':dict(source='https://www.irishstatutebook.ie/eli/2018/act/6/enacted/en/print',note='Minimum age is 18, not strictly over 18; previous age-exemption provisions were repealed.'),
 'mould':dict(source='https://fsistraining.fsis.usda.gov/pluginfile.php/18440/mod_resource/content/1/TPSP%20Student%20Guide%20Edits12092021.pdf',note='Growth and heat-resistance conditions vary by organism and food; source temperatures/timings are historical examples, not validated universal safety limits.'),
}


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]}
 s={n:page_text(d['scheme'],n) for n in range(11,18)};fixes={};added=[];old=originals()
 def put(n,part,marks,notation,rows,**extra):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' \uf0b7 ','\n• ');assert not re.search(r'\([a-d]\)',prompt)
  stem=q[n].split('(a)',1)[0].strip()
  cid=f'he-2022-hl-sb-q{n}{part}'+('-conditions' if (n,part)==(3,'b') else '')
  fixes[cid]=dict(reason='Complete 2022 Higher B source review; whole open profiles and exact partial-credit tariffs.',set=dict(questionText=prompt,questionRef=f'2022 HL Section B Q{n}({part})',stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Paper and complete scheme independently reviewed: he_review_2022_hl_main_b.py.',**extra))
 def body(text,grade):
  value=text.split(f'(graded {grade})',1)[1].strip();assert value.endswith('etc.'),value;return value
 put(1,'a',20,'4 comment/elaboration points × 5 (5:4:3:2:1:0)',[criterion('factors','factors',4,list(range(6)),'Use the chart and develop four points, each graded 5:4:3:2:1:0. All six printed factors remain available; this is one open response. Complete guidance: '+body(s[11],'5:4:3:2:1:0'))],questionFigureKey='home-economics-2022-hl-sb-q1a-chart',questionFigureIncludesPrompt=False,figureKey='')
 put(1,'b',20,'4 points × 5 (5:3:0)',[criterion('measures','dietary measures',4,[0,3,5],'Four developed measures, each graded 5:3:0. Complete guidance: '+body(s[12].split('(c)',1)[0],'5:3:0'))])
 vit=between(s[12],'(c)','(d)');functions,deficiency,properties=named_sections(vit,['Biological functions','Effects of deficiency','Properties'])
 put(1,'c',20,'Functions 4 × 2; deficiency 3 × 2; properties 3 × 2 (all 2:0)',[
  criterion('functions','Biological functions',4,[0,2],'Four functions, each graded 2:0. Complete guidance: '+body(functions,'2:0')),
  criterion('deficiency','Effects of deficiency',3,[0,2],'Three effects, each graded 2:0. Source clarification: tooth decay involves acids from oral bacteria acting on sugars/starches, not simply vitamin D deficiency. Complete historical guidance: '+body(deficiency,'2:0')),
  criterion('properties','Properties',3,[0,2],'Three properties, each graded 2:0. Source correction: stability depends on the food and processing conditions; vitamin D is not universally unaffected by heat or oxidation. Complete historical wording: '+body(properties,'2:0'))])
 put(1,'d',20,'5 points × 4 (4:2:0)',[criterion('health','health status',5,[0,2,4],'Five points, each graded 4:2:0. Complete guidance: '+body(s[12].split('(d)',1)[1],'4:2:0'))])
 nutrients=between(s[13],'Protein include','(b)');nutrients='Protein include '+nutrients
 rows=[]
 for i in range(1,4):
  rows.extend([criterion(f'nutrient-{i}','name nutrient',1,[0,2],f'Nutrient {i} you choose, graded 2:0. '+('The five model nutrients are illustrative, not a finite selection pool. Complete guidance: '+nutrients if i==1 else 'Use a different nutrient from the other slots.')),criterion(f'strategy-{i}','strategy',1,[0,2,4],f'A strategy preventing deficiency of your nutrient {i}, graded 4:2:0. Keep each named nutrient and its strategy paired.')])
 put(2,'a',18,'3 nutrient/strategy pairs × (2 (2:0) + 4 (4:2:0))',rows)
 manufacture=s[13].split('stages in manufacture 6 points @ 3 marks (graded 3:2:0)',1)[1].strip();labels=['Textured Vegetable Protein','Mycoprotein','Tofu','Soya milk','Soya yoghurt','Tempeh','Miso'];values=named_sections(manufacture,labels);routes=[]
 for i,(name,value) in enumerate(zip(labels,values),1):
  assert value.endswith('etc.'),name
  routes.append(dict(id=f'food-{i}',label=name,rows=[criterion('name','name',1,[0,2],'Name the alternative protein food, graded 2:0. This route: '+name),criterion('manufacture','stages in manufacture',6,[0,2,3],'Six stages for that food, each graded 3:2:0. Complete published process: '+value)]))
 routes.append(dict(id='another',label='Another valid protein food',rows=[criterion('name','name',1,[0,2],'Name one alternative protein food, graded 2:0. The paper leaves this choice open.'),criterion('manufacture','stages in manufacture',6,[0,2,3],'Six accurate stages for the same chosen food, each graded 3:2:0. The source prints seven model processes, not an exhaustive list.')]))
 put(2,'b',20,'Name 2 (2:0) + manufacture 6 × 3 (3:2:0)',deepcopy(routes[0]['rows']),answerVariants=routes)
 put(2,'c',12,'3 points × 4 (4:2:0)',[criterion('protection','protects the consumer',3,[0,2,4],'Three points, each graded 4:2:0. Complete historical examination guidance, including the continuation on scheme page 14: '+body(s[14],'4:2:0'))])
 put(3,'a',15,'3 points × 5 (5:3:0)',[criterion('enzymes','enzymes',3,[0,3,5],'Three points, each graded 5:3:0. Complete guidance: '+body(between(s[15],'(a)','(b)'),'5:3:0'))])
 mould=between(s[15],'(b)','(c)');characteristics=between(mould,'Name Characteristics','Conditions necessary for growth');conditions=mould.split('Conditions necessary for growth',1)[1].strip();labels=['Mucor','Rhizopus','Penicillium','Aspergillus'];values=named_sections(characteristics,labels);routes=[]
 for i,(name,value) in enumerate(zip(labels,values),1):
  assert value.endswith('etc.'),name
  routes.append(dict(id=f'mould-{i}',label=name,rows=[criterion('name','Name',1,[0,2],'Name one mould, graded 2:0. This route: '+name),criterion('characteristics','Characteristics',3,[0,3],'Three characteristics of that mould, each graded 3:0. Temperatures are source examples; species and conditions vary. Complete published description: '+value),criterion('conditions','conditions necessary for growth',4,[0,1,2,3],'Four conditions relevant to that mould, each graded 3:2:1:0. Growth and heat-resistance vary by species and food; these historical examples are not universal safety limits. Complete guidance: '+conditions)]))
 routes.append(dict(id='another',label='Another valid mould',rows=[criterion('name','Name',1,[0,2],'Name one valid mould, graded 2:0. The paper does not limit the choice to four examples.'),criterion('characteristics','Characteristics',3,[0,3],'Three accurate characteristics of your chosen mould, each graded 3:0. No model description for another mould is printed.'),criterion('conditions','conditions necessary for growth',4,[0,1,2,3],'Four relevant conditions, each graded 3:2:1:0. Apply the general guidance appropriately to the mould chosen: '+conditions)]))
 put(3,'b',23,'Name 2 (2:0); characteristics 3 × 3 (3:0); conditions 4 × 3 (3:2:1:0)',deepcopy(routes[0]['rows']),answerVariants=routes)
 put(3,'c',12,'3 points × 4 (4:3:2:1:0)',[criterion('uses','uses of micro-organisms',3,list(range(5)),'Three uses, each graded 4:3:2:1:0. Complete guidance: '+body(s[15].split('(c)',1)[1],'4:3:2:1:0'))])
 put(4,'a',16,'4 factors × 4 (4:2:0)',[criterion('factors','factors',4,[0,2,4],'Four factors, each graded 4:2:0. Complete guidance: '+body(between(s[16],'(a)','(b)'),'4:2:0'))])
 put(4,'b',24,'4 conditions × 6 (6:4:2:0)',[criterion('conditions','conditions',4,[0,2,4,6],'Four conditions, each graded 6:4:2:0. Historical 2022 scheme: income multiples and documents are not presented as current lending requirements. Complete wording: '+between(s[16],'(grade 6:4:2:0)','(c)'))])
 put(4,'c',10,'2 points × 5 (5:3:0)',[criterion('services','consumers are protected',2,[0,3,5],'Two points, each graded 5:3:0. Historical question on the named 1980 Act, not a statement of all current consumer law. Complete guidance: '+body(s[16].split('(c)',1)[1],'5:3:0'))])
 put(5,'a',16,'4 points × 4 (4:2:0)',[criterion('marriage','legal obligations',4,[0,2,4],'Four points, each graded 4:2:0. Source corrections: minimum age is 18 (not strictly over 18); notify the civil registration service for religious as well as civil/secular marriages. Capacity is assessed for the decision and must not be inferred from a diagnosis alone. Complete historical wording: '+body(between(s[17],'(a)','(b)'),'4:2:0'))])
 put(5,'b',20,'5 points × 4 (4:2:0)',[criterion('roles','changing roles',5,[0,2,4],'Five points, each graded 4:2:0. Complete guidance: '+body(between(s[17],'(b)','(c)'),'4:2:0'))])
 why,procedure=named_sections(s[17].split('(graded 2:1:0)',1)[1],['Why','Procedure']);assert why.endswith('etc.') and procedure.endswith('etc.')
 put(5,'c',14,'Why 2 × 2 (2:0) + procedure 5 × 2 (2:1:0)',[])
 fixes['he-2022-hl-sb-q5c']['set'].update(topicId='home-economics-2-1',questionText='State why it is important to make a will.',questionRef='2022 HL Section B Q5(c) — importance',totalMarks=4,tariffModel=dict(kind='fixed',notation='2 reasons × 2 (2:0)'),rows=[criterion('why','why',2,[0,2],'Two reasons, each graded 2:0. Historical examination guidance: '+why)])
 c=deepcopy(old['he-2022-hl-sb-q5c']);c.update(id='he-2022-hl-sb-q5c-procedure',conceptId='making-a-will-procedure',questionText='Outline the procedure involved in making a will.',questionRef='2022 HL Section B Q5(c) — procedure',stem=q[5].split('(a)',1)[0].strip(),totalMarks=10,tariffModel=dict(kind='fixed',notation='5 steps × 2 (2:1:0)'),rows=[criterion('procedure','Procedure',5,[0,1,2],'Five steps, each graded 2:1:0. Historical examination guidance: '+procedure)],notes='Independently practicable procedure prompt; reasons retain the original Q5(c) ID.');added.append(c)
 c['topicId']='home-economics-2-1'
 assert len(fixes)==16 and len(added)==1
 return fixes,added


def write():
 fixes,added=build();save_batch('B',fixes,added,dict(tasks=17,marks=280,sourceClarifications=CLARIFICATIONS,selectionDecisions='B1 chart is one open four-point response. Required vitamin headings stay together. Vegan diet uses three open paired nutrient/strategy slots. Alternative protein food and mould are whole open profiles, with every published model route and a further valid choice. B5(c) has two independent prompts and tariffs; reasons/procedure split. The existing mould ID retains progress while recovering all eleven omitted name/characteristic marks.',checked='2026-11-01'))
 print('2022 Higher B: 17 reviewed tasks, all 280 offered marks.')


if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
