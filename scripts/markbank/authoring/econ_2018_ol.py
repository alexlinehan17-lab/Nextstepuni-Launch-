#!/usr/bin/env python3
"""Economics 2018 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2018-ol-ev.json, made
from a visual sweep of all 12 paper pages and 36 scheme pages before any 2018
card existed. Section B restarts at Question 1, so every citation names its
section and every id carries it (-sa-, -sb-). Question wording and stems are
sliced from the question paper; every marking point is sliced from the scheme
(econ_legacy_lib.py). The Ordinary scheme reprints each question above its
answer, so a slice always starts after the reprinted wording. The only prose
written here is guidance: tariffs, route labels and what a figure shows.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2018, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2018, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2018-OL-scheme-'
PAP = 'economics-2018-OL-paper-'
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

# Q1 ─ GNP, CPI, CSO
add('sa-q1', '3-0', 'gnp-cpi-and-cso', ref('A', 1), H.q(2, 'What do the following letters stand for?', ' GNP'),
    '9 (3+3+3), (2+1+1), (1+1+1)', 16,
    [point('r-gnp', H.cell('GNP Gross National Product'), 9, 'GNP, 9 marks (3 + 3 + 3), a word at a time.'),
     point('r-cpi', H.opt('CPI Consumer Price Index', '⟨(1+1+1)⟩'), 4, 'CPI, 4 marks (2 + 1 + 1).'),
     point('r-cso', H.cell('CSO Central Statistics Office'), 3, 'CSO, 3 marks (1 + 1 + 1).')], **A)

# Q2 ─ monopoly
q2 = H.q(2, 'The diagram below represents the long run equilibrium of a firm in Monopoly.', ' (i)')
add('sa-q2-i', '2-0', 'labelling-a-monopoly-diagram', ref('A', 2, '(i)'),
    H.q(2, 'Write in words the full label (not abbreviations)', ' 1 P'),
    '3 x 4', 12,
    [point(f'r-{n}', f'{n} — ' + H.traced(H.chunk(f'{n} {label}', ' 4').split(' ', 1)[1]), 4, f'Line {n}, 4 marks.')
     for n, label in ((1, 'Marginal cost'), (2, 'Average cost'), (3, 'Average revenue'))],
    stem=q2, figure=PAP + 'p02-q2-diagram', **A)
pick('sa-q2-ii', '2-0', 'barriers-to-entry', ref('A', 2, '(ii)'),
     H.q(2, 'Some firms may wish to enter a monopoly industry', ' (16 marks)'), 'A barrier to entry — any one',
     bl('• The government may grant a firm the sole right', 'Outline: A complete sentence'),
     1, 4, 'One barrier, 4 marks. ' + H.traced('Outline: A complete sentence is required in the candidate’s answer to merit full marks'),
     stem=q2, **A)

# Q3 ─ what shifts a firm's supply: true or false
sentences = [('(i) The price of the good itself.', 'True'), ('(ii) The consumer’s level of income.', 'False'),
             ('(iii) The cost of the firm’s raw materials.', 'True'), ('(iv) The state of the firm’s production technology.', 'True')]
add('sa-q3', '1-2', 'factors-in-a-firms-supply', ref('A', 3, '(i)–(iv)'),
    # The paper's own words, the answer table's header row dropped.
    H.q(2, 'Some of the factors below influence the supply of an individual firm.', ' (16 marks)').replace(' SENTENCE TRUE or FALSE', ''),
    '2 x 6 & 2 x 2', 16,
    [anyN('r-1', 'Each sentence marked correctly', 16, 4, 6,
          [f'{H.traced(ans)} — {H.traced(sent)}' for sent, ans in sentences],
          'All four: the first two correct 6 marks each, the other two 2 each.', steps=[6, 6, 2, 2])],
    kind='fixed', **A)

# Q4 ─ an economist
q4 = H.q(3, 'Name an economist you have studied and outline one contribution', ' (i)')
add('sa-q4-i', '0-0', 'naming-an-economist', ref('A', 4, '(i)'), H.q(3, 'Name economist:', ' (ii)'), '10', 10,
    [point('r-1', H.opt('Adam Smith / Thomas Malthus / David Ricardo', '⟨6⟩'), 10,
           'Naming an economist, 10 marks: any economist studied, such as those the scheme lists.')],
    stem=q4, **A)
q4ii = H.q(3, 'Outline one contribution to economic theory:', ' (16 marks)')
economists = (
    ('smith', 'Adam Smith', H.split('The pursuit of self interest', 'Thomas Malthus',
                                    ['The pursuit of self interest', 'Division of Labour', 'Labour Theory of Value',
                                     'State protection of property rights', '\'Invisible hand of competition\'',
                                     'Perfect Competition -', 'Laissez-faire', 'Canons of Taxation', 'Paradox of Value',
                                     'Free Trade -'])),
    ('malthus', 'Thomas Malthus', [H.opt('Theory of population and food supply:', 'David Ricardo')]),
    ('ricardo', 'David Ricardo', H.split('Law of comparative advantage dictates', '5 | P a g e',
                                         ['Law of comparative advantage', 'He developed the theory of economic rent',
                                          'Agreed with Malthus'])),
    ('marx', 'Karl Marx', H.split('Labour Theory of Value - The value of a good', 'John Maynard Keynes',
                                  ['Labour Theory of Value', 'Distribution of Capitalist profits', 'Evolution of Communism',
                                   'Exploitation of labour'])),
    ('keynes', 'John Maynard Keynes', H.split('National Income may be less than full employment.', 'Milton Friedman',
                                              ['National Income may be less', 'Output is demand determined',
                                               'He favoured government intervention', 'Investment decisions by entrepreneurs',
                                               'Investment could be less than savings', 'He developed new economic concepts',
                                               'He developed a liquidity preference theory'])),
    ('friedman', 'Milton Friedman', H.split('Monetary policy should be the main instrument', '6 | P a g e',
                                            ['Monetary policy should be', 'Monetarists suggest', 'Favoured a reduction in inflation',
                                             'He favoured a return to laissez faire', 'Supply side policies'])))
for key, name, options in economists:
    pick(f'sa-q4-ii-{key}', '0-0', 'an-economists-contribution', ref('A', 4, '(ii)', key),
         f'{q4ii} Answer for: {H.traced(name)}.', f'A contribution by {H.traced(name)} — any one', options, 1, 6,
         'One contribution, 6 marks. The scheme lists each economist’s own contributions.', stem=q4, **A)

# Q5 ─ substitutes and complements
add('sa-q5', '1-1', 'substitutes-and-complements-for-cars', ref('A', 5),
    H.q(3, 'The following items are either substitute goods or complementary goods', ' Answer:'), '4 @ 4', 16,
    [point(f'r-{item.split()[0].lower()}', f'{H.traced(side)} — {H.traced(item)}', 4, f'{side.capitalize()}, 4 marks.')
     for side, item in (('Substitute goods', 'BUS'), ('Substitute goods', 'TRAIN'),
                        ('Complementary goods', 'WINDSCREEN WIPERS'), ('Complementary goods', 'DIESEL'))], **A)

# Q6 ─ DIRT
q6 = H.q(3, 'The rate of DIRT was reduced to 37% in Budget 2018.', ' (i)')
add('sa-q6-i', '3-1', 'dirt-in-full', ref('A', 6, '(i)'), H.q(3, 'What do the letters DIRT stand for?', ' (ii)'), '8', 8,
    [point('r-1', H.traced('Deposit Interest Retention Tax'), 8, 'DIRT in full, 8 marks.')], stem=q6, **A)
pick('sa-q6-ii', '3-1', 'a-lower-dirt-rate-for-savers', ref('A', 6, '(ii)'),
     H.q(3, 'Outline one economic benefit for savers', ' (17 marks)'), 'A benefit for savers — any one',
     bl('• Savers will receive a greater return', '7 Price inflation in Ireland'), 1, 9, 'One benefit, 9 marks.', stem=q6, **A)

# Q7 ─ price inflation
q7 = H.q(3, 'Price inflation in Ireland is very low at present.', ' (i)')
add('sa-q7-i', '3-3', 'price-inflation', ref('A', 7, '(i)'), H.q(3, 'Price Inflation:', ' (ii)'), '8', 8,
    [point('r-1', H.traced('An increase in prices of goods / services over a period of time.'), 8, 'The explanation, 8 marks.')],
    stem=q7, **A)
pick('sa-q7-ii', '3-3', 'advantages-of-low-inflation', ref('A', 7, '(ii)'),
     H.q(3, 'Advantage of low rate of price inflation for Irish consumers:', ' (17 marks)'), 'An advantage — any one',
     bl('• Reduced prices for goods and services for consumers', '7 | P a g e'), 1, 9, 'One advantage, 9 marks.', stem=q7, **A)

# Q8 ─ the circular flow of income
q8 = H.q(4, 'The diagram below represents the Circular Flow of Income', ' 1')
add('sa-q8-i', '3-0', 'imports-as-a-leakage', ref('A', 8, '(i)'), H.q(4, 'Imports are a leakage', ' (ii)'), '8', 8,
    [point('r-1', H.opt('This means that money leaves the domestic economy', '(ii) State what each'), 8,
           'The explanation, 8 marks.')], stem=q8, **A)
add('sa-q8-ii', '3-0', 'lines-of-the-circular-flow', ref('A', 8, '(ii)'),
    H.q(4, 'State what each of the lines numbered 1 to 3 represents.', ' Line 1'), '3 x 3', 9,
    [point(f'r-{n}', H.opt(f'Line {n}:', nxt), 3, f'Line {n}, 3 marks.')
     for n, nxt in ((1, 'Line 2:'), (2, 'Line 3:'), (3, '9 Use three'))],
    stem=q8, figure=PAP + 'p04-q8-diagram', **A)

# Q9 ─ economic goods
add('sa-q9', '0-1', 'economic-goods', ref('A', 9),
    H.q(4, 'Use three of the five terms below to complete the explanation', ' (17 marks)'), '1 x 9 & 2 x 4', 17,
    [anyN('r-1', 'Each term placed', 17, 3, 9, [H.traced(t) for t in ('scarce resources', 'opportunity cost', 'price')],
          'The three terms in order: the first correct 9 marks, the other two 4 each. The scheme’s completed sentence: '
          + H.opt('Economic goods require the use of scarce resources', '8 | P a g e'), steps=[9, 4, 4])],
    kind='fixed', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════
B = dict(section='B')
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell


def by_heading(rid, label, options, per, note):
    """One printed head ("Employees", "Banks") and any one of its responses."""
    return heading(rid, H.traced(label) + ' — any one', options, per, note)


# Q1 ─ perfect competition; low-cost airlines
q1 = H.q(5, 'The diagram below represents the long run equilibrium of a firm in Perfect Competition.', ' Price')
q1_fig = PAP + 'p05-q1-diagram'
add('sb-q1-a-i', '2-0', 'labels-of-perfect-competition', ref('B', 1, '(a)(i)'),
    H.q(5, 'Write out what each of the five underlined labels above represents.', ' Copy'), '5 @ 4', 20,
    [point(f'r-{lab.lower()}', f'{H.traced(lab)} — {H.traced(full)}', 4, f'{lab}, 4 marks.')
     for lab, full in (('MC', 'Marginal Cost'), ('AC', 'Average Cost'), ('D', 'Demand'), ('AR', 'Average Revenue'),
                       ('MR', 'Marginal Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'equilibrium-in-perfect-competition', ref('B', 1, '(a)(ii)'),
    H.q(5, 'Equilibrium occurs at point B on the diagram.', ' (30 marks)'), '5 + 5', 10,
    [point('r-price', H.opt('The price the firm will charge for its output (use label P1).', '• The output'), 5,
           'P1, 5 marks. The completed diagram is shown with the answer.'),
     point('r-output', H.traced('The output the firm will produce in equilibrium (use label Q1).'), 5, 'Q1, 5 marks.')],
    stem=q1, figure=SOL + 'p11-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
q1b = H.q(5, 'Explain each of the following characteristics of a perfectly competitive market.', ' (i)')
# The scheme reprints the three characteristics, then answers each under its own
# line: the second occurrence of each is the answer's head.
for part, concept, head, nxt, ask_end in (
        ('i', 'perfect-knowledge', 'Perfect knowledge exists.', 'All goods produced are homogenous goods.', ' (ii)'),
        ('ii', 'homogenous-goods', 'All goods produced are homogenous goods.', 'Free entry and exit exists in the industry.', ' (iii)'),
        ('iii', 'free-entry-and-exit', 'Free entry and exit exists in the industry.', '⟨21⟩', ' (21 marks)')):
    answer = H.opt(head, nxt, occ=1)[len(head):].strip()
    add(f'sb-q1-b-{part}', '2-0', concept, ref('B', 1, f'(b)({part})'), f'{q1b} {H.q(5, head, ask_end)}', '7', 7,
        [point('r-1', H.traced(answer), 7, 'The explanation, 7 marks.')], **B)
q1c = H.q(5, 'In 2017 Ryanair experienced increased competition', ' Outline')
add('sb-q1-c', '2-0', 'competition-among-low-cost-airlines', ref('B', 1, '(c)'),
    H.q(5, 'Outline two possible advantages for consumers and one possible challenge', ' (24 marks)'), '3 x 8', 24,
    [anyN('r-advantages', H.traced('Possible advantages of increased competition for consumers') + ' — any two', 16, 2, 8,
          H.split('More competitive prices', 'Possible challenge of increased competition',
                  ['More competitive prices', 'Greater choice of routes', 'Improved quality / range of services']),
          'Two advantages for consumers, 8 marks each.'),
     by_heading('r-challenge', 'Possible challenge of increased competition for producers/business',
                H.split('Need to be more cost efficient', '⟨24⟩',
                        ['Need to be more cost efficient', 'Possible loss of customers', 'More innovation required']), 8,
                'One challenge for producers, 8 marks.')],
    kind='fixed', stem=q1c, **B)

# Q2 ─ utility; demand for smartphones; the sugar tax
q2a = H.q(6, 'People consume goods because they receive utility.', ' (i)')
q2a_table = PAP + 'p06-q2a-table'
add('sb-q2-a-i', '1-1', 'utility-and-marginal-utility', ref('B', 2, '(a)(i)'), f"{q2a} {H.q(6, 'Explain each of the underlined terms.', ' (ii)')}",
    '5 + 5', 10,
    [point('r-utility', 'Utility — ' + H.traced('The satisfaction a consumer receives from consuming a good / service.'), 5, 'Utility, 5 marks.'),
     point('r-mu', 'Marginal utility — ' + H.opt('This is the extra / additional satisfaction', '(ii) Complete the following'), 5,
           'Marginal utility, 5 marks.')], **B)
add('sb-q2-a-ii', '1-1', 'calculating-marginal-utility', ref('B', 2, '(a)(ii)'),
    H.q(6, 'Using the table below calculate the marginal utility at A, B and C.', ' (iii)'), '3 x 4', 12,
    [point(f'r-{k}', f'{k} — {H.traced(w)}', 4, f'{k}, 4 marks.')
     for k, w in (('A', '110 – 70 = 40'), ('B', '130 – 110 = 20'), ('C', '140 – 130 = 10'))],
    stem=q2a, figure=q2a_table, **B)
add('sb-q2-a-iii', '1-1', 'where-diminishing-marginal-utility-sets-in', ref('B', 2, '(a)(iii)'),
    H.q(6, 'State at what point diminishing marginal utility sets in', ' 1 2'), '1 + 2', 3,
    [point('r-point', H.traced('After the 4th unit is consumed / on the consumption of the 5th unit.'), 1, 'The point, 1 mark.'),
     point('r-reason', H.opt('On the consumption of the 5th unit the consumer’s marginal utility', '⟨25⟩'), 2,
           'The explanation, 2 marks.')],
    stem=q2a, figure=q2a_table, **B)
q2b = H.q(6, 'The diagram below shows two demand curves for smartphones.', ' Price')
q2b_fig = PAP + 'p06-q2b-diagram'
add('sb-q2-b-i', '1-1', 'the-shape-of-a-demand-curve', ref('B', 2, '(b)(i)'),
    H.q(6, 'Explain the shape of a demand curve for smartphones.', ' (ii)'), '7', 7,
    [point('r-1', H.traced('As the price of smartphones decrease the quantity demanded will increase.'), 7, 'The explanation, 7 marks.')],
    stem=q2b, figure=q2b_fig, **B)
add('sb-q2-b-ii', '1-1', 'an-increase-in-demand', ref('B', 2, '(b)(ii)'),
    H.q(6, 'State whether the shift in demand from D1 to D2 above', ' (iii)'), '6', 6,
    [point('r-1', H.opt('The shift in demand from D1 to D2: represents', '(iii) State and explain two', occ=0), 6, 'The answer, 6 marks.')],
    stem=q2b, figure=q2b_fig, **B)
pick('sb-q2-b-iii', '1-1', 'why-demand-for-smartphones-shifts', ref('B', 2, '(b)(iii)'),
     H.q(6, 'State and explain two reasons why the demand for smartphones', ' (25 marks)'), 'A reason — any two',
     H.split('Increase in incomes\nConsumers', '⟨25⟩',
             ['Increase in incomes', 'Changing preference / taste', 'Reduction in the price of complements', 'Unplanned factors']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q2b, figure=q2b_fig, **B)
q2c = H.q(6, 'A tax on sugar‐sweetened drinks was introduced', ' (i)')
pick('sb-q2-c-i', '1-3', 'why-introduce-a-sugar-tax', ref('B', 2, '(c)(i)'),
     H.q(6, 'Outline two reasons why the government introduced the sugar tax.', ' (ii)'), 'A reason — any two',
     H.split('Reduce consumption of sugary foods / reduce obesity levels', '(ii) Outline two possible advantages and one',
             ['Reduce consumption of sugary foods', 'Revenue for state', 'Help fund health initiatives',
              'Help reduce future health costs', 'Incentive for entrepreneurs'], occ=None),
     2, 5, 'Two reasons, 5 marks each.', stem=q2c, **B)
add('sb-q2-c-ii', '1-3', 'the-sugar-tax-for-consumers', ref('B', 2, '(c)(ii)'),
    H.q(6, 'Outline two possible advantages and one possible disadvantage of this sugar tax', ' (25 marks)'), '3 x 5', 15,
    [anyN('r-advantages', H.traced('Advantages') + ' — any two', 10, 2, 5,
          [cc('Healthier lifestyle / reduction in obesity'), cc('Possible increase in disposable income'),
           cc('More alternatives may become available')], 'Two advantages, 5 marks each.'),
     by_heading('r-disadvantage', 'Disadvantage', [cc('Higher prices for consumers'), cc('May be regressive')], 5,
                'One disadvantage, 5 marks.')],
    kind='fixed', stem=q2c, **B)

# Q3 ─ factors of production; costs and revenue; the minimum wage
explain, ret = H.traced('Explanation'), H.traced('Return')
# Each explanation is one table cell; the cell's line-end hyphen ("pro- duction")
# is joined back, as the page prints the word across a line break.
dehyphen = lambda t: re.sub(r'(\w)- (\w)', r'\1\2', t)
factors = [(H.traced('Land'), dehyphen(cc('anything supplied by nature')), H.traced('Rent')),
           (H.traced('Labour'), dehyphen(cc('the human effort involved')), H.traced('Wages / Salary')),
           (H.traced('Capital'), dehyphen(cc('anything man-made used')), H.traced('Interest'))]
add('sb-q3-a', '0-1', 'factors-of-production-and-their-returns', ref('B', 3, '(a)'),
    H.q(7, 'Explain the three other factors of production', ' (24 marks)'), '3 x 8 (3 + 2 + 3)', 24,
    [point(f'r-{f.lower()}', f'{f} — {ret}: {r} — {e}', 8, f'{f}: the factor, its explanation and its return, 8 marks (3 + 2 + 3).')
     for f, e, r in factors],
    stem=H.q(7, 'Profit is the return to the factor of production enterprise.', ' Explain'), **B)
q3b = H.q(7, 'The table below shows the output, total cost and total revenue', ' Output')
q3b_table = PAP + 'p07-q3b-table'
add('sb-q3-b-i', '1-5', 'total-revenue-at-each-output', ref('B', 3, '(b)(i)'),
    H.q(7, 'Calculate the total revenue received at each level of output', ' (ii)'), '3 x 4', 12,
    [point(f'r-{k.lower()}', f'{k} — {H.traced(w)} — {H.traced(a)}', 4, f'{k}, 4 marks.')
     for k, w, a in (('A', '200 x €10', '€2,000'), ('B', '300 x €10', '€3,000'), ('C', '400 x €10', '€4,000'))],
    stem=q3b, figure=q3b_table, **B)
add('sb-q3-b-ii', '1-5', 'profit-at-200-units', ref('B', 3, '(b)(ii)'), H.q(7, 'Calculate the profit earned when the firm sells 200 units.', ' (iii)'),
    '6', 6, [point('r-1', H.traced('(200 x €10) = €2,000 - €600 = €1,400'), 6, 'The profit with its working, 6 marks.')],
    stem=q3b, figure=q3b_table, **B)
add('sb-q3-b-iii', '1-5', 'fixed-and-variable-costs', ref('B', 3, '(b)(iii)'),
    H.q(7, 'The total costs of the firm include fixed costs and variable costs.', ' (30 marks)'), '2 x 6 (4 + 2)', 12,
    [point('r-fixed', 'Fixed cost — ' + H.opt('Costs which do not change as output changes', 'Variable cost'), 6,
           'Fixed costs with an example, 6 marks (4 + 2).'),
     point('r-variable', 'Variable cost — ' + H.opt('Costs which do change as output changes.', '⟨30⟩'), 6,
           'Variable costs with an example, 6 marks (4 + 2).')],
    stem=q3b, **B)
side = lambda label, options: [f'{H.traced(label)} — {o}' for o in options]
pos, neg = 'Possible positive economic effect', 'Possible negative economic effect'


def cell_bullets(first):
    """The bullets of one table cell (the cell rendering joins them on one line)."""
    return [H.traced(x.strip().rstrip(' .').strip()) for x in cc('• ' + first).split('•') if x.strip().rstrip(' .').strip()]


add('sb-q3-c', '2-1', 'raising-the-minimum-wage', ref('B', 3, '(c)'),
    H.q(7, 'State and explain one possible economic effect of an increase in the national minimum wage', ' (21 marks)'),
    '3 x 7 (4 + 3)', 21,
    [by_heading(f'r-{who.lower()}', who,
                side(pos, cell_bullets(p_first)) + side(neg, cell_bullets(n_first)), 7,
                f'One effect for {who.lower()}, positive or negative, 7 marks (4 + 3).')
     for who, p_first, n_first in (('Employees', 'Higher Standard of living', 'Possible loss of hours'),
                                   ('Businesses', 'More productivity', 'Loss of competitiveness'),
                                   ('Consumers', 'Better quality service', 'Higher prices'))],
    kind='fixed', stem=H.q(7, 'Trade unions favour an increase in the national minimum wage rate.', ' State'), **B)

# Q4 ─ money; savings; non-cash payment
pick('sb-q4-a', '3-4', 'functions-of-money', ref('B', 4, '(a)'), H.q(7, 'State and explain any three functions of money.', ' (21 marks)'),
     'A function of money — any three', [H.traced(x) for x in ('Medium of exchange', 'Measure of Value', 'Store of Wealth',
                                                            'Standard for Deferred Payment')],
     3, 7, 'Three functions, 7 marks each (2 + 5): the scheme prints the four functions by name.', **B)
pick('sb-q4-b-i', '3-4', 'why-consumers-save', ref('B', 4, '(b)(i)'),
     H.q(7, 'State and explain two reasons why consumers may decide to save', ' (ii)'), 'A reason — any two',
     H.split('Income levels / Tax on incomes', '16 | P a g e',
             ['Income levels / Tax on incomes', 'Rate of DIRT', 'Future Demands on their spending', 'Create a ‘rainy day fund’',
              'Interest rate']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', **B)
add('sb-q4-b-ii', '3-4', 'savings-and-the-irish-economy', ref('B', 4, '(b)(ii)'),
    H.q(7, 'Discuss one economic advantage and one economic disadvantage of savings', ' (24 marks)'), '2 x 6 (3 + 3)', 12,
    [by_heading('r-advantage', 'One possible economic advantage',
                [cc(x, whole=True) for x in ('Reduced inflation', 'Reduced demand for imports', 'More funds available for investment',
                                             'Ease personal debt')]
                + [cc('Reduce future demands on'), cc('Increase in DIRT revenue for the')], 6,
                'One advantage, 6 marks (3 + 3).'),
     by_heading('r-disadvantage', 'One possible economic disadvantage',
                [cc('Reduced spending in the economy', whole=True), cc('Increase in unemployment due to'),
                 cc('Reduced economic growth', whole=True)], 6,
                'One disadvantage, 6 marks (3 + 3).')],
    kind='fixed', **B)
q4c = H.q(7, 'There is a move away from cash', ' (i)')
pick('sb-q4-c-i', '3-4', 'non-cash-methods-of-payment', ref('B', 4, '(c)(i)'), H.q(7, 'Name two non cash‐based methods of payments.', ' (ii)'),
     'A method — any two', [H.traced(x) for x in ('Credit Card', 'Debit Card', 'Cheque', 'Direct Debit', 'Standing Order',
                                                 'Transfers via online banking')],
     2, 6, 'Two methods, 6 marks each.', stem=q4c, **B)
add('sb-q4-c-ii', '3-4', 'advantages-of-non-cash-payment', ref('B', 4, '(c)(ii)'),
    H.q(7, 'Outline one possible economic advantage which non cash', ' (30 marks)'), '3 x 6', 18,
    [by_heading('r-banks', 'Banks', H.split('Time saved by staff dealing with cash', 'Businesses\nLess',
                                            ['Time saved by staff', 'Development of new / improved banking methods',
                                             'Reduction in staff numbers']), 6, 'One advantage for banks, 6 marks.'),
     by_heading('r-businesses', 'Businesses', H.split('Less need to handle cash', 'Consumers\nMore',
                                                     ['Less need to handle cash', 'Reduced security risks',
                                                      'Lower insurance premiums']), 6, 'One advantage for businesses, 6 marks.'),
     by_heading('r-consumers', 'Consumers', H.split('More convenient for consumers', '⟨30⟩',
                                                   ['More convenient for consumers', 'Written record:']), 6,
                'One advantage for consumers, 6 marks.')],
    kind='fixed', stem=q4c, **B)

# Q5 ─ the budget; taxes; spending on education
q5a = ' '.join([H.q(8, 'The following figures were presented in Budget 2018:', ' Government'),
                ])
q5a_table = PAP + 'p08-q5a-table'
add('sb-q5-a-i', '3-1', 'budget-deficit-or-surplus', ref('B', 5, '(a)(i)'),
    H.q(8, 'Is the government planning a budget deficit or budget surplus?', ' The national'), '6 (3 + 3)', 6,
    [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate([
        (H.traced('€67.4 bn - €70.1 bn = €2.7 billion.'), 'The scheme prices the answer and its explanation 6 (3 + 3) together '
         'and does not say which earns which.'),
        (H.traced('A budget deficit.'), 'Part of the answer.'),
        (H.traced('It is planning to spend more than it is bringing in in current revenue.'), 'Claim the complete answer: 6 marks in all.')], 1)],
    kind='questionTotal', stem=q5a, figure=q5a_table, **B)
q5aii_stem = H.q(8, 'The national debt is approximately €200 billion currently.', ' (ii)')
add('sb-q5-a-ii', '3-1', 'the-budget-and-the-national-debt', ref('B', 5, '(a)(ii)'),
    H.q(8, 'State the effect which Budget 2018, calculated in part (i) above', ' (iii)'), '6 (3 + 3)', 6,
    [point(f'r-{i}', t, None, n) for i, (t, n) in enumerate([
        (H.traced('The national debt will increase.'), 'The scheme prices the effect and its explanation 6 (3 + 3) together '
         'and does not say which earns which.'),
        (H.traced('Expenditure is greater than income (by €2.7 bn) and this must be borrowed.'), 'The explanation.'),
        (H.traced('The budget deficit must be borrowed.'), 'Claim the complete answer: 6 marks in all.')], 1)],
    kind='questionTotal', stem=f'{q5a} {q5aii_stem}', figure=q5a_table, **B)
add('sb-q5-a-iii', '3-1', 'increasing-the-national-debt', ref('B', 5, '(a)(iii)'),
    H.q(8, 'State and explain one economic advantage and one economic disadvantage of increasing', ' (24 marks)'),
    '2 x 6 (3 + 3)', 12,
    [by_heading('r-advantage', 'Economic advantage',
                [cc('Current cost of borrowing is low.', whole=True), cc('Provision of / Improvement'),
                 cc('Improvements in infrastructure.', whole=True), cc('Homelessness problem may be addressed.', whole=True)], 6,
                'One advantage, 6 marks (3 + 3).'),
     by_heading('r-disadvantage', 'Economic disadvantage',
                [cc('Increased annual interest repayments.', whole=True), cc('Opportunity cost.', whole=True),
                 cc('Increased pressure on taxpayers.', whole=True), cc('Increased risk to the provision of public'),
                 cc('Reduced confidence in the economy.', whole=True)], 6, 'One disadvantage, 6 marks (3 + 3).')],
    kind='fixed', stem=q5aii_stem, **B)
q5b = H.q(8, 'In the case of each of the following taxes:', ' (i)')
# Each tax is named by the paper's own bullet (the scheme's table cell splits the
# last across two lines).
taxes = (('profits', 'a tax on company profits', 'Corporation Profits Tax', 'Direct'),
         ('wages', 'a tax on employees’ wages', 'Income tax / PAYE', 'Direct'),
         ('goods', 'a tax on goods or services', 'Value Added Tax', 'Indirect'))
for _, t, _, _ in taxes:
    assert t in q5b, t
add('sb-q5-b-i', '3-1', 'naming-taxes', ref('B', 5, '(b)(i)'), H.q(8, 'Name each tax above.', ' (ii)'), '3 x 3', 9,
    [point(f'r-{k}', f'{t} — {H.traced(n)}', 3, 'A name, 3 marks: the scheme prices the six cells of (i) and (ii) 6 x 3.')
     for k, t, n, _ in taxes], stem=q5b, **B)
add('sb-q5-b-ii', '3-1', 'direct-or-indirect-taxes', ref('B', 5, '(b)(ii)'),
    H.q(8, 'State whether each tax is an example of a direct tax', ' (iii)'), '3 x 3', 9,
    [point(f'r-{k}', f'{t} — {H.traced(n)} — {H.traced(d)}', 3, '3 marks, a cell of the scheme’s 6 x 3.')
     for k, t, n, d in taxes], stem=q5b, **B)
add('sb-q5-b-iii', '3-1', 'direct-and-indirect-taxes', ref('B', 5, '(b)(iii)'),
    H.q(8, 'Explain each of the underlined terms in part (ii) above.', ' (30 marks)'), '2 x 6', 12,
    [point('r-direct', H.traced('Direct taxes: are taxes on income or profits.'), 6, 'Direct taxes, 6 marks.'),
     point('r-indirect', H.traced('Indirect taxes: are taxes on goods and services / taxes on spending.'), 6, 'Indirect taxes, 6 marks.')],
    stem=q5b, **B)
q5c = H.q(8, 'Spending by the Irish government on education', ' (i)')
add('sb-q5-c-i', '0-1', 'opportunity-cost', ref('B', 5, '(c)(i)'), H.q(8, 'Explain the term opportunity cost.', ' (ii)'), '7', 7,
    [point('r-1', H.opt('The cost of foregone alternatives', '(ii) State and explain two possible'), 7, 'The explanation, 7 marks.')],
    stem=q5c, **B)
pick('sb-q5-c-ii', '3-1', 'spending-on-education', ref('B', 5, '(c)(ii)'),
     H.q(8, 'State and explain two possible economic advantages of increased government spending', ' (21 marks)'),
     'An advantage — any two',
     H.split('Citizens may be better informed / more opportunities', '⟨21⟩',
             ['Citizens may be better informed', 'Improved quality of education service', 'Workforce improved',
              'Business productivity / reduced costs', 'Access to education improved', 'May make Ireland more attractive',
              'Promote entrepreneurship']),
     2, 7, 'Two advantages, 7 marks each (4 + 3).', stem=q5c, **B)

# Q6 ─ national income; multinationals; development aid
q6a = H.q(9, 'Given National Income (Y) as:', ' (i)')
letters = [H.traced(x) for x in ('Consumption', 'Investment', 'Government expenditure', 'Exports', 'Imports')]
add('sb-q6-a-i', '3-0', 'the-national-income-identity', ref('B', 6, '(a)(i)'),
    H.q(9, 'State what each of the letters in the formula above represents.', ' (ii)'), '10 (5 x 2)', 10,
    [point(f'r-{k.lower()}', f'{H.traced(k)} — {w}', 2, f'{k}, 2 marks.') for k, w in zip('CIGXM', letters)],
    stem=q6a, **B)
add('sb-q6-a-ii', '3-0', 'calculating-national-income', ref('B', 6, '(a)(ii)'),
    H.q(9, 'Calculate, using the figures provided, the level of National Income.', ' (20 marks)'), '10', 10,
    [point('r-1', H.traced('€2,500m + €500m + €600m + (€300m - €200m) = €3,700m'), 10, 'National income with its working, 10 marks.')],
    stem=q6a, **B)
q6b = H.q(9, 'Multinational Companies (MNCs), such as Facebook', ' (i)')
add('sb-q6-b-i', '4-1', 'multinationals-and-economic-growth', ref('B', 6, '(b)(i)'),
    H.q(9, 'Explain the terms multinational company and economic growth.', ' (ii)'), '2 x 5', 10,
    [point('r-mnc', 'Multinational company — ' + H.opt('Is a business that operates in many different countries', 'Economic growth\n•'), 5,
           'A multinational company, 5 marks.'),
     point('r-growth', 'Economic growth — ' + H.opt('It is the rise in GNP / output', '• Increased productive'), 5,
           'Economic growth, 5 marks. The scheme also accepts its second statement.',
           accepts=[H.traced('Increased productive capacity of an economy.')])], stem=q6b, **B)
pick('sb-q6-b-ii', '4-1', 'benefits-of-multinationals', ref('B', 6, '(b)(ii)'),
     H.q(9, 'Discuss two possible economic benefits of MNCs, other than economic growth', ' (iii)'), 'A benefit — any two',
     [f"{cc(head, whole=True)} — {cc(text)}" for head, text in (
         ('Employment', 'The MNCs will create jobs'), ('Exports will increase', 'These firms produce their goods'),
         ('Taxation revenues will increase', 'With the increase in the level of employment'),
         ('Attract investment', 'If the MNCs are profitable'), ('Benefits to local economy', 'Firms in the local economy'))],
     2, 5, 'Two benefits, 5 marks each (3 + 2).', stem=q6b, **B)
pick('sb-q6-b-iii', '4-1', 'challenges-of-multinationals', ref('B', 6, '(b)(iii)'),
     H.q(9, 'Discuss one possible economic challenge of MNCs', ' (25 marks)'), 'A challenge — any one',
     [f"{cc(head, whole=True)} — {cc(text)}" for head, text in (
         ('Domestic firm closures', 'Unable to compete'), ('Less competition', 'Less competition which'),
         ('Loss of jobs if they re-locate', 'Should the MNC relocate'),
         ('Repatriation of profits to home country', 'The repatriation of profits'),
         ('Negotiating too favourable terms from the state', 'Some MNC may have'))],
     1, 5, 'One challenge, 5 marks (3 + 2).', stem=q6b, **B)
q6c = H.q(9, '‘An extra €13 million is being spend', ' (i)')
pick('sb-q6-c-i', '4-0', 'characteristics-of-ldcs', ref('B', 6, '(c)(i)'),
     H.q(9, 'Outline two characteristics of Less Developed Countries', ' (ii)'), 'A characteristic — any two',
     bl('• High population growth rates in LDCs', '(ii) Describe two types'), 2, 5, 'Two characteristics, 5 marks each.',
     stem=q6c, **B)
pick('sb-q6-c-ii', '4-0', 'non-financial-aid', ref('B', 6, '(c)(ii)'),
     H.q(9, 'Describe two types of aid, other than financial aid', ' (iii)'), 'A type of aid — any two',
     bl('• Aid through voluntary agencies', '26 | P a g e'), 2, 5, 'Two types of aid, 5 marks each.', stem=q6c, **B)
pick('sb-q6-c-iii', '4-0', 'when-financial-aid-fails', ref('B', 6, '(c)(iii)'),
     H.q(9, 'Outline two reasons why financial aid may not always help', ' (30 marks)'), 'A reason — any two',
     H.split('Unfair distribution of benefits / poverty gap may widen', '⟨30⟩',
             ['Unfair distribution of benefits', 'Costs to the environment', 'Rapid population growth',
              'Citizens may become dependent', 'Using aid to invest in high profile projects', 'Financial aid is tied',
              'UN Target 0.7% GNP']),
     2, 5, 'Two reasons, 5 marks each.', stem=q6c, **B)

# Q7 ─ trade; visible trade; Brexit
q7a = H.q(9, 'Ireland as a small open economy relies on international trade.', ' (i)')
add('sb-q7-a-i', '4-2', 'an-open-economy', ref('B', 7, '(a)(i)'), H.q(9, 'Explain the term open economy.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Explanation: it engages in trade i.e. it imports and exports goods and services.'), 6,
           'The explanation, 6 marks.')], stem=q7a, **B)
pick('sb-q7-a-ii', '4-2', 'why-ireland-trades', ref('B', 7, '(a)(ii)'),
     H.q(9, 'State and explain three economic reasons why Ireland engages in trade.', ' (24 marks)'), 'A reason — any three',
     H.split('Job creation.\nExports', '⟨24⟩',
             ['Job creation.', 'Increased GNP / Economic growth', 'Increased sales [', 'Earn foreign currencies',
              'Attract investment', 'More choice for consumers', 'Raw materials unavailable', 'Enhanced international reputation']),
     3, 6, 'Three reasons, 6 marks each (3 + 3).', stem=q7a, **B)
q7b = H.q(9, '‘Visible exports were €45,537 million', ' (i)')
vx, vm = H.traced('Visible exports'), H.traced('Visible imports')
add('sb-q7-b-i', '4-2', 'visible-exports-and-imports', ref('B', 7, '(b)(i)'),
    H.q(9, '‘Visible exports were €45,537 million', ' (ii) Name one example'),
    '2 x 6', 12,
    [point('r-exports', f"{vx} — {cc('The sale of Irish goods abroad')}", 6, 'Visible exports, 6 marks.'),
     point('r-imports', f"{vm} — {cc('The purchase of foreign goods')}", 6, 'Visible imports, 6 marks.')],
    **B)
add('sb-q7-b-ii', '4-2', 'examples-of-visible-trade', ref('B', 7, '(b)(ii)'),
    H.q(9, 'Name one example of a visible export and a visible import', ' (iii)'), '2 x 3', 6,
    [point('r-export', f"{vx} — {H.traced('Sale of Irish beef abroad.')}", 3, 'An example of a visible export, 3 marks.'),
     point('r-import', f"{vm} — {H.traced('Purchase of foreign cars.')}", 3, 'An example of a visible import, 3 marks.')],
    stem=q7b, **B)
pick('sb-q7-b-iii', '4-2', 'advantages-of-a-trade-surplus', ref('B', 7, '(b)(iii)'),
     H.q(9, 'Outline two economic advantages for the Irish economy if exports are greater', ' (30 marks)'), 'An advantage — any two',
     H.split('Employment creation\nIf exports', '⟨30⟩',
             ['Employment creation', 'Increased GNP / Economic growth', 'Attract investment', 'Government finances',
              'Increased sales / profits']),
     2, 6, 'Two advantages, 6 marks each.', stem=q7b, **B)
q7c = H.q(9, 'Brexit will occur formally in March 2019.', ' (i)')
add('sb-q7-c-i', '4-2', 'brexit', ref('B', 7, '(c)(i)'), H.q(9, 'What is meant by the term Brexit?', ' (ii)'), '8', 8,
    [point('r-1', H.traced('Brexit means that the UK will leave the EU in 2019.'), 8, 'The explanation, 8 marks.')], stem=q7c, **B)
add('sb-q7-c-ii', '4-2', 'tariffs-and-quotas', ref('B', 7, '(c)(ii)'),
    H.q(9, 'Irish exporting firms may have to deal with tariffs and quotas.', ' (iii)'), '2 x 3', 6,
    [point('r-tariffs', f"{H.traced('Tariffs')} — {cc('This is a tax on imported goods.', whole=True)}", 3, 'Tariffs, 3 marks.'),
     point('r-quotas', f"{H.traced('Quotas')} — {cc('This is a limit on the quantity of goods')}", 3, 'Quotas, 3 marks.')],
    stem=q7c, **B)
pick('sb-q7-c-iii', '4-2', 'brexit-challenges-for-exporters', ref('B', 7, '(c)(iii)'),
     H.q(9, 'State and explain one economic challenge, other than tariffs and quotas', ' (21 marks)'), 'A challenge — any one',
     H.split('Transport costs\nAs Ireland', '⟨21⟩',
             ['Transport costs', 'Exchange rate risk', 'Language skills', 'Bureaucracy in other countries',
              'Higher level of costs coming', 'Capacity of the firm', 'Develop new markets', 'Uncertainty']),
     1, 7, 'One challenge, 7 marks (4 + 3).', stem=q7c, **B)

# Q8 ─ employment; the retirement age; homelessness
q8a = H.q(10, '‘Ireland’s unemployment rate is expected to be 6 %', ' (i)')
add('sb-q8-a-i', '3-2', 'measuring-unemployment', ref('B', 8, '(a)(i)'), H.q(10, 'Name one method of measuring unemployment', ' (ii)'),
    '3', 3, [point('r-1', H.traced('Live Register or Quarterly National Household Survey.'), 3, 'One method, 3 marks.')],
    stem=q8a, **B)
add('sb-q8-a-ii', '3-2', 'effects-of-rising-employment', ref('B', 8, '(a)(ii)'),
    H.q(10, 'Discuss one economic effect which the continuing rise in employment', ' (30 marks)'), '3 x 9 (5 + 4)', 27,
    [by_heading('r-retailers', 'Retailers in Ireland',
                H.split('Increased Sales/Profits', 'Government finances\nTax', ['Increased Sales/Profits', 'Expansion Retailers']), 9,
                'One effect on retailers, 9 marks (5 + 4).'),
     by_heading('r-finances', 'Government finances',
                H.split('Tax revenues\nIncreased', 'Ireland’s Balance of Trade\nIncreased',
                        ['Tax revenues', 'Social welfare spending', 'Reduced state borrowing', 'Less social problems']), 9,
                'One effect on government finances, 9 marks (5 + 4).'),
     by_heading('r-trade', 'Ireland’s Balance of Trade',
                H.split('Increased demand for imports', '⟨30⟩', ['Increased demand for imports', 'Imports of raw materials']), 9,
                'One effect on the balance of trade, 9 marks (5 + 4).')],
    kind='fixed', stem=q8a, **B)
add('sb-q8-b', '2-1', 'extending-the-retirement-age', ref('B', 8, '(b)'),
    H.q(10, 'Outline two advantages of extending the public service retirement age', ' (24 marks)'), '4 x 6', 24,
    [anyN('r-employees', H.traced('Employees') + ' — any two', 12, 2, 6,
          H.split('Can participate in the labour force for longer', 'Government\nReduced',
                  ['Can participate in the labour force', 'Higher standard of living', 'Greater personal satisfaction']),
          'Two advantages for employees, 6 marks each.'),
     anyN('r-government', H.traced('Government') + ' — any two', 12, 2, 6,
          H.split('Reduced pension bill', '⟨24⟩',
                  ['Reduced pension bill', 'Increased tax revenues', 'Less skills shortages', 'Reduction on spending and training']),
          'Two advantages for the government, 6 marks each.')],
    kind='fixed', stem=H.q(10, '‘There will be one million people over 65', ' Outline'), **B)
q8c = H.q(10, '‘The number of homeless people increased again in September', ' (i)')
pick('sb-q8-c-i', '3-1', 'why-homelessness-is-rising', ref('B', 8, '(c)(i)'),
     H.q(10, 'Outline one economic reason for the increase in number of homeless people.', ' (ii)'), 'A reason — any one',
     H.split('Growing demand for housing caused', '(ii) State and explain two economic measures',
             ['Growing demand', 'Reduced supply of (social) houses', 'Reduced availability of rental properties', 'Rising rents',
              'Poverty / unemployment', 'High personal debt', 'Central Bank regulations']),
     1, 7, 'One reason, 7 marks.', stem=q8c, **B)
pick('sb-q8-c-ii', '3-1', 'reducing-homelessness', ref('B', 8, '(c)(ii)'),
     H.q(10, 'State and explain two economic measures that could be taken', ' (21 marks)'), 'A measure — any two',
     H.split('Increase supply of (social) housing', '⟨21⟩',
             ['Increase supply of (social) housing', 'Provision of modular housing', 'Repair to and supply of boarded-up',
              'Increased provision of emergency', 'More subsidies for people on low incomes', 'Reduce taxation on construction',
              'New regulations introduced in December 2015', 'Introduce legislation to reduce interest', 'Incentivise investors']),
     2, 7, 'Two measures, 7 marks each (4 + 3).', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
