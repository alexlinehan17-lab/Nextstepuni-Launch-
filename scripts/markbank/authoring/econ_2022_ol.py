#!/usr/bin/env python3
"""Economics 2022 Ordinary Level — Section B.

Authored against econ_parts; see econ_2021_hl.py for what `drop` is for.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

P = Paper(2022, 'ordinary')
SCAFFOLD = ('Possible responses', 'Suggested responses', 'Minimum Unit Price for A')

P.menu('advantages for consumers of many firms providing streaming', 'econ-2022-ol-q11-a-ii',
       'economics-2-0', 'advantages-of-many-firms-for-consumers',
       'Outline two advantages for consumers of many firms providing streaming services in this '
       'market.',
       'An advantage to consumers — any two',
       'Two advantages, the first paid 8 and the second 4.',
       claim=2, per=8, steps=[8, 4], drop=SCAFFOLD,
       stem='Set on a chart of US streaming services by number of users — YouTube highest, '
            'Vimeo lowest.')

P.menu('Firms who may wish to enter a monopoly industry face barriers', 'econ-2022-ol-q11-c-ii',
       'economics-2-0', 'barriers-to-entry',
       'Firms who may wish to enter a monopoly industry face barriers to entry. Outline two '
       'possible barriers to entry.',
       'A barrier to entry — any two',
       'Two barriers, 4 marks each.',
       drop=SCAFFOLD)

P.menu('two ways that a business could be more sustainable', 'econ-2022-ol-q12-c-ii',
       'economics-0-2', 'ways-a-business-can-be-sustainable',
       'Suggest two ways that a business could be more sustainable.',
       'A way to be more sustainable — any two',
       'Two ways, 7 marks each.',
       drop=SCAFFOLD)

P.menu('features/characteristics of a less developed nation', 'econ-2022-ol-q13-a-i',
       'economics-4-0', 'features-of-a-less-developed-nation',
       'Outline two features/characteristics of a less developed nation.',
       'A feature of a less developed nation — any two',
       'Two features, 8 marks each.',
       drop=SCAFFOLD)

P.menu('reasons why the Irish government gives aid', 'econ-2022-ol-q13-a-ii',
       'economics-4-0', 'why-ireland-gives-aid',
       'Outline two reasons why the Irish government gives aid to less developed nations.',
       'A reason Ireland gives aid — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD)

P.menu('reasons why TikTok would locate in Ireland', 'econ-2022-ol-q14-a-ii',
       'economics-4-1', 'why-mncs-locate-in-ireland-ol',
       'Outline two reasons why TikTok would locate in Ireland.',
       'A reason an MNC locates in Ireland — any two',
       'Two reasons, 4 marks each.',
       drop=SCAFFOLD)

P.menu('economic benefits to the local community of a Multi-National', 'econ-2022-ol-q14-a-iii',
       'economics-4-1', 'local-benefits-of-an-mnc',
       'Describe two possible economic benefits to the local community of a Multi-National '
       'Company locating there.',
       'A benefit to the local community — any two',
       'Two benefits, 4 marks each.',
       drop=SCAFFOLD)

P.menu('benefits to the Irish economy of exporting', 'econ-2022-ol-q14-b-ii',
       'economics-4-2', 'benefits-of-exporting',
       'Outline two benefits to the Irish economy of exporting to other countries.',
       'A benefit of exporting — any two',
       'Two benefits, 8 marks each.',
       drop=SCAFFOLD, cap=5)

P.menu('reasons why the government introduced minimum pricing', 'econ-2022-ol-q15-a-i',
       'economics-1-3', 'minimum-pricing-on-alcohol',
       'Outline two reasons why the government introduced minimum pricing on alcohol.',
       'A reason for minimum pricing — any two',
       'Two reasons, 6 marks each.',
       drop=SCAFFOLD)

P.menu('one social benefit and one private benefit of the government increasing the tax on cigaret',
       'econ-2022-ol-q15-a-iii-social', 'economics-2-2', 'social-benefits-of-cigarette-tax',
       'Outline one social benefit of the government increasing the tax on cigarettes.',
       'A social benefit — any one',
       'One social benefit, 4 marks; the paper pays a private benefit at 4 as well.',
       ref='2022 OL Q15(a)(iii) — social benefit',
       claim=1, per=4, drop=SCAFFOLD, stop='Private Benefits',
       notes='The scheme heads the social benefits and the private benefits separately, and the '
             'question wants one of each, so each side is its own card.')

P.menu('one social benefit and one private benefit of the government increasing the tax on cigaret',
       'econ-2022-ol-q15-a-iii-private', 'economics-2-2', 'private-benefits-of-cigarette-tax',
       'Outline one private benefit of the government increasing the tax on cigarettes.',
       'A private benefit — any one',
       'One private benefit, 4 marks.',
       ref='2022 OL Q15(a)(iii) — private benefit',
       claim=1, per=4,
       drop=SCAFFOLD + ('Greater productivity', 'Reduction in cancer', 'Reduced pressure on hosp',
                        'Population healthier', 'Improved environment', 'Private Benefits'))

# The id counts the wrong part: the paper prints this question at Q16(b)(ii) —
# (a)(ii) is the smoking-measures question, carded below as
# econ-2022-ol-q16-a-ii-smoking. The id is left alone (review history is keyed
# on it) and the citation is corrected here, the same call econ_refs.py makes
# for the nineteen cards whose id counts the wrong question.
P.menu('economic effects which this rate of price inflation may have', 'econ-2022-ol-q16-a-ii',
       'economics-3-3', 'effects-of-inflation-on-citizens',
       'Discuss two economic effects which this rate of price inflation may have on Irish '
       'citizens.',
       'An effect on citizens — any two',
       'Two effects, 8 marks each.',
       ref='2022 OL Q16(b)(ii)', drop=SCAFFOLD)

P.menu('governments can intervene in the market', 'econ-2022-ol-q11-c-iii',
       'economics-1-3', 'government-intervention-dominant-firm',
       'Suggest one way governments can intervene in the market if one firm becomes too dominant.',
       'A way government can intervene — either one',
       'One way, 4 marks. The scheme names two: regulate the firm, or legislate against the '
       'behaviour.',
       claim=1, per=4, drop=SCAFFOLD)


# ── A figure card ───────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2022-ol-q11-b-i', 2022, 'ordinary', 'economics-2-0', 'labelling-a-monopoly-diagram',
    '2022 OL Q11(b)(i)',
    'The diagram shows a firm operating under conditions of monopoly. Write out in full what '
    'each of the three numbered items represents.',
    'fixed', 21,
    [point('r-1', 'Price', 7, 'Item 1 — the vertical axis.'),
     point('r-2', 'Marginal Cost', 7, 'Item 2 — the U-shaped curve rising to the right, above AC.'),
     point('r-3', 'Marginal Revenue', 7, 'Item 3 — the steeper of the two downward-sloping lines. '
                                         'AC and AR are already labelled on the diagram.')],
    'Abbreviations are not accepted.', tariff_kind='fixed',
    figure_key='economics-2022-OL-paper-p11-i0',
    label_key=[{'letter': '1', 'meaning': 'Price', 'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': True},
               {'letter': 'AC', 'meaning': 'Average Cost', 'askedInThisQuestion': False},
               {'letter': 'AR', 'meaning': 'Average Revenue', 'askedInThisQuestion': False}]))


# ── Section B, second pass ──────────────────────────────────────────────────
# The plain id 'econ-2022-ol-q13-a-ii' is taken by a card citing 2022 OL
# Q14(c)(ii) — one of the nineteen whose id counts the wrong question, left
# alone because review history is keyed on it. See econ_refs.py.
P.menu('Explain current OR capital government expenditure', 'econ-2022-ol-q13-a-ii-expenditure',
       'economics-3-1', 'current-versus-capital-spending',
       'Explain current OR capital government expenditure, using a relevant example to support '
       'your answer.',
       'One of the two kinds of spending — either one',
       'One explanation with an example, 9 marks. Capital spending buys something that lasts; '
       'current spending is the day-to-day bill.',
       ref='2022 OL Q13(a)(ii)', claim=1, per=9,
       drop=SCAFFOLD + ('support your answer. Tick',))

P.menu('reason for the increase in consumer spending', 'econ-2022-ol-q13-c-i',
       'economics-1-1', 'why-consumer-spending-rose',
       'Outline one possible reason for the increase in consumer spending in Ireland in 2023.',
       'A reason spending rose — any one', 'One reason, 10 marks.',
       ref='2022 OL Q13(c)(i)', claim=1, per=10, drop=SCAFFOLD)

P.menu('economic argument in favour of the reintroduction of water charges',
       'econ-2022-ol-q14-b-i', 'economics-1-3', 'the-case-for-water-charges',
       'Outline one economic argument in favour of the reintroduction of water charges.',
       'An argument for water charges — any one', 'One argument, 7 marks.',
       ref='2022 OL Q14(b)(i)', claim=1, per=7, drop=SCAFFOLD)

P.menu('benefits of the government collecting corporation tax', 'econ-2022-ol-q15-a-ii',
       'economics-3-1', 'what-corporation-tax-pays-for',
       'Explain the benefits of the government collecting corporation tax.',
       'A benefit of the revenue — any one', 'One benefit, 9 marks.',
       ref='2022 OL Q15(a)(ii)', claim=1, per=9, drop=SCAFFOLD)

# 2022 OL Q16(b)(ii), the inflation effects, is carded above as
# econ-2022-ol-q16-a-ii — the id counts the wrong part and the citation is
# corrected on the call. Duplicate TEXT is the check that stops it being carded
# twice — a duplicate id would not have caught it, the ids differ.

# ── Section B, third pass ──────────────────────────────────────────────────
P.menu('consumers behaving rationally', 'econ-2022-ol-q13-c-ii',
       'economics-1-1', 'what-a-rational-consumer-does',
       'Explain the concept of consumers behaving rationally, using an example to support '
       'your answer.',
       'The explanation and an example — both of these',
       'Explanation 6 and example 4.',
       ref='2022 OL Q13(c)(ii)', claim=2, per=6, steps=[6, 4], drop=SCAFFOLD)

P.menu('Explain the term indirect tax giving', 'econ-2022-ol-q16-c-i',
       'economics-3-1', 'what-an-indirect-tax-is',
       'Explain the term indirect tax, giving an example other than excise duties.',
       'The explanation and an example — both of these',
       'Explanation and example, 8 marks between them.',
       ref='2022 OL Q16(c)(i)', claim=2, per=4, drop=SCAFFOLD)

P.menu('Explain the term hidden economy', 'econ-2022-ol-q16-c-ii',
       'economics-3-1', 'what-the-hidden-economy-is',
       'Explain the term hidden economy, giving one other example of such an activity.',
       'The explanation and an example — both of these',
       'Explanation and example, 8 marks each.',
       ref='2022 OL Q16(c)(ii)', claim=2, per=8, drop=SCAFFOLD)

P.menu('Have been consistent to the US with no major changes',
       'econ-2022-ol-q15-c-i', 'economics-4-2', 'reading-irish-export-trends',
       "Comment on the trends in Ireland's exports to the US and to the UK using the figures "
       'in the graph.',
       'The trend on each side — both of these', 'US 6 and UK 6.',
       ref='2022 OL Q15(c)(i)', claim=2, per=6,
       drop=SCAFFOLD + ('Exports to the UK',))

# ── Section B, fourth pass: the non-menu parts ─────────────────────────────
# Definitions with one printed answer, and menu parts whose tariff cell the
# extractor left in a neighbouring segment, so econ_parts cannot see them.
# Sliced from the scheme directly, the way econ_2023_ol_seca.py builds its Q10.
BODY = tidy(load(2022, 'ordinary'))

P.cards.append(card(
    'econ-2022-ol-q11-c-i', 2022, 'ordinary', 'economics-2-0', 'what-a-monopoly-is',
    '2022 OL Q11(c)(i)',
    'Explain the term monopoly and give one example of a monopoly that you are familiar with '
    'in Ireland.',
    'fixed', 9,
    [point('r-1', 'A monopoly firm arises when there is only one firm in the industry.', 5,
           'The explanation, 5 marks.'),
     point('r-2', 'An example — An Post, Irish Rail, Irish Water, a sole pub in your village.', 4,
           'Any one example, 4 marks.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-q12-b-i', 2022, 'ordinary', 'economics-1-1', 'what-shifts-demand',
    '2022 OL Q12(b)(i)',
    'If a celebrity was featured on a social media platform (TikTok) wearing Gym + Coffee '
    'clothing how might this effect the demand for Gym + Coffee clothing?',
    'fixed', 8,
    [point('r-1', 'This would lead to an increase in the quantity demanded for Gym + Coffee '
                  'clothing. The celebrity endorsement would make the clothing more attractive '
                  'to the consumer. Appearing on the social media platform is advertising the '
                  'clothing and makes it more well-known so the demand for the clothing would '
                  'increase.', 8, 'The effect and why, 8 marks.')],
    'Parts (ii) and (iii) mark the shift and the new equilibrium on the printed diagram and '
    'are not carded.',
    stem='Set beside a demand-and-supply diagram for Gym + Coffee clothing.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-q12-c-i', 2022, 'ordinary', 'economics-0-2', 'what-sustainability-is',
    '2022 OL Q12(c)(i)',
    'Nineteen30 café in Limerick offers its customers a fresh and sustainable approach to '
    'convenience coffee. Explain the term sustainability.',
    '1 @ 5', 5,
    [anyN('r-1', 'The definition — either wording', 5, 1, 5,
          ['Achieving economic growth without harming society or the environment.',
           'Meeting the current needs of humanity without compromising the ability of future '
           'generations to meet their needs.'],
          'One definition, 5 marks: 3 for the definition and 2 for development.')],
    ''))

P.cards.append(card(
    'econ-2022-ol-q13-b-i', 2022, 'ordinary', 'economics-3-0', 'the-national-income-formula',
    '2022 OL Q13(b)(i)',
    'National Income is calculated using the formula: National Income = Consumption + I + '
    'Government Spending + X – M. State what each of the letters I, X and M stand for.',
    'fixed', 12,
    [point('r-1', 'I: Investment X: Exports M: Imports', 12,
           'All three letters. The scheme prints 12 for the part with no per-letter split, so '
           'the three answers are held as one point.')],
    '', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2022-ol-q13-b-iii', 2022, 'ordinary', 'economics-3-0', 'meaning-of-the-multiplier',
    '2022 OL Q13(b)(iii)',
    'The multiplier formula for an open economy is 1 ÷ (MPS + MPM). Assume that MPS is 0.1 '
    'and MPM is 0.4, giving a multiplier of 2. Explain the economic meaning of the figure you '
    'have calculated for the multiplier.',
    '1 @ 6', 6,
    [anyN('r-1', 'The meaning — either wording', 6, 1, 6,
          ['For any €1 injected into the economy, national income will double.',
           'For each euro spent in the economy, National Income will increase by €2.'],
          'The meaning of the figure, 6 marks.')],
    'Part (ii), the calculation itself, is the worked arithmetic and is not carded; its '
    'result is folded into the question so this part stands alone.'))

# The plain ids econ-2022-ol-q14-a-ii and -q14-a-iii are taken by cards citing
# 2022 OL Q15(b)(ii) and Q15(b)(iii) — see econ_refs.py — so the true Q14(a)
# parts ride a suffix.
P.cards.append(card(
    'econ-2022-ol-q14-a-ii-scarce', 2022, 'ordinary', 'economics-0-1',
    'what-a-scarce-resource-is',
    '2022 OL Q14(a)(ii)',
    'Glenisk extracts water from local ponds, and filters it for use in its production as '
    'they acknowledge that water is a scarce resource. Explain what a scarce resource is.',
    '1 @ 3', 3,
    [anyN('r-1', 'The definition — any wording', 3, 1, 3,
          ['There is not enough water / the supply of water is finite to meet the needs of '
           'everyone.',
           'The supply of a resource / factor of production is limited the demand is unlimited.',
           'Quantity of goods and services people like to have exceeded the amount which the '
           'economy’s resources are capable of producing.'],
          'The definition, 3 marks.')],
    ''))

P.cards.append(card(
    'econ-2022-ol-q14-a-iii-water', 2022, 'ordinary', 'economics-0-2', 'sustainable-use-of-water',
    '2022 OL Q14(a)(iii)',
    'Comment on Glenisk’s approach to water usage as a scarce resource.',
    'fixed', 7,
    [point('r-1', 'The company tries to minimise the wastage of water and use a sustainable '
                  'approach to the consumption of water for their factory. This approach '
                  'reduces the negative impact on the environment.', 7,
           'The comment, 7 marks.')],
    '',
    stem='Glenisk extracts water from local ponds and filters it for use in its production, '
         'acknowledging that water is a scarce resource.',
    tariff_kind='fixed'))

# Q14(b)'s tariff is printed beside the question head, Section A style: 1st x 10
# (6+4) belongs to part (i) and 2nd x 7 (4+3) to part (ii) — together the 17
# marks Q14 leaves for (b). The (ii) segment itself carries no cell, which is
# why econ_parts cannot see this part.
P.cards.append(card(
    'econ-2022-ol-q14-b-ii-water', 2022, 'ordinary', 'economics-1-3',
    'why-citizens-oppose-water-charges',
    '2022 OL Q14(b)(ii)',
    'Explain why some citizens in Ireland would be unhappy if water charges were reintroduced.',
    '1 @ 7', 7,
    [anyN('r-1', 'A reason citizens would be unhappy — any one', 7, 1, 7,
          bullets(block(BODY, 'Lower standard of living', '22 | P a g e')),
          'One explanation, 7 marks: 4 for the point and 3 for developing it.')],
    'The plain id econ-2022-ol-q14-b-ii is taken by a card citing 2022 OL Q15(c)(ii); see '
    'econ_refs.py.'))

# Carded like econ-2022-ol-q15-c-i: the scheme prints the trend statement, so
# the card holds it rather than leaving the part as a chart read.
P.cards.append(card(
    'econ-2022-ol-q15-a-i-trend', 2022, 'ordinary', 'economics-3-1',
    'reading-corporation-tax-trends',
    '2022 OL Q15(a)(i)',
    'Explain the trend in corporation tax received by the Irish government during the period '
    '2011 to 2020, using the figures in the graph.',
    'fixed', 10,
    [point('r-1', 'There has been a steady increase in the amount of money received by the '
                  'Irish state from corporation tax. It has increased from approx. €4m in 2011 '
                  'to approx. €12m in 2020.', 10,
           '10 marks: 6 for the trend and 4 for supporting figures.')],
    'The plain id econ-2022-ol-q15-a-i is taken by a card citing 2022 OL Q16(a)(i); see '
    'econ_refs.py.',
    stem='Set on a bar chart of corporation tax receipts in € millions, 2011 to 2020.',
    tariff_kind='fixed'))

# The scheme's list of MNC names, one option per name. 'Coca Cola' is printed
# twice (once hyphenated), so the fold on hyphens keeps one of the pair.
_mncs, _seen = [], set()
for _n in block(BODY, 'Apple, Google, Facebook', '(ii) Outline two reasons why TikTok').split(','):
    _n = tidy(_n).rstrip('.')
    _k = _n.replace('-', ' ').lower()
    if _n and _k not in _seen:
        _seen.add(_k)
        _mncs.append(_n)
P.cards.append(card(
    'econ-2022-ol-q15-b-i', 2022, 'ordinary', 'economics-4-1', 'mncs-in-ireland',
    '2022 OL Q15(b)(i)',
    'Name two other Multi-National Corporations operating in Ireland.',
    '2 @ 6', 12,
    [anyN('r-1', 'A Multi-National Corporation in Ireland — any two', 12, 2, 6, _mncs,
          'Two names, 6 marks each.')],
    '', stem='TikTok had shortlisted five Dublin sites for its new headquarters.'))

# The real Q16(a)(ii): the plain id econ-2022-ol-q16-a-ii is taken by the
# inflation-effects card above, whose citation the paper puts at Q16(b)(ii).
P.menu('increased the price of a packet of cigarettes by 50c in Budget',
       'econ-2022-ol-q16-a-ii-smoking', 'economics-1-3', 'measures-to-reduce-smoking',
       'The government increased the price of a packet of cigarettes by 50c in Budget 2022. '
       'Suggest one other measure the government could take to help reduce the consumption '
       'of cigarettes.',
       'A measure to reduce smoking — any one',
       'One measure, 7 marks: 4 for the point and 3 for developing it.',
       ref='2022 OL Q16(a)(ii)', claim=1, per=7,
       drop=SCAFFOLD + ('Suggest one other measure',))

P.cards.append(card(
    'econ-2022-ol-q16-b-i', 2022, 'ordinary', 'economics-3-3', 'what-price-inflation-is',
    '2022 OL Q16(b)(i)',
    'The annual rate of price inflation in Ireland rose by 5.5% in December 2021. Explain '
    'the term price inflation.',
    '1 @ 8', 8,
    [anyN('r-1', 'The definition — either wording', 8, 1, 8,
          ['An increase in the general level of prices for goods & services over a period '
           'of time',
           'A decrease in the value of money / people can buy less with their money.'],
          'One definition, 8 marks: 6 for the definition and 2 for development.')],
    ''))

# econ_excluded records '2022 OL Q16(c)(iii)' as coursework grading bands. That
# entry describes the Student Research Project block the extractor welded onto
# this part's segment, not the part the paper prints, which the scheme answers
# with the six effects sliced here.
P.cards.append(card(
    'econ-2022-ol-q16-c-iii', 2022, 'ordinary', 'economics-3-1',
    'effects-of-the-hidden-economy',
    '2022 OL Q16(c)(iii)',
    'Outline one economic effect for the Irish economy of activities taking place in the '
    'hidden economy.',
    '1 @ 8', 8,
    [anyN('r-1', 'An economic effect — any one', 8, 1, 8,
          bullets(block(BODY, 'Loss of revenue to the government', 'Student Research Project')),
          'One effect, 8 marks.')],
    ''))

# ── Worked calculations the scheme prints in full ──────────────────────────
# The scheme sets a fraction as a stacked 2-D layout, so extraction flattens it:
# the numerator and the answer come out on one line and the denominator after
# them. Nothing is missing and nothing is added — the note on each card says how
# to read the order, which is the honest fix for a layout the text layer cannot
# preserve.

P.cards.append(card(
    'econ-2022-ol-q13-a-i-percentage', 2022, 'ordinary', 'economics-3-1',
    'current-spending-as-a-share-of-total-expenditure', '2022 OL Q13(a)(i)',
    'Calculate current expenditure as a percentage of total government expenditure. Show your '
    'workings.',
    '16', 16,
    [point('r-1', as_option(block(BODY, '\u20ac71.82 bn x 100 = 86.61',
                                  '(ii) Explain current OR capital')), 16,
           'Read as a fraction: \u20ac71.82bn over \u20ac82.92bn, times 100. The scheme stacks '
           'it, so extraction puts the denominator last. The total is the WHOLE pie, not the '
           'capital slice \u2014 dividing by \u20ac11.1bn is the usual error.')],
    'The plain id econ-2022-ol-q13-a-i is taken by a card citing 2022 OL Q14(c)(i), and an id '
    'is never renamed because it keys a student\u2019s review history \u2014 hence the suffix. '
    'The pie prints current and capital separately and the total in its heading, so the '
    'denominator has to be recognised before any arithmetic happens.',
    tariff_kind='fixed',
    figure_key='economics-2022-OL-paper-p16-i0'))

P.cards.append(card(
    'econ-2022-ol-q13-b-ii', 2022, 'ordinary', 'economics-3-0',
    'calculating-the-multiplier-in-an-open-economy', '2022 OL Q13(b)(ii)',
    'The multiplier formula for an open economy is: 1 / (MPS + MPM). Assume that MPS is 0.1 '
    'and MPM is 0.4. Calculate, using the above formula, the size of the multiplier.',
    '12', 12,
    [point('r-1', as_option(block(BODY, '0.1 + 0.4 = 2',
                                  '(iii) Explain the economic meaning of the figure')), 12,
           'The two leakages are ADDED first, then divided into 1. Adding the multipliers of each '
           'leakage separately, or dividing 1 by each in turn, is the usual way this goes wrong.')],
    'The scheme prints this as a fraction with 1 above the line, so the flat text reads '
    '\u201c0.1 + 0.4 = 2\u201d \u2014 which is why the scheme\u2019s own working rides with '
    'the card as a picture.',
    tariff_kind='fixed',
    figure_key='economics-2022-OL-scheme-p20-q13bii-working'))

P.emit()
