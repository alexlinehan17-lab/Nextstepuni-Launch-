#!/usr/bin/env python3
"""The marks the SEC prints INSIDE an Italian answer, as rows and steps.

    python3 scripts/markbank/authoring/it_rows.py scripts/markbank/authored/italian.json [--write]

An Italian comprehension answer is often priced in halves on its own line —
"Erano stati compagni (1m) di scuola (4m)", "By summer [2] 2022 [1]", "Ha
rinunciato ad un lavoro stabile (3) come interprete (2)" — and it_scheme keeps
the line whole because the SEC set it as one line. Carded whole, the two priced
answers sat behind one five-mark claim, so a student who had one of them could
not say so. Alex's rule (2026-10-23): what the scheme prices is a row with its
marks on it.

Two printed shapes, each read once:

  Erano stati compagni (1m) di scuola (4m)        two rows, 1 and 4: each row is the
                                                   text before its price, with the
                                                   joiner the SEC wrote between them
                                                   ("e", "ma", ", ") dropped
  La mamma è stupita (2m) (2+3) che i ragazzi …    the ask's split printed beside the
                                                   first price is not a price: taken
                                                   out before the line is cut

A full answer the SEC wrapped onto a second line, whose tail it_scheme read as
a lesser answer — "… di Rosello (3) e voleva coinvolgere" then "Rosello stesso
(2)" under a "5 marks (3+2)" head — is joined back from the card's own note
before it is cut, because the tail's price completes the line's to the ask's
split; it_scheme joins it at the source now too.

A lesser answer the scheme prints under a full one ("Nata nel 2020 2m") was a
sentence in the row's note; on a fixed-tariff point row the note stays and the
row gains the lesser answer's mark as a printed step, so the student who wrote
the shorter form places it. An any-N row has no per-option steps, so its note
stays as it was.

it_all.py applies this to every card it builds, and the same pass run on the
authored JSON upgrades a file built before it existed; it changes nothing on a
second run.
"""
import json
import re
import sys

# "(1m)", "(2 m)", "[2]", "(3)": a price the SEC prints inside an answer.
PRICE = re.compile(r'\s*(?:\(\s*(\d{1,2})\s*m\s*\)|\[\s*(\d{1,2})\s*\]|\(\s*(\d{1,2})\s*\))')
# "(2+3)": the ask's split, printed beside the first price rather than on the head.
SPLIT = re.compile(r'\s*\(\s*(\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)')
JOINER = re.compile(r'^(?:e|ed|o|oppure|ma|and|or|but)\b\s*', re.I)
LESSER = 'The scheme also pays part marks for a shorter answer: '
RUNG = re.compile(r'“([^”]+)”\s*(\d{1,2})\s*marks?')
# "The scheme prints the tariff as '5 marks (3+2)'": the card's own record of the head.
HEAD_SPLIT = re.compile(r"tariff as '\d{1,3}\s*marks?\s*\((\d{1,2}(?:\s*\+\s*\d{1,2})+)\)'")
ROW_KEYS = {'id', 'kind', 'verbatim', 'marks', 'contextNote'}


def tidy(text):
    """A segment without the punctuation and joiner the scheme wrote around its price."""
    text = ' '.join(text.split())
    text = re.sub(r'^[\s,.;:/]+', '', text)
    text = JOINER.sub('', text)
    return re.sub(r'[\s,;:/]+$', '', text)


def _value(token):
    return int(next(group for group in token.groups() if group))


def _rejoin(row, card):
    """The wrapped tail of a full answer, back on its line from the note.

    Only where everything the join needs is printed: ONE price mid-line, ONE
    lesser answer in the note, the two prices adding up to the row, and the
    head's own split naming exactly those two terms.
    """
    text = row['verbatim']
    note = row.get('contextNote') or ''
    tokens = list(PRICE.finditer(text))
    if len(tokens) != 1 or tokens[0].end() >= len(text.rstrip()) or LESSER not in note:
        return
    head, tail = note.split(LESSER, 1)
    rungs = RUNG.findall(tail)
    if len(rungs) != 1 or tail.strip() != f'“{rungs[0][0]}” {rungs[0][1]} mark{"s" if rungs[0][1] != "1" else ""}.':
        return
    value, extra = _value(tokens[0]), int(rungs[0][1])
    split = HEAD_SPLIT.search(card.get('notes') or '')
    terms = [int(x) for x in re.findall(r'\d{1,2}', split.group(1))] if split else []
    if value + extra != row['marks'] or sorted(terms) != sorted([value, extra]):
        return
    row['verbatim'] = f"{text.rstrip()} {rungs[0][0]} ({extra})"
    row['contextNote'] = head.rstrip()
    if not row['contextNote']:
        del row['contextNote']


def _cut(row):
    """The row's pieces at the prices printed inside it, or None where they do not add up."""
    text = row['verbatim']
    marks = row['marks']
    split = SPLIT.search(text)
    if split and sum(int(x) for x in re.findall(r'\d{1,2}', split.group(1))) == marks:
        text = text[:split.start()] + text[split.end():]
    tokens = list(PRICE.finditer(text))
    if len(tokens) < 2:
        return None
    values = [_value(token) for token in tokens]
    if sum(values) != marks:
        return None
    pieces = []
    start = 0
    for index, token in enumerate(tokens):
        pieces.append({'id': f"{row['id']}-{index + 1}", 'kind': 'point',
                       'verbatim': tidy(text[start:token.start()]), 'marks': values[index]})
        start = token.end()
    rest = tidy(text[start:])
    if rest:
        pieces[-1]['verbatim'] = f"{pieces[-1]['verbatim']} {rest}"
    if any(not re.search(r'[^\W_]', piece['verbatim']) for piece in pieces):
        return None
    if row.get('contextNote'):
        pieces[0]['contextNote'] = row['contextNote']
    return pieces


# The id a cut piece carries: "r-1-2" is the second piece of row r-1.
PIECE = re.compile(r'^r-\d+-\d+$')


def _steps(row):
    """A point row whose note prices shorter answers, as a criterion row with those steps.

    Not on a cut piece: the shorter answer the note prices is a shorter form of
    the WHOLE answer, not of the one piece that happens to carry the note.
    """
    note = row.get('contextNote') or ''
    if row['kind'] != 'point' or LESSER not in note or not isinstance(row['marks'], int) or PIECE.match(row['id']):
        return
    rungs = sorted({int(value) for _, value in RUNG.findall(note.split(LESSER, 1)[1])})
    if not rungs or rungs[-1] >= row['marks']:
        return
    row['kind'] = 'criterion'
    row['permittedMarks'] = [0, *rungs, row['marks']]


def split_priced(card):
    """The card with every priced line cut at the marks printed inside it and every
    lesser answer a printed step; unchanged when there are none."""
    if card['tariffModel']['kind'] != 'fixed':
        return card
    rows = []
    for row in card['rows']:
        if row['kind'] != 'point' or not isinstance(row['marks'], int) or set(row) - ROW_KEYS:
            rows.append(row)
            continue
        _rejoin(row, card)
        pieces = _cut(row)
        if pieces:
            rows.extend(pieces)
        else:
            _steps(row)
            rows.append(row)
    card['rows'] = rows
    return card


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    with open(path, encoding='utf-8') as fh:
        cards = json.load(fh)
    before = {card['id']: json.dumps(card, ensure_ascii=False) for card in cards}
    changed = [card['id'] for card in cards if json.dumps(split_priced(card), ensure_ascii=False) != before[card['id']]]
    print(f'{len(changed)} cards changed: {", ".join(changed[:6])}{" …" if len(changed) > 6 else ""}', file=sys.stderr)
    if '--write' in sys.argv:
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(cards, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
