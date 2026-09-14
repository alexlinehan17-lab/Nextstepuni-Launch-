#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2023 OL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2023, 'ol')

A.card(5, topic='agsci-4-3-3', concept='farm-biosecurity-threats-and-controls',
       source='pdf', join=[(6, 2), (9, 11)], marks=[5, 5], notation='2 × (4+1)',
       figure='agricultural-science-2023-OL-paper-p07-i0',
       checked='Opened the official paper page: the generic parser correctly retains '
               'the whole Question 5 prompt and both pictured biosecurity hazards.',
       context='Each row pairs one pictured threat with its matching risk-reduction action.')

A.card(7, 'a', topic='agsci-4-3-2', concept='interpreting-ewe-mothering-scores',
       source='pdf', use=[6, 8], marks=[3, 3], notation='2(3)', stem=False,
       figure='agricultural-science-2023-OL-paper-p10-art-mothering')

A.card(14, 'b', 'iv', topic='agsci-4-3-1', concept='least-environmentally-friendly-farming',
       source='pdf',
       use=[1, [2, 4, 5, 6, 7, 8, 9], [3, 4, 5, 6, 7, 8, 9]],
       marks=[4, 4, 4], notation='4 + 2(4)',
       figure='agricultural-science-2023-OL-paper-p24-art',
       notes='The first row identifies the diagram. The next two are separate reason '
             'slots and carry every other scheme-accepted reason as alternatives.')

A.emit()
