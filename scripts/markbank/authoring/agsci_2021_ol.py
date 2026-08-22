#!/usr/bin/env python3
"""Agricultural Science 2021 Ordinary Level — parts the deck had not carded.

Not carded here, and why:
  Q8(b)(i)    the safety sign it asks about is not among the published figures.
  Q10(d)      the whole answer is an X placed on a diagram; there is no
              marking point a card could show.
  Q11(b)(iv)  same, plus the scheme's reason column is interleaved with the
              placement instruction.
  Q12(a)      the breed photographs are not published, and the paper's word
              bank runs into the question text.
  Q18(b)(iii) the paper's own question landed in the block after the intro, so
              the extractor reports the intro as the question. Left until the
              text can be lifted correctly rather than typed in by hand.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2021, 'ol')

# Q4 shows two profiles side by side: A humus-rich, stony, 3 m to parent rock;
# B pale grey and heavily leached over a darker brown horizon, 2 m. Q4(a),
# already carded, names them; these two ask what follows from each.
FIG = 'agricultural-science-2021-OL-paper-p07-i1'

A.card(4, 'b', topic='agsci-2-1', concept='uses-of-a-brown-earth-soil',
       use=[[0, 1, 2, 3]], marks=[2], figure=FIG,
       notes='Any one use scores the 2 marks; the scheme prints four.')

A.card(4, 'c', topic='agsci-2-1', concept='disadvantages-of-a-podzol',
       use=[0, 1], marks=[3, 1], notation='3+1', spread=True, figure=FIG,
       context='Scheme tariff is 3+1: the first disadvantage scores 3 and the '
               'second 1, so the order the answers are given in decides the total.')

# Q12(a), the breed plate, is not carded. The scheme names all four breeds and
# the figure exists, but agricultural-science-2021-OL-paper-p16-i0 has not been
# through the inspection pass, so it has no verified alt text and the build
# refuses to bind it. Carding it needs that pass, not more authoring.

A.emit()
