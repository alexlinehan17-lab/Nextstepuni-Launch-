#!/usr/bin/env python3
"""Economics 2010 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2010-hl-ev.json, made
from a visual sweep of all 8 paper pages and 35 scheme pages before any 2010
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The scheme reprints each question above its answer, so a
slice always starts after the reprinted wording. A stem stops before any
printed table: the table is the crop beside the typed ask. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.

The scheme file (examiner-reports/economics/schemes/2010-hl.md) was built with
the appenders' cover check pointed at the file itself: this scheme's cover
prints its level in capitals ("HIGHER LEVEL"), which the check otherwise reads
past. Its page numbers are the PDF's and equal the printed ones.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2010, 'higher', 'LC034ALP000EV')
D = OldDeck(2010, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2010-HL-scheme-'
PAP = 'economics-2010-HL-paper-'
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
CELLS = [ln.strip() for ln in H.full_md.split('<!-- markbank:table-cells -->', 1)[1]
         .split('<!-- /markbank:table-cells -->', 1)[0].splitlines()]


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def pair(first):
    """A two-column row: a cell and the cell printed after it."""
    i = CELLS.index(first)
    return f'{H.traced(first)} — {H.traced(CELLS[i + 1])}'


def lettered(options):
    """Responses read without the next response's own letter ("(d)"), which the
    scheme prints at the end of the line before it."""
    return [H.traced(re.sub(r'\s*\([a-g]\)$', '', o)) for o in options]


def bare(options):
    """Responses read without a colon the scheme prints after a heading that stands alone."""
    return [H.traced(o.rstrip(':').strip()) for o in options]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ falling land prices
add('sa-q1', '1-0', 'why-land-prices-fell', ref('A', 1),
    H.q(2, 'State three reasons why prices of land for housing development have fallen', ' (i)'), '6 + 5 + 5', 16,
    [anyN('r-1', 'A reason — any three', 16, 3, 6,
          lettered(H.split('(a) Deflation:', '3 points: 6 marks + 5 marks + 5 marks each',
                           ['Deflation:', 'Recession:', 'Uncertainty about jobs', 'Credit crunch:', 'Emigration is rising',
                            'Reduced speculation in property:', 'Overcapacity in housing market:'])),
          'Three reasons: ' + H.traced('3 points: 6 marks + 5 marks + 5 marks each = 16 marks.') + ' The first correct 6.',
          steps=[6, 5, 5])],
    kind='fixed', **A)

# Q2 ─ raising consumer spending
pick('sa-q2', '3-1', 'raising-consumer-spending', ref('A', 2),
     H.q(2, 'Outline two measures the Irish Government could take to increase consumer spending', ' Answer 1:'), 'A measure — any two',
     lettered(H.split('(a) Decrease indirect taxes e.g. VAT', '2 points at 8 marks each.',
                      ['Decrease indirect taxes e.g. VAT', 'Provide incentives to consumers to spend',
                       'Decrease direct taxes e.g. income taxes', 'Generate confidence in the economy',
                       'Facilitate lending by the financial institutions', 'Capital investment programme:'])),
     2, 8, 'Two measures, ' + H.traced('2 points at 8 marks each. State: 4 marks. Explain: 4 marks.'), **A)

# Q3 ─ a unit elastic demand
add('sa-q3', '1-4', 'a-unit-elastic-demand', ref('A', 3),
    H.q(2, 'A consumer spends €200 monthly on Product A', ' Workings:'), '6 @ 2 + 4', 16,
    [anyN('r-starred', 'Each starred figure of the working', 12, 6, 2,
          [H.traced(x) for x in ('- 20*', '50*', '( 4.50)*', '(180)*', '- *', '1.0*')],
          H.traced('6 * at 2 marks each = 12 marks') + '. The working is shown with the answer: the quantities 100 and 80 units '
          '(€200 over each price), then -20 over 50, times €2 + €2.50 (4.50) over 100 + 80 (180), = -1.0, the minus sign and '
          'the 1.0 starred apart.'),
     point('r-explanation', H.traced('It has a minus sign / obeys the law of demand. This good is unit elastic because PED = 1.'), 4,
           'The explanation, ' + H.traced('4 marks') + ', which the scheme does not divide between its two sentences. '
           + H.traced('(Reference to a normal good max: 2 marks)'))],
    kind='fixed', figure=SOL + 'p04-q3-working', **A)

# Q4 ─ non-price competition
add('sa-q4', '2-0', 'non-price-competition', ref('A', 4),
    H.q(2, 'Define the term ‘non-price competition’. State two examples.', ' Definition:'), '12 + 2 @ 2', 16,
    [point('r-definition', H.traced('Competition between firms where each firm tries to increase its sales / market share by methods '
                                    'other than changing prices.'), 12, 'The definition, 12 marks.'),
     anyN('r-examples', 'An example — any two', 4, 2, 2,
          H.split('Branding: establishing', '2 at 2 marks each.',
                  ['Branding:', 'Packaging:', 'Competitive Advertising:', 'Opening hours:', 'Quality of service:', 'Sponsorship:',
                   'Special offers:']),
          'Two examples, ' + H.traced('2 at 2 marks each.'))],
    kind='fixed', **A)

# Q5 ─ entrepreneurship
add('sa-q5', '0-1', 'why-entrepreneurship-matters', ref('A', 5),
    H.q(2, 'State three economic reasons why entrepreneurship is important', ' (i)'), '6 + 5 + 5', 16,
    [anyN('r-1', 'A reason — any three', 16, 3, 6,
          H.split('1. Creates employment', '3 points: 6 marks + 5 marks each',
                  ['Creates employment', 'Organises production', 'Decides what commodities will be produced',
                   'Decides what prices to be charged', 'Encourages further investment', 'Provides an outlet for savers funds',
                   'Generates revenue for the government', 'May increase exports', 'Creates wealth within the country']),
          'Three reasons: ' + H.traced('3 points: 6 marks + 5 marks each + 5 marks each = 16 marks.') + ' The first correct 6.',
          steps=[6, 5, 5])],
    kind='fixed', **A)

# Q6 ─ the multiplier
add('sa-q6', '3-0', 'the-irish-multiplier', ref('A', 6),
    H.q(3, 'It is estimated that in the Irish economy:', ' Answer:'), '5 @ 1 + 12', 17,
    [anyN('r-working', 'Each item of the working', 5, 5, 1, [H.traced(x) for x in ('1', '0.25', '0.3', '0.2', '1.33')],
          H.traced('5 marks: 1 mark for each item.') + ' The working is shown with the answer: 1 over (0.25 + 0.3 + 0.2) = 1.33, '
          'the 1, the three propensities and the answer each an item.'),
     point('r-meaning', H.traced('This means that for any given injection into the economy national income will increase by 1.33 times'),
           12, 'The meaning of the figure, 12 marks.')],
    kind='fixed', figure=SOL + 'p06-q6-working', **A)

# Q7 ─ the Live Register
add('sa-q7', '3-2', 'limits-of-the-live-register', ref('A', 7),
    H.q(3, 'Outline two limitations in using the Live Register', ' (i)'), '9 + 8', 17,
    [anyN('r-1', 'A limitation — any two', 17, 2, 9,
          bare([o.split(' •')[0] for o in lettered(
              H.split('(a) It includes people who are legitimately', '2 points: 9 marks + 8 marks.',
                      ['It includes people who are legitimately', 'It includes people who may be drawing',
                       'It includes people who may not be actively', 'It includes those signing on only']))]),
          'Two limitations: ' + H.traced('2 points: 9 marks + 8 marks.') + ' The first correct 9.', steps=[9, 8])],
    kind='fixed', **A)

# Q8 ─ rent of ability
add('sa-q8', '2-1', 'rent-of-ability', ref('A', 8),
    H.q(3, 'Explain, with the aid of an example, the meaning of the term', ' (17 marks)'), '12 + 5', 17,
    [point('r-meaning', H.traced('Economic rent/SNP earned by an entrepreneur/labour/human effort due to their business acumen / '
                                 'innate talent/natural talent'), 12, 'The meaning, 12 marks.'),
     point('r-example', H.traced('Premier League footballer – superior physical ability.'), 5,
           'An example, 5 marks: the scheme accepts ' + H.traced('any appropriate example') + '.')],
    kind='fixed', **A)

# Q9 ─ water charges
add('sa-q9', '1-3', 'the-case-for-water-charges', ref('A', 9),
    H.q(3, 'Outline three possible economic arguments in favour of the introduction of water charges', ' (i)'), '6 + 6 + 5', 17,
    [anyN('r-1', 'An argument — any three', 17, 3, 6,
          H.split('1. Reduce consumption of water / discourage waste.', '3 points: 6 marks + 6 marks + 5 marks.',
                  ['Reduce consumption of water / discourage waste.', 'Generate revenue for the service provider',
                   'Improve quality of water supply', 'Encourage investment in alternative technologies.',
                   'Helps reduce need to raise direct taxation.', 'Impossible to evade / helps government financial planning.']),
          'Three arguments: ' + H.traced('3 points: 6 marks + 6 marks + 5 marks.') + ' The first two correct 6 each.',
          steps=[6, 6, 5])],
    kind='fixed', stem=H.q(3, 'The Irish Government is considering the introduction of water charges', ' Outline'), **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ the market for Quencher; PED; cutting soft-drink consumption
q1a = H.q(4, 'The data below represents the market demand and the market supply schedules', ' Price')
q1a_table = PAP + 'p04-q1a-table'
q1a_diagram = SOL + 'p08-q1a-diagram'
# The scheme's own schedule: price, quantity demanded, quantity supplied, new quantity supplied.
schedule = [ln.split() for ln in H.chunk('2.00 40 5 25', '\n(i) Using').strip().splitlines()]
assert [len(r) for r in schedule] == [4] * 5, schedule
plotted = lambda col: [f'{H.traced(r[0])} — {H.traced(r[col])}' for r in schedule]
add('sb-q1-a-i', '1-0', 'demand-supply-and-equilibrium', ref('B', 1, '(a)(i)'),
    H.q(4, 'Using the above data, draw the diagram showing the market demand and market supply curves', ' (ii)'),
    '5 @ 1 + 1 + 5 @ 1 + 1 + 3 @ 1', 15,
    [anyN('r-demand', 'The demand curve — each point plotted (price € — quantity demanded, ’000 units)', 5, 5, 1, plotted(1),
          'The demand curve’s five points, ' + H.traced('D/C: 5 points at 1 mark each') + '. The completed diagram is shown with the '
          'answer.'),
     point('r-demand-label', f"{H.traced('D/C')} — {H.traced('Correct label')}", 1,
           'Labelling the demand curve, 1 mark: the scheme’s diagram labels it D.'),
     anyN('r-supply', 'The supply curve — each point plotted (price € — quantity supplied, ’000 units)', 5, 5, 1, plotted(2),
          'The supply curve’s five points, ' + H.traced('S/C: 5 points at 1 mark each') + '.'),
     point('r-supply-label', f"{H.traced('S/C')} — {H.traced('Correct label')}", 1,
           'Labelling the supply curve, 1 mark: the scheme’s diagram labels it S1.'),
     anyN('r-equilibrium', 'The equilibrium — each of the three', 3, 3, 1,
          [H.traced('Equilibrium point'), f"{H.traced('Equilibrium price')} — {H.traced('2.50')}",
           f"{H.traced('Equilibrium Quantity')} — {H.traced('20')}"],
          H.traced('Equilibrium point + Equilibrium price + Equilibrium Quantity: 3 at 1 mark each.') + ' The diagram marks the '
          'point where the curves cross at €2.50 and 20 (’000 units).')],
    kind='fixed', stem=q1a, figure=q1a_diagram, **B)
beside_ask(cards[-1], q1a_table)
add('sb-q1-a-ii', '1-0', 'a-market-in-equilibrium', ref('B', 1, '(a)(ii)'),
    H.q(4, 'Explain what it means for the market ‘to be in equilibrium’.', ' (iii)'), '7', 7,
    [point('r-1', H.traced('where quantity demanded equals/meets quantity supplied and there is no tendency for prices to change.'), 7,
           'The explanation, 7 marks.')],
    kind='fixed', stem=q1a, figure=q1a_table, **B)
add('sb-q1-a-iii', '1-0', 'a-fall-in-costs-shifts-supply', ref('B', 1, '(a)(iii)'),
    H.q(4, 'Assume costs of production fell, resulting in an extra 20,000 units supplied', ' (30 marks)'), '5 @ 1 + 3 @ 1', 8,
    [anyN('r-new-supply', 'The new supply curve — each point plotted (price € — new quantity supplied, ’000 units)', 5, 5, 1,
          plotted(3),
          'The new supply curve’s five points, ' + H.traced('New S/C: 5 points at 1 mark each') + ', from the scheme’s New Quantity '
          'Supplied column. The completed diagram is shown with the answer (S2).'),
     anyN('r-new-equilibrium', 'The new equilibrium — each of the three', 3, 3, 1,
          [H.traced('Equilibrium point'), f"{H.traced('Equilibrium price')} — {H.traced('2.25')}",
           f"{H.traced('Equilibrium Quantity')} — {H.traced('30')}"],
          H.traced('Equilibrium point + Equilibrium price + Equilibrium Quantity: 3 at 1 mark each.') + ' The diagram marks the '
          'point where the new supply curve crosses demand at €2.25 and 30 (’000 units).')],
    kind='fixed', stem=q1a, figure=q1a_diagram, **B)
beside_ask(cards[-1], q1a_table)
pick('sb-q1-b-i', '1-4', 'what-affects-price-elasticity', ref('B', 1, '(b)(i)'),
     H.q(4, 'Outline four factors which affect price elasticity of demand (PED).', ' (ii)'), 'A factor — any four',
     H.split('1. The availability of close substitutes.', '4 points at 5 marks each: State: 2 marks.',
             ['The availability of close substitutes.', 'Complementary goods.', 'Is the commodity a luxury or necessity?',
              'The proportion of income which is spent on the commodity.', 'The durability of the commodity.',
              'Expectations as to future changes in price.', 'The length of time allowed for adjustment to price changes.',
              'Consumer habits / brand loyalty.', 'Number of alternative uses the good has.']),
     4, 5, 'Four factors, ' + H.traced('4 points at 5 marks each: State: 2 marks. Explain: 3 marks.'), **B)
add('sb-q1-b-ii', '1-4', 'a-ped-of-minus-3-8', ref('B', 1, '(b)(ii)'),
    H.q(4, 'The PED for the soft drink ‘Quencher’ has been calculated at', ' (30 marks)'), '5 + 2 + 3', 10,
    [point('r-sign', f"{cc('Sign is minus', whole=True)} — {H.traced('As price increases, demand will fall /obeys the law of demand')}", 5,
           'The minus sign, 5 marks. ' + H.traced('(Reference to a normal good max: 2 marks)')),
     heading('r-value', cc('Value is 3.8', whole=True) + ' — either',
             [H.traced('This is a price elastic good'), H.traced('This is a luxury good')], 2,
             'The value, 2 marks: the scheme accepts either reading.'),
     heading('r-why', 'Why — either',
             [H.traced('The percentage change in quantity demand is greater than then the percentage change in price'),
              H.traced('Because when price rises the demand will fall by a greater percentage, indicating that the good is not a '
                       'necessity.')], 3,
             'Why, 3 marks: the scheme prints the first beside a price elastic good and the second beside a luxury good.')],
    kind='fixed', **B)
pick('sb-q1-c', '1-3', 'cutting-soft-drink-consumption', ref('B', 1, '(c)'),
     H.q(4, 'Advise the Minister for Health and Children on possible economic actions', ' (15 marks)'), 'An action — any three',
     [pair(x) for x in ('Taxation: Increase taxes on soft drinks', 'Education: Education / Awareness campaign',
                        'Legislation: Introduce legislative changes',
                        'Subsidisation: Subsidise the price of substitute goods / Reduce VAT rates on substitute goods')],
     3, 5, 'Three actions, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks.'),
     stem=H.q(4, 'Many health advisors wish to reduce the consumption of soft drinks.', ' Advise'), **B)

# Q2 ─ monopoly; price discrimination; monopoly against perfect competition
pick('sb-q2-a-i', '2-0', 'assumptions-of-monopoly', ref('B', 2, '(a)(i)'),
     H.q(4, 'State and explain three assumptions underlying the theory of monopoly.', ' (ii)'), 'An assumption — any three',
     H.split('One firm in the industry\n', '3 points at 5 marks each. State: 2 marks.',
             ['One firm in the industry', 'Controls price or output', 'Profit maximisation', 'Barriers to entry']),
     3, 5, 'Three assumptions, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), **B)
pick('sb-q2-a-ii', '2-0', 'advantages-of-monopoly', ref('B', 2, '(a)(ii)'),
     H.q(4, 'Outline two possible advantages of monopoly as a market structure.', ' (25 marks)'), 'An advantage — any two',
     H.split('Economies of scale\nProduction', '2 points at 5 marks each. State: 2 marks.',
             ['Economies of scale', 'Guarantee supply of product / service', 'Employment', 'Reduced use of scarce resources',
              'Potential for innovation/ R & D']),
     2, 5, 'Two advantages, ' + H.traced('2 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), **B)
q2b = H.q(4, 'Iarnród Eireann (Irish Rail) is the state monopoly', ' (i)')
add('sb-q2-b-i', '2-0', 'price-discrimination', ref('B', 2, '(b)(i)'),
    H.q(4, 'Explain the underlined term, giving one example as practiced by Iarnród Eireann.', ' (ii)'), '6 + 2', 8,
    [point('r-definition', H.traced('Price Discrimination') + ' — ' + H.traced('When a good or service is sold to different consumers / different '
                                                                'markets at varying ratios between marginal cost and price or the '
                                                                'price difference is not due to difference in the cost of production.'),
           6, 'Price discrimination, 6 marks.'),
     heading('r-example', 'An example — either',
             [H.traced('A student being charged a lower rate for travel from Cork to Dublin than another passenger'),
              H.traced('Consumers being charged different rates for peak and off-peak travel.')], 2,
             'An example, 2 marks: the scheme accepts either.')],
    kind='fixed', stem=q2b, **B)
pick('sb-q2-b-ii', '2-0', 'conditions-for-price-discrimination', ref('B', 2, '(b)(ii)'),
     H.q(4, 'State and explain three conditions necessary for price discrimination to take place.', ' (20 marks)'),
     'A condition — any three',
     H.split('1. Monopoly Power.', '3 points at 4 marks each.',
             ['Monopoly Power.', 'Separation of markets.', 'Different consumer price elasticities of demand.', 'Consumer Indifference.',
              'Lack of awareness by consumers.', 'Consumer attitudes to the goods.']),
     3, 4, 'Three conditions, ' + H.traced('3 points at 4 marks each. State: 2 marks. Explain: 2 marks.'), stem=q2b, **B)
add('sb-q2-c', '2-0', 'monopoly-against-perfect-competition', ref('B', 2, '(c)'),
    H.q(4, 'Using suitably labelled diagram(s), compare the long run equilibrium position', ' (30 marks)'),
    '10 @ 1 + 3 @ 2 + 3 + 3 + 4 + 4', 30,
    [anyN('r-diagram-1', 'The diagram — each item circled 1', 10, 10, 1,
          [H.traced(x) for x in ('P', 'Q', 'MC', 'AC', 'PM', 'PC', 'QM', 'Qc', 'F', 'E')],
          'The diagram, ' + H.traced('10 items at 1 mark each + 3 items at 2 marks each = 16 marks.') + ' The ten circled 1: the '
          'axes P and Q, MC, AC, the prices PM and PC, the outputs QM and Qc and the equilibrium points F and E. The completed '
          'diagram is shown with the answer.'),
     anyN('r-diagram-2', 'The diagram — each item circled 2', 6, 3, 2, [H.traced(x) for x in ('D = AR=MR', 'D = AR [M]', 'MR')],
          'The three circled 2: the perfectly competitive firm’s D = AR = MR, the monopoly’s D = AR and its MR.'),
     point('r-price', f"{H.traced('Price')} — {H.traced('A firm in a monopoly position sells its output at a higher price– Pm rather than Pc.')}",
           3, 'Price, 3 marks.'),
     point('r-output', f"{H.traced('Output')} — "
           f"{H.traced('A firm in a monopoly position produces a smaller output than in perfect competition – Qm rather than Qc.')}",
           3, 'Output, 3 marks.'),
     anyN('r-profits', 'Profits — each part marked (1)', 4, 4, 1,
          [H.traced(x) for x in ('Because AR = AC', 'a firm in PC earns normal profit', 'Because AR > AC',
                                 'a firm in monopoly can earn SNPs.')],
          'Profits, ' + H.traced('4 marks') + ': (2) for each firm, 1 for each part the scheme marks (1).'),
     anyN('r-efficiency', 'Efficiency — each part marked (1)', 4, 4, 1,
          [H.traced(x) for x in ('A firm in PC produces at the lowest point of AC', 'and so is efficient',
                                 'A monopoly may not produce at the lowest point of AC', 'and so maybe inefficient')],
          'Efficiency, 4 marks: (2) for each firm, 1 for each part the scheme marks (1).')],
    kind='fixed', figure=SOL + 'p13-q2c-diagram', **B)

# Q3 ─ labour terms; the efficiency of labour; the minimum wage; the black economy
add('sb-q3-a', '2-1', 'four-labour-market-terms', ref('B', 3, '(a)'),
    H.q(5, 'With reference to the factor of production labour, explain the following terms:', ' (20 marks)'), '4 @ 5', 20,
    [point('r-derived', H.traced('Derived Demand') + ' — ' + H.traced('Where labour is demanded for its contribution to the production process.'), 5,
           'Derived demand: ' + H.traced('4 at 5 marks each.')),
     point('r-mrp', H.traced('MRP') + ' — ' + H.traced('The extra revenue earned when an additional unit of labour/ is employed.'), 5,
           'Marginal revenue productivity, 5 marks.'),
     point('r-drift', H.traced('Wage Drift') + ' — ' + H.traced('When wage levels rise above the negotiated levels.'), 5, 'Wage drift, 5 marks.'),
     point('r-cyclical', H.traced('Cyclical Unemployment') + ' — ' + H.traced('Unemployment that results from reduced demand for goods and services.'), 5,
           'Cyclical unemployment, 5 marks. The scheme also prints the bracketed wording.',
           accepts=[H.traced('(Unemployment resulting from the economic recession / decline in trade cycles / reduced aggregate '
                             'demand).')])],
    kind='fixed', **B)
pick('sb-q3-b-i', '2-1', 'the-efficiency-of-labour', ref('B', 3, '(b)(i)'),
     H.q(5, 'State and explain four factors which influence the efficiency of labour', ' Recently'), 'A factor — any four',
     [cc(x) for x in ('Education / Training / Qualifications:', 'Degree of specialisation:', 'Innate / natural talent of the worker:',
                      'Climatic conditions:', 'Quality of the other factors:', 'Management expertise:', 'Availability of other factors:',
                      'Commitment of the worker:', 'Living conditions of the workforce:')],
     4, 5, 'Four factors, ' + H.traced('4 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), **B)
wage_adv = [cc(x) for x in ('Lower labour costs', 'Lower selling prices', 'Increased demand / protection of jobs', 'Investment stimulus',
                            'Reduced risk of re-location')]
wage_dis = [cc(x) for x in ('Reduced standard of living', 'Reduced aggregate demand', 'Impact on general', 'Workers on lower incomes',
                            'Discourage employment')]
add('sb-q3-b-ii', '2-1', 'cutting-the-minimum-wage', ref('B', 3, '(b)(ii)'),
    H.q(5, 'Outline one possible economic advantage and one possible economic disadvantage', ' (30 marks)'), '5 + 5', 10,
    [anyN('r-advantage', 'An advantage — any one', 5, 1, 5, wage_adv,
          'One advantage, ' + H.traced('1 at 5 marks.') + ' ' + H.traced('State 2 marks. Explain: 3 marks') + '.'),
     anyN('r-disadvantage', 'A disadvantage — any one', 5, 1, 5, wage_dis, 'One disadvantage, 5 marks, the same way.')],
    kind='fixed', stem=H.q(5, 'Recently the Organisation for Economic Cooperation and Development', ' (ii)'), **B)
q3c = H.q(5, 'Ireland’s ‘Black Economy’', ' (i)')
pick('sb-q3-c-i', '3-0', 'effects-of-the-black-economy', ref('B', 3, '(c)(i)'),
     H.q(5, 'State and explain three economic effects of this activity in Ireland.', ' (ii)'), 'An effect — any three',
     H.split('Loss of tax revenue to the government.', '3 points at 5 marks each. State: 2',
             ['Loss of tax revenue to the government.', 'Decline in legitimate business activity', 'Increased government expenditure on',
              'Pressure on government services', 'Increase crime levels.', 'Standards of products/services']),
     3, 5, 'Three effects, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), stem=q3c, **B)
pick('sb-q3-c-ii', '3-1', 'discouraging-the-black-economy', ref('B', 3, '(c)(ii)'),
     H.q(5, 'Outline two economic measures the Irish Government could take to discourage this activity.', ' (25 marks)'),
     'A measure — any two',
     H.split('1. Reduce direct taxation rates.', '2 at 5 marks each. State: 2 marks.',
             ['Reduce direct taxation rates.', 'Reduce indirect taxation.', 'Better enforcement by revenue commissioners.',
              'Educate the public about the importance', 'Simplification of the tax system']),
     2, 5, 'Two measures, ' + H.traced('2 at 5 marks each. State: 2 marks. Explain: 3 marks.'), stem=q3c, **B)

# Q4 ─ the tax base; a good tax system; the carbon tax; the national debt
q4a = H.q(5, '“Next year, almost half of income earners will pay no income tax', ' (i)')
add('sb-q4-a-i', '3-1', 'taxation-revenues-and-the-tax-base', ref('B', 4, '(a)(i)'),
    H.q(5, 'Explain briefly the underlined terms.', ' (ii)'), '5 + 5', 10,
    [point('r-revenues', H.traced('Taxation revenues') + ' — ' + H.traced('Monies/incomes received by the government in the form of direct & indirect '
                                                           'taxes, and used in the running of the country.'), 5,
           'Taxation revenues, ' + H.traced('5 marks') + '.'),
     point('r-base', H.traced('Broaden the tax base') + ' — ' + H.traced('Increasing the number of people / areas on which tax is levied / in the tax net.'),
           5, 'Broadening the tax base, 5 marks.')],
    kind='fixed', stem=q4a, **B)
pick('sb-q4-a-ii', '3-1', 'a-good-taxation-system', ref('B', 4, '(a)(ii)'),
     H.q(5, 'Discuss the characteristics of a good taxation system.', ' (30 marks)'), 'A characteristic — any five',
     H.split('1. Taxes should be equitable', '5 at 4 marks each.',
             ['Taxes should be equitable', 'Taxes should be certain', 'Taxes should be convenient', 'Taxes should be economic',
              'Taxes should not act as a disincentive.', 'Taxes should aid the redistribution of income.',
              'Tax rates should be consistent with national economic objectives.', 'Should have a stabilising influence on the economy.',
              'Evasion should be impossible']),
     5, 4, 'Five characteristics, ' + H.traced('5 at 4 marks each. State: 2 marks. Explain: 2 marks.') + ' The paper does not say how '
     'many; the scheme credits five.', stem=q4a, **B)
q4b = H.q(5, 'The Irish government introduced a carbon tax in its latest Budget', ' (i)')
add('sb-q4-b-i', '3-1', 'is-the-carbon-tax-regressive', ref('B', 4, '(b)(i)'),
    H.q(5, 'Is this tax an example of a progressive or a regressive tax? Explain your answer.', ' (ii)'), '2 + 3', 5,
    [point('r-answer', H.traced('It is a regressive tax'), 2,
           'Stating it, 2 marks, and explaining it, 3 (the scheme prints ' + H.traced('5 marks: State: 2 marks. Explain: 3 marks') + ').'),
     point('r-why', H.traced('because it does not take into account your ability to pay the tax/ people on lower incomes would pay a '
                             'greater proportion of their income in tax.'), 3, 'Why, 3 marks.')],
    kind='fixed', stem=q4b, **B)
carbon_adv = [cc(x) for x in ('Government revenues', 'Investment in R&D', 'More efficient use of resources', 'Help pay towards our carbon')]
carbon_dis = [cc(x) for x in ('Inflationary pressures', 'Loss of competitiveness', 'Decrease in the standard of living',
                              'Regressive form of taxation')]
add('sb-q4-b-ii', '3-1', 'the-carbon-tax-for-and-against', ref('B', 4, '(b)(ii)'),
    H.q(5, 'State and explain two possible economic advantages and two possible economic disadvantages', ' (25 marks)'),
    '2 @ 5 + 2 @ 5', 20,
    [anyN('r-advantages', 'An advantage — any two', 10, 2, 5, carbon_adv,
          'Two advantages, ' + H.traced('2 at 5 marks each.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks.')),
     anyN('r-disadvantages', 'A disadvantage — any two', 10, 2, 5, carbon_dis, 'Two disadvantages, 5 marks each, the same way.')],
    kind='fixed', stem=q4b, **B)
pick('sb-q4-c', '3-1', 'problems-of-the-national-debt', ref('B', 4, '(c)'),
     H.q(5, 'State and explain four problems associated with the Irish National Debt.', ' (20 marks)'), 'A problem — any four',
     H.split('1. Opportunity costs involved.', '4 points at 5 marks each. State: 2',
             ['Opportunity costs involved.', 'Increased burden on taxpayers.', 'Increased annual interest repayments.',
              'Diminished international credit-rating.', 'Euro stability pact requirements.', 'Poor management of economy.',
              'Risk in Provision of Public Services', 'Servicing the external portion of the National Debt']),
     4, 5, 'Four problems, ' + H.traced('4 points at 5 marks each. State: 2 marks. Explain: 3 marks.'),
     stem=H.q(5, 'At end of December 2008 the Irish National Debt', ' State and explain'), **B)

# Q5 ─ GNP at factor cost and national income; VAT and farm subsidies; national income statistics
q5a = H.q(6, 'Given that Gross National Product at Current Market Prices is €200m', ' (i)')
add('sb-q5-a-i', '3-0', 'gnp-at-factor-cost', ref('B', 5, '(a)(i)'),
    H.q(6, '(i) Gross National Product at Factor Cost;', ' (ii)'), '2 + 2 + 2 + 4', 10,
    [point('r-gnp', f"{H.traced('GNP @ Market Prices')} — {H.traced('€200 million')}", 2, '2 marks, printed under €200 million.'),
     point('r-subsidies', f"{H.traced('+ Price Subsidies')} — {H.traced('€5 million')}", 2, '2 marks, printed under €5 million.'),
     point('r-taxes', f"{H.traced('– Indirect Taxes')} — {H.traced('€30 million')}", 2, '2 marks, printed under €30 million.'),
     point('r-answer', f"{H.traced('= GNP @ Factor Cost')} — {H.traced('€175 million')}", 4,
           '4 marks, printed under €175 million (' + H.traced('Gross National Product at Factor Cost – 10 marks') + ' in all).')],
    kind='fixed', stem=q5a, figure=SOL + 'p20-q5ai-working', **B)
add('sb-q5-a-ii', '3-0', 'national-income-from-gnp', ref('B', 5, '(a)(ii)'),
    H.q(6, '(ii) Net National Product at Factor Cost/National Income.', ' (20 marks)'), '3 + 3 + 4', 10,
    [point('r-gnp', f"{H.traced('GNP @ Factor Cost')} — {H.traced('€175 million*')}", 3,
           '3 marks, printed under €175 million*, the answer to (i).'),
     point('r-depreciation', f"{H.traced('– Depreciation')} — {H.traced('€12 million')}", 3, '3 marks, printed under €12 million.'),
     point('r-answer', f"{H.traced('= NNP @ FC')} — {H.traced('€163 million')}", 4,
           '4 marks, printed under €163 million (' + H.traced('Net National Product at Factor Cost/National Income – 10 marks')
           + ' in all).')],
    kind='fixed', stem=q5a, figure=SOL + 'p20-q5aii-working', **B)
q5b = H.q(6, 'Explain the economic effect which each of the following could have on the level of GNP', ' (i)')
long_run = H.traced('The Long run')
for roman, item, rid, (effect, why), (l_effect, l_why) in (
        ('i', H.q(6, 'a reduction in the general level of VAT;', ' (ii)'), 'vat',
         (cc('Will decrease', whole=True), cc('The reduction in VAT will decrease the prices')),
         (cc('Will increase', whole=True), cc('With lower prices consumers may buy more'))),
        ('ii', H.q(6, 'a reduction in the subsidies paid to farmers.', ' (20 marks)'), 'subsidies',
         (cc('Will increase', whole=True), cc('The reduction in subsidies paid to farmers will increase')),
         (cc('Will decrease', whole=True), cc('Prices will rise and so demand')))):
    concept = 'a-vat-cut-and-gnp' if rid == 'vat' else 'cutting-farm-subsidies-and-gnp'
    add(f'sb-q5-b-{roman}-prices', '3-0', concept, ref('B', 5, f'(b)({roman})', 'the price effect'),
        f'{item} Answer for: the effect on the prices consumers pay in the market place.', '4 + 6', 10,
        [point('r-effect', effect, 4, 'The effect on GNP at market prices, 4 marks. The scheme also prints ' + long_run
               + ', with the opposite effect, as its other reading.'),
         point('r-explanation', why, 6, 'The explanation, 6 marks (' + H.traced('10 mks') + ' in all).')],
        kind='fixed', stem=q5b, **B)
    add(f'sb-q5-b-{roman}-long-run', '3-0', concept, ref('B', 5, f'(b)({roman})', 'the long run'),
        f'{item} Answer for: {long_run}.', '4 + 6', 10,
        [point('r-effect', l_effect, 4, 'The effect on GNP at market prices in ' + long_run + ', 4 marks.'),
         point('r-explanation', l_why, 6, 'The explanation, 6 marks (10 in all).')],
        kind='fixed', stem=q5b, **B)
pick('sb-q5-c-i', '3-0', 'uses-of-national-income-statistics', ref('B', 5, '(c)(i)'),
     H.q(6, 'Outline the main uses of National Income Statistics.', ' (ii)'), 'A use — any three',
     H.split('1. Indication of alterations in our standard of living', '3 points at 5 marks each.\nState',
             ['Indication of alterations in our standard of living', 'Means of comparing the standard of living',
              'Assists the government in formulating economic policy.', 'Evaluate economic policy', 'EU Budget Contributions / Benefits']),
     3, 5, 'Three uses, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks.') + ' The paper does not say how many; '
     'the scheme credits three.', **B)
pick('sb-q5-c-ii', '3-0', 'limits-of-national-income-statistics', ref('B', 5, '(c)(ii)'),
     H.q(6, 'State and explain four reasons why care should be taken when using National Income', ' (35 marks)'),
     'A reason — any four',
     H.split('• Population changes', '4 points at 5 marks each. State: 2',
             ['Population changes', 'Inflation/deflation', 'Employment / Unemployment', 'Levels of taxation', 'Levels of social welfare',
              'Measures flow of wealth not welfare', 'Hidden social costs attached', 'Distribution of national income.',
              'Exclusion of important activities', 'Nature of the goods produced', 'Government services at cost price.']),
     4, 5, 'Four reasons, ' + H.traced('4 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), **B)

# Q6 ─ nationalising the banks; economic aims and their conflicts; monetarism
q6a = H.q(6, 'It has been suggested that the main commercial (retail) banks', ' (i)')
add('sb-q6-a-i', '3-4', 'commercial-banks-and-nationalisation', ref('B', 6, '(a)(i)'),
    H.q(6, 'Explain the underlined terms.', ' (ii)'), '5 + 5', 10,
    [point('r-banks', H.traced('Commercial banks') + ' — ' + H.traced('Institutions which provide deposit / lending services to personal consumers / '
                                                       'business.'), 5, 'Commercial banks, 5 marks.'),
     point('r-nationalisation', H.traced('Nationalisation') + ' — ' + H.traced('Taking an industry or assets into public ownership by a government.'), 5,
           'Nationalisation, 5 marks.')],
    kind='fixed', stem=q6a, **B)
bank_for = [cc(x) for x in ('Stability to economy / investor confidence', 'Availability of credit', 'Rationalisation of banking services',
                            'Employment / consumer protection', 'Development of ethical banking practices',
                            'Continued provision of banking services')]
bank_against = [cc(x) for x in ('Unnecessary state interference', 'Shareholders penalised', 'Increased taxation Taxes may',
                                'Opportunity costs The money', 'Profit motive diminished', 'Financial Cost')]
add('sb-q6-a-ii', '3-4', 'nationalising-the-banks-for-and-against', ref('B', 6, '(a)(ii)'),
    H.q(6, 'Outline two possible economic arguments for and two possible economic arguments against', ' (30 marks)'),
    '2 @ 5 + 2 @ 5', 20,
    [anyN('r-for', 'An argument for — any two', 10, 2, 5, bank_for,
          'Two arguments for, ' + H.traced('2 at 5 marks each.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks.')),
     anyN('r-against', 'An argument against — any two', 10, 2, 5, bank_against, 'Two arguments against, 5 marks each, the same way.')],
    kind='fixed', stem=q6a, **B)
pick('sb-q6-b-i', '3-1', 'the-governments-economic-aims', ref('B', 6, '(b)(i)'),
     H.q(6, 'State and explain what you consider to be the three most important economic aims', ' (ii)'), 'An aim — any three',
     H.split('1. Achieve Full Employment.', '3 at 5 marks each.\nState',
             ['Achieve Full Employment.', 'Achieve moderate economic growth.', 'Control government finances', 'Stability in the banking sector.',
              'Broaden the tax base.', 'Promote balanced regional development.', 'Improve infrastructure.', 'Maintain state services.',
              'Distribution of wealth.']),
     3, 5, 'Three aims, ' + H.traced('3 at 5 marks each. State: 2 marks. Explain: 3 marks.'), **B)
pick('sb-q6-b-ii', '3-1', 'conflicting-economic-aims', ref('B', 6, '(b)(ii)'),
     H.q(6, 'Outline two examples of possible conflicts between government economic aims/objectives.', ' (25 marks)'),
     'A conflict — any two',
     H.split('1. Control of national finances v. full employment.', '2 conflicts at 5 marks each.',
             ['Control of national finances v. full employment.', 'Control of national finances v. Economic growth.',
              'Distribution of wealth v. broadening the tax base.', 'Stability in banking sector v. control of government finances.',
              'Balanced regional development v maintaining state services.', 'Full employment v. price stability.']),
     2, 5, 'Two conflicts, ' + H.traced('2 conflicts at 5 marks each. State: 2 marks. Explain: 3 marks.') + ' The scheme names each '
     'conflict and prints no explanation.', **B)
pick('sb-q6-c', '0-0', 'features-of-monetarism', ref('B', 6, '(c)'),
     H.q(6, 'Outline four features of ‘Monetarism’.', ' (20 marks)'), 'A feature — any four',
     H.split('Monetary policy should be the main instrument', '4 at 5 marks each.\nState',
             ['Monetary policy should be', 'Control of money supply', 'Reduction in inflation increases', 'Laissez faire principles',
              'Supply side policies']),
     4, 5, 'Four features, ' + H.traced('4 at 5 marks each. State: 2 marks. Explain: 3 marks.'),
     stem=H.q(6, 'The economist Milton Friedman was regarded as one of the major thinkers', ' Outline'), **B)

# Q7 ─ trade and competitiveness; developed and developing countries; the IMF or the World Bank
q7a = H.q(7, 'Many believe that export-led growth is the way forward', ' (i)')
pick('sb-q7-a-i', '4-2', 'why-trade-is-essential-for-ireland', ref('B', 7, '(a)(i)'),
     H.q(7, 'Explain why international trade is essential for the Irish economy.', ' (ii)'), 'A reason — any three',
     H.split('1. Greater standard of living / increased wealth.', '3 points at 5 marks each.\nState',
             ['Greater standard of living / increased wealth.', 'Greater choice of commodities', 'More competitive prices of goods and services.',
              'Employment / Investment opportunities.', 'Companies benefit from economies of large scale production',
              'Allows for the sale of surplus', 'More efficient use of scarce world resources.', 'Lack of domestic demand.']),
     3, 5, 'Three reasons, ' + H.traced('3 points at 5 marks each. State: 2 marks each. Explain: 3 marks each.') + ' The paper does not '
     'say how many; the scheme credits three.', stem=q7a, **B)
pick('sb-q7-a-ii', '4-2', 'improving-irish-competitiveness', ref('B', 7, '(a)(ii)'),
     H.q(7, 'Discuss three measures which the Irish government could take to improve the competitiveness', ' (30 marks)'),
     'A measure — any three',
     H.split('1. Reduce the national minimum wage / wage restraint.', '3 at 5 marks each.\nState',
             ['Reduce the national minimum wage / wage restraint.', 'Reduce utility charges.', 'Reduce taxation.', 'Reduce bureaucracy.',
              'Subsidies / grants to firms.', 'Develop the infrastructure.', 'Ease credit availability', 'Fund skills development.']),
     3, 5, 'Three measures, ' + H.traced('3 at 5 marks each. State: 2 marks. Explain: 3 marks.'), stem=q7a, **B)
pick('sb-q7-b-i', '4-0', 'developed-and-developing-countries', ref('B', 7, '(b)(i)'),
     H.q(7, 'Describe the main differences between a developed country and a developing country', ' (ii)'), 'A difference — any three',
     H.split('High population growth rates in less developed countries', '3 at 5 marks each. State: 2 marks.',
             ['High population growth rates', 'Famine in LDCs.', 'High foreign debts.', 'More uneven distribution of wealth in LDCs',
              'Over-dependence on one crop in LDCs.', 'High percentage of the population engaged', 'Unfavourable Terms of Trade for LDCs.',
              'Poor infrastructure in LDCs.', 'Lack of capital / Low levels of investment in LDCs.', 'Low per capita incomes in LDCs.',
              'Poor levels of education/literacy in LDCs.', 'Political corruption / less stable political institutions.',
              'Exploitation by multinationals of LDCs.']),
     3, 5, 'Three differences, ' + H.traced('3 at 5 marks each. State: 2 marks. Explain: 3 marks.') + ' The paper does not say how many; '
     'the scheme credits three.', **B)
pick('sb-q7-b-ii', '4-0', 'promoting-development-in-ldcs', ref('B', 7, '(b)(ii)'),
     H.q(7, 'Discuss three measures which the governments of developed countries could take', ' (30 marks)'), 'A measure — any three',
     H.split('1. Assist foreign aid programmes / capital provision.', '3 at 5 marks each.\nState',
             ['Assist foreign aid programmes / capital provision.', 'Restructure their national debts.', 'Improve trading opportunities.',
              'Encourage multinationals to set up firms there.', 'Assist LDCs with skills / technologies.',
              'Assist peace measures and promote political stability.']),
     3, 5, 'Three measures, ' + H.traced('3 at 5 marks each. State: 2 marks. Explain: 3 marks.'), **B)
q7c = H.q(7, 'Write a brief account on the role of the International Monetary Fund (IMF)', ' (15 marks)')
imf = H.split('Expansion of World Trade\nThe IMF', 'The World Bank\nEncourage',
              ['Expansion of World Trade', 'Promote exchange rate stability.', 'Orderly correction of balance of payments problems.',
               'Operation of a multilateral system of payments.', 'Provision of technical assistance and training.'])
world_bank = H.split('Encourage investment funds to LDCs', '3 points at 5 marks each. State: 2',
                     ['Encourage investment funds to LDCs', 'Finance capital projects in member countries.', 'Debt relief for LDCs'])
for word, name, opts in (('imf', 'The International Monetary Fund', imf), ('world-bank', 'The World Bank', world_bank)):
    pick(f'sb-q7-c-{word}', '4-1', 'the-imf-or-the-world-bank', ref('B', 7, '(c)', 'the IMF' if word == 'imf' else 'the World Bank'),
         f'{q7c} Answer for: {H.traced(name)}.', 'A role — any three', opts, 3, 5,
         'Three roles, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks.') + ' The scheme credits the IMF and the '
         'World Bank, each with its own list.', **B)

# Q8 ─ the economy's performance; an ageing population and emigration; savings
areas = (('Price levels', 'Price levels continue to fall', '\nEconomic growth'),
         ('Economic growth', 'Gross domestic product (GDP) shrank', '\nGovernment current budgetary position'),
         ('Government current budgetary position', 'Because of deteriorating government finances', '\nEmployment / unemployment'),
         ('Employment / unemployment', 'The number of people signing on', '7 marks + 6 marks'))
performance = [o for area, start, end in areas for o in side(area, H.bullets(start, end))]
add('sb-q8-a', '3-5', 'how-the-economy-performed', ref('B', 8, '(a)(i)–(iv)'),
    H.q(7, 'Outline, using appropriate figures, how the Irish economy has performed', ' (25 marks)'), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'One for each area', 25, 4, 7, performance,
          'All four areas, price levels, economic growth, the government’s current budgetary position and employment, one '
          'point for each, on one ladder: ' + H.traced('7 marks + 6 marks + 6 marks + 6 marks= 25 marks.') + ' The scheme does not say '
          'which area earns the 7, so the first correct area is claimed at 7 and the other three at 6. Its points are the '
          'figures of the year to mid-2010.', steps=[7, 6, 6, 6])],
    kind='fixed', **B)
pick('sb-q8-b-i', '3-5', 'effects-of-an-ageing-population', ref('B', 8, '(b)(i)'),
     H.q(7, 'Outline two possible economic effects of an ageing population on the Irish economy.', ' The number'), 'An effect — any two',
     H.split('1. Pressure on provision of state pensions', '2 at 5 marks.',
             ['Pressure on provision of state pensions:', 'Possible increased tax burden:', 'Increased government expenditure:',
              'Changing pattern of demand:', 'The participation rate falls:', 'Reduced mobility of labour:']),
     2, 5, 'Two effects, ' + H.traced('2 at 5 marks.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks.'),
     stem=H.q(7, 'By 2036 one in five Irish people will be over 65 years of age', ' (i)'), **B)
pick('sb-q8-b-ii', '3-2', 'consequences-of-rising-emigration', ref('B', 8, '(b)(ii)'),
     H.q(7, 'State and explain three economic consequences of the recent increase in emigration.', ' (25 marks)'),
     'A consequence — any three',
     H.split('1. Higher dependency ratio.', '3 points at 5 marks each.\nState',
             ['Higher dependency ratio.', 'Opportunity costs.', 'Loss of skills within the economy', 'Smaller domestic market',
              'Upward pressure on Irish wage levels.', 'Demand for state services.', 'Unemployment reduced.', 'Contacts.']),
     3, 5, 'Three consequences, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks') + '.',
     stem=H.q(7, 'The number of emigrants from Ireland, in the year to April 2009', ' (ii)'), **B)
q8c = H.q(7, 'There has been a sharp increase in the rate of savings in Ireland in the past year.', ' (i)')
pick('sb-q8-c-i', '3-4', 'what-drives-savings-now', ref('B', 8, '(c)(i)'),
     H.q(7, 'Discuss two factors currently influencing the rate of savings in the Irish economy.', ' (ii)'), 'A factor — any two',
     H.split('Future Expectations for the economy', '2 points at 5 marks each.',
             ['Future Expectations for the economy', 'Security of savings', 'Price levels / real rate of interest',
              'Quality of financial products', 'Deferred spending', 'Future Levels of state benefits']),
     2, 5, 'Two factors, ' + H.traced('2 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), stem=q8c, **B)
pick('sb-q8-c-ii', '3-4', 'effects-of-higher-savings', ref('B', 8, '(c)(ii)'),
     H.q(7, 'Outline three economic effects which an increase in the rate of savings may have', ' (25 marks)'), 'An effect — any three',
     H.split('Reduced spending within the economy / leakage', '3 points at 5 marks each. State: 2',
             ['Reduced spending within the economy', 'Increase in unemployment.', 'More funds available for investment.',
              'Reduced inflation.', 'Reduced demand for imports.', 'Increased revenue for government.', 'Stabilise banking sector.']),
     3, 5, 'Three effects, ' + H.traced('3 points at 5 marks each. State: 2 marks. Explain: 3 marks.'), stem=q8c, **B)

# A short ask the paper prints for several parts would read the same on every card, and the
# deck refuses two cards asking one question: each carries its stem in its question instead,
# as 2012 OL and 2013 OL do.
_asked = [' '.join(c['questionText'].split()).lower() for c in cards]
for c in cards:
    if _asked.count(' '.join(c['questionText'].split()).lower()) > 1 and c.get('stem'):
        c['questionText'], c['stem'] = f"{c['stem']} {c['questionText']}", ''

if __name__ == '__main__':
    emit(cards)
