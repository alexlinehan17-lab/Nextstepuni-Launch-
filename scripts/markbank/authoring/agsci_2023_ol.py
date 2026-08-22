#!/usr/bin/env python3
"""Agricultural Science 2023 Ordinary Level — parts the deck had not carded."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2023, 'ol')

A.card(1, 'b', topic='agsci-2-2-1', concept='reading-a-soil-ph-probe',
       figure='agricultural-science-2023-OL-paper-p03-i0',
       notes='The value is read off the probe in the figure, whose display shows 6.5.')

# Five continental bulls, lettered A-E, with a word bank above them. The tariff
# is centred on the middle line and covers the part: any three identified score
# 3, 2 and 1. The scheme spells the C answer "Limousine" where the paper's word
# bank spells it "Limousin"; the scheme's spelling is kept because that is the
# text the provenance gate matches against.
A.card(2, 'a', topic='agsci-4-3-3', concept='identifying-continental-beef-breeds',
       use=[0, 1, 2], marks=[3, 2, 1], notation='3+2+1', spread=True,
       figure='agricultural-science-2023-OL-paper-p04-i1', labels='auto',
       context='A is cream-white, B dark with a tan saddle, C solid red-brown, '
               'D red-and-white with a white face, E black-and-white and heavily '
               'muscled. Any three of the five score, at 3, 2 and 1 marks.')

A.card(9, 'a', 'i', topic='agsci-4-1', concept='the-fourth-stomach-chamber',
       figure='agricultural-science-2023-OL-paper-p12-i0', stem=False,
       notes='Three diagrams show the stomach at first week, 3 to 4 months and '
             'maturity. Rumen, omasum and reticulum are labelled on each; A is the '
             'chamber left unlabelled.')

A.card(10, 'b', 'ii', topic='agsci-4-3-1', concept='comparing-bull-sperm-motility',
       figure='agricultural-science-2023-OL-paper-p15-i0',
       notes='Read from the table: Bull 1 is the only one at 100% motility.')

A.card(13, 'a', 'ii', topic='agsci-3-3-1', concept='plants-for-a-reseeded-pasture',
       use=[0, 1, 2], marks=[6, 3, 3], notation='6+3+3', stem=False,
       figure='agricultural-science-2023-OL-paper-p20-i0', labels='auto',
       context='A is a head of pink-purple clover flowers, B a grass seedhead, '
               'C a white clover flower over trifoliate leaves.',
       notes="The scheme's rubric that clover is accepted once only is printed on "
             "the same line as answer C, so it travels with it.")

A.card(18, 'b', 'i', topic='agsci-4-3-2', concept='how-crispr-gene-editing-works',
       use=[0, 2], marks=[3, 1], notation='3+1', spread=True, stem=False,
       figure='agricultural-science-2023-OL-paper-p35-i0',
       notes='The diagram runs top to bottom: the target gene is marked on the '
             'strand, cut at the lightning bolt, and the strand then either repairs '
             'itself or takes an inserted gene.')

# ── Q14(b): three river diagrams ───────────────────────────────────────────
# Read from the scheme PDF rather than the markdown: the markdown splits
# "animals are not allowed into river to drink" across two answers. The figure
# is a fresh crop — the earlier one cut diagram C off entirely, which is the
# diagram part (i) asks about.
RIVER = 'agricultural-science-2023-OL-paper-p24-art'
RIVER_CONTEXT = ('Three block diagrams of one stretch of river. A: cows grazing behind a '
                 'wide strip of tall crop, arrowed X. B: cows standing in the water on '
                 'bare eroded banks, a tractor above and a person spraying, arrowed W. '
                 'C: mature trees along both banks, flowering plants, a kingfisher and '
                 'an otter, with the cattle fenced back.')

A.card(14, 'b', 'i', topic='agsci-3-3-1', concept='comparing-riverbank-biodiversity',
       source='pdf', use=[1, [2, 3, 4, 5, 6]], marks=[4, 4], spread=False,
       figure=RIVER, context=RIVER_CONTEXT)

A.card(14, 'b', 'ii', topic='agsci-3-3-1', concept='why-a-riparian-buffer-strip',
       source='pdf', use=[[1, 2, 3, 4, 5]], marks=[4], figure=RIVER,
       notes='Crop X is the strip between the cows and the river in diagram A. '
             'Any one reason scores the 4 marks; the scheme prints five.')

# Takes over the id of the hand-authored text-only card for this part rather
# than orphaning it: same question, now carrying the figure it refers to.
A.card(14, 'b', 'iii', topic='agsci-3-3-1', concept='advantages-of-spot-spraying',
       source='pdf', use=[[1, 2, 3, 4]], marks=[4], figure=RIVER,
       card_id='agsci-2023-ol-q14b-iii',
       notes='Farmer W is the figure spot-spraying in diagram B.')

# Q14(b)(iv) is left out: the scheme prints its tariff as "4, 2(4)" against a
# question asking for a diagram and two reasons, and I cannot tell from the
# scheme whether that means two reasons at 2 or four at 2. Guessing a total is
# worse than leaving the part uncarded.

# ── Q6(a)(iii): silage for dry suckler cows ───────────────────────────────
# One mark, which the scheme prints beside the answer. The extraction carries
# the tail of the question onto the front of the marking point, so the answer
# is taken from the third word on.
A.card(6, 'a', 'iii', topic='agsci-3-3-3', concept='silage-dmd-for-dry-suckler-cows',
       from_run=((6, 'a', 'iii'), 0, slice(2, 5)), marks=[1],
       notes='D is the lowest band on the paper\'s own list of silage qualities.')

A.card(13, 'b', 'ii', topic='agsci-3-2', concept='what-the-reseeding-trial-shows',
       source='pdf', from_run=((12, 'b', 'ii'), 1, slice(0, None)), marks=[2],
       notes='The scheme numbers this answer under its own Question 12 while the paper '
             'prints Question 13, and only the PDF reading has it — the markdown one '
             'files it under 13 with the question cue spliced onto the front.')

A.emit()
