#!/usr/bin/env python3
"""Agricultural Science 2021 Higher Level — parts the deck had not carded.

Every questionText here comes from the paper and every verbatim from the
scheme; agsci_lib refuses anything else. What this file contributes is the
editorial part: which part is worth a card, where it sits in the topic tree,
how the scheme's tariff notation maps onto rows, and what the figure is
showing. See agsci_lib.Author for what it will not let through.

Not carded here, and why:
  Q14(a)      the scheme prints a two-column comparison table that the
              markdown extraction interleaves — the marking points come out
              spliced together and cannot be trusted.
  Q14(b)(i)   readable, but its figure (p27) is not published yet, and an
              "identify each of the following breeds" card without the
              photographs is a dangling reference.
  Q15(b)(*)   same: the graph on p32 is not published, and every part leans
              on reading it.
  Q16(a)(i)   the scheme's answer is a worked calculation laid out as a
              table, interleaved the same way Q14(a) is.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2021, 'hl')

A.card(1, 'a', topic='agsci-3-2', concept='identifying-common-weeds',
       figure='agricultural-science-2021-HL-paper-p03-i0', labels='auto',
       context='Three photographs. A is a yellow five-petalled flower in grass, '
               'B a cluster of purple spiny flowerheads, C a broad-leaved rosette.')

# ── Q3(a): the farm safety notice ──────────────────────────────────────────
A.card(3, 'a', 'i', topic='agsci-1-5', concept='farm-safety-sign-symbols',
       use=[[0, 1], 2], marks=[2, 2],
       figure='agricultural-science-2021-HL-paper-p06-i0', labels='auto',
       context='On the reproduced notice, A is the yellow panel beside a triangular '
               'warning pictogram of a bull, and B the red panel beside a pictogram '
               'of an adult and child. The other two panels are already captioned.')

A.card(3, 'a', 'ii', topic='agsci-1-5', concept='animal-husbandry-equipment',
       figure='agricultural-science-2021-HL-paper-p06-i1', labels='auto',
       context='C is a long-handled pincer tool with blue grips; D a hinged metal '
               'frame with a ratcheted bar and two red cords.')

A.card(3, 'a', 'iii', topic='agsci-1-5', concept='castration-and-farm-sustainability',
       use=[[0, 2, 3]], marks=[2],
       figure='agricultural-science-2021-HL-paper-p06-i1',
       notes='The question points back at picture C from part (ii), so the card '
             'carries the same figure.')

# ── Q3(b): the two tractors ────────────────────────────────────────────────
A.card(3, 'b', 'i', topic='agsci-3-3-2', concept='identifying-farm-machines',
       use=[[0, 1, 2], 3], marks=[2, 2],
       figure='agricultural-science-2021-HL-paper-p07-i0', labels='auto',
       context='Red arrows mark each machine. A is mounted behind a tracked tractor '
               'working bare tilled ground; B is a high-sided trailer being towed '
               'across standing grass.')

A.card(3, 'b', 'ii', topic='agsci-3-3-2', concept='tracked-tractor-advantage',
       use=[[0, 1, 3, 4]], marks=[2],
       figure='agricultural-science-2021-HL-paper-p07-i0',
       notes='Any one advantage scores the 2 marks; the scheme prints four.')

A.card(3, 'b', 'iii', topic='agsci-3-3-2', concept='one-pass-environmental-benefit',
       use=[[0, 1, 2, 4]], marks=[2],
       figure='agricultural-science-2021-HL-paper-p07-i0')

# ── Q4(c): the farmyard photograph ─────────────────────────────────────────
A.card(4, 'c', topic='agsci-4-3-1', concept='farmyard-environmental-improvements',
       use=[1, 2], marks=[2, 2], notation='2(2)', spread=True, omit=[0],
       figure='agricultural-science-2021-HL-paper-p08-i0',
       context="Scheme tariff is 2(2): any two of the printed ways score 2 marks each.",
       notes="The scheme's first line welds a rubric — that the answer may not repeat "
             "part (a) — onto its first suggestion, so that line is left off the card "
             "rather than shown as an answer. The rubric itself is in the question.")

A.emit()
