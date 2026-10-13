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
breaks = []  # (page, y) of each printed OR between alternatives; a part never runs past one
HEAD = re.compile(r'^(?:Q(?:uestion)?\s*)?(\d{1,2})(?:\s*\.|(?=\s+(?:\(|Option|Any|Two|Four|Answer|[A-Z]))|\s*$)\s*')
MARKER = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\s*')
OPTION = re.compile(r'^Option\s+(One|Two)\b\.?\s*', re.I)
FURNITURE = re.compile(r'^(Leaving Certificate|Agricultural Science\s*[–-]|Marking scheme Agricultural|Page \d+|\d{1,2}$|There is no examination material)', re.I)


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
    for p, rows in enumerate(pages, 1):
        for i, (y0, y1, x, text) in enumerate(rows):
            if re.fullmatch(r'OR|Or', text):
                breaks.append((p, y0))
            if FURNITURE.match(text) or x > 0.30:
                continue
            s = text
            m = HEAD.match(s)
            if m and x < 0.16:
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
                if as_letter:
                    letter, roman = tok, None
                elif as_roman:
                    roman = tok
                else:
                    break
                events.append(((q, opt, letter, roman), p, y0))
                s = s[mk.end():]
    return events, bounds


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
        stop = next((b for b in sorted(breaks) if (page, y) < b < end), None)
        out[key_label(key)] = dict(key=key, start=(page, y), end=stop or end,
                                   stem_end=_point(events, first_child, bounds) if first_child else None)
    return out, bounds


def _point(events, idx, bounds):
    if idx is None:
        return None
    if idx >= len(events):
        last = len(bounds)
        while last > 0 and bounds[last - 1][0] is None:
            last -= 1
        return (last, bounds[last - 1][1] + 0.004)
    return (events[idx][1], events[idx][2])


def _cut(start, end, bounds):
    (p0, y0), (p1, y1) = start, end
    pieces = []
    for p in range(p0, p1 + 1):
        top, bottom = bounds[p - 1]
        if top is None:
            continue
        a = max(y0 - 0.004, 0.0) if p == p0 else top - 0.004
        b = (y1 - 0.003) if p == p1 else bottom + 0.004
        if b - a > 0.01:
            pieces.append(dict(p=p, r=[0, round(a, 3), 1, round(b, 3)]))
    return pieces


def task_regions(table, ref, with_stems=True):
    """Crop for a task ref: question lead-in, letter lead-in (for a roman part), then the part."""
    node = table[0][ref] if isinstance(table, tuple) else table[ref]
    data, bounds = table if isinstance(table, tuple) else (table, None)
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
                regions += _cut(data[label]['start'], data[label]['stem_end'], bounds)
    regions += _cut(node['start'], node['end'], bounds)
    return regions


if __name__ == '__main__':
    table = spans(sys.argv[1])
    refs = sys.argv[2:] or list(table[0])
    for ref in refs:
        print(ref, task_regions(table, ref))
