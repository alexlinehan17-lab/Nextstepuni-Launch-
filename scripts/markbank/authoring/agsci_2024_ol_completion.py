#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2024 OL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2024, 'ol')

A.card(11, 'a', 'ii', topic='agsci-4-2', concept='selecting-breeding-offspring',
       source='md', use=[0], marks=[3],
       figure='agricultural-science-2024-ol-paper-p014-i0')

A.card(13, 'b', 'iii', topic='agsci-2-1', concept='choosing-a-graph-for-frequency-data',
       source='pdf', from_run=((13, 'b', 'iii'), 1, 1), marks=[6],
       figure='agricultural-science-2024-OL-paper-p21-i1',
       checked='Opened the official scheme page: its tick is in the middle box, B, '
               'which is the bar chart shown on the paper.')

A.card(14, 'b', 'i', topic='agsci-3-2', concept='silage-cutting-stage',
       source='pdf', from_run=((14, 'b', 'i'), 1, 1), marks=[2],
       figure='agricultural-science-2024-OL-paper-p22-i1',
       checked='Opened the official paper and scheme pages: the complete prompt is '
               'correct and the tick is in box B.')

A.emit()
