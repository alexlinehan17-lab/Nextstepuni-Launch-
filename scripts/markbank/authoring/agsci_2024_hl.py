#!/usr/bin/env python3
"""Agricultural Science 2024 Higher Level — parts the deck had not carded.

Q9(b)(i) is left out: the scheme's third answer reads "C: Poor 15%/carry
boluses/farms." — text from a neighbouring part has run into it, so the answer
set is incomplete and the corrupted line cannot be shown as written.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2024, 'hl')

A.card(10, 'a', topic='agsci-3-2', concept='recognising-a-multi-species-sward',
       figure='agricultural-science-2024-HL-paper-p15-i0',
       notes='Two cutaway sward illustrations. A is a single grass species with '
             'short, uniform roots; B carries grasses, broadleaf herbs and clover '
             'above ground and a mix of shallow and deep roots below it.')

A.emit()
