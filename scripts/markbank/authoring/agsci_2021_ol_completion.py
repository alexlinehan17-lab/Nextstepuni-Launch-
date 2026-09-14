#!/usr/bin/env python3
"""Final provenance-checked Agricultural Science 2021 OL cards."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2021, 'ol')

A.card(11, 'b', 'iv', topic='agsci-4-3-1', concept='interpreting-a-farm-plan',
       source='pdf', use=[1, 4], marks=[2, 2], notation='2+2',
       figure='agricultural-science-2021-OL-paper-p15-i0')

A.card(18, 'b', 'iii', topic='agsci-4-3-2', concept='polled-cattle-trait-and-benefit',
       source='pdf',
       from_runs=[((18, 'b', 'iii'), 1, slice(17, 22)),
                  ((18, 'b', 'iii'), 1, slice(23, None))],
       marks=[2, 2], notation='2+2',
       figure='agricultural-science-2021-OL-paper-p34-i0')

A.emit()
