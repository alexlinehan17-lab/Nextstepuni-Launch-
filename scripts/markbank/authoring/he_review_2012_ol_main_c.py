#!/usr/bin/env python3
"""2012 Ordinary electives, preserving original choices and linked profiles."""
from copy import deepcopy
from he_review_2012_ol_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n).replace('\uf0b7','•') for n in range(13,19)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def prompt(n,letter,roman):
  v=select(part(n,letter),f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip().replace('\uf0b7','•')
 def add(n,letter,roman,topic,marks,rows,notation,suffix='',custom=None,**extra):
  stem=part(n,letter).split('(i)',1)[0].strip()
  if n==1 and letter=='a':stem=stem.split('Screening',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman}{suffix}','C',f'E{n} Q{n}({letter})({roman})'+(' — '+suffix[1:] if suffix else ''),topic,custom or prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 stages=guide(13,'4 stages @ 5 marks','(ii)')
 add(1,'a','i','3-5',20,[criterion('stages','stages',4,[0,5],'Explain four stages from the ORIGINAL diagram, including any of its printed choices. Complete source models: '+stages+' The diagram also names Fluoridation and Softening, but the scheme supplies no explanations for them. A named stage still requires an explanation; no model has been invented.')],'4 stages × 5',questionFigureKey='home-economics-2012-ol-sc-q1-water',questionFigureIncludesPrompt=False)
 heads=['ball cock / valve','stop cock','overflow pipe','mains pipe.'];bodies=named(guide(13,'4 functions @ 5 marks'),['• '+h for h in heads]);add(1,'a','ii','3-5',20,[criterion(f'part-{i}',h,1,[0,5],v[2:]) for i,(h,v) in enumerate(zip(heads,bodies),1)],'4 required parts × 5')
 judged(1,'a','iii','3-5',2,5,'methods',re.sub(r'\s+and$','',guide(14,'2 methods @ 5 marks','1(b)')))
 judged(1,'b','i','3-3',2,3,'planning permission',guide(14,'2 points @ 3 marks','(ii)'))
 full=prompt(1,'b','ii');before,after=full.split(' and describe ',1);comparison=guide(14,'Outline Planning Permission:','Procedure:');outline,fullpermission=comparison.split('Full Planning Permission:',1)
 add(1,'b','ii','3-3',8,[criterion('outline','Outline Planning Permission',1,[0,4],'Historical 2012 source: '+outline),criterion('full','Full Planning Permission',1,[0,4],'Historical 2012 source: '+fullpermission)],'1 point on each type × 4',suffix='-difference',custom=before)
 judged(1,'b','ii','3-3',4,4,'Procedure',re.sub(r'\s+or$','',guide(14,'Procedure for Full Planning Permission:','1.(c)')),suffix='-procedure',custom='describe '+after)
 judged(1,'c','i','3-4',3,5,'factors',guide(14,'3 factors @ 5 marks','(ii)'))
 judged(1,'c','ii','3-4',3,5,'safety considerations',guide(14,'3 considerations @ 5 marks'))
 heads=['function','shape','proportion'];bodies=named(select(s[15],'Refer to:','(ii)'),['• '+h for h in heads]);add(2,'a','i','3-8',12,[criterion(f'heading-{i}',h,2,[0,2],re.sub(r'\(12\)','',v[2:])) for i,(h,v) in enumerate(zip(heads,bodies),1)],'2 references to EACH heading × 2',questionFigureKey='home-economics-2012-ol-sc-q2-uniform',questionFigureIncludesPrompt=False)
 fibre=guide(15,'Reason: 3 marks','(iii)');variants=[]
 for key,label,body in [('wool','wool',select(fibre,'wool –','Acrylic –')),('acrylic','Acrylic',select(fibre,'Acrylic –'))]:variants.append(dict(id=key,label=label,rows=[point('name',label,3),criterion('reason','Reason',1,[0,3],'One reason matching the SAME fibre. Source: '+body)]))
 variants.append(dict(id='another-fibre',label='Another suitable fibre',rows=[criterion('name','Name',1,[0,3],'One fibre suitable for this school cardigan.'),criterion('reason','Reason',1,[0,3],'A reason matching the SAME fibre. The source models wool and acrylic; no further model is printed.')]))
 add(2,'a','ii','3-7',6,deepcopy(variants[0]['rows']),'Name3 + reason3',answerVariants=variants,questionFigureKey='home-economics-2012-ol-sc-q2-uniform',questionFigureIncludesPrompt=False)
 crest=re.sub(r'\s+and$','',guide(15,'Description: 2 points @ 2 marks each'));names,model=crest.split('appliqué:',1);options=examples(names).replace(' etc','').split(',');variants=[]
 for i,label in enumerate(options,1):
  label=label.strip();variants.append(dict(id=f'method-{i}',label=label,rows=[point('name',label,3),criterion('description','Description',2,[0,2],'Describe the SAME method. '+('Original model: '+model if label=='appliqué' else 'The scheme names this method but supplies no model description; its only described example is appliqué: '+model))]))
 variants.append(dict(id='another-method',label='Another valid method',rows=[criterion('name','Name',1,[0,3],'One method of applying a school crest.'),criterion('description','Description',2,[0,2],'Two matching description points. No further model is printed; original appliqué model: '+model)]))
 add(2,'a','iii','3-8',7,deepcopy(variants[0]['rows']),'Name3 + description 2×2',answerVariants=variants)
 designer=guide(16,'Contribution: 3 marks','(ii)');names,contribution=designer.split('e.g.',2)[1:];options=[v.strip() for v in names.replace('etc.','').split(',') if v.strip()]
 add(2,'b','i','3-8',6,[menu('name','Name',1,3,options),criterion('contribution','Contribution',1,[0,3],'Contribution of the SAME designer. Complete source examples: '+contribution)],'Name3 + matching contribution3')
 judged(2,'b','ii','3-8',3,3,'contribution of accessories',re.sub(r'\s+or$','',guide(16,'3 points @ 3 marks','2.(c)')))
 judged(2,'c','i','3-8',3,2,'factors',guide(16,'3 factors @ 2 marks','(ii)'))
 judged(2,'c','ii','3-8',3,3,'stages',guide(16,'3 stages @ 3 marks'))
 heads=['more people living in urban areas','changing attitudes to marriage','changing attitudes to parenting','improvements in the provision of social welfare.'];bodies=named(select(s[17],'(40)','(ii)'),['• '+h for h in heads]);add(3,'a','i','3-11',40,[criterion(f'effect-{i}',h,2,[0,5],select(v,'2 points @ 5 marks')) for i,(h,v) in enumerate(zip(heads,bodies),1)],'2 effects under EACH of 4 headings × 5')
 initiative=guide(17,'Details 2 points @ 3 marks');names=['redeployment of government departments and state agencies to rural locations','rural resettlement schemes','IDA','Fás /Solas','Enterprise Ireland','County Enterprise Boards','Job Start','Improved infrastructure']
 add(3,'a','ii','3-9',10,[menu('name','Name',1,4,chosen(initiative,names)),criterion('details','Details',2,[0,3],'Two points about the SAME initiative. Full historical source: '+initiative)],'Name4 + details 2×3')
 judged(3,'b','i','3-9',4,5,'reasons',guide(18,'4 reasons @ 5 marks','(ii)'))
 c=judged(3,'b','ii','3-9',2,5,'protection',re.sub(r'\s+or$','',select(s[18].split('3.(c)',1)[0],'2 points @ 5 marks')));c['rows'][0]['contextNote']='Historical 2012 examination guidance for the named Act. '+c['rows'][0]['contextNote']
 programmes=guide(18,'Programmes:','(ii)');names=chosen(programmes,['School Completion Programme','Leaving Cert Applied','Youthreach','LCVP','Transition Year','JCSP']);rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'name-{i}','Name',1,4,names,'Choose a DIFFERENT education programme for each pair.'),criterion(f'details-{i}','Details',1,[0,5],'One detail point about the SAME named programme. Complete source: '+programmes+' The scheme names four further programmes without model details; no new details have been invented.')]);groups.append(dict(sourceCardId=f'he-2012-ol-sc-q3ci-pair-{i}',label=f'Education programme {i}',marks=9,rowIds=[f'name-{i}',f'details-{i}']))
 add(3,'c','i','3-10',18,rows,'2 programmes × (name4 + details5)',taskGroups=groups)
 benefit=guide(18,'Benefits:');c=add(3,'c','ii','3-10',12,[criterion(f'benefits-{i}','benefits',2,[0,3],f'Programme {i}: two benefits of the SAME programme named in part (i), separately for each of the two programmes. Full original source: '+benefit) for i in [1,2]],'2 benefits for EACH of 2 programmes × 3');c['stem']+='\n\n'+prompt(3,'c','i')
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='C1(b)(ii) difference/procedure independently8/16. All required heading quotas and chosen-fibre, crest, designer, initiative and education-programme dependencies preserved, including previous programme prompt on benefits. Missing crest/programme model guidance visibly identified.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
