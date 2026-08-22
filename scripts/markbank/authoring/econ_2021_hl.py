#!/usr/bin/env python3
"""Economics 2021 Higher Level — Section B.

Authored against econ_parts, which reads the tariff and the response headings off
the scheme, so each card states only what a machine cannot decide: the topic, the
question as a student should read it, and whether the part is a menu at all.

`drop` removes the scheme's own scaffolding — "Suggested responses:", the heading
over a list — and, where one part answers two opposite questions, the half a
given card is not about.

The second cell of a pair here — ⟨2 @ 7⟩ ⟨(3 + 4)⟩ — is the split WITHIN one
answer (3 for the point, 4 for developing it), not between the two answers.
Reading it as a descending tariff would halve the marks, so it goes on the row
note instead.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, block, card, defurnish, load, point, tidy  # noqa: E402

P = Paper(2021, 'higher')
SCAFFOLD = ('Suggested responses', 'Possible responses')

P.menu('positive impacts and two negative', 'econ-2021-hl-q12-a-ii-pos',
       'economics-4-1', 'positive-impacts-of-globalisation',
       'Outline two positive impacts of globalisation.',
       'A positive impact of globalisation — any two',
       'Two impacts, 8 marks each, split 5 for the point and 3 for developing it.',
       ref='2021 HL Q12(a)(ii) — positive impacts',
       drop=SCAFFOLD + ('Positive impacts of globalisation',),
       stop='Negative impacts of globalisation',
       notes='The part asks for two positive AND two negative impacts, and the scheme lists them '
             'under a heading each. Carded one per side, which is the rule for parallel accounts, '
             'so a student is not shown fifteen options to pick two from.')

P.menu('positive impacts and two negative', 'econ-2021-hl-q12-a-ii-neg',
       'economics-4-1', 'negative-impacts-of-globalisation',
       'Outline two negative impacts of globalisation.',
       'A negative impact of globalisation — any two',
       'Two impacts, 5 marks each, split 2 for the point and 3 for developing it.',
       ref='2021 HL Q12(a)(ii) — negative impacts', claim=2, per=5,
       drop=SCAFFOLD + ('Positive impacts of globalisation', 'Trade enhances division',
                        'Improvements in economic growth', 'Reduction in numbers living',
                        'Innovation is encouraged', 'Benefits of economies of scale',
                        'Negative impacts of globalisation'))

P.menu('Evaluate two reasons why the Minister for Finance', 'econ-2021-hl-q12-b-i',
       'economics-3-1', 'reasons-for-the-125-corporation-tax-rate',
       'The Minister for Finance reaffirmed Ireland’s commitment to the 12.5% corporation tax '
       'rate. Evaluate two reasons why the Minister made this decision.',
       'A reason for keeping the 12.5% rate — any two',
       'Two reasons, 7 marks each — split 3 for the reason and 4 for developing it, so a named '
       'reason with nothing after it earns less than half.',
       drop=SCAFFOLD)

P.menu('Discuss two implications of this exit', 'econ-2021-hl-q12-c-i',
       'economics-4-2', 'implications-of-brexit-for-ireland',
       'The United Kingdom left the European Union on January 31, 2020. Discuss two implications '
       'of this exit for the Irish economy.',
       'An implication of Brexit for Ireland — any two',
       'Two implications, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD)

P.menu('advantages to Ireland of remaining a member', 'econ-2021-hl-q12-c-ii',
       'economics-4-1', 'advantages-of-eu-membership',
       'Outline two possible advantages to Ireland of remaining a member of the EU.',
       'An advantage of EU membership — any two',
       'Two advantages, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD)

P.menu('potential advantages to Ireland as a country of maintaining', 'econ-2021-hl-q14-a-ii',
       'economics-3-3', 'advantages-of-low-inflation',
       'Outline the potential advantages to Ireland of maintaining the lowest price inflation '
       'rate relative to the Euro Area and the UK over this period.',
       'An advantage of low inflation — any two',
       'Two advantages, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD,
       stem='Set on a chart of Irish, UK and Euro Area inflation from 2014 to 2019, with Ireland '
            'lowest throughout.')

P.menu('disadvantages to Irish citizens of a low inflation', 'econ-2021-hl-q14-b-i',
       'economics-3-3', 'disadvantages-of-low-inflation',
       'Outline two possible disadvantages to Irish citizens of a low inflation rate in Ireland.',
       'A disadvantage of low inflation — any two',
       'Two disadvantages, 7 marks each, split 3 and 4. The paper asks for the downside of LOW '
       'inflation, which is the harder half of the topic.',
       drop=SCAFFOLD)

P.menu('Continued capital investment in the National Broadband Plan', 'econ-2021-hl-q14-c-ii',
       'economics-4-2', 'broadband-and-competitiveness',
       'Discuss the importance of continued capital investment in the National Broadband Plan '
       'for Ireland’s international competitiveness.',
       'A reason broadband investment matters — any two',
       'Two points, 6 marks each, split 3 and 3.',
       drop=SCAFFOLD + ('Ireland’s international competitiv',))

P.menu('Choose two other areas the Irish Government should focus on', 'econ-2021-hl-q14-c-iii',
       'economics-4-2', 'improving-international-competitiveness',
       'Choose two other areas the Irish Government should focus on to become more '
       'internationally competitive. Justify your choice in each case.',
       'An area to focus on — any two',
       'Two areas, 6 marks each, split 3 for the choice and 3 for the justification.',
       drop=SCAFFOLD)

P.menu('negative implications of this reduction in air passenger', 'econ-2021-hl-q15-b-iii',
       'economics-3-2', 'effects-of-falling-air-passenger-numbers',
       'Outline two negative implications of the reduction in air passenger numbers on the Irish '
       'economy.',
       'A negative implication — any two',
       'Two implications, 5 marks each.',
       drop=SCAFFOLD)

P.menu('reasons for the increase in the number of homeless', 'econ-2021-hl-q16-a-i',
       'economics-2-2', 'causes-of-homelessness',
       'Discuss two reasons for the increase in the number of homeless people in Ireland.',
       'A reason homelessness rose — any two',
       'Two reasons, 6 marks each.',
       drop=SCAFFOLD)

P.menu('economic measures, other than social housing', 'econ-2021-hl-q16-a-ii',
       'economics-1-3', 'measures-to-reduce-homelessness',
       'Outline two economic measures, other than social housing, that could be taken by the '
       'Irish government to help reduce the number of homeless people.',
       'A measure other than social housing — any two',
       'Two measures, 6 marks each. Social housing is excluded by the question.',
       drop=SCAFFOLD + ('Irish government to help reduce',))

# ── Elasticity, which is not a menu ─────────────────────────────────────────
BODY = block(tidy(load(2021, 'higher')), 'Question 12 Possible responses Max Mark', occ=0)
P.cards.append(card(
    'econ-2021-hl-q13-c-ii', 2021, 'higher', 'economics-1-4', 'reading-a-ped-figure',
    '2021 HL Q13(c)(ii)',
    'The Price Elasticity of Demand for Apple Airpods was calculated as −1.63. State whether '
    'demand is elastic or inelastic, and give a reason for your answer.',
    '(4 + 4)', 8,
    [point('r-answer', 'Based upon the above calculation Apple Airpods can be said to be Elastic.',
           4, 'The scheme pays this half for the classification alone.'),
     anyN('r-reason', 'The reason — either one', 4, 1, 4,
          [defurnish(x) for x in block(
              BODY, '• The number is greater than 1',
              '(iii) If the firm selling the above product').split('•') if len(x.strip()) > 12],
          'Either reason earns the second half: the size of the number, or what it means about '
          'the two percentage changes.')],
    'The calculation itself (15 marks) is not carded — it is keyed to figures printed on the '
    'paper. What is carded is reading the answer, which is where marks are lost.',
    tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-hl-q13-c-iii', 2021, 'higher', 'economics-1-4', 'elasticity-and-revenue',
    '2021 HL Q13(c)(iii)',
    'If the firm selling this product intends to maximise revenue from its sale, should it '
    'increase, decrease, or maintain the same price? Explain your answer.',
    'fixed', 10,
    [point('r-1',
           'As the price elasticity of demand is elastic the firm should decrease price in order '
           'to increase total revenue. A decrease in price will lead to a more than proportionate '
           'increase in quantity demanded than the percentage decrease in price thereby increasing '
           'total revenue.', 10,
           'One point, and the marks are for the mechanism: elastic demand means the quantity '
           'response outweighs the price cut.')],
    '', tariff_kind='fixed'))

# ── Question 11, recovered ──────────────────────────────────────────────────
# Not an oversight in the authoring: the extractor could not see this question.
# Section B used to begin at the first "Question 1x" heading that repeated the
# response-table caption, and on this paper alone that heading is question 12 —
# so question 11's five pages were in neither section's output and could not be
# carded. econ_parts now begins Section B at the first such heading of any kind.
P.menu('Would you consider this market to be competitive', 'econ-2021-hl-q11-a-ii',
       'economics-2-0', 'reading-a-concentration-ratio',
       'Explain why the global aircraft market in 2018 would be considered highly concentrated.',
       'A reason it is highly concentrated — any one',
       'One reason, 5 marks. The part pays 8: 3 for naming the market highly concentrated and 5 '
       'for the explanation, and it is the explanation that is carded.',
       ref='2021 HL Q11(a)(ii)', claim=1, per=5,
       stem='Boeing and Airbus each held 46% of the global aircraft market in 2018, Embraer 5%, '
            'Others 2% and Bombardier 1%.',
       drop=SCAFFOLD + ('Highly concentrated because',))

P.menu('Would you advise the above firm to engage in price competition', 'econ-2021-hl-q11-b-ii',
       'economics-2-0', 'price-competition-in-oligopoly',
       'A firm in oligopoly is at long-run equilibrium. Would you advise it to engage in price '
       'competition? Give two reasons for your answer.',
       'A reason not to compete on price — any two',
       'Two reasons, 4 marks each. Every response the scheme lists argues against price '
       'competition, so the answer the examiner is marking is "no".',
       ref='2021 HL Q11(b)(ii)', drop=SCAFFOLD)

P.menu('small firms such as Embraer and Bombardier', 'econ-2021-hl-q11-b-iii',
       'economics-2-0', 'small-firms-in-an-oligopoly',
       'Outline two reasons why small firms such as Embraer and Bombardier may survive in a '
       'market dominated by two large firms.',
       'A reason a small firm survives — any two',
       'Two reasons, 4 marks each.',
       ref='2021 HL Q11(b)(iii)', drop=SCAFFOLD)

P.menu('Internal Economies of Scale which could arise for Boeing and Embraer',
       'econ-2021-hl-q11-c-ii', 'economics-1-5', 'internal-economies-of-scale',
       'Outline possible internal economies of scale which could arise for Boeing and Embraer if '
       'a merger between them were to occur.',
       'An internal economy of scale — any three',
       'Three economies, 6 marks each.',
       ref='2021 HL Q11(c)(ii)', drop=SCAFFOLD + ('Possible responses',))


# ── A figure card ───────────────────────────────────────────────────────────
# Not cardable until the figure pipeline reached Economics: the answer IS the
# diagram. The four lines cannot be named from the scheme's word list without
# seeing which curve each numeral points at.
P.cards.append(card(
    'econ-2021-hl-q11-b-i', 2021, 'higher', 'economics-2-0', 'labelling-an-oligopoly-diagram',
    '2021 HL Q11(b)(i)',
    'The diagram shows the long-run equilibrium of a firm in oligopoly at point E, producing Q1 '
    'and selling at P1. Write out in full the label for each of the lines numbered 1 to 4.',
    'fixed', 16,
    [point('r-1', 'Marginal Cost', 4, 'Line 1 — the curve rising steeply to the top right.'),
     point('r-2', 'Average (Total) Cost', 4, 'Line 2 — the U-shaped curve above point E.'),
     point('r-3', 'Demand / Average Revenue', 4, 'Line 3 — the kinked line falling to the right.'),
     point('r-4', 'Marginal Revenue', 4, 'Line 4 — the short line dropping steeply below E.')],
    'Abbreviations are not accepted: the part says to write the labels out in full.',
    tariff_kind='fixed',
    figure_key='economics-2021-HL-paper-p16-i0',
    label_key=[{'letter': '1', 'meaning': 'Marginal Cost', 'askedInThisQuestion': True},
               {'letter': '2', 'meaning': 'Average (Total) Cost', 'askedInThisQuestion': True},
               {'letter': '3', 'meaning': 'Demand / Average Revenue', 'askedInThisQuestion': True},
               {'letter': '4', 'meaning': 'Marginal Revenue', 'askedInThisQuestion': True}]))


# ── Section B, second pass ──────────────────────────────────────────────────
P.menu('European Commission want to remove this power', 'econ-2021-hl-q12-b-ii',
       'economics-4-2', 'why-brussels-wants-tax-harmony',
       'Outline one reason why the European Commission wants to remove the power to set '
       'corporation tax from the Irish government.',
       'A reason the Commission wants it — any one', 'One reason, 7 marks.',
       ref='2021 HL Q12(b)(ii)', claim=1, per=7, drop=SCAFFOLD)

P.menu('Government intervention in this market could address', 'econ-2021-hl-q13-b-ii',
       'economics-2-2', 'fixing-information-failure',
       'Misinformation to consumers by technology retailers is a market failure. Evaluate how '
       'Government intervention in this market could address this market failure.',
       'A form of intervention — any one', 'One point, 6 marks.',
       ref='2021 HL Q13(b)(ii)', claim=1, per=6, drop=SCAFFOLD)

P.menu('one advantage of a government regulation', 'econ-2021-hl-q13-b-iii',
       'economics-1-3', 'advantages-of-regulation',
       'Explain, giving an example, one advantage of a government regulation.',
       'An advantage of regulation — any one',
       'One advantage, 6 marks: the marks split between the point and the example.',
       ref='2021 HL Q13(b)(iii)', claim=1, per=6, drop=SCAFFOLD)

P.menu('method the government could use to address rising inflation', 'econ-2021-hl-q14-b-ii',
       'economics-3-3', 'government-tools-against-inflation',
       'Explain one method the government could use to address rising inflation.',
       'A method against inflation — any one', 'One method, 7 marks.',
       ref='2021 HL Q14(b)(ii)', claim=1, per=7, drop=SCAFFOLD)

P.menu('more accurate indicator of Ireland', 'econ-2021-hl-q15-a',
       'economics-3-0', 'gni-or-gdp-for-welfare',
       'Which measure is a more accurate indicator of Ireland’s economic welfare: gross national '
       'income or gross domestic product? Justify your answer.',
       'A case for one measure — either one',
       'One justification, 7 marks. The scheme sets out the case for each measure; gross national '
       'income is the one that counts income actually accruing to Irish residents.',
       ref='2021 HL Q15(a)', claim=1, per=7, drop=SCAFFOLD)

P.menu('negative multiplier effects of large corporations', 'econ-2021-hl-q15-c-iii',
       'economics-3-0', 'the-multiplier-in-reverse',
       'Discuss two possible negative multiplier effects if a large corporation moved its staff to '
       'remote working.',
       'A negative multiplier effect — any two', 'Two effects, 7 marks each.',
       ref='2021 HL Q15(c)(iii)', claim=2, per=7, drop=SCAFFOLD + ('Possible Responses',))

P.menu('one social reason and one economic reason', 'econ-2021-hl-q16-b-ii-social',
       'economics-2-1', 'social-case-for-the-minimum-wage',
       'Explain one SOCIAL reason why the Irish government has increased the national minimum '
       'wage.',
       'A social reason — any one', 'One reason, 5 marks.',
       ref='2021 HL Q16(b)(ii) — social', claim=1, per=5,
       drop=SCAFFOLD + ('Social reasons:',), stop='Economic reasons:',
       notes='The part asks for one of each and the scheme heads the two lists separately, so '
             'each side is its own card.')

P.menu('one social reason and one economic reason', 'econ-2021-hl-q16-b-ii-economic',
       'economics-2-1', 'economic-case-for-the-minimum-wage',
       'Explain one ECONOMIC reason why the Irish government has increased the national minimum '
       'wage.',
       'An economic reason — any one', 'One reason, 5 marks.',
       ref='2021 HL Q16(b)(ii) — economic', claim=1, per=5,
       drop=SCAFFOLD, after='Economic reasons:')

P.emit()
