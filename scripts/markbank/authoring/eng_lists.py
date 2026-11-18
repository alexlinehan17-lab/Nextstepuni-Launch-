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

* alternative_menus -- one marking point the scheme answers several ways
  ("Ratchet and pawl ... / Micrometer ... / Lathe tailstock ...", any one of
  them; a column's interchangeable properties) is an `alt` row whose
  alternatives the session prints run together, joined with "or", in ONE
  row. On a phone a student cannot find the answer they wrote in a
  twelve-mark paragraph of three. Each alternative becomes an option of its
  own in an any-N menu, the kind the any-N tariffs already use, claimed
  once at the row's price: count 1, each option the row's marks. The
  options are the row's own lifted strings, unchanged and in order; no
  text is split. A row on an OR route keeps its route (a menu pick commits
  the route as a tick does, since the shared session fix of 13 November),
  and a row the scheme prices only with its question becomes a menu with no
  price of its own, as its card states the question's total.

* or_routes -- a 2021-2025 Higher card that prints two (c) branches either
  side of an OR ("Outline how weld cracks ... form. OR Explain the following
  terms in relation to the autonomous mobile robots") and is priced only as
  a whole ('4 + 4', or the question's total) listed both branches' answers
  as one list, so a student who answered one branch in full read as having
  missed half. Each branch becomes a route of its own: the rows before the
  OR are route 'a', the rows from the one named in OR_BRANCH_B on are route
  'b'. One card (2024 HL Q8(c)(ii)) carried no row for the branch before its
  OR although the scheme prints one; that row is lifted from the scheme's
  extracted text, checked there word for word, and opens route 'a'.
"""
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

import eng_lift                                              # noqa: E402

LEVEL = {'higher': 'hl', 'ordinary': 'ol'}


def sitting(card):
    """(year, level token) of the papers a card was lifted from: a deferred
    card's ('eng-2022-hl-deferred-...') are its own sitting's (eng_deferred)."""
    level = LEVEL[card['level']]
    if re.match(r'^eng-\d{4}-(?:hl|ol)-deferred-', card['id']):
        level += '-deferred'
    return card['year'], level
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
        lists = paper_lists(*sitting(c))
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
    present = {sitting(c) for c in cards}
    rows = {k: v for k, v in CELL_ROWS.items() if k[:2] in present}
    for (year, level, page, base), _why in rows.items():
        left, right = cell_pair(year, level, page, base)
        pat = re.compile(re.escape(left) + r'\s+' + re.escape(right))
        for c in cards:
            if sitting(c) != (year, level):
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
        proven = raised_degrees(*sitting(c))
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


def alternative_menus(cards):
    """Each alt row with listed alternatives becomes a count-1 any-N menu."""
    changed = []
    for card in cards:
        whole = card['tariffModel'].get('kind') == 'questionTotal'
        if card['tariffModel'].get('kind') != 'fixed' and not whole:
            continue
        for i, row in enumerate(card['rows']):
            accepts = row.get('accepts') or []
            if row.get('kind') != 'alt' or not accepts \
                    or (row.get('marks') is None) != whole:
                continue
            options = [row['verbatim']] + list(accepts)
            if len(set(options)) != len(options):
                raise SystemExit(f'alternative_menus {card["id"]} {row["id"]}: an alternative '
                                 f'is listed twice')
            menu = {'id': row['id'], 'kind': 'anyN', 'verbatim': options[0],
                    'marks': row['marks'],
                    'group': {'claimMax': 1, 'perOption': row['marks'], 'options': options}}
            for key, value in row.items():
                if key not in ('id', 'kind', 'verbatim', 'marks', 'accepts'):
                    menu[key] = value
            card['rows'][i] = menu
            if card['id'] not in changed:
                changed.append(card['id'])
    return changed



# The first row of route 'b' on each OR card, read off the card's own rows
# against the question's two branches (rows before it are the first branch).
OR_BRANCH_B = {
    'eng-2021-hl-q8-c-i': 'r-3', 'eng-2021-hl-q8-c-ii': 'r-5',
    'eng-2021-hl-q9-c-i': 'r-3', 'eng-2021-hl-q9-c-ii': 'r-2',
    'eng-2022-hl-q6-c-i': 'r-4', 'eng-2022-hl-q6-c-ii': 'r-3',
    'eng-2022-hl-q8-c-i': 'r-7', 'eng-2022-hl-q8-c-ii': 'r-3',
    'eng-2022-hl-q9-c-i': 'r-2', 'eng-2022-hl-q9-c-ii': 'r-4',
    'eng-2023-hl-q6-c-i': 'r-4', 'eng-2023-hl-q6-c-ii': 'r-2',
    'eng-2023-hl-q8-c-i': 'r-2', 'eng-2023-hl-q8-c-ii': 'r-5',
    'eng-2023-hl-q9-c-i': 'r-3', 'eng-2023-hl-q9-c-ii': 'r-4',
    'eng-2024-hl-q8-c-i': 'r-5', 'eng-2024-hl-q8-c-ii': 'r-1',
    'eng-2024-hl-q9-c-i': 'r-7', 'eng-2024-hl-q9-c-ii': 'r-5',
    'eng-2025-hl-q8-c-i': 'r-3', 'eng-2025-hl-q8-c-ii': 'r-4',
}

# A first branch the scheme answers and the card carried no row for:
# card id -> (new row id, the scheme's own words). 2024 HL Q8(c)(ii) asks
# "Identify any two lubricants commonly used when machining. OR Outline two
# safety features ..."; the scheme prints "(ii) Lubricating materials: Oil,
# grease, graphite, PTFE, etc." and then the safety features.
OR_BRANCH_A_LIFTED = {
    'eng-2024-hl-q8-c-ii': ('r-5', 'Lubricating materials: Oil, grease, graphite, PTFE, etc.'),
}


def or_routes(cards):
    """Each branch of a 2021-2025 Higher OR card becomes a route of its own."""
    by_id = {c['id']: c for c in cards}
    missing = sorted(set(OR_BRANCH_B) - set(by_id))
    if missing:
        raise SystemExit(f'or_routes: no card {missing}')
    for cid, first_b in OR_BRANCH_B.items():
        card = by_id[cid]
        if card['tariffModel'].get('kind') == 'fixed' or ' OR ' not in card['questionText']:
            raise SystemExit(f'or_routes {cid}: not a whole-priced OR card')
        if any(r.get('route') for r in card['rows']):
            raise SystemExit(f'or_routes {cid}: already has routes')
        if cid in OR_BRANCH_A_LIFTED:
            rid, text = OR_BRANCH_A_LIFTED[cid]
            md = os.path.join(eng_lift.ROOT, 'examiner-reports', 'engineering', 'schemes',
                              f'{card["year"]}-{LEVEL[card["level"]]}.md')
            if text not in open(md, encoding='utf-8').read():
                raise SystemExit(f'or_routes {cid}: {text!r} is not in {md}')
            if any(r['id'] == rid for r in card['rows']):
                raise SystemExit(f'or_routes {cid}: row {rid} exists')
            card['rows'].insert(0, {'id': rid, 'kind': 'point', 'verbatim': text, 'marks': None})
        ids = [r['id'] for r in card['rows']]
        if first_b not in ids or ids.index(first_b) == 0:
            raise SystemExit(f'or_routes {cid}: {first_b} does not open a second branch')
        cut = ids.index(first_b)
        for i, row in enumerate(card['rows']):
            row['route'] = 'a' if i < cut else 'b'
    return sorted(OR_BRANCH_B)


if __name__ == '__main__':
    path = os.path.join(eng_lift.ROOT, 'scripts', 'markbank', 'authored', 'engineering.json')
    cards = json.load(open(path, encoding='utf-8'))
    before = {c['id']: json.dumps(c, ensure_ascii=False) for c in cards}
    v = vertical_lists(cards)
    t = table_cells(cards)
    g = degree_signs(cards)
    m = alternative_menus(cards)
    for i in m:
        print(f'MENU  {i}')
    for i in g:
        print(f'DEGREE {i}')
    for c in cards:
        if c['id'] in v:
            print(f'LIST  {c["id"]}: {c["questionText"]!r}')
    for c in cards:
        if c['id'] in t:
            print(f'CELLS {c["id"]}')
    print(f'{len(v)} cards set lists on lines; {len(t)} cards joined table cells; '
          f'{len(g)} cards read a raised o as a degree sign; '
          f'{len(m)} cards set alternatives as menus')
