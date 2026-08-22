#!/usr/bin/env python3
"""Business 2022 Ordinary Level — Section 2 Question 9.

Marks are the splits the scheme prints in its own tariff column beside each
point: 8m (4 + 4) for the first, 7m (4 + 3) for the second.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2022, 'ol')

A.card(2, 9, 'b', topic='business-5-15', concept='why-do-market-research',
       extend=1, use=[[1, 2], [3, 4]], marks=[8, 7],
       notation='8m (4 + 4), 7m (4 + 3)')

A.card(2, 9, 'e', topic='business-5-16', concept='choosing-advertising-media',
       extend=1, use=[[1, 2, 3, 4], [5, 6]], marks=[8, 7],
       notation='8m (4 + 4), 7m (4 + 3)')

A.emit()
