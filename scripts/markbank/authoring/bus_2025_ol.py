#!/usr/bin/env python3
"""Business 2025 Ordinary Level — Section 2 Question 9."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2025, 'ol')

A.card(2, 9, 'a', topic='business-4-18', concept='why-a-business-expands',
       use=[[0, 1], [2, 3, 4]], marks=[10, 5], notation='7 + 3, then 4 + 1')

A.card(2, 9, 'b', topic='business-3-16', concept='what-a-swot-analysis-gives-you',
       extend=1, use=[[1, 2], [3, 4]], marks=[10, 5], notation='7 + 3, then 4 + 1')

A.card(2, 9, 'c', topic='business-0-13', concept='what-enterprise-ireland-does',
       use=[[0, 1], [2, 3]], marks=[10, 5], notation='7 + 3, then 4 + 1')

A.card(2, 9, 'd', topic='business-6-13', concept='insurance-terms-explained',
       extend=0, use=[[0, 1, 2], [3, 4, 5], [6, 7, 8]], marks=[5, 5, 5],
       notation='4 + 1 for each of the three')

# Q9(E), the principles of insurance, is not carded. The scheme heads each
# principle before defining it and sets those headings in a column of their own,
# so the lines making up one principle are not contiguous in the markdown and
# the point cannot be quoted as a single verbatim. The build's provenance gate
# refuses it, and it is right to.

A.emit()
