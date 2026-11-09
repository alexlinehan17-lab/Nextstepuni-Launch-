#!/usr/bin/env python3
"""2014 Ordinary electives: exact quotas, dependent outfit context and visible source gaps."""
from he_review_2014_ol_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(15,23)};cards=[]
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
 electricity=guide(15,'(1 reference to each + 1 other)','(ii)');add(1,'a','i','3-5',18,[criterion('meter','meter box',1,[0,6],'One reference to the meter box. Original shared source: '+electricity),criterion('breakers','miniature circuit breakers',1,[0,6],'One reference to the miniature circuit breakers. Original shared source: '+electricity),criterion('other','1 other',1,[0,6],'One ADDITIONAL point about electricity entering the home, with no fixed two-per-heading quota. Original source: '+electricity)],'Meter box 6 + circuit breakers 6 + one other 6',questionFigureKey='home-economics-2014-ol-sc-q1-electricity',questionFigureIncludesPrompt=False)
 heads=['• fuse','• kilowatt per hour (kWh)','• voltage.'];rows=[criterion(f'term-{i}',head.removeprefix('• ').rstrip('.'),1,[0,4],body) for i,(head,body) in enumerate(zip(heads,named(guide(15,'3 points @ 4 marks each'),heads)),1)];rows[1]['contextNote']='The paper and scheme print “kilowatt per hour (kWh)”. The original term and source explanation are retained as printed. '+rows[1]['contextNote'];add(1,'a','ii','3-5',12,rows,'3 required terms × 4')
 judged(1,'a','iii','3-5',4,5,'guidelines',re.sub(r'\s+and$','',guide(16,'4 guidelines @ 5 marks each','1. (b)')))
 judged(1,'b','i','3-3',3,4,'amenities',guide(16,'3 points @ 4 marks each','(ii)'))
 heads=['• a young single person','• a retired couple','• a family with young children.'];add(1,'b','ii','3-3',18,[criterion(f'household-{i}',head.removeprefix('• ').rstrip('.'),1,[0,6],re.sub(r'\s+or$','',body)) for i,(head,body) in enumerate(zip(heads,named(guide(16,'3 points @ 6 marks each'),heads)),1)],'3 required households × 6')
 judged(1,'c','i','3-5',3,5,'ways',guide(17,'3 ways @ 5 marks each','(ii)'))
 judged(1,'c','ii','3-5',3,5,'factors',guide(17,'3 factors @ 5 marks each'))
 sketch=guide(18,'Sketch: 6 marks, Description: 2 points @ 3 marks each','(ii)');draw,description=named(sketch,['Sketch:','Description:']);add(2,'a','i','3-8',12,[criterion('sketch','Sketch',1,[0,6],'The original scheme gives criteria but no model drawing. Draw the SAME two-piece interview outfit described below. Original criteria: '+draw),criterion('description','Description',2,[0,3],'Two description points for the SAME two-piece outfit. No full model outfit is supplied. Original criteria: '+description)],'Sketch 6 + description 2×3')
 fabric=guide(18,'Fabric = 3 marks, Reason = 3 marks','(iii)');names=chosen(select(fabric,'Fabric:','Reason:'),['cotton','linen','light wool','silk','polyester','acrylic']);reason=select(fabric,'Reason:');c=add(2,'a','ii','3-8',6,[menu('fabric','Fabric',1,3,names,'Choose one fabric suitable for the SAME preceding interview outfit.'),criterion('reason','Reason',1,[0,3],'Give one reason matching the SAME chosen fabric and outfit. The original fabric/reason lists are unpaired; no exact pairings have been invented. Original reason guidance: '+reason)],'Fabric 3 + reason 3');c['stem']+='\n\n'+prompt(2,'a','i')
 principle=re.sub(r'\s+and$','',guide(18,'Name: 4 marks, Explanation: 3 marks','2.(b)'));names=chosen(principle,['Balance','Emphasis','Proportion','Rhythm']);c=add(2,'a','iii','3-8',7,[menu('name','Name',1,4,names,'One principle shown in the SAME outfit sketch.'),criterion('explanation','Explanation',1,[0,3],'Explain the SAME principle in the preceding outfit. Original models: '+principle)],'Name 4 + explanation 3');c['stem']+='\n\n'+prompt(2,'a','i')
 judged(2,'b','i','3-8',3,3,'roles',guide(18,'3 roles @ 3 marks each','(ii)'))
 c=judged(2,'b','ii','3-8',2,3,'career opportunities',guide(18,'2 career opportunities @ 3 marks each'));c['rows'][0]['contextNote']='Describe TWO career opportunities. The original scheme lists names only, without model descriptions; no missing descriptions have been invented. '+c['rows'][0]['contextNote']
 judged(2,'c','i','3-7',1,5,'fabric finishes',guide(19,'1 point @ 5 marks','(ii)'))
 finishes=guide(19,'2 @ 5 marks each ((Name: 3 marks, Detail: 2 marks)');names=chosen(finishes,['Crease resistant','stain resistant','waterproof','anti static','mercerising','flame retardant (Proban)','turbenising','moth proofing']);rows=[];groups=[]
 for i in [1,2]:
  rows.extend([menu(f'name-{i}','Name',1,3,names,'Choose TWO different finishes in total.'),criterion(f'detail-{i}','Detail',1,[0,2],'One detail for the SAME named finish. Complete original models: '+finishes)]);groups.append(dict(sourceCardId=f'he-2014-ol-sc-q2cii-finish-{i}',label=f'Finish {i}',marks=5,rowIds=[f'name-{i}',f'detail-{i}']))
 add(2,'c','ii','3-7',10,rows,'2 finishes × (name 3 + detail 2)',taskGroups=groups)
 judged(3,'a','i','3-9',4,5,'factors',guide(20,'4 factors @ 5 marks each','(ii)'))
 full=guide(20,'(1 reference to each + 1 other)','(iii)');heads=['• role overload','• role conflict','• distribution of parental and homecare responsibilities.'];rows=[criterion(f'heading-{i}',head.removeprefix('• ').rstrip('.'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)];rows.append(criterion('other','1 other',1,[0,5],'One ADDITIONAL point from any required heading. Original source: '+full));add(3,'a','ii','3-11',20,rows,'3 required headings × 5 + one other 5')
 c=judged(3,'a','iii','3-9',2,5,'Family Income Supplement',guide(20,'2 points @ 5 marks each'));c['rows'][0]['contextNote']='Historical 2014 FIS conditions and payment wording retained. '+c['rows'][0]['contextNote']
 full=guide(21,'(1 reference to each + 2 others)','(ii)');importance,impact=named(full,['Importance of leisure:','Impact of recession:']);add(3,'b','i','3-11',20,[criterion('importance','Importance of leisure',1,[0,5],importance),criterion('impact','Impact of recession',1,[0,5],impact),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points across either required heading; no fixed two-per-heading quota. Original source: '+full)],'Importance 5 + impact 5 + two others × 5')
 judged(3,'b','ii','3-11',2,5,'development',re.sub(r'\s+or$','',guide(21,'2 points @ 5 marks each','3.(c)')))
 judged(3,'c','i','3-9',4,5,'reasons',guide(21,'4 reasons @ 5 marks each'))
 agencies=guide(22,'Name: 5 marks, Details: 5 marks');names=chosen(agencies,['St. Vincent De Paul','Simon Community','Focus Ireland']);add(3,'c','ii','3-9',10,[menu('name','Name',1,5,names,'Choose ONE voluntary agency.'),criterion('details','Details',1,[0,5],'One detail for the SAME chosen agency. Complete original source: '+agencies)],'Name 5 + detail 5')
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='Original meter/breaker inputs and required/flexible quotas retained. Outfit sketch6/description6 with no drawing, dependent fabric/principle context and unpaired source reasons explicit. Career descriptions absent from source visibly identified. Two paired finishes, flexible dual-earner and leisure accounts, and complete voluntary-agency continuation preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
