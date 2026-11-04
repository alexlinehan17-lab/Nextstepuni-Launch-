#!/usr/bin/env python3
"""Economics 2015 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2015-ol-ev.json, made
from a visual sweep of all 12 paper pages and 36 scheme pages before any 2015
Ordinary card existed. Section B restarts at Question 1, so every citation names
its section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The Ordinary scheme reprints each question above its
answer, so a slice always starts after the reprinted wording. A stem stops
before any printed table: the table is the crop beside the typed ask. The only
prose written here is guidance: tariffs, route labels and what a figure or a
calculation shows.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2015, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2015, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2015-OL-scheme-'
PAP = 'economics-2015-OL-paper-'
bl = H.bullets
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
# The paper's ruled answer lines are set as an ellipsis, so a statement still reads as one to complete.
blanks = lambda t: ' '.join(re.sub(r'\s*_{2,}\s*', ' … ', t).split())


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it:
    "<heading> — <response>". Both halves trace."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def by_heading(rid, label, options, per, note):
    """One printed head ("Households", "To the consumer") and any one of its responses."""
    return heading(rid, H.traced(label) + ' — any one', options, per, note)


def head_cell(first):
    """A table cell that opens with its bold head and runs on into its explanation."""
    return cc(first)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ factors of production
add('sa-q1', '0-1', 'factors-and-their-examples', ref('A', 1, '(i)–(iv)'),
    H.q(2, 'Insert the factor of production or an appropriate example', ' Factor of'), '8 + 4 + 2 + 2', 16,
    [anyN('r-1', 'Each space filled', 16, 4, 8,
          [cc(x) for x in ('(i) AGRICULTURAL LAND oil', '(ii) LABOUR', '(iii) MACHINERY, infrastructure', '(iv) ENTERPRISE')],
          'All four spaces: the first correct response 8 marks, the 2nd 4, the 3rd and 4th 2 each. The spaces sit in the '
          'paper’s table: (i) the example of land, (ii) the factor of a teacher, (iii) the example of capital, (iv) the '
          'factor of a business owner.', steps=[8, 4, 2, 2])],
    kind='fixed', figure=PAP + 'p02-q1-table', **A)

# Q2 ─ perfect competition: true or false
sentences = (('(i) The goods are homogenous / identical.', 'TRUE'), ('(ii) Barriers to entry exist in this market.', 'FALSE'),
             ('(iii) There are many buyers and sellers in the market.', 'TRUE'), ('(iv) The goods are close substitutes.', 'FALSE'))
add('sa-q2', '2-0', 'perfect-competition-true-or-false', ref('A', 2, '(i)–(iv)'),
    # The printed sentences follow the ask, the answer table's header row dropped.
    f"{H.q(2, 'Which of the characteristics / assumptions listed below', ' SENTENCE')} "
    f"{H.q(2, '(i) The goods are homogenous / identical.', ' (16 marks)')}", '8 + 4 + 2 + 2', 16,
    [anyN('r-1', 'Each sentence marked correctly', 16, 4, 8,
          [f'{H.traced(ans)} — {H.traced(sent)}' for sent, ans in sentences],
          'All four: the first correct response 8 marks, the 2nd 4, the 3rd and 4th 2 each.', steps=[8, 4, 2, 2])],
    kind='fixed', **A)

# Q3 ─ corporation tax
add('sa-q3', '3-1', 'corporation-tax-at-12-5', ref('A', 3),
    H.q(2, 'The rate of Corporation Tax in Ireland is currently 12.5 %.', ' Explanation:'), '10 + 6', 16,
    [point('r-explanation', H.traced('This is a tax on the profits made by businesses (in Ireland).'), 10,
           'The explanation, 10 marks (5 + 5).'),
     heading('r-reason', 'A reason — any one',
             H.split('To continue to attract foreign direct investment', 'Explanation: 10 marks',
                     ['To continue to attract', 'To have a competitive tax rate', 'To enable businesses in Ireland re-invest',
                      'To enable businesses to expand', 'To increase economic growth', 'To increase exports',
                      'To improve government finances']), 6, 'One reason, 6 marks.')],
    kind='fixed', **A)

# Q4 ─ visible exports and invisible imports
add('sa-q4', '4-2', 'visible-exports-and-invisible-imports', ref('A', 4),
    blanks(H.ask(3, 'Choose the correct words from the list below', ' (16 marks)')), '6 + 6 + 2 + 2', 16,
    [anyN('r-1', 'Each word placed', 16, 4, 6,
          [f'{H.traced(st)} — {H.traced(w)}' for st, w in (('Statement A', 'Sale'), ('Statement A', 'Goods'),
                                                          ('Statement B', 'Purchase'), ('Statement B', 'Services'))],
          'The four words, as the scheme completes the statements: '
          + H.traced('Visible exports are defined as the Sale of Irish Goods to foreign countries.') + ' '
          + H.traced('Invisible imports are defined as the Purchase of foreign Services by Irish people.')
          + ' The first 2 correct responses 6 marks each, the 3rd and 4th 2 each.', steps=[6, 6, 2, 2])],
    kind='fixed', **A)

# Q5 ─ LDCs
add('sa-q5', '4-0', 'ldcs-and-supporting-them', ref('A', 5, '(a)–(b)'),
    ' '.join([H.q(3, 'State two economic characteristics of Less Developed Countries', ' Characteristic 1'),
              H.q(3, 'Outline one way Ireland (the Irish Government or Irish citizens)', ' _')]), '6 + 6 + 4', 16,
    [anyN('r-1', 'Two characteristics and one way', 16, 3, 6,
          side('(a) State two economic characteristics', bl('• Low per capita income', '(b) Outline one way'))
          + side('(b) Outline one way', bl('• Citizens could buy goods produced in LDCs', 'First 2 correct responses')),
          'Two characteristics for (a) and one way for (b). The scheme prices the three on one ladder, not by part: the '
          'first 2 correct responses 6 marks each, the 3rd 4.', steps=[6, 6, 4])],
    kind='fixed', **A)

# Q6 ─ ECB, CPI, WTO
add('sa-q6', '3-3', 'ecb-cpi-and-wto', ref('A', 6), H.q(3, 'What do the following letters stand for?', ' (17 marks)'), '6 + 6 + 5', 17,
    [anyN('r-1', 'Each name in full', 17, 3, 6,
          [f'{k} — {H.traced(full)}' for k, full in (('ECB', 'European Central Bank'), ('CPI', 'Consumer Price Index'),
                                                    ('WTO', 'World Trade Organisation'))],
          'All three: the first 2 correct responses 6 marks each (2 + 2 + 2), the 3rd 5 (2 + 2 + 1).', steps=[6, 6, 5])],
    kind='fixed', **A)

# Q7 ─ price elasticity of demand
q7 = H.q(4, 'Suppose the Apple iPhone 6 has a Price Elasticity of Demand (PED) of – 2.8.', ' (i)')
add('sa-q7-i', '1-4', 'the-negative-sign', ref('A', 7, '(i)'), H.q(4, 'Explain what is meant by the negative (–) sign.', ' _'), '10', 10,
    [point('r-1', H.traced('This means that as the price of this good rises quantity demanded falls.'), 10,
           'The explanation, 10 marks (5 + 5).')], stem=q7, **A)
add('sa-q7-ii', '1-4', 'reading-price-elasticity', ref('A', 7, '(ii)'),
    H.q(4, 'Circle the correct answer in each case to complete the following statement.', ' (17 marks)'), '4 + 3', 7,
    [anyN('r-1', 'Each circled answer', 7, 2, 4, [H.traced(x) for x in ('rise', '28%')],
          'Both circled answers, as the scheme boxes them: a rise, by 28%. The first correct 4 marks, the second 3.',
          steps=[4, 3])],
    kind='fixed', stem=q7, **A)

# Q8 ─ the brain drain
add('sa-q8', '3-2', 'the-brain-drain', ref('A', 8),
    H.q(4, 'Some economists say Ireland is experiencing a ‘Brain Drain’', ' Explanation:'), '10 + 7', 17,
    [point('r-explanation', H.traced('The emigration of many of the most highly educated Irish workers to rich countries.'), 10,
           'The explanation, 10 marks.'),
     heading('r-problem', 'One other economic problem — any one',
             H.split('Possible higher dependency ratio', 'Explanation: 10 marks',
                     ['Possible higher dependency ratio', 'The state loses out', 'Smaller domestic market']), 7,
             'One other problem, 7 marks.')],
    kind='fixed', **A)

# Q9 ─ online shopping
q9 = H.q(4, 'There are more Irish consumers buying/shopping online (internet).', ' (a)')
pick('sa-q9-a', '1-1', 'benefits-of-online-shopping', ref('A', 9, '(a)'),
     H.q(4, 'Outline two economic benefits of this development for Irish consumers.', ' Benefit 1:'), 'A benefit — any two',
     bl('• Greater choice of goods and services', '2 points at 6 marks each'), 2, 6, 'Two benefits, 6 marks each.', stem=q9, **A)
pick('sa-q9-b', '3-0', 'costs-of-online-shopping', ref('A', 9, '(b)'),
     H.q(4, 'Outline one possible economic cost of this development for the Irish economy.', ' _'), 'A cost — any one',
     bl('• Decline in domestic economic activity', '5 marks'), 1, 5, 'One cost, 5 marks.', stem=q9, **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ imperfect competition; barriers and characteristics; advertising
q1 = ' '.join([H.q(5, 'The diagram below represents the long run equilibrium of a firm in Imperfect Competition.', ' P AC'),
               H.q(5, 'Copy the diagram into your answer book.', ' (i)')])
q1_fig = PAP + 'p05-q1-diagram'
add('sb-q1-a-i', '2-0', 'labels-of-imperfect-competition', ref('B', 1, '(a)(i)'),
    H.q(5, 'State what each of the 5 labels circled above represent.', ' (ii)'), '5 @ 5', 25,
    [point(f'r-{lab.lower()}', f'{lab} — {H.traced(full)}', 5, f'{lab}, 5 marks' + (' (3 + 2).' if len(lab) == 2 else '.'))
     for lab, full in (('P', 'Price'), ('Q', 'Quantity'), ('AC', 'Average Cost'), ('MC', 'Marginal Cost'), ('AR', 'Average Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'equilibrium-in-imperfect-competition', ref('B', 1, '(a)(ii)'),
    H.q(5, 'The firm is in equilibrium at point S.', ' (30 marks)'), '3 + 2', 5,
    [anyN('r-1', 'Each label shown', 5, 2, 3, [H.traced('Q1 the quantity the firm will produce'), H.traced('P1 the price charged for this output')],
          'Q1 and P1: the 1st correct response 3 marks, the 2nd 2. The completed diagram is shown with the answer.', steps=[3, 2])],
    kind='fixed', stem=q1, figure=SOL + 'p09-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
q1b = H.q(5, 'There are no barriers to entry in Imperfect Competition.', ' (i)')
add('sb-q1-b-i', '2-0', 'barriers-to-entry', ref('B', 1, '(b)(i)'), H.q(5, 'Explain the term barriers to entry.', ' (ii)'), '4', 4,
    [point('r-1', H.traced('Are those factors which may prevent other firms from entering a market/ an industry.'), 4,
           'The explanation, 4 marks. ' + H.traced('Example only (2 marks)') + ': ' + H.traced(
               'Example: a single firm may have sole ownership of a factor of production/key resource.'))], stem=q1b, **B)
pick('sb-q1-b-ii', '2-0', 'characteristics-of-imperfect-competition', ref('B', 1, '(b)(ii)–(iii)'),
     ' '.join([H.q(5, 'State two other characteristics of Imperfect Competition.', ' (iii)'),
               H.q(5, 'Write brief notes on each of these.', ' (20 marks)')]), 'A characteristic, with its note — any two',
     H.split('There are many buyers.', '2 at 8 marks each',
             ['There are many buyers.', 'There are many sellers.', 'Differentiated products.', 'Almost Perfect knowledge',
              'Each firm tries to maximise profits.']),
     2, 8, 'Two characteristics, 8 marks each (4 + 4): the scheme prices (ii) and (iii) together.', stem=q1b, **B)
q1c = H.q(5, 'Firms in Imperfect Competition advertise to build brand loyalty.', ' (i)')
add('sb-q1-c-i', '2-0', 'brand-loyalty', ref('B', 1, '(c)(i)'), H.q(5, 'Explain the term brand loyalty.', ' (ii)'), '5', 5,
    [point('r-1', H.opt('The desire by customers to stick with one brand', '5 marks'), 5, 'The explanation, 5 marks.')], stem=q1c, **B)
ADV = {'consumer': ('Provides information / awareness / choice', 'More competitive prices', 'Economies of scale If'),
       'seller': ('Increased Sales / Profits', 'Bigger share of the market', 'New firms Enables')}
DIS = {'consumer': ('Higher prices The firm', 'False / Misleading information', 'Impulse buying', 'Harmful commodities',
                    'May eliminate competition'),
       'seller': ('Increased costs Advertising', 'Expectations of consumers', 'Legal action', 'Pressure to improve performance')}
for part, concept, ask, nxt, table, word in (
        ('ii', 'advantages-of-advertising', 'State and explain one possible advantage of advertising', ' (iii)', ADV, 'advantage'),
        ('iii', 'disadvantages-of-advertising', 'State and explain one possible disadvantage of advertising', ' (25 marks)', DIS, 'disadvantage')):
    add(f'sb-q1-c-{part}', '2-0', concept, ref('B', 1, f'(c)({part})'), H.q(5, ask, nxt), '2 x 5 (3 + 2)', 10,
        [by_heading(f'r-{who}', f'To the {who}', [cc(x) for x in table[who]], 5,
                    f'One {word} for the {who}, 5 marks (3 + 2).') for who in ('consumer', 'seller')],
        kind='fixed', stem=q1c, **B)

# Q2 ─ the market for smartphones; shifts; water charges
q2 = H.q(6, 'The information below represents the market demand and supply schedules for Smartphones.', ' Price')
q2_table = PAP + 'p06-q2-table'
add('sb-q2-a', '1-0', 'drawing-the-smartphone-market', ref('B', 2, '(a)(i)–(iii)'),
    ' '.join([H.q(6, 'Using the above information and one diagram:', ' (a)'), H.q(6, '(i) Draw and label the market demand curve', ' (30 marks)')]),
    '10 + 10 + 4 + 3 + 3', 30,
    [point('r-demand', H.traced('D/C: 5 points at 2 marks each'), 10, 'The demand curve, 10 marks: its five points at 2 each.'),
     point('r-supply', H.traced('S/C: 5 points at 2 marks each'), 10, 'The supply curve, 10 marks: its five points at 2 each.'),
     anyN('r-labels', 'Each label', 4, 4, 1, [H.traced(x) for x in ('P', 'Q', 'D/C', 'S/C')],
          'The four labels, ' + H.traced('(4 at 1 mark each)') + ': the scheme prices them on one line, which spans (i) and (ii).'),
     point('r-p1', 'P1 — ' + H.traced('300'), 3, 'The equilibrium price P1, 3 marks (the scheme’s P1 and Q1 : 2 x 3 marks each). '
           + H.traced('(1 mark each if lines drawn but P1 and Q1 are not labelled).')),
     point('r-q1', 'Q1 — ' + H.traced('30,000'), 3, 'The equilibrium quantity Q1, 3 marks. The completed graph is shown with the answer.')],
    kind='fixed', stem=q2, figure=SOL + 'p12-q2a-graph', **B)
beside_ask(cards[-1], q2_table)
q2b = ' '.join([H.q(6, 'The demand curve for Smartphones OR the supply curve for Smartphones may shift', ' In relation'),
                H.q(6, 'In relation to each development above, answer the following three questions:', ' (i)')])
fault, apps = H.traced('Fault in the Manufacturer’s design'), H.traced('A range of new Apps is made available')
alt_fault = cc('Reputational damage may cause Demand Curve to shift to the left.', whole=True)
alt_apps = cc('Supply Curve may shift to the right as more companies increase', whole=False)
for part, concept, ask, nxt, a, b, per, alt in (
        ('i', 'which-curve-shifts', 'State whether the demand curve or the supply curve will shift', ' (ii)',
         cc('Supply Curve', whole=True), cc('Demand Curve', whole=True), 5, True),
        ('ii', 'which-way-the-curve-shifts', 'State whether the curve you mention will shift to the right or the left', ' (iii)',
         cc('Left', whole=True), cc('Right', whole=True), 3, False),
        ('iii', 'why-the-curve-shifts', 'Explain why the curve has shifted in the direction you have stated.', ' (20 marks)',
         cc('Less smartphones will be supplied at each price.', whole=True), cc('More smartphones will be demanded'), 2, True)):
    note = (' The scheme’s alternative answer for the whole column (10) is also accepted.' if alt else '')
    add(f'sb-q2-b-{part}', '1-0', concept, ref('B', 2, f'(b)({part})'), H.q(6, ask, nxt), f'{per} + {per}', 2 * per,
        [point('r-fault', f'{fault} — {a}', per, f'The design fault, {per} marks.' + note, accepts=[alt_fault] if alt else None),
         point('r-apps', f'{apps} — {b}', per, f'The new Apps, {per} marks.' + note, accepts=[alt_apps] if alt else None)],
        stem=q2b, **B)
q2c = H.q(6, 'Domestic users in most European countries pay for the provision of clean water', ' (i)')
pick('sb-q2-c-i', '1-3', 'why-charge-for-water', ref('B', 2, '(c)(i)'),
     H.q(6, 'Outline two economic reasons for the introduction of water charges for households.', ' (ii)'), 'A reason — any two',
     H.split('1. Revenue\nThese', '2 at 6 marks (3 + 3)', ['Revenue', 'Development of infrastructure', 'Water conservation']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q2c, **B)
add('sb-q2-c-ii', '1-3', 'effects-of-water-charges', ref('B', 2, '(c)(ii)'),
    H.q(6, 'State and explain one possible economic effect which these water charges may have', ' (25 marks)'), '7 + 6', 13,
    [by_heading('r-households', 'Households', [cc(x) for x in ('Lower standard of living', 'Opportunity cost This charge',
                                                             'Reduce consumption of water')], 7,
                'One effect on households, 7 marks: ' + H.traced('State: 4 marks. Explain: 3 marks') + '.'),
     by_heading('r-government', 'Irish Government', [cc(x) for x in ('Reduced consumer spending', 'Public unrest',
                                                                     'Increased employment More people')], 6,
                'One effect on the government, 6 marks (3 + 3).')],
    kind='fixed', stem=q2c, **B)

# Q3 ─ the garden designer's costs; labour; entrepreneurship
q3 = H.q(7, 'Emma O’Neill is an entrepreneur and has set up a business designing and creating gardens.', ' Number of units')
q3_table = PAP + 'p07-q3-table'
add('sb-q3-a-i', '0-1', 'the-entrepreneur', ref('B', 3, '(a)(i)'), H.q(7, 'Explain the underlined term above.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('An entrepreneur undertakes the risk in setting up a business.'), 6,
           'The explanation, 6 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('An entrepreneur combines the other factors of production into a production unit.')])],
    stem=q3, **B)
add('sb-q3-a-ii', '1-5', 'costs-and-profit-for-the-garden-designer', ref('B', 3, '(a)(ii)'),
    H.q(7, 'Using the table calculate the total costs at A and B', ' (iii)'), '4 x 4 (1 + 1 + 2)', 16,
    [point(f'r-{k.lower()}', f'{k}. {H.traced(w)}', 4, f'{k}, 4 marks (1 + 1 + 2).')
     for k, w in (('A', '€2,000 + €3,300 = €5,300'), ('B', '€2,000 + €5,000 = €7,000'), ('C', '€6,500 – €5,300 = €1,200'),
                  ('D', '€8,800 – €7,000 = €1,800'))],
    stem=q3, figure=q3_table, **B)
add('sb-q3-a-iii', '1-5', 'fixed-and-variable-costs-of-gardening', ref('B', 3, '(a)(iii)'),
    H.q(7, 'The following are examples of costs incurred by a garden designer:', ' (30 marks)'), '4 x 1 + 2 x 2', 8,
    [anyN('r-identify', 'Each cost placed', 4, 4, 1,
          [f'{H.traced(kind)} — {H.traced(x)}' for kind, x in (('Fixed costs', 'Lawnmower'), ('Fixed costs', 'Truck'),
                                                               ('Variable costs', 'Plants/Shrubs'), ('Variable costs', 'Fertiliser'))],
          H.traced('Identify 4 costs: 4 at 1 marks = 4 marks') + '.'),
     point('r-fixed', f"{H.traced('Fixed costs')} — {cc('These remain the same irrespective')}", 2, 'Why they are fixed, 2 marks.'),
     point('r-variable', f"{H.traced('Variable costs')} — {cc('These will increase as more gardens')}", 2,
           'Why they are variable, 2 marks: ' + H.traced('2 explanations: 2 at 2 marks = 4 marks') + '.')],
    kind='fixed', stem=q3, **B)
q3b = H.q(7, 'If the business continues to expand Emma may consider employing additional labour', ' (i)')
add('sb-q3-b-i', '2-1', 'labour-and-the-minimum-wage', ref('B', 3, '(b)(i)'), H.q(7, 'Explain each of the underlined terms.', ' (ii)'),
    '6 + 6', 12,
    [point('r-labour', f"{H.traced('Labour')} — {cc('Labour is defined as the human effort')}", 6, 'Labour, 6 marks (4 + 2).'),
     point('r-nmw', f"{H.traced('National Minimum Wage Rate')} — {cc('The lowest wage employers must by')}", 6,
           'The national minimum wage, 6 marks (4 + 2). The scheme prints 7 beside it, but sets it as 4 + 2, and only 6 '
           'fits the paper’s (24) for (b).')],
    stem=q3b, **B)
pick('sb-q3-b-ii', '2-1', 'why-take-on-workers', ref('B', 3, '(b)(ii)'),
     H.q(7, 'State and explain two factors which may encourage Emma to employ additional workers.', ' (24 marks)'), 'A factor — any two',
     H.split('Increased demand for output', '2 factors at 6 marks',
             ['Increased demand for output', 'Government policies', 'Reduction in the national minimum wage']),
     2, 6, 'Two factors, 6 marks each (3 + 3).', stem=q3b, **B)
pick('sb-q3-c-i', '0-1', 'why-entrepreneurship-matters', ref('B', 3, '(c)(i)'),
     H.q(7, 'Outline two reasons why entrepreneurship is important for the Irish economy', ' (ii)'), 'A reason — any two',
     H.split('Improve the Balance of Payments', '2 at 6 marks (3+3)',
             ['Improve the Balance of Payments', 'Encourage further investment', 'Innovation: new products', 'Helps generate tax revenue']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', **B)
add('sb-q3-c-ii', '0-1', 'encouraging-entrepreneurship', ref('B', 3, '(c)(ii)'),
    H.q(7, 'Outline one action which each of the following could take to encourage entrepreneurship:', ' (21 marks)'), '6 + 3', 9,
    [anyN('r-1', 'One action for each — the government and consumers', 9, 2, 6,
          side('The Irish Government', H.split('Enterprise education\nGreater', 'Irish consumers\nIncrease',
                                               ['Enterprise education', 'Government policies', 'Labour market skills', 'Develop the country',
                                                'Promoting/maintaining stability']))
          + side('Irish consumers', H.split('Increase spending in domestic market', '1st correct response',
                                            ['Increase spending in domestic market', 'Buy Irish', 'Shop local', 'Change in attitude'])),
          'One action for the government and one for consumers: the 1st correct response 6 marks (3 + 3), the 2nd 3 (2 + 1).',
          steps=[6, 3])],
    kind='fixed', **B)

# Q4 ─ functions of money; savings; Keynes and other economists
add('sb-q4-a', '3-4', 'functions-of-money', ref('B', 4, '(a)'),
    H.q(7, 'Medium of exchange and measure of value are functions of money.', ' (21 marks)'), '7 + 7 + 7', 21,
    [point('r-medium', 'Medium of exchange — ' + H.traced('An item that buyers give to sellers when they want to purchase goods and services.'),
           7, 'Medium of exchange, 7 marks.'),
     point('r-measure', 'Measure of Value — ' + H.traced('The yardstick people use to post prices and record debts.'), 7,
           'Measure of value, 7 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('Money enables a value/price to be put on goods & services.')]),
     heading('r-other', 'One other function — any one', [H.traced('Store of Wealth'), H.traced('Standard for Deferred Payment')], 7,
             'One other function, 7 marks.')],
    kind='fixed', **B)
q4b = H.q(7, 'The rate of DIRT is one factor which influences the level of personal savings.', ' (i)')
add('sb-q4-b-i', '3-1', 'dirt-in-full', ref('B', 4, '(b)(i)'), H.q(7, 'What do the initials DIRT stand for?', ' (ii)'), '8', 8,
    [point('r-1', H.traced('Deposit Interest Retention Tax'), 8, 'DIRT in full, 8 marks.')], stem=q4b, **B)
add('sb-q4-b-ii', '3-4', 'savings', ref('B', 4, '(b)(ii)'), f"{q4b} {H.q(7, 'Explain the underlined term.', ' (iii)')}", '6', 6,
    [point('r-1', H.traced('Savings: that part of a person’s income which is not spent.'), 6, 'The explanation, 6 marks.')], **B)
pick('sb-q4-b-iii', '3-4', 'what-shapes-saving', ref('B', 4, '(b)(iii)'),
     H.q(7, 'State and explain two factors, other than the rate of DIRT', ' (30 marks)'), 'A factor — any two',
     H.split('Interest rates\n•', '2 at 8 marks each',
             ['Interest rates', 'Income levels', 'Level of Inflation', 'Levels of Social Welfare Benefits', 'Tax levels',
              'Future expectations']),
     2, 8, 'Two factors, 8 marks each (4 + 4).', stem=q4b, **B)
q4c = H.q(7, 'The economist John Maynard Keynes stated that people have three motives', ' Explain')
pick('sb-q4-c-i', '3-4', 'keynes-motives', ref('B', 4, '(c)(i)'), f"{q4c} {H.q(7, 'Explain any two of the above motives.', ' (ii)')}",
     'A motive — any two',
     [f'{cc(m, whole=True)} — {cc(e)}' for m, e in (('Transactionary', 'Cash is needed to buy goods'),
                                                   ('Precautionary', 'Cash is needed for emergencies'),
                                                   ('Speculative', 'Cash is needed to take advantage'))],
     2, 8, 'Two motives, 8 marks each.', **B)
q4cii = H.q(7, 'Name one other economist who contributed to economic thought', ' (24 marks)')
economists = (('marx', 'Karl Marx', ['Labour Theory of Value'], '• The value of an item equals'),
              ('smith', 'Adam Smith', ['Canons of Taxation', 'Perfect Competition', 'Laissez Faire'], '• The principles of a fair taxation'),
              ('malthus', 'Thomas Malthus', ['Theory of Population'], '• Population grows geometrically'),
              ('ricardo', 'David Ricardo', ['Law of Comparative Advantage'], '• Where one country is most efficient'))
for key, name, statements, expl in economists:
    rows = [point('r-name', H.traced(name), 2, 'The economist named, 2 marks.')]
    if len(statements) == 1:
        rows.append(point('r-statement', H.traced(statements[0]), 3, 'The contribution stated, 3 marks.'))
    else:
        rows.append(heading('r-statement', 'A contribution stated — any one', [H.traced(s) for s in statements], 3,
                            'The contribution stated, 3 marks: the scheme lists three for Adam Smith.'))
    rows.append(point('r-explanation', cc(expl).lstrip('• '), 3,
                      'The contribution explained, 3 marks' + (': the scheme’s explanation is of the Canons of Taxation.'
                                                               if key == 'smith' else '.')))
    add(f'sb-q4-c-ii-{key}', '0-0', 'another-economists-contribution', ref('B', 4, '(c)(ii)', key),
        f'{q4cii} Answer for: {H.traced(name)}.', '2 + 3 + 3', 8, rows, kind='fixed', **B)

# Q5 ─ the balance of trade; beef exports; the euro against sterling
q5a = H.q(8, 'You are given the following information about a country’s trade in a year.', ' Visible Exports')
q5a_table = PAP + 'p08-q5a-table'
add('sb-q5-a-i', '4-2', 'the-balance-of-trade', ref('B', 5, '(a)(i)'), H.q(8, 'Explain the term Balance of Trade.', ' (ii)'), '6 (3 + 3)', 6,
    [point('r-1', H.traced('This is the difference between visible exports and visible imports.'), 6, 'The explanation, 6 marks (3 + 3).')],
    **B)
add('sb-q5-a-ii', '4-2', 'calculating-the-balance-of-trade', ref('B', 5, '(a)(ii)'),
    H.q(8, 'Using the above data calculate the Balance of Trade and explain your answer.', ' (iii)'), '6 + 2 + 2', 10,
    [point('r-working', H.traced('€25,000 m - €24,200 m = €800m'), 6, 'The working and the balance, 6 marks (2 + 2 + 2).'),
     point('r-surplus', H.traced('It is a surplus balance of trade.'), 2, 'The surplus, 2 marks (the scheme’s 4 marks: 2 + 2).'),
     point('r-because', H.traced('Because visible exports are greater than visible imports.'), 2, 'The reason, 2 marks.')],
    stem=q5a, figure=q5a_table, **B)
add('sb-q5-a-iii', '4-2', 'a-new-balance-of-trade', ref('B', 5, '(a)(iii)'),
    H.q(8, 'If the level of visible imports above increased by €1,000m', ' (26 marks)'), '4 + 4 + 2', 10,
    [point('r-imports', 'New visible imports — ' + H.traced('€25,200'), 4,
           '4 marks: the scheme’s raised 1 beside each of €24,200m and €1,000m and 2 beside €25,200m.'),
     point('r-balance', 'New Balance of Trade — ' + H.traced('- €200'), 4,
           '4 marks: 1 beside each of €25,000m and €25,200m and 2 beside the -€200.'),
     point('r-deficit', H.traced('It is a deficit'), 2, '2 marks. The figure shows the working as printed.')],
    stem=q5a, figure=SOL + 'p22-q5aiii-working', **B)
beside_ask(cards[-1], q5a_table)
q5b = H.q(8, 'Exports of beef from Ireland should increase due to the ending of a 16-year embargo', ' (i)')
add('sb-q5-b-i', '4-2', 'an-embargo', ref('B', 5, '(b)(i)'), H.q(8, 'Explain the economic term embargo.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('This is a total ban on the importation of a good into a country.'), 5, 'The explanation, 5 marks.')], stem=q5b, **B)
add('sb-q5-b-ii', '4-2', 'beef-as-a-visible-export', ref('B', 5, '(b)(ii)'),
    H.q(8, 'Is the export of beef from Ireland a visible export or an invisible export?', ' (iii)'), '3 + 3', 6,
    [point('r-answer', H.traced('Answer: Visible export'), 3, 'The answer, 3 marks.'),
     point('r-explanation', H.traced('Explanation: It is the purchase of an Irish good by a citizen in the US.'), 3, 'The explanation, 3 marks.')],
    stem=q5b, **B)
pick('sb-q5-b-iii', '4-2', 'benefits-of-more-exports', ref('B', 5, '(b)(iii)'),
     H.q(8, 'State and explain two economic benefits of an increase in exports', ' (25 marks)'), 'A benefit — any two',
     H.split('Employment creation\nExports', '14 marks: 2 benefits',
             ['Employment creation', 'Increased GNP / Economic growth', 'Increased sales / profits', 'The receipt of foreign currencies',
              'Attract investment', 'Government finances']),
     2, 7, 'Two benefits, 7 marks each: ' + H.traced('State: 4 marks. Explain: 3 marks.'), stem=q5b, **B)
# The two boxed rates are one printed line each, so the stem carries them.
q5c = H.q(8, 'You are given the following information regarding the euro', ' Explain the possible')
effects = (('Ireland’s exports to the UK', '• Exports cheaper', 'The prices of Irish exports'),
           ('Ireland’s imports from the UK', '• Imports dearer', 'The prices of UK imports'),
           ('Employment in Ireland', '• Increase', 'With increased exports to the UK'))
add('sb-q5-c', '4-2', 'a-weaker-euro-against-sterling', ref('B', 5, '(c)(i)–(iii)'),
    H.q(8, 'Explain the possible effects which this fall in the value of the euro', ' (24 marks)'), '12 + 6 + 6', 24,
    [anyN('r-1', 'The effect on each — all three', 24, 3, 12,
          [f'{cc(area, whole=True)} — {cc(eff)} {cc(expl)}' for area, eff, expl in effects],
          'All three areas, each its effect and explanation. The scheme prices them by order, not by area: the 1st correct '
          'answer 12 marks (state 6, explain 6), the 2nd and 3rd 6 each (3 + 3).', steps=[12, 6, 6])],
    kind='fixed', stem=q5c, **B)

# Q6 ─ the current budget; income tax; cigarettes
q6a = H.q(9, 'The estimated Government current budget for 2015 is as follows:', ' (i)')
add('sb-q6-a-i', '3-1', 'the-current-budget-deficit', ref('B', 6, '(a)(i)'), H.q(9, 'Calculate the current budget deficit.', ' (ii)'),
    '1 + 2 + 2', 5,
    [point('r-income', 'Government current income — ' + H.traced('€45,255'), 1, '1 mark, printed beside the income figure.'),
     point('r-expenditure', 'Less government current expenditure — ' + H.traced('€48,985'), 2,
           '2 marks, the scheme’s 1 beside the minus sign and 1 beside the expenditure figure.'),
     point('r-deficit', 'Current budget deficit — ' + H.traced('(€ 3,730)'), 2,
           '2 marks, printed beside the answer: ' + H.traced('3 at 1 mark each and correct answer 2 marks') + '. The figure shows the working.')],
    stem=q6a, figure=SOL + 'p25-q6ai-working', **B)
add('sb-q6-a-ii', '3-1', 'reducing-the-deficit', ref('B', 6, '(a)(ii)'), H.q(9, 'Suggest two ways the government could reduce this deficit.', ' (iii)'),
    '2 x 5', 10,
    [point('r-spending', H.traced('Reduce current government expenditure or examples of this e.g. reduce social welfare spending.'), 5,
           'Cutting spending, 5 marks.'),
     point('r-income', H.traced('Increase current government income or examples of this e.g. increase income tax.'), 5,
           'Raising income, 5 marks.')], stem=q6a, **B)
add('sb-q6-a-iii', '3-1', 'current-income-and-expenditure', ref('B', 6, '(a)(iii)'),
    H.q(9, 'State one example of Government current income and one example', ' (25 marks)'), '2 x 5', 10,
    [by_heading('r-income', 'Government current income',
                H.split('1. Direct tax revenue (or example)', '1. Salaries of all state employees',
                        ['Direct tax revenue', 'Indirect tax revenue', 'Interest on loans', 'Surpluses of semi-state',
                         'Departmental balances', 'Prize Bond scheme', 'Fees charged for state services'], occ=0, source='cells'), 5,
                'One example of current income, 5 marks.'),
     by_heading('r-expenditure', 'Government current expenditure',
                H.split('1. Salaries of all state employees', ' Government current income',
                        ['Salaries of all state employees', 'Cost of running government', 'Costs of running state institutions',
                         'Social welfare payments', 'National debt service', 'Grants to local authorities',
                         'Ireland’s contribution to the EU'], occ=0, source='cells'), 5,
                'One example of current expenditure, 5 marks.')],
    kind='fixed', stem=q6a, **B)
q6b = H.q(9, 'In Budget 2015 the Government reduced the higher rate of income tax', ' (i)')
add('sb-q6-b-i', '3-1', 'the-usc', ref('B', 6, '(b)(i)'), H.q(9, 'What do the initials USC stand for?', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Universal Social Charge'), 6, 'The name, 6 marks.')], stem=q6b, **B)
add('sb-q6-b-ii', '3-1', 'income-tax-as-a-direct-tax', ref('B', 6, '(b)(ii)'), H.q(9, 'Is income tax a direct or indirect tax?', ' (iii)'),
    '3 + 3', 6,
    [point('r-answer', H.traced('Answer: Direct tax.'), 3, 'The answer, 3 marks.'),
     point('r-explanation', H.traced('Explanation: It is a tax levied on income.'), 3, 'The explanation, 3 marks.')], stem=q6b, **B)
cut_bullets = lambda cell: [H.traced(x.strip()) for x in cc(cell).split('•') if x.strip()]
# The scheme prices its Statement and Explanation columns apart (2 at 3 marks
# each), and its cells never print a statement beside its own explanation, so
# each column is its own claim, each response named by its category.
areas = (('Government’s current budget deficit', ['Deficit may increase.', 'Deficit may decrease.'],
          cut_bullets('• If there is no increase in employment')),
         ('Level of employment in Ireland', ['May increase.'], cut_bullets('• If spending increases this may boost')),
         ('Level of emigration from Ireland', ['May fall.'], cut_bullets('• More disposable incomes may encourage')))
add('sb-q6-b-iii', '3-1', 'a-lower-income-tax-rate', ref('B', 6, '(b)(iii)'),
    H.q(9, 'Explain one possible economic effect which the reduction in the rate of income tax', ' (24 marks)'), '2 x 3 + 2 x 3', 12,
    [anyN('r-statement', 'The effect stated — any two areas', 6, 2, 3,
          [f'{cc(area, whole=True)} — {H.traced(st)}' for area, sts, _ in areas for st in sts],
          'The effect on two of the three areas, 3 marks each: the scheme’s Statement column, '
          + H.traced('2 at 3 marks') + '.'),
     anyN('r-explanation', 'The effect explained — the same two areas', 6, 2, 3,
          [f'{cc(area, whole=True)} — {b}' for area, _, bs in areas for b in bs],
          'The explanation for each of the two areas, 3 marks each: the scheme’s Explanation column, '
          + H.traced('2 at 3 marks') + '. The budget deficit’s first explanation goes with Deficit may increase, the '
          'other two with Deficit may decrease.')],
    kind='fixed', stem=q6b, **B)
q6c = H.q(9, 'The tax on a packet of twenty cigarettes was increased by 40c in Budget 2015.', ' (i)')
pick('sb-q6-c-i', '1-3', 'reducing-cigarette-consumption', ref('B', 6, '(c)(i)'),
     H.q(9, 'Outline one other measure which could be taken to reduce the consumption of cigarettes.', ' (ii)'), 'A measure — any one',
     [f'{cc(m, whole=True)} — {cc(e)}' for m, e in (
         ('Introduce plain packaging.', 'This may limit advertising'), ('Ban vending machines in pubs.', 'This will reduce availability'),
         ('Restrict number of sales outlets.', 'The sale of cigarettes could be banned'),
         ('Subsidise products available to help people quit smoking.', 'Subsidising such products'),
         ('Provide Information on the negative effects of cigarette consumption.', 'The use of more shocking'))],
     1, 6, 'One measure, 6 marks: ' + H.traced('State: 3 marks. Explanation: 3 marks.'), stem=q6c, **B)
pick('sb-q6-c-ii', '1-3', 'smoking-less-for-individuals', ref('B', 6, '(c)(ii)'),
     H.q(9, 'State and explain two economic benefits for individuals if they reduce their consumption', ' (iii)'), 'A benefit — any two',
     H.split('Greater disposable incomes:', '10 marks: 2 at 5 marks', ['Greater disposable incomes:', 'Healthier lifestyle:',
                                                                    'Reduced spending on healthcare:', 'Reduced healthcare insurance premiums:',
                                                                    'Increased life expectancy:']),
     2, 5, 'Two benefits, 5 marks each (3 + 2).', stem=q6c, **B)
pick('sb-q6-c-iii', '2-2', 'smoking-less-for-society', ref('B', 6, '(c)(iii)'),
     H.q(9, 'State and explain two benefits for society if the consumption of cigarettes falls.', ' (26 marks)'), 'A benefit — any two',
     H.split('Greater productivity/reduction in absenteeism', '10 marks: 2 at 5',
             ['Greater productivity/reduction', 'Reduction in cancer related deaths', 'Population healthier:', 'Improved environment:']),
     2, 5, 'Two benefits, 5 marks each (3 + 2).', stem=q6c, **B)

# Q7 ─ social housing; economic growth; the EU
q7a = ' '.join([H.q(9, 'Following Budget 2015 the Government announced plans to spend €2.2bn', ' Note:'),
                H.q(9, 'Note: Social Housing refers to housing supplied by the Government', ' (i)')])
add('sb-q7-a-i', '3-1', 'social-housing-as-capital-spending', ref('B', 7, '(a)(i)'),
    H.q(9, 'Does this spending on social housing represent current expenditure or capital expenditure', ' (ii)'), '3 + 3', 6,
    [point('r-answer', H.traced('Answer: Capital expenditure'), 3, 'The answer, 3 marks.'),
     point('r-explanation', H.traced('Explanation: Citizens will benefit from social housing over a number of years.'), 3,
           'The explanation, 3 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('This is a once-off / long-term item of expenditure.')])], stem=q7a, **B)
pick('sb-q7-a-ii', '3-1', 'advantages-of-social-housing', ref('B', 7, '(a)(ii)'),
     H.q(9, 'Outline two advantages of expenditure on social housing for the Irish economy.', ' (iii)'), 'An advantage — any two',
     [f'{cc(s, whole=True)} — {cc(e)}' for s, e in (
         ('Reduced homelessness', 'With more housing available'), ('Improved standard of living', 'Those people who move from hostels'),
         ('Generates employment in construction industry', 'Demand for workers in the construction'),
         ('Reduced rental prices', 'With increased supply of housing'), ('Improved infrastructure', 'The state’s infrastructure improves'),
         ('Economic growth', 'There will be an increase in demand for goods and services associated'))],
     2, 7, 'Two advantages, 7 marks each: ' + H.traced('State: 4 marks. Explain: 3 marks.'), stem=q7a, **B)
add('sb-q7-a-iii', '0-1', 'the-opportunity-cost-of-social-housing', ref('B', 7, '(a)(iii)'),
    H.q(9, 'Explain, using an example, one opportunity cost of this investment in social housing.', ' (26 marks)'), '3 + 3', 6,
    [point('r-cost', H.traced('The government could spend the money on health care.'), 3,
           'The opportunity cost, 3 marks: ' + H.traced('Any one example stated and explained: 6 marks (3 + 3)') + '.'),
     point('r-example', H.traced('They could open wards in hospitals / invest in new ambulances.'), 3, 'The example, 3 marks.')],
    stem=q7a, **B)
q7b = H.q(9, '“The Irish economy is forecast to grow by 3.7% in 2015', ' (i)')
add('sb-q7-b-i', '3-5', 'measuring-growth', ref('B', 7, '(b)(i)'), H.q(9, 'State one measure of economic growth.', ' (ii)'), '7', 7,
    [heading('r-1', 'A measure — any one', [H.traced('Gross National Product / GNP'), H.traced('Gross Domestic Product / GDP')], 7,
             'One measure, 7 marks.')], kind='fixed', stem=q7b, **B)
growth = (('Irish citizens', ['Employment opportunities', 'Increased standard of living', 'Improved state services', 'Less need to emigrate'],
           '• If sales increase more workers'),
          ('Businesses', ['Increased sales / profits', 'Expansion / less risk of closure'], '• Sales increase leading'),
          ('Government finances', ['Tax revenues', 'Social welfare spending', 'Reduced borrowing / Ability to repay debt'], '• Increased employment will result'))
rows = []
for who, statements, first in growth:
    expl = cut_bullets(first)
    rows.append(by_heading(f'r-{who.split()[0].lower()}', who,
                           [f'{H.traced(s) if " / Ability" not in s else H.traced("Reduced borrowing") + " / " + H.traced("Ability to repay debt")} — {e}'
                            for s, e in zip(statements, expl)], 6,
                           f'One benefit for {who if who.startswith("Irish") else who.lower()}, 6 marks: ' + H.traced('State: 3 marks') + ', ' + H.traced('Explain: 3 marks') + '.'))
add('sb-q7-b-ii', '3-5', 'who-gains-from-growth', ref('B', 7, '(b)(ii)'),
    H.q(9, 'State and explain one benefit of economic growth for each of the following', ' (25 marks)'), '3 x 6 (3 + 3)', 18,
    rows, kind='fixed', stem=q7b, **B)
q7c = H.q(9, 'Ireland has been a member of the European Union (EU) since 1973.', ' (i)')
pick('sb-q7-c-i', '4-1', 'why-join-the-eu', ref('B', 7, '(c)(i)'),
     H.q(9, 'Outline two reasons why countries may want to become members of the EU.', ' (ii)'), 'A reason — any two',
     bl('• Assess to a larger market', '2 points at 6 marks each'), 2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q7c, **B)
pick('sb-q7-c-ii', '4-1', 'disadvantages-of-eu-membership', ref('B', 7, '(c)(ii)'),
     H.q(9, 'Outline two possible economic disadvantages for Ireland of membership of the EU.', ' (24 marks)'), 'A disadvantage — any two',
     bl('• Cost to Ireland', '2 points at 6 marks each'), 2, 6, 'Two disadvantages, 6 marks each (3 + 3).', stem=q7c, **B)

# Q8 ─ the circular flow; the national income formula; the multiplier
q8a = H.q(10, 'The diagram below represents the Circular Flow of Income in an economy without government', ' 1 Households')
q8a_fig = PAP + 'p10-q8a-diagram'
add('sb-q8-a-i', '3-0', 'lines-of-a-simple-circular-flow', ref('B', 8, '(a)(i)'),
    H.q(10, 'Copy the diagram into your answerbook. Clearly label each of the lines 1 to 3.', ' (ii)'), '4 + 3 + 4', 11,
    [point('r-1', '1 — ' + H.traced('Supply factors of production to firms'), 4, 'Line 1, 4 marks (2 + 2).'),
     point('r-2', '2 — ' + H.traced('Spending / payment for goods and services.'), 3, 'Line 2, 3 marks.'),
     point('r-3', '3 — ' + H.traced('Households receive factor income for supplying inputs (factors of production)'), 4,
           'Line 3, 4 marks (2 + 2).')],
    stem=q8a, figure=q8a_fig, **B)
add('sb-q8-a-ii', '3-0', 'households-and-firms', ref('B', 8, '(a)(ii)'),
    H.q(10, 'Explain the types of transactions / activities which take place between households and firms.', ' (iii)'), '2 x 4 (2 + 2)', 8,
    [point('r-households', H.traced('Households: supply factors of production (to firms) and in return receive an income.'), 4,
           'Households, 4 marks (2 + 2).'),
     point('r-firms', H.traced('Firms: sell commodities (goods & services) to households, who spend their income on these.'), 4,
           'Firms, 4 marks (2 + 2).')], stem=q8a, figure=q8a_fig, **B)
add('sb-q8-a-iii', '4-2', 'is-ireland-open', ref('B', 8, '(a)(iii)'), H.q(10, 'Is Ireland an open economy? Explain your answer.', ' (25 marks)'),
    '3 + 3', 6,
    [point('r-answer', H.traced('Answer: It is an open economy.'), 3, 'The answer, 3 marks.'),
     point('r-explanation', H.traced('Explanation: it engages in trade i.e. it imports and exports goods and services.'), 3,
           'The explanation, 3 marks.')], **B)
q8b = H.q(10, 'National Income is calculated using the following formula:', ' (i)')
add('sb-q8-b-i', '3-0', 'national-income', ref('B', 8, '(b)(i)'), f"{q8b} {H.q(10, 'Explain the underlined term.', ' (ii)')}", '5', 5,
    [point('r-1', H.traced('Income earned by the permanent residents of a country from current economic activity in one year.'), 5,
           'The explanation, 5 marks: the scheme prints 4 marks and 1 mark beneath its one sentence.')], **B)
add('sb-q8-b-ii', '3-0', 'i-x-and-m', ref('B', 8, '(b)(ii)'), H.q(10, 'State what each of the letters I, X and M stand for.', ' (iii)'),
    '3 x 5', 15,
    [point(f'r-{k.lower()}', H.traced(f'{k}: {w}'), 5, f'{k}, 5 marks.')
     for k, w in (('I', 'Investment expenditure.'), ('X', 'Exports.'), ('M', 'Imports'))], stem=q8b, **B)
pick('sb-q8-b-iii', '3-0', 'why-consumer-spending-is-rising', ref('B', 8, '(b)(iii)'),
     H.q(10, 'The level of consumer spending (consumption) is beginning to rise in Ireland.', ' (30 marks)'), 'A reason — any two',
     [f'{cc(s, whole=True)} — {cc(e)}' for s, e in (
         ('Increase in employment', 'Employment is increasing in Ireland'), ('Decrease in income tax rate / USC rate', 'In Budget 2015 the government'),
         ('Increase in consumer confidence', 'Some consumers are feeling more confident'),
         ('Competitive credit terms from car dealerships', 'Some car dealerships are offering'))],
     2, 5, 'Two reasons, 5 marks each (3 + 2).', stem=q8b, **B)
q8c = H.q(10, 'The Multiplier formula for an open economy is:', ' 1 MPS')
q8c_fig = PAP + 'p10-q8c-formula'
add('sb-q8-c-i', '3-0', 'mpm-and-mps', ref('B', 8, '(c)(i)'), H.q(10, 'Explain the terms MPM and MPS.', ' Assume'), '6 + 6', 12,
    [point('r-mpm', f"{H.traced('MPM: Marginal Propensity to Import')} — {H.traced('The proportion of extra income which is spent on imports.')}", 6,
           'MPM, 6 marks (3 + 3).'),
     point('r-mps', f"{H.traced('MPS: Marginal Propensity to Save')} — {H.traced('The proportion of extra income which is saved.')}", 6,
           'MPS, 6 marks (3 + 3).')], stem=q8c, figure=q8c_fig, **B)
add('sb-q8-c-ii', '3-0', 'calculating-the-multiplier', ref('B', 8, '(c)(ii)'),
    ' '.join([H.q(10, 'Assume that MPM is 0.3 and MPS is 0.2.', ' (ii)'), H.q(10, 'Calculate, using the above formula, the size of the Multiplier.', ' (20 marks)')]),
    '4 x 2', 8,
    [anyN('r-1', 'Each starred figure', 8, 4, 2, [H.traced(x) for x in ('1*', '0.3*', '0.2*', '2*')],
          H.traced('8 marks: each * figure at 2 marks each.') + ' The figure shows the working as printed: 1 over 0.3 + '
          '0.2, and the answer 2.')],
    kind='fixed', stem=q8c, figure=SOL + 'p33-q8cii-working', **B)
beside_ask(cards[-1], q8c_fig)

if __name__ == '__main__':
    emit(cards)
