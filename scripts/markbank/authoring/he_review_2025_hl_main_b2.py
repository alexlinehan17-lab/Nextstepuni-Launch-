#!/usr/bin/env python3
"""2025 Higher B2: paper-authoritative lettering, calcium reference repair and full cheese guidance."""
from copy import deepcopy
import json,sys
from he_review_2025_hl_main import documents,page_text,originals,save_batch,criterion,between,named_sections


def build():
 d=documents();paper=between(page_text(d['bc'],3),'Question 2','Question 3');scheme=page_text(d['scheme'],14);old=originals();fixes={};added=[];stem=paper.split('(a)',1)[0].strip()
 def body(token,end=None):
  assert scheme.count(token)==1,token;t=scheme.split(token,1)[1];assert end is None or end in t,end;return (t.split(end,1)[0] if end else t).strip()
 def value(ref,prompt,marks,notation,rows,**extra):
  return dict(questionRef='2025 HL Section B Q2'+ref,questionText=prompt,stem=stem,totalMarks=marks,tariffModel=dict(kind='fixed',notation=notation),rows=rows,notes='Paper page 3 controls lettering. Scheme page 14 omits the calcium (b) label and mislabels cheese (b). Preserve the existing cheese identity and correct its displayed reference to (c).',**extra)
 assert 'Describe osteoporosis and discuss why a person might be at risk of developing this condition.' in paper
 fixes['he-2025-hl-sb-q2a']=dict(reason='Independently priced osteoporosis description: preserve existing identity at its 6-mark boundary.',set=value('(a) — description','Describe osteoporosis.',6,'2 description points × 3 (3:2:0)',[criterion('description','points described',2,[0,2,3],'Two developed description points, each graded 3:2:0. Complete source guidance: '+body('2 points described @ 3 marks (graded 3:2:0)','4 reasons discussed'))]))
 risk=deepcopy(old['he-2025-hl-sb-q2a']);risk.update(value('(a) — risk factors','Discuss why a person might be at risk of developing this condition (osteoporosis).',12,'4 reasons × 3 (3:2:0)',[criterion('reasons','reasons discussed',4,[0,2,3],'Four distinct reasons, each graded 3:2:0. These are risk factors, not inevitable outcomes or a diagnosis. Complete source wording: '+body('4 reasons discussed @ 3 marks (graded 3:2:0)','Outline the factors'))]),id='he-2025-hl-sb-q2a-risk',conceptId='osteoporosis-risk-factors');added.append(risk)
 prompt=between(paper,'(b)','(15 marks)');calcium=value('(b)',prompt,15,'5 factors × 3 (3:2:1:0)',[criterion('factors','points',5,[0,1,2,3],'Five factors, each graded 3:2:1:0. Source clarification: vitamin D supports active calcium absorption; oxalic/phytic acids can reduce absorption. The source mixes absorption with broader calcium balance; its blanket phosphorus-as-an-aid entry is misleading (NIH notes a small reduction in net absorption). Do not treat this list as supplement instructions. Complete historical guidance: '+body('5 points @ 3 marks (graded 3:2:1:0)','(b) Give a detailed'))],topicId='home-economics-0-8');fixes['he-2025-hl-sb-q2a-calcium']=dict(reason='Existing calcium card was misfiled under (a); preserve its identity and use the paper’s (b) reference.',set=calcium)
 stages,packaging,labelling=named_sections(body('labelling 3 points @ 1 mark (graded 1:0)'),['Stages of production:','Packaging:','Labelling:'])
 fixes['he-2025-hl-sb-q2b']=dict(reason='Existing cheese card is the paper’s part (c), mislettered (b) in the scheme. Preserve identity/progress and restore the complete production guidance.',set=value('(c)',between(paper,'(c)','(17 marks)').replace(' • ','\n• '),17,'Production 6 × 2 (2:1:0); packaging 2 × 1; labelling 3 × 1',[criterion('stages','Stages of production',6,[0,1,2],'Six stages, each graded 2:1:0. Complete source process, including the previously omitted rind, maturation, grading and portioning stages; this is an industrial account, not a validated home-preservation recipe: '+stages),criterion('packaging','Packaging',2,[0,1],'Two packaging points, each graded 1:0. Complete source examples: '+packaging),criterion('labelling','Labelling',3,[0,1],'Three label details, each graded 1:0. Complete source examples: '+labelling)]))
 assert len(fixes)==3 and len(added)==1 and sum(f['set']['totalMarks'] for f in fixes.values())+sum(c['totalMarks'] for c in added)==50
 return fixes,added


def write():
 fixes,added=build();save_batch('B2',fixes,added,dict(tasks=4,marks=50,selectionDecisions='One independent description and one risk-factor task under (a); correct existing calcium to (b), correct the existing cheese card to (c) without changing its ID. Required cheese headings stay whole. No finite printed option pool.',sourceClarifications={'calcium':dict(source='https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/',note='Distinguish active absorption, factors reducing absorption and broader calcium balance; phosphorus is not a universal absorption aid.')},checked='2026-11-01'));print('2025 Higher B2: four reviewed tasks, 50 offered marks; cheese and calcium IDs preserved; references corrected.')

if __name__=='__main__':
 if '--write' in sys.argv:write()
 else:print(json.dumps(build(),ensure_ascii=False,indent=2))
