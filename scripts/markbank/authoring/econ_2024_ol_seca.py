#!/usr/bin/env python3
"""Economics 2024 Ordinary Level — Section A.

100 marks over ten questions of twelve, eight of which are answered, with a
mark added for each of the first four answered correctly.

Not carded: the true/false and tick-the-box parts (Q2(a), Q3(a), Q5, Q7 — the
answer is a tick, and where a reason is printed the table columns interleave it
line-by-line so no contiguous slice holds it), Q8's read-the-Gini-chart boxes,
and question 10, whose responses the extractor could not separate from the
Section B header printed directly beneath them.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402
from econ_lib import anyN, as_option, block, bullets, card, load, point, tidy  # noqa: E402

P = Paper(2024, 'ordinary', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('one reason why our oceans and seas are a valuable economic resource',
       'econ-2024-ol-sa-q1-i', 'economics-0-2', 'oceans-as-an-economic-resource',
       'Explain one reason why our oceans and seas are a valuable economic resource.',
       'A reason the oceans are valuable — any one',
       'One reason, 8 marks.',
       ref='2024 OL Section A Q1(i)', claim=1, per=8, drop=SCAFFOLD,
       stem='UN Sustainable Development Goal 14 is to conserve and sustainably use the oceans, '
            'seas and marine resources.')

P.menu('one way individuals can help protect this valuable resource', 'econ-2024-ol-sa-q1-ii',
       'economics-0-2', 'protecting-the-marine-environment',
       'Outline one way individuals can help protect the oceans and seas.',
       'A way an individual can help — any one',
       'One way, 4 marks.',
       ref='2024 OL Section A Q1(ii)', claim=1, per=4, drop=SCAFFOLD)

P.menu('Competitive advertising promotes the advantages of one firm', 'econ-2024-ol-sa-q3-b',
       'economics-2-0', 'when-advertising-does-not-help-consumers',
       'Competitive advertising promotes the advantages of one firm’s product over that of its '
       'competitors. Outline two reasons why competitive advertising may not always benefit the '
       'consumer.',
       'A reason advertising may not benefit the consumer — any two',
       'Two reasons, the first paid 8 and the second 4.',
       ref='2024 OL Section A Q3(b)', steps=[8, 4], drop=SCAFFOLD)

P.menu('do not contribute to a rainy', 'econ-2024-ol-sa-q4-a',
       'economics-1-1', 'why-households-are-not-saving',
       'Explain one reason why these families may not be saving.',
       'A reason a family is not saving — any one',
       'One reason, 12 marks.',
       ref='2024 OL Section A Q4(a)', claim=1, per=12, drop=SCAFFOLD,
       stem='47% of Irish families with young children do not contribute to a rainy-day savings '
            'fund.')

P.menu('measure financial institutions in Ireland could take to encourage citizens',
       'econ-2024-ol-sa-q4-b', 'economics-3-4', 'encouraging-households-to-save',
       'Outline one measure financial institutions in Ireland could take to encourage citizens '
       'in Ireland to save.',
       'A measure a bank could take — any one',
       'One measure, 12 marks.',
       ref='2024 OL Section A Q4(b)', claim=1, per=12, drop=SCAFFOLD)

P.menu('Deposit Return Scheme was introduced', 'econ-2024-ol-sa-q6',
       'economics-0-2', 'effects-of-the-deposit-return-scheme',
       'Outline two effects the Deposit Return Scheme may have on Irish consumers.',
       'An effect on consumers — any two',
       'Two effects, the first paid 8 and the second 4.',
       ref='2024 OL Section A Q6', steps=[8, 4], drop=SCAFFOLD,
       stem='Under the Deposit Return Scheme, introduced on 1 February 2024, a consumer pays a '
            'deposit on a drink container and gets it back when the container is returned.')

# Q2(b) prints no tariff cell of its own inside its segment — the ⟨12⟩ lands at
# the tail of Q2(a)'s segment in the flattened text — so econ_parts drops the
# part entirely and P.find cannot reach it. Built by hand from the same slices.
# The bare ⟨12⟩ is the same shape as Q4(a) and Q4(b) above: one explained
# answer, 12 marks.
T = tidy(load(2024, 'ordinary'))
P.cards.append(card(
    'econ-2024-ol-sa-q2-b', 2024, 'ordinary', 'economics-1-1',
    'benefits-of-discount-coupons',
    '2024 OL Section A Q2(b)',
    'Explain how Lidl’s customers can benefit from the discount coupons (special offers) '
    'being offered to customers who download the Lidl Plus app.',
    '1 @ 12', 12,
    [anyN('r-1', 'A way customers benefit — any one', 12, 1, 12,
          bullets(block(T, 'Savings on purchases', '3. (a) Coffee shops')),
          'One explained benefit, 12 marks.')],
    '', stem='Lidl now offer discount coupons (special offers) to customers who download the '
             'Lidl Plus app.',
    section='A', tariff_kind='bestNofParts'))

# Q9 is a fill-in-the-blanks table — "G ___ Domestic P___" and "G ___ N ___
# Income" — and the scheme pays the four blanks in paper order: 1st @ 4,
# 2nd @ 4, 3rd @ 2, 4th @ 2. That is the same ordinal-steps-to-printed-order
# mapping the Q1 cards above already ride ((i) @ 8, (ii) @ 4), so GDP's two
# blanks make 8 and GNI's two make 4. econ_parts cannot see the part — its
# responses are two bare noun phrases, not a bullet list — so it is built by
# hand from the same slices.
P.cards.append(card(
    'econ-2024-ol-sa-q9', 2024, 'ordinary', 'economics-3-0', 'gdp-and-gni',
    '2024 OL Section A Q9',
    'Complete the following table to show what each of the abbreviations stand for: '
    'G___ Domestic P___ and G___ N___ Income.',
    '1 @ 4+1 @ 4+1 @ 2+1 @ 2', 12,
    [point('r-gdp', as_option(block(T, 'Gross Domestic Product', 'Gross National Income')), 8,
           'The paper prints G___ Domestic P___ — the two blanks are Gross and Product, '
           'the first and second answered, paid 4 each.'),
     point('r-gni', as_option(block(T, 'Gross National Income', '10. Matcha')), 4,
           'The paper prints G___ N___ Income — the two blanks are Gross and National, '
           'the third and fourth answered, paid 2 each.')],
    'The scheme pays the four blanks in paper order: 1st @ 4, 2nd @ 4, 3rd @ 2, 4th @ 2.',
    stem='The Department of Finance gave two different estimates of Ireland’s economic '
         'growth for 2023: Real GDP 4.7% and Real GNI 0.4%.',
    section='A', tariff_kind='fixed'))

P.emit()
