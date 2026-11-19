#!/usr/bin/env python3
"""2020 Higher electives: whole choices, source continuations and exact tariffs."""
from copy import deepcopy
from he_review_2020_hl_main import *
def build():
 d=documents();p={n:text(d['bc'],n+4) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(19,28)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,l):return stripjoin(select(p[n],f'{n}.({l})',f'{n}.({chr(ord(l)+1)})' if f'{n}.({chr(ord(l)+1)})' in p[n] else None))
 def prompt(n,l,r):return re.sub(r'\s*\(\d+ marks\)\s*$','',re.split(r'\((?:i|ii|iii)\)',select(part(n,l),f'({r})'),1)[0]).strip()
 def add(n,l,r,topic,marks,rows,notation,**extra):
  stem=part(n,l).split('(i)',1)[0].strip()
  if (n,l,r)==(2,'a','ii'):stem+=' '+prompt(2,'a','i')
  c=card(f'sc-q{n}{l}{r}','C',f'E{n} Q{n}({l})({r})',topic,prompt(n,l,r),stem,marks,rows,n+4,notation,**extra);cards.append(c);return c
 def guide(pn,token,end=None,include=False):return stripjoin(select(s[pn],token,end,include))
 def judged(n,l,r,topic,count,steps,label,guidance,**extra):return add(n,l,r,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; original steps '+str(steps),**extra)
 judged(1,'a','i','3-3',4,[0,2,4],'points','Evaluate FOUR points using the complete original positive/negative pool, with no fixed balance quota. '+select(s[19].split('(ii)',1)[0],'(graded 4:2:0)'))
 judged(1,'a','ii','3-4',4,[0,2,4],'factors',select(select(s[19],'(ii)','(iii)'),'(graded 4:2:0)'))
 judged(1,'a','iii','3-4',3,[0,2,4,6],'principles','Select THREE DIFFERENT principles and include an application for each. The source gives six marks overall per principle, with no internal description/application split. All four complete original models: '+guide(19,'Balance; proportion; emphasis; rhythm;',include=True))
 judged(1,'b','i','3-3',4,[0,2,4],'factors','Compare buying and renting using FOUR points overall; no fixed quota for each cost category. Original historical 2020 source figures and conditions: '+select(s[20].split('(ii)',1)[0],'(graded 4:2:0)'))
 heads=['Housing Assistance Payment (HAP):','Mortgage Allowance Scheme:','Rebuilding Ireland Home Loan (Home Choice Loan/ Local Authority Mortgage):','Incremental Purchase Scheme:'];full=guide(20,heads[0],include=True);models=named(full,heads);variants=[]
 for i,(head,model) in enumerate(zip(heads,models),1):
  variants.append(dict(id=f'housing-{i}',label=head.rstrip(':'),rows=[criterion('name','Name',1,[0,1,2],'Name ONE local-authority scheme consistently throughout. Original selected name: '+head.rstrip(':')),criterion('details','points',3,[0,2,4],'Give THREE details for the SAME selected scheme. Original historical 2020 rates and conditions: '+model)]))
 variants.append(dict(id='other-housing',label='Another valid local-authority housing scheme',rows=[criterion('name','Name',1,[0,1,2],'Name ONE valid local-authority housing scheme.'),criterion('details','points',3,[0,2,4],'Give THREE details for the SAME selected scheme; no additional model is printed or invented.')]))
 add(1,'b','ii','3-3',14,deepcopy(variants[0]['rows']),'One name2 + three matching details4',answerVariants=variants)
 judged(1,'c','i','3-5',4,[0,2,4],'points',select(s[21].split('(ii)',1)[0],'(graded 4:2:0)'))
 full=guide(21,'Name of heating system',include=True)+' '+s[22];names=select(full,'(graded 1:0)','Fuel/energy source:');fuel=select(full,'Fuel/energy source:','Working principle',True);working=select(full,'Working principle','Impact on the environment:');impact=select(full,'Impact on the environment:',include=True)
 add(1,'c','ii','3-5',14,[criterion('name','Name of heating system',1,[0,1],'Use ONE coherent system throughout. Full original choice pool: '+names),criterion('fuel','Fuel/energy source',1,[0,1],'Choose a fuel appropriate to the SAME selected system. '+fuel),criterion('working','Working principle',3,[0,2,3],'Explain the SAME selected system, using its matching model from the complete original wet/dry/solar/air-source/ground-source pool. Name-only alternatives retain the published tariff; no extra model is invented. Labelled diagrams are accepted. '+working),criterion('environment','Impact on the environment',1,[0,2,3],'For the SAME system and selected fuel. '+impact)],'Name1 + fuel1 + working3×3 + environmental impact3')
 add(2,'a','i','3-8',10,[criterion('sketch','Sketch',1,[0,1,2,3,4],'Sketch a daywear outfit suitable for a college student, as requested in the original paper. The source prints a sketch tariff but no model sketch.'),criterion('description','Description',1,[0,2,4,6],'Describe the SAME daywear outfit. The source prints a description tariff but no model account; none is invented.')],'Matching sketch4 + description6')
 heads=['Suitability for purpose:','Sustainability:','Current fashion trends:'];full=guide(23,heads[0],'2.(b)',True)
 add(2,'a','ii','3-8',15,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,3,5],'Evaluate the SAME college-student daywear outfit for this REQUIRED heading. Current trends refer to the original 2020 context. '+model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'ONE required suitability/sustainability/fashion point5 EACH')
 full=select(select(s[23],'2.(b)','(ii)'),'(graded 2:0)');finishes=semis(full.replace('moth- proof','moth-proof'))
 add(2,'b','i','3-7',6,[menu('finishes','finishes',3,2,finishes,'Choose ANY THREE different functional finishes from the complete original pool.')],'Three different finish names2')
 judged(2,'b','ii','3-7',3,[0,2,3],'points','Explain THREE enhancement points across the original finish pool; no fixed requirement for three different finishes. Moth-proof is accepted by name in the preceding source list without an additional printed model. '+select(select(s[23].split('2.(b)',1)[1],'(ii)'),'(graded 3:2:0)'))
 judged(2,'c','i','3-7',3,[0,2,3],'points',select(s[24].split('(ii)',1)[0],'(graded 3:2:0)'))
 judged(2,'c','ii','3-7',2,[0,2,3],'points',select(select(s[24],'(ii)'),'(graded 3:2:0)'))
 judged(3,'a','i','3-10',3,[0,3,5],'points',select(s[25].split('(ii)',1)[0],'(graded 5:3:0)'))
 heads=['Physical development:','Emotional development:','Moral development:','Intellectual development:'];full=guide(25,heads[0],'(iii)',True)
 add(3,'a','ii','3-10',20,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,3,5],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'ONE required physical/emotional/moral/intellectual account5 EACH')
 judged(3,'a','iii','3-10',5,[0,2,3],'points',guide(25,'(graded 3:2:0)'))
 judged(3,'b','i','3-9',3,[0,2,3],'causes',select(s[26].split('(ii)',1)[0],'(graded 3:2:0)'))
 judged(3,'b','ii','3-9',3,[0,2,4],'effects',select(select(s[26],'(ii)','(iii)'),'(graded 4:2:0)'))
 heads=['IDA Ireland (Industrial Development Agency):','Enterprise Ireland:'];full=guide(26,heads[0],'3.(c)',True);models=named(full.split('SOLAS;',1)[0],heads);names=[h.rstrip(':') for h in heads]+['SOLAS','Local Enterprise Offices (LEO)','Another valid statutory initiative'];variants=[]
 for i,name in enumerate(names):
  model=models[i] if i<2 else 'The source accepts this initiative by name only; no detail model is printed or invented.' if i<4 else 'The source leaves valid alternatives open; no additional model is printed or invented.'
  variants.append(dict(id=f'initiative-{i+1}',label=name,rows=[criterion('name','Name',1,[0,1,2,3],'Name ONE statutory initiative consistently throughout. Selected name: '+name),criterion('details','points',2,[0,2,3],'Give TWO details about the SAME named initiative. '+model)]))
 add(3,'b','iii','3-9',9,deepcopy(variants[0]['rows']),'One name3 + two matching details3',answerVariants=variants)
 full=guide(26,'Age:',include=True);models=named(full,['Age:','Gender:']);add(3,'c','i','3-11',12,[criterion('age','Age',2,[0,2,3],models[0]),criterion('gender','Gender',2,[0,2,3],models[1])],'TWO age points3 + TWO gender points3')
 heads=['Facilities offered:','Value for money:','Benefit to the community:'];full=guide(27,heads[0],include=True);models=named(full,heads);names=guide(27,'N.B. accept all leisure facilities','Facilities offered:',True);rows=[];groups=[]
 for i in [1,2]:
  ids=[]
  for j,(head,model) in enumerate(zip(heads,models),1):
   key=f'facility-{i}-{j}';ids.append(key);rows.append(criterion(key,head.rstrip(':'),1,[0,2,3],f'Evaluate facility {i} of TWO DIFFERENT facilities. All three criteria must refer to the SAME selected facility; choose relevant guidance from the original pool. '+names+' '+model))
  groups.append(dict(sourceCardId=f'he-2020-hl-sc-q3cii-facility-{i}',label=f'Leisure facility {i}',marks=9,rowIds=ids))
 add(3,'c','ii','3-11',18,rows,'TWO coherent facilities × (facilities3 + value3 + community3)',taskGroups=groups)
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='All four design-principle and local-authority-scheme models, historical cost figures, coherent heating profiles with original continuation, linked daywear sketch/evaluation, all finish choices and named-only gaps, required education headings, all statutory initiative alternatives, exact age/gender quotas and two coherent leisure-facility profiles.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
