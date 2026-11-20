#!/usr/bin/env python3
"""Two coordinator-approved corrections to LIVE cards of the small languages
(rulings 6 and 7, 20 Nov 2026). Nothing else on a live card may move.

    python3 scripts/markbank/authoring/sl_livefix.py note dutch
    python3 scripts/markbank/authoring/sl_livefix.py pages dutch 2022=2,3 2023=2,3

note   The answer-language note. eu_topics.language_note (live on every card of
       the one-language subjects) quotes one sitting's sentence for every
       sitting and says it is printed "on its own first page", which is each
       booklet's cover. Replaced, on each live card, by sl_lib.rule_note: the
       rule as THAT card's paper prints it, with the page number the booklet
       prints. Only the note's own text changes, wherever it stands (a row's
       contextNote, the reading text's presentationNote).
pages  The reading text's pages (sourceMaterial.pages), to the pages the paper
       prints the passage on, checked on the render.

Each command prints every card it changes and then proves the rest: every live
card, with the one field masked, is byte-identical to before.
"""
import json
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sl_lib                                                       # noqa: E402
from eu_topics import language_note, LANGUAGE_NAME                  # noqa: E402
from sl_batch import authored_path, ADDITIONS                       # noqa: E402


def _live(subject):
    with open(authored_path(subject), encoding='utf-8') as fh:
        cards = json.load(fh)
    added = set()
    if os.path.exists(ADDITIONS):
        with open(ADDITIONS, encoding='utf-8') as fh:
            added = {i for v in json.load(fh).get(subject, {}).values() for i in v}
    return cards, added


def _save(subject, cards):
    with open(authored_path(subject), 'w', encoding='utf-8') as fh:
        json.dump(cards, fh, ensure_ascii=False, indent=1)
        fh.write('\n')


def _prove(before, after, mask):
    """Every card, with `mask` applied to both copies, is byte-identical."""
    assert [c['id'] for c in before] == [c['id'] for c in after], 'card order or ids moved'
    for b, a in zip(before, after):
        if json.dumps(mask(b), sort_keys=True) != json.dumps(mask(a), sort_keys=True):
            raise AssertionError(f'{a["id"]}: more than the corrected field moved')


def note(subject):
    cards, added = _live(subject)
    before = json.loads(json.dumps(cards))
    old = language_note(subject, LANGUAGE_NAME[subject]) if subject in LANGUAGE_NAME else None
    # The live note as the deck carries it, where another generator wrote it
    # (Ukrainian: the same "on its own first page" sentence, a subject eu_topics
    # does not list in ONE_LANGUAGE): read off the cards themselves.
    # (Modern Greek: its walker's own sentence, "The paper states that answers are to be given in Modern
    # Greek: "...""), one sitting's rule quoted for every sitting and no page.)
    found = {m.group(0) for c in cards if c['id'] not in added for r in c['rows']
             for m in [re.search(r'The examination requires every answer in [A-Z]+\. The paper prints the rule '
                                 r'on its own first page: "[^"]*"|The paper states that answers are to be given '
                                 r'in [A-Z][a-z]+(?: [A-Z][a-z]+)?: "[^"]*"', r.get('contextNote') or '')] if m}
    if len(found) == 1 and old not in found:
        old = next(iter(found))
    docs, changed = {}, []
    for c in cards:
        if c['id'] in added:
            continue
        year = c['year']
        if year not in docs:
            docs[year] = sl_lib.documents(subject, year, 'hl', scheme=False)[1]
        new = sl_lib.rule_note(subject, docs[year], None)
        hits = 0
        for r in c['rows']:
            if old in (r.get('contextNote') or ''):
                r['contextNote'] = r['contextNote'].replace(old, new)
                hits += 1
        src = c.get('sourceMaterial') or {}
        if old in (src.get('presentationNote') or ''):
            src['presentationNote'] = src['presentationNote'].replace(old, new)
            hits += 1
        if hits:
            changed.append((c['id'], hits))

    def mask(c):
        c = json.loads(json.dumps(c))
        for r in c['rows']:
            r.pop('contextNote', None)
        (c.get('sourceMaterial') or {}).pop('presentationNote', None)
        return c
    _prove(before, cards, mask)
    # And the notes themselves: only the old sentence was replaced.
    for b, a in zip(before, cards):
        for rb, ra in zip(b['rows'], a['rows']):
            if rb.get('contextNote') != ra.get('contextNote'):
                assert rb['contextNote'].replace(old, '') == ra['contextNote'].replace(
                    sl_lib.rule_note(subject, sl_lib.documents(subject, a['year'], 'hl', scheme=False)[1], None), ''), a['id']
    _save(subject, cards)
    for cid, hits in changed:
        print(f'  {cid}: {hits} note(s)')
    print(f'{subject}: answer-language note corrected on {len(changed)} live card(s); '
          f'everything else byte-identical')


def pages(subject, specs):
    want = {int(y): [int(p) for p in ps.split(',')] for y, ps in (a.split('=') for a in specs)}
    cards, added = _live(subject)
    before = json.loads(json.dumps(cards))
    changed = []
    for c in cards:
        src = c.get('sourceMaterial')
        if c['id'] in added or not src or c['year'] not in want:
            continue
        if src['pages'] != want[c['year']]:
            changed.append((c['id'], src['pages'], want[c['year']]))
            src['pages'] = list(want[c['year']])

    def mask(c):
        c = json.loads(json.dumps(c))
        (c.get('sourceMaterial') or {}).pop('pages', None)
        return c
    _prove(before, cards, mask)
    _save(subject, cards)
    for cid, was, now in changed:
        print(f'  {cid}: {was} -> {now}')
    print(f'{subject}: reading-text pages corrected on {len(changed)} live card(s); everything else byte-identical')


if __name__ == '__main__':
    cmd, subject = sys.argv[1], sys.argv[2]
    if cmd == 'note':
        note(subject)
    elif cmd == 'pages':
        pages(subject, sys.argv[3:])
