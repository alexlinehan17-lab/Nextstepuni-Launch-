#!/usr/bin/env python3
"""Economics 2023 Ordinary Level — Section B.

Same rules as econ_2024_ol.py. This paper is bulleted throughout and writes every
descending tariff in words beside the question.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, bullets, card, emit, load, tidy  # noqa: E402

YEAR, LEVEL = 2023, 'ordinary'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 11 Possible responses Max Mark', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, note, notes='', steps=None, stem=''):
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      bullets(block(BODY, start, end)), note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2023-ol-q11-a-i', 'economics-2-0', 'monopolistic-competition-identified',
         '2023 OL Q11(a)(i)',
         'Outline two reasons why, in your opinion, the hair and beauty industries are an '
         'example of monopolistic competition.',
         '1st @ 6 + 2nd @ 4', 10, 'A reason it is monopolistic competition — any two', 2, 6,
         '• There are many firms in the industry',
         '(ii) Outline two advantages for consumers of monopolistic competition',
         'Two reasons, the first paid 6 and the second 4.',
         steps=[6, 4]),

    menu('econ-2023-ol-q11-a-ii', 'economics-2-0', 'monopolistic-competition-consumer-advantages',
         '2023 OL Q11(a)(ii)',
         'Outline two advantages for consumers of monopolistic competition.',
         '1st @ 6 + 2nd @ 4', 10, 'An advantage to consumers — any two', 2, 6,
         '• Consumers benefit from increased choice',
         '(b) The diagram below represents the long run equilibrium',
         'Two advantages, the first paid 6 and the second 4.',
         steps=[6, 4]),

    menu('econ-2023-ol-q12-b-ii', 'economics-3-1', 'principles-of-a-good-tax-system',
         '2023 OL Q12(b)(ii)',
         'Explain two other principles of a good tax system that you would consider important '
         'in the current economic climate.',
         '1st @ 8 + 2nd @ 4', 12, 'A principle of a good tax system — any two', 2, 8,
         '• A good tax system should not be a disincentive to work',
         '(c) As part of Budget 2023 the government have announced an electricity credit',
         'Two principles, the first paid 8 and the second 4. Equity — ability to pay — is '
         'excluded by the question.',
         steps=[8, 4]),

    menu('econ-2023-ol-q12-c-i', 'economics-1-3', 'benefit-of-the-electricity-credit',
         '2023 OL Q12(c)(i)',
         'Outline one benefit of the €600 electricity credit to the Irish household.',
         '1 @ 8', 8, 'A benefit to the household — any one', 1, 8,
         '• It helps Irish households to maintain their standard of living',
         '(ii) Describe two actions an Irish household could take',
         'One benefit, 8 marks.'),

    menu('econ-2023-ol-q12-c-ii', 'economics-0-2', 'household-actions-to-cut-electricity-use',
         '2023 OL Q12(c)(ii)',
         'Describe two actions an Irish household could take to reduce their electricity bills '
         'and make them more sustainable.',
         '1st @ 10 + 2nd @ 4', 14, 'An action the household could take — any two', 2, 10,
         '• The Irish household could reduce their consumption of electricity',
         '(iii) Name the three pillars of sustainability',
         'Two actions, the first paid 10 and the second 4.',
         steps=[10, 4]),

    menu('econ-2023-ol-q13-a-ii', 'economics-4-2', 'advantages-of-exports',
         '2023 OL Q13(a)(ii)',
         'Describe two advantages of exports for the Irish economy.',
         '1st @ 8 + 2nd @ 2', 10, 'An advantage of exports — any two', 2, 8,
         '• Increased national income: exporting goods and services',
         '(b) National Income is calculated using the following formula',
         'Two advantages, the first paid 8 and the second 2.',
         steps=[8, 2]),
]

emit(cards)
