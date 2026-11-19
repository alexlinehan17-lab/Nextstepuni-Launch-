#!/usr/bin/env python3
"""Source-pinned 2021 Ordinary main review; shared helpers and Section A."""
from copy import deepcopy
import hashlib,json,re,sys
import fitz
from he_review_2023_hl import ROOT,tidy,between,criterion
from he_review_2023_hl_deferred import a_regions,region_text
from he_review_2023_hl_deferred_c1 import named_sections
PAPER_A='examiner-reports/home-economics/papers/2021-ol-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2021-ol-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2021/LC098GLP000EV.pdf'
HASHES={PAPER_A:'75d58efd9c87f4d18c5800212a7e19537264cdfe1bfebd15e9903aeb95b54822',PAPER_BC:'14d85cdaeefa4491d30a42cbed2a367ecd3e9037953145ef4daff34786960c0e',SCHEME:'8f7e8b5c26529cc1f087117b873cf2b1f545e55db5deb6f2aaa19fb87448355e'}
REVIEW='scripts/markbank/authoring/home-economics/2021-ol-main-review.json'


def page_text(doc,n):
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,doc[n-1].rect.width,730 if doc.name.endswith('LC098GLP000EV.pdf') else 760)))


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 d=dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))
 pattern=r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b'
 expected_a={1:['each','following','or'],2:['following'],3:['one','two'],4:['each','following','or'],5:['three'],6:['each','following','or'],7:['three','one','each'],8:['each','following','or'],9:['or'],10:['two','one'],11:['two'],12:['three'],13:['each','following'],14:['each','following']}
 expected_bc={2:['one','each','or','four','three','each','following','four'],3:['four','one','two'],4:['four','two','two','one','one','each','following','one'],5:['or','one','or','either','or','either','or','four','each','following','or','or','three'],6:['either','or','one','either','one','each','following','two','or','each','following'],7:['either','or','each','following','four','three','three','each','following','or','one'],8:['either','or','three','following','or','or','three','three']}
 for n,r in a_regions(d['a'],range(3,8),760).items():assert re.findall(pattern,region_text(d['a'],r),re.I)==expected_a[n],n
 for n,tokens in expected_bc.items():assert re.findall(pattern,page_text(d['bc'],n),re.I)==tokens,n
 return d


def originals():return {c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/home-economics.json').read_text())}


def card(key,section,ref,topic,concept,question,stem,marks,notation,rows,page):
 from he_review_2022_ol import card as previous
 c=previous(key,section,ref,topic,concept,question,stem,marks,notation,rows,page)
 c['id']=c['id'].replace('2022','2021');c['year']=2021;c['questionRef']=c['questionRef'].replace('2022','2021');c['sourceMaterial']['attribution']=c['sourceMaterial']['attribution'].replace('2022','2021');c['notes']='Source-pinned 2021 Ordinary paper and full scheme review; see he_review_2021_ol_main.py.'
 return c


def save_batch(section,fixes,added,review_data):
 p=ROOT/'scripts/markbank/card-corrections.json';data=json.loads(p.read_text());data['home-economics'].update(fixes);p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/'scripts/markbank/authored/home-economics.json';data=json.loads(p.read_text())
 for c in added:
  i=next((i for i,v in enumerate(data) if v['id']==c['id']),None)
  if i is None:data.append(c)
  else:data[i]=c
 p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;r=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2021,level='ordinary',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 32 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–31, back cover 32.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 40 pages: cover 1, guidance/rubrics 2–3, A 4–8, B 9–14, C 15–25, explicit blanks 26–27, separate food-studies coursework 28–36, blanks 37–39, back cover 40. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=61,expectedSectionTasks=dict(A=17,B=17,C=27),offeredPracticeMarks=749,candidateMarks=[200,240],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};r['tasks']=[t for t in r['tasks'] if t['id'] not in ids]
 r['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items() if not f.get('drop')]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 r[f'section{section}Review']=review_data;p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


def build():
 d=documents();s={n:region_text(d['scheme'],r) for n,r in a_regions(d['scheme'],range(4,9),730).items()};old=originals();fixes={};added=[]
 def put(n,marks,notation,rows,**extra):
  fixes[f'he-2021-ol-sa-q{n}']=dict(reason='Full 2021 Ordinary A source review: complete prompt, independent task boundaries and exact published partial credit.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def split(n,suffix,prompt,marks,notation,rows):
  c=deepcopy(old[f'he-2021-ol-sa-q{n}']);c.update(id=f'he-2021-ol-sa-q{n}-{suffix}',conceptId=c['conceptId']+'-'+suffix,questionRef=f'2021 OL Section A Q{n} — {suffix}',questionText=prompt,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Independent printed prompt with its own published tariff. See he_review_2021_ol_main.py.');added.append(c)
 statements={
  1:[('Meat contains high biological value protein',True),('Proteins are large molecules made up of smaller units called amino acids',True),('Sugar is a source of protein',False)],
  4:[('Peas, beans and lentils are pulse vegetables',True),('Fruit and vegetables do not contain fibre',False),('Vegetables have a high water content',True)],
  6:[('Food is processed to extend its shelf life',True),('An example of cross contamination is the transfer of bacteria from raw to cooked food',True),('Cooking food at 50°C kills all bacteria',False)],
  8:[('Periodontal/gum disease affects the tissues surrounding the teeth',True),('A lacto-vegetarian does not eat dairy produce',False),('A high fibre diet reduces the risk of bowel disease',True)]}
 for n,items in statements.items():
  put(n,6,'3 statements × 2 (2:0)',[criterion(f'statement-{i}',text+' — '+('True' if correct else 'False'),1,[0,2],'Published answer, graded 2:0; no partial credit.') for i,(text,correct) in enumerate(items,1)],questionText='Indicate with a tick (✓) whether each of the following statements is true or false.\n\n'+'\n'.join(text for text,_ in items))
 put(2,6,'3 statements × 2 (2:0)',deepcopy(old['he-2021-ol-sa-q2']['rows']),questionText='Using the words listed below, complete the following statements in relation to minerals.\n\ncalcium    osteoporosis    iron\n\nA deficiency of calcium in the diet can cause ___________________________.\nVitamin C assists in _______________________ absorption.\nCheese is a good dietary source of ___________________________.')
 put(3,2,'1 cause × 2 (2:1:0)',[criterion('cause','Cause of toughness',1,[0,1,2],'One cause, graded 2:1:0. Complete historical guidance: '+between(s[3],'(graded 2:1:0)','Name two methods'))],questionText='Outline one cause of toughness in meat.',questionRef='2021 OL Section A Q3 — cause')
 split(3,'methods','Name two methods of tenderising meat.',4,'2 methods × 2 (2:0)',[criterion('methods','methods of tenderising meat',2,[0,2],'Two different methods, each graded 2:0. Complete published examples: '+s[3].split('(graded 2:0)',1)[1].strip())])
 for n,label in [(5,'healthy eating guidelines'),(12,'uses of textiles')]:
  put(n,6,'3 points × 2 (2:1:0)',[criterion('points',label,3,[0,1,2],'Three different points, each graded 2:1:0. Complete guidance: '+s[n].split('(graded 2:1:0)',1)[1].strip())])
 flour=[('Self-raising flour','Cakes; biscuits; scones.'),('Wholemeal flour','Brown bread; brown scones; wholemeal pastry; wholemeal muffins.'),('Plain white flour (cream)','Pizza; apple tart; sauces; cupcakes; etc.')]
 put(7,6,'3 required flours × 2 (2:1:0)',[criterion(f'flour-{i}',label,1,[0,1,2],'One different culinary use for this required flour, graded 2:1:0. Complete cell guidance: '+body) for i,(label,body) in enumerate(flour,1)],questionText='Listed below are three types of flour. Give one different culinary use of each.\n\nSelf-raising flour\nWholemeal flour\nPlain white flour (cream)')
 put(9,6,'3 definitions × 2 (2:0)',deepcopy(old['he-2021-ol-sa-q9']['rows']),questionText='Match the method of food preservation with the correct definition.\n\nHeat treatment    Dehydration    Freezing\n\nBoiling fruit, vegetables or a mixture of both with sugar, vinegar and spices\nUsing very low temperatures which are unsuitable for enzyme activity and microbial growth\nPreserves food by removing moisture')
 put(10,4,'2 advantages × 2 (2:1:0)',[criterion('advantages','advantages',2,[0,1,2],'Two different advantages, each graded 2:1:0. Historical examination examples; actual cover depends on the policy. Complete guidance: '+s[10].split('(graded 2:1:0)',1)[1].split('Suggest one method',1)[0].strip())],questionText='Give two advantages of private health insurance.',questionRef='2021 OL Section A Q10 — advantages')
 split(10,'payment','Suggest one method of payment that could be used to purchase private health insurance.',2,'1 method × 2 (2:1:0)',[criterion('payment','Method of payment',1,[0,1,2],'One method, graded 2:1:0. Complete published examples: '+s[10].rsplit('(graded 2:1:0)',1)[1].strip())])
 put(11,4,'2 factors × 2 (2:0)',[criterion('factors','factors',2,[0,2],'Two factors, each graded 2:0. Complete guidance: '+s[11].split('(graded 2:0)',1)[1].split('How can electrical',1)[0].strip())],questionText='Outline two factors that should be considered when choosing electrical appliances.',questionRef='2021 OL Section A Q11 — choice factors')
 split(11,'disposal','How can electrical appliances be disposed of to avoid damage to the environment?',2,'1 point × 2 (2:0)',[criterion('disposal','point',1,[0,2],'One point, graded 2:0. Complete guidance: '+s[11].rsplit('(graded 2:0)',1)[1].strip())])
 labels=['Essential expenditure:','Discretionary expenditure:'];values=named_sections(s[13],labels)
 put(13,6,'2 required terms × 3 (3:2:1:0)',[criterion(f'term-{i}',label.rstrip(':'),1,[0,1,2,3],'Explain this required term, graded 3:2:1:0. Categories depend on household needs; source examples are historical, not a universal classification. Complete wording: '+body) for i,(label,body) in enumerate(zip(labels,values),1)],questionText='In relation to household expenditure, explain each of the following:\n\nEssential expenditure\nDiscretionary expenditure')
 symbols=card('sa-q14','A','Q14','1-4','fabric-care-symbols','What information does each of the following fabric care symbols convey to the consumer?','',6,'2 symbols × 3 (3:2:1:0)',[criterion('top','Hand wash',1,[0,1,2,3],'Top symbol, graded 3:2:1:0. Complete guidance: Hand wash only; wash by hand; used for wool/delicate fabrics; etc.'),criterion('bottom','Medium iron',1,[0,1,2,3],'Bottom symbol, graded 3:2:1:0. Complete guidance: Medium iron; warm iron; temperature for ironing wool/polyester mixtures; etc.')],7);symbols.update(questionFigureKey='home-economics-2021-ol-sa-q14-symbols',questionFigureIncludesPrompt=False);added.append(symbols)
 assert len(fixes)==13 and len(added)==4 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==84
 return fixes,added


def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=17,marks=84,selectionDecisions='A3 cause/methods, A10 insurance/payment and A11 purchase/disposal have independent published tariffs. Required true/false grids, word bank, matching definitions, flour headings, expenditure terms and both care symbols remain whole tasks. The scheme’s open example lists do not restrict valid answers.',checked='2026-11-01'));print('2021 Ordinary A: 17 reviewed tasks, 84 offered marks.')


if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))


