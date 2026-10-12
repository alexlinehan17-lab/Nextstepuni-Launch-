#!/usr/bin/env python3
"""Rebuild irish-ordinary-2026-p1-source-review.json from the official paper (see _ledger.py).

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
import json,re,hashlib,sys
from pathlib import Path
import fitz
ROOT=Path(str(_REPO))
sys.path.insert(0,str(ROOT/'scripts/markbank/authoring'))
from irish_ordinary_2026_p1 import DIRECTIVE,clean
COMP='Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark routes and 30 full 100-mark selections (one title from each of two sections).'
FORM='Required form wording inside one composition (giota leanúnach nó blag; litir/ríomhphost; dó/di); not a separate route.'
rules=[(2,'peann gorm nó','Pen colour instruction, not an answer route.'),(2,'Tá dhá chuid','Paper structure statement: both parts required.'),
 (3,'Freagair gach cuid','Required answers; no finite task menu.'),(3,'seo a bheith i nGaeilge','Required answers; no finite task menu.'),
 (3,'lá amháin','One required answer; Satharn or Domhnach are both accepted answers to one task.'),(3,'Cad é an dáta deireanach','One required answer.'),
 (4,'dhá chomhrá','Required listening section structure.'),(6,'an teideal a roghnaítear','Instruction to keep the chosen title connected; selection classified on page 7.'),
 (7,'Freagair do rogha dhá cheann',COMP),(7,'giota leanúnach nó blag',COMP+' '+FORM),(7,'Ceap scéal',COMP),(7,'nó',COMP),
 (7,'Scríobh an litir/an ríomhphost',FORM),(7,'ag insint dó/di',FORM),(7,'a bhailiú don chlub',FORM),(7,'chuig cara leat ag insint dó/di',FORM),(7,'Scríobh an comhrá',FORM),
 (16,'D’fhéadfadh sé','Copyright statement, not a task.'),(16,'Gaolmhar, 2000','Copyright statement, not a task.'),(16,'chuici. Ní ghlacann','Copyright statement, not a task.')]
paper=ROOT/'paper-trail-corpus/exampapers/2026/LC001GLP100IV.pdf';scheme=ROOT/'paper-trail-corpus/markingschemes/2026/LC001GLP100IV.pdf'
d=fitz.open(paper);decisions=[]
for i,p in enumerate(d,1):
    for line in p.get_text().splitlines():
        raw=clean(line)
        if not DIRECTIVE.search(raw):continue
        hits=sorted([(len(k),r) for pg,k,r in rules if pg==i and (k==raw if k=='nó' else k in raw)],reverse=True)
        assert hits and (len(hits)==1 or hits[0][0]>hits[1][0]),(i,raw,hits)
        decisions.append(dict(page=i,raw=raw,decision=hits[0][1]))
ledger=dict(year=2026,level='ordinary',paperFileid='LC001GLP100IV.pdf',schemeFileid='LC001GLP100IV.pdf',
 paperSha256=hashlib.sha256(paper.read_bytes()).hexdigest(),schemeSha256=hashlib.sha256(scheme.read_bytes()).hexdigest(),
 reviewDate='2026-10-11',status='reviewed',reviewedPaperPages=list(range(1,17)),reviewedSchemePages=list(range(1,14))+[34,35,36,37,38,39,40],
 schemeScope='Combined Ordinary scheme. PDF 1–2 cover and note; 3 listening tariffs; 4–6 transcript; 7–9 listening answers; 10–13 composition marking and tables; 34–35 modified marking (SMM, incl. the composition 40-mark table); 36–40 blank. PDF 14–33 are Paper 2.',
 reviewMethod='Visual inspection of every paper page (answer-booklet pages 8–15 are ruled writing space) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=decisions,
 audio=dict(url='https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3',httpStatus=200,contentType='audio/mpeg',bytes=43718095,verified='2026-10-11',
   note='The same SEC recording serves Higher and Ordinary; Ordinary asks different questions on the same extracts.'),
 nonPoolDecisions=['Listening answers with alternatives (e.g. Satharn / Domhnach) are accepted answers to one task, not routes.',
   'Composition: closed choose-two of four sections; each printed title is a 50-mark route and every two-section combination of titles is a 100-mark selection. Letter/email and conversation partner wording stay inside one response.',
   'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
 sourceFindings=['Paper 1 = 160: listening 60 (Cuid A 24, B 24, C 12; every question 3 marks) and composition 100 (any two of A–D at 50: Tasc 2, Ábhar 8, Cumas Gaeilge 40).',
   'Listening language: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge” (scheme PDF 3 and 9) is one section-level deduction; cards state it without applying it. Partial answers: Oifig = 2, Teastas = 2, Neirbhíseach = 2, Cluichí = 2.',
   'Composition 40-mark table (PDF 12) with short-attempt columns M/F1/F2/F3 (36/30/20/10, PDF 13); F1–F3 line counts differ for the body of a letter/email (PDF 11).'],
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = [('Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark routes and 30 full 100-mark selections (one '
  'title from each of two sections).',
  'Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark title cards, each marked on its own 50. '
  'Choice is not a route: no two-section combination cards; the instruction is in each title card’s task requirements.'),
 ('Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark routes and 30 full 100-mark selections (one '
  'title from each of two sections). Required form wording inside one composition (giota leanúnach nó blag; litir/ríomhphost; dó/di); not a separate route.',
  'Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark title cards, each marked on its own 50. '
  'Choice is not a route: no two-section combination cards; the instruction is in each title card’s task requirements. Required form wording inside one '
  'composition (giota leanúnach nó blag; litir/ríomhphost; dó/di); not a separate route.'),
 ('Composition: closed choose-two of four sections; each printed title is a 50-mark route and every two-section combination of titles is a 100-mark selection. '
  'Letter/email and conversation partner wording stay inside one response.',
  'Composition: closed choose-two of four sections; each printed title is a 50-mark card. Choice is not a route: no two-section combination cards are '
  'published; the choose-two instruction is in each title card’s task requirements. Letter/email and conversation partner wording stay inside one response.')]
RECORDED = {'audio': {'url': 'https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3',
           'httpStatus': 200,
           'contentType': 'audio/mpeg',
           'bytes': 43718095,
           'verified': '2026-10-11',
           'note': 'The same SEC recording serves Higher and Ordinary; Ordinary asks different questions on the same extracts.',
           'browserReadyState': 4,
           'durationSeconds': 1366.190469,
           'playbackAdvanced': True},
 'runtimeVerification': {'date': '2026-10-11',
                         'viewport': [390, 844],
                         'markBankRoutes': 4,
                         'atlasRoutes': 5,
                         'sourceReader': 'Listening exercise (3 sections, 8/8/4 questions), a single listening card, a single title and a two-section '
                                         'selection rendered their paper page; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Each route rendered its paper page plus scheme pages (listening 1+1, composition 1+4).',
                         'audio': 'Official SEC 2026 Higher/Ordinary recording played in Bank and Atlas, duration 1366.190469 seconds.',
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
 'schemeScope',
 'reviewMethod',
 'selectionDecisions',
 'audio',
 'nonPoolDecisions',
 'sourceFindings',
 'remainingWork',
 'runtimeVerification']

if __name__ == '__main__':
    finish(LEDGER, 'irish-ordinary-2026-p1-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
