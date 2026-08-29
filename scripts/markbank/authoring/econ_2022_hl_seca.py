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
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

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


# ── Second pass: the non-menu parts, built from the scheme directly ─────────
# Each of these prints its whole answer as one or two blocks rather than a
# bulleted menu, so the extractor has nothing to split and the card is sliced
# by hand. Every slice is a contiguous run of the scheme; scheme typos ride
# along uncorrected, because retyping is how corruption enters.

# Q1(b). The paper's demand graph is in the figure manifest as a complete art
# crop, so the card can carry the question as the paper words it.
P.cards.append(card(
    'econ-2022-hl-sa-q1-b', 2022, 'higher', 'economics-1-1', 'the-law-of-demand',
    '2022 HL Section A Q1(b)',
    'With reference to the graph above explain the law of demand.',
    '5', 5,
    [point('r-1', as_option(block(BODY, 'The Law of Demand states',
                                  '2. (a) Using the data provided')), 5,
           'The law itself, then what it looks like on this graph: the price rise from €4 to €5 '
           'cuts quantity demanded from 8 to 4.')],
    'Part (a), the elasticity calculation off the same graph, is not carded — the response is '
    'the worked formula.', section='A',
    tariff_kind='fixed', figure_key='economics-2022-HL-paper-p03-art'))

# Q3(b). The market-failure explanation, 3 for the statement and 3 for the
# example.
P.cards.append(card(
    'econ-2022-hl-sa-q3-b', 2022, 'higher', 'economics-2-2', 'alcohol-and-market-failure',
    '2022 HL Section A Q3(b)',
    'The purchase of alcohol in the free market may generate a market failure. Explain this '
    'statement using an example to illustrate your understanding.',
    '3 + 3', 6,
    [point('r-1', as_option(block(BODY, 'Market failure occurs when the price mechanism',
                                  '4. (a) Categorise each of the following')), 6,
           '3 for explaining market failure and 3 for an example of it in the alcohol market.')],
    '', section='A', tariff_kind='fixed',
    stem='From early 2022 a 750ml bottle of wine could not be sold for less than €7.40, a '
         '500ml can of beer for less than €1.70, or a 70cl bottle of spirits for less than '
         '€20.70.'))

# Q4(b). The ticks in (a) are not carded — they are a table — but the scheme
# prints a fixed justification for each of the three items, on a descending
# 3+2+2, and the justification states the categorisation it defends.
P.cards.append(card(
    'econ-2022-hl-sa-q4-b', 2022, 'higher', 'economics-3-0', 'injections-and-leakages-justified',
    '2022 HL Section A Q4(b)',
    'Categorise each of the following as either an injection, or a leakage from the circular '
    'flow of income. Justify each of your choices.',
    '3 + 2 + 2', 7,
    [anyN('r-1', 'The justification for each item — all three', None, 3, 3,
          bullets(block(BODY, 'Public sector salaries are a part of government spending',
                        'OR (c) Outline two reasons why inflows')),
          'Three justifications, paid 3, 2 and 2. Each names the side of the circular flow its '
          'item sits on.', steps=[3, 2, 2])],
    'The tick table in (a) carries its own 3+3+2; this card is the justification the paper '
    'asks for in (b).', section='A',
    tariff_kind='fixed', figure_key='economics-2022-HL-paper-p06-i0'))

# Q9(a) and Q9(b). Private cost, private benefit, then the social benefits —
# each side priced by its own printed cell.
P.cards.append(card(
    'econ-2022-hl-sa-q9-a', 2022, 'higher', 'economics-2-2', 'private-costs-and-benefits',
    '2022 HL Section A Q9(a)',
    'Identify one private cost and one private benefit for the consumer of installing solar '
    'panels.',
    '5 + 5', 10,
    [point('r-cost', as_option(block(BODY, 'The private cost of installing solar panels',
                                     'A private benefit for the consumer')), 5,
           'The private cost, 5 marks.'),
     point('r-benefit', as_option(block(BODY, 'A private benefit for the consumer of installing '
                                              'solar panels')), 5,
           'The private benefit, 5 marks.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-hl-sa-q9-b', 2022, 'higher', 'economics-2-2', 'social-benefits-of-solar-panels',
    '2022 HL Section A Q9(b)',
    'Installing solar panels also creates social benefits. Discuss this statement.',
    '5', 5,
    [point('r-1', as_option(block(BODY, 'Social benefits are benefits to society',
                                  '10. (a)')), 5,
           'What a social benefit is, then the two this good creates: finite resources spared '
           'and emissions avoided.')],
    '', section='A', tariff_kind='fixed'))

# Q10(b). Point X is judged against the production possibility schedule, which
# the figure manifest carries whole; the reasoning — inside the frontier is
# inefficient — is the economics the 9 marks pay for. Part (a), the opportunity
# cost read off the same schedule, is a worked figure and is not carded.
P.cards.append(card(
    'econ-2022-hl-sa-q10-b', 2022, 'higher', 'economics-0-1', 'producing-inside-the-frontier',
    '2022 HL Section A Q10(b)',
    'The point X (20,20) is another production possibility for PepsiCo. Would you recommend '
    'them to produce at this point? Explain your answer.',
    '9', 9,
    [point('r-1', as_option(block(BODY, 'No, as it can be seen as waste of resources',
                                  'SECTION B')), 9,
           'No — X lies inside the frontier, so resources are idle: at 20 of either product the '
           'schedule allows 80 of the other.')],
    '', section='A', tariff_kind='fixed',
    stem='Cork based firm PepsiCo have 23 brands in total. Doritos and Tropicana are two of '
         'their most popular products.',
    figure_key='economics-2022-HL-paper-p13-i0'))

# ── Tick tables, answered by the scheme's own completed table ──────────────
# See econ_tick_crop.py: the ✔ is drawn, not set in the text layer, so
# extraction keeps the tick and loses the column it sits in — and the column is
# the answer. The completed table is bound as a SOLUTION crop, hidden until
# reveal, the way the Maths deck carries a printed model solution.

P.cards.append(card(
    'econ-2022-hl-seca-q4-a-ticks', 2022, 'higher', 'economics-3-0',
    'injections-and-leakages-in-the-circular-flow', '2022 HL Section A Q4(a)',
    'Categorise each of the following as either an injection, or a leakage from the circular '
    'flow of income: the Irish government increases public sector salaries by 1% in 2023; Irish '
    'exports increase to record \u20ac160 bn despite the Covid 19 Pandemic; Irish consumers '
    'saved more than \u20ac10bn in first quarter of 2021.',
    '3+3+2', 8,
    [point('r-1', as_option(block(BODY, 'Injection Leakage The Irish government',
                                  'Answer either (b) or (c)')), 8,
           'Read the completed table below \u2014 in flat text the three ticks carry no column. '
           'Government spending and exports are INJECTIONS, money entering the domestic flow; '
           'saving is a LEAKAGE, income received but not spent. The test is direction of travel, '
           'not whether the sum is large or welcome.')],
    'Saving is the one students misplace: it is money that stayed out of the flow, so it leaks '
    'even though nobody spent it abroad.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2022-HL-scheme-p07-q4a-ticks'))

P.emit()
