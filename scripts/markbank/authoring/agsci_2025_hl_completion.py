#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2025 HL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2025, 'hl')

A.card(1, 'b', topic='agsci-4-1', concept='dominant-polled-cattle-breed',
       source='md', from_run=((1, 'b', None), 0, slice(-4, None)), marks=[2],
       figure='agricultural-science-2025-HL-paper-p03-art')

A.card(6, 'a', topic='agsci-4-3-2', concept='identifying-lambing-equipment',
       source='pdf', use=[2, 3, 4], marks=[2, 2, 2], notation='3 × (1+1)',
       figure='agricultural-science-2025-HL-paper-p11-art-lambing-kit', labels='auto',
       notes='Each selected item earns one mark for the correct picture and one for '
             'the scheme-stated name.')

A.card(7, 'b', topic='agsci-2-2-2', concept='soil-microbiome-and-water-retention',
       source='pdf', use=[6, 12], marks=[4, 1], notation='4+1',
       figure='agricultural-science-2025-HL-paper-p12-i0',
       context='This card uses the official water-retention route: contribution first, '
               'then its productivity benefit.')

A.card(15, 'c', topic='agsci-3-2', concept='weed-control-advice',
       source='pdf',
       use=[[2, 3, 4, 5, 6, 7],
            [10, 11, 12, 13, 14],
            [16, 17, 18, 19],
            [3, 4, 5, 6, 7, 11, 12, 13, 14, 17, 18, 19]],
       marks=[4, 4, 4, 4], notation='4 × 4',
       figure='agricultural-science-2025-HL-paper-p30-art',
       context='Rows 1–3 give one point under each printed heading; row 4 is a '
               'different additional point from any heading.',
       notes='The fourth answer must be distinct from the three already used.')

A.emit()
