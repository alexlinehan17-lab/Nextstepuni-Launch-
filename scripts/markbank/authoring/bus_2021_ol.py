#!/usr/bin/env python3
"""Business 2021 Ordinary Level — Section 2 parts the deck had not carded.

Question and answer both come from the marking scheme's table; see bus_lib for
why that is the source for this subject and not the paper.

Every tariff here is the one the scheme prints. Where it prints a split as well
— "2 x 10m", "(5 + 5)" — the split is what the marks are.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bus_lib import Author  # noqa: E402

A = Author(2021, 'ol')

# Q1(A)(i) and (ii) are not here: both are carded already. Neither shows up in
# bus_todo because 'What do the letters CCPC stand for?' is too short a question
# to identify by its text, which is what that tool matches on.

# Q4(E), why the advertisement is unlawful, is not here either. A card for it
# exists already and carries the advertisement itself, which this one could not;
# the build dropped this version as superseded, which is the right call.

A.card(2, 9, 'a', topic='business-5-13', concept='why-a-brand-name-matters',
       extend=1, use=[[1, 2], [3, 4]], marks=[8, 7], notation='8m (4 + 4), 7m (4 + 3)')

A.card(2, 9, 'b', topic='business-5-13', concept='what-sets-a-price',
       extend=1, use=[1, 2, 3], marks=[7, 7, 6], notation='7m (4 + 3), 7m (4 + 3), 6m')

A.card(2, 9, 'e', topic='business-4-18', concept='merger-versus-takeover',
       use=[[0, 1, 2], [3, 4, 5]], marks=[5, 5], notation='5m (3 + 2) each')

A.emit()
