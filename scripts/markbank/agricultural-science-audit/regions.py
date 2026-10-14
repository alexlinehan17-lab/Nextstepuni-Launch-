"""Locate every question and part of a legacy (pre-2021) Agricultural Science paper or scheme.

    python3 scripts/markbank/agricultural-science-audit/regions.py <pdf> [ref ...]

Reads the PDF's text lines, follows the printed numbering (question heads, Option One/Two,
(a)-(j), (i)-(x)) and records where each part starts and ends on the page. A review module
asks for a task's crop with task_regions(): the question's own lead-in, the letter's lead-in
for a roman part, then the part itself, split across pages where the part runs on.

The result is a FIRST DRAFT of the crops. Every crop is still rendered and inspected
(render_pairs.py), and a module overrides any region the numbering cannot place.
"""
import re
import sys

import fitz

ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
LETTERS = 'abcdefghijklmnop'
breaks = []  # (page, y) of each printed OR or section heading; see spans() for when one ends a part
SECTION = re.compile(r'^SECTION\s+(?:ONE|TWO|THREE|A|B|C)\b', re.I)
HEAD = re.compile(r'^(?:Q(?:uestion)?\s*)?(\d{1,2})(?:\s*\.|(?=\s+(?:\(|Option|Any|Two|Four|Answer|[A-Z]))|\s*$)\s*')
MARKER = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\s*')
OPTION = re.compile(r'^Option\s+(One|Two)\b\.?\s*', re.I)
FURNITURE = re.compile(r'^(Leaving Certificate|Agricultural Science\s*[–-]|Marking scheme Agricultural|Page \d+|\d{1,2}$|There is no examination material|\[OVER\]$)', re.I)


def _lines(pdf):
    out = []
    with fitz.open(pdf) as doc:
        for n, page in enumerate(doc):
            H, W = page.rect.height, page.rect.width
            rows = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    text = ' '.join(''.join(span['text'] for span in line['spans']).split())
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    rows.append((y0 / H, y1 / H, x0 / W, text))
            rows.sort(key=lambda r: (round(r[0], 2), r[2]))
            out.append(rows)
    return out


def _content_bounds(rows):
    body = [r for r in rows if not FURNITURE.match(r[3])]
    if not body:
        return None, None
    return min(r[0] for r in body), max(r[1] for r in body)


def parse(pdf, max_question=20):
    """[(key, page, y)] marker events in reading order, plus per-page content bounds."""
    pages = _lines(pdf)
    events = []
    q = opt = letter = roman = None
    bounds = [_content_bounds(rows) for rows in pages]
    breaks.clear()
    # A paper that names its questions ("Question 2.") numbers lists inside them with bare
    # digits ("2. Explain your answer."): there, only a named head opens a question.
    named = any(re.match(r'^Question\s+\d+\s*\.', r[3]) for rows in pages for r in rows)
    for p, rows in enumerate(pages, 1):
        for i, (y0, y1, x, text) in enumerate(rows):
            if re.fullmatch(r'OR|Or', text) or SECTION.match(text):
                breaks.append((p, y0))
            if FURNITURE.match(text) or x > 0.30:
                continue
            s = text
            m = HEAD.match(s)
            if m and x < 0.16 and (not named or s.startswith('Q')):
                n = int(m.group(1))
                rest = s[m.end():]
                ahead = rest or (rows[i + 1][3] if i + 1 < len(rows) else '')
                o = OPTION.match(ahead.strip())
                restart = q is not None and n == q and o is not None
                if (q is None and n == 1) or (q is not None and n == q + 1 and n <= max_question) or restart:
                    q, opt, letter, roman = n, (o.group(1).title() if o else None), None, None
                    events.append(((q, opt, None, None), p, y0))
                    s = rest[o.end():] if (o and rest) else rest
            o = OPTION.match(s)
            if o and q is not None:
                opt = o.group(1).title()
                last = events[-1] if events else None
                if not (last and last[0] == (q, opt, None, None)):
                    events.append(((q, opt, None, None), p, y0))
                letter = roman = None
                s = s[o.end():]
            while q is not None:
                mk = MARKER.match(s)
                if not mk:
                    break
                tok = mk.group(1)
                nxt_letter = 'a' if letter is None else (LETTERS[LETTERS.index(letter) + 1] if letter in LETTERS[:-1] else None)
                nxt_roman = 'i' if roman is None else (ROMANS[ROMANS.index(roman) + 1] if roman in ROMANS[:-1] else None)
                as_letter = tok == nxt_letter
                as_roman = tok == nxt_roman
                if as_letter and as_roman:
                    later = ' '.join(r[3] for r in rows[i + 1:i + 14])
                    following = f'({LETTERS[LETTERS.index(tok) + 1]})'
                    head = later.split('(ii)')[0] if '(ii)' in later else later
                    as_roman = '(ii)' in later and following not in head
                    as_letter = not as_roman
                if not as_letter and not as_roman and letter and tok == letter:
                    # A letter printed twice (2018 OL Q13 prints a second "(a)" where the
                    # scheme has (b)): when the letter after the missing one follows before
                    # the missing one or the next question, the repeat is the missing letter.
                    missing = LETTERS[LETTERS.index(letter) + 1]
                    for later in [r[3] for r in rows[i + 1:]] + [r[3] for page in pages[p:] for r in page]:
                        mk2 = MARKER.match(later)
                        if HEAD.match(later) and later.startswith('Q') or (mk2 and mk2.group(1) == missing):
                            break
                        if mk2 and mk2.group(1) == LETTERS[LETTERS.index(missing) + 1]:
                            tok, as_letter = missing, True
                            break
                if as_letter:
                    letter, roman = tok, None
                elif as_roman:
                    roman = tok
                else:
                    break
                events.append(((q, opt, letter, roman), p, _heading_top(rows, i)))
                s = s[mk.end():]
    return events, bounds


def _heading_top(rows, i):
    """Where a marked part starts. Some schemes print a part's italic heading half a line
    ABOVE its (b) marker ("Using footbaths:" sits beside, not below, the marker's top), so the
    part starts at the highest line that overlaps the marker's own line by 15% of its
    height or more. A neighbour's line box only touches the marker's by a hair, and the marks
    column (far right) belongs to whatever row it prices, so only the text column beside the
    marker counts, and only a heading (a line ending in a colon, or the part's own marker line):
    the last line of the previous answer can overlap the marker's box just as much."""
    y0, y1, x = rows[i][0], rows[i][1], rows[i][2]
    height = y1 - y0
    heading = lambda text: text.rstrip().endswith(':') or MARKER.match(text)
    tops = [r[0] for r in rows if x <= r[2] < x + 0.3 and r[0] < y0 and heading(r[3])
            and min(r[1], y1) - max(r[0], y0) >= 0.15 * height]
    return min([y0] + tops)


def key_label(key):
    q, opt, letter, roman = key
    out = f'Q{q}' + (f' Option {opt}' if opt else '')
    if letter:
        out += f' ({letter})' if opt else f'({letter})'
    if roman:
        out += f'({roman})'
    return out


def _descends(child, parent):
    return all(c == p or p is None for c, p in zip(child, parent)) and child != parent and child[:2] == parent[:2]


def spans(pdf):
    events, bounds = parse(pdf)
    out = {}
    for idx, (key, page, y) in enumerate(events):
        # extent: until the next event that is not a descendant
        end_idx = next((j for j in range(idx + 1, len(events)) if not _descends(events[j][0], key)), len(events))
        first_child = idx + 1 if idx + 1 < len(events) and _descends(events[idx + 1][0], key) else None
        end = _point(events, end_idx, bounds)
        # An OR between two Options (or a section heading) ends a part; an OR inside a part's
        # answer (two methods of one experiment) does not. The difference is what follows it:
        # a question or Option head, or just the next lettered part.
        def separates(b):
            nxt = next((e for e in events if (e[1], e[2]) > b), None)
            return nxt is None or nxt[0][2] is None
        stop = next((b for b in sorted(breaks) if (page, y) < b < end and separates(b)), None)
        out[key_label(key)] = dict(key=key, start=(page, y), end=stop or end,
                                   stem_end=_point(events, first_child, bounds) if first_child else None)
    return out, list(bounds) + [pdf]  # the source pdf rides last, for boundary snapping


def _point(events, idx, bounds):
    if idx is None:
        return None
    if idx >= len(events):
        last = len(bounds)
        while last > 0 and bounds[last - 1][0] is None:
            last -= 1
        return (last, bounds[last - 1][1] + 0.004)
    return (events[idx][1], events[idx][2])


_RASTERS = {}
INK = 220  # a grey this light still shows as a dot in a crop, so it counts as ink


def _ink_rows(pdf, page):
    """Per-row ink counts of a rendered page, cached."""
    key = (pdf, page)
    if key not in _RASTERS:
        with fitz.open(pdf) as doc:
            pix = doc[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), colorspace=fitz.csGRAY)
        w, h, data = pix.width, pix.height, pix.samples
        _RASTERS[key] = [sum(1 for v in data[r * w:(r + 1) * w] if v < INK) for r in range(h)]
    return _RASTERS[key]


def snap(pdf, page, y, before=0.012, after=0.006):
    """Move a boundary into the gap between two printed lines near y (line boxes overlap; the
    gap between the glyphs is where a crop should cut).

    A line box often starts a few pixels above its glyphs, so the window reaches a little past
    y. Among the rows that are as empty as the window allows (table borders keep a few pixels
    in every row), the one nearest y wins: an earlier, cleaner gap between two lines of the
    SAME part must not pull the cut back through that part's last line. The cut then moves
    toward the middle of that gap (at most 0.004 of the page), so rounding a region to three
    decimals cannot land it on a neighbouring line's ascenders or descenders."""
    if pdf is None:
        return y
    rows = _ink_rows(pdf, page)
    h = len(rows)
    lo, hi = max(0, int((y - before) * h)), min(h - 1, int((y + after) * h))
    floor = min(rows[lo:hi + 1])
    empty = lambda r: rows[r] <= floor + 1
    best = min((r for r in range(lo, hi + 1) if empty(r)), key=lambda r: abs(r - y * h))
    first, last = best, best
    while first > 0 and empty(first - 1):
        first -= 1
    while last < h - 1 and empty(last + 1):
        last += 1
    reach = int(0.004 * h)
    middle = min(max((first + last) / 2, best - reach), best + reach)
    return middle / h


def _cut(start, end, bounds, pdf=None):
    (p0, y0), (p1, y1) = start, end
    pieces = []
    for p in range(p0, p1 + 1):
        top, bottom = bounds[p - 1]
        if top is None:
            continue
        # Line boxes overlap by a hair: start just inside this line's box and stop just
        # inside the next one's, so neither neighbour's descenders nor ascenders leak in.
        a = snap(pdf, p, y0, before=0.006, after=0.006) if p == p0 else top - 0.004
        b = snap(pdf, p, y1) if p == p1 else bottom + 0.004
        if b - a > 0.01:
            pieces.append(dict(p=p, r=[0, round(a, 3), 1, round(b, 3)]))
    return pieces


def task_regions(table, ref, with_stems=True):
    """Crop for a task ref: question lead-in, letter lead-in (for a roman part), then the part."""
    data, bounds = table
    node = data[ref]
    pdf, bounds = bounds[-1], bounds[:-1]
    key = node['key']
    regions = []
    if with_stems:
        q, opt, letter, roman = key
        parents = [(q, opt, None, None)]
        if roman:
            parents.append((q, opt, letter, None))
        for parent in parents:
            label = key_label(parent)
            if label != ref and label in data and data[label]['stem_end']:
                regions += _cut(data[label]['start'], data[label]['stem_end'], bounds, pdf)
    regions += _cut(node['start'], node['end'], bounds, pdf)
    return regions


if __name__ == '__main__':
    table = spans(sys.argv[1])
    refs = sys.argv[2:] or list(table[0])
    for ref in refs:
        print(ref, task_regions(table, ref))
