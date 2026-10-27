#!/usr/bin/env python3
"""Economics 2023 Higher Level, Sections A and B.

Re-authored from the independent census in drafts/economics-2023-hl-ev.json,
made from a visual sweep of all 40 paper pages and 44 scheme pages. Every card
ID the earlier extractors shipped is kept (student progress follows the ID).
The census differs from the earlier one in one place: Q16(a)(i) (individual and
market demand, 4 + 4) is its own task, no longer joined to the Q16(a)(ii)
diagram; the 2023 Higher Irish review mirrors that route change only.

Question wording and stems are sliced from the question paper; every marking
point is sliced from the scheme (econ_2026_lib.py). The only prose written here
is guidance: tariffs, route labels and what a figure or a calculation shows.
Scheme PDF page = printed page + 2.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_2026_lib import Deck, Sheet, show_before_reveal  # noqa: E402
from econ_lib import anyN, as_option, bullets, emit, heads, point, tidy  # noqa: E402

H = Sheet(2023, 'higher', 'LC034ALP000EV')
D = Deck(2023, 'higher')
cards, add, pick, heading, ref = D.cards, D.add, D.pick, D.heading, D.ref
A = dict(section='A')
SOL = 'economics-2023-HL-scheme-'
PAP = 'economics-2023-HL-paper-'


def bl(start, end, occ=None):
    """The scheme's bullet-listed responses between two anchors."""
    return bullets(H.chunk(start, end, occ))


def at(start, end, firsts, occ=None):
    """Responses printed without bullets, split where each one begins."""
    return [as_option(o) for o in heads(H.chunk(start, end, occ), firsts)]


def at_columns(start, end, firsts, occ=None):
    """As at(), from the scheme's recovered column runs (a two-column table the
    primary extraction interleaves line by line; the provenance gate searches the
    column-runs block too)."""
    from econ_lib import block
    return [as_option(o) for o in heads(block(H.full_md, start, end, occ), firsts)]


def bl_full(start, end, occ=None):
    """As bl(), from the whole scheme file: the appended blocks keep a run whole where
    the primary extraction interleaves a part marker into it."""
    from econ_lib import block
    return bullets(block(H.full_md, start, end, occ))


def paras(options):
    """A list of the scheme's examples printed as one marking point."""
    return '\n\n'.join(options)


def shared(rid, label, options, note):
    """A required heading inside a jointly priced answer (1st @ n, 2nd @ m)."""
    return point(rid, paras(options), None, f'{label}. {note}')


def steps(rid, label, options, first, second, what):
    """Two responses paid first-then-second (1st @ 5, 2nd @ 4)."""
    return anyN(rid, label, None, 2, first, options,
                f'Two {what}: the first correct one {first} marks and the second {second}.',
                steps=[first, second])


def stance(prefix, choices, topic, q, parts, qtext, per, *, stem=''):
    """A printed tick-box choice whose scheme credits each side: one card per side."""
    for cid, word, label, options, concept in choices:
        pick(cid, topic, concept, ref(q, parts, word),
             f'{qtext} Answer for: {word.upper()}.', label, options, 1, per,
             f'One developed justification for the {word} choice, {per} marks. The scheme credits '
             f'both choices; these are its examples, not a closed list.', stem=stem)


# ═════════════════════════════════ SECTION A ══════════════════════════════════

# Q1 ─ Rugby World Cup tickets
q1_stem = H.ask(3, 'France will host the Rugby World Cup in 2023.', ' Explain, with')
add('sa-q1-a', '1-2', 'supply-of-a-fixed-capacity-good', ref(1, '(a)', sa=True),
    H.ask(3, 'Explain, with the aid of a fully labelled diagram', ' Diagram Explanation'), '3 + 3', 6,
    [point('r-diagram', 'It is perfectly inelastic or vertical', 3,
           'Diagram, 3 marks: label Price and Quantity and draw the supply curve S as a VERTICAL '
           'line at the fixed number of seats. The official diagram is shown in the figure.'),
     heading('r-explanation', 'The fixed supply of tickets',
             bl('• Regardless of price, the quantity of seats', '(b) Explain two conditions'), 3,
             'Explanation, 3 marks: the venues hold a fixed number, so supply does not respond to '
             'price.')],
    stem=q1_stem, figure=SOL + 'p05-q1a-supply', **A)
pick('sa-q1-b', '2-0', 'conditions-for-price-discrimination-2023', ref(1, '(b)', sa=True),
     H.ask(3, 'Explain two conditions necessary for price discrimination', ' 1. 2.'),
     'A condition for price discrimination — any two',
     at('Consumer ignorance:', '3 | P a g e',
        ['Consumer ignorance:', 'Consumer indifference:', 'Consumer attitudes:', 'Monopoly power:',
         'Different price elasticities of demand:', 'Market separation:']),
     2, 3, 'Two conditions, 3 marks each.', stem=q1_stem, **A)

# Q2 ─ petrol price; elasticity; excise duty
q2_stem = H.ask(4, 'On the 3rd of March, 2022', ' Adapted from')
add('sa-q2-a', '1-4', 'why-petrol-demand-is-inelastic', ref(2, '(a)', sa=True),
    H.ask(4, 'Select, using a tick', ' Price elastic: Price inelastic:'), '1 + 5', 6,
    [point('r-choice', 'Price inelastic', 1, 'Tick PRICE INELASTIC, 1 mark.'),
     heading('r-explanation', 'Why petrol demand is price inelastic',
             bl('• Petrol has price inelastic demand', 'Answer (b) or (c)', occ=0), 5,
             'Explain, 5 marks.')],
    stem=q2_stem, **A)
pick('sa-q2-b', '1-4', 'why-retailers-need-elasticity', ref(2, '(b)', sa=True),
     H.ask(4, 'Outline two reasons why it is important for retailers', ' 1. 2.'),
     'A reason retailers need to understand PED — any two',
     bl('• They will know by how much quantity demanded', '(c) OR'),
     2, 3, 'Two reasons, 3 marks each. Answer either (b) or (c).', stem=q2_stem, **A)
q2c_adv = bl('• Cost of Living Crisis:', 'Disadvantages')
q2c_dis = bl('• Government revenue:', '5 | P a g e')
add('sa-q2-c-adv', '3-1', 'not-raising-excise-duty-advantage-and-disadvantage', ref(2, '(c)', sa=True),
    H.ask(4, 'Outline one advantage and one disadvantage for the Irish economy', ' Advantage:'),
    '2 @ 3', 6,
    [heading('r-advantage', 'Advantage', q2c_adv, 3, 'Complete BOTH headings. One advantage, 3 marks.'),
     heading('r-disadvantage', 'Disadvantage', q2c_dis, 3, 'One disadvantage, 3 marks.')],
    stem=q2_stem, notes='Answer either (b) or (c).', **A)

# Q3 ─ utility
add('sa-q3-a', '1-1', 'filling-in-total-and-marginal-utility', ref(3, '(a)', sa=True),
    H.ask(5, 'Complete the missing total utility and marginal utility figures', ' Number of units'), '6', 6,
    [point('r-answer', H.run('• 80 – 40 = 40', 'Answer (b) or (c)'), 6,
           'Marginal utility is the change in total utility: MU of the 2nd unit = 80 − 40 = 40; TU '
           'of the 3rd = 80 + 35 = 115; MU of the 4th = 137 − 115 = 22. The scheme gives 6 for the '
           'three cells and workings; the completed table is shown in the figure.')],
    figure=SOL + 'p08-q3a-working', **A)
add('sa-q3-b', '1-1', 'where-diminishing-marginal-utility-sets-in', ref(3, '(b)', sa=True),
    H.ask(5, 'Based upon the marginal utility figures calculated above', ' Answer:'), '6', 6,
    [point('r-1', H.run('• Answer: on the consumption of the third unit', 'OR\n(c) Does the formula'), 6,
           'Answer and explain, 6 marks: marginal utility first FALLS on the third unit, from 40 to '
           '35 utils. Answer either (b) or (c).')],
    figure=PAP + 'p05-i0', **A)
add('seca-q3-c', '1-1', 'testing-the-equi-marginal-principle', ref(3, '(c)', sa=True),
    H.ask(5, 'Does the formula below obey the Equi', 'Explain your answer.', include_end=True), '6', 6,
    [point('r-1', H.run('• No, because:', '6 | P a g e'), 6,
           'Answer NO and explain, 6 marks: MUx ÷ Px = 1800 ÷ 10 = 180 and MUy ÷ Py = 3600 ÷ 10 = '
           '360. The principle needs marginal utility per euro to be EQUAL across goods; 180 is not '
           '360. Answer either (b) or (c).')],
    figure=PAP + 'p05-q3c-formula', **A)

# Q4 ─ costs
q4_stem = H.ask(6, 'The table below shows the output and total costs in a firm.', ' (a)')
add('sa-q4-a', '1-5', 'filling-in-average-and-marginal-cost', ref(4, '(a)', sa=True),
    H.ask(6, 'Complete the missing average cost and marginal cost figures', ' Output'), '6', 6,
    [point('r-answer', H.run('• 82 ÷ 2 = 41', 'Answer (b) or (c)'), 6,
           'Average cost = total cost ÷ output; marginal cost = the change in total cost. AC at 2 = '
           '82 ÷ 2 = 41; MC at 3 = 108 − 82 = 26; AC at 4 = 152 ÷ 4 = 38; MC at 4 = 152 − 108 = 44. '
           'The scheme gives 6 for the table; the completed table is shown in the figure.')],
    stem=q4_stem, figure=SOL + 'p09-q4a-table', **A)
add('sa-q4-b', '1-5', 'covering-costs-in-the-short-run', ref(4, '(b)', sa=True),
    H.ask(6, 'To remain in production, in the short run', ' Agree:') + ' Explain your answer.', '6', 6,
    [point('r-1', H.run('In the short run a firm must cover its average variable costs', 'OR\n(c) Explain the relationship'), 6,
           'Tick DISAGREE: the scheme credits no agree answer. Explain, 6 marks for the choice and '
           'its explanation together: in the short run only AVERAGE VARIABLE costs must be covered. '
           'Answer either (b) or (c).')],
    **A)
add('sa-q4-c', '1-5', 'marginal-cost-and-average-cost', ref(4, '(c)', sa=True),
    H.ask(6, 'Explain the relationship between the Marginal Cost Curve', ' Explanation:'), '6', 6,
    [point('r-1', H.run('• When Marginal Cost is greater than Average Cost', '7 | P a g e'), 6,
           'All three relationships, 6 marks: MC above AC, AC rising; MC below AC, AC falling; MC '
           'equal to AC, AC at its minimum. Answer either (b) or (c).')],
    **A)

# Q5 ─ production possibilities frontier
add('sa-q5-a', '0-1', 'reading-a-production-frontier', ref(5, '(a)', sa=True),
    H.ask(7, 'The diagram below shows the Production Possibilities Frontier', ' Laptops') + ' '
    + H.ask(7, 'Identify from the diagram above which option', ' Choose one letter'), '6', 6,
    [point('r-1', 'Efficient Production Point C', None, 'Efficient: C, on the frontier.'),
     point('r-2', 'Inefficient Production Point A', None, 'Inefficient: A, inside the frontier.'),
     point('r-3', 'Impossible Production Point B', None,
           'Impossible: B, outside the frontier. The scheme gives one 6 for the three letters.')],
    kind='questionTotal', figure=PAP + 'p07-art', **A)
add('sa-q5-b', '0-1', 'efficient-inefficient-and-impossible-points', ref(5, '(b)', sa=True),
    H.ask(7, 'Justify each of your choices you made in (a) above.', ' Efficient:'), '6', 6,
    [point('r-1', paras(bl('• Efficient refers to a production point', '8 | P a g e')), 6,
           'Justify all three, 6 marks overall: on the frontier, inside it, outside it.')],
    stem=H.ask(7, 'The diagram below shows the Production Possibilities Frontier', ' Laptops'),
    figure=PAP + 'p07-art', **A)

# Q6 ─ taxation
add('seca-q6-a', '3-1', 'sorting-taxes-direct-and-indirect', ref(6, '(a)', sa=True),
    H.ask(8, 'In each case below, indicate by placing a tick', ' Tax Direct Tax') + ' VAT; PAYE; '
    'Customs and Excise Duty.', '6', 6,
    [point('r-1', H.run('Tax Direct Tax Indirect Tax', '(b) Outline three canons'), 6,
           'VAT: INDIRECT; PAYE: DIRECT; Customs and Excise Duty: INDIRECT. The scheme gives 6 for '
           'the three ticks; the completed table is shown in the figure.')],
    figure=SOL + 'p11-q6a-ticks', **A)
add('sa-q6-b', '3-1', 'canons-of-taxation', ref(6, '(b)', sa=True),
    H.ask(8, 'Outline three canons/principles of taxation', ' 1. 2. 3.'), '6', 6,
    [point('r-1', paras(bl('• Certainty: it should be clear', '9 | P a g e')), 6,
           'Three canons, 6 marks overall, with no published split per canon; these are the '
           'scheme’s examples.')], **A)

# Q7 ─ rental market; vacant property tax
add('sa-q7-a', '1-0', 'landlords-leaving-and-the-rental-market', ref(7, '(a)', sa=True),
    H.ask(9, 'Show on the diagram below how this development', ' S Explanation:'), '3 + 3', 6,
    [point('r-diagram', 'S1', 3,
           'Diagram, 3 marks: shift supply LEFT from S to S1; the equilibrium price rises from Pe to '
           'Pe1 and the quantity falls from Qe to Qe1. The official diagram is shown in the figure.'),
     point('r-explanation', H.run('• As landlords leave the market', '(b) The introduction of the vacant'), 3,
           'Explain, 3 marks: fewer landlords means fewer rental properties supplied, so the '
           'equilibrium rent rises. The scheme’s bullets name the curves S1 to S2 and Pe1 to Pe2; '
           'its diagram labels them S to S1 and Pe to Pe1.')],
    stem=H.ask(9, 'Landlords are leaving the Irish housing market', ' Adapted from'),
    figure=SOL + 'p12-q7a-rental', **A)
add('sa-q7-b', '1-3', 'why-a-vacant-property-tax', ref(7, '(b)', sa=True),
    H.ask(9, 'Outline two reasons why the Irish government introduced this vacant', ' 1. 2.'), '6', 6,
    [point('r-1', paras(bl('• Increased government revenue to help', '10 | P a g e')), 6,
           'Two reasons, 6 marks overall, with no published split; these are the scheme’s '
           'examples.')],
    stem=H.ask(9, 'The introduction of the vacant property tax', ' Outline two'), **A)

# Q8 ─ ECB interest rates
q8_stem = H.ask(10, 'Eurozone interest rates increased four times', ' Adapted from')
add('sa-q8-a', '3-3', 'why-the-ecb-raised-interest-rates', ref(8, '(a)', sa=True),
    H.ask(10, 'Justify why the European Central Bank', ' (b)'), '6', 6,
    [point('r-1', H.run('• The European Central Bank (ECB) made this monetary policy decision', '(b) Does being'), 6,
           'Justify, 6 marks: to combat inflation / the cost-of-living crisis.')],
    stem=q8_stem, **A)
pick('sa-q8-b', '3-3', 'eurozone-membership-and-monetary-policy', ref(8, '(b)', sa=True),
     H.ask(10, 'Does being a member of the Eurozone affect', ' Yes:') + ' Explain your answer.',
     'A way membership constrains Irish monetary policy — any one',
     bl('• Ireland doesn’t have sovereignty', '9. China, is the world'),
     1, 6, 'Tick YES: the scheme credits no no answer. One explanation, 6 marks for the choice and '
     'its explanation together.', stem=q8_stem, **A)

# Q9 ─ diminishing returns; specialisation
q9_stem = H.ask(11, 'China is the world’s powerhouse', ' Adapted from')
add('sa-q9-a', '1-5', 'law-of-diminishing-marginal-returns', ref(9, '(a)', sa=True),
    H.ask(11, 'Explain the economic concept of the law of diminishing marginal returns.', ' Explanation:'),
    '6', 6,
    [point('r-1', H.run('The law of diminishing marginal returns states', '(b) Harvard Kennedy School'), 6,
           'Explain the law, 6 marks.')],
    stem=q9_stem, **A)
add('sa-q9-b', '1-5', 'cost-advantages-of-specialisation', ref(9, '(b)', sa=True),
    H.ask(11, 'Outline two cost advantages China’s firms experience', ' 1. 2.'), '6', 6,
    [point('r-1', paras(bl('• The firm’s marginal / average cost will fall', '11 | P a g e')), 6,
           'Two cost advantages, 6 marks overall, with no published split; these are the scheme’s '
           'examples.')],
    stem=H.ask(11, 'Harvard Kennedy School suggests', ' Adapted from'), **A)

# Q10 ─ national accounts ladder (B and C are separately priced, 2 @ 6)
q10_stem = H.ask(12, 'The data below has been adapted from Ireland’s National Accounts', ' Description')
q10_ask = H.ask(12, 'Given that Gross Domestic Product (GDP) at Current Market Prices (CMP) was',
                ' Relationships / Workings Answer')
add('sa-q10', '3-0', 'calculate-gni', ref(10, '(B)', sa=True),
    q10_ask + ' Answer for: B = Gross National Income at Current Market Prices.', '6', 6,
    [point('r-calculation', H.run('Gross National Product (GNP) at Current Market Prices: €323bn',
                                  'Relationships / Workings:\nGross National Income at Current Market Prices: €324.2 bn'), 6,
           'B: GNI = GNP + EU subsidies − EU taxes = €323bn + €1.7bn − €0.5bn = €324.2bn, 6 marks.')],
    stem=q10_stem, figure=PAP + 'p12-q10-question', **A)
add('sa-q10-c', '3-0', 'calculate-modified-gni', ref(10, '(C)', sa=True),
    q10_ask + ' Answer for: C = Modified Gross National Income at Current Market Prices.', '6', 6,
    [point('r-calculation', H.run('Gross National Income at Current Market Prices: €324.2 bn', '12 | P a g e'), 6,
           'C: modified GNI = GNI − adjustments = €324.2bn − €89bn = €235.2bn, 6 marks. B must be '
           'found first.')],
    stem=q10_stem, figure=PAP + 'p12-q10-question', **A)


# ═════════════════════════════════ SECTION B ══════════════════════════════════

# Q11 ─ Census 2022; labour mobility; HDI
q11_stem = H.ask(13, 'The infographic below shows preliminary results for Census 2022', ' (a)')
add('q11-a-i', '3-5', 'percentage-change-in-the-irish-population', ref(11, '(a)(i)'),
    H.ask(13, 'Using the data in the table below (extracted from the infographic above)', ' Population 2016'),
    '8', 8,
    [point('r-calculation', '7.59 %', 8,
           'Total change ÷ 2016 population × 100 = 361,671 ÷ 4,761,865 × 100 = 7.59%. Deduct 1 mark '
           'if % is omitted. The official working is shown in the figure.')],
    stem=q11_stem, figure=SOL + 'p15-q11ai-working')
pick('q11-a-ii', '3-5', 'drivers-of-population-growth', ref(11, '(a)(ii)'),
     H.ask(13, 'Explain two factors which are likely to have influenced this trend', ' 1. 2.'),
     'A factor behind the population trend — any two',
     bl('• Increased birth rate:', '(iii) An increase in population'),
     2, 5, 'Two factors, 5 marks each.', stem=q11_stem, figure=PAP + 'p13-i0')
add('q11-a-iii-neg', '3-1', 'population-growth-and-government-finances', ref(11, '(a)(iii)'),
    H.ask(14, 'An increase in population can have a positive and negative effect', ' One negative effect:'),
    '5 + 5', 10,
    [heading('r-negative', 'One negative effect', bl('• Pressure on provision of state services:', 'Positive ⟨5⟩'), 5,
             'Complete BOTH headings. One negative effect on government finances, 5 marks.'),
     heading('r-positive', 'One positive effect',
             bl('• Increased demand for goods and services:', '(b) Labour is one of the factors'), 5,
             'One positive effect on government finances, 5 marks.')])
q11b_stem = H.ask(14, 'Labour is one of the factors of production.', ' (i)')
add('q11-b-i', '2-1', 'factor-of-production-labour', ref(11, '(b)(i)'),
    H.ask(14, 'Explain the factor of production labour.', ' (ii)'), '6', 6,
    [point('r-1', H.run('Labour refers to all human effort', '(ii) Explain two factors'), 6,
           'Explain the term, 6 marks.')],
    stem=q11b_stem)
add('q11-b-ii', '2-1', 'geographical-mobility-of-labour', ref(11, '(b)(ii)'),
    H.ask(14, 'Explain two factors that influence geographical mobility', ' 1. 2.'), '5 + 4', 9,
    [steps('r-1', 'A factor that influences geographical mobility — any two',
           bl('• Housing: if there is affordable housing', '(iii) Explain two ways the government'), 5, 4,
           'factors')],
    stem=q11b_stem)
add('q11-b-iii', '2-1', 'increasing-mobility-of-labour', ref(11, '(b)(iii)'),
    H.ask(15, 'Explain two ways the government can possibly increase', ' 1. 2.'), '5 + 4', 9,
    [steps('r-1', 'A way to increase geographical mobility — any two',
           bl('• Financial incentives: to encourage firm', '14 | P a g e'), 5, 4, 'ways')],
    stem=q11b_stem)
q11c_stem = H.ask(15, 'The table below (adapted from the UNDP)', ' Rank Country')
add('q11-c-i', '4-0', 'life-expectancy-and-the-hdi', ref(11, '(c)(i)'),
    H.ask(15, 'In your opinion, if the average life expectancy', ' Positively:') + ' '
    + H.ask(15, 'Explain the reason for your answer.', ' Explanation:'), '1 + 4', 5,
    [point('r-1', 'Negatively.', 1, 'NEGATIVELY: the scheme credits no positive answer; 1 mark for the choice.'),
     point('r-2', H.run('• If average life expectancy were to decrease', '(ii) Despite Ireland'), 4,
           'Explain, 4 marks: life expectancy is one of the HDI’s three components, so a fall lowers '
           'the score.')],
    stem=q11c_stem, figure=PAP + 'p15-i0')
add('q11-c-ii', '3-1', 'policies-to-address-inequality', ref(11, '(c)(ii)'),
    H.ask(16, 'Outline two economic policies which the Irish Government could consider', ' 1. 2.'),
    '5 + 4', 9,
    [steps('r-1', 'A policy to address inequality, justified — any two',
           bl('• Invest in education:', '15 | P a g e'), 5, 4, 'policies, each justified')],
    stem=H.ask(16, 'Despite Ireland’s high HDI ranking, inequalities still exist.', ' Outline two'))
add('q11-c-iii', '3-1', 'disadvantages-of-inequality-policies', ref(11, '(c)(iii)'),
    H.ask(16, 'If the policies you suggested in (ii) above were introduced', ' 1. 2.'), '5 + 4', 9,
    [anyN('r-1', 'A disadvantage of one of your two policies — one for each', None, 2, 5,
          bl('• Education: abolishing fees', 'Note: one disadvantage of each policy required.'),
          'Two disadvantages, the first correct one 5 marks and the second 4. The scheme requires '
          'one disadvantage of EACH policy you gave in (ii), not two of the same policy.', steps=[5, 4])])

# Q12 ─ perfect competition; HHI; windfall tax
q12a_stem = H.ask(17, 'If a consumer wishes to purchase milk in the Irish market', ' Adapted from')
pick('q12-a-i', '2-0', 'perfect-competition-characteristics', ref(12, '(a)(i)'),
     H.ask(17, 'Identify three characteristics of a perfectly competitive market.', ' 1. 2. 3.'),
     'A characteristic of perfect competition — any three',
     bl('• Large number of buyers.', '(ii) Identify one reason why the market for Irish milk'),
     3, 4, 'Three characteristics, 4 marks each.', stem=q12a_stem, figure=PAP + 'p17-i0')
pick('q12-a-ii', '2-0', 'irish-milk-not-perfectly-competitive', ref(12, '(a)(ii)'),
     H.ask(17, 'Identify one reason why the market for Irish milk', ' Leaving'),
     'A reason the milk market is not perfectly competitive — any one',
     bl('• There are some large sellers in the industry', '17 | P a g e'),
     1, 4, 'One reason, 4 marks.', stem=q12a_stem)
add('q12-a-iii', '2-0', 'long-run-equilibrium-in-perfect-competition', ref(12, '(a)(iii)'),
    H.ask(18, 'Explain, with the use of a fully labelled diagram', ' Leaving'), '9 + 8', 17,
    [point('r-diagram', 'Price Quantity P C Q MC AC D/AR/MR E', 9,
           'Diagram, 9 marks at 1 per label: Price, Quantity, P, C, Q, MC, AC, D = AR = MR and E. MC '
           'cuts the horizontal D = AR = MR line at the minimum of AC (E), so P = C. The official '
           'diagram is shown in the figure.'),
     point('r-2', H.run('• Equilibrium is at point E (where MC = MR).', '18 | P a g e'), 8,
           'Explanation, 8 marks with no separately priced steps: E where MC = MR, output Q, price '
           'P, cost C, normal profit because AR = AC, and production at minimum average cost.')],
    figure=SOL + 'p20-q12aiii-competition')
q12b_stem = H.ask(19, 'The bar chart below shows the percentage (%) market share', ' Market Share')
add('q12-b-i', '2-0', 'calculating-the-herfindahl-hirschman-index', ref(12, '(b)(i)'),
    H.ask(19, 'Based upon the figures in the bar chart above, calculate the', ' Workings:'), '9', 9,
    [point('r-calculation', '3172', 9,
           'Square each market share and add: 48² + 27² + 8² + 7² + 3² + 3² + 2² + 2² = 2,304 + 729 + '
           '64 + 49 + 9 + 9 + 4 + 4 = 3,172. The official working is shown in the figure.')],
    stem=q12b_stem, figure=SOL + 'p21-q12bi-working')
pick('q12-b-ii', '2-0', 'reading-the-dairy-market-hhi', ref(12, '(b)(ii)'),
     H.ask(19, 'Would you consider this market to be competitive', ' Answer:'),
     'Why the market is highly concentrated — either one',
     bl('• The market is dominate by two large firms.', '(iii) Outline one possible economic advantage'),
     1, 5, 'Answer HIGHLY CONCENTRATED and explain, 5 marks: an HHI above 2,500 is highly '
     'concentrated, and two firms hold 75% of the market.',
     stem=q12b_stem, figure=PAP + 'p19-q12b-chart')
add('q12-b-iii-adv', '2-0', 'perfect-competition-advantage-and-disadvantage', ref(12, '(b)(iii)'),
    H.ask(19, 'Outline one possible economic advantage and one possible economic', ' Advantage:'), '10', 10,
    [shared('r-advantage', 'One advantage', bl('• Low prices - the firm sells', 'Disadvantages'),
            'Complete BOTH headings. The scheme prices the pair as one 10: the first correct answer '
            '6 marks and the second 4, with no fixed share for either heading.'),
     shared('r-disadvantage', 'One disadvantage', bl('• Little potential to expand or develop', '19 | P a g e'),
            'One disadvantage.')],
    kind='questionTotal')
q12c_for = at_columns('For Reduce consumer exploitation.', '\nAgainst Deter future investment', occ=1, firsts=
              ['Reduce consumer exploitation.', 'Help people during current crisis',
               'Support Irish businesses.', 'Achieve a more equitable tax system.'])
add('q12-c', '1-3', 'windfall-tax-for-and-against', ref(12, '(c)'),
    H.ask(20, 'Discuss the arguments for and the arguments against this proposal.', ' 75 marks'), '8 + 5 + 5', 18,
    [anyN('r-1', 'An argument for or against the windfall tax — any three, covering both sides', None, 3, 8,
          q12c_for + at_columns('Against Deter future investment in energy development.', '18 1st @ 8',
                                ['Deter future investment in energy development.', 'Inadequate infrastructure.',
                                 'Erratic future supply of energy.']),
          'Three arguments: the first correct one 8 marks and the next two 5 each. The first four '
          'are the scheme’s arguments FOR and the last three its arguments AGAINST; discuss both '
          'sides.', steps=[8, 5, 5])],
    stem=H.ask(20, 'Budget 2023 proposed introducing a temporary 33% windfall tax', ' Adapted from'))

# Q13 ─ circular flow; hidden economy; multiplier; MNCs; competitiveness
add('q13-a-i', '3-0', 'drawing-the-circular-flow-for-an-open-economy', ref(13, '(a)(i)'),
    H.ask(21, 'Draw a fully labelled diagram showing the Circular Flow', ' (ii)'), '13 @ 1', 13,
    [point('r-1', H.run('Households Firms\nPurchase of Goods and Services', '(ii) Explain the terms injections'), 13,
           'Thirteen labels at 1 mark each: Households, Firms, Incomes for supplying factors of '
           'production / Wages, Purchase of Goods and Services, Taxation, Savings, Imports, '
           'Government, Financial Institutions, Foreign Markets, Government Spending, Investment '
           'and Exports. The official diagram is shown in the figure.')],
    figure=SOL + 'p23-q13ai-circular-flow')
add('q13-a-ii', '3-0', 'injections-and-leakages', ref(13, '(a)(ii)'),
    H.ask(21, 'Explain the terms injections and leakages', ' Injections:'), '2 + 4 + 2 + 4', 12,
    [point('r-injections', H.run('Injections are variables in an economy', 'Examples: Government Spending'), 2,
           'Explain injections, 2 marks.'),
     point('r-injection-examples', 'Examples: Government Spending, Investment, Exports.', 4,
           'Two injections from your diagram, 2 marks each.'),
     point('r-leakages', H.run('Leakages are the non-consumption uses of income', 'Examples: Taxation'), 2,
           'Explain leakages, 2 marks.'),
     point('r-leakage-examples', 'Examples: Taxation, Savings, Imports.', 4,
           'Two leakages from your diagram, 2 marks each.')],
    figure=SOL + 'p23-q13ai-circular-flow')
pick('q13-a-iii', '3-0', 'effects-of-the-hidden-economy-hl', ref(13, '(a)(iii)'),
     H.ask(22, 'Outline two effects on the Irish economy of activities in the hidden economy.', ' 1. 2.'),
     'An effect of the hidden economy — any two',
     bl('• Loss of revenue for the government', 'Marginal Propensity to Consume (MPC) 0.7'),
     2, 4, 'Two effects, 4 marks each.',
     stem=H.ask(22, 'Some citizens engage in activities in the hidden economy', ' Outline two'))
q13b_stem = H.ask(22, 'Use the information in the table below, to answer the questions that follow:', ' (i)')
add('q13-b-i-mps', '3-0', 'marginal-propensity-to-save-from-the-mpc', ref(13, '(b)(i)'),
    H.ask(22, 'Calculate the marginal propensity to save (MPS)', ' Workings:'), '3 @ 2', 6,
    [point('r-calculation', 'MPS = 0.3', 6, 'MPS = 1 − MPC = 1 − 0.7 = 0.3; the scheme marks it 3 @ 2.')],
    stem=q13b_stem)
add('q13-b-ii-multiplier', '3-0', 'the-multiplier-in-an-open-economy', ref(13, '(b)(ii)'),
    H.ask(22, 'Calculate the value of the multiplier in this open economy.', ' Workings:'), '4 @ 2', 8,
    [point('r-calculation', '2', 8,
           'Multiplier = 1 ÷ (MPS + MPM) = 1 ÷ (0.3 + 0.2) = 2; or 1 ÷ (1 − (MPC − MPM)) = 1 ÷ (1 − '
           '(0.7 − 0.2)) = 2. The scheme marks it 4 @ 2; the official working is shown in the figure.')],
    stem=q13b_stem, figure=SOL + 'p24-q13bii-working')
add('q13-b-iii', '3-0', 'the-injection-needed-to-reach-full-employment', ref(13, '(b)(iii)'),
    H.ask(23, 'How much will the government have to inject', ' Workings:'), '8', 8,
    [point('r-calculation', '€125m', 8,
           'Gap = €750m − €500m = €250m; injection = gap ÷ multiplier = €250m ÷ 2 = €125m. The '
           'small 2s beside the scheme’s working are mark annotations, not powers.')],
    stem=q13b_stem)
q13c_stem = H.ask(23, 'Our income tax system is heavily reliant', ' Adapted from')
add('q13-b-i', '4-1', 'risks-of-over-reliance-on-mncs', ref(13, '(c)(i)'),
    H.ask(23, 'Outline two risks associated with over', ' 1. 2.'), '7 + 5', 12,
    [steps('r-1', 'A risk of over-reliance on MNCs — any two',
           bl('• Vulnerable tax revenue position:', '23 | P a g e'), 7, 5, 'risks')],
    stem=q13c_stem)
pick('q13-b-ii', '4-2', 'factors-affecting-competitiveness', ref(13, '(c)(ii)'),
     H.ask(24, 'Discuss two factors that are currently impacting', ' 1. 2.'),
     'A factor affecting competitiveness — any two',
     bl('• Transport costs:', '24 | P a g e'), 2, 4, 'Two factors, 4 marks each.', stem=q13c_stem)

# Q14 ─ unemployment; full employment; PUP; trade protection
q14_stem = H.ask(25, 'The graph below shows the monthly unemployment rate', ' SEASONALLY')
add('q14-a-i', '3-2', 'trend-in-the-monthly-unemployment-rate', ref(14, '(a)(i)'),
    H.ask(25, 'From the graph above analyse one trend', ' (ii)'), '4 + 4', 8,
    [point('r-response', paras(bl('• Between March 2021 and September 2022, the unemployment rate fell.',
                                  'Survey. Give two reasons why')), 8,
           'One trend with figures, 4 + 4: the direction and the supporting figures. These are the '
           'scheme’s three alternative trends; the changes are in percentage points.')],
    stem=q14_stem, figure=PAP + 'p25-i0')
add('q14-a-ii', '3-2', 'why-the-labour-force-survey-is-better', ref(14, '(a)(ii)'),
    H.ask(25, 'Another method of measuring unemployment', ' 1. 2.'), '4', 4,
    [point('r-credit', H.run('Award 4 marks to all candidates who attempted this question.',
                             '• The Live Register includes'), None,
           'The SEC gave all 4 marks for any attempt: the question should have named the Labour '
           'Force Survey.'),
     point('r-reasons', paras(bl('• The Live Register includes those who receive', '25 | P a g e')), None,
           'The scheme’s reasons the survey is more accurate, for practice.')],
    kind='questionTotal')
pick('q14-a-iii', '3-2', 'types-of-unemployment', ref(14, '(a)(iii)'),
     H.ask(26, 'Describe two types of unemployment', ' Type 1:'),
     'A type of unemployment, with an example — any two',
     bl_full('• Structural unemployment: This occurs when there is a mismatch',
               ' Explain the economic term full employment. Full Employment', occ=1),
     2, 7, 'Two types, each described with an example, 7 marks each.')
add('q14-b-i', '3-2', 'the-term-full-employment', ref(14, '(b)(i)'),
    H.ask(26, 'Explain the economic term full employment.', ' Full employment:'), '4 + 2', 6,
    [point('r-1', 'Full Employment refers to a situation in which all those members of the labour force '
           'who are willing and able to work are employed', 4, 'The body of the definition, 4 marks.'),
     point('r-2', 'at existing wage rates', 2, 'The closing condition, 2 marks (the scheme’s small 4 and 2 '
           'mark the split).')])
pick('q14-b-ii', '3-1', 'government-economic-objectives', ref(14, '(b)(ii)'),
     H.ask(26, 'Outline two other current economic objectives', ' 1. 2.'),
     'An economic objective other than full employment, justified — any two',
     bl('• Build more houses / reduce homelessness.', '26 | P a g e'),
     2, 4, 'Two objectives, each justified, 4 marks each.',
     stem=H.ask(26, 'Maintaining full employment is an objective', ' Outline two'))
add('q14-b-iii', '0-1', 'cost-benefit-analysis-of-the-pup', ref(14, '(b)(iii)'),
    H.ask(27, 'Use a cost', ' Private benefit:'), '3 @ 4', 12,
    [heading('r-private', 'Private benefit', bl('• People who were left unemployed', 'External benefit'), 4,
             'Complete ALL THREE headings. Who enjoyed the private benefit, 4 marks.'),
     heading('r-external', 'External benefit', bl('• The government received taxation revenue', 'Who bore the cost'), 4,
             'Who enjoyed the external benefit, 4 marks.'),
     heading('r-cost', 'Who bore the costs', bl('• The government had to borrow', '(c)\n23 In the 1950s'), 4,
             'Who bore the costs, 4 marks.')],
    stem=H.ask(27, 'The Irish government spent €8.8bn', ' Adapted from'))
q14c_stem = H.ask(27, 'In the 1950s and 1960s, Ireland had a very high rate', ' (i)')
add('q14-c-i', '4-2', 'the-term-trade-protection', ref(14, '(c)(i)'),
    H.ask(27, 'Explain the economic term trade protection.', ' Explanation:'), '7', 7,
    [point('r-1', H.run('Trade Protection refers to government policies', '27 | P a g e'), 7,
           'Explain the term, 7 marks.')],
    stem=q14c_stem)
pick('q15-b-ii', '4-2', 'reasons-for-trade-protection', ref(14, '(c)(ii)'),
     H.ask(28, 'Discuss two economic reasons why countries are favouring', ' 1. 2.'),
     'A reason for a return to trade protection — any two',
     bl('• Reduction in leakages from the circular flow', '• Stagnation of technological'),
     2, 4, 'Two reasons, 4 marks each.',
     stem=H.ask(28, 'Some countries are now favouring a return', ' Discuss two'))
pick('q15-b-iii', '4-2', 'disadvantages-of-trade-protection', ref(14, '(c)(iii)'),
     H.ask(28, 'Outline two possible disadvantages of trade protection.', ' 1. 2.'),
     'A disadvantage of trade protection — any two',
     bl('• Stagnation of technological advancements', '28 | P a g e'),
     2, 4, 'Two disadvantages, 4 marks each.', stem=q14c_stem)

# Q15 ─ electricity prices; inflation; ECB; exchange rates; €600 credit
q15_stem = H.ask(29, 'The diagram below shows the average electricity price', ' Average')
add('q15-a-i', '3-3', 'how-rising-prices-change-behaviour', ref(15, '(a)(i)'),
    H.ask(29, 'Outline one key trend in electricity prices', ' Trend:'), '6', 6,
    [point('r-trend', H.run('Overall upward trend from S1 2020 to S1 2022.', '⟨6⟩'), None,
           'One key trend with figures. The chart is in euro cents per kWh: about 23 cents in 2020 S1 '
           'rising to about 26–28 cents; the scheme writes the figures as €21/€22 to €26/€27 per kwh.'),
     point('r-impact', paras(bl('• Purchasing power reduced:', '• Cost-push inflation occurs')), None,
           'Explain the effect on consumer behaviour. The scheme gives one 6 for the trend and the '
           'effect together, with no published split.')],
    kind='questionTotal', stem=q15_stem, figure=PAP + 'p29-i1')
add('q15-a-ii', '3-3', 'demand-pull-and-cost-push-inflation', ref(15, '(a)(ii)'),
    H.ask(29, 'Distinguish between demand', ' Demand'), '4 + 4', 8,
    [point('r-1', 'Cost-push inflation occurs when increases in cost of production', 4,
           'Cost-push, 4 marks: higher costs of production passed on as higher prices.'),
     point('r-2', 'Demand-pull inflation occurs when (aggregate) demand is greater than', 4,
           'Demand-pull, 4 marks: aggregate demand greater than aggregate supply pulls prices up. '
           'The scheme’s small 2s mark the split within each.')])
add('q15-a-iii', '3-3', 'building-a-weighted-composite-price-index', ref(15, '(a)(iii)'),
    H.ask(30, 'The table below shows a country’s composite price index', ' % of'), '19', 19,
    [point('r-calculation', '112.2', 19,
           'Simple index = current price ÷ base price × 100: food 55 ÷ 50 × 100 = 110; transport 24 ÷ '
           '20 × 100 = 120; other items 81 ÷ 75 × 100 = 108. Weighted: 110 × 60% = 66.0; 120 × 25% = '
           '30.0; 108 × 15% = 16.2. Price index for the current year = 112.2. The scheme gives 19 for '
           'the whole table; the official worksheet is shown in the figure.')],
    figure=SOL + 'p32-q15aiii-working')
q15b_stem = H.ask(30, 'One role of the European Central Bank (ECB) is to formulate', ' (i)')
add('q15-b-i', '3-3', 'the-term-monetary-policy', ref(15, '(b)(i)'),
    H.ask(30, 'Explain the term monetary policy.', ' Leaving'), '8', 8,
    [point('r-1', H.run('Monetary policy refers to any action by the European Central Bank', '30 | P a g e'), 8,
           'Explain the term, 8 marks.')],
    stem=q15b_stem)
add('q15-b-ii-depreciation', '4-2', 'reading-appreciation-or-depreciation-off-an-exchange-rate-chart',
    ref(15, '(b)(ii)'),
    H.ask(31, 'Does the prevailing trend on the graph below', ' Appreciation:') + ' Explain your answer.', '6', 6,
    [point('r-1', H.run('Answer: Depreciation', 'Yes\nPrice of imports will decrease'), 6,
           'DEPRECIATION, 6 marks with the explanation: from 01/09/2022 to 01/11/2022 the euro falls '
           'from £0.90 to £0.86, so each euro buys less sterling.')],
    stem=q15b_stem, figure=PAP + 'p31-art')
stance('q15-b-iii', [
    ('q15-b-iii-euro', 'yes', 'A reason the government should be concerned — any one',
     at('Price of imports will decrease.', 'OR\nNo',
        ['Price of imports will decrease.', 'Price of exports will increase.']),
     'euro-appreciation-concern-yes'),
    ('q15-b-iii-euro-no', 'no', 'A reason the government need not be concerned — any one',
     at('Increased purchasing power / improved standard of living', '31 | P a g e',
        ['Increased purchasing power / improved standard of living', 'Reduced inflationary pressures:']),
     'euro-appreciation-concern-no')],
    '4-2', 15, '(b)(iii)',
    H.ask(31, 'Should the Irish government be concerned if the Euro to Dollar', ' Yes:') + ' Justify your answer.',
    8)
q15c_stem = H.ask(31, 'In budget 2023 the Irish government introduced a €600', ' (i)')
pick('q15-c-i', '1-3', 'why-the-electricity-credit', ref(15, '(c)(i)'),
     H.ask(31, 'Explain the main economic reason for the above government intervention.', ' Leaving'),
     'The main economic reason — any one',
     bl('• Help Irish citizens with the cost of living', '• Opportunity cost:'),
     1, 7, 'One developed reason, 7 marks.', stem=q15c_stem)
pick('q15-c-ii', '1-3', 'downside-of-the-electricity-credit', ref(15, '(c)(ii)'),
     H.ask(32, 'Outline one possible economic disadvantage of this government intervention.', ' (iii)'),
     'An economic disadvantage — any one',
     bl('• Opportunity cost:', 'Answer: No'), 1, 7, 'One developed disadvantage, 7 marks.', stem=q15c_stem)
add('q15-c-iii', '1-3', 'does-the-credit-reduce-electricity-use', ref(15, '(c)(iii)'),
    H.ask(32, 'In your opinion does the above government intervention', ' Yes:') + ' Explain your answer.',
    '6', 6,
    [point('r-1', H.run('Answer: No', '32 | P a g e'), 6,
           'Tick NO: the scheme credits no yes answer. Explain, 6 marks for the choice and its '
           'explanation together: the credit shields households from the price rise, so use need '
           'not fall.')],
    stem=q15c_stem)

# Q16 ─ demand; government and market failure; circular economy; national herd; DRS
add('q16-a-i', '1-0', 'individual-and-market-demand', ref(16, '(a)(i)'),
    H.ask(33, 'Distinguish between the economic terms individual demand and market demand.',
          ' Individual demand:'), '4 + 4', 8,
    [point('r-individual', H.run('• Individual Demand refers to the quantity', '• Market Demand refers'), 4,
           'Individual demand, 4 marks.'),
     point('r-market', H.run('• Market Demand refers to the quantity', '(ii) The Irish Government'), 4,
           'Market demand, 4 marks: the demand of ALL consumers in the market.')])
q16a2_stem = H.ask(33, 'The Irish Government has provided free school transport', ' Demonstrate')
add('q16-a-ii', '1-0', 'free-school-transport-and-the-car-market', ref(16, '(a)(ii)'),
    H.ask(33, 'Demonstrate, with the use of a fully labelled diagram', ' Diagram Explanation'), '7 + 8', 15,
    [point('r-diagram', 'The demand curve will shift to the left from D1 to D2.', 7,
           'Diagram, 7 marks: demand shifts LEFT from D1 to D2; the equilibrium price falls from P1 '
           'to P2 and the quantity from Q1 to Q2. The official diagram is shown in the figure.'),
     point('r-explanation', H.run('• The demand curve will shift to the left from D1 to D2.',
                                  'Does this represent a government failure?'), 8,
           'Explanation, 8 marks: free school buses are a substitute for cars, so demand for cars '
           'falls and the equilibrium price and quantity fall.')],
    stem=q16a2_stem, figure=SOL + 'p35-q16aii-diagram')
add('q16-a-iii', '2-2', 'school-transport-government-failure', ref(16, '(a)(iii)'),
    H.ask(33, 'The rapid introduction of this scheme created', ' Yes:'), '5', 5,
    [point('r-1', H.run('This government intervention into the market created', '33 | P a g e'), 5,
           'Tick YES: the scheme credits no no answer. Explain, 5 marks for the choice and its '
           'explanation together.')],
    stem=q16a2_stem)
q16b_stem = H.ask(34, 'In 2006, multinational oil trading company Trafigura', ' (i)')
add('q16-b-i', '2-2', 'toxic-waste-and-market-failure', ref(16, '(b)(i)'),
    H.ask(34, 'Does this represent a market failure? Justify your answer.', ' Yes:'), '5', 5,
    [point('r-1', H.run('Explanation: Market failure occurs when', 'July 2022.'), 5,
           'Answer YES: the scheme credits no no answer. Justify, 5 marks: dumping imposed negative '
           'externalities (pollution, ill health) on third parties.')],
    stem=q16b_stem)
pick('q16-b-ii', '0-2', 'moving-to-a-circular-economy', ref(16, '(b)(ii)'),
     H.ask(34, 'Outline two of the challenges the economy will face', ' 1. 2.'),
     'A challenge of the transition to a circular economy — any two',
     bl('• Consumer attitudes and behaviour:', '34 | P a g e'), 2, 4, 'Two challenges, 4 marks each.',
     stem=H.ask(34, 'The Circular Economy and Miscellaneous Provisions Act 2022', ' Adapted from'))
add('q16-b-iii', '0-2', 'reducing-household-food-waste', ref(16, '(b)(iii)'),
    H.ask(35, 'Describe initiatives the Irish government could take', ' 1. 2.'), '6 + 4', 10,
    [steps('r-1', 'A government initiative on food waste — any two',
           bl('• Public awareness campaigns.', '35 | P a g e'), 6, 4, 'initiatives')],
    stem=H.ask(35, 'On average households in Ireland are responsible for 117 kg', ' Adapted from'))
q16c1_for = bl('• The beef industry in Ireland is in decline', 'Against:')
q16c1_against = bl('• Protection of rural economy.', '36 | P a g e')
add('q16-c-i-for', '0-2', 'arguments-for-and-against-reducing-the-national-herd', ref(16, '(c)(i)'),
    H.ask(35, 'The argument for reducing the national herd', ' For:'), '12', 12,
    [shared('r-for', 'One argument for', q16c1_for,
            'Complete BOTH headings. The scheme prices the pair as one 12: the first correct argument '
            '7 marks and the second 5, with no fixed share for either heading.'),
     shared('r-against', 'One argument against', q16c1_against, 'One argument against.')],
    kind='questionTotal', stem=H.ask(35, 'Deputy Barry Cowen described the argument', ' Adapted from'))
add('q16-c-ii', '0-2', 'effects-of-the-deposit-return-scheme', ref(16, '(c)(ii)'),
    H.ask(36, 'Outline two likely effects the introduction of the Deposit Return Scheme', ' 1. 2.'),
    '7 + 5', 12,
    [steps('r-1', 'An effect on the Irish consumer — any two',
           bl('• Will incentivise consumers to return these containers', '37 | P a g e'), 7, 5, 'effects')],
    stem=H.ask(36, 'The Deposit Return Scheme is to be introduced in February 2024.', ' Adapted from'))

# A card whose figure slot holds its solution carries the whole printed question.
for cid, fig in [('sa-q3-a', 'p05-q3a-question'), ('sa-q4-a', 'p06-q4a-question'),
                 ('sa-q7-a', 'p09-q7a-question'), ('q11-a-i', 'p13-q11ai-question'),
                 ('q12-b-i', 'p19-q12bi-question'), ('q15-a-iii', 'p30-q15aiii-question')]:
    show_before_reveal(next(c for c in cards if c['id'] == D.prefix + cid), None, PAP + fig)


# ── Withdrawn halves ──────────────────────────────────────────────────────────
# The earlier extractors split four required-heading responses into one card per
# heading. Each half is still emitted, lifted from its own heading, so that
# card-corrections.json can withdraw it by ID and name the combined card that
# now carries its saved progress (cardAliases.ts). None of these ships.
WITHDRAWN = [
    ('sa-q2-c-dis', 'sa-q2-c-adv', 'Disadvantage', q2c_dis, 3),
    ('q11-a-iii-pos', 'q11-a-iii-neg', 'One positive effect',
     bl('• Increased demand for goods and services:', '(b) Labour is one of the factors'), 5),
    ('q12-b-iii-dis', 'q12-b-iii-adv', 'One disadvantage',
     bl('• Little potential to expand or develop', '19 | P a g e'), 4),
    ('q16-c-i-against', 'q16-c-i-for', 'One argument against', q16c1_against, 5),
]
for old, canonical, label, options, per in WITHDRAWN:
    base = next(c for c in cards if c['id'] == D.prefix + canonical)
    pick(old, base['topicId'].removeprefix('economics-'), base['conceptId'] + '-withdrawn-half',
         base['questionRef'], f"{base['questionText']} Withdrawn half: {label}.", label, options, 1, per,
         f'Withdrawn: this heading is answered within {D.prefix + canonical}.', stem=base.get('stem', ''),
         section=base['section'])

if __name__ == '__main__':
    emit(cards)
