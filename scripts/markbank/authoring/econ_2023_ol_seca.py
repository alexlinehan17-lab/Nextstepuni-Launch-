#!/usr/bin/env python3
"""Economics 2023 Ordinary Level — Section A.

The richest Ordinary Section A of the five years: seven of its ten questions
are answered from a list the examiner wrote out rather than by completing a
table or reading a figure.

The paper offers (a) or (b) on four of these questions and the two alternatives
are worth the same 12 marks, split 8 for the first response and 4 for the
second — which is why so many of these cards carry a descending tariff rather
than a flat one.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

P = Paper(2023, 'ordinary', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('Outline two functions of the Central Bank of Ireland', 'econ-2023-ol-sa-q2-b',
       'economics-3-4', 'functions-of-the-central-bank-ol',
       'Outline two functions of the Central Bank of Ireland.',
       'A function of the Central Bank — any two',
       'Two functions, the first paid 8 and the second 4.',
       ref='2023 OL Section A Q2(b)', steps=[8, 4], drop=SCAFFOLD,
       stem='In 2021 KBC Bank and Ulster Bank announced their intentions to withdraw from the '
            'Irish market.')

P.menu('one economic effect of a skilled labour shortage', 'econ-2023-ol-sa-q3-a-ii',
       'economics-2-1', 'effects-of-a-skills-shortage',
       'Outline one economic effect of a skilled labour shortage for the Irish economy.',
       'An effect of a skills shortage — any one',
       'One effect, 4 marks; the paper pays 8 for naming the area short of skills.',
       ref='2023 OL Section A Q3(a)(ii)', claim=1, per=4, drop=SCAFFOLD)

P.menu('measures the Irish government could take to address this labour shortage',
       'econ-2023-ol-sa-q3-b', 'economics-2-1', 'measures-to-address-a-labour-shortage',
       'Outline two measures the Irish government could take to address a labour shortage.',
       'A measure to address the shortage — any two',
       'Two measures, the first paid 8 and the second 4.',
       ref='2023 OL Section A Q3(b)', steps=[8, 4], drop=SCAFFOLD)

P.menu('two characteristics of a monopoly market', 'econ-2023-ol-sa-q4-b',
       'economics-2-0', 'characteristics-of-a-monopoly',
       'Outline two characteristics of a monopoly market.',
       'A characteristic of a monopoly — any two',
       'Two characteristics, the first paid 8 and the second 4.',
       ref='2023 OL Section A Q4(b)', steps=[8, 4], drop=SCAFFOLD)

P.menu('one advantage of increasing GDP for the Irish economy', 'econ-2023-ol-sa-q6-ii',
       'economics-3-5', 'advantages-of-rising-gdp',
       'Outline one advantage of an increasing GDP for the Irish economy.',
       'An advantage of rising GDP — any one',
       'One advantage, 4 marks.',
       ref='2023 OL Section A Q6(ii)', claim=1, per=4, drop=SCAFFOLD,
       stem='Ireland’s GDP was predicted to increase by 2.7% in 2023.')

P.menu('Corporation tax receipts in Ireland rose', 'econ-2023-ol-sa-q7',
       'economics-3-1', 'why-a-government-collects-tax',
       'Explain two reasons why the government in Ireland collects tax.',
       'A reason government collects tax — any two',
       'Two reasons, the first paid 8 and the second 4.',
       ref='2023 OL Section A Q7', steps=[8, 4], drop=SCAFFOLD,
       stem='Corporation tax receipts in Ireland rose by 52.9% to €8.8 billion between June 2021 '
            'and June 2022, almost a quarter of all tax collected.')

# ── Q10, built from the scheme directly ────────────────────────────────────
# "Private benefit:" and "Social benefit:" are bare headings between bullets, so
# each arrives glued to the response above it and there is no bullet to cut the
# list at. Sliced here at the headings themselves.
BODY = tidy(load(2023, 'ordinary'))
for side, half, cid, concept, marks in (
        ('private', block(BODY, 'Teenagers will have more disposable income', 'Social benefit'),
         'econ-2023-ol-sa-q10-private', 'private-benefit-of-curbing-vaping', 8),
        ('social', block(BODY, 'Healthier young population', 'Question 11'),
         'econ-2023-ol-sa-q10-social', 'social-benefit-of-curbing-vaping', 4)):
    P.cards.append(card(
        cid, 2023, 'ordinary', 'economics-2-2', concept,
        f'2023 OL Section A Q10 — {side} benefit',
        f'The government wants to reduce vaping among young Irish teenagers. State one {side} '
        f'benefit if this government intervention is successful.',
        f'1 @ {marks}', marks,
        [anyN('r-1', f'A {side} benefit — any one', marks, 1, marks, bullets(half),
              f'One {side} benefit, {marks} marks.')],
        'The part asks for one private and one social benefit and the scheme heads the two lists '
        'separately, so each side is its own card. The paper pays 8 for the private benefit and '
        '4 for the social one.', section='A'))


# ── The parts the extractor could not segment, sliced by hand ───────────────
# Question 2 prints its descending tariff beside the STEM — the "1st @ 8 /
# 2nd @ 4" pair spans whichever of (a)/(b) is answered — and "Answer either
# (a) or (b)" reads as a part marker, so econ_parts never yields a Q2(a) part
# for find() to reach. Sliced from the scheme's own bullet list instead.
P.cards.append(card(
    'econ-2023-ol-sa-q2-a', 2023, 'ordinary', 'economics-3-4',
    'effects-of-banks-exiting-the-market', '2023 OL Section A Q2(a)',
    'Outline two effects on the Irish consumer of KBC Bank and Ulster Bank leaving the Irish '
    'banking market.',
    '1 @ 8+1 @ 4', 12,
    [anyN('r-1', 'An effect on the Irish consumer — any two', None, 2, 8,
          bullets(block(BODY, 'Less choice for the consumer', 'OR (b) Outline two functions')),
          'Two effects, the first paid 8 and the second 4.', steps=[8, 4])],
    'The tariff is printed once beside the stem and covers whichever of (a) or (b) is '
    'answered — the same pair the carded (b) claims.',
    stem='In 2021, KBC Bank and Ulster Bank announced their intentions to withdraw from the '
         'Irish market.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-ol-sa-q3-a-i', 2023, 'ordinary', 'economics-2-1',
    'areas-of-skills-shortage', '2023 OL Section A Q3(a)(i)',
    'Identify one area where the Irish economy is experiencing a skills shortage.',
    '1 @ 8', 8,
    [anyN('r-1', 'An area short of skills — any one', 8, 1, 8,
          bullets(block(BODY, 'Hospitality sector', '(ii) Outline one economic effect'))
          + ['Transport.'],
          'One area, 8 marks; the paper pays 4 more for the effect in (ii). The scheme lists '
          'five sectors; "Transport." is its fifth bullet, appended whole because it is too '
          'short for the bullet splitter to keep.')],
    '', section='A'))

P.cards.append(card(
    'econ-2023-ol-sa-q4-a-ii', 2023, 'ordinary', 'economics-2-0',
    'what-a-monopoly-is', '2023 OL Section A Q4(a)(ii)',
    'Explain the term monopoly in economics.',
    '1 @ 4', 4,
    [anyN('r-1', 'A way of putting it — any one', 4, 1, 4,
          [as_option(block(BODY, a, b)) for a, b in (
              ('A monopoly exists when there is only one firm', 'A monopoly is the sole supplier'),
              ('A monopoly is the sole supplier', 'The firm can control the price or quantity'),
              ('The firm can control the price or quantity', 'OR (b) Outline two characteristics'))],
          'One explanation, 4 marks; the paper pays 8 for the tick in (i). The scheme gives '
          'three sentences of the same idea.')],
    '', section='A'))

P.cards.append(card(
    'econ-2023-ol-sa-q5', 2023, 'ordinary', 'economics-1-2',
    'fixed-supply-of-tickets', '2023 OL Section A Q5',
    'The diagram below represents the supply of tickets for the Rugby World Cup in France in '
    'September 2023. Explain the relationship between the price of tickets and the supply of '
    'tickets.',
    '1 @ 12', 12,
    [point('r-1', as_option(block(BODY, 'The supply of tickets for the Rugby World Cup is fixed',
                                  '6. Ireland’s GDP is predicted')), 12,
           'The one relationship the diagram supports, 12 marks.')],
    'Not the law of supply: the S1 the paper draws is vertical, so the quantity of tickets '
    'cannot respond to price at all.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2023-OL-paper-p07-i0'))

P.cards.append(card(
    'econ-2023-ol-sa-q6-i', 2023, 'ordinary', 'economics-3-0',
    'what-gdp-stands-for', '2023 OL Section A Q6(i)',
    'What do the initials GDP stand for? G is completed for your benefit.',
    '2 @ 4', 8,
    [point('r-1', 'DOMESTIC', 4, 'The D — Gross is completed on the paper.'),
     point('r-2', 'PRODUCT', 4, 'The P.')],
    'Gross DOMESTIC PRODUCT — the two blanks, 4 marks each.',
    stem='Ireland’s GDP is predicted to increase by 2.7% in 2023.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-ol-sa-q8-i', 2023, 'ordinary', 'economics-4-0',
    'elements-of-the-hdi', '2023 OL Section A Q8(i)',
    'Name two of the three areas (elements) that the Human Development Index (HDI) measures. '
    'One has been completed for your benefit.',
    '1 @ 4+1 @ 2', 6,
    [anyN('r-1', 'The two areas left to name', None, 2, 4,
          ['EDUCATION', 'LIFE EXPECTANCY'],
          'Gross National Income is the area completed on the paper; the first named is paid 4 '
          'and the second 2.', steps=[4, 2])],
    '', stem='Ireland ranks eighth highest in the world on the Human Development Index (HDI).',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-ol-sa-q8-ii', 2023, 'ordinary', 'economics-4-0',
    'expenditure-behind-irelands-hdi', '2023 OL Section A Q8(ii)',
    'In your opinion, what area of government expenditure has helped Ireland to achieve its '
    'position as eighth in the world on the HDI? Explain your answer.',
    '1 @ 4+1 @ 2', 6,
    [point('r-1', 'Education', 4, 'The scheme’s suggested area of expenditure, 4 marks.'),
     point('r-2', as_option(block(BODY, 'An educated workforce is able to gain employment',
                                  '9. (i) Explain the term')), 2,
           'The explanation, 2 marks.')],
    'An opinion question, marked on its merits — the scheme’s model answer is education.',
    section='A', tariff_kind='fixed'))

# Question 9 prints ONE descending pair — 1st @ 8, 2nd @ 4 — against a question
# whose two parts ask for exactly two things, and a Section A question is 12
# marks. So the 8 is the (i) definition and the 4 the (ii) opportunity cost;
# both ride one card under the bare Q9, the way sa-q7 does, because five words
# of question text could never be placed in the paper on their own.
P.cards.append(card(
    'econ-2023-ol-sa-q9', 2023, 'ordinary', 'economics-0-1',
    'opportunity-cost-and-housing-spend', '2023 OL Section A Q9',
    'Explain the term opportunity cost. Outline one opportunity cost involved in the '
    'government expenditure on social and affordable housing.',
    '1 @ 8+1 @ 4', 12,
    [anyN('r-1', 'The definition — either wording', 8, 1, 8,
          bullets(block(BODY, 'The cost of the foregone alternatives', '(ii) Capital funding')),
          'One definition, 8 marks; the scheme also accepts a fully explained example.'),
     point('r-2', as_option(block(BODY, 'The Irish government could have spent the money',
                                  '10. The government is currently looking')), 4,
           'One opportunity cost of the housing spend, 4 marks.')],
    '',
    stem='Capital funding of €2.3bn has been allocated for social and affordable housing in '
         'Budget 2023.',
    section='A', tariff_kind='fixed'))

P.emit()
