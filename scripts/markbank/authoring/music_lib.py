#!/usr/bin/env python3
"""Shared readers for Music schemes (music lane, from 19 Nov 2026).

Composing Section B (harmony) is marked on the scheme's bands PLUS lines that
count items at a printed rate: "0.5 mark per correct bass note under each chord
symbol (0.5 X 20)", "1 mark for each chord that is part of a good progression
in all chord boxes" (22 marks). `harmony_criteria` reads one question's table
off the scheme page and returns the card's criteria in the order printed:

  * a band criterion (Melody, Descant): one band per printed row, the row's
    first descriptor as the band's label and the rest as its guidance, the
    row's sub-ranges ("38 – 40 / 36 – 37 / 34 – 35") joined into one band;
  * a counted criterion: the rate line verbatim as its label, its bullets as
    guidance, `counted` {rate, items}, placed on every count 0..items;
  * a quality criterion ("Quality of bass line, including ..."): its bands
    from the small table printed inside its cell.

Every string returned is the scheme's own text, cut at its printed bullets and
line breaks; the caller traces each one against the scheme again.
"""
import re

import fitz

RANGE = re.compile(r'(\d+)\s*[–\-‐]\s*(\d+)|(\d+)')
RATE = re.compile(r'^(\d+(?:\.\d+)?)\s*marks?\s+(?:per|for each)\b', re.I)
RATE_X = re.compile(r'\(\s*(\d+(?:\.\d+)?)\s*[xX×]\s*(\d+)\s*\)')


def clean(text):
    text = re.sub(r'\s+', ' ', (text or '').replace(' ', ' ')).strip()
    return re.sub(r'\(\s+', '(', re.sub(r'\s+\)', ')', text))


def cell_lines(cell):
    """A descriptor cell as its printed items: a bullet starts an item, a line
    that starts in lower case (or with a bracket) continues the one before."""
    out, current = [], ''
    for raw in (cell or '').split('\n'):
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith('•'):
            if current:
                out.append(current)
            current = raw.lstrip('• ').strip()
        elif current and (raw[:1].islower() or raw[:1] in '(,;'):
            current += ' ' + raw
        else:
            if current:
                out.append(current)
            current = raw
    if current:
        out.append(current)
    return [clean(x) for x in out if clean(x)]


def marks_of(cell):
    """Every mark a printed mark cell covers: "38 – 40 / 36 – 37 / 34 – 35" -> 34..40, "2 – 3 / 1 / 0" -> 0..3."""
    nums = []
    for a, b, c in RANGE.findall(cell or ''):
        if a:
            nums += list(range(int(a), int(b) + 1))
        else:
            nums.append(int(c))
    return sorted(set(nums))


def _is_marks(cell):
    return bool(cell) and bool(re.fullmatch(r'[\d\s–\-‐/\n]+', cell)) and bool(re.search(r'\d', cell))


def band_rows(table):
    """[(lines, marks)] for a small band table: a descriptor cell and a mark cell per row."""
    out = []
    for row in table.extract():
        cells = [c for c in row if c and c.strip()]
        mark = next((c for c in reversed(cells) if _is_marks(c)), None)
        desc = next((c for c in cells if not _is_marks(c)), None)
        if not mark or not desc or desc.strip().lower().startswith('quality of'):
            continue
        out.append((cell_lines(desc), marks_of(mark)))
    return out


def _band(lines, marks):
    return {'label': lines[0], 'marks': list(range(min(marks), max(marks) + 1)), 'guidance': lines[1:]}


def harmony_criteria(pdf_path, page, question):
    """The criteria of one Composing Section B question, read off its table on `page` (1-based)."""
    pg = fitz.open(pdf_path)[page - 1]
    tables = pg.find_tables().tables
    main = next(t for t in tables if any('Descriptors' in (c or '') for row in t.extract()[:1] for c in row))
    nested = [t for t in tables if t is not main]
    nested.sort(key=lambda t: t.bbox[1])
    criteria, side, q = [], None, None
    for row in main.extract():
        cells = [c or '' for c in row]
        if cells[0].strip().isdigit():
            q = int(cells[0].strip())
        if q != question:
            continue
        label = next((c.strip() for c in cells[1:3] if c.strip() and not _is_marks(c) and '•' not in c and len(c.strip()) < 20), None)
        if label:
            side = label
        texts = [c for c in cells if c.strip() and not _is_marks(c) and c.strip() != side and not c.strip().isdigit()]
        marks = [c for c in cells[1:] if _is_marks(c)]
        if not texts or not marks:
            continue
        lines = cell_lines(texts[-1])
        first = lines[0]
        mark_cell = marks[0]
        rate = RATE.match(first)
        if rate:
            top = int(mark_cell.strip())
            per = float(rate.group(1))
            x = RATE_X.search(first)
            if x:
                per, items = float(x.group(1)), int(x.group(2))
            else:
                items = round(top / per)
            per = int(per) if per == int(per) else per
            if per * items != top:
                raise SystemExit(f'Q{question}: "{first}" does not make its printed {top}')
            criteria.append({'id': f'{side.lower()}-count', 'label': first, 'maxMarks': top,
                             'permittedMarks': [i * per for i in range(items + 1)],
                             'guidance': lines[1:], 'counted': {'rate': per, 'items': items}})
            continue
        if first.lower().startswith('quality of'):
            top = int(mark_cell.strip())
            inner = nested.pop(0)
            bands = [_band(l, m) for l, m in band_rows(inner)]
            # The cell holds the small band table too: its lines are the bands, not guidance.
            criteria.append({'id': f'{side.lower()}-quality', 'label': first, 'maxMarks': top,
                             'permittedMarks': list(range(top + 1)), 'guidance': [], 'bands': bands})
            continue
        # A band row of the side's own criterion (Melody, Descant).
        band = _band(lines, marks_of(mark_cell))
        own = next((k for k in criteria if k['id'] == side.lower()), None)
        if own is None:
            own = {'id': side.lower(), 'label': side, 'maxMarks': None, 'permittedMarks': None,
                   'guidance': [], 'bands': []}
            criteria.append(own)
        own['bands'].append(band)
    for k in criteria:
        if k['maxMarks'] is None:
            top = max(m for b in k['bands'] for m in b['marks'])
            k['maxMarks'], k['permittedMarks'] = top, list(range(top + 1))
        if k.get('bands'):
            covered = sorted(m for b in k['bands'] for m in b['marks'])
            if covered != list(range(k['maxMarks'] + 1)):
                raise SystemExit(f'Q{question} {k["label"]}: bands cover {covered}, not 0..{k["maxMarks"]}')
    return criteria


def text_blocks_below(pdf_path, page, after_y):
    """The scheme's own paragraphs printed below `after_y` on a page, as items (general points)."""
    pg = fitz.open(pdf_path)[page - 1]
    items = []
    for b in sorted(pg.get_text('blocks'), key=lambda b: b[1]):
        if b[1] <= after_y:
            continue
        items += cell_lines(b[4])
    return items
