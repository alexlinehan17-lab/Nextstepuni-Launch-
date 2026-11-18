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
"""Paper-only Atlas anchors for Engineering's deferred sittings.

The archive holds two (paper-trail-corpus/deferredexams/<year>/LC027ALP000EV.pdf,
2022 and 2023 Higher, English). Paper Trail indexes each as its own paper,
"LC027ALP000EV-deferred.pdf", and the Topic Atlas lists its nine printed
questions under that file id (topic-tags/tags/engineering.json, kept by
build-engineering-exam-topic-crosswalk.mjs). This writes the anchor map those
questions open from, in the form History's deferred maps use: paper only
(no scheme mapping claimed), mode "pagejump", one entry per printed question.

Both papers print one question to a page, pages 3 to 11, each headed
"Question N." at the left margin (2023 sets "(50 marks)" on the same
line). A question's crop runs from its heading to
the bottom of its own page (endP/endY): to just above the running footer
("Leaving Certificate <year> / Engineering - Higher level / <page>") when the
page's content stops above it, to the page bottom when a figure or label runs
beside the footer. Nothing is guessed: every heading is found on the page,
the run must be exactly Questions 1 to 9 on pages 3 to 11, and a page without
its footer stops the build.

    python3 scripts/paper-trail/engineering_deferred.py           # write
    python3 scripts/paper-trail/engineering_deferred.py --check   # compare
"""
import argparse
import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS = ROOT / 'paper-trail-corpus' / 'deferredexams'
OUT = ROOT / 'public' / 'paper-anchors'
SOURCE_FILEID = 'LC027ALP000EV.pdf'
FILEID = 'LC027ALP000EV-deferred.pdf'
YEARS = (2022, 2023)
QUESTIONS = 9
FIRST_PAGE = 3                       # 1-based page of Question 1
HEADING = re.compile(r'^Question\s+(\d+)\.?(?:\s+\(50 marks\))?$')
LEFT_MARGIN = 120                    # pt: a heading starts at the left margin
FOOTER_PAD = 0.004                   # stop this far above the footer
CONTENT_PAD = 0.004                  # and at least this far below the content


def page_anchor(page, number):
    """(heading top, crop end) of the question printed on this page."""
    height = page.rect.height
    heading = footer = None
    bottom = 0.0
    for block in page.get_text('dict')['blocks']:
        if block['type'] != 0:
            continue
        for line in block['lines']:
            text = ''.join(span['text'] for span in line['spans']).strip()
            if not text:
                continue
            top = line['bbox'][1] / height
            match = HEADING.match(text)
            if match and line['bbox'][0] < LEFT_MARGIN and top < 0.15:
                if heading is not None or int(match.group(1)) != number:
                    raise SystemExit(f'p{page.number + 1}: heading {text!r}, expected Question {number}')
                heading = top
            elif text.startswith('Leaving Certificate') and top > 0.85:
                footer = top
            elif top > 0.9 and (text.startswith('Engineering') or text.isdigit()):
                continue                     # the footer's second and third lines
            else:
                bottom = max(bottom, line['bbox'][3] / height)
    if heading is None or footer is None:
        raise SystemExit(f'p{page.number + 1}: Question {number} heading or footer not found')
    for info in page.get_image_info():
        bottom = max(bottom, fitz.Rect(info['bbox']).y1 / height)
    for drawing in page.get_drawings():
        if drawing['rect'].y1 / height < footer:
            bottom = max(bottom, drawing['rect'].y1 / height)
    end = 1.0 if bottom + CONTENT_PAD > footer - FOOTER_PAD else footer - FOOTER_PAD
    return round(heading, 4), round(end, 4)


def anchor_map(year):
    document = fitz.open(CORPUS / str(year) / SOURCE_FILEID)
    questions = []
    for index in range(QUESTIONS):
        number = index + 1
        page = FIRST_PAGE + index
        top, end = page_anchor(document[page - 1], number)
        questions.append({
            'n': str(number), 'pP': page, 'pY': [top, end], 'region': [{'p': 1}],
            'mode': 'pagejump', 'conf': 0.5, 'label': f'Question {number}',
            'printOrder': number, 'endP': page, 'endY': end,
        })
    return {
        'v': 1, 'paperFileid': FILEID, 'schemeFileid': '', 'component': '000',
        'band': [1, 1], 'copyright': '© State Examinations Commission', 'paperOnly': 1,
        'q': questions,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for year in YEARS:
        text = json.dumps(anchor_map(year), ensure_ascii=False, separators=(',', ':')) + '\n'
        path = OUT / str(year) / f'{FILEID}.json'
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                stale.append(str(path.relative_to(ROOT)))
            continue
        path.write_text(text, encoding='utf-8')
        print(f'wrote {path.relative_to(ROOT)}')
    if stale:
        print('stale: ' + ', '.join(stale))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
