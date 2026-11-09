#!/usr/bin/env python3
"""Independent full visual census of 2016 Ordinary, before card authoring."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
 ('paper', 'examiner-reports/japanese/papers/2016-ol-000-paper.pdf', '9377b217ba808b6320baa90d17f5fa0a1a33c65cb520f363a4cdef944067e4b7'),
 ('aural', 'examiner-reports/japanese/papers/2016-ol-A00-paper.pdf', 'acacbc404fed69359b1e90797d1263307fc7a2cbbd0c6ea0124c9e6e98d163e1'),
 ('scheme', 'examiner-reports/japanese/schemes/2016-ol.pdf', 'd9cf9b92a4cebec8e58be494bd8388efddd680651e1271d1a08bfe42dadea3c5'),
]
TASKS=[]
def task(section,q,marks,pp,sp,atlas,roman=None):
 component='aural' if section.startswith('L') else 'paper'
 TASKS.append({'key':[section,q,None,roman], 'marks':marks,'component':component,'paperPages':[pp],'schemePages':sp,
  'atlas':{'fileid':f'LC058GLP{"A00" if component=="aural" else "000"}EV.pdf','questionNumber':str(atlas)}})
def build():
 for q,marks in enumerate([10,2,4,4,6,4],1):task('1',q,marks,3,[5],q)
 task('2A',1,9,5,[6],7)
 task('2A',2,3,5,[6],8)
 for roman in ['i','ii']:task('2A',3,2,5,[6],9,roman)
 task('2A',4,15,5,[6],10)
 for q in [1,2]:task('2B',q,10,6,[7],17)
 task('2C',None,10,7,[7],18)
 task('3A',1,2,9,[8],11)
 for roman,marks in [('i',4),('ii',2)]:task('3A',2,marks,9,[8],12,roman)
 for roman in ['i','ii','iii']:task('3A',3,3,9,[8],13,roman)
 for roman in ['i','ii','iii']:task('3A',4,3,9,[8],14,roman)
 task('3B',None,3,10,[8],19)
 task('4',None,30,11,[9],15)
 task('5',None,50,12,[9,10],16)
 for q,marks in [(1,[2,4,4]),(2,[2,4,4]),(3,[4,4])]:
  for roman,mark in zip(['i','ii','iii'],marks):task('LA',q,mark,2,[3],q,roman)
 for q,marks,atlas in [(1,[4,4,4,4],7),(2,[4,4],8)]:
  for roman,mark in zip(['i','ii','iii','iv'],marks):task('LB',q,mark,3,[3],atlas,roman)
 for roman in ['i','ii','iii']:task('LC',1,4,4,[4],9,roman)
 task('LC',2,4,4,[4],10)
 for roman in ['i','ii']:task('LC',3,4,4,[4],11,roman)
 for q,atlas in [(1,12),(2,13),(3,14),(4,4),(5,5),(6,6)]:task('LD',q,4,5,[4],atlas)
 assert len(TASKS)==52
 totals={name:sum(t['marks'] for t in TASKS if condition(t)) for name,condition in [
  ('reading',lambda t:t['key'][0][0] in '123'),('writing',lambda t:t['key'][0][0] in '45'),('listening',lambda t:t['component']=='aural'),('total',lambda t:True)]}
 assert totals=={'reading':120,'writing':80,'listening':100,'total':300},totals
 sources=[]
 for component,path,expected in SOURCES:
  assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected
  sources.append({'component':component,'path':path,'sha256':expected})
 return {'subjectId':'japanese','year':2016,'level':'ol','reviewedAt':'2026-11-09',
 'method':'Independent full visual sweep of all sixteen written, eight aural and sixteen scheme physical pages before authoring. Required pools/tables remain whole; separately priced independent responses follow the original scheme.',
 'sources':sources,'tasks':TASKS,'checksums':totals,
 'candidateMaximum':{'written':200,'listening':100,'total':300,'writingChoice':'All five written questions required. Q4 all ten cloze blanks, use each word once; Q5 any five of seven responses.'},
 'pageRoles':{
 'paper':dict(zip(map(str,range(1,17)),[
 'cover: written200, answer all five questions',
 'Q1 full Tokyo orchestra kids workshop flyer with times, rooms, meals, instruments and event calendar',
 'Q1 five required start times, date, two rooms, choose-two meals, three month events, choose-two Japanese instruments',
 'Q2 full MATCHA Harajuku article: Marion Crepes, Yoyogi flea market and Kiddy Land',
 'Q2A required shop/location matching, one crepe fact, separate girl/boy character pools and all five truth/Japanese-evidence pairs',
 'Q2B all five positive forms and all five particle selections, examples and underlining',
 'Q2C ten required kanji meanings and all English/Irish distractors, given year example',
 'Q3 full illustrated Sandra day timeline with times, meals, lessons, work and vocabulary',
 'Q3A nine priced responses: Ueno, two nationalities, lunch, three multiple choices and three Japanese answers',
 'Q3B culture comparison of typical Japanese high-school day with own day',
 'Q4 full ten-blank self-introduction cloze, complete word bank and use-once direction',
 'Q5 full seven summer-holiday prompts, answer five, vocabulary',
 'explicit blank','explicit blank','explicit blank','explicit blank back cover'])),
 'aural':dict(zip(map(str,range(1,9)),[
 'cover: listening100, all answers English',
 'A three interviews: eight lotto tasks with complete multiple-choice options',
 'B friends conversation before/after concert: six tasks and complete options',
 'C three news items: six tasks including four missing phone digits and two weather responses',
 'D Daniel/neighbour conversation: six tasks and complete options',
 'explicit blank','explicit blank','explicit blank back cover'])),
 'scheme':dict(zip(map(str,range(1,17)),[
 'cover','general examiner guidance',
 'listening Japanese/romaji/script half credit; A28 and B24; car1 plus one descriptor1',
 'C24: four phone digits1each and whole weather response4; D24 six answers4each',
 'reading appropriate-language half credit; Q1 six tasks30 with required pools/date1+1/choices',
 'Q2A31: match3each, crepe3, girl/boy2each, all five truth1/evidence2 pairs',
 'Q2B20: five positive forms2each (printed second answer omits ro) and five particles2each; Q2C ten meanings1each',
 'Q3A26: all nine responses; third Japanese prompt misnumbered(ii); culture point2 plus discretionary1',
 'Q4 ten answers3each; Q5 any five C5/E5, content bands1/2-3/4-5, Ecap3 where C<4',
 'Q5 full expression bands1/2-3/4-5, error guidance and global-language instruction',
 'tapescript A','tapescript B','tapescript C','tapescript D','explicit blank','back cover'])),
 },
 'sourceDiscrepancies':[
 {'taskKey':['2B',1,None,None],'paperPages':[6],'schemePages':[7],
  'evidence':'Paper(ii) is フリーマーケットはおもしろくないです。 The original scheme prints おもしいです。 as its positive answer, visibly omitting ろ. Preserve the literal published answer and expose this spelling discrepancy; do not silently replace the source wording.'},
 {'taskKey':['3A',4,None,'iii'],'paperPages':[9],'schemePages':[8],
  'evidence':'The third Japanese prompt 先生はどんな人ですか。 is numbered(iii) in the paper but repeats(ii) in the scheme. Exact prompt/answer wording establishes the binding; retain the paper reference and disclose the scheme numbering.'}],
 'choiceBoundaries':[
 'Q1 requires five times2each, two rooms2each and three events2each as three whole pools; date is day1 plus month1; choose two of three lunch options2each and two of three instruments2each.',
 'Q2A match all three locations3each in one pool; choose one crepe detail3; separately priced girl/boy character pools choose one each2; all five truth1/Japanese-evidence2 pairs remain one required pool15. Both grammar pools require five answers2each, and kanji requires ten1each.',
 'Q3A two nationalities of four2each and one lunch detail2; three multiple choices3each and three Japanese answers3each separately priced. Q3B has no model answer: one source-priced point2 and one separately claimable discretionary mark1.',
 'Q4 all ten cloze answers3each and full use-once word bank. Q5 any five of seven independent C5/E5 responses; each response Ecap3 when its own C<=3. No inherited name/age allocation.',
 'Listening26 tasks: A8/B6/C6/D6. Car1 plus choose-one descriptor1; Asia/Vietnam choose-one2. Phone0570-064-110 has four missing digits5,6,4,1, each1; printed digits unpriced. Weather each requires one response4 with all listed alternatives, no invented per-detail marks.',
 'Appropriate-language half credit applies to all24 reading tasks; Japanese/romaji/script half credit applies to all26 listening tasks. No writing-language or extraneous-material reduction printed.',
 'Preserve all19 original written and14 aural Atlas identities/labels/regions; scheme upper bounds17 to16 only.'
 ]}
if __name__=='__main__':
 result=build()
 (Path(__file__).parent/'reviews/japanese-2016-ol-census.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
