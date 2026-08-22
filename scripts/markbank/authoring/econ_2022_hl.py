#!/usr/bin/env python3
"""Economics 2022 Higher Level — Section B.

Same rules as econ_2024_hl.py. This paper writes its tariffs as `⟨1 x 8⟩`
`⟨1 x 4⟩` rather than `⟨1 @ 8⟩`, which is the same descending shape with a
different sign, and bullets its responses.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, bullets, card, emit, load, tidy  # noqa: E402

YEAR, LEVEL = 2022, 'higher'
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
    menu('econ-2022-hl-q11-a-i', 'economics-2-1', 'regional-rent-disparity', '2022 HL Q11(a)(i)',
         'Outline two possible reasons for the disparity in average rents between Dublin City '
         'and Waterford City in Q2, 2021.',
         '1 x 8 + 1 x 4', 12, 'A reason for the rent disparity — any two', 2, 8,
         '• Greater population per sq. km in Dublin',
         '(ii) Outline two possible interventions the Irish government could pursue',
         'Two reasons, the first paid 8 and the second 4.',
         steps=[8, 4]),

    menu('econ-2022-hl-q11-a-ii', 'economics-3-5', 'balanced-regional-development',
         '2022 HL Q11(a)(ii)',
         'Outline two possible interventions the Irish government could pursue to support '
         'balanced regional development in Ireland.',
         '1 x 8 + 1 x 4', 12, 'An intervention for balanced regional development — any two', 2, 8,
         '• Increased investment in industry in rural areas',
         '(b) Explain, with the use of a fully labelled diagram how the equilibrium price of land',
         'Two interventions, the first paid 8 and the second 4.',
         steps=[8, 4]),

    menu('econ-2022-hl-q11-b-ii', 'economics-1-2', 'characteristics-of-land', '2022 HL Q11(b)(ii)',
         'Other than land being fixed in supply, outline two characteristics of land in the '
         'economic sense.',
         '2 x 5', 10, 'A characteristic of land — any two', 2, 5,
         '• No cost of production to society as a whole',
         '(iii) Explain how the concept of derived demand',
         'Two characteristics, 5 marks each. Fixed supply is excluded by the question, which '
         'leaves exactly the three the scheme prints.'),

    menu('econ-2022-hl-q12-a-ii', 'economics-2-0', 'advantages-of-deregulation',
         '2022 HL Q12(a)(ii)',
         'Outline two advantages of deregulation of a market.',
         '2 x 3', 6, 'An advantage of deregulation — any two', 2, 3,
         '• Encourage greater efficiency / less waste of scarce resources',
         '(iii) Explain the term privatisation',
         'Two advantages, 3 marks each.'),
]

emit(cards)
