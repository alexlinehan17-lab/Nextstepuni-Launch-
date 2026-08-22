#!/usr/bin/env python3
"""Economics 2023 Higher Level — Section A.

100 marks, eight questions of twelve answered out of ten, plus a mark for each
of the first four answered correctly.

Not carded: the table completion in question 4(a), the national income
calculation in question 10, and the two parts whose marks are for drawing a
shift on a supplied diagram rather than for the reasoning printed beside it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, block, bullets, card, load, tidy  # noqa: E402

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

P.emit()
