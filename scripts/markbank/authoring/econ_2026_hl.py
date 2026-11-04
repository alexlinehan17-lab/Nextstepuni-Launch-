#!/usr/bin/env python3
"""Economics 2026 Higher Level, Sections A and B.

Authored from the independent census in drafts/economics-2026-hl-ev.json,
made from a visual sweep of all 40 paper pages and 88 scheme pages before any
2026 card existed. Question wording and stems are sliced from the question
paper; every marking point is sliced from the scheme (econ_2026_lib.py). The
only prose written here is guidance: tariffs, route labels and what a figure
or a calculation shows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, block, emit, point, tidy  # noqa: E402

H = Sheet(2026, 'higher', 'LC034ALP000EV')
D = Deck(2026, 'higher')
cards, add, pick, heading, ref, stance = D.cards, D.add, D.pick, D.heading, D.ref, D.stance


# ═════════════════════════════════ SECTION A ══════════════════════════════════
A = dict(section='A')

def q1b_menu():
    """Q1(b): six characteristics, each a heading line over its two periods.

    The headings carry no dash, so the bold-heading split would open each
    option at "Early 1950s"; slice the column rendering line by line instead,
    one option per heading with its Early 1950s and Present day lines.
    """
    raw = block(H.full_md, 'Types of goods and services exported\nEarly 1950s', 'ompare one main ec', 1)
    groups = []
    for line in [l.strip() for l in raw.split('\n') if l.strip()]:
        if line.startswith(('Early 1950s', 'Present day')):
            groups[-1].append(line)
        else:
            groups.append([line])
    assert len(groups) == 6 and all(len(g) == 3 for g in groups), groups
    return [tidy(' '.join(g)) for g in groups]


# Q1 ─ specialisation; Irish trade then and now
q1_stem = H.ask(3, '9th March 2026', '(a)')
pick('sa-q1-a', '0-1', 'benefits-of-specialisation-for-a-firm', ref(1, '(a)', sa=True),
     H.ask(3, 'Smith discussed', ' 1. 2.'),
     'A benefit for the firm — any two',
     H.menu('Outline two possible benefits for a firm which specialises its labour.',
            '(b) Compare one main economic characteristic', [5]),
     2, 3, 'Two benefits, 3 marks each.', stem=q1_stem, **A)


pick('sa-q1-b', '4-2', 'irish-trade-1950s-and-today', ref(1, '(b)', sa=True),
     H.ask(3, 'Compare one main economic characteristic', ' In the early 1950s:'),
     'One characteristic compared across both periods',
     q1b_menu(),
     1, 6, 'One characteristic, compared for the early 1950s AND the present day, 6 marks. The '
     'scheme gives one 6 for the comparison and does not split it between the two periods. '
     'These six headings are its examples, not a closed list.', stem=q1_stem, **A)

# Q2 ─ music spending; Spotify
q2_stem = ' '.join([H.ask(4, 'The graphic below shows excerpts', ' €172'),
                    H.clip(4, (145, 150, 298, 205)), H.clip(4, (298, 150, 452, 205))])
q2a = H.ask(4, 'The data above shows consumers spend', ' Spending on music streaming Spending')
pick('sa-q2-a-events', '1-4', 'price-elasticity-of-music-spending', ref(2, '(a)', 'music events', sa=True),
     q2a + ' Justify the choice: SPENDING ON MUSIC EVENTS.', 'Why music events are more price elastic',
     H.menu('Spending on music events ✓', 'If candidate states spending on streaming', [7]),
     1, 6, 'One developed justification, 6 marks. The scheme ticks music events; these are its '
     'examples, not a closed list.', stem=q2_stem, **A)
pick('sa-q2-a-streaming', '1-4', 'price-elasticity-of-music-spending', ref(2, '(a)', 'music streaming', sa=True),
     q2a + ' Justify the choice: SPENDING ON MUSIC STREAMING.', 'Why streaming is more price elastic',
     H.menu('If candidate states spending on streaming is more price elastic:',
            'Answer either (b) or (c)', [7]),
     1, 6, 'One developed justification, 6 marks. The scheme also credits this choice, with these '
     'two examples.', stem=q2_stem, **A)
pick('sa-q2-b', '1-5', 'objectives-other-than-profit-maximisation', ref(2, '(b)', sa=True),
     H.ask(4, 'Outline two reasons why streaming companies', ' 1. 2.'),
     'A reason for another objective — any two',
     H.menu('(b) Outline two reasons why streaming companies, like Spotify, may pursue objectives',
            '(c) Outline one reason why large online streaming', [8]),
     2, 3, 'Two reasons, 3 marks each. Answer either (b) or (c).',
     stem=H.ask(4, 'In 2024, streaming platform, Spotify', ' Adapted from'), **A)
pick('sa-q2-c', '1-5', 'near-zero-marginal-cost-of-streaming', ref(2, '(c)', sa=True),
     H.ask(4, 'Outline one reason why large online streaming', ' Reason:'),
     'A reason marginal cost is near zero',
     H.menu('(c) Outline one reason why large online streaming', '3 The graphic below shows', [8]),
     1, 6, 'One developed reason, 6 marks. Answer either (b) or (c).', **A)

# Q3 ─ All-Ireland travel costs; market failure; rural transport
q3_stem = ' '.join([H.ask(5, 'The graphic below shows the average cost', ' Cork Tipperary'),
                    H.ask(5, 'Due to rising costs', ' Do you agree')])
stance('sa-q3-a', [
    ('agree', 'agree', 'A reason to subsidise public transport',
     H.menu('AGREE – Reasons in favour of subsidising public transport:',
            'DISAGREE – Reasons against subsidising', [9])),
    ('disagree', 'disagree', 'A reason not to subsidise public transport',
     H.menu('DISAGREE – Reasons against subsidising public transport:',
            '(b) Irish Rail has imposed', [10])),
], '1-3', 'subsidising-public-transport-to-finals', 3, '(a)',
    H.ask(5, 'Do you agree or disagree with this proposal?', ' Agree Disagree'), 6, sa=True,
    stem=q3_stem, section='A')
pick('sa-q3-b', '2-2', 'noise-on-trains-as-market-failure', ref(3, '(b)', sa=True),
     H.ask(5, 'Outline one reason why this passenger behaviour', ' Reason:'),
     'A reason this is market failure',
     H.menu('Outline one reason why this passenger behaviour is an example of market failure.',
            'Outline two ways the Connecting Ireland Rural Mobility Plan', [11]),
     1, 6, 'One developed reason, 6 marks. Answer either (b) or (c).',
     stem=H.ask(5, 'Irish Rail has imposed', ' Outline one reason'), **A)
pick('sa-q3-c', '0-2', 'rural-transport-and-inequality', ref(3, '(c)', sa=True),
     H.ask(6, 'Outline two ways the Connecting Ireland', ' 1. 2.'),
     'A way the plan reduces inequality — any two',
     H.menu('Outline two ways the Connecting Ireland Rural Mobility Plan can help reduce inequality',
            '4 The chart below shows that workers in Bangladesh', [12]),
     2, 3, 'Two ways, 3 marks each. Answer either (b) or (c).',
     stem=H.ask(6, 'The Connecting Ireland Rural Mobility Plan is', ' Adapted from'), **A)

# Q4 ─ garment wages; second-hand clothing
q4_stem = H.ask(6, 'The chart below shows that workers in Bangladesh', ' Retail Price')
pick('sa-q4-a', '2-1', 'why-ldc-wages-are-lower', ref(4, '(a)', sa=True),
     H.ask(6, 'Outline one reason why workers in less developed', ' Reason:'),
     'A reason LDC wages are lower',
     H.menu('Outline one reason why workers in less developed countries (LDCs) tend to earn lower',
            '(b) Suggest two possible measures', [13]),
     1, 6, 'One developed reason, 6 marks.', stem=q4_stem, **A)
pick('sa-q4-b', '1-3', 'raising-demand-for-second-hand-clothing', ref(4, '(b)', sa=True),
     H.ask(7, 'Suggest two possible measures', ' 1. 2.'),
     'A government measure — any two',
     H.menu('(b) Suggest two possible measures the Irish government',
            '(c) Outline two ways the use of online second-hand', [14]),
     2, 3, 'Two measures, 3 marks each. Answer either (b) or (c).',
     stem=H.ask(7, 'The global market for used clothes', ' Adapted from'), **A)
pick('sa-q4-c', '1-1', 'benefits-of-second-hand-clothing-apps', ref(4, '(c)', sa=True),
     H.ask(7, 'Outline two ways the use of online second-hand', ' 1. 2.'),
     'A benefit for consumers — any two',
     H.menu('(c) Outline two ways the use of online second-hand clothing apps',
            '5 Some financial companies, such as Klarna', [15]),
     2, 3, 'Two benefits, 3 marks each. Answer either (b) or (c).', **A)

# Q5 ─ buy now, pay later; consumer assumptions
q5_stem = H.ask(8, 'Some financial companies, such as Klarna', ' BUY NOW, PAY LATER')
stance('sa-q5-a', [
    ('rational', 'rational consumer behaviour', 'A reason BNPL supports rational choices',
     H.menu('Answer: Rational behaviour', 'Answer: Irrational behaviour', [16])),
    ('irrational', 'irrational consumer behaviour', 'A reason BNPL encourages irrational choices',
     H.menu('Answer: Irrational behaviour', '(b) Rational consumer behaviour is one assumption', [16])),
], '1-1', 'bnpl-and-rational-behaviour', 5, '(a)',
    H.ask(8, 'Do you think BNPL companies', ' Rational consumer behaviour Irrational'), 6, sa=True,
    stem=q5_stem, section='A')
pick('sa-q5-b', '1-1', 'assumptions-of-consumer-behaviour', ref(5, '(b)', sa=True),
     H.ask(8, 'Outline two other key assumptions', ' 1. 2.'),
     'Another assumption — any two',
     H.menu('Outline two other key assumptions about consumer behaviour used in economics.',
            '6 China\'s first Legoland', [17]),
     2, 3, 'Two other assumptions, 3 marks each. Rational behaviour is given in the question.',
     stem=H.ask(8, 'Rational consumer behaviour is one assumption', ' Outline two'), **A)


# Q6 ─ theme parks and globalisation
q6_stem = H.ask(9, "China's first Legoland", ' Adapted from')
glob = H.run('Explain the term globalisation.\nGlobalisation is', 'Outline one economic benefit to a company of investing')
glob = glob[glob.index('Globalisation is'):]
defs = ['Globalisation is' + x for x in glob.split('Globalisation is')[1:]]
defs = [d.strip() for d in defs]
add('sa-q6-a', '4-1', 'globalisation-and-investing-in-theme-parks', ref(6, '(a)', sa=True),
    H.ask(9, 'Explain the term globalisation.', ' Explain:'), '3 + 3', 6,
    [anyN('r-globalisation', 'What globalisation means', 3, 1, 3, defs,
          'Explain globalisation, 3 marks. Any one of the scheme\'s explanations.'),
     heading('r-benefit', 'A benefit to the company',
             H.menu('Outline one economic benefit to a company of investing in theme parks.',
                    '(b) Outline two economic benefits of the operation of theme parks', [18]),
             3, 'One benefit to the company, 3 marks.')],
    stem=' '.join([q6_stem, H.ask(9, 'Theme parks, such as Disney', ' Explain the term')]), **A)
pick('sa-q6-b', '3-5', 'benefits-of-theme-parks-to-a-country', ref(6, '(b)', sa=True),
     H.ask(9, 'Outline two economic benefits of the operation', ' 1. 2.'),
     'A benefit to the country — any two',
     H.menu('(b) Outline two economic benefits of the operation of theme parks within a country.',
            '7 (a) In your opinion, which of the following fiscal policy tools', [19]),
     2, 3, 'Two benefits, 3 marks each.',
     stem=H.ask(9, 'Ireland’s main theme park', ' Outline two'), **A)

# Q7 ─ plastic packaging; the environmental Kuznets curve
q7_stem = H.ask(10, 'Ireland generates more plastic packaging', ' Adapted from')
stance('sa-q7-a', [
    ('subsidy', 'subsidy for firms', 'A justification for the subsidy',
     H.menu('Answer: Subsidy for firms', 'Answer: Tax on firms', [20])),
    ('tax', 'tax on firms', 'A justification for the tax',
     H.menu('Answer: Tax on firms', '(b) The diagram below shows the Environmental', [20, 21])),
], '1-3', 'subsidy-or-tax-on-packaging', 7, '(a)',
    H.ask(10, 'In your opinion, which of the following fiscal policy tools', ' Subsidy for firms Tax on firms'),
    6, sa=True, stem=q7_stem, section='A')
stance('sa-q7-b', [
    ('yes', 'yes (relevant)', 'Why the curve is relevant',
     H.menu('Answer: Yes (relevant)', 'Answer: No (not relevant)', [21])),
    ('no', 'no (not relevant)', 'Why the curve is not relevant',
     H.menu('Answer: No (not relevant)', '8 (a) Farming may be seen', [22])),
], '0-2', 'relevance-of-the-environmental-kuznets-curve', 7, '(b)',
    H.ask(10, 'In your opinion, is the above curve relevant', ' Yes (relevant) No'), 6, sa=True,
    stem=H.ask(10, 'The diagram below shows the Environmental', ' Damage to the'), section='A')

# Q8 ─ farming as a career; farm input costs
q8_stem = H.ask(11, 'One-third of farmers', ' Adapted from')
pick('sa-q8-a', '2-1', 'why-young-people-avoid-farming', ref(8, '(a)', sa=True),
     H.ask(11, 'Outline two factors which may discourage', ' 1. 2.'),
     'A discouraging factor — any two',
     H.menu('Outline two factors which may discourage younger people from becoming farmers.',
            '(b) Cattle input costs have surged', [23]),
     2, 3, 'Two factors, 3 marks each.',
     stem=' '.join([q8_stem, H.ask(11, 'Farming may be seen', ' Outline two')]), **A)
pick('sa-q8-b', '1-0', 'farm-input-costs-and-local-business', ref(8, '(b)', sa=True),
     H.ask(11, 'Outline two ways in which this development', ' 1. 2.'),
     'An effect on other local businesses — any two',
     H.menu('Outline two ways in which this development may affect other businesses in the local',
            '9 The charts below show', [24]),
     2, 3, 'Two ways, 3 marks each.',
     stem=H.ask(11, 'Cattle input costs have surged', ' Adapted from'), **A)


# Q9 ─ EU and US GDP
q9_stem = H.ask(12, 'The charts below shows the total', ' 2008 2024')
add('sa-q9-a', '3-5', 'us-gdp-growth-and-comment', ref(9, '(a)', sa=True),
    H.ask(12, 'The increase in GDP for the EU between 2008', ' Workings:'), '6', 6,
    [point('r-change', H.run('Change = $29.2', 'Percentage change ='), None,
           'Find the change in US GDP first.'),
     point('r-percentage', 'Percentage change = $14.4 trillion/$14.8 trillion x 100 = 97.3 %', None,
           'Percentage change = change ÷ the 2008 value × 100. Answer: 97.3%.'),
     point('r-comment', H.run('• The USA experienced a much greater percentage increase', '(b) The data in the charts above'),
           None, 'Comment on the difference in growth between the two regions.')],
    kind='questionTotal', stem=q9_stem,
    notes='The scheme gives 6 for the calculation and the comment together, with no published split.', **A)
add_pick_q9b = pick('sa-q9-b', '3-5', 'eu-concerns-from-slower-growth', ref(9, '(b)', sa=True),
     H.ask(12, 'The data in the charts above create', ' 1. 2.'),
     'A concern for EU governments — any two',
     H.menu('What in your opinion are two economic concerns presented by the above data for EU',
            '10 The diagram compares the prices', [26]),
     2, 3, 'Two concerns, 3 marks each.', stem=q9_stem, **A)

# Q10 ─ price levels
q10_stem = ' '.join([H.ask(13, 'The diagram below compares the prices', ' Euro Area'),
                     H.ask(13, 'The chart above shows that the average price', ' (a)')])
pick('sa-q10-a', '3-3', 'effects-of-higher-prices', ref(10, '(a)', sa=True),
     H.ask(13, 'Outline two economic effects of higher prices', ' 1. 2.'),
     'An effect of higher prices — any two',
     H.menu('(a) Outline two economic effects of higher prices on the Irish economy.',
            '(b) Outline two ways in which rising food prices', [27]),
     2, 3, 'Two effects, 3 marks each.', stem=q10_stem, **A)
pick('sa-q10-b', '3-3', 'unequal-effects-of-food-price-rises', ref(10, '(b)', sa=True),
     H.ask(13, 'Outline two ways in which rising food prices', ' 1. 2.'),
     'A way consumers are affected unequally — any two',
     H.menu('(b) Outline two ways in which rising food prices do not affect all consumers equally.',
            'SECTION B', [28]),
     2, 3, 'Two ways, 3 marks each.', stem=q10_stem, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════
FIG = 'economics-2026-HL-scheme-'


def lines(start, end, occ=None):
    """The scheme's one-per-line list between two anchors (no bold headings)."""
    raw = H.chunk(start, end, occ)
    return [x.strip() for x in raw.split('\n')[1:] if x.strip() and '| P a g e' not in x]


def paras(options):
    return '\n\n'.join(options)


# Q11 ─ sport, gyms, YED and PED
q11_stem = H.ask(14, 'The chart below shows the percentage of people', ' Sports Participation')
pick('q11-a-i', '1-3', 'raising-sport-participation-over-45', ref(11, '(a)(i)'),
     H.ask(14, 'Suggest one measure which local authorities', ' Measure:'),
     'A measure for local authorities',
     H.menu('(i) Suggest one measure which local authorities in Ireland could take',
            '(ii) Outline two ways in which increasing participation', [29]),
     1, 6, 'One developed measure, 6 marks.', stem=q11_stem)
pick('q11-a-ii', '2-2', 'social-benefits-of-sport-participation', ref(11, '(a)(ii)'),
     H.ask(14, 'Outline two ways in which increasing participation', ' 1. 2.'),
     'A benefit to society — any two',
     H.menu('(ii) Outline two ways in which increasing participation in sports',
            '(b) There are approximately 1,100 gyms', [30]),
     2, 6, 'Two ways, 6 marks each.', stem=q11_stem)
q11b_stem = H.ask(15, 'There are approximately 1,100 gyms', ' Adapted from')
mc_fig = FIG + 'p31-q11bi-short-run-equilibrium'
add('q11-b-i', '2-0', 'draw-monopolistic-competition-short-run', ref(11, '(b)(i)', 'diagram'),
    H.ask(15, 'Explain, with the aid of a clearly labelled diagram', ' Explain:') + ' Draw the diagram.', '12', 12,
    [point('r-diagram', H.run('P Q MR AR MC AC E Q1 P1 C1 SNPs', 'Explanation:'), 12,
           'Label both axes (Price / Costs; Quantity) and the MC, AC, AR = D and MR curves. '
           'Mark equilibrium E where MC = MR (MC rising), output Q1, price P1 on AR at P, average '
           'cost C1 on AC at C, and shade the supernormal profit (SNPs) between P1 and C1; W marks '
           'minimum AC. The scheme lists these eleven labels for the 12-mark diagram without a '
           'per-label split.')],
    stem=q11b_stem, figure=mc_fig,
    notes='The diagram (12) and the written explanation (9) are separately priced in the scheme.')
add('q11-b-i-explanation', '2-0', 'explain-monopolistic-competition-short-run',
    ref(11, '(b)(i)', 'explanation'),
    H.ask(15, 'Explain, with the aid of a clearly labelled diagram', ' Explain:') + ' Write the explanation.', '9', 9,
    [point('r-explanation', H.run('• Equilibrium occurs at point E', '(ii) Some gyms in Ireland'), 9,
           'Explain all six features of the short-run equilibrium; the scheme gives 9 for the '
           'explanation with no separately priced steps.')],
    stem=q11b_stem, figure=mc_fig)
add('q11-b-ii', '2-0', 'oligopoly-versus-monopolistic-competition-for-members', ref(11, '(b)(ii)'),
    H.ask(16, 'Outline how conditions for gym members', ' Choice of gyms:'), '4 + 4', 8,
    [heading('r-choice', 'Choice of gyms',
             H.menu('Choice of gyms:', 'Cost of gym membership:', [32]), 4,
             'Complete BOTH headings. Choice of gyms, 4 marks.'),
     heading('r-cost', 'Cost of gym membership',
             H.menu('Cost of gym membership:', '(c) (i) When Cian', [32]), 4,
             'Cost of gym membership, 4 marks.')],
    stem=H.ask(16, 'Some gyms in Ireland operate under', ' Outline how'))
q11c_stem = H.ask(16, 'When Cian’s weekly income is €400', ' Assuming Cian')
yed_fig = FIG + 'p33-q11ci-yed-working'
add('q11-c-i', '1-4', 'calculate-income-elasticity', ref(11, '(c)(i)', 'calculation'),
    H.ask(16, 'Assuming Cian pays per gym visit', ' and explain your answer.') + '.', '7', 7,
    [point('r-answer', 'Answer: +1.8', 7,
           'Midpoint YED = (ΔQ ÷ ΔY) × ((Y1 + Y2) ÷ (Q1 + Q2)) = (+1 ÷ +100) × (900 ÷ 5) = +1.8. '
           'The official working is shown in the figure.')],
    stem=q11c_stem, figure=yed_fig,
    notes='The workings (7) and the explanation (5) are separately priced in the scheme.')
add('q11-c-i-meaning', '1-4', 'interpret-income-elasticity', ref(11, '(c)(i)', 'explanation'),
    H.ask(16, 'Assuming Cian pays per gym visit', ' Workings:') + ' Write the explanation.', '5', 5,
    [point('r-meaning', H.run('The sign is plus therefore the good is a normal good.', '(ii) Recently, some politicians'), 5,
           'Explain both the sign (normal good) and the size (income elastic, a luxury); 5 marks '
           'for the explanation.')],
    stem=q11c_stem)
stance('q11-c-ii', [
    ('agree', 'agree', 'A reason for tax relief on gym memberships',
     H.menu('AGREE (Gym memberships should receive tax relief)', 'DISAGREE (Gym memberships', [34])),
    ('disagree', 'disagree', 'A reason against tax relief on gym memberships',
     H.menu('DISAGREE (Gym memberships should not receive tax relief)', '(iii) A knowledge of price', [35])),
], '1-3', 'tax-relief-for-gym-memberships', 11, '(c)(ii)',
    H.ask(17, 'Do you agree or disagree, that gym memberships', ' Agree Disagree'), 6,
    stem=H.ask(17, 'Recently, some politicians proposed', ' Do you agree'))
add('q11-c-iii', '1-4', 'ped-and-maximising-gym-revenue', ref(11, '(c)(iii)'),
    H.ask(17, 'Explain the term price elasticity of demand and discuss', ' Explain:'), '10', 10,
    [point('r-ped', H.run('Price elasticity of demand refers to', 'Discuss measure:'), None,
           'Explain price elasticity of demand.'),
     point('r-measure', paras(H.menu('Discuss measure:', 'Question 12', [36], drop=('Discuss measure',))), None,
           'Discuss ONE measure that uses PED to maximise revenue. These are the scheme\'s '
           'examples, not a closed list.')],
    kind='questionTotal', stem=H.ask(17, 'A knowledge of price elasticity of demand', ' (iii)'),
    notes='The scheme gives one 10 for the explanation and the measure together, with no published split.')

# Q12 ─ trade, tariffs, oil, ESB Networks
q12a_stem = H.ask(18, 'The chart below shows the value of Ireland', ' Value of Ireland')
q12ai = H.ask(18, 'Outline the overall trend in the value', ' Indicate which overall trend')
for suffix, word, start, end in [
        ('imports', 'total goods imports', 'Trend – Total goods imports:', 'Trend – Total goods exports'),
        ('exports', 'total goods exports', 'Trend – Total goods exports', '(ii) In your opinion, do the changes')]:
    add(f'q12-a-i-{suffix}', '4-2', 'trend-in-irish-goods-trade', ref(12, '(a)(i)', word),
        f'{q12ai} Ticked box: {word.upper()}.', '4', 4,
        [point('r-trend', H.run(start, end).split(':', 1)[-1].strip() if suffix == 'imports'
               else H.run(start, end)[len('Trend – Total goods exports'):].strip(), 4,
               'State the overall trend with figures from the chart, 4 marks.')],
        stem=q12a_stem)
stance('q12-a-ii', [
    ('benefit', 'economic benefit', 'A benefit of these trade changes',
     H.menu('Economic benefit:', 'Economic challenge:', [37, 38], occ=0)),
    ('challenge', 'economic challenge', 'A challenge from these trade changes',
     H.menu('Economic challenge:', '(iii) The European Commission has warned', [38], occ=0)),
], '4-2', 'benefits-or-challenges-of-trade-changes', 12, '(a)(ii)',
    H.ask(18, 'In your opinion, do the changes', ' Economic benefit Economic challenge'), 8,
    stem=q12a_stem)
add('q12-a-iii', '4-2', 'dumping', ref(12, '(a)(iii)'),
    H.ask(19, 'Explain what you understand by the economic term dumping', ' Dumping:'), '6', 6,
    [point('r-dumping', H.run('Dumping refers to an exporting firm', '(b) A trade agreement'), 6,
           'Explain dumping, 6 marks.')],
    stem=H.ask(19, 'The European Commission has warned China', ' Adapted from'))
q12b_stem = H.ask(19, 'A trade agreement between the European Union', ' (i) Explain')
add('q12-b-i', '4-2', 'tariff', ref(12, '(b)(i)'),
    H.ask(19, 'Explain what you understand by the economic term tariff.', ' Explain:'), '6', 6,
    [point('r-tariff', H.run('A tariff refers to a tax', '(ii) Outline two economic implications'), 6,
           'Explain tariff, 6 marks.')], stem=q12b_stem)
pick('q12-b-ii', '4-2', 'us-tariff-implications-for-irish-exporters', ref(12, '(b)(ii)'),
     H.ask(19, 'Outline two economic implications that Irish exporters', ' 1. 2.'),
     'An implication for Irish exporters — any two',
     H.menu('(ii) Outline two economic implications that Irish exporters may face',
            '(iii) Outline one economic benefit and one economic challenge for a country', [39, 40]),
     2, 6, 'Two implications, 6 marks each.', stem=q12b_stem)
add('q12-b-iii', '4-2', 'benefit-and-challenge-of-protectionism', ref(12, '(b)(iii)'),
    H.ask(19, 'Outline one economic benefit and one economic challenge for a country', ' Economic benefit:'),
    '6 + 6', 12,
    [heading('r-benefit', 'One economic benefit',
             H.menu('engages in trade protectionism.', 'One economic challenge:', [40]), 6,
             'Complete BOTH headings. One economic benefit, 6 marks.'),
     heading('r-challenge', 'One economic challenge',
             H.menu('One economic challenge:', '(c) The graphic below shows the eight leading', [41]), 6,
             'One economic challenge, 6 marks.')])
q12c_stem = H.ask(20, 'The graphic below shows the eight leading', ' Adapted from')
oil_fig = FIG + 'p42-q12ci-oil-share-working'
add('q12-c-i', '2-0', 'concentration-of-world-oil-output', ref(12, '(c)(i)', 'calculation'),
    H.ask(20, 'Using the data above, calculate the combined', ' Outline how this'), '7', 7,
    [point('r-total', H.run('22.7m (US) + 10.7m', '• Total world production'), None,
           'Add the outputs of the top three producers.'),
     point('r-answer', 'Answer: 42.7 %', None,
           '43.9 ÷ 102.8 × 100 = 42.7%. The official working is shown in the figure.')],
    kind='questionTotal', stem=q12c_stem, figure=oil_fig,
    notes='The workings are priced at 7 as a whole; the influence on prices is separately priced at 4.')
pick('q12-c-i-influence', '2-0', 'oil-concentration-and-prices', ref(12, '(c)(i)', 'influence on prices'),
     H.ask(20, 'Outline how this concentration of production', ' Workings:'),
     'An influence on global oil prices',
     H.menu('Influence on global oil prices', '(ii) According to the Energy Institute', [42]),
     1, 4, 'One developed influence, 4 marks.', stem=q12c_stem)
stance('q12-c-ii', [
    ('option-a', 'option A', 'A justification for a larger carbon tax increase',
     H.menu('Option A (larger annual increase in the carbon tax)', 'OR\nOption B (subsidies for renewable', [43])),
    ('option-b', 'option B', 'A justification for renewable-energy subsidies',
     H.menu('Option B (subsidies for renewable energy alternatives)', '(iii) The Irish Government plans to end', [44])),
], '1-3', 'carbon-tax-or-renewable-subsidies', 12, '(c)(ii)',
    H.ask(20, 'In your opinion, which government intervention option', ' Option A Option B'), 6,
    stem=H.ask(20, 'According to the Energy Institute', ' In your opinion'))
add('q12-c-iii', '2-0', 'ending-the-esb-networks-monopoly', ref(12, '(c)(iii)'),
    H.ask(21, 'Outline how this change may affect each', ' Employment levels in the electricity sector:'),
    '5 + 5', 10,
    [heading('r-employment', 'Employment levels in the electricity sector',
             H.menu('Employment levels in the electricity sector:',
                    'Electricity prices for large businesses in the Irish economy:', [45]), 5,
             'Complete BOTH headings. Employment, 5 marks.'),
     heading('r-prices', 'Electricity prices for large businesses',
             H.menu('Electricity prices for large businesses in the Irish economy:', 'Question 13', [46]), 5,
             'Electricity prices for large businesses, 5 marks.')],
    stem=H.ask(21, 'The Irish Government plans to end ESB', ' Adapted from'))


# Q13 ─ ECB, credit, a surf school's costs, housing
q13_stem = H.ask(22, 'The chart below shows changes in the European Central Bank', ' Adapted from')
pick('q13-a-i', '3-3', 'why-the-ecb-cut-rates', ref(13, '(a)(i)'),
     H.ask(22, 'Outline one economic factor which may have influenced', ' Outline:'),
     'A factor behind the rate cuts',
     H.menu('(i) Outline one economic factor which may have influenced the ECB',
            '(ii) 60,770 personal loans', [47]),
     1, 6, 'One developed factor, 6 marks.', stem=q13_stem)
pick('q13-a-ii', '3-4', 'demand-for-credit', ref(13, '(a)(ii)'),
     H.ask(22, 'Outline two factors, other than interest rates', ' 1. 2.'),
     'A factor increasing demand for credit — any two',
     H.menu('Outline two factors, other than interest rates, which may increase the demand for',
            '(b) Surfriders', [48]),
     2, 6, 'Two factors, 6 marks each. Interest rates are excluded by the question.',
     stem=H.ask(22, '60,770 personal loans worth', ' Adapted from'))
q13b_stem = H.ask(23, 'Surfriders, a surf school in Bundoran', ' Daily Output')
add('q13-b-i', '1-5', 'fixed-and-variable-costs-with-examples', ref(13, '(b)(i)'),
    H.ask(23, 'Explain the terms fixed costs and variable costs', ' Fixed costs:'), '6 + 6', 12,
    [point('r-fixed', H.run('Fixed costs refer to costs of production', 'Variable costs:'), 6,
           'Explain fixed costs AND give one surf-school example, 6 marks. The scheme does not split '
           'the 6 between the meaning and the example; the listed examples are not a closed list.'),
     point('r-variable', H.run('Variable costs are costs of production that change', '(ii) Using data from the table above'), 6,
           'Explain variable costs AND give one surf-school example, 6 marks, unsplit as above.')],
    stem=q13b_stem)
add('q13-b-ii', '1-5', 'draw-total-cost-curves', ref(13, '(b)(ii)'),
    H.ask(23, 'Using data from the table above draw', ' Costs (€) 900'), '16', 16,
    [point('r-diagram', H.run('TC\n600 TVC', '(iii) When the surf school provides'), 16,
           'Scale and label both axes (Costs (€) and Quantity, 0–40 lessons). Plot TFC as a '
           'horizontal line at €300; TVC through €0, €120, €210, €360 and €600; TC = TFC + TVC '
           'through €300, €420, €510, €660 and €900. Label all three curves. The scheme gives 16 '
           'for the complete diagram with no published split.')],
    stem=q13b_stem, figure=FIG + 'p50-q13bii-cost-curves')
add('q13-b-iii', '1-5', 'minimum-price-for-a-target-profit', ref(13, '(b)(iii)'),
    H.ask(24, 'When the surf school provides 40 lessons per day', ' Workings:'), '4', 4,
    [point('r-working', H.run('At 40 lessons per day total costs (TC) = €900', 'Answer: €25'), None,
           'Total revenue must cover total cost plus the target profit.'),
     point('r-answer', 'Answer: €25 (minimum price charged per lesson)', None,
           'TR = €900 + €100 = €1,000; P = €1,000 ÷ 40 = €25.')],
    kind='questionTotal', stem=q13b_stem,
    notes='The scheme gives 4 for the working and answer together.')
q13c_stem = H.ask(24, 'The government’s new housing plan', ' (i) Discuss')
add('q13-c-i', '0-1', 'benefit-and-challenge-of-town-centre-renewal', ref(13, '(c)(i)'),
    H.ask(24, 'Discuss one economic benefit and one economic challenge of revitalising', ' Benefit:'),
    '5 + 5', 10,
    [heading('r-benefit', 'One economic benefit',
             H.menu('Discuss one economic benefit and one economic challenge of revitalising town',
                    'One Economic challenge:', [51]), 5,
             'Complete BOTH headings. One economic benefit, 5 marks.'),
     heading('r-challenge', 'One economic challenge',
             H.menu('One Economic challenge:', '(ii) Outline two possible implications of Ireland', [52]), 5,
             'One economic challenge, 5 marks.')],
    stem=q13c_stem)
pick('q13-c-ii', '2-1', 'eu-membership-and-construction-labour', ref(13, '(c)(ii)'),
     H.ask(24, 'Outline two possible implications of Ireland’s EU membership', ' 1. 2.'),
     'An implication of EU membership — any two',
     H.menu('(ii) Outline two possible implications of Ireland’s EU membership',
            '(iii) Do you agree or disagree with local authorities', [53]),
     2, 5, 'Two implications, 5 marks each.', stem=q13c_stem)
stance('q13-c-iii', [
    ('agree', 'agree', 'A reason to allow compulsory purchase',
     H.menu('Do you agree or disagree with local authorities being allowed to compulsorily buy',
            'Disagree: OR', [54])),
    ('disagree', 'disagree', 'A reason against compulsory purchase',
     H.menu('Disagree: OR\nOpportunity cost of public funds', 'Question 14', [55])),
], '1-3', 'compulsory-purchase-of-derelict-property', 13, '(c)(iii)',
    H.ask(25, 'Do you agree or disagree with local authorities', ' Agree Disagree'), 5,
    stem=H.ask(25, 'The Irish Government’s new Housing Plan', ' Adapted from'))

# Q14 ─ national income, circular flow, arrears, PS5 equilibrium
add('q14-a-i', '3-0', 'net-factor-income-from-abroad', ref(14, '(a)(i)'),
    H.ask(26, 'Calculate Ireland’s net factor income from abroad', ' Workings:'), '6', 6,
    [point('r-formula', 'NFIA = GNP – GDP', None, 'State the relationship.'),
     point('r-answer', H.run('NFIA = €107.0bn', '(ii) Outline two limitations'), None,
           '€107.0bn − €153.4bn = −€46.4bn: negative, because more factor income leaves Ireland than enters it.')],
    kind='questionTotal', stem=H.ask(26, 'Ireland’s GDP was €153.4 billion', ' Calculate'),
    notes='The scheme gives 6 for the relationship and the answer together.')
pick('q14-a-ii', '3-0', 'limitations-of-gdp-for-welfare', ref(14, '(a)(ii)'),
     H.ask(26, 'Outline two limitations of gross domestic product', ' 1. 2.'),
     'A limitation of GDP — any two',
     H.menu('(ii) Outline two limitations of gross domestic product (GDP) as a measure',
            '(iii) National income accounts do not record', [56, 57]),
     2, 5, 'Two limitations, 5 marks each.')
add('q14-a-iii', '3-0', 'economic-and-social-impacts-of-the-hidden-economy', ref(14, '(a)(iii)'),
    H.ask(26, 'Outline one economic impact and one social impact', ' Economic impact:'), '5 + 5', 10,
    [heading('r-economic', 'One economic impact',
             H.menu('One economic impact:', 'One social impact:', [58]), 5,
             'Complete BOTH headings. One economic impact, 5 marks.'),
     heading('r-social', 'One social impact',
             H.menu('One social impact:', '(b) The diagram below shows the circular flow', [59]), 5,
             'One social impact, 5 marks.')],
    stem=H.ask(26, 'National income accounts do not record', ' Outline one'))
q14b_stem = H.ask(27, 'The diagram below shows the circular flow', ' 44')
add('q14-b-i', '3-0', 'complete-the-open-economy-circular-flow', ref(14, '(b)(i)'),
    H.ask(27, 'Complete the diagram above by inserting', ' 1 2 3 4'), '8', 8,
    [point(f'r-{n}', x, None, f'Component {n}.')
     for n, x in enumerate(lines('components numbered 1 to 4 in the table below.',
                                 '(ii) Explain the term imports'), 1)],
    kind='questionTotal', stem=q14b_stem,
    notes='The scheme gives 8 for the four components with no per-component split.')
add('q14-b-ii', '4-2', 'imports-and-what-influences-them', ref(14, '(b)(ii)'),
    H.ask(27, 'Explain the term imports in the circular flow', ' Imports:'), '4 + 2 @ 4', 12,
    [point('r-imports', H.run('Imports refer to goods and services produced abroad', 'Two factors which currently'), 4,
           'Explain imports in the circular flow, 4 marks.'),
     anyN('r-factors', 'A factor influencing imports — any two', 8, 2, 4,
          H.menu('Two factors which currently influence the level of imports in the Irish economy:',
                 '(iii) 301,000 households', [60, 61]),
          'Two factors, 4 marks each.')],
    stem=q14b_stem)
stance('q14-b-iii', [
    ('agree', 'agree', 'A reason for the government to clear the arrears',
     H.menu('301,000 households in Ireland owed arrears', 'Disagree: OR', [62])),
    ('disagree', 'disagree', 'A reason against clearing the arrears',
     H.menu('Disagree: OR\nOpportunity cost of government spending', '(c)\nComplete each diagram', [63])),
], '3-1', 'paying-household-electricity-arrears', 14, '(b)(iii)',
    H.ask(28, 'The Government should pay €142m', ' Agree Disagree'), 5,
    stem=H.ask(28, '301,000 households in Ireland owed arrears', ' Adapted from'))
q14c_stem = H.ask(28, 'Complete each diagram below to show how each', ' (i) A viral')
for roman, page, start, end, fig in [
        ('i', 28, 'A viral TikTok clip features', ' Diagram', 'p64-q14ci-demand-shift'),
        ('ii', 29, 'Sony shifts more PS5 production', ' Diagram', 'p65-q14cii-supply-shift'),
        ('iii', 29, 'Global shipping insurance premiums rise', ' Diagram', 'p65-q14ciii-supply-shift')]:
    event = H.ask(page, start, end)
    nxt = {'i': '(ii) Sony shifts more PS5', 'ii': '(iii) Global shipping insurance', 'iii': 'Question 15'}[roman]
    add(f'q14-c-{roman}', '1-0', 'ps5-market-equilibrium-' + {'i': 'demand-rise', 'ii': 'cheaper-production', 'iii': 'shipping-costs'}[roman],
        ref(14, f'(c)({roman})'), event, '8', 8,
        [point('r-explanation', H.run(f'({roman}) ' + start, nxt).split('Explanation', 1)[1].strip(), None,
               'Complete the diagram (the curve that shifts, its direction, the new price and quantity '
               'labelled) and explain. The official diagram is shown with the answer.')],
        kind='questionTotal', stem=q14c_stem, figure=FIG + fig,
        notes='The scheme gives 8 for the diagram and explanation together.')


# Q15 ─ the budget, the tax base, VAT, labour productivity
q15_stem = H.ask(30, 'The chart below shows the Irish exchequer', ' Budget 2026 Composition')
add('q15-a-i', '3-1', 'current-and-capital-spending-with-examples', ref(15, '(a)(i)'),
    H.ask(30, 'Explain the difference between current government expenditure', ' Current government expenditure:'),
    '6 + 6', 12,
    [point('r-current', H.run('Current government expenditure refers to', 'Capital expenditure:'), 6,
           'Explain current expenditure AND give one example, 6 marks. The scheme does not split '
           'the 6 between the explanation and the example; the listed examples are not a closed list.'),
     point('r-capital', H.run('Capital expenditure refers to spending by the government', 'In Budget 2026, capital spending made up'), 6,
           'Explain capital expenditure AND give one example, 6 marks, unsplit as above.')],
    stem=q15_stem)
pick('q15-a-ii', '3-1', 'why-raise-the-capital-share', ref(15, '(a)(ii)'),
     H.ask(30, 'Why, in your opinion, is the government planning', ' Reason:'),
     'A reason for raising the capital share',
     H.menu('(ii) Why, in your opinion, is the government planning to increase the proportion',
            '(iii) In Budget 2026, the Irish government ended', [67]),
     1, 6, 'One developed reason, 6 marks.',
     stem=q15_stem + ' ' + H.ask(30, 'In Budget 2026, capital spending made up', ' (ii) Why'))
pick('q15-a-iii', '3-1', 'why-targeted-supports', ref(15, '(a)(iii)'),
     H.ask(31, 'Outline one reason why the government took the step', ' Reason:'),
     'A reason for targeted supports',
     H.menu('Outline one reason why the government took the step to introduce more targeted',
            '(b) The Irish government has a narrow tax base', [68]),
     1, 6, 'One developed reason, 6 marks.',
     stem=H.ask(31, 'In Budget 2026, the Irish government ended', ' (iii) Outline'))
q15b_stem = H.ask(31, 'The Irish government has a narrow tax base', ' Adapted from')
broaden = [x.strip() for x in H.run('To broaden the tax base is to increase', '(ii) Outline two possible benefits').split('//')]
add('q15-b-i', '3-1', 'broadening-the-tax-base', ref(15, '(b)(i)'),
    H.ask(31, 'Explain what you understand by the term to broaden', ' Explain:'), '1 @ 6', 6,
    [anyN('r-1', 'What broadening the tax base means', 6, 1, 6, broaden,
          'Explain the term, 6 marks. Any one of the scheme\'s explanations.')],
    kind='bestNofParts', stem=q15b_stem)
pick('q15-b-ii', '3-1', 'benefits-of-a-broader-tax-base', ref(15, '(b)(ii)'),
     H.ask(31, 'Outline two possible benefits to the Irish economy', ' 1. 2.'),
     'A benefit of a broader base — any two',
     H.menu('Outline two possible benefits to the Irish economy of broadening the tax base.',
            '(iii) The government plans to reduce value-added tax', [69, 70]),
     2, 6, 'Two benefits, 6 marks each.', stem=q15b_stem)
stance('q15-b-iii', [
    ('agree', 'agree', 'A reason for the hospitality VAT cut',
     H.menu('Do you agree or disagree with this VAT reduction', 'Disagree: OR', [70])),
    ('disagree', 'disagree', 'A reason against the hospitality VAT cut',
     H.menu('Disagree: OR\nHigh opportunity cost', '(c) The graphic below shows the levels of labour', [71])),
], '3-1', 'hospitality-vat-reduction', 15, '(b)(iii)',
    H.ask(31, 'Do you agree or disagree with this VAT reduction', ' Agree Disagree'), 6,
    stem=H.ask(31, 'The government plans to reduce value-added tax', ' Do you agree'))
q15c_stem = H.ask(32, 'The graphic below shows the levels of labour productivity', ' Adapted from')
add('q15-c-i', '3-5', 'labour-productivity-and-sector-examples', ref(15, '(c)(i)'),
    H.ask(32, 'Explain what you understand by the term labour productivity.', ' Labour productivity:'),
    '5 + 2 + 2', 9,
    [point('r-meaning', H.run('Labour productivity refers to the value of output', 'Foreign sector example:'), 5,
           'Explain labour productivity, 5 marks.'),
     anyN('r-foreign', 'A foreign-dominated sector', 2, 1, 2,
          lines('Foreign sector example:', 'Domestic sector example:'), 'One foreign-dominated sector, 2 marks.'),
     anyN('r-domestic', 'A domestic-dominated sector', 2, 1, 2,
          lines('Domestic sector example:', '(ii) Increasing labour productivity'), 'One domestic-dominated sector, 2 marks.')],
    stem=q15c_stem)
add('q15-c-ii', '3-5', 'why-productivity-matters-and-how-to-raise-it', ref(15, '(c)(ii)'),
    H.ask(32, 'Outline one reason why increasing labour productivity', ' Reason:'), '6 + 6', 12,
    [heading('r-reason', 'One reason', H.menu('One reason:', 'One strategy:', [73]), 6,
             'Complete BOTH parts. One reason, 6 marks.'),
     heading('r-strategy', 'One strategy an employer could take',
             H.menu('One strategy:', '(iii) Artificial Intelligence', [74]), 6,
             'One employer strategy, 6 marks.')],
    stem=' '.join([q15c_stem, H.ask(32, 'Increasing labour productivity is important', ' Outline one')]))
stance('q15-c-iii', [
    ('narrow', 'narrow the gap', 'A reason AI may narrow the gap',
     H.menu('Narrow the gap:', 'Widen the gap:', [75])),
    ('widen', 'widen the gap', 'A reason AI may widen the gap',
     H.menu('Widen the gap:', 'Question 16', [75])),
], '3-5', 'ai-and-the-productivity-gap', 15, '(c)(iii)',
    H.ask(33, 'In your opinion, will AI narrow or widen', ' Narrow the gap Widen'), 6,
    stem=H.ask(33, 'Artificial Intelligence (AI) is expected', ' Adapted from'))

# Q16 ─ tourism, exchange rates, airports, Malawi
q16_stem = H.ask(34, 'The diagram below shows the market equilibrium for hotel rooms', ' Price S')
add('q16-a-i', '1-0', 'coolcations-and-hotel-room-equilibrium', ref(16, '(a)(i)'),
    H.ask(34, 'Using the diagram above, show how the increasing popularity', ' (ii) Prices'), '4', 4,
    [point('r-diagram', H.run('Price S\nPe2 E2', '(ii) Prices for hotel rooms in Dublin'), 4,
           'Shift demand right from D to D2. Supply S is vertical in the short run, so the new '
           'equilibrium E2 is at a higher price Pe2 with the quantity unchanged at Qe. Label every '
           'change; the scheme gives 4 for the completed diagram.')],
    stem=q16_stem, figure=FIG + 'p76-q16ai-hotel-rooms')
pick('q16-a-ii', '1-0', 'why-hotel-prices-rise-for-events', ref(16, '(a)(ii)'),
     H.ask(34, 'Explain why hotels can charge increased prices', ' Explain:'),
     'A reason hotels can charge more',
     H.menu('Explain why hotels can charge increased prices for their rooms during such concerts',
            '(iii) Local authorities in County Dublin', [76]),
     1, 7, 'One developed reason, 7 marks.',
     stem=H.ask(34, 'Prices for hotel rooms in Dublin rise sharply', ' Explain why'))
pick('q16-a-iii', '3-1', 'using-tourist-tax-revenue', ref(16, '(a)(iii)'),
     H.ask(34, 'Outline two ways the local authorities could use revenue', ' 1. 2.'),
     'A use of tourist-tax revenue — any two',
     H.menu('Outline two ways the local authorities could use revenue from a possible tourist tax',
            '(b) The chart below shows the main countries', [77]),
     2, 7, 'Two ways, 7 marks each.',
     stem=H.ask(34, 'Local authorities in County Dublin have discussed', ' Outline two'))
q16b_stem = H.ask(35, 'The chart below shows the main countries of origin', ' Foreign Visitors')
add('q16-b-i', '4-2', 'share-of-visitors-from-france', ref(16, '(b)(i)'),
    H.ask(35, 'Using data from the chart above, calculate the percentage', ' Workings:'), '5', 5,
    [point('r-working', '32,500/654,500 × 100/1', None, 'French visitors ÷ total visitors × 100.'),
     point('r-answer', 'Answer: 4.96 %', None, '32,500 ÷ 654,500 × 100 = 4.96%.')],
    kind='questionTotal', stem=q16b_stem, figure=FIG + 'p78-q16bi-france-share-working',
    notes='The scheme gives 5 for the working and answer together.')
pick('q16-b-ii', '4-2', 'weaker-dollar-and-us-visitors', ref(16, '(b)(ii)'),
     H.ask(35, 'Outline one way this development may have influenced', ' Outline:'),
     'An influence on US visitor numbers',
     H.menu('Outline one way this development may have influenced visitor numbers from the USA',
            '(iii) About 40 million people used Irish airports', [78, 79]),
     1, 7, 'One developed way, 7 marks.',
     stem=H.ask(35, 'In the months leading up to June 2025', ' Outline one way'))
pick('q16-b-iii', '3-5', 'state-airports-and-regional-development', ref(16, '(b)(iii)'),
     H.ask(36, 'Outline two ways the Irish government could use its ownership', ' 1. 2.'),
     'A way to use the airports — any two',
     H.menu('Outline two ways the Irish government could use its ownership of Dublin, Shannon',
            '(c) The production possibility frontier', [79, 80]),
     2, 7, 'Two ways, 7 marks each.',
     stem=H.ask(36, 'About 40 million people used Irish airports', ' Adapted from'))
q16c_stem = H.ask(36, 'The production possibility frontier (PPF) below shows', ' Tobacco leaf')
add('q16-c-i', '0-1', 'point-inside-the-ppf', ref(16, '(c)(i)'),
    H.ask(36, 'Explain what the blue point (labelled A)', ' Explain:'), '6', 6,
    [point('r-explain', H.run('Point A lies inside the production possibility frontier', 'Severe flash floods in Malawi'), 6,
           'Explain what an inside point shows about resource use, 6 marks.')],
    stem=q16c_stem, figure='economics-2026-HL-paper-p36-q16c-ppf')
cards[-1]['labelKey'] = [
    {'letter': 'A', 'meaning': 'the blue point inside PPF1, at quantities QTL of tobacco leaf and QC of corn', 'askedInThisQuestion': True},
    {'letter': 'B', 'meaning': 'the red point on the curve PPF1', 'askedInThisQuestion': False}]
add('q16-c-ii', '0-1', 'floods-and-the-ppf', ref(16, '(c)(ii)'),
    H.ask(37, 'Show in the diagram above how this development', ' Explain:'), '6', 6,
    [point('r-explain', H.run('Flash floods can damage farmland', 'In January 2025 the United States'), 6,
           'Draw PPF2 inside PPF1 and explain the fall in productive capacity; the scheme gives 6 '
           'for the diagram and explanation together.')],
    stem=q16c_stem + ' ' + H.ask(37, 'Severe flash floods in Malawi', ' Show in'),
    figure=FIG + 'p81-q16cii-ppf-shift')
add('q16-c-iii', '4-0', 'malawi-and-falling-us-aid', ref(16, '(c)(iii)'),
    H.ask(37, 'Outline one economic challenge and one social challenge', ' Economic:'), '6 + 6', 12,
    [heading('r-economic', 'Economic challenge',
             H.menu('result of this decline in US foreign aid.', 'Social challenge:', [82]), 6,
             'Complete BOTH headings. One economic challenge, 6 marks.'),
     heading('r-social', 'Social challenge',
             H.menu('Social challenge:', '81 | P a g e', [82]), 6,
             'One social challenge, 6 marks.')],
    stem=H.ask(37, 'In January 2025 the United States', ' Adapted from'))


# ── The paper's own charts, tables and starting diagrams, shown before reveal ──
QFIG = 'economics-2026-HL-paper-'
# The whole printed question, for the cards whose figure slot holds a solution.
FULLQ = {'q12-c-i': 'p20-q12ci-question', 'q13-b-ii': 'p23-q13bii-question',
         'q16-a-i': 'p34-q16ai-question', 'q16-b-i': 'p35-q16bi-question',
         'q16-c-ii': 'p36-q16cii-question'}
for keys, fig in [
        (['sa-q3-a-agree', 'sa-q3-a-disagree'], 'p05-q3-fan-costs'),
        (['sa-q4-a'], 'p06-q4-tshirt-price'),
        (['sa-q7-b-yes', 'sa-q7-b-no'], 'p10-q7b-kuznets-curve'),
        (['sa-q9-a', 'sa-q9-b'], 'p12-q9-gdp-charts'),
        (['sa-q10-a', 'sa-q10-b'], 'p13-q10-consumer-prices'),
        (['q11-a-i', 'q11-a-ii'], 'p14-q11-sport-participation'),
        (['q12-a-i-imports', 'q12-a-i-exports', 'q12-a-ii-benefit', 'q12-a-ii-challenge'], 'p18-q12-goods-trade'),
        (['q12-c-i', 'q12-c-i-influence'], 'p20-q12c-oil-producers'),
        (['q13-a-i'], 'p22-q13-ecb-rate'),
        (['q13-b-i', 'q13-b-ii', 'q13-b-iii'], 'p23-q13b-surf-school-costs'),
        (['q14-b-i', 'q14-b-ii'], 'p27-q14b-circular-flow'),
        (['q15-a-i', 'q15-a-ii'], 'p30-q15-budget-composition'),
        (['q15-c-i', 'q15-c-ii'], 'p32-q15c-labour-productivity'),
        (['q16-a-i'], 'p34-q16a-hotel-rooms'),
        (['q16-b-i'], 'p35-q16b-visitors'),
        (['q16-c-ii'], 'p36-q16c-ppf')]:
    for c in cards:
        short = c['id'].removeprefix('econ-2026-hl-')
        if short in keys:
            show_before_reveal(c, QFIG + fig, FULLQ.get(short) and QFIG + FULLQ[short])

if __name__ == '__main__':
    emit(cards)
