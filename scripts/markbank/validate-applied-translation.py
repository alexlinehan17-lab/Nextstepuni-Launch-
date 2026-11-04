#!/usr/bin/env python3
"""Validate recorded Irish source review; never infer review completion."""
import json
import re
import sys
import unicodedata

import fitz

DIRECTIVE_PATTERN = r'\b(?:roghn\w*|ceann|cinn|(?:c|ch)eist\w*.*[fF]h?reag\w*|[fF]h?reag\w*.*(?:c|ch)eist\w*|nó|cibé|ceachtar|ar bith|aon)\b'
paper = json.load(sys.stdin)
documents = {'paper': fitz.open(sys.argv[1]), 'scheme': fitz.open(sys.argv[2])}
for kind, document in documents.items():
    if paper[f'{kind}PagesReviewed'] != list(range(1, len(document) + 1)):
        raise ValueError(f'{kind}: incomplete page review')
    for question in paper['questions']:
        regions = question[f'{kind}Region']
        if not regions:
            raise ValueError(f'{kind}: missing regions for Q{question["n"]}')
        for source in regions:
            page_number, rect = source['p'], source['r']
            if not isinstance(page_number, int) or not 1 <= page_number <= len(document):
                raise ValueError(f'{kind}: invalid page for Q{question["n"]}')
            if len(rect) != 4 or not (0 <= rect[0] < rect[2] <= 1 and 0 <= rect[1] < rect[3] <= 1):
                raise ValueError(f'{kind}: invalid region for Q{question["n"]}')
            page = document[page_number - 1]
            box = fitz.Rect(rect[0] * page.rect.width, rect[1] * page.rect.height,
                            rect[2] * page.rect.width, rect[3] * page.rect.height)
            if not page.get_text(clip=box).strip():
                raise ValueError(f'{kind}: empty region for Q{question["n"]}')
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    text = ''.join(span['text'] for span in line['spans']).strip()
                    x0, y0, x1, y1 = line['bbox']
                    y0, y1 = y0 / page.rect.height, y1 / page.rect.height
                    if text and x0 < box.x1 and x1 > box.x0 and (
                        y0 + .0005 < rect[1] < y1 - .0005 or y0 + .0005 < rect[3] < y1 - .0005
                    ):
                        raise ValueError(f'{kind}: Q{question["n"]} page {page_number} clips {text!r}')
selections = []
for index, page in enumerate(documents['paper']):
    for line in page.get_text().splitlines():
        line = ' '.join(unicodedata.normalize('NFKC', line).split())
        if re.search(DIRECTIVE_PATTERN, line, re.I):
            selections.append({'page': index + 1, 'text': line})
print(json.dumps({'selections': selections, 'schemePages': len(documents['scheme'])}))
