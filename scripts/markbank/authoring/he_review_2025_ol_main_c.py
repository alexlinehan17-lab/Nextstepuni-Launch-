#!/usr/bin/env python3
"""2025 Ordinary C: complete required headings, dependent profiles and source figures."""
from copy import deepcopy
import json,re,sys
from he_review_2025_ol_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections,source_material
CLARIFICATIONS={'electrical-terms':dict(sources=['https://www.seai.ie/data-and-insights/seai-statistics/conversion-factors','https://www.esbnetworks.ie/safety/safety-tips/home-safety/electrical-installation-safety-features'],note='kWh means kilowatt-hour, an energy unit. MCB overcurrent protection and RCD earth-leakage protection are distinct; an MCB does not inherently contain an RCD.')}

def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(16,24)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};old=originals();fixes={};added=[]
 def put(n,part,roman,marks,notation,rows,suffix='',**extra):
  group=p[n].split(f'{n}.({part})',1)[1]
  if part!='c':group=group.split(f'{n}.({chr(ord(part)+1)})',1)[0]
  # The yoghurt prompt itself contains (i)/(ii): locate the printed task start.
  lead={'i':'Give an account','ii':'In relation','iii':'There is'}[roman] if n==4 and part=='a' else '';token=f'({roman})'+(' '+lead if lead else '')
  assert group.count(token)==1,(n,part,roman,token)
  prompt=(lead+group.split(token,1)[1]).split(f'({marks} marks)',1)[0].strip().replace(' • ','\n• ')
  cid=f'he-2025-ol-sc-q{n}{part}{roman}{suffix}';v=dict(questionText=prompt,questionRef=f'2025 OL Section C '+(f'E{n} ' if n<4 else '')+f'Q{n}({part})({roman})',stem=group.split('(i)',1)[0].strip(),totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,sourceMaterial=source_material(n+4),notes='Full independent paper/scheme review: he_review_2025_ol_main_c.py.');v.update(extra)
  fixes[cid]=dict(reason='2025 Ordinary C full source review: complete prompts and dependent details, exact partial credit and all source guidance.',set=v);return cid
 def body(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip().removesuffix(' and').removesuffix(' or')
 def points(n,part,roman,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return put(n,part,roman,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 def headings(n,part,roman,labels,values,count,steps,notes=None,**extra):
  grade=':'.join(map(str,reversed(steps)));return put(n,part,roman,len(labels)*count*steps[-1],f'{len(labels)} required headings × {count} points × {steps[-1]} ({grade})',[criterion(f'heading-{i}',label,count,steps,f'{count} points under this required heading, each graded {grade}. '+((notes or {}).get(i,''))+'Complete historical guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)],**extra)
 heat=dict(questionFigureKey='home-economics-2025-ol-sc-q1a-heat-loss',questionFigureIncludesPrompt=False,figureKey='')
 points(1,'a','i',20,4,[0,3,5],body(16,'4 methods @ 5 marks (graded 5:3:0)','(ii)'),label='methods',**heat)
 points(1,'a','ii',15,3,[0,3,5],body(16,'3 advantages @ 5 marks (graded 5:3:0)','(iii)'),label='advantages',**heat)
 points(1,'a','iii',15,3,[0,3,5],body(16,'3 practices @ 5 marks (graded 5:3:0)'),label='practices',**heat)
 points(1,'b','i',15,3,[0,3,5],body(17,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 labels=['Miniature circuit breaker','Voltage','Kilowatt per hour (kWh)'];values=named_sections(body(17,'(15 marks) Miniature circuit breaker:','or 1.(c)'),['safety feature;','Voltage:','Kilowatt per hour (kWh):']);values[0]='safety feature; '+values[0]
 headings(1,'b','ii',labels,values,1,[0,3,5],notes={1:'Source clarification: an MCB interrupts overcurrent; an RCD detects leakage. An MCB does not inherently contain an RCD. ',3:'Source correction: the paper says “kilowatt per hour”, but kWh means kilowatt-hour, a unit of ENERGY. One kWh is the energy used at 1 kW for one hour; 1 kW is 1000 W of power. '})
 labels=['Family size and stage','Cost','Comfort'];values=named_sections(body(17,'(15 marks) Family size and stage:','(ii) Explain'),['will influence','Cost:','Comfort:']);values[0]='will influence '+values[0]
 headings(1,'c','i',labels,values,1,[0,3,5])
 cid=put(1,'c','ii',15,'Definition 5 + 2 examples × 5 (5:3:0)',[criterion('texture','texture',1,[0,3,5],'Explain texture, graded 5:3:0. Complete guidance: '+body(17,'1 point on texture @ 5 marks (graded 5:3:0)','2 examples'))])
 original=fixes[cid]['set'];full=original['questionText'];assert ', and give two examples' in full
 original.update(questionText=full.split(', and give two examples',1)[0]+'.',totalMarks=5,tariffModel=dict(kind='fixed',notation='Definition 5 (5:3:0)'))
 c=deepcopy(old[cid]);c.update(original,id=cid+'-examples',conceptId=c['conceptId']+'-examples',questionText='Give two examples'+full.split(', and give two examples',1)[1],questionRef=original['questionRef']+' — examples',totalMarks=10,tariffModel=dict(kind='fixed',notation='2 examples × 5 (5:3:0)'),rows=[criterion('examples','examples',2,[0,3,5],'Two distinct applications of texture, each graded 5:3:0. Complete guidance: '+body(17,'2 examples @ 5 marks (graded 5:3:0)'))]);added.append(c)
 wedding=dict(questionFigureKey='home-economics-2025-ol-sc-q2a-wedding-outfits',questionFigureIncludesPrompt=False,figureKey='')
 labels=['Comfort','Function','Aesthetic appeal'];values=named_sections(body(18,'(18 marks) Comfort:','(ii)'),['flowing fabric','Function:','Aesthetic appeal:']);values[0]='flowing fabric '+values[0]
 headings(2,'a','i',labels,values,2,[0,2,3],**wedding)
 put(2,'a','ii',7,'Accessory 3 (3:0) + reason 4 (4:2:0)',[criterion('accessory','accessory',1,[0,3],'Choose one accessory for one of the original outfits, graded 3:0. Complete examples: '+body(18,'1 reason @ 4 marks (graded 4:2:0)')),criterion('reason','reason',1,[0,2,4],'Explain one reason for the SAME accessory and outfit, graded 4:2:0. The source gives the criterion and partial ladder but no developed model reason.')],**wedding)
 points(2,'b','i',6,2,[0,2,3],body(19,'2 reasons @ 3 marks (graded 3:2:0)','(ii)'),label='reasons')
 names=['waterproofing:','anti-static:','stain resistant:','crease resistant:','mercerising:','flame retardant:'];values=named_sections(body(19,'Example: 3 marks (graded 3:2:0)','or 2.(c)'),names);variants=[]
 for i,(name,value) in enumerate(zip(names,values)):
  desc,example=value.split('e.g.',1);variants.append(dict(id=str(i),label=name[:-1],rows=[criterion('name',name[:-1],1,[0,2,3],'Name this finish, graded 3:2:0.'),criterion('description',desc.strip(),1,[0,2,3],'Describe the SAME finish, graded 3:2:0.'),criterion('example',example.strip(),1,[0,2,3],'Give a use of the SAME finish, graded 3:2:0.')]))
 variants.append(dict(id='another',label='Another valid finish',rows=[criterion('name','Name',1,[0,2,3],'Name another valid finish, graded 3:2:0. The choice is open.'),criterion('description','Description',1,[0,2,3],'Describe that same finish accurately, graded 3:2:0. No further model is printed.'),criterion('example','Example',1,[0,2,3],'Give a matching textile use, graded 3:2:0.')]))
 put(2,'b','ii',9,'Name 3 + description 3 + example 3 (3:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(2,'c','i',9,3,[0,2,3],body(19,'3 factors @ 3 marks (graded 3:2:0)','(ii)'),label='factors')
 points(2,'c','ii',6,2,[0,2,3],body(19,'2 points @ 3 marks (graded 3:2:0)'))
 labels=['Age range of primary school children','Choice / types of primary schools','Curriculum offered'];values=named_sections(body(20,'(20 marks)','(ii)'),[x+':' for x in labels]);rows=[criterion(str(i),label,1,[0,3,5],'One point under this required heading, graded 5:3:0. Historical 2025 examination context. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)]
 rows.append(criterion('other','other point',1,[0,3,5],'One further distinct point under any of the three headings, graded 5:3:0.'))
 classroom=dict(questionFigureKey='home-economics-2025-ol-sc-q3a-classroom',questionFigureIncludesPrompt=False,figureKey='')
 put(3,'a','i',20,'3 required headings × 5 + other point 5 (5:3:0)',rows,**classroom)
 put(3,'a','ii',15,'Name 5 + 2 details × 5 (5:3:0)',[criterion('name','Name',1,[0,3,5],'Name one initiative, graded 5:3:0. All printed examples: '+body(20,'Name: 5 marks (graded 5:3:0), 2 details @ 5 marks (graded 5:3:0)','(iii)')),criterion('details','details',2,[0,3,5],'Give two accurate details of the SAME initiative supporting school attendance, each graded 5:3:0. The scheme publishes this criterion and ladder but no developed details; the name alone earns at most five marks.')],suffix='-name',**classroom)
 social,physical=named_sections(body(20,'1 reference to social, 1 reference to physical, + 1 other point'),['social:','physical:'])
 put(3,'a','iii',15,'Social 5 + physical 5 + other 5 (5:3:0)',[criterion('social','social',1,[0,3,5],'One social-development point, graded 5:3:0. Complete guidance: '+social),criterion('physical','physical',1,[0,3,5],'One physical-development point, graded 5:3:0. Complete guidance: '+physical),criterion('other','other point',1,[0,3,5],'One further distinct point from either heading, graded 5:3:0.')],**classroom)
 points(3,'b','i',15,3,[0,3,5],body(21,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 put(3,'b','ii',15,'Name 5 + 2 details × 5 (5:3:0)',[criterion('name','Name',1,[0,3,5],'Name one support, graded 5:3:0. Historical 2025 examples: '+body(21,'Name: 1 @ 5 marks (graded 5:3:0), 2 details @ 5 marks (graded 5:3:0)','or 3.(c)')),criterion('details','details',2,[0,3,5],'Give two accurate details of the SAME support, each graded 5:3:0. The scheme prints this criterion and ladder but no developed details; naming alone earns at most five marks.')],suffix='-name')
 points(3,'c','i',15,3,[0,3,5],body(21,'3 reasons @ 5 marks (graded 5:3:0)','(ii)'),label='reasons')
 points(3,'c','ii',15,3,[0,3,5],'These are possible effects, not inevitable outcomes for a particular family. '+body(21,'3 effects @ 5 marks (graded 5:3:0)'),label='effects')
 nutrition,diet=named_sections(body(22,'(1 reference to nutritive value, 1 reference to dietetic value, + 2 other points)','(ii) In relation'),['Nutritive value','Dietetic value']);yoghurt=dict(questionFigureKey='home-economics-2025-ol-sc-q4a-yoghurt',questionFigureIncludesPrompt=False,figureKey='')
 put(4,'a','i',20,'Nutritive 1 + dietetic 1 + other 2, each 5 (5:4:3:2:0)',[criterion('nutritive','Nutritive value',1,[0,2,3,4,5],'One nutritive point, graded 5:4:3:2:0. Amounts depend on product composition and fortification. Complete guidance: '+nutrition),criterion('dietetic','Dietetic value',1,[0,2,3,4,5],'One dietetic point, graded 5:4:3:2:0. Suitability depends on the individual and product. Complete guidance: '+diet),criterion('other','other points',2,[0,2,3,4,5],'Two further distinct points from either heading, each graded 5:4:3:2:0.')],**yoghurt)
 labels=['Culinary uses','Guidelines for buying','Guidelines for storing'];values=named_sections(body(22,'(18 marks)','(iii)'),[x+':' for x in labels]);headings(4,'a','ii',labels,values,2,[0,2,3],**yoghurt)
 points(4,'a','iii',12,3,[0,2,4],body(22,'3 reasons @ 4 marks (graded 4:2:0)'),label='reasons',**yoghurt)
 points(4,'b','i',15,3,[0,3,5],body(23,'3 reasons @ 5 marks (graded 5:3:0)','(ii)'),label='reasons')
 put(4,'b','ii',15,'Name 3 + 2 details × 3 + 2 reasons × 3 (3:2:0)',[criterion('name','Name',1,[0,2,3],'Name one saving scheme, graded 3:2:0. Complete historical examples: '+body(23,'Details 2 points @ 3 marks (graded 3:2:0)','2 reasons @ 3')),criterion('details','Details',2,[0,2,3],'Give two accurate details of the SAME saving scheme, each graded 3:2:0. The scheme prints this criterion and ladder but no developed details; do not omit these six marks.'),criterion('reasons','reasons',2,[0,2,3],'Give two reasons for choosing that same scheme, each graded 3:2:0. Historical examination context; terms vary by product. Complete guidance: '+body(23,'2 reasons @ 3 marks (graded 3:2:0)','or 4.(c)'))],suffix='-name-reasons')
 points(4,'c','i',15,3,[0,3,5],body(23,'3 ways @ 5 marks (graded 5:3:0)','(ii)'),label='ways')
 points(4,'c','ii',15,3,[0,3,5],s[23].rsplit('3 ways @ 5 marks (graded 5:3:0)',1)[1].strip(),label='ways')
 assert len(fixes)==27 and len(added)==1 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==385
 assert all(cid in old for cid in fixes)
 return fixes,added

def write():
 fixes,added=build();save_batch('C',fixes,added,dict(tasks=28,marks=385,selectionDecisions='Separate texture definition and application prompts at their 5/10 tariffs. Restore accessory reason, attendance-initiative details, family-support details and saving-scheme details inside existing dependent task IDs. Required headings retain exact quotas. Fabric finish has six source models and one open alternative. All original figures and their captions carried.',sourceClarifications=CLARIFICATIONS,checked='2026-11-06'));print('2025 Ordinary C: 28 tasks, 385 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
