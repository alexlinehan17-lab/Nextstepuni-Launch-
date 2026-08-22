#!/usr/bin/env python3
"""Economics 2025 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, card, heads, load, tidy  # noqa: E402

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


# ── A figure card ───────────────────────────────────────────────────────────
# The one labelling part in the five years that is a genuine choice: four
# labels are printed and any three earn the marks.
P.cards.append(card(
    'econ-2025-ol-q11-b-i', 2025, 'ordinary', 'economics-2-0',
    'labelling-perfect-competition-ol', '2025 OL Q11(b)(i)',
    'The diagram represents the long-run equilibrium of a firm in perfect competition. Write out '
    'in full what any three of the four labels represent.',
    '3 @ 8', 24,
    [anyN('r-1', 'A label written out in full — any three', 24, 3, 8,
          ['Marginal Cost', 'Quantity', 'Demand / Average Revenue / Marginal Revenue',
           'Average Cost'],
          'Three labels, 8 marks each. Abbreviations are not accepted.')],
    '', tariff_kind='bestNofParts',
    figure_key='economics-2025-OL-paper-p12-art',
    label_key=[{'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
               {'letter': 'Q', 'meaning': 'Quantity', 'askedInThisQuestion': True},
               {'letter': 'D = AR = MR',
                'meaning': 'Demand / Average Revenue / Marginal Revenue', 'askedInThisQuestion': True},
               {'letter': 'AC', 'meaning': 'Average Cost', 'askedInThisQuestion': True},
               {'letter': 'E', 'meaning': 'long-run equilibrium, where marginal cost cuts average '
                                          'cost at its minimum', 'askedInThisQuestion': False}]))


# ── Section B, second pass ──────────────────────────────────────────────────
SIDES4 = ('The part asks for one of each and the scheme heads the two lists separately, so each '
          'side is its own card.')

P.menu('two assumptions of perfect competition', 'econ-2025-ol-q11-a-ii',
       'economics-2-0', 'assumptions-of-perfect-competition-ol',
       'Outline two assumptions of perfect competition, other than homogenous products.',
       'An assumption of perfect competition — any two',
       'Two assumptions, the first paid 10 and the second 4. Homogenous products is excluded by '
       'the question.',
       ref='2025 OL Q11(a)(ii)', steps=[10, 4], drop=SCAFFOLD)

P.menu('Outline one aim of the ECB', 'econ-2025-ol-q12-c-ii',
       'economics-3-3', 'aims-of-the-ecb',
       'The ECB decreased interest rates in 2024. Outline one aim of the ECB.',
       'An aim of the ECB — any one', 'One aim, 4 marks.',
       ref='2025 OL Q12(c)(ii)', claim=1, per=4, drop=SCAFFOLD)

P.menu('economic measure the Irish government or employers could take',
       'econ-2025-ol-q13-a-iii-gov', 'economics-2-1', 'government-action-on-skills',
       'Outline one economic measure the Irish government or employers could take to help '
       'increase the supply of skilled labour in the economy — the GOVERNMENT’s side.',
       'A measure for the government — any one', 'One measure, 7 marks.',
       ref='2025 OL Q13(a)(iii) — government', claim=1, per=7,
       drop=SCAFFOLD + ('Irish government',), stop='Responses for employers', notes=SIDES4)

P.menu('economic measure the Irish government or employers could take',
       'econ-2025-ol-q13-a-iii-emp', 'economics-2-1', 'employer-action-on-skills',
       'Outline one economic measure the Irish government or employers could take to help '
       'increase the supply of skilled labour in the economy — the EMPLOYERS’ side.',
       'A measure for employers — any one', 'One measure, 7 marks.',
       ref='2025 OL Q13(a)(iii) — employers', claim=1, per=7,
       drop=SCAFFOLD, after='Responses for employers')

P.menu('Ukraine and Moldova have applied for membership', 'econ-2025-ol-q14-a-iii',
       'economics-4-2', 'enlarging-the-european-union',
       'Ukraine and Moldova have applied for membership of the European Union. Outline one reason '
       'why Ireland might support their application.',
       'A reason to support enlargement — any one', 'One reason, 4 marks.',
       ref='2025 OL Q14(a)(iii)', claim=1, per=4, drop=SCAFFOLD)

P.menu('measure a country can take to help it improve its HDI', 'econ-2025-ol-q14-c-ii',
       'economics-4-0', 'raising-a-countrys-hdi',
       'Suggest one measure a country can take to help it improve its HDI score.',
       'A measure to raise HDI — any one', 'One measure, 10 marks.',
       ref='2025 OL Q14(c)(ii)', claim=1, per=10,
       drop=SCAFFOLD + ('Possible Responses',))

P.menu('permanently shut their doors in the last year', 'econ-2025-ol-q15-a-iii',
       'economics-3-5', 'when-hospitality-businesses-close',
       'More than 570 restaurants, cafes and other food businesses have permanently shut in the '
       'last year. Discuss one effect this development may have on local communities.',
       'An effect on the community — either one', 'One effect, 10 marks.',
       ref='2025 OL Q15(a)(iii)', claim=1, per=10, drop=SCAFFOLD)

P.menu('Restrictions were introduced limiting the movement of cars', 'econ-2025-ol-q15-b-iii-pos',
       'economics-2-2', 'traffic-restrictions-positive',
       'Restrictions were introduced limiting the movement of cars on the Quays in Dublin City '
       'centre. Outline one POSITIVE effect for people who live in Dublin.',
       'A positive effect — any one', 'One effect, 6 marks.',
       ref='2025 OL Q15(b)(iii) — positive', claim=1, per=6,
       drop=SCAFFOLD + ('Positive Effects',), stop='Negative Effects', notes=SIDES4)

P.menu('Restrictions were introduced limiting the movement of cars', 'econ-2025-ol-q15-b-iii-neg',
       'economics-2-2', 'traffic-restrictions-negative',
       'Restrictions were introduced limiting the movement of cars on the Quays in Dublin City '
       'centre. Outline one NEGATIVE effect for people who live in Dublin.',
       'A negative effect — any one', 'One effect, 6 marks.',
       ref='2025 OL Q15(b)(iii) — negative', claim=1, per=6,
       drop=SCAFFOLD, after='Negative Effects')

P.menu('Excise duty is charged on certain goods', 'econ-2025-ol-q16-a-ii',
       'economics-3-1', 'why-tax-alcohol-and-tobacco',
       'Explain one reason why the government places taxes on goods such as alcohol and '
       'cigarettes.',
       'A reason for the tax — any one', 'One reason, 10 marks.',
       ref='2025 OL Q16(a)(ii)', claim=1, per=10, drop=SCAFFOLD)

P.menu('promote Balanced Regional', 'econ-2025-ol-q16-c-ii',
       'economics-3-1', 'balanced-regional-development',
       'One aim of the Irish government is to promote Balanced Regional Development throughout '
       'Ireland. Suggest one measure the government could take to help achieve this aim.',
       'A measure for regional development — any one', 'One measure, 6 marks.',
       ref='2025 OL Q16(c)(ii)', claim=1, per=6,
       drop=SCAFFOLD + ('Irish government could take to help achieve',))

# ── further Section B parts ────────────────────────────────────────────────
P.menu('economic term homogenous product', 'econ-2025-ol-q11-a-i',
       'economics-2-1', 'what-a-homogenous-product-is',
       'Explain the economic term homogenous product and give one example of a homogenous '
       'product.',
       'The explanation and an example — both of these',
       'Explanation and example, 6 marks between them.',
       ref='2025 OL Q11(a)(i)', claim=2, per=3, drop=SCAFFOLD)

# Q12(b)(i) is not carded: it asks what C, G and X each stand for, and the
# scheme's three answers come out welded across two lines — "Consumption
# expenditure G:" and "Government Spending X: Exports" — so a card would show a
# letter run onto the end of the answer before it.

# The plain id belongs to a card citing 2025 OL Q16(a)(iii) on falling
# inflation — another part whose reconstructed path is a numeral out.
P.menu('Cross-border shopping & loss of revenue', 'econ-2025-ol-q16-a-iii-excise',
       'economics-3-1', 'downside-of-raising-excise-on-alcohol-and-tobacco',
       'Outline one possible negative effect for the Irish economy if it continues to '
       'increase excise duty on alcohol and tobacco.',
       'A negative effect — any one', 'One effect, 8 marks.',
       ref='2025 OL Q16(a)(iii)', claim=1, per=8, drop=SCAFFOLD)

# The scheme lists the two groups the question names — savers, then borrowers —
# and gives an effect for each, so both are rows on one card.
P.menu('Savers may decide to save less', 'econ-2025-ol-q12-c-iii',
       'economics-3-4', 'who-gains-when-interest-rates-fall',
       'Explain the economic effect interest rate decreases could have on savers in Ireland '
       'and on borrowers who are repaying mortgages.',
       'The effect on each group — both of these', 'Savers 6 and borrowers 4.',
       ref='2025 OL Q12(c)(iii)', claim=2, per=6, steps=[6, 4],
       drop=SCAFFOLD + ('Savers in Ireland • Borrowers who are repaying mortgages',))

P.emit()
