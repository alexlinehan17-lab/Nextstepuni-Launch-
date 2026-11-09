#!/usr/bin/env python3
"""2010 Ordinary elective tasks and the scheme's explicit flexible quotas."""
from he_review_2010_ol_main import *

def build():
 d=documents();p={n:text(d['paper'],n+8) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(14,21)};cards=[]
 def part(n,letter):
  v=select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None)
  return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);prompt=select(v,f'({roman})') if roman else v
  if roman:prompt=re.split(r'\((?:i|ii|iii)\)',prompt,1)[0]
  prompt=re.sub(r'\s*\(\d+\)\s*$','',prompt).replace('\uf0b7','•').strip()
  stem=v.split('(i)',1)[0].strip() if roman and '(i)' in v else ''
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt,stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None):return select(s[page],token,end)
 def judged(n,letter,roman,topic,count,per,guidance,label='Published answer points',**extra):
  return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Use distinct points at the source’s printed value; no smaller steps are published. Complete source guidance: '+guidance)],f'{count} points × {per}',**extra)
 judged(1,'a','i','3-3',4,5,guide(14,'4 points @ 5 marks each','(ii)'),'suitability',questionFigureKey='home-economics-2010-ol-sc-q1-plan',questionFigureIncludesPrompt=False)
 judged(1,'a','ii','3-3',3,5,guide(14,'3 factors @ 5 marks each','(iii)'),'factors')
 roles=re.sub(r'\s+and$','',guide(14,'3 points @ 5 marks each'));add(1,'a','iii','3-3',15,[point(f'role-{i}',v,5) for i,v in enumerate(named(roles,['Architect:','Surveyor:','Solicitor:']),1)],'3 required roles × 5')
 efficiencies=guide(15,'3 areas @ 3 marks each + 3 methods @ 3 marks each','(ii)');rows=[];groups=[]
 for i in range(1,4):
  rows += [criterion(f'area-{i}','area',1,[0,3],'Name a different area in each pair. Complete source examples and methods: '+efficiencies),criterion(f'method-{i}','method',1,[0,3],'A method appropriate to this SAME area. Complete guidance is in the paired area row.')]
  groups.append(dict(sourceCardId=f'he-2010-ol-sc-q1bi-pair-{i}',label=f'Area / method {i}',marks=6,rowIds=[f'area-{i}',f'method-{i}']))
 add(1,'b','i','3-6',18,rows,'3 pairs × (area 3 + method 3)',taskGroups=groups)
 judged(1,'b','ii','3-6',3,4,guide(15,'3 points @ 4 marks each','or 1.(c)'),'advantages / the disadvantages')
 judged(1,'c','i','3-4',2,6,guide(15,'2 points @ 6 marks each','(ii)'),'pattern')
 flooring=guide(15,'2 types @ 3 marks each','State two properties');properties=guide(15,'4 properties @ 3 marks each');rows=[];groups=[]
 for i in range(1,3):
  rows += [criterion(f'type-{i}','type',1,[0,3],'Choose a different suitable flooring for each pair. Full source options: '+flooring),criterion(f'properties-{i}','properties',2,[0,3],'Two properties for this SAME flooring. Full printed guidance: '+properties)]
  groups.append(dict(sourceCardId=f'he-2010-ol-sc-q1cii-flooring-{i}',label=f'Flooring {i}',marks=9,rowIds=[f'type-{i}',f'properties-{i}']))
 add(1,'c','ii','3-4',18,rows,'2 profiles × (type 3 + 2 properties × 3)',taskGroups=groups)
 fashion=guide(16,'6 points @ 3 marks each','(ii)')
 c=judged(2,'a','i','3-8',6,3,fashion,'fashion trends',questionFigureKey='home-economics-2010-ol-sc-q2-fashion',questionFigureIncludesPrompt=False)
 c['rows'][0]['contextNote']='Address all three printed headings and both outfits. The source gives six points at three marks, without a split between headings. Its fashion-influences answer bullet is blank; no missing model has been invented. Complete printed guidance: '+fashion
 design=re.sub(r'\s+And$','',guide(16,'description @ 4 marks [2 points @ 2 marks each)'));methods=select(design,'method:','appliqué:');description=select(design,'appliqué:',include=True)
 add(2,'a','ii','3-8',7,[menu('method','method',1,3,[x.strip() for x in examples(methods).split(',')]),criterion('description','description',2,[0,2],'Two details of this SAME chosen method. The source gives one model: '+description)],'Method 3 + description 2 × 2')
 judged(2,'b','i','3-8',3,3,guide(17,'3 points @ 3 marks each','(ii)'),'cottage industries')
 judged(2,'b','ii','3-8',2,3,guide(17,'2 reasons @ 3 marks each','or 2.(c)'),'reasons')
 fabric=guide(17,'(1 reference to each + 1 other point)');production=select(fabric,' fibre production',' properties');properties=select(fabric,' properties',' fabric uses');uses=select(fabric,' fabric uses')
 rows=[criterion('name','name',1,[0,3],'The original paper names three profile headings. The scheme additionally requires the fabric name, then production, properties and uses plus one further point. Its worked example is Nylon; no extra paper question has been invented.'),criterion('production','fibre production',1,[0,3],production),criterion('properties','properties',1,[0,3],properties),criterion('uses','fabric uses',1,[0,3],uses),criterion('other','1 other point',1,[0,3],'One further distinct point about this SAME manufactured fabric. Complete printed guidance: '+fabric)]
 add(2,'c',None,'3-7',15,rows,'5 points × 3; one reference to each + one other')
 unemployment=guide(18,'(1 reference to each + 1 other point)','(ii)');family=select(unemployment,' the family unit',' the individual');individual=select(unemployment,' the individual',' society.');society=select(unemployment,' society.')
 add(3,'a','i','3-9',20,[criterion('family','the family unit',1,[0,5],family),criterion('individual','the individual',1,[0,5],individual),criterion('society','society',1,[0,5],society),criterion('other','1 other point',1,[0,5],'One further distinct effect from any of the three required headings. Complete source guidance: '+unemployment)],'4 effects × 5; one reference to each + one other')
 volunteering=guide(18,'( 2 references to each)','(iii)');person=select(volunteering,'unemployed person:','community:');community=select(volunteering,'community:')
 add(3,'a','ii','3-9',16,[criterion('person','unemployed person',2,[0,4],person),criterion('community','community',2,[0,4],community)],'2 required headings × 2 benefits × 4')
 judged(3,'a','iii','3-9',2,7,re.sub(r'\s+and$','',guide(18,'2 types @ 7 marks each')),'types of support')
 care=guide(19,'(1 reference to each + 3 others)','(ii)');supervision=select(care,' adequate levels of supervision',' adequate resources');resources=select(care,' adequate resources',' high levels of hygiene and safety.');hygiene=select(care,' high levels of hygiene and safety.')
 add(3,'b','i','3-10',18,[criterion('supervision','adequate levels of supervision',1,[0,3],supervision),criterion('resources','sufficient resources',1,[0,3],resources),criterion('hygiene','high levels of hygiene and safety',1,[0,3],hygiene),criterion('other','3 others',3,[0,3],'Three further distinct reasons under any of the required headings. Complete source guidance: '+care)],'6 reasons × 3; one reference to each + three others')
 judged(3,'b','ii','3-10',3,4,guide(19,'3 points @ 4 marks each','or 3.(c)'),'development')
 home=guide(19,'(1 references to each of any 3 of the listed headings + 2 other points)')+' '+s[20]
 c=judged(3,'c',None,'3-11',5,6,home,'home care duties')
 c['rows'][0]['contextNote']='Choose THREE of the four printed headings. Give at least one point under each chosen heading, then two further distinct points within those chosen headings. Five points at six marks; do not count the same point twice. Full original guidance, including the next scheme page: '+home
 assert len(cards)==18 and sum(c['totalMarks'] for c in cards)==275
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=18,marks=275,selectionDecisions='Required area/method and flooring/properties pairs stay whole. All flexible heading quotas remain explicit. Fashion-influences source blank and extra scheme fabric-name requirement are recorded in visible row notes. C3(c) is one choose-three task with all four headings and its continued original guidance.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
