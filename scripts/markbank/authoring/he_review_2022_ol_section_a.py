#!/usr/bin/env python3
"""Review all Section A tariffs; preserve IDs and split two independent prompts."""
from copy import deepcopy
import json
import re
import sys
from he_review_2022_ol import ROOT, REVIEW, documents, page_text, criterion, tidy, between, named_sections

TOKENS={1:['each','following','or'],2:['two','one'],3:['one','each'],4:['following'],5:['two'],6:['three'],7:['each','following','or','or'],8:['three'],9:['each'],10:['one','each'],11:['two','one'],12:['each','following','or','any'],13:['three'],14:['each','following']}
CLARIFICATIONS={
 'lipid-membranes':dict(source='https://www.ncbi.nlm.nih.gov/books/NBK9928/',note='Lipids form cell membranes; human cells do not have cell walls. Retain the historical scheme wording with this correction.'),
 'reheating':dict(source='https://www.fsai.ie/consumer-advice/food-safety-and-hygiene/cooking-and-reheating',note='FSAI advises reheating to at least 70°C throughout. For stews/casseroles the liquid should boil for 3–5 minutes to heat the meat through; the source’s 100°C example is not a universal core-temperature rule.'),
}


def build():
 d=documents()
 def blocks(which,pages):
  raw='\n'.join(d[which][n-1].get_text(clip=__import__('fitz').Rect(0,0,595,760 if which=='a' else 810)) for n in pages)
  heads=list(re.finditer(r'(?m)^(\d{1,2})\.\s*\n',raw));assert [int(h[1]) for h in heads]==list(range(1,15))
  return {int(h[1]):tidy(raw[h.end():heads[i+1].start() if i+1<len(heads) else len(raw)]) for i,h in enumerate(heads)}
 p=blocks('a',range(3,8));s=blocks('scheme',range(6,11))
 for n,text in p.items(): assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b',text,re.I)==TOKENS[n],n
 old={c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/home-economics.json').read_text())};fixes={};added=[]
 def fix(n,rows,notation,**extra):
  fixes[f'he-2022-ol-sa-q{n}']=dict(reason='Paper pp3–7 and scheme pp6–10 independently reviewed, including floating answer text. See he_review_2022_ol_section_a.py.',set=dict(rows=rows,tariffModel=dict(kind='fixed',notation=notation),**extra))
 def guidance(n):return s[n].split('(graded 2:1:0)',1)[1].strip()
 for n in [1,7,12]:
  rows=deepcopy(old[f'he-2022-ol-sa-q{n}']['rows'])
  for row in rows:row['contextNote']='Published 2022 examination answer, graded 2:0; no partial credit.'
  extra={}
  if n==1:extra['questionText']=old['he-2022-ol-sa-q1']['questionText'].replace('Coronary heart disease is caused','Coronary heart disease can be caused')
  fix(n,rows,'3 statements × 2 (2:0)',**extra)
 functions=between(s[2],'2 functions @ 2 marks (graded 2:0)','Name one dietary source');sources=s[2].split('1 sources @ 2 marks (graded 2:0)',1)[1].strip()
 assert functions.endswith('etc.') and sources.endswith('seeds; etc.')
 fix(2,[criterion('functions','functions of lipids (fats)',2,[0,2],'Two functions, each graded 2:0. Source correction: lipids form cell membranes; human cells do not have cell walls. Complete published wording: '+functions)],'2 functions × 2 (2:0)',totalMarks=4,questionText='State two functions of lipids (fats).',questionRef='2022 OL Section A Q2 — functions')
 source=deepcopy(old['he-2022-ol-sa-q2']);source.update(id='he-2022-ol-sa-q2-source',conceptId='dietary-source-of-lipids',questionText='Name one dietary source of lipids (fats).',questionRef='2022 OL Section A Q2 — dietary source',totalMarks=2,tariffModel=dict(kind='fixed',notation='1 source × 2 (2:0)'),rows=[criterion('source','dietary source of lipids (fats)',1,[0,2],'One source, graded 2:0. Complete published examples: '+sources)],notes='Independent source prompt, with its own 2-mark tariff; functions stay on the original Q2 ID.');added.append(source)
 labels=['Roux based sauce','Egg based sauce','Sweet sauce'];values=named_sections(guidance(3),labels)
 fix(3,[criterion(f'sauce-{i}',name,1,[0,1,2],'One suitable example for this required sauce class, graded 2:1:0. Complete published examples: '+body) for i,(name,body) in enumerate(zip(labels,values),1)],'3 required classes × 2 (2:1:0)')
 rows=deepcopy(old['he-2022-ol-sa-q4']['rows'])
 for row in rows:row['contextNote']='Use the supplied word bank. Each required completed statement is graded 2:0.'
 fix(4,rows,'3 statements × 2 (2:0)')
 dishes=guidance(5).split('Cooking method Dishes',1)[1].strip()
 row=criterion('examples','examples of dishes',1,list(range(7)),'Supply two different baking dishes and two different grilling dishes. The scheme awards two examples at 2 marks (2:1:0), and two at 1 mark (1:0); it does not assign the higher tariff to a named cooking method. Keep all four examples within this six-mark task. Complete published examples: '+dishes)
 row['parts']=[dict(id=f'example-{i}',verbatim=f'Example {i} ({mark} marks)',marks=mark,permittedMarks=list(range(mark+1))) for i,mark in enumerate([2,2,1,1],1)]
 fix(5,[row],'2 examples × 2 (2:1:0) + 2 examples × 1 (1:0)',questionText='Give two different examples of dishes cooked using the cooking methods named below.\n\nBaking: (i), (ii)\nGrilling: (i), (ii)')
 for n,label in [(6,'meal planning guidelines'),(8,'factors'),(13,'factors')]:
  body=guidance(n).split('Citrus fruits',1)[0].strip();assert body.endswith('etc.'),(n,body)
  fix(n,[criterion('points',label,3,[0,1,2],'Three distinct points, each graded 2:1:0. Complete published guidance: '+body)],'3 points × 2 (2:1:0)')
 labels=['Food storage','Personal hygiene','Reheating food'];values=named_sections(guidance(9),labels)
 fix(9,[criterion(f'heading-{i}',name,1,[0,1,2],'One guideline under this required heading, graded 2:1:0. '+('Source clarification: FSAI advises at least 70°C throughout; for stews/casseroles boil the liquid for 3–5 minutes to heat meat through. The source’s 100°C example is not a universal core-temperature rule. ' if i==3 else '')+'Complete published wording: '+body) for i,(name,body) in enumerate(zip(labels,values),1)],'3 required headings × 2 (2:1:0)')
 labels=['Flavourings','Preservatives','Sweeteners'];values=named_sections(guidance(10),labels)
 fix(10,[criterion(f'class-{i}',name,1,[0,1,2],'One example of this required class, graded 2:1:0. Complete published examples: '+body) for i,(name,body) in enumerate(zip(labels,values),1)],'3 required classes × 2 (2:1:0)')
 advantages=guidance(11).split('Suggest one form',1)[0].strip();credit=page_text(d['scheme'],9).split('Loan;',1)[1].strip();credit='Loan; '+credit
 assert advantages.endswith('etc.') and credit=='Loan; hire purchase; PCP (personal contract plans); credit card; etc.'
 fix(11,[criterion('advantages','advantages of buying goods on credit',2,[0,1,2],'Two distinct advantages, each graded 2:1:0. Complete published examples: '+advantages)],'2 advantages × 2 (2:1:0)',totalMarks=4,questionText='State two advantages of buying goods on credit.',questionRef='2022 OL Section A Q11 — advantages')
 car=deepcopy(old['he-2022-ol-sa-q11']);car.update(id='he-2022-ol-sa-q11-car',conceptId='credit-for-a-car',questionText='Suggest one form of credit suitable for buying a car.',questionRef='2022 OL Section A Q11 — car credit',totalMarks=2,tariffModel=dict(kind='fixed',notation='1 form × 2 (2:1:0)'),rows=[criterion('credit','form of credit',1,[0,1,2],'One suitable form, graded 2:1:0. Published 2022 examples (extracted after the following question’s table): '+credit)],notes='Separate printed prompt with its own 2-mark tariff. Historical exam examples, not financial advice.');added.append(car)
 assert len(fixes)==13
 return fixes,added


def write():
 fixes,added=build();p=ROOT/'scripts/markbank/card-corrections.json';saved=json.loads(p.read_text());saved['home-economics'].update(fixes);p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/'scripts/markbank/authored/home-economics.json';saved=json.loads(p.read_text())
 for c in added:
  i=next((i for i,v in enumerate(saved) if v['id']==c['id']),None)
  if i is None:saved.append(c)
  else:saved[i]=c
 p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());ids=set(fixes)|{c['id'] for c in added};review['tasks']=[t for t in review['tasks'] if t['id'] not in ids]
 review['tasks'] += [dict(id=cid,status='source-reviewed',section='A',marks=fix['set'].get('totalMarks',6)) for cid,fix in fixes.items()]+[dict(id=c['id'],status='source-reviewed',section='A',marks=c['totalMarks']) for c in added]
 review['sectionAReview']=dict(tasks=16,marks=84,sourceClarifications=CLARIFICATIONS,selectionDecisions='All three true/false grids, the whole word bank, all required table headings, and open example counts remain one task each. Q2/Q11 have independent separately priced prompts. Q5 retains the unassigned 2+2+1+1 tariff without inventing which method gets two marks.',checked='2026-11-01');p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');print('2022 Ordinary A: 16 source-reviewed tasks; separate lipid source and car credit; full guidance and published partial credit.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
