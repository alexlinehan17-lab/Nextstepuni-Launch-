#!/usr/bin/env python3
"""Economics 2023 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import card, point  # noqa: E402

P = Paper(2023, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('hair and beauty industries are an', 'econ-2023-ol-q11-a-i',
       'economics-2-0', 'monopolistic-competition-identified',
       'Outline two reasons why, in your opinion, the hair and beauty industries are an example '
       'of monopolistic competition.',
       'A reason it is monopolistic competition — any two',
       'Two reasons, the first paid 6 and the second 4.',
       drop=SCAFFOLD + ('example of monopolistic',))

P.menu('advantages for consumers of monopolistic competition', 'econ-2023-ol-q11-a-ii',
       'economics-2-0', 'monopolistic-competition-consumer-advantages',
       'Outline two advantages for consumers of monopolistic competition.',
       'An advantage to consumers — any two',
       'Two advantages, the first paid 6 and the second 4.',
       drop=SCAFFOLD)

P.menu('one effect the hidden economy in the hair and beauty industry', 'econ-2023-ol-q11-c-ii',
       'economics-3-1', 'effects-of-the-hidden-economy-ol',
       'Outline one effect the hidden economy in the hair and beauty industry has on businesses '
       'in this industry and on the Irish Government.',
       'An effect of the hidden economy — any two',
       'The paper pays 6 for the effect on business and 4 for the effect on government; the '
       'scheme lists the business effects first.',
       drop=SCAFFOLD + ('businesses in this indus',))

P.menu('other principles of a good tax system', 'econ-2023-ol-q12-b-ii',
       'economics-3-1', 'principles-of-a-good-tax-system',
       'Explain two other principles of a good tax system that you would consider important in '
       'the current economic climate.',
       'A principle of a good tax system — any two',
       'Two principles, the first paid 8 and the second 4. Equity — ability to pay — is excluded '
       'by the question.',
       drop=SCAFFOLD + ('in the current economic',))

P.menu('actions an Irish household could take to reduce their electricity', 'econ-2023-ol-q12-c-ii',
       'economics-0-2', 'household-actions-to-cut-electricity-use',
       'Describe two actions an Irish household could take to reduce their electricity bills and '
       'make them more sustainable.',
       'An action the household could take — any two',
       'Two actions, the first paid 10 and the second 4.',
       drop=SCAFFOLD + ('make them more sustainab',))

P.menu('advantages of exports for the Irish economy', 'econ-2023-ol-q13-a-ii',
       'economics-4-2', 'advantages-of-exports',
       'Describe two advantages of exports for the Irish economy.',
       'An advantage of exports — any two',
       'Two advantages, the first paid 8 and the second 2.',
       drop=SCAFFOLD)

P.menu('ways the Irish government may influence consumers to switch to electric',
       'econ-2023-ol-q15-a-i', 'economics-1-3', 'encouraging-electric-vehicles',
       'Outline two ways the Irish government may influence consumers to switch to electric '
       'vehicles.',
       'A way to encourage electric vehicles — any two',
       'Two ways, the first paid 8 and the second 4.',
       drop=SCAFFOLD)

P.menu('Explain any two of the above terms', 'econ-2023-ol-q16-a-i',
       'economics-0-1', 'properties-of-an-economic-good',
       'Explain any two of the following terms: scarce; transferable; utility.',
       'One of the three terms — any two',
       'Two terms, 7 marks each. The scheme explains each against the same example, a bag of '
       'crisps.',
       drop=SCAFFOLD)

P.menu('benefit of this electricity credit', 'econ-2023-ol-q12-c-i',
       'economics-1-3', 'benefit-of-the-electricity-credit',
       'Outline one benefit of the €600 electricity credit to the Irish household.',
       'A benefit to the household — any one',
       'One benefit, 10 marks.',
       claim=1, per=10, drop=SCAFFOLD)


# ── A figure card ───────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2023-ol-q11-b-i', 2023, 'ordinary', 'economics-2-0',
    'labelling-monopolistic-competition', '2023 OL Q11(b)(i)',
    'The diagram represents the long run equilibrium of a firm in the hair and beauty industry. '
    'Write out in full what each of the three numbered items represents.',
    'fixed', 24,
    [point('r-1', 'AVERAGE COST', 8, 'Item 1 — the blue U-shaped curve, whose minimum is point W.'),
     point('r-2', 'AVERAGE REVENUE / DEMAND', 8, 'Item 2 — the yellow line falling to the right.'),
     point('r-3', 'QUANTITY', 8, 'Item 3 — the horizontal axis. MC and MR are already labelled.')],
    'Abbreviations are not accepted.', tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p11-art',
    label_key=[{'letter': '1', 'meaning': 'AVERAGE COST', 'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'AVERAGE REVENUE / DEMAND', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'QUANTITY', 'askedInThisQuestion': True},
               {'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': False},
               {'letter': 'MR', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': False}]))


# ── Section B, second pass ──────────────────────────────────────────────────
P.menu('Explain the term hidden economy', 'econ-2023-ol-q11-c-i',
       'economics-3-1', 'what-the-hidden-economy-is-ol',
       'Explain the term hidden economy. Give one other example of an activity in the Irish '
       'hidden economy.',
       'A way of putting it — any one',
       'One explanation, 6 marks. The three the scheme lists are the same idea said three ways.',
       ref='2023 OL Q11(c)(i)', claim=1, per=6,
       drop=SCAFFOLD + ('Give one other example',))

P.menu('increase in interest rates would affect consumers', 'econ-2023-ol-q13-c-i',
       'economics-3-3', 'interest-rates-and-mortgage-holders',
       'Explain how an increase in interest rates would affect consumers with a mortgage.',
       'An effect on mortgage holders — any one', 'One effect, 8 marks.',
       ref='2023 OL Q13(c)(i)', claim=1, per=8, drop=SCAFFOLD)

P.menu('increase in interest rates could affect savings', 'econ-2023-ol-q13-c-ii',
       'economics-3-3', 'interest-rates-and-saving',
       'Outline how an increase in interest rates could affect savings in the Irish economy.',
       'An effect on savings — any one',
       'One effect, 8 marks. The scheme accepts savings rising, falling, or not moving at all — '
       'what is marked is the reasoning.',
       ref='2023 OL Q13(c)(ii)', claim=1, per=8, drop=SCAFFOLD)

P.menu('switching to the online banking app', 'econ-2023-ol-q13-c-iii',
       'economics-3-4', 'why-consumers-switch-bank',
       'Outline one reason why consumers are switching to online banking apps such as Revolut.',
       'A reason to switch — any one', 'One reason, 2 marks.',
       ref='2023 OL Q13(c)(iii)', claim=1, per=2, drop=SCAFFOLD)

P.menu('price of petrol changed from April to June', 'econ-2023-ol-q14-a-ii-reason',
       'economics-3-3', 'why-petrol-prices-rose',
       'Outline one reason why the price of petrol changed from April to June 2022.',
       'The reason the price rose',
       'One reason, 8 marks; the part pays 4 more for the effect on consumers.',
       ref='2023 OL Q14(a)(ii) — reason', claim=1, per=8,
       drop=SCAFFOLD, stop='Effect:',
       notes='The part asks for a reason and an effect, and the scheme heads the two separately, '
             'so each is its own card.')

P.menu('price of petrol changed from April to June', 'econ-2023-ol-q14-a-ii-effect',
       'economics-3-3', 'effect-of-higher-petrol-prices',
       'Outline one reason why the price of petrol changed from April to June and explain one '
       'effect this had on Irish consumers — the EFFECT.',
       'The effect on consumers', 'One effect, 4 marks.',
       ref='2023 OL Q14(a)(ii) — effect', claim=1, per=4,
       drop=SCAFFOLD, after='Effect:')

P.menu('shortage of parts for making electronic devices', 'econ-2023-ol-q14-b-iii',
       'economics-1-2', 'why-a-global-parts-shortage',
       'A shortage of parts for making electronic devices has developed worldwide. Explain one '
       'possible reason for this shortage of parts.',
       'A reason for the shortage — any one', 'One reason, 3 marks.',
       ref='2023 OL Q14(b)(iii)', claim=1, per=3,
       drop=SCAFFOLD + ('Explain one possible reason for this shortage',))

P.menu('important for a business to continue to earn profit', 'econ-2023-ol-q14-c-ii',
       'economics-1-5', 'why-profit-matters',
       'Outline one reason why it is important for a business to continue to earn profit.',
       'A reason profit matters — any one', 'One reason, 5 marks.',
       ref='2023 OL Q14(c)(ii)', claim=1, per=5, drop=SCAFFOLD)

P.menu('factor, other than an increase in income, that would affect the demand',
       'econ-2023-ol-q15-b-iii', 'economics-1-1', 'what-shifts-demand-for-electric-cars',
       'Explain one factor, other than an increase in income, that would affect the demand for '
       'electric cars in a market.',
       'A factor shifting demand — any one', 'One factor, 5 marks.',
       ref='2023 OL Q15(b)(iii)', claim=1, per=5,
       drop=SCAFFOLD + ('electric cars in a market.',))

# ── Q16(c): food waste ─────────────────────────────────────────────────────
P.menu('cost to society of wasting food', 'econ-2023-ol-q16-c-i',
       'economics-0-2', 'the-social-cost-of-food-waste',
       'Outline one cost to society of wasting food.',
       'A cost to society — any one', 'One cost, 8 marks. The scheme lists seven.',
       ref='2023 OL Q16(c)(i)', claim=1, per=8, drop=SCAFFOLD)

P.menu('action consumers could take to reduce food waste', 'econ-2023-ol-q16-c-ii',
       'economics-0-2', 'how-consumers-can-cut-food-waste',
       'Describe one action consumers could take to reduce food waste.',
       'An action a consumer can take — any one', 'One action, 8 marks. The scheme lists six.',
       ref='2023 OL Q16(c)(ii)', claim=1, per=8, drop=SCAFFOLD)

P.menu('action producers could take to reduce food waste', 'econ-2023-ol-q16-c-iii',
       'economics-0-2', 'how-producers-can-cut-food-waste',
       'Describe one action producers could take to reduce food waste.',
       'An action a producer can take — any one', 'One action, 8 marks.',
       ref='2023 OL Q16(c)(iii)', claim=1, per=8, drop=SCAFFOLD)

P.menu('social benefit for Ireland if more consumers switch to hybrid and electric',
       'econ-2023-ol-q15-c-ii', 'economics-0-2', 'social-benefits-of-electric-cars',
       'Describe one social benefit for Ireland if more consumers switch to hybrid and '
       'electric cars.',
       'A social benefit — any one', 'One benefit, 8 marks.',
       ref='2023 OL Q15(c)(ii)', claim=1, per=8, drop=SCAFFOLD)

P.menu('entrepreneurs important to the development of the Irish economy',
       'econ-2023-ol-q16-a-ii', 'economics-1-5', 'why-entrepreneurs-matter',
       'In your opinion are entrepreneurs important to the development of the Irish economy? '
       'Explain your answer.',
       'A reason entrepreneurs matter — any one', 'One reason, 4 marks after 2 for the stance.',
       ref='2023 OL Q16(a)(ii)', claim=1, per=4, drop=SCAFFOLD)

# Q14(c)(i) is not carded: the scheme welds the variable-cost definition onto
# the end of the fixed-cost examples line — "Examples: rent of premises,
# insurance, rates ... Variable costs: costs which vary with output" — so
# neither half separates cleanly and a card would carry the other's definition.

P.emit()
