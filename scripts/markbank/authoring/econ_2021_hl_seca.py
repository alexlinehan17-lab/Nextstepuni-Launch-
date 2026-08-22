#!/usr/bin/env python3
"""Economics 2021 Higher Level — Section A.

Section A is 75 of this paper's 300 marks and reads, on a first skim, like
chart lookups. Most of it is not: "Outline two reasons why achieving a trade
surplus is an objective of the Irish government" is answered by a list of named
responses and needs no chart at all.

What is deliberately not carded, and why:

  * a part answered by reading the figure printed with it — "compare the level
    of gross debt per person from 2007 to 2019". The figure pipeline could
    carry those, but the card would then test chart-reading, not economics.
  * a part whose responses are worked to the student's own earlier choice —
    "give one reason for each of your chosen market structures above".

Every reference here is the one the QUESTION PAPER gives, not the one the
scheme's running order implies; econ_refcheck.py derives it again and compares.
The two disagree more often than they look like they should — the scheme prints
question 3's first part on the page it heads question 2.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2021, 'higher', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('reasons why achieving a trade surplus is an objective', 'econ-2021-hl-sa-q1-b',
       'economics-4-2', 'why-a-trade-surplus-is-an-aim',
       'Outline two reasons why achieving a trade surplus is an objective of the Irish government.',
       'A reason a trade surplus is an aim — both of these',
       'Two reasons, 4 marks each, and the scheme lists exactly two.',
       ref='2021 HL Section A Q1(b)', drop=SCAFFOLD)

P.menu('willing to pay different prices for a Netflix subscription', 'econ-2021-hl-sa-q3-a',
       'economics-1-1', 'why-consumers-accept-different-prices',
       'Outline one reason why consumers are willing to pay different prices for the same '
       'Netflix subscription in different countries.',
       'A reason consumers accept the difference — any one',
       'One reason, 5 marks: 2 for naming it and 3 for explaining it.',
       ref='2021 HL Section A Q3(a)', claim=1, per=5, drop=SCAFFOLD,
       stem='A basic Netflix account cost far more per month in Switzerland than in Rwanda.')

P.menu('other conditions necessary for price discrimination', 'econ-2021-hl-sa-q3-b',
       'economics-1-1', 'conditions-for-price-discrimination-hl',
       'Explain two conditions, other than the willingness of consumers to pay, that are '
       'necessary for price discrimination to occur.',
       'A condition for price discrimination — both of these',
       'Two conditions, 5 marks each.',
       ref='2021 HL Section A Q3(b)', drop=SCAFFOLD)

P.menu('other duties of the Central Bank', 'econ-2021-hl-sa-q5-b',
       'economics-3-4', 'duties-of-the-central-bank',
       'Other than the regulation of commercial banks, outline two other duties of the Central '
       'Bank of Ireland.',
       'A duty of the Central Bank — any two',
       'Two duties, 4 marks each. Regulating the commercial banks is excluded by the question.',
       ref='2021 HL Section A Q5(b)', drop=SCAFFOLD)

P.menu('advise the governments of these countries on one policy', 'econ-2021-hl-sa-q6-b',
       'economics-4-0', 'policies-to-raise-a-countrys-hdi',
       'Advise the governments of the countries lowest on the Human Development Index on one '
       'policy they could use to improve their HDI ranking.',
       'A policy that would raise HDI — any one',
       'One policy, 8 marks: 4 for the policy and 4 for explaining how it raises the ranking.',
       ref='2021 HL Section A Q6(b)', claim=1, per=8, drop=SCAFFOLD,
       stem='Chad, the Central African Republic and Niger ranked 187th, 188th and 189th on the '
            'HDI in 2020.')

P.menu('Advise the Irish government on how it could assist', 'econ-2021-hl-sa-q6-c',
       'economics-4-0', 'how-a-rich-country-can-assist-ldcs',
       'Advise the Irish government on how it could assist the countries lowest on the Human '
       'Development Index to improve their HDI ranking.',
       'A way Ireland could assist — any one',
       'One way, 8 marks: 4 for the measure and 4 for explaining it. The paper offers this part '
       'or the one before it, not both.',
       ref='2021 HL Section A Q6(c)', claim=1, per=8, drop=SCAFFOLD)

P.menu('economic disadvantages for a government in achieving a budget surplus',
       'econ-2021-hl-sa-q7-b', 'economics-3-1', 'disadvantages-of-a-budget-surplus',
       'Explain the economic disadvantages for a government in achieving a budget surplus.',
       'A disadvantage of a budget surplus — any two',
       'Two disadvantages, 3 marks each.',
       ref='2021 HL Section A Q7(b)', drop=SCAFFOLD)

P.emit()
