#!/usr/bin/env python3
"""2024 Ordinary C: all profiles, required headings and two page continuations."""
from copy import deepcopy
import json,re,sys
from he_review_2024_ol_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections
CLARIFICATIONS={
 'winterproofing':dict(source='https://www.water.ie/help/supply/winterproofing',note='Uisce Éireann advises insulating pipes/tanks and keeping the home warm; running taps does not prevent freezing. Distinguish prevention from thawing already frozen pipes.'),
 'milk-temperature':dict(source='https://www.fsai.ie/getmedia/2d516a18-247a-41e4-ab78-93fdd9eb8837/Farmhouse-Cheesemakers-Workbook-FINAL.pdf?ext=.pdf',note='UHT requires at least 135°C with a suitable holding time; pasteurised milk is quickly cooled to no more than 6°C. The source’s 132°C UHT / 10°C cooling examples are inaccurate.')}


def build():
 d=documents();s={n:page_text(d['scheme'],n) for n in range(16,26)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};old=originals();fixes={}
 def put(n,part,roman,marks,notation,rows,suffix='',**extra):
  group=p[n].split(f'{n}.({part})',1)[1]
  if part!='c':group=group.split(f'{n}.({chr(ord(part)+1)})',1)[0]
  if roman:
   if n==4 and part=='a':
    # The milk-account prompt itself contains (i)/(ii); use its printed task boundary.
    token={'i':'(i) Give an account','ii':'(ii) Describe','iii':'(iii) Outline'}[roman]
    assert group.count(token)==1,token
    prompt=token.split(') ',1)[1]+group.split(token,1)[1].split(f'({marks} marks)',1)[0]
   else:prompt=between(group,f'({roman})',f'({marks} marks)')
   stem=group.split('(i)',1)[0].strip()
  else:stem,prompt=group.split('Write a profile',1);prompt='Write a profile'+prompt.split(f'({marks} marks)',1)[0];stem=stem.strip()
  prompt=prompt.replace(' • ','\n• ')
  if not (n==4 and part=='a' and roman=='i'):assert not re.search(r'\((?:i|ii|iii|iv)\)',prompt),prompt
  cid=f'he-2024-ol-sc-q{n}{part}{roman}{suffix}';fixes[cid]=dict(reason='Complete 2024 Ordinary C source review: original prompts, exact partial credit, all profile models and continued guidance.',set=dict(questionText=prompt,questionRef=f'2024 OL Section C '+(f'E{n} ' if n<4 else '')+f'Q{n}({part})'+(f'({roman})' if roman else ''),stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Full source-pinned review: he_review_2024_ol_main_c.py. Required headings and dependent name/details remain whole.',**extra));return cid
 def body(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def points(n,part,roman,marks,count,steps,text,label='points',**extra):
  grade=':'.join(map(str,reversed(steps)));return put(n,part,roman,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete historical guidance: '+text)],**extra)
 def headings(n,part,roman,labels,values,count,steps,note='',**extra):
  grade=':'.join(map(str,reversed(steps)));put(n,part,roman,len(labels)*count*steps[-1],f'{len(labels)} required headings × {count} points × {steps[-1]} ({grade})',[criterion(f'heading-{i}',label,count,steps,f'{count} points under this required heading, each graded {grade}. '+note+'Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)],**extra)
 points(1,'a','i',20,4,[0,3,5],body(16,'4 stages @ 5 marks (graded 5:3:0)','(ii)'),label='stages')
 points(1,'a','ii',15,3,[0,3,5],'Source clarification: Uisce Éireann advises that running taps does not prevent freezing; insulate exposed pipes/tanks and maintain warmth. The historical heat-bulb/dripping-tap examples are not general installation instructions. Prevention is distinct from thawing already frozen pipes. '+body(16,'3 points @ 5 marks (graded 5:3:0)','(iii)'))
 labels=['service pipe','ball valve','storage tank'];heads=['service pipe connects','ball valve controls the level of water in the water tank','storage tank located'];values=named_sections(s[16].rsplit('(15 marks)',1)[1],heads);values=[h[len(label)+1:]+' '+v for h,label,v in zip(heads,labels,values)]
 headings(1,'a','iii',labels,values,1,[0,3,5])
 points(1,'b','i',15,3,[0,3,5],'Historical examination summary, not current planning-law guidance. '+body(17,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 labels=['architect','engineer','solicitor'];heads=['architect advises','engineer provides','solicitor deals'];values=named_sections(s[17].rsplit('(15 marks)',1)[1].removesuffix(' or'),heads);values=[h[len(label)+1:]+' '+v for h,label,v in zip(heads,labels,values)]
 headings(1,'b','ii',labels,values,1,[0,3,5],note='Historical examples of professional roles; individual services and legal requirements vary. ')
 points(1,'c','i',15,3,[0,3,5],body(18,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 ventilation=body(18,'underlying principles 2 points @ 5 marks (graded 5:3:0)')
 put(1,'c','ii',15,'Name 5 + 2 principle points × 5 (5:3:0)',[criterion('name','Name',1,[0,3,5],'Name one kitchen ventilation method, graded 5:3:0. Complete examples for extractor fan, ducted cooker hood, open doors/windows, trickle vents and air vents: '+ventilation),criterion('principle','underlying principles',2,[0,3,5],'Two explanation points for the same chosen method, each graded 5:3:0. The choice is open; name and explanation stay together.')])
 labels=['comfort','function','aesthetic appeal'];values=named_sections(body(19,'(18 marks)','(ii)'),['comfort allows','function suitable','aesthetic appeal stripes']);values=[a+b for a,b in zip(['allows ','suitable ','stripes '],values)];image=dict(questionFigureKey='home-economics-2024-ol-sc-q2a-sportswear',questionFigureIncludesPrompt=False,figureKey='')
 headings(2,'a','i',labels,values,2,[0,2,3],**image)
 emphasis=body(19,'1 point @ 4 marks (graded 4:2:0), 2nd point @ 3 marks (graded 3:2:0)')
 put(2,'a','ii',7,'First point 4 (4:2:0) + second point 3 (3:2:0)',[criterion('first','point',1,[0,2,4],'First emphasis point, graded 4:2:0. Complete guidance: '+emphasis),criterion('second','2nd point',1,[0,2,3],'Second different emphasis point, graded 3:2:0. Use the complete guidance above; both original outfits are retained.')],**image)
 production,properties,tests=named_sections(body(20,'(15 marks)','or 2.(c)'),['fibre production linen','properties linen','test to identify a natural fibre hold']);columns=[]
 for value,heads in [('linen '+production,['linen made','cotton comes','wool fleece','silk silkworms']),('linen '+properties,['linen absorbent','cotton absorbent','wool warm','silk absorbent']),('hold '+tests,['linen takes','cotton flares','wool burns','silk burns'])]:
  columns.append([h.split(' ',1)[1]+' '+v for h,v in zip(heads,named_sections(value,heads))])
 variants=[]
 for i,name in enumerate(['Linen','Cotton','Wool','Silk']):
  variants.append(dict(id=name.lower(),label=name,rows=[criterion('production','fibre production',1,[0,3,5],'One developed production point for '+name+', graded 5:3:0. Naming the fibre has no separate tariff. Complete guidance: '+columns[0][i]),criterion('properties','properties',1,[0,3,5],'One developed property point, graded 5:3:0. Complete historical wording: '+columns[1][i]),criterion('test','test to identify a natural fibre',1,[0,3,5],'One developed identification-test point, graded 5:3:0. Source observations for supervised practical work: hold fabric over a flame proof dish; ignite; etc. '+columns[2][i])]))
 other=deepcopy(variants[0]['rows'])
 for row,note in zip(other,['Give a developed fibre-production account for another valid natural fibre, graded 5:3:0. The choice is open; no other model is printed.','Give a developed property point about the same fibre, graded 5:3:0.','Give a developed identification-test account for the same fibre, graded 5:3:0.']):row['contextNote']=note
 variants.append(dict(id='another',label='Another natural fibre',rows=other))
 put(2,'b','',15,'Production 5 + properties 5 + identification 5 (5:3:0)',deepcopy(variants[0]['rows']),suffix='-linen',answerVariants=variants,conceptId='natural-fibre-profile-ol')
 points(2,'c','i',6,2,[0,2,3],'Interpret current trends in the 2024 examination context. '+body(20,'2 points @ 3 marks (graded 3:2:0)','(ii)'))
 points(2,'c','ii',9,3,[0,2,3],body(20,'3 points @ 3 marks (graded 3:2:0)'))
 labels=['paid work','unpaid work','voluntary work'];heads=['paid work done','unpaid work no','voluntary work involves'];values=named_sections(body(21,'(15 marks)','(ii)'),heads);values=[h[len(label)+1:]+' '+v for h,label,v in zip(heads,labels,values)]
 headings(3,'a','i',labels,values,1,[0,3,5])
 points(3,'a','ii',15,3,[0,3,5],body(21,'3 reasons @ 5 marks (graded 5:3:0)','(iii)'),label='reasons')
 points(3,'a','iii',20,4,[0,3,5],'These are possible effects, not inevitable outcomes or assumptions about any family. '+body(21,'4 points @ 5 marks (graded 5:3:0)').removesuffix(' and'))
 labels=['gender','age','cultural influences'];heads=['gender some','age young','cultural influences in'];values=named_sections(body(22,'(15 marks)','(ii)'),heads);values=[h[len(label)+1:]+' '+v for h,label,v in zip(heads,labels,values)]
 headings(3,'b','i',labels,values,1,[0,3,5],note='Historical examples of influences, not fixed traits or universal age-based activity rules. ')
 points(3,'b','ii',15,3,[0,3,5],body(22,'3 benefits @ 5 marks (graded 5:3:0)','or 3.(c)'),label='benefits')
 text=s[22].rsplit('(15 marks)',1)[1]+' '+s[23].split('(ii)',1)[0].removeprefix('23 ');labels=['improvements in the provision of education','parenting roles within the family','improved conditions at work'];values=named_sections(text,labels)
 headings(3,'c','i',labels,values,1,[0,3,5],note='“Today” refers to the 2024 paper. ')
 points(3,'c','ii',15,3,[0,3,5],body(23,'3 points @ 5 marks (graded 5:3:0)'))
 nutritive,dietetic=named_sections(body(24,'(1 reference to nutritive value, 1 reference to dietetic value, & 2 other points)','(ii) Describe'),['nutritive value','dietetic value'])
 put(4,'a','i',20,'Nutritive 1 + dietetic 1 + other 2, each 5 (5:4:3:2:0)',[criterion('nutritive','nutritive value',1,[0,2,3,4,5],'One nutritive point, graded 5:4:3:2:0. Amounts depend on milk type and fortification. Complete guidance: '+nutritive),criterion('dietetic','dietetic value',1,[0,2,3,4,5],'One dietetic point, graded 5:4:3:2:0. Suitability and digestibility depend on the individual. Complete historical guidance: '+dietetic),criterion('other','other points',2,[0,2,3,4,5],'Two further distinct points under either heading, each graded 5:4:3:2:0.')])
 process=body(24,'(18 marks)','(iii)');models,labelling=process.split('labelling type',1);names=['pasteurisation','sterilisation','ultra-heat treatment (UHT)','condensed milk','evaporated milk'];values=named_sections(models,names);variants=[]
 for name,value in zip(names,values):
  value=re.sub(r'(\d)oC',r'\1°C',value);note=''
  if name=='pasteurisation':note='Source correction: quickly cool pasteurised milk to no more than 6°C; 10°C is not the target. '
  if name=='ultra-heat treatment (UHT)':note='Source correction: UHT requires at least 135°C with a suitable holding time; the printed 132°C is too low. '
  variants.append(dict(id=name.split(' ',1)[0],label=name.title() if name!='ultra-heat treatment (UHT)' else 'UHT',rows=[criterion('name','name of process',1,[0,1,2],'Name the chosen process, graded 2:1:0. This model: '+name),criterion('process','how the process is carried out',4,[0,2,3],'Four points, each graded 3:2:0. '+note+'Historical industrial-process examples, not a validated domestic preservation recipe. Complete source wording: '+value),criterion('labelling','labelling',2,[0,1,2],'Two label points, each graded 2:1:0. Complete guidance: type'+labelling)]))
 other=deepcopy(variants[0]['rows']);other[0]['contextNote']='Name another valid process, graded 2:1:0. The scheme explicitly accepts Spray Drying and Roller Drying, but prints no further model for them.';other[1]['contextNote']='Four accurate process points about the same method, each graded 3:2:0. No additional model is printed; this is not a home-preservation recipe.';variants.append(dict(id='another',label='Another valid process (including spray or roller drying)',rows=other))
 put(4,'a','ii',18,'Name 2 (2:1:0); process 4 × 3 (3:2:0); labelling 2 × 2 (2:1:0)',deepcopy(variants[0]['rows']),suffix='-pasteurisation',answerVariants=variants,conceptId='milk-heat-treatment')
 dairy=body(24,'3 ways @ 4 marks (graded 4:2:0)')+' '+s[25].split('and 4.(b)',1)[0].removeprefix('25 ')
 points(4,'a','iii',12,3,[0,2,4],dairy,label='ways')
 points(4,'b','i',15,3,[0,3,5],body(25,'3 factors @ 5 marks (graded 5:3:0)','(ii)'),label='factors')
 points(4,'b','ii',15,3,[0,3,5],'Follow the manufacturer’s safety instructions; the historical examples are not directions for unqualified electrical repairs. '+body(25,'3 guidelines @ 5 marks (graded 5:3:0)','or 4.(c)'),label='guidelines')
 points(4,'c','i',15,3,[0,3,5],'The source summarises requirements in the historical 2024 examination context; this is not a current legal checklist. '+body(25,'3 points @ 5 marks (graded 5:3:0)','(ii)'))
 points(4,'c','ii',15,3,[0,3,5],'Historical relationship and legal examples, not advice on a particular couple’s legal obligations. '+s[25].rsplit('3 points @ 5 marks (graded 5:3:0)',1)[1].strip())
 assert len(fixes)==26 and sum(f['set']['totalMarks'] for f in fixes.values())==385
 assert all(cid in old for cid in fixes)
 return fixes,[]


def write():
 fixes,added=build();save_batch('C',fixes,added,dict(tasks=26,marks=385,sourceClarifications=CLARIFICATIONS,selectionDecisions='All required headings and dependent profiles remain whole. One natural-fibre profile contains four model routes and another valid choice; one milk-treatment profile contains all five models, spray/roller drying acceptance and an open alternative. Existing withdrawn identities and progress aliases are unchanged. Preserve both original sportswear images on both dependent tasks, the 4+3 emphasis allocation, parenting continuation on page 23 and dairy examples on page 25.',checked='2026-11-01'));print('2024 Ordinary C: 26 reviewed tasks, 385 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
