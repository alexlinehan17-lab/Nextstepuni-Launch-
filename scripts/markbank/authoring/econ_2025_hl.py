#!/usr/bin/env python3
"""Economics 2025 Higher Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2025-hl-ev.json,
made from a visual sweep of all 40 paper pages and 77 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID);
a card whose required headings had been split across two IDs is one card again
and the other ID resolves to it through an explicit progress alias.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). The only prose written
here is guidance: tariffs, route labels and what a figure or a calculation
shows. Scheme PDF page = printed page + 1.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_glyphfill import fill  # noqa: E402
from econ_lib import bullets, emit, point  # noqa: E402

H = Sheet(2025, 'higher', 'LC034ALP000EV')
D = Deck(2025, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2025-HL-scheme-'
PAP = 'economics-2025-HL-paper-'


def listed(start, end, occ=None):
    """The scheme's bullet list between two anchors, glyph-filled like every menu."""
    return bullets(fill(H.chunk(start, end, occ), 2025, 'hl'), drop_prefix=start)


# Headings the scheme draws with a glyph its text layer maps to a space (a bold K,
# an ff ligature) that no agreeing sighting can restore. Their explanations are
# set in the regular weight and read intact, so those options are lifted from
# the explanation alone rather than shipping a broken heading.
UNREADABLE_HEADINGS = ('nowledge Development Box', 'cluster e ect')


def readable(options):
    return [o.split(' – ', 1)[1] if any(u in o.split(' – ', 1)[0] for u in UNREADABLE_HEADINGS) else o
            for o in options]


def paras(options):
    """An open example list printed as one marking point (a whole-cell tariff)."""
    return '\n\n'.join(options)


def stance(prefix, choices, topic, concept, q, parts, qtext, per, *, sa=False, stem='', section='B',
           verb='justification for the', figure=''):
    """A printed tick-box choice whose scheme credits each side: one card per side."""
    for suffix, word, label, options in choices:
        pick(f'{prefix}-{suffix}', topic, concept, ref(q, parts, word, sa),
             f'{qtext} Answer for: {word.upper()}.', label, options, 1, per,
             f'One developed {verb} {word} choice, {per} marks. The scheme credits both choices; '
             f'these are its examples, not a closed list.',
             stem=stem, section='A' if sa else section, figure=figure)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ Euro 2024; cost benefit analysis
q1_stem = H.ask(3, 'Germany hosted the European Football Championship', ' (a)')
add('sa-q1-a-for', '3-5', 'hosting-a-major-sporting-event', ref(1, '(a)', sa=True),
    H.ask(3, 'Discuss one argument for and one argument against', ' Argument for hosting'), '6 + 6', 12,
    [heading('r-for', 'Argument for',
             H.menu('Argument for:', 'Argument against:', [5]), 6,
             'Complete BOTH headings. One argument for, 6 marks.'),
     heading('r-against', 'Argument against',
             H.menu('Argument against:', '(b) Outline what you understand by the economic term cost', [5]), 6,
             'One argument against, 6 marks.')],
    stem=q1_stem, **A)
add('sa-q1-b', '0-1', 'cost-benefit-analysis', ref(1, '(b)', sa=True),
    H.ask(3, 'Outline what you understand by the economic term cost benefit analysis.', ' Cost benefit'), '6', 6,
    [point('r-1', H.run('Helps weigh up / evaluate', '4 | P a g e'), 6, 'Explain the term, 6 marks.')],
    stem=q1_stem, **A)

# Q2 ─ household savings
q2_stem = H.ask(4, 'The table below shows household disposable income', ' (a)')
add('seca-q2-a', '3-0', 'household-percentage-savings-rate', ref(2, '(a)', sa=True),
    H.ask(4, 'From the data in the above table, calculate the household percentage savings rate',
          ' Workings:'), '6', 6,
    [point('r-answer', 'Answer: 15 %', 6,
           'Savings rate = household savings ÷ household disposable income × 100 = €6.59bn ÷ '
           '€43.91bn × 100 = 15%. The official working is shown in the figure. Deduct 1 mark if % '
           'is omitted.')],
    stem=q2_stem, figure=SOL + 'p06-q2a-working', **A)
pick('sa-q2-b', '3-0', 'what-households-weigh-when-saving', ref(2, '(b)', sa=True),
     H.ask(4, 'Outline two economic factors which some households', ' 1. 2.'),
     'A factor other than income — any two',
     H.menu('(b) Outline two economic factors which some households', '7 | P a g e', [7]),
     2, 3, 'Two factors, 3 marks each. Answer either (b) or (c).', stem=q2_stem, figure=PAP + 'p04-i0', **A)
stance('sa-q2-c', [
    ('agree', 'agree', 'A reason high household savings help',
     H.menu('\nAGREE:', 'DISAGREE:', [8], occ=0)),
    ('disagree', 'disagree', 'A reason high household savings harm',
     H.menu('DISAGREE:', '8 | P a g e', [8], occ=0))],
    '3-0', 'household-savings-and-the-economy', 2, '(c)',
    H.ask(4, 'A high level of household savings is desirable', ' Agree Disagree'), 6, sa=True, stem=q2_stem,
    figure=PAP + 'p04-i0')

# Q3 ─ used cars; EV imports; protectionism
q3_stem = H.ask(5, 'The chart below shows the number of used cars', ' Adapted from')
pick('sa-q3-a', '4-2', 'why-import-patterns-shift', ref(3, '(a)', sa=True),
     H.ask(5, 'Outline one economic reason why Irish consumers are switching', ' Economic reason:'),
     'An economic reason — any one',
     H.menu('3 (a) Outline one economic reason why Irish consumers', '8 | P a g e', [9]),
     1, 6, 'One developed reason, 6 marks.', stem=q3_stem, figure=PAP + 'p05-i0', **A)
pick('sa-q3-b', '4-2', 'alternatives-to-a-tariff', ref(3, '(b)', sa=True),
     H.ask(5, 'Explain one alternative measure the EU could use', ' Alternative measure:'),
     'An alternative measure — any one',
     H.menu('(b) Explain one alternative measure the EU could use', '9 | P a g e', [10]),
     1, 6, 'One measure, explained, 6 marks. Answer either (b) or (c).',
     stem=H.ask(5, 'In 2024, the European Union (EU) increased the tariffs', ' Explain one'), **A)
pick('sa-q3-c', '4-2', 'why-protectionism-is-rising', ref(3, '(c)', sa=True),
     H.ask(5, 'Outline one reason why, in your opinion, trade protectionism', ' Reason:'),
     'A reason protectionism is rising — any one',
     H.menu('Outline one reason why, in your opinion, trade protectionism', '10 | P a g e', [11]),
     1, 6, 'One developed reason, 6 marks.', stem=H.ask(5, 'Trade protectionism seems to be increasing globally.', ' Outline'),
     **A)

# Q4 ─ chocolate CPI; cost of living; cocoa
q4_stem = H.ask(6, 'The chart below displays the year-on-year percentage changes', ' Adapted from')
add('sa-q4-a-good', '3-3', 'trend-in-chocolate-inflation', ref(4, '(a)', sa=True),
    H.ask(6, 'Comment on the trend in the CPI for chocolate', ' Comment on trend:'), '6', 6,
    [point('r-trend', H.run('The trend in the CPI for chocolate shows a steady decline', 'Beneficial for chocolate consumers:'),
           None, 'Comment on the trend with data: 9.1% in January to 4.8% in June, a fall of 4.3 '
           'points. The chart shows the annual RATE of change, so chocolate prices are still '
           'rising, only more slowly.'),
     point('r-beneficial', H.run('Beneficial for chocolate consumers:', '11 | P a g e'), None,
           'Explain whether the trend is beneficial: either view is credited, and these are the '
           'scheme’s examples of each. The scheme gives one 6 for the trend and the explanation '
           'together, with no published split.')],
    kind='questionTotal', stem=q4_stem, figure=PAP + 'p06-i0', **A)
add('sa-q4-b-gov', '3-1', 'coping-with-the-cost-of-living', ref(4, '(b)', sa=True),
    H.ask(6, 'While the rate of price inflation has fallen', ' Irish government:'), '6 + 6', 12,
    [heading('r-government', 'One measure taken by the Irish government',
             H.menu('One measure taken by the Irish Government:', '12 | P a g e', [13]), 6,
             'Complete BOTH headings. The government measure, 6 marks.'),
     heading('r-consumers', 'One measure taken by consumers in Ireland',
             H.menu('One measure taken by consumers in Ireland:', '13 | P a g e', [14]), 6,
             'The consumer measure, 6 marks.')],
    notes='Answer either (b) or (c).', **A)
pick('sa-q4-c', '3-3', 'identifying-cost-push-inflation', ref(4, '(c)', sa=True),
     H.ask(7, 'Do you regard the above situation to be an example', ' Demand-pull inflation Cost-push'),
     'A justification for cost-push inflation — any one',
     H.menu('Justification:', '14 | P a g e', [15], occ=0),
     1, 6, 'Answer: Cost-push inflation. The scheme credits no demand-pull answer; one developed '
     'justification of cost-push, 6 marks for the choice and its justification together.',
     stem=H.ask(7, 'Chocolate producers buy cocoa in advance', ' Do you regard'), **A)

# Q5 ─ positive and normative
add('sa-q5-a', '0-0', 'positive-versus-normative-statements', ref(5, '(a)', sa=True),
    H.ask(7, 'Explain the difference between a positive economic statement', ' Positive economic'), '2 @ 3', 6,
    [point('r-positive', H.run('A positive economic statement is objective and fact-based.', 'Normative economic statement:'), 3,
           'Explain a positive statement, 3 marks.'),
     point('r-normative', H.run('A normative statement is subjective', '(b) Determine whether each'), 3,
           'Explain a normative statement, 3 marks.')], **A)
add('seca-q5-b', '0-0', 'positive-and-normative-statements-sorted', ref(5, '(b)', sa=True),
    H.ask(7, 'Determine whether each of the economic statements below', ' Positive Normative') + ' 1. '
    + H.clip(7, (80, 676, 420, 706)) + ' 2. ' + H.clip(7, (80, 709, 420, 753)), '2 @ 3', 6,
    [point('r-1', 'All citizens in Ireland deserve free healthcare to', 3,
           'Statement 1 is NORMATIVE: a value judgement (“deserve”), 3 marks.'),
     point('r-2', 'If the Irish government were to raise the', 3,
           'Statement 2 is POSITIVE: a prediction that can be tested against evidence, 3 marks.')],
    figure=SOL + 'p16-q5b-ticks', **A)

# Q6 ─ price floor; minimum wage diagram
add('sa-q6-a', '1-3', 'what-a-price-floor-is', ref(6, '(a)', sa=True),
    H.ask(8, 'Explain what you understand by the economic term price floor.', ' Price floor:'), '6', 6,
    [point('r-1', H.run('A price floor is a legal minimum price', '(b) The diagram below shows a free labour market.'), 6,
           'Explain the term, 6 marks.')],
    stem=H.ask(8, 'The national minimum wage rate currently stands', ' Explain what'), **A)
add('seca-q6-b', '2-1', 'a-minimum-wage-above-the-equilibrium', ref(6, '(b)', sa=True),
    H.ask(8, 'The diagram below shows a free labour market.', ' Wage rate'), '6', 6,
    [point('r-diagram', 'Unemployment gap / Excess supply of labour', None,
           'Draw the minimum wage as a horizontal line above WE. Label QD where it meets DL and QS '
           'where it meets SL; the gap QD to QS is the unemployment gap / excess supply of labour. '
           'The official diagram is shown in the figure.'),
     point('r-explanation', H.run('Wage rate: the national minimum wage rate', '16 | P a g e'), None,
           'Explain the wage rate, the rise in supply, the fall in demand and the excess supply. '
           'The scheme gives one 6 for the diagram and the explanation together.')],
    kind='questionTotal', figure=SOL + 'p17-q6b-labour-market', **A)

# Q7 ─ YED; merit goods
add('seca-q7-a', '1-4', 'spotting-a-necessity-and-a-luxury-from-yed', ref(7, '(a)', sa=True),
    H.ask(9, 'Identify one necessity and one luxury good', ' Product Justify'), '6', 6,
    [point('r-necessity', H.run('Necessity product – Electricity or Noodles', 'Luxury good'), None,
           'Necessity: domestic electricity (YED +0.1, between 0 and 1). Instant noodles (YED −0.5) '
           'is also accepted. Justify from the YED value.'),
     point('r-luxury', H.run('Luxury good – Premium branded clothing', '(b) The government announced'), None,
           'Luxury: premium branded clothing (YED +4.1, above 1). Justify from the YED value. The '
           'scheme gives one 6 for both answers, with no published split.')],
    kind='questionTotal', stem=H.ask(9, 'The table below shows estimated values for Income Elasticity', ' Product YED'),
    figure=PAP + 'p09-i0', **A)
add('sa-q7-b', '2-2', 'phone-pouches-as-merit-goods', ref(7, '(b)', sa=True),
    H.ask(9, 'Phone pouches in all secondary schools are considered', ' Explanation:'), '6', 6,
    [point('r-1', H.run('Phone pouches in secondary schools are considered a merit good', '17 | P a g e'), 6,
           'Explain why the pouches are a merit good, 6 marks.')],
    stem=H.ask(9, 'The government announced in Budget 2025', ' Phone pouches'), **A)

# Q8 ─ environmental sustainability; greenwashing
add('sa-q8-a', '0-2', 'irish-environmental-sustainability-initiative', ref(8, '(a)', sa=True),
    H.ask(10, 'Explain the concept of environmental sustainability', ' Environmental sustainability:'), '6', 6,
    [point('r-concept', H.run('Environmental sustainability refers to', 'Recent government initiative:'), None,
           'Explain the concept.'),
     point('r-initiative', paras(listed('Recent government initiative:', '18 | P a g e', occ=0)), None,
           'Outline one recent initiative; these are the scheme’s examples. The scheme gives one 6 '
           'for the concept and the initiative together, with no published split.')],
    kind='questionTotal', **A)
pick('sa-q8-b', '2-2', 'greenwashing-as-market-failure', ref(8, '(b)', sa=True),
     H.ask(10, 'Explain two ways in which greenwashing can lead to market failure.', ' 1. 2.'),
     'A way greenwashing causes market failure — any two',
     H.menu('Explain two ways in which greenwashing can lead to market failure.', '19 | P a g e', [20]),
     2, 3, 'Two ways, 3 marks each.',
     stem=H.ask(10, 'A study has shown that shoppers struggle', ' Explain two ways'), **A)

# Q9 ─ kinked demand curve
q9_stem = H.ask(11, 'The diagram below represents the long run equilibrium', ' Price 1')
add('q9-a', '2-0', 'labelling-the-kinked-demand-diagram', ref(9, '(a)', sa=True),
    H.ask(11, 'Using the answer box provided, write out in full', ' Number Label'), '6', 6,
    [point('r-1', 'Marginal cost', None, 'Item 1, the green curve through E.'),
     point('r-2', 'Average revenue = Demand', None, 'Item 2, the kinked yellow curve.'),
     point('r-3', 'Marginal revenue', None, 'Item 3, the red line with the vertical gap. The scheme '
           'gives one 6 for the three labels, with no published per-label split.')],
    kind='questionTotal', stem=q9_stem, figure=PAP + 'p11-art', **A)
add('sa-q9-b', '2-0', 'the-kinked-demand-curve', ref(9, '(b)', sa=True),
    H.ask(11, 'With reference to the diagram above, explain the shape', ' Explanation:'), '6', 6,
    [point('r-before', H.run('Before the kink', 'After the kink'), None,
           'Above the kink: rivals do not follow a price rise, so demand is relatively price elastic.'),
     point('r-after', H.run('After the kink', '20 | P a g e'), None,
           'Below the kink: rivals match a price cut, so demand is relatively price inelastic. The '
           'scheme gives one 6 for the explanation, with no published split.')],
    kind='questionTotal', stem=q9_stem, figure=PAP + 'p11-art', **A)

# Q10 ─ economic cycle
q10_stem = H.ask(12, 'The diagram below illustrates different phases', ' Output /')
add('seca-q10-a', '3-5', 'reading-boom-and-recession-off-the-cycle', ref(10, '(a)', sa=True),
    H.ask(12, 'Identify from the diagram above which option', ' An economic boom An economic recession'),
    '2 @ 3', 6,
    [point('r-boom', H.run('In this period, leading up to 2008', 'Economic recession justification:'), 3,
           'Economic boom: A. Justify from the steady rise in real GDP to 2008, 3 marks.'),
     point('r-recession', H.run('After the 2008 global financial crisis', '21 | P a g e'), 3,
           'Economic recession: B. Justify from the fall in output to 2011, 3 marks.')],
    stem=q10_stem, figure=PAP + 'p12-art', **A)
pick('sa-q10-b', '3-5', 'what-caused-the-irish-downturn', ref(10, '(b)', sa=True),
     H.ask(12, 'Outline one economic factor which led to a change', ' Economic factor:'),
     'An economic factor — any one',
     H.menu('(b) Outline one economic factor which led to a change', '22 | P a g e', [23]),
     1, 6, 'One developed factor, 6 marks.', stem=q10_stem, figure=PAP + 'p12-art', **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ health insurance HHI; patent monopoly; GPs
q11_stem = H.ask(13, 'The chart below shows the market shares of private health insurance', ' Adapted from')
add('q11-a-i', '2-0', 'hhi-for-irish-health-insurance', ref(11, '(a)(i)'),
    H.ask(13, 'Using the data provided above, calculate the Herfindahl Hirschman Index', ' Competitive Highly'),
    '8', 8,
    [point('r-answer', '2,401 + 784 + 400 + 9 = 3,594', None,
           'Tick HIGHLY CONCENTRATED. Square each share and add: 49² + 28² + 20² + 3² = 2,401 + 784 + '
           '400 + 9 = 3,594. The official working is shown in the figure.'),
     point('r-justify', H.run('According to the European Commission and the US Department of Justice', '23 | P a g e'),
           None, 'Justify: an HHI above 2,500 is highly concentrated; three firms hold 97%. The scheme '
           'gives one 8 for the tick, workings and justification together.')],
    kind='questionTotal', stem=q11_stem, figure=SOL + 'p24-q11ai-hhi-working')
pick('q11-a-ii', '2-0', 'effects-of-new-market-entrant', ref(11, '(a)(ii)'),
     H.ask(13, 'With the entry of this new firm into the Irish health insurance market', ' 1. 2.'),
     'An effect on the existing firms — any two',
     H.menu('(ii) With the entry of this new firm into the Irish health insurance', '24 | P a g e', [25]),
     2, 7, 'Two effects, 7 marks each.',
     stem=H.ask(13, 'New health insurance provider, Level Health', ' With the entry'))
q11b_stem = H.ask(14, 'A patent gives a pharmaceutical company the sole right', ' Explain, with')
mono_fig = SOL + 'p26-q11bi-patent-monopoly'
q11b_ask = H.ask(14, 'Explain, with the aid of a fully labelled diagram', ' Explanation:')
add('q11-b-i', '2-0', 'long-run-equilibrium-of-a-patent-monopoly', ref(11, '(b)(i)', 'diagram'),
    q11b_ask + ' Draw the diagram.', '12', 12,
    [point('r-diagram', 'P Q MR AR MC AC E Q1 P1 C1 SNPs', 12,
           'Label Price / Cost (€) and Quantity, and the MC, AC, AR = D and MR curves. Equilibrium E '
           'where MC = MR with MC rising; output Q1; price P1 on AR at Z; average cost C1 on AC at Y; '
           'shade the supernormal profit (SNPs) between P1 and C1; W marks minimum AC. The scheme '
           'lists these eleven labels for the 12-mark diagram without a per-label split.')],
    stem=q11b_stem, figure=mono_fig,
    notes='The diagram (12) and the written explanation (9) are separately priced in the scheme.')
add('q11-b-i-explanation', '2-0', 'explain-patent-monopoly-long-run', ref(11, '(b)(i)', 'explanation'),
    q11b_ask + ' Write the explanation.', '9', 9,
    [point('r-explanation', H.run('• Equilibrium is at point E', '25 | P a g e'), 9,
           'Explain all six features of the long-run equilibrium; the scheme gives 9 for the '
           'explanation with no separately priced steps.')],
    stem=q11b_stem, figure=mono_fig)
pick('q11-b-ii', '2-0', 'barriers-to-entry-in-monopoly', ref(11, '(b)(ii)'),
     H.ask(14, 'Outline one barrier to entry often found in monopoly markets', ' Barrier to entry:'),
     'A barrier to entry other than a patent — any one',
     H.menu('(ii) Outline one barrier to entry often found in monopoly markets', '26 | P a g e', [27]),
     1, 4, 'One barrier other than a patent, 4 marks.')
add('q11-b-iii-adv', '2-0', 'monopoly-power-and-consumers', ref(11, '(b)(iii)'),
    H.ask(15, 'Outline one economic advantage and one economic disadvantage for consumers', ' Economic advantage:'),
    '4 + 4', 8,
    [heading('r-advantage', 'Economic advantage for consumers',
             H.menu('Economic Advantage for Consumers:', 'Economic Disadvantage for Consumers:', [28]), 4,
             'Complete BOTH headings. The advantage, 4 marks.'),
     heading('r-disadvantage', 'Economic disadvantage for consumers',
             H.menu('Economic Disadvantage for Consumers:', '27 | P a g e', [28]), 4,
             'The disadvantage, 4 marks.')])
q11c_stem = H.ask(15, 'More than three-quarters of the approximately 2,500 GP', ' (i)')
pick('q11-c-i', '2-1', 'effects-of-a-gp-shortage', ref(11, '(c)(i)'),
     H.ask(15, 'Outline two possible effects that the above development', ' 1. 2.'),
     'An effect on patients — any two',
     H.menu('(i) Outline two possible effects that the above development', '(ii) Suggest one economic measure', [29]),
     2, 4, 'Two effects, 4 marks each.', stem=q11c_stem)
pick('q11-c-ii', '2-1', 'addressing-a-shortage-of-gps', ref(11, '(c)(ii)'),
     H.ask(16, 'Suggest one economic measure the Irish government could take', ' Economic measure:'),
     'An economic measure — any one',
     H.menu('(ii) Suggest one economic measure the Irish government could take', 'The Irish healthcare system reflects', [29, 30]),
     1, 4, 'One measure, 4 marks.', stem=q11c_stem)
add('q11-c-iii', '1-0', 'evidence-that-ireland-is-a-mixed-economy', ref(11, '(c)(iii)'),
    H.ask(16, 'Explain what is meant by the term mixed economy', ' Mixed economy:'), '8', 8,
    [point('r-meaning', H.run('A mixed economy is an economic system', 'Any relevant example:'), None,
           'Explain the term.'),
     point('r-example', paras(H.menu('Any relevant example:', '29 | P a g e', [30], occ=0)), None,
           'Outline another example other than healthcare; these are the scheme’s examples. The '
           'scheme gives one 8 for the meaning and the example together, with no published split.')],
    kind='questionTotal', stem=H.ask(16, 'The Irish healthcare system reflects', ' Explain what'))

# Q12 ─ government debt; tax revenue; auto-enrolment
q12_stem = H.ask(17, 'The chart below displays Ireland’s general government debt', ' Adapted from')
q12a_ask = H.ask(17, 'Outline the overall trend in Ireland’s general government debt', ' Overall trend:')
for cid, word, start, end in [
        ('q12-a-i', 'debt as a % of GNI*', 'Government Debt as a % of GNI*:', 'Government Debt as a % of GDP:'),
        ('q12-a-i-gdp', 'debt as a % of GDP', 'Government Debt as a % of GDP:', 'Downward + Reference')]:
    add(cid, '3-1', 'the-trend-in-irelands-government-debt', ref(12, '(a)(i)', word),
        q12a_ask + f' Answer for: {word.upper()}.', '6', 6,
        [point('r-trend', H.run(start, end), 6,
               'The ticked series: state the downward trend and support it with two distinct figures '
               'or the overall fall, as the scheme requires (“Downward + Reference to two distinct '
               'figures or overall percentage decrease”).')],
        stem=q12_stem, figure=PAP + 'p17-i0')
add('q12-a-ii-tax', '3-1', 'advantages-of-lower-government-debt', ref(12, '(a)(ii)'),
    H.ask(17, 'Outline one economic advantage of Ireland reducing its level', ' Taxpayers in Ireland: The'),
    '7 + 7', 14,
    [heading('r-taxpayers', 'Taxpayers in Ireland',
             H.menu('Taxpayers in Ireland:', 'The Irish government:', [32]), 7,
             'Complete BOTH headings. The advantage for taxpayers, 7 marks.'),
     heading('r-government', 'The Irish government',
             H.menu('The Irish government:', '31 | P a g e', [32]), 7,
             'The advantage for the government, 7 marks.')],
    stem=q12_stem, figure=PAP + 'p17-i0')
pick('q12-a-iii', '3-0', 'why-gni-star-beats-gdp', ref(12, '(a)(iii)'),
     H.ask(18, 'Which is a more accurate measure of Ireland’s debt burden', ' Debt as a percentage of GNI* Debt'),
     'A justification for debt as a % of GNI* — any one',
     listed('Justify :', '32 | P a g e'),
     1, 6, 'Tick DEBT AS A PERCENTAGE OF GNI*: the scheme credits no GDP answer. One developed '
     'justification, 6 marks for the choice and its justification together.', stem=q12_stem,
     figure=PAP + 'p17-i0')
q12b_stem = H.ask(18, 'The two charts below compare Ireland', ' (i)')
add('q12-b-i', '3-1', 'what-changed-in-irish-tax-revenue', ref(12, '(b)(i)'),
    H.ask(18, 'Identify the MOST significant change', ' Most significant change:'), '6 + 6', 12,
    [point('r-change', H.run('The most significant change is the increase in Corporation Tax', 'Reason:'), 6,
           'The increase in Corporation Tax from 16% to 27% (11 points), 6 marks.'),
     heading('r-reason', 'Reason for the change',
             readable(H.menu('Reason:', '33 | P a g e', [34], occ=0)), 6, 'One reason for the change, 6 marks.')],
    stem=q12b_stem, figure=PAP + 'p18-i0')
pick('q12-b-ii', '3-1', 'why-vat-is-regressive', ref(12, '(b)(ii)'),
     H.ask(19, 'Do you regard Ireland’s value added tax system', ' Progressive tax Regressive'),
     'Why VAT is regressive',
     [H.run('A regressive tax is a tax that takes a higher proportion', '(iii) Some politicians')],
     1, 8, 'Tick REGRESSIVE TAX: the scheme credits no progressive answer. Justify, 8 marks for the '
     'choice and its justification together.')
stance('q12-b-iii', [
    ('agree', 'agree', 'A reason for a higher top rate',
     H.menu('\nAGREE:', '34 | P a g e', [35], occ=1)),
    ('disagree', 'disagree', 'A reason against a higher top rate',
     H.menu('DISAGREE:', '35 | P a g e', [36], occ=1))],
    '3-1', 'a-higher-income-tax-rate-above-100000', 12, '(b)(iii)',
    H.ask(19, 'Do you agree or disagree with the statement, that individuals', ' Agree Disagree'), 8,
    stem=H.ask(19, 'Some politicians are debating the possible introduction', ' Do you agree'))
q12c_stem = H.ask(20, 'This September, the Irish government will introduce', ' Outline one')
add('q12-c-i-employee', '2-1', 'auto-enrolment-for-employee-and-employer', ref(12, '(c)(i)'),
    H.ask(20, 'Outline one possible economic advantage to the employee', ' Advantage to the employee:'),
    '7 + 7', 14,
    [heading('r-employee', 'Economic advantage to the employee',
             H.menu('Economic Advantage to the Employee:', 'Economic Disadvantage to the Employer:', [37]), 7,
             'Complete BOTH headings. The advantage to the employee, 7 marks.'),
     heading('r-employer', 'Economic disadvantage to the employer',
             H.menu('Economic Disadvantage to the Employer:', '36 | P a g e', [37]), 7,
             'The disadvantage to the employer, 7 marks.')],
    stem=q12c_stem)
add('q12-c-ii', '3-0', 'pension-saving-and-the-multiplier', ref(12, '(c)(ii)'),
    H.ask(20, 'Discuss how this auto-enrolment pension scheme may influence', ' Influence on'), '7', 7,
    [point('r-1', H.run('It will result in a weaker multiplier effect.', '37 | P a g e'), 7,
           'A weaker multiplier, explained through lower spending and the larger denominator from a '
           'lower MPC, 7 marks.')],
    stem=q12c_stem)

# Q13 ─ exports; FDI; comparative advantage; ODA
q13_stem = H.ask(21, 'The chart below shows the value of Ireland’s exports', ' Adapted from')
add('q13-a-i', '4-2', 'share-of-goods-exports-to-the-united-states', ref(13, '(a)(i)'),
    H.ask(21, 'Calculate the percentage of Ireland’s total goods exports', ' Workings:'), '8', 8,
    [point('r-answer', 'Answer: 31.48% / 32%', 8,
           'Exports to the US ÷ total goods exports × 100 = €34bn ÷ €108bn × 100 = 31.48% (32% '
           'accepted). The official working is shown in the figure. Deduct 1 mark if % is omitted.')],
    stem=q13_stem, figure=SOL + 'p39-q13ai-working')
add('q13-a-ii-benefit', '4-2', 'benefit-and-challenge-of-irish-exports', ref(13, '(a)(ii)'),
    H.ask(21, 'Outline one economic benefit and one economic challenge', ' Economic benefit:'), '7 + 7', 14,
    [heading('r-benefit', 'Economic benefit',
             H.menu('Economic Benefit:', 'Economic Challenge:', [40]), 7,
             'Complete BOTH headings. The benefit, 7 marks.'),
     heading('r-challenge', 'Economic challenge',
             H.menu('Economic Challenge:', '39 | P a g e', [40]), 7, 'The challenge, 7 marks.')],
    stem=H.ask(21, 'In 2022, the CSO reported', ' Outline one'))
pick('q13-a-iii', '4-1', 'why-outward-fdi-matters', ref(13, '(a)(iii)'),
     H.ask(22, 'Outline one economic reason why such outflows of FDI', ' Reason:'),
     'An economic reason — any one',
     H.menu('(iii) Outline one economic reason why such outflows of FDI', '40 | P a g e', [41]),
     1, 7, 'One developed reason, 7 marks.',
     stem=H.ask(22, 'Ireland is now the ninth-largest contributor', ' Adapted from'))
q13b_stem = H.ask(22, 'Over 90 foreign pharmaceutical companies operate', ' Adapted from')
add('q13-b-i', '4-2', 'the-principle-of-comparative-advantage', ref(13, '(b)(i)'),
    H.ask(22, 'Ireland has a comparative advantage in attracting', ' Principle of'), '7', 7,
    [point('r-1', H.run('Comparative advantage occurs when a country specialises', '(ii) Outline two sources'), 7,
           'Explain the principle, 7 marks.')],
    stem=q13b_stem)
pick('q13-b-ii', '4-2', 'sources-of-comparative-advantage', ref(13, '(b)(ii)'),
     H.ask(23, 'Outline two sources of comparative advantage in Ireland', ' 1. 2.'),
     'A source of comparative advantage — any two',
     readable(H.menu('(ii) Outline two sources of comparative advantage in Ireland', '(iii) The World Trade Organisation', [42, 43])),
     2, 6, 'Two sources, 6 marks each.', stem=q13b_stem)
pick('q13-b-iii', '4-2', 'functions-of-the-wto', ref(13, '(b)(iii)'),
     H.ask(23, 'Outline one function of the WTO.', ' One function:'),
     'A function of the WTO — any one',
     H.menu('(iii) The World Trade Organisation (WTO) plays a crucial role', '42 | P a g e', [43]),
     1, 6, 'One function, 6 marks.', stem=H.ask(23, 'The World Trade Organisation (WTO) plays', ' Outline one'))
q13c_stem = H.ask(23, 'The chart below shows the percentage of Gross National Income', ' Adapted from')
pick('q13-c-i', '4-0', 'why-ireland-misses-the-aid-target', ref(13, '(c)(i)'),
     H.ask(23, 'Outline one possible economic reason for the Irish government failing', ' Explain:'),
     'An economic reason — any one',
     H.menu('(i) Outline one possible economic reason for the Irish government failing', '43 | P a g e', [44]),
     1, 7, 'One developed reason, 7 marks.', stem=q13c_stem, figure=PAP + 'p23-i0')
pick('q13-c-ii', '4-0', 'what-overseas-aid-does-for-ldcs', ref(13, '(c)(ii)'),
     H.ask(24, 'Outline one possible economic benefit that Ireland’s ODA provides', ' Outline:'),
     'An economic benefit — any one',
     H.menu('(ii) Outline one possible economic benefit that Ireland', '44 | P a g e', [45]),
     1, 7, 'One developed benefit, 7 marks.', stem=q13c_stem, figure=PAP + 'p23-i0')
pick('q13-c-iii', '4-0', 'the-cost-of-aid-dependence', ref(13, '(c)(iii)'),
     H.ask(24, 'Outline one challenge for LDCs who have become dependent', ' Challenge:'),
     'A challenge of aid dependence — any one',
     H.menu('(iii) Outline one challenge for LDCs who have become dependent', '45 | P a g e', [46]),
     1, 7, 'One developed challenge, 7 marks.', stem=q13c_stem, figure=PAP + 'p23-i0')

# Q14 ─ online shopping; Scentastic; gig economy; full employment
q14_stem = H.ask(25, 'The graphic below shows that the majority of internet users', ' Adapted from')
pick('q14-a-i', '1-1', 'benefits-of-online-shopping', ref(14, '(a)(i)'),
     H.ask(25, 'Outline two benefits of online shopping for consumers', ' 1. 2.'),
     'A benefit of online shopping — any two',
     H.menu('Possible benefits:', '46 | P a g e', [47]),
     2, 5, 'Two benefits, 5 marks each. Wider selection is excluded by the question.',
     stem=q14_stem, figure=PAP + 'p25-i0')
pick('q14-a-ii', '2-0', 'amazon-expansion-and-small-retailers', ref(14, '(a)(ii)'),
     H.ask(25, 'Outline two economic difficulties which Amazon', ' 1. 2.'),
     'A difficulty for small and medium retailers — any two',
     H.menu('Economic difficulties:', '47 | P a g e', [48]),
     2, 5, 'Two difficulties, 5 marks each.', stem=H.ask(25, 'Amazon plans to open a dedicated store', ' Outline two'))
q14a3_ask = H.ask(26, 'Online shopping shows how advances in technology', ' Agriculture Sports')
for cid, word, start, end, pages in [
        ('q14-a-iii-agri', 'agriculture', 'Agriculture:', '48 | P a g e', [49]),
        ('q14-a-iii-sport', 'sports and fitness', 'Sports & Fitness:', '49 | P a g e', [50])]:
    pick(cid, '1-2', 'technology-and-a-sector', ref(14, '(a)(iii)', word),
         f'{q14a3_ask} Answer for: {word.upper()}.', f'A way technology changes {word} — any one',
         H.menu(start, end, pages), 1, 5,
         f'One developed way for the ticked sector, 5 marks. The scheme credits both sectors; these '
         f'are its examples, not a closed list.')
q14b_stem = H.ask(26, 'The data below represents the market demand and the market supply schedules', ' (i)')
add('q14-b-i', '1-0', 'plotting-demand-and-supply-and-finding-equilibrium', ref(14, '(b)(i)'),
    H.ask(26, 'Using the data above, complete on the graph paper provided below', ' Price €'), '2 + 6 + 6 + 3', 17,
    [point('r-axes', 'Axes:', 2, 'Complete both axes: price €0.50 to €3.00 and quantity 10,000 to 50,000, 2 marks.'),
     point('r-demand', 'D:6', 6, 'Plot the five demand points and join them, labelled D, 6 marks.'),
     point('r-supply', 'S:6', 6, 'Plot the five supply points and join them, labelled S, 6 marks.'),
     point('r-equilibrium', 'Equil', 3,
           'Label the intersection E, show Pe = €2.00 and Qe = 30,000 units: 1 mark each. The scheme '
           'prints this 17 × 1 split in its margin (Equil, Pe, Qe); the official graph is shown in the figure.')],
    stem=q14b_stem, figure=SOL + 'p51-q14bi-graph')
q14b2_ask = H.ask(27, 'Using an appropriate formula, calculate the price elasticity', ' Workings:')
add('q14-b-ii', '1-4', 'calculate-price-elasticity-of-demand', ref(14, '(b)(ii)', 'calculation'),
    q14b2_ask + ' Do the calculation.', '9', 9,
    [point('r-answer', 'Answer: - 1.8', 9,
           'Midpoint PED = (ΔQ ÷ ΔP) × ((P1 + P2) ÷ (Q1 + Q2)) = (−10,000 ÷ 0.50) × (4.50 ÷ 50,000) '
           '= −1.8. The official working is shown in the figure.')],
    figure=SOL + 'p52-q14bii-ped-working',
    notes='The workings (9) and the economic meaning (5) are separately priced in the scheme.')
add('q14-b-ii-meaning', '1-4', 'interpreting-a-ped-value', ref(14, '(b)(ii)', 'economic meaning'),
    q14b2_ask + ' Write the economic meaning.', '5', 5,
    [point('r-meaning', H.run('The sign is minus therefore Scentastic obeys the Law of Demand.', '51 | P a g e'), 5,
           'Explain the sign (law of demand, inverse relationship) and the size (1.8 > 1, price '
           'elastic). The scheme’s last line says a €1 price rise cuts quantity by 1.8%; PED compares '
           'percentage changes, so it is a 1% rise in price that cuts quantity demanded by 1.8%.')])
q14c_stem = H.ask(27, 'Nearly 200,000 citizens in Ireland work in the gig economy.', ' Do you agree')
stance('q15-a-i', [
    ('agree', 'agree', 'A reason to regulate gig work further',
     H.menu('\nAGREE:', 'DISAGREE responses overleaf', [53], occ=2)),
    ('disagree', 'disagree', 'A reason against further regulation',
     H.menu('DISAGREE:', '53 | P a g e', [54], occ=2))],
    '2-1', 'regulating-the-gig-economy', 14, '(c)(i)',
    H.ask(27, 'Do you agree or disagree with the statement above?', ' Agree Disagree'), 7, stem=q14c_stem)
add('q14-c-ii-positive', '3-2', 'effects-of-full-employment', ref(14, '(c)(ii)'),
    H.ask(28, 'Outline one positive economic effect and one negative economic effect', ' Positive economic effect:'),
    '6 + 6', 12,
    [heading('r-positive', 'Positive economic effect',
             H.menu('Positive economic effect:', 'Negative economic effect:', [55]), 6,
             'Complete BOTH headings. The positive effect, 6 marks.'),
     heading('r-negative', 'Negative economic effect',
             H.menu('Negative economic effect:', '54 | P a g e', [55]), 6, 'The negative effect, 6 marks.')],
    stem=H.ask(28, 'Ireland has maintained near to full employment', ' Outline one'))

# Q15 ─ access to cash; credit; RPPI; infrastructure
q15_stem = H.ask(29, 'The Government has published The Finance', ' (a)')
stance('q15-a-i-cash', [
    ('agree', 'agree', 'A reason to support the bill',
     H.menu('\nAGREE:', 'DISAGREE:', [56], occ=3)),
    ('disagree', 'disagree', 'A reason to oppose the bill',
     H.menu('DISAGREE:', '55 | P a g e', [56], occ=3))],
    '3-4', 'protecting-access-to-cash', 15, '(a)(i)',
    H.ask(29, 'Do you agree or disagree with The Finance', ' Agree Disagree'), 6, stem=q15_stem)
pick('q15-a-ii', '3-4', 'factors-affecting-credit-creation', ref(15, '(a)(ii)'),
     H.ask(29, 'Outline two factors that affect the amount of credit', ' 1. 2.'),
     'A factor affecting credit creation — any two',
     H.menu('(ii) Outline two factors, which affect the amount of credit', '(iii) ccording to', [57]),
     2, 6, 'Two factors, 6 marks each.')
pick('q15-a-iii-aib', '3-4', 'why-a-bank-invests-in-its-branches', ref(15, '(a)(iii)'),
     H.ask(29, 'Outline one economic reason, why, in your opinion, AIB', ' Economic reason:'),
     'An economic reason — any one',
     H.menu('(iii) ccording to the Irish Times', '56 | P a g e', [57]),
     1, 6, 'One developed reason, 6 marks.', stem=H.ask(29, 'According to the Irish Times', ' Outline one'))
q15b_stem = H.ask(30, 'The chart below, adapted from the CSO', ' (i)')
add('q15-b-i', '3-3', 'percentage-increase-in-the-residential-property-price-index', ref(15, '(b)(i)'),
    H.ask(30, 'Using the data in the chart above, calculate the percentage increase', ' Workings:'), '8', 8,
    [point('r-answer', 'Answer: 36.48%', 8,
           '(August − March) ÷ March × 100 = (10.1 − 7.4) ÷ 7.4 × 100 = 36.48%. The chart plots '
           'annual growth RATES, so this is the increase in the rate of property-price inflation. '
           'The official working is shown in the figure. Deduct 1 mark if % is omitted.')],
    stem=q15b_stem, figure=SOL + 'p58-q15bi-working')
pick('q15-b-ii', '2-1', 'property-prices-and-the-labour-market', ref(15, '(b)(ii)'),
     H.ask(30, 'Discuss two economic effects which this development', ' 1. 2.'),
     'An effect on the labour market — any two',
     H.menu('Discuss two economic effects which the development above may have', '58 | P a g e', [59]),
     2, 6, 'Two effects, 6 marks each.', stem=H.ask(30, 'Rising property prices is affecting', ' Discuss two'))
stance('q15-b-iii', [
    ('agree', 'agree', 'A reason for mortgage interest relief',
     H.menu('\nAGREE:', 'DISAGREE:', [60], occ=4)),
    ('disagree', 'disagree', 'A reason against mortgage interest relief',
     H.menu('DISAGREE:', '59 | P a g e', [60], occ=4))],
    '1-3', 'mortgage-interest-relief', 15, '(b)(iii)',
    H.ask(31, 'Do you agree or disagree with this government decision?', ' Agree Disagree'), 5,
    stem=H.ask(31, 'In Budget 2025, the government decided', ' Do you agree'))
q15c_stem = H.ask(31, 'What we have to prioritise now is enabling infrastructure', ' (i)')
add('q15-c-i', '3-1', 'what-public-infrastructure-is', ref(15, '(c)(i)'),
    H.ask(31, 'Explain the economic term public infrastructure', ' Public infrastructure:'), '6', 6,
    [point('r-meaning', H.run('Public infrastructure refers to essential facilities', 'Any relevant example:'), None,
           'Explain the term.'),
     point('r-example', H.run('Ireland’s public water supply system', '60 | P a g e'), None,
           'Illustrate with one example; these are the scheme’s examples. The scheme gives one 6 for '
           'the term and the example together, with no published split.')],
    kind='questionTotal', stem=q15c_stem)
pick('q15-c-ii', '3-1', 'challenges-of-insufficient-infrastructure-spending', ref(15, '(c)(ii)'),
     H.ask(31, 'Discuss two possible challenges for the Irish economy', ' 1. 2.'),
     'A challenge for the economy — any two',
     H.menu('(ii) Discuss two possible challenges for the Irish economy', '61 | P a g e', [62]),
     2, 5, 'Two challenges, 5 marks each.', stem=q15c_stem)
pick('q15-c-iii', '3-1', 'why-government-spending-rose', ref(15, '(c)(iii)'),
     H.ask(32, 'Explain two economic reasons for the significant increase', ' 1. 2.'),
     'A reason other than infrastructure — any two',
     H.menu('Explain two economic reasons for the significant increase', 'More possible responses continued overleaf', [63])
     + H.menu('More possible responses continued overleaf', '63 | P a g e', [64]),
     2, 5, 'Two reasons other than infrastructure, 5 marks each.',
     stem=H.ask(32, 'The data below shows the levels of total expenditure', ' Year 2015'), figure=PAP + 'p32-i0')

# Q16 ─ smoothie costs; diseconomies; LRAC; hospitality; entrepreneurship
q16_stem = H.ask(33, 'The table below shows the daily output and production costs', ' Output Fixed')
add('q16-a-i', '1-5', 'filling-in-variable-and-average-cost', ref(16, '(a)(i)'),
    H.ask(33, 'Complete the variable cost and average cost, labelled A and B', ' Answer Label'), '6', 6,
    [point('r-a', '€70 - €60 = €10', None, 'A: variable cost = total cost − fixed cost = €70 − €60 = €10.'),
     point('r-b', 'Answer = €1.92', None, 'B: average cost = total cost ÷ output = €115 ÷ 60 = €1.92. The '
           'official working is shown in the figure. The scheme gives one 6 for both cells, with no '
           'published split.')],
    kind='questionTotal', stem=q16_stem, figure=SOL + 'p65-q16ai-working')
add('q16-a-ii', '1-5', 'calculating-profit-from-revenue-and-cost', ref(16, '(a)(ii)'),
    H.ask(33, 'If the outlet charges €4.00 for a fresh smoothie', ' Workings:'), '5', 5,
    [point('r-answer', 'PROFIT €70', 5,
           'Revenue €4.00 × 40 = €160, minus the total cost of 40 smoothies, €90 (from the table), '
           'gives a profit of €70.')],
    stem=q16_stem, figure=PAP + 'p33-i0')
pick('q16-a-iii', '1-5', 'firm-objectives-other-than-profit', ref(16, '(a)(iii)'),
     H.ask(33, 'Outline two objectives the owner of the smoothie', ' 1. 2.'),
     'An objective other than profit maximisation — any two',
     H.menu('(iii) Outline two objectives the owner of the smoothie', '65 | P a g e', [66]),
     2, 7, 'Two objectives, 7 marks each.', stem=q16_stem, figure=PAP + 'p33-i0')
add('q16-b-i-diseconomies', '1-5', 'diseconomies-of-scale-in-a-smoothie-business', ref(16, '(b)(i)'),
    H.ask(34, 'Explain the term diseconomies of scale and outline one example', ' Diseconomies of scale:'), '9', 9,
    [point('r-meaning', H.run('Diseconomies of scale refer to factors', 'Example:'), None, 'Explain the term.'),
     point('r-example', paras(H.menu('Example:', '66 | P a g e', [67], occ=0)), None,
           'Outline one example for a smoothie retailer; these are the scheme’s examples. The scheme '
           'gives one 9 for the term and the example together, with no published split.')],
    kind='questionTotal', stem=H.ask(34, 'Retailers in the Irish fresh smoothie market', ' Explain the term'))
lrac_fig = SOL + 'p68-q16bii-lrac'
lrac_q = PAP + 'p34-q16bii-question'
q16b2_ask = H.ask(34, 'The partially completed diagram below shows', ' Costs SRAC')
add('q16-b-ii', '1-5', 'constructing-and-reading-the-lrac', ref(16, '(b)(ii)', 'diagram'),
    q16b2_ask + ' Draw the diagram.', '3 + 3 + 1 + 1', 8,
    [point('r-srac', 'SRAC x 3', 3, 'Draw three more short-run average cost curves, 1 mark each.'),
     point('r-srac-labels', 'Labels x 3', 3, 'Label them SRAC3, SRAC4 and SRAC5, 1 mark each.'),
     point('r-lrac', 'LRAC x 1', 1, 'Draw the LRAC as the envelope touching each SRAC, 1 mark.'),
     point('r-lrac-label', 'Label x 1', 1, 'Label the LRAC, 1 mark. The scheme prints this split in '
           'its margin; the official diagram is shown in the figure.')],
    figure=lrac_fig,
    notes='The diagram (8) and the written explanation (8) are separately priced in the scheme.')
add('q16-b-ii-explanation', '1-5', 'explaining-the-shape-of-the-lrac', ref(16, '(b)(ii)', 'explanation'),
    q16b2_ask + ' Write the explanation.', '8', 8,
    [point('r-down', H.run('Downward sloping part of the LRAC', 'Upward sloping part of the LRAC'), None,
           'Downward part: economies of scale dominate, Q1 to Q3.'),
     point('r-up', H.run('Upward sloping part of the LRAC', '67 | P a g e'), None,
           'Upward part: diseconomies of scale dominate after Q3, with a further example of a '
           'diseconomy other than the one in (b)(i). The scheme gives one 8 for the explanation, with '
           'no published split.')],
    kind='questionTotal', figure=lrac_fig)
q16c_stem = H.ask(35, 'The graphic below shows the number of companies', ' Adapted from')
pick('q16-b-i', '1-3', 'reducing-hospitality-closures', ref(16, '(c)(i)'),
     H.ask(35, 'Outline two economic measures the Irish government could implement', ' 1. 2.'),
     'A measure to reduce closures — any two',
     H.menu('(i) Outline two economic measures the Irish government could implement', 'More possible response continued overleaf', [69])
     + H.menu('More possible response continued overleaf', '(ii) In the short run', [70]),
     2, 6, 'Two measures, 6 marks each.', stem=q16c_stem, figure=PAP + 'p35-i0')
add('q16-c-ii', '1-5', 'staying-open-at-a-short-run-loss', ref(16, '(c)(ii)'),
    H.ask(35, 'In the short run a company may remain in business', ' Explanation:'), '5', 5,
    [point('r-1', H.run('Even if making a loss, a firm should continue', '69 | P a g e'), 5,
           'Explain why a loss-making firm stays open in the short run, 5 marks.')],
    stem=q16c_stem)
pick('q16-c', '0-0', 'importance-of-entrepreneurship', ref(16, '(c)(iii)'),
     H.ask(36, 'Discuss two reasons, why entrepreneurship is important', ' 1. 2.'),
     'A reason entrepreneurship matters — any two',
     H.menu('Discuss two reasons, why entrepreneurship is important', '70 | P a g e', [71]),
     2, 4, 'Two reasons, 4 marks each.',
     stem=H.ask(36, 'Entrepreneurship is central to Ireland’s broad-based', ' Discuss two'))

# The paper's own data, shown beside the typed ask; a card whose figure slot holds
# its solution carries the whole printed question instead (see show_before_reveal).
for cid, fig in [('q11-a-i', 'p13-q11ai-question'), ('q13-a-i', 'p21-q13ai-question'),
                 ('q14-b-i', 'p26-q14bi-question'), ('q15-b-i', 'p30-q15bi-question'),
                 ('q16-a-i', 'p33-q16ai-question'), ('seca-q6-b', 'p08-q6b-question'),
                 ('q16-b-ii', 'p34-q16bii-question'), ('q16-b-ii-explanation', 'p34-q16bii-question')]:
    c = next(c for c in cards if c['id'] == D.prefix + cid)
    show_before_reveal(c, None, PAP + fig)


# Letter and number keys the earlier extractors shipped with these cards, kept
# as they were: the question names lettered or numbered items in its figure.
LABEL_KEYS = {
    'q9-a': [{'letter': '1', 'meaning': 'Marginal cost', 'askedInThisQuestion': True},
             {'letter': '2', 'meaning': 'Average revenue = Demand', 'askedInThisQuestion': True},
             {'letter': '3', 'meaning': 'Marginal revenue', 'askedInThisQuestion': True},
             {'letter': 'E', 'meaning': 'the equilibrium where marginal cost cuts marginal revenue',
              'askedInThisQuestion': False}],
    'q16-a-i': [{'letter': 'A', 'meaning': 'the missing Variable Cost cell, at an output of 20 smoothies',
                 'askedInThisQuestion': True},
                {'letter': 'B', 'meaning': 'the missing Average Cost cell, at an output of 60 smoothies',
                 'askedInThisQuestion': True}],
    'seca-q10-a': [{'letter': 'A', 'meaning': 'a point on the rising stretch of the cycle curve, before 2008',
                    'askedInThisQuestion': True},
                   {'letter': 'B', 'meaning': 'a point on the falling stretch of the cycle curve, after 2008',
                    'askedInThisQuestion': True}],
}
for c in cards:
    key = LABEL_KEYS.get(c['id'].removeprefix(D.prefix))
    if key:
        c['labelKey'] = key


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split seven required-heading responses into one card per
# heading. Each half is still emitted, lifted from its own heading, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('sa-q1-a-against', 'sa-q1-a-for', 'Argument against', '6',
     H.menu('Argument against:', '(b) Outline what you understand by the economic term cost', [5]), 6, 3, A),
    ('sa-q4-a-bad', 'sa-q4-a-good', 'Not beneficial for chocolate consumers', '6',
     H.menu('Not beneficial for chocolate consumers:', '11 | P a g e', [12]), 6, 6, A),
    ('sa-q4-b-cons', 'sa-q4-b-gov', 'One measure taken by consumers in Ireland', '6',
     H.menu('One measure taken by consumers in Ireland:', '13 | P a g e', [14]), 6, 6, A),
    ('q11-b-iii-dis', 'q11-b-iii-adv', 'Economic disadvantage for consumers', '4',
     H.menu('Economic Disadvantage for Consumers:', '27 | P a g e', [28]), 4, 15, {}),
    ('q12-a-ii-gov', 'q12-a-ii-tax', 'The Irish government', '7',
     H.menu('The Irish government:', '31 | P a g e', [32]), 7, 17, {}),
    ('q12-c-i-employer', 'q12-c-i-employee', 'Economic disadvantage to the employer', '7',
     H.menu('Economic Disadvantage to the Employer:', '36 | P a g e', [37]), 7, 20, {}),
    ('q13-a-ii-challenge', 'q13-a-ii-benefit', 'Economic challenge', '7',
     H.menu('Economic Challenge:', '39 | P a g e', [40]), 7, 21, {}),
]
for old, canonical, label, _, options, per, _page, section in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this heading is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'], figure=base.get('figureKey', '') if not base.get('questionFigureKey') else '')

if __name__ == '__main__':
    emit(cards)
