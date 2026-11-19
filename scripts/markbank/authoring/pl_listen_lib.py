#!/usr/bin/env python3
"""The selector language a Polish listening (and written-task) spec is written in.

Every string a card shows is CUT from a printed document by a selector, never
typed: `S(n)` is line n of the scheme's .md (the very text build-deck's
provenance check reads), `S(n, after=..., before=...)` cuts that line at two
printed anchors, and `J(...)` joins cuts that the SEC wrapped over lines.
Marks are READ from the tariff the scheme prints (`T(n)` parses the k-th
tariff on line n) and every card is checked to add up to it. The question
comes from the paper's own text layer (pl_paper, the census's reading of the
Listening Comprehension booklet); `Q(...)` overrides it with cut paper lines.

The spec only decides which printed lines are the answers, which are a
lower-paid alternative, and which address the card answers. See
pl_listen_specs.py for the specs and pl_listen.py for the side-by-side draft
the specs are written from.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

BULLET = re.compile(r'^[\s\-‐–—•●▪✓✔]+')
# Every price notation these schemes print: (2x2 m) (2 x 2 m) (2 m) (2m)
# (3 marks) (3 x 3 marks) (1 x 2 marks) (2+2 m), and a bare "2 m" / "1 mark"
# in a table's last cell.
TARIFF = re.compile(
    r'\(\s*(?P<n>\d{1,2})\s*[x×]\s*(?P<p>\d{1,2})\s*(?:m|marks?)\s*\)'
    r'|\(\s*(?P<p1>\d{1,2})\s*(?:m|marks?)\s*\)'
    r'|\(\s*(?P<s0>\d{1,2})(?P<sr>(?:\s*\+\s*\d{1,2}){1,7})\s*(?:m|marks?)\s*\)'
    r'|(?<![\w(])(?P<p2>\d{1,2})\s*(?:m|marks?)\b(?!\s*\))', re.I)


class Sel:
    """A cut of printed text. `src` is 'scheme' or 'paper'."""
    def __init__(self, src, n, after=None, before=None, keep_tariff=False):
        self.src, self.n, self.after, self.before = src, n, after, before
        self.keep_tariff = keep_tariff

    def text(self, doc):
        lines = doc[self.src]
        if not (1 <= self.n <= len(lines)):
            raise ValueError(f'{self.src} line {self.n} does not exist')
        t = lines[self.n - 1]
        if self.after is not None:
            if self.after not in t:
                raise ValueError(f'{self.src} line {self.n}: anchor {self.after!r} not in {t!r}')
            t = t.split(self.after, 1)[1]
        if self.before is not None:
            if self.before not in t:
                raise ValueError(f'{self.src} line {self.n}: anchor {self.before!r} not in {t!r}')
            t = t.split(self.before, 1)[0]
        if not self.keep_tariff:
            t = TARIFF.sub(' ', t)
        t = BULLET.sub('', t)
        t = re.sub(r'\s+', ' ', t).strip()
        t = re.sub(r'\s*\bor\s*$', '', t).strip()
        if not t:
            raise ValueError(f'{self.src} line {self.n} cut to nothing')
        return t


def S(n, after=None, before=None, raw=False):
    """`raw` keeps the prices in the cut: a quoted note, never an answer."""
    return Sel('scheme', n, after, before, keep_tariff=raw)


class Join:
    def __init__(self, *parts, sep=' '):
        self.parts, self.sep = parts, sep

    def text(self, doc):
        out = ''
        for p in self.parts:
            t = p.text(doc)
            # A line the SEC wrapped right after a slash continues the same
            # word list: "sport centres/" over "schools".
            out = f'{out}{t}' if out.endswith('/') else (f'{out}{self.sep}{t}' if out else t)
        return re.sub(r'\s+', ' ', out).strip()


def J(*parts):
    return Join(*parts)


class Tariff:
    """The k-th price printed on scheme line n: (count, per). With `each`, one
    answer at the per-answer price: a table row of "(3 x 3 marks)"."""
    def __init__(self, n, k=0, each=False):
        self.n, self.k, self.each = n, k, each

    def read(self, doc):
        line = doc['scheme'][self.n - 1]
        found = list(TARIFF.finditer(line))
        if len(found) <= self.k:
            raise ValueError(f'scheme line {self.n} prints no tariff #{self.k}: {line!r}')
        m = found[self.k]
        if m.group('n'):
            return (1 if self.each else int(m.group('n'))), int(m.group('p')), m.group(0)
        if m.group('s0'):
            terms = [int(m.group('s0'))] + [int(t) for t in re.findall(r'\d{1,2}', m.group('sr'))]
            if len(set(terms)) != 1:
                raise ValueError(f'scheme line {self.n}: unequal terms in {m.group(0)!r}')
            return (1 if self.each else len(terms)), terms[0], m.group(0)
        per = int(m.group('p1') or m.group('p2'))
        return 1, per, m.group(0)


def T(n, k=0, each=False):
    return Tariff(n, k, each)


# ------------------------------------------------------------------ rows ---
class Row:
    pass


class One(Row):
    """One answer, priced by the card's tariff (or its own). `lead` is the
    printed question this row answers, where one ask sets two (a table)."""
    def __init__(self, sel, tariff=None, alts=(), lead=None):
        self.sel, self.tariff, self.alts, self.lead = sel, tariff, alts, lead


class Menu(Row):
    """"Any N of": the options, the printed (N, per), and any lower-paid
    alternatives — (selector, index of the option it stands in for, tariff)."""
    def __init__(self, options, tariff=None, partials=(), lead=None):
        self.options, self.tariff, self.partials, self.lead = options, tariff, partials, lead


def one(sel, tariff=None, partials=(), lead=None):
    return One(sel, tariff, partials, lead)


def menu(options, tariff=None, partials=(), lead=None):
    return Menu(options, tariff, partials, lead)


def part(sel, of, tariff):
    """A lower-paid alternative standing in for option `of` (0-based)."""
    return (sel, of, tariff)


class ColumnMarks:
    """The number in a table's "Marks" column, last on scheme line n: a
    true/false row "(vi) Harcerze potrafią ... ✓ 2"."""
    def __init__(self, n):
        self.n = n

    def read(self, doc):
        line = doc['scheme'][self.n - 1]
        m = re.search(r'(\d{1,2})\s*$', line)
        if not m:
            raise ValueError(f'scheme line {self.n} ends in no marks cell: {line!r}')
        return 1, int(m.group(1)), m.group(1)


def TM(n):
    return ColumnMarks(n)


class PaperLine:
    """The question paper's printed line on `page` that opens with `opening`."""
    def __init__(self, page, opening):
        self.page, self.opening = page, opening

    def text(self, doc):
        hits = [t for p, t in doc['paper'] if p == self.page and t.startswith(self.opening)]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page}: {len(hits)} lines open {self.opening!r}')
        return re.sub(r'\s+', ' ', hits[0]).strip()


def PL(page, opening):
    return PaperLine(page, opening)


class Token:
    """The k-th cell of a printed row of single-word cells, scheme line n:
    "E C F A B D" under "1. 2. 3. 4. 5. 6." (a matching task's key)."""
    def __init__(self, n, k):
        self.n, self.k = n, k

    def text(self, doc):
        cells = doc['scheme'][self.n - 1].split()
        if self.k >= len(cells):
            raise ValueError(f'scheme line {self.n} has no cell #{self.k}')
        return cells[self.k]


def W(n, k):
    return Token(n, k)
