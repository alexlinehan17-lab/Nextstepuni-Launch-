#!/usr/bin/env python3
"""2013 Higher electives: original models, required quotas and dependent profiles."""
from copy import deepcopy
from he_review_2013_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,22)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip().replace('\uf0b7','•')
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip() if roman else ''
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','i','3-3',5,4,'historical development',guide(14,'5 points @ 4 marks each','(ii)'))
 groups=guide(14,'6 points @ 3 marks each (2 points on each group)')+' '+s[15].split('(iii)',1)[0];heads=['Families:','Single people:','Elderly people :'];add(1,'a','ii','3-3',18,[criterion(f'group-{i}',h.rstrip(' :'),2,[0,3],v) for i,(h,v) in enumerate(zip(heads,named(groups,heads)),1)],'2 references to EACH group × 3')
 social=select(s[15],'(iii)','1.(b)');judged(1,'a','iii','3-3',3,4,'social housing',re.sub(r'\s+and$','',select(social,'3 points @ 4 marks each')))
 lighting=select(select(s[15],'1.(b)','(ii)'),'3 points @ 4 marks each');bodies=named(lighting,['CFL/fluorescents lights:','LED:']);variants=[]
 for i,(label,body) in enumerate(zip(['CFL/fluorescents lights','LED'],bodies),1):variants.append(dict(id=f'source-{i}',label=label,rows=[criterion('principle','underlying principle',3,[0,4],'Three points explaining the SAME energy-efficient lighting type. Original model: '+body)]))
 variants.append(dict(id='another-type',label='Another energy-efficient lighting type',rows=[criterion('principle','underlying principle',3,[0,4],'Explain three principle points for ONE type. The scheme models CFL/fluorescents and LED only; no further model is printed.')]))
 add(1,'b','i','3-5',12,deepcopy(variants[0]['rows']),'Principle3×4; no name tariff',answerVariants=variants)
 judged(1,'b','ii','3-5',3,6,'developments',re.sub(r'\s+or$','',guide(15,'3 points @ 6 marks each')))
 floors=guide(16,'(2 references to each type of floor)','(ii)');heads=['Solid floors:','Suspended floors:'];add(1,'c','i','3-4',12,[criterion(f'type-{i}',h[:-1],2,[0,3],v) for i,(h,v) in enumerate(zip(heads,named(floors,heads)),1)],'2 references to EACH floor type × 3')
 full=guide(16,'(Name = 3 marks, Description = 2 marks, Advantage = 2 marks, Disadvantage =2 marks) x 2');semi=select(full,'Semi hard:','Soft:');soft=select(full,'Soft:');rows=[];task_groups=[]
 for key,label,body,names in [('semi-hard','Semi hard',semi,['wood','vinyl','linoleum','cork','coir','sisal']),('soft','Soft',soft,['carpet','rugs','carpet tiles'])]:
  # These are the source's initial type lists, not synthesized combinations.
  list_text=body.split('Wood:',1)[0] if key=='semi-hard' else body.split('Carpet:',1)[0]
  options=[v.strip().removesuffix(' etc.').strip() for v in list_text.split(',') if v.strip()!='etc.'];assert options==names,(label,options)
  rows.append(menu(f'{key}-name','Name',1,3,options,f'ONE {label} flooring for the family living room.'))
  for criterion_id,heading in [('description','Description'),('advantage','Advantage'),('disadvantage','Disadvantage')]:rows.append(criterion(f'{key}-{criterion_id}',heading,1,[0,2],'Match this point to the SAME chosen '+label+' flooring. Complete original models: '+body+' The source names linoleum/rugs without separate models and does not supply every evaluative point for every example; no missing detail has been invented.'))
  task_groups.append(dict(sourceCardId=f'he-2013-hl-sc-q1cii-{key}',label=label+' flooring',marks=9,rowIds=[f'{key}-{v}' for v in ['name','description','advantage','disadvantage']]))
 add(1,'c','ii','3-4',18,rows,'Required semi-hard + soft, each name3/description2/advantage2/disadvantage2',taskGroups=task_groups)
 fashion=guide(17,'(one reference to each + one other)','(ii)');heads=['Colour/pattern:','Line/shape:','Accessories:'];rows=[criterion(f'heading-{i}',h[:-1],1,[0,3],v) for i,(h,v) in enumerate(zip(heads,named(fashion,heads)),1)];rows.append(criterion('other','one other',1,[0,3],'One ADDITIONAL point across these required headings. Original 2013 fashion examples: '+fashion));add(2,'a','i','3-8',12,rows,'One per heading3 + one other3')
 custom=guide(17,'Diagram = 4 marks','(iii)');add(2,'a','ii','3-8',7,[criterion('description','Description',1,[0,3],'Describe ONE customisation. The source supplies these examples but no further full model: '+custom),criterion('diagram','Diagram',1,[0,4],'Draw the SAME customisation. No model diagram is printed in the scheme. Source examples: '+custom)],'Description3 + matching diagram4')
 c=add(2,'a','iii','3-8',6,[criterion('function','function',1,[0,3],'Evaluate the FUNCTION of the SAME customised jeans from part(ii). The scheme prints this criterion but no model evaluation.'),criterion('aesthetic','aesthetic appeal',1,[0,3],'Evaluate AESTHETIC APPEAL of the SAME customised jeans from part(ii). The scheme prints this criterion but no model evaluation.')],'Function3 + aesthetic appeal3');c['stem']+='\n\n'+prompt(2,'a','ii')
 nylon=guide(17,'Fibre production:');synthetic=select(s[18],'Synthetic fibres:','Regenerated fibres:');regenerated=select(s[18],'Regenerated fibres:','Fabric properties:');properties=select(s[18],'Fabric properties:','Fibre identification tests:');identification=re.sub(r'\s+or$','',select(s[18],'Fibre identification tests:','2.(c)'));property_bodies=named(properties,['Nylon:','Polyester:','Acrylic:','Viscose/Rayon:','Acetate:']);id_bodies=named(identification,['Nylon:','Polyester:','Acrylic:','Viscose:','Acetate:']);variants=[]
 for i,(label,props,test) in enumerate(zip(['Nylon','Polyester','Acrylic','Viscose/Rayon','Acetate'],property_bodies,id_bodies)):
  production=(nylon+' '+synthetic) if i==0 else synthetic if i<3 else regenerated
  variants.append(dict(id=f'fabric-{i}',label=label,rows=[point('name',label,2),criterion('production','fibre production',3,[0,2],'Three production points about this SAME fibre. Original applicable model/group guidance: '+production+(' No separate detailed manufacturing model is printed for this individual fibre.' if i else '')),criterion('properties','fabric properties',2,[0,2],'Two properties of this SAME fabric. Original model: '+props),criterion('identification','fibre identification test',1,[0,3],'Identification of this SAME fibre. Original model: '+test)]))
 variants.append(dict(id='another-fabric',label='Another manufactured fabric',rows=[criterion('name','Name',1,[0,2],'ONE fabric made from manufactured fibres.'),criterion('production','fibre production',3,[0,2],'Three matching production points. The scheme models nylon and gives synthetic/regenerated group guidance; no additional individual model is printed.'),criterion('properties','fabric properties',2,[0,2],'Two matching properties. No model for another fabric is printed.'),criterion('identification','fibre identification test',1,[0,3],'Identification of the SAME fibre. No model for another fabric is printed.')]))
 add(2,'b',None,'3-7',15,deepcopy(variants[0]['rows']),'Name2 + production3×2 + properties2×2 + identification3',answerVariants=variants)
 judged(2,'c','i','3-8',2,3,'promoted',guide(18,'2 points @ 3 marks each','(ii)'))
 judged(2,'c','ii','3-8',3,3,'textile craft work',guide(18,'3 points @ 3 marks each'))
 work=guide(19,'2 points @ 5 marks each','(ii)');heads=['Paid work:','Unpaid work :'];add(3,'a','i','3-9',10,[criterion(f'type-{i}',h.rstrip(' :'),1,[0,5],v) for i,(h,v) in enumerate(zip(heads,named(work,heads)),1)],'Paid work5 + unpaid work5')
 changes=guide(19,'(1 ref. to social, 1 ref. to economic, 1 ref. to technological + 2 others)','(iii)');heads=['Social:','Economic:','Technological:'];rows=[criterion(f'heading-{i}',h[:-1],1,[0,5],v) for i,(h,v) in enumerate(zip(heads,named(changes,heads)),1)];rows.append(criterion('other','2 others',2,[0,5],'Two ADDITIONAL points across the three required headings; no extra per-heading quota. Source: '+changes));add(3,'a','ii','3-9',25,rows,'Social5/economic5/technological5 + two others5')
 judged(3,'a','iii','3-9',3,5,'attitude to work',guide(19,'3 points @ 5 marks each'))
 poverty=guide(20,'(1 ref. to extent and 1 ref. to distribution + 2 others)','(ii)');extent,distribution=named(poverty,['Extent:','Distribution:']);add(3,'b','i','3-9',20,[criterion('extent','extent',1,[0,5],extent),criterion('distribution','distribution',1,[0,5],distribution),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points across either required heading. Historical 2013 source: '+poverty)],'Extent5 + distribution5 + two others5')
 statutory=re.sub(r'\s+or$','',guide(20,'Social welfare assistance and benefits:','3.(c)'));statutory='Social welfare assistance and benefits: '+statutory
 add(3,'b','ii','3-9',10,[criterion('name','Name',1,[0,5],'Name ONE statutory response. The printed marking scheme awards 5 marks for the name. Complete original examples: '+statutory),criterion('details','details',1,[0,5],'One detail point for the SAME response. The printed marking scheme awards 5 marks for one matching detail. Original guidance: '+statutory)],'Visible source: name5 + one detail5')
 education=select(s[20],'Choice / Types:',include=True)+' '+s[21];heads=['Choice / Types:','Curriculum offered:','Educational supports / resources:','Provision for special needs:'];counts=[3,3,2,2]
 c=add(3,'c',None,'3-10',30,[criterion(f'heading-{i}',h[:-1],count,[0,3],v) for i,(h,count,v) in enumerate(zip(heads,counts,named(education,heads)),1)],'Required headings9 + 9 + 6 + 6');original=part(3,'c');c['stem']=original.split('Discuss primary level education in Ireland.',1)[0].strip();c['questionText']=prompt(3,'c',None).split('Discuss primary level education in Ireland.',1)[1];c['questionText']='Discuss primary level education in Ireland.'+c['questionText']
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=19,marks=275,selectionDecisions='Required/flexible heading quotas and full continuations retained. Paired floor recommendations remain linked9+9. Manufactured-fabric variants preserve individual source models and visible gaps. Customisation diagram/evaluation has no invented model. Visually verified C3(b)(ii) tariff5+5 overrides hidden old4/2×3 text.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
