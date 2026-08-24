#!/usr/bin/env python3
"""Physics 2025 Higher Level — the beta decay of iodine-131."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2025, 'hl')

A.card(14, 'c', 'ii', topic='phys-4-4', concept='beta-decay-equation-iodine-131',
       source='pdf', use=[1], marks=[7],
       notation='7 × 1',
       notes='The scheme pays the equation a mark per correct term and takes three off '
             'for each extra species written in.')

A.card(3, None, 'iv', topic='phys-u2', concept='speed-of-sound-from-a-graph',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3])


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(5, None, 'i', topic='phys-u2', concept='circuit-for-the-filament-bulb-experiment',
       source='pdf', use=[1, 2, 3, 4], marks=[3, 3, 3, 3])

A.card(12, 'b', 'i', topic='phys-3-6', concept='parts-of-an-ac-generator',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3], first_sentence=True)


# ── 2025 HL close-out ──────────────────────────────────────────────────────
# The scheme sets Section A/B answers in a two-column layout that the block
# parser interleaves, so most of these parts lift from a neighbouring key via
# from_runs. Every parent/point/slice below was read off the token dump first.

A.card(1, None, 'iii', topic='phys-1-2', concept='forces-on-the-metre-stick-diagram',
       source='pdf', use=[1], marks=[6], notation='6 x 1',
       figure='physics-2025-HL-paper-p02-i0',
       notes='The scheme itemises the drawing in words: six force arrows, a mark '
             'each, with the weight arrow labelled.')

A.card(1, None, 'vi', topic='phys-1-2', concept='sum-of-moments-about-an-axis',
       source='pdf',
       from_runs=[((1, 'b', None), 1, slice(0, 3)),
                  ((1, 'b', None), 1, slice(4, 8)),
                  ((1, 'b', None), 1, slice(9, 12)),
                  ((1, 'b', None), 1, slice(13, 16))],
       marks=[3, 3, 3, 3],
       figure='physics-2025-HL-paper-p02-i0',
       notes='The scheme prints the four marking points on one line under the '
             '(b) cue; the weight of the metre stick at the 50.0 cm mark counts '
             'among the clockwise moments about the 5 cm axis.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-speed-of-sound-experiment',
       source='pdf', use=[1, 2, [3, 4]], marks=[4, 4, 4],
       notes='The scheme prints "tuning fork / metre stick" as equally acceptable '
             'third components, and takes 1 mark off a diagram with no label.')

A.card(4, None, 'ii', topic='phys-u2', concept='graph-for-the-snells-law-experiment',
       source='pdf', use=[3, 4, 5, 6], marks=[3, 3, 3, 3],
       notes='The scheme prints the expected values alongside: sin i 0.342 0.500 '
             '0.643 0.766 0.866 0.940 and sin r 0.225 0.326 0.454 0.500 0.574 '
             '0.629 — the graph that shows the relationship is sin i against sin r, '
             'not i against r.')

A.card(4, None, 'iv', topic='phys-u2', concept='refractive-index-from-the-slope-of-a-graph',
       source='pdf', use=[1, 2], marks=[3, 3],
       checked='The paper prints the part mark in brackets after the question, so '
               'the text ends on a number rather than punctuation. The question '
               'itself is complete.',
       notes='The refractive index is the slope of the sin i against sin r graph '
             'drawn in part (ii).')

A.card(5, None, 'ii', topic='phys-u2', concept='graph-of-voltage-against-current-for-a-filament-bulb',
       source='pdf', use=[1, 2, 3], marks=[3, 3, 3],
       figure='physics-2025-HL-paper-p06-i0',
       notes='A curve, not a line, of best fit — the filament bulb is non-ohmic.')

A.card(5, None, 'iv', topic='phys-3-3', concept='resistance-of-the-bulb-at-two-currents',
       source='pdf',
       from_runs=[((5, 'b', None), 1, slice(0, 3)),
                  ((5, 'a', None), 1, slice(0, 4)),
                  ((5, 'b', None), 2, slice(0, 4))],
       marks=[3, 2, 2],
       figure='physics-2025-HL-paper-p06-i0',
       context='The voltages at 40 mA and at 90 mA are read off the curve plotted '
               'in the previous part from the data table.',
       notes='The scheme splits the answers under (a) 40 mA — R ≈ 43 Ω — and '
             '(b) 90 mA — R ≈ 54 Ω — around the shared formula.')

A.card(6, 'a', None, topic='phys-1-2', concept='function-of-a-hydrometer',
       source='pdf', card_id='phys-2025-hl-q6-a', stem=False,
       from_runs=[((5, 'a', None), 3, slice(0, 1)),
                  ((5, 'a', None), 4, slice(0, 2))],
       marks=[4, 3],
       notes='The scheme names no particular example — "example given" is its own '
             'wording — so any valid practical use (testing milk, battery acid, '
             'home-brewing) earns the 3.')

A.card(6, 'b', None, topic='phys-1-2', concept='forces-on-a-car-on-an-incline',
       source='pdf', card_id='phys-2025-hl-q6-b', stem=False,
       from_run=((5, 'b', None), 5, slice(0, 8)), marks=[7],
       notation='2 + 2 + 2 + 1',
       notes='The scheme takes 1 mark off a diagram with no label, and 1 off for '
             'additional incorrect forces.')

A.card(6, 'c', None, topic='phys-1-1', concept='time-for-two-projectiles-to-meet',
       source='pdf', card_id='phys-2025-hl-q6-c', stem=False,
       from_runs=[((5, 'c', None), 7, slice(0, 11)),
                  ((5, 'c', None), 8, slice(0, 11)),
                  ((5, 'c', None), 9, slice(0, 4))],
       marks=[3, 2, 2],
       context='The diagram prints the particles 20 m apart: X is projected up '
               'from the ground as Y is projected down from a point 20 m above '
               'it, with g = 9.8 m s–2.')

A.card(6, 'e', None, topic='phys-2-3', concept='ray-diagram-virtual-image-concave-mirror',
       source='pdf', card_id='phys-2025-hl-q6-e', stem=False,
       from_runs=[((5, 'e', None), 1, slice(0, 3)),
                  ((5, 'e', None), 2, slice(0, 3)),
                  ((5, 'e', None), 3, slice(0, 3))],
       marks=[3, 2, 2],
       notes='The object must sit inside the focus — that is the only placement '
             'for which a concave mirror forms a virtual image.')

A.card(6, 'h', 'i', topic='phys-2-6', concept='third-harmonic-diagram',
       source='pdf', card_id='phys-2025-hl-q6-h-i',
       from_run=((5, 'h', 'i'), 1, slice(0, 11)), marks=[4],
       notes='The scheme prints a single [4 + 3] across (h)(i) and (h)(ii); the '
             'sibling card for (h)(ii) carries the 3, so the diagram takes the 4.')

A.card(6, 'j', None, topic='phys-3-3', concept='p-n-junction-charge-regions',
       source='pdf', card_id='phys-2025-hl-q6-j', stem=False,
       from_runs=[((5, 'h', 'i'), 7, slice(0, 5)),
                  ((5, 'h', 'i'), 8, slice(0, 8))],
       marks=[4, 3], notation='4, then 1 + 1 + 1')

A.card(7, None, 'viii', topic='phys-1-6', concept='normal-reaction-on-a-person-at-the-equator',
       source='pdf', stem=False,
       from_runs=[((5, 'h', 'viii'), 0, slice(0, 3)),
                  ((5, 'h', 'viii'), 0, slice(4, 12))],
       marks=[2, 2],
       context='A person of mass 80 kg stands at the equator, rotating with a '
               'linear velocity of 463 m s–1; the centripetal force found in the '
               'previous part is 2.68 N.')

A.card(7, None, 'ix', topic='phys-1-6', concept='forces-on-a-person-at-the-equator',
       source='pdf', stem=False,
       from_run=((5, 'h', 'viii'), 0, slice(14, 19)), marks=[4],
       notation='2 + 2',
       context='A person of mass 80 kg stands at the equator of the Earth, '
               'rotating with the Earth in circular motion.',
       notes='The scheme takes 1 mark off a diagram with no label, and 1 off for '
             'additional incorrect forces.')

A.card(8, None, 'iv', topic='phys-2-6', concept='formation-of-a-diffraction-pattern',
       source='pdf',
       from_runs=[((5, 'h', 'iv'), 4, slice(0, 6)),
                  ((5, 'h', 'iv'), 5, slice(0, 2)),
                  ((5, 'h', 'iv'), 6, slice(0, 2)),
                  ((5, 'h', 'iv'), 9, slice(0, 5))],
       use=[[0, 1, 2], 3], marks=[6, 3],
       notes='The scheme separates the first three answers with a solidus, so any '
             'one of them earns the 6.')

A.card(8, None, 'vi', topic='phys-2-6', concept='maximum-number-of-diffraction-images',
       source='pdf',
       from_runs=[((5, 'h', 'vi'), 2, slice(0, 3)),
                  ((5, 'h', 'vi'), 3, slice(0, 3)),
                  ((5, 'h', 'vi'), 4, slice(0, 14))],
       marks=[3, 2, 1],
       context='d is the grating spacing found in the previous part (300 lines '
               'per mm) and λ = 691 nm.',
       notes='nmax counts orders to one side; the images are the central maximum '
             'plus four orders each side.')

A.card(9, None, 'iii', topic='phys-4-2', concept='structure-of-a-photocell',
       source='pdf',
       from_run=((5, 'b', 'iii'), 1, slice(0, 5)), marks=[9],
       notation='3 + 3 + 3',
       notes='The scheme takes 1 mark off a diagram with no label.')

A.card(10, None, 'v', topic='phys-2-1', concept='unmarked-thermometer-length-at-42-degrees',
       source='pdf', stem=False,
       from_runs=[((5, 'c', 'v'), 3, slice(30, 35)),
                  ((5, 'c', 'v'), 3, slice(39, 44)),
                  ((5, 'c', 'v'), 3, slice(48, 53)),
                  ((5, 'c', 'v'), 3, slice(59, 69))],
       marks=[3, 3, 2, 2],
       context='100 degree-units of temperature span 30.0 – 3.0 = 27 cm of '
               'mercury column.',
       notes='The scheme prints a graphical route as the // alternative at each '
             'step — axes labelled [3], points plotted [3], line of best fit [2], '
             'length ≈ 14.34 cm [2].')

A.card(11, None, 'viii', topic='phys-3-3', concept='adjusting-a-potential-divider-thermostat',
       source='pdf', stem=False,
       from_run=((12, None, 'viii'), 0, slice(24, 27)), marks=[4],
       context='Vout is taken across the thermistor. At a higher temperature the '
               'thermistor resistance is lower, so the variable resistance must '
               'be lower for Vout still to reach 8 V.',
       notes='The scheme adds: valid reference to a PTC thermistor acceptable '
             'for full marks.')

A.card(12, 'a', 'i', topic='phys-4-5', concept='cockcroft-walton-nuclear-equation',
       source='pdf', stem=False,
       from_run=((12, None, 'i'), 2, slice(0, 12)), marks=[8],
       notation='4 × 2',
       context='Cockcroft and Walton bombarded lithium nuclei with accelerated '
               'protons; each collision produced two alpha particles.',
       notes='The scheme sets the equation with raised mass and atomic numbers, '
             'which the text layer scatters after each symbol: read '
             '¹₁H + ⁷₃Li → ⁴₂He + ⁴₂He. The examiner takes 2 off for each '
             'additional incorrect species.')

A.card(12, 'a', 'vi', topic='phys-4-5', concept='verifying-mass-energy-equivalence',
       source='pdf', stem=False,
       from_runs=[((12, None, 'vi'), 2, slice(0, 6)),
                  ((12, None, 'vi'), 3, slice(0, 7)),
                  ((12, None, 'vi'), 3, slice(7, 21))],
       use=[[0, 1], 2], marks=[4, 2],
       context='The total, 2.801 × 10–12 J, agrees with the measured kinetic '
               'energy of the alpha particles, 2.77 × 10–12 J.',
       notes='The scheme separates the two references with a solidus, so either '
             'earns the 4.')

A.card(12, 'a', 'ix', topic='phys-4-5', concept='positron-emission-equation-fluorine-18',
       source='pdf',
       from_run=((12, None, 'viii'), 7, slice(0, 11)), marks=[7],
       notation='7 × 1',
       checked='The paper prints the part mark in brackets after the question, so '
               'the text ends on a number rather than punctuation. The question '
               'itself is complete.',
       notes='The scheme sets the equation with raised mass and atomic numbers, '
             'which the text layer scatters after each symbol: read '
             '¹⁸₉F → ¹⁸₈O + ⁰₊₁e. The examiner takes 3 off for each additional '
             'incorrect species.')

A.card(12, 'b', 'iii', topic='phys-3-3', concept='bridge-rectifier-for-smooth-dc',
       source='pdf', stem=False, use=[1, 2, 3], marks=[3, 3, 3],
       checked='The paper prints the part mark in brackets after the question, so '
               'the text ends on a number rather than punctuation. The question '
               'itself is complete.')

A.card(12, 'b', 'ix', topic='phys-3-3', concept='galvanometer-to-voltmeter',
       source='pdf', stem=False,
       from_runs=[((12, 'b', 'viii'), 4, slice(0, 2)),
                  ((12, 'b', 'viii'), 5, slice(0, 5))],
       marks=[3, 3],
       checked='The paper prints the part mark in brackets after the question, so '
               'the text ends on a number rather than punctuation. The question '
               'itself is complete.')

A.card(14, 'b', 'iii', topic='phys-2-3', concept='optical-fibre-signal-transmission',
       source='pdf', stem=False, first_sentence=True,
       use=[1, 2], marks=[4, 2], notation='4 + 2',
       notes='The scheme prints a single stacked [4 + 2] across the two points, '
             'so the split is order-dependent: the labelled ray diagram carries '
             'the 4.')

A.emit()
