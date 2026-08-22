#!/usr/bin/env python3
"""Economics 2021 Ordinary Level — Section A.

Ordinary Section A is not the same kind of thing as Higher Section A. Where the
Higher paper asks for two reasons from a list of five, the Ordinary paper asks
the student to complete a table, calculate an elasticity, name two countries
from a chart, or define a term — parts with one right answer rather than a
choice from the examiner's list, and nothing for a menu card to be built from.
One part of this paper's Section A is a menu, and it is here.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from econ_auto import Paper  # noqa: E402

P = Paper(2021, 'ordinary', 'A')

P.menu('one reason why different wages are paid for different jobs', 'econ-2021-ol-sa-q10-b',
       'economics-2-1', 'why-wages-differ-between-jobs',
       'Explain one reason why different wages are paid for different jobs.',
       'A reason wages differ — any one',
       'One reason, 15 marks: 9 for the reason and 6 for explaining it.',
       ref='2021 OL Section A Q10(b)', claim=1, per=15,
       drop=('Possible responses', 'Suggested responses'))

P.menu('term invisible export', 'econ-2021-ol-sa-q6-b',
       'economics-4-2', 'what-an-invisible-export-is',
       'Explain what is meant by the term invisible export. Give an example.',
       'The explanation and an example — both of these',
       'Explanation and example, 9 marks for the part.',
       ref='2021 OL Section A Q6(b)', claim=2, per=5, drop=('Possible responses', 'Suggested responses'))

P.menu('environmentally sustainable choices', 'econ-2021-ol-sa-q9-b',
       'economics-0-2', 'sustainable-choices-an-individual-can-make',
       'Explain, using two relevant examples, how an individual can make more '
       'environmentally sustainable choices.',
       'A sustainable choice — any two', 'Two examples, 9 marks for the part.',
       ref='2021 OL Section A Q9(b)', claim=2, per=5, drop=('Possible responses', 'Suggested responses'))

P.emit()
