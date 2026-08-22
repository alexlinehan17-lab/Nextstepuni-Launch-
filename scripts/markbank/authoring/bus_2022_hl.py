#!/usr/bin/env python3
"""Business 2022 Higher Level — the Applied Business Question on expansion.

The scheme sets its Name/Explain/Link column labels on the same lines as the
answer, so a point cannot always be quoted to the end of its paragraph: joining
the third line of the organic-expansion answer picks up a stray "Name" that sits
elsewhere in the flattened markdown and stops the point tracing. Each row here
is quoted as far as it traces.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2022, 'hl')

A.card(2, 0, 'b', topic='business-4-18', concept='organic-expansion-and-franchising',
       words=9, use=[[1, 2], [9, 10, 11]], marks=[10, 10],
       notation='2 × 10m (3 + 3 + 3, 1)',
       notes='The two methods are organic expansion and franchising. The scheme names '
             'each in a heading of its own above the explanation, and pays for naming '
             'it, explaining it, quoting the text and evaluating it.')

A.emit()
