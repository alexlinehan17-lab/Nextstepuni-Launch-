#!/usr/bin/env python3
"""Rebuild irish-higher-2024-p1-source-review.json from the official paper (see _ledger.py).

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
"""Write the 2024 Higher Paper 1 source-review ledger: every raw directive line classified."""
import sys, json, hashlib
ROOT = str(_REPO)
sys.path.insert(0, ROOT + '/scripts/markbank/authoring')
import fitz
from irish_higher_2024_p1 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA, AUDIO_URL

paper = fitz.open(ROOT + '/paper-trail-corpus/exampapers/2024/LC001ALP100IV.pdf')
assert hashlib.sha256(open(ROOT + '/paper-trail-corpus/exampapers/2024/LC001ALP100IV.pdf', 'rb').read()).hexdigest() == PAPER_SHA
assert hashlib.sha256(open(ROOT + '/paper-trail-corpus/markingschemes/2024/LC001ALP000IV.pdf', 'rb').read()).hexdigest() == SCHEME_SHA
lines = []
for i, page in enumerate(paper, 1):
    for line in page.get_text().splitlines():
        raw = clean(line)
        if DIRECTIVE.search(raw) and (i, raw) not in lines:
            lines.append((i, raw))
TWO = 'Two required points; the scheme’s list of accepted points is the answer key for one task, not a pool of task routes.'
ONE = 'One required answer; the accepted list is the answer key for one task.'
COMP = 'Closed choose-one of A, B, C; with the printed titles this gives nine whole 100-mark title cards: A(a)–(e), B(a)–(b), C(a)–(b).'
FORM = 'AISTE nó ALT is a writing-form choice inside one response (same Stíl/Ábhar/Gaeilge marking); not a separate card. Each printed title A(a)–(e) is its own card.'
D = {
    'Scríobh do chuid freagraí le peann gorm nó le peann dubh. Ní ceadmhach peann luaidhe a úsáid.': 'Pen colour instruction, not an answer route.',
    'Tá dhá chuid sa scrúdú seo.': 'Paper structure statement: both parts required.',
    'Freagair gach cuid – A, B, C – sa fhreagarleabhar seo. Caithfidh do chuid freagraí uile sa triail': 'Required answers; no finite task menu.',
    'seo a bheith i nGaeilge, ach amháin nuair nach gá sin.': 'Required answers; no finite task menu.',
    'Cloisfidh tú dhá chomhrá sa chuid seo. Cloisfidh tú gach comhrá díobh faoi dhó. Cloisfidh tú': 'Required listening section structure.',
    'Freagair do rogha CEANN AMHÁIN de A, B nó C anseo thíos.': COMP,
    'Treoracha: Ní gá níos mó ná 500‐600 focal nó mar sin a scríobh i gcás ar bith.': 'Length guidance (500–600 words), not a selection.',
    'Ní mór ceangal cinnte leanúnach a bheith ann idir an teideal a roghnaítear agus an t‐ábhar': 'Instruction to keep the chosen title connected; the selection itself is classified on the title lines.',
    'Scríobh AISTE nó ALT NUACHTÁIN/IRISE ar cheann amháin de na hábhair seo.': FORM,
    'A AISTE nó ALT NUACHTÁIN/IRISE 100 marc': FORM,
    'Ceap SCÉAL a mbeadh do rogha ceann amháin díobh seo oiriúnach mar theideal air.': COMP + ' Two titles (a)–(b) for B.',
    'Freagair do rogha ceann amháin díobh seo.': COMP + ' C(a) or C(b).',
    'Scríobh an chaint a dhéanfá i ndíospóireacht scoile ar son an rúin seo a leanas nó ina aghaidh:': 'Stance for or against the motion is the argument direction inside one speech, marked identically; not a separate card.',
}


def decide(p, r):
    if r in D:
        return D[r]
    if p == 20:
        return 'Copyright statement, not a task.'
    if p in (3, 4, 5, 6) and (' dhá ' in r or ' an dá ' in r):
        return TWO
    if p in (3, 4, 5, 6) and 'amháin' in r:
        return ONE
    raise SystemExit(f'Unclassified directive: {p} {r}')


out = [dict(page=p, raw=r, decision=decide(p, r)) for p, r in lines]
ledger = dict(
    year=2024, level='higher', paperFileid='LC001ALP100IV.pdf', schemeFileid='LC001ALP000IV.pdf',
    paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA, reviewDate='2026-10-12', status='reviewed',
    reviewedPaperPages=list(range(1, 21)), reviewedSchemePages=list(range(1, 18)) + [51],
    schemeScope=('Combined Paper 1 and Paper 2 scheme. PDF 1–2 cover and note; 3 listening tariffs; 4–6 listening transcript (never shown '
                 'to students); 7–11 listening answers; 12–17 composition marking, annotation symbols, Stíl/Ábhar/Gaeilge bands and S1–S4 '
                 'grades; 51 modified marking (SMM). PDF 18–50 are Paper 2; 52–56 blank or Paper 2 tables.'),
    reviewMethod=('Visual inspection of every paper page (answer-booklet pages 8–19 are ruled writing space) and every applicable scheme page; '
                  'cross-checked extracted text.'),
    audio=dict(url=AUDIO_URL, verified='2026-10-11', evidence='scripts/markbank/authored/irish-listening-audio-verification.json',
               note='One SEC recording serves the Higher and Ordinary 2024 listening test; all 2024 listening cards already play it (commit ef1a7e550).'),
    selectionDecisions=out,
    nonPoolDecisions=[
        'Listening: “Scríobh síos dhá …/Tabhair dhá …” asks for two points at 2 + 2; the scheme lists more accepted points than required. These are answer keys for one task, not task routes.',
        'Card unit for listening: the eight retained legacy segment cards (Fógra, Mír, Píosa) keep their IDs and stay the card unit, because the Bank plays one recording section as one exercise; every printed question is a separate criterion at its published 2 or 2 + 2 tariff (23 questions, 60 marks). Separate question cards are not added: they would repeat the same prompts inside that exercise.',
        'Composition: A–C is a closed choose-one; the nine printed titles were already carded as their own cards (live IDs retained). AISTE nó ALT (form) and the debate stance (ar son nó ina aghaidh) stay inside one response.',
        'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.',
    ],
    sourceFindings=[
        'Paper 1 = 160: Cuid I listening 60 (Cuid A 18 = Fógra 1 10 + Fógra 2 8; Cuid B 28 = Comhrá 1 14 (Mír 1 6 + Mír 2 8) + Comhrá 2 14 (Mír 1 8 + Mír 2 6); Cuid C 14 = Píosa 1 8 + Píosa 2 6), every question 2 marks or 2 + 2; Cuid II composition 100 (choose one of A, B, C).',
        'Listening language: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge” (scheme PDF 3 and 11) is one section-level deduction; each card states it without applying it.',
        'Píosa a hAon Q1: the scheme prints “uair an chlog” where the paper has “uair an chloig”; the card keeps the paper wording.',
        'Composition S4 (“Easnamhach”) applies only to A(c), A(d) and A(e) in 2024 (scheme PDF 17).',
        'Legacy corrections (IDs, totals and topics unchanged): each segment card had one undivided criterion; the nine composition cards carried paraphrased English marking notes and no S1–S4 grades. All now carry the lifted 2024 scheme text and per-question tariffs.',
    ],
    remainingWork=[],
)
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = []
RECORDED = {'runtimeVerification': {'date': '2026-10-12',
                         'viewport': [390, 844],
                         'markBankRoutes': 4,
                         'atlasRoutes': 5,
                         'sourceReader': 'The full listening test (first exercise Cuid A), one segment card and two composition titles rendered their paper '
                                         'page; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Segment and title routes rendered their paper page plus reviewed scheme pages (listening 1+1 and 1+2, composition 1+6); the '
                                  'frozen Cuid A section kept its original crop.',
                         'audio': 'Official SEC 2024 Higher/Ordinary recording (LC001ZLP017IV.mp3) played in Bank and Atlas, duration 1356.796719 seconds.',
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
 'audio',
 'selectionDecisions',
 'nonPoolDecisions',
 'sourceFindings',
 'remainingWork',
 'runtimeVerification']

if __name__ == '__main__':
    finish(LEDGER, 'irish-higher-2024-p1-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
