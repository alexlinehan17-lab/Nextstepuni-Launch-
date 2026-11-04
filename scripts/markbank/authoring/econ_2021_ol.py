#!/usr/bin/env python3
"""Economics 2021 Ordinary Level, Sections A and B.

Authored from the independent census in drafts/economics-2021-ol-ev.json, made
from a visual sweep of all 28 paper pages and 28 scheme pages. Every card ID the
earlier extractors shipped is kept (student progress follows the ID). The census
adds one task: Q14(b)(ii) prints a separate 1 @ 8 cell for each of its two
objectives, so Maintaining State Services is its own card beside the older card,
which keeps Care for the Environment. Q6(b), Q9(b) and Q12(b) now carry their
printed tariffs, and the parts that print one cell for two required headings
(Q13(b)(i), Q16(b)(i), Q16(c)(i)) are heading cards. The targeted Q3 boundary
review's whole-question 15 is kept.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). This scheme sets most menus
as headed paragraphs ("Heading: explanation"), split where each heading begins;
its bullet lists are split at the bullets. The only prose written here is
guidance: tariffs, route labels and what a figure or a calculation shows.
Scheme PDF page = printed page + 1.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, bullets, defurnish, emit, heads, point  # noqa: E402

O = Sheet(2021, 'ordinary', 'LC034GLP000EV')
D = Deck(2021, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2021-OL-scheme-'
PAP = 'economics-2021-OL-paper-'
EITHER = 'Answer either (a) or (b).'
# A separator the scheme prints between alternatives, or the number of the next
# list item, left at the end of an option when the list is split.
TAIL = re.compile(r'(?:\s+(?:OR|or|\d\.)|\s*•)\s*$')


def clean(options):
    return [TAIL.sub('', o).strip() for o in options]


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return clean(bullets(O.chunk(start, end, occ)))


def at(start, end, firsts, occ=None):
    """Responses printed as headed paragraphs, split where each one begins."""
    return clean([as_option(o) for o in heads(O.chunk(start, end, occ), firsts)])


def cell(start):
    """The first line of the scheme file that opens with `start`, its marks cell
    removed (the recovered table cells keep a cell on one line where the primary
    extraction splits it around a tick)."""
    hits = [ln.strip() for ln in O.full_md.splitlines() if ln.strip().startswith(start)]
    if not hits:
        raise ValueError(f'no scheme line opens with {start!r}')
    return defurnish(hits[0])


def slashed(text, lead=''):
    """A list the scheme prints as one slash-separated run, split on its slashes."""
    return [x.strip().rstrip('.') for x in re.split(r'\s*/\s*', text.removeprefix(lead)) if x.strip()]


def lifted(text):
    """A string the provenance gate reads from the scheme file, checked here."""
    if text not in O.full_md:
        raise ValueError(f'not in the scheme file: {text!r}')
    return text


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ government expenditure by department
q1_stem = O.ask(3, 'The diagram below shows the estimated total government expenditure', ' Estimated Total')
q1_fig = PAP + 'p03-i0'
add('sa-q1-i', '3-1', 'education-as-a-percentage-of-government-spending', ref(1, '(i)', sa=True),
    O.ask(3, 'The estimated government expenditure for all departments', ' Workings:'), '3 @ 4', 12,
    [point('r-1', O.run('8.9/ 89.6 x 100 = 9.93%', '(ii) Give two examples'), 12,
           'Three steps at 4 marks: Education’s €8.9bn, read off its bar, over the €89.6bn total, times '
           '100, gives 9.93%.')],
    stem=q1_stem, figure=q1_fig, **A)
add('sa-q1-ii', '3-1', 'social-protection-spending-examples', ref(1, '(ii)', sa=True),
    O.ask(3, 'Give two examples of government expenditure on Social Protection.', ' Example 1:'), '1 @ 2, 1 @ 1', 3,
    [anyN('r-1', 'An example of Social Protection spending — any two', None, 2, 2,
          slashed(O.run('Unemployment Benefit / Income Supports', '2 Study the statements')),
          'Two examples: the first correct one 2 marks and the second 1. The scheme prints these as one '
          'slash-separated list.', steps=[2, 1])],
    stem=q1_stem, figure=q1_fig, **A)

# Q2 ─ positive and normative statements
add('sa-q2', '0-0', 'positive-or-normative-statement', ref(2, sa=True),
    O.ask(4, 'Study the statements below and indicate', ' Statement Positive'), '1 @ 9, 1 @ 6', 15,
    [point('r-exports', 'Positive — ' + cell('In 2022 exports in Ireland will grow'), None,
           'POSITIVE: a forecast the figures can check once 2022 has happened.'),
     point('r-drugs', 'Normative — ' + cell('Increased government expenditure on drug abuse will reduce'), None,
           'NORMATIVE: a judgement about what a policy will achieve. The scheme prices the two ticks '
           'together, the first correct 9 and the second 6; the completed table is shown in the figure.')],
    kind='questionTotal', figure=SOL + 'p04-q2-ticks', **A)

# Q3 ─ price elasticity of demand for kerosene (targeted boundary review: one card)
add('sa-q3-i', '1-4', 'price-elasticity-of-demand-for-kerosene', ref(3, '(i)–(ii)', sa=True),
    O.ask(4, 'Using the formula supplied, calculate the consumers', ' ∆Q') + ' '
    + O.ask(4, 'Indicate if the demand for Kerosene is price elastic', ' Answer: Leaving'), '6 @ 2, 1 @ 2, 1 @ 1', 15,
    [point('r-calculation', 'Answer: - 4.71', None,
           'PED = (ΔQ ÷ ΔP) × ((P1 + P2) ÷ (Q1 + Q2)) = (−250 ÷ +50) × (1,650 ÷ 1,750) = −4.71. The '
           'working is worth 6 @ 2 and the answer 1 @ 2; the official working is shown in the figure.'),
     point('r-interpretation', O.run('It is elastic (the PED is greater', '4 Complete the blank spaces'), None,
           'Elastic: −4.71 is greater than 1 in absolute terms. The scheme prints its last 1 @ 1 before (ii) '
           'and totals the question at 15, so the calculation and the answer are one card.')],
    kind='questionTotal', figure=SOL + 'p05-q3i-working', **A)

# Q4 ─ marginal utility
add('sa-q4', '1-1', 'completing-a-marginal-utility-table-and-finding-the-turn', ref(4, sa=True),
    O.ask(5, 'Complete the blank spaces below and answer', ' Bags of') + ' '
    + O.ask(5, 'Based on the table above:', ' Workings:'), '6 @ 2, 1 @ 3', 15,
    [point('r-1', O.run('38 – 25 = 13', 'Based on the table above'), 12,
           'The two marginal utilities, 13 and 9, with workings, 6 @ 2: each is one total utility less the '
           'one before it.'),
     point('r-2', O.run('After 2nd is consumed or before 3rd', '5 Sony released'), 3,
           'The point, 1 @ 3: marginal utility first falls after the second bag (15 down to 13), while total '
           'utility is still rising. The completed table is shown in the figure.')],
    figure=SOL + 'p05-q4-working', **A)

# Q5 ─ substitute goods
add('sa-q5', '1-1', 'substitute-goods', ref(5, sa=True),
    O.ask(5, 'Sony released The Playstation 5', ' Substitute good:'), '9 + 6', 15,
    [point('r-name', O.run('Name: Microsoft Xbox, Nintendo Switch', 'Goods that satisfy'), 9,
           'Name a substitute, 9 marks.'),
     heading('r-explanation', 'What a substitute good is — any wording',
             at('Goods that satisfy the same needs', '4 | P a g e',
                ['Goods that satisfy', 'Goods that can be consumed', 'Goods that can be used']), 6,
             'Explain, 6 marks; the scheme prints three wordings.')],
    **A)

# Q6 ─ the circular flow; invisible exports
add('sa-q6-a', '3-0', 'reading-the-circular-flow', ref(6, '(a)', sa=True),
    O.ask(6, 'The diagram below represents the Circular Flow', ' 1 Households'), '1 @ 9, 2 @ 3', 15,
    [point('r-1', cell('1. Incomes for supplying the factors'), None, 'Flow 1, from firms to households.'),
     point('r-2', cell('2. Savings'), None, 'Flow 2, from households to financial institutions.'),
     point('r-3', cell('3. Exports'), None,
           'Flow 3, from foreign markets to firms. The scheme prices the three as 1 @ 9 and 2 @ 3, the '
           'first correct answer 9 and the other two 3 each.')],
    kind='questionTotal', figure=PAP + 'p06-art', notes=EITHER, **A)
add('sa-q6-b', '4-2', 'what-an-invisible-export-is', ref(6, '(b)', sa=True),
    O.ask(6, 'Explain what is meant by the term invisible export.', ' Explanation:'), '9 + 6', 15,
    [point('r-explanation', O.run('Explanation: services sold to other countries.', 'Example: Foreign'), 9,
           'The explanation, 9 marks.'),
     point('r-example', O.run('Example: Foreign students', '7 Using the following'), 6,
           'An example, 6 marks; the scheme gives these two.')],
    notes=EITHER, **A)

# Q7 ─ the budgetary position
add('sa-q7', '3-1', 'working-out-a-budget-surplus-or-deficit', ref(7, sa=True),
    O.ask(7, 'Using the following figures, calculate', ' Workings:'), '5 @ 3', 15,
    [point('r-1', O.run('Total Income (€87.5 bn)', '5 | P a g e'), 15,
           'Income less expenditure, €1.4bn, and the verdict SURPLUS: 5 @ 3.')],
    **A)

# Q8 ─ a fall in demand
add('sa-q8', '1-1', 'demand-shift-tourism-fall', ref(8, sa=True),
    O.ask(7, 'Illustrate the impact the above statement', ' Price D'), '9 + 6', 15,
    [point('r-shift', lifted('Demand shift to left'), 9,
           'The drawing, 9 marks: demand shifts left from D1 to D2, so the quantity at price P falls from Q1 '
           'to Q2. The completed diagram is shown in the figure.'),
     point('r-explain', O.run('With reduced tourists visiting Ireland', '9 Answer either'), 6,
           'The explanation, 6 marks (3 + 3).')],
    stem=O.ask(7, 'It is predicted that tourism in Ireland', ' Adapted from'), figure=SOL + 'p07-q8-diagram', **A)

# Q9 ─ sustainability
add('sa-q9-a', '0-2', 'three-pillars-of-sustainability', ref(9, '(a)', sa=True),
    O.ask(8, 'Name the 3 pillars of sustainability.', ' Sustainability'), '1 @ 9, 2 @ 3', 15,
    [point('r-1', cell('1. Social'), None, 'The social pillar.'),
     point('r-2', cell('2. Economic'), None, 'The economic pillar.'),
     point('r-3', cell('3. Environmental'), None,
           'The environmental pillar. The scheme prices the three as 1 @ 9 and 2 @ 3, the first correct '
           'answer 9 and the other two 3 each.')],
    kind='questionTotal', notes=EITHER, **A)
add('sa-q9-b', '0-2', 'sustainable-choices-an-individual-can-make', ref(9, '(b)', sa=True),
    O.ask(8, 'Explain, using two relevant examples', ' 1. 2.'), '1 @ 9, 1 @ 6', 15,
    [anyN('r-1', 'A more sustainable choice, with an example — any two', None, 2, 9,
          [O.run('Recycle more.', '2. Cut down'), O.run('Cut down on air pollution', '3. Walk more'),
           O.run('Walk more use the car less.', '4. Watch'), O.run('Watch what kind of fuel', 'Any acceptable')],
          'Two choices: the first correct one 9 marks and the second 6. The scheme adds: '
          + O.run('Any acceptable response illustrated', '6 | P a g e'), steps=[9, 6])],
    notes=EITHER, **A)

# Q10 ─ public and private sector pay
q10_stem = O.ask(9, 'CSO data shows that public sector workers', ' Adapted from')
add('sa-q10-a', '2-1', 'public-and-private-sector-workers', ref(10, '(a)', sa=True),
    O.ask(9, 'Explain the terms in bold outlined above.', ' Public Sector'), '1 @ 9, 1 @ 6', 15,
    [point('r-public', O.run('Public Sector Workers:', 'Private Sector Workers:'), None, 'Public sector workers.'),
     point('r-private', O.run('Private Sector Workers:', 'OR\n(b) Explain one reason'), None,
           'Private sector workers. The scheme prices the two as 1 @ 9 and 1 @ 6, the first correct '
           'explanation 9 and the second 6.')],
    kind='questionTotal', stem=q10_stem, notes=EITHER, **A)
pick('sa-q10-b', '2-1', 'why-wages-differ-between-jobs', ref(10, '(b)', sa=True),
     O.ask(9, 'Explain one reason why different wages are paid', ' Leaving'),
     'A reason different jobs are paid differently — any one',
     at('Different skills:', '7 | P a g e',
        ['Different skills:', 'Training:', 'Educational qualifications:', 'Nature & Conditions',
         'Negotiating strength', 'Traditions attaching', 'Possession of innate talents:', 'Gender Bias:']),
     1, 15, 'One reason, 15 marks (9 + 6).', stem=q10_stem, notes=EITHER, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ the HDI; globalisation and MNCs; growth and Fair Trade
q11_stem = O.ask(10, 'The data below is extracted from the Human Development Index', ' 2019 Rank')
q11_fig = PAP + 'p10-q11-hdi-tables'
add('q11-a-i', '4-0', 'reading-the-change-in-irelands-hdi-position', ref(11, '(a)(i)'),
    O.ask(10, 'Using the data provided in the tables above calculate', ' Difference in'), '4 @ 3', 12,
    [point('r-rank', '+ 1', 3, 'The rank, 3 to 2: up one place.'),
     point('r-life', '+ 0.2 Years', 3, 'Life expectancy at birth, 82.1 to 82.3.'),
     point('r-schooling', '+ 0.2', 3, 'Mean years of schooling, 12.5 to 12.7.'),
     point('r-improved', 'Yes', 3, 'A smaller rank number is a higher place, so the position improved.')],
    stem=q11_stem, figure=q11_fig)
pick('q11-a-ii', '4-0', 'what-improved-irelands-hdi', ref(11, '(a)(ii)'),
     O.ask(10, 'Given your answers in (i) above explain', ' Leaving'),
     'A cause of the change — either one',
     at('Life expectancy has increased through', '8 | P a g e',
        ['Life expectancy has increased', 'Mean years of schooling has increased']),
     1, 8, 'One cause, 8 marks (4 + 4).', stem=q11_stem, figure=q11_fig)
q11b_ask = O.ask(11, 'Outline one advantage or one disadvantage of globalisation.', ' Advantage:')
for cid, word, concept, label, options in [
        ('q11-b-i-pos', 'advantage', 'advantages-of-globalisation', 'An advantage of globalisation — any one',
         at('Employment: MNCs provide jobs', 'Possible disadvantages:',
            ['Employment:', 'Advancements of ICT:', 'Economic growth in developing', 'Spin-off effects:',
             'Boosts competition:', 'Improvements in fair trade:', 'New experiences:',
             'Improved government relations:'])),
        ('q11-b-i-neg', 'disadvantage', 'disadvantages-of-globalisation', 'A disadvantage of globalisation — any one',
         at('Widens the gap between rich and poor', '(ii) Name two',
            ['Widens the gap', 'Environmental impact', 'Outsourcing', 'Lower cost countries']))]:
    pick(cid, '4-1', concept, ref(11, '(b)(i)', word), f'{q11b_ask} Answer for: {word.upper()}.', label,
         options, 1, 5, f'One {word}, 5 marks. The paper asks for an advantage OR a disadvantage, ticked; the '
                        'scheme lists both, so each is its own route.')
pick('q11-b-ii', '4-1', 'mncs-operating-in-ireland', ref(11, '(b)(ii)'),
     O.ask(11, 'Name two multinational companies', ' 1. 2.'),
     'A multinational company operating in Ireland — any two',
     slashed(O.run('Apple / Google / Facebook', '9 | P a g e')),
     2, 3, 'Two companies, 3 marks each. The scheme prints these as one slash-separated list.')
pick('q11-b-iii', '4-1', 'why-mncs-locate-in-ireland', ref(11, '(b)(iii)'),
     O.ask(11, 'Outline two reasons why MNCs locate in Ireland.', ' 1. 2.'),
     'A reason MNCs locate in Ireland — any two',
     at('Availability of a skilled/English', '(c) (i) Foreign Direct Investment',
        ['Availability of a skilled', 'Low rates of taxation:', 'Access to EU market', 'Availability of state',
         'Good industrial relations:', 'Stable rate of economic growth:', 'Stable economic climate:']),
     2, 7, 'Two reasons, 7 marks each (3 + 4).')
add('q11-c-i', '3-5', 'what-economic-growth-is', ref(11, '(c)(i)'),
    O.ask(12, 'Explain the term economic growth.', ' (ii)'), '10', 10,
    [point('r-1', O.run('It is the rise in GNP/output', '(ii) Explain your understanding'), 10,
           'Explain the term, 10 marks; any of the wordings separated by a slash.')],
    stem=O.ask(12, 'Foreign Direct Investment (FDI) has been a key contributor', ' Adapted from'))
add('q11-c-ii', '4-0', 'the-fair-trade-movement', ref(11, '(c)(ii)'),
    O.ask(12, 'Explain your understanding of the Fair', ' Fairtrade:'), '10 + 2 @ 5', 20,
    [point('r-expl', O.run('Fair Trade is a trading partnership', 'Examples:'), 10,
           'The explanation, 10 marks.'),
     anyN('r-ex', 'A fair-trade product — any two', 10, 2, 5,
          slashed(O.run('Examples: Bananas', '10 | P a g e'), 'Examples: '),
          'Two products, 5 marks each. The scheme prints these as one slash-separated list.')])

# Q12 ─ perfect competition
q12a_stem = O.ask(13, 'The diagram below represents the long run', ' D (i)')
add('q12-a-i', '2-0', 'labelling-perfect-competition', ref(12, '(a)(i)'),
    O.ask(13, 'Write out in full what each of the four labels represent.', ' Label'), '4 @ 5', 20,
    [point('r-mc', cell('MC Marginal Cost'), 5, 'MC, the rising curve through B.'),
     point('r-ac', cell('AC Average Cost'), 5, 'AC, the U-shaped curve whose lowest point is B.'),
     point('r-ar', cell('AR Average Revenue'), 5, 'AR, on the horizontal line D = AR = MR.'),
     point('r-mr', cell('MR Marginal Revenue'), 5,
           'MR, the same horizontal line: for a price taker demand, average revenue and marginal revenue '
           'coincide.')],
    stem=q12a_stem, figure=PAP + 'p13-i0')
add('q12-a-ii', '2-0', 'marking-price-output-and-cost-in-long-run-perfect-competition', ref(12, '(a)(ii)'),
    O.ask(13, 'Equilibrium occurs at the point B', ' Leaving'), '2 @ 4, 1 @ 2', 10,
    [point('r-1', O.run('The price the firm will charge for its output', '• The output the firm'), 4,
           'P1, 4 marks: on the price axis level with B, where the horizontal D = AR = MR line starts.'),
     point('r-2', O.run('The output the firm will produce in equilibrium', '• The average cost'), 4,
           'Q1, 4 marks: straight down from B on the quantity axis.'),
     point('r-3', O.run('The average cost of producing this output', '11 | P a g e'), 2,
           'C1, 2 marks: in long-run equilibrium average cost equals price, so the scheme labels the axis '
           'P1/C1. It prints 2 @ 4 and 1 @ 2 beside P1/Q1/C1; the completed diagram is shown in the figure.')],
    stem=q12a_stem, figure=SOL + 'p12-q12a-diagram')
add('q12-b', '2-0', 'assumptions-of-perfect-competition', ref(12, '(b)'),
    O.ask(14, 'Discuss three main assumptions', ' Adapted from'), '1 @ 9, 2 @ 6', 21,
    [anyN('r-1', 'An assumption of perfect competition — any three', None, 3, 9,
          at('There are many buyers in the industry', '(c) (i) Outline one benefit',
             ['There are many buyers', 'There are many sellers', 'Firm tries to maximise', 'Perfect knowledge',
              'Free entry and exit', 'All goods produced', 'No collusion', 'Elastic supply']),
          'Three assumptions: the first correct one 9 marks (6 + 3) and the next two 6 each (3 + 3).',
          steps=[9, 6, 6])],
    stem=O.ask(14, 'The image below shows a photo', ' Discuss'), figure=PAP + 'p14-i0')
q12c_ask = O.ask(15, 'Outline one benefit of perfect competition', ' The consumer:')
for cid, route, word, concept, start, end in [
        ('q12-c-i-consumer', 'the consumer', 'THE CONSUMER', 'perfect-competition-benefits-consumer',
         '• Low prices:', 'The economy in general:'),
        ('q12-c-i-economy', 'the economy in general', 'THE ECONOMY IN GENERAL', 'perfect-competition-benefits-economy',
         '• No advertising:', '(ii) Firms in perfect competition')]:
    pick(cid, '2-0', concept, ref(12, '(c)(i)', route), f'{q12c_ask} Answer for: {word}.',
         f'A benefit to {route} — any one', bl(start, end), 1, 8,
         f'One benefit, 8 marks (4 + 4). The scheme prints a separate 1 @ 8 for {route}.')
add('q12-c-ii', '2-0', 'snps-attract-new-entrants', ref(12, '(c)(ii)'),
    O.ask(15, 'Firms in perfect competition may earn', ' 75 marks'), '4 + 4', 8,
    [point('r-1', O.run('Other firms will be aware of the SNPs', '12 | P a g e'), 8,
           'What happens and why, 8 marks (4 + 4): new firms enter, because supernormal profits are known '
           'about and there are no barriers to entry.')])

# Q13 ─ minimum wage, fiscal and monetary policy; a new lender; deflation and inflation
add('q13-a-i', '2-1', 'what-the-minimum-wage-is', ref(13, '(a)(i)'),
    O.ask(16, 'Outline what is meant by the term minimum wage.', ' (ii)'), '8', 8,
    [point('r-1', O.run('The lowest wage employers must by law', '(ii) A government may use'), 8,
           'Explain the term, 8 marks.')],
    stem=O.ask(16, 'The Irish government is accused of resisting', ' Adapted from'))
add('q13-a-ii', '3-1', 'what-fiscal-policy-is', ref(13, '(a)(ii)'),
    O.ask(16, 'Explain what is meant by fiscal policy.', ' (iii)'), '8', 8,
    [point('r-1', O.run('Fiscal Policy: Any actions taken', '(iii) Monetary policy'), 8,
           'Explain the term, 8 marks.')],
    stem=O.ask(16, 'A government may use fiscal policy', ' Explain what'))
pick('q13-a-iii', '3-3', 'monetary-policy-and-price-stability', ref(13, '(a)(iii)'),
     O.ask(16, 'Explain one of the terms in bold', ' Leaving'),
     'One of the two terms — either one',
     at('Monetary Policy: actions taken by the ECB', '(b) Avantcard',
        ['Monetary Policy:', 'Price stability:']),
     1, 8, 'One term, 8 marks (4 + 4).',
     stem=O.ask(16, 'Monetary policy and delivering price stability', ' Adapted from'))
q13b_stem = O.ask(17, 'Avantcard which is owned by Spanish bank', ' Adapted from')
add('q13-b-i', '3-4', 'effect-of-a-new-mortgage-lender', ref(13, '(b)(i)'),
    O.ask(17, 'Outline the impact the introduction of a new mortgage lender', ' Consumers'), '2 @ 7', 14,
    [heading('r-consumers', 'Consumers applying for a mortgage — any one',
             at('More choice:', 'Interest rates:', ['More choice:', 'More disposable income:']), 7,
             'One impact on consumers, 7 marks (4 + 3).'),
     point('r-rates', O.run('Decreased interest rates:', '13 | P a g e'), 7,
           'The impact on interest rates, 7 marks (4 + 3). The scheme prices the pair as one 2 @ 7.')],
    stem=q13b_stem)
add('q13-b-ii', '3-4', 'why-the-central-bank-fines-firms', ref(13, '(b)(ii)'),
    O.ask(17, 'Outline one reason why the Central Bank of Ireland imposes', ' Leaving'), '7', 7,
    [point('r-1', O.run('Central Bank may fine regulated entities', '14 | P a g e'), 7,
           'One reason, 7 marks: regulation for financial stability, consumer protection and market '
           'integrity.')],
    stem=O.ask(17, 'The Central Bank of Ireland imposed a fine', ' Adapted from'))
add('q13-c-i', '3-3', 'what-deflation-is', ref(13, '(c)(i)'),
    O.ask(18, 'State the term used to describe when the price', ' Answer:'), '5', 5,
    [point('r-1', 'Deflation.', 5, 'The term, 5 marks.')])
add('q13-c-ii-cpi', '3-3', 'reading-inflation-rates-off-a-cpi-chart', ref(13, '(c)(ii)'),
    O.ask(18, 'What was the percentage change in inflation in October 2020?', ' (iii)'), '3 @ 6', 18,
    [point('r-october', '-1.5%', 6, 'October 2020: −1.5%, the lowest point on the line.'),
     point('r-aug-sep', '-0.2%', 6, 'August to September: from −1 to −1.2, a change of −0.2.'),
     point('r-increase', cell('October to November November to December'), 6,
           'Where the line rises, from −1.5 to −1.1 and then to −1, though every figure is still below '
           'zero.')],
    stem=O.ask(18, 'The diagram below shows the changing inflation rates', ' Annual'), figure=PAP + 'p18-art')
pick('q13-c-iii-types', '3-3', 'types-of-inflation-ol', ref(13, '(c)(iii)'),
     O.ask(18, 'Explain one possible cause of inflation', ' Explanation:'),
     'A cause of inflation — any one',
     at('Demand pull inflation occurs', '15 | P a g e',
        ['Demand pull inflation', 'Cost push inflation', 'Imported inflation', 'Government induced inflation']),
     1, 7, 'One cause, 7 marks.',
     stem=O.ask(18, 'The general prices of goods and services rose', ' Explain one'))

# Q14 ─ the Oweninny project; the mixed economy; taxes and intervention
q14_stem = O.ask(19, 'The ESB and Bord na Móna are pleased', ' Adapted from')
add('q14-a-i-capital', '3-1', 'current-versus-capital-expenditure', ref(14, '(a)(i)'),
    O.ask(19, 'Is the above an example of current or capital', ' Answer:'), '7 + 7', 14,
    [point('r-verdict', 'Capital expenditure.', 7, 'The answer, 7 marks.'),
     point('r-why', O.run('This is a once off/long term item', '(ii) The spending by the government'), 7,
           'The explanation, 7 marks. The scheme prints three 7s down part (a) and totals it 21; the third '
           'is (ii)’s.')],
    stem=q14_stem)
add('q14-a-ii', '0-1', 'what-opportunity-cost-is', ref(14, '(a)(ii)'),
    O.ask(19, 'The spending by the government on the Oweninny Project', ' Leaving'), '7', 7,
    [point('r-1', O.run('The cost of foregone alternatives', '(b) (i) Define the term'), 7,
           'Explain the term, applied to the windfarm, 7 marks.')],
    stem=q14_stem)
add('q14-b-i', '1-0', 'what-a-mixed-economy-is', ref(14, '(b)(i)'),
    O.ask(20, 'Define the term mixed economy.', ' (ii)'), '8', 8,
    [point('r-1', O.run('An economy that incorporates elements', '(ii) Outline one measure'), 8,
           'Define the term, 8 marks: both the government and markets allocate resources.')])
q14b2_ask = O.ask(20, 'Outline one measure the Irish government could use', ' Care for')
pick('q13-c-ii', '0-2', 'measures-for-sustainable-objectives', ref(14, '(b)(ii)', 'care for the environment'),
     f'{q14b2_ask} Care for the Environment:', 'A measure to care for the environment — any one',
     at('Public education information campaigns', 'Maintaining State Services:',
        ['Public education', 'Increase taxes:', 'Provide / subsidise', 'Grants for solar', 'Investment in more']),
     1, 8, 'One measure, 8 marks (2 @ 4). The scheme prints a separate 1 @ 8 for each objective.')
pick('q14-b-ii-services', '3-1', 'measures-to-maintain-state-services', ref(14, '(b)(ii)', 'maintaining state services'),
     f'{q14b2_ask} Maintaining State Services:', 'A measure to maintain state services — any one',
     at('Continue to invest in our services', '(c) The table below',
        ['Continue to invest', 'Ensure sufficient employment', 'Fund local authorities', 'Build a sustainable']),
     1, 8, 'One measure, 8 marks (4 + 4). The scheme prints a separate 1 @ 8 for each objective.')
q14c_stem = O.ask(21, 'The table below shows the comparison in income taxes', ' Adapted from')
add('q14-c-i', '3-1', 'comparing-income-tax-across-countries', ref(14, '(c)(i)'),
    O.ask(21, 'Using the data above name the countries', ' (ii)'), '2 @ 5', 10,
    [point('r-lowest', cell('The lowest tax Ireland'), 5, 'The lowest: Ireland, €510.'),
     point('r-highest', cell('The highest tax Germany'), 5, 'The highest: Germany, €4,770.')],
    stem=q14c_stem, figure=PAP + 'p21-i0')
add('q14-c-ii', '3-1', 'vat-is-an-indirect-tax', ref(14, '(c)(ii)'),
    O.ask(21, 'Is Value Added Tax a direct tax', ' Answer:'), '5 + 5', 10,
    [point('r-verdict', 'Indirect Tax.', 5, 'The answer, 5 marks.'),
     point('r-why', O.run('It is a tax on spending/transactions.', '17 | P a g e'), 5,
           'The explanation, 5 marks.')])
pick('q13-c-iii', '1-3', 'why-government-intervenes', ref(14, '(c)(iii)'),
     O.ask(21, 'Outline two reasons why the Irish Government may intervene', ' 1. 2.'),
     'A reason the government may intervene — any two',
     at('Provide employment:', '18 | P a g e',
        ['Provide employment:', 'Social welfare', 'Education:', 'Regulates the development', 'Non-profit companies:',
         'Encourage foreign direct', 'Achieve economic / social']),
     2, 5, 'Two reasons, 5 marks each (2 + 3).')

# Q15 ─ supply of hand sanitiser; Nike; scarcity and tariffs
q15_stem = O.ask(22, 'The first notable increase in hand sanitiser', ' Adapted from')
add('q15-a-i-supply', '1-2', 'the-law-of-supply', ref(15, '(a)(i)'),
    O.ask(22, 'State the law of supply.', ' (ii)'), '8', 8,
    [point('r-law', O.run('The Law of Supply states that as prices rise', 'Any appropriate example.', occ=0), None,
           'State the law: any of the wordings separated by a slash.'),
     point('r-example', 'Any appropriate example.', None,
           'Support it with an example. The scheme gives one 8 for the law and its example, with no published '
           'split.')],
    kind='questionTotal', stem=q15_stem)
add('q15-a-ii-sanitiser', '1-2', 'law-of-supply-applied', ref(15, '(a)(ii)'),
    O.ask(22, 'Does the law of supply apply to hand sanitiser', ' Answer:'), '7', 7,
    [point('r-answer', 'Yes.', None, 'YES.'),
     point('r-explanation', O.run('The Law of Supply states that as prices rise', '19 | P a g e', occ=1), None,
           'Explain: as the price consumers were willing to pay rose, supply rose. The scheme gives one 7 for '
           'the answer and its explanation, with no published split.')],
    kind='questionTotal', stem=q15_stem)
q15b_stem = O.ask(23, 'Nike is famous for its', ' (i)')
add('q15-b-i', '1-1', 'which-diagram-shows-a-successful-ad-campaign', ref(15, '(b)(i)'),
    O.ask(23, 'Indicate by means of a tick', ' Diagram A Diagram B'), '10', 10,
    [point('r-1', cell('Diagram B √'), 10,
           'Diagram B, 10 marks: a successful campaign raises demand at every price, so D2 lies to the right '
           'of D1.')],
    stem=q15b_stem, figure=PAP + 'p23-art')
add('q15-b-ii', '1-2', 'input-costs-shift-supply', ref(15, '(b)(ii)'),
    O.ask(23, 'The cost of cotton which is a raw material', ' Demand curve or'), '8 + 7', 15,
    [point('r-verdict', 'Supply curve.', 8, 'The answer, 8 marks.'),
     point('r-why', O.run('An increase in the price of cotton', '(iii) Many consumers'), 7,
           'The explanation, 7 marks: a higher input cost shifts supply to the left.')],
    stem=q15b_stem)
add('q15-b-iii', '1-1', 'what-consumer-loyalty-is', ref(15, '(b)(iii)'),
    O.ask(23, 'Explain what is meant by the term consumer loyalty.', ' Leaving'), '10', 10,
    [point('r-1', O.run('A consumer may become strongly attached', '(c) (i) All economic goods'), 10,
           'Explain the term, 10 marks.')],
    stem=O.ask(23, 'Many consumers are loyal to the Nike brand.', ' Explain'))
add('q15-c-i', '0-1', 'the-concept-of-scarcity', ref(15, '(c)(i)'),
    O.ask(24, 'Explain the concept of scarcity.', ' (ii)'), '7 + 3', 10,
    [point('r-1', O.run('Scarcity means that resources are limited', '(ii) Explain how scarcity'), 10,
           'Explain the concept, 10 marks (7 + 3).')],
    stem=O.ask(24, 'All economic goods are scarce', ' Explain the concept'))
pick('q15-c-ii', '0-1', 'scarcity-and-consumer-choice', ref(15, '(c)(ii)'),
     O.ask(24, 'Explain how scarcity can affect my decision', ' (iii)'),
     'How scarcity affects a consumer’s decisions — either account',
     at('The scarcer a good / service', '(iii) Since the UK',
        ['The scarcer a good', 'Because of scarcity a consumer']),
     1, 5, 'One account, 5 marks.')
add('q15-c-iii', '4-2', 'what-a-tariff-is', ref(15, '(c)(iii)'),
    O.ask(24, 'Explain what is meant by the term tariff.', ' 75 marks'), '7 + 3', 10,
    [point('r-1', 'A tax on imported goods from abroad.', 10, 'Explain the term, 10 marks (7 + 3).')],
    stem=O.ask(24, 'Since the UK left the EU', ' Explain what'))

# Q16 ─ factors of production; the sugar tax; Brexit
add('q16-a', '0-1', 'factors-of-production', ref(16, '(a)'),
    O.ask(25, 'Complete the table below explaining', ' Factors of'), '3 @ 8', 24,
    [point('r-land', O.run('Land is anything supplied by nature', 'Labour is the human effort'), 8,
           'Land, with an example, 8 marks.'),
     point('r-labour', O.run('Labour is the human effort', 'Enterprise is the factor'), 8,
           'Labour, with an example, 8 marks.'),
     point('r-enterprise', O.run('Enterprise is the factor of production that brings', '(b) The Irish government'), 8,
           'Enterprise, with an example, 8 marks. Capital is completed on the paper.')],
    figure=PAP + 'p25-i0')
q16b_stem = O.ask(25, 'The Irish government raised over €33 million', ' Adapted from')
add('q14-a-i', '2-2', 'benefits-of-the-sugar-tax', ref(16, '(b)(i)'),
    O.ask(25, 'Explain one social benefit and one economic benefit', ' Social benefit:'), '2 @ 10', 20,
    [heading('r-social', 'A social benefit — any one',
             at('Reduce consumption of sugary foods', 'Economic benefits:',
                ['Reduce consumption', 'Healthier population:', 'Incentive for entrepreneurs:']), 10,
             'One social benefit, 10 marks (6 + 4).'),
     heading('r-economic', 'An economic benefit — any one',
             at('Revenue for state:', '21 | P a g e',
                ['Revenue for state:', 'Help fund health initiatives:', 'Help reduce future health costs:']), 10,
             'One economic benefit, 10 marks (6 + 4). The scheme prices the pair as one 2 @ 10.')],
    stem=q16b_stem)
pick('q16-b-ii', '2-2', 'what-market-failure-is', ref(16, '(b)(ii)'),
     O.ask(26, 'Explain, giving an example, what is meant by the term Market Failure.', ' (c)'),
     'What market failure is, with an example — any one account',
     at('Market failure happens when', '(c) On 1st January',
        ['Market failure happens', 'Complete market failure', 'Partial failure occurs']),
     1, 7, 'One account with an example, 7 marks (4 + 3).', stem=q16b_stem)
add('q15-a-i', '4-2', 'effects-of-brexit-on-consumers-and-firms', ref(16, '(c)(i)'),
    O.ask(26, 'Discuss one economic effect Brexit will have', ' Consumers in Ireland:'), '2 @ 8', 16,
    [heading('r-consumers', 'An effect on consumers in Ireland — any one',
             at('Increased prices:', 'Businesses in Ireland:',
                ['Increased prices:', 'Decreased standard of living:', 'Encourage import substitution:',
                 'Consumer rights', 'Possible shortages of goods']), 8,
             'One effect on consumers, 8 marks (4 + 4).'),
     heading('r-businesses', 'An effect on businesses in Ireland — any one',
             at('Reduced sales / profits:', '22 | P a g e',
                ['Reduced sales / profits:', 'Possible closure', 'Possible relocation to UK',
                 'Problems with supply chains']), 8,
             'One effect on businesses, 8 marks (4 + 4). The scheme prices the pair as one 2 @ 8.')],
    stem=O.ask(26, 'On 1 January 2020, the UK officially left the EU.', ' (i)'))
pick('q15-a-ii', '4-2', 'benefits-of-exports-to-ireland', ref(16, '(c)(ii)'),
     O.ask(26, 'Outline one possible effect this growth in Irish exports', ' 75 marks'),
     'An effect of the growth in exports — any one',
     at('Employment creation:', '23 | P a g e',
        ['Employment creation:', 'Increased GNP', 'Increased sales / profits:', 'Attract investment FDI:',
         'Government finances:']),
     1, 8, 'One effect, 8 marks (4 + 4).',
     stem=O.ask(26, 'Irish exports to the UK have grown by 16%', ' Adapted from'))

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('sa-q2', 'p04-q2-question'), ('sa-q3-i', 'p04-q3-question'), ('sa-q4', 'p05-q4-question'),
                 ('sa-q8', 'p07-q8-question'), ('q12-a-ii', 'p13-q12a-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)

if __name__ == '__main__':
    emit(cards)
