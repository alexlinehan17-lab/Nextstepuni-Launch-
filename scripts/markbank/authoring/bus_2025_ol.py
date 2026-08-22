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

A.emit()
