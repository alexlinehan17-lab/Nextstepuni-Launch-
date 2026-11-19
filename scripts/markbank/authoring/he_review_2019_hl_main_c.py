#!/usr/bin/env python3
"""2019 Higher electives: original partial ladders, complete pools and visible source gaps."""
from he_review_2019_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(16,23)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,letter):return stripjoin(select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None))
 def prompt(n,letter,roman):return re.sub(r'\s*\(\d+\)\s*$','',re.split(r'\((?:i|ii|iii|iv)\)',select(part(n,letter),f'({roman})'),1)[0]).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  c=card(f'sc-q{n}{letter}{roman}','C',f'E{n} Q{n}({letter})({roman})',topic,prompt(n,letter,roman),part(n,letter).split('(i)',1)[0].strip(),marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,steps,label,guidance,**extra):return add(n,letter,roman,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; printed steps '+str(steps),**extra)
 judged(1,'a','i','3-3',5,[0,2,4],'housing styles','The original scheme requires reference to TWO centuries across FIVE points, with no fixed points-per-century quota. Keep that requirement when assessing. All three original century models remain available: '+guide(16,'19th Century:','(ii)',True))
 full=guide(16,'Economic: income',include=True);heads=['Economic:','Environmental:'];models=named(full,heads)
 add(1,'a','ii','3-3',18,[criterion('economic','economic factor',1,[0,2,4,6],models[0]),criterion('environmental','environmental factor',1,[0,2,4,6],models[1]),criterion('other','1 other',1,[0,2,4,6],'One ADDITIONAL point from either required category. '+full)],'One economic6 + one environmental6 + one additional6')
 judged(1,'a','iii','3-3',4,[0,1,2,3],'professional services','Four service details; names alone are not complete accounts. Original explained and name-only choices: '+stripjoin(guide(17,'Architect:','1.(b)',True)))
 judged(1,'b','i','3-4',4,[0,2,4],'factors',guide(17,'(graded 4:2:0)','(ii)'))
 full=stripjoin(guide(17,'Water-based paint:',include=True));rows=[];groups=[]
 for i in [1,2]:
  ids=[f'name-{i}',f'description-{i}',f'properties-{i}']
  rows += [criterion(ids[0],'Name',1,[0,1],f'Choose TWO different wall finishes. Name selected finish {i}. Preserve each description/property relationship in the complete source pool: '+full),criterion(ids[1],'Description',1,[0,2],f'Describe the SAME finish {i}. Paint and wallpaper subtypes retain their shared property lists; tiles retain their own model. Wood panelling, mosaic and stone are name-only alternatives; no description is invented. '+full),criterion(ids[2],'Properties',2,[0,2],f'Two properties of the SAME finish {i}. '+full)]
  groups.append(dict(sourceCardId=f'he-2019-hl-sc-q1bii-finish-{i}',label=f'Wall finish {i}',marks=7,rowIds=ids))
 add(1,'b','ii','3-4',14,rows,'Two finishes×(name1 + description2 + two properties2)',taskGroups=groups)
 full=guide(18,'Ring circuit:','(ii)',True);heads=['Ring circuit:','MCB:'];add(1,'c','i','3-5',12,[criterion(f'part-{i}',head.rstrip(':'),3,[0,1,2],model+' Accept clearly labelled diagrams.') for i,(head,model) in enumerate(zip(heads,named(full.replace('Accept clearly labelled diagrams',''),heads)),1)],'BOTH ring circuit and MCB: three points2 each')
 judged(1,'c','ii','3-5',6,[0,2,3],'guidelines',guide(18,'(graded 3:2:0)'))
 judged(2,'a','i','3-8',5,[0,2,3],'factors',select(s[19].split('(ii)',1)[0],'(graded 3:2:0)'))
 add(2,'a','ii','3-8',10,[criterion('sketch','Sketch',1,[0,2,4],'Sketch an outfit suitable for an outdoor music festival. The original scheme prints the sketch tariff but no model outfit; none is invented.'),criterion('description','Description',1,[0,2,4,6],'Describe the SAME outfit. Accept description on labelled sketch. The original scheme gives no model outfit description.')],'Sketch4 [0,2,4] + description6 [0,2,4,6]')
 judged(2,'b','i','3-7',3,[0,2,3],'constructed',select(select(s[19],'2.(b)','(ii)'),'(graded 3:2:0)'))
 add(2,'b','ii','3-7',6,[criterion('properties','Properties',3,[0,1],guide(19,'Properties: warm','3 uses',True)),criterion('uses','Uses',3,[0,1],stripjoin(guide(19,'Uses:',include=True)))],'Three properties1 + three uses1')
 designers=guide(20,'Simone Rocca;','(ii)',True)
 add(2,'c','i','3-8',6,[criterion('name','Name',1,[0,2],'Choose ONE contemporary Irish designer. Complete original name pool: '+designers),criterion('details','Details',2,[0,2],'Give TWO details about the SAME selected designer. The source prints accepted names only; no biographical/work models are printed or invented. '+designers)],'One name2 + two matching details2')
 judged(2,'c','ii','3-8',3,[0,2,3],'economy',guide(20,'(graded 3:2:0)'))
 full=guide(21,'Primary:','(ii)',True);heads=['Primary:','Secondary:','Tertiary:'];add(3,'a','i','3-9',12,[criterion(f'sector-{i}',head.rstrip(':'),1,[0,2,4],'Comment on this REQUIRED sector, relating its contribution to the food industry. Original model: '+model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Required primary/secondary/tertiary contributions4 each')
 full=guide(21,'Positive: interesting','(iii)',True);heads=['Positive:','Negative:'];add(3,'a','ii','3-9',16,[criterion(f'effect-{i}',head.rstrip(':'),2,[0,2,4],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Two positive4 + two negative4')
 judged(3,'a','iii','3-10',2,[0,2,3,5],'educational qualifications',guide(21,'(graded 5:3:2:0)','(iv)'))
 full=guide(21,'Safety, Health and Welfare at Work Act 2005:',include=True)+' '+stripjoin(select(s[22],'Organisation of Working Time Act 1997:','3.(b)',True))
 judged(3,'a','iv','3-9',3,[0,1,2,3,4],'legislation','Explain protection WITH examples across three points; no separate statute/example quota is printed. Original historical 2019 account, including all page-22 continuation choices: '+full)
 judged(3,'b','i','3-11',4,[0,2,3],'factors',select(select(s[22],'3.(b)','(ii)'),'(graded 3:2:0)'))
 pool=stripjoin(guide(22,'Montessori;','3.(c)',True));rows=[];groups=[]
 for i in [1,2]:
  ids=[f'name-{i}',f'evaluation-{i}'];rows += [criterion(ids[0],'Name',1,[0,1],f'Name different childcare option {i} of TWO. Original choices: '+pool),criterion(ids[1],'Evaluate',4,[0,1,2],f'Evaluate the SAME option {i} across four points. The scheme supplies accepted option names only, with no evaluation models; none are invented. '+pool)]
  groups.append(dict(sourceCardId=f'he-2019-hl-sc-q3bii-childcare-{i}',label=f'Childcare option {i}',marks=9,rowIds=ids))
 add(3,'b','ii','3-11',18,rows,'Two options×(name1 + four evaluation points2)',taskGroups=groups)
 judged(3,'c','i','3-9',4,[0,1,3],'groups','Identify/discuss groups AND give reasons across four points; no separate group/reason allocation is printed. The original guidance lists groups without model reasons; none are invented. '+select(select(s[22],'3.(c)','(ii)'),'(graded 3:1:0)'))
 judged(3,'c','ii','3-9',6,[0,2,3],'social policy','Discuss social policy AND include the state response across six points; the source sets no fixed policy/response quota. Original historical account: '+guide(22,'Social Policy:',include=True))
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='Two-century requirement and economic/environmental/additional quota; full wall-finish paired pools; both electrical-system accounts; original sketch/description ladders; all designer names with visible absence of detail models; all three industrial sectors; employment-law continuation; two coherent childcare profiles with source-model gaps; poverty reasons and state response requirements.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
