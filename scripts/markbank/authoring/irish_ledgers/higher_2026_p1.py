#!/usr/bin/env python3
"""Rebuild irish-higher-2026-p1-source-review.json from the official paper (see _ledger.py).

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
from irish_higher_2026_p1 import DIRECTIVE,clean
REQ='Required answers; no finite task menu.'
TWO='Two required points; the scheme’s list of accepted points is the answer key for one task, not a pool of task routes.'
ONE='One required reason; the accepted list is the answer key for one task.'
COMP='Closed choose-one of A, B, C; with the printed titles this gives nine whole 100-mark routes: A(a)–(e), B(a)–(b), C(a)–(b).'
FORM='AISTE nó ALT is a writing-form choice inside one response (same Stíl/Ábhar/Gaeilge marking); not a separate route. Each printed title is a route.'
STANCE='Stance for or against the motion is the argument direction inside one speech, marked identically (consistent with English “for or against” tasks); not expanded.'
rules=[(2,'peann gorm nó','Pen colour instruction, not an answer route.'),(2,'Tá dhá chuid','Paper structure statement: both parts required.'),
 (3,'Freagair gach cuid',REQ),(3,'seo a bheith i nGaeilge',REQ),(3,'dhá cháilíocht',TWO),(3,'dhá rud a chaithfidh',TWO),
 (4,'dhá chomhrá',REQ),(4,'dhá phointe eolais faoin gcalaois',TWO),(4,'Luaigh cúis amháin',ONE),(4,'an dá phointe eolais faoin tsaoire',TWO),
 (5,'dhá chúis',TWO),(6,'an dá rud a mheallann',TWO),(6,'dhá dheis',TWO),
 (7,'Freagair do rogha CEANN AMHÁIN',COMP),(7,'Treoracha: Ní gá','Length guidance (500–600 words), not a selection.'),(7,'an teideal a roghnaítear','Instruction to keep the chosen title connected; selection itself is classified on the title lines.'),
 (7,'Scríobh AISTE nó ALT NUACHTÁIN/IRISE ar cheann amháin',FORM+' Five titles (a)–(e) are a closed choose-one pool.'),(7,'Ceap SCÉAL',COMP+' Two titles (a)–(b).'),(7,'Freagair do rogha ceann amháin díobh seo.',COMP+' C(a) or C(b).'),
 (7,'ar son an rúin',STANCE),(7,'A AISTE nó ALT NUACHTÁIN/IRISE 100 marc',FORM),
 (20,'D’fhéadfadh sé','Copyright statement, not a task.'),(20,'Gaolmhar, 2000','Copyright statement, not a task.'),(20,'chuici. Ní ghlacann','Copyright statement, not a task.')]
paper=ROOT/'paper-trail-corpus/exampapers/2026/LC001ALP100IV.pdf';scheme=ROOT/'paper-trail-corpus/markingschemes/2026/LC001ALP100IV.pdf'
d=fitz.open(paper);decisions=[]
for i,p in enumerate(d,1):
    for line in p.get_text().splitlines():
        raw=clean(line)
        if not DIRECTIVE.search(raw):continue
        hits={r for pg,k,r in rules if pg==i and k in raw}
        assert len(hits)==1,(i,raw,hits)
        decisions.append(dict(page=i,raw=raw,decision=hits.pop()))
ledger=dict(year=2026,level='higher',paperFileid='LC001ALP100IV.pdf',schemeFileid='LC001ALP100IV.pdf',
 paperSha256=hashlib.sha256(paper.read_bytes()).hexdigest(),schemeSha256=hashlib.sha256(scheme.read_bytes()).hexdigest(),
 reviewDate='2026-10-11',status='reviewed',reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,17))+[49,50,51,52],
 schemeScope='Combined Paper 1 and Paper 2 scheme. PDF 1–2 cover and note; 3 listening tariffs; 4–6 listening transcript and annotation notes; 7–10 listening answers; 11–16 composition marking; 49 modified marking (SMM); 50–52 blank/back cover. PDF 17–48 are Paper 2 and outside this component.',
 reviewMethod='Visual inspection of every paper page (answer-booklet pages 8–19 are ruled writing space) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=decisions,
 audio=dict(url='https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3',httpStatus=200,contentType='audio/mpeg',bytes=43718095,verified='2026-10-11',
   note='One SEC recording serves the Higher and Ordinary listening test; the Higher-specific filename (LC001ALP017IV.mp3) returns 404.'),
 nonPoolDecisions=['Listening: “Scríobh síos dhá …” asks for two points at 2 + 2; the scheme lists more accepted points than required. These are answer keys for one task, not task routes.',
   'Composition: A–C is a closed choose-one; the nine printed titles are the routes. AISTE nó ALT (form) and the debate stance (ar son nó ina aghaidh) stay inside one response.',
   'Scheme listening notes accept equivalent wording; this does not create extra tasks.',
   'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
 sourceFindings=[
  'Paper 1 = 160: Cuid I listening 60 (Cuid A 18 = Fógra 1 10 + Fógra 2 8; Cuid B 28 = Comhrá 1 14 + Comhrá 2 14; Cuid C 14 = Píosa 1 8 + Píosa 2 6), every question 2 marks or 2 + 2; Cuid II composition 100 (choose one of A, B, C).',
  'Listening language: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge” (scheme PDF 3 and 10) is one section-level deduction (Tuiscint 60, Cumas Gaeilge −0–3), not a per-question award; each card states it without applying it.',
  'Scheme PDF 6 notes: equivalent wording is accepted; a cancelled answer counts if no other is given; extra answers that invalidate the correct one are not accepted.',
  'Wording differences paper vs scheme: Comhrá 2 Mír 1 Q2 “duais” (paper) vs “bonn” (scheme); Píosa 2 Q2 “seirbhísí óige” (paper) vs “seirbhísí óga” (scheme). Accepted answers unaffected; both originals kept.',
  'Composition (scheme PDF 11–16): Stíl 5, Ionramháil Ábhair 15 (bands 13–15 … 0–2), Cumas Gaeilge 80 (Sármhaith 68–80 … An-íseal 0–7), assessed as one unit; deficient attempts S1 (4/13/68), S2 (3/11/56), S3 (2/9/44); S4 (5/10/54) only for A(a), A(b), A(c).',
  'Recording: the 2026 SEC archive serves LC001ZLP017IV.mp3 (Higher/Ordinary listening) — HTTP 200, 43,718,095 bytes. The full transcript on scheme PDF 4–6 is answer material, never a prompt.'],
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = []
RECORDED = {'audio': {'url': 'https://www.examinations.ie/archive/exampapers/2026/LC001ZLP017IV.mp3',
           'httpStatus': 200,
           'contentType': 'audio/mpeg',
           'bytes': 43718095,
           'verified': '2026-10-11',
           'note': 'One SEC recording serves the Higher and Ordinary listening test; the Higher-specific filename (LC001ALP017IV.mp3) returns 404.',
           'browserReadyState': 4,
           'durationSeconds': 1366.190469,
           'playbackAdvanced': True},
 'nonPoolDecisions': ['Listening: “Scríobh síos dhá …” asks for two points at 2 + 2; the scheme lists more accepted points than required. These are answer '
                      'keys for one task, not task routes.',
                      'Composition: A–C is a closed choose-one; the nine printed titles are the routes. AISTE nó ALT (form) and the debate stance (ar son nó '
                      'ina aghaidh) stay inside one response.',
                      'Scheme listening notes accept equivalent wording; this does not create extra tasks.',
                      'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.',
                      'Card unit for listening: each printed question at its own 2 or 2 + 2 tariff. No whole-segment duplicate is added, because the Bank '
                      'reader already shows every question of a recording section together and an overlapping segment card would repeat each prompt.'],
 'runtimeVerification': {'date': '2026-10-11',
                         'viewport': [390, 844],
                         'markBankRoutes': 6,
                         'atlasRoutes': 5,
                         'sourceReader': 'Listening exercise (3 sections, 7/11/5 questions), single listening cards and composition routes rendered their '
                                         'paper page; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Each route rendered its paper page plus scheme pages (listening 1+1, composition 1+5).',
                         'audio': 'Official SEC 2026 Higher/Ordinary recording (LC001ZLP017IV.mp3) played in Bank and Atlas, duration 1366.190469 seconds.',
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
    finish(LEDGER, 'irish-higher-2026-p1-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
