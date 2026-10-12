#!/usr/bin/env python3
"""Rebuild irish-foundation-2026-source-review.json from the official paper (see _ledger.py).

Generated from the review-time maker; AMENDMENTS and RECORDED carry the later, dated edits.
Run with --check to verify the committed ledger is byte-identical. Run from any directory.
"""
import os
import sys
from pathlib import Path
_REPO = Path(__file__).resolve().parents[4]
os.chdir(_REPO)
sys.path.insert(0, str(_REPO / 'scripts/markbank/authoring'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ledger import finish  # noqa: E402
"""One-off writer for the reviewed 2026 Foundation ledger (scratch). Raws matched exactly from the PDF."""
import json,re,hashlib
from pathlib import Path
import fitz
ROOT=Path(str(_REPO))
DIRECTIVE=re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|trí phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]|dó/di|Cuir ciorcal|dhá thagairt',re.I)
clean=lambda t:re.sub(r'\s+',' ',t).strip()
REQ='Required answers within the section or selected passage; no finite task menu.'
WRITE='Closed choose-two of four writing tasks: 4A+4B, 4A+5A, 4A+5B, 4B+5A, 4B+5B, 5A+5B. Each pair is 90 marks. 4(b) is a letter in 2026, so there is no interview-date choice.'
PAIR2='Choose two of three passages: AB, AC, BC; each route 50 marks. Each published answer is also independently practicable at its own printed tariff.'
PAIR3='Choose two of three passages: AB, AC, BC; each route 60 marks. Each published answer is also independently practicable at its own printed tariff.'
TICK='Correct-answer selection; MCQ distractors and map boxes are not valid task routes.'
TEXT='Source-text wording inside a reading passage, not a candidate instruction.'
LETTER='Required picture instruction: two open information points per picture are required content, not a closed menu. Open friend and flexible dó/di.'
rules=[(2,'Freagair gach ceist.',REQ),(2,'Freagair gach ceist (1, 2 agus 3).',REQ),(2,'Freagair dhá cheist',WRITE),(2,'peann gorm nó',"Pen colour instruction, not an answer route."),
 (3,'Freagair gach ceist.',REQ),(3,'Cuir tic',TICK),(4,'Cuir tic',TICK),(5,'Nuair a bheidh',REQ),(6,'Freagair gach ceist',REQ),
 (7,'Ceist 2 Freagair do rogha',PAIR2),(7,'Léigh an litir',REQ),(7,'mhí Feabhra. Luaigh',TEXT),(7,'nuachtán na scoile',TEXT),
 (8,'Léigh an bróisiúr',REQ),(8,'ag siúl nó ag rothaíocht',TEXT),(8,'trí oíche, ceithre oíche nó',TEXT),(9,'Léigh an scéal',REQ),
 (10,'Ceist 3 Freagair do rogha',PAIR3),(10,'Léigh an t-alt',REQ),(10,'dheartháir Jason',TEXT),(11,'Léigh an giota',REQ),(12,'Léigh na véarsaí',REQ),
 (13,'Freagair dhá cheist',WRITE),(13,'4 (a), 4 (b), 5 (a) nó 5 (b)',WRITE),(14,'Freagair dhá cheist',WRITE),
 (15,'ag insint dó/di',LETTER),(15,'dhá phointe eolais',LETTER),(20,'D’fhéadfadh sé',"Copyright statement, not a task."),(20,'chuici. Ní ghlacann',"Copyright statement, not a task.")]
paper_path=ROOT/'paper-trail-corpus/exampapers/2026/LC001BLP100IV.pdf';scheme_path=ROOT/'paper-trail-corpus/markingschemes/2026/LC001BLP100IV.pdf'
d=fitz.open(paper_path);decisions=[]
for i,p in enumerate(d,1):
    for line in p.get_text().splitlines():
        raw=clean(line)
        if not DIRECTIVE.search(raw):continue
        hits={r for pg,k,r in rules if pg==i and k in raw}
        if i in (2,3) and raw.startswith('Freagair gach ceist'):hits={REQ}
        assert len(hits)==1,(i,raw,hits)
        decisions.append(dict(page=i,raw=raw,decision=hits.pop()))
assert len(decisions)==32,len(decisions)
ledger=dict(year=2026,level='foundation',paperFileid='LC001BLP100IV.pdf',schemeFileid='LC001BLP100IV.pdf',
 paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
 reviewDate='2026-10-11',status='reviewed',reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,21)),
 reviewMethod='Visual inspection of every rendered paper and scheme page (pairs at 1.5×), including covers, blank pages, general guidance, modified scheme, transcript and annotation key; cross-checked extracted text.',
 selectionDecisions=decisions,
 boundaries=dict(listening=dict(tasks=14,marks=120,paperPages=[3,4,5],schemePages=[2]),
   matching=dict(tasks=10,marks=40,paperPages=[6],schemePages=[3],answers='HGFBIJECDA'),
   readingQ2=dict(tasks=15,tariffs={'2A':[1,6,6,6,6],'2B':[6,6,6,6,1],'2C':[6,1,6,6,6]},pairedRoutes=3,marksPerPair=50,paperPages=[7,8,9],schemePages=[4]),
   readingQ3=dict(tasks=15,tariffs={'3A':[7,7,7,2,7],'3B':[6,6,6,6,6],'3C':[7,7,7,7,2]},pairedRoutes=3,marksPerPair=60,paperPages=[10,11,12],schemePages=[5]),
   writing=dict(wholeResponses=4,marksPerResponse=45,pairedRoutes=6,marksPerPair=90,paperPages=[14,15,16,17],schemePages=[6,7,8,9,10,11,12,13,14,15]),
   expectedCards=70,candidateExamMarks=360),
 sourceFindings=[
  'Full visual sweep 2026-10-11: paper PDF 1–20 and scheme PDF 1–20. Paper 360 = listening 120 + matching 40 + Q2 50 + Q3 60 + writing 90 (any two of 4(a), 4(b), 5(a), 5(b), 45 each).',
  'Listening tariffs are unequal and published per part on scheme PDF 2: 1(a) 10, 1(b) 4; 2(a) 10, 2(b) 4; 3 8; 4 8; 5(a) 8, 5(b) 8; 6(a) 15, 6(b) 5; 7(a)/(b) 10 each; 8(a)/(b) 10 each = 120. Map answer: fourth box at the top. The scheme also prints the full listening transcript (PDF 16–18); it is answer material, never a listening prompt.',
  'Reading tariffs are unequal and published per part on scheme PDF 4–5: 2(a) 1/6/6/6/6; 2(b) 6/6/6/6/1; 2(c) 6/1/6/6/6; 3(a) 7/7/7/2/7; 3(b) 6 each; 3(c) 7/7/7/7/2. Each passage still totals 25 or 30. Every card uses its own printed tariff; no equal split is imposed.',
  'Scheme spelling variants against the paper: 3a(2) “Is realta cheoil í.” (paper réalta), 3a(4) “Podchraoladh ráthúil” (paper rathúil), 3b(5) “Compórdach” (paper Compordach). The scheme wording is kept as the key; the printed option is the same answer.',
  'Matching key HGFBIJECDA (paper PDF 6, scheme PDF 3); a picture number in place of the letter is accepted if clear.',
  'Notice 4(a) silent disco with Calvin Harris and new speakers (paper PDF 14; scheme PDF 7–9): layout 1, picture 1 10 (5+5), picture 2 13 (4+3+3+3), picture 3 5, picture 4 5, language 11 = 45. −1 each time the past tense is used.',
  'Letter 4(b) trip to London (paper PDF 15; scheme PDF 10–11): address 2, date 1, greeting 1, closing 2; four pictures at 7 each (two points, 4+3); language 11 = 45. No word-count penalty is printed for the letter.',
  'Stories 5(a) birthday party (paper PDF 16; scheme PDF 12) and 5(b) lost dog in the park (paper PDF 17; scheme PDF 13–14): communication 34, −4 for each missing reference (mark out of 30, 26, 22, 18 or 14), length table 80–90: 0, 60–79: −2, 30–59: −3, <30: −4 applied only when marking out of 34; language 11.',
  'Published scheme carry-overs: the 5(a) task line names “Féile cheoil” although the paper and the scheme reference examples concern the Cóisir Lae Breithe; the modified-scheme page (PDF 15) lists “Ceist 4(b) Foirm Iarratais” although 4(b) is a letter. Both originals are preserved and disclosed; the printed 2026 tasks are assessed.',
  'Language uses the 2026 four-band table (Sár-mhaith 9–11, An-mhaith 6–8, Maith/Maith go leor 3–5, Lag/An-lag 0–2) on every writing task; earlier seven-band tables are not imported. Scheme PDF 6: all attempted writing answers are marked and the best two count.'],
 nonPoolDecisions=[
  'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
  'Notice headings and the four letter picture instructions are compulsory context; the two information points per letter picture are open content, not a printed menu.',
  'The five story references are a communication criterion with non-exhaustive examples, not a printed choose-five menu; the 5(b) picture captions are vocabulary support.',
  'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.'],
 audio=dict(url='https://www.examinations.ie/archive/exampapers/2026/LC001BLP017IV.mp3',httpStatus=200,contentType='audio/mpeg',bytes=56491925,verified='2026-10-11'),
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = []
RECORDED = {'audio': {'url': 'https://www.examinations.ie/archive/exampapers/2026/LC001BLP017IV.mp3',
           'httpStatus': 200,
           'contentType': 'audio/mpeg',
           'bytes': 56491925,
           'verified': '2026-10-11',
           'browserReadyState': 4,
           'durationSeconds': 1765.372656,
           'playbackAdvanced': True},
 'runtimeVerification': {'date': '2026-10-11',
                         'viewport': [390, 844],
                         'markBankRoutes': 16,
                         'atlasRoutes': 13,
                         'sourceReader': 'Reader page counts matched every card (aural 3, pairs 2); next/last navigation, close/focus return and '
                                         'horizontal-overflow checks passed.',
                         'atlas': 'Every Atlas route rendered exactly its paper plus scheme pages (notice 1+3, letter 1+2, 4B+5A 2+3, section 3 5+9).',
                         'audio': 'Official SEC Foundation 2026 recording played in Bank and Atlas, readyState 4, duration 1765.372656 seconds.',
                         'browserErrors': []}}
KEY_ORDER = ['year',
 'level',
 'paperFileid',
 'schemeFileid',
 'paperSha256',
 'schemeSha256',
 'reviewDate',
 'status',
 'reviewedPaperPages',
 'reviewedSchemePages',
 'reviewMethod',
 'selectionDecisions',
 'boundaries',
 'sourceFindings',
 'nonPoolDecisions',
 'audio',
 'remainingWork',
 'runtimeVerification']

if __name__ == '__main__':
    finish(LEDGER, 'irish-foundation-2026-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
