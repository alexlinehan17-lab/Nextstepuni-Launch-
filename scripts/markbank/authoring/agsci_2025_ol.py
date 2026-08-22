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

# ── Q4: the aerial farmyard photograph ────────────────────────────────────
YARD = 'agricultural-science-2025-OL-paper-p06-art'
YARD_CONTEXT = ('Aerial photograph of the farmyard with three drawn yellow arrows: A '
                'points at a large circular tank with a dark open top standing on its '
                'own hardstanding, B at a long low narrow building along the bottom of '
                'the yard, C at a small pitched-roof shed on the western side.')

A.card(4, 'a', topic='agsci-4-3-1', concept='farmyard-layout-and-labour-efficiency',
       use=[0, 1], marks=[3, 2], notation='3+2', spread=True, omit=[5],
       figure=YARD, context=YARD_CONTEXT,
       notes="The scheme's last line, 'any two valid examples', is a rubric rather than "
             "an answer, so it is left off the card.")

# The scheme runs its cue and its answer together here — "...by placing an X on
# the structure in the photograph A" — and the answer is the final letter.
A.card(4, 'b', topic='agsci-4-3-1', concept='identifying-a-slurry-store',
       source='pdf', from_run=((4, 'b', None), 0, -1), marks=[3],
       figure=YARD, context=YARD_CONTEXT,
       # Described by what each arrow points at, not by what it is for — naming
       # the function would put the answer in the label key.
       labels={'A': 'the large circular tank with a dark open top, standing alone '
                    'on hardstanding at the top of the yard',
               'B': 'the long, low, narrow building along the bottom of the yard',
               'C': 'the small pitched-roof shed on the western side, beside the '
                    'machinery area'},
       notes='The scheme prints this answer at the end of its own question cue, so the '
             'card takes the final letter of that line.')

A.card(4, 'c', topic='agsci-4-3-1', concept='farm-layout-suited-to-paddock-grazing',
       source='pdf', use=[[1, 2, 3, 4]], marks=[2], figure=YARD, context=YARD_CONTEXT)

# ── Q1(a): the cattle plate ───────────────────────────────────────────────
CATTLE = 'agricultural-science-2025-OL-paper-p03-art'
CATTLE_CONTEXT = ('Four cattle photographs under a word bank of Jersey, Holstein '
                  'Friesian, Charolais and Limousin. A is a cream-white bull, B a fawn '
                  'cow grazing among a fawn herd, C a deep red-brown heavily muscled '
                  'bull in a straw shed, D a black-and-white cow grazing.')

A.card(1, 'a', 'i', topic='agsci-4-3-2', concept='identifying-cattle-breeds-from-a-list',
       use=[0, 1, 2], marks=[2, 2, 2], notation='3x2', spread=True,
       figure=CATTLE, labels='auto', context=CATTLE_CONTEXT,
       notes='Any three of the four score at 2 marks each; the fourth is carried as an '
             'accepted alternative.')

A.card(1, 'a', 'ii', topic='agsci-4-3-2', concept='which-of-these-breeds-are-beef',
       marks=[4], figure=CATTLE, context=CATTLE_CONTEXT,
       notes='Either of the two beef breeds in the plate scores; the other two are dairy.')

A.emit()
