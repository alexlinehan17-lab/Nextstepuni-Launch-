#!/usr/bin/env python3
"""Agricultural Science 2023 Higher Level — parts the deck had not carded."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2023, 'hl')

# The scheme splits this five and three: five for reading the relationship off
# the graph, three for what a farmer should do about it.
A.card(15, 'c', 'ii', topic='agsci-3-1', concept='soil-ph-and-nitrous-oxide-emissions',
       use=[0, 1], marks=[5, 3], notation='5 + 3')

A.card(8, 'c', topic='agsci-3-1', concept='what-the-urea-leaching-test-shows',
       from_run=((8, 'c', None), 0, slice(1, None)), marks=[3],
       notes='The scheme goes on to say what a farmer should do about it: use protected '
             'urea, because less nitrate leaches from it.')

A.card(16, 'a', 'ii', topic='agsci-4-3-1', concept='reading-an-emissions-figure-against-average',
       from_runs=[((16, 'a', 'ii'), 0, slice(5, 6)),
                  ((16, 'a', 'ii'), 0, slice(6, None))],
       marks=[5, 1], notation='5 + 1')

A.emit()
