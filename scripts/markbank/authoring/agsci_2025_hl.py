#!/usr/bin/env python3
"""Agricultural Science 2025 Higher Level — parts the deck had not carded.

Q15(c) is not here: it asks for advice under three headings and the scheme sets
its answers as three grouped lists worth 4 marks each, which the row model would
have to flatten into one undifferentiated set. It needs its own shape rather than
a rushed one.

Q1(b) is not here either: the scheme's answer runs on from the tail of its own
question cue — "the breed. A or Aberdeen Angus" — and the PDF parser puts the
answer in a different block from the part. Neither rendering gives a clean
answer to show, and trimming one by hand is the thing this pipeline exists to
avoid.
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

# ── Q1: the two bulls ─────────────────────────────────────────────────────
BULLS = 'agricultural-science-2025-HL-paper-p03-art'
BULLS_CONTEXT = ('Two bulls photographed side by side. A is solid black, deep-bodied '
                 'and hornless, in a rope halter. B is dark red with a white face, '
                 'white underline, white flank patches and white lower legs.')

A.card(1, 'a', topic='agsci-4-2', concept='identifying-cattle-breeds',
       use=[0, 1], marks=[5, 1], notation='5+1',
       figure=BULLS, labels='auto', context=BULLS_CONTEXT)

# Takes over the hand-authored card for this part: same question, now showing
# the two bulls, so the hornless one is there to look at.
A.card(1, 'c', topic='agsci-4-2', concept='what-polled-means',
       figure=BULLS, card_id='agsci-2025-hl-q1c',
       notes='Part (b) establishes that one of the two breeds is polled; this part asks '
             'what the term means.')

A.card(14, 'a', 'i', topic='agsci-3-1', concept='identifying-a-compacted-soil',
       source='pdf', use=[1, 2], marks=[6, 4], notation='6 + 4')

A.card(14, 'a', 'ii', topic='agsci-3-1', concept='available-water-in-a-soil',
       source='pdf', from_run=((14, 'a', 'ii'), 1, slice(0, None)), marks=[6],
       notation='3 for the method and 3 for the answer, or 6 for a correct answer alone')

A.emit()
