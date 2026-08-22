#!/usr/bin/env python3
"""Economics 2025 Higher Level — Section A.

Six of these ten questions are answered either way — agree or disagree, an
argument for and an argument against, beneficial or not beneficial — and the
scheme heads the two lists separately. Each side is its own card, which is the
rule for parallel accounts: a student choosing two responses from a list of ten
that argues both ways is not answering the question the examiner asked.

On the tariff: this scheme heads Section A "(75 marks)" while the paper prints
100, and prints ⟨6⟩ against each of the two lists of a two-sided part rather
than a split of one figure. Every card here carries the cell the scheme printed
beside its own list, which is the same rule the rest of this subject follows.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2025, 'higher', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')
EVENTS = ('Germany hosted the European Football Championship in 2024. 2.7 million people '
          'attended the 51 matches.')

P.menu('one argument for and one argument against', 'econ-2025-hl-sa-q1-a-for',
       'economics-3-5', 'the-case-for-hosting-a-major-event',
       'Discuss one argument FOR the view that hosting a major sporting event, such as Euro 2024, '
       'benefits the host country’s economy.',
       'An argument for hosting — any one',
       'One argument, 6 marks.',
       ref='2025 HL Section A Q1(a) — argument for', claim=1, per=6,
       drop=SCAFFOLD, stop='Argument against', stem=EVENTS,
       notes='The part asks for an argument on each side and the scheme heads the two lists '
             'separately, so each side is its own card.')

P.menu('one argument for and one argument against', 'econ-2025-hl-sa-q1-a-against',
       'economics-3-5', 'the-case-against-hosting-a-major-event',
       'Discuss one argument AGAINST the view that hosting a major sporting event, such as '
       'Euro 2024, benefits the host country’s economy.',
       'An argument against hosting — any one',
       'One argument, 6 marks.',
       ref='2025 HL Section A Q1(a) — argument against', claim=1, per=6,
       drop=SCAFFOLD, after='Argument against', stem=EVENTS)

P.menu('economic factors which some households in Ireland may consider', 'econ-2025-hl-sa-q2-b',
       'economics-3-0', 'what-households-weigh-when-saving',
       'Outline two economic factors which some households in Ireland may consider when deciding '
       'how much of their income to save.',
       'A factor a household weighs — any two',
       'Two factors, 3 marks each.',
       ref='2025 HL Section A Q2(b)', drop=SCAFFOLD)

P.menu('household savings is desirable', 'econ-2025-hl-sa-q2-c-agree',
       'economics-3-0', 'why-high-household-savings-help',
       'A high level of household savings is desirable for the Irish economy. Argue that you '
       'AGREE with this statement.',
       'A reason high savings help — any one',
       'One argument, 6 marks.',
       ref='2025 HL Section A Q2(c) — agree', claim=1, per=6,
       drop=SCAFFOLD, stop='Reduced consumer spending',
       notes='The part is answered either way and the scheme heads the two lists AGREE and '
             'DISAGREE, so each side is its own card.')

P.menu('household savings is desirable', 'econ-2025-hl-sa-q2-c-disagree',
       'economics-3-0', 'why-high-household-savings-harm',
       'A high level of household savings is desirable for the Irish economy. Argue that you '
       'DISAGREE with this statement.',
       'A reason high savings harm — any one',
       'One argument, 6 marks.',
       ref='2025 HL Section A Q2(c) — disagree', claim=1, per=6,
       drop=SCAFFOLD, after='Reduced consumer spending')

P.menu('why Irish consumers are switching to importing more', 'econ-2025-hl-sa-q3-a',
       'economics-4-2', 'why-import-patterns-shift',
       'Outline one economic reason why Irish consumers are switching to importing more used cars '
       'from Japan and fewer from the UK.',
       'A reason for the switch — any one',
       'One reason, 6 marks.',
       ref='2025 HL Section A Q3(a)', claim=1, per=6, drop=SCAFFOLD)

P.menu('alternative measure the EU could use', 'econ-2025-hl-sa-q3-b',
       'economics-4-2', 'alternatives-to-a-tariff',
       'The EU increased the tariffs charged on electric vehicles imported from China. Explain '
       'one alternative measure the EU could use, other than tariffs, to reduce those imports.',
       'An alternative to a tariff — any one',
       'One measure, 6 marks.',
       ref='2025 HL Section A Q3(b)', claim=1, per=6, drop=SCAFFOLD)

P.menu('Trade protectionism seems to be increasing globally', 'econ-2025-hl-sa-q3-c',
       'economics-4-2', 'why-protectionism-is-rising',
       'Trade protectionism seems to be increasing globally. Outline one reason why.',
       'A reason protectionism is rising — any one',
       'One reason, 6 marks.',
       ref='2025 HL Section A Q3(c)', claim=1, per=6, drop=SCAFFOLD)

P.menu('Comment on the trend in the CPI', 'econ-2025-hl-sa-q4-a-good',
       'economics-3-3', 'why-disinflation-helps-consumers',
       'Explain if the trend you have outlined in the CPI for chocolate is beneficial for '
       'chocolate consumers — argue that it IS.',
       'A reason disinflation helps — any one',
       'One explanation, 6 marks.',
       ref='2025 HL Section A Q4(a) — beneficial', claim=1, per=6,
       stem='Ireland’s year-on-year CPI for chocolate fell steadily from January to June 2024.',
       drop=SCAFFOLD + ('Beneficial for chocolate consumers',), stop='Not beneficial',
       notes='The part is answered either way and the scheme heads the two lists separately, so '
             'each side is its own card.')

P.menu('Comment on the trend in the CPI', 'econ-2025-hl-sa-q4-a-bad',
       'economics-3-3', 'why-disinflation-is-not-relief',
       'Explain if the trend you have outlined in the CPI for chocolate is beneficial for '
       'chocolate consumers — argue that it is NOT.',
       'A reason disinflation is not relief — any one',
       'One explanation, 6 marks.',
       ref='2025 HL Section A Q4(a) — not beneficial', claim=1, per=6,
       stem='Ireland’s year-on-year CPI for chocolate fell steadily from January to June 2024.',
       drop=SCAFFOLD, after='Prices are still increasing')

P.menu('Outline one measure both the Irish government', 'econ-2025-hl-sa-q4-b-gov',
       'economics-3-1', 'government-measures-on-the-cost-of-living',
       'Irish consumers continue to pay higher prices even as inflation falls. Outline one '
       'measure the Irish government has taken to help with the cost of living.',
       'A government measure — any one',
       'One measure, 6 marks.',
       ref='2025 HL Section A Q4(b) — government', claim=1, per=6,
       drop=SCAFFOLD, stop='One measure taken by consumers',
       notes='The part asks for a measure from the government and one from consumers, and the '
             'scheme heads the two lists separately, so each side is its own card.')

P.menu('Outline one measure both the Irish government', 'econ-2025-hl-sa-q4-b-cons',
       'economics-1-1', 'household-responses-to-higher-prices',
       'Irish consumers continue to pay higher prices even as inflation falls. Outline one '
       'measure consumers in Ireland have taken in response.',
       'A measure consumers have taken — any one',
       'One measure, 6 marks.',
       ref='2025 HL Section A Q4(b) — consumers', claim=1, per=6,
       drop=SCAFFOLD, after='Budgeting / Cost-cutting')

P.menu('cocoa prices tripled', 'econ-2025-hl-sa-q4-c',
       'economics-3-3', 'identifying-cost-push-inflation',
       'Chocolate producers buy cocoa in advance of making products. In Q1 2024 cocoa prices '
       'tripled. Justify classifying the price rise that followed as cost-push inflation.',
       'A justification — any one',
       'One justification, 6 marks.',
       ref='2025 HL Section A Q4(c)', claim=1, per=6,
       drop=SCAFFOLD + ('Cost-push inflation Justification',))

P.menu('difference between a positive economic statement and a normative', 'econ-2025-hl-sa-q5-a',
       'economics-0-0', 'positive-versus-normative-statements',
       'Explain the difference between a positive economic statement and a normative economic '
       'statement.',
       'One of the two terms — both of them',
       'Both terms, 3 marks each. The question names them, so this is not a choice.',
       ref='2025 HL Section A Q5(a)', drop=SCAFFOLD)

P.menu('recent initiative introduced by', 'econ-2025-hl-sa-q8-a',
       'economics-0-2', 'irish-environmental-sustainability-initiatives',
       'Outline one recent initiative introduced by the Irish government to improve the country’s '
       'environmental sustainability.',
       'A government initiative — any one',
       'One initiative, 6 marks. The scheme prints 6 against this part, covering both the '
       'explanation of the concept and the initiative.',
       ref='2025 HL Section A Q8(a)', claim=1, per=6,
       drop=SCAFFOLD + ('Environmental sustainability refers to',))

P.menu('shoppers struggle to tell the difference between goods', 'econ-2025-hl-sa-q8-b',
       'economics-2-2', 'greenwashing-as-market-failure',
       'Greenwashing is a practice where companies make false or exaggerated claims to appear '
       'more environmentally friendly than they are. Outline two ways greenwashing causes market '
       'failure.',
       'A way greenwashing causes market failure — any two',
       'Two ways, 3 marks each.',
       ref='2025 HL Section A Q8(b)', drop=SCAFFOLD)

P.menu('explain the shape of the curve labelled', 'econ-2025-hl-sa-q9-b',
       'economics-2-0', 'the-kinked-demand-curve',
       'With reference to the diagram, explain the shape of the curve labelled 2 — the kinked '
       'demand curve facing a firm in an oligopoly market.',
       'One side of the kink — both of these',
       'Both halves, 3 marks each: what rivals do when the firm raises price, and what they do '
       'when it cuts price.',
       ref='2025 HL Section A Q9(b)', claim=2, per=3, drop=SCAFFOLD)

P.menu('economic factor which led to a change in Ireland', 'econ-2025-hl-sa-q10-b',
       'economics-3-5', 'what-caused-the-irish-downturn',
       'Outline one economic factor which led to a change in Ireland’s economic output during the '
       'years 2008 to 2011.',
       'A factor behind the downturn — any one',
       'One factor, 6 marks.',
       ref='2025 HL Section A Q10(b)', claim=1, per=6, drop=SCAFFOLD)

# Q6(b) is not carded: its 6 marks cover a diagram to be completed AND the
# explanation, and the scheme does not split them. Four written steps at 1 mark
# each was my arithmetic, not the scheme's.

P.emit()
