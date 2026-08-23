#!/usr/bin/env python3
"""Physics 2025 Higher Level — the beta decay of iodine-131."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2025, 'hl')

A.card(14, 'c', 'ii', topic='phys-4-4', concept='beta-decay-equation-iodine-131',
       source='pdf', use=[1], marks=[7],
       notation='7 × 1',
       notes='The scheme pays the equation a mark per correct term and takes three off '
             'for each extra species written in.')

A.card(3, None, 'iv', topic='phys-u2', concept='speed-of-sound-from-a-graph',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3])


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(5, None, 'i', topic='phys-u2', concept='circuit-for-the-filament-bulb-experiment',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3])

A.card(12, 'b', 'i', topic='phys-3-6', concept='parts-of-an-ac-generator',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3], first_sentence=True)

A.emit()
