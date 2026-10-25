#!/usr/bin/env python3
"""Geography citation gate: check every card's cited question against the PAPER.

The Geography census is built from the review ledgers, so reconcile.py's zero
orphans cannot catch a card citing the wrong question. This reads the paper:
for each card it finds the question text on the cited paper page and the
nearest printed question heading before it ("Question 7" then "A.", "9C.",
"4."). The card's questionRef must name that question and letter, and a card
whose text opens with a printed roman must cite that roman (a whole-question
card that prints every roman cites the question).

    python3 scripts/markbank/authoring/geography_refcheck.py   # exit 1 on any mismatch
"""
import json
import os
import re
import sys
from collections import defaultdict

import geography_review as GR

CARDS = json.load(open(os.path.join(GR.ROOT, 'components', 'MarkBank', 'cards', 'geography',
                                    'authored.json'), encoding='utf-8'))['cards']
REF = re.compile(r'^(\d{4}) (HL|OL) Part ([12]) Q(\d+)([ABC])?(?:\(([ivx]+)\))?')
QUESTION = re.compile(r'^Question\s+(\d{1,2})$')
NUM_LETTER = re.compile(r'^(\d{1,2})([ABC])\.(?:\s|·|$)')
LETTER = re.compile(r'^([ABC])\.(?:\s|·|$)')
NUMBER = re.compile(r'^(\d{1,2})\.(?:\s|·|$)')
ROMAN = re.compile(r'^\(([ivx]+)\)')


def norm(text):
    # The generator displays "km2" as "km²" and "(oC)" as "(°C)".
    text = text.replace('²', '2').replace('°', 'o')
    return re.sub(r'[^a-z0-9]', '', text.lower())


sittings = {}
lines_cache = {}


def page_lines(year, level, part, page):
    key = (year, level, part, page)
    if key not in lines_cache:
        if (year, level) not in sittings:
            sittings[(year, level)] = GR.Sitting.open(year, level)
        doc = sittings[(year, level)].papers[part]
        lines_cache[key] = doc.lines(page) if page <= len(doc.doc) else []
    return lines_cache[key]


def headings_before(year, level, part, page, upto):
    """(question, letter) in force at line ``upto`` of ``page``."""
    q, letter = None, None
    # Page 1 is the cover, whose mark grid prints "Question 1" ... "Question 12".
    for pg in range(2, page + 1):
        lines = page_lines(year, level, part, pg)
        # The heading may share the matched line ("13. · Discuss ...").
        stop = upto + 1 if pg == page else len(lines)
        for line in lines[:stop]:
            # Answer lines ("1. ____", "A. ____") are not headings.
            if '___' in line:
                continue
            m = QUESTION.match(line)
            if m:
                q, letter = int(m.group(1)), None
                continue
            # Question numbers run in sequence; a map's numbered labels
            # ("1. Belgium") or a printed list do not.
            m = NUM_LETTER.match(line)
            if m and (q or 0) <= int(m.group(1)) <= (q or 0) + 1:
                q, letter = int(m.group(1)), m.group(2)
                continue
            m = LETTER.match(line)
            if m:
                letter = m.group(1)
                continue
            m = NUMBER.match(line)
            if m and int(m.group(1)) == (q or 0) + 1:
                q, letter = int(m.group(1)), None
    return q, letter


def locate(lines, text):
    """Index of the line where ``text`` starts (normalised), or candidates."""
    target = norm(text)[:60]
    joined, starts = '', []
    for line in lines:
        starts.append(len(joined))
        joined += norm(line)
    hits = [m.start() for m in re.finditer(re.escape(target), joined)] if target else []
    out = []
    for hit in hits:
        index = max(i for i, s in enumerate(starts) if s <= hit)
        out.append(index)
    return out


problems = defaultdict(list)
checked = 0
for card in CARDS:
    m = REF.match(card['questionRef'])
    if not m:
        problems['unparsed-ref'].append((card['id'], card['questionRef']))
        continue
    year, lvl, part, q, letter, roman = m.groups()
    year, part, q = int(year), int(part), int(q)
    level = 'higher' if lvl == 'HL' else 'ordinary'
    first = card['questionText'].split('\n')[0]
    lines = page_lines(year, level, part, card['paperPage'])
    hits = locate(lines, first)
    if not hits and ROMAN.match(first):
        # Some pages print the roman after its text in the text layer
        # ("Name the island at A ..." then "(i)"); match the text alone.
        hits = locate(lines, ROMAN.sub('', first, count=1))
    if not hits:
        problems['text-not-on-cited-page'].append((card['id'], card['questionRef'], card['paperPage'], first[:70]))
        continue
    found = {headings_before(year, level, part, card['paperPage'], hit) for hit in hits}
    if (q, letter) not in found:
        problems['question-mismatch'].append((card['id'], card['questionRef'], sorted(found, key=str), first[:60]))
        continue
    rm = ROMAN.match(first)
    if rm and roman and rm.group(1) != roman:
        problems['roman-mismatch'].append((card['id'], card['questionRef'], first[:60]))
        continue
    # A whole-question card that prints every roman ((i) and (ii)) cites the question.
    whole = len(set(re.findall(r'(?m)^\(([ivx]+)\)', card['questionText']))) > 1
    if rm and not roman and not whole and f'({rm.group(1)})' not in card['questionRef']:
        problems['roman-uncited'].append((card['id'], card['questionRef'], first[:60]))
        continue
    checked += 1

print(f'{len(CARDS)} cards; {checked} citations agree with the paper')
for kind, rows in problems.items():
    print(f'== {kind}: {len(rows)}')
    for row in rows:
        print('  ', row)
sys.exit(1 if problems else 0)
