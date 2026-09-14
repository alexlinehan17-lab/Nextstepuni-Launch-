#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2023 HL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2023, 'hl')

A.card(7, 'a', topic='agsci-4-3-2', concept='goat-and-cow-dairy-comparison',
       source='pdf',
       from_runs=[((7, 'a', None), 2, 0),
                  ((7, 'a', None), 2, slice(1, None)),
                  ((7, 'a', None), 3, slice(0, 3)),
                  ((7, 'a', None), 3, slice(3, None))],
       marks=[3, 3, 2, 2], notation='3+3+2+2', stem=False,
       figure='agricultural-science-2023-HL-paper-p10-art-goat-table',
       notes='Rows follow the four empty cells in the official comparison table.')

A.card(7, 'b', topic='agsci-4-3-1', concept='dairy-sustainability-bonus-actions',
       source='pdf', join=[(4, 5, 2), (6, 8, 7), (9, 10), (21, 20)],
       marks=[3, 3, 2, 2], tariff='orderedSplit', notation='3+3+2+2',
       context='Each row links a named action to the scheme description that earns it.')

A.card(18, 'a', 'v', topic='agsci-4-3-3', concept='california-mastitis-test-order',
       source='pdf', use=[1], marks=[8], row_kind='allOf', notation='4(2)',
       figure='agricultural-science-2023-HL-paper-p38-art-cmt')

A.emit()
