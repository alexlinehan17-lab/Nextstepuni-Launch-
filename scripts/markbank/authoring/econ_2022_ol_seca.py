#!/usr/bin/env python3
"""Economics 2022 Ordinary Level — Section A.

Ordinary Section A is mostly parts with one right answer — complete the table,
calculate the elasticity, tick the substitute goods, say what CSO stands for —
and those are not menu cards. Three parts here ask for a response from a list
the examiner wrote out, and those are carded.

This paper writes its descending tariff as "1st x 9 / 2nd x 6" where others
write "1st @ 8", and prints it beside the question rather than the part, so the
tariffs below are read off the scheme by hand rather than taken from the part.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2022, 'ordinary', 'A')
SCAFFOLD = ('Possible responses', 'Suggested responses')

P.menu('use the Irish Government would make of the information collected',
       'econ-2022-ol-sa-q2-ii', 'economics-1-3', 'what-the-census-is-used-for',
       'Explain one use the Irish Government would make of the information collected in the '
       'census.',
       'A use for the census — any one',
       'One use, 6 marks.',
       ref='2022 OL Section A Q2(ii)', claim=1, per=6, drop=SCAFFOLD,
       stem='In April 2022 the CSO conducted a census, an official count of Ireland’s population.')

P.menu('Outline one possible reason for this development', 'econ-2022-ol-sa-q3-i',
       'economics-1-1', 'why-consumers-moved-online',
       'More Irish consumers shopped online during 2020 and 2021. Outline one possible reason '
       'for this development.',
       'A reason consumers moved online — any one',
       'One reason, 9 marks: 6 for the reason and 3 for explaining it.',
       ref='2022 OL Section A Q3(i)', claim=1, per=9, drop=SCAFFOLD)

P.menu('advantages for the Irish economy of increasing the minimum wage', 'econ-2022-ol-sa-q5-a',
       'economics-2-1', 'advantages-of-a-higher-minimum-wage',
       'Outline two advantages for the Irish economy of increasing the minimum wage.',
       'An advantage of a higher minimum wage — any two',
       'Two advantages, the first paid 9 and the second 6.',
       ref='2022 OL Section A Q5(a)', steps=[9, 6], drop=SCAFFOLD,
       stem='The government increased the minimum wage by 30c in Budget 2022.')

P.menu('disadvantage of this development for local retailers',
       'econ-2022-ol-sa-q3-ii', 'economics-2-0', 'how-online-shopping-hurts-local-retailers',
       'Outline one possible disadvantage of the growth in online shopping for local retailers.',
       'A disadvantage — any one', 'One disadvantage, 6 for the point and 3 for developing it.',
       ref='2022 OL Section A Q3(ii)', claim=1, per=6, drop=SCAFFOLD)

P.emit()
