"""Crop a Mathematics part's printed model solution from a scheme that sets the paper out with its answers.

    python3 scripts/markbank/authoring/maths/scheme_solution_figures.py <year> <hl|ol> [--write]

Why: up to 2015 the SEC's Mathematics scheme is two documents in one. "Model
Solutions" reprints the question paper with each part's worked solution boxed
under it, and "Detailed marking notes" lists each scale's credit bands as
prose. The bands lift cleanly as text; the model solutions are MathType
equations whose text layer is scattered digits ("13 | 64 | 3 | 9 | 27"), so a
card cannot quote them. This attaches the SEC's own print instead: the part as
the scheme prints it, from its marker down to the next part's marker, with the
worked solution beneath it, shown only after the reveal (CardFigure.solution).
scheme_row_figures.py does the same for the 2016+ schemes, which set every part
in one ruled table row; this is its counterpart for the earlier layout.

How a part is found -- geometry, not prose: every part marker ("Question 3",
"(a)", "(b)  (i)", "(ii)") is printed at the left margin of the model-solution
pages. The crop runs from the card's first marker to the next marker that is
not part of the card, across a page break when the solution continues.

Outputs (with --write):
  exam-papers/maths/figures/<year>-<level>/maths-<year>-<LEVEL>-scheme-p<page>-i<n>.png
  scripts/markbank/authored/maths-scheme-row-figures-catalogue.json   (entries for this sitting)
and they publish with scheme_row_figures.py --publish, which reads that catalogue.
"""
import io
import json
import os
import re
import sys

import pymupdf
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
LEVEL = {'hl': 'higher', 'ol': 'ordinary', 'fl': 'foundation'}
LEVEL_WORD = {'hl': 'Higher Level', 'ol': 'Ordinary Level', 'fl': 'Foundation Level'}
SCHEME = {'hl': 'LC003ALP000EV.pdf', 'ol': 'LC003GLP000EV.pdf', 'fl': 'LC003BLP000EV.pdf'}
CATALOGUE = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'maths-scheme-row-figures-catalogue.json')
DPI = 200
X0, X1 = 40.0, 560.0

# Each paper's model-solution pages and detailed-marking-notes pages (PDF
# positions, inclusive). A card's crop is its model solution with its marking
# notes printed under it, so the reveal shows every credit band even where the
# notes set a band in mangled maths that cannot be quoted.
SECTIONS = {
    (2013, 'fl'): {'p1': {'solutions': (7,19), 'notes': (22,28)}, 'p2': {'solutions': (31,45), 'notes': (48,58)}},
    (2013, 'ol'): {'p1': {'solutions': (7,19), 'notes': (22,33)}, 'p2': {'solutions': (37,53), 'notes': (56,66)}},
    (2013, 'hl'): {'p1': {'solutions': (7,26), 'notes': (29,38)}, 'p2': {'solutions': (41,62), 'notes': (65,76)}},
    (2013, 'fl', 'project'): {'p1': {'solutions': (7,19), 'notes': (22,28)}, 'p2': {'solutions': (31,45), 'notes': (48,58)}},
    (2013, 'ol', 'project'): {'p1': {'solutions': (7, 19), 'notes': (22, 32)}, 'p2': {'solutions': (35, 51), 'notes': (54, 64)}},
    (2013, 'hl', 'project'): {'p1': {'solutions': (7, 25), 'notes': (28, 38)}, 'p2': {'solutions': (41, 62), 'notes': (65, 76)}},
    (2014, 'ol'): {'p1': {'solutions': (7, 20), 'notes': (23, 32)}, 'p2': {'solutions': (35, 51), 'notes': (54, 65)}},
    (2014, 'hl'): {'p1': {'solutions': (7, 27), 'notes': (30, 40)}, 'p2': {'solutions': (43, 62), 'notes': (65, 76)}},
    (2015, 'ol'): {'p1': {'solutions': (7, 19), 'notes': (22, 27)}, 'p2': {'solutions': (31, 44), 'notes': (47, 57)}},
    (2015, 'hl'): {'p1': {'solutions': (7, 22), 'notes': (25, 34)}, 'p2': {'solutions': (37, 53), 'notes': (56, 64)}},
}
# The cards whose model solution the text layer cannot carry, per sitting.
AFFECTED = {
    (2013, 'fl'): ['maths-2013-fl-p1-q1', 'maths-2013-fl-p1-q2-a', 'maths-2013-fl-p1-q2-b', 'maths-2013-fl-p1-q3-a', 'maths-2013-fl-p1-q3-b', 'maths-2013-fl-p1-q4-a', 'maths-2013-fl-p1-q4-b', 'maths-2013-fl-p1-q5-a', 'maths-2013-fl-p1-q5-b', 'maths-2013-fl-p1-q5-c', 'maths-2013-fl-p1-q6-a', 'maths-2013-fl-p1-q6-b', 'maths-2013-fl-p1-q6-c', 'maths-2013-fl-p1-q7-a', 'maths-2013-fl-p1-q7-b', 'maths-2013-fl-p1-q7-c', 'maths-2013-fl-p1-q8-a-i', 'maths-2013-fl-p1-q8-a-ii', 'maths-2013-fl-p1-q8-a-iii', 'maths-2013-fl-p1-q8-a-iv', 'maths-2013-fl-p1-q8-b-i', 'maths-2013-fl-p1-q8-b-ii', 'maths-2013-fl-p1-q9-a', 'maths-2013-fl-p1-q9-b-row-2', 'maths-2013-fl-p1-q9-b-row-3', 'maths-2013-fl-p1-q9-b-row-4', 'maths-2013-fl-p1-q9-b-row-5', 'maths-2013-fl-p1-q9-b-row-6', 'maths-2013-fl-p1-q9-d', 'maths-2013-fl-p1-q9-e', 'maths-2013-fl-p1-q9-f', 'maths-2013-fl-p1-q10-a', 'maths-2013-fl-p1-q10-b', 'maths-2013-fl-p2-q1-a-i', 'maths-2013-fl-p2-q1-a-ii', 'maths-2013-fl-p2-q1-b-i', 'maths-2013-fl-p2-q1-b-ii', 'maths-2013-fl-p2-q1-b-iii', 'maths-2013-fl-p2-q2-a-i', 'maths-2013-fl-p2-q2-a-ii', 'maths-2013-fl-p2-q2-b', 'maths-2013-fl-p2-q2-c', 'maths-2013-fl-p2-q3-a-meal-01', 'maths-2013-fl-p2-q3-a-meal-02', 'maths-2013-fl-p2-q3-a-meal-03', 'maths-2013-fl-p2-q3-a-meal-04', 'maths-2013-fl-p2-q3-a-meal-05', 'maths-2013-fl-p2-q3-a-meal-06', 'maths-2013-fl-p2-q3-a-meal-07', 'maths-2013-fl-p2-q3-a-meal-08', 'maths-2013-fl-p2-q3-a-meal-09', 'maths-2013-fl-p2-q3-a-meal-10', 'maths-2013-fl-p2-q3-a-meal-11', 'maths-2013-fl-p2-q3-a-meal-12', 'maths-2013-fl-p2-q3-a-meal-13', 'maths-2013-fl-p2-q3-a-meal-14', 'maths-2013-fl-p2-q3-a-meal-15', 'maths-2013-fl-p2-q3-a-meal-16', 'maths-2013-fl-p2-q3-a-meal-17', 'maths-2013-fl-p2-q3-a-meal-18', 'maths-2013-fl-p2-q3-a-meal-19', 'maths-2013-fl-p2-q3-a-meal-20', 'maths-2013-fl-p2-q3-a-meal-21', 'maths-2013-fl-p2-q3-a-meal-22', 'maths-2013-fl-p2-q3-a-meal-23', 'maths-2013-fl-p2-q3-a-meal-24', 'maths-2013-fl-p2-q3-a-meal-25', 'maths-2013-fl-p2-q3-a-meal-26', 'maths-2013-fl-p2-q3-a-meal-27', 'maths-2013-fl-p2-q3-a-meal-28', 'maths-2013-fl-p2-q3-a-meal-29', 'maths-2013-fl-p2-q3-a-meal-30', 'maths-2013-fl-p2-q3-a-meal-31', 'maths-2013-fl-p2-q3-a-meal-32', 'maths-2013-fl-p2-q3-a-meal-33', 'maths-2013-fl-p2-q3-a-meal-34', 'maths-2013-fl-p2-q3-a-meal-35', 'maths-2013-fl-p2-q3-a-meal-36', 'maths-2013-fl-p2-q3-a-meal-37', 'maths-2013-fl-p2-q3-a-meal-38', 'maths-2013-fl-p2-q3-a-meal-39', 'maths-2013-fl-p2-q3-a-meal-40', 'maths-2013-fl-p2-q3-a-meal-41', 'maths-2013-fl-p2-q3-a-meal-42', 'maths-2013-fl-p2-q3-a-meal-43', 'maths-2013-fl-p2-q3-a-meal-44', 'maths-2013-fl-p2-q3-a-meal-45', 'maths-2013-fl-p2-q3-a-meal-46', 'maths-2013-fl-p2-q3-a-meal-47', 'maths-2013-fl-p2-q3-a-meal-48', 'maths-2013-fl-p2-q3-a-meal-49', 'maths-2013-fl-p2-q3-a-meal-50', 'maths-2013-fl-p2-q3-a-meal-51', 'maths-2013-fl-p2-q3-a-meal-52', 'maths-2013-fl-p2-q3-a-meal-53', 'maths-2013-fl-p2-q3-a-meal-54', 'maths-2013-fl-p2-q3-a-meal-55', 'maths-2013-fl-p2-q3-a-meal-56', 'maths-2013-fl-p2-q3-a-meal-57', 'maths-2013-fl-p2-q3-a-meal-58', 'maths-2013-fl-p2-q3-a-meal-59', 'maths-2013-fl-p2-q3-a-meal-60', 'maths-2013-fl-p2-q3-b', 'maths-2013-fl-p2-q3-c', 'maths-2013-fl-p2-q4-a', 'maths-2013-fl-p2-q4-b', 'maths-2013-fl-p2-q4-c', 'maths-2013-fl-p2-q4-d', 'maths-2013-fl-p2-q4-e', 'maths-2013-fl-p2-q5-a', 'maths-2013-fl-p2-q5-b-i', 'maths-2013-fl-p2-q5-b-ii', 'maths-2013-fl-p2-q5-c', 'maths-2013-fl-p2-q6-a', 'maths-2013-fl-p2-q6-b', 'maths-2013-fl-p2-q6-c', 'maths-2013-fl-p2-q7-a', 'maths-2013-fl-p2-q7-b-i', 'maths-2013-fl-p2-q7-b-ii', 'maths-2013-fl-p2-q7-b-iii', 'maths-2013-fl-p2-q8a-a', 'maths-2013-fl-p2-q8a-b', 'maths-2013-fl-p2-q8a-c', 'maths-2013-fl-p2-q8b-a', 'maths-2013-fl-p2-q8b-b', 'maths-2013-fl-p2-q8b-c-ab-dc', 'maths-2013-fl-p2-q8b-c-ad-bc', 'maths-2013-fl-p2-q8b-d', 'maths-2013-fl-p2-q8b-e', 'maths-2013-fl-p2-q9-a', 'maths-2013-fl-p2-q9-b', 'maths-2013-fl-p2-q9-c', 'maths-2013-fl-p2-q9-d', 'maths-2013-fl-p2-q9-e', 'maths-2013-fl-p2-q9-f', 'maths-2013-fl-p2-q10-a-i', 'maths-2013-fl-p2-q10-a-ii', 'maths-2013-fl-p2-q10-b-i', 'maths-2013-fl-p2-q10-b-ii', 'maths-2013-fl-p2-q10-c'],
    (2013, 'ol'): ['maths-2013-ol-p1-q1-a', 'maths-2013-ol-p1-q1-b', 'maths-2013-ol-p1-q1-c', 'maths-2013-ol-p1-q1-d', 'maths-2013-ol-p1-q2-a', 'maths-2013-ol-p1-q2-b', 'maths-2013-ol-p1-q3-a', 'maths-2013-ol-p1-q3-b-i', 'maths-2013-ol-p1-q3-b-ii-abcde', 'maths-2013-ol-p1-q3-b-ii-abcdf', 'maths-2013-ol-p1-q3-b-ii-abcdg', 'maths-2013-ol-p1-q3-b-ii-abcef', 'maths-2013-ol-p1-q3-b-ii-abceg', 'maths-2013-ol-p1-q3-b-ii-abcfg', 'maths-2013-ol-p1-q3-b-ii-abdef', 'maths-2013-ol-p1-q3-b-ii-abdeg', 'maths-2013-ol-p1-q3-b-ii-abdfg', 'maths-2013-ol-p1-q3-b-ii-abefg', 'maths-2013-ol-p1-q3-b-ii-acdef', 'maths-2013-ol-p1-q3-b-ii-acdeg', 'maths-2013-ol-p1-q3-b-ii-acdfg', 'maths-2013-ol-p1-q3-b-ii-acefg', 'maths-2013-ol-p1-q3-b-ii-adefg', 'maths-2013-ol-p1-q3-b-ii-bcdef', 'maths-2013-ol-p1-q3-b-ii-bcdeg', 'maths-2013-ol-p1-q3-b-ii-bcdfg', 'maths-2013-ol-p1-q3-b-ii-bcefg', 'maths-2013-ol-p1-q3-b-ii-bdefg', 'maths-2013-ol-p1-q3-b-ii-cdefg', 'maths-2013-ol-p1-q3-c', 'maths-2013-ol-p1-q4-a', 'maths-2013-ol-p1-q4-b', 'maths-2013-ol-p1-q4-c', 'maths-2013-ol-p1-q5-a', 'maths-2013-ol-p1-q5-b', 'maths-2013-ol-p1-q5-c', 'maths-2013-ol-p1-q5-d', 'maths-2013-ol-p1-q5-e', 'maths-2013-ol-p1-q5-f', 'maths-2013-ol-p1-q6-a', 'maths-2013-ol-p1-q6-b', 'maths-2013-ol-p1-q6-c-i', 'maths-2013-ol-p1-q6-c-ii', 'maths-2013-ol-p1-q6-d', 'maths-2013-ol-p1-q6-e', 'maths-2013-ol-p1-q6-f', 'maths-2013-ol-p1-q6-g', 'maths-2013-ol-p1-q6-h', 'maths-2013-ol-p1-q7-a', 'maths-2013-ol-p1-q7-b-i', 'maths-2013-ol-p1-q7-b-ii', 'maths-2013-ol-p1-q7-c-i', 'maths-2013-ol-p1-q7-c-ii', 'maths-2013-ol-p1-q7-c-iii', 'maths-2013-ol-p1-q7-c-iv', 'maths-2013-ol-p1-q8-a', 'maths-2013-ol-p1-q8-b-i', 'maths-2013-ol-p1-q8-b-ii', 'maths-2013-ol-p1-q8-c-i', 'maths-2013-ol-p1-q8-c-ii', 'maths-2013-ol-p1-q8-c-iii', 'maths-2013-ol-p2-q1-a', 'maths-2013-ol-p2-q1-b', 'maths-2013-ol-p2-q1-c', 'maths-2013-ol-p2-q2-a-i', 'maths-2013-ol-p2-q2-b', 'maths-2013-ol-p2-q2-c', 'maths-2013-ol-p2-q3-a', 'maths-2013-ol-p2-q3-b', 'maths-2013-ol-p2-q3-c', 'maths-2013-ol-p2-q4-a', 'maths-2013-ol-p2-q4-b', 'maths-2013-ol-p2-q4-c', 'maths-2013-ol-p2-q5-a', 'maths-2013-ol-p2-q5-b', 'maths-2013-ol-p2-q5-c', 'maths-2013-ol-p2-q6a-a', 'maths-2013-ol-p2-q6a-b', 'maths-2013-ol-p2-q6a-c', 'maths-2013-ol-p2-q6b', 'maths-2013-ol-p2-q7-a', 'maths-2013-ol-p2-q7-b', 'maths-2013-ol-p2-q7-c', 'maths-2013-ol-p2-q7-d-i', 'maths-2013-ol-p2-q7-d-ii', 'maths-2013-ol-p2-q7-e', 'maths-2013-ol-p2-q7-f', 'maths-2013-ol-p2-q7-g', 'maths-2013-ol-p2-q7-h', 'maths-2013-ol-p2-q7-i', 'maths-2013-ol-p2-q8-a-i', 'maths-2013-ol-p2-q8-a-ii', 'maths-2013-ol-p2-q8-a-iii', 'maths-2013-ol-p2-q8-a-iv', 'maths-2013-ol-p2-q8-a-v', 'maths-2013-ol-p2-q8-b-i', 'maths-2013-ol-p2-q8-b-ii', 'maths-2013-ol-p2-q8-b-iii', 'maths-2013-ol-p2-q8-b-iv', 'maths-2013-ol-p2-q8-c-i', 'maths-2013-ol-p2-q8-c-ii'],
    (2013, 'hl'): ['maths-2013-hl-p1-q1-a', 'maths-2013-hl-p1-q1-b', 'maths-2013-hl-p1-q1-c', 'maths-2013-hl-p1-q2-a', 'maths-2013-hl-p1-q2-b', 'maths-2013-hl-p1-q3-a', 'maths-2013-hl-p1-q3-b', 'maths-2013-hl-p1-q4-a-i', 'maths-2013-hl-p1-q4-a-ii', 'maths-2013-hl-p1-q4-b', 'maths-2013-hl-p1-q5-a', 'maths-2013-hl-p1-q5-b', 'maths-2013-hl-p1-q5-c', 'maths-2013-hl-p1-q5-d', 'maths-2013-hl-p1-q5-e', 'maths-2013-hl-p1-q5-f', 'maths-2013-hl-p1-q5-g', 'maths-2013-hl-p1-q6-a-i', 'maths-2013-hl-p1-q6-a-ii', 'maths-2013-hl-p1-q6-b', 'maths-2013-hl-p1-q6-c', 'maths-2013-hl-p1-q6-d', 'maths-2013-hl-p1-q6-e', 'maths-2013-hl-p1-q7-a', 'maths-2013-hl-p1-q7-b-i', 'maths-2013-hl-p1-q7-b-ii', 'maths-2013-hl-p1-q7-c-i', 'maths-2013-hl-p1-q7-c-ii', 'maths-2013-hl-p1-q8-a', 'maths-2013-hl-p1-q8-b-i', 'maths-2013-hl-p1-q8-b-ii', 'maths-2013-hl-p1-q8-c-i', 'maths-2013-hl-p1-q8-c-ii', 'maths-2013-hl-p1-q8-c-iii'],
    (2014, 'ol'): ['maths-2014-ol-p1-q1-a', 'maths-2014-ol-p1-q1-b', 'maths-2014-ol-p1-q1-c', 'maths-2014-ol-p1-q2-a-i', 'maths-2014-ol-p1-q2-a-ii', 'maths-2014-ol-p1-q2-a-iii', 'maths-2014-ol-p1-q2-b', 'maths-2014-ol-p1-q3-a-i', 'maths-2014-ol-p1-q3-a-ii', 'maths-2014-ol-p1-q3-b', 'maths-2014-ol-p1-q4-a', 'maths-2014-ol-p1-q4-b', 'maths-2014-ol-p1-q4-c-i', 'maths-2014-ol-p1-q5-a-i', 'maths-2014-ol-p1-q5-b', 'maths-2014-ol-p1-q5-c', 'maths-2014-ol-p1-q6-a-i', 'maths-2014-ol-p1-q6-a-ii', 'maths-2014-ol-p1-q6-b-i', 'maths-2014-ol-p1-q6-b-ii', 'maths-2014-ol-p1-q7-a', 'maths-2014-ol-p1-q7-b-i', 'maths-2014-ol-p1-q7-b-ii', 'maths-2014-ol-p1-q7-b-iii', 'maths-2014-ol-p1-q8-a', 'maths-2014-ol-p1-q8-b', 'maths-2014-ol-p1-q8-c', 'maths-2014-ol-p1-q8-d', 'maths-2014-ol-p1-q8-e', 'maths-2014-ol-p1-q9-a', 'maths-2014-ol-p1-q9-b', 'maths-2014-ol-p1-q9-c-i', 'maths-2014-ol-p1-q9-c-ii', 'maths-2014-ol-p1-q9-c-iii', 'maths-2014-ol-p1-q9-d-i', 'maths-2014-ol-p1-q9-e-i', 'maths-2014-ol-p1-q9-e-ii', 'maths-2014-ol-p1-q9-e-iii', 'maths-2014-ol-p1-q9-f'],
    (2014, 'hl'): ['maths-2014-hl-p1-q1-a', 'maths-2014-hl-p1-q1-b-i', 'maths-2014-hl-p1-q1-b-ii', 'maths-2014-hl-p1-q2-a', 'maths-2014-hl-p1-q2-b-i', 'maths-2014-hl-p1-q2-b-ii', 'maths-2014-hl-p1-q3-a', 'maths-2014-hl-p1-q3-b', 'maths-2014-hl-p1-q3-c', 'maths-2014-hl-p1-q4-a', 'maths-2014-hl-p1-q4-b', 'maths-2014-hl-p1-q5-a', 'maths-2014-hl-p1-q5-b-i', 'maths-2014-hl-p1-q5-b-ii', 'maths-2014-hl-p1-q6-a-i', 'maths-2014-hl-p1-q6-a-ii', 'maths-2014-hl-p1-q6-b', 'maths-2014-hl-p1-q6-c', 'maths-2014-hl-p1-q7-a-i', 'maths-2014-hl-p1-q7-a-ii', 'maths-2014-hl-p1-q7-b-i', 'maths-2014-hl-p1-q7-b-ii', 'maths-2014-hl-p1-q8-a', 'maths-2014-hl-p1-q8-b', 'maths-2014-hl-p1-q8-c', 'maths-2014-hl-p1-q8-d', 'maths-2014-hl-p1-q8-e', 'maths-2014-hl-p1-q9-a', 'maths-2014-hl-p1-q9-b', 'maths-2014-hl-p1-q9-c', 'maths-2014-hl-p1-q9-d', 'maths-2014-hl-p1-q9-e-i', 'maths-2014-hl-p1-q9-f-i', 'maths-2014-hl-p1-q9-f-ii'],
    (2015, 'ol'): ['maths-2015-ol-p1-q1-a', 'maths-2015-ol-p1-q1-b', 'maths-2015-ol-p1-q1-c', 'maths-2015-ol-p1-q2-a', 'maths-2015-ol-p1-q2-b-i', 'maths-2015-ol-p1-q2-c', 'maths-2015-ol-p1-q3-a', 'maths-2015-ol-p1-q3-b', 'maths-2015-ol-p1-q3-c', 'maths-2015-ol-p1-q4-a', 'maths-2015-ol-p1-q4-b', 'maths-2015-ol-p1-q4-c', 'maths-2015-ol-p1-q5-a', 'maths-2015-ol-p1-q5-b-i', 'maths-2015-ol-p1-q6-a-i', 'maths-2015-ol-p1-q6-b-i', 'maths-2015-ol-p1-q6-b-ii', 'maths-2015-ol-p1-q7-a', 'maths-2015-ol-p1-q7-b', 'maths-2015-ol-p1-q7-c', 'maths-2015-ol-p1-q7-d-i', 'maths-2015-ol-p1-q7-e', 'maths-2015-ol-p1-q7-f', 'maths-2015-ol-p1-q7-g', 'maths-2015-ol-p1-q7-h', 'maths-2015-ol-p1-q8-a', 'maths-2015-ol-p1-q8-b', 'maths-2015-ol-p1-q8-c-i', 'maths-2015-ol-p1-q8-d-i', 'maths-2015-ol-p1-q8-d-ii', 'maths-2015-ol-p1-q8-e', 'maths-2015-ol-p1-q9-a-i', 'maths-2015-ol-p1-q9-a-ii', 'maths-2015-ol-p1-q9-a-iii', 'maths-2015-ol-p1-q9-b', 'maths-2015-ol-p2-q1-a', 'maths-2015-ol-p2-q1-b-i', 'maths-2015-ol-p2-q1-c', 'maths-2015-ol-p2-q2-a-i', 'maths-2015-ol-p2-q2-b', 'maths-2015-ol-p2-q2-c', 'maths-2015-ol-p2-q3-a', 'maths-2015-ol-p2-q3-b', 'maths-2015-ol-p2-q3-c', 'maths-2015-ol-p2-q4-a', 'maths-2015-ol-p2-q4-b-i', 'maths-2015-ol-p2-q5-a-i', 'maths-2015-ol-p2-q5-a-ii', 'maths-2015-ol-p2-q5-b', 'maths-2015-ol-p2-q6-a-i', 'maths-2015-ol-p2-q6-b-i', 'maths-2015-ol-p2-q7-a-i', 'maths-2015-ol-p2-q7-a-ii', 'maths-2015-ol-p2-q7-b', 'maths-2015-ol-p2-q7-c-i', 'maths-2015-ol-p2-q8-a-i', 'maths-2015-ol-p2-q8-a-ii', 'maths-2015-ol-p2-q8-b-i', 'maths-2015-ol-p2-q8-b-ii', 'maths-2015-ol-p2-q8-b-iii', 'maths-2015-ol-p2-q8-c-i', 'maths-2015-ol-p2-q8-c-ii', 'maths-2015-ol-p2-q9-a', 'maths-2015-ol-p2-q9-b-i', 'maths-2015-ol-p2-q9-b-ii', 'maths-2015-ol-p2-q9-b-iii', 'maths-2015-ol-p2-q9-c-i', 'maths-2015-ol-p2-q9-c-ii', 'maths-2015-ol-p2-q9-c-iii', 'maths-2015-ol-p2-q9-c-iv', 'maths-2015-ol-p2-q9-d-i', 'maths-2015-ol-p2-q9-d-ii'],
    (2015, 'hl'): ['maths-2015-hl-p1-q1-a', 'maths-2015-hl-p1-q1-b', 'maths-2015-hl-p1-q1-c', 'maths-2015-hl-p1-q2', 'maths-2015-hl-p1-q3-a-i', 'maths-2015-hl-p1-q3-b-i', 'maths-2015-hl-p1-q4-a', 'maths-2015-hl-p1-q4-b', 'maths-2015-hl-p1-q5-a', 'maths-2015-hl-p1-q5-b', 'maths-2015-hl-p1-q5-c', 'maths-2015-hl-p1-q6-a-i', 'maths-2015-hl-p1-q6-b', 'maths-2015-hl-p1-q7-a-i', 'maths-2015-hl-p1-q7-a-ii', 'maths-2015-hl-p1-q7-b-i', 'maths-2015-hl-p1-q7-b-ii', 'maths-2015-hl-p1-q7-c', 'maths-2015-hl-p1-q7-d-i', 'maths-2015-hl-p1-q7-d-ii', 'maths-2015-hl-p1-q8-a-i', 'maths-2015-hl-p1-q8-a-ii', 'maths-2015-hl-p1-q8-a-iii', 'maths-2015-hl-p1-q8-b-i', 'maths-2015-hl-p1-q8-b-ii', 'maths-2015-hl-p1-q8-c', 'maths-2015-hl-p1-q8-d', 'maths-2015-hl-p1-q9-a', 'maths-2015-hl-p1-q9-b', 'maths-2015-hl-p1-q9-c', 'maths-2015-hl-p1-q9-d', 'maths-2015-hl-p1-q9-e', 'maths-2015-hl-p2-q1-a', 'maths-2015-hl-p2-q1-b-i', 'maths-2015-hl-p2-q1-c', 'maths-2015-hl-p2-q2-a', 'maths-2015-hl-p2-q2-b', 'maths-2015-hl-p2-q2-c', 'maths-2015-hl-p2-q3-a', 'maths-2015-hl-p2-q3-b', 'maths-2015-hl-p2-q3-c-i', 'maths-2015-hl-p2-q4-a', 'maths-2015-hl-p2-q4-b-i', 'maths-2015-hl-p2-q4-b-ii', 'maths-2015-hl-p2-q4-c', 'maths-2015-hl-p2-q5-a', 'maths-2015-hl-p2-q5-b', 'maths-2015-hl-p2-q6-a', 'maths-2015-hl-p2-q6-b', 'maths-2015-hl-p2-q7-a', 'maths-2015-hl-p2-q7-b', 'maths-2015-hl-p2-q7-c-i', 'maths-2015-hl-p2-q7-c-ii', 'maths-2015-hl-p2-q8-a', 'maths-2015-hl-p2-q8-b', 'maths-2015-hl-p2-q8-c', 'maths-2015-hl-p2-q8-d-i', 'maths-2015-hl-p2-q8-d-ii', 'maths-2015-hl-p2-q8-e-i', 'maths-2015-hl-p2-q8-e-ii', 'maths-2015-hl-p2-q8-f-i', 'maths-2015-hl-p2-q9-a', 'maths-2015-hl-p2-q9-b', 'maths-2015-hl-p2-q9-c-i', 'maths-2015-hl-p2-q9-c-ii', 'maths-2015-hl-p2-q9-d-i', 'maths-2015-hl-p2-q9-d-ii']
}

AFFECTED[(2013, 'hl')] += ['maths-2013-hl-p2-q1-a-i', 'maths-2013-hl-p2-q1-a-ii', 'maths-2013-hl-p2-q1-a-iii', 'maths-2013-hl-p2-q1-b', 'maths-2013-hl-p2-q2-a-i', 'maths-2013-hl-p2-q2-a-ii', 'maths-2013-hl-p2-q2-b', 'maths-2013-hl-p2-q3-a', 'maths-2013-hl-p2-q3-b', 'maths-2013-hl-p2-q4-a', 'maths-2013-hl-p2-q4-b-i', 'maths-2013-hl-p2-q4-b-ii', 'maths-2013-hl-p2-q5-a', 'maths-2013-hl-p2-q5-b-i', 'maths-2013-hl-p2-q5-b-ii', 'maths-2013-hl-p2-q5-c', 'maths-2013-hl-p2-q6a-a', 'maths-2013-hl-p2-q6a-b', 'maths-2013-hl-p2-q6a-c', 'maths-2013-hl-p2-q6b-a', 'maths-2013-hl-p2-q6b-b', 'maths-2013-hl-p2-q7-a-i', 'maths-2013-hl-p2-q7-a-ii', 'maths-2013-hl-p2-q7-b-i', 'maths-2013-hl-p2-q7-b-ii', 'maths-2013-hl-p2-q7-c', 'maths-2013-hl-p2-q7-d-i', 'maths-2013-hl-p2-q7-d-ii', 'maths-2013-hl-p2-q7-e-i', 'maths-2013-hl-p2-q7-e-ii', 'maths-2013-hl-p2-q7-f-i', 'maths-2013-hl-p2-q7-f-ii', 'maths-2013-hl-p2-q7-f-iii', 'maths-2013-hl-p2-q7-f-iv', 'maths-2013-hl-p2-q8-a-i', 'maths-2013-hl-p2-q8-a-ii', 'maths-2013-hl-p2-q8-b', 'maths-2013-hl-p2-q9-a', 'maths-2013-hl-p2-q9-b-i', 'maths-2013-hl-p2-q9-b-ii', 'maths-2013-hl-p2-q9-c-i', 'maths-2013-hl-p2-q9-c-ii', 'maths-2013-hl-p2-q9-c-iii', 'maths-2013-hl-p2-q9-d']

AFFECTED[(2014, 'hl')] += ['maths-2014-hl-p2-q1-a-i', 'maths-2014-hl-p2-q1-a-ii', 'maths-2014-hl-p2-q1-b', 'maths-2014-hl-p2-q2-a', 'maths-2014-hl-p2-q2-b', 'maths-2014-hl-p2-q3-a', 'maths-2014-hl-p2-q3-b', 'maths-2014-hl-p2-q3-c', 'maths-2014-hl-p2-q4-a-i', 'maths-2014-hl-p2-q4-b-i', 'maths-2014-hl-p2-q4-c-i', 'maths-2014-hl-p2-q5-a', 'maths-2014-hl-p2-q5-b', 'maths-2014-hl-p2-q5-c', 'maths-2014-hl-p2-q6a-a', 'maths-2014-hl-p2-q6a-b', 'maths-2014-hl-p2-q6b-a', 'maths-2014-hl-p2-q6b-b', 'maths-2014-hl-p2-q6b-c', 'maths-2014-hl-p2-q7-a', 'maths-2014-hl-p2-q7-b', 'maths-2014-hl-p2-q7-c-i', 'maths-2014-hl-p2-q7-c-ii', 'maths-2014-hl-p2-q7-c-iii', 'maths-2014-hl-p2-q7-d-i', 'maths-2014-hl-p2-q7-d-ii', 'maths-2014-hl-p2-q7-d-iii', 'maths-2014-hl-p2-q8-a-i', 'maths-2014-hl-p2-q8-a-ii', 'maths-2014-hl-p2-q8-a-iii', 'maths-2014-hl-p2-q8-a-iv', 'maths-2014-hl-p2-q8-b-i', 'maths-2014-hl-p2-q8-b-ii', 'maths-2014-hl-p2-q9-a-i', 'maths-2014-hl-p2-q9-a-ii', 'maths-2014-hl-p2-q9-a-iii', 'maths-2014-hl-p2-q9-a-iv', 'maths-2014-hl-p2-q9-a-v', 'maths-2014-hl-p2-q9-b-i', 'maths-2014-hl-p2-q9-b-ii', 'maths-2014-hl-p2-q9-b-iii']

AFFECTED[(2014, 'ol')] += ['maths-2014-ol-p2-q1-a-i', 'maths-2014-ol-p2-q1-b-i', 'maths-2014-ol-p2-q1-b-ii', 'maths-2014-ol-p2-q1-c', 'maths-2014-ol-p2-q2-a', 'maths-2014-ol-p2-q2-b', 'maths-2014-ol-p2-q2-c', 'maths-2014-ol-p2-q2-d', 'maths-2014-ol-p2-q3-a-i', 'maths-2014-ol-p2-q3-b-i', 'maths-2014-ol-p2-q3-b-ii', 'maths-2014-ol-p2-q3-c', 'maths-2014-ol-p2-q4-a-i', 'maths-2014-ol-p2-q4-a-ii', 'maths-2014-ol-p2-q4-b-i', 'maths-2014-ol-p2-q5-a', 'maths-2014-ol-p2-q5-b-i', 'maths-2014-ol-p2-q5-b-ii', 'maths-2014-ol-p2-q5-c', 'maths-2014-ol-p2-q6a-a-i', 'maths-2014-ol-p2-q6a-a-ii', 'maths-2014-ol-p2-q6a-b', 'maths-2014-ol-p2-q6b', 'maths-2014-ol-p2-q7-a-i', 'maths-2014-ol-p2-q7-b', 'maths-2014-ol-p2-q7-c-i', 'maths-2014-ol-p2-q7-c-ii', 'maths-2014-ol-p2-q7-c-iii', 'maths-2014-ol-p2-q7-c-iv', 'maths-2014-ol-p2-q7-c-v', 'maths-2014-ol-p2-q8-a-i', 'maths-2014-ol-p2-q8-a-ii', 'maths-2014-ol-p2-q8-a-iii', 'maths-2014-ol-p2-q8-a-iv', 'maths-2014-ol-p2-q8-b', 'maths-2014-ol-p2-q8-c-i', 'maths-2014-ol-p2-q8-c-ii', 'maths-2014-ol-p2-q9-a-i', 'maths-2014-ol-p2-q9-a-ii', 'maths-2014-ol-p2-q9-b-i', 'maths-2014-ol-p2-q9-b-ii']

MARK = re.compile(r'\((?:[a-h]|i{1,3}|iv|vi{0,3}|ix|x)\)')
QHEAD = re.compile(r'^Question\s+(\d{1,2}[A-Z]?)\b')
ROMAN = re.compile(r'^(?:i{1,3}|iv|vi{0,3}|ix|x)$')
FOOTER = re.compile(r'^\[\d+\]$')


def markers(doc, first, last, align_marker_baselines=False):
    """[(q, letter, roman, page, y)] for every part marker at the left margin, in order."""
    out, q, letter = [], None, None
    for pno in range(first, last + 1):
        page = doc[pno - 1]
        lines = []
        for b in page.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                t = ''.join(s['text'] for s in ln['spans']).strip()
                if t:
                    lines.append((round(ln['bbox'][1], 1), ln['bbox'][0], t))
        # Some older PDFs position a roman marker 0.1pt above its parent
        # letter. Read those near-identical baselines left-to-right.
        ordered = sorted(lines, key=lambda row: (round(row[0]), row[1])) if align_marker_baselines else sorted(lines)
        for y, x, t in ordered:
            if x > 140:
                continue
            # 2015 Ordinary Paper 2 Q9(d)(i) omits the opening parenthesis
            # in its detailed-note heading, while the allocation table is clear.
            if t.startswith('d(i)') and 'Scale 5C' in t:
                t = '(d)(i)' + t[len('d(i)'):]
            m = QHEAD.match(t)
            if m:
                q, letter = (int(m.group(1)) if m.group(1).isdigit() else m.group(1)), None
                out.append((q, None, None, pno, y))
                continue
            toks = []
            rest = t
            while True:
                mm = MARK.match(rest)
                if not mm:
                    break
                toks.append(mm.group(0)[1:-1])
                rest = rest[mm.end():].lstrip()
            if not toks or q is None:
                continue
            roman = None
            for tok in toks:
                # (i) after (h) would be a letter; Mathematics never runs that far.
                if ROMAN.match(tok) and (letter is not None or len(toks) > 1 and tok != toks[0]):
                    roman = tok
                else:
                    letter, roman = tok, None
            out.append((q, letter, roman, pno, y))
    return out


def parse_part(printed):
    m = re.match(r'^Q(\d+[A-Z]?)(?:\(([a-h])\))?(?:\(([ivx]+)\))?$', printed)
    return (int(m.group(1)) if m.group(1).isdigit() else m.group(1)), m.group(2), m.group(3)


def span(entries, printed):
    """(start entry index, end entry index or None) for a card's printed parts.

    The notes print a combined scale once ("(a)(i) and (ii) combined"), so a
    card's later parts need not have markers of their own; a question with no
    lettered parts runs to the next question.
    """
    q, letter, roman = parse_part(printed[0])
    candidates = [i for i, e in enumerate(entries)
                  if e[0] == q and (e[1] == letter or letter is None) and (roman is None or e[2] == roman)]
    if not candidates and len(printed) > 1:
        # A combined notes heading may be just (c), or (b)(i)(ii). Only
        # reviewed groups may fall back to their shared parent marker.
        romans = {parse_part(p)[2] for p in printed}
        candidates = [i for i, e in enumerate(entries) if e[0] == q and e[1] == letter
                      and (e[2] is None or e[2] in romans)]
    if not candidates:
        raise ValueError(f'No source marker for {printed}')
    start = candidates[0]
    if letter is None:
        end = next((j for j in range(start + 1, len(entries)) if entries[j][0] != q), None)
        return start, end
    last = start
    for part in printed:
        pq, pl, pr = parse_part(part)
        for i in range(start, len(entries)):
            e = entries[i]
            if e[0] == pq and e[1] == pl and (pr is None or e[2] == pr):
                last = max(last, i)
    lq, ll, lr = entries[last][0], entries[last][1], entries[last][2]
    lr = parse_part(printed[-1])[2] if parse_part(printed[-1])[2] else (lr if entries[last][2] else None)
    for j in range(last + 1, len(entries)):
        e = entries[j]
        if e[0] != lq or e[1] != ll or (lr is not None and e[2] != lr):
            return start, j
    return start, None


def content_bottom(page):
    ys = [b[1] for b in page.get_text('blocks') if FOOTER.match(b[4].strip())]
    return (min(ys) - 4) if ys else page.rect.height - 50


def crop(doc, a, b, last_page, start_top=None, end_bottom=None, continuation_tops=None):
    """Image of the pages from entry a to entry b (or the section's end)."""
    (_, _, _, p0, y0) = a
    p1, y1 = (b[3], b[4]) if b else (last_page, None)
    pieces = []
    for pno in range(p0, p1 + 1):
        page = doc[pno - 1]
        top = (start_top if start_top is not None else y0 - 5) if pno == p0 else (continuation_tops or {}).get(pno, 45.0)
        bottom = (y1 - 5) if (pno == p1 and y1 is not None) else content_bottom(page)
        if pno == p1 and end_bottom is not None:
            bottom = end_bottom
        # A new section can precede the next question on the following page.
        # It is not a continuation of this solution (2015 HL P1 Q6(b)).
        if b and b[0] != a[0] and pno == p1:
            headings = [block[1] for block in page.get_text('blocks')
                        if re.search(r'\bSection [AB]\b', block[4])
                        and (pno != p0 or top <= block[1]) and block[1] < bottom]
            if headings:
                bottom = min(headings) - 5
        if bottom - top < 8:
            continue
        pix = page.get_pixmap(clip=pymupdf.Rect(X0, top, X1, bottom), dpi=DPI)
        im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('L')
        rows = [y for y in range(im.height) if min(im.crop((0, y, im.width, y + 1)).getdata()) < 200]
        if rows:
            pieces.append(im.crop((0, max(0, rows[0] - 6), im.width, min(im.height, rows[-1] + 7))))
    out = Image.new('L', (max(p.width for p in pieces), sum(p.height for p in pieces) + 12 * (len(pieces) - 1)), 255)
    y = 0
    for p in pieces:
        out.paste(p, (0, y)); y += p.height + 12
    return out


def main():
    year, lv = int(sys.argv[1]), sys.argv[2]
    write = '--write' in sys.argv
    edition = 'project' if '--project' in sys.argv else None
    config = (year, lv, edition) if edition else (year, lv)
    variant = f'{edition}-' if edition else ''
    scheme_file = SCHEME[lv].replace('LP000EV', 'LP030EV') if edition == 'project' else SCHEME[lv]
    doc = pymupdf.open(os.path.join(ROOT, 'paper-trail-corpus', 'markingschemes', str(year), scheme_file))
    tasks = {}
    for key in ('p1', 'p2'):
        path = os.path.join(ROOT, 'scripts', 'markbank', 'mathematics', 'reviews', f'{year}-{LEVEL[lv]}-{key}{"-" + edition if edition else ""}.json')
        if os.path.exists(path):
            tasks.update({c['id']: c for c in json.load(open(path))['cards']})
    out_dir = os.path.join(ROOT, 'exam-papers', 'maths', 'figures', f'{year}-{lv}')
    if write:
        os.makedirs(out_dir, exist_ok=True)
    index = {k: {part: markers(doc, *rng, align_marker_baselines=year in (2013, 2014)) for part, rng in v.items()} for k, v in SECTIONS[config].items()}
    if (year, lv) == (2013, 'fl') and 'p2' in index:
        # Printed notes have '(b)((ii)' in Q1 and 'b(ii)' in Q5.
        index['p2']['notes'] = [(q, letter, 'ii' if (q, letter, roman, page) == (1, 'b', None, 48) else roman, page, y) for q, letter, roman, page, y in index['p2']['notes']]
        index['p2']['notes'].append((5, 'b', 'ii', 52, 292.1))
        index['p2']['notes'].sort(key=lambda e: (e[3], e[4]))
    if (year, lv) == (2013, 'ol') and 'p2' in index:
        # Q7(i) is a lettered task, not a roman subpart of Q7(h).
        for section in ('solutions', 'notes'):
            index['p2'][section] = [(q, 'i', None, page, y) if (q, letter, roman) == (7, 'h', 'i') else (q, letter, roman, page, y) for q, letter, roman, page, y in index['p2'][section]]
    if (year, lv) == (2014, 'ol'):
        # PDF 28 omits (a) before (i); paper, model and summary confirm Q6(a)(i).
        index['p1']['notes'] = [(q, 'a', 'i', page, y) if q == 6 and letter == 'i' and roman is None else (q, letter, roman, page, y) for q, letter, roman, page, y in index['p1']['notes']]
    per_page, entries = {}, []
    seen_selections = set()
    for cid in (list(tasks) if edition else AFFECTED[config]):
        task = tasks[cid]
        selection = task.get('selectionVariant', {}).get('groupId')
        if selection in seen_selections:
            continue  # All finite routes share the complete original solution/scale.
        if selection:
            seen_selections.add(selection)
        key = cid.split('-')[3]
        images, where = [], []
        for part in ('solutions', 'notes'):
            ents = index[key][part]
            a, b = span(ents, ['Q5'] if cid == 'maths-2013-ol-p1-project-q5' else ['Q1'] if cid in ('maths-2013-fl-p1-project-q1','maths-2013-fl-p1-q1') else task['printedParts'])
            if cid in ('maths-2013-ol-p2-project-q7-i', 'maths-2013-ol-p2-q7-i'):
                a = next(i for i, marker in enumerate(ents) if marker[:3] == (7, 'i', None))
                b = a + 1 if a + 1 < len(ents) else None
            start, end = ents[a], (ents[b] if b is not None else None)
            if (year, lv, part) == (2014, 'ol', 'notes') and a > 0 and ents[a-1][0] == start[0] and ents[a-1][1] is None:
                start = ents[a-1]  # Keep the complete question heading, not a clipped descender.
            # Inspected tight boundaries: preserve the complete shared setup,
            # and omit the preceding graph's bottom rule before Q8(a)(iii).
            solution_tops = {
                'maths-2013-ol-p2-project-q2-a-i': 74,
                'maths-2013-ol-p2-q2-a-i': 74,
                'maths-2013-ol-p2-project-q4-a': 74,
                'maths-2013-ol-p2-q4-a': 74,
                'maths-2013-ol-p2-project-q6b': 46,
                'maths-2013-ol-p2-q6b': 46,
                'maths-2013-ol-p1-project-q2-a': 74,
                'maths-2013-ol-p1-q2-a': 74,
                'maths-2013-ol-p1-q6-a': 75,
                'maths-2013-ol-p1-q6-c-i': 342,
                'maths-2013-ol-p1-project-q8-a': 75,
                'maths-2013-ol-p1-project-q8-c-i': 342,
                'maths-2013-hl-p2-q4-a': 74,
                'maths-2013-hl-p2-project-q4-a': 74,
                'maths-2013-hl-p2-q7-b-ii': 328,
                'maths-2013-hl-p2-project-q7-b-ii': 328,
                'maths-2013-hl-p2-q9-a': 52,
                'maths-2013-hl-p2-project-q9-a': 52,
                'maths-2013-hl-p1-project-q6-a': 75,
                'maths-2014-ol-p2-q8-a-i': 75,
                'maths-2014-ol-p2-q8-c-i': 55,
                'maths-2014-ol-p1-q4-c-i': 54,
                'maths-2014-ol-p1-q9-a': 75,
                'maths-2014-hl-p2-q5-a': 75,
                'maths-2014-hl-p2-q9-a-i': 75,
                'maths-2014-hl-p2-q9-a-v': 270,
                'maths-2014-hl-p2-q9-b-i': 490,
                'maths-2014-hl-p1-q4-b': 248,
                'maths-2014-hl-p1-q5-b-i': 197,
                'maths-2014-hl-p1-q6-a-i': 78,
                'maths-2014-hl-p1-q7-b-i': 54,
                'maths-2014-hl-p1-q8-a': 75,
                'maths-2014-hl-p1-q9-a': 75,
                'maths-2015-ol-p2-q2-a-i': 58,
                'maths-2015-ol-p2-q4-b-i': 430,
                'maths-2015-ol-p2-q5-a-i': 58,
                'maths-2015-ol-p2-q6-a-i': 58,
                'maths-2015-ol-p2-q8-a-i': 58,
                'maths-2015-ol-p2-q8-b-i': 294,
                'maths-2015-ol-p1-q2-b-i': 268,
                'maths-2015-ol-p1-q5-a': 58,
                'maths-2015-ol-p1-q5-b-i': 360,
                'maths-2015-ol-p1-q6-a-i': 57,
                'maths-2015-ol-p1-q7-a': 311,
                'maths-2015-ol-p1-q7-e': 248,
                'maths-2015-ol-p1-q8-a': 58,
                'maths-2015-ol-p1-q8-c-i': 582,
                'maths-2015-hl-p1-q3-a-i': 75,
                'maths-2015-hl-p1-q6-a-i': 72,
                'maths-2015-hl-p1-q8-a-iii': 481,
                'maths-2015-hl-p1-q8-b-i': 586,
                'maths-2015-hl-p2-q3-c-i': 402,
                'maths-2015-hl-p2-q4-a': 52,
                'maths-2015-hl-p2-q4-b-i': 264,
                'maths-2015-hl-p2-q5-b': 503,
                'maths-2015-hl-p2-q8-e-i': 377,
                'maths-2015-hl-p2-q8-f-i': 271,
                'maths-2015-hl-p2-q9-c-i': 73,
                'maths-2015-hl-p2-q9-d-i': 32,
                'maths-2015-hl-p2-q9-d-ii': 32,
            }
            part_image = crop(doc, start, end, SECTIONS[config][key][part][1],
                               solution_tops.get(cid) if part == 'solutions' else (94 if cid == 'maths-2015-ol-p2-q7-a-i' else None),
                               {'maths-2014-hl-p2-q9-a-iv': 265, 'maths-2014-hl-p1-q4-a': 248, 'maths-2015-hl-p2-q4-a': 263, 'maths-2015-hl-p2-q5-a': 496, 'maths-2015-ol-p1-q7-d-i': 248}.get(cid) if part == 'solutions' else (270 if cid == 'maths-2015-ol-p1-q9-b' else None),
                               {51: 30} if cid == 'maths-2015-hl-p2-q9-b' and part == 'solutions' else None)
            regions = {
                'maths-2013-hl-p2-q5-a': [(47,(40,74,570,595))],
                'maths-2013-hl-p2-q6b-b': [(51,(40,90,565,398))],
                'maths-2013-hl-p2-q7-a-i': [(52,(40,583,565,700))],
                'maths-2013-hl-p2-q7-b-i': [(53,(40,206,565,328))],
                'maths-2013-hl-p2-q7-e-i': [(54,(40,199,565,554))],
                'maths-2013-hl-p1-q6-e': [(20,(40,345,565,780))],
                'maths-2013-hl-p1-q8-b-i': [(24,(40,197,565,438))],
                'maths-2013-hl-p2-q1-b': [(41,(40,447,565,760))],
                'maths-2013-hl-p2-project-q1-b': [(41,(40,447,565,760))],
                'maths-2013-hl-p2-q6a-c': [(49,(40,488,565,780))],
                'maths-2013-hl-p2-project-q6a-c': [(49,(40,488,565,780))],
                'maths-2013-hl-p2-q7-d-i': [(54,(40,52,332,102)),(54,(333,48,550,197))],
                'maths-2013-hl-p2-project-q7-d-i': [(54,(40,52,332,102)),(54,(333,48,550,197))],
                'maths-2013-hl-p2-q7-d-ii': [(54,(40,48,565,198))],
                'maths-2013-hl-p2-project-q7-d-ii': [(54,(40,48,565,198))],
                'maths-2013-hl-p2-q7-f-iv': [(55,(40,603,560,627)),(55,(85,185,545,418))],
                'maths-2013-hl-p2-project-q7-f-iv': [(55,(40,603,560,627)),(55,(85,185,545,418))],
                'maths-2013-hl-p1-project-q6-a': [(15,(40,74,330,145)),(15,(335,60,550,211)),(15,(40,214,565,294))],
                # Independently inspected diagrams cross the automatic text boundaries.
                'maths-2014-ol-p2-q4-b-i': [(38, (40, 75, 565, 583)), (39, (40, 267, 565, 570))],
                'maths-2014-ol-p2-q5-b-i': [(40, (40, 200, 400, 344)), (40, (405, 248, 565, 355))],
                'maths-2014-ol-p2-q5-b-ii': [(40, (40, 345, 400, 510)), (40, (405, 416, 565, 525))],
                'maths-2014-ol-p2-q5-c': [(40, (40, 512, 400, 733)), (40, (405, 575, 565, 683))],
                'maths-2014-ol-p2-q6a-b': [(42, (40, 54, 565, 450))],
                'maths-2014-ol-p2-q6b': [(43, (40, 75, 565, 505))],
                'maths-2014-ol-p2-q7-b': [(44, (20, 352, 565, 801))],
                'maths-2014-ol-p2-q8-b': [(48, (40, 219, 580, 570))],
                'maths-2014-ol-p1-q6-b-ii': [(13, (40, 525, 565, 705))],
                'maths-2014-ol-p1-q9-c-i': [(18, (40, 271, 565, 702)), (19, (40, 54, 565, 113))],
                'maths-2014-ol-p1-q9-c-ii': [(18, (40, 271, 565, 702)), (19, (40, 119, 565, 170))],
                'maths-2014-ol-p1-q9-c-iii': [(18, (40, 271, 565, 702)), (19, (40, 173, 565, 222))],
                'maths-2014-ol-p1-q9-d-i': [(19, (40, 241, 565, 500))],
                'maths-2014-hl-p2-q6a-b': [(51, (40, 54, 560, 445))],
                'maths-2014-hl-p2-q6b-c': [(52, (40, 604, 560, 740))],
                # Keep both complete methods, without the empty continuation space.
                'maths-2014-hl-p1-q8-c': [(22, (40, 54, 565, 535)), (23, (40, 55, 565, 520))],
                'maths-2014-hl-p1-q6-c': [(16, (40, 54, 560, 440))],
                'maths-2015-ol-p1-q4-c': [(11, (40, 36, 560, 385))],
                'maths-2015-ol-p1-q7-b': [(14, (18, 539, 560, 749))],
            }.get(cid) if part == 'solutions' else None
            if cid == 'maths-2013-hl-p1-q6-e' and part == 'notes':
                regions = [(35,(40,280,565,430))]
            if cid.startswith('maths-2013-fl-p2-project-'):
                suffix = cid.split('-project-')[1]
                if part == 'solutions':
                    regions = {
                        'q1-b-i': [(31,(40,458,565,613))],
                        'q1-b-ii': [(31,(40,612,565,668))],
                        'q1-b-iii': [(31,(40,671,565,727))],
                        'q5-a': [(36,(40,74,565,298))],
                        'q5-b-i': [(36,(40,305,565,332)),(36,(330,74,550,280))],
                        'q6-a': [(37,(40,74,350,162)),(37,(355,74,550,240))],
                        'q6-b': [(37,(40,182,350,210)),(37,(40,241,565,311))],
                        'q8a-b': [(40,(40,595,565,635)),(40,(70,210,550,590))],
                        'q8a-c': [(40,(40,637,565,718))],
                        'q8b-a': [(41,(40,162,302,247))],
                        'q8b-b': [(41,(40,250,302,350))],
                        'q8b-e': [(41,(40,597,565,635)),(41,(300,92,570,325))],
                        'q10-a-i': [(44,(40,140,300,220))],
                        'q10-b-i': [(44,(40,339,565,726))],
                    }.get(suffix, regions)
                elif suffix == 'q9-a':
                    regions = [(57,(40,80,565,150))]
            if cid.startswith('maths-2013-fl-p2-q'):
                suffix = cid.split('-p2-')[1]
                if part == 'solutions':
                    regions = {
                        'q1-b-i': [(31,(40,458,565,613))],
                        'q1-b-ii': [(31,(40,612,565,668))],
                        'q1-b-iii': [(31,(40,671,565,727))],
                        'q5-a': [(36,(40,74,565,298))],
                        'q5-b-i': [(36,(40,305,565,332)),(36,(330,74,550,280))],
                        'q6-a': [(37,(40,74,350,162)),(37,(355,74,550,240))],
                        'q6-b': [(37,(40,182,350,210)),(37,(40,241,565,311))],
                        'q8a-b': [(40,(40,595,565,635)),(40,(70,210,550,590))],
                        'q8a-c': [(40,(40,637,565,718))],
                        'q8b-a': [(41,(40,162,302,247))],
                        'q8b-b': [(41,(40,250,302,350))],
                        'q8b-e': [(41,(40,597,565,635)),(41,(300,88,570,335))],
                        'q10-a-i': [(44,(40,140,300,220))],
                        'q10-b-i': [(44,(40,339,565,726))],
                    }.get(suffix, regions)
                elif suffix == 'q9-a':
                    regions = [(57,(40,80,565,150))]
            if cid.startswith('maths-2013-fl-p1-project-'):
                suffix = cid.split('-project-')[1]
                if part == 'solutions':
                    regions = {
                        'q1': [(7,(40,159,565,287)),(7,(40,350,565,480)),(7,(40,547,565,649))],
                        'q3-b': [(9,(40,582,565,735))],
                        'q10-a': [(18,(40,75,565,327))],
                        'q10-h': [(19,(40,229,565,745))],
                    }.get(suffix, regions)
                elif suffix == 'q8-b':
                    regions = [(26,(40,348,565,434))]
            if cid.startswith('maths-2013-fl-p1-q'):
                suffix = cid.split('-p1-')[1]
                if part == 'solutions':
                    regions = {
                        'q1': [(7,(40,159,565,287)),(7,(40,350,565,480)),(7,(40,547,565,649))],
                        'q3-b': [(9,(40,582,565,735))],
                        'q9-a': [(16,(40,75,565,327))],
                        'q9-f': [(17,(40,54,565,203))],
                        'q10-b': [(18,(40,377,565,762)),(19,(40,54,565,506))],
                    }.get(suffix, regions)
                elif suffix == 'q9-f':
                    regions = [(27,(40,408,565,500))]
            if part == 'solutions' and cid.startswith('maths-2013-ol-p2-project-'):
                regions = {
                    'q6a-b': [(42,(40,432,565,467)),(42,(145,178,452,390))],
                    'q6a-c': [(42,(40,514,565,652))],
                    'q8-b-ii': [(50,(54,184,302,262)),(50,(302,184,568,430))],
                    'q8-b-iii': [(50,(54,294,302,434)),(50,(302,184,568,430)),(50,(54,452,565,502))],
                }.get(cid.split('-project-')[1], regions)
            if part == 'solutions' and cid.startswith('maths-2013-ol-p2-q'):
                regions = {
                    'q6a-b': [(44,(40,432,565,467)),(44,(145,178,452,390))],
                    'q6a-c': [(44,(40,514,565,652))],
                    'q8-b-ii': [(52,(54,184,302,262)),(52,(302,184,568,430))],
                    'q8-b-iii': [(52,(54,294,302,434)),(52,(302,184,568,430)),(52,(54,452,565,502))],
                }.get('q'+cid.split('-p2-q')[1], regions)
            if part == 'solutions' and cid.startswith('maths-2013-ol-p1-project-'):
                regions = {
                    'q1-a': [(7,(54,170,316,192)),(7,(318,134,560,382))],
                    'q1-b': [(7,(54,194,316,382)),(7,(318,134,560,382))],
                    'q6-a': [(13,(54,143,316,233))],
                    'q6-b-i': [(13,(54,261,320,368))],
                    'q6-b-ii': [(13,(54,417,327,454)),(13,(80,488,543,530))],
                }.get(cid.split('-project-')[1], regions)
            if part == 'solutions' and cid.startswith('maths-2013-ol-p1-q'):
                regions = {
                    'q4-c': [(11,(40,54,565,210))],
                    'q6-h': [(15,(40,466,565,720))],
                    'q7-c-i': [(17,(54,135,316,234))],
                    'q7-c-ii': [(17,(54,271,320,371))],
                    'q7-c-iii': [(17,(54,416,327,460)),(17,(80,471,543,505))],
                    'q1-a': [(7,(54,170,316,192)),(7,(318,134,560,382))],
                    'q1-b': [(7,(54,194,316,382)),(7,(318,134,560,382))],
                }.get(cid.split('-p1-')[1], regions)
            if part == 'notes' and cid.startswith(('maths-2013-hl-p2-q8-', 'maths-2013-hl-p2-project-q8-')):
                # Roman labels inside the common Note are not question boundaries.
                own = {'a-i': (78,223), 'a-ii': (280,427), 'b': (433,482)}[cid.split('-q8-')[1]]
                regions = [(74,(40,own[0],565,own[1])),(74,(40,227,565,276)),(74,(40,487,565,594)),(75,(40,52,565,291))]
            if part == 'notes' and cid == 'maths-2013-ol-p1-q6-h':
                regions = [(29,(40,458,565,519))]
            prefixes = {
                'maths-2014-hl-p1-q1-b-ii': [(7, (335, 158, 545, 325))],
                'maths-2014-hl-p1-q9-e-i': [(26, (78, 291, 542, 560))],
                'maths-2015-ol-p2-q2-c': [(32, (365, 55, 560, 205))],
                'maths-2015-ol-p2-q5-a-ii': [(35, (285, 62, 565, 248))],
                'maths-2015-ol-p2-q5-b': [(35, (285, 62, 565, 248))],
                'maths-2015-ol-p2-q7-a-i': [(38, (100, 228, 520, 802))],
                'maths-2015-ol-p2-q7-a-ii': [(38, (100, 228, 520, 802))],
                'maths-2015-ol-p2-q9-c-iii': [(43, (55, 278, 548, 498))],
                'maths-2015-ol-p2-q9-c-iv': [(43, (55, 278, 548, 498))],
                'maths-2015-ol-p1-q5-b-i': [(12, (330, 80, 545, 287))],
                'maths-2015-ol-p1-q8-c-i': [(16, (85, 272, 550, 580))],
                'maths-2015-ol-p1-q9-a-i': [(18, (30, 125, 552, 461))],
                'maths-2015-ol-p1-q9-a-ii': [(18, (30, 125, 552, 461))],
                'maths-2015-ol-p1-q9-a-iii': [(18, (30, 125, 552, 461))],
            }.get(cid, []) if part == 'solutions' else []
            if part == 'notes' and cid in {f'maths-2013-fl-p1-q8-a-{s}' for s in ('ii','iii','iv')}:
                prefixes = [(26,(54,178,555,197))]
            if part == 'notes' and cid == 'maths-2013-fl-p1-q9-d':
                prefixes = [(27,(54,241,550,259))]
            if part == 'notes' and cid in {f'maths-2013-fl-p1-project-q9-a-{s}' for s in ('ii','iii','iv')}:
                prefixes = [(27,(80,176,550,196))]
            if part == 'notes' and cid == 'maths-2013-fl-p1-project-q10-d':
                prefixes = [(28,(70,225,550,245))]
            if part == 'notes' and cid in {f'maths-2013-ol-p1-q5-{s}' for s in ('b','c','d')}:
                prefixes = [(26,(80,324,550,360))]
            if part == 'notes' and cid in {f'maths-2013-ol-p1-q5-{s}' for s in ('e','f')}:
                prefixes = [(27,(80,177,550,198))]
            if part == 'notes' and cid in {f'maths-2013-ol-p1-project-q7-{s}' for s in ('b','c','d')}:
                prefixes = [(28,(80,304,550,338))]
            if part == 'notes' and cid in {f'maths-2013-ol-p1-project-q7-{s}' for s in ('e','f')}:
                prefixes = [(29,(80,177,550,198))]
            if part == 'solutions' and cid.startswith(('maths-2013-hl-p2-q8-', 'maths-2013-hl-p2-project-q8-')):
                prefixes = [(56,(40,74,565,109))]
            if part == 'notes' and cid.startswith('maths-2014-ol-p1-q9-c-'):
                prefixes = [(31, (40, 337, 565, 358))]
            if part == 'notes' and cid.startswith('maths-2014-hl-p1-q6-'):
                prefixes = [(35, (55, 83, 545, 102))]
            if part == 'notes' and cid == 'maths-2014-hl-p1-q7-a-i':
                prefixes = [(36, (55, 312, 545, 358))]
            if regions or prefixes:
                pieces = [Image.open(io.BytesIO(doc[pno - 1].get_pixmap(clip=pymupdf.Rect(rect), dpi=DPI).tobytes('png'))).convert('L')
                          for pno, rect in (regions or prefixes)]
                if cid in ('maths-2013-ol-p1-project-q1-a', 'maths-2013-ol-p1-project-q1-b', 'maths-2013-ol-p1-q1-a', 'maths-2013-ol-p1-q1-b') and part == 'solutions':
                    # Remove the unrelated question tariff above the Argand graph.
                    pieces[1].paste(255, (round((480-318)*DPI/72), 0, pieces[1].width, round(13*DPI/72)))
                if cid == 'maths-2013-hl-p1-project-q6-a' and part == 'solutions':
                    pieces[1].paste(255, (round((475-335)*DPI/72), 0, pieces[1].width, round(14*DPI/72)))
                if cid == 'maths-2015-ol-p2-q2-c':
                    # Remove the preceding sentence fragment without touching the graph.
                    pieces[0].paste(255, (0, 0, round((480 - 365) * DPI / 72), round((78 - 55) * DPI / 72)))
                if cid == 'maths-2013-fl-p2-q8b-e' and part == 'solutions':
                    # Remove neighbouring text fragments, preserving all reflected labels.
                    pieces[1].paste(255, (0, round((128-88)*DPI/72), round(8*DPI/72), round((155-88)*DPI/72)))
                if not regions:
                    pieces.append(part_image)
                width = max(im.width for im in pieces)
                part_image = Image.new('L', (width, sum(im.height for im in pieces) + 12 * (len(pieces) - 1)), 255)
                y = 0
                for im in pieces:
                    part_image.paste(im, ((width - im.width) // 2, y)); y += im.height + 12
            if part == 'solutions' and cid == 'maths-2015-ol-p1-q7-e':
                part_image.paste(255, (int((418 - X0) * DPI / 72), 0, part_image.width, 10))
            images.append(part_image)
            where.append((start, end))
        pno = where[0][0][3]
        n = per_page.get(pno, 0); per_page[pno] = n + 1
        name = f'maths-{year}-{lv.upper()}-scheme-{variant}p{pno:03d}-i{n}'
        paper_no = key[1]
        refs = ', '.join(task['printedParts'])
        desc = (f"The marking scheme's printed model solution and detailed marking notes for {year} {LEVEL_WORD[lv]} Paper {paper_no} {refs}, "
                f"as the State Examinations Commission set them: the part as printed with its worked solution beneath it, then the "
                f"scale and every credit band the notes give for it.")
        entries.append({'file': name + '.png', 'kind': 'figure', 'truncated': False, 'description': desc, 'solution': True,
                        'questionRef': f"{year} {lv.upper()} Paper {paper_no} {refs}"})
        if cid == 'maths-2015-ol-p1-q5-a':
            entries[-1]['sourceNote'] = 'NextStepUni clarification: the printed factorisation has a sign error. It should read (x − 1)(x − 3) = 0. The scheme’s answers A(1, 4) and B(3, 6) are correct.'
        corrections = {
            'maths-2013-hl-p1-q4-a-ii': 'NextStepUni source note: the first model gives €392 for deposits at the beginning of each month, as stated in the question. The alternative model gives €393 using an end-of-month payment convention. Both models are printed in the official scheme.',
            'maths-2013-fl-p2-project-q4-e': 'NextStepUni clarification: the printed sample answer repeats age 55. The original plot contains one patient aged 55. The complete list is 31, 32, 36, 36, 36, 39, 43, 46, 50, 50, 55, 58.',
            'maths-2013-fl-p2-project-q3-a-meal-01': 'The scheme shows one example lunch. Any one starter, one main course and one dessert from the printed menu is valid; use the route named in this practice card.',
            'maths-2013-fl-p2-q3-a-meal-01': 'The scheme shows one example lunch. Any one starter, one main course and one dessert from the printed menu is valid; use the route named in this practice card.',

            'maths-2013-ol-p1-project-q5': 'SEC marking note: parts (a), (b) and (c) share one 25-mark scale. Some requested skills were outside the syllabus for these candidates. The official scheme marks syllabus-related skills only and allows full credit for consistently demonstrating them, for example three terms correctly differentiated.',
            **{f'maths-2013-hl-p2-q8-{part}': 'SEC source warning: this question contains inconsistent data. Different valid methods give different answers. The official scheme accepts valid approaches and carries the candidate’s values forward. Where the error affects the work, it awards full marks for that part and subsequent parts. All published models and impact criteria are preserved below; this is not a question with one reliable numerical answer.' for part in ('a-i','a-ii','b')},
            **{f'maths-2013-hl-p2-project-q8-{part}': 'SEC source warning: this question contains inconsistent data. Different valid methods give different answers. The official scheme accepts valid approaches and carries the candidate’s values forward. Where the error affects the work, it awards full marks for that part and subsequent parts. All published models and impact criteria are preserved below; this is not a question with one reliable numerical answer.' for part in ('a-i','a-ii','b')},
            'maths-2013-hl-p2-q7-e-i': 'NextStepUni clarification: the first model reverses the interval endpoints. The interval is [0·6684, 0·7316]. Its rejection decision and the second model are unchanged. The scheme also accepts work that excludes the don’t-know responses, using 664/902 and n = 902.',
            'maths-2013-hl-p2-project-q7-e-i': 'NextStepUni clarification: the first model reverses the interval endpoints. The interval is [0·6684, 0·7316]. Its rejection decision and the second model are unchanged. The scheme also accepts work that excludes the don’t-know responses, using 664/902 and n = 902.',
            'maths-2013-hl-p2-q9-c-i': 'NextStepUni clarification: in the fourth row, r₂ = 4 and r₃ = 2, so the substitution must use 4² + 2², not 4² + 1². The final area 8π cm² is correct. The notes label the scale 5B in error but print 0, 5, 10; the allocation table and question total confirm 10 marks.',
            'maths-2013-hl-p2-project-q9-c-i': 'NextStepUni clarification: in the fourth row, r₂ = 4 and r₃ = 2, so the substitution must use 4² + 2², not 4² + 1². The final area 8π cm² is correct. The notes label the scale 5B in error but print 0, 5, 10; the allocation table and question total confirm 10 marks.',
            'maths-2013-hl-p1-project-q4-a-ii': 'NextStepUni source note: the first model gives €392 for deposits at the beginning of each month, as stated in the question. The alternative model gives €393 using an end-of-month payment convention. Both models are printed in the official scheme.',
            'maths-2013-hl-p1-project-q6-d': 'NextStepUni clarification: the model reprints the reference as part (a). The original question asks for the percentage error in the trapezoidal estimate from part (b), compared with the exact area from part (c).',
            'maths-2013-hl-p1-project-q8-d': 'NextStepUni clarification: the printed branch k(t − 10) omits the 80 metres already fallen in the first 10 seconds. The official solution includes that distance: s(t) = 80 + 9(t − 10) after 10 seconds, giving a total time of 70 seconds for 620 metres.',
            'maths-2013-hl-p1-project-q9-e': 'NextStepUni clarification: 4234 in the first model is a printing error. The question gives 4134 matchsticks; the working and second model correctly use 4134, giving n = 52 and 2704 small triangles.',
            'maths-2014-ol-p2-q7-a-i': 'NextStepUni clarification: the model gives 1·71 because the question states the property count in millions. This means 1,710,000 properties.',
            'maths-2014-ol-p2-q7-b': 'NextStepUni clarification: the printed calculation for Band 4 says 37·44° ≈ 90° in error. It should read approximately 37°, as shown correctly in the model pie chart.',
            'maths-2014-ol-p1-q4-c-i': 'NextStepUni source note: the allocation summary lists 10C for Q4(c), but the detailed notes give 5C. This card follows the detailed notes, keeping Question 4 at its printed total of 25 marks (15 + 5 + 5).',
            'maths-2014-hl-p2-q7-d-i': 'NextStepUni clarification: the printed model says “Male unemployment declined”. The chart and conclusion concern employment: male employment fell after 2007, female employment after 2008, with the larger fall among males.',
            **{f'maths-2014-hl-p2-q9-a-{part}': 'NextStepUni source note: the allocation summary gives 10 marks each to Q9(a)(i) and (iv), but the detailed marking notes give 15C and 5C respectively. These cards follow the detailed notes. Question 9 still totals 60 marks.' for part in ('i', 'iv')},
            'maths-2015-ol-p2-q4-a': 'NextStepUni clarification: the printed calculation for y uses 100° in error. The diagram gives 110°, so y = 180° − (110° + 30°) = 40°. The final answers x = 30°, y = 40° and z = 70° are correct.',
            'maths-2015-ol-p2-q4-b-i': 'NextStepUni clarification: in part (ii), triangle BCE is one quarter of parallelogram ABCD, not one half as printed. Its area is 480 ÷ 4 = 120 m². Both final areas in the scheme are correct.',
            'maths-2015-ol-p2-q8-b-iii': 'NextStepUni clarification: using the displayed 129 litres gives 129 ÷ 25 = 5·16 tins. Using the unrounded 129·2 litres gives approximately 5·17 tins. Either way, six whole tins are needed and the cost is €1080.',
        }
        if cid in corrections:
            entries[-1]['sourceNote'] = corrections[cid]
        fmt = lambda se: f"p{se[0][3]} y{se[0][4]:.0f} -> " + (f"p{se[1][3]} y{se[1][4]:.0f}" if se[1] else 'section end')
        print(f'{cid:32} solution {fmt(where[0])} | notes {fmt(where[1])}  {name}')
        if write:
            # The worked solution above, its marking notes below, ruled apart.
            w = max(im.width for im in images)
            out = Image.new('L', (w, sum(im.height for im in images) + 41), 255)
            out.paste(images[0], (0, 0))
            for x in range(10, w - 10):
                out.putpixel((x, images[0].height + 20), 120)
            out.paste(images[1], (0, images[0].height + 41))
            out.save(os.path.join(out_dir, name + '.png'))
    if write:
        cat = json.load(open(CATALOGUE)) if os.path.exists(CATALOGUE) else []
        # Require a page number: unlabelled 'p' must not also match 'project-p'.
        sitting_pattern = re.compile(rf'^maths-{year}-{lv.upper()}-scheme-{variant}p\d')
        keep = [e for e in cat if not sitting_pattern.match(e['file'])]
        open(CATALOGUE, 'w').write(json.dumps(keep + entries, ensure_ascii=False, indent=1) + '\n')
        print(f'wrote {len(entries)} crops and catalogue entries')


if __name__ == '__main__':
    main()
