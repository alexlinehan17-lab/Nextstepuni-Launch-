#!/usr/bin/env python3
"""Latin marking schemes — what the SEC states, at the address it states it.

    python3 scripts/markbank/authoring/lat_scheme.py 2025 hl
    python3 scripts/markbank/authoring/lat_scheme.py 2023 ol --json

WHAT THE SCHEME PRINTS, AND WHAT IT DOES NOT
--------------------------------------------
Latin's scheme is unusually generous and unusually uneven, and the split is not
between questions but between KINDS of question:

  * **Comprehension** (Question 1 Section B) — the answers themselves, priced
    phrase by phrase: "(i) A maiden (3) and one of the hostages (3)",
    "(iii) She swam across the Tiber (4) … ----any three for full twelve marks".
  * **Literature and Roman history** (Question 3's second part, Question 5) —
    a printed tariff ("(a) 4 + 3 (+ 3) for one reason") and then, under the
    head "Indicative Notes—Candidates may make valid points other than those
    listed below", paragraphs of the SEC's own content.
  * **Grammar** (Question 4(i)) — at Higher from 2023 the answers themselves:
    "patriae=dative meaning 'for'; defendi=pres infin passive after possent".
  * **Translation** (Question 1 Section A, Question 2, Question 3's first
    part) — NO answer. What is printed is the SOURCE, cut into units with a
    mark against each: "reportatur Segestam;/2", "Vident…aegrius; 12/", or the
    English of a prose composition with a per-word tariff written above it.
    Ordinary replaces even that with a deduction table ("Major error= -3").
    That is a mark allocation over a text the candidate is given, not a model
    answer, so a translation ask is an EXCLUSION with the printed line as its
    evidence — not the Applied Maths model-solution case.

HOW AN ADDRESS IS READ
----------------------
The scheme heads its units in eight different ways across the corpus — "Q3 A.
(i) (60) Translate", "3.A [90]", "3 A (ii) Indicative Notes:", "3B (ii)",
"1 B. Indicative Answers: [75]", "5A.", "(A)", "A. Ovid" — so the head is read
as a pattern rather than a literal, and a question number may only ever go
FORWARDS. The route letter is dropped for Questions 4 and 5, which print no
routes on the paper: the "A." under Q5 in the 2025 scheme is a section heading
left over from a paper that has not set sections since 2022.

The letter run is NOT forward-only, because the scheme prints it twice — once
as the tariff list and again under the Indicative Notes — and forcing it
forwards threw the second copy, which is the half that holds the answers.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

SUBJECT = 'latin'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii']


def scheme_path(year, level, subject=SUBJECT):
    path = os.path.join(ROOT, 'examiner-reports', subject, 'schemes',
                        f'{year}-{level}.md')
    if not os.path.exists(path):
        raise FileNotFoundError(f'no {subject} scheme for {year} {level}')
    return path


# The two front pages every SEC scheme opens with, and the running heads.
BOILERPLATE = re.compile(
    r'^Note to teachers and students|^Marking schemes? (?:published|are)'
    r'|^Coimisi[úu]n na Scr[úu]duithe|^State Examinations Commission'
    r'|^Leaving Certi[fi]+cate \d{4}|^Marking Scheme$|^Higher Level$'
    r'|^Ordinary Level$|^Latin$|^Future Marking Schemes'
    r'|^LC Latin (?:Higher|Ordinary) Level Marking Scheme'
    r'|^Leaving Certificate Latin (?:Higher|Ordinary) Level'
    r'|^\s*\d{1,2}\s*(?:\|\s*P\s*a\s*g\s*e)?\s*$'
    r'|^BLANK PAGE|^## Page ', re.I)

# A question head, in every spelling the eight schemes print:
#   "Q1. Answer Section A or Section B in this question [75]"
#   "1. Answer Section A or Section B in this question:- [75]"
#   "3.A [90]"        "3 A (ii) Indicative Notes:"      "3B. (i) (60) Translate"
#   "Q3 A. (i) Translate (60)"   "1 B. Indicative Answers: [75]"    "5A."
QHEAD = re.compile(
    # The route letter must carry a DELIMITER of its own — "3.A [90]", "1 B.",
    # "(A)". Without one, "1. Answer Section A or Section B" opened a Section
    # A whose first marking point was "nswer Section A or Section B".
    r'^Q?\s*([1-5])\s*[.\s]?\s*'
    r'(?:\(([A-D])\)\s*\.?\s*|([A-D])\s*[.)]?(?=[\s.)]|$)\s*[.)]?\s*)?'
    r'(?:\((' + '|'.join(ROMANS) + r')\)\s*)?')
# A route head on its own line: "A.", "(A)", "B. Virgil", "A. Translate into
# Latin:-", "B. Indicative Answers:".
RHEAD = re.compile(r'^\(?([A-D])\)?\s*[.)]?\s+|^\(?([A-D])\)?\s*[.)]\s*$')
RMARK = re.compile(r'^\((' + '|'.join(ROMANS) + r')\)\s*')
# "( c )" — the 2021 Higher scheme sets one letter with spaces inside the
# brackets, and a tight pattern filed its answer under (b).
LMARK = re.compile(r'^\(\s*([a-f])\s*\)\s*')
NOTES = re.compile(r'Indicative\s+(?:Notes?|Answers?)', re.I)
TARIFF_TOTAL = re.compile(r'\[(\d{1,3})\]')


class Entry:
    """Every printed line the scheme sets at one address."""
    __slots__ = ('key', 'lines', 'notes_from')

    def __init__(self, key):
        self.key = key
        self.lines = []
        # The index in `lines` at which the Indicative Notes began, or None.
        # Everything before it is the SEC's arithmetic; everything after is
        # the SEC's content. Both are kept — Question 1 Section B and Question
        # 4 print their answers in the arithmetic half.
        self.notes_from = None

    @property
    def tariff_lines(self):
        return self.lines[:self.notes_from if self.notes_from is not None
                          else len(self.lines)]

    @property
    def note_lines(self):
        return ([] if self.notes_from is None
                else self.lines[self.notes_from:])

    def __repr__(self):
        return f'<Entry {self.key} {len(self.lines)} line(s)>'


class LatScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        self.text = open(self.path, encoding='utf-8').read()
        self._entries = None
        self.question_totals = {}

    def entries(self):
        if self._entries is None:
            self._entries = self._walk()
        return self._entries

    def by_key(self):
        return self.entries()

    def _walk(self):
        out = {}
        q, route, roman, letter = None, None, None, None
        in_notes = False

        def key():
            # Questions 4 and 5 print no routes on the paper; the "A." the
            # 2025 scheme sets under Q5 is a heading left over from a paper
            # that has not printed sections since 2022, and keying on it made
            # every 2025 essay an orphan.
            return (None if q in (4, 5) else route, q, letter, roman)

        def add(line):
            if q is None:
                return
            entry = out.setdefault(key(), Entry(key()))
            if in_notes and entry.notes_from is None:
                entry.notes_from = len(entry.lines)
            entry.lines.append(line)

        for raw in self.text.splitlines():
            line = ' '.join(raw.split())
            if not line or BOILERPLATE.match(line):
                continue
            head = QHEAD.match(line)
            if head and int(head.group(1)) >= (q or 1) and _is_head(line, head):
                nq = int(head.group(1))
                rest_of_head = line[head.end():].strip()
                if nq != q or rest_of_head:
                    # A head that carries MORE than its own address opens a
                    # new unit, and a new unit starts with its tariff list:
                    # "3B. (i) (60) Translate" ends the Indicative Notes of
                    # Section A above it. A head that is only an address —
                    # "3A.", "5A." — is the notes' own heading and does not.
                    # Without the distinction the whole of Question 3 Section
                    # B read as notes, its tariff line went with them, and 41
                    # asks had no notation to card with.
                    in_notes = bool(NOTES.search(line))
                q = nq
                route = head.group(2) or head.group(3)
                roman = head.group(4)
                letter = None
                total = TARIFF_TOTAL.search(line)
                if total:
                    self.question_totals[q] = int(total.group(1))
                rest = line[head.end():].strip()
                if NOTES.search(line):
                    in_notes = True
                if rest and not NOTES.match(rest):
                    add(rest)
                continue
            if NOTES.match(line):
                in_notes = True
                rest = NOTES.sub('', line, count=1).strip(' -—:;.')
                if rest:
                    add(rest)
                continue
            if q == 2:
                m = Q2_AUTHOR.match(line)
                if m:
                    route = m.group(2) or route
                    roman, letter = m.group(3), None
                    rest = line[m.end():].strip()
                    add(f'{m.group(1)} {rest}'.strip())
                    continue
            m = RHEAD.match(line)
            if m and _is_route(line):
                route = m.group(1) or m.group(2)
                roman, letter = None, None
                rest = line[m.end():].strip()
                # A route head opens a new unit, and a new unit starts with
                # its own tariff list — "B. (i) Translate into English (60)"
                # ends Section A's Indicative Notes above it. Left running,
                # the whole of Question 3 Section B read as notes and its
                # tariff line went with them.
                in_notes = bool(NOTES.search(line))
                if in_notes:
                    rest = NOTES.sub('', rest, count=1).strip(' -—:;.')
                rm = RMARK.match(rest)
                if rm:
                    roman = rm.group(1)
                    rest = rest[rm.end():].strip()
                if rest:
                    add(rest)
                continue
            rest, moved = _consume_markers(line)
            if moved:
                roman = moved[0] if moved[0] is not None else roman
                letter = moved[1]
                if moved[0] is not None:
                    letter = moved[1]
                if rest:
                    add(rest)
                continue
            add(line)
        return _reattach(out)


def _reattach(entries):
    """Put the Indicative Notes back under the part they answer.

    The scheme prints its answers twice removed from their address. It heads
    the notes for Question 3 Section A with "3A." and then lists "(a)", "(b)",
    "(c)" — never restating the "(ii)" those letters live under, because the
    examiner reading it has the tariff list on the page above. Read literally
    that files the answer to Question 3 Section A (ii)(a) at a roman-less
    address the paper never prints, and the card for the printed ask finds
    nothing.

    The scheme's own tariff list is the evidence for where it belongs: it
    already priced "(a)" under "(ii)" a page earlier. So a roman-less entry is
    merged into its lettered sibling when the scheme names exactly ONE roman
    for that letter — never when it names two, which would be a guess.

    The same head does it one level up: "5A." is followed by the notes for
    Question 5(i) with no "(i)" in front of them, because (i) is the first
    part of the question. Those merge into the question's first roman.
    """
    def merge(src, dst):
        at = len(dst.lines)
        dst.lines += src.lines
        if src.notes_from is not None and dst.notes_from is None:
            dst.notes_from = at + src.notes_from
        elif src.notes_from is not None:
            pass
        return dst

    for key in [k for k in entries if k[2] is not None and k[3] is None]:
        sibs = [k for k in entries
                if k[:3] == key[:3] and k[3] is not None]
        if len(sibs) == 1:
            merge(entries.pop(key), entries[sibs[0]])

    for key in [k for k in entries if k[2] is None and k[3] is None]:
        entry = entries[key]
        if entry.notes_from is None:
            continue
        romans = sorted((k for k in entries
                         if k[:2] == key[:2] and k[2] is None
                         and k[3] is not None),
                        key=lambda k: ROMANS.index(k[3]))
        if not romans:
            continue
        notes = entry.note_lines
        entry.lines = entry.tariff_lines
        entry.notes_from = None
        target = entries[romans[0]]
        at = len(target.lines)
        target.lines += notes
        if target.notes_from is None:
            target.notes_from = at
    return entries


def _consume_markers(line):
    """Strip the part markers a printed line OPENS with, however many.

    The scheme sets more than one on a line: the Indicative Notes of the 2025
    Higher Question 5 open "(vi) (a) Photograph B – Depicts the Romans
    carrying the plunder…", and consuming only the first filed the answer to
    (a) under (vi), where the card for (a) could never find it.

    Returns (the rest of the line, (roman, letter)) — or (line, None) when the
    line opens with no marker at all.
    """
    roman = letter = None
    rest, hit = line, False
    while True:
        m = RMARK.match(rest)
        if m:
            roman, letter, hit = m.group(1), None, True
            rest = rest[m.end():].strip()
            continue
        m = LMARK.match(rest)
        if m:
            tail = rest[m.end():].strip()
            if hit and re.match(r'^(?:or|and|,)\b', tail, re.I):
                # "(i) (a) or (b) 4 + 3 + 3 (10)" — the SEC naming the choice
                # the part offers, not opening part (a). Consumed as a marker
                # it filed Question 4's whole tariff under (a) and left (b)
                # with nothing, in both 2021 and 2022 Higher.
                break
            letter, hit = m.group(1), True
            rest = tail
            continue
        break
    return (rest, (roman, letter)) if hit else (line, None)


def _is_head(line, m):
    """Is this "3.A [90]" a question head, or a sentence that starts with a digit?

    A head names its own unit and then stops: what follows is a rubric, a
    tariff, a route letter or nothing at all. A marking point never opens with
    a bare number and a full stop.
    """
    rest = line[m.end():].strip()
    if m.group(2) or m.group(3) or m.group(4):
        return True
    return bool(re.match(r'^(?:Answer|Translate|Any\b|\[|\(|$)', rest, re.I))


# Question 2 heads its passages by AUTHOR, and prints the address after the
# name rather than in front of it: "Virgil A (i) Principio sociis edicit signa
# sequantur/7", "Ovid A (ii)", "Catullus (ii)". Read left to right the line
# opens with a word, so nothing marked it, and the 2024 and 2025 Section A
# passages were filed under the route head above them — one address for two
# printed passages.
Q2_AUTHOR = re.compile(
    r'^([A-Z][A-Za-z]{2,11})\s+(?:([A-D])\s+)?\((' + '|'.join(ROMANS) + r')\)\s*')


def _is_route(line):
    """Is this "B. Virgil" a route head, or a marking point that begins with one?

    A route head is the letter and then, at most, the author or the rubric of
    the route it opens. Anything longer is an answer — "D. Nunc homo
    audacissimus atque amentissimus hoc cogitat./5" is Section D's PASSAGE,
    printed under its own letter, and it is one line long.
    """
    if re.match(r'^\([A-D]\)', line):
        # A BRACKETED capital is always the SEC heading a route. The 2021
        # Higher scheme prints Question 2's four passages as "(A) illi haec
        # inter se dubiis de rebus agebant" — head and passage on one line —
        # so a length test called the longest of them a marking point.
        return True
    body = re.sub(r'^\(?[A-D]\)?\s*[.)]?\s*', '', line).strip()
    if not body:
        return True
    if len(body) <= 60:
        return True
    return bool(re.match(
        r'^(?:Translate|Indicative|Answer|\((?:' + '|'.join(ROMANS) + r')\))',
        body, re.I))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    S = LatScheme(args.year, args.level)
    entries = S.entries()
    if args.json:
        json.dump({str(k): e.lines for k, e in entries.items()}, sys.stdout,
                  ensure_ascii=False, indent=1)
        return 0
    print(f'{args.year} {args.level}: {len(entries)} priced address(es), '
          f'question totals {S.question_totals}')
    for k in sorted(entries, key=str):
        e = entries[k]
        print(f'  {str(k):26} {len(e.lines):2}L notes@{e.notes_from} '
              f'{" | ".join(e.lines)[:110]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
