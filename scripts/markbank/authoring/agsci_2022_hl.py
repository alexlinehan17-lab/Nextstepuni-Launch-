#!/usr/bin/env python3
"""Agricultural Science 2022 Higher Level — parts the deck had not carded."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2022, 'hl')

# The extraction carries the tail of the question onto the front of the marking
# point, so the answer is taken from the tenth word on.
A.card(16, 'c', 'i', topic='agsci-3-2', concept='named-grazing-systems',
       from_run=((16, 'c', 'i'), 0, slice(9, None)), marks=[3],
       notation='3 for naming one, and 1 each thereafter',
       notes='Block, strip grazing and the spokes-of-a-wheel layout also score. Zero '
             'grazing does not.')

A.emit()
