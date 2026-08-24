#!/usr/bin/env python3
"""Physics 2022 OL — parts the deck had not carded.

Physics answers only trace through the PDF scheme, so every card here reads
source='pdf'.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2022, 'ol')

A.card(2, None, 'v', topic='phys-u2', concept='average-refractive-index-from-results',
       source='pdf',
       from_runs=[((2, None, 'v'), 0, slice(0, 12)),
                  ((2, None, 'v'), 0, slice(13, 18))],
       marks=[3, 3],
       notes='Either route scores: an average of the calculated values, or the slope of '
             'a graph of sin i against sin r.')

A.card(5, None, 'v', topic='phys-u2', concept='reading-a-current-off-a-graph',
       source='pdf',
       from_runs=[((5, None, 'v'), 0, slice(0, 5)),
                  ((5, None, 'v'), 0, slice(6, 10))],
       marks=[3, 3])

A.card(7, None, 'ii', topic='phys-u5', concept='converting-minutes-to-seconds',
       source='pdf', from_run=((7, None, 'ii'), 0, slice(0, 6)), marks=[6])

A.card(9, None, 'iv', topic='phys-2-3', concept='image-position-from-the-lens-formula',
       source='pdf',
       from_runs=[((9, None, 'iv'), 0, slice(0, 5)),
                  ((9, None, 'iv'), 0, slice(6, 7)),
                  ((9, None, 'iv'), 0, slice(8, 12))],
       marks=[6, 3, 3])

A.card(14, 'a', 'iv', topic='phys-1-4', concept='kinetic-energy-of-a-thrown-stone',
       source='pdf', from_run=((14, 'a', 'iv'), 0, slice(0, 8)), marks=[5])

A.card(14, 'a', 'v', topic='phys-1-4', concept='maximum-height-from-kinetic-energy',
       source='pdf', from_run=((14, 'a', 'v'), 0, slice(0, 8)), marks=[5],
       notes='The scheme accepts the suvat route as well.')

A.card(2, None, 'vi', topic='phys-u2', concept='whether-the-results-verify-snells-law',
       source='pdf',
       from_runs=[((2, None, 'vi'), 0, slice(0, 6)),
                  ((2, None, 'vi'), 0, slice(7, 18))],
       marks=[3, 3])


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(5, None, 'iv', topic='phys-u2', concept='plotting-current-squared-against-temperature-rise',
       source='pdf',
       from_runs=[((5, None, 'iv'), 0, slice(0, 2)),
                  ((5, None, 'iv'), 0, slice(3, 8)),
                  ((5, None, 'iv'), 0, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3')

A.card(7, None, 'vii', topic='phys-1-2', concept='forces-on-a-train-at-constant-speed',
       source='pdf', from_run=((7, None, 'vii'), 0, slice(0, 3)), marks=[9],
       notes='The scheme takes a mark off for each of the four forces left out.')

A.card(1, None, 'ii', topic='phys-u2', concept='what-distance-was-measured-on-the-tape',
       source='pdf', use=[[0, 1, 2]], marks=[3])

A.card(3, None, 'ii', topic='phys-u2', concept='what-length-of-string-was-measured',
       source='pdf', use=[[0, 1]], marks=[3])

A.card(3, None, 'viii', topic='phys-u2', concept='graph-of-frequency-against-one-over-length',
       source='pdf',
       from_runs=[((3, None, 'viii'), 1, slice(0, 2)),
                  ((3, None, 'viii'), 1, slice(3, 5)),
                  ((3, None, 'viii'), 1, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3', checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(9, None, 'ii', topic='phys-2-3', concept='ray-diagram-for-a-magnified-image-ol',
       source='pdf',
       from_runs=[((9, None, 'ii'), 1, slice(0, 3)),
                  ((9, None, 'ii'), 1, slice(4, 7)),
                  ((9, None, 'ii'), 1, slice(8, 11))],
       marks=[5, 2, 2])

A.card(9, None, 'vii', topic='phys-2-3', concept='which-side-of-a-convex-mirror-reflects',
       source='pdf',
       from_runs=[((9, None, 'vii'), 2, slice(0, 1)),
                  ((9, None, 'vii'), 2, slice(2, 3))],
       marks=[3, 3], first_sentence=True)

# ── The remaining open parts, closed 2026-08-24 ────────────────────────────
# Q8(i), Q8(ii) are not here: the ask is to explain marked regions X and Y of
# the heating-curve graph, the paper block for Q8 is the flattened drawing
# ("gas Y Temperature X melting solid Heat added"), and no verified figure for
# it exists yet — they need the graph cropped from page 7 of the paper.
# Q14(c)(i), (ii) and (iv) are the same shape: the forces and their positions
# live only in the metre-stick drawing on page 14, which no verified figure
# carries either.
MARK = ('The paper prints the part mark in brackets after the question, so the text '
        'ends on a number rather than punctuation. The question itself is complete.')

A.card(1, None, 'i', topic='phys-u2', concept='apparatus-to-measure-constant-velocity',
       source='pdf',
       from_runs=[((1, None, 'i'), 0, slice(0, 1)),
                  ((1, None, 'i'), 1, slice(0, 1)),
                  ((1, None, 'i'), 1, slice(1, 2)),
                  ((1, None, 'i'), 2, slice(0, 1)),
                  ((1, None, 'i'), 2, slice(1, 2)),
                  ((1, None, 'i'), 3, slice(0, 1)),
                  ((1, None, 'i'), 4, slice(0, 1))],
       use=[[0, 1], [2, 3], [4, 5, 6]], marks=[6, 3, 3], notation='6 + 3 + 3',
       checked=MARK,
       notes='Either of each line\'s alternatives scores; the scheme takes a mark off '
             'if the diagram carries no labels.')

A.card(2, None, 'i', topic='phys-u2', concept='apparatus-to-verify-snells-law',
       source='pdf',
       from_runs=[((2, None, 'i'), 0, slice(0, 2)),
                  ((2, None, 'i'), 0, slice(2, 3)),
                  ((2, None, 'i'), 1, slice(0, 1)),
                  ((2, None, 'i'), 2, slice(0, 1)),
                  ((2, None, 'i'), 2, slice(1, 8))],
       use=[[0], [1, 2, 3], [4]], marks=[6, 3, 3], notation='6 + 3 + 3',
       notes='Any of the second line\'s alternatives scores; the scheme takes a mark '
             'off if the diagram carries no labels.')

A.card(2, None, 'ii', topic='phys-u2', concept='labelling-the-angles-measured',
       source='pdf', use=[0], marks=[6], checked=MARK)

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-stretched-string-experiment',
       source='pdf',
       from_runs=[((3, None, 'i'), 0, slice(0, 1)),
                  ((3, None, 'i'), 1, slice(0, 2)),
                  ((3, None, 'i'), 1, slice(3, 13))],
       use=[[0, 1], [2]], marks=[3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(3, None, 'vii', topic='phys-u2', concept='completing-the-table-of-one-over-length',
       source='pdf', from_run=((3, None, 'vii'), 1, slice(3, 9)), marks=[6],
       notation='6 × 1', notes='One mark for each of the six 1/l values.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-specific-heat-capacity-experiment',
       source='pdf', from_run=((4, None, 'i'), 0, slice(0, 16)), marks=[9],
       notation='any 3 × 3',
       notes='Any three of the scheme\'s list score three marks each; the scheme takes '
             'a mark off if the diagram carries no labels.')

A.card(4, None, 'iii', topic='phys-u2', concept='mass-of-the-water-from-the-results',
       source='pdf', use=[0], marks=[6])

A.card(4, None, 'iv', topic='phys-u2', concept='temperature-rise-of-the-calorimeter-and-water',
       source='pdf', use=[0], marks=[6], checked=MARK)

A.card(4, None, 'vi', topic='phys-u2', concept='specific-heat-capacity-from-the-results',
       source='pdf',
       from_runs=[((4, None, 'vi'), 0, slice(0, 13)),
                  ((4, None, 'vi'), 0, slice(18, 24))],
       marks=[10, 2], notation='6 + 2 + 2 + 2',
       notes='The scheme\'s note: heat energy added = heat energy gained by water + '
             'calorimeter. The paper supplies the specific heat capacity of copper, '
             '390 J kg–1 K–1.')

A.card(5, None, 'i', topic='phys-u2', concept='apparatus-for-the-joules-law-experiment',
       source='pdf', from_run=((5, None, 'i'), 0, slice(0, 15)), marks=[9],
       notation='any 3 × 3',
       notes='Any three of the scheme\'s list score three marks each; the scheme takes '
             'a mark off if the diagram carries no labels.')

A.card(5, None, 'iii', topic='phys-u2', concept='completing-the-table-of-current-squared',
       source='pdf', from_run=((5, None, 'iii'), 1, slice(2, 8)), marks=[6],
       notation='6 × 1', checked=MARK,
       notes='One mark for each of the six I² values.')

A.card(6, 'd', None, topic='phys-2-3', concept='light-through-an-optical-fibre',
       source='pdf', card_id='phys-2022-ol-q6-d',
       from_run=((6, 'd', None), 0, slice(0, 4)), marks=[7],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(7, None, 'ix', topic='phys-1-1', concept='speed-time-graph-for-the-train',
       source='pdf',
       from_runs=[((7, None, 'viii'), 4, slice(0, 2)),
                  ((7, None, 'viii'), 4, slice(3, 5))],
       marks=[2, 6], checked=MARK,
       notes='For the shape, the scheme accepts a partial answer for 3 of the 6 marks.')

A.card(8, None, 'viii', topic='phys-2-1', concept='experiment-to-calibrate-a-thermometer',
       source='pdf', stem=False,
       from_runs=[((8, None, 'viii'), 0, slice(0, 2)),
                  ((8, None, 'viii'), 0, slice(3, 5)),
                  ((8, None, 'viii'), 0, slice(6, 9)),
                  ((8, None, 'viii'), 0, slice(10, 11))],
       marks=[3, 3, 3, 3], checked=MARK,
       notes='The scheme prints no detail for the method, and takes a mark off if the '
             'diagram carries no labels.')

A.card(10, None, 'i', topic='phys-2-5', concept='experiment-to-show-sound-is-a-mechanical-wave',
       source='pdf',
       from_runs=[((10, None, 'i'), 0, slice(11, 18)),
                  ((10, None, 'i'), 0, slice(19, 28)),
                  ((10, None, 'i'), 0, slice(29, 36)),
                  ((10, None, 'i'), 0, slice(37, 38))],
       marks=[3, 3, 3, 3],
       notes='The scheme prints no detail for the observation.')

A.card(10, None, 'iv', topic='phys-2-6', concept='experiment-to-show-sound-interference',
       source='pdf',
       from_runs=[((10, None, 'iv'), 0, slice(0, 8)),
                  ((10, None, 'iv'), 0, slice(9, 15)),
                  ((10, None, 'iv'), 0, slice(16, 17))],
       marks=[3, 3, 3],
       notes='The scheme prints no detail for the observation.')

A.card(10, None, 'vii', topic='phys-2-5', concept='first-position-of-resonance-in-a-pipe',
       source='pdf', from_run=((10, None, 'vii'), 0, slice(0, 13)), marks=[6],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(11, None, 'iii', topic='phys-3-3', concept='circuit-diagram-of-a-torch',
       source='pdf',
       from_runs=[((11, None, 'iii'), 0, slice(34, 36)),
                  ((11, None, 'iii'), 0, slice(39, 42))],
       marks=[3, 3], notation='3 × 1 + 3',
       checked='The question ends on the paper\'s own parenthetical pointer to the '
               'circuit symbols in the Formulae and Tables booklet, so the block ends '
               'on a closing bracket. The question itself is complete.',
       notes='One mark for each of the three component symbols.')

A.card(11, None, 'viii', topic='phys-3-3', concept='resistance-of-two-wires-in-parallel',
       source='pdf',
       from_runs=[((11, None, 'viii'), 0, slice(10, 15)),
                  ((11, None, 'viii'), 0, slice(16, 17)),
                  ((11, None, 'viii'), 0, slice(18, 22))],
       marks=[3, 3, 3])

A.card(12, None, 'ii', topic='phys-4-2', concept='experiment-to-demonstrate-the-photoelectric-effect',
       source='pdf',
       from_runs=[((12, None, 'ii'), 0, slice(0, 7)),
                  ((12, None, 'ii'), 0, slice(8, 9)),
                  ((12, None, 'ii'), 0, slice(10, 11))],
       marks=[3, 3, 3],
       notes='The scheme prints no detail for the method or the observation.')

A.card(12, None, 'iv', topic='phys-4-2',
       concept='wavelength-and-photon-energy-at-the-threshold-frequency',
       source='pdf',
       from_runs=[((12, 'a', None), 0, slice(0, 12)),
                  ((12, 'b', None), 0, slice(0, 12))],
       marks=[6, 6],
       checked='The paper\'s block runs on into the X-ray introduction that follows '
               'the part, so the text ends mid-narrative. The (a) and (b) asks '
               'themselves are complete.',
       notes='The first row answers (a), the second answers (b).')

A.card(13, None, 'v', topic='phys-1-5', concept='acceleration-due-to-gravity-on-the-moon',
       source='pdf', from_run=((13, None, 'v'), 0, slice(10, 25)), marks=[7],
       checked=MARK, stem=False)

A.card(14, 'd', 'ii', topic='phys-4-4', concept='experiment-to-compare-penetrating-powers',
       source='pdf', stem=False,
       from_runs=[((4, 'd', 'ii'), 0, slice(15, 20)),
                  ((4, 'd', 'ii'), 0, slice(21, 24)),
                  ((4, 'd', 'ii'), 0, slice(25, 26)),
                  ((4, 'd', 'ii'), 0, slice(27, 28)),
                  ((4, 'd', 'ii'), 1, slice(0, 1))],
       use=[[0], [1], [2], [3, 4]], marks=[3, 3, 3, 3],
       notes='The scheme prints no detail for the method; the fourth mark\'s '
             'observation may instead be made with a detector.')

A.emit()
