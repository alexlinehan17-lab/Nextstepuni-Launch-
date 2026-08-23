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
