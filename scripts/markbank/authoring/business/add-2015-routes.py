from abq_authoring import response,notes
from pathlib import Path
import json,hashlib,fitz,re
sources={kind:dict(fileid='LC033ALP000EV.pdf',sha256=hashlib.sha256(Path(f'paper-trail-corpus/{kind}/2015/LC033ALP000EV.pdf').read_bytes()).hexdigest()) for kind in ['exampapers','markingschemes']}
paper=fitz.open('paper-trail-corpus/exampapers/2015/LC033ALP000EV.pdf')
text=re.sub(r'\s+',' ',paper[7].get_text())
def source(start,end):return text[text.index(start):text.index(end,text.index(start))].strip()
def pool(q,part,choose,options,total,support,prompt,sourceword,requirements,guidance,concept):
 tariff=9 if q==4 else 10
 return dict(id=f'bus-2015-hl-s3-q{q}{part}',choose=choose,sourceWording=sourceword,routePrompt=prompt,options=options,review=dict(status='partial-subject-review',year=2015,level='higher',section='3',question=f'{q}({part[0].upper()})({part.split("-")[1]})',sources=sources,paperPagesReviewed=[8],schemePagesReviewed=[tariff]+support,boundaries={part:total},selectionAnalysis=f'The printed task requires {choose} of {len(options)} named options. Every unordered selection is generated mechanically; each alternative retains {total} marks.',sourceClarifications=guidance),template=dict(year=2015,level='higher',section='3',paperFileid='LC033ALP000EV',paperPages=[8],sourceLabel='QUESTION PAPER',sourceTitle=f'2015 Business · Question {q}',questionRef=f'2015 HL Section 3 Q{q}({part[0].upper()})({part.split("-")[1]})',totalMarks=total,conceptId=concept,rubric=dict(system='business',taskRequirements=requirements,guidance=guidance,schemeFileid='LC033ALP000EV',schemePages=[tariff]+support,markingGuideNote=notes)))
points=[('july','July: €50,000',1),('august','August: €60,000',1),('september','September: €40,000',1),('october','October: €30,000',1),('november','November: €20,000',1),('december','December: €10,000',1),('title','Chart title',2),('x-axis','X axis: months',2),('y-axis','Y axis: sales in €',2)]
graphs=[dict(id=id,label=label,topicId='business-2-12',response=dict(allocations=response(1,label,points)['allocations'])) for id,label in [('bar-chart','Bar chart'),('line-graph','Line graph')]]
p4=pool(4,'a-i',1,graphs,12,[34],'Use Water Solutions Ltd’s six-month projected sales data in the question paper. Illustrate the data in the following form:',source('Illustrate the above data','(ii) Outline the principles'),['Draw the named representation. Award 1 mark for each of six correct bars or points, 2 for the title and 2 for each axis.'],['The paper explicitly offers a bar chart or a line graph. Each route retains the same six figures, source table and 12-mark allocation. The remaining 13 marks in Part (A) belong to the separate communication-principles task.'],'sales-data-graph')
p4['template']['rubric']['markingGuideNote']='Compare your graph with the official graph and published allocations. Use all six months and label the axes and title.'
stages=[dict(id=id,label=label,topicId='business-4-15',response=dict(allocations=response(1,label,[('explain','Explanation',2),('develop','Development',3)])['allocations'])) for id,label in [('feasibility-study','Feasibility Study'),('test-marketing','Test Marketing'),('product-screening','Product Screening'),('prototype-development','Prototype Development')]]
p5=pool(5,'b-ii',3,stages,15,[39,40],'Outline your understanding of the following three stages in the new Product Development Process:',source('Feasibility Study, Test Marketing','(20 marks)'),['Outline all three named stages at 5 marks each (2 + 3).'],['The printed menu contains four stages and asks for any three: all four unordered triples are required. The separate 5-mark ordering task remains a single card containing all four stages.'],'product-development-stages')
path=Path('components/MarkBank/cards/business/route-pools.json');d=json.loads(path.read_text());ids={p4['id'],p5['id']};d['pools']=[p for p in d['pools'] if p['id'] not in ids]+[p4,p5];path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# Classify newly caught lowercase alternatives in the previously reviewed years,
# then every raw directive in the visually reviewed 2015 paper.
path=Path('scripts/markbank/authored/business-selection-reviews.json');d=json.loads(path.read_text())
for year in [2013,2014,2015]:
 for item in json.loads((Path(__file__).resolve().parent / 'directives' / f'{year}-directives.json').read_text()):
  if item['id'] in d['reviews']:continue
  t=item['matchedText'];w=item['wording'];poolid=None
  if t.endswith(' of') and w.startswith('Page '):
   category='exam-navigation';reason='Printed page counter, not an answer choice. Every page of this paper, including its blank pages, has been visually reviewed.'
  elif t=='any three' and year==2015:
   category='finite-pool';reason='Section 3 Q5(B)(ii) asks for three of the four stages printed immediately above. All four unordered triples retain 15 marks.';poolid=p5['id']
  elif t=='or' and 'bar chart or a line graph' in w:
   category='finite-pool';reason='Section 3 Q4(A)(i) explicitly offers two representations. Generate a 12-mark bar-chart card and a 12-mark line-graph card, both with the same sales table.';poolid=p4['id']
  elif t=='or' and 'True or False' in w:
   category='required-headings';reason='True/False are answer labels for every required statement, not optional tasks. Retain all five statements in one exercise with its shared cumulative tariff.'
  elif t=='or' and any(s in w for s in ['progressive or regressive','sample or','products or services']):
   category='case-context';reason='The alternative is wording inside a matching-table explanation. Every printed business term must still be matched; it does not offer optional examination tasks.'
  elif t=='choose' and 'MNCs' in w:
   category='case-context';reason='The verb describes the location decision of multinational companies. Candidates discuss reasons; no closed task menu is printed.'
  else:
   assert t in ['either','or','Answer eight','Answer Four'],item
   assert t!='or' or 'either Part 1 or Part 2' in w,item
   category='exam-navigation';reason='This selects whole questions for an examination sitting. All numbered questions remain separately available for practice, without combined sitting variants.'
  r=dict(wording=w,paperSha256=item['paperSha256'],classification=category,reason=reason)
  if poolid:r['poolId']=poolid
  d['reviews'][item['id']]=r
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Added six route variants and reviewed all new raw matches for 2013–2015 English Higher.')
