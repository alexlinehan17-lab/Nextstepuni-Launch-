#!/usr/bin/env python3
"""2026 Ordinary: independently inspected sources, shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='paper-trail-corpus/exampapers/2026/LC098GLP014EV.pdf'
PAPER_BC='paper-trail-corpus/exampapers/2026/LC098GLP039EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2026/LC098GLP000EV.pdf'
HASHES={'paper-trail-corpus/exampapers/2026/LC098GLP014EV.pdf': '78eebd039a3f2d2678243e6d2592f327f09b181ca61e6bb8d0b7659c1bb9f590', 'paper-trail-corpus/exampapers/2026/LC098GLP039EV.pdf': '96a2dc5a978dd38392a28c7814130c0c32a6083c7f307047027960707afedfab', 'paper-trail-corpus/markingschemes/2026/LC098GLP000EV.pdf': '833bb4365215e38cdb3d718989fb3b89be6c89fc6ca98bb88046547dd917f885'}
REVIEW='scripts/markbank/authoring/home-economics/2026-ol-main-review.json'
CLARIFICATIONS={}

def write_scheme_transcript():
 doc=documents()['scheme']
 target=ROOT/'examiner-reports/home-economics/schemes/2026-ol.md'
 target.write_text('# SEC Home Economics 2026 Ordinary marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+ '\n'.join(line.rstrip() for line in page.get_text().splitlines()).strip() for i,page in enumerate(doc))+'\n')


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 return dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))

def page_text(doc,n):return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,790 if doc.name.endswith("LC098GLP000EV.pdf") else 740)))

def card(key,section,ref,topic,concept,prompt,stem,marks,notation,rows,page,**extra):
 c=dict(id='he-2026-ol-'+key,subjectId='home-economics',topicId='home-economics-'+topic,conceptId=concept,level='ordinary',year=2026,section=section,questionRef='2026 OL Section '+section+' '+ref,questionText=prompt,stem=stem,figureKey='',labelKey=[],totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,sourceMaterial=dict(kind='source-question',label='OFFICIAL QUESTION',title='Source and question',pages=[page],attribution='SEC Home Economics 2026 Ordinary Level examination paper — © State Examinations Commission.',presentationNote='Open the original examination page to review this task in context.'),notes='Independently reviewed original paper and scheme. See 2026-ol-main-review.json. Required headings and same-answer name/details remain whole.');c.update(extra);return c

def after(text,token,end=None):
 assert token in text,token;t=text.split(token,1)[1];assert end is None or end in t,end;return (t.split(end,1)[0] if end else t).strip()

def options(text):return [x.strip() for x in re.sub(r'\s*etc\.?\s*$','',text).split(';') if x.strip()]

def any_points(key,label,count,per,text,note=''):
 opts=options(text);assert count<=len(opts)<=25,(key,opts)
 return dict(id=key,kind='anyN',verbatim=label,marks=count*per,openList=True,group=dict(claimMax=count,perOption=per,options=opts),contextNote=note+f'Claim {count} distinct points at {per} mark'+('s' if per!=1 else '')+' each; further valid answers may be credited.')

def save_batch(section,cards,review_data):
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text())
 for c in cards:
  i=next((i for i,v in enumerate(data) if v['id']==c['id']),None)
  if i is None:data.append(c)
  else:data[i]=c
 p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2026,level='ordinary',sitting='main',language='ev',status='partial-carding; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 32 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled answer pages 9–31, back cover 32.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 34 pages: cover 1, guidance/rubrics/annotations 2–5, A 6–8, B 9–14, C 15–22, separate food-studies coursework 23–32, blank 33, back cover 34. Coursework is a separate assessment and is not counted as written-paper tasks.'),expectedTasks=58,expectedSectionTasks=dict(A=15,B=17,C=26),offeredPracticeMarks=749,candidateMarks=[280,320],sourceClarifications=CLARIFICATIONS,tasks=[])
 ids={c['id'] for c in cards};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks'],topicId=c['topicId'],questionRef=c['questionRef']) for c in cards];r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def a_regions(doc,pages,body_bottom=790):
 # The scheme has a stray hidden '14.' at x75 inside A12. Real question
 # numbers are in the x49–57 left margin, verified against every source page.
 result={}
 for page in pages:
  p=doc[page-1];starts=[(int(w[4][:-1]),w[1]-3) for w in p.get_text('words') if re.fullmatch(r'\d+\.',w[4]) and w[0]<65 and w[1]<760]
  for i,(n,top) in enumerate(starts):
   bound=starts[i+1][1] if i+1<len(starts) else body_bottom
   ends=[w[3] for w in p.get_text('words') if w[1]>=top and w[3]<=bound]
   ends += [d['rect'].y1 for d in p.get_drawings() if d['rect'].y0>=top and d['rect'].y1<=bound]
   result[n]=dict(page=page,rect=[0,top,p.rect.width,min(bound,max(ends)+8)])
 assert list(result)==list(range(1,15)),list(result)
 return result

def build():
 d=documents();pr=a_regions(d['a'],range(3,8),740);sr=a_regions(d['scheme'],range(6,9),790);p={n:re.sub(r'^\d+\.\s*','',region_text(d['a'],r)) for n,r in pr.items()};s={n:re.sub(r'\(graded(?=\d)', '(graded ',region_text(d['scheme'],r)) for n,r in sr.items()};s[8]=s[8].replace('(graded3:', '(graded 3:');s[11]=s[11].replace('(graded 2:1;0)', '(graded 2:1:0)');s[12]=s[12].replace('information14. on', 'information on');cards=[]
 def question(n):return re.sub(r'\s*\((?:i|ii|iii)\)','',p[n]).strip()
 def add(n,topic,concept,rows,notation,marks=6,suffix='',**extra):
  c=card(f'sa-q{n}{suffix}','A',f'Q{n}'+(' — '+suffix[1:] if suffix else ''),topic,concept,question(n),'',marks,notation,rows,pr[n]['page']);c.update(extra);cards.append(c);return c
 for n,topic,concept,lines,answers in [(1,'0-6','carbohydrate-statements',['Sugar and starch provide heat and energy to the body','Fibre helps to prevent bowel disorders','Carbohydrates contain the element nitrogen'],['True','True','False']),(5,'0-9','egg-nutrition-statements',['Eggs contain saturated fat','The protein in eggs is a low biological value protein','Eggs are a good source of vitamin C'],['True','False','False'])]:
  assert ' '.join(lines)==p[n].split('True False ',1)[1]
  add(n,topic,concept,[criterion(f'statement-{i}',line+' — '+answer,1,[0,2],'Published answer: '+answer+'. Graded 2:0.') for i,(line,answer) in enumerate(zip(lines,answers),1)],'3 required statements × 2 (2:0)')
 for n,topic,concept,count,steps,label in [(2,'0-10','food-choice-factors',3,[0,1,2],'factors'),(7,'0-3','pastry-success-guidelines',3,[0,1,2],'guidelines'),(8,'0-4','microorganism-growth-conditions',2,[0,2,3],'conditions'),(9,'0-11','paper-cardboard-packaging',3,[0,1,2],'advantages'),(10,'1-1','credit-purchase-advantages',3,[0,1,2],'advantages'),(12,'1-3','fridge-freezer-energy-label',2,[0,1,2,3],'information'),(13,'1-2','sale-goods-services-consumer-protection',3,[0,1,2],'ways')]:
  grade=':'.join(map(str,reversed(steps)));text=after(s[n],f'(graded {grade})');note=''
  if n==13:note='This question concerns the historical Act named in the paper; it is not current individual consumer advice. '
  if n==12:note='Use the original label. Annual consumption is energy in kWh, not a power rating. '
  c=add(n,topic,concept,[criterion('points',label,count,steps,f'{count} distinct responses, each graded {grade}. '+note+'Complete source guidance: '+text)],f'{count} responses × {steps[-1]} ({grade})')
  if n in [7,12]:c.update(questionFigureKey=f'home-economics-2026-ol-sa-q{n}-'+('pastry' if n==7 else 'energy-label'),questionFigureIncludesPrompt=(n==12))
 for answer in ['polyunsaturated','lipase','adipose']:assert answer in s[3]
 add(3,'0-7','lipid-terms',[criterion(str(i),label+' — '+answer,1,[0,2],'Correct completion: '+answer+'. Graded 2:0.') for i,(label,answer) in enumerate([('fatty acids found in oily fish','polyunsaturated'),('enzyme converting fats / lipids','lipase'),('tissue storing excess fats / lipids','adipose')],1)],'3 required blanks × 2 (2:0)')
 first,last=question(4).split('Name one dietary source',1)
 add(4,'0-8','vitamin-d-functions',[criterion('functions','functions',2,[0,1,2],'Two functions, each graded 2:1:0. Complete source guidance: '+after(s[4],'2 @ 2 marks (graded 2:1:0)','Name one dietary source'))],'2 functions × 2 (2:1:0)',marks=4,questionText=first.strip())
 add(4,'0-8','vitamin-d-dietary-source',[criterion('source',after(s[4],'1 @ 2 marks (graded 2:1:0)'),1,[0,1,2],'Name one valid dietary source; the actual published alternatives are shown in this claimable row. Graded 2:1:0.')],'1 source × 2 (2:1:0)',marks=2,suffix='-source',questionText='Name one dietary source'+last)
 descriptions=['Boiling fruit, vegetables, vinegar, sugar and spices together','A method of removing moisture from foods','Food is frozen at -25°C, small ice crystals are formed'];answers=['Chutney making','Drying','Quick freezing']
 table=d['scheme'][6].find_tables().tables[1].extract()
 for description,answer,cells in zip(descriptions,answers,table[1:]):assert [tidy(c) for c in cells if c is not None]==[description,answer]
 add(6,'0-3','preservation-process-matching',[criterion(str(i),description+' — '+answer,1,[0,2],'Published process: '+answer+'. Graded 2:0.') for i,(description,answer) in enumerate(zip(descriptions,answers),1)],'3 required matches × 2 (2:0)')
 labels=['Water pollution','Air pollution','Noise pollution'];values=named_sections(after(s[11],'(graded 2:1:0)'),[x+':' for x in labels])
 add(11,'1-5','pollution-examples',[criterion(str(i),label+' — '+value,1,[0,1,2],'Give one example of this required type. Complete published alternatives are shown in this claimable row. Graded 2:1:0.') for i,(label,value) in enumerate(zip(labels,values),1)],'3 required types × 2 (2:1:0)')
 labels=['Absorbent','Flammable','Crease resistant'];values=named_sections(after(s[14],'(graded 2:1:0)'),[x+':' for x in labels])
 add(14,'3-7','fabric-properties',[criterion(str(i),label+' — '+value,1,[0,1,2],'Explain this required property, graded 2:1:0.') for i,(label,value) in enumerate(zip(labels,values),1)],'3 required properties × 2 (2:1:0)',questionFigureKey='home-economics-2026-ol-sa-q14-fabrics',questionFigureIncludesPrompt=False)
 cards.sort(key=lambda c:(int(re.search(r'sa-q(\d+)',c['id']).group(1)),c['id']))
 assert len(cards)==15 and sum(c['totalMarks'] for c in cards)==84
 return cards

def write():
 write_scheme_transcript();cards=build();save_batch('A',cards,dict(tasks=15,marks=84,selectionDecisions='Vitamin D functions and dietary source have separate prompts and 4/2 tariffs. Required statements, matches, pollution examples and fabric properties stay whole. Closed and priced answers appear in claimable rows; open responses retain exact published partial steps and full guidance.',checked='2026-11-06'));print('2026 Ordinary A: 15 tasks, 84 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
