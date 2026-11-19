#!/usr/bin/env python3
"""2017 Higher electives: complete linked profiles and original descending names tariff."""
from copy import deepcopy
from he_review_2017_hl_main import *
def build():
 d=documents();p={n:re.sub(r'(\d)\.\s+\(([abc])\)',r'\1.(\2)',text(d['paper'],n+8)) for n in [1,2,3]};s={n:text(d['scheme'],n) for n in range(18,26)};cards=[]
 def stripjoin(v):return re.sub(r'\s+(?:and|or)\s*$','',v).strip()
 def part(n,letter):return stripjoin(select(p[n],f'{n}.({letter})',f'{n}.({chr(ord(letter)+1)})' if f'{n}.({chr(ord(letter)+1)})' in p[n] else None))
 def prompt(n,letter,roman):
  v=part(n,letter)
  if roman:v=select(v,f'({roman})');v=re.split(r'\((?:i|ii|iii|iv)\)',v,1)[0]
  return re.sub(r'\s*\(\d+\)\s*$','',v).strip()
 def add(n,letter,roman,topic,marks,rows,notation,**extra):
  v=part(n,letter);stem=v.split('(i)',1)[0].strip() if roman else ''
  if n==1 and letter=='a':stem=stem.split('Murphy Family Bungalow',1)[0].strip()
  if n==2 and letter=='a':stem=stem.split('(www.marieclaire.com)',1)[0].strip()
  if n==3 and letter=='a':stem=stem.split('2011 2012',1)[0].strip()
  c=card(f'sc-q{n}{letter}{roman or ""}','C',f'E{n} Q{n}({letter})'+(f'({roman})' if roman else ''),topic,prompt(n,letter,roman),stem,marks,rows,n+8,notation,**extra);cards.append(c);return c
 def guide(page,token,end=None,include=False):return select(s[page],token,end,include)
 def judged(n,letter,roman,topic,count,per,label,guidance,**extra):return add(n,letter,roman,topic,count*per,[criterion('points',label,count,[0,per],'Complete original source guidance: '+guidance)],f'{count} points × {per}',**extra)
 c=judged(1,'a','i','3-4',4,5,'suitability',guide(18,'4 points @ 5 marks each','(ii)'),questionFigureKey='home-economics-2017-hl-sc-q1-bungalow',questionFigureIncludesPrompt=False);c['rows'][0]['contextNote']='Evaluate present/future needs and suggest modifications if required, within FOUR points. The source gives no separate evaluation/modification allocation. The complete original plan and family ages remain available. '+c['rows'][0]['contextNote']
 c=judged(1,'a','ii','3-6',3,5,'energy inefficiencies',guide(18,'(3 energy inefficiencies and related strategies)'));c['rows'][0]['contextNote']='Give THREE energy inefficiencies and the related improvement strategy for EACH. Each linked account has five marks; do not detach the strategy from its inefficiency. '+c['rows'][0]['contextNote']
 judged(1,'a','iii','3-6',3,5,'BER certificate',stripjoin(guide(19,'3 points @ 5 marks each','1.(b)')))
 c=judged(1,'b','i','3-3',3,6,'social housing provision',guide(19,'3 points @ 6 marks each','(ii)'));c['rows'][0]['contextNote']='Historical 2017 provision and conditions as printed. '+c['rows'][0]['contextNote']
 heads=['Schools:','Transport:','Refuse collection:'];add(1,'b','ii','3-3',12,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,4],stripjoin(body)) for i,(head,body) in enumerate(zip(heads,named(guide(19,'Schools:',include=True),heads)),1)],'Schools4 + transport4 + refuse4')
 judged(1,'c','i','3-5',3,4,'ventilation',guide(20,'3 points @ 4 marks each','(ii)'))
 full=guide(20,'Natural methods:',include=True);natural=semis(select(full,'Natural methods:','Underlying principle:'));principle=select(full,'Underlying principle:','Artificial methods');heads=['Extractor fan:','Cooker hood:'];variants=[]
 for i,(name,detail) in enumerate(zip(heads,named(select(full,'Artificial methods'),heads)),1):
  rows=[menu('natural-name','Natural methods',1,3,natural,'Choose ONE natural method suitable for the kitchen/living area, and explain its matching principle.'),criterion('natural-principle','Principle',2,[0,3],'Two principle points matching the SAME natural method. '+principle),point('artificial-name',name.rstrip(':'),3),criterion('artificial-principle','Principle',2,[0,3],'Two principle points matching this SAME artificial method. '+detail)]
  variants.append(dict(id=f'artificial-{i}',label=name.rstrip(':'),rows=rows))
 variants.append(dict(id='other-artificial',label='Another valid artificial method',rows=[deepcopy(variants[0]['rows'][0]),deepcopy(variants[0]['rows'][1]),criterion('artificial-name','Artificial methods',1,[0,3],'Name ONE artificial method suitable for the kitchen/living area.'),criterion('artificial-principle','Principle',2,[0,3],'Two principle points matching the SAME selected method. The source gives worked models only for extractor fan and cooker hood; no additional model is invented.')]))
 groups=[dict(sourceCardId=f'he-2017-hl-sc-q1cii-{kind}',label=kind.title()+' ventilation',marks=9,rowIds=[kind+'-name',kind+'-principle']) for kind in ['natural','artificial']]
 add(1,'c','ii','3-5',18,deepcopy(variants[0]['rows']),'Natural(name3 + principle2×3) + artificial(name3 + principle2×3)',answerVariants=variants,taskGroups=groups)
 heads=['Comfort:','Aesthetic appeal:','Current fashion trend:'];add(2,'a','i','3-8',15,[criterion(f'heading-{i}',head.rstrip(':'),1,[0,5],body) for i,(head,body) in enumerate(zip(heads,named(guide(21,'Comfort:','(ii)',True),heads)),1)],'Comfort5 + aesthetic5 + current fashion5',questionFigureKey='home-economics-2017-hl-sc-q2-outfit',questionFigureIncludesPrompt=False)
 full=guide(21,'(1 reference to trendsetters, 1 reference to media)');add(2,'a','ii','3-8',10,[criterion('trendsetters','trendsetters',1,[0,5],'One point specifically about trendsetters. Complete shared source: '+full),criterion('media','media',1,[0,5],'One point specifically about media. Complete shared source: '+full)],'Trendsetters5 + media5')
 full=guide(22,'Fibre production','2.(c)');production=select(full.split('Blending:',1)[0],'Wool:',include=True);blending=select(full,'Blending:','Fabric properties:',True);properties=select(full,'Fabric properties:','Uses:');uses=stripjoin(select(full,'Uses:'));heads=['Wool:','Nylon:','Polyester:','Cotton:'];prod=named(production,heads);props=named(properties,heads);variants=[]
 for i,(label,indices) in enumerate([('wool and nylon',[0,1]),('polyester cotton',[2,3])],1):
  rows=[criterion('production','fibre production',3,[0,3],'Three points about production of the SAME chosen blended fabric, using its constituent fibres and blending. '+' '.join(prod[j] for j in indices)+' '+blending),criterion('properties','fabric properties',3,[0,1],'Three properties of the SAME blended fabric, reflecting BOTH constituents. '+' '.join(props[j] for j in indices)),criterion('uses','uses',3,[0,1],'Three uses appropriate to the SAME selected blend. Complete original shared guidance: '+uses)]
  variants.append(dict(id=f'blend-{i}',label=label,rows=rows))
 variants.append(dict(id='another-blend',label='Another valid blended fabric',rows=[criterion('production','fibre production',3,[0,3],'Use ONE blended fabric consistently. The source models wool/nylon and polyester/cotton only; no production model is invented for another blend. Shared blending guidance: '+blending),criterion('properties','fabric properties',3,[0,1],'Three properties of the SAME blend reflecting its constituents. No additional model is printed.'),criterion('uses','uses',3,[0,1],'Three uses appropriate to the SAME blend. Complete shared source: '+uses)]))
 add(2,'b',None,'3-7',15,deepcopy(variants[0]['rows']),'Production3×3 + properties3×1 + uses3×1; no name tariff',answerVariants=variants)
 judged(2,'c','i','3-8',3,3,'promotion',select(guide(22,'2.(c)'),'3 points @ 3 marks each','(ii)'))
 full=guide(22,'Name: 2 marks; Details: 2 points @ 2 marks each');add(2,'c','ii','3-8',6,[menu('name','Name',1,2,semis(full),'Choose ONE career consistently; every original career name is available.'),criterion('details','Details',2,[0,2],'Two details about the SAME chosen career. The original scheme supplies names only, with no worked career details; none are invented. Complete original pool: '+full)],'Name2 + details2×2')
 c=judged(3,'a','i','3-9',4,5,'Comment',guide(23,'4 points @ 5 marks each','(ii)'),questionFigureKey='home-economics-2017-hl-sc-q3-unemployment',questionFigureIncludesPrompt=False);c['rows'][0]['contextNote']='Comment on the source table AND analyse the change within FOUR points. The source gives no fixed comment/analysis quota. Complete six-year table retained. '+c['rows'][0]['contextNote']
 full=guide(23,'(1 reference to individuals, families and society + 2 others)')+' '+guide(24,'Effects on society','(iii)',True);heads=['Effects on individuals','Effects on families','Effects on society'];add(3,'a','ii','3-9',20,[criterion(f'heading-{i}',head,1,[0,4],body) for i,(head,body) in enumerate(zip(heads,named(full,heads)),1)]+[criterion('other','2 others',2,[0,4],'Two ADDITIONAL effects from any of the three required headings. '+full)],'Individuals4 + families4 + society4 + two others4')
 full=stripjoin(guide(24,'Name: 2 marks; Details: 2 points @ 4 marks each','3.(b)'));add(3,'a','iii','3-9',10,[menu('name','Name',1,2,semis(full),'Choose ONE scheme to reduce low-income family expenditure. Original historical 2017 names retained.'),criterion('details','Details',2,[0,4],'Two details of the SAME selected scheme. The original scheme lists names and brief descriptors only, not complete two-point worked accounts. No additional model is invented. Complete original pool: '+full)],'Name2 + details2×4')
 judged(3,'b','i','3-11',3,5,'participation of women',guide(24,'3 factors @ 5 marks each','(ii)'))
 full=stripjoin(guide(24,'Details: (3 points @ 2 marks each) X 2'));names=['Crèche','Childminder in own or child’s home','Au pair','Naíonra','Playschools / Playgroups','Montessori'];names=chosen(full,names);r=menu('names','Name',2,2,names,'Choose TWO different childcare options. The first credited name earns2, the second1; no fixed option is tied to either award. Keep three details matched to EACH named option.');r['group']['perOptionSteps']=[2,1];r['marks']=3
 rows=[r]+[criterion(f'details-{i}','Details',3,[0,2],f'Three details of the SAME option {i} selected above. The source gives accounts for Crèche, Childminder and Au pair; Naíonra, Playschools/Playgroups and Montessori have names only. No additional models are invented. Complete original paired guidance: '+full) for i in [1,2]]
 add(3,'b','ii','3-11',15,rows,'Two names2+1 + three details2 for EACH selected option')
 judged(3,'c','i','3-11',4,5,'impact',guide(25,'4 points @ 5 marks each','(ii)'))
 judged(3,'c','ii','3-11',2,5,'work ethic',guide(25,'2 points @ 5 marks each'))
 assert len(cards)==19 and sum(c['totalMarks'] for c in cards)==275,(len(cards),sum(c['totalMarks'] for c in cards))
 return cards
if __name__=='__main__':
 cards=build()
 if '--write' in sys.argv:write_section('C',cards,dict(tasks=19,marks=275,selectionDecisions='Complete original bungalow/outfit/unemployment inputs, required linked natural/artificial ventilation and blended-fabric profiles, all source-only career/benefit gaps, full society continuation, and descending childcare name2/1 plus matching detail6/6 retained.'))
 else:print(json.dumps(cards,ensure_ascii=False,indent=2))
