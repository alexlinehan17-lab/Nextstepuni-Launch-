#!/usr/bin/env python3
"""Source-pinned 2025 Ordinary main review: source extraction and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='examiner-reports/home-economics/papers/2025-ol-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2025-ol-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2025/LC098GLP000EV.pdf'
HASHES={PAPER_A:'f1d9435a507af6a43aeac07851aa75413ab4875a93c3c68c1e62bf402d4010a3',PAPER_BC:'398dde1de551cdbce0ac53623c6b7297011f70f9bf6eaca982f2dce57c9d13da',SCHEME:'479835ebb1deae606c8bebd92dbd833129874d66d0dcac91c1f4a6390d5affb5'}
REVIEW='scripts/markbank/authoring/home-economics/2025-ol-main-review.json'

def page_text(doc,n):
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,740 if doc.name.endswith('2025-ol-014-paper.pdf') else 760)))

def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 return dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))

def originals():return {c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/home-economics.json').read_text())}

def source_material(page):return dict(kind='source-question',label='OFFICIAL QUESTION',title='Source and question',pages=[page],attribution='SEC Home Economics 2025 Ordinary Level examination paper — © State Examinations Commission.',presentationNote='Open the original examination page to review this task in context.')

def save_batch(section,fixes,added,review_data):
 p=ROOT/'scripts/markbank/card-corrections.json';data=json.loads(p.read_text());data['home-economics'].update(fixes);p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text())
 for c in added:
  i=next((i for i,v in enumerate(data) if v['id']==c['id']),None)
  if i is None:data.append(c)
  else:data[i]=c
 p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2025,level='ordinary',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 32 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–31, back cover 32.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 37 pages: cover 1, guidance/rubrics/annotations 2–5, A 6–9, B 10–15, C 16–23, separate food-studies coursework 24–35, blank 36, back cover 37. Coursework is a separate assessment, not a written-paper task.'),expectedTasks=60,expectedSectionTasks=dict(A=16,B=16,C=28),offeredPracticeMarks=749,candidateMarks=[280,320],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]
 r['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items()]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def build():
 d=documents();pr=a_regions(d['a'],range(3,8),740);p={n:re.sub(r'^\d+\.\s*','',region_text(d['a'],r)) for n,r in pr.items()};s={n:region_text(d['scheme'],r) for n,r in a_regions(d['scheme'],range(6,10),760).items()};old=originals();fixes={};added=[]
 def prompt(n):return re.sub(r'\s*\((?:i|ii|iii)\)','',p[n]).strip()
 def after(n,token,end=None):
  assert token in s[n],(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def put(n,marks,notation,rows,new=False,suffix='',**extra):
  cid=f'he-2025-ol-sa-q{n}{suffix}';v=dict(questionText=prompt(n),questionRef=f'2025 OL Section A Q{n}'+(' — '+suffix[1:] if suffix else ''),stem='',totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,sourceMaterial=source_material(pr[n]['page']));v.update(extra)
  if new:
   c=deepcopy(old[f'he-2025-ol-sa-q{n}' if n<14 else 'he-2025-ol-sa-q12']);c.update(v,id=cid,conceptId=('fabric-care-symbols' if n==14 else c['conceptId']+suffix));added.append(c)
  else:fixes[cid]=dict(reason='2025 Ordinary A full source review: original prompts/tables, all guidance and exact partial tariffs.',set=v)
 for n in [1,3]:
  statements=p[n].split('True False ',1)[1];lines=['High salt intake is linked with high blood pressure','Ultra-processed foods are less healthy than fresh foods','Vitamin B and Vitamin C are fat soluble vitamins'] if n==1 else ['Oily fish contains omega 3 fatty acids','Fish flesh is made up of short fibres called myomeres','White fish is high in fat']
  assert ' '.join(lines)==statements
  put(n,6,'3 statements × 2 (2:0)',[criterion(f'statement-{i}',line+' — '+answer,1,[0,2],'Published answer: '+answer+'. Graded 2:0.') for i,(line,answer) in enumerate(zip(lines,['True','True','False']),1)])
 put(2,4,'2 functions × 2 (2:1:0)',[criterion('functions','functions',2,[0,1,2],'Two functions, each graded 2:1:0. Complete guidance: '+after(2,'(graded 2:1:0)','Name one dietary'))],questionText=prompt(2).split('Name one',1)[0].strip())
 put(2,2,'1 source × 2 (2:0)',[criterion('source','dietary source',1,[0,2],'One source, graded 2:0. Complete examples: '+after(2,'(graded 2:0)'))],new=True,suffix='-source',questionText='Name one'+prompt(2).split('Name one',1)[1])
 put(4,6,'3 blanks × 2 (2:0)',[criterion(k,label+' — '+answer,1,[0,2],'Correct completion: '+answer+'. Graded 2:0.') for k,label,answer in [('movement','movement of food','dietary fibre'),('glucose','Glucose releases heat','energy'),('storage','Excess carbohydrate','liver')]])
 for n,count,steps,label in [(5,2,[0,2,3],'effects'),(6,3,[0,1,2],'guidelines'),(8,3,[0,1,2],'benefits'),(11,3,[0,1,2],'factors'),(12,3,[0,1,2],'uses'),(13,3,[0,1,2],'disadvantages')]:
  grade=':'.join(map(str,reversed(steps)));put(n,6,f'{count} points × {steps[-1]} ({grade})',[criterion('points',label,count,steps,f'{count} distinct points, each graded {grade}. Complete guidance: '+after(n,f'(graded {grade})'))])
 # Table labels and answers are lifted separately to retain the original paper's "suggest" wording.
 dishes=['Pasta carbonara','Lemon cheesecake','Cheese sandwich'];answers=['parmesan cheese','cream cheese','cheddar cheese slices']
 for dish,answer in zip(dishes,answers):assert dish+' '+answer in s[7]
 put(7,6,'3 matches × 2 (2:1:0)',[criterion(str(i),dish+' — '+answer,1,[0,1,2],'Suitable cheese: '+answer+'. Graded 2:1:0.') for i,(dish,answer) in enumerate(zip(dishes,answers),1)])
 labels=['Money available','Time available','Equipment available'];values=named_sections(after(9,'(graded 2:1:0)'),labels)
 put(9,6,'3 required factors × 2 (2:1:0)',[criterion(str(i),label,1,[0,1,2],'Explain this required factor, graded 2:1:0. Complete guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 put(10,4,'2 sources × 2 (2:1:0)',[criterion('sources','sources',2,[0,1,2],'Two types/sources, each graded 2:1:0. Source clarification: nuclear power uses non-renewable fuel; hydrogen is an energy carrier and is only renewable when made using renewable sources. These two historical acceptances must not be taught as unqualified renewable sources. Complete historical wording: '+after(10,'(graded 2:1:0)','Explain one benefit'))],questionText=prompt(10).split('Explain one benefit',1)[0].strip())
 put(10,2,'1 benefit × 2 (2:1:0)',[criterion('benefit','benefit',1,[0,1,2],'One benefit, graded 2:1:0. Complete guidance: '+s[10].rsplit('(graded 2:1:0)',1)[1].strip())],new=True,suffix='-benefit',questionText='Explain one benefit'+prompt(10).split('Explain one benefit',1)[1])
 wash,iron=after(14,'(graded 3:2:0)').split('(www.woolmark.com)',1)
 put(14,6,'2 symbols × 3 (3:2:0)',[criterion('wash','hand wash only',1,[0,2,3],'First symbol, graded 3:2:0. Complete guidance: '+wash.strip()),criterion('iron','medium iron',1,[0,2,3],'Second symbol, graded 3:2:0. Complete guidance: '+iron.replace('(www.omo.com)','').strip())],new=True,topicId='home-economics-1-4',questionFigureKey='home-economics-2025-ol-sa-q14-care-symbols',questionFigureIncludesPrompt=False,figureKey='')
 assert len(fixes)==13 and len(added)==3 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==84
 return fixes,added

def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=16,marks=84,selectionDecisions='Protein functions/source and renewable-energy sources/benefit have independent prompts and tariffs. Required table cells, statements and money/time/equipment headings remain whole. All scheme examples retained. Missing care-symbol task recovered with both original symbols.',sourceClarifications={'renewable-energy':dict(sources=['https://www.eia.gov/energyexplained/what-is-energy/sources-of-energy.php','https://www.eia.gov/energyexplained/hydrogen/'],note='Nuclear power is non-renewable; hydrogen is an energy carrier produced from renewable or non-renewable sources.')},checked='2026-11-06'));print('2025 Ordinary A: 16 tasks, 84 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
