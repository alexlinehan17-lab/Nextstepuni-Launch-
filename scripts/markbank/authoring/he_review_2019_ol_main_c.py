#!/usr/bin/env python3
"""2019 Ordinary electives: paired profiles, original source gaps and exact ladders."""
from copy import deepcopy
from he_review_2019_ol_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(15,22)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,letter):return stripjoin(select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None))
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:v=re.split(r'\((?:i|ii|iii|iv)\)',select(v,f'({roman})'),1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  stem=part(n,letter).split('(i)',1)[0].strip() if roman else ''
  if n==1 and letter=='a':stem=stem.split('(www.cbaarchitecture.ie)',1)[0].strip()
  if n==2 and letter=='a':stem=stem.split('(www.lidl.co.uk)',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,steps,label,guidance,**extra):return add(n,letter,roman,topic,count*steps[-1],[criterion('points',label,count,steps,guidance)],f'{count} points; original steps '+str(steps),**extra)
 judged(1,'a','i','3-3',3,[0,2,5],'environmental factors',select(s[15].split('(ii)',1)[0],'(graded 5:2:0)'),questionFigureKey='home-economics-2019-ol-sc-q1-house',questionFigureIncludesPrompt=False)
 full=guide(15,'Family requirements:',include=True);heads=['Family requirements:','Energy efficiency:','Technological developments:','Cost:'];add(1,'a','ii','3-3',20,[criterion(f'influence-{i}',head.rstrip(':'),1,[0,2,5],'Explain this REQUIRED influence. '+model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'All FOUR required house-design influences5')
 judged(1,'a','iii','3-3',5,[0,3],'steps','Original historical 2019 planning procedure and application fee: '+stripjoin(select(s[16].split('1.(b)',1)[0],'(graded 3:0)')))
 judged(1,'b','i','3-5',3,[0,2,4,6],'factors',select(select(s[16],'1.(b)','(ii)'),'(graded 6:4:2:0)'))
 full=stripjoin(guide(16,'Sensor and motion activated lights;','1.(c)',True));rows=[];groups=[]
 for i in [1,2]:
  ids=[f'name-{i}',f'details-{i}'];rows += [criterion(ids[0],'Name',1,[0,3],f'Name different lighting development {i} of TWO. Original choices: '+full),criterion(ids[1],'Details',1,[0,2,3],f'Give details for the SAME selected development {i}. The original source lists choices without detailed model accounts; none are invented. '+full)];groups.append(dict(sourceCardId=f'he-2019-ol-sc-q1bii-light-{i}',label=f'Lighting development {i}',marks=6,rowIds=ids))
 add(1,'b','ii','3-5',12,rows,'Two developments×(name3 + matching details3)',taskGroups=groups)
 types=guide(16,'Type: full central heating:',include=True);fuels=guide(17,'Fuel/energy source:','Efficiency and convenience:',True);efficiency=guide(17,'Efficiency and convenience:','(ii)',True)
 add(1,'c','i','3-5',15,[criterion('name','Name',1,[0,3],'Choose ONE heating system consistently throughout all four criteria. Original complete and name-only choices: '+types),criterion('type','type of heating system',1,[0,2,4],'Describe the SAME selected system; no additional model is invented for Air to water heat exchanger, which is accepted by name only. '+types),criterion('fuel','fuel/energy source',1,[0,4],'State a fuel/energy source appropriate to the SAME selected system. Complete original pool, without invented system/fuel pairings: '+fuels),criterion('efficiency','efficiency and convenience',1,[0,2,4],'Explain efficiency/convenience appropriate to the SAME selected system. Select matching guidance from the original pool: '+efficiency)],'Name3 + type4 + fuel4 + efficiency/convenience4')
 judged(1,'c','ii','3-5',3,[0,2,5],'benefits','Choose ANY THREE timer and/or thermostat benefits; no fixed category quota. '+guide(17,'Timers:',include=True))
 full=guide(18,'Comfort:','(ii)',True);heads=['Comfort:','Aesthetic appeal:','Shape:'];fig=dict(questionFigureKey='home-economics-2019-ol-sc-q2-leisure',questionFigureIncludesPrompt=False)
 add(2,'a','i','3-8',18,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,1,3],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Two required points3 for EACH comfort/aesthetic appeal/shape',**fig)
 full=stripjoin(guide(18,'Sketch: clearly labelled','2.(b)',True));models=named(full,['Sketch:','Description:']);add(2,'a','ii','3-8',7,[criterion('sketch','Sketch',1,[0,1,3],models[0]),criterion('description','Description',1,[0,2,4],models[1])],'Sketch3 [0,1,3] + matching description4 [0,2,4]',**fig)
 production=guide(19,'Fibre production:','Accept:');props=guide(19,'Properties:','Fabric construction technique:');construction=stripjoin(guide(19,'Fabric construction technique:','2.(c)',True));productions=named(production,['Viscose (rayon fibre):','Nylon:']);properties=named(props,['Viscose:','Nylon:']);variants=[]
 for i,label in enumerate(['Viscose','Nylon','Acetate','tri-acetate','Polyester','Acrylic','Another valid manufactured fabric']):
  model=productions[i] if i<2 else 'The original source accepts this fibre by name only; no production model is printed or invented.' if i<6 else 'The source leaves valid alternatives open; no further production model is printed or invented.'
  property_model=properties[i] if i<2 else 'No property model is printed or invented for this additional selected fabric.'
  rows=[criterion('production','fibre production',2,[0,1,3],f'Write ONE coherent {label} fabric profile throughout. '+model),criterion('properties','properties',3,[0,1],f'Three properties of the SAME selected fabric. '+property_model),criterion('construction','fabric construction technique',2,[0,1,3],'Explain a construction technique appropriate to the SAME selected fabric across two points. Both original weaving and knitting models are available; there is no requirement to describe both. '+construction)]
  variants.append(dict(id=f'fabric-{i+1}',label=label,rows=rows))
 add(2,'b','', '3-7',15,deepcopy(variants[0]['rows']),'One profile: two production3 + three properties1 + two construction3',answerVariants=variants)
 judged(2,'c','i','3-8',3,[0,1,3],'points',select(select(s[19],'2.(c)','(ii)'),'(graded 3:1:0)'))
 judged(2,'c','ii','3-8',2,[0,1,3],'information','Explain the importance of ONE selected pattern-envelope information item across two points; do not require two different items. Complete source choices: '+select(select(select(s[19],'2.(c)'),'(ii)'),'(graded 3:1:0)'))
 judged(3,'a','i','3-10',2,[0,3],'adult and second-chance education','Explain this combined concept across TWO points; the source does not allocate one point to each term separately. '+select(s[20].split('(ii)',1)[0],'(graded 3:0)'))
 judged(3,'a','ii','3-10',4,[0,2,4],'reasons',select(select(s[20],'(ii)','(iii)'),'(graded 4:2:0)'))
 judged(3,'a','iii','3-10',4,[0,2,4],'ways',select(select(s[20],'(iii)','(iv)'),'(graded 4:2:0)'))
 judged(3,'a','iv','3-9',3,[0,2,4],'protects','Original historical 2019 source account of the 1996 Act: '+stripjoin(select(select(s[20],'(iv)','3.(b)'),'(graded 4:2:0)')))
 judged(3,'b','i','3-11',3,[0,2,5],'benefits',guide(20,'(graded 5:2:0)'))
 full=stripjoin(guide(21,'Physical:','3.(c)',True));heads=['Physical:','Social:','Emotional:'];add(3,'b','ii','3-11',15,[criterion(f'development-{i}',head.rstrip(':'),1,[0,2,5],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Required physical/social/emotional accounts5 EACH')
 judged(3,'c','i','3-9',3,[0,2,5],'reasons',select(select(s[21],'3.(c)','(ii)'),'(graded 5:2:0)'))
 full=guide(21,'St. Vincent de Paul:',include=True);heads=['St. Vincent de Paul:','Simon Community:','Focus Ireland:'];models=named(full.split('Lions Club;',1)[0],heads);variants=[]
 for i,label in enumerate(['St. Vincent de Paul','Simon Community','Focus Ireland','Lions Club','Rotary Club','Another valid voluntary organisation']):
  name_row=point('name',label,3) if i<5 else criterion('name','Name',1,[0,3],'Name ONE valid voluntary organisation helping families experiencing poverty; the source leaves valid alternatives open.')
  model=models[i] if i<3 else 'This organisation is accepted by name only; no detail model is printed or invented.' if i<5 else 'No additional detail model is printed or invented.'
  variants.append(dict(id=f'organisation-{i+1}',label=label,rows=[name_row,criterion('details','Details',3,[0,2,4],'Give THREE details about the SAME named organisation. '+model)]))
 add(3,'c','ii','3-9',15,deepcopy(variants[0]['rows']),'One organisation name3 + three matching details4',answerVariants=variants)
 assert len(cards)==20 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=20,marks=275,selectionDecisions='All house/photo contexts and four design requirements, original planning tariff/fee, coherent lighting/heating selections with visible source gaps, complete leisure photo for both linked asks, all manufactured-fibre choices and appropriate construction methods, ONE pattern-envelope item across two points, education/worker-protection source tariffs, required leisure-development headings, all paired organisation alternatives and page continuations.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
