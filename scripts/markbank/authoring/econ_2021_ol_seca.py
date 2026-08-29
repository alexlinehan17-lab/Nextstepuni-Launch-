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

P.cards.append(card(
    'econ-2021-ol-sa-q8', 2021, 'ordinary', 'economics-1-1', 'demand-shift-tourism-fall',
    '2021 OL Section A Q8',
    'It is predicted that tourism in Ireland could drop by up to 80% in Summer 2021. '
    'Illustrate the impact the above statement could have on the demand curve for '
    'coaches/car hire in Ireland using the diagram below. Explain your answer.',
    'fixed', 15,
    [point('r-shift', sl('Demand shift to left', ' Price'), 9,
           'The drawing: the demand curve shifted to the left of D (D1 to D2).'),
     point('r-explain', sl('With reduced tourists visiting Ireland',
                           ' 9 Answer either'), 6,
           'The explanation, 6 marks: 3 + 3.')],
    'The scheme pays 9 for the shifted curve drawn on the diagram and 6 (3 + 3) for the '
    'explanation.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-OL-paper-p07-art'))

# ── Worked calculations the scheme prints in full ──────────────────────
# Ordinary Section A prints no per-part marks, so every tariff here is attributed
# by COORDINATE in the scheme rather than by the order the extractor emits: a
# mark cell sits in the right margin on the same row as the line it prices. Read
# that way, each of these questions sums to 15, which is what the paper pays for
# a Section A question — the check that the attribution is right.

P.cards.append(card(
    'econ-2021-ol-sa-q1-i', 2021, 'ordinary', 'economics-3-1',
    'education-as-a-percentage-of-government-spending', '2021 OL Section A Q1(i)',
    'The estimated government expenditure for all departments is €89.6 billion. Calculate '
    'the estimated expenditure on Education as a percentage of total government expenditure '
    'for 2021. Show your workings.',
    '3 @ 4', 12,
    [point('r-1', sl('8.9/ 89.6 x 100 = 9.93%', '(ii) Give two examples'), 12,
           'Three steps at four marks each: the Education figure over the total, times 100, '
           'and the result. The 8.9 is not in the wording — it is read off the chart.')],
    'Nothing in the question gives you 8.9; it comes off the Education bar. Students who work '
    'from the wording alone have no numerator.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-OL-paper-p03-i0'))

P.cards.append(card(
    'econ-2021-ol-sa-q3-i', 2021, 'ordinary', 'economics-1-4',
    'price-elasticity-of-demand-for-kerosene', '2021 OL Section A Q3(i)',
    'Using the formula supplied, calculate the consumers price elasticity of demand when the '
    'price of Kerosene (home fuel heating oil) changes due to an increase in carbon tax.',
    'fixed', 15,
    [point('r-1', sl('Changes -250 litres +50', '⟨6 @ 2⟩'), 12,
           'Six figures at two marks each — the two quantities, the two prices and the two '
           'changes. The Changes row is worked first: quantity falls 250, price rises 50.'),
     point('r-2', sl('+50 𝑥 800 + 850 1000 + 750', 'Answer: - 4.71'), 2,
           'The substitution itself. PED is the change in quantity over the change in price, '
           'times the SUM of the prices over the SUM of the quantities — the midpoint form '
           'the paper supplies, not the simple percentage form.'),
     point('r-3', sl('Answer: - 4.71', '(ii) Indicate if the demand'), 1,
           'One mark for the figure. It is negative because quantity and price moved in '
           'opposite directions, and the sign is part of the answer.')],
    'The scheme prints this as stacked fractions, which is why the working rides with the card '
    'as a picture. Flattened into a line of text the numerator and denominator run together and '
    'the calculation stops being readable.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-OL-scheme-p05-q3i-working'))

P.cards.append(card(
    'econ-2021-ol-sa-q7', 2021, 'ordinary', 'economics-3-1',
    'working-out-a-budget-surplus-or-deficit', '2021 OL Section A Q7',
    'Using the following figures, calculate the expected budgetary position for Ireland in '
    '2022. Indicate if it is a surplus or a deficit. Total income: €87.5 billion Total '
    'expenditure: €86.1 billion',
    '5 @ 3', 15,
    [point('r-1', sl('Total Income (€87.5 bn) - Total Expenditure', '5 | P a g e'), 15,
           'Five steps at three marks each, and the verdict is one of them: the arithmetic '
           'alone does not answer the question, which asks whether it is a surplus or a '
           'deficit.')],
    'Income above expenditure is a SURPLUS. The word is worth marks on its own, so a correct '
    '€1.4bn with no verdict is an incomplete answer.',
    section='A', tariff_kind='fixed'))

P.cards.append(card(
    'econ-2021-ol-sa-q4', 2021, 'ordinary', 'economics-1-1',
    'completing-a-marginal-utility-table-and-finding-the-turn', '2021 OL Section A Q4',
    'Complete the blank spaces below and answer the question that follows. Show your workings. '
    'Based on the table above: At what point does the point of diminishing marginal utility set '
    'in?',
    'fixed', 15,
    [point('r-1', sl('38 \u2013 25 = 13', 'Based on the table above'), 12,
           'Six figures at two marks each. Marginal utility is the DIFFERENCE between one total '
           'and the one before it, so each blank is a subtraction down the total utility row.'),
     point('r-2', sl('After 2nd is consumed or before 3rd is consumed', '5 Sony released'), 3,
           'Diminishing marginal utility sets in where the marginal figures start to FALL '
           '\u2014 15 down to 13 \u2014 not where total utility falls. Total utility is still '
           'rising throughout this table.')],
    'Total utility rises all the way to 47, so a student watching the wrong row sees no turning '
    'point at all. The turn is in the marginal row, and it happens while the total is still '
    'climbing.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-OL-scheme-p05-q4-working'))

P.cards.append(card(
    'econ-2021-ol-sa-q2', 2021, 'ordinary', 'economics-0-0',
    'positive-or-normative-statement', '2021 OL Section A Q2',
    'Study the statements below and indicate by placing a tick (\u221a) in the correct box '
    'which is a positive statement and which is a normative statement.',
    'fixed', 15,
    [point('r-1', sl('Statement Positive Normative 1. In 2022 exports in Ireland will grow',
                     '3 | P a g e'), 15,
           'Two statements, the first worth 9 and the second 6. A POSITIVE statement is a factual '
           'claim that could be checked; a NORMATIVE one is a judgement about what should be '
           'done.')],
    'A forecast is POSITIVE \u2014 it can be checked once 2022 has happened. The second '
    'statement claims a policy will produce a good outcome, which is a value judgement. The '
    'answer is which column the tick sits in, and extraction loses the column, so the completed '
    'table rides with the card as a picture.',
    section='A', tariff_kind='fixed',
    figure_key='economics-2021-OL-scheme-p04-q2-ticks'))

P.emit()
