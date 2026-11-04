#!/usr/bin/env python3
"""The marks the SEC prints INSIDE an Ordinary Level History answer, as rows.

    python3 scripts/markbank/authoring/hist_rows.py scripts/markbank/authored/history.json [--write]

Ordinary Level Part A prices a six-mark answer in halves on the answer's own
line — "Sods (3M) and saplings (3M)", "Yes (3M), he will go with them 'to the
end' (3M)" — and hist_scheme keeps that line whole because the SEC set it as
one line. Carded whole, the two priced answers sat behind one six-mark claim,
so a student who had one of them could not say so. Alex's rule (2026-10-23):
what the scheme prices is a row with its marks on it.

This pass cuts such a line at the marks the scheme prints inside it and adds
no words: each row is the text before its "(3M)", with the joiner the scheme
wrote between them ("and", ", ") dropped, and anything printed after the last
price stays with the row it follows. Four printed shapes, each read once:

  Sods (3M) and saplings (3M)                      two rows, 3 and 3
  French (3m) and Latin (3m) [a little Italian (3m)]
                                                   the prices that reach the total are
                                                   rows; the alternative after them is a note
  Clonmel prison (6m), Clonmel only (3m), prison only (3m)
                                                   one row at 6 with 3 as a printed step
  Any TWO: Liverpool, Manchester, Birmingham, and/or Leeds (3M + 3M)
                                                   an any-two group at 3 each
  Identification of doc B and quote from doc B required. 5M + 5M Max =
                                                   a question-total ask whose printed split
                                                   lost its ceiling to the tariff reader:
                                                   the fragment leaves the row for its note

hist_all.py applies this to every card it builds, and the same pass run on the
authored JSON upgrades a file built before it existed; it changes nothing on a
second run.
"""
import json
import re
import sys

INLINE = re.compile(r'\s*\(\s*(\d+)\s*[Mm]\s*\)')
PAIR = re.compile(r'\s*\(\s*(\d+)\s*[Mm]\s*\+\s*(\d+)\s*[Mm]\s*\)')
DANGLING = re.compile(r'\s*(\d+\s*M\s*\+\s*\d+\s*M\s*Max\s*=)\s*$', re.I)
JOINER = re.compile(r'^(?:and/or|and|with|plus|or|&)\b\s*', re.I)
LIST_LEAD = re.compile(r'^(Any\s+(one|two|three|four))\s*:\s*', re.I)
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4}


def tidy(text):
    """A segment without the punctuation and joiner the scheme wrote around its price."""
    text = ' '.join(text.split())
    text = re.sub(r'^[\s,.;:]+', '', text)
    text = JOINER.sub('', text)
    return re.sub(r'[\s,;:]+$', '', text)


def _note(row, extra):
    row['contextNote'] = ' — '.join(x for x in (row.get('contextNote'), extra) if x)


def split_priced(card):
    """The card with its one priced line cut at the marks printed inside it; unchanged when there are none."""
    rows = card['rows']
    kind = card['tariffModel']['kind']
    if kind == 'questionTotal':
        for row in rows:
            m = DANGLING.search(row['verbatim'])
            if m:
                row['verbatim'] = row['verbatim'][:m.start()].rstrip()
                _note(row, f"{' '.join(m.group(1).split())} {card['totalMarks']}M")
        return card
    if kind != 'fixed' or len(rows) != 1:
        return card
    row = rows[0]
    text = row['verbatim']
    total = card['totalMarks']

    pair = PAIR.search(text)
    if pair:
        lead = text[:pair.start()].strip()
        head = LIST_LEAD.match(lead)
        prices = {int(pair.group(1)), int(pair.group(2))}
        if head and len(prices) == 1:
            per = prices.pop()
            count = WORDS[head.group(2).lower()]
            options = [tidy(x) for x in re.split(r',\s*|\s+and/or\s+|\s+and\s+|\s+or\s+', lead[head.end():])]
            options = [x for x in options if x]
            if count * per == total and len(options) >= count:
                group = {'id': row['id'], 'kind': 'anyN', 'verbatim': head.group(1), 'marks': None,
                         'group': {'claimMax': count, 'perOption': per, 'options': options}}
                if row.get('contextNote'):
                    group['contextNote'] = row['contextNote']
                rows[:] = [group]
        return card

    tokens = list(INLINE.finditer(text))
    if len(tokens) < 2:
        return card
    values = [int(t.group(1)) for t in tokens]

    if values[0] == total:
        steps = sorted({v for v in values[1:] if 0 < v < total})
        head = tidy(text[:tokens[0].start()])
        tail = tidy(text[tokens[0].end():])
        if head and steps:
            rows[:] = [{'id': row['id'], 'kind': 'criterion', 'verbatim': head, 'marks': total,
                        'contextNote': tail, 'permittedMarks': [0, *steps, total]}]
            if row.get('contextNote'):
                _note(rows[0], row['contextNote'])
        return card

    running, cut = 0, None
    for index, value in enumerate(values):
        running += value
        if running == total:
            cut = index
            break
        if running > total:
            return card
    if cut is None:
        return card
    pieces = []
    start = 0
    for index, token in enumerate(tokens[:cut + 1]):
        pieces.append({'id': f'r-{index + 1}', 'kind': 'point', 'verbatim': tidy(text[start:token.start()]), 'marks': values[index]})
        start = token.end()
    rest = tidy(text[start:])
    if rest:
        if cut + 1 < len(tokens):
            _note(pieces[-1], rest)
        else:
            pieces[-1]['verbatim'] = f"{pieces[-1]['verbatim']} {rest}"
    if any(not piece['verbatim'] for piece in pieces):
        return card
    if row.get('contextNote'):
        pieces[0]['contextNote'] = row['contextNote']
    rows[:] = pieces
    return card


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    with open(path, encoding='utf-8') as fh:
        cards = json.load(fh)
    before = json.dumps(cards, ensure_ascii=False)
    changed = [card['id'] for card in cards if json.dumps(split_priced(card), ensure_ascii=False) != json.dumps(json.loads(before)[cards.index(card)], ensure_ascii=False)]
    print(f'{len(changed)} cards cut: {", ".join(changed[:6])}{" …" if len(changed) > 6 else ""}', file=sys.stderr)
    if '--write' in sys.argv:
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(cards, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
