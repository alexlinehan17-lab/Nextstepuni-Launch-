#!/usr/bin/env python3
"""The printed five-row Gaeilge (5 mharc) table for Higher Paper 2 literature answers, lifted from the scheme.

Each Higher scheme prints the same table (Sárchumas 5 … Cumas lag/an-lag 1) beside the prose, poetry
and additional-literature keys, with the note that every literature answer earns 5 for Gaeilge.
`lifted(scheme)` returns that table and note exactly as printed, for the shared Gaeilge award.
"""
from __future__ import annotations
import re

TABLE = re.compile(r'Gaeilge \(5 mharc\) Sárchumas maidir leis na príomhghnéithe de cheart na teanga.*?'
                   r'Cumas lag/an-lag maidir leis na príomhghnéithe de cheart na teanga \(gramadach, comhréir, struchtúr, deilbhíocht\) 1')
NOTE = re.compile(r'Nóta: I gcás na gceisteanna 2 \(Prós\), 3 \(Filíocht\),? agus 4 \(Litríocht Bhreise\).*?ar Ghaeilge\.')
ROWS = ('Sárchumas', 'Cumas an-mhaith', 'Cumas maith', 'Cumas measartha', 'Cumas lag/an-lag')


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def lifted(scheme, first_page=1):
    """(table, note, table page, note page) from a fitz scheme document, searching from `first_page`."""
    table = note = None
    for number in range(first_page, len(scheme) + 1):
        text = re.sub(r'^\d+\s', '', clean(scheme[number - 1].get_text()))
        if note is None and NOTE.search(text):
            note = (NOTE.search(text).group(0), number)
        if table is None and TABLE.search(text):
            table = (TABLE.search(text).group(0), number)
        if table and note:
            break
    assert table and note, 'Gaeilge table or note not found'
    # Exactly the five printed rows, scored 5 down to 1; no row is added or paraphrased.
    assert [row for row in ROWS if row in table[0]] == list(ROWS) and re.findall(r'\) ([1-5])\b', table[0]) == ['5', '4', '3', '2', '1'], table[0]
    assert 'gan fiúntas' not in table[0]
    return table[0], note[0], table[1], note[1]
