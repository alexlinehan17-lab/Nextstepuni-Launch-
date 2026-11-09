#!/usr/bin/env python3
"""2015 Higher electives: original profiles, compulsory points and source model gaps."""
from copy import deepcopy
from he_review_2015_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(16,24)};cards=[]
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
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 heads=['Ergonomics:','Aesthetics:','Comfort:'];add(1,'a','i','3-4',18,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(guide(16,'3 points @ 6 marks each','(ii)'),heads)),1)],'Three required design headings×6')
 grid=table_rows(d['scheme'][15].find_tables().tables[0],d['scheme'][15]);assert len(grid)==3,grid;rows=[];groups=[]
 for i,(kind,properties,uses) in enumerate(grid[1:],1):
  rows.extend([criterion(f'properties-{i}','Properties',2,[0,4],kind+' '+properties),criterion(f'examples-uses-{i}','Examples and Uses',2,[0,1],kind+' Cover both an example and its matching use within the TWO one-mark points for this type. Original table: '+uses)])
  groups.append(dict(sourceCardId=f'he-2015-hl-sc-q1aii-type-{i}',label=kind.rstrip(':'),marks=10,rowIds=[f'properties-{i}',f'examples-uses-{i}']))
 add(1,'a','ii','3-4',20,rows,'Two required types×(properties2×4 + examples/uses2×1)',taskGroups=groups,figureKey='home-economics-2015-hl-sc-q1aii-plastics')
 full=re.sub(r'\s+and$','',guide(17,'3 points @ 4 marks each','1.(b)'));effects,prevention=named(full,['Effects:','Reduce/prevent:']);add(1,'a','iii','3-5',12,[criterion('effects','Effects',1,[0,4],effects),criterion('prevention','Reduce/prevent',1,[0,4],prevention),criterion('other','condensation',1,[0,4],'One ADDITIONAL point from either requested heading, THREE total points; no fixed two-per-heading quota. Complete original source: '+full)],'Three points×4 covering both effects and prevention')
 c=judged(1,'b','i','3-5',3,4,'charges',guide(17,'3 charges @ 4 marks each','(ii)'));c['rows'][0]['contextNote']='Three DIFFERENT charges, each named and explained; no separate name/explanation marks are printed. Historical 2015 bill wording/rates retained. '+c['rows'][0]['contextNote']
 heads=['Fuses:','Miniature Circuit Breakers (MCB):','Earth wire:'];add(1,'b','ii','3-5',18,[criterion(f'device-{i}',head.rstrip(':'),1,[0,6],re.sub(r'\s+or$','',body)) for i,(head,body) in enumerate(zip(heads,named(guide(17,'3 points @ 6 marks each'),heads)),1)],'Three required safety devices×6')
 full=guide(18,'(Expect reference to underlined + 3 others)','(ii)');add(1,'c','i','3-5',15,[criterion('service-pipe','service pipe',1,[0,3],'Required underlined part. Original system description: '+full),criterion('stopcock','stopcock',1,[0,3],'Required underlined part. Original system description: '+full),criterion('other','3 others',3,[0,3],'Three ADDITIONAL system points. Original description: '+full)],'Required service pipe3 + stopcock3 + three others×3')
 full=guide(18,'3 points @ 5 marks each');supply,quality,charges=named(full,['Rural areas:','Water quality:','Water charges:']);add(1,'c','ii','3-5',15,[criterion('supply','sources of domestic water',1,[0,5],'Choose EITHER rural OR urban sources for this required heading; both original models retained. '+supply),criterion('quality','water quality',1,[0,5],quality),criterion('charges','water charges',1,[0,5],'Historical 2015 examination conditions/rates are retained. '+charges)],'Three required headings×5')
 add(2,'a','i','3-8',9,[criterion('sketch','Sketch',1,[0,5],'The original scheme gives Sketch = 5 marks, without a model drawing or smaller allocations. Draw the SAME playsuit/jumpsuit described in your answer, suitable for your chosen occasion.'),criterion('description','Description',1,[0,4],'The original scheme gives Description = 4 marks, without a model description or smaller allocations. Describe the SAME chosen garment and occasion.')],'Sketch5 + description4')
 measurements=guide(19,'2 points @ 2marks each','• type of fabric');fabric=guide(19,'Type of fabric: 2 marks, Reason: 2 marks','• outline plan');names=chosen(fabric,['Cotton','polyester cotton','denim','viscose']);plan=re.sub(r'\s+and$','',guide(19,'(expect reference to underlined)','2.(b)'))
 rows=[criterion('measurements','body measurements required',2,[0,2],measurements),menu('fabric','Type of fabric',1,2,names,'Choose one fabric suitable for the SAME preceding garment.'),criterion('reason','Reason',1,[0,2],'Give a reason for the SAME selected fabric and garment. The original source lists fabric names only; it supplies no reason models and none have been invented.'),criterion('layout','layout/ pattern pieces on fabric',1,[0,2],'Required underlined stage. Complete original plan for the SAME garment: '+plan),criterion('pin-tack','pin and tack pieces together',1,[0,2],'Required underlined stage. Complete original plan for the SAME garment: '+plan),criterion('other-stages','outline plan of work',2,[0,2],'Two ADDITIONAL stages from the complete original work plan for the SAME garment: '+plan)]
 c=add(2,'a','ii','3-8',16,rows,'Measurements2×2 + fabric2/reason2 + plan4×2');c['stem']+='\n\n'+prompt(2,'a','i')
 full=guide(19,'Name of fabric: 3 marks')+' '+s[20].split('2.(c)',1)[0];full=re.sub(r'\s+or$','',full);names=['Cotton','Linen','Wool','Silk'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(full,names)),1):
  production,properties,uses=named(body,['Fibre production:','Properties:','Uses:']);variants.append(dict(id=f'source-{i}',label=name,rows=[point('name',name,3),criterion('production','fibre production',3,[0,2],'Three production points for this SAME fabric. '+production),criterion('properties','fabric properties',3,[0,1],'Three properties of this SAME fabric. '+properties),criterion('uses','uses',3,[0,1],'Three uses of this SAME fabric. '+uses)]))
 variants.append(dict(id='another-fabric',label='Another valid natural fabric',rows=[criterion('name','Name of fabric',1,[0,3],'One fabric manufactured from natural fibres; use that SAME fabric throughout. Four original models are available.'),criterion('production','fibre production',3,[0,2],'Three matching production points; no additional model is printed.'),criterion('properties','fabric properties',3,[0,1],'Three matching properties; no additional model is printed.'),criterion('uses','uses',3,[0,1],'Three matching uses; no additional model is printed.')]))
 add(2,'b',None,'3-7',15,deepcopy(variants[0]['rows']),'Name3 + production3×2 + properties3×1 + uses3×1',answerVariants=variants)
 judged(2,'c','i','3-8',2,3,'music and/or musicians',guide(20,'2 points @ 3 marks each','(ii)'))
 judged(2,'c','ii','3-8',3,3,'examples',guide(20,'3 examples @ 3 marks each'))
 full=guide(21,'(1 ref. to individual, 1 ref. to family + 3 others)','(ii)');add(3,'a','i','3-9',20,[criterion('individual','individual',1,[0,4],'One effect on individuals. Complete original shared source: '+full),criterion('family','family',1,[0,4],'One effect on families. Complete original shared source: '+full),criterion('other','3 others',3,[0,4],'Three ADDITIONAL points from either required heading. Complete original shared source: '+full)],'Individual4 + family4 + three others×4')
 # This page has two identical five-point tariffs; narrow to part(ii) first.
 c=judged(3,'a','ii','3-11',5,4,'flexibility',select(select(s[21],'(ii)'),'5 points @ 4 marks each'));c['rows'][0]['contextNote']='Historical 2015 leave and employment conditions retained. '+c['rows'][0]['contextNote']
 full=re.sub(r'\s+and$','',guide(22,'Name: 2 marks. Details: 2 points @ 4 marks each','3.(b)'));names=chosen(full,['IDA','Solas','Enterprise Ireland','County / City Enterprise Boards','Údarás na Gaeltachta','JobBridge']);add(3,'a','iii','3-9',10,[menu('name','Name',1,2,names,'Choose ONE original historical initiative; all details must match it.'),criterion('details','Details',2,[0,4],'Two details of the SAME selected initiative. Complete original historical models: '+full)],'Name2 + details2×4')
 judged(3,'b','i','3-10',3,5,'supports',guide(22,'3 supports @ 5 marks each','(ii)'))
 judged(3,'b','ii','3-10',3,5,'education',guide(22,'3 points @ 5 marks each'))
 heads=['Physical development:','Social development:','Emotional development:'];add(3,'c','i','3-11',18,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(guide(23,'3 points @ 6 marks each','(ii)'),heads)),1)],'Three required development headings×6')
 full=guide(23,'Name = 2 marks, Evaluate: (2 points @ 2 mark each) x 2');names=semis(select(full,'Name:','Evaluate:'));evaluation=select(full,'Evaluate:');rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'name-{i}','Name',1,2,names,'Choose TWO different facilities in total.'),criterion(f'evaluation-{i}','Evaluate',2,[0,2],'Two evaluation points for the SAME selected facility, in the retired-person context. Original shared guidance: '+evaluation+' The source gives facility names and shared evaluation criteria, not complete facility-specific models.')]);groups.append(dict(sourceCardId=f'he-2015-hl-sc-q3cii-facility-{i}',label=f'Facility {i}',marks=6,rowIds=[f'name-{i}',f'evaluation-{i}']))
 add(3,'c','ii','3-11',12,rows,'Two facilities×(name2 + evaluation2×2)',taskGroups=groups)
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=19,marks=275,selectionDecisions='Required design headings and both plastic profiles retained, flexible condensation allocation covers both asks. Compulsory water-system and garment-construction points visible. Sketch/description/reason source gaps explicit; all four natural-fabric profiles retained. Historical water/work/initiative guidance and paired leisure facilities preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
