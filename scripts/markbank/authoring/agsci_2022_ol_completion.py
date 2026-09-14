#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2022 OL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2022, 'ol')

A.card(10, 'a', topic='agsci-2-2-2', concept='testing-soil-ph-and-texture',
       source='pdf', use=[2, 4], marks=[4, 3], tariff='orderedSplit',
       notation='4+2+1', notes='The official tariff awards the response by position.')

A.card(12, 'a', topic='agsci-2-1', concept='factors-in-soil-formation',
       source='pdf', use=[2, 7, 12], marks=[2, 1, 1], tariff='orderedSplit',
       notation='2+1+1')

A.card(16, 'a', 'ii', topic='agsci-3-2', concept='reading-a-grass-growth-graph',
       source='pdf', use=[1], marks=[2], row_kind='criterion',
       figure='agricultural-science-2022-OL-paper-p29-art-q16a')

A.card(17, 'b', 'i', topic='agsci-3-2', concept='nitrogen-cycle-processes',
       source='md', use=[0, 1], marks=[4, 4], notation='2(4)',
       figure='agricultural-science-2022-OL-paper-p33-art')

A.card(17, 'b', 'iii', topic='agsci-3-2', concept='nitrogen-cycle-calculation',
       source='md', use=[0, 1], marks=[4, 2], notation='4+2',
       figure='agricultural-science-2022-OL-paper-p33-art')

A.emit()
