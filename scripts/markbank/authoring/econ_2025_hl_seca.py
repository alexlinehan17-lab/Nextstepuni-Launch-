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
from econ_lib import as_option, block, card, load, point, tidy  # noqa: E402

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
       ref='2025 HL Section A Q9(b)', claim=2, per=3, drop=SCAFFOLD,
       figure='economics-2025-HL-paper-p11-art')

P.menu('economic factor which led to a change in Ireland', 'econ-2025-hl-sa-q10-b',
       'economics-3-5', 'what-caused-the-irish-downturn',
       'Outline one economic factor which led to a change in Ireland’s economic output during the '
       'years 2008 to 2011.',
       'A factor behind the downturn — any one',
       'One factor, 6 marks.',
       ref='2025 HL Section A Q10(b)', claim=1, per=6, drop=SCAFFOLD)

# ── Definitions with one printed answer, built from the scheme directly ─────
# These parts print a single response under a single tariff cell, so they are
# not menus; each is a point card, the same shape as 2024's Q6(b) halves. The
# slice ends at the page footer or the next part, so nothing foreign rides in.
BODY = tidy(load(2025, 'higher'))

P.cards.append(card(
    'econ-2025-hl-sa-q1-b', 2025, 'higher', 'economics-0-1', 'cost-benefit-analysis',
    '2025 HL Section A Q1(b)',
    'Outline what you understand by the economic term cost benefit analysis.',
    'fixed', 6,
    [point('r-1', as_option(block(BODY, 'Helps weigh up / evaluate whether the positive benefits',
                                  '4 | P a g e')), 6,
           'One explanation, 6 marks. The scheme prints one answer and one only.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2025-hl-sa-q6-a', 2025, 'higher', 'economics-1-3', 'what-a-price-floor-is',
    '2025 HL Section A Q6(a)',
    'Explain what you understand by the economic term price floor.',
    'fixed', 6,
    [point('r-1', as_option(block(BODY, 'A price floor is a legal minimum price',
                                  '(b) The diagram below shows a free labour market')), 6,
           'One explanation, 6 marks: what a price floor is, and what it is for.')],
    '', stem='The national minimum wage rate currently stands at €13.50 per hour. This is an '
             'example of a price floor.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2025-hl-sa-q7-b', 2025, 'higher', 'economics-2-2', 'phone-pouches-as-merit-goods',
    '2025 HL Section A Q7(b)',
    'Phone pouches in all secondary schools are considered to be merit goods. Explain your '
    'understanding of this statement.',
    'fixed', 6,
    [point('r-1', as_option(block(BODY, 'Phone pouches in secondary schools are considered a merit good',
                                  '17 | P a g e')), 6,
           'One explanation, 6 marks: why the good would be under-consumed, and the positive '
           'externalities it creates.')],
    '', stem='The government announced in Budget 2025 that it would spend €9m on phone pouches '
             '(for the storage of each student’s mobile phone during the school day) for all '
             'secondary school students in the country.',
    section='A', tariff_kind='fixed'))

# Q6(b) is not carded: its 6 marks cover a diagram to be completed AND the
# explanation, and the scheme does not split them. Four written steps at 1 mark
# each was my arithmetic, not the scheme's.

# ── Worked calculations the scheme prints in full ──────────────────────────
# Excluded until now as "the response is the worked calculation". That is a
# description of the answer, not a blocker: the scheme sets out the formula, the
# substitution and the result, so every step a student is credited for is on the
# page and traces. Where the figures come off a chart the crop rides with the
# card, because the arithmetic is unanswerable without it.

P.cards.append(card(
    'econ-2025-hl-seca-q2-a', 2025, 'higher', 'economics-3-0',
    'household-percentage-savings-rate', '2025 HL Section A Q2(a)',
    'From the data in the above table, calculate the household percentage savings rate for '
    'Quarter 1, 2024. Show all your workings.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Workings: Household savings',
                                  'Deduct 1 mark if % omitted')), 6,
           'Savings over DISPOSABLE INCOME, not over consumption. The table prints all three '
           'figures, so the mark is for choosing the right denominator.')],
    'The table gives income, consumption and savings, and only two of the three belong in this '
    'ratio.',
    tariff_kind='fixed', section='A',
    figure_key='economics-2025-HL-paper-p04-i0'))

# ── Diagram parts whose explanation the scheme prints ──────────────────────
# Excluded as diagram completions. The drawing is only half the ask — the paper
# also says "Explain" — and the scheme prints that explanation as ordinary
# prose. The paper's own diagram rides as the card's figure, so the student has
# the axes and curves the question is about.

P.cards.append(card(
    'econ-2025-hl-seca-q6-b', 2025, 'higher', 'economics-2-1',
    'a-minimum-wage-above-the-equilibrium', '2025 HL Section A Q6(b)',
    'The diagram below shows a free labour market. Complete the diagram below to show how a '
    'change to Ireland\u2019s current national minimum wage rate, at a rate higher than WE in '
    'the diagram below, will affect the market for labour. Clearly label any changes you make. '
    'Explain your answer.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Wage rate: the national minimum wage rate (NMW) lies '
                                        'above', '16 | P a g e')), 6,
           'Four steps, and the order is the argument: the minimum sits ABOVE equilibrium, so '
           'supply of labour rises and demand for it falls, and the gap between them is the '
           'unemployment. The \u27e86\u27e9 covers the drawing and the explanation together.')],
    'The trade-off is the answer: some workers earn more and others lose hours or jobs. A '
    'response that only says "wages go up" has drawn the line without reading the diagram.',
    tariff_kind='fixed', section='A',
    figure_key='economics-2025-HL-paper-p08-art'))

# ── A tick table, answered by the scheme's own completed table ─────────────
# See econ_tick_crop.py for why: the ✔ is drawn, not set in the text layer, so
# extraction keeps it and loses the column it sits in. Here the flat run reads
# "All citizens in Ireland deserve free healthcare to ✓ 1. ensure equal access"
# — the tick lands mid-sentence and names no column at all. The scheme states
# this answer graphically, so it is taken graphically: the completed table is
# bound as a SOLUTION crop, hidden until reveal, the way the Maths deck carries
# a printed model solution.
P.cards.append(card(
    'econ-2025-hl-seca-q5-b', 2025, 'higher', 'economics-0-1',
    'positive-and-normative-statements-sorted', '2025 HL Section A Q5(b)',
    'Determine whether each of the economic statements below is a positive statement or a '
    'normative statement. Indicate your choice below by ticking (\u2713) the relevant box. '
    '1. All citizens in Ireland deserve free healthcare to ensure equal access to medical '
    'services. 2. If the Irish government were to raise the corporation tax rate by 3%, it '
    'would reduce foreign direct investment in the country by at least 25%.',
    '2 @ 3', 6,
    [point('r-1', as_option(block(BODY, 'Economic Statement Statement Statement All citizens',
                                  '15 | P a g e')), 6,
           'Read the completed table below rather than the line above it \u2014 in flat text '
           'the ticks land mid-sentence and name no column. Statement 1 is NORMATIVE: '
           '"deserve" is a value judgement and nothing could test it. Statement 2 is POSITIVE '
           'despite being a prediction and quite possibly wrong: it is falsifiable, and '
           'testability rather than truth is what makes a statement positive. Three marks each.')],
    'The trap is assuming a positive statement must be TRUE. Statement 2 forecasts a precise 25% '
    'fall that may never happen; it is positive because evidence could settle it.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2025-HL-scheme-p16-q5b-ticks'))


# ── Backfill: asks the scheme answers in full ──────────────────────────────

P.cards.append(card(
    'econ-2025-hl-seca-q10-a', 2025, 'higher', 'economics-3-5',
    'reading-boom-and-recession-off-the-cycle', '2025 HL Section A Q10(a)',
    'Identify from the diagram above which option (A or B) represents an economic boom and which '
    'represents an economic recession. Indicate your choice below and justify your choice in '
    'each case.',
    '2 @ 3', 6,
    [point('r-1', as_option(block(BODY, 'Economic boom A Economic recession B', '(b)')), 6,
           'A is the boom and B the recession, and the justification is the SHAPE of the curve '
           'at each point: output rising steeply to 2008, then falling. Naming the letters '
           'without saying what the curve is doing there answers half of it.')],
    'The cycle drawing runs 2000 to 2020, so the two letters sit either side of the 2008 turning '
    'point. Ireland\u2019s own history is the giveaway.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2025-HL-paper-p12-art',
    label_key=[{'letter': 'A', 'meaning': 'a point on the rising stretch of the cycle curve, '
                                          'before 2008', 'askedInThisQuestion': True},
               {'letter': 'B', 'meaning': 'a point on the falling stretch of the cycle curve, '
                                          'after 2008', 'askedInThisQuestion': True}]))

# ── Backfill ───────────────────────────────────────────────────────────────
# One row, not two. The question asks for two things and the scheme prints one
# ⟨6⟩ over both, so splitting it 3 and 3 would be arithmetic on a printed total
# rather than a printed split — the same guess the tariff rule forbids.
P.cards.append(card(
    'econ-2025-hl-seca-q7-a', 2025, 'higher', 'economics-1-1',
    'spotting-a-necessity-and-a-luxury-from-yed', '2025 HL Section A Q7(a)',
    'Identify one necessity and one luxury good from the above table, using the Income '
    'Elasticity of Demand (YED) data provided. Justify both of your answers.',
    '6', 6,
    [point('r-1', as_option(block(BODY, 'Necessity product \u2013 Electricity or Noodles',
                                  '8 ')), 6,
           'The YED VALUE decides it, not the product. Between 0 and 1 means income inelastic, so '
           'demand barely moves with income \u2014 a necessity. Above 1 means income elastic, so '
           'demand moves more than income does \u2014 a luxury. Electricity at +0.1 and premium '
           'clothing at +4.1 sit either side of that line.')],
    'Noodles carry a NEGATIVE YED of \u22120.5, which makes them inferior rather than merely a '
    'necessity \u2014 demand falls as income rises. The scheme accepts them alongside '
    'electricity, but the two are inelastic for different reasons.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2025-HL-paper-p09-i0'))


P.emit()
