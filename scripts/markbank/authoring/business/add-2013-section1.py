from abq_authoring import response, notes
from pathlib import Path
import json,hashlib
path=Path('components/MarkBank/cards/business/rubric-authored.json')
data=json.loads(path.read_text());created=[];reviews=[]
sources={kind:dict(fileid='LC033ALP000EV.pdf',sha256=hashlib.sha256(Path(f'paper-trail-corpus/{kind}/2013/LC033ALP000EV.pdf').read_bytes()).hexdigest()) for kind in ['exampapers','markingschemes']}

def add(q,suffix,prompt,total,topic,concept,page,support,requirement,responses,guidance=None):
 ref=f'Q{q}'+(f'({suffix})' if suffix else '')
 card=dict(id=f'bus-2013-hl-s1-q{q}{suffix}',year=2013,level='higher',section='1',paperFileid='LC033ALP000EV',paperPages=[page],sourceLabel='QUESTION PAPER',sourceTitle=f'2013 Business · Section 1 Question {q}',questionRef=f'2013 HL Section 1 {ref}',questionText=prompt,totalMarks=total,topicId=topic,conceptId=concept,rubric=dict(system='business',taskRequirements=[requirement],guidance=guidance or [],responses=responses,schemeFileid='LC033ALP000EV',schemePages=[5]+support,markingGuideNote=notes))
 assert sum(a['maxMarks'] for r in responses for a in r['allocations'])==total
 created.append(card)

def cumulative(answers):
 r=response(1,'Correct answers',[('correct','Total from the published 3 + 3 + 2 + 1 + 1 sequence',10)])
 r['allocations'][0]['permittedMarks']=[0,3,6,8,9,10]
 return [r]

add(1,'','Outline two characteristics of a private limited company.',10,'business-5-14','private-limited-company',2,[11],'Outline two distinct characteristics. The published allocation is 6 + 4 marks.',[response(1,'Characteristic 1',[('outline','Outline',6)]),response(2,'Characteristic 2',[('outline','Outline',4)])],['Use the historical company-law context of the 2013 paper.'])
add(2,'a','What do the letters NCA stand for?',4,'business-0-13','national-consumer-agency',2,[11],'The name carries 4 marks.',[response(1,'NCA',[('name','National Consumer Agency',4)])],['This question uses the consumer body named in the 2013 paper.'])
add(2,'b','Outline two functions of the NCA (National Consumer Agency).',6,'business-0-13','national-consumer-agency-functions',2,[11],'Outline two functions at 3 marks each (2 + 1).',[response(i,f'Function {i}',[('name','Function',2),('develop','Development',1)]) for i in [1,2]],['The acronym is expanded so that this task can be practised independently of Part (a). Apply the agency’s role at the time of the 2013 examination.'])
add(3,'a','Using the figures for Sentry Ltd in the question paper, calculate its Current Ratio. Show your workings.',7,'business-3-19','current-ratio',2,[11],'The scheme awards seven individual marks: the formula, five correctly classified figures and the final ratio.',[response(1,'Current Ratio',[('formula','Current Assets : Current Liabilities',1),('debtors','Current assets include debtors €12,000',1),('cash','Current assets include cash €15,000',1),('stock','Current assets include closing stock €8,000',1),('overdraft','Current liabilities include bank overdraft €20,000',1),('creditors','Current liabilities include creditors €50,000',1),('ratio','€35,000 : €70,000 = 0.5 : 1',1)])])
add(3,'b','Sentry Ltd has a Current Ratio of 0.5 : 1. Comment on the liquidity position of Sentry Ltd.',3,'business-3-19','liquidity-interpretation',2,[12],'Comment on the liquidity position for 3 marks (2 + 1).',[response(1,'Liquidity position',[('comment','Comment',2),('develop','Development',1)])],['The ratio from Part (a) is supplied so this interpretation can be practised independently. The scheme contrasts €0.50 of current assets per €1 of current liabilities with its recommended 2 : 1 ratio.'])
add(4,'','Write True or False after each statement:\n1. Batch Production is used when making a single, one off, unique product.\n2. In a Hire Purchase agreement legal ownership of the good transfers to the buyer when the first installment is made.\n3. A Cash Flow deficit can be addressed by negotiating a shorter period of credit with debtors.\n4. A sole trader is an ownership structure that benefits from limited liability.\n5. When a company’s equity capital is greater than its debt capital it has low gearing.',10,'business-3-16','business-true-false',3,[12],'Answer all five statements. Apply the published 3 + 3 + 2 + 1 + 1 sequence across correct answers.',cumulative(None),['Answers in printed order: False; False; True; False; True.','For 0, 1, 2, 3, 4 or 5 correct answers, record 0, 3, 6, 8, 9 or 10 marks respectively. The shared sequence is not a fixed mark value assigned to each statement.'])
add(5,'','Outline two implications for management when a company develops its own website.',10,'business-2-12','management-implications-of-a-website',3,[12],'Outline two distinct implications. The published allocation is 6 + 4 marks.',[response(1,'Implication 1',[('outline','Outline',6)]),response(2,'Implication 2',[('outline','Outline',4)])])
add(6,'','In break-even analysis a distinction is made between ‘Fixed Costs’ and ‘Variable Costs’. Explain these terms, and give one example in each case.',10,'business-3-19','fixed-and-variable-costs',3,[13],'Cover both required terms with an example for each. Each term carries 5 marks, printed as 3 + 2 (1 + 1).',[response(i,label,[('first','First component',3),('second','Second component',1),('third','Third component',1)]) for i,label in enumerate(['Fixed costs','Variable costs'],1)],['The scheme reproduces the nested component split without naming the components. Consult the official explanation and examples when assessing each term.'])
add(7,'','Explain the term ‘Constructive Dismissal’.',10,'business-0-14','constructive-dismissal',3,[13],'Explain the term using the published 6 + 4 allocation.',[response(1,'Constructive dismissal',[('explain','Explanation',6),('develop','Development',4)])],['Use the historical employment-law context of this examination.'])
add(8,'','Match each economic term to its correct explanation in the question-paper table. Write the letter under the relevant number: 1. Exchange Rate; 2. Interest Rate; 3. Taxation; 4. Economic Growth; 5. Inflation. One explanation does not refer to any of these terms.',10,'business-5-15','economic-terms-matching',4,[13],'Match all five terms to the supplied explanations. Apply the published 3 + 3 + 2 + 1 + 1 sequence across correct matches.',cumulative(None),['Answers in printed order: 1–E; 2–F; 3–D; 4–A; 5–B. Explanation C is unused.','For 0, 1, 2, 3, 4 or 5 correct matches, record 0, 3, 6, 8, 9 or 10 marks respectively. The task is one matching exercise, not a choice of questions.'])
add(9,'','Distinguish between a ‘Directive’ and a ‘Regulation’ as legislative instruments within the EU.',10,'business-6-14','eu-directives-and-regulations',4,[13],'Distinguish both legislative instruments. The published allocation is 4 + 4 + 2 marks.',[response(1,'Directive and Regulation',[('first','First component',4),('second','Second component',4),('third','Third component',2)])],['The summary does not name the three components. Compare your distinction with both explanations in the official support notes.'])
add(10,'','Outline two possible implications for a business if a manager adopts McGregor’s Theory X approach to managing.',10,'business-2-11','theory-x-implications',4,[14],'Outline two implications at 5 marks each (3 + 2).',[response(i,f'Implication {i}',[('explain','Explanation',3),('develop','Development',2)]) for i in [1,2]])
next(c for c in created if c['id']=='bus-2013-hl-s1-q4')['additionalTopicIds']=['business-4-15','business-5-14','business-3-19']
assert len(created)==12
ids={c['id'] for c in created};data['cards']=[c for c in data['cards'] if c['id'] not in ids]+created
data['reviews']=[r for r in data['reviews'] if not(r['year']==2013 and r['section']=='1')]
for q in range(1,11):
 cohort=[c for c in created if c['questionRef'].split(' Q')[1].split('(')[0]==str(q)]
 selection='Characteristics, functions, implications and illustrations are open examples. Required definitions and all true/false or matching responses remain together; there is no finite optional task pool.'
 clarification=['All ten numbered short questions remain available; the instruction to answer eight governs the exam sitting only.']
 if q in [4,8]:clarification.append('The shared 3+3+2+1+1 sequence rewards successive correct responses. Keep all five rows together; do not assign the larger rewards to particular printed rows or expand distractor choices into alternative tasks.')
 if q==3:clarification.append('A splits at 7 marks and B at 3. The calculated ratio is carried into the independent interpretation task.')
 data['reviews'].append(dict(status='partial-subject-review',year=2013,level='higher',section='1',question=str(q),cardIds=[c['id'] for c in cohort],sources=sources,paperPagesReviewed=cohort[0]['paperPages'],schemePagesReviewed=sorted({p for c in cohort for p in c['rubric']['schemePages']}),boundaries={c['questionRef'].split(' Q')[1]:c['totalMarks'] for c in cohort},selectionAnalysis=selection,sourceClarifications=clarification))
data['cards'].sort(key=lambda c:(c['year'],c['section'],c['id']));data['reviews'].sort(key=lambda r:(r['year'],r['section'],r['question']))
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
path=Path('data/examTopics/business-source-reviewed-topics.json');data=json.loads(path.read_text())
data['questions']=[r for r in data['questions'] if not(r['year']==2013 and r['n'] in {str(i) for i in range(1,11)})]
for q in range(1,11):
 cohort=[c for c in created if c['questionRef'].split(' Q')[1].split('(')[0]==str(q)]
 topics=list(dict.fromkeys(c['topicId'] for c in cohort))
 if q==4:topics=['business-4-15','business-3-16','business-5-14','business-3-19']
 data['questions'].append(dict(year=2013,level='higher',paperKey='single',n=str(q),canonicalNodeIds=topics,reason=f'2013 Higher Section 1 Question {q}, visually checked against PDF paper page {cohort[0]["paperPages"][0]} and the scheme. This is the numbered short question; Section 3 uses the distinct S3Q identity.'))
data['questions'].sort(key=lambda r:(r['year'],str(r['n'])));path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
path=Path('scripts/markbank/authored/business-selection-reviews.json');data=json.loads(path.read_text())
inventory=json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
doc=next(d for d in inventory['documents'] if d['year']==2013 and d['level']=='higher' and d['language']=='ev')
for directive in doc['selectionDirectives']:
 if directive['id'] in data['reviews']:continue
 if directive['matchedText'].endswith(' of'):
  reason='This is the printed page counter (Page N of 12), visually checked on the source page. It is pagination, not a candidate answer choice.'
 else:
  assert directive['matchedText'] in ['either','Answer eight']
  reason='This specifies the choice of whole examination questions across sections. Each question is retained for independent practice; it does not create combinations within a marked task.'
 data['reviews'][directive['id']]=dict(wording=directive['wording'],paperSha256=directive['paperSha256'],classification='exam-navigation',reason=reason)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Authored {len(created)} Section 1 tasks and classified all 2013 English Higher selection directives.')
