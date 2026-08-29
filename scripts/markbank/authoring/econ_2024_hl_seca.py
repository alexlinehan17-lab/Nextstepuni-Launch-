#!/usr/bin/env python3
"""Economics 2024 Higher Level — Section A.

Section A is 100 of the paper's 400 marks and reads, on a first skim, like chart
lookups. Most of it is not: "Outline one advantage of a balance of payments
surplus" is answered by five named responses and needs no chart at all. Those
parts are carded here.

What is NOT carded, and why:

  * a part whose answer is read off the infographic printed with it — "calculate
    the current account balance from the data above". The figure pipeline could
    carry those, but the card would then be a chart lookup rather than economics.
  * a part whose marks are for a diagram.

Section A's option cap is 8, not Section B's 14, because it is short-answer.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, heads, load, point, tidy  # noqa: E402

P = Paper(2024, 'higher', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('why full employment is an economic aim', 'econ-2024-hl-sa-q2-b',
       'economics-3-2', 'why-full-employment-is-an-aim',
       'Explain, giving two reasons, why full employment is an economic aim of the government.',
       'A reason full employment is an aim — any two',
       'Two reasons, 3 marks each.',
       ref='2024 HL Section A Q2(b)', drop=SCAFFOLD,
       stem='Ireland’s seasonally adjusted unemployment rate for October 2023 was 4.8%, which '
            'may be regarded as full employment.')

P.menu('The achievement of full employment is an economic aim', 'econ-2024-hl-sa-q2-c',
       'economics-3-1', 'conflicting-economic-aims',
       'Explain how any other two current economic aims of the government may conflict with the '
       'aim of full employment.',
       'A conflicting aim — any two',
       'Two conflicts, 3 marks each. Each is a pair, so naming an aim without saying what it '
       'clashes with earns nothing.',
       ref='2024 HL Section A Q2(c)', drop=SCAFFOLD)

P.menu('energy credits of €450 for all households', 'econ-2024-hl-sa-q3-c',
       'economics-1-3', 'reasons-for-energy-credits',
       'In Budget 2024 the government announced energy credits of €450 for all households. '
       'Outline two reasons for this measure.',
       'A reason for the energy credit — either one',
       'Two reasons, 3 marks each.',
       ref='2024 HL Section A Q3(c)', drop=SCAFFOLD)

P.menu('factors which may affect an individual company’s demand for labour',
       'econ-2024-hl-sa-q4-b', 'economics-2-1', 'demand-for-labour',
       'Outline two factors which may affect an individual company’s demand for labour.',
       'A factor affecting demand for labour — any two',
       'Two factors, 3 marks each.',
       ref='2024 HL Section A Q4(b)', drop=SCAFFOLD)

P.menu('ways the Irish government could intervene in the vaping market',
       'econ-2024-hl-sa-q7-b', 'economics-2-2', 'intervening-in-the-vaping-market',
       'Outline two ways the Irish government could intervene in the vaping market.',
       'A way to intervene — any two',
       'Two ways, 3 marks each.',
       ref='2024 HL Section A Q7(b)', drop=SCAFFOLD)

P.menu('characteristics of consumers that permit/allow price discrimination',
       'econ-2024-hl-sa-q8-b', 'economics-1-1', 'conditions-for-price-discrimination',
       'Outline two characteristics of consumers that permit price discrimination to occur.',
       'A characteristic of consumers — any two',
       'Two characteristics, 3 marks each.',
       ref='2024 HL Section A Q8(b)', drop=SCAFFOLD)

P.menu('advantage of having a surplus on the balance of payments', 'econ-2024-hl-sa-q1-b',
       'economics-4-2', 'advantages-of-a-payments-surplus',
       'Outline one advantage of having a surplus on the balance of payments.',
       'An advantage of a surplus — any one',
       'One advantage, 6 marks.',
       ref='2024 HL Section A Q1(b)', claim=1, per=6, drop=SCAFFOLD)

P.menu('why the purchase of vape products are a form of market failure', 'econ-2024-hl-sa-q7-a',
       'economics-2-2', 'vaping-as-a-market-failure',
       'Explain why the purchase of vape products is a form of market failure.',
       'A way of explaining the failure — any one',
       'One explanation, 6 marks.',
       ref='2024 HL Section A Q7(a)', claim=1, per=6, drop=SCAFFOLD,
       stem='The number of teenagers in Ireland who vape is on the rise.')

P.menu('what you understand by the term price discrimination', 'econ-2024-hl-sa-q8-a',
       'economics-1-1', 'examples-of-price-discrimination',
       'Give an example of price discrimination.',
       'An example of price discrimination — any one',
       'One example, 2 marks; the part pays 4 more for explaining the term.',
       ref='2024 HL Section A Q8(a)', claim=1, per=2,
       drop=SCAFFOLD + ('different consumers and the price difference',))

# ── Q6(b) and Q9(a), built from the scheme directly ─────────────────────────
# Both parts answer two questions at once and head the two halves in the body
# text — "Downward sloping part:", "Opportunity cost:" — rather than as parts of
# their own, so there is nothing in the extractor's output to cut them at.
BODY = tidy(load(2024, 'higher'))
P.cards.append(card(
    'econ-2024-hl-sa-q6-b-down', 2024, 'higher', 'economics-1-5', 'why-average-cost-falls',
    '2024 HL Section A Q6(b) — downward sloping part',
    'Explain the downward sloping part of a firm’s short run average cost curve.',
    '1 @ 2', 2,
    [anyN('r-1', 'A reason average cost falls — any one', 2, 1, 2,
          [as_option(h) for h in heads(
              block(BODY, 'Specialisation/division of labour', 'Upward sloping part'),
              ['Specialisation/division of labour', 'Greater spread of fixed costs'])],
          'One reason, 2 marks; the part pays 2 more for the upward sloping part.')],
    'The part asks about both halves of the curve and the scheme heads them separately, so each '
    'half is its own card.', section='A'))

P.cards.append(card(
    'econ-2024-hl-sa-q6-b-up', 2024, 'higher', 'economics-1-5', 'why-average-cost-rises',
    '2024 HL Section A Q6(b) — upward sloping part',
    'Explain the upward sloping part of a firm’s short run average cost curve.',
    'fixed', 2,
    [point('r-1', as_option(block(BODY, 'The law of diminishing marginal returns - as more',
                                  '7 The number of teenagers in Ireland who vape')), 2,
           'One point, 2 marks. The scheme gives one reason and one only: diminishing marginal '
           'returns.')],
    '', section='A', tariff_kind='fixed'))

for side, half, cid, topic, concept in (
        ('opportunity cost', block(BODY, 'The €2 billion could have been used', 'Social benefit'),
         'econ-2024-hl-sa-q9-a-cost', 'economics-0-1', 'opportunity-cost-of-planting-woodland'),
        ('social benefit', block(BODY, 'It could assist Climate change by helping',
                                 '(b) The Atlantic Technological University'),
         'econ-2024-hl-sa-q9-a-benefit', 'economics-2-2', 'social-benefit-of-planting-woodland')):
    P.cards.append(card(
        cid, 2024, 'higher', topic, concept,
        f'2024 HL Section A Q9(a) — {side}',
        f'Coillte has pledged to add 100,000 hectares of woodland by 2050, at an estimated cost '
        f'of €2 billion. Outline one {side} of this pledge.',
        '1 @ 3', 3,
        [anyN('r-1', f'A {side} of the pledge — any one', 3, 1, 3, bullets(half),
              f'One {side}, 3 marks; the part pays 3 more for the other side.')],
        'The part asks for one opportunity cost and one social benefit and the scheme heads the '
        'two lists separately, so each side is its own card.', section='A'))

# ── Definitions and single-answer parts, built from the scheme directly ─────
# Each prints its tariff beside the part and one answer — or a short list of
# accepted formulations — under it. None is a menu econ_parts can read.
P.cards.append(card(
    'econ-2024-hl-sa-q2-a', 2024, 'higher', 'economics-3-2', 'what-full-employment-is',
    '2024 HL Section A Q2(a)',
    'Explain what you understand by the term full employment.',
    'fixed', 6,
    [point('r-1', as_option(block(BODY, 'Full employment is a situation',
                                  'Answer either (b) or (c)')), 6,
           'One explanation, 6 marks: who counts as employed — everyone in the labour force '
           'willing and able to work at existing wage rates — and the 4% to 5% unemployment '
           'rate it corresponds to in Ireland.')],
    '', section='A', tariff_kind='fixed',
    stem='Ireland’s seasonally adjusted unemployment rate for October 2023 was 4.8%, which '
         'may be regarded as full employment.'))

q3b = block(BODY, 'A price ceiling is a maximum price', 'OR (c)')
P.cards.append(card(
    'econ-2024-hl-sa-q3-b', 2024, 'higher', 'economics-1-3', 'price-ceiling',
    '2024 HL Section A Q3(b)',
    'Explain your understanding of the economic term price ceiling.',
    '2 @ 3', 6,
    [anyN('r-1', 'A point of the explanation — any two', 6, 2, 3,
          [as_option(h) for h in heads(q3b, ['A price ceiling is a maximum price',
                                             'This price may be below the equilibrium',
                                             'A measure put in place to prevent'])],
          'Two points, 3 marks each: what the ceiling is — a legal maximum price — plus its '
          'position below the market equilibrium or its purpose.')],
    '', section='A',
    stem='In an effort to combat the energy crisis, the European Commission considered a €200 '
         'per megawatt hour limit on the price of electricity.'))

P.cards.append(card(
    'econ-2024-hl-sa-q4-c', 2024, 'higher', 'economics-1-5', 'marginal-efficiency-of-capital',
    '2024 HL Section A Q4(c)',
    'Explain the term Marginal Efficiency of Capital (MEC).',
    'fixed', 6,
    [point('r-1', as_option(block(BODY, 'The MEC is the extra profit', '5 Harry Styles')), 6,
           'One definition, 6 marks: the extra profit earned from employing one extra unit of '
           'capital.')],
    '', section='A', tariff_kind='fixed'))

# The explanation beside the MC/AC diagram. Its ⟨3⟩ is printed apart from the
# diagram's ⟨5⟩, so the written half is carded the way the Q11(c) explanations
# are in the Section B script.
P.cards.append(card(
    'econ-2024-hl-sa-q6-a', 2024, 'higher', 'economics-1-5', 'marginal-cost-and-average-cost',
    '2024 HL Section A Q6(a)',
    'With the aid of a fully labelled diagram below (including the axes), explain the '
    'relationship between a firm’s short run average cost curve and its marginal cost curve.',
    'fixed', 3,
    [point('r-1', as_option(block(BODY, 'If marginal cost is less than average cost',
                                  '(b) Explain the shape of the short run')), 3,
           'The written explanation, 3 marks: what average cost does while marginal cost is '
           'below it, above it, and equal to it.')],
    'PARTIAL CARD. The part is worth 8 — 5 for a correctly drawn and labelled diagram and 3 '
    'for the written explanation. Only the explanation is carded; the Mark Bank cannot mark '
    'a drawing.', section='A', tariff_kind='fixed'))

# The explanation of the ticket-shortage diagram. Q5 splits its tariff the way
# Q6 does — ⟨8⟩ for the diagram in (a), ⟨4⟩ for the written explanation in (b) —
# so the written half is carded the same way as sa-q6-a above.
P.cards.append(card(
    'econ-2024-hl-sa-q5-b', 2024, 'higher', 'economics-1-0', 'explaining-a-ticket-shortage',
    '2024 HL Section A Q5(b)',
    'Illustrate with the aid of a fully labelled diagram (including the axes) how a shortage '
    'of tickets for this concert may arise. Explain your diagram.',
    'fixed', 4,
    [point('r-1', as_option(block(BODY, 'The demand for tickets is downward sloping',
                                  '6 (a) With the aid of a fully labelled diagram below')), 4,
           'The written explanation, 4 marks: demand slopes down, supply is fixed / perfectly '
           'inelastic at the 80,000 capacity, and at €97.10 — below the equilibrium price — '
           'there is excess demand.')],
    'Part (a) pays 8 for the fully labelled diagram itself, which is not carded — the Mark '
    'Bank cannot mark a drawing. This card is part (b), the written explanation of it.',
    section='A', tariff_kind='fixed',
    stem='Harry Styles performed a concert at Slane Castle on 10th June 2023 with a maximum '
         'capacity of 80,000 people. The ticket prices for the show were €97.10 each and the '
         'concert sold out in hours.'))

q9b = block(BODY, 'With positive externalities the benefit', '10 The data in the table below')
P.cards.append(card(
    'econ-2024-hl-sa-q9-b', 2024, 'higher', 'economics-2-2', 'positive-externalities',
    '2024 HL Section A Q9(b)',
    'Explain what you understand by the term, positive externality.',
    '1 @ 6', 6,
    [anyN('r-1', 'A way of explaining the term — any one', 6, 1, 6,
          [as_option(h) for h in heads(q9b, ['With positive externalities the benefit',
                                             'Goods / services which give a benefit',
                                             'The existence of ATU will bring benefits'])],
          'One explanation, 6 marks. Society’s benefit exceeding private benefit, or a benefit '
          'to a third party — the ATU line is the scheme’s own illustration.')],
    '', section='A',
    stem='The Atlantic Technological University was launched in April 2022 creating a positive '
         'externality for counties Donegal, Sligo, and Mayo.'))

P.cards.append(card(
    'econ-2024-hl-sa-q10-b', 2024, 'higher', 'economics-3-0', 'net-factor-income-from-abroad',
    '2024 HL Section A Q10(b)',
    'Explain the term Net factor income from abroad.',
    'fixed', 6,
    [point('r-1', as_option(block(BODY, 'Net factor income is the income earned',
                                  'Section B: 300 marks')), 6,
           'One definition, 6 marks, and it runs both ways: Irish factor income repatriated '
           'home MINUS foreign factor income repatriated out.')],
    '', section='A', tariff_kind='fixed'))

# ── The part whose question IS a chart ─────────────────────────────────────
# Excluded until now as a lookup off the figure printed with it. That described
# the response, not a blocker: the crop is catalogued with verified alt text and
# an md5 the build re-checks, so binding it gives the student what the candidate
# in the hall had.

P.cards.append(card(
    'econ-2024-hl-seca-q1-a', 2024, 'higher', 'economics-4-2',
    'calculating-the-current-account-balance', '2024 HL Section A Q1(a)',
    'From the data above, calculate the balance of payments, current account balance. State '
    'whether it is a surplus or a deficit. Show all your workings.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Workings: \u20ac76bn + \u20ac91bn', 'Q2')), 6,
           'The workings and the verdict, 6 marks as one block \u2014 the scheme prints no '
           'split between them. Credits and debits are each totalled off the infographic '
           'before they are subtracted, which is where the arithmetic usually goes wrong.')],
    'Every figure comes off the CSO infographic; nothing is given in the wording. The answer '
    'is a surplus, so a student who subtracts the wrong way round gets the sign as well as the '
    'verdict wrong.',
    tariff_kind='fixed', section='A',
    figure_key='economics-2024-HL-paper-p03-i0'))

# ── Tick tables, answered by the scheme's own completed table ──────────────
# See econ_tick_crop.py: the ✔ is drawn, so extraction keeps the tick and loses
# the column. The completed table is bound as a SOLUTION crop.

P.cards.append(card(
    'econ-2024-hl-seca-q4-a-ticks', 2024, 'higher', 'economics-1-5',
    'capital-deepening-or-widening', '2024 HL Section A Q4(a)',
    'The table below shows a firm\u2019s capital to labour ratio for the previous two years '
    '\u2014 machines 5 then 10, workers 5 then 5, ratio 1:1 then 2:1. Indicate by means of a '
    'tick whether capital widening or capital deepening is occurring.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Capital Widening Capital Deepening',
                                  '(b) Outline two factors which may affect')), 6,
           'Read the completed answer below. It is capital DEEPENING: machines double while the '
           'workforce stays at five, so capital PER WORKER rises from 1:1 to 2:1. Widening would '
           'be more machines AND more workers with the ratio unchanged \u2014 the ratio row is '
           'the whole test.')],
    'Both answers involve buying machines, so counting the machines settles nothing. Only the '
    'ratio distinguishes them.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2024-HL-scheme-p08-q4a-ticks'))

P.emit()
