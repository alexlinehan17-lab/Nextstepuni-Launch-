"""Engineering's printed layout, put back where a one-line string loses it.

    python3 scripts/markbank/authoring/eng_lists.py      # what each pass would change

Two passes over the finished cards, run last by eng_all.py. Neither adds,
drops or moves a word: each only restores a piece of LAYOUT the page prints.

* vertical_lists -- a list the PAPER prints down the page, one item a row,
  each row opening with the same marker at the same x: a roman "(i)", a typed
  bullet "•", or a bullet the font draws (Symbol's U+F0B7, which the text
  layer drops). The reader joins a block's rows with spaces, so "under the
  following headings: • Temperature • Cooling process • Effects on the steel."
  runs three printed rows into one. Where a card's question text holds two or
  more items of such a list on ONE line, each item is set on a line of its own,
  as printed, and text the paper prints after the list starts a line too. A
  list the paper sets ACROSS one row ("(i) Iron ore, (ii) Galvanised steel,
  (iii) Tuyere, (iv) Tinplate.") is inline on the page and stays inline.

* table_cells -- a scheme answer printed as a two-column table row ("Cast iron"
  in one column, "Cupola furnace" in the next) reaches a row's text as "Cast
  iron Cupola furnace", the two cells run together with nothing between them.
  The rows below were each opened on their page and are tables; the two cells
  are joined with " — ", the separator the deck already reads as a label and
  its value (build-deck.mjs traces each half of an option, the value of a
  row). Keyed by page and printed baseline: the words are read off the page,
  never typed here, and an entry no card uses stops the build.

* degree_signs -- the SEC sets a temperature's degree mark as a raised small
  letter "o" ("40" then a superscript "o" then "C"), and the text layer reports
  the letter: "40oC". Where the PDF's own glyph data proves the raise -- the
  "o" is a span of its own, flagged superscript or set smaller and above its
  digits' baseline, between a number and a C or F -- the card reads "40°C".
  Only a temperature the sitting's paper or scheme prints that way is changed;
  a letter o the page sets on the line stays a letter.
"""
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

import eng_lift                                              # noqa: E402

LEVEL = {'higher': 'hl', 'ordinary': 'ol'}
ROMAN = re.compile(r'^\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)$')
LETTER = re.compile(r'^\([a-z]\)$')
GAP = 20          # pt: a gap this wide ends a printed run of words


def _is_bullet(w):
    return len(w) == 1 and (w == '•' or 0xF000 <= ord(w) <= 0xF0FF)


# --------------------------------------------------------------- lists ---

def _item(ws):
    """An item's words on one row: up to a wide gap, past which a picture's
    caption or label printed on the same baseline is not the item's."""
    out = ws[:1]
    for a, b in zip(ws, ws[1:]):
        if b[0] - a[2] >= GAP:
            break
        out.append(b)
    return [w[4] for w in out]


def _tail(ws):
    """The words past that gap -- a caption, or the item's own second column
    ("Driver assistance        (level 1)")."""
    return [w[4] for w in ws[len(_item(ws)):]]


_LISTS = {}


def paper_lists(year, level):
    """[(page, [item, ...], (top, bottom))] -- each item (marker, words): the marker as the
    card text carries it ('(ii)', '•', or None for a font-drawn bullet) and the
    item's printed words, its continuation rows included."""
    key = (year, level)
    if key in _LISTS:
        return _LISTS[key]
    out = []
    try:
        doc = eng_lift._doc(year, level, 'paper')
    except Exception:                                        # noqa: BLE001
        _LISTS[key] = out
        return out
    for pno in range(len(doc)):
        pg = doc[pno]
        rows = eng_lift._lines(year, level, 'paper', pno + 1,
                               (0, 0, pg.rect.width, pg.rect.height))
        run, kind, x, last_y, tx = [], None, None, None, None
        span = [0, 0]

        def flush():
            if len(run) >= 2:
                out.append((pno + 1, [(m, ' '.join(ws), ' '.join(t)) for m, ws, t in run],
                            (span[0], span[1])))

        for y, ws in rows:
            words = [w[4] for w in ws]
            # The row's marker: a roman, once in the row (two or more set
            # side by side are an inline list), possibly after a letter or a
            # lead-in; or a bullet opening the row (after a letter, if any).
            mk = None
            romans = [i for i, w in enumerate(words) if ROMAN.match(w)]
            if len(romans) == 1 and romans[0] < len(words) - 1:
                i = romans[0]
                mk = ('roman', ws[i][0], words[i], _item(ws[i + 1:]), ws[i + 1][0],
                      _tail(ws[i + 1:]))
            else:
                i = 1 if words and LETTER.match(words[0]) and len(words) > 1 else 0
                if _is_bullet(words[i]) and i < len(words) - 1:
                    mark = '•' if words[i] == '•' else None
                    mk = ('bullet', ws[i][0], mark, _item(ws[i + 1:]), ws[i + 1][0],
                          _tail(ws[i + 1:]))
            if mk and kind == mk[0] and abs(mk[1] - x) <= 4 \
                    and (last_y is None or y - last_y <= 120):
                run.append((mk[2], mk[3], mk[5]))
                span[1] = y
                last_y, tx = y, mk[4]
                continue
            # A row that starts under the current item's words continues it.
            if run and not mk and abs(ws[0][0] - tx) <= 8 and y - last_y <= 18:
                run[-1] = (run[-1][0], run[-1][1] + _item(ws), run[-1][2])
                span[1] = y
                last_y = y
                continue
            # A picture's label printed well right of the list, between two
            # of its rows, neither continues an item nor ends the list.
            if run and not mk and ws[0][0] > tx + 40 and y - last_y <= 30:
                continue
            flush()
            run, kind, x, last_y = [], None, None, None
            if mk:
                run, kind, x, last_y, tx = [(mk[2], mk[3], mk[5])], mk[0], mk[1], y, mk[4]
                span = [y - 12, y]
        flush()
    _LISTS[key] = out
    return out


def _words_re(words, n):
    ws = [re.escape(eng_lift._clean(w)) for w in words[:n] if eng_lift._clean(w)]
    return r'\s+'.join(ws)


def set_lines(text, items):
    """text with each found item of one printed list on its own line."""
    found, cursor = [], 0
    for marker, words, tail in items:
        ws = words.split()
        if not ws:
            continue
        head = _words_re(ws, 2)
        pat = (re.escape(marker) + r'\s*' + head) if marker else head
        m = re.compile(pat).search(text, cursor)
        if not m:
            continue
        # where the item's printed words end, to start what follows on a line
        full = re.compile(((re.escape(marker) + r'\s*') if marker else '')
                          + _words_re(ws, len(ws)))
        f = full.match(text, m.start())
        end = f.end() if f else None
        # the row's own second column, printed past a gap, stays on its line
        if end is not None and tail:
            t = re.compile(r'\s+' + _words_re(tail.split(), len(tail.split()))).match(text, end)
            if t:
                end = t.end()
        found.append((m.start(), end))
        cursor = m.end()
    if len(found) < 2:
        return text
    # only a list that the text runs together: two items on one line
    if all('\n' in text[a:b] for (a, _), (b, _) in zip(found, found[1:])):
        return text
    cuts = [a for a, _ in found]
    # an "OR" printed on its own row between two alternatives' lists
    m = re.search(r'(?:^|\s)(OR)\s+$', text[:cuts[0]])
    if m:
        cuts.append(m.start(1))
    end = found[-1][1]
    if end is not None and text[end:].strip() and text[end:end + 1].isspace():
        after = end + len(text[end:]) - len(text[end:].lstrip())
        cuts.append(after)
        # the "OR" printed on its own row before the other alternative
        m = re.match(r'OR\s+(?=\S)', text[after:])
        if m:
            cuts.append(after + m.end())
    for at in sorted(set(cuts), reverse=True):
        k = at
        while k > 0 and text[k - 1] in ' \t':
            k -= 1
        if k == 0 or text[k - 1] == '\n':
            continue
        text = text[:k] + '\n' + text[at:]
    return text


def vertical_lists(cards):
    """Set each card's runs-together vertical lists on their lines. -> [ids]"""
    changed = []
    for c in cards:
        lists = paper_lists(c['year'], LEVEL[c['level']])
        text = c.get('questionText') or ''
        new = text
        for _, items, _ in lists:
            new = set_lines(new, items)
        if new != text:
            c['questionText'] = new
            changed.append(c['id'])
    return changed


# --------------------------------------------------------------- cells ---

# (year, level, scheme page, printed baseline) -> what the row is. Each
# opened on its page: a table whose two columns the row's text runs together.
CELL_ROWS = {
    (2014, 'hl', 10, 178): 'Q2(b)(ii): "From the graph" and the value read off it',
    (2014, 'ol', 8, 670): 'Q2(c)(i): metal and furnace columns',
    (2014, 'ol', 8, 684): 'Q2(c)(i): metal and furnace columns',
    (2014, 'ol', 8, 698): 'Q2(c)(i): metal and furnace columns',
    (2014, 'ol', 9, 721): 'Q2(d): alloy and use columns',
    (2014, 'ol', 9, 735): 'Q2(d): alloy and use columns',
    (2014, 'ol', 14, 723): 'Q5(d): item and plastic columns',
    (2014, 'ol', 14, 737): 'Q5(d): item and plastic columns',
    (2016, 'ol', 9, 334): 'Q2(b): metal and furnace columns',
    (2016, 'ol', 9, 348): 'Q2(b): metal and furnace columns',
    (2016, 'ol', 9, 362): 'Q2(b): metal and furnace columns',
    (2018, 'ol', 8, 115): 'Q2(a): "Name:" and "Function:" columns',
    (2018, 'ol', 8, 130): 'Q2(a): "Name:" and "Function:" columns',
    (2018, 'ol', 18, 296): 'Q7(b)(iv): the asked value and its answer',
    (2021, 'ol', 9, 146): 'Q2(a): "Name:" and "Function:" columns',
    (2021, 'ol', 9, 161): 'Q2(a): "Name:" and "Function:" columns',
    (2024, 'ol', 24, 516): 'Q7(c): instrument and use columns',
    (2024, 'ol', 24, 665): 'Q7(c): instrument and use columns',
}

def cell_pair(year, level, page, baseline):
    """(left, right): the printed row's two cells, split at its wide gap."""
    pg = eng_lift._doc(year, level, 'scheme')[page - 1]
    rows = eng_lift._lines(year, level, 'scheme', page,
                           (0, baseline - 14, 430, baseline + 5))
    hit = [ws for y, ws in rows if abs(y - baseline) <= 3]
    if not hit:
        raise SystemExit(f'eng_lists: {year} {level} p{page} y{baseline}: no printed row')
    ws = hit[0]
    runs = [[ws[0]]]
    for a, b in zip(ws, ws[1:]):
        if b[0] - a[2] >= GAP:
            runs.append([b])
        else:
            runs[-1].append(b)
    if len(runs) != 2:
        raise SystemExit(f'eng_lists: {year} {level} p{page} y{baseline}: '
                         f'{len(runs)} cells, not two')
    del pg
    return tuple(eng_lift._clean(' '.join(w[4] for w in r)) for r in runs)


def _texts(row):
    if 'verbatim' in row:
        yield ('verbatim', None)
    for i, _ in enumerate(row.get('accepts') or []):
        yield ('accepts', i)
    g = row.get('group')
    if g:
        for i, _ in enumerate(g.get('options') or []):
            yield ('options', i)


def table_cells(cards):
    """Join each listed table row's two cells with " — ". -> [ids]"""
    changed, used = [], set()
    present = {(c['year'], LEVEL[c['level']]) for c in cards}
    rows = {k: v for k, v in CELL_ROWS.items() if k[:2] in present}
    for (year, level, page, base), _why in rows.items():
        left, right = cell_pair(year, level, page, base)
        pat = re.compile(re.escape(left) + r'\s+' + re.escape(right))
        for c in cards:
            if c['year'] != year or LEVEL[c['level']] != level:
                continue
            hit = False
            for row in c['rows']:
                for field, i in _texts(row):
                    if field == 'verbatim':
                        old = row['verbatim']
                    elif field == 'accepts':
                        old = row['accepts'][i]
                    else:
                        old = row['group']['options'][i]
                    new = pat.sub(lambda m: f'{left} — {right}', old)
                    if new != old:
                        hit = True
                        if field == 'verbatim':
                            row['verbatim'] = new
                        elif field == 'accepts':
                            row['accepts'][i] = new
                        else:
                            row['group']['options'][i] = new
            if hit:
                used.add((year, level, page, base))
                if c['id'] not in changed:
                    changed.append(c['id'])
    stale = set(rows) - used
    if stale:
        raise SystemExit(f'eng_lists: CELL_ROWS no card carries: {sorted(stale)}')
    return changed


# ------------------------------------------------------------- degrees ---

# The o may stand apart from the unit too: 2010 HL scheme p11 sets "40 o C",
# the o raised so far above its line that a lift reads it as a line of its
# own and the residue joins it back between the number and the unit.
_DEG_TEXT = re.compile(r'(\d+)( ?)o ?([CF])\b')
_PROVEN = {}


def raised_degrees(year, level):
    """{"40oC", "1147 oC", ...}: temperatures this sitting's paper or scheme
    prints with a RAISED o, read off the glyph spans."""
    key = (year, level)
    if key in _PROVEN:
        return _PROVEN[key]
    found = set()
    for doc in ('paper', 'scheme'):
        try:
            pdf = eng_lift._doc(year, level, doc)
        except Exception:
            continue
        for page in pdf:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = line['spans']
                    for i in range(1, len(spans) - 1):
                        s, prev, nxt = spans[i], spans[i - 1], spans[i + 1]
                        if s['text'].strip() != 'o':
                            continue
                        num = re.search(r'(\d+)\s*$', prev['text'])
                        unit = re.match(r'\s*([CF])', nxt['text'])
                        if not num or not unit:
                            continue
                        raised = bool(s['flags'] & 1) or (
                            s['size'] <= 0.8 * prev['size']
                            and prev['origin'][1] - s['origin'][1] >= 1.5)
                        if not raised:
                            continue
                        sep = ' ' if (prev['text'].endswith(' ') or s['text'].startswith(' ')) else ''
                        found.add(f'{num.group(1)}{sep}o{unit.group(1)}')
    _PROVEN[key] = found
    return found


def _deg(text, proven):
    return _DEG_TEXT.sub(lambda m: (f'{m.group(1)}{m.group(2)}°{m.group(3)}'
                                    if f'{m.group(1)}{m.group(2)}o{m.group(3)}' in proven
                                    else m.group(0)), text)


def degree_signs(cards):
    """A proven raised o after a temperature read as the degree sign. -> [ids]"""
    changed = []
    for c in cards:
        blob = json.dumps(c, ensure_ascii=False)
        if not _DEG_TEXT.search(blob):
            continue
        proven = raised_degrees(c['year'], LEVEL[c['level']])
        if not proven:
            continue
        hit = False
        for k in ('questionText', 'stem', 'notes'):
            if isinstance(c.get(k), str):
                new = _deg(c[k], proven)
                hit |= new != c[k]
                c[k] = new
        for row in c.get('rows', []):
            for field, i in _texts(row):
                if field == 'verbatim':
                    old = row['verbatim']
                elif field == 'accepts':
                    old = row['accepts'][i]
                else:
                    old = row['group']['options'][i]
                new = _deg(old, proven)
                if new != old:
                    hit = True
                    if field == 'verbatim':
                        row['verbatim'] = new
                    elif field == 'accepts':
                        row['accepts'][i] = new
                    else:
                        row['group']['options'][i] = new
        for lab in c.get('labelKey') or []:
            if isinstance(lab.get('meaning'), str):
                new = _deg(lab['meaning'], proven)
                hit |= new != lab['meaning']
                lab['meaning'] = new
        if hit:
            changed.append(c['id'])
    return changed


if __name__ == '__main__':
    path = os.path.join(eng_lift.ROOT, 'scripts', 'markbank', 'authored', 'engineering.json')
    cards = json.load(open(path, encoding='utf-8'))
    before = {c['id']: json.dumps(c, ensure_ascii=False) for c in cards}
    v = vertical_lists(cards)
    t = table_cells(cards)
    g = degree_signs(cards)
    for i in g:
        print(f'DEGREE {i}')
    for c in cards:
        if c['id'] in v:
            print(f'LIST  {c["id"]}: {c["questionText"]!r}')
    for c in cards:
        if c['id'] in t:
            print(f'CELLS {c["id"]}')
    print(f'{len(v)} cards set lists on lines; {len(t)} cards joined table cells; '
          f'{len(g)} cards read a raised o as a degree sign')
