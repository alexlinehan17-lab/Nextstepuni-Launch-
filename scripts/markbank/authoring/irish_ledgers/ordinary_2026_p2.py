#!/usr/bin/env python3
"""Rebuild irish-ordinary-2026-p2-source-review.json from the official paper (see _ledger.py).

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
import sys, re, json, hashlib
ROOT=str(_REPO)
sys.path.insert(0, ROOT+'/scripts/markbank/authoring')
import fitz
from irish_ordinary_2026_p2 import DIRECTIVE, clean
paper=fitz.open(ROOT+'/paper-trail-corpus/exampapers/2026/LC001GLP200IV.pdf')
lines=[(i,clean(l)) for i,p in enumerate(paper,1) for l in p.get_text().splitlines() if DIRECTIVE.search(clean(l))]
lines=list(dict.fromkeys(lines))
REQ='Required answers; no finite task menu.'
BOTH='Both reading passages and every question in each are required; each printed (a)/(b) part is also a 5-mark practice card.'
PASSAGE='Source-text wording inside a reading passage or poem, not a candidate instruction.'
COPY='Copyright statement, not a task.'
Q2='Closed choice: Q2A (Prós Ainmnithe) or Q2B (Prós Roghnach), then any two of (a), (b), (c); 2A(a) offers Cáca Milis or An Lasair Choille and 2B(a) a film or a play. Eight whole 25-mark routes; two routes from different letters make each 50-mark selection (2A 5, 2B 5).'
Q3='Closed choice: Q3A (Filíocht Ainmnithe) or Q3B (Filíocht Roghnach), then any two of (a), (b), (c). Six whole 25-mark routes; two routes from different letters make each 50-mark selection (3A 3, 3B 3).'
HEAD='Section heading / structure statement, not a separate route.'
TWO35='Two required points inside one printed sub-question priced 3 mharc + 2 mharc (first correct 3, second 2): the part stays whole at 0/3/5.'
TWOLIT='Two required points inside one printed literature sub-question; the scheme prices them together (3 + 2, 4 + 4, or opinion 1 + reasons), so the sub-question card is the smallest printed unit.'
OPT='Required content inside one optional route (open text chosen by the candidate); kept whole with its title marks.'
RESTRICT='Restriction on content, not a route.'
SAME='Restriction recorded on every 3B selection: the same optional poem may not be used twice.'
def decide(p,r):
    if p==3:
        if r.startswith('FREAGAIR GACH'): return REQ
        if r.startswith('Freagair Léamhthuiscint'): return BOTH
        if '2A (Prós' in r or r=='2B. Prós Roghnach (leathanach 9)': return Q2
        if '3A (Filíocht' in r or r=='3B. Filíocht Roghnach (leathanach 13)': return Q3
        if r=='nó' or r.startswith('Freagair do rogha'): return 'Printed four times on the instructions page (under 2A, 2B, 3A and 3B): within the chosen section any two of (a), (b), (c); expanded on pages 8, 9, 10 and 13. “nó” separates 2A from 2B and 3A from 3B (alternatives, never combined).'
    if p in (4,6) and r.startswith('Léigh an sliocht'): return BOTH
    if p==4 and r=='Freagair A agus B anseo.': return BOTH
    if p in (5,6) and (r.startswith('Ní Churraoin') or r.startswith('Caroline')): return PASSAGE
    if p in (5,7): return TWO35
    if p==8:
        if r.startswith('Ceist 2') or r.startswith('Freagair 2A') or r.startswith('Freagair do rogha') or r.startswith('Freagair na ceisteanna thíos faoin scannán') or r=='nó': return Q2
        if r.startswith('Freagair an cheist thíos faoin ngearrscéal') or r.startswith('Freagair na ceisteanna thíos faoin ngiota'): return Q2
        return TWOLIT
    if p==9:
        if r.startswith('Níl cead'): return RESTRICT
        if r.startswith('Maidir le'): return OPT
        return Q2
    if p==10:
        if r.startswith('Freagair') or r.startswith('Ceist 3'): return Q3
        return TWOLIT
    if p==11 and r.startswith('Cliabh'): return PASSAGE
    if p in (11,12): return TWOLIT
    if p==13:
        if r.startswith('Níl cead aon ábhar'): return RESTRICT
        if r.startswith('Níl cead an dán'): return SAME
        if r.startswith('Freagair do rogha') or r.startswith('3B FILÍOCHT'): return Q3
        return OPT
    if p==16: return COPY
    return None
out=[]
for p,r in lines:
    d=decide(p,r)
    if d is None:
        # page-3 summary box lines
        d = Q2 if (p==3 and lines.index((p,r)) < [x for x in lines].index((3,'Freagair 3A (Filíocht Ainmnithe) nó 3B (Filíocht Roghnach).'))) else Q3
    out.append(dict(page=p, raw=r, decision=d))
paper_sha=hashlib.sha256(open(ROOT+'/paper-trail-corpus/exampapers/2026/LC001GLP200IV.pdf','rb').read()).hexdigest()
scheme_sha=hashlib.sha256(open(ROOT+'/paper-trail-corpus/markingschemes/2026/LC001GLP100IV.pdf','rb').read()).hexdigest()
ledger=dict(
 year=2026, level='ordinary', paperFileid='LC001GLP200IV.pdf', schemeFileid='LC001GLP100IV.pdf',
 paperSha256=paper_sha, schemeSha256=scheme_sha, reviewDate='2026-10-11', status='reviewed',
 reviewedPaperPages=list(range(1,17)), reviewedSchemePages=list(range(14,35)),
 schemeScope='Combined Ordinary scheme. PDF 14 Paper 2 general notes and reading annotation key; 15–16 Léamhthuiscint A; 17–18 Léamhthuiscint B; 19 literature annotation key; 20–25 Prós Ainmnithe (2A); 26–27 Prós Roghnach (2B); 28–31 Filíocht Ainmnithe (3A); 32–33 Filíocht Roghnach (3B); 34 modified marking (SMM). PDF 1–13 and 35–40 belong to Paper 1 or are blank.',
 reviewMethod='Visual inspection of every paper page (pages 1–3 cover/instructions, 14–16 blank/acknowledgements) and every applicable scheme page; cross-checked extracted text.',
 selectionDecisions=out,
 nonPoolDecisions=[
  'Reading: all ten questions are required; each printed (a)/(b) part is a 5-mark practice card. “3 mharc + 2 mharc” items are order-dependent (first correct point 3, second 2) and stay whole at 0/3/5; single answers with a printed partial (“= 3 mharc”) allow 0/3/5, otherwise 0/5.',
  'Reading language: “Gaeilge lochtach: 0 - 5 a bhaint den iomlán a gnóthaíodh” is one deduction from each 50-mark passage total; cards state it without applying it inside a part.',
  'Prescribed prose and poetry: each printed text is a whole 25-mark route with its own sub-question tariffs and one 0–4 Gaeilge deduction; every printed sub-question is also a practice card at its own tariff. 3A(b)(i) prints four 2-mark questions (a)–(d): each is a practice slot (0/2, “Freagra:” keys with no printed partial).',
  'Literature mark values: “3 mharc + 2 mharc” sub-questions keep 0/3/5; other literature sub-questions keep the full range because the scheme’s points are indicative and further relevant points are credited “de réir a bhfiúntais”.',
  'Optional prose (2B) and optional poetry (3B) routes stay whole: the text is open content chosen by the candidate, and the title/author marks (2) belong to the whole answer.',
  'Choose-two within 2A, 2B, 3A or 3B is expanded mechanically into every two-route selection from different letters (2A 5, 2B 5, 3A 3, 3B 3 = 16). Alternatives inside one letter (Cáca Milis or An Lasair Choille; film or play) are never combined with each other.',
  'Q2A or Q2B and Q3A or Q3B are alternatives: selections never mix 2A with 2B or 3A with 3B.',
  'Scheme lists of sample answers are indicative answer keys, not route pools.',
  'The modified marking scheme (PDF 34) changes assessment for eligible candidates, not the printed tasks.',
 ],
 sourceFindings=[
  'Paper 2 = 200: Léamhthuiscint A 50 + B 50 (five questions of 10, each (a) 5 + (b) 5), Prós 50 (two of three at 25), Filíocht 50 (two of three at 25).',
  'Reading A “Pobal Ráth Chairn” (paper pages 4–5, scheme PDF 15–16) and B “The Corrs – Clann cheolmhar cháiliúil” (paper 6–7, scheme PDF 17–18).',
  'Prescribed prose (paper 8): Cáca Milis / An Lasair Choille (i)–(v) at 5 each; Dís one 25-mark question (five points at 5 = 2 + 3); Hurlamaboc (i)–(v) at 5. Optional prose (paper 9): 23 for the account (5,5,5,4,4) + 2 for title and writer/author.',
  'Prescribed poetry (paper 10–12): Géibheann, An tEarrach Thiar, An Spailpín Fánach at 8/8/9; An tEarrach Thiar (i) is four 2-mark questions. Optional poetry (paper 13): (a) 9/7/7, (b) 9/7/7, (c) 9/7/7, + 2 for poem and poet each; the same poem may not be used twice.',
  'Literature language: “[Gaeilge lochtach: 0-4 a bhaint den iomlán a gnóthaíodh]” after every literature route; it is a deduction from that route, applied once.',
 ],
 remainingWork=[],
)
LEDGER = ledger

# Later, dated edits (see _ledger.py).
AMENDMENTS = [('Closed choice: Q2A (Prós Ainmnithe) or Q2B (Prós Roghnach), then any two of (a), (b), (c); 2A(a) offers Cáca Milis or An Lasair Choille and 2B(a) a film or '
  'a play. Eight whole 25-mark routes; two routes from different letters make each 50-mark selection (2A 5, 2B 5).',
  'Closed choice: Q2A (Prós Ainmnithe) or Q2B (Prós Roghnach), then any two of (a), (b), (c); 2A(a) offers Cáca Milis or An Lasair Choille (different texts '
  'and Atlas headings: one card each) and 2B(a) a film or a play (one grid and one Atlas heading: one card carrying both). Seven whole 25-mark option cards; '
  'each is its own card; no combination cards (choice is not a route).'),
 ('Closed choice: Q3A (Filíocht Ainmnithe) or Q3B (Filíocht Roghnach), then any two of (a), (b), (c). Six whole 25-mark routes; two routes from different '
  'letters make each 50-mark selection (3A 3, 3B 3).',
  'Closed choice: Q3A (Filíocht Ainmnithe) or Q3B (Filíocht Roghnach), then any two of (a), (b), (c). Six whole 25-mark routes; each route is its own card; no '
  'combination cards (choice is not a route).'),
 ('Restriction recorded on every 3B selection: the same optional poem may not be used twice.',
  'Restriction printed in every 3B route’s prompt: the same optional poem may not be used twice.'),
 ('Choose-two within 2A, 2B, 3A or 3B is expanded mechanically into every two-route selection from different letters (2A 5, 2B 5, 3A 3, 3B 3 = 16). '
  'Alternatives inside one letter (Cáca Milis or An Lasair Choille; film or play) are never combined with each other.',
  'Choose-two within 2A, 2B, 3A or 3B is a choice, not a route: each printed route keeps its own 25-mark card and carries the instruction in its task '
  'requirements; no two-route combination cards are published. Alternatives inside one letter are decided by the Atlas mapping: Cáca Milis and An Lasair '
  'Choille file under different headings and keep one card each; the optional film and play file under one heading and share one card that carries both '
  'printed alternatives.')]
RECORDED = {'runtimeVerification': {'date': '2026-10-11',
                         'viewport': [390, 844],
                         'markBankRoutes': 7,
                         'atlasRoutes': 6,
                         'sourceReader': 'Whole reading question and one reading part (passage pages 4–5 / 6–7, swiped to the last page), a prescribed prose '
                                         'route, an optional play route, a 3A(b)(i) two-mark slot, a 3B selection and a 2A selection rendered their paper '
                                         'pages; navigation, close/focus return and overflow checks passed.',
                         'atlas': 'Each route rendered its paper pages plus its reviewed scheme pages (reading 2+1 and 2+2, 2A selection 1+3, 3A(b) 1+2, 3B(c) '
                                  '1+1, generic Question 2 with 7 scheme pages).',
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
    finish(LEDGER, 'irish-ordinary-2026-p2-source-review.json', AMENDMENTS, RECORDED, KEY_ORDER)
