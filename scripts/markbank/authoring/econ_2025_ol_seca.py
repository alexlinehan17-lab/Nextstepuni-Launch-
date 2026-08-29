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
from econ_lib import anyN, as_option, block, bullets, card, heads, load, point, tidy  # noqa: E402

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

# ── The read-the-answer parts of this section ───────────────────────────────
# Each is one printed answer with its tariff printed beside it, sliced by
# anchor — the shape econ_2024_ol.py established. econ_parts cannot see them
# because none lists a menu of responses.
T = tidy(load(2025, 'ordinary'))

P.cards.append(card(
    'econ-2025-ol-sa-q1-i', 2025, 'ordinary', 'economics-3-0', 'what-cso-stands-for',
    '2025 OL Section A Q1(i)',
    'What do the initials CSO stand for? S is completed for your benefit.',
    '2 @ 4', 8,
    [point('r-1', as_option(block(T, 'Central Statistics Office')), 8,
           'Two initials to complete, 4 marks each; the S is given.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2025-ol-sa-q5-i', 2025, 'ordinary', 'economics-3-0', 'what-gdp-stands-for',
    '2025 OL Section A Q5(i)',
    'What do the initials GDP stand for? P is completed for your benefit.',
    'fixed', 4,
    [point('r-1', as_option(block(T, 'GROSS DOMESTIC PRODUCT')), 4,
           'The scheme prints ⟨4⟩ for the part as a whole; the P is given.')],
    '', stem='Ireland’s GDP was expected to grow by 3.6% in 2025.',
    section='A', tariff_kind='fixed'))

# The figure is the artwork crop of the vertical supply curve — the reason for
# its shape is the thing the part asks about, so the diagram rides the card.
P.cards.append(card(
    'econ-2025-ol-sa-q10-ii', 2025, 'ordinary', 'economics-1-2',
    'why-ticket-supply-is-vertical', '2025 OL Section A Q10(ii)',
    'The diagram shows the supply curve for tickets for this event. Explain the reason for '
    'the shape of this supply curve.',
    'fixed', 4,
    [point('r-1', as_option(block(T, 'The supply of tickets is fixed')), 4,
           'One reason, 4 marks: the stadium holds 82,300 whatever the ticket price, so '
           'supply cannot respond to price and the curve is vertical.')],
    '', stem='Oasis will play Croke Park, capacity 82,300, in August 2025.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2025-OL-paper-p10-art',
    label_key=[{'letter': 'S', 'meaning': 'the supply of tickets — vertical at the stadium’s '
                                          'capacity of 82,300', 'askedInThisQuestion': True}]))

# ── The either/or halves of questions 2 and 4 ──────────────────────────────
# Two earlier cards cited Q2(b) with a question of their own invention — the
# paper's (b) is a definition, not a second run at the schoolbooks debate —
# and a third re-carded Q4(a)'s responses as Q4(b). All three are deleted;
# these are the parts the paper actually prints. The ⟨12⟩ each question
# carries is printed once and covers whichever of (a) or (b) is answered,
# the reading econ_2023_ol_seca.py established for the same layout.
P.cards.append(card(
    'econ-2025-ol-sa-q2-b', 2025, 'ordinary', 'economics-3-1',
    'government-current-budget-surplus', '2025 OL Section A Q2(b)',
    'The Irish government has planned for a current budget surplus once again for 2025. '
    'Explain the term government current budget surplus.',
    'fixed', 12,
    [point('r-1', as_option(block(T, 'When government current revenue exceeds',
                                  '3 Answer either')), 12,
           'One explanation, 12 marks.')],
    'The ⟨12⟩ is printed once beside Question 2 and covers whichever of (a) or (b) is '
    'answered.',
    section='A', tariff_kind='fixed'))

# The scheme ticks Yes and lists three explanations; the extractor welds them
# past the "OR" onto Q4(a), so they are sliced by anchor here.
P.cards.append(card(
    'econ-2025-ol-sa-q4-b', 2025, 'ordinary', 'economics-3-1',
    'opportunity-cost-of-budget-measures', '2025 OL Section A Q4(b)',
    'Is there an opportunity cost of these measures to the government? Place a tick (✔) in '
    'the relevant box below and explain your answer.',
    '1 @ 12', 12,
    [anyN('r-1', 'A reason there is an opportunity cost — any one', 12, 1, 12,
          [as_option(h) for h in heads(
              block(T, 'Less tax revenue for the government', '5 Ireland’s GDP'),
              ['Less tax revenue for the government',
               'Government now more reliant on corporation tax',
               'Alternative use of funds'])],
          'The scheme ticks Yes; the 12 marks cover the tick and one explanation.')],
    'The ⟨12⟩ is printed once beside Question 4 and covers whichever of (a) or (b) is '
    'answered.',
    stem='Budget 2025 included changes to the threshold of the higher tax bracket, along '
         'with USC cuts and cost-of-living payments.',
    section='A', tariff_kind='bestNofParts'))

# Question 8 prints ONE descending pair — 1st x 8, 2nd x 4 — against a question
# whose two parts ask for exactly two things: the tick in (i) and this barrier
# in (ii). So the 8 is the tick and the 4 the barrier, the reading
# econ_2023_ol_seca.py took for the same layout on its Q9. The tick itself is
# in econ_excluded; the barrier menu is prose and is carded.
P.cards.append(card(
    'econ-2025-ol-sa-q8-ii', 2025, 'ordinary', 'economics-2-0',
    'barriers-to-entry-in-a-monopoly', '2025 OL Section A Q8(ii)',
    'In a monopoly market structure, there are barriers to entry. Outline one such possible '
    'barrier to entry.',
    '1 @ 4', 4,
    [anyN('r-1', 'A barrier to entry — any one', 4, 1, 4,
          bullets(block(T, 'The Government may grant a company the sole right',
                        '9 In September 2024')),
          'One barrier, 4 marks.')],
    '',
    section='A', tariff_kind='bestNofParts'))

# ── Worked calculations the scheme prints in full ──────────────────────────
# Excluded until now as "the response is the worked calculation". That is a
# description of the answer, not a blocker: the scheme sets out the formula, the
# substitution and the result, so every step a student is credited for is on the
# page and traces. Where the figures come off a chart the crop rides with the
# card, because the arithmetic is unanswerable without it.

P.cards.append(card(
    'econ-2025-ol-seca-q7-i', 2025, 'ordinary', 'economics-3-1',
    'percentage-increase-in-the-over-65-population', '2025 OL Section A Q7(i)',
    'The number of people aged 65 and over has increased by 243,700. Calculate the percentage '
    'increase in number of people aged 65 and over from 2014 to 2024. Show all your workings.',
    '4', 4,
    [point('r-1', as_option(block(T, '243,700 x 100 = 41.3',
                                  '(ii) Outline one possible economic effect')), 4,
           'The increase is given; the 2014 population is the denominator. Dividing by the 2024 '
           'figure instead is the standard error here.')],
    'The question hands over the change but not the base, so the base has to be taken from the '
    'table before the division can happen.',
    tariff_kind='fixed', section='A'))

# ── Tick tables, answered by the scheme's own completed table ──────────────
# See econ_tick_crop.py: the ✔ is drawn, so extraction keeps it and loses the
# column. The completed table is bound as a SOLUTION crop, hidden until reveal.

P.cards.append(card(
    'econ-2025-ol-seca-q8-i-ticks', 2025, 'ordinary', 'economics-2-0',
    'which-firm-is-a-monopoly', '2025 OL Section A Q8(i)',
    'Identify, with a tick (\u2714), which one of the following firms exist in a monopoly '
    'market structure: Ryanair; An Post (mail service for letter post); Vodafone.',
    '1st @ 8+2nd @ 4', 12,
    [point('r-1', as_option(block(T, 'Name of Organisation Tick', '(ii) In a monopoly market')), 12,
           'Read the completed table below. Only An Post\u2019s letter post is ticked: it is '
           'the sole legal supplier, which is what a monopoly means. Ryanair and Vodafone are '
           'large and well known but both compete with rivals, and size is not market structure.')],
    'The trap is reading "monopoly" as "big". Ryanair carries far more passengers than An Post '
    'carries letters, and it is still not a monopoly.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2025-OL-scheme-p14-q8i-ticks'))

P.emit()
