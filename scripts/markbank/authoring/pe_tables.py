#!/usr/bin/env python3
"""Read the Physical Education scheme's answers out of its own TABLE CELLS.

    python3 scripts/markbank/authoring/pe_tables.py 2023 ol

Some PE asks are answered INSIDE a printed table rather than beside it: four
explanations to be matched to four named psychological factors, four statements
to be ticked True or False, three periodisation cycles to be matched to three
timeframes.  The flat text layer reads such a table ACROSS the row, so the
SEC's prompt and the SEC's answer arrive welded into one line:

    A general emotional state. Trait anxiety
    Run a sprint, rest, receive feedback, Distributed repeat.

A card built from that states neither, and the second is not even a sentence.
pymupdf's find_tables(strategy='lines') reads the same page with the columns
intact — the rules really are drawn on these tables — so the prompt, the
answer and the marks come back in their own cells:

    ['A general emotional state.', 'Trait anxiety', None, None, '2', None, None]

and a True/False grid comes back with the tick in the column it was printed in:

    ['', 'True', None, 'False']
    ['Carbohydrates are the body's main source of energy.', '✓', None, '']

which is the only way to know WHICH column it is in.  Nothing here is
invented: every string is a cell the SEC printed, and the pairing is the
table's own row.

A row is joined to the scheme PART that prices it by its own words, never by
position: the part's flat text still holds the welded line, so a table row
whose prompt and answer both appear inside one of the part's printed lines is
that part's row.  A row that matches no part is dropped rather than guessed at.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'physical-education', 'schemes')

TICK = re.compile(r'[✓✔✓]')
MARKS_CELL = re.compile(r'^\(?\s*(\d{1,2})\s*(?:marks?)?\s*\)?$', re.I)
# A cell that is the table's own furniture or the examiner's own criterion
# rather than one of the two things a matching row pairs. "Correct example" is
# the SEC saying any example scores, not an example; "please choose from above"
# is the column heading.
NOT_AN_ANSWER = re.compile(
    r'^(?:marks?|description|explanation|answer|category|example'
    r'|(?:please )?choose from above|correct \w+|appropriate \w+'
    r'|accurate \w+|relevant \w+|any \w+|true|false)$', re.I)


def tidy(s):
    return ' '.join((s or '').split())


def flat(s):
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())


def _rows_of(table):
    """(prompt, answer, marks) for every answered row of one printed table."""
    try:
        data = table.extract()
    except Exception:
        return []
    cleaned = [[tidy(c) for c in row] for row in data]
    # A TRUE/FALSE grid: a header row naming the two columns, and a tick in one
    # of them on every row under it. The column INDEX is the answer.
    headings = {}
    for row in cleaned:
        for i, cell in enumerate(row):
            if cell.lower() in ('true', 'false'):
                headings[i] = cell
        if len(headings) >= 2:
            break
    out = []
    for row in cleaned:
        text = [c for c in row if c]
        if len(text) < 2:
            continue
        if headings and any(TICK.search(c) for c in row):
            prompt = next((c for c in row if c and not TICK.search(c)
                           and not MARKS_CELL.match(c)), '')
            ticked = [headings[i] for i, c in enumerate(row)
                      if i in headings and TICK.search(c)]
            if prompt and len(ticked) == 1:
                out.append((prompt, ticked[0], None))
            continue
        words = [c for c in row if c and not MARKS_CELL.match(c)
                 and not TICK.search(c)]
        marks = next((int(MARKS_CELL.match(c).group(1)) for c in row
                      if c and MARKS_CELL.match(c)), None)
        # The ANSWER cell of a matching row is a term, never a tariff or a
        # band: "2 x 4 Marks", "6-8" and "2 marks 2 marks" are the marks column
        # landing in a two-column table, and pairing a criterion with its own
        # price is not an answer to anything.
        if (len(words) == 2 and all(len(w) >= 3 for w in words)
                and not re.search(r'\d', words[1])
                and len(re.findall(r'[A-Za-z]', words[1])) >= 3
                and not NOT_AN_ANSWER.match(words[0])
                and not NOT_AN_ANSWER.match(words[1])):
            out.append((words[0], words[1], marks))
    # The table's own HEADER row reads like a matching row — "Timeframe |
    # Periodisation Cycle | 3 Marks" — and the give-away is its marks cell:
    # the SEC prints the TABLE's total there, so it equals the sum of the rows
    # beneath it. Dropped on that arithmetic rather than on how its words look.
    if (len(out) > 2 and out[0][2] is not None
            and all(row[2] is not None for row in out[1:])
            and out[0][2] == sum(row[2] for row in out[1:])):
        out = out[1:]
    # Two rows is a header and one answer; a matching task prints at least
    # three, and requiring three keeps an ordinary two-column criterion table
    # ("Description | 4 Marks") out.
    return out if len(out) >= 3 else []


_CACHE = {}


def answer_rows(year, level):
    """Every answered table row the scheme prints, in document order."""
    key = (year, level)
    if key in _CACHE:
        return _CACHE[key]
    import pymupdf
    path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
    out = []
    with pymupdf.open(path) as doc:
        for page in doc:
            try:
                tables = page.find_tables(strategy='lines').tables
            except Exception:
                continue
            for table in tables:
                out.extend(_rows_of(table))
    _CACHE[key] = out
    return out


def rows_for(part, year, level):
    """The table rows that belong to one scheme part, in printed order.

    Joined on the part's OWN WORDS: the flat reading of the same table is
    still in the part, with the prompt and the answer welded into one line, so
    a row whose two cells both appear inside one of those lines is this part's.
    """
    printed = [flat(t) for t in [part.cue] + part.rows + part.answers if t]
    out = []
    for prompt, answer, marks in answer_rows(year, level):
        a = flat(prompt)
        # The PROMPT is what both readings share. The answer is not: the flat
        # reading posts it into the middle of the prompt ("Run a sprint, rest,
        # receive feedback, Distributed repeat.") and a True/False grid does
        # not print it on the row at all — the tick is in a column whose
        # heading is two rows up. So the join is on a prefix of the prompt,
        # long enough that no two parts of one scheme share it.
        b = flat(answer)
        if len(a) < 8:
            continue
        # A long prompt identifies its part on its own. A short one — "A full
        # year", "Two months" — needs its answer beside it in the same flat
        # line to be sure, which is exactly what the welded reading gives.
        if any(a[:20] in line and (len(a) >= 20 or b in line)
               for line in printed):
            out.append((tidy(prompt), tidy(answer), marks))
    return out


if __name__ == '__main__':
    year, level = int(sys.argv[1]), sys.argv[2]
    for prompt, answer, marks in answer_rows(year, level):
        print(f'{marks!s:>4}  {prompt[:70]!r} -> {answer[:40]!r}')
