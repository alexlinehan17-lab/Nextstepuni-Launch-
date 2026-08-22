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

A.emit()
