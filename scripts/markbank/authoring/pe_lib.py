#!/usr/bin/env python3
"""Pair a Physical Education paper ask with the scheme part that prices it.

    python3 scripts/markbank/authoring/pe_lib.py            # the pairing audit
    python3 scripts/markbank/authoring/pe_lib.py 2024 hl    # one sitting

THE DENOMINATOR IS THE PAPER (Law 1).  This walks the CENSUS's leaf asks —
741 of them over thirteen papers — and finds the scheme part that prices each
one.  An earlier version walked the scheme's parts instead and reported 644
"paired asks" out of a denominator it never looked at; the 97 the paper prints
and the scheme never reaches were not in any bucket at all.

LAW 4 — never join paper to scheme on the part key — applies here even though
PE's two documents happen to print the SAME address.  The key is where the
pairing STARTS; something else has to make it evidence.  Three routes, tried
in order, and a pair resting on none of them is REPORTED rather than used:

  wording   the scheme reprints the ask above or inside its table (2023
            onward), or its criterion rows are the ask rewritten as what the
            examiner must see — "Identifies test to measure flexibility"
            against "Identify a test that could be used to measure
            flexibility".  Scored with align.py's bag-of-words overlap.
  shape     the markers the two documents print under one question are
            IDENTICAL and in the same order.  This is the Baltic rule: the
            same number of rows under the letter, or nothing.  It covers the
            commonest Section A shape too — a question BOTH documents keep
            whole has exactly one unit on each side, and a stimulus-heavy ask
            ("The Collins Dictionary defines a characteristic as...") scores
            below the wording floor against a table that never quotes it.
  parent    the scheme prices the LETTER where the paper numbers romans
            under it, or prices the QUESTION where the paper letters it.  The
            ask is then inside the part, and a card written from that part
            covers it — which is exactly how reconcile.py reads a card cited
            one level up.

A wrong pairing shows a real question under a real answer that does not
answer it and passes every downstream gate; the only thing that catches it is
refusing to make it.
"""
import collections
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import pe_scheme as S                                            # noqa: E402
from align import bag, score                                     # noqa: E402
from paper import Paper                                          # noqa: E402
from paper_census import census_subject                           # noqa: E402

SUBJECT = 'physical-education'
# 2020 sat an altered examination: Section C offered three long questions where
# every other year offers five, so its paper stops at Question 16 and no
# Ordinary paper was set at all.
SITTINGS = S.SITTINGS
# The wording floor.  Set from the corpus rather than picked: at 0.30 every
# sitting pairs over 85% of its asks on wording alone, and the pairs that fall
# below it are the ones whose scheme part prints nothing but a mark ladder —
# which have no words to agree with.
FLOOR = 0.30


def scheme_dir():
    return os.path.join(ROOT, 'examiner-reports', SUBJECT, 'schemes')


def normalise(text):
    text = (text or '').replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('–', '-').replace('—', '-')
    return re.sub(r'[^a-z0-9]+', '', text.lower())


_MD = {}


def load_md(year, level):
    """The whole scheme file, normalised the way the provenance gate reads it.

    Both renderings are in it — the converted page order and the block order
    append-scheme-blocks.py appended — and the gate searches both, so a line
    this reader rebuilt out of two wrapped halves traces against the block
    rendering even where the page order split it.
    """
    path = os.path.join(scheme_dir(), f'{year}-{level}.md')
    raw = open(path, encoding='utf-8').read()
    keep = [l for l in raw.split('\n')
            if not re.match(r'^##\s*Page\s*\d+\s*$', l)
            and not re.match(r'^\s*\d+\s*$', l)]
    return normalise('\n'.join(keep))


def traces(year, level, text):
    """True where `text` appears in its own scheme, the way the gate compares."""
    key = (year, level)
    if key not in _MD:
        _MD[key] = load_md(year, level)
    return normalise(text) in _MD[key]


_CENSUS = {}


def leaves(year, level):
    """The census's own leaf asks for one paper, as (key, label, text).

    Taken from paper_census.py itself rather than re-walked here, so the
    denominator this reader works against is the one reconcile.py checks.
    """
    if not _CENSUS:
        for paper in census_subject(SUBJECT)['papers']:
            _CENSUS[(paper['year'], paper['level'])] = [
                (tuple(l['key']), l['label'], l['text']) for l in paper['leaves']]
    return _CENSUS[(year, level)]


def evidence(part):
    """The scheme part's own words, for scoring against the paper's ask."""
    words = [part.cue] + [r for r in part.rows if not S.TABLE_HEAD.match(r)]
    return bag(' '.join(words))


def pair(year, level):
    """(paper, parts, pairs, unpaired, why) for one sitting.

    `pairs` maps a CENSUS leaf key to the scheme part that prices it, with the
    route that made it evidence.  `unpaired` is the leaf asks no part reaches.
    """
    paper = Paper(SUBJECT, year, level)
    asks = leaves(year, level)
    parts = S.read(year, level)
    by_key = {}
    for p in parts:
        by_key.setdefault(p.address, p)
    shape_ok = {}
    for q in {k[0] for k, _, _ in asks}:
        mine = [(k[1], k[2]) for k, _, _ in asks if k[0] == q]
        every = [p.address[1:] for p in parts if p.address[0] == q]
        theirs = [t for t in every if t != (None, None)]
        # Either the two documents print the same markers under this question
        # in the same order, or NEITHER prints a marker at all — a question
        # both documents keep whole has exactly one unit on each side, which
        # is the same rule at one row.
        shape_ok[q] = ((bool(mine) and mine == theirs)
                       or (mine == [(None, None)] and every == [(None, None)]))

    pairs, unpaired = collections.OrderedDict(), []
    why = collections.Counter()
    for key, label, text in asks:
        q, letter, roman = key
        exact = by_key.get(key)
        ask_bag = bag(text or '')
        if exact is not None:
            agreement = score(evidence(exact), ask_bag)
            if agreement >= FLOOR:
                pairs[key] = (exact, 'wording', round(agreement, 2))
                why['wording'] += 1
                continue
            if shape_ok[q]:
                pairs[key] = (exact, 'shape', round(agreement, 2))
                why['shape'] += 1
                continue
        # The scheme priced a level UP: the letter where the paper numbers
        # romans, or the question where the paper letters its asks. The ask is
        # inside that part, which is how reconcile.py reads a card cited there.
        for up in ((q, letter, None), (q, None, None)):
            if up == key:
                continue
            parent = by_key.get(up)
            if parent is None:
                continue
            agreement = score(evidence(parent), ask_bag)
            pairs[key] = (parent, 'parent', round(agreement, 2))
            why['parent'] += 1
            break
        else:
            unpaired.append((key, label, text))
    return paper, parts, pairs, unpaired, why


def audit():
    rows = []
    for year, level in SITTINGS:
        paper, parts, pairs, unpaired, why = pair(year, level)
        asks = len(pairs) + len(unpaired)
        rows.append((asks, len(pairs)))
        print(f'{year} {level.upper()}: {asks} leaf asks, {len(parts)} scheme '
              f'parts, {len(pairs)} paired '
              f'({why["wording"]} wording, {why["shape"]} shape, '
              f'{why["parent"]} parent), {len(unpaired)} unpaired')
        for key, label, text in unpaired[:6]:
            print(f'    UNPAIRED {label}: {(text or "")[:70]}')
    tot, paired = sum(r[0] for r in rows), sum(r[1] for r in rows)
    print(f'\n{paired}/{tot} leaf asks paired to a scheme part '
          f'({paired * 100 // max(tot, 1)}%)')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        y, lv = int(sys.argv[1]), sys.argv[2]
        paper, parts, pairs, unpaired, _ = pair(y, lv)
        for key, (part, route, sc) in pairs.items():
            print(f'{key} <- {part!r} [{route} {sc}]')
        for key, label, text in unpaired:
            print(f'UNPAIRED {label}: {(text or "")[:90]}')
    else:
        audit()
