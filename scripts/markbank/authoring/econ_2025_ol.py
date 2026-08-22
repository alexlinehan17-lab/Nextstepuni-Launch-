#!/usr/bin/env python3
"""Economics 2025 Ordinary Level — Section B.

Same rules as econ_2024_ol.py. This paper writes most of its descending tariffs
in words beside the question — "1st @ 8", "2nd @ 4" — and its possible responses
run together under bold headings rather than as bullets, so it splits with
`heads()` like a Higher paper rather than with `bullets()`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, card, defurnish, emit, heads, load, tidy  # noqa: E402

YEAR, LEVEL = 2025, 'ordinary'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'sellers to influence the price at which the product is sold', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, headings, note, notes='', steps=None, stem=''):
    chunk = block(BODY, start, end)
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      [defurnish(h) for h in heads(chunk, headings)], note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2025-ol-q11-b-iii', 'economics-2-0', 'perfect-competition-consumer-advantage',
         '2025 OL Q11(b)(iii)',
         'As a consumer what, in your opinion, is the main advantage of a perfectly competitive '
         'market? Explain your answer.',
         '1 @ 8', 8, 'An advantage to the consumer — any one', 1, 8,
         'Low prices - firms are competitive', '(c) Dublin Airport has a passenger cap',
         ['Low prices -', 'No Advertising', 'Efficient use of scarce resources'],
         'One advantage, 8 marks. The question asks for an opinion and the scheme answers it '
         'with the three the examiner accepts.'),

    menu('econ-2025-ol-q11-c-i', 'economics-2-2', 'dublin-airport-passenger-cap',
         '2025 OL Q11(c)(i)',
         'Outline one reason why, in your opinion, a limit has been placed on the number of '
         'passengers who can pass through Dublin Airport.',
         '1 @ 8', 8, 'A reason for the passenger cap — any one', 1, 8,
         'Reduce emissions – flying creates a lot of emissions', 'Question 12',
         ['Reduce emissions', 'Reduce traffic around Dublin airport', 'Reduce noise pollution'],
         'One reason, 8 marks.',
         stem='Dublin Airport has a cap of 32 million passengers a year, which was exceeded '
              'in 2024.'),

    menu('econ-2025-ol-q13-c', 'economics-3-1', 'uses-of-the-apple-tax-money', '2025 OL Q13(c)',
         'Outline two areas of infrastructure the Irish government could spend the €14 billion '
         'Apple tax money on (other than a new city and reunification of Ireland). Justify your '
         'choice in each case.',
         '2 @ 7', 14, 'An area of infrastructure — any two', 2, 7,
         'Social Housing – build more social and affordable housing', 'Question 14',
         ['Social Housing', 'Public transport', 'School building', 'Water infrastructure',
          'Invest in Ireland’s electricity provision', 'Build / expand hospitals'],
         'Two areas, 7 marks each. The scheme opens with "Accept relevant infrastructure '
         'spending", so this list is what it names rather than all it allows.'),

    menu('econ-2025-ol-q14-c', 'economics-4-0', 'ldc-actions-to-improve-welfare', '2025 OL Q14(b)',
         'Suggest two actions the governments of LDCs receiving aid can take to improve their '
         'citizens’ welfare.',
         '1st @ 6 + 2nd @ 4', 10, 'An action to improve citizens’ welfare — any two', 2, 6,
         'Infrastructure Development - investing in essential infrastructure',
         '(c) The data below is extracted from Ireland',
         ['Infrastructure Development', 'Education and skills training', 'Healthcare -',
          'Job Creation'],
         'Two actions. The paper pays the first 6 and the second 4 — the scheme writes the '
         'split out in words rather than in the marks column.',
         steps=[6, 4]),
]

emit(cards)
