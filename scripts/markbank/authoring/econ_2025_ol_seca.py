#!/usr/bin/env python3
"""Economics 2025 Ordinary Level — Section A.

Four of these questions are answered either way, and three ask for one response
of each of two kinds — a private benefit and a social benefit, a private cost
and a social cost. The scheme heads each list separately, so each side is its
own card: a student shown one list of ten that argues both ways is not being
asked the question the examiner asked.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2025, 'ordinary', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')
SIDES = ('The part asks for one of each and the scheme heads the two lists separately, so each '
         'side is its own card.')
EITHER = ('The part is answered either way and the scheme heads the two lists separately, so each '
          'side is its own card.')
BOOKS = ('Budget 2025 extended the free schoolbooks scheme to all students at second level.')
LIBRARY = ('Ireland’s newest library opened in Kilkenny, with a further €25 million investment in '
           'the Public Library Service announced.')
VAPES = ('Disposable vapes are to be banned in Ireland. A former minister called them a health '
         'emergency and an epidemic among teenagers.')

P.menu('one economic benefit for Irish consumers of lower electricity prices',
       'econ-2025-ol-sa-q1-ii', 'economics-1-1', 'benefits-of-cheaper-electricity',
       'Outline one economic benefit for Irish consumers of lower electricity prices.',
       'A benefit of cheaper electricity — any one',
       'One benefit, 4 marks.',
       ref='2025 OL Section A Q1(ii)', claim=1, per=4, drop=SCAFFOLD)

P.menu('Norma Foley announced the measure', 'econ-2025-ol-sa-q2-a-yes',
       'economics-0-1', 'free-schoolbooks-as-efficient-use',
       'Do you think extending the free schoolbooks scheme represents an efficient use of scarce '
       'resources? Justify a YES answer.',
       'A reason it is efficient — any one',
       'One justification, 12 marks.',
       ref='2025 OL Section A Q2(a) — yes', claim=1, per=12,
       drop=SCAFFOLD, stop='It is not equitable', stem=BOOKS, notes=EITHER)

P.menu('Norma Foley announced the measure', 'econ-2025-ol-sa-q2-a-no',
       'economics-0-1', 'free-schoolbooks-as-inefficient-use',
       'Do you think extending the free schoolbooks scheme represents an efficient use of scarce '
       'resources? Justify a NO answer.',
       'A reason it is not efficient — any one',
       'One justification, 12 marks.',
       ref='2025 OL Section A Q2(a) — no', claim=1, per=12,
       drop=SCAFFOLD, after='It is not equitable', stem=BOOKS)

P.menu('private benefit or social benefit of the increased use of public libraries',
       'econ-2025-ol-sa-q3-a-private', 'economics-2-2', 'private-benefit-of-public-libraries',
       'Outline one private benefit of the increased use of public libraries.',
       'A private benefit — any one',
       'One benefit, 12 marks.',
       ref='2025 OL Section A Q3(a) — private benefit', claim=1, per=12,
       drop=SCAFFOLD + ('Private Benefit',), stop='Community hub', trim='Social Benefit',
       stem=LIBRARY, notes=SIDES)

P.menu('private benefit or social benefit of the increased use of public libraries',
       'econ-2025-ol-sa-q3-a-social', 'economics-2-2', 'social-benefit-of-public-libraries',
       'Outline one social benefit of the increased use of public libraries.',
       'A social benefit — any one',
       'One benefit, 12 marks.',
       ref='2025 OL Section A Q3(a) — social benefit', claim=1, per=12,
       drop=SCAFFOLD, after='Community hub', stem=LIBRARY)

P.menu('hosting of international sporting', 'econ-2025-ol-sa-q3-b-agree',
       'economics-3-5', 'the-case-for-hosting-events-ol',
       'The Government should continue to support the hosting of international sporting events in '
       'Ireland. Justify AGREEING with this statement.',
       'A reason to agree — any one',
       'One justification, 12 marks.',
       ref='2025 OL Section A Q3(b) — agree', claim=1, per=12,
       drop=SCAFFOLD + ('Justify your answer. Agree',), stop='Opportunity cost', notes=EITHER)

P.menu('hosting of international sporting', 'econ-2025-ol-sa-q3-b-disagree',
       'economics-3-5', 'the-case-against-hosting-events-ol',
       'The Government should continue to support the hosting of international sporting events in '
       'Ireland. Justify DISAGREEING with this statement.',
       'A reason to disagree — any one',
       'One justification, 12 marks.',
       ref='2025 OL Section A Q3(b) — disagree', claim=1, per=12,
       drop=SCAFFOLD, after='Opportunity cost')

P.menu('one reason why the government introduced the above measures', 'econ-2025-ol-sa-q4-a',
       'economics-3-1', 'why-a-budget-cuts-tax',
       'Outline one reason why the government introduced tax band changes, USC cuts and '
       'cost-of-living payments in Budget 2025.',
       'A reason for the budget measures — any one',
       'One reason, 12 marks.',
       ref='2025 OL Section A Q4(a)', claim=1, per=12, drop=SCAFFOLD)

P.menu('Higher incomes / living standards - increasing GDP', 'econ-2025-ol-sa-q5-ii',
       'economics-3-5', 'advantages-of-rising-gdp-ol',
       'Outline one advantage of an increasing GDP for citizens in Ireland.',
       'An advantage of rising GDP — any one',
       'One advantage, 8 marks.',
       ref='2025 OL Section A Q5(ii)', claim=1, per=8, drop=SCAFFOLD,
       stem='Ireland’s GDP was expected to grow by 3.6% in 2025.')

P.menu('disposable vapes are to be banned', 'econ-2025-ol-sa-q6-private',
       'economics-2-2', 'private-cost-of-vaping',
       'Outline one private cost to the individual with the use of disposable vapes.',
       'A private cost — any one',
       'One cost, 8 marks; the part pays 4 more for a social cost.',
       ref='2025 OL Section A Q6 — private cost', claim=1, per=8,
       drop=SCAFFOLD, stop='Healthcare costs', stem=VAPES, notes=SIDES)

P.menu('disposable vapes are to be banned', 'econ-2025-ol-sa-q6-social',
       'economics-2-2', 'social-cost-of-vaping',
       'Outline one social cost to society with the use of disposable vapes.',
       'A social cost — any one',
       'One cost, 4 marks.',
       ref='2025 OL Section A Q6 — social cost', claim=1, per=4,
       drop=SCAFFOLD, after='Healthcare costs', stem=VAPES)

P.menu('economic effect which this increase in the number of people aged', 'econ-2025-ol-sa-q7-ii',
       'economics-3-1', 'ageing-population-and-the-exchequer',
       'Outline one possible economic effect for the Irish Government of the increase in the '
       'number of people aged 65 and over.',
       'An effect on the Government — any one',
       'One effect, 8 marks.',
       ref='2025 OL Section A Q7(ii)', claim=1, per=8,
       drop=SCAFFOLD + ('Irish Government.',),
       stem='The number of people in Ireland aged 65 and over rose by 243,700 between 2014 and '
            '2024.')

P.menu('one factor, other than ticket prices', 'econ-2025-ol-sa-q10-i',
       'economics-1-1', 'what-shifts-demand-for-tickets',
       'Outline one factor, other than ticket prices, that affects a consumer’s demand for '
       'concert tickets.',
       'A factor affecting demand — any one',
       'One factor, 8 marks.',
       ref='2025 OL Section A Q10(i)', claim=1, per=8, drop=SCAFFOLD,
       stem='Oasis will play Croke Park, capacity 82,300, in August 2025.')

# The scheme runs both sides together and marks the break with "No", so each
# side of Q2(b) is its own card.
P.menu('Cost of attending school reduced', 'econ-2025-ol-sa-q2-b-yes',
       'economics-1-3', 'the-case-for-free-schoolbooks',
       'Do you think the Budget 2025 schoolbooks measure was a good use of government '
       'expenditure? Explain YES.',
       'A reason in favour — any one', 'One reason, 12 marks for the part.',
       ref='2025 OL Section A Q2(b) — yes', claim=1, per=12,
       drop=SCAFFOLD, stop='It is not equitable')

P.menu('It is not equitable', 'econ-2025-ol-sa-q2-b-no',
       'economics-1-3', 'the-case-against-free-schoolbooks',
       'Do you think the Budget 2025 schoolbooks measure was a good use of government '
       'expenditure? Explain NO.',
       'A reason against — any one', 'One reason, 12 marks for the part.',
       ref='2025 OL Section A Q2(b) — no', claim=1, per=12, drop=SCAFFOLD)

P.menu('reason why the government introduced the above measures',
       'econ-2025-ol-sa-q4-b', 'economics-1-3', 'why-cost-of-living-measures',
       'Outline one reason why the government introduced the cost-of-living measures.',
       'A reason — any one', 'One reason, 12 marks for the part.',
       ref='2025 OL Section A Q4(b)', claim=1, per=12, drop=SCAFFOLD)

P.emit()
