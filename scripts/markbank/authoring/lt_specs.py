#!/usr/bin/env python3
"""Lithuanian cards the shared generator (lt_all.py) refuses, carded by the
rulings since (languages-q3 lane, 20 Nov 2026).

    python3 scripts/markbank/authoring/lt_specs.py listen 2026 hl     # review one sitting's listening cards

LISTENING (CARD-STANDARD 10g). Every listening ask of a sitting is read from
the scheme's own lines by lt_listen.py (100% of the paper's listening asks,
2022-2026), and its rows are lifted from those lines by the approved shapes:

* one answer under a priced head .................... a point row at the price
* several answers, no directive ..................... any one of them, at the price
* "One of:" / "Any two of:" + the printed split ..... an anyN menu at the split
* a full answer beside lesser or part answers ....... one menu, claim one, the full
  answer at its printed marks and each lesser one at
  its own, optionOf the fuller answer (lead ruling
  (B), 20 Nov 2026; the Portuguese standing ruling)
* a true/false tick grid (CARD-STANDARD 10c) ........ one card, a verdict row per
  statement at the printed split, the column read
  from the tick's place on the scheme PDF

Nothing is typed: every option is cut from a scheme line by its printed
bullet and price, and the deck's provenance gate traces it. A record no shape
fits is REFUSED with its lines named, never guessed (`overrides`).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import lt_listen                                                    # noqa: E402
from lt_paper import LtPaper                                        # noqa: E402
from lt_topics import topic_for, concept_for, answer_language, language_note  # noqa: E402
from paper_census import key_label, LT_FOLDED_ASKS                  # noqa: E402

SUBJECT = 'lithuanian'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TITLE = {'hl': 'Higher', 'ol': 'Ordinary'}
MAX_OPTIONS = 16
SCHEMES = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'schemes')
NBSP = '\xa0'

CELL_SPLIT = re.compile(r'\s*[•]\s*')
TRAIL_PRICE = re.compile(r'\s*(\d{1,2})\s*[Mm]arks?\s*$')
TRAIL_SPLIT = re.compile(r'\s*\((\d)\s*[x×]\s*(\d{1,2})(?:\s*[Mm]arks?)?\)\s*$')
HEAD_PRICE = re.compile(r'(\d{1,2})\s*[Mm]arks?\b')
HEAD_SPLIT = re.compile(r'\((\d)\s*[x×]\s*(\d{1,2})(?:\s*[Mm]arks?)?\)')
DIRECTIVE_N = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
TICK = re.compile(r'[✓✔]')
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


class Refused(Exception):
    pass


class NeedColumns(Exception):
    """A two-column answer list whose cells wrap: read it off the page."""


def card_id(year, level, key):
    section, q, letter, roman = key
    parts = ['lt', str(year), level, str(section).lower(), str(q)]
    if letter:
        parts.append(letter)
    if roman:
        parts.append(str(roman))
    return '-'.join(parts)


def _norm(t):
    return re.sub(r'\s+', ' ', (t or '').replace(NBSP, ' ')).strip()


def _words(t):
    return {w.lower() for w in WORD.findall(t)}


# ------------------------------------------------------------- the record ---
def read_record(raw, rec):
    """The head's price and split, the directive, and every answer cell with
    its own printed price, from the record's scheme lines."""
    head = _norm(' '.join(raw[n - 1] for n in rec.head))
    price = split = None
    if TICK.search(head) and not lt_listen.TICK_HEAD.search(head):
        # A statement of a section-wide true/false table, printed as its own
        # numbered question: the statement is the head (and any line it wraps
        # onto), the price is the section's own split.
        own = None
        statement = _norm(TICK.sub('', re.sub(r'^(\d{1,2}\.\s*)?\(([a-h])\)\s*', '', head)))
        mp = TRAIL_PRICE.search(statement)
        if mp:
            own, statement = int(mp.group(1)), statement[:mp.start()].strip()
        for n in rec.lines:
            t = _norm(TICK.sub('', raw[n - 1]))
            if lt_listen.BULLET.match(t):
                raise Refused(f'a true/false statement with an answer line: {t!r}')
            mp = TRAIL_PRICE.search(t)
            if mp:
                own, t = int(mp.group(1)), t[:mp.start()].strip()
            if t:
                statement = _norm(statement + ' ' + t)
        if own is None:
            sec = _norm(' '.join(raw[n - 1] for n in rec.section_lines))
            ms = HEAD_SPLIT.search(sec) or re.search(r'\b(\d)\s*[x×]\s*(\d{1,2})\s*[Mm]arks?\b', sec)
            if not ms:
                raise Refused('a true/false statement with no price of its own and no section split')
            own = int(ms.group(2))
        return {'head': head, 'price': own, 'split': (1, own), 'directive': None,
                'cells': [], 'table': [], 'statement': statement}
    m = list(HEAD_PRICE.finditer(HEAD_SPLIT.sub(' ', head)))
    if m:
        price = int(m[-1].group(1))
    s = HEAD_SPLIT.search(head)
    if s:
        split = (int(s.group(1)), int(s.group(2)))
    directive, cells, table, rejected = None, [], [], []
    tf_cols = False
    for n in rec.lines:
        t = _norm(raw[n - 1])
        if re.fullmatch(r'Item \d{1,2}', t):
            # Section E's printed sub-heading between its items, not an answer.
            continue
        d = lt_listen.DIRECTIVE.match(t)
        if d:
            w = d.group(1).lower().split()
            directive = 1 if w[0] == 'one' else DIRECTIVE_N.get(w[1], None) or int(w[1])
            continue
        if lt_listen.TF_HEADER.match(t):
            tf_cols = True
            continue
        if tf_cols and (lt_listen.HEAD_LET.match(t) or (table and not lt_listen.BULLET.match(t))):
            if lt_listen.HEAD_LET.match(t):
                table.append({'line': n, 'text': t})
            else:
                table[-1]['text'] += ' ' + t
                table[-1].setdefault('more', []).append(n)
            continue
        if lt_listen.BULLET.match(t):
            parts = [p for p in CELL_SPLIT.split(t) if p.strip()]
            for k, p in enumerate(parts):
                cell = {'line': n, 'text': p.strip(), 'marks': None, 'pos': k, 'of_line': len(parts)}
                ms = TRAIL_SPLIT.search(cell['text'])
                if ms:
                    split = (int(ms.group(1)), int(ms.group(2)))
                    cell['text'] = cell['text'][:ms.start()].strip()
                mp = TRAIL_PRICE.search(cell['text'])
                if mp:
                    cell['marks'] = int(mp.group(1))
                    cell['text'] = cell['text'][:mp.start()].strip()
                cells.append(cell)
            continue
        if re.search(r'[–-]\s*no marks? awarded', t, re.I):
            # an answer the scheme refuses by name: quoted, never a row
            rejected.append(t)
            continue
        if lt_listen._price_only(t) or re.fullmatch(r'\(\d\s*[x×]\s*\d{1,2}\s*[Mm]arks?\)', t):
            ms = HEAD_SPLIT.search(t)
            if ms:
                split = (int(ms.group(1)), int(ms.group(2)))
            mp = HEAD_PRICE.search(HEAD_SPLIT.sub(' ', t))
            if mp and price is None:
                price = int(mp.group(1))
            continue
        ml = re.fullmatch(r'([^?]{2,60}\?)\s+(\S.*)', t)
        if ml and not lt_listen.BULLET.match(t):
            # a labelled answer the scheme prints under the ask's own
            # sub-questions ("How many? 5", "From where? Library")
            cell = {'line': n, 'text': ml.group(2).strip(), 'marks': None, 'pos': 0, 'of_line': 1,
                    'lead': ml.group(1).strip()}
            mp = TRAIL_PRICE.search(cell['text'])
            if mp:
                cell['marks'], cell['text'] = int(mp.group(1)), cell['text'][:mp.start()].strip()
            cells.append(cell)
            continue
        # A wrapped answer: the rest of the last cell (only where that cell
        # stood alone on its line, so the column it belongs to is not in doubt).
        if cells and any(c['of_line'] > 1 for c in cells):
            raise NeedColumns(f'line {n} wraps a cell of a two-column list')
        if not cells:
            # the answer printed without a bullet under a priced head
            cell = {'line': n, 'text': t, 'marks': None, 'pos': 0, 'of_line': 1}
            mp = TRAIL_PRICE.search(t)
            if mp:
                cell['marks'], cell['text'] = int(mp.group(1)), t[:mp.start()].strip()
            cells.append(cell)
            continue
        if cells and cells[-1]['of_line'] == 1:
            cells[-1]['text'] = (cells[-1]['text'] + ' ' + t).strip()
            mp = TRAIL_PRICE.search(cells[-1]['text'])
            if mp:
                cells[-1]['marks'] = int(mp.group(1))
                cells[-1]['text'] = cells[-1]['text'][:mp.start()].strip()
            continue
        raise Refused(f'line {n} fits no shape: {t!r}')
    if split and price is None:
        price = split[0] * split[1]
    return {'head': head, 'price': price, 'split': split, 'directive': directive,
            'cells': cells, 'table': table, 'rejected': rejected}


def column_cells(year, level, raw, rec):
    """The answer cells of a two-column list, read DOWN each column on the
    scheme PDF: a bullet opens a cell, and a fragment with no bullet continues
    the cell above it in its own column. Every word is the page's own."""
    import fitz
    first = next(n for n in rec.lines if lt_listen.BULLET.match(_norm(raw[n - 1])))
    probe = ' '.join(CELL_SPLIT.split(_norm(raw[first - 1]))[1].split()[:3])
    pdf = fitz.open(os.path.join(SCHEMES, f'{year}-{level}.pdf'))
    for page in pdf:
        hits = page.search_for(probe)
        if not hits:
            continue
        top = hits[0].y0 - 2
        frags = {}
        for w in page.get_text('words'):
            if w[1] < top:
                continue
            frags.setdefault((w[5], w[6]), []).append(w)
        lines = sorted(([min(x[0] for x in ws), min(x[1] for x in ws), ' '.join(x[4] for x in sorted(ws, key=lambda x: x[0]))]
                        for ws in frags.values()), key=lambda f: (round(f[1]), f[0]))
        cells, cols = [], []
        for x0, y0, text in lines:
            t = _norm(text)
            if re.match(r'^(\(([a-h])\)|\d\.)\s', t) or t.startswith('Section') or re.fullmatch(r'\d{1,3}', t) \
                    or re.fullmatch(r'Item \d{1,2}', t):
                break
            if lt_listen.BULLET.match(t):
                cells.append({'x': x0, 'text': lt_listen.BULLET.sub('', t).strip()})
                continue
            if lt_listen.DIRECTIVE.match(t):
                continue
            # a continuation: the latest cell above it in its own column (the
            # column whose bullet stands nearest to its left)
            col = [c for c in cells if c['x'] <= x0 + 2]
            if not col:
                # printed left of every bullet, across the page: an answer of
                # its own (2025 OL: "Miestelis / jūra / ... / gražus 1 mark")
                cells.append({'x': x0, 'text': t})
                continue
            band = max(c['x'] for c in col)
            owner = [c for c in col if abs(c['x'] - band) < 3][-1]
            owner['text'] = owner['text'] + ' ' + t
        out = []
        for c in cells:
            text = c['text']
            mp = TRAIL_PRICE.search(text)
            marks = int(mp.group(1)) if mp else None
            if mp:
                text = text[:mp.start()].strip()
            out.append({'line': first, 'text': _norm(text), 'marks': marks, 'pos': 0, 'of_line': 1})
        # each column read DOWN, left column first, as the page prints it
        xs = sorted({round(c['x']) for c in cells})
        out = [o for x in xs for o, c in zip(out, cells) if round(c['x']) == x]
        return out
    raise Refused(f'the two-column list is not on the scheme PDF ("{probe}")')


def rows_for(r, note):
    """The card's rows and total by the approved shapes, or Refused."""
    if r.get('statement'):
        raise Refused('a true/false statement: read by statement_row')
    cells = [c for c in r['cells'] if c['text']]
    if r['table']:
        raise Refused('a tick grid: read by tick_rows')
    if not cells:
        raise Refused('no answer printed')
    if r.get('rejected'):
        note = note + ' The scheme prints ' + '; '.join(f'“{x}”' for x in r['rejected']) + '.'
    priced = [c for c in cells if c['marks'] is not None]
    k = r['directive'] or (r['split'][0] if r['split'] else 1)
    # One bullet the split prices as k details, printed as a list in the line
    # ("Aukštas, stiprus ir gražus" under "(3 x 2 marks)"): cut at its own
    # printed commas and "ir"/"and", only if that gives exactly k details.
    if len(cells) == 1 and not priced and k > 1 and r['split'] and not r['directive']:
        parts = [p for p in re.split(r',\s*|\s+ir\s+|\s+and\s+', cells[0]['text']) if p.strip()]
        if len(parts) == k:
            cells = [dict(cells[0], text=p.strip()) for p in parts]
    # A full answer whose parts the split prices ("(2 x 2 marks)" over a full
    # answer and its two parts at 2): ruling (B), the full answer at k x p.
    unpriced = [c for c in cells if c['marks'] is None]
    if r['split'] and len(unpriced) == 1 and len(priced) == k and k > 1 \
            and all(c['marks'] == r['split'][1] for c in priced):
        unpriced[0]['marks'] = k * r['split'][1]
        priced = [c for c in cells if c['marks'] is not None]
        r = dict(r, directive=1, split=None, price=k * r['split'][1])
        k = 1
    if r['split'] and len(priced) == len(cells) and len(cells) == k + 1 and k > 1 \
            and max(c['marks'] for c in cells) == k * r['split'][1]:
        r = dict(r, directive=1, split=None, price=k * r['split'][1])
        k = 1
    if not priced:
        if r['price'] is None:
            raise Refused('no price printed for the ask or its answers')
        if r['split']:
            count, per = r['split']
            if count * per != r['price']:
                raise Refused(f'the split {r["split"]} does not make {r["price"]}')
        else:
            count, per = k, r['price'] // k
            if count * per != r['price']:
                raise Refused(f'{r["price"]} over {count} answers is not a whole mark')
        if len(cells) == 1 and count == 1:
            return [{'id': 'r-1', 'kind': 'point', 'verbatim': cells[0]['text'], 'marks': per,
                     'contextNote': note}], per
        if len(cells) == count:
            # every printed answer is required: a claimable row each (led by
            # its printed sub-question where the scheme labels it)
            def ctx(i, c):
                lead = f'For “{c["lead"]}”' if c.get('lead') else ''
                if i == 1:
                    return f'{lead}: {note}' if lead else note
                return lead
            return [{'id': f'r-{i}', 'kind': 'point', 'verbatim': c['text'], 'marks': per,
                     **({'contextNote': ctx(i, c)} if ctx(i, c) else {})} for i, c in enumerate(cells, 1)], count * per
        if len(cells) < count:
            raise Refused(f'{count} answers priced over {len(cells)} printed')
        if len(cells) > MAX_OPTIONS:
            raise Refused(f'{len(cells)} answers, over the {MAX_OPTIONS}-option cap')
        return [{'id': 'r-1', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                 'marks': None, 'contextNote': note,
                 'group': {'claimMax': count, 'perOption': per, 'options': [c['text'] for c in cells]}}], count * per
    if len(priced) != len(cells):
        # The head prices the list and some answers print a lower price of
        # their own: an unpriced answer takes the head's per-answer price.
        if r['price'] is None and not r['split']:
            raise Refused('some answers carry their own price and the head prints none')
        per = r['split'][1] if r['split'] else r['price'] // k
        if (r['split'] and r['split'][0] * r['split'][1] != r['price'] and r['price'] is not None) or \
                (not r['split'] and per * k != r['price']):
            raise Refused(f'the head prices {r["price"]} over {k} answers')
        for c in cells:
            if c['marks'] is None:
                c['marks'] = per
            elif c['marks'] > per:
                raise Refused(f'"{c["text"]}" priced {c["marks"]}, above the {per} the head pays an answer')
        r = dict(r, price=k * per)
    top = max(c['marks'] for c in cells)
    fulls = [c for c in cells if c['marks'] == top]
    lessers = [c for c in cells if c['marks'] < top]
    count = k
    if r['split'] and r['split'][1] != top:
        raise Refused(f'the split {r["split"]} disagrees with the answers priced {top}')
    if r['price'] is not None and r['price'] != count * top:
        raise Refused(f'the head prices {r["price"]}, the answers {count} x {top}')
    if not lessers:
        if len(cells) == 1:
            return [{'id': 'r-1', 'kind': 'point', 'verbatim': cells[0]['text'], 'marks': top,
                     'contextNote': note}], top
        return [{'id': 'r-1', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                 'marks': None, 'contextNote': note,
                 'group': {'claimMax': count, 'perOption': top, 'options': [c['text'] for c in cells]}}], count * top
    # Ruling (B): each lesser answer is paid in place of a fuller one. With
    # one full answer (and one answer claimed) it is that one; otherwise the
    # one whose words hold the lesser answer's words, if exactly one does.
    # Where none does, the scheme prices it as an answer of its own, and the
    # card says only that: no relation it does not print.
    options = [c['text'] for c in fulls] + [c['text'] for c in lessers]
    marks = [top] * len(fulls) + [c['marks'] for c in lessers]
    of, extra = [None] * len(fulls), []
    for c in lessers:
        hold = [j for j, f in enumerate(fulls) if _words(c['text']) <= _words(f['text'])]
        i = 0 if (len(fulls) == 1 and k == 1) else (hold[0] if len(hold) == 1 else None)
        of.append(i)
        unit = 'mark' if c['marks'] == 1 else 'marks'
        extra.append(f'The scheme allows “{c["text"]}” for {c["marks"]} {unit}, in place of '
                     f'“{fulls[i]["text"]}”, never beside it.' if i is not None else
                     f'The scheme prices “{c["text"]}” at {c["marks"]} {unit}, as an answer of its own.')
    if len(options) > MAX_OPTIONS:
        raise Refused(f'{len(options)} answers, over the {MAX_OPTIONS}-option cap')
    return [{'id': 'r-1', 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
             'marks': None, 'contextNote': ' '.join([note] + extra),
             'group': {'claimMax': k, 'perOption': top, 'options': options,
                       'optionMarks': marks, 'optionOf': of}}], k * top


def tick_rows(year, level, raw, rec, r, note):
    """A true/false grid: one verdict row per statement, the column read from
    the tick's place against the printed True/False headings on the scheme PDF."""
    import fitz
    if not r['split']:
        raise Refused('a tick grid with no printed split')
    count, per = r['split']
    if len(r['table']) != count:
        raise Refused(f'{len(r["table"])} statements printed, the split prices {count}')
    pdf = fitz.open(os.path.join(SCHEMES, f'{year}-{level}.pdf'))
    rows, total = [], 0
    for i, row in enumerate(r['table'], 1):
        text = TICK.sub('', row['text'])
        text = _norm(re.sub(r'^\(([a-h]|i{1,3}|iv|v|vi)\)\s*', '', text))
        verdict = _verdict(pdf, text)
        rows.append({'id': f'r-{i}', 'kind': 'point', 'verbatim': verdict, 'marks': per,
                     'contextNote': (f'For “{text}”: {note}' if i == 1 else f'For “{text}”')})
        total += per
    return rows, total


def _verdict(pdf, statement):
    """The heading word ("True"/"False", "Teisingai"/"Neteisingai") whose column
    holds the tick on the statement's printed row."""
    probe = ' '.join(statement.split()[:4])
    for page in pdf:
        hits = page.search_for(probe)
        if not hits:
            continue
        y0, y1 = hits[0].y0 - 2, hits[0].y1 + 14
        words = page.get_text('words')
        heads = [w for w in words if w[4] in ('True', 'False', 'Teisingai', 'Neteisingai', 'Teisingas', 'Neteisingas')
                 and w[1] < hits[0].y0]
        ticks = [w for w in words if TICK.search(w[4]) and y0 <= (w[1] + w[3]) / 2 <= y1]
        if not heads or not ticks:
            continue
        x = (ticks[0][0] + ticks[0][2]) / 2
        near = min(heads, key=lambda w: (hits[0].y0 - w[1], abs((w[0] + w[2]) / 2 - x)))
        row_y = near[1]
        line = [w for w in heads if abs(w[1] - row_y) < 3]
        best = min(line, key=lambda w: abs((w[0] + w[2]) / 2 - x))
        return best[4]
    raise Refused(f'no tick found for "{statement}" on the scheme')


# ------------------------------------------------------------- the cards ---
def _recording(year):
    with open(os.path.join(ROOT, 'data', 'lithuanianAudio.json'), encoding='utf-8') as fh:
        for e in json.load(fh):
            if e['year'] == year:
                return e
    raise KeyError(f'no recording for {year}')


def _intro(path, page):
    import fitz
    lines = [_norm(x) for x in fitz.open(path)[page - 1].get_text().split('\n') if _norm(x)]
    hear = next((x for x in lines if x.startswith('You will hear')), None)
    lang = next((x for x in lines if re.match(r'^Answer the questions in (Lithuanian|English)\.?$', x)), None)
    return ' '.join(x for x in (hear, lang) if x), lang


def _bullets_only(rec, raw):
    """The record with its bullet and wrap lines left out (the cells are read
    off the page), so its head, directive and split are read as usual."""
    import copy
    r = copy.copy(rec)
    r.lines = [n for n in rec.lines if lt_listen.DIRECTIVE.match(_norm(raw[n - 1]))
               or lt_listen._price_only(_norm(raw[n - 1]))]
    return r


LABEL = re.compile(r'^[^•\uf0b7\uf0d8]{2,60}\?$')


def group_rows(raw, rec, note):
    """An ask the scheme answers under its own printed sub-questions, each a
    label line ("Kada?", "Iš kurios aikštelės?") over its own answers (2024 OL
    LA Q1(c); lead ruling (a), 20 Nov 2026): one row per group, built by the
    usual shapes. An answer printed with no mark beside a priced one is quoted
    in that group's note, never a row and never a guessed mark."""
    groups, cur = [], None
    for n in rec.lines:
        t = _norm(raw[n - 1])
        if LABEL.match(t) and not lt_listen.BULLET.match(t):
            cur = {'label': t, 'lines': []}
            groups.append(cur)
        elif cur is not None:
            cur['lines'].append(n)
        else:
            raise Refused(f'line {n} before the first sub-question: {t!r}')
    rows, total = [], 0
    for i, g in enumerate(groups, 1):
        import copy
        sub = copy.copy(rec)
        sub.head, sub.lines = rec.head, g['lines']
        r = read_record(raw, sub)
        r['price'] = None
        unpriced = [c for c in r['cells'] if c['marks'] is None]
        priced = [c for c in r['cells'] if c['marks'] is not None]
        if not priced:
            raise Refused(f'the group "{g["label"]}" prices nothing')
        r['cells'] = priced
        lead = f'For “{g["label"]}”'
        extra = ' '.join(f'The scheme also prints “{c["text"]}”. The scheme prints no mark for this shorter answer.'
                         for c in unpriced)
        gnote = (f'{lead}: {note}' if i == 1 else lead) + (f' {extra}' if extra else '')
        if i > 1 and not extra:
            gnote = lead
        grows, gtotal = rows_for(r, gnote if i == 1 else (f'{lead}: {extra}' if extra else lead))
        for row in grows:
            row['id'] = f'r-{len(rows) + 1}'
            rows.append(row)
        total += gtotal
    return rows, total


def listening_cards(year, level, report=False):
    P = LtPaper(year, level, SUBJECT)
    raw = lt_listen.scheme_lines(year, level)
    recs = lt_listen.asks(year, level)
    folded = LT_FOLDED_ASKS.get((SUBJECT, year, level), {})
    child_of = {c: p for p, cs in folded.items() for c in cs}
    rec_audio = _recording(year)
    out, refused, seen = [], [], set()
    for ask in P.aural_asks():
        key = child_of.get(ask.key, ask.key)
        if key in seen:
            continue
        seen.add(key)
        rec = recs.get(key)
        if rec is None:
            refused.append((key, 'no scheme record'))
            continue
        children = [a for a in P.aural_asks() if child_of.get(a.key) == key]
        question = _norm(ask.full_text) if not children else _norm(
            os.path.commonprefix([_norm(a.full_text) for a in children]).rsplit(' ', 1)[0])
        stem, lang_line = _intro(P.aural_path, ask.page)
        # The booklet names the answer language on the section's own page.
        language = (('Lithuanian' if 'Lithuanian' in lang_line else 'English or Irish') if lang_line
                    else answer_language(SUBJECT, question))
        note = language_note(SUBJECT, language, year)
        try:
            seq0 = rec.head[1:] + rec.lines
            if sum(1 for n in seq0 if LABEL.match(_norm(raw[n - 1])) and not lt_listen.BULLET.match(_norm(raw[n - 1]))) >= 2:
                r = {'statement': None, 'table': []}
            else:
                r = None
            try:
                r = r or read_record(raw, rec)
            except NeedColumns:
                r = read_record(raw, _bullets_only(rec, raw))
                r['cells'] = column_cells(year, level, raw, rec)
            seq = rec.head[1:] + rec.lines
            labels = [n for n in seq if LABEL.match(_norm(raw[n - 1])) and not lt_listen.BULLET.match(_norm(raw[n - 1]))]
            if len(labels) >= 2 and not r.get('statement') and not r['table']:
                import copy
                grec = copy.copy(rec)
                # a sub-question label read as the head's wrap belongs to the groups
                grec.head = [x for x in rec.head if x not in labels]
                grec.lines = [x for x in seq if x not in grec.head]
                rows, total = group_rows(raw, grec, note)
            elif r.get('statement'):
                import fitz
                verdict = _verdict(fitz.open(os.path.join(SCHEMES, f'{year}-{level}.pdf')), r['statement'])
                rows, total = [{'id': 'r-1', 'kind': 'point', 'verbatim': verdict, 'marks': r['price'],
                                'contextNote': f'For “{r["statement"]}”: {note}'}], r['price']
            else:
                rows, total = (tick_rows(year, level, raw, rec, r, note) if r['table'] else rows_for(r, note))
        except Refused as e:
            refused.append((key, str(e)))
            continue
        q, letter = key[1], key[2]
        card = {
            'id': card_id(year, level, key),
            'subjectId': SUBJECT,
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            'topicId': topic_for(SUBJECT, year, key[0], q),
            'conceptId': concept_for(question),
            'questionRef': f'{year} {level.upper()} {key_label(key, SUBJECT)}',
            'questionText': question,
            'tariffModel': {'kind': 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'The scheme prices this listening ask {total} {"mark" if total == 1 else "marks"} '
                      f'(scheme lines {rec.head[0]}-{max([rec.head[-1]] + rec.lines)}); the listening booklet '
                      f'prints it on page {ask.page}.' + (f' {rec.note}.' if rec.note else '')),
            'stem': stem,
            'sourceMaterial': {
                'kind': 'source-text',
                'label': 'LISTENING COMPREHENSION',
                'title': f'Section {key[0][1]} — Question {q}' + (f'({letter})' if letter else ''),
                'pages': [ask.page],
                'sourceLabel': 'Aural Paper',
                'attribution': (f'SEC Lithuanian {year} {LEVEL_TITLE[level]} Level Listening '
                                f'Comprehension — © State Examinations Commission.'),
                'presentationNote': 'The question page of the listening booklet. Play the recording, then answer.',
            },
            'audioMaterial': {**rec_audio['source'], 'label': f'Section {key[0][1]} · listening'},
        }
        out.append(card)
    return out, refused


def main():
    if sys.argv[1:2] == ['listen']:
        year, level = int(sys.argv[2]), sys.argv[3]
        cards, refused = listening_cards(year, level)
        for c in cards:
            r = c['rows'][0]
            g = r.get('group')
            print(c['questionRef'], c['totalMarks'], '|', c['questionText'][:60])
            for row in c['rows']:
                g = row.get('group')
                if g:
                    print('     anyN', g['claimMax'], 'x', g['perOption'], g['options'][:6],
                          ('marks ' + str(g.get('optionMarks'))) if g.get('optionMarks') else '',
                          ('of ' + str(g.get('optionOf'))) if g.get('optionOf') else '')
                else:
                    print('     point', row['marks'], '|', row['verbatim'][:70], '|', row.get('contextNote', '')[:50])
        print(f'== {len(cards)} cards; {len(refused)} refused')
        for k, why in refused:
            print('   REFUSED', key_label(k, SUBJECT), '|', why)


if __name__ == '__main__':
    main()
