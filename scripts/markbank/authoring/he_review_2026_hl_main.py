#!/usr/bin/env python3
"""2026 Higher: independently inspected sources, shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='paper-trail-corpus/exampapers/2026/LC098ALP014EV.pdf'
PAPER_BC='paper-trail-corpus/exampapers/2026/LC098ALP039EV.pdf'
SCHEME='paper-trail-corpus/markingschemes/2026/LC098ALP000EV.pdf'
HASHES={PAPER_A:'d52d52c9b5a7b8c0274dcbc67c1118b06f3d302238b8b66669155a4526c4de73',PAPER_BC:'32ddb5ae4cda9b1ae4ab638b1a33c6a5cd10a1d137b768ab112e8c01693ae228',SCHEME:'45f563434c737a5a5fa6faf8e08705ebd08ddbd9aa4148ae3619377cdf9456b7'}
REVIEW='scripts/markbank/authoring/home-economics/2026-hl-main-review.json'
CLARIFICATIONS={'uht':dict(source='https://www.fsai.ie/getmedia/2d516a18-247a-41e4-ab78-93fdd9eb8837/Farmhouse-Cheesemakers-Workbook-FINAL.pdf?ext=.pdf',note='UHT requires at least 135°C with a suitable holding time; the source table gives 132°C (130–135°C).'),'transformer':dict(source='https://www.se.com/us/en/faqs/FA115747/',note='A transformer changes voltage, not the supply frequency.'),'flash-point':dict(source='https://www.nist.gov/glossary-term/38496',note='Flash-point testing applies an ignition source; spontaneous ignition is a different property.'),'food-toxins':dict(source='https://www.cdc.gov/staph-food-poisoning/about/',note='Cooking can kill Staph bacteria but does not destroy its toxin. The scheme’s generic boiling-time statement is not safe decontamination guidance.')}

def write_scheme_transcript():
 doc=documents()['scheme']
 target=ROOT/'examiner-reports/home-economics/schemes/2026-hl.md'
 target.write_text('# SEC Home Economics 2026 Higher marking scheme\n\n'+'\n\n'.join(f'## Physical page {i+1}\n\n'+ '\n'.join(line.rstrip() for line in page.get_text().splitlines()).strip() for i,page in enumerate(doc))+'\n')


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 return dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))

def page_text(doc,n):return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,790 if doc.name.endswith("LC098ALP000EV.pdf") else 740)))

def card(key,section,ref,topic,concept,prompt,stem,marks,notation,rows,page,**extra):
 c=dict(id='he-2026-hl-'+key,subjectId='home-economics',topicId='home-economics-'+topic,conceptId=concept,level='higher',year=2026,section=section,questionRef='2026 HL Section '+section+' '+ref,questionText=prompt,stem=stem,figureKey='',labelKey=[],totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,sourceMaterial=dict(kind='source-question',label='OFFICIAL QUESTION',title='Source and question',pages=[page],attribution='SEC Home Economics 2026 Higher Level examination paper — © State Examinations Commission.',presentationNote='Open the original examination page to review this task in context.'),notes='Independently reviewed original paper and scheme. See 2026-hl-main-review.json. Required headings and same-answer name/details remain whole.');c.update(extra);return c

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
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2026,level='higher',sitting='main',language='ev',status='partial-carding; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled answer pages 9–39, back cover 40.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 40 pages: cover 1, guidance/rubrics/annotations 2–5, A 6–9, B 10–16, C 17–28, separate food-studies coursework 29–38, blank 39, back cover 40. Coursework is a separate assessment and is not counted as written-paper tasks.'),expectedTasks=60,expectedSectionTasks=dict(A=15,B=18,C=27),offeredPracticeMarks=749,candidateMarks=[280,320],sourceClarifications=CLARIFICATIONS,tasks=[])
 ids={c['id'] for c in cards};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks'],topicId=c['topicId'],questionRef=c['questionRef']) for c in cards];r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

def build():
 d=documents();pr=a_regions(d['a'],range(3,8),740);sr=a_regions(d['scheme'],range(6,10),790);p={n:re.sub(r'^\d+\.\s*','',region_text(d['a'],r)) for n,r in pr.items()};s={n:region_text(d['scheme'],r) for n,r in sr.items()};cards=[]
 def question(n):return re.sub(r'\s*\((?:i|ii|iii)\)','',p[n]).strip()
 def add(n,topic,concept,rows,notation,marks=6,suffix='',**extra):
  c=card(f'sa-q{n}{suffix}','A',f'Q{n}'+(' — '+suffix[1:] if suffix else ''),topic,concept,question(n),'',marks,notation,rows,pr[n]['page']);c.update(extra);cards.append(c);return c
 table=d['scheme'][5].find_tables().tables[0].extract();formula=['C6H12O6','C12H22O11','(C6H10O5)n'];labels=['Monosaccharide','Disaccharide','Polysaccharide'];rows=[];groups=[]
 for i,(label,value,column) in enumerate(zip(labels,formula,[3,6,9]),1):
  assert value in s[1];sample=tidy(table[2][column]);rows += [dict(id=f'formula-{i}',kind='point',verbatim=label+' — '+value,marks=1),any_points(f'example-{i}',label+' — Example',1,1,sample)];groups.append(dict(sourceCardId=f'he-2026-hl-sa-q1-column-{i}',label=label,marks=2,rowIds=[f'formula-{i}',f'example-{i}']))
 add(1,'0-6','carbohydrate-formulas-examples',rows,'6 required cells × 1 (1:0)',taskGroups=groups,questionFigureKey='home-economics-2026-hl-sa-q1-carbohydrate-table',questionFigureIncludesPrompt=False)
 values=named_sections(s[2],['Smoke Point','Flash Point']);rows=[]
 for i,(label,value) in enumerate(zip(['Smoke Point','Flash Point'],values),1):
  text=after(value,'(graded 1:0)');note='Historical temperature examples vary by fat/oil and conditions. '+('Source correction: flash point involves an external ignition source; it is distinct from spontaneous autoignition. ' if i==2 else '')
  rows.append(any_points(str(i),label,3,1,text,note))
 add(2,'0-7','lipid-smoke-flash-points',rows,'2 required terms × 3 points × 1 (1:0)')
 add(3,'0-8','vitamin-c-functions',[criterion('functions','functions',3,[0,1,2],'Three functions, each graded 2:1:0. Complete historical guidance: '+after(s[3],'(graded 2:1:0)'))],'3 functions × 2 (2:1:0)')
 values=named_sections(s[4],['Caramelisation','Crystallisation']);rows=[]
 for i,(label,value) in enumerate(zip(['Caramelisation','Crystallisation'],values),1):
  text=after(value,'(graded 1:0)').split('Accept culinary application',1)[0].strip();rows.append(any_points(str(i),label,3,1,text,'A culinary application is accepted. The printed temperatures describe the historical model. '))
 add(4,'0-6','carbohydrate-caramelisation-crystallisation',rows,'2 required properties × 3 points × 1 (1:0)')
 table=d['scheme'][6].find_tables().tables[0].extract();values=[tidy(table[1][i]) for i in [3,6,9]]
 add(5,'0-9','uht-milk-processing',[criterion('temperature','Temperature — '+values[0],1,[0,1,2],'Source correction: UHT requires at least 135°C with a suitable holding time. The printed historical answer 132°C (130–135°C) is below that requirement except at its upper limit. Graded 2:1:0.'),criterion('time','Time — '+values[1],1,[0,1,2],'Historical scheme holding time, graded 2:1:0; a valid industrial process depends on the temperature/time combination.'),criterion('effect','Effect',1,[0,1,2],'One effect, graded 2:1:0. Complete source examples: '+values[2])],'3 required cells × 2 (2:1:0)',questionFigureKey='home-economics-2026-hl-sa-q5-uht-table',questionFigureIncludesPrompt=False)
 q=question(6);definition,factors=q.split('State two factors',1)
 add(6,'0-1','basal-metabolic-rate',[criterion('definition','Basal Metabolic Rate',1,[0,1,2],'Definition, graded 2:1:0. Complete guidance: '+after(s[6],'(graded 2:1:0)','State two factors'))],'Definition 2 (2:1:0)',marks=2,questionText=definition.strip())
 add(6,'0-1','basal-metabolic-rate-factors',[any_points('factors','factors',2,2,after(s[6],'(graded 2:0)'),'Complete historical factors; no partial mark is printed. ')],'2 factors × 2 (2:0)',marks=4,suffix='-factors',questionText='State two factors'+factors)
 add(7,'0-8','iron-absorption-factors',[criterion('factors','factors',2,[0,1,2,3],'Two explained factors, each with printed partial steps 3:2:1; zero is available for an absent/incorrect response. One card covers either enhancing or inhibiting factors; no quota is printed. Complete historical guidance: '+after(s[7],'(graded 3:2:1)'))],'2 factors × 3 (3:2:1; zero for no credit)')
 add(8,'0-4','fsai-role',[criterion('roles','roles',3,[0,1,2],'Three roles, each graded 2:1:0. Complete guidance: '+after(s[8],'(graded 2:1:0)'))],'3 roles × 2 (2:1:0)')
 values=named_sections(s[9],['Infectious Food Poisoning','Toxic Food Poisoning']);rows=[]
 for i,(label,value) in enumerate(zip(['Infectious Food Poisoning','Toxic Food Poisoning'],values),1):
  text=after(value,'(graded 1:0)');note='These are historical examination descriptions; incubation time and heat resistance depend on the organism/toxin. '+('Source correction: cooking does not destroy Staph toxin. Do not treat the generic “boil for 30 minutes” example as a method to make contaminated food safe. ' if i==2 else '')
  rows.append(any_points(str(i),label,3,1,text,note))
 add(9,'0-4','infectious-toxic-food-poisoning',rows,'2 required types × 3 points × 1 (1:0)')
 values=named_sections(s[10],['Transformer','Magnetron'])
 add(10,'1-3','microwave-components',[criterion('transformer','Transformer',1,[0,1,2,3],'Explain its function, graded 3:2:1:0. Source correction: a transformer raises voltage, not supply frequency. Historical wording: '+after(values[0],'(graded 3:2:1:0)')),criterion('magnetron','Magnetron',1,[0,1,2,3],'Explain its function, graded 3:2:1:0. Complete guidance: '+after(values[1],'(graded 3:2:1:0)'))],'2 functions × 3 (3:2:1:0)')
 add(11,'1-4','furniture-fire-safety-label',[criterion('information','information',2,[0,2,3],'Two pieces of information, each graded 3:2:0. Answer about the legislation named in the historical paper; a labelled sketch is accepted. Complete guidance: '+after(s[11],'(graded 3:2:0)'))],'2 information points × 3 (3:2:0)')
 values=[after(s[12],'Contributory Old Age Pension','Non-Contributory Old Age Pension'),after(s[12],'Non-Contributory Old Age Pension')]
 add(12,'1-1','state-pension-types',[any_points(str(i),label,3,1,after(value,'(graded 1:0)'),'The source explicitly gives 2025 rates and historical eligibility summaries, not current benefit advice. ') for i,(label,value) in enumerate(zip(['Contributory Old Age Pension','Non-Contributory Old Age Pension'],values),1)],'2 required pension types × 3 points × 1 (1:0)')
 add(13,'3-3','housing-development-trends',[criterion('trends','trends',3,[0,1,2],'Three analysed trends, each graded 2:1:0. Recent refers to the 2026 examination context. Complete guidance: '+after(s[13],'(graded 2:1:0)'))],'3 trends × 2 (2:1:0)')
 add(14,'1-1','mabs-role',[criterion('points','points',2,[0,2,3],'Two discussed points, each graded 3:2:0. Complete guidance: '+after(s[14],'(graded 3:2:0)'))],'2 points × 3 (3:2:0)')
 assert len(cards)==15 and sum(c['totalMarks'] for c in cards)==84
 return cards

def write():
 write_scheme_transcript();cards=build();save_batch('A',cards,dict(tasks=15,marks=84,selectionDecisions='BMR definition/factors have independent prompts and 2/4 tariffs. All required carbohydrate cells, terms, processing cells and pension types remain whole. Binary one-mark source clauses are directly claimable option rows; open judged responses preserve exact partial-credit ladders and full guidance.',checked='2026-11-06'));print('2026 Higher A: 15 tasks, 84 offered marks.')
if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
