#!/usr/bin/env python3
"""Agricultural Science 2024 Ordinary Level — parts the deck had not carded.

Q1(a) is not here: its whole answer is a tick placed in one of two boxes and the
scheme prints no wording for it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2024, 'ol')

GRAZING = 'agricultural-science-2024-OL-paper-p03-art'
GRAZING_CONTEXT = ('The field is drawn as four vertical bands shading from dark green '
                   'on the left to pale on the right. Three cows and a trough stand in '
                   'the third band, the two bands to their left are grazed down, and a '
                   'grey square lettered A sits on the line between with a red arrow '
                   'pointing right.')

A.card(1, 'b', topic='agsci-3-3-2', concept='what-divides-a-grazing-strip',
       figure=GRAZING, context=GRAZING_CONTEXT,
       notes='A is the grey square on the line between the grazed and grazing bands.')

A.card(1, 'c', topic='agsci-3-3-2', concept='recognising-strip-grazing',
       figure=GRAZING, context=GRAZING_CONTEXT)

# Takes over the hand-authored card for this part: same question, now carrying
# the diagram the advantage is being read off.
A.card(1, 'd', topic='agsci-3-3-2', concept='advantages-of-strip-grazing',
       use=[[0, 1, 2, 3, 4]], marks=[2], card_id='agsci-2024-ol-q1d',
       figure=GRAZING, context=GRAZING_CONTEXT)

A.emit()
