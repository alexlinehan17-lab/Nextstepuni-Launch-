#!/usr/bin/env python3
"""Pair a Physical Education paper ask with the scheme part that prices it.

    python3 scripts/markbank/authoring/pe_lib.py            # the pairing audit
    python3 scripts/markbank/authoring/pe_lib.py 2024 hl    # one sitting

LAW 4 — never join paper to scheme on the part key — applies here even though
PE's two documents happen to print the SAME address.  The key is where the
pairing STARTS; wording is what makes it evidence.  Two independent checks have
to agree before a pair is used:

  1. the key printed on the scheme part exists on the paper, and
  2. the scheme part's own words echo the paper's ask.

For 2023 onward (2) is easy: the scheme reprints the ask above its table, so
the cue is scored against the paper's text directly.  For 2020-2022 the scheme
reprints NOTHING — a part opens "Question 3 (6 Marks)", "(a)", "Description
Marks" and goes straight to "Identifies test to measure flexibility 1 mark".
There the evidence is the criterion ROWS, which are the ask rewritten as what
the examiner must see: "Identifies test to measure flexibility" against
"Identify a test that could be used to measure flexibility".  Scored the same
way, they agree at the same rate.

Where neither scores, the pair is REPORTED, not used.  A wrong pairing shows a
real question under a real answer that does not answer it and passes every
downstream gate; the only thing that catches it is refusing to make it.
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

SUBJECT = 'physical-education'
# 2020 sat an altered examination: Section C offered three long questions where
# every other year offers five, so its paper stops at Question 16.
SITTINGS = [(2020, 'hl')] + [(y, lv) for y in range(2021, 2027)
                             for lv in ('hl', 'ol')]
# The wording floor.  Set from the corpus rather than picked: at 0.30 every
# sitting pairs over 85% of its scheme parts, and the pairs that fall below it
# are the ones whose scheme part prints nothing but a mark ladder — which have
# no words to agree with and are refused for that reason anyway.
FLOOR = 0.30


def scheme_dir():
    return os.path.join(ROOT, 'examiner-reports', SUBJECT, 'schemes')


def load_md(year, level):
    """The scheme markdown the provenance gate reads, normalised the way it is."""
    path = os.path.join(scheme_dir(), f'{year}-{level}.md')
    raw = open(path, encoding='utf-8').read()
    keep = [l for l in raw.split('\n')
            if not re.match(r'^##\s*Page\s*\d+\s*$', l)
            and not re.match(r'^\s*\d+\s*$', l)]
    return normalise('\n'.join(keep))


_MD = {}


def traces(year, level, text):
    """True where `text` appears in its own scheme, the way the gate compares."""
    key = (year, level)
    if key not in _MD:
        _MD[key] = load_md(year, level)
    return normalise(text) in _MD[key]


def normalise(text):
    text = (text or '').replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('–', '-').replace('—', '-')
    return re.sub(r'\s+', ' ', text).strip().lower()


def evidence(part):
    """The scheme part's own words, for scoring against the paper's ask."""
    words = [part.cue] + [r for r in part.rows if not S.TABLE_HEAD.match(r)]
    return bag(' '.join(words))


def _shape(keys, q):
    """The part markers one document prints under question `q`, in order."""
    return [(k[1], k[2]) for k in keys if k[0] == q]


def pair(year, level):
    """(paper, parts, pairs, unpaired) for one sitting.

    `pairs` maps a paper key to the scheme parts that price it, in printed
    order — a paper ask is sometimes answered by two consecutive scheme parts
    (2020 prices Q4's two types of feedback in one table and its two
    explanations in the next).
    """
    paper = Paper(SUBJECT, year, level)
    keys = list(paper.paths())
    text = {k: paper.text(*k) or '' for k in keys}
    parts = S.read(year, level)

    pairs, unpaired = collections.OrderedDict(), []
    why = collections.Counter()
    scheme_keys = [p.address for p in parts]
    for part in parts:
        q, letter, roman = part.address
        candidates = [k for k in keys if k[0] == q]
        if not candidates:
            unpaired.append((part, 0.0, 'the paper prints no such question'))
            continue
        exact = [k for k in candidates if k[1] == letter and k[2] == roman]
        # A scheme part addressed at the QUESTION where the paper letters its
        # asks is the question's own head; it prices the whole question.
        if not exact and letter is None and roman is None:
            exact = candidates
        if not exact:
            # The paper wins over the scheme on the address. A letter the
            # paper does not print is reported, never re-keyed to a neighbour.
            unpaired.append((part, 0.0, 'the paper prints no such part'))
            continue
        ev = evidence(part)
        best = max(exact, key=lambda k: score(ev, bag(text[k])))
        agreement = score(ev, bag(text[best])) if ev else 0.0
        if agreement >= FLOOR:
            pairs.setdefault(best, []).append(part)
            why['wording'] += 1
            continue
        # The second route, for the sittings that reprint NOTHING. 2020, 2021
        # and 2022 open a part "(a)", "Description Marks" and go straight to
        # "Identifies test to measure flexibility 1 mark" — there are no words
        # to score, and refusing on that alone lost 196 parts across the
        # corpus. What is still printed is the SHAPE: the markers the two
        # documents set under one question. Accepted only when they are
        # IDENTICAL and in the same order, which is the Baltic rule — the two
        # documents must print the same number of rows under that letter — and
        # never where the scheme prints one marker the paper does not.
        if _shape(scheme_keys, q) == _shape(keys, q) and len(exact) == 1:
            pairs.setdefault(exact[0], []).append(part)
            why['shape'] += 1
            continue
        # The third route, and the last: printed ORDER, under the Baltic rule —
        # the two documents must print the SAME NUMBER of parts under that
        # question, and the pairing is then position for position. It is what
        # recovers the case study, where the scheme addresses "Q13 (i)" and
        # "Q13 (ii)" the paper prints as "Q13(a)(i)" and "Q13(a)(ii)": the
        # paper wins on the address, and the order is the evidence. One
        # mismatch in the count abandons the whole question rather than
        # shifting the rest by one.
        mine, theirs = _shape(scheme_keys, q), _shape(keys, q)
        if len(mine) == len(theirs) and len(mine) > 1:
            pairs.setdefault(keys[[k[0] for k in keys].index(q)
                                  + mine.index((letter, roman))], []).append(part)
            why['order'] += 1
            continue
        unpaired.append((part, round(agreement, 2),
                         'neither the wording, the printed shape nor the order agrees'))
    return paper, parts, pairs, unpaired, why


def audit():
    rows = []
    for year, level in SITTINGS:
        paper, parts, pairs, unpaired, why = pair(year, level)
        rows.append((year, level, len(list(paper.paths())), len(parts),
                     sum(len(v) for v in pairs.values()), len(unpaired)))
        print(f'{year} {level.upper()}: {len(list(paper.paths()))} paper asks, '
              f'{len(parts)} scheme parts, '
              f'{sum(len(v) for v in pairs.values())} paired, '
              f'{len(unpaired)} unpaired '
              f'({why["wording"]} on wording, {why["shape"]} on printed shape, '
              f'{why["order"]} on printed order)')
        for part, sc, reason in unpaired[:6]:
            print(f"    UNPAIRED {part!r} {sc} — {reason}")
    tot_parts = sum(r[3] for r in rows)
    tot_paired = sum(r[4] for r in rows)
    print(f'\n{tot_paired}/{tot_parts} scheme parts paired on wording '
          f'({tot_paired * 100 // max(tot_parts, 1)}%)')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        y, lv = int(sys.argv[1]), sys.argv[2]
        paper, parts, pairs, unpaired, _ = pair(y, lv)
        for key, ps in pairs.items():
            print(f'{key} <- {[repr(p) for p in ps]}')
            print(f'    {(paper.text(*key) or "")[:120]}')
        for part, sc, why in unpaired:
            print(f'UNPAIRED {part!r} {sc} — {why}')
    else:
        audit()
