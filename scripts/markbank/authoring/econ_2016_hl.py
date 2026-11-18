#!/usr/bin/env python3
"""Economics 2016 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2016-hl-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2016
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The scheme reprints each question above its answer, so a
slice always starts after the reprinted wording. The only prose written here is
guidance: tariffs, route labels and what a figure or a calculation shows.

The scheme marks the items of three workings with a raised numeral or a star
beside each ("+ 100 1 x 1 €57,000 1 ...", "1*/0.2* +* 0.2*", "€620m 2 - €500m 2").
A row claims each marked figure, sliced short of its numeral, and the hidden
solution figure shows the working as printed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2016, 'higher', 'LC034ALP000EV')
D = OldDeck(2016, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2016-HL-scheme-'
PAP = 'economics-2016-HL-paper-'
bl = H.bullets
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it:
    "<heading> — <response>". Both halves trace."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def unpriced(pairs):
    """questionTotal rows: the scheme prices them as one total and splits nothing."""
    return [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate(pairs, 1)]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ perfect competition in the short run
q1 = H.q(2, 'The diagram below shows a firm operating under conditions of perfect competition', ' 1 Price')
q1_fig = PAP + 'p02-q1-diagram'
add('sa-q1-a', '2-0', 'labels-of-short-run-perfect-competition', ref('A', 1, '(a)'),
    H.q(2, 'What is represented by the lines numbered 1 to 3?', ' 2 Number'), '3 x 3', 9,
    [point(f'r-{n}', f'{n} — {H.traced(label)}', 3, f'Line {n}, 3 marks.')
     for n, label in ((1, 'Marginal cost'), (2, 'Average costs'), (3, 'Average Revenue / Marginal Revenue / Demand'))],
    stem=q1, figure=q1_fig, **A)
q1bi = H.q(2, 'Show clearly on the diagram the total supernormal profit of the firm.', ' (ii)')
add('sa-q1-b-i', '2-0', 'showing-supernormal-profit', ref('A', 1, '(b)(i)'), q1bi, '3', 3,
    [ask_row('r-1', q1bi, 3, 'The supernormal profit shaded, 3 marks. The scheme shades it on its diagram ('
             + H.traced('Shaded region above') + '); the figure shows it.')],
    stem=q1, figure=SOL + 'p05-q1-diagram', **A)
beside_ask(cards[-1], q1_fig)
add('sa-q1-b-ii', '2-0', 'supernormal-profit', ref('A', 1, '(b)(ii)'), H.q(2, 'Explain the term supernormal profit', ' (16 marks)'),
    '4', 4, [point('r-1', H.traced('It is any profit earned in excess of normal profit (part of the AC). (It arises when AR is greater than AC).'),
                   4, 'The explanation, 4 marks.')], stem=q1, **A)

# Q2 ─ the law of diminishing marginal returns
add('sa-q2', '1-5', 'the-law-of-diminishing-marginal-returns', ref('A', 2),
    H.q(2, 'Define the Law of Diminishing Marginal Returns and illustrate', ' Definition'), '10 + 6', 16,
    [point('r-definition', H.opt('The Law of Diminishing Marginal Returns states', '10 marks'), 10, 'The definition, 10 marks.'),
     point('r-example', H.traced('Any suitable example explained'), 6,
           'The example, 6 marks. The scheme prints no example: any suitable one, explained.')], **A)

# Q3 ─ the mobility of labour
pick('sa-q3', '2-1', 'improving-labour-mobility', ref('A', 3),
     H.q(2, 'Outline two ways the Irish government could improve the mobility of labour', ' (i)'), 'A way — any two',
     side('Occupational mobility', bl('• Provide retraining programmes', 'Geographical mobility'))
     + side('Geographical mobility', bl('• Government could offer relocation subsidies', '2 x 8 marks each')),
     2, 8, 'Two ways, 8 marks each.', **A)

# Q4 ─ economies of scale in the aircraft industry
add('sa-q4', '1-5', 'economies-of-scale-in-aircraft', ref('A', 4),
    H.q(3, 'Firms within the aircraft industry can benefit from economies of scale.', ' Explanation'), '10 + 6', 16,
    [point('r-explanation', H.opt('These result in a reduction in the LRAC of production', '10 marks'), 10, 'The explanation, 10 marks.'),
     heading('r-example', 'An example — any one', bl('• Technical economies', 'Example must refer'), 6,
             'One example, 6 marks. ' + H.traced('Example must refer to the aircraft/airline industry') + '.')],
    kind='fixed', **A)

# Q5 ─ youth unemployment
pick('sa-q5-a', '3-2', 'effects-of-youth-unemployment', ref('A', 5, '(a)'),
     H.q(3, 'Outline two possible effects on the Irish economy of high levels of youth unemployment.', ' (i)'), 'An effect — any two',
     bl('• Increase government expenditure', '2 x 5 marks each (2 + 3)'), 2, 5, 'Two effects, 5 marks each (2 + 3).', **A)
pick('sa-q5-b', '3-2', 'reducing-youth-unemployment', ref('A', 5, '(b)'),
     H.q(3, 'State one economic policy the government could introduce to reduce youth unemployment.', ' (16 marks)'),
     'A policy — any one', bl('• Reduce minimum wage for younger workers', 'One policy 6 marks'), 1, 6, 'One policy, 6 marks.', **A)

# Q6 ─ income elasticity of demand
q6 = H.q(3, 'The table below shows the annual average level of income', ' (i)')
items = [H.traced(x) for x in ('+ 100', 'x', '€57,000', '€63,000', '+ €6,000', '100', '200', '+', '6.67')]
add('sa-q6-i', '1-4', 'calculating-income-elasticity', ref('A', 6, '(i)'),
    H.q(3, 'Calculate the income elasticity of demand (YED) for Product A.', ' Workings:'), '9 x 1', 9,
    [anyN('r-1', 'Each item the scheme marks', 9, 9, 1, items,
          'The working and answer, 9 marks: 1 for each item the scheme marks with a raised 1. They are the change in quantity '
          '+100, the times sign, the incomes €57,000 and €63,000, the change in income +€6,000, the quantities 100 and 200, '
          'and the answer’s + sign and its 6.67. The figure shows the working as printed.')],
    kind='fixed', stem=q6, figure=SOL + 'p08-q6i-working', **A)
add('sa-q6-ii', '1-4', 'what-the-income-elasticity-means', ref('A', 6, '(ii)'),
    H.q(3, 'Using your knowledge of YED, explain the economic meaning', ' ____'), '4 + 4', 8,
    [point('r-sign', '+ sign — ' + H.traced('This is a normal good'), 4, 'The + sign, 4 marks.'),
     point('r-size', '6.67 — ' + H.traced('This is a luxury good as the good is income elastic (>1) The percentage increase in quantity '
                                         'demanded is greater than the percentage increase in income/ As income rises, consumers '
                                         'spend proportionally more on the good.'), 4, 'The size, 6.67, 4 marks.')],
    stem=q6, **A)

# Q7 ─ monetary policy and price stability
q7 = H.q(4, 'The primary aim of the ECBs monetary policy is to maintain price stability.', ' (a)')
add('sa-q7-a', '3-3', 'monetary-policy', ref('A', 7, '(a)'), H.q(4, 'Define the term monetary policy.', ' (b)'), '3 + 3 + 3', 9,
    [point('r-money', H.traced('those actions by the ECB, which influence the money supply'), 3, '3 marks, printed after the money supply.'),
     point('r-interest', H.traced('interest rates'), 3, '3 marks, printed after interest rates.'),
     point('r-credit', H.traced('or the availability of credit'), 3, '3 marks, printed after the availability of credit.')],
    stem=q7, **A)
pick('sa-q7-b', '3-3', 'benefits-of-price-stability', ref('A', 7, '(b)'),
     H.q(4, 'Outline two benefits of price stability for the Irish economy.', ' (i)'), 'A benefit — any two',
     bl('• Maintain value of money', '2 benefits x 4 marks each'), 2, 4, 'Two benefits, 4 marks each.', stem=q7, **A)

# Q8 ─ a levy on home insurance; the flooding crisis
add('sa-q8', '1-3', 'a-flood-levy-and-alternatives', ref('A', 8, '(a)–(b)'),
    ' '.join([H.q(4, 'Outline two possible economic effects of the Irish government introducing a levy', ' (i)'),
              H.q(4, 'Suggest one alternative method for addressing the flooding crisis in Ireland.', ' (17 marks)')]),
    '7 + 5 + 5', 17,
    [anyN('r-1', 'Two effects of the levy and one alternative method', 17, 3, 7,
          side('(a) Outline two possible economic effects', bl('• Increase in cost of insurance for householders', '(b) Suggest one'))
          + side('(b) Suggest one alternative method', bl('• Investment by the government in improved flood', '7 marks (4+3)')),
          'Two effects for (a) and one method for (b). The scheme prices the three on one ladder, not by part: the first '
          'correct response 7 marks (4 + 3), the other two 5 each (3 + 2).', steps=[7, 5, 5])],
    kind='fixed', **A)

# Q9 ─ the national minimum wage
add('sa-q9', '2-1', 'raising-the-minimum-wage', ref('A', 9),
    H.q(4, 'Outline three possible economic impacts of this measure on the Irish economy.', ' (i)'), '7 + 5 + 5', 17,
    [anyN('r-1', 'An impact — any three', 17, 3, 7,
          side('Positive impacts', bl('• Higher standard of living for low income families', 'Negative impacts:'))
          + side('Negative impacts', bl('• Price of goods may increase as input costs', 'Any 3 impacts')),
          'Three impacts, positive or negative: the first correct 7 marks (4 + 3), the other two 5 each (3 + 2).',
          steps=[7, 5, 5])],
    kind='fixed', stem=H.q(4, '“The national minimum wage is increased by 50 cent', ' Outline'), **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ supply; elasticity; a concert ticket shortage
pick('sb-q1-a-i', '1-2', 'what-determines-supply', ref('B', 1, '(a)(i)'),
     H.q(5, 'Outline four factors that determine the supply of a good or service.', ' (ii)'), 'A factor — any four',
     bl('• Price of the good itself', '4 x 5 marks.'), 4, 5,
     'Four factors, 5 marks each: ' + H.traced('State: 2 marks. Explain: 3 marks.') + ' The scheme names the factors only.', **B)
add('sb-q1-a-ii', '1-2', 'movements-along-and-shifts-in-supply', ref('B', 1, '(a)(ii)'),
    H.q(5, 'Explain the difference between a movement along a supply curve', ' [35]'), '3 + 5 + 2 + 5', 15,
    [point('r-move-diagram', 'Diagram — ' + H.traced('Movement along a supply curve'), 3,
           'The diagram of a movement along the supply curve, 3 marks. The figure shows the scheme’s two diagrams.'),
     point('r-move', cc('A change in the selling price of the good itself'), 5, 'The movement explained, 5 marks.'),
     point('r-shift-diagram', 'Diagram — ' + H.traced('Shift in a supply curve.'), 2, 'The diagram of a shift in the supply curve, 2 marks.'),
     point('r-shift', cc('A change in any of the factors other than price'), 5, 'The shift explained, 5 marks.')],
    figure=SOL + 'p11-q1aii-diagrams', **B)
q1b = H.q(5, 'Read the following statements and indicate if they are TRUE or FALSE.', ' (i)')
for part, concept, ask, nxt, answer, start, end in (
        ('i', 'cross-price-elasticity-of-substitutes', 'The cross price elasticity of demand for substitute goods', ' (ii)', 'FALSE',
         'The cross price elasticity of demand for substitute goods is positive', '(ii) PED tends'),
        ('ii', 'price-elasticity-over-time', 'Price Elasticity of Demand (PED) tends to be more elastic', ' (iii)', 'TRUE',
         'In general, for many goods, demand is more elastic', '(iii) When demand'),
        ('iii', 'inelastic-demand-and-revenue', 'When demand for a good is price inelastic', ' (iv)', 'FALSE',
         'If demand is inelastic it means that buyers', '(iv) Income elasticity'),
        ('iv', 'income-elasticity-of-luxuries', 'Income elasticity of demand (YED) for luxury goods is positive.', ' [24]', 'TRUE',
         'As income rises consumers spend proportionately', 'True / False:')):
    add(f'sb-q1-b-{part}', '1-4', concept, ref('B', 1, f'(b)({part})'), H.q(5, ask, nxt), '2 + 4', 6,
        [point('r-answer', H.traced(answer), 2, f'{answer}, 2 marks.'),
         point('r-explanation', H.opt(start, end), 4, 'The explanation, 4 marks.')],
        stem=q1b, **B)
q1c = H.q(5, 'Using the concepts of demand and supply explain', ' The concert')
add('sb-q1-c', '1-0', 'a-concert-ticket-shortage', ref('B', 1, '(c)'), H.q(5, 'Using the concepts of demand and supply explain', ' [16]'),
    '12 + 4', 16,
    [ask_row('r-diagram', 'with the aid of a labelled diagram', 12,
             'The labelled diagram, 12 marks: the figure shows the scheme’s, a vertical supply curve at 30,000 and excess demand at P2.'),
     point('r-explanation', H.opt('Supply of concert tickets is fixed regardless of the price.', '4 marks'), 4, 'The explanation, 4 marks.')],
    figure=SOL + 'p13-q1c-diagram', **B)

# Q2 ─ oligopoly; a new entrant; small and large firms
q2 = H.q(5, 'Cadbury, Mars and Nestlé dominate the chocolate industry', ' (a)')
add('sb-q2-a-i', '2-0', 'naming-the-market-structure', ref('B', 2, '(a)(i)'),
    H.q(5, 'State a market structure which most closely reflects the situation above', ' (ii)'), '7', 7,
    unpriced([(H.traced('Oligopoly'), 'The scheme prices the structure and its reason 7 together and does not say which earns which.'),
              (H.opt('The industry is dominated / controlled by a small number of firms', '7marks'), 'Claim the complete answer: 7 marks in all.')]),
    kind='questionTotal', stem=q2, **B)
pick('sb-q2-a-ii', '2-0', 'characteristics-of-oligopoly', ref('B', 2, '(a)(ii)'),
     H.q(5, 'Outline two other key characteristics of this market structure.', ' (iii)'), 'A characteristic — any two',
     H.split('Mutual interdependence between firms', '2 x 5 marks (2+3)',
             ['Mutual interdependence', 'Product differentiation', 'Brand proliferation', 'Barriers to entry', 'Collusion may occur',
              'Non-price competition', 'Firms may pursue objectives']),
     2, 5, 'Two characteristics, 5 marks each (2 + 3).', stem=q2, **B)
add('sb-q2-a-iii', '2-0', 'the-kinked-demand-curve', ref('B', 2, '(a)(iii)'),
    H.q(5, 'Explain, with the aid of a labelled diagram, the likely shape of the demand curve', ' [35]'), '5 + 3 + 5 + 5', 18,
    [point('r-diagram', H.traced('Diagram: P, Q, AB, BC, P1'), 5, 'The diagram, 5 marks: 1 for each of P, Q, AB, BC and P1.'),
     point('r-overall', f"{H.traced('Overall D/C')} — {H.traced('The overall demand curve is ABC, kinked at point B.')}", 3,
           'The overall curve, 3 marks.'),
     point('r-ab', f"{H.traced('Demand curve - AB')} — {H.opt('This portion of the D/C is elastic.', '5 marks')}", 5, 'AB, 5 marks.'),
     point('r-bc', f"{H.traced('Demand curve – BC')} — {H.opt('This portion of the D/C is inelastic.', '5 marks')}", 5, 'BC, 5 marks.')],
    stem=q2, figure=SOL + 'p15-q2aiii-diagram', **B)
pick('sb-q2-b-i', '2-0', 'a-new-entrant-and-competition', ref('B', 2, '(b)(i)'),
     H.q(5, 'If a large US chocolate manufacturer entered the EU chocolate market', ' (ii)'), 'An impact — any three',
     H.split('Lower prices for consumers\nIncreased', '3 x 5 marks (2+3)',
             ['Lower prices for consumers', 'More choice for consumers', 'Better quality product', 'More innovation',
              'Better use of scare resources']),
     3, 5, 'Three impacts, 5 marks each (2 + 3).', stem=q2, **B)
pick('sb-q2-b-ii', '2-0', 'barriers-for-a-new-entrant', ref('B', 2, '(b)(ii)'),
     H.q(5, 'Outline two factors which could make it difficult for this US chocolate manufacturer', ' [25]'), 'A factor — any two',
     H.split('Existence of trade agreements / EU import tariffs', '2 x 5 marks (2+3)',
             ['Existence of trade agreements', 'Brand loyalty of existing customers', 'Economies of scale in the European market',
              'Knowledge and expertise', 'Transport costs']),
     2, 5, 'Two factors, 5 marks each (2 + 3).', stem=q2, **B)
pick('sb-q2-c', '2-0', 'small-and-large-firms', ref('B', 2, '(c)'),
     H.q(5, 'Explain why small firms succeed in some markets', ' [15]'), 'A reason — any three',
     side('Why small firms succeed in some markets',
          H.split('Personal service\nSmall firms', 'Why some markets are dominated by large firms:',
                  ['Personal service', 'Size of market doesn’t justify', 'Government assistance for small firms', 'Consumer loyalty',
                   'Viable community', 'Niche markets/traditional markets', 'Nature of product']))
     + side('Why some markets are dominated by large firms',
            H.split('Existence of economies of scale\nLarger', '3 x 5 marks (2+3)',
                    ['Existence of economies of scale', 'Existence of barriers to entry', 'Advertising', 'Product differentiation',
                     'Brand Proliferation'])),
     3, 5, 'Three reasons, 5 marks each (2 + 3), for small firms, large firms or both.', **B)

# Q3 ─ labour terms; the supply of labour; wage differences
q3a_terms = (('Participation rate', '• The proportion of the active age group', '(ii) Real wages'),
             ('Real wages', '• The purchasing power of wages', '(iii) Labour Productivity'),
             ('Labour Productivity', '• The output per worker per period', '(iv) Derived demand'),
             ('Derived demand', '• Firms do not demand labour', '1st correct response'))
add('sb-q3-a', '2-1', 'terms-of-the-labour-market', ref('B', 3, '(a)(i)–(iv)'),
    H.q(6, 'Explain the following terms in relation to the factor of production labour.', ' [20]'), '8 + 4 + 4 + 4', 20,
    [anyN('r-1', 'Each term explained', 20, 4, 8,
          [o for term, start, end in q3a_terms for o in side(term, bl(start, end))],
          'One explanation for each of the four terms. The scheme prices them on one ladder, not by term: the '
          '1st correct response 8 marks, the 2nd, 3rd and 4th 4 each.', steps=[8, 4, 4, 4])],
    kind='fixed', **B)
q3b = H.q(6, 'Discuss the factors that impact on the supply of labour.', ' (ii)')
pick('sb-q3-b-i', '2-1', 'the-supply-of-labour', ref('B', 3, '(b)(i)'), q3b, 'A factor — any four',
     H.split('The average number of hours worked per week', '4 x 5 marks (2+3)',
             ['The average number of hours worked', 'High marginal tax rates', 'Government regulation / policies',
              'Participation Rate The proportion', 'Labour mobility', 'Migration levels']),
     4, 5, 'Four factors, 5 marks each (2 + 3).', **B)
challenges = (side('Excess supply of labour', H.cut_cell('Excess supply of labour Different segments',
                                                          ['Different segments of the labour market', 'Currently Ireland is experiencing',
                                                           'Those in long term unemployment']))
              + side('Excess demand for labour', H.cut_cell('Excess demand for labour Possible labour shortages',
                                                            ['Possible labour shortages', 'Wage demands.', 'Shortages exist in the health'])))
policies = (side('Excess supply of labour', H.cut_cell('Provision of (re) training where skill shortages',
                                                        ['Provision of (re) training', 'Help people search for jobs', 'Employ workers directly',
                                                         'Subsidise private sector employment']))
            + side('Excess demand for labour', H.cut_cell('Open up the Irish labour market',
                                                          ['Open up the Irish labour market', 'Encourage emigrants to return home',
                                                           'Provide more attractive working conditions'])))
add('sb-q3-b-ii', '2-1', 'labour-market-challenges-and-policy', ref('B', 3, '(b)(ii)'),
    H.q(6, 'Outline two challenges currently facing the Irish labour market', ' [35]'), '4 + 3 & 4 + 4', 15,
    [anyN('r-challenges', 'A challenge — any two', 7, 2, 4, challenges,
          'Two challenges, ' + H.traced('(4+3) = 7 marks') + ': the first 4, the second 3.', steps=[4, 3]),
     anyN('r-policies', 'A policy response for each challenge — any two', 8, 2, 4, policies,
          'One policy for each challenge, ' + H.traced('(4+4) = 8 marks') + '.')],
    kind='fixed', **B)
pick('sb-q3-c', '2-1', 'why-wages-differ', ref('B', 3, '(c)'),
     H.q(6, 'Discuss reasons why different workers are paid different wage rates.', ' [20]'), 'A reason — any four',
     H.split('Productivity of worker', '4 x 5 marks (2+3)',
             ['Productivity of worker', 'Different skills / degree', 'Length of training involved', 'Educational qualifications',
              'Nature / conditions / risk', 'Negotiating strength', 'Regulation / tradition', 'Possession of innate talents', 'Gender Bias']),
     4, 5, 'Four reasons, 5 marks each (2 + 3).', **B)

# Q4 ─ production periods; marginal revenue and cost; competitiveness
add('sb-q4-a-i', '1-5', 'the-short-run-and-the-long-run', ref('B', 4, '(a)(i)'),
    H.q(6, 'Distinguish between the short-run and the long-run production periods.', ' (ii)'), '5 + 5', 10,
    [point('r-short', H.traced('In the short run production period at least one factor of production/input is fixed and cannot be varied'), 5,
           'The short run, 5 marks (the scheme’s 10 marks (5+5)).'),
     point('r-long', H.traced('while in the long run all factors of production /inputs are variable.'), 5, 'The long run, 5 marks.')], **B)
add('sb-q4-a-ii', '1-5', 'staying-in-at-a-loss', ref('B', 4, '(a)(ii)'),
    H.q(6, 'In the short-run firms may stay in the industry even if they are making a loss.', ' [15]'), '5', 5,
    [point('r-1', H.opt('If a firm’s total revenue is greater than its total variable costs', '5 marks'), 5, 'The explanation, 5 marks.')], **B)
q4b = H.q(6, 'The table below shows costs and revenue data of a firm.', ' Output')
q4b_table = PAP + 'p06-q4b-table'
add('sb-q4-b-i', '1-5', 'marginal-revenue-and-marginal-cost', ref('B', 4, '(b)(i)'),
    H.q(6, 'Explain the terms marginal revenue and marginal cost.', ' The table'), '2 x 5', 10,
    [point('r-mr', H.traced('Marginal revenue is the addition to total revenue as a result of producing one extra unit of output.'), 5,
           'Marginal revenue, 5 marks.'),
     point('r-mc', H.traced('Marginal cost is the addition to total cost of producing an extra unit of output.'), 5, 'Marginal cost, 5 marks.')],
    **B)
col = lambda run: ', '.join(H.traced(x) for x in run)
mr = ('40 - 20 = 20', '60 - 40 = 20', '80 - 60 = 20', '100 – 80 = 20')
mc = ('60 – 42 = 18', '77 – 60 = 17', '97 – 77 = 20', '130 – 97 = 33')
H.traced(' '.join(mr)), H.traced(' '.join(mc))   # each column is printed as one run
add('sb-q4-b-ii', '1-5', 'calculating-mr-and-mc', ref('B', 4, '(b)(ii)'),
    H.q(6, 'Calculate the marginal revenue and marginal cost at each output level.', ' (iii)'), '4 + 4', 8,
    [point('r-mr', f'MR — {col(mr)}', 4, H.traced('Calculation of MR: 4 marks.') + ' Outputs 2 to 5.'),
     point('r-mc', f'MC — {col(mc)}', 4, H.traced('Calculation of MC: 4 marks.') + ' The figure shows the scheme’s table.')],
    stem=q4b, figure=SOL + 'p22-q4bii-table', **B)
beside_ask(cards[-1], q4b_table)
add('sb-q4-b-iii', '1-5', 'graphing-profit-maximisation', ref('B', 4, '(b)(iii)'),
    H.q(6, 'Draw one graph showing the marginal revenue and marginal cost', ' [30]'), '5 + 3 + 4', 12,
    [anyN('r-graph', 'The graph — each element', 5, 5, 1,
          [H.traced(x) for x in ('Price', 'Quantity', 'MR', 'MC', 'Identify profit max. output')],
          'The graph, 5 marks: 1 for each element the scheme lists. The figure shows its graph.'),
     point('r-output', H.traced('Profit-maximising level of output: 4 units of output: where MC = MR'), 3, 'The output, 3 marks.'),
     point('r-explanation', H.opt('If more than 4 units are produced', '4 marks'), 4, 'The explanation, 4 marks.')],
    kind='fixed', stem=q4b, figure=SOL + 'p22-q4biii-graph', **B)
beside_ask(cards[-1], q4b_table)
q4c = H.q(6, '“Overall Ireland’s improving competitiveness performance', ' (i)')
pick('sb-q4-c-i', '4-2', 'what-drives-competitiveness', ref('B', 4, '(c)(i)'),
     H.q(6, 'Outline the factors that influence the competitiveness of firms in Ireland.', ' (ii)'), 'A factor — any three',
     H.split('Wage costs\nHigh labour', '3 x 5 marks (2+3)',
             ['Wage costs', 'Cost of doing business', 'Tax rates / increases', 'Inadequate infrastructure', 'Regulation (ease of doing',
              'Inflation rates', 'State of Technology', 'Research and Development', 'Changing value of the Euro']),
     3, 5, 'Three factors, 5 marks each (2 + 3).', stem=q4c, **B)
pick('sb-q4-c-ii', '4-2', 'improving-competitiveness', ref('B', 4, '(c)(ii)'),
     H.q(6, 'Discuss three policies that the Irish government could consider', ' [30]'), 'A policy — any three',
     H.split('Wage restraint\nThe government', '3 x 5 marks (2+3)',
             ['Wage restraint', 'Reduce taxation', 'Reduce utility charges', 'Improve the infrastructure', 'Reduce bureaucracy',
              'Subsidies to firms', 'Funding skills', 'Encourage competition in the market']),
     3, 5, 'Three policies, 5 marks each (2 + 3).', stem=q4c, **B)

# Q5 ─ full employment; the multiplier; GDP
add('sb-q5-a-i', '3-2', 'full-employment', ref('B', 5, '(a)(i)'), H.q(7, 'Define the term full employment.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('When everyone who seeks work can find work at existing wage levels/at the going market wage level.'), 5,
           'The definition, 5 marks.')], **B)
benefits = [cc(x) for x in ('Increased standard of living for citizens', 'Fall in social welfare bill', 'Increased aggregate demand /Economic',
                            'Increased investment Full', 'An increase in confidence in the economy', 'Reduces inequality and may prevent')]
challenges5 = [cc(x) for x in ('Possible skilled labour shortages', 'Possible wage demands', 'Pressure on the state infrastructure',
                               'Loss of service In', 'Inflationary pressures')]
add('sb-q5-a-ii', '3-2', 'benefits-and-challenges-of-full-employment', ref('B', 5, '(a)(ii)'),
    H.q(7, 'Discuss the possible economic benefits and economic challenges of full employment', ' [25]'), '2 x 5 & 2 x 5', 20,
    [anyN('r-benefits', H.traced('Economic benefits') + ' — any two', 10, 2, 5, benefits, 'Two benefits, 5 marks each (2 + 3).'),
     anyN('r-challenges', H.traced('Economic challenges') + ' — any two', 10, 2, 5, challenges5, 'Two challenges, 5 marks each (2 + 3).')],
    kind='fixed', **B)
q5b = H.q(7, 'Use the information in the table to answer the questions below.', ' (i)')
add('sb-q5-b-i', '3-0', 'the-marginal-propensity-to-save', ref('B', 5, '(b)(i)'),
    H.q(7, 'Define the term marginal propensity to save (MPS).', ' (ii)'), '6', 6,
    [point('r-1', H.traced('It is the proportion of each extra unit of income that is not consumed / that is saved.'), 6, 'The definition, 6 marks.')],
    stem=q5b, **B)
add('sb-q5-b-ii', '3-0', 'calculating-the-mps', ref('B', 5, '(b)(ii)'),
    H.q(7, 'Calculate the MPS for this economy illustrated in the table above.', ' (iii)'), '6', 6,
    [point('r-1', H.traced('MPS = 1 – MPC = 1 – 0.8 = 0.2'), 6, 'The MPS with its working, 6 marks.')], stem=q5b, **B)
add('sb-q5-b-iii', '3-0', 'the-open-economy-multiplier', ref('B', 5, '(b)(iii)'),
    H.q(7, 'Calculate the value of the multiplier in this open economy.', ' (iv)'), '4 + 4', 8,
    [point('r-working', H.traced('1*/0.2* +* 0.2*'), 4,
           'The working, 4 marks: ' + H.traced('* 1 mark each') + ', Method 1, 1 over MPS + MPM. The scheme also accepts its '
           'Method 2, 1 over 1 – (MPC – MPM), starred the same way. The figure shows both as printed.',
           accepts=[H.traced('1*/1* – *0.6*')]),
     point('r-answer', H.traced('2.5'), 4, H.traced('Correct answer: 4 marks') + '.')],
    stem=q5b, figure=SOL + 'p26-q5biii-working', **B)
add('sb-q5-b-iv', '3-0', 'the-injection-for-full-employment', ref('B', 5, '(b)(iv)'),
    H.q(7, 'How much will the government have to inject into this economy', ' [30]'), '5 x 2', 10,
    [point('r-full', 'Full-employment income — ' + H.traced('€620m'), 2, '2 marks, printed beside €620m.'),
     point('r-current', 'Less current income — ' + H.traced('€500m'), 2, '2 marks, printed beside €500m.'),
     point('r-shortfall', 'The shortfall in national income — ' + H.traced('€120m'), 2, '2 marks, printed beside €120m.'),
     point('r-multiplier', 'Divided by the multiplier — ' + H.traced('2.5'), 2, '2 marks, printed beside 2.5.'),
     point('r-injection', 'The government must increase spending by — ' + H.traced('€48m'), 2,
           '2 marks, printed beside the answer. The figure shows the working as printed.')],
    stem=q5b, figure=SOL + 'p26-q5biv-working', **B)
pick('sb-q5-c', '3-0', 'what-changes-gdp', ref('B', 5, '(c)'),
     H.q(7, 'Explain how Ireland’s Gross Domestic Product (GDP) could be affected by any two', ' [20]'), 'A development and its effect — any two',
     [f'{H.traced(dev)} — {H.opt(start, end)}' for dev, start, end in (
         ('An increase in Child Benefit payments.', 'This has no impact on GDP', '(ii) A foreign-owned company'),
         ('A foreign-owned company, operating in Ireland, sends back to their home country all the profits they have earned in Ireland.',
          'There will be no impact on the calculated figure for GDP', '(iii) An oil spill'),
         ('An oil spill off the coast costs the Irish Government significant clean-up costs.', 'This will increase GDP.', '2 x 10 marks each.'))],
     2, 10, 'Two developments, 10 marks each: ' + H.traced('Effect on GDP: 4 marks.') + ' ' + H.traced('Explanation: 6 marks.'), **B)

# Q6 ─ exchange rates; the balance of payments; SMEs abroad
add('sb-q6-a-i', '4-2', 'the-exchange-rate', ref('B', 6, '(a)(i)'), H.q(7, 'Explain the term exchange rate.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('The price of one currency expressed in terms of another currency.'), 5,
           'The explanation, 5 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('The price for which the currency of a country can be exchanged for another country’s currency')])], **B)
pick('sb-q6-a-ii', '4-2', 'a-stronger-euro', ref('B', 6, '(a)(ii)'),
     H.q(7, 'Outline the possible economic effects on the Irish economy of an appreciation', ' [25]'), 'An effect — any four',
     H.split('Imports prices decrease / imports cheaper', '4 x 5 marks (2+3)',
             ['Imports prices decrease', 'Exports prices increase', 'Falling employment', 'Slowdown in rate of economic growth',
              'US investment in the Irish economy']),
     4, 5, 'Four effects, 5 marks each (2 + 3).', **B)
q6b = H.q(7, '“The Balance of Payments (BOP) Current Account had a surplus', ' (i)')
add('sb-q6-b-i', '4-2', 'elements-of-the-balance-of-payments', ref('B', 6, '(b)(i)'),
    H.q(7, 'Describe the main elements of Ireland’s balance of payments (BOP) account.', ' (ii)'), '7 + 7 + 3', 17,
    [point(f'r-{k}', f"{H.traced(name)} — {cc(first)}", m, f'{name}, {m} marks.')
     for k, name, first, m in (('current', 'Current Account', 'The current account is the sum', 7),
                               ('capital', 'Capital Account', 'It records inflows and outflows', 7),
                               ('financial', 'Financial Account', 'This section covers transactions', 3))],
    stem=q6b, **B)
add('sb-q6-b-ii', '4-2', 'a-current-account-surplus', ref('B', 6, '(b)(ii)'),
    H.q(7, 'Explain what is meant by a surplus on the BOP current account.', ' (iii)'), '7', 7,
    [point('r-1', H.opt('A surplus on the current account means', '7 marks'), 7, 'The explanation, 7 marks.')], stem=q6b, **B)
pick('sb-q6-b-iii', '4-2', 'problems-of-a-surplus', ref('B', 6, '(b)(iii)'),
     H.q(7, 'Can a surplus on the BOP current account pose problems for an economy?', ' [30]'), 'A problem — any one',
     H.split('BOP Surplus due to weak domestic demand', '6 marks (3+3)',
             ['BOP Surplus due to weak domestic demand', 'Current account surpluses finance', 'Manipulating the value of the currency',
              'A current account surplus must be running', 'Current account surpluses could cause', 'Persistently large surpluses',
              'A current account surplus could boost']),
     1, 6, 'One problem, explained, 6 marks (3 + 3).', stem=q6b, **B)
add('sb-q6-c', '4-2', 'smes-in-foreign-markets', ref('B', 6, '(c)'),
    H.q(7, 'Outline the benefits and challenges for Irish SMEs operating in foreign markets.', ' [20]'), '2 x 5 & 2 x 5', 20,
    [anyN('r-benefits', 'A benefit — any two', 10, 2, 5,
          H.split('Access to larger markets/ Increased sales', 'The benefits for Irish SMEs operating in foreign markets - continued',
                  ['Access to larger markets', 'Economies of scale', 'Diversifying risk'])
          + H.split('Easier to access finance', '2 x 5 marks (2+3)', ['Easier to access finance', 'Government support available']),
          'Two benefits, 5 marks each (2 + 3).'),
     anyN('r-challenges', 'A challenge — any two', 10, 2, 5,
          H.split('Transport costs\nThese increase', '2 x 5 marks (2+3)',
                  ['Transport costs', 'Labour costs', 'Exchange rate risks', 'Language skills', 'Bureaucracy in other countries',
                   'Level of costs if coming', 'Competitiveness If the inflation', 'Other costs e.g.', 'Accessing credit', 'Capacity of the firm']),
          'Two challenges, 5 marks each (2 + 3).')],
    kind='fixed', stem=H.q(7, '“Irish SMEs (Small and Medium Enterprises)', ' Outline'), **B)

# Q7 ─ income, taxes and incidence; inequality; the environment
pairs = (('Income and wealth', 'Wealth\nThis is a stock', 'Progressive taxes\nOne'),
         ('Progressive taxes and regressive taxes', 'Progressive taxes\nOne', 'Impact of taxation\nThe impact'),
         ('Impact of taxation and incidence of taxation.', 'Impact of taxation\nThe impact', 'Terms correctly distinguished'))
pick('sb-q7-a', '3-1', 'distinguishing-economic-concepts', ref('B', 7, '(a)'),
     H.q(8, 'In the case of any two of the following three pairs, distinguish between', ' [20]'), 'A pair distinguished — any two',
     [f'{H.traced(pair)} — {H.opt(start, end)}' for pair, start, end in pairs],
     2, 10, 'Two pairs, 10 marks each (5 + 5): ' + H.traced('Terms correctly distinguished') + '.', **B)
pick('sb-q7-b-i', '3-1', 'policies-against-inequality', ref('B', 7, '(b)(i)'),
     H.q(8, 'Outline two economic policies which the Irish Government could consider to address inequality', ' (ii)'), 'A policy — any two',
     H.split('Increasing the national minimum wage / introduce a national living wage', '2 x 8 marks (3+5)',
             ['Increasing the national minimum wage', 'Tax policy', 'Social welfare policy', 'Universal access to basic goods',
              'Invest in training schemes', 'Create more employment']),
     2, 8, 'Two policies, 8 marks each (3 + 5). ' + H.traced('(Reference to how policy could help reduce inequality required for full marks.)'),
     **B)
pick('sb-q7-b-ii', '3-1', 'inequality-and-other-aims', ref('B', 7, '(b)(ii)'),
     H.q(8, 'Policies introduced to reduce inequality may make it more difficult', ' [30]'), 'A conflict — any two',
     H.split('More equitable distribution of income / wealth vs. economic growth', '2 x 7 marks (3+4)',
             ['More equitable distribution', 'Reduce unemployment vs Balanced Budget', 'Creating employment vs. equitable',
              'Progressive taxation vs job creation', 'Creating employment vs Balance of Payments']),
     2, 7, 'Two conflicts, with examples, 7 marks each (3 + 4).', **B)
add('sb-q7-c', '0-2', 'protecting-the-environment', ref('B', 7, '(c)'),
    H.q(8, 'Outline actions the Irish government could take to protect the environment.', ' [25]'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'An action — any four', 25, 4, 7,
          H.split('Introduce new taxes / Increase existing taxes', '4 points:',
                  ['Introduce new taxes', 'Tax incentives / subsidies', 'Provide / subsidise public transport', 'Information / education campaigns',
                   'Legislation / improved regulation']),
          'Four actions: the first correct 7 marks (4 + 3), the other three 6 each (3 + 3).', steps=[7, 6, 6, 6])],
    kind='fixed', stem=H.q(8, 'A clean and healthy environment is a scarce and valuable resource.', ' Outline'), **B)

# Q8 ─ the economy's performance; deficit and debt; urbanisation
q8a = H.q(8, 'Outline, using appropriate figures, how the Irish economy has performed', ' [20]')
TARIFF = H.traced('2 marks (approximate figure) + 3 marks (trend 1m + comment on trend 2m)')
areas = (('growth', '3-5', 'economic-growth-performance', 'Economic growth', '6.5% GDP / 5% GNP',
          'Irrespective of the agency which is forecasting', 'Price levels'),
         ('prices', '3-3', 'price-level-performance', 'Price level', '0% May 2016 / + 0.5% year on year',
          'Price inflation across the economy was low', 'Unemployment\n7.9%'),
         ('unemployment', '3-2', 'unemployment-performance', 'Unemployment', '7.9% - April 2016',
          'Unemployment levels continue to fall', 'Interest rates\n0%'),
         ('interest', '3-3', 'interest-rate-performance', 'Interest rates', '0%',
          'The Eurozone’s monetary policymakers (ECB)', '4 x 5 marks'))
for key, topic, concept, area, figure, trend_start, end in areas:
    # The area's figure, its trend in bold, then the comments, a line each.
    lines = [x.strip() for x in H.chunk(trend_start, end).split('\n') if x.strip()]
    trend_end = next(i for i, x in enumerate(lines) if x.endswith('.')) + 1
    trend = H.traced(' '.join(lines[:trend_end]))
    comments = H.split(lines[trend_end], end, [ln[:24] for ln in lines[trend_end:] if ln[:1].isupper() and not ln.startswith('Finance')])
    add(f'sb-q8-a-{key}', topic, concept, ref('B', 8, '(a)', area.lower()), f'{q8a} Answer for: {H.traced(area)}.',
        '5 (2 + 1 + 2)', 5,
        unpriced([(H.traced(figure), f'The scheme’s figure for the area. It prices each area 5, {TARIFF}, without tying the marks to these rows.'),
                  (trend, 'The trend the scheme sets in bold.')]
                 + [(c, 'A comment the scheme lists.' if i < len(comments) - 1 else 'Claim the complete assessment: 5 marks in all.')
                    for i, c in enumerate(comments)]),
        kind='questionTotal', **B)
q8b = H.q(8, '“The government will run a budget deficit of only 1%', ' (i)')
pick('sb-q8-b-i', '3-1', 'reducing-the-deficit-and-debt', ref('B', 8, '(b)(i)'),
     H.q(8, 'Discuss how the Irish Government has achieved reductions in the budget deficit', ' (ii)'), 'A way — any three',
     side('Budget Deficit', H.split('Taxation: new taxes / tax increases', 'Gross Debt\nCapital', ['Taxation: new taxes', 'Reduction in expenditure']))
     + side('Gross Debt', H.split('Capital spending reduced', '3 points x 7 marks', ['Capital spending reduced', 'Restructuring debt'])),
     3, 7, 'Three ways, 7 marks each (3 + 4). ' + H.traced('(Must have a minimum of one point under each heading.)'), stem=q8b, **B)
pick('sb-q8-b-ii', '3-1', 'the-costs-of-austerity', ref('B', 8, '(b)(ii)'),
     H.q(8, 'Outline the possible costs to Irish society in achieving these reductions.', ' [35]'), 'A cost — any two',
     H.split('Lower standard of living\nThe increased', '2 points x 7 marks',
             ['Lower standard of living', 'Deterioration in state services', 'Economic growth / job creation', 'Increased indebtedness']),
     2, 7, 'Two costs, 7 marks each (3 + 4).', stem=q8b, **B)
pick('sb-q8-c', '3-5', 'an-urbanising-population', ref('B', 8, '(c)'),
     H.q(8, 'Outline the economic consequences (positive and negative) of this development', ' [20]'), 'A consequence — any four',
     side('Positive economic consequences', [cc(x) for x in ('Increased standard of living Cities', 'Easier access to services',
                                                             'Easier to attract FDI', 'More attractive for entrepreneurs',
                                                             'Better use of scare resources')])
     + side('Negative economic consequences', [cc(x) for x in ('Quality of life/pressure', 'Housing: costs / availability',
                                                               'Provision of services Due', 'Prospect of future shortage',
                                                               'Loss of a sense of')]),
     4, 5, 'Four consequences, 5 marks each (2 + 3). ' + H.traced('(Must have a minimum of one point under each heading.)'),
     stem=H.q(8, 'Ireland’s population has become increasingly urbanised.', ' Outline'), **B)

if __name__ == '__main__':
    emit(cards)
