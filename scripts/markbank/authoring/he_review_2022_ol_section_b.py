#!/usr/bin/env python3
"""Review the twelve existing B tasks; four missing tasks are in the recovery writer."""
import json
import re
import sys
from he_review_2022_ol import ROOT, REVIEW, documents, page_text, criterion, between, named_sections

CLARIFICATIONS={
 'tooth-decay':dict(source='https://www.nidcr.nih.gov/health-info/tooth-decay',note='Decay is driven by acids produced by oral bacteria acting on sugars/starches, not simply calcium deficiency.'),
 'popcorn':dict(source='https://www.nal.usda.gov/exhibits/speccoll/exhibits/show/popcorn/how-does-popcorn-pop-',note='Water inside the heated kernel produces pressure; popping is not caused by starch absorbing fat.'),
 'cellulose':dict(source='https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/questions-and-answers-dietary-fiber',note='Cellulose remains non-digestible dietary fibre; cooking can soften the food without making cellulose digestible by human enzymes.'),
 'consent':dict(source='https://www2.hse.ie/services/sexual-health/what-is/',note='Sexual activity requires freely given, ongoing consent; marriage does not confer entitlement to sex.'),
 'marriage-consent':dict(source='https://data.oireachtas.ie/ie/oireachtas/act/2019/6/eng/enacted/a0619.pdf',note='Distinguish consensual arranged marriages from forced marriages. Do not generalise the scheme’s community example to all members of that community.'),
}


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]}
 tokens={1:['four','three','each','following','four'],2:['one'],3:['one','four','two'],4:['or','four','two'],5:['following','two']}
 for n,text in q.items():assert re.findall(r'\b(?:choose|select|one|two|three|four|five|either|or|each|following|any)\b',text,re.I)==tokens[n],n
 s={n:page_text(d['scheme'],n) for n in range(11,17)};fixes={}
 def put(n,part,marks,notation,rows):
  prompt=between(q[n],f'({part})',f'({marks} marks)').replace(' \uf0b7 ','\n• ');assert not re.search(r'\([a-d]\)',prompt)
  stem=q[n].split('(a)',1)[0].strip()
  if n==1:stem=stem.split('The table below',1)[0].strip()
  fixes[f'he-2022-ol-sb-q{n}{part}']=dict(reason='Complete 2022 Ordinary B source review, including required headings, open choices and partial marks.',set=dict(questionText=prompt,stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Paper and full scheme independently reviewed; see he_review_2022_ol_section_b.py.'))
 def body(text,grade):
  result=text.split(f'(graded {grade})',1)[1].strip();assert result.endswith('etc.'),result;return result
 put(1,'b',12,'3 ways × 4 (4:2:0)',[criterion('ways','ways',3,[0,2,4],'Three distinct ways, each graded 4:2:0. Complete published guidance: '+body(s[11].split('(b)',1)[1],'4:2:0'))])
 calcium=between(s[12],'(c)','(d)');functions=body(calcium.split('• dietary sources',1)[0],'4:2:0');sources=body(between(calcium,'• dietary sources','• effect of deficiency.'),'4:2:0');deficiency=body(calcium.split('• effect of deficiency.',1)[1],'4:2:0')
 put(1,'c',28,'Functions 3 × 4; sources 3 × 4; deficiency 4 (all 4:2:0)',[criterion('functions','functions in the body',3,[0,2,4],'Three functions, each graded 4:2:0. Complete published guidance: '+functions),criterion('sources','dietary sources',3,[0,2,4],'Three sources, each graded 4:2:0. Complete published guidance: '+sources),criterion('deficiency','effect of deficiency',1,[0,2,4],'One effect, graded 4:2:0. Source clarification: dental decay is caused by acids from oral bacteria acting on sugars/starches, not simply calcium deficiency. Complete historical guidance: '+deficiency)])
 buying,storing=named_sections(s[12].split('(d)',1)[1],['Buying:','Storing:'])
 put(1,'d',20,'4 × 5 (5:3:0): buying 1, storing 1, other 2',[criterion('buying','buying',1,[0,3,5],'One required buying factor, graded 5:3:0. Complete guidance: '+buying),criterion('storing','storing',1,[0,3,5],'One required storage factor, graded 5:3:0. Complete guidance: '+storing),criterion('other','plus 2 others',2,[0,3,5],'Two further distinct factors on either heading, each graded 5:3:0. Do not count the same point twice.')])
 put(2,'c',12,'3 effects × 4 (4:2:0)',[criterion('effects','effects of heat',3,[0,2,4],'Three effects, each graded 4:2:0. Source clarifications: popcorn expands when water in the heated kernel creates pressure, not because starch absorbs fat. Cooking softens food, but cellulose remains non-digestible dietary fibre. Complete published wording: '+body(s[13].split('(c)',1)[1],'4:2:0'))])
 put(3,'b',16,'4 guidelines × 4 (4:2:0)',[criterion('safety','safety guidelines',4,[0,2,4],'Four guidelines, each graded 4:2:0. Complete guidance: '+body(between(s[14],'(b)','(c)'),'4:2:0'))])
 put(3,'c',10,'2 ways × 5 (5:3:0)',[criterion('labelling','benefits the consumer',2,[0,3,5],'Two ways, each graded 5:3:0. Complete guidance: '+body(s[14].split('(c)',1)[1],'5:3:0'))])
 put(4,'a',16,'4 rights × 4 (4:2:0)',[criterion('rights','rights',4,[0,2,4],'Name and explain four rights, each graded 4:2:0. Published 2022 examination guidance: '+body(between(s[15],'(a)','(b)'),'4:2:0'))])
 appliance=between(s[15],'(b)','(c)');names,use,care=named_sections(appliance,['Type of appliance:','Guidelines for use:','Guidelines for care and cleaning:']);names=names.split('4 guidelines @',1)[0].strip();use=use.split('3 guidelines @',1)[0].strip()
 assert all(x.endswith('etc.') for x in [names,use,care])
 put(4,'b',24,'Type 3; use 4 × 3; care/cleaning 3 × 3 (all 3:2:0)',[criterion('type','type of appliance',1,[0,2,3],'Name the appliance studied, graded 3:2:0. Published examples: '+names),criterion('use','guidelines for use',4,[0,2,3],'Four guidelines for the same chosen appliance, each graded 3:2:0. Use relevant guidance: '+use),criterion('care','guidelines for care and cleaning',3,[0,2,3],'Three relevant guidelines for the chosen appliance, each graded 3:2:0. Complete guidance: '+care)])
 put(4,'c',10,'2 benefits × 5 (5:3:0)',[criterion('benefits','benefits',2,[0,3,5],'Two benefits, each graded 5:3:0. Historical 2022 scheme examples: '+body(s[15].split('(c)',1)[1],'5:3:0'))])
 put(5,'a',20,'4 points × 5 (5:3:0)',[criterion('marriage','rights and responsibilities',4,[0,3,5],'Both headings are required; the scheme does not reserve an exact number for either. Four points, each graded 5:3:0. Source correction: marriage does not confer entitlement to sexual activity; freely given, ongoing consent is always required. Complete historical wording: '+body(between(s[16],'(a)','(b)'),'5:3:0'))])
 separation,divorce=named_sections(between(s[16],'(b)','(c)'),['Legal separation:','Divorce:'])
 put(5,'b',20,'4 × 5 (5:3:0): separation 1, divorce 1, other 2',[criterion('separation','legal separation',1,[0,3,5],'One required point, graded 5:3:0. Published 2022 guidance: '+separation),criterion('divorce','divorce',1,[0,3,5],'One required point, graded 5:3:0. Published 2022 guidance: '+divorce),criterion('other','plus 2 others',2,[0,3,5],'Two further distinct points on either heading, each graded 5:3:0; do not score a point twice. This is historical examination guidance.')])
 put(5,'c',10,'2 variations × 5 (5:3:0)',[criterion('variations','cultural variations',2,[0,3,5],'Two different variations, each graded 5:3:0. The question is open; the guidance headings are examples, not a finite selection pool. Distinguish consensual arranged marriage from forced marriage. The community example in the scheme is not a claim about all members. Complete historical wording: '+body(s[16].split('(c)',1)[1],'5:3:0'))])
 assert len(fixes)==12
 return fixes


def write():
 fixes=build();p=ROOT/'scripts/markbank/card-corrections.json';saved=json.loads(p.read_text());saved['home-economics'].update(fixes);p.write_text(json.dumps(saved,ensure_ascii=False,indent=1)+'\n')
 p=ROOT/REVIEW;review=json.loads(p.read_text());review['tasks']=[t for t in review['tasks'] if t['id'] not in fixes]+[dict(id=cid,status='source-reviewed',section='B',marks=f['set']['totalMarks']) for cid,f in fixes.items()]
 review['sectionBReview']=dict(tasks=16,marks=280,sourceClarifications=CLARIFICATIONS,selectionDecisions='Milk choice has two answer routes in one card; all meal courses/beverages are required; preservation and appliance are single open profiles. Required calcium, buying/storage, separation/divorce headings preserve exact tariffs. Cultural variations are open examples.',checked='2026-11-01');p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n');print('2022 Ordinary B: all sixteen tasks reviewed, full guidance and exact partial marks.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
