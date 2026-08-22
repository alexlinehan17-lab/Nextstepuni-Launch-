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
from econ_lib import anyN, block, bullets, card, emit, load, tidy  # noqa: E402

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
]

emit(cards)
