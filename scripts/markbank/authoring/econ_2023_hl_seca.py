#!/usr/bin/env python3
"""Economics 2023 Higher Level — Section A.

100 marks, eight questions of twelve answered out of ten, plus a mark for each
of the first four answered correctly.

Not carded: the table completions in questions 3(a) and 4(a) and the national
income calculation in question 10 (the marks are for figures and workings, not
prose); 3(b), which is answered by reading the marginal-utility figures the
student calculated in 3(a); 3(c), whose response is the worked equi-marginal
ratio; 6(a), answered by ticking direct or indirect against each tax; and the
two parts whose marks are for drawing a shift on a supplied diagram rather
than for the reasoning printed beside it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

P = Paper(2023, 'higher', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('France will host the Rugby World Cup', 'econ-2023-hl-sa-q1-a',
       'economics-1-2', 'supply-of-a-fixed-capacity-good',
       'France will host the Rugby World Cup in 2023. Explain the supply curve for tickets for '
       'this event.',
       'A way of explaining the shape — any one',
       'One explanation, 3 marks. The part pays 6: the other 3 are for the labelled diagram, '
       'which is not carded.',
       ref='2023 HL Section A Q1(a)', claim=1, per=3, drop=SCAFFOLD)

P.menu('conditions necessary for price discrimination to occur in the selling',
       'econ-2023-hl-sa-q1-b', 'economics-1-1', 'conditions-for-price-discrimination-2023',
       'Explain two conditions necessary for price discrimination to occur in the selling of '
       'tickets for the Rugby World Cup 2023.',
       'A condition for price discrimination — any two',
       'Two conditions, 3 marks each.',
       ref='2023 HL Section A Q1(b)',
       drop=SCAFFOLD + ('tickets for the Rugby World Cup 2023.',))

P.menu('if petrol is considered to have price elastic demand', 'econ-2023-hl-sa-q2-a',
       'economics-1-4', 'why-petrol-demand-is-inelastic',
       'Is petrol considered to have price elastic or price inelastic demand? Explain your '
       'answer.',
       'A way of explaining it — any one',
       'One explanation, 5 marks. The sixth mark is for the tick itself: petrol is price '
       'inelastic.',
       ref='2023 HL Section A Q2(a)', claim=1, per=5, drop=SCAFFOLD,
       stem='On 3 March 2022 the price of petrol in Ireland broke €2 a litre for the first time.')

P.menu('important for retailers to understand the concept of price', 'econ-2023-hl-sa-q2-b',
       'economics-1-4', 'why-retailers-need-elasticity',
       'Outline two reasons why it is important for retailers to understand the concept of price '
       'elasticity of demand.',
       'A reason retailers need elasticity — any two',
       'Two reasons, 3 marks each.',
       ref='2023 HL Section A Q2(b)', drop=SCAFFOLD)

# ── Q2(c), built from the scheme directly ──────────────────────────────────
# The part answers two opposite questions and the scheme heads the two lists
# "Advantages" and "Disadvantages" — but a bare heading between bullets is not a
# bullet, so it arrives glued to the end of the response above it and there is
# nothing left to cut the list at. Sliced here at the headings themselves.
BODY = tidy(load(2023, 'higher'))
for side, half, cid, concept, verb in (
        ('advantage', block(BODY, 'Cost of Living Crisis: Irish citizens', 'Disadvantages'),
         'econ-2023-hl-sa-q2-c-adv', 'not-raising-excise-duty-advantage',
         'An advantage of holding the duty — any one'),
        ('disadvantage', block(BODY, 'Government revenue: petrol has price inelastic demand',
                               '3. (a) Complete the missing total utility'),
         'econ-2023-hl-sa-q2-c-dis', 'not-raising-excise-duty-disadvantage',
         'A disadvantage of holding the duty — any one')):
    P.cards.append(card(
        cid, 2023, 'higher', 'economics-3-1', concept,
        f'2023 HL Section A Q2(c) — {side}',
        f'Outline one {side} for the Irish economy of the decision not to increase excise duties '
        f'on petrol in Budget 2023.',
        '1 @ 3', 3,
        [anyN('r-1', verb, 3, 1, 3, bullets(half),
              f'One {side}, 3 marks; the part pays 3 more for the other side.')],
        'The part asks for one advantage and one disadvantage, and the scheme heads the two lists '
        'separately, so each side is its own card.', section='A'))

P.menu('relationship between the Marginal Cost Curve', 'econ-2023-hl-sa-q4-c',
       'economics-1-5', 'marginal-cost-and-average-cost',
       'Explain the relationship between the marginal cost curve and the average cost curve.',
       'A part of the relationship — all three',
       'Three statements, 2 marks each. The scheme lists exactly three and they are the whole '
       'relationship, not a choice.',
       ref='2023 HL Section A Q4(c)', claim=3, per=2, drop=SCAFFOLD)

P.menu('canons/principles of taxation', 'econ-2023-hl-sa-q6-b',
       'economics-3-1', 'canons-of-taxation',
       'Outline three canons of taxation which are achieved through the use of direct taxes.',
       'A canon of taxation — any three',
       'Three canons, 2 marks each.',
       ref='2023 HL Section A Q6(b)', claim=3, per=2, drop=SCAFFOLD)

P.menu('vacant property tax in Ireland can be classed', 'econ-2023-hl-sa-q7-b',
       'economics-1-3', 'why-a-vacant-property-tax',
       'The vacant property tax can be classed as a government intervention. Outline two reasons '
       'why the Irish government introduced it.',
       'A reason for the vacant property tax — any two',
       'Two reasons, 3 marks each.',
       ref='2023 HL Section A Q7(b)', claim=2, per=3,
       drop=SCAFFOLD + ('intervention. Outline two reasons',))

P.menu('cost advantages China', 'econ-2023-hl-sa-q9-b',
       'economics-1-5', 'cost-advantages-of-specialisation',
       'Outline two cost advantages China’s firms experience through specialisation.',
       'A cost advantage of specialising — any two',
       'Two advantages, 3 marks each.',
       ref='2023 HL Section A Q9(b)', claim=2, per=3,
       drop=SCAFFOLD + ('Through specialisation firms can become more efficient',))

# ── Q5(b), built from the scheme directly ───────────────────────────────────
# The mark cell ⟨6⟩ sits inside the first response, a line down from the part,
# so the extractor reads half that response as the question and hands the other
# half back as an option beginning "use of scarce resources".
P.cards.append(card(
    'econ-2023-hl-sa-q5-b', 2023, 'higher', 'economics-0-1',
    'efficient-inefficient-and-impossible-points', '2023 HL Section A Q5(b)',
    'A production possibilities frontier shows an efficient, an inefficient and an impossible '
    'production point. Justify each of your choices.',
    '3 @ 2', 6,
    [anyN('r-1', 'A production point justified — all three', 6, 3, 2,
          bullets(block(BODY, 'Efficient refers to a production point where the firm is making',
                        '6. (a) In each case below')),
          'Three justifications, 2 marks each. The three are the whole answer, not a choice.')],
    '', section='A'))


# ── A figure card ───────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2023-hl-sa-q5-a', 2023, 'higher', 'economics-0-1', 'reading-a-production-frontier',
    '2023 HL Section A Q5(a)',
    'Identify from the diagram above which option (A, B or C) represents an efficient, an '
    'inefficient and an impossible production point respectively.',
    'fixed', 6,
    [point('r-1', 'Efficient Production Point C', 2, 'C sits on the frontier itself.'),
     point('r-2', 'Inefficient Production Point A', 2, 'A sits inside it, so resources are idle.'),
     point('r-3', 'Impossible Production Point B', 2,
           'B sits outside it, beyond what current resources allow.')],
    'The justifications are carded separately, from the same diagram.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-HL-paper-p07-art',
    label_key=[{'letter': 'A', 'meaning': 'an inefficient production point, inside the frontier',
                'askedInThisQuestion': True},
               {'letter': 'B', 'meaning': 'an impossible production point, outside the frontier',
                'askedInThisQuestion': True},
               {'letter': 'C', 'meaning': 'an efficient production point, on the frontier',
                'askedInThisQuestion': True}]))

# ── The definition-shaped parts, built from the scheme directly ────────────
# Each prints one tariff cell over one stated answer (or one short list of
# alternative wordings), so these are point/anyN cards sliced with block()
# rather than menus — the extractor hands them back with the answer welded to
# the question and nothing to claim.

P.cards.append(card(
    'econ-2023-hl-sa-q4-b', 2023, 'higher', 'economics-1-5',
    'covering-costs-in-the-short-run', '2023 HL Section A Q4(b)',
    'To remain in production, in the short run a firm must cover its average total costs. '
    'Do you agree or disagree with this statement? Explain your answer.',
    '1 @ 6', 6,
    [point('r-1', as_option(block(BODY, 'In the short run a firm must cover its average variable',
                                  'OR (c) Explain the relationship')),
           6, 'The ticked box is DISAGREE: in the short run only average variable costs must '
              'be covered. One explanation, 6 marks.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-sa-q8-a', 2023, 'higher', 'economics-3-3',
    'why-the-ecb-raised-interest-rates', '2023 HL Section A Q8(a)',
    'Eurozone interest rates increased four times in the last six months of 2022. Justify '
    'why the European Central Bank (ECB) made this decision.',
    '1 @ 6', 6,
    [point('r-1', as_option(block(BODY, 'The European Central Bank (ECB) made this monetary',
                                  '(b) Does being a member')),
           6, 'One justification, 6 marks.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-sa-q8-b', 2023, 'higher', 'economics-3-3',
    'eurozone-membership-and-monetary-policy', '2023 HL Section A Q8(b)',
    'Does being a member of the Eurozone affect Ireland’s ability to implement monetary '
    'policy in Ireland? Explain your answer.',
    '1 @ 6', 6,
    [anyN('r-1', 'A way membership constrains Irish monetary policy — any one', 6, 1, 6,
          bullets(block(BODY, 'Ireland doesn’t have sovereignty over its monetary policy',
                        '9. China')),
          'The answer is YES. One explanation, 6 marks.')],
    '', section='A'))

P.cards.append(card(
    'econ-2023-hl-sa-q9-a', 2023, 'higher', 'economics-1-5',
    'law-of-diminishing-marginal-returns', '2023 HL Section A Q9(a)',
    'Explain the economic concept of the law of diminishing marginal returns.',
    '1 @ 6', 6,
    [point('r-1', as_option(block(BODY, 'The law of diminishing marginal returns states',
                                  '(b) Harvard Kennedy School')),
           6, 'The definition, 6 marks.')],
    '', section='A', tariff_kind='fixed'))

# Q7(a), repriced. The scheme prints TWO ⟨3⟩ cells for this part: one beside
# the S1 curve of its model diagram (y=163 on the page) and one beside the
# explanation bullets (y=354) — 3 for the drawn shift, 3 for the reasoning.
# The old card claimed "2 @ 3" over the explanation alone, which paid the
# diagram's marks to prose; and its question was a paraphrase econ_refcheck
# could not place in the paper. Now the explanation at its printed 3, worded
# from the paper, on the sa-q1-a pattern (diagram half left uncarded).
P.cards.append(card(
    'econ-2023-hl-sa-q7-a', 2023, 'higher', 'economics-1-1',
    'landlords-leaving-and-the-rental-market', '2023 HL Section A Q7(a)',
    'Explain how this development will alter the rental market equilibrium position.',
    '1 @ 3', 3,
    [point('r-1',
           as_option(block(BODY, 'As landlords leave the market it reduces the supply',
                           '(b) The introduction of the vacant property tax')
                     ).replace(' • ', ' '),
           3, 'The explanation, 3 marks. The part pays 6: the other 3 are for the '
              'shift drawn on the supplied diagram, which is not carded.')],
    'The scheme prints the explanation as three bullets under one ⟨3⟩ cell — a '
    'sequence, not alternatives — so it is carded as the one contiguous run.',
    section='A', tariff_kind='fixed',
    stem='Landlords are leaving the Irish housing market in their thousands, blaming '
         'excessive taxation, rent control and constantly changing laws.'))

# ── A tick table, answered by the scheme's own completed table ─────────────
# See econ_tick_crop.py. The flat run reads "VAT ✓ PAYE ✓ ⟨6⟩ Customs and Excise
# Duty ✓" — three ticks, no columns, and the mark cell sitting between two of
# them. The completed table is bound as a SOLUTION crop instead, hidden until
# reveal.
P.cards.append(card(
    'econ-2023-hl-seca-q6-a', 2023, 'higher', 'economics-3-1',
    'sorting-taxes-direct-and-indirect', '2023 HL Section A Q6(a)',
    'In each case below, indicate by placing a tick (\u2713) whether the tax is an example of '
    'direct taxation or indirect taxation: VAT; PAYE; Customs and Excise Duty.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Tax Direct Tax Indirect Tax VAT',
                                  '(b) Outline three canons')), 6,
           'Read the completed table below: in flat text the ticks carry no column at all. VAT '
           'and Customs and Excise Duty are INDIRECT \u2014 taxes on spending, borne by the '
           'consumer but collected and remitted by someone else \u2014 while PAYE is DIRECT, '
           'deducted from income and paid over by the person who bears it. Who hands the money '
           'to Revenue is the test, not who ends up poorer.')],
    'Two of the three are indirect, so a student splitting them evenly gets one wrong on '
    'symmetry alone.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p11-q6a-ticks'))


# ── Backfill ───────────────────────────────────────────────────────────────
# NOTE on the sibling part (b): the scout's sliding-window anchor matched it to
# a block about the law of diminishing marginal RETURNS, but (b) asks about
# marginal UTILITY — a different concept in a different question. Widening the
# anchor raises the hit rate and with it the risk of hitting the wrong block, so
# the subject of the located block is checked, not just its existence. (b) is
# left uncarded until its own block is found.
P.cards.append(card(
    'econ-2023-hl-seca-q3-c', 2023, 'higher', 'economics-1-4',
    'testing-the-equi-marginal-principle', '2023 HL Section A Q3(c)',
    'Does the formula above obey the Equi-Marginal Principle of consumer behaviour? Explain your '
    'answer.',
    '6', 6,
    [point('r-1', as_option(block(BODY, '\u2022 No, because:', '6 | P a g e')), 6,
           'Work both ratios and compare: 1800 \u00f7 10 = 180 against 3600 \u00f7 10 = 360. The '
           'principle is satisfied only when marginal utility per euro is EQUAL across goods, so '
           'unequal ratios mean it is not obeyed \u2014 and the answer is No.')],
    'Both goods cost the same \u20ac10 here, which makes it tempting to say the condition holds. '
    'It is the utility per euro that must match, not the price.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-sa-q3-a', 2023, 'higher', 'economics-1-1',
    'filling-in-total-and-marginal-utility', '2023 HL Section A Q3(a)',
    'Complete the missing total utility and marginal utility figures in the table below. Show '
    'your workings.',
    '3 @ 2', 6,
    [point('r-1', as_option(block(BODY, '\u2022 80 \u2013 40 = 40', 'Answer (b) or (c)')), 6,
           'Three cells, three workings, two marks each. Marginal utility is the DIFFERENCE '
           'between consecutive totals, so it runs both ways: subtract to get a marginal from '
           'two totals, add to get the next total from a marginal.')],
    'The blanks alternate between the two rows on purpose, so the same relationship has to be '
    'used forwards and backwards. Reading marginal utility as a total is what breaks it.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p08-q3a-working'))

P.cards.append(card(
    'econ-2023-hl-sa-q3-b', 2023, 'higher', 'economics-1-1',
    'where-diminishing-marginal-utility-sets-in', '2023 HL Section A Q3(b)',
    'Based upon the marginal utility figures calculated above, at what point does the law of '
    'diminishing marginal utility set in? Explain your answer.',
    '6', 6,
    [point('r-1', as_option(block(BODY, '\u2022 Answer: on the consumption of the third unit',
                                  'OR (c) Does the formula above obey')), 6,
           'The point is where marginal utility first FALLS \u2014 40 to 35, on the third unit. '
           'The explanation has to quote those two figures; naming the unit alone does not carry '
           'the marks.')],
    'The scheme accepts either wording of the same moment \u2014 on the third unit, or after '
    'the second. What it will not accept is the point where TOTAL utility turns, which is a '
    'different thing and happens later.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p08-q3a-working'))

P.cards.append(card(
    'econ-2023-hl-sa-q4-a', 2023, 'higher', 'economics-1-5',
    'filling-in-average-and-marginal-cost', '2023 HL Section A Q4(a)',
    'Complete the missing average cost and marginal cost figures in the table below.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Workings: \u2022 82 \u00f7 2 = 41',
                                  'Answer (b) or (c)')), 6,
           'Four blanks, four workings. Average cost DIVIDES total cost by output; marginal cost '
           'SUBTRACTS one total cost from the next. The two are different operations on the same '
           'row and mixing them is the whole error.')],
    'Marginal cost is N/A at one unit because there is no previous output to compare with. At '
    'four units marginal cost is 44 while average cost is only 38 \u2014 the marginal figure '
    'has overtaken the average, which is why the average starts to rise.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p09-q4a-table'))

P.cards.append(card(
    'econ-2023-hl-sa-q10', 2023, 'higher', 'economics-3-0',
    'from-gnp-to-gni-and-modified-gni', '2023 HL Section A Q10',
    'Given that Gross Domestic Product (GDP) at Current Market Prices (CMP) was \u20ac426bn, '
    'use the information above to calculate the following terms B, and C. A has been completed '
    'for you. State the relationships and show all your workings.',
    '2 @ 6', 12,
    [point('r-1', as_option(block(BODY, 'Gross National Product (GNP) at Current Market Prices: \u20ac323bn',
                                  '12 | P a g e')), 12,
           'Two steps at six marks each, and each starts from the figure the step above produced. '
           'B adds EU subsidies and subtracts EU taxes to GNP; C then subtracts the \u20ac89bn '
           'of adjustments from B.')],
    'Modified GNI exists because the ordinary figures are distorted by redomiciled companies, '
    'aircraft leasing and intellectual property \u2014 the \u20ac89bn taken out at the last '
    'step. It is the measure that comes closest to what the Irish economy actually produces.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-HL-paper-p12-i0'))

P.emit()
