#!/usr/bin/env python3
"""Chemistry 2024 Ordinary Level — parts the deck had not carded.

Every pairing here was read and confirmed rather than assumed. The wording
score cannot vouch for most of them — an electron configuration shares no words
with "Write the electron configuration for an atom of nitrogen" — so the aligner
places them on order alone, and order alone is not evidence. Read against the
scheme they are unambiguous: 1s2, 2s2, 2p3 for nitrogen and 2p5 for fluorine,
3.98 - 3.04 for the electronegativity difference between N and F, polar covalent
for the bonding that follows from it.

Marks are not guessed. The scheme prints one combined tariff per question —
"(9 + 6 + 4 + 3 + 2 + 2 + 2)" against Q5(b) and "(8 + 6 + 2 + 2)" against Q8(a) —
which splits over the parts in order. Q5(b)'s seven numbers sum to 28 and the
paper prints (28) at the end of that question, so the split is confirmed rather
than assumed.

Q4(f)(ii) is not here: it asks about hazard symbol B and that symbol is not
among the published figures, so the card would ask about something it cannot
show.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('chemistry', 2024, 'ol')

A.card(5, 'b', 'i', topic='chem-4-3', concept='naming-a-greenhouse-gas',
       source='pdf', use=[[0]], marks=[9], notation='9 + 6 + 4 + 3 + 2 + 2 + 2')

A.card(5, 'b', 'ii', topic='chem-1-2', concept='electron-configuration-of-nitrogen',
       source='pdf', use=[[0, 1]], marks=[6], notation='9 + 6 + 4 + 3 + 2 + 2 + 2')

A.card(5, 'b', 'iii', topic='chem-1-2', concept='electron-configuration-of-fluorine',
       source='pdf', use=[[0, 1]], marks=[4], notation='9 + 6 + 4 + 3 + 2 + 2 + 2')

A.card(5, 'b', 'v', topic='chem-1-3', concept='electronegativity-difference-n-and-f',
       source='pdf', use=[0], marks=[2], notation='9 + 6 + 4 + 3 + 2 + 2 + 2')

A.card(5, 'b', 'vi', topic='chem-2-2', concept='bonding-from-electronegativity-difference',
       source='pdf', use=[[0, 1]], marks=[2], notation='9 + 6 + 4 + 3 + 2 + 2 + 2')

A.card(8, 'a', 'i', topic='chem-2-4', concept='homologous-series-of-ethene',
       source='pdf', use=[1], marks=[8], notation='8 + 6 + 2 + 2')

A.card(8, 'a', 'ii', topic='chem-4-2', concept='naming-the-alcohol-from-ethene',
       source='pdf', use=[1], marks=[6], notation='8 + 6 + 2 + 2')

A.card(5, 'b', 'vii', topic='chem-1-4', concept='shape-of-a-four-atom-molecule',
       source='pdf', from_run=((5, 'b', 'vii'), 5, slice(0, 1)), marks=[2],
       notation='2 of the 28 the scheme splits 9 + 6 + 4 + 3 + 2 + 2 + 2 across Q5(b)',
       first_sentence=True,
       notes='The scheme accepts tetrahedral, triangular or trigonal as well.')

A.card(7, 'a', 'ii', topic='chem-u1', concept='graph-of-oxygen-volume-against-time',
       source='pdf',
       from_runs=[((7, 'a', 'ii'), 0, slice(0, 2)),
                  ((7, 'a', 'ii'), 0, slice(3, 5)),
                  ((7, 'a', 'ii'), 0, slice(6, 8)),
                  ((7, 'a', 'ii'), 0, slice(21, 25))],
       marks=[3, 3, 6, 3], notation='3 + 3 + 6 × 1 + 3',
       notes='The scheme caps the plotting marks at three if graph paper is not used, '
             'and wants a curve of best fit rather than a straight line — the rate falls '
             'away as the reaction proceeds.')

A.emit()
