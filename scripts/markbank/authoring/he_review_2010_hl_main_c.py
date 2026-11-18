#!/usr/bin/env python3
"""2010 Higher C: original elective tasks, open choices and exact tariffs."""
import json,re,sys
from copy import deepcopy
from he_review_2010_hl_main import *

def build():
 d=documents();p={n:text(d['paper'],n+8) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(13,20)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);prompt=select(v,f'({roman})') if roman else v
  prompt=re.split(r'\((?:i|ii|iii)\)',prompt,1)[0] if roman else prompt
  prompt=re.sub(r'\s*\(\d+\)\s*$','',prompt).strip().replace('\uf0b7','•')
  stem=v.split('(i)',1)[0].strip() if '(i)' in v else ''
  if not stem and letter!='a':stem=part(n,'a').split('(i)',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt,stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(n,token,end=None):return select(s[n],token,end)
 def judged(n,letter,roman,topic,count,per,word,guidance,**extra):
  return add(n,letter,roman,topic,count*per,[criterion('points',word,count,[0,per],'Use distinct relevant points at the source’s printed value. No finer partial-credit ladder is printed. Complete source guidance: '+guidance)],f'{count} points @ {per} marks each',**extra)
 def pool(n,letter,roman,topic,count,per,options,**extra):
  return add(n,letter,roman,topic,count*per,[menu('points','Published answer points',count,per,options)],f'{count} points @ {per} marks each',**extra)
 principles=guide(13,'3 points @ 6 marks each','(ii)');pool(1,'a','i','3-4',3,6,named(principles,['Proportion –','Emphasis –','Balance –','Rhythm –']))
 interiors=guide(13,'5 points @ 4 marks each','(iii)');judged(1,'a','ii','3-4',5,4,'factors',interiors)
 fabric=guide(13,'3 marks for type of fabric, reasons 3 @ 3marks each');fabric=re.sub(r'\s+and$','',fabric);names=select(fabric,'Fabrics –','Reasons –');reasons=select(fabric,'Reasons –')
 add(1,'a','iii','3-4',12,[menu('fabric','Fabrics',1,3,[x.strip() for x in re.sub(r'\s*etc\.?$','',names).split(',') if x.strip()]),criterion('reasons','Reasons',3,[0,3],'Three reasons for the same fabric and purpose. Complete source examples: '+reasons)],'Fabric 3 + reasons 3 × 3')
 processes=guide(14,'5 points @ 3 marks each','(ii)');pool(1,'b','i','3-5',5,3,named(processes,['Screening –','Sedimentation –','Filtration –','Chlorination –','Fluoridation –','Softening –','Testing –']))
 water=guide(14,'3 points @ 5 marks each',' or 1.(c)');add(1,'b','ii','3-5',15,[point(f'part-{i}',v,5) for i,v in enumerate(named(water,['Stop cock –','Ball valve –','Overflow pipe –']),1)],'3 required points @ 5 marks each')
 judged(1,'c','i','3-3',3,6,'housing provision',guide(14,'3 points @ 6 marks each'))
 housing=guide(15,'Details – 2 points @ 4 marks each');variants=[]
 labels=['Local authority housing','Tenant purchase scheme','Shared ownership scheme','Mortgage allowance scheme','Affordable housing scheme','Voluntary housing','Co-operative housing']
 for label,body in zip(labels,named(housing,[x+' –' for x in labels])):
  actual_name=body.split(' –',1)[0];details=body.split(' –',1)[1].strip()
  variants.append(dict(id=re.sub(r'[^a-z]+','-',label.lower()),label=actual_name,rows=[point('name',actual_name,4),criterion('details','Details',2,[0,4],'Two details about this same form of social housing. Complete historical source description: '+details)]))
 variants.append(dict(id='another-type',label='Another valid type',rows=[criterion('name','Name',1,[0,4],'The choice is open. The scheme prints seven examples; no example has been invented here.'),criterion('details','Details',2,[0,4],'Two details of the same valid type, four marks each; the source prints no additional model.')]))
 add(1,'c','ii','3-3',12,deepcopy(variants[0]['rows']),'Name 4 + details 2 × 4',answerVariants=variants)
 # Textiles: sketch and description are together one outfit response, not two unrelated tasks.
 clothing=guide(16,'4 points @ 2 marks each','(ii)');pool(2,'a','i','3-8',4,2,[x.strip() for x in re.sub(r',?\s*etc\.?$','',clothing).split(',')])
 add(2,'a','ii','3-8',9,[criterion('sketch','Sketch',1,[0,5],'The scheme prints Sketch = 5 marks, with no model drawing or smaller step.'),criterion('description','Description',1,[0,4],'The scheme prints Description = 4 marks, with no model description or smaller step.')],'Sketch 5 + Description 4')
 outfit=guide(16,'functional finish = 2 marks',' and 2.(b)');fabric=select(outfit,'Fabric –','Functional finish –');finish=select(outfit,'Functional finish –');names=[]
 for name in ['cotton','Polyester cotton','Lycra']:
  assert name in fabric;names.append(fabric[fabric.index(name):fabric.index(name)+len(name)])
 outfit_card=add(2,'a','iii','3-7',8,[menu('fabric','Fabric',1,2,names),criterion('reasons','reasons',2,[0,2],'Two reasons for the SAME fabric. Complete source examples: '+fabric),menu('finish','Functional finish',1,2,[x.strip() for x in re.sub(r'\s*etc\.?$','',finish).split(',')])],'Type 2 + reasons 2 × 2 + functional finish 2')
 outfit_card['stem'] += '\n\n'+select(part(2,'a'),'(ii)','(iii)')
 blend=re.sub(r'\s+or$','',guide(16,'(15)'));production=select(blend,'Production:','Properties -');properties=select(blend,'Properties -','Identification test -');identification=select(blend,'Identification test -','Uses-');uses=select(blend,'Uses-')
 add(2,'b',None,'3-7',15,[criterion('production','production',3,[0,2],'Three production points for the one blended fabric selected. Full source guidance: '+production),criterion('properties','properties',2,[0,2],'Two properties. Source: '+properties),point('test',identification,3),menu('uses','uses',2,1,[x.strip() for x in re.sub(r'\s*etc\.?$','',uses).split(',')])],'Production 3 × 2 + properties 2 × 2 + identification 3 + uses 2 × 1')
 pool(2,'c','i','3-8',3,3,semis(guide(17,'3 points @ 3 marks each','(ii)')))
 careers=guide(17,'2 points @ 2 marks each');add(2,'c','ii','3-8',6,[menu('career','Name',1,2,[x.strip() for x in re.sub(r',?\s*etc\.?$','',careers).split(',')]),criterion('details','give details',2,[0,2],'Two details about the SAME named career; the scheme lists careers but no model career details.')],'Name 2 + details 2 × 2')
 # Social Studies: mandatory headings do not get a split the source never gave them.
 judged(3,'a','i','3-9',5,6,'contributory factor',guide(18,'5 points @ 6 marks each','(ii)'))
 poverty=guide(18,'2 points @ 5 marks each','(iii)');labels=['Social welfare assistance / benefits','Initiatives encouraging foreign investment.','Schemes to reduce expenditure for low income families','Combat Poverty Agency','Community Development Programmes','National Anti Poverty Strategy (NAPS)','National minimum wage.','Money Advice and Budgeting Service']
 pool(3,'a','ii','3-9',2,5,named(poverty,labels))
 charities=re.sub(r'\s+and$','',guide(18,'2 facts @ 4 marks each'));charities=re.sub(r'^e\.g\.\s*','',charities)
 add(3,'a','iii','3-9',10,[menu('name','Name',1,2,[x.strip() for x in re.sub(r'\s*etc\.?$','',charities).split(',')]),criterion('facts','facts',2,[0,4],'Two facts about the SAME named organisation; the scheme prints names but no model facts.')],'Name 2 + facts 2 × 4')
 attitudes=select(s[19].split('(ii)',1)[0],'2 points @ 5 marks each');add(3,'b','i','3-9',10,[point('intrinsic',select(attitudes,'Intrinsic –','Extrinsic –',True),5),point('extrinsic',select(attitudes,'Extrinsic –',include=True),5)],'2 required points @ 5 marks each')
 work=guide(19,'4 points @ 5 marks each',' or 3.(c)');pool(3,'b','ii','3-9',4,5,semis(work))
 education=select(s[19],'Personal qualities –','(ii)',True);pool(3,'c','i','3-10',2,5,named(education,['Personal qualities –','Academic / Skills –','Socialisation –','Educational programmes –']))
 equality=guide(19,'(2 points @ 5 marks each) x 2');gender=select(equality,'Gender inequity –','Early school leavers –');leavers=select(equality,'Early school leavers –')
 add(3,'c','ii','3-10',20,[menu('gender','Gender inequity',2,5,semis(gender)),menu('early-leavers','Early school leavers',2,5,semis(leavers))],'2 headings × 2 points × 5 marks')
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 c=build()
 if '--write' in sys.argv:write_section('C',c,dict(tasks=20,marks=275,selectionDecisions='Required headings, chosen-fabric profiles and sketch-plus-description stay whole. Open social-housing choice uses one card with source-specific marking routes. E1(a)(ii) and E3(a)(i) share a total point quota across required headings, with no invented allocation between headings. Only source-printed per-point full values are offered.'))
 else:print(json.dumps(c,ensure_ascii=False,indent=2))
