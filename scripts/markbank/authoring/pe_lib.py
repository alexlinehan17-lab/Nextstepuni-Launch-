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


def tidy(s):
    return ' '.join((s or '').split())


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


# The paper's own page furniture, printed inside a stem.
STEM_JUNK = re.compile(
    r'\s*(?:This question continues on the next page\.?'
    r'|Space for extra work.*$|Do not write on this page.*$'
    r'|Section\s+[ABC]\b.*$|\(\d{1,3}\s*marks?\)'
    r'|Indicate clearly the question number.*$)', re.I)
# A stem that OPENS with the paper's own instruction is the ask itself: the
# walker keeps the stimulus sentence as the part's text and files the
# imperative printed under it as the stem, so 106 of the 741 leaf asks print
# their verb one level away from their own text.
ASK_OPENER = re.compile(
    r'^(what|why|how|when|where|which|who|name|state|give|list|define|explain'
    r'|describe|identify|suggest|outline|discuss|examine|analyse|compare'
    r'|evaluate|justify|complete|write|select|choose|tick|put|match|fill'
    r'|apply|label|comment|account|distinguish|calculate|draw|using|from the)\b',
    re.I)

_CENSUS = {}
_PAPERS = {}


def paper_for(year, level):
    if (year, level) not in _PAPERS:
        _PAPERS[(year, level)] = Paper(SUBJECT, year, level)
    return _PAPERS[(year, level)]


def leaves(year, level):
    """The census's own leaf asks for one paper, as (key, label, text).

    The KEYS and the LABELS come from paper_census.py itself rather than being
    re-walked here, so the denominator this reader works against is the one
    reconcile.py checks. The TEXT does not: the census stores the first 160
    characters of an ask, which is all a census needs and half of what a card
    needs — "Put a tick in the True or False column for each of the following
    statements:" and four of its six statements. The full printed wording is
    read back off the paper, with the census's own text as the fallback for a
    key the census completed and the walker does not hold.
    """
    if not _CENSUS:
        for paper in census_subject(SUBJECT)['papers']:
            _CENSUS[(paper['year'], paper['level'])] = [
                (tuple(l['key']), l['label'], l['text']) for l in paper['leaves']]
    paper = paper_for(year, level)
    return [(key, label, ask_text(year, level, key, paper.text(*key) or text))
            for key, label, text in _CENSUS[(year, level)]]


def ask_text(year, level, key, printed):
    """The whole printed ask, in the paper's own words.

    The census keeps what the walker filed under the leaf's own marker. Where
    that is the stimulus and the imperative was filed one level up — which is
    what the walker does when the SEC prints "Physical Education is a concept
    of physical activity." and then "Explain Physical Education in this
    context." as two blocks — the instruction is put back on the end, in the
    order the page prints it. Only an instruction is ever added: a stem that
    does not OPEN with one of the paper's own ask verbs is a table heading, a
    figure caption or a continuation notice, and adding one of those would
    make the question worse rather than whole.
    """
    text = tidy(STEM_JUNK.sub(' ', printed))
    if ASK_OPENER.match(text):
        return text
    stem = tidy(STEM_JUNK.sub(' ', paper_for(year, level).stem(key[0], key[1]) or ''))
    if stem and ASK_OPENER.match(stem) and stem.lower() not in text.lower():
        return tidy(f'{text} {stem}')
    return text


# ------------------------------------------------------------ the source ----
# An ask that points at a printed figure, table or case study is not refused
# for pointing at one: the SEC's own page is in the Paper Trail index, and
# card-source-bindings.json attaches it so the student opens the exact
# examination page the question was set on. What still cannot be carded is an
# answer the SCHEME does not state in words — a tick in a column, or the other
# half of a matching table — and those keep their own named buckets.
_PAGES = {}


def _page_text(year, level):
    if (year, level) not in _PAGES:
        import pymupdf
        path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')
        with pymupdf.open(path) as doc:
            _PAGES[(year, level)] = [tidy(page.get_text()) for page in doc]
    return _PAGES[(year, level)]


def _flat(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').lower())


def source_pages(year, level, qtext):
    """The paper's own page(s) this ask and its source are printed on.

    One-based, as build-deck requires, and found by searching the paper for the
    ask's own words and for every figure it names — never guessed from the
    question number, which is a page apart from its figure often enough to put
    the wrong page in front of a student.
    """
    pages = _page_text(year, level)
    wanted = _flat(qtext)[:60]
    found = []
    if wanted:
        for i, text in enumerate(pages):
            if wanted and wanted in _flat(text):
                found.append(i + 1)
                break
    for label in re.findall(r'\bFigure\s*\d+\b', qtext, re.I):
        needle = _flat(label)
        for i, text in enumerate(pages):
            if needle in _flat(text):
                if (i + 1) not in found:
                    found.append(i + 1)
                break
    return sorted(found)[:2]


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
        # A parent that prices NOTHING is not a pricing, and pairing to one is
        # strictly worse than pairing to the address both documents print:
        # sixteen asks were excluded as "the scheme prints no row for this
        # part" while the scheme's own row for them sat one level down,
        # unreachable because a stimulus-heavy ask shares no word with the
        # table that prices it.
        for up in ((q, letter, None), (q, None, None)):
            if up == key:
                continue
            parent = by_key.get(up)
            if parent is None or not (parent.rows or parent.answers or parent.cue):
                continue
            agreement = score(evidence(parent), ask_bag)
            pairs[key] = (parent, 'parent', round(agreement, 2))
            why['parent'] += 1
            break
        else:
            # The last route, and the weakest: the ADDRESS both documents
            # print, used only where the scheme's part at it states something
            # and nothing above it does. Counted separately so the share of
            # the deck resting on it is always visible.
            if exact is not None and (exact.rows or exact.answers):
                pairs[key] = (exact, 'address', 0.0)
                why['address'] += 1
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
              f'{why["parent"]} parent, {why["address"]} address), '
              f'{len(unpaired)} unpaired')
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
