#!/usr/bin/env python3
"""Economics 2012 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2012-ol-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2012
Ordinary card existed. Section B restarts at Question 1, so every citation
names its section and every id carries it (-sa-, -sb-). Question wording and
stems are sliced from the question paper; every marking point is sliced from
the scheme (econ_legacy_lib.py). A stem stops before any printed table,
formula or diagram: that is the crop beside the typed ask, and printed items a
student must read to answer are typed from the text layer. The only prose
written here is guidance: tariffs, route labels and what a figure or a
calculation shows.

Many answers sit in the scheme's Group / Statement / Explanation tables. Their
table-cell rendering prints each group's statements as one bulleted cell and
its explanations as the next, so each option is "<statement> — <explanation>",
paired by the row the scheme prints them on (`rows_of`).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2012, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2012, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2012-OL-scheme-'
PAP = 'economics-2012-OL-paper-'
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
blanks = lambda t: ' '.join(re.sub(r'\s*_{2,}\s*', ' … ', t).split())
CELLS = [ln.strip() for ln in H.full_md.split('<!-- markbank:table-cells -->', 1)[1]
         .split('<!-- /markbank:table-cells -->', 1)[0].splitlines()]


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def pair(head, body):
    return f'{H.traced(head)} — {H.traced(body)}'


def bullets_of(cell):
    """A cell's own bullets, each traced."""
    return [H.traced(p.strip()) for p in cell.split('•') if p.strip()]


def se(statement):
    """A Statement / Explanation row: the statement cell and the cell after it."""
    i = CELLS.index(statement)
    return f'{H.traced(statement)} — {H.traced(CELLS[i + 1])}'


def rows_of(statements, explanations, rows):
    """One group of a Group / Statement / Explanation table: its statement cell's
    bullets paired with its explanation cell's bullets, row by row as the scheme
    prints them. `rows` lists (statement index, explanation index); a statement
    index of None is an explanation the scheme prints beside no statement."""
    st, ex = bullets_of(cc(statements, whole=True)), bullets_of(cc(explanations, whole=True))
    return [ex[e] if s is None else f'{st[s]} — {ex[e]}' for s, e in rows]


def lined(statements, explanations):
    """A group whose statement cell prints no bullets: each statement read on its
    own, beside the explanation bullet printed level with it (None: none)."""
    ex = bullets_of(explanations)
    if len(ex) != len(statements):
        raise ValueError(f'{len(statements)} statements for {len(ex)} explanations')
    return [e if s is None else f'{H.traced(s)} — {e}' for s, e in zip(statements, ex)]


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def qn(page, anchor, start, end):
    """An ask the page prints more than once, read after a unique anchor before it."""
    text = H.q(page, anchor, end)
    return text[text.index(start):]


def ladder(rid, label, total, options, steps, note):
    return anyN(rid, label, total, len(steps), steps[0], options, note, steps=steps)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ the canons of taxation
add('sa-q1-a', '3-1', 'who-wrote-the-canons-of-taxation', ref('A', 1, '(a)'),
    H.q(2, 'Which of the following economists developed the Canons of Taxation?', ' (b)'), '2', 2,
    [point('r-1', H.traced('Adam Smith'), 2, 'The economist, 2 marks.')], **A)
# The two printed lists follow the ask, each column read down as printed (the text layer
# interleaves them row by row, which would set each canon beside an explanation it is not).
q1_canons = [H.q(2, a, b) for a, b in (('A Equity', ' 1 The'), ('B Certainty', ' 2 The'), ('C Convenience', ' 3 Takes'),
                                       ('D Economy', ' 4 An'))]
q1_expl = [H.q(2, a, b) for a, b in (('1 The tax revenue collected', ' B Certainty'), ('2 The tax should be collected', ' C Convenience'),
                                     ('3 Takes a higher proportion', ' D Economy'), ('4 An individual’s tax bill', ' CANON'))]
q1_canon_h, q1_expl_h = H.q(2, 'Canons Explanation', ' A Equity').split(' ')
add('sa-q1-b', '3-1', 'matching-the-canons-of-taxation', ref('A', 1, '(b)'),
    f"{H.q(2, 'In relation to the following canons of taxation', ' Canons Explanation')} "
    f"{q1_canon_h}: {' '.join(q1_canons)} {q1_expl_h}: {' '.join(q1_expl)}",
    '4 + 4 + 3 + 3', 14,
    [ladder('r-1', 'Each canon matched', 14,
            [pair(c, e) for c, e in (
                ('Equity', 'Takes a higher proportion of an individual’s income in tax as income increases.'),
                ('Certainty', 'An individual’s tax bill should be clear.'),
                ('Convenience', 'The tax should be collected in a way and at a time which accommodates the taxpayer.'),
                ('Economy', 'The tax revenue collected should be greater than the costs of collection.'))],
            [4, 4, 3, 3],
            'All four (the scheme’s answer row: A 3, B 4, C 2, D 1): the first two correct responses 4 marks each, the 3rd and 4th 3 each.')],
    kind='fixed', figure=PAP + 'p02-q1b-table', **A)

# Q2 ─ the cycle-to-work scheme
add('sa-q2', '1-3', 'the-cycle-to-work-scheme', ref('A', 2),
    H.q(2, 'The Irish Government introduced a cycle-to-work scheme', ' (i)'), '12 + 4', 16,
    [ladder('r-1', 'An advantage — any two', 16,
            H.split('1. Possible reduction in traffic congestion.', '1st correct response: 12 marks.',
                    ['Possible reduction in traffic congestion.', 'Reduced fuel emissions', 'Scarce resources saved',
                     'Possible healthier population', 'Reduced carbon emissions', 'Increased demand for bicycles', 'Less congested towns',
                     'Workers have more disposable income', 'It allows people to buy bicycles', 'It allows consumers buy']),
            [12, 4], 'Two advantages: the 1st correct response 12 marks, the 2nd 4.')],
    kind='fixed', **A)

# Q3 ─ labour
add('sa-q3', '2-1', 'labour-and-its-payment', ref('A', 3),
    blanks(H.ask(2, 'Complete the following statement:', ' (16 marks)')), '8 + 4 + 4', 16,
    [ladder('r-1', 'Each word placed', 16, [H.traced('human'), H.traced('goods'), H.traced('wages / salary')], [8, 4, 4],
            'The three words, as the scheme completes the statement: '
            + H.traced('Labour, as a factor of production, is defined as the human effort involved in the production of goods and services.')
            + ' ' + H.traced('The payment for labour is called wages / salary.')
            + ' The 1st correct response 8 marks, the 2nd and 3rd 4 each.')],
    kind='fixed', **A)

# Q4 ─ austerity
add('sa-q4', '3-1', 'effects-of-austerity', ref('A', 4),
    H.q(2, '‘Austerity’ is a consequence of the policy of reducing Government Budget Deficits.', ' Effect 1:'), '12 + 4', 16,
    [ladder('r-1', 'An effect — any two', 16,
            H.split('1. Higher taxes / introduction of new taxes', '1st correct response: 12 marks.',
                    ['Higher taxes / introduction of new taxes', 'Reduced standard of living', 'Increased unemployment',
                     'Increased emigration', 'Increased charges for services', 'Loss of services', 'Lack of confidence in economy']),
            [12, 4], 'Two effects: the 1st correct response 12 marks, the 2nd 4.')],
    kind='fixed', **A)

# Q5 ─ privatisation; the EU and the IMF
add('sa-q5', '1-3', 'privatisation-and-the-eu-imf', ref('A', 5),
    H.q(2, 'The Irish Government is considering privatisation.', ' Explanation:'), '6 + 5 @ 2', 16,
    [point('r-explanation', H.traced('This is the sale of a state / government company to private owners.'), 6,
           'Privatisation explained, 6 marks.'),
     point('r-eu', H.traced('EU: European Union'), 4,
           'EU in full, 4 marks: the scheme prints ' + H.traced('5 at 2 marks each') + ' beneath the five words of the two names, '
           'read here as 2 a word.'),
     point('r-imf', H.traced('IMF: International Monetary Fund.'), 6, 'IMF in full, 6 marks: 2 a word.')],
    kind='fixed', **A)

# Q6 ─ the price elasticity of demand formula
add('sa-q6', '1-4', 'the-ped-formula', ref('A', 6),
    f"{H.q(3, 'The formula for measuring Price Elasticity of Demand is as follows:', ' ∆Q X')} "
    f"{H.q(3, 'Complete the following table to indicate what each of the above symbols stands for:', ' ∆Q Change')}",
    '8 + 3 + 3 + 3', 17,
    [ladder('r-1', 'Each symbol', 17,
            [pair(s, m) for s, m in (('∆P', 'Change in price.'), ('P1', 'Original price.'), ('P2', 'New / Current Price.'),
                                     ('Q2', 'New / current quantity of the good.'))],
            [8, 3, 3, 3], 'The four blank rows: the 1st correct response 8 marks, the 2nd, 3rd and 4th 3 each. The table prints ∆Q '
            'and Q1 already filled in.')],
    kind='fixed', figure=PAP + 'p03-q6-table', **A)

# Q7 ─ alcohol
add('sa-q7', '1-3', 'cutting-alcohol-consumption', ref('A', 7),
    H.q(3, 'The Minister of State in the Department of Health is concerned', ' Action:'), '12 + 5', 17,
    [ladder('r-1', 'One action and one advantage', 17,
            side('One economic action',
                 H.split('1. Taxes: increase taxes', '\nOne Advantage:',
                         ['Taxes:', 'Opening hours:', 'Introduce limits on the amount', 'Age restrictions:', 'Sales points:', 'Sponsorship:',
                          'Café licences:', 'Awareness:', 'Price:']))
            + side('One Advantage',
                   H.split('1. Reduction in absenteeism levels:', '1st correct response: 12 marks.',
                           ['Reduction in absenteeism levels:', 'Reduced pressure on hospitals:', 'Increased productivity:',
                            'Reduction in alcohol related deaths', 'Health /well being:'])),
            [12, 5], 'One action and one advantage, one of each: the 1st correct response 12 marks, the 2nd 5.')],
    kind='fixed', **A)

# Q8 ─ emigration
add('sa-q8', '3-2', 'emigration-and-its-effects', ref('A', 8),
    H.q(3, 'This is one of the effects of the current emigration of Irish citizens.', ' Explanation:'), '11 + 6', 17,
    [ladder('r-1', 'The explanation and one other effect', 17,
            [pair('Explanation', 'Movement of Irish nationals to reside elsewhere / to other countries.')]
            + side('One economic Effect',
                   H.split('1. Loss of skills to the Irish economy', '1st correct response: 11 marks.',
                           ['Loss of skills to the Irish economy', 'Reduction in domestic demand', 'Reduction in unemployment levels',
                            'Loss of confidence in the economy', 'Reduced pressure on state services', 'Loss of revenue to state',
                            'No return on the state’s investment', 'Dependency ratio:'])),
            [11, 6], 'The explanation and one other effect, one of each: the 1st correct response 11 marks, the 2nd 6.')],
    kind='fixed',
    stem=H.q(3, '‘The largest manufacturer of sportswear in Ireland', ' This is one'), **A)

# Q9 ─ the VAT increase
add('sa-q9', '3-1', 'effects-of-the-vat-increase', ref('A', 9),
    H.q(3, 'Outline the possible economic effect which the increase in the VAT rate', ' Cross-border shopping:'), '9 + 4 + 4', 17,
    [ladder('r-1', 'One effect for each — cross-border shopping, employment, the budget deficit', 17,
            [pair('Cross-border shopping', 'May encourage people to go to Northern Ireland and shop resulting in a reduction in VAT revenue '
                                            'collected by government.'),
             pair('Irish employment levels', 'If consumer demand falls it will result in a reduction in employment levels.'),
             pair('Government Budget Deficit', 'Spending falls resulting in a reduction in VAT revenues collected so the budget deficit '
                                                'will increase.'),
             pair('Government Budget Deficit', 'Increased unemployment may lead to increased social welfare, so the budget deficit will '
                                                'increase.')],
            [9, 4, 4], 'One effect for each of cross-border shopping, Irish employment levels and the government budget deficit, one per '
            'group: the 1st correct response 9 marks, the 2nd and 3rd 4 each. The scheme gives two effects on the budget deficit.')],
    kind='fixed', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ imperfect competition; close substitutes; Bord Gáis prices
q1 = H.q(4, 'The diagram below represents the Long Run Equilibrium of a firm in Imperfect Competition.', ' 1 3 2')
q1_fig = PAP + 'p04-q1-diagram'
lines1 = (('1', 'Price', '4 marks.'), ('2', 'Marginal Cost', '4 marks (2 + 2).'), ('3', 'Average Cost', '4 marks (2 + 2).'),
          ('4', 'Average Revenue / Demand', '4 marks (2 + 2).'), ('5', 'Quantity', '4 marks.'))
add('sb-q1-a-i', '2-0', 'lines-of-imperfect-competition', ref('B', 1, '(a)(i)'),
    f"{H.q(4, 'Copy the diagram into your answer book.', ' (i)')} {H.q(4, 'Clearly label each of the lines numbered 1 to 5.', ' (ii)')}",
    '5 @ 4', 20,
    [point(f'r-{n}', f'{n} — {H.traced(name)}', 4, f'Line {n}, {m}') for n, name, m in lines1],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'equilibrium-in-imperfect-competition', ref('B', 1, '(a)(ii)'),
    H.q(4, 'Equilibrium occurs at point E on the diagram.', ' (30 marks)'), '4 + 4 + 2', 10,
    [ladder('r-1', 'Each label shown', 10,
            [H.traced(x) for x in ('Q1 the quantity the firm will produce', 'P1 the price charged for this output',
                                   'C1 the average cost of producing this output')],
            [4, 4, 2], 'All three: the 1st and 2nd correct responses 4 marks each, the 3rd 2. P1 and C1 share one point on the price axis, level with the point above E '
            'where the demand curve touches the average cost curve, as the scheme’s diagram shows.')],
    kind='fixed', stem=q1, figure=SOL + 'p09-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
q1b = H.q(4, 'Firms in imperfect competition produce goods that are close substitutes.', ' (i)')
add('sb-q1-b-i', '2-0', 'close-substitutes', ref('B', 1, '(b)(i)'), H.q(4, 'Explain the underlined term.', ' (ii) State two'), '7', 7,
    [heading('r-1', 'Close substitutes — either',
             [H.traced('a good that can be consumed or used in place of another'),
              H.traced('a good that can be used to satisfy the same need as another good')], 7,
             'The explanation, 7 marks: the scheme accepts either.')],
    kind='fixed', stem=q1b, **B)
pick('sb-q1-b-ii', '2-0', 'characteristics-of-imperfect-competition', ref('B', 1, '(b)(ii)–(iii)'),
     ' '.join([H.q(4, 'State two other characteristics of imperfect competition.', ' (iii)'),
               H.q(4, 'Write brief notes on each of these.', ' (21 marks)')]), 'A characteristic, with its note — any two',
     H.split('There are many buyers.', '2 points at 7 marks each.',
             ['There are many buyers.', 'There are a large number of sellers.', 'No barriers to entry.', 'Almost Perfect knowledge',
              'Each firm tries to maximise profits.', 'Elastic supply of factors of production']),
     2, 7, 'Two characteristics, 7 marks each (4 to state it, 3 for its note): the scheme prices (ii) and (iii) together.',
     stem=q1b, **B)
q1c = H.q(4, 'Bord Gáis increased its electricity prices by 12% in August 2011.', ' (i)')
pick('sb-q1-c-i', '2-0', 'a-rival-electricity-supplier', ref('B', 1, '(c)(i)'),
     H.q(4, 'Name one competitor to Bord Gáis which supplies electricity in Ireland.', ' (ii)'), 'A competitor — any one',
     [H.traced('Electric Ireland'), H.traced('Air Tricity')], 1, 8, 'One competitor, 8 marks.', stem=q1c, **B)
add('sb-q1-c-ii', '1-0', 'effects-of-dearer-electricity', ref('B', 1, '(c)(ii)'),
    H.q(4, 'State and explain one economic effect of this increase in electricity prices', ' (24 marks)'), '8 + 4 + 4', 16,
    [ladder('r-1', 'One effect for each — consumers, other suppliers, the Irish economy', 16,
            rows_of('• Decreased standard of living due to higher prices • Economies in usage • Switching by consumers',
                    '• Resulting from lower disposable income. • Higher prices may result in economy in usage of electricity. '
                    '• Consumers may choose a cheaper/low cost competitor.', [(0, 0), (1, 1), (2, 2)])
            + rows_of('• Price advantage • Employment • Potential price increase',
                      '• Other suppliers may use their price advantage to increase their share of market. • If market share increased they '
                      'may create additional employment. • Other suppliers may increase their prices and so their profits may increase.',
                      [(0, 0), (1, 1), (2, 2)])
            + rows_of('• Inflation • Higher business costs • Export prices increased. • Renewable energies',
                      '• Due to higher energy prices. • Leading to job losses / reduction in spending may lead to job losses in economy. '
                      '• Leading to a reduction in demand. • Move away from oil generated electricity towards alternatives so less '
                      'reliance on imported oil.', [(0, 0), (1, 1), (2, 2), (3, 3)]),
            [8, 4, 4], 'One effect for each group, one per group: the 1st correct response 8 marks (4 to state it, 4 to explain it), '
            'the 2nd and 3rd 4 each (2 + 2). The scheme lists three effects '
            'for consumers of Bord Gáis, then three for other suppliers of electricity, then four for the Irish economy, in that order '
            'here.')],
    kind='fixed', stem=q1c, **B)

# Q2 ─ the ticket market; a shift in demand; motorway tolls
q2a = H.q(5, 'The diagram below shows the demand for match tickets', ' 1 3 Demand')
q2a_fig = PAP + 'p05-q2a-diagram'
add('sb-q2-a-i', '1-0', 'lines-of-the-ticket-market', ref('B', 2, '(a)(i)'),
    H.q(5, 'Copy the diagram into your answer book. Label each of the lines 1 to 3.', ' (ii)'), '3 @ 3', 9,
    [point(f'r-{n}', f'{n} — {H.traced(name)}', 3, f'Line {n}, 3 marks.') for n, name in (('1', 'Price'), ('2', 'Quantity'), ('3', 'Supply'))],
    stem=q2a, figure=q2a_fig, **B)
add('sb-q2-a-ii', '1-0', 'equilibrium-in-the-ticket-market', ref('B', 2, '(a)(ii)'),
    H.q(5, 'Show on your diagram: • equilibrium price', ' (iii)'), '3 + 3', 6,
    [point('r-price', f"{H.traced('Equilibrium price')} — {H.traced('P1')}", 3, 'The equilibrium price, 3 marks.'),
     point('r-quantity', f"{H.traced('Equilibrium quantity')} — {H.traced('Q1')}", 3,
           'The equilibrium quantity, 3 marks: P1 and Q1 read off where the demand curve crosses the vertical supply line, as the '
           'scheme’s diagram shows.')],
    stem=q2a, figure=SOL + 'p12-q2a-diagram', **B)
beside_ask(cards[-1], q2a_fig)
add('sb-q2-a-iii', '1-0', 'a-fixed-supply-of-tickets', ref('B', 2, '(a)(iii)'),
    H.q(5, 'Explain the relationship between the price of tickets and the supply of tickets', ' (21 marks)'), '6', 6,
    [point('r-1', H.traced('As the price of tickets changes the supply of seats remains unchanged / fixed.'), 6, 'The relationship, 6 marks.')],
    stem=q2a, figure=q2a_fig, **B)
q2b = H.q(5, 'Assume the demand for these match tickets shifts to the right as shown below.', ' 3 1')
q2b_fig = PAP + 'p05-q2b-diagram'
factors = (('Income levels', 'If income rises then the demand for tickets will increase.'),
           ('Tastes / Preference', 'If an extensive advertising campaign convinces consumers to purchase Euro 2010 tickets then the demand '
                                   'for tickets will increase.'),
           ('Expectations concerning the future', 'If consumers expect ticket prices to rise in the near future'),
           ('Unplanned events', 'If the Irish team wins its opening match'),
           ('Change in price of substitute good', 'If the price of tickets to an alternative event increased'),
           ('Change in price of complementary gd.', 'If the price of hotel accommodation near the venues'))
add('sb-q2-b-i', '1-1', 'why-ticket-demand-shifts-right', ref('B', 2, '(b)(i)'),
    H.q(5, 'State and explain two possible reasons why the demand curve for these tickets', ' (ii)'), '2 @ 7', 14,
    [anyN('r-1', 'A factor, with how it shifts the curve — any two', 14, 2, 7,
          [f'{cc(f, whole=True)} — {cc(h)}' for f, h in factors],
          'Two reasons, 7 marks each: the scheme prints ' + H.traced('2 at 4 marks each') + ' beneath its factors and '
          + H.traced('2 at 3 marks each') + ' beneath how each shifts the demand curve, read here as 4 for the factor and 3 for how.')],
    kind='fixed', stem=q2b, figure=q2b_fig, **B)
add('sb-q2-b-ii', '1-0', 'demand-shift-and-the-equilibrium-price', ref('B', 2, '(b)(ii)'),
    H.q(5, 'Explain the effect this shift in the demand curve has on the equilibrium price.', ' (iii)'), '8', 8,
    [point('r-1', H.traced('The equilibrium price will increase.'), 8, 'The effect, 8 marks.')], stem=q2b, figure=q2b_fig, **B)
add('sb-q2-b-iii', '1-1', 'a-complement-to-match-tickets', ref('B', 2, '(b)(iii)'),
    H.q(5, 'State one complementary good for these match tickets', ' (30 marks)'), '4 + 2 + 2', 8,
    [heading('r-good', 'A complementary good — any one', [H.traced(x) for x in ('Accommodation', 'Travel Fares', 'Jerseys')], 4,
             'The complementary good, 4 marks.'),
     point('r-effect', H.traced('Will increase'), 2, 'The effect on its demand, 2 marks.'),
     point('r-reason', cc('If demand for tickets continues to increase'), 2, 'The reason, 2 marks.')],
    kind='fixed', stem=q2b, **B)
q2c = H.q(5, 'The government is considering introducing toll charges for more motorways in Ireland.', ' (i)')
tolls = 'Introducing toll charges for more motorways in Ireland'
add('sb-q2-c-i', '1-3', 'for-and-against-motorway-tolls', ref('B', 2, '(c)(i)'),
    H.q(5, 'Outline one possible economic advantage and one possible economic disadvantage', ' (ii)'), '6 + 6', 12,
    [heading('r-advantage', H.traced('Economic advantages') + ' — any one',
             [cc(x) for x in ('Revenue / Profits Operator', 'Possible reduced use of motorways', 'Targeted use of charge',
                              'Jobs created If toll')], 6,
             'One advantage, 6 marks (3 to state it, 3 to explain it).'),
     heading('r-disadvantage', H.traced('Economic disadvantages') + ' — any one',
             [cc(x) for x in ('Reduced standard of living With', 'Use of alternative routes Road', 'Increased transport costs Haulage')], 6,
             'One disadvantage, 6 marks (3 + 3).')],
    kind='fixed', stem=q2c, **B)
add('sb-q2-c-ii', '1-3', 'tolls-for-hauliers-and-the-deficit', ref('B', 2, '(c)(ii)'),
    H.q(5, 'Explain how this development would affect each of the following:', ' (24 marks)'), '6 + 6', 12,
    [heading('r-hauliers', H.traced('Irish Trucking / Haulage Companies') + ' — any one',
             [cc(x) for x in ('Increased costs resulting in a loss', 'Job losses To help', 'Use of alternative routes In')], 6,
             'One effect on trucking and haulage companies, 6 marks (3 + 3).'),
     heading('r-deficit', H.traced('Government’s Current Budget Deficit') + ' — any one',
             [cc(x) for x in ('If revenue accrues to Government', 'If revenue accrues to Operator', 'If employment increases')], 6,
             'One effect on the government’s current budget deficit, 6 marks (3 + 3).')],
    kind='fixed', stem=q2c, **B)

# Q3 ─ costs and profit; enterprise; shopping local
q3a = H.q(6, 'A business must control both its fixed costs and variable costs', ' (i)')
add('sb-q3-a-i', '1-5', 'normal-profit', ref('B', 3, '(a)(i)'), qn(6, 'so that it can earn normal profit.', 'Explain the underlined term.', ' (ii)'), '3', 3,
    [heading('r-1', 'Normal profit — any one',
             [H.traced(x) for x in ('The minimum profit needed to continue in existence.', 'The profit the entrepreneur needs to earn to stay in business.',
                                    'The profit earned when AR = AC.')], 3,
             'The explanation, 3 marks: the scheme accepts any of its three.')],
    kind='fixed', stem=q3a, **B)
fixed, variable = H.traced('Fixed Costs'), H.traced('Variable Costs')
example = H.traced('One correct example')
add('sb-q3-a-ii', '1-5', 'fixed-and-variable-costs', ref('B', 3, '(a)(ii)'),
    H.q(6, 'Define fixed cost and variable cost and state one example of each.', ' (iii)'), '3 + 1 + 2 + 3 + 1 + 2', 12,
    [point('r-fixed', f"{fixed} — {H.traced('costs which do not change')}", 3,
           'The fixed cost definition, 3 marks: the scheme prints ' + H.traced('3 marks') + ' beside “costs which do not change” and '
           + H.traced('1 marks') + ' beside “as output changes”. Its other definition, printed beneath “or”, is read here in the same '
           'two halves.',
           accepts=[H.traced('costs which have to be paid')]),
     point('r-fixed-output', f"{fixed} — {H.traced('as output changes')}", 1, 'As output changes, 1 mark.',
           accepts=[H.traced('even if nothing is produced')]),
     point('r-fixed-example', f'{fixed} — {example}', 2,
           'An example of a fixed cost, ' + H.traced('2 marks') + ': the scheme prints no example.'),
     point('r-variable', f"{variable} — {H.traced('costs which do change')}", 3, 'The variable cost definition, 3 marks.'),
     point('r-variable-output', f"{variable} — {H.traced('as output changes')}", 1, 'As output changes, 1 mark.'),
     point('r-variable-example', f'{variable} — {example}', 2, 'An example of a variable cost, 2 marks: the scheme prints no example.')],
    kind='fixed', stem=q3a, **B)
pick('sb-q3-a-iii', '1-5', 'why-profit-matters', ref('B', 3, '(a)(iii)'),
     H.q(6, 'State and explain two reasons why it is important for a business to earn profit.', ' (25 marks)'), 'A reason — any two',
     H.split('1. Encourages risk taking:', '2 points at 5 marks each.',
             ['Encourages risk taking:', 'Continue production:', 'Fund expansion:', 'Reward innovation:']),
     2, 5, 'Two reasons, 5 marks each (2 to state it, 3 to explain it).', stem=q3a, **B)
q3b = H.q(6, 'The factor of production ‘Enterprise’ combines the other factors of production', ' (i)')
add('sb-q3-b-i', '0-1', 'the-other-factors-of-production', ref('B', 3, '(b)(i)'),
    H.q(6, 'Name the other factors of production referred to above.', ' (ii)'), '4 + 4 + 4', 12,
    [point(f'r-{f.lower()}', H.traced(f), 4, f'{f}, 4 marks.') for f in ('Land', 'Labour', 'Capital')],
    kind='fixed', stem=q3b, **B)
pick('sb-q3-b-ii', '0-1', 'why-entrepreneurs-matter', ref('B', 3, '(b)(ii)'),
     H.q(6, 'Outline two reasons why entrepreneurs are important', ' (iii)'), 'A reason — any two',
     H.split('1. Organise production.', '2 reasons at 5 marks each.',
             ['Organise production.', 'Create Jobs.', 'What commodities will be produced.', 'Encourage further investment.',
              'Place for savers funds.', 'Revenue for the government.', 'Improve the Balance of Payments.', 'Innovation.', 'Creates wealth.']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q3b, **B)
add('sb-q3-b-iii', '0-1', 'encouraging-enterprise', ref('B', 3, '(b)(iii)'),
    H.q(6, 'Outline one action each of the following could take to encourage enterprise:', ' (30 marks)'), '4 + 4', 8,
    [heading('r-government', H.traced('The Irish government') + ' — any one',
             H.split('1. Enterprise education.', '1 point at 4 (2+2) marks.',
                     ['Enterprise education.', 'Taxation policies.', 'Government policies / regulation.', 'Labour market policies.',
                      'Improved economic outlook / confidence in the economy.', 'Development of the state’s infrastructure.',
                      'Improve competitiveness.', 'Availability of bank credit.', 'Government initiatives.']), 4,
             'One action by the Irish government, 4 marks (2 + 2).'),
     heading('r-schools', H.traced('Schools / Colleges') + ' — any one',
             H.split('1. Offer courses / competitions', '1 point at 4 (2+2) marks.',
                     ['Offer courses / competitions', 'Provide R & D assistance', 'Operation space', 'Co-ordinate local business']), 4,
             'One action by schools and colleges, 4 marks (2 + 2).')],
    kind='fixed', stem=q3b, **B)
q3c = H.q(6, 'Businesses throughout Ireland are encouraging consumers to shop local', ' (i)')
pick('sb-q3-c-i', '1-3', 'getting-shoppers-to-shop-local', ref('B', 3, '(c)(i)'),
     H.q(6, 'State and explain two methods a Local Authority could use', ' (ii)'), 'A method — any two',
     H.split('1. Parking facilities / charges', '2 methods at 3 marks each.',
             ['Parking facilities / charges', 'Reduce local authority rates', 'Improve physical environment',
              'Co-ordinate promotions to shop local']),
     2, 3, 'Two methods, 3 marks each (2 to state it, 1 to explain it).', stem=q3c, **B)
pick('sb-q3-c-ii', '1-0', 'benefits-of-shopping-local', ref('B', 3, '(c)(ii)'),
     H.q(6, 'Discuss two benefits to the local economy if more consumers shop locally.', ' (20 marks)'), 'A benefit — any two',
     H.split('1. Jobs\n', '2 benefits at 7 marks each.',
             ['Jobs', 'Increased economic activity', 'Revenue to local authority', 'Better prospects for local business',
              'Optimism / confidence improved', 'Essential services continued', 'Community spirit']),
     2, 7, 'Two benefits, 7 marks each (4 to state it, 3 to explain it).', stem=q3c, **B)

# Q4 ─ money and barter; growth and the ECB; inflation and the CPI
q4a = H.q(6, '‘Barter’ and ‘money’ are used as mediums of exchange.', ' (i)')
pick('sb-q4-a-i', '3-4', 'characteristics-of-money', ref('B', 4, '(a)(i)'), H.q(6, 'Explain any two of the underlined terms.', ' (ii)'),
     'A term — any two',
     [pair(t, e) for t, e in (('Relatively scarce', 'It should be limited in supply (in relation to the demand).'),
                              ('Portable', 'It should be easy to carry around.'),
                              ('Durable', 'It should be capable of withstanding a lot of handling.'))],
     2, 5, 'Two terms, 5 marks each. The underlined terms are relatively scarce, portable and durable.',
     stem=q4a, **B)
pick('sb-q4-a-ii', '3-4', 'the-difficulty-of-barter', ref('B', 4, '(a)(ii)'),
     H.q(6, 'Outline the difficulty of using ‘barter’ as a medium of exchange.', ' (iii)'), 'A difficulty — any one',
     [pair('Establishing Value', 'It can be difficult to put a precise value on items.'),
      pair('Time consuming / Double coincidence of wants', 'It takes time to find who has what you want and wants what you have.')],
     1, 5, 'One difficulty, 5 marks (2 to state it, 3 to explain it).', stem=q4a, **B)
pick('sb-q4-a-iii', '3-4', 'functions-of-money', ref('B', 4, '(a)(iii)'),
     H.q(6, 'Explain two functions of money other than a ‘medium of exchange’.', ' (25 marks)'), 'A function — any two',
     [pair(t, e) for t, e in (('Measure of Value', 'Money enables a value/price to be put on goods & services.'),
                              ('Store of Wealth', 'Allows people to save for the future.'),
                              ('Standard for Deferred Payment', 'Money is capable of measuring value for a future date.'),
                              ('Standard for Deferred Payment', 'Money makes credit trading (i.e. buying & selling) possible.'))],
     2, 5, 'Two functions, 5 marks each (2 to state it, 3 to explain it). The scheme gives two explanations of a standard for deferred payment; they are one function.', stem=q4a, **B)
q4b = H.q(6, 'The ECB decreased interest rates in 2011 with the aim of increasing economic growth.', ' (i)')
add('sb-q4-b-i', '3-5', 'economic-growth', ref('B', 4, '(b)(i)'), qn(6, 'with the aim of increasing economic growth.', 'Explain the underlined term.', ' (ii)'),
    '6', 6, [point('r-1', H.traced('Economic Growth: an increase in GNP per head.'), 6, 'The explanation, 6 marks.')], stem=q4b, **B)
add('sb-q4-b-ii', '3-3', 'ecb-in-full', ref('B', 4, '(b)(ii)'), H.q(6, 'What do the initials ECB stand for?', ' (iii)'), '7', 7,
    [point('r-1', H.traced('European Central Bank'), 7, 'The name, 7 marks.')], stem=q4b, **B)
pick('sb-q4-b-iii', '3-5', 'effects-of-faster-growth', ref('B', 4, '(b)(iii)'),
     H.q(6, 'State and explain two possible economic effects which an increase in economic growth', ' (25 marks)'), 'An effect — any two',
     H.split('Increased employment\nA rise', '2 points at 6 marks each.',
             ['Increased employment', 'Increased exports', 'Increased imports', 'Improved standard of living', 'Inflation',
              'Effects on Emigration', 'Investment opportunities', 'Government Finances']),
     2, 6, 'Two effects, 6 marks each (3 to state it, 3 to explain it).', stem=q4b, **B)
q4c = H.q(6, 'One measure of price inflation is the CPI.', ' (i)')
add('sb-q4-c-i', '3-3', 'price-inflation', ref('B', 4, '(c)(i)'), qn(6, 'One measure of price inflation is the CPI.', 'Explain the underlined term.', ' (ii)'),
    '4', 4,
    [heading('r-1', 'Price inflation — either',
             [H.traced('An increase in prices of goods / services over a period of time.'),
              H.traced('A decrease in the value of money / people buy less with their money.')], 4,
             'The explanation, 4 marks: the scheme accepts either.')],
    kind='fixed', stem=q4c, **B)
add('sb-q4-c-ii', '3-3', 'cpi-in-full', ref('B', 4, '(c)(ii)'), H.q(6, 'What do the initials CPI stand for?', ' (iii)'), '6', 6,
    [point('r-1', H.traced('Consumer Price Index'), 6, 'The name, 6 marks.')], stem=q4c, **B)
add('sb-q4-c-iii', '3-3', 'effects-of-falling-inflation', ref('B', 4, '(c)(iii)'),
    H.q(6, 'Explain how a fall in the rate of price inflation may affect each of the following:', ' (25 marks)'), '7 + 4 + 4', 15,
    [ladder('r-1', 'One effect for each — employees, people on social welfare, business', 15,
            # These statement cells print no bullets, so each statement is read on its own; the
            # explanation cells' bullets are paired with the statement printed level with them.
            lined(['Increased disposable income/ higher standard of living', 'Increased disposable income/ higher standard of living',
                   'Reduced wage demands', 'Discourage spending'], cc('• Employees may increase spending'))
            + lined(['Lower cost of living', 'Improved standard of living', None], cc('• The cost of living would decrease'))
            + lined(['Lower costs of production', 'Continuity of production', 'Expand / Innovate', 'Increase employment/pay'],
                    cc('• Business may be able to increase its profits.')),
            [7, 4, 4], 'One effect for each group, one per group: the 1st correct response 7 marks (4 to state it, 3 to explain it), '
            'the 2nd and 3rd 4 each (2 + 2). The scheme lists four '
            'effects for employees (its first statement carries two explanations), then three for people in receipt of social welfare '
            '(its last explanation sits beside no statement), then four for business, in that order here, each statement beside the '
            'explanation printed level with it.')],
    kind='fixed', stem=q4c, **B)

# Q5 ─ transfer payments; the open-economy multiplier; the black economy
q5a = H.q(7, 'Social welfare payments and student grants are examples of transfer payments.', ' (i)')
add('sb-q5-a-i', '3-0', 'transfer-payments', ref('B', 5, '(a)(i)'), qn(7, 'are examples of transfer payments.', 'Explain the underlined term.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Income received by a factor of production when no factor had been supplied.'), 6, 'The explanation, 6 marks.')],
    stem=q5a, **B)
add('sb-q5-a-ii', '3-0', 'why-transfers-are-left-out', ref('B', 5, '(a)(ii)'),
    H.q(7, 'Explain why transfer payments are not included in National Income.', ' (iii)'), '5', 5,
    [heading('r-1', 'Why — any one',
             [H.traced(x) for x in ('Including this figure would lead to double counting.',
                                    'This amount was already included in the calculation of national income when the income received by '
                                    'the original factor was counted.',
                                    'To include them would mean that national income was over estimated.')], 5,
             'The explanation, 5 marks: the scheme gives three explanations.')],
    kind='fixed', stem=q5a, **B)
pick('sb-q5-a-iii', '3-0', 'uses-of-national-income-statistics', ref('B', 5, '(a)(iii)'),
     H.q(7, 'State and explain two possible uses of National Income Statistics.', ' (25 marks)'), 'A use — any two',
     H.split('Changes in the level of economic growth\nThe', '2 points at 7 marks each.',
             ['Changes in the level of economic growth', 'Changes in standard of living', 'Changes to employment levels',
              'International comparisons', 'Distribution of income', 'Contribution of government']),
     2, 7, 'Two uses, 7 marks each (4 to state it, 3 to explain it).', stem=q5a, **B)
q5b = H.q(7, 'The Multiplier formula for an open economy is:', ' 1 MPS')
q5b_fig = PAP + 'p07-q5b-formula'
q5b_data = H.q(7, 'Assume that MPM is 0.2 and MPS is 0.3.', ' (i)')
add('sb-q5-b-i', '3-0', 'the-multiplier-and-an-open-economy', ref('B', 5, '(b)(i)'),
    H.q(7, 'Explain each of the above underlined terms.', ' (ii)'), '6 + 6', 12,
    [point('r-multiplier', H.traced('The multiplier tells us by how much national income increases for any given injection into the economy.'), 6,
           'The multiplier, 6 marks.'),
     point('r-open', H.traced('An open economy is one which engages in trade / imports and exports.'), 6, 'An open economy, 6 marks.')],
    kind='fixed', stem=q5b, figure=q5b_fig, **B)
add('sb-q5-b-ii', '3-0', 'calculating-the-open-multiplier', ref('B', 5, '(b)(ii)'),
    f"{q5b_data} {H.q(7, 'Calculate, using the above formula, the size of the Multiplier.', ' (20 marks)')}", '8', 8,
    [point('r-1', 'The multiplier — ' + H.traced('2'), 8,
           'The multiplier, ' + H.traced('8 marks') + ': 1 over (0.3 + 0.2) = 2. The working is shown with the answer.')],
    kind='fixed', stem=q5b, figure=SOL + 'p24-q5bii-working', **B)
beside_ask(cards[-1], q5b_fig)
q5c = H.q(7, 'The Irish government is concerned about the size of the ‘black economy’.', ' (i)')
add('sb-q5-c-i', '3-0', 'the-black-economy', ref('B', 5, '(c)(i)'), qn(7, 'concerned about the size of the ‘black economy’.', 'Explain the underlined term.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Economic activity which takes place which is not recorded and therefore not included in national income accounts.'), 6,
           'The explanation, 6 marks.')], stem=q5c, **B)
pick('sb-q5-c-ii', '3-0', 'black-economy-activities', ref('B', 5, '(c)(ii)'),
     H.q(7, 'State two examples of activities considered part of the black economy.', ' (iii)'), 'An example — any two',
     [H.traced('A teacher giving grinds without declaring the income for tax purposes.'),
      H.traced('A plumber working for cash payment and not declaring the income for tax purposes.')],
     2, 6, 'Two examples, 6 marks each: the scheme’s two.', stem=q5c, **B)
pick('sb-q5-c-iii', '3-1', 'discouraging-the-black-economy', ref('B', 5, '(c)(iii)'),
     H.q(7, 'State and explain two actions the Irish Government could take to discourage', ' (30 marks)'), 'An action — any two',
     H.split('1. Reduce direct taxation.', '2 at 6 marks. State: 3 marks. Explain: 3 marks.',
             ['Reduce direct taxation.', 'Reduce indirect taxation.', 'Better enforcement by revenue commissioners', 'Educate the public',
              'Increase penalties for offenders.']),
     2, 6, 'Two actions, 6 marks each (3 to state it, 3 to explain it).', stem=q5c, **B)

# Q6 ─ the Live Register; infrastructure; energy grants
q6a = H.q(7, 'One of the main economic aims of the Irish Government is to reduce the number', ' (i)')
add('sb-q6-a-i', '3-2', 'the-live-register', ref('B', 6, '(a)(i)'), qn(7, 'to reduce the number on the Live Register.', 'Explain the underlined term.', ' (ii)'),
    '5', 5,
    [point('r-1', H.traced('Those people who sign stating they are unemployed and receive social welfare payments.'), 5, 'The explanation, 5 marks.')],
    stem=q6a, **B)
pick('sb-q6-a-ii', '3-2', 'a-shorter-live-register', ref('B', 6, '(a)(ii)'),
     H.q(7, 'Outline two economic advantages to the economy if the number on the Live Register', ' (iii)'), 'An advantage — any two',
     H.split('1. Increased standard of living:', '2 points at 5 marks each.',
             ['Increased standard of living:', 'Government Finances:', 'Emigration decreases:', 'Investment climate improves:',
              'Economic growth:']),
     2, 5, 'Two advantages, 5 marks each (2 + 3).', stem=q6a, **B)
pick('sb-q6-a-iii', '3-1', 'the-governments-other-aims', ref('B', 6, '(a)(iii)'),
     H.q(7, 'State and explain three other economic aims of the Irish Government.', ' (30 marks)'), 'An aim — any three',
     H.split('1. Price inflation.', '3 at 5 marks each.',
             ['Price inflation.', 'Economic growth.', 'Encourage exports.', 'Control government finances.',
              'Achieve taxation equity / broaden the tax base.', 'Regional development.', 'Improve state services.',
              'Equitable distribution of income.', 'Improve infrastructure.', 'Reduce the national debt.', 'Bank stability.',
              'Restore consumer confidence.']),
     3, 5, 'Three aims, 5 marks each (2 to state it, 3 to explain it).', stem=q6a, **B)
q6b = H.q(7, 'The Irish Government reduced capital expenditure on infrastructure', ' (i)')
add('sb-q6-b-i', '3-1', 'infrastructure', ref('B', 6, '(b)(i)'), qn(7, 'by approximately €750m in its 2012 budget.', 'Explain the underlined term.', ' (ii)'), '5', 5,
    [heading('r-1', 'Infrastructure — any one',
             [H.traced(x) for x in ('Goods /services which are essential for the smooth running of an economy.',
                                    'Goods /services which industry requires to function properly.',
                                    'Capital equipment used to supply publicly available services.')], 5,
             'The explanation, 5 marks: the scheme accepts any of its three.')],
    kind='fixed', stem=q6b, **B)
pick('sb-q6-b-ii', '3-1', 'cutting-capital-spending', ref('B', 6, '(b)(ii)'),
     H.q(7, 'Outline three economic effects which this reduction in capital expenditure', ' (20 marks)'), 'An effect — any three',
     H.split('1. Reduced government borrowing', '3 at 5 marks each.',
             ['Reduced government borrowing', 'Postponement of infrastructural development', 'Employment depressed',
              'Deterioration in existing infrastructure']),
     3, 5, 'Three effects, 5 marks each (2 + 3).', stem=q6b, **B)
q6c = H.q(7, 'The Irish Government provided grants towards energy improvements', ' (i)')
add('sb-q6-c-i', '0-1', 'opportunity-cost', ref('B', 6, '(c)(i)'), qn(7, 'these grants involved an opportunity cost.', 'Explain the underlined term.', ' (ii)'), '7', 7,
    [heading('r-1', 'Opportunity cost — either',
             [H.traced('The cost of foregone alternatives.'), H.traced('The cost of passing up the next best alternative when making a decision.')], 7,
             'The explanation, 7 marks: the scheme accepts either.')],
    kind='fixed', stem=q6c, **B)
grants = (('households', 'Individual households', 'individual households',
           rows_of('• Reduced spending on energy • Improved standard of living • Higher BER rating • Cheaper to improve home',
                   '• Better insulation will reduce energy consumption / result in higher disposable income. • Warmer homes will improve '
                   'the quality of lives. • Value of property may increase. • As it is more affordable more people may avail of the '
                   'facility.', [(0, 0), (1, 1), (2, 2), (3, 3)])),
          ('businesses', 'Businesses', 'businesses',
           rows_of('• Increased demand for products • Employment opportunities • Opportunities for innovation',
                   '• Increased sales / profits – better future prospects. • If sales increase more workers will be required. • Firms may '
                   'develop new/better ways of improving energy performance in homes.', [(0, 0), (1, 1), (2, 2)])),
          ('economy', 'The Irish economy', 'the Irish economy',
           rows_of('• Increased economic growth • Government finances • Improved energy efficiency',
                   '• Spending increases with demand / national income increasing. • Government will pay out more. • Opportunity cost: '
                   'government have less money to spend on other projects. • Increased spending will lead to increased VAT revenues. '
                   '• Increased employment will increase income tax revenue and reduce social welfare spending. • Will result in reduced '
                   'carbon emissions and less damage to the environment.', [(0, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 5)])))
add('sb-q6-c-ii', '1-3', 'effects-of-home-energy-grants', ref('B', 6, '(c)(ii)'),
    H.q(7, 'Discuss one economic effect which these grants have for each of the following:', ' (25 marks)'), '3 @ 6 (3 + 3)', 18,
    [heading(f'r-{rid}', H.traced(g) + ' — any one', opts, 6,
             f'One effect for {name}, 6 marks (3 to state it, 3 to explain it).'
             + (' The scheme gives four explanations beside government finances.' if rid == 'economy' else ''))
     for rid, g, name, opts in grants],
    kind='fixed', stem=q6c, **B)

# Q7 ─ comparative advantage; invisible imports and exports; MNCs
q7a = f"{H.q(8, 'The table below illustrates the Law of Comparative Advantage.', ' Country')} {H.q(8, 'Although Germany is more efficient', ' (i)')}"
q7a_table = PAP + 'p08-q7a-table'
add('sb-q7-a-i', '4-2', 'what-germany-should-produce', ref('B', 7, '(a)(i)'),
    H.q(8, 'Which good will Germany produce? Explain briefly.', ' (ii)'), '4 + 3', 7,
    [point('r-good', H.traced('It should produce Cars.'), 4, 'The good, 4 marks.'),
     point('r-why', H.traced('It is three times more efficient than France in the production of cars.'), 3, 'Why, 3 marks.')],
    kind='fixed', stem=q7a, figure=q7a_table, **B)
add('sb-q7-a-ii', '4-2', 'what-france-should-produce', ref('B', 7, '(a)(ii)'),
    H.q(8, 'Which good will France produce? Explain briefly.', ' (iii)'), '4 + 1', 5,
    [point('r-good', H.traced('It should produce Wine.'), 4, 'The good, 4 marks.'),
     point('r-why', H.traced('It is least inefficient in the production of wine than in car production.'), 1, 'Why, 1 mark.')],
    kind='fixed', stem=q7a, figure=q7a_table, **B)
add('sb-q7-a-iii', '4-2', 'output-after-specialising', ref('B', 7, '(a)(iii)'),
    H.q(8, 'If each country specialises in the good you have selected', ' (20 marks)'), '3 + 3 + 2', 8,
    [point('r-germany', f"{H.traced('Germany')} — {H.traced('Cars')} — {H.traced('1200* x 2* = 2400*')}", 3,
           'Germany’s cars, ' + H.traced('3 figures x 1 mark each') + ': the scheme stars each figure that earns a mark. Germany makes '
           'no wine.'),
     point('r-france', f"{H.traced('France')} — {H.traced('Wine')} — {H.traced('800* x 2* = 1600*')}", 3,
           'France’s wine, 3 figures at 1 mark each. France makes no cars.'),
     point('r-total', f"{H.traced('Total Output')} — {H.traced('1600*')} — {H.traced('2400*')}", 2,
           'The total output, 1600 litres of wine and 2400 units of cars, ' + H.traced('2 figures x 1 marks each') + ' ('
           + H.traced('8 marks: 8 workings at 1 mark each') + '). The working is shown with the answer.')],
    kind='fixed', stem=q7a, figure=SOL + 'p29-q7aiii-working', **B)
beside_ask(cards[-1], q7a_table)
q7b = H.q(8, 'Irish people attending the Olympic Games in London 2012', ' (i)')
add('sb-q7-b-i', '4-2', 'invisible-imports', ref('B', 7, '(b)(i)'),
    H.q(8, 'Explain the underlined term and state one other example of an invisible import.', ' (ii)'), '6 + 4', 10,
    [point('r-explanation', H.traced('The purchase of foreign services by Irish consumers / money leaves Ireland.'), 6,
           'The explanation, 6 marks.'),
     heading('r-example', 'Another example — any one',
             [H.traced(x) for x in ('Irish people using foreign financial services.', 'Foreign rock groups performing in Ireland.',
                                    'Ryanair using maintenance crews in countries outside Ireland.')], 4,
             'One other example, 4 marks.')],
    kind='fixed', stem=q7b, **B)
pick('sb-q7-b-ii', '4-2', 'benefits-of-more-exports', ref('B', 7, '(b)(ii)'),
     H.q(8, 'Discuss three benefits to the Irish economy of increasing exports.', ' (25 marks)'), 'A benefit — any three',
     H.split('1. Employment creation.', '15 marks: 3 points at 5 marks each.',
             ['Employment creation.', 'Increased GNP / Economic growth.', 'Increased sales / profits.', 'Earn foreign currencies.',
              'Attract investment.', 'Government finances.']),
     3, 5, 'Three benefits, 5 marks each (2 to state it, 3 to explain it).', stem=q7b, **B)
q7c = H.q(8, 'IDA Ireland has been successful in attracting investment', ' (i)')
pick('sb-q7-c-i', '4-1', 'mncs-in-ireland', ref('B', 7, '(c)(i)'), H.q(8, 'Name two MNCs in Ireland.', ' (ii)'), 'An MNC — any two',
     [H.traced(x) for x in ('Google', 'Facebook', 'Pfizer', 'Coca Cola', 'Intel', 'Apple', 'Kerry Group', 'Dell', 'IBM', 'Microsoft',
                            'CRH')],
     2, 5, 'Two companies, 5 marks each.', stem=q7c, **B)
pick('sb-q7-c-ii', '4-1', 'why-mncs-come-to-ireland', ref('B', 7, '(c)(ii)'),
     H.q(8, 'State and explain two reasons why MNCs are attracted to Ireland.', ' (iii)'), 'A reason — any two',
     H.split('1. Availability of educated workforce.', '2 reasons at 5 marks each',
             ['Availability of educated workforce.', 'Low rates of taxation.', 'Access to EU market / Member of the euro currency.',
              'Availability of state incentives.', 'Good industrial relations.', 'Attractive rates of return on investments.']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q7c, **B)
pick('sb-q7-c-iii', '4-1', 'advantages-of-mncs', ref('B', 7, '(c)(iii)'),
     H.q(8, 'Discuss two economic advantages to the Irish economy of MNCs locating here.', ' (30 marks)'), 'An advantage — any two',
     [se(x) for x in ('Employment should increase', 'Exports will increase', 'Taxation revenue will increase', 'Economic activity will increase',
                      'Attract investment', 'Benefits to local economy')],
     2, 5, 'Two advantages, 5 marks each (2 + 3).', stem=q7c, **B)

# Q8 ─ terms; the 2012 taxes; the national debt
pick('sb-q8-a', '3-1', 'four-economic-terms', ref('B', 8, '(a)'),
     H.q(9, 'Explain any three of the following:', ' (21 marks)'), 'A term — any three',
     [pair(t, e) for t, e in (('Current Budget Deficit', 'Government current spending exceeds government current income.'),
                              ('Progressive Tax', 'A tax which takes a higher proportion of income in tax as income rises.'),
                              ('Nationalisation', 'Taking a privately owned business into government ownership.'),
                              ('Economic recession', 'A decline in GDP for two or more consecutive quarters.'))],
     3, 7, 'Three terms, 7 marks each.', **B)
q8b = H.q(9, 'An increased rate of VAT, increased carbon taxes', ' (i)')
add('sb-q8-b-i', '3-1', 'vat-carbon-tax-and-the-household-charge', ref('B', 8, '(b)(i)'),
    H.q(9, 'Explain each of the underlined taxes.', ' (ii)'), '3 @ 5', 15,
    [point(f'r-{rid}', H.traced(t), 5, f'{name}, 5 marks.') for rid, name, t in (
        ('vat', 'VAT', 'VAT: tax placed on goods and services / on spending.'),
        ('carbon', 'Carbon taxes', 'Carbon taxes: an environmental tax levied on the carbon content of fuels.'),
        ('household', 'The household charge', 'Household charge: an annual charge which is payable by owners of residential property.'))],
    kind='fixed', stem=q8b, **B)
taxes = (('households', 'Households', 'households',
          rows_of('• Standard of living • Reduced incentive to work • Incentive to become energy efficient • Black economy • Reduced '
                  'productivity • Financial difficulties',
                  '• Decreases due to lower disposable income. • Taxpayers may choose not to work. • Consumers may become more energy '
                  'efficient and insulate; change to more energy efficient cars. • To avoid higher VAT charges people may buy commodities '
                  'on the black market. • Deterioration in health due to financial difficulties may reduce productivity. • Some may '
                  'struggle to meet their financial commitments and may be forced to rely on state aid.',
                  [(i, i) for i in range(6)])),
         ('retailers', 'Retailers in Ireland', 'retailers in Ireland',
          rows_of('• Reduced sales • Job losses • Possible closure • Need to compete',
                  '• Resulting in reduced profits. • With reduced sales workers may be let go. • If sales fall to unacceptable levels '
                  'businesses may be forced to close e.g. GAME stores. • Retailers may reduce prices / improve services to attract customers.',
                  [(i, i) for i in range(4)])),
         ('deficit', 'Government’s Current Budget Deficit', 'the government’s current budget deficit',
          rows_of('• Increased indirect tax revenue • Spending falls • Business activity declines',
                  '• So Current Budget Deficit (CBD) should fall. • If the VAT increase leads to reduced spending then VAT revenue will '
                  'fall and CBD will rise. • Employment will fall and hence direct tax revenue will fall and CBD will rise.',
                  [(i, i) for i in range(3)])))
add('sb-q8-b-ii', '3-1', 'effects-of-the-2012-tax-increases', ref('B', 8, '(b)(ii)'),
    H.q(9, 'Discuss one economic effect which these tax increases will have', ' (30 marks)'), '3 @ 5 (2 + 3)', 15,
    [heading(f'r-{rid}', H.traced(g) + ' — any one', opts, 5,
             f'One effect for {name}, 5 marks (2 to state it, 3 to explain it).')
     for rid, g, name, opts in taxes],
    kind='fixed', stem=q8b, **B)
q8c = H.q(9, 'One of the functions of the NTMA is to manage Ireland’s National Debt', ' (i)')
add('sb-q8-c-i', '3-1', 'ntma-in-full', ref('B', 8, '(c)(i)'), H.q(9, 'What do the initials NTMA stand for?', ' (ii)'), '8', 8,
    [point('r-1', H.traced('National Treasury Management Agency'), 8, 'The name, 8 marks.')], stem=q8c, **B)
add('sb-q8-c-ii', '3-1', 'the-national-debt', ref('B', 8, '(c)(ii)'), H.q(9, 'Explain the underlined term.', ' (iii)'), '6', 6,
    [point('r-1', H.traced('The total amount / cumulative of government /borrowing which is outstanding/ due /owed.'), 6,
           'The explanation, 6 marks.')], stem=q8c, **B)
pick('sb-q8-c-iii', '3-1', 'disadvantages-of-the-national-debt', ref('B', 8, '(c)(iii)'),
     H.q(9, 'State and explain two economic disadvantages of Ireland’s National Debt.', ' (24 marks)'), 'A disadvantage — any two',
     H.split('1. Opportunity costs involved.', '2 points at 5 marks each.',
             ['Opportunity costs involved.', 'Increased burden on taxpayers.', 'Annual interest repayments.',
              'Risk to provision of public services / cuts in government spending.', 'Reduced public confidence.',
              'Diminished international credit-rating.', 'EU / IMF: conditions applied to Ireland.']),
     2, 5, 'Two disadvantages, 5 marks each (2 to state it, 3 to explain it).', stem=q8c, **B)

# A short ask the paper prints for several parts ("Explain the underlined term.") would
# read the same on every card, and the deck refuses two cards asking one question: each
# carries its stem in its question instead, as 2013 OL does.
_asked = [' '.join(c['questionText'].split()).lower() for c in cards]
for c in cards:
    if _asked.count(' '.join(c['questionText'].split()).lower()) > 1 and c.get('stem'):
        c['questionText'], c['stem'] = f"{c['stem']} {c['questionText']}", ''

if __name__ == '__main__':
    emit(cards)
