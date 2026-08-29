#!/usr/bin/env python3
"""Economics 2024 Ordinary Level — Section B.

Same rules as the Higher paper (see econ_2024_hl.py), with one difference in how
the scheme is laid out: Ordinary Level sets its possible responses as a BULLET
LIST and spells the descending tariff out in words beside the question — "1st @
8", "2nd @ 4" — where Higher Level runs the responses together under bold
headings and puts the tariff in the marks column. Underneath they are the same
shape, so `bullets()` does here what `heads()` does there.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, emit, load, point, tidy  # noqa: E402

YEAR, LEVEL = 2024, 'ordinary'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 11 (a) The chart shows increases in electricity prices',
             'Student Research Project', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, note, notes='', steps=None, stem=''):
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      bullets('• ' + block(BODY, start, end)), note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    # ── Question 11 ─────────────────────────────────────────────────────────
    menu('econ-2024-ol-q11-a-ii', 'economics-1-2', 'effect-of-energy-costs-on-business',
         '2024 OL Q11(a)(ii)',
         'Outline one possible economic effect of these price increases on businesses in Ireland.',
         '1 @ 5', 5, 'An economic effect on business — any one', 1, 5,
         'Increased costs for business due to higher prices',
         '(iii) During winter 2023',
         'One effect, 5 marks.',
         stem='Set on a chart of Irish electricity price increases from 2020 to 2022.'),

    menu('econ-2024-ol-q11-a-iii', 'economics-1-3', 'electricity-credit-rationale',
         '2024 OL Q11(a)(iii)',
         'During winter 2023 – 2024, the Irish government granted all households a credit of €450 '
         'towards their electricity bills. Why, in your opinion, did the government do this?',
         '1 @ 5', 5, 'A reason the government granted the credit — any one', 1, 5,
         'To alleviate the financial burden/economic welfare of Irish households',
         '(b) The diagram below represents the long-run equilibrium',
         'One reason, 5 marks. The question asks for an opinion, and the scheme answers it with '
         'six the examiner will accept — it is not open-ended.'),

    menu('econ-2024-ol-q11-b-iii', 'economics-2-0', 'oligopoly-in-ireland', '2024 OL Q11(b)(iii)',
         'The electricity market is an example of an oligopoly market in Ireland. Give one '
         'example of an oligopoly market in Ireland and explain a reason for your choice.',
         '1 @ 4', 4, 'A reason a market is an oligopoly — any one', 1, 4,
         'Only a few providers dominate the market',
         '(c) Panda Power left the Irish energy market',
         'One reason, 4 marks. The scheme accepts mobile phones, broadband, insurance, banking, '
         'TV services or supermarkets as the example; the marks are for the reason.'),

    # ── Question 12 ─────────────────────────────────────────────────────────
    menu('econ-2024-ol-q12-a-ii', 'economics-3-2', 'benefits-of-increased-employment',
         '2024 OL Q12(a)(ii)',
         'Outline one possible economic benefit of increased employment for the Irish economy.',
         '1 @ 7', 7, 'A benefit of increased employment — any one', 1, 7,
         '• Increased standard of living for citizens',
         '(b) (i) Currently there is a shortage of skilled employees',
         'One benefit, 7 marks.',
         stem='In 2022 the number of people employed in Ireland exceeded 2.5 million for the '
              'first time.'),

    # ── Question 13 ─────────────────────────────────────────────────────────
    menu('econ-2024-ol-q13-b-ii', 'economics-3-3', 'effects-of-food-price-inflation',
         '2024 OL Q13(b)(ii)',
         'Explain one possible economic effect food price inflation will have on consumers.',
         '1 @ 10', 10, 'An effect on consumers — any one', 1, 10,
         '• Reduced purchasing power / standard of living',
         '(c) Toilet paper prices rose',
         'One effect, 10 marks.',
         stem='Set on a chart of annual food price inflation across six countries — Switzerland '
              'lowest, Turkey highest.'),

    # These two are here because they are the paper's only cards on their strand
    # topic — scarcity, and the cost structure of a firm.
    card('econ-2024-ol-q12-b-i', YEAR, LEVEL, 'economics-0-1', 'scarcity-of-labour',
         '2024 OL Q12(b)(i)',
         'Currently there is a shortage of skilled employees in different sectors of the Irish '
         'economy. Explain the economic term scarcity in relation to labour (employees).',
         '1 @ 4', 4,
         # The scheme prints the two wordings as consecutive sentences rather
         # than as a list, and they open with the same eleven words, so neither
         # a bullet split nor an anchor split can separate them — each is cut
         # out by naming where it starts and where the next one does.
         [anyN('r-1', 'Scarcity applied to labour — either wording', 4, 1, 4,
               [as_option(block(BODY, a, b)) for a, b in (
                   ('When applied to labour, scarcity refers to the situation where the number',
                    'When applied to labour, scarcity refers to the situation where there are firms'),
                   ('When applied to labour, scarcity refers to the situation where there are firms',
                    '(ii) The pharmaceutical industry has experienced'))],
               'The scheme gives two wordings of the same idea: demand for workers exceeds the '
               'supply of them. Either earns the 4.')],
         '', tariff_kind='bestNofParts'),

    card('econ-2024-ol-q13-a-ii', YEAR, LEVEL, 'economics-1-5', 'fixed-and-variable-costs',
         '2024 OL Q13(a)(ii)',
         'Explain the difference between fixed costs and variable costs. Give an example in '
         'each case.',
         '2 @ 8', 16,
         [point('r-fixed', 'Fixed Costs: Costs which do not change as output changes / Costs '
                'which have to be paid even if nothing is produced.', 8,
                'The scheme sets the two definitions side by side in a table with their examples '
                'in the next column: rent and loan repayments for fixed.',
                accepts=['Rent', 'Loan repayments']),
          point('r-variable', 'Variable Costs: Costs which do change as output changes.', 8,
                'Examples the scheme prints: electricity, labour, raw materials.',
                accepts=['Electricity', 'Labour', 'Raw materials'])],
         'Carded as two rows rather than one menu: the question asks for the DIFFERENCE, so a '
         'student needs both halves, and picking either from a list would not be answering it.',
         tariff_kind='fixed'),
]

# ── The parts econ_parts found that hand-reading had passed over ────────────
P = Paper(YEAR, LEVEL)
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('ways citizens in Ireland can behave more sustainably', 'econ-2024-ol-q12-c-ii',
       'economics-0-2', 'sustainable-household-behaviour',
       'Outline two ways citizens in Ireland can behave more sustainably in their use of energy.',
       'A way to behave more sustainably — any two',
       'Two ways, 8 marks each.',
       drop=SCAFFOLD)

P.menu('reasons why exports are important for the Irish economy', 'econ-2024-ol-q14-a-ii',
       'economics-4-2', 'importance-of-exports',
       'Outline two reasons why exports are important for the Irish economy.',
       'A reason exports matter — any two',
       # The scheme prints ⟨1 @ 6⟩ and ⟨1 @ 4⟩ against this part, not 6 twice.
       # Found on the second pass, when a duplicate-text check paired this card
       # with a new one written from the same block of scheme.
       'Two reasons, the first paid 6 and the second 4.',
       steps=[6, 4], drop=SCAFFOLD)


# ── A figure card ───────────────────────────────────────────────────────────
P.cards.append(card(
    'econ-2024-ol-q11-b-i', 2024, 'ordinary', 'economics-2-0', 'labelling-an-oligopoly-diagram-ol',
    '2024 OL Q11(b)(i)',
    'The diagram represents the long-run equilibrium of a firm in oligopoly. Write out in full '
    'what each of the three labels represents.',
    'fixed', 24,
    [point('r-1', 'Demand/Average Revenue', 8, 'D=AR — the kinked line falling to the right.'),
     point('r-2', 'Marginal Cost', 8, 'MC — the curve rising through point E.'),
     point('r-3', 'Marginal Revenue', 8, 'MR — the line with a vertical break beneath the kink.')],
    'Abbreviations are not accepted.', tariff_kind='fixed',
    figure_key='economics-2024-OL-paper-p11-art',
    label_key=[{'letter': 'D=AR', 'meaning': 'Demand/Average Revenue', 'askedInThisQuestion': True},
               {'letter': 'MC', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
               {'letter': 'MR', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': True},
               {'letter': 'E', 'meaning': 'the equilibrium, where marginal cost cuts marginal revenue',
                'askedInThisQuestion': False}]))


# ── Section B, second pass ──────────────────────────────────────────────────
# The parts of this paper that list named responses and had no card citing
# them, found by econ_todo.py.
SCAF = ('Possible responses', 'Suggested responses')
SIDES = ('The part is answered either way and the scheme heads the two lists separately, so each '
         'side is its own card.')

# 2024 OL Q11(b)(iii) is NOT here: econ_todo reported it uncarded because the
# part path it reconstructs from the paper is one roman numeral out, and a
# card on that part already exists forty lines above. econ_all.py's duplicate-id
# guard is what caught it.
P.menu('Irish energy market more competitive or less competitive', 'econ-2024-ol-q11-c-i',
       'economics-2-0', 'fewer-firms-and-competition',
       'A fourth energy company left the Irish market. In your opinion, is the Irish energy '
       'market more competitive or less competitive as a result? Explain your choice.',
       'A reason it is less competitive — any one',
       'One explanation, 6 marks. Every response the scheme lists argues that the market became '
       'LESS competitive.',
       ref='2024 OL Q11(c)(i)', claim=1, per=6,
       drop=SCAF + ('result of this development',))

P.menu('pharmaceutical industry has experienced a shortage of skilled labour',
       'econ-2024-ol-q12-b-ii', 'economics-2-1', 'effects-of-a-skills-shortage-on-a-sector',
       'The pharmaceutical industry has experienced a shortage of skilled labour. Explain one '
       'effect a shortage of labour could have on this industry.',
       'An effect on the industry — any one',
       'One effect, 10 marks.',
       ref='2024 OL Q12(b)(ii)', claim=1, per=10,
       drop=SCAF + ('years. Explain one effect',))

P.menu('economic measure the Irish government could take to help increase',
       'econ-2024-ol-q12-b-iii', 'economics-2-1', 'increasing-the-supply-of-skilled-labour',
       'Outline one economic measure the Irish government could take to help increase the supply '
       'of skilled labour in the economy.',
       'A measure to raise the supply of skills — any one',
       'One measure, 10 marks.',
       ref='2024 OL Q12(b)(iii)', claim=1, per=10,
       drop=SCAF + ('supply of more skilled labour',))

P.menu('labour costs increasing some Irish businesses are finding it difficult',
       # Not 'econ-2024-ol-q12-c-ii': that id is already taken by a card which
       # cites 2024 OL Q11(c)(ii) — one of the nineteen whose id counts the
       # wrong question and whose citation econ_refs.py corrects. The ids are
       # left alone because a student's review history is keyed on them, and
       # this is the cost of that: a later card on the REAL Q12(c)(ii) has to
       # find another name.
       'econ-2024-ol-q12-c-ii-unemployment', 'economics-3-2', 'labour-costs-and-unemployment',
       'With labour costs increasing, some Irish businesses are finding it difficult to continue '
       'to operate. Outline how this development may affect unemployment in Ireland.',
       'A way unemployment could rise — either one',
       'One point, 10 marks. Both responses the scheme lists point the same way: unemployment '
       'rises.',
       ref='2024 OL Q12(c)(ii)', claim=1, per=10,
       drop=SCAF + ('to operate. Outline how',))

P.menu('why some people remain unemployed while job vacancies exist',
       'econ-2024-ol-q12-c-iii', 'economics-3-2', 'unemployment-alongside-vacancies',
       'Outline one reason why some people remain unemployed while job vacancies exist in the '
       'Irish economy.',
       'A reason the two coexist — any one',
       'One reason, 10 marks. This is structural unemployment: the vacancies and the unemployed '
       'do not match.',
       ref='2024 OL Q12(c)(iii)', claim=1, per=10, drop=SCAF)

P.menu('manufacturers, like toilet paper companies, use more', 'econ-2024-ol-q13-c-ii-yes',
       'economics-0-2', 'the-case-for-sustainable-materials',
       'In your opinion, should manufacturers, like toilet paper companies, use more expensive '
       'environmentally friendly raw materials? Argue YES.',
       'A reason to say yes — any one',
       'One explanation, 10 marks.',
       ref='2024 OL Q13(c)(ii) — yes', claim=1, per=10,
       drop=SCAF + ('YES Explanation',), stop='NO Explanation', notes=SIDES)

P.menu('manufacturers, like toilet paper companies, use more', 'econ-2024-ol-q13-c-ii-no',
       'economics-0-2', 'the-case-against-sustainable-materials',
       'In your opinion, should manufacturers, like toilet paper companies, use more expensive '
       'environmentally friendly raw materials? Argue NO.',
       'A reason to say no — any one',
       'One explanation, 10 marks.',
       ref='2024 OL Q13(c)(ii) — no', claim=1, per=10,
       drop=SCAF, after='NO Explanation')

P.menu('European Central Bank (ECB) is concerned about inflation rates',
       'econ-2024-ol-q13-c-iii', 'economics-3-3', 'why-the-ecb-fears-inflation',
       'Explain why you think the European Central Bank is concerned about inflation rates in the '
       'euro area.',
       'A reason the ECB is concerned — any one',
       'One explanation, 4 marks.',
       ref='2024 OL Q13(c)(iii)', claim=1, per=4,
       drop=SCAF + ('Explain why you think the ECB',))

P.menu('why the government applies a 0% VAT rate', 'econ-2024-ol-q14-b-i',
       'economics-1-3', 'why-some-goods-are-zero-rated',
       'Outline one reason why the government applies a 0% VAT rate to goods such as milk, bread, '
       'books, children’s clothes and disability aids.',
       'A reason for the zero rate — any one',
       'One reason, 7 marks.',
       ref='2024 OL Q14(b)(i)', claim=1, per=7, drop=SCAF)

P.menu('9% VAT rate for the tourism and hospitality industry would return',
       'econ-2024-ol-q14-b-iii-agree', 'economics-1-3', 'the-case-for-restoring-the-vat-rate',
       'The government announced the 9% VAT rate for the tourism and hospitality industry would '
       'return to 13.5%. Argue that you AGREE with the increase.',
       'A reason to agree — any one',
       'One explanation, 7 marks.',
       ref='2024 OL Q14(b)(iii) — agree', claim=1, per=7,
       drop=SCAF + ('AGREE Explanation',), stop='DISAGREE Explanation', notes=SIDES)

P.menu('9% VAT rate for the tourism and hospitality industry would return',
       'econ-2024-ol-q14-b-iii-disagree', 'economics-1-3',
       'the-case-against-restoring-the-vat-rate',
       'The government announced the 9% VAT rate for the tourism and hospitality industry would '
       'return to 13.5%. Argue that you DISAGREE with the increase.',
       'A reason to disagree — any one',
       'One explanation, 7 marks.',
       ref='2024 OL Q14(b)(iii) — disagree', claim=1, per=7,
       drop=SCAF, after='DISAGREE Explanation')

P.menu('why you think global population has grown so rapidly', 'econ-2024-ol-q16-a-i',
       'economics-3-5', 'why-world-population-grew',
       'Outline one reason why you think global population has grown so rapidly since 1804.',
       'A reason population grew — any one',
       'One reason, 9 marks.',
       ref='2024 OL Q16(a)(i)', claim=1, per=9, drop=SCAF)

P.menu('unretired', 'econ-2024-ol-q16-a-ii', 'economics-2-1', 'older-workers-returning-to-work',
       'Many people over 65 hope to become part of the so-called “unretired”. Outline one effect '
       'on the Irish economy if more people over 65 return to work.',
       'An effect of the unretired — any one',
       'One effect, 9 marks. The scheme lists four gains and one cost: more competition for '
       'younger workers.',
       ref='2024 OL Q16(a)(ii)', claim=1, per=9, drop=SCAF)

P.menu('population is ageing faster than anywhere else in Europe', 'econ-2024-ol-q16-a-iii',
       'economics-3-1', 'ageing-and-the-irish-exchequer',
       'Ireland’s population is ageing faster than anywhere else in Europe. Outline one economic '
       'effect this will have on the Irish government.',
       'An effect on the government — any one',
       'One effect, 9 marks.',
       ref='2024 OL Q16(a)(iii)', claim=1, per=9, drop=SCAF)

P.menu('Corporation tax is now the second largest source of tax revenue',
       'econ-2024-ol-q16-b-i', 'economics-3-1', 'the-risk-in-corporation-tax',
       'Corporation tax is now the second largest source of tax revenue for Ireland. Outline one '
       'possible risk to the Irish economy of this development.',
       'A risk of the reliance — any one',
       'One risk, 10 marks.',
       ref='2024 OL Q16(b)(i)', claim=1, per=10,
       drop=SCAF + ('Outline one possible risk',))

P.menu('corporation tax rate set to rise', 'econ-2024-ol-q16-b-ii-adv',
       'economics-3-1', 'raising-corporation-tax-advantage',
       'Ireland’s corporation tax rate rose from 12.5% to 15% as part of a global deal. Outline '
       'one possible economic ADVANTAGE of this for Ireland.',
       'An advantage of the rise — any one',
       'One advantage, 9 marks.',
       ref='2024 OL Q16(b)(ii) — advantage', claim=1, per=9,
       drop=SCAF + ('Economic advantage:',), stop='Economic disadvantage',
       notes='The part asks for one of each and the scheme heads the two lists separately, so '
             'each side is its own card.')

P.menu('corporation tax rate set to rise', 'econ-2024-ol-q16-b-ii-dis',
       'economics-3-1', 'raising-corporation-tax-disadvantage',
       'Ireland’s corporation tax rate rose from 12.5% to 15% as part of a global deal. Outline '
       'one possible economic DISADVANTAGE of this for Ireland.',
       'A disadvantage of the rise — any one',
       'One disadvantage, 9 marks.',
       ref='2024 OL Q16(b)(ii) — disadvantage', claim=1, per=9,
       drop=SCAF, after='Possibility that some MNCs might relocate')

P.menu('new mortgage borrowing rules has a positive or negative', 'econ-2024-ol-q16-c-i-pos',
       'economics-1-1', 'looser-mortgage-rules-positive',
       'Do you think the new mortgage borrowing rules has a positive or negative effect on '
       'first-time home buyers and the Irish housing market? Explain a POSITIVE effect.',
       'A positive effect — any one',
       'One explanation, 10 marks.',
       ref='2024 OL Q16(c)(i) — positive', claim=1, per=10,
       drop=SCAF + ('Positive effect explanation',), stop='Negative effect explanation',
       notes=SIDES)

P.menu('new mortgage borrowing rules has a positive or negative', 'econ-2024-ol-q16-c-i-neg',
       'economics-1-1', 'looser-mortgage-rules-negative',
       'Do you think the new mortgage borrowing rules has a positive or negative effect on '
       'first-time home buyers and the Irish housing market? Explain a NEGATIVE effect.',
       'A negative effect — any one',
       'One explanation, 10 marks.',
       ref='2024 OL Q16(c)(i) — negative', claim=1, per=10,
       drop=SCAF, after='Negative effect explanation')

# The plain id is taken by a card citing 2024 OL Q14(a)(ii) on the importance of
# exports — one of the parts whose reconstructed path is a numeral out. Left
# alone because review history is keyed on it.
P.menu('reason why the Irish government contributes to the EU', 'econ-2024-ol-q14-a-ii-eu',
       'economics-4-1', 'why-ireland-pays-into-the-eu-budget',
       'Outline one reason why the Irish government contributes to the EU.',
       'A reason Ireland contributes — any one',
       'One reason, 4 marks. The scheme lists eight.',
       ref='2024 OL Q14(a)(ii)', claim=1, per=4,
       drop=SCAF + ('Outline one reason why the Irish government contributes',))

P.menu('Revolut becoming a mortgage lender', 'econ-2024-ol-q16-c-ii',
       'economics-2-0', 'a-new-entrant-to-the-mortgage-market',
       'Outline one possible economic effect Revolut becoming a mortgage lender may have.',
       'An economic effect — any one', 'One effect, 10 marks.',
       ref='2024 OL Q16(c)(ii)', claim=1, per=10,
       drop=SCAF + ('Evidence of Data', 'The Research Process', 'Process overall mark',
                    'Deduct 1m'))

# ── Section B, third pass ───────────────────────────────────────────────────
# The definition and read-the-answer parts of this paper. None of them lists a
# menu of bulleted responses, so econ_parts cannot see them: each is one
# printed answer, or a handful of consecutive wordings, sliced by anchor.

P.cards.append(card(
    'econ-2024-ol-q13-c-i', YEAR, LEVEL, 'economics-3-3', 'cost-push-inflation',
    '2024 OL Q13(c)(i)',
    'Explain what is meant by the economic term, cost-push inflation.',
    'fixed', 10,
    [point('r-1', as_option(block(BODY, 'This occurs when the source of upward pressure',
                                  '(ii) In your opinion, should manufacturers')), 10,
           'One explanation, 10 marks. The scheme answers with the definition and then its '
           'imported form — dearer raw materials from abroad passing into home prices — as one '
           'continuous explanation.')],
    '', stem='Toilet paper prices rose by 15.6% in 2022 because manufacturers used more '
             'expensive environmentally friendly raw materials — the paper names this as an '
             'example of cost-push inflation.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2024-ol-q14-a-iii', YEAR, LEVEL, 'economics-3-1', 'national-debt',
    '2024 OL Q14(a)(iii)',
    'Outline what is meant by the economic term national debt.',
    'fixed', 4,
    [point('r-1', as_option(block(BODY, 'The total / cumulative amount of government borrowing',
                                  'According to the NTMA')), 4,
           'One definition, 4 marks. The scheme adds that Ireland’s gross national debt stood '
           'at €235.9bn at the end of April 2023 — one of the highest per-capita burdens in '
           'the world.')],
    '', tariff_kind='fixed'))

# The scheme prints the applied almond-milk answer first and then three generic
# wordings as consecutive sentences, not bullets — each is cut out by naming
# where it starts and where the next one does, as with scarcity above.
P.cards.append(card(
    'econ-2024-ol-q15-b-iii', YEAR, LEVEL, 'economics-1-1', 'substitute-goods',
    '2024 OL Q15(b)(iii)',
    'Almond milk can be classed as a substitute good for cow’s milk. Explain the meaning of '
    'the economic term substitute good.',
    '1 @ 6', 6,
    [anyN('r-1', 'Substitute good — any wording', 6, 1, 6,
          [as_option(block(BODY, a, b)) for a, b in (
              ('Almond milk can be classed as a substitute good for cow’s milk because',
               'A good that satisfies the same need'),
              ('A good that satisfies the same need', 'A good that can be consumed'),
              ('A good that can be consumed', 'Goods that can be used as alternatives'),
              ('Goods that can be used as alternatives', '(c) (i) Using the formula supplied'))],
          'Any one wording, 6 marks.')],
    '', tariff_kind='bestNofParts'))

P.cards.append(card(
    'econ-2024-ol-q15-c-ii', YEAR, LEVEL, 'economics-1-4', 'reading-a-ped-figure',
    '2024 OL Q15(c)(ii)',
    'Indicate if the demand for a bar of chocolate is price elastic or price inelastic. '
    'Explain your answer.',
    'fixed', 5,
    [point('r-1', as_option(block(BODY, 'Price elastic demand', 'Possible responses')), 5,
           'The 5 marks cover the indication and the explanation as one block; the scheme '
           'states no split between them.')],
    'The calculation itself (20 marks) is not carded — the scheme’s response is the worked '
    'arithmetic. What is carded is reading the answer.',
    stem='Follows the elasticity calculation in (c)(i): the price of a bar of chocolate rose '
         'from 100 cents to 140 cents, demand fell from 90 bars to 50, and the PED came '
         'to −1.71.',
    tariff_kind='fixed'))

# ── The part whose question IS a chart ─────────────────────────────────────
# Excluded until now as "answered by reading the unemployment chart printed
# beside it". The crop is catalogued with verified alt text and an md5 the
# build re-checks, so binding it gives the student what the candidate had, and
# the scheme's response is ordinary prose quoting figures off the bars.
P.cards.append(card(
    'econ-2024-ol-q12-c-i', 2024, 'ordinary', 'economics-3-2',
    'overall-trend-in-irish-unemployment', '2024 OL Q12(c)(i)',
    'Identify the overall trend in Irish unemployment using figures from the graph above.',
    '6', 6,
    [point('r-1', as_option(block(BODY,
        'Based on the above data, the rate of unemployment in Ireland remained broadly stable',
        'Outline one')), 6,
        'One statement of the trend, 6 marks. The scheme wants the direction AND the figures '
        'that show it \u2014 the peak, the floor and the movement between them.')],
    'The bars barely move, and the scheme rewards saying so precisely: "broadly stable or '
    'slightly increased" with 4.5 and 4.3 quoted is a better answer than calling it a rise.',
    tariff_kind='fixed',
    figure_key='economics-2024-OL-paper-p15-i0'))


emit(cards + P.cards)
