#!/usr/bin/env python3
"""2016 Ordinary C: required profiles, full original models and continuation text."""
from copy import deepcopy
from he_review_2016_ol_main import *
def build():
 d=documents();norm=lambda v:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',v);p={n:norm(text(d['paper'],n+8)) for n in [1,2,3]};s={n:norm(text(d['scheme'],n)) for n in range(15,23)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def prompt(n,letter,roman):
  v=select(part(n,letter),f'({roman})');v=re.split(r'\((?:i|ii|iii)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  stem=part(n,letter).split('(i)',1)[0].strip();c=card(f'sc-q{n}{letter}{roman}','C',f'E{n} Q{n}({letter})({roman})',topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra)
  if n==1 and letter=='a':c.update(questionFigureKey='home-economics-2016-ol-sc-q1-kitchen',questionFigureIncludesPrompt=False)
  if n==2 and letter=='a':c.update(questionFigureKey='home-economics-2016-ol-sc-q2-suits',questionFigureIncludesPrompt=False)
  cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 full=guide(15,'(1 reference to each plus 1 other)','(ii)');heads=['Suitability for family use:','Ventilation:','Ergonomics:'];rows=[criterion(f'heading-{i}',head.rstrip(':'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)];rows.append(criterion('other','1 other',1,[0,5],'One ADDITIONAL point from any of the THREE required headings. '+full));add(1,'a','i','3-4',20,rows,'Three required headings×5 + one other5')
 judged(1,'a','ii','3-6',3,5,'factors',guide(15,'3 factors @ 5 marks each'))
 judged(1,'a','iii','3-6',3,5,'ways',stripjoin(guide(16,'3 ways @ 5 marks each','1.(b)')))
 judged(1,'b','i','3-4',4,5,'factors',guide(16,'4 factors @ 5 marks each','(ii)'))
 full=stripjoin(guide(16,'Name: 4 marks, Properties: 2 @ 3 marks each'));names=['Tiles:','Vinyl:','Wooden flooring:','Safety flooring:'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(full,names)),1):
  variants.append(dict(id=f'floor-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),4),criterion('properties','Properties',2,[0,3],'Two properties of the SAME chosen bathroom floor covering. Complete original model: '+body)]))
 variants.append(dict(id='another-floor',label='Another valid floor covering',rows=[criterion('name','Name',1,[0,4],'Choose ONE suitable family-bathroom floor covering; all four original models remain available.'),criterion('properties','Properties',2,[0,3],'Two properties of that SAME covering. No additional source model is printed.')]))
 add(1,'b','ii','3-4',10,deepcopy(variants[0]['rows']),'Name4 + properties2×3',answerVariants=variants)
 judged(1,'c','i','3-3',3,4,'rental accommodation',guide(17,'3 points @ 4 marks each','(ii)'))
 full=guide(17,'Name: 3 @ 3marks each, Reasons: 3 @ 3marks each');heads=['(a) college student:','(b) person with reduced mobility:','(c) elderly couple:'];rows=[];groups=[]
 for i,(head,body) in enumerate(zip(heads,named(full,heads)),1):
  types,reasons=body.split('reasons:',1);rows.extend([criterion(f'name-{i}','Name',1,[0,3],'Name ONE suitable accommodation type for this required group. All original options: '+types),criterion(f'reason-{i}','Reasons',1,[0,3],'Give ONE reason matching the SAME selected accommodation and this required group. '+reasons)])
  groups.append(dict(sourceCardId=f'he-2016-ol-sc-q1cii-group-{i}',label=head[4:].rstrip(':'),marks=6,rowIds=[f'name-{i}',f'reason-{i}']))
 add(1,'c','ii','3-3',18,rows,'Three required groups×(name3 + reason3)',taskGroups=groups)
 heads=['function:','comfort:','aesthetic appeal:'];add(2,'a','i','3-8',18,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(guide(18,'3 points @ 6 marks each','(ii)'),heads)),1)],'Three required office-suit headings×6')
 full=stripjoin(guide(18,'Name: 3 marks, Reason: 1 point @ 4 marks'));names=['wool:','linen:','cotton:','silk:','polyester:','viscose/rayon:','acrylic:','polyester cotton:'];variants=[]
 # The word cotton also occurs inside the final blended-fabric name; split
 # exact model starts following the original punctuation, not loose tokens.
 bodies=re.split(r'(?<=etc\.)\s+(?=(?:linen|cotton|silk|polyester|viscose/rayon|acrylic|polyester cotton):)',full);assert len(bodies)==8,bodies
 for i,(name,body) in enumerate(zip(names,bodies),1):
  assert body.startswith(name),(name,body)
  variants.append(dict(id=f'fabric-{i}',label=name.rstrip(':'),rows=[point('name',name.rstrip(':'),3),criterion('reason','Reason',1,[0,4],'ONE reason for the SAME selected fabric in the pictured suit-jacket context. '+body)]))
 variants.append(dict(id='another-fabric',label='Another valid fabric',rows=[criterion('name','Name',1,[0,3],'One suitable fabric for the pictured suit jacket; all eight source models remain available.'),criterion('reason','Reason',1,[0,4],'One reason for the SAME fabric. No additional source model is printed.')]))
 add(2,'a','ii','3-8',7,deepcopy(variants[0]['rows']),'Name3 + reason4',answerVariants=variants)
 production=guide(19,'3 points @ 2 marks each','• how fabric is constructed.');construction=guide(19,'1 point @ 3 marks','(ii)');names=['linen:','cotton:','wool:','silk:'];variants=[]
 for i,(name,body) in enumerate(zip(names,named(production,names)),1):
  variants.append(dict(id=f'natural-{i}',label=name.rstrip(':'),rows=[criterion('production','fibre production',3,[0,2],'Three production points for this SAME natural fabric. No separate name marks are printed. '+body),criterion('construction','how fabric is constructed',1,[0,3],'One construction account appropriate to the SAME fabric. Complete original weaving/knitting/bonding pool: '+construction)]))
 variants.append(dict(id='another-natural',label='Another valid natural fabric',rows=[criterion('production','fibre production',3,[0,2],'Three production points for ONE natural fabric consistently; no additional source model is printed.'),criterion('construction','how fabric is constructed',1,[0,3],'One account appropriate to the SAME fabric. Complete original construction pool: '+construction)]))
 add(2,'b','i','3-7',9,deepcopy(variants[0]['rows']),'Production3×2 + construction3',answerVariants=variants)
 judged(2,'b','ii','3-7',2,3,'advantages',stripjoin(guide(19,'2 advantages @ 3 marks each','2.(c)')))
 judged(2,'c','i','3-8',3,3,'media',select(select(s[19],'2.(c)'),'3 points @ 3 marks each','(ii)'))
 judged(2,'c','ii','3-8',2,3,'contribution',guide(19,'2 contributions @ 3 marks each'))
 heads=['Paid work:','Unpaid work:','Voluntary work:'];add(3,'a','i','3-11',18,[criterion(f'type-{i}',head.rstrip(':'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(guide(20,'3 points @ 6 marks each','(ii)'),heads)),1)],'Three required work types×6')
 full=guide(20,'(1 advantage, 1 disadvantage, plus 2 others)','(iii)');advantages,disadvantages=named(full,['Advantages:','Disadvantages:']);add(3,'a','ii','3-11',20,[criterion('advantage','advantage',1,[0,5],advantages),criterion('disadvantage','disadvantage',1,[0,5],disadvantages),criterion('other','2 others',2,[0,5],'Two ADDITIONAL points from either required heading. '+full)],'Advantage5 + disadvantage5 + two others×5')
 c=judged(3,'a','iii','3-11',3,4,'protect young people',guide(20,'3 points @ 4 marks each'));c['rows'][0]['contextNote']='Original historical 2016 employment conditions and €6.06 minimum-wage wording retained. '+c['rows'][0]['contextNote']
 judged(3,'b','i','3-10',3,6,'reasons',guide(21,'3 reasons @ 6 marks each','(ii)'))
 full=stripjoin(guide(21,'Name: 4 marks, Details: 2 points @ 4 marks each','3.(c)'));options=semis(full);add(3,'b','ii','3-10',12,[menu('name','Name',1,4,options,'Choose ONE adult-education initiative consistently. Complete original historical source names/brief descriptors retained.'),criterion('details','Details',2,[0,4],'Two details of the SAME initiative. The original supplies names and brief descriptors only, not complete two-point worked accounts; no additional model has been invented. '+full)],'Name4 + details2×4')
 judged(3,'c','i','3-11',1,6,'leisure',guide(21,'1 point @ 6 marks','(ii)'))
 full=guide(21,'4 points @ 6 marks each')+' '+s[22];heads=['Age:','Occupation:','Culture:','Cost:'];add(3,'c','ii','3-11',24,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,6],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)],'Four required leisure headings×6')
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=20,marks=275,selectionDecisions='Kitchen and both suits retain original pictures and required headings; all three required accommodation name/reason pairs remain coherent18. All floor-covering, suit-fabric and natural-fabric choices retained with matching criteria. Source-only adult-initiative guidance and the full leisure continuation through scheme22 preserved.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
