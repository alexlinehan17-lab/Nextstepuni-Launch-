#!/usr/bin/env python3
"""Rebuild irish-ordinary-2024-p2-source-review.json from the official paper (see _ledger.py).

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
"""Write the 2024 Ordinary Paper 2 source-review ledger: every raw directive line classified."""
import sys, json, hashlib
ROOT = str(_REPO)
sys.path.insert(0, ROOT + '/scripts/markbank/authoring')
import fitz
from irish_ordinary_2024_p2 import DIRECTIVE, clean, PAPER_SHA, SCHEME_SHA

P = ROOT + '/paper-trail-corpus/exampapers/2024/LC001GLP200IV.pdf'
assert hashlib.sha256(open(P, 'rb').read()).hexdigest() == PAPER_SHA
assert hashlib.sha256(open(ROOT + '/paper-trail-corpus/markingschemes/2024/LC001GLP000IV.pdf', 'rb').read()).hexdigest() == SCHEME_SHA
lines = []
for i, page in enumerate(fitz.open(P), 1):
    for line in page.get_text().splitlines():
        raw = clean(line)
        if DIRECTIVE.search(raw) and (i, raw) not in lines:
            lines.append((i, raw))
REQ = 'Required answers; no finite task menu.'
BOTH = 'Both reading passages and every question in each are required; each printed (a)/(b) part is also a 5-mark practice card.'
PASSAGE = 'Source-text wording inside a reading passage or poem, not a candidate instruction.'
COPY = 'Copyright statement, not a task.'
Q2 = ('Closed choice: Q2A (Prós Ainmnithe) or Q2B (Prós Roghnach), then any two of (a), (b), (c). Choice is not a route: each printed '
      'option is its own whole 25-mark card carrying this instruction in its task requirements; no combination cards.')
Q3 = ('Closed choice: Q3A (Filíocht Ainmnithe) or Q3B (Filíocht Roghnach), then any two of (a), (b), (c). Choice is not a route: each of the six '
      'printed options is its own whole 25-mark card carrying this instruction in its task requirements; no combination cards.')
SUMMARY = ('Printed four times in the instructions box (under 2A, 2B, 3A and 3B): within the chosen section any two of (a), (b), (c); repeated on '
           'pages 8, 9, 10 and 13. “nó” separates 2A from 2B and 3A from 3B (alternatives, never combined).')
TWO35 = 'Two required points inside one printed reading part priced 3 mharc + 2 mharc (first correct 3, second 2): the part stays whole at 0/3/5.'
TWOLIT = ('Two required points inside one printed literature sub-question; the scheme prices them together (3 + 2, 4 + 4, or opinion 1 + reasons), '
          'so the sub-question card is the smallest printed unit.')
OPT = 'Required content inside one optional route (open text chosen by the candidate); kept whole with its title marks.'
RESTRICT = 'Restriction on content, not a route.'
SAME = 'Restriction on the 3B choice: the same optional poem may not be used twice. It is stated in every 3B option’s task requirements.'
OPTION = 'Names one printed option inside the closed choice; the option is one whole 25-mark card with its printed sub-questions as practice cards.'
C2A = ('Choose-one inside 2A(c): the film Cáca Milis or the play An Lasair Choille. Different syllabus texts (topics irish-4-6 and irish-4-8) with '
       'their own sample answers, so each is its own 25-mark card (the legacy 2A(c) card is Cáca Milis; An Lasair Choille is added).')
C2B = ('Choose-one inside 2B(c): an optional film or an optional play. Same grid (23 + 2) and same topic (optional prose), so one card carries both '
       'printed alternatives.')


def decide(p, r):
    if p == 3:
        if r.startswith('FREAGAIR GACH'):
            return REQ
        if r.startswith('Freagair Léamhthuiscint'):
            return BOTH
        if r.startswith('Freagair 2A') or r.startswith('2B. Prós'):
            return Q2
        if r.startswith('Freagair 3A') or r.startswith('3B. Filíocht'):
            return Q3
        if r == 'nó' or r.startswith('Freagair do rogha'):
            return SUMMARY
    if p == 4 and r == 'Freagair A agus B anseo.':
        return BOTH
    if p in (4, 6) and r.startswith('Léigh an sliocht'):
        return BOTH
    if p in (4, 6, 7) and not r.startswith(('(a)', '(b)', '2.', '3.', '4.', '5.')):
        return PASSAGE
    if p in (5, 7):
        if r.startswith('(b) Cén sórt duine a roghnaíodh'):
            return 'Question wording (“roghnaíodh” = was chosen), one required answer; not a selection.'
        return TWO35
    if p == 8:
        if r.startswith('Freagair an cheist thíos faoin scannán Cáca Milis') or r == 'nó':
            return C2A
        if r.startswith('Freagair na ceisteanna thíos'):
            return OPTION
        if r.startswith(('Luaigh', 'Tabhair', 'Scríobh')):
            return TWOLIT
        return Q2
    if p == 9:
        if r.startswith('Níl cead'):
            return RESTRICT
        if r.startswith('Freagair an cheist thíos faoin scannán roghnach') or r == 'nó':
            return C2B
        if r.startswith('Maidir le'):
            return OPT
        return Q2
    if p == 10:
        if r.startswith('Freagair') or r.startswith('Ceist 3'):
            return Q3
        return TWOLIT
    if p in (11, 12):
        return TWOLIT
    if p == 13:
        if r.startswith('Níl cead aon ábhar'):
            return RESTRICT
        if r.startswith('Níl cead an dán'):
            return SAME
        if r.startswith('Freagair do rogha') or r.startswith('3B FILÍOCHT'):
            return Q3
        return OPT
    if p == 16:
        return COPY
    raise SystemExit(f'Unclassified directive: {p} {r}')


out = [dict(page=p, raw=r, decision=decide(p, r)) for p, r in lines]
ledger = dict(
    year=2024, level='ordinary', paperFileid='LC001GLP200IV.pdf', schemeFileid='LC001GLP000IV.pdf',
    paperSha256=PAPER_SHA, schemeSha256=SCHEME_SHA, reviewDate='2026-10-12', status='reviewed',
    reviewedPaperPages=list(range(1, 17)), reviewedSchemePages=list(range(14, 34)),
    schemeScope=('Combined Ordinary scheme. PDF 14 Paper 2 notes and reading annotation key; 15–16 Léamhthuiscint A; 17–18 Léamhthuiscint B; '
                 '19 literature annotation key; 20–24 Prós Ainmnithe (2A); 25–26 Prós Roghnach (2B); 27–30 Filíocht Ainmnithe (3A); 31–32 '
                 'Filíocht Roghnach (3B); 33 modified marking (SMM; 34 is its Paper 1 table). PDF 1–13 belong to Paper 1; 35–36 are blank.'),
    reviewMethod=('Visual inspection of every paper page (pages 1–3 cover/instructions, 14–15 blank, 16 acknowledgements) and every applicable '
                  'scheme page; cross-checked extracted text.'),
    selectionDecisions=out,
    nonPoolDecisions=[
        'Reading: all ten questions are required; each printed (a)/(b) part is a 5-mark practice card. “3 mharc + 2 mharc” items are order-dependent '
        '(first correct point 3, second 2) and stay whole at 0/3/5; single answers with a printed partial (“= 3 mharc”) allow 0/3/5, otherwise 0/5.',
        'Reading language: “Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh” is one deduction from each 50-mark passage total; cards state '
        'it without applying it inside a part.',
        'Prescribed prose (2A): Dís (a) and Oisín i dTír na nÓg (b) each print five 5-mark sub-questions: each whole option is a 25-mark card and '
        'every sub-question is also a practice card (“3 mharc + 2 mharc” sub-questions keep 0/3/5). 2A(c) is a choose-one between two texts: '
        'Cáca Milis and An Lasair Choille are separate 25-mark cards (different topics).',
        'Prescribed poetry (3A): each poem is a whole 25-mark card with (i) 8, (ii) 8, (iii) 9 and one 0–4 Gaeilge deduction; every printed '
        'sub-question is also a practice card. 3A(b)(i) prints four 2-mark questions (a)–(d): each is a practice slot (0/2).',
        'Literature mark values: other literature sub-questions keep the full range because the scheme’s points are indicative and further '
        'relevant points are credited “de réir a bhfiúntais”.',
        'Optional prose (2B) and optional poetry (3B) stay whole: the text is open content chosen by the candidate. 2B(c) film or play shares one '
        'grid and one topic, so it stays one card with both printed alternatives.',
        'Choose-two within 2A, 2B, 3A or 3B is a choice, not a route: each printed option keeps its own card and carries the instruction in its '
        'task requirements; no combination cards. The scheme marks each option on its own (no joint marking).',
        'Q2A or Q2B and Q3A or Q3B are alternatives; scheme lists of sample answers are indicative answer keys, not route pools.',
        'The modified marking scheme (PDF 33) changes language assessment for eligible candidates, not the printed tasks.',
    ],
    sourceFindings=[
        'Paper 2 = 200: Léamhthuiscint A 50 + B 50 (five questions of 10, each (a) 5 + (b) 5), Prós 50 (two of three at 25), Filíocht 50 '
        '(two of three at 25).',
        'Reading A “Oileán agus Ionad an Bhlascaoid Mhóir” (paper pages 4–5, scheme PDF 15–16) and B “Mearfhaisean” (paper 6–7, scheme PDF 17–18).',
        'Prescribed prose (paper 8): Dís (i)–(v) and Oisín i dTír na nÓg (i)–(v) at 5 each; Cáca Milis or An Lasair Choille one 25-mark question '
        '(five points at 2 + 3). Optional prose (paper 9): (a) theme 1 + 22 + title/author 2; (b) naming 1 + 22 + title 2; (c) film or play 23 '
        '(5,5,5,4,4) + title/writer 2.',
        'Prescribed poetry (paper 10–12): Colscaradh, An Spailpín Fánach ((i) four 2-mark questions), Géibheann at 8/8/9. Optional poetry (paper 13): '
        '(a) 9 (5 + 4) / 7 (1 + 3 + 3) / 7, (b) 9 (1 + 4 + 4) / 7 / 7, (c) 9 / 7 / 7, + 2 for poem and poet; the same poem may not be used twice.',
        'Literature language: “[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]” after every literature answer; it is a deduction from that '
        'answer, never inside one sub-question.',
        'The legacy cards marked every literature answer as one 25-mark Eolas block and every reading question as one 10-mark block; the 2A(c) card '
        'carried both texts. They now carry the printed part and sub-question tariffs, and 2A(c) is Cáca Milis.',
    ],
    remainingWork=[],
)
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = []
RECORDED = {'runtimeVerification': {'date': '2026-10-12',
                         'viewport': [390, 844],
                         'markBankRoutes': 5,
                         'atlasRoutes': 5,
                         'sourceReader': 'A retained whole reading question, a Dís sub-question, the An Lasair Choille option, the 2B(c) film-or-play card and '
                                         'a 3A(b)(i) question rendered their paper pages; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Each route rendered its paper pages plus reviewed scheme pages (frozen reading Ceist 2 2+1, Cáca Milis 1+2, An Lasair '
                                  'Choille 1+3, 2B(c) 1+1, 3A(b)(i) 1+2).',
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
 'nonPoolDecisions',
 'sourceFindings',
 'remainingWork',
 'runtimeVerification']

if __name__ == '__main__':
    finish(LEDGER, 'irish-ordinary-2024-p2-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
