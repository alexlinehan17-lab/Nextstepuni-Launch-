#!/usr/bin/env python3
"""Rebuild irish-higher-2025-p1-source-review.json from the official paper (see _ledger.py).

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
from irish_higher_2025_p1 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA
paper=fitz.open('paper-trail-corpus/exampapers/2025/LC001ALP100IV.pdf')
lines=list(dict.fromkeys((i,clean(l)) for i,p in enumerate(paper,1) for l in p.get_text().splitlines() if DIRECTIVE.search(clean(l))))
TWO='Two required points; the scheme’s list of accepted points is the answer key for one task, not a pool of task routes.'
ONE='One required answer; the accepted list is the answer key for one task.'
CHOICE='Closed choose-one of A, B, C; with the printed titles this gives nine whole 100-mark routes: A(a)–(e), B(a)–(b), C(a)–(b).'
FORM='AISTE nó ALT is a writing-form choice inside one response (same Stíl/Ábhar/Gaeilge marking); not a separate route. Each printed title A(a)–(e) is a route.'
dec={
 'Scríobh do chuid freagraí le peann gorm nó le peann dubh. Ní ceadmhach peann luaidhe a úsáid.':'Pen colour instruction, not an answer route.',
 'Tá dhá chuid sa scrúdú seo.':'Paper structure statement: both parts required.',
 'Freagair gach cuid – A, B, C – sa fhreagarleabhar seo. Caithfidh do chuid freagraí uile sa triail':'Required answers; no finite task menu.',
 'seo a bheith i nGaeilge, ach amháin nuair nach gá sin.':'Required answers; no finite task menu.',
 '2. Scríobh síos dhá rud a bheidh le cloisteáil ar an gclár.':TWO,
 '(b) Scríobh síos rud amháin a dhéanfaidh na scoláirí nuair a bheidh an taighde':ONE,
 'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú':'Required listening section structure.',
 '2. Scríobh síos an dá chineál oibre a bhíonn ar siúl ag Seán.':TWO,
 '3. Luaigh cúis amháin a dtaitníonn an post le Seán.':ONE,
 '1. Scríobh síos an dá chúis nár lean Aoife ar aghaidh leis an gcleachtadh coirp nuair a bhí':TWO,
 '2. Scríobh síos an dá chúis ar imigh deirfiúr Liam go dtí an Astráil.':TWO,
 '3. Tabhair fáth amháin a ndeir Liam gur mór an chabhair í an teicneolaíocht dá deirfiúr':ONE,
 '2. Luaigh dhá rud a léiríonn gur bean ar leith í Maria, an bhean Bhrasaíleach, dar le hÁine.':TWO,
 '2. Cá gcuireann an custaiméir an buidéal plaisteach folamh nó an canna alúmanaim':'One required answer; “buidéal … nó canna” names the items in one question, not alternative tasks.',
 'Scríobh síos toradh fiúntach amháin a chreideann an rialtas a bheidh ar an scéim seo.':ONE,
 'Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.':CHOICE,
 'Treoracha: Ní gá níos mó ná 500‐600 focal nó mar sin a scríobh i gcás ar bith.':'Length guidance (500–600 words), not a selection.',
 'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar':'Instruction to keep the chosen title connected; the selection itself is classified on the title lines.',
 'Scríobh AISTE nó ALT NUACHTÁIN/IRISE ar cheann amháin de na hábhair seo.':FORM,
 'Ceap SCÉAL a mbeadh do rogha ceann amháin díobh seo oiriúnach mar theideal air.':CHOICE+' Two titles (a)–(b) for B.',
 'Freagair do rogha ceann amháin díobh seo.':CHOICE+' C(a) or C(b).',
 'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:':'Stance for or against the motion is the argument direction inside one speech, marked identically; not a separate route.',
 'A AISTE nó ALT NUACHTÁIN/IRISE 100 marc':FORM,
}
out=[]
for p,r in lines:
    d=dec.get(r) or ('Copyright statement, not a task.' if p==20 else None)
    assert d,(p,r); out.append(dict(page=p,raw=r,decision=d))
ver=json.load(open('scripts/markbank/authored/irish-listening-audio-verification.json'))
ledger=dict(year=2025, level='higher', paperFileid='LC001ALP100IV.pdf', schemeFileid='LC001ALP000IV.pdf', paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA,
 reviewDate='2026-10-11', status='reviewed', reviewedPaperPages=list(range(1,21)), reviewedSchemePages=list(range(1,18))+[48],
 schemeScope='Combined Paper 1 and Paper 2 scheme. PDF 1–2 cover and note; 3 listening tariffs; 4–6 listening transcript (never shown to students); 7–11 listening answers; 12–17 composition marking, annotation symbols, Stíl/Ábhar/Gaeilge bands and S1–S4 grades; 48 modified marking (SMM). PDF 18–47 are Paper 2; 49–52 blank.',
 reviewMethod='Visual inspection of every paper page (answer-booklet pages 8–19 are ruled writing space) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=out,
 audio=dict(url='https://www.examinations.ie/archive/exampapers/2025/LC001ZLP017IV.mp3', verified='2026-10-11', evidence='scripts/markbank/authored/irish-listening-audio-verification.json', note='One SEC recording serves the Higher and Ordinary 2025 listening test; all 2025 listening cards already play it (commit ef1a7e550).'),
 nonPoolDecisions=[
  'Listening: “Scríobh síos dhá …/Luaigh dhá …” asks for two points at 2 + 2; the scheme lists more accepted points than required. These are answer keys for one task, not task routes.',
  'Card unit for listening: each printed question at its own 2 or 2 + 2 tariff. The eight retained legacy whole-segment cards (Fógra, Mír, Píosa) keep their IDs and now carry the same lifted scheme text; the Bank reader groups a recording section into one exercise.',
  'Composition: A–C is a closed choose-one; the nine printed titles are the routes and were already carded (IDs retained). AISTE nó ALT (form) and the debate stance (ar son nó ina aghaidh) stay inside one response.',
  'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.'],
 sourceFindings=[
  'Paper 1 = 160: Cuid I listening 60 (Cuid A 18 = Fógra 1 10 + Fógra 2 8; Cuid B 28 = Comhrá 1 14 + Comhrá 2 14; Cuid C 14 = Píosa 1 6 + Píosa 2 8), every question 2 marks or 2 + 2; Cuid II composition 100 (choose one of A, B, C).',
  'Listening language: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge” (scheme PDF 3 and 11) is one section-level deduction; each card states it without applying it.',
  'Comhrá 2 An Chéad Mhír Q3: the scheme notes the paper omitted the séimhiú on ‘deirfiúr’ (“dá deirfiúr”); kept as printed.',
  'Composition S4 (“Easnamhach”) applies only to A(a), A(d), A(e) and C(b) in 2025 (scheme PDF 17).',
  'Legacy corrections: the Píosa a Dó segment card had composition text leaked into its answer key, and the nine composition cards carried paraphrased English marking notes; all now carry the lifted 2025 scheme text. IDs, totals and topics unchanged.'],
 remainingWork=[])
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = [('Card unit for listening: each printed question at its own 2 or 2 + 2 tariff. The eight retained legacy whole-segment cards (Fógra, Mír, Píosa) keep their '
  'IDs and now carry the same lifted scheme text; the Bank reader groups a recording section into one exercise.',
  'Card unit for listening: the eight retained legacy segment cards (Fógra, Mír, Píosa) keep their IDs and stay the card unit, because the Bank plays one '
  'recording section as one exercise; every printed question is a separate criterion at its published 2 or 2 + 2 tariff (24 questions, 60 marks). Separate '
  'question cards are not added: they would repeat the same prompts inside that exercise.'),
 ('Legacy corrections: the Píosa a Dó segment card had composition text leaked into its answer key, and the nine composition cards carried paraphrased English '
  'marking notes; all now carry the lifted 2025 scheme text. IDs, totals and topics unchanged.',
  'Legacy corrections (IDs, totals and topics unchanged): the Píosa a Dó segment card had composition text leaked into its answer key; each segment card had '
  'one undivided criterion; the nine composition cards carried paraphrased English marking notes and no S1–S4 grades. All now carry the lifted 2025 scheme '
  'text and per-question tariffs.')]
RECORDED = {'runtimeVerification': {'date': '2026-10-11',
                         'viewport': [390, 844],
                         'markBankRoutes': 4,
                         'atlasRoutes': 5,
                         'sourceReader': 'The full listening test (first exercise Cuid A, 8 prompts with per-question marks), one segment card and two '
                                         'composition titles rendered their paper page; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Segment and title routes rendered their paper page plus reviewed scheme pages (listening 1+1 and 1+2, composition 1+6); the '
                                  'frozen Cuid A section kept its original crop.',
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
    finish(LEDGER, 'irish-higher-2025-p1-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
