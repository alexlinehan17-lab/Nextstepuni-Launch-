#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2022 HL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2022, 'hl')

A.card(13, 'a', 'iv', topic='agsci-3-2', concept='identifying-plants-from-a-plate',
       source='md', use=[0, 1], marks=[3, 3], notation='2(3)',
       figure='agricultural-science-2022-HL-paper-p20-i0')

A.card(13, 'b', 'iii', topic='agsci-3-2', concept='certified-and-uncertified-seed',
       source='pdf', join=[(1, 7), (2, 8), (3, 9), (4, 10)],
       marks=[2, 2, 2, 2], tariff='orderedSplit', notation='4 × 2',
       context='Each row reads Certified seed first, then Uncertified seed.',
       notes='The official comparison table is retained as paired rows.')

A.card(14, 'c', 'ii', topic='agsci-4-3-1', concept='ventilation-opening-calculation',
       source='pdf', use=[1, 2], marks=[4, 1], notation='4+1', row_kind='criterion',
       figure='agricultural-science-2022-HL-paper-p25-i0')

A.card(18, 'b', 'ii', topic='agsci-4-3-1', concept='integrated-mitigation-strategies',
       source='pdf', join=[(2, 1), (4, 3), (6, 7, 5), (9, 8)],
       marks=[3, 3, 3, 3], tariff='orderedSplit', notation='4 × 3',
       figure='agricultural-science-2022-HL-paper-p38-i0',
       context='Each row links the scheme heading to its matching advice.')

A.emit()
