#!/usr/bin/env python3
"""Economics 2024 Ordinary Level — Section B.

Same rules as the Higher paper (see econ_2024_hl.py), with one difference in how
the scheme is laid out: Ordinary Level sets its possible responses as a BULLET
LIST and spells the descending tariff out in words beside the question — "1st @
8", "2nd @ 4" — where Higher Level runs the responses together under bold
headings and puts the tariff in the marks column. Underneath they are the same
shape, so `bullets()` does here what `heads()` does there.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, block, bullets, card, emit, load, point, tidy  # noqa: E402

YEAR, LEVEL = 2024, 'ordinary'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 11 (a) The chart shows increases in electricity prices',
             'Student Research Project', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, note, notes='', steps=None, stem=''):
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      bullets('• ' + block(BODY, start, end)), note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    # ── Question 11 ─────────────────────────────────────────────────────────
    menu('econ-2024-ol-q11-a-ii', 'economics-1-2', 'effect-of-energy-costs-on-business',
         '2024 OL Q11(a)(ii)',
         'Outline one possible economic effect of these price increases on businesses in Ireland.',
         '1 @ 8', 8, 'An economic effect on business — any one', 1, 8,
         'Increased costs for business due to higher prices',
         '(iii) During winter 2023',
         'One effect, 8 marks.',
         stem='Set on a chart of Irish electricity price increases from 2020 to 2022.'),

    menu('econ-2024-ol-q11-a-iii', 'economics-1-3', 'electricity-credit-rationale',
         '2024 OL Q11(a)(iii)',
         'During winter 2023 – 2024, the Irish government granted all households a credit of €450 '
         'towards their electricity bills. Why, in your opinion, did the government do this?',
         '1 @ 8', 8, 'A reason the government granted the credit — any one', 1, 8,
         'To alleviate the financial burden/economic welfare of Irish households',
         '(b) The diagram below represents the long-run equilibrium',
         'One reason, 8 marks. The question asks for an opinion, and the scheme answers it with '
         'six the examiner will accept — it is not open-ended.'),

    menu('econ-2024-ol-q11-b-iii', 'economics-2-0', 'oligopoly-in-ireland', '2024 OL Q11(b)(iii)',
         'The electricity market is an example of an oligopoly market in Ireland. Give one '
         'example of an oligopoly market in Ireland and explain a reason for your choice.',
         '1 @ 8', 8, 'A reason a market is an oligopoly — any one', 1, 8,
         'Only a few providers dominate the market',
         '(c) Panda Power left the Irish energy market',
         'One reason, 8 marks. The scheme accepts mobile phones, broadband, insurance, banking, '
         'TV services or supermarkets as the example; the marks are for the reason.'),

    # ── Question 12 ─────────────────────────────────────────────────────────
    menu('econ-2024-ol-q12-a-ii', 'economics-3-2', 'benefits-of-increased-employment',
         '2024 OL Q12(a)(ii)',
         'Outline one possible economic benefit of increased employment for the Irish economy.',
         '1 @ 8', 8, 'A benefit of increased employment — any one', 1, 8,
         '• Increased standard of living for citizens',
         '(b) (i) Currently there is a shortage of skilled employees',
         'One benefit, 8 marks.',
         stem='In 2022 the number of people employed in Ireland exceeded 2.5 million for the '
              'first time.'),

    # ── Question 13 ─────────────────────────────────────────────────────────
    menu('econ-2024-ol-q13-b-ii', 'economics-3-3', 'effects-of-food-price-inflation',
         '2024 OL Q13(b)(ii)',
         'Explain one possible economic effect food price inflation will have on consumers.',
         '1 @ 8', 8, 'An effect on consumers — any one', 1, 8,
         '• Reduced purchasing power / standard of living',
         '(iii)',
         'One effect, 8 marks.',
         stem='Set on a chart of annual food price inflation across six countries — Switzerland '
              'lowest, Turkey highest.'),

    # These two are here because they are the paper's only cards on their strand
    # topic — scarcity, and the cost structure of a firm.
    card('econ-2024-ol-q12-b-i', YEAR, LEVEL, 'economics-0-1', 'scarcity-of-labour',
         '2024 OL Q12(b)(i)',
         'Currently there is a shortage of skilled employees in different sectors of the Irish '
         'economy. Explain the economic term scarcity in relation to labour (employees).',
         '1 @ 8', 8,
         [anyN('r-1', 'Scarcity applied to labour — either wording', 8, 1, 8,
               bullets('• ' + block(BODY, 'When applied to labour, scarcity refers to the situation where the number',
                                    '(ii) The pharmaceutical industry has experienced')),
               'The scheme gives two wordings of the same idea: demand for workers exceeds the '
               'supply of them. Either earns the 8.')],
         '', tariff_kind='bestNofParts'),

    card('econ-2024-ol-q13-a-ii', YEAR, LEVEL, 'economics-1-5', 'fixed-and-variable-costs',
         '2024 OL Q13(a)(ii)',
         'Explain the difference between fixed costs and variable costs. Give an example in '
         'each case.',
         'fixed', 8,
         [point('r-fixed', 'Fixed Costs: Costs which do not change as output changes / Costs '
                'which have to be paid even if nothing is produced.', 4,
                'The scheme sets the two definitions side by side in a table with their examples '
                'in the next column: rent and loan repayments for fixed.',
                accepts=['Rent', 'Loan repayments']),
          point('r-variable', 'Variable Costs: Costs which do change as output changes.', 4,
                'Examples the scheme prints: electricity, labour, raw materials.',
                accepts=['Electricity', 'Labour', 'Raw materials'])],
         'Carded as two rows rather than one menu: the question asks for the DIFFERENCE, so a '
         'student needs both halves, and picking either from a list would not be answering it.',
         tariff_kind='fixed'),
]

# ── The parts econ_parts found that hand-reading had passed over ────────────
P = Paper(YEAR, LEVEL)
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('ways citizens in Ireland can behave more sustainably', 'econ-2024-ol-q12-c-ii',
       'economics-0-2', 'sustainable-household-behaviour',
       'Outline two ways citizens in Ireland can behave more sustainably in their use of energy.',
       'A way to behave more sustainably — any two',
       'Two ways, 8 marks each.',
       drop=SCAFFOLD)

P.menu('reasons why exports are important for the Irish economy', 'econ-2024-ol-q14-a-ii',
       'economics-4-2', 'importance-of-exports',
       'Outline two reasons why exports are important for the Irish economy.',
       'A reason exports matter — any two',
       'Two reasons, 6 marks each.',
       claim=2, per=6, drop=SCAFFOLD)

emit(cards + P.cards)
