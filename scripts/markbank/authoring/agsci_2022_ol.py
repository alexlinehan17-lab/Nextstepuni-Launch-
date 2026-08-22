#!/usr/bin/env python3
"""Agricultural Science 2022 Ordinary Level — parts the deck had not carded.

Not carded here, and why:
  Q10(a), Q12(a)
                 the scheme lays these out as Test/Description and
                 Factor/Description tables, and the markdown extraction
                 interleaves the columns — the marking points come out spliced.
                 Q10(c) was in this list and is now carded: only its first line
                 is spliced, and the precautions under it each stand alone.
  Q13(b)(i), Q16(a)(ii)
                 the whole answer is a shape drawn onto a photograph or graph.
  Q17(b)(i)/(iii)
                 the nitrogen table (p33) is not published.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2022, 'ol')

# Two photographs, each tagged with a drawn red arrow: A a hopper spreader on a
# tractor's three-point linkage, B a tanker with a trailing-shoe boom. The
# scheme prints the identity and the function of A on one line, so they share a
# row and the 2 + 2 marks that go with them.
A.card(1, 'a', topic='agsci-1-5', concept='identifying-farm-machinery-and-function',
       use=[[0, 1], 2, 3], marks=[4, 2, 2], notation='2,2,2,2',
       figure='agricultural-science-2022-OL-paper-p03-i0',
       context='A red arrow points at each implement. A is mounted behind the '
               'tractor and works grass; B is a tanker towed on a hard yard with a '
               'boom of trailing pipes.',
       notes="The scheme prints A's identity and A's function on a single line, so "
             "the card keeps them together and gives that row both 2-mark units. "
             "B's identity and function are printed separately and get a row each.")

# ── Q2(a): the breed plate ────────────────────────────────────────────────
BREEDS = 'agricultural-science-2022-OL-paper-p04-art'
BREEDS_CONTEXT = ('Four photographs above a word bank of Jersey, Blackface mountain, '
                  'Landrace and Simmental. A is a heavy red-brown bull with a white '
                  'face and white socks, B a long pale pink pig with drooping ears, C '
                  'a white-fleeced horned ewe with a black-and-white face, D a small '
                  'fawn cow with a large udder.')

A.card(2, 'a', 'i', topic='agsci-4-3-2', concept='identifying-farm-animal-breeds',
       use=[0, 1, 2], marks=[2, 2, 2], notation='3(2)', spread=True,
       figure=BREEDS, labels='auto', context=BREEDS_CONTEXT,
       notes='Any three of the four score at 2 marks each; the fourth is carried as an '
             'accepted alternative.')

A.card(2, 'a', 'ii', topic='agsci-4-3-2', concept='traits-of-a-sire',
       use=[0, 1], marks=[3, 1], notation='3+1', spread=True,
       figure=BREEDS, context=BREEDS_CONTEXT,
       notes='Animal A is the bull in the top-left photograph. The first trait scores 3 '
             'and the second 1, so the order they are given in decides the total.')

# ── Q7(b)(ii): how a leaf is adapted ──────────────────────────────────────
# The scheme prints "3+1" against this part, the same shape as (b)(i)'s
# "4+1+1" — the whole part is four marks, three for the first way and one for
# the second, not four for each. spread carries the six adaptations the card
# does not put on a line of its own, because any of them scores.
A.card(7, 'b', 'ii', topic='agsci-2-1', concept='leaf-adaptations-for-photosynthesis',
       use=[0, 1], marks=[3, 1], notation='3+1', spread=True, row_kind='anyN')

# ── Q10(c): sampling the pit face ─────────────────────────────────────────
# The scheme prints "2+1" — three marks, two for the first precaution and one
# for the second. Its first line is dropped: the extraction splices the tail of
# the question cue onto the front of it ("pit face to ensure accuracy when
# sampling Samples taken at random..."), so putting it on a card would show a
# student half a question as though it were an answer.
A.card(10, 'c', topic='agsci-3-3-3', concept='taking-a-representative-silage-sample',
       use=[1, 2], marks=[2, 1], notation='2+1', spread=True, row_kind='anyN',
       omit=(0,))

A.card(3, 'b', topic='agsci-3-1', concept='what-a-low-soil-ph-means-for-a-crop',
       from_runs=[((3, 'b', None), 0, slice(7, None)),
                  ((3, 'b', None), 3, slice(5, None))],
       marks=[3, 1], notation='3 + 1',
       notes='The scheme also allows reduced yield, slower growth or an effect on '
             'earthworm activity as the implication.')

A.emit()
