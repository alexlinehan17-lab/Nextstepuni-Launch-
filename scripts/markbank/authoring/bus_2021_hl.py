#!/usr/bin/env python3
"""Business 2021 Higher Level — the Applied Business Question on planning.

The scheme lists five kinds of plan and pays four of them, 8 + 8 + 7 + 7. Under
each it quotes the ABQ text a candidate is expected to link to; those quotes
belong to that year's case study rather than to the theory, so the rows here are
the kind of plan and what it is.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2021, 'hl')

A.card(2, 0, 'a', topic='business-3-16', concept='types-of-business-plan',
       extend=1, use=[[1, 2, 3, 4], [8, 9, 10, 11], [16, 17, 18], [22, 23, 24]],
       marks=[8, 8, 7, 7], notation='8 + 8 + 7 + 7',
       notes='The scheme lists a fifth, the mission statement, and pays four. Each is '
             'worth naming, explaining, and quoting the text that shows it.')

A.card(2, 0, 'b', 'i', topic='business-6-13', concept='types-of-business-insurance',
       extend=1, use=[[1, 2, 3, 4], [8, 9, 10, 11], [16, 17, 18, 19, 20]],
       marks=[6, 6, 6], notation='3 × 6m (2 + 2 + 2)',
       notes='Each type is paid for naming it, explaining it, and quoting the text that '
             'shows the risk. The scheme lists motor insurance as a fourth.')

A.emit()
