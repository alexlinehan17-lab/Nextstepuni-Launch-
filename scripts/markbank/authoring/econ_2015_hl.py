#!/usr/bin/env python3
"""Economics 2015 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2015-hl-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2015
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The scheme reprints each question above its answer, so a
slice always starts after the reprinted wording. A stem stops before any
printed table: the table is the crop beside the typed ask (coordinator,
2026-11-04: tables are never typed into a question). The only prose written
here is guidance: tariffs, route labels and what a figure or a calculation
shows.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2015, 'higher', 'LC034ALP000EV')
D = OldDeck(2015, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2015-HL-scheme-'
PAP = 'economics-2015-HL-paper-'
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


def slash_items(line):
    """The scheme's own list of marked elements, split where it prints its slashes."""
    return [H.traced(x.strip()) for x in re.split(r'\s*/\s*', line) if x.strip()]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ choice
add('sa-q1', '0-1', 'why-choice-is-fundamental', ref('A', 1),
    H.q(2, 'Outline why ‘choice’ is fundamental to the study of economics.', ' _'), '8 + 4 + 4', 16,
    [anyN('r-1', 'A point of information — all three', 16, 3, 8,
          [H.traced(x) for x in ('In Economics resources are limited / finite / scarce and have alternative uses',
                                 'wants are unlimited / infinite.',
                                 'As a result choices must be made and these choices involve an opportunity cost.')],
          'Three points of information, as the scheme sets them in bold: the first correct 8 marks, the other two 4 each.',
          steps=[8, 4, 4])],
    kind='fixed', **A)

# Q2 ─ the equi-marginal principle
q2 = None
add('sa-q2-a', '1-1', 'the-equi-marginal-principle', ref('A', 2, '(a)'),
    H.q(2, 'Explain the concept of the Equi-Marginal Principle of Consumer Behaviour.', ' _'), '6', 6,
    [point('r-1', H.opt('Consumers spend their income so that the ratio of marginal utility', '6 marks'), 6, 'The explanation, 6 marks.')], **A)
# The paper's answer box sits inside the ask's sentence ("5 bottles Workings: of water").
q2b = H.q(2, 'In equilibrium, a consumer buys 5 bottles', ' Answer:').replace(' Workings:', '')
add('sa-q2-b', '1-1', 'the-equi-marginal-principle-in-numbers', ref('A', 2, '(b)'), q2b, '7 + 3', 10,
    [point('r-working', H.traced('5/€2.50 = €3 x'), 7,
           'The working, 7 marks: MU of water over its price equals MU of bagels over theirs, 5 over €2.50 = x over €3. '
           'The figure shows it as printed.'),
     point('r-answer', H.traced('x = 6 utils (the marginal utility of the 8th bagel)'), 3, 'The correct answer, 3 marks.')],
    figure=SOL + 'p05-q2b-working', **A)

# Q3 ─ the NTMA and bond yields
add('sa-q3-a', '3-1', 'the-ntma', ref('A', 3, '(a)'),
    H.q(2, 'Outline the primary responsibility of the National Treasury Management Agency', ' _'), '8', 8,
    [point('r-1', H.opt('Its core function is borrowing for the exchequer', '8 marks'), 8, 'The responsibility, 8 marks.')], **A)
add('sa-q3-b', '3-1', 'low-bond-yields', ref('A', 3, '(b)'),
    H.q(2, 'Is selling bonds at a low yield good or bad for the Irish Government?', ' _'), '2 + 6', 8,
    [point('r-answer', H.traced('Answer: It is good for the Irish government.'), 2, 'The answer, 2 marks.'),
     heading('r-explanation', 'An explanation — any one',
             [H.traced(x) for x in ('It means the cost to the government of raising money / borrowing money is reduced',
                                    'It means the bond buyers have confidence in the Irish economy and are prepared to buy Irish bonds.',
                                    'It means that the deficit will be smaller / it is cheaper to fund government services.')],
             6, 'One explanation, 6 marks.')],
    kind='fixed', stem=H.q(2, '“The NTMA sells bonds worth €4bn at a low yield', ' (b)'), **A)

# Q4 ─ oligopoly
q4 = H.q(3, 'A high concentration ratio is a key feature of an Oligopolistic Market.', ' (a)')
add('sa-q4-a', '2-0', 'the-concentration-ratio', ref('A', 4, '(a)'), H.q(3, 'Explain this statement and give one example.', ' _'), '6 + 2', 8,
    [point('r-explanation', H.opt('A high concentration ratio exists in an industry if a small number of firms', '6 marks'), 6,
           'The explanation, 6 marks.'),
     heading('r-example', 'An example — any one',
             slash_items(H.opt('Grocery trade in Ireland / Banking', 'Example: 2marks')), 2, 'One example, 2 marks.')],
    kind='fixed', stem=q4, **A)
pick('sa-q4-b', '2-0', 'how-oligopolists-behave', ref('A', 4, '(b)'), H.q(3, 'Outline two ways oligopolists behave in the market:', ' (i)'),
     'A way — any two',
     H.split('Firms act in a way that affects the behaviour', '2 ways at 4 marks',
             ['Firms act in a way', 'Firms can compete via non-price', 'Firms may engage in collusive']),
     2, 4, 'Two ways, 4 marks each.', stem=q4, **A)

# Q5 ─ indirect taxation
q5 = H.q(3, '“Indirect taxes can be regressive but they also have advantages for governments.”', ' (a)')
add('sa-q5-a', '3-1', 'a-regressive-tax', ref('A', 5, '(a)'), H.q(3, 'Explain what is meant by a regressive tax.', ' _'), '8', 8,
    [point('r-1', H.opt('Takes a higher percentage of income from low income taxpayers', 'Explanation: 8 marks'), 8,
           'The explanation, 8 marks.')], stem=q5, **A)
pick('sa-q5-b', '3-1', 'advantages-of-indirect-taxation', ref('A', 5, '(b)'),
     H.q(3, 'Outline two advantages of indirect taxation for governments:', ' (i)'), 'An advantage — any two',
     H.split('Low collection cost / convenient collection', '2 advantages at 4 marks each',
             ['Low collection cost', 'Hard to avoid', 'Less distortionary', 'Could be politically more popular',
              'Government can change consumption patterns']),
     2, 4, 'Two advantages, 4 marks each.', stem=q5, **A)

# Q6 ─ the Classical economists
add('sa-q6', '0-0', 'the-classical-economists', ref('A', 6),
    H.q(3, 'Outline two main contributions to economic thought put forward by the Classical Economists:', ' (i)'), '9 + 8', 17,
    [anyN('r-1', 'A contribution — any two', 17, 2, 9,
          H.split('Efficiency of free markets\nClassical', '9 marks (4 + 5)',
                  ['Efficiency of free markets', 'Self-adjusting mechanism', 'Laissez faire', 'Freedom for the individual', 'Free trade']),
          'Two contributions: the first correct 9 marks (4 + 5), the second 8 (4 + 4).', steps=[9, 8])],
    kind='fixed', **A)

# Q7 ─ elasticity: true or false
ticks = [('TRUE', 'A good with an income elasticity of demand (YED) of +2.5 is a luxury good.'),
         ('TRUE', 'If the cross-price elasticity of demand (CED) is negative then it may be said'),
         ('FALSE', 'When demand is price elastic, a reduction in price will lead to a decrease in'),
         ('TRUE', 'When many close substitute goods are available, demand for any one of them')]
tails = {'If the cross-price': 'that the goods are complements.', 'When demand is price': 'total revenue.',
         'When many close': 'should be highly elastic.'}
statements = [s + next((' ' + H.traced(t) for k, t in tails.items() if s.startswith(k)), '') for _, s in ticks]
add('sa-q7', '1-4', 'elasticity-true-or-false', ref('A', 7),
    # The four printed statements follow the ask: the card cannot be answered without them.
    f"{H.q(4, 'Read each statement below and indicate if the statement is true or false.', ' STATEMENT')} "
    f"{H.q(4, 'A good with an income elasticity of demand (YED) of +2.5', ' (17 marks)')}", '5 + 4 + 4 + 4', 17,
    [anyN('r-1', 'Each statement ticked correctly', 17, 4, 5,
          [f'{H.traced(t)} — {H.traced(s)}' for (t, _), s in zip(ticks, statements)],
          'All four: the 1st correct response 5 marks, the other three 4 each.', steps=[5, 4, 4, 4])],
    kind='fixed', **A)

# Q8 ─ the euro against the dollar
q8 = H.q(4, '“The Euro (€) is hitting a four and a half year low against the US $.”', ' Explain')
add('sa-q8-a', '4-2', 'a-weaker-euro', ref('A', 8, '(a)'), H.q(4, 'Explain what the above statement means.', ' _'), '7', 7,
    [point('r-1', H.opt('The price of the euro has fallen in terms of the $', '7 marks'), 7, 'The explanation, 7 marks.')], stem=q8, **A)
pick('sa-q8-b', '4-2', 'effects-of-a-weaker-euro', ref('A', 8, '(b)'),
     H.q(4, 'Outline two possible economic effects of this development for the Irish economy:', ' (i)'), 'An effect — any two',
     side('Possible positive economic effects', H.split('Irish exports to USA become relatively cheaper', 'Possible negative economic effects:',
                                                        ['Irish exports to USA', 'Increased employment due to', 'FDI may be encouraged']))
     + side('Possible negative economic effects', H.split('Irish imports from USA become relatively more expensive', '2 effects at 5 marks each',
                                                          ['Irish imports from USA', 'Reduced profits for Irish', 'As many of Ireland’s imports'])),
     2, 5, 'Two effects, 5 marks each, positive or negative.', stem=q8, **A)

# Q9 ─ life expectancy
add('sa-q9', '3-5', 'a-longer-life-expectancy', ref('A', 9),
    H.q(4, 'Outline two possible economic implications of this development', ' (i)'), '2 x 6 + 5', 17,
    [anyN('r-implications', 'An economic implication — any two', 12, 2, 6,
          H.split('Can cause higher dependency ratio', '2 implications at 6 marks each',
                  ['Can cause higher dependency ratio', 'More demands on government services', 'Increased budget or change',
                   'A change in the pattern of demand', 'Increased pressure on pensions', 'Possible increased tax burden',
                   'Preference change:']), 'Two implications, 6 marks each.'),
     heading('r-policy', 'A policy measure — any one',
             H.split('Extend retirement age to reduce', 'One policy measure: 5 marks',
                     ['Extend retirement age', 'Seek to expand the working population', 'Reform the pension system',
                      'Health and social services plan', 'Educating the younger population']), 5, 'One policy measure, 5 marks.')],
    kind='fixed', stem=H.q(4, '“Since 1990 Ireland has achieved the largest gain in life expectancy', ' Outline'), **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')

# Q1 ─ the market for 4G TVs; shifts in the wheat market; a rent ceiling
q1a = H.q(5, 'The table below refers to the market data for 4G High Definition Televisions (TVs).', ' Quantity Demanded')
q1a_table = PAP + 'p05-q1a-table'
add('sb-q1-a-i', '1-0', 'drawing-the-4g-tv-market', ref('B', 1, '(a)(i)'),
    H.q(5, 'Using the above data, draw a diagram showing the market demand', ' (ii)'), '6 + 6 + 2 + 2', 16,
    [point('r-demand', H.traced('D/C: 5 points x 1 mark each + Correct label x 1 mark.'), 6,
           'The demand curve, 6 marks. The completed graph is shown with the answer.'),
     point('r-supply', H.traced('S/C: 5 points x 1 mark each + Correct label x 1 mark.'), 6, 'The supply curve, 6 marks.'),
     point('r-axes', H.traced('Price & Quantity axes: 2 x 1 mark each.'), 2, 'The two axes, 2 marks.'),
     point('r-equilibrium', H.traced('Equilibrium price + equilibrium Quantity: 2 x 1 mark each.'), 2,
           'The equilibrium price (€600) and quantity (50,000), 2 marks.')],
    stem=q1a, figure=SOL + 'p09-q1ai-graph', **B)
beside_ask(cards[-1], q1a_table)
add('sb-q1-a-ii', '1-0', 'how-equilibrium-is-reached', ref('B', 1, '(a)(ii)'),
    H.q(5, 'Define the concept market equilibrium.', ' (30)'), '10 + 4', 14,
    [point('r-definition', H.opt('Market equilibrium arises where the quantity demanded equals the quantity supplied', '10 marks (6 + 4)'), 10,
           'The definition, 10 marks (6 + 4).'),
     heading('r-how', 'How equilibrium is arrived at — either route',
             [H.opt('If the price on the market is below the equilibrium price of €600', 'OR'),
              H.opt('If the price on the market is above the equilibrium price of €600', '4 marks')], 4,
             'The explanation, 4 marks: by excess demand or by excess supply.')],
    kind='fixed', stem=q1a, figure=q1a_table, **B)
q1b = H.q(5, 'The market for wheat is in equilibrium.', ' (i)')
shifts = (
    ('i', 'wet-weather-and-wheat', 'Exceptionally wet weather conditions', ' (ii)', 'S/C shifts to the left (S2)',
     'Diagram: D / S1 / S2 / Indication of Higher Price and lower quantity', 'p10-q1bi-diagram'),
    ('ii', 'wheat-allergies-and-demand', 'An increasing percentage of the population is suffering', ' (iii)', 'D/C shifts to the left (D2)',
     'Diagram: S / D1 / D2 / Indication of lower price and lower quantity', 'p11-q1bii-diagram'),
    ('iii', 'cheaper-oil-and-wheat', 'A decrease in the price of oil.', ' (30)', 'S/C shifts to the right (S2)',
     'Diagram: D / S1 / S2 / Indication of lower Price and higher quantity', 'p11-q1biii-diagram'))
# The scheme prints the new equilibrium as P_E with a raised 2 (scheme pp10-11, rendered
# and looked at); the text layer flattens it to "PE 2", so the mark is set back as the
# superscript it is (the build folds ² to 2 to compare).
raise2 = lambda t: re.sub(r'\b([PQ]E) 2\b', r'\1²', t)
for part, concept, ask, nxt, first, elements, crop in shifts:
    pts = [raise2(x) for x in H.bullets('• ' + first, 'Diagram:', occ=0)]
    els = slash_items(elements.split(': ', 1)[1])
    head, q_ = els[-1].rsplit(' and ', 1)
    els = els[:-1] + [H.traced(head), H.traced(q_)]
    add(f'sb-q1-b-{part}', '1-0', concept, ref('B', 1, f'(b)({part})'), H.q(5, ask, nxt), 'Diagram 5 + explanation 5', 10,
        [anyN('r-diagram', 'The diagram — each element', 5, 5, 1, els,
              'The diagram, 5 marks: 1 for each element the scheme lists. The completed diagram is shown with the answer.'),
         point('r-shift', pts[0], 1, 'The shift, 1 mark.'),
         point('r-price', pts[-2], 1, 'The new price, 1 mark.'),
         point('r-quantity', pts[-1], 1, 'The new quantity, 1 mark.'),
         point('r-reason', pts[1], 2, 'The reason for the shift, 2 marks. The scheme’s other bullets set out how the '
               'market moves to the new equilibrium.')],
        kind='fixed', stem=q1b, figure=SOL + crop, **B)
pick('sb-q1-c', '1-3', 'a-rent-ceiling', ref('B', 1, '(c)'),
     H.q(5, 'Advise the Minister for the Environment on the possible economic consequences', ' (15)'), 'A consequence — any three',
     H.split('Shortage of accommodation\nIf the price', '3 points at 5 marks each (2 + 3)',
             ['Shortage of accommodation', 'Lower Rents', 'Allocation by alternative methods', 'Reduced mobility',
              'Quality of accommodation', 'Black Market', 'Lower supply of available housing']),
     3, 5, 'Three consequences, 5 marks each (2 + 3).',
     stem=H.q(5, 'Following recent sharp increases in the price of private rented accommodation', ' Advise'), **B)

# Q2 ─ monopoly; price discrimination; regulating Irish Water
pick('sb-q2-a-i', '2-0', 'barriers-to-entry', ref('B', 2, '(a)(i)'),
     H.q(6, 'State and explain two examples of barriers to entry', ' (ii)'), 'A barrier — any two',
     H.split('Legal / statutory restrictions', '2 points at 5 marks (2 + 3)',
             ['Legal / statutory restrictions', 'Trade Agreements / market sharing', 'Ownership of a key resource',
              'Industry requires a large investment', 'Mergers / Takeovers', 'Limit pricing', 'Brand dominance of a large supplier',
              'Natural monopoly / economies of scale', 'Ownership of a patent / copyright']),
     2, 5, 'Two barriers, 5 marks each (2 + 3).', **B)
diagram_points = [H.traced(x) for x in ('Price axis', 'Quantity axis', 'AR', 'MR', 'MC', 'AC', 'Correct Equilibrium point - E',
                                        'P1', 'C1', 'Q1', 'Profits shown')]
add('sb-q2-a-ii', '2-0', 'long-run-equilibrium-in-monopoly', ref('B', 2, '(a)(ii)'),
    H.q(6, 'Explain, with the aid of a diagram, the long run equilibrium position of a monopolist.', ' (35)'), '11 + 3 + 3 + 2 + 3 + 3', 25,
    [anyN('r-diagram', 'The diagram — each point', 11, 11, 1, diagram_points,
          'The diagram, 11 marks: ' + H.traced('Diagram: 11 points at 1 mark each.') + ' The completed diagram is shown with the answer.'),
     point('r-equilibrium', f"{H.traced('1. Equilibrium')} — {H.traced('Occurs at point E where')} {H.traced('MC = MR [and MC is rising]')}", 3,
           'Equilibrium, 3 marks: 1 for point E, 2 for MC = MR with MC rising.'),
     point('r-output', f"{H.traced('2. Price / Output')} — {H.traced('The firm produces Q1')} {H.traced('and sells it at P1')}", 3,
           'Price and output, 3 marks: 2 for Q1, 1 for P1.'),
     point('r-cost', f"{H.traced('3. Cost')} — {H.traced('The cost of producing this output is shown at point C1')}", 2, 'The cost, 2 marks.'),
     point('r-snp', f"{H.traced('4. SNP')} — {H.traced('The firm is earning SNP [P1 C1D B]')} "
                    f"{H.traced('because AR > AC or they can continue to exist due to barriers to entry.')}", 3,
           'Supernormal profit, 3 marks: 1 for the SNP shown, 2 for why it lasts.'),
     point('r-waste', f"{H.traced('5. Waste of Scarce Resources / Inefficiency')} — "
                      f"{H.traced('The firm is not producing at the lowest point on the AC curve')}", 3,
           'Inefficiency, 3 marks: 1 for the head, 2 for the lowest point of AC. The scheme’s explanation totals 14.')],
    kind='fixed', figure=SOL + 'p14-q2aii-diagram', **B)
q2b = H.q(6, 'A monopolist can increase its profits by engaging in price discrimination.', ' (i)')
add('sb-q2-b-i', '2-0', 'price-discrimination', ref('B', 2, '(b)(i)'),
    H.q(6, 'Explain the concept price discrimination, using a suitable example.', ' (ii)'), '8 + 2', 10,
    [point('r-explanation', H.opt('When the same goods or services are sold to different consumers', '8 marks'), 8,
           'The explanation, 8 marks.'),
     heading('r-example', 'An example — any one',
             H.split('By location (different regions', '2 marks',
                     ['By location', 'By demographic', 'By time', 'By status']), 2, 'One example, 2 marks.')],
    kind='fixed', stem=q2b, **B)
pick('sb-q2-b-ii', '2-0', 'conditions-for-price-discrimination', ref('B', 2, '(b)(ii)'),
     H.q(6, 'State and explain the market conditions necessary for price discrimination', ' (25)'), 'A condition — all three',
     H.split('Some monopoly / market power', '3 conditions at 5 marks each (2 + 3)',
             ['Some monopoly / market power', 'Separation of markets', 'Different consumer price elasticities']),
     3, 5, 'Three conditions, 5 marks each (2 + 3).', stem=q2b, **B)
pick('sb-q2-c', '1-3', 'regulating-irish-water', ref('B', 2, '(c)'),
     H.q(6, 'Discuss whether or not Irish Water (Uisce Éireann)', ' (15)'), 'A reason, for or against — any three',
     side('Arguments why Irish Water should be regulated',
          H.split('Pricing: ensure that consumers are charged a fair price', 'Arguments why Irish Water should not be regulated',
                  ['Pricing: ensure', 'Quality: provision of clean water', 'Invest in infrastructure', 'Protection of the environment']))
     + side('Arguments why Irish Water should not be regulated',
            H.split('Laissez faire policies should be pursued', '3 reasons at 5 marks each (2 + 3)',
                    ['Laissez faire policies', 'Prices should be determined by the market', 'Irish Water can generate funds'])),
     3, 5, 'Three reasons, 5 marks each (2 + 3), for or against.',
     stem=H.q(6, 'The Commission for Energy Regulation (CER)', ' Discuss'), **B)

# Q3 ─ costs and profit; the bakery's costs; economies of scale
add('sb-q3-a', '1-5', 'cost-and-profit-concepts', ref('B', 3, '(a)'),
    H.q(6, 'In the case of any two of the following three pairs distinguish between the two concepts:', ' (20)'), '4 x 5', 20,
    [anyN('r-1', 'Each concept explained — two pairs', 20, 4, 5,
          H.split('Marginal cost\nIs the addition', '4 explanations at 5 marks each',
                  ['Marginal cost', 'Average cost', 'Explicit cost', 'Implicit cost', 'Normal Profit', 'Supernormal profit']),
          'Two pairs, both concepts of each: 4 explanations, 5 marks each.')],
    kind='fixed', **B)
q3b = H.q(6, 'The table below shows the output and production costs for a small bakery.', ' Units of')
q3b_table = PAP + 'p06-q3b-table'
add('sb-q3-b-i', '1-5', 'the-bakerys-costs', ref('B', 3, '(b)(i)'),
    H.q(6, 'Use the data in the table above to answer the following questions:', ' (ii)'), '6 + 3 + 3', 12,
    [point('r-fixed', H.traced('Fixed costs: €100. To produce 0 units costs €100 so these are the fixed costs.'), 6,
           'The fixed costs with the reason, 6 marks.'),
     point('r-variable', H.traced('Total Variable Costs of 300 loaves: €330 – €100 = €230'), 3, 'The variable costs, 3 marks.'),
     point('r-average', H.traced('€0.90 per loaf'), 3,
           'The average cost, 3 marks: total cost over total output, €360 over 400. The figure shows the working as printed.')],
    stem=q3b, figure=SOL + 'p18-q3bi-working', **B)
beside_ask(cards[-1], q3b_table)
add('sb-q3-b-ii', '1-5', 'graphing-the-bakerys-costs', ref('B', 3, '(b)(ii)'),
    H.q(6, 'Using the data from the table above, draw one graph showing the following', ' (iii)'), '2 + 4 + 7 + 7', 20,
    [point('r-labels', H.traced('Labels: Costs / Qty'), 2, 'The two axis labels, 2 marks (2 at 1 mark each). The completed graph is shown with the answer.'),
     point('r-fc', H.traced('Graph of total fixed costs:'), 4, 'The FC line, 4 marks.'),
     point('r-tc', H.traced('Graph of total cost:'), 7, 'The TC curve, 7 marks (2 + 2 + 3): '
           + H.traced('(Start point / end point + correct trend)') + '.'),
     point('r-vc', H.traced('Graph of total variable cost:'), 7, 'The VC curve, 7 marks (2 + 2 + 3), the same way.')],
    stem=q3b, figure=SOL + 'p18-q3bii-graph', **B)
beside_ask(cards[-1], q3b_table)
add('sb-q3-b-iii', '1-5', 'the-short-run', ref('B', 3, '(b)(iii)'),
    H.q(6, 'With reference to the graph you have drawn in part (ii)', ' (35)'), '3', 3,
    [point('r-1', H.traced('The graph represents the short run'), None,
           'The scheme prices the answer and its reason 3 together and does not say which earns which.'),
     point('r-2', H.traced('Fixed costs only exist in the short run / at least one of the factors of production being used is fixed in quantity.'),
           None, 'Claim the complete answer: 3 marks in all.')],
    kind='questionTotal', stem=q3b, **B)
pick('sb-q3-c', '1-5', 'economies-and-diseconomies-of-scale', ref('B', 3, '(c)'),
     H.q(6, 'Discuss possible economies of scale and diseconomies of scale that the bakery', ' (20)'), 'An economy or diseconomy — any four',
     side('Possible economies of scale for the bakery',
          bl('• Technical economies of scale', 'Possible diseconomies of scale for the bakery'))
     + side('Possible diseconomies of scale for the bakery', bl('• Managerial diseconomies', '4 points at 5 marks each')),
     4, 5, 'Four points, 5 marks each (2 + 3). ' + H.traced('Must have a minimum of one economy / diseconomy.') + ' '
     + H.traced('Reference must be made to the bakery'), **B)

# Q4 ─ enterprise and profit; capital, investment and the railways; Keynes's motives
pick('sb-q4-a-i', '0-1', 'characteristics-of-enterprise', ref('B', 4, '(a)(i)'),
     H.q(7, 'State and explain two economic characteristics of enterprise', ' (ii)'), 'A characteristic — any two',
     H.split('Enterprise can earn a loss', '2 characteristics at 5 marks each (2 + 3)',
             ['Enterprise can earn a loss', 'Returns can vary', 'Return is residual']),
     2, 5, 'Two characteristics, 5 marks each (2 + 3).', **B)
pick('sb-q4-a-ii', '1-5', 'why-profits-matter', ref('B', 4, '(a)(ii)'),
     H.q(7, 'Explain the importance of profits in a market economy.', ' (30)'), 'A reason — any four',
     H.split('Encourages risk taking and entrepreneurship', '4 points at 5 marks each (2+3)',
             ['Encourages risk taking', 'Indicates the best use of resources', 'Encourages investment', 'Provide funds for expansion',
              'Profits reward innovation', 'Source of revenue for the government']),
     4, 5, 'Four points, 5 marks each (2 + 3).', **B)
add('sb-q4-b-i', '0-1', 'capital-and-investment', ref('B', 4, '(b)(i)'),
    H.q(7, 'Distinguish between the terms capital and investment as used by economists.', ' (ii)'), '2 x 5', 10,
    [heading('r-capital', H.traced('Capital') + ' — any one statement',
             [H.traced(x) for x in ('Capital anything made by man used in the production of goods and services.',
                                    'Capital refers to the equipment/machinery used in the production process.',
                                    'Capital is a stock concept.')], 5, 'Capital, 5 marks.'),
     heading('r-investment', H.traced('Investment') + ' — any one statement',
             [H.traced(x) for x in ('Investment involves the production of capital goods / capital formation.',
                                    'In economics investment relates to a firm buying new capital, such as machinery or factory buildings.',
                                    'It is any addition /increase to the capital stock/spending on capital equipment. It is a flow concept.')],
             5, 'Investment, 5 marks.')],
    kind='fixed', **B)
pick('sb-q4-b-ii', '3-1', 'investing-in-the-railways', ref('B', 4, '(b)(ii)'),
     H.q(7, 'Discuss the case for and against the Government investing in Ireland’s railways.', ' (30)'), 'A point for or against — any four',
     side('The case for', H.split('Facilitates geographic mobility', 'The case against:',
                                  ['Facilitates geographic mobility', 'Balanced regional development', 'Less traffic gridlock',
                                   'Relatively environmentally friendly', 'Capital intensive investment', 'Improved infrastructure',
                                   'Social benefit']))
     + side('The case against', H.split('Very capital intensive', '4 points at 5 marks each (2 + 3)',
                                        ['Very capital intensive', 'It is a very long term investment', 'Opportunity cost',
                                         'Reduction in the demand for rail services', 'Commitment to on-going subsidies',
                                         'Increased competition from bus companies'])),
     4, 5, 'Four points, 5 marks each (2 + 3). ' + H.traced('Must have a minimum of one argument in favour / one against'), **B)
q4c = H.q(7, 'State and explain the three motives put forward by John Maynard Keynes', ' (ii)')
motives = (('transactionary', 'Transactionary', 'People desire to hold money for day-to- day spending', 'Level of income: People on higher incomes'),
           ('precautionary', 'Precautionary', 'People hold money for emergencies', 'Level of income: The higher the level of income'),
           ('speculative', 'Speculative', 'People desire to hold money for any possible profitable', 'Interest rates: If interest rates are high'))
add('sb-q4-c-i', '3-4', 'keynes-motives-for-holding-money', ref('B', 4, '(c)(i)'), q4c, '3 x 3 (1 + 2)', 9,
    [point(f'r-{k}', f'{cc(name, whole=True)} — {cc(expl)}', 3, f'{name}, 3 marks: 1 for the motive, 2 for its explanation '
           '(the scheme’s 3 at 5 marks (1 + 2 + 2), its Statement and Explanation columns).')
     for k, name, expl, _ in motives], **B)
add('sb-q4-c-ii', '3-4', 'influences-on-each-motive', ref('B', 4, '(c)(ii)'),
    H.q(7, 'Outline one main influence on each motive.', ' (15)'), '3 x 2', 6,
    [point(f'r-{k}', f'{cc(name, whole=True)} — {cc(infl)}', 2, f'The influence on the {name.lower()} motive, 2 marks '
           '(the scheme’s One main influence column).')
     for k, name, _, infl in motives], stem=q4c, **B)

# Q5 ─ credit creation and regulation; mortgage rules; SME funding
pick('sb-q5-a-i', '3-4', 'limits-on-credit-creation', ref('B', 5, '(a)(i)'),
     H.q(7, 'Outline three factors that limit the ability of banks to create credit.', ' (ii)'), 'A factor — any three',
     H.split('Availability of creditworthy customers', '3 factors at 6 marks each (3 + 3)',
             ['Availability of creditworthy customers', 'Cash deposits in the banks', 'Demand for loans', 'Customers\' demands for cash',
              'Guidelines by European Central Bank']),
     3, 6, 'Three factors, 6 marks each (3 + 3).', **B)
pick('sb-q5-a-ii', '3-4', 'why-regulate-the-financial-system', ref('B', 5, '(a)(ii)'),
     H.q(7, 'Discuss the economic reasons why the financial system in Ireland should be regulated.', ' (30)'), 'A reason — any two',
     H.split('To provide a degree of protection to depositors', '2 reasons at 6 marks each (3 + 3)',
             ['To provide a degree of protection', 'To ensure proper lending procedures', 'To maintain the stability',
              'To reduce macro-economic instability']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', **B)
add('sb-q5-b', '3-4', 'mortgage-lending-rules', ref('B', 5, '(b)'),
    H.q(7, 'State and explain the possible economic impacts of these restrictions', ' (20)'), '7 + 7 + 6', 20,
    [anyN('r-1', 'An impact — any three', 20, 3, 7,
          H.split('Could ease the trend of rising property prices', '3 impacts:',
                  ['Could ease the trend', 'Potential supply effect', 'Could lead to lower levels of construction',
                   'Greater safety around the mortgage', 'Help stabilise the business cycle', 'Could hinder the recovery']),
          'Three impacts: ' + H.traced('3 impacts: 7 marks (4 + 3) + 7 marks (4 + 3) + 6 marks (3 + 3)') + '.', steps=[7, 7, 6])],
    kind='fixed', stem=H.q(7, 'In January 2015, the Central Bank of Ireland (CBI) introduced', ' State'), **B)
add('sb-q5-c', '3-4', 'funding-for-smes', ref('B', 5, '(c)'),
    H.q(7, 'Discuss the possible economic benefits of increased access to funding for the SME sector', ' (25)'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'A benefit — any four', 25, 4, 7,
          H.split('Create job / training opportunities', '4 benefits:',
                  ['Create job / training', 'Encourage entrepreneurship', 'Flexible/Able to adapt', 'Local development improvements',
                   'Government finances improve', 'Balance of payments', 'Reduced reliance on FDI']),
          'Four benefits: ' + H.traced('4 benefits: 7 marks (4 + 3) + 3 at 6 marks (3 + 3)') + '.', steps=[7, 6, 6, 6])],
    kind='fixed', stem=H.q(7, 'The Strategic Banking Corporation of Ireland (SBCI)', ' Discuss'), **B)

# Q6 ─ the CPI and deflation; types of unemployment; unemployment statistics
q6a = H.q(8, '“Prices on average as measured by the Consumer Price Index (CPI)', ' (i)')
add('sb-q6-a-i', '3-3', 'is-the-cpi-accurate', ref('B', 6, '(a)(i)'),
    H.q(8, 'Do you consider the CPI an accurate measure of changes in the cost of living?', ' (ii)'), '2 + 3 x 5', 17,
    [point('r-answer', H.traced('No, for the following reasons:'), 2, 'No, 2 marks: the scheme credits No.'),
     anyN('r-reasons', 'A reason — any three', 15, 3, 5,
          H.split('Limitations of an average / relevance', 'No: 2 marks',
                  ['Limitations of an average', 'Introduction of new products', 'Limited range of products', 'Rural versus urban',
                   'Switching by consumers', 'Quality bias of products', 'Price index not cost of living', 'Unrepresentative weights']),
          'Three reasons, 5 marks each (2 + 3).')],
    kind='fixed', stem=q6a, **B)
pick('sb-q6-a-ii', '3-3', 'effects-of-deflation', ref('B', 6, '(a)(ii)'),
     H.q(8, 'Discuss two possible economic effects of price deflation on the Irish economy.', ' (25)'), 'An effect — any two',
     H.split('Income effect / increasing purchasing power', '2 effects at 4 marks each (2 + 2)',
             ['Income effect', 'Debt burden effect', 'Decline in spending', 'A fall in investment', 'Increased competitiveness',
              'Long-term damage to the economy']),
     2, 4, 'Two effects, 4 marks each (2 + 2).', stem=q6a, **B)
q6b = H.q(8, 'Economists classify unemployment into different types.', ' (i)')
pick('sb-q6-b-i', '3-2', 'types-of-unemployment', ref('B', 6, '(b)(i)'), H.q(8, 'State and explain three types of unemployment.', ' (ii)'),
     'A type — any three',
     H.split('Cyclical unemployment\nThis type', '3 points at 5 marks each (2 + 3)',
             ['Cyclical unemployment', 'Structural unemployment', 'Frictional unemployment', 'Seasonal unemployment',
              'Institutional unemployment']),
     3, 5, 'Three types, 5 marks each (2 + 3).', stem=q6b, **B)
pick('sb-q6-b-ii', '3-2', 'policies-for-unemployment', ref('B', 6, '(b)(ii)'),
     H.q(8, 'Outline one appropriate government policy response for each of two unemployment types', ' (25)'), 'A policy — any two',
     H.split('Cyclical unemployment\nPolicymakers', '2 measures at 5 marks each (2 + 3)',
             ['Cyclical unemployment', 'Structural unemployment', 'Frictional unemployment', 'Seasonal unemployment',
              'Institutional unemployment']),
     2, 5, 'Two policies, each for a type explained in (i), 5 marks each (2 + 3).', stem=q6b, **B)
q6c = H.q(8, 'According to the Quarterly National Household Survey (QNHS)', ' (i)')
add('sb-q6-c-i', '3-2', 'the-live-register', ref('B', 6, '(c)(i)'),
    H.q(8, 'Name one other commonly used source of unemployment statistics in Ireland.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('The Live Register'), 5, 'The source, 5 marks.')], stem=q6c, **B)
pick('sb-q6-c-ii', '3-2', 'why-the-sources-differ', ref('B', 6, '(c)(ii)'),
     H.q(8, 'State and explain the reasons for the differences between both sources.', ' (iii)'), 'A reason — any two',
     side('The Live Register overstates the “true” level of unemployment because it includes',
          H.split('1. People who are legitimately working part time', '2 reasons at 5 marks each',
                  ['People who are legitimately working', 'People who may be drawing social welfare', 'People who may not be actively',
                   'Those signing on only'])),
     2, 5, 'Two reasons, 5 marks each.', stem=q6c, **B)
add('sb-q6-c-iii', '3-1', 'employment-and-the-current-finances', ref('B', 6, '(c)(iii)'),
    H.q(8, 'Outline the possible economic effects which a rise in the level of employment', ' (25)'), '2 x 5 (2 + 3)', 10,
    [point(f'r-{k}', t, 5, n) for k, t, n in zip(
        ('revenue', 'expenditure'),
        H.split('(Current) revenue increases', '2 effects at 5 marks each (2 + 3)', ['(Current) revenue increases', '(Current) expenditure decreases']),
        ('Current revenue rising, 5 marks (2 + 3).', 'Current expenditure falling, 5 marks (2 + 3).'))],
    stem=q6c, **B)

# Q7 ─ the circular flow; comparing national income; growth
q7ai = H.q(8, 'Explain, with the aid of a diagram, the Circular Flow of Income for an open economy.', ' (ii)')
add('sb-q7-a-i', '3-0', 'the-circular-flow-of-income', ref('B', 7, '(a)(i)'), q7ai, '13 + 5 + 5', 23,
    [ask_row('r-diagram', q7ai[q7ai.index('the Circular'):].rstrip('.'), 13,
             'The diagram, 13 marks: the scheme prints the circular flow for an open economy (shown with the answer) and prices it 13.'),
     point('r-households', f"{H.traced('Households')} — {H.opt('Households are the owners of the factors of production', 'Firms')}", 5,
           'Households, 5 marks (the scheme’s 10 marks (5 + 5)).'),
     point('r-firms', f"{H.traced('Firms')} — {H.opt('Firms produce goods and services using factors of production', '10 marks')}", 5,
           'Firms, 5 marks.')],
    kind='fixed', figure=SOL + 'p30-q7ai-diagram', **B)
add('sb-q7-a-ii', '3-0', 'exports-savings-and-national-income', ref('B', 7, '(a)(ii)'),
    H.q(8, 'Outline how each of the following should affect the level of National Income in Ireland:', ' (35)'), '6 + 6', 12,
    [point('r-exports', f"{H.traced('An increase in Irish exports')} — {cc('This is an injection into the circular flow')}", 6,
           'Exports, 6 marks (3 + 3).'),
     point('r-savings', f"{H.traced('An increase in the level of savings')} — {cc('This is a withdrawal from the circular flow')}", 6,
           'Savings, 6 marks (3 + 3).')], **B)
pick('sb-q7-b', '3-0', 'comparing-national-income', ref('B', 7, '(b)'),
     H.q(8, 'Discuss four factors which should be considered when comparing national income statistics', ' (20)'), 'A factor — any four',
     H.split('Population/ Should be done on a per capita basis', '4 points at 5 marks each (2 + 3)',
             ['Population/ Should be done', 'The price levels', 'Common currency', 'Distribution of national income', 'Size of the black economy',
              'Nature of government expenditure', 'Government services at cost price', 'Issues specific to individual countries']),
     4, 5, 'Four factors, 5 marks each (2 + 3).', **B)
q7c = H.q(8, 'The Central Bank of Ireland (CBI) raised its forecast for 2015 economic growth', ' (i)')
add('sb-q7-c-i', '3-5', 'economic-growth', ref('B', 7, '(c)(i)'), H.q(8, 'Define the term economic growth.', ' (ii)'), '4', 4,
    [point('r-1', H.opt('Can be defined as an increase in real Gross National Product', '4 marks'), 4, 'The definition, 4 marks.')],
    stem=q7c, **B)
benefits = [cc(x) for x in ('Increased employment opportunities', 'Improved government finances With', 'Effects on Balance of Payments',
                            'Increased standard of living Economic', 'Effects on migration', 'Investment opportunities /', 'Reduced poverty')]
costs = [cc(x) for x in ('Inflationary pressures With', 'Using up scarce resources', 'Labour shortages', 'Revised expectations by citizens',
                         'Uneven distribution of wealth', 'Environmental consequences', 'Demographic problems',
                         'Quality of life / pressure on infrastructure')]
pick('sb-q7-c-ii', '3-5', 'costs-and-benefits-of-growth', ref('B', 7, '(c)(ii)'),
     H.q(8, 'Discuss possible costs and benefits of economic growth.', ' (20)'), 'A cost or benefit — any four',
     side('Possible benefits', benefits) + side('Possible costs', costs),
     4, 4, 'Four points, 4 marks each (2 + 2). ' + H.traced('Must have a minimum of one cost / benefit'), stem=q7c, **B)

# Q8 ─ budget deficits; regional development; emigration
q8a = H.q(9, '“A Budget deficit stimulates the economy and therefore should be encouraged.”', ' (20)')
irish = [H.traced(x) for x in H.chunk('The Irish economy:', 'If the candidate answers that a budget deficit should be encouraged').split('•')[1:]]
irish = [H.traced(' '.join(x.split())) for x in irish]
for word, label, start, end in (
        ('agree', 'If the candidate answers that a budget deficit should be encouraged:', 'The increased government expenditure will increase',
         'If the candidate answers that a budget deficit should not be encouraged'),
        ('disagree', 'If the candidate answers that a budget deficit should not be encouraged:', 'It can lead to increased borrowing',
         'For reference to the Irish economy')):
    add(f'sb-q8-a-{word}', '3-1', 'should-a-budget-deficit-be-encouraged', ref('B', 8, '(a)', word),
        f'{q8a} Justify the choice: {word.upper()}.', '6 (3 + 3) + 7 + 7', 20,
        [anyN('r-ireland', 'Reference to the Irish economy — both', 6, 2, 3, irish,
              H.traced('For reference to the Irish economy 6 marks (3 + 3)') + '.'),
         anyN('r-points', H.traced(label.rstrip(':')) + ' — any two', 14, 2, 7, bl('• ' + start, end),
              'Two points, 7 marks each (4 + 3). The scheme credits agreeing and disagreeing, each with its own list.')],
        kind='fixed', **B)
q8b = None
pick('sb-q8-b-i', '3-5', 'policies-for-regional-development', ref('B', 8, '(b)(i)'),
     H.q(9, 'Outline three policies the Irish Government could consider to achieve balanced regional development.', ' (ii)'),
     'A policy — any three',
     H.split('Grants/Tax Incentives\nIf', '3 points at 5 marks each (2 + 3)',
             ['Grants/Tax Incentives', 'Investment in the infrastructure', 'High speed broadband', 'Improved access to training',
              'Provide venture capital']),
     3, 5, 'Three policies, 5 marks each (2 + 3).', **B)
pick('sb-q8-b-ii', '3-5', 'regional-development-for-rural-communities', ref('B', 8, '(b)(ii)'),
     H.q(9, 'Outline two economic benefits to rural communities of balanced regional development.', ' (25)'), 'A benefit — any two',
     H.split('Employment creation\nRegional', '2 points at 5 marks each (2 + 3)',
             ['Employment creation', 'Maintain local services', 'Reduce emigration', 'Promote / support more vibrant', 'Less rural / urban divide']),
     2, 5, 'Two benefits, 5 marks each (2 + 3).', **B)
negative = [cc(x) for x in ('Higher dependency ratio The', 'Opportunity costs The state', 'Loss of skills within the economy',
                            'Underutilisation of services', 'Upward pressure on Irish wage rates', 'Reduced domestic demand',
                            'Decline in rural communities')]
positive = [cc(x) for x in ('Unemployment reduced', 'Emigrants returning to Ireland may help', 'Contacts / Export opportunities',
                            'Demand for state services', 'Emigrants’ remittances to Ireland')]
pick('sb-q8-c-i', '3-2', 'effects-of-emigration', ref('B', 8, '(c)(i)'),
     H.q(9, 'Discuss the economic effects of emigration on the Irish economy.', ' (ii)'), 'An effect — any four',
     side('Negative consequences', negative) + side('Positive consequences', positive),
     4, 5, 'Four effects, 5 marks each (2 + 3), negative or positive.', **B)
pick('sb-q8-c-ii', '3-2', 'bringing-emigrants-home', ref('B', 8, '(c)(ii)'),
     H.q(9, 'Advise the Government on two policy initiatives/measures', ' (30)'), 'A measure — any two',
     H.split('Lower taxation\nBy reducing', '2 points at 5 marks each (2 + 3)',
             ['Lower taxation', 'Provide grants/subsidies to firms', 'Training and education', 'Support recovery in the economy',
              'Devote more resources to capital spending', 'Improve services']),
     2, 5, 'Two measures, 5 marks each (2 + 3).', **B)

if __name__ == '__main__':
    emit(cards)
