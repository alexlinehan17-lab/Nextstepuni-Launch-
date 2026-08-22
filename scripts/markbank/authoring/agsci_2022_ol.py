#!/usr/bin/env python3
"""Agricultural Science 2022 Ordinary Level — parts the deck had not carded.

Not carded here, and why:
  Q10(a), Q10(c), Q12(a)
                 the scheme lays these out as Test/Description and
                 Factor/Description tables, and the markdown extraction
                 interleaves the columns — the marking points come out spliced.
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

A.emit()
