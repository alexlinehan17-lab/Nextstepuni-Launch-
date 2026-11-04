#!/usr/bin/env python3
"""Economics 2024 Ordinary Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2024-ol-ev.json,
made from a visual sweep of all 32 paper pages and 46 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID), and
the 61 routes are the ones the 2024 Ordinary Irish review mirrors task for task,
so the Irish attachment is unchanged.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). Ordinary Level sets its
responses as a bullet list ("• Heading: explanation"), so menus are split at the
bullets. The only prose written here is guidance: tariffs, route labels and what
a figure or a calculation shows. Scheme PDF page = printed page.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, bullets, emit, heads, point  # noqa: E402

O = Sheet(2024, 'ordinary', 'LC034GLP000EV')
D = Deck(2024, 'ordinary')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2024-OL-scheme-'
PAP = 'economics-2024-OL-paper-'


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return bullets(O.chunk(start, end, occ))


def at(start, end, firsts, occ=None):
    """Responses printed as plain sentences, split where each one begins."""
    return [as_option(o) for o in heads(O.chunk(start, end, occ), firsts)]


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, note):
    """A required answer inside a jointly priced response (1st @ n, 2nd @ m).

    One unpriced point carrying its examples: a per-option price here would
    print "n marks each" for a share the scheme never fixes.
    """
    return point(rid, paras(options), None, f'{label}. {note}')


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1st @ 8, 2nd @ 4)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


def stance(prefix, choices, topic, q, parts, qtext, per, *, stem='', figure=''):
    """A printed tick-box choice whose scheme credits each side: one card per side."""
    for suffix, word, route, label, options, concept in choices:
        pick(f'{prefix}-{suffix}', topic, concept, ref(q, parts, route),
             f'{qtext} Answer for: {word.upper()}.', label, options, 1, per,
             f'One developed explanation for the {word} choice, {per} marks. The scheme credits '
             f'both choices; these are its examples, not a closed list.',
             stem=stem, figure=figure)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ SDG 14: oceans and seas
q1_stem = O.ask(3, 'The UN Sustainable Development Goal (SDG) 14', ' Adapted from')
q1_reasons = bl('• Fisheries and employment:', '(ii) Outline one way individuals')
q1_ways = bl('• Reduce water usage.', '2. Lidl now offer')
add('sa-q1-i', '0-2', 'value-and-protection-of-marine-resources', ref(1, sa=True),
    O.ask(3, 'Explain one reason why our oceans and seas', ' Explanation:') + ' '
    + O.ask(3, 'Outline one way individuals can help protect', ' Leaving'), '12', 12,
    [shared('r-1', 'One reason oceans and seas are a valuable economic resource', q1_reasons,
            'Complete BOTH parts. The scheme prices (i) and (ii) together as one 12: the first '
            'correct answer 8 marks and the second 4, with no fixed share for either part.'),
     shared('r-2', 'One way individuals can help protect this resource', q1_ways,
            'These are the scheme’s examples, not a closed list.')],
    kind='questionTotal', stem=q1_stem, figure=PAP + 'p03-i0', **A)

# Q2 ─ Lidl Plus coupons
q2_stem = O.ask(4, 'Lidl now offer discount coupons', ' (a)')
add('sa-q2-a', '2-0', 'price-or-non-price-competition', ref(2, '(a)', sa=True),
    O.ask(4, 'Indicate using a tick (✔) in the table below', ' Price competition'), '12', 12,
    [point('r-1', 'Non-price competition ✔', None,
           'Tick NON-PRICE COMPETITION: the scheme credits no price-competition answer for this '
           'app-based offer. The completed table is shown in the figure.'),
     point('r-2', O.run('Lidl is competing with other supermarkets', 'OR'), None,
           'Explain the choice. The scheme prices the tick and the explanation together as one 12 '
           '(first correct answer 8, second 4), with no fixed share for either. Answer either (a) '
           'or (b).')],
    kind='questionTotal', stem=q2_stem, figure=SOL + 'p06-q2a-ticks', **A)
pick('sa-q2-b', '1-1', 'benefits-of-discount-coupons', ref(2, '(b)', sa=True),
     O.ask(4, 'Explain how Lidl’s customers can benefit', ' Explanation:'),
     'A way customers benefit — any one', bl('• Savings on purchases:', '7 | P a g e'),
     1, 12, 'One developed benefit, 12 marks. Answer either (a) or (b).', stem=q2_stem, **A)

# Q3 ─ monopolistic competition; competitive advertising
add('seca-q3-a-ticks', '2-0', 'monopolistic-competition-true-or-false', ref(3, '(a)', sa=True),
    O.ask(5, 'Coffee shops in Ireland operate in monopolistic competition.', ' Statement True False')
    + ' 1. ' + O.ask(5, 'Barriers to entry exist in the Irish coffee shop market.', ' The demand curve')
    + ' 2. ' + O.ask(5, 'The demand curve / average revenue curve', ' 2.') + ' '
    + O.ask(5, 'shop is downward', ' OR'), '12', 12,
    [point('r-1', 'Barriers to entry exist in the Irish coffee shop market.', None,
           'Statement 1 is FALSE: firms in monopolistic competition are free to enter and leave '
           'the market.'),
     point('r-2', 'Irish coffee shop is downward-sloping from left to right.', None,
           'Statement 2 is TRUE: each shop’s product is differentiated, so it faces a '
           'downward-sloping demand / average revenue curve. The scheme prices the two together as '
           'one 12 (first correct answer 8, second 4); the completed table is shown in the figure. '
           'Answer either (a) or (b).')],
    kind='questionTotal', figure=SOL + 'p08-q3a-ticks', **A)
add('sa-q3-b', '2-0', 'when-advertising-does-not-help-consumers', ref(3, '(b)', sa=True),
    O.ask(5, 'Outline two reasons why competitive advertising', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A reason advertising may not benefit the consumer — any two',
           bl('• Increased prices:', '8 | P a g e'), 8, 4, 'reasons')],
    stem=O.ask(5, 'Competitive advertising promotes the advantages', ' Outline two'),
    notes='Answer either (a) or (b).', **A)

# Q4 ─ household saving
q4_stem = O.ask(6, '47% of Irish families with young children', ' Adapted from')
pick('sa-q4-a', '1-1', 'why-households-are-not-saving', ref(4, '(a)', sa=True),
     O.ask(6, 'Explain one reason why these families may not be saving.', ' Explanation:'),
     'A reason a family is not saving — any one',
     bl('• Level of inflation:', 'OR\n(b) Outline one measure financial'),
     1, 12, 'One developed reason, 12 marks. Answer either (a) or (b).', stem=q4_stem, **A)
pick('sa-q4-b', '3-4', 'encouraging-households-to-save', ref(4, '(b)', sa=True),
     O.ask(6, 'Outline one measure financial institutions in Ireland', ' One measure:'),
     'A measure a financial institution could take — any one',
     bl('• Pass on the increase in interest rates to savers:', '9 | P a g e'),
     1, 12, 'One developed measure, 12 marks. Answer either (a) or (b).', stem=q4_stem, **A)

# Q5 ─ imports and exports
add('seca-q5-ticks', '4-2', 'imports-and-exports-visible-and-invisible', ref(5, sa=True),
    O.ask(6, 'Indicate by means of a tick (✔) which of the following', ' Import Export Reason')
    + ' 1. ' + O.clip(6, (83, 580, 200, 640)) + ' 2. ' + O.clip(6, (83, 650, 200, 712)),
    '2 @ 6', 12,
    [point('r-beef', 'This is a visible export.', 6,
           'Tick EXPORT: a good sold from Ireland to Germany, so money flows into Ireland. The '
           'choice and its reason, 6 marks.'),
     point('r-hotel', 'This is an invisible import.', 6,
           'Tick IMPORT: Irish residents buy a service (hotels) in France, so money flows out of '
           'Ireland. The choice and its reason, 6 marks. The completed table is shown in the '
           'figure.')],
    figure=SOL + 'p10-q5-ticks', **A)

# Q6 ─ Deposit Return Scheme
add('sa-q6', '0-2', 'effects-of-the-deposit-return-scheme', ref(6, sa=True),
    O.ask(7, 'Outline two effects this scheme may have on Irish consumers.', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'An effect on consumers — any two',
           bl('• Encourage the consumer to return these drink containers', '10 | P a g e'), 8, 4,
           'effects')],
    stem=O.ask(7, 'The Deposit Return Scheme was introduced', ' Outline two'), **A)

# Q7 ─ positive and normative statements
add('seca-q7-ticks', '0-0', 'sorting-positive-and-normative-statements', ref(7, sa=True),
    O.ask(7, 'Study the statements below and indicate', ' Statement Positive Normative')
    + ' 1. ' + O.ask(7, 'The introduction of the plastic bag levy', ' The government should')
    + ' 2. ' + O.ask(7, 'The government should increase the amount', ' Leaving'), '12', 12,
    [point('r-1', 'The introduction of the plastic bag levy has led to a decrease', None,
           'Statement 1 is POSITIVE: a claim about what happened, which data could test.'),
     point('r-2', 'The government should increase the amount of the', None,
           'Statement 2 is NORMATIVE: “should” is a value judgement. The scheme prices the two '
           'together as one 12 (first correct answer 8, second 4); the completed table is shown in '
           'the figure.')],
    kind='questionTotal', figure=SOL + 'p11-q7-ticks', **A)

# Q8 ─ Gini coefficients
add('sa-q8-i', '3-0', 'lowest-and-highest-income-inequality', ref(8, sa=True),
    O.ask(8, 'From the data given, state in the boxes below', ' (i)') + ' '
    + O.ask(8, '(i) Country with the lowest level of inequality.', ' (ii)') + ' '
    + O.ask(8, '(ii) Country with the highest level of inequality.', ' Question 9'), '12', 12,
    [point('r-1', 'Slovakia', None, '(i) Lowest inequality: Slovakia, the smallest coefficient, 0.22.'),
     point('r-2', 'USA', None,
           '(ii) Highest inequality: USA, the largest coefficient, 0.38. The scheme prices the two '
           'together as one 12: the first correct answer 8 and the second 4.')],
    kind='questionTotal', stem=O.ask(8, 'The Gini Coefficient measures inequality', ' Gini Coefficients 2019'),
    figure=PAP + 'p08-art', **A)

# Q9 ─ GDP and GNI
add('sa-q9', '3-0', 'gdp-and-gni', ref(9, sa=True),
    O.ask(8, 'Complete the following table to show what each of the abbreviations', ' G'), '12', 12,
    [point('r-gdp-gross', 'Gross', None, 'G___ in the first row: Gross (Gross Domestic Product).'),
     point('r-gdp-product', 'Product', None, 'P___ in the first row: Product; Domestic is printed.'),
     point('r-gni-gross', 'Gross', None, 'G___ in the second row: Gross (Gross National Income).'),
     point('r-gni-national', 'National', None,
           'N___ in the second row: National; Income is printed. The scheme pays the first two '
           'correct fields 4 each and the next two 2 each, with no fixed field for each price.')],
    kind='questionTotal',
    stem=O.ask(8, 'The following data shows two different estimates', ' Adapted from Economic'),
    figure=PAP + 'p08-i3', **A)

# Q10 ─ matcha tea
add('sa-q10', '1-0', 'which-diagram-shows-the-new-matcha-equilibrium', ref(10, sa=True),
    O.ask(9, 'Assume the market for matcha tea is in equilibrium', ' Diagram A Diagram B') + ' '
    + O.ask(9, 'Explain your answer including the effects', ' Explanation:'), '8 + 4', 12,
    [point('r-1', 'Diagram A ✔', 8,
           'Tick DIAGRAM A, 8 marks: favourable media coverage changes tastes, so DEMAND shifts '
           'right to D2. Diagram B moves supply.'),
     point('r-2', O.run('• The demand curve shifts to the right (D2).', '12 | P a g e'), 4,
           'Explain, 4 marks: demand shifts right, the shortage at the old price drives the price '
           'up, and the new equilibrium price and quantity are both higher.')],
    stem=O.ask(9, 'Matcha tea can help improve memory', ' Adapted from'), figure=PAP + 'p09-i0', **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ electricity prices; oligopoly; energy market
q11a_stem = O.ask(10, 'The chart below shows increases in electricity prices', ' Electricity Price')
add('q11-a-i', '3-3', 'highest-and-lowest-electricity-price-increases', ref(11, '(a)(i)'),
    O.ask(10, 'Which company had the highest price increase?', ' (ii)'), '12', 12,
    [point('r-1', 'Flogas', None, 'Highest: Flogas, the tallest bar.'),
     point('r-2', 'Electric Ireland', None,
           'Lowest: Electric Ireland, the shortest bar. The scheme prices the two together as one '
           '12: the first correct answer 8 and the second 4. The chart compares percentage '
           'increases, not price levels.')],
    kind='questionTotal', stem=q11a_stem, figure=PAP + 'p10-art')
pick('q11-a-ii', '1-5', 'effect-of-energy-costs-on-business', ref(11, '(a)(ii)'),
     O.ask(10, 'Outline one possible economic effect of these price increases', ' One effect:'),
     'An economic effect on businesses — any one',
     bl('• Increased costs for business due to higher prices:', '13 | P a g e'),
     1, 5, 'One developed effect, 5 marks.', stem=q11a_stem, figure=PAP + 'p10-art')
pick('q11-a-iii', '1-3', 'electricity-credit-rationale', ref(11, '(a)(iii)'),
     O.ask(10, 'During winter 2023', ' Reason:'),
     'A reason the government granted the credit — any one',
     bl('• To alleviate the financial burden', '14 | P a g e'),
     1, 5, 'One developed reason, 5 marks. These are the scheme’s examples, not a closed list.')
q11b_stem = O.ask(11, 'The diagram below represents the long', ' Price')
c = add('q11-b-i', '2-0', 'labelling-an-oligopoly-diagram-ol', ref(11, '(b)(i)'),
        O.ask(11, 'Write out in full what each of the following three labels', ' D=AR MC MR'), '3 x 8', 24,
        [point('r-1', 'Demand/Average Revenue', 8, 'D=AR in full, 8 marks.'),
         point('r-2', 'Marginal Cost', 8, 'MC in full, 8 marks.'),
         point('r-3', 'Marginal Revenue', 8, 'MR in full, 8 marks. All three labels are asked.')],
        stem=q11b_stem, figure=PAP + 'p11-art')
c['labelKey'] = [{'letter': 'D=AR', 'meaning': 'Demand/Average Revenue', 'askedInThisQuestion': True},
                 {'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
                 {'letter': 'MR', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': True},
                 {'letter': 'E', 'meaning': 'the equilibrium, where marginal cost cuts marginal revenue',
                  'askedInThisQuestion': False}]
add('q11-b-ii', '2-0', 'reading-output-and-price-off-a-kinked-demand-curve', ref(11, '(b)(ii)'),
    O.ask(11, 'Equilibrium occurs at point E on the diagram above.', ' The electricity market'), '3', 3,
    [point('r-1', 'Q1', None, 'Q1: drop a line from E to the quantity axis.'),
     point('r-2', 'P1', None,
           'P1: from Q1 go up to the demand / average revenue curve (the kink), then across to the '
           'price axis; the price is read off the demand curve, not off E. The scheme gives 3 for '
           'both labels, with no published split; the official diagram is shown in the figure.')],
    kind='questionTotal', stem=q11b_stem, figure=SOL + 'p15-q11b-diagram')
add('q11-b-iii', '2-0', 'oligopoly-in-ireland', ref(11, '(b)(iii)'),
    O.ask(11, 'Give one other example of an oligopoly market', ' Example:'), '4', 4,
    [point('r-example', O.run('Mobile phones / Broadband / Insurance', '• Only a few providers'), None,
           'Name one OTHER oligopoly market; the scheme accepts these.'),
     point('r-reason', paras(bl('• Only a few providers dominate the market:', '15 | P a g e')), None,
           'Explain a reason for the choice: an oligopoly feature of that market. The scheme gives '
           'one 4 for the example and the reason together, with no published split.')],
    kind='questionTotal', stem=O.ask(11, 'The electricity market is an example of an oligopoly', ' (iii)'))
q11c_stem = O.ask(12, 'Panda Power left the Irish energy market.', ' (i)')
pick('q11-c-i', '2-0', 'fewer-firms-and-competition', ref(11, '(c)(i)'),
     O.ask(12, 'In your opinion, is the Irish energy market more competitive', ' More Competitive'),
     'An explanation of the less competitive market — any one',
     bl('• Reduced number of firms:', '16 | P a g e'),
     1, 6, 'Tick LESS COMPETITIVE: the scheme credits no more-competitive answer. One developed '
     'explanation, 6 marks for the choice and its explanation together.', stem=q11c_stem)
pick('q12-c-ii', '0-2', 'sustainable-household-behaviour', ref(11, '(c)(ii)'),
     O.ask(12, 'Outline two ways citizens in Ireland can behave more sustainably', ' 1. 2.'),
     'A way to behave more sustainably — any two',
     bl('• Use energy-efficient appliances:', '17 | P a g e'),
     2, 8, 'Two ways, 8 marks each.')

# Q12 ─ employment; scarcity of labour; unemployment
q12_stem = O.ask(13, 'In 2022, the number of people employed in Ireland', ' Adapted from')
add('q12-a-i', '3-2', 'percentage-increase-in-people-in-employment', ref(12, '(a)(i)'),
    O.ask(13, 'From the data given on the left', ' Workings:'), '6 @ 3', 18,
    [point('r-answer', 'Percentage increase: 2.73%', 18,
           'Employment rose from 2,506,000 (Q4 2021) to 2,574,500 (Q4 2022): 2,574,500 − 2,506,000 '
           '= 68,500. Percentage increase = 68,500 ÷ 2,506,000 × 100 = 2.73%. Divide by the EARLIER '
           'figure. The scheme marks the working 6 @ 3; deduct 1 if % is omitted.')],
    stem=q12_stem, figure=PAP + 'p13-i0')
pick('q12-a-ii', '3-2', 'benefits-of-increased-employment', ref(12, '(a)(ii)'),
     O.ask(13, 'Outline one possible economic benefit of increased employment', ' Benefit:'),
     'A benefit of increased employment — any one',
     bl('• Increased standard of living for citizens:', '18 | P a g e'),
     1, 7, 'One developed benefit, 7 marks.', stem=q12_stem)
q12b1_stem = O.ask(14, 'Currently there is a shortage of skilled employees', ' Explain the economic term')
pick('q12-b-i', '0-1', 'scarcity-of-labour', ref(12, '(b)(i)'),
     O.ask(14, 'Explain the economic term scarcity', ' Scarcity:'),
     'Scarcity applied to labour — either wording',
     at('When applied to labour, scarcity refers to the situation where the number',
        '(ii) The pharmaceutical industry has experienced',
        ['When applied to labour, scarcity refers to the situation where the number',
         'When applied to labour, scarcity refers to the situation where there are firms']),
     1, 4, 'Explain the term, 4 marks: the scheme gives two wordings of the same idea, demand for '
     'workers exceeding the supply of them.', stem=q12b1_stem)
pick('q12-b-ii', '2-1', 'effects-of-a-skills-shortage-on-a-sector', ref(12, '(b)(ii)'),
     O.ask(14, 'Explain one effect a shortage of labour', ' Explanation:'),
     'An effect on the industry — any one',
     bl('• Increased wages / Increase cost of labour:', '19 | P a g e'),
     1, 10, 'One developed effect, 10 marks.',
     stem=O.ask(14, 'The pharmaceutical industry has experienced', ' Explain one effect'))
pick('q12-b-iii', '2-1', 'increasing-the-supply-of-skilled-labour', ref(12, '(b)(iii)'),
     O.ask(14, 'Outline one economic measure the Irish government could take to help increase',
           ' Economic measure:'),
     'A measure to increase the supply of skilled labour — any one',
     bl('• Increase funding for education and training:', '20 | P a g e'),
     1, 10, 'One developed measure, 10 marks.')
q12c_stem = O.ask(15, 'The chart below shows the monthly seasonally adjusted', ' Seasonally')
add('q12-c-i', '3-2', 'overall-trend-in-irish-unemployment', ref(12, '(c)(i)'),
    O.ask(15, 'Identify the overall trend in Irish unemployment', ' Trend:'), '6', 6,
    [point('r-trend', O.run('Based on the above data, the rate of unemployment',
                            '(ii) With labour costs increasing'), 6,
           'Identify the trend with figures, 6 marks: broadly stable, from 4.3% in July 2022 to '
           '4.4% in January 2023, peaking at 4.5% in October and November. The rise is 0.1 '
           'percentage point; the scheme writes “0.1%” and “in 2022”, though the chart runs to '
           'January 2023.')],
    stem=q12c_stem, figure=PAP + 'p15-i0')
pick('q12-c-ii-unemployment', '3-2', 'labour-costs-and-unemployment', ref(12, '(c)(ii)'),
     O.ask(15, 'Outline how this development may effect unemployment', ' Effect:'),
     'An effect on unemployment — either one',
     bl('• Could lead to increased unemployment', '(iii) Outline one reason why some people'),
     1, 10, 'One developed effect, 10 marks. Both responses the scheme lists point the same way: '
     'unemployment rises.',
     stem=O.ask(15, 'With labour costs increasing some Irish businesses', ' (ii)'))
pick('q12-c-iii', '3-2', 'unemployment-alongside-vacancies', ref(12, '(c)(iii)'),
     O.ask(15, 'Outline one reason why some people remain unemployed', ' Reason:'),
     'A reason people remain unemployed while vacancies exist — any one',
     bl('• Mismatch between the skills and qualifications', '21 | P a g e'),
     1, 10, 'One developed reason, 10 marks: skills mismatch, visa or language barriers, '
     'transport, housing or the loss of benefits.')

# Q13 ─ costs; food prices; cost-push inflation
q13a_fig, q13a_q = SOL + 'p22-q13ai-diagram', PAP + 'p16-q13ai-question'
add('q13-a-i', '1-5', 'plotting-fixed-and-variable-costs-against-output', ref(13, '(a)(i)'),
    O.ask(16, 'You have been given the data below for a firm.', ' Quantity (units'), '2 @ 2 + 3 + 5', 12,
    [point('r-axes', 'Axes:', 4,
           'Complete and label both axes: Costs (€) and Quantity (units of output), 2 marks each.'),
     point('r-fc', 'FC @ 3', 3, 'Draw and label the fixed costs: a horizontal line at €600, 3 marks.'),
     point('r-vc', 'VC @ 5', 5,
           'Draw and label the variable costs: €500, €600, €700 and €800 at outputs 1 to 4, a '
           'rising line, 5 marks. The two lines cross at output 2, where both are €600. The '
           'official graph is shown in the figure.')],
    figure=q13a_fig)
add('q13-a-ii', '1-5', 'fixed-and-variable-costs', ref(13, '(a)(ii)'),
    O.ask(16, 'Explain the difference between fixed costs and variable costs.', ' Explanation Example'),
    '2 @ 8', 16,
    [point('r-fixed', 'Fixed Costs: Costs which do not change as output changes / Costs which have '
           'to be paid even if nothing is produced.', 8,
           'Explain fixed costs and give an example, such as rent or loan repayments, 8 marks.',
           accepts=['Rent', 'Loan repayments']),
     point('r-variable', 'Variable Costs: Costs which do change as output changes.', 8,
           'Explain variable costs and give an example, such as electricity, labour or raw '
           'materials, 8 marks.', accepts=['Electricity', 'Labour', 'Raw materials'])])
q13b_stem = O.ask(17, 'The chart below shows the annual percentage change in food price', ' Annual Food')
add('q13-b-i', '3-3', 'highest-and-lowest-food-price-inflation', ref(13, '(b)(i)'),
    O.ask(17, 'Which country had the lowest food price inflation?', ' (ii)'), '13', 13,
    [point('r-1', 'Switzerland', None, 'Lowest: Switzerland, the shortest bar.'),
     point('r-2', 'Turkey', None,
           'Highest: Turkey, the longest bar. The scheme prices the two together as one 13: the '
           'first correct answer 8 and the second 5.')],
    kind='questionTotal', stem=q13b_stem, figure=PAP + 'p17-art')
pick('q13-b-ii', '3-3', 'effects-of-food-price-inflation', ref(13, '(b)(ii)'),
     O.ask(17, 'Explain one possible economic effect food price inflation', ' Economic effect:'),
     'An effect on consumers — any one',
     bl('• Reduced purchasing power / standard of living', '23 | P a g e'),
     1, 10, 'One developed effect, 10 marks.', stem=q13b_stem, figure=PAP + 'p17-art')
q13c_stem = O.ask(18, 'Toilet paper prices rose by 15.6% in 2022.', ' Adapted from')
add('q13-c-i', '3-3', 'cost-push-inflation', ref(13, '(c)(i)'),
    O.ask(18, 'Explain what is meant by the economic term, cost', ' Cost'), '10', 10,
    [point('r-1', O.run('This occurs when the source of upward pressure on prices',
                        '(ii) In your opinion, should manufacturers'), 10,
           'Explain the term, 10 marks: rising costs of production, not matched by productivity, '
           'passed on as higher prices; imported inflation is one form of it.')],
    stem=q13c_stem)
stance('q13-c-ii', [
    ('yes', 'yes', 'yes', 'A reason to say yes — any one',
     bl('• It helps protect the environment:', '24 | P a g e'), 'the-case-for-sustainable-materials'),
    ('no', 'no', 'no', 'A reason to say no — any one',
     bl('• Increases production costs:', '25 | P a g e'), 'the-case-against-sustainable-materials')],
    '0-2', 13, '(c)(ii)', O.ask(18, 'In your opinion, should manufacturers', ' Yes No'), 10,
    stem=q13c_stem)
pick('q13-c-iii', '3-3', 'why-the-ecb-fears-inflation', ref(13, '(c)(iii)'),
     O.ask(18, 'Explain why you think the ECB is concerned', ' Explanation:'),
     'A reason the ECB is concerned — any one',
     bl('• The ECB has a price stability mandate:', '26 | P a g e'),
     1, 4, 'One developed reason, 4 marks. The scheme’s price-stability example quotes the older '
     '“close to, but below, 2%” definition; since July 2021 the ECB’s target is a symmetric 2% '
     'inflation rate over the medium term.',
     stem=O.ask(18, 'The European Central Bank (ECB) is concerned', ' Explain why'))

# Q14 ─ government spending; VAT; trade
q14_stem = O.ask(19, 'The chart below shows estimated levels of spending', ' Estimated')
q14a_ask = O.ask(19, 'Using the figures in the chart above answer the following questions.', ' Question Workings')
add('q14-a-i', '3-1', 'total-government-spending', ref(14, '(a)(i)', 'total'),
    q14a_ask + ' ' + O.ask(19, 'Calculate how much the government planned', ' Using your answer'),
    '5 @ 1 + 7', 12,
    [point('r-total', '€44.22 billion', 12,
           'Total = €23.4bn + €9.63bn + €3.91bn + €3.98bn + €3.30bn = €44.22 billion. Five figures '
           'at 1 mark each and the answer 7. Deduct 1 for omission of € and 1 for omission of bn.')],
    stem=q14_stem, figure=PAP + 'p19-i0')
add('q14-a-i-education', '3-1', 'education-share-of-government-spending', ref(14, '(a)(i)', 'education share'),
    q14a_ask + ' ' + O.ask(19, 'Using your answer from (i) above calculate', ' (ii)'), '3 @ 1 + 5', 8,
    [point('r-share', '21.78%', 8,
           'Education share = 9.63 ÷ 44.22 × 100 = 21.78%, using the €44.22bn total from the first '
           'calculation. Three working entries at 1 mark and the answer 5. Deduct 1 if % is omitted.')],
    stem=q14_stem, figure=PAP + 'p19-i0')
pick('q14-a-ii-eu', '4-1', 'why-ireland-pays-into-the-eu-budget', ref(14, '(a)(ii)'),
     O.ask(19, 'Outline one reason why the Irish government contributes', ' One reason:'),
     'A reason Ireland contributes — any one',
     bl('• To help achieve economic growth and cohesion:',
        '(iii) Outline what is meant by the economic term, national debt'),
     1, 4, 'One developed reason, 4 marks.',
     stem=O.ask(19, 'Ireland is estimated to contribute €2 billion', ' Outline one reason'))
add('q14-a-iii', '3-1', 'national-debt', ref(14, '(a)(iii)'),
    O.ask(19, 'Outline what is meant by the economic term national debt', ' National debt:'), '4', 4,
    [point('r-1', O.run('The total / cumulative amount of government borrowing', 'According to the NTMA'), 4,
           'Explain the term, 4 marks: the total government borrowing outstanding. The scheme adds '
           'that Ireland’s gross national debt stood at €235.9bn at the end of April 2023.')])
q14b_stem = O.ask(20, 'The standard rate of Value Added Tax', ' (i)')
pick('q14-b-i', '3-1', 'why-some-goods-are-zero-rated', ref(14, '(b)(i)'),
     O.ask(20, 'Outline one reason why the government applies a 0% VAT rate', ' One reason:'),
     'A reason for the 0% rate — any one',
     bl('• To support basic needs:', '(ii) Indicate with a tick'),
     1, 7, 'One developed reason, 7 marks.', stem=q14b_stem)
add('q14-b-ii', '3-1', 'why-vat-is-an-indirect-tax', ref(14, '(b)(ii)'),
    O.ask(20, 'Indicate with a tick (✔) below whether VAT', ' Direct tax'), '7', 7,
    [point('r-1', 'Indirect tax ✔', None,
           'Tick INDIRECT TAX: the scheme credits no direct-tax answer.'),
     point('r-2', O.run('VAT is a tax on spending / on goods and services.', '29 | P a g e'), None,
           'Explain the choice. The scheme gives one 7 for the tick and the explanation together, '
           'with no published split.')],
    kind='questionTotal', stem=q14b_stem)
stance('q14-b-iii', [
    ('agree', 'agree', 'agree', 'A reason to agree — any one',
     bl('• Some tax revenue is lost to the exchequer:', 'DISAGREE Explanation:'),
     'the-case-for-restoring-the-vat-rate'),
    ('disagree', 'disagree', 'disagree', 'A reason to disagree — any one',
     bl('• It boosts tourism:', '(c) The table below shows Ireland’s trade'),
     'the-case-against-restoring-the-vat-rate')],
    '3-1', 14, '(b)(iii)',
    O.ask(20, 'Do you agree with the tourism and hospitality industry', ' Please tick') + ' '
    + O.ask(20, 'Explain your answer.', ' Explanation:'), 7,
    stem=O.ask(20, 'In February 2023, the government announced', ' Do you agree'))
add('q14-c-i', '4-2', 'balance-of-trade-surplus-or-deficit', ref(14, '(c)(i)'),
    O.ask(21, 'Using the information in the table above, calculate', ' Workings:'), '4 @ 3 + 4', 16,
    [point('r-1', O.run('Balance of trade: Total exports – Total imports', '( -1m for omission'), 12,
           'Balance of trade = total exports − total imports = €165.7bn − €103.7bn = €62bn. The '
           'working is 4 @ 3; deduct 1 for omission of € or bn.'),
     point('r-2', 'The Balance of Trade is a surplus because the exports are greater than the imports.', 4,
           'Tick SURPLUS and explain, 4 marks: exports exceed imports.')],
    stem=O.ask(21, 'The table below shows Ireland’s trade in goods in 2021.', ' Exports Imports'),
    figure=PAP + 'p21-i0')
add('q14-a-ii', '4-2', 'importance-of-exports', ref(14, '(c)(ii)'),
    O.ask(21, 'Outline two reasons why exports are important', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A reason exports matter — any two',
           bl('• Exports can help create employment:', '32 | P a g e'), 6, 4, 'reasons')])

# Q15 ─ factors of production; fertiliser; elasticity
q15a_fig, q15a_q = SOL + 'p33-q15a-table', PAP + 'p22-q15a-question'
add('q15-a', '0-1', 'naming-and-explaining-the-factors-on-a-farm', ref(15, '(a)'),
    O.ask(22, 'The table below concerns factors of production', ' Example Name'), '20', 20,
    [point('r-machinery', 'Capital', None, 'Farm Machinery: name the factor, Capital.'),
     point('r-workers', 'Labour', None, 'Farm Workers: name the factor, Labour.'),
     point('r-owners', 'Enterprise', None, 'Farm Owners: name the factor, Enterprise.'),
     point('r-owners-explanation', 'The one taking a risk in setting up the farm in return for profit.',
           None, 'Farm Owners: explain Enterprise, the risk-taker who sets up the farm for profit.'),
     point('r-land-explanation', 'Anything supplied by nature which helps in producing the output from '
           'the farm.', None,
           'Farm Land: explain Land, anything supplied by nature (the scheme also accepts “The '
           'ground on which the farm is located / is built.”). The scheme prices the five blanks '
           'as 3 @ 5 and 1 @ 3, 1 @ 2 (20) without naming which cell earns which; the completed '
           'table is shown in the figure.')],
    kind='questionTotal', figure=q15a_fig)
q15b_stem = (O.ask(23, 'The diagram below shows the demand and supply curve', ' Price') + ' '
             + O.ask(23, 'The price of fertiliser in Ireland increased', ' Adapted from'))
q15b_fig = SOL + 'p34-q15b-diagram'
q15b1_ask = O.ask(23, 'As a result, the increase in fertiliser prices', ' (ii)')
add('q15-b-i', '1-0', 'showing-a-supply-shift-after-a-cost-rise', ref(15, '(b)(i)'),
    q15b1_ask, '3 @ 5', 15,
    [point('r-1', 'S2 Price S1 E2 Pe2 E1 Pe1 D Qe2 Qe1 Quantity', 15,
           'Shift supply LEFT from S1 to S2: dearer fertiliser means less is supplied at every '
           'price. Mark the new equilibrium E2, the higher price Pe2 and the lower quantity Qe2. '
           'The scheme gives 3 @ 5 for the diagram without naming the three; the official diagram '
           'is shown in the figure.')],
    stem=q15b_stem, figure=q15b_fig)
add('q15-b-ii', '1-0', 'explaining-the-fertiliser-supply-shift', ref(15, '(b)(ii)'),
    O.ask(23, 'Explain your answer.', ' Explanation:'), '9', 9,
    [point('r-1', O.run('• As the cost of fertiliser has risen', '(iii) Almond milk'), 9,
           'Explain the chain, 9 marks: dearer fertiliser, less used, lower yields, so supply shifts '
           'left from S1 to S2, giving a higher equilibrium price (Pe2) and a lower equilibrium '
           'quantity (Qe2).')],
    stem=q15b_stem + ' ' + q15b1_ask, figure=q15b_fig)
pick('q15-b-iii', '1-1', 'substitute-goods', ref(15, '(b)(iii)'),
     O.ask(23, 'Explain the meaning of the economic term substitute good.', ' Explain:'),
     'What a substitute good is — any wording',
     at('Almond milk can be classed as a substitute good for cow’s milk because', '(c) (i) Using the formula',
        ['Almond milk can be classed as a substitute good for cow’s milk because',
         'A good that satisfies the same need', 'A good that can be consumed / used',
         'Goods that can be used as alternatives']),
     1, 6, 'Explain the term, 6 marks; the scheme accepts any of these wordings.',
     stem=O.ask(23, 'Almond milk can be classed as a substitute good for cow’s milk.', ' Explain the meaning'))
q15c_fig, q15c_q = SOL + 'p35-q15ci-working', PAP + 'p24-q15ci-question'
add('q15-c-i', '1-4', 'price-elasticity-of-demand-for-chocolate', ref(15, '(c)(i)'),
    O.ask(24, 'Using the formula supplied, calculate', ' Show all your workings.', include_end=True),
    '10 @ 2', 20,
    [point('r-answer', 'Answer: -1.71', 20,
           'PED = (ΔQ ÷ ΔP) × ((P1 + P2) ÷ (Q1 + Q2)) = (−40÷40) × (240÷140) = −1.714…, so −1.71. The '
           'scheme marks the working 10 @ 2 and deducts 2 if the minus sign is omitted; the official '
           'working is shown in the figure.')],
    figure=q15c_fig)
add('q15-c-ii', '1-4', 'reading-a-ped-figure', ref(15, '(c)(ii)'),
    O.ask(24, 'Indicate if the demand for a bar of chocolate', ' Answer:'), '5', 5,
    [point('r-answer', 'Answer: Price elastic demand', None, 'Price ELASTIC: the PED of −1.71 is greater '
           'than 1 in absolute value.'),
     point('r-explanation', O.run('The answer is greater than 1 in absolute terms.', '35 | P a g e'), None,
           'Explain: the percentage change in quantity demanded is greater than the percentage change '
           'in price. Here the price RISES from 100 to 140 cent and the quantity falls; the scheme’s '
           'last line describes a 1% price fall. The scheme gives one 5 for the answer and the '
           'explanation together.')],
    kind='questionTotal', figure=PAP + 'p24-i0')

# Q16 ─ population; corporation tax; mortgage rules
pick('q16-a-i', '3-5', 'why-world-population-grew', ref(16, '(a)(i)'),
     O.ask(25, 'Outline one reason why you think global population', ' One reason:'),
     'A reason population grew — any one',
     bl('• The birth rate exceeds the death rate:', '36 | P a g e'),
     1, 9, 'One developed reason, 9 marks. International migration moves people between countries '
     'and cannot itself increase the WORLD total; reasons through births, deaths or longevity '
     'answer the question.',
     stem=O.ask(25, 'According to the United Nations, the global population', ' Global Population'),
     figure=PAP + 'p25-i1')
pick('q16-a-ii', '2-1', 'older-workers-returning-to-work', ref(16, '(a)(ii)'),
     O.ask(25, 'Outline one effect on the Irish economy if more people aged 65', ' Effect:'),
     'An effect of the unretired — any one',
     bl('• Employment levels may rise / Increase in tax revenues:', '37 | P a g e'),
     1, 9, 'One developed effect, 9 marks. The scheme’s dependency-ratio example counts '
     'non-working-age people; more over-65s working changes the share who are economically '
     'dependent, not the AGE-BASED dependency ratio itself.',
     stem=O.ask(25, 'In several countries many people over 65', ' Adapted from'))
pick('q16-a-iii', '3-1', 'ageing-and-the-irish-exchequer', ref(16, '(a)(iii)'),
     O.ask(25, 'Outline one economic effect the above development', ' Economic effect:'),
     'An effect on the government — any one',
     bl('• Increased costs of pensions:', '38 | P a g e'),
     1, 9, 'One developed effect, 9 marks.',
     stem=O.ask(25, 'Ireland’s population is ageing faster', ' Outline one economic'))
q16b_stem = O.ask(26, 'Corporation tax amounted to €22.6bn', ' Adapted from')
pick('q16-b-i', '3-1', 'the-risk-in-corporation-tax', ref(16, '(b)(i)'),
     O.ask(26, 'Corporation tax is now the second largest source', ' Economic risk:'),
     'A risk of this development — any one',
     bl('• The risk of CPT being a transitory source', '(ii) Irelands corporation tax rate'),
     1, 10, 'One developed risk, 10 marks.', stem=q16b_stem)
q16b2_disadvantages = bl('• Possibility that some MNCs might relocate:', '(c) The information below details')
add('q16-b-ii-adv', '3-1', 'advantages-and-disadvantages-of-global-corporation-tax-deal', ref(16, '(b)(ii)'),
    O.ask(26, 'Outline one possible economic advantage and one', ' Economic advantage:'), '9 + 9', 18,
    [heading('r-advantage', 'Economic advantage',
             bl('• Raise more revenue for the government:', 'Economic disadvantage:'), 9,
             'Complete BOTH headings. One economic advantage, 9 marks. The global minimum rate '
             'applies to large groups (annual turnover of at least €750m), not to every Irish '
             'business.'),
     heading('r-disadvantage', 'Economic disadvantage', q16b2_disadvantages, 9,
             'One economic disadvantage, 9 marks.')],
    stem=O.ask(26, 'Irelands corporation tax rate set to rise', ' Adapted from the Irish Times'))
q16c_stem = O.ask(27, 'The information below details new rules', ' 2022')
stance('q16-c-i', [
    ('pos', 'positive', 'positive', 'A positive effect — any one',
     bl('• Homes will become more affordable:', 'Negative effect explanation:'),
     'looser-mortgage-rules-positive'),
    ('neg', 'negative', 'negative', 'A negative effect — any one',
     bl('• Risk of overborrowing and household debt:', '41 | P a g e'),
     'looser-mortgage-rules-negative')],
    '3-4', 16, '(c)(i)', O.ask(27, 'Indicate with a tick (✔) below whether you think', ' Positive:'), 10,
    stem=q16c_stem, figure=PAP + 'p27-i0')
pick('q16-c-ii', '3-4', 'a-new-entrant-to-the-mortgage-market', ref(16, '(c)(ii)'),
     O.ask(27, 'Outline one possible economic effect Revolut', ' Economic effect:'),
     'An economic effect on mortgage applicants — any one',
     bl('• Increase in competition:', '42 | P a g e'),
     1, 10, 'One developed effect, 10 marks.',
     stem=O.ask(27, 'Fintech company, Revolut, now has over two million', ' Adapted from'))

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('q11-b-ii', 'p11-q11bii-question'), ('q13-a-i', 'p16-q13ai-question'),
                 ('q15-a', 'p22-q15a-question'), ('q15-b-i', 'p23-q15b-question'),
                 ('q15-b-ii', 'p23-q15b-question'), ('q15-c-i', 'p24-q15ci-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split three jointly priced answers into one card per
# part. Each half is still emitted, lifted from its own part, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('sa-q1-ii', 'sa-q1-i', 'One way individuals can help', q1_ways, 4),
    ('sa-q8-ii', 'sa-q8-i', 'Country with the highest level of inequality', ['USA'], 4),
    ('q16-b-ii-dis', 'q16-b-ii-adv', 'Economic disadvantage', q16b2_disadvantages, 9),
]
for old, canonical, label, options, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this part is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
