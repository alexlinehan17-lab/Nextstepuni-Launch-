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
from econ_lib import anyN, as_option, block, card, load, point, tidy  # noqa: E402

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


# ── Second pass: the parts with one printed answer ──────────────────────────
# Sliced from the scheme with block(), because these are not menus econ_parts
# can split: a slash-separated list of examples, a name plus its definition, and
# paired definitions whose mark cells interrupt the question.
BODY = tidy(load(2021, 'ordinary'))


def sl(start, end=None, occ=None):
    """One marking point, sliced from the scheme and cleaned of furniture."""
    return as_option(block(BODY, start, end, occ))


P.cards.append(card(
    'econ-2021-ol-sa-q1-ii', 2021, 'ordinary', 'economics-3-1',
    'social-protection-spending-examples',
    '2021 OL Section A Q1(ii)',
    'Give two examples of government expenditure on Social Protection.',
    '1 @ 2+1 @ 1', 3,
    [anyN('r-1', 'An example of Social Protection spending — any two', None, 2, 2,
          [n.strip() for n in
           sl('Unemployment Benefit / Income Supports', '2 Study the statements').split('/')
           if n.strip()],
          'Two examples: the first paid 2 and the second 1.', steps=[2, 1])],
    'The scheme prints its accepted examples as one slash-separated run; split here on the '
    'scheme’s own separators so each is offered on its own.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-sa-q5', 2021, 'ordinary', 'economics-1-1', 'substitute-goods',
    '2021 OL Section A Q5',
    'Sony released The Playstation 5 (PS5) in 2020. Name a substitute good for this item and '
    'explain your answer.',
    'fixed', 15,
    [point('r-name', sl('Microsoft Xbox', 'Goods that satisfy'), 9,
           'Naming any valid substitute earns the 9; the scheme names the Xbox and the Switch.'),
     point('r-expl', sl('Goods that satisfy the same needs', '6 Answer (a) or (b)'), 6,
           'Any one of the three wordings — goods that satisfy the same needs, or that can be '
           'used in place of one another — earns the 6.')],
    '', section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-sa-q9-a', 2021, 'ordinary', 'economics-0-2',
    'three-pillars-of-sustainability',
    '2021 OL Section A Q9(a)',
    'Name the 3 pillars of sustainability.',
    'fixed', 15,
    [point('r-1', 'Social', 9, 'The first pillar named is paid 9.'),
     point('r-2', 'Economic', 3, 'The second, 3.'),
     point('r-3', 'Environmental', 3, 'The third, 3.')],
    'The scheme pays ⟨1 @ 9⟩ ⟨2 @ 3⟩: the first pillar 9 and the other two 3 each, in any '
    'order.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-sa-q10-a', 2021, 'ordinary', 'economics-2-1',
    'public-and-private-sector-workers',
    '2021 OL Section A Q10(a)',
    'CSO data shows that public sector workers earn, on average, more than private sector '
    'workers. Explain the terms in bold outlined above.',
    'fixed', 15,
    [point('r-public', sl('People who are employed and paid', 'Private Sector Workers'), 9,
           'Public sector workers.'),
     point('r-private', sl('People who are employed by private individuals',
                           'OR (b) Explain one reason'), 6,
           'Private sector workers.')],
    'The first term explained is paid 9 and the second 6.',
    section='A', tariff_kind='fixed'))

P.emit()
