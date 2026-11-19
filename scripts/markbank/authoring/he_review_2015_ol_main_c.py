#!/usr/bin/env python3
"""2015 Ordinary electives: all original profiles and visible source model gaps."""
from copy import deepcopy
from he_review_2015_ol_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(13,20)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:
   v=v.split(f'({roman})',1)[1]
   if not(n==1 and letter=='c' and roman=='ii'):v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip().replace('\uf0b7','•')
 def add(n,letter,roman,topic,marks,rows,notation,keySuffix='',**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip() if roman else ''
  if n==1 and letter=='a':stem=stem.split('The diagram below shows the floor plan for the house.',1)[0]+'The diagram below shows the floor plan for the house.'
  if n==3 and letter=='a':stem=stem.split('2009 / 2010',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman or ""}{keySuffix}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra)
  if keySuffix:c['questionRef']+=' — '+keySuffix.lstrip('-')
  cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 full=prompt(1,'a','i');c=judged(1,'a','i','3-3',3,5,'suitability',guide(13,'3 points @ 5 marks each','Suggest two modifications'),keySuffix='-evaluation',questionFigureKey='home-economics-2015-ol-sc-q1-plan',questionFigureIncludesPrompt=False);c['questionText']=full.split('Suggest two modifications',1)[0].strip(' -')
 c=judged(1,'a','i','3-3',2,5,'modifications',guide(13,'2 modifications @ 5 marks each','(ii)'),keySuffix='-modifications',questionFigureKey='home-economics-2015-ol-sc-q1-plan',questionFigureIncludesPrompt=False);c['questionText']='Suggest two modifications'+full.split('Suggest two modifications',1)[1]
 c=judged(1,'a','ii','3-3',3,6,'services',guide(13,'3 services @ 6 marks each'));c['rows'][0]['contextNote']='Name AND describe THREE different services. The 6 marks apply to each complete profile; no name/description subprice is printed. The original scheme gives descriptions for Architect, Surveyor, Engineer and Solicitor, and names only for Builder, Electrician, Plumber and Plasterer; no missing models are invented. '+c['rows'][0]['contextNote']
 judged(1,'a','iii','3-3',1,7,'planning permission',re.sub(r'\s+and$','',guide(14,'1 point @ 7 marks','1.(b)')))
 judged(1,'b','i','3-4',3,4,'factors',guide(14,'3 factors @ 4 marks each','(ii)'))
 items=guide(14,'Items:','2 reasons @ 4 marks each');reasons=re.sub(r'\s+or$','',guide(14,'Reasons:','1.(c)'));rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'item-{i}','Name',1,3,semis(items),'Choose TWO different storage furniture items in total.'),criterion(f'description-{i}','Description',1,[0,2],'Describe the SAME named item. The original scheme lists types but supplies no item-specific description models; no missing model is invented. Complete original types: '+items),criterion(f'reason-{i}','reasons',1,[0,4],'One reason for the SAME named item. Original shared reason pool: '+reasons)]);groups.append(dict(sourceCardId=f'he-2015-ol-sc-q1bii-item-{i}',label=f'Item {i}',marks=9,rowIds=[f'item-{i}',f'description-{i}',f'reason-{i}']))
 add(1,'b','ii','3-4',18,rows,'2 profiles × (name3 + description2 + reason4)',taskGroups=groups)
 c=judged(1,'c','i','3-5',3,5,'methods',guide(14,'3 methods @ 5 marks each','(ii)'));c['rows'][0]['contextNote']='Original historical 2015 water-charge context retained. '+c['rows'][0]['contextNote']
 heads=['Stop cock:','Storage tank:','Overflow pipe:'];add(1,'c','ii','3-5',15,[criterion(f'part-{i}',head[:-1],1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(14,'3 functions @ 5 marks each'),heads)),1)],'3 required functions × 5')
 sketch=guide(15,'Sketch: should','Description:',True);description=guide(15,'Description: colour','(ii)',True)
 add(2,'a','i','3-8',10,[criterion('sketch','Sketch',1,[0,6],'Sketch the chosen outfit. The original source supplies criteria, without a worked drawing; no model is invented. Original criteria: '+sketch),criterion('description','Description',2,[0,2],'Two descriptive points about the SAME outfit. Original criteria, without an outfit-specific model: '+description)],'Sketch6 + description2×2')
 heads=['Colour:','Line:','Shape:'];c=add(2,'a','ii','3-8',15,[criterion(f'element-{i}',head[:-1],1,[0,5],'Relate this required element to the SAME outfit sketched in part(i). Original guidance: '+re.sub(r'\s+and$','',body)) for i,(head,body) in enumerate(zip(heads,named(guide(15,'3 points @ 5 marks each','2.(b)'),heads)),1)],'3 required design elements × 5');c['stem']+='\n\n'+prompt(2,'a','i')
 production=guide(15,'Fibre production:');properties=guide(16,'Properties:','Fabric construction technique:');construction=re.sub(r'\s+or$','',guide(16,'Fabric construction technique:','2.(c)'));heads=['Nylon:','Polyester:'];prod=named(production,heads);props=named(properties,heads);variants=[]
 for i,(head,a,b) in enumerate(zip(heads,prod,props),1):
  full=a+' '+b+' '+construction;variants.append(dict(id=f'fabric-{i}',label=head[:-1],rows=[point('name',head[:-1],3),criterion('production','fibre production',1,[0,3],'One reference for the SAME chosen fabric. Original model: '+a),criterion('properties','properties',1,[0,3],'One reference for the SAME chosen fabric. Original model: '+b),criterion('construction','fabric construction technique',1,[0,3],'One reference for the SAME chosen fabric. Source models weaving; other named techniques have no model explanation. Original guidance: '+construction),criterion('other','1 other',1,[0,3],'One ADDITIONAL point from any of the three headings for the SAME fabric. No fixed 6-mark heading. Complete original model: '+full)]))
 variants.append(dict(id='other-valid-fabric',label='Another valid synthetic fabric',rows=[criterion('name','Name',1,[0,3],'One valid synthetic/manmade fabric under the original open list.')]+[criterion(key,label,1,[0,3],'One reference for the SAME chosen fabric. The original scheme provides no worked model for this additional choice; apply the printed criterion without inventing source guidance.') for key,label in [('production','fibre production'),('properties','properties'),('construction','fabric construction technique')]]+[criterion('other','1 other',1,[0,3],'One ADDITIONAL point from any required heading for the SAME chosen fabric; no fixed 6-mark heading.')]))
 add(2,'b',None,'3-7',15,deepcopy(variants[0]['rows']),'Name3 + three headings3 each + one other3',answerVariants=variants)
 judged(2,'c','i','3-8',3,3,'factors',guide(16,'3 factors @ 3 marks each','(ii)'))
 judged(2,'c','ii','3-8',2,3,'pressing',guide(16,'2 points @ 3 marks each'))
 judged(3,'a','i','3-10',4,5,'reasons',guide(17,'4 reasons @ 5 marks each','(ii)'),questionFigureKey='home-economics-2015-ol-sc-q3-school',questionFigureIncludesPrompt=False)
 judged(3,'a','ii','3-10',4,5,'factors',guide(17,'4 factors @ 5 marks each','(iii)'))
 full=guide(17,'Name: 5 marks, Details: 5 marks')+' '+re.sub(r'\s+and$','',select(s[18],'School Completion Programme:','3.(b)',True));heads=['Leaving Cert Applied','LCVP','Transition Year','JCSP','School Completion Programme','Home School Community Liaison Scheme','DEIS','NBSS'];add(3,'a','iii','3-10',10,[menu('initiative','Name',1,5,chosen(full,heads),'Choose ONE initiative.'),criterion('details','Details',1,[0,5],'Give details of the SAME chosen initiative. All eight original historical 2015 models, including the page18 continuation: '+full)],'Name5 + details5')
 full=guide(18,'(1 reference to each + 1 other)','(ii)');heads=['changes in settlement patterns from rural to urban areas','reduction in working hours','improved conditions of work.'];rows=[criterion(f'heading-{i}',head.rstrip('.'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)];rows.append(criterion('other','1 other',1,[0,5],'One ADDITIONAL point from any required heading. Three headings plus ONE other; no fixed second point per heading. Complete original source: '+full));add(3,'b','i','3-11',20,rows,'Three headings5 each + one other5')
 c=judged(3,'b','ii','3-11',2,5,'rights',re.sub(r'\s+or$','',guide(18,'2 points @ 5 marks each')));c['rows'][0]['contextNote']='Original historical 2015 young-worker terms retained as examination guidance. '+c['rows'][0]['contextNote']
 c=judged(3,'c','i','3-11',3,7,'options',guide(19,'3 options @ 7 marks each','(ii)'));c['rows'][0]['contextNote']='Identify AND describe THREE different childcare options, with 7 marks for each complete profile and no invented name/description split. '+c['rows'][0]['contextNote']
 full=guide(19,'Name: 5 marks, Details: 2 points @ 2 marks each');heads=['Back to School Supports','Child Benefit','F.I.S.','Rent Allowance','Fuel vouchers','Widow/Widower’s Allowance'];add(3,'c','ii','3-9',9,[menu('benefit','Name',1,5,chosen(full,heads),'Choose ONE social welfare support/benefit.'),criterion('details','Details',2,[0,2],'Two details for the SAME chosen benefit. Original historical 2015 terms retained. Rent Allowance, Fuel vouchers and Widow/Widower’s Allowance are named without model details; no missing details are invented. Complete original source: '+full)],'Name5 + two details×2')
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=20,marks=275,selectionDecisions='House-plan evaluation15/modifications10 split. Two furniture profiles9 each, same-outfit design context, same-fabric flexible15 account and all original initiative/childcare/benefit choices retained. Source gaps and historical terms render. Nested cold-water part labels remain complete.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
