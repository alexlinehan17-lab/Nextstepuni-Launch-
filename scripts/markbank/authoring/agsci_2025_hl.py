#!/usr/bin/env python3
"""Agricultural Science 2025 Higher Level — parts the deck had not carded.

Q15(c) is not here: it asks for advice under three headings and the scheme sets
its answers as three grouped lists worth 4 marks each, which the row model would
have to flatten into one undifferentiated set. It needs its own shape rather than
a rushed one.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2025, 'hl')

A.card(15, 'b', topic='agsci-3-1', concept='identifying-common-farm-weeds',
       use=[0, 1, 2], marks=[1, 1, 1], notation='3x1', spread=True,
       figure='agricultural-science-2025-HL-paper-p30-art', labels='auto',
       context='Four photographs lettered A to D: A narrow leaves in whorls up square '
               'stems, B open sky-blue daisy-like flowers, C small yellow five-petalled '
               'flowers among toothed silvery leaflets, D a field of tall yellow '
               'four-petalled flowers. Any three of the four score.')

A.emit()
