#!/usr/bin/env python3
"""Economics 2022 Ordinary Level — Section B.

Same rules as econ_2024_ol.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, bullets, card, emit, load, tidy  # noqa: E402

YEAR, LEVEL = 2022, 'ordinary'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'graph below shows the breakdown of streaming services in the US', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, note, notes='', steps=None, stem=''):
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      bullets(block(BODY, start, end)), note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2022-ol-q11-a-ii', 'economics-2-0', 'advantages-of-many-firms-for-consumers',
         '2022 OL Q11(a)(ii)',
         'Outline two advantages for consumers of many firms providing streaming services in '
         'this market.',
         '1 x 8 + 1 x 4', 12, 'An advantage to consumers — any two', 2, 8,
         '• Gives the consumer more choice',
         '(b) If Netflix were to buy out (take over) all the other streaming services',
         'Two advantages, the first paid 8 and the second 4.',
         stem='Set on a chart of US streaming services by number of users — YouTube highest, '
              'Vimeo lowest.',
         steps=[8, 4]),

    menu('econ-2022-ol-q11-c-ii', 'economics-2-0', 'barriers-to-entry', '2022 OL Q11(c)(ii)',
         'Firms who may wish to enter a monopoly industry face barriers to entry. Outline two '
         'possible barriers to entry.',
         '2 x 4', 8, 'A barrier to entry — any two', 2, 4,
         '• The Government may grant a company the sole right',
         '(iii) Suggest one way, governments can intervene',
         'Two barriers, 4 marks each.'),

    menu('econ-2022-ol-q11-c-iii', 'economics-1-3', 'government-intervention-dominant-firm',
         '2022 OL Q11(c)(iii)',
         'Suggest one way governments can intervene in the market if one firm becomes too '
         'dominant.',
         '1 @ 4', 4, 'A way government can intervene — any one', 1, 4,
         '• Regulation: regulators can ensure that dominant firms', 'Question 12',
         'One way, 4 marks.'),
]

emit(cards)
