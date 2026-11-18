#!/usr/bin/env python3
"""2018 Ordinary electives: original paired profiles and descending crest tariff."""
from copy import deepcopy
from he_review_2018_ol_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,21)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,letter):return stripjoin(select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None))
 def prompt(n,letter,roman):
  v=select(part(n,letter),f'({roman})');v=re.split(r'\((?:i|ii|iii|iv)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip()
  if n==1 and letter=='a':stem=stem.split('(www.engineersireland.ie)',1)[0].strip()+' (www.engineersireland.ie)'
  if n==2 and letter=='a':stem=stem.split('(www.aldi.ie)',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman}','C',f'E{n} Q{n}({letter})({roman})',topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 full=guide(14,'(18)','(ii)');heads=['stopcock','ball valve (ballcock)','overflow pipe.'];add(1,'a','i','3-5',18,[criterion(f'part-{i}',head.rstrip('.'),2,[0,3],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Three required parts×two function points3',questionFigureKey='home-economics-2018-ol-sc-q1-water',questionFigureIncludesPrompt=False)
 full=guide(14,'4 stages @ 4 marks each');heads=['Screening:','Chlorination:','Fluoridation:','Testing:'];add(1,'a','ii','3-5',16,[criterion(f'stage-{i}',head.rstrip(':'),1,[0,4],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Four required stages4')
 c=judged(1,'a','iii','1-5',4,4,'conserving water',stripjoin(guide(15,'4 ways @ 4 marks each','1.(b)')));c['rows'][0]['contextNote']='Choose ANY FOUR conservation ways across all source headings; no toilet/tap/appliance/water quota. '+c['rows'][0]['contextNote']
 c=judged(1,'b','i','3-3',3,5,'benefits',guide(15,'3 benefits @ 5 marks each','(ii)'));c['rows'][0]['contextNote']='Discuss benefits of ANY THREE local amenities for families with young children. Keep each benefit matched to its amenity; preserve all described/name-only choices. '+c['rows'][0]['contextNote']
 judged(1,'b','ii','3-3',3,5,'reasons',stripjoin(guide(15,'3 reasons @ 5 marks each')))
 judged(1,'c','i','3-4',3,5,'factors',guide(16,'3 factors @ 5 marks each','(ii)'))
 full=guide(16,'Built-in wardrobes:',include=True);names=['Built-in wardrobes:','shelving:','modular units:','free-standing units:','bed storage:','clothes organisers/rails','bedside lockers'];add(1,'c','ii','3-4',15,[menu('names','Identify',3,2,[name.rstrip(':') for name in chosen(full,names)],'Choose ANY THREE different items of storage furniture.'),criterion('descriptions','Description',3,[0,3],'Describe EACH of the SAME THREE selected items. Complete paired source guidance: '+full+' Clothes organisers/rails and bedside lockers are accepted names only; no description models are invented.')],'Three names2 + three matching descriptions3')
 full=guide(17,'Function:','(ii)',True);heads=['Function:','Comfort:','Aesthetic appeal:'];add(2,'a','i','3-8',18,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,3],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Function2×3 + comfort2×3 + aesthetic appeal2×3',questionFigureKey='home-economics-2018-ol-sc-q2-uniforms',questionFigureIncludesPrompt=False)
 full=stripjoin(guide(17,'2 methods: 1 @ 4 marks, 1 @ 3 marks'));r=menu('methods','methods',2,4,semis(full),'Choose ANY TWO different methods from the complete original pool. The first credited method earns4 and the second3; no fixed method receives the higher award.');r['group']['perOptionSteps']=[4,3];r['marks']=7;add(2,'a','ii','3-8',7,[r],'Two methods4+3')
 judged(2,'b','i','3-7',3,3,'fabric finishes',guide(18,'3 reasons @ 3 marks each','(ii)'))
 full=stripjoin(guide(18,'Waterproofing:','2.(c)',True));heads=['Waterproofing:','anti-static:','stain resistant:','crease resistant:','mercerising:','flame retardant:'];variants=[]
 for i,(head,model) in enumerate(zip(heads,named(full,heads)),1):variants.append(dict(id=f'finish-{i}',label=head.rstrip(':'),rows=[point('name',head.rstrip(':'),3),criterion('description','Description',1,[0,3],'Describe this SAME selected finish. '+model)]))
 variants.append(dict(id='another-finish',label='Another valid fabric finish',rows=[criterion('name','Name',1,[0,3],'Choose ONE finish consistently; all six original models retained.'),criterion('description','Description',1,[0,3],'Describe the SAME selected finish; no additional original model is printed.')]))
 add(2,'b','ii','3-7',6,deepcopy(variants[0]['rows']),'Name3 + description3',answerVariants=variants)
 judged(2,'c','i','3-8',3,3,'factors',select(guide(18,'2.(c)'),'3 factors @ 3 marks each','(ii)'))
 judged(2,'c','ii','3-8',2,3,'challenges',guide(18,'2 challenges @ 3 marks each'))
 judged(3,'a','i','3-9',2,3,'unemployment',guide(19,'2 points @ 3 marks each','(ii)'))
 full=guide(19,'Young adult:','(iii)',True);heads=['Young adult:','Family:','Society:'];add(3,'a','ii','3-9',24,[criterion(f'heading-{i}',head.rstrip(':'),2,[0,4],model) for i,(head,model) in enumerate(zip(heads,named(full,heads)),1)],'Three required headings×two effects4')
 judged(3,'a','iii','3-10',2,4,'qualification',select(select(s[19],'(iii)','(iv)'),'2 points @ 4 marks each'))
 full=stripjoin(guide(19,'Solas:',include=True));names=['Solas','Springboard','Momentum - Action Plan for Jobs','Jobs Plus','VTOS','Back to Education Programme','Skillsnet','Safe Pass'];add(3,'a','iv','3-9',12,[menu('name','Name',1,4,chosen(full,names),'Choose ONE programme/course consistently; historical2018 original names retained.'),criterion('details','Details',2,[0,4],'Give TWO details of the SAME named programme. Complete original models: '+full+' VTOS, Back to Education Programme, Skillsnet and Safe Pass are accepted names only; no extra details are invented.')],'Name4 + two matching details4')
 judged(3,'b','i','3-11',3,5,'reasons',guide(20,'3 reasons @ 5 marks each','(ii)'))
 full=stripjoin(select(select(s[20],'3.(b)','3.(c)'),'3 points @ 5 marks each'));c=judged(3,'b','ii','3-11',3,5,'dual-earners',full);c['rows'][0]['contextNote']='Address advantages AND disadvantages across three points. No separate category quota or internal split is printed. '+c['rows'][0]['contextNote']
 judged(3,'c','i','3-11',3,5,'urban areas',select(select(s[20],'3.(c)','(ii)'),'3 points @ 5 marks each'))
 judged(3,'c','ii','3-11',3,5,'migration',select(select(s[20],'3.(c)').split('(ii)',1)[1],'3 points @ 5 marks each'))
 assert len(cards)==21 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=21,marks=275,selectionDecisions='Full water-system and three-uniform inputs; every required water-treatment/appearance/unemployment heading; complete paired storage-furniture and fabric-finish pools; crest methods4+3 without fixed-method assignment; all programme/course alternatives with source-only gaps; dual-earner shared tariff.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
