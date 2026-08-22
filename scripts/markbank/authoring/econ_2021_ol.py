#!/usr/bin/env python3
"""Economics 2021 Ordinary Level — Section B.

Same rules as econ_2024_ol.py. This paper runs its responses under bold headings
rather than as bullets, so it splits with `heads()`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, card, defurnish, emit, heads, load, tidy  # noqa: E402

YEAR, LEVEL = 2021, 'ordinary'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'loping countries to benefit from globalisation', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, headings, note, notes='', steps=None, stem=''):
    chunk = block(BODY, start, end)
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      [defurnish(h) for h in heads(chunk, headings)], note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2021-ol-q11-b-i-neg', 'economics-4-1', 'disadvantages-of-globalisation',
         '2021 OL Q11(b)(i) — disadvantages',
         'Outline two possible disadvantages of globalisation.',
         '2 @ 3', 6, 'A disadvantage of globalisation — any two', 2, 3,
         'Widens the gap between rich and poor', '(ii) Name two multinational companies',
         ['Widens the gap between rich and poor', 'Environmental impact', 'Outsourcing',
          'Lower cost countries'],
         'Two disadvantages, 3 marks each.',
         notes='The scheme answers advantages and disadvantages under one part, so each side is '
               'carded on its own with its own questionRef — the rule for parallel accounts.'),

    menu('econ-2021-ol-q11-b-iii', 'economics-4-1', 'why-mncs-locate-in-ireland',
         '2021 OL Q11(b)(iii)',
         'Outline two reasons why multinational companies choose to locate in Ireland.',
         '2 @ 7', 14, 'A reason MNCs locate in Ireland — any two', 2, 7,
         'Low rates of taxation: the rate of corporation profits tax',
         '(c) (i) Foreign Direct Investment (FDI) has been a key contributor',
         ['Low rates of taxation', 'Access to EU market / Member of the euro currency',
          'Availability of state incentives', 'Good industrial relations',
          'Stable rate of economic growth', 'Stable economic climate'],
         'Two reasons, 7 marks each, split 3 for the reason and 4 for developing it.'),
]

emit(cards)
