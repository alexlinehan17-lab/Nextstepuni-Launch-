#!/usr/bin/env python3
"""2020 Ordinary electives: complete source pools and exact printed tariffs."""
from copy import deepcopy
from he_review_2020_ol_main import *
def build():
 d=documents();p={n:text(d['bc'],n+4) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,22)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,l):return stripjoin(select(p[n],f'{n}.({l})',f'{n}.({chr(ord(l)+1)})' if f'{n}.({chr(ord(l)+1)})' in p[n] else None))
 def prompt(n,l,r):return re.sub(r'\s*\(\d+ marks\)\s*$','',re.split(r'\((?:i|ii|iii|iv)\)',select(part(n,l),f'({r})'),1)[0]).strip()
 def add(n,l,r,topic,marks,rows,notation,**extra):
  stem=part(n,l).split('(i)',1)[0].strip()
  if (n,l)==(1,'a'):stem=stem.split('Utility',1)[0].strip()
  c=card(f'sc-q{n}{l}{r}','C',f'E{n} Q{n}({l})({r})',topic,prompt(n,l,r),stem,marks,rows,n+4,notation,**extra);cards.append(c);return c
 def guide(pn,token,end=None,include=False):return stripjoin(select(s[pn],token,end,include))
 def judged(n,l,r,topic,count,steps,label,guidance,**extra):return add(n,l,r,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; original steps '+str(steps),**extra)
 def paired(n,l,r,topic,label,count,name_steps,detail_count,detail_steps,guidance,name_note='',detail_label='Description'):
  rows=[];groups=[];per=name_steps[-1]+detail_count*detail_steps[-1]
  for i in range(1,count+1):
   ids=[f'name-{i}',f'details-{i}'];rows += [criterion(ids[0],'Name',1,name_steps,f'Select {label} {i} of {count} DIFFERENT options, keeping the SAME option throughout its criteria. '+name_note+' Complete original paired pool: '+guidance),criterion(ids[1],detail_label,detail_count,detail_steps,f'For the SAME selected {label} {i}, use the matching original guidance above. '+name_note)];groups.append(dict(sourceCardId=f'he-2020-ol-sc-q{n}{l}{r}-choice-{i}',label=f'{label} {i}',marks=per,rowIds=ids))
  return add(n,l,r,topic,count*per,rows,f'{count} coherent choices each name{name_steps[-1]} + {detail_count} details{detail_steps[-1]}',taskGroups=groups)
 plan=dict(questionFigureKey='home-economics-2020-ol-sc-q1-floor-plan',questionFigureIncludesPrompt=False)
 judged(1,'a','i','3-3',4,[0,3,5],'points',select(s[14].split('(ii)',1)[0],'(graded 5:3:0)'),**plan)
 judged(1,'a','ii','3-3',2,[0,3,5],'modifications',select(select(s[14],'(ii)','(iii)'),'(graded 5:3:0)'),**plan)
 full=guide(14,'Architect:',include=True)+' '+guide(15,'Engineer:','(iv)',True)
 paired(1,'a','iii','3-3','Professional service',2,[0,3],1,[0,1,2],full,'Architect, Surveyor, Engineer, Solicitor and Builder have full printed models. Electrician, Plummer, Plasterer and Interior Designer are printed by name only; no description model is invented for these or another valid alternative.')
 full=select(select(s[15],'(iv)','1.(b)'),'(graded 3:2:0)');paired(1,'a','iv','3-4','Interior trend',2,[0,2],1,[0,2,3],stripjoin(full),'Choose two distinct trends from the full original pool; current trends refer to the original 2020 context. The source prints names with no separate expanded commentary model.',detail_label='Comment')
 judged(1,'b','i','3-5',3,[0,2,4],'points',select(select(s[15],'1.(b)','(ii)'),'(graded 4:2:0)'))
 full=guide(15,'2 methods @ 3 marks',include=True)
 paired(1,'b','ii','3-5','Ventilation method',2,[0,2,3],2,[0,2,3],full,'Extractor fan and wall vents have full printed principle models. Other original method names and valid alternatives remain available, but no unprinted principle is invented.',detail_label='Underlying principle')
 judged(1,'c','i','3-4',4,[0,2,4],'factors',select(s[16].split('(ii)',1)[0],'(graded 4:2:0)'))
 heads=['Emulsion water-based paint:','Oil-based paint:','Specialised paint:','Wall tiles:','Wallpaper:'];full=guide(16,heads[0],include=True);models=named(full.split('Wood panelling;',1)[0],heads);names=[h.rstrip(':') for h in heads]+['Wood panelling','mosaic','Another valid wall finish'];variants=[]
 for i,name in enumerate(names):
  model=models[i] if i<5 else 'The source lists this finish by name only; no further advantage/disadvantage model is printed or invented.' if i<7 else 'The paper leaves the choice open; no further model is printed or invented.'
  advantage=select(model,'Advantage:','Disadvantage:',True) if i<5 else model;disadvantage=select(model,'Disadvantage:',include=True) if i<5 else model
  variants.append(dict(id=f'finish-{i+1}',label=name,rows=[criterion('name','Name',1,[0,2,4],'Use ONE coherent finish profile throughout. Selected source name and types: '+(model.split('Advantage:',1)[0] if i<5 else name)),criterion('advantage','Advantage',1,[0,3,5],'ONE advantage of the SAME finish. '+advantage),criterion('disadvantage','Disadvantage',1,[0,3,5],'ONE disadvantage of the SAME finish. '+disadvantage)]))
 add(1,'c','ii','3-4',14,deepcopy(variants[0]['rows']),'ONE finish: name4 + advantage5 + disadvantage5',answerVariants=variants)
 photo=dict(questionFigureKey='home-economics-2020-ol-sc-q2-clothing',questionFigureIncludesPrompt=False)
 heads=['Function:','Comfort:','Aesthetic appeal:'];full=guide(17,heads[0],'(ii)',True)
 add(2,'a','i','3-8',18,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,2,3],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'TWO points3 for EACH function/comfort/aesthetic appeal',**photo)
 heads=['Wool:','Linen:','Cotton:','Polyester:','Viscose/rayon:','Acrylic:','Polyester cotton:'];full=guide(17,heads[0],include=True);models=named(full,heads);variants=[]
 for i,(head,model) in enumerate(zip(heads,models),1):variants.append(dict(id=f'fabric-{i}',label=head.rstrip(':'),rows=[criterion('name','Name',1,[0,3],'Name ONE fabric consistently throughout: '+head.rstrip(':')),criterion('reason','Reason',1,[0,2,4],'Give ONE reason matching the SAME selected fabric. '+model)]))
 variants.append(dict(id='other-fabric',label='Another valid fabric',rows=[criterion('name','Name',1,[0,3],'Name ONE suitable fabric.'),criterion('reason','Reason',1,[0,2,4],'Give ONE matching reason; no additional model is printed or invented.')]))
 add(2,'a','ii','3-7',7,deepcopy(variants[0]['rows']),'ONE fabric: name3 + matching reason4',answerVariants=variants,**photo)
 judged(2,'b','i','3-8',3,[0,2,3],'points',select(s[18].split('(ii)',1)[0],'(graded 3:2:0)'))
 full=guide(18,'Dyeing:','2.(c)',True);models=named(full.split('Fabric painting;',1)[0],['Dyeing:','Tie-dyeing:']);names=['Dyeing','Tie-dyeing','Fabric painting','Batik','screen printing','Another valid colour-application method'];variants=[]
 for i,name in enumerate(names):
  model=models[i] if i<2 else 'The source accepts this method by name only; no detailed model is printed or invented.' if i<5 else 'The choice remains open to valid alternatives; no further model is printed or invented.'
  variants.append(dict(id=f'colour-{i+1}',label=name,rows=[criterion('name','Name',1,[0,2],'Name ONE method consistently throughout: '+name),criterion('description','Description',2,[0,2],'TWO description points for the SAME method. '+model)]))
 add(2,'b','ii','3-7',6,deepcopy(variants[0]['rows']),'ONE method name2 + TWO description points2',answerVariants=variants)
 full=select(s[18],'2.(c)');judged(2,'c','i','3-8',3,[0,2,3],'points',select(full.split('(ii)',1)[0],'(graded 3:2:0)'))
 judged(2,'c','ii','3-8',2,[0,2,3],'points','Give TWO details of ONE selected career. The source prints career names but no expanded detail model or fixed name/detail allocation; none is invented. Complete original name pool: '+select(select(full,'(ii)'),'(graded 3:2:0)'))
 full=guide(19,'Work:','(ii)',True);heads=['Work:','Work ethic:'];add(3,'a','i','3-9',6,[criterion(f'term-{i}',head.rstrip(':'),1,[0,2,3],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Required work3 + work ethic3')
 judged(3,'a','ii','3-9',4,[0,3,5],'factors',select(select(s[19],'(ii)','(iii)'),'(graded 5:3:0)'))
 full=guide(19,'Volunteer:','(iv)',True);models=named(full,['Volunteer:','Community:'])
 add(3,'a','iii','3-11',16,[criterion('volunteer','Volunteer',1,[0,2,4],models[0]),criterion('community','Community',1,[0,2,4],models[1]),criterion('other','2 points',2,[0,2,4],'TWO additional distinct benefits from either required category; no repeated credit. '+full)],'ONE volunteer4 + ONE community4 + TWO other4')
 full=guide(19,'Financial:',include=True)
 add(3,'a','iv','3-9',8,[criterion('name','Name',1,[0,2],'Choose ONE support consistently throughout. Complete original paired pool: '+full),criterion('details','Details',2,[0,2,3],'TWO details of the SAME support. Financial/housing/advisory/material have original examples; emotional/social support are named with no further model printed or invented. '+full)],'ONE support name2 + TWO matching details3')
 judged(3,'b','i','3-11',4,[0,2,4],'factors',select(s[20].split('(ii)',1)[0],'(graded 4:2:0)'))
 full=guide(20,'Full day care:','3.(c)',True)
 paired(3,'b','ii','3-11','Childcare option',2,[0,2,3],1,[0,2,4],full,'Choose TWO DIFFERENT options from the complete original pool; named suboptions remain within their full original profiles, and valid alternatives remain open.')
 full=guide(20,'Reduction in working hours',include=True)+' '+guide(21,'Improved conditions of work','(ii)',True)
 heads=['Reduction in working hours','Improved conditions of work','Improvements in the provision of education'];models=named(full,heads)
 add(3,'c','i','3-11',18,[criterion(f'heading-{i}',head,2,[0,2,3],select(model,'(graded 3:2:0)')) for i,(head,model) in enumerate(zip(heads,models),1)],'TWO points3 for EACH of three required changes; original continuation retained')
 judged(3,'c','ii','3-9',3,[0,2,4],'points','Historical 2020 source wording: '+select(select(s[21],'(ii)'),'(graded 4:2:0)'))
 assert len(cards)==22 and sum(c['totalMarks'] for c in cards)==275
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=22,marks=275,selectionDecisions='Full floorplan/photo source inputs, all professional/ventilation/finish/fabric/colour/support/childcare alternatives with visible name-only gaps, required headings and flexible categories, precise original partial ladders, and cross-page continuations.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
