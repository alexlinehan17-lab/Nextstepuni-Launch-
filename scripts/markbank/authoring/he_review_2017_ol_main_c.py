#!/usr/bin/env python3
"""2017 Ordinary electives: all source models, linked choices and exact awards."""
from copy import deepcopy
from he_review_2017_ol_main import *
def build():
 d=documents();norm=lambda v:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',v);p={n:norm(text(d['paper'],n+8)) for n in [1,2,3]};s={n:norm(text(d['scheme'],n)) for n in range(14,21)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,letter):return stripjoin(select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None))
 def prompt(n,letter,roman):
  v=select(part(n,letter),f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,suffix='',**extra):
  stem=part(n,letter).split('(i)',1)[0].strip()
  if n in [1,2] and letter=='a':stem=stem.split('(www.',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman}{suffix}','C',f'E{n} Q{n}({letter})({roman})',topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra)
  if suffix:c['questionRef']+=' — '+('poverty definition' if suffix=='-definition' else 'poverty types')
  if n==1 and letter=='a':c.update(questionFigureKey='home-economics-2017-ol-sc-q1-housing',questionFigureIncludesPrompt=False)
  if n==2 and letter=='a':c.update(questionFigureKey='home-economics-2017-ol-sc-q2-outfits',questionFigureIncludesPrompt=False)
  cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','i','3-3',4,5,'factors',guide(14,'4 factors @ 5 marks each','(ii)'))
 full=guide(14,'• attic','(iii)',True);heads=['• attic','• walls','• windows.'];names=[['fibre blanket','loose fill','foam insulation','blown-fibre insulation'],['cavity walls','solid walls'],['double or triple glazed','curtains']];rows=[];groups=[]
 for i,(head,body,options) in enumerate(zip(heads,named(full,heads),names),1):
  options=chosen(body,options);label=head.lstrip('• ').rstrip('.')
  rows += [menu(f'name-{i}','Name',1,2,options,f'Name ONE insulation method for the required {label} area.'),criterion(f'description-{i}','Description',1,[0,3],f'Describe the SAME method chosen for {label}. One whole description earns three marks; no internal split is printed. Complete original paired models: '+body)]
  groups.append(dict(sourceCardId=f'he-2017-ol-sc-q1aii-area-{i}',label=label,marks=5,rowIds=[f'name-{i}',f'description-{i}']))
 add(1,'a','ii','3-6',15,rows,'Attic, walls and windows: name 2 + description 3 each',taskGroups=groups)
 judged(1,'a','iii','3-6',3,5,'advantages',stripjoin(guide(14,'3 advantages @ 5 marks each')))
 judged(1,'b','i','3-4',3,5,'colour',guide(15,'3 points @ 5 marks each','(ii)'))
 full=stripjoin(guide(15,'Soft furnishings:','1.(c)',True));furnishings,reasons=named(full,['Soft furnishings:','Reasons:'])
 rows=[menu('names','Soft furnishings',2,4,semis(furnishings.split(':',1)[1]),'Choose TWO different furnishings. Keep one reason linked to EACH chosen furnishing.')]+[criterion(f'reason-{i}','Reasons',1,[0,marks],f'Give a reason for the SAME furnishing {i} selected above. The first credited reason earns 4, the second 3; no named furnishing is tied to either award. Complete original reason pool: '+reasons) for i,marks in [(1,4),(2,3)]]
 add(1,'b','ii','3-4',15,rows,'Two furnishing names 4 each + paired reasons 4 then 3')
 judged(1,'c','i','3-5',3,5,'guidelines',guide(15,'3 guidelines @ 5 marks each','(ii)'))
 full=guide(15,'Type: gas;',include=True);energy,reasons=named(full,['Type:','Reasons:']);add(1,'c','ii','3-6',15,[menu('type','Type',1,5,semis(energy.split(':',1)[1]),'Choose ONE alternative energy supply.'),criterion('reasons','reasons',2,[0,5],'Give TWO reasons appropriate to the SAME chosen energy supply. Complete original shared source: '+reasons)],'Type 5 + two matching reasons 5')
 full=guide(16,'Suit - shape:','(ii)',True);suit,dress=named(full,['Suit - shape:','Dress - shape:']);heads=['shape:','proportion:','design features:'];suit_parts=named(suit,heads);dress_parts=named(dress,heads)
 add(2,'a','i','3-8',18,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,3],'Two points under this required heading. Address the pictured outfits; no fixed one-per-outfit quota is printed. Complete original suit model: '+a+' Complete original dress model: '+b) for i,(head,a,b) in enumerate(zip(heads,suit_parts,dress_parts),1)],'Shape, proportion and design features: two points 3 each')
 full=guide(16,'Man:',include=True);variants=[]
 for i,(name,body) in enumerate(zip(['Man','Woman'],named(full,['Man:','Woman:'])),1):
  variants.append(dict(id=f'outfit-{i}',label=name,rows=[criterion('accessory','accessory',1,[0,3],'Choose ONE accessory for this pictured outfit. Complete original paired pool: '+body),criterion('reason','reason',1,[0,4],'One reason matching that SAME accessory and outfit. Complete original paired pool: '+body)]))
 add(2,'a','ii','3-8',7,deepcopy(variants[0]['rows']),'Accessory 3 + matching reason 4',answerVariants=variants)
 full=guide(17,'Animal:','(ii)',True);animal,plant=named(full,['Animal:','Plant:']);rows=[];groups=[]
 for i,(name,body) in enumerate([('Animal',animal),('Plant',plant)],1):
  rows += [point(f'class-{i}',name,2),menu(f'example-{i}','Examples',1,2,semis(body.split(':',1)[1]),'Give ONE example of this SAME natural-fibre class.')]
  groups.append(dict(sourceCardId=f'he-2017-ol-sc-q2bi-class-{i}',label=name,marks=4,rowIds=[f'class-{i}',f'example-{i}']))
 add(2,'b','i','3-7',8,rows,'Two required classes: class 2 + example 2 each',taskGroups=groups)
 full=stripjoin(guide(17,'Burn test:','2.(c)',True));variants=[dict(id='burn',label='Burn test',rows=[point('name','Burn test',3),criterion('description','Description',1,[0,4],'Describe the SAME test, retaining the complete original cotton, linen, silk and wool behaviour. One whole description earns four marks; no per-stage allocation is printed. '+full)]),dict(id='other-test',label='Another valid natural-fibre test',rows=[criterion('name','Name',1,[0,3],'Choose ONE suitable natural-fibre identification test. The source models only the burn test.'),criterion('description','Description',1,[0,4],'Describe the SAME selected test. No additional source model is printed and none is invented.')])]
 add(2,'b','ii','3-7',7,deepcopy(variants[0]['rows']),'Name 3 + whole description 4',answerVariants=variants)
 full=guide(17,'Name: 3 marks, Comment: 3 marks','(ii)');names=['John Rocha','Louise Kennedy','Philip Treacy','Paul Costelloe','Orla Kiely','Helen Cody'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(full,names)),1):variants.append(dict(id=f'designer-{i}',label=name,rows=[point('name',name,3),criterion('comment','Comment',1,[0,3],'Comment on this SAME designer. Complete historical 2017 source model: '+body)]))
 variants.append(dict(id='other-designer',label='Another valid Irish designer',rows=[criterion('name','Name',1,[0,3],'Name ONE Irish fashion designer; all six source models remain available.'),criterion('comment','Comment',1,[0,3],'Comment on the SAME designer. No additional source model is printed.')]))
 add(2,'c','i','3-8',6,deepcopy(variants[0]['rows']),'Name 3 + matching comment 3',answerVariants=variants)
 c=judged(2,'c','ii','3-8',3,3,'trends',guide(17,'3 trends @ 3 marks each'));c['rows'][0]['contextNote']='Historical 2017 fashion wording retained. '+c['rows'][0]['contextNote']
 c=judged(3,'a','i','3-9',1,6,'Definition',guide(18,'Definition: 6 marks','Relative Poverty:'),suffix='-definition');c['questionText']=select(prompt(3,'a','i'),'Define poverty.','(6)',True)
 c=add(3,'a','i','3-9',12,[criterion('relative','Relative Poverty',1,[0,6],guide(18,'Relative Poverty: 6 marks','Absolute Poverty:')),criterion('absolute','Absolute Poverty',1,[0,6],guide(18,'Absolute Poverty: 6 marks','(ii)'))],'Relative poverty 6 + absolute poverty 6',suffix='-types');c['questionText']=select(prompt(3,'a','i'),'Explain each of the following:',include=True)
 full=guide(18,'3 groups @ 3 marks each, 3 effects @ 3 marks each');names=chosen(full,['Elderly people','unemployed people','lone parents','low-paid workers','refugees / ethnic minorities','people with disabilities / long term illness','small farmers / rural households','members of travelling community','homeless people','children'])
 rows=[menu('groups','groups',3,3,names,'Choose ANY THREE groups, then give one matching effect for EACH.')]+[criterion(f'effect-{i}','effects',1,[0,3],f'Give ONE effect for the SAME group {i} selected above. Complete original paired pool: '+full) for i in [1,2,3]]
 add(3,'a','ii','3-9',18,rows,'Three names 3 + three matching effects 3')
 full=stripjoin(guide(19,'Name: 2 marks, Details: 3 points @ 4 marks each','3.(b)'));described=full.split('Lions Club;',1)[0];names=['St. Vincent De Paul:','Simon Community:','Focus Ireland:'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(described,names)),1):variants.append(dict(id=f'charity-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),2),criterion('details','Details',3,[0,4],'Three details of this SAME organisation. Complete original model: '+body)]))
 for i,name in enumerate(['Lions Club','Rotary Club','Another valid voluntary organisation'],1):
  note='The original scheme names Lions Club and Rotary Club without detail models. No model is invented. Keep three details about the SAME chosen organisation.'
  variants.append(dict(id=f'other-charity-{i}',label=name,rows=[criterion('name','Name',1,[0,2],note) if i==3 else point('name',name,2,note=note),criterion('details','Details',3,[0,4],note)]))
 add(3,'a','iii','3-9',14,deepcopy(variants[0]['rows']),'Name 2 + three matching details 4',answerVariants=variants)
 judged(3,'b','i','3-11',3,5,'factors',guide(19,'3 factors @ 5 marks each','(iii)'))
 full=stripjoin(guide(19,'(1 reference to individual, 1 reference to community plus 1 other)'));individual,community=named(full,['Individual:','Community:']);c=add(3,'b','ii','3-11',15,[criterion('individual','individual',1,[0,5],individual),criterion('community','community',1,[0,5],community),criterion('other','1 other',1,[0,5],'One ADDITIONAL benefit from either heading. '+full)],'Individual 5 + community 5 + one other 5');c['rows'][0]['contextNote']='The original paper labels this (ii); the original scheme misprints it (iii). This card preserves the paper identity and the complete matching voluntary-work guidance. '+c['rows'][0]['contextNote']
 full=guide(20,'Details: (2 points @ 2 marks each) X 2','(ii)');names=chosen(full,['Play groups and play schools','Early start pre-school project','Crèche','Montessori school','NaíonraÍ','nurseries']);r=menu('names','Name',2,4,names,'Choose TWO different pre-school options. First credited name earns 4, second 3; no option is fixed to either award. Keep two details matched to EACH chosen option.');r['group']['perOptionSteps']=[4,3];r['marks']=7
 rows=[r]+[criterion(f'details-{i}','Details',2,[0,2],f'Two details about the SAME option {i} selected above. The original gives full models for play groups/play schools, Early Start, Crèche and Montessori; NaíonraÍ and nurseries have names only. No additional model is invented. Complete paired source guidance: '+full) for i in [1,2]]
 add(3,'c','i','3-10',15,rows,'Two names 4 then 3 + two details 2 for EACH selected option')
 judged(3,'c','ii','3-10',3,5,'advantages',guide(20,'3 advantages @ 5 marks each'))
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='All housing/outfit images and models, linked insulation/accessory/classification profiles, original unequal furnishing-reason and pre-school-name awards, separately printed poverty definition/types tariffs, ten poverty group/effect models, all designer/charity alternatives, and the paper/scheme C3(b)(ii)/(iii) label discrepancy retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
