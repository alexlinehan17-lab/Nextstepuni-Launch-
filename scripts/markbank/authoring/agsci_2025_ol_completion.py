#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2025 OL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2025, 'ol')

A.card(5, 'a', topic='agsci-2-2-1', concept='ideal-soil-composition',
       source='pdf', use=[1, [2, 3, 4, 5]], marks=[3, 2], notation='3+2',
       figure='agricultural-science-2025-OL-paper-p07-i0')

A.card(5, 'b', topic='agsci-2-2-1', concept='high-mineral-and-organic-content',
       source='pdf', use=[1], marks=[2], spread=True, omit=[0],
       figure='agricultural-science-2025-OL-paper-p07-i0')

A.card(7, 'a', topic='agsci-3-2', concept='identifying-sward-plants',
       source='pdf', use=[1, 2, 3], marks=[2, 2, 2], notation='3x2',
       spread=True, omit=[0],
       figure='agricultural-science-2025-OL-paper-p08-art-plants',
       labels={'A': 'Perennial ryegrass', 'B': 'White clover',
               'C': 'Nettle', 'D': 'Chicory'})

A.card(7, 'b', topic='agsci-3-2', concept='undesired-sward-plant',
       source='md', use=[0], marks=[4],
       figure='agricultural-science-2025-OL-paper-p08-art-plants')

A.card(9, 'a', 'i', topic='agsci-4-3-2', concept='normal-calf-presentation',
       source='pdf', use=[1], marks=[5], notation='3+2',
       figure='agricultural-science-2025-OL-paper-p10-i0')

A.card(10, 'a', topic='agsci-4-2', concept='identifying-a-sex-cell',
       source='md', use=[0], marks=[3],
       figure='agricultural-science-2025-OL-paper-p12-i0',
       labels={'A': 'Sperm or male'})

A.card(12, 'a', 'i', topic='agsci-4-3-3', concept='main-cause-of-lamb-mortality',
       source='md', use=[0], marks=[3],
       figure='agricultural-science-2025-OL-paper-p15-art-mortality')

A.card(12, 'a', 'ii', topic='agsci-4-3-3', concept='completing-a-mortality-chart',
       source='md', use=[0], marks=[2], row_kind='criterion',
       figure='agricultural-science-2025-OL-paper-p15-art-mortality')

A.card(12, 'b', 'i', topic='agsci-4-3-2', concept='comparing-lamb-growth-rates',
       source='md', use=[0], marks=[3],
       figure='agricultural-science-2025-OL-paper-p16-art-growth')

A.card(12, 'b', 'iii', topic='agsci-4-3-2', concept='predicting-lamb-slaughter-weight',
       source='md', use=[0], marks=[3],
       figure='agricultural-science-2025-OL-paper-p16-art-growth')

A.card(14, 'a', 'ii', topic='agsci-3-2', concept='weather-effects-on-potato-planting',
       source='pdf', use=[3, 11], marks=[5, 4], tariff='orderedSplit',
       notation='2(2)+3+2',
       context='The selected official crop is potatoes; the rows cover temperature '
               'and rainfall with their matching impacts.')

A.card(14, 'c', 'iii', topic='agsci-3-2', concept='identifying-field-crops',
       source='pdf', use=[1, 2], marks=[4, 4], notation='2(4)', spread=True,
       omit=[0], figure='agricultural-science-2025-OL-paper-p23-art-crops',
       labels={'J': 'Maize', 'K': 'Wheat', 'L': 'Oilseed rape'})

A.card(15, 'd', 'i', topic='agsci-4-3-2', concept='ordering-calf-nutrition-stages',
       source='pdf', join=[(1, 2, 3)], marks=[8], row_kind='allOf', notation='4x2',
       figure='agricultural-science-2025-OL-paper-p27-art-calf-nutrition')

A.card(16, 'a', 'i', topic='agsci-4-3-2', concept='suitable-beef-animal-housing',
       source='pdf', use=[1, 2, 3], marks=[4, 4, 2], tariff='orderedSplit',
       notation='4+4+2', spread=True, omit=[0],
       figure='agricultural-science-2025-OL-paper-p28-art-housing')

A.card(16, 'c', 'i', topic='agsci-4-3-2', concept='grass-silage-dry-matter',
       source='md', use=[0], marks=[6],
       figure='agricultural-science-2025-OL-paper-p30-art-dm-table')

A.card(17, 'b', 'ii', topic='agsci-2-2-1', concept='ordering-a-flocculation-test',
       source='pdf', join=[(1, 2, 3)], marks=[16], row_kind='allOf', notation='4x4',
       figure='agricultural-science-2025-ol-paper-p032-i0')

A.card(17, 'd', topic='agsci-4-3-2', concept='matching-production-systems-and-dam-breeds',
       source='pdf',
       from_runs=[((17, 'd', None), 10, slice(0, 3)),
                  ((17, 'd', None), 11, slice(2, 4)),
                  ((17, 'd', None), 12, slice(3, 6)),
                  ((17, 'd', None), 10, slice(3, None)),
                  ((17, 'd', None), 11, 4),
                  ((17, 'd', None), 12, slice(6, None))],
       join=[(0, 1, 2), (3, 4, 5)], marks=[6, 6], notation='2 × (3+3)',
       context='Each row gives a production system, a suitable dam breed, and the '
               'scheme reason for that breed.')

A.card(18, 'c', 'i', topic='agsci-1-3', concept='reading-dairy-export-change',
       source='md', from_run=((18, 'c', 'i'), 0, slice(1, None)), marks=[6],
       figure='agricultural-science-2025-OL-paper-p36-art-exports')

A.card(18, 'c', 'ii', topic='agsci-1-3', concept='estimating-dairy-export-tonnage',
       source='md', use=[0], marks=[6],
       figure='agricultural-science-2025-OL-paper-p36-art-exports')

A.emit()
