#!/usr/bin/env python3
"""The Lithuanian reading asks the shared generator (lt_all.py) refused, carded
(languages-q3 lane, 20 Nov 2026). The 306 live cards are never regenerated:
lt_q3_batch.py adds these beside them.

Each card is lt_all's own skeleton (id, reference, task section, topic,
concept, stem, reading text, language note); only its rows are new, and every
row is lifted from the scheme's own lines (the markdown the provenance gate
reads), at a mark the scheme prints for that row: the row's own price or the
printed split above it ("4 Marks (4 x 1)", "6 Marks (3 x 2)"). Nothing is
divided and nothing is typed. The shapes, approved by the coordinator:

  fewer    rows (ii)-(v) of a word-box task whose row (i) the SEC prints
           answered (10d): a card each, the scheme's completed line at the
           split's per-row mark.
  box      a folded "letters under numbers" grid (10c): one card, a point row
           per printed number with the scheme's letter, led by that number's
           half-sentence as the paper prints it.
  order    an ordering task: one card, a point row per action with the
           scheme's position, led by the action; the row the paper prints
           already numbered is the worked example and is named in the note.
  order_row  the same task where the census keeps each row as its own ask
           (2026 OL A Q1(g)): a card per row.
  ticks    a "tick what you will find" list (2024 OL A Q2(h)): one card, a
           point row per option the scheme ticks; the unticked one is named.
  prov     the two two-column answer lists lt_all refused only because the
           flat scheme text broke them (2023 HL A Q1(a), 2026 HL A Q2(a)):
           lt_all's own card, built now that the re-extracted scheme
           (15dbc58f9) holds each answer as one run of words.

Every anchor below is a lookup key into the scheme or the paper (where to
read), never card text; each must match exactly one line.

    python3 scripts/markbank/authoring/lt_reading.py 2026 ol
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

import lt_all  # noqa: E402
from lt_paper import LtPaper  # noqa: E402
from lt_scheme import LtScheme  # noqa: E402

SUBJECT = 'lithuanian'
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'lithuanian', 'schemes')

# (year, level) -> [(shape, (section, q, letter), scheme anchor, extra)]
# extra: for 'order'/'order_row', the actions the PAPER prints already numbered
# (the worked example), read off the paper page (STATUS.md, 10d).
SPECS = {
    (2026, 'ol'): [
        ('fewer', ('A', 1, 'e'), '(e) Išrinkite tinkamą žodį ir jį įrašykite. Remkitės tekstu. (2 dalis)', None),
        # ('order_row', ('A', 1, 'g'), '(g) Sunumeruokite veiksmus pagal jų eiliškumą tekste.',
        #  ['Pasirąžo kėdėje.']),  HELD: the census keeps this task's five rows as five asks, where the
        #  three other ordering tasks are one ask each; a fold is put to the coordinator (20 Nov).
        ('box', ('A', 2, 'a'), '(a) Sudarykite sakinius. Įrašykite atsakymo raidę prie pateiktų skaičių. (1 dalis)', None),
        ('fewer', ('A', 2, 'h'), '(h) Išrinkite tinkamą žodį ir jį įrašykite. Remkitės tekstu. (3 dalis)', None),
        ('box', ('A', 3, 'g'), '(g) Sudarykite sakinius. Įrašykite atsakymo raidę prie pateiktų skaičių. (3 dalis)', None),
    ],
    (2026, 'hl'): [
        ('prov', ('A', 2, 'a'), None, None),
    ],
    (2025, 'ol'): [
        ('box', ('A', 1, 'f'), '(f) Sudarykite sakinius. Įrašykite atsakymo raidę prie žemiau pateiktų skaičių pagal pavyzdį.', None),
        ('order', ('A', 1, 'i'), '(i) Sunumeruokite įvykius eilės tvarka pagal pavyzdį. (3 dalis)', ['Groja didelėje scenoje.']),
        ('box', ('A', 2, 'h'), '(h) Raskite tekste pabrauktų žodžių reikšmes. Įrašykite atsakymo raidę prie žemiau pateiktų', None),
        ('box', ('A', 3, 'g'), '(g) Sudarykite sakinius. Įrašykite atsakymo raidę prie žemiau pateiktų skaičių. (2 dalis)', None),
    ],
    (2024, 'ol'): [
        ('fewer', ('A', 1, 'e'), '(e) Išrinkite tinkamą žodį ir jį įrašykite. (2 dalis) 4 Marks (4 x 1)', None),
        ('order', ('A', 1, 'g'), '(g) Sunumeruokite veiksmus pagal jų eiliškumą tekste. (2 dalis) 10 Marks (5 x 2)',
         ['Pasakotojas paprašo Ričio nubėgti arbatos.']),
        ('box', ('A', 2, 'e'), '(e) Suderinkite sakinius. Įrašykite atsakymo raidę prie žemiau pateiktų skaičių. (2 dalis)', None),
        ('ticks', ('A', 2, 'h'), '(h) Remdamiesi tekstu pažymėkite ( ✓ ), ką rasite Kondigno žaidime. (3 dalis)', None),
        ('box', ('A', 3, 'e'), 'e) Sudarykite sakinius. Įrašykite atsakymo raidę prie žemiau pateiktų skaičių. (2 dalis)', None),
    ],
    (2023, 'ol'): [
        ('order', ('A', 1, 'h'), '(h) Ką veikė Severija? Sunumeruokite įvykius eilės tvarka pagal pavyzdį. (3 dalis)', None),
    ],
    (2023, 'hl'): [
        ('prov', ('A', 1, 'a'), None, None),
    ],
}

SPLIT = re.compile(r'\((\d+)\s*[x×]\s*(\d+)(?:\s*marks?)?\)', re.I)
HEAD = re.compile(r'^\(?[a-j]\)\s')
ROMAN = re.compile(r'^\(?(i{1,3}|iv|v|vi)[.)]\s+')


class Refused(Exception):
    pass


def _norm(t):
    return re.sub(r'\s+', ' ', str(t)).strip()


def _scheme_lines(year, level):
    """The scheme's own pages. The column-runs appendix the provenance gate
    also reads (append-scheme-columns.py) repeats the heads, so an anchor is
    looked up only above it."""
    with open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf-8') as fh:
        text = fh.read()
    return [_norm(l) for l in text.split('<!-- markbank:column-runs -->')[0].split('\n')]


def _block(lines, anchor):
    """The scheme lines of one task: its head line (the anchor), then every
    line up to the next lettered head or page furniture."""
    hits = [i for i, l in enumerate(lines) if l.startswith(anchor)]
    if len(hits) != 1:
        raise Refused(f'scheme anchor {anchor!r} matches {len(hits)} lines')
    i = hits[0]
    out = [lines[i]]
    for l in lines[i + 1:]:
        if not l or l.startswith('## Page') or l.startswith('<!--'):
            continue
        if HEAD.match(l) and not ROMAN.match(l):
            break
        if re.fullmatch(r'\d{1,2}', l):          # a page number
            continue
        if l.startswith('Answer question') or l.startswith('SECTION'):
            break
        out.append(l)
    return out


def _split(block):
    """The printed split (count, per) in the task's head lines."""
    for l in block[:3]:
        m = SPLIT.search(l)
        if m:
            return int(m.group(1)), int(m.group(2)), None
    raise Refused(f'no printed split in {block[:3]}')


def _notation(block):
    """The price exactly as the head prints it, e.g. "4 Marks (4 x 1)"."""
    text = ' '.join(block[:2])
    m = re.search(r'(\d+\s*[Mm]arks?\s*)?\(?\d+\s*[x×]\s*\d+(?:\s*marks?)?\)?', text)
    return _norm(m.group(0)) if m else ''


def _skeleton(P, ask, key, year, level, question, total, rows, notes):
    language = lt_all.answer_language(SUBJECT, question)
    card = {
        'id': lt_all.card_id(SUBJECT, year, level, key),
        'subjectId': SUBJECT,
        'level': lt_all.LEVEL_WORD[level],
        'year': year,
        'section': f'U{key[1]}',
        'topicId': lt_all.topic_for(SUBJECT, year, key[0], key[1]),
        'conceptId': lt_all.concept_for(question),
        'questionRef': lt_all.question_ref(year, level, key),
        'questionText': question,
        'tariffModel': {'kind': 'fixed'},
        'totalMarks': total,
        'rows': rows,
        'notes': notes,
    }
    lead = P.lead(key[0], key[1])
    if lead and len(lead) >= 12:
        card['stem'] = lead
    source = lt_all.source_material(P, ask, language, level, year, SUBJECT)
    if source:
        card['sourceMaterial'] = source
    return card, lt_all.language_note(SUBJECT, language, year)


def _led(rows, note):
    """First row carries the language note after its lead, as tick_rows does."""
    for i, r in enumerate(rows):
        lead = r.pop('_lead', None)
        ctx = f'For “{lead}”' if lead else ''
        if i == 0:
            ctx = f'{ctx}: {note}' if ctx else note
        if ctx:
            r['contextNote'] = ctx
    return rows


def _asks(P, sec, q, letter):
    return [a for a in P.all_asks() if (a.section, a.q, a.letter) == (sec, q, letter)]


def fewer(P, lines, year, level, key3, anchor, _extra):
    block = _block(lines, anchor)
    count, per, _ = _split(block)
    asks = [a for a in _asks(P, *key3) if a.roman and a.roman != 'i']
    if len(asks) != count:
        raise Refused(f'{key3}: {len(asks)} rows asked, the split prices {count}')
    cards = []
    for ask in asks:
        line = next((l for l in block if l.startswith(f'({ask.roman}) ')), None)
        if line is None:
            raise Refused(f'{key3}({ask.roman}): no scheme line')
        answer = line[len(ask.roman) + 3:]
        if not answer.startswith(_norm(ask.text)):
            raise Refused(f'{key3}({ask.roman}): scheme line {answer!r} is not the paper row {ask.text!r} completed')
        card, note = _skeleton(P, ask, ask.key, year, level, _norm(ask.full_text), per, [], '')
        card['rows'] = _led([{'id': 'r-1', 'kind': 'point', 'verbatim': answer, 'marks': per}], note)
        card['notes'] = (f'The scheme prints the tariff as {_notation(block)!r} over rows (ii)-(v); row (i) '
                         f'is printed answered as the worked example. The paper prints this ask on page '
                         f'{ask.page} of the question booklet.')
        cards.append(card)
    return cards


def box(P, lines, year, level, key3, anchor, _extra):
    block = _block(lines, anchor)
    count, per, _ = _split(block)
    nums_i = next(i for i, l in enumerate(block) if re.fullmatch(r'(\d\.\s*)+', l))
    nums = re.findall(r'(\d)\.', block[nums_i])
    letters = block[nums_i + 1].split()
    if len(nums) != len(letters) or not all(re.fullmatch(r'[A-F]', x) for x in letters):
        raise Refused(f'{key3}: numbers {nums} against letters {letters}')
    children = sorted(_asks(P, *key3), key=lambda a: int(a.roman))
    if [a.roman for a in children] != nums:
        raise Refused(f'{key3}: paper rows {[a.roman for a in children]} against scheme {nums}')
    paid = list(zip(nums, letters, children))
    example = None
    if len(paid) == count + 1:
        # the SEC answers number 1 itself ("pagal pavyzdį"): out of the rows
        example, paid = paid[0], paid[1:]
        if not re.search(r'pagal\s+pavyzd', anchor + ' ' + (children[0].stem or '')):
            raise Refused(f'{key3}: one number more than the split pays, and no worked example printed')
    if len(paid) != count:
        raise Refused(f'{key3}: {len(paid)} numbers paid, the split prices {count}')
    stem = _norm(children[0].stem)
    printed = [f'{a.roman}. {_norm(a.text)}' for a in children]
    question = '\n'.join([stem] + printed)
    rows = []
    for n, letter, a in paid:
        left = _norm(re.split(r'\s[A-F]\.\s', ' ' + _norm(a.text) + ' ', maxsplit=1)[0])
        rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'point', 'verbatim': letter, 'marks': per,
                     '_lead': f'{n}. {left}'})
    parent = key3 + (None,)
    card, note = _skeleton(P, children[0], parent, year, level, question, count * per, rows, '')
    _led(card['rows'], note)
    ex = (f' Number {example[0]} is printed answered ("{example[1]}") as the worked example.' if example else '')
    card['notes'] = (f'The scheme prints the tariff as {_notation(block)!r} and answers the grid in one line, '
                     f'"{block[nums_i]}" over "{block[nums_i + 1]}".{ex} The paper prints this task on page '
                     f'{children[0].page} of the question booklet; the census counts it once (10c).')
    return [card]


ROW = re.compile(r'^(?:\((?:i{1,3}|iv|v|vi)\)\s*|(?:i{1,3}|iv|v|vi)\.\s*)?(.+?)\.?\s+(\(?)(\d)(\)?)$')


def _order_rows(block):
    out = []
    for l in block[1:]:
        m = ROW.match(l)
        if m and not l.startswith('Veiksmas') and not SPLIT.fullmatch(l):
            out.append({'text': m.group(1), 'n': m.group(3), 'bracketed': bool(m.group(2))})
    return out


def _match_row(rows, text):
    want = _norm(text).rstrip('.')
    hit = [r for r in rows if r['text'].rstrip('.') == want]
    if len(hit) != 1:
        raise Refused(f'action {text!r} matches {len(hit)} scheme rows')
    return hit[0]


def order(P, lines, year, level, key3, anchor, examples):
    block = _block(lines, anchor)
    count, per, _ = _split(block)
    rows_s = _order_rows(block)
    asks = _asks(P, *key3)
    folded = any(a.roman for a in asks)
    if folded:
        # 2023 OL A Q1(h): the scheme brackets the four answers it pays and
        # prints the two worked-example positions bold and unbracketed
        actions = [_norm(a.text) for a in asks]
        examples = [r['text'] for r in rows_s if not r['bracketed']]
        stem = _norm(asks[0].stem)
        anchor_ask = asks[0]
    else:
        anchor_ask = asks[0]
        stem = _norm(re.split(r'\s+Veiksmas\s+Eiliškumas', anchor_ask.full_text)[0])
        actions = _paper_actions(P, anchor_ask, rows_s)
    def bare(a):
        # the paper prints an example row with its number in the box
        return re.sub(r'\s+\d$', '', a).rstrip('.')
    ex_set = {e.rstrip('.') for e in examples}
    paid = [a for a in actions if bare(a) not in ex_set]
    if len(paid) != count or len(actions) - len(paid) < 1:
        raise Refused(f'{key3}: {len(paid)} actions paid of {len(actions)}, the split prices {count}')
    rows = []
    for a in paid:
        r = _match_row(rows_s, bare(a))
        rows.append({'id': f'r-{len(rows) + 1}', 'kind': 'point', 'verbatim': r['n'], 'marks': per, '_lead': a})
    ex_rows = [_match_row(rows_s, e) for e in examples]
    if folded:
        shown = actions                       # the paper's own rows, numbers as printed
    else:
        shown = [f'{a} {_match_row(rows_s, bare(a))["n"]}' if bare(a) in ex_set else a for a in actions]
    question = '\n'.join([stem] + shown)
    parent = key3 + (None,)
    card, note = _skeleton(P, anchor_ask, parent, year, level, question, count * per, rows, '')
    _led(card['rows'], note)
    card['notes'] = (f'The scheme prints the tariff as {_notation(block)!r}; '
                     + '; '.join(f'"{e["text"]}" is printed already numbered {e["n"]} as the worked example'
                                 for e in ex_rows)
                     + f'. The positions are the scheme\'s. The paper prints this task on page '
                       f'{anchor_ask.page} of the question booklet' + ('; the census counts it once (10c).'
                                                                         if folded else '.'))
    return [card]


def _paper_actions(P, ask, rows_s):
    """The actions in the order the paper prints them: the scheme's rows,
    found in the paper's own text of the task (which the reader may cut
    short), and ordered by where the paper prints them."""
    import fitz
    page = _norm(fitz.open(P.path)[ask.page - 1].get_text())
    at = []
    for r in rows_s:
        k = page.find(r['text'].rstrip('.'))
        if k < 0:
            raise Refused(f'scheme action {r["text"]!r} not on paper page {ask.page}')
        at.append((k, r['text'].rstrip('.') + '.'))
    return [t for _, t in sorted(at)]


def order_row(P, lines, year, level, key3, anchor, examples):
    block = _block(lines, anchor)
    count, per, _ = _split(block)
    rows_s = _order_rows(block)
    asks = [a for a in _asks(P, *key3)
            if a.roman and not any(_norm(a.text).startswith(e.rstrip('.')) for e in examples)]
    if len(asks) != count:
        raise Refused(f'{key3}: {len(asks)} rows asked, the split prices {count}')
    cards = []
    for ask in asks:
        r = _match_row(rows_s, ask.text)
        card, note = _skeleton(P, ask, ask.key, year, level, _norm(ask.full_text), per, [], '')
        card['rows'] = _led([{'id': 'r-1', 'kind': 'point', 'verbatim': r['n'], 'marks': per,
                              '_lead': _norm(ask.text)}], note)
        card['notes'] = (f'The scheme prints the tariff as {_notation(block)!r} over the rows the candidate '
                         f'numbers; "{examples[0]}" is printed already numbered 1 as the worked example. The '
                         f'position is the scheme\'s. The paper prints this ask on page {ask.page} of the '
                         f'question booklet.')
        cards.append(card)
    return cards


def ticks(P, lines, year, level, key3, anchor, _extra):
    block = _block(lines, anchor)
    count, per, _ = _split(block)
    opts = []
    for l in block[1:]:
        m = re.match(r'^\((i{1,3}|iv|v|vi)\)\s+(.+?)(\s*✓)?$', l)
        if m:
            opts.append({'roman': m.group(1), 'text': m.group(2).strip(), 'ticked': bool(m.group(3))})
    asks = _asks(P, *key3)
    if [o['roman'] for o in opts] != [a.roman for a in asks]:
        raise Refused(f'{key3}: scheme options {[o["roman"] for o in opts]} against paper {[a.roman for a in asks]}')
    ticked = [o for o in opts if o['ticked']]
    if len(ticked) != count:
        raise Refused(f'{key3}: {len(ticked)} ticked, the split prices {count}')
    stem = _norm(asks[0].stem)
    question = '\n'.join([stem] + [f'({a.roman}) {_norm(a.text)}' for a in asks])
    rows = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': o['text'], 'marks': per}
            for i, o in enumerate(ticked, 1)]
    card, note = _skeleton(P, asks[0], key3 + (None,), year, level, question, count * per, rows, '')
    _led(card['rows'], note)
    left = [o['text'] for o in opts if not o['ticked']]
    card['rows'][0]['contextNote'] += ' The scheme leaves ' + ', '.join(f'“{t}”' for t in left) + ' unticked.'
    card['notes'] = (f'The scheme prints the tariff as {_notation(block)!r} and ticks {count} of the '
                     f'{len(opts)} options; the ticks were read on a render of the whole table. The paper '
                     f'prints this task on page {asks[0].page} of the question booklet; the census counts it '
                     f'once (10c).')
    return [card]


def prov(P, _lines, year, level, key3, _anchor, _extra):
    S = LtScheme(year, level, SUBJECT)
    priced = {a.key: a for a in S.reading()}
    priced.update(lt_all._order_pairs(P, S))
    printed = lt_all._scheme_text(SUBJECT, year, level)
    key = key3 + (None,)
    ask = next(a for a in P.all_asks() if a.key == key)
    cards, refused = [], []
    lt_all._reading(P, S, priced, ask, year, level, lt_all.question_ref(year, level, key), cards,
                    lambda r, ref, ev='': refused.append((r, ev)), [], SUBJECT, printed)
    if refused or len(cards) != 1:
        raise Refused(f'{key3}: lt_all still refuses: {refused}')
    return cards


SHAPES = {'fewer': fewer, 'box': box, 'order': order, 'order_row': order_row, 'ticks': ticks, 'prov': prov}


def reading_cards(year, level):
    P = LtPaper(year, level, SUBJECT)
    lines = _scheme_lines(year, level)
    out, refused = [], []
    for shape, key3, anchor, extra in SPECS.get((year, level), []):
        try:
            out += SHAPES[shape](P, lines, year, level, key3, anchor, extra)
        except Refused as e:
            refused.append((shape, key3, str(e)))
    return out, refused


def main():
    import json
    year, level = int(sys.argv[1]), sys.argv[2]
    cards, refused = reading_cards(year, level)
    for c in cards:
        print(c['id'], c['totalMarks'], '|', c['questionText'].replace('\n', ' ¶ ')[:150])
        for r in c['rows']:
            g = r.get('group')
            print('     ', r['kind'], r.get('marks'), '|', (g['options'] if g else r['verbatim'])[:200] if g else r['verbatim'][:90],
                  '|', r.get('contextNote', '')[:110])
        print('      notes:', c['notes'][:260])
    print(f'== {len(cards)} cards; {len(refused)} refused')
    for x in refused:
        print('   REFUSED', x)


if __name__ == '__main__':
    main()
