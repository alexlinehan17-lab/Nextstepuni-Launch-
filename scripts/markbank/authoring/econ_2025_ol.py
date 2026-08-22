#!/usr/bin/env python3
"""Economics 2025 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, block, card, heads, load, as_option, tidy  # noqa: E402

P = Paper(2025, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Accept relevant infras',
            'Justify your answer')

P.menu('areas of public infrastructure the Government could invest', 'econ-2025-ol-q13-c',
       'economics-3-1', 'uses-of-the-apple-tax-money',
       'Outline two areas of public infrastructure the Government could invest the €14 billion '
       'Apple tax money in, other than a new city and reunification of Ireland. Justify your '
       'choice in each case.',
       'An area of infrastructure — any two',
       'Two areas, 7 marks each. The scheme opens "Accept relevant infrastructure spending", so '
       'its list is what it names rather than all it allows.',
       drop=SCAFFOLD)

P.menu('reasons why imports are important to the Irish economy', 'econ-2025-ol-q14-a-ii',
       'economics-4-2', 'importance-of-imports',
       'Outline two reasons why imports are important to the Irish economy.',
       'A reason imports matter — any two',
       'Two reasons, the first paid 10 and the second 6.',
       drop=SCAFFOLD)

P.menu('Governments of LDCs who receive this aid', 'econ-2025-ol-q14-c',
       'economics-4-0', 'ldc-actions-to-improve-welfare',
       'Suggest two actions the governments of LDCs receiving aid can take to improve their '
       'citizens’ welfare.',
       'An action to improve citizens’ welfare — any two',
       'Two actions, the first paid 6 and the second 4.',
       ref='2025 OL Q14(b)', drop=SCAFFOLD)

P.menu('one economic benefit for each of the following of this reduction in overall',
       'econ-2025-ol-q15-a-i', 'economics-3-1', 'benefits-of-lower-national-debt',
       'Outline one economic benefit of a reduction in overall national debt for the Irish '
       'government, and one for citizens in Ireland.',
       'A benefit of lower national debt — any two',
       'The paper pays 8 for the government benefit and 6 for the citizens one; the scheme lists '
       'the government benefits first.',
       drop=SCAFFOLD + ('Irish government and 2', 'Irish Government'))

P.menu('economic effects which falling price inflation may have', 'econ-2025-ol-q16-a-iii',
       'economics-3-3', 'effects-of-falling-inflation',
       'Discuss two economic effects which falling price inflation may have on Irish consumers.',
       'An effect of falling inflation — any two',
       'Two effects, the first paid 8 and the second 4.',
       drop=SCAFFOLD)

P.menu('action that each of the following sectors of the Irish economy', 'econ-2025-ol-q16-b-i-ag',
       'economics-0-2', 'agricultural-actions-on-climate',
       'Identify one action the agricultural sector could take to reduce the effects of climate '
       'change. Justify your answer.',
       'An action for the agricultural sector — any one',
       'One action, 6 marks; the paper pays a second for the industrial sector.',
       ref='2025 OL Q16(b)(i) — agricultural sector',
       claim=1, per=6, drop=SCAFFOLD + ('Agricultural Sector',), stop='Industrial Sector',
       notes='The part asks for one action from each of two sectors and the scheme heads the two '
             'lists separately, so each sector is its own card.')

P.menu('action that each of the following sectors of the Irish economy', 'econ-2025-ol-q16-b-i-ind',
       'economics-0-2', 'industrial-actions-on-climate',
       'Identify one action the industrial sector could take to reduce the effects of climate '
       'change. Justify your answer.',
       'An action for the industrial sector — any one',
       'One action, 6 marks.',
       ref='2025 OL Q16(b)(i) — industrial sector',
       claim=1, per=6,
       drop=SCAFFOLD + ('Agricultural Sector', 'Adopt sustainable farm', 'Promote reforestation',
                        'Transition to low-emis', 'Encourage organic farm', 'Invest in renewable',
                        'Industrial Sector'))

# ── Perfect competition, from an earlier part of the paper ──────────────────
BODY = block(tidy(load(2025, 'ordinary')),
             'sellers to influence the price at which the product is sold', occ=0)
P.cards.append(card(
    'econ-2025-ol-q11-b-iii', 2025, 'ordinary', 'economics-2-0',
    'perfect-competition-consumer-advantage', '2025 OL Q11(b)(iii)',
    'As a consumer, what in your opinion is the main advantage of a perfectly competitive '
    'market? Explain your answer.',
    '1 @ 8', 8,
    [anyN('r-1', 'An advantage to the consumer — any one', 8, 1, 8,
          [as_option(h) for h in heads(
              block(BODY, 'Low prices - firms are competitive',
                    '(c) Dublin Airport has a passenger cap'),
              ['Low prices -', 'No Advertising', 'Efficient use of scarce resources'])],
          'One advantage, 8 marks. The question asks for an opinion and the scheme answers it '
          'with the three the examiner accepts.')],
    '', tariff_kind='bestNofParts'))

P.cards.append(card(
    'econ-2025-ol-q11-c-i', 2025, 'ordinary', 'economics-2-2', 'dublin-airport-passenger-cap',
    '2025 OL Q11(c)(i)',
    'Outline one reason why, in your opinion, a limit has been placed on the number of '
    'passengers who can pass through Dublin Airport.',
    '1 @ 8', 8,
    [anyN('r-1', 'A reason for the passenger cap — any one', 8, 1, 8,
          [as_option(h) for h in heads(
              block(BODY, 'Reduce emissions – flying creates a lot of emissions', 'Question 12'),
              ['Reduce emissions', 'Reduce traffic around Dublin airport',
               'Reduce noise pollution'])],
          'One reason, 8 marks.')],
    '', stem='Dublin Airport has a cap of 32 million passengers a year, which was exceeded in '
             '2024.', tariff_kind='bestNofParts'))

P.emit()
