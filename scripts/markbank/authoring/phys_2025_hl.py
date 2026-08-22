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

A.emit()
