#!/usr/bin/env python3
"""Economics 2024 Higher Level — Section B.

Every option is SLICED out of the scheme, never retyped, so re-running this is
how a card's provenance is audited without re-reading the PDF.

What is carded and what is not:

  * `⟨N @ M⟩` over a list of named responses is the shape this subject is full
    of, and it becomes one `anyN` row: claim N, M marks each. The option is the
    scheme's whole response — heading AND the sentence explaining it — because
    "Outline" is what the marks are for and the heading alone would teach a
    student to write a bare list.
  * `⟨1 @ 6⟩ ⟨1 @ 4⟩` is the same shape with a DESCENDING tariff: two answers
    wanted, the first paid 6 and the second 4. It is the commonest tariff on the
    paper, so it is carried honestly with `steps=[6, 4]` rather than averaged to
    "5 marks each" — which is wrong for both halves.
  * A part whose marks are for a DIAGRAM is carded for its written explanation
    only, and says so on the card. The Mark Bank cannot mark a drawing.
  * Section A is not carded here. Its answers are one or two words keyed to an
    infographic printed on the paper, so they need the figure pipeline.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, card, defurnish, emit, heads, load, point, tidy  # noqa: E402

YEAR, LEVEL = 2024, 'higher'
T = tidy(load(YEAR, LEVEL))

# The scheme prints its answers once and the appended table cells repeat them, so
# the body is bounded to the first pass; an anchor found twice would otherwise be
# ambiguous for reasons that have nothing to do with the paper.
BODY = block(T, 'Question 11 Possible Responses Marks', 'Student Research Project')


def opts(chunk, headings):
    """The scheme's named responses, each with the sentence that explains it."""
    return [as_option(h) for h in heads(chunk, headings)]


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         chunk, headings, note, notes='', steps=None, stem=''):
    """One card that is a single bounded menu, which most parts of this paper are."""
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      opts(chunk, headings), note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


# The second pass authors against econ_parts through Paper; the first pass
# built its cards by hand, and both are emitted together.
P = Paper(2024, 'higher')
cards = []

# ── Question 11 ─────────────────────────────────────────────────────────────
q11c = block(BODY, '(iii) Outline one possible disadvantage of increasing tourism',
             '(b) (i) It has been estimated')
cards.append(card(
    'econ-2024-hl-q11-a-iii', YEAR, LEVEL, 'economics-4-1', 'disadvantages-of-tourism',
    '2024 HL Q11(a)(iii)',
    'Outline one possible disadvantage of increasing tourism numbers in the Irish economy.',
    '1 @ 6', 6,
    [anyN('r-1', 'A disadvantage of rising tourism numbers — any one', 6, 1, 6,
          opts(q11c, ['Increased pressure on infrastructure', 'Increased prices',
                      'Increased pressure to secure workers', 'Possible damage to the environment',
                      'Increased littering']),
          'One disadvantage, 6 marks. The scheme wants the point AND the explanation of it — '
          'naming the disadvantage without saying why is not what the marks are for.')],
    'Set on a chart of foreign tourist arrivals in July 2021 and August 2023, but the part itself '
    'does not need the chart: it asks for a disadvantage of rising tourism in general.'))

q11b3 = block(BODY, '(iii) Outline two uses of the information provided by national income statistics',
              '(c) Assume the market for brand of organic ice cream')
cards.append(card(
    'econ-2024-hl-q11-b-iii', YEAR, LEVEL, 'economics-3-0', 'uses-of-national-income-statistics',
    '2024 HL Q11(b)(iii)',
    'Outline two uses of the information provided by national income statistics.',
    '2 @ 4', 8,
    [anyN('r-1', 'A use of national income statistics — any two', 8, 2, 4,
          opts(q11b3, ['Indication of alterations to our standard of living',
                       'A way of comparing the standard of living in different countries',
                       'Help determine EU budget contributions',
                       'Formulating economic policy', 'Evaluating economic policy',
                       'Effective research']),
          'Two uses, 4 marks each. Each is the use and what it is used FOR; the scheme pairs them.')],
    ''))

# ── Question 14 ─────────────────────────────────────────────────────────────
q14a = block(BODY, 'Outline three characteristics (other than many sellers)',
             '(ii) Firms operating under monopolistic competition waste resources')
cards.append(card(
    'econ-2024-hl-q14-a-i', YEAR, LEVEL, 'economics-2-0', 'monopolistic-competition-characteristics',
    '2024 HL Q14(a)(i)',
    'Outline three characteristics (other than many sellers) of a firm operating in '
    'monopolistic competition.',
    '3 @ 5', 15,
    [anyN('r-1', 'A characteristic of monopolistic competition — any three', 15, 3, 5,
          opts(q14a, ['There are many buyers', 'Each firm seeks to maximise profits',
                      'Freedom of entry and exit', 'Reasonable knowledge regarding profits',
                      'Product differentiation exists']),
          'Three characteristics, 5 marks each. "Many sellers" is excluded by the question — the '
          'scheme lists five others, all set in the restaurant market the question describes.')],
    'Set in the Irish restaurant market, given as the example of monopolistic competition.'))

q14b2 = block(BODY, '(ii) Outline one possible economic advantage to consumers of monopolistic',
              'The President of the European Central Bank')
cards.append(card(
    'econ-2024-hl-q14-b-ii', YEAR, LEVEL, 'economics-2-0', 'monopolistic-competition-consumer-advantage',
    '2024 HL Q14(b)(ii)',
    'Outline one possible economic advantage to consumers of monopolistic competitive markets.',
    '1 @ 5', 5,
    [anyN('r-1', 'An advantage to consumers — any one', 5, 1, 5,
          opts(q14b2, ['Consumers benefit from increased choice', 'Access to information',
                       'Normal profit', 'Increased quality of services']),
          'One advantage, 5 marks.')],
    ''))

# ── Question 12 ─────────────────────────────────────────────────────────────
cards.append(menu(
    'econ-2024-hl-q12-a-i', 'economics-3-1', 'canons-of-taxation', '2024 HL Q12(a)(i)',
    'The principle of certainty is one of the canons of taxation, i.e. taxpayers should be '
    'aware of their tax liability. Explain two other canons/principles of taxation.',
    '2 @ 5', 10, 'A canon of taxation — any two', 2, 5,
    block(BODY, 'Explain two other canons/principles of taxation',
          '(ii) Revenue actively challenges all forms of hidden'),
    ['Equity:', 'Economy:', 'Convenience:', 'Taxes should not be perceived',
     'Taxes should assist in the redistribution of income',
     'Taxes should be consistent with and aid the national economic objectives',
     'Taxes should have a stabilising influence on the economy',
     'Tax evasion should not be possible'],
    'Two canons, 5 marks each. Certainty is excluded by the question; the scheme lists eight others.'))

cards.append(menu(
    'econ-2024-hl-q12-a-ii', 'economics-3-1', 'effects-of-the-hidden-economy', '2024 HL Q12(a)(ii)',
    'Outline two effects on the Irish economy of an increase in activities in the hidden economy.',
    '2 @ 5', 10, 'An effect of a growing hidden economy — any two', 2, 5,
    block(BODY, 'Loss of tax revenue to the government/pressure on government services',
          '(iii) A new 30% tax rate for middle-income earners'),
    ['Loss of tax revenue to the government', 'Decline in legitimate business activity',
     'Increased government expenditure on enforcement', 'Increased crime levels',
     'Standards of products/services', 'Increase in employment in the hidden economy'],
    'Two effects, 5 marks each.'))

cards.append(menu(
    'econ-2024-hl-q12-b-iii', 'economics-3-3', 'effects-of-high-inflation', '2024 HL Q12(b)(iii)',
    'Outline two possible economic effects of high price inflation on the Irish economy.',
    '2 @ 3', 6, 'An effect of high price inflation — any two', 2, 3,
    block(BODY, 'Loss of purchasing power / fall in living standards',
          '(c) Up to €10,000 a minute is spent in Ireland'),
    ['Loss of purchasing power / fall in living standards', 'Those on fixed incomes are losing lose out',
     'Possibility of wage demands', 'Loss of international competitiveness',
     'If tax rates are not indexed to the rate of inflation', 'Borrowers may benefit'],
    'Two effects, 3 marks each.'))

cards.append(menu(
    'econ-2024-hl-q12-c-ii', 'economics-2-2', 'demerit-goods', '2024 HL Q12(c)(ii)',
    'Cigarettes are classified as demerit goods. Outline one possible effect of the demerit '
    'good markets.',
    '1 @ 4', 4, 'An effect of demerit good markets — any one', 1, 4,
    block(BODY, 'Over-consumption of a product',
          '(iii) One assumption of consumer behaviour'),
    ['Over-consumption of a product', 'Employment (direct and spin off)', 'Tax revenues',
     'Negative externalities', 'Government funding of programmes to deal with negative externalities'],
    'One effect, 4 marks. The scheme lists benefits as well as harms — employment and tax revenue '
    'are both listed, so "effect" here does not mean "disadvantage".'))

cards.append(menu(
    'econ-2024-hl-q12-c-iii', 'economics-1-1', 'assumptions-of-consumer-behaviour', '2024 HL Q12(c)(iii)',
    'One assumption of consumer behaviour is that they have limited incomes. Explain two other '
    'key assumptions of consumer behaviour.',
    '2 @ 5', 10, 'An assumption of consumer behaviour — any two', 2, 5,
    block(BODY, 'Consumers seek to get maximum utility from that income',
          'Question 13'),
    ['Consumers seek to get maximum utility from that income',
     'Consumers are subject to the law of diminishing marginal utility',
     'Most consumers will act rationally'],
    'Two assumptions, 5 marks each. Limited income is excluded by the question, which leaves '
    'exactly the three the scheme prints.'))

# ── Question 13 ─────────────────────────────────────────────────────────────
cards.append(menu(
    'econ-2024-hl-q13-a-ii', 'economics-3-5', 'consequences-of-a-rising-population', '2024 HL Q13(a)(ii)',
    'Discuss two economic consequences of an increasing population.',
    '1 @ 6 + 1 @ 4', 10, 'An economic consequence of a rising population — any two', 2, 6,
    block(BODY, 'Increased demand for goods & services / larger domestic market for firms',
          '(iii) The infographic on page 21 also highlights'),
    ['Increased demand for goods & services', 'Increased government revenue',
     'Reduction in labour shortages', 'Increased pressure on public services',
     'Increased pressure on the country’s infrastructure', 'Land values / housing shortages'],
    'Two consequences. The paper pays the first 6 and the second 4 — not 5 each. The scheme lists '
    'gains and costs together, so a good answer need not be all one or the other.',
    steps=[6, 4]))

cards.append(menu(
    'econ-2024-hl-q13-a-iii', 'economics-3-1', 'vacant-home-tax', '2024 HL Q13(a)(iii)',
    'Outline two advantages of the introduction of the Vacant Home Tax.',
    '1 @ 6 + 1 @ 4', 10, 'An advantage of the Vacant Home Tax — any two', 2, 6,
    block(BODY, 'Encourage people to sell the vacant property', '(b) (i) Globalisation is not dead'),
    ['Encourage people to sell the vacant property', 'May ease the housing crisis',
     'Revenue for the government', 'Misallocation of resources/opportunity cost/market failure',
     'Reduction on derelict sites'],
    'Two advantages, the first paid 6 and the second 4.',
    steps=[6, 4]))

cards.append(menu(
    'econ-2024-hl-q13-b-ii', 'economics-4-1', 'growth-of-globalisation', '2024 HL Q13(b)(ii)',
    'Explain two reasons behind the growth of globalisation in the second half of the 20th '
    'Century (i.e. between 1950 – 1999).',
    '1 @ 6 + 1 @ 4', 10, 'A reason globalisation grew — any two', 2, 6,
    block(BODY, 'Improved transport - transport advances make global travel easier',
          '(iii) Outline one positive and one negative impact of globalisation'),
    ['Improved transport', 'Improved technology', 'Increased population / increased consumer demands',
     'Peace / recovery following World War II', 'Free Trade agreements',
     'Labour availability and skills'],
    'Two reasons, the first paid 6 and the second 4.',
    steps=[6, 4]))

# ── Question 15 ─────────────────────────────────────────────────────────────
cards.append(menu(
    'econ-2024-hl-q15-a-ii', 'economics-4-0', 'solving-the-ldc-debt-crisis', '2024 HL Q15(a)(ii)',
    'Outline one step which could be taken by the governments of developed countries to help '
    'solve the debt crisis which LDCs are experiencing.',
    '1 @ 5', 5, 'A step developed countries could take — any one', 1, 5,
    block(BODY, 'Abolish the outstanding debt', '(iii) Explain two reasons why financial aid'),
    ['Abolish the outstanding debt', 'Help restructuring of national debts',
     'Allow LDCs to extend the length of the repayment period',
     'Reduce the annual interest repayments', 'Provide financial aid / official development assistance'],
    'One step, 5 marks.',
    stem='Set on a chart showing LDC debt servicing rising from $22bn in 2016 to $43bn in 2022.'))

cards.append(menu(
    'econ-2024-hl-q15-a-iii', 'economics-4-0', 'limits-of-financial-aid', '2024 HL Q15(a)(iii)',
    'Explain two reasons why financial aid given to LDCs may not always help LDCs resolve '
    'their difficulties.',
    '1 @ 6 + 1 @ 4', 10, 'A reason aid may not help — any two', 2, 6,
    block(BODY, 'Countries / citizens may become too dependent on the financial aid',
          '(b) In 2022, the IMD'),
    ['Countries / citizens may become too dependent on the financial aid',
     'Unfair distribution of benefits', 'Financial aid may be ‘tied’',
     'Aid is used to invest in high profile projects', 'Inadequate oversight by the donors'],
    'Two reasons, the first paid 6 and the second 4.',
    steps=[6, 4]))

cards.append(menu(
    'econ-2024-hl-q15-b-i', 'economics-4-2', 'improving-competitiveness', '2024 HL Q15(b)(i)',
    'Suggest two economic measures that the Irish government could implement to continue the '
    'improvement in the competitiveness of firms in Ireland.',
    '2 @ 4', 8, 'A measure to improve competitiveness — any two', 2, 4,
    block(BODY, 'Reduce taxation - a reduction in indirect taxes',
          '(ii) Over the past year, the American dollar'),
    ['Reduce taxation', 'Subsidies to firms in relation to energy costs',
     'Continue to promote foreign direct investment',
     'Increase the availability and affordability of accommodation',
     'Invest more in infrastructure', 'Reduce costs for businesses'],
    'Two measures, 4 marks each.'))

cards.append(menu(
    'econ-2024-hl-q15-c-i', 'economics-4-1', 'reasons-to-join-the-eu', '2024 HL Q15(c)(i)',
    'Give two reasons why countries wish to join the EU.',
    '1 @ 6 + 1 @ 4', 10, 'A reason to join the EU — any two', 2, 6,
    block(BODY, 'Access to the single market - the EU', '(ii) According to a European Agency, Eurostat'),
    ['Access to the single market', 'Ease of movement / travel / work',
     'Provision and protections of citizens’ rights',
     'Access to financial funds / improvements in standard of living',
     'International diplomacy & development', 'Democratic society / structures'],
    'Two reasons, the first paid 6 and the second 4.',
    stem='Set in 2023, the fiftieth anniversary of Ireland joining the EU, with Ukraine and '
         'Moldova seeking membership.',
    steps=[6, 4]))

cards.append(menu(
    'econ-2024-hl-q15-c-iii', 'economics-2-2', 'data-centres-negative-consequences', '2024 HL Q15(c)(iii)',
    'Discuss two possible negative consequences for the Irish economy of these data centres '
    'locating in Ireland.',
    '1 @ 6 + 1 @ 4', 10, 'A negative consequence of data centres — any two', 2, 6,
    block(BODY, 'Energy supplies – Data centres use a large proportion'),
    ['Energy supplies', 'Environmental impact', 'Water –', 'Increased demand of land',
     'Skilled labour shortages'],
    'Two consequences, the first paid 6 and the second 4.',
    stem='Amazon secured planning permission for two new data centres in Dublin despite '
         'objections from environmental groups.',
    steps=[6, 4]))

# The paper's only cards on how a market reaches a new equilibrium. The DIAGRAM
# marks are not carded — the Mark Bank cannot mark a drawing — but the four
# explanation points beside it are exactly what the diagram is meant to show.
for cid, ref, qtext, concept, start, end in [
    ('econ-2024-hl-q11-c-i', '2024 HL Q11(c)(i)',
     'Assume the market for a brand of organic ice cream is in equilibrium. Explain the effect '
     'a prolonged heatwave during the summer in Ireland is most likely to have on the initial '
     'equilibrium position of this market.',
     'demand-shift-heatwave',
     '• D/C shifts to the right (D2).', '(ii) An increase in lactose intolerant consumers'),
    ('econ-2024-hl-q11-c-ii', '2024 HL Q11(c)(ii)',
     'Explain the effect an increase in lactose intolerant consumers is most likely to have on '
     'the initial equilibrium position of this market.',
     'demand-shift-consumer-tastes',
     '• D/C shifts to the left (D2).', '(iii) Producers are receiving a subsidy'),
    ('econ-2024-hl-q11-c-iii', '2024 HL Q11(c)(iii)',
     'Explain the effect producers receiving a subsidy for organic ice cream production is most '
     'likely to have on the initial equilibrium position of this market.',
     'supply-shift-subsidy',
     # Ends at its own Explanation line: it is the last part of the question, so
     # without a bound the fourth point swallows the examiner's summary of it.
     '• S/C shifts to the right (S2).', 'Explanation ⟨4 @ 1⟩ Shift in S/C'),
]:
    cards.append(card(
        cid, YEAR, LEVEL, 'economics-1-0', concept, ref, qtext, '4 @ 1', 4,
        [anyN('r-1', 'What happens to the curve, the price and the quantity — all four', 4, 4, 1,
              [as_option(x) for x in block(BODY, start, end).split('•') if len(x.strip()) > 12][:4],
              'Four points at 1 mark each, and the scheme wants all four: which curve moves and '
              'which way, why, what happens to price, and what happens to quantity. The paper '
              'also pays 5 marks for the diagram itself, which is not carded.')],
        'PARTIAL CARD. The part is worth 9 — 5 for a correctly drawn and labelled diagram and 4 '
        'for the written explanation. Only the explanation is carded; the Mark Bank cannot mark '
        'a drawing.', tariff_kind='fixed'))


# ── Section B, second pass ──────────────────────────────────────────────────
SCAF2 = ('Possible responses', 'Suggested responses', 'Possible Responses')
SIDES2 = ('The part asks for one of each and the scheme heads the two lists separately, so each '
          'side is its own card.')

P.menu('new 30% tax rate for middle-income earners', 'econ-2024-hl-q12-a-iii-tax',
       'economics-3-1', 'a-middle-rate-and-the-taxpayer',
       'A new 30% tax rate for middle-income earners has not been ruled out. Outline one economic '
       'consequence for the TAX PAYER if this new tax rate was introduced.',
       'A consequence for the taxpayer — any one', 'One consequence, 4 marks.',
       ref='2024 HL Q12(a)(iii) — taxpayer', claim=1, per=4,
       drop=SCAF2, stop='Less government revenue from direct taxation',
       notes='The part is answered for the taxpayer OR the government and the scheme lists each '
             'separately, so each side is its own card.')

P.menu('new 30% tax rate for middle-income earners', 'econ-2024-hl-q12-a-iii-gov',
       'economics-3-1', 'a-middle-rate-and-the-exchequer',
       'A new 30% tax rate for middle-income earners has not been ruled out. Outline one economic '
       'consequence for the GOVERNMENT if this new tax rate was introduced.',
       'A consequence for the government — any one', 'One consequence, 4 marks.',
       ref='2024 HL Q12(a)(iii) — government', claim=1, per=4,
       drop=SCAF2, after='Less government revenue from direct taxation')

P.menu('gambling industry in Ireland is', 'econ-2024-hl-q12-c-i',
       'economics-2-2', 'why-regulate-gambling',
       'Outline two reasons why it is important that the gambling industry in Ireland is '
       'regulated.',
       'A reason to regulate gambling — any two',
       'Two reasons, the first paid 4 and the second 2.',
       ref='2024 HL Q12(c)(i)', steps=[4, 2], drop=SCAF2)

P.menu('one positive and one negative impact of globalisation', 'econ-2024-hl-q13-b-iii-pos',
       'economics-4-1', 'positive-impacts-of-globalisation-2024',
       'Outline one positive and one negative impact of globalisation — the POSITIVE side.',
       'A positive impact — any one', 'One impact, 6 marks.',
       ref='2024 HL Q13(b)(iii) — positive', claim=1, per=6,
       drop=SCAF2, stop='Inequality / widens the gap', notes=SIDES2)

P.menu('one positive and one negative impact of globalisation', 'econ-2024-hl-q13-b-iii-neg',
       'economics-4-1', 'negative-impacts-of-globalisation-2024',
       'Outline one positive and one negative impact of globalisation — the NEGATIVE side.',
       'A negative impact — any one', 'One impact, 4 marks.',
       ref='2024 HL Q13(b)(iii) — negative', claim=1, per=4,
       drop=SCAF2, after='Inequality / widens the gap')

P.menu('Explain a reason for this trend', 'econ-2024-hl-q13-c-i',
       'economics-3-1', 'why-corporation-tax-receipts-rose',
       'Corporation tax receipts rose from €3,520m in 2011 to €22,643m in 2022. Explain a reason '
       'for this trend.',
       'A reason for the rise — either one',
       'One reason, 4 marks. The part pays 4 more for outlining the trend itself.',
       ref='2024 HL Q13(c)(i)', claim=1, per=4,
       drop=SCAF2 + ('Irelands corporation tax receipts have been increasing',
                     'Between 2011 and 2022 they have increased',
                     'The biggest increase was from 2021 to 2022'))

P.menu('economic consequence of having a government budget surplus', 'econ-2024-hl-q13-c-iii-pos',
       'economics-3-1', 'benefits-of-a-budget-surplus',
       'Outline one possible POSITIVE economic consequence of having a government budget surplus.',
       'A positive consequence — any one', 'One consequence, 3 marks.',
       ref='2024 HL Q13(c)(iii) — positive', claim=1, per=3,
       drop=SCAF2, stop='Rise in conflicting expectations', notes=SIDES2)

P.menu('economic consequence of having a government budget surplus', 'econ-2024-hl-q13-c-iii-neg',
       'economics-3-1', 'drawbacks-of-a-budget-surplus',
       'Outline one possible NEGATIVE economic consequence of having a government budget surplus.',
       'A negative consequence — any one', 'One consequence, 3 marks.',
       ref='2024 HL Q13(c)(iii) — negative', claim=1, per=3,
       drop=SCAF2, after='Rise in conflicting expectations')

P.menu('waste resources', 'econ-2024-hl-q14-a-ii-agree',
       'economics-2-0', 'monopolistic-competition-wastes-resources',
       'Firms operating under monopolistic competition waste resources. Justify AGREEING with '
       'this statement.',
       'The case that resources are wasted',
       'One justification, 6 marks: the firm does not produce at the minimum of average cost.',
       ref='2024 HL Q14(a)(ii) — agree', claim=1, per=6,
       drop=SCAF2 + ('Do you agree or disagree',), stop='DISAGREE',
       notes='The part is answered either way and the scheme heads the two, so each side is its '
             'own card.')

P.menu('waste resources', 'econ-2024-hl-q14-a-ii-disagree',
       'economics-2-0', 'monopolistic-competition-does-not-waste',
       'Firms operating under monopolistic competition waste resources. Justify DISAGREEING with '
       'this statement.',
       'The case that resources are not wasted',
       'One justification, 6 marks: spending on innovation and variety is not waste.',
       ref='2024 HL Q14(a)(ii) — disagree', claim=1, per=6,
       drop=SCAF2, after='DISAGREE')

P.menu('interest rate increases have on each', 'econ-2024-hl-q14-c-i-spending',
       'economics-3-3', 'interest-rates-and-consumer-spending',
       'Explain one economic effect these interest rate increases have on the level of consumer '
       'spending.',
       'An effect on consumer spending — either one', 'One effect, 4 marks.',
       ref='2024 HL Q14(c)(i) — consumer spending', claim=1, per=4,
       drop=SCAF2, stop='Increased interest payments', notes=SIDES2)

P.menu('interest rate increases have on each', 'econ-2024-hl-q14-c-i-debt',
       'economics-3-1', 'interest-rates-and-the-national-debt',
       'Explain one economic effect these interest rate increases have on Ireland’s national '
       'debt.',
       'An effect on the national debt — either one', 'One effect, 4 marks.',
       ref='2024 HL Q14(c)(i) — national debt', claim=1, per=4,
       drop=SCAF2, after='Increased interest payments')

# ── Q15(c)(ii) and Q16(a): obesity and housing ─────────────────────────────
# The scheme heads the two halves "Economic measure" and "Social measure", and
# the question asks for one of each, so each half is its own card.
P.menu('economic measure and one social measure', 'econ-2024-hl-q15-c-ii-economic',
       'economics-1-3', 'economic-measures-against-obesity',
       'Explain one ECONOMIC measure which, if taken, could help reduce obesity levels in '
       'Ireland.',
       'An economic measure — any one', 'One measure, 6 marks.',
       ref='2024 HL Q15(c)(ii) — economic', claim=1, per=6,
       drop=SCAF2 + ('Economic measure',), stop='Social measure')

P.menu('economic measure and one social measure', 'econ-2024-hl-q15-c-ii-social',
       'economics-1-3', 'social-measures-against-obesity',
       'Explain one SOCIAL measure which, if taken, could help reduce obesity levels in '
       'Ireland.',
       'A social measure — any one', 'One measure, 6 marks.',
       ref='2024 HL Q15(c)(ii) — social', claim=1, per=6,
       drop=SCAF2 + ('Economic measure',), after='Social measure')

P.menu('reasons for the increase in the number of homeless people',
       'econ-2024-hl-q16-a-i', 'economics-1-3', 'why-homelessness-rose-in-ireland',
       'Outline two reasons for the increase in the number of homeless people in Ireland.',
       'A reason homelessness rose — any two', 'Two reasons, 6 marks each.',
       ref='2024 HL Q16(a)(i)', claim=2, per=6, drop=SCAF2)

P.menu('Revitalisation of local communities',
       'econ-2024-hl-q16-a-ii', 'economics-1-3', 'benefits-of-social-housing-spending',
       'Discuss two benefits of increasing expenditure on social housing, apart from helping '
       'to reduce homelessness.',
       'A benefit — any two', 'Two benefits, 6 marks each.',
       ref='2024 HL Q16(a)(ii)', claim=2, per=6, drop=SCAF2)

P.menu('Void in Irish banking market', 'econ-2024-hl-q14-c-iii',
       'economics-2-0', 'why-neobanks-grew-in-ireland',
       'Outline two reasons why the number of people using the services offered by '
       'Neobanks/Challenger banks such as Revolut and N26 has grown rapidly in Ireland.',
       'A reason they grew — any two', 'Two reasons, 6 marks each.',
       ref='2024 HL Q14(c)(iii)', claim=2, per=6, drop=SCAF2)

P.menu('Irish exports should increase', 'econ-2024-hl-q15-b-ii',
       'economics-4-2', 'a-stronger-dollar-and-irish-trade',
       'Outline the effects an increase in the value of the American dollar could have on '
       "Ireland's exports to the US and on Irish imports from the US.",
       'The effect on each side — both of these', 'Two effects, 5 marks each.',
       ref='2024 HL Q15(b)(ii)', claim=2, per=5,
       drop=SCAF2 + ('Outline the effects this increase in the value',))

P.menu('Capital expenditure is spending on items not used up', 'econ-2024-hl-q16-c-i',
       'economics-3-1', 'what-capital-expenditure-is',
       'Explain the term capital expenditure, using an example other than transport.',
       'The explanation — this one', 'The explanation carries 4 with 2 for the example.',
       ref='2024 HL Q16(c)(i)', claim=1, per=4, drop=SCAF2)

# The scheme heads the halves "Social benefit:", and the question asks for one
# cost and one benefit, so each is its own card.
P.menu('social cost and one social benefit of the proposed DART', 'econ-2024-hl-q16-c-ii-cost',
       'economics-2-2', 'social-costs-of-the-dart-project',
       'Outline one social COST of the proposed DART+ project.',
       'A social cost — any one', 'One cost, 5 marks; a benefit is worth 5 as well.',
       ref='2024 HL Q16(c)(ii) — cost', claim=1, per=5,
       drop=SCAF2, stop='Social benefit:')

P.menu('social cost and one social benefit of the proposed DART', 'econ-2024-hl-q16-c-ii-benefit',
       'economics-2-2', 'social-benefits-of-the-dart-project',
       'Outline one social BENEFIT of the proposed DART+ project.',
       'A social benefit — any one', 'One benefit, 5 marks; a cost is worth 5 as well.',
       ref='2024 HL Q16(c)(ii) — benefit', claim=1, per=5,
       drop=SCAF2 + ('Social benefit:',), after='Social benefit:')

# The scheme runs advantages then disadvantages, marking the turn with "Disad"
# at the end of the built-in-stabiliser line, so each side is its own card.
P.menu('Low collection cost', 'econ-2024-hl-q16-c-iii-advantage',
       'economics-3-1', 'advantages-of-indirect-taxation',
       'Outline one advantage of raising tax revenue through increasing indirect taxation.',
       'An advantage — any one', 'One advantage, 6 marks; a disadvantage is worth 6 too.',
       ref='2024 HL Q16(c)(iii) — advantage', claim=1, per=6,
       drop=SCAF2 + ('The Research Process', 'Data (Application'),
       stop='Will increase inflation')

P.menu('Low collection cost', 'econ-2024-hl-q16-c-iii-disadvantage',
       'economics-3-1', 'disadvantages-of-indirect-taxation',
       'Outline one disadvantage of raising tax revenue through increasing indirect taxation.',
       'A disadvantage — any one', 'One disadvantage, 6 marks; an advantage is worth 6 too.',
       ref='2024 HL Q16(c)(iii) — disadvantage', claim=1, per=6,
       drop=SCAF2 + ('The Research Process', 'Data (Application'),
       after='Will increase inflation')

emit(cards + P.cards)
