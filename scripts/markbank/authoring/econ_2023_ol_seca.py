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
from econ_lib import anyN, block, bullets, card, load, tidy  # noqa: E402

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

P.emit()
