#!/usr/bin/env python3
"""Economics 2013 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2013-ol-ev.json, made
from a visual sweep of all 12 paper pages and 40 scheme pages before any 2013
Ordinary card existed. Section B restarts at Question 1, so every citation
names its section and every id carries it (-sa-, -sb-). Question wording and
stems are sliced from the question paper; every marking point is sliced from
the scheme (econ_legacy_lib.py). The scheme's cover is in Irish
("Gnáthleibhéal") although the scheme is the English one, so its scheme file
was built with the appenders' cover check pointed at the file. A stem stops
before any printed table: the table is the crop beside the typed ask, and
printed items a student must read to answer are typed from the text layer.
The only prose written here is guidance: tariffs, route labels and what a
figure or a calculation shows.

Many answers sit in the scheme's two-column Statement / Explanation tables.
Their table-cell rendering prints each statement cell on its own line with
its explanation on the next (`se`), so each option is "<statement> — <explanation>".
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

H = Old(2013, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2013, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2013-OL-scheme-'
PAP = 'economics-2013-OL-paper-'
bl = H.bullets
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
blanks = lambda t: ' '.join(re.sub(r'\s*_{2,}\s*', ' … ', t).split())
CELLS = [ln.strip() for ln in H.full_md.split('<!-- markbank:table-cells -->', 1)[1]
         .split('<!-- /markbank:table-cells -->', 1)[0].splitlines()]


def se(statement, after=None):
    """A Statement / Explanation row: the statement cell and the cell after it.
    `after`: a cell of the same table printed before it, where an earlier table
    prints the same statement ("Increased VAT rates", "Unemployment")."""
    i = CELLS.index(statement, CELLS.index(after) if after else 0)
    return f'{H.traced(statement)} — {H.traced(CELLS[i + 1])}'


def unnum(cell):
    """A cell read without the scheme's own list numeral ("1. ")."""
    return H.traced(re.sub(r'^\d\.\s+', '', cell))


def bullets_of(cell):
    """A cell's own bullets, each traced."""
    return [H.traced(p.strip()) for p in cell.split('•') if p.strip()]


def side(label, options):
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def numbered(cell, firsts):
    """A cell listing "1. Head Body 2. Head Body …", cut at each numbered head."""
    out = []
    for k, f in enumerate(firsts):
        a = cell.index(f'{k + 1}. {f}')
        b = cell.index(f'{k + 2}. {firsts[k + 1]}') if k + 1 < len(firsts) else len(cell)
        out.append(H.traced(cell[a + len(f'{k + 1}. '):b].strip()))
    return out


def ladder(rid, label, total, options, steps, note):
    return anyN(rid, label, total, len(steps), steps[0], options, note, steps=steps)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ factors of production
add('sa-q1', '0-1', 'factors-and-their-examples', ref('A', 1),
    H.q(2, 'Write, in the blank spaces below, which factor of production', ' Carpenter'), '6 + 6 + 2 + 2', 16,
    [ladder('r-1', 'Each factor’s example', 16,
            [f'{H.traced(f)} — {H.traced(x)}' for f, x in (('LAND', 'Natural Gas'), ('LABOUR', 'Carpenter'), ('CAPITAL', 'Buildings'),
                                                ('ENTERPRISE', 'Business Owner'))],
            [6, 6, 2, 2], 'All four: ' + H.traced('2 at 6 marks + 2 at 2 marks') + ', the first two correct 6 each.')],
    kind='fixed', figure=PAP + 'p02-q1-table', **A)

# Q2 ─ the supply of a firm: true or false
# The scheme reprints the sentences beside its answers ((iv) as "the company’s production technology").
s2 = (('(i) The price of the good itself.', 'TRUE'), ('(ii) The cost of labour.', 'TRUE'),
      ('(iii) The consumer’s taste / preference for the good.', 'FALSE'), ('(iv) The state of the company’s production technology.', 'TRUE'))
add('sa-q2', '1-2', 'what-shifts-a-firms-supply', ref('A', 2, '(i)–(iv)'),
    f"{H.q(2, 'Some of the factors outlined below influence the supply', ' SENTENCE')} "
    f"{H.q(2, '(i) The price of the good itself.', ' (16 marks)')}", '6 + 6 + 2 + 2', 16,
    [ladder('r-1', 'Each sentence marked', 16,
            [f'{H.traced(a)} — {H.traced(s)}' for s, a in s2], [6, 6, 2, 2],
            'All four: ' + H.traced('2 at 6 marks + 2 at 2 marks') + ', the first two correct 6 each. The scheme prints (iv) '
            'as “the company’s production technology”.')],
    kind='fixed', **A)

# Q3 ─ online purchasing
add('sa-q3', '1-1', 'online-purchasing', ref('A', 3),
    H.q(2, 'Outline one reason for this development and state one economic effect', ' Reason:'), '10 + 6', 16,
    [heading('r-reason', 'A reason — any one',
             H.split('1. Greater choice:', '\nEconomic effect:', ['Greater choice:', 'Increased use by retailers:', 'Competitive prices:',
                                                                 'Consumer confidence:', 'Convenience:', 'Broadband access:']), 10,
             'One reason, 10 marks: the scheme prices the reason and the effect ' + H.traced('10 marks + 6 marks') + '.'),
     heading('r-effect', 'An effect for retailers — any one',
             H.split('1. Possible increased sales:', '10 marks + 6 marks',
                     ['Possible increased sales:', 'Reduced costs:', 'Possible reduced sales:', 'Reduced staff numbers:',
                      'Business investment in online business']), 6, 'One effect, 6 marks.')],
    kind='fixed', stem=H.q(2, 'Online purchasing (i.e. using the internet)', ' Outline one'), **A)

# Q4 ─ Keynes's motives
motives = (('Transactionary', 'Cash is needed to buy goods and services'), ('Precautionary', 'Cash is needed for emergencies'),
           ('Speculative', 'Cash is needed to take advantage of possible profitable'))
add('sa-q4', '3-4', 'keynes-motives', ref('A', 4),
    f"{H.q(2, 'John Maynard Keynes stated that people have three motives', ' Transactionary')} Transactionary Precautionary Speculative",
    '10 + 3 + 3', 16,
    [ladder('r-1', 'Each motive explained', 16, [f'{H.traced(m)} — {cc(e)}' for m, e in motives], [10, 3, 3],
            'All three: ' + H.traced('10 marks+3 marks + 3 marks') + ', claimed in the order the answers are correct.')],
    kind='fixed', **A)

# Q5 ─ aid to LDCs
add('sa-q5', '4-0', 'falling-aid-to-ldcs', ref('A', 5),
    H.q(2, 'There has been a decline in financial aid donated by Irish citizens', ' Reason:'), '10 + 6', 16,
    [heading('r-reason', 'A reason — any one',
             H.split('1. Unemployment: People', '\nEconomic effect:', ['Unemployment:', 'Decreased incomes:', 'Concern about the destination of the aid:',
                                                                    'Concern about administration expenses:']), 10,
             'One reason, 10 marks: ' + H.traced('10 marks + 6 marks') + '.'),
     heading('r-effect', 'An effect for the citizens of LDCs — any one',
             H.split('1. Reduced standard of living', '10 marks + 6 marks',
                     ['Reduced standard of living', 'Deterioration in infrastructure', 'Increased poverty / famine', 'Increased death rates',
                      'Decline in provision of services']), 6, 'One effect, 6 marks.')],
    kind='fixed', **A)

# Q6 ─ the furniture firm's costs
q6 = H.q(3, 'A furniture firm produces 5 sofas each week.', ' (a)')
add('sa-q6-a', '1-5', 'fixed-and-variable-costs-of-sofas', ref('A', 6, '(a)'),
    H.q(3, 'Write, in the spaces below, which two are fixed costs', ' Fixed Costs'), '3 + 2 + 2 + 2', 9,
    [ladder('r-1', 'Each cost placed', 9, [f'{H.traced(k)} — {H.traced(c)}' for k, c in (('Fixed Costs', 'Insurance'), ('Fixed Costs', 'Rent'),
                                                                                      ('Variable Costs', 'Raw Materials'), ('Variable Costs', 'Wages'))],
            [3, 2, 2, 2], H.traced('1 at 3 marks + 3 at 2 marks each') + ', the first correct 3.')],
    kind='fixed', stem=q6, **A)
add('sa-q6-b-i', '1-5', 'total-cost-of-the-sofas', ref('A', 6, '(b)(i)'), H.q(3, 'The total cost of producing all 5 sofas:', ' _'), '5', 5,
    [point('r-1', H.traced('€400 + €100 + €500 + €300 = €1,300'), 5, 'The total cost with its working, 5 marks.')], stem=q6, **A)
add('sa-q6-b-ii', '1-5', 'profit-on-the-sofas', ref('A', 6, '(b)(ii)'), H.q(3, 'The profit made on total sales:', ' _'), '3', 3,
    [point('r-1', H.traced('€1,500 - €1,300 = €200.'), 3, 'The profit with its working, 3 marks.')], stem=q6, **A)

# Q7 ─ private health insurance
add('sa-q7', '1-3', 'cancelled-health-insurance', ref('A', 7),
    H.q(3, 'State one possible economic reason why people may have cancelled', ' Economic Reason:'), '11 + 6', 17,
    [heading('r-reason', 'A reason — any one',
             H.split('1. Increased health premiums:', '\nEconomic effect:', ['Increased health premiums:', 'Unemployment:', 'Higher taxation:',
                                                                           'People are prepared to wait', 'Opportunity cost:']), 11,
             'One reason, 11 marks: ' + H.traced('11 marks +6 marks') + '.'),
     heading('r-effect', 'An effect — any one',
             H.split('1. Increased pressure on publicly funded health services:', '11 marks +6 marks',
                     ['Increased pressure on publicly funded health services:', 'Increased pressure on government finances',
                      'Less healthy population', 'Private health insurance companies']), 6, 'One effect, 6 marks.')],
    kind='fixed', stem=H.q(3, '‘More than 60,000 people have cancelled', ' State one'), **A)

# Q8 ─ monopoly curves
q8 = H.q(3, 'The diagram below represents a Monopoly firm in equilibrium', ' (a)')
q8_fig = PAP + 'p03-q8-diagram'
add('sa-q8-a', '2-0', 'curves-of-the-monopolist', ref('A', 8, '(a)'),
    H.q(3, 'Name each of the curves numbered 1 to 3.', ' (b)'), '3 x 5 (3 + 2)', 15,
    [point(f'r-{n}', f'{n} — {H.traced(name)}', 5, f'Curve {n}, ' + H.traced('5 (3+2)') + ' marks.')
     for n, name in (('1', 'Marginal Cost'), ('2', 'Average Cost'), ('3', 'Marginal Revenue'))],
    stem=q8, figure=q8_fig, **A)
add('sa-q8-b', '2-0', 'price-and-cost-of-the-monopolist', ref('A', 8, '(b)'),
    H.q(3, 'Show on the diagram the price the firm will sell at', ' ANSWER BOX'), '1 + 1', 2,
    [anyN('r-1', 'Each shown', 2, 2, 1, [H.traced('P1'), H.traced('C1')],
          H.traced('2 marks (1+1)') + ': P1 and C1 marked on the price axis, as the scheme’s diagram shows.')],
    kind='fixed', stem=q8, figure=SOL + 'p08-q8-diagram', **A)
beside_ask(cards[-1], q8_fig)

# Q9 ─ infrastructure
add('sa-q9', '3-1', 'infrastructure-and-the-hospital', ref('A', 9),
    H.q(3, 'The proposed construction of the National Children’s Hospital', ' Explanation:'), '7 + 10', 17,
    [heading('r-explanation', 'The explanation — any one', bl('• Capital equipment used to supply publicly', 'Economic benefit:'), 7,
             'The explanation, 7 marks: ' + H.traced('7 marks + 10 marks') + '.'),
     heading('r-benefit', 'An economic benefit — any one',
             H.split('1. Improved health care for children in Ireland.', '7 marks + 10 marks',
                     ['Improved health care', 'Reduced costs', 'Employment for those', 'Employment in spin-off', 'Government revenue']), 10,
             'One benefit, 10 marks.')],
    kind='fixed', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ perfect competition; petrol and diesel prices
q1 = H.q(4, 'The diagram below represents the Long Run Equilibrium of a firm in Perfect Competition.', ' P MC')
q1_fig = PAP + 'p04-q1-diagram'
add('sb-q1-a-i', '2-0', 'labels-of-perfect-competition', ref('B', 1, '(a)(i)'),
    H.q(4, 'Copy the diagram into your answer book.', ' (ii)'), '6 @ 4', 24,
    [point(f'r-{lab.lower()}', f'{lab} — {H.traced(full)}', 4, f'{lab}, 4 marks' + (' (2 + 2).' if len(lab) == 2 else '.'))
     for lab, full in (('P', 'Price'), ('Q', 'Quantity'), ('AC', 'Average Cost'), ('MC', 'Marginal Cost'), ('AR', 'Average Revenue'),
                       ('MR', 'Marginal Revenue'))],
    stem=q1, figure=q1_fig, **B)
add('sb-q1-a-ii', '2-0', 'equilibrium-in-perfect-competition', ref('B', 1, '(a)(ii)'),
    H.q(4, 'Equilibrium occurs at point E on the diagram.', ' (30 marks)'), '3 @ 2', 6,
    [point(f'r-{lab[0].lower()}', H.traced(f'{lab} {what}'), 2, f'{lab}, 2 marks.')
     for lab, what in (('Q1', 'the output the company will produce'), ('C1', 'the average cost of producing this output'),
                       ('P1', 'the price charged for this output'))],
    stem=q1, figure=SOL + 'p09-q1a-diagram', **B)
beside_ask(cards[-1], q1_fig)
q1b = H.q(4, 'One of the characteristics of Perfect Competition is that all goods produced are', ' (i)')
add('sb-q1-b-i', '2-0', 'homogeneous-goods', ref('B', 1, '(b)(i)'), f"{q1b} {H.q(4, 'Explain the underlined term.', ' (ii)')}", '7', 7,
    [point('r-1', H.traced('The products supplied by producers are identical products.'), 7, 'The explanation, 7 marks.')], **B)
pick('sb-q1-b-ii', '2-0', 'characteristics-of-perfect-competition', ref('B', 1, '(b)(ii)–(iii)'),
     ' '.join([H.q(4, 'State two other characteristics of perfect competition.', ' (iii)'),
               H.q(4, 'Write brief notes on each of these two other characteristics.', ' (21 marks)')]), 'A characteristic, with its note — any two',
     H.split('There are many buyers in the industry', '2 at 7 marks (4+3) each',
             ['There are many buyers in the industry', 'There are many sellers in the industry', 'Free entry and exit', 'Perfect knowledge',
              'Company tries to maximise profits', 'Elastic supply of factors of production', 'No collusion in the market']),
     2, 7, 'Two characteristics, 7 marks each (4 + 3): the scheme prices (ii) and (iii) together.', stem=q1b, **B)
q1c = H.q(4, 'The prices of petrol and diesel have increased in Ireland in recent years.', ' (i)')
pick('sb-q1-c-i', '1-0', 'why-fuel-prices-rose', ref('B', 1, '(c)(i)'), H.q(4, 'State and explain one reason for these increases.', ' (ii)'),
     'A reason — any one', H.split('1. Increase in indirect taxation', '4 marks (2+2)',
                                   ['Increase in indirect taxation', 'Rising international prices for oil', 'Decrease in value of euro',
                                    'Availability of oil']),
     1, 4, 'One reason, 4 marks (2 + 2).', stem=q1c, **B)
motorists = cc('• Increased cost of transport • Cutbacks')
add('sb-q1-c-ii', '1-0', 'effects-of-dear-fuel', ref('B', 1, '(c)(ii)'),
    H.q(4, 'State and explain one economic effect which high petrol and diesel prices', ' (iii)'), '2 x 5 (2 + 3)', 10,
    [heading('r-motorists', H.traced('Irish motorists') + ' — any one',
             [f'{s} — {e}' for s, e in zip(bullets_of(cc('• Increased cost of transport')), bullets_of(cc('• Reduced disposable income and a lower')))],
             5, 'One effect on motorists, 5 marks (2 + 3).'),
     heading('r-economy', H.traced('Irish economy') + ' — any one',
             [f'{s} — {e}' for s, e in zip(bullets_of(cc('• Inflation • Potential job losses')), bullets_of(cc('• Increased transport costs may')))],
             5, 'One effect on the economy, 5 marks (2 + 3).')],
    kind='fixed', stem=q1c, **B)
pick('sb-q1-c-iii', '3-1', 'cutting-motorists-costs', ref('B', 1, '(c)(iii)'),
     H.q(4, 'State and explain two measures the Irish Government could take', ' (24 marks)'), 'A measure — any two',
     H.split('1. Decrease indirect taxation', '2 at 5 marks (2+3) each', ['Decrease indirect taxation', 'Reduce cost of NCT', 'Reduce car tax',
                                                                         'Reduce VAT on car repairs']),
     2, 5, 'Two measures, 5 marks each (2 + 3).', stem=q1c, **B)

# Q2 ─ the iPad market; demand; financial and opportunity cost
q2 = H.q(5, 'The information below represents the market demand and supply schedules for Apple iPads.', ' Price')
q2_table = PAP + 'p05-q2a-table'
add('sb-q2-a', '1-0', 'drawing-the-ipad-market', ref('B', 2, '(a)(i)–(iii)'),
    ' '.join([H.q(5, 'Using the above information and one diagram:', ' (i)'), H.q(5, '(i) Draw and label the market demand curve', ' (30 marks)')]),
    '10 + 10 + 4 + 3 + 3', 30,
    [point('r-demand', H.traced('D/C: 5 points at 2 marks each'), 10, 'The demand curve, 10 marks: its five points at 2 each.'),
     point('r-supply', H.traced('S/C: 5 points at 2 marks each'), 10, 'The supply curve, 10 marks: its five points at 2 each.'),
     anyN('r-labels', 'Each label', 4, 4, 1, [H.traced(x) for x in ('P', 'Q', 'D/C', 'S/C')], H.traced('(4 x 1 marks each)') + '.'),
     point('r-pe', 'Pe — ' + H.traced('500'), 3, H.traced('Pe and Qe : 2 at 3 marks each') + ': the equilibrium price, read off the scheme’s graph.'),
     point('r-qe', 'Qe — ' + H.traced('600'), 3, 'The equilibrium quantity, 3 marks. The completed graph is shown with the answer.')],
    kind='fixed', stem=q2, figure=SOL + 'p13-q2a-graph', **B)
beside_ask(cards[-1], q2_table)
terms = (('Normal good', 'A consumer buys more of this good as income rises.'), ('Substitute good', 'Goods that satisfy the same needs'),
         ('Complementary good', 'Goods that are used in conjunction'))
pick('sb-q2-b-i', '1-1', 'normal-substitute-and-complementary-goods', ref('B', 2, '(b)(i)'),
     H.q(5, 'Explain any two of the following economic terms:', ' (ii)'), 'A term — any two',
     [f'{cc(t, whole=True)} — {cc(e)}' for t, e in terms], 2, 5, H.traced('2 explanations at 5 marks each') + '.', **B)
measures2 = ['Reduce iPad price', 'Innovation / improved design / change specification / advertising', 'Additional Apps ‘Freebies’', 'On-line Assistance']
add('sb-q2-b-ii', '1-1', 'a-cheaper-rival-to-the-ipad', ref('B', 2, '(b)(ii)'),
    H.q(5, 'Samsung, a competitor of Apple, introduced to the market a similar product', ' (25 marks)'), '2 + 3 + 2 x 5', 15,
    [point('r-shift', H.traced('The market demand curve will shift to the left.'), 2, H.traced('D/C shifts to the left: 2 marks') + '.'),
     point('r-why', H.traced('Less iPads may be demanded as consumers switch to the Samsung Galaxy due to its more competitive price.'), 3,
           H.traced('Explanation: 3 marks.')),
     anyN('r-measures', 'A measure — any two', 10, 2, 5, [se(m) for m in measures2], H.traced('2 measures at 5 marks (2+3) each') + '.')],
    kind='fixed', **B)
q2c = H.q(5, 'There is a financial cost and an opportunity cost involved', ' (i)')
fin_why = bullets_of(cc('• Can the consumer afford the product'))
opp_why = bullets_of(cc('• What is the consumer giving up'))
add('sb-q2-c-i', '0-1', 'financial-and-opportunity-cost', ref('B', 2, '(c)(i)'),
    f"{q2c} {H.q(5, 'Explain the underlined terms.', ' (ii)')}", '6 + 6', 12,
    [point('r-financial', f"{H.traced('Financial cost')} — {H.traced('This is the money cost in buying the iPad.')}", 6, 'The financial cost, 6 marks.'),
     heading('r-opportunity', H.traced('Opportunity cost') + ' — any one', bullets_of(cc('• The cost of foregone alternatives.')), 6,
             'The opportunity cost, 6 marks: the scheme gives three explanations.')],
    kind='fixed', **B)
add('sb-q2-c-ii', '0-1', 'weighing-both-costs', ref('B', 2, '(c)(ii)'),
    H.q(5, 'Discuss why each cost should be considered before purchasing an item.', ' (20 marks)'), '5 + 3', 8,
    [heading('r-financial', H.traced('Financial cost') + ' — any one', fin_why, 5, 'Why the financial cost matters, 5 marks.'),
     heading('r-opportunity', H.traced('Opportunity cost') + ' — any one', opp_why, 3, 'Why the opportunity cost matters, 3 marks.')],
    kind='fixed', stem=q2c, **B)

# Q3 ─ labour; the public sector; IT skills
q3 = H.q(6, 'The factor of production labour receives a payment called wages.', ' (a)')
add('sb-q3-a-i', '2-1', 'labour', ref('B', 3, '(a)(i)'), f"{q3} {H.q(6, 'Explain the underlined term.', ' (ii)')}", '7', 7,
    [point('r-1', H.traced('Labour is defined as the human effort involved in the production of goods and services.'), 7, 'The explanation, 7 marks.')], **B)
pick('sb-q3-a-ii', '2-1', 'why-wages-differ', ref('B', 3, '(a)(ii)'),
     H.q(6, 'State and explain two reasons why different wage rates are paid', ' (iii)'), 'A reason — any two',
     H.split('1. Different skills', '2 reasons at 6 marks (3+3) each',
             ['Different skills', 'Training', 'Educational qualifications', 'Nature & Conditions of the job', 'Negotiating strength',
              'Traditions attaching to certain jobs', 'Possession of innate talents', 'Gender Bias']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q3, **B)
add('sb-q3-a-iii', '2-1', 'occupational-mobility', ref('B', 3, '(a)(iii)'),
    H.q(6, 'Explain the term occupational mobility of labour', ' (25 marks)'), '4 + 2', 6,
    [point('r-definition', H.traced('The ability/ease of a worker to move from one job to another.'), 4, 'The definition, 4 marks.'),
     heading('r-factor', 'A factor — any one',
             H.split('1. Availability and access to affordable education courses.', '1 factor at 2 marks',
                     ['Availability and access to affordable', 'Availability and access to training', 'Government policies which aid mobility',
                      'Reduced barriers to entry', 'Loss of seniority', 'Workers may be so specialised']), 2, 'One factor, 2 marks.')],
    kind='fixed', stem=q3, **B)
q3b = H.q(6, '‘The Irish Government plans to reduce the numbers employed in the public sector', ' (i)')
add('sb-q3-b-i', '3-1', 'the-public-sector', ref('B', 3, '(b)(i)'),
    H.q(6, 'Explain the underlined term and state one example of an occupation', ' (ii)'), '5 + 5', 10,
    [point('r-term', H.opt('That part of the economy which is run by state bodies', '\nExample:'), 5, 'The public sector, 5 marks.'),
     point('r-example', 'Example: ' + H.traced('Secondary School Teaching'), 5, 'An example, 5 marks: the scheme’s is teaching.')],
    stem=q3b, **B)
pick('sb-q3-b-ii', '3-1', 'why-cut-public-sector-numbers', ref('B', 3, '(b)(ii)'),
     H.q(6, 'State and explain one reason why the government continues to reduce', ' (iii)'), 'A reason — any one',
     [se(x) for x in ('Reduce costs', 'Increase efficiency', 'Meet ‘Troika’ requirements')], 1, 6, 'One reason, 6 marks (3 + 3).', stem=q3b, **B)
pick('sb-q3-b-iii', '3-1', 'effects-of-fewer-public-servants', ref('B', 3, '(b)(iii)'),
     H.q(6, 'Discuss two effects on the Irish economy of this reduction', ' (26 marks)'), 'An effect — any two',
     [se(x) for x in ('Government Finances', 'Provision of services', 'Industrial disputes', 'Discontented workforce', 'Unemployment', 'Reduced Demand')],
     2, 5, 'Two effects, 5 marks each (2 + 3).', stem=q3b, **B)
q3c = H.q(6, 'Some companies in the Information Technology (IT) sector are experiencing shortages', ' (i)')
pick('sb-q3-c-i', '2-1', 'the-it-skills-shortage', ref('B', 3, '(c)(i)'),
     H.q(6, 'State and explain two economic effects of this skills shortage', ' (ii)'), 'An effect — any two',
     [se(x) for x in ('Foreign companies may not locate here', 'Increased wage rates / Training costs', 'Increased immigration',
                      'Increased demand for IT courses', 'Loss of productivity')],
     2, 6, 'Two effects, 6 marks each (3 + 3).', stem=q3c, **B)
groups3 = (('IT Companies', '• Increase wage rates • Internships', '• This may attract workers into the IT sector.'),
           ('Colleges / Universities', '• Offer IT courses • Bonus points', '• Develop courses in conjunction'),
           ('Irish Government', '• Work permits / Visas', '• WPs will ease restrictions'))
actions = []
for g, acts, expls in groups3:
    actions += [f'{a} — {e}' for a, e in zip(bullets_of(cc(acts)), bullets_of(cc(expls)))]
pick('sb-q3-c-ii', '2-1', 'easing-the-it-skills-shortage', ref('B', 3, '(c)(ii)'),
     H.q(6, 'Outline one action which any two of the following could take', ' (24 marks)'), 'An action — any two, from two of the groups',
     actions, 2, 6, H.traced('ANY 2 actions at 6 marks (3+3) each') + ', one for each of two groups. The scheme lists four actions for '
     'the IT companies, then two for colleges and universities, then three for the government, in that order here.', stem=q3c, **B)

# Q4 ─ privatisation; a sugar tax; the Budget 2013 measures
q4a = H.q(6, 'The Irish Government is planning to privatise some state assets', ' (i)')
add('sb-q4-a-i', '1-3', 'privatisation', ref('B', 4, '(a)(i)'), H.q(6, 'What is meant by the term \'privatisation\'?', ' (ii)'), '5', 5,
    [point('r-1', H.traced('This is the sale of a state owned company to private owners.'), 5, 'The explanation, 5 marks.')], stem=q4a, **B)
for part, concept, ask, nxt, heads, word in (
        ('ii', 'arguments-for-privatisation', 'Outline two economic arguments in favour of privatisation.', ' (iii)',
         ['Improved quality / choice of services', 'More competitive prices', 'Continuity of supply', 'Employment opportunities',
          'More rewards/Incentives for innovation', 'Revenue from sale / reduced borrowing', 'Shedding of loss making companies'], 'in favour'),
        ('iii', 'arguments-against-privatisation', 'Outline two economic arguments against privatisation.', ' (25 marks)',
         ['Loss of non-profit making services', 'Standards of service / increased prices', 'Curtailment in Pay / Pension increases',
          'Loss of jobs / reduced job security', 'Loss of a valuable state resource', 'Foreign ownership', 'Costs of the Sale'], 'against')):
    pick(f'sb-q4-a-{part}', '1-3', concept, ref('B', 4, f'(a)({part})'), H.q(6, ask, nxt), f'An argument {word} — any two',
         [unnum(cc(f'{k + 1}. {h}')) for k, h in enumerate(heads)], 2, 5, 'Two arguments, 5 marks each (2 + 3).', stem=q4a, **B)
q4b = H.q(6, 'The Institute of Public Health in Ireland recommended that a ‘sugar tax’', ' (i)')
add('sb-q4-b-i', '3-1', 'vat', ref('B', 4, '(b)(i)'), H.q(6, 'Explain the term \'VAT\'.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('VAT: tax placed on goods and services / on spending'), 5, 'The explanation, 5 marks.')], stem=q4b, **B)
pick('sb-q4-b-ii', '1-3', 'arguments-for-a-sugar-tax', ref('B', 4, '(b)(ii)'),
     H.q(6, 'State and explain two economic arguments in favour of this \'sugar tax\'.', ' (iii)'), 'An argument in favour — any two',
     [unnum(cc(f'{k + 1}. {h}')) for k, h in enumerate(['Revenue for state/Improved', 'Reduce consumption of sugary foods', 'Help fund health initiatives',
                                                 'Help reduce future health costs', 'Healthier population'])],
     2, 5, 'Two arguments, 5 marks each (2 + 3).', stem=q4b, **B)
pick('sb-q4-b-iii', '1-3', 'an-argument-against-a-sugar-tax', ref('B', 4, '(b)(iii)'),
     H.q(6, 'State and explain one economic argument against introducing this', ' (20 marks)'), 'An argument against — any one',
     [unnum(cc(f'{k + 1}. {h}')) for k, h in enumerate(['Higher Prices Consumers', 'Job losses If', 'Development of ‘nanny state’',
                                                 'Encourages alcohol consumption', 'Inequitable This extra'])],
     1, 5, 'One argument, 5 marks (2 + 3).', stem=q4b, **B)
budget = (('property', 'Introduction of the household property tax (i.e. 0.18% on values of homes).',
           ['Government revenue These charges', 'Stable tax', 'Less need to raise direct taxes', 'Government planning', 'Economic The cost'],
           ['Regressive', 'Decreased disposable incomes Less', 'Inequitable People in different', 'Reduction in demand/spending']),
          ('child-benefit', 'Reduction in the rate of child benefit (i.e. minimum of €10 per child).',
           ['Decreased government expenditure', 'Reduced need to increase taxes', 'Less need to affect state services', 'Higher income groups'],
           ['Reduced incomes This will mean', 'Inequitable This reduction', 'Increase in child poverty']),
          ('registration', 'Increase in third level education registration charge',
           ['Revenue for colleges', 'Less strain on the government’s finances', 'Opportunity cost The government', 'Extension of college activities'],
           ['Discourage people attending third level', 'Inequitable These higher', 'Workforce less educated', 'Less FDI',
            'Students less disposable incomes']))
rows4 = []
for key, label, pro, con in budget:
    for side_, opts in (('for', pro), ('against', con)):
        found = []
        for k, h in enumerate(opts):
            prefix = f'{k + 1}. {h}' if not (key == 'property' and side_ == 'for' and k == 4) else '5. Economic The cost'
            found.append(unnum(cc(prefix)))
        rows4.append(heading(f'r-{key}-{side_}', f"{H.traced(label.split(' (')[0])} — an argument {'in favour' if side_ == 'for' else 'against'}",
                             found, 5, f"One argument {'in favour' if side_ == 'for' else 'against'}, " + H.traced('1 at 5 marks (2+3)') + '.'))
add('sb-q4-c', '3-1', 'arguing-the-budget-2013-measures', ref('B', 4, '(c)'),
    H.q(6, 'Outline one economic argument in favour of and one economic argument against each', ' (30 marks)'), '6 x 5 (2 + 3)', 30,
    rows4, kind='fixed', **B)

# Q5 ─ the circular flow; consumer spending; the black economy
q5 = H.q(7, 'The diagram below represents the Circular Flow of Income in an open economy without', ' 1 Households')
q5_fig = PAP + 'p07-q5-diagram'
lines5 = (('1', 'Payment / for factors of production', '4 marks: ' + H.traced('2 marks + 2 marks (wages)')),
          ('2', 'Spending /on (domestic) goods & services', '4 marks: 2 + 2'), ('3', 'Savings', '4 marks'), ('4', 'Imports', '4 marks'),
          ('5', 'Exports', '4 marks'))
add('sb-q5-a-i', '3-0', 'lines-of-the-open-circular-flow', ref('B', 5, '(a)(i)'),
    H.q(7, 'State what each of the lines numbered 1 to 5 represents.', ' (ii)'), '5 @ 4', 20,
    [point(f'r-{n}', f'{n} — {cc(r, whole=True)}', 4, f'Line {n}, {m}.') for n, r, m in lines5], stem=q5, figure=q5_fig, **B)
add('sb-q5-a-ii', '3-0', 'activities-around-the-flow', ref('B', 5, '(a)(ii)'),
    H.q(7, 'Referring to the diagram above, explain briefly the types of activities', ' (30 marks)'), '3 + 3 + 4', 10,
    [point('r-savings', f"{H.traced('Households and financial institutions')} — {H.traced('Households save part of their income with financial institutions.')}", 3,
           'Households and financial institutions, 3 marks.'),
     point('r-imports', f"{H.traced('Households and foreign markets')} — "
           f"{H.traced('Households spend part of their income buying imports i.e. goods and services from abroad.')}", 3,
           'Households and foreign markets, 3 marks.'),
     point('r-exports', f"{H.traced('Foreign markets and firms')} — "
           f"{H.traced('Firms export some of their goods and services to foreign markets and receive income for these.')}", 4,
           'Foreign markets and firms, 4 marks.')],
    stem=q5, figure=q5_fig, **B)
q5b = H.q(7, 'The level of consumer expenditure in Ireland has fallen in recent times.', ' (i)')
pick('sb-q5-b-i', '3-0', 'why-consumer-spending-fell', ref('B', 5, '(b)(i)'),
     H.q(7, 'Outline two economic reasons for this development.', ' (ii)'), 'A reason — any two',
     [se(x) for x in ('Increased unemployment', 'Increased taxation', 'Reduced consumer confidence', 'Increased VAT rates',
                      'Reduced child benefit rates', 'Increased mortgage interest rates')],
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q5b, **B)
pick('sb-q5-b-ii', '3-1', 'raising-consumer-spending', ref('B', 5, '(b)(ii)'),
     H.q(7, 'Discuss two actions which the government could take to increase consumer expenditure.', ' (20 marks)'), 'An action — any two',
     [se(x) for x in ('Decrease VAT rates', 'Decrease income taxes / levies', 'Provide incentives to consumers to spend',
                      'Facilitate lending by the financial institutions', 'Generate confidence in the economy', 'Increase government capital spending')],
     2, 5, 'Two actions, 5 marks each (2 + 3).', stem=q5b, **B)
q5c = H.q(7, '‘Illegal trade (black economy) costs the State €860m', ' (i)')
pick('sb-q5-c-i', '3-0', 'black-economy-activities', ref('B', 5, '(c)(i)'),
     H.q(7, 'State one example of an activity in Ireland’s \'black economy\'.', ' (ii)'), 'An example — any one',
     bl('• A teacher giving grinds', '5 marks'), 1, 5, 'One example, 5 marks.', stem=q5c, **B)
pick('sb-q5-c-ii', '3-0', 'why-the-black-economy-grew', ref('B', 5, '(c)(ii)'),
     H.q(7, 'State and explain two reasons for the recent growth', ' (iii)'), 'A reason — any two',
     # The table-cell rendering drops two statement cells an earlier table also prints, so those rows are read whole.
     [se('Reduced disposable incomes'), f"{H.traced('Increased VAT rates')} — {cc('Causing prices to increase and consumers want')}",
      f"{H.traced('Unemployment')} — {cc('Those who have lost jobs cannot afford VAT')}", se('Disillusionment with government taxation policies')],
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q5c, **B)
pick('sb-q5-c-iii', '3-0', 'effects-of-the-black-economy', ref('B', 5, '(c)(iii)'),
     H.q(7, 'Explain two economic effects which the growing \'black economy\'', ' (25 marks)'), 'An effect — any two',
     [se(x) for x in ('Increased government expenditure', 'Increased unemployment bill', 'Decline in legitimate business activity',
                      'Pressure on government finances / Provision of services', 'Effect on health services of uses of products')],
     2, 5, 'Two effects, 5 marks each (2 + 3).', stem=q5c, **B)

# Q6 ─ emigration; an ageing population; unemployment
q6a = H.q(8, 'Emigration from Ireland in recent years has increased.', ' (i)')
add('sb-q6-a-i', '3-2', 'emigration', ref('B', 6, '(a)(i)'), f"{q6a} {H.q(8, 'Explain the underlined term.', ' (ii)')}", '4', 4,
    [point('r-1', H.traced('Movement of Irish nationals to reside elsewhere / to other countries.'), 4, 'The explanation, 4 marks.')], **B)
add('sb-q6-a-ii', '3-2', 'why-emigration-rose', ref('B', 6, '(a)(ii)'),
    H.q(8, 'State and explain two reasons for the increase in emigration.', ' (iii)'), '6 + 2', 8,
    [ladder('r-1', 'A reason — any two', 8,
            H.split('Economic recession in Ireland / Job opportunities abroad', '1st reason at 6 marks',
                    ['Economic recession in Ireland / Job opportunities abroad', 'Wage rates in Ireland', 'Rising levels of taxation in Ireland',
                     'Prospects for economic recovery', 'Develop skills abroad', 'More optimistic outlook']),
            [6, 2], 'Two reasons: the ' + H.traced('1st reason at 6 marks (4 + 2)') + ', the 2nd at 2.')],
    kind='fixed', stem=q6a, **B)
neg6 = [cc(x) for x in ('Higher dependency ratio Young', 'Opportunity cost The state loses', 'Loss of skills within the economy',
                       'Smaller domestic market As', 'Upward pressure on Irish wage')]
pos6 = [cc(x) for x in ('Unemployment reduced Those', 'Emigrants returning to Ireland', 'Contacts / Export opportunities',
                       'Demand for state services With')]
add('sb-q6-a-iii', '3-2', 'effects-of-emigration', ref('B', 6, '(a)(iii)'),
    H.q(8, 'State and explain two economic effects which this increase in emigration', ' (24 marks)'), '8 + 4', 12,
    [ladder('r-1', 'An effect — any two, negative or positive', 12, side('Negative effects', neg6) + side('Positive effects', pos6), [8, 4],
            'Two effects: the ' + H.traced('1st effect at 8 marks ( 6 + 2)') + ', the 2nd at 4 (2 + 2).')],
    kind='fixed', stem=q6a, **B)
q6b = H.q(8, '‘The number of people aged over 65 years is projected', ' (i)')
add('sb-q6-b-i', '3-5', 'effects-of-an-ageing-population', ref('B', 6, '(b)(i)'),
    H.q(8, 'Outline two possible economic effects which this ageing population', ' (ii)'), '8 + 4', 12,
    [ladder('r-1', 'An effect — any two', 12,
            H.split('Pressure on provision of state pensions', '1st effect at 8 marks',
                    ['Pressure on provision of state pensions', 'Possible increased tax burden', 'Increased government expenditure',
                     'Changing nature of goods/services demanded', 'The participation rate falls', 'Reduced mobility of labour']),
            [8, 4], 'Two effects: the ' + H.traced('1st effect at 8 marks (6 + 2)') + ', the 2nd at 4 (2 + 2).')],
    kind='fixed', stem=q6b, **B)
pick('sb-q6-b-ii', '3-5', 'a-later-retirement-age', ref('B', 6, '(b)(ii)'),
     H.q(8, 'Suggest one reason why the Irish Government increased the retirement age', ' (21 marks)'), 'A reason — any one',
     H.split('1. Reduce the costs of future pensions', '1 reason at 9 marks',
             ['Reduce the costs of future pensions', 'Less services required from the state', 'People living longer', 'Retain experienced workforce']),
     1, 9, 'One reason, 9 marks (6 + 3).', stem=q6b, **B)
q6c = H.q(8, 'The rate of unemployment in Ireland remains in excess of 14%.', ' (i)')
pick('sb-q6-c-i', '3-2', 'measuring-unemployment', ref('B', 6, '(c)(i)'),
     H.q(8, 'Name one method of measuring unemployment in Ireland.', ' (ii)'), 'A method — any one',
     bl('• Live Register', '6 marks'), 1, 6, 'One method, 6 marks.', stem=q6c, **B)
add('sb-q6-c-ii', '3-2', 'why-unemployment-stays-high', ref('B', 6, '(c)(ii)'),
    H.q(8, 'State and explain two possible reasons for Ireland’s continuing high unemployment.', ' (iii)'), '8 + 4', 12,
    [ladder('r-1', 'A reason — any two', 12,
            [se(x) for x in ('Worldwide economic recession', 'Relocation of industry outside of Ireland', 'Inability of businesses to get credit',
                             'Irish consumers not spending', 'Construction sector', 'Irish companies exporting to UK', 'Public sector job losses')],
            [8, 4], 'Two reasons: the ' + H.traced('1st reason at 8 marks ( 6 + 2)') + ', the 2nd at 4 (2 + 2).')],
    kind='fixed', stem=q6c, **B)
cons6 = [cc(x) for x in ('Increase spending By', '"Buying Irish"', 'Avoid the black economy', 'Holiday in Ireland')]
gov6 = [cc(x) for x in ('Reduce VAT rates This would help', 'Reduce direct taxes', 'Give subsidies to employers', 'Training opportunities')]
add('sb-q6-c-iii', '3-2', 'cutting-unemployment', ref('B', 6, '(c)(iii)'),
    H.q(8, 'Suggest one measure each of the following could take', ' (30 marks)'), '8 + 4', 12,
    [ladder('r-1', 'One measure for each — consumers and the government', 12, side('Irish Consumers', cons6) + side('Irish Government', gov6),
            [8, 4], 'One measure for each: the ' + H.traced('1st measure at 8 marks ( 6 + 2)') + ', the 2nd at 4 (2 + 2).')],
    kind='fixed', stem=q6c, **B)

# Q7 ─ imports; tourism; Irish multinationals
q7a = H.q(8, '‘Half of all groceries purchased in a family’s weekly shop are imported.’', ' (i)')
pick('sb-q7-a-i', '4-2', 'a-visible-import', ref('B', 7, '(a)(i)'), H.q(8, 'State one example of a visible import to Ireland.', ' (ii)'),
     'An example — any one', bl('• Purchase of foreign cars.', '2 marks'), 1, 2, 'One example, 2 marks.', stem=q7a, **B)
for part, concept, ask, nxt, start, end, firsts, word in (
        ('ii', 'benefits-of-imports', 'State and explain two benefits of imported goods', ' (iii)', '1. More choice for consumers',
         '1st benefit at 8', ['More choice for consumers', 'Raw materials unavailable in Ireland', 'Jobs in the distribution sector',
                              'Tax revenue for the state', 'Small domestic market'], 'benefit'),
        ('iii', 'why-restrict-imports', 'State and explain two reasons why the Irish government may wish to restrict', ' (26 marks)',
         '1. Protect domestic industries', '1st reason at 8', ['Protect domestic industries', 'Protect domestic employment',
                                                               'Protect against ‘Cheap Labour’ economies', 'National Security', 'Protect human rights',
                                                               'Production of strategic goods', 'Prevent dumping', 'Protect the Balance of Payments'],
         'reason')):
    add(f'sb-q7-a-{part}', '4-2', concept, ref('B', 7, f'(a)({part})'), H.q(8, ask, nxt), '8 + 4', 12,
        [ladder('r-1', f'A {word} — any two', 12, H.split(start, end, firsts), [8, 4],
                f'Two {word}s: the 1st correct 8 marks (6 + 2), the 2nd 4 (2 + 2).')],
        kind='fixed', stem=q7a, **B)
q7b = H.q(8, 'The Gathering Ireland 2013 aims to attract an extra 325,000 visitors', ' (i)')
for part, concept, ask, nxt, start, end, firsts, word in (
        ('i', 'what-visitors-weigh-up', 'State and explain two economic factors which people might consider', ' (ii)',
         'Price / Availability of air transport', '1st factor at 8', ['Price / Availability of air transport', 'Prices of accommodation',
                                                                     'Quality of services', 'Advertising / Promotion', 'Range of services',
                                                                     'Exchange Rate/Value of the euro', 'Peaceful country'], 'factor'),
        ('ii', 'benefits-of-more-tourism', 'State and explain two advantages for the Irish economy of an increase in tourism.', ' (24 marks)',
         '1. Increased employment\nMore', '1st advantage at 8', ['Increased employment', 'Increased income / GNP', 'Benefits to business',
                                                                'Tax revenues', 'Improved reputation for Ireland'], 'advantage')):
    add(f'sb-q7-b-{part}', '4-2', concept, ref('B', 7, f'(b)({part})'), H.q(8, ask, nxt), '8 + 4', 12,
        [ladder('r-1', f'A{"n" if word[0] in "aeiou" else ""} {word} — any two', 12, H.split(start, end, firsts), [8, 4],
                f'Two {word}s: the 1st correct 8 marks (6 + 2), the 2nd 4 (2 + 2).')],
        kind='fixed', stem=q7b, **B)
q7c = H.q(8, 'Kerry Group plc is an example of an Irish MNC.', ' (i)')
add('sb-q7-c-i', '4-1', 'mnc-in-full', ref('B', 7, '(c)(i)'), H.q(8, 'What do the initials MNC stand for?', ' (ii)'), '9', 9,
    [point('r-1', H.traced('Multi National Company / Corporation'), 9, 'The name, 9 marks.')], stem=q7c, **B)
pick('sb-q7-c-ii', '4-1', 'another-irish-mnc', ref('B', 7, '(c)(ii)'), H.q(8, 'Name one other Irish MNC.', ' (iii)'), 'An Irish MNC — any one',
     [H.traced(x) for x in ('Greencore', 'Glanbia', 'Ryanair', 'CRH')], 1, 4, 'One MNC, 4 marks.', stem=q7c, **B)
add('sb-q7-c-iii', '4-1', 'benefits-of-irish-mncs', ref('B', 7, '(c)(iii)'),
    H.q(8, 'Discuss two benefits to the Irish economy of Irish MNCs.', ' (25 marks)'), '8 + 4', 12,
    [ladder('r-1', 'A benefit — any two', 12,
            # The table-cell rendering drops the first statement cell ("Employment"), so that row is read whole.
            [f"{H.traced('Employment')} — {cc('The Irish MNCs will create jobs directly')}"]
            + [se(x, 'Exports will increase') for x in ('Exports will increase', 'Taxation revenue will increase',
                                                         'Economic activity will increase', 'Attract investment', 'Benefits to local economy')],
            [8, 4], 'Two benefits: the ' + H.traced('1st benefit at 8 marks (6+2)') + ', the 2nd at 4 (2 + 2).')],
    kind='fixed', stem=q7c, **B)

# Q8 ─ savings; bank closures; money and the euro
q8a = H.q(9, 'The rate of DIRT on savings increased to 33% in the 2013 Budget.', ' (i)')
add('sb-q8-a-i', '3-1', 'dirt-in-full', ref('B', 8, '(a)(i)'), H.q(9, 'What do the initials DIRT stand for?', ' (ii)'), '7', 7,
    [point('r-1', H.traced('Deposit Interest Retention Tax'), 7, 'DIRT in full, 7 marks.')], stem=q8a, **B)
pick('sb-q8-a-ii', '3-4', 'what-shapes-saving', ref('B', 8, '(a)(ii)'),
     H.q(9, 'Outline two factors, other than the rate of DIRT', ' (iii)'), 'A factor — any two',
     H.split('Interest rate levels', '2 factors at 5 marks',
             ['Interest rate levels', 'Income levels', 'Level of Inflation', 'Levels of Social Welfare Benefits', 'Tax levels',
              'Future Expectations / Confidence in the economy', 'Security of savings', 'Demands on disposable income']),
     2, 5, 'Two factors, 5 marks each (2 + 3).', stem=q8a, **B)
add('sb-q8-a-iii', '3-4', 'savings-and-the-economy', ref('B', 8, '(a)(iii)'),
    H.q(9, 'Discuss one economic advantage and one economic disadvantage of savings', ' (25 marks)'), '4 + 4', 8,
    [heading('r-advantage', 'An advantage — any one',
             [cc(x) for x in ('Reduced inflation With', 'Reduced demand for imports', 'More funds available for investment', 'Ease personal debt',
                              'Reduce future demands on state', 'Increase in DIRT revenue')], 4, 'One advantage, 4 marks (2 + 2).'),
     heading('r-disadvantage', 'A disadvantage — any one',
             [cc(x) for x in ('Reduced spending within the economy', 'Increase in unemployment Falling', 'Reduced economic growth')], 4,
             'One disadvantage, 4 marks (2 + 2).')],
    kind='fixed', stem=q8a, **B)
q8b = H.q(9, '‘Allied Irish Bank (AIB) closed 44 of its bank branches', ' (i)')
pick('sb-q8-b-i', '3-4', 'why-banks-close-branches', ref('B', 8, '(b)(i)'),
     H.q(9, 'State and explain one reason why some of Ireland’s major banks are closing branches.', ' (ii)'), 'A reason — any one',
     [se(x) for x in ('Decrease costs', 'Increased use of internet', 'Advances in technology')], 1, 6, 'One reason, 6 marks (3 + 3).', stem=q8b, **B)
groups8 = (('customers', 'Customers', ['Loss of service', 'Inconvenience', 'Lack of relationship with manager']),
           ('employees', 'Employees', ['Loss of jobs', 'Re-location/redeployment']),
           ('community', 'Local community', ['Reduced economic activity', 'Job losses', 'Increased pressure on Post Office', 'Risk of theft']))
add('sb-q8-b-ii', '3-4', 'effects-of-branch-closures', ref('B', 8, '(b)(ii)'),
    H.q(9, 'Discuss one possible economic effect which the closure of these bank branches', ' (24 marks)'), '3 x 6 (3 + 3)', 18,
    [heading(f'r-{rid}', H.traced(g) + ' — any one', numbered(CELLS[CELLS.index(g) + 1], heads), 6,
             f'One effect on {g.lower()}, 6 marks (3 + 3).') for rid, g, heads in groups8],
    kind='fixed', stem=q8b, **B)
q8c = H.q(9, 'A new series of €5 notes is in circulation', ' (i)')
add('sb-q8-c-i', '3-3', 'the-ecb', ref('B', 8, '(c)(i)'), H.q(9, 'What do the initials ECB stand for?', ' (ii)'), '6', 6,
    [point('r-1', H.traced('European Central Bank.'), 6, 'The name, 6 marks.')], stem=q8c, **B)
add('sb-q8-c-ii', '3-4', 'characteristics-of-money', ref('B', 8, '(c)(ii)'),
    H.q(9, '\'Money should be durable\'.', ' (iii)'), '4 + 2 x 4', 12,
    [point('r-durable', H.traced('Durable: it should be capable of withstanding a lot of handling.'), 4, 'Durable explained, 4 marks.'),
     anyN('r-others', 'Another characteristic — any two', 8, 2, 4,
          [H.traced(x) for x in ('Relatively scarce', 'Portable', 'Generally acceptable', 'Homogeneous', 'Divisible')],
          H.traced('2 at 4 marks each') + '.')],
    kind='fixed', stem=q8c, **B)
add('sb-q8-c-iii', '4-1', 'the-euro-for-ireland', ref('B', 8, '(c)(iii)'),
    H.q(9, 'The euro currency has been experiencing difficulties.', ' (26 marks)'), '4 + 4', 8,
    [heading('r-advantage', 'An advantage of the euro — any one',
             [cc(x) for x in ('Low interest rates Consumers', 'Foreign Travel', 'Increased trade opportunities', 'Exchange risk eliminated',
                              'Price comparisons')], 4, 'One advantage, 4 marks (2 + 2).'),
     heading('r-disadvantage', 'A disadvantage of the euro — any one',
             [cc(x) for x in ('Economic policies dictated by EU', 'Exports from Ireland depend', 'Adherence to EU agreements', 'Loss of businesses')], 4,
             'One disadvantage, 4 marks (2 + 2).')],
    kind='fixed', stem=q8c, **B)

if __name__ == '__main__':
    emit(cards)
