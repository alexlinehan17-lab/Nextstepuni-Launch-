#!/usr/bin/env python3
"""2012 Higher C: original elective choices and source-specific marking."""
from copy import deepcopy
from he_review_2012_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,20)};cards=[]
 p={n:re.sub(r'\(([abc])\s+\)',r'(\1)',v) for n,v in p.items()}
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter)
  if roman:prompt=select(v,f'({roman})');prompt=re.split(r'\((?:i|ii|iii)\)',prompt,1)[0];stem=v.split('(i)',1)[0].strip()
  else:prompt=v;stem=''
  prompt=re.sub(r'\s*\(\d+\)\s*$','',prompt).strip().replace('\uf0b7','•')
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt,stem,marks,rows,n+8,notation,**extra)
  if n==3 and letter=='a':
   c['stem']=c['stem'].split('2006',1)[0].strip();c.update(questionFigureKey='home-economics-2012-hl-sc-q3-unemployment',questionFigureIncludesPrompt=False)
  cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):
  return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Distinct points at the published value; no finer partial-credit steps are printed. Complete source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','i','3-5',4,4,'factors',guide(14,'4 points @ 4 marks each','(ii)'))
 fuel=guide(14,'Fuel / energy source -','Working Principle');principles=guide(14,'Working Principle','Impact on the environment -');impact=guide(14,'Impact on the environment -','(iii)');heads=['Wet system/small bore system/indirect system –','Dry system/under floor heating/storage heating –','Solar heating –'];variants=[]
 for i,(label,body) in enumerate(zip(heads,named(principles,heads)),1):
  name=label[:-2];variants.append(dict(id=f'source-{i}',label=name,rows=[point('name',name,4),criterion('fuel','fuel/energy source',1,[0,4],'Name a fuel for the SAME system. Source examples: '+fuel),criterion('principle','working principle',3,[0,4],'Three points including heat transfer for the SAME system. Source: '+body),criterion('impact','impact on the environment',1,[0,4],'Match the impact to the SAME system. Source examples: '+impact)]))
 variants.append(dict(id='another-system',label='Another valid system',rows=[criterion('name','Naming system',1,[0,4],'One central heating system. The source provides wet, dry and solar examples.'),criterion('fuel','fuel/energy source',1,[0,4],'A fuel for the SAME system. Source examples: '+fuel),criterion('principle','working principle',3,[0,4],'Three principle points including heat transfer for the SAME system. No additional model is printed.'),criterion('impact','impact on the environment',1,[0,4],'One matching environmental impact. Source examples: '+impact)]))
 add(1,'a','ii','3-5',24,deepcopy(variants[0]['rows']),'Name 4 + fuel 4 + principle 3 × 4 + impact 4',answerVariants=variants)
 judged(1,'a','iii','3-5',2,5,'thermal comfort',guide(14,'2 points @ 5 marks each'))
 judged(1,'b','i','3-5',3,5,'ventilation',guide(15,'3 points @ 5 marks each','(ii)'))
 ventilation=re.sub(r'\s+or$','',guide(15,'Working principle: 3 points @ 4 marks each','1.(c)'));extractor=select(ventilation,'Extractor fans –','Cooker hoods –',True);hood=select(ventilation,'Cooker hoods –','Working Principle Ducted',True);ducted=select(ventilation,'Working Principle Ducted','Working Principle Ductless',True);ductless=select(ventilation,'Working Principle Ductless',include=True);variants=[]
 for i,(label,body) in enumerate([('Extractor fans',extractor),('Cooker hoods — ducted',hood+' '+ducted),('Cooker hoods — ductless',hood+' '+ductless)],1):
  name='Extractor fans' if i==1 else 'Cooker hoods';variants.append(dict(id=f'source-{i}',label=label,rows=[point('name',name,3),criterion('principle','Working principle',3,[0,4],'Three points for the SAME method. Full source: '+body)]))
 variants.append(dict(id='another-method',label='Another valid method',rows=[criterion('name','Name method',1,[0,3],'One artificial ventilation method suitable for a kitchen.'),criterion('principle','Working principle',3,[0,4],'Three matching principle points. The source models extractor fans and ducted/ductless cooker hoods; no other model is printed.')]))
 add(1,'b','ii','3-5',15,deepcopy(variants[0]['rows']),'Name 3 + principle 3 × 4',answerVariants=variants)
 interior=guide(15,'One reference to each heading+ 3 other points');heads=['Function –','Cost –','Environmental awareness –'];bodies=named(interior,heads);rows=[criterion(f'heading-{i}',label[:-2],1,[0,3],'One reference to this required heading. Source: '+body) for i,(label,body) in enumerate(zip(heads,bodies),1)];rows.append(criterion('other-points','other points',3,[0,3],'Three ADDITIONAL points across the required headings; no per-heading quota for these three. Full source: '+interior));add(1,'c','i','3-4',18,rows,'1 reference per heading × 3 + 3 other points × 3')
 elements=guide(16,'Elements – colour, pattern, texture');rows=[];groups=[]
 for i in [1,2]:
  rows.extend([criterion(f'explanation-{i}','Explanation',1,[0,3],'Choose a different element in each pair. Source: '+elements),criterion(f'application-{i}','Application',1,[0,3],'One application of that SAME element. Source: '+elements)]);groups.append(dict(sourceCardId=f'he-2012-hl-sc-q1cii-pair-{i}',label=f'Design element {i}',marks=6,rowIds=[f'explanation-{i}',f'application-{i}']))
 add(1,'c','ii','3-4',12,rows,'2 pairs × (explanation 3 + application 3)',taskGroups=groups)
 judged(2,'a','i','3-8',5,3,'socio-economic influences',guide(17,'5 points @ 3 marks each','(ii)'))
 outfit=guide(17,'Large jewellery','Sketch –',);outfit='Large jewellery'+outfit
 add(2,'a','ii','3-8',10,[criterion('sketch','Sketch',1,[0,6],'An outfit for the printed 1980’s birthday-party theme. The source supplies clothing examples but no model drawing. Source: '+outfit),criterion('description','Description',2,[0,2],'Describe the SAME sketched outfit. Source examples: '+outfit)],'Sketch 6 + description 2 × 2')
 blended=select(s[17],'2.(b)','2.(c)');why=select(blended,'2 points @ 3 marks each','(ii)');judged(2,'b','i','3-7',2,3,'blended fabrics',why)
 model=re.sub(r'\s+or$','',select(blended,'Name –',include=True));props=select(model,'Properties –','Uses –');uses=select(model,'Uses –');variants=[dict(id='polycotton',label='polyester cotton (polycotton)',rows=[point('name',select(model,'Name –','Properties –'),3),criterion('properties','properties',3,[0,1],'Three properties of this SAME fabric. Source: '+props),criterion('uses','uses',3,[0,1],'Three uses of this SAME fabric. Source: '+uses)]),dict(id='another-blend',label='Another blended fabric',rows=[criterion('name','name',1,[0,3],'Name ONE blended fabric you studied. The source models polyester cotton only.'),criterion('properties','properties',3,[0,1],'Three properties of that SAME blend. No further model is printed.'),criterion('uses','uses',3,[0,1],'Three uses of that SAME blend. No further model is printed.')])]
 add(2,'b','ii','3-7',9,deepcopy(variants[0]['rows']),'Name 3 + properties 3 × 1 + uses 3 × 1',answerVariants=variants)
 methods=guide(17,'3 @ 5 marks each (name+description)');heads=['Fabric construction –','Colour application –','Design application –'];stem,asks=part(2,'c').split('In relation to textile manufacture, name and describe each of the following:',1);asks=re.sub(r'\s*\(15\)\s*$','',asks).replace('\uf0b7','•').split('• ')[1:]
 for key,ask,head,body in zip(['construction','colour','design'],asks,heads,named(methods,heads)):
  c=add(2,'c',None,'3-7',5,[criterion('name-description',head[:-2],1,[0,5],'Name AND describe one matching technique. Five marks cover the complete response; no name/description sub-allocation is printed. The scheme lists names but supplies no model descriptions. Original source options: '+body)],'Name + description 5');c.update(id=f'he-2012-hl-sc-q2c-{key}',questionRef=f'2012 HL Section C E2 Q2(c) — {head[:-2]}',questionText='In relation to textile manufacture, name and describe each of the following: • '+ask.strip(),stem=stem.strip())
 unemployment=guide(18,'One point to refer to the chart','(ii)');anomaly='Original paper table: 2010 is 13.7%; the scheme repeats 13.6%. Use the paper’s original 13.7%. The prose states 14.4% for October 2011 while the table gives 14.2%; both original values remain visible.'
 add(3,'a','i','3-9',20,[criterion('chart-reference','One point to refer to the chart',1,[0,5],anomaly+' Source: '+unemployment),criterion('discussion','unemployment in Ireland',3,[0,5],'Three further discussion points. Complete historical source: '+unemployment)],'1 chart point × 5 + 3 discussion points × 5')
 impacts=guide(18,'One reference to each heading + one other point')+' '+select(s[19],'Demand for products / services –','(iii)',True);heads=['Geographical location –','Global economy –','Demand for products / services –'];rows=[criterion(f'heading-{i}',head[:-2],1,[0,5],'One point on this required heading. Source: '+body) for i,(head,body) in enumerate(zip(heads,named(impacts,heads)),1)];rows.append(criterion('other-point','one other point',1,[0,5],'One ADDITIONAL point across the three headings. Source: '+impacts));add(3,'a','ii','3-9',20,rows,'1 reference per heading × 5 + 1 other point × 5')
 statutory=re.sub(r'\s+and$','',guide(19,'Details = 5 marks','3.(b)'));names=chosen(statutory,['Enterprise Ireland','County Enterprise Board','FÁS/ Solas','Forfás','IDA','Low corporation tax','JobBridge']);add(3,'a','iii','3-9',10,[menu('name','Name',1,5,names),criterion('details','Details',1,[0,5],'Details of that SAME statutory response. Original historical source: '+statutory)],'Name 5 + matching details 5')
 leisure=select(s[19],'3.(b)','3.(c)');definition=select(leisure,'Leisure is','Value –',True);value=select(leisure,'Value –','(ii)');whole=select(part(3,'b'),'(i)','(ii)');before,after=whole.split(' and ',1)
 c=add(3,'b','i','3-11',6,[point('definition',definition,6,'The source gives six marks for the definition, without smaller steps.')],'Definition 6');c.update(id='he-2012-hl-sc-q3bi-definition',questionRef='2012 HL Section C E3 Q3(b)(i) — definition',questionText=before)
 c=add(3,'b','i','3-11',12,[criterion('discussion','value',3,[0,4],value)],'Discussion 3 × 4');c.update(id='he-2012-hl-sc-q3bi-value',questionRef='2012 HL Section C E3 Q3(b)(i) — value',questionText=re.sub(r'\s*\(18\)\s*$','',after).strip());c['stem']+='\n\n'+before
 choice=re.sub(r'\s+or$','',select(select(leisure,'(ii)'),'3 points @ 4 marks each'));judged(3,'b','ii','3-11',3,4,'factors',choice)
 childcare=select(s[19],'3.(c)');judged(3,'c','i','3-11',3,4,'requirements for childcare',select(childcare,'3 points @ 4 marks each','(ii)'))
 options=select(childcare,'e.g.','evaluative statement');evaluation=select(childcare,'evaluative statement',include=True);rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'name-{i}','Name',1,3,semis(options),'Choose two DIFFERENT childcare types.'),criterion(f'evaluation-{i}','evaluative statement',2,[0,3],'Two evaluations of the SAME childcare type. The source requires advantages/disadvantages but provides no model evaluations. Source wording: '+evaluation)]);groups.append(dict(sourceCardId=f'he-2012-hl-sc-q3cii-option-{i}',label=f'Childcare type {i}',marks=9,rowIds=[f'name-{i}',f'evaluation-{i}']))
 add(3,'c','ii','3-11',18,rows,'2 types × (name 3 + 2 evaluation points × 3)',taskGroups=groups)
 assert len(cards)==22 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=22,marks=275,selectionDecisions='C2(c) three independently required techniques at5 each; C3(b)(i) definition6/value12 independent. Full chosen profiles and printed flexible heading quotas preserved. Paper/scheme unemployment discrepancy visible. Named technique/childcare examples retained while missing model descriptions/evaluations explicitly identified.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
