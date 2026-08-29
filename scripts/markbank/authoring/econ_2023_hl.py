#!/usr/bin/env python3
"""Economics 2023 Higher Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for. This
paper writes its descending tariffs in words ("1st @ 5", "2nd @ 4"), which is
the Ordinary style — the two are not a level split.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, heads, load, make_load, point, tidy  # noqa: E402

P = Paper(2023, 'higher')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Deduct 1m', 'The Research Process')

P.menu('factors which are likely to have influenced this trend in the Irish population',
       'econ-2023-hl-q11-a-ii', 'economics-3-5', 'drivers-of-population-growth',
       'Explain two factors which are likely to have influenced this trend in the Irish '
       'population.',
       'A factor behind the population trend — any two',
       'Two factors, 5 marks each.',
       drop=SCAFFOLD)

P.menu('factors that influence the geographical mobility of labour', 'econ-2023-hl-q11-b-ii',
       'economics-2-1', 'geographical-mobility-of-labour',
       'Explain two factors that influence the geographical mobility of labour.',
       'A factor affecting geographical mobility — any two',
       'Two factors, the first paid 5 and the second 4.',
       drop=SCAFFOLD)

P.menu('ways the government can possibly increase geographical mobility', 'econ-2023-hl-q11-b-iii',
       'economics-2-1', 'increasing-mobility-of-labour',
       'Explain two ways the government can possibly increase geographical mobility of labour.',
       'A way to increase mobility of labour — any two',
       'Two ways, the first paid 5 and the second 4.',
       drop=SCAFFOLD)

P.menu('Despite Ireland’s high HDI ranking', 'econ-2023-hl-q11-c-ii',
       'economics-3-1', 'policies-to-address-inequality',
       'Despite Ireland’s high HDI ranking, inequalities still exist. Outline two economic '
       'policies the Irish Government could consider to address inequality. Justify your answers.',
       'A policy to address inequality — any two',
       'Two policies, the first paid 5 and the second 4. The marks are for the justification as '
       'much as the policy.',
       drop=SCAFFOLD + ('Outline two economic pol',))

P.menu('above were introduced, outline two possible economic disadvantages', 'econ-2023-hl-q11-c-iii',
       'economics-3-1', 'disadvantages-of-inequality-policies',
       'If the policies you suggested above were introduced, outline two possible economic '
       'disadvantages of their implementation.',
       'A disadvantage of those policies — any two',
       'Two disadvantages, the first paid 5 and the second 4. Each answers one of the policies '
       'from part (ii), so the two parts are marked as a pair.',
       drop=SCAFFOLD + ('college and universities',))

P.menu('Identify three characteristics of a perfectly competitive market', 'econ-2023-hl-q12-a-i',
       'economics-2-0', 'perfect-competition-characteristics',
       'Identify three characteristics of a perfectly competitive market.',
       'A characteristic of perfect competition — any three',
       'Three characteristics, 4 marks each.',
       drop=SCAFFOLD)

P.menu('Explain the terms injections and leakages', 'econ-2023-hl-q13-a-ii',
       'economics-3-0', 'injections-and-leakages',
       'Explain the terms injections and leakages, and refer to two examples of each.',
       'The two terms — both of them',
       'Both terms, and the scheme prints two examples of each. The question names them, so this '
       'is not a choice.',
       drop=SCAFFOLD)

P.menu('Some citizens engage in activities in the hidden economy', 'econ-2023-hl-q13-a-iii',
       'economics-3-1', 'effects-of-the-hidden-economy-hl',
       'Some citizens engage in activities in the hidden economy in Ireland. Outline two effects '
       'on the Irish economy.',
       'An effect of the hidden economy — any two',
       'Two effects, 4 marks each.',
       drop=SCAFFOLD)

P.menu('risks associated with over-reliance on MNCs', 'econ-2023-hl-q13-b-i',
       'economics-4-1', 'risks-of-over-reliance-on-mncs',
       'Outline two risks associated with over-reliance on MNCs for Ireland’s tax revenue.',
       'A risk of over-reliance on MNCs — any two',
       'Two risks, the first paid 7 and the second 5.',
       drop=SCAFFOLD + ('which is hugely volatile',))

P.menu('factors that are currently impacting on Ireland’s international competitiveness',
       'econ-2023-hl-q13-b-ii', 'economics-4-2', 'factors-affecting-competitiveness',
       'Discuss two factors that are currently impacting on Ireland’s international '
       'competitiveness.',
       'A factor affecting competitiveness — any two',
       'Two factors, 4 marks each.',
       drop=SCAFFOLD + ('insurance), these tend t',))

P.menu('Describe two types of unemployment', 'econ-2023-hl-q14-a-iii',
       'economics-3-2', 'types-of-unemployment',
       'Describe two types of unemployment, giving examples to support your answer.',
       'A type of unemployment — any two',
       'Two types, 7 marks each. Structural unemployment is given in the question, so the scheme '
       'lists the others.',
       drop=SCAFFOLD + ('of the year. E.g. a pers',))

P.menu('Maintaining full employment is an objective of the government', 'econ-2023-hl-q14-b-ii',
       'economics-3-1', 'government-economic-objectives',
       'Maintaining full employment is an objective of the government. Outline two other current '
       'economic objectives of the Irish government.',
       'An economic objective — any two',
       'Two objectives, 4 marks each. Full employment is excluded by the question.',
       drop=SCAFFOLD)

P.menu('Pandemic Unemployment Payment (PUP)', 'econ-2023-hl-q14-b-iii',
       'economics-3-0', 'the-multiplier-and-the-pup',
       'The Irish government spent €8.8bn on the Pandemic Unemployment Payment in 2021. Use the '
       'multiplier to explain the effect of this expenditure on the Irish economy.',
       'A step in the multiplier effect — any three',
       'Three points, 4 marks each. The scheme walks the money round the circular flow, so the '
       'points are a sequence rather than alternatives.',
       drop=SCAFFOLD + ('citizens received money',))

P.menu('countries are now favouring a return to trade protection', 'econ-2023-hl-q15-b-ii',
       'economics-4-2', 'reasons-for-trade-protection',
       'Some countries are now favouring a return to trade protection measures. Discuss two '
       'economic reasons for this.',
       'A reason for trade protection — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD + ('produced goods. This wil',))

P.menu('possible disadvantages of trade protection', 'econ-2023-hl-q15-b-iii',
       'economics-4-2', 'disadvantages-of-trade-protection',
       'Outline two possible disadvantages of trade protection.',
       'A disadvantage of trade protection — any two',
       'Two disadvantages, 4 marks each.',
       drop=SCAFFOLD + ('market because of limita',))

P.menu('Circular Economy and Miscellaneous Provisions Act 2022', 'econ-2023-hl-q16-b-ii',
       'economics-0-2', 'moving-to-a-circular-economy',
       'Outline two changes required if Ireland is to move to a circular economy.',
       'A change the circular economy requires — any two',
       'Two changes, 4 marks each.',
       drop=SCAFFOLD + ('acknowledge/unaware of t',))

P.menu('households in Ireland are responsible for 117 kg of food waste', 'econ-2023-hl-q16-b-iii',
       'economics-0-2', 'reducing-household-food-waste',
       'Outline two measures that could be taken to reduce household food waste in Ireland.',
       'A measure to reduce food waste — any two',
       'Two measures, the first paid 6 and the second 4.',
       drop=SCAFFOLD + ('widespread public awaren',))

P.menu('market for Irish milk can no longer be considered', 'econ-2023-hl-q12-a-ii',
       'economics-2-0', 'irish-milk-not-perfectly-competitive',
       'Identify one reason why the market for Irish milk can no longer be considered perfectly '
       'competitive.',
       'A reason the milk market is not perfectly competitive — any one',
       'One reason, 4 marks.',
       claim=1, per=4, drop=SCAFFOLD)


# ── Section B, second pass ──────────────────────────────────────────────────
SIDES5 = ('The part asks for one of each and the scheme heads the two lists separately, so each '
          'side is its own card.')

P.menu('increase in population can have a positive or negative effect',
       'econ-2023-hl-q11-a-iii-neg', 'economics-3-1', 'population-growth-and-state-finances-cost',
       'An increase in population can have a positive or negative effect on government finances. '
       'Discuss one NEGATIVE effect.',
       'A cost to the state — any one', 'One effect, 5 marks.',
       ref='2023 HL Q11(a)(iii) — negative', claim=1, per=5,
       drop=SCAFFOLD, stop='Increased demand for goods and services', notes=SIDES5)

P.menu('increase in population can have a positive or negative effect',
       'econ-2023-hl-q11-a-iii-pos', 'economics-3-1', 'population-growth-and-state-finances-gain',
       'An increase in population can have a positive or negative effect on government finances. '
       'Discuss one POSITIVE effect.',
       'A gain to the state — any one', 'One effect, 5 marks.',
       ref='2023 HL Q11(a)(iii) — positive', claim=1, per=5,
       drop=SCAFFOLD, after='Increased demand for goods and services')

P.menu('Would you consider this market to be competitive', 'econ-2023-hl-q12-b-ii',
       'economics-2-0', 'reading-the-dairy-market-hhi',
       'The HHI for the Irish dairy market was 3,172. Would you consider this market to be '
       'competitive, moderately concentrated, or highly concentrated? Explain your answer.',
       'A reason it is highly concentrated — either one',
       'One reason, 5 marks. Above 2,500 the market counts as highly concentrated.',
       ref='2023 HL Q12(b)(ii)', claim=1, per=5,
       drop=SCAFFOLD + ('concentrated? Explain your answer',))

P.menu('economic advantage and one possible economic disadvantage of',
       'econ-2023-hl-q12-b-iii-adv', 'economics-2-0', 'advantages-of-perfect-competition',
       'Outline one possible economic advantage and one possible economic disadvantage of a '
       'perfectly competitive market — the ADVANTAGE.',
       'An advantage of perfect competition — any one', 'One advantage, 6 marks.',
       ref='2023 HL Q12(b)(iii) — advantage', claim=1, per=6,
       drop=SCAFFOLD + ('a perfectly competitive market. Advantages',),
       stop='Little potential to expand', notes=SIDES5)

P.menu('economic advantage and one possible economic disadvantage of',
       'econ-2023-hl-q12-b-iii-dis', 'economics-2-0', 'disadvantages-of-perfect-competition',
       'Outline one possible economic DISADVANTAGE of a perfectly competitive market.',
       'A disadvantage of perfect competition — any one', 'One disadvantage, 4 marks.',
       ref='2023 HL Q12(b)(iii) — disadvantage', claim=1, per=4,
       drop=SCAFFOLD, after='Little potential to expand')

P.menu('why this measure is considered more accurate', 'econ-2023-hl-q14-a-ii',
       'economics-3-2', 'why-the-labour-force-survey-is-better',
       'Give two reasons why the Labour Force Survey is considered a more accurate measure of '
       'unemployment than data collected from the Live Register.',
       'A reason the survey is more accurate — any one',
       'The SEC voided this part: it awarded 4 marks to every candidate who attempted it, because '
       'the question said Quarterly National Household Survey when it should have said Labour '
       'Force Survey. The economics below is still what the scheme accepts.',
       ref='2023 HL Q14(a)(ii)', claim=1, per=4,
       drop=SCAFFOLD + ('are included as being fully unemployed',))

P.menu('impacted on Irish consumer behaviou', 'econ-2023-hl-q15-a-i',
       'economics-3-3', 'how-rising-prices-change-behaviour',
       'Electricity prices rose through 2021 and 2022. Explain how this will have impacted on '
       'Irish consumer behaviour.',
       'An impact on consumer behaviour — any one', 'One impact, 6 marks.',
       ref='2023 HL Q15(a)(i)', claim=1, per=6,
       drop=SCAFFOLD + ('Impact on consumer behavior',))

# ── Q16: the national herd, the Deposit Return Scheme, school transport ────
# The scheme heads the two sides of Q16(c)(i) "For:" and runs them together, so
# each side is its own card, as the deck does elsewhere for a question that asks
# for one of each.
P.menu('simply reduce the national herd', 'econ-2023-hl-q16-c-i-for',
       'economics-0-2', 'the-case-for-reducing-the-national-herd',
       'Outline one argument FOR the proposal that the agricultural industry must simply '
       'reduce the national herd to play its part in reducing emissions.',
       'An argument for — any one', 'One argument, 7 marks, with 5 for the other side.',
       ref='2023 HL Q16(c)(i) — for', claim=1, per=7,
       drop=SCAFFOLD + ('Outline one argument for and one argument against',),
       stop='Protection of rural economy')

P.menu('simply reduce the national herd', 'econ-2023-hl-q16-c-i-against',
       'economics-0-2', 'the-case-against-reducing-the-national-herd',
       'Outline one argument AGAINST the proposal that the agricultural industry must simply '
       'reduce the national herd to play its part in reducing emissions.',
       'An argument against — any one', 'One argument, 5 marks, with 7 for the other side.',
       ref='2023 HL Q16(c)(i) — against', claim=1, per=5,
       drop=SCAFFOLD + ('Outline one argument for and one argument against',
                        'The beef industry in Ireland is in decline',
                        'Emission credits costs', 'Agricultural emissions are 32%',
                        'Environmental Sustainability. The Climate Action Plan'))

P.menu('Deposit Return Scheme is to be introduced', 'econ-2023-hl-q16-c-ii',
       'economics-0-2', 'effects-of-the-deposit-return-scheme',
       'Outline two likely effects the introduction of the Deposit Return Scheme will have on '
       'the Irish consumer.',
       'An effect on the consumer — any two', 'Two effects, 7 then 5.',
       ref='2023 HL Q16(c)(ii)', claim=2, per=7, steps=[7, 5],
       drop=SCAFFOLD + ('Outline two likely effects the introduction',))

# Q16(a)(ii) is not carded: its marks are for a fully labelled diagram and the
# scheme's tariff cells read 4/4/7/8 across the part, which does not tell me how
# much of that is for the written explanation as against the drawing. Guessing a
# split would put a made-up tariff on a real question.

P.menu('economic disadvantage of this government intervention', 'econ-2023-hl-q15-c-ii',
       'economics-1-3', 'downside-of-the-electricity-credit',
       'Outline one possible economic disadvantage of the government electricity credit.',
       'A disadvantage — any one', 'One disadvantage, 7 marks.',
       ref='2023 HL Q15(c)(ii)', claim=1, per=7, drop=SCAFFOLD)


# ── Third pass: the parts the extractor hands back with fewer than two ──────
# options — definitions with one printed answer, yes/no parts with one printed
# justification, and one two-column table. Built from the scheme directly.
#
# Left alone on purpose, besides what the header and econ_excluded already
# record: Q11(a)(i), Q12(b)(i), Q13(b)(i)-(iii) and Q15(a)(iii) are worked
# calculations; Q14(a)(i) and Q15(b)(ii) are answered by reading the chart
# printed beside them; Q16(a)(i) has no tariff the scheme attributes to it
# (the margin prints 4/4/7/8 between (ii)'s marker and (iii)'s, nothing beside
# (i)'s two definitions); Q13(a)(i) is a drawing whose 13 credited labels at 1
# mark each live in the scheme's model circular-flow diagram, so it needs that
# figure cropped before it can be carded.
BODY = tidy(load(2023, 'higher'))

P.cards.append(card(
    'econ-2023-hl-q11-b-i', 2023, 'higher', 'economics-2-1',
    'factor-of-production-labour', '2023 HL Q11(b)(i)',
    'Explain the factor of production labour.',
    '1 @ 6', 6,
    [point('r-1', as_option(block(BODY, 'Labour refers to all human effort',
                                  '(ii) Explain two factors')),
           6, 'The definition, 6 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-q11-c-i', 2023, 'higher', 'economics-4-0',
    'life-expectancy-and-the-hdi', '2023 HL Q11(c)(i)',
    'In your opinion, if the average life expectancy in Ireland were to decrease, would it '
    'positively or negatively affect Ireland’s HDI score? Explain the reason for your answer.',
    '1+4', 5,
    [point('r-1', 'Negatively.', 1, 'The scheme pays 1 mark for the choice itself.'),
     point('r-2', as_option(block(BODY, 'If average life expectancy were to decrease',
                                  '(ii) Despite Ireland’s high HDI ranking')),
           4, 'The explanation, 4 marks.')],
    '', tariff_kind='fixed'))

# Q12(c): the windfall-tax debate. The scheme sets it as a two-column
# For/Against table and the primary extraction interleaves the columns
# mid-sentence, so no argument separates from it. append-scheme-blocks.py
# recovered each column as one contiguous run (the markbank:column-runs block,
# which the provenance gate searches too), so the arguments are sliced from
# there — occ=1 naming the column-runs copy of the For run.
RAW = tidy(make_load('economics')(2023, 'higher'))
_FOR = block(RAW, 'For Reduce consumer exploitation.', 'Against Deter future investment', occ=1)
_AGAINST = block(RAW, 'Against Deter future investment in energy development.', '18 1st @ 8')
WINDFALL = ([as_option(h) for h in heads(_FOR, (
                'Reduce consumer exploitation.',
                'Help people during current crisis',
                'Support Irish businesses.',
                'Achieve a more equitable tax system.'))] +
            [as_option(h) for h in heads(_AGAINST, (
                'Deter future investment in energy development.',
                'Inadequate infrastructure.',
                'Erratic future supply of energy.'))])

P.cards.append(card(
    'econ-2023-hl-q12-c', 2023, 'higher', 'economics-1-3', 'windfall-tax-for-and-against',
    '2023 HL Q12(c)',
    'Budget 2023 proposed introducing a temporary 33% windfall tax on energy companies’ '
    'profits. Discuss the arguments for and the arguments against this proposal.',
    '1 @ 8+1 @ 5+1 @ 5', 18,
    [anyN('r-1', 'An argument for or against the windfall tax — any three, covering both sides',
          None, 3, 8, WINDFALL,
          'The first four are the scheme’s arguments FOR, the last three its arguments '
          'AGAINST. The first argument earns 8 and the next two 5 each, and a discussion of '
          'both sides needs at least one of each.',
          steps=[8, 5, 5])],
    'Not split into a for-card and an against-card the way Q16(c)(i) is: the scheme prices '
    'the three arguments across the sides — 1st @ 8, 2 @ 5 — and states no per-side split.',
    tariff_kind='fixed'))

_FULL = block(BODY, 'Full Employment refers to a situation', '(ii) Maintaining full employment')
_CORE, _TAIL = _FULL.split(' 4 ')
P.cards.append(card(
    'econ-2023-hl-q14-b-i', 2023, 'higher', 'economics-3-2',
    'the-term-full-employment', '2023 HL Q14(b)(i)',
    'Explain the economic term full employment.',
    '4+2', 6,
    [point('r-1', tidy(_CORE), 4, 'The body of the definition, 4 marks.'),
     point('r-2', _TAIL.split('.')[0], 2,
           'The closing condition, which the scheme prices separately at 2.')],
    'The scheme prints its 4/2 split as inline ticks in the sentence — "... are employed 4 '
    'at existing wage rates.2" — so the definition is carded as its two priced halves.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-q14-c-i', 2023, 'higher', 'economics-4-2',
    'the-term-trade-protection', '2023 HL Q14(c)(i)',
    'Explain the economic term trade protection.',
    '1 @ 7', 7,
    [point('r-1', as_option(block(BODY, 'Trade Protection refers to government policies',
                                  '(ii) Some countries are now favouring')),
           7, 'The definition, 7 marks.')],
    '', tariff_kind='fixed'))

# Q15(a)(ii): the scheme prices each definition at 4 and marks 2-mark ticks
# INSIDE each sentence — "cost of production2 are passed" — so a whole-sentence
# slice cannot dodge the digit. Each definition is its two contiguous halves,
# joined for display with an em-dash where the tick falls; the gate checks the
# half after the dash, and the half before it is a verbatim slice too.
_CP = block(BODY, 'Cost-push inflation occurs when increases', '• Demand-pull inflation occurs')
_CP1, _CP2 = _CP.split('2 ')
_DP = block(BODY, 'Demand-pull inflation occurs when', '⟨8⟩')
_DP1, _DP2 = _DP.split('2 ')
P.cards.append(card(
    'econ-2023-hl-q15-a-ii', 2023, 'higher', 'economics-3-3',
    'demand-pull-and-cost-push-inflation', '2023 HL Q15(a)(ii)',
    'Distinguish between demand-pull inflation and cost-push inflation.',
    '4+4', 8,
    [point('r-1', f"{tidy(_CP1)} — {tidy(_CP2.split('2.')[0])}", 4, 'Cost-push, 4 marks.'),
     point('r-2', f"{tidy(_DP1)} — {tidy(_DP2.split('2.')[0])}", 4, 'Demand-pull, 4 marks.')],
    'The em-dash in each definition marks where the scheme prints an inline 2-mark tick.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-q15-b-i', 2023, 'higher', 'economics-3-3',
    'the-term-monetary-policy', '2023 HL Q15(b)(i)',
    'One role of the European Central Bank (ECB) is to formulate monetary policy for the '
    'Eurozone. Explain the term monetary policy.',
    '1 @ 8', 8,
    [point('r-1', as_option(block(BODY, 'Monetary policy refers to any action',
                                  '(ii) Does the trend on the graph')),
           8, 'The definition, 8 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-q15-c-i', 2023, 'higher', 'economics-1-3',
    'why-the-electricity-credit', '2023 HL Q15(c)(i)',
    'In budget 2023 the Irish government introduced a €600 electricity credit for all '
    'households. Explain the main economic reason for the above government intervention.',
    '1 @ 7', 7,
    [anyN('r-1', 'A main economic reason — any one', 7, 1, 7,
          bullets(block(BODY, 'Help Irish citizens with the cost of living crisis',
                        '(ii) Outline one possible economic disadvantage')),
          'One reason, 7 marks.')],
    ''))

P.cards.append(card(
    'econ-2023-hl-q15-c-iii', 2023, 'higher', 'economics-1-3',
    'does-the-credit-reduce-electricity-use', '2023 HL Q15(c)(iii)',
    'In your opinion does the €600 electricity credit encourage electricity users to reduce '
    'their use of electricity? Explain your answer.',
    '1 @ 6', 6,
    [point('r-1', as_option(block(BODY, 'As consumers can continue to purchase',
                                  'Question 16')),
           6, 'The scheme answers NO — the credit shields consumers from the price rise, so '
              'usage holds. One explanation, 6 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-q16-a-iii', 2023, 'higher', 'economics-2-2',
    'school-transport-government-failure', '2023 HL Q16(a)(iii)',
    'The rapid introduction of this scheme created an additional demand of 6,000 bus tickets '
    'in late September 2022 after schools had opened. Does this represent a government '
    'failure? Explain your answer.',
    '1 @ 5', 5,
    [point('r-1', as_option(block(BODY, 'This government intervention into the market',
                                  '(b) In 2006, multinational oil trading')),
           5, 'The scheme answers YES. One explanation, 5 marks.')],
    '', tariff_kind='fixed',
    stem='The Irish Government provided free school transport for the 2022/2023 school year.'))

# Q15(b)(iii): should the government worry about a rising euro. econ_excluded
# records this part as "the yes and no cases are welded onto the cue line and
# neither separates" — true of the EXTRACTOR's output, not of the scheme, which
# prints two Yes justifications, an OR, and two No justifications in sequence.
# Sliced apart here the way 2021 OL Q11(c)(ii) and 2023 OL Q14(c)(i) were when
# their "welded" verdicts fell to the same knife; the econ_excluded line is now
# stale. The tariff is the ⟨8⟩ the scheme prints beside the justifications: on
# the page the ⟨6⟩ above it sits at y=324, still inside (ii)'s span (which ends
# at (iii)'s marker, y=327), and 8 + 6 + 8 is the 22 the scheme prints against
# part (b). Either side of the argument earns the 8.
P.cards.append(card(
    'econ-2023-hl-q15-b-iii-euro', 2023, 'higher', 'economics-4-2',
    'effects-of-euro-appreciation', '2023 HL Q15(b)(iii)',
    'Should the Irish government be concerned if the Euro to Dollar exchange rate is '
    'appreciating? Justify your answer.',
    '1 @ 8', 8,
    [anyN('r-1', 'A justification, on either side — any one', 8, 1, 8,
          [as_option(block(BODY, 'Price of imports will decrease',
                           'Price of exports will increase')),
           as_option(block(BODY, 'Price of exports will increase', 'OR No Increased')),
           as_option(block(BODY, 'Increased purchasing power / improved standard',
                           'Reduced inflationary pressures')),
           as_option(block(BODY, 'Reduced inflationary pressures', '31 | P a g e'))],
          'One justification, 8 marks. The scheme credits either box: the first two '
          'justify YES (dearer exports, cheaper imports leaking income abroad), the '
          'last two justify NO (purchasing power, cooler inflation).')],
    'The id carries a suffix because econ-2023-hl-q15-b-iii is the trade-protection '
    'card econ_refs re-cites to Q14(c)(iii).'))

P.cards.append(card(
    'econ-2023-hl-q16-b-i', 2023, 'higher', 'economics-2-2',
    'toxic-waste-and-market-failure', '2023 HL Q16(b)(i)',
    'Does this represent a market failure? Justify your answer.',
    '1 @ 5', 5,
    [point('r-1', as_option(block(BODY, 'Market failure occurs when the price mechanism',
                                  '(ii) The Circular Economy')),
           5, 'The scheme answers YES. The justification, 5 marks.')],
    '', tariff_kind='fixed',
    stem='In 2006 the multinational oil trader Trafigura rejected a US$620,000 offer to '
         'dispose of its toxic waste safely in The Netherlands and instead paid US$17,000 to '
         'have it dumped illegally in Côte d’Ivoire, leaving more than 100,000 people in '
         'need of medical assistance.'))

# ── The parts whose question IS a chart ────────────────────────────────────
# Excluded until now as "every response reads the chart printed with it". That
# was true of the response and was never a reason to leave the part out: the
# crop is catalogued, carries verified alt text and an md5 the build re-checks,
# and the scheme's responses are ordinary prose that quotes figures off it.
# With the figure bound the student has exactly what the candidate in the hall
# had.

P.cards.append(card(
    'econ-2023-hl-q14-a-i', 2023, 'higher', 'economics-3-2',
    'trend-in-the-monthly-unemployment-rate', '2023 HL Q14(a)(i)',
    'From the graph above analyse one trend in Ireland\u2019s monthly unemployment rate from '
    'March 2021 to September 2022, using figures from the above graph.',
    '1 @ 8', 8,
    [anyN('r-1', 'One trend, quoted off the graph \u2014 any one', 8, 1, 8,
          [as_option(block(BODY, 'Between March 2021 and September 2022, the unemployment rate fell',
                           'Between March 2021 and May 2022')),
           as_option(block(BODY, 'Between March 2021 and May 2022 the unemployment rate fell',
                           'Between May 2022 and September 2022')),
           as_option(block(BODY, 'Between May 2022 and September 2022 the unemployment rate rose',
                           'Another method of measuring unemployment'))],
          'The question asks for ONE trend and the scheme prints three, so any one earns the 8. '
          'The tariff is written (4+4): half for naming the direction, half for the figures that '
          'evidence it \u2014 a trend named without numbers is half an answer. Note the third '
          'option runs the other way; the graph does not fall throughout.')],
    'The scheme is explicit that a rise counts as readily as a fall. A student who spots the '
    'uptick from May 2022 has analysed a trend just as well as one who takes the whole period.',
    figure_key='economics-2023-HL-paper-p25-i0'))


# ── Worked calculations the scheme prints in full ──────────────────────────
# The scheme sets a fraction as a stacked 2-D layout, so extraction flattens it:
# the numerator and the answer come out on one line and the denominator after
# them. Nothing is missing and nothing is added — the note on each card says how
# to read the order, which is the honest fix for a layout the text layer cannot
# preserve.

P.cards.append(card(
    'econ-2023-hl-q13-b-iii', 2023, 'higher', 'economics-3-0',
    'the-injection-needed-to-reach-full-employment', '2023 HL Q13(b)(iii)',
    'How much will the government have to inject into this economy if it wants the economy to '
    'operate at its full employment level? Show your workings.',
    '8', 8,
    [point('r-1', as_option(block(BODY, '\u20ac750m - \u20ac500m', '22 | P a g e')), 8,
           'The 2s between the steps are the marks: four steps at 2 each make the \u27e88\u27e9. '
           'Find the deflationary gap first (\u20ac750m \u2212 \u20ac500m), then divide by the '
           'multiplier \u2014 the injection is SMALLER than the gap, because the multiplier does '
           'the rest of the work.')],
    'The gap is €250m but the injection is €125m. Answering €250m is answering a different '
    'question: it ignores that the injection multiplies through the economy.',
    tariff_kind='fixed',
    figure_key='economics-2023-HL-paper-p22-i0'))

# ── Two-cell part: a labelled diagram and its explanation ──────────────────
P.cards.append(card(
    'econ-2023-hl-q12-a-iii', 2023, 'higher', 'economics-2-0',
    'long-run-equilibrium-in-perfect-competition', '2023 HL Q12(a)(iii)',
    'Explain, with the use of a fully labelled diagram (including the axes), the long run '
    'equilibrium of a firm in perfect competition.',
    '9 + 8', 17,
    [point('r-1', as_option(block(BODY, 'Price MC AC E P/C D = AR = MR', 'Explanation:')), 9,
           'Nine labels, one mark each, and the scheme says so. Note D = AR = MR is a SINGLE '
           'horizontal line here: a price-taking firm sells every unit at the market price, which '
           'is what separates this diagram from every other market structure.'),
     point('r-2', as_option(block(BODY, '\u2022 Equilibrium is at point E (where MC = MR).',
                                  '18 | P a g e')), 8,
           'The long-run outcome is NORMAL profit, because AR = AC \u2014 free entry has competed '
           'any surplus away. And the firm sits at the minimum of its ATC curve, so it is '
           'productively efficient, which monopoly and monopolistic competition are not.')],
    'This is the benchmark diagram the other three are judged against: normal profit, efficient '
    'output, and a flat demand curve at the market price.',
    tariff_kind='fixed'))

# ── Worked calculations whose printed form does not survive extraction ─────
# Every one of these is set as a FRACTION or with SUPERSCRIPTS on the page, and
# flat text does not merely dull them, it falsifies them: the HHI working comes
# out "482 + 272 + ..." once the squares are lost, the multiplier comes out
# "0.3 + 0.2 = 2", and the percentage change loses its numerator outright and
# reads "4761865 x 100 = 7.59 %". So the scheme's own working is cropped and
# rides with the card as a solution figure, the mechanism the tick tables use.

P.cards.append(card(
    'econ-2023-hl-q11-a-i', 2023, 'higher', 'economics-3-5',
    'percentage-change-in-the-irish-population', '2023 HL Q11(a)(i)',
    'Using the data in the table below (extracted from the infographic above), calculate the '
    'percentage change in the Irish population from 2016 to 2022. Show your workings.',
    '8', 8,
    [point('r-1', as_option(block(BODY, '4761865 \u00d7 100 = 7.59 %', '- 1 Mark if %')), 8,
           'The base is the EARLIER population, so the change divides by the 2016 figure, not '
           'the 2022 one. A mark goes for the % sign.')],
    'The table gives the total change outright, so the arithmetic is one division \u2014 but '
    'dividing by the wrong year is the standard slip, and it makes the answer look plausible.',
    tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p15-q11ai-working'))

P.cards.append(card(
    'econ-2023-hl-q12-b-i', 2023, 'higher', 'economics-2-0',
    'calculating-the-herfindahl-hirschman-index', '2023 HL Q12(b)(i)',
    'Based upon the figures in the bar chart above, calculate the Herfindahl Hirschman Index '
    'for Irish Dairy Producers. Show your workings.',
    '9', 9,
    [point('r-1', as_option(block(BODY, '482 + 272 + 82 + 72 + 32 + 32 + 22 + 22 = 3172',
                                  '(ii) Would you consider this market')), 9,
           'Every share is SQUARED before adding \u2014 that is what makes the index sensitive '
           'to the big firms. Adding the shares unsquared gives 100 for any market at all.')],
    'The shares are read off the bar chart, and all eight go in. Squaring is the whole point: it '
    'is why two firms on 48 and 27 dominate the index.',
    tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p21-q12bi-working'))

P.cards.append(card(
    'econ-2023-hl-q13-b-i-mps', 2023, 'higher', 'economics-3-0',
    'marginal-propensity-to-save-from-the-mpc', '2023 HL Q13(b)(i)',
    'Calculate the marginal propensity to save (MPS) for this economy. Show your workings.',
    '3 @ 2', 6,
    [point('r-1', as_option(block(BODY, '1- MPC 1-0.7', 'Calculate the value of the multiplier')), 6,
           'Three steps at two marks each: the relationship, the substitution and the figure. '
           'MPS is what is left of a marginal euro after consumption \u2014 imports do not come '
           'into it, so the MPM of 0.2 in the table is not used here.')],
    'The table supplies MPC and MPM together, which invites subtracting both. Saving is 1 minus '
    'the propensity to CONSUME.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2023-hl-q13-b-ii-multiplier', 2023, 'higher', 'economics-3-0',
    'the-multiplier-in-an-open-economy', '2023 HL Q13(b)(ii)',
    'Calculate the value of the multiplier in this open economy. Show your workings.',
    '4 @ 2', 8,
    [point('r-1', as_option(block(BODY, '1 \U0001d440\U0001d443\U0001d446+ \U0001d440\U0001d443\U0001d440',
                                  '(iii) How much will the government')), 8,
           'Both leakages go in the denominator TOGETHER, then 1 is divided by the sum. The '
           'scheme prints a second acceptable form built from MPC and MPM, and both reach 2.')],
    'An open economy leaks to saving AND to imports, so a multiplier worked from MPS alone is '
    'too big. The two forms the scheme accepts are the same statement rearranged.',
    tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p24-q13bii-working'))

P.cards.append(card(
    'econ-2023-hl-q15-a-iii', 2023, 'higher', 'economics-3-3',
    'building-a-weighted-composite-price-index', '2023 HL Q15(a)(iii)',
    'The table below shows a country\u2019s composite price index for the following categories '
    'of expenditure: food; transport; and other items. Using the information in the table below '
    'to calculate the price index for the current year. The base value is 100. Show your '
    'workings.',
    '19', 19,
    [point('r-1', as_option(block(BODY, 'item (s) \u20ac year \u20ac 55 X 100 = 110 x 60% = 66.0',
                                  '(b) 22')), 19,
           'Each category gets its own simple index first \u2014 current price over base price '
           'times 100 \u2014 and only THEN is it weighted. The composite is the sum of the '
           'weighted results, not an average of the simple indices.')],
    'The weights are what make it composite: food moves the index almost four times as much as '
    'other items. Averaging the three simple indices ignores that and is the usual wrong answer.',
    tariff_kind='fixed',
    figure_key='economics-2023-HL-scheme-p32-q15aiii-working'))

P.emit()
