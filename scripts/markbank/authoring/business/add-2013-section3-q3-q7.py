from abq_authoring import response, notes
from pathlib import Path
import json

path=Path('components/MarkBank/cards/business/rubric-authored.json')
data=json.loads(path.read_text())
pending_path=Path('scripts/markbank/authored/business-2013-hl-pending-review.json')
pending=json.loads(pending_path.read_text())
created=[]

def parts(*marks):
 return [(f'component-{i}',f'Component {i}',mark) for i,mark in enumerate(marks,1)]

def points(labels,marks=(2,3)):
 return [response(i,label,[('name','Point',marks[0]),('explain','Development',marks[1])]) for i,label in enumerate(labels,1)]

def add(question,suffix,prompt,total,topic,concept,requirement,responses,guidance=None):
 task=next(t for t in pending['tasks'] if t['question']==str(question))
 part=''.join(f'({v.upper() if i==0 else v})' for i,v in enumerate(suffix.split('-')))
 key=suffix.split('-')[0].upper()+''.join(f'({v})' for v in suffix.split('-')[1:])
 assert task['boundaries'][key]==total
 assert sum(a['maxMarks'] for r in responses for a in r['allocations'])==total
 created.append(dict(id=f'bus-2013-hl-s3-q{question}{suffix}',year=2013,level='higher',section='3',paperFileid='LC033ALP000EV',paperPages=task['paperPages'],sourceLabel='QUESTION PAPER',sourceTitle=f'2013 Business · Question {question}',questionRef=f'2013 HL Section 3 Q{question}{part}',questionText=prompt,totalMarks=total,topicId=topic,conceptId=concept,rubric=dict(system='business',taskRequirements=[requirement],guidance=guidance or [],responses=responses,schemeFileid='LC033ALP000EV',schemePages=[task['tariffPage']]+task['supportPages'][key],markingGuideNote=notes)))

add(3,'a-i','Explain the terms ‘Balance of Trade’ and ‘Balance of Payments’.',10,'business-6-13','balance-of-trade-and-payments','Explain both required terms. Each definition carries 5 marks (3 + 2).',[response(i,label,[('explain','Explanation',3),('develop','Development',2)]) for i,label in enumerate(['Balance of Trade','Balance of Payments'],1)])
add(3,'a-ii','Using the CSO data in the question paper, calculate the Balance of Payments figures for both years.',6,'business-6-13','balance-of-payments-calculation','Calculate both years. The scheme awards 1 mark to each of the six figures.',[response(1,'Quarter 2, 2012',[('trade','Balance of Trade: €10,004m',1),('invisible','Balance of Invisible Trade: −€6,769m',1),('payments','Balance of Payments: €3,235m surplus',1)]),response(2,'Quarter 2, 2011',[('trade','Balance of Trade: €9,660m',1),('invisible','Balance of Invisible Trade: −€9,192m',1),('payments','Balance of Payments: €468m surplus',1)])],['Balance of Payments = Balance of Trade + Balance of Invisible Trade. The bracketed figures in the source table are deficits.'])
add(3,'a-iii','Illustrate what is meant by the term ‘invisible exports’ with reference to the Irish economy.',4,'business-6-13','invisible-exports','Explain and illustrate invisible exports with reference to Ireland. The allocation is 2 + 2 marks.',[response(1,'Invisible exports',[('explain','Explanation',2),('illustration','Irish illustration',2)])])
add(3,'b','Discuss the opportunities and challenges for large indigenous companies, such as Kerry Group plc, in exporting to non EU countries.',20,'business-6-13','exporting-to-non-eu-countries','Discuss two opportunities and two challenges. Each carries 5 marks (2 + 3).',points(['Opportunity 1','Opportunity 2','Challenge 1','Challenge 2']))
add(3,'c','Ireland’s Presidency of the Council of the European Union is an opportunity to play an active part in shaping Europe’s future.\n\nDiscuss the benefits for the Irish economy of on-going membership of the EU.',20,'business-6-14','benefits-of-eu-membership','Discuss four benefits. Each carries 5 marks (2 + 3).',points([f'Benefit {i}' for i in range(1,5)]),['Answer in the context of this 2013 examination.'])

add(4,'a-i','Explain the term ‘intrapreneurship’.',6,'business-1-5','intrapreneurship','The explanation carries 6 marks (4 + 2).',[response(1,'Intrapreneurship',[('explain','Explanation',4),('develop','Development',2)])])
add(4,'a-ii','Outline methods of promoting intrapreneurship in EducaPrint Ltd.',14,'business-1-5','promoting-intrapreneurship','Outline two methods in the context of EducaPrint Ltd. Each carries 7 marks (4 + 2 + 1).',[response(i,f'Method {i}',parts(4,2,1)) for i in [1,2]],['The summary specifies 4 + 2 + 1 without naming the individual components. Use the official support notes when assessing each method, including its relevance to EducaPrint Ltd.'])
add(4,'b','Outline the benefits and challenges for EducaPrint Ltd of a matrix organisation structure (team structure) for the development of the eBook products.',20,'business-2-13','matrix-organisation-structure','Outline two benefits and two challenges. Each carries 5 marks (2 + 3).',points(['Benefit 1','Benefit 2','Challenge 1','Challenge 2']))
add(4,'c','Discuss the importance of the management activity of ‘planning’ for EducaPrint Ltd.',20,'business-2-13','importance-of-planning','Discuss three points. The first two carry 7 marks each (4 + 3); the third carries 6 marks (3 + 3).',[response(i,f'Planning point {i}',[('explain','Explanation',4 if i<3 else 3),('develop','Development',3)]) for i in [1,2,3]])

calc=[response(1,'Gross taxable income',[('gross','Salary €78,000 + benefit-in-kind €2,000 = €80,000',2)]),
 response(2,'PAYE before credits',[('band','Higher-rate band: €80,000 − €32,800 = €47,200',1),('standard','€32,800 × 20% = €6,560',1),('higher','€47,200 × 41% = €19,352 (own figure)',1),('gross','Gross PAYE: €25,912 (own figure)',1)]),
 response(3,'Tax credits and net PAYE',[('single','Single Person Tax Credit: €1,650',1),('paye','PAYE Tax Credit: €1,650',1),('rent','Rent Tax Credit: €320',1),('net','Net tax payable: €22,292 (own figure)',1)]),
 response(4,'Employee PRSI',[('prsi','€80,000 × 4% = €3,200',2)]),
 response(5,'Universal Social Charge',[('first','€10,036 × 2% = €200.72',1),('second','€5,980 × 4% = €239.20',1),('balance','Remaining band: €63,984',1),('higher','€63,984 × 7% = €4,478.88 (own figure)',1),('total','Total USC: €4,918.80 (own figure)',1)]),
 response(6,'Monthly take-home pay',[('divide','Divide annual net pay (€47,589.20) by 12',2),('monthly','Net monthly take-home pay: €3,965.77',1)])]
for r in calc:
 for a in r['allocations']:a['permittedMarks']=[0,a['maxMarks']]
add(5,'a','Using all the salary, benefit-in-kind, tax, USC and PRSI information in the question paper, calculate Audrey Stapleton’s net monthly take-home pay.',20,'business-3-18','net-monthly-pay-calculation','The worked calculation awards fourteen figures at 1 mark and three figures/actions at 2 marks. Use the historical rates and credits supplied in this paper.',calc,['Own-figure allowances are printed for higher-rate PAYE, gross PAYE, net tax payable, higher-rate USC and total USC. Apply these where indicated in the official table.','Total deductions are €30,410.80. Annual cash take-home is €78,000 − €30,410.80 = €47,589.20. The €2,000 benefit-in-kind is taxable but is not cash salary.'])
add(5,'b','Explain the different types of financial and non-financial rewards for employees in a business.',20,'business-3-20','employee-rewards','Explain two financial and two non-financial rewards. Each carries 5 marks (2 + 3).',points(['Financial reward 1','Financial reward 2','Non-financial reward 1','Non-financial reward 2']),['The scheme allows benefits-in-kind as financial or non-financial rewards depending on whether they are subject to tax.'])
add(5,'c-i','Outline two reasons why a household should prepare a cash flow forecast.',10,'business-3-16','household-cash-flow-forecast','Outline two reasons. Each carries 5 marks (2 + 3).',points(['Reason 1','Reason 2']))
add(5,'c-ii','Illustrate how a household can overcome cash flow problems.',10,'business-3-16','household-cash-flow-problems','Illustrate two solutions. Each carries 5 marks (2 + 3).',points(['Solution 1','Solution 2']))

add(6,'a','Outline the internal and external sources of new product ideas for technology companies like Google.',20,'business-4-14','sources-of-product-ideas','Outline two internal and two external sources. Each carries 5 marks (2 + 3).',points(['Internal source 1','Internal source 2','External source 1','External source 2']))
add(6,'b','‘For a business to survive it needs to grow and expand.’\n\nEvaluate two methods of business expansion.',20,'business-4-18','methods-of-business-expansion','Evaluate two methods. Each carries 10 marks (2 + 3 + 3 + 2). Include your own judgement.',[response(i,f'Method {i}',parts(2,3,3,2)) for i in [1,2]],['The summary gives four component allowances without explicitly naming them. Apply the official support notes, including a personal evaluation, to each method. The methods illustrated in the scheme are examples, not a closed answer menu.'])
add(6,'c','Discuss the short-term and long-term implications of business expansion using the following headings:\nOrganisation Structure; Product mix; Profitability; Employment.',20,'business-4-18','implications-of-business-expansion','Cover all four required headings and both short-term and long-term implications. Each heading carries 5 marks (4 + 1).',[response(i,label,parts(4,1)) for i,label in enumerate(['Organisation Structure','Product mix','Profitability','Employment'],1)],['The scheme does not label the 4 + 1 split as short-term versus long-term. Assess the full discussion under each heading using the official support notes.'])

add(7,'a','Outline the market research techniques available to ‘All-Weather Wellies Ltd’ for developing its product range.',20,'business-4-16','market-research-techniques','Outline two techniques. Each carries 10 marks (2 + 3 + 3 + 2).',[response(i,f'Technique {i}',parts(2,3,3,2)) for i in [1,2]],['The support notes discuss desk and field research in the company’s context. The summary gives the four component allowances without explicitly naming them; consult the official notes when marking.'])
add(7,'b-i','Explain the term ‘market segmentation’ with reference to ‘All-Weather Wellies Ltd’.',6,'business-4-16','market-segmentation','Explain market segmentation with reference to the company. The allocation is 6 marks (3 + 2 + 1).',[response(1,'Market segmentation',parts(3,2,1))],['The component allowances are reproduced as printed; the support notes explain segmentation and its application to All-Weather Wellies Ltd.'])
add(7,'b-ii','Discuss the reasons why the marketing department of ‘All-Weather Wellies Ltd’ might engage in market segmentation.',14,'business-4-16','reasons-for-market-segmentation','Discuss two reasons. Each carries 7 marks (4 + 3).',points(['Reason 1','Reason 2'],(4,3)))
add(7,'c','Outline the factors a marketing manager might consider in determining the selling price of products at ‘All-Weather Wellies Ltd’.',20,'business-4-17','price-setting-factors','Outline four factors. Each carries 5 marks (2 + 3).',points([f'Factor {i}' for i in range(1,5)]))

assert len(created)==20
ids={c['id'] for c in created}
data['cards']=[c for c in data['cards'] if c['id'] not in ids]+created
questions={str(i) for i in range(3,8)}
data['reviews']=[r for r in data['reviews'] if not (r['year']==2013 and r['section']=='3' and r['question'] in questions)]
for task in pending['tasks']:
 q=task['question']; cohort=[c for c in created if c['id'].startswith(f'bus-2013-hl-s3-q{q}')]
 data['reviews'].append(dict(status='partial-subject-review',year=2013,level='higher',section='3',question=q,cardIds=[c['id'] for c in cohort],sources=pending['sources'],paperPagesReviewed=task['paperPages'],schemePagesReviewed=[task['tariffPage']]+sorted({p for pages in task['supportPages'].values() for p in pages}),boundaries={q+k:v for k,v in task['boundaries'].items()},selectionAnalysis='Methods, reasons, benefits and illustrations are open examples rather than closed printed pools. '+pending['selectionAnalysis'],sourceClarifications=task['notes']))
data['cards'].sort(key=lambda c:(c['year'],c['section'],c['id']))
data['reviews'].sort(key=lambda r:(r['year'],r['section'],r['question']))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

path=Path('data/examTopics/business-source-reviewed-topics.json')
data=json.loads(path.read_text())
data['questions']=[r for r in data['questions'] if not (r['year']==2013 and r['n'] in {'S3Q'+q for q in questions})]
for q in range(3,8):
 cohort=[c for c in created if c['id'].startswith(f'bus-2013-hl-s3-q{q}')]
 data['questions'].append(dict(year=2013,level='higher',paperKey='single',n=f'S3Q{q}',canonicalNodeIds=list(dict.fromkeys(c['topicId'] for c in cohort)),reason=f'All printed parts and published mark boundaries of 2013 Higher Section 3 Question {q} were visually reviewed against the paper and scheme. Topics follow the assessed tasks retained in rubric-authored.json.'))
data['questions'].sort(key=lambda r:(r['year'],str(r['n'])))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
pending['status']='authored-and-validated'  # validated after authoring (2026-10-11 checkpoint)
pending['authoredCardIds']=sorted(ids)
pending_path.write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n')
print(f'Authored {len(created)} cards; previous cohorts preserved.')
