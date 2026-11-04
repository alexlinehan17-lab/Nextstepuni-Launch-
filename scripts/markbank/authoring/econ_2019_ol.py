#!/usr/bin/env python3
"""Economics 2019 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2019-ol-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2019
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The Ordinary scheme reprints each question above its
answer, so a slice always starts after the reprinted wording. The only prose
written here is guidance: tariffs, route labels and what a figure shows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import show_before_reveal  # noqa: E402
from econ_legacy_lib import Old, OldDeck  # noqa: E402
from econ_lib import anyN, block, emit, point  # noqa: E402

O = Old(2019, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2019, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
bl = O.bullets
A = dict(section='A')
SOL = 'economics-2019-OL-scheme-'
PAP = 'economics-2019-OL-paper-'


def pair(a, b):
    """Two cells of one table row, each traced, as one response: "Land — The ground ..."."""
    return f'{a} — {b}'


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ EU, ECB, WTO
add('sa-q1', '4-1', 'eu-ecb-and-wto', ref('A', 1),
    O.q(2, 'What do the following letters stand for?', ' (16 marks)'), '8 @ 2', 16,
    [point('r-eu', O.opt('EU European Union', 'ECB European Central'), 4,
           'EU, 4 marks: 2 for each word. The scheme prints 8 @ 2 over the eight words of the three names.'),
     point('r-ecb', O.opt('ECB European Central Bank', 'WTO World'), 6, 'ECB, 6 marks: 2 for each word.'),
     point('r-wto', O.opt('WTO World Trade Organisation', '2 The diagram below'), 6, 'WTO, 6 marks: 2 for each word.')],
    **A)

# Q2 ─ long-run equilibrium in perfect competition
q2_stem = O.q(2, 'The diagram below represents the long run equilibrium of a firm in Perfect Competition.', ' (i)')
q2_fig = PAP + 'p02-q2-question'   # the whole printed question: diagram, answer box and asks
add('sa-q2-i', '2-0', 'labelling-perfect-competition', ref('A', 2, '(i)'),
    O.q(2, 'Write in words the full label (not abbreviations)', ' 1 P 2'), '2 @ 6', 12,
    [point('r-1', O.traced(O.chunk('1 Marginal cost', ' 6')), 6, 'Line 1, 6 marks.'),
     point('r-2', O.traced(O.chunk('2 Average cost', ' 6')), 6, 'Line 2, 6 marks.')],
    stem=q2_stem, figure=q2_fig, **A)
add('sa-q2-ii', '2-0', 'equilibrium-in-perfect-competition', ref('A', 2, '(ii)'),
    O.q(2, 'On the above diagram show:', ' (16 marks)'), '2 @ 2', 4,
    [point(f'r-{i}', text, 2, '2 marks.') for i, text in enumerate(
        [O.opt('The price the firm will charge for its output (use label P1)\n', '• The output'),
         O.opt('The output the firm will produce in equilibrium (use label Q1).\nP 1', 'P 1')], 1)],
    stem=q2_stem, figure=SOL + 'p06-q2-diagram', **A)
show_before_reveal(cards[-1], None, q2_fig)

# Q3 ─ examples of the factors of production
add('sa-q3', '0-1', 'examples-of-factors-of-production', ref('A', 3),
    O.q(2, 'State examples of the four factors of production', ' (16 marks)'), '1 @ 8, 1 @ 4, 2 @ 2', 16,
    [anyN('r-1', 'An example for each factor', 16, 4, 8,
          [pair(O.cell(f, whole=True), O.cell(e)) for f, e in (
              ('Land', 'The ground on which the factory is built'), ('Labour', 'The workers who produce'),
              ('Capital', 'Machinery / factory building'), ('Enterprise', 'The owners / shareholders'))],
          'All four factors: the first correct example 8 marks, the next 4, the last two 2 each.',
          steps=[8, 4, 2, 2])],
    kind='fixed', **A)

# Q4 ─ economists
add('sa-q4', '0-0', 'economists-and-their-ideas', ref('A', 4),
    O.q(3, 'Name the economist associated with any three', ' (16 marks)'), '1 @ 8, 2 @ 4', 16,
    [anyN('r-1', 'An economist named — any three', 16, 3, 8,
          [pair(O.cell(i, whole=True), O.cell(e, whole=True)) for i, e in (
              ('Canons of Taxation', 'Adam Smith'), ('Theory of Population and Food Supply', 'Thomas Malthus'),
              ('Worker exploitation in a capitalist system', 'Karl Marx'), ('The multiplier', 'John Maynard Keynes'))],
          'Any three: the first 8 marks, the next two 4 each.', steps=[8, 4, 4])],
    kind='fixed', **A)

# Q5 ─ GNP
q5_stem = O.q(3, 'In 2017 the GNP of a country was €44 billion.', ' (i)')
add('sa-q5-i', '3-0', 'gnp-in-full', ref('A', 5, '(i)'),
    O.q(3, 'What do the letters GNP stand for?', ' (ii)'), '9 (3 x 3)', 9,
    [point('r-1', O.opt('Gross National Product.', '(ii) Calculate'), 9, '9 marks: 3 for each word.')],
    stem=q5_stem, **A)
add('sa-q5-ii', '3-0', 'percentage-increase-in-gnp', ref('A', 5, '(ii)'),
    O.q(3, 'Calculate the percentage increase in GNP', ' Answer:'), '7', 7,
    [point('r-1', O.traced(O.chunk('Answer: 5%', '\n').strip()), 7,
           'The answer with its working, 7 marks. The scheme sets the working as a fraction; the figure shows it as '
           'printed.')],
    stem=q5_stem, figure=SOL + 'p07-q5ii-working', **A)

# Q6 ─ injections and leakages
inj, leak = O.traced('INJECTIONS'), O.traced('LEAKAGES')
add('sa-q6', '3-0', 'injections-and-leakages', ref('A', 6),
    O.q(3, 'The items listed below are examples of injections', ' Taxation'), '1 @ 8, 3 @ 3', 17,
    [anyN('r-1', 'Each item placed', 17, 4, 8,
          [pair(inj, O.cell('INVESTMENT EXPENDITURE', whole=True)), pair(inj, O.cell('EXPORTS', whole=True)),
           pair(leak, O.cell('TAXATION', whole=True)), pair(leak, O.cell('IMPORTS', whole=True))],
          'All four items: the first correct placement 8 marks, the other three 3 each.', steps=[8, 3, 3, 3])],
    kind='fixed', figure=SOL + 'p08-q6-table', **A)
show_before_reveal(cards[-1], None, PAP + 'p03-q6-question')

# Q7 ─ USC
q7_stem = O.q(4, 'The 4.75% rate of USC was reduced to 4.5% in Budget 2019.', ' (i)')
add('sa-q7-i', '3-1', 'usc-in-full', ref('A', 7, '(i)'),
    O.q(4, 'What do the letters USC stand for?', ' ___'), '8 (4 + 2 + 2)', 8,
    [point('r-1', O.opt('Universal Social Charge', '(ii) Outline one economic benefit'), 8, '8 marks (4 + 2 + 2).')],
    stem=q7_stem, **A)
pick('sa-q7-ii', '3-1', 'benefit-of-a-usc-cut', ref('A', 7, '(ii)'),
     O.q(4, 'Outline one economic benefit for workers', ' ___'),
     'A benefit for workers — any one',
     O.split('Increased disposable income so workers', '8 (a) Explain what',
             ['Increased disposable income', 'Increased productivity', 'Some workers may be able to save',
              'Some workers may use the extra income']),
     1, 9, 'One benefit, 9 marks.', stem=q7_stem, **A)

# Q8 ─ scarcity and waste
add('sa-q8-a', '0-1', 'scarcity-of-resources', ref('A', 8, '(a)'),
    O.q(4, 'Explain what is meant in economics by the term scarcity of resources.', ' ___'), '7', 7,
    [point('r-1', O.opt('Not enough factors of production and limitless wants.', 'Quantity of goods'), 7,
           'The explanation, 7 marks. The scheme also accepts its second statement.',
           accepts=[O.opt('Quantity of goods & services people like to have exceeds', '(b) Outline two')])], **A)
pick('sa-q8-b', '0-2', 'ways-citizens-waste-resources', ref('A', 8, '(b)'),
     O.q(4, 'Outline two examples of ways Irish citizens waste resources.', ' (i)'),
     'A way resources are wasted — any two',
     O.split('(i) Buying items they may not need', '8 | P a g e',
             ['Buying items', 'Not re-cycling', 'Using private transport', 'Leaving electrical items']),
     2, 5, 'Two examples, 5 marks each.', **A)

# Q9 ─ fixed and variable costs (one ladder across (a) and (b))
add('sa-q9', '1-5', 'fixed-and-variable-costs', ref('A', 9),
    ' '.join([O.q(4, '(a) Explain what is meant by fixed costs', ' Fixed Costs:'),
              O.q(4, '(b) Explain what is meant by variable costs', ' Variable Costs:')]),
    '1 @ 5, 3 @ 4', 17,
    [anyN('r-1', 'Each definition and example', 17, 4, 5,
          [O.opt('Fixed Costs: costs which do not change', 'Example: Rent'),
           O.opt('Example: Rent of pizza firm', '(b) Explain'),
           O.opt('Variable Costs: costs which change', 'Example: Flour'),
           O.opt('Example: Flour/ingredients to make the pizza', '9 | P a g e')],
          'The four elements across (a) and (b): the first correct one 5 marks, the other three 4 each. The '
          'scheme prices them on one ladder, not by part.', steps=[5, 4, 4, 4])],
    kind='fixed', stem=O.q(4, 'A pizza delivery firm must cover', ' (a)'), **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ imperfect competition; household waste collection
q1a = O.q(5, 'The diagram below represents the long run equilibrium of a firm in Imperfect Competition.', ' P AC')
add('sb-q1-a-i', '2-0', 'labels-of-imperfect-competition', ref('B', 1, '(a)(i)'),
    ' '.join([O.q(5, 'Write out in full what each of the five labels circled above represents.', ' Copy'),
              O.q(5, 'Copy the diagram into your answer book.', ' (ii)')]), '5 @ 4', 20,
    [point(f'r-{label.split()[0].lower()}', O.opt(label, end), 4, '4 marks.') for label, end in (
        ('P Price', 'Q Quantity'), ('Q Quantity', 'AC Average'), ('AC Average Cost', 'AR Average'),
        ('AR Average Revenue', 'MR Marginal'), ('MR Marginal Revenue', 'Copy the diagram'))],
    stem=q1a, figure=PAP + 'p05-q1a-diagram', **B)
add('sb-q1-a-ii', '2-0', 'equilibrium-of-an-imperfectly-competitive-firm', ref('B', 1, '(a)(ii)'),
    O.q(5, 'Equilibrium occurs at point X on the diagram.', ' (30 marks)'), '5 + 5', 10,
    [point('r-price', O.opt('The price the firm will charge for its output (use label P1).', '• The output'), 5,
           'P1, 5 marks. The completed diagram is in the figure.'),
     point('r-output', O.traced(O.chunk('The output the firm will produce in equilibrium (use label Q1).', ' (30 marks)', occ=1)), 5,
           'Q1, 5 marks.')],
    stem=q1a, figure=SOL + 'p10-q1a-diagram', **B)
show_before_reveal(cards[-1], None, PAP + 'p05-q1a-question')
q1b = O.q(5, 'Free entry and exit is one of the characteristics', ' (i)')
add('sb-q1-b-i', '2-0', 'free-entry-and-exit', ref('B', 1, '(b)(i)'),
    O.q(5, 'Explain the term free entry and exit.', ' (ii)'), '1 @ 9', 9,
    [point('r-1', O.opt('Free entry and exit exists in the industry.', '(ii) State two other'), 9,
           'The explanation, 9 marks.')], stem=q1b, **B)
pick('sb-q1-b-ii', '2-0', 'characteristics-of-imperfect-competition', ref('B', 1, '(b)(ii)–(iii)'),
     ' '.join([O.q(5, 'State two other characteristics of Imperfect Competition.', ' (iii)'),
               O.q(5, 'Write brief notes on each of these characteristics.', ' (21 marks)')]),
     'A characteristic with its note — any two',
     O.split('Many buyers ⟨2 @ 6⟩', '11 | P a g e',
             ['Many buyers', 'Many sellers', 'Differentiated products', 'Almost Perfect knowledge',
              'Each firm tries to maximise profits']),
     2, 6, 'Two characteristics, each with its note, 6 marks each. The scheme prices (ii) and (iii) together.',
     stem=q1b, **B)
add('sb-q1-c', '2-0', 'more-firms-in-waste-collection', ref('B', 1, '(c)'),
    O.q(5, 'Outline two possible economic advantages and one possible economic disadvantage', ' (24 marks)'),
    '2 @ 9, 1 @ 6', 24,
    [anyN('r-advantage', 'An advantage — any two', 18, 2, 9,
          O.split('More competitive prices', 'Possible disadvantages of increased entry',
                  ['More competitive prices', 'Greater range/choice of services', 'Improved quality of services',
                   'Increased efficiency by firms']),
          'Two advantages, 9 marks each.'),
     anyN('r-disadvantage', 'A disadvantage — any one', 6, 1, 6,
          O.split('Duplication of services', '12 | P a g e',
                  ['Duplication of services', 'Some customers may not be provided', 'Price comparisons can be difficult',
                   'Reduced market share']),
          'One disadvantage, 6 marks.')],
    kind='fixed', stem=O.q(5, 'An increasing number of firms, such as Greenstar', ' Outline two'), **B)

# Q2 ─ demand and supply for sandwiches; electric vehicles
q2a = ' '.join([O.q(6, 'The information below represents the quantity demanded', ' Price Quantity'),
                O.q(6, 'Using the above data and one diagram', ' (a)')])
labels = O.opt('Labels: P, Q, D/C and S/C = 4 marks', 'P1 and Q1')
q2a_cards = (
    ('sb-q2-a-i', 'drawing-the-demand-curve', '(a)(i)', O.q(6, 'Draw and label the demand curve for sandwiches.', ' (ii)'),
     O.opt('D/C: 5 points at 2 marks each = 10 marks', 'S/C: 5 points'), 10, 1,
     'The D/C label, 1 mark (the scheme’s summary prints 11 (5 @ 2) + 1).'),
    ('sb-q2-a-ii', 'drawing-the-supply-curve', '(a)(ii)', O.q(6, 'Draw and label the supply curve for sandwiches.', ' (iii)'),
     O.opt('S/C: 5 points at 2 marks each = 10 marks', 'Labels: P'), 10, 1,
     'The S/C label, 1 mark (the scheme’s summary prints 11 (5 @ 2) + 1).'),
    ('sb-q2-a-iii', 'equilibrium-price-and-quantity', '(a)(iii)', O.q(6, 'Show on your diagram: • The equilibrium price', ' (30 marks)'),
     O.opt('P1 and Q1 : 2 x 3 marks each = 6 marks', '13 | P a g e'), 6, 2,
     'The P and Q axis labels, 1 mark each (the scheme’s summary prints 6 (3 + 3) + 1 + 1).'))
for cid, concept, parts, ask, run, marks, label_marks, label_note in q2a_cards:
    add(cid, '1-0', concept, ref('B', 2, parts), ask, f'{marks} + {label_marks}', marks + label_marks,
        [point('r-1', run, marks, f'{marks} marks. The completed graph is in the figure.'),
         point('r-labels', labels, label_marks, label_note)],
        stem=q2a, figure=SOL + 'p13-q2a-graph', **B)
    show_before_reveal(cards[-1], None, PAP + 'p06-q2a-question')
q2b = ' '.join([O.q(6, 'The demand curve for sandwiches or the supply curve', ' In relation'),
                O.q(6, 'In relation to each of the above situations', ' (i)')])
cost, visit = O.cell('Increase in the cost of ingredients for sandwiches'), O.cell('An additional 200 students visiting')
for cid, concept, parts, ask, cells, per in (
        ('sb-q2-b-i', 'which-curve-shifts', '(b)(i)', O.q(6, 'State whether the demand curve or supply curve will shift.', ' (ii)'),
         ('Supply Curve', 'Demand Curve'), 4),
        ('sb-q2-b-ii', 'which-way-the-curve-shifts', '(b)(ii)', O.q(6, 'State whether the curve you mention will shift', ' (iii)'),
         ('Left', 'Right'), 4),
        ('sb-q2-b-iii', 'why-the-curve-shifts', '(b)(iii)', O.q(6, 'Explain why the curve has shifted in the direction', ' (20 marks)'),
         ('Costs of production have increased', 'The additional students will'), 2)):
    a, b = cells
    add(cid, '1-0', concept, ref('B', 2, parts), ask, f'{per} + {per}', 2 * per,
        [point('r-costs', pair(cost, O.cell(a, whole=len(a.split()) <= 2)), per, f'The rise in ingredient costs, {per} marks.'),
         point('r-students', pair(visit, O.cell(b, whole=len(b.split()) <= 2)), per, f'The extra students, {per} marks.')],
        stem=q2b, **B)
q2c = O.q(6, 'The Government extended the electric vehicle (EV) purchase grant', ' (i)')
pick('sb-q2-c-i', '1-3', 'why-extend-the-ev-grant', ref('B', 2, '(c)(i)'),
     O.q(6, 'Outline one economic reason why the government took the above action.', ' (ii)'),
     'A reason for the grant — any one',
     O.split('CO2 emissions/cleaner environment', '(ii) State and explain one economic effect',
             ['CO2 emissions', 'Reduced dependence on fossil fuels', 'EU Climate change targets', 'Reduced EU fines']),
     1, 6, 'One reason, 6 marks (4 + 2).', stem=q2c, **B)
add('sb-q2-c-ii', '1-1', 'ev-grant-and-demand', ref('B', 2, '(c)(ii)'),
    O.q(6, 'State and explain one economic effect the above action may have', ' (iii)'), '7 (5 + 2)', 7,
    [point('r-1', O.opt('Demand should increase.', '(iii) State and explain two other actions'), 7,
           'The effect and its explanation, 7 marks (5 + 2).')], stem=q2c, **B)
pick('sb-q2-c-iii', '1-3', 'encouraging-ev-purchases', ref('B', 2, '(c)(iii)'),
     O.q(6, 'State and explain two other actions the Irish government could take', ' (25 marks)'),
     'An action to encourage EV purchases — any two',
     O.split('Reduce motor tax/VRT', '15 | P a g e',
             ['Reduce motor tax/VRT', 'Plug-in points', 'Allow electric vehicles to use bus lanes', 'Free parking',
              'Remove / reduce motorway tolls', 'Reduce benefit-in-kind taxes']),
     2, 6, 'Two actions, 6 marks each (4 + 2).', stem=q2c, **B)

# Q3 ─ the labour market
add('sb-q3-a', '2-1', 'labour-market-terms', ref('B', 3, '(a)'),
    O.q(7, 'Explain any three of the following terms: • National minimum wage rate', ' (21 marks)'), '1 @ 11, 2 @ 5', 21,
    [anyN('r-1', 'A term explained — any three', 21, 3, 11,
          O.split('National minimum wage rate\nThe lowest wage', '(b) Labour has a major role',
                  ['National minimum wage rate', 'Occupational mobility of labour', 'Benefit -in-kind',
                   'Public sector employment']),
          'Any three: the first 11 marks, the next two 5 each.', steps=[11, 5, 5])],
    kind='fixed', **B)
q3b = O.q(7, 'Labour has a major role to play in helping an economy develop.', ' (i)')
add('sb-q3-b-i', '2-1', 'labour-as-a-factor', ref('B', 3, '(b)(i)'),
    O.q(7, 'Explain the term underlined above.', ' (ii)'), '6', 6,
    [point('r-1', O.opt('The human effort involved in producing', '(ii) Outline two reasons'), 6, 'The explanation, 6 marks.')],
    stem=q3b, **B)
pick('sb-q3-b-ii', '2-1', 'why-employers-demand-labour', ref('B', 3, '(b)(ii)'),
     O.q(7, 'Outline two reasons why employers might demand additional labour.', ' (iii)'),
     'A reason employers demand more labour — any two',
     O.split('Demand for output / product', '(iii) State and explain two factors',
             ['Demand for output', 'Government policies', 'Reduction in the national minimum wage',
              'Labour may be cheaper than technology']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q3b, **B)
pick('sb-q3-b-iii', '2-1', 'raising-labour-force-participation', ref('B', 3, '(b)(iii)'),
     O.q(7, 'State and explain two factors which may encourage more people to participate', ' (30 marks)'),
     'A factor encouraging participation — any two',
     O.split('Increased wage rates may make it more worthwhile', '17 | P a g e',
             ['Increased wage rates', 'Reduced state benefits', 'Lower income tax / USC', 'More flexible working hours',
              'Cheaper child minding services', 'Retirees re-joining the workforce', 'Changed personal circumstances',
              'Provide incentives for up-skilling workers']),
     2, 6, 'Two factors, 6 marks each (3 + 3).', stem=q3b, **B)
q3c = O.q(7, 'The Irish economy is currently experiencing skills shortages', ' (i)')
add('sb-q3-c-i', '2-1', 'effects-of-skills-shortages', ref('B', 3, '(c)(i)'),
    O.q(7, 'Discuss one economic effect of skills shortages for each of the following:', ' (ii)'), '2 @ 6 (4 + 2)', 12,
    [heading('r-firms', O.traced(O.chunk('Firms:', '\n').strip()).rstrip(':') + ' — any one',
             O.split('May have to reduce output / reduced productivity', 'The Irish economy:',
                     ['May have to reduce output', 'Firms may lose customers', 'Firms may lose market share',
                      'Wage rate may be forced upwards', 'Firms may have to source labour']),
             6, 'One effect for firms, 6 marks (4 + 2).'),
     heading('r-economy', O.traced(O.chunk('The Irish economy:', '\n').strip()).rstrip(':') + ' — any one',
             O.split('Foreign companies may not locate here', '(ii) Two measures firms',
                     ['Foreign companies may not locate', 'Increased immigration as those', 'Pressure in the provision',
                      'Increased demand for courses', 'Reduction in economic growth']),
             6, 'One effect for the economy, 6 marks (4 + 2).')],
    kind='fixed', stem=q3c, **B)
pick('sb-q3-c-ii', '2-1', 'firms-raising-the-supply-of-skills', ref('B', 3, '(c)(ii)'),
     O.q(7, 'State and explain two measures firms could take to increase the supply', ' (24 marks)'),
     'A measure firms could take — any two',
     O.split('Upskill the existing workforce', '18 | P a g e',
             ['Upskill the existing workforce', 'Increase wage rates', 'Internships', 'Information campaign',
              'Providing/Offering subsidised accommodation', 'Recognition of foreign qualifications']),
     2, 6, 'Two measures, 6 marks each (4 + 2).', stem=q3c, **B)

# Q4 ─ trade; the Rainy Day Fund
add('sb-q4-a', '4-2', 'trade-terms', ref('B', 4, '(a)'),
    O.q(7, 'Explain any three of the following terms: • Open economy', ' (21 marks)'), '1 @ 11, 2 @ 5', 21,
    [anyN('r-1', 'A term explained — any three', 21, 3, 11,
          O.split('Open economy\nOne that engages', '(b) Irish rugby supporters',
                  ['Open economy', 'Exchange Rate', 'Economic growth', 'Tariffs']),
          'Any three: the first 11 marks, the next two 5 each.', steps=[11, 5, 5])],
    kind='fixed', **B)
q4b = O.q(7, 'Irish rugby supporters will travel to Japan', ' (i)')
add('sb-q4-b-i', '4-2', 'an-invisible-import', ref('B', 4, '(b)(i)'),
    O.q(7, 'Is this an example of an invisible import or an invisible export', ' (ii)'), '4 + 3', 7,
    [point('r-answer', O.traced(O.chunk('This is an example of an invisible import', ' as the money')), 4,
           'The answer, 4 marks: the scheme prints 4 beside it and 3 beside the reason.'),
     point('r-reason', O.opt('as the money is leaving and going into the', '(ii) Explain what a surplus'), 3,
           'The reason, 3 marks.')], stem=q4b, **B)
add('sb-q4-b-ii', '4-2', 'balance-of-trade-surplus', ref('B', 4, '(b)(ii)'),
    O.q(7, 'Explain what a surplus in Ireland’s Balance of Trade means.', ' (iii)'), '9', 9,
    [point('r-1', O.opt('The amount of goods exported exceeds', '19 | P a g e'), 9, 'The explanation, 9 marks.')],
    stem=q4b, **B)
pick('sb-q4-b-iii', '4-2', 'advantages-of-international-trade', ref('B', 4, '(b)(iii)'),
     O.q(7, 'Outline two economic advantages of international trade for the Irish economy.', ' (30 marks)'),
     'An advantage of international trade — any two',
     O.split('Employment creation', '20 | P a g e',
             ['Employment creation', 'Increased GNP / Economic growth', 'Increased sales / profits', 'Attract investment',
              'Government finances', 'More choice for consumers', 'Raw materials unavailable in Ireland']),
     2, 7, 'Two advantages, 7 marks each (4 + 3).', stem=q4b, **B)
q4c = O.q(7, 'The government is planning to contribute €500m', ' (i)')
add('sb-q4-c-i', '0-1', 'opportunity-cost', ref('B', 4, '(c)(i)'),
    O.q(7, 'Explain the term opportunity cost.', ' (ii)'), '6', 6,
    [point('r-1', O.traced(O.chunk('The cost of foregone alternatives.', '\n').strip()), 6,
           'The explanation, 6 marks. The scheme also accepts its second statement.',
           accepts=[O.opt('The cost of passing up the next best choice', '(ii) In your opinion')])],
    stem=q4c, **B)
q4cii = O.q(7, 'In your opinion is this Rainy Day Fund a good idea?', ' (iii)')
pick('sb-q4-c-ii-yes', '3-1', 'the-rainy-day-fund', ref('B', 4, '(c)(ii)', 'yes'),
     f'{q4cii} Justify the choice: YES.', 'A reason for answering YES — any one',
     O.split('It will provide a fund to the government', 'NO.', ['It will provide a fund', 'If there was an economic crash']),
     1, 6, 'One developed reason, 6 marks. The scheme credits YES and NO, each with its own content.', stem=q4c, **B)
add('sb-q4-c-ii-no', '3-1', 'the-rainy-day-fund', ref('B', 4, '(c)(ii)', 'no'),
    f'{q4cii} Justify the choice: NO.', '6', 6,
    [point('r-1', O.opt('The funds could be used in the economy now', '(iii) Suggest two uses'), 6,
           'The reason, 6 marks. The scheme credits YES and NO, each with its own content.')], stem=q4c, **B)
pick('sb-q4-c-iii', '3-1', 'other-uses-for-the-500m', ref('B', 4, '(c)(iii)'),
     O.q(7, 'Suggest two uses for the €500m', ' (24 marks)'),
     'A use for the €500m, with its reason — any two',
     O.split('Social Housing', '21 | P a g e',
             ['Social Housing', 'Building schools / hospitals', 'Provision of broadband', 'Improvement in public transport',
              'Improved public services', 'Increase the pension reserve fund']),
     2, 6, 'Two uses, 6 marks each (4 + 2).', stem=q4c, **B)

# Q5 ─ non-cash payment; interest rates; post office closures
groups = (('Students\nMore convenient', 'More convenient', 'University\nLess security',
           ['More convenient', 'Safer', 'Digital record']),
          ('University\nLess security', 'Less security risks', 'Banks\nTime saving',
           ['Less security risks', 'Lower insurance premiums', 'Convenience/efficiency']),
          ('Banks\nTime saving', 'Time saving', '22 | P a g e',
           ['Time saving', 'Development of new', 'Reduction in staff numbers', 'Reduced risk of robberies']))
add('sb-q5-a', '3-4', 'non-cash-payments-on-campus', ref('B', 5, '(a)'),
    O.q(8, 'Outline one advantage of a non cash‐based method of payment', ' (21 marks)'), '3 @ 7 (4 + 3)', 21,
    [heading(f'r-{i}', O.traced(O.chunk(label, '\n')) + ' — any one', O.split(start, end, firsts), 7,
             'One advantage for this group, 7 marks (4 + 3).')
     for i, (label, start, end, firsts) in enumerate(groups, 1)],
    kind='fixed', stem=O.q(8, 'Maynooth University issues a campus smartcard', ' Outline one'), **B)
groups = (('Households\nBorrowing', 'Borrowing discouraged', 'Firms\nCosts of production',
           ['Borrowing discouraged', 'Savings encouraged']),
          ('Firms\nCosts of production', 'Costs of production / prices', 'The Irish Government\nCost of Servicing',
           ['Costs of production / prices', 'Decreased competitiveness', 'Loss of jobs']),
          ('The Irish Government\nCost of Servicing', 'Cost of Servicing the National Debt', '23 | P a g e',
           ['Cost of Servicing', 'Investment and impact on economic growth', 'Taxation revenues']))
add('sb-q5-b', '3-3', 'effects-of-higher-interest-rates', ref('B', 5, '(b)'),
    O.q(8, 'Explain how an increase in interest rates is likely to affect each of the following:', ' (24 marks)'),
    '3 @ 8 (4 + 4)', 24,
    [heading(f'r-{i}', O.traced(O.chunk(label, '\n')) + ' — any one', O.split(start, end, firsts), 8,
             'One effect for this group, 8 marks (4 + 4).')
     for i, (label, start, end, firsts) in enumerate(groups, 1)],
    kind='fixed', stem=O.q(8, 'Some economists are predicting an increase in interest rates', ' Explain how'), **B)
q5c = O.q(8, 'One hundred and sixty one post offices are set to close', ' (Source')
pick('sb-q5-c-i', '1-5', 'why-post-offices-close', ref('B', 5, '(c)(i)'),
     O.q(8, 'State and explain two possible reasons for the closure', ' (ii)'),
     'A reason for the closures — any two',
     [pair(O.cell('Decrease costs', whole=True), O.cell('An Post wants to reduce')),
      pair(O.cell('Decrease in the use of services', whole=True), O.cell('In some areas consumers are using'))],
     2, 6, 'Two reasons, each stated and explained, 6 marks each (3 + 3).', stem=q5c, **B)
add('sb-q5-c-ii', '3-2', 'effects-of-post-office-closures', ref('B', 5, '(c)(ii)'),
    O.q(8, 'Outline one economic effect which the closure of the post offices may have', ' (30 marks)'),
    '3 @ 6 (3 + 3)', 18,
    [heading('r-customers', O.cell('Customers', whole=True) + ' — any one',
             [O.cell('Loss of service/inconvenience The customer')], 6, 'One effect for customers, 6 marks (3 + 3).'),
     heading('r-employees', O.cell('Employees', whole=True) + ' — any one',
             O.cut_cell('Loss of jobs Some employees', ['Loss of jobs', 'Re-location']), 6,
             'One effect for employees, 6 marks (3 + 3).'),
     heading('r-community', O.cell('The Local community', whole=True) + ' — any one',
             O.cut_cell('Reduced economic activity/rural decline Less', ['Reduced economic activity', 'Job losses']), 6,
             'One effect for the local community, 6 marks (3 + 3).')],
    kind='fixed', stem=q5c, **B)

# Q6 ─ taxation and Budget 2019
q6 = O.q(8, 'Raising revenue from taxation and reducing tax evasion', ' (a)')
add('sb-q6-a-i', '3-1', 'tax-evasion', ref('B', 6, '(a)(i)'),
    O.q(8, 'Explain the term underlined above and state one example of tax evasion.', ' (ii)'), '5 + 2', 7,
    [point('r-explanation', O.opt('Making false tax returns', 'Examples'), 5, 'The explanation, 5 marks.'),
     anyN('r-example', 'An example — any one', 2, 1, 2,
          [O.opt('A teacher giving grinds', '2. Paying'), O.opt('Paying for a good/service in cash', '(ii) State and explain')],
          'One example, 2 marks.')],
    kind='fixed', stem=q6, **B)
pick('sb-q6-a-ii', '3-1', 'why-taxation-is-essential', ref('B', 6, '(a)(ii)'),
     O.q(8, 'State and explain two economic reasons why taxation is essential', ' (21 marks)'),
     'A reason taxation is essential — any two',
     O.split('Provides revenue for the government', '25 | P a g e',
             ['Provides revenue for the government', 'Provide public services', 'Help to re-distribute wealth',
              'Promote industry', 'Achieve Social Objective', 'Achieve a favourable balance of payments']),
     2, 7, 'Two reasons, 7 marks each (3 + 4).', stem=q6, **B)
q6b = O.q(8, 'In Budget 2019, the Value Added Tax (VAT) rate', ' (i)')
add('sb-q6-b-i', '3-1', 'value-added-tax', ref('B', 6, '(b)(i)'),
    O.q(8, 'Explain the term Value Added Tax.', ' (ii)'), '8', 8,
    [point('r-1', O.opt('This is a tax on goods and services.', '(ii) It is an indirect tax.'), 8, 'The explanation, 8 marks.')],
    stem=q6b, **B)
add('sb-q6-b-ii', '3-1', 'vat-is-an-indirect-tax', ref('B', 6, '(b)(ii)'),
    O.q(8, 'Is VAT an example of a direct tax or an indirect tax?', ' (iii)'), '3 + 3', 6,
    [point('r-answer', O.opt('It is an indirect tax.', 'It is not a tax on income'), 3, 'The answer, 3 marks.'),
     point('r-reason', O.opt('It is not a tax on income or wealth', '(iii) Two possible'), 3, 'The explanation, 3 marks.')],
    stem=q6b, **B)
pick('sb-q6-b-iii', '3-1', 'effects-of-the-hospitality-vat-rise', ref('B', 6, '(b)(iii)'),
     O.q(8, 'Outline two possible economic effects on the Irish economy of this increase', ' (30 marks)'),
     'An effect of the VAT increase — any two',
     O.split('Higher prices\nFirms may increase', '26 | P a g e',
             ['Higher prices', 'Loss of jobs/unemployment increase', 'Discourages (may alter spending)', 'Tax implications',
              'Achieve greater efficiencies', 'Rural hotels adversely affected']),
     2, 8, 'Two effects, 8 marks each (4 + 4).', stem=q6b, **B)
# Each measure's own heading on the answer side (the question is reprinted above it).
# The first is printed there in lower case ("increase in social welfare ..."), so
# it is named as the scheme's reprinted question bullet prints it.
measures = [O.traced('Increase in social welfare payments of €5 per week')] + [
    O.opt(a, 'Economic argument in favour', occ) for a, occ in (
        ('Increase of 50c in the price of a packet of 20 cigarettes\nEconomic', None),
        ('Introduction of 2 extra weeks paid parental leave to every parent of a child under one\nyear', 1))]
favour = [(0, 'Better standard of living More income'), (0, 'Fairer distribution of Income The extra payment'),
          (1, 'Government revenue This increase'), (1, 'Reduce consumption / personal health Consumption'),
          (1, 'Social benefit A healthier society'), (1, 'Reduced healthcare costs As less people'),
          (1, 'Opportunity cost The money saved'), (2, 'Some cost savings Reduced childcare'),
          (2, 'Social benefit Workers may be'), (2, 'Increase in population May')]
against = [(0, 'Increased Government expenditure / borrowing'), (0, 'Opportunity cost The money could be put'),
           (0, 'Possibility of increased taxation With the increase'), (0, 'Disincentive to work An increase'),
           (1, 'Standard of living Disposable incomes'), (1, 'Inflation Price of tobacco'), (1, 'Inequitable / regressive'),
           (1, 'Smuggling/black (shadow) economy'), (1, 'Tax revenue If consumption falls'),
           (2, 'Increased government expenditure Its provision'), (2, 'Opportunity cost The money used'),
           (2, 'Labour shortages Difficulty')]
add('sb-q6-c', '3-1', 'arguments-on-budget-2019-measures', ref('B', 6, '(c)'),
    O.q(8, 'Outline one economic argument in favour of and one economic argument against any two', ' (24 marks)'),
    '4 @ 6 (3 + 3)', 24,
    [anyN('r-favour', 'An argument in favour — one for each of your two measures', 12, 2, 6,
          [pair(measures[m], O.cell(c, cells_only=True)) for m, c in favour],
          'One argument in favour of each measure you choose, 6 marks each (3 + 3). Each option names its measure.'),
     anyN('r-against', 'An argument against — one for each of your two measures', 12, 2, 6,
          [pair(measures[m], O.cell(c, cells_only=True)) for m, c in against],
          'One argument against each of the same two measures, 6 marks each (3 + 3).')],
    kind='fixed', **B)

# Q7 ─ national income, multinationals, the multiplier
q7a = O.q(9, 'The CSO calculates the level of National Income', ' (i)')
add('sb-q7-a-i', '3-0', 'cso-in-full', ref('B', 7, '(a)(i)'),
    O.q(9, 'What do the letters CSO stand for?', ' (ii)'), '9 (3 x 3)', 9,
    [point('r-1', O.opt('Central Statistics Office', '(ii) Explain any one'), 9, '9 marks: 3 for each word.')],
    stem=q7a, **B)
pick('sb-q7-a-ii', '3-0', 'a-method-of-measuring-national-income', ref('B', 7, '(a)(ii)'),
     O.q(9, 'Explain any one of the three methods used to calculate national income.', ' (iii)'),
     'A method explained — any one',
     O.split('Income method\nThis method adds up all the income', '(iii) Two reasons why',
             ['Income method', 'Output method', 'Expenditure method']),
     1, 5, 'One method, 5 marks.', stem=q7a, **B)
pick('sb-q7-a-iii', '3-0', 'why-measure-national-income', ref('B', 7, '(a)(iii)'),
     O.q(9, 'State and explain two reasons why it is important to calculate', ' (24 marks)'),
     'A reason to measure national income — any two',
     O.split('Indicates changes in the level of economic growth', '29 | P a g e',
             ['Indicates changes in the level', 'To help formulate government economic policy',
              'It facilitates International comparisons', 'EU Budget contributions']),
     2, 5, 'Two reasons, 5 marks each (3 + 2).', stem=q7a, **B)
q7b = O.q(9, 'One possible reason why multinational companies (MNCs)', ' (i)')
add('sb-q7-b-i', '4-1', 'mncs-and-corporation-tax', ref('B', 7, '(b)(i)'),
    O.q(9, 'Explain the terms multinational company and corporation tax.', ' (ii)'), '2 @ 6', 12,
    [point('r-mnc', O.opt('Multinational company\nHas offices', 'Corporation tax\nThis is a tax'), 6,
           'A multinational company, 6 marks.'),
     point('r-tax', O.opt('Corporation tax\nThis is a tax on the profits', '(ii) Discuss two other'), 6,
           'Corporation tax, 6 marks.')], stem=q7b, **B)
pick('sb-q7-b-ii', '4-1', 'why-mncs-locate-in-ireland', ref('B', 7, '(b)(ii)'),
     O.q(9, 'Discuss two other economic reasons why MNCs may locate in Ireland.', ' (iii)'),
     'A reason MNCs locate in Ireland — any two',
     O.split('Skilled workforce', '30 | P a g e',
             ['Skilled workforce', 'Government incentives', 'Membership of EU', 'Improved infrastructure']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q7b, **B)
pick('sb-q7-b-iii', '4-1', 'why-mncs-may-not-locate-in-ireland', ref('B', 7, '(b)(iii)'),
     O.q(9, 'Discuss one economic reason why some MNCs may not locate in Ireland.', ' (30 marks)'),
     'A reason MNCs may not locate here — any one',
     O.split('Lower wage costs elsewhere', '31 | P a g e',
             ['Lower wage costs elsewhere', 'Lower costs of production', 'Lack of reasonably priced accommodation',
              'Skilled Labour shortages', 'Restrictive regulatory framework', 'Emerging economies in a growth phase',
              'Lack of advanced technologies']),
     1, 6, 'One reason, 6 marks (3 + 3).', stem=q7b, **B)
q7c = O.q(9, 'The Multiplier formula for an open economy is:', ' 1 MPS')
q7c_fig = PAP + 'p09-q7c-formula'
add('sb-q7-c-i', '3-0', 'mps-and-mpm', ref('B', 7, '(c)(i)'),
    O.q(9, 'Explain each of the terms MPS and MPM.', ' Assume'), '2 @ 5', 10,
    [point('r-mps', O.opt('MPS (The marginal propensity to save)', 'MPM (The marginal'), 5, 'MPS, 5 marks.'),
     point('r-mpm', O.opt('MPM (The marginal propensity to import)', '(ii) Calculate'), 5, 'MPM, 5 marks.')],
    stem=q7c, figure=q7c_fig, **B)
add('sb-q7-c-ii', '3-0', 'calculating-the-open-economy-multiplier', ref('B', 7, '(c)(ii)'),
    ' '.join([O.q(9, 'Assume that MPS is 0.1 and MPM is 0.4.', ' (ii)'),
              O.q(9, 'Calculate, using the above formula, the size of the multiplier.', ' (iii)')]), '8', 8,
    # The printed answer is a line of its own ("2"), which the loader drops with
    # every bare-number line; it is cut from the raw scheme file instead.
    [point('r-1', O.traced(block(open('examiner-reports/economics/schemes/2019-ol.md').read(),
                                 '0.1 + 0.4\n2\n', '(iii) Explain the meaning').split()[-1]), 8,
           'The multiplier, 8 marks. The scheme sets the working as a fraction; the figure shows it as printed.')],
    stem=q7c, figure=SOL + 'p32-q7cii-working', **B)
show_before_reveal(cards[-1], None, PAP + 'p09-q7c-question')
add('sb-q7-c-iii', '3-0', 'meaning-of-the-multiplier', ref('B', 7, '(c)(iii)'),
    O.q(9, 'Explain the meaning of your answer.', ' (21 marks)'), '3', 3,
    [point('r-1', O.opt('This means that for each €1 spent in the economy', '32 | P a g e'), 3, 'The meaning, 3 marks.')],
    stem=q7c, figure=q7c_fig, **B)

# Q8 ─ terms; infrastructure; rural decline
add('sb-q8-a', '3-2', 'economic-terms', ref('B', 8, '(a)'),
    O.q(10, 'Explain any three of the following terms:', ' (21 marks)'), '1 @ 11, 2 @ 5', 21,
    [anyN('r-1', 'A term explained — any three', 21, 3, 11,
          O.split('Price inflation\nAn increase in the general', '33 | P a g e',
                  ['Price inflation', 'Full employment', 'Emigration', 'Privatisation']),
          'Any three: the first 11 marks, the next two 5 each.', steps=[11, 5, 5])],
    kind='fixed', **B)
q8b = O.q(10, 'The government is committed to improving the infrastructure', ' (i)')
infra = bl('(i) Infrastructure ⟨6⟩', '(ii) One economic advantage')
add('sb-q8-b-i', '3-5', 'infrastructure', ref('B', 8, '(b)(i)'),
    O.q(10, 'Explain the term infrastructure.', ' (ii)'), '6', 6,
    [point('r-1', infra[0], 6, 'The explanation, 6 marks. The scheme also accepts its second statement.',
           accepts=infra[1:])], stem=q8b, **B)
add('sb-q8-b-ii', '3-5', 'rural-broadband', ref('B', 8, '(b)(ii)'),
    O.q(10, 'Discuss one economic advantage which the provision of broadband', ' (iii)'), '2 @ 8 (5 + 3)', 16,
    [heading('r-households', O.cell('Households Firms', upto='Households') + ' — any one',
             O.cut_cell('More flexible working arrangements Household',
                        ['More flexible working arrangements', 'Access to online banking services', 'Internet access',
                         'Access to state services']), 8, 'One advantage for households, 8 marks (5 + 3).'),
     heading('r-firms', O.cell('Households Firms')[len('Households '):] + ' — any one',
             O.cut_cell('Order supplies and raw materials online will help',
                        ['Order supplies and raw materials', 'Meet consumer orders', 'Methods of payment',
                         'May locate in rural areas']), 8, 'One advantage for firms, 8 marks (5 + 3).')],
    kind='fixed', stem=q8b, **B)
pick('sb-q8-b-iii', '3-5', 'where-ireland-should-invest', ref('B', 8, '(b)(iii)'),
     O.q(10, 'State one example of infrastructure, other than broadband', ' (30 marks)'),
     'An example with its reason — any one',
     [pair(O.cell(e, whole=True), O.cell(r)) for e, r in (
         ('Hospitals', 'As there is an overcrowding'), ('Schools', 'With the increase in population there will'),
         ('Public Transport', 'To reduce emissions and get private'), ('Housing', 'Investment in social, affordable'))],
     1, 8, 'One example and its reason, 8 marks (5 + 3).', stem=q8b, **B)
q8c = O.q(10, 'Small‐town Ireland must fight to thrive.', ' (Source')
pick('sb-q8-c-i', '3-5', 'problems-of-rural-decline', ref('B', 8, '(c)(i)'),
     O.q(10, 'Outline two possible problems caused by the decline', ' (ii)'),
     'A problem caused by the decline — any two',
     O.split('Decline in population/decline in communities', '(ii) State and explain two measures',
             ['Decline in population', 'Loss of local services', 'Physical appearance of town',
              'Under-utilisation of local infrastructure']),
     2, 6, 'Two problems, 6 marks each (4 + 2).', stem=q8c, **B)
pick('sb-q8-c-ii', '3-5', 'reversing-rural-decline', ref('B', 8, '(c)(ii)'),
     O.q(10, 'State and explain two measures which could be introduced', ' (24 marks)'),
     'A measure to reverse the decline — any two',
     O.split('Maintain the local services', '36 | P a g e',
             ['Maintain the local services', 'Improve the infrastructure: roads', 'Provide grants for community centres',
              'Help develop local community enterprises', 'Shop local', 'Incentivise owners']),
     2, 6, 'Two measures, 6 marks each (4 + 2).', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
