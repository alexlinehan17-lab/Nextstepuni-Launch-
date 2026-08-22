#!/usr/bin/env python3
"""Physics 2022 Higher Level — the net force part of the equilibrium experiment.

The two nuclear-equation parts of Question 10 are not here: the scheme sets
them in a bold font the text layer reads as doubled letters, so the equation
comes out as a run of repeated characters rather than nuclide symbols. They are
in the same class as the Chemistry formulae already recorded as font-mangled.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2022, 'hl')

A.card(1, None, 'vii', topic='phys-u2', concept='net-vertical-force-on-a-metre-stick',
       source='pdf', use=[0], marks=[3],
       notes='The scheme keeps "[upwards]" on the answer — the direction is part of it.')

A.emit()
