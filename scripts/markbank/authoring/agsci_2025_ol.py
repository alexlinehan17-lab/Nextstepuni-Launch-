#!/usr/bin/env python3
"""Agricultural Science 2025 Ordinary Level — parts the deck had not carded.

Left out: Q1(a), Q4, Q7(b), Q12, Q16 and Q17(b) all depend on artwork that is
catalogued but not published, or on a graph that was never catalogued at all;
Q12(a)(ii) and Q15(d)(i) are answered by drawing on or reordering a figure;
Q14(a)(ii) and Q17(d) are comparison tables the markdown extraction interleaves.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2025, 'ol')

A.card(8, 'b', topic='agsci-1-5', concept='reading-fertiliser-hazard-symbols',
       marks=[5], notation='3+2',
       figure='agricultural-science-2025-OL-paper-p09-i1',
       notes='Four hazard pictograms run left to right and the scheme numbers them '
             'in that order: 1 environmental hazard, 2 exclamation mark, 3 flame '
             'over a circle, 4 skull and crossbones. The two the question describes '
             'are the irritant and the fire risk.')

A.card(9, 'b', 'ii', topic='agsci-1-3', concept='what-falling-input-prices-mean',
       figure='agricultural-science-2025-OL-paper-p11-i0',
       notes='The infographic splits into input prices — electricity down 22%, '
             'fertilisers down 40%, feedstuffs down 21% — and output prices. Part '
             '(i) establishes that inputs fell; this part asks what that means.')

A.card(9, 'b', 'iv', topic='agsci-1-3', concept='what-the-price-gap-means-for-profit',
       figure='agricultural-science-2025-OL-paper-p11-i0')

A.card(13, 'a', 'i', topic='agsci-2-2-2', concept='choosing-a-soil-sampling-pattern',
       use=[0, [1, 2, 3, 4, 6]], marks=[5, 4], notation='5,4', omit=[5],
       figure='agricultural-science-2025-OL-paper-p18-i0',
       context='Three sampling patterns drawn on a field: A a tight zigzag confined '
               'to one diagonal band, B a ring of marks round the edges, C a broad '
               'W crossing the whole field.',
       notes="The scheme prints a stray 'or' on its own line between two reasons; "
             "it is not an answer and is left off the card.")

A.emit()
