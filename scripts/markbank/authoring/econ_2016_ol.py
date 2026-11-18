#!/usr/bin/env python3
"""Economics 2016 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2016-ol-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2016
Ordinary card existed. Section B restarts at Question 1, so every citation names
its section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The Ordinary scheme reprints each question above its
answer, so a slice always starts after the reprinted wording. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2016, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2016, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2016-OL-scheme-'
PAP = 'economics-2016-OL-paper-'
bl = H.bullets
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
# The scheme breaks a few words across a line end ("jus- tify"); the page prints them whole.
dehyphen = lambda t: re.sub(r'(\w)[-‐] (\w)', r'\1\2', t)


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it:
    "<heading> — <response>". Both halves trace."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def by_heading(rid, label, options, per, note):
    """One printed head ("Business", "Employees") and any one of its responses."""
    return heading(rid, H.traced(label) + ' — any one', options, per, note)


def underlined(page, stem, stem_start, end):
    """The paper prints "Explain the underlined term." three times on one page:
    the ask is sliced after its own stem, and the stem is folded into the
    card's question so the card names which term it is."""
    s = H.q(page, stem_start, end)
    return f"{stem} {s[s.rindex('Explain the underlined term.'):]}"


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ land as a factor of production
# The paper's blanks are ruled lines; the card sets each as an ellipsis so the
# statement still reads as one to complete.
q1 = re.sub(r'\s*_{2,}\s*', ' … ', H.ask(2, 'Complete the following statement:', ' (16 marks)')).replace(' … .', ' … .').strip()
add('sa-q1', '0-1', 'land-as-a-factor-of-production', ref('A', 1), ' '.join(q1.split()), '8 + 4 + 4', 16,
    [anyN('r-1', 'Each blank completed', 16, 3, 8,
          [f'{H.traced(before)} — {H.traced(word)}' for before, word in (
              ('anything supplied by', 'NATURE'), ('production of', 'GOODS'), ('The payment for land is called', 'RENT'))],
          'The three blanks: the first correct response 8 marks, the 2nd and 3rd 4 each.', steps=[8, 4, 4])],
    kind='fixed', **A)

# Q2 ─ protection against imports
add('sa-q2', '4-2', 'embargoes-quotas-tariffs-and-subsidies', ref('A', 2),
    # The four statements follow the ask, from the paper's own table rows.
    f"{H.q(2, 'Indicate by means of a tick', ' Statement Embargo')} {H.q(2, 'A tax on goods imported into the country.', ' (16 marks)')}",
    '8 + 4 + 2 + 2', 16,
    [anyN('r-1', 'Each statement ticked correctly', 16, 4, 8,
          [f'{cc(stmt)} — {H.traced(cat)}' for stmt, cat in (
              ('A tax on goods imported into the country', 'Tariff'), ('A complete ban on the importation', 'Embargo'),
              ('A physical limit placed by the government', 'Quota'), ('Any payment or assistance given by', 'Subsidy'))],
          'All four: the first correct response 8 marks, the 2nd 4, the 3rd and 4th 2 each.', steps=[8, 4, 2, 2])],
    kind='fixed', figure=PAP + 'p02-q2-table', **A)

# Q3 ─ marginal utility
q3 = H.q(2, 'The table below, when completed, illustrates', ' Number of units')
q3_table = PAP + 'p02-q3-table'
add('sa-q3-a', '1-1', 'completing-the-utility-table', ref('A', 3, '(a)'), H.q(2, 'Complete the blank spaces in the table above.', ' (b)'),
    '4 + 4 + 4', 12,
    [point(f'r-{unit}', f'Marginal utility of unit {unit} — {H.traced(mu)}', 4, f'Unit {unit}, 4 marks.')
     for unit, mu in ((3, '30'), (5, '10'), (6, '5'))],
    stem=q3, figure=q3_table, **A)
add('sa-q3-b', '1-1', 'when-diminishing-marginal-utility-sets-in', ref('A', 3, '(b)'),
    H.q(2, 'Explain why diminishing marginal utility sets in when 4 units are consumed.', ' (16 marks)'), '4', 4,
    [point('r-1', H.traced('The marginal utility received from the 4th unit consumed is less than that of the 3rd unit.'), 4,
           'The explanation, 4 marks.')], stem=q3, figure=q3_table, **A)

# Q4 ─ costs, profit and average cost
q4 = ' '.join([H.q(3, 'A firm produces 50 units each week.', ' Calculate'),
               H.q(3, 'Calculate the following, showing your workings.', ' Workings')])
add('sa-q4-a', '1-5', 'total-cost', ref('A', 4, '(a)'), H.q(3, 'Total cost of producing 50 units.', ' €'), '5 x 2', 10,
    [point(f'r-{k}', f'{label} — {H.traced(fig)}', 2, f'{label}, 2 marks: {H.traced("Each correct figure: 5 x 2 marks")}.')
     for k, label, fig in (('wages', 'Wages', '€5,000'), ('materials', 'Raw materials', '€25,000'), ('light', 'Light & Heat', '€3,000'),
                           ('rent', 'Rent of premises', '€7,000'), ('total', 'Total cost', '€40,000'))],
    stem=q4, **A)
add('sa-q4-b', '1-5', 'profit-on-sales', ref('A', 4, '(b)'), H.q(3, 'Profit made on sales.', ' €'), '3 x 1', 3,
    [point(f'r-{k}', f'{label} — {H.traced(fig)}', 1, f'{label}, 1 mark.')
     for k, label, fig in (('sales', 'Sales', '€50,000'), ('cost', 'Less total cost', '€40,000'), ('profit', 'Profit', '€10,000'))],
    stem=q4, **A)
add('sa-q4-c', '1-5', 'average-cost', ref('A', 4, '(c)'), H.q(3, 'Cost of producing one unit.', ' (c)'), '3 x 1', 3,
    [point(f'r-{k}', f'{label} — {H.traced(fig)}', 1, f'{label}, 1 mark.')
     for k, label, fig in (('cost', 'Total cost', '€40,000'), ('units', 'Divided by the units produced', '50'), ('average', 'Average cost', '€800'))],
    stem=q4, **A)

# Q5 ─ economists and their ideas
# The two printed lists follow the ask, each column read down as printed (the text layer
# interleaves them row by row, which would set each idea beside an economist it is not).
q5_ideas = [H.q(3, a, b) for a, b in (('A. The Multiplier', ' 1. Karl'), ('B. Law of Comparative', ' 2. Adam'),
                                      ('C. Laissez Faire', ' 3. John'), ('D. Worker exploitation', ' 4. David'))]
q5_who = [H.q(3, a, b) for a, b in (('1. Karl Marx', ' B. Law'), ('2. Adam Smith', ' C. Laissez'),
                                    ('3. John Maynard Keynes', ' D. Worker'), ('4. David Ricardo', ' Economic Idea A'))]
q5_idea_h, q5_who_h = H.q(3, 'Economic Idea Economist', ' A. The').rsplit(' ', 1)
add('sa-q5', '0-0', 'economists-and-their-ideas', ref('A', 5),
    f"{H.q(3, 'Match the economic ideas listed below with the related economist:', ' Economic Idea')} "
    f"{q5_idea_h}: {' '.join(q5_ideas)} {q5_who_h}: {' '.join(q5_who)}",
    '8 + 4 + 2 + 2', 16,
    [anyN('r-1', 'Each idea matched', 16, 4, 8,
          [f'{H.traced(idea)} — {H.traced(who)}' for idea, who in (
              ('The Multiplier', 'John Maynard Keynes'), ('Law of Comparative Advantage', 'David Ricardo'),
              ('Laissez Faire', 'Adam Smith'), ('Worker exploitation in a capitalist system.', 'Karl Marx'))],
          'All four (the scheme’s answer row: A 3, B 4, C 2, D 1): the first correct response 8 marks, the 2nd 4, the 3rd and '
          '4th 2 each.', steps=[8, 4, 2, 2])],
    kind='fixed', figure=PAP + 'p03-q5-lists', **A)

# Q6 ─ homelessness
add('sa-q6', '3-1', 'homelessness', ref('A', 6, '(a)–(b)'),
    ' '.join([H.q(3, 'Outline one economic reason for the increase in homelessness.', ' (b)'),
              H.q(3, 'Outline one possible economic measure that could be taken', ' (17 marks)')]),
    '10 + 7', 17,
    [anyN('r-1', 'One reason and one measure', 17, 2, 10,
          side('(a) Outline one reason for the increase in homelessness',
               H.split('Growing demand for housing caused by increased population.', '(b) Outline one possible',
                       ['Growing demand for housing', 'Reduced supply of social houses', 'Reduced availability of rental',
                        'Rising rent costs', 'Poverty / unemployment', 'High personal debt', 'Central Bank regulation',
                        'Profit margin on new build']))
          + side('(b) Outline one possible economic measure',
                 H.split('Increase availability of social housing', 'First correct response: 10 marks.',
                         ['Increase availability of social housing', 'Provision of modular housing', 'Repair and supply boarded-up',
                          'Increase provision of emergency', 'Increase subsidies for people', 'Reduce taxation on construction',
                          'New regulations introduced'])),
          'One reason for (a) and one measure for (b). The scheme prices the two by order, not by part: the first correct '
          'response 10 marks, the second 7.', steps=[10, 7])],
    kind='fixed', stem=H.q(3, 'Homelessness is becoming a major social problem', ' (a)'), **A)

# Q7 ─ plain packaging
q7 = H.q(4, 'The Irish government is considering only permitting the sale of cigarettes', ' (a)')
add('sa-q7-a', '2-0', 'branding', ref('A', 7, '(a)'), H.q(4, 'Explain the term branding.', ' (b)'), '10', 10,
    [point('r-1', H.traced('The practice of creating a name, symbol or design that identifies and differentiates a product from other similar products.'),
           10, 'The explanation, 10 marks.')], stem=q7, **A)
pick('sa-q7-b', '1-3', 'why-plain-packaging', ref('A', 7, '(b)'),
     H.q(4, 'Outline one reason why the Irish government is considering introducing this measure.', ' (17 marks)'), 'A reason — any one',
     H.split('To help reduce the demand for cigarettes', 'One reason: 7 marks.',
             ['To help reduce the demand', 'Makes advertising by tobacco', 'If consumption declines', 'Expenditure on health may decrease']),
     1, 7, 'One reason, 7 marks.', stem=q7, **A)

# Q8 ─ the black economy
q8 = H.q(4, '“The size of the black economy could be as high as €25 billion a year.”', ' (a)')
add('sa-q8-a', '3-0', 'the-black-economy', ref('A', 8, '(a)'), H.q(4, 'Explain the term black economy.', ' (b)'), '5', 5,
    [point('r-1', H.traced('Economic activity which takes place which is not recorded and therefore not included in national income accounts.'),
           5, 'The explanation, 5 marks.')], stem=q8, **A)
add('sa-q8-b', '3-0', 'who-the-black-economy-affects', ref('A', 8, '(b)'),
    H.q(4, 'Outline how each of the following is affected by activities in the black economy.', ' (17 marks)'), '8 + 4', 12,
    [anyN('r-1', 'One effect on each', 12, 2, 8,
          side('Irish government', H.split('Taxation: reduction in taxation revenues', 'Irish businesses:',
                                           ['Taxation: reduction', 'Increased government spending', 'Increased social welfare bill',
                                            'Reduction in provision of state services']))
          + side('Irish businesses', H.split('Reduction in sales / profits as consumers', 'First correct response: 8 marks.',
                                             ['Reduction in sales / profits', 'Reduction in workforce', 'Pressure to reduce prices'])),
          'One effect on the government and one on businesses. The scheme prices the two by order, not by side: the '
          'first correct response 8 marks, the second 4.', steps=[8, 4])],
    kind='fixed', stem=q8, **A)

# Q9 ─ the symbols of income elasticity
add('sa-q9', '1-4', 'symbols-of-income-elasticity', ref('A', 9),
    H.q(4, 'The formula for measuring Income Elasticity of Demand (YED) is as follows:', ' ∆Q') + ' '
    + H.q(4, 'Complete the following table to indicate what each of the above symbols represent:', ' ∆Q'), '8 + 3 + 3 + 3', 17,
    [anyN('r-1', 'Each blank symbol explained', 17, 4, 8,
          [f'{H.traced(sym)} — {H.traced(meaning)}' for sym, meaning in (
              ('∆Q', 'Change in quantity demanded of the good.'), ('∆Y', 'Change in the consumer’s income.'),
              ('Y2', 'New income of the consumer.'), ('Q1', 'Original quantity demanded of the good.'))],
          'The four symbols the paper leaves blank (it prints Y1 and Q2): the first correct response 8 marks, the 2nd, 3rd '
          'and 4th 3 each.', steps=[8, 3, 3, 3])],
    kind='fixed', figure=PAP + 'p04-q9-table', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ perfect competition; alcohol
q1 = H.q(5, 'The diagram below represents the long run equilibrium of a firm in Perfect Competition.', ' P MC')
q1_fig = PAP + 'p05-q1-diagram'
add('sb-q1-a-i', '2-0', 'labels-of-perfect-competition', ref('B', 1, '(a)(i)'),
    H.q(5, 'Copy the diagram into your answer book.', ' (ii)'), '6 @ 4', 24,
    [point(f'r-{lab.lower()}', f'{lab} — {H.traced(full)}', 4, f'{lab}, 4 marks' + (' (2 + 2).' if len(lab) == 2 else '.'))
     for lab, full in (('P', 'Price'), ('Q', 'Quantity'), ('AC', 'Average Cost'), ('MC', 'Marginal Cost'),
                       ('AR', 'Average Revenue'), ('MR', 'Marginal Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'price-and-output-in-perfect-competition', ref('B', 1, '(a)(ii)'),
    H.q(5, 'Equilibrium occurs at point G on the diagram.', ' (30 marks)'), '3 + 3', 6,
    [point('r-p1', 'P1 — ' + H.traced('the price the firm will charge for its output'), 3,
           'P1, 3 marks: ' + H.traced('3 marks each x 2 = 6 marks') + '. The completed diagram is shown with the answer.'),
     point('r-q1', 'Q1 — ' + H.traced('the output the company will produce'), 3, 'Q1, 3 marks.')],
    stem=q1, figure=SOL + 'p10-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
q1b = H.q(5, 'One of the characteristics of perfect competition is that perfect knowledge exists.', ' (i)')
add('sb-q1-b-i', '2-0', 'perfect-knowledge', ref('B', 1, '(b)(i)'), H.q(5, 'Explain the underlined term.', ' (ii) State two other'), '4', 4,
    [point('r-1', H.opt('In the market every firm has full knowledge', ' Consumers'), 4,
           'The explanation, 4 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('Consumers are fully aware of the prices being charged for products.')])],
    stem=q1b, **B)
pick('sb-q1-b-ii', '2-0', 'characteristics-of-perfect-competition', ref('B', 1, '(b)(ii)–(iii)'),
     ' '.join([H.q(5, 'State two other characteristics of perfect competition.', ' (iii)'),
               H.q(5, 'Write brief notes explaining each of these two characteristics.', ' (20 marks)')]),
     'A characteristic, with its note — any two',
     H.split('The goods are homogeneous.', '2 x 8 marks each',
             ['The goods are homogeneous.', 'There are many buyers', 'There are many sellers', 'Free entry and exit.',
              'Firm tries to maximise profits.', 'Elastic supply of factors']),
     2, 8, 'Two characteristics, 8 marks each: ' + H.traced('State: 2 x4 marks each.') + ' ' + H.traced('Explanation: 2 x4 marks each.')
     + ' The scheme prices (ii) and (iii) together and names the characteristics only.', stem=q1b, **B)
q1c = H.q(5, 'Alcohol advertising is to be banned in all sports grounds.', ' (i)')
pick('sb-q1-c-i', '1-3', 'sport-and-the-alcohol-advertising-ban', ref('B', 1, '(c)(i)'),
     H.q(5, 'State one reason why sporting organisations may not favour the above measure.', ' (ii)'), 'A reason — any one',
     H.split('Loss of advertising revenue for the firms', '5 marks (2+3)',
             ['Loss of advertising revenue', 'Reduction in quality of services', 'Increase in charges / fees', 'May have to seek alternative']),
     1, 5, 'One reason, 5 marks (2 + 3).', stem=q1c, **B)
pick('sb-q1-c-ii', '1-3', 'reducing-alcohol-consumption', ref('B', 1, '(c)(ii)'),
     H.q(5, 'State and explain two other measures which could be taken to help reduce', ' (iii)'), 'A measure — any two',
     # The split's trailing-numeral cut would take "21." for a list number: that
     # option is sliced whole.
     [H.traced('Age restrictions: raise the legal age for the consumption of alcohol to 21.') if o.startswith('Age restrictions') else o
      for o in H.split('Taxes: increase taxes such as excise duty', '2 x 5 marks (2+3)',
                       ['Taxes:', 'Regulate availability:', 'Introduce limits to the amount', 'Age restrictions:', 'Sales points:',
                        'Sponsorship:', 'Consumer Awareness:', 'Introduce minimum pricing:', 'Introduce harsher penalties'])],
     2, 5, 'Two measures, 5 marks each (2 + 3).', stem=q1c, **B)
pick('sb-q1-c-iii', '1-3', 'benefits-of-reduced-alcohol-consumption', ref('B', 1, '(c)(iii)'),
     H.q(5, 'Outline two benefits to society of reduced alcohol consumption.', ' (25 marks)'), 'A benefit — any two',
     H.split('Reduced pressure on hospitals / reduction in health spending', '2 x 5 marks (2+3)',
             ['Reduced pressure on hospitals', 'Reduction in crime levels', 'Population healthier', 'Life expectancy:',
              'Increased worker productivity', 'Reduction in absenteeism', 'Reduction in the number of alcohol']),
     2, 5, 'Two benefits, 5 marks each (2 + 3).', stem=q1c, **B)

# Q2 ─ electric cars; shifts in demand and supply; banking
q2a = H.q(6, 'Assume the diagram below represents the market for electric cars in Ireland.', ' 1 Supply')
q2a_fig = PAP + 'p06-q2a-diagram'
add('sb-q2-a-i', '1-0', 'labelling-the-market-diagram', ref('B', 2, '(a)(i)'),
    H.q(6, 'Copy the diagram into your answer book. Clearly label each of the lines marked 1 to 3.', ' (ii)'), '3 x 2', 6,
    [point(f'r-{n}', f'{n} — {H.traced(label)}', 2, f'Line {n}, 2 marks.') for n, label in ((1, 'Price'), (2, 'Quantity'), (3, 'Demand'))],
    stem=q2a, figure=SOL + 'p13-q2a-diagram', **B)
beside_ask(cards[-1], q2a_fig)
add('sb-q2-a-ii', '1-0', 'equilibrium-price-and-quantity', ref('B', 2, '(a)(ii)'),
    H.q(6, 'Show on your diagram:', ' (iii)'), '2 + 2', 4,
    [point('r-p1', H.traced('equilibrium price P1'), 2, 'P1, 2 marks. The completed diagram is shown with the answer.'),
     point('r-q1', H.traced('equilibrium quantity Q1'), 2, 'Q1, 2 marks.')],
    stem=q2a, figure=SOL + 'p13-q2a-diagram', **B)
beside_ask(cards[-1], q2a_fig)
pick('sb-q2-a-iii', '0-2', 'advantages-of-electric-cars', ref('B', 2, '(a)(iii)'),
     H.q(6, 'Outline two possible advantages for Ireland of increased usage of electric cars.', ' (iv)'), 'An advantage — any two',
     H.split('Reduced emissions / cleaner environment', '2 x 5 marks (2+3) each',
             ['Reduced emissions', 'Less waste of scarce resources', 'Newer vehicles on roads', 'Car running costs are reduced']),
     2, 5, 'Two advantages, 5 marks each (2 + 3).', stem=q2a, **B)
pick('sb-q2-a-iv', '1-3', 'encouraging-electric-cars', ref('B', 2, '(a)(iv)'),
     H.q(6, 'Outline one measure the Irish government could consider to encourage consumers', ' (25 marks)'), 'A measure — any one',
     H.split('Offer a grant towards the purchase price', '5 marks (2+3)',
             ['Offer a grant', 'Reduce motor tax', 'Provide more ‘plug-in’ points', 'Allow electric cars to use bus lanes',
              'Free parking for electric cars', 'Remove tolls', 'Offer incentives to convert']),
     1, 5, 'One measure, 5 marks (2 + 3).', stem=q2a, **B)
q2b = ' '.join([H.q(6, 'The following factors cause either a demand curve or a supply curve', ' In relation'),
                H.q(6, 'In relation to each factor above, answer the following three questions:', ' (i)')])
income, tech = H.traced('Income levels in the economy fall'), H.traced('The firm’s production technology improves')
for part, concept, ask, nxt, a, b, per in (
        ('i', 'which-curve-shifts', 'state whether the demand curve or supply curve will shift', ' (ii)',
         cc('Demand Curve', whole=True), cc('Supply Curve', whole=True), 4),
        ('ii', 'which-way-the-curve-shifts', 'state whether the curve you mention will shift to the right or the left', ' (iii)',
         cc('Left', whole=True), cc('Right', whole=True), 3),
        ('iii', 'why-the-curve-shifts', 'explain why the curve has shifted in the direction you have stated.', ' (20 marks)',
         cc('Consumers cannot afford to buy'), cc('The firm’s ability to produce'), 3)):
    add(f'sb-q2-b-{part}', '1-0', concept, ref('B', 2, f'(b)({part})'), H.q(6, ask, nxt), f'{per} + {per}', 2 * per,
        [point('r-income', f'{income} — {a}', per, f'Falling incomes, {per} marks.'),
         point('r-technology', f'{tech} — {b}', per, f'Better technology, {per} marks.')],
        stem=q2b, **B)
q2c = H.q(6, 'Electronic banking refers to the use of computers to carry out banking transactions.', ' (i)')
pick('sb-q2-c-i', '3-4', 'functions-of-commercial-banks', ref('B', 2, '(c)(i)'),
     H.q(6, 'State and explain two functions of commercial banks.', ' (ii)'), 'A function — any two',
     [H.traced(x) for x in ('Savings Facilities.', 'Lending.', 'Operate cheque system/current accounts', '24 Hour Banking.',
                            'Computerised Transfer of Money/Automated Bill Payment.', 'Foreign Exchange.')],
     2, 5, 'Two functions, 5 marks each (2 + 3). The scheme names the functions only.', stem=q2c, **B)
pick('sb-q2-c-ii', '3-4', 'why-banks-favour-electronic-banking', ref('B', 2, '(c)(ii)'),
     H.q(6, 'Outline two economic reasons why a bank may favour electronic banking.', ' (iii)'), 'A reason — any two',
     H.split('Reduce staff costs:', '2 x 5 marks (2 + 3)',
             ['Reduce staff costs:', 'Increase profits:', 'Facilitate increased use of technology', 'Encourages use of on-line',
              'Increased efficiency:', 'Improved customer service.']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q2c, **B)
pick('sb-q2-c-iii', '3-4', 'disadvantages-of-electronic-banking', ref('B', 2, '(c)(iii)'),
     H.q(6, 'Outline two possible disadvantages of electronic banking for bank customers.', ' (30 marks)'), 'A disadvantage — any two',
     H.split('IT Literacy:', '2 x 5 marks (2+3)',
             ['IT Literacy:', 'May encourage people to keep cash', 'Difficulties at ATMs:', 'Security issues:',
              'Some services are not suitable']),
     2, 5, 'Two disadvantages, 5 marks each (2 + 3).', stem=q2c, **B)

# Q3 ─ the factors of production and enterprise; the minimum wage; the Web Summit
q3a = H.q(7, 'An entrepreneur takes a risk in combining land', ' (i)')
add('sb-q3-a-i', '0-1', 'labour-and-capital', ref('B', 3, '(a)(i)'),
    H.q(7, 'State and explain the two factors of production, other than enterprise and land.', ' (ii)'), '2 x (3 + 3)', 12,
    [point('r-labour', f"{H.traced('Labour')} — {H.traced(cc('• the human effort involved').lstrip('• '))}", 6, 'Labour, 6 marks (3 + 3).'),
     point('r-capital', f"{H.traced('Capital')} — {H.traced(cc('• man-made wealth').lstrip('• ').replace(' / • ', ' / '))}", 6,
           'Capital, 6 marks (3 + 3).')],
    stem=q3a, **B)
pick('sb-q3-a-ii', '0-1', 'benefits-of-entrepreneurs', ref('B', 3, '(a)(ii)'),
     H.q(7, 'Outline two benefits of entrepreneurs for the Irish economy.', ' (24 marks)'), 'A benefit — any two',
     H.split('Helps create / maintain jobs.', '2 x 6 marks (3+3)',
             ['Helps create / maintain jobs.', 'Improves the Balance of Payments.', 'Encourage further investment', 'Innovation:',
              'Help generate tax revenue']),
     2, 6, 'Two benefits, 6 marks each (3 + 3).', stem=q3a, **B)
q3b = H.q(7, 'The national minimum wage in Ireland was increased', ' (i)')
add('sb-q3-b-i', '2-1', 'the-national-minimum-wage', ref('B', 3, '(b)(i)'),
    underlined(7, q3b, 'The national minimum wage in Ireland was increased', ' (ii)'),
    '7 (4 + 3)', 7, [point('r-1', H.traced('The lowest wage employers must by law pay their employees.'), 7, 'The explanation, 7 marks (4 + 3).')],
    **B)
pick('sb-q3-b-ii', '2-1', 'aims-of-a-minimum-wage', ref('B', 3, '(b)(ii)'),
     H.q(7, 'Outline two aims of a national minimum wage.', ' (iii)'), 'An aim — any two',
     H.split('Increase worker’s standard of living', '2 x 5 marks (2 + 3)',
             ['Increase worker’s standard of living', 'Increase the incentive to work', 'Introduce an equitable distribution',
              'Protection of must vulnerable', 'Reduce unemployment:']),
     2, 5, 'Two aims, 5 marks each (2 + 3).', stem=q3b, **B)
pick('sb-q3-b-iii', '2-1', 'costs-of-a-higher-minimum-wage', ref('B', 3, '(b)(iii)'),
     H.q(7, 'Outline two possible economic disadvantages of an increase in the national minimum wage.', ' (27 marks)'),
     'A disadvantage — any two',
     H.split('Firms’ costs would increase', '2 x 5 marks (2 + 3)',
             ['Firms’ costs would increase', 'Reduced employment.', 'Quality of service', 'Risk of closure', 'Reduced competitiveness.',
              'Decline in investment.']),
     2, 5, 'Two disadvantages, 5 marks each (2 + 3).', stem=q3b, **B)
q3c = ' '.join([H.q(7, 'The Web Summit held annually in Dublin', ' Note:'), H.q(7, 'Note: the Web Summit is an annual technology', ' (i)')])
pick('sb-q3-c-i', '4-2', 'hosting-major-conferences', ref('B', 3, '(c)(i)'),
     H.q(7, 'Outline two advantages to the local economy in Dublin of hosting major conferences', ' (ii)'), 'An advantage — any two',
     H.split('Increased demand for hospitality services:', '2 x 6 marks (3 + 3)',
             ['Increased demand for hospitality', 'Increased short term employment', 'Attract further international conferences',
              'Boost for Irish IT']),
     2, 6, 'Two advantages, 6 marks each (3 + 3).', stem=q3c, **B)
pick('sb-q3-c-ii', '4-2', 'attracting-international-conferences', ref('B', 3, '(c)(ii)'),
     H.q(7, 'State two measures that either the Irish government or local government/authorities', ' (24 marks)'), 'A measure — any two',
     H.split('Hotel accommodation:', '2 x 6 marks (3 + 3)',
             ['Hotel accommodation:', 'Ease transport concerns:', 'Improve broadband availability', 'Dedicated IDA TEAM',
              'Investment in a national convention']),
     2, 6, 'Two measures, 6 marks each (3 + 3).', stem=q3c, **B)

# Q4 ─ the census; a centrally planned economy; LDCs
q4a = H.q(7, 'In April 2016 the CSO conducted a count of Ireland’s population', ' (i)')
add('sb-q4-a-i', '3-0', 'the-cso', ref('B', 4, '(a)(i)'), H.q(7, 'What do the initials CSO stand for?', ' (ii)'), '5', 5,
    [point('r-1', H.traced('Central Statistics Office.'), 5, 'The name, 5 marks.')], stem=q4a, **B)
add('sb-q4-a-ii', '3-5', 'the-census', ref('B', 4, '(a)(ii)'), H.q(7, 'What is the official term used for a count of the population?', ' (iii)'),
    '5', 5, [point('r-1', H.traced('Census (of Population).'), 5, 'The term, 5 marks.')], stem=q4a, **B)
pick('sb-q4-a-iii', '3-5', 'the-cost-of-the-census', ref('B', 4, '(a)(iii)'),
     H.q(7, 'State one possible expenditure item included in the cost of €55m.', ' (iv)'), 'An expenditure item — any one',
     H.split('Wages for enumerators.', '5 marks\n(iv)', ['Wages for enumerators.', 'Training for enumerators.', 'Printing of the Census forms.',
                                                       'Distribution and collection of the forms.']),
     1, 5, 'One item, 5 marks.', stem=q4a, **B)
add('sb-q4-a-iv', '3-5', 'uses-of-census-data', ref('B', 4, '(a)(iv)'),
    H.q(7, 'Explain one use each of the following could make of the data collected:', ' (25 marks)'), '2 x 5 (3 + 2)', 10,
    [by_heading('r-business', 'Business', H.cut_cell('Future levels of consumer demand', ['Future levels of consumer demand', 'Population data',
                                                                                         'Labour market']), 5,
                'One use for businesses, 5 marks (3 + 2).'),
     by_heading('r-government', 'Irish Government', H.cut_cell('Infrastructural requirements', ['Infrastructural requirements',
                                                                                                'Provision of essential services',
                                                                                                'Pension / financial planning',
                                                                                                'Demographic changes',
                                                                                                'Qualifications of workforce']), 5,
                'One use for the government, 5 marks (3 + 2).')],
    kind='fixed', stem=q4a, **B)
q4b = H.q(7, 'China is no longer a centrally planned economy', ' (i)')
add('sb-q4-b-i', '1-0', 'a-centrally-planned-economy', ref('B', 4, '(b)(i)'),
    underlined(7, q4b, 'China is no longer a centrally planned economy', ' (ii)'), '5', 5, [point('r-1', H.traced('Resources are allocated by the state through a central planning mechanism.'), 5,
                   'The explanation, 5 marks. The scheme also accepts its second statement.',
                   accepts=[H.traced('The government intervenes to regulate all economic activity.')])], **B)
pick('sb-q4-b-ii', '3-5', 'ending-the-one-child-policy', ref('B', 4, '(b)(ii)'),
     H.q(7, 'Outline two advantages of the change in the “one-child policy”', ' (iii)'), 'An advantage — any two',
     H.split('Demographics: the structure of the population in China', '2 x 5 marks (3 + 2)',
             ['Demographics:', 'More freedom for people:', 'Future workers:', 'Plan for China’s older population:',
              'Increased demand for goods and services for children.']),
     2, 5, 'Two advantages, 5 marks each (3 + 2).', stem=q4b, **B)
pick('sb-q4-b-iii', '1-0', 'life-in-a-centrally-planned-economy', ref('B', 4, '(b)(iii)'),
     H.q(7, 'State and explain two possible economic disadvantages for citizens who live in a centrally planned economy.', ' (25 marks)'),
     'A disadvantage — any two',
     H.split('Less freedom for individuals', '2 x 5 marks (3 + 2)',
             ['Less freedom for individuals', 'Restricted choice for consumers', 'Social costs may exceed private costs',
              'Lack of independent media']),
     2, 5, 'Two disadvantages, 5 marks each (3 + 2).', stem=q4b, **B)
q4c = H.q(7, 'Economic development continues to be a key economic aim', ' (i)')
add('sb-q4-c-i', '4-0', 'economic-development', ref('B', 4, '(c)(i)'),
    underlined(7, q4c, 'Economic development continues to be a key economic aim', ' (ii)'),
    '5 (3 + 2)', 5, [point('r-1', H.opt('An increase in the level of income/ standard of living', '5 marks: 3 marks'), 5,
                           'The explanation, 5 marks (3 + 2).')], **B)
pick('sb-q4-c-ii', '4-0', 'difficulties-in-ldcs', ref('B', 4, '(c)(ii)'),
     H.q(7, 'Outline two economic difficulties which citizens of LDCs experience.', ' (iii)'), 'A difficulty — any two',
     [H.traced(x) for x in ('High population growth rates in LDCs.', 'Low life expectancy.', 'High foreign debts / lack of capital.',
                            'Over-dependence on one crop in LDCs / Famine',
                            'High percentage of the population engaged in extractive/primary industries.', 'Poor infrastructure in LDCs.',
                            'Low per capita incomes in LDCs.', 'Poor levels of education/literacy in LDCs.', 'Exploitation by large multinationals.')],
     2, 5, 'Two difficulties, 5 marks each (3 + 2).', stem=q4c, **B)
pick('sb-q4-c-iii', '4-0', 'solutions-for-ldcs', ref('B', 4, '(c)(iii)'),
     H.q(7, 'Suggest two possible solutions to the economic difficulties identified.', ' (25 marks)'), 'A solution — any two',
     H.split('Re-structure their national debts or cancel their debt', '2 x 5 marks (3 + 2)',
             ['Re-structure their national debts', 'Provision of clean water', 'Provide aid for infrastructural',
              'Better terms of trade', 'Introduce technology to improve yields']),
     2, 5, 'Two solutions, 5 marks each (3 + 2).', stem=q4c, **B)

# Q5 ─ taxes and the sugar tax; the USC; unemployment
q5a = H.q(8, 'Irish citizens contribute both direct taxes and indirect taxes to the government.', ' (i)')
examples = lambda first, names: [H.traced(x) for x in names if x in cc(first)]
add('sb-q5-a-i', '3-1', 'direct-and-indirect-taxes', ref('B', 5, '(a)(i)'),
    H.q(8, 'Explain each of the underlined terms and state one example of each.', ' (ii)'), '(3 + 2) x 2', 10,
    [point('r-direct', f"{H.traced('Direct taxes')} — {cc('These are taxes on income or')}", 3, 'Direct taxes explained, 3 marks.'),
     heading('r-direct-example', 'An example of a direct tax — any one', examples('Income Tax Deposit', ('Income Tax', 'Deposit Interest Retention Tax', 'Corporation Profits Tax')), 2, 'One direct tax, 2 marks.'),
     point('r-indirect', f"{H.traced('Indirect taxes')} — {cc('These are taxes on goods')}", 3, 'Indirect taxes explained, 3 marks.'),
     heading('r-indirect-example', 'An example of an indirect tax — any one', examples('Value Added Tax Excise', ('Value Added Tax', 'Excise Duties', 'Vehicle Registration Tax')), 2, 'One indirect tax, 2 marks.')],
    kind='fixed', stem=q5a, **B)
pick('sb-q5-a-ii', '3-1', 'uses-of-tax-revenue', ref('B', 5, '(a)(ii)'),
     H.q(8, 'Outline two uses of taxation revenue by the government.', ' (iii)'), 'A use — any two',
     H.split('To provide revenue for the government\nThe government', '2 x 5 marks (2 + 3)',
             ['To provide revenue for the government', 'To provide essential goods', 'To help re-distribute income',
              'To develop the infrastructure', 'To help industry', 'Achieve desirable social objectives',
              'To help achieve a favourable Balance', 'To achieve other government objectives']),
     2, 5, 'Two uses, 5 marks each (2 + 3).', stem=q5a, **B)
q5aiii = H.q(8, 'The Irish government may consider introducing a sugar tax', ' (30 marks)')
for word, label, start, end, firsts in (
        ('for', 'Two arguments in favour', 'Revenue for state\nThis tax', 'OR\nTwo arguments against',
         ['Revenue for state', 'Reduce consumption of sugary foods', 'Help fund health initiatives', 'Reduce future health costs',
          'Healthier population', 'Opportunities for entrepreneurs']),
        ('against', 'Two arguments against its introduction', 'Higher Prices\nConsumers', '2 x 5 marks (2 + 3)',
         ['Higher Prices', 'Job losses', 'A sugar tax is regressive'])):
    pick(f'sb-q5-a-iii-{word}', '1-3', 'for-or-against-a-sugar-tax', ref('B', 5, '(a)(iii)', word),
         f'{q5aiii} Justify the choice: {word.upper()}.', f'{H.traced(label)} — any two', H.split(start, end, firsts), 2, 5,
         'Two arguments, 5 marks each (2 + 3). The scheme credits arguments for OR against, each with its own list.',
         stem=q5a, **B)
q5b = H.q(8, 'In Budget 2016 the Government reduced the rates of USC.', ' (i)')
add('sb-q5-b-i', '3-1', 'the-usc', ref('B', 5, '(b)(i)'), H.q(8, 'What do the initials USC stand for?', ' (ii)'), '5', 5,
    [point('r-1', H.traced('Universal Social Charge'), 5, 'The name, 5 marks.')], stem=q5b, **B)
split_bullets = lambda cell: [H.traced(x.strip()) for x in cc(cell).split('•') if x.strip()]
add('sb-q5-b-ii', '3-1', 'cutting-the-usc', ref('B', 5, '(b)(ii)'),
    H.q(8, 'Explain one possible economic effect which reductions in the USC rates may have', ' (20 marks)'), '3 x 5 (2 + 3)', 15,
    [by_heading(f'r-{k}', who, side(statement, split_bullets(first)), 5,
                f'One effect on {what}, 5 marks: ' + H.traced('State: 2 marks. Explain: 3 marks') + '.')
     for k, who, what, statement, first in (
         ('employees', 'Employees', 'employees', 'Higher disposable income', '• Some employees may buy more'),
         ('imports', 'Imports into Ireland', 'imports', 'May increase.', '• With higher disposable income'),
         ('employment', 'Level of employment', 'the level of employment', 'May increase.', '• If spending increases'))],
    kind='fixed', stem=q5b, **B)
q5c = H.q(8, '“The unemployment rate is continuing to fall', ' (i)')
add('sb-q5-c-i', '3-2', 'measuring-unemployment', ref('B', 5, '(c)(i)'), H.q(8, 'Name one method of measuring unemployment in Ireland.', ' (ii)'),
    '6', 6, [point('r-1', H.traced('Live Register or Quarterly National Household Survey.'), 6, 'One method, 6 marks.')], stem=q5c, **B)
pick('sb-q5-c-ii', '3-2', 'advantages-of-falling-unemployment', ref('B', 5, '(c)(ii)'),
     H.q(8, 'State and explain two possible economic advantages for Ireland of this fall in unemployment.', ' (iii)'), 'An advantage — any two',
     [H.traced(x) for x in ('Increase in standard of living / reduced poverty.', 'Increase in government tax revenues.', 'Reduction in social welfare.',
                            'Economic growth.', 'Increase in investment.', 'Expansion by firms.', 'Improved outlook for rural towns.')],
     2, 7, 'Two advantages, 7 marks each (4 + 3). The scheme names the advantages only.', stem=q5c, **B)
pick('sb-q5-c-iii', '3-2', 'reducing-youth-unemployment', ref('B', 5, '(c)(iii)'),
     H.q(8, 'Suggest one measure the Irish government could take to reduce youth unemployment.', ' (25 marks)'), 'A measure — any one',
     [H.traced(x) for x in ('Provide more opportunities for education / training.', 'Subsidise work placements/internships.',
                            'Lower PRSI contributions.', 'More school based vocational training / introduce entrepreneurship courses in school.',
                            'Taxation / social welfare policy / minimum wage rates.', 'Abolition / reduction of third level fees.')],
     1, 5, 'One measure, 5 marks (3 + 2).', stem=q5c, **B)

# Q6 ─ imports; tourism; MNCs
q6a = H.q(8, 'Irish people attending the Euro 2016', ' (i)')
add('sb-q6-a-i', '4-2', 'visible-and-invisible-imports', ref('B', 6, '(a)(i)'),
    H.q(8, 'Distinguish between a visible import and an invisible import.', ' (ii)'), '5 + 5', 10,
    [point('r-visible', 'Visible import — ' + H.traced('This is the purchase of a foreign good by a person in Ireland / money leaves Ireland.'), 5,
           'A visible import, 5 marks.'),
     point('r-invisible', 'Invisible import — ' + H.traced('This is the purchase of a foreign service by a person in Ireland / money leaves Ireland.'),
           5, 'An invisible import, 5 marks.')], stem=q6a, **B)
pick('sb-q6-a-ii', '4-2', 'why-imports-matter', ref('B', 6, '(a)(ii)'),
     H.q(8, 'State and explain two reasons why imports are important for the Irish economy.', ' (20 marks)'), 'A reason — any two',
     H.split('More choice for consumers / Higher standard of living', '2 x 5 marks (2 + 3)',
             ['More choice for consumers', 'Raw materials unavailable', 'Employment in the distribution', 'Tax revenue for the state',
              'Small domestic market']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q6a, **B)
q6b = H.q(8, '“More than 8 million tourists are expected to visit Ireland in 2016.”', ' (i)')
pick('sb-q6-b-i', '4-2', 'advantages-of-more-tourists', ref('B', 6, '(b)(i)'),
     H.q(8, 'State and explain two economic advantages of this development for the Irish economy.', ' (ii)'), 'An advantage — any two',
     H.split('Increased employment\nMore jobs', '2 x 5 marks (2 + 3)',
             ['Increased employment', 'Increased income / GNP', 'Benefits to businesses', 'Tax revenues', 'International reputation',
              'Spin-off industries benefit']),
     2, 5, 'Two advantages, 5 marks each (2 + 3).', stem=q6b, **B)
pick('sb-q6-b-ii', '4-2', 'keeping-tourist-numbers-rising', ref('B', 6, '(b)(ii)'),
     H.q(8, 'Outline two measures which firms in the Irish Tourism Industry could take', ' (iii)'), 'A measure — any two',
     H.split('Offer competitive air fares / extend the number of routes', '2 x 5 marks (2 + 3)',
             ['Offer competitive air fares', 'Advertising & Promotion', 'More competitive prices', 'Offer special promotions']),
     2, 5, 'Two measures, 5 marks each (2 + 3).', stem=q6b, **B)
pick('sb-q6-b-iii', '4-2', 'why-ireland-attracts-tourists', ref('B', 6, '(b)(iii)'),
     H.q(8, 'Outline one reason why Ireland is considered a popular tourist location.', ' (25 marks)'), 'A reason — any one',
     H.split('Fall in the value of the euro', '5 marks (2 + 3)',
             ['Fall in the value of the euro', 'Price / availability of air transport', 'Targeted advertising', 'Ireland has a wide range']),
     1, 5, 'One reason, 5 marks (2 + 3).', stem=q6b, **B)
q6c = H.q(8, 'Apple, an example of an MNC operating in Ireland', ' (i)')
add('sb-q6-c-i', '4-1', 'mnc-in-full', ref('B', 6, '(c)(i)'), H.q(8, 'What do the initials MNC mean?', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Multinational Company.'), 6, 'The name, 6 marks.')], stem=q6c, **B)
pick('sb-q6-c-ii', '4-1', 'naming-an-mnc', ref('B', 6, '(c)(ii)'), H.q(8, 'Name one other MNC located in Ireland.', ' (iii)'), 'An MNC — any one',
     [H.traced(x.strip()) for x in H.chunk('Google / Facebook', '\n').split(' / ')], 1, 6,
     'One MNC, 6 marks: any MNC located in Ireland, such as those the scheme lists.', stem=q6c, **B)
pick('sb-q6-c-iii', '4-1', 'why-apple-chose-ireland', ref('B', 6, '(c)(iii)'),
     H.q(8, 'State one reason why Apple may have located in Ireland.', ' (iv)'), 'A reason — any one',
     [H.traced(x) for x in ('Availability of a skilled workforce.', 'Availability of land/planning permission.', 'Access to good infrastructure.',
                            'Availability of state incentives.', 'Low rates of taxation.', 'Access to large European market.')],
     1, 6, 'One reason, 6 marks (3 + 3).', stem=q6c, **B)
pick('sb-q6-c-iv', '4-1', 'mncs-and-local-communities', ref('B', 6, '(c)(iv)'),
     H.q(8, 'Discuss two possible economic advantages to a local community', ' (30 marks)'), 'An advantage — any two',
     [H.traced(x) for x in ('Indirect employment.', 'Economic activity will increase.', 'May attract other foreign investment.',
                            'Communities may become more vibrant.')],
     2, 6, 'Two advantages, 6 marks each (3 + 3). The scheme names the advantages only.', stem=q6c, **B)

# Q7 ─ national income; the national income identity; growth
q7a = H.q(9, 'One method for calculating National Income, is the expenditure method.', ' (i)')
add('sb-q7-a-i', '3-0', 'national-income', ref('B', 7, '(a)(i)'),
    underlined(9, q7a, 'One method for calculating National Income, is the expenditure method.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('Income earned by the permanent residents of a country from current economic activity in one year.'), 5,
           'The explanation, 5 marks.')], **B)
add('sb-q7-a-ii', '3-0', 'methods-of-measuring-national-income', ref('B', 7, '(a)(ii)'),
    H.q(9, 'Name the two other methods used to calculate national income.', ' (iii)'), '2 x 5', 10,
    [point('r-income', H.traced('Income'), 5, 'The income method, 5 marks: the scheme’s ' + H.traced('Income and Output methods') + '.'),
     point('r-output', H.traced('Output methods'), 5, 'The output method, 5 marks.')], stem=q7a, **B)
pick('sb-q7-a-iii', '3-0', 'uses-of-national-income-statistics', ref('B', 7, '(a)(iii)'),
     H.q(9, 'State and explain two possible uses of national income statistics for a country.', ' (25 marks)'), 'A use — any two',
     H.split('Changes in the level of economic growth', '2 x 5 marks (3+2)',
             ['Changes in the level of economic growth', 'Changes in standard of living', 'Changes to employment levels',
              'International comparisons', 'Distribution of income', 'Contribution of government']),
     2, 5, 'Two uses, 5 marks each (3 + 2).', stem=q7a, **B)
q7b = H.q(9, 'Given National Income (Y) as:', ' (i)')
add('sb-q7-b-i', '3-0', 'the-national-income-identity', ref('B', 7, '(b)(i)'),
    H.q(9, 'State what each of the letters / symbols in the formula above represents.', ' (ii)'), '5 x 2', 10,
    [point(f'r-{k.lower()}', f'{k} — {H.traced(w)}', 2, f'{k}, 2 marks: ' + H.traced('2 marks per symbol') + '.')
     for k, w in zip('CIGXM', ('Consumption', 'Investment', 'Government Expenditure', 'Exports', 'Imports'))],
    stem=q7b, **B)
add('sb-q7-b-ii', '3-0', 'calculating-national-income', ref('B', 7, '(b)(ii)'),
    H.q(9, 'Calculate, using the figures provided, the level of National Income.', ' (20 marks)'), '10', 10,
    [point('r-1', H.traced('€2,000m + €700m + €500m + €200m - €150m = €3,250m'), 10, 'National income with its working, 10 marks.')],
    stem=q7b, **B)
q7c = H.q(9, '“The EU has predicted that Ireland’s GDP will grow by 4.5% in 2016.”', ' (i)')
add('sb-q7-c-i', '3-0', 'the-eu-and-gdp', ref('B', 7, '(c)(i)'), H.q(9, 'What do the letters EU and GDP stand for?', ' (ii)'), '4 + 6', 10,
    [point('r-eu', 'EU — ' + H.traced('European Union'), 4, 'The EU, 4 marks: the scheme’s 10marks (4+6), in the order printed.'),
     point('r-gdp', 'GDP — ' + H.traced('Gross Domestic Product'), 6, 'GDP, 6 marks.')], stem=q7c, **B)
pick('sb-q7-c-ii', '3-5', 'advantages-of-gdp-growth', ref('B', 7, '(c)(ii)'),
     H.q(9, 'State and explain two possible economic advantages of the above development', ' (iii)'), 'An advantage — any two',
     H.split('Increased employment\nA rise in GDP', '2 x 5 marks (3 + 2)',
             ['Increased employment', 'Improved government finances', 'Improved Balance of Payments', 'Improved standard of living',
              'Effects on Emigration', 'Investment opportunities.']),
     2, 5, 'Two advantages, 5 marks each (3 + 2).', stem=q7c, **B)
pick('sb-q7-c-iii', '3-5', 'costs-of-economic-growth', ref('B', 7, '(c)(iii)'),
     H.q(9, 'Outline two possible costs of economic growth.', ' (30 marks)'), 'A cost — any two',
     H.split('Pressure on housing market', '2 x 5 marks (3 + 2)',
             ['Pressure on housing market', 'Demand for wage increases.', 'Revised expectations by citizens', 'Increased demand for imports',
              'Inflationary pressures.', 'Inequitable distribution']),
     2, 5, 'Two costs, 5 marks each (3 + 2).', stem=q7c, **B)

# Q8 ─ the national debt; Metro North; the environment
q8a = H.q(9, 'Reducing Ireland’s national debt is one of the Irish government’s economic aims.', ' (i)')
add('sb-q8-a-i', '3-1', 'the-national-debt', ref('B', 8, '(a)(i)'),
    underlined(9, q8a, 'Reducing Ireland’s national debt is one of the Irish government’s economic aims.', ' (ii)'),
    '5', 5, [point('r-1', H.traced('National Debt: the total amount of government borrowing which is outstanding.'), 5, 'The explanation, 5 marks.')],
    **B)
pick('sb-q8-a-ii', '3-1', 'advantages-of-reducing-the-debt', ref('B', 8, '(a)(ii)'),
     H.q(9, 'State and explain two economic advantages of reducing Ireland’s national debt.', ' (iii)'), 'An advantage — any two',
     H.split('Lower annual interest repayments', '2 x 5 marks (3 + 2)',
             ['Lower annual interest repayments', 'Opportunity cost: increased funds', 'Reduced pressure on taxpayers',
              'Circular flow of income', 'Increased provision of public services', 'Improved international credit-rating.',
              'Improved confidence in the economy']),
     2, 5, 'Two advantages, 5 marks each (3 + 2).', stem=q8a, **B)
pick('sb-q8-a-iii', '3-1', 'other-economic-aims', ref('B', 8, '(a)(iii)'),
     H.q(9, 'State and explain two other economic aims of the Irish government.', ' (25 marks)'), 'An aim — any two',
     [H.traced(x) for x in ('Achieve full employment.', 'Sustainable government finances / reduce borrowing.', 'Achieve economic growth.',
                            'Broaden the tax base / lower income tax.', 'Provide efficient state services.',
                            'Infrastructural development / broadband access.', 'Promote balanced regional development.',
                            'Boost exports / improve competitiveness / attract investment / up-skill the workforce.',
                            'Sustainable economic development.')],
     2, 5, 'Two aims, 5 marks each (3 + 2). The scheme names the aims only.', stem=q8a, **B)
q8b = H.q(9, '‘Metro North, a high-speed rail from Dublin City centre', ' (i)')
add('sb-q8-b-i', '3-1', 'infrastructure', ref('B', 8, '(b)(i)'),
    underlined(9, q8b, '‘Metro North, a high-speed rail from Dublin City centre', ' (ii)'), '6', 6, [point('r-1', H.traced('goods /services which are essential for the smooth running of an economy'), 6,
                   'The explanation, 6 marks. The scheme also accepts its other two statements.',
                   accepts=[H.traced('goods /services which industry requires to function properly'),
                            H.traced('capital equipment used to supply publicly available services')])], **B)
advantages = [cc(x) for x in ('Less traffic congestion/reduced', 'Reduced pollution / Environmental', 'Shorter travelling times:',
                              'Enhanced local environment', 'Reduced oil consumption', 'Increased employment Jobs')]
disadvantages = [dehyphen(cc(x)) for x in ('Increase in land / property', 'Financial cost of the project', 'Opportunity cost of the project',
                                           'Disruption during construction', 'Loss of income for taxi', 'Population density may not')]
add('sb-q8-b-ii', '3-1', 'metro-north', ref('B', 8, '(b)(ii)'),
    H.q(9, 'State and explain one possible economic advantage and one possible economic disadvantage', ' (iii)'), '6 (3 + 3) + 6 (3 + 3)', 12,
    [by_heading('r-advantage', 'Economic advantages', advantages, 6, 'One advantage, 6 marks (3 + 3).'),
     by_heading('r-disadvantage', 'Economic disadvantages', disadvantages, 6, 'One disadvantage, 6 marks (3 + 3).')],
    kind='fixed', stem=q8b, **B)
infra = ('Broadband', 'Hospitals', 'Schools', 'Public Transport')
reasons = [cc(x) for x in ('Access is not uniform', 'As there is an overcrowding', 'With the increase in population there will',
                           'To reduce emissions the government should')]
add('sb-q8-b-iii', '3-1', 'investing-in-infrastructure', ref('B', 8, '(b)(iii)'),
    H.q(9, 'State one other example of infrastructure which should be invested in currently', ' (26 marks)'), '4 + 4', 8,
    [heading('r-example', 'An example of infrastructure — any one', [cc(x, whole=True) for x in infra], 4,
             H.traced('Any acceptable infrastructure: 4 marks.') + ' The scheme’s examples.'),
     heading('r-reason', 'A reason for your choice — any one', [f'{cc(x, whole=True)} — {r}' for x, r in zip(infra, reasons)], 4,
             H.traced('Reason for choice: 4 marks.'))],
    kind='fixed', stem=q8b, **B)
pick('sb-q8-c', '0-2', 'protecting-the-environment', ref('B', 8, '(c)'),
     H.q(9, 'Suggest one measure which any three of the following could take', ' (24 marks)'), 'A measure for a group — any three',
     side('Consumers', H.split('Shop local:', 'Businesses\nSponsorship',
                               ['Shop local:', 'Re-cycle / compost', 'Don’t litter', 'Use public transport', 'Switch to solar energy',
                                'Buy electric cars', 'Turn off lights']))
     + side('Businesses', H.split('Sponsorship for local communities', 'Local communities\nTidy',
                                  ['Sponsorship for local', 'Facilitate re-cycling', 'Reduce energy use', 'Introduce charges for plastic',
                                   'Reduce packaging']))
     + side('Local communities', H.split('Tidy Towns Competitions', 'Irish government\nEducation',
                                         ['Tidy Towns', 'Organise community re-cycling', 'Maintain / develop public amenity',
                                          'Facilitate local / farmer markets']))
     + side('Irish government', H.split('Education campaigns helps', '3 x 8 marks (4 + 4)',
                                        ['Education campaigns', 'Increase taxes on those practices', 'Provide / subsidise public transport',
                                         'Grants for solar energy'])),
     3, 8, 'One measure each for three of the four groups, 8 marks each (4 + 4).', **B)

if __name__ == '__main__':
    emit(cards)
