#!/usr/bin/env python3
"""Physics 2025 Ordinary Level — the case for fusion over fission.

The scheme numbers its answer sections independently of the paper, so this
part's answers sit under its Question 11 while the paper prints Question 12.
from_run names the scheme's key rather than the paper's for that reason.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import Author  # noqa: E402

A = Author('physics', 2025, 'ol')

A.card(12, 'b', 'vii', topic='phys-4-6', concept='advantage-of-fusion-over-fission',
       source='pdf', from_run=((11, 'b', 'vii'), 1, slice(0, 5)), marks=[3],
       row_kind='criterion',
       checked='The paper prints the part mark "(36)" for the whole question after this '
               'part, so the text ends on a number and a page footer. The question itself '
               'is complete.')

A.card(8, None, 'vii', topic='phys-2-3', concept='why-sound-diffracts-and-light-does-not',
       source='pdf', from_run=((8, None, 'vii'), 2, slice(0, 3)), marks=[4],
       row_kind='criterion')


# ── Drawing questions whose scheme says what the drawing must show ─────────
A.card(2, None, 'v', topic='phys-u2', concept='plotting-one-over-pressure-against-volume',
       source='pdf',
       from_runs=[((2, None, 'v'), 2, slice(0, 2)),
                  ((2, None, 'v'), 2, slice(3, 5)),
                  ((2, None, 'v'), 2, slice(8, 12))],
       marks=[3, 6, 3], notation='3 + 6 × 1 + 3')

A.card(7, None, 'viii', topic='phys-1-2', concept='forces-on-a-skydiver-at-constant-velocity',
       source='pdf',
       from_runs=[((7, None, 'viii'), 1, slice(10, 12)),
                  ((7, None, 'viii'), 1, slice(13, 15)),
                  ((7, None, 'viii'), 1, slice(16, 19))],
       marks=[2, 2, 2], checked='The paper prints the part mark in brackets after the question, so the text ends on a number rather than punctuation. The question itself is complete.')

A.card(9, None, 'ii', topic='phys-2-3', concept='ray-diagram-for-a-real-image',
       source='pdf',
       from_runs=[((9, None, 'ii'), 0, slice(0, 3)),
                  ((9, None, 'ii'), 0, slice(4, 7)),
                  ((9, None, 'ii'), 0, slice(8, 11)),
                  ((9, None, 'ii'), 0, slice(12, 18))],
       marks=[3, 3, 3, 2])


# ── Section A apparatus diagrams: the scheme names every creditable item ───
A.card(1, None, 'i', topic='phys-u2', concept='apparatus-for-the-momentum-experiment',
       source='pdf',
       from_runs=[((1, None, 'i'), 1, slice(0, 3)),    # runway // airtrack
                  ((1, None, 'i'), 1, slice(4, 9)),    # two trolleys // two riders
                  ((1, None, 'i'), 1, slice(10, 11)),  # timer
                  ((1, None, 'i'), 2, slice(0, 2)),    # metre stick
                  ((1, None, 'i'), 3, slice(0, 2)),    # mass balance
                  ((1, None, 'i'), 3, slice(3, 6))],   # means of coalescence
       use=[[0], [1], [2, 3, 4], [5]], marks=[3, 3, 3, 3],
       notes="The scheme's third line reads 'timer / metre stick / mass balance' — "
             'any one measuring instrument takes that mark. The scheme also notes '
             '-1 if no label is present on the diagram.')

A.card(2, None, 'i', topic='phys-u2', concept='apparatus-for-the-boyles-law-experiment',
       source='pdf', from_run=((2, None, 'i'), 1, slice(0, 16)), marks=[9],
       notation='6 + 3',
       notes="The marking point is the scheme's own 'any two of' list — the first "
             'feature drawn takes 6, the second takes 3. The scheme also notes -1 '
             'if no label is present on the diagram.')

A.card(3, None, 'i', topic='phys-u2', concept='apparatus-for-the-refractive-index-experiment',
       source='pdf',
       from_runs=[((3, None, 'i'), 1, slice(0, 1)),   # block
                  ((3, None, 'i'), 1, slice(2, 4)),   # ray box
                  ((3, None, 'i'), 2, slice(0, 1)),   # laser
                  ((3, None, 'i'), 3, slice(0, 1)),   # pins
                  ((3, None, 'i'), 3, slice(2, 7))],  # detail: ruler, protractor...
       use=[[0], [1, 2, 3], [4]], marks=[3, 3, 3],
       notes="The scheme's second line reads 'ray box / laser / pins' — any one "
             'way of marking the rays takes that mark. The scheme also notes -1 '
             'if no label is present on the diagram.')

A.card(3, None, 'ii', topic='phys-u2', concept='labelling-the-rays-and-the-normal',
       source='pdf',
       from_runs=[((3, None, 'ii'), 1, slice(0, 2)),   # incident ray
                  ((3, None, 'ii'), 1, slice(3, 5)),   # refracted ray
                  ((3, None, 'ii'), 1, slice(6, 7))],  # normal
       marks=[3, 3, 3],
       notes='The scheme also notes -1 if no label is present on the diagram.')

A.card(4, None, 'i', topic='phys-u2', concept='apparatus-for-the-latent-heat-experiment',
       source='pdf',
       from_runs=[((4, None, 'i'), 1, slice(0, 1)),    # calorimeter
                  ((4, None, 'i'), 1, slice(2, 3)),    # water
                  ((4, None, 'i'), 1, slice(4, 6)),    # steam generator
                  ((4, None, 'i'), 1, slice(7, 8)),    # thermometer
                  ((4, None, 'i'), 2, slice(0, 2)),    # mass balance
                  ((4, None, 'i'), 2, slice(3, 11))],  # detail: lagging, lid...
       use=[[0], [1], [2], [3, 4], [5]], marks=[3, 3, 3, 3, 2],
       notes="The scheme's fourth line reads 'thermometer / mass balance' — either "
             'instrument takes that mark. The scheme also notes -1 if no label is '
             'present on the diagram.')


# ── Section A table completions: the scheme prints the finished table ──────
A.card(2, None, 'iv', topic='phys-u2', concept='completing-the-one-over-pressure-table',
       source='pdf', from_run=((2, None, 'iv'), 2, slice(5, 8)), marks=[6],
       notation='3 × 2',
       notes='The scheme prints the completed 1/p row of the table and prices the '
             'three new values at 3 × 2; the first three values are given in the '
             "paper's own table, which the stem carries.")

A.card(3, None, 'iv', topic='phys-u2', concept='completing-the-sine-table',
       source='pdf',
       from_runs=[((3, None, 'iii'), 4, slice(4, 5)),   # n for i = 20°
                  ((3, None, 'iii'), 5, slice(2, 5)),   # sin i, sin r, n for 46°
                  ((3, None, 'iii'), 6, slice(2, 5))],  # sin i, sin r, n for 61°
       marks=[1, 3, 3], notation='2 × 1 + 2 × 1 + 3 × 1',
       notes='The scheme prints the completed table and prices each missing value '
             'at one mark — sin i values (2 × 1), sin r values (2 × 1), '
             'sin i / sin r values (3 × 1). The rows here group the lifted values '
             'by table row: first the n value for i = 20°, then sin i, sin r and '
             'n for i = 46° and for i = 61°.')

A.card(5, None, 'iv', topic='phys-u2', concept='relationship-between-length-and-resistance',
       source='pdf', from_run=((5, 'a', 'iv'), 0, slice(0, 2)), marks=[4],
       notes="The scheme's answer sections drift a question behind the paper here: "
             "this part's answer sits under its (5)(a)(iv).")


# ── Section B: drawings the scheme describes in words, and criterion parts ─
A.card(6, 'k', None, topic='phys-4-3', concept='labelled-diagram-of-the-atom',
       source='pdf', from_run=((5, 'h', 'i'), 6, slice(0, 12)), marks=[7],
       card_id='phys-2025-ol-q6-k', stem=False,
       notes="The scheme numbers the short-answer question 5 where the paper "
             "prints 6, so this part's answer sits under its (5)(h)(i) block. "
             "Scheme adds '[accept partial answer for 4]'.")

A.card(7, None, 'iv', topic='phys-1-2', concept='example-of-a-vector-quantity',
       source='pdf', from_run=((7, None, 'iv'), 0, slice(0, 3)), marks=[3],
       row_kind='criterion', first_sentence=True, stem=False,
       notes="The scheme accepts 'any valid example' of a vector quantity — the "
             'criterion is the whole marking point.')

A.card(9, None, 'vi', topic='phys-2-3', concept='fibre-optic-total-internal-reflection-diagram',
       source='pdf', stem=False,
       from_runs=[((9, None, 'vi'), 0, slice(0, 7)),    # two materials of...
                  ((9, None, 'vi'), 0, slice(8, 11)),   # ray of light
                  ((9, None, 'vi'), 0, slice(12, 15))],  # multiple internal reflections
       marks=[2, 2, 2],
       notes='The scheme also notes -1 if no label is present on the diagram.')

A.card(10, None, 'ii', topic='phys-3-4', concept='sketch-of-the-field-around-a-bar-magnet',
       source='pdf', stem=False,
       from_runs=[((9, None, 'ii'), 1, slice(0, 10)),   # field lines above and below
                  ((9, None, 'ii'), 1, slice(11, 16))],  # from north to south
       marks=[4, 4],
       notes="The scheme's answer sections drift a question behind the paper here: "
             "Q10's answers run inside its Question 9 blocks.")

A.card(11, None, 'iv', topic='phys-2-1', concept='example-of-a-thermometric-property',
       source='pdf', stem=False, from_run=((11, None, 'iv'), 0, slice(7, 12)),
       marks=[7], row_kind='criterion',
       notes="The scheme accepts 'any valid named thermometric property' — the "
             "criterion is the whole marking point. Scheme adds '[accept partial "
             "answer for 4]'.")

A.emit()
