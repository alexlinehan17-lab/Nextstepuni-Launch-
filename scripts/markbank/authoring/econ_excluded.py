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
}


def is_excluded(ref):
    return ref in EXCLUDED
