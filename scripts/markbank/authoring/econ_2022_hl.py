#!/usr/bin/env python3
"""Economics 2022 Higher Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2022-hl-ev.json,
made from a visual sweep of all 40 paper pages and 48 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID), and
the 75 routes are the ones the 2022 Higher Irish review mirrors task for task,
so the Irish attachment is unchanged.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). The scheme sets most
responses as a bullet list, so menus are split at the bullets; the living-wage
and Brexit lists are bold headings and are split where each heading begins. The
only prose written here is guidance: tariffs, route labels and what a figure or
a calculation shows. Scheme PDF page = printed page + 1.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, defurnish, emit, heads, point  # noqa: E402

H = Sheet(2022, 'higher', 'LC034ALP000EV')
D = Deck(2022, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2022-HL-scheme-'
PAP = 'economics-2022-HL-paper-'
EITHER = 'Answer either (b) or (c).'
DIAGRAM = 'Fully labelled diagram'


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return bullets(H.chunk(start, end, occ))


def at(start, end, firsts, occ=None):
    """Responses printed as headed paragraphs, split where each one begins."""
    return [as_option(o) for o in heads(H.chunk(start, end, occ), firsts)]


def line(start):
    """One whole line of the scheme file that opens with `start` (the recovered
    table cells keep a cell on one line where the primary extraction splits it
    around a tick)."""
    hits = [ln.strip() for ln in H.full_md.splitlines() if ln.strip().startswith(start)]
    if not hits:
        raise ValueError(f'no scheme line opens with {start!r}')
    return defurnish(hits[0])


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, note):
    """A required answer inside a jointly priced response."""
    return point(rid, paras(options), None, f'{label}. {note}')


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1 x 8, 1 x 4)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


def stance(prefix, choices, topic, q, parts, qtext, per, split, *, stem='', sa=False, figure=''):
    """A printed either/or choice whose scheme credits each side: one card per side."""
    for suffix, word, route, label, options, concept in choices:
        pick(f'{prefix}-{suffix}', topic, concept, ref(q, parts, route, sa=sa),
             f'{qtext} Answer for: {word.upper()}.', label, options, 1, per,
             f'One developed justification for the {word} side, {per} marks ({split}). The scheme '
             f'credits both sides; these are its examples, not a closed list.',
             stem=stem, figure=figure, **(A if sa else {}))


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ face masks: price elasticity; the law of demand
add('sa-q1-a', '1-4', 'price-elasticity-of-demand-off-a-demand-curve', ref(1, '(a)', sa=True),
    H.ask(3, 'Using an appropriate formula, calculate the price elasticity', ' DEMAND FOR'), '10', 10,
    [point('r-answer', '−3', 10,
           'PED = (ΔQD ÷ ΔP) × ((P1 + P2) ÷ (QD1 + QD2)) = (−4 ÷ +1) × ((4 + 5) ÷ (8 + 4)) = −3. '
           'The quantities 8 and 4 are read off the graph at €4 and €5. The complete calculation is '
           'worth 10 marks; the official working, with its fraction bars, is shown in the figure.')],
    figure=SOL + 'p05-q1a-working', **A)
add('sa-q1-b', '1-1', 'the-law-of-demand', ref(1, '(b)', sa=True),
    H.ask(3, 'With reference to the graph above explain the law of demand.', ' Leaving'), '5', 5,
    [point('r-1', H.run('The Law of Demand states that as the price', '2. (a) Using the data'), 5,
           'State the law, then show it on the graph, 5 marks: the price rises from €4 to €5 and the '
           'quantity demanded falls from 8 to 4.')],
    figure=PAP + 'p03-q1-graph', **A)

# Q2 ─ Quarterly National Accounts
q2_stem = H.ask(4, 'The infographic below shows the Quarterly National Accounts', ' www.cso.ie')
q2_fig = PAP + 'p04-q2-infographic'
add('seca-q2-a', '4-2', 'is-the-balance-of-payments-expansionary', ref(2, '(a)', sa=True),
    H.ask(4, 'Using the data above, explain whether the Balance of Payments', ' Expansionary:'), '9', 9,
    [point('r-1', H.run('Answer: Expansionary', '(b) Outline one factor which could'), 9,
           'Tick EXPANSIONARY and explain with the figures, 9 marks: exports grew 6.4% against 5.4% '
           'for imports, so the injection grew by more than the leakage.')],
    stem=q2_stem, figure=q2_fig, **A)
pick('sa-q2-b', '1-1', 'what-moves-personal-consumption', ref(2, '(b)', sa=True),
     H.ask(4, 'Outline one factor which could have influenced the above trend', ' Leaving'),
     'A factor behind the trend in personal consumption — any one',
     bl('• Pent up demand:', '4 | P a g e'),
     1, 6, 'One developed factor, 6 marks (3 + 3). Personal consumption grew 12.6% in the quarter.',
     stem=q2_stem, figure=q2_fig, **A)

# Q3 ─ minimum unit pricing of alcohol
q3_stem = H.ask(5, 'Minimum Unit Pricing (MUP) for alcohol was introduced', ' Adapted from')
stance('sa-q3-a', [
    ('agree', 'agree', 'agree', 'A reason to agree — any one',
     bl('• May combat alcohol abuse', 'I disagree with MUP:'), 'the-case-for-minimum-unit-pricing'),
    ('disagree', 'disagree', 'disagree', 'A reason to disagree — any one',
     bl('• It is inequitable', '(b) The purchase of alcohol'), 'the-case-against-minimum-unit-pricing')],
    '1-3', 3, '(a)', H.ask(5, 'Do you agree with this new MUP for alcohol?', ' Agree:') + ' '
    + H.ask(5, 'Justify your answer.', ' Justify:'), 9, '5 + 4', stem=q3_stem, sa=True)
add('sa-q3-b', '2-2', 'alcohol-and-market-failure', ref(3, '(b)', sa=True),
    H.ask(5, 'The purchase of alcohol in the free market may generate', ' Leaving'), '3 + 3', 6,
    [point('r-definition', H.run('Market failure occurs when the price mechanism',
                                 'The production of these goods may lead'), 3,
           'Explain market failure, 3 marks.'),
     point('r-example', H.run('The production of these goods may lead', '5 | P a g e'), 3,
           'Illustrate it from the alcohol market, 3 marks: harmful consumption and the healthcare '
           'cost borne by third parties.')],
    stem=q3_stem, **A)

# Q4 ─ the circular flow; foreign direct investment
q4a_ask = (H.ask(6, 'Categorise each of the following as either an injection', ' Injection Leakage')
           + ' 1. ' + H.ask(6, 'The Irish government increases public sector', ' 2.')
           + ' 2. ' + H.ask(6, 'Irish exports increase to record', ' 3.')
           + ' 3. ' + H.ask(6, 'Irish consumers saved more than', ' Answer either'))
add('seca-q4-a-ticks', '3-0', 'injections-and-leakages-in-the-circular-flow', ref(4, '(a)', sa=True),
    q4a_ask, '3 + 3 + 2', 8,
    [point('r-salaries', 'Injection — ' + line('The Irish government increases public sector'), None,
           'Government spending on pay is an INJECTION.'),
     point('r-exports', 'Injection — ' + line('Irish exports increase to record €160 bn despite'), None,
           'Exports are an INJECTION: money from outside the circular flow.'),
     point('r-saving', 'Leakage — ' + line('Irish consumers saved more than €10bn in'), None,
           'Saving is a LEAKAGE: income not spent. The scheme prices the three 3 + 3 + 2 without '
           'naming which row earns which; the completed table is shown in the figure.')],
    kind='questionTotal', figure=SOL + 'p07-q4a-ticks', **A)
q4b_reasons = bl('• Public sector salaries are a part of government', 'OR\n(c) Outline two reasons')
add('sa-q4-b', '3-0', 'injections-and-leakages-justified', ref(4, '(b)', sa=True),
    H.ask(6, 'In the box below justify each of your choices in part (a) above.', include_end=False,
          end=' 1. 2. 3.'), '3 + 2 + 2', 7,
    [point(f'r-{i}', option, None, note) for i, (option, note) in enumerate(zip(q4b_reasons, [
        'Justify the public-sector salaries row.', 'Justify the exports row.',
        'Justify the saving row. The scheme prices the three justifications 3 + 2 + 2, not a fixed '
        'value per row.']), 1)],
    kind='questionTotal', figure=PAP + 'p06-i0', notes=EITHER, **A)
add('sa-q4-c', '4-1', 'importance-of-foreign-direct-investment', ref(4, '(c)', sa=True),
    H.ask(6, 'Outline two reasons why inflows of foreign direct investment', ' 1. 2.'), '7', 7,
    [point('r-1', paras(bl('• Increased employment opportunities for Irish labour force',
                           '6 | P a g e')), None,
           'Give two reasons. These are the scheme’s examples, not three compulsory points. The '
           'scheme prints one 3 + 2 + 2 beside the (b) or (c) choice and no separate value for each '
           'FDI reason, so assess the complete response against its 7 marks.')],
    kind='questionTotal', notes=EITHER, **A)

# Q5 ─ the ageing population
q5_stem = H.ask(7, 'It is predicted that the number of people in Ireland aged over 65', ' Adapted from')
add('sa-q5-a', '3-5', 'why-the-population-is-ageing', ref(5, '(a)', sa=True),
    H.ask(7, 'Explain two factors which are likely to have influenced', ' 1. 2.'), '4 + 3', 7,
    [steps('r-1', 'A factor behind the ageing population — any two',
           bl('• Improvement in healthcare in Ireland', '(b) • Improved planning')
           + bl('• Improved planning by government', 'Answer either (b) or (c)\nOutline two economic'),
           4, 3, 'factors')],
    stem=q5_stem, **A)
pick('sa-q5-b', '2-1', 'economic-advantages-of-an-ageing-population', ref(5, '(b)', sa=True),
     H.ask(7, 'Outline two economic advantages of an ageing Irish population.', ' 1. 2.'),
     'An economic advantage of an ageing population — any two',
     bl('• Increased numbers may participate in the labour force', '7 | P a g e'),
     2, 4, 'Two advantages, 4 marks each. Answer either (b) or (c).', stem=q5_stem, **A)
add('sa-q5-c', '3-1', 'ageing-population-and-government-policy', ref(5, '(c)', sa=True),
    H.ask(7, 'Outline two impacts Ireland’s ageing population will have', ' 1. 2.'), '4 + 3', 7,
    [steps('r-1', 'An impact on government policy — any two',
           bl('• Increased spending on healthcare', '8 | P a g e'), 4, 3, 'impacts')],
    stem=q5_stem, notes=EITHER, **A)

# Q6 ─ perfect competition: two complete routes
q6_ask = H.ask(8, 'Firms in Perfect Competition are said to be Price-Takers.', ' The Market')
q6_rows = [
    point('r-diagrams', 'The Market The Firm', None,
          'Compare both labelled diagrams with the official solution: market supply shifts right '
          'from S1 to S2, and the firm’s horizontal D = AR = MR line falls from P1 to P2. The scheme '
          'prints 4, 2 and 2 beside (a) and no separate value beside (b) or (c), so the complete '
          'route is assessed against its 15 marks.'),
    point('r-market', H.run('Explanation for the market:', 'Explanation for the firm:'), None,
          'Explain the market diagram: supernormal profit attracts entry, supply shifts right, '
          'quantity rises and price falls.'),
    point('r-firm', H.run('Explanation for the firm:', '(b) Answer either (b) or (c)'), None,
          'Explain the firm diagram: a price-taker accepts the lower market price.')]
for suffix, part, concept, start, end, alt_start, alt_end in [
        ('b', '(b)', 'perfect-competition-complete-route-b', 'Firms can survive in the short run',
         ' Explanation:', '• In the short run if AR is greater than AVC', '(c) OR'),
        ('c', '(c)', 'perfect-competition-complete-route-c', 'In the long run only the most efficient',
         ' Explanation:', 'A firm is most efficient when it is producing', '9 | P a g e')]:
    add(f'sa-q6-a-{suffix}', '2-0', concept, ref(6, f'(a) and {part}', sa=True),
        q6_ask + ' ' + H.ask(9, start, end), '15', 15,
        q6_rows + [point('r-alternative', H.run(alt_start, alt_end), None,
                         f'Answer {part} as well as both diagrams and their explanations.')],
        kind='questionTotal', figure=SOL + 'p10-q6a-diagrams', **A)

# Q7 ─ the ECB rate
q7_stem = H.ask(10, 'Only one of the charts below accurately displays', ' Figure A:')
q7_fig = PAP + 'p10-art'
add('sa-q7-a-i', '3-3', 'which-chart-shows-the-real-ecb-rate-trend', ref(7, '(a)(i)', sa=True),
    H.ask(10, 'Identify which chart accurately displays the correct trend', ' Figure A: Figure B:'), '1', 1,
    [point('r-1', 'Figure B', 1,
           'Tick FIGURE B, 1 mark: the ECB rate fell after 2008 and sat at zero; Figure A has it '
           'rising through the 2010s. The scheme writes “2000 to 2021”; the paper says 2020.')],
    stem=q7_stem, figure=q7_fig, **A)
add('seca-q7-a-ii', '3-3', 'why-the-ecb-cut-rates-to-zero', ref(7, '(a)(ii)', sa=True),
    H.ask(10, 'Justify your choice in (i) above.', ' Justify:'), '2 x 4', 8,
    [point('r-1', H.run('In the wake of the global financial crisis', '(b) ⟨2 x 3⟩'), 8,
           'Two developed points, 4 marks each: WHAT the ECB did (cut its base rate gradually to '
           'zero after the 2007/2008 crisis) and WHY (to discourage saving and encourage borrowing, '
           'investment and growth).')],
    stem=q7_stem, figure=q7_fig, **A)
pick('sa-q7-b', '3-4', 'roles-of-the-european-central-bank', ref(7, '(b)', sa=True),
     H.ask(10, 'Other than setting the base % interest rate', ' 1. 2.'),
     'Another role of the ECB — any two', bl('• Ensure price stability:', '10 | P a g e'),
     2, 3, 'Two roles, 3 marks each. Setting the base rate is excluded by the question.', **A)

# Q8 ─ the hidden economy; supply chains
q8_stem = H.ask(11, 'Brexit and possible supply chain issues', ' Adapted from')
pick('sa-q8-a', '3-0', 'what-the-hidden-economy-is', ref(8, '(a)', sa=True),
     H.ask(11, 'Explain what is meant by the economic term hidden economy.', ' Explain:'),
     'The hidden economy — any wording',
     bl('• Hidden economic activity refers to', '(b) Outline two reasons for the supply chain'),
     1, 5, 'Explain the term, 5 marks; the scheme gives three wordings of the same idea.',
     stem=q8_stem, **A)
pick('sa-q8-b', '4-2', 'causes-of-supply-chain-disruption', ref(8, '(b)', sa=True),
     H.ask(11, 'Outline two reasons for the supply chain issues', ' 1. 2.'),
     'A reason for the supply chain issues — any two',
     bl('• Covid-19 impacts:', '9. (a)'),
     2, 5, 'Two reasons, 5 marks each (3 + 2). These are the scheme’s examples, not a closed list.',
     stem=q8_stem, **A)

# Q9 ─ solar panels
add('sa-q9-a', '2-2', 'private-costs-and-benefits', ref(9, '(a)', sa=True),
    H.ask(12, 'Identify one private cost and one private benefit', ' Private cost of'), '5 + 5', 10,
    [point('r-cost', H.run('The private cost of installing solar panels', 'A private benefit for the consumer'), 5,
           'The private cost, 5 marks.'),
     point('r-benefit', H.run('A private benefit for the consumer of installing', '(b) Installing solar panels'), 5,
           'The private benefit, 5 marks.')], **A)
add('sa-q9-b', '2-2', 'social-benefits-of-solar-panels', ref(9, '(b)', sa=True),
    H.ask(12, 'Installing solar panels also creates social benefits.', ' Leaving'), '5', 5,
    [point('r-1', H.run('Social benefits are benefits to society', '11 | P a g e'), 5,
           'Explain social benefits and apply them, 5 marks: less use of finite non-renewable '
           'resources and fewer harmful emissions.')], **A)

# Q10 ─ PepsiCo's production possibility frontier
q10_stem = H.ask(13, 'Cork based firm PepsiCo have 23 brands in total.', ' (a)')
q10_fig = PAP + 'p13-q10-data'
q10_oc = bl('• Tropicana decreases from 62 million litres', '(b)\nThe point X')
add('seca-q10-a', '0-1', 'opportunity-cost-along-the-ppf', ref(10, '(a)', sa=True),
    H.ask(13, 'Calculate the opportunity cost of PepsiCo moving production', ' Doritos') + ' '
    + H.ask(13, 'Answer: Explain your answer.', ' Explanation:')[len('Answer: '):], '6', 6,
    [point('r-1', paras([q10_oc[0], q10_oc[1].rstrip('3')]), 6,
           'Opportunity cost is what is given up, 6 marks: moving from D (50, 62) to H (90, 0), '
           'Tropicana falls from 62 million litres to 0, so the cost is 62 million litres of '
           'Tropicana. (The scheme’s trailing “3” is a footnote mark.)')],
    stem=q10_stem, figure=q10_fig, **A)
add('sa-q10-b', '0-1', 'producing-inside-the-frontier', ref(10, '(b)', sa=True),
    H.ask(13, 'The point X (20,20) is another production possibility', ' Answer:'), '9', 9,
    [point('r-1', H.run('No, as it can be seen as waste of resources.', '12 | P a g e'), 9,
           'Answer NO and explain, 9 marks: X lies inside the frontier, so resources are idle; at '
           '20 of either product the schedule allows about 80 of the other.')],
    stem=q10_stem, figure=q10_fig, **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ rents; land; the North Runway
q11_stem = H.ask(14, 'The infographic below shows data extracted from the Residential', ' www.rtb.ie')
add('q11-a-i', '1-1', 'regional-rent-disparity', ref(11, '(a)(i)'),
    H.ask(14, 'Outline two possible reasons for the disparity in average rents', ' 1. 2.'), '8 + 4', 12,
    [steps('r-1', 'A reason for the disparity in rents — any two',
           bl('• Greater population per sq. km in Dublin', '(ii) Outline two possible interventions'),
           8, 4, 'reasons')],
    stem=q11_stem, figure=PAP + 'p14-q11-infographic')
add('q11-a-ii', '3-5', 'balanced-regional-development', ref(11, '(a)(ii)'),
    H.ask(15, 'Outline two possible interventions the Irish government could pursue', ' (b)'), '8 + 4', 12,
    [steps('r-1', 'An intervention for balanced regional development — any two',
           bl('• Increased investment in industry in rural areas', '13 | P a g e'), 8, 4,
           'interventions')])
add('q11-b-i', '1-0', 'how-the-equilibrium-price-of-land-is-determined', ref(11, '(b)(i)'),
    H.ask(15, 'Explain, with the use of a fully labelled diagram how the equilibrium price of land',
          ' Explanation:'), '6 + 5', 11,
    [point('r-diagram', DIAGRAM, 6,
           'The diagram, 6 marks: Price and Quantity axes, a VERTICAL supply curve S (land is fixed '
           'in quantity), a downward-sloping demand curve D, and the equilibrium E at PE and QE. The '
           'official diagram is shown in the figure.'),
     point('r-explanation', H.run('The supply of land is fixed in quantity at S.', '(ii) Other than land'), 5,
           'The explanation, 5 marks: with supply fixed, the price is set where demand meets the '
           'vertical supply curve.')],
    figure=SOL + 'p15-q11bi-diagram')
pick('q11-b-ii', '1-2', 'characteristics-of-land', ref(11, '(b)(ii)'),
     H.ask(16, 'Other than land being fixed in supply, outline two characteristics', ' 1. 2.'),
     'A characteristic of land — any two',
     bl('• No cost of production to society', '(iii) Explain how the concept of derived'),
     2, 5, 'Two characteristics, 5 marks each. Fixed supply is excluded by the question.')
add('q11-b-iii', '1-1', 'derived-demand-and-land', ref(11, '(b)(iii)'),
    H.ask(16, 'Explain how the concept of derived demand relates', ' (c)'), '5', 5,
    [point('r-1', H.run('Derived demand states that a factor of production', '14 | P a g e'), 5,
           'Explain the concept and apply it, 5 marks: land is wanted for what it lets people '
           'produce, not for itself.')])
q11c_stem = H.ask(16, 'It is estimated the North Runway Project', ' Adapted from')
add('q11-c-i', '0-1', 'what-opportunity-cost-is', ref(11, '(c)(i)'),
    H.ask(16, 'Explain the term opportunity cost.', ' Leaving'), '8', 8,
    [point('r-1', H.run('Opportunity cost refers to the cost of foregone alternatives',
                        '(ii) Outline one opportunity cost involved'), 8,
           'Explain the term, 8 marks: the cost of the next best alternative forgone.')],
    stem=q11c_stem)
add('q11-c-ii', '0-1', 'opportunity-cost-of-transport-spending', ref(11, '(c)(ii)'),
    H.ask(17, 'Outline one opportunity cost involved in the above government expenditure', ' The loss'),
    '5', 5,
    [point('r-1', H.run('Example: spending forgone on building new hospitals',
                        '(iii) The Irish government should provide'), 5,
           'One opportunity cost with an example, 5 marks. The runway is capital spending, so the '
           'alternative forgone must be capital spending too, such as a hospital or a school.')],
    stem=q11c_stem)
add('q11-c-iii-for', '1-3', 'arguments-for-and-against-supporting-regional-airports', ref(11, '(c)(iii)'),
    H.ask(17, 'The Irish government should provide more financial support', ' Arguments for:'),
    '6 + 6', 12,
    [heading('r-for', 'An argument for — any one',
             bl('• Supports the government objective of balanced', 'Against financial support:'), 6,
             'Complete BOTH sides. One argument for, 6 marks (3 + 3).'),
     heading('r-against', 'An argument against — any one',
             bl('• Opportunity cost is funding for more developed', '15 | P a g e'), 6,
             'One argument against, 6 marks (3 + 3). The scheme prints the pair as 2 x 6 and adds '
             '“Must have a minimum of one argument either for or against”.')],
    stem=H.ask(17, 'The loss of the daily Dublin-Kerry regional airline service', ' Adapted from'))

# Q12 ─ electricity: concentration, deregulation, privatisation; data centres
q12a_stem = H.ask(18, 'The pie charts below show the market share of domestic electricity', ' MARKET SHARE')
q12_fig = PAP + 'p18-q12-charts'
q12a_points = bl('• In 2005 the HHI figure of 10,000', '(ii) Explain two reasons why a government')
add('q12-a-i', '2-0', 'what-a-falling-hhi-shows', ref(12, '(a)(i)'),
    H.ask(18, 'Comment on what the Herfindahl-Hirschman Index (HHI) results', ' (ii)'), '3 x 3', 9,
    [point(f'r-{i}', option, 3, note) for i, (option, note) in enumerate(zip(q12a_points, [
        '2005, 3 marks: an HHI of 10,000 is a monopoly, one producer.',
        '2019, 3 marks: the index has fallen to 3,328 as firms entered.',
        'The level, 3 marks: 3,328 is still above 2,500, so the market remains highly concentrated.'
    ]), 1)],
    stem=q12a_stem, figure=q12_fig)
pick('q12-a-ii', '2-0', 'reasons-to-deregulate', ref(12, '(a)(ii)'),
     H.ask(18, 'Explain two reasons why a government would decide to deregulate', ' 1.'),
     'A reason to deregulate — any two',
     bl('• Offer consumers more choice/larger quantity', '16 | P a g e'),
     2, 3, 'Two reasons, 3 marks each.', stem=q12a_stem)
add('q12-a-iii', '1-3', 'what-privatisation-is', ref(12, '(a)(iii)'),
    H.ask(19, 'Explain the term privatisation.', ' Explanation:'), '4', 4,
    [point('r-1', H.run('This is the sale of a state-owned company', '(iv) A government could choose'), 4,
           'Explain the term, 4 marks: a whole or partial sale of a state-owned company or asset to '
           'the private sector.')])
pick('q12-a-iv', '1-3', 'why-privatise-rather-than-deregulate', ref(12, '(a)(iv)'),
     H.ask(19, 'A government could choose privatisation of a semi-state body', ' Explanation:'),
     'A reason to privatise rather than deregulate — any one',
     bl('• Generates revenue for the Irish government', '(b)\n(i) The market structure'),
     1, 5, 'One developed reason, 5 marks (2 + 3).')
q12b1_ask = H.ask(19, 'The market structures in the pie charts in (i) above', ' Monopoly:')
for side, label, start, end, concept in [
        ('monopoly', 'Monopoly:', '• Economies of Scale', '17 | P a g e', 'advantages-of-a-state-monopoly'),
        ('oligopoly', 'Oligopoly:', '• Stability in prices / price comparability', '18 | P a g e',
         'advantages-of-an-oligopoly')]:
    pick(f'q12-b-i-{side}', '2-0', concept, ref(12, '(b)(i)', side), f'{q12b1_ask} {label}',
         f'An advantage of {side} — any one', bl(start, end), 1, 5,
         f'One developed advantage of {side}, 5 marks (2 + 3). The question asks for one of each '
         f'and the scheme prices each 5.', figure=q12_fig)
add('q12-b-ii', '2-0', 'long-run-equilibrium-of-a-monopoly', ref(12, '(b)(ii)'),
    H.ask(20, 'Explain, with the use of a fully labelled diagram, the long-run equilibrium', ' Explanation:'),
    '11 + 8', 19,
    [point('r-labels', H.run('1 mark per label = 11 marks', '• Equilibrium is at point E'), 11,
           'The diagram, 1 mark for each of the 11 labels: the two axes, P1, Q1, C1, E, D/AR, MR, MC, '
           'AC and the supernormal profit area. The official diagram is shown in the figure.'),
     point('r-explanation', H.run('• Equilibrium is at point E', '(iii) Explain two changes'), 8,
           'The explanation, 8 marks: equilibrium where MC = MR, output Q1 sold at P1 with costs at '
           'C1, supernormal profit because AR is above AC, and inefficiency because output is not at '
           'the lowest point of AC.')],
    figure=SOL + 'p20-q12bii-monopoly')
pick('q12-b-iii', '2-0', 'monopoly-versus-oligopoly', ref(12, '(b)(iii)'),
     H.ask(20, 'Explain two changes in market conditions', ' 1. 2.'),
     'A change in market conditions — any two',
     bl('• Number of firms in the market', '19 | P a g e'),
     2, 3, 'Two changes, 3 marks each.')
pick('q12-c-i', '0-2', 'challenges-of-a-carbon-neutral-motor-industry', ref(12, '(c)(i)'),
     H.ask(21, 'Outline two challenges which the Irish economy faces', ' 1. 2.'),
     'A challenge — any two', bl('• Prohibitive cost of electric cars.', '20 | P a g e'),
     2, 4, 'Two challenges, 4 marks each (2 + 2).',
     stem=H.ask(21, 'By 2030, there will be an estimated 500,000 electric vehicles', ' Adapted from'))
q12c2_stem = H.ask(21, 'Analysis has shown that demand for electricity from data centres', ' Adapted from')
q12c2_ask = H.ask(21, 'Discuss one reason why the Irish government should grant', ' Reason for:')
for side, label, route, start, end, concept in [
        ('for', 'Reason for:', 'for', '• Supports technological industry in Ireland',
         'Reasons against granting planning permission:', 'the-case-for-more-data-centres'),
        ('against', 'Reason against:', 'against', '• Electricity supply under pressure in Ireland',
         '21 | P a g e', 'the-case-against-more-data-centres')]:
    pick(f'q12-c-ii-{side}', '1-3', concept, ref(12, '(c)(ii)', route), f'{q12c2_ask} {label}',
         f'A reason {side} granting planning permission — any one', bl(start, end), 1, 4,
         f'One developed reason {side}, 4 marks (2 + 2). The question asks for one reason each way '
         f'and the scheme prices each 4.', stem=q12c2_stem)

# Q13 ─ government income and spending; behaviour; the 15% corporation tax
q13_stem = H.ask(22, 'The infographic below shows the sources of income and expenditure', ' www.cso.ie')
add('q13-a-i', '3-1', 'why-social-benefits-dominate-spending', ref(13, '(a)(i)'),
    H.ask(22, 'Using the infographic above, explain why social benefits', ' (ii)'), '5 + 4', 9,
    [heading('r-explanation', 'Why social benefits are such a high proportion — any one',
             bl('• It is part of the governments objectives', 'Example:'), 5,
             'Explain why social benefits, 37c of every euro spent, are so large a share, 5 marks.'),
     point('r-example', bl('• Payments such as unemployment benefit', '(ii) The Irish government uses both')[0], 4,
           'An example of a social benefit, 4 marks.')],
    stem=q13_stem, figure=PAP + 'p22-q13-infographic')
add('q13-a-ii', '3-1', 'direct-and-indirect-taxes', ref(13, '(a)(ii)'),
    H.ask(22, 'The Irish government uses both direct and indirect tax', ' Leaving'), '(6 + 2) + (6 + 2)', 16,
    [point('r-direct', H.run('Direct taxes are taxes placed upon income', 'Indirect taxes are taxes'), 8,
           'Direct tax: 6 for the distinction and 2 for an example.'),
     point('r-indirect', H.run('Indirect taxes are taxes placed on spending', '22 | P a g e'), 8,
           'Indirect tax: 6 for the distinction and 2 for an example.')])
q13b1_stem = H.ask(23, 'Governments can use incentives to encourage certain human behaviour', ' Outline one possible')
q13b1_ask = H.ask(23, 'Outline one possible incentive the government uses', ' Encourages:')
for side, label, route, start, end, concept, what in [
        ('incentive', 'Encourages:', 'incentive', '• Provision of a grant towards the purchase',
         'Discourages:', 'incentives-that-change-behaviour', 'an incentive that encourages'),
        ('tax', 'Discourages:', 'tax measure', '• Plastic bag tax', '(ii) Outline two interventions',
         'taxes-that-change-behaviour', 'a tax measure that discourages')]:
    pick(f'q13-b-i-{side}', '1-3', concept, ref(13, '(b)(i)', route), f'{q13b1_ask} {label}',
         f'{what[0].upper()}{what[1:]} — any one', bl(start, end), 1, 7,
         f'One {what.split(" ", 1)[1]}, with an example, 7 marks (4 + 3). The question asks for one of each and the '
         f'scheme prices each 7.', stem=q13b1_stem)
pick('q13-b-ii', '1-3', 'interventions-to-influence-behaviour', ref(13, '(b)(ii)'),
     H.ask(23, 'Outline two interventions, other than incentives/taxes', ' 1.'),
     'Another intervention — any two', bl('• Minimum prices such as the minimum unit price', '23 | P a g e'),
     2, 6, 'Two interventions, 6 marks each (3 + 3). Incentives and taxes are excluded by the question.')
q13c_stem = H.ask(24, 'The Irish Government has signed up to the Organisation', ' Adapted from')
pick('q13-c-i', '3-1', 'effects-of-the-15-percent-minimum-tax', ref(13, '(c)(i)'),
     H.ask(24, 'Outline the possible economic effects of this measure', ' Leaving'),
     'An economic effect of the measure — any two', bl('• Larger tax take for the Irish government', '24 | P a g e'),
     2, 8, 'Two effects, 8 marks each (4 + 4). The scheme lists gains and costs together.',
     stem=q13c_stem)
stance('q13-c-ii', [
    ('yes', 'yes', 'yes', 'A reason to impose it on all firms — any one',
     bl('• Greater tax revenue for Irish government', 'Against implementation:'),
     'taxing-all-firms-at-15-percent-for'),
    ('no', 'no', 'no', 'A reason not to impose it on all firms — any one',
     bl('• Infant industries.', '25 | P a g e'), 'taxing-all-firms-at-15-percent-against')],
    '3-1', 13, '(c)(ii)', H.ask(25, 'Should the Irish Government impose the new 15%', ' Yes: No:') + ' '
    + H.ask(25, 'Justify your answer.', ' 75 marks'), 8, '4 + 4', stem=q13c_stem)

# Q14 ─ building costs; cost table; gender pay gap; living wage
q14_stem = H.ask(26, 'The cost of building a house has risen by 30% in 2021.', ' Adapted from')
add('q14-a-i', '3-3', 'what-cost-push-inflation-is', ref(14, '(a)(i)'),
    H.ask(26, 'Explain the term cost push inflation with reference', ' Explanation:'), '3 + 3', 6,
    [point('r-definition', H.run('Cost push inflation refers to increases in the average price',
                                 'In the above example as the cost'), 3,
           'Explain the term, 3 marks.'),
     point('r-application', H.run('In the above example as the cost of housing', '(ii) Choose by means'), 3,
           'Relate it to the statement, 3 marks: dearer cement and timber pushing up house prices.')],
    stem=q14_stem)
add('q14-a-ii-ticks', '1-5', 'fixed-and-variable-building-costs', ref(14, '(a)(ii)'),
    H.ask(26, 'Choose by means of a tick', ' Building Expense') + ' '
    + H.clip(26, (58, 438, 182, 652)), '(2 + 4) x 3', 18,
    [point('r-cement', 'Variable cost — ' + line('As more output, houses, are produced more of the raw'), 6,
           'Bags of cement: tick VARIABLE, 2, and explain, 4.'),
     point('r-carpenters', 'Variable cost — ' + line('As more output, houses, are produced more of labour'), 6,
           'Carpenters: tick VARIABLE, 2, and explain, 4. The scheme also allows FIXED where the '
           'labour is on a fixed-price contract.'),
     point('r-site', 'Fixed cost — ' + line('Regardless of whether more or less houses'), 6,
           'The site: tick FIXED, 2, and explain, 4. The completed table is shown in the figure.')],
    figure=SOL + 'p27-q14aii-ticks')
q14b_stem = H.ask(27, 'The figures below represent the costs of building', ' Adapted from')
add('q14-b-i', '1-5', 'total-average-total-and-marginal-cost', ref(14, '(b)(i)'),
    H.ask(27, 'Calculate the missing figures for A, B, and C in the table below.', include_end=False,
          end=' Average'), '9', 9,
    [point('r-1', '€360,000 €200,000 €50,000', 9,
           'A: total cost = €100,000 + €260,000 = €360,000. B: average total cost = €400,000 ÷ 2 = '
           '€200,000. C: marginal cost = €450,000 − €400,000 = €50,000. The paper labels B average '
           'TOTAL cost; the official working, shown in the figure, labels it average variable cost in '
           'error although it divides total cost.')],
    stem=q14b_stem, figure=SOL + 'p28-q14bi-working')
add('q14-b-ii', '1-5', 'plotting-fixed-variable-and-total-costs', ref(14, '(b)(ii)'),
    H.ask(27, 'Using the figures obtained in the table above draw and label', ' Leaving'), '5 + 5 + 2 + 4', 16,
    [point('r-tc', 'Total Cost (€)', 5, 'Total cost, 5 marks: 360,000, 400,000, 450,000 and 505,000.'),
     point('r-vc', 'Variable Cost (€)', 5, 'Variable cost, 5 marks: 260,000, 300,000, 350,000 and 405,000.'),
     point('r-fc', 'Fixed Cost (€)', 2, 'Fixed cost, 2 marks: flat at 100,000.'),
     point('r-axes', 'Axes', 4,
           'Axes, 4 marks: costs against units of housing. Total cost runs €100,000 above variable '
           'cost at every output; the official graph is shown in the figure.')],
    stem=q14b_stem, figure=SOL + 'p28-q14bii-graph')
add('q14-b-iii', '1-5', 'profit-maximising-output', ref(14, '(b)(iii)'),
    H.ask(28, 'If the firm earns €55,000 for an additional unit', ' Answer:'), '5', 5,
    [point('r-1', H.run('The firm should produce 4 houses.', '27 | P a g e'), 5,
           'Answer 4 houses and explain, 5 marks: marginal cost equals marginal revenue at €55,000.')],
    stem=q14b_stem, figure=PAP + 'p27-i0')
q14c_stem = H.ask(28, 'The chart below shows the difference between average hourly earnings', ' Adapted from')
add('q14-c-i', '2-1', 'average-gender-wage-gap-across-five-countries', ref(14, '(c)(i)'),
    H.ask(28, 'Based upon the data above calculate the average gender wage gap', ' Calculations:'), '8', 8,
    [point('r-1', '21.7 + 19.2 + 14 + 11.3 + 1.3 = 67.5 ÷ 5 = 13.5', 8,
           'Add the five gaps and divide by five: 67.5 ÷ 5 = 13.5, 8 marks.')],
    stem=q14c_stem, figure=PAP + 'p28-q14c-chart')
pick('q14-c-ii', '2-1', 'why-a-gender-pay-gap-persists', ref(14, '(c)(ii)'),
     H.ask(29, 'Explain one reason why a gender pay gap persists', ' Explanation:'),
     'A reason the gap persists — any one', bl('• Discrimination in the workplace:', '28 | P a g e'),
     1, 5, 'One developed reason, 5 marks (2 + 3).')
q14c3_for = at('Introduce a more equitable distribution of income.', 'Arguments against:',
               ['Introduce a more equitable', 'Protection of the most vulnerable', 'Reduce problem of poverty.',
                'Increase worker’s standard of living.', 'Increase the incentive to work.',
                'Boost economic growth.'])
q14c3_against = at('Increases the cost of business.', '29 | P a g e',
                   ['Increases the cost of business.', 'Cost push inflation.',
                    'May lead to decreased employment.', 'May be a deterrent for FDI.'])
add('q14-c-iii', '2-1', 'arguments-for-and-against-a-living-wage', ref(14, '(c)(iii)'),
    H.ask(29, 'Discuss one argument for and one argument against', ' For:'), '4 + 4', 8,
    [heading('r-for', 'An argument for — any one', q14c3_for, 4,
             'Complete BOTH sides. One argument for, 4 marks (2 + 2).'),
     heading('r-against', 'An argument against — any one', q14c3_against, 4,
             'One argument against, 4 marks (2 + 2).')],
    stem=H.ask(29, 'In Budget 2022 the national minimum wage increased', ' Adapted from'))

# Q15 ─ milk; exchange rates and Brexit; the EU budget
q15_stem = H.ask(30, 'The chart below shows the evolution of Irish milk production', ' Evolution')
q15_fig = PAP + 'p30-q15a-chart'
pick('q15-a-i', '1-2', 'reading-trends-in-irish-milk-production', ref(15, '(a)(i)'),
     H.ask(30, 'Analyse two key trends in Irish milk production', ' (ii)'),
     'A key trend — any two',
     bl('• Rapid increase in milk production from approximately 3,200', '(ii) Explain each of the following'),
     2, 4, 'Two trends with figures, 4 marks each (2 + 2).', stem=q15_stem, figure=q15_fig)
add('q15-a-ii', '1-3', 'subsidy-and-quota', ref(15, '(a)(ii)'),
    H.ask(30, 'Explain each of the following economic terms', ' Subsidy:'), '2 x 4', 8,
    [point('r-subsidy', H.run('Subsidy: is a payment from the government', 'Quota: is a maximum'), 4,
           'Subsidy, 4 marks.'),
     point('r-quota', H.run('Quota: is a maximum limit imposed', '30 | P a g e'), 4,
           'Quota, 4 marks. Both terms are asked.')],
    stem=q15_stem, figure=q15_fig)
add('q15-a-iii', '1-0', 'how-grant-aid-shifts-the-supply-of-milk', ref(15, '(a)(iii)'),
    H.ask(31, 'Explain, with the use of a fully labelled diagram below', ' Explanation:'), '9 + 5', 14,
    [point('r-diagram', DIAGRAM, 9,
           'The diagram, 9 marks: label both axes, D1, S1, S2, the equilibria EA and EB, prices P1 '
           'and P2 and quantities Q1 and Q2. Supply shifts right; price falls and quantity rises. The '
           'official diagram is shown in the figure.'),
     point('r-explanation', H.run('• This grant should help reduce costs', '31 | P a g e'), 5,
           'The explanation, 5 marks: the grant cuts costs, so supply shifts right from S1 to S2, '
           'the price falls from P1 to P2 and the quantity rises from Q1 to Q2.')],
    stem=H.ask(31, 'Grant aid of €395m was provided to Irish farmers', ' Adapted from'),
    figure=SOL + 'p32-q15aiii-subsidy')
q15b_stem = H.ask(32, 'The graph below shows the Euro (€) to Pound Sterling', ' Euro (€) to Pound')
q15b_fig = PAP + 'p32-q15b-chart'
pick('q15-b-i', '4-2', 'spotting-a-depreciating-euro-on-a-chart', ref(15, '(b)(i)'),
     H.ask(32, 'Identify one period where the value of the Euro depreciates', ' Answer:'),
     'A period when the euro depreciates — any one',
     [o.split(' declines from')[0] for o in at(
         'During the period December 2013 to December 2015.', 'Apart from the change in exchange',
         ['During the period December 2013', 'During the period December 2018',
          'During the period December 2020'])],
     1, 8,
     'Name one period and explain the depreciation (4 + 4). Interpret the values as pounds per €1 '
     '(£/€), as the scheme explanation does: €1 buys fewer pounds as the line falls; the paper prints '
     '€/£ on the axis. For example, December 2013 to December 2015 falls from about £0.83 to £0.74 '
     'per euro (83p to 74p). The scheme’s “0.80 pence” wording is incorrect: 0.80 pounds is 80 '
     'pence. The listed periods are examples from the graph, not a closed list.',
     stem=q15b_stem, figure=q15b_fig)
pick('q15-b-ii', '4-2', 'brexit-and-irish-uk-trade', ref(15, '(b)(ii)'),
     H.ask(32, 'Apart from the change in exchange rates between the two currencies', ' 1. 2.'),
     'Another impact of Brexit on UK-Irish trade — any two',
     at('Possible negative effect on Irish exports.', '(iii) Explain how a knowledge',
        ['Possible negative effect on Irish exports.', 'Effects on agricultural sector',
         'Labour market effects.', 'Imports from the UK.', 'Relocation of U.K. based firms.',
         'Instability in Northern Ireland.']),
     2, 7, 'Two impacts, 7 marks each (4 + 3).', stem=q15b_stem, figure=q15b_fig)
add('q15-b-iii', '1-4', 'using-ped-to-set-an-export-price', ref(15, '(b)(iii)'),
    H.ask(33, 'Explain how a knowledge of price elasticity of demand', ' Explanation:'), '6', 6,
    [point('r-1', paras(bl('• A knowledge of Price Elasticity of Demand', '33 | P a g e')), 6,
           'Explain, 6 marks: where UK demand is more elastic, a lower price raises total revenue; '
           'where it is less elastic, a higher price does.')])
q15c_stem = H.ask(33, 'The graph below shows the countries which were net beneficiaries', ' Net Beneficiaries')
q15c_fig = PAP + 'p33-q15c-chart'
add('q15-c-i', '4-2', 'the-eus-largest-contributor-and-beneficiary', ref(15, '(c)(i)'),
    H.ask(33, 'Using the data in the graph above, name the country', ' EU’s largest Contributor:'), '7', 7,
    [point('r-contributor', 'Largest EU Contributor: GERMANY', None,
           'Germany: the deepest bar below zero (net contributor).'),
     point('r-beneficiary', 'Largest EU Beneficiary: POLAND', None,
           'Poland: the tallest bar above zero. The scheme prices the two together as 4 + 3, the '
           'first correct answer 4 and the second 3.')],
    kind='questionTotal', stem=q15c_stem, figure=q15c_fig)
pick('q15-c-ii', '4-1', 'why-net-contributors-stay-in-the-eu', ref(15, '(c)(ii)'),
     H.ask(34, 'Justify why countries such as Germany, France, Italy', ' Justify:'),
     'A reason a net contributor stays — any two',
     bl('• Free Trade Area / larger market', '35 | P a g e'),
     2, 5, 'Two reasons, 5 marks each (2 + 3).', stem=q15c_stem, figure=q15c_fig)

# Q16 ─ rent caps; environmental sustainability; fast fashion
q16a_stem = H.ask(35, 'Rent increases in so-called rent pressure zones', ' Adapted from')
add('q16-a-i', '0-2', 'rent-caps-and-social-sustainability', ref(16, '(a)(i)'),
    H.ask(35, 'What are the likely impacts of this government intervention', ' (ii)'), '8 + 4', 12,
    [steps('r-1', 'An impact on social sustainability — any two',
           bl('• Reduced homelessness.', '36 | P a g e'), 8, 4, 'impacts')],
    stem=q16a_stem)
add('q16-a-ii', '1-3', 'interventions-for-housing-access', ref(16, '(a)(ii)'),
    H.ask(35, 'Other than rent caps, suggest two other government interventions', ' Intervention 1:'),
    '8 + 4', 12,
    [steps('r-1', 'Another intervention — any two',
           bl('• Improved access to social housing.', '(b) The UN Secretary-General'), 8, 4,
           'interventions')],
    stem=q16a_stem)
q16b_stem = H.ask(36, 'The UN Secretary-General said the Working Group', ' Adapted from')
pick('q16-b-i', '0-2', 'why-environmental-sustainability-matters', ref(16, '(b)(i)'),
     H.ask(36, 'Outline the importance of environmental sustainability', ' (ii)'),
     'Why environmental sustainability matters — any one', bl('• Threat to human life', '37 | P a g e'),
     1, 7, 'One developed point, 7 marks (4 + 3).', stem=q16b_stem)
q16b2_ask = H.ask(36, 'Suggest strategies that could be employed', ' Irish Government:')
for cid, actor, label, start, end, concept in [
        ('q16-b-ii', 'Irish government', 'Irish Government:', '• Increased incentives to purchase electric',
         'Citizens:', 'low-carbon-strategy-government'),
        ('q16-b-ii-citizens', 'Irish citizens', 'Irish Citizens:', '• More ethically aware consumption',
         '38 | P a g e', 'low-carbon-strategy-citizens')]:
    pick(cid, '0-2', concept, ref(16, '(b)(ii)', actor), f'{q16b2_ask} {label}',
         f'A strategy for {actor} — any one', bl(start, end), 1, 7,
         f'One developed strategy for {actor}, 7 marks (4 + 3). The question asks for both actors and '
         f'the scheme prices each 7.', stem=q16b_stem)
q16c_stem = H.ask(37, 'The fashion industry produces 10%', ' Adapted from')
add('q16-c-i', '1-3', 'minimum-pricing-on-fast-fashion', ref(16, '(c)(i)'),
    H.ask(37, 'Explain, with the use of a fully labelled diagram, how the introduction', ' Explanation:'),
    '10 + 5', 15,
    [point('r-diagram', DIAGRAM, 10,
           'The diagram, 10 marks: place Pmin above the equilibrium price PE, mark QD and QS at the '
           'minimum price with the surplus between them, the original equilibrium E and QE, both '
           'curves and both axes. The official diagram is shown in the figure.'),
     point('r-effects', H.run('Effect on price', '(ii) Outline two steps consumers'), 5,
           'The effects, 5 marks: price rises from PE to Pmin, quantity demanded falls from QE to QD '
           'and quantity supplied rises to QS, leaving a surplus. The scheme’s “fall in demand” is a '
           'fall in quantity demanded, a movement along the curve.')],
    stem=q16c_stem, figure=SOL + 'p40-q16ci-minimum-price')
pick('q16-c-ii', '0-2', 'consumer-steps-on-fast-fashion', ref(16, '(c)(ii)'),
     H.ask(38, 'Outline two steps consumers in Ireland can take', ' 1. 2.'),
     'A step consumers can take — any two',
     bl('• Ethical consumption of goods/Research the product.', '(iii) Outline one step businesses'),
     2, 5, 'Two steps, 5 marks each (2 + 3).', stem=q16c_stem)
pick('q16-c-iii', '0-2', 'how-business-can-curb-fast-fashion', ref(16, '(c)(iii)'),
     H.ask(38, 'Outline one step businesses in Ireland can take', ' Businesses in Ireland:'),
     'A step businesses can take — any one',
     bl('• Alterations to production methods.', '40 | P a g e'),
     1, 5, 'One developed step, 5 marks (2 + 3).', stem=q16c_stem)

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('sa-q1-a', 'p03-q1a-question'), ('seca-q4-a-ticks', 'p06-q4a-question'),
                 ('q14-a-ii-ticks', 'p26-q14aii-question'), ('q14-b-i', 'p27-q14b-question'),
                 ('q14-b-ii', 'p27-q14b-question'), ('q15-a-iii', 'p31-q15aiii-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split two jointly priced answers into one card per
# part. Each half is still emitted, lifted from its own part, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('sa-q6-a-i', 'sa-q6-a-b', 'The market diagram and its explanation',
     [H.run('Explanation for the market:', 'Explanation for the firm:')], 4),
    ('sa-q6-a-ii', 'sa-q6-a-b', 'The firm diagram and its explanation',
     [H.run('Explanation for the firm:', '(b) Answer either (b) or (c)')], 4),
    ('q11-c-iii-against', 'q11-c-iii-for', 'An argument against',
     bl('• Opportunity cost is funding for more developed', '15 | P a g e'), 6),
]
for old, canonical, label, options, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this part is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
