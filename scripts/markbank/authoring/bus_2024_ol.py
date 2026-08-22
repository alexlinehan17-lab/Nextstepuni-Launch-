#!/usr/bin/env python3
"""Business 2024 Ordinary Level — Section 2 Question 9.

The scheme splits these fifteen as 7 + 3 for the first point and 4 + 1 for the
second, so the two rows are ten and five rather than an even eight and seven.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2024, 'ol')

A.card(2, 9, 'b', topic='business-5-15', concept='why-do-market-research',
       extend=1, use=[[1, 2], [3, 4]], marks=[10, 5], notation='7 + 3, then 4 + 1')

A.card(2, 9, 'c', topic='business-5-16', concept='what-packaging-is-for',
       extend=1, use=[[1, 2, 3], [4, 5]], marks=[10, 5], notation='7 + 3, then 4 + 1')

A.card(2, 9, 'd', topic='business-4-18', concept='why-a-business-expands',
       use=[[0, 1, 2], [3, 4, 5]], marks=[10, 5], notation='7 + 3, then 4 + 1')

A.card(2, 9, 'a', 'i', topic='business-5-14', concept='where-product-ideas-come-from',
       extend=1, use=[[1, 2]], marks=[10], shared_tariff=True,
       notation='15m covers (i) and (ii); this part is 10 of it, paid 7 + 3',
       row_kind='anyN',
       notes='One method is asked for and any of the scheme\'s four scores: research '
             'and development, market research, copying or adapting a competitor, or '
             'brainstorming. Research and development is the one it leads with.')

A.emit()
