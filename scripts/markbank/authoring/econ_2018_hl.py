#!/usr/bin/env python3
"""Economics 2018 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2018-hl-ev.json, made
from a visual sweep of all 12 paper pages and 52 scheme pages before any 2018
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The only prose written here is guidance: tariffs, route
labels and what a figure or a calculation shows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2018, 'higher', 'LC034ALP000EV')
D = OldDeck(2018, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2018-HL-scheme-'
PAP = 'economics-2018-HL-paper-'
bl = H.bullets


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def side(label, options):
    """Options listed under one of the scheme's own side headings ("For", "Against"),
    each named by it: "<heading> — <response>". Both halves trace."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ the price taker
q1 = H.q(2, 'The firm in perfect competition is a', ' (a)')
pick('sa-q1-a', '2-0', 'the-price-taker', ref('A', 1, '(a)'), f"{q1} {H.q(2, 'Explain this statement.', ' (b)')}",
     'A point — any two', [H.opt('Each individual firm must accept the price', 'Because each firm'),
                           H.opt('Because each firm supplies such a tiny fraction', 'Demand is perfectly elastic'),
                           H.opt('Demand is perfectly elastic and if price increases', '(b) Other than price')],
     2, 4, 'Two points, 4 marks each. The scheme prints 8: 4 + 4 beside its three statements.', **A)
pick('sa-q1-b', '2-0', 'characteristics-of-perfect-competition', ref('A', 1, '(b)'),
     H.q(2, 'Other than price taking, outline two characteristics', ' (i)'), 'A characteristic — any two',
     bl('• Freedom of entry and exit.', '4 | P a g e'), 2, 4, 'Two characteristics, 4 marks each (2 + 2).',
     stem=q1, **A)

# Q2 ─ a rise in interest rates
pick('sa-q2', '3-3', 'effects-of-higher-interest-rates', ref('A', 2),
     H.q(2, 'Outline two possible economic effects of an increase in interest rates', ' (i)'), 'An economic effect — any two',
     bl('• Borrowing discouraged / disincentive to invest', '3 The EU is an example'), 2, 8,
     'Two effects, 8 marks each (4 + 4).', stem=H.q(2, 'Raising interest rates before the end of the decade', ' Outline'), **A)

# Q3 ─ customs union
add('sa-q3', '4-2', 'customs-union', ref('A', 3), H.q(2, 'The EU is an example of a customs union.', ' (16 marks)'),
    '12 + 4', 16,
    [point('r-1', H.opt('A Customs Union exists where the member countries agree', '(a) State the Law'), 16,
           'The explanation, 16 marks (12 + 4).')], **A)

# Q4 ─ diminishing marginal returns
add('sa-q4-a', '1-5', 'law-of-diminishing-marginal-returns', ref('A', 4, '(a)'),
    H.q(3, 'State the Law of Diminishing Marginal Returns.', ' (b)'), '10', 10,
    [point('r-1', H.opt('If increasing quantities of a variable factor', '(b) Does this apply'), 10, 'The law, 10 marks.')], **A)
add('sa-q4-b', '1-5', 'diminishing-returns-in-the-short-run', ref('A', 4, '(b)'),
    H.q(3, 'Does this law apply in the short run or in the long run?', ' (16 marks)'), '6 (2 + 4)', 6,
    [point('r-answer', H.opt('It applies in the short run only.', 'Why?'), None,
           'The scheme prices the answer and its reason 6 (2 + 4) together and does not say which earns which.'),
     point('r-reason', H.opt('It is only in the short run that at least one input is fixed.', '5 | P a g e'), None,
           'Claim both: 6 marks in all.')],
    kind='questionTotal', **A)

# Q5 ─ true or false: national income
statements = [('FALSE', '‘Double counting’ could occur when economic activity', 'Exports represent'),
              ('TRUE', 'Exports represent an injection into the circular flow of', 'Gross Domestic'),
              ('FALSE', 'Gross Domestic Product (GDP) includes a provision for', 'Primary school'),
              ('FALSE', 'Primary school teacher salaries are categorised as', '6 State and explain')]
add('sa-q5', '3-0', 'national-income-true-or-false', ref('A', 5),
    # The printed statements follow the ask, from the paper's own table rows: set at phone
    # width the table's text falls near 8 px, and the card cannot be answered without them.
    f"{H.q(3, 'Read each statement below', ' STATEMENT')} {H.q(3, '‘Double counting’ could occur', ' (16 marks)')}",
    '2 x 6, 2 x 2', 16,
    [anyN('r-1', 'Each statement ticked correctly', 16, 4, 6,
          [f"{H.traced(tick)} — {H.opt(a, b).replace(' ✓', '').replace('✓', '').strip()}" for tick, a, b in statements],
          'All four: the first two correct 6 marks each, the other two 2 each. The completed table is shown with the '
          'answer.', steps=[6, 6, 2, 2])],
    kind='fixed', figure=SOL + 'p08-q5-ticks', **A)
beside_ask(cards[-1], PAP + 'p03-q5-table')

# Q6 ─ the canons of taxation
add('sa-q6', '3-1', 'canons-of-taxation', ref('A', 6), H.q(3, 'State and explain Adam Smith’s four Canons', ' (i)'),
    '1 x 5, 3 x 4', 17,
    [anyN('r-1', 'Each canon stated and explained', 17, 4, 5,
          H.split('Equity\nThe more you earn', '7 (a) Outline two policies', ['Equity', 'Economy', 'Certainty', 'Convenience']),
          'All four: the first credited 5 marks, the other three 4 each.', steps=[5, 4, 4, 4])],
    kind='fixed', **A)

# Q7 ─ income inequality
pick('sa-q7-a', '3-1', 'policies-to-reduce-income-inequality', ref('A', 7, '(a)'),
     H.q(4, 'Outline two policies a government could consider to reduce income inequality.', ' (i)'),
     'A policy — any two', bl('Welfare benefits could be increased or maintained', '(b) Outline one possible challenge'),
     2, 6, 'Two policies, 6 marks each (3 + 3).', **A)
pick('sa-q7-b', '3-1', 'challenges-of-reducing-inequality', ref('A', 7, '(b)'),
     H.q(4, 'Outline one possible challenge for the Irish economy', ' (17 marks)'), 'A challenge — any one',
     bl('• Possible increase in costs to businesses', '8 Outline three economic'), 1, 5, 'One challenge, 5 marks.', **A)

# Q8 ─ raising the retirement age
add('sa-q8', '2-1', 'raising-the-retirement-age', ref('A', 8),
    H.q(4, 'Outline three economic consequences of raising the retirement age', ' Economic consequences'),
    '6 + 6 + 5', 17,
    [anyN('r-1', 'An economic consequence — any three', 17, 3, 6,
          bl('• As people work longer they will be contributing', '7 | P a g e'),
          'Three consequences: the first two credited 6 marks each (3 + 3), the third 5 (3 + 2).', steps=[6, 6, 5])],
    kind='fixed', **A)

# Q9 ─ price discrimination
add('sa-q9-a', '2-0', 'price-discrimination', ref('A', 9, '(a)'), H.q(5, 'Define the term price discrimination.', ' Definition'),
    '8', 8, [point('r-1', H.opt('Selling the same product at different prices', '(b) Outline three conditions'), 8,
                   'The definition, 8 marks.')], **A)
pick('sa-q9-b', '2-0', 'conditions-for-price-discrimination', ref('A', 9, '(b)'),
     H.q(5, 'Outline three conditions necessary for price discrimination', ' (i)'), 'A condition — any three',
     H.split('Some monopoly / market power', '8 | P a g e',
             ['Some monopoly / market power', 'Separation of markets', 'Different consumer price elasticities']),
     3, 3, 'Three conditions, 3 marks each.', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ demand; the music venue; consumer surplus
add('sb-q1-a-i', '1-1', 'movement-along-and-shift-in-demand', ref('B', 1, '(a)(i)'),
    H.q(6, 'Distinguish between a movement along a demand curve and a shift', ' (ii)'), '2 @ 5', 10,
    [point('r-movement', H.opt('A change in the price of the good itself', 'A shift in a demand curve:'), 5,
           'A movement along the demand curve, 5 marks.'),
     point('r-shift', H.opt('A change in any of the factors other than price', '(ii) Explain, using a supply'), 5,
           'A shift in the demand curve, 5 marks.')], **B)
labels9 = [H.traced(x) for x in ('Price', 'Quantity', 'S', 'D', 'P1', 'PE', 'QD', 'QS', 'SURPLUS')]
add('sb-q1-a-ii', '1-0', 'returning-to-equilibrium-after-a-surplus', ref('B', 1, '(a)(ii)'),
    H.q(6, 'Explain, using a supply and demand diagram how a market would return', ' [25]'), 'Diagram 9 (9 x 1) + 6', 15,
    [anyN('r-diagram', 'The diagram — each correctly labelled element', 9, 9, 1, labels9,
          'The diagram, 9 marks: 1 for each of the nine labels the scheme marks with a raised 1 (both axes, S, D, '
          'P1, PE, QD, QS and the surplus). The completed diagram is shown with the answer.'),
     point('r-explanation', H.opt('When there is a surplus or excess supply for a good', '9 | P a g e'), 6,
           'The explanation, 6 marks. The scheme opens: ' + H.opt('An excess supply (surplus) in the market implies', '• When there is a surplus') + '')],
    kind='fixed', figure=SOL + 'p11-q1aii-diagram', **B)
q1b = H.q(6, 'The owners of a music venue, with a maximum capacity', ' Price')
q1b_table = PAP + 'p06-q1b-table'
venue_labels = H.cell('Labels: P, Q, D/C, S/C, PE, QE', upto='QE')
add('sb-q1-b-i', '1-0', 'drawing-the-venue-market', ref('B', 1, '(b)(i)'),
    H.q(6, 'Using the above data, draw the demand and supply curve', ' (ii)'), 'Diagram 13', 13,
    [anyN('r-labels', 'Each label', 6, 6, 1,
          [H.traced(x) for x in venue_labels.split(': ', 1)[1].split(', ')],
          'The six labels, 1 mark each (P, Q, D/C, S/C, PE and QE).'),
     point('r-vertical', H.traced('Vertical S/C at 400 units'), 2, 'The vertical supply curve at 400 units, 2 marks.'),
     point('r-points', H.traced('5 points along D/C'), 5, 'The five demand points, 1 mark each. The completed diagram is '
           'shown with the answer.')],
    kind='fixed', stem=q1b, figure=SOL + 'p12-q1bi-diagram', **B)
beside_ask(cards[-1], q1b_table)
add('sb-q1-b-ii', '1-2', 'a-fixed-capacity-supply-curve', ref('B', 1, '(b)(ii)'),
    H.q(6, 'Explain the reason for the shape of the supply curve', ' (iii)'), '6', 6,
    [point('r-1', H.opt('Regardless of price the quantity supplied will be fixed at 400', 'It is perfectly inelastic'), 6,
           'The reason, 6 marks. ' + H.traced('If 400 is not referred to: -1m'),
           accepts=[H.opt('It is perfectly inelastic / vertical', 'If 400 is not')])],
    stem=q1b, figure=q1b_table, **B)
add('sb-q1-b-iii', '1-1', 'consumer-surplus-and-total-revenue', ref('B', 1, '(b)(iii)'),
    H.q(6, 'Explain the terms consumer surplus and total revenue.', ' (iv)'), '2 @ 6', 12,
    [point('r-cs', H.opt('Consumer surplus is the difference', 'Total Revenue: is'), 6, 'Consumer surplus, 6 marks.'),
     point('r-tr', H.opt('Total Revenue: is the total revenue received', '(iv) Show clearly'), 6, 'Total revenue, 6 marks.')],
    stem=q1b, **B)
add('sb-q1-b-iv', '1-1', 'areas-of-consumer-surplus-and-revenue', ref('B', 1, '(b)(iv)'),
    H.q(6, 'Show clearly on the diagram you have drawn in part (i) above', ' [35]'), '2 + 2', 4,
    [point('r-cs', H.traced('Consumer Surplus'), 2, 'The consumer surplus area, 2 marks.'),
     point('r-tr', H.traced('Total Revenue'), 2, 'The total revenue area, 2 marks. Both are shaded on the completed diagram.')],
    stem=q1b, figure=SOL + 'p12-q1bi-diagram', **B)
beside_ask(cards[-1], q1b_table)
q1c = H.q(6, 'The owners of this venue decide to charge €60 per ticket.', ' (i)')
add('sb-q1-c-i', '1-5', 'total-revenue-at-a-full-house', ref('B', 1, '(c)(i)'),
    H.q(6, 'Calculate the total revenue from the ticket sales', ' (ii)'), '6', 6,
    [point('r-1', H.traced('400 x €60 = €24,000'), 6, 'The total revenue with its working, 6 marks.')], stem=q1c, **B)
add('sb-q1-c-ii', '1-1', 'using-consumer-surplus', ref('B', 1, '(c)(ii)'),
    H.q(6, 'Explain how a knowledge of the concept of consumer surplus', ' [15]'), '9 graded', 9,
    [point(f'r-{i}', text, None, note) for i, (text, note) in enumerate([
        (H.opt('The owners of the venue know that some consumers', 'The owners could charge'),
         'The scheme grades the explanation out of 9 and does not price its points.'),
        (H.opt('The owners could charge higher prices and extract', 'If the consumer was charged'), 'Graded.'),
        (H.opt('If the consumer was charged the highest price', 'For small firms'), 'Graded.'),
        (H.opt('For small firms an understanding of the consumer surplus', '11 | P a g e'), 'Claim the complete explanation: 9 marks in all.')], 1)],
    kind='questionTotal', stem=q1c, **B)

# Q2 ─ oligopoly; collusion in motor insurance
q2a = H.q(7, 'An oligopoly is a market structure in which', ' (i)')
add('sb-q2-a-i', '2-0', 'how-oligopolists-compete', ref('B', 2, '(a)(i)'),
    H.q(7, 'Describe how firms in this market structure compete', ' (ii)'), '6', 6,
    [point('r-1', H.opt('Because products are close substitutes firms may compete', '-2m if no reference'), 6,
           'Non-price competition, 6 marks. ' + H.traced('-2m if no reference made to product differentiation'))],
    stem=q2a, **B)
add('sb-q2-a-ii', '2-0', 'advantages-and-disadvantages-of-oligopoly', ref('B', 2, '(a)(ii)'),
    H.q(7, 'Discuss the advantages and disadvantages of oligopoly', ' [30]'), '4 @ 6 (3 + 3)', 24,
    [anyN('r-advantages', H.traced('Possible advantages include:').rstrip(':') + ' — any two', 12, 2, 6,
          H.split('Stability in prices / price comparability', '12 | P a g e',
                  ['Stability in prices', 'Profit levels', 'Quality of product /service', 'Benefits of advertising',
                   'Possibility of lower prices', 'More secure employment']),
          'Two advantages, 6 marks each (3 + 3).'),
     anyN('r-disadvantages', H.traced('Possible disadvantages include:').rstrip(':') + ' — any two', 12, 2, 6,
          H.split('Supernormal profits\nModerate', '13 | P a g e',
                  ['Supernormal profits', 'Higher prices', 'Effects of cartels / collusion', 'Restricted choice',
                   'Prevention of the entry of new firms']),
          'Two disadvantages, 6 marks each (3 + 3).')],
    kind='fixed', stem=q2a, **B)
elements = [H.traced(x) for x in H.chunk('Price axis / Quantity axis / Kinked D/C', '\n').strip().split(' / ')]
add('sb-q2-b-i', '2-0', 'long-run-equilibrium-in-oligopoly', ref('B', 2, '(b)(i)'),
    H.q(7, 'Explain, using a clearly labelled diagram, the long', ' (ii)'), 'Diagram 9 (9 x 1) + explanation 8 (4 x 2)', 17,
    [anyN('r-diagram', 'The diagram — each correctly labelled element', 9, 9, 1, elements,
          'The diagram, 9 marks: 1 for each of the nine elements the scheme lists. The completed diagram is shown with '
          'the answer.'),
     anyN('r-explanation', 'The explanation — any four points', 8, 4, 2,
          [H.opt(a, b) for a, b in (('Equilibrium occurs where (a) MC = MR', '2. The firm will'),
                                    ('The firm will produce Q1 and sell', '3. The firm’s cost'),
                                    ('The firm’s cost of production is shown at point G.', '4. Should costs'),
                                    ('Should costs rise between points E and D', 'or\n5.'),
                                    ('This firm is earning SNPs because AR exceeds AC', '(ii) With reference'))],
          'The explanation, 8 marks: any four of the five points, 2 marks each.')],
    kind='fixed', figure=SOL + 'p16-q2bi-diagram', **B)
add('sb-q2-b-ii', '2-0', 'price-rigidity-and-the-kinked-demand-curve', ref('B', 2, '(b)(ii)'),
    H.q(7, 'With reference to the ‘kinked’ demand curve', ' [25]'), '8 graded', 8,
    [point(f'r-{i}', text, None, note) for i, (text, note) in enumerate([
        (H.opt('The firm above would fear increasing its price above P1', 'The firm would fear lowering'),
         'The scheme grades the rationale out of 8 and does not price its points.'),
        (H.opt('The firm would fear lowering its price below P1', 'This results in the kinked'), 'Graded.'),
        (H.opt('This results in the kinked D/C and no incentive', '14 | P a g e'), 'Claim the complete rationale: 8 marks in all.')], 1)],
    kind='questionTotal', **B)
q2c = H.q(7, '‘Motor insurance providers in Ireland targeted', ' (i)')
pick('sb-q2-c-i', '2-0', 'effects-of-collusion-on-consumers', ref('B', 2, '(c)(i)'),
     H.q(7, 'Explain the likely effects on consumers if collusion', ' (ii)'), 'An effect on consumers — any two',
     H.split('Higher / less competitive prices', '(ii) Suggest two measures',
             ['Higher / less competitive prices', 'Restricted choice', 'Supernormal profits earned']),
     2, 5, 'Two effects, 5 marks each (2 + 3).', stem=q2c, **B)
pick('sb-q2-c-ii', '1-3', 'discouraging-anti-competitive-practice', ref('B', 2, '(c)(ii)'),
     H.q(7, 'Suggest two measures the government could consider to discourage', ' [20]'), 'A measure — any two',
     H.split('Improved consumer protection / education / awareness', '15 | P a g e',
             ['Improved consumer protection', 'Improved regulation of the industry',
              'Improved investigation of alleged lack', 'Deregulation of the industry']),
     2, 5, 'Two measures, 5 marks each (2 + 3).', stem=q2c, **B)

# Q3 ─ marginal cost; price elasticity of supply; sterling
q3a = H.q(7, 'The table below shows the output and total cost for a firm.', ' Output')
q3a_table = PAP + 'p07-q3a-table'
mc = H.chunk('MC (€) 20 10 15 20 30 45 50', '\n').split()[2:]
add('sb-q3-a-i', '1-5', 'marginal-cost', ref('B', 3, '(a)(i)'), H.q(7, 'Define the term marginal cost.', ' (ii)'), '5', 5,
    [point('r-1', H.opt('The change / addition to total cost as a result', '(ii) Draw and clearly label'), 5,
           'The definition, 5 marks.')], stem=q3a, **B)
add('sb-q3-a-ii', '1-5', 'graphing-marginal-cost', ref('B', 3, '(a)(ii)'),
    H.q(7, 'Draw and clearly label a graph to illustrate the marginal cost', ' (iii)'), 'Diagram 8: 7 x 1 + 1', 8,
    [anyN('r-points', 'Each marginal cost plotted (output — MC)', 7, 7, 1,
          [f'{H.traced(str(q))} — {H.traced(v)}' for q, v in zip(range(1, 8), mc)],
          'The seven marginal costs, 1 mark each, from the scheme’s completed table: output 1 to 7, MC €20, €10, €15, '
          '€20, €30, €45, €50. The graph is shown with the answer.'),
     point('r-label', H.traced('MC'), 1, 'Labelling the curve, 1 mark.')],
    kind='fixed', stem=q3a, figure=SOL + 'p18-q3a-graph', **B)
beside_ask(cards[-1], q3a_table)
q3aiii = H.q(7, 'Indicate on the graph that you have drawn the profit', ' (iv)')
add('sb-q3-a-iii', '1-5', 'profit-maximising-output', ref('B', 3, '(a)(iii)'), q3aiii, '2 + 2, 4', 8,
    [ask_row('r-indicate', q3aiii[:q3aiii.index(' and explain')], 4,
             'Indicating the profit-maximising output on the graph, 4 marks (2 + 2): the scheme’s graph marks it at 5 '
             'units, where MC = MR, and is shown with the answer.'),
     point('r-explanation', H.opt('Profit maximisation occurs when MC = MR.', '(iv) Calculate the profit'), 4,
           'The explanation, 4 marks.')],
    stem=q3a, figure=SOL + 'p18-q3a-graph', **B)
beside_ask(cards[-1], q3a_table)
add('sb-q3-a-iv', '1-5', 'profit-at-the-profit-maximising-output', ref('B', 3, '(a)(iv)'),
    H.q(7, 'Calculate the profit earned at this profit', ' [25]'), '4', 4,
    [point('r-1', H.traced('€150 - €115= €35'), 4, 'The profit, 4 marks, with the scheme’s working: TR – TC, '
           'TR (P x Q) = €30 x 5 = €150.')],
    stem=q3a, figure=q3a_table, **B)
add('sb-q3-b-i', '1-4', 'price-elasticity-of-supply', ref('B', 3, '(b)(i)'),
    H.q(7, 'Define the term price elasticity of supply (PES).', ' (ii)'), '5', 5,
    [point('r-1', H.opt('It is the percentage change in quantity supplied', 'Price elasticity of supply measures'), 5,
           'The definition, 5 marks. The scheme also accepts its second statement.',
           accepts=[H.opt('Price elasticity of supply measures the degree', '(ii) Explain, by means')])], **B)
add('sb-q3-b-ii', '1-4', 'pes-in-the-short-and-long-run', ref('B', 3, '(b)(ii)'),
    H.q(7, 'Explain, by means of an example, why the PES might be different', ' (iii)'), '10 graded', 10,
    [point(f'r-{i}', text, None, note) for i, (text, note) in enumerate([
        (H.opt('In the short run, the quantity supplied is not very responsive', 'Supply is usually more elastic'),
         'The scheme grades the explanation out of 10 and does not price its points.'),
        (H.opt('Supply is usually more elastic in the long run', 'It takes time to respond'), 'Graded.'),
        (H.opt('It takes time to respond to a price change.', '17 | P a g e'),
         'Claim the complete explanation: 10 marks in all.')], 1)],
    kind='questionTotal', **B)
pick('sb-q3-b-iii', '1-4', 'factors-influencing-pes', ref('B', 3, '(b)(iii)'),
     H.q(7, 'Discuss two factors, other than time period, that influence the PES', ' [25]'), 'A factor — any two',
     H.split('The nature of the product / ease of storing stock', 'Must refer to elastic',
             ['The nature of the product', 'Is the firm operating at full productive capacity',
              'Mobility of the factors of production', 'Degree of specialised labour', 'Ease of switching',
              'Production cost conditions', 'Products in joint supply']),
     2, 5, 'Two factors, 5 marks each (2 + 3). ' + H.traced('Must refer to elastic / inelastic: -1 mark'), **B)
add('sb-q3-c-i', '4-2', 'a-weaker-sterling-and-irish-prices', ref('B', 3, '(c)(i)'),
    H.q(7, 'Outline the potential impact a fall in the value of Sterling', ' (ii)'), '7', 7,
    [point('r-1', H.opt('A fall in the value of sterling means that Irish goods', '(ii) Explain how knowledge'), 7,
           'The impact, 7 marks.')], **B)
pick('sb-q3-c-ii', '1-4', 'ped-and-exporting-to-the-uk', ref('B', 3, '(c)(ii)'),
     H.q(7, 'Explain how knowledge of price elasticity of demand (PED)', ' [25]'), 'An explanation — any two',
     [H.opt('If the product has an inelastic demand then there is scope', 'If demand for their product is elastic'),
      H.opt('If demand for their product is elastic then the firm', 'Or\nIf response'),
      H.opt('A fall in the value of sterling means that Irish exporters', '⟨25⟩')],
     2, 9, 'Two explanations, 9 marks each, graded: inelastic and elastic demand, or the answer linked to part (i) '
     '(the scheme’s third paragraph). ' + H.traced('Elastic-Inelastic / Explanation / reference to UK market'), **B)

# Q4 ─ labour productivity; economies of scale; mobility of labour
add('sb-q4-a-i', '2-1', 'labour-productivity', ref('B', 4, '(a)(i)'), H.q(8, 'Define the term labour productivity.', ' (ii)'),
    '8', 8, [point('r-1', H.opt('The output produced per worker per period', '(ii) Explain how a firm'), 8,
                   'The definition, 8 marks.')], **B)
pick('sb-q4-a-ii', '2-1', 'raising-labour-productivity', ref('B', 4, '(a)(ii)'),
     H.q(8, 'Explain how a firm could increase the productivity of labour.', ' [20]'), 'A way to raise productivity — any two',
     H.split('Education / training/retraining', '20 | P a g e',
             ['Education / training', 'Introduce incentive schemes', 'Improve the quality of the other factors',
              'Introduce new work practices']),
     2, 6, 'Two ways, 6 marks each (3 + 3).', **B)
q4b = H.q(8, 'Globalisation allows firms to exploit economies of scale.', ' (i)')
add('sb-q4-b-i', '1-5', 'economies-of-scale', ref('B', 4, '(b)(i)'), H.q(8, 'Explain the term economies of scale.', ' (ii)'),
    '9', 9, [point('r-1', H.opt('Economies of scale arise when average cost', '(ii) Discuss how a firm'), 9,
                   'The explanation, 9 marks.')], stem=q4b, **B)
pick('sb-q4-b-ii', '1-5', 'benefits-of-economies-of-scale', ref('B', 4, '(b)(ii)'),
     H.q(8, 'Discuss how a firm might benefit from economies of scale', ' (iii)'), 'A benefit, with an example — any two',
     H.split('Technical economies of scale\nHigher', '-1m if example',
             ['Technical economies of scale', 'Labour economies', 'Economies in the use of raw materials',
              'Financial economies', 'Purchasing economies', 'Economies in distribution', 'Marketing / advertising economies',
              'Managerial economies'])
     + H.split('Better infrastructure.', '(b) ⟨1 x 7⟩',
               ['Better infrastructure', 'Development of specialist firms', 'Development of separate R & D units']),
     2, 7, 'Two benefits, 7 marks each (3 + 4). ' + H.traced('-1m if example is not given'), stem=q4b, **B)
pick('sb-q4-b-iii', '1-5', 'can-firms-become-too-big', ref('B', 4, '(b)(iii)'),
     H.q(8, 'Can firms become ‘too big’? Explain your answer.', ' [30]'), 'A disadvantage of size — any one',
     H.split('Managerial diseconomies', '⟨30⟩',
             ['Managerial diseconomies', 'Lack of worker motivation', 'Shortages of skilled labour',
              'Increase in bureaucracy']),
     1, 7, 'One explained disadvantage, 7 marks (3 + 4). The scheme’s answer: '
     + H.opt('Yes, as there are disadvantages associated', 'Possible responses include'), stem=q4b, **B)
q4c = H.q(8, 'Restrictions placed on workers’ mobility', ' (i)')
add('sb-q4-c-i', '2-1', 'occupational-and-geographic-mobility', ref('B', 4, '(c)(i)'),
    H.q(8, 'Distinguish between occupational mobility of labour', ' (ii)'), '5 + 5', 10,
    [point('r-occupational', H.opt('Occupational mobility of labour is the ease', 'Geographic mobility'), 5,
           'Occupational mobility, 5 marks.'),
     point('r-geographic', H.opt('Geographic mobility of labour is the ease', '(ii) Discuss the factors'), 5,
           'Geographic mobility, 5 marks.')], stem=q4c, **B)
pick('sb-q4-c-ii', '2-1', 'limits-to-geographic-mobility', ref('B', 4, '(c)(ii)'),
     H.q(8, 'Discuss the factors that limit the geographic mobility', ' (iii)'), 'A factor — any two',
     bl('• Accommodation/ high cost of renting property', '23 | P a g e'),
     2, 5, 'Two factors, 5 marks each (2 + 3).', stem=q4c, **B)
pick('sb-q4-c-iii', '2-1', 'improving-geographic-mobility', ref('B', 4, '(c)(iii)'),
     H.q(8, 'Suggest one measure which could be considered to address', ' [25]'), 'A measure — any one',
     bl('• Reform of the housing market', '⟨25⟩'), 1, 5, 'One measure, 5 marks (2 + 3).', stem=q4c, **B)

# Q5 ─ fiscal and monetary policy; indirect taxes; budget deficits
add('sb-q5-a-i', '3-1', 'fiscal-and-monetary-policy', ref('B', 5, '(a)(i)'),
    H.q(8, 'Explain the terms fiscal policy and monetary policy.', ' (ii)'), '2 @ 5', 10,
    [point('r-fiscal', H.opt('Any action taken by the government which influences the timing', 'Monetary policy\nAny'), 5,
           'Fiscal policy, 5 marks.'),
     point('r-monetary', H.opt('Any action taken by the ECB which influences', '(ii) Outline how Ireland'), 5,
           'Monetary policy, 5 marks.')], **B)
q5aii = H.q(8, 'Outline how Ireland’s membership of the Eurozone affects', ' [20]')
for word, label, start, end, firsts in (
        ('monetary', 'Monetary Policy', 'ECB controls monetary policy', '25 | P a g e',
         ['ECB controls monetary policy', 'Decisions by ECB may not suit Ireland', 'Central Bank of Ireland has imposed rules']),
        ('fiscal', 'Fiscal Policy', 'Fiscal restraint required by Irish government', '⟨20⟩',
         ['Fiscal restraint required', 'EU rules re budget deficits', 'Budget pre-approved by EU'])):
    pick(f'sb-q5-a-ii-{word}', '3-3' if word == 'monetary' else '3-1', 'the-eurozone-and-irish-policy',
         ref('B', 5, '(a)(ii)', word), f'{q5aii} Answer on: {word} policy.', f'{H.traced(label)} — any two',
         H.split(start, end, firsts), 2, 5,
         'Two effects, 5 marks each (2 + 3). The paper asks about monetary policy OR fiscal policy, and the scheme '
         'lists each separately.', **B)
q5b = H.q(8, 'Indirect taxes are frequently used as a government policy', ' (i)')
add('sb-q5-b-i', '3-1', 'indirect-tax', ref('B', 5, '(b)(i)'), H.q(8, 'Explain the term indirect tax.', ' (ii)'), '5', 5,
    [point('r-1', H.opt('An indirect tax is a tax on the consumption', '(ii) Explain how indirect taxes'), 5,
           'The explanation, 5 marks.')], stem=q5b, **B)
pick('sb-q5-b-ii', '3-1', 'indirect-taxes-and-consumer-behaviour', ref('B', 5, '(b)(ii)'),
     H.q(8, 'Explain how indirect taxes could be used to change', ' (iii)'), 'A use of indirect taxes, with an example — any three',
     H.split('Increased VAT on sunbed services', '-1m if example omitted',
             ['Increased VAT on sunbed services', 'Tax on sugar sweetened drinks', 'Environmental levy on plastic bags',
              'Tobacco products tax', 'Introduction of Carbon taxes'])
     + H.split('Reduced VAT rate for the tourism sector', '(iii) Outline one intervention',
               ['Reduced VAT rate for the tourism sector', 'VRT Since']),
     3, 5, 'Three uses, 5 marks each. ' + H.traced('-1m if example omitted'), stem=q5b, **B)
pick('sb-q5-b-iii', '1-3', 'changing-behaviour-without-tax', ref('B', 5, '(b)(iii)'),
     H.q(8, 'Outline one intervention, other than taxation', ' [25]'), 'An intervention — any one',
     H.split('National Advertising Campaigns', '28 | P a g e',
             ['National Advertising Campaigns', 'Education Programmes', 'Legislation Passing', 'Government grants']),
     1, 5, 'One intervention, 5 marks (2 + 3).', stem=q5b, **B)
q5c = H.q(8, 'In 2016, the Government [budget] deficit was', ' (i)')
add('sb-q5-c-i', '3-1', 'budget-deficit', ref('B', 5, '(c)(i)'), H.q(8, 'Define the term budget deficit.', ' (ii)'), '6', 6,
    [point('r-1', H.opt('A budget deficit arises when government current expenditure', '(ii) Discuss the possible'), 6,
           'The definition, 6 marks.')], stem=q5c, **B)
pick('sb-q5-c-ii', '3-1', 'reducing-the-budget-deficit', ref('B', 5, '(c)(ii)'),
     H.q(8, 'Discuss the possible economic consequences of a reduction in the budget deficit', ' (iii)'),
     'An economic consequence — any two',
     bl('• Less borrowing for the Irish economy', 'Other:') + [H.opt('More people may engage in the black economy', '29 | P a g e')],
     2, 6, 'Two consequences, 6 marks each (3 + 3). The last option is the scheme’s “Other”.', stem=q5c, **B)
q5ciii = H.q(8, 'Is a budget deficit always bad for an economy?', ' [30]')
for word, start, end, firsts in (
        ('no', 'Stimulates demand\nIf', 'Yes\nUnsustainable', ['Stimulates demand', 'Job creation', 'Self-financing deficit']),
        ('yes', 'Unsustainable debt levels', '⟨30⟩', ['Unsustainable debt levels', 'High future taxation levels', 'Deadweight debt'])):
    pick(f'sb-q5-c-iii-{word}', '3-1', 'is-a-budget-deficit-always-bad', ref('B', 5, '(c)(iii)', word),
         f'{q5ciii} Justify the choice: {word.upper()}.', f'A reason for answering {word.upper()} — any two',
         H.split(start, end, firsts), 2, 6,
         'Two reasons, 6 marks each (3 + 3). The scheme credits NO and YES, each with its own list.', stem=q5c, **B)

# Q6 ─ migration; the Single European Market; development aid
q6 = H.q(9, 'Ireland’s net inward migration in 2017', ' (a)')
pick('sb-q6-a-i', '3-2', 'drivers-of-migration', ref('B', 6, '(a)(i)'),
     H.q(9, 'Describe the factors that drive migration between countries.', ' (ii)'), 'A factor — any three',
     H.split('Lack of jobs opportunities / Ireland’s economy recovery', '31 | P a g e',
             ['Lack of jobs opportunities', 'Low rates of pay', 'Existence of high taxes', 'Valuable work experience',
              'Political or religious persecution']),
     3, 5, 'Three factors, 5 marks each (2 + 3).', stem=q6, **B)
pick('sb-q6-a-ii', '3-2', 'consequences-of-immigration', ref('B', 6, '(a)(ii)'),
     H.q(9, 'Discuss the economic consequences of increased immigration', ' [30]'), 'An economic consequence — any three',
     bl('• Effect on state services', '⟨30⟩'), 3, 5, 'Three consequences, 5 marks each (2 + 3).', stem=q6, **B)
add('sb-q6-b', '4-1', 'the-single-european-market', ref('B', 6, '(b)'),
    H.q(9, 'Discuss the economic arguments for and against Ireland being a member', ' [25]'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'Two arguments for and two against', 25, 4, 7,
          side('Arguments for', H.split('Larger market / encourages trade expansion', '7+6+6+6',
                                        ['Larger market / encourages trade expansion', 'Irish firms can bid for public sector',
                                         'Benefits for consumers', 'Ease of trade', 'Free movement of capital',
                                         'Free movement of labour', 'Legislative / funding benefits', 'Social benefits',
                                         'Profitable investment opportunities'], source='cells'))
          + side('Arguments against', H.split('Increased / intensified competition', 'Possible responses Max Mark (c) For 2018',
                                              ['Increased / intensified competition', 'Loss of sovereignty',
                                               'Reduced availability of EU funding', 'Public procurement of large public contracts',
                                               'EU monitoring / EU wide polices', 'Isolation from EU decisions'], source='block')),
          'Two points in favour and two against. The scheme prices the four on one ladder, not by side: the first '
          'credited 7 marks (3 + 4), the other three 6 each (3 + 3).', steps=[7, 6, 6, 6])],
    kind='fixed', **B)
q6c = H.q(9, 'For 2018, the Irish government has allocated', ' (c)')
add('sb-q6-c', '4-0', 'official-development-assistance', ref('B', 6, '(c)'),
    H.q(9, 'Discuss the benefits and challenges of Official Development Assistance', ' [20]'), '4 @ 5 (2 + 3)', 20,
    [anyN('r-benefits', H.traced('Benefits:').rstrip(':') + ' — any two', 10, 2, 5,
          [H.traced(x) for x in ('Lives saved', 'Helps builds infrastructure (which promotes industrial development)',
                                 'Improvement in health services', 'Aid for agriculture', 'Clean water and sanitation',
                                 'Support education / training', 'Reduction in poverty levels etc.')],
          'Two benefits, 5 marks each (2 + 3).'),
     anyN('r-challenges', H.traced('Challenges') + ' — any two', 10, 2, 5,
          H.split('Aid may not ‘trickle down’', '⟨20⟩',
                  ['Aid may not ‘trickle down’', 'Develop a culture of dependency', 'High profile projects',
                   'Implications of aid', 'Political Corruption', 'Type / use of aid']),
          'Two challenges, 5 marks each (2 + 3).')],
    kind='fixed', stem=q6c, **B)

# Q7 ─ the Irish economy; banking regulation; capital spending
q7a = H.q(9, 'Assess the performance of the Irish economy in the past 12 months', ' (i)')
areas = (('i', '3-5', 'economic-growth-performance', 'Economic growth', ' (ii)', 'GDP rate of growth over approx.', 'Employment/ unemployment'),
         ('ii', '3-2', 'employment-performance', 'Employment / unemployment', ' (iii)', 'Unemployment rate below 6%.', 'Inflation/Price level'),
         ('iii', '3-3', 'inflation-performance', 'Inflation', ' (iv)', 'Rate of inflation below 1%.', '37 | P a g e'),
         ('iv', '3-1', 'national-debt-performance', 'The size of the National Debt.', ' [20]', 'Ireland’s national debt at approx. €200 bn.', '2 marks + 1 mark'))
for part, topic, concept, area, nxt, start, end in areas:
    figure = H.opt(start, '\n')
    # The bullets under the area's figure; the scheme prints one debt bullet twice.
    pts = [t for t in dict.fromkeys(H.bullets(start, end)) if t != figure]
    rows = [point('r-figure', figure, None,
                  'The scheme’s figure for the area. It prices each area 5, ' + H.traced('2 marks + 1 mark + 2 marks')
                  + ' for ' + H.traced('3 points: approximate figure + accurate trend + comment')
                  + ', without tying the marks to these rows.')] + [
            point(f'r-{i}', t, None, 'A point the scheme lists.' if i < len(pts) else
                  'Claim the complete assessment: 5 marks in all.')
            for i, t in enumerate(pts, 1)]
    add(f'sb-q7-a-{part}', topic, concept, ref('B', 7, f'(a)({part})'),
        f"{H.q(9, 'Assess the performance of the Irish economy in the past 12 months in each', ' (i)').rstrip('.')}: {H.q(9, area, nxt).rstrip('.')}.",
        '5 (2 + 1 + 2)', 5, rows, kind='questionTotal', **B)
add('sb-q7-b', '3-4', 'regulating-the-banking-sector', ref('B', 7, '(b)'),
    H.q(9, 'Outline the economic advantages of effective regulation of the banking sector.', ' [25]'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'Two advantages for citizens and two for the banking industry', 25, 4, 7,
          side('Citizens', H.split('Provide protection to depositors / consumers', '7+6+6+6',
                                   ['Provide protection to depositors', 'May help consumers make better',
                                    'Confidence in banking sector', 'Secure employment', 'Benefits for taxpayers'], source='cells'))
          + side('Banking sector', H.split('To avoid reckless lending', '39 | P a g e',
                                           ['To avoid reckless lending', 'To maintain stability in the financial system',
                                            'Less prone to shocks', 'To reduce macro-economic instability'], source='block')),
          'A minimum of two for citizens and two for the banking industry. The scheme prices the four on one ladder, not '
          'by side: the first credited 7 marks (3 + 4), the other three 6 each (3 + 3).', steps=[7, 6, 6, 6])],
    kind='fixed', **B)
q7c = H.q(9, 'The Government’s Summer Economic Statement', ' (i)')
pick('sb-q7-c-i', '3-1', 'arguments-for-capital-spending', ref('B', 7, '(c)(i)'),
     H.q(9, 'Explain three economic arguments in favour of an increase', ' (ii)'), 'An argument in favour — any three',
     bl('• Increased demand for housing', '40 | P a g e'), 3, 6, 'Three arguments, 6 marks each (3 + 3).', stem=q7c, **B)
pick('sb-q7-c-ii', '3-1', 'capital-spending-and-other-objectives', ref('B', 7, '(c)(ii)'),
     H.q(9, 'Discuss how this planned expenditure on capital projects', ' [30]'), 'A conflicting objective — any two',
     bl('• Could be inflationary', '⟨30⟩'), 2, 6, 'Two conflicts, 6 marks each (3 + 3).', stem=q7c, **B)

# Q8 ─ national income; FDI; the environment
q8a = ' '.join([H.q(10, 'The table shows National Income (Y)', ' Y'),
                H.q(10, 'Calculate the following, showing all your workings:', ' (i)')])
q8a_table = PAP + 'p10-q8a-table'
for part, concept, ask, nxt, answer, marks, note in (
        ('i', 'national-income-from-the-identity', 'the value of National Income in 2016', ' (ii)',
         H.traced('80,000 + 20,000 + 90,000 – 90,000 = 100,000'), 5,
         'National income, 5 marks, from the scheme’s Y = C + I + G + X – M.'),
        ('ii', 'net-exports', 'the value of Net Exports in 2017', ' (iii)', H.traced('Net exports: 120 000 – 100 000 = 20,000'), 6,
         'Net exports, 6 marks. The scheme first finds M: 150,000 = 100 000 + 30 000 + (120 000 – M), so M = 100 000.'),
        ('iii', 'savings', 'the level of Savings in the economy in 2017', ' (iv)', H.traced('150,000 – 100 000 = 50 000'), 3,
         'Savings, 3 marks, from the scheme’s S = Y - C.')):
    add(f'sb-q8-a-{part}', '3-0', concept, ref('B', 8, f'(a)({part})'), H.q(10, ask, nxt), str(marks), marks,
        [point('r-1', answer, marks, note)], stem=q8a, figure=q8a_table, **B)
add('sb-q8-a-iv', '3-0', 'the-multiplier', ref('B', 8, '(a)(iv)'), H.q(10, 'the size of the Multiplier.', ' [20]'), '6', 6,
    [point('r-1', H.traced('1.25'), 6, 'The multiplier, 6 marks. The scheme sets MPC (0.4), MPM (0.2) and MPS (0.6) and '
           'both methods as fractions; the figure shows them as printed.')],
    stem=q8a, figure=SOL + 'p44-q8aiv-working', **B)
beside_ask(cards[-1], q8a_table)
add('sb-q8-b', '4-1', 'benefits-and-challenges-of-fdi', ref('B', 8, '(b)'),
    H.q(10, 'Discuss the benefits and challenges of Foreign Direct Investment', ' [25]'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'Two benefits and two challenges', 25, 4, 7,
          side('Benefits', H.split('Creates employment (direct and indirect employment)', '7+6+6+6',
                                   ['Creates employment', 'Exports / effect on balance of trade', 'Effect on government revenue',
                                    'Economic growth', 'Benefits to workers’ productivity', 'Increases the attractiveness'],
                                   source='cells'))
          + side('Challenges', H.split('Challenges • Taxation issues', ' allenges Taxation',
                                       ['Taxation issues', 'Effects on Ireland if they re-locate', 'Repatriation of profits',
                                        'Current uncertainties re the location', 'Distribution of benefits'], source='cells')),
          'Two benefits and two challenges. The scheme prices the four on one ladder, not by side: the first credited '
          '7 marks (3 + 4), the other three 6 each (3 + 3).', steps=[7, 6, 6, 6])],
    kind='fixed', **B)
q8c = H.q(10, '‘Official greenhouse gas emission projections', ' (i)')
pick('sb-q8-c-i', '0-2', 'why-governments-protect-the-environment', ref('B', 8, '(c)(i)'),
     H.q(10, 'Outline three economic reasons why protection of the environment', ' (ii)'), 'A reason — any three',
     bl('• Protection of a valuable asset', '45 | P a g e'), 3, 5, 'Three reasons, 5 marks each (2 + 3).', stem=q8c, **B)
add('sb-q8-c-ii', '0-2', 'cutting-carbon-emissions', ref('B', 8, '(c)(ii)'),
    H.q(10, 'Explain one measure each of the following could take', ' [30]'), '3 @ 5 (2 + 3)', 15,
    [heading('r-individuals', H.traced('Individuals') + ' — any one',
             bl('• Cleaner / alternative methods of transport', 'Firms ⟨5⟩', occ=0), 5, 'One measure for individuals, 5 marks (2 + 3).'),
     heading('r-firms', H.traced('Firms') + ' — any one',
             bl('• Cleaner / alternative methods of transport', '46 | P a g e', occ=1), 5, 'One measure for firms, 5 marks (2 + 3).'),
     heading('r-government', H.traced('The Irish Government') + ' — any one',
             bl('• Investment by the government in the', '⟨30⟩'), 5, 'One measure for the government, 5 marks (2 + 3).')],
    kind='fixed', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
