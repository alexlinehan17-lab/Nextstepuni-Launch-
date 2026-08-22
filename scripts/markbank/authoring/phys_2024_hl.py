#!/usr/bin/env python3
"""Physics 2024 Higher Level — the charge held by the capacitor."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2024, 'hl')

A.card(11, None, 'vii', topic='phys-3-2', concept='charge-on-a-capacitor-mid-discharge',
       source='pdf', use=[0, 1, 2], marks=[2, 3, 3])

A.emit()
