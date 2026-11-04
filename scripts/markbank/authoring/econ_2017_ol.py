#!/usr/bin/env python3
"""Economics 2017 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2017-ol-ev.json, made
from a visual sweep of all 12 paper pages and 36 scheme pages before any 2017
Ordinary card existed. Section B restarts at Question 1, so every citation names
its section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The Ordinary scheme reprints each question above its
answer, so a slice always starts after the reprinted wording. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.

The scheme prints the marks of its four calculations as small raised numerals
beside each figure of the working ("€53,245¹ m -¹ €50,548¹m = € 2,697m²"). The
text layer sets each numeral flat against its figure, so a row claims the
figure alone, sliced short of the numeral, and its note says which printed
marks it carries; the hidden solution figure shows the working as printed.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2017, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2017, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2017-OL-scheme-'
PAP = 'economics-2017-OL-paper-'
bl = H.bullets
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell


def side(label, options):
    """Options listed under one of the scheme's own headings ("Economic advantage"),
    each named by it: "<heading> — <response>". Both halves trace."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def by_heading(rid, label, options, per, note):
    """One printed head ("Retailers in the Republic of Ireland") and any one of its responses."""
    return heading(rid, H.traced(label) + ' — any one', options, per, note)


def unpriced(pairs):
    """questionTotal rows: the scheme prices them as one total and splits nothing."""
    return [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate(pairs, 1)]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ matching taxes
add('sa-q1', '3-1', 'matching-taxes-to-explanations', ref('A', 1),
    H.q(2, 'In relation to the following taxes, match the tax', ' Tax Explanation'), '4 x 4', 16,
    [point(f'r-{letter.lower()}', f'{letter} {H.traced(tax)} — {H.traced(expl)}', 4, f'{tax}, 4 marks: the scheme’s answer row puts {expl[0]} under {letter}.')
     for letter, tax, expl in (('A', 'VAT', '5 A tax on purchases and services.'), ('B', 'DIRT', '4 A tax on interest earned on deposits in financial institutions.'),
                               ('C', 'PAYE', '1 A tax on income.'), ('D', 'Customs duty', '2 A tax on goods imported into a country.'))],
    figure=PAP + 'p02-q1-table', **A)

# Q2 ─ fixed costs
q2 = H.q(2, 'You are given the following data for a firm.', ' Quantity')
q2_table = PAP + 'p02-q2-table'
add('sa-q2-i', '1-5', 'drawing-fixed-costs', ref('A', 2, '(i)'), H.q(2, 'Draw and label the fixed costs for this firm.', ' (ii)'),
    '3 + 3 + 4', 10,
    [point('r-q-axis', H.traced('Q axis + label'), 3, 'The quantity axis and its label, 3 marks. The completed graph is shown with the answer.'),
     point('r-costs-axis', H.traced('Costs axis + label'), 3, 'The costs axis and its label, 3 marks.'),
     point('r-fc', H.traced('FC labelled at €3,000'), 4, 'The fixed-cost line at €3,000, labelled, 4 marks.')],
    stem=q2, figure=SOL + 'p05-q2-graph', **A)
beside_ask(cards[-1], q2_table)
add('sa-q2-ii', '1-5', 'fixed-costs', ref('A', 2, '(ii)'), H.q(2, 'Explain the term fixed costs and state one example', ' Example:'),
    '6', 6,
    unpriced([(H.traced('FC: costs which do not change as the level of output changes.'),
               'The scheme prices the explanation and the example 6 together and does not say which earns which.'),
              (H.traced('Example: Rent of a fixed asset'), 'Claim the complete answer: 6 marks in all.')]),
    kind='questionTotal', **A)

# Q3 ─ cross-border shopping
add('sa-q3', '4-2', 'shopping-in-northern-ireland', ref('A', 3),
    H.q(3, 'Outline one possible economic effect which an increase in the number of people', ' (16 marks)'), '2 x 8', 16,
    [by_heading('r-retailers', 'Retailers in the Republic of Ireland',
                H.split('Reduced sales and profits for these businesses.', 'Irish Government’s finances:',
                        ['Reduced sales and profits', 'Closure of some businesses', 'More competitive pricing']), 8,
                'One effect on retailers, 8 marks.'),
     by_heading('r-finances', 'Irish Government’s finances',
                H.split('Taxation revenue: reduced VAT receipts', '2 x 8 marks each',
                        ['Taxation revenue', 'Reduction in excise duties', 'Taxation policy', 'If unemployment were to increase']), 8,
                'One effect on the government’s finances, 8 marks.')],
    kind='fixed', **A)

# Q4 ─ visible and invisible trade
add('sa-q4', '4-2', 'visible-and-invisible-trade', ref('A', 4),
    # The four statements follow the ask, from the paper's own table rows, so the
    # phone reader is not left to the table's small print alone.
    f"{H.q(3, 'Indicate by means of a tick', ' Visible Invisible')} {H.q(3, 'Expenditure of Irish soccer supporters', ' (16 marks)')}",
    '4 x 4', 16,
    [point(f'r-{k}', f'{H.traced(stmt)} — {H.traced(cat)}', 4, f'{cat}, 4 marks.')
     for k, stmt, cat in (('soccer', 'Expenditure of Irish soccer supporters having travelled to Austria.', 'Invisible imports'),
                          ('cheese', 'Irish firms selling cheese in Germany.', 'Visible exports'),
                          ('tourists', 'Foreign tourists using Ryanair to travel to Ireland.', 'Invisible exports'),
                          ('cars', 'Irish consumers buying cars in the UK and bringing them back to Ireland.', 'Visible imports'))],
    figure=PAP + 'p03-q4-table', **A)

# Q5 ─ IMF, ECB, WTO
add('sa-q5', '4-1', 'imf-ecb-and-wto', ref('A', 5), H.q(3, 'What do the following letters stand for?', ' (16 marks)'),
    '5 + 6 + 5', 16,
    [point(f'r-{k.lower()}', f'{k} — {H.traced(full)}', m, f'{k}, {m} marks.')
     for k, full, m in (('IMF', 'International Monetary Fund', 5), ('ECB', 'European Central Bank', 6), ('WTO', 'World Trade Organisation', 5))],
    **A)

# Q6 ─ the opportunity cost of third-level education
add('sa-q6', '0-1', 'investing-in-third-level-education', ref('A', 6),
    H.q(3, 'The Irish government invests significant amounts of taxpayers’ money', ' Explanation:'), '7 + 2 x 5', 17,
    [point('r-term', 'Opportunity cost — ' + H.traced('The cost of foregone alternatives.'), 7,
           'Opportunity cost, 7 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('The cost of passing up the next best choice when making a decision.')]),
     anyN('r-advantages', 'An advantage — any two', 10, 2, 5,
          bl('• A better educated workforce may result', '2 x 5 marks each'), 'Two advantages, 5 marks each.')],
    kind='fixed', **A)

# Q7 ─ the demand for new cars
q7 = H.q(4, 'This diagram represents the demand for new cars in Ireland in 2015.', ' (i)')
q7_fig = PAP + 'p04-q7-diagram'
add('sa-q7-i', '1-1', 'drawing-an-increase-in-demand', ref('A', 7, '(i)'),
    H.q(4, 'The demand for new cars increased in 2016.', ' D (ii)'), '7', 7,
    [point('r-1', H.traced('New D/Curve correctly labelled'), 7, 'The new curve D1, to the right of D and labelled, 7 marks. '
           'The completed diagram is shown with the answer.')],
    stem=q7, figure=SOL + 'p07-q7-diagram', **A)
beside_ask(cards[-1], q7_fig)
# The text layer sets the diagram's Q axis label inside the ask's line ("in Q Ireland").
q7ii = H.q(4, 'Suggest two reasons for the increase in the demand for new cars', ' Reason 1:').replace(' in Q Ireland', ' in Ireland')
pick('sa-q7-ii', '1-1', 'why-demand-for-new-cars-rose', ref('A', 7, '(ii)'), q7ii, 'A reason — any two',
     H.split('Some companies are offering loans at low or zero interest rates', '2 x 5 marks each',
             ['Some companies are offering loans', 'People who can afford to do so', 'People are changing cars so as',
              'Some credit unions / banks', 'Increased employment;']),
     2, 5, 'Two reasons, 5 marks each.', stem=q7, figure=q7_fig, **A)

# Q8 ─ taxes on disposable packaging
adv = H.split('Revenue for the government increases', 'Economic disadvantage',
              ['Revenue for the government', 'Fund initiatives', 'Encourage suppliers to consider', 'If income from the tax is ring',
               'Polluter pays principle', 'Consumption of fast food may be discouraged'])
dis = H.split('Increased prices for consumers of these goods', '1st correct response',
              ['Increased prices for consumers', 'Increased administration costs', 'Citizens may be become more disgruntled',
               'A regressive tax'])
add('sa-q8', '1-3', 'taxing-disposable-packaging', ref('A', 8),
    H.q(4, 'Outline one possible economic advantage and one possible economic disadvantage', ' Economic advantage:'), '10 + 7', 17,
    [anyN('r-1', 'One advantage and one disadvantage', 17, 2, 10,
          side('Economic advantage', adv) + side('Economic disadvantage', dis),
          'One advantage and one disadvantage. The scheme prices the two by order, not by side: the first correct '
          'response 10 marks, the second 7.', steps=[10, 7])],
    kind='fixed', stem=H.q(4, '‘The government was advised to consider introducing new taxes', ' Outline'), **A)

# Q9 ─ long-run equilibrium in perfect competition
q9 = H.q(4, 'The diagram below represents the long run equilibrium of a firm in Perfect Competition.', ' (i)')
q9_fig = PAP + 'p04-q9-diagram'
add('sa-q9-i', '2-0', 'labels-of-perfect-competition', ref('A', 9, '(i)'),
    H.q(4, 'Write in words the full label (not abbreviations)', ' 1 P 2'), '3 x 4', 12,
    [point(f'r-{n}', f'{n} — {H.traced(label)}', 4, f'Line {n}, 4 marks.')
     for n, label in ((1, 'Marginal Cost'), (2, 'Average Cost'), (3, 'Average revenue / marginal revenue / demand'))],
    stem=q9, figure=q9_fig, **A)
add('sa-q9-ii', '2-0', 'normal-profit-in-perfect-competition', ref('A', 9, '(ii)'),
    H.q(4, 'Is the firm earning supernormal profit?', ' (17 marks)'), '5', 5,
    [point('r-1', 'No — ' + H.traced('It is not earning SNP because AR = AC.'), 5,
           'No, with its reason, 5 marks: the scheme sets No in bold.')],
    stem=q9, figure=q9_fig, **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ monopoly; barriers to entry; state companies
q1 = ' '.join([H.q(5, 'The diagram below represents a Monopoly firm in equilibrium.', ' P MC'),
               H.q(5, 'Copy the diagram into your answer book.', ' (i)')])
q1_fig = PAP + 'p05-q1-diagram'
add('sb-q1-a-i', '2-0', 'labels-of-a-monopoly-diagram', ref('B', 1, '(a)(i)'),
    H.q(5, 'Write out what each of the six underlined labels represents.', ' (ii)'), '6 @ 4', 24,
    [point(f'r-{k}', f'{lab} — {H.traced(full)}', 4, f'{lab}, 4 marks.')
     for k, lab, full in (('pc', 'P / C', 'Price / Cost'), ('q', 'Q', 'Quantity'), ('ac', 'AC', 'Average Cost'),
                          ('ar', 'AR', 'Average Revenue'), ('mc', 'MC', 'Marginal Cost'), ('mr', 'MR', 'Marginal Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'price-and-average-cost-in-monopoly', ref('B', 1, '(a)(ii)'),
    H.q(5, 'The firm is in equilibrium at point G and produces output Q1.', ' (30 marks)'), '6', 6,
    unpriced([(H.cell('The price the firm will charge for Q1. P1'),
               'The scheme prices P1 and C1 6 together and does not say which earns which. The completed diagram is shown with the answer.'),
              (H.cell('The average cost of producing this output. C1'), 'Claim the complete answer: 6 marks in all.')]),
    kind='questionTotal', stem=q1, figure=SOL + 'p09-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
pick('sb-q1-b', '2-0', 'barriers-to-entry', ref('B', 1, '(b)(i)–(ii)'),
     H.q(5, 'New firms may wish to enter a monopoly market', ' (21 marks)'), 'A barrier to entry, with its note — any three',
     H.split('Legal /state restrictions', '3 x 7 marks each',
             ['Legal /state restrictions', 'Ownership of a Patent', 'Trade Agreements & Collusion', 'Ownership of raw materials',
              'Industry requires a large investment', 'Mergers / Takeovers']),
     3, 7, 'Three barriers, each with its brief note, 7 marks each: the scheme prices (i) and (ii) together.', **B)
q1c = H.q(5, 'The state‐owned companies Bus Éireann', ' (i)')
pick('sb-q1-c-i', '1-3', 'why-the-state-provides-services', ref('B', 1, '(c)(i)'),
     H.q(5, 'State and explain one reason why some services provided by the above companies', ' (ii)'), 'A reason — any one',
     H.split('Loss making services / demand is low', '1 x 8 marks',
             ['Loss making services', 'Government deems services socially', 'Lack of capital by private', 'Economies of scale']),
     1, 8, 'One reason, 8 marks.', stem=q1c, **B)
pick('sb-q1-c-ii', '1-3', 'reducing-state-company-losses', ref('B', 1, '(c)(ii)'),
     H.q(5, 'State and explain two measures these state‐owned companies', ' (24 marks)'), 'A measure — any two',
     H.split('Decrease wage costs / pensions', '2 x 8 marks each',
             ['Decrease wage costs', 'Decrease numbers employed', 'Cut / reduce the provision', 'Increase revenue / efficiency']),
     2, 8, 'Two measures, 8 marks each.', stem=q1c, **B)

# Q2 ─ economic goods; demand and supply; income elasticity
q2a = H.q(6, 'The Apple iPhone 7 is an economic good.', ' (i)')
pick('sb-q2-a-i', '0-1', 'characteristics-of-economic-goods', ref('B', 2, '(a)(i)'),
     H.q(6, 'Explain any two of the underlined terms, with reference to the Apple iPhone 7.', ' (ii)'), 'A characteristic — any two',
     H.split('Scarce\nThere must be less', '2 x 5 marks', ['Scarce', 'Transferable', 'Utility']),
     2, 5, 'Two characteristics, 5 marks each.', stem=q2a, **B)


def term(name, first):
    """One column of the three-term table: the term, and its column's statements."""
    line = H.cell(f'{name} {first}')
    return f'{H.traced(name)} — {H.traced(line[len(name):].strip())}'


pick('sb-q2-a-ii', '1-1', 'normal-substitute-and-complementary-goods', ref('B', 2, '(a)(ii)'),
     H.q(6, 'Explain any two of the following economic terms:', ' (20 marks)'), 'A term — any two',
     [term(n, f) for n, f in (('Normal good', 'One which'), ('Substitute good', 'Goods that satisfy'), ('Complementary good', 'Goods that are used'))],
     2, 5, 'Two terms, 5 marks each.', stem=q2a, **B)
q2b = H.q(6, 'The information below represents the market demand and supply schedule', ' Price Quantity')
add('sb-q2-b', '1-0', 'drawing-demand-and-supply', ref('B', 2, '(b)(i)–(iii)'),
    H.q(6, 'Using the above information and one diagram', ' (30 marks)'), '10 + 10 + 4 + 3 + 3', 30,
    [point('r-demand', H.opt('D: 5 points at 2 marks each', 'S: 5 points'), 10, 'The demand curve, 10 marks: its five points at 2 each.'),
     point('r-supply', H.opt('S: 5 points at 2 marks each', 'Labels: P'), 10, 'The supply curve, 10 marks: its five points at 2 each.'),
     point('r-labels', H.opt('Labels: P, Q, D/C and S/C', 'P1 and Q1'), 4,
           'The four labels, 4 marks: the scheme prices them on one line, which spans (i) and (ii).'),
     point('r-p1', 'P1 — ' + H.traced('600'), 3, 'The equilibrium price P1, 3 marks (the scheme’s P1 and Q1: 2 x 3 marks each).'),
     point('r-q1', 'Q1 — ' + H.traced('800'), 3, 'The equilibrium quantity Q1, 3 marks. The completed graph is shown with the answer.')],
    stem=q2b, figure=SOL + 'p13-q2b-graph', **B)
beside_ask(cards[-1], PAP + 'p06-q2b-table')
q2c = H.q(6, 'The formula for measuring Income Elasticity of Demand (YED) is:', ' ∆Q')
q2c_fig = PAP + 'p06-q2c-formula'
add('sb-q2-c-i', '1-4', 'symbols-of-income-elasticity', ref('B', 2, '(c)(i)'),
    H.q(6, 'Explain what each of the above symbols represent.', ' (ii)'), '6 x 2', 12,
    [point(f'r-{k}', f'{sym} — {H.traced(meaning)}', 2, f'{sym}, 2 marks.')
     for k, sym, meaning in (('dq', '∆Q', 'Change in the quantity demanded of the good'), ('dy', '∆Y', 'Change in the income of the consumer.'),
                             ('y1', 'Y1', 'Original income of the consumer.'), ('y2', 'Y2', 'New / current income of the consumer.'),
                             ('q1', 'Q1', 'Original quantity of the good demanded.'), ('q2', 'Q2', 'New / current quantity demanded of the good'))],
    stem=q2c, figure=q2c_fig, **B)
add('sb-q2-c-ii', '1-4', 'is-the-iphone-a-luxury-good', ref('B', 2, '(c)(ii)'),
    H.q(6, 'The Income Elasticity of Demand (YED) for the Apple iPhone 7 is +2.8.', ' (25 marks)'), '5 + 8', 13,
    [point('r-answer', H.traced('This good is a luxury good.'), 5, 'The answer, 5 marks.'),
     point('r-reason', H.opt('Luxury goods tend to be income elastic.', 'Answer: 5 marks.'), 8, 'The reason, 8 marks.')],
    stem=q2c, **B)

# Q3 ─ factors of production; public and private sector pay; wages and emigration
add('sb-q3-a', '0-1', 'factors-of-production-for-housing', ref('B', 3, '(a)'),
    H.q(7, 'State and explain the four factors of production that might be used', ' (20 marks)'), '4 x 5', 20,
    [point(f'r-{f.lower()}', f'{H.traced(f)} — {H.traced(cc(first).lstrip("• ").strip())}', 5, f'{f}, 5 marks.')
     for f, first in (('Land', '• anything supplied by nature'), ('Labour', '• the human effort involved'),
                      ('Capital', '• man‐made wealth'), ('Enterprise', '• the person who takes the risk'))],
    stem=H.q(7, 'A construction firm converts inputs', ' State'), **B)
q3b = H.q(7, 'The Irish Government is facing demands for wage increases', ' (i)')
add('sb-q3-b-i', '2-1', 'public-and-private-sectors', ref('B', 3, '(b)(i)'),
    H.q(7, 'Explain each of the underlined terms and state one example of an occupation', ' (ii)'), '2 x 7 (4 + 3)', 14,
    [point('r-public', 'Public sector — ' + H.opt('That part of the economy which is run by state bodies', 'Private sector'), 7,
           'The public sector with an example, 7 marks (4 + 3).'),
     point('r-private', 'Private sector — ' + H.opt('That part of the economy which is run by private individuals', 'Explanations: 2 x 7'), 7,
           'The private sector with an example, 7 marks (4 + 3).')],
    stem=q3b, **B)
pick('sb-q3-b-ii', '2-1', 'why-employees-seek-pay-rises', ref('B', 3, '(b)(ii)'),
     H.q(7, 'State and explain one economic reason why employees are currently seeking', ' (iii)'), 'A reason — any one',
     H.split('Economic growth\nThe government states', '1 x 8 marks (4+4)',
             ['Economic growth', 'Return for accepting austerity', 'Increased cost of living', 'Pay equality', 'Increase in minimum wage']),
     1, 8, 'One reason, 8 marks (4 + 4).', stem=q3b, **B)
pick('sb-q3-b-iii', '2-1', 'the-cost-of-pay-rises', ref('B', 3, '(b)(iii)'),
     H.q(7, 'Discuss one possible economic disadvantage for the Irish economy', ' (30 marks)'), 'A disadvantage — any one',
     H.split('Inflation\nIf wages increase', '1 x 8 marks (4+4)',
             ['Inflation', 'Rising costs for business', 'Loss of jobs', 'Less attractive for MNCs', 'Increased taxation', 'Reduced state services']),
     1, 8, 'One disadvantage, 8 marks (4 + 4).', stem=q3b, **B)
pick('sb-q3-c-i', '2-1', 'why-wages-differ', ref('B', 3, '(c)(i)'),
     H.q(7, 'State and explain two economic reasons why different wages are paid', ' (ii)'), 'A reason — any two',
     H.split('Different skills', '2 x 6 marks (3+3)',
             ['Different skills', 'Training/experience', 'Educational qualifications', 'Nature & Conditions of the job',
              'Negotiating strength', 'Traditions attaching to certain jobs', 'Possession of innate talents']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', **B)
add('sb-q3-c-ii', '3-2', 'encouraging-emigrants-home', ref('B', 3, '(c)(ii)'),
    H.q(7, 'The Irish Government is trying to encourage Irish emigrants', ' (25 marks)'), '7 + 6', 13,
    [anyN('r-1', 'A measure — any two', 13, 2, 7,
          H.split('Improve government services/develop infrastructure', '1st correct response',
                  ['Improve government services', 'Lower taxation', 'Provide grants/subsidies', 'Training and education',
                   'Devote more resources to capital']),
          'Two measures: the first correct 7 marks (4 + 3), the second 6 (3 + 3).', steps=[7, 6])],
    kind='fixed', **B)

# Q4 ─ money and barter; savings; price inflation
q4a = H.q(7, 'In modern economies money has replaced barter.', ' (i)')
add('sb-q4-a-i', '3-4', 'money-and-barter', ref('B', 4, '(a)(i)'), H.q(7, 'Explain the terms money and barter.', ' (ii)'), '2 x 5', 10,
    [point('r-money', 'Money — ' + H.traced('Anything which is acceptable in payment for a debt / buying a good.'), 5, 'Money, 5 marks.'),
     point('r-barter', 'Barter — ' + H.traced('Swapping one item for another.'), 5, 'Barter, 5 marks.')],
    stem=q4a, **B)
pick('sb-q4-a-ii', '3-4', 'a-difficulty-with-barter', ref('B', 4, '(a)(ii)'),
     H.q(7, 'Explain one difficulty associated with the use of barter.', ' (iii)'), 'A difficulty — any one',
     H.split('Time consuming\nIt may take', '1 explanation x 5 marks',
             ['Time consuming', 'Difficult to establish value', 'Specialisation of labour']),
     1, 5, 'One difficulty, 5 marks.', stem=q4a, **B)
pick('sb-q4-a-iii', '3-4', 'other-forms-of-money', ref('B', 4, '(a)(iii)'),
     H.q(7, 'State two other items which are currently used as money', ' (25 marks)'), 'An item — any two',
     [H.traced(x) for x in ('Cheques', 'Credit Cards', 'Debit Cards', 'Electronic bank transfers')],
     2, 5, 'Two items, 5 marks each.', stem=q4a, **B)
q4b = H.q(7, 'Some banks are offering customers a low interest rate', ' (i)')
# The stem is folded into the ask: Q3(b)(i) opens with the same six words.
add('sb-q4-b-i', '3-4', 'interest-rates-and-savings', ref('B', 4, '(b)(i)'),
    f"{q4b} {H.q(7, 'Explain each of the underlined terms.', ' (ii) State and explain two factors')}", '2 x 6', 12,
    [point('r-interest', H.opt('Interest rate: the price of money', 'Savings: that part'), 6, 'The interest rate, 6 marks.'),
     point('r-savings', H.traced('Savings: that part of a person’s income which is not spent.'), 6, 'Savings, 6 marks.')],
    **B)
# The scheme breaks one word across a line end ("peo‐ ple"); the page prints it whole.
dehyphen = lambda t: re.sub(r'(\w)[-‐] (\w)', r'\1\2', t)
pick('sb-q4-b-ii', '3-4', 'why-households-save', ref('B', 4, '(b)(ii)'),
     H.q(7, 'State and explain two factors, other than interest rate', ' (26 marks)'), 'A factor — any two',
     [dehyphen(x) for x in H.split('Income levels\n•', '2 x 7 marks (4+3)',
                                   ['Income levels', 'Rate of DIRT', 'Level of Inflation', 'Levels of Social Welfare Benefits',
                                    'Tax Rates', 'Future Expectations', 'Demands on disposable income'])],
     2, 7, 'Two factors, 7 marks each (4 + 3).', stem=q4b, **B)
add('sb-q4-c-i', '3-3', 'price-inflation', ref('B', 4, '(c)(i)'), H.q(7, 'Explain the term price inflation.', ' (ii)'), '8', 8,
    [point('r-1', H.traced('An increase in prices of goods / services (over a period of time) in the economy.'), 8,
           'The explanation, 8 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('A decrease in the value of money / people buy less for their money.')])], **B)


def effect(category, statement, explanation):
    """One row of a Category / Statement / Explanation table: "<category> — <statement> <explanation>".
    The statement and its explanation are adjacent cells, read in the order printed."""
    return f'{H.traced(category)} — {H.traced(statement + " " + explanation)}'


pick('sb-q4-c-ii', '3-3', 'what-moves-the-inflation-rate', ref('B', 4, '(c)(ii)'),
     H.q(7, 'State one economic effect which any two of the following developments', ' (24 marks)'),
     'A development, its effect and explanation — any two',
     [effect('Increase in world oil prices.', 'Inflation rate will rise.', cc('The cost of production / transportation')),
      effect('Decrease in the rates of Irish indirect taxes.', 'Inflation rate will fall.', cc('As indirect taxes fall the prices')),
      effect('Decrease in the Irish level of savings.', 'Inflation rate will rise.', cc('If level of savings fall it may'))],
     2, 8, 'Two developments, 8 marks each (4 + 4).', **B)

# Q5 ─ the multiplier; the circular flow; economic growth
q5a = H.q(8, 'The multiplier formula for an open economy is', ' 1 MPS')
q5a_fig = PAP + 'p08-q5a-formula'
q5a_data = H.q(8, 'Assume the MPM is 0.25 and MPS is 0.15', ' (i)')
add('sb-q5-a-i', '3-0', 'the-multiplier', ref('B', 5, '(a)(i)'), H.q(8, 'Explain the term multiplier.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('The multiplier tells us by how much national income increases for any given injection into the economy.'), 5,
           'The explanation, 5 marks.')], stem=q5a, figure=q5a_fig, **B)
add('sb-q5-a-ii', '3-0', 'calculating-the-multiplier', ref('B', 5, '(a)(ii)'),
    f"{q5a_data} {H.q(8, 'Using the formula above calculate the size of the multiplier.', ' (iii)')}", '2 + 3 + 3 + 2', 10,
    [point('r-one', 'The numerator — ' + H.traced('1'), 2, '2 marks, printed beside the 1 over the line.'),
     point('r-mps', 'MPS — ' + H.traced('0.15'), 3, '3 marks, printed beside the 0.15.'),
     point('r-mpm', 'MPM — ' + H.traced('0.25'), 3, '3 marks, printed beside the 0.25.'),
     point('r-answer', 'The multiplier — ' + H.traced('2.5'), 2, '2 marks, printed beside the answer. The figure shows the working as printed.')],
    stem=q5a, figure=SOL + 'p21-q5aii-working', **B)
beside_ask(cards[-1], q5a_fig)
add('sb-q5-a-iii', '3-0', 'the-multiplier-and-national-income', ref('B', 5, '(a)(iii)'),
    f"{q5a_data} {H.q(8, 'If investment in the economy increases by €10 million', ' (21 marks)')}", '2 + 2 + 2', 6,
    [point('r-investment', 'The increase in investment — ' + H.traced('€10 million'), 2, '2 marks, printed beside the €10 million.'),
     point('r-multiplier', 'Times the multiplier — ' + H.traced('2.5'), 2, '2 marks, printed beside the 2.5.'),
     point('r-answer', 'The increase in national income — ' + H.traced('€25 million'), 2,
           '2 marks, printed beside the answer. The figure shows the working as printed.')],
    stem=q5a, figure=SOL + 'p21-q5aiii-working', **B)
beside_ask(cards[-1], q5a_fig)
q5b = H.q(8, 'The diagram below represents the Circular Flow of Income in an open economy', ' 1 Households')
q5b_fig = PAP + 'p08-q5b-diagram'
add('sb-q5-b-i', '4-2', 'an-open-economy', ref('B', 5, '(b)(i)'), H.q(8, 'Ireland is an open economy. Explain this statement.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('Explanation: it engages in trade i.e. it imports and exports goods and services.'), 5, 'The explanation, 5 marks.')],
    **B)
add('sb-q5-b-ii', '3-0', 'lines-of-the-circular-flow', ref('B', 5, '(b)(ii)'),
    H.q(8, 'State what each of the lines numbered 1 to 3 represents.', ' (iii)'), '3 x 5', 15,
    [point(f'r-{n}', f'{n} — {H.traced(rep)}', 5, f'Line {n}, 5 marks.')
     for n, rep in ((1, 'Payment / for factors of production'), (2, 'Savings'), (3, 'Exports'))],
    stem=q5b, figure=q5b_fig, **B)
pick('sb-q5-b-iii', '3-0', 'flows-between-sectors', ref('B', 5, '(b)(iii)'),
     H.q(8, 'Referring to the diagram above, explain the type of activities', ' (30 marks)'), 'A pair and its activity — any two',
     [f'{H.traced(pair)} — {H.traced(act)}' for pair, act in (
         ('Foreign markets and firms', 'Firms export some of their goods (to foreign markets) and receive income for these.'),
         ('Households and foreign markets', 'Households: spend part of their income buying imports.'),
         ('Households and financial institutions', 'Households: save part of their income in financial institutions.'))],
     2, 5, 'Two pairs, 5 marks each.', stem=q5b, figure=q5b_fig, **B)
q5c = H.q(8, 'One of the aims of government is to achieve economic growth.', ' (i)')
add('sb-q5-c-i', '3-5', 'economic-growth', ref('B', 5, '(c)(i)'), H.q(8, 'Explain the term economic growth.', ' (ii)'), '8', 8,
    [point('r-1', H.traced('Explanation: it is the rise in GNP / output / national income per head within a country.'), 8,
           'The explanation, 8 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('The increase in the amount of goods and services in an economy over a period of time.')])],
    stem=q5c, **B)
pick('sb-q5-c-ii', '3-5', 'why-economic-growth-matters', ref('B', 5, '(c)(ii)'),
     H.q(8, 'Outline two reasons why it is important for an economy to achieve economic growth.', ' (24 marks)'), 'A reason — any two',
     H.split('Increased employment\nEconomic growth will lead', '2 x 8 marks each (4 + 4)',
             ['Increased employment', 'Reduced Emigration', 'Improved government finances', 'Improved standard of living',
              'Investment opportunities', 'Positive effects on Businesses']),
     2, 8, 'Two reasons, 8 marks each (4 + 4).', stem=q5c, **B)

# Q6 ─ the current budget; Budget 2017; state services or tax cuts
q6a = H.q(9, 'The estimated Government current budget for 2017 is as follows:', ' (i)')
add('sb-q6-a-i', '3-1', 'the-current-budget-surplus', ref('B', 6, '(a)(i)'),
    H.q(9, 'Calculate the current budget surplus. Show your workings.', ' (ii)'), '1 + 2 + 2', 5,
    [point('r-income', 'Government current income — ' + H.traced('€53,245'), 1, '1 mark, printed beside the income figure.'),
     point('r-expenditure', 'Less government current expenditure — ' + H.traced('€50,548'), 2,
           '2 marks, the scheme’s 1 beside the minus sign and 1 beside the expenditure figure.'),
     point('r-surplus', 'Current budget surplus — ' + H.traced('€ 2,697m'), 2,
           '2 marks, printed beside the answer. The figure shows the working as printed.')],
    stem=q6a, figure=SOL + 'p24-q6ai-working', **B)
add('sb-q6-a-ii', '3-1', 'current-income-and-expenditure', ref('B', 6, '(a)(ii)'),
    H.q(9, 'State one example of government current income and one example', ' (iii)'), '2 x 5', 10,
    [by_heading('r-income', 'Government current income',
                H.cut_cell('1. Direct tax revenue (or example).', ['Direct tax revenue', 'Indirect tax revenue', 'Interest on loans given',
                                                                  'Surpluses of semi', 'Departmental balances', 'Prize Bond scheme',
                                                                  'Fees charged for state services']), 5,
                'One example of current income, 5 marks.'),
     by_heading('r-expenditure', 'Government current expenditure',
                H.cut_cell('1. Salaries of all state employees.', ['Salaries of all state employees', 'Cost of running government',
                                                                   'Costs of running state institutions', 'Social welfare payments',
                                                                   'National debt service', 'Grants to local authorities',
                                                                   'Ireland’s contribution to the EU']), 5,
                'One example of current expenditure, 5 marks.')],
    kind='fixed', stem=q6a, **B)
add('sb-q6-a-iii', '3-1', 'falling-unemployment-and-the-budget', ref('B', 6, '(a)(iii)'),
    H.q(9, 'Explain two economic effects of the falling unemployment rate', ' (25 marks)'), '2 x 5 (3 + 2)', 10,
    [point(f'r-{k}', t, 5, n) for k, t, n in zip(
        ('revenue', 'expenditure'),
        H.split('Current revenue increases', '2 x 5 marks each (3+2)', ['Current revenue increases', 'Current expenditure decreases']),
        ('Current revenue rising, 5 marks (3 + 2).', 'Current expenditure falling, 5 marks (3 + 2).'))],
    **B)
measures = (H.traced('An increase in social welfare payment of €5 per week'),
            H.traced('Decrease in rate of Deposit Interest Retention Tax (DIRT) from 45% to 39%.'),
            H.traced('Increase in excise duty on tobacco (e.g. 50c increase on a packet of 20 cigarettes)'))
favour = ((['Increased standard of living For those', 'Fairer distribution of income Citizens', 'Reduction in demand for state funding',
            'Increased spending in the economy']),
          (['Encourage savings The reduced', 'Increased availability of loans Financial', 'Reduce inflation If people',
            'Encourage future planning People']),
          (['Increase Government revenue This increase will help', 'Reduce consumption / better personal health',
            'Social benefit of healthier population', 'Reduced healthcare costs in society', 'Opportunity cost The money saved']))
against = ((['Increased government expenditure / borrowing', 'Opportunity cost The money could', 'Possibility of increased taxation',
             'Possible effect on workers/may discourage work']),
           (['Reduce Government revenue', 'Need for the government to raise other taxes', 'May discourage spending If',
             'Could be considered inequitable']),
           (['Decrease in standard of living Disposable', 'Inflation Prices of tobacco', 'Inequitable Only applies',
             'Smuggling/black economy may increase', 'Tax revenue may fall If']))
arg = lambda starts: [cc(s, whole=s == 'Increased spending in the economy') for s in starts]
add('sb-q6-b', '3-1', 'budget-2017-measures', ref('B', 6, '(b)'),
    H.q(9, 'Outline one economic argument in favour of and one economic argument against any two', ' (24 marks)'), '4 x 6', 24,
    [anyN('r-for', 'An argument in favour — any two', 12, 2, 6,
          [o for m, starts in zip(measures, favour) for o in side(m, arg(starts))],
          'One argument in favour for each of the two measures you chose, 6 marks each.'),
     anyN('r-against', 'An argument against — any two', 12, 2, 6,
          [o for m, starts in zip(measures, against) for o in side(m, arg(starts))],
          'One argument against for each of the same two measures, 6 marks each.')],
    kind='fixed', **B)
q6c = H.q(9, 'Various opinion polls have indicated that people in Ireland favour', ' (i)')
pick('sb-q6-c-i', '3-1', 'improving-state-services', ref('B', 6, '(c)(i)'),
     H.q(9, 'Identify two state services which could be improved', ' (ii)'), 'A state service — any two',
     H.split('Health services\nEmploy more', '2 x 8 marks (4 + 4)', ['Health services', 'Education', 'Disability services', 'Social housing']),
     2, 8, 'Two services, 8 marks each (4 + 4).', stem=q6c, **B)
q6cii = H.q(9, 'Would you favour a reduction in taxation rates', ' (26 marks)')
for word, starts in (('yes', ['Increased disposable income / savings Lower', 'Increased reward for effort', 'Cheaper prices If indirect',
                              'Attract emigrants back to Ireland If', 'Revenue for the government Higher',
                              'Reduced activity in the Black economy Lower']),
                     ('no', ['Loss of state services / charges', 'Deterioration in state services', 'Greater inequality Reduced',
                             'New Sources of revenue would be required', 'Less government funding available for state initiatives There'])):
    pick(f'sb-q6-c-ii-{word}', '3-1', 'would-you-cut-tax-rates', ref('B', 6, '(c)(ii)', word),
         f'{q6cii} Justify the choice: {word.upper()}.', f'A reason for answering {word.upper()} — any two',
         [cc(s) for s in starts], 2, 5, 'Two reasons, 5 marks each (3 + 2). The scheme credits YES and NO, each with its own list.',
         stem=q6c, **B)

# Q7 ─ the balance of trade; corporation tax and location; Brexit
q7a = H.q(9, 'You are given the following information about a country’s trade in a year.', ' Visible Exports')
q7a_table = PAP + 'p09-q7a-table'
add('sb-q7-a-i', '4-2', 'the-balance-of-trade', ref('B', 7, '(a)(i)'), H.q(9, 'Explain the term Balance of Trade.', ' (ii)'), '9', 9,
    [point('r-1', H.traced('This is the difference between visible exports and visible imports.'), 9, 'The explanation, 9 marks.')], **B)
add('sb-q7-a-ii', '4-2', 'calculating-the-balance-of-trade', ref('B', 7, '(a)(ii)'),
    H.q(9, 'Using the above data, calculate the Balance of Trade', ' (iii)'), '8', 8,
    unpriced([(H.traced('€22,000 m ‐ €23,500 m = (1,500m)'),
               'The scheme prices the working and the answer 8 together and does not say which earns which.'),
              (H.traced('The balance of trade is a deficit.'), 'Claim the complete answer: 8 marks in all.')]),
    kind='questionTotal', stem=q7a, figure=q7a_table, **B)
add('sb-q7-a-iii', '4-2', 'a-new-balance-of-trade', ref('B', 7, '(a)(iii)'),
    H.q(9, 'If the level of visible exports above increased by €2,000m', ' (25 marks)'), '3 + 3 + 2', 8,
    [point('r-exports', 'New visible exports — ' + H.traced('€24,000'), 3,
           '3 marks, printed 1 beside each of the €22,000m, the €2,000m and the €24,000m they add to.'),
     point('r-balance', 'New Balance of Trade — ' + H.traced('€500'), 3,
           '3 marks, printed 1 beside each of the €24,000m, the €23,500m and the €500m.'),
     point('r-surplus', H.traced('It is a surplus'), 2, '2 marks. The figure shows the working as printed.')],
    stem=q7a, figure=SOL + 'p28-q7aiii-working', **B)
beside_ask(cards[-1], q7a_table)
q7b = H.q(9, 'The Irish government retained the rate of Corporation Tax at 12.5% in Budget 2017.', ' (i)')
add('sb-q7-b-i', '3-1', 'corporation-tax', ref('B', 7, '(b)(i)'), H.q(9, 'Explain the underlined term.', ' (ii) State and explain two economic factors'),
    '8', 8, [point('r-1', H.traced('This is a tax on the profits made by a company.'), 8, 'The explanation, 8 marks.')], stem=q7b, **B)
pick('sb-q7-b-ii', '4-1', 'where-multinationals-locate', ref('B', 7, '(b)(ii)'),
     H.q(9, 'State and explain two economic factors, other than the rate of corporation tax', ' (24 marks)'), 'A factor — any two',
     H.split('Availability of skilled workforce', '2 x 8 marks each (4 + 4)',
             ['Availability of skilled workforce', 'Government incentives', 'Efficient Transport network', 'Availability of essential services',
              'Land for expansion', 'Regulations: environmental', 'Proximity to the market', 'Social infrastructure', 'Membership of EU']),
     2, 8, 'Two factors, 8 marks each (4 + 4).', stem=q7b, **B)
q7c = H.q(9, 'In June 2016 the UK voted to leave the EU', ' (i)')
add('sb-q7-c-i', '4-1', 'the-eu', ref('B', 7, '(c)(i)'), H.q(9, 'What do the letters EU stand for?', ' (ii)'), '6', 6,
    [point('r-1', H.traced('European Union.'), 6, 'The name, 6 marks.')], stem=q7c, **B)
pick('sb-q7-c-ii', '4-2', 'brexit-and-ireland', ref('B', 7, '(c)(ii)'),
     H.q(9, 'Discuss one economic effect which the exit of the UK from the EU', ' (26 marks)'), 'An area and one effect — any two',
     side('Irish firms exporting to UK', H.cut_cell('Irish firms (faced with possible tariffs', ['Irish firms (faced', 'If Irish firms can’t find',
                                                                                            'Some Irish exporters who rely']))
     + side('Tourism between Ireland & UK', H.cut_cell('If the euro increases in value', ['If the euro increases', 'If the euro decreases',
                                                                                         'The introduction of border controls']))
     + side('Consumers in Ireland', [cc('If tariffs are imposed by the EU on UK goods')]),
     2, 10, 'Two of the three areas, one effect each, 10 marks each (4 + 6).', stem=q7c, **B)

# Q8 ─ population; obesity; rural broadband
q8a = H.q(10, 'The population of Ireland counted in April 2016', ' (i)')
add('sb-q8-a-i', '3-0', 'the-cso', ref('B', 8, '(a)(i)'), H.q(10, 'What do the initials CSO stand for?', ' (ii)'), '9', 9,
    [point('r-1', H.traced('Central Statistics Office'), 9, 'The name, 9 marks.')], stem=q8a, **B)
add('sb-q8-a-ii', '3-5', 'the-census', ref('B', 8, '(a)(ii)'), H.q(10, 'What is the official term used for a count of the population?', ' (iii)'),
    '5', 5, [point('r-1', H.traced('Census (of Population)'), 5, 'The term, 5 marks.')], stem=q8a, **B)
pick('sb-q8-a-iii', '3-5', 'effects-of-a-growing-population', ref('B', 8, '(a)(iii)'),
     H.q(10, 'State and explain one possible economic effect which this increase', ' (30 marks)'),
     'An area, its effect and explanation — any two',
     [effect('Demand for Goods & services', 'Increase', 'There are more people requiring goods and services.'),
      effect('Provision of State services', 'Need for more services', cc('There will be an increased demand for state services')),
      effect('Irish Labour market', 'Increase in number of workers', cc('Participation in the labour market should'))],
     2, 8, 'Two areas, 8 marks each (4 + 4).', stem=q8a, **B)
pick('sb-q8-b', '1-3', 'measures-against-obesity', ref('B', 8, '(b)'),
     H.q(10, 'State and explain two other economic measures you would suggest', ' (20 marks)'), 'A measure — any two',
     H.split('Education in schools', '2 x 10 marks each (5 +5)',
             ['Education in schools', 'Better labelling of products', 'Calorie information displayed', 'Improved social infrastructure',
              '‘No fry zones’', 'Ban vending machines', '“Healthy Weight for Ireland']),
     2, 10, 'Two measures, 10 marks each (5 + 5).',
     stem=H.q(10, 'The Irish government is considering introducing a sugar tax in 2018', ' State'), **B)
q8c = H.q(10, '‘The government is going to privatise the long awaited rural broadband network.’', ' (i)')
add('sb-q8-c-i', '1-3', 'privatisation', ref('B', 8, '(c)(i)'), H.q(10, 'Explain the meaning of the term privatisation.', ' (ii)'), '9', 9,
    [point('r-1', H.traced('This is the sale / transfer of a state / government company to private owners.'), 9, 'The explanation, 9 marks.')],
    stem=q8c, **B)
pick('sb-q8-c-ii', '3-5', 'rural-broadband', ref('B', 8, '(c)(ii)'),
     H.q(10, 'Outline two economic advantages of this investment in broadband for rural areas.', ' (25 marks)'), 'An advantage — any two',
     H.split('Access to internet (for individuals and business)', '2 x 8 marks (4 + 4)',
             ['Access to internet', 'More business start', 'Economic growth', 'Sustainable rural communities']),
     2, 8, 'Two advantages, 8 marks each (4 + 4).', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
