#!/usr/bin/env python3
"""Economics 2021 Higher Level — Section A.

Section A is 75 of this paper's 300 marks and reads, on a first skim, like
chart lookups. Most of it is not: "Outline two reasons why achieving a trade
surplus is an objective of the Irish government" is answered by a list of named
responses and needs no chart at all.

What is deliberately not carded, and why:

  * a part answered by reading the figure printed with it — "compare the level
    of gross debt per person from 2007 to 2019". The figure pipeline could
    carry those, but the card would then test chart-reading, not economics.
  * a part whose responses are worked to the student's own earlier choice —
    "give one reason for each of your chosen market structures above".

Every reference here is the one the QUESTION PAPER gives, not the one the
scheme's running order implies; econ_refcheck.py derives it again and compares.
The two disagree more often than they look like they should — the scheme prints
question 3's first part on the page it heads question 2.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, card, load, point, tidy  # noqa: E402

P = Paper(2021, 'higher', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('reasons why achieving a trade surplus is an objective', 'econ-2021-hl-sa-q1-b',
       'economics-4-2', 'why-a-trade-surplus-is-an-aim',
       'Outline two reasons why achieving a trade surplus is an objective of the Irish government.',
       'A reason a trade surplus is an aim — both of these',
       'Two reasons, 4 marks each, and the scheme lists exactly two.',
       ref='2021 HL Section A Q1(b)', drop=SCAFFOLD)

P.menu('willing to pay different prices for a Netflix subscription', 'econ-2021-hl-sa-q3-a',
       'economics-1-1', 'why-consumers-accept-different-prices',
       'Outline one reason why consumers are willing to pay different prices for the same '
       'Netflix subscription in different countries.',
       'A reason consumers accept the difference — any one',
       'One reason, 5 marks: 2 for naming it and 3 for explaining it.',
       ref='2021 HL Section A Q3(a)', claim=1, per=5, drop=SCAFFOLD,
       stem='A basic Netflix account cost far more per month in Switzerland than in Rwanda.')

P.menu('other conditions necessary for price discrimination', 'econ-2021-hl-sa-q3-b',
       'economics-1-1', 'conditions-for-price-discrimination-hl',
       'Explain two conditions, other than the willingness of consumers to pay, that are '
       'necessary for price discrimination to occur.',
       'A condition for price discrimination — both of these',
       'Two conditions, 5 marks each.',
       ref='2021 HL Section A Q3(b)', drop=SCAFFOLD)

P.menu('other duties of the Central Bank', 'econ-2021-hl-sa-q5-b',
       'economics-3-4', 'duties-of-the-central-bank',
       'Other than the regulation of commercial banks, outline two other duties of the Central '
       'Bank of Ireland.',
       'A duty of the Central Bank — any two',
       'Two duties, 4 marks each. Regulating the commercial banks is excluded by the question.',
       ref='2021 HL Section A Q5(b)', drop=SCAFFOLD)

P.menu('advise the governments of these countries on one policy', 'econ-2021-hl-sa-q6-b',
       'economics-4-0', 'policies-to-raise-a-countrys-hdi',
       'Advise the governments of the countries lowest on the Human Development Index on one '
       'policy they could use to improve their HDI ranking.',
       'A policy that would raise HDI — any one',
       'One policy, 8 marks: 4 for the policy and 4 for explaining how it raises the ranking.',
       ref='2021 HL Section A Q6(b)', claim=1, per=8, drop=SCAFFOLD,
       stem='Chad, the Central African Republic and Niger ranked 187th, 188th and 189th on the '
            'HDI in 2020.')

P.menu('Advise the Irish government on how it could assist', 'econ-2021-hl-sa-q6-c',
       'economics-4-0', 'how-a-rich-country-can-assist-ldcs',
       'Advise the Irish government on how it could assist the countries lowest on the Human '
       'Development Index to improve their HDI ranking.',
       'A way Ireland could assist — any one',
       'One way, 8 marks: 4 for the measure and 4 for explaining it. The paper offers this part '
       'or the one before it, not both.',
       ref='2021 HL Section A Q6(c)', claim=1, per=8, drop=SCAFFOLD)

P.menu('economic disadvantages for a government in achieving a budget surplus',
       'econ-2021-hl-sa-q7-b', 'economics-3-1', 'disadvantages-of-a-budget-surplus',
       'Explain the economic disadvantages for a government in achieving a budget surplus.',
       'A disadvantage of a budget surplus — any two',
       'Two disadvantages, 3 marks each.',
       ref='2021 HL Section A Q7(b)', drop=SCAFFOLD)

# ── The definition-shaped parts, built from the scheme directly ────────────
# Each prints one tariff cell over one stated answer, so these are point cards
# sliced with block() rather than menus — the extractor hands them back with
# the answer welded to the question and nothing to claim.
BODY = tidy(load(2021, 'higher'))

P.cards.append(card(
    'econ-2021-hl-sa-q4-a', 2021, 'higher', 'economics-2-2', 'demerit-goods',
    '2021 HL Section A Q4(a)',
    'Explain your understanding of the economic term Demerit Goods.',
    '4 + 3', 7,
    [point('r-1', as_option(block(BODY, 'Demerit goods are goods whose positive effect',
                                  'Answer part (b) or (c)')), 7,
           'The scheme splits the 7 as 4 + 3: the definition, then the negative '
           'externalities demerit goods carry.')],
    '', section='A', tariff_kind='fixed',
    stem='In Budget 2021 the price of a 20 pack of cigarettes rose from €13.50 to €14.00. '
         'Cigarettes are classed as Demerit Goods and as such their purchase constitutes a '
         'market failure.'))

P.cards.append(card(
    'econ-2021-hl-sa-q4-b', 2021, 'higher', 'economics-2-2', 'cigarettes-and-market-failure',
    '2021 HL Section A Q4(b)',
    'Explain why the purchase of demerit goods, such as cigarettes, is seen as a market '
    'failure.',
    '4 + 4', 8,
    [point('r-1', as_option(block(BODY, 'The purchase of demerit goods is seen as a market '
                                        'failure as',
                                  'OR (c) Explain why the Irish Government')), 8,
           'The scheme splits the 8 as 4 + 4: the free market over-produces and over-consumes '
           'the good, and its price fails to reflect the true private or social cost.')],
    'The paper offers part (b) or part (c), not both; the one printed 8-mark tariff covers '
    'whichever is answered.', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-sa-q4-c', 2021, 'higher', 'economics-2-2', 'taxing-demerit-goods',
    '2021 HL Section A Q4(c)',
    'Explain why the Irish Government intervenes by imposing higher taxes on cigarettes in '
    'budgets.',
    '4 + 4', 8,
    [point('r-1', as_option(block(BODY, 'The government intervenes in order to increase the '
                                        'price',
                                  '5 | P a g e')), 8,
           'One explanation, 8 marks: the tax deters consumption of a harmful good, and the '
           'revenue helps fund the cost of its negative externalities.')],
    'The paper offers part (b) or part (c), not both. The scheme prints its one 8-mark (4 + 4) '
    'cell over the pair, and question 4 carries 15 in total: 7 for part (a) and 8 for this '
    'slot.', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-sa-q5-a', 2021, 'higher', 'economics-3-4',
    'why-bank-regulation-protects-consumers', '2021 HL Section A Q5(a)',
    'Based upon the above statement outline why it is important for consumers that Irish '
    'banks are properly regulated by the Central Bank of Ireland.',
    '7', 7,
    [point('r-1', as_option(block(BODY, 'Protection of consumer of financial services',
                                  '(b) Other than regulation of commercial banks')), 7,
           'One reason, 7 marks: unregulated banks may fail to operate within the guidelines, '
           'and consumers are the ones exploited when they do.')],
    '', section='A', tariff_kind='fixed',
    stem='KBC Bank Ireland has been fined €18.3 million by the Central Bank of Ireland for '
         'its role in the State’s tracker mortgage scandal.'))

P.cards.append(card(
    'econ-2021-hl-sa-q6-a', 2021, 'higher', 'economics-4-0', 'hdi-versus-gdp',
    '2021 HL Section A Q6(a)',
    'Explain why the Human Development Index (HDI) may provide a more accurate profile of '
    'human welfare in a country than the Gross Domestic Product (GDP) figure of that country.',
    '4 + 3', 7,
    [point('r-1', as_option(block(BODY, 'The HDI is a more accurate indicator of human welfare',
                                  'Answer question (b) or (c)')), 7,
           'The scheme splits the 7 as 4 + 3: the HDI is a composite of income per person, '
           'education and life expectancy, where GDP reflects production alone.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-sa-q7-c', 2021, 'higher', 'economics-3-1',
    'national-debt-and-opportunity-cost', '2021 HL Section A Q7(c)',
    'Servicing the national debt creates opportunity costs, explain how this occurs.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Servicing the national debt involves using up scarce '
                                        'resources',
                                  '9 | P a g e')), 6,
           'One explanation, 6 marks: the resources used on repayments are the alternative '
           'government uses forgone.')],
    'The paper offers part (b) or part (c), not both. Question 7 carries 15 marks: 9 for part '
    '(a), so this slot pays the 6 the scheme prices part (b) at.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-sa-q10-a', 2021, 'higher', 'economics-3-3', 'why-ecb-rates-fell-to-zero',
    '2021 HL Section A Q10(a)',
    'Explain the historical reason for this trend in the European Central Bank’s interest '
    'rate.',
    '8', 8,
    [point('r-1', as_option(block(BODY, 'In the wake of the great recession in 2008 there was '
                                        'a credit crunch',
                                  '(b) Outline whether you would advise')), 8,
           'One explanation, 8 marks: the post-2008 credit crunch, and the cuts made to '
           'cheapen borrowing and encourage growth.')],
    '', section='A', tariff_kind='fixed',
    figure_key='economics-2021-HL-paper-p14-art'))


# ── The part whose question IS a chart ─────────────────────────────────────
# Excluded until now as a lookup off the figure printed with it. That described
# the response, not a blocker: the crop is catalogued with verified alt text and
# an md5 the build re-checks, so binding it gives the student what the candidate
# in the hall had.

P.cards.append(card(
    'econ-2021-hl-seca-q7-a', 2021, 'higher', 'economics-3-1',
    'gross-debt-per-person-2007-to-2019', '2021 HL Section A Q7(a)',
    'Compare the level of Gross Debt per Person from 2007 to 2019 and outline one possible '
    'reason for this increase in the gross debt per person.',
    '5 + 4', 9,
    [point('r-1', as_option(block(BODY, 'Between 2007 and 2019 the gross debt per person rose',
                                  'Reason:')), 5,
           'The comparison, 5 marks. The infographic prints three debt-per-person figures and '
           'the scheme quotes the movement between them, so the marks are for the numbers as '
           'much as for the direction \u2014 and the middle of the period runs the other way '
           'from the ends.'),
     point('r-2', as_option(block(BODY, 'Reason: Between 2007 and 2013 the Irish economy fell '
                                        'into recession')), 4,
           'The reason, 4 marks. The scheme wants the bank bailout and the borrowing that paid '
           'for it, not a general statement that debt rose.')],
    'The question says "this increase", but the chart does not only increase: debt per person '
    'rises steeply to 2013 and then falls back. The scheme rewards saying so.',
    tariff_kind='fixed', section='A',
    figure_key='economics-2021-HL-paper-p10-art'))

# ── Worked calculations the scheme prints in full ──────────────────────────
# Excluded until now as "the response is the worked calculation". That is a
# description of the answer, not a blocker: the scheme sets out the formula, the
# substitution and the result, so every step a student is credited for is on the
# page and traces. Where the figures come off a chart the crop rides with the
# card, because the arithmetic is unanswerable without it.

P.cards.append(card(
    'econ-2021-hl-seca-q8-a', 2021, 'higher', 'economics-1-4',
    'price-from-the-equi-marginal-principle', '2021 HL Section A Q8(a)',
    'Calculate the price John would be willing to pay for one unit of good Z. Complete your '
    'calculations in the box below.',
    '7', 7,
    [point('r-1', as_option(block(BODY, '2500 \u00f7 200 = 12.5',
                                  '(b) Explain why John would pay this price')), 7,
           'Utility per euro is established from a good whose price is known, and that rate is '
           'then applied to good Z. The scheme prints two routes to the same 12.5.')],
    'The calculation runs in two stages, and the scheme accepts either of the two goods for the '
    'first \u2014 both give the same utility-per-euro.',
    tariff_kind='fixed', section='A'))

# ── Backfill: asks the scheme answers in full ──────────────────────────────
# Each was excluded under a label that described the ANSWER — a worked
# calculation, a chart lookup, a table — rather than any blocker. The scheme
# prints a tariff and a response for every one, and where the figures come off
# printed artwork the catalogued crop rides with the card.

P.cards.append(card(
    'econ-2021-hl-seca-q1-a', 2021, 'higher', 'economics-4-2',
    'calculating-the-balance-of-trade', '2021 HL Section A Q1(a)',
    'Calculate the balance of trade for the period 2015 \u2013 2019. Identify whether it is a '
    'surplus or a deficit.',
    '7', 7,
    [point('r-1', as_option(block(BODY, 'Total Exports: 112+119+123+141+152=647',
                                  '(b) Outline two reasons')), 7,
           'Both series are totalled across the whole period before subtracting, and the verdict '
           'is part of the answer: exports exceed imports, so it is a SURPLUS. A figure without '
           'the word is half of it.')],
    'The chart plots five years of each series and the question asks for the period, not a year, '
    'so ten figures are read off before any arithmetic happens.',
    tariff_kind='fixed', section='A',
    figure_key='economics-2021-HL-paper-p03-i0'))

P.cards.append(card(
    'econ-2021-hl-seca-q8-b', 2021, 'higher', 'economics-1-4',
    'why-the-equi-marginal-price-is-paid', '2021 HL Section A Q8(b)',
    'Explain why John would pay this price.',
    '2 @ 4', 8,
    [point('r-1', as_option(block(BODY, 'He would pay this price in order to maximise',
                                  '9. (a) What is the corresponding market structure')), 8,
           'Two things at 4 each: that he is maximising utility, and the rule that does it \u2014 '
           'the ratio of marginal utility to price equal across every good. Saying only that he '
           'wants the most utility misses the mechanism.')],
    'The equi-marginal principle is a RATIO condition. It is satisfied when the last euro spent '
    'on each good buys the same utility, not when the goods cost the same.',
    stem='Part (a) works out the price John would pay for one unit of good Z from the '
         'utility-per-euro he gets elsewhere.',
    tariff_kind='fixed', section='A'))

P.cards.append(card(
    'econ-2021-hl-seca-q9-a', 2021, 'higher', 'economics-2-0',
    'naming-the-market-structure', '2021 HL Section A Q9(a)',
    'Identify the corresponding market structure for each of these products/firms: A the Irish '
    'banking sector; B Irish Water (the company); C a takeaway food outlet.',
    '3 @ 3', 9,
    [point('r-1', as_option(block(BODY, 'A The Irish banking sector Oligopoly',
                                  '(b) Give one reason')), 9,
           'Three at 3 each. The sequence runs down the concentration scale \u2014 a few large '
           'banks (oligopoly), a single supplier (monopoly), many small outlets selling close '
           'but differentiated substitutes (monopolistic competition).')],
    'None of the three is perfect competition, which is the structure that almost never has a '
    'real-world example.',
    tariff_kind='fixed', section='A',
    figure_key='economics-2021-HL-paper-p13-i0'))

P.cards.append(card(
    'econ-2021-hl-seca-q9-b', 2021, 'higher', 'economics-2-0',
    'reasons-for-each-market-structure', '2021 HL Section A Q9(b)',
    'Give one reason for each of your chosen market structures above.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'The Irish banking sector is dominated by a few large firms',
                                  '10 | P a g e')), 6,
           'One reason per structure, and each names the FEATURE that defines it: a few large '
           'firms, a sole provider, many sellers of close substitutes with some price control.')],
    'The reason has to be the defining feature, not a fact about the industry. "Banks are big" '
    'is not why banking is an oligopoly; "a few firms hold the market" is.',
    stem='Part (a) names the structures: the Irish banking sector, Irish Water and a takeaway '
         'food outlet.',
    tariff_kind='fixed', section='A'))

P.cards.append(card(
    'econ-2021-hl-sa-q2', 2021, 'higher', 'economics-0-0',
    'sorting-positive-from-normative-statements', '2021 HL Section A Q2',
    'Select, using a tick (\u2714), whether each of the following statements are Normative '
    'statements or Positive statements.',
    'fixed', 15,
    [point('r-1', as_option(block(BODY, 'Statement Positive Normative Statement Statement',
                                  '3 | P a g e')), 15,
           'Four statements, priced 4, 4, 4 and 3. A POSITIVE statement is one that could be '
           'tested against the facts, whether or not it turns out true; a NORMATIVE one says what '
           'OUGHT to happen and no evidence can settle it.')],
    'The giveaway words are should and have to \u2014 both normative. A prediction about '
    'unemployment is positive even though nobody knows yet whether it will happen, because it is '
    'the KIND of claim evidence could settle. The scheme states its answer by which column the '
    'tick sits in, and that column does not survive extraction, so the completed table rides '
    'with the card as a picture.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-HL-scheme-p04-q2-ticks'))

P.cards.append(card(
    'econ-2021-hl-sa-q10-b', 2021, 'higher', 'economics-3-3',
    'what-you-would-advise-the-ecb-to-do-with-a-zero-rate', '2021 HL Section A Q10(b)',
    'Outline whether you would advise the European Central Bank to: increase, decrease, or '
    'maintain the current interest rate of 0%. Justify your choice.',
    '1 @ 7', 7,
    [anyN('r-1', 'A course of action for the ECB, with its justification \u2014 any one', 7, 1, 7,
          [o.strip(' \u2022') for o in
           as_option(block(BODY, 'During these economically volatile times',
                           '11 | P a g e')).split(' OR ') if o.strip(' \u2022')],
          'Seven marks for one recommendation properly justified. The scheme takes either '
          'answer \u2014 it is the reasoning that is marked, not the choice.')],
    'Both accepted answers rest on the same mechanism: a low or negative rate discourages saving '
    'and encourages borrowing and spending. What separates them is how far the ECB should push '
    'it, and the scheme calls a negative rate an extreme measure for weak growth and low '
    'inflation.',
    section='A', tariff_kind='fixed'))

P.emit()
