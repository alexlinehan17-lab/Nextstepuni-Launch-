#!/usr/bin/env python3
"""Economics parts deliberately left uncarded, and why.

econ_todo lists every part with responses that no card cites. Some of those are
not gaps: they are decisions, taken with a reason, and recorded until now only
in the prose at the top of the paper scripts. That made the worklist argue for
work that had already been considered and declined — and worse, invited someone
to card a part the deck had deliberately left alone.

Recorded here instead, keyed by the reference the QUESTION PAPER gives.

Deleting a line puts the part back on the worklist, which is the point: a
decision should be as easy to revisit as it was to take.
"""

EXCLUDED = {
    # Answered by reading the figure printed beside the question. The figure
    # pipeline could carry these, but the card would test chart-reading rather
    # than economics.
    '2021 HL Section A Q7(a)':
        'answered by reading the gross-debt-per-person figure printed with it',
    '2022 HL Section A Q2(a)':
        'answered by reading the infographic printed with it',
    '2022 HL Section A Q2(b)':
        'answered by reading the infographic printed with it',
    '2024 HL Section A Q1(a)':
        'the answer is calculated off the infographic printed with it',
    '2021 HL Q14(a)(i)':
        'every response describes the shape of the inflation chart printed with it',
    '2025 HL Q12(a)(i)':
        'every response reads the government-debt chart printed with it',
    '2022 HL Q12(a)(i)':
        'a reading of the HHI figures printed in the chart with it',
    '2022 OL Q15(c)(i)-chart':
        'superseded — carded as econ-2022-ol-q15-c-i',

    # Answered against a choice the student made earlier in the question, so
    # there is no fixed answer for a card to hold.
    '2021 HL Section A Q9(b)':
        "responses are worked to the student's own choice of market structures",

    # The marks are for a diagram. Where such a part also carries a written
    # explanation, that explanation IS carded; these have only the drawing.
    '2023 HL Section A Q4(a)':
        'a table completion — the marks are for filling the table, not for prose',

    # The Student Research Project. Its "responses" are the examiner's grading
    # bands — "Deduct 1m if no quantitative data", "The Research Process 40
    # Marks Excellent Very Good Good Fair Weak" — not answers to a question.
    '2021 HL Q16(c)(iii)':
        'coursework grading bands, not answers to a question',
    '2022 OL Q16(c)(iii)':
        'coursework grading bands, not answers to a question',
    '2022 HL Q16(c)(iii)-srp':
        'coursework grading bands, not answers to a question',

    # The whole answer is a tick placed in a box, or a table to be completed.
    # There is no wording for a card to carry.
    '2022 HL Q14(a)(ii)':
        'answered by ticking fixed or variable against each item in a table',
    '2024 OL Q14(b)(ii)':
        'answered by ticking direct or indirect, with the explanation welded to the tick row',
    '2024 OL Section A Q2(a)':
        'answered by ticking a box in a table',
    '2025 OL Section A Q8(i)':
        'answered by ticking which firm is in a monopoly',
    '2022 OL Q14(a)(i)':
        'a table completion — the marks are for filling the table',
    '2025 OL Q12(b)(i)':
        "the scheme's three answers are welded across two lines, so no half separates",
    '2023 OL Q14(c)(i)':
        'the variable-cost definition is welded onto the fixed-cost examples line',
    '2022 OL Q11(b)(ii)':
        'labels to be placed on a diagram; no wording to show',
    '2023 OL Q11(b)(ii)':
        'labels to be placed on a diagram; no wording to show',
    '2024 OL Q11(b)(ii)':
        'labels to be placed on a diagram; no wording to show',
    '2025 OL Q13(b)(i)':
        'a graph to be drawn; the responses are its axis values',
    '2024 OL Q13(a)(i)':
        'a graph to be drawn; the responses are its axis values',
    '2025 HL Q16(a)(i)':
        'a table completion — the marks are for the figures, not for prose',
    '2025 HL Section A Q9(a)':
        'writing out what numbered items on a diagram stand for; no prose answer',

    # An "explain your answer" beside a diagram, marked for the part as a whole.
    # The scheme does not say how much of the tariff is the drawing, so splitting
    # it over the written steps would be arithmetic rather than the scheme's.
    '2025 OL Q15(b)(ii)':
        'the explanation beside a diagram, with the tariff covering both',
    '2024 OL Q15(b)(ii)':
        'the explanation beside a diagram, with the tariff covering both',
    '2025 HL Section A Q6(b)':
        'the explanation beside a diagram, with the tariff covering both',
    '2022 HL Q15(a)(iii)':
        'the explanation beside a diagram, with the tariff covering both',
    '2023 HL Q16(a)(ii)':
        'the explanation beside a diagram, with the tariff covering both',
    '2025 HL Q11(b)(i)':
        'the explanation beside a diagram, with the tariff covering both',
    '2025 OL Q11(c)(ii)':
        'the scheme heads three areas and answers only the first before the rubric',

    # The scheme DOES split the diagram from the explanation here — "1 mark per
    # label = 9 marks", explanation 8 — but 8 marks over five written steps has
    # no split the scheme states, and choosing one is inventing a tariff.
    '2023 HL Q12(a)(iii)':
        'the explanation is worth 8 over five steps and the scheme states no split',
    '2024 HL Q14(b)(i)':
        'the explanation is marked as a block and the scheme states no split',

    # Calculations: the scheme's response IS the worked arithmetic, so a card
    # would show the answer beside the sum that produces it.
    '2025 HL Section A Q2(a)':
        'the response is the worked calculation of the savings rate',
    '2024 OL Q14(a)(i)': 'the response is the worked percentage calculation',
    '2024 OL Q14(c)(i)': 'the response is the worked balance-of-trade calculation',
    '2024 OL Q15(c)(i)': 'the response is the worked elasticity calculation',
    '2025 HL Q11(a)(i)': 'the response is the worked HHI calculation',
    '2025 HL Q13(a)(i)': 'the response is the worked percentage calculation',
    '2025 HL Q15(b)(i)': 'the response is the worked calculation',
    '2025 HL Q16(a)(ii)': 'the response is the worked calculation',
    '2025 HL Q16(b)(ii)': 'the response is the worked calculation',
    '2024 HL Q11(a)(i)': 'the response is the worked calculation',
    '2024 HL Q11(b)(i)': 'the response is the worked multiplier calculation',
    '2024 HL Q16(b)(ii)': 'the response is the worked elasticity calculation',
    '2024 HL Q16(b)(iii)': 'the response is the worked elasticity calculation',
    '2023 OL Q13(b)(ii)': 'the response is the worked calculation',
    '2021 OL Q13(c)(ii)': 'the responses are figures read out of the CPI table',
    '2023 HL Section A Q10':
        'the responses are the national-accounts workings, not prose',
    '2021 HL Section A Q10(b)':
        'the scheme prints no responses for this part — only the section header',
    '2021 OL Q11(c)(ii)':
        'the scheme gives the definition welded to the cue and only an examples line after',
    '2024 OL Section A Q10':
        'answered by ticking which diagram applies, with the explanation beside it',
    '2025 HL Section A Q7':
        'answered by naming a product from the table and justifying off its YED value',
    '2024 HL Q14(c)(ii)': 'the response is the worked real-interest-rate calculation',
    '2022 OL Section A Q9(i)': 'the response is the worked elasticity calculation',
    '2022 OL Section A Q4':
        'answered by ticking substitute or complementary against each product',
    '2022 HL Q14(c)(iii)':
        'the scheme welds its two sides together and neither separates cleanly',
    '2023 HL Q15(b)(iii)':
        'the yes and no cases are welded onto the cue line and neither separates',
    '2025 HL Q14(b)(i)':
        'a graph to be completed; the responses are its axis and equilibrium labels',

    # Already carded under a reference the worklist cannot match, because the
    # scheme leaves the part unplaced and gives it no question cue to compare.
    '2021 OL Q11(b)(iii)-mnc': 'carded as econ-2021-ol-q11-b-iii',
    '2023 HL Section A Q5(b)-ppf': 'carded as econ-2023-hl-sa-q5-b',
    '2025 OL Section A Q5(ii)-gdp': 'carded as econ-2025-ol-sa-q5-ii',
}


# A part the scheme leaves unplaced has no reference to key on, so these are
# matched on a distinctive phrase from the scheme's own responses instead.
EXCLUDED_TEXT = {
    'Availability of a skilled/English speaking workforce':
        'carded as econ-2021-ol-q11-b-iii, the reasons MNCs locate in Ireland',
    'Efficient refers to a production point':
        'carded as econ-2023-hl-sa-q5-b, the PPF justifications',
    'Higher incomes / living standards':
        'carded as econ-2025-ol-sa-q5-ii, the advantages of a growing GDP',
    'The supply of land is fixed in quantity':
        'the explanation beside a diagram, with the tariff covering both',
    'Specialisation/division of labour':
        'the two halves of a long-run average cost curve, marked as one part with '
        'the diagram',
    'As the cost of fertiliser has risen':
        'the explanation beside a diagram, with the tariff covering both',
    'Commits to environmental sustainability / cost reduction':
        'carded as econ-2025-hl-q15-a-iii-aib',
    'The increase in population will lead to an increase in demand for housing':
        'the explanation beside a diagram, with the tariff covering both',
    'Demand curve shifts to the right (D1)':
        'labels to be placed on a diagram; no wording to show',
    'Effect on price Through imposing a minimum price':
        'the explanation beside a diagram, marked 10 for the drawing and 5 for the '
        'writing, with no split stated across the three effects',
    'They sell the output at price P1':
        'the explanation beside a monopoly diagram, marked 1 per label with the '
        'explanation as a block',
}


def is_excluded(ref, question=''):
    if ref in EXCLUDED:
        return EXCLUDED[ref]
    for phrase, why in EXCLUDED_TEXT.items():
        if phrase in (question or ''):
            return why
    return None
