#!/usr/bin/env python3
"""Economics 2012 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2012-hl-ev.json, made
from a visual sweep of all 8 paper pages and 40 scheme pages before any 2012
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The scheme reprints each question above its answer, so a
slice always starts after the reprinted wording. A stem stops before any
printed table: the table is the crop beside the typed ask. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2012, 'higher', 'LC034ALP000EV')
D = OldDeck(2012, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2012-HL-scheme-'
PAP = 'economics-2012-HL-paper-'
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def dots(cell):
    """A table cell's bullets, each read whole."""
    return [H.traced(x.strip()) for x in cell.split('•') if x.strip()]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ demand for bottled water
add('sa-q1', '1-1', 'why-demand-for-bottled-water-rises', ref('A', 1),
    H.q(2, 'State three reasons why the demand curve for bottled water may shift to the right.', ' (i)'), '6 + 5 + 5', 16,
    [anyN('r-1', 'A reason — any three', 16, 3, 6,
          H.split('(i) Incomes:', '3 points: 6 + 5 + 5 marks.',
                  ['Incomes:', 'Taste / Preference:', 'Expectations:', 'Price of substitute goods:', 'Unplanned factors:',
                   'Government policies:']),
          'Three reasons, ' + H.traced('3 points: 6 + 5 + 5 marks.') + ' The first correct 6.', steps=[6, 5, 5])],
    kind='fixed', **A)

# Q2 ─ the ECB
add('sa-q2', '3-3', 'what-the-ecb-is-responsible-for', ref('A', 2),
    H.q(2, 'State three areas of responsibility of the European Central Bank (ECB).', ' (i)'), '6 + 5 + 5', 16,
    [anyN('r-1', 'An area of responsibility — any three', 16, 3, 6,
          H.split('1. Price Stability:', '3 points: 6 + 5 + 5 marks.',
                  ['Price Stability:', 'EU monetary policy:', 'Official reserves of the euro area countries:', 'Supervision:',
                   'Issues euro currency:']),
          'Three areas, ' + H.traced('3 points: 6 + 5 + 5 marks.') + ' The first correct 6.', steps=[6, 5, 5])],
    kind='fixed', **A)

# Q3 ─ the black economy
add('sa-q3', '3-0', 'the-black-economy-and-the-exchequer', ref('A', 3),
    H.q(2, 'Outline two reasons for the growth of the ‘Black Economy’', ' Reason 1:'), '2 @ 4 + 2 @ 4', 16,
    [anyN('r-reasons', 'A reason for its growth — any two', 8, 2, 4,
          H.split('Reduced disposable incomes:', 'Two effects for the Exchequer:',
                  ['Reduced disposable incomes:', 'Increased VAT rates:', 'Unemployment:', 'Disillusionment with government policies:']),
          'Two reasons, 4 marks each: ' + H.traced('2 reasons at 4 marks each.')),
     anyN('r-effects', 'An effect for the Exchequer — any two', 8, 2, 4,
          H.split('Loss of tax revenue:', '2 reasons at 4 marks each.',
                  ['Loss of tax revenue:', 'Increased government expenditure:', 'Unemployment bill is higher:',
                   'Decline in legitimate business activity:', 'Pressure on government finances / provision of services:']),
          'Two effects, 4 marks each: ' + H.traced('2 effects at 4 marks each.'))],
    kind='fixed', **A)

# Q4 ─ economies and diseconomies of scale
ticks = (('Repetitive tasks, workers are bored', '(b) Diseconomy of Scale', 'Internal'),
         ('R&D costs are shared by many firms', '(a) Economy of Scale', 'External'),
         ('Discounts are available for bulk buying', '(a) Economy of Scale', 'Internal'),
         ('Inadequate infrastructure', '(b) Diseconomy of Scale', 'External'))
add('sa-q4', '1-5', 'internal-or-external-economies-of-scale', ref('A', 4),
    # The four statements follow the ask, from the paper's own table rows: the card cannot be answered without them.
    f"{H.q(2, 'In relation to each statement listed below', ' (a) Economy of Scale (b)')} "
    f"{H.q(2, 'Repetitive tasks, workers are bored', ' (16 marks)')}", '4 @ 4', 16,
    [point(f'r-{i}', f'{cc(s, whole=True)} — {H.traced(group)} — {H.traced(col)}', 4,
           f'Ticked {col.lower()}, under {group[4:].lower()}: 4 marks. ' + H.traced('4 correct answers at 4 marks each.'))
     for i, (s, group, col) in enumerate(ticks, 1)],
    kind='fixed', figure=SOL + 'p06-q4-ticks', **A)
beside_ask(cards[-1], PAP + 'p02-q4-table')

# Q5 ─ inferior goods
q5 = H.q(2, '‘Inferior products have a negative Income Elasticity of Demand (YED)’.', ' (a)')
add('sa-q5-a', '1-4', 'negative-income-elasticity', ref('A', 5, '(a)'), H.q(2, 'Explain this statement.', ' Explanation:'), '10', 10,
    [point('r-1', H.traced('As a consumer’s income decreases s/he will buy more of an inferior product.'), 10, 'The explanation, 10 marks.')],
    stem=q5, **A)
add('sa-q5-b', '1-4', 'an-inferior-good', ref('A', 5, '(b)'),
    H.q(2, 'State one example of an inferior product, giving a reason for your answer.', ' Example:'), '6', 6,
    [point('r-example', H.opt('Remould tyres / low price cuts of meat', '\nReason:'), None,
           'An example: any one of the scheme’s.'),
     point('r-reason', H.opt('As incomes decline the demand for supermarket own brands', '\n6 marks'), None,
           'The reason. Claim the complete answer: the scheme prices the example and its reason ' + H.traced('6 marks')
           + ' together, without dividing them.')],
    kind='questionTotal', stem=q5, **A)

# Q6 ─ the MPS and the multiplier
q6 = H.q(3, 'Study the table below and calculate (i) and (ii), showing all your workings.', ' Year')
q6_table = PAP + 'p03-q6-table'
add('sa-q6-i', '3-0', 'the-marginal-propensity-to-save', ref('A', 6, '(i)'),
    H.q(3, 'The Marginal Propensity to Save (MPS).', ' Answer:'), '9', 9,
    [point('r-1', H.traced('0.3 or 30%'), 9,
           'The MPS, ' + H.traced('9 marks') + '. The working is shown with the answer: the change in savings (€3,000) over the change '
           'in income (€10,000), or 1 minus the MPC.')],
    kind='fixed', stem=q6, figure=SOL + 'p07-q6i-working', **A)
beside_ask(cards[-1], q6_table)
add('sa-q6-ii', '3-0', 'the-size-of-the-multiplier', ref('A', 6, '(ii)'),
    H.q(3, 'The size of the Multiplier.', ' Answer:'), '8', 8,
    [point('r-1', H.traced('1.25'), 8,
           'The multiplier, ' + H.traced('8 marks') + '. The working is shown with the answer: the MPM (0.5) from the change in imports, '
           'then either of the scheme’s two methods.')],
    kind='fixed', stem=q6, figure=SOL + 'p07-q6ii-working', **A)
beside_ask(cards[-1], q6_table)

# Q7 ─ savings
add('sa-q7', '3-4', 'what-affects-savings-in-ireland', ref('A', 7),
    H.q(3, 'Outline three factors currently affecting the rate of savings in the Irish economy.', ' (i)'), '6 + 6 + 5', 17,
    [anyN('r-1', 'A factor — any three', 17, 3, 6,
          H.split('Confidence in economy\nPeople', '3 points: 6 + 6 + 5 marks.',
                  ['Confidence in economy', 'Security of savings', '(Real) Rate of interest', 'Income levels', 'Rate of DIRT']),
          'Three factors, ' + H.traced('3 points: 6 + 6 + 5 marks.') + ' The first two correct 6 each.', steps=[6, 6, 5])],
    kind='fixed', **A)

# Q8 ─ is imperfect competition wasteful?  A printed Yes / No; the scheme credits each side.
q8 = H.q(3, '‘Imperfect Competition is wasteful of resources’.', ' _')
yes = [H.traced('It does not produce at the lowest point of average cost.'),
       H.traced('This is due to spending by the firm on advertising its products / services or the firm does not produce a '
                'sufficient quantity to benefit from economies of scale.')]
no = [H.traced('If a firm invests in innovation and increases sales it may not be considered wasteful'),
      H.traced('e.g. Apple’s investment confers an advantage on the company that it would not enjoy without such spending.')]
for word, answer, points, how in (
        ('yes', 'Yes.', yes, 'its answer’s two sentences'),
        ('no', 'No.', no, 'its answer’s point and its example')):
    add(f'sa-q8-{word}', '2-0', 'is-imperfect-competition-wasteful', ref('A', 8, '', word),
        f'{q8} Justify the choice: {word.upper()}.', '1 + 8 + 8', 17,
        [point('r-answer', H.traced(answer), 1, 'The answer, 1 mark. The scheme credits Yes and No, each with its own explanation.'),
         anyN('r-explanation', 'The explanation — both points', 16, 2, 8, points,
              'The explanation, two points at 8: the scheme prints ' + H.traced('(1+8+8) marks') + ' beneath one answer, read here as '
              + how + '.')],
        kind='fixed', **A)

# Q9 ─ the household charge
q9 = H.q(3, 'The Irish Government introduced the household charge (property tax)', ' (a)')
pick('sa-q9-a', '3-1', 'the-household-charge-for-the-exchequer', ref('A', 9, '(a)'),
     H.q(3, 'State two advantages of this charge/tax for the Exchequer.', ' (i)'), 'An advantage — any two',
     H.split('1. Government revenue', '2 points at 4 marks each.',
             ['Government revenue', 'Stable tax', 'Less need to raise direct taxes', 'Economic', 'Ease introduction of property tax',
              'Government planning']),
     2, 4, 'Two advantages, ' + H.traced('2 points at 4 marks each.'), stem=q9, **A)
add('sa-q9-b', '3-1', 'is-the-household-charge-progressive', ref('A', 9, '(b)'),
    H.q(3, 'Is this a progressive tax or a regressive tax? Explain your answer.', ' _'), '9', 9,
    [point('r-answer', H.traced('Regressive.'), None, 'The answer: regressive.'),
     point('r-1', H.traced('Because it does not take into account a person’s ability to pay the tax.'), None, 'Why.'),
     point('r-2', H.traced('People on lower income would pay a greater proportion of their income in tax.'), None,
           'Claim the complete answer: the scheme prices the answer and its explanation ' + H.traced('9 marks')
           + ' together, without dividing them.')],
    kind='questionTotal', stem=q9, **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ the consumer; PED and revenue; cross elasticity
add('sb-q1-a-i', '1-1', 'the-equi-marginal-principle', ref('B', 1, '(a)(i)'),
    H.q(4, 'Explain the Equi-Marginal Principle of consumer behaviour.', ' (ii)'), '10', 10,
    [point('r-1', H.opt('Consumers will spend their incomes in such a way', '\n10 marks.'), 10, 'The explanation, 10 marks.')], **B)
pick('sb-q1-a-ii', '1-1', 'assumptions-of-consumer-behaviour', ref('B', 1, '(a)(ii)'),
     H.q(4, 'State and explain three other economic assumptions used to analyse consumer behaviour.', ' (25)'),
     'An assumption — any three',
     H.split('1. The consumer has a limited income.', '3 at 5 marks each.',
             ['The consumer has a limited income.', 'The consumer acts rationally.',
              'The consumer is subject to the law of diminishing marginal utility.']),
     3, 5, 'Three assumptions, ' + H.traced('3 at 5 marks each.'), **B)
products = (('Product A: - 2.8', 'Decrease price', 'Elastic', 'Because: the % ↑ in demand exceeds the % ↓ in price', 'This will increase'),
            ('Product B: - 1.0', 'Leave price unchanged', 'Unit elastic', 'Because: the % ∆ in demand equals the % ∆ in price',
             'Will remain unchanged'),
            ('Product C: - 0.5', 'Increase price', 'Inelastic', 'Because: the % ↑ in price exceeds the % ↓ in demand', 'This will increase'))
add('sb-q1-b', '1-4', 'pricing-to-maximise-revenue', ref('B', 1, '(b)'),
    H.q(4, 'A manufacturer of three different products calculates', ' (30)'), '10 + 10 + 10', 30,
    [point(f'r-{p[8].lower()}', ' — '.join(cc(x, whole=True) for x in (p, change, kind_, why, effect)), 10,
           f'Product {p[8]}, 10 marks: the price change, the type of good, the reason and the effect on total revenue, with its '
           'demand curve (shown with the answer). The scheme does not divide the 10.')
     for p, change, kind_, why, effect in products],
    kind='fixed', figure=SOL + 'p11-q1b-table', **B)
q1c = H.q(4, 'You are given the following information about certain products:', ' (i) Which')
add('sb-q1-c-i', '1-4', 'substitutes-by-cross-elasticity', ref('B', 1, '(c)(i)'),
    H.q(4, 'Which of the products above are substitutes for Product X?', ' (ii)'), '4 + 6', 10,
    [point('r-answer', H.traced('Products B and D are substitutes to Product X.'), 4, 'The answer, 4 marks.'),
     point('r-explanation', H.opt('This is because substitutes have a positive CED', '\n10 (4+6) marks'), 6,
           'The explanation, 6 marks (' + H.traced('10 (4+6) marks') + ').')],
    kind='fixed', stem=q1c, **B)
add('sb-q1-c-ii', '1-4', 'the-closer-complement', ref('B', 1, '(c)(ii)'),
    H.q(4, 'Which product is the closer complement to Product X?', ' (20)'), '4 + 6', 10,
    [point('r-answer', H.traced('Product C is the closer complement to Product X.'), 4, 'The answer, 4 marks.'),
     point('r-explanation', H.opt('Product C has the highest numerical value', '\n10 (4+6) marks'), 6,
           'The explanation, 6 marks (' + H.traced('10 (4+6) marks') + ').')],
    kind='fixed', stem=q1c, **B)

# Q2 ─ perfect competition; its equilibrium; against monopoly
add('sb-q2-a-i', '2-0', 'the-perfectly-competitive-firms-demand-curve', ref('B', 2, '(a)(i)'),
    H.q(4, 'Explain the reason for the shape of the demand curve of an individual firm', ' (ii)'), '6 + 4', 10,
    [point('r-price-taker', H.traced('A firm in perfect competition is a price taker / it accepts the market price.'), 6,
           'The price taker, 6 marks.'),
     heading('r-why', 'Why — either',
             [H.traced('The single firm by its own actions cannot influence the market price because the single firm represents such a '
                       'small proportion of the total supply.'),
              H.traced('If a firm increases price quantity demanded will fall to zero as consumers switch to the cheaper identical '
                       'goods available.')], 4,
             'The explanation, 4 marks: the scheme accepts either.')],
    kind='fixed', **B)
pick('sb-q2-a-ii', '2-0', 'advantages-of-perfect-competition', ref('B', 2, '(a)(ii)'),
     H.q(4, 'Outline two advantages of perfect competition.', ' (20)'), 'An advantage — any two',
     H.split('Low prices\nThe firm sells', '2 at 5 marks each.', ['Low prices', 'Efficient', 'No advertising', 'Normal profits earned']),
     2, 5, 'Two advantages, ' + H.traced('2 at 5 marks each.'), **B)
add('sb-q2-b-i', '2-0', 'short-run-equilibrium-in-perfect-competition', ref('B', 2, '(b)(i)'),
    H.q(4, 'Explain, with the aid of a labelled diagram, the equilibrium position', ' (ii)'), '7 + 5 @ 2', 17,
    [anyN('r-diagram', 'The diagram — each element', 7, 7, 1,
          [H.traced(x) for x in ('MC curve', 'AC curve', 'D = AR = MR', 'Point A', 'P1', 'Q1', 'Cost is at point B.')],
          'The diagram, ' + H.traced('7 marks') + ' for the seven elements the scheme lists under it, 1 each. The completed diagram '
          'is shown with the answer.'),
     anyN('r-explanation', 'The explanation — each point', 10, 5, 2,
          [H.traced(x) for x in ('Equilibrium at point A: MC = MR and MC cuts MR from below.', 'The firm produces Q1',
                                 'Firm will sell this output at P1', 'Cost of production is at point B.',
                                 'Firm will earn SNP’s because AR exceeds AC.')],
          'The explanation, ' + H.traced('10 marks: 5 at 2 marks each') + '.')],
    kind='fixed', figure=SOL + 'p14-q2bi-diagram', **B)
add('sb-q2-b-ii', '2-0', 'new-firms-enter-a-competitive-market', ref('B', 2, '(b)(ii)'),
    H.q(4, 'With the aid of labelled diagrams, explain the impact', ' (35)'), '4 + 4 + 5 @ 2', 18,
    [anyN('r-market', 'The market diagram — each element', 4, 4, 1, [H.traced(x) for x in ('S1', 'S2', 'P1', 'P2')],
          'The market diagram, 4 marks for the four elements the scheme lists under it, 1 each. The completed diagrams are shown '
          'with the answer.'),
     anyN('r-firm', 'The firm diagram — each element', 4, 4, 1,
          [H.traced(x) for x in ('D = AR =MR (new)', 'P2', 'Q2', 'Equilibrium point (E)')],
          'The firm diagram, 4 marks for the four elements the scheme lists under it, 1 each.'),
     anyN('r-explanation', 'The explanation — each point', 10, 5, 2,
          [H.traced(x) for x in ('Market supply curve shifts out to the right.', 'The market price falls',
                                 'Individual firm’s D/C falls / its price falls', 'Firm will now produce a smaller quantity.',
                                 'Amount of SNP’s earned will fall / are eliminated.')],
          'The explanation, ' + H.traced('10 marks: 5 at 2 marks each') + ' (' + H.traced('18 marks') + ' in all).')],
    kind='fixed', figure=SOL + 'p15-q2bii-diagrams', **B)
contrasts = (('barriers', 'No barriers to entry exist.', 'Barriers to entry do exist.', 'Barriers to entry: 6 marks', 6),
             ('profits', 'Only earns normal profit.', 'Can earn SNPs.', 'Profits in the long run: 6 marks', 6),
             ('scale', 'Tend not to benefit from E/S.', 'May benefit from E/S.', 'Economies of scale: 4 marks', 4),
             ('discrimination', 'Cannot practise price discrimination.', 'Could practise price discrimination.',
              'Price discrimination: 4 marks', 4))
add('sb-q2-c', '2-0', 'perfect-competition-against-monopoly', ref('B', 2, '(c)'),
    H.q(4, 'Contrast the characteristics of perfect competition with monopoly', ' (20)'), '6 + 6 + 4 + 4', 20,
    [point(f'r-{rid}', f'{cc(pc)} — {cc(mono)}', marks,
           H.traced(tariff) + '. Perfect competition, then monopoly.')
     for rid, pc, mono, tariff, marks in contrasts],
    kind='fixed', **B)

# Q3 ─ factor incomes; entrepreneurship; small firms
add('sb-q3-a-i', '2-1', 'supply-price-and-transfer-earnings', ref('B', 3, '(a)(i)'),
    H.q(5, 'Explain the following terms in relation to a factor of production:', ' (ii)'), '5 + 5', 10,
    [point('r-supply-price', 'Supply Price — ' + H.traced('The minimum payment necessary to bring a factor into use and maintain it in '
                                                         'that particular use.'), 5, 'Supply price, 5 marks.'),
     heading('r-transfer', 'Transfer Earnings — either',
             [H.traced('The earnings of a factor in the next best alternative employment.'),
              H.traced('What a factor must receive to keep it in its present use and prevent it from transferring to another use.')], 5,
             'Transfer earnings, 5 marks: the scheme accepts either.')],
    kind='fixed', **B)
add('sb-q3-a-ii', '2-1', 'economic-rent', ref('B', 3, '(a)(ii)'),
    H.q(5, 'Explain the concept Economic Rent', ' (25)'), '5 + 5 + 5', 15,
    [point('r-rent', 'Economic Rent — ' + H.traced('Any earnings of a factor of production above its supply price/transfer earnings.'), 5,
           'Economic rent, 5 marks.'),
     anyN('r-circumstances', 'A circumstance — any two', 10, 2, 5,
          H.split('1. Shortage in the supply of any factor of production', '2 points at 5 marks each.',
                  ['Shortage in the supply of any factor of production', 'Possession of a rare skill or talent', 'Rent of Ability',
                   'Completely specific factors of production']),
          'Two circumstances, ' + H.traced('2 points at 5 marks each.'))],
    kind='fixed', **B)
pick('sb-q3-b-i', '0-1', 'why-entrepreneurship-matters', ref('B', 3, '(b)(i)'),
     H.q(5, 'State and explain the economic reasons why entrepreneurship is important', ' (ii)'), 'A reason — any three',
     H.split('1. Creates employment', '3 at 5 marks each.',
             ['Creates employment', 'Organises production', 'What to produce / prices to charge', 'Innovation',
              'Encourages further investment / Enterprise culture', 'Outlet for savers funds', 'Revenue for the government',
              'Improve Balance of Payments', 'Creates wealth']),
     3, 5, 'Three reasons, ' + H.traced('3 at 5 marks each.'), **B)
pick('sb-q3-b-ii', '0-1', 'encouraging-entrepreneurship', ref('B', 3, '(b)(ii)'),
     H.q(5, 'State and explain three means by which the Irish Government could encourage', ' (30)'), 'A means — any three',
     H.split('1. Enterprise education', '3 at 5 marks each.',
             ['Enterprise education', 'Taxation policies', 'Government Policies / regulation', 'Labour market policies',
              'Improved economic outlook / confidence in economy', 'Develop infrastructure', 'Improve competitiveness',
              'Availability of bank credit', 'Government initiatives']),
     3, 5, 'Three means, ' + H.traced('3 at 5 marks each.'), **B)
pick('sb-q3-c', '2-0', 'why-small-firms-survive', ref('B', 3, '(c)'),
     H.q(5, 'Discuss the reasons why small firms survive in the Irish economy.', ' (20)'), 'A reason — any four',
     H.split('1. Small size of market / Scale of operation', '4 at 5 marks each.',
             ['Small size of market / Scale of operation', 'Personal services', 'Consumer loyalty', 'Support the community',
              'Traditional / Niche markets', 'Exclusive nature of the commodity', 'Availability of capital',
              'Membership of voluntary groups.']),
     4, 5, 'Four reasons, ' + H.traced('4 at 5 marks each.'), stem=H.q(5, '‘There are 200,000 small firms in Ireland', ' Discuss'), **B)

# Q4 ─ cost curves; location; the minimum price
# The ask's own opening words name the diagrams, so each card's question carries them (its diagram row restates them).
q4a = H.q(5, 'With the aid of two clearly labelled diagrams', ' (i)')
drawn = H.q(5, 'With the aid of two clearly labelled diagrams', ', explain')
add('sb-q4-a-i', '1-5', 'short-and-long-run-average-cost', ref('B', 4, '(a)(i)'),
    H.q(5, 'With the aid of two clearly labelled diagrams', ' (ii)'), '6 + 3 + 4', 13,
    [ask_row('r-diagram', drawn, 6,
             'The diagram, 6 marks: the scheme prints ' + H.traced('13 (6+3+4) marks') + ' beneath its diagram, its SRAC point and its '
             'LRAC point, read here in that order. The diagram is shown with the answer: SRAC curves along a U-shaped LRAC.'),
     heading('r-srac', 'SRAC — either', [H.traced('Each SRAC curve represents a different scale of operation / size of firm.'),
                                         H.traced('As a firm expands each SRAC represents its costs at a different stage of development.')],
             3, 'SRAC, 3 marks: the scheme accepts either.'),
     heading('r-lrac', 'LRAC — either', [H.traced('Is made up of all the lowest points on the SRAC curves.'),
                                         H.traced('The aim of any firm is to maximise its profits so the firm will produce where unit '
                                                  'costs of production are cheapest i.e. along LRAC.')],
             4, 'LRAC, 4 marks: the scheme accepts either.')],
    kind='fixed', figure=SOL + 'p21-q4ai-diagram', **B)
add('sb-q4-a-ii', '1-5', 'average-and-marginal-cost', ref('B', 4, '(a)(ii)'),
    f"{q4a} {H.q(5, '(ii) the short run average cost curve and marginal cost curve.', ' (25)')}", '6 + 6', 12,
    [ask_row('r-diagram', drawn, 6,
             'The diagram, 6 marks (' + H.traced('12 (6+6) marks') + '): MC rising through the lowest point of a U-shaped AC, as the '
             'figure shows.'),
     point('r-relationship', ' — '.join(H.traced(x) for x in ('When MC is greater than AC then AC is rising', 'When MC is less than AC then AC is falling',
                                                           'When MC equals AC then AC is at a minimum / constant')), 6,
           'The relationship, 6 marks: the scheme’s three lines, which it does not divide.')],
    kind='fixed', figure=SOL + 'p21-q4aii-diagram', **B)
pick('sb-q4-b', '1-2', 'where-a-firm-locates', ref('B', 4, '(b)'),
     H.q(5, 'Discuss the economic factors which should be considered by a firm', ' (25)'), 'A factor — any five',
     side('Within countries',
          H.split('Transport infrastructure Firm', '\nAcross Countries',
                  ['Transport infrastructure', 'Access to water supplies / power', 'Land for expansion / cost of land', 'Planning permission',
                   'Environmental regulations', 'Workforce availability', 'Government incentives', 'Proximity to the market',
                   'Proximity to the raw materials', 'Other: Availability of social infrastructure']))
     + side('Across Countries',
            H.split('Access to EU market / Member of the euro currency', '5 at 5 marks each.',
                    ['Access to EU market / Member of the euro currency', 'Good industrial relations',
                     'Attractiveness of return on investments', 'Stable economic climate / economic growth',
                     'Low wage / production costs'])),
     5, 5, 'Five factors, ' + H.traced('5 at 5 marks each.') + ' The last within countries is the scheme’s “Other”.', **B)
q4c = H.q(5, 'Ocean Blue Ltd produces two boats weekly', ' (i) in the short run?')
each = H.q(5, 'Explain your answers in each case.', ' (25)')
add('sb-q4-c-i', '1-5', 'the-short-run-minimum-price', ref('B', 4, '(c)(i)'),
    f"{H.q(5, 'in the short run?', ' (ii) in the long run?')} {each}", '9 + 6', 15,
    [point('r-price', H.traced('Minimum price per boat 1,800'), 9,
           'The minimum price, 9 marks (' + H.traced('15 (9+6) marks') + '): the variable costs, raw materials and labour (€3,600), '
           'over the two boats. The working is shown with the answer.'),
     point('r-explanation', H.traced('a firm must cover its variable costs in the short run'), 6, 'The explanation, 6 marks.')],
    kind='fixed', stem=q4c, figure=SOL + 'p23-q4ci-working', **B)
add('sb-q4-c-ii', '1-5', 'the-long-run-minimum-price', ref('B', 4, '(c)(ii)'),
    f"{H.q(5, 'in the long run?', ' Explain your answers')} {each}", '6 + 4', 10,
    [point('r-price', H.traced('Minimum price per boat 2,900'), 6,
           'The minimum price, 6 marks (' + H.traced('10 (6+4) marks') + '): all the costs, normal profit included (€5,800), over the '
           'two boats. The working is shown with the answer.'),
     point('r-explanation', H.traced('a firm must cover all its costs in the long run'), 4, 'The explanation, 4 marks.')],
    kind='fixed', stem=q4c, figure=SOL + 'p23-q4cii-working', **B)

# Q5 ─ population; growth in LDCs; Malthus
q5a = H.q(6, 'The following table shows the world population and the projection for 2012', ' Population in Billions')
q5a_table = PAP + 'p06-q5a-table'
pick('sb-q5-a-i', '3-5', 'why-world-population-grew', ref('B', 5, '(a)(i)'),
     H.q(6, 'Suggest two reasons for the rapid growth in world population in recent times.', ' (ii)'), 'A reason — any two',
     H.split('1. Birth rate higher than death rate', '2 at 5 marks each.',
             ['Birth rate higher than death rate', 'Health care', 'Government policies', 'Increased agricultural productivity',
              'Increased life expectancy', 'International migration']),
     2, 5, 'Two reasons, ' + H.traced('2 at 5 marks each.'), stem=q5a, figure=q5a_table, **B)
pick('sb-q5-a-ii', '3-5', 'a-growing-population-and-ireland', ref('B', 5, '(a)(ii)'),
     H.q(6, 'Discuss the economic effects of an increasing population on the Irish economy.', ' (30)'), 'An effect — any four',
     H.split('1. Larger domestic market', '4 at 5 marks each.',
             ['Larger domestic market', 'Pressure on infrastructure / economic planning', 'Dependency Ratio',
              'Government employment strategy', 'Land values', 'Government finances']),
     4, 5, 'Four effects, ' + H.traced('4 at 5 marks each.'), stem=q5a, figure=q5a_table, **B)
pick('sb-q5-b-i', '4-0', 'benefits-of-growth-for-ldcs', ref('B', 5, '(b)(i)'),
     H.q(6, 'State and explain the benefits of economic growth for developing countries', ' (ii)'), 'A benefit — any three',
     H.split('1. Increased standard of living', '3 points at 5 marks each.',
             ['Increased standard of living', 'Better services', 'Employment / less reliance on primary sector',
              'Resources available to the government', 'Alleviation of poverty', 'Investment in Research & Development',
              'Reduced reliance on foreign aid / borrowing']),
     3, 5, 'Three benefits, ' + H.traced('3 points at 5 marks each.'), **B)
adv = [cc(x) for x in ('Increased exports / larger market', 'Lower Irish consumer prices', 'Employment If exports',
                       'Less need for Irish state aid', 'Disposable incomes in Ireland', 'Economies of Scale If Irish')]
dis = [cc(x) for x in ('Re-location of companies', 'Greater import bill', 'Increased demand for resources', 'Increased world pollution')]
add('sb-q5-b-ii', '4-0', 'ldc-growth-and-ireland', ref('B', 5, '(b)(ii)'),
    H.q(6, 'Discuss one advantage and one disadvantage for the Irish economy', ' (25)'), '5 + 5', 10,
    [anyN('r-advantage', 'An advantage — any one', 5, 1, 5, adv, 'One advantage, ' + H.traced('1 at 5 marks.')),
     anyN('r-disadvantage', 'A disadvantage — any one', 5, 1, 5, dis, 'One disadvantage, 5 marks.')],
    kind='fixed', **B)
q5c = H.q(6, 'The classical economist, Thomas Malthus', ' (i)')
add('sb-q5-c-i', '0-0', 'malthus-on-population', ref('B', 5, '(c)(i)'),
    H.q(6, 'Explain Malthus’s theory on population.', ' (ii)'), '4 + 4 + 2', 10,
    [anyN('r-1', 'The theory — all three points', 10, 3, 4,
          [H.traced('Malthus stated that population increases in a geometric progression (i.e. 2, 4, 8, 16 etc)'),
           H.traced('while food supply increases in an arithmetic progression (i.e. 2, 3, 4, 5 etc).'),
           H.traced('Population would outgrow the means of subsistence. The outcome would be famine, disease etc.')],
          'The theory: the scheme prints ' + H.traced('10 (4+4+2) marks') + ' beneath its two bullets and does not say which point '
          'earns which, so the first two correct points are claimed at 4 and the third at 2.', steps=[4, 4, 2])],
    kind='fixed', stem=q5c, **B)
q5cii = H.q(6, 'Is Malthus’s theory on population relevant today? Explain your answer.', ' (20)')
pop_yes, pop_no = dots(cc('• The rapid increase in population • World')), dots(cc('• Extensive population control measures'))
food_yes, food_no = dots(cc('• The rapid increase in population cannot')), dots(cc('• Because of the development of high'))
for word, head, pop, food in (('yes', 'His theory is relevant today', pop_yes, food_yes),
                              ('no', 'His theory is not relevant today', pop_no, food_no)):
    pick(f'sb-q5-c-ii-{word}', '0-0', 'is-malthus-relevant-today', ref('B', 5, '(c)(ii)', word),
         f'{q5cii} Justify the choice: {word.upper()}.', H.traced(head) + ' — any two',
         side('Population', pop) + side('Food Production', food), 2, 5,
         H.traced('2 points at 5 marks each.') + ' The scheme credits Yes and No, each with its own column.',
         stem=q5c, **B)

# Q6 ─ economic aims; taxes; third-level fees
pick('sb-q6-a', '3-1', 'the-governments-economic-aims', ref('B', 6, '(a)'),
     H.q(6, 'Discuss four other economic aims of the Government', ' (20)'), 'An aim — any four',
     H.split('1. Reduce unemployment (curb emigration)', '4 at 5 marks each.',
             ['Reduce unemployment (curb emigration)', 'Achieve economic growth', 'Broaden the tax base', 'Reduce the national debt',
              'Stability in the banking sector', 'Improve state services / make them more efficient', 'Improve infrastructure',
              'Boost exports / improve competitiveness', 'Restore consumer confidence', 'State finances',
              'Promote balanced regional development', 'Distribution of wealth']),
     4, 5, 'Four aims, ' + H.traced('4 at 5 marks each.') + ' ' + H.traced('Must refer to current statistic or piece of relevant information.'),
     stem=H.q(6, 'One of the economic aims of the Irish Government at present', ' Discuss four'), **B)
q6b = H.q(6, '‘Most eurozone countries with large deficits are using VAT to generate revenue.’', ' (i)')
add('sb-q6-b-i', '3-1', 'direct-and-indirect-taxes', ref('B', 6, '(b)(i)'),
    H.q(6, 'Explain, using examples, the difference between direct taxes and indirect taxes.', ' (ii)'), '8', 8,
    [point('r-direct', f"{H.traced('Direct taxes')} — {cc('Are taxes on income / wealth / profits', whole=True)} — "
           f"{cc('Income tax; CPT; DIRT', whole=True)}", None, 'Direct taxes: the explanation, then the examples.'),
     point('r-indirect', f"{H.traced('Indirect taxes')} — {cc('Are taxes on goods / services / spending', whole=True)} — "
           f"{cc('VAT, Excise duties', whole=True)}", None,
           'Indirect taxes, the same way. Claim the complete answer: the scheme prices it ' + H.traced('8 marks')
           + ' without dividing it between the explanations and the examples.')],
    kind='questionTotal', stem=q6b, **B)
vat_adv = [cc(x) for x in ('Economic The costs of collection', 'Impossible to evade', 'Convenient As they', 'No disincentive to work',
                           'Used by government to change', 'Acts as a built in stabiliser')]
vat_dis = [cc(x) for x in ('Inflation Increased VAT', 'Inequitable / Regressive', 'Disincentive to spend',
                           'May lead to black economy activities', 'Burden of collection passed', 'Revenue uncertain')]
add('sb-q6-b-ii', '3-1', 'raising-vat-instead-of-income-tax', ref('B', 6, '(b)(ii)'),
    H.q(6, 'Discuss the economic advantages and disadvantages for the Government', ' (iii)'), '2 @ 5 + 2 @ 5', 20,
    [anyN('r-advantages', 'An advantage — any two', 10, 2, 5, vat_adv, 'Two advantages, ' + H.traced('2 at 5 marks.')),
     anyN('r-disadvantages', 'A disadvantage — any two', 10, 2, 5, vat_dis, 'Two disadvantages, 5 marks each.')],
    kind='fixed', stem=q6b, **B)
add('sb-q6-b-iii', '1-3', 'a-tax-on-sugary-foods', ref('B', 6, '(b)(iii)'),
    H.q(6, 'Outline how imposing a tax on sugary foods', ' (35)'), '4 + 3', 7,
    [anyN('r-1', 'A benefit — any two', 7, 2, 4,
          H.split('1. Revenue for state', '1st correct point at 4 marks.',
                  ['Revenue for state', 'Help fund health initiatives', 'Reduce consumption of sugary foods',
                   'Help reduce future health costs / healthier population']),
          'Two benefits: ' + H.traced('1st correct point at 4 marks.') + ' ' + H.traced('2nd correct point at 3 marks.'), steps=[4, 3])],
    kind='fixed', stem=q6b, **B)
favour = [cc(x) for x in ('Reduced cost for taxpayers', 'Opportunity cost The saving', 'Effect on third level institutions',
                          'Equitable Those students')]
against = [cc(x) for x in ('Discourage people from attending', 'Reduce skills of population', 'Reduced incentive to invest',
                           'Inequitable The additional', 'Increased debt levels')]
add('sb-q6-c', '1-3', 'students-paying-towards-third-level', ref('B', 6, '(c)'),
    H.q(6, 'State and explain two economic arguments in favour of and two economic arguments against', ' (20)'), '2 @ 5 + 2 @ 5', 20,
    [anyN('r-favour', 'An argument in favour — any two', 10, 2, 5, favour, 'Two arguments in favour, ' + H.traced('2 at 5 marks.')),
     anyN('r-against', 'An argument against — any two', 10, 2, 5, against, 'Two arguments against, 5 marks each.')],
    kind='fixed', **B)

# Q7 ─ comparative advantage; competitiveness; slower euro-area growth
q7a = H.q(7, 'The table below illustrates the Law of Comparative Advantage.', ' Country')
q7a_table = PAP + 'p07-q7a-table'
add('sb-q7-a-i', '4-2', 'the-law-of-comparative-advantage', ref('B', 7, '(a)(i)'),
    H.q(7, 'State the Law of Comparative Advantage.', ' (ii)'), '10', 10,
    [point('r-1', H.opt('The law states that a country should specialise', '\n10 (6+4) marks.'), 10,
           'The law, ' + H.traced('10 (6+4) marks.'))],
    kind='fixed', stem=q7a, figure=q7a_table, **B)
q7aii = H.q(7, 'Explain how both countries benefit from international trade in the above example.', ' (iii)')
add('sb-q7-a-ii-option-1', '4-2', 'how-both-countries-gain-from-trade', ref('B', 7, '(a)(ii)', 'option 1'),
    f'{q7aii} Answer for: {H.traced("Option 1")}, how the world gains.', '3 + 3 + 2', 8,
    [point('r-clothing', H.traced('With specialisation the output of clothing has increased by 10 units or 33.33%.'), 3,
           'The scheme’s Option 1: ' + H.traced('If the student assumes that there are only 2 countries in the world and interprets the '
                                                'question as saying how the world will benefit from trade.')
           + ' The rise in clothing, 3 marks: the scheme prints ' + H.traced('8 (3+3+2) marks') + ' beneath its three bullets, read here '
           'in the order it prints them.'),
     point('r-food', H.traced('The output of Food has decreased by 20 units or 20 %'), 3, 'The fall in food, 3 marks.'),
     point('r-better-off', H.opt('Therefore since the increase in the output of clothing', '\n8 (3+3+2) marks.'), 2,
           'The world is better off, 2 marks.')],
    kind='fixed', stem=q7a, figure=q7a_table, **B)
add('sb-q7-a-ii-option-2', '4-2', 'how-both-countries-gain-from-trade', ref('B', 7, '(a)(ii)', 'option 2'),
    f'{q7aii} Answer for: {H.traced("Option 2")}, each country apart from part (iii).', '8', 8,
    [point('r-uk', 'UK — ' + H.opt('For each unit of Clothing which the UK imports', '\nChina'), None,
           'The scheme’s Option 2: ' + H.traced('The student answers part (ii) independently of answering part (iii)') + '. The UK.'),
     point('r-china', 'China — ' + H.opt('For each item of Food which China imports', '\nOption 3'), None,
           'China. Claim the complete answer: the scheme prices the option 8 marks without dividing it.')],
    kind='questionTotal', stem=q7a, figure=q7a_table, **B)
add('sb-q7-a-ii-option-3', '4-2', 'how-both-countries-gain-from-trade', ref('B', 7, '(a)(ii)', 'option 3'),
    f'{q7aii} Answer for: {H.traced("Option 3")}, from the terms of trade in part (iii).', '8', 8,
    [point('r-uk', H.opt('If the UK can get more than', '\nIf China'), None,
           'The scheme’s Option 3: ' + H.traced('The student answers part (iii) of the question first and then answers part (ii) using '
                                                'the info obtained.') + ' The UK.'),
     point('r-china', H.opt('If China can get more than', '\n8 marks'), None,
           'China. Claim the complete answer: the scheme prices the option ' + H.traced('8 marks') + ' without dividing it.')],
    kind='questionTotal', stem=q7a, figure=q7a_table, **B)
tot = [f"{H.traced('UK')} — {H.traced('1 unit of Food is the equivalent of / equals 0.25 units of clothing')}",
       f"{H.traced('UK')} — {H.traced('1 unit of Clothing is the equivalent of / equals 4 units of food')}",
       f"{H.traced('China')} — {H.traced('1 unit of Food is the equivalent of / equals 0.33 units of clothing')}",
       f"{H.traced('China')} — {H.traced('1 item of Clothing is the equivalent of / equals 3 units of food')}",
       H.traced('FOOD: lies between 0.25 units of clothing and 0.3 units of clothing.'),
       H.traced('CLOTHING: lies between 4 units of food and 3 units of food.')]
add('sb-q7-a-iii', '4-2', 'the-terms-of-trade', ref('B', 7, '(a)(iii)'),
    H.q(7, 'Calculate the terms of trade for both goods.', ' (30)'), '4 @ 3', 12,
    [anyN('r-1', 'A line of the working — any four', 12, 4, 3, tot,
          H.traced('4 at 3 marks.') + ' The scheme does not say which four of its lines earn them; its last two '
          'lines give the possible terms of trade. The working is shown with the answer.')],
    kind='fixed', stem=q7a, figure=SOL + 'p32-q7aiii-working', **B)
beside_ask(cards[-1], q7a_table)
pick('sb-q7-b-i', '4-2', 'what-makes-irish-firms-competitive', ref('B', 7, '(b)(i)'),
     H.q(7, 'Discuss three economic factors which affect the competitiveness of Irish firms', ' (ii)'), 'A factor — any three',
     H.split('1. Irish inflation rates v. that of competitors', '3 at 5 marks each.',
             ['Irish inflation rates v. that of competitors', 'Value of the Euro v. that of other currencies', 'Transport costs',
              'Labour Market - Costs', 'Government policies which affect a firm’s cost structure', 'Costs of production']),
     3, 5, 'Three factors, ' + H.traced('3 at 5 marks each.'), **B)
pick('sb-q7-b-ii', '4-2', 'how-trade-benefits-irish-consumers', ref('B', 7, '(b)(ii)'),
     H.q(7, 'Outline how international trade benefits Irish consumers.', ' (25)'), 'A benefit — any two',
     H.split('1. Greater choice of commodities', '2 at 5 marks each.',
             ['Greater choice of commodities / Commodities not produced in Ireland', 'More competitive prices', 'Innovation']),
     2, 5, 'Two benefits, ' + H.traced('2 at 5 marks each.'), **B)
pick('sb-q7-c', '4-2', 'slower-growth-in-the-euro-area', ref('B', 7, '(c)'),
     H.q(7, 'Discuss the possible effects on the Irish economy of the slowdown', ' (20)'), 'An effect — any four',
     H.split('1. Exports\nWith declining', '4 at 5 marks each.',
             ['Exports', 'Employment', 'Standard of living', 'Government Finances', 'Emigration', 'Reduced FDI', 'Imports',
              'Interest rate reduction']),
     4, 5, 'Four effects, ' + H.traced('4 at 5 marks each.'), stem=H.q(7, '‘Euro area growth is forecast to slow down', ' Discuss'), **B)

# Q8 ─ emigration; the Live Register; Keynes
q8a = H.q(7, 'It is often said that ‘push’ factors and ‘pull’ factors drive emigration.', ' (i)')
q8ai = H.q(7, 'Describe two economic ‘push’ factors OR two economic ‘pull’ factors', ' (ii)')
push = [cc(x) for x in ('Economic recession in Ireland This', 'Wage rates in Ireland Wage', 'Rising levels of taxation in Ireland.',
                        'Prospects for economic recovery Some')]
pull = [cc(x) for x in ('Job opportunities abroad', 'Develop skills abroad', 'Better standard of living The possibility',
                        'More optimistic outlook')]
for word, head, opts in (('push', 'Push factors', push), ('pull', 'Pull factors', pull)):
    pick(f'sb-q8-a-i-{word}', '3-2', 'push-and-pull-factors', ref('B', 8, '(a)(i)', f'{word} factors'),
         f'{q8ai} Justify the choice: {word.upper()} FACTORS.', H.traced(head) + ' — any two', opts, 2, 5,
         'Two factors. ' + H.traced('Any 2 push OR pull factors at 5 marks each.')
         + ' The scheme credits push and pull factors, each with its own column.', stem=q8a, **B)
neg = [cc(x) for x in ('Higher dependency ratio', 'Opportunity costs The state', 'Loss of skills within the economy',
                       'Smaller domestic market As', 'Upward pressure on Irish wage levels')]
pos = [cc(x) for x in ('Unemployment reduced', 'Emigrants returning to Ireland', 'Contacts / Export opportunities',
                       'Demand for state services')]
add('sb-q8-a-ii', '3-2', 'consequences-of-emigration', ref('B', 8, '(a)(ii)'),
    H.q(7, 'State and explain the positive and negative consequences of emigration', ' (30)'), '2 @ 5 + 2 @ 5', 20,
    [anyN('r-negative', 'A negative consequence — any two', 10, 2, 5, neg, 'Two negative consequences, ' + H.traced('2 at 5 marks.')),
     anyN('r-positive', 'A positive consequence — any two', 10, 2, 5, pos, 'Two positive consequences, 5 marks each.')],
    kind='fixed', stem=q8a, **B)
add('sb-q8-b-i', '3-2', 'the-live-register-rate-in-2012', ref('B', 8, '(b)(i)'),
    H.q(7, 'State the rate of unemployment in Ireland during 2012', ' (ii)'), '5', 5,
    [point('r-1', H.traced('14.8% (May 2012: 432,907)'), 5,
           'The rate, 5 marks. The scheme also prints the forecast rate for the year.',
           accepts=[H.traced('(Forecasted rate during 2012: 14.1%)')])], **B)
included = [H.opt('It includes people who are legitimately working part time', '\n(b) It includes'),
            H.opt('It includes those people who may be drawing social welfare', '\n(c) It includes'),
            H.opt('It includes those people who may not be actively seeking employment.', '\n(d) It includes', ),
            H.opt('It includes those signing on only for', '\nExcluded but should NOT be:')]
excluded = [H.opt('People who though unemployed and seeking employment', '\n3 at 5 marks each.')]
pick('sb-q8-b-ii', '3-2', 'limits-of-the-live-register', ref('B', 8, '(b)(ii)'),
     H.q(7, 'Outline the limitations of the Live Register', ' (20)'), 'A limitation — any three',
     side('Included but should NOT be', included) + side('Excluded but should NOT be', excluded),
     3, 5, 'Three limitations, ' + H.traced('3 at 5 marks each.'), **B)
q8c = H.q(7, 'The economist John Maynard Keynes', ' (i)')
add('sb-q8-c-i', '3-1', 'keynes-and-fiscal-policy', ref('B', 8, '(c)(i)'), H.q(7, 'Explain the above statement.', ' (ii)'), '9 + 4', 13,
    [anyN('r-1', 'A point — both', 13, 2, 9,
          [H.traced('He suggested government cut direct taxation to boost income, therefore boosting expenditure to help create jobs.'),
           H.traced('The government could increase its expenditure, thereby increasing demand (through direct public works) so as to '
                    'help create jobs.')],
          'The explanation: the scheme prints ' + H.traced('13 (9+4) marks') + ' beneath its two bullets and does not say which earns '
          'which, so the first correct point is claimed at 9 and the second at 4.', steps=[9, 4])],
    kind='fixed', stem=q8c, **B)
pick('sb-q8-c-ii', '0-0', 'keynes-other-key-concepts', ref('B', 8, '(c)(ii)'),
     H.q(7, 'Discuss two other key concepts which Keynes contributed to economic thought.', ' (25)'), 'A concept — any two',
     H.split('Equilibrium National Income.', '2 at 6 marks each.',
             ['Equilibrium National Income.', 'Output is demand determined.', 'Investment decisions by entrepreneurs.',
              'Investment could be less than savings.', 'New Economic Concepts – The Multiplier', 'Liquidity Preference Theory:',
              'Managed system of exchange rates:']),
     2, 6, 'Two concepts, ' + H.traced('2 at 6 marks each.'), stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
