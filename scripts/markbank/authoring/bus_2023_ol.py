#!/usr/bin/env python3
"""Business 2023 Ordinary Level — Section 2 Question 9."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2023, 'ol')

A.card(2, 9, 'a', topic='business-0-12', concept='where-business-ideas-come-from',
       extend=1, use=[1, 2], marks=[5, 5], notation='5m each')

A.card(2, 9, 'b', topic='business-5-15', concept='desk-and-field-research',
       extend=1, use=[[1, 2, 3, 4], [7, 8, 9, 10, 11, 12]], marks=[8, 7],
       notation='8m (3 + 3 + 2), 7m (3 + 2 + 2)',
       notes='The scheme lists examples of each kind under it — the internet and '
             'sales reports for desk research, surveys and questionnaires for field '
             'research. They are illustrations, not the marking points.')

A.card(2, 9, 'e', topic='business-0-12', concept='challenges-of-starting-a-business',
       use=[[0, 1, 2, 3, 4], [5, 6]], marks=[8, 7],
       notation='8m (4 + 4), 7m (4 + 3)')

A.emit()
