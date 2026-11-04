import json,hashlib
from pathlib import Path
p=Path('components/MarkBank/cards/business/rubric-authored.json')
d=json.loads(p.read_text())
original={c['id']:c for c in json.load(open('scripts/markbank/authored/business.json'))}
linknote='Use a separate relevant quotation, phrase or statement from the case study for each point. No link is awarded without relevant theory.'
notes='The official support notes give possible responses, not an exhaustive list. Other relevant answers are considered on their merits. Apply the published allocation to your answer; do not count the same point twice.'
def response(i,label,parts):
 a=[dict(id=k,label=l,maxMarks=m,permittedMarks=list(range(m+1))) for k,l,m in parts]
 for x in a:
  if x['id']=='link':x['requiresAnyOf']=[y['id'] for y in a if y['id'] in ['name','explain','develop']]
 return dict(id=f'response-{i}',label=label,allocations=a)
def start(year,title,tariff_page,paper_pages=None):
 global yr,source_title,tariff,paper_id,case_pages
 yr=year;source_title=title;tariff=tariff_page
 paper_id="LC033ALP041EV" if year>=2020 else "LC033ALP000EV"
 case_pages=paper_pages or [2]
 # Higher Level ABQ only: an Ordinary paper's Section 2 shares the number.
 d['cards']=[c for c in d['cards'] if not (c['year']==yr and c['level']=='higher' and c['section']=='2')]
 d['reviews']=[r for r in d['reviews'] if not (r['year']==yr and r['level']=='higher' and r['section']=='2')]
def add(suffix,prompt,total,topic,concept,requirements,responses,pages,guidance=None):
 cid=f'bus-{yr}-hl-s2-abq-{suffix}';part=''.join(f'({v.upper() if i==0 else v})' for i,v in enumerate(suffix.split('-')))
 c=dict(id=cid,year=yr,level='higher',section='2',paperFileid=paper_id,paperPages=case_pages,sourceTitle=source_title,questionRef=f'{yr} HL Section 2 ABQ{part}',questionText=prompt,totalMarks=total,topicId=topic,conceptId=concept,rubric=dict(system='business',taskRequirements=requirements,guidance=guidance if guidance is not None else [linknote],responses=responses,schemeFileid='LC033ALP000EV',schemePages=[tariff]+pages,markingGuideNote=notes))
 if cid in original:c['correction']=dict(originalQuestionText=original[cid]['questionText'],originalTotalMarks=original[cid]['totalMarks'],reason=f'Visually verified paper page 2 and scheme PDF pages {",".join(map(str,[tariff]+pages))}: restore the complete printed prompt, use its canonical topic, and replace fixed example ticks with the published response allocations. Retain the existing card ID and total marks.')
 d['cards'].append(c)
def finish(boundaries,pages,analysis,clarifications):
 d['reviews'].append(dict(status='partial-subject-review',year=yr,level='higher',section='2',question='ABQ',sources={kind:dict(fileid=f,sha256=hashlib.sha256(Path(f'paper-trail-corpus/{kind}/{yr}/{f}').read_bytes()).hexdigest()) for kind,f in [('exampapers',paper_id+'.pdf'),('markingschemes','LC033ALP000EV.pdf')]},paperPagesReviewed=case_pages,schemePagesReviewed=[tariff]+pages,boundaries=boundaries,selectionAnalysis=analysis,sourceClarifications=clarifications))
 d['cards'].sort(key=lambda c:(c['year'],c['id']));d['reviews'].sort(key=lambda r:r['year'])
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
