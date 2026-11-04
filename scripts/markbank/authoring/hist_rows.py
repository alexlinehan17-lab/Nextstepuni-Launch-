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
  Green ribbons (ribbons = 3m)                     one row at 6 with 3 as a printed step:
                                                   the bracket is the scheme's partial, kept
                                                   as the row's note (#294 made these three
                                                   cards by hand; this reads them)
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
# The same price with its "M" dropped by the SEC: "Parnell (2M) Davitt (2M)
# Croke (2)" (2016 Ordinary). Read only beside at least one full "(nM)" price
# in the same answer, and only when the prices then add up to the tariff.
INLINE_LOOSE = re.compile(r'\s*\(\s*(\d+)\s*[Mm]?\s*\)')
BARE_M = re.compile(r'\s*\(\s*()[Mm]\s*\)')
EACH_TAIL = re.compile(r'\s+(\d+)\s*M each$')
MULTIPLIED = re.compile(r'\s*\((\d+)\s*M\s*x\s*(\d+)\)', re.I)
PAIR = re.compile(r'\s*\(\s*(\d+)\s*[Mm]\s*\+\s*(\d+)\s*[Mm]\s*\)')
DANGLING = re.compile(r'\s*(\d+\s*M\s*\+\s*\d+\s*M\s*Max\s*=)\s*$', re.I)
JOINER = re.compile(r'^(?:and/or|and|with|plus|or|&)\b\s*', re.I)
LIST_LEAD = re.compile(r'^(Any\s+(one|two|three|four))\s*:\s*', re.I)
# A partial the scheme prints in a bracket at the END of a one-line answer:
# "Massive German air raids (air raids alone = 3m)".
PARTIAL = re.compile(r'^(?P<head>.*\S)\s*\((?P<note>[^()]*?=\s*(?P<n>\d+)\s*[Mm])\)\s*$')
# "Chapel bell/convent chimes/organ (any two for 3m + 3m)": the scheme's
# alternatives, any two of which earn 3m each. hist_scheme has already lifted
# the bracket onto the row's note.
# ... and "To watch over everyone/ ... / To report to ministers if necessary Any
# TWO @ 4M" (2016 Ordinary Q1(a)), the price per alternative, unbracketed.
# Also "Efficient/ Hard-working/ Intelligent/ Shrewd TWO @ 3M each" and "Salt
# fish, hides, cattle, hobby-horses Any THREE @ 2M each" (2014-2019 Ordinary).
ANY_OF_NOTE = re.compile(r'^(?:\((any (one|two|three))(?: for)?\s*(\d+)m(?:\s*\+\s*(\d+)m)*\)'
                         r'|((?:Any )?(?:ONE|TWO|THREE|[1-3])) (?:@|for) (\d+)M(?: each)?)$', re.I)
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
# The count printed as a figure after a dash: "Pleasant situation/ Gorgeous
# buildings/ Population/ Obedience and loyalty - Any 2 for 3M each" (2011).
DASH_ANY = re.compile(r'\s+-\s+(?P<note>Any [1-3] (?:for|@) \d+M(?: each)?)$')
# The second of two priced answers printed as an answer the scheme does not
# give: "Attackers (3M) Any ONE valid reason (3M) (6)" (2011 Ordinary).
TAIL_PRICED = re.compile(r'^Any (?:ONE|TWO) valid [^()]*\(\d+\s*M\)$')
NUMBER_WORDS = {n: w for w, n in WORDS.items()}


def tidy(text):
    """A segment without the punctuation and joiner the scheme wrote around its price."""
    text = ' '.join(text.split())
    text = re.sub(r'^[\s,.;:]+', '', text)
    text = JOINER.sub('', text)
    return re.sub(r'[\s,;:]+$', '', text)


def _note(row, extra):
    row['contextNote'] = ' — '.join(x for x in (row.get('contextNote'), extra) if x)


# A count and the price of each, printed together on a row that names no
# answers: "Any TWO features from second paragraph of text @ 3M each", "TWO
# valid aims of the Apprentice Boys of Derry 3M x 2", "Any TWO countries
# invaded by Napoleon 3M + 3M" (2013-2019 Ordinary, (6)). The count is in
# capitals, as the scheme prints it.
COUNTED = re.compile(r'\b(?:(?-i:(TWO|THREE|FOUR))|(?<=Any )(two|three|four))\b')
PER_EACH = re.compile(r'@\s*(\d+)\s*M\b', re.I)
PER_TIMES = re.compile(r'\b(\d+)\s*M\s*x\s*(\d+)\b', re.I)
PER_PLUS = re.compile(r'\b(\d+)\s*M?(?:\s*\+\s*(\d+)\s*M?)+\b', re.I)


# A list printed as a sentence, "A, B or C".
OXFORD_LIST = re.compile(r'^[^,/]+(?:,\s*[^,/]+)+\s+(?:or|and)\s+[^,/]+$')
# The count and price printed beside the answers, as the row's note: "Any TWO
# @ 3M each", "All THREE @ 2M each" (2012-2017 Ordinary).
NOTE_COUNTED = re.compile(r'^(?P<all>Any|All) (?P<n>TWO|THREE|FOUR) (?:@|for) (?P<per>\d+)M(?: each)?$')


def step_counted(card):
    """A counted row with its price per answer is stepped at that price.

    One plain row that prints how many answers it wants and what each earns,
    and names none of them, was one claim for the whole part: a student with
    one of the two earned nothing. The printed price per answer is the step,
    so "Any TWO ... @ 3M each" on a (6) part claims 0, 3 or 6. Only when the
    count times the price is the part's tariff exactly; the row's words are
    unchanged."""
    rows = card['rows']
    if card['tariffModel']['kind'] != 'fixed' or len(rows) != 1:
        return card
    row = rows[0]
    total = card['totalMarks']
    if row['kind'] != 'point' or row.get('marks') != total:
        return card
    text = row['verbatim']
    note = NOTE_COUNTED.match(row.get('contextNote') or '')
    if note and WORDS[note.group('n').lower()] * int(note.group('per')) == total:
        # The answers are printed and the price per answer is the note.
        n, per = WORDS[note.group('n').lower()], int(note.group('per'))
        items = [tidy(x) for x in re.split(r',\s*|\s+(?:or|and)\s+', text) if tidy(x)]
        if note.group('all') == 'All' and len(items) == n:
            # "Liberty, equality, fraternity" under "All THREE @ 2M each": each
            # answer at its price, as "(2M x 3)" is.
            rows[:] = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': item, 'marks': per}
                       for i, item in enumerate(items, start=1)]
            return card
        if note.group('all') == 'Any':
            # The answers run together where no option can be told from the
            # next ("Von Eckstadt Vienna 1848" under "Any TWO @ 3M each"): the
            # row is stepped at the printed price.
            rows[:] = [{**row, 'kind': 'criterion', 'permittedMarks': [per * k for k in range(n + 1)]}]
        return card
    count = COUNTED.search(text)
    if not count:
        return card
    n = WORDS[(count.group(1) or count.group(2)).lower()]
    each = PER_EACH.search(text)
    times = PER_TIMES.search(text)
    plus = PER_PLUS.search(text[count.end():])
    if each:
        per = int(each.group(1))
    elif times and int(times.group(2)) == n:
        per = int(times.group(1))
    elif plus:
        terms = [int(x) for x in re.findall(r'\d+', plus.group(0))]
        if len(terms) != n or len(set(terms)) != 1:
            return card
        per = terms[0]
    else:
        return card
    if per * n != total:
        return card
    rows[:] = [{**row, 'kind': 'criterion', 'permittedMarks': [per * k for k in range(n + 1)]}]
    return card


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

    dash = DASH_ANY.search(text) if not row.get('contextNote') else None
    if dash:
        text = row['verbatim'] = text[:dash.start()].rstrip()
        row['contextNote'] = dash.group('note')
    any_of = ANY_OF_NOTE.match(row.get('contextNote') or '')
    if any_of:
        if any_of.group(1):
            lead, count, per = any_of.group(1), WORDS[any_of.group(2).lower()], int(any_of.group(3))
        else:
            lead = any_of.group(5)
            last = lead.split()[-1].lower()
            count, per = (int(last) if last.isdigit() else WORDS[last]), int(any_of.group(6))
            if not lead.lower().startswith('any'):
                lead = f'Any {lead}'
        options = [tidy(x) for x in text.split('/') if tidy(x)]
        if len(options) == 1:
            # The alternatives listed with commas: "Nantes, Bordeaux, Lisbon, Cadiz".
            options = [tidy(x) for x in text.split(',') if tidy(x)]
        if len(options) <= count and OXFORD_LIST.match(text):
            # The alternatives listed as a sentence: "There was no roof, door or
            # windscreen" under "Any TWO @ 3M each" (2017 Ordinary).
            options = [tidy(x) for x in re.split(r',\s*|\s+(?:or|and)\s+', text) if tidy(x)]
        if count * per == total and len(options) > count:
            rows[:] = [{'id': row['id'], 'kind': 'anyN', 'verbatim': lead, 'marks': None,
                        'group': {'claimMax': count, 'perOption': per, 'options': options}}]
            return card
    tokens = list(INLINE.finditer(text))
    loose = list(INLINE_LOOSE.finditer(text))
    if (tokens and len(loose) > len(tokens) and sum(int(t.group(1)) for t in tokens) < total
            and sum(int(t.group(1)) for t in loose) == total):
        tokens = loose
    elif (not tokens and len(loose) >= 2 and all(0 < int(t.group(1)) < total for t in loose)
            and sum(int(t.group(1)) for t in loose) == total
            # Never a printed numbering, "BBC (1) were very much in favour of
            # the strike (2) did not monitor NI broadcasts (3) ... (4) ..."
            # (2010 Ordinary): 1 + 2 + 3 + 4 is the part's 10 by chance.
            and [int(t.group(1)) for t in loose] != list(range(1, len(loose) + 1))):
        # Every price printed without its M: "DMP prevented looting (3) and the
        # call-out of the military (3)" (2013 Ordinary, (6)). Read only when
        # the bracketed figures add up to the tariff exactly.
        tokens = loose
    mult = MULTIPLIED.search(text)
    if not tokens and mult and int(mult.group(1)) * int(mult.group(2)) == total:
        # "Civilisation, wealth and manufactures (2M x 3)" (2013 Ordinary, (6)):
        # each of the named items at its price, when the count is the items'.
        items = [tidy(x) for x in re.split(r',\s*|\s+and\s+', text[:mult.start()]) if tidy(x)]
        after = text[mult.end():].strip()
        if len(items) == int(mult.group(2)) and not after:
            rows[:] = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': item, 'marks': int(mult.group(1))}
                       for i, item in enumerate(items, start=1)]
            if row.get('contextNote'):
                rows[0]['contextNote'] = row['contextNote']
            return card
        if (len(items) == int(mult.group(2)) and after.startswith('/') and tidy(after[1:])
                and not INLINE_LOOSE.search(after)):
            # The priced items, OR the answer after the solidus: "The spirit,
            # content and enterprise (2M x 3)/ A free Constitution" (2013
            # Ordinary, (6)). Two routes, as Chemistry's double solidus is: the
            # three items at their price, or the alternative for the part's
            # whole tariff; claiming one side locks the other.
            rows[:] = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': item, 'marks': int(mult.group(1)),
                        'route': 'priced-items'}
                       for i, item in enumerate(items, start=1)]
            rows.append({'id': f'r-{len(items) + 1}', 'kind': 'point', 'verbatim': tidy(after[1:]),
                         'marks': total, 'route': 'alternative',
                         'contextNote': f'The scheme accepts this instead of the {NUMBER_WORDS[len(items)]} answers above, '
                                        f'for all {total} marks. The examiner marks one or the other.'})
            if row.get('contextNote'):
                rows[0]['contextNote'] = row['contextNote']
            return card
    each = EACH_TAIL.search(text)
    if not tokens and each and int(each.group(1)) and total % int(each.group(1)) == 0:
        # "Mathematics, Literature and Religion 2M each" (2010 Ordinary, (6)):
        # each named item at its price, when the count is the items'.
        items = [tidy(x) for x in re.split(r',\s*|\s+and\s+', text[:each.start()]) if tidy(x)]
        if len(items) * int(each.group(1)) == total and len(items) > 1:
            rows[:] = [{'id': f'r-{i}', 'kind': 'point', 'verbatim': item, 'marks': int(each.group(1))}
                       for i, item in enumerate(items, start=1)]
            if row.get('contextNote'):
                rows[0]['contextNote'] = row['contextNote']
            return card
    bare = list(BARE_M.finditer(text))
    if (tokens and len(bare) == 1 and bare[0].start() > tokens[-1].end()
            and 0 < total - sum(int(t.group(1)) for t in tokens)):
        # "On the floor (4M) and in the bathtubs (M)" (2015 Ordinary, 8M): the
        # last price printed without its figure takes what the tariff leaves.
        tokens = tokens + bare
    partial = PARTIAL.match(text)
    if not tokens and partial and int(partial.group('n')) == 0:
        # A bracketed answer the scheme credits with nothing, "No post (No buses
        # = 0M)" (2014 Ordinary): the bracket is the row's note, never a step.
        row['verbatim'] = tidy(partial.group('head'))
        _note(row, ' '.join(partial.group('note').split()))
        return card
    if not tokens and partial and 0 < int(partial.group('n')) < total:
        rows[:] = [{'id': row['id'], 'kind': 'criterion', 'verbatim': tidy(partial.group('head')),
                    'marks': total, 'contextNote': ' '.join(partial.group('note').split()),
                    'permittedMarks': [0, int(partial.group('n')), total]}]
        if row.get('contextNote'):
            _note(rows[0], row['contextNote'])
        return card
    note_price = INLINE.search(row.get('contextNote') or '')
    if (len(tokens) == 1 and note_price and TAIL_PRICED.match(row.get('contextNote') or '')
            and text[tokens[0].end():].strip() in ('', '.')
            and int(tokens[0].group(1)) + int(note_price.group(1)) == total):
        note = row['contextNote']
        rows[:] = [{'id': 'r-1', 'kind': 'point', 'verbatim': tidy(text[:tokens[0].start()]),
                    'marks': int(tokens[0].group(1))},
                   {'id': 'r-2', 'kind': 'point', 'verbatim': tidy(note[:note_price.start()]),
                    'marks': int(note_price.group(1))}]
        return card
    if len(tokens) < 2:
        return card
    values = [int(t.group(1)) if t.group(1) else total - sum(int(x.group(1)) for x in tokens if x.group(1))
              for t in tokens]

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
        elif tokens is loose and not any(t.group(0).strip().lower().endswith('m)') for t in tokens):
            # Every price a bare figure, and the phrase runs on past the last
            # one: "In a slap-dash (3) meaningless (3) way" (2013 Ordinary,
            # (6)). The scheme prices the words BEFORE each figure, so the rows
            # are those priced spans; the run-on word is priced by neither, and
            # joined on it would make a row the scheme never prints whole.
            pass
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
