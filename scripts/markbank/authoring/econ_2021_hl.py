#!/usr/bin/env python3
"""Economics 2021 Higher Level — Section B.

Same rules as econ_2024_hl.py. This paper runs its responses together under bold
headings with no bullet, so it splits with `heads()`, and it writes the split of
each answer's own marks as a second cell — `⟨2 @ 7⟩ ⟨(3 + 4)⟩` means two answers
at 7, each of which is 3 for the point and 4 for developing it. That inner split
is between parts of ONE answer, not between the two answers, so it does not make
a descending tariff.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_lib import anyN, block, card, defurnish, emit, heads, load, point, tidy  # noqa: E402

YEAR, LEVEL = 2021, 'higher'
T = tidy(load(YEAR, LEVEL))
BODY = block(T, 'Question 12 Possible responses Max Mark', occ=0)


def menu(cid, topic, concept, ref, qtext, notation, total, verbatim, claim, per,
         start, end, headings, note, notes='', steps=None, stem=''):
    chunk = block(BODY, start, end)
    return card(cid, YEAR, LEVEL, topic, concept, ref, qtext, notation, total,
                [anyN('r-1', verbatim, None if steps else total, claim, per,
                      [defurnish(h) for h in heads(chunk, headings)], note, steps=steps)],
                notes, stem=stem,
                tariff_kind='fixed' if steps else 'bestNofParts')


cards = [
    menu('econ-2021-hl-q12-b-i', 'economics-3-1', 'reasons-for-the-125-corporation-tax-rate',
         '2021 HL Q12(b)(i)',
         'The Minister for Finance reaffirmed Ireland’s commitment to the 12.5% corporation tax '
         'rate. Evaluate two reasons why the Minister for Finance made this decision.',
         '2 @ 7', 14, 'A reason for keeping the 12.5% rate — any two', 2, 7,
         'Incentivise FDI / discourage any exodus of MNCs',
         '(b) The Irish government has repeatedly rejected calls',
         ['Incentivise FDI / discourage any exodus of MNCs', 'Maintain employment levels',
          'Government revenue', 'Maintain economic growth', 'Loss of fiscal sovereignty'],
         'Two reasons, 7 marks each — the scheme splits each into 3 for the reason and 4 for '
         'developing it, so a named reason with nothing after it earns less than half.'),

    menu('econ-2021-hl-q12-c-i', 'economics-4-2', 'implications-of-brexit-for-ireland',
         '2021 HL Q12(c)(i)',
         'The United Kingdom left the European Union on January 31, 2020. Discuss two '
         'implications of this exit for the Irish economy.',
         '2 @ 6', 12, 'An implication of Brexit for Ireland — any two', 2, 6,
         'Possible negative effect on Irish exports',
         '(ii) Outline two possible advantages to Ireland of remaining a member of the EU',
         ['Possible negative effect on Irish exports',
          'Effects on agricultural sector / agri-food sectors', 'Labour market effects',
          'Imports from the UK'],
         'Two implications, 6 marks each, split 3 for the point and 3 for developing it.'),

    menu('econ-2021-hl-q12-c-ii', 'economics-4-1', 'advantages-of-eu-membership',
         '2021 HL Q12(c)(ii)',
         'Outline two possible advantages to Ireland of remaining a member of the EU.',
         '2 @ 6', 12, 'An advantage of EU membership — any two', 2, 6,
         'Free Trade Area / larger market / trade expansion', 'Question 13',
         ['Free Trade Area / larger market / trade expansion',
          'Access to capital / research funding', 'Freedom movement of capital / labour',
          'Foreign Direct Investment / job creation'],
         'Two advantages, 6 marks each, split 3 for the point and 3 for developing it.'),
]

# ── Question 14 — inflation and competitiveness ─────────────────────────────
cards.append(menu(
    'econ-2021-hl-q14-a-ii', 'economics-3-3', 'advantages-of-low-inflation', '2021 HL Q14(a)(ii)',
    'Outline the potential advantages to Ireland as a country of maintaining the lowest price '
    'inflation rate relative to the Euro Area and the UK over this period.',
    '2 @ 6', 12, 'An advantage of low inflation — any two', 2, 6,
    'More competitive exports As Irish prices will be lower',
    '(b) (i) Outline two possible disadvantages to Irish citizens',
    ['More competitive exports', 'Competitive costs',
     'Domestic spending / savings / wage restraint / reduced demand for imports',
     'Government finances'],
    'Two advantages, 6 marks each, split 3 for the point and 3 for developing it.',
    stem='Set on a chart of Irish, UK and Euro Area inflation from 2014 to 2019, with Ireland '
         'lowest throughout.'))

cards.append(menu(
    'econ-2021-hl-q14-b-i', 'economics-3-3', 'disadvantages-of-low-inflation', '2021 HL Q14(b)(i)',
    'Outline two possible disadvantages to Irish citizens of a low inflation rate in Ireland.',
    '2 @ 7', 14, 'A disadvantage of low inflation — any two', 2, 7,
    'Consumers may postpone spending', '(ii) Explain one method the government could use',
    ['Consumers may postpone spending', 'No / low wage increases',
     'Debt burden effect (mortgage debt and state debt)', 'Asset appreciation rate may fall'],
    'Two disadvantages, 7 marks each, split 3 for the point and 4 for developing it. The paper '
    'asks for the downside of LOW inflation, which is the harder half of the topic.'))

cards.append(menu(
    'econ-2021-hl-q14-c-ii', 'economics-4-2', 'broadband-and-competitiveness', '2021 HL Q14(c)(ii)',
    'Discuss the importance of continued capital investment in the National Broadband Plan for '
    'Ireland’s international competitiveness.',
    '2 @ 6', 12, 'A reason broadband investment matters — any two', 2, 6,
    'Ability to attract FDI Companies who may wish to locate',
    '(iii) Choose two other areas the Irish Government should focus on',
    ['Ability to attract FDI', 'More flexible working arrangements',
     'Allow state provide services more efficiently', 'Reduce costs of running business'],
    'Two points, 6 marks each, split 3 and 3.'))

cards.append(menu(
    'econ-2021-hl-q14-c-iii', 'economics-4-2', 'improving-international-competitiveness',
    '2021 HL Q14(c)(iii)',
    'Choose two other areas the Irish Government should focus on to become more internationally '
    'competitive. Justify your choice in each case.',
    '2 @ 6', 12, 'An area to focus on — any two', 2, 6,
    'Fund skills, education and training programmes', 'Question 15',
    ['Fund skills, education and training programmes', 'Improve the infrastructure for business',
     'Manage the current housing shortage', 'Supporting Enterpris'],
    'Two areas, 6 marks each, split 3 for the choice and 3 for the justification.'))

# The corpus's only cards on elasticity as a decision rule rather than as a
# calculation, which is what the topic is actually for.
cards.append(card(
    'econ-2021-hl-q13-c-ii', YEAR, LEVEL, 'economics-1-4', 'reading-a-ped-figure',
    '2021 HL Q13(c)(ii)',
    'The Price Elasticity of Demand for Apple Airpods was calculated as −1.63. State whether '
    'demand is elastic or inelastic, and give a reason for your answer.',
    '(4 + 4)', 8,
    [point('r-answer', 'Based upon the above calculation Apple Airpods can be said to be Elastic.',
           4, 'The scheme pays this half for the classification alone.'),
     anyN('r-reason', 'The reason — either one', 4, 1, 4,
          [defurnish(x) for x in block(
              BODY, '• The number is greater than 1',
              '(iii) If the firm selling the above product').split('•')
           if len(x.strip()) > 12],
          'Either reason earns the second half: the size of the number, or what it means about '
          'the two percentage changes.')],
    'The calculation itself (15 marks) is not carded — it is keyed to figures printed on the '
    'paper. What is carded is reading the answer, which is the part students lose marks on.',
    tariff_kind='fixed'))

cards.append(card(
    'econ-2021-hl-q13-c-iii', YEAR, LEVEL, 'economics-1-4', 'elasticity-and-revenue',
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

emit(cards)
