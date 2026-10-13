#!/usr/bin/env python3
"""Rebuild irish-ordinary-2023-p1-source-review.json from the official paper (see _ledger.py).

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
"""Write the 2023 Ordinary Paper 1 source-review ledger: every raw directive line classified."""
import sys, json, hashlib
ROOT = str(_REPO)
sys.path.insert(0, ROOT + '/scripts/markbank/authoring')
import fitz
from irish_ordinary_2023_p1 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA

P = ROOT + '/paper-trail-corpus/exampapers/2023/LC001GLP100IV.pdf'
assert hashlib.sha256(open(P, 'rb').read()).hexdigest() == PAPER_SHA
assert hashlib.sha256(open(ROOT + '/paper-trail-corpus/markingschemes/2023/LC001GLP000IV.pdf', 'rb').read()).hexdigest() == SCHEME_SHA
lines = []
for i, page in enumerate(fitz.open(P), 1):
    for line in page.get_text().splitlines():
        raw = clean(line)
        if DIRECTIVE.search(raw) and (i, raw) not in lines:
            lines.append((i, raw))
COMP = ('Closed choose-two of sections A–D, each section offering printed titles (A 3, B 2, C 2, D 2): 9 whole 50-mark title cards, each marked '
        'on its own 50. Choice is not a route: no two-section combination cards; the instruction is in each title card’s task requirements.')
FORM = ('Required form wording inside one composition (giota leanúnach nó blag; litir/ríomhphost; deartháir/deirfiúr; dó/di; uaidh/uaithi; cara or tuismitheoirí); not a separate card.')


def decide(p, r):
    if p == 2 and r.startswith('Scríobh do chuid'):
        return 'Pen colour instruction, not an answer route.'
    if p == 2:
        return 'Paper structure statement: both parts required.'
    if p == 3 and (r.startswith('Freagair gach cuid') or r.startswith('Caithfidh do chuid')):
        return 'Required answers; no finite task menu.'
    if r.startswith('Cloisfidh tú') or r.startswith('an comhrá ó thosach'):
        return 'Required listening section structure.'
    if p == 3 and r.startswith('Luaigh dhá áit'):
        return 'Two required places priced 3 mharc + 3 mharc inside one printed question; the scheme’s list is the answer key for one task.'
    if p in (3, 4) and 'amháin' in r:
        return 'One required answer; the accepted list is the answer key for one task.'
    if p == 6:
        return 'Instruction to keep the chosen title connected; selection classified on page 7.'
    if p == 7 and (r.startswith('Freagair do rogha') or r.startswith('Scríobh giota') or r.startswith('Ceap scéal') or r == 'nó'):
        return COMP
    if p == 7 and r.startswith('Tá tairiscintí CAO'):
        return 'Task wording (“do chéad rogha” = your first CAO choice) inside D(ii); not a selection.'
    if p == 7:
        return FORM
    if p == 16:
        return 'Copyright statement, not a task.'
    raise SystemExit(f'Unclassified directive: {p} {r}')


out = [dict(page=p, raw=r, decision=decide(p, r)) for p, r in lines]
ledger = dict(
    year=2023, level='ordinary', paperFileid='LC001GLP100IV.pdf', schemeFileid='LC001GLP000IV.pdf',
    paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA, reviewDate='2026-10-13', status='reviewed',
    reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=list(range(1, 14)) + [33, 34],
    schemeScope=('Combined Ordinary scheme. PDF 1–2 cover and note; 3 listening tariffs; 4–6 transcript (never shown to students); 7–9 listening '
                 'answers; 10–13 composition marking, symbols, 40-mark table and short-attempt columns; 33–34 modified marking (SMM, incl. the '
                 'composition 40-mark table). PDF 14–32 are Paper 2; 35–36 blank.'),
    reviewMethod=('Visual inspection of every paper page (1 cover with the COVID-19 adjustment note; answer-booklet pages 8–15 are ruled writing space) and every applicable scheme page; '
                  'cross-checked extracted text.'),
    audio=dict(url='https://www.examinations.ie/archive/exampapers/2023/LC001ZLP017IV.mp3', verified='2026-10-11',
               evidence='scripts/markbank/authored/irish-listening-audio-verification.json',
               note='One SEC recording serves the Higher and Ordinary 2023 listening test; Ordinary asks different questions on the same extracts. All 2023 listening cards already play it (commit ef1a7e550).'),
    selectionDecisions=out,
    nonPoolDecisions=[
        'Listening answers with alternatives (e.g. Hallaí na léachtaí / Na saotharlanna eolaíochta / An leabharlann / An t-ionad spóirt) are accepted answers to one task, not routes.',
        'Card unit for listening: the six retained legacy segment cards keep their IDs and stay the card unit, because the Bank plays one recording section as one exercise; every printed question is a separate criterion (19 questions: eighteen at 3 and Fógra a Dó Ceist 2 at 3 + 3; 60 marks). Separate question cards are not added: they would repeat the same prompts inside that exercise.',
        'Composition: closed choose-two of four sections; each printed title is a 50-mark card (already carded, IDs retained). Choice is not a route: no two-section combination cards are published; the choose-two instruction is in each title card’s task requirements. Letter/email, recipient (deartháir/deirfiúr) and conversation partner wording stay inside one response.',
        'The modified marking scheme changes assessment for eligible candidates, not the printed tasks.',
    ],
    sourceFindings=[
        'Paper 1 = 160: listening 60 (Cuid A 24, B 24, C 12; every question 3 marks except Fógra a Dó Ceist 2 at 3 + 3) and composition 100 (any two of A–D at 50: Tasc 2, Ábhar 8, Cumas Gaeilge 40).',
        'Listening language: “Bainfear ó 0 go 6 ar chaighdeán na Gaeilge” (scheme PDF 3 and 9) is one section-level deduction; cards state it without applying it. Printed partial answers (2 mharc): Scéal/scéalta, Halla(í), Saotharlann(a), Ionad, (Ag) féile, Bruscar, Páirc, (Ar an) raidió, 2022, An bhliain seo caite, Mí na Nollag.',
        'Cover (PDF 1, printed as an image): the 2023 papers were adjusted to compensate for COVID-19 learning disruption. The cards follow the printed 2023 structure; the note offers no choice.',
        'Composition 40-mark table (PDF 12) with short-attempt columns M/F1/F2/F3 (36/30/20/10, PDF 13); those columns include odd values, so the Cumas Gaeilge award takes any value 0–40.',
        'Legacy corrections (IDs, totals and topics unchanged): each segment card had one undivided criterion; the nine composition cards carried short paraphrased notes. All now carry the lifted 2023 scheme text and per-question tariffs.',
    ],
    remainingWork=[],
)
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = []
RECORDED = {'runtimeVerification': {'date': '2026-10-13',
                         'viewport': [390, 844],
                         'markBankRoutes': 4,
                         'atlasRoutes': 4,
                         'sourceReader': 'The full Ordinary listening test (first exercise Cuid A), the Fógra a Dó segment (3 + 3 question) and two '
                                         'composition titles rendered their paper page; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Segment and title routes rendered their paper page plus reviewed scheme pages (listening 1+1, composition 1+4); the frozen '
                                  'Cuid A section kept its original crop.',
                         'audio': 'Official SEC 2023 Higher/Ordinary recording (LC001ZLP017IV.mp3) played in Bank and Atlas, duration 1398.912031 seconds.',
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
    finish(LEDGER, 'irish-ordinary-2023-p1-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
