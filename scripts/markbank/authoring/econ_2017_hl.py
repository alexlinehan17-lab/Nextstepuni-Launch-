#!/usr/bin/env python3
"""Economics 2017 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2017-hl-ev.json, made
from a visual sweep of all 8 paper pages and 40 scheme pages before any 2017
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The only prose written here is guidance: tariffs, route
labels and what a figure or a calculation shows.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2017, 'higher', 'LC034ALP000EV')
D = OldDeck(2017, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2017-HL-scheme-'
PAP = 'economics-2017-HL-paper-'
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

# Q1 ─ the opportunity cost of restoring public pay
pick('sa-q1', '3-1', 'opportunity-costs-of-restoring-public-pay', ref('A', 1),
     H.q(2, 'Outline two opportunity costs for the Irish economy', ' (i)'), 'An opportunity cost — any two',
     bl('• Less funds available to improve state services', '2 at 8 marks each'), 2, 8, 'Two opportunity costs, 8 marks each.',
     stem=H.q(2, 'The Irish government is under pressure to restore public sector pay', ' Outline'), **A)

# Q2 ─ true or false: labour and capital
ticks = [('TRUE', 'The labour force includes part-time workers.'),
         ('FALSE', 'Quasi-rent is economic rent earned by a factor of production in the long run.'),
         ('TRUE', 'The market value of an existing bond rises if the rate of interest falls.'),
         ('TRUE', 'Capital Widening refers to the situation where the capital stock is increasing at')]
add('sa-q2', '2-1', 'labour-and-capital-true-or-false', ref('A', 2), H.q(2, 'Indicate by means of a tick', ' STATEMENT'),
    '6 + 4 + 3 + 3', 16,
    [anyN('r-1', 'Each statement ticked correctly', 16, 4, 6,
          [f"{H.traced(t)} — {H.traced(st)}" + (' ' + H.traced('the same rate as the labour force.') if st.endswith('increasing at') else '')
           for t, st in ticks],
          'All four: the 1st correct response 6 marks, the 2nd 4, the 3rd and 4th 3 each. The completed table is shown with '
          'the answer.', steps=[6, 4, 3, 3])],
    kind='fixed', figure=SOL + 'p05-q2-ticks', **A)
beside_ask(cards[-1], PAP + 'p02-q2-table')

# Q3 ─ direct and indirect taxation
add('sa-q3-a', '3-1', 'direct-and-indirect-taxation', ref('A', 3, '(a)'),
    H.q(2, 'Distinguish between Direct Taxation and Indirect Taxation', ' (b)'), '2 x 5 + 2 x 1', 12,
    [point('r-direct', 'Direct Taxation — ' + H.cell('These are taxes on all forms of income or wealth', cells_only=True), 5,
           'Direct taxation, 5 marks.'),
     point('r-indirect', 'Indirect Taxation — ' + H.cell('These are taxes on consumption / spending.', cells_only=True), 5,
           'Indirect taxation, 5 marks.'),
     point('r-direct-example', 'Example — ' + H.cell('PAYE, Corporation Tax, Capital gains tax.', cells_only=True), 1,
           'An example of a direct tax, 1 mark.'),
     point('r-indirect-example', 'Example — ' + H.cell('VAT, Excise Duties, stamp duties.', cells_only=True, whole=True), 1,
           'An example of an indirect tax, 1 mark.')], **A)
add('sa-q3-b', '3-1', 'why-indirect-taxes-are-inequitable', ref('A', 3, '(b)'),
    H.q(2, 'Why are Indirect Taxes sometimes seen as inequitable?', ' (16 marks)'), '4', 4,
    [point('r-1', H.opt('They are inequitable because those on lower incomes pay', '4 marks'), 4, 'The reason, 4 marks.')], **A)

# Q4 ─ limits on credit creation
add('sa-q4', '3-4', 'limits-on-credit-creation', ref('A', 4), H.q(3, 'State three limitations on the power of banks', ' (i)'),
    '6 + 5 + 5', 16,
    [anyN('r-1', 'A limitation — any three', 16, 3, 6,
          [H.traced(x) for x in ('Limited availability of suitable borrowers', 'Limited ability to attract cash deposits',
                                 'Lack of demand for loans / credit by customers', "Customers' demands for cash/Liquidity ratios",
                                 'Controls by European Central Bank/Reserve ratios',
                                 'Ability of banks to raise capital on international markets.')],
          'Three limitations: the first 6 marks, the other two 5 each.', steps=[6, 5, 5])],
    kind='fixed', **A)

# Q5 ─ the flash crash in sterling
pick('sa-q5', '4-2', 'consequences-of-a-weaker-sterling', ref('A', 5),
     H.q(3, 'State and explain two possible economic consequences', ' (i)'), 'An economic consequence — any two',
     H.split('Irish export prices to the UK become relatively more expensive', '2 at 8 marks each',
             ['Irish export prices to the UK', 'Less UK tourists', 'Falling employment in sectors', 'Import prices from UK',
              'Decreased costs of production', 'Reduced FDI from UK firms', 'Creates uncertainty', 'Effect on balance of trade']),
     2, 8, 'Two consequences, 8 marks each.', stem=H.q(3, 'After plans for ‘Brexit’ were revealed', ' State'), **A)

# Q6 ─ long-run equilibrium in monopoly
q6 = H.q(3, 'The diagram below shows a firm operating under conditions of Monopoly.', ' (a)')
q6_fig = PAP + 'p03-q6-diagram'
labels = H.traced('MR, AR (D), MC')
add('sa-q6-a', '2-0', 'labelling-a-monopoly-diagram', ref('A', 6, '(a)'), H.q(3, 'Label the lines/curves in the diagram', ' and'),
    '3 at 2', 6,
    [point(f'r-{x.split()[0].lower()}', x, 2, f'{x}, 2 marks. The labelled diagram is shown with the answer.')
     for x in labels.split(', ')],
    stem=q6, figure=SOL + 'p06-q6-diagram', **A)
beside_ask(cards[-1], q6_fig)
expl = [H.traced(x) for x in ('Equilibrium is where MC = MR .', 'Firms produces Q1 and sells it at P1.', 'Costs are shown at C1.')]
add('sa-q6-b', '2-0', 'long-run-equilibrium-in-monopoly', ref('A', 6, '(b)'),
    H.q(3, 'Use the diagram to explain the long run equilibrium position', ' Explanation'), '11 graded', 11,
    [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate([
        (expl[0], 'The scheme grades the explanation out of 11 and does not price its points.'),
        (expl[1], 'A point the scheme lists.'), (expl[2], 'A point the scheme lists.'),
        (H.opt('SNPs are being earned as AR > AC/', 'or'), 'A point the scheme lists; it also accepts its alternative.'),
        (H.opt('Firm is not efficient at it is not', 'Q1 Quantity'), 'Claim the complete explanation: 11 marks in all.')], 1)],
    kind='questionTotal', stem=q6, figure=SOL + 'p06-q6-diagram', **A)
beside_ask(cards[-1], q6_fig)

# Q7 ─ cross price elasticity
q7 = H.q(4, 'A consumer buys 80 units of Good A', ' Workings')
add('sa-q7-a', '1-4', 'calculating-cross-price-elasticity', ref('A', 7, '(a)'), q7, '8 + 4', 12,
    [point('r-workings', H.traced('= - 4 x 0.95'), 8, 'The workings, 8 marks: 1 for each of the eight items the scheme sets '
           'in its fraction, 40 over −10 times 100 + 90 (190) over 80 + 120 (200). The figure shows it as printed.'),
     point('r-answer', H.traced('= - 3.8'), 4, 'The correct answer, 4 marks (2 + 2).')],
    figure=SOL + 'p07-q7a-working', **A)
add('sa-q7-b', '1-4', 'substitute-or-complement', ref('A', 7, '(b)'),
    H.q(4, 'Is Good A a substitute or a complement to Good B?', ' (17 marks)'), '2 + 3', 5,
    [point('r-answer', H.traced('Good A is a Complement.'), 2, 'Complement, 2 marks.'),
     point('r-reason', H.opt('It has a Negative CED.', 'Workings: 8 items'), 3, 'The reason, 3 marks.')], stem=q7, **A)

# Q8 ─ conflicting policy objectives
add('sa-q8', '3-1', 'conflicting-policy-objectives', ref('A', 8),
    ' '.join([H.q(4, 'Explain how the following Government policy objectives may conflict', ' Economic growth'),
              H.q(4, 'Economic growth versus Balance of Payments equilibrium:', ' Economic growth'),
              H.q(4, 'Economic growth versus a Just Social Policy:', ' (17 marks)')]),
    '12 + 5', 17,
    [anyN('r-1', 'Each conflict explained', 17, 2, 12,
          [f"{H.traced('Economic growth versus Balance of Payments equilibrium:').rstrip(':')} — "
           + H.opt('Economic growth means more employment', 'Economic growth versus a Just'),
           f"{H.traced('Economic growth versus a Just Social Policy:').rstrip(':')} — "
           + H.opt('Economic growth tends to benefit incomes of the better off.', 'Possible example:')],
          'Both conflicts: the first correct response 12 marks, the second 5. For the second the scheme also gives an '
          'example: ' + H.opt('To achieve a just social policy the government may impose', '2 conflicts explained'),
          steps=[12, 5])],
    kind='fixed', **A)

# Q9 ─ third-level fees
add('sa-q9', '3-1', 'third-level-fees', ref('A', 9),
    H.q(4, 'Outline one possible economic advantage and one possible economic disadvantage', ' Economic advantage'),
    '9 + 8', 17,
    [anyN('r-1', 'One advantage and one disadvantage', 17, 2, 9,
          side('Possible economic advantages', H.split('Reduced cost for taxpayers', 'Possible economic disadvantages',
                                                       ['Reduced cost for taxpayers', 'Opportunity costs', 'Incentives',
                                                        'Greater course engagement', 'Fairness', 'HEI funding']))
          + side('Possible economic disadvantages', H.split('Increased debt on individuals', '2 points explained',
                                                            ['Increased debt on individuals', 'May lead to greater inequality',
                                                             'Reduced positive externalities', 'Undermining of certain discipline'])),
          'One advantage and one disadvantage: the first correct response 9 marks, the second 8.', steps=[9, 8])],
    kind='fixed', stem=H.q(4, 'The Irish government is considering the reintroduction', ' Outline'), **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)


def cell_body(first):
    """A bulleted table cell, read whole from the cell rendering: its leading bullet
    and the marks printed at its foot set aside."""
    return H.traced(re.sub(r'\s*\d+ marks$', '', cc('• ' + first)).lstrip('• ').strip())


def slash_items(line):
    """The scheme's own list of marked elements, split where it prints its slashes."""
    return [H.traced(x.strip()) for x in re.split(r'\s*/\s*', line) if x.strip()]


# Q1 ─ concepts; electric cars; rent control
q1a = H.q(5, 'In the case of any two of the following distinguish between the concepts.', ' [25]')
add('sb-q1-a', '1-0', 'distinguishing-market-concepts', ref('B', 1, '(a)'), q1a, '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'Each concept defined — two pairs', 25, 4, 7,
          H.split('The Law of Demand states that as prices rise', '1st correct response',
                  ['The Law of Demand', 'The Law of Supply', 'Consumer Surplus is', 'Producer Surplus is',
                   'Derived Demand is', 'Joint Demand is']),
          'Two pairs, four concepts: the 1st correct response 7 marks, the remaining three 6 each.', steps=[7, 6, 6, 6])],
    kind='fixed', **B)
q1b = H.q(5, 'Assume the market for electric cars is in equilibrium.', ' (i)')
shifts = (
    ('i', 'technological-advance-and-electric-cars', 'A technological advance in the production process of electric cars.',
     '(ii) The motor', 'S/C shifts to the right (S2)', 'Diagram: 5m', 'D / S1 / S2 / Indication of lower equilibrium price, higher quantity',
     'p10-q1bi-diagram'),
    ('ii', 'motor-tax-and-electric-cars', 'The motor tax on petrol engine cars is expected to rise in the near future.',
     '(iii) The government', 'D/C shifts to the right (D2)', 'Diagram: 5m', 'S / D1 / D2 / Indication of higher equilibrium price and quantity',
     'p10-q1bii-diagram'),
    ('iii', 'public-transport-subsidies-and-electric-cars', 'The government increases subsidies on public transport',
     '(c) The average', 'D/C shifts to the left (D2)', 'Diagram: 5m', 'S / D1 / D2 / Indication of lower equilibrium price and quantity',
     'p11-q1biii-diagram'))
for part, concept, ask, nxt, first, end, elements, crop in shifts:
    pts = H.bullets('• ' + first, end, occ=0)
    els = slash_items(elements)
    if ', ' in els[-1]:
        els = els[:-1] + [H.traced(x) for x in els[-1].split(', ')]
    elif ' and ' in els[-1]:
        head, q_ = els[-1].rsplit(' and ', 1)
        els = els[:-1] + [H.traced(head), H.traced(q_)]
    add(f'sb-q1-b-{part}', '1-0', concept, ref('B', 1, f'(b)({part})'), H.q(5, ask, f' {nxt}' if part != 'iii' else ' [30]'),
        'Diagram 5 + explanation 5', 10,
        [anyN('r-diagram', 'The diagram — each element', 5, 5, 1, els,
              'The diagram, 5 marks: 1 for each element the scheme lists. The completed diagram is shown with the answer.'),
         point('r-shift', pts[0], 1, 'The shift, 1 mark.'),
         point('r-price', pts[3], 1, 'The new price, 1 mark.'),
         point('r-quantity', pts[4], 1, 'The new quantity, 1 mark.'),
         anyN('r-reason', 'The reason — any one', 2, 1, 2, pts[1:3], 'The reason behind the change, 2 marks.')],
        kind='fixed', stem=q1b, figure=SOL + crop, **B)
q1c = H.q(5, 'The average monthly rental price for private residential property', ' (i)')
rent_labels = slash_items('P / Q / S / D / € 1,078 / QE / S1 / D1')
add('sb-q1-c-i', '1-3', 'illustrating-a-rent-control', ref('B', 1, '(c)(i)'),
    H.q(5, 'Assume the average monthly equilibrium rental price is €1,078.', ' (ii)'), '8 x 1 + 2', 10,
    [anyN('r-labels', 'Each label — 1 mark', 8, 8, 1, rent_labels,
          'The diagram, 8 marks: 1 for each of the eight labels the scheme lists. The completed diagram is shown with the answer.'),
     point('r-ceiling', H.traced('€715'), 2, 'The €715 maximum rent, 2 marks.')],
    kind='fixed', stem=q1c, figure=SOL + 'p11-q1ci-diagram', **B)
pick('sb-q1-c-ii', '1-3', 'consequences-of-a-rent-control', ref('B', 1, '(c)(ii)'),
     H.q(5, 'Discuss the likely economic consequences of such a rent control', ' [20]'), 'An economic consequence — any two',
     H.split('Effect on demand\nThe rent price', '2 at 5 marks each',
             ['Effect on demand', 'Effect on consumers', 'Effect on landlords', 'Allocation of available supply',
              'Difficulties for government']),
     2, 5, 'Two consequences, 5 marks each (2 + 3).', stem=q1c, **B)

# Q2 ─ perfect competition; artisan food
q2ai = H.q(5, 'Show, by means of two separate labelled diagrams', ' (ii)')
sr = slash_items('P / Q / AC / MC / P = AR = MR / P1 / Q1 / C1 / Equilibrium point')
lr = slash_items('P2 /C2 / Q2 / Equilibrium point')
add('sb-q2-a-i', '2-0', 'short-and-long-run-in-perfect-competition', ref('B', 2, '(a)(i)'), q2ai,
    'Short run 9 at 1 + long run 8', 17,
    [anyN('r-short', 'The short-run diagram — each element', 9, 9, 1, sr,
          'The short-run diagram, 9 marks: 1 for each of the nine elements the scheme lists.'),
     point('r-tangent', H.traced('AC (2m) at a tangent to AR (2m)'), 4,
           'The long-run diagram: AC at a tangent to AR, 2 marks each.'),
     anyN('r-long', 'The long-run diagram — each further element', 4, 4, 1, lr,
          'Then P2, C2, Q2 and the equilibrium point, 1 mark each. Both completed diagrams are shown with the answer.')],
    kind='fixed', figure=SOL + 'p13-q2ai-diagrams', **B)
q2aii = H.q(5, 'Compare the short run equilibrium position with the long run', ' [35]')
add('sb-q2-a-ii', '2-0', 'short-and-long-run-compared', ref('B', 2, '(a)(ii)'), q2aii, '3 x 6', 18,
    [point(f'r-{k}', f'{H.traced(head)} — {text}', 6, f'{head}, 6 marks.') for k, head, text in (
        ('price', 'Price and Output', cell_body('When new firms enter the industry the market price falls')),
        ('profits', 'Profits', cell_body('In the short run the firm earns SNP')),
        ('efficiency', 'Efficiency', cell_body('In the short run as there is SNP there is no incentive')))],
    **B)
q2b = H.q(5, 'The table below shows data for a perfectly competitive firm in equilibrium.', ' Average')
q2b_table = PAP + 'p05-q2b-table'
add('sb-q2-b-i', '2-0', 'marginal-revenue-in-perfect-competition', ref('B', 2, '(b)(i)'),
    H.q(5, 'Using your knowledge of perfect competition, what is the marginal revenue', ' (ii)'), '8 (4 + 4)', 8,
    [point('r-answer', H.traced('In Perfect Competition MR = AR thus MR = €50'), 4, 'The answer, 4 marks.'),
     point('r-reason', H.opt('In perfect competition the firm is a price taker', '8 marks'), 4, 'The explanation, 4 marks.')],
    stem=q2b, figure=q2b_table, **B)
add('sb-q2-b-ii', '2-0', 'should-the-firm-continue', ref('B', 2, '(b)(ii)'),
    H.q(5, 'Should this firm continue in business? Explain your answer.', ' [20]'), '12 (4 + 4 + 4)', 12,
    [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate([
        (H.traced('This firm should continue in business in the short run even though it is making a loss.'),
         'The scheme prices the answer 12 (4 + 4 + 4) without tying each 4 to a line.'),
        (H.opt('The Price (i.e. AR) €50 is below the ATC of €60.', 'The firm is actually'), 'Part of the answer.'),
        (H.opt('The firm is actually covering all of its variable costs', 'Thus, the firm'), 'Part of the answer.'),
        (H.opt('Thus, the firm should continue in business in the short run and absorb', '12 marks'),
         'Claim the complete answer: 12 marks in all.')], 1)],
    kind='questionTotal', stem=q2b, figure=q2b_table, **B)
q2c = H.q(5, 'Bord Bia reported the total value of the Artisan Food market', ' (i)')
add('sb-q2-c-i', '2-0', 'the-artisan-food-market-structure', ref('B', 2, '(c)(i)'),
    H.q(5, 'State a market structure which most closely reflects this situation', ' (ii)'), '4 + 2 x 3', 10,
    [point('r-structure', H.traced('The Artisan Food market is imperfectly competitive (monopolistically competitive).'), 4,
           'The market structure, 4 marks.'),
     anyN('r-reasons', 'A reason — any two', 6, 2, 3,
          H.split('There are many firms in this industry', '2 reasons at 3 marks',
                  ['There are many firms', 'There is freedom of entry', 'Product differentiation exists']),
          'Two reasons, 3 marks each.')],
    kind='fixed', stem=q2c, **B)
add('sb-q2-c-ii', '2-0', 'the-demand-curve-in-imperfect-competition', ref('B', 2, '(c)(ii)'),
    H.q(5, 'Explain the shape of the demand curve of a firm in this market structure.', ' [20]'), '4 + 6', 10,
    [point('r-shape', H.traced('An imperfectly competitive firm faces a downward (negatively) sloping demand curve.'), 4,
           'The shape, 4 marks.'),
     point('r-why', H.opt('Because it sells a differentiated product', '6 mark graded'), 6, 'Why, 6 marks, graded.')],
    stem=q2c, **B)

# Q3 ─ costs; MEC; MRPL
q3a = H.q(6, 'The table below shows the output and the total cost of a firm producing wireless earphones.', ' Output')
q3a_table = PAP + 'p06-q3a-table'
add('sb-q3-a-i', '1-5', 'fixed-and-variable-cost', ref('B', 3, '(a)(i)'),
    H.q(6, 'Calculate the fixed cost and the variable cost when output is 3,000 units.', ' (ii)'), '5', 5,
    [point('r-1', H.opt('FC = €5,000 because at Output 0', ' 5marks'), 5, 'Both costs with their workings, 5 marks.')],
    stem=q3a, figure=q3a_table, **B)
add('sb-q3-a-ii', '1-5', 'average-variable-cost', ref('B', 3, '(a)(ii)'),
    H.q(6, 'Calculate the average variable cost when output is 5,000 units.', ' (iii)'), '5', 5,
    [point('r-1', H.opt('AVC = VC/Q.', ' 5 marks'), 5, 'The average variable cost with its working, 5 marks.')],
    stem=q3a, figure=q3a_table, **B)
add('sb-q3-a-iii', '1-5', 'total-profit', ref('B', 3, '(a)(iii)'), H.q(6, 'Calculate total profit if 4,000 units are sold.', ' (iv)'),
    '4', 4, [point('r-1', H.opt('Total Profit = Total Revenue (P x Q) – Total Cost', ' 4 marks'), 4, 'The profit with its working, 4 marks.')],
    stem=q3a, figure=q3a_table, **B)
outs = ['1,000', '2,000', '3,000', '4,000', '5,000', '6,000']
ac = H.chunk('Average Cost - 13 9 8 8 9', '⟨').split()[3:] + ['10']
mc = H.chunk('Marginal Cost - 8 5 6 8 13', '⟨').split()[3:] + ['15']
add('sb-q3-a-iv', '1-5', 'graphing-average-and-marginal-cost', ref('B', 3, '(a)(iv)'),
    H.q(6, 'Using the data in the table above, draw one graph', ' [30]'), '6 + 6 + 4 at 1', 16,
    [anyN('r-ac', 'Each point on the AC curve (output — AC)', 6, 6, 1, [f'{H.traced(o)} — {H.traced(v)}' for o, v in zip(outs, ac)],
          'The six AC points, 1 mark each, from the scheme’s completed table. The graph is shown with the answer.'),
     anyN('r-mc', 'Each point on the MC curve (output — MC)', 6, 6, 1, [f'{H.traced(o)} — {H.traced(v)}' for o, v in zip(outs, mc)],
          'The six MC points, 1 mark each.'),
     anyN('r-labels', 'Each label', 4, 4, 1, slash_items('Costs / Quantity/MC/AC'), 'The axis and curve labels, 1 mark each.')],
    kind='fixed', stem=q3a, figure=SOL + 'p16-q3aiv-graph', **B)
beside_ask(cards[-1], q3a_table)
add('sb-q3-b-i', '1-5', 'marginal-efficiency-of-capital', ref('B', 3, '(b)(i)'),
    H.q(6, 'Explain the term Marginal Efficiency of Capital (MEC).', ' (ii)'), '10', 10,
    [point('r-1', H.opt('It is the extra profit earned as result of employing one', '10 marks'), 10, 'The explanation, 10 marks.')], **B)
pick('sb-q3-b-ii', '1-5', 'why-mec-falls', ref('B', 3, '(b)(ii)'), H.q(6, 'Outline two possible reasons for a fall in MEC.', ' [20]'),
     'A reason — any two', [H.traced(x) for x in ('Cost of capital increases / Rate of interest increases',
                                                 'Increase in cost of capital goods', 'Selling price of the good falling',
                                                 'Fall in productivity of the extra capital being used.')],
     2, 5, 'Two reasons, 5 marks each (2 + 3).', **B)
q3ci = H.q(6, 'Explain with the aid of a diagram the Marginal Revenue Product', ' (ii)')
add('sb-q3-c-i', '2-1', 'marginal-revenue-product-of-labour', ref('B', 3, '(c)(i)'), q3ci, '5 + 5 + 5', 15,
    [ask_row('r-diagram', q3ci[:q3ci.index(' the Marginal')], 5,
             'The diagram, 5 marks. The scheme’s diagram is shown with the answer.'),
     point('r-explanation', H.opt('The marginal revenue product of labour is the additional revenue', ' 5 marks'), 5,
           'The explanation of MRPL, 5 marks.'),
     anyN('r-other', 'One other point — any one', 5, 1, 5,
          [H.opt('For a competitive profit-maximising firm the MRPL curve', '\nOR'),
           H.opt('The reasons why MRPL slopes downwards:', '\n5 marks\nDiagram')],
          'One other point, 5 marks.')],
    kind='fixed', figure=SOL + 'p17-q3ci-diagram', **B)
pick('sb-q3-c-ii', '2-1', 'mrpl-and-public-sector-pay', ref('B', 3, '(c)(ii)'),
     H.q(6, 'Discuss the reasons why MRPL might not be a suitable method', ' [25]'), 'A reason — any two',
     H.split('Physical output not always produced.', '2 at 5 marks each',
             ['Physical output not always produced.', 'The goods/services produced within public sector', 'When capital and labour']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', **B)

# Q4 ─ national income; the circular flow; uses of national income statistics
add('sb-q4-a-i', '3-0', 'methods-of-measuring-national-income', ref('B', 4, '(a)(i)'),
    H.q(6, 'One method for calculating National Income is the output method.', ' (ii)'), '2 at 6', 12,
    [point('r-income', 'The Income method — ' + H.opt('They can add up all the income earned', 'The expenditure method:'), 6,
           'The income method, 6 marks.'),
     point('r-expenditure', 'The expenditure method — ' + H.opt('They can add the total amount of money spent', '2 at 6 marks'), 6,
           'The expenditure method, 6 marks.')], **B)
add('sb-q4-a-ii', '3-0', 'double-counting', ref('B', 4, '(a)(ii)'),
    H.q(6, 'Describe the problem of ‘double counting’', ' [20]'), '8 graded', 8,
    [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate([
        (H.opt('‘Double counting’ occurs if the expenditure on intermediate goods', 'Sometimes it is very difficult'),
         'The scheme grades the description out of 8 and does not price its paragraphs.'),
        (H.opt('Sometimes it is very difficult to distinguish', '8 marks graded'), 'Claim the complete description: 8 marks in all.')], 1)],
    kind='questionTotal', **B)
q4bi = H.q(6, 'Explain, with the aid of a diagram, the Circular Flow of Income in an open economy.', ' (ii)')
add('sb-q4-b-i', '3-0', 'the-circular-flow-of-income', ref('B', 4, '(b)(i)'), q4bi, 'Diagram 13 + explanation 10', 23,
    [anyN('r-sectors', 'Each sector identified', 5, 5, 1,
          [H.traced(x) for x in ('HOUSEHOLDS', 'FIRMS', 'GOVERNMENT', 'FINANCIAL INSTITUTIONS', 'FOREIGN MARKETS')],
          'The five sectors, 1 mark each.'),
     anyN('r-flows', 'Each flow, its component and direction', 8, 8, 1,
          [H.traced(x) for x in ("Incomes for supplying F.O.P's", 'Spending on the output of firms', 'Tax', 'Government Expenditure',
                                 'Savings', 'Investment', 'Imports', 'Exports')],
          'The eight flows, 1 mark each: the scheme gives ½ for the component and ½ for the direction. The completed diagram is '
          'shown with the answer.'),
     anyN('r-explanation', 'The explanation — each point', 10, 5, 2,
          bl('• Households supply the factors of production', 'Explanation: 10 marks'),
          'The explanation, 10 marks: 2 for each of the five points the scheme lists.')],
    kind='fixed', figure=SOL + 'p20-q4bi-diagram', **B)
add('sb-q4-b-ii', '3-1', 'budget-2017-and-the-circular-flow', ref('B', 4, '(b)(ii)'),
    H.q(6, 'Outline how each of the following Budget 2017 policies should affect', ' [35]'), '6 + 6', 12,
    [point('r-capital', H.traced('Increased Capital spending on road and rail projects of €4.5 billion') + ' — '
           + cell_body('This is an injection into the circular flow'), 6, 'Capital spending, 6 marks.'),
     point('r-usc', H.traced('A reduction in the amount of the universal social charge (USC) that workers must pay.') + ' — '
           + cell_body('This is a reduction in taxes'), 6, 'The USC reduction, 6 marks.')],
    **B)
q4c = H.q(6, 'The CSO recorded an increase in GDP of 26.3%', ' (i)')
pick('sb-q4-c-i', '3-0', 'uses-of-national-income-statistics', ref('B', 4, '(c)(i)'),
     H.q(6, 'Describe three uses of a country’s National Income statistics.', ' (ii)'), 'A use — any three',
     bl('• Indication of alterations in the standard of living.', '3 points at 5 marks'), 3, 5, 'Three uses, 5 marks each (2 + 3).',
     stem=q4c, **B)
pick('sb-q4-c-ii', '3-0', 'an-overestimated-gdp', ref('B', 4, '(c)(ii)'),
     H.q(6, 'Outline an economic implication for the Irish Government', ' [20]'), 'An implication — any one',
     [H.opt('It would make it look like our economy was growing faster', 'Our GDP figures'),
      H.opt('Our GDP figures are used to calculate various ratios', 'It would indicate'),
      H.opt('It would indicate, incorrectly, that our Debt to GDP ratio', '1 at 5 marks')],
     1, 5, 'One implication, 5 marks (2 + 3). ' + H.traced('Other acceptable answers are marked on their merits.'), stem=q4c, **B)

# Q5 ─ absolute and comparative advantage; protection; the terms of trade
add('sb-q5-a-i', '4-2', 'absolute-and-comparative-advantage', ref('B', 5, '(a)(i)'),
    H.q(7, 'Distinguish between the concepts Absolute Advantage and Comparative Advantage', ' (ii)'), '4 + 8 graded', 12,
    [point('r-absolute', 'Absolute Advantage — ' + H.opt('The capability of a county to produce more', 'Comparative Advantage\nThe'), 4,
           'Absolute advantage, 4 marks.'),
     point('r-comparative', 'Comparative Advantage — ' + H.opt('The ability of a country to produce a particular product', 'Any suitable example'), 8,
           'Comparative advantage with a suitable example, 8 marks, graded. The scheme’s further points: '
           + H.opt('Even if one country has an absolute advantage', 'Absolute Advantage: 4 marks'))], **B)
pick('sb-q5-a-ii', '4-2', 'why-one-country-produces-better', ref('B', 5, '(a)(ii)'),
     H.q(7, 'State and explain reasons why one country might be better', ' [30]'), 'A reason — any three',
     bl('• Suitable climate and land quality', '3 at 6marks'), 3, 6, 'Three reasons, 6 marks each (3 + 3).', **B)
q5b = H.q(7, 'In his 1958 study, “Economic Development” T. K. Whitaker', ' (i)')
pick('sb-q5-b-i', '4-2', 'trade-protectionist-measures', ref('B', 5, '(b)(i)'), H.q(7, 'Describe two trade protectionist measures.', ' (ii)'),
     'A protectionist measure — any two',
     H.split('Tariffs\nTax on imports', '2 points at 5 marks each',
             ['Tariffs', 'Quotas', 'Embargoes', 'Administrative barriers', 'Export subsidies', 'Exchange Control regulations']),
     2, 5, 'Two measures, 5 marks each (2 + 3).', stem=q5b, **B)
side_ = lambda label, opts: [f'{H.traced(label)} — {o}' for o in opts]
add('sb-q5-b-ii', '4-2', 'protecting-infant-industries', ref('B', 5, '(b)(ii)'),
    H.q(7, 'Discuss the economic arguments for and against a government introducing', ' [25]'), '3 at 5 (2 + 3)', 15,
    [anyN('r-1', 'An argument for or against — any three', 15, 3, 5,
          side_('For', [cc(x) for x in ('New businesses need to find their feet', 'Some countries might be enticed',
                                        'By imposing tariffs on competing products', 'Infant industry may provide goods')])
          + side_('Against', [cc(x) for x in ('The ‘infant’ industry may have an incentive', 'How does a government choose',
                                              'How long should a government support', 'May lead to retaliation')]),
          'Three arguments, 5 marks each (2 + 3). ' + H.traced('(Must have at least one for and one against)'))],
    kind='fixed', stem=q5b, **B)
q5c = H.q(7, 'The table below shows Ireland’s terms of trade for selected years.', ' Year')
q5c_table = PAP + 'p07-q5c-table'
add('sb-q5-c-i', '4-2', 'terms-of-trade', ref('B', 5, '(c)(i)'), H.q(7, 'Explain the phrase terms of trade.', ' (ii)'), '5', 5,
    [anyN('r-1', 'An explanation — any one', 5, 1, 5, bl('• A country’s terms of trade is a ratio', '5 marks', occ=0),
          'The explanation, 5 marks: any one of the scheme’s statements.')],
    kind='fixed', stem=q5c, figure=q5c_table, **B)
add('sb-q5-c-ii', '4-2', 'calculating-the-terms-of-trade', ref('B', 5, '(c)(ii)'),
    H.q(7, 'Calculate the terms of trade for 2011 from the data in the table above.', ' (iii)'), '5', 5,
    [point('r-1', H.traced('(96.6 / 98.7 ) x 100 = 97.9'), 5, 'The terms of trade with the working, 5 marks.')],
    stem=q5c, figure=q5c_table, **B)
pick('sb-q5-c-iii', '4-2', 'effects-of-improving-terms-of-trade', ref('B', 5, '(c)(iii)'),
     H.q(7, 'Outline the possible effects on the Irish economy of the movement', ' [20]'), 'An effect — any two',
     H.split('Effect on export sector', '2 points at 5 marks each',
             ['Effect on export sector', 'Effect on imports', 'Effect on Employment', 'Effects on Government revenue'], occ=None),
     2, 5, 'Two effects, 5 marks each (2 + 3). ' + H.traced('Other acceptable answers are marked on their merits.'),
     stem=q5c, figure=q5c_table, **B)

# Q6 ─ the CPI; inflation; residential property prices
add('sb-q6-a-i', '3-3', 'calculating-the-cpi', ref('B', 6, '(a)(i)'),
    H.q(7, 'Explain briefly how the Consumer Price Index (CPI) is calculated.', ' (ii)'), '8 graded', 8,
    [point(f'r-{i}', t, None, 'The scheme grades the explanation out of 8 and does not price its steps.' if i == 1
           else 'Claim the complete explanation: 8 marks in all.' if i == 6 else 'A step the scheme lists.')
     for i, t in enumerate(bl('• Choosing a representative base year.', '8 marks graded'), 1)],
    kind='questionTotal', **B)
pick('sb-q6-a-ii', '3-3', 'limitations-of-the-cpi', ref('B', 6, '(a)(ii)'),
     H.q(7, 'Discuss three possible limitations of the CPI', ' [20]'), 'A limitation — any three',
     H.split('Limitations of an average.', '3 at 4 marks',
             ['Limitations of an average.', 'Introduction of new products', 'Rural versus urban lifestyles',
              'Switching by consumers', 'Quality of products', 'Only measures changes to prices', 'Static weights']),
     3, 4, 'Three limitations, 4 marks each (2 + 2).', **B)
add('sb-q6-b-i', '3-3', 'demand-pull-and-cost-push-inflation', ref('B', 6, '(b)(i)'),
    H.q(7, 'Define the terms demand‐pull inflation and cost‐push inflation.', ' (ii)'), '2 at 5', 10,
    [point('r-demand-pull', 'Demand-pull inflation — ' + H.opt('Is a type of inflation that occurs when there is persistent', 'Cost-push inflation\nCost'), 5,
           'Demand-pull inflation, 5 marks.'),
     point('r-cost-push', 'Cost-push inflation — ' + H.opt('Cost-push inflation is caused by persistent', '2 at 5 marks each'), 5,
           'Cost-push inflation, 5 marks.')], **B)
q6bii = H.q(7, 'The Irish inflation rate was at, or close to, 0% between 2013 and 2016.', ' (iii)')
good_h = [cc(x) for x in ('Real wages maintained It is good', 'No decline in standard of living The value',
                         'Better planning Households can plan')]
good_f = [cc(x) for x in ('Improved competitiveness / increased exports', 'Wage costs reduced Trade Unions',
                         'Increased investment Firms may be', 'Better planning As prices and costs')]
bad_h = H.cut_cell('Households Reduced spending', ['Reduced spending', 'Increased debt burden'])
bad_f = H.cut_cell('Firms Reduced demand for output', ['Reduced demand for output', 'Increased debt burden', 'Reduced incentive to expand',
                                                       'No rent reductions', 'Risk of deflation'])
for word, label, hh, ff in (('good', 'A low rate of inflation may be good', good_h, good_f),
                            ('bad', 'A low rate of inflation may be bad', bad_h, bad_f)):
    add(f'sb-q6-b-ii-{word}', '3-3', 'is-low-inflation-good-or-bad', ref('B', 6, '(b)(ii)', word),
        f'{q6bii} Justify the choice: {word.upper()}.', '2 at 5 (2 + 3)', 10,
        [heading('r-households', H.traced('Households') + ' — any one', hh, 5, 'One effect on households, 5 marks (2 + 3).'),
         heading('r-firms', H.traced('Firms') + ' — any one', ff, 5, 'One effect on firms, 5 marks (2 + 3).')],
        kind='fixed', **B)
pick('sb-q6-b-iii', '3-3', 'the-ecb-and-inflation', ref('B', 6, '(b)(iii)'),
     H.q(7, 'Outline how the European Central Bank’s (ECB) monetary policy changes', ' [30]'), 'A monetary policy change — any two',
     [f"{cc(h, whole=True)} — {cc(t)}" for h, t in (('Interest rates', 'If the ECB increase interest rates'),
                                                    ('Money Supply', 'If money supply grows faster'),
                                                    ('Availability of credit', 'If credit becomes more readily'))],
     2, 5, 'Two points, 5 marks each (2 + 3).', **B)
q6c = H.q(7, '“From the trough in early 2013, residential property prices', ' (i)')
pick('sb-q6-c-i', '1-0', 'why-house-prices-rose', ref('B', 6, '(c)(i)'), H.q(7, 'State and explain three factors that caused the price', ' (ii)'),
     'A factor — any three',
     H.split('Recovery in employment and incomes / Confidence', '3 at 5 marks each',
             ['Recovery in employment and incomes', 'Lack of supply', 'Pent up demand for houses', 'Cost of borrowing / incentives',
              'Financial institutions are more stable', 'Increasing urbanisation', 'Demographics', 'Central Bank Guidelines']),
     3, 5, 'Three factors, 5 marks each (2 + 3).', stem=q6c, **B)
pick('sb-q6-c-ii', '1-0', 'consequences-of-rising-house-prices', ref('B', 6, '(c)(ii)'),
     H.q(7, 'Discuss two possible economic consequences of the above situation.', ' [25]'), 'An economic consequence — any two',
     H.split('Increased pressure on the rental market', '2 at 5 marks each',
             ['Increased pressure on the rental market', 'Increased government revenue', 'Increased construction of property',
              'Overheating of the property market', 'Reduction in demand for other goods', 'Lack of affordability',
              'Wealth effect', 'May discourage FDI']),
     2, 5, 'Two consequences, 5 marks each (2 + 3). ' + H.traced('Other acceptable answers are marked on their merits.'), stem=q6c, **B)

# Q7 ─ fiscal terms; privatisation; economists
add('sb-q7-a', '3-1', 'national-debt-fiscal-policy-deficit-and-avoidance', ref('B', 7, '(a)'),
    H.q(8, 'Explain the following terms:', ' [20]'), '4 at 5', 20,
    [point('r-debt', H.opt('National debt is the value of total outstanding debt', 'Fiscal policy\nIs'), 5, 'The national debt, 5 marks.'),
     point('r-fiscal', 'Fiscal policy — ' + H.opt('Is any change in government spending and taxation that is designed', 'Budget deficit is'), 5,
           'Fiscal policy, 5 marks.'),
     point('r-deficit', H.opt('Budget deficit is when total government expenditure exceeds', 'Tax avoidance is'), 5, 'A budget deficit, 5 marks.'),
     point('r-avoidance', H.opt('Tax avoidance is the arranging of one’s affairs', '4 at 5 marks each'), 5, 'Tax avoidance, 5 marks.')], **B)
q7b = H.q(8, 'The National Broadband Plan is the government’s commitment', ' (i)')
add('sb-q7-b-i', '1-3', 'privatisation', ref('B', 7, '(b)(i)'), H.q(8, 'Explain the term privatisation.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('The selling of a state owned company / asset in whole or in part to the private sector.'), 5,
           'The explanation, 5 marks.')], stem=q7b, **B)
add('sb-q7-b-ii', '1-3', 'arguments-on-privatisation', ref('B', 7, '(b)(ii)'),
    H.q(8, 'State and explain the economic arguments for and against privatisation', ' [30]'), '4 at 5 (2 + 3) + 5', 25,
    [anyN('r-arguments', 'An argument for or against — any four', 20, 4, 5,
          side_('For', H.split('Revenue for government\nThe government', 'Possible economic arguments against',
                               ['Revenue for government', 'More competition', 'Employment opportunities', 'Enterprise culture',
                                'Access to finance/overseas markets', 'Greater incentives for innovation',
                                'Shedding of loss making companies', 'Less pressure on the government finances']))
          + side_('Against', H.split('Increased Prices/ falling standards of service', '4 at 5 marks (2 + 3)',
                                     ['Increased Prices/ falling standards', 'Loss of jobs and reduced job security',
                                      'Loss of a State Resource', 'Foreign Ownership', 'Cost of the Sale', 'Curtailment in pay',
                                      'Loss of essential public services', 'Possible abuse of monopoly power'])),
          'Four arguments, 5 marks each (2 + 3). ' + H.traced('Minimum of one point for AND one point against.')),
     anyN('r-example', 'A valid Irish example — any one', 5, 1, 5,
          [H.traced(x) for x in ('Aer Tricity, Energia', 'IAG purchase of Aer Lingus.',
                                 'If Bus Éireann sold its Expressway services its costs may be reduced.',
                                 'Bord Gais (retained the pipeline network).', 'National Lottery and Aer Lingus.')],
          'Reference to any valid example, 5 marks. These are the examples the scheme prints.')],
    kind='fixed', stem=q7b, **B)
economists = [(name, H.bo(start, end)) for name, start, end in (
    ('Adam Smith', 'Adam Smith The pursuit of self', 'Milton Friedman Favoured'),
    ('Milton Friedman', 'Milton Friedman Favoured Monetary policy', 'Karl Marx Labour'),
    ('Karl Marx', 'Karl Marx Labour Theory of Value', 'Thomas Robert Malthus Theory'),
    ('Thomas Robert Malthus', 'Thomas Robert Malthus Theory on Population', 'John Maynard Keynes National'),
    ('John Maynard Keynes', 'John Maynard Keynes National Income', '2 contributions per economist'))]
add('sb-q7-c', '0-0', 'contributions-to-economic-thought', ref('B', 7, '(c)'),
    H.q(8, 'Outline the key contributions to economic thought by any three', ' [25]'), '5 (3+2) + 4 (2+2) x 5', 25,
    [anyN('r-1', 'An economist, with two of the contributions the scheme lists — any three', 25, 3, 9,
          [text for _, text in economists],
          'Three economists, two contributions each: the 1st correct response 5 marks (3 + 2) and each of the rest 4 (2 + 2), '
          'so 9 for the first economist and 8 for each of the other two.', steps=[9, 8, 8])],
    kind='fixed', **B)

# Q8 ─ migration; a growing population; social housing
q8a = H.q(8, 'The information below refers to data taken from the Census of Population', ' Population')
q8a_table = PAP + 'p08-q8a-table'
add('sb-q8-a-i', '3-2', 'natural-increase-and-net-migration', ref('B', 8, '(a)(i)'),
    H.q(8, 'Explain the terms natural increase and net migration.', ' (ii)'), '2 at 5', 10,
    [point('r-natural', H.opt('Natural Increase is the amount that total births exceed', 'Net migration is'), 5, 'Natural increase, 5 marks.'),
     point('r-migration', H.opt('Net migration is defined as the difference', '2 at 5 marks each'), 5, 'Net migration, 5 marks.')],
    stem=q8a, figure=q8a_table, **B)
add('sb-q8-a-ii', '3-2', 'calculating-net-migration', ref('B', 8, '(a)(ii)'),
    H.q(8, 'Using the above data, calculate net migration between 2011 and 2016.', ' (iii)'), '5', 5,
    [point('r-1', H.traced('– 28,558 = Net Migration'), 5, 'Net migration, 5 marks, with the scheme’s workings: population change = '
           'natural increase + net migration; 4,757,976 – 4,588,252 = +169,724 = 198,282 + net migration.')],
    stem=q8a, figure=q8a_table, **B)
add('sb-q8-a-iii', '3-2', 'why-people-emigrate', ref('B', 8, '(a)(iii)'),
    H.q(8, 'State and explain three reasons why people emigrate from Ireland.', ' [30]'), '3 at 5 (2 + 3)', 15,
    [anyN('r-1', 'A push or pull factor — any three', 15, 3, 5,
          side_('Push factors', [cc(x) for x in ('Economic recession in Ireland This', 'Wage rates in Ireland Wage',
                                                 'Various income levies /new taxes The')])
          + side_('Pull factors', [cc(x) for x in ('Job opportunities abroad Those', 'Develop skills abroad Some',
                                                   'Better standard of living The possibility', 'Better lifestyle/ Existence',
                                                   'Immigrants returning to their home countries')]),
          'Three reasons, 5 marks each (2 + 3).')],
    kind='fixed', stem=q8a, **B)
add('sb-q8-b', '3-5', 'consequences-of-a-growing-population', ref('B', 8, '(b)'),
    H.q(8, 'Discuss the economic consequences of Ireland’s increasing population.', ' [25]'), '7 (4 + 3) + 6 + 6 + 6', 25,
    [anyN('r-1', 'An economic consequence — any four', 25, 4, 7,
          H.split('Increased demand for goods & services / Larger domestic market', '4 points: 7',
                  ['Increased demand for goods & services', 'Increased pressure on services',
                   'Increased pressure on the country’s infrastructure', 'Land values / housing shortages', 'Economic Planning',
                   'Government employment strategy', 'Impact on Government finances', 'Dependency ratio']),
          'Four points: the first 7 marks (4 + 3), the other three 6 each (3 + 3).', steps=[7, 6, 6, 6])],
    kind='fixed', stem=H.q(8, 'The 2016 Census of Population in Ireland showed', ' Discuss'), **B)
pick('sb-q8-c', '1-3', 'benefits-of-social-housing', ref('B', 8, '(c)'),
     H.q(8, 'Discuss the social benefits and economic benefits of investment in social housing', ' [20]'), 'A social or economic benefit — any four',
     H.split('Reduced homelessness/reduced poverty and deprivation rates', '4 points at 5 marks',
             ['Reduced homelessness', 'Less Government spending on rent supplements', 'Improved stability /well being',
              'Revitalisation of local communities', 'Economic benefits to local communities', 'Less pressure on private property market',
              'Employment in the construction sector', 'Economic growth /Spending increases']),
     4, 5, 'Four points, 5 marks each (2 + 3). ' + H.traced('Must have a minimum of 1 social AND 1 economic point'),
     stem=H.q(8, 'In December 2016 the European Investment Bank', ' Discuss'), **B)

if __name__ == '__main__':
    emit(cards)
