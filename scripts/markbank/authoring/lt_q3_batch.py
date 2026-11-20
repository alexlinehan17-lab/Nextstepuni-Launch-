#!/usr/bin/env python3
"""Add one Lithuanian sitting's new cards to the bank (languages-q3 lane).

    python3 scripts/markbank/authoring/lt_q3_batch.py review 2026 hl listening
    python3 scripts/markbank/authoring/lt_q3_batch.py add 2026 hl listening

On the Portuguese pattern (pt_q3_batch.py). The 306 live Lithuanian cards were
written by the shared generator (lt_all.py), which refuses the asks this lane
cards, so the authored file is NEVER regenerated: a sitting's new cards are
merged in beside the live ones, and a live card is never touched. A card that
is already in the bank must regenerate byte for byte, or the add stops.

New cards come from lt_specs.py: the listening asks (CARD-STANDARD 10g) now;
the reading grids and the written tasks follow.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'lithuanian.json')
FILINGS = '/Users/alexlinehan/Documents/NextStepUni-MarkBank-Lanes-20261104/languages-q3/filings-pending.json'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
KINDS = ('listening',)


def new_cards(year, level, kinds):
    import lt_specs
    out = []
    if 'listening' in kinds:
        cards, refused = lt_specs.listening_cards(year, level)
        if refused:
            raise ValueError(f'{year} {level}: listening asks refused {refused}')
        out += cards
    return out


def add(year, level, kinds):
    with open(AUTHORED, encoding='utf-8') as fh:
        authored = json.load(fh)
    have = {c['id']: c for c in authored}
    new = new_cards(year, level, kinds)
    ids = [c['id'] for c in new]
    if len(ids) != len(set(ids)):
        raise ValueError(f'{year} {level}: duplicate new ids')
    drift = [c['id'] for c in new if c['id'] in have
             and json.dumps(c, sort_keys=True) != json.dumps(have[c['id']], sort_keys=True)]
    if drift:
        raise ValueError(f'{year} {level}: cards in the bank no longer regenerate as they stand {drift}')
    new = [c for c in new if c['id'] not in have]
    lv = LEVEL_WORD[level]
    out = list(authored)
    # The listening booklet follows the written one: a sitting's listening
    # cards go after its last card, in the booklet's own order.
    mine = [i for i, x in enumerate(out) if x['year'] == year and x['level'] == lv]
    if not mine:
        raise ValueError(f'{year} {level}: no card of this sitting in the bank to place beside')
    at = max(mine)
    for c in new:
        at += 1
        out.insert(at, c)
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return new


def write_filings(cards):
    """card id -> the heading it files under and why (CARD-STANDARD 9). The
    Lithuanian Atlas headings are its task types (lt_topics.TOPICS), so the
    heading is the card's own topic."""
    import lt_topics
    names = {v: k for k, v in lt_topics.TOPICS['lithuanian'].items()}
    why = {'aural': 'a listening ask: the Atlas files the Listening Comprehension booklet section under '
                    'the listening task type',
           'production': 'a written task: Section B Written Production, filed under the written task type',
           'new_reading': 'a reading ask of the post-2022 paper, filed under the reading task type'}
    data = {}
    if os.path.exists(FILINGS):
        with open(FILINGS, encoding='utf-8') as fh:
            data = json.load(fh)
    for c in cards:
        kind = names.get(c['topicId'], '')
        data[c['id']] = {'heading': c['topicId'], 'questionRef': c['questionRef'],
                         'reason': f"{why.get(kind, 'the card’s own topic')} ({c['topicId']})"}
    with open(FILINGS, 'w', encoding='utf-8') as fh:
        json.dump(dict(sorted(data.items())), fh, ensure_ascii=False, indent=1)
        fh.write('\n')


def main():
    cmd, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    kinds = tuple(sys.argv[4].split(',')) if len(sys.argv) > 4 else KINDS
    if cmd == 'review':
        for c in new_cards(year, level, kinds):
            print(f"  {c['id']:26} {c['totalMarks']:2} | {c['questionText'][:90]}")
    elif cmd == 'add':
        new = add(year, level, kinds)
        write_filings(new)
        print(f'{year} {level}: {len(new)} cards added to {AUTHORED}: {[c["id"] for c in new]}')
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
