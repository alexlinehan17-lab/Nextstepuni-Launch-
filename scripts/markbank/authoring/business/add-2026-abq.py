import json, hashlib
from pathlib import Path
p=Path('components/MarkBank/cards/business/rubric-authored.json')
d=json.loads(p.read_text())
old=d.pop('review',None)
if old:
 old.update(year=2025,level='higher',section='2',question='ABQ')
 d['reviews']=[old]
d['schemaVersion']=2
# The 2026 Higher ABQ only (written when it was the only 2026 Business source).
d['cards']=[c for c in d['cards'] if not (c['year']==2026 and c['level']=='higher' and c['section']=='2')]
d['reviews']=[r for r in d['reviews'] if not (r['year']==2026 and r['level']=='higher' and r['section']=='2')]
for c in d['cards']:
 for r in c['rubric']['responses']: r['label']=r['label'].replace('Hrm','HRM')
 if c['totalMarks']==2: c['rubric']['taskRequirements']=['The scheme awards 2 marks for one recommendation.']
base=dict(year=2026,level='higher',section='2',paperFileid='LC033ALP041EV',paperPages=[2],sourceTitle='Coffee & Chill Ltd.')
linknote='Use a separate relevant quotation, phrase or statement from the case study for each point. No link is awarded without relevant theory.'
noten=d['cards'][0]['rubric']['markingGuideNote']
def response(i,label,parts):
 allocations=[dict(id=k,label=l,maxMarks=m,permittedMarks=list(range(m+1))) for k,l,m in parts]
 for a in allocations:
  if a['id']=='link': a['requiresAnyOf']=[b['id'] for b in allocations if b['id'] in ['name','explain']]
 return dict(id=f'response-{i}',label=label,allocations=allocations)
def add(suffix,prompt,marks,topic,concept,requirements,responses,pages,guidance=None):
 part=''.join(f'({v.upper() if i==0 else v})' for i,v in enumerate(suffix.split('-')))
 d['cards'].append(dict(**base,id=f'bus-2026-hl-s2-abq-{suffix}',questionRef=f'2026 HL Section 2 ABQ{part}',questionText=prompt,totalMarks=marks,topicId=topic,conceptId=concept,rubric=dict(system='business',taskRequirements=requirements,guidance=guidance if guidance is not None else [linknote],responses=responses,schemeFileid='LC033ALP000EV',schemePages=[6]+pages,markingGuideNote=noten)))
add('a','Explain how Martina rewards her employees. Refer to the text in your answer.',20,'business-3-20','employee-rewards',['Apply the 15-mark allocation to your stronger reward response and the 5-mark allocation to a different reward.'],[
 response(1,'Reward response · 15 marks',[('name','Reward',8),('explain','Explain',2),('link','Link',5)]),
 response(2,'Reward response · 5 marks',[('name','Reward',2),('explain','Explain',1),('link','Link',2)])],[22,23])
add('b-i','Explain price discrimination. Refer to the text in your answer.',6,'business-4-17','price-discrimination',['The scheme awards 5 marks for the explanation and 1 mark for the case-study link.'],[response(1,'Price discrimination',[('explain','Explain',5),('link','Link',1)])],[23])
add('b-ii','Describe the other pricing strategies used by Martina. Refer to the text in your answer.',24,'business-4-17','pricing-strategies',['Describe two pricing strategies other than price discrimination. The scheme awards 12 marks for each.'],[response(i,f'Pricing strategy {i}',[('name','Strategy',6),('explain','Explain',2),('link','Link',4)]) for i in [1,2]],[24])
add('c-i','Evaluate the management control techniques used by Martina in Coffee & Chill Ltd. Refer to the text in your answer.',24,'business-2-13','management-control-effectiveness',['The scheme awards 3 responses at 8 marks each, including an evaluation for each control.'],[response(i,f'Management control {i}',[('name','Control',2),('explain','Explain',2),('link','Link',2),('evaluate','Evaluate',2)]) for i in [1,2,3]],[25,26])
add('c-ii','Recommend and explain an alternative sales promotion technique Martina can use instead of giving away free t-shirts.',6,'business-4-17','sales-promotion',['The scheme awards 3 marks for the recommendation and 3 for its explanation.'],[response(1,'Alternative sales promotion',[('recommend','Recommendation',3),('explain','Explanation',3)])],[27],[])
d['reviews'].append(dict(status='partial-subject-review',year=2026,level='higher',section='2',question='ABQ',sources={kind:dict(fileid=fileid,sha256=hashlib.sha256(Path(f'paper-trail-corpus/{kind}/2026/{fileid}').read_bytes()).hexdigest()) for kind,fileid in [('exampapers','LC033ALP041EV.pdf'),('markingschemes','LC033ALP000EV.pdf')]},paperPagesReviewed=[2],schemePagesReviewed=[6,22,23,24,25,26,27],boundaries={'A':20,'B(i)':6,'B(ii)':24,'C(i)':24,'C(ii)':6},selectionAnalysis='No finite answer menu is printed in these tasks. Reward methods, pricing strategies and promotional suggestions in the support notes are open examples, not required option pools. B(ii) excludes price discrimination, whose independent B(i) response remains attached to the same case study. Five tasks follow the separately published scheme allocations.',sourceClarifications=['The tariff overview on PDF page 6 repeats Explain in B(i); the detailed B(i) row on PDF page 23 unambiguously allocates Explain 5 + Link 1.','The two reward responses have unequal 15/5 allocations. They stay together as one 20-mark task because the paper does not assign a fixed reward to either allocation.']))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
