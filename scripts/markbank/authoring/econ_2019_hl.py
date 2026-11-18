#!/usr/bin/env python3
"""Economics 2019 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2019-hl-ev.json, made
from a visual sweep of all 12 paper pages and 36 scheme pages before any 2019
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The only prose written here is guidance: tariffs, route
labels and what a figure or a calculation shows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import show_before_reveal  # noqa: E402
from econ_legacy_lib import Old, OldDeck  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2019, 'higher', 'LC034ALP000EV')
D = OldDeck(2019, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2019-HL-scheme-'
PAP = 'economics-2019-HL-paper-'
GRADED = ' Graded.'


bl = H.bullets


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ the equi-marginal principle
add('sa-q1-a', '1-1', 'equi-marginal-principle', ref('A', 1, '(a)'),
    H.q(2, 'Explain the economic concept of the Equi‐Marginal Principle', ' (b)'), '6 (3 + 3)', 6,
    [point('r-1', H.opt('The equi-marginal principle of consumer behaviour states', 'The equi-marginal principle states'), 6,
           'The principle, 6 marks (3 + 3). The scheme also accepts its second statement of it.',
           accepts=[H.opt('The equi-marginal principle states that utility', '(b) MUA')])], **A)
add('sa-q1-b', '1-1', 'equi-marginal-calculation', ref('A', 1, '(b)'),
    ' '.join([H.q(2, 'In equilibrium, a consumer buys 6 apples', ' Workings:'),
              H.q(2, 'at €0.90 each and 7 oranges', ' Answer:'), H.q(2, '(Show your workings.)', ' (16 marks)')]),
    '10', 10,
    [point('r-1', H.traced(H.chunk('MUO = 5 utils.', '\n').strip()), 10,
           'The answer with its working, 10 marks. The scheme sets the working as fractions: MU over price is '
           'equal for both goods, so the orange’s MU is 0.50 times 9 over 0.90. The figure shows it as printed.')],
    figure=SOL + 'p06-q1b-working', **A)

# Q2 ─ true or false: the labour market
q2 = H.q(2, 'Indicate by means of a tick', ' STATEMENT')
add('sa-q2', '2-1', 'labour-market-true-or-false', ref('A', 2), q2, '4 @ 4', 16,
    [point('r-derived', 'TRUE — ' + H.cell('The demand for labour is a derived demand.'), 4,
           'TRUE, 4 marks.'),
     point('r-register', 'FALSE — ' + H.cell('The Live Register is the most accurate measure of Ireland’s unemployment rate.'), 4,
           'FALSE, 4 marks.'),
     point('r-cyclical', 'TRUE — ' + H.cell('Cyclical unemployment is caused by a recession.'), 4,
           'TRUE, 4 marks.'),
     point('r-backward', 'TRUE — ' + H.cell('The backward bending labour supply curve illustrates'), 4,
           'TRUE, 4 marks. The completed table is shown in the figure.')],
    figure=SOL + 'p06-q2-ticks', **A)
show_before_reveal(cards[-1], None, PAP + 'p02-q2-question')

# Q3 ─ development and growth
add('sa-q3', '4-0', 'economic-development-and-growth', ref('A', 3),
    H.q(2, 'Distinguish between the terms Economic Development', ' (16 marks)'), '2 @ 8 graded', 16,
    [point('r-development', H.bo('Economic development refers to', ' Economic growth refers'), 8,
           'Economic development, 8 marks.' + GRADED),
     point('r-growth', H.bo('Economic growth refers to', 'society.', include_end=True), 8,
           'Economic growth, 8 marks.' + GRADED)], **A)

# Q4 ─ Keynes
pick('sa-q4', '0-0', 'keynes-contributions', ref('A', 4),
     H.q(3, 'Outline two main contributions to economic thought', ' (i)'),
     'A contribution by Keynes — any two',
     H.split('Favoured government intervention - Keynes', '5. (a) The diagram below',
             ['Favoured government intervention', 'The Multiplier Effect', 'Liquidity preference theory',
              'Paradox of thrift', 'Investment - could be', 'Keynes took issue with Say’s Law']),
     2, 8, 'Two contributions, 8 marks each.', **A)

# Q5 ─ long-run equilibrium in imperfect competition
q5_stem = H.q(3, 'The diagram below represents the long run equilibrium', ' (i)')
q5_fig = PAP + 'p03-q5-question'   # the whole printed question: diagram, answer box and asks
add('sa-q5-i', '2-0', 'labelling-imperfect-competition', ref('A', 5, '(i)'),
    H.q(3, 'Write in full the label (not abbreviation)', ' Price 2') + ' '
    + H.q(3, 'for each of the lines numbered 1 to 4.', ' 1 Use') + ' '
    + H.q(3, 'Use the answer box provided.', ' Number'), '4 @ 2', 8,
    [point(f'r-{n}', f'{n} — ' + H.cell(label), 2, f'Line {n}, 2 marks.')
     for n, label in ((1, 'Marginal Cost'), (2, 'Average Cost'), (3, 'Marginal Revenue'),
                      (4, 'Demand / Average Revenue'))],
    stem=q5_stem, figure=q5_fig, **A)
p1c1q1 = H.traced(H.chunk('P1 / C1 / Q1', ' ⟨'))
add('sa-q5-ii', '2-0', 'equilibrium-in-imperfect-competition', ref('A', 5, '(ii)'),
    H.q(3, 'Show clearly on the diagram the long run equilibrium', ' (iii)'), '3 @ 1', 3,
    [point(f'r-{x.lower()}', H.traced(x), 1, f'{x}, 1 mark.') for x in p1c1q1.split(' / ')],
    stem=q5_stem, figure=SOL + 'p07-q5-diagram', **A)
show_before_reveal(cards[-1], None, q5_fig)
add('sa-q5-iii', '2-0', 'normal-profit-in-imperfect-competition', ref('A', 5, '(iii)'),
    H.q(3, 'State whether or not the firm is earning supernormal profits.', ' (16 marks)'), '2 + 3', 5,
    [point('r-answer', H.opt('The firm is not earning supernormal profits', 'This is because'), 2,
           'The answer, 2 marks.'),
     point('r-reason', H.opt('This is because the firm produces where AR=AC.', '7 | P a g e'), 3,
           'The reason, 3 marks.')],
    stem=q5_stem, figure=q5_fig, **A)

# Q6 ─ free trade area and customs union
add('sa-q6', '4-2', 'free-trade-area-and-customs-union', ref('A', 6),
    H.q(3, 'Distinguish between a Free Trade Area and a Customs Union.', ' (17 marks)'), '11 + 6', 17,
    [point('r-fta', H.opt('A Free Trade Area means', 'A Customs Union is'), None,
           'The scheme prices the distinction 11 + 6 beside both definitions and does not say which earns '
           'which.'),
     point('r-cu', H.opt('A Customs Union is more advanced', '7. (a) Approximate'), None,
           'Claim the complete response: 17 marks in all.')],
    kind='questionTotal', **A)

# Q7 ─ debt-to-GDP and unemployment
add('sa-q7-a', '3-1', 'irish-debt-and-unemployment-rates', ref('A', 7, '(a)'),
    H.q(4, 'Place a tick', ' (b)'), '5 + 4', 9,
    [point('r-debt', H.opt('Approximate debt to GDP ratio 70%', 'Approximate unemployment'), None,
           'The scheme prices the two ticks 5 + 4 and does not say which earns which.'),
     point('r-unemployment', H.opt('Approximate unemployment rate 6%', '(b) Due to'), None,
           'Claim both: 9 marks in all.')],
    kind='questionTotal', **A)
add('sa-q7-b', '3-1', 'recent-trends-in-debt-and-unemployment', ref('A', 7, '(b)'),
    H.q(4, 'Explain the recent trend for each economic indicator above.', ' Government'), '4 + 4', 8,
    [point('r-debt', H.opt('Due to increased economic growth the ratio', 'Unemployment has continued'), 4,
           'The debt-to-GDP trend, 4 marks.'),
     point('r-unemployment', H.opt('Unemployment has continued to decrease', '8. Advantages'), 4,
           'The unemployment trend, 4 marks.')], **A)

# Q8 ─ raising the higher-rate threshold
add('sa-q8', '3-1', 'raising-the-higher-tax-threshold', ref('A', 8),
    H.q(4, 'Outline two possible economic advantages and one possible', ' Advantages:'), '1 @ 9, 1 @ 4; 4', 17,
    [anyN('r-advantage', 'An advantage — any two', 13, 2, 9,
          H.split('Increased disposable income/improved standard of living.', 'Disadvantage',
                  ['Increased disposable income', 'Incentive to work', 'More equitable',
                   'Greater consumer demand', 'Reduced pressure on wage demands']),
          'Two advantages: the first 9 marks, the second 4 (graded).', steps=[9, 4]),
     anyN('r-disadvantage', 'A disadvantage — any one', 4, 1, 4,
          H.split('Less government revenue from taxation.', '8 | P a g e',
                  ['Less government revenue from taxation', 'Negative impact on balance of payments']),
          'One disadvantage, 4 marks.')],
    kind='fixed', stem=H.q(4, 'The Taoiseach has pledged', ' Outline two'), **A)

# Q9 ─ extended working lives
q9_stem = H.q(5, 'In Japan 12% of the working population', ' (a)')
add('sa-q9-a', '2-1', 'supporting-extended-working-lives', ref('A', 9, '(a)'),
    H.q(5, 'Outline two reasons why government policies', ' (i)'), '1 @ 9, 1 @ 4 graded', 13,
    [anyN('r-1', 'A reason to support extended working lives — any two', 13, 2, 9,
          H.split('Enlarged labour force/ healthier workforce', 'Pension top-up schemes.',
                  ['Enlarged labour force', 'Valuable skillset and experience', 'Increased income tax revenue',
                   'Reduced government spending on pensions', 'Recognition of a valuable part of society',
                   'Improved dependency ratio']),
          'Two reasons: the first 9 marks, the second 4 (graded).', steps=[9, 4])],
    kind='fixed', stem=q9_stem, **A)
pick('sa-q9-b', '2-1', 'measures-for-extended-working-lives', ref('A', 9, '(b)'),
     H.q(5, 'Suggest one measure which the government or firms', ' (17 marks)'),
     'A measure — any one',
     H.split('Pension top-up schemes.', '9 | P a g e',
             ['Pension top-up schemes', 'Tax breaks', 'Offer more flexible work arrangements',
              'Investment in lifelong education', 'Investment in redesigning office',
              'Promotion of an age-inclusive work culture', 'Abolish / increase the statutory retirement age']),
     1, 4, 'One measure, 4 marks.', stem=q9_stem, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')


def diagram_card(cid, concept, parts, qtext, stem, crit, explain, crits, fig):
    """A shift diagram and its explanation: 5 for the diagram at 1 per element,
    5 for the explanation (the reason 2, then shift, price and quantity 1 each)."""
    reason, shift = crits
    rows = [point('r-diagram', crit, 5, 'The diagram, 5 marks: 1 for each element the scheme names.')]
    rows.append(point('r-reason', explain[0], 2, reason))
    for i, text in enumerate(explain[1:4], 1):
        rows.append(point(f'r-step-{i}', text, 1, shift))
    return add(cid, '1-0', concept, ref('B', 1, parts), qtext, 'Diagram 5 + explanation 5', 10, rows,
               stem=stem, figure=fig, **B)


# Q1 ─ demand, market equilibrium, rent control
add('sb-q1-a-i', '1-1', 'individual-and-market-demand', ref('B', 1, '(a)(i)'),
    H.q(6, 'Define the economic terms individual demand and market demand.', ' (ii)'), '5 + 5', 10,
    [point('r-individual', H.opt('Individual demand refers to the quantity demanded', 'Market demand refers'), 5,
           'Individual demand, 5 marks.'),
     point('r-market', H.opt('Market demand refers to the aggregate', '(ii) • Change'), 5,
           'Market demand, 5 marks.')], **B)
pick('sb-q1-a-ii', '1-1', 'factors-affecting-market-demand', ref('B', 1, '(a)(ii)'),
     H.q(6, 'Outline three factors that would affect market demand', ' [25]'),
     'A factor affecting market demand — any three',
     bl('(ii) • Change in consumer tastes', '10 | P a g e'),
     3, 5, 'Three factors, 5 marks each (2 + 3).', **B)
q1b = H.q(6, 'Assume the market for a brand of Irish crisps is in equilibrium.', ' (i) The lack')
diagram_card('sb-q1-b-i', 'supply-shift-from-a-drought', '(b)(i)',
             H.q(6, 'The lack of rainfall in 2018 creates a drought', ' (ii) Vegan'), q1b,
             H.opt('D1, S1, S2, Indication of higher equilibrium price', 'Reference to reduced'),
             bl('• The lack of rainfall reduces the potato crop', 'D1, S1, S2, Indication of higher'),
             (H.opt('Reference to reduced availability of raw materials', 'Shift S/C to the left'),
              H.opt('Shift S/C to the left, Higher P, Lower Q', '11 | P a g e')),
             SOL + 'p11-q1bi-diagram')
diagram_card('sb-q1-b-ii', 'demand-shift-from-protests', '(b)(ii)',
             H.q(6, 'Vegan consumers stage protests', ' (iii) Crisp'), q1b,
             H.opt('S1, D1, D2, Indication of lower equilibrium price and lower quantity', 'Reference to negative'),
             bl('• The protests against the product', 'S1, D1, D2, Indication'),
             (H.opt('Reference to negative publicity reducing demand', 'Shift D/C'),
              H.opt('Shift D/C to the left, Lower P, Lower Q', '(iii) Price')),
             SOL + 'p12-q1bii-diagram')
diagram_card('sb-q1-b-iii', 'supply-shift-from-a-subsidy', '(b)(iii)',
             H.q(6, 'Crisp companies receive a subsidy from the government.', ' [30]'), q1b,
             H.opt('D1, S1, S2, Indication of lower equilibrium price and higher quantity', 'Reference to subsidy'),
             bl('• A subsidy is a payment from the govt.', 'D1, S1, S2, Indication of lower'),
             (H.opt('Reference to subsidy reducing cost of production', 'Shift S/C to the right'),
              H.opt('Shift S/C to the right, Lower P, Higher Q', '12 | P a g e')),
             SOL + 'p12-q1biii-diagram')
q1c = ' '.join([H.q(6, 'The latest figures from the Residential Tenancies Board', ' (Source'),
                H.q(6, 'The diagram above illustrates a government intervention', ' (i)')])
q1c_fig = PAP + 'p06-q1c-diagram'
add('sb-q1-c-i', '1-3', 'rent-control-as-a-price-ceiling', ref('B', 1, '(c)(i)'),
    H.q(6, 'Explain the impact of the implementation of the rent control', ' (ii)'), '12 (graded)', 12,
    [point('r-ceiling', H.opt('The price has been restricted to / set at the level PMax.', 'The price level falls'), None,
           'The scheme grades the whole explanation out of 12; these are the points it lists.'),
     point('r-price', H.opt('The price level falls from the equilibrium level', 'Quantity supplied'), None,
           'A point the scheme lists.'),
     point('r-supply', H.opt('Quantity supplied decreased from the equilibrium', 'Quantity demanded'), None,
           'A point the scheme lists.'),
     point('r-demand', H.opt('Quantity demanded increased from the equilibrium', 'This creates'), None,
           'A point the scheme lists.'),
     point('r-shortage', H.opt('This creates excess demand/shortage', '(ii) Improved'), None,
           'A point the scheme lists.')],
    kind='questionTotal', stem=q1c, figure=q1c_fig, **B)
pick('sb-q1-c-ii', '1-3', 'consequences-of-rent-control', ref('B', 1, '(c)(ii)'),
     H.q(6, 'Outline the possible economic consequences on the Irish rental', ' [20]'),
     'A consequence of rent control — any two',
     H.split('Improved standard of living for consumers.', '13 | P a g e',
             ['Improved standard of living for consumers', 'Excess Demand is created', 'Decrease in number of landlords',
              'Disimproved quality of accommodation', 'Increase in black market activity', 'Increased utility costs']),
     2, 4, 'Two consequences, 4 marks each (2 + 2).', stem=q1c, **B)

# Q2 ─ monopoly
pick('sb-q2-a-i', '2-0', 'characteristics-of-monopoly', ref('B', 2, '(a)(i)'),
     H.q(7, 'Outline three characteristics of a monopoly firm.', ' (ii)'),
     'A characteristic of monopoly — any three',
     H.split('1. The firm is the sole supplier', '(ii) There must be',
             ['The firm is the sole supplier', 'The firm seeks to maximise', 'The firm controls either',
              'High barriers to entry', 'A unique good is sold']),
     3, 5, 'Three characteristics, 5 marks each (2 + 3).', **B)
add('sb-q2-a-ii', '2-0', 'monopoly-power-and-price-discrimination', ref('B', 2, '(a)(ii)'),
    H.q(7, 'Explain why some degree of monopoly power must exist', ' [20]'), '5 (graded)', 5,
    [point('r-1', H.bo('There must be some degree of monopoly/market power', 'more expensive market.', include_end=True), 5,
           'The explanation, 5 marks.' + GRADED)], **B)
header = H.chunk('Price Quantity D=AR MR MC AC Equilibrium P1 Q1 C1 SNPs', ' ⟨').split()
elements = [H.cell('Price axis'), H.cell('Quantity axis'), *header[2:6], H.cell('Equilibrium Point E'), *header[7:]]
explanation = [H.opt(a, b) for a, b in (
    ('Occurs at point E where', '• MC = MR'), ('MC = MR [and MC is rising]', '2. Price/ Output'),
    ('The firm produces Q1', '• and sells'), ('and sells it at P1', '3. Cost'),
    ('The cost is shown at C1 (point Y)', '4. SNP'), ('The firm is earning SNP (P1,C1,Y,X)', '• because'),
    ('because AR > AC or they can continue', '5. Inefficiency'),
    ('The firm is not producing at the lowest point', '• It is thus'),
    ('It is thus inefficient/wasteful of resources.', '(ii) In the monopoly'))]
q2_diagram = SOL + 'p15-q2bi-diagram'
add('sb-q2-b-i', '2-0', 'long-run-equilibrium-of-a-monopoly', ref('B', 2, '(b)(i)'),
    H.q(7, 'Explain, using a clearly labelled diagram, the long‐run equilibrium', ' (ii)'),
    'Diagram 11 @ 1 + explanation 9 @ 1', 20,
    [anyN('r-diagram', 'The diagram — each correctly labelled element', 11, 11, 1, elements,
          'The diagram, 11 marks: 1 for each of the eleven elements the scheme lists. The completed diagram is in '
          'the figure.'),
     anyN('r-explanation', 'The explanation — each point', 9, 9, 1, explanation,
          'The explanation, 9 marks: 1 for each of the nine points, under equilibrium, price and output, cost, '
          'supernormal profit and inefficiency.')],
    kind='fixed', figure=q2_diagram, **B)
add('sb-q2-b-ii', '2-0', 'demand-curve-under-monopoly-and-perfect-competition', ref('B', 2, '(b)(ii)'),
    H.q(7, 'With reference to the diagram you have drawn in part', ' [30]'), '5 + 5 (2 + 3)', 10,
    [point('r-monopoly', H.opt('In the monopoly market structure firms face', 'In the perfectly competitive'), 5,
           'Monopoly, 5 marks (2 + 3).'),
     point('r-perfect', H.opt('In the perfectly competitive market structure firms face', '15 | P a g e'), 5,
           'Perfect competition, 5 marks (2 + 3). The (b)(i) diagram is in the figure.')],
    figure=q2_diagram, **B)
q2c = H.q(7, 'Big Western technology firms such as Apple', ' (Source')
add('sb-q2-c-i', '2-0', 'advantages-of-large-scale-business', ref('B', 2, '(c)(i)'),
    H.q(7, 'State and explain three advantages of large‐scale businesses', ' (ii)'), '1 @ 9, 2 @ 4', 17,
    [anyN('r-1', 'An advantage of large-scale business, with an example — any three', 17, 3, 9,
          H.split('Economies of scale (cost advantages)', 'Example required in each advantage',
                  ['Economies of scale (cost advantages)', 'SNP used for R&D', 'Less waste of scarce resources',
                   'Secure & attractive employment', 'Guaranteed supply', 'Contribution to state finances']),
          'Three advantages: the first 9 marks, the next two 4 each. '
          + H.opt('Example required in each advantage', '(ii) Reduced prices') + '.', steps=[9, 4, 4])],
    kind='fixed', stem=q2c, **B)
pick('sb-q2-c-ii', '1-3', 'regulating-a-monopoly', ref('B', 2, '(c)(ii)'),
     H.q(7, 'Outline the possible effects on a monopoly market structure', ' [25]'),
     'An effect of regulation — any two',
     H.split('Reduced prices – anti-competitive regulation', '16 | P a g e',
             ['Reduced prices', 'Increased quantity/choice', 'Employment levels may be affected', 'Poorer service']),
     2, 4, 'Two effects, 4 marks each.', stem=q2c, **B)

# Q3 ─ elasticity
add('sb-q3-a-i', '1-4', 'price-elasticity-of-demand', ref('B', 3, '(a)(i)'),
    H.q(7, 'Explain the term Price Elasticity of Demand (PED).', ' (ii)'), '5', 5,
    [point('r-1', H.opt('Refers to the responsiveness of quantity demanded', '(ii) Durability'), 5,
           'The definition, 5 marks.')], **B)
add('sb-q3-a-ii', '1-4', 'factors-affecting-ped', ref('B', 3, '(a)(ii)'),
    H.q(7, 'Outline four factors that affect the PED for a good or service', ' [25]'), '2 @ 6, 2 @ 4', 20,
    [anyN('r-1', 'A factor affecting PED, with an example — any four', 20, 4, 6,
          H.split('Durability – the greater the durability', '17 | P a g e',
                  ['Durability –', 'Availability of close substitutes –', 'Cheaper of two complements –',
                   'Time allowed for adjustment', 'Luxury or necessity –', 'Brand loyalty –',
                   'Percentage of total income spent', 'Expectation of future price changes –'], source='blocks'),
          'Four factors: the first two 6 marks each, the next two 4 each. An example is required in each.',
          steps=[6, 6, 4, 4])],
    kind='fixed', **B)
q3b = H.q(7, 'The price elasticity of demand for airline tickets', ' (i)')
add('sb-q3-b-i', '1-4', 'ped-of-business-and-holiday-travellers', ref('B', 3, '(b)(i)'),
    H.q(7, 'Using your knowledge of PED, explain which figure', ' (ii)'), '5 + 5 (2 + 3)', 10,
    [point('r-business', H.opt('- 0.1 relates to business peoples', '- 2.4 relates'), 5,
           'Business travellers, 5 marks (2 + 3).'),
     point('r-holiday', H.opt('- 2.4 relates to holiday-makers', '(ii) Diagram 1'), 5,
           'Holiday-makers, 5 marks (2 + 3).')],
    stem=q3b, **B)
add('sb-q3-b-ii', '1-4', 'elastic-and-inelastic-demand-diagrams', ref('B', 3, '(b)(ii)'),
    H.q(7, 'Explain, with the aid of diagrams, the difference between price elastic', ' (iii)'),
    'Diagrams 2 @ 6 (2 + 2 + 2) + explanations 2 + 2', 16,
    [point('r-diagram-inelastic', H.traced(H.chunk('Diagram 1: Inelastic Demand', ' Diagram 2')), 6,
           'The inelastic demand diagram, 6 marks (2 + 2 + 2). Both completed diagrams are in the figure.'),
     point('r-diagram-elastic', H.traced(H.chunk('Diagram 2: Elastic Demand', ' Diagrams:')), 6,
           'The elastic demand diagram, 6 marks (2 + 2 + 2).'),
     point('r-explain-inelastic', H.opt('Shows a relatively price inelastic demand curve', 'Diagram 2.'), 2,
           'Explaining the inelastic diagram, 2 marks.'),
     point('r-explain-elastic', H.opt('Shows a relatively price elastic demand curve', '18 | P a g e'), 2,
           'Explaining the elastic diagram, 2 marks.')],
    stem=q3b, figure=SOL + 'p18-q3bii-diagrams', **B)
add('sb-q3-b-iii', '1-4', 'ped-and-airline-revenue', ref('B', 3, '(b)(iii)'),
    H.q(7, 'Explain how knowledge of PED is useful when analysing', ' [30]'), '2 @ 2', 4,
    [point('r-inelastic', H.opt('Consumers with a price inelastic demand', 'Consumers with a price elastic'), 2,
           'Inelastic demand, 2 marks.'),
     point('r-elastic', H.opt('Consumers with a price elastic demand', 'Possible responses'), 2,
           'Elastic demand, 2 marks.')],
    stem=q3b, **B)
add('sb-q3-c-i', '1-4', 'cross-price-elasticity-calculation', ref('B', 3, '(c)(i)'),
    H.q(7, 'Assume that when the price of a tablet device was €500', ' (ii)'), 'Calculation 12 + explanation 4', 16,
    [point('r-calculation', H.traced(H.chunk('+ 2.43', '\n').strip()), 12,
           'The cross price elasticity, 12 marks. The scheme sets the working as fractions; the figure shows it as '
           'printed.'),
     point('r-explanation', H.opt('These goods are substitute goods.', '(ii) No. The cross-price'), 4,
           'The relationship between the goods, 4 marks.' + GRADED)],
    figure=SOL + 'p19-q3ci-working', **B)
add('sb-q3-c-ii', '1-4', 'ced-for-complements', ref('B', 3, '(c)(ii)'),
    H.q(7, 'Would you expect a similar CED for a tablet device and a tablet case?', ' [20]'), '4 (graded)', 4,
    [point('r-1', H.bo('No. The cross-price elasticity between these goods', 'would increase.', include_end=True), 4,
           'The answer and its explanation, 4 marks.' + GRADED)], **B)


# Q4 ─ factors of production and costs of production
add('sb-q4-a-i', '1-5', 'distinguishing-cost-and-labour-terms', ref('B', 4, '(a)(i)'),
    H.q(8, 'In the case of any two of the following three pairs', ' (ii)'), '2 @ 6, 2 @ 4', 20,
    [anyN('r-1', 'A term defined — four, for two of the three pairs', 20, 4, 6,
          H.split('(i) Average cost', '(ii) Two factors',
                  ['Average cost', 'Marginal cost', 'Employment rate', 'Participation rate',
                   'Marginal physical product', 'Marginal revenue product']),
          'Both terms of two pairs: the scheme prices the four definitions 2 @ 6 and 2 @ 4 without tying either '
          'price to a pair.', steps=[6, 6, 4, 4])],
    kind='fixed', **B)
pick('sb-q4-a-ii', '2-1', 'factors-influencing-mrp', ref('B', 4, '(a)(ii)'),
     H.q(8, 'Outline two factors which influence the Marginal Revenue Product', ' [30]'),
     'A factor influencing MRP — any two',
     H.split('The productivity / commitment of the factor', '20 | P a g e',
             ['The productivity / commitment of the factor', 'The selling price of the output', 'The Law of Demand -',
              'Quality / Specialised nature', 'Training / Education provided', 'Law of Diminishing Marginal Returns']),
     2, 5, 'Two factors, 5 marks each (2 + 3).', **B)
q4b = ' '.join([H.q(8, 'The table below shows cost data for a firm in equilibrium.', ' Quantity of'),
                H.q(8, 'Show your workings for all calculations.', ' (i)')])
q4b_fig = PAP + 'p08-q4b-table'
for cid, concept, parts, ask, run, marks in (
        ('sb-q4-b-i', 'average-total-cost-from-a-table', '(b)(i)',
         H.q(8, 'Calculate the average total cost of producing the 6th unit', ' (ii)'),
         H.opt('AVC + AFC = ATC\n300 + 100 = 400', '(ii) AVC'), 7),
        ('sb-q4-b-ii', 'total-cost-from-a-table', '(b)(ii)',
         H.q(8, 'Calculate the total cost of producing 2 units of output.', ' (iii)'),
         H.opt('AVC + AFC = ATC x Q = TC\n150 + 300', '(iii) AVC'), 6),
        ('sb-q4-b-iii', 'marginal-cost-from-a-table', '(b)(iii)',
         H.q(8, 'Calculate the marginal cost of increasing output', ' (iv)'),
         H.opt('MC = TC5 – TC4', '(iv) Firm produces'), 3),
        ('sb-q4-b-iv', 'profit-maximising-output', '(b)(iv)',
         H.q(8, 'If the firm maximises profits where marginal revenue', ' [20]'),
         H.opt('Firm produces where MC = MR.', '21 | P a g e'), 4)):
    add(cid, '1-5', concept, ref('B', 4, parts), ask, str(marks), marks,
        [point('r-1', run, marks, f'The answer with its working, {marks} marks.')],
        stem=q4b, figure=q4b_fig, **B)
q4c = H.q(8, 'The jobs market is currently suffering from skills shortages', ' (Source')
pick('sb-q4-c-i', '2-1', 'effects-of-skills-shortages', ref('B', 4, '(c)(i)'),
     H.q(8, 'Explain three economic effects of skills shortages', ' (ii)'),
     'An effect of skills shortages — any three',
     H.split('Upward pressure on wages / demand for courses', '(ii) Open up',
             ['Upward pressure on wages', 'Reduced availability of services', 'Deterioration in quality of services',
              'Increased immigration', 'Less attractive location for FDI', 'Negative impact on productivity']),
     3, 5, 'Three effects, 5 marks each (2 + 3).', stem=q4c, **B)
pick('sb-q4-c-ii', '2-1', 'measures-against-skills-shortages', ref('B', 4, '(c)(ii)'),
     H.q(8, 'Outline measures which the government and / or firms could take', ' [25]'),
     'A measure against skills shortages — any two',
     H.split('Open up the Irish labour market', '22 | P a g e',
             ['Open up the Irish labour market', 'Provide more attractive working conditions', 'Improve access to affordable',
              'Increased student grants', 'Government Initiatives:', 'Government introduction of more apprenticeships']),
     2, 5, 'Two measures, 5 marks each (2 + 3).', stem=q4c, **B)

# Q5 ─ money and banking; the budget surplus and the national debt
q5 = H.q(9, 'The Financial Times estimated that cash costs', ' (Source')
pick('sb-q5-a-i', '3-4', 'characteristics-of-money', ref('B', 5, '(a)(i)'),
     H.q(9, 'State and explain two characteristics of money.', ' (ii)'),
     'A characteristic of money — any two',
     H.split('Durable – money needs', '(ii) ⟨4 @ 5⟩',
             ['Durable –', 'Divisible –', 'Recognisable –', 'Acceptable –', 'Portable –', 'Scarce –', 'Homogenous –']),
     2, 5, 'Two characteristics, 5 marks each (2 + 3).', stem=q5, **B)
lists = (
    ('r-bank-advantage', H.cell('Advantages for the banking industry', upto='industry'),
     ['Reduced need for labour Reduced costs', 'Greater efficiencies Bank processes', 'More profitable Due to']),
    ('r-consumer-advantage', H.traced(H.chunk('Advantages for consumers', ' ⟨')),
     ['Convenience It is less time', 'Less expensive It is less', 'Less crime Stolen', 'Electronic paper trail Makes',
      'International transactions Online']),
    ('r-bank-disadvantage', H.traced(H.chunk('Disadvantages for banking industry', ' Disadvantages for consumers')),
     ['Security risks/hacking Banks need', 'Data protection issues Have', 'Technological issues Banks become',
      'Human Resource / IR issues As workers', 'Costs of initial set-up & maintenance Banks must']),
    ('r-consumer-disadvantage', H.traced(H.chunk('Disadvantages for consumers', '\n')),
     ['Difficulty of use for people', 'Security risks/hacking Consumers need', 'Technological issues Cash based',
      'Possible overspending / impulse buying The convenience']))
add('sb-q5-a-ii', '3-4', 'electronic-money-for-citizens-and-banks', ref('B', 5, '(a)(ii)'),
    H.q(9, 'Outline the possible advantages and disadvantages of using electronic money', ' [30]'), '4 @ 5 (2 + 3)', 20,
    [heading(rid, f'{label} — any one', [H.cell(c) for c in cells], 5,
             f'One from this list, 5 marks (2 + 3). The scheme prints 4 @ 5 beside its four lists.')
     for rid, label, cells in lists],
    kind='fixed', stem=q5, **B)
add('sb-q5-b', '3-3', 'arguments-against-raising-ecb-rates', ref('B', 5, '(b)'),
    H.q(9, 'Given the current state of the Irish economy, outline the possible arguments', ' [20]'),
    '4 @ 4 (2 + 2) + 4', 20,
    [anyN('r-arguments', 'An argument against an increase — any four', 16, 4, 4,
          H.split('Reduced investment.', 'Note: Must link',
                  ['Reduced investment', 'Increased cost of borrowing', 'Increased incentive to save',
                   'Slowing economic growth', 'Rising unemployment', 'Risk of personal bankruptcies']),
          'Four arguments, 4 marks each (2 + 2).'),
     point('r-climate', H.opt('Note: Must link answers to current economic climate', '25 | P a g e'), 4,
           'The scheme prints a further 4 beneath 4 @ 4, beside this note.')],
    kind='fixed', stem=H.q(9, 'The President of the European Central Bank', ' (Source'), **B)
add('sb-q5-c-i', '3-1', 'government-budget-surplus', ref('B', 5, '(c)(i)'),
    H.q(9, 'Define the term government budget surplus.', ' (ii)'), '6', 6,
    [point('r-1', H.opt('A government budget surplus exists when', '(ii) National debt'), 6, 'The definition, 6 marks.')], **B)
add('sb-q5-c-ii', '3-1', 'budget-surplus-and-national-debt', ref('B', 5, '(c)(ii)'),
    H.q(9, 'Outline the possible effect of a government budget surplus', ' (iii)'), '7', 7,
    [point('r-1', H.opt('National debt is the total amount (cumulative)', '(iii) Reduced'), 7, 'The effect, 7 marks.')], **B)
pick('sb-q5-c-iii', '3-1', 'national-debt-and-conflicting-objectives', ref('B', 5, '(c)(iii)'),
     H.q(9, 'Outline how measures to reduce Ireland’s national debt', ' [25]'),
     'A conflict with another objective — any two',
     H.split('Reduced national debt vs economic growth.', '26 | P a g e',
             ['Reduced national debt vs economic growth', 'Reduced national debt vs full employment',
              'Reduced national debt vs improved infrastructure', 'Reduced national debt vs balanced regional',
              'Reduced national debt vs redistribution']),
     2, 6, 'Two conflicts, 6 marks each (3 + 3).', **B)

# Q6 ─ inflation and international competitiveness
q6a = H.q(9, 'The CPI is an example of a composite price index.', ' (i)')
add('sb-q6-a-i', '3-3', 'constructing-a-composite-price-index', ref('B', 6, '(a)(i)'),
    H.q(9, 'Explain the steps involved in constructing a composite price index.', ' (ii)'), '8 (graded)', 8,
    [point(f'r-{i}', text, None, 'The scheme grades the whole explanation out of 8; these are the steps it lists.'
           if i == 1 else 'A step the scheme lists.')
     for i, text in enumerate(bl('(i) • Choose a representative base year', '(ii) The nominal wage'), 1)],
    kind='questionTotal', stem=q6a, **B)
add('sb-q6-a-ii', '3-3', 'nominal-and-real-wages', ref('B', 6, '(a)(ii)'),
    H.q(9, 'Distinguish between the terms nominal wage and real wage.', ' (iii)'), '2 @ 4', 8,
    # The scheme prints a superscript footnote mark after "inflation" (scheme p27,
    # rendered and looked at: "inflation²)"); the text layer flattens it to a digit,
    # which would read as "inflation2". The slice is traced as extracted, then the
    # mark is set back as the superscript it is (the build folds ² to 2 to compare).
    [point('r-nominal', H.opt('The nominal wage is the money wage', 'The real wage is').replace('inflation2)', 'inflation²)'), 4,
           'The nominal wage, 4 marks.'),
     point('r-real', H.opt('The real wage is the money wage adjusted', '(iii) Real wages'), 4, 'The real wage, 4 marks.')],
    stem=q6a, **B)
formula = H.traced(H.chunk('Real wages = Nominal rate - Inflation rate', '\n').strip())
add('sb-q6-a-iii', '3-3', 'real-wage-change-from-cpi', ref('B', 6, '(a)(iii)'),
    H.q(9, 'With reference to the table below, calculate the percentage change in real wages', ' Consumer Price'),
    '9 (graded)', 9,
    [point('r-2014', H.traced(H.chunk('-0.2 – 0.3 = -0.5', '\n').strip()), None,
           f'2014. The scheme grades the three answers together out of 9; its working: {formula}.'),
     point('r-2015', H.traced(H.chunk('1.2 – (-0.3) = 1.5', ' graded').strip()), None, '2015.'),
     point('r-2016', H.traced(H.chunk('1.1 – 0.0 = 1.1', '\n').strip()), None, '2016.')],
    kind='questionTotal', stem=q6a, figure=PAP + 'p09-q6a-table', **B)
add('sb-q6-b-i', '3-3', 'causes-of-inflation', ref('B', 6, '(b)(i)'),
    H.q(9, 'State and explain two causes of inflation.', ' (ii)'), '5 + 5 (2 + 3)', 10,
    [point('r-demand-pull', H.opt('Demand pull inflation occurs when', 'Cost push inflation'), 5,
           'Demand-pull inflation, 5 marks (2 + 3).'),
     point('r-cost-push', H.opt('Cost push inflation occurs when', '27 | P a g e'), 5,
           'Cost-push inflation, 5 marks (2 + 3).')], **B)
pick('sb-q6-b-ii', '3-3', 'effects-of-high-inflation', ref('B', 6, '(b)(ii)'),
     H.q(9, 'Outline three possible economic effects of high inflation', ' (iii)'),
     'An effect of high inflation — any three',
     H.split('Loss of purchasing power/fall in living standards.', '(iii) Current deflation',
             ['Loss of purchasing power', 'Loss of international competitiveness', 'Those on fixed incomes',
              'Saving is discouraged', 'Investment is skewed towards property', 'If tax rates are not indexed',
              'Demand for wage increases']),
     3, 4, 'Three effects, 4 marks each (2 + 2).', **B)
add('sb-q6-b-iii', '3-3', 'deflation-and-growth', ref('B', 6, '(b)(iii)'),
    H.q(9, 'Explain how deflation might, in the short run', ' [30]'), '8 (graded)', 8,
    [point('r-expectation', H.opt('Current deflation may create the expectation', 'Their best response'), None,
           'The scheme grades the whole explanation out of 8; these are the steps it lists.'),
     point('r-postpone', H.opt('Their best response is thus to postpone', 'As aggregate demand'), None, 'A step the scheme lists.'),
     point('r-labour', H.opt('As aggregate demand for goods and services falls', 'As the demand for labour falls'), None,
           'A step the scheme lists.'),
     point('r-growth', H.opt('As the demand for labour falls unemployment arises', '28 | P a g e'), None,
           'A step the scheme lists.')],
    kind='questionTotal', **B)
pick('sb-q6-c', '4-2', 'influences-on-irish-competitiveness', ref('B', 6, '(c)'),
     H.q(9, 'Outline the factors which influence Ireland’s international competitiveness.', ' [20]'),
     'A factor influencing competitiveness — any four',
     H.split('Shortage of available and affordable accommodation', '29 | P a g e',
             ['Shortage of available and affordable accommodation', 'Infrastructure - the delay',
              'Increases in business services costs', 'Brexit uncertainty', 'Increasing wage levels',
              'Productivity of the indigenous enterprises', 'Foreign direct investment.', 'Climate action.']),
     4, 5, 'Four factors, 5 marks each (2 + 3).',
     stem=H.q(9, 'National competitiveness is the ability of enterprises', ' (Source'), **B)

# Q7 ─ national income
pick('sb-q7-a-i', '3-0', 'uses-of-national-income-statistics', ref('B', 7, '(a)(i)'),
     H.q(10, 'State and explain the uses of national income statistics.', ' (ii)'),
     'A use of national income statistics — any two',
     H.split('Indication of alterations in standard of living.', 'Population changes.',
             ['Indication of alterations in standard of living', 'Means of comparing the standard of living',
              'Assists the government in formulating', 'Evaluate economic policy', 'EU Budget Contributions']),
     2, 7, 'Two uses, 7 marks each.' + GRADED, **B)
pick('sb-q7-a-ii', '3-0', 'limitations-of-gdp', ref('B', 7, '(a)(ii)'),
     H.q(10, 'Outline the limitations of using GDP as a measure', ' [30]'),
     'A limitation of GDP — any two',
     H.split('Population changes.', '31 | P a g e',
             ['Population changes', 'Inflation/deflation', 'Employment / Unemployment', 'Levels of taxation',
              'Exclusion of important activities', 'Hidden social costs', 'Distribution of national income',
              'Nature of the goods produced', 'Government services at cost price']),
     2, 8, 'Two limitations, 8 marks each.' + GRADED, **B)
q7b = ' '.join([H.q(10, 'Use the information in the table to answer the questions below.', ' Marginal'),
                H.q(10, 'Show your workings for all calculations.', ' (i)')])
q7b_fig = PAP + 'p10-q7b-table'
add('sb-q7-b-i', '3-0', 'marginal-propensity-to-consume', ref('B', 7, '(b)(i)'),
    H.q(10, 'Define marginal propensity to consume (MPC).', ' (ii)'), '5', 5,
    [point('r-1', H.opt('Marginal propensity to consume refers to', '(ii) MPS'), 5, 'The definition, 5 marks.')],
    stem=q7b, figure=q7b_fig, **B)
add('sb-q7-b-ii', '3-0', 'marginal-propensity-to-save', ref('B', 7, '(b)(ii)'),
    H.q(10, 'Calculate the marginal propensity to save (MPS).', ' (iii)'), '5', 5,
    [point('r-1', H.opt('MPS = 1 – MPC', '(iii) 1'), 5, 'The answer with its working, 5 marks.')],
    stem=q7b, figure=q7b_fig, **B)
add('sb-q7-b-iii', '3-0', 'open-economy-multiplier', ref('B', 7, '(b)(iii)'),
    H.q(10, 'Calculate the value of the multiplier in this open economy', ' (iv)'), 'Calculation 5 + explanation 4', 9,
    [point('r-calculation', H.traced(H.chunk('1.25', ' ', occ=0)), 5,
           'The multiplier, 5 marks. The scheme sets both workings as fractions; the figure shows them as printed.'),
     point('r-explanation', H.bo('Any injection into the circular flow of income', 'initial injection.', include_end=True), 4,
           'Its meaning, 4 marks.')],
    stem=q7b, figure=SOL + 'p32-q7biii-working', **B)
show_before_reveal(cards[-1], None, PAP + 'p10-q7b-question')
add('sb-q7-b-iv', '3-0', 'injection-to-reach-full-employment', ref('B', 7, '(b)(iv)'),
    H.q(10, 'Calculate the size of the injection required', ' [25]'), '6', 6,
    [point('r-1', H.traced(H.chunk('150bn – 100bn', ' ⟨6⟩')), 6, 'The answer with its working, 6 marks.')],
    stem=q7b, figure=q7b_fig, **B)
q7c = H.q(10, 'In 2017, the Office of the Revenue Commissioners seized', ' (Source')
add('sb-q7-c-i', '3-0', 'the-shadow-economy', ref('B', 7, '(c)(i)'),
    H.q(10, 'Explain what is meant by the economic term shadow economy.', ' (ii)'), '5', 5,
    [point('r-1', H.opt('The shadow economy refers to all economic activity', '(ii) 1. Loss'), 5, 'The definition, 5 marks.')],
    stem=q7c, **B)
pick('sb-q7-c-ii', '3-0', 'effects-of-the-shadow-economy', ref('B', 7, '(c)(ii)'),
     H.q(10, 'Outline the economic effects for Ireland of increased activity', ' [20]'),
     'An effect of the shadow economy — any three',
     H.split('1. Loss of tax revenue to the government', '32 | P a g e',
             ['Loss of tax revenue', 'Decline in legitimate business activity',
              'Increased government expenditure on enforcement', 'Increase crime levels', 'Standards of products/services']),
     3, 5, 'Three effects, 5 marks each (2 + 3).', stem=q7c, **B)

# Q8 ─ government objectives and fiscal policy
q8 = H.q(11, 'Budget 2019 failed to increase carbon taxes.', ' (a)')
add('sb-q8-a-i', '3-1', 'progressive-and-regressive-taxes', ref('B', 8, '(a)(i)'),
    H.q(11, 'Explain the terms progressive tax and regressive tax', ' (ii)'), '5 + 5 (4 + 1)', 10,
    [point('r-progressive', H.opt('A progressive tax takes a higher proportion', 'A regressive tax takes'), 5,
           'A progressive tax with its example, 5 marks (4 + 1).'),
     point('r-regressive', H.opt('A regressive tax takes a higher proportion', '(ii) Yes, because'), 5,
           'A regressive tax with its example, 5 marks (4 + 1).')],
    stem=q8, **B)
q8aii = H.q(11, 'In your opinion, did the government make the correct decision', ' [25]')
for word, start, end, firsts in (
        ('yes', 'Yes, because it wasn’t needed', 'or\nNo, because',
         ['Yes, because it wasn’t needed', 'It tends to be regressive', 'The poorest households spend',
          'The carbon tax would add to business costs', 'The carbon tax would have a detrimental',
          'Firms should be allowed time', 'Carbon taxes may be considered as anti-rural']),
        ('no', 'No, because the fuels', '33 | P a g e',
         ['No, because the fuels', 'The government is failing to meet', 'It would also generate additional revenue',
          'It would encourage businesses and households'])):
    pick(f'sb-q8-a-ii-{word}', '3-1', 'carbon-tax-in-budget-2019', ref('B', 8, '(a)(ii)', word),
         f'{q8aii} Justify the choice: {word.upper()}.', f'A reason for answering {word.upper()} — any three',
         H.split(start, end, firsts),
         3, 5, f'Three developed reasons, 5 marks each (2 + 3). The scheme credits YES and NO, each with its own list.',
         stem=q8, **B)
q8b = H.q(11, 'The key message from the Irish Fiscal Advisory Council', ' (Source')
pick('sb-q8-b-i', '3-1', 'effects-of-government-overspending', ref('B', 8, '(b)(i)'),
     H.q(11, 'Outline the possible negative economic effects of the government’s repeated overspending.', ' (ii)'),
     'A negative effect of overspending — any three',
     H.split('Running the risk of future budget deficits.', '(ii) Loss of FDI',
             ['Running the risk of future budget deficits', 'Running the risk of accumulating additional debt',
              'Uncertainty and lack of credibility', 'Deterioration in quality of service provision',
              'Damage to Ireland’s international reputation']),
     3, 5, 'Three effects, 5 marks each (2 + 3).', stem=q8b, **B)
pick('sb-q8-b-ii', '3-1', 'raising-corporation-tax', ref('B', 8, '(b)(ii)'),
     H.q(11, 'Ireland’s corporation tax rate of 12.5%', ' [30]'),
     'An effect of raising corporation tax — any three',
     H.split('Loss of FDI / difficulty in attracting new FDI.', '34 | P a g e',
             ['Loss of FDI', 'Loss of employment', 'Effects on government revenue', 'Equitable taxation system']),
     3, 5, 'Three effects, 5 marks each (2 + 3).', stem=q8b, **B)
q8c = H.q(11, 'Social Justice Ireland’s Poverty Focus 2018 report', ' (Source')
add('sb-q8-c-i', '3-1', 'a-just-social-policy', ref('B', 8, '(c)(i)'),
    H.q(11, 'One of the government’s objectives is to achieve a just social policy.', ' (ii)'), '6 (graded)', 6,
    [point('r-1', H.opt('A just social policy refers to', '(ii) Increased minimum wage'), 6,
           'The explanation, 6 marks.' + GRADED)],
    stem=q8c, **B)
pick('sb-q8-c-ii', '3-1', 'measures-for-the-working-poor', ref('B', 8, '(c)(ii)'),
     H.q(11, 'Outline measures which the government and/or firms could consider', ' [20]'),
     'A measure for the working poor — any two',
     H.split('Increased minimum wage.', '35 | P a g e',
             ['Increased minimum wage', 'Tackle issues such as cost of housing', 'Alterations to the tax structure',
              'Reduce public transport costs', 'Means testing', 'Increase social welfare payments',
              'Legislation on work contacts', 'Firms could subsidise workers']),
     2, 7, 'Two measures, 7 marks each (4 + 3).', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
