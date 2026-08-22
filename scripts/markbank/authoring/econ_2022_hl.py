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

cards += [
    menu('econ-2022-hl-q12-b-iii', 'economics-2-0', 'monopoly-versus-oligopoly',
         '2022 HL Q12(b)(iii)',
         'Explain two changes in market conditions (characteristics) which allow a market to '
         'move from a Monopoly to an Oligopoly.',
         '2 x 3', 6, 'A change in market conditions — any two', 2, 3,
         '• Number of firms in the market: in a monopoly',
         'By 2030, there will be an estimated 500,000 electric vehicles',
         'Two changes, 3 marks each.'),

    menu('econ-2022-hl-q13-b-ii', 'economics-1-3', 'interventions-to-influence-behaviour',
         '2022 HL Q13(b)(ii)',
         'Outline two interventions, other than incentives/taxes, that a government could '
         'consider implementing to influence consumer behaviour.',
         '2 x 6', 12, 'An intervention to influence behaviour — any two', 2, 6,
         '• Minimum prices such as the minimum unit price on alcohol',
         '(c) The Irish Government has signed up to the Organisation',
         'Two interventions, 6 marks each. Incentives and taxes are excluded by the question.'),

    menu('econ-2022-hl-q15-c-ii', 'economics-4-1', 'why-net-contributors-stay-in-the-eu',
         '2022 HL Q15(c)(ii)',
         'Justify why countries which are Net Contributors to the EU, despite the financial cost '
         'of membership, still decide to remain members of the EU.',
         '2 x 5', 10, 'A reason a net contributor stays — any two', 2, 5,
         '• Free Trade Area / larger market / trade expansion/ improved balance of payments',
         'Question 16',
         'Two reasons, 5 marks each.'),

    menu('econ-2022-hl-q16-c-ii', 'economics-0-2', 'consumer-steps-on-fast-fashion',
         '2022 HL Q16(c)(ii)',
         'Outline two steps consumers in Ireland can take to reduce the effects of the fast '
         'fashion industry.',
         '2 x 5', 10, 'A step a consumer can take — any two', 2, 5,
         '• Ethical consumption of goods/Research the product',
         '(iii) Outline one step businesses in Ireland can take',
         'Two steps, 5 marks each. The scheme heads this list "The Irish Consumer" and lists the '
         'business steps separately, so the two sides are not interchangeable.'),
]

emit(cards)
