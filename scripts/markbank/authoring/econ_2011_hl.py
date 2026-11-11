#!/usr/bin/env python3
"""Economics 2011 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2011-hl-ev.json, made
from a visual sweep of all 8 paper pages and 40 scheme pages before any 2011
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The scheme reprints each question above its answer, so a
slice always starts after the reprinted wording. A stem stops before any
printed table: the table is the crop beside the typed ask. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.

This scheme prints its short-question tariffs as a total with its parts in
brackets ("17 marks (10+5+2)"). Over a list of responses that is a ladder,
claimed in the order the answers are correct; over printed parts of different
kinds it is read in the order the parts are printed, and the card's note says
so.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2011, 'higher', 'LC034ALP000EV')
D = OldDeck(2011, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2011-HL-scheme-'
PAP = 'economics-2011-HL-paper-'
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
CELLS = [ln.strip() for ln in H.full_md.split('<!-- markbank:table-cells -->', 1)[1]
         .split('<!-- /markbank:table-cells -->', 1)[0].splitlines()]


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def pair(first):
    """A two-column row: a cell and the cell printed after it."""
    i = CELLS.index(first)
    return f'{H.traced(first)} — {H.traced(CELLS[i + 1])}'


def unnum(text):
    """A response read without the scheme's own list numeral ("1. ")."""
    return H.traced(re.sub(r'^\d\.\s*', '', text))


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ constructing the CPI
add('sa-q1', '3-3', 'constructing-the-cpi', ref('A', 1),
    H.q(2, 'State four steps involved in constructing a Consumer Price Index (CPI).', ' Step 1'), '4 @ 4', 16,
    [anyN('r-1', 'A step — any four', 16, 4, 4,
          [H.traced(re.sub(r'^Step \d:\s*', '', x)) for x in H.split('Step 1: Determine the commodities', '4 points x 4 marks each',
                                                                     ['Step 1:', 'Step 2:', 'Step 3:', 'Step 4:', 'Step 5:'])],
          'Four steps, ' + H.traced('4 points x 4 marks each = 16 marks') + '.')],
    kind='fixed', **A)

# Q2 ─ a mixed economy
add('sa-q2', '1-0', 'ireland-as-a-mixed-economy', ref('A', 2),
    H.q(2, 'Define a mixed economy.', ' Definition:'), '12 + 2 @ 2', 16,
    [point('r-definition', H.opt('An economy that incorporates elements of both central planning', '\nTwo Examples:'), 12,
           'The definition, 12 marks: the scheme prints ' + H.traced('16 marks (12+4)') + ' beneath its definition and its examples, '
           'read here in that order, the definition 12 and the two examples 4 between them (2014 HL prices an explanation 12 '
           'and its example 4 the same way).'),
     anyN('r-examples', 'An example — any two', 4, 2, 2,
          H.split('1. Existence of Social Partnership', '16 marks (12+4)',
                  ['Existence of Social Partnership', 'Existence of semi-state bodies', 'Government Departments / Regulators',
                   'Legislation passed by Government', 'Use of taxation / government expenditure']),
          'Two examples, the 4 marks shared between them, 2 each.')],
    kind='fixed', **A)

# Q3 ─ which market structure
structures = (('The firm has a perfectly elastic demand curve.', 'Perfect Competition'),
              ('The product of the firm is unique.', 'Monopoly'),
              ('Restaurants could be an example of this market structure.', 'Imperfect Competition'),
              ('Average costs of the firm are at a minimum.', 'Perfect Competition'))
add('sa-q3', '2-0', 'which-market-structure', ref('A', 3, '(i)–(iv)'),
    # The four statements follow the ask, from the paper's own table rows.
    f"{H.q(2, 'Name the market structure (Perfect Competition, Imperfect Competition or Monopoly)', ' STATEMENT')} "
    f"{H.q(2, '(i) The firm has a perfectly elastic demand curve.', ' (16 marks)')}", '4 @ 4', 16,
    [point(f'r-{n}', f'{H.traced(s)} — {H.traced(m)}', 4, f'Statement ({n}), 4 marks: '
           + H.traced('4 correct responses x 4 marks each = 16 marks') + '.')
     for n, (s, m) in zip(('i', 'ii', 'iii', 'iv'), structures)],
    kind='fixed', **A)

# Q4 ─ the NTMA
add('sa-q4', '3-1', 'what-the-ntma-does', ref('A', 4),
    H.q(2, 'Outline three areas of responsibility of the National Treasury Management Agency', ' (i)'), '10 + 4 + 2', 16,
    [anyN('r-1', 'An area of responsibility — any three', 16, 3, 10,
          [unnum(x) for x in H.split('1. Borrowing on behalf of the Irish Government', '16 marks (10+4+2)',
                                     ['1. Borrowing on behalf of the Irish', '2. Managing the Irish National Debt', '3. Managing the National Pension',
                                      '4. Managing other government funds', '5. Borrowing on behalf of the Housing', '6. Providing financial advice',
                                      '7. Providing a Central Treasury Service', '8. Personal injuries claims', '9. Acting as Ireland’s agent'])],
          'Three areas: ' + H.traced('16 marks (10+4+2)') + ', the first correct 10, the 2nd 4 and the 3rd 2.', steps=[10, 4, 2])],
    kind='fixed', **A)

# Q5 ─ occupational mobility of labour
add('sa-q5', '2-1', 'occupational-mobility-of-labour', ref('A', 5),
    H.q(2, 'Define the term occupational mobility of labour.', ' Definition:'), '12 + 2 @ 2', 16,
    [point('r-definition', H.traced('the ability/ease of a worker to move from one job to another.'), 12,
           'The definition, 12 marks: the scheme prints ' + H.traced('16 marks (12+4)') + ' beneath its definition and its factors, '
           'read here in that order, the definition 12 and the two factors 4 between them.'),
     anyN('r-factors', 'A factor — any two', 4, 2, 2,
          [unnum(x) for x in H.split('1. Availability and access to affordable', '16 marks (12+4)',
                                     ['1. Availability and access to affordable', '2. Availability and access to training',
                                      '3. Government policies which aid', '4. Reduced barriers for entry'])],
          'Two factors, the 4 marks shared between them, 2 each.')],
    kind='fixed', **A)

# Q6 ─ a falling euro
add('sa-q6', '4-2', 'a-falling-euro-against-the-dollar', ref('A', 6),
    H.q(3, 'Outline two possible economic effects for the Irish economy of the euro', ' (i)'), '9 + 8', 17,
    [anyN('r-1', 'An effect — any two', 17, 2, 9,
          H.split('1. Import prices (from US) dearer', '17 marks (9 + 8 )',
                  ['Import prices (from US) dearer', 'Export prices (to US) cheaper', 'Employment opportunities',
                   'Economic growth may increase', 'US Investment in Ireland']),
          'Two effects: ' + H.traced('17 marks (9 + 8 )') + ', the first correct 9 and the 2nd 8.', steps=[9, 8])],
    kind='fixed', **A)

# Q7 ─ multinationals moving to Southeast Asia
add('sa-q7', '4-1', 'why-multinationals-move-to-southeast-asia', ref('A', 7),
    H.q(3, 'State three reasons why multinational firms are re-locating', ' (i)'), '10 + 5 + 2', 17,
    [anyN('r-1', 'A reason — any three', 17, 3, 10,
          [unnum(x) for x in H.split('1. Lower wage costs:', '17 marks (10+5+2)',
                                     ['1. Lower wage costs:', '2. Lower costs of production:', '3. Less restrictive regulatory',
                                      '4. Emerging economies', '5. Development in communications'])],
          'Three reasons: ' + H.traced('17 marks (10+5+2)') + ', the first correct 10, the 2nd 5 and the 3rd 2.', steps=[10, 5, 2])],
    kind='fixed', **A)

# Q8 ─ cross elasticity
q8 = H.q(3, 'A consumer buys 20 units of Good A when the price of Good B is €8.', ' Using an appropriate')
add('sa-q8', '1-4', 'cross-elasticity-of-good-a', ref('A', 8),
    H.q(3, 'Using an appropriate formula, calculate this consumer’s cross elasticity', ' Answer:') + ' '
    + H.q(3, 'Is Good A a substitute for, or a complement to, Good B? Explain you answer.', ' _'), '8 + 5 + 2 + 2', 17,
    [ask_row('r-working', 'Using an appropriate formula', 8,
             'The formula and working, 8 marks: the scheme prints ' + H.traced('17 marks (8+5+2+2)') + ' beneath its formula and '
             'working, its answer, “Complement” and its reason, read here in that order. The working is shown with the answer: the '
             'change in A (-8) over the change in B’s price (€2), times (€8 + €10) over (20 + 12).'),
     point('r-answer', H.traced('= - 2.25'), 5, 'The answer, 5 marks.'),
     point('r-complement', H.traced('Good A is a Complement.'), 2, 'A complement, 2 marks.'),
     point('r-why', H.traced('It has a negative CED.'), 2, 'Why, 2 marks.')],
    kind='fixed', stem=q8, figure=SOL + 'p08-q8-working', **A)

# Q9 ─ mortgage arrears
reasons = [unnum(x) for x in H.split('1. Increased interest rates', 'Two actions:',
                                     ['1. Increased interest rates', '2. Increased unemployment:', '3. Economic recession:',
                                      '4. Reckless lending/ borrowing:'])]
actions = [unnum(x) for x in H.split('1. Re-schedule the loan contract:', '17 marks (5+4+4+4)',
                                     ['1. Re-schedule the loan contract:', '2. Interest only payments:', '3. No penalty payments',
                                      '4. Debt / equity swaps:', '5. Debt forgiveness', '6. Re-value properties'])]
add('sa-q9', '3-4', 'mortgage-arrears', ref('A', 9),
    H.q(3, 'Outline two economic reasons for this development and two actions', ' Reasons:'), '5 + 4 + 4 + 4', 17,
    [anyN('r-1', 'Two reasons and two actions', 17, 4, 5, side('Two reasons', reasons) + side('Two actions', actions),
          'Two reasons and two actions, on one ladder: ' + H.traced('17 marks (5+4+4+4)') + ', the first correct answer 5 and the '
          'next three 4 each.', steps=[5, 4, 4, 4])],
    kind='fixed', stem=H.q(3, 'In September 2010 approximately 5.1% of mortgage accounts', ' Outline two'), **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ individual and market demand; shifts; utility
add('sb-q1-a-i', '1-1', 'individual-and-market-demand', ref('B', 1, '(a)(i)'),
    H.q(4, 'Define the economic terms: individual (consumer) demand; market demand.', ' (ii)'), '6', 6,
    [point('r-individual', 'Individual demand — ' + H.traced('the quantity of a good an individual consumer demands at different prices.'),
           None, 'Individual demand.'),
     point('r-market', 'Market demand — ' + H.traced('total quantity of a good that all consumers demand at different prices.'), None,
           'Market demand. Claim the complete answer: the scheme prices the two definitions ' + H.traced('6 marks')
           + ' together, without dividing them.')],
    kind='questionTotal', **B)
q1aii = H.q(4, 'Explain, with the aid of labelled diagrams, the relationship between individual', ' (20)')
add('sb-q1-a-ii', '1-1', 'adding-up-to-market-demand', ref('B', 1, '(a)(ii)'), q1aii, '3 + 3 + 5 + 3', 14,
    [anyN('r-consumers', 'Each consumer’s diagram — each element', 6, 6, 1,
          side('Consumer A', [H.traced(x) for x in ('Graduated P axis', 'Graduated Q axis', 'labelled D/C')])
          + side('Consumer B', [H.traced(x) for x in ('Graduated P axis', 'Graduated Q axis', 'labelled D/C')]),
          H.traced('2 diagrams x 3 marks each: Graduated P axis; Graduated Q axis; labelled D/C (1 mark each)')
          + '. The completed diagrams are shown with the answer.'),
     anyN('r-market-axes', 'The market diagram — each axis', 2, 2, 1, [H.traced(x) for x in ('Graduated P axis', 'Graduated Q axis')],
          'The market diagram’s two axes, 1 mark each, of its ' + H.traced('Market diagram: 5 marks') + '.'),
     point('r-market-dc', H.traced('Correct cumulative D/C'), 3, 'The market diagram’s demand curve, 3 marks.'),
     point('r-explanation', H.opt('To derive the market demand add the quantity demanded', '\n3 marks'), 3, 'The explanation, 3 marks.')],
    kind='fixed', figure=SOL + 'p09-q1aii-diagrams', **B)
add('sb-q1-b-i', '1-1', 'movement-along-or-shift-in-demand', ref('B', 1, '(b)(i)'),
    H.q(4, 'Distinguish between the economic meanings of a ‘movement along a demand curve’', ' (ii)'), '8 + 8', 16,
    [point('r-movement', 'Movement along a demand curve — ' + H.opt('Caused by a change in the selling price of the good itself', '\nDiagram:'), 8,
           'A movement along, 8 marks, with its diagram (shown with the answer): the scheme does not divide the 8.'),
     point('r-shift', 'Shift in a demand curve — ' + H.opt('If any of the factors other than the price of the good itself change', '\nP\nD/C2'), 8,
           'A shift, 8 marks, with its diagram: the scheme does not divide the 8.')],
    kind='fixed', figure=SOL + 'p10-q1bi-diagrams', **B)
pick('sb-q1-b-ii', '1-1', 'what-shifts-demand-for-concert-tickets', ref('B', 1, '(b)(ii)'),
     H.q(4, 'State and explain two factors that would cause a shift in a demand curve', ' (30)'), 'A factor — any two',
     [pair(x) for x in ('Income levels', 'Taste / Preference', 'Expectations about the future', 'Unplanned events',
                        'Change in price of substitute good', 'Change in price of complementary good')],
     2, 7, 'Two factors, ' + H.traced('2 x 7 marks each') + ': each with how it shifts the curve.', **B)
q1c = H.q(4, 'The Law of Diminishing Marginal Utility states that as more of a product is consumed', ' (i)')
pick('sb-q1-c-i', '1-1', 'assumptions-of-diminishing-marginal-utility', ref('B', 1, '(c)(i)'),
     H.q(4, 'Explain two assumptions underlying the Law of Diminishing Marginal Utility.', ' A consumer'), 'An assumption — any two',
     H.split('1. Applies after a certain point called the origin.', '2 x 6 marks each',
             ['Applies after a certain point called the origin.', 'It does not apply to Addictive goods.',
              'Time lapse between consumption of successive units.', '‘Other factors’ affecting utility do not change.']),
     2, 6, 'Two assumptions, ' + H.traced('2 x 6 marks each') + '.', stem=q1c, **B)
add('sb-q1-c-ii', '1-1', 'the-equi-marginal-principle-at-work', ref('B', 1, '(c)(ii)'),
    H.q(4, 'Using the Equi-Marginal Principle of Consumer Behaviour calculate', ' (25)'), '9 + 4', 13,
    [ask_row('r-working', 'Using the Equi-Marginal Principle of Consumer Behaviour', 9,
             'The working, 9 marks: the scheme prints ' + H.traced('13 marks (9+4)') + ' beneath its working and its answer, read here '
             'in that order. The working is shown with the answer: 40 over 80 equals X over 150.'),
     point('r-answer', H.traced('= 75 utils'), 4, 'The answer, 4 marks.')],
    kind='fixed', stem=f"{q1c} {H.q(4, 'A consumer in equilibrium buys 6 health bars', ' (ii)')}",
    figure=SOL + 'p11-q1cii-working', **B)

# Q2 ─ oligopoly; the kinked demand curve; price and non-price competition
q2a = H.q(4, 'Some Telecoms’ analysts believe the main mobile operators in Ireland', ' (i)')
pick('sb-q2-a-i', '2-0', 'features-of-oligopoly', ref('B', 2, '(a)(i)'),
     H.q(4, 'Outline three key features of an oligopolistic market.', ' Firms in'), 'A feature — any three',
     H.split('1. Few Sellers in the industry.', '3 features x 5 marks each',
             ['Few Sellers in the industry.', 'Interdependence between firms.', 'Product Differentiation occurs.', 'Barriers to entry.',
              'Collusion may occur.', 'Non-price competition is more common than price competition.']),
     3, 5, 'Three features, ' + H.traced('3 features x 5 marks each') + '.', stem=q2a, **B)
pick('sb-q2-a-ii', '2-0', 'objectives-other-than-profit', ref('B', 2, '(a)(ii)'),
     H.q(4, 'Outline two objectives firms in oligopoly may have', ' (25)'), 'An objective — any two',
     H.split('1. Prevent government market intervention/interference', '2 x 5 marks each',
             ['Prevent government market intervention/interference', 'Discourage the entry of new firms into the industry',
              'Maximisation of sales / increased share of market', 'Maintain adequate profits.']),
     2, 5, 'Two objectives, ' + H.traced('2 x 5 marks each') + '.',
     stem=f"{q2a} {H.q(4, 'Firms in an oligopolistic market may have objectives other than profit maximisation.', ' (ii)')}", **B)
kinked = [H.traced(x) for x in ('Price axis', 'Quantity axis', 'Kinked D/C', 'Distinct MR curve', 'MC', 'AC', 'P1', 'Q1', 'Point G')]
equilibrium = [unnum(x) for x in (
    H.traced('1. Equilibrium occurs at point G where (a) MC = MR & (b) MC is rising.'),
    H.traced('2. The firm will produce Q1 and sell this output at price P1'),
    H.traced('3. The firm’s cost of production is shown at point G.'),
    H.traced('4. Should costs rise between points D and E then market price tends to remain constant at P1.'),
    H.traced('5. This firm is earning SNPs because AR exceeds AC or barriers to entry exist.'))]
add('sb-q2-b', '2-0', 'the-kinked-demand-curve', ref('B', 2, '(b)(i)–(ii)'),
    ' '.join([H.q(4, 'Using one clearly labelled diagram:', ' (i)'), H.q(4, '(i) Explain the shape of the ‘kinked’ demand curve', ' (25)')]),
    '9 + 8 + 8', 25,
    [anyN('r-diagram', 'The diagram — each element', 9, 9, 1, kinked,
          'The diagram, ' + H.traced('9 marks') + ' for the nine elements the scheme lists beside it, 1 each. The completed '
          'diagram is shown with the answer.'),
     point('r-shape', ' — '.join([H.traced('Demand curve - AB'), H.opt('If this firm increases its price others will leave', '\nDemand curve'),
                                  H.traced('Demand curve – BC'), H.opt('If this firm lowers its price others will match', '\n(ii)')]), 8,
           '(i) The shape of the demand curve, ' + H.traced('8 marks') + ': AB elastic and BC inelastic, which the scheme does not divide.'),
     point('r-equilibrium', ' — '.join(equilibrium), 8,
           '(ii) The long run equilibrium, ' + H.traced('8 marks') + ': the scheme lists five points and does not divide the 8.')],
    kind='fixed', figure=SOL + 'p14-q2b-diagram', **B)
q2c = H.q(4, 'It is suggested that consumers prefer price competition in the market place', ' (i)')
prefer = H.split('1. Lower prices / value for money', '(ii) Benefits of non-price competition.',
                 ['Lower prices / value for money', 'Higher disposable income', 'More choice', 'Preferable to non-price competitive'])
benefits = H.split('1. Consumer loyalty rewarded', '25 marks (7+6+6+6)',
                   ['Consumer loyalty rewarded', 'Stability in prices', 'Better quality commodities / services',
                    'Allows consumers to save', 'More informed consumers'])
add('sb-q2-c', '2-0', 'price-and-non-price-competition', ref('B', 2, '(c)(i)–(ii)'),
    ' '.join([H.q(4, '(i) Explain two reasons why consumers may prefer price competition.', ' (ii)'),
              H.q(4, '(ii) Describe two benefits to consumers of non-price competition.', ' (25)')]), '7 + 6 + 6 + 6', 25,
    [anyN('r-1', 'Two reasons and two benefits', 25, 4, 7,
          side('Reasons why consumers may prefer price competition', prefer) + side('Benefits of non-price competition', benefits),
          'Two reasons for (i) and two benefits for (ii), on one ladder: ' + H.traced('25 marks (7+6+6+6)') + ', the first correct '
          'answer 7 and the next three 6 each.', steps=[7, 6, 6, 6])],
    kind='fixed', stem=q2c, **B)

# Q3 ─ MRP; investment; public transport
add('sb-q3-a-i', '2-1', 'marginal-revenue-productivity', ref('B', 3, '(a)(i)'),
    H.q(5, 'Define the term Marginal Revenue Productivity (MRP) of a factor of production.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('The extra revenue earned when an additional unit of a factor of production is employed.'), 5,
           'The definition, 5 marks.')], **B)
pick('sb-q3-a-ii', '2-1', 'what-influences-mrp', ref('B', 3, '(a)(ii)'),
     H.q(5, 'State and explain two factors that can influence MRP.', ' (iii)'), 'A factor — any two',
     H.split('1. The productivity/ commitment of the factor.', '2 points x 5 marks each',
             ['The productivity/ commitment of the factor.', 'The selling price of the output.', 'The Law of Demand.',
              'Quality / Specialised nature', 'Training/Education provided', 'Expertise of the entrepreneur.',
              'Law of Diminishing Marginal Returns.']),
     2, 5, 'Two factors, ' + H.traced('2 points x 5 marks each') + '.', **B)
pick('sb-q3-a-iii', '2-1', 'measuring-mrp', ref('B', 3, '(a)(iii)'),
     H.q(5, 'Outline two difficulties that may arise in measuring MRP.', ' (25)'), 'A difficulty — any two',
     H.split('1. Not all factors produce physical output.', '2 points x 5 marks each',
             ['Not all factors produce physical output.', 'Output not sold in the market place.',
              'Combination of capital and labour']),
     2, 5, 'Two difficulties, ' + H.traced('2 points x 5 marks each') + '.', **B)
q3b = H.q(5, '‘Capital Investment has been an important driver', ' (i)')
pick('sb-q3-b-i', '3-5', 'why-investment-matters', ref('B', 3, '(b)(i)'),
     H.q(5, 'State and explain three reasons why investment is important for the Irish economy.', ' (ii)'), 'A reason — any three',
     H.split('1. Increased productive capacity', '3 points x 5 marks each',
             ['Increased productive capacity', 'Increased labour productivity', 'Increased employment', 'Increased GNP',
              'Investment generates future wealth', 'Increased Government Revenues']),
     3, 5, 'Three reasons, ' + H.traced('3 points x 5 marks each') + '.', stem=q3b, **B)
pick('sb-q3-b-ii', '3-5', 'what-drives-investment-now', ref('B', 3, '(b)(ii)'),
     H.q(5, 'Describe three factors that currently influence the level of investment', ' (30)'), 'A factor — any three',
     H.split('1. Rates of interest / Cost of borrowing', '3 points x 5 marks each',
             ['Rates of interest / Cost of borrowing', 'Business people\'s expectations', 'Government economic policies',
              'The international economic climate', 'The Marginal Efficiency of Capital', 'Stability in the banking sector',
              'The cost of capital goods', 'Availability of a skilled English speaking workforce']),
     3, 5, 'Three factors, ' + H.traced('3 points x 5 marks each') + '.', stem=q3b, **B)
transport_adv = [cc(x) for x in ('Better use of scarce resources', 'Improved public infrastructure/Regional')] + [
    H.bo('Reduced CO2 emissions / Environment better protected', ' Loss of taxation revenues')] + [cc(x) for x in (
                                 'Reduced traffic congestion', 'Reduced imports', 'Increased employment If demand',
                                 'Benefits to transport providers')]
transport_dis = [cc(x) for x in ('Investment may be costlier', 'People in rural areas disadvantaged', 'Loss of taxation revenues',
                                 'Subsidies from the state', 'Behaviour of roads users unchanged', 'May argue the opposite',
                                 'Costs of not investing in roads')]
add('sb-q3-c', '2-2', 'public-transport-or-new-roads', ref('B', 3, '(c)'),
    H.q(5, 'Advise the Minister for Transport on two possible economic advantages', ' (20)'), '2 @ 5 + 2 @ 5', 20,
    [anyN('r-advantages', 'An advantage — any two', 10, 2, 5, transport_adv, 'Two advantages, ' + H.traced('2 x 5 marks') + '.'),
     anyN('r-disadvantages', 'A disadvantage — any two', 10, 2, 5, transport_dis,
          'Two disadvantages, 5 marks each. “May argue the opposite of this point” sits beside the advantage of increased employment.')],
    kind='fixed', **B)

# Q4 ─ costs; falling costs; the BP oil spill
q4 = H.q(5, 'The table below shows the short run production costs', ' Number of units')
q4_table = PAP + 'p05-q4-table'
add('sb-q4-a-i', '1-5', 'marginal-cost-average-cost-and-profit', ref('B', 4, '(a)(i)'),
    H.q(5, 'Using the information in the table above calculate the following:', ' (ii)'), '12', 12,
    [point('r-mc', H.traced('€3,300 – €2,250 = €1,050'), None, 'The marginal cost of the 4th unit.'),
     point('r-ac', H.traced('€900'), None, 'The average cost of 5 units: €4,500 over 5.'),
     point('r-profit', H.traced('5 x €1,200 (€6,000) – €4,500 = €1,500'), None,
           'The profit. Claim the complete answer: the scheme prices the three calculations ' + H.traced('12 marks')
           + ' together, without dividing them. The working is shown with the answer.')],
    kind='questionTotal', stem=q4, figure=SOL + 'p20-q4ai-working', **B)
beside_ask(cards[-1], q4_table)
q4aii = H.q(5, 'Using the information in the table above, draw the firm’s short run average cost', ' (30)')
add('sb-q4-a-ii', '1-5', 'the-short-run-average-cost-curve', ref('B', 4, '(a)(ii)'), q4aii, '12 + 6', 18,
    [ask_row('r-diagram', 'draw the firm’s short run average cost (AC) curve', 12,
             'The diagram, ' + H.traced('12 marks') + ': the AC curve plotted from the table, falling to its lowest point at 3 '
             'units and rising after, as the figure shows.'),
     point('r-explanation', ' — '.join([H.traced('Slopes downward:'), H.traced('Declining FC per unit / FC spread over a larger number of units of output'),
                                        H.traced('Specialisation of labour: helps reduce cost per unit'), H.traced('Slopes upward:'),
                                        H.traced('Increasing VC per unit because of the Law of Diminishing Marginal returns')]), 6,
           'The explanation, ' + H.traced('6 marks') + ': why it slopes down (either reason) and why it slopes up, which '
           'the scheme does not divide.')],
    kind='fixed', stem=q4, figure=SOL + 'p20-q4aii-diagram', **B)
beside_ask(cards[-1], q4_table)
q4b = H.q(5, '‘The cost of doing business in Ireland is falling.', ' (i)')
pick('sb-q4-b-i', '4-2', 'falling-costs-and-the-irish-economy', ref('B', 4, '(b)(i)'),
     H.q(5, 'Discuss the economic advantages of falling costs of production for the Irish economy.', ' (ii)'), 'An advantage — any three',
     H.split('1. Increased competitiveness', '3 points x 5 marks each',
             ['Increased competitiveness', 'Lower prices', 'Increased demand', 'Increased employment',
              'Attract investment / Improve international reputation', 'Profits may increase']),
     3, 5, 'Three advantages, ' + H.traced('3 points x 5 marks each') + '.', stem=q4b, **B)
pick('sb-q4-b-ii', '1-2', 'what-holds-irish-businesses-back', ref('B', 4, '(b)(ii)'),
     H.q(5, 'Outline possible restrictions on the growth of businesses in the Irish economy at present.', ' (30)'),
     'A restriction — any three',
     H.split('1. Limited availability of credit', '3 points x 5 marks each',
             ['Limited availability of credit', 'Reduction in domestic demand', 'Restrictive wage agreements',
              'Legislative requirements / framework', 'Merger / takeover legislation', 'High costs of production.']),
     3, 5, 'Three restrictions, ' + H.traced('3 points x 5 marks each') + '.', stem=q4b, **B)
private = [cc(x) for x in ('Cost of repairing the defective oil rig', 'Clean-up costs', 'Compensation costs',
                           'Reduction in share price / asset value', 'Reduction in profits', 'Lost oil', 'Reputational damage',
                           'Fines by government')]
social = [cc(x) for x in ('Environmental damage', 'Cost of investigation / clean-up', 'Disruption to local communities / tourism',
                          'Damage to food chain', 'Higher oil prices')]
add('sb-q4-c', '2-2', 'the-costs-of-the-bp-oil-spill', ref('B', 4, '(c)'),
    H.q(5, 'Identify two costs for BP and two costs to society associated with this oil spill.', ' (15)'), '4 + 4 + 4 + 3', 15,
    [anyN('r-1', 'Two costs for BP and two costs to society', 15, 4, 4,
          side('Costs for BP – Private costs', private) + side('Costs to society – Social costs', social),
          'Two private and two social costs, on one ladder: ' + H.traced('15 marks (4+4+4+3)') + ', the first three correct 4 each and '
          'the 4th 3.', steps=[4, 4, 4, 3])],
    kind='fixed', stem=H.q(5, 'The British Petroleum (BP) oil spill in the Gulf of Mexico', ' Identify'), **B)

# Q5 ─ fiscal policy; privatisation; the public sector wage bill
q5a = H.q(6, 'The Budget is a statement of the Government’s fiscal policy.', ' (i)')
add('sb-q5-a-i', '3-1', 'fiscal-policy', ref('B', 5, '(a)(i)'), H.q(6, 'Explain the underlined term.', ' (ii)'), '10', 10,
    [point('r-1', H.opt('Any action taken by the government which influences the timing', '\n10 marks'), 10,
           'Fiscal policy, 10 marks.')], stem=q5a, **B)
pick('sb-q5-a-ii', '3-1', 'effects-of-cutting-the-deficit', ref('B', 5, '(a)(ii)'),
     H.q(6, 'State and explain four possible economic effects on the Irish economy', ' (30)'), 'An effect — any four',
     H.split('1. Reduced standard of living', '4 points x 5 marks each',
             ['Reduced standard of living', 'Public services: loss / deterioration', 'Changed ownership of strategic state assets',
              'Public Sector Effects', 'Level of economic activity / demand fall', 'Growth in the black economy',
              'Widening gap between rich and poor', 'Public unrest']),
     4, 5, 'Four effects, ' + H.traced('4 points x 5 marks each') + '.', stem=q5a, **B)
q5b = H.q(6, 'It has been suggested that in order to reduce the National Debt', ' (i)')
add('sb-q5-b-i', '1-3', 'privatisation', ref('B', 5, '(b)(i)'), H.q(6, 'Explain the term ‘privatisation’.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('This is the sale of a state owned company to private owners.'), 5, 'Privatisation, 5 marks.')],
    stem=q5b, **B)
q5bii = H.q(6, 'Outline four economic arguments in favour of privatisation OR', ' (25)')
favour = [unnum(cc(x)) for x in ('1. Improved quality', '2. More competitive prices', '3. Continuity of supply', '4. Employment opportunities',
                                 '5. More rewards/Incentives', '6. Revenue from sale', '7. Shedding of loss making')]
against = [unnum(cc(x)) for x in ('1. Loss of non-profit', '2. Standards of service', '3. Curtailment in Pay', '4. Loss of jobs',
                                  '5. Loss of a state resource', '6.Costs of the Sale', '7. Foreign ownership')]
for word, head, opts in (('favour', 'arguments in favour', favour), ('against', 'arguments against', against)):
    pick(f'sb-q5-b-ii-{word}', '1-3', 'for-or-against-privatisation', ref('B', 5, '(b)(ii)', f'arguments {word}' if word == 'against'
                                                                         else 'arguments in favour'),
         f'{q5bii} Justify the choice: {"IN FAVOUR" if word == "favour" else "AGAINST"}.', H.traced(head) + ' — any four', opts, 4, 5,
         'Four arguments, ' + H.traced('4 points x 5 marks each') + '. The scheme credits arguments in favour and against, each '
         'with its own column.', stem=q5b, **B)
add('sb-q5-c', '3-1', 'cutting-the-public-sector-wage-bill', ref('B', 5, '(c)'),
    H.q(6, 'Discuss four measures the Minister for Finance could take', ' (20)'), '7 + 7 + 3 + 3', 20,
    [anyN('r-1', 'A measure — any four', 20, 4, 7,
          H.split('1. Reduce the numbers employed in the sector', '20 marks (7+7+3+3)',
                  ['Reduce the numbers employed in the sector', 'Reduce rates of pay per employee', 'Change terms of employment',
                   'Change pension entitlements', 'Outsource services']),
          'Four measures: ' + H.traced('20 marks (7+7+3+3)') + ', the first two correct 7 each and the next two 3 each.',
          steps=[7, 7, 3, 3])],
    kind='fixed', stem=H.q(6, '‘The number of staff in the Irish public sector grew', ' Discuss'), **B)

# Q6 ─ money; bank regulation; rising interest rates
q6a = H.q(6, 'Money is usually defined by reference to the functions it performs.', ' (i)')
pick('sb-q6-a-i', '3-4', 'the-functions-of-money', ref('B', 6, '(a)(i)'),
     H.q(6, 'Outline four functions of money.', ' (ii)'), 'A function — all four',
     H.split('1. Medium of exchange', '4 functions x 5 marks each',
             ['Medium of exchange', 'Measure of Value', 'Store of Wealth', 'Standard for Deferred Payment']),
     4, 5, 'Four functions, ' + H.traced('4 functions x 5 marks each') + '.', stem=q6a, **B)
add('sb-q6-a-ii', '3-3', 'monetary-policy', ref('B', 6, '(a)(ii)'), H.q(6, 'Explain the term ‘Monetary Policy’.', ' (iii)'), '8', 8,
    [point('r-1', H.opt('Those actions by the ECB, which influences the money supply', '\n8 marks'), 8, 'Monetary policy, 8 marks.')],
    stem=q6a, **B)
add('sb-q6-a-iii', '3-4', 'the-lender-of-last-resort', ref('B', 6, '(a)(iii)'),
    H.q(6, 'Explain a central bank’s function as ‘lender of last resort’.', ' (35)'), '7', 7,
    [point('r-1', H.opt('The central bank offers credit to financial institutions', '\n7 marks'), 7, 'The explanation, 7 marks.')],
    stem=q6a, **B)
pick('sb-q6-b', '3-4', 'why-regulate-the-banks', ref('B', 6, '(b)'),
     H.q(6, 'Discuss the economic reasons why commercial banks in Ireland should be regulated.', ' (20)'), 'A reason — any four',
     H.split('1. Protect consumers', '4 points x 5 marks each',
             ['Protect consumers', 'Proper lending policies', 'Banking system stability', 'Economic stability / confidence',
              'Less need for government intervention', 'Less need for EU / IMF funds']),
     4, 5, 'Four reasons, ' + H.traced('4 points x 5 marks each') + '.',
     stem=H.q(6, 'Many believe that a lack of supervision', ' Discuss'), **B)
pick('sb-q6-c', '3-3', 'rising-interest-rates', ref('B', 6, '(c)'),
     H.q(6, 'Explain the economic effects of rising interest rates on the Irish economy.', ' (20)'), 'An effect — any four',
     H.split('1. Borrowing discouraged', '4 points x 5 marks each',
             ['Borrowing discouraged', 'Savings encouraged', 'Increased mortgage repayments', 'Increased cost of servicing the National Debt',
              'Increased costs of production / reduced competitiveness', 'Disincentive to Invest', 'Economic Growth hindered',
              'Taxation revenue effects', 'Increases in Unemployment']),
     4, 5, 'Four effects, ' + H.traced('4 points x 5 marks each') + '.',
     stem=H.q(6, 'It is being suggested that the ECB will increase interest rates', ' Explain'), **B)

# Q7 ─ GDP and GNP; the multiplier; economic growth
add('sb-q7-a-i', '3-0', 'gdp-and-gnp', ref('B', 7, '(a)(i)'),
    H.q(7, 'Define the following terms:', ' (ii)'), '7 + 7', 14,
    [point('r-gdp', 'Gross Domestic Product at Current Market Prices — '
           + H.opt('The total output produced by the factors of production in the domestic economy', '\n7 marks'), 7, 'GDP, 7 marks.'),
     point('r-gnp', 'Gross National Product at Factor Cost — '
           + H.opt('The total output produced ( value of goods & services ) by Irish owned', '\n7 marks'), 7, 'GNP, 7 marks.')], **B)
pick('sb-q7-a-ii', '3-0', 'why-gdp-exceeds-gnp', ref('B', 7, '(a)(ii)'),
     H.q(7, 'Explain two reasons why GDP in Ireland at present is larger than GNP.', ' (30)'), 'A reason — any two',
     [unnum(x) for x in H.split('1. Repatriation of profits', '\n16 marks',
                                ['1. Repatriation of profits', '2. Repayment of interest', '3. Remittances of immigrants'])],
     2, 8, 'Two reasons, 8 each: the scheme prints ' + H.traced('16 marks') + ' beneath three reasons for an ask of two.', **B)
add('sb-q7-b-i', '3-0', 'the-multiplier', ref('B', 7, '(b)(i)'),
    H.q(7, 'Explain what is meant by the term ‘Multiplier’.', ' (ii)'), '8', 8,
    [point('r-1', H.opt('The multiplier shows the relationship between an (initial) injection', '\n8 marks'), 8, 'The explanation, 8 marks.')],
    **B)
add('sb-q7-b-ii', '3-0', 'the-irish-multiplier', ref('B', 7, '(b)(ii)'),
    H.q(7, 'Calculate the value of the Multiplier in the Irish economy.', ' (iii)'), '8', 8,
    [point('r-1', H.traced('1.25'), 8, 'The multiplier, ' + H.traced('8 marks') + ' by either of the scheme’s two methods: 1 over (MPS + '
           'MPT + MPM), or 1 over (1 – (MPC – MPT – MPM)). The working is shown with the answer.')],
    stem=H.q(7, 'It has been estimated that in the Irish economy:', ' Calculate'), figure=SOL + 'p30-q7bii-working', **B)
add('sb-q7-b-iii', '3-0', 'taxes-and-the-multiplier', ref('B', 7, '(b)(iii)'),
    H.q(7, 'Outline briefly how taxes affect the value of the Multiplier.', ' (25)'), '9', 9,
    [point(f'r-{i}', unnum(t), None, n) for i, (t, n) in enumerate((
        (H.traced('1. Taxes decrease spending within the economy / taxes are a leakage from the circular flow of national income.'),
         'Taxes are a leakage.'),
        (H.traced('2. When spending decreases less economic activity is generated within the economy.'), 'Less activity.'),
        (H.traced('3. The value/the magnitude of the multiplier decreases.'),
         'The multiplier falls. Claim the complete answer: the scheme prices its three points ' + H.traced('9 marks')
         + ' together, without dividing them.')), 1)],
    kind='questionTotal', **B)
growth_pos = [cc(x) for x in ('Increased employment Economic growth', 'Improved government finances', 'Effects on Balance of Payments',
                              'Improved standard of living', 'Effects on migration', 'Investment opportunities')]
growth_neg = [cc(x) for x in ('Inflationary pressures', 'Use of scarce resources', 'Increased demand for imports',
                              'Revised expectations by citizens', 'Uneven distribution of wealth')]
pick('sb-q7-c', '3-5', 'effects-of-faster-growth', ref('B', 7, '(c)'),
     H.q(7, 'Discuss the economic effects of an increase in the rate of economic growth', ' (20)'), 'An effect — any four',
     side('Positive economic effects', growth_pos) + side('Negative economic effects', growth_neg), 4, 5,
     'Four effects, positive or negative: ' + H.traced('4 points x 5 marks each') + '.',
     stem=H.q(7, '‘The Irish Government predicts that the rate of economic growth', ' Discuss'), **B)

# Q8 ─ the census; net outward migration; unemployment and the EU/IMF support
gov = [cc(x) for x in ('Infrastructural requirements It', 'Provision of essential services', 'Pension planning', 'Demographic changes',
                       'Qualifications of workforce')]
biz = [cc(x) for x in ('Future levels of consumer demand', 'Population data', 'Labour market The data')]
pick('sb-q8-a', '3-5', 'uses-of-the-2011-census', ref('B', 8, '(a)'),
     H.q(7, 'Discuss the economic uses of the 2011 Census of Population data', ' (20)'), 'A use — any four',
     side('Government', gov) + side('Business', biz), 4, 5,
     'Four uses, ' + H.traced('4 points x 5 marks each') + '. ' + H.traced('Candidates must have a minimum of one from each.'), **B)
add('sb-q8-b', '3-2', 'why-net-outward-migration-is-high', ref('B', 8, '(b)'),
    H.q(7, 'Discuss the reasons why Ireland is now experiencing a high level of net outward migration.', ' (25)'), '4 + 3 @ 7', 25,
    [point('r-compulsory', unnum(H.opt('1. Foreign nationals returning to their home countries', '\n_')), 4,
           H.traced('1 Compulsory point: 4 marks') + '.'),
     anyN('r-other', 'Another reason — any three', 21, 3, 7,
          H.split('2. Economic recession in Ireland', '\n31 | P a g e',
                  ['Economic recession in Ireland', 'Wage rates in Ireland', 'Prospects for economic recovery',
                   'Job opportunities abroad / emigration of skilled workers', 'Rising levels of taxation in Ireland.']),
          'Three other reasons, ' + H.traced('3 other points x 7 marks each') + '.')],
    kind='fixed', stem=H.q(7, '‘Ireland is experiencing the highest level of net outward migration since 1989’.', ' Discuss'), **B)
q8c = H.q(7, '‘The unemployment rate in Ireland in December 2010 was 13.6%’.', ' (i)')
pick('sb-q8-c-i', '3-2', 'measures-against-unemployment', ref('B', 8, '(c)(i)'),
     H.q(7, 'Discuss two economic measures which the Government could take', ' At the end'), 'A measure — any two',
     H.split('1. Reduce taxation', '2 points x 5 marks each',
             ['Reduce taxation', 'Subsidise additional labour employed', 'Reduce costs for business',
              'Government prudent management of the economy', 'Infrastructural development',
              'Maintain a low corporation profits tax base', 'Investment in education / training', 'Banking stability']),
     2, 5, 'Two measures, ' + H.traced('2 points x 5 marks each') + '.', stem=q8c, **B)
support_pos = [unnum(cc(x)) for x in ('1. Pay public sector workers', '2. Maintain public services', '3. Continuity of a banking system',
                                      '4. Acceptance of tax adjustments', '5. Acceptance of wage moderation')]
support_neg = [unnum(cc(x)) for x in ('1. High cost of repayment', '2. Taxation increases', '3. Loss of economic sovereignty',
                                      '4. Loss of confidence in economy', '5. Unemployment / Emigration')]
pick('sb-q8-c-ii', '3-1', 'the-eu-imf-financial-support', ref('B', 8, '(c)(ii)'),
     H.q(7, 'Discuss the economic effects of this financial support on the Irish economy.', ' (30)'), 'An effect — any four',
     side('Positive economic effects', support_pos) + side('Negative economic effects', support_neg), 4, 5,
     'Four effects, positive or negative: ' + H.traced('4 points x 5 marks each') + '.',
     stem=f"{q8c} {H.q(7, 'At the end of the year 2010, the EU and the IMF agreed', ' (ii)')}", **B)

if __name__ == '__main__':
    emit(cards)
