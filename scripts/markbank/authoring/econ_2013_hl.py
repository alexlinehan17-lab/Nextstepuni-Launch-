#!/usr/bin/env python3
"""Economics 2013 Higher Level, Sections A and B (old syllabus, first cards).

Authored from the independent census in drafts/economics-2013-hl-ev.json, made
from a visual sweep of all 8 paper pages and 40 scheme pages before any 2013
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

H = Old(2013, 'higher', 'LC034ALP000EV')
D = OldDeck(2013, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
B = dict(section='B')
SOL = 'economics-2013-HL-scheme-'
PAP = 'economics-2013-HL-paper-'
bl = H.bullets
cc = lambda text, **kw: H.cell(text, cells_only=True, **kw)   # a whole table cell
untariffed = lambda t: H.traced(re.sub(r'\s*:?\s*at \d+m\s*$', '', t))   # "… shown on diagram at 1m"


def ask_row(rid, card_ask, marks, note):
    """A row restating the card's own ask: the scheme answers it with a drawing
    and prints no words to claim (its print is the hidden solution figure)."""
    return {"id": rid, "kind": "point", "verbatim": card_ask, "marks": marks, "openList": True,
            "contextNote": note, "ask": True}


def side(label, options):
    """Options listed under one of the scheme's own headings, each named by it."""
    lab = H.traced(label)
    return [f'{lab} — {o}' for o in options]


def cut(text, firsts):
    """One cell holding several responses, cut where each begins."""
    return [H.traced(o) for o in H._cut(text, firsts, firsts[0])]


def numbered(cell, n):
    """A cell listing "1. … 2. … n. …", cut at each numeral and read without it."""
    parts = re.split(r'(?:^|\s)(?=\d\.\s)', cell)
    return [H.traced(re.sub(r'^\d\.\s+', '', p).strip()) for p in parts if p.strip()][:n]


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ scarcity
add('sa-q1', '0-1', 'the-problem-of-scarcity', ref('A', 1),
    H.q(2, 'The fundamental economic problem is one of ‘scarcity’.', ' _'), '2 @ 8', 16,
    [anyN('r-1', 'A point — any two', 16, 2, 8,
          [H.traced(x) for x in ('Scarcity means that while the supply of resources / factors of production are limited the demand '
                                 'for these is unlimited (unlimited wants/limited resources).',
                                 'Hence, society must choose on the use to which the resources are put.',
                                 'Making choices involves an opportunity cost.')],
          H.traced('Any 2 points at 8 marks each') + ': the scheme prints one answer, read here by its sentences.')],
    kind='fixed', **A)

# Q2 ─ the marginal efficiency of capital
add('sa-q2', '1-5', 'the-marginal-efficiency-of-capital', ref('A', 2),
    H.q(2, 'Define the ‘Marginal Efficiency of Capital’ (MEC).', ' Definition:'), '8 + 4 + 4', 16,
    [point('r-definition', H.traced('It is the extra profit earned as result of employing one extra unit of capital.'), 8,
           'The definition, 8 marks.'),
     anyN('r-reasons', 'A reason for a fall in MEC — any two', 8, 2, 4,
          H.split('1. An increase in interest rates.', 'Any 2 points at 4 marks',
                  ['An increase in interest rates.', 'An increase in the cost of capital goods.', 'A decrease in the price of the finished goods.',
                   'A decrease in the productivity of capital']),
          'Two reasons, 4 marks each (2 + 2).')],
    kind='fixed', **A)

# Q3 ─ elastic or inelastic
ped = (('INELASTIC', 'Consumers are strongly attached and loyal to the product.'),
       ('ELASTIC', 'Many close substitutes are available for the product.'), ('ELASTIC', 'The product is a luxury product.'),
       ('INELASTIC', 'The product accounts for only a small fraction of a consumer’s weekly expenditure.'))
add('sa-q3', '1-4', 'elastic-or-inelastic', ref('A', 3),
    f"{H.q(2, 'Read each statement below and indicate if the price elasticity of demand', ' STATEMENT')} "
    f"{H.q(2, 'Consumers are strongly attached and loyal to the product.', ' (16 marks)')}", '4 @ 4', 16,
    [anyN('r-1', 'Each statement ticked', 16, 4, 4, [f'{cc(t, whole=True)} — {cc(s, whole=True)}' for t, s in ped],
          H.traced('4 at 4 marks each') + '.')],
    kind='fixed', **A)

# Q4 ─ collusion and price wars
add('sa-q4-a', '2-0', 'collusion', ref('A', 4, '(a)'),
    H.q(2, 'Collusion may be a feature of an oligopolistic market.', ' _'), '8', 8,
    [point('r-1', H.traced('Rival sellers in the industry come together for their mutual benefit.'), 8, 'The explanation, 8 marks.')], **A)
pick('sa-q4-b', '2-0', 'price-wars-for-consumers', ref('A', 4, '(b)'),
     H.q(2, 'Collusive practices may be undermined by price wars.', ' (i)'), 'A benefit — any two',
     H.split('1. Lower prices / value for money', 'Any 2 points at 4 marks each.',
             ['Lower prices / value for money', 'Higher disposable income', 'More choice']),
     2, 4, 'Two benefits, 4 marks each.', **A)

# Q5 ─ restricting free trade
barriers = (('Tariff', 'A tax on imports.'), ('Quota', 'A limit on the quantity of goods imported.'), ('Embargo', 'A total ban on imports.'),
            ('Subsidy', 'A payment to exporters to reduce production costs.'), ('Administrative barriers', 'Rules / regulations applying to imports.'),
            ('Exchange controls', 'Limit the amount of foreign currency available to importers to buy imported goods.'))
add('sa-q5', '4-2', 'restricting-free-trade', ref('A', 5),
    H.q(2, 'Outline three mechanisms for restricting free trade.', ' (i)'), '6 + 5 + 5', 16,
    [anyN('r-1', 'A mechanism — any three', 16, 3, 6, [f'{cc(m, whole=True)} — {cc(d, whole=True)}' for m, d in barriers],
          'Three mechanisms: ' + H.traced('6 marks + 5 marks + 5 marks') + ', the first correct 6.', steps=[6, 5, 5])],
    kind='fixed', **A)

# Q6 ─ the paradox of thrift
add('sa-q6', '3-0', 'the-paradox-of-thrift', ref('A', 6),
    H.q(3, 'Explain what is meant by the economic term ‘Paradox of Thrift’.', ' _'), '17', 17,
    [point('r-1', H.traced('An increase in savings by individuals could result in a fall in national / total savings due to reduced '
                           'consumption, reduced demand, falling incomes, job losses and so total savings will fall.'), None,
           'The scheme prices its one answer ' + H.traced('7 marks + 6 marks + 4 marks') + ' and does not say which words earn which.'),
     point('r-2', H.traced('Increased savings represent a diminishing circular flow of income.'), None,
           'Claim the complete answer: 17 marks in all.')],
    kind='questionTotal', **A)

# Q7 ─ Adam Smith
smith = ['The pursuit of self -interest', 'The Division of Labour', 'Labour Theory of Value', 'State protection of property rights',
         "'Invisible hand of competition'", 'Perfect Competition', 'Laissez-faire / Limited government intervention', 'Canons of Taxation',
         'Paradox of Value', 'Advocated Free Trade']
add('sa-q7', '0-0', 'adam-smiths-contributions', ref('A', 7),
    H.q(3, 'Outline four contributions of Adam Smith to economic thought.', ' (i)'), '5 + 4 + 4 + 4', 17,
    [anyN('r-1', 'A contribution — any four', 17, 4, 5, H.split('The pursuit of self -interest', '5+4+4+4', smith),
          'Four contributions: the 1st correct 5 marks, the 2nd, 3rd and 4th 4 each (' + H.traced('5+4+4+4') + ').',
          steps=[5, 4, 4, 4])],
    kind='fixed', **A)

# Q8 ─ the APC
q8_table = PAP + 'p03-q8-table'
add('sa-q8', '3-0', 'the-average-propensity-to-consume', ref('A', 8),
    H.q(3, 'Define the term \'Average Propensity to Consume\' (APC)', ' WORKINGS'), '9 + 3 x 2 + 2 x 1', 17,
    [point('r-definition', H.traced('The proportion / fraction of total income which is spent on goods and services.'), 9,
           'The definition, 9 marks.'),
     anyN('r-starred', 'Each starred figure', 6, 3, 2, [H.traced(x) for x in ('€34,000*', '€5,200*', '€28,800*')],
          H.traced('Each * item at 2 mark = 6 marks.') + ' The working is shown with the answer.'),
     anyN('r-bold', 'Each bolded figure', 2, 2, 1, [H.traced(x) for x in ('0.847 or 84.7%', '€34,000')],
          H.traced('2 bolded figures at 1 mark each') + ': the answer and the income it is divided by, as the working shows.')],
    kind='fixed', figure=SOL + 'p07-q8-working', **A)
beside_ask(cards[-1], q8_table)

# Q9 ─ alcohol: its costs and a minimum price
private = numbered(cc('1. Decreased disposable income. 2. Possibility'), 5)
social = numbered(cc('1. Increased health care costs.'), 4)
adv = numbered(cc('1. Reduction in alcohol consumption.'), 6)
dis = numbered(cc('1. Increased prices for consumers'), 5)
add('sa-q9', '1-3', 'alcohol-costs-and-a-minimum-price', ref('A', 9, '(a)–(b)'),
    ' '.join([H.q(3, 'Outline one private cost and one social cost', ' (b)'), H.q(3, 'Describe one advantage and one disadvantage', ' (a) Private')]),
    '5 + 4 + 4 + 4', 17,
    [anyN('r-1', 'A private cost, a social cost, an advantage and a disadvantage', 17, 4, 5,
          side('One private cost', private) + side('One social cost', social) + side('Advantage', adv) + side('Disadvantage', dis),
          'One of each, on one ladder across (a) and (b): ' + H.traced('1st correct answer 5 marks. Next 3 correct answers at 4 marks each.'),
          steps=[5, 4, 4, 4])],
    kind='fixed', stem=H.q(3, 'A recent report to the Irish government highlighted', ' (a)'), **A)

# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q1 ─ demand; the jeans market; substitution and income effects
add('sb-q1-a-i', '1-1', 'effective-and-derived-demand', ref('B', 1, '(a)(i)'),
    H.q(4, 'Distinguish between the terms ‘effective demand’ and ‘derived demand’.', ' (ii)'), '7 + 4', 11,
    [anyN('r-1', 'Each term explained', 11, 2, 7,
          [f"{cc('Effective demand', whole=True)} — {cc('Effective demand is demand supported by the necessary purchasing power.', whole=True)}",
           f"{cc('Derived demand', whole=True)} — {cc('Where a factor or production is demanded', whole=False)}"],
          'Both terms: the 1st correct response 7 marks (4 + 3), the 2nd 4 (2 + 2).', steps=[7, 4])],
    kind='fixed', **B)
pick('sb-q1-a-ii', '1-1', 'exceptions-to-the-law-of-demand', ref('B', 1, '(a)(ii)'),
     H.q(4, 'Outline two possible exceptions to the Law of Demand.', ' (25)'), 'An exception — any two',
     H.split('1. Giffen Goods', '2 at 7 marks (4+3) each',
             ['Giffen Goods', 'Status Symbols / Snob items', 'Goods the purchase of which is influenced by expectations', 'Goods of Addiction']),
     2, 7, 'Two exceptions, 7 marks each (4 + 3).', **B)
q1b = H.q(4, 'The market for a brand of blue jeans is in equilibrium.', ' (i)')
shifts = (('i', 'a-fall-in-real-income', 'Due to the economic downturn there is a reduction', ' (ii)', '• D/C shifts to the left (D2)',
           '\n(ii) A fall in the price of cotton', 'Diagram: S/C; D1; D2; Lower P, Lower Q', 'p10-q1bi-diagram'),
          ('ii', 'cheaper-cotton', 'A fall in the price of cotton, a key input', ' (iii)', '• S/C shifts to the right (S2)',
           '\n(iii) The blue jeans have recently', 'Diagram: D/C; S1; S2; Lower P, Larger Q', 'p10-q1bii-diagram'),
          ('iii', 'a-sports-star-endorsement', 'The blue jeans have recently been endorsed', ' (30)', '• D/C shifts to the right (D2)',
           '8 | P a g e', 'Diagram: S/C; D1; D2; Higher P, Higher Q', 'p10-q1biii-diagram'))
for part, concept, ask, nxt, first, end, elements, crop in shifts:
    pts = [untariffed(x) for x in bl(first, end)]
    els = [H.traced(x.strip()) for x in re.split(r'[;,]', H.traced(elements).split(': ', 1)[1])]
    add(f'sb-q1-b-{part}', '1-0', concept, ref('B', 1, f'(b)({part})'), H.q(4, ask, nxt), 'Diagram 5 + explanation 5', 10,
        [anyN('r-diagram', 'The diagram — each element', 5, 5, 1, els,
              'The diagram, 5 marks: ' + H.traced('all at 1 mark each = 5 marks') + '. The completed diagram is shown with the answer.'),
         point('r-shift', pts[0], 1, 'The shift shown on the diagram, 1 mark.'),
         point('r-reason', pts[1], 2, 'The reason, 2 marks.'),
         point('r-price', pts[2], 1, 'The new price, 1 mark.'),
         point('r-quantity', pts[3], 1, 'The new quantity, 1 mark.')],
        kind='fixed', stem=q1b, figure=SOL + crop, **B)
q1c = H.q(4, 'A fall in the price of a consumer product has both a substitution effect', ' (i)')
add('sb-q1-c-i', '1-1', 'substitution-and-income-effects', ref('B', 1, '(c)(i)'),
    f"{q1c} {H.q(4, 'Explain the underlined terms.', ' (ii)')}", '5 + 5', 10,
    [point('r-substitution', f"{cc('Substitution effect', whole=True)} — {cc('When the price of a good rises customers may shift', whole=False)}", 5,
           'The substitution effect, 5 marks.'),
     point('r-income', f"{cc('Income effect', whole=True)} — {cc('When the price of a good falls it means that', whole=False)}", 5,
           'The income effect, 5 marks.')], **B)
add('sb-q1-c-ii', '1-1', 'when-an-inferior-good-gets-cheaper', ref('B', 1, '(c)(ii)'),
    H.q(4, 'If the price of an inferior product falls', ' (20)'), '3 + 3 + 4', 10,
    [point('r-substitution', f"{cc('Substitution effect', whole=True)} — {cc('Demand will rise', whole=True)} — "
           f"{cc('The consumer is getting more marginal utility', whole=False)}", 3, 'The substitution effect, 3 marks.'),
     point('r-income', f"{cc('Income effect', whole=True)} — {cc('Demand will fall', whole=True)} — "
           f"{cc('Because the good is an inferior good', whole=False)}", 3, 'The income effect, 3 marks.'),
     heading('r-net', 'The net effect — either', [H.opt('If positive substitution effect is greater', '\nor'),
                                                 H.opt('If negative income effect is greater', '\n4 marks')], 4,
             'Whether more or less is bought, 4 marks: the scheme accepts either, by which effect is greater.')],
    kind='fixed', stem=q1c, **B)

# Q2 ─ barriers and monopoly; the monopolist's equilibrium; advertising
q2a = H.q(4, 'Technology companies such as Apple and Samsung', ' (i)')
pick('sb-q2-a-i', '2-0', 'barriers-other-than-patents', ref('B', 2, '(a)(i)'),
     H.q(4, 'Explain three barriers to entry, other than patents', ' (ii)'), 'A barrier — any three',
     H.split('Government Regulation / Legal restrictions', '3 at 5 marks (2+3) each',
             ['Government Regulation / Legal restrictions', 'Trade Agreements & Collusion.', 'Ownership of raw materials',
              'Industry requires a large investment in capital', 'Mergers / Takeovers', 'Monopolies based on fear, force or threats',
              'Limit pricing', 'Proliferation of brands on the market']),
     3, 5, 'Three barriers, 5 marks each (2 + 3).', stem=q2a, **B)
pick('sb-q2-a-ii', '2-0', 'monopoly-against-the-public-interest', ref('B', 2, '(a)(ii)'),
     H.q(4, 'Outline two reasons why monopolies may not be in the public interest.', ' (25)'), 'A reason — any two',
     H.split('Higher Prices\nMonopolies', '2 at 5 marks (2+3) each',
             ['Higher Prices', 'Lower output produced', 'Inefficiency/Wasteful of resources', 'Super Normal Profits', 'Poorer Quality Service',
              'Lack of innovation', 'May engage in price discrimination', 'Loss making state monopolies']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q2a, **B)
q2b = H.q(4, 'Explain, with the aid of a diagram, the long run equilibrium position of a monopoly firm.', ' (25)')
# The scheme's numbered table of the ten points: its long labels are cells, its short ones the labels themselves.
labels = ([cc('Price axis', whole=True), cc('Quantity axis', whole=True)] + [H.traced(x) for x in ('AR', 'MR', 'MC', 'AC')]
          + [cc('Equilibrium point- E', whole=True)] + [H.traced(x) for x in ('P1', 'C1', 'Q1')])
add('sb-q2-b', '2-0', 'long-run-equilibrium-of-a-monopoly', ref('B', 2, '(b)'), q2b, '10 + 4 + 4 + 2 + 3 + 2', 25,
    [anyN('r-diagram', 'The diagram — each point', 10, 10, 1, labels,
          'The diagram, ' + H.traced('10 points at 1 mark each.') + ' The completed diagram is shown with the answer.'),
     anyN('r-equilibrium', H.traced('1. Equilibrium/Profit maximising point').split('. ', 1)[1] + ' — any two', 4, 2, 2,
          [H.traced(x) for x in ('Occurs at point E.', 'Where MC = MR.', 'And MC is rising.')], H.traced('Any 2 points at 2 marks each.')),
     anyN('r-price', 'Price / Output — both', 4, 2, 2, [H.traced('The firm produces Q1'), H.traced('and sells it at P1')],
          'Output and price, 2 marks each.'),
     point('r-cost', H.traced('The cost of producing this output / normal profit is shown at point C1'), 2, 'Cost or normal profit, 2 marks.'),
     anyN('r-snp', 'SNP’s — both', 3, 2, 2, [H.traced('The firm is earning SNPs'),
                                            H.traced('Because AR > AC or they can continue to exist due to barriers to entry.')],
          'Supernormal profits 2 marks, and why 1.', steps=[2, 1]),
     anyN('r-waste', 'Waste of Scarce Resources / Inefficiency — both', 2, 2, 1,
          [H.traced('Waste of Scarce Resources / Inefficiency'), H.traced('The firm is not producing at the lowest point of AC')],
          'The waste of resources, 1 mark, and why, 1.')],
    kind='fixed', figure=SOL + 'p14-q2b-diagram', **B)
q2c = H.q(4, 'The global market for toothpaste products', ' (i)')
add('sb-q2-c-i', '2-0', 'competitive-advertising', ref('B', 2, '(c)(i)'), H.q(4, 'Explain the term ‘competitive advertising’.', ' (ii)'), '7', 7,
    [point('r-1', H.traced('This is advertising which stresses the advantages of one firm’s products/services over its rivals.'), 7,
           'The explanation, 7 marks.')], stem=q2c, **B)
add('sb-q2-c-ii', '2-0', 'advertising-as-a-barrier', ref('B', 2, '(c)(ii)'),
    H.q(4, 'Outline, using an example, how advertising can be used to prevent small firms', ' (iii)'), '3 + 3', 6,
    [heading('r-explanation', 'An explanation — either', [H.opt('If a small firm has to advertise in order to compete', '\nor'),
                                                          H.opt('Existing firms may continue to spend money on advertising', '\nAny correct Example')], 3,
             'The explanation, 3 marks: ' + H.traced('Prohibitive costs of advertising') + '.'),
     point('r-example', H.opt('Two firms spend €6,000 on an advertising campaign.', '\n(iii)'), 3,
           'An example, 3 marks: the scheme’s is one of any correct example.')],
    kind='fixed', stem=q2c, **B)
pick('sb-q2-c-iii', '2-0', 'advertising-and-the-consumer', ref('B', 2, '(c)(iii)'),
     H.q(4, 'State and explain two possible disadvantages of advertising for the consumer.', ' (25)'), 'A disadvantage — any two',
     H.split('1. Increased prices\nThe firm', '2 at 6 marks (3+3) each',
             ['Increased prices', 'False / Misleading information', 'Impulse buying / creates unsustainable wants', 'Harmful commodities',
              'Unnecessary pollution']),
     2, 6, 'Two disadvantages, 6 marks each (3 + 3).', stem=q2c, **B)

# Q3 ─ the demand for labour; wage determination; the gender pay gap; Marx
add('sb-q3-a', '2-1', 'demand-for-labour', ref('B', 3, '(a)'),
    H.q(5, 'State and explain four economic influences on an individual firm’s demand for labour.', ' (25)'), '7 + 7 + 7 + 4', 25,
    [anyN('r-1', 'An influence — any four', 25, 4, 7,
          H.split('1. Marginal revenue productivity of labour', 'First 3 points at 7 marks',
                  ['Marginal revenue productivity of labour', '(Minimum) Wage rate', 'Demand for output', 'Price of other factors of production',
                   'State subsidies', 'Taxation Rates on the firm’s profits', 'Payroll taxes / Employers rate of PRSI', 'Availability of technology',
                   'Trade union involvement']),
          'Four influences: ' + H.traced('First 3 points at 7 marks (4+3) each') + '; ' + H.traced('4th point at 4 marks (2+2)') + '.',
          steps=[7, 7, 7, 4])],
    kind='fixed', **B)
q3b = H.q(5, 'Explain, with the aid of a labour market diagram in each case', ' (25)')
add('sb-q3-b', '2-1', 'how-wages-are-set', ref('B', 3, '(b)'), q3b, '5 + 7 + 5 + 8', 25,
    [ask_row('r-free-diagram', 'A free labour market', 5, 'The free market’s diagram, 5 marks: S/C and D/C of labour crossing at WE, as the '
             'figure shows.'),
     point('r-free', H.traced('A free market is one where there are no restrictions on the demand and supply of labour. Where the demand '
                              'for labour equals the supply of labour the equilibrium wage rate is set.'), 7,
           'The free market’s explanation, ' + H.traced('7 marks (4+3)') + '.'),
     ask_row('r-union-diagram', 'A labour market where a trade union has negotiated a minimum wage', 5,
             'The union market’s diagram, 5 marks: the supply of labour horizontal at WMIN before it rises, as the figure shows.'),
     point('r-union', H.traced('The trade union may negotiate a minimum wage rate: this is set at WMIN. • No workers will be supplied below WMIN.'), 8,
           'The union market’s explanation, ' + H.traced('8 marks (4+4)') + '.')],
    kind='fixed', figure=SOL + 'p17-q3b-diagrams', **B)
q3c = H.q(5, 'Women in Ireland earn on average 17.1% less per hour than men', ' (i)')
pick('sb-q3-c-i', '2-1', 'why-women-earn-less', ref('B', 3, '(c)(i)'),
     H.q(5, 'Outline two possible reasons for the lower wage rates earned by women', ' (ii)'), 'A reason — any two',
     H.split('1. Discrimination in the workplace', '2 points at 5 marks (2+3) each',
             ['Discrimination in the workplace', 'Lack of enforcement by State agencies', 'Balancing work and family responsibilities',
              '‘Glass ceiling’/fewer women', 'Different jobs, different sectors', 'Undervaluing of women’s work and skills',
              'Gender role of women / Tradition']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q3c, **B)
pick('sb-q3-c-ii', '2-1', 'closing-the-gender-pay-gap', ref('B', 3, '(c)(ii)'),
     H.q(5, 'Outline one measure that could be taken to close the gender pay gap.', ' (15)'), 'A measure — any one',
     H.split('1. Awareness - raising Campaign', '1 point at 5 marks',
             ['Awareness - raising Campaign', 'Collective Agreements', 'Labour Inspections / Name and shame the offenders', 'Audits by companies',
              'Make pay systems transparent', 'Gender Equality Studies', 'Implement / enforce existing laws', 'Education on gender stereotyping']),
     1, 5, 'One measure, 5 marks (2 + 3).', stem=q3c, **B)
add('sb-q3-d', '0-0', 'marx-on-exploitation', ref('B', 3, '(d)'),
    H.q(5, 'Explain briefly Karl Marx’s economic theory about the exploitation of labour', ' (10)'), '10', 10,
    [point('r-1', H.traced(' • '.join(bl('• Marx argued that workers were paid subsistence', '10 marks (6+4)'))), 10,
           'The theory, ' + H.traced('10 marks (6+4)') + '.')], **B)

# Q4 ─ the deficit; budget and inequality; excise and motor tax; capital spending
q4a = H.q(5, '‘The Exchequer deficit in December 2012 was €14.89bn’.', ' (i)')
pick('sb-q4-a-i', '3-1', 'consequences-of-the-deficit', ref('B', 4, '(a)(i)'),
     H.q(5, 'Discuss four possible economic consequences of the Government Current Budget Deficit', ' (ii)'), 'A consequence — any four',
     H.split('1. Additional taxation', '4 points at 5 marks (2+3) each',
             ['Additional taxation', 'Cuts in public expenditure', 'Reduction in the provision of state services', 'Troika intervention',
              'Public sector pay', 'Reduction in aggregate demand / job losses', 'Loss of confidence / emigration', 'Moderation in citizens expectations']),
     4, 5, 'Four consequences, 5 marks each (2 + 3).', stem=q4a, **B)
pick('sb-q4-a-ii', '3-1', 'the-budget-and-inequality', ref('B', 4, '(a)(ii)'),
     H.q(5, 'Explain how a government budget could be used to reduce income inequalities', ' (30)'), 'A measure — any two',
     H.split('Welfare benefits could be increased / maintained', '2 points at 5 marks (2+3) each',
             ['Welfare benefits could be increased / maintained', 'Tax changes', 'Wealth tax', 'Target universal entitlements',
              'Increase the minimum wage rate']),
     2, 5, 'Two points, 5 marks each (2 + 3).', stem=q4a, **B)
pick('sb-q4-b-i', '3-1', 'why-tax-cigarettes-and-alcohol', ref('B', 4, '(b)(i)'),
     H.q(5, 'State and explain two reasons why the government increased taxes on cigarettes', ' (ii)'), 'A reason — any two',
     H.split('1. To discourage smoking / alcohol consumption', '2 points at 6 marks (3+3) each',
             ['To discourage smoking / alcohol consumption', 'To reduce health care costs', 'To reduce absenteeism from work',
              'To increase revenue from these taxes', 'To specifically target the consumption', 'To discourage/ limit tax evasion']),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', **B)
pick('sb-q4-b-ii', '3-1', 'a-higher-motor-tax', ref('B', 4, '(b)(ii)'),
     H.q(5, 'Outline three economic impacts for the Irish economy of an increase in Motor Tax.', ' (30)'), 'An impact — any three',
     H.split('1. Increased tax revenue for the local authority', '3 points at 6 marks (3+3) each',
             ['Increased tax revenue for the local authority', 'Reduced disposable income for consumers',
              'No incentive for purchasing environmentally friendly cars', 'Increased costs for businesses', 'Possible closure of car dealerships',
              'Better for environment']),
     3, 6, 'Three impacts, 6 marks each (3 + 3).', **B)
add('sb-q4-c', '3-1', 'cutting-capital-expenditure', ref('B', 4, '(c)'),
    H.q(5, 'As an Advisor to the Minister for Public Expenditure and Reform', ' (15)'), '10 + 5', 15,
    [anyN('r-1', 'An argument — any two', 15, 2, 10,
          H.split('1. Reduce state borrowing and reduce the national debt', '2 points\n1st point',
                  ['Reduce state borrowing and reduce the national debt', 'New Infrastructure already in place / fewer bottlenecks',
                   'Private sector is providing necessary infrastructure', 'Spending in line with other European countries']),
          'Two arguments: the ' + H.traced('1st point at 10 marks (5+5)') + ', the ' + H.traced('2nd point at 5 marks (2+3)') + '.',
          steps=[10, 5])],
    kind='fixed', stem=H.q(5, '‘The Public Capital Programme must make a further contribution', ' As an Advisor'), **B)

# Q5 ─ national income terms; the circular flow; the multiplier
inkind = bl('• Income / rewards received in a non-monetary form.', 'Net Factor Income from the Rest of the World:')
add('sb-q5-a', '3-0', 'national-income-terms', ref('B', 5, '(a)'),
    H.q(6, 'Explain the following terms which are commonly used in estimating the National Income', ' (15)'), '3 x 5', 15,
    [point('r-subsidies', 'Subsidies — ' + H.traced('Payments to a producer to help reduce the cost of production (price of the good)/ increase output.'), 5,
           'Subsidies, 5 marks.'),
     point('r-in-kind', 'Incomes-in-kind — ' + inkind[0], 5, 'Incomes-in-kind, 5 marks. The scheme also accepts its second statement.',
           accepts=inkind[1:]),
     point('r-nfia', 'Net Factor Income from the Rest of the World — '
           + H.opt('This is the difference between incomes earned by foreign factors', '\n(b)'), 5,
           'Net factor income from the rest of the world, 5 marks.')], **B)
add('sb-q5-b-i', '3-0', 'the-circular-flow-of-an-open-economy', ref('B', 5, '(b)(i)'),
    H.q(6, 'Illustrate by means of a diagram the Circular Flow of Income for an open economy.', ' (ii)'), '5 x 2 + 8 x 1', 18,
    [anyN('r-sectors', 'Each sector', 10, 5, 2, [H.traced(x) for x in ('HOUSEHOLDS', 'FIRMS', 'GOVERNMENT', 'FINANCIAL INSTITUTIONS', 'FOREIGN MARKETS')],
          H.traced('Identifying the 5 ‘sectors’') + ', 2 marks each.'),
     anyN('r-flows', 'Each flow, with its direction', 8, 8, 1,
          [H.traced(x) for x in ("Incomes for supplying F.O.P's", 'Spending on the output of firms', 'Tax', 'Expenditure', 'Savings', 'Investment',
                                 'Imports', 'Exports')],
          H.traced('Identifying the correct 8 ‘flows’ (component & direction)') + ', 1 mark each: the eighth flow is Government '
          'Expenditure. The completed diagram is shown with the answer.')],
    kind='fixed', figure=SOL + 'p23-q5bi-diagram', **B)
add('sb-q5-b-ii', '3-0', 'transfer-payments-as-an-injection', ref('B', 5, '(b)(ii)'),
    H.q(6, 'Are transfer payments an injection into, or a leakage', ' (iii)'), '2 + 3', 5,
    [point('r-answer', H.traced('They are an injection into to the circular flow of income.'), 2, 'The answer, 2 marks.'),
     point('r-explanation', H.traced('They become incomes for the recipients which they spend, and this increases aggregate demand.'), 3,
           'The explanation, 3 marks.')], **B)
pick('sb-q5-b-iii', '3-0', 'what-drives-consumption', ref('B', 5, '(b)(iii)'),
     H.q(6, 'Outline three current determinants of the level of consumption', ' (35)'), 'A determinant — any three',
     H.split('1. Levels of incomes (irrespective of source)', '3 points at 4 marks (2+2) each',
             ['Levels of incomes (irrespective of source)', 'Interest rates', 'Access to / availability of credit', 'Rates of taxation',
              'Consumer confidence', 'MPC']),
     3, 4, 'Three determinants, 4 marks each (2 + 2).', **B)
add('sb-q5-c-i', '3-0', 'the-keynesian-multiplier', ref('B', 5, '(c)(i)'),
    H.q(6, 'Using the Keynesian multiplier process outline how a fiscal stimulus', ' (ii)'), '4 + 9', 13,
    [point('r-greater', H.traced('The initial increase in government expenditure will have a greater final increase in aggregate demand.'), 4,
           'The greater final increase, 4 marks.'),
     point('r-multiplier', H.traced('Increase in aggregate demand = initial increase in government expenditure x by the multiplier.'), 9,
           'The multiplier at work, 9 marks. The scheme also accepts its worked example.',
           accepts=[H.traced('Government injects €10m. Multiplier is 2. So increase in Aggregate Demand = €10m x 2 = €20m.')])], **B)
add('sb-q5-c-ii', '3-1', 'why-a-stimulus-is-hard', ref('B', 5, '(c)(ii)'),
    H.q(6, 'Explain why the Irish government might find it difficult to implement', ' (25)'), '8 + 4', 12,
    [anyN('r-1', 'A reason — any two', 12, 2, 8,
          H.split('1. Ireland is in a bailout programme', '12 marks. 2 points',
                  ['Ireland is in a bailout programme', 'Ireland is an open economy', 'Ireland needs a global recovery', 'Reaction of the public',
                   'Current economic climate / expectations of citizens']),
          'Two points: ' + H.traced('First point 8 marks (4+4)') + '; ' + H.traced('Second point 4 marks (2+2)') + '.', steps=[8, 4])],
    kind='fixed', **B)

# Q6 ─ credit creation; quantitative easing and interest rates; the CPI
q6ai = H.q(6, 'Explain, using a numerical example, how banks create credit in an economy.', ' (ii)')
steps_a = [H.opt(s, e) for s, e in (('Commercial banks accept cash deposits from their customers', ' 4 marks'),
                                    ('These banks know from experience that their customers', ' 4 marks'),
                                    ('So they now have surplus cash with which to give loans', ' 4 marks'),
                                    ('The amount of loans they give is related to', '\n⟨4 marks⟩'))]
add('sb-q6-a-i-reserve-ratio', '3-4', 'how-banks-create-credit', ref('B', 6, '(a)(i)', 'the reserve ratio'),
    f'{q6ai} Answer for: {H.traced("Alternative A")}, the reserve ratio.', '4 x 4 + 4 x 1', 20,
    [point(f'r-step-{i + 1}', s, 4, f'Step {i + 1}, 4 marks.') for i, s in enumerate(steps_a)]
    + [anyN('r-example', 'Each asterisked figure of the numerical example', 4, 4, 1, [H.traced(x) for x in ('€100*', '1 *', '€1,000*', '€ 900*')],
            'The numerical example, 4 marks: ' + H.traced('( 1 mark per asterisked figure)') + ', as the figure shows. The scheme '
            'also gives the four steps as one formula: ' + H.traced('Increase in credit = Increase in Cash Deposits x 1') + ' over '
            + H.traced('Banks Reserve Ratio') + '.')],
    kind='fixed', figure=SOL + 'p26-q6ai-example', **B)
add('sb-q6-a-i-balance-sheet', '3-4', 'how-banks-create-credit', ref('B', 6, '(a)(i)', 'the balance sheet'),
    f'{q6ai} Answer for: {H.traced("Alternative B")}, the balance sheet.', '4 + 6 + 5 x 2', 20,
    # Each sheet is claimed by the scheme's own title for it; the sheets themselves are the hidden crop,
    # so no table is flattened into a row.
    [point('r-sheet-1', H.traced('Balance Sheet of a Bank'), 4,
           'The first balance sheet, 4 marks: cash lodged by X of 100 against X’s deposit of 100, as the figure shows.'),
     point('r-sheet-2', H.traced('Balance Sheet of a Bank'), 6,
           'The second balance sheet, 6 marks: cash of 100 and a loan of 900 against deposits of 100 and new deposits of '
           '900, totals of 1,000, as the figure shows.'),
     anyN('r-explanation', 'Each step of the explanation', 10, 5, 2,
          H.split('1. Mr. X lodges €100 into the bank', 'Explanation 10 marks',
                  ['Mr. X lodges €100 into the bank', 'It knows that only 10% is demanded in cash.', 'It has enough cash to support',
                   'The bank can create another €900 in deposits.', 'So €100 cash is sufficient']),
          H.traced('Explanation 10 marks: 5 at 2 marks each') + '.')],
    kind='fixed', figure=SOL + 'p26-q6ai-balance-sheets', **B)
pick('sb-q6-a-ii', '3-4', 'limits-on-credit-in-a-recession', ref('B', 6, '(a)(ii)'),
     H.q(6, 'Outline two factors which limit the ability of banks to create credit', ' (30)'), 'A factor — any two',
     H.split('1. Creditworthy customers / increased risks for banks', '2 points at 5 marks (2+3) each',
             ['Creditworthy customers / increased risks for banks', 'Cash deposits in the banks', 'Demand for loans / credit by customers',
              'Irish banks have weak balance sheets / Deleveraging', 'Customers\' demands for cash']),
     2, 5, 'Two factors, 5 marks each (2 + 3).', **B)
q6b = H.q(6, 'Some central banks have responded to the global financial crisis', ' (i)')
pick('sb-q6-b-i', '3-3', 'effects-of-quantitative-easing', ref('B', 6, '(b)(i)'),
     H.q(6, 'Outline two possible economic effects of this measure for an economy.', ' The European'), 'An effect — any two',
     H.split('1. Increased bank lending', '2 points at 4 marks (2+2) each',
             ['Increased bank lending', 'Economic growth / jobs', 'Possible inflation', 'Interest rates', 'Government bonds']),
     2, 4, 'Two effects, 4 marks each (2 + 2).', stem=q6b, **B)
pick('sb-q6-b-ii', '3-3', 'benefits-of-lower-interest-rates', ref('B', 6, '(b)(ii)'),
     H.q(6, 'Discuss two possible economic benefits of falling interest rates for the Irish economy.', ' (20)'), 'A benefit — any two',
     H.split('1. Borrowing encouraged\nBorrowing', '2 points at 6 marks (3+3) each',
             ['Borrowing encouraged', 'Savings discouraged', 'Reduced mortgage repayments', 'Cost of Servicing the National Debt',
              'Costs of Production / increased competitiveness', 'Incentive to Invest', 'Economic Growth encouraged', 'Taxation revenues',
              'Employment']),
     2, 6, 'Two benefits, 6 marks each (3 + 3).',
     stem=f"{q6b} {H.q(6, 'The European Central Bank (ECB) reduced interest rates in 2012.', ' (ii)')}", **B)
q6c = H.q(6, 'The monetary policy of the ECB aims to maintain the annual euro area inflation rate', ' (i)')
add('sb-q6-c-i', '3-3', 'irelands-inflation-rate', ref('B', 6, '(c)(i)'),
    H.q(6, 'State the rate of inflation in Ireland during 2013', ' (ii)'), '5', 5,
    [point('r-1', H.traced('May 2013: 0.4%'), 5, 'The rate, 5 marks. The scheme also accepts its second figure.',
           accepts=[H.traced('From January 2012 to January 2013: 1.2%')])], stem=q6c, **B)
pick('sb-q6-c-ii', '3-3', 'uses-of-the-cpi', ref('B', 6, '(c)(ii)'),
     H.q(6, 'Outline two uses of the CPI, other than as a measure of the rate of inflation.', ' (iii)'), 'A use — any two',
     H.split('1. Measures International Competitiveness', '2 points at 5 marks (2+3) each',
             ['Measures International Competitiveness', 'Indicator of economic performance', 'Indexation of savings / investments',
              'Used by government indexing tax bands', 'Used in pay negotiations']),
     2, 5, 'Two uses, 5 marks each (2 + 3).', stem=q6c, **B)
pick('sb-q6-c-iii', '3-3', 'limits-of-the-cpi', ref('B', 6, '(c)(iii)'),
     H.q(6, 'Discuss the possible limitations of the CPI as an accurate measure', ' (25)'), 'A limitation — any two',
     H.split('1. Limitations of an average', '2 points at 5 marks (2+3) each',
             ['Limitations of an average', 'New products', 'Rural versus urban lifestyles', 'Switching by consumers', 'Quality of products',
              'Measures changes to prices', 'Static weights']),
     2, 5, 'Two limitations, 5 marks each (2 + 3).', stem=q6c, **B)

# Q7 ─ the balance of payments; a rising euro; exporters' challenges
q7a = H.q(7, '‘The Balance of Payments figures give the most detailed information', ' (i)')
bop = bl('• This shows the receipts and payments for visible and invisible trade', '6 marks')
add('sb-q7-a-i', '4-2', 'the-current-account', ref('B', 7, '(a)(i)'),
    H.q(7, 'Explain the term Balance of Payments Current Account.', ' (ii)'), '6', 6,
    [point('r-1', bop[0], 6, 'The explanation, 6 marks. The scheme also accepts its alternative.', accepts=bop[1:])], stem=q7a, **B)
pick('sb-q7-a-ii', '4-2', 'a-current-account-surplus', ref('B', 7, '(a)(ii)'),
     H.q(7, 'Explain two economic consequences of a surplus', ' (iii)'), 'A consequence — any two',
     H.split('1. Injection into the economy', '12 marks: 2 points at 6 marks',
             ['Injection into the economy', 'Increase in our external reserves', 'Jobs created', 'Attract FDI']),
     2, 6, 'Two consequences, 6 marks each (3 + 3).', stem=q7a, **B)
pick('sb-q7-a-iii', '4-2', 'foreign-firms-and-the-current-account', ref('B', 7, '(a)(iii)'),
     H.q(7, 'Describe how foreign firms operating in Ireland may affect', ' (30)'), 'An effect — any two',
     H.split('1. Salaries / wages returned to home country', '12 marks: 2 points at 6 marks',
             ['Salaries / wages returned to home country', 'Imported raw materials / capital goods', 'Exported finished products',
              'Repatriated profits']),
     2, 6, 'Two effects, 6 marks each (3 + 3).', stem=q7a, **B)
pick('sb-q7-b', '4-2', 'a-rising-euro', ref('B', 7, '(b)'),
     H.q(7, 'Discuss the possible economic effects for the Irish economy of the euro rising', ' (25)'), 'An effect — any five',
     H.split('1. Imports Cheaper', '5 points at 5 marks (2+3) each',
             ['Imports Cheaper', 'Exports Dearer', 'Tourism into Ireland suffers', 'Employment', 'Slowdown in rate of economic growth',
              'Foreign investment in Ireland discouraged']),
     5, 5, 'Five effects, 5 marks each (2 + 3).', **B)
pick('sb-q7-c', '4-2', 'challenges-for-exporters', ref('B', 7, '(c)'),
     H.q(7, 'Discuss the key challenges for Irish businesses on international markets.', ' (20)'), 'A challenge — any four',
     H.split('1. Finding new markets', '4 points at 5 marks (2+3) each',
             ['Finding new markets', 'Global Recession', 'Difficulty accessing credit', 'Competitiveness', 'Exchange rate',
              'Keep bureaucracy to a minimum', 'Education and skills', 'Transport costs', 'Language skills']),
     4, 5, 'Four challenges, 5 marks each (2 + 3).', stem=H.q(7, '\'Exporting businesses need to become the engine', ' Discuss the key'), **B)

# Q8 ─ youth unemployment; the national debt; an ageing population
q8a = H.q(7, '‘The rate of unemployment among 15-24 year olds', ' (i)')
youth = (('Increased government (current) expenditure', 'The government will have to fund a higher social welfare bill.'),
         ('Reduced government (current) revenue', 'With fewer people working the government will collect less'),
         ('Loss on return on investment in education ‘Lost generation’', 'With young people not contributing to society'),
         ('Emigration', 'With less job opportunities available some people'), ('Social costs to society', 'Crime, vandalism and anti-social'),
         ('Increased demand for places in third level', 'With employment prospects poor those who had not availed'),
         ('Less incentive for businesses to invest', 'As there is less demand for goods and services by people on lower incomes'))
pick('sb-q8-a-i', '3-2', 'consequences-of-youth-unemployment', ref('B', 8, '(a)(i)'),
     H.q(7, 'Explain three economic consequences of a high rate of youth unemployment', ' (ii)'), 'A consequence — any three',
     [f'{cc(s, whole=True)} — {cc(e)}' for s, e in youth], 3, 5, 'Three consequences, 5 marks each (2 + 3).', stem=q8a, **B)
pick('sb-q8-a-ii', '3-2', 'tackling-youth-unemployment', ref('B', 8, '(a)(ii)'),
     H.q(7, 'Discuss three measures which the Irish government may introduce', ' (30)'), 'A measure — any three',
     H.split('1. Provide more opportunities for education / training', '3 points at 5 marks (2+3) each',
             ['Provide more opportunities for education / training', 'Subsidised work placements/internships', 'Lower PRSI contributions',
              'Reduce the minimum wage', 'Healthy banking sector', 'More school based vocational training',
              'Policies to encourage geographical mobility', 'Reduce costs for business including payroll and other taxes',
              'Reduce rates of social welfare for ‘young’ unemployed']),
     3, 5, 'Three measures, 5 marks each (2 + 3).', stem=q8a, **B)
q8b = H.q(7, '\'Ireland’s National Debt was €137.6bn at the end of December 2012\'.', ' (i)')
pick('sb-q8-b-i', '3-1', 'costs-of-a-high-national-debt', ref('B', 8, '(b)(i)'),
     H.q(7, 'Discuss the disadvantages for Ireland of having a high National Debt.', ' (ii)'), 'A disadvantage — any three',
     H.split('1. Opportunity costs involved / loss of public services', '3 points at 6 marks (3+3) each',
             ['Opportunity costs involved / loss of public services', 'Increased burden on current and future taxpayers',
              'Annual interest repayments', 'Loss of economic sovereignty / intervention of Troika', 'Reduction in our international credit rating',
              'Sale of semi-state bodies']),
     3, 6, 'Three disadvantages, 6 marks each (3 + 3).', stem=q8b, **B)
pick('sb-q8-b-ii', '3-1', 'a-more-sustainable-debt', ref('B', 8, '(b)(ii)'),
     H.q(7, 'Outline two means by which Ireland’s National Debt may be made more sustainable.', ' (30)'), 'A means — any two',
     H.split('1. Debt write off', '2 points at 6 marks (3+3) each',
             ['Debt write off', 'Negotiate Lower interest rates', 'Negotiate a longer time repayment period', 'Ensure debt is ‘self-liquidating’',
              'Encourage Economic growth']),
     2, 6, 'Two means, 6 marks each (3 + 3).', stem=q8b, **B)
pick('sb-q8-c', '3-5', 'an-ageing-population', ref('B', 8, '(c)'),
     H.q(7, 'Discuss the possible economic consequences of an ageing population', ' (15)'), 'A consequence — any three',
     H.split('1. Pressure on provision of state pensions', '3 points at 5 marks (2+3) each',
             ['Pressure on provision of state pensions', 'Possible increased tax burden', 'Increased government expenditure',
              'Changing pattern of demand', 'The participation rate falls', 'Reduced mobility of labour']),
     3, 5, 'Three consequences, 5 marks each (2 + 3).', stem=H.q(7, 'Ireland, in common with many developed countries', ' Discuss'), **B)

if __name__ == '__main__':
    emit(cards)
