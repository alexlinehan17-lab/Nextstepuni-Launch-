#!/usr/bin/env python3
"""Economics 2011 Ordinary Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2011-ol-ev.json, made
from a visual sweep of all 12 paper pages and 36 scheme pages before any 2011
Ordinary card existed. Section B restarts at Question 1, so every citation
names its section and every id carries it (-sa-, -sb-). Question wording and
stems are sliced from the question paper; every marking point is sliced from
the scheme (econ_legacy_lib.py). The scheme's cover prints its level in
capitals ("ORDINARY LEVEL"), so its scheme file was built with the appenders'
cover check pointed at the file (visually verified as the English Ordinary
scheme). A stem stops before any printed table: the table is the crop beside
the typed ask, and printed items a student must read to answer are typed from
the text layer. The only prose written here is guidance: tariffs, route labels
and what a figure or a calculation shows.

The scheme's two-column tables print each heading cell on its own line with
its explanation on the next (`pair`); its multi-item cells are cut at their
own headings (`H.cut_cell`). Its bullets are set in a symbol font that the text
layer reads as "x "; that marker is cut from each option.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_legacy_lib import UNDERSCORES, Old, OldDeck, beside_ask  # noqa: E402
from econ_lib import anyN, emit, point, tidy  # noqa: E402

H = Old(2011, 'ordinary', 'LC034GLP000EV')
D = OldDeck(2011, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2011-OL-scheme-'
PAP = 'economics-2011-OL-paper-'
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
    return H.traced(re.sub(r'^\d{1,2}\.\s*', '', text.strip()))


def unx(text):
    """A response read without the symbol-font bullet the text layer sets as "x "."""
    return H.traced(re.sub(r'^x\s+', '', text.strip()))


def qa(page, after, start, end):
    """The paper's words from `start` to `end`, the first `start` printed after
    `after`: a short ask the page prints more than once ("Explain the
    underlined term.")."""
    text = H.page_text(page)
    i = text.index(start, text.index(after))
    return tidy(UNDERSCORES.sub(' ', text[i:text.index(end, i + len(start))]))


def numbered(start, end, firsts):
    """A numbered list sliced from the primary rendering, each read without its numeral."""
    return [unnum(x) for x in H.split(start, end, firsts)]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ NAMA, the ECB and the IMF
add('sa-q1', '3-1', 'nama-the-ecb-and-the-imf', ref('A', 1, '(i)–(iii)'),
    H.q(2, 'Fill in the missing words in the spaces below to complete the names of the organisations.', ' (i)'),
    '2 + 2 + 3 + 3 + 3 + 3', 16,
    [point('r-national', 'NAMA — ' + H.traced('NATIONAL'), 2, '(i) NAMA, its first missing word: ' + H.traced('2 MARKS + 2 MARKS') + '.'),
     point('r-management', 'NAMA — ' + H.traced('MANAGEMENT'), 2, 'NAMA, its second missing word, 2 marks.'),
     point('r-european', 'ECB — ' + H.traced('EUROPEAN'), 3, '(ii) ECB, its first missing word: ' + H.traced('3 MARKS + 3 MARKS') + '.'),
     point('r-bank', 'ECB — ' + H.traced('BANK.'), 3, 'ECB, its second missing word, 3 marks.'),
     point('r-international', 'IMF — ' + H.traced('INTERNATIONAL'), 3, '(iii) IMF, its first missing word, 3 marks.'),
     point('r-monetary', 'IMF — ' + H.traced('MONETARY'), 3, 'IMF, its second missing word, 3 marks.')],
    kind='fixed', **A)

# Q2 ─ economic systems
systems = (('Major government involvement in the economy', 'Centrally Planned'),
           ('The market system decides what to produce', 'Free Enterprise'),
           ('Production is carried out by the public sector and the private sector.', 'Mixed Economy'))
add('sa-q2', '1-0', 'which-economic-system', ref('A', 2, '(i)–(iii)'),
    # The three statements follow the ask, from the paper's own table rows.
    f"{H.q(2, 'Name the economic system (Free Enterprise, Mixed Economy or Centrally Planned)', ' STATEMENT')} "
    f"{H.q(2, '(i) Major government involvement in the economy.', ' (16 marks)')}", '8 + 4 + 4', 16,
    [anyN('r-1', 'Each statement named', 16, 3, 8, [f'{H.traced(s)} — {H.traced(e)}' for s, e in systems],
          'All three: ' + H.traced('1st correct answer: 8 marks. 2nd & 3rd: 2 x 4 marks each') + '.', steps=[8, 4, 4])],
    kind='fixed', **A)

# Q3 ─ third-level fees
add('sa-q3', '1-3', 'third-level-college-fees', ref('A', 3),
    H.q(2, 'State one economic advantage and one economic disadvantage', ' One economic advantage'), '12 + 4', 16,
    [anyN('r-1', 'One advantage and one disadvantage', 16, 2, 12,
          side('One economic advantage', numbered('1. Increased revenue for colleges.', 'One economic disadvantage:',
                                                  ['1. Increased revenue', '2. Reduced strain', '3. Opportunity cost', '4. Colleges can appoint']))
          + side('One economic disadvantage', numbered('1. May discourage people going to third level.', '\n⟨(16 marks)⟩',
                                                       ['1. May discourage', '2. The fees may fall', '3. If less people attend',
                                                        '4. Could damage Ireland'])),
          'One of each, on one ladder: ' + H.traced('1st correct response: 12 marks. 2nd correct response: 4 marks.'), steps=[12, 4])],
    kind='fixed', **A)

# Q4 ─ perfect competition's long-run equilibrium
q4 = H.q(2, 'The diagram below represents the long run equilibrium of a firm in Perfect Competition.', ' (a)')
q4_diagram = PAP + 'p02-q4-diagram'
labels = (('1', 'PRICE', 2, 'Line 1, 2 marks.'), ('2', 'MARGINAL COST', 3, 'Line 2, 3 marks (2 + 1).'),
          ('3', 'AVERAGE COST', 3, 'Line 3, 3 marks (2 + 1).'), ('4', 'DEMAND / AR / MR', 3, 'Line 4, 3 marks (2 + 1).'),
          ('5', 'QUANTITY', 2, 'Line 5, 2 marks.'))
add('sa-q4-a', '2-0', 'labelling-perfect-competition', ref('A', 4, '(a)'),
    H.q(2, 'Name each of the lines numbered 1 to 5.', ' (b)'), '2 + 3 + 3 + 3 + 2', 13,
    [point(f'r-{n}', f'{n} — {H.traced(lab)}', m, note) for n, lab, m, note in labels],
    kind='fixed', stem=q4, figure=q4_diagram, **A)
add('sa-q4-b', '2-0', 'the-competitive-firms-output', ref('A', 4, '(b)'),
    H.q(2, 'Show on the diagram the output the firm will produce in equilibrium', ' 2 Answer'), '3', 3,
    [ask_row('r-q1', 'Show on the diagram the output the firm will produce in equilibrium', 3,
             H.traced('Q1 3 marks ( If Q1 not stated but line drawn – 1 mark)') + '. The diagram is shown with the answer: a line '
             'from where MC cuts the lowest point of AC down to the quantity axis.')],
    kind='fixed', stem=q4, figure=SOL + 'p05-q4-diagram', **A)
beside_ask(cards[-1], q4_diagram)

# Q5 ─ barriers to trade
q5_barriers = [H.q(3, a, b) for a, b in (('A. Administrative barriers', ' 1. A payment'), ('B. Embargo', ' 2. A limit'),
                                         ('C. Quota', ' 3. Rules'), ('D. Subsidy', ' 4. A tax'), ('E. Tariff', ' 5. A total'))]
q5_explained = [H.q(3, a, b) for a, b in (('1. A payment to exporters', ' B. Embargo'), ('2. A limit on the quantity', ' C. Quota'),
                                          ('3. Rules / regulations', ' D. Subsidy'), ('4. A tax on imports.', ' E. Tariff'),
                                          ('5. A total ban on imports.', ' BARRIER'))]
matches = (('Administrative barriers', 'Rules / regulations applying to imports.'), ('Embargo', 'A total ban on imports.'),
           ('Quota', 'A limit on the quantity of goods imported.'), ('Tariff', 'A tax on imports.'))
add('sa-q5', '4-2', 'matching-barriers-to-trade', ref('A', 5),
    # The two printed lists follow the ask, each read down as printed (the text layer interleaves them).
    f"{H.q(3, 'In relation to the following barriers to trade, match the barrier', ' Barrier')} "
    f"Barrier: {' '.join(q5_barriers)} Explanation: {' '.join(q5_explained)}", '6 + 6 + 2 + 2', 16,
    [anyN('r-1', 'Each barrier matched', 16, 4, 6, [f'{H.traced(b)} — {H.traced(e)}' for b, e in matches],
          'The four the paper leaves open (D, Subsidy, is matched for illustration): ' + H.traced('1st and 2nd correct response: 2 x 6 marks each.')
          + ' ' + H.traced('3rd and 4th correct responses: 2 x 2 marks each.'), steps=[6, 6, 2, 2])],
    kind='fixed', **A)

# Q6 ─ an economic good
add('sa-q6', '0-1', 'an-economic-good', ref('A', 6),
    f"{H.q(3, 'Explain the term economic good.', ' Explanation:')} {H.q(3, 'Circle only two of these:', ' (17 marks)')}",
    '2 @ 4 + 5 + 4', 17,
    [anyN('r-explanation', 'A point of the explanation — any two', 8, 2, 4,
          [H.traced(x) for x in ('SCARCE', 'commands a PRICE', 'TRANSFERABLE', 'provides UTILITY')],
          'The explanation: ' + H.traced('Any two points of information x 4 marks each = 8 marks.') + ' The scheme’s sentence: '
          + H.traced('It is a good which is SCARCE / commands a PRICE, is TRANSFERABLE and provides UTILITY.')),
     anyN('r-circled', 'The two economic goods circled', 9, 2, 5, [H.traced('Cars'), H.traced('Food')],
          'The two goods: ' + H.traced('1st correct response: 5 marks. 2nd correct response: 4 marks.'), steps=[5, 4])],
    kind='fixed', **A)

# Q7 ─ what influences consumer demand
sentences = (('The price of the good itself.', 'TRUE'), ('The cost of producing the good.', 'FALSE'),
             ('The state of production technology.', 'FALSE'), ('The income of the consumer.', 'TRUE'))
add('sa-q7', '1-1', 'what-influences-consumer-demand', ref('A', 7, '(i)–(iv)'),
    f"{H.q(3, 'Some of the factors outlined below influence consumer demand for a good.', ' SENTENCE')} "
    f"{H.q(3, '(i) The price of the good itself.', ' (17 marks)')}", '6 + 6 + 3 + 2', 17,
    [anyN('r-1', 'Each sentence marked true or false', 17, 4, 6, [f'{H.traced(s)} — {H.traced(t)}' for s, t in sentences],
          'All four: ' + H.traced('1st and 2nd correct responses: 2 x 6 marks') + ', the 3rd 3 and the 4th 2.', steps=[6, 6, 3, 2])],
    kind='fixed', **A)

# Q8 ─ the government's economic aims
add('sa-q8', '3-1', 'other-economic-aims', ref('A', 8),
    H.q(3, 'State three other economic aims of the Government.', ' (i)'), '9 + 4 + 4', 17,
    [anyN('r-1', 'An aim — any three', 17, 3, 9,
          numbered('1. Increase employment / decrease unemployment', '\n⟨(17 marks)⟩',
                   [f'{n}. ' for n in range(1, 14)]),
          'Three aims: ' + H.traced('1st correct response: 9 marks. 2nd & 3rd: 4 marks each.'), steps=[9, 4, 4])],
    kind='fixed', stem=H.q(3, 'One of the economic aims of the Irish Government at present', ' State three'), **A)

# Q9 ─ national income with trade
add('sa-q9', '3-0', 'national-income-with-trade', ref('A', 9),
    H.q(3, 'If National Income (Y) =C + I + G = €2,400m, calculate the National Income', ' WORKINGS'), '3 @ 3 + 2 @ 2 + 4', 17,
    [anyN('r-figures', 'Each figure in the working', 9, 3, 3, [H.traced(x) for x in ('€2,400m', '€300m', '€200m')],
          H.traced('Each component: 3 figures x 3 marks each = 9 marks') + ', in ' + H.traced('Y = €2,400m + €300m - €200m')
          + '. The working is shown with the answer.'),
     anyN('r-signs', 'Each sign', 4, 2, 2, [H.traced('+ €300m'), H.traced('- €200m')],
          H.traced('2 signs x 2 marks each = 4 marks') + ': exports added and imports taken away.'),
     point('r-answer', H.traced('€ 2,500 m'), 4, H.traced('Correct answer = 4 marks') + '.')],
    kind='fixed', figure=SOL + 'p06-q9-working', **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ monopoly; barriers to entry; the ESB
q1 = H.q(4, 'The diagram below represents a Monopoly firm in equilibrium.', ' P MC')
q1_diagram = PAP + 'p04-q1-diagram'
titles = (('Marginal Cost', 4, 'MC, 4 marks (2 + 2).'), ('Average Cost', 4, 'AC, 4 marks (2 + 2).'),
          ('Marginal Revenue', 4, 'MR, 4 marks (2 + 2).'), ('Average Revenue / Demand', 4, 'AR, 4 marks (2 + 2).'),
          ('Quantity', 3, 'Q, 3 marks.'), ('Price', 3, 'P, 3 marks.'))
add('sb-q1-a-i', '2-0', 'labelling-the-monopoly-diagram', ref('B', 1, '(a)(i)'),
    H.q(4, 'Copy the diagram into your answer book. Write out each of the six labels', ' (ii)'), '4 + 4 + 4 + 4 + 3 + 3', 22,
    [point(f'r-{i}', H.traced(t), m, n) for i, (t, m, n) in enumerate(titles, 1)],
    kind='fixed', stem=q1, figure=q1_diagram, **B)
add('sb-q1-a-ii', '2-0', 'price-and-cost-in-monopoly', ref('B', 1, '(a)(ii)'),
    H.q(4, 'The firm produces Q1 output in equilibrium.', ' (30 marks)'), '4 + 4', 8,
    [anyN('r-1', 'P1 and C1 — both', 8, 2, 4,
          [f"{H.traced('P1')} — {H.traced('the price charged for this output')}",
           f"{H.traced('C1')} — {H.traced('the average cost of producing this output')}"],
          'Both: ' + H.traced('1st correct response: 4 marks. 2nd correct response: 4 marks.') + ' The diagram is shown with the answer.')],
    kind='fixed', stem=q1, figure=SOL + 'p07-q1a-diagram', **B)
beside_ask(cards[-1], q1_diagram)
add('sb-q1-b', '2-0', 'barriers-to-a-monopoly-market', ref('B', 1, '(b)(i)–(ii)'),
    ' '.join([H.q(4, '(i) State three possible barriers.', ' (ii)'), H.q(4, '(ii) Write brief notes on each of these.', ' (21 marks)')]),
    '11 + 5 + 5', 21,
    [anyN('r-1', 'A barrier stated and explained — any three', 21, 3, 11,
          H.split('Ownership of a Patents / Copyrights', '1st correct response: 11 marks.',
                  ['Ownership of a Patents / Copyrights', 'Government Regulation / Legal restrictions', 'Trade Agreements & Collusion.',
                   'Ownership of raw materials', 'Industry requires a large investment', 'Mergers / Takeovers',
                   'Monopolies based on fear, force or threats', 'Limit pricing', 'Proliferation of brands on the market']),
          'Three barriers, each stated for (i) and explained for (ii), on one ladder: ' + H.traced('1st correct response: 11 marks. State: 8 marks. Explain: 3 marks.')
          + ' ' + H.traced('2nd and 3rd correct responses: 2 x 5 marks each. State: 3marks. Explain: 2 marks.') + ' '
          + H.traced('Example on its own of each barrier with no explanation: 1 mark only.'), steps=[11, 5, 5])],
    kind='fixed', stem=H.q(4, 'New firms may wish to enter a monopoly market', ' (i)'), **B)
q1c = H.q(4, 'The Electricity Supply Board (ESB) is facing increasing competition', ' (i)')
add('sb-q1-c-i', '1-3', 'privatisation', ref('B', 1, '(c)(i)'), H.q(4, 'Explain the underlined term.', ' (ii)'), '6', 6,
    [heading('r-1', 'Privatisation — either', [H.traced('This is the sale of a state owned company to private owners.'),
                                               H.traced('The transfer of ownership from the Government owned public sector to the private sector.')],
             6, 'Privatisation, 6 marks (' + H.traced('3 marks + 3 marks') + '): the scheme accepts either.')],
    kind='fixed', stem=q1c, **B)
add('sb-q1-c-ii', '1-3', 'a-competitor-to-the-esb', ref('B', 1, '(c)(ii)'),
    H.q(4, 'Name one company currently competing with the ESB', ' (iii)'), '6', 6,
    [point('r-1', H.traced('Bord Gais / Air Tricity'), 6, 'One company, 6 marks: either.')], stem=q1c, **B)
esb = {
    'consumers': [unnum(cc(x)) for x in ('1. Quality / Choice of services', '2. More competitive prices', '3. Continuity of supply',
                                         '1. Loss of non-profit making', '2. Standards of service', '3. Preference to meet shareholders',
                                         '4. Increased prices / Charges')],
    'employees': [unnum(cc(x)) for x in ('1. Reward/Incentive for innovation.', '2. Employment opportunities', '3. Voluntary redundancy',
                                         '1. Loss of job / reduced job security.', '2. Changed working environment', '3. Curtailment in Pay')],
    'government': [unnum(cc(x)) for x in ('1. Revenue from Sale', '2. Opportunities of citizens', '3. Allows private sector to grow.',
                                          '4. Government retain part ownership', '1. Loss of control', '2. Control may go outside',
                                          '3. Increased unemployment.', '4. Loss of future revenues')],
}
add('sb-q1-c-iii', '1-3', 'privatising-the-esb', ref('B', 1, '(c)(iii)'),
    H.q(4, 'State and explain one way any two of the following may be affected', ' (24 marks)'), '6 + 6', 12,
    [anyN('r-1', 'One way for each of any two groups', 12, 2, 6,
          side('CONSUMERS', esb['consumers']) + side('EMPLOYEES', esb['employees']) + side('GOVERNMENT', esb['government']),
          'One way for each of two groups, positive or negative: ' + H.traced('Any 1 x 6 marks. State: 3m. Explain: 3m') + ' a group.')],
    kind='fixed', stem=q1c, **B)

# Q2 ─ the umbrella market; shifts; motorways and rail
q2 = H.q(5, 'The information below represents the expected demand and the planned supply schedule', ' Price')
q2_table = PAP + 'p05-q2-table'
add('sb-q2-a', '1-0', 'the-umbrella-market', ref('B', 2, '(a)(i)–(iii)'),
    ' '.join([H.q(5, 'Using the above data and one diagram', ' (a)'), H.q(5, '(i) Draw and label the market demand curve', ' (25 marks)')]),
    '8 + 8 + 4 + 3 + 2', 25,
    [point('r-demand', H.traced('D/C: 4 points x 2 marks each = 8 marks'), 8,
           '(i) The demand curve, 8 marks: ' + H.traced('(exclude: €3 and 400 units)') + ', the point the curves share. The completed '
           'graph is shown with the answer.'),
     point('r-supply', H.traced('S/C: 4 points x 2 marks each = 8 marks'), 8, '(ii) The supply curve, 8 marks, the same way.'),
     point('r-labels', H.traced('Labels: P, Q, D/C and S/C'), 4, 'The four labels, ' + H.traced('4 marks (4 x 1 marks each)') + '.'),
     anyN('r-equilibrium', 'The equilibrium price and quantity — both', 5, 2, 3, [H.traced('PE'), H.traced('QE')],
          '(iii) ' + H.traced('Pe and Qe : 1st correct response: 3 marks. 2nd correct response: 2 marks.') + ' '
          + H.traced('(1 mark each if lines drawn but Pe and Qe are not labelled).'), steps=[3, 2])],
    kind='fixed', stem=q2, figure=SOL + 'p11-q2a-graph', **B)
beside_ask(cards[-1], q2_table)
rain = [unx(x) for x in cc('x More people will want / need umbrellas').split(' x ')]
truck = [unx(x) for x in cc('x Less umbrellas will be supplied').split(' x ')]
add('sb-q2-b', '1-0', 'shifts-in-the-umbrella-market', ref('B', 2, '(b)(i)–(iii)'),
    ' '.join([H.q(5, 'In relation to each of the above statements, answer the three following questions:', ' (i)'),
              H.q(5, '(i) state whether the demand curve or supply curve will shift;', ' (20 marks)')]), '(3 + 3 + 4) x 2', 20,
    [point('r-rain-curve', f"{H.traced('Unexpected heavy rainfall')} — {H.traced('Demand Curve')}", 3, 'Heavy rainfall: (i) the demand curve, 3 marks.'),
     point('r-rain-direction', f"{H.traced('Unexpected heavy rainfall')} — {H.traced('Right')}", 3, 'Heavy rainfall: (ii) to the right, 3 marks.'),
     point('r-rain-why', ' — '.join(rain), 4,
           'Heavy rainfall: (iii) why, 4 marks: the scheme prints 2 beside each of its two points, the second put either way.'),
     point('r-truck-curve', f"{H.traced('Breakdown of the main supply truck')} — {H.traced('Supply Curve')}", 3,
           'The supply truck: (i) the supply curve, 3 marks.'),
     point('r-truck-direction', f"{H.traced('Breakdown of the main supply truck')} — {H.traced('Left')}", 3, 'The supply truck: (ii) to the left, 3 marks.'),
     point('r-truck-why', ' — '.join(truck), 4,
           'The supply truck: (iii) why, 4 marks: 2 beside each of its two points, the second put either way.')],
    kind='fixed', stem=H.q(5, 'The demand curve for umbrellas OR the supply curve for umbrellas', ' In relation'), **B)
q2c = H.q(5, 'The opening of new sections of motorways between Dublin and other Irish cities', ' (i)')
q2ci = H.q(5, 'Outline one possible economic advantage OR one possible economic disadvantage', ' (ii)')
motor = {'advantage': [unnum(cc(x)) for x in ('1. Safer Transport', '2. Quicker Journeys', '3. Improved lifestyle', '4. Employment / Government')],
         'disadvantage': [unnum(cc(x)) for x in ('1. Reduced economic activity', '2. Possibility of tolls', '3. Damage to environment',
                                                 '4. Opportunity cost')]}
for word, head in (('advantage', 'Possible economic advantage'), ('disadvantage', 'Possible economic disadvantage')):
    pick(f'sb-q2-c-i-{word}', '1-0', 'new-motorways-for-the-public', ref('B', 2, '(c)(i)', word),
         f'{q2ci} Justify the choice: {word.upper()}.', H.traced(head) + ' — any one', motor[word], 1, 6,
         'One ' + word + ', ' + H.traced('1 point x 6 marks. State: 3 marks. Explain: 3 marks') + '. The scheme credits an advantage '
         'and a disadvantage, each with its own column.', stem=q2c, **B)
pick('sb-q2-c-ii', '1-2', 'raising-demand-for-irish-rail', ref('B', 2, '(c)(ii)'),
     H.q(5, 'State and explain two actions Iarnród Eireann (Irish Rail) could take', ' (iii)'), 'An action — any two',
     numbered('1. Reduce prices to attract', '2 points x 6 marks each.', ['1. Reduce prices', '2. Incentives', '3. Advertising',
                                                                          '4. Increased frequency', '5. Improve quality']),
     2, 6, 'Two actions, ' + H.traced('2 points x 6 marks each. State: 3 marks each. Explain: 3 marks each.'), stem=q2c, **B)
pick('sb-q2-c-iii', '2-2', 'the-gains-from-public-transport', ref('B', 2, '(c)(iii)'),
     H.q(5, 'Explain two advantages for the Irish economy of increased use of public transport', ' (30 marks)'), 'An advantage — any two',
     numbered('1. Reduced traffic congestion resulting', '2 points x 6 marks each.',
              ['1. Reduced traffic', '2. Reduced carbon', '3. Reduced use of fossil', '4. Improved safety', '5. Improved utilisation',
               '6. Reduced imports', '7. Lower cost of living', '8. Increased employment']),
     2, 6, 'Two advantages, 6 marks each (3 + 3).', stem=q2c, **B)

# Q3 ─ costs; wages; the minimum wage
q3a = H.q(6, 'A retailer needs capital to commence business.', ' (i)')
add('sb-q3-a-i', '0-1', 'capital-as-a-factor', ref('B', 3, '(a)(i)'),
    H.q(6, 'Explain the term ‘capital’ as a factor of production.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('Anything man made which helps in the production of output.'), 6,
           'Capital, 6 marks, the scheme printing 4 marks beneath “man made” and 2 beneath “production of output”.')],
    stem=q3a, **B)
add('sb-q3-a-ii', '1-5', 'fixed-and-variable-costs', ref('B', 3, '(a)(ii)'),
    H.q(6, 'Define the terms fixed costs and variable costs.', ' (iii)'), '5 + 5', 10,
    [heading('r-fixed', 'Fixed Costs — either', [H.traced('costs which do not change as output changes'),
                                                  H.traced('those costs which have to paid, even if nothing is produced')], 5,
             'Fixed costs, 5 marks: the scheme prints “4 marks” and “1 marks” beside the definition, and accepts either.'),
     point('r-variable', f"{H.traced('Variable Costs')} — {H.traced('costs which change as output changes')}", 5,
           'Variable costs, 5 marks, the same way (4 + 1).')],
    kind='fixed', stem=q3a, **B)
add('sb-q3-a-iii', '1-5', 'fixed-or-variable', ref('B', 3, '(a)(iii)'),
    H.q(6, 'State whether each of the three underlined costs above is an example', ' (25 marks)'), '3 + 3 + 3', 9,
    [point('r-rent', f"{H.traced('Rent')} — {H.traced('Fixed Costs')}", 3, 'Rent, a fixed cost: 3 marks.'),
     point('r-stock', f"{H.traced('Stock')} — {H.traced('Variable Costs')}", 3, 'Stock, a variable cost: 3 marks.'),
     point('r-wages', f"{H.traced('Wages')} — {H.traced('Variable Costs')}", 3, 'Wages, a variable cost: 3 marks.')],
    kind='fixed', stem=q3a, **B)
q3b = H.q(6, 'Wage levels have fallen in both the public sector and the private sector in Ireland.', ' (i)')
add('sb-q3-b-i', '3-1', 'the-public-and-private-sectors', ref('B', 3, '(b)(i)'),
    H.q(6, 'Explain each of the underlined terms and state one example of an occupation in each.', ' (ii)'), '3 + 2 + 2 + 2', 9,
    [point('r-public', 'Public sector — ' + H.opt('That part of the economy which is run by state bodies', '\nExample: a teacher'), 3,
           'The public sector, ' + H.traced('5 marks ( 3 + 2 for example )') + ': the explanation 3.'),
     point('r-public-example', H.traced('Example: a teacher'), 2, 'A public-sector occupation, 2 marks: the scheme’s is an example.'),
     point('r-private', 'Private sector — ' + H.opt('That part of the economy which is run by private individuals', '\nExample: a shop worker'), 2,
           'The private sector, ' + H.traced('4 marks ( 2 + 2 for example )') + ': the explanation 2.'),
     point('r-private-example', H.traced('Example: a shop worker'), 2, 'A private-sector occupation, 2 marks: the scheme’s is an example.')],
    kind='fixed', stem=q3b, **B)
businesses = [unnum(cc(x)) for x in ('1. Reduced costs / Lower prices', '2. Continuity of production', '3. Hiring additional labour',
                                     '4. Reduced demand for output', '5. Difficulty in filling')]
govfin = [unnum(cc(x)) for x in ('1. Reduced current expenditure', '2. Reduced borrowing', '3. Reduced direct tax revenue.',
                                 '4. Reduced VAT / Excise', '5. Effect on social welfare')]
add('sb-q3-b-ii', '2-1', 'falling-wages-for-business-and-the-state', ref('B', 3, '(b)(ii)'),
    H.q(6, 'Discuss two economic effects which falling wage levels may have on each of the following:', ' (25 marks)'), '2 @ 4 + 2 @ 4', 16,
    [anyN('r-businesses', 'An effect on businesses — any two', 8, 2, 4, businesses,
          'Businesses: two effects, ' + H.traced('2 x 4 marks each.') + ' ' + H.traced('State: 2 marks. Explain: 2 marks.')),
     anyN('r-government', 'An effect on government finance — any two', 8, 2, 4, govfin,
          'Government finance: two effects, 4 marks each (2 + 2).')],
    kind='fixed', stem=q3b, **B)
q3c = H.q(6, 'In the Government’s Budget introduced in December 2010', ' (i)')
add('sb-q3-c-i', '2-1', 'the-national-minimum-wage', ref('B', 3, '(c)(i)'), qa(6, 'per hour.', 'Explain the underlined term.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('The lowest wage that employers must, by law, pay their employees.'), 5,
           'The minimum wage, 5 marks, the scheme printing 2 beneath “lowest wage” and 3 beneath “by law”.')],
    stem=q3c, **B)
pick('sb-q3-c-ii', '2-1', 'why-the-minimum-wage-was-cut', ref('B', 3, '(c)(ii)'),
     H.q(6, 'State two economic reasons why, in your opinion, the national minimum wage was reduced.', ' (iii)'), 'A reason — any two',
     H.split('1. Reduce costs / restore competitiveness:', '2 x 5 marks each = 10 marks.',
             ['Reduce costs / restore competitiveness:', 'Reduce prices:', 'Increase employment:', 'Attract investment:',
              'Encourage MNCs to stay in Ireland:']),
     2, 5, 'Two reasons, ' + H.traced('2 x 5 marks each = 10 marks.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks'), stem=q3c, **B)
pick('sb-q3-c-iii', '2-1', 'a-lower-minimum-wage-for-workers', ref('B', 3, '(c)(iii)'),
     H.q(6, 'Outline two possible economic effects of this wage reduction for the Irish worker.', ' (25 marks)'), 'An effect — any two',
     H.split('1. Lower standard of living:', '2 x 5 marks each = 10 marks.',
             ['Lower standard of living:', 'Lower productivity:', 'Reduced incentive to work:', 'Increase in debt / mortgage arrears',
              'Less leisure time:']),
     2, 5, 'Two effects, 5 marks each (2 + 3).', stem=q3c, **B)

# Q4 ─ visible trade; the small open economy; tourism
q4b_ = H.q(6, 'You are given the following information about a country’s trade.', ' Visible Exports')
q4_table = PAP + 'p06-q4-table'
add('sb-q4-a-i', '4-2', 'visible-exports-and-imports', ref('B', 4, '(a)(i)'),
    H.q(6, 'Explain the terms ‘visible exports’ and ‘visible imports’', ' (ii)'), '5 + 2 + 5 + 2', 14,
    [point('r-exports', f"{H.traced('Visible exports')} — {cc('The sale of Irish goods abroad / to consumers outside Ireland', whole=True)}", 5,
           'Visible exports, ' + H.traced('5 marks ( 3 + 2 )') + '.'),
     heading('r-exports-example', 'An example of a visible export — any one',
             [unx(x) for x in cc('x Sale of Irish beef abroad.').split(' x ')], 2, H.traced('One example: 2 marks') + '.'),
     point('r-imports', f"{H.traced('Visible imports')} — {cc('The purchase of foreign goods from abroad / by Irish consumers', whole=True)}", 5,
           'Visible imports, 5 marks (3 + 2).'),
     heading('r-imports-example', 'An example of a visible import — any one',
             [unx(x) for x in cc('x Purchase of foreign cars.').split(' x ')], 2, 'One example, 2 marks.')],
    kind='fixed', stem=q4b_, figure=q4_table, **B)
add('sb-q4-a-ii', '4-2', 'the-new-balance-of-trade', ref('B', 4, '(a)(ii)'),
    H.q(6, 'If the level of visible imports above increased by €600m', ' (iii)'), '7', 7,
    [point('r-1', H.traced('(€200m)'), 7,
           'The new balance of trade, 7 marks: visible exports €24,000m less visible imports of €23,600m + €600m = €24,200m, a '
           'balance of minus €200m. The working is shown with the answer.')],
    kind='fixed', stem=q4b_, figure=SOL + 'p17-q4aii-working', **B)
beside_ask(cards[-1], q4_table)
add('sb-q4-a-iii', '4-2', 'surplus-or-deficit', ref('B', 4, '(a)(iii)'),
    H.q(6, 'State whether the new Balance of Trade is a surplus or deficit', ' (25 marks)'), '2 + 2', 4,
    [point('r-deficit', H.traced('The Balance of Trade has now changed to a deficit.'), 2, 'A deficit, 2 marks.'),
     point('r-why', H.traced('Because (visible) imports exceed (visible) exports.'), 2, 'Why, 2 marks.')],
    kind='fixed', stem=q4b_, figure=q4_table, **B)
q4b = H.q(6, 'Ireland as a small open economy relies on international trade.', ' (i)')
add('sb-q4-b-i', '4-2', 'a-small-open-economy', ref('B', 4, '(b)(i)'), qa(6, 'relies on international trade.', 'Explain the underlined term.', ' (ii)'), '5', 5,
    [point('r-1', H.traced('An economy which engages in trade / imports and exports.'), 5, 'A small open economy, 5 marks.')], stem=q4b, **B)
pick('sb-q4-b-ii', '4-2', 'why-ireland-must-trade', ref('B', 4, '(b)(ii)'),
     H.q(6, 'State and explain three economic reasons why Ireland needs to engage in trade.', ' (20 marks)'), 'A reason — any three',
     H.split('1. Job creation.', '3 x 5 marks each.',
             ['Job creation.', 'Increased GNP / Economic growth', 'Increased sales', 'Earn foreign currencies', 'Attract investment',
              'More choice for consumers', 'Raw materials unavailable in Ireland', 'Enhanced international reputation']),
     3, 5, 'Three reasons, ' + H.traced('3 x 5 marks each. State: 2 marks. Explain: 3 marks.'), stem=q4b, **B)
q4c = H.q(6, 'Overseas visitors to Ireland are an example of an invisible export.', ' (i)')
add('sb-q4-c-i', '4-2', 'an-invisible-export', ref('B', 4, '(c)(i)'), qa(6, 'an invisible export.', 'Explain the underlined term.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('The purchase of an Irish service (4 ) by a foreign citizen / the money comes into Ireland. (2)'), 6,
           'An invisible export, 6 marks: an Irish service 4 and bought by a foreign citizen 2.')],
    stem=q4c, **B)
pick('sb-q4-c-ii', '4-2', 'gains-from-more-overseas-visitors', ref('B', 4, '(c)(ii)'),
     H.q(6, 'State and explain two benefits for the Irish economy of an increase in the number', ' (iii)'), 'A benefit — any two',
     H.split('1. Increased employment\nMore jobs', '2 points x 6 marks each.',
             ['Increased employment', 'Increased income / GNP', 'Benefits to business', 'Tax revenues']),
     2, 6, 'Two benefits, ' + H.traced('2 points x 6 marks each. State: 3 marks. Explain: 3 marks') + '.', stem=q4c, **B)
pick('sb-q4-c-iii', '4-2', 'attracting-overseas-visitors', ref('B', 4, '(c)(iii)'),
     H.q(6, 'State and explain two actions which the Irish Tourist Industry could take', ' (30 marks)'), 'An action — any two',
     H.split('1. Reduce air fares', '2 points x 6 marks each.',
             ['Reduce air fares', 'Advertising', 'More competitive prices for accommodation', 'Special promotions', 'Car hire:',
              'Industry lobbying of Government']),
     2, 6, 'Two actions, 6 marks each (3 + 3).', stem=q4c, **B)

# Q5 ─ the current budget; water charges; the national debt
q5a = H.q(7, 'The Irish Government’s Current Budget Deficit was €11.5 m', ' (i)')
add('sb-q5-a-i', '3-1', 'the-current-budget', ref('B', 5, '(a)(i)'), qa(7, 'Current Budget Deficit', 'Explain each of the underlined terms.', ' (ii)'), '5 + 4 + 4', 13,
    [point('r-deficit', 'Current Budget Deficit — ' + H.traced('Government current spending exceeds government current income.'), 5,
           'The current budget deficit, 5 marks: 1 beneath each of five words.'),
     point('r-income', 'Government current income — ' + H.traced('Income received by the government on a continuous / day-to-day basis.'), 4,
           H.traced('Government current income – 4 marks') + ' (2 + 2).'),
     point('r-spending', 'Government current spending — ' + H.traced('Spending by the government on a continuous / day-to-day basis.'), 4,
           H.traced('Government current spending – 4 marks') + ' (2 + 2).')],
    kind='fixed', stem=q5a, **B)
income = H.cut_cell('Government Current Income 1. Direct tax revenue',
                    ['1. Direct tax revenue', '2. Indirect tax', '3. National lottery', '4. Interest on loans', '5. Surpluses',
                     '6. Departmental', '7. Prize Bond', '8. Fees charged'])
spending = H.cut_cell('Government Current Expenditure 1. Salaries',
                      ['1. Salaries', '2. Cost of running government', '3. Costs of running state', '4. Social welfare',
                       '5. National debt service', '6. Grants to local', '7. Ireland’s contribution'])
add('sb-q5-a-ii', '3-1', 'current-income-and-spending', ref('B', 5, '(a)(ii)'),
    H.q(7, 'State two examples of Government Current Income and two examples', ' (25 marks)'), '2 @ 3 + 2 @ 3', 12,
    [anyN('r-income', 'An example of current income — any two', 6, 2, 3, [unnum(x) for x in income],
          'Current income: ' + H.traced('2 x 3 marks each = 6') + '.'),
     anyN('r-spending', 'An example of current spending — any two', 6, 2, 3, [unnum(x) for x in spending],
          'Current spending: two examples, 3 marks each.')],
    kind='fixed', stem=q5a, **B)
q5b = H.q(7, 'The Irish Government is considering the introduction of household water charges.', ' (i)')
pick('sb-q5-b-i', '3-1', 'why-water-charges', ref('B', 5, '(b)(i)'),
     H.q(7, 'Outline two economic reasons for the introduction of these charges.', ' (ii)'), 'A reason — any two',
     [unnum(cc(x)) for x in ('1. Revenue for government', '2. Evasion eliminated', '3. Employment in metering', '4. Development of infrastructure',
                             '5. Water conservation')],
     2, 5, 'Two reasons, ' + H.traced('2 x 5 marks each.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks'), stem=q5b, **B)
pick('sb-q5-b-ii', '3-1', 'water-charges-and-households', ref('B', 5, '(b)(ii)'),
     H.q(7, 'Discuss two economic effects of these charges on households.', ' (20 marks)'), 'An effect — any two',
     [unnum(cc(x)) for x in ('1. Lower standard of living', '2. Inequitable', '3. Reduced economic growth', '4. Household budgeting')],
     2, 5, 'Two effects, 5 marks each (2 + 3).', stem=q5b, **B)
q5c = H.q(7, 'Ireland’s National Debt as a percentage of GDP is continuing to increase.', ' (i)')
add('sb-q5-c-i', '3-1', 'the-national-debt', ref('B', 5, '(c)(i)'), qa(7, 'continuing to increase.', 'Explain the underlined term.', ' (ii)'), '6', 6,
    [point('r-1', H.traced('the total amount / cumulative of government borrowing which is outstanding.'), 6,
           'The national debt, 6 marks: the scheme prints 3, 2 and 1 beneath its three bold phrases.')], stem=q5c, **B)
add('sb-q5-c-ii', '3-0', 'what-gdp-stands-for', ref('B', 5, '(c)(ii)'), H.q(7, 'What do the initials GDP stand for?', ' (iii)'), '2 + 2 + 2', 6,
    [point('r-gross', 'GDP — ' + H.traced('Gross'), 2, 'Each word, ' + H.traced('6 marks (2 + 2 + 2)') + '.'),
     point('r-domestic', 'GDP — ' + H.traced('Domestic'), 2, 'Domestic, 2 marks.'),
     point('r-product', 'GDP — ' + H.traced('Product'), 2, 'Product, 2 marks.')],
    kind='fixed', stem=q5c, **B)
pick('sb-q5-c-iii', '3-1', 'why-the-national-debt-has-grown', ref('B', 5, '(c)(iii)'),
     H.q(7, 'State one reason why Ireland’s National Debt has been increasing', ' (iv)'), 'A reason — any one',
     numbered('1. Increased borrowing by the state for current', '1 x 6 marks',
              ['1. Increased borrowing by the state for current', '2. Increased borrowing by the state for infrastructural',
               '3. Increased interest rates', '4. Borrowing to finance']),
     1, 6, 'One reason, ' + H.traced('1 x 6 marks') + '.', stem=q5c, **B)
pick('sb-q5-c-iv', '3-1', 'disadvantages-of-a-rising-national-debt', ref('B', 5, '(c)(iv)'),
     H.q(7, 'State and explain two economic disadvantages which may result', ' (30 marks)'), 'A disadvantage — any two',
     H.split('1. Opportunity costs involved.', '2 points x 6 marks each.',
             ['Opportunity costs involved.', 'Increased burden on taxpayers.', 'Increased annual interest repayments.',
              'Risk to provision of public services', 'Reduced public confidence.', 'Diminished international credit-rating.',
              'EU / IMF: conditions applied to Ireland.']),
     2, 6, 'Two disadvantages, ' + H.traced('2 points x 6 marks each.') + ' ' + H.traced('State: 3 marks. Explain: 3 marks.'), stem=q5c, **B)

# Q6 ─ national income and the multiplier; ghost estates; infrastructure
q6a = H.q(7, 'The ‘Multiplier effect’ tells us by how much National Income will increase', ' (i)')
add('sb-q6-a-i', '3-0', 'national-income', ref('B', 6, '(a)(i)'), qa(7, 'increase in government spending', 'Explain the underlined term.', ' (ii)'), '6', 6,
    [point('r-1', H.opt('Income earned by the permanent residents of a country from current economic activity', '\n2 marks'), 6,
           'National income, 6 marks: the scheme prints 2 beneath each of its three phrases.')], stem=q6a, **B)
pick('sb-q6-a-ii', '3-0', 'effects-of-an-injection', ref('B', 6, '(a)(ii)'),
     H.q(7, 'Outline two economic effects which an injection may have on an economy.', ' (iii)'), 'An effect — any two',
     H.split('1. Increased demand\nAn injection', '2 x 6 marks each.',
             ['Increased demand', 'Increased employment', 'Increased inflation', 'Increased savings', 'Increased imports',
              'Government revenues']),
     2, 6, 'Two effects, ' + H.traced('2 x 6 marks each.') + ' ' + H.traced('State: 3 marks. Explain: 3 marks.'), stem=q6a, **B)
add('sb-q6-a-iii', '3-0', 'the-new-national-income', ref('B', 6, '(a)(iii)'),
    H.q(7, 'Calculate the new level of National Income.', ' (25 marks)'), '1 + 1 + 1 + 1 + 3', 7,
    [point('r-injection', H.traced('€20m'), 1, 'The working ' + H.traced('€20m x 2 = €40m + €600m = €640m') + ': the injection, 1 mark.'),
     point('r-multiplier', H.traced('x 2'), 1, 'Times the multiplier, 1 mark.'),
     point('r-increase', H.traced('€40m'), 1, 'The increase, 1 mark.'),
     point('r-old', H.traced('+ €600m'), 1, 'Added to the old national income, 1 mark.'),
     point('r-answer', H.traced('€640m'), 3, 'The new national income, 3 marks.')],
    kind='fixed', stem=f"{q6a} {H.q(7, 'Given the following information:', ' Calculate')}", **B)
q6b = H.q(7, 'The fall in demand for residential property (houses)', ' (i)')
pick('sb-q6-b-i', '1-0', 'why-demand-for-houses-fell', ref('B', 6, '(b)(i)'),
     H.q(7, 'State and explain two reasons for the falling demand for residential property.', ' (ii)'), 'A reason — any two',
     [pair(x) for x in ('Higher interest rates', 'Availability of loans', 'Economic recession', 'Speculation in houses.',
                        'Expectations re: future prices', 'Increased emigration / decreased immigration')],
     2, 6, 'Two reasons, ' + H.traced('2 x 6 marks each. State: 3 marks. Explain: 3 marks.'), stem=q6b, **B)
pick('sb-q6-b-ii', '1-0', 'why-ghost-estates-grew', ref('B', 6, '(b)(ii)'),
     H.q(7, 'State and explain one reason for the growth in these ‘ghost estates’.', ' (iii)'), 'A reason — any one',
     H.split('1. Surplus of houses', '1 x 5 marks.', ['Surplus of houses', 'Developers going bust / lack of finance',
                                                       'Unemployment / Economic recession']),
     1, 5, 'One reason, ' + H.traced('1 x 5 marks. State: 2 marks. Explain: 3 marks.'), stem=q6b, **B)
pick('sb-q6-b-iii', '1-0', 'what-to-do-with-ghost-estates', ref('B', 6, '(b)(iii)'),
     H.q(7, 'Suggest two economic actions the Government could take', ' (25 marks)'), 'An action — any two',
     numbered('1. Demolish the unfinished houses', '2 x 4 marks each.', ['1. Demolish', '2. Complete the houses and make', '3. Complete the houses and try']),
     2, 4, 'Two actions, ' + H.traced('2 x 4 marks each.'), stem=q6b, **B)
q6c = H.q(7, 'The Construction Industry Federation (CIF) favours increased spending', ' (i)')
add('sb-q6-c-i', '3-1', 'infrastructure-and-opportunity-cost', ref('B', 6, '(c)(i)'),
    qa(7, 'involves an opportunity cost.', 'Explain each of the underlined terms.', ' (ii)'), '3 + 3 + 6', 12,
    [heading('r-infrastructure', 'Infrastructure — any one',
             [H.traced(x) for x in ('Those goods /services which are essential for the smooth running of an economy.',
                                    'Those goods /services which industry requires to function properly.',
                                    'Capital equipment used to supply publicly available services')], 3,
             'Infrastructure, 6 marks with its examples: the scheme prices its examples 3 in '
             'brackets, so the explanation is read here as the other 3.'),
     point('r-examples', H.traced('Examples: transport, telecommunications, electricity and gas, water supplies'), 3,
           'Examples of infrastructure, ' + H.traced('3 marks') + '.'),
     heading('r-opportunity-cost', 'Opportunity cost — any one',
             [H.traced(x) for x in ('The cost of foregone alternatives.', 'The cost of passing up the next best alternative when making a decision.',
                                    'The amount of other goods / services which could have been obtained instead of any good.')], 6,
             'Opportunity cost, 6 marks.')],
    kind='fixed', stem=q6c, **B)
projects = [unx(x) for x in cc('x Terminal 2 Dublin Airport').split(' x ')] + [unx(x) for x in cc('x Broadband').split(' x ')]
pick('sb-q6-c-ii', '3-1', 'recent-infrastructure-projects', ref('B', 6, '(c)(ii)'),
     H.q(7, 'State two examples of major infrastructure projects recently completed in Ireland.', ' (iii)'), 'A project — any two',
     projects, 2, 4, 'Two projects, ' + H.traced('2 x 4 marks each.') + ' The scheme’s are examples.', stem=q6c, **B)
pick('sb-q6-c-iii', '3-1', 'why-keep-building-infrastructure', ref('B', 6, '(c)(iii)'),
     H.q(7, 'Outline one economic benefit for continuing to spend on Ireland’s infrastructure.', ' (25 marks)'), 'A benefit — any one',
     H.split('1. Reduced costs of completion', '1 x 5 marks.', ['Reduced costs of completion', 'Availability of labour', 'Economic growth',
                                                                 'Standard of living.']),
     1, 5, 'One benefit, ' + H.traced('1 x 5 marks.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks.'), stem=q6c, **B)

# Q7 ─ money; nationalised banks; Keynes
q7a = H.q(8, 'Currency is one form of money. One function of money is a store of wealth.', ' (i)')
add('sb-q7-a-i', '3-4', 'currency-and-a-store-of-wealth', ref('B', 7, '(a)(i)'), qa(8, 'store of wealth.', 'Explain each of the underlined terms.', ' (ii)'), '5 + 5', 10,
    [point('r-currency', 'Currency — ' + H.traced('Notes and coins used to buy goods and services.'), 5, H.traced('Currency: 5 marks') + '.'),
     point('r-store', 'Store of wealth — ' + H.traced('Allows people to save for the future.'), 5, H.traced('Store of wealth: 5 marks') + '.')],
    kind='fixed', stem=q7a, **B)
pick('sb-q7-a-ii', '3-4', 'other-functions-of-money', ref('B', 7, '(a)(ii)'),
     H.q(8, 'State and explain two other functions of money.', ' (iii)'), 'A function — any two',
     H.split('Medium of exchange\nx Money allows', '2 x 5 marks.', ['Medium of exchange', 'Measure of Value', 'Standard for Deferred Payment']),
     2, 5, 'Two functions, ' + H.traced('2 x 5 marks.') + ' ' + H.traced('State: 2 marks. Explain: 3 marks'), stem=q7a, **B)
pick('sb-q7-a-iii', '3-4', 'money-other-than-currency', ref('B', 7, '(a)(iii)'),
     H.q(8, 'State one example of money, other than currency.', ' (25 marks)'), 'An example — any one',
     [H.traced(x) for x in ('Cheques', 'Credit Cards', 'Debit Cards')], 1, 5, 'One example, ' + H.traced('1 x 5 marks') + '.', stem=q7a, **B)
q7b = H.q(8, 'Some banks in Ireland have been nationalised', ' (i)')
add('sb-q7-b-i', '3-4', 'nationalised-banks', ref('B', 7, '(b)(i)'),
    H.q(8, 'Explain the underlined term and name one bank that has been nationalised.', ' (ii)'), '5 + 2', 7,
    [point('r-nationalised', 'Nationalised — ' + H.traced('Taking of banks into public / government ownership.'), 5, 'Nationalised, 5 marks.'),
     point('r-bank', H.traced('Anglo Irish Bank'), 2, 'A nationalised bank, 2 marks.')],
    kind='fixed', stem=q7b, **B)
bank_groups = (('business', 'Business customers', H.cut_cell('1. Loss of local service/higher costs',
                                                              ['1. Loss of local', '2. Inconvenience', '3. Lack of relationship'])),
               ('employees', 'Employees', H.cut_cell('1. Loss of jobs Some', ['1. Loss of jobs', '2. Re-location'])),
               ('shareholders', 'Shareholders', H.cut_cell('1. Reduced profits If the bank', ['1. Reduced profits', '2. Poor publicity',
                                                                                                 '3. Reduction in share price'])))
add('sb-q7-b-ii', '3-4', 'when-a-bank-closes', ref('B', 7, '(b)(ii)'),
    H.q(8, 'Discuss one economic effect which the closure of a bank may have on each of the following:', ' (25 marks)'), '6 + 6 + 6', 18,
    [heading(f'r-{rid}', H.traced(group) + ' — any one', [unnum(x) for x in items], 6,
             f'{group}: one effect, ' + H.traced('3 points x 6 marks each.') + ' ' + H.traced('State: 3 marks. Explain: 3 marks.'))
     for rid, group, items in bank_groups],
    kind='fixed', stem=q7b, **B)
q7c = H.q(8, 'The economist, John Maynard Keynes, stated that people keep their wealth', ' Explain each')
add('sb-q7-c-i', '3-4', 'keynes-motives-for-holding-cash', ref('B', 7, '(c)(i)'),
    H.q(8, 'Explain each of the above reasons.', ' (ii)'), '6 + 6 + 6', 18,
    [point(f'r-{m.lower()}', pair(m), 6, f'{m}, ' + H.traced('3 x 6 marks each') + '.') for m in ('Transactionary', 'Precautionary', 'Speculative')],
    kind='fixed', stem=q7c, **B)
q7cii = H.q(8, 'Keynes favoured Government involvement/participation in an economy.', ' (25 marks)')
keynes = {'agree': ('Reasons for agreeing', [cc(x) for x in ('Redistribute wealth Government', 'Essential services Services',
                                                            'Economic growth Government', 'Create employment By',
                                                            'Protection of consumers Legislation', 'Prevent growth of private monopolies')]),
          'disagree': ('Reasons for disagreeing', [cc(x) for x in ('Decreased taxation Less', 'Costly / inefficient services The',
                                                                  'Discourage enterprise Costs', 'Stifle economic growth Excessive',
                                                                  'Borrowing by government Government')])}
for word, answer in (('agree', 'Yes'), ('disagree', 'No')):
    head, opts = keynes[word]
    add(f'sb-q7-c-ii-{word}', '0-0', 'do-you-agree-with-keynes', ref('B', 7, '(c)(ii)', word),
        f'{q7cii} Justify the choice: {answer.upper()}.', '1 + 6', 7,
        [point('r-answer', H.traced(answer), 1, 'The answer: ' + H.traced('Yes / No. 1 mark') + '. The scheme credits agreeing and '
               'disagreeing, each with its own column.'),
         anyN('r-reason', H.traced(head) + ' — any one', 6, 1, 6, opts, 'One reason, 6 marks. ' + H.traced('State: 3 marks. Explain: 3 marks.'))],
        kind='fixed', stem=q7c, **B)

# Q8 ─ the census; the retirement age; aid to LDCs
q8a = H.q(8, 'In April 2011 the CSO conducted a Census of Population', ' (i)')
add('sb-q8-a-i', '3-0', 'what-cso-stands-for', ref('B', 8, '(a)(i)'), H.q(8, 'What do the initials CSO stand for?', ' (ii)'), '3 + 3 + 3', 9,
    [point(f'r-{w.lower()}', 'CSO — ' + H.traced(w), 3, f'{w}, 3 marks' + (': ' + H.traced('9 marks (3 + 3 + 3)') if w == 'Central' else '') + '.')
     for w in ('Central', 'Statistics', 'Office')],
    kind='fixed', stem=q8a, **B)
add('sb-q8-a-ii', '3-5', 'a-census-of-population', ref('B', 8, '(a)(ii)'), H.q(8, 'Explain the meaning of the underlined term.', ' (iii)'), '4', 4,
    [point('r-1', H.traced('This is the official counting of the country’s population.'), 4, 'A census of population, 4 marks.')], stem=q8a, **B)
census_groups = (('business', 'Business', cc('Future levels of consumer demand Producers'),
                  ['Future levels of consumer demand', 'Population data', 'Labour market']),
                 ('local', 'Local government', cc('Housing requirements The local'),
                  ['Housing requirements', 'Provision of services', 'Need for facilities']),
                 ('central', 'Central Government', cc('Infrastructural requirements It helps'),
                  ['Infrastructural requirements', 'Provision of essential services', 'Pension / financial planning', 'Demographic changes',
                   'Qualifications of workforce']))
add('sb-q8-a-iii', '3-5', 'uses-of-census-data', ref('B', 8, '(a)(iii)'),
    H.q(8, 'Explain one use each of the following could make of the data collected:', ' (25 marks)'), '4 + 4 + 4', 12,
    [heading(f'r-{rid}', H.traced(group) + ' — any one', H.cut_cell(cell[:30], firsts), 4,
             f'{group}: one use, ' + H.traced('3 x 4 marks each – ONE POINT PER GROUP.') + ' ' + H.traced('State: 2 marks. Explain: 2 marks.'))
     for rid, group, cell, firsts in census_groups],
    kind='fixed', stem=q8a, **B)
q8b = H.q(8, 'The Irish Government increased the statutory retirement age from 65 to 68 years.', ' (i)')
pick('sb-q8-b-i', '3-1', 'why-raise-the-retirement-age', ref('B', 8, '(b)(i)'),
     H.q(8, 'State and explain a reason why the Government increased the retirement age.', ' (ii)'), 'A reason — any one',
     H.split('1. Reduce the costs of future pensions', '1 x 8 marks.', ['Reduce the costs of future pensions', 'People living longer.',
                                                                      'Retain experienced workforce']),
     1, 8, 'One reason, ' + H.traced('1 x 8 marks.') + ' ' + H.traced('State: 4 marks. Explain: 4 marks.'), stem=q8b, **B)
retire = (('labour', 'Irish Labour Market', H.cut_cell('1.Reduced job vacancies', ['1.Reduced job vacancies', '2. Days lost', '3. Productivity',
                                                                                    '4. Lower training costs'])),
          ('spending', 'Consumer spending', H.cut_cell('1. Increased spending by those', ['1. Increased spending', '2. Changed pattern'])))
add('sb-q8-b-ii', '2-1', 'a-later-retirement-age', ref('B', 8, '(b)(ii)'),
    H.q(8, 'State and explain one possible economic effect which an increase in the retirement age', ' (20 marks)'), '6 + 6', 12,
    [heading(f'r-{rid}', H.traced(group) + ' — any one', [H.traced(re.sub(r'^\d\.\s*', '', x)) for x in items], 6,
             f'{group}: one effect, ' + H.traced('2 x 6 marks each.') + ' ' + H.traced('State: 3 marks. Explain: 3 marks.'))
     for rid, group, items in retire],
    kind='fixed', stem=q8b, **B)
q8c = H.q(8, 'The Irish Government continues to spend on financial aid', ' (i)')
add('sb-q8-c-i', '4-0', 'economic-development', ref('B', 8, '(c)(i)'), qa(8, 'at a reduced level.', 'Explain the underlined term.', ' (ii)'), '4 + 2', 6,
    [anyN('r-1', 'The explanation — both points', 6, 2, 4,
          [H.traced('An increase in the level of income standard of living / output / GNP per person'),
           H.traced('accompanied by a change in the structure of society.')],
          'Economic development: ' + H.traced('1st correct response: 4 marks') + ', the 2nd 2. The scheme’s one sentence is read here '
          'as its two parts.', steps=[4, 2])],
    kind='fixed', stem=q8c, **B)
pick('sb-q8-c-ii', '4-0', 'less-aid-for-ldcs', ref('B', 8, '(c)(ii)'),
     H.q(8, 'State and explain two economic effects which this reduction in financial aid', ' (iii)'), 'An effect — any two',
     H.split('1. Reduced standard of living\nWith less', '2 points x 6 marks each.',
             ['Reduced standard of living', 'Deterioration in infrastructure', 'Increased poverty', 'Increased death rates',
              'Decline in provision of services']),
     2, 6, 'Two effects, ' + H.traced('2 points x 6 marks each.') + ' ' + H.traced('State: 3 marks. Explain: 3 marks'), stem=q8c, **B)
pick('sb-q8-c-iii', '4-0', 'raising-living-standards-in-ldcs', ref('B', 8, '(c)(iii)'),
     H.q(8, 'Outline two actions which the governments of LDCs could take', ' (30 marks)'), 'An action — any two',
     H.split('1. Promote population control.', '2 points x 6 marks each.',
             ['Promote population control.', 'Improve basic infrastructure.', 'Promote land / agricultural reform.', 'Improve education.',
              'Provide better services.', 'State bureaucracy / corruption / spending on arms.']),
     2, 6, 'Two actions, 6 marks each (3 + 3).', stem=q8c, **B)

# A short ask the paper prints for several parts ("Explain the underlined term.") would
# read the same on every card, and the deck refuses two cards asking one question: each
# carries its stem in its question instead, as 2012 OL and 2013 OL do.
_asked = [' '.join(c['questionText'].split()).lower() for c in cards]
for c in cards:
    if _asked.count(' '.join(c['questionText'].split()).lower()) > 1 and c.get('stem'):
        c['questionText'], c['stem'] = f"{c['stem']} {c['questionText']}", ''

if __name__ == '__main__':
    emit(cards)
