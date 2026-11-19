#!/usr/bin/env python3
"""Independent 2015 Higher full-page visual inventory, before card authoring."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
SOURCES = [
 ('paper','examiner-reports/japanese/papers/2015-hl-000-paper.pdf','91e2718a0447eca580669607a334026aff6299d0d4523e86937a43bff1b16145'),
 ('aural','examiner-reports/japanese/papers/2015-hl-A00-paper.pdf','d66a1b1135ce90d812f908f6ce0db96693b679bf8cedf1eb7c85ecd640102d7f'),
 ('scheme','examiner-reports/japanese/schemes/2015-hl.pdf','eebf8e3aacf9c162bf075915785491f93d1d633d2dab3278536e6d7eea48e2e1'),
]
TASKS=[]
def task(section,q,marks,pp,sp,atlas,roman=None,additional=None):
 component='aural' if section.startswith('L') else 'paper'
 t={'key':[section,q,None,roman],'marks':marks,'component':component,'paperPages':[pp],'schemePages':sp,
    'atlas':{'fileid':f'LC058ALP{"A00" if component=="aural" else "000"}EV.pdf','questionNumber':str(atlas)}}
 if additional:t['atlas']['additionalQuestionNumbers']=list(map(str,additional))
 TASKS.append(t)
def build():
 task('1A',1,6,3,[5],1)
 for roman in ['i','ii']:task('1A',2,2,3,[5],2,roman)
 for roman in ['i','ii','iii']:task('1A',3,2,3,[6],3,roman)
 for roman,marks in [('i',2),('ii',4)]:task('1A',4,marks,3,[6],4,roman)
 for q in range(1,5):task('1B',q,2,4,[6],q+4)
 task('2A',1,12,7,[7],9)
 for roman in ['i','ii','iii','iv']:task('2A',2,2,7,[7],10,roman)
 for roman,sp in [('i',7),('ii',7),('iii',8)]:task('2A',3,2,7,[sp],11,roman)
 task('2A',4,4,7,[8],12)
 for q in [1,2]:task('2B',q,5,8,[8],20)
 task('2C',1,5,9,[8],21)
 task('2C',2,5,9,[9],21)
 for q,pairs in [(1,[('i',3),('ii',2)]),(2,[('i',2),('ii',2)]),(3,[('i',3),('ii',2)])]:
  for roman,marks in pairs:task('3A',q,marks,11,[10],q+12,roman)
 for q in [1,2]:task('3B',q,3,11,[10],q+15)
 task('3C',None,10,12,[10],22)
 task('3D',None,10,12,[11],23)
 task('4',None,40,14,[12,13],18)
 task('5',None,60,16,[14,15],19)
 task('LA',None,18,2,[3],1,additional=[2,3])
 for roman,marks in [('i',2),('ii',2),('iii',2),('iv',3),('v',3)]:task('LB',1,marks,3,[3],8,roman)
 task('LB',2,6,3,[3],9)
 for roman in ['i','ii']:task('LB',3,3,3,[4],10,roman)
 for roman,marks in [('i',2),('ii',2),('iii',3),('iv',4)]:task('LC',1,marks,4,[4],11,roman)
 for roman,marks in [('i',3),('ii',2),('iii',4)]:task('LC',2,marks,4,[4],12,roman)
 for q,marks,sp,atlas in [(1,4,4,13),(2,3,4,14),(3,3,5,15),(4,2,5,4),(5,2,5,5),(6,2,5,6),(7,2,5,7)]:task('LD',q,marks,5,[sp],atlas)
 assert len(TASKS)==60,len(TASKS)
 totals={name:sum(t['marks'] for t in TASKS if condition(t)) for name,condition in [
  ('reading',lambda t:t['key'][0][0] in '123'),('writing',lambda t:t['key'][0][0] in '45'),('listening',lambda t:t['component']=='aural'),('total',lambda t:True)]}
 assert totals=={'reading':120,'writing':100,'listening':80,'total':300},totals
 sources=[]
 for component,path,sha in SOURCES:
  assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha
  sources.append({'component':component,'path':path,'sha256':sha})
 return {'subjectId':'japanese','year':2015,'level':'hl','reviewedAt':'2026-11-09',
 'method':'Independent full visual sweep of all twenty written, eight aural and twenty scheme physical pages, before authoring. Required pools and tables stay whole; all alternatives, source partials and source scope are retained.',
 'sources':sources,'tasks':TASKS,'checksums':totals,
 'candidateMaximum':{'written':220,'listening':80,'total':300,'writingChoice':'All five written questions required; Q4 one of concert/restaurant options using the same grid; Q5 any four of six headings.'},
 'pageRoles':{
  'paper':dict(zip(map(str,range(1,21)),[
   'cover: written220, all five questions required',
   'Q1 full Kelloggs webpage: eight links, six brands and banana honey-nut recipe',
   'Q1A required six links, two AllBran varieties, two granola fruits, three brand questions and two recipe tasks',
   'Q1B full four forum comments, vocabulary and four separately priced questions',
   'explicit blank',
   'Q2 full cultural programme flyer: sumo, wadaiko and geisha, underlined translation and vocabulary',
   'Q2A required three-course table with two given cells, four Japanese questions, three English questions and translation',
   'Q2B five required meanings and five different required readings, examples',
   'Q2C two required five-item grammar pools, full post-blank contexts',
   'Q3 full Brendan WWOOF blog entries for21/22/23August, pictures, dates and vocabulary',
   'Q3A six independent English tasks; Q3B two Japanese tasks',
   'Q3C five required reading/meaning pairs; Q3D all ten particle blanks across seven sentences',
   'explicit blank',
   'Q4 concert OR restaurant email, two required questions in chosen option,200characters',
   'Q4 answer grid',
   'Q5 scholarship application essay, any four of six headings,320characters',
   'Q5 answer grid','Q5 answer grid','Q5 answer grid','explicit blank back cover'])),
  'aural':dict(zip(map(str,range(1,9)),[
   'cover: listening80, all answers English',
   'A three speeches: complete required twelve-cell table, four headings',
   'B three news items: garage-sale five tasks including eight phone blanks, Peter Frankl choice pool and two weather tasks',
   'C campus/hospital conversations: seven tasks including directions, symptoms and suggestions choices',
   'D Lisa/Mari conversation: seven tasks and full context',
   'explicit blank','explicit blank','explicit blank back cover'])),
  'scheme':dict(zip(map(str,range(1,21)),[
   'cover','general examiner guidance',
   'listening Japanese/romaji/script half credit; A18 table, B1 garage sale12 and B2 Frankl6; phone whole3, no digit allocation; three items whole3, no per-item allocation',
   'B3 two weather pools descending2+1; C20 full/partial/directions/symptoms/suggestions; D1 two details2each and D2 descending2+1',
   'D3 descending2+1, D4to7 full2each; reading120, Q1 heading30 with incorrect-language half credit; Q1A links6 and two choice pools2each',
   'Q1A three brand answers2each, recipe2 and two steps2each; Q1B8 including two breakfast options1each and sausage1/muffin1',
   'Q2A table12 with two unpriced given cells; four Japanese answers2each with extraneous-half rule; first two English answers2each',
   'Q2A English answer3 and translation2+2; Q2B five meanings1each and five readings1each; Q2C first five forms1each',
   'Q2C five verb forms1each',
   'Q3A14 with descending pools and1-mark partial; describe one foreigner only; B6 with generic-difficult2 partial/full3; C five reading1/meaning1 pairs',
   'Q3D all ten blank answers1each',
   'Q4 both alternatives and shared C20/E20: two content8, discretionary4 including opening1/closing1',
   'Q4 expression full bands, lower15 when C<=10 or length<150, global-language/error guidance',
   'Q5 six headings, choose four content6each; discretionary6 including opening1/closing1; expression30',
   'Q5 expression full bands, lower20 when C<=15 or length<200, global-language/error guidance',
   'tapescript A and B1/B2; multiple languages then12, famous foreigner and famous street performer, popular at end',
   'tapescript B3 and C',
   'tapescript D','explicit blank','back cover'])),
 },
 'sourceDiscrepancies':[],
 'choiceBoundaries':[
  'Q1A all six required links1each stay whole; varieties choose two of five1each, fruits choose two of four1each. Three brands are separately priced2 each. Recipe name2, choose-two complete steps2each. Q1B has four tasks2each, breakfast choose-two1each and sausage1/muffin1.',
  'Q2A complete table has ten blank cells priced12: two days separately1 in each of first two rows, all other blank cells1; everyday and not applicable are given/unpriced. Four Japanese tasks2each; three English tasks2each; translation two components2each. Two different kanji pools5each and two grammar pools5each remain four complete required tasks.',
  'Q3 journey choose-two descending2+1; year-out purpose full2/college background partial1. Weather choose-two1each. Describe one foreigner only, two details descending2+1, preserve both complete person pools behind one-person selection without creating separate scheduled cards. Family choose-two descending2+1; dialect exact comparison3/generic difficult2. Kanji all five reading1/meaning1 pairs; particles all ten1each.',
  'Q4 concert OR restaurant is one40-mark task with the shared grid and both complete alternatives. Each of two content responses8, opening1, closing1, remaining discretionary2 kept global. C<=10 or length<150 applies lowerE15. Q5 any four of six headings6each, opening1, closing1 and remaining discretionary4 global; C<=15 or length<200 lowerE20. No invented per-heading discretionary allocation.',
  'Listening A one whole required twelve-cell table18 with source component rows and local enjoyment quotas; all three existing row Atlas anchors retained. B/C/D retain all22 independent tasks and published descending/partial pools. Phone03-6576-8180 is whole3 without a digit split. Garage-sale three-item pool has total3 but no explicit per-item tariff: retain full pool in unpriced confidence review with exact language guidance visible, no invented item allocation.',
  'Peter Frankl chooses three response details at2each with popular partial1 printed at pool level. Many languages/12 languages are one transcript-supported concept. Popular is not exclusively attached to famous-foreigner because transcript separately describes a famous foreigner, famous street performer, and popularity; preserve the partial scope and count each answer once. Street performer and juggler remain distinct printed facts.',
  'Listening half-credit rule explicitly names Japanese/romaji/script. Q1 incorrect-language rule is printed on its heading; do not silently extend it to Q2/Q3. Q2A2 extraneous-half rule covers its four Japanese responses only. No writing penalty invented.',
  'Preserve all23 written and15 aural Atlas IDs/labels/regions, including the three original A-table row anchors. Scheme upper bounds21to20 only.'
 ]}
if __name__=='__main__':
 result=build()
 (Path(__file__).parent/'reviews/japanese-2015-hl-census.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(f'{len(TASKS)} independently counted tasks; {result["checksums"]}')
