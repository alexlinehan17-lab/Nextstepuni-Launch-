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

# ── Q17(c): the soil organic matter calculations ──────────────────────────
# Read from the scheme PDF, which keeps the worked calculation and the
# examiner's award note in separate blocks; the markdown runs them together.
PEAT = 'agricultural-science-2024-HL-paper-p36-art'
PEAT_CONTEXT = ('The results table gives the peat sample a loss in mass of 55.2 g with '
                'its two percentage cells blanked and lettered A and B; the loam row '
                'below is filled in at 3.8, 4.2 and 2.4.')

A.card(17, 'c', 'ii', topic='agsci-3-1', concept='calculating-percent-soil-organic-matter',
       source='pdf', use=[1], marks=[6], figure=PEAT, context=PEAT_CONTEXT,
       notes='The scheme adds that a candidate giving 61.3 or 61 without showing the '
             'calculation still takes the 6 marks.')

A.card(17, 'c', 'iii', topic='agsci-3-1', concept='calculating-percent-soil-organic-carbon',
       source='pdf', use=[1], marks=[6], figure=PEAT, context=PEAT_CONTEXT,
       notes='Carries the answer to part (ii) forward; 0.58 is the conversion from '
             'organic matter to organic carbon.')

A.emit()
