#!/usr/bin/env python3
"""Economics 2025 Higher Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, card, heads, load, point, tidy  # noqa: E402

P = Paper(2025, 'higher')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'More possible response',
            'Possible benefits:', 'Economic difficulties:')

P.menu('entry of this new firm into the Irish health insurance', 'econ-2025-hl-q11-a-ii',
       'economics-2-0', 'effects-of-new-market-entrant',
       'With the entry of this new firm into the Irish health insurance market, outline two '
       'potential economic effects on the existing firms in the industry.',
       'An effect on the existing firms — any two',
       'Two effects, 7 marks each. The scheme lists gains and losses together — a new entrant is '
       'not simply bad news for the incumbents.',
       drop=SCAFFOLD,
       stem='Level Health, a new health insurance provider, entered the Irish market in November '
            '2024. Three firms already held 97% of it.')

P.menu('effects that the above development may have on existing /', 'econ-2025-hl-q11-c-i',
       'economics-2-1', 'effects-of-a-gp-shortage',
       'Around 700 GPs are due to retire in the next five years. Outline two possible effects '
       'this may have on existing and potential patients.',
       'An effect on patients — any two',
       'Two effects, 4 marks each.',
       drop=SCAFFOLD)

P.menu('sources of comparative advantage in Ireland', 'econ-2025-hl-q13-b-ii',
       'economics-4-2', 'sources-of-comparative-advantage',
       'Outline two sources of comparative advantage in Ireland which help attract foreign '
       'direct investment from pharmaceutical companies.',
       'A source of Ireland’s comparative advantage — any two',
       'Two sources, 6 marks each.',
       drop=SCAFFOLD)

P.menu('benefits of online shopping for consumers', 'econ-2025-hl-q14-a-i',
       'economics-1-1', 'benefits-of-online-shopping',
       'Outline two benefits of online shopping for consumers in Ireland, other than being able '
       'to choose from a wider selection of products.',
       'A benefit of online shopping — any two',
       'Two benefits, 5 marks each. Wider selection is excluded by the question.',
       drop=SCAFFOLD)

P.menu('Amazon plans to open a dedicated store', 'econ-2025-hl-q14-a-ii',
       'economics-2-0', 'amazon-expansion-and-small-retailers',
       'Amazon plans to open a dedicated store in Ireland in 2025. Outline two economic '
       'difficulties this may create for small and medium-sized retailers in Ireland.',
       'A difficulty for small and medium retailers — any two',
       'Two difficulties, 5 marks each.',
       drop=SCAFFOLD)

P.menu('factors, which affect the amount of credit', 'econ-2025-hl-q15-a-ii',
       'economics-3-4', 'factors-affecting-credit-creation',
       'Outline two factors which affect the amount of credit that Irish retail banks can create.',
       'A factor affecting credit creation — any two',
       'Two factors, 6 marks each.',
       drop=SCAFFOLD)

P.menu('Rising property prices is affecting the labour market', 'econ-2025-hl-q15-b-ii',
       'economics-2-1', 'property-prices-and-the-labour-market',
       'Rising property prices are affecting the labour market in Ireland. Discuss two economic '
       'effects this may have on the Irish labour market.',
       'An effect on the labour market — any two',
       'Two effects, 6 marks each.',
       drop=SCAFFOLD)

P.menu('challenges for the Irish economy, if government expenditure on', 'econ-2025-hl-q15-c-ii',
       'economics-3-1', 'challenges-of-cutting-capital-spending',
       'Discuss two possible challenges for the Irish economy if government expenditure on '
       'capital projects were reduced.',
       'A challenge for the economy — any two',
       'Two challenges, 5 marks each.',
       drop=SCAFFOLD)

P.menu('levels of expenditure by the Irish government for the years', 'econ-2025-hl-q15-c-iii',
       'economics-3-1', 'why-government-spending-rose',
       'Explain two economic reasons for the significant increase in government expenditure over '
       'this period.',
       'A reason spending rose — any two',
       'Two reasons, 5 marks each.',
       drop=SCAFFOLD)

P.menu('objectives the owner of the smoothie and juice bar', 'econ-2025-hl-q16-a-iii',
       'economics-1-5', 'firm-objectives-other-than-profit',
       'Outline two objectives the owner of the smoothie and juice bar may pursue other than '
       'profit maximisation.',
       'An objective other than profit — any two',
       'Two objectives, 7 marks each.',
       drop=SCAFFOLD)

P.menu('economic measures the Irish government could implement to help reduce',
       'econ-2025-hl-q16-b-i', 'economics-1-3', 'supporting-small-business',
       'Outline two economic measures the Irish government could implement to help reduce the '
       'pressures facing small businesses.',
       'A measure to support small business — any two',
       'Two measures, 6 marks each.',
       drop=SCAFFOLD)

P.menu('Entrepreneurship is central to Ireland', 'econ-2025-hl-q16-c',
       'economics-0-0', 'importance-of-entrepreneurship',
       'Discuss two reasons why entrepreneurship is important to the continued development of '
       'the Irish economy.',
       'A reason entrepreneurship matters — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD + ('Higher Level Economics',), cap=10)

P.menu('barrier to entry often found in monopoly', 'econ-2025-hl-q11-b-ii',
       'economics-2-0', 'barriers-to-entry-in-monopoly',
       'Outline one barrier to entry often found in monopoly markets, other than a patent.',
       'A barrier to entry — any one',
       'One barrier, 4 marks. Patents are excluded by the question.',
       claim=1, per=4, drop=SCAFFOLD)


# ── A figure card ───────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2025-hl-q9-a', 2025, 'higher', 'economics-2-0', 'labelling-the-kinked-demand-diagram',
    '2025 HL Q9(a)',
    'The diagram represents the long run equilibrium of a firm operating in an oligopoly market. '
    'Write out in full what each of the numbered items 1 to 3 represents.',
    'fixed', 6,
    [point('r-1', 'Marginal cost', 2, 'Item 1 — the green curve rising through point E.'),
     point('r-2', 'Average revenue = Demand', 2, 'Item 2 — the yellow kinked line.'),
     point('r-3', 'Marginal revenue', 2, 'Item 3 — the red line, which breaks vertically under '
                                         'the kink in item 2.')],
    'Abbreviations are not accepted.', tariff_kind='fixed',
    figure_key='economics-2025-HL-paper-p11-art',
    label_key=[{'letter': '1', 'meaning': 'Marginal cost', 'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'Average revenue = Demand', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'Marginal revenue', 'askedInThisQuestion': True},
               {'letter': 'E', 'meaning': 'the equilibrium where marginal cost cuts marginal revenue',
                'askedInThisQuestion': False}]))


# ── Section B, second pass ──────────────────────────────────────────────────
# The first pass covered every topic of the specification; it did not cover
# every part. These are the parts of this paper that list named responses and
# had no card citing them, found by econ_todo.py.
SIDES = ('The part asks for one of each and the scheme heads the two lists separately, so each '
         'side is its own card.')

P.menu('economic advantage and one economic disadvantage for consumers',
       'econ-2025-hl-q11-b-iii-adv', 'economics-2-0', 'monopoly-advantages-for-consumers',
       'Outline one economic advantage for consumers if a pharmaceutical company has monopoly '
       'power.',
       'An advantage to consumers — any one',
       'One advantage, 4 marks.',
       ref='2025 HL Q11(b)(iii) — advantage', claim=1, per=4,
       drop=SCAFFOLD, stop='Economic Disadvantage for Consumers', notes=SIDES)

P.menu('economic advantage and one economic disadvantage for consumers',
       'econ-2025-hl-q11-b-iii-dis', 'economics-2-0', 'monopoly-disadvantages-for-consumers',
       'Outline one economic disadvantage for consumers if a pharmaceutical company has monopoly '
       'power.',
       'A disadvantage to consumers — any one',
       'One disadvantage, 4 marks.',
       ref='2025 HL Q11(b)(iii) — disadvantage', claim=1, per=4,
       drop=SCAFFOLD, after='Economic Disadvantage for Consumers')

P.menu('Suggest one economic measure the Irish government could take to address',
       'econ-2025-hl-q11-c-ii', 'economics-2-1', 'addressing-a-shortage-of-gps',
       'More than three-quarters of GP practices in Ireland have closed their lists to new '
       'patients. Suggest one economic measure the Irish government could take to address this.',
       'A measure to ease the GP shortage — any one',
       'One measure, 4 marks.',
       ref='2025 HL Q11(c)(ii)', claim=1, per=4,
       drop=SCAFFOLD + ('More possible responses on next page',))

# The scheme runs three worked examples together under one "Any relevant
# example:" heading with no bullet between them, so the extractor hands back one
# 746-character option -- which the audit refuses, and rightly: a student would
# be shown three answers as though they were one. Cut at the sectors themselves.
_MIXED = tidy(load(2025, 'higher'))
P.cards.append(card(
    'econ-2025-hl-q11-c-iii', 2025, 'higher', 'economics-1-0',
    'evidence-that-ireland-is-a-mixed-economy', '2025 HL Q11(c)(iii)',
    'Outline an example which shows that Ireland is a mixed economy.',
    '1 @ 8', 8,
    [anyN('r-1', 'An example of the mixed economy — any one', 8, 1, 8,
          [as_option(h) for h in heads(
              block(_MIXED, 'Education – Ireland’s school system includes both public',
                    'Possible Responses'),
              ['Education –', 'Transport –', 'Energy –', 'State regulation –'])],
          'One example, 8 marks. The part pays the same 8 for explaining the term itself.')],
    'Each example names a sector where the State and private firms both operate — which is what '
    'a mixed economy is.', tariff_kind='bestNofParts'))

P.menu('economic advantage of Ireland reducing its level of general government debt',
       'econ-2025-hl-q12-a-ii-tax', 'economics-3-1', 'lower-debt-and-the-taxpayer',
       'Outline one economic advantage of Ireland reducing its level of general government debt '
       'for taxpayers in Ireland.',
       'An advantage to taxpayers — any one',
       'One advantage, 7 marks.',
       ref='2025 HL Q12(a)(ii) — taxpayers', claim=1, per=7,
       drop=SCAFFOLD, stop='The Irish government', notes=SIDES)

P.menu('economic advantage of Ireland reducing its level of general government debt',
       'econ-2025-hl-q12-a-ii-gov', 'economics-3-1', 'lower-debt-and-the-exchequer',
       'Outline one economic advantage of Ireland reducing its level of general government debt '
       'for the Irish government.',
       'An advantage to the government — any one',
       'One advantage, 7 marks.',
       ref='2025 HL Q12(a)(ii) — government', claim=1, per=7,
       drop=SCAFFOLD, after='Lower annual interest repayments')

P.menu('more accurate measure of Ireland', 'econ-2025-hl-q12-a-iii',
       'economics-3-0', 'why-gni-star-beats-gdp',
       'Which is the more accurate measure of Ireland’s debt burden: debt as a percentage of '
       'GNI* or debt as a percentage of GDP? Justify your choice.',
       'A justification — any one',
       'One justification, 6 marks. Every response the scheme lists argues for GNI*.',
       ref='2025 HL Q12(a)(iii)', claim=1, per=6, drop=SCAFFOLD)

P.menu('higher rate of income tax on individuals who earn above', 'econ-2025-hl-q12-b-iii-agree',
       'economics-3-1', 'the-case-for-a-higher-top-rate',
       'Some politicians are debating a higher rate of income tax on individuals earning above '
       '€100,000. Argue that you AGREE.',
       'A reason to agree — any one',
       'One argument, 8 marks.',
       ref='2025 HL Q12(b)(iii) — agree', claim=1, per=8,
       drop=SCAFFOLD, stop='Negative impact on FDI',
       notes='The part is answered either way and the scheme lists the responses for each side, '
             'so each side is its own card.')

P.menu('higher rate of income tax on individuals who earn above', 'econ-2025-hl-q12-b-iii-disagree',
       'economics-3-1', 'the-case-against-a-higher-top-rate',
       'Some politicians are debating a higher rate of income tax on individuals earning above '
       '€100,000. Argue that you DISAGREE.',
       'A reason to disagree — any one',
       'One argument, 8 marks.',
       ref='2025 HL Q12(b)(iii) — disagree', claim=1, per=8,
       drop=SCAFFOLD, after='Negative impact on FDI')

P.menu('economic advantage to the employee and one possible economic disadvantage to the employer',
       'econ-2025-hl-q12-c-i-employee', 'economics-2-1', 'auto-enrolment-and-the-employee',
       'Outline one possible economic advantage to the employee of the auto-enrolment pension '
       'scheme.',
       'An advantage to the employee — any one',
       'One advantage, 7 marks.',
       ref='2025 HL Q12(c)(i) — employee', claim=1, per=7,
       drop=SCAFFOLD, stop='Economic Disadvantage to the Employer', notes=SIDES)

P.menu('economic advantage to the employee and one possible economic disadvantage to the employer',
       'econ-2025-hl-q12-c-i-employer', 'economics-2-1', 'auto-enrolment-and-the-employer',
       'Outline one possible economic disadvantage to the employer of the auto-enrolment pension '
       'scheme.',
       'A disadvantage to the employer — any one',
       'One disadvantage, 7 marks.',
       ref='2025 HL Q12(c)(i) — employer', claim=1, per=7,
       drop=SCAFFOLD, after='Higher business costs')

P.menu('pension scheme may influence the multiplier effect', 'econ-2025-hl-q12-c-ii',
       'economics-3-0', 'pension-saving-and-the-multiplier',
       'Discuss how the auto-enrolment pension scheme may influence the multiplier effect in '
       'Ireland in the short term.',
       'A step in the argument — either one',
       'The scheme’s verdict is that the multiplier gets WEAKER, and the 7 marks are for the '
       'mechanism that gets you there.',
       ref='2025 HL Q12(c)(ii)', claim=1, per=7,
       drop=SCAFFOLD + ('Ireland in the short term', 'It will result in a weaker multiplier'))

P.menu('economic benefit and one economic challenge of Ireland', 'econ-2025-hl-q13-a-ii-benefit',
       'economics-4-2', 'benefits-of-exporting-2025',
       'Outline one economic benefit of Ireland’s exports for the Irish economy.',
       'A benefit of exporting — any one',
       'One benefit, 7 marks.',
       ref='2025 HL Q13(a)(ii) — benefit', claim=1, per=7,
       drop=SCAFFOLD + ('Economic Benefit:',), stop='Economic Challenge', notes=SIDES)

P.menu('economic benefit and one economic challenge of Ireland', 'econ-2025-hl-q13-a-ii-challenge',
       'economics-4-2', 'challenges-of-an-export-led-economy',
       'Outline one economic challenge of Ireland’s exports for the Irish economy.',
       'A challenge of exporting — any one',
       'One challenge, 7 marks.',
       ref='2025 HL Q13(a)(ii) — challenge', claim=1, per=7,
       drop=SCAFFOLD, after='Vulnerability to external shocks')

P.menu('outflows of FDI from Ireland are important', 'econ-2025-hl-q13-a-iii',
       'economics-4-1', 'why-outward-fdi-matters',
       'Ireland is the ninth-largest contributor of foreign direct investment into the US. '
       'Outline one economic reason why such outflows of FDI are important for the Irish economy.',
       'A reason outward FDI matters — any one',
       'One reason, 7 marks.',
       ref='2025 HL Q13(a)(iii)', claim=1, per=7, drop=SCAFFOLD)

P.menu('World Trade Organisation (WTO) plays a crucial role', 'econ-2025-hl-q13-b-iii',
       'economics-4-2', 'functions-of-the-wto',
       'The World Trade Organisation (WTO) plays a crucial role in global trade. Outline one '
       'function of the WTO.',
       'A function of the WTO — any one',
       'One function, 6 marks.',
       ref='2025 HL Q13(b)(iii)', claim=1, per=6, drop=SCAFFOLD)

P.menu('Irish government failing to reach the UN', 'econ-2025-hl-q13-c-i',
       'economics-4-0', 'why-ireland-misses-the-aid-target',
       'Outline one possible economic reason for the Irish government failing to reach the UN '
       'target for overseas development aid.',
       'A reason the target was missed — any one',
       'One reason, 7 marks.',
       ref='2025 HL Q13(c)(i)', claim=1, per=7, drop=SCAFFOLD)

P.menu('benefit that Ireland', 'econ-2025-hl-q13-c-ii',
       'economics-4-0', 'what-overseas-aid-does-for-ldcs',
       'Outline one possible economic benefit that Ireland’s overseas development aid provides to '
       'least developed countries.',
       'A benefit to the recipient — any one',
       'One benefit, 7 marks.',
       ref='2025 HL Q13(c)(ii)', claim=1, per=7, drop=SCAFFOLD)

P.menu('challenge for LDCs who have become dependent on international aid', 'econ-2025-hl-q13-c-iii',
       'economics-4-0', 'the-cost-of-aid-dependence',
       'Outline one challenge for least developed countries that have become dependent on '
       'international aid.',
       'A cost of aid dependence — any one',
       'One challenge, 7 marks.',
       ref='2025 HL Q13(c)(iii)', claim=1, per=7, drop=SCAFFOLD + ('Possible Responses',))

P.menu('advances in technology can influence Ireland', 'econ-2025-hl-q14-a-iii-agri',
       'economics-1-2', 'technology-in-irish-agriculture',
       'Outline one way changes in technology may affect how the agriculture sector operates.',
       'A way technology changes farming — any one',
       'One way, 5 marks.',
       ref='2025 HL Q14(a)(iii) — agriculture', claim=1, per=5,
       drop=SCAFFOLD, stop='Sports & Fitness',
       notes='The part offers agriculture or sport and the scheme heads the two lists separately, '
             'so each sector is its own card.')

P.menu('advances in technology can influence Ireland', 'econ-2025-hl-q14-a-iii-sport',
       'economics-1-2', 'technology-in-sport-and-fitness',
       'Outline one way changes in technology may affect how the sports and fitness sector '
       'operates.',
       'A way technology changes sport — any one',
       'One way, 5 marks.',
       ref='2025 HL Q14(a)(iii) — sport', claim=1, per=5,
       drop=SCAFFOLD, after='Sports & Fitness')

# ── Q15(a)(i): the gig economy ─────────────────────────────────────────────
# The scheme runs both sides together and marks the break with "DISAGREE
# responses overleaf DISAGREE:", so each side is its own card.
P.menu('Do you agree or disagree with the statement', 'econ-2025-hl-q15-a-i-agree',
       'economics-3-5', 'the-case-for-regulating-gig-work',
       'Gig economy workers need greater protection and regulation. Do you AGREE with the '
       'statement? Explain your answer.',
       'A reason to agree — any one', 'One reason, 7 marks.',
       ref='2025 HL Q15(a)(i) — agree', claim=1, per=7,
       drop=SCAFFOLD, stop='DISAGREE responses overleaf')

P.menu('Do you agree or disagree with the statement', 'econ-2025-hl-q15-a-i-disagree',
       'economics-3-5', 'the-case-against-regulating-gig-work',
       'Gig economy workers need greater protection and regulation. Do you DISAGREE with the '
       'statement? Explain your answer.',
       'A reason to disagree — any one', 'One reason, 7 marks.',
       ref='2025 HL Q15(a)(i) — disagree', claim=1, per=7,
       drop=SCAFFOLD + ('DISAGREE responses overleaf',), after='DISAGREE responses overleaf')

# ── Q14(c)(ii): full employment ────────────────────────────────────────────
P.menu('positive and one negative economic effect of full employment',
       'econ-2025-hl-q14-c-ii-positive', 'economics-3-2',
       'positive-effects-of-full-employment',
       'Outline one POSITIVE economic effect of full employment on the Irish economy.',
       'A positive effect — any one', 'One positive effect, 6 marks; a negative one is '
       'worth 6 as well.',
       ref='2025 HL Q14(c)(ii) — positive', claim=1, per=6,
       drop=SCAFFOLD, stop='Negative')

P.emit()
