#!/usr/bin/env python3
"""Physics 2022 Higher Level — the net force part of the equilibrium experiment.

The two nuclear-equation parts of Question 10 are not here: the scheme sets
them in a bold font the text layer reads as doubled letters, so the equation
comes out as a run of repeated characters rather than nuclide symbols. They are
in the same class as the Chemistry formulae already recorded as font-mangled.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2022, 'hl')

A.card(1, None, 'vii', topic='phys-u2', concept='net-vertical-force-on-a-metre-stick',
       source='pdf', use=[0], marks=[3],
       notes='The scheme keeps "[upwards]" on the answer — the direction is part of it.')

A.card(11, None, 'i', topic='phys-2-1', concept='heat-capacity-and-specific-heat-capacity',
       source='pdf',
       from_runs=[((11, None, 'i'), 0, slice(12, 25)),
                  ((11, None, 'i'), 0, slice(27, 41))],
       marks=[3, 3],
       notes='Each definition may be given in words or as the formula beside it, which is '
             'what the scheme\'s solidus separates.')

A.card(14, 'd', 'i', topic='phys-3-6', concept='laws-of-electromagnetic-induction',
       source='pdf', first_sentence=True,
       from_runs=[((14, 'd', 'i'), 0, slice(0, 6)),
                  ((14, 'd', 'i'), 0, slice(7, 16)),
                  ((14, 'd', 'i'), 0, slice(17, 21)),
                  ((14, 'd', 'i'), 0, slice(22, 32))],
       marks=[3, 3, 3, 3])

A.card(1, None, 'vi', topic='phys-u2', concept='net-moment-about-a-point',
       source='pdf',
       from_runs=[((1, None, 'vi'), 0, slice(0, 15)),
                  ((1, None, 'vi'), 0, slice(16, 27)),
                  ((1, None, 'vi'), 0, slice(28, 35))],
       marks=[3, 3, 3])

A.card(3, None, 'iv', topic='phys-u2', concept='refractive-index-from-a-slope',
       source='pdf',
       from_runs=[((3, None, 'iv'), 0, slice(0, 2)),
                  ((3, None, 'iv'), 0, slice(3, 6))],
       marks=[3, 3])


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(3, None, 'iii', topic='phys-u2', concept='graph-to-verify-snells-law',
       source='pdf',
       from_runs=[((3, None, 'iii'), 0, slice(0, 7)),
                  ((3, None, 'iii'), 2, slice(0, 2)),
                  ((3, None, 'iii'), 2, slice(3, 6)),
                  ((3, None, 'iii'), 2, slice(7, 11))],
       marks=[3, 3, 3, 3],
       notes='Snell\'s law is verified against the sines, not the angles, so the first '
             'mark is for working those out before plotting anything.')

A.card(5, None, 'iii', topic='phys-u2', concept='graph-to-verify-joules-law',
       source='pdf',
       from_runs=[((5, None, 'iii'), 0, slice(0, 3)),
                  ((5, None, 'iii'), 3, slice(0, 2)),
                  ((5, None, 'iii'), 3, slice(3, 6)),
                  ((5, None, 'iii'), 3, slice(7, 11))],
       marks=[3, 3, 3, 3])

A.card(9, 'a', 'i', topic='phys-3-1', concept='electric-field-around-a-charged-sphere',
       source='pdf',
       from_runs=[((8, 'a', 'i'), 0, slice(0, 4)),
                  ((8, 'a', 'i'), 0, slice(5, 10))],
       marks=[3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme numbers this answer under its own Question 8 while the paper '
             'prints Question 9.')

A.card(12, 'b', 'ii', topic='phys-3-5', concept='parts-of-a-moving-coil-galvanometer',
       source='pdf',
       from_runs=[((12, 'b', 'ii'), 0, slice(0, 1)),
                  ((12, 'b', 'ii'), 0, slice(2, 3)),
                  ((12, 'b', 'ii'), 0, slice(4, 7)),
                  ((12, 'b', 'ii'), 0, slice(8, 11))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(12, 'b', 'iv', topic='phys-3-3', concept='converting-a-galvanometer-to-an-ammeter',
       source='pdf',
       from_runs=[((12, 'b', 'iv'), 0, slice(0, 3)),
                  ((12, 'b', 'iv'), 0, slice(4, 8))],
       marks=[3, 3])

A.card(12, 'b', 'v', topic='phys-3-3', concept='converting-a-galvanometer-to-an-ohmmeter',
       source='pdf',
       from_runs=[((12, 'b', 'v'), 0, slice(0, 6)),
                  ((12, 'b', 'v'), 0, slice(7, 9))],
       marks=[3, 3])

A.card(1, None, 'iii', topic='phys-u2', concept='applying-vertical-forces-to-a-metre-stick',
       source='pdf',
       from_runs=[((1, None, 'iii'), 0, slice(0, 4)),
                  ((1, None, 'iii'), 1, slice(0, 6))],
       marks=[2, 2], notes='The scheme takes a mark off if the diagram carries no labels.')

# The paper indexes this part as Q13(iii) — its (a), (b), (c) letters sit
# inside part (ii), not around it — so the card is keyed to (13, None, 'iii')
# and keeps the id it shipped under.
A.card(13, None, 'iii', topic='phys-2-3', concept='ray-diagram-for-a-virtual-image',
       source='pdf', card_id='phys-2022-hl-q13c-iii',
       from_runs=[((12, 'c', 'iii'), 0, slice(15, 17)),
                  ((12, 'c', 'iii'), 0, slice(18, 22))],
       marks=[2, 2],
       checked='The paper prints the part mark "(7)" after the question, so the text '
               'ends on a bracketed number rather than punctuation. The sentence about '
               'Huygens\' telescope in front of it is the question\'s own setup.',
       notes='The scheme numbers this answer under its own Question 12 while the paper '
             'prints Question 13. The object must be inside the focal point — that is '
             'what makes the image virtual.')

A.card(14, 'a', 'ii', topic='phys-u2', concept='apparatus-for-the-resultant-of-two-vectors',
       source='pdf',
       from_runs=[((14, 'a', 'ii'), 0, slice(0, None)),
                  ((14, 'a', 'ii'), 2, slice(0, 2)),
                  ((14, 'a', 'ii'), 2, slice(3, 5))],
       marks=[2, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.',
       notes='The scheme also allows three systems of weights and pulleys in place of '
             'the newtonmeters.')

A.card(11, None, 'iv', topic='phys-2-4', concept='drawing-the-third-harmonic-hl',
       source='pdf',
       from_runs=[((11, None, 'iv'), 0, slice(0, 4)),
                  ((11, None, 'iv'), 0, slice(4, 6))],
       marks=[4, 2], notation='4 + 2')

A.card(14, 'b', 'ii', topic='phys-2-5', concept='how-the-doppler-effect-arises',
       source='pdf',
       from_runs=[((14, 'b', 'ii'), 0, slice(0, 5)),
                  ((14, 'b', 'ii'), 0, slice(6, 13)),
                  ((14, 'b', 'ii'), 0, slice(14, 20))],
       marks=[3, 3, 3], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')


# ── The 2022 backlog: the experiment questions' diagrams and graphs ────────
A.card(2, None, 'ii', topic='phys-u2', concept='apparatus-to-verify-boyles-law',
       source='pdf',
       from_runs=[((2, None, 'ii'), 0, slice(0, 4)),
                  ((2, None, 'ii'), 0, slice(5, 11)),
                  ((2, None, 'ii'), 0, slice(12, 20))],
       marks=[3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(2, None, 'iv', topic='phys-u2', concept='graph-to-verify-boyles-law',
       source='pdf',
       from_runs=[((2, None, 'iv'), 0, slice(0, 5)),
                  ((2, None, 'iv'), 3, slice(0, 2)),
                  ((2, None, 'iv'), 3, slice(3, 6)),
                  ((2, None, 'iv'), 3, slice(7, 11))],
       marks=[3, 3, 3, 3],
       notes='Boyle’s law is verified against a reciprocal — a straight line '
             'needs p plotted against 1/l, or l against 1/p — so the first mark is '
             'for working those values out before plotting anything.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-to-verify-snells-law',
       source='pdf',
       from_runs=[((3, None, 'i'), 0, slice(0, 2)),
                  ((3, None, 'i'), 0, slice(3, 5)),
                  ((3, None, 'i'), 1, slice(0, 1)),
                  ((3, None, 'i'), 2, slice(0, 1)),
                  ((3, None, 'i'), 2, slice(2, 7))],
       use=[0, [1, 2, 3], 4], marks=[3, 3, 3],
       notes='The scheme’s solidus offers ray box, laser or pins as the one '
             'mark. It takes a mark off if the diagram carries no labels.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-to-measure-the-speed-of-sound',
       source='pdf',
       from_runs=[((4, None, 'i'), 0, slice(0, 1)),
                  ((4, None, 'i'), 0, slice(2, 6)),
                  ((4, None, 'i'), 0, slice(7, 11)),
                  ((4, None, 'i'), 0, slice(12, 14))],
       marks=[3, 3, 3, 3],
       notes='The scheme takes a mark off if the diagram carries no labels.')

A.card(4, None, 'iv', topic='phys-u2', concept='speed-of-sound-from-a-slope',
       source='pdf',
       from_runs=[((4, None, 'iv'), 0, slice(0, 2)),
                  ((4, None, 'iv'), 0, slice(3, 12))],
       marks=[3, 3],
       notes='The slope of the l against 1/f graph is a quarter of the wavelength–'
             'frequency constant — the slope here is 85, so the scheme multiplies '
             'it by 4 to reach c.')

A.card(5, None, 'i', topic='phys-u2', concept='apparatus-for-the-joules-law-experiment',
       source='pdf',
       from_runs=[((5, None, 'i'), 0, slice(0, 2)),
                  ((5, None, 'i'), 0, slice(3, 5)),
                  ((5, None, 'i'), 1, slice(0, 1)),
                  ((5, None, 'i'), 1, slice(2, 5)),
                  ((5, None, 'i'), 1, slice(6, 7))],
       use=[0, [1, 2], 3, 4], marks=[3, 3, 3, 3],
       notes='The scheme’s solidus allows power supply or battery. It takes a '
             'mark off if the diagram carries no labels.')

A.card(5, None, 'iv', topic='phys-u2', concept='slope-of-the-joules-law-graph',
       source='pdf',
       from_runs=[((5, None, 'iv'), 0, slice(0, 2)),
                  ((5, None, 'iv'), 0, slice(3, 9))],
       marks=[3, 3])

A.card(5, None, 'v', topic='phys-u2', concept='specific-heat-capacity-of-olive-oil',
       source='pdf', first_sentence=True,
       from_runs=[((5, None, 'v'), 1, slice(0, 1)),
                  ((5, None, 'v'), 2, slice(0, 1)),
                  ((5, None, 'v'), 2, slice(2, 8))],
       use=[[0, 1], 2], marks=[4, 3],
       notes='The scheme’s solidus offers the energy formula either way — mcΔθ '
             'or I2Rt. In the substitution, 180 s is the three minutes of heating '
             'and 0.35 kg the mass of the oil.')

A.card(6, 'c', None, topic='phys-1-2', concept='forces-on-a-floating-object',
       source='pdf', card_id='phys-2022-hl-q6-c',
       from_runs=[((6, 'c', None), 0, slice(0, 3)),
                  ((6, 'c', None), 0, slice(3, 6)),
                  ((6, 'c', None), 0, slice(9, 14))],
       marks=[3, 2, 2],
       notation='3 + 2 for the two labelled forces, 2 for equal and opposite',
       notes='The wood is at rest, so the two force vectors must be drawn equal '
             'and opposite.')

A.card(7, None, 'ix', topic='phys-1-6',
       concept='forces-at-minimum-tension-in-a-vertical-circle',
       source='pdf', first_sentence=True, stem=False,
       from_runs=[((7, 'a', 'viii'), 2, slice(42, 45)),
                  ((7, 'a', 'viii'), 2, slice(46, 49))],
       marks=[2, 2],
       notes='The object is rotating in a vertical circle on a string, so at minimum '
             'tension both forces act downwards. The scheme takes 2 marks off for '
             'each additional incorrect force, ignores references to centripetal '
             'force, and 1 mark off if the diagram carries no labels.')

A.card(8, None, 'v', topic='phys-3-3', concept='charge-distribution-in-a-p-n-junction',
       source='pdf', first_sentence=True, stem=False,
       from_runs=[((8, None, 'v'), 0, slice(0, 8)),
                  ((8, None, 'v'), 0, slice(9, 17)),
                  ((8, None, 'v'), 0, slice(18, 21))],
       marks=[2, 2, 2])

A.card(8, None, 'vi', topic='phys-3-3', concept='diode-in-forward-bias-circuit',
       source='pdf', stem=False,
       from_runs=[((8, None, 'vi'), 0, slice(0, 4)),
                  ((8, None, 'vi'), 0, slice(5, 8))],
       marks=[3, 3],
       notes='“This arrangement” is the one the question describes: a variable '
             'voltage applied across a diode held in forward bias.')

A.card(8, None, 'vii', topic='phys-3-3', concept='current-voltage-graph-for-a-diode',
       source='pdf', stem=False,
       from_runs=[((8, None, 'vii'), 5, slice(6, 8)),
                  ((8, None, 'vii'), 5, slice(9, 11)),
                  ((8, None, 'vii'), 5, slice(12, 15))],
       marks=[3, 3, 3],
       notes='The arrangement is a variable voltage across a diode in forward bias; '
             'the question’s own preamble says the depletion layer breaks down as '
             'the junction voltage is reached, which is what the correct shape shows.')

# The paper's stimulus between Q9(b)(i) and (ii) describes the parallel-plate
# capacitor that part (ii) is about, so it is not attached here.
A.card(9, 'b', 'i', topic='phys-3-2',
       concept='demonstrating-that-a-capacitor-stores-energy',
       source='pdf', stem=False,
       from_runs=[((8, 'b', 'i'), 0, slice(0, 7)),
                  ((8, 'b', 'i'), 0, slice(8, 15)),
                  ((8, 'b', 'i'), 0, slice(16, 17))],
       marks=[4, 4, 4],
       notes='The scheme numbers this answer under its own Question 8 while the '
             'paper prints Question 9. It spells out the two halves of the method '
             'but leaves the observation itself unspecified.')

A.card(12, 'a', 'i', topic='phys-4-5', concept='cockcroft-and-walton-apparatus',
       source='pdf',
       from_runs=[((12, 'a', 'i'), 0, slice(0, 3)),
                  ((12, 'a', 'i'), 0, slice(4, 10)),
                  ((12, 'a', 'i'), 0, slice(11, 14)),
                  ((12, 'a', 'i'), 0, slice(15, 16))],
       marks=[3, 3, 3, 3],
       notes='“Their apparatus” is Cockcroft and Walton’s: the question’s '
             'preamble has them accelerating protons through 70 kV into lithium metal.')

A.card(12, 'a', 'vi', topic='phys-4-5',
       concept='mass-lost-in-the-cockcroft-walton-interaction',
       source='pdf',
       from_runs=[((12, 'a', 'v'), 0, slice(34, 42)),
                  ((12, 'a', 'v'), 0, slice(43, 51))],
       marks=[3, 3],
       checked='The paper sets this part as an item under a single “Calculate” '
               'cue, so its text is a clause ending in a comma. The page was opened; '
               'the clause is the complete printed ask.',
       notes='An item of the paper’s “Calculate” list covering (v)–(viii). '
             'The masses in the substitution are lithium–7, hydrogen and helium–4 '
             'in u, from the Formulae and Tables booklet.')

A.card(12, 'a', 'viii', topic='phys-4-5',
       concept='speed-of-the-alpha-particles-formed',
       source='pdf', first_sentence=True,
       from_runs=[((12, 'a', 'v'), 2, slice(0, 3)),
                  ((12, 'a', 'v'), 2, slice(4, 11))],
       marks=[3, 3],
       notes='An item of the paper’s “Calculate” list covering (v)–(viii); '
             'the energy produced in part (vii) is shared between the two alpha '
             'particles formed.')

A.emit()
