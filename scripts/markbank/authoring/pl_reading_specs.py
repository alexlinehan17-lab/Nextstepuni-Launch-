#!/usr/bin/env python3
"""Reviewed specs for the Polish reading asks pl_all cannot read, one card each.

The rest of a sitting's reading cards come from pl_all.build(), which pairs the
paper's ask with the scheme's on their printed address. These are the asks it
refuses, read on the rendered page and set out by SELECTORS (pl_listen_lib):
every answer is a line of the scheme's .md cut at printed anchors, every price
the tariff the scheme prints for it, every question the census's reading of the
paper (plus, where the card needs them, the paper's own printed lines).

True/false verdicts are read from the TICK'S COLUMN on the rendered scheme page
(the .md keeps the tick and loses its column) and recorded with the page; the
verdict's word is cut from the table's own header row ("True False",
"Prawda Fałsz Marks").
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pl_paper                                                  # noqa: E402
from pl_listen import scheme_lines                               # noqa: E402
from pl_listen_lib import (S, J, T, TM, PL, W, one, menu, part, One, shown,  # noqa: E402,F401
                           graded, ladder, components)
from pl_listen_specs import build_rows, conflict                 # noqa: E402
from pl_topics import (topic_for, concept_for, answer_language,  # noqa: E402
                       language_note)
from pl_all import card_id, question_ref, source_material        # noqa: E402
from paper_census import key_label                              # noqa: E402

LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
# Section, question, letter, roman: 'A2ei'; the old papers' 'I4', 'II1', 'III2'.
KEY = re.compile(r'^(A|III|II|I)(\d{1,2})([a-l])?(i{1,3}|iv|vi{0,3})?$')


class R:
    """One reading card: the census address, its rows, notes for the student
    (`rownote`, a callable of the documents or a string) and the reviewer's
    evidence (`note`)."""
    def __init__(self, key, rows, total=None, note=None, rownote=None, question=None,
                 extra_pages=(), whole=False):
        self.key, self.rows, self.total, self.note = key, rows, total, note
        # The scheme prices the ask only as a whole (`questionTotal`): its rows
        # are shown, never claimed, and `total` is the printed price.
        self.whole = whole
        self.rownote, self.question = rownote, question
        # Paper pages the card needs beside its text's: a matching task's
        # pictures printed on a page of their own.
        self.extra_pages = extra_pages


class TextRemainder:
    """The price of a part the scheme prices nowhere but in its text's total:
    the "(50 marks)" printed on the text's head line, less the prices printed
    for the text's other parts (the bank's cards for them, each lifted from
    its printed tariff). One answer at that price."""
    def __init__(self, n_total, prefix, own_id):
        self.n_total, self.prefix, self.own_id = n_total, prefix, own_id

    def read(self, doc):
        import json
        line = doc['scheme'][self.n_total - 1]
        m = re.search(r'\(\s*(\d{1,3})\s*marks\s*\)', line)
        if not m:
            raise ValueError(f'scheme line {self.n_total} prints no text total: {line!r}')
        with open(os.path.join(HERE, '..', 'authored', 'polish.json'), encoding='utf-8') as fh:
            others = [c for c in json.load(fh)
                      if c['id'].startswith(self.prefix) and c['id'] != self.own_id]
        rest = int(m.group(1)) - sum(c['totalMarks'] for c in others)
        if not 0 < rest <= 10:
            raise ValueError(f'{self.own_id}: {m.group(0)} less the other parts leaves {rest}')
        return 1, rest, (f'{m.group(0)} for the text, less the {int(m.group(1)) - rest} '
                         f'printed for its other {len(others)} parts')


class OptionOnly:
    """A price printed as "(2 marks for one option only)", wrapped over two
    lines: one answer, from the printed alternatives, at that price."""
    def __init__(self, n):
        self.n = n

    def read(self, doc):
        line = doc['scheme'][self.n - 1].replace('\xa0', ' ')
        m = re.search(r'\(\s*(\d{1,2})\s*marks?\s+for\s+one\b', line)
        if not m:
            raise ValueError(f'scheme line {self.n} prints no "for one option" price: {line!r}')
        return 1, int(m.group(1)), m.group(0)


class Times:
    """A split printed without brackets inside a question's price line,
    "(d) 8 marks: (i) 3 x 2 marks, (ii) 2 marks": the k-th "N x P marks"."""
    def __init__(self, n, k=0):
        self.n, self.k = n, k

    def read(self, doc):
        line = doc['scheme'][self.n - 1].replace('\xa0', ' ')
        found = list(re.finditer(r'(\d{1,2})\s*[x×]\s*(\d{1,2})\s*marks?', line))
        if len(found) <= self.k:
            raise ValueError(f'scheme line {self.n} prints no "N x P marks" #{self.k}: {line!r}')
        m = found[self.k]
        return int(m.group(1)), int(m.group(2)), m.group(0)


class Rule:
    """A price the 2021 scheme prints in words or brackets, read by a pattern
    on scheme line n whose groups give (count, per): "Po 1 punkcie za podanie
    korzyści (3 pkt max)" is three answers at 1, "2 punkty za wytłumaczenie"
    one answer at 2, "(5)" one at 5, "CZĘŚĆ II (40/70)" one at 40."""
    def __init__(self, n, pattern, order=('count', 'per')):
        self.n, self.pattern, self.order = n, pattern, order

    def read(self, doc):
        line = re.sub(r'[\s\xa0]+', ' ', doc['scheme'][self.n - 1]).strip()
        m = re.search(self.pattern, line)
        if not m:
            raise ValueError(f'scheme line {self.n} does not print {self.pattern!r}: {line!r}')
        vals = dict(zip(self.order, (int(g) for g in m.groups())))
        return vals.get('count', 1), vals['per'], m.group(0)


def per_point_max(n):
    return Rule(n, r'Po (\d{1,2}) punkcie\b.*?\((\d{1,2}) (?:pkt|punkty) max\)', ('per', 'count'))


def points_for(n, what):
    return Rule(n, r'(\d{1,2}) punkty za ' + re.escape(what), ('per',))


def bracket(n):
    return Rule(n, r'\((\d{1,3})(?:/\d{1,3})?\)', ('per',))


class PaperPrice:
    """A part's price as the QUESTION PAPER prints it beside the part, "(1)"
    at the part's own line height (2013 Higher Q1, p3), where the scheme
    prints only the question's total. One answer at that price."""
    def __init__(self, page, y):
        self.page, self.y = page, y

    def read(self, doc):
        hits = [l.text for l in doc['lines'] if l.page == self.page and abs(l.y - self.y) < 2
                and re.fullmatch(r'\(\s*\d{1,2}\s*\)', l.text.strip())]
        if len(hits) != 1:
            raise ValueError(f'paper p{self.page} y{self.y}: {len(hits)} printed prices')
        return 1, int(re.search(r'\d{1,2}', hits[0]).group(0)), f'{hits[0]} (paper p{self.page})'


def columns(d, page, y0, y1, edges):
    """A printed table's columns between y0 and y1 on a paper page, each read
    top to bottom and left to right inside its own x-range: "Marta lubi: •
    modę oraz • utwory Stanisława Lema". `edges` are the column boundaries."""
    out = []
    for lo, hi in zip(edges, edges[1:]):
        cell = sorted((l for l in d['lines'] if l.page == page and y0 <= l.y <= y1 and lo <= l.x < hi),
                      key=lambda l: (round(l.y / 4), l.x))
        out.append(re.sub(r'\s+', ' ', ' '.join(l.text for l in cell)).strip())
    return out


def _remainder_line(rule, d):
    """The arithmetic, where the student sees it (row contextNote)."""
    _c, rest, notation = rule.read(d)
    total = int(re.search(r'\d{1,3}', notation).group(0))
    return (f'The scheme prints no mark for this part; {rest} marks is the {total} printed for '
            f'the text less the {total - rest} printed for its other parts.')


def lifted(*sels):
    """A note quoting printed lines, for the student."""
    return lambda d: ' '.join(f'The scheme notes: “{s.text(d)}”.' for s in sels)


SPECS = {}

# ================================================================ 2026 HL ===
SPECS[(2026, 'hl')] = [
    # True/false, priced (1+1 m) on the head row. Rendered scheme p6: the
    # tick for (i) stands in the False column, for (ii) in the True column.
    R('A1ji', [one(S(187, after='True '), T(183, each=True))],
      rownote=lifted(S(185, raw=True), S(186, raw=True)),
      note='The tick stands in the False column (scheme p6, rendered).'),
    R('A1jii', [one(S(187, before=' False'), T(183, each=True))],
      rownote=lifted(S(185, raw=True), S(186, raw=True)),
      note='The tick stands in the True column (scheme p6, rendered).'),
    # "- pastor metodystów (2 m)" or "- pastor (1 m)": the shorter answer in
    # place of the full one, never beside it.
    R('A2aii', [one(S(201), T(201), [part(S(203), 0, T(203))])]),
]

# ================================================================ 2026 OL ===
SPECS[(2026, 'ol')] = [
    # "Podkreśl zdanie prawdziwe": the scheme prints the true sentence, by its
    # printed number, and prices the ask (4 marks).
    R('A1c', [one(S(105), T(106))]),
    # Multiple choice A-D: the scheme answers "C (2 marks)". The paper prints
    # the four options in the question itself.
    R('A2biii', [one(S(162), T(162))]),
    # A matching task: names 2-6 to portraits A-F (1. Agatka is the example).
    # The scheme sets its key as a table, numbers over letters ("1. 2. 3. 4.
    # 5. 6." / "E C F A B D", cells read by find_tables in that order) and
    # "2 marks" under each answer; each row is one name's letter, led by the
    # name as the paper prints it (p11). The portraits are on paper p11.
    R('A2c', [one(W(166, k - 1), T(167, k - 2), lead=PL(11, f'{k}. ')) for k in range(2, 7)],
      question=lambda d, q: '\n'.join([q] + [PL(11, f'{k}. ').text(d) for k in range(2, 7)]),
      extra_pages=(11,)),
]

# ================================================================ 2025 HL ===
SPECS[(2025, 'hl')] = [
    R('A2aii', [one(S(191), T(191), [part(S(193), 0, T(193))])]),
    # True/false, priced (2 x 1 m). Rendered scheme p7: (i) False, (ii) True.
    R('A2hi', [one(S(255, after='True '), T(251, each=True))],
      rownote=lifted(S(253, raw=True), S(254, raw=True)),
      note='The tick stands in the False column (scheme p7, rendered).'),
    R('A2hii', [one(S(255, before=' False'), T(251, each=True))],
      rownote=lifted(S(253, raw=True), S(254, raw=True)),
      note='The tick stands in the True column (scheme p7, rendered).'),
]

# ================================================================ 2025 OL ===
SPECS[(2025, 'ol')] = [
    # "Tick the three correct answers from the six boxes below": one card for
    # the printed question (CARD-STANDARD 10c), the scheme's three ticked boxes
    # as its rows at their printed 2 marks each. The six boxes are printed on
    # pages 5 and 6; each row names its box as the paper prints it.
    R('A1d', [one(S(113), T(113), lead=PL(5, 'A. ')),
              one(S(114), T(114), lead=PL(5, 'C. ')),
              one(S(115), T(115), lead=PL(6, 'F. '))],
      question=lambda d, q: '\n'.join(
          [re.sub(r'\s*✓\s*$', '', q)]
          + [PL(p, f'{x}. ').text(d) for p, x in ((5, 'A'), (5, 'B'), (5, 'C'),
                                                  (6, 'D'), (6, 'E'), (6, 'F'))])),
    # The answer is printed on the question's own row, before its price.
    R('A2bi', [one(S(148, after='ZHP? '), T(148))]),
    R('A2bii', [one(S(149, after='ZHP? '), T(149))]),
    # Rendered scheme p6: the (vi) tick stands in the Prawda column (x=406
    # under "Prawda" at x=392; "Fałsz" is at x=446). Priced in the Marks column.
    R('A2cvi', [one(S(152, before=' Fałsz'), TM(160))],
      note='The tick stands in the Prawda column (scheme p6, rendered).'),
]


# ======================================================= the old exam, shared ===
class EachOf:
    """A part priced "(5)" with "1 pkt za każdy przykład": as many answers as
    the total allows, at the per-answer price."""
    def __init__(self, total, per):
        self.total, self.per = total, per

    def read(self, doc):
        _c, whole, wn = self.total.read(doc)
        _c2, per, pn = self.per.read(doc)
        if whole % per:
            raise ValueError(f'{wn} is not a whole number of {pn}')
        return whole // per, per, f'{wn}, {pn}'


def part_pkt(n, letter):
    """'a) 2 pkt' / '- b) 3 pkt' on scheme line n: one answer at that price."""
    return Rule(n, rf'{letter}\) (\d{{1,2}}) pkt', ('per',))


def pkt_line(n):
    """A line that is only a price, "3 pkt"."""
    return Rule(n, r'^-?\s*(\d{1,2}) pkt$', ('per',))


def examples(head_line, *sels):
    """The criteria rule and a task's points, quoted on the first row."""
    return lambda d: (f'The scheme prints, for Części II and III: “{S(head_line).text(d)}” Its points '
                      f'for this task, as examples, not a checklist: '
                      + '; '.join(f'“{x.text(d)}”' for x in sels) + '.')


def essay_question(page):
    def build(d, q):
        title = re.sub(r'^\d\.\s*', '', q)
        return f'{PL(page, "Napisz wypracowanie").text(d)} {title}'
    return build


def _j(*ranges):
    return [J(*[S(n) for n in rng]) for rng in ranges]


def _p(*ranges):
    """Paragraphs as printed, each a run of wrapped lines."""
    return [shown(J(*[S(n) for n in rng])) for rng in ranges]


def _refl(n):
    return lambda d: f'Under the scheme\'s heading “{S(n).text(d)}”: examples, not a checklist.'


def criteria(l1, p1, l2, p2, l3, p3, l4):
    """The four printed criteria (each a line or two, the line printing its
    percentage last)."""
    return [(J(*[S(n) for n in range(l1, p1 + 1)]), p1), (J(*[S(n) for n in range(l2, p2 + 1)]), p2),
            (J(*[S(n) for n in range(l3, p3 + 1)]), p3), (S(l4), l4)]


# ================================================================ 2010 HL ===
# Q5 prints its whole scale, "(5 pkt za trzy powody, 4 pkt za dwa, 3 pkt za
# jeden )": a ladder of 3, then 1, then 1, read from those printed totals. Q3
# prints "(5 pkt za trzy przykłady, 4 pkt za dwa, itd.)", which leaves the
# one-example price unprinted: a whole-question card that quotes the rule.
CRITERIA_2010 = criteria(141, 142, 143, 144, 145, 146, 147)


class Step:
    """The difference between two printed totals of one scale: "4 pkt za dwa"
    less "3 pkt za jeden" is what the second answer adds."""
    def __init__(self, higher, lower):
        self.higher, self.lower = higher, lower

    def read(self, doc):
        _a, hi, hn = self.higher.read(doc)
        _b, lo, ln = self.lower.read(doc)
        return 1, hi - lo, f'{hn} less {ln}'


def _rules_2010(*sels):
    def note(d):
        head = J(S(139), S(140)).text(d)
        tail = (' Its model for this task, as an example, not a checklist: '
                + ' '.join(f'“{x.text(d)}”' for x in sels) + '.') if sels else ''
        return f'The scheme prints, for Części II and III: “{head}”{tail}'
    return note


SPECS[(2010, 'hl')] = [
    R('I1a', [shown(S(22)), shown(J(S(23), S(24), S(25)))], total=bracket(21), whole=True),
    R('I1b', [shown(J(S(27), S(28), S(29), S(30)))], total=bracket(26), whole=True),
    R('I2', [shown(J(*[S(n) for n in range(34, 43)]))], total=bracket(33), whole=True),
    R('I3', [shown(x) for x in _j([47], [48], range(53, 55), range(55, 57), [57], range(58, 60))],
      total=bracket(45), whole=True, rownote=lifted(S(46))),
    R('I4', [shown(J(*[S(n) for n in range(62, 71)])), shown(J(*[S(n) for n in range(72, 78)]))],
      total=bracket(61), whole=True,
      rownote=lambda d: f'The scheme prints two answers, either one, joined by “{S(71).text(d)}”.'),
    R('I5', [ladder([S(n) for n in range(86, 93)],
                    Rule(82, r'(\d) pkt za jeden', ('per',)),
                    Step(Rule(82, r'(\d) pkt za dwa', ('per',)), Rule(82, r'(\d) pkt za jeden', ('per',))),
                    Rule(82, r'(\d) pkt za trzy', ('per',)))],
      rownote=lambda d: (f'The scheme pays by how many reasons are given, in its own words: '
                         f'“{S(82).text(d)}”. Its lead-in: “{J(S(83), S(84), S(85)).text(d)}”')),
    R('I6', [shown(x) for x in _j(range(102, 105), range(105, 109), range(109, 111), range(111, 114))],
      total=bracket(101), whole=True),
    R('II1', [graded(S(115), bracket(114), CRITERIA_2010)],
      rownote=_rules_2010(J(*[S(n) for n in range(120, 125)]), J(S(125), S(126), S(127)))),
    R('III1', [graded(J(S(133), S(134)), bracket(132), CRITERIA_2010)], rownote=_rules_2010(),
      question=essay_question(4)),
    R('III2', [graded(J(S(133), S(134)), bracket(132), CRITERIA_2010)], rownote=_rules_2010(),
      question=essay_question(4)),
]


# ================================================================ 2011 HL ===
# Q5 prices its two components in words, "3 pkt tylko za akapit 3" and "2 pkt
# tylko za akapit 4": each answer is a row at its printed price. The criteria
# block stands at the end (p5), headed over two lines.
CRITERIA_2011 = criteria(131, 132, 133, 134, 135, 136, 137)


def _rules_2011(*sels):
    def note(d):
        head = J(S(129), S(130)).text(d)
        tail = (' Its points for this task, as examples, not a checklist: '
                + '; '.join(f'“{x.text(d)}”' for x in sels) + '.') if sels else ''
        return f'The scheme prints, for Części II and III: “{head}”{tail}'
    return note


def _essay_2011(d, q):
    title = re.sub(r'^\d\.\s*', '', q)
    return f'{PL(4, "Używając około 300").text(d)} {title}'


SPECS[(2011, 'hl')] = [
    R('I1a', [one(J(S(25), S(26)), bracket(23))], rownote=lifted(S(24))),
    R('I1b', [one(S(28), bracket(27))], rownote=lifted(S(29))),
    R('I1c', [one(S(31), bracket(30))]),
    R('I1d', [one(S(33), bracket(32))]),
    R('I1e', [one(S(35), bracket(34))]),
    R('I2', [shown(J(S(39), S(40), S(41), S(42)))], total=bracket(38), whole=True),
    R('I3', [shown(x) for x in _j(range(49, 51), range(51, 53), [53])], total=bracket(48), whole=True),
    R('I4', [shown(x) for x in _j([56], [57], [58], range(59, 61), [61])], total=bracket(55), whole=True),
    R('I5', [one(J(*[S(n) for n in range(64, 71)], S(71, before=' 3 pkt')),
                 Rule(71, r'(\d) pkt tylko za akapit 3', ('per',))),
             one(J(S(72), S(73), S(74, before=' 2 pkt')),
                 Rule(74, r'(\d) pkt tylko za akapit 4', ('per',)))],
      total=bracket(63)),
    R('I6', [shown(x) for x in _j(range(79, 81), range(85, 87), range(87, 89), range(89, 91),
                                  range(91, 94), range(94, 96))], total=bracket(78), whole=True),
    R('II1', [graded(S(97), bracket(96), CRITERIA_2011)],
      rownote=_rules_2011(*_j([102], [103], [104], [105], range(106, 108), range(108, 110)))),
    R('III1', [graded(J(S(111), S(112)), bracket(110), CRITERIA_2011)],
      rownote=_rules_2011(*_j(range(115, 117), [117], range(122, 124), [124])), question=_essay_2011),
    R('III2', [graded(J(S(111), S(112)), bracket(110), CRITERIA_2011)],
      rownote=_rules_2011(), question=_essay_2011),
]


# ================================================================ 2012 HL ===
# Q1 prints "(1)" for each word and its accepted synonyms as a dash list: any
# one of them. The criteria block stands at the END of this scheme (p7).
CRITERIA_2012 = criteria(171, 172, 173, 174, 175, 176, 177)


def _q2012_1(d, q):
    instr = re.sub(r'^1\.\s*', '', PL(3, '1. Zastąp').text(d))
    return q if q.startswith(instr[:20]) else f'{instr} {q}'


def _q2012_4b(d, q):
    quote = re.sub(r'^4\.\s*', '', PL(4, '4. „Z gąszczu').text(d))
    return f'{quote} {q}'


def _essay_2012(d, q):
    title = re.sub(r'(?<=[a-z])\d$', '', re.sub(r'^\d\.\s*', '', q))   # the footnote mark
    return f'{PL(4, "Napisz wypracowanie").text(d)} {title}'


SPECS[(2012, 'hl')] = [
    *[R(f'I1{x}', [menu([S(n) for n in opts], bracket(price))], question=_q2012_1)
      for x, opts, price in (('a', (27, 28), 26), ('b', (31, 32, 33), 30), ('c', (36, 37), 35),
                             ('d', (39, 40), 38), ('e', (42, 43), 41))],
    R('I2', [shown(x) for x in _j(range(50, 52), range(52, 54), range(54, 56))],
      total=bracket(49), whole=True),
    R('I3', [shown(x) for x in _j(range(57, 59), range(59, 61))], total=bracket(56), whole=True),
    R('I4a', [shown(J(S(63), S(64)))], total=bracket(62), whole=True),
    R('I4b', [shown(J(S(66), S(67), S(68), S(69)))], total=bracket(65), whole=True, question=_q2012_4b),
    R('I5', [shown(x) for x in _j(range(72, 75), range(75, 77))], total=bracket(71), whole=True),
    R('I6', [shown(x) for x in _j(range(87, 90), range(90, 93), range(93, 96), range(96, 98),
                                  range(98, 101), range(101, 104))], total=bracket(86), whole=True),
    R('II1', [graded(S(105), bracket(104), CRITERIA_2012)],
      rownote=examples(170, *_j([110], (111, 112, 113, 118, 119), [120], [121], range(122, 126),
                                range(126, 130)))),
    R('III1', [graded(J(S(131), S(132)), bracket(130), CRITERIA_2012)],
      rownote=examples(170, *_j([136], range(137, 140), range(140, 142), [142], range(143, 145),
                                [145], [146])),
      question=_essay_2012),
    R('III2', [graded(J(S(131), S(132)), bracket(130), CRITERIA_2012)],
      rownote=examples(170, *_j(range(156, 158), range(158, 160), [160], [161], [162], [163], [164],
                                [165], [166], range(167, 169))),
      question=_essay_2012),
]


# ================================================================ 2013 HL ===
# The scheme prices Q1 only as "(5)"; the PAPER prints "(1)" beside each of
# its five words (p3), and that printed price is each part's. Q3 and Q5 print
# their parts' shares, "(3)" and "(2)", on both documents.
CRITERIA_2013 = criteria(50, 50, 51, 52, 53, 54, 55)


def _q2013_3b(d, q):
    quote = (re.sub(r'^3\.\s*', '', PL(4, '3. „').text(d)) + ' '
             + PL(4, '[…] coś, do czego').text(d))
    return f'{quote} {q}'


def _q2013_5a(d, q):
    quote = (re.sub(r'^5\.\s*', '', PL(4, '5. „Być').text(d)) + ' '
             + PL(4, '– marzący').text(d))
    return f'{quote} {q}'


SPECS[(2013, 'hl')] = [
    *[R(f'I1{x}', [one(S(n), PaperPrice(3, y))])
      for x, n, y in zip('abcde', (60, 62, 64, 66, 68), (590, 606, 622, 638, 654))],
    R('I2', [shown(x) for x in _j(range(72, 75), range(75, 77), range(81, 85))],
      total=bracket(71), whole=True),
    R('I3a', [shown(x) for x in _j([92], range(93, 95), range(95, 99))], total=bracket(88), whole=True),
    R('I3b', [shown(x) for x in _j(range(101, 103), range(103, 106))], total=bracket(90), whole=True,
      question=_q2013_3b),
    R('I4', [shown(x) for x in _j(range(110, 114), range(118, 121))], total=bracket(109), whole=True),
    R('I5a', [shown(x) for x in _j(range(128, 131), range(131, 134), [134])], total=bracket(125),
      whole=True, question=_q2013_5a),
    R('I5b', [shown(x) for x in _j(range(137, 139), [139], range(140, 142), range(142, 144),
                                   range(144, 146))], total=bracket(126), whole=True),
    R('I6', [shown(x) for x in _j(range(155, 157), range(157, 160), range(160, 162), range(162, 165),
                                  range(165, 170))], total=bracket(149), whole=True),
    R('II1', [graded(S(172), bracket(171), CRITERIA_2013)],
      rownote=examples(49, *_j(range(175, 178), range(178, 180), range(180, 183), range(183, 187),
                               range(187, 190), range(194, 196), range(196, 198)))),
    R('III1', [graded(J(S(200), S(201)), bracket(199), CRITERIA_2013)],
      rownote=examples(49, *_j([206], [207], [208], [209], range(210, 212), [212])),
      question=essay_question(4)),
    R('III2', [graded(J(S(200), S(201)), bracket(199), CRITERIA_2013)],
      rownote=examples(49, *_j([217], [218], [219], [220], [221], [222], [223], [224])),
      question=essay_question(4)),
]


# ================================================================ 2014 HL ===
# 2014 prints its prices as words in brackets under each question: ladders
# ("(3 pkt za jedno wyjaśnienie i 2 pkt za drugie)" across Q1's two parts, so
# Q1 is one card for the printed question, as the ordering tasks are), a
# split by component (Q4), and a split by part (Q5).
CRITERIA_2014 = criteria(49, 49, 50, 51, 52, 53, 54)


def _q2014_1(d, q):
    head = re.sub(r'^1\.\s*', '', PL(3, '1. Wyjaśnij').text(d))
    return '\n'.join([head, f'{PL(3, "a)").text(d)} {PL(3, "„być").text(d)}',
                       f'{PL(3, "b)").text(d)} {PL(3, "„wlec").text(d)}'])


def _q2014_5(d, q):
    return (re.sub(r'^5\.\s*', '', PL(4, '5. „Czas').text(d)) + ' '
            + PL(4, 'należy rozumieć').text(d))


def _ladder_note(n, steps):
    return lambda d: (f'The scheme pays a descending ladder here, in its own words: '
                      f'“{S(n).text(d)}” — {steps} marks, in that order, to a printed total of 5.')


SPECS[(2014, 'hl')] = [
    R('I1', [ladder([S(60), J(S(62), S(63))],
                    Rule(58, r'\((\d) pkt za jedno', ('per',)), Rule(58, r'i (\d) pkt za drugie', ('per',)),
                    bracket(57))],
      question=_q2014_1, rownote=_ladder_note(58, '3, 2')),
    R('I2', [ladder([S(67), J(S(68), S(69)), S(70)],
                    Rule(66, r'\((\d) pkt za jeden', ('per',)),
                    Rule(66, r'i (\d) pkt za każdy kolejny', ('per',)), bracket(65))],
      rownote=_ladder_note(66, '3, 1, 1')),
    R('I3', [ladder([J(S(79), S(80)), J(S(81), S(82), S(83))],
                    Rule(74, r'\((\d) pkt za pierwszy', ('per',)), Rule(74, r'i (\d) pkt za drugi', ('per',)),
                    bracket(73))],
      rownote=_ladder_note(74, '3, 2')),
    # Priced by component: the explanation 3, the student's own comment 2.
    # The scheme's points for each are quoted on the row as examples.
    R('I4', [components(S(88), [(S(88, after='pkt za ', before=' i 2'),
                                 Rule(88, r'\((\d) pkt za wyjaśnienie', ('per',))),
                                (S(88, after='2 pkt za ', before=')'),
                                 Rule(88, r'i (\d) pkt za własny', ('per',)))])],
      total=bracket(87),
      rownote=lambda d: ('Examples the scheme prints, not a checklist: '
                         + '; '.join(f'“{x.text(d)}”' for x in
                                     [J(S(89), S(90)), S(91), S(92), J(S(93), S(94)), J(S(95), S(96)),
                                      J(S(98), S(99), S(100)), J(S(102), S(103), S(104))]) + '.')),
    R('I5a', [shown(S(n)) for n in (110, 111, 112, 113)],
      total=Rule(108, r'\((\d) pkt za sens dosłowny', ('per',)), whole=True, question=_q2014_5),
    R('I5b', [shown(S(n)) for n in (116, 117, 122, 123)],
      total=Rule(108, r'i (\d) pkt za sens przenośny', ('per',)), whole=True, question=_q2014_5),
    R('I6', [shown(x) for x in _j(range(128, 130), range(130, 133), range(133, 135), range(136, 138),
                                  range(138, 140), [140])],
      total=bracket(127), whole=True),
    R('II1', [graded(S(143), bracket(142), CRITERIA_2014)],
      rownote=examples(48, *_j(range(149, 152), range(152, 155), range(155, 160), range(164, 167),
                               range(167, 169), range(170, 172), [172], [173], [174], [175]))),
    R('III1', [graded(J(S(178), S(179)), bracket(177), CRITERIA_2014)],
      rownote=examples(48, *_j([184], [185], [186], [187], [188], [189], [190], [191])),
      question=essay_question(4)),
    R('III2', [graded(J(S(178), S(179)), bracket(177), CRITERIA_2014)],
      rownote=examples(48, *_j([197], range(198, 200), [200], [201])),
      question=essay_question(4)),
]


# ================================================================ 2015 HL ===
# Read against the repaired scheme (464645160: its text layer had reported
# the Polish letters as other code points). Q3 prices its parts in words,
# "2 pkt za część (a) i 3 pkt za część (b)", and prints no split inside
# either: each part is a whole-question card at its printed share.
CRITERIA_2015 = criteria(51, 52, 53, 54, 55, 56, 57)


def _q2015_3(d, q):
    lead = re.sub(r'^3\.\s*', '', PL(4, '3. Odwołując').text(d))
    return f'{lead} {q}'


def _heading(n):
    return lambda d: f'Under the scheme\'s heading “{S(n).text(d)}”: examples, not a checklist.'


SPECS[(2015, 'hl')] = [
    R('I1', [menu([S(n) for n in range(63, 68)],
                  EachOf(bracket(61), Rule(62, r'(\d) pkt za każde', ('per',))))],
      rownote=lambda d: f'The scheme ends its list “{S(68).text(d)}”.'),
    R('I2', [ladder([S(72), S(73), S(74)],
                    Rule(71, r'^(\d) pkt za jeden', ('per',)),
                    Rule(71, r'i (\d) pkt za każdy kolejny', ('per',)), bracket(70))],
      rownote=lambda d: (f'The scheme pays a descending ladder here, in its own words: '
                         f'“{S(71).text(d)}” — 3, 1, 1 marks, in that order, to a printed total of 5.')),
    R('I3a', [shown(S(87)), shown(S(88))],
      total=Rule(85, r'(\d) pkt za część \(a\)', ('per',)), whole=True, question=_q2015_3),
    R('I3b', [shown(J(S(91), S(92))), shown(S(93))],
      total=Rule(85, r'(\d) pkt za część \(b\)', ('per',)), whole=True, question=_q2015_3),
    R('I4', [shown(x) for x in _j(range(102, 105), [105], range(106, 109), range(109, 111), [111])],
      total=bracket(100), whole=True, rownote=_heading(101)),
    R('I5', [shown(S(n)) for n in (117, 118, 119, 120, 121, 122, 123, 128, 129)],
      total=bracket(115), whole=True, rownote=_heading(116)),
    R('I6', [shown(x) for x in _j([136], [137], range(138, 140), range(140, 142), range(142, 144),
                                  range(144, 146))],
      total=bracket(134), whole=True, rownote=_heading(135)),
    R('II1', [graded(S(148), bracket(147), CRITERIA_2015)],
      rownote=examples(50, *_j(range(153, 155), range(155, 157), range(157, 160), [160]))),
    R('III1', [graded(J(S(167), S(168)), bracket(166), CRITERIA_2015)],
      rownote=examples(50, *_j([172], [173], [174], [175], [176], range(177, 179))),
      question=essay_question(4)),
    R('III2', [graded(J(S(167), S(168)), bracket(166), CRITERIA_2015)],
      rownote=examples(50, *_j([183], [184], [185], [186], [187], [188], [189])),
      question=essay_question(4)),
]


# ================================================================ 2016 HL ===
CRITERIA_2016 = criteria(49, 50, 51, 52, 53, 54, 55)


SPECS[(2016, 'hl')] = [
    *[R(f'I1{x}', [one(sel, Rule(64, r'(\d) pkt za każde', ('per',)))])
      for x, sel in zip('abcde', [S(65, after='a) '), S(66, after='b) '), S(67, after='c) '),
                                  S(68, after='d) '), J(S(69, after='e) '), S(70))])],
    R('I2', [ladder(_j(range(78, 80), [80], range(81, 83), range(83, 85), range(85, 87), range(87, 89)),
                    Rule(73, r'^(\d) pkt za jeden', ('per',)),
                    Rule(73, r'i (\d) pkt za każdy kolejny', ('per',)), bracket(72))],
      rownote=lambda d: (f'The scheme pays a descending ladder here, in its own words: '
                         f'“{S(73).text(d)}” — 3, 1, 1 marks, in that order, to a printed total of 5.')),
    # A model reading, then one example for each stance, each under the
    # scheme's own heading ("ZGADZAM SIĘ:" / "NIE ZGADZAM SIĘ:").
    R('I3', [shown(x) for x in _j(range(93, 100), range(101, 106), range(107, 112))],
      total=bracket(92), whole=True),
    R('I4', [shown(x) for x in _j(range(120, 123), range(123, 125), range(125, 127))],
      total=bracket(114), whole=True, rownote=_refl(119)),
    R('I5', [shown(x) for x in _j(range(133, 135), range(135, 138), range(139, 142), range(142, 144),
                                  range(145, 147), range(147, 149), range(149, 151))],
      total=bracket(131), whole=True, rownote=_refl(132)),
    R('I6', [shown(x) for x in _j(range(161, 165), range(165, 168), range(169, 172), range(173, 177))],
      total=bracket(155), whole=True, rownote=_refl(160)),
    R('II1', [graded(S(179), bracket(178), CRITERIA_2016)],
      rownote=examples(48, *_j(range(185, 188), range(188, 190), range(190, 193), range(193, 195)))),
    R('III1', [graded(J(S(201), S(202)), bracket(200), CRITERIA_2016)],
      rownote=examples(48, *_j([207], range(208, 210), range(210, 212), range(212, 214), range(214, 216),
                               [216], [217], [218])),
      question=essay_question(4)),
    R('III2', [graded(J(S(201), S(202)), bracket(200), CRITERIA_2016)],
      rownote=examples(48, *_j(range(225, 227), range(227, 229), [229], range(230, 232), range(232, 234),
                               range(234, 236), [236], [237])),
      question=essay_question(4)),
]


# ================================================================ 2017 HL ===
CRITERIA_2017 = criteria(49, 50, 51, 52, 53, 54, 55)


def _instr_2017(d, q):
    # (a)-(d) are read without the instruction printed once over all five.
    instr = re.sub(r'^1\.\s*', '', PL(4, '1. Wyjaśnij').text(d))
    return q if q.startswith(instr[:30]) else f'{instr} {q}'


SPECS[(2017, 'hl')] = [
    *[R(f'I1{x}', [one(sel, Rule(67, r'(\d) pkt za każde', ('per',)))], question=_instr_2017)
      for x, sel in zip('abcde', [S(68, after='a) '), J(S(69, after='b) '), S(70)), S(71, after='c) '),
                                  J(S(72, after='d) '), S(73)), S(74, after='e) ')])],
    R('I2', _p(range(81, 83), range(83, 85), range(85, 87), range(87, 90)),
      total=bracket(76), whole=True),
    R('I3', [ladder([J(S(95), S(96)), J(S(97), S(98)), J(S(99), S(100)), J(S(101), S(102))],
                    Rule(93, r'^(\d) pkt za jedną', ('per',)),
                    Rule(93, r'i (\d) pkt za każdą kolejną', ('per',)), bracket(92))],
      rownote=lambda d: (f'The scheme pays a descending ladder here, in its own words: '
                         f'“{S(93).text(d)}” — 3, 1, 1 marks, in that order, to a printed total of 5.')),
    R('I4', _p(range(106, 110), range(110, 114), range(114, 116)), total=bracket(105), whole=True),
    R('I5', _p(range(124, 126), range(126, 129), range(129, 133)), total=bracket(122), whole=True,
      rownote=_refl(123)),
    R('I6', _p(range(137, 141), range(141, 144), range(144, 147), range(147, 151)),
      total=bracket(135), whole=True, rownote=_refl(136)),
    R('II1', [graded(S(153), bracket(152), CRITERIA_2017)],
      rownote=examples(48, *[J(*[S(n) for n in rng]) for rng in
                             (range(164, 166), range(166, 169), range(169, 171), range(171, 175))])),
    R('III1', [graded(J(S(177), S(178)), bracket(176), CRITERIA_2017)],
      rownote=examples(48, *[J(*[S(n) for n in rng]) for rng in
                             (range(182, 191), (191, 192, 197, 198, 199), range(200, 202),
                              range(202, 207), range(207, 210))]),
      question=essay_question(4)),
    R('III2', [graded(J(S(177), S(178)), bracket(176), CRITERIA_2017)],
      rownote=examples(48, *[J(*[S(n) for n in rng]) for rng in
                             (range(216, 220), range(220, 222), range(222, 226), range(226, 229),
                              range(229, 233))]),
      question=essay_question(4)),
]


# ================================================================ 2018 HL ===
CRITERIA_2018 = criteria(51, 52, 53, 54, 55, 56, 57)


def _rule_note(n):
    return lambda d: f'The scheme notes: “{S(n).text(d)}”, over the model points below.'


SPECS[(2018, 'hl')] = [
    *[R(f'I1{x}', [one(sel, Rule(67, r'(\d) pkt za każde', ('per',)))])
      for x, sel in zip('abcde', [S(68, after='a) '), S(69, after='b) '), S(70, after='c) '),
                                  J(S(71, after='d) '), S(72)), J(S(73, after='e) '), S(74))])],
    R('I2', [menu([S(n) for n in range(82, 87)],
                  EachOf(bracket(76), Rule(81, r'(\d) pkt za każdy', ('per',))))]),
    # "1 pkt za każdy element" over three printed paragraphs that each hold
    # several elements, never listed one by one: the question's "(5)" is the
    # price, the paragraphs are shown and the rule is quoted.
    R('I3', [shown(J(S(91), S(92), S(93), S(94))), shown(J(S(95), S(96))),
             shown(J(S(97), S(98), S(99), S(100)))],
      total=bracket(89), whole=True, rownote=_rule_note(90)),
    R('I4', [shown(J(S(105), S(106), S(107))), shown(S(108)), shown(S(109)), shown(S(110))],
      total=bracket(104), whole=True),
    R('I5', [shown(J(S(121), S(122), S(123), S(124))), shown(J(S(125), S(126), S(127), S(128))),
             shown(J(S(129), S(130), S(131), S(132)))],
      total=bracket(115), whole=True,
      rownote=lambda d: f'Under the scheme\'s heading “{S(120).text(d)}”: examples, not a checklist.'),
    R('I6', [shown(J(S(137), S(138))), shown(J(S(139), S(140))), shown(J(S(141), S(142))),
             shown(J(S(143), S(144), S(145), S(146), S(147)))],
      total=bracket(135), whole=True,
      rownote=lambda d: f'Under the scheme\'s heading “{S(136).text(d)}”: examples, not a checklist.'),
    R('II1', [graded(S(154), bracket(153), CRITERIA_2018)],
      rownote=examples(50, S(161), S(162), S(163), S(165), J(S(166), S(167), S(168)))),
    R('III1', [graded(J(S(171), S(172)), bracket(170), CRITERIA_2018)],
      rownote=examples(50, J(S(176), S(177), S(178)), J(S(179), S(180), S(181)), S(182),
                       J(S(187), S(188)), J(S(189), S(190)), J(S(191), S(192), S(193), S(194)),
                       J(S(195), S(196))),
      question=essay_question(4)),
    R('III2', [graded(J(S(171), S(172)), bracket(170), CRITERIA_2018)],
      rownote=examples(50, S(202), J(S(203), S(204)), S(205), S(206), J(S(207), S(208)), S(209),
                       S(211), S(212), S(213), S(214)),
      question=essay_question(4)),
]


# ================================================================ 2019 HL ===
CRITERIA_2019 = criteria(51, 52, 53, 54, 55, 56, 57)


def _q2019_3(d, q):
    return (re.sub(r'^3\.\s*', '', PL(4, '3. W świetle').text(d)) + ' '
            + PL(4, 'dr. Dalewskiego z Politechniki').text(d))


SPECS[(2019, 'hl')] = [
    *[R(f'I1{x}', [one(S(n, after=f'{x}) '), Rule(66, r'(\d) pkt za każde', ('per',)))])
      for x, n in zip('abcde', range(67, 72))],
    R('I2', [menu([S(77), S(78), S(79), S(84), S(85)],
                  EachOf(bracket(73), Rule(74, r'(\d) pkt za każdy', ('per',))))],
      rownote=lifted(S(75), S(76))),
    R('I3a', [shown(J(S(90), S(91), S(92)))], total=part_pkt(89, 'a'), whole=True, question=_q2019_3),
    R('I3b', [shown(J(S(94), S(95), S(96), S(97)))], total=part_pkt(93, 'b'), whole=True,
      question=_q2019_3),
    # "3 pkt" and "2 pkt" over two printed points: each point carries its price.
    R('I4', [one(J(S(102), S(103), S(104)), pkt_line(101)), one(J(S(106), S(107)), pkt_line(105))],
      total=bracket(100)),
    R('I5a', [shown(J(S(114), S(115))), shown(J(S(116), S(117))), shown(S(118)),
              shown(J(S(119), S(120), S(121))), shown(J(S(126), S(127), S(128)))],
      total=part_pkt(113, 'a'), whole=True),
    R('I5b', [shown(J(S(131), S(132)))], total=part_pkt(130, 'b'), whole=True),
    R('I6a', [shown(J(S(138), S(139), S(140))), shown(J(S(141), S(142))), shown(J(S(143), S(144)))],
      total=part_pkt(137, 'a'), whole=True),
    R('I6b', [shown(J(S(147), S(148)))], total=part_pkt(145, 'b'), whole=True,
      rownote=lambda d: f'Under the scheme\'s heading “{S(146).text(d)}”: an example, not a checklist.'),
    R('II1', [graded(S(151), bracket(150), CRITERIA_2019)],
      rownote=examples(50, J(S(157), S(158), S(159)), J(S(164), S(165), S(166)),
                       J(S(167), S(168), S(169)), J(S(170), S(171)))),
    R('III1', [graded(J(S(174), S(175)), bracket(173), CRITERIA_2019)],
      rownote=examples(50, J(S(180), S(181)), J(S(182), S(183), S(184), S(185)),
                       J(S(186), S(187), S(188), S(189)), J(S(190), S(191)), J(S(192), S(193))),
      question=essay_question(4)),
    R('III2', [graded(J(S(174), S(175)), bracket(173), CRITERIA_2019)],
      rownote=examples(50, J(S(203), S(204)), *[S(n) for n in range(205, 211)],
                       J(S(212), S(213)), *[S(n) for n in range(214, 218)]),
      question=essay_question(4)),
]


# ================================================================ 2020 HL ===
# The old examination (Część I: a text and six questions, 30; Część II: ~100
# words, 30; Część III: an essay, 40). The scheme prices Q1 a point a word and
# Q2-Q6 only as a whole "(5)" over model points; Części II and III on four
# printed percentage criteria (30/30/30/10%), which give whole marks of 30
# and of 40 (CARD-STANDARD 10b). The paper carries a second, hidden text layer
# that repeats and reorders Q4-Q6; their questions are its visible lines, as
# the rendered p4 sets them.
CRITERIA_2020 = [(J(S(51), S(52)), 52), (J(S(53), S(54)), 54), (J(S(55), S(56)), 56), (S(57), 57)]


def _examples(*sels):
    return lambda d: (f'The scheme prints, for Części II and III: “{S(50).text(d)}” Its points for '
                      f'this task, as examples, not a checklist: '
                      + '; '.join(f'“{x.text(d)}”' for x in sels) + '.')


def _essay_2020(d, q):
    title = re.sub(r'^\d\.\s*', '', q)
    return f'{PL(4, "Napisz wypracowanie").text(d)} {PL(4, "300 słów:").text(d)} {title}'


SPECS[(2020, 'hl')] = [
    *[R(f'I1{x}', [one(S(n, after=f'{x}) '), Rule(67, r'(\d) pkt za każde', ('per',)))])
      for x, n in zip('abcde', range(68, 73))],
    R('I2', [shown(S(80)), shown(S(81)), shown(S(82))], total=bracket(79), whole=True),
    R('I3', [shown(J(S(85), S(86), S(87))), shown(S(88))], total=bracket(84), whole=True),
    R('I4', [shown(J(S(91), S(92))), shown(J(S(93), S(94))), shown(S(95)), shown(S(96))],
      total=bracket(90), whole=True,
      question=lambda d, q: (re.sub(r'^4\.\s*', '', PL(4, '4. Dlaczego').text(d))
                             .replace(' (akapit 3) ', ' ') + ' (akapit 3)')),
    R('I5', [shown(J(S(99), S(100))), shown(J(S(101), S(102)))], total=bracket(98), whole=True,
      question=lambda d, q: re.sub(r'^5\.\s*', '', PL(4, '5. Dlaczego').text(d))),
    R('I6', [shown(S(105)), shown(J(S(106), S(107))), shown(S(108)), shown(J(S(109), S(110))),
             shown(S(111)), shown(S(112)), shown(S(113))], total=bracket(104), whole=True,
      question=lambda d, q: f'{PL(4, "Jaką cenę").text(d)} {PL(4, "społeczeństwa?").text(d)}'),
    R('II1', [graded(S(119), bracket(118), CRITERIA_2020)],
      rownote=_examples(*[S(n) for n in range(122, 126)])),
    R('III1', [graded(J(S(127), S(128)), bracket(126), CRITERIA_2020)],
      rownote=_examples(S(132), J(S(133), S(134)), S(135), S(136), J(S(137), S(138))),
      question=_essay_2020),
    R('III2', [graded(J(S(127), S(128)), bracket(126), CRITERIA_2020)],
      rownote=_examples(S(140), J(S(141), S(142))),
      question=_essay_2020),
]


# ================================================================ 2021 HL ===
# The 2021 paper (Część I: a text and six questions, 30; Część II: an essay,
# 40). Its scheme prices in words: "Po 1 punkcie za podanie korzyści (3 pkt
# max), 2 punkty za wytłumaczenie". Where it prices points, they are rows;
# where it prints a model answer or a list of reflections priced only as a
# whole, the card is `questionTotal` and shows them (CARD-STANDARD 10a).
def _essay_note(head, total):
    return lambda d: (f'The scheme marks the essay as a whole, out of {total.read(d)[1]}: its '
                      f'criterion, then under “{head.text(d)}” examples of what an essay may '
                      f'reflect on, not a checklist.')


def _essay_question(d, q):
    # The paper's instruction over the two titles (p4), then the title.
    title = re.sub(r'\s*ALBO\s*$', '', q)
    return f'{PL(4, "Napisz wypracowanie").text(d)} {title}'


SPECS[(2021, 'hl')] = [
    R('I4', [menu([S(91), J(S(92), S(93)), S(94), S(95), S(96)], per_point_max(89), lead=S(90)),
             one(J(S(98), S(99)), points_for(89, 'wytłumaczenie'), lead=S(97))],
      total=bracket(88), rownote=lifted(S(89))),
    R('I5', [menu([S(n) for n in range(109, 114)], per_point_max(107), lead=S(108)),
             menu([J(S(114), S(115), S(116)), J(S(118), S(119), S(120))],
                  points_for(107, 'podanie swojej opinii'))],
      total=bracket(106), rownote=lifted(S(107))),
    # "(5)" for the question, no split: the two printed points are the
    # scheme's answer, shown, and the student assesses against the 5.
    R('I6', [shown(J(S(123), S(124), S(125))), shown(J(S(126), S(127)))],
      total=bracket(122), whole=True),
    R('II1', [shown(J(S(133), S(134))), shown(J(S(138), S(139)))]
             + [shown(S(n)) for n in range(140, 145)] + [shown(S(145))]
             + [shown(S(n)) for n in range(146, 150)],
      total=bracket(132), whole=True, rownote=_essay_note(S(137), bracket(132)),
      question=_essay_question),
    # The list runs on over a page break (p6-p7) and ends "‐itp.", which the
    # note's "not a checklist" carries.
    R('II2', [shown(J(S(133), S(134)))] + [shown(S(n)) for n in (154, 155, 156, 161)]
             + [shown(J(S(162), S(163))), shown(S(164)), shown(J(S(165), S(166)))]
             + [shown(S(n)) for n in (167, 168)],
      total=bracket(132), whole=True, rownote=_essay_note(S(153), bracket(132)),
      question=_essay_question),
]


# ================================================================ 2022 OL ===
SPECS[(2022, 'ol')] = [
    # Ordering (rendered scheme p5, paper p7): one card for the printed
    # question, a row per numbered event with the scheme's position and its
    # "1 mark"; (iii) is the printed example with its "1" (18526a518). The
    # scheme words (ii) "co zastanie", the paper "co zobaczy": rows are led by
    # the paper's lines, the answers are the scheme's numbers.
    R('A1f', [one(S(109, after='buty. '), T(109), lead=PL(7, '(i) Zmienił')),
              one(S(110, after='Adama. '), T(110), lead=PL(7, '(ii) ')),
              one(S(112, after='szkoły. '), T(112), lead=PL(7, '(iv) ')),
              one(S(113, after='szatni. '), T(113), lead=PL(7, '(v) ')),
              one(S(114, after='przystanek. '), T(114), lead=PL(7, '(vi) ')),
              one(S(115, after='przygodę. '), T(115), lead=PL(7, '(vii) '))],
      total=T(106, 1),
      question=lambda d, q: '\n'.join(
          [_marker_off(PL(7, '(f) Co po kolei').text(d)) + ' ' + PL(7, '(akapity: 3, 4)').text(d),
           PL(7, '(i) Zmienił').text(d), PL(7, '(ii) ').text(d),
           PL(7, '(iii) ').text(d) + ' ' + PL(7, '1').text(d),
           PL(7, '(iv) ').text(d), PL(7, '(v) ').text(d), PL(7, '(vi) ').text(d),
           PL(7, '(vii) ').text(d)]),
      note='The positions are the scheme\'s (p5, rendered); (iii) is the printed example.'),
    # Matching (rendered scheme p6): 2 = D, 3 = A, 4 = B, "2 marks" each.
    R('A2b', [one(W(159, 0), T(160, 0), lead=PL(10, '2. Najmłodszy')),
              one(W(159, 1), T(160, 1), lead=PL(10, '3. Największy')),
              one(W(159, 2), T(160, 2), lead=PL(10, '4. Najstarszy'))],
      total=T(155, 1),
      question=lambda d, q: '\n'.join(
          [_marker_off(PL(10, '(b) Połącz').text(d)) + ' ' + PL(10, 'odpowiedzi wpisz').text(d)]
          + [PL(10, f'{n}. ').text(d) for n in (1, 2, 3, 4)]
          + [PL(10, f'{x}. ').text(d) for x in 'ABCD'])),
    # "6 marks (2 x 3 marks)" over "Any three of:" and "Podaj 3 szczegóły"
    # (rendered scheme p8): the printed price is carded (CARD-STANDARD 5, the
    # coordinator's ruling on 2026 OL Część A Q4) and both lines are quoted.
    R('A3a', [menu([S(n) for n in range(206, 211)], T(202, 1))],
      rownote=conflict(S(205), T(202, 1), ', though the paper asks for three details')),
    R('A3di', [menu([S(n) for n in range(225, 231)], Times(220, 0))]),
    R('A3dii', [one(S(232), T(220, 2))]),
]


# ================================================================ 2022 HL ===
SPECS[(2022, 'hl')] = [
    # Rendered scheme p7: "(2 x 2m)" is printed on (e)'s head row, one price
    # for each sentence (the old "no tariff" exclusion missed it). The paper
    # prints each answer line opening with the underlined word (p9).
    R('A2ei', [one(S(216), T(213, each=True))],
      question=lambda d, q: ' '.join(
          [_marker_off(PL(9, '(e) Podkreślone').text(d)), q, PL(9, 'zdziwienie').text(d)])),
    R('A2eii', [one(S(218), T(213, each=True))],
      question=lambda d, q: ' '.join(
          [q, PL(9, 'produktywna').text(d)])),
]


# ================================================================ 2023 HL ===
SPECS[(2023, 'hl')] = [
    # Rendered scheme p5: (ii)'s synonyms are printed with no price, and the
    # (d) head prints none. "Celebrytka z Instagramu (50 marks)" less the 48
    # its twelve other parts print ((i) "(2m)") leaves 2. The paper prints the
    # answer line opening with the underlined word, "mnóstwo –" (p5).
    R('A1dii', [one(S(130), TextRemainder(77, 'pl-2023-hl-a-1-', 'pl-2023-hl-a-1-d-ii'))],
      rownote=lambda d: _remainder_line(
          TextRemainder(77, 'pl-2023-hl-a-1-', 'pl-2023-hl-a-1-d-ii'), d),
      question=lambda d, q: ' '.join(
          [_marker_off(PL(5, '(d) Podkreślone').text(d)), q, PL(5, 'mnóstwo').text(d)]),
      note=('The scheme prints no price for (ii); its 2 marks are the text\'s printed '
            '50 less the 48 printed for its other parts (scheme pp4-7).')),
]


# ================================================================ 2023 OL ===
SPECS[(2023, 'ol')] = [
    # Ordering (rendered paper p7, scheme p5): one card for the printed
    # question, a row for each numbered sentence with the position the scheme
    # prints for it and its "2 marks". (iii) is the worked example, printed
    # with its "1" (the census leaves it out: 18526a518), and is shown in the
    # question as printed.
    R('A1g', [one(S(134, after='street. '), T(134), lead=PL(7, '(i) ')),
              one(S(135, after='pictures. '), T(135), lead=PL(7, '(ii) ')),
              one(S(137, after='picture. '), T(137), lead=PL(7, '(iv) ')),
              one(S(138, after='gallery. '), T(138), lead=PL(7, '(v) '))],
      question=lambda d, q: '\n'.join(
          [_marker_off(PL(7, '(g) Put').text(d)) + ' ' + PL(7, '(paragraphs: 5, 6)').text(d),
           PL(7, '(i) ').text(d), PL(7, '(ii) ').text(d),
           PL(7, '(iii) ').text(d) + ' ' + PL(7, '1').text(d),
           PL(7, '(iv) ').text(d), PL(7, '(v) ').text(d)]),
      note='The positions are the scheme\'s (p5, rendered); (iii) is the printed example.'),
    # One printed ask over three columns (paper p10): each person's interests,
    # and the museum the scheme names for each. Zosia's two museums are
    # alternatives, "(2 marks for one option only)".
    R('A2d', [one(S(164, after='Marta – '), T(164), lead=PL(10, 'Marta lubi:')),
              one(S(165, after='Tomek – '), T(165), lead=PL(10, 'Tomek lubi:')),
              menu([S(166, after='Zosia – ', before='/ Żywe'),
                    S(166, after='Poznania/ ', before=' (2 marks')], OptionOnly(166),
                   lead=PL(10, 'Zosia lubi:'))],
      question=lambda d, q: '\n'.join(
          [q.split(' Marta lubi:')[0]] + columns(d, 10, 450, 505, (60, 220, 375, 600))),
      extra_pages=(10,),
      note='Zosia: the scheme prices one of its two museums, "(2 marks for one option only)".'),
    # The table's answers are printed in its right-hand column (rendered
    # scheme p8): the old exclusion ("no answer, only its price") misread it.
    R('A3ai', [one(S(206, after='(i) '), T(208))]),
    R('A3aii', [one(S(209, after='listu '), T(209))]),
    R('A3aiii', [one(S(210, after='Miejscowość '), T(210))]),
    R('A3aiv', [one(S(211, after='Data '), T(211))]),
]


# ================================================================ 2024 OL ===
SPECS[(2024, 'ol')] = [
    # Rendered scheme p6: the (v) tick stands in the Prawda column. The price
    # is the "2 marks" printed in the Marks column on (v)'s first line.
    R('A2cv', [one(S(155, before=' Fałsz'), T(164))],
      note='The tick stands in the Prawda column (scheme p6, rendered).'),
]


def _marker_off(text):
    return re.sub(r'^\(\s*[a-l]\s*\)\s*', '', text)


# Question texts the census reads short or long, corrected with the paper's
# own lines (id -> f(documents, census question) -> question). Applied to the
# cards pl_all builds; the census itself is unchanged.
QFIX = {
    # The box of headings the task matches to parts 2-6, and its example, as
    # the paper prints them under the task (p9).
    'pl-2026-ol-a-2-a': lambda d, q: '\n'.join(
        [q, PL(9, 'W świecie bez internetu').text(d), PL(9, 'Pierwsze dobranocki').text(d),
         PL(9, 'Przykład:').text(d)]),
    # The text layer repeats the NEXT row's label beside this one ("miejsce
    # pierwszej styczności", p4 x=87), and the census appended it.
    'pl-2026-hl-a-1-a-i': lambda d, q: q.split(' miejsce pierwszej styczności')[0],
    # "Podkreślone wyrazy zastąp synonimami ..." heads the part, and the paper
    # prints each answer line opening with the underlined word ("dobrych –",
    # p5); the census keeps neither once the sentence runs past 60 characters,
    # and without them the card does not say which word to replace.
    'pl-2026-hl-a-1-e-i': lambda d, q: ' '.join(
        [_marker_off(PL(5, '(e) Podkreślone').text(d)), q, PL(5, 'dobrych').text(d)]),
    'pl-2026-hl-a-1-e-ii': lambda d, q: ' '.join([q, PL(5, 'uratował').text(d)]),
}


TF = {'true', 'false', 'prawda', 'fałsz'}


def with_instruction(card, ask):
    """A true/false row's card carries the table's printed instruction
    ("Indicate whether the following statements are true or false. ..."): the
    census keeps it only when the statement is short, and a statement alone
    does not say what to do with it."""
    rows = card.get('rows') or []
    if len(rows) == 1 and rows[0]['verbatim'].strip().lower() in TF and ask is not None \
            and ask.stem and not card['questionText'].startswith(ask.stem[:40]):
        card['questionText'] = f'{ask.stem} {card["questionText"]}'
    return card


def fix_question(card, year, level, doc=None, ask=None):
    with_instruction(card, ask)
    fix = QFIX.get(card['id'])
    if not fix:
        return card
    if doc is None:
        doc = {'scheme': scheme_lines(year, level),
               'paper': [(l.page, l.text) for l in pl_paper.PlPaper(year, level).lines]}
    card['questionText'] = fix(doc, card['questionText'])
    return card


def cards(year, level):
    specs = SPECS.get((year, level), [])
    doc = {'scheme': scheme_lines(year, level)}
    P = pl_paper.PlPaper(year, level)
    doc['paper'] = [(l.page, l.text) for l in P.lines]
    doc['lines'] = P.lines
    asks = {a.key: a for a in P.all_asks()}
    out = []
    for spec in specs:
        m = KEY.match(spec.key)
        key = (m.group(1), int(m.group(2)), m.group(3), m.group(4))
        # A card for a whole printed question whose rows the census reads as
        # romans (an ordering task) cites the question; its page is theirs.
        depth = next((i for i, part in enumerate(key) if part is None), len(key))
        ask = asks.get(key) or next(a for k, a in sorted(asks.items(), key=str)
                                    if k[:depth] == key[:depth])
        question = ask.full_text
        if spec.question:
            question = spec.question(doc, question)
        language = answer_language(question)
        note = language_note(language)
        if spec.rownote:
            note = f'{note} {spec.rownote(doc) if callable(spec.rownote) else spec.rownote}'
        rows, total = build_rows(doc, spec, note)
        if spec.whole:
            if total != 0 or spec.total is None:
                raise ValueError(f'{year} {level} {spec.key}: a whole-question card shows rows only')
            tc, tp, _tn = spec.total.read(doc)
            total = tc * tp
        elif spec.total is not None:
            tc, tp, tn = spec.total.read(doc)
            if tc * tp != total:
                raise ValueError(f'{year} {level} {spec.key}: rows add to {total}, printed {tn!r}')
        card = {
            'id': card_id(year, level, key),
            'subjectId': 'polish',
            'level': LEVEL_WORD[level],
            'year': year,
            'section': key[0],
            'topicId': topic_for(year, key[0]),
            'conceptId': concept_for(question),
            'questionRef': question_ref(year, level, key),
            'questionText': question,
            'tariffModel': {'kind': 'questionTotal' if spec.whole else 'fixed'},
            'totalMarks': total,
            'rows': rows,
            'notes': (f'Read on the rendered scheme and paper (languages-q3 lane, 19 Nov 2026); '
                      f'the paper prints this ask on page {ask.page} of the question booklet.'
                      + (f' {spec.note}' if spec.note else '')),
        }
        lead = P.lead(key[1])
        if lead and len(lead) >= 12:
            card['stem'] = lead
        source = source_material(P, ask, language, level, year)
        if source:
            for p in spec.extra_pages:
                if p not in source['pages']:
                    source['pages'].append(p)
            card['sourceMaterial'] = source
        with_instruction(card, ask)
        out.append(card)
    return out
