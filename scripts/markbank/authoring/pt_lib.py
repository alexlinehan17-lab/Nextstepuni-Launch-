#!/usr/bin/env python3
"""The selector language a Portuguese spec (reading and listening) is written in.

Portuguese-only, on the Polish pattern (pl_listen_lib): every string a card
shows is CUT from a printed document by a selector, never typed. `S(n)` is
line n of the scheme's .md (the text build-deck's provenance check reads),
cut at printed anchors with `after=` / `before=`; `J(...)` joins lines the SEC
wrapped. Marks are READ from the price the scheme prints (`T(n)`) and every
card is checked to add up to it.

The Portuguese schemes (2022 on) set every price in the marks column, which
the .md carries in angle brackets beside the answer: "Há um problema técnico
com as escadas do avião. ⟨2 marks: 2 x 1 mark⟩", "⟨(any 2)⟩" under it. A cut
is taken from the line with those cells blanked; a price is read from the line
as printed (a cell the extractor left unbracketed, "4 marks: 2 x 2 marks", is
read the same way).

Row shapes, each a CARD-STANDARD treatment with a precedent in the bank:
* one(sel, T)          one answer at its printed price (a point row);
* menu([sel...], T)    "n x p" over printed answers: anyN, claim n at p each;
* alt(sel, T, of)      inside a menu, an answer the scheme prices LOWER:
                       in place of option `of` where printed as its
                       alternative, else an answer of its own (optionOf null);
* stepped(sel, T)      one printed statement priced "n x p" that does not cut
                       into n answers: a criterion row placed on 0, p ... n*p
                       (Spanish es-2010-hl-a1a-5: [0, 3, 6, 9]);
* shown(sel)           a line shown after the reveal with no marks of its own,
                       on a card the scheme prices only as a whole
                       (questionTotal, CARD-STANDARD 5).
A table of cue and answer ("Lenta (parte 1) Rápida") is one point row per
pair, the cue as the row's lead ("For “Lenta (parte 1)”").
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from pl_listen_lib import Sel, Join, J, PL                       # noqa: E402,F401

SCHEMES = os.path.join(ROOT, 'examiner-reports', 'portuguese', 'schemes')
ANGLE = re.compile('⟨[^⟩]*⟩')
# "6 marks: 2 x 3 marks", "4 marks", "1 marks: 1 x 1 mark", "20 Marks".
# The per-answer "marks" may be left off: "⟨6 marks: 3 x 2⟩" (2023 Ordinary).
PRICE = re.compile(r'(?<![\w.])(?P<total>\d{1,3})\s*marks?\b'
                   r'(?:\s*:\s*(?P<n>\d{1,2})\s*[x×]\s*(?P<p>\d{1,2})(?:\s*marks?\b)?)?', re.I)
ANY_N = re.compile(r'\(\s*any\s+(\d{1,2})\s*\)', re.I)


def scheme_doc(year, level):
    with open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf-8') as fh:
        raw = fh.read().split('\n')
    return {'raw': raw, 'scheme': [ANGLE.sub(' ', l) for l in raw]}


def S(n, after=None, before=None):
    return Sel('scheme', n, after, before)


class Bullets:
    """Printed bullets read as one answer (a stepped price over several
    bullets): each bullet's text, the bullet break shown as "; " where the
    bullet does not already end in punctuation. A bullet the SEC wrapped is
    one J(...) part."""
    def __init__(self, *parts):
        self.parts = parts

    def text(self, doc):
        out = ''
        for p in self.parts:
            t = p.text(doc)
            out = t if not out else (f'{out} {t}' if re.search(r'[.;:!?]$', out) else f'{out}; {t}')
        return out


def B(*parts):
    return Bullets(*parts)


class Cell:
    """The text of the k-th marks-column cell on scheme line n, as printed:
    the number a numbering task's answer column sets there ("⟨4⟩", 2024
    Higher Q2(j)), which the cut view of the line blanks with the prices."""
    def __init__(self, n, k=0):
        self.n, self.k = n, k

    def text(self, doc):
        cells = [m.group(0)[1:-1].strip() for m in ANGLE.finditer(doc['raw'][self.n - 1])]
        if len(cells) <= self.k or not cells[self.k]:
            raise ValueError(f'scheme line {self.n} prints no cell #{self.k}')
        return cells[self.k]


def CELL(n, k=0):
    return Cell(n, k)


class Price:
    """The k-th price printed on scheme line n: (count, per, notation). With
    `each`, one answer at the per-answer price (a table row of "4 x 1 mark")."""
    def __init__(self, n, k=0, each=False):
        self.n, self.k, self.each = n, k, each

    def read(self, doc):
        line = doc['raw'][self.n - 1]
        found = list(PRICE.finditer(line))
        if len(found) <= self.k:
            raise ValueError(f'scheme line {self.n} prints no price #{self.k}: {line!r}')
        m = found[self.k]
        total = int(m.group('total'))
        notation = m.group(0)
        tail = line[m.end():m.end() + 40]
        any_n = ANY_N.search(tail) or ANY_N.search(doc['raw'][self.n] if self.n < len(doc['raw']) else '')
        if any_n:
            notation = f'{notation} (any {any_n.group(1)})'
        if m.group('n'):
            n, p = int(m.group('n')), int(m.group('p'))
            if n * p != total:
                raise ValueError(f'scheme line {self.n}: {m.group(0)!r} does not add up')
            return (1 if self.each else n), p, notation
        return 1, total, notation


def T(n, k=0, each=False):
    return Price(n, k, each)


SPLIT_TOTAL = re.compile(r'(\d{1,3})\s*marks?\s*:', re.I)
SPLIT_EACH = re.compile(r'(\d{1,2})\s*[x×]\s*(\d{1,2})\s*marks?\b', re.I)


class SplitPrice:
    """A price the scheme breaks over two lines: "⟨4 marks:⟩" on line n1,
    "⟨4 x 1 mark⟩" on line n2 (2025 Ordinary). Read from both, checked to add
    up; with `each`, one answer at the per-answer price."""
    def __init__(self, n1, n2, each=False):
        self.n1, self.n2, self.each = n1, n2, each

    def read(self, doc):
        a, b = doc['raw'][self.n1 - 1], doc['raw'][self.n2 - 1]
        t, e = SPLIT_TOTAL.search(a), SPLIT_EACH.search(b)
        if not t or not e:
            raise ValueError(f'scheme lines {self.n1}/{self.n2} print no split price: {a!r} / {b!r}')
        total, n, p = int(t.group(1)), int(e.group(1)), int(e.group(2))
        if n * p != total:
            raise ValueError(f'scheme lines {self.n1}/{self.n2}: {t.group(0)} {e.group(0)} does not add up')
        notation = f'{t.group(0)} {e.group(0)}'
        return (1 if self.each else n), p, notation


def T2(n1, n2, each=False):
    return SplitPrice(n1, n2, each)


class GluedPrice:
    """One price cell the extractor broke over two lines' marks cells:
    "⟨3 marks: 3 x 1⟩" on n1 and "⟨mark⟩" on n2 (2023 Higher Parte E): the
    cells' text joined, then read as one price."""
    def __init__(self, n1, n2, each=False):
        self.n1, self.n2, self.each = n1, n2, each

    def read(self, doc):
        cells = ' '.join(m.group(0)[1:-1] for n in (self.n1, self.n2)
                         for m in ANGLE.finditer(doc['raw'][n - 1]))
        m = PRICE.search(cells)
        if not m or not m.group('n'):
            raise ValueError(f'scheme lines {self.n1}/{self.n2}: no split price in {cells!r}')
        n, p, total = int(m.group('n')), int(m.group('p')), int(m.group('total'))
        if n * p != total:
            raise ValueError(f'scheme lines {self.n1}/{self.n2}: {m.group(0)!r} does not add up')
        return (1 if self.each else n), p, m.group(0)


def TG(n1, n2, each=False):
    return GluedPrice(n1, n2, each)


ANY_WORD = re.compile(r'\bany\s+(\d{1,2})\b', re.I)


class AnyOf:
    """One printed list's share of a price set over several lists: the count
    from the "Any 3" printed beside the list on line n_any, the per-answer
    marks from `price` (2025 Ordinary Q3(b): "12 marks: 6 x 2 marks" over two
    columns, each "Any 3")."""
    def __init__(self, price, n_any):
        self.price, self.n_any = price, n_any

    def read(self, doc):
        _c, per, notation = self.price.read(doc)
        m = ANY_WORD.search(doc['raw'][self.n_any - 1])
        if not m:
            raise ValueError(f'scheme line {self.n_any} prints no "Any N"')
        return int(m.group(1)), per, f'{notation}, {m.group(0)}'


class Row:
    lead = None


class One(Row):
    def __init__(self, sel, tariff, lead=None):
        self.sel, self.tariff, self.lead = sel, tariff, lead


class Menu(Row):
    def __init__(self, options, tariff, alts=(), lead=None):
        self.options, self.tariff, self.alts, self.lead = options, tariff, alts, lead


class Alt:
    """A lower-priced answer. `of` is the index of the fuller answer it is
    printed as an alternative to ("ou", "or", "accept ... for N": paid in place
    of it, never beside it); None only where the scheme prints it as a
    distinct point of its own."""
    def __init__(self, sel, tariff, of=None):
        self.sel, self.tariff, self.of = sel, tariff, of


class Stepped(Row):
    def __init__(self, sel, tariff, lead=None):
        self.sel, self.tariff, self.lead = sel, tariff, lead


class Shown(Row):
    def __init__(self, sel, lead=None):
        self.sel, self.lead = sel, lead


class Rest(Row):
    """The marks a price pays beyond the answers the scheme prints: "6 marks:
    3 x 2 marks" over two printed answers leaves 2 for which it prints none.
    The card's LAST row, CARD-STANDARD 3 (UNPRINTED_ANSWER), as German
    de-2011-hl-t2-3-a: a criterion row with the fixed line, placed 0 to its
    marks. `printed` is how many answers the scheme prints; each was carded
    at the price's per-answer marks."""
    def __init__(self, tariff, printed):
        self.tariff, self.printed = tariff, printed


UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'
NUMBER = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven'}


def rest(tariff, printed):
    return Rest(tariff, printed)


def one(sel, tariff, lead=None):
    return One(sel, tariff, lead)


def menu(options, tariff, alts=(), lead=None):
    return Menu(options, tariff, alts, lead)


def alt(sel, tariff, of=None):
    return Alt(sel, tariff, of)


def stepped(sel, tariff, lead=None):
    return Stepped(sel, tariff, lead)


def shown(sel, lead=None):
    return Shown(sel, lead)


class PctCriterion(Row):
    """A percentage criterion the scheme prints for an essay ("1. Clareza do
    discurso – ... - 30%", 2010/2011 Higher Parts II and III), carded under
    CARD-STANDARD 10b: the printed line whole, at its percentage of the
    printed total, placed 0 to that mark. Refused unless the percentage times
    the total is a whole number (never round a tariff into existence)."""
    def __init__(self, sel, total, lead=None):
        self.sel, self.total, self.lead = sel, total, lead


def pct(sel, total, lead=None):
    return PctCriterion(sel, total, lead)


def pairs(lines, tariff, after=None):
    """One point row per printed cue/answer pair on `lines`, each at the
    per-answer price of `tariff` (a scheme line number, or a price object):
    "Lenta (parte 1) Rápida" is the answer "Rápida" led by its cue "Lenta
    (parte 1)". `after` is the text that closes the cue on every line (the
    part reference, or the statement's full stop)."""
    price = T(tariff, each=True) if isinstance(tariff, int) else tariff
    return [one(Cut(n, after), price, lead=Cue(n, after)) for n in lines]


class Cut(Sel):
    """The answer cell of a cue/answer row: what follows the cue's closing
    reference "(parte 1)" / "(Parágrafo 3)"."""
    def __init__(self, n, closer=None):
        super().__init__('scheme', n)
        self.closer = closer

    def _split(self, doc):
        line = re.sub(r'\s+', ' ', doc['scheme'][self.n - 1].replace('\xa0', ' ')).strip()
        if self.closer:
            if self.closer not in line:
                raise ValueError(f'scheme line {self.n}: {self.closer!r} not in {line!r}')
            cue, ans = line.split(self.closer, 1)
            return f'{cue}{self.closer}'.strip(), ans.strip()
        m = re.match(r'^(.*\))\s+(\S.*)$', line)
        if not m:
            raise ValueError(f'scheme line {self.n}: no cue/answer split in {line!r}')
        return m.group(1).strip(), m.group(2).strip()

    def text(self, doc):
        return self._split(doc)[1]


class Cue(Cut):
    def text(self, doc):
        return self._split(doc)[0]


def _marks(n):
    return 'mark' if n == 1 else 'marks'


def _joined(ctx, said):
    """A row's own note after its lead: "For “Assaltante 2”: The scheme ..."."""
    if not ctx:
        return said
    return f'{ctx}: {said}' if ctx.endswith('”') else f'{ctx} {said}'


def build_rows(doc, rows, note, key=''):
    """The card's rows and the marks they add to. The language note (and any
    card note) goes on the FIRST row only, as German, Spanish and Polish set
    it; a later row carries its own lead ("For “…”") or nothing."""
    out, total = [], 0
    for i, r in enumerate(rows, 1):
        rid = f'r-{i}'
        lead = r.lead.text(doc) if r.lead is not None else None
        if i == 1:
            ctx = f'For “{lead}”: {note}' if lead else note
        else:
            ctx = f'For “{lead}”' if lead else ''
        if isinstance(r, Shown):
            out.append({'id': rid, 'kind': 'point', 'verbatim': r.sel.text(doc), 'marks': None,
                        **({'contextNote': ctx} if ctx else {})})
            continue
        if isinstance(r, PctCriterion):
            text = r.sel.text(doc)
            m = re.search(r'(\d{1,3})\s*%\s*$', text)
            if not m:
                raise ValueError(f'{key}: criterion {text!r} ends in no percentage')
            count, per, notation = r.total.read(doc)
            whole = count * per
            if int(m.group(1)) * whole % 100:
                raise ValueError(f'{key}: {m.group(1)}% of {notation!r} is not a whole mark')
            marks = int(m.group(1)) * whole // 100
            out.append({'id': rid, 'kind': 'criterion', 'verbatim': text, 'marks': marks,
                        'permittedMarks': list(range(marks + 1)),
                        **({'contextNote': ctx} if ctx else {})})
            total += marks
            continue
        if isinstance(r, One):
            count, per, notation = r.tariff.read(doc)
            if count != 1:
                raise ValueError(f'{key}: one answer priced {notation!r}; use stepped() or menu()')
            out.append({'id': rid, 'kind': 'point', 'verbatim': r.sel.text(doc), 'marks': per,
                        **({'contextNote': ctx} if ctx else {})})
            total += per
            continue
        if isinstance(r, Rest):
            count, per, notation = r.tariff.read(doc)
            left = (count - r.printed) * per
            if left <= 0:
                raise ValueError(f'{key}: {notation!r} pays no more than the {r.printed} printed answers')
            if r.printed == 0:
                # A task the scheme prints no answer for at all (2018 Higher
                # Part III Proposta 2): the card's one row.
                said = f'The paper prices this task “{notation}”; the scheme prints no answer for it.'
            else:
                said = (f'The scheme prices this ask “{notation}” and prints {NUMBER[r.printed]} '
                        f'answer{"" if r.printed == 1 else "s"}; it prints no answer for the rest.')
            out.append({'id': rid, 'kind': 'criterion', 'verbatim': UNPRINTED_ANSWER, 'marks': left,
                        'unprinted': True, 'permittedMarks': list(range(left + 1)),
                        'contextNote': _joined(ctx, said)})
            total += left
            continue
        if isinstance(r, Stepped):
            count, per, notation = r.tariff.read(doc)
            if count < 2:
                raise ValueError(f'{key}: stepped() over a single price {notation!r}; use one()')
            whole = count * per
            said = f'The scheme prices this answer “{notation}”.'
            out.append({'id': rid, 'kind': 'criterion', 'verbatim': r.sel.text(doc), 'marks': whole,
                        'permittedMarks': list(range(0, whole + 1, per)),
                        'contextNote': _joined(ctx, said)})
            total += whole
            continue
        if isinstance(r, Menu):
            count, per, notation = r.tariff.read(doc)
            texts = [o.text(doc) for o in r.options]
            if len(texts) < count:
                raise ValueError(f'{key}: {notation!r} prices {count} answers over {len(texts)} printed')
            group = {'claimMax': count, 'perOption': per, 'options': texts}
            extra = []
            if r.alts:
                marks, of = [per] * len(texts), [None] * len(texts)
                for a in r.alts:
                    c, p, n = a.tariff.read(doc)
                    if c != 1 or p >= per:
                        raise ValueError(f'{key}: alternative priced {n!r} against {per}')
                    t = a.sel.text(doc)
                    group['options'].append(t)
                    marks.append(p)
                    of.append(a.of)
                    if a.of is None:
                        extra.append(f'The scheme prices “{t}” at {p} {_marks(p)}, as an answer of its own.')
                    else:
                        extra.append(f'The scheme allows “{t}” for {p} {_marks(p)}, in place of '
                                     f'“{texts[a.of]}”, never beside it.')
                group['optionMarks'], group['optionOf'] = marks, of
            joined = ' '.join(x for x in [ctx] + extra if x)
            out.append({'id': rid, 'kind': 'anyN', 'verbatim': 'The answers the scheme accepts in full',
                        'marks': None, **({'contextNote': joined} if joined else {}), 'group': group})
            total += count * per
            continue
        raise TypeError(f'{key}: unknown row {r!r}')
    return out, total
