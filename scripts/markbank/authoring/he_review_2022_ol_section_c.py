#!/usr/bin/env python3
"""Review all 28 Ordinary Section C tasks and two complete source illustrations."""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2022_ol import ROOT, REVIEW, PAPER_BC, documents, page_text, criterion, between, named_sections

SELECTORS={5:['or','one','or','either','or','either','or','three','three','three','three','or','following','four'],6:['either','or','one','one','each','following','two','or','three'],7:['either','or','each','following','four','one','three','or','any','three'],8:['either','or','one','one','one','one','three','or','following','three']}
FIGURES={
 'home-economics-2022-ol-sc-q1-room':dict(page=5,bounds=[115,210,493,345],sha256='40f65cef79179c3b439f18971011e3ae4e67af491c70981b6c946bf3951574b0',alt='An overhead view of an open-plan kitchen, dining and living room. Left: corner sofa, armchair, coffee table, television and window. Right: dining table with four chairs, kitchen units, hob, extractor, sink and worktops. Pale wood-effect flooring continues throughout.'),
 'home-economics-2022-ol-sc-q2-outfits':dict(page=6,bounds=[199,129,382,302],sha256='2f033a5e8d4600fcc94c9f2e5c47947f643a232873a838678f291de84e9f25e5',alt='Two athleisure outfits. Left: navy open zip jacket, white T-shirt, navy drawstring joggers and white trainers. Right: open taupe hooded jacket, white T-shirt, cropped olive trousers with a drawstring waist, white socks and light-coloured trainers. Both full outfits are visible.'),
}
CLARIFICATIONS={
 'electrical-protection':dict(source='https://new.abb.com/low-voltage/products/system-pro-m/residual-current-devices',note='An ordinary MCB provides overcurrent protection; an RCBO combines overcurrent and residual-current protection. MCBs do not universally contain RCDs.'),
 'poverty':dict(source='https://www.cso.ie/en/media/csoie/releasespublications/documents/ep/surveyonincomeandlivingconditions/2022/factsheets/0127101_At_Risk_of_Poverty_Explained_Leaflet.pdf',note='CSO’s at-risk-of-poverty threshold is 60% of median equivalised disposable income, not the scheme’s 50% of average household income. Preserve the general relative-poverty definition and distinguish the erroneous threshold.'),
}


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in range(5,9)}
 for n,text in p.items():assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b',text,re.I)==SELECTORS[n],n
 questions,stems={},{}
 for q in range(1,5):
  for part,next_part in [('a','b'),('b','c'),('c',None)]:
   block=p[q+4].split(f'{q}.({part})',1)[1]
   if next_part:block=block.split(f'{q}.({next_part})',1)[0]
   matches=list(re.finditer(r'\((i{1,3})\)\s+(.*?)\s*\((\d+) marks\)',block));expected=['i','ii','iii'] if part=='a' and q!=2 else ['i','ii'];assert [m[1] for m in matches]==expected,(q,part)
   stem=block[:matches[0].start()].strip()
   for m in matches:questions[(q,part+m[1])]=(m[2].strip().replace(' \uf0b7 ','\n• '),int(m[3]));stems[(q,part+m[1])]=stem
 assert len(questions)==27
 s={n:page_text(d['scheme'],n) for n in range(17,26)};fixes={};added=[]
 def put(q,part,rows,notation,variants=None,**extra):
  question,marks=questions[(q,part)];v=dict(questionText=question,stem=stems[(q,part)],totalMarks=marks,rows=rows,tariffModel=dict(kind='fixed',notation=notation),sourceMaterial=dict(kind='source-question',label='OFFICIAL QUESTION',title='Source and question',pages=[q+4],attribution='SEC Home Economics 2022 Ordinary Level examination paper — © State Examinations Commission.',presentationNote='Open the original examination page to review this task in context.'),notes='Full question and scheme independently reviewed, including all required headings and grades. See he_review_2022_ol_section_c.py.')
  if variants:v['answerVariants']=variants
  v.update(extra);fixes[f'he-2022-ol-sc-q{q}{part}']=dict(reason='2022 Ordinary C source review: full context, all guidance, actual mark boundaries and partial credit.',set=v)
 def body(text,grade):
  result=text.split(f'(graded {grade})',1)[1].strip();assert result.endswith('etc.'),result;return result
 def points(q,part,label,count,grade,text,**extra):
  assert text.endswith('etc.'),(q,part,text);steps=sorted(map(int,grade.split(':')));put(q,part,[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete published guidance: '+text)],f'{count} points × {steps[-1]} ({grade})',**extra)
 points(1,'ai','suitability',4,'5:3:0',body(between(s[17],'(i)','(ii)'),'5:3:0'),figureKey='',questionFigureKey='home-economics-2022-ol-sc-q1-room',questionFigureIncludesPrompt=False)
 points(1,'aii','lighting system',3,'5:3:0',body(between(s[17],'(ii)','(iii)'),'5:3:0'),stem='',figureKey='')
 points(1,'aiii','types',3,'5:3:0',body(s[17].split('(iii)',1)[1],'5:3:0'),stem='',figureKey='')
 b=between(s[18],'1. (b)','1. (c)').removesuffix('or').strip();c=s[18].split('1. (c)',1)[1]
 points(1,'bi','choice of housing',3,'5:3:0',body(between(b,'(i)','(ii)'),'5:3:0'))
 points(1,'bii','reduce their home energy bills',3,'5:3:0',body(b.split('(ii)',1)[1],'5:3:0'))
 mcb,earth=named_sections(c.split('(ii)',1)[0],['Miniature circuit breaker:','Earth wire:'])
 put(1,'ci',[criterion('mcb','miniature circuit breakers',1,[0,3,5],'Required device, graded 5:3:0. Source correction: an ordinary MCB protects against overcurrent; an RCBO combines overcurrent and residual-current protection. Ordinary MCBs do not universally contain RCDs. Complete published wording: '+mcb),criterion('earth','earth wire',1,[0,3,5],'Required device, graded 5:3:0. Complete published guidance: '+earth)],'2 required devices × 5 (5:3:0)')
 points(1,'cii','safe use of electricity',4,'5:3:0',body(c.split('(ii)',1)[1],'5:3:0'))
 labels=['Comfort:','Function:','Design features:'];values=named_sections(s[19].split('(ii)',1)[0],labels)
 put(2,'ai',[criterion(f'heading-{i}',label.rstrip(':'),1,[0,3,6],'One point under this required heading, graded 6:3:0. Complete guidance: '+text) for i,(label,text) in enumerate(zip(labels,values),1)],'3 required headings × 6 (6:3:0)',figureKey='',questionFigureKey='home-economics-2022-ol-sc-q2-outfits',questionFigureIncludesPrompt=False)
 accessories=s[19].split('1 reason @ 4 marks (graded 4:2:0)',1)[1].strip();assert accessories.endswith('etc.')
 put(2,'aii',[criterion('name','Name',1,[0,2,3],'Name one accessory for the pictured outfits, graded 3:2:0. Complete paired examples: '+accessories),criterion('reason','reason',1,[0,2,4],'Give a reason for the accessory you chose, graded 4:2:0. Use the complete paired guidance above.')],'Name 3 (3:2:0); reason 4 (4:2:0)',figureKey='',questionFigureKey='home-economics-2022-ol-sc-q2-outfits',questionFigureIncludesPrompt=False)
 fabric=between(s[20],'2. (b)','(ii)');construction=between(fabric,'3 points @ 2 marks (graded 2:1:0)','• properties.');properties=fabric.split('2nd property @ 1 mark (graded 1:0)',1)[1].strip();names=['Viscose','Acetate','Polyester','Nylon','Acrylic'];details=named_sections(properties,[n+':' for n in names]);variants=[]
 for name,text in list(zip(names,details))+[('Another man-made fabric','The paper leaves this choice open; no additional worked property list is printed.')]:
  rows=[criterion('construction','how the fabric is constructed',3,[0,1,2],'Three construction points for the fabric chosen, each graded 2:1:0. Naming the fabric carries no separate marks. Complete example and accepted methods: '+construction),criterion('first','1st property',1,[0,2],'First property of the chosen fabric, graded 2:0. Complete published guidance: '+text),criterion('second','2nd property',1,[0,1],'Second distinct property of the same fabric, graded 1:0. Use the guidance above; do not count a property twice.')]
  variants.append(dict(id=name.lower().replace(' ','-'),label=name,rows=rows))
 put(2,'bi',deepcopy(variants[0]['rows']),'Construction 3 × 2 (2:1:0); properties 2 (2:0) + 1 (1:0)',variants)
 manmade=between(s[20],'2. (b)','2. (c)').removesuffix('or').strip();fashion=s[20].split('2. (c)',1)[1]
 put(2,'bii',[criterion('advantages','advantages',2,[0,2,3],'Two advantages, each graded 3:2:0. Properties vary with fibre, construction and finish: select examples that actually apply, rather than treating the list as universal. Complete published examples: '+body(manmade.split('(ii)',1)[1],'3:2:0'))],'2 advantages × 3 (3:2:0)')
 points(2,'ci','factors',3,'3:2:0',body(between(fashion,'(i)','(ii)'),'3:2:0'))
 points(2,'cii','social media',2,'3:2:0',body(fashion.split('(ii)',1)[1],'3:2:0'))
 poverty=between(s[21],'(i)','(ii)');definition=body(poverty.split('Explain each',1)[0],'4:2:0');relative,absolute=named_sections(poverty,['Relative poverty:','Absolute poverty:'])
 put(3,'ai',[criterion('definition','poverty',1,[0,2,4],'Define poverty, graded 4:2:0. Complete published guidance: '+definition)],'Definition 4 (4:2:0)',totalMarks=4,questionRef='2022 OL Section C E3 Q3(a)(i) — definition',questionText='Define ‘poverty’.')
 old=next(c for c in json.loads((ROOT/'scripts/markbank/authored/home-economics.json').read_text()) if c['id']=='he-2022-ol-sc-q3ai');terms=deepcopy(old);terms.update(fixes[old['id']]['set']);terms.update(id='he-2022-ol-sc-q3ai-terms',conceptId='relative-and-absolute-poverty',questionText='Explain each of the following:\n• relative poverty\n• absolute poverty.',questionRef='2022 OL Section C E3 Q3(a)(i) — terms',totalMarks=12,tariffModel=dict(kind='fixed',notation='2 terms × 2 points × 3 (3:2:0)'),rows=[criterion('relative','relative poverty',2,[0,2,3],'Two points, each graded 3:2:0. Source correction: CSO’s at-risk-of-poverty threshold is 60% of median equivalised disposable income, not 50% of average household income. Complete published wording: '+relative),criterion('absolute','absolute poverty',2,[0,2,3],'Two points, each graded 3:2:0. Complete published guidance: '+absolute)]);added.append(terms)
 points(3,'aii','reasons',4,'5:3:0',body(between(s[21],'(ii)','(iii)'),'5:3:0'))
 voluntary=s[21].split('2 details @ 5 marks (graded 5:3:0)',1)[1].strip();other='Lions Club; '+voluntary.split('Lions Club;',1)[1];voluntary=voluntary.split('Lions Club;',1)[0].strip();names=['St. Vincent de Paul','Simon Community','Focus Ireland'];details=named_sections(voluntary,[n+':' for n in names]);variants=[]
 for name,text in list(zip(names,details))+[('Another voluntary organisation','Other published names: '+other+' The scheme prints no model details for these additional examples.')]:
  variants.append(dict(id=re.sub(r'[^a-z]+','-',name.lower()).strip('-'),label=name,rows=[criterion('name','Name',1,[0,2,4],'Name one relevant organisation, graded 4:2:0. '+name),criterion('details','details',2,[0,3,5],'Two details about the same organisation, each graded 5:3:0. Historical 2022 guidance: '+text)]))
 put(3,'aiii',deepcopy(variants[0]['rows']),'Name 4 (4:2:0); details 2 × 5 (5:3:0)',variants)
 rural=between(s[22],'3. (b)','3. (c)').removesuffix('or').strip();child=s[22].split('3. (c)',1)[1]
 points(3,'bi','reasons',3,'5:3:0',body(between(rural,'(i)','(ii)'),'5:3:0'))
 put(3,'bii',[criterion('impact','family life',3,[0,3,5],'Three points explaining the impact, each graded 5:3:0. The rural/urban headings organise examples; the scheme assigns no per-heading quota. Complete guidance: '+body(rural.split('(ii)',1)[1],'5:3:0'))],'3 points × 5 (5:3:0)')
 points(3,'ci','factors',3,'5:3:0',body(between(child,'(i)','(ii)'),'5:3:0'))
 points(3,'cii','development',3,'5:3:0',body(child.split('(ii)',1)[1],'5:3:0'))
 # The printed task itself contains (i)/(ii) headings; split its scheme at the
 # later main-task '(ii) Outline:', not at the first internal '(ii)'.
 nutrition=between(s[23],'Nutritional value:','(ii) Outline:');nutritive,dietetic=named_sections('Nutritional value: '+nutrition,['Nutritional value:','Dietetic value:'])
 put(4,'ai',[criterion('nutritive','nutritive value',1,[0,2,4],'One required nutritive point, graded 4:2:0. Complete guidance: '+nutritive),criterion('dietetic','dietetic value',1,[0,2,4],'One required dietetic point, graded 4:2:0. Complete guidance: '+dietetic),criterion('other','plus 3 others',3,[0,2,4],'Three further distinct points on either heading, each graded 4:2:0. Do not count a point twice.')],'5 × 4 (4:2:0): nutritive 1, dietetic 1, other 3')
 fish=between(s[23],'(ii) Outline:','(iii)');buying=body(fish.split('• the effects of cooking on fish.',1)[0],'3:2:0');cooking=body(fish.split('• the effects of cooking on fish.',1)[1],'3:2:0')
 put(4,'aii',[criterion('buying','buying fresh fish',3,[0,2,3],'Three buying guidelines, each graded 3:2:0. Complete guidance: '+buying),criterion('cooking','effects of cooking',3,[0,2,3],'Three cooking effects, each graded 3:2:0. Complete guidance: '+cooking)],'Buying 3 × 3; cooking 3 × 3 (all 3:2:0)')
 processing=s[23].split('(iii)',1)[1];names=['Freezing','Canning','Smoking'];details=named_sections(processing,[n+':' for n in names]);variants=[]
 for name,text in zip(names,details):
  advantage,disadvantage=re.split(r'Disadvantages?:',text.split('Advantages:',1)[1],maxsplit=1)
  variants.append(dict(id=name.lower(),label=name,rows=[criterion('name','method',1,[0,4],'Name the chosen method, graded 4:0. '+name),criterion('advantage','advantage',1,[0,2,4],'One advantage of the method, graded 4:2:0. Published examples: '+advantage.strip()),criterion('disadvantage','disadvantage',1,[0,2,4],'One disadvantage, graded 4:2:0. These are possible effects of particular products/processes, not universal to every product. Published examples: '+disadvantage.strip())]))
 variants.append(dict(id='another',label='Another valid method',rows=[criterion('name','method',1,[0,4],'Name another valid method, graded 4:0; the paper leaves the choice open.'),criterion('advantage','advantage',1,[0,2,4],'Give one accurate advantage of your method, graded 4:2:0. No further model answer is printed.'),criterion('disadvantage','disadvantage',1,[0,2,4],'Give one accurate disadvantage of that method, graded 4:2:0. No further model answer is printed.')]))
 put(4,'aiii',deepcopy(variants[0]['rows']),'Method 4 (4:0); advantage 4 + disadvantage 4 (4:2:0)',variants)
 retail=between(s[24],'4. (b)','4. (c)').removesuffix('or').strip();home=s[24].split('4. (c)',1)[1]
 points(4,'bi','ways',3,'5:3:0',body(between(retail,'(i)','(ii)'),'5:3:0'))
 points(4,'bii','procedure',5,'3:2:0',body(retail.split('(ii)',1)[1],'3:2:0'))
 labels=['Dual roles:','Stages in life cycle:','Employment patterns:'];details=named_sections(home,labels)
 put(4,'ci',[criterion(f'factor-{i}',name.rstrip(':'),1,[0,3,5],'One point on this required factor, graded 5:3:0. Published guidance: '+detail) for i,(name,detail) in enumerate(zip(labels,details),1)],'3 required factors × 5 (5:3:0)')
 points(4,'cii','technology',3,'5:3:0',body(s[25],'5:3:0'))
 assert len(fixes)==27 and len(added)==1
 return fixes,added


def write():
 fixes,added=build();p=ROOT/'scripts/markbank/card-corrections.json';saved=json.loads(p.read_text());saved['home-economics'].update(fixes);p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n');p=ROOT/'scripts/markbank/authored/home-economics.json';saved=json.loads(p.read_text())
 for c in added:
  i=next((i for i,v in enumerate(saved) if v['id']==c['id']),None)
  if i is None:saved.append(c)
  else:saved[i]=c
 p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n');p=ROOT/'components/MarkBank/figures-home-economics.json';manifest=json.loads(p.read_text());d=documents()
 for key,spec in FIGURES.items():
  target=ROOT/f'public/exam-figures/home-economics/{key}.png';d['bc'][spec['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(spec['bounds'])).save(target);assert hashlib.sha256(target.read_bytes()).hexdigest()==spec['sha256'];manifest[key]=dict(src=f'/exam-figures/home-economics/{key}.png',md5=hashlib.md5(target.read_bytes()).hexdigest(),alt=spec['alt'],attribution=f'SEC Home Economics 2022 Ordinary examination paper, page {spec["page"]} — © State Examinations Commission.',sourceNote=f'Original source image only; bounds {spec["bounds"]}, 2×. Complete image visually inspected. SHA256 {spec["sha256"]}.')
 p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');p=ROOT/REVIEW;review=json.loads(p.read_text());ids=set(fixes)|{c['id'] for c in added};review['tasks']=[t for t in review['tasks'] if t['id'] not in ids]+[dict(id=cid,status='source-reviewed',section='C',marks=f['set']['totalMarks']) for cid,f in fixes.items()]+[dict(id=c['id'],status='source-reviewed',section='C',marks=c['totalMarks']) for c in added]
 assert len(review['tasks'])==60 and sum(t['marks'] for t in review['tasks'])==749
 review['sectionCReview']=dict(tasks=28,marks=385,figures=FIGURES,sourceClarifications=CLARIFICATIONS,selectionDecisions='All offered a/b/c tasks in all three electives and the alternative core are included. Required headings stay together. Fabric, voluntary organisation, accessory and fish processing are single open choices with internal model routes where helpful. Poverty definition is independent of its two required terms.',checked='2026-11-01')
 review['status']='source-complete; all-source-pages-visually-reviewed; browser-QA-pending'
 review['completion']=dict(sourceReviewedTasks=60,offeredPracticeMarks=749,candidateMarks=[200,240],sourcePagesReviewed=81,atlasQuestionGroups=23,note='Full independent paper/scheme sweep. All final 23 paper/scheme anchor pairs and four clean source figures visually checked. Candidate section and elective choices are not additive. Irish editions remain separate; browser QA remains pending.')
 p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');print('2022 Ordinary C: 28 reviewed tasks; all 60 sitting tasks and 749 offered practice marks now accounted for.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
