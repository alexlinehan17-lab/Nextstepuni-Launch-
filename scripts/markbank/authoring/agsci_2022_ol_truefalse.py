#!/usr/bin/env python3
"""Agricultural Science 2022 OL Q4(b) — the true/false statements.

The paper prints five statements to mark true or false, with the first worked as
an example. The scheme sets its answers as a table and prints them as a single
run — "False True True False False" — with the roman markers in a neighbouring
cell, so no parser attributes an answer to a part. from_run takes the nth word
of that run for the nth statement: the word is lifted from the scheme, and only
the correspondence between position and part is read off the page.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agsci_lib import Author  # noqa: E402

A = Author(2022, 'ol')
RUN = ((4, 'b', None), 1, None)     # parent part, the point holding the run
CHECKED = ('Page 7 of the paper opened: the five statements are set in a table '
           'with True and False tick columns and the extracted text matches each '
           'row exactly. They carry no full stop because the paper prints none.')
NOTE = ('The scheme prints the five answers as one run against Q4(b) rather than '
        'against each statement, so this answer is the run\'s word for this '
        'statement. Tariff 5(2): five statements at 2 marks each.')

for index, (roman, concept) in enumerate((
        ('i', 'oestrus-cycle-length'),
        ('ii', 'gestation-length-in-cattle'),
        ('iii', 'rumen-ph'),
        ('iv', 'body-condition-score-at-calving'),
        ('v', 'compartments-in-the-ruminant-stomach'))):
    A.card(4, 'b', roman, topic='agsci-4-1', concept=concept, source='pdf',
           from_run=(RUN[0], RUN[1], index), marks=[2], notation='5(2)',
           checked=CHECKED, notes=NOTE)

A.emit()
