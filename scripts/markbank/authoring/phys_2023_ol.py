#!/usr/bin/env python3
"""Physics 2023 Ordinary Level — parts the deck had not carded.

The scheme repeats each question before answering it, so the answer is taken
out of the line rather than off one of its own.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2023, 'ol')

# The paper prints Q13's parts roman-only — (i) to (viii) — but the scheme's
# text layer misses the "14." heading and picks up Q13(iv)'s inline "(a)/(b)"
# sub-letters, so the scheme parser keys Q13(v) onward under (13, 'b', ...)
# and all of Q14 under 13's letters. Cards cite the paper's own numbering and
# keep their shipped ids; only the from_run parents use the parser's keys.
A.card(13, None, 'v', topic='phys-4-4', concept='daughter-nucleus-after-beta-decay',
       source='pdf', card_id='phys-2023-ol-q13b-v',
       from_run=((13, 'b', 'v'), 1, slice(0, 2)), marks=[3],
       checked='The paper prints the part mark "(7)" after the question, so the text ends '
               'on a bracketed number rather than punctuation. The question itself is '
               'complete.',
       notes='The scheme prints "[3 + 2 + 2]" against this line, covering this part and '
             'the two that follow it.')

A.card(10, None, 'vi', topic='phys-2-4', concept='nodes-on-a-stationary-wave',
       source='pdf', from_run=((10, None, 'vi'), 0, slice(9, 10)), marks=[4],
       notes='The scheme reprints the question above its answer and the two run together '
             'in one line, so the answer is the word after the question mark.')

A.card(10, None, 'vii', topic='phys-2-4', concept='amplitude-on-a-stationary-wave',
       source='pdf', use=[0], marks=[4])

A.card(10, None, 'viii', topic='phys-2-4', concept='wavelength-from-node-separation',
       source='pdf', from_run=((10, None, 'viii'), 1, slice(0, 6)), marks=[6],
       notes='The scheme runs the next part on from this answer in the same line; the '
             'six words taken are this part\'s working and result.')

A.card(13, None, 'viii', topic='phys-4-6', concept='why-fusion-is-preferred-to-fission',
       source='pdf', card_id='phys-2023-ol-q13b-viii',
       from_run=((13, 'b', 'viii'), 1, slice(12, 17)), marks=[7],
       checked='The paper prints this part as the sentence introducing the question that '
               'follows it in the same block. The question asked is the one the scheme '
               'reprints above its answer.')

A.card(11, None, 'vii', topic='phys-3-3', concept='why-a-filament-graph-curves',
       source='pdf', use=[[1, 2, 3]], marks=[6],
       notes='The scheme prints three ways of saying it and pays six for any of them, '
             'with three for a partial answer.')

A.card(8, None, 'iv', topic='phys-2-3', concept='angle-of-refraction-from-snells-law',
       source='pdf', first_sentence=True,
       from_runs=[((8, None, 'iv'), 0, slice(12, 17)),
                  ((8, None, 'iv'), 0, slice(18, 19)),
                  ((8, None, 'iv'), 0, slice(20, 23))],
       marks=[3, 3, 3])

# 2023 OL Q3(i) and Q3(ii) are not carded. They ask for the equipment labelled
# A and B on a diagram the card cannot show (paper page 3), and the build
# refuses a card that names a lettered part without a labelled figure behind
# it. Q8(ii) and Q8(iii) are the same shape: naming A, B and C on the paper's
# glass-block ray diagram, and copying that diagram (paper page 7). All four
# wait on figure crops.
#
# Q4(v) and Q4(vi) are not carded. The paper's text layer renders the stacked
# fraction 1/l as mojibake ("the value of ଵ ௟"), so the question cannot be
# carried without typing it, which lift-never-write rules out.

A.card(7, None, 'v', topic='phys-1-4', concept='velocity-from-energy-or-suvat',
       source='pdf',
       from_runs=[((7, None, 'v'), 0, slice(0, 9)),
                  ((7, None, 'v'), 0, slice(10, 11)),
                  ((7, None, 'v'), 0, slice(12, 17))],
       marks=[3, 3, 3],
       notes='Either route scores, the energy one or the equation of motion, but a '
             'partial answer cannot be taken from both.')

A.card(8, None, 'vi', topic='phys-2-3', concept='image-position-for-a-converging-lens',
       source='pdf',
       from_runs=[((8, None, 'vi'), 0, slice(7, 12)),
                  ((8, None, 'vi'), 0, slice(13, 14)),
                  ((8, None, 'vi'), 0, slice(15, 19))],
       marks=[3, 3, 3])

A.card(11, None, 'v', topic='phys-3-3', concept='total-resistance-of-two-parallel-bulbs',
       source='pdf',
       from_runs=[((11, None, 'v'), 0, slice(9, 14)),
                  ((11, None, 'v'), 0, slice(15, 16)),
                  ((11, None, 'v'), 0, slice(17, 21))],
       marks=[3, 3, 3])

# ── Experiment questions (Section A): apparatus diagrams, graphs, results ──
# The scheme itemises what each drawing must show, so the components are
# carded per the drawing-questions-are-cardable policy.

A.card(1, None, 'i', topic='phys-u2', concept='newtons-second-law-apparatus',
       source='pdf',
       from_runs=[((1, None, 'i'), 0, slice(0, 1)),
                  ((1, None, 'i'), 0, slice(2, 3)),
                  ((1, None, 'i'), 0, slice(4, 8)),
                  ((1, None, 'i'), 0, slice(9, 13))],
       marks=[3, 3, 3, 3],
       checked='The paper prints the part mark "(12)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete.',
       notes='The scheme takes one mark off if no label is present on the diagram.')

A.card(1, None, 'iv', topic='phys-u2', concept='graph-of-force-against-acceleration',
       source='pdf',
       from_runs=[((1, None, 'iv'), 0, slice(0, 2)),
                  ((1, None, 'iv'), 0, slice(3, 5)),
                  ((1, None, 'iv'), 0, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3',
       notes='Six plotted points at one mark each.')

A.card(2, None, 'i', topic='phys-u2', concept='concave-mirror-focal-length-apparatus',
       source='pdf', from_run=((2, None, 'i'), 0, slice(0, 3)), marks=[12],
       notation='6 + 3 + 3',
       notes='The scheme takes one mark off if no label is present on the diagram.')

A.card(2, None, 'ii', topic='phys-u2', concept='marking-u-and-v-on-the-diagram',
       source='pdf',
       from_runs=[((2, None, 'ii'), 0, slice(0, 2)),
                  ((2, None, 'ii'), 0, slice(3, 5))],
       marks=[3, 3],
       checked='The paper prints the part mark "(18)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete.',
       notes='This part follows the apparatus diagram asked for in part (i).')

A.card(3, None, 'ix', topic='phys-u2', concept='specific-latent-heat-result',
       source='pdf', first_sentence=True,
       from_run=((3, None, 'viii'), 2, slice(0, 14)), marks=[6],
       notes='E = 3094.07 J is the heat lost by the water and calorimeter, calculated '
             'in part (vii); 16 °C is the rise in temperature of the ice, from part '
             '(viii). The scheme runs this answer on from part (viii) in the same '
             'block.')

A.card(4, None, 'i', topic='phys-u2', concept='speed-of-sound-apparatus',
       source='pdf', from_run=((4, None, 'i'), 0, slice(0, 11)), marks=[12],
       notation='6 + 3 + 3',
       notes='The scheme takes one mark off if no label is present on the diagram.')

A.card(4, None, 'ii', topic='phys-u2', concept='showing-the-measured-air-column-length',
       source='pdf', from_run=((4, None, 'ii'), 0, slice(0, 3)), marks=[3],
       checked='The paper prints the part mark "(15)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete.',
       notes='This part follows the apparatus diagram asked for in part (i).')

A.card(5, None, 'iii', topic='phys-u2', concept='graph-of-length-against-resistance',
       source='pdf',
       from_runs=[((5, None, 'iii'), 0, slice(0, 2)),
                  ((5, None, 'iii'), 0, slice(3, 5)),
                  ((5, None, 'iii'), 0, slice(8, 12))],
       marks=[4, 6, 3], notation='4 + 6 × 1 + 3',
       checked='The paper prints the part mark "(13)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete.',
       notes='Six plotted points at one mark each.')

A.card(6, 'd', None, topic='phys-1-4', concept='unit-of-work',
       source='pdf', card_id='phys-2023-ol-q6-d',
       from_run=((6, 'd', None), 1, slice(0, 1)), marks=[7],
       notes='The printed scheme answers this by setting joule in bold among the four '
             'options it reprints; the answer is read off the rendered page the same '
             'way a tick would be.')

A.card(7, None, 'ii', topic='phys-1-2', concept='forces-on-a-carriage-at-constant-velocity',
       source='pdf',
       from_runs=[((7, None, 'ii'), 0, slice(0, 2)),
                  ((7, None, 'ii'), 0, slice(3, 6))],
       marks=[3, 3],
       notes='The scheme takes one mark off if the arrows are clearly not equal.')

A.card(7, None, 'vii', topic='phys-1-2', concept='forces-on-a-falling-carriage',
       source='pdf', from_run=((7, None, 'vii'), 1, slice(0, 2)), marks=[6],
       notes='The scheme reprints the question above its answer; the answer is the '
             'single downward arrow, weight.')

A.card(7, None, 'viii', topic='phys-1-1', concept='velocity-time-graph-of-the-ride',
       source='pdf',
       from_runs=[((7, None, 'viii'), 0, slice(0, 2)),
                  ((7, None, 'viii'), 0, slice(3, 5)),
                  ((7, None, 'viii'), 0, slice(6, 8))],
       marks=[2, 3, 3],
       checked='The paper prints the part mark "(14)" and the question group\'s data '
               'line "acceleration due to gravity = 9.8 m s–2" after the question, so '
               'the text ends on that rather than punctuation. The question itself is '
               'complete.',
       notes='The scheme takes one mark off if an incorrect acceleration is shown.')

A.card(8, None, 'v', topic='phys-2-3', concept='ray-diagram-for-a-real-image',
       source='pdf',
       from_runs=[((8, None, 'v'), 0, slice(0, 2)),
                  ((8, None, 'v'), 0, slice(3, 8))],
       marks=[3, 9], notation='3 + 3 × 3',
       notes='Object, incident ray(s) and image formed earn three marks each.')

A.card(10, None, 'ix', topic='phys-2-4', concept='frequency-from-wave-speed-and-wavelength',
       source='pdf', from_run=((10, None, 'viii'), 1, slice(19, 25)), marks=[6],
       checked='The paper prints the part mark "(20)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The question itself '
               'is complete.',
       notes='0.9 m is the wavelength calculated in part (viii), converted from 90 cm; '
             '400 m s–1 is the wave speed given on the paper. The scheme runs this '
             'answer on from part (viii) in the same block.')

A.card(11, None, 'iv', topic='phys-3-3', concept='two-bulbs-in-parallel-circuit-diagram',
       source='pdf',
       from_runs=[((11, None, 'iv'), 0, slice(0, 2)),
                  ((11, None, 'iv'), 0, slice(3, 5))],
       marks=[3, 3])

A.card(12, None, 'iii', topic='phys-4-3', concept='labelled-diagram-of-the-atom',
       source='pdf',
       from_runs=[((12, None, 'iii'), 0, slice(15, 18)),
                  ((12, None, 'iii'), 0, slice(19, 20)),
                  ((12, None, 'iii'), 0, slice(21, 24))],
       marks=[3, 3, 3])

A.card(12, None, 'ix', topic='phys-2-4', concept='wavelength-of-an-x-ray',
       source='pdf', from_run=((12, None, 'viii'), 0, slice(58, 70)), marks=[6],
       notes='The scheme runs this answer on from part (viii) in the same block.')

A.card(13, None, 'iv', topic='phys-4-4', concept='protons-and-neutrons-in-tritium',
       source='pdf',
       from_runs=[((13, 'a', None), 0, slice(9, 10)),
                  ((13, 'b', None), 0, slice(9, 10))],
       marks=[4, 3],
       checked='The paper prints the nuclide symbol for tritium with a stacked '
               'superscript 3 and subscript 1, which the text layer flattens to '
               '"H1 3", and it prints the part mark "(7)" after the question. The '
               'question itself is complete.',
       notes='The first row is (a), the number of protons; the second row is (b), the '
             'number of neutrons.')

A.card(14, 'b', 'i', topic='phys-2-3', concept='path-of-a-ray-through-an-optical-fibre',
       source='pdf', card_id='phys-2023-ol-q14-b-i',
       from_run=((13, 'b', 'i'), 0, slice(0, 9)), marks=[6])

A.emit()
