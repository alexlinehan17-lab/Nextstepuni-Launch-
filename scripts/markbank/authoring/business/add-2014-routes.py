from abq_authoring import response,notes
from pathlib import Path
import json,hashlib,fitz,re
sources={kind:dict(fileid='LC033ALP000EV.pdf',sha256=hashlib.sha256(Path(f'paper-trail-corpus/{kind}/2014/LC033ALP000EV.pdf').read_bytes()).hexdigest()) for kind in ['exampapers','markingschemes']}
paper=fitz.open('paper-trail-corpus/exampapers/2014/LC033ALP000EV.pdf')
def wording(page,start):
 t=re.sub(r'\s+',' ',paper[page-1].get_text())
 return t[t.index(start):].split('(20 marks)')[0].strip()
def components(*marks):return [(f'component-{i}',f'Component {i}',m) for i,m in enumerate(marks,1)]
def pool(q,choose,options,page,support,prompt,sourceword,requirements,guidance,clarifications,ordered=None):
 p=dict(id=f'bus-2014-hl-s3-q{q}c',choose=choose,sourceWording=sourceword,routePrompt=prompt,options=options,review=dict(status='partial-subject-review',year=2014,level='higher',section='3',question=f'{q}(C)',sources=sources,paperPagesReviewed=[page],schemePagesReviewed=[7 if q==1 else 8]+support,boundaries={f'{q}(C)':20},selectionAnalysis=f'The printed task requires {choose} of {len(options)} named options. Generate every unordered combination mechanically; each alternative retains the published 20 marks.',sourceClarifications=clarifications),template=dict(year=2014,level='higher',section='3',paperFileid='LC033ALP000EV',paperPages=[page],sourceLabel='QUESTION PAPER',sourceTitle=f'2014 Business · Question {q}(C)',questionRef=f'2014 HL Section 3 Q{q}(C)',totalMarks=20,conceptId='consumer-rights-under-1980-act' if q==1 else 'impact-of-eu-policies',rubric=dict(system='business',taskRequirements=requirements,guidance=guidance,schemeFileid='LC033ALP000EV',schemePages=[7 if q==1 else 8]+support,markingGuideNote=notes)))
 if ordered:p['orderedResponses']=ordered
 return p
rights=[dict(id=id,label=label,topicId='business-0-13') for id,label in [('merchantable-quality','(i) Merchantable Quality'),('guarantees','(ii) Guarantees'),('limiting-signs','(iii) Signs limiting consumer rights'),('unsolicited-goods','(iv) Unsolicited Goods')]]
p1=pool(1,3,rights,6,[22],'Outline a consumer’s legal rights under the terms of the Sale of Goods and Supply of Services Act 1980, with reference to the following three headings:',wording(6,'Outline a consumer’s'),['Cover all three named headings. The response allowances are 7, 7 and 6 marks, printed as 7 (4 (2 + 2) + 3), 7 (4 + 3) and 6 (4 + 2).'],['Apply the 7/7/6 allowance across your three distinct responses. The unequal allowances are not fixed marks belonging to particular named headings.','Use the historical Act specified in the examination. Consult the official notes for the consumer rights under each selected heading.'],['The paper’s four named consumer-rights headings give four choose-three combinations.','An unequal response sequence is kept separately from the option order. Do not attach a permanent 7- or 6-mark value to a particular consumer right.'],[response(1,'Selected heading response 1',components(2,2,3)),response(2,'Selected heading response 2',components(4,3)),response(3,'Selected heading response 3',components(4,2))])
policies=[dict(id=id,label=label,topicId='business-6-14',response=dict(allocations=response(1,'policy',[('policy','Policy statement',4),('impact','Impact on Irish business',4),('evaluation','Evaluation',2)])['allocations'])) for id,label in [('emu','(i) European Monetary Union (EMU)'),('competition','(ii) European Union Competition Policy'),('social-charter','(iii) European Social Charter')]]
p3=pool(3,2,policies,7,[27,28],'Evaluate the impact that the following two EU policies have on Irish businesses:',wording(7,'Evaluate the impact'),['Evaluate both named policies. Each carries 10 marks: policy statement 4, impact 4 and evaluation 2.'],['An evaluation is required for each policy. Use the context of the 2014 examination.'],['The paper names European Monetary Union (EMU); the support notes expand that heading to European Economic and Monetary Union. The route prompt preserves the paper’s wording.'])
path=Path('components/MarkBank/cards/business/route-pools.json');d=json.loads(path.read_text());ids={p1['id'],p3['id']};d['pools']=[p for p in d['pools'] if p['id'] not in ids]+[p1,p3];path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
path=Path('scripts/markbank/authored/business-selection-reviews.json');d=json.loads(path.read_text())
inv=json.loads(Path('scripts/markbank/authored/business-corpus-inventory.json').read_text())
doc=next(x for x in inv['documents'] if x['year']==2014 and x['level']=='higher' and x['language']=='ev')
for item in doc['selectionDirectives']:
 if item['id'] in d['reviews']:continue  # re-runs keep the reviewed record
 t=item['matchedText'];w=item['wording'];pool_id=None
 if t.endswith(' of') and w.startswith('Page '):
  classification='exam-navigation';reason='This is the printed page counter, not an answer choice. The paper has nine numbered pages and three further blank PDF pages; all were visually checked.'
 elif t=='any three':
  classification='finite-pool';reason='Section 3 Q1(C) requires three of four named consumer-rights headings: all four unordered triples are required.';pool_id=p1['id']
 elif t=='any two' and 'EU policies' in w:
  classification='finite-pool';reason='Section 3 Q3(C) requires two of three named EU policies: all three unordered pairs are required.';pool_id=p3['id']
 elif t=='any two' and 'Interest Groups' in w:
  classification='open-response';reason='The candidate may select any two interest groups; the printed paper supplies no finite list. The scheme’s examples do not create a closed menu.'
 elif t=='choose':
  classification='case-context';reason='The phrase describes a prospective business owner choosing a franchise model. It is the subject of the question, not a candidate’s choice of examination task.'
 elif t=='one of':
  classification='case-context';reason='The matching-table explanation describes brainstorming as a method of idea generation. It offers no optional task route; all five terms must be matched.'
 else:
  assert t in ['either','Answer eight','Answer Four'],item
  classification='exam-navigation';reason='The instruction selects whole questions for the examination sitting. All numbered questions remain available individually for practice; no combined examination-answer cards are created.'
 r=dict(wording=w,paperSha256=item['paperSha256'],classification=classification,reason=reason)
 if pool_id:r['poolId']=pool_id
 d['reviews'][item['id']]=r
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Added two source-pinned pools and reviewed all 18 raw directives in the 2014 English Higher paper.')
