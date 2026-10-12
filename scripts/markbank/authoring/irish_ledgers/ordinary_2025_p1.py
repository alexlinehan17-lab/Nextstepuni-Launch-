#!/usr/bin/env python3
"""Rebuild irish-ordinary-2025-p1-source-review.json from the official paper (see _ledger.py).

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
import json,sys
sys.path.insert(0,'scripts/markbank/authoring')
import fitz
from irish_ordinary_2025_p1 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA
paper=fitz.open('paper-trail-corpus/exampapers/2025/LC001GLP100IV.pdf')
lines=list(dict.fromkeys((i,clean(l)) for i,p in enumerate(paper,1) for l in p.get_text().splitlines() if DIRECTIVE.search(clean(l))))
CH='Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark routes and 30 full 100-mark selections (one title from each of two sections).'
FORM='Required form wording inside one composition (giota leanúnach nó blag; litir/ríomhphost; dó/di; cara or tuismitheoirí); not a separate route.'
dec={'Scríobh do chuid freagraí le peann gorm nó le peann dubh. Ní ceadmhach peann luaidhe a úsáid.':'Pen colour instruction, not an answer route.',
 'Tá dhá chuid sa scrúdú seo.':'Paper structure statement: both parts required.',
 'Freagair gach cuid – A, B, C – sa fhreagarleabhar seo.':'Required answers; no finite task menu.',
 'Caithfidh do chuid freagraí uile sa triail seo a bheith i nGaeilge, ach amháin nuair nach gá sin.':'Required answers; no finite task menu.',
 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú':'Required listening section structure.',
 '2. Scríobh síos áit amháin ina bhfuil na meaisíní speisialta ar fáil chun buidéil phlaisteacha':'One required answer; siopaí and ollmhargaí are both accepted answers to one task.',
 'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar':'Instruction to keep the chosen title connected; selection classified on page 7.',
 'Freagair do rogha dhá cheann de A, B, C, D anseo.':CH,
 'Scríobh giota leanúnach nó blag (leathleathanach nó mar sin) ar cheann amháin de na hábhair seo.':CH+' '+FORM,
 'Ceap scéal (leathleathanach nó mar sin) a mbeadh ceann amháin de na sleachta seo a leanas':CH,
 'nó':CH,
 'Scríobh an litir/an ríomhphost (leathleathanach nó mar sin) a chuirfeá chuig cara leat':FORM,
 'ag insint dó/di faoi na himeachtaí a d’eagraigh Comhairle na nDaltaí agus faoin bpáirt':FORM,
 'ag insint dó/di faoin titim shneachta sin agus faoi mar a chaith tú féin agus do mhuintir':FORM,
 'do chara leat. Scríobh an comhrá (leathleathanach nó mar sin) a bheadh agat le do chara':FORM,
 'nó mar sin) a bheadh agat le do thuismitheoirí faoin ábhar sin.':FORM}
out=[]
for p,r in lines:
    d=dec.get(r) or ('Copyright statement, not a task.' if p==16 else None)
    assert d,(p,r); out.append(dict(page=p,raw=r,decision=d))
ledger=dict(year=2025, level='ordinary', paperFileid='LC001GLP100IV.pdf', schemeFileid='LC001GLP000IV.pdf', paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
 reviewDate='2026-10-11', status='reviewed', reviewedPaperPages=list(range(1,17)), reviewedSchemePages=list(range(1,14))+[30,31],
 schemeScope='Combined Ordinary scheme. PDF 1–2 cover and note; 3 listening tariffs; 4–6 transcript (never shown to students); 7–9 listening answers; 10–13 composition marking, symbols, 40-mark table and short-attempt columns; 30–31 modified marking (SMM, incl. the composition 40-mark table). PDF 14–29 are Paper 2; 32–36 blank.',
 reviewMethod='Visual inspection of every paper page (answer-booklet pages 8–15 are ruled writing space) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=out,
 audio=dict(url='https://www.examinations.ie/archive/exampapers/2025/LC001ZLP017IV.mp3', verified='2026-10-11', evidence='scripts/markbank/authored/irish-listening-audio-verification.json',
            note='One SEC recording serves the Higher and Ordinary 2025 listening test; Ordinary asks different questions on the same extracts. All 2025 listening cards already play it (commit ef1a7e550).'),
 nonPoolDecisions=['Listening answers with alternatives (e.g. siopaí / ollmhargaí) are accepted answers to one task, not routes.',
  'Card unit for listening: the six retained legacy segment cards keep their IDs and stay the card unit, because the Bank plays one recording section as one exercise; every printed question is a separate 3-mark criterion (20 questions, 60 marks). Separate question cards are not added: they would repeat the same prompts inside that exercise.',
  'Composition: closed choose-two of four sections; each printed title is a 50-mark route (already carded, IDs retained) and every two-section combination of titles is a 100-mark selection (30 added). Letter/email and conversation partner wording stay inside one response.',
  'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
 sourceFindings=['Paper 1 = 160: listening 60 (Cuid A 24, B 24, C 12; every question 3 marks) and composition 100 (any two of A–D at 50: Tasc 2, Ábhar 8, Cumas Gaeilge 40).',
  'Listening language: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge” (scheme PDF 3 and 9) is one section-level deduction; cards state it without applying it. Printed partial answers: RTÉ = 1, San ionad = 1, Nócha = 2, Sa chlub = 1, Léargas … = 1.',
  'Composition 40-mark table (PDF 12) with short-attempt columns M/F1/F2/F3 (36/30/20/10, PDF 13); those columns include odd values, so the Cumas Gaeilge award takes any value 0–40.',
  'Legacy corrections (IDs, totals and topics unchanged): each segment card had one undivided criterion; the nine composition cards carried short paraphrased notes and an even-only Cumas Gaeilge scale. All now carry the lifted 2025 scheme text and per-question tariffs.'],
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = [('Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark routes and 30 full 100-mark selections (one '
  'title from each of two sections).',
  'Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark title cards, each marked on its own 50. '
  'Choice is not a route: no two-section combination cards; the instruction is in each title card’s task requirements.'),
 ('Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark routes and 30 full 100-mark selections (one '
  'title from each of two sections). Required form wording inside one composition (giota leanúnach nó blag; litir/ríomhphost; dó/di; cara or tuismitheoirí); '
  'not a separate route.',
  'Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark title cards, each marked on its own 50. '
  'Choice is not a route: no two-section combination cards; the instruction is in each title card’s task requirements. Required form wording inside one '
  'composition (giota leanúnach nó blag; litir/ríomhphost; dó/di; cara or tuismitheoirí); not a separate route.'),
 ('Composition: closed choose-two of four sections; each printed title is a 50-mark route (already carded, IDs retained) and every two-section combination of '
  'titles is a 100-mark selection (30 added). Letter/email and conversation partner wording stay inside one response.',
  'Composition: closed choose-two of four sections; each printed title is a 50-mark card (already carded, IDs retained). Choice is not a route: no two-section '
  'combination cards are published; the choose-two instruction is in each title card’s task requirements. Letter/email and conversation partner wording stay '
  'inside one response.')]
RECORDED = {'runtimeVerification': {'date': '2026-10-12',
                         'viewport': [390, 844],
                         'markBankRoutes': 4,
                         'atlasRoutes': 4,
                         'sourceReader': 'The full Ordinary listening test (first exercise Cuid A, per-question marks), one segment card, one composition '
                                         'title and one two-section selection rendered their paper page; navigation, close/focus return and overflow checks '
                                         'passed.',
                         'atlas': 'Segment, title and selection routes rendered their paper page plus reviewed scheme pages (listening 1+1, composition 1+4); '
                                  'the frozen Cuid A section kept its original crop.',
                         'audio': 'Official SEC 2025 Higher/Ordinary recording (LC001ZLP017IV.mp3) played in Bank and Atlas, duration 1306.487969 seconds.',
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
    finish(LEDGER, 'irish-ordinary-2025-p1-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
