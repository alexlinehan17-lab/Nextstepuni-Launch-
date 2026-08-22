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
}


def is_excluded(ref):
    return ref in EXCLUDED
