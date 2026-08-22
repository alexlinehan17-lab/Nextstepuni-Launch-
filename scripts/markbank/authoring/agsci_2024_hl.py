#!/usr/bin/env python3
"""Agricultural Science 2024 Higher Level — parts the deck had not carded.

Q9(b)(i) is left out: the scheme's third answer reads "C: Poor 15%/carry
boluses/farms." — text from a neighbouring part has run into it, so the answer
set is incomplete and the corrupted line cannot be shown as written.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2024, 'hl')

A.card(10, 'a', topic='agsci-3-2', concept='recognising-a-multi-species-sward',
       figure='agricultural-science-2024-HL-paper-p15-i0',
       notes='Two cutaway sward illustrations. A is a single grass species with '
             'short, uniform roots; B carries grasses, broadleaf herbs and clover '
             'above ground and a mix of shallow and deep roots below it.')

# ── Q17(c): the soil organic matter calculations ──────────────────────────
# Read from the scheme PDF, which keeps the worked calculation and the
# examiner's award note in separate blocks; the markdown runs them together.
PEAT = 'agricultural-science-2024-HL-paper-p36-art'
PEAT_CONTEXT = ('The results table gives the peat sample a loss in mass of 55.2 g with '
                'its two percentage cells blanked and lettered A and B; the loam row '
                'below is filled in at 3.8, 4.2 and 2.4.')

A.card(17, 'c', 'ii', topic='agsci-3-1', concept='calculating-percent-soil-organic-matter',
       source='pdf', use=[1], marks=[6], figure=PEAT, context=PEAT_CONTEXT,
       notes='The scheme adds that a candidate giving 61.3 or 61 without showing the '
             'calculation still takes the 6 marks.')

A.card(17, 'c', 'iii', topic='agsci-3-1', concept='calculating-percent-soil-organic-carbon',
       source='pdf', use=[1], marks=[6], figure=PEAT, context=PEAT_CONTEXT,
       notes='Carries the answer to part (ii) forward; 0.58 is the conversion from '
             'organic matter to organic carbon.')

# ── Q2(a): three breed photographs ────────────────────────────────────────
BREEDS24 = 'agricultural-science-2024-HL-paper-p04-art'
BREEDS24_CONTEXT = ('Three photographs: A a long pale pink pig with forward-drooping '
                    'ears, B the head of a sheep with a bare blue-grey face and long '
                    'upright ears over a dense cream fleece, C a heavy red-brown bull '
                    'with broad white patches and a white head.')

A.card(2, 'a', 'i', topic='agsci-4-1', concept='identifying-pig-sheep-and-cattle-breeds',
       use=[0, 1], marks=[2, 2], notation='2(2)', spread=True,
       figure=BREEDS24, labels='auto', context=BREEDS24_CONTEXT,
       notes='Any two of the three score at 2 marks each; the third is carried as an '
             'accepted alternative.')

# The scheme runs this answer on from the tail of its own cue — "Explain the
# underlined term. Produce many offspring" — so the card takes the words after it.
A.card(2, 'a', 'ii', topic='agsci-4-1', concept='what-prolificacy-means',
       from_run=((2, 'a', 'ii'), 0, slice(4, None)), marks=[2],
       figure=BREEDS24,
       notes='Breed B is the sheep in the middle photograph.')

A.card(2, 'a', 'iii', topic='agsci-4-1', concept='characteristics-of-a-terminal-sire',
       source='pdf', use=[1, 2], marks=[2, 2], notation='2(2)', spread=True,
       figure=BREEDS24,
       notes='Bull C is the red-and-white bull in the right-hand photograph.')

# ── Q1: bale wrapper, stomach tube, head gate ─────────────────────────────
KIT = 'agricultural-science-2024-HL-paper-p03-art'
KIT_CONTEXT = ('Three photographs. A is a green trailed machine with two rollers and a '
               'hooped arm carrying reels of film. B is a person kneeling in straw with '
               'a lamb across their lap, a long flexible tube running from a large '
               'syringe into its mouth. C is a hinged frame set into a hurdle pen that '
               'closes around an animal\'s neck, with a ewe and lamb beside it.')

A.card(1, 'a', topic='agsci-1-5', concept='identifying-sheep-farm-equipment',
       use=[0, 1, [2, 3]], marks=[2, 2, 2], notation='3(2)',
       figure=KIT, labels='auto', context=KIT_CONTEXT,
       notes="The scheme accepts either name for C.")

# The scheme runs this answer on from the tail of its own cue — "on a sheep
# farm. Filled with colostrum" — so the card takes the words after it.
A.card(1, 'b', topic='agsci-1-5', concept='how-a-stomach-tube-is-used',
       from_run=((1, 'b', None), 0, slice(4, None)), marks=[4],
       figure=KIT,
       notes='Equipment B is the tube and syringe in the middle photograph. The scheme '
             'also accepts describing the tube being passed down the oesophagus into the '
             'stomach, and feeding weak lambs.')

A.emit()
