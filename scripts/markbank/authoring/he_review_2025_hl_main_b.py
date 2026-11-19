#!/usr/bin/env python3
"""Finish 2025 Higher Section B from the pinned original paper and scheme."""
from copy import deepcopy
import json,re,sys
from he_review_2025_hl_main import ROOT,documents,page_text,originals,save_batch,criterion,between,named_sections,tidy

ALIASES={
 'he-2025-hl-sb-q1b-mono':'he-2025-hl-sb-q1b',
 'he-2025-hl-sb-q1b-poly':'he-2025-hl-sb-q1b',
 'he-2025-hl-sb-q4b-features':'he-2025-hl-sb-q4b-principle',
}
CLARIFICATIONS={
 'food-temperature':dict(source='https://www.fsai.ie/consumer-advice/food-safety-and-hygiene/cooking-and-reheating',note='Reheating guidance is 70°C or higher at the core, not the scheme’s above-100°C statement.'),
 'food-storage':dict(source='https://www.fsai.ie/consumer-advice/food-safety-and-hygiene/storage',note='Thawed food may be frozen after thorough cooking; the scheme’s never-refreeze statement needs that distinction.'),
 'botulism':dict(source='https://www.who.int/news-room/fact-sheets/detail/botulism',note='The scheme’s pH 4–6 wording is imprecise: C. botulinum does not grow below pH 4.6.'),
 'fatty-acids':dict(source='https://ods.od.nih.gov/factsheets/Omega3FattyAcids-HealthProfessional/',note='Distinguish essential fatty acids and research on health outcomes from the scheme’s blanket medical claims.'),
}


def build():
 d=documents();p={n:page_text(d['bc'],n) for n in [2,3,4]};q={1:p[2].rsplit('Question 1',1)[1],2:between(p[3],'Question 2','Question 3'),3:p[3].split('Question 3',1)[1],4:between(p[4],'Question 4','Question 5'),5:p[4].split('Question 5',1)[1]};s={n:page_text(d['scheme'],n) for n in range(11,19)};old=originals();fixes={}
 def body(n,token,end=None):
  assert s[n].count(token)==1,(n,token);t=s[n].split(token,1)[1];assert end is None or end in t,(n,end);return (t.split(end,1)[0] if end else t).strip()
 def put(n,part,marks,notation,rows,suffix='',**extra):
  cid=f'he-2025-hl-sb-q{n}{part}{suffix}';assert cid in old,cid
  stem=q[n].split('(a)',1)[0].strip() if n!=1 else 'In 2024, a survey identified the main food sources of energy in the diet of adults in Ireland.'
  value=dict(questionText=between(q[n],f'({part})',f'({marks} marks)').replace(' • ','\n• '),questionRef=f'2025 HL Section B Q{n}({part})',stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,**extra)
  fixes[cid]=dict(reason='Complete source-pinned 2025 Higher B review: original prompts, required headings, exact partial marks and every printed model.',set=value)
 def points(n,part,marks,count,steps,text,**extra):
  grade=':'.join(map(str,reversed(steps)));put(n,part,marks,f'{count} points × {steps[-1]} ({grade})',[criterion('points','points',count,steps,f'{count} distinct developed points, each graded {grade}. Complete scheme guidance: '+text)],**extra)
 chart=body(11,'4 points @ 5 marks (graded 5:4:3:2:1:0)')+' '+s[12].split('(b)',1)[0].strip()
 for label in ['23%','21%','16%','14%','9%','7%','5%','3%']:assert label in chart
 points(1,'a',20,4,list(range(6)),chart,questionFigureKey='home-economics-2025-hl-sb-q1a-chart',questionFigureIncludesPrompt=False,figureKey='')
 names=['Saturated fatty acids','Monounsaturated fatty acids','Polyunsaturated fatty acids'];values=named_sections(body(12,'1 example @ 2 marks (graded 2:0) x 3').removesuffix('Accept clear diagrams').strip(),names);rows=[];groups=[]
 for i,(name,value) in enumerate(zip(names,values),1):
  structure,example=value.split('Example ',1)
  rows += [criterion(f'structure-{i}','Structure',4,[0,1],'Four structure points at 1 mark each. Accept clear diagrams. '+structure),criterion(f'example-{i}','Example',1,[0,2],'One example, graded 2:0. '+example)]
  groups.append(dict(sourceCardId=f'he-2025-hl-sb-q1b-heading-{i}',label=name,marks=6,rowIds=[f'structure-{i}',f'example-{i}']))
 put(1,'b',18,'3 required acids × (4 structure points × 1 + example 2 (2:0))',rows,taskGroups=groups)
 points(1,'c',12,3,list(range(5)),'Source clarification: linoleic acid and alpha-linolenic acid are the essential dietary fatty acids; arachidonic acid is not universally essential because it can be made from linoleic acid. Historical marking examples follow; the medical-outcome statements are not guarantees of prevention or treatment. '+body(13,'3 points @ 4 marks (graded 4:3:2:1:0)','(d)'))
 points(1,'d',10,5,[0,1,2],body(13,'5 points @ 2 marks (graded 2:1:0)','(e)'))
 points(1,'e',20,4,[0,3,5],body(13,'4 points @ 5 marks (graded 5:3:0)'))
 table=d['scheme'][14].find_tables().tables[0].extract();assert len(table)==6 and all(len(row)==5 for row in table)
 variants=[]
 for i,raw in enumerate(table[1:]):
  name,source,foods,growth,symptoms=[tidy(v) for v in raw];growth=re.sub(r'(\d)oC',r'\1°C',growth)
  caution=' Source correction: growth does not occur below pH 4.6; the printed pH 4–6 range is imprecise.' if name=='Clostridium botulinum' else ''
  variants.append(dict(id=str(i),label=name,rows=[criterion('name','Name of bacteria',1,[0,1,2],'Identify the chosen bacterium, graded 2:1:0. '+name),criterion('source','Source',1,[0,1,2],'One source for the SAME bacterium, graded 2:1:0. '+source),criterion('foods','High-risk foods',2,[0,1,2],'Two foods for the SAME bacterium, each graded 2:1:0. '+foods),criterion('growth','Factors affecting growth',3,[0,1,2],'Three factors for the SAME bacterium, each graded 2:1:0.'+caution+' Original scheme wording: '+growth),criterion('symptoms','Food-poisoning symptoms',2,[0,1,2],'Two symptoms for the SAME bacterium, each graded 2:1:0. '+symptoms)]))
 assert [v['label'] for v in variants]==['Salmonella','Listeria','E. coli','Clostridium botulinum','Staphylococcus aureus']
 other=deepcopy(variants[0]['rows'])
 for row in other:row['contextNote']='Use this criterion for the same chosen bacterium; each point is graded 2:1:0. The scheme also names Clostridium perfringens and Campylobacter but supplies no model cells for them.'
 variants.append(dict(id='another',label='Another valid bacterium',rows=other))
 put(3,'a',18,'Name 2 + source 2 + foods 2 × 2 + growth 3 × 2 + symptoms 2 × 2 (2:1:0)',deepcopy(variants[0]['rows']),answerVariants=variants,figureKey='home-economics-2025-hl-sb-q3a-scheme-table',labelKey=[])
 storage,cooking=named_sections(body(16,'1 point to refer to storage; 1 point to refer to cooking/reheating and 2 others','(c)'),['Storage','Cooking/reheating'])
 put(3,'b',20,'Storage 1 + cooking/reheating 1 + other 2, each 5 (5:3:0)',[criterion('storage','Storage',1,[0,3,5],'One storage point, graded 5:3:0. Source clarification: thawed food may be frozen after thorough cooking; the printed never-refreeze rule omits that distinction. Historical wording: '+storage),criterion('cooking','Cooking/reheating',1,[0,3,5],'One cooking/reheating point, graded 5:3:0. Source correction: FSAI recommends reheating to at least 70°C at the core; the scheme’s above-100°C statement is not the core-temperature target. Original wording: '+cooking),criterion('other','points',2,[0,3,5],'Two further distinct points under either heading, each graded 5:3:0. Do not count the same point twice.')])
 points(3,'c',12,3,[0,2,4],body(16,'3 points @ 4 marks (graded 4:2:0)'))
 names=['Choosing','Using','Disposing'];values=named_sections(body(17,'1 point on each and 1 other','(b)'),names)
 put(4,'a',16,'Choosing 1 + using 1 + disposing 1 + other 1, each 4 (4:2:0)',[criterion(str(i),name,1,[0,2,4],'One point under this required heading, graded 4:2:0. '+v) for i,(name,v) in enumerate(zip(names,values))]+[criterion('other','point',1,[0,2,4],'One further point under any heading, graded 4:2:0.')])
 principle=body(17,'Credit points in bold + 2 other points','• modern features.');features=body(17,'3 points @ 2 marks (graded 2:1:0)','(c)')
 required=['a motor is attached to a compressor which forces a gaseous refrigerant','in the condenser, the refrigerant cools and converts to a liquid','liquid refrigerant passes into the evaporator where it changes to a gas']
 assert all(t in principle for t in required)
 rows=[criterion('name','name of refrigeration appliance',1,[0,1],'Name the refrigeration appliance studied: 1 mark.')]
 rows += [criterion(f'principle-{i}',name,1,[0,1,2,3],'Required bold component in the printed scheme, graded 3:2:1:0. '+text) for i,(name,text) in enumerate(zip(['Compressor','Condenser','Evaporator'],required))]
 rows += [criterion('other','other points',2,[0,1,2,3],'Two other distinct points, each graded 3:2:1:0. Credit a clearly labelled diagram. Complete historical account: '+principle),criterion('features','Modern features',3,[0,1,2],'Three features of the SAME appliance, each graded 2:1:0. '+features)]
 put(4,'b',22,'Name 1 + working principle 5 × 3 (3:2:1:0) + features 3 × 2 (2:1:0)',rows,suffix='-principle')
 points(4,'c',12,3,[0,2,4],'Answer about the Act named in this historical examination. '+body(17,'3 points @ 4 marks (graded 4:2:0)'))
 points(5,'a',20,4,[0,3,5],'Interpret “present day” in the 2025 examination context. '+body(18,'4 points @ 5 marks (graded 5:3:0)','(b)'))
 points(5,'b',18,3,list(range(7)),'Each of the three responses must pair a family function with a related State support; the 6-mark ladder judges the pair as a whole. '+body(18,'3 functions and related state support @ 6 marks (graded 6:5:4:3:2:1:0)','(c)'))
 points(5,'c',12,3,[0,2,4],body(18,'3 points @ 4 marks (graded 4:2:0)'))
 for cid,target in ALIASES.items():fixes[cid]=dict(drop=True,replacementId=target,reason='Required headings belong to one whole printed task; progress is preserved by CARD_ID_ALIASES.')
 live=[f for f in fixes.values() if not f.get('drop')];assert len(live)==14 and sum(f['set']['totalMarks'] for f in live)==230
 return fixes,[]


def write():
 fixes,added=build();save_batch('B-rest',fixes,added,dict(tasks=14,marks=230,sourceClarifications=CLARIFICATIONS,selectionDecisions='B1(b) is one required three-acid profile; B4(b) one required appliance study. Three withdrawn identities have direct progress aliases. Four sources from the eight-category chart remain one choice task. B3(a) remains one chosen bacterium with five complete source models and an open alternative. B5(b) keeps each function/support pair on its single printed six-mark ladder.',checked='2026-11-06'));print('2025 Higher B complete: 18 tasks, 280 offered marks; three required-heading cards consolidated with aliases.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
