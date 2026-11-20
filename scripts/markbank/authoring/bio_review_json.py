"""A Biology review ledger kept as data: scripts/markbank/authored/biology-deferred-ledgers/<year>-<level>.json.

The deferred sittings' ledgers (bio_review_<year>_<level>_deferred.py) are written as JSON, so a reviewer's
work is data the runner reads, never code. Each module is two lines:

    from bio_review_json import load
    globals().update(load('2022-hl'))

The JSON holds exactly what a Python ledger holds, under the same names (SOURCES, PAGE_ROLES,
QUESTION_TOTALS, PART_TOTALS, BEST_OF, LADDERS, CHECKSUMS, SCAN_PAGES, SELECTION_SCAN, ROUTES, FIGURES,
TASKS, and the optional LAYOUT_CHECKS, ANSWER_VARIANTS, LADDER_OF, LADDER_EXEMPT, ATLAS_UNIT_EQUIV), plus
"doc" (the ledger's method note: the runner records its first paragraph) and "reviewedAt". Two encodings
stand in for what JSON cannot say:

  * A key naming a question part is written "11a" (question 11, part a) and read as the tuple (11, 'a');
    a plain question is "11". SCAN_PAGES values are [first, last] page ranges.
  * A selector, row or label is an object with ONE key naming its bio_review_lib constructor and the
    constructor's arguments: {"Q": {"page": 3, "start": "Name the ..."}} is Q(page=3, start="Name the ..."),
    {"pt": {"sel": {"S": {"start": "Fungi"}}, "marks": 3}} is pt(S("Fungi"), 3). A list of arguments is
    passed positionally. Every task in TASKS is an object of T()'s arguments, read the same way.

Nothing here decides anything: it only turns the data back into what bio_review_lib's constructors return,
so the runner's every gate applies unchanged.
"""
import json
import os

import bio_review_lib as B

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGERS = os.path.join(HERE, '..', 'authored', 'biology-deferred-ledgers')
CONSTRUCTORS = {name: getattr(B, name) for name in ('Q', 'M', 'SQ', 'S', 'pt', 'unprinted', 'anyn', 'allof',
                                                     'G', 'L')}
PART_KEYED = ('PART_TOTALS', 'CHECKSUMS', 'BEST_OF', 'LADDERS')


def decode(value):
    if isinstance(value, list):
        return [decode(v) for v in value]
    if isinstance(value, dict):
        if len(value) == 1:
            (name, args), = value.items()
            if name in CONSTRUCTORS:
                args = decode(args)
                return CONSTRUCTORS[name](*args) if isinstance(args, list) else CONSTRUCTORS[name](**args)
        return {k: decode(v) for k, v in value.items()}
    return value


def part_key(key):
    """'11a' -> (11, 'a'); '11' -> 11."""
    digits = key.rstrip('abcdefghijklmnopqrstuvwxyz')
    return (int(digits), key[len(digits):]) if digits != key else int(key)


def task(spec):
    spec = decode(spec)
    for field in ('item',):
        if spec.get(field) is not None:
            spec[field] = tuple(spec[field])
    return B.T(**spec)


def load(name):
    with open(os.path.join(LEDGERS, f'{name}.json'), encoding='utf-8') as fh:
        data = json.load(fh)
    out = {'__doc__': data['doc'], 'REVIEWED_AT': data['reviewedAt'], 'DEFERRED': True,
           'SEC': 'State Examinations Commission'}
    for key, value in data.items():
        if key in ('doc', 'reviewedAt', 'TASKS'):
            continue
        if key in ('QUESTION_TOTALS',):
            value = {int(k): v for k, v in value.items()}
        elif key in PART_KEYED:
            value = {part_key(k): (tuple(v) if key == 'BEST_OF' else
                                   {int(m): n for m, n in v.items()} if key == 'CHECKSUMS' else v)
                     for k, v in value.items()}
        elif key == 'PAGE_ROLES':
            value = {doc: {int(p): role for p, role in roles.items()} for doc, roles in value.items()}
        elif key == 'SCAN_PAGES':
            value = {doc: range(first, last + 1) for doc, (first, last) in value.items()}
        elif key == 'SELECTION_SCAN':
            value = [tuple(entry) for entry in value]
        elif key == 'FIGURES':
            value = {k: tuple(decode(v)) for k, v in value.items()}
        elif key in ('LADDER_EXEMPT',):
            value = tuple(value)
        else:
            value = decode(value)
        out[key] = value
    out['TASKS'] = [task(spec) for spec in data['TASKS']]
    return out
