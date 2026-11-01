#!/usr/bin/env python3
"""Source-pinned 2022 Higher main review: shared helpers and Section A.

All 94 source pages were independently inspected before authoring. The review
remains partial until B/C, final Atlas crops and regression checks are complete.
"""
from copy import deepcopy
import hashlib
import json
import re
import sys
import fitz
from he_review_2023_hl import ROOT, tidy, between, criterion
from he_review_2023_hl_deferred_c1 import named_sections

PAPER_A='examiner-reports/home-economics/papers/2022-hl-014-paper.pdf'
PAPER_BC='examiner-reports/home-economics/papers/2022-hl-039-paper.pdf'
SCHEME='paper-trail-corpus/markingschemes/2022/LC098ALP000EV.pdf'
HASHES={PAPER_A:'40ccc02c39d133657b9248faeabca42ce92dbe286fce217d748bfd26f028bb5b',PAPER_BC:'d9fc4f8d3aa3f81a5258b9aabe3ba2824e81f5623db827a434d4843a0f31ec78',SCHEME:'703878ac5312b2cc5b087ce3c2243051f4b49b495ea81c67fbaa1a96efb3dade'}
REVIEW='scripts/markbank/authoring/home-economics/2022-hl-main-review.json'
CLARIFICATIONS={
 'foam':dict(source='https://www.ifst.org/lovefoodlovescience/resources/protein-foam-formation',note='Whisking mechanically unfolds proteins around air bubbles; subsequent heating sets the foam. Whisking does not need to generate cooking heat, as the scheme suggests.'),
 'ombudsman':dict(source='https://ombudsman.ie/en/publication/8e009-who-we-can-investigate/',note='The Office of the Ombudsman deals with public services. Its remit excludes banks, insurance companies and An Post, despite their inclusion in the historical scheme.'),
 'green-dot':dict(source='https://www.verpact.nl/en/green-dot-symbol',note='The symbol indicates financial participation in packaging recovery; it does not itself certify recyclability or recycled content.'),
 'ecolabel':dict(source='https://environment.ec.europa.eu/topics/circular-economy-topics/eu-ecolabel/articles-and-success-stories/eu-ecolabel-and-eus-sustainable-consumption-pledge_en',note='The EU Ecolabel concerns compliance with product-category environmental criteria assessed across the life cycle, not zero environmental impact.'),
}


def documents():
 for p,sha in HASHES.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 docs=dict(a=fitz.open(ROOT/PAPER_A),bc=fitz.open(ROOT/PAPER_BC),scheme=fitz.open(ROOT/SCHEME))
 from he_review_2023_hl_deferred import a_regions,region_text
 pattern=r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b'
 expected_a={1:['two','one'],2:[],3:['one'],4:[],5:['three'],6:['one'],7:['each','following'],8:['one'],9:['each','following'],10:['each','following'],11:['one'],12:['two','one','two'],13:['two'],14:['each','following']}
 expected_bc={2:['one','each'],3:['three','each','one'],4:[],5:['or','one','or','either','or','either','or','three','one','or'],6:['either','or','two','two','or','one'],7:['either','or','either','or','following','one','two','or','two'],8:['either','or','or']}
 for n,r in a_regions(docs['a'],range(3,8),760).items():assert re.findall(pattern,region_text(docs['a'],r),re.I)==expected_a[n],n
 for n,tokens in expected_bc.items():assert re.findall(pattern,page_text(docs['bc'],n),re.I)==tokens,n
 return docs


def page_text(doc,n):
 return tidy(doc[n-1].get_text(clip=fitz.Rect(0,35,595,775 if doc.page_count==42 else 760)))


def originals():
 return {c['id']:c for c in json.loads((ROOT/'scripts/markbank/authored/home-economics.json').read_text())}


def save_batch(section,fixes,added,review_data):
 p=ROOT/'scripts/markbank/card-corrections.json';saved=json.loads(p.read_text());saved['home-economics'].update(fixes);p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/'scripts/markbank/authored/home-economics.json';saved=json.loads(p.read_text())
 for c in added:
  index=next((i for i,v in enumerate(saved) if v['id']==c['id']),None)
  if index is None:saved.append(c)
  else:saved[index]=c
 p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text()) if p.exists() else dict(schemaVersion=1,year=2022,level='higher',sitting='main',language='ev',status='partial-review; all-source-pages-visually-reviewed; browser-QA-pending',sources={path:dict(sha256=sha,pages=len(fitz.open(ROOT/path))) for path,sha in HASHES.items()},visualSweep=dict(a='All 40 pages: cover 1, instructions 2, questions 3–7, answer instructions 8, ruled pages 9–39, back cover 40.',bc='All 12 pages: cover 1, B 2–4, C 5–8, explicit blanks 9–11, back cover 12.',scheme='All 42 pages: cover 1, guidance/rubrics 2–5, A 6–10, B 11–17, C 18–30, separate food-studies coursework 31–40, blank 41, back cover 42. Coursework is a separate assessment, not a task in these written-paper booklets.'),expectedTasks=62,expectedSectionTasks=dict(A=17,B=17,C=28),offeredPracticeMarks=749,candidateMarks=[200,240],tasks=[])
 ids=set(fixes)|{c['id'] for c in added};review['tasks']=[t for t in review['tasks'] if t['id'] not in ids]
 review['tasks'] += [dict(id=cid,status='source-reviewed',section=section,marks=f['set']['totalMarks']) for cid,f in fixes.items() if not f.get('drop')]+[dict(id=c['id'],status='source-reviewed',section=section,marks=c['totalMarks']) for c in added]
 review[f'section{section}Review']=review_data;p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')


def build():
 d=documents();raw='\n'.join(d['scheme'][n-1].get_text(clip=fitz.Rect(0,35,595,775)) for n in range(6,11));heads=list(re.finditer(r'(?m)^(\d{1,2})\.\s*\n',raw));assert [int(h[1]) for h in heads]==list(range(1,15))
 s={int(h[1]):tidy(raw[h.end():heads[i+1].start() if i+1<len(heads) else len(raw)]) for i,h in enumerate(heads)}
 old=originals();fixes={};added=[]
 def fix(n,marks,notation,rows,**extra):
  fixes[f'he-2022-hl-sa-q{n}']=dict(reason='Complete source review of 2022 Higher A, including independent prompts, required tables and source corrections.',set=dict(totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra))
 def split(n,suffix,question,marks,notation,rows):
  c=deepcopy(old[f'he-2022-hl-sa-q{n}']);c.update(id=f'he-2022-hl-sa-q{n}-{suffix}',conceptId=f'{c["conceptId"]}-{suffix}',questionRef=f'2022 HL Section A Q{n} — {suffix}',questionText=question,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Separate printed prompt with an independent published tariff. Source review: he_review_2022_hl_main.py.');added.append(c)
 functions=between(s[1],'(graded 2:1:0)','Identify one factor');absorption=s[1].split('(graded 2:0)',1)[1].strip()
 fix(1,4,'2 functions × 2 (2:1:0)',[criterion('functions','functions of calcium',2,[0,1,2],'Two functions, each graded 2:1:0. Complete guidance: '+functions)],questionText='State two functions of calcium in the body.',questionRef='2022 HL Section A Q1 — functions')
 split(1,'absorption','Identify one factor that affects calcium absorption.',2,'1 factor × 2 (2:0)',[criterion('factor','factor that affects calcium absorption',1,[0,2],'One factor, graded 2:0. Both increased and reduced absorption are in the published guidance: '+absorption)])
 fix(2,6,'3 required cells × 2 (2:0)',[criterion('enzyme','Amylase',1,[0,2],'Pancreatic juice: supply the enzyme, graded 2:0.'),criterion('substrate','Starch',1,[0,2],'Supply the substrate digested by this enzyme, graded 2:0.'),criterion('product','Maltose',1,[0,2],'Supply the resulting product, graded 2:0.')],questionText='Complete the table below in relation to the digestion of carbohydrates.\n\nSecretion: Pancreatic juice\nEnzyme: ______\nSubstrate: ______\nProduct: ______')
 foam=s[3].split('(graded 2:0)',1)[1].split('Give one culinary',1)[0].strip();examples=s[3].rsplit('(graded 2:0)',1)[1].strip()
 fix(3,4,'2 points × 2 (2:0)',[criterion('foam','foam formation',2,[0,2],'Two points, each graded 2:0. Source correction: whisking mechanically unfolds proteins, which surround and stabilise air bubbles; heating afterwards sets the foam. The historical claim that whisking generates sufficient heat is inaccurate. Complete historical wording: '+foam)],questionText='In relation to proteins, explain foam formation.',questionRef='2022 HL Section A Q3 — explanation')
 split(3,'example','Give one culinary example of foam formation.',2,'1 example × 2 (2:0)',[criterion('example','culinary example',1,[0,2],'One example, graded 2:0. Complete published examples: '+examples)])
 body=s[4].split('Trans Fatty acids',1)[1].strip();cis,trans=body.split('etc.',1);trans=trans.strip();assert trans.endswith('etc.')
 fix(4,6,'2 descriptions × 3 (3:2:1:0)',[criterion('cis','Cis Fatty acids',1,[0,1,2,3],'Describe the cis arrangement, graded 3:2:1:0. Published guidance: '+cis+'etc.'),criterion('trans','Trans Fatty acids',1,[0,1,2,3],'Describe the trans arrangement, graded 3:2:1:0. Published guidance: '+trans)])
 fix(5,6,'3 guidelines × 2 (2:1:0)',[criterion('guidelines','guidelines',3,[0,1,2],'Three different guidelines, each graded 2:1:0. Complete guidance: '+s[5].split('(graded 2:1:0)',1)[1].strip())])
 process,advantage=named_sections(s[6].split('Advantage 1 point @ 2 marks (graded 2:0)',1)[1],['Process','Advantage'])
 fix(6,4,'2 process points × 2 (2:1:0)',[criterion('process','Process',2,[0,1,2],'Two process points, each graded 2:1:0. Published 2022 example: '+process)],questionText='In relation to freezing, describe quick-freezing.',questionRef='2022 HL Section A Q6 — process')
 split(6,'advantage','Give one advantage of quick-freezing.',2,'1 advantage × 2 (2:0)',[criterion('advantage','Advantage',1,[0,2],'One advantage, graded 2:0. Complete guidance: '+advantage)])
 labels=['Polystyrene','Glass bottle','Waxed carton'];values=named_sections(s[7].split('(graded 2:0)',1)[1],labels)
 fix(7,6,'3 required packaging types × 2 (2:0)',[criterion(f'packaging-{i}',label,1,[0,2],'A different benefit for each required material, graded 2:0. Environmental properties depend on the particular material and available collection/processing system; these are historical scheme examples: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 names=between(s[8],'Moist methods of cooking:','Describe the underlying principle');principle=s[8].rsplit('(graded 2:0)',1)[1].strip()
 fix(8,6,'Method 2 + principle 2 × 2 (all 2:0)',[criterion('method','moist method of cooking',1,[0,2],'One method suitable for fish, graded 2:0. Complete names: '+names),criterion('principle','Underlying principle',2,[0,2],'Two points relevant to the method you named, each graded 2:0. The open named-method profile stays together. Complete guidance: '+principle)])
 labels=['Anti-caking agent','Emulsifier'];values=named_sections(s[9].split('(graded 3:2:0)',1)[1],labels)
 fix(9,6,'2 required functions × 3 (3:2:0)',[criterion(f'function-{i}',label,1,[0,2,3],'One function, graded 3:2:0. Published guidance: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 labels=['Pay Related Social Insurance (PRSI)','Universal Social Charge (USC)'];values=named_sections(s[10].split('(graded 3:2:0)',1)[1],labels)
 fix(10,6,'2 required explanations × 3 (3:2:0)',[criterion(f'income-{i}',label,1,[0,2,3],'One explanation, graded 3:2:0. Historical 2022 examination guidance; rates and rules are not presented as current advice: '+value) for i,(label,value) in enumerate(zip(labels,values),1)])
 agencies=s[11].rsplit('(graded 3:2:0)',1)[1].strip();assert 'District court/Small Claims Procedure:' in agencies and agencies.endswith('etc.')
 fix(11,6,'Name 3 + role 3 (both 3:2:0)',[criterion('agency','Name',1,[0,2,3],'Name one statutory agency, graded 3:2:0. The open choice is not restricted to a finite pool. Complete historical examples and roles: '+agencies),criterion('role','Role',1,[0,2,3],'One role of the same agency, graded 3:2:0. Source correction: the Office of the Ombudsman deals with public services; banks, insurance companies and An Post are outside its remit, despite their inclusion in this scheme. Do not confuse it with the Financial Services and Pensions Ombudsman.')])
 assurance=s[12].split('(graded 4:2:0)',1)[1].strip();assert 'Endowment life assurance' in assurance
 fix(12,6,'2 types × 1 (1:0) + comparison 4 (4:2:0)',[criterion('types','Name',2,[0,1],'Name two types, each graded 1:0. The comparison must refer to the same pair. Complete historical type descriptions: '+assurance),criterion('difference','Difference',1,[0,2,4],'One difference between your two named types, graded 4:2:0. Keep names and their dependent comparison in one response; the source examples are not a finite selection pool.')])
 fix(13,6,'2 pieces × 3 (3:2:0)',[criterion('label','information',2,[0,2,3],'Two pieces of information, each graded 3:2:0. Historical examination question about the named orders. Complete guidance: '+s[13].split('(graded 3:2:0)',1)[1].strip())])
 dot,eco=named_sections(s[14].split('(graded 3:2:0)',1)[1],['Green dot','Eco Label'])
 fix(14,6,'2 required symbols × 3 (3:2:0)',[criterion('green-dot','Green dot',1,[0,2,3],'Meaning of the first symbol, graded 3:2:0. Financial participation does not itself certify recyclability or recycled content. Published guidance: '+dot),criterion('eco-label','Eco Label',1,[0,2,3],'Meaning of the second symbol, graded 3:2:0. It certifies compliance with product-category environmental criteria across the life cycle, not zero impact. Published guidance: '+eco)],questionText='What information does each of the following symbols convey to the consumer?',questionFigureKey='home-economics-2022-hl-sa-q14-symbols',questionFigureIncludesPrompt=False,figureKey='')
 assert len(fixes)==14 and len(added)==3
 return fixes,added


def write():
 fixes,added=build();save_batch('A',fixes,added,dict(tasks=17,marks=84,sourceClarifications=CLARIFICATIONS,selectionDecisions='Q1, Q3 and Q6 each have two independent printed prompts and published tariffs. The required digestion table, packaging, additives, income terms and symbol pair remain whole tasks. Q8/Q11 are open named profiles and Q12 is a dependent comparison of the two named insurance types.',checked='2026-11-01'))
 print('2022 Higher A: 17 reviewed tasks, 84 offered marks; source figures still require final export.')


if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
