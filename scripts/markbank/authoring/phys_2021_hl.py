#!/usr/bin/env python3
"""Physics 2021 Higher Level — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'; the markdown extraction has no points for any of these parts. The
scheme reprints the question above its own answer, which is why index 0 is
never used — it is the cue, not a marking point.

Only parts whose scheme prints an answer are here. Where it prints the marking
convention instead — "apparatus, method, observation (3 × 3)" against a
describe-an-experiment part — there is nothing to put on the back of a card, and
Q10(ii) and Q14(b)(ii) are left alone for the reason Q10(i)'s note already gives.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2021, 'hl')
MARK = ('The paper prints the part mark in brackets after the question, so the text ends '
        'on a number rather than punctuation. The question itself is complete.')

A.card(4, None, 'vi', topic='phys-3-3', concept='resistivity-of-a-metal-calculation',
       source='pdf', use=[1, 3, 4], marks=[3, 3, 3], checked=MARK,
       notes='The scheme lists "substitution" between the formula and the area with no mark '
             'of its own, so it is not a row here.')

A.card(8, None, 'iv', topic='phys-2-6', concept='deriving-the-grating-formula',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3], checked=MARK)

A.card(10, None, 'vi', topic='phys-3-6', concept='emf-induced-in-a-loop-entering-a-field',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3],
       notes='Each line carries two routes to the same mark, separated by the scheme’s '
             'own solidus: the flux route on the left, the Bsv route on the right.')

A.card(12, None, 'vi', topic='phys-3-2', concept='field-pattern-in-a-parallel-plate-capacitor',
       source='pdf', use=[1, 2], marks=[3, 3], first_sentence=True)

A.card(13, 'b', 'iv', topic='phys-3-3', concept='structure-of-a-bipolar-transistor',
       source='pdf', use=[1], marks=[7], checked=MARK,
       notes='The scheme splits the seven marks 3 + 2 + 2 across the three layers.')

A.card(14, 'b', 'iii', topic='phys-2-5', concept='doppler-speed-of-a-source',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3])

# 2021 HL Q14(c)(ii) is not here. The paper prints it as one line of a list of
# conditions — "f > fo , f is increasing and I is constant," — which is not a
# question on its own, and a card would have to supply the sentence introducing
# the list. That sentence would be written rather than lifted, so the part is
# left for a pass that can carry the stem.

A.card(2, None, 'v', topic='phys-u2', concept='focal-length-from-all-the-data',
       source='pdf', use=[1, 2], marks=[3, 3], first_sentence=True,
       notes='The scheme takes a mark off if the values are not averaged.')

A.card(2, None, 'vii', topic='phys-u2', concept='focal-length-from-a-graph',
       source='pdf', use=[1, 2], marks=[3, 3], checked=MARK)

A.card(3, None, 'iv', topic='phys-u2', concept='linear-density-from-a-graph',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 2, 3, 2], first_sentence=True)

A.card(4, None, 'iv', topic='phys-u2', concept='reading-a-temperature-off-a-resistance-graph',
       source='pdf', use=[1], marks=[3], first_sentence=True)

A.card(5, None, 'iv', topic='phys-u2', concept='average-resistance-of-a-heating-coil',
       source='pdf', use=[1, 2, 4, 5, 6], marks=[3, 3, 3, 2, 2], first_sentence=True,
       notes='The scheme prints the two energy expressions on either side of the equation '
             'it wants them set equal in.')

A.card(12, None, 'v', topic='phys-3-2', concept='why-parallel-capacitors-add',
       source='pdf', use=[1], marks=[3], first_sentence=True)

A.emit()
