#!/usr/bin/env python3
# Copyright 2026 Nextstepuni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The provenance gate's copy of a deferred Chemistry scheme: three renderings of the SEC's own PDF.

    python3 scripts/markbank/authoring/chem_deferred_scheme_text.py 2022 hl

A deferred scheme sets its answers in narrow table cells beside a column of
cue labels ("DESCRIBE", "PROCEDURE:") and a column of marks. extract-scheme.py's
flat text splits a word that wraps inside its cell ("wi" / "th"), and the
table-cells text (append-scheme-tables.py) floats subscripts to the cell's end
("KMn / O , MnO , 4 4"); in the text layer's own order a label can sit inside
the answer it labels ("MnO4 – PROCEDURE: solution it is to contain"). The gate
compares a card's claim with the union of the renderings, so this appends two
more, each only the SEC's printed words in their printed order:

  * the text layer of each page, in reading order;
  * the answer column alone: each printed line's words that stand right of the
    label column and left of the marks column (x 150-480 of a 595-wide page),
    which drops the labels, part letters and marks and nothing else.

Re-running replaces the appended sections; the flat and table-cell text above
them are never touched.
"""
import os
import subprocess
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MARK = '<!-- pdf-text-order: the PDF text layer in reading order (deferred scheme) -->'
COLUMN = '<!-- pdf-answer-column: the answer column alone, line by line (deferred scheme) -->'
FOLD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fold-scheme-text.mjs')


def fold(text):
    return subprocess.run(['node', FOLD], input=text, capture_output=True, text=True, check=True).stdout


def answer_column(page, left=150, right=480):
    rows = {}
    for x0, y0, _x1, _y1, word, *_ in page.get_text('words'):
        if left <= x0 < right:
            rows.setdefault(round(y0 / 3), []).append((x0, word))
    return '\n'.join(' '.join(w for _x, w in sorted(words)) for _y, words in sorted(rows.items()))


def main(year, level):
    stem = f'{year}-{level}-deferred'
    md = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes', f'{stem}.md')
    pdf = fitz.open(os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes', f'{stem}.pdf'))
    assert 'Deferred' in pdf[0].get_text(), stem
    original = open(md, encoding='utf-8').read().split(MARK)[0].rstrip('\n')
    order = '\n'.join(' '.join(page.get_text().split()) for page in pdf)
    column = '\n'.join(answer_column(page) for page in pdf)
    with open(md, 'w', encoding='utf-8') as fh:
        fh.write(f'{original}\n\n{MARK}\n\n{fold(order)}\n\n{COLUMN}\n\n{fold(column)}\n')
    print(f'{stem}: appended the text layer and the answer column')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
