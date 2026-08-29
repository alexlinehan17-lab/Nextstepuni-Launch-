#!/usr/bin/env python3
"""Economics 2023 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, card, load, point, tidy  # noqa: E402

P = Paper(2023, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses')
BODY = tidy(load(2023, 'ordinary'))

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

# The id counts the wrong part: the paper prints this question at Q15(c)(i) —
# (a)(i) is the private-car percentage calculation. The id is a review-history
# key and stays; the citation, which a student does see, says what the paper
# says. Same call as econ_refs.CORRECTIONS, made here because this script owns
# the card.
P.menu('ways the Irish government may influence consumers to switch to electric',
       'econ-2023-ol-q15-a-i', 'economics-1-3', 'encouraging-electric-vehicles',
       'Outline two ways the Irish government may influence consumers to switch to electric '
       'cars.',
       'A way to encourage electric cars — any two',
       'Two ways, the first paid 8 and the second 4.',
       ref='2023 OL Q15(c)(i)', drop=SCAFFOLD)

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

# ── The non-menu parts, sliced by hand ─────────────────────────────────────
# Q14(c)(i) was recorded in econ_excluded as welded — "the variable-cost
# definition is welded onto the fixed-cost examples line". Re-read with block()
# anchored at 'Examples:' and 'Variable costs:', all four halves separate
# cleanly, so the part is carded after all; the econ_excluded line is now stale.
P.cards.append(card(
    'econ-2023-ol-q14-c-i', 2023, 'ordinary', 'economics-1-5',
    'fixed-and-variable-costs', '2023 OL Q14(c)(i)',
    'Explain the terms fixed costs and variable costs and state one example of each.',
    'fixed', 18,
    [point('r-fixed-def', as_option(block(BODY, 'Fixed costs: costs which remain the same',
                                          'Examples: rent of premises')), 6,
           'The fixed-cost definition, 6 marks.'),
     point('r-fixed-ex', as_option(block(BODY, 'rent of premises, insurance, rates',
                                         'Variable costs:')), 3,
           'An example of a fixed cost — any one, 3 marks.'),
     point('r-var-def', as_option(block(BODY, 'Variable costs: costs which vary with output',
                                        'Examples: raw materials')), 6,
           'The variable-cost definition, 6 marks.'),
     point('r-var-ex', as_option(block(BODY, 'raw materials, electricity, wages, packaging',
                                       '(ii) Outline one reason why it is important')), 3,
           'An example of a variable cost — any one, 3 marks.')],
    'The scheme prints ⟨6⟩ on each definition and ⟨3⟩ on each examples line.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-ol-q11-b-iii', 2023, 'ordinary', 'economics-2-0',
    'efficiency-in-monopolistic-competition', '2023 OL Q11(b)(iii)',
    'Is the above firm producing efficiently? Give a reason for your answer.',
    'fixed', 2,
    [point('r-1', 'No.', 1, 'The stance, 1 mark.'),
     point('r-2', as_option(block(BODY, 'The firm is not producing at the minimum point',
                                  '(c) The hidden economy in the Hair')), 1,
           'The reason, 1 mark: equilibrium at E sits to the left of W, the minimum of the '
           'average cost curve.')],
    'The same long-run equilibrium diagram as (b)(i).',
    stem='The diagram represents the long run equilibrium of a firm in the hair and beauty '
         'industry.',
    tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p11-art',
    label_key=[{'letter': '1', 'meaning': 'AVERAGE COST', 'askedInThisQuestion': False},
               {'letter': '2', 'meaning': 'AVERAGE REVENUE / DEMAND', 'askedInThisQuestion': False},
               {'letter': '3', 'meaning': 'QUANTITY', 'askedInThisQuestion': False},
               {'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': False},
               {'letter': 'MR', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': False}]))

P.cards.append(card(
    'econ-2023-ol-q12-b-i', 2023, 'ordinary', 'economics-3-1',
    'equity-in-taxation', '2023 OL Q12(b)(i)',
    'Equity is one of the principles of a good tax system. Explain the term equity.',
    '1 @ 8', 8,
    [point('r-1', as_option(block(BODY, 'This means the more income you earn',
                                  '(ii) Explain two other principles')), 8,
           'One explanation, 8 marks.')],
    '', tariff_kind='fixed'))

# ⟨3⟩ is printed for the three pillars together; three names for three marks is
# the only integral split, and each point carries it.
P.cards.append(card(
    'econ-2023-ol-q12-c-iii', 2023, 'ordinary', 'economics-0-2',
    'three-pillars-of-sustainability', '2023 OL Q12(c)(iii)',
    'Name the three pillars of sustainability.',
    'fixed', 3,
    [point('r-1', 'Economic', 1, 'The first pillar.'),
     point('r-2', 'Environment', 1, 'The second.'),
     point('r-3', 'Social', 1, 'The third.')],
    'The scheme prints ⟨3⟩ against the three names together.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-ol-q13-b-i', 2023, 'ordinary', 'economics-3-0',
    'letters-in-the-national-income-formula', '2023 OL Q13(b)(i)',
    'State what each of the letters C and G represent.',
    '2 @ 4', 8,
    [point('r-1', 'Consumption expenditure', 4, 'The C.'),
     point('r-2', 'Government expenditure', 4, 'The G.')],
    '',
    stem='National Income is calculated using the following formula: National Income (Y) = '
         'C + Investment + G + Exports – Imports.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-ol-q15-a-ii', 2023, 'ordinary', 'economics-1-3',
    'subsidising-public-transport', '2023 OL Q15(a)(ii)',
    'The Irish government are currently subsiding the users of public transport. Explain the '
    'term subsidy in the context of public transport.',
    '1 @ 5', 5,
    [point('r-1', as_option(block(BODY, 'The Irish government is paying part of the cost',
                                  'Draw and label')), 5,
           'One explanation, 5 marks.')],
    '', tariff_kind='fixed'))

# The factors-of-production table. Six cells are blank on the paper and the
# scheme prints ⟨6 @ 4⟩ over its completed copy, setting the answers in caps —
# each blank cell is a point here, lifted from the scheme's own table cells.
# The id carries a suffix because econ-2023-ol-q16-a-i is the terms card whose
# citation econ_refs corrects to Q16(b)(i).
P.cards.append(card(
    'econ-2023-ol-q16-a-i-factors', 2023, 'ordinary', 'economics-0-1',
    'factors-of-production', '2023 OL Q16(a)(i)',
    'Complete the table below to show your understanding of the factors of production used in '
    'the production of Keogh’s Crisps. Some of the information has been completed for you.',
    '6 @ 4', 24,
    # One anyN row, not six point rows: six cells at 4 marks each is over the
    # five-row structural cap for fixed cards, and the table IS a claim-six
    # menu — each option one blank cell, in the scheme's own capitals.
    [anyN('r-1', 'A completed cell of the table — all six', 24, 6, 4,
          ['POTATOES SALT OIL',
           'LABOUR',
           'THE HUMAN EFFORT INVOLVED IN THE PRODUCTION OF A GOOD OR SERVICE.',
           'ANYTHING MADE BY HUMANS WHICH IS USED IN PRODUCTION.',
           'ENTERPRISE',
           'TOM KEOGH'],
          'The blank cells in order: the land example (any one of the three), '
          'the labour row name and explanation, the capital explanation, and '
          'the enterprise row name and example — 4 marks each.')],
    'The rows the paper leaves blank: the land example, the labour row’s name and '
    'explanation, the capital explanation, and the enterprise row’s name and example.',
    tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p25-i0'))

P.cards.append(card(
    'econ-2023-ol-q16-b-ii', 2023, 'ordinary', 'economics-1-5',
    'economies-of-scale-ol', '2023 OL Q16(b)(ii)',
    'This expansion will allow Keogh’s Crisps to benefit from economies of scale. Explain the '
    'term economies of scale with reference to Keogh’s crisps.',
    '1 @ 7', 7,
    [point('r-1', as_option(block(BODY, 'Economies of scale arise as the firm increases',
                                  'In Ireland, we generate')), 7,
           'One explanation, 7 marks.')],
    '',
    stem='Keogh’s Crisps are due to increase production capacity by 50%.',
    tariff_kind='fixed'))

# ── The parts whose question IS a chart ────────────────────────────────────
# Excluded until now as "every response reads the chart printed with it". That
# was true of the response and was never a reason to leave the part out: the
# crop is catalogued, carries verified alt text and an md5 the build re-checks,
# and the scheme's responses are ordinary prose that quotes figures off it.
# With the figure bound the student has exactly what the candidate in the hall
# had.

P.cards.append(card(
    'econ-2023-ol-q14-a-i', 2023, 'ordinary', 'economics-3-3',
    'trend-in-petrol-prices', '2023 OL Q14(a)(i)',
    'Comment on one key trend in the price of petrol in the line graph above, using '
    'information from the line graph.',
    '1 @ 10', 10,
    [anyN('r-1', 'One key trend, quoted off the graph \u2014 any one', 10, 1, 10,
          [as_option(block(BODY, 'From April to June 2022, petrol prices increased steadily',
                           'From June 2022 to September 2022 petrol prices fell')),
           as_option(block(BODY, 'From June 2022 to September 2022 petrol prices fell',
                           'Outline one reason why the price of petrol changed'))],
          'One trend, 10 marks, written (6+4): 6 for the trend and 4 for the figures taken off '
          'the graph. The two halves of the year run opposite ways and either is accepted.')],
    'The graph rises to a June peak and falls back after it, so "petrol got dearer in 2022" is '
    'only half of what the line shows.',
    figure_key='economics-2023-OL-paper-p19-art'))


# ── Backfill: asks the scheme answers in full ──────────────────────────────

P.cards.append(card(
    'econ-2023-ol-q12-a-i', 2023, 'ordinary', 'economics-3-1',
    'total-planned-government-revenue', '2023 OL Q12(a)(i)',
    'Using the figures in the pie chart above, calculate how much the government is expecting to '
    'receive in revenue. Show your workings.',
    '16', 16,
    [point('r-1', as_option(block(BODY, '\u20ac27.5m + \u20ac14m + \u20ac17m',
                                  'Deduct 1 mark each for omission')), 16,
           'Every slice is added, including the two small ones. The scheme deducts a mark each '
           'for dropping the \u20ac or the "million", so the units are part of the answer rather '
           'than decoration.')],
    'Six slices, and the two smallest are easy to skip \u2014 leaving either out changes the '
    'total the NEXT part divides by.',
    tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p13-i0'))

P.cards.append(card(
    'econ-2023-ol-q12-a-ii', 2023, 'ordinary', 'economics-3-1',
    'income-tax-as-a-share-of-revenue', '2023 OL Q12(a)(ii)',
    'Using your answer from (i) above calculate what percentage of government revenue will be '
    'received in income tax. Show your workings.',
    '12', 12,
    [point('r-1', as_option(block(BODY, '\u20ac27.5m / \u20ac95m x 100 = 28.94%',
                                  '(iii)')), 12,
           'Income tax over the TOTAL from part (i), not over any single other slice. A wrong '
           'total in (i) carries straight through, which is why the scheme prints the €95m again '
           'here.')],
    'The answer depends on the previous part, so an error in the total is paid for twice.',
    tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p13-i0'))

P.emit()
