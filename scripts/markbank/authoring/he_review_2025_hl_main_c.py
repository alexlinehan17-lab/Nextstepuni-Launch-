#!/usr/bin/env python3
"""Source-reviewed 2025 Higher electives/core, preserving required and dependent tasks."""
from copy import deepcopy
import json,re,sys
from he_review_2025_hl_main import documents,page_text,originals,save_batch,criterion,between,named_sections


def build():
 d=documents();s={n:page_text(d['scheme'],n).removeprefix(f'{n} ') for n in range(19,31)};p={n:page_text(d['bc'],n+4) for n in range(1,5)};old=originals();fixes={};added=[]
 def put(n,part,roman,marks,notation,rows,**extra):
  group=p[n].split(f'{n}.({part})',1)[1]
  if part!='c':group=group.split(f'{n}.({chr(ord(part)+1)})',1)[0]
  if n==2 and part=='b':stem,prompt=group.split('Name two performance',1);prompt='Name two performance'+prompt.split('(15 marks)',1)[0];stem=stem.strip()
  else:prompt=between(group,f'({roman})',f'({marks} marks)');stem=group.split('(i)',1)[0].strip()
  if n==2 and part=='a':stem='A blazer is a wardrobe staple.'
  cid=f'he-2025-hl-sc-q{n}{part}{roman}';assert cid in old,cid
  fixes[cid]=dict(reason='2025 Higher C full source review: paper prompts, independent task boundaries, required quotas and complete scheme guidance.',set=dict(questionText=prompt.replace(' • ','\n• '),questionRef=f'2025 HL Section C '+(f'E{n} ' if n<4 else '')+f'Q{n}({part})'+(f'({roman})' if not(n==2 and part=='b') else ''),stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra));return cid
 def body(n,token,end=None):
  assert s[n].count(token)==1,(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def points(n,part,roman,marks,count,steps,text,**extra):
  grade=':'.join(map(str,reversed(steps)));return put(n,part,roman,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points','points',count,steps,f'{count} distinct developed points, each graded {grade}. Complete source guidance: '+text)],**extra)
 def split(cid,suffix,prompt,marks,rows,label,concept):
  c=deepcopy(old[cid]);c.update(fixes[cid]['set']);c.update(id=cid+suffix,conceptId=concept,questionText=prompt,questionRef=c['questionRef'].split(' — ',1)[0]+' — '+label,totalMarks=marks,tariffModel=dict(kind='fixed',notation=f'{marks} marks at the independent published boundary'),rows=rows);added.append(c)
 labels=['family size and circumstances','ergonomics','environmental awareness'];values=named_sections(body(19,'1 point on each heading and 1 other point','(ii)'),labels)
 put(1,'a','i',16,'Three required headings + one other point, each 4 (4:2:0)',[criterion(str(i),label,1,[0,2,4],'One point under this required heading, graded 4:2:0. '+v) for i,(label,v) in enumerate(zip(labels,values))]+[criterion('other','point',1,[0,2,4],'One other point under any heading, graded 4:2:0.')])
 points(1,'a','ii',16,4,[0,2,4],body(19,'(ii) Outline the principles that should be considered when planning a lighting system for a kitchen/dining room. (16 marks) 4 points @ 4 marks (graded 4:2:0)','(iii)'))
 cid=put(1,'a','iii',18,'Principle 9 + effects 9',[]);v=fixes[cid]['set'];v.update(questionText='Explain the underlying principle of ventilation in a kitchen/dining room.',questionRef=v['questionRef']+' — principle',totalMarks=9,tariffModel=dict(kind='fixed',notation='3 principle points × 3 (3:2:0)'),rows=[criterion('principle','Underlying principle',3,[0,2,3],'Three explanation points, each graded 3:2:0. '+body(19,'3 points re underlying principle of ventilation @ 3 marks (graded 3:2:0)','3 effects'))])
 split(cid,'-effects','Outline the effects of inadequate ventilation in a kitchen/dining room.',9,[criterion('effects','Effects of inadequate ventilation',3,[0,2,3],'Three effects, each graded 3:2:0. '+body(19,'3 effects of inadequate ventilation @ 3 marks (graded 3:2:0)'))],'effects','inadequate-ventilation-effects')
 labels=['families with school going children','people with disabilities'];values=named_sections(body(20,'2 points on each and any 2 others','(ii)'),labels)
 put(1,'b','i',18,'Each required group 2 + other 2, each 3 (3:2:0)',[criterion(str(i),label,2,[0,2,3],'Two points for this required group, each graded 3:2:0. '+v) for i,(label,v) in enumerate(zip(labels,values))]+[criterion('other','points',2,[0,2,3],'Two further points for either group, each graded 3:2:0.')])
 points(1,'b','ii',12,3,[0,2,4],'Use the scheme’s 2025 examination context. '+body(20,'3 points @ 4 marks (graded 4:2:0)'))
 points(1,'c','i',15,5,[0,2,3],body(21,'(i) Describe the cold-water system in a house. (15 marks) 5 points @ 3 marks (graded 3:2:0)','(ii)'))
 points(1,'c','ii',15,5,[0,2,3],s[21].rsplit('5 points @ 3 marks (graded 3:2:0)',1)[1].strip())
 outfit=body(22,'one reference to each outfit and one other','(ii)')
 put(2,'a','i',15,'One point on each outfit + one other, each 5 (5:3:0)',[criterion('first','outfit',1,[0,3,5],'Evaluate the first outfit, graded 5:3:0. Across the answer address design, comfort and aesthetic appeal. The scheme requires one reference to each outfit and one other; it does not assign five marks to each heading. Complete model guidance: '+outfit),criterion('second','outfit',1,[0,3,5],'Evaluate the second outfit, graded 5:3:0. Use the complete model guidance above.'),criterion('other','other',1,[0,3,5],'One additional evaluation of either outfit, graded 5:3:0. Across the answer cover all three printed headings.')],questionFigureKey='home-economics-2025-hl-sc-q2a-outfits',questionFigureIncludesPrompt=False,figureKey='')
 names=['Balance','Emphasis','Proportion','Rhythm'];values=named_sections(body(22,'How it is demonstrated in either outfit 2 points @ 3 marks (graded 3:2:0)'),names);variants=[]
 for name,v in zip(names,values):variants.append(dict(id=name.lower(),label=name,rows=[criterion('name','Design principle',1,[0,4],'Name the chosen principle, graded 4:0. '+name),criterion('explanation','How it is demonstrated',2,[0,2,3],'Two explanations of the SAME principle in either shown outfit, each graded 3:2:0. '+v)]))
 other=deepcopy(variants[0]['rows']);other[0]['contextNote']='Name another valid design principle, graded 4:0.';other[1]['contextNote']='Two explanations showing the same principle in either pictured outfit, each graded 3:2:0. No further model is printed.';variants.append(dict(id='another',label='Another valid principle',rows=other))
 put(2,'a','ii',10,'Name 4 (4:0) + explanation 2 × 3 (3:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants,questionFigureKey='home-economics-2025-hl-sc-q2a-outfits',questionFigureIncludesPrompt=False,figureKey='')
 tests=body(23,'procedure involved 3 points @ 3 marks (graded 3:2:0)')
 put(2,'b','i',15,'Two test names × 3 + one procedure 3 × 3 (3:2:0)',[criterion('names','Two performance tests',2,[0,2,3],'Name two distinct tests, each graded 3:2:0. All eleven printed test models are retained in the procedure guidance.'),criterion('procedure','procedure involved',3,[0,2,3],'Three procedure points for ONE of the two tests you named, each graded 3:2:0. Heating/flame examples describe supervised laboratory work. Complete scheme guidance: '+tests)])
 points(2,'c','i',9,3,[0,2,3],body(24,'3 influences @ 3 marks (graded 3:2:0)','(ii)'))
 points(2,'c','ii',6,2,[0,2,3],body(24,'2 points @ 3 marks (graded 3:2:0)'))
 education,flexibility=named_sections(body(25,'2 points to refer to increased educational requirements, 2 points to refer to flexibility in working hours and 1 other','(ii)'),['increased educational requirements','increased flexibility in working hours'])
 put(3,'a','i',20,'Education 2 + flexibility 2 + other 1, each 4 (4:2:0)',[criterion('education','Increased educational requirements',2,[0,2,4],'Two points, each graded 4:2:0. '+education),criterion('flexibility','Flexibility in working hours',2,[0,2,4],'Two points, each graded 4:2:0. '+flexibility),criterion('other','point',1,[0,2,4],'One further point under either heading, graded 4:2:0.')])
 intrinsic,extrinsic=named_sections(body(25,'1 point on each + 1 other point','(iii)'),['intrinsic work satisfaction','extrinsic work satisfaction'])
 put(3,'a','ii',15,'Intrinsic 1 + extrinsic 1 + other 1, each 5 (5:3:0)',[criterion('intrinsic','intrinsic work satisfaction',1,[0,3,5],'One analysed point, graded 5:3:0. '+intrinsic),criterion('extrinsic','extrinsic work satisfaction',1,[0,3,5],'One analysed point, graded 5:3:0. The examples describe possible experiences, not fixed traits of workers. '+extrinsic),criterion('other','point',1,[0,3,5],'One further analysis under either heading, graded 5:3:0.')])
 put(3,'a','iii',15,'Name 3 (3:0) + evaluation 4 × 3 (3:2:0)',[criterion('name','Childcare option',1,[0,3],'Name one option, graded 3:0. '+body(25,'name of childcare option @ 3 marks (graded 3:0)','evaluation of childcare option')),criterion('evaluation','evaluation of childcare option',4,[0,2,3],'Four points about the SAME option, each graded 3:2:0. '+body(25,'4 points @ 3 marks (graded 3:2:0)').removesuffix(' and'))])
 points(3,'b','i',18,3,[0,2,4,6],body(26,'(i) Analyse the reasons why adults return to education. (18 marks) 3 points @ 6 marks (graded 6:4:2:0)','(ii)'))
 points(3,'b','ii',12,3,[0,2,4],body(26,'3 points @ 4 marks (graded 4:2:0)','or 3.(c)'))
 points(3,'c','i',18,3,[0,2,4,6],'The answer must refer to the cycle of poverty; no separate compulsory point tariff is printed for that reference. '+s[26].rsplit('3 points @ 6 marks (graded 6:4:2:0)',1)[1].split('(ii)',1)[0].strip())
 absolute,relative=named_sections(body(26,'• relative poverty. 2 points @ 3 marks (graded 3:2:0)'),['absolute poverty','relative poverty'])
 put(3,'c','ii',12,'Each required type: 2 × 3 (3:2:0)',[criterion('absolute','Absolute poverty',2,[0,2,3],'Two points, each graded 3:2:0. '+absolute),criterion('relative','Relative poverty',2,[0,2,3],'Two points, each graded 3:2:0. '+relative)])
 points(4,'a','i',20,5,list(range(5)),body(27,'5 points @ 4 marks (4:3:2:1:0)','(ii)'))
 cid=put(4,'a','ii',18,'Causes 6 + methods 12',[]);v=fixes[cid]['set'];v.update(questionText='Outline two causes of toughness in meat.',questionRef=v['questionRef']+' — causes',totalMarks=6,tariffModel=dict(kind='fixed',notation='2 causes × 3 (3:2:0)'),rows=[criterion('causes','Causes of toughness',2,[0,2,3],'Two causes, each graded 3:2:0. '+body(27,'2 outlined causes of toughness @ 3 marks (graded 3:2:0)','4 described methods'))])
 split(cid,'-methods','Describe four methods of tenderising meat.',12,[criterion('methods','Methods of tenderising',4,[0,2,3],'Four methods, each graded 3:2:0. '+body(27,'4 described methods of tenderising meat @ 3 marks (graded 3:2:0)','(iii)'))],'methods','meat-tenderising-methods')
 points(4,'a','iii',12,3,[0,2,4],body(27,'3 points @ 4 marks (graded 4:2:0)'))
 points(4,'b','i',16,4,[0,2,4],'This is the historical scheme’s account, not a statement of current lending limits or eligibility. '+body(28,'4 points @ 4 marks (graded 4:2:0)'))
 mortgage=body(29,'description: 3 points @ 4 marks (graded 4:2:0)','or 4.(c)');models,others=mortgage.split('Tracker;',1);names=['Annuity/Repayment mortgage:','Endowment:','Pension linked:','Local authority mortgage/Home Choice Loan:'];values=named_sections(models,names);variants=[]
 for i,(name,v) in enumerate(zip(names,values)):variants.append(dict(id=str(i),label=name.rstrip(':'),rows=[criterion('name','Name',1,[0,1,2],'Name the chosen type, graded 2:1:0. '+name.rstrip(':')),criterion('description','Description',3,[0,2,4],'Three points about the SAME type, each graded 4:2:0. Historical exam example; product availability, figures and terms are not current lending advice. '+v)]))
 other=deepcopy(variants[0]['rows']);other[0]['contextNote']='Name another valid type, graded 2:1:0. Other printed examples: Tracker;'+others;other[1]['contextNote']='Three accurate points about the SAME named type, each graded 4:2:0. No further model is printed.';variants.append(dict(id='another',label='Another valid type',rows=other))
 put(4,'b','ii',14,'Name 2 (2:1:0) + description 3 × 4 (4:2:0)',deepcopy(variants[0]['rows']),answerVariants=variants)
 points(4,'c','i',15,3,[0,3,5],body(29,'3 points @ 5 marks (graded 5:3:0)'))
 ease=between(s[30],'2 points @ 3 marks (graded 3:2:0)','• effect on nutritive') if s[30].count('2 points @ 3 marks (graded 3:2:0)')==1 else s[30].split('2 points @ 3 marks (graded 3:2:0)',1)[1].split('• effect on nutritive',1)[0].strip()
 nutritive=body(30,'1 @ 3 marks (graded 3:2:0)','• palatability');palatable=s[30].rsplit('2 points @ 3 marks (graded 3:2:0)',1)[1].strip()
 put(4,'c','ii',15,'Ease 2 + nutritive 1 + palatability 2, each 3 (3:2:0)',[criterion('ease','Ease of use',2,[0,2,3],'Two points, each graded 3:2:0. '+ease),criterion('nutritive','Effect on nutritive value',1,[0,2,3],'One point, graded 3:2:0. '+nutritive),criterion('palatability','Palatability',2,[0,2,3],'Two points, each graded 3:2:0. '+palatable)])
 assert len(fixes)==26 and len(added)==2 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==385
 return fixes,added


def write():
 fixes,added=build();save_batch('C',fixes,added,dict(tasks=28,marks=385,selectionDecisions='Separate ventilation principle/effects (9/9) and meat toughness/tenderising (6/12). All required headings remain whole. Outfit evaluation follows the printed one-reference-per-outfit quota, without inventing a tariff per heading. Fabric testing stays one two-names/one-dependent-procedure response with all eleven models. Design principles, childcare and mortgage choices retain their dependent accounts.',checked='2026-11-06'));print('2025 Higher C: 28 reviewed tasks, 385 offered marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
