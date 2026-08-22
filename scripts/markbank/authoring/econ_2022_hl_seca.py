#!/usr/bin/env python3
"""Economics 2022 Higher Level — Section A.

Not carded: the two parts answered by reading the infographic printed with them
(the expansionary/contractionary balance of payments call, the opportunity cost
off the production possibility frontier), and the two diagram-labelling parts.

Question 5 pays its two alternatives differently — the scheme's mark column
prints "4 + 4" against (b) and "7 (4+3)" against (c) — and each card carries
the tariff printed against its own part.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, block, bullets, card, load, tidy  # noqa: E402

P = Paper(2022, 'higher', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')
AGREE = ('I agree with MUP', 'May combat alcohol abuse', 'Less personal', 'Reduced admissions',
         'A healthier population')

P.menu('influenced the above trend in Personal', 'econ-2022-hl-sa-q2-b',
       'economics-1-1', 'what-moves-personal-consumption',
       'Outline one factor which could have influenced the trend in personal consumption in '
       'Quarter 2, 2021.',
       'A factor behind the rise in consumption — any one',
       'One factor, 6 marks: 3 for the factor and 3 for explaining it.',
       ref='2022 HL Section A Q2(b)', claim=1, per=6, drop=SCAFFOLD,
       stem='The Quarterly National Accounts for Quarter 2 of 2021 — the quarter Ireland came out '
            'of its third lockdown — showed personal consumption rising.')

P.menu('Minimum Unit Pricing (MUP) for alcohol was introduced', 'econ-2022-hl-sa-q3-a-agree',
       'economics-1-3', 'the-case-for-minimum-unit-pricing',
       'Do you agree with this new MUP (Minimum Unit Pricing) for alcohol? Justify the case for '
       'it.',
       'A reason to agree with minimum pricing — any one',
       'One justification, 9 marks: 5 for the point and 4 for developing it. The scheme marks '
       'either side, so a case against earns the same.',
       ref='2022 HL Section A Q3(a) — the case for', claim=1, per=9,
       drop=SCAFFOLD + ('I agree with MUP',), stop='I disagree with MUP',
       stem='From early 2022 a 750ml bottle of wine could not be sold for less than €7.40, a '
            '500ml can of beer for less than €1.70, or a 70cl bottle of spirits for less than '
            '€20.70.',
       notes='The part is answered either way and the scheme lists the responses for each side '
             'under its own heading, so each side is its own card — the rule for parallel '
             'accounts, so a student is not shown ten options to pick one from.')

P.menu('Minimum Unit Pricing (MUP) for alcohol was introduced', 'econ-2022-hl-sa-q3-a-disagree',
       'economics-1-3', 'the-case-against-minimum-unit-pricing',
       'Do you agree with this new MUP (Minimum Unit Pricing) for alcohol? Justify the case '
       'against it.',
       'A reason to disagree with minimum pricing — any one',
       'One justification, 9 marks: 5 for the point and 4 for developing it.',
       ref='2022 HL Section A Q3(a) — the case against', claim=1, per=9,
       drop=SCAFFOLD + AGREE + ('I disagree with MUP',),
       stem='From early 2022 a 750ml bottle of wine could not be sold for less than €7.40, a '
            '500ml can of beer for less than €1.70, or a 70cl bottle of spirits for less than '
            '€20.70.')

P.menu('significant change in the ageing demographics', 'econ-2022-hl-sa-q5-a',
       'economics-3-5', 'why-the-population-is-ageing',
       'Explain two factors which are likely to have influenced the ageing of the Irish '
       'population.',
       'A factor behind the ageing population — any two',
       'Two factors, the first paid 4 and the second 3.',
       ref='2022 HL Section A Q5(a)', steps=[4, 3], drop=SCAFFOLD,
       stem='The number of people in Ireland aged over 65 is predicted to reach 1 million by 2031.')

P.menu('ageing population will have on future government', 'econ-2022-hl-sa-q5-c',
       'economics-3-1', 'ageing-population-and-government-policy',
       'Outline two impacts Ireland’s ageing population will have on future government policy.',
       'An impact on government policy — any two',
       'Two impacts, the first paid 4 and the second 3.',
       ref='2022 HL Section A Q5(c)', steps=[4, 3], drop=SCAFFOLD)

P.menu('Ensure price stability: ECB aims for an inflation rate', 'econ-2022-hl-sa-q7-b',
       'economics-3-4', 'roles-of-the-european-central-bank',
       'Other than setting the base interest rate, outline two other roles of the European '
       'Central Bank.',
       'A role of the ECB — any two',
       'Two roles, 3 marks each. Setting the base rate is excluded by the question.',
       ref='2022 HL Section A Q7(b)', drop=SCAFFOLD)

P.menu('Explain what is meant by the economic term hidden economy', 'econ-2022-hl-sa-q8-a',
       'economics-3-1', 'what-the-hidden-economy-is',
       'Explain what is meant by the economic term hidden economy.',
       'A way of putting it — any one',
       'One explanation, 5 marks. The three the scheme lists are the same idea said three ways, '
       'so any of them earns the marks.',
       ref='2022 HL Section A Q8(a)', claim=1, per=5, drop=SCAFFOLD)

P.menu('reasons for the supply chain issues', 'econ-2022-hl-sa-q8-b',
       'economics-4-2', 'causes-of-supply-chain-disruption',
       'Outline two reasons for the supply chain issues which many companies experienced in '
       'Ireland during 2021 and 2022.',
       'A reason for the supply chain issues — both of these',
       'Two reasons, 5 marks each, and the scheme lists exactly two.',
       ref='2022 HL Section A Q8(b)', drop=SCAFFOLD)

# ── Q5(b), built from the scheme directly ───────────────────────────────────
# The mark cell ⟨4 + 4⟩ is printed four bullets down its own response list, so
# everything above it reads as the question and the part arrives with one option
# left. Sliced here instead, between the first response and the next part.
BODY = tidy(load(2022, 'higher'))
P.cards.append(card(
    'econ-2022-hl-sa-q5-b', 2022, 'higher', 'economics-2-1',
    'economic-advantages-of-an-ageing-population', '2022 HL Section A Q5(b)',
    'Outline two economic advantages of an ageing Irish population.',
    '2 @ 4', 8,
    [anyN('r-1', 'An advantage of an ageing population — any two', 8, 2, 4,
          bullets(block(BODY, 'Increased numbers may participate in the labour force',
                        '(c) OR Outline two impacts')),
          'Two advantages, 4 marks each.')],
    '', section='A',
    stem='The number of people in Ireland aged over 65 is predicted to reach 1 million by 2031.'))

P.emit()
