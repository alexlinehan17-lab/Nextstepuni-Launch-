#!/usr/bin/env python3
"""Economics 2022 Ordinary Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2022-ol-ev.json,
made from a visual sweep of all 32 paper pages and 36 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID).
The census differs from the earlier one in three places: Q3, Q8 and Q14(b) each
print one "1st x n, 2nd x m" tariff across two printed parts, so each is one
task with unpriced rows (as 2023 OL Q9 and 2024 OL Q1 already are), and the
second-part cards resolve by alias. The 2022 Ordinary Irish review mirrors those
route changes only.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). Ordinary Level sets its
responses as a bullet list, so menus are split at the bullets; the lists the
scheme sets as headed paragraphs are split where each heading begins. The only
prose written here is guidance: tariffs, route labels and what a figure or a
calculation shows. The Irish label notes the earlier review placed on three
English asks and on Q2(i) are kept as they were. Scheme PDF page = printed + 1.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, bullets, defurnish, emit, heads, point  # noqa: E402

O = Sheet(2022, 'ordinary', 'LC034GLP000EV')
D = Deck(2022, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2022-OL-scheme-'
PAP = 'economics-2022-OL-paper-'


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return bullets(O.chunk(start, end, occ))


def at(start, end, firsts, occ=None):
    """Responses printed as headed paragraphs, split where each one begins."""
    return [as_option(o) for o in heads(O.chunk(start, end, occ), firsts)]


def line(start):
    """One whole line of the scheme file that opens with `start` (the recovered
    table cells keep a cell on one line where the primary extraction splits it)."""
    hits = [ln.strip() for ln in O.full_md.splitlines() if ln.strip().startswith(start)]
    if not hits:
        raise ValueError(f'no scheme line opens with {start!r}')
    return defurnish(hits[0])


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, note):
    """A required answer inside a jointly priced response (1st x n, 2nd x m)."""
    return point(rid, paras(options), None, f'{label}. {note}')


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1st x 9, 2nd x 6)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ forecast growth
q1_stem = O.ask(3, 'The diagram below shows the forecast growth in the Irish economy', ' www.centralbank.ie')
q1_fig = PAP + 'p03-q1-infographic'
add('sa-q1-i', '3-5', 'highest-and-lowest-forecast-growth-years', ref(1, '(i)', sa=True),
    O.ask(3, 'Using the information above, complete the table below.', ' Economic growth:')
    .removesuffix(' (ii) Explain the term economic growth.'), '9', 9,
    [point('r-highest', '2022', None, 'Highest: 2022, at 7.1%.'),
     point('r-lowest', '2020', None,
           'Lowest: 2020, at −4.9%, a fall in output. The scheme prices the two together as 6 + 3, '
           'the first correct answer 6 and the second 3.')],
    kind='questionTotal', stem=q1_stem, figure=q1_fig, **A)
add('sa-q1-ii', '3-5', 'what-economic-growth-is', ref(1, '(ii)', sa=True),
    O.ask(3, 'Explain the term economic growth.', ' Economic growth:'), '6', 6,
    [point('r-1', O.run('It is the increase in GNP / output', '2. In April 2022'), 6,
           'Explain the term, 6 marks; any of the wordings separated by a slash. The chart shows rates '
           'of change: the negative rate in 2020 is a contraction, a smaller positive rate slower growth.')],
    stem=q1_stem, figure=q1_fig, **A)

# Q2 ─ the census
q2_stem = O.ask(4, 'In April 2022 the CSO conducted a census', ' (i)')
add('sa-q2-i', '0-0', 'what-the-cso-is', ref(2, '(i)', sa=True),
    O.ask(4, 'What do the initials CSO stand for?', ' (ii)') + ' (POS in the Irish paper)', '9', 9,
    [point('r-1', 'Central Statistics Office', 9, 'Write the name out in full, 9 marks.')],
    stem=q2_stem, **A)
pick('sa-q2-ii', '0-0', 'what-the-census-is-used-for', ref(2, '(ii)', sa=True),
     O.ask(4, 'Explain one use the Irish Government would make', ' Question 3'),
     'A use of the census information — any one',
     bl('• Helps the government plan future infrastructural', '4 | P a g e'),
     1, 6, 'One developed use, 6 marks.', stem=q2_stem, **A)

# Q3 ─ online shopping
add('sa-q3-i', '1-1', 'online-shopping-cause-and-retailer-disadvantage', ref(3, sa=True),
    O.ask(4, 'Outline one possible reason for this development.', ' One reason:') + ' '
    + O.ask(4, 'Outline one possible disadvantage of this development', ' One disadvantage:'), '15', 15,
    [shared('r-reason', 'One reason more consumers shopped online',
            bl('• Lockdowns due to Covid-19:', '(ii) Outline one possible disadvantage'),
            'Complete BOTH parts. The scheme prices (i) and (ii) together as one 15: the first correct '
            'answer 9 marks (6 + 3) and the second 6 (3 + 3), with no fixed share for either part.'),
     shared('r-disadvantage', 'One disadvantage for local retailers',
            bl('• Reduced sales / profits:', '4. Apple released'),
            'A disadvantage for local shops.')],
    kind='questionTotal',
    stem=O.ask(4, 'During 2020 and 2021 more Irish consumers shopped online.', ' (i)'), **A)

# Q4 ─ substitutes and complements
add('seca-q4-ticks', '1-1', 'substitutes-and-complements-for-the-iphone', ref(4, sa=True),
    O.ask(5, 'Apple released the iPhone 13 in September 2021.', ' Substitute Goods'), '15', 15,
    [point('r-samsung', 'Substitute — Samsung S21', None, 'Samsung S21: SUBSTITUTE, a rival phone.'),
     point('r-case', 'Complementary — iPhone 13 case', None, 'iPhone 13 case: COMPLEMENTARY, used with the phone.'),
     point('r-plug', 'Complementary — iPhone charging plug', None,
           'iPhone charging plug: COMPLEMENTARY.'),
     point('r-pixel', 'Substitute — Google Pixel 4A smartphone', None,
           'Google Pixel 4A: SUBSTITUTE. The scheme prices the four ticks together as 15, the first '
           'correct 9 and the other three 2 each; the completed table is shown in the figure.')],
    kind='questionTotal', figure=SOL + 'p06-q4-ticks', **A)

# Q5 ─ the minimum wage
q5_stem = O.ask(5, 'The government increased the minimum wage by 30c', ' (a)')
add('sa-q5-a', '2-1', 'advantages-of-a-higher-minimum-wage', ref(5, '(a)', sa=True),
    O.ask(5, 'Outline two advantages for the Irish economy of increasing', ' 1. 2.'), '9 + 6', 15,
    [steps('r-1', 'An advantage for the Irish economy — any two',
           bl('• Increase in tax revenue:', 'OR\n(b) Outline two advantages'), 9, 6, 'advantages')],
    stem=q5_stem, notes='Answer either (a) or (b).', **A)
add('sa-q5-b', '2-1', 'employee-advantages-of-a-higher-minimum-wage', ref(5, '(b)', sa=True),
    O.ask(5, 'Outline two advantages for employees of this increase', ' 1. 2.'), '9 + 6', 15,
    [steps('r-1', 'An advantage for employees — any two',
           bl('• Increased standard of living:', '6 | P a g e'), 9, 6, 'advantages')],
    stem=q5_stem, notes='Answer either (a) or (b).', **A)

# Q6 ─ unemployment
q6_stem = O.ask(6, 'The graph below shows the monthly number of people unemployed', ' Number of people unemployed')
q6_fig = PAP + 'p06-i0'
add('seca-q6-i', '3-2', 'peak-months-of-unemployment', ref(6, '(i)', sa=True),
    O.ask(6, 'Identify the two months when the number of people unemployed', ' Month 1:'), '9', 9,
    [point('r-1', 'Month 1: March (2021)', None, 'March 2021, the top of the curve.'),
     point('r-2', 'Month 2: April (2021)', None,
           'April 2021. The scheme prices the two together as 6 + 3, the first correct answer 6 and '
           'the second 3.')],
    kind='questionTotal', stem=q6_stem, figure=q6_fig, **A)
add('sa-q6-ii', '3-2', 'why-unemployment-rose-in-lockdown', ref(6, '(ii)', sa=True),
    O.ask(6, 'Outline one reason for the increase in unemployment', ' Leaving'), '6', 6,
    [point('r-1', O.run('The imposition of a national lockdown', '7 | P a g e'), 6,
           'The reason, 6 marks: the lockdown forced businesses to let workers go.')],
    stem=q6_stem, figure=q6_fig, **A)

# Q7 ─ costs of a bakery
add('sa-q7-a-i', '1-5', 'what-fixed-costs-are', ref(7, '(a)(i)', sa=True),
    O.ask(7, 'Explain the term fixed costs.', ' (ii)'), '5', 5,
    [point('r-1', O.run('Costs which do not change as output changes', '(ii) Indicate by means'), 5,
           'Explain the term, 5 marks.')],
    notes='Answer either (a) or (b).', **A)
add('seca-q7-a-ii-ticks', '1-5', 'sorting-fixed-and-variable-costs', ref(7, '(a)(ii)', sa=True),
    O.ask(7, 'Indicate by means of a tick', ' Fixed Cost Variable Cost'), '4 + 4 + 1 + 1', 10,
    [point('r-wages', 'Variable — Wages €1,000', None, 'Wages: VARIABLE, they rise with output.'),
     point('r-materials', 'Variable — Raw Materials €1,500', None, 'Raw materials: VARIABLE.'),
     point('r-light', 'Variable — Light & Heat €300', None, 'Light and heat: VARIABLE.'),
     point('r-rent', 'Fixed — Rent of the premises €750', None,
           'Rent: FIXED, owed whatever the output. The scheme prices the four together as 4 + 4 + 1 + '
           '1 without naming which row earns which; the completed table is shown in the figure.')],
    kind='questionTotal', figure=SOL + 'p09-q7aii-ticks', notes='Answer either (a) or (b).', **A)
q7b_stem = O.ask(7, 'A bakery receives €5,000 in total', ' (i)')
add('sa-q7-b-i', '1-5', 'adding-up-a-bakerys-total-cost-for-the-week', ref(7, '(b)(i)', sa=True),
    O.ask(7, 'The total cost of operating the bakery for the week.', ' (ii)') + ' '
    + O.ask(7, 'Show your workings.', ' Total Cost:'), '5 x 2', 10,
    [point('r-1', '€1,000 + €1,500 + €300 + €750 = €3,550', 10,
           'Add every cost in the table, fixed and variable: €3,550. Five steps at 2 marks; deduct 1 if '
           'the € is omitted.')],
    stem=q7b_stem, figure=PAP + 'p07-i0', notes='Answer either (a) or (b).', **A)
add('sa-q7-b-ii', '1-5', 'net-profit-from-total-revenue-and-total-cost', ref(7, '(b)(ii)', sa=True),
    O.ask(7, 'The net profit the bakery earned in the week.', ' Show') + ' '
    + O.ask(7, 'Show your workings.', ' Total Cost:'), '2 + 2 + 1', 5,
    [point('r-1', 'Total revenue – Total Costs = Net Profit', 5,
           'Net profit = €5,000 − €3,550 = €1,450, the total cost carried from (i). The scheme awards '
           '2 + 2 + 1 and deducts 1 if the € is omitted; the official working is shown in the figure.')],
    stem=q7b_stem, figure=SOL + 'p09-q7bii-working', notes='Answer either (a) or (b).', **A)

# Q8 ─ vaccines
add('sa-q8-i', '2-2', 'vaccination-externality-and-opportunity-cost', ref(8, sa=True),
    O.ask(8, 'State one example of a positive externality', ' (ii)') + ' '
    + O.ask(8, 'Outline one opportunity cost for the Irish government', ' Question 9'), '15', 15,
    [shared('r-externality', 'One positive externality of vaccination',
            bl('• Protection of others from contracting the virus:', '(ii) Outline one opportunity cost'),
            'Complete BOTH parts. The scheme prices (i) and (ii) together as one 15: the first correct '
            'answer 9 marks (6 + 3) and the second 6 (3 + 3), with no fixed share for either part.'),
     shared('r-opportunity-cost', 'One opportunity cost for the government',
            [O.run('The money the government could have used', '9 | P a g e')],
            'Name what else the money could have paid for.')],
    kind='questionTotal',
    stem=O.ask(8, '51.6% of the world population has received', ' Adapted from'), **A)

# Q9 ─ price elasticity of demand
q9_stem = O.ask(8, 'The price of an iPad falls from €750 to €500.', ' ∆Q')
add('seca-q9-i', '1-4', 'working-the-ped-formula', ref(9, '(i)', sa=True),
    O.ask(8, 'Using the formula above, complete the workings', ' Workings:'), '13', 13,
    [point('r-1', '- 1', 13,
           'PED = (ΔQ ÷ ΔP) × ((P1 + P2) ÷ (Q1 + Q2)) = (15,000 ÷ −250) × (1,250 ÷ 75,000) = −1. Keep '
           'the minus sign. The calculation is worth 13 marks; the official working is shown in the '
           'figure.')],
    stem=q9_stem, figure=SOL + 'p11-q9i-working', **A)
add('sa-q9-ii', '1-4', 'interpreting-a-ped-value', ref(9, '(ii)', sa=True),
    O.ask(8, 'Indicate if the demand is price elastic', ' Answer: Leaving'), '2', 2,
    [point('r-1', 'UNIT ELASTIC', 2, 'Unit elastic, 2 marks: the PED from (i) is exactly −1.')],
    stem=q9_stem, **A)

# Q10 ─ interest on the national debt
q10_stem = O.ask(9, 'The graph below shows the amount of interest paid', ' General Government')
q10_fig = PAP + 'p09-q10-chart'
add('sa-q10-a', '3-1', 'comparing-debt-interest-payments', ref(10, '(a)', sa=True),
    O.ask(9, 'Compare the interest paid on the national debt in 2018', ' Compare:'), '9 + 3 + 3', 15,
    [point('r-1', O.run('The interest to be paid on the National Debt in 2024', 'OR\n(b) Explain the term'), 15,
           'The comparison and its two figures, 15 marks (9 + 3 + 3): the 2024 forecast, €3.51bn, is '
           'well below the €5.32bn paid in 2018.')],
    stem=q10_stem, figure=q10_fig, notes='Answer either (a) or (b).', **A)
pick('sa-q10-b', '3-1', 'what-the-national-debt-is', ref(10, '(b)', sa=True),
     O.ask(9, 'Explain the term National Debt.', ' National Debt:'),
     'The national debt — either wording',
     at('Refers to the total amount of government borrowing', '11 | P a g e',
        ['Refers to the total amount of government borrowing', 'Refers to the total amount of money']),
     1, 15, 'Explain the term, 15 marks (9 + 3 + 3). Answer either (a) or (b).', stem=q10_stem,
     figure=q10_fig, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ streaming; monopoly
q11_stem = O.ask(10, 'The graph below shows the breakdown of streaming services in the US.', ' Streaming')
q11_fig = PAP + 'p10-art'
add('q11-a-i', '2-0', 'highest-and-lowest-market-share-in-streaming', ref(11, '(a)(i)'),
    O.ask(10, 'Using the data above complete the table below:', ' (ii)'), '9 + 3', 12,
    [point('r-highest', 'YouTube', None, 'Highest: YouTube, about 164 million users.'),
     point('r-lowest', 'Vimeo', None,
           'Lowest: Vimeo, about 15 million, just below Amazon Prime Video. The scheme prices the two '
           'together as 9 + 3, the first correct answer 9 and the second 3.')],
    kind='questionTotal', stem=q11_stem, figure=q11_fig)
add('q11-a-ii', '2-0', 'advantages-of-many-firms-for-consumers', ref(11, '(a)(ii)'),
    O.ask(10, 'Outline two advantages for consumers of many firms', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'An advantage for consumers — any two',
           bl('• Gives the consumer more choice', '12 | P a g e'), 8, 4, 'advantages')],
    stem=q11_stem, figure=q11_fig)
q11b_stem = O.ask(11, 'If Netflix were to buy out (take over)', ' (i)')
q11b_fig = PAP + 'p11-q11b-diagram'
c = add('q11-b-i', '2-0', 'labelling-a-monopoly-diagram', ref(11, '(b)(i)'),
        O.ask(11, 'Write out in full what each of the three numbered items', ' 1. 2. 3.'), '3 x 7', 21,
        [point('r-1', 'Price', 7, 'Item 1, the vertical axis, 7 marks.'),
         point('r-2', 'Marginal Cost', 7, 'Item 2, the steeper U-shaped curve through G, 7 marks.'),
         point('r-3', 'Marginal Revenue', 7,
               'Item 3, the steeper downward-sloping line, 7 marks. AC and AR are printed; write each '
               'item in full.')],
        stem=q11b_stem, figure=q11b_fig)
c['labelKey'] = [{'letter': '1', 'meaning': 'Price', 'askedInThisQuestion': True},
                 {'letter': '2', 'meaning': 'Marginal cost', 'askedInThisQuestion': True},
                 {'letter': '3', 'meaning': 'Marginal revenue', 'askedInThisQuestion': True},
                 {'letter': 'AC', 'meaning': 'Average cost', 'askedInThisQuestion': False},
                 {'letter': 'AR', 'meaning': 'Average revenue', 'askedInThisQuestion': False}]
add('q11-b-ii', '2-0', 'marking-output-price-and-average-cost-on-a-monopoly-diagram', ref(11, '(b)(ii)'),
    O.ask(11, 'Equilibrium occurs at the point G on the diagram above.', ' Leaving')
    + ' On the Irish paper use C₁ for output and Co₁ for average cost; the price label is P₁.', '4 + 4 + 1', 9,
    [point('r-q1', O.run('• The output the firm will produce in equilibrium', '• The price the firm will').removeprefix('• '), 4,
           'Q1, 4 marks: drop straight down from G, where MC cuts MR, to the quantity axis.'),
     point('r-p1', O.run('• The price the firm will charge', '• The average cost of producing').removeprefix('• '), 4,
           'P1, 4 marks: go up from Q1 to the AR curve and across to the price axis; the price is read '
           'off AR, not off G.'),
     point('r-c1', O.run('• The average cost of producing this output', '13 | P a g e').removeprefix('• '), 1,
           'C1, 1 mark: average cost read off AC above the same Q1, below P1. The official diagram is '
           'shown in the figure.')],
    stem=q11b_stem, figure=SOL + 'p14-q11bii-diagram')
q11c_stem = O.ask(12, 'In some industries a firm can become a monopoly.', ' (i)')
add('q11-c-i', '2-0', 'what-a-monopoly-is', ref(11, '(c)(i)'),
    O.ask(12, 'Explain the term monopoly and give one example', ' Explanation:'), '5 + 4', 9,
    [point('r-definition', 'A monopoly firm arises when there is only one firm in the industry.', 5,
           'Explain the term, 5 marks.'),
     point('r-example', 'An example — An Post, Irish Rail, Irish Water, a sole pub in your village.', 4,
           'One Irish example, 4 marks; the scheme accepts these.')],
    stem=q11c_stem)
pick('q11-c-ii', '2-0', 'barriers-to-entry', ref(11, '(c)(ii)'),
     O.ask(12, 'Firms who may wish to enter a monopoly industry', ' 1. 2.'),
     'A barrier to entry — any two', bl('• The Government may grant a company', '(iii) Suggest one way'),
     2, 4, 'Two barriers, 4 marks each (2 + 2).', stem=q11c_stem)
pick('q11-c-iii', '1-3', 'government-intervention-dominant-firm', ref(11, '(c)(iii)'),
     O.ask(12, 'Outline one way, governments can intervene', ' 75 marks'),
     'A way the government can intervene — either one', bl('• Regulation:', '14 | P a g e'),
     1, 4, 'One developed way, 4 marks (2 + 2).', stem=q11c_stem)

# Q12 ─ coffee cups; Gym + Coffee; sustainability
add('q12-a-i', '1-0', 'plotting-demand-supply-and-market-equilibrium', ref(12, '(a)(i)–(iii)'),
    O.ask(13, 'Using the above information and on one diagram', ' Demand and Supply Curves')
    + ' On the Irish paper use C₁ for quantity; the price label is P₁.', '28 (14 x 2)', 28,
    [point('r-diagram', 'Demand and Supply Curves Reusable Coffee Cups', 28,
           'The diagram, 28 marks (14 x 2): plot demand falling from 10,000 cups at €9 to 50,000 at €5 '
           'and supply rising from 10,000 at €5 to 50,000 at €9, label them D and S, and mark P1 = €7 '
           'and Q1 = 30,000 where they cross (the horizontal axis is in thousands). The official graph is '
           'shown in the figure.')],
    stem=O.ask(13, 'The information below represents the market demand and supply schedules', ' Price (€)'),
    figure=SOL + 'p16-q12a-diagram')
q12b_stem = O.ask(14, 'The diagram below shows the demand and supply curves for Gym', ' S D')
q12b_sol = SOL + 'p17-q12b-diagram'
add('q12-b-i', '1-1', 'what-shifts-demand', ref(12, '(b)(i)'),
    O.ask(14, 'If a celebrity was featured on a social media platform', ' (ii)'), '8', 8,
    [point('r-1', O.run('This would lead to an increase in the quantity demanded', '(ii) Show, on the above'), 8,
           'The effect and why, 8 marks: the endorsement makes the clothing more attractive and better '
           'known, so demand rises.')],
    stem=q12b_stem, figure=PAP + 'p14-q12b-diagram')
add('q12-b-ii', '1-1', 'showing-a-demand-shift-after-a-celebrity-endorsement', ref(12, '(b)(ii)'),
    O.ask(14, 'Show, on the above diagram how the change in (i)', ' (iii)'), '8', 8,
    [point('r-1', 'Demand curve would shift to the right – D2 above on diagram.', 8,
           'Shift demand right to D2, 8 marks: tastes changed, not the price, so the whole curve moves. '
           'The official diagram is shown in the figure.')],
    stem=q12b_stem, figure=q12b_sol)
add('q12-b-iii', '1-0', 'reading-the-new-equilibrium-after-a-demand-shift', ref(12, '(b)(iii)'),
    O.ask(14, 'Show, on the above diagram, the new equilibrium price', ' Leaving')
    + ' On the Irish paper use C₂ for the new quantity; the new price label is P₂.', '6 + 6', 12,
    [point('r-price', 'the new equilibrium price (P2)', 6,
           'P2, 6 marks: the higher price where D2 meets the unchanged supply curve.'),
     point('r-quantity', 'the new equilibrium quantity (Q2)', 6,
           'Q2, 6 marks: the higher quantity at the same new intersection.')],
    stem=q12b_stem, figure=q12b_sol)
q12c_stem = O.ask(15, 'Nineteen30 café in Limerick was founded in 2021.', ' Adapted from')
pick('q12-c-i', '0-2', 'what-sustainability-is', ref(12, '(c)(i)'),
     O.ask(15, 'Explain the term sustainability.', ' (ii)'),
     'Sustainability — either wording',
     at('Achieving economic growth without harming', '(ii) Suggest two ways',
        ['Achieving economic growth', 'Meeting the current needs']),
     1, 5, 'Explain the term, 5 marks (3 + 2).', stem=q12c_stem)
pick('q12-c-ii', '0-2', 'ways-a-business-can-be-sustainable', ref(12, '(c)(ii)'),
     O.ask(15, 'Suggest two ways that a business could be more sustainable.', ' 1. 2.'),
     'A way to be more sustainable — any two', bl('• Encourage use of own cups:', '17 | P a g e'),
     2, 7, 'Two ways, 7 marks each (4 + 3).', stem=q12c_stem)

# Q13 ─ government expenditure; national income; consumers
q13_stem = O.ask(16, 'The pie chart below gives the forecasted government current', ' Total Government')
add('q13-a-i-percentage', '3-1', 'current-spending-as-a-share-of-total-expenditure', ref(13, '(a)(i)'),
    O.ask(16, 'Calculate current expenditure as a percentage', ' Workings:'), '16', 16,
    [point('r-1', '86.61%', 16,
           'Current expenditure ÷ total expenditure × 100 = €71.82bn ÷ €82.92bn × 100 = 86.61%, 16 '
           'marks; the official working is shown in the figure.')],
    stem=q13_stem, figure=SOL + 'p19-q13ai-working')
q13a2_ask = O.ask(16, 'Explain current or capital government expenditure', ' Current expenditure:')
for cid, name, route, start, end, ex_start, ex_end in [
        ('q13-a-ii-expenditure', 'current', 'current expenditure', 'Current expenditure is spending',
         'Example: salaries', 'Example: salaries of state employees', '18 | P a g e'),
        ('q13-a-ii-capital', 'capital', 'capital expenditure', 'Capital expenditure is spending',
         'Example: building a school', 'Example: building a school', 'OR\nCurrent expenditure')]:
    add(cid, '3-1', f'{name}-government-expenditure', ref(13, '(a)(ii)', route),
        f'{q13a2_ask} Answer for: {route.upper()}.', '6 + 3', 9,
        [point('r-definition', O.run(start, end), 6, f'Explain {route}, 6 marks.'),
         point('r-example', O.run(ex_start, ex_end), 3, 'One relevant example, 3 marks.')],
        stem=q13_stem, figure=PAP + 'p16-q13-chart',
        notes='The paper asks for current OR capital expenditure; each is its own route.')
q13b_stem = O.ask(17, 'National Income is calculated using the following formula:', ' (i)')
add('q13-b-i', '3-0', 'the-national-income-formula', ref(13, '(b)(i)'),
    O.ask(17, 'State what each of the letters I, X and M stand for.', ' I:'), '12', 12,
    [point('r-i', 'Investment', None, 'I: investment.'),
     point('r-x', 'Exports', None, 'X: exports.'),
     point('r-m', 'Imports', None, 'M: imports. The scheme gives 12 for the three letters, with no '
           'published split.')],
    kind='questionTotal', stem=q13b_stem)
add('q13-b-ii', '3-0', 'calculating-the-multiplier-in-an-open-economy', ref(13, '(b)(ii)'),
    O.ask(17, 'Assume that MPS is 0.1 and MPM is 0.4.', ' Workings:'), '12', 12,
    [point('r-1', '2', 12,
           'Multiplier = 1 ÷ (MPS + MPM) = 1 ÷ (0.1 + 0.4) = 1 ÷ 0.5 = 2, 12 marks; the official working '
           'is shown in the figure.')],
    stem='The multiplier formula for an open economy is: 1 ÷ (MPS + MPM)', figure=SOL + 'p20-q13bii-working')
add('q13-b-iii', '3-0', 'meaning-of-the-multiplier', ref(13, '(b)(iii)'),
    O.ask(17, 'Explain the economic meaning of the figure you have calculated', ' Explanation:'), '6', 6,
    [point('r-1', 'For each euro spent in the economy, National Income will increase by €2.', 6,
           'Explain, 6 marks: each extra €1 injected raises national income by €2 in total. The scheme’s '
           'other line, that national income “will double”, overstates it: the existing national income '
           'does not double.')])
q13c_stem = O.ask(18, 'Domestic demand is forecast to grow by 7.1% in 2023.', ' Adapted from')
pick('q13-c-i', '1-1', 'why-consumer-spending-rose', ref(13, '(c)(i)'),
     O.ask(18, 'Outline one possible reason for the expected increase in consumer spending', ' (ii)'),
     'A reason for the increase in consumer spending — any one',
     bl('• The easing of health restrictions:', '(ii) It is assumed that consumers'),
     1, 10, 'One developed reason, 10 marks (6 + 4).', stem=q13c_stem)
add('q13-c-ii', '1-1', 'what-a-rational-consumer-does', ref(13, '(c)(ii)'),
    O.ask(18, 'Explain the concept of consumers behaving rationally', ' Explanation:'), '10', 10,
    [shared('r-definition', 'What behaving rationally means',
            [O.run('Behaving rationally means the consumer acts', 'Example: If a consumer')],
            'Complete BOTH: the explanation and an example. The scheme prices the two together as one '
            '10: the first correct element 6 marks and the second 4.'),
     shared('r-example', 'One example of a rational choice',
            at('Example: If a consumer prefers', '20 | P a g e',
               ['Example: If a consumer prefers', 'If the trainers are for sale']),
            'The scheme gives these two.')],
    kind='questionTotal',
    stem=O.ask(18, 'It is assumed that consumers taking part in economic activity', ' Explain the concept'))

# Q14 ─ Glenisk: factors, water, development
q14_stem = O.ask(19, 'For three decades the Cleary family', ' Adapted from')
add('q14-a-i', '0-1', 'the-four-factors-of-production-in-a-yogurt-plant', ref(14, '(a)(i)'),
    O.ask(19, 'Complete the table below to show your understanding', ' Factor of'), '4 x 6', 24,
    [point('r-land', paras([line('Anything supplied by nature which helps in the production of yogurt. Ground'),
                            line('Milk Sugar Berries')]), 6,
           'Row 1, Land: explain it and give an example (milk, sugar or berries), 6 marks.'),
     point('r-labour', 'LABOUR — ' + line('The human effort involved in the production of yogurt. The workers'), 6,
           'Row 2: name the factor, Labour, and explain it, 6 marks.'),
     point('r-capital', paras([line('Man-made items used to produce Glenisk organic yogurt.'),
                               line('Machinery Equipment Vehicles The factory building')]), 6,
           'Row 3, Capital: explain it and give an example, 6 marks.'),
     point('r-enterprise', 'ENTERPRISE — The Cleary Family', 6,
           'Row 4: name the factor, Enterprise, and give an example, the Cleary family, 6 marks. The '
           'scheme prices each row 6, the first blank 4 and the second 2; the completed table is shown '
           'in the figure.')],
    stem=q14_stem, figure=SOL + 'p22-q14ai-table')
q14a2_stem = O.ask(20, 'Glenisk extracts water from local ponds', ' Adapted from')
pick('q14-a-ii-scarce', '0-1', 'what-a-scarce-resource-is', ref(14, '(a)(ii)'),
     O.ask(20, 'Explain what a scarce resource is.', ' Scarce resource:'),
     'A scarce resource — any wording',
     at('There is not enough water', '(iii) Comment on Glenisk',
        ['There is not enough water', 'The supply of a resource', 'Quantity of goods and services']),
     1, 3, 'Explain the term, 3 marks.', stem=q14a2_stem)
add('q14-a-iii-water', '0-2', 'sustainable-use-of-water', ref(14, '(a)(iii)'),
    O.ask(20, 'Comment on Glenisk’s approach to water usage', ' (b)'), '7', 7,
    [point('r-1', O.run('The company tries to minimise the wastage of water', '(b) The Organisation'), 7,
           'Comment, 7 marks: Glenisk cuts waste and uses water sustainably, reducing its impact on the '
           'environment.')],
    stem=q14a2_stem)
add('q14-b-i', '1-3', 'the-case-for-and-against-water-charges', ref(14, '(b)'),
    O.ask(20, 'Outline one economic argument in favour of the reintroduction', ' Leaving') + ' '
    + O.ask(21, 'Explain why some citizens in Ireland would be unhappy', ' Explanation:'), '17', 17,
    [shared('r-for', 'One argument for water charges',
            bl('• Better use of a scare resource:', '(ii) Explain why some citizens'),
            'Complete BOTH parts. The scheme prices (i) and (ii) together as one 17: the first correct '
            'answer 10 marks (6 + 4) and the second 7 (4 + 3), with no fixed share for either part.'),
     shared('r-against', 'Why some citizens would be unhappy',
            bl('• Lower standard of living:', '22 | P a g e'),
            'A reason citizens would object.')],
    kind='questionTotal',
    stem=O.ask(20, 'The Organisation for Economic Co-operation and Development', ' Adapted from'))
q14c_stem = O.ask(21, 'Glenisk partnered with the international development charity', ' Adapted from')
pick('q13-a-i', '4-0', 'features-of-a-less-developed-nation', ref(14, '(c)(i)'),
     O.ask(21, 'Outline two features/characteristics of a less developed nation.', ' 1. 2.'),
     'A feature of a less developed nation — any two',
     at('High population growth rates:', '23 | P a g e',
        ['High population growth rates:', 'Famine / low life expectancy:', 'High foreign debts',
         'Over-dependence on one crop:', 'High percentage of the population', 'Poor infrastructure:',
         'Poverty / low income per capita:', 'Poor levels of education', 'Exploitation by MNCs',
         'Political corruption:']),
     2, 8, 'Two features, 8 marks each (4 + 4).', stem=q14c_stem)
pick('q13-a-ii', '4-0', 'why-ireland-gives-aid', ref(14, '(c)(ii)'),
     O.ask(21, 'Outline two reasons why the Irish government gives aid', ' 1. 2.'),
     'A reason Ireland gives aid — any two',
     at('Promote economic development:', '24 | P a g e',
        ['Promote economic development:', 'Humanitarian reasons:', 'Reduce poverty, hunger etc:',
         'Support citizens cope', 'Improve access and quality of education:',
         'Provide access to clean water', 'Meet UN target']),
     2, 4, 'Two reasons, 4 marks each (2 + 2).', stem=q14c_stem)

# Q15 ─ corporation tax; MNCs; exports
q15_stem = O.ask(22, 'The graph below shows the corporation tax received', ' Corporation Tax')
q15_fig = PAP + 'p22-q15a-chart'
add('q15-a-i-trend', '3-1', 'reading-corporation-tax-trends', ref(15, '(a)(i)'),
    O.ask(22, 'Explain the trend in corporation tax received', ' Explanation:'), '6 + 4', 10,
    [point('r-1', O.run('There has been a steady increase in the amount of money', 'It has increased from approx.'), 10,
           'The trend 6 and figures 4: a steady rise from about €3,500 million in 2011 to about €12,000 '
           'million in 2020 (about €3.5bn to €12bn). The scheme writes “€4m to €12m”; the axis is in '
           'millions of euro.')],
    stem=q15_stem, figure=q15_fig)
add('q15-a-ii', '3-1', 'what-corporation-tax-pays-for', ref(15, '(a)(ii)'),
    O.ask(22, 'Explain the benefits of the government collecting corporation tax.', ' Leaving'), '6 + 3', 9,
    [point('r-revenue', O.run('Provides revenue for the government', 'Provide public services:'), 6,
           'Increased revenue for the government, 6 marks.'),
     heading('r-services', 'What the revenue provides — any one',
             at('Provide public services:', '2 concepts:',
                ['Provide public services:', 'Help to re-distribute wealth:', 'Promote / support industry:']), 3,
             'Link it to the services it pays for, 3 marks. The scheme marks two linked concepts: '
             'increased revenue 6, to provide additional services for citizens 3.')],
    stem=q15_stem, figure=q15_fig)
q15b_stem = O.ask(23, 'TikTok shortlists five Dublin sites for new headquarters.', ' Adapted from')
pick('q15-b-i', '4-1', 'mncs-in-ireland', ref(15, '(b)(i)'),
     O.ask(23, 'Name two other Multi-National Corporations operating in Ireland.', ' 1. 2.'),
     'A multinational operating in Ireland — any two',
     ['Apple', 'Google', 'Facebook', 'Coca-Cola', 'PayPal', 'Microsoft', 'Twitter', 'Pfizer', 'Intel',
      'Dell', 'IBM', 'Glanbia', 'Kerry Group', 'Ryanair'],
     2, 6, 'Two other multinationals, 6 marks each; these are the scheme’s examples.', stem=q15b_stem)
pick('q14-a-ii', '4-1', 'why-mncs-locate-in-ireland-ol', ref(15, '(b)(ii)'),
     O.ask(23, 'Outline two reasons why TikTok would locate in Ireland.', ' 1. 2.'),
     'A reason TikTok would locate in Ireland — any two',
     at('Availability of a skilled educated', '(iii) Describe two possible economic benefits',
        ['Availability of a skilled educated', 'Low rates of taxation:', 'Access to EU market',
         'Availability of state incentives:', 'Good industrial relations:', 'Stable rate of economic growth:',
         'Stable economic climate:']),
     2, 4, 'Two reasons, 4 marks each (2 + 2).', stem=q15b_stem)
pick('q14-a-iii', '4-1', 'local-benefits-of-an-mnc', ref(15, '(b)(iii)'),
     O.ask(23, 'Describe two possible economic benefits to the local community', ' 1. 2.'),
     'A benefit to the local community — any two',
     at('Creation of employment:', '26 | P a g e',
        ['Creation of employment:', 'Increased economic growth:', 'Increase in economic activity locally:',
         'More vibrant local communities:', 'Improvements in the local infrastructure:']),
     2, 4, 'Two benefits, 4 marks each (2 + 2).', stem=q15b_stem)
q15c_stem = O.ask(24, 'The graph below shows exports out of Ireland to the US', ' Exports from Ireland')
add('q15-c-i', '4-2', 'reading-irish-export-trends', ref(15, '(c)(i)'),
    O.ask(24, 'Comment on the trends in Irelands exports', ' 1.Exports'), '6 + 6', 12,
    [point('r-us', O.run('Have been consistent to the US', 'Exports to the UK'), 6,
           'Exports to the US, 6 marks: a trend with figures, about €4bn or more most months.'),
     point('r-uk', O.run('Exports between €1bn and approx. €2bn', '(ii) Outline two benefits'), 6,
           'Exports to the UK, 6 marks: between about €1bn and €2bn, much lower than to the US.')],
    stem=q15c_stem, figure=PAP + 'p24-q15c-chart')
pick('q14-b-ii', '4-2', 'benefits-of-exporting', ref(15, '(c)(ii)'),
     O.ask(24, 'Outline two benefits to the Irish economy of exporting', ' 1. 2.'),
     'A benefit of exporting — any two',
     at('Employment creation:', '27 | P a g e',
        ['Employment creation:', 'Increased GNP / economic growth:', 'Government finances:',
         'Attract investment:', 'Increased sales / profits:']),
     2, 8, 'Two benefits, 8 marks each (4 + 4).', stem=q15c_stem, figure=PAP + 'p24-q15c-chart')

# Q16 ─ minimum unit pricing and cigarettes; inflation; indirect tax and the hidden economy
q16_stem = O.ask(25, 'The table below shows the effect on alcohol prices', ' Minimum Unit Price for')
pick('q15-a-i', '1-3', 'minimum-pricing-on-alcohol', ref(16, '(a)(i)'),
     O.ask(25, 'Outline two reasons why the government introduced minimum pricing', ' 1. 2.'),
     'A reason for minimum pricing — any two',
     bl('• To reduce alcohol abuse / consumption', '(ii) The government increased the price'),
     2, 6, 'Two reasons, 6 marks each (3 + 3).', stem=q16_stem, figure=PAP + 'p25-i0')
pick('q16-a-ii-smoking', '1-3', 'measures-to-reduce-smoking', ref(16, '(a)(ii)'),
     O.ask(25, 'The government increased the price of a packet of cigarettes', ' Leaving'),
     'Another measure to reduce smoking — any one',
     bl('• Consumer awareness / education:', '28 | P a g e'),
     1, 7, 'One developed measure, 7 marks (4 + 3).')
q16a3_ask = O.ask(26, 'Outline one social benefit and one private benefit', ' Social benefit:')
for cid, label, route, start, end, concept in [
        ('q15-a-iii-social', 'Social benefit:', 'social benefit', '• Greater productivity/reduction',
         'Private Benefits:', 'social-benefits-of-cigarette-tax'),
        ('q15-a-iii-private', 'Private benefit:', 'private benefit', '• Increased disposable incomes:',
         '29 | P a g e', 'private-benefits-of-cigarette-tax')]:
    pick(cid, '2-2', concept, ref(16, '(a)(iii)', route), f'{q16a3_ask} {label}',
         f'A {route} — any one', bl(start, end), 1, 4,
         f'One {route}, 4 marks (2 + 2). The question asks for one of each and the scheme prices each 4.')
q16b_stem = O.ask(26, 'The annual rate of price inflation in Ireland rose by 5.5%', ' Adapted from')
pick('q16-b-i', '3-3', 'what-price-inflation-is', ref(16, '(b)(i)'),
     O.ask(26, 'Explain the term price inflation.', ' (ii)'),
     'Price inflation — either wording',
     at('An increase in the general level of prices', '(ii) Discuss two economic effects',
        ['An increase in the general level', 'A decrease in the value of money']),
     1, 8, 'Explain the term, 8 marks (6 + 2).', stem=q16b_stem)
pick('q16-a-ii', '3-3', 'effects-of-inflation-on-citizens', ref(16, '(b)(ii)'),
     O.ask(26, 'Discuss two economic effects which this rate of price inflation', ' 1. 2.'),
     'An effect on Irish citizens — any two',
     bl('• Reduction in purchasing power:', '30 | P a g e'),
     2, 8, 'Two effects, 8 marks each (4 + 4).', stem=q16b_stem)
q16c_stem = O.ask(27, 'Excise duties rose by €100 million to almost €1.7bn last year.', ' Adapted from')
add('q16-c-i', '3-1', 'what-an-indirect-tax-is', ref(16, '(c)(i)'),
    O.ask(27, 'Excise duties are an example of an indirect tax.', ' Explanation:'), '8', 8,
    [point('r-response', O.run('An indirect tax is a tax on the consumption', '(ii) The smuggling'), None,
           'Explain indirect tax and give one example other than excise duties. The scheme gives one 8 '
           'for the explanation and the example together, with no published split.')],
    kind='questionTotal', stem=q16c_stem)
add('q16-c-ii', '3-0', 'what-the-hidden-economy-is', ref(16, '(c)(ii)'),
    O.ask(27, 'Explain the term hidden economy, giving one other example', ' Explanation:'), '8', 8,
    [point('r-definition-example', O.run('The hidden economy refers to economic activity', '(iii) Outline one economic'),
           None, 'Explain the hidden economy and give one example other than cigarette smuggling. The '
           'scheme gives one 8 for both (its English layout prints this 8 beside the example; the Irish '
           'scheme places an 8 beside each of (i), (ii) and (iii)).')],
    kind='questionTotal',
    stem=O.ask(27, 'The smuggling of cigarettes into Ireland is an example', ' Explain the term'))
pick('q16-c-iii', '3-0', 'effects-of-the-hidden-economy', ref(16, '(c)(iii)'),
     O.ask(27, 'Outline one economic effect for the Irish economy of activities', ' One economic effect:'),
     'An economic effect of the hidden economy — any one',
     bl('• Loss of revenue to the government:', '31 | P a g e'),
     1, 8, 'One developed effect, 8 marks.', stem=q16c_stem)

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('seca-q4-ticks', 'p05-q4-question'), ('seca-q7-a-ii-ticks', 'p07-q7aii-question'),
                 ('sa-q7-b-ii', 'p07-q7b-question'), ('seca-q9-i', 'p08-q9i-question'),
                 ('q11-b-ii', 'p11-q11bii-question'), ('q12-a-i', 'p13-q12a-question'),
                 ('q12-b-ii', 'p14-q12b-question'), ('q12-b-iii', 'p14-q12b-question'),
                 ('q13-a-i-percentage', 'p16-q13ai-question'), ('q13-b-ii', 'p17-q13bii-question'),
                 ('q14-a-i', 'p19-q14ai-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# Earlier extractors split four jointly priced answers into one card per part.
# Each half is still emitted, lifted from its own part, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('q12-a-ii', 'q12-a-i', 'The market supply curve', ['Demand and Supply Curves Reusable Coffee Cups'], 14),
    ('sa-q3-ii', 'sa-q3-i', 'One disadvantage for local retailers',
     bl('• Reduced sales / profits:', '4. Apple released'), 6),
    ('sa-q8-ii', 'sa-q8-i', 'One opportunity cost for the government',
     [O.run('The money the government could have used', '9 | P a g e')], 6),
    ('q14-b-ii-water', 'q14-b-i', 'Why some citizens would be unhappy',
     bl('• Lower standard of living:', '22 | P a g e'), 7),
]
for old, canonical, label, options, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this part is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
