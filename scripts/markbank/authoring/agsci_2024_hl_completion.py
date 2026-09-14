#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2024 HL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2024, 'hl')

A.card(5, 'a', topic='agsci-3-2', concept='identifying-cereal-crops',
       source='md', from_run=((5, 'a', None), 0, slice(0, 6)), marks=[7],
       row_kind='allOf', notation='5+2(1)',
       figure='agricultural-science-2024-hl-paper-p009-i0',
       labels={'A': 'Oats', 'B': 'Wheat', 'C': 'Barley'})

A.card(9, 'b', 'i', topic='agsci-2-2-1', concept='soil-structure-quality',
       source='md', use=[0, 1, 2], marks=[2, 2, 2], notation='3(2)',
       figure='agricultural-science-2024-HL-paper-p14-i0', labels='auto')

A.card(9, 'b', 'ii', topic='agsci-2-2-1', concept='features-of-good-soil-structure',
       source='md', use=[0], marks=[4], spread=True,
       figure='agricultural-science-2024-HL-paper-p14-i0')

A.card(13, 'a', 'ii', topic='agsci-3-2', concept='identifying-grassland-plants',
       source='md', from_run=((13, 'a', 'ii'), 0, slice(-8, None)), marks=[8],
       row_kind='allOf', notation='4(2)',
       figure='agricultural-science-2024-HL-paper-p22-art-plants',
       labels={'A': 'Primrose', 'B': 'Nettle', 'C': 'Ragwort',
               'D': 'Meadow Thistle'})

A.card(15, 'c', 'i', topic='agsci-4-3-2', concept='average-daily-liveweight-gain',
       source='pdf', use=[3], marks=[6],
       figure='agricultural-science-2024-HL-paper-p30-art-growth')

A.card(18, 'a', 'ii', topic='agsci-4-3-2', concept='identifying-parent-breeds',
       source='pdf', use=[1, 2], marks=[6, 2], notation='6+2',
       figure='agricultural-science-2024-HL-paper-p37-art-parents', labels='auto')

A.card(18, 'b', 'iii', topic='agsci-4-2', concept='genetic-modification-in-breeding',
       source='pdf', use=[4, 5, 6], marks=[2, 2, 2], notation='3(2)',
       context='The selected official route is Genetic modification: name, description, '
               'then one importance in animal breeding.')

A.card(18, 'c', topic='agsci-3-2', concept='integrated-pest-management-controls',
       source='pdf', use=[2, 8, 21], marks=[6, 6, 4],
       tariff='orderedSplit', notation='6+6+4',
       figure='agricultural-science-2024-HL-paper-p39-art-ipm',
       notes='One official example is retained from each required approach: biological, '
             'physical, and preventative control.')

A.emit()
