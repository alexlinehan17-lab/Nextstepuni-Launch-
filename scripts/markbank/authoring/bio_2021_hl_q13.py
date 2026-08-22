#!/usr/bin/env python3
"""Biology 2021 Higher Level Q13(b) — the respiration-diagram parts.

The scheme answers these on the same line as the question it is repeating —
"Name the series of events represented by Y: *Krebs' cycle 3" — so the answer is
taken out of that line rather than off a line of its own. The leading asterisk
is the scheme's mark for an essential answer, an annotation to the examiner, and
no card in any deck carries one.

Part (viii)'s question runs into part (ix) in the paper's block, so the question
text is trimmed to its own sentence and confirmed against the scheme.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('biology', 2021, 'hl')

A.card(13, 'b', 'vii', topic='bio-2-2', concept='the-series-of-events-at-y',
       source='pdf', from_run=((13, 'b', 'vii'), 0, slice(8, 10)), marks=[3],
       notes='Y labels a stage on the respiration diagram in the paper.')

A.card(13, 'b', 'viii', topic='bio-2-2', concept='the-substance-at-z',
       source='pdf', from_run=((13, 'b', 'viii'), 0, slice(11, 15)), marks=[3],
       first_sentence=True,
       notes='Z labels a product on the respiration diagram in the paper.')

A.card(13, 'b', 'iv', topic='bio-2-2', concept='the-3-carbon-molecule-of-stage-1',
       source='pdf', from_run=((13, 'b', 'iv'), 0, slice(8, 12)), marks=[3])

A.card(13, 'b', 'v', topic='bio-2-2', concept='the-organelle-at-w',
       source='pdf', from_run=((13, 'b', 'v'), 0, slice(3, 4)), marks=[3],
       notes='W labels an organelle on the respiration diagram in the paper.')

A.card(13, 'b', 'vi', topic='bio-2-2', concept='the-2-carbon-molecule-x',
       source='pdf', from_run=((13, 'b', 'vi'), 0, slice(5, 8)), marks=[3],
       notes='X labels a molecule on the respiration diagram in the paper.')

A.emit()
