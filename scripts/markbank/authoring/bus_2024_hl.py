#!/usr/bin/env python3
"""Business 2024 Higher Level — the Applied Business Question.

Higher Level splits its scheme in two: a tariff table at the front carrying the
question and its marks, and support notes at the back carrying the answer. Only
the notes can be carded from, and bus_parts reads both and merges them.

The scheme sets each answer as a name, an explanation of it, and then quotes
from the ABQ text that a candidate is expected to link to. The quotes belong to
that year's case study rather than to the theory, so the rows here are the name
and the explanation; the note says the link is required as well.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2024, 'hl')

A.card(2, 0, 'a', topic='business-0-12', concept='entrepreneurial-characteristics',
       words=21, use=[[1, 2, 3, 4], [11, 12, 13], [19, 20, 21]], marks=[10, 5, 5],
       notation='10m (4 + 3 + 3), then 5m (2 + 2 + 1) each', shared_tariff=True,
       notes='Each characteristic is paid for naming it, explaining it, and quoting the '
             'ABQ text that shows it. The quotes are specific to this case study, so the '
             'rows here are the name and the explanation.')

A.card(2, 0, 'c', topic='business-3-17', concept='management-skills',
       words=23, use=[[1, 2, 3, 4, 5], [24, 25, 26, 27, 28], [53, 54, 55, 56, 57, 58]],
       marks=[10, 10, 10], notation='3 × 10m (4 + 3 + 2 + 1)',
       notes='The three skills the scheme sets out, each paid for naming it, explaining '
             'it, quoting the text that shows it and evaluating it. The quotes and the '
             'evaluation are specific to this case study.')

A.emit()
