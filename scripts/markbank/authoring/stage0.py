#!/usr/bin/env python3
"""Does this subject's marking scheme print answers? Ask BEFORE anything else.

    python3 scripts/markbank/authoring/stage0.py            # every subject
    python3 scripts/markbank/authoring/stage0.py accounting --list

Geography was fetched, parsed and abandoned because roughly 80% of its paper is
answered by rubric — "Discussion 14 x SRP's" — and there is nothing in a rubric
to lift onto a card. That check cost days because it was made last. It is one
grep, so it goes first.

The measure is the priced line. A marking scheme awards marks against lines, and
each line either STATES something a student could have written, or describes the
shape of an answer and leaves the content to the examiner. Only the first kind
can become a card, because the rule of this bank is that the answer is lifted
from the scheme and never written.

The seven subjects already in the bank and the one that was rejected calibrate
the number, so a new subject is read against them rather than against a
threshold picked out of the air.
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
REPORTS = os.path.join(ROOT, 'examiner-reports')

SHIPPED = {'agricultural-science', 'biology', 'business', 'chemistry',
           'economics', 'home-economics', 'physics'}
REJECTED = {'geography'}

# THE SCORE ABOVE DECIDES NOTHING, and these four are the proof. Each was
# measured on 10-11 September 2026 by counting the marked asks and how many
# carry stated liftable content — the three re-measures because their standing
# verdicts had been recorded WITHOUT a count, Physical Education because it had
# never been assessed at all. All four score ABOVE every subject already
# shipped (52-86% against a shipped range of 28-46%), and two of them are still
# rejections. Read the counts, not the percentage.
VERDICTS = {
    'physical-education': (
        'PASSES, and its share swings hard by sitting. 824 scheme parts over '
        'the 13 sittings 2020-2026; 187 state an answer a student could have '
        'written ("Barriers may include: -Facilities -Access -Finance") and '
        '637 print a band ladder and nothing else ("Clear and accurate '
        'definition. 2 / Some accuracy in the definition. 1"). Per sitting: '
        '56% of 2021 Higher and 55% of 2024 Higher state answers, against 4% '
        'of 2025 Higher and 5% of 2025 Ordinary, so one paper decides nothing. '
        'Denominator 741 leaf asks (paper_census, merged mode). See pe_all.py.'),
    'accounting': (
        'UPHELD, now with the count the original verdict lacked. 10,097 ledger '
        'rows ("Sales 659,650 [3]") against 913 prose sentences in the answers '
        'over 34 schemes. Cut into answer RUNS: 202 prose answers, of which '
        '105 quote that paper\'s own dataset ("The dividend cover is 1.33 '
        'times. Last year\'s dividend cover was 1.4 times") and 97 are '
        'dataset-free named principle ("An adverse variance is when actual '
        'costs exceed the budgeted costs"; "When a Contingent Liability is '
        'probable, the estimated amount should be provided for in the '
        'accounts"). That is 2.85 cardable prose answers a sitting, and the '
        'ORDINARY papers print almost none — 0 in eleven of seventeen '
        'Ordinary schemes. A real fraction, but a thin one: card the theory '
        'parts only alongside a subject, not as one.'),
    'music': (
        'REJECTED, and the standing verdict was HALF wrong. Music sets three '
        'written booklets, not one, and they have to be counted separately. '
        'COMPOSING (component 006): 2,649 priced lines, of which 1,893 are '
        'band descriptors — "Excellent sense of shape and structure 38 - 40", '
        '"Quality of Bass Line 20", "Very little or no attempt 1" — and the '
        'remaining 756 are marking RULES for the candidate\'s own composition '
        '("1 mark for each chord that fits melody and descant lines", ".5 mark '
        'per correct bass note under each chord symbol", "Deduct .5 mark per '
        'note if given rhythm not used"). Neither is a stated answer: a rule '
        'for pricing what the candidate wrote is not something a student could '
        'have written. LISTENING-CORE (008): 2,219 of 2,728 priced lines (81%) '
        'state an answer — "Imperfect cadence 1", "F major 2", "Viola + Cello '
        '2 + 2", "Tierce de Picardie occurs when a piece in the minor key ends '
        'on a major tonic chord" — so "quality bands" is simply untrue of this '
        'half. It is refused on the OTHER ground instead, and the same one the '
        'eleven carded languages use: the recording IS the ask. The paper '
        'prints "Excerpt 1, played three times. (a) Identify two different '
        'instruments which play the melody in this excerpt", no audio ships in '
        'this bank today, and the printed score is a mangled glyph stream in '
        'the text layer. LISTENING-ELECTIVE (007) is a band-graded essay: "A '
        'Excellent awareness and detailed knowledge of musical features of '
        'chosen topic 10".'),
    'dcg': (
        'OVERTURNED — the strongest of the four. "A drawing subject" is true '
        'and irrelevant: the scheme states the CRITERIA, exactly as '
        'Construction Studies\' does. 4,396 priced construction steps over 33 '
        'schemes, each its own stated requirement with its own printed mark — '
        '"(i) Traces of required cutting planes parallel to HT in plan ... 3", '
        '"(iii) X1Y1 parallel to line of intersection ... 6", "(iv) Draw plan '
        'of sphere using correct radius ... 2" — under 920 priced parts. Only '
        '209 priced steps are band-like, and every one of those is the same '
        'row: "Presentation ... 2". Card it: the denominator is 66 papers and '
        'the blocker is FIGURES, not content.'),
}

# A line the scheme prices.
PRICED = re.compile(r'[\[(]\s*\d{1,3}\s*[\])]|\b\d{1,3}\s*m(?:ark)?s?\b'
                    r'|\b\d{1,2}\s*[x×]\s*\d{1,2}\b', re.I)

# A priced line that describes the shape of an answer instead of stating one.
# These are what a rubric-marked subject prints instead of an answer.
RUBRIC = re.compile(
    r'\b(srps?|significant relevant point|valid information|surplus information'
    r'|discussion|indicative (?:material|content)|graded|named example'
    r'|any valid|any correct|any suitable|any other|as above|accept any'
    r'|candidates? (?:may|might|should|will)|examiners? (?:may|should|will|must)'
    r'|credit (?:any|is|may|will)|at the discretion|not exhaustive'
    r'|aspects?\b.*\bmarks?\b|expression and (?:accuracy|coherence)'
    r'|apparatus\b|method\b|observation\b|procedure\b'
    r'|\b(?:two|three|four|five|one)\s+(?:points?|reasons?|ways?|examples?'
    r'|factors?|items?|uses?|answers?|effects?|causes?|advantages?'
    r'|disadvantages?|features?|benefits?)\b)', re.I)

# Scheme front matter and page furniture — not evidence either way.
FURNITURE = re.compile(
    r'(marking scheme|leaving certificate|coimisi|state examinations'
    r'|page \d+ of|blank page|^\s*\d+\s*$|annotation|general (?:instructions|'
    r'principles)|structure of the (?:marking scheme|examination)'
    r'|total marks|section [a-d]\s*$|^\s*\|)', re.I)


def score(path):
    concrete, rubric = [], []
    for raw in open(path, errors='ignore'):
        line = raw.strip()
        if len(line) < 12 or FURNITURE.search(line):
            continue
        if not PRICED.search(line):
            continue
        # What is left once the price and any rubric words are removed: if
        # nothing substantive survives, the line stated nothing.
        bare = PRICED.sub('', line)
        bare = re.sub(r'[^A-Za-z ]+', ' ', bare)
        bare = ' '.join(w for w in bare.split() if len(w) > 2)
        if RUBRIC.search(line) or len(bare) < 14:
            rubric.append(line)
        else:
            concrete.append(line)
    return concrete, rubric


def report(subject, show=False):
    # The full corpus lives in <subject>/schemes — five years at both levels.
    # The .md files loose in <subject>/ are the examiner-report library's own
    # partial extractions, and reading those instead put biology at 108 priced
    # lines when its schemes hold thousands. Wrong corpus, meaningless number.
    d = os.path.join(REPORTS, subject, 'schemes')
    if not os.path.isdir(d):
        return None
    files = sorted(f for f in os.listdir(d) if f.endswith('.md'))
    if not files:
        return None
    C, R = [], []
    for f in files:
        c, r = score(os.path.join(d, f))
        C += c
        R += r
    total = len(C) + len(R)
    if not total:
        return None
    pct = len(C) * 100 // total
    tag = ' (shipped)' if subject in SHIPPED else (
        ' (REJECTED)' if subject in REJECTED else '')
    print(f'{subject:<22}{pct:>4}% stated   {len(C):>5} stated  {len(R):>5} rubric'
          f'   {len(files)} scheme(s){tag}')
    if show:
        print('\n  -- stated ' + '-' * 60)
        for line in C[:12]:
            print(f'   {line[:150]}')
        print('\n  -- rubric ' + '-' * 60)
        for line in R[:12]:
            print(f'   {line[:150]}')
    return pct


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show = '--list' in sys.argv
    targets = args or sorted(os.listdir(REPORTS))
    rows = {}
    for s in targets:
        if not os.path.isdir(os.path.join(REPORTS, s)):
            continue
        p = report(s, show and len(targets) == 1)
        if p is not None:
            rows[s] = p
    if len(rows) > 1:
        ship = [rows[s] for s in rows if s in SHIPPED]
        rej = [rows[s] for s in rows if s in REJECTED]
        print('\n  --- calibration ---')
        if ship:
            print(f'  shipped subjects  : {min(ship)}%–{max(ship)}% stated')
        if rej:
            print(f'  rejected (geography): {rej[0]}% stated')
        print('\n  --- ranked, subjects not yet in the bank ---')
        for s, p in sorted(rows.items(), key=lambda kv: -kv[1]):
            if s not in SHIPPED and s not in REJECTED:
                print(f'  {p:>3}%  {s}')
