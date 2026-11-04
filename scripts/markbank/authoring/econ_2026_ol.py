#!/usr/bin/env python3
"""Economics 2026 Ordinary Level, Sections A and B.

Authored from the independent census in drafts/economics-2026-ol-ev.json,
made from a visual sweep of all 32 paper pages and 47 scheme pages before any
2026 Ordinary card existed. Question wording and stems are sliced from the
question paper; every marking point is sliced from the scheme (econ_2026_lib).
The only prose written here is guidance: tariffs, route labels and what a
figure or a calculation shows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, emit, point  # noqa: E402

O = Sheet(2026, 'ordinary', 'LC034GLP000EV')
D = Deck(2026, 'ordinary')
cards, add, pick, heading, ref, stance = D.cards, D.add, D.pick, D.heading, D.ref, D.stance
A = dict(section='A')
FIG = 'economics-2026-OL-scheme-'
QFIG = 'economics-2026-OL-paper-'
# The whole printed question, for the card whose figure slot holds a solution.
FULLQ = {'q11-b-ii': 'p12-q11bii-question'}


def paras(options):
    return '\n\n'.join(options)


def lines(start, end, occ=None):
    """The scheme's one-per-line list between two anchors (no bold headings)."""
    raw = O.chunk(start, end, occ)
    return [x.strip() for x in raw.split('\n')[1:] if x.strip() and '| P a g e' not in x]


def stance_one(prefix, choices, topic, concept, q, parts, qtext, per, *, sa=False, stem=''):
    """A printed either/or whose routes ask for one item each (not a stance to justify)."""
    for suffix, word, label, options, prompt in choices:
        pick(f'{prefix}-{suffix}', topic, concept, ref(q, parts, word, sa),
             f'{qtext} {prompt}', label, options, 1, per,
             f'One developed answer for the {word} route, {per} marks. The scheme credits both '
             f'routes; these are its examples, not a closed list.',
             stem=stem, section='A' if sa else 'B')


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ the CSO; exports
q1_stem = O.ask(3, 'The Minister for Enterprise', ' Adapted from')
add('sa-q1-i', '0-0', 'what-cso-stands-for', ref(1, '(i)', sa=True),
    O.ask(3, 'What do the initials CSO stand for?', ' Central S O'), '6', 6,
    [point('r-s', 'Statistics', None, 'The S: Statistics.'),
     point('r-o', 'Office', None, 'The O: Office. Central is given; first correct 4 marks, second 2.')],
    kind='questionTotal', stem=q1_stem,
    notes='The scheme pays the first correct word 4 and the second 2 (1st x 4, 2nd x 2).', **A)
add('sa-q1-ii', '4-2', 'an-export-and-why-ireland-exports', ref(1, '(ii)', sa=True),
    O.ask(3, 'Give one example of goods that Ireland exports', ' Example of export:'), '6', 6,
    [point('r-example', paras(O.menu('Example:\nPharmaceuticals', 'Reason:\nTo earn', [5])), None,
           'One example of an Irish export.'),
     point('r-reason', paras(O.menu('Reason:\nTo earn', '2 Figures from the Society', [5])), None,
           'One reason Ireland exports. Example AND reason are both required: first correct 4 '
           'marks, second 2.')],
    kind='questionTotal', stem=q1_stem,
    notes='1st x 4, 2nd x 2 across the example and the reason; no fixed side split.', **A)

# Q2 ─ electric cars (answer (a) or (b))
q2_stem = O.ask(4, 'Figures from the Society of the Irish Motor Industry', ' Adapted from')
q2a = O.ask(4, 'Discuss one private benefit or one social benefit', ' Indicate your choice')
stance_one('sa-q2-a', [
    ('private', 'private benefit', 'A private benefit — any one',
     O.menu('Private Benefits:', 'Social Benefits:', [6]), 'Ticked box: PRIVATE BENEFIT.'),
    ('social', 'social benefit', 'A social benefit — any one',
     O.menu('Social Benefits:', '(b) Outline one way in which the Irish Government', [6]),
     'Ticked box: SOCIAL BENEFIT.'),
], '2-2', 'private-or-social-benefit-of-electric-cars', 2, '(a)', q2a, 12, sa=True, stem=q2_stem)
q2b = O.ask(4, 'Outline one way in which the Irish Government or car retailers', ' Indicate your choice')
stance_one('sa-q2-b', [
    ('government', 'Irish Government', 'A government measure — any one',
     O.menu('Irish Government:', 'Car retailers:', [7]), 'Ticked box: GOVERNMENT.'),
    ('retailers', 'car retailers', 'A car-retailer measure — any one',
     O.menu('Car retailers:', '3 Department stores including Brown Thomas', [7]),
     'Ticked box: CAR RETAILERS.'),
], '1-3', 'encouraging-electric-car-purchases', 2, '(b)', q2b, 12, sa=True, stem=q2_stem)

# Q3 ─ paper bag charges (answer (a) or (b))
q3_stem = O.ask(5, 'Department stores including Brown Thomas', ' (a)')
pick('sa-q3-a', '0-2', 'advantage-of-charging-for-bags', ref(3, '(a)', sa=True),
     O.ask(5, 'Outline one possible advantage', ' Advantage:'), 'An advantage — any one',
     O.menu('paper carrier bags.\nEncourages Sustainable Consumer Habits', '(b) Outline one possible disadvantage', [7, 8]),
     1, 12, 'One developed advantage, 12 marks. Answer (a) or (b).', stem=q3_stem, **A)
pick('sa-q3-b', '0-2', 'disadvantage-of-charging-for-bags', ref(3, '(b)', sa=True),
     O.ask(5, 'Outline one possible disadvantage', ' Disadvantage:'), 'A disadvantage — any one',
     O.menu('branded paper carrier bags.\nPerceived', '4 (a) Do you consider this proposed spending', [8]),
     1, 12, 'One developed disadvantage, 12 marks. Answer (a) or (b).', stem=q3_stem, **A)

# Q4 ─ Cork light rail (answer (a) or (b))
q4_stem = O.ask(6, 'The Government is proposing the development', ' Adapted from')
add('sa-q4-a', '3-1', 'light-rail-as-capital-spending', ref(4, '(a)', sa=True),
    O.ask(6, 'Do you consider this proposed spending', ' Current: Capital:'), '12', 12,
    [point('r-tick', 'Capital', None, 'Tick CAPITAL: the scheme ticks Capital only.'),
     point('r-explain', O.run('Capital expenditure is spending by the government', '(b) Outline one possible economic advantage'),
           None, 'Explain why it is capital expenditure. Answer (a) or (b).')],
    kind='questionTotal', stem=q4_stem,
    notes='The scheme gives 12 for the classification and its explanation together.', **A)
q4b = O.ask(6, 'Outline one possible economic advantage or one possible economic disadvantage', ' Indicate your choice')
stance_one('sa-q4-b', [
    ('advantage', 'advantage', 'An economic advantage — any one',
     O.menu('Advantage:\n⟨12⟩\nJob creation', 'Disadvantage:\nHigh construction', [9]), 'Ticked box: ADVANTAGE.'),
    ('disadvantage', 'disadvantage', 'An economic disadvantage — any one',
     O.menu('Disadvantage:\nHigh construction', '5 Discuss one possible advantage or one possible disadvantage', [9]),
     'Ticked box: DISADVANTAGE.'),
], '3-1', 'advantage-or-disadvantage-of-cork-light-rail', 4, '(b)', q4b, 12, sa=True, stem=q4_stem)

# Q5 ─ overseas aid
q5_stem = ' '.join([O.ask(7, 'Ireland has an opportunity to show leadership', ' Adapted from'),
                    O.ask(7, 'Note: ODA is government aid', ' Discuss one')])
q5 = O.ask(7, 'Discuss one possible advantage or one possible disadvantage of aid', ' Place a tick')
stance_one('sa-q5', [
    ('advantage', 'advantage', 'An advantage of aid — any one',
     O.menu('countries.\nAdvantage:', 'Disadvantage:\nCreation of Aid', [10]), 'Ticked box: ADVANTAGE.'),
    ('disadvantage', 'disadvantage', 'A disadvantage of aid — any one',
     O.menu('Disadvantage:\nCreation of Aid Dependency', '6 College fees for third level', [10]),
     'Ticked box: DISADVANTAGE.'),
], '4-0', 'advantage-or-disadvantage-of-aid', 5, '', q5, 12, sa=True, stem=q5_stem)

# Q6 ─ college fees
add('sa-q6', '3-1', 'advantage-and-disadvantage-of-lower-college-fees', ref(6, sa=True),
    O.ask(7, 'Explain one advantage and one disadvantage of this €500', ' Advantage:'), '12', 12,
    [point('r-advantage', paras(O.menu('Advantage: 1stx 8', 'Disadvantage:\nIncreased Strain', [11])), None,
           'One advantage.'),
     point('r-disadvantage', paras(O.menu('Disadvantage:\nIncreased Strain', '7 2026 marks the 250th', [11])), None,
           'One disadvantage. Both are required: first correct 8 marks, second 4.')],
    kind='questionTotal', stem=O.ask(7, 'College fees for third level students', ' Adapted from'),
    notes='1st x 8, 2nd x 4 across the advantage and the disadvantage; no fixed side split.', **A)

# Q7 ─ canons of taxation
canon = {
    'b': ('3. The amount paid should be clear and straightforward.', 'B. Certainty matches explanation 3.'),
    'c': ('4. The amount of revenue collected should be greater than the cost of collection.',
          'C. Economy matches explanation 4.'),
    'd': ('1. The system of taxation should take a higher proportion of income in tax as income '
          'rises/the ability of each person to pay tax must be considered.', 'D. Equity matches explanation 1.'),
}
add('sa-q7', '3-1', 'matching-the-canons-of-taxation', ref(7, sa=True),
    O.ask(8, 'Match the canon of taxation', ' Canon Explanation'), '12', 12,
    [point(f'r-{k}', v, None, n) for k, (v, n) in canon.items()],
    kind='questionTotal', stem=O.ask(8, '2026 marks the 250th anniversary', ' Match the canon'),
    notes='Convenience (A) is given as 2. First correct match 8, second 2, third 2.', **A)
show_before_reveal(cards[-1], QFIG + 'p08-q7-canons-table')

# Q8 ─ the Deer Park steps
q8_stem = O.ask(8, 'The National Transport Authority paid', ' Adapted from')
stance('sa-q8', [
    ('agree', 'agree', 'A reason to agree', O.menu('Agree: ⟨12⟩', 'OR\nDisagree:', [13])),
    ('disagree', 'disagree', 'A reason to disagree', O.menu('OR\nDisagree:', '9 Outline one possible economic advantage', [13])),
], '0-1', 'waste-of-public-money', 8, '',
    O.ask(8, 'Indicate with a tick', ' Agree: Disagree:'), 12, sa=True, stem=q8_stem, section='A')

# Q9 ─ employment growth
add('sa-q9', '3-2', 'advantage-and-disadvantage-of-rising-employment', ref(9, sa=True),
    O.ask(9, 'Outline one possible economic advantage and one possible economic disadvantage', ' Economic advantage:'),
    '12', 12,
    [point('r-advantage', paras(O.menu('Advantage: 2ndx 4', 'Disadvantage:\nLabour/skills shortages', [14])), None,
           'One economic advantage.'),
     point('r-disadvantage', paras(O.menu('Disadvantage:\nLabour/skills shortages', '10 Adapted government expenditure', [14])),
           None, 'One economic disadvantage. Both are required: first correct 8 marks, second 4.')],
    kind='questionTotal', stem=O.ask(9, 'Although employment growth in Ireland', ' Percentage growth'),
    notes='1st x 8, 2nd x 4 across the advantage and the disadvantage; no fixed side split.', **A)
show_before_reveal(cards[-1], QFIG + 'p09-q9-employment-growth')

# Q10 ─ government expenditure
q10_stem = O.ask(10, 'Adapted government expenditure figures for 2025', ' Government Expenditure')
add('sa-q10-i', '3-1', 'highest-and-lowest-spending-areas', ref(10, '(i)', sa=True),
    O.ask(10, 'Using the information above, answer the following questions:', ' (ii)'), '6', 6,
    [point('r-highest', 'Social Protection', None, 'Highest: Social Protection, €27bn.'),
     point('r-lowest', 'Transport/Justice', None, 'Lowest: Transport or Justice, €4bn each. First '
           'correct 4 marks, second 2.')],
    kind='questionTotal', stem=q10_stem, **A)
add('sa-q10-ii', '3-1', 'examples-of-spending-by-area', ref(10, '(ii)', sa=True),
    O.ask(10, 'State one example of spending by the government in each', ' Health:', include_end=True),
    '6', 6,
    [point('r-social', 'Pensions, jobseeekers allowance / benefit, disability allowance.', None,
           'One Social Protection example.'),
     point('r-health', 'Building new hospital, doctors / nurses /staff wages, medicines etc.', None,
           'One Health example. First correct 4 marks, second 2.')],
    kind='questionTotal', stem=q10_stem, **A)
for c in cards[-2:]:
    show_before_reveal(c, QFIG + 'p10-q10-expenditure')


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ Irish Rail, monopoly, supermarkets
add('q11-a-i', '2-0', 'is-irish-rail-a-monopoly', ref(11, '(a)(i)'),
    O.ask(11, 'Is Irish Rail an example of a monopoly?', ' YES: NO:') + ' Justify your answer.', '4 + 5', 9,
    [point('r-yes', 'YES', 4, 'Tick YES: the scheme credits YES only, 4 marks.'),
     heading('r-justify', 'A justification',
             O.menu('Justify :', '(ii) Outline one possible economic disadvantage and one possible', [16]), 5,
             'Justify, 5 marks.')],
    stem=O.ask(11, 'The image below shows the new DART fleet', ' Adapted from'))
add('q11-a-ii', '2-0', 'disadvantage-and-advantage-of-monopoly', ref(11, '(a)(ii)'),
    O.ask(11, 'Outline one possible economic disadvantage and one possible economic advantage', ' Disadvantage:'),
    '12', 12,
    [point('r-disadvantage', paras(O.menu('2nd x 4\nDisadvantage:', 'Advantage:\nSecure employment', [16])), None,
           'One economic disadvantage.'),
     point('r-advantage', paras(O.menu('Advantage:\nSecure employment', '(b) (i) The diagram below represents', [16])),
           None, 'One economic advantage. Both are required: first correct 8 marks, second 4.')],
    kind='questionTotal', stem=O.ask(11, 'A monopoly may present possible disadvantages', ' Outline one'),
    notes='1st x 8, 2nd x 4 across the disadvantage and the advantage; no fixed side split.')
q11b_stem = O.ask(12, 'The diagram below represents the long', ' Q1 (i)')
add('q11-b-i', '2-0', 'monopoly-diagram-labels', ref(11, '(b)(i)'),
    # The labels asked about are the answer table's Label column, read off the paper.
    O.ask(12, 'Write out in full what each of the following labels represent.', ' Label Answer') + ' '
    + O.clip(12, (110, 375, 160, 478)),
    '3 x 8', 24,
    [point('r-mc', 'Marginal Cost', 8, 'MC — the yellow curve rising through E.'),
     point('r-ar', 'Average Revenue', 8, 'AR — the red downward-sloping line.'),
     point('r-mr', 'Marginal Revenue', 8, 'MR — the blue line falling more steeply than AR, through E.')],
    stem=q11b_stem)
add('q11-b-ii', '2-0', 'price-and-average-cost-on-monopoly-diagram', ref(11, '(b)(ii)'),
    O.ask(12, 'Equilibrium occurs at point E on the diagram', ' (iii)'), '4', 4,
    [point('r-diagram', O.run('P1\nAC1 C1', '(iii) A firm wishing to enter'), 4,
           'Go vertically up from Q1: where the line meets AC mark C1 and read AC1 on the price axis; '
           'where it meets AR read the price P1. The scheme gives 4 for both labels with no split.')],
    stem=q11b_stem, figure=FIG + 'p17-q11bii-price-and-cost')
pick('q11-b-iii', '2-0', 'barrier-to-entry-to-monopoly', ref(11, '(b)(iii)'),
     O.ask(12, 'A firm wishing to enter a Monopoly industry', ' Outline:'), 'A barrier to entry — any one',
     O.menu('Outline one possible barrier to entry.', '(c) The supermarket industry', [17]),
     1, 4, 'One barrier, 4 marks.')
q11c_stem = ' '.join([O.ask(13, 'The supermarket industry in Ireland', ' Recent percentage')])
add('q11-c-i', '2-0', 'largest-supermarket-shares', ref(11, '(c)(i)'),
    O.ask(13, 'Using the data in the above infographic', ' 1. 2.'), '2 x 8', 16,
    [point('r-1', 'Dunnes Stores', 8, 'Dunnes Stores, 23.9%.'),
     point('r-2', 'Tesco', 8, 'Tesco, 23.7%.')],
    stem=q11c_stem)
stance('q11-c-ii', [
    ('agree', 'agree', 'A reason to agree', O.menu('Give a reason for your answer.\nAgree:', 'Disagree: OR', [18])),
    ('disagree', 'disagree', 'A reason to disagree', O.menu('Disagree: OR\nEconomies of Scale', 'Question 12', [19])),
], '2-0', 'do-oligopolies-benefit-consumers', 11, '(c)(ii)',
    O.ask(13, 'Do you agree or disagree with this statement?', ' Agree: Disagree:') + ' Give a reason for your answer.', 6,
    stem=O.ask(13, 'An oligopoly market with a small number', ' Do you agree'))

# Q12 ─ flights, water, Revolut
q12a_stem = O.ask(14, 'Aer Lingus had a successful advertising campaign', ' Aerlingus.com')
pick('q12-a-i', '1-1', 'factors-affecting-demand-for-flights', ref(12, '(a)(i)'),
     O.ask(14, 'Outline one factor other than an advertising campaign', ' Outline:'), 'A factor — any one',
     O.menu('(i) Outline one factor other than an advertising campaign', '(ii) If Ryanair were to enter', [20]),
     1, 10, 'One factor, 10 marks. Advertising is excluded by the question.', stem=q12a_stem)
pick('q12-a-ii', '2-0', 'ryanair-entry-and-passenger-numbers', ref(12, '(a)(ii)'),
     O.ask(14, 'If Ryanair were to enter the market', ' Explain:'), 'An effect — any one',
     O.menu('(ii) If Ryanair were to enter the market', '(b) Minister James Browne', [20]),
     1, 10, 'One developed explanation, 10 marks.', stem=q12a_stem)
q12b_stem = O.ask(15, 'Government Minister James Browne announces', ' Adapted from')
pick('q12-b-i', '3-1', 'why-invest-in-water-services', ref(12, '(b)(i)'),
     O.ask(15, 'In your opinion, outline why investment in water services', ' Outline:'),
     'A reason the investment is necessary — any one',
     O.menu('(i) In your opinion, outline why investment in water services', '(ii) Investing in infrastructure like water', [21]),
     1, 7, 'One developed reason, 7 marks.', stem=q12b_stem)
pick('q12-b-ii', '3-1', 'other-economic-aims-of-government', ref(12, '(b)(ii)'),
     O.ask(15, 'Suggest two other current economic aims', ' Aim 1:'), 'An economic aim, justified — any two',
     O.menu('(ii) Investing in infrastructure like water is an economic aim', '(c) The number of people using the Revolut', [21, 22]),
     2, 10, 'Two other aims, each justified, 10 marks each. Investment in infrastructure like water '
     'is excluded by the question.',
     stem=q12b_stem + ' ' + O.ask(15, 'Investing in infrastructure like water is an economic aim', ' Suggest two'))
q12c_stem = O.ask(16, 'The number of people using the Revolut', ' Adapted from')
pick('q12-c-i', '3-4', 'why-people-use-revolut', ref(12, '(c)(i)'),
     O.ask(16, 'Discuss one reason why more people in Ireland', ' Discuss:'), 'A reason — any one',
     O.menu('(i) Discuss one reason why more people in Ireland are using the Revolut', '(ii) Name two financial institutions', [22]),
     1, 8, 'One developed reason, 8 marks.', stem=q12c_stem)
pick('q12-c-ii', '3-4', 'financial-institutions-in-ireland', ref(12, '(c)(ii)'),
     O.ask(16, 'Name two financial institutions', ' 1. 2.'), 'A financial institution — any two',
     ['AIB', 'PTSB', 'Bank of Ireland', 'Credit Union', 'An Post'],
     2, 8, 'Two institutions other than Revolut, 8 marks each. The scheme ends its list "etc.": other '
     'regulated institutions are also credited.', stem=q12c_stem)
pick('q12-c-iii', '3-4', 'why-regulate-financial-institutions', ref(12, '(c)(iii)'),
     O.ask(16, 'Outline one reason why it is important that financial institutions', ' Outline:'),
     'A reason for regulation — any one',
     O.menu('Outline one reason why it is important that financial institutions are regulated.', 'Question 13', [23]),
     1, 4, 'One reason, 4 marks.',
     stem=O.ask(16, 'All financial institutions in Ireland, including Revolut', ' Outline one'))


# Q13 ─ corporation tax, tax cuts, welfare, MNCs
q13a_stem = O.ask(17, 'The graph below shows Ireland’s corporation tax receipts', ' Ireland’s Corporation')
add('q13-a-i', '3-1', 'corporation-tax', ref(13, '(a)(i)'),
    O.ask(17, 'Explain the term corporation tax.', ' Explain:'), '6', 6,
    [point('r-meaning', 'This is a tax on the profits made by a company / corporation.', 6,
           'Explain corporation tax, 6 marks.')], stem=q13a_stem)
add('q13-a-ii', '3-1', 'trend-in-corporation-tax-receipts', ref(13, '(a)(ii)', 'trend'),
    O.ask(17, 'Comment on the overall trend', ' In your opinion'), '12', 12,
    [point('r-trend', O.run('There has been an increase in the amount of money received', 'In your opinion, is this trend'),
           12, 'State the rising trend with figures from the graph, 12 marks: €10.4bn in 2018 to '
           '€28.1bn in 2024, up €17.7bn.')],
    stem=q13a_stem,
    notes='The trend (12) and the positive/negative opinion (3) are separately priced in the scheme.')
q13aii = O.ask(17, 'In your opinion, is this trend a positive development', ' Trend:')
stance_one('q13-a-ii', [
    ('positive', 'positive development', 'Why the trend is positive — any one',
     O.menu('Positive development: ⟨3⟩', 'Negative development:', [24]), 'Ticked box: POSITIVE DEVELOPMENT.'),
    ('negative', 'negative development', 'Why the trend is negative',
     O.menu('Negative development:', '(iii) Outline one possible reason why Ireland', [25]),
     'Ticked box: NEGATIVE DEVELOPMENT.'),
], '3-1', 'is-the-corporation-tax-trend-positive', 13, '(a)(ii)', q13aii, 3, stem=q13a_stem)
pick('q13-a-iii', '3-1', 'why-corporation-tax-receipts-rose', ref(13, '(a)(iii)'),
     O.ask(17, 'Outline one possible reason why Ireland’s corporation tax receipts', ' Reason:'),
     'A reason receipts rose — any one',
     O.menu('(iii) Outline one possible reason why Ireland’s corporation tax receipts', '(b) The Irish government is expected', [25]),
     1, 6, 'One reason, 6 marks.', stem=q13a_stem)
q13b_stem = O.ask(18, 'The Irish government is expected to have a budget surplus', ' Adapted from')
stance_one('q13-b-i', [
    ('households', 'households', 'A benefit to households — any one',
     O.menu('Households:', 'Economy:', [25]), 'Ticked box: HOUSEHOLDS.'),
    ('economy', 'economy', 'A benefit to the economy — any one',
     O.menu('Economy:', '(ii) Outline one economic argument against reducing taxes.', [26]), 'Ticked box: ECONOMY.'),
], '3-1', 'benefit-of-tax-cuts', 13, '(b)(i)',
    O.ask(18, 'Discuss one benefit to either households or the economy', ' Place a tick'), 8, stem=q13b_stem)
pick('q13-b-ii', '3-1', 'argument-against-tax-cuts', ref(13, '(b)(ii)'),
     O.ask(18, 'Outline one economic argument against reducing taxes.', ' Argument'),
     'An argument against — any one',
     O.menu('(ii) Outline one economic argument against reducing taxes.', '(iii) In Budget 2026 the government increased social', [26]),
     1, 8, 'One argument, 8 marks.', stem=q13b_stem)
stance('q13-b-iii', [
    ('agree', 'agree', 'A reason to agree', O.menu('Justify your answer.\nAgree:\nHelps people cope', 'Disagree:\nOpportunity cost', [27])),
    ('disagree', 'disagree', 'A reason to disagree', O.menu('Disagree:\nOpportunity cost', '(c) Many Multi National', [27])),
], '3-1', 'ten-euro-welfare-increase', 13, '(b)(iii)',
    O.ask(18, 'Do you agree or disagree with this increase?', ' Agree Disagree'), 8,
    stem=O.ask(18, 'In Budget 2026 the government increased social welfare', ' Do you agree'))
q13c_stem = O.ask(19, 'Many Multi National Corporations', ' Adapted from')
pick('q13-c-i', '4-1', 'effect-of-lower-mnc-hiring', ref(13, '(c)(i)'),
     O.ask(19, 'Discuss one possible economic effect a reduction', ' Economic effect:'), 'An economic effect — any one',
     O.menu('(i) Discuss one possible economic effect a reduction in the hiring', '(ii) Recently some American', [27, 28]),
     1, 8, 'One developed effect, 8 marks.', stem=q13c_stem)
pick('q13-c-ii', '4-1', 'why-mncs-may-relocate-to-the-usa', ref(13, '(c)(ii)'),
     O.ask(19, 'Outline two possible reasons why these corporations', ' 1. 2.'), 'A reason to relocate — any two',
     O.menu('Outline two possible reasons why these corporations may relocate back to the USA.', 'Question 14', [28]),
     2, 8, 'Two reasons, 8 marks each.',
     stem=q13c_stem + ' ' + O.ask(19, 'Recently some American multi', ' (ii)'))

# Q14 ─ inflation, pensions, electricity
q14_stem = O.ask(20, 'The diagram below shows the changing rate of price inflation', ' Rate of price')
add('q14-a-i', '3-3', 'price-inflation', ref(14, '(a)(i)'),
    O.ask(20, 'Explain the term price inflation.', ' Explanation:'), '10', 10,
    [point('r-meaning', O.run('The steady and persistent increase in the general level of prices', '(ii) The level of inflation'),
           10, 'Explain price inflation, 10 marks.')], stem=q14_stem)
q14aii = O.ask(20, 'In your opinion does this benefit consumers in Ireland?', ' YES: NO:') + ' Explain your answer.'
stance_one('q14-a-ii', [
    ('yes', 'yes', 'Why higher inflation may benefit consumers — any one',
     O.menu('Yes:\nShrinks the', '(b) (i) On 1st January 2026', [29]), 'Ticked box: YES.'),
    ('no', 'no', 'Why higher inflation does not benefit consumers — any one',
     O.menu('No:\nReduced Purchasing Power', 'Yes:\nShrinks the', [29]), 'Ticked box: NO.'),
], '3-3', 'does-higher-inflation-benefit-consumers', 14, '(a)(ii)', q14aii, 10,
    stem=q14_stem + ' ' + O.ask(20, 'The level of price inflation in Ireland increased', ' In your opinion'))
q14b_stem = O.ask(21, 'On 1st January 2026, the Irish government introduced', ' (i)')
stance_one('q14-b-i', [
    ('employee', 'advantage to the employee', 'An advantage to the employee — any one',
     O.menu('Advantage to the employee:', 'Disadvantage to the employer:', [30]), 'Ticked box: ADVANTAGE TO THE EMPLOYEE.'),
    ('employer', 'disadvantage to the employer', 'A disadvantage to the employer — any one',
     O.menu('Disadvantage to the employer:', '(ii) The auto enrolment pension scheme', [30]),
     'Ticked box: DISADVANTAGE TO THE EMPLOYER.'),
], '1-3', 'auto-enrolment-for-employees-and-employers', 14, '(b)(i)',
    O.ask(21, 'Outline one possible economic advantage to the employee', ' Indicate which'), 12, stem=q14b_stem)
pick('q14-b-ii', '3-1', 'investing-for-an-ageing-population', ref(14, '(b)(ii)'),
     O.ask(21, 'Suggest one other area that the Irish government should invest', ' Other Area:'),
     'Another area, justified — any one',
     O.menu('Suggest one other area that the Irish government should invest in', '(iii) One possible reason why Modified', [31]),
     1, 12, 'One area with its justification, 12 marks. The pension scheme is given in the question.',
     stem=O.ask(21, 'The auto enrolment pension scheme was introduced', ' Suggest'))
pick('q14-b-iii', '3-0', 'why-modified-domestic-demand-growth-fell', ref(14, '(b)(iii)'),
     O.ask(21, 'Outline one possible reason why the growth of Modified Domestic Demand', ' Outline:'),
     'A reason growth declined — any one',
     O.menu('(iii) One possible reason why Modified Domestic Demand', '(c) The price elasticity of demand', [31]),
     1, 6, 'One reason, 6 marks.',
     stem=O.ask(21, 'The percentage change in Ireland’s Modified Domestic Demand', ' Centralbank.ie'))
q14c_stem = O.ask(22, 'The price elasticity of demand (PED) for electricity', ' (i)')
add('q14-c-i', '1-4', 'why-electricity-demand-is-inelastic', ref(14, '(c)(i)'),
    O.ask(22, 'Discuss why the demand for electricity is price inelastic.', ' Discuss:'), '5', 5,
    [point('r-why', O.run('The demand is inelastic as it less than 1 in absolute terms.', '(ii) The number of households'),
           5, 'Explain the inelastic reading (|PED| below 1) and why, 5 marks.')], stem=q14c_stem)
pick('q14-c-ii', '1-0', 'why-electricity-prices-rose', ref(14, '(c)(ii)'),
     O.ask(22, 'Outline one possible reason for this increase', ' Reason:'), 'A reason prices rose — any one',
     O.menu('Outline one possible reason for this increase in the price of electricity.', '(iii) One measure that Irish households', [32]),
     1, 8, 'One reason, 8 marks.',
     stem=' '.join([O.ask(22, 'The number of households in arrears', ' Adapted from'),
                    O.ask(22, 'The price of electricity in Ireland has increased', ' Outline one')]))
pick('q14-c-iii', '1-1', 'cutting-household-electricity-bills', ref(14, '(c)(iii)'),
     O.ask(22, 'Suggest one measure that Irish households', ' Suggestion:'), 'A household measure — any one',
     O.menu('(iii) One measure that Irish households could take', 'Question 15', [32]),
     1, 12, 'One developed measure, 12 marks.', stem=q14c_stem)


# Q15 ─ sport, Castore, the hidden economy
q15a_stem = O.ask(23, 'Through the National Sports Policy', ' Adapted from')
add('q15-a-i', '2-2', 'private-and-social-benefits-of-sport-spending', ref(15, '(a)(i)'),
    O.ask(23, 'Outline one possible private benefit and one possible social benefit', ' Private benefit:'),
    '8 + 8', 16,
    [heading('r-private', 'One private benefit', O.menu('Private benefit:', 'Social Benefit:', [33]), 8,
             'Complete BOTH. One private benefit, 8 marks.'),
     heading('r-social', 'One social benefit', O.menu('Social Benefit:', '(ii) Malcolm Byrne TD', [33]), 8,
             'One social benefit, 8 marks.')],
    stem=q15a_stem)
stance('q15-a-ii', [
    ('agree', 'agree', 'A reason to agree', O.menu('Justify your answer.\nAgree:\n32', 'Disagree:\nThe Deadweight', [33, 34])),
    ('disagree', 'disagree', 'A reason to disagree', O.menu('Disagree:\nThe Deadweight', '(b) Castore (a sports', [34])),
], '1-3', 'subsidising-gym-use', 15, '(a)(ii)',
    O.ask(23, 'Do you agree or disagree with this statement?', ' Agree Disagree'), 8,
    stem=O.ask(23, 'Malcolm Byrne TD has suggested', ' (ii)'))
q15b_stem = O.ask(24, 'Castore (a sports and athletic clothing manufacturer)', ' (i)')
pick('q15-b-i', '1-2', 'another-sportswear-manufacturer', ref(15, '(b)(i)'),
     O.ask(24, 'State one other manufacturer', ' (ii)'), 'A manufacturer — any one',
     [x.strip().rstrip('.') for x in O.run('O’Neills, Nike', '(ii) Outline one advantage to a manufacturer').split(',')],
     1, 8, 'One other manufacturer, 8 marks; Castore is excluded.', stem=q15b_stem)
pick('q15-b-ii', '1-2', 'advantage-of-a-sole-supplier-contract', ref(15, '(b)(ii)'),
     O.ask(24, 'Outline one advantage to a manufacturer', ' Advantage:'), 'An advantage — any one',
     O.menu('(ii) Outline one advantage to a manufacturer of sports and athletic clothing', 'Castore produces jerseys each week', [35]),
     1, 4, 'One advantage, 4 marks.', stem=q15b_stem)
add('q15-b-iii', '1-5', 'castore-weekly-cost-and-profit', ref(15, '(b)(iii)'),
    O.ask(24, 'Calculate the total weekly cost and the total weekly profit', ' Total Cost:'), '16', 16,
    [point('r-cost', '€35,000', None, 'Total weekly cost = €5,000 + €25,000 + €2,000 + €3,000 = €35,000.'),
     point('r-profit', '€65,000', None, 'Profit = revenue − total cost = €100,000 − €35,000 = €65,000.')],
    kind='questionTotal',
    stem=q15b_stem + ' ' + O.ask(24, 'Castore produces Ireland jerseys each week', ' (iii)'),
    figure=FIG + 'p35-q15biii-cost-and-profit',
    notes='The scheme gives 16 for both calculations with no published split.')
q15c_stem = O.ask(25, 'Castore is concerned that there might be', ' (i)')
add('q15-c-i', '3-0', 'hidden-economy-and-an-example', ref(15, '(c)(i)'),
    O.ask(25, 'Explain the term hidden economy.', ' Hidden economy:'), '7 + 4', 11,
    [anyN('r-meaning', 'What the hidden economy is', 7, 1, 7,
          [x.strip() for x in O.run('All economic activity that goes unrecorded', 'Example:').split('//')],
          'Explain the hidden economy, 7 marks. Any one of the scheme\'s explanations.'),
     anyN('r-example', 'Another hidden-economy activity', 4, 1, 4,
          [x.strip().rstrip('.') for x in O.run('Teacher giving grinds', '(ii) Outline one economic effect hidden').split(',')],
          'One other example, 4 marks.')],
    stem=q15c_stem)
add('q15-c-ii', '3-0', 'hidden-economy-effects-on-business-and-government', ref(15, '(c)(ii)'),
    O.ask(25, 'Outline one economic effect hidden economic activities', ' Businesses:'), '6 + 6', 12,
    [heading('r-business', 'One effect on businesses', O.menu('Businesses:', 'Government: ⟨6⟩', [36]), 6,
             'Complete BOTH. Effect on businesses, 6 marks.'),
     heading('r-government', 'One effect on the government', O.menu('Government: ⟨6⟩', 'Question 16', [36]), 6,
             'Effect on the government, 6 marks.')],
    stem=q15c_stem)

# Q16 ─ tariffs, enterprise, the minimum wage
q16a_stem = O.ask(26, 'Sony is increasing the price', ' Adapted from')
add('q16-a-i', '4-2', 'tariff', ref(16, '(a)(i)'), O.ask(26, 'Explain the economic term tariff.', ' Explain:'), '8', 8,
    [point('r-tariff', 'A tax on goods imported into a country.', 8, 'Explain tariff, 8 marks.')], stem=q16a_stem)
pick('q16-a-ii', '4-2', 'why-the-us-raised-tariffs', ref(16, '(a)(ii)'),
     O.ask(26, 'Outline one possible economic reason why Donald Trump', ' Outline:'), 'A reason — any one',
     O.menu('Outline one possible economic reason why Donald Trump increased tariffs in 2025.', '(iii) Outline one possible economic effect', [37]),
     1, 8, 'One reason, 8 marks.', stem=q16a_stem)
pick('q16-a-iii', '4-2', 'effect-of-us-tariffs-on-ireland', ref(16, '(a)(iii)'),
     O.ask(26, 'Outline one possible economic effect of this increase in tariffs', ' Outline:'), 'An effect on Ireland — any one',
     O.menu('(iii) Outline one possible economic effect of this increase in tariffs', '(b) Entrepreneurs take a risk', [38]),
     1, 9, 'One effect on the Irish economy, 9 marks.', stem=q16a_stem)
q16b_stem = O.ask(27, 'Entrepreneurs take a risk in organising', ' (i)')
pick('q16-b-i', '2-1', 'factors-of-production-other-than-enterprise', ref(16, '(b)(i)'),
     O.ask(27, 'Name any two factors of production other than enterprise.', ' 1. 2.'), 'A factor — any two',
     lines('(i) Name any two other factors of production other than enterprise.', '(ii) Explain one of the factors'),
     2, 3, 'Two factors, 3 marks each. Enterprise is excluded by the question.', stem=q16b_stem)
pick('q16-b-ii', '2-1', 'explaining-a-factor-of-production', ref(16, '(b)(ii)'),
     O.ask(27, 'Explain one of the factors of production you named', ' The factor'), 'An explanation — the factor you named',
     lines('(ii) Explain one of the factors of production you named above', '(iii) Suggest one measure the Irish government'),
     1, 7, 'Explain one of the factors you named in (i), 7 marks.', stem=q16b_stem)
pick('q16-b-iii', '1-3', 'encouraging-entrepreneurship', ref(16, '(b)(iii)'),
     O.ask(27, 'Suggest one measure the Irish government could take', ' Measure:'), 'A measure — any one',
     O.menu('Measure:\nProvide grants', '(c) The government increased the level', [39]),
     1, 12, 'One developed measure, 12 marks.', stem=q16b_stem)
q16c_stem = O.ask(28, 'The government increased the level of the minimum wage', ' Adapted from')
pick('q16-c-i', '2-1', 'why-a-higher-minimum-wage-matters', ref(16, '(c)(i)'),
     O.ask(28, 'Explain why increasing the minimum wage', ' Explain:'), 'A reason — any one',
     O.menu('(i) Explain why increasing the minimum wage is important', '(ii) Outline one economic argument against', [40]),
     1, 8, 'One developed reason, 8 marks.', stem=q16c_stem)
pick('q16-c-ii', '2-1', 'argument-against-a-higher-minimum-wage', ref(16, '(c)(ii)'),
     O.ask(28, 'Outline one economic argument against any further increase', ' Outline:'), 'An argument against — any one',
     O.menu('(ii) Outline one economic argument against any further increase', '(iii) Suggest one other measure that an employer', [40]),
     1, 8, 'One argument, 8 marks.', stem=q16c_stem)
pick('q16-c-iii', '2-1', 'rewarding-employee-loyalty', ref(16, '(c)(iii)'),
     O.ask(28, 'Suggest one other measure that an employer', ' Measure:'), 'A measure — any one',
     O.menu('(iii) Suggest one other measure that an employer could take', 'Ordinary Level Economics Student Research Project', [41]),
     1, 9, 'One measure other than a wage increase, 9 marks.', stem=q16c_stem)

# ── The paper's own charts, tables and diagrams, shown before reveal ──
for keys, fig in [
        (['q11-b-i', 'q11-b-ii'], 'p12-q11b-monopoly-diagram'),
        (['q11-c-i', 'q11-c-ii-agree', 'q11-c-ii-disagree'], 'p13-q11c-supermarket-shares'),
        (['q13-a-i', 'q13-a-ii', 'q13-a-ii-positive', 'q13-a-ii-negative', 'q13-a-iii'], 'p17-q13a-corporation-tax'),
        (['q14-a-i', 'q14-a-ii-yes', 'q14-a-ii-no'], 'p20-q14-cpi-inflation'),
        (['q14-b-iii'], 'p21-q14biii-modified-domestic-demand')]:
    for c in cards:
        short = c['id'].removeprefix('econ-2026-ol-')
        if short in keys:
            show_before_reveal(c, QFIG + fig, FULLQ.get(short) and QFIG + FULLQ[short])

if __name__ == '__main__':
    emit(cards)
