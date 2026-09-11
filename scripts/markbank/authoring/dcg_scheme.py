#!/usr/bin/env python3
"""Design & Communication Graphics marking schemes — what the SEC prices.

    python3 scripts/markbank/authoring/dcg_scheme.py 2024 hl
    python3 scripts/markbank/authoring/dcg_scheme.py --audit

WHY A DRAWING SUBJECT CARDS AT ALL
----------------------------------
DCG was refused once as "a drawing subject": 57 images in 28 scheme pages, and
nothing to lift. That was true about the wrong half of the document. The
scheme prints the drawn solution AFTER a page banner reading "Sample
Solutions"; everything BEFORE that banner is a priced list of the construction
steps the drawing must contain, in the examiner's own words:

    Question A-1                                                        MARKS
    (a) Complete the perspective drawing of the stand                    (18)
      (i)   Completion of back of stand – vertical surface ................. 6
      (ii)  Completion of back of stand – inclined surface ................. 3
      (iii) Locate side profile of shelf on perspective .................... 5
      (iv)  Completion of the shelf and stand .............................. 4
    (b) Determine and indicate the overall height of the stand            (2)
      (v)   Correct height of stand indicated in millimetres ............... 2
    Total = 20

That is the Construction Studies rule — a drawing question is cardable when
the scheme says what the drawing must contain — with a tariff on every line.
Over the 33 schemes on disk the shape never changes; only the head's case does
("QUESTION A-1" to 2021, "Question A-1" from 2022).

THREE THINGS THE ARITHMETIC HAS TO SETTLE, AND DOES
---------------------------------------------------
1. **A question the paper asks WHOLE** is priced whole: 2010 Higher A-2 heads
   "Axonometric Projection (20)" with no letter at all, and 2024 Higher C-5
   heads "Sectional elevation (60)" and then divides it into the ASSEMBLY's
   own named groups — "Assembly (6)", "Main Body (12)", "Ratchet Pulley (12)".
   A head with marks and no letter opens a unit; a head with marks inside a
   unit that is not yet paid for is a GROUP inside it.

2. **"Presentation" is priced on the QUESTION, not on the part it follows.**
   Every Ordinary question ends with a presentation mark printed as the next
   roman in the run — 2024 Ordinary A-1 sets "(c) Parabolic curve (4)" and
   then "(vi) 2, (vii) 2, (viii) Presentation 2". Read as part (c) it made (c)
   worth six against a printed four, on 10 of that sitting's 12 questions.
   A step that would overflow the unit it follows belongs to the question.

3. **Every sum is checked both ways**: each unit's steps sum to the mark the
   unit prints, and the units plus the question-level steps sum to the "Total
   = N" the SEC prints at the foot. `--audit` reports every question where
   they do not, and there is no averaging or apportioning anywhere in here.
"""
import argparse
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

SUBJECT = 'dcg'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix',
          'xx', 'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii',
          'xxviii', 'xxix', 'xxx']

QHEAD = re.compile(r'^QUESTION\s+([ABC])\s*[-‐-―]\s*([1-9])\s*\.?\s*$', re.I)
# A part marker. The letter is sometimes CAPITAL -- 2015 Ordinary A-4 heads
# its third part "(C) Points of Contact (4)" between a lower-case (a) and (b)
# -- and a lower-case-only class read that part as an unlettered head, which
# put its four marks on the question instead of on the part the paper letters.
PART = re.compile(r'^\(([A-Ha-h])\)\s*(.*?)\s*\((\d{1,3})\)\s*$')
STEP = re.compile(r'^\((' + '|'.join(ROMANS) + r')\)\s*(.*?)\s*(\d{1,3})\s*$')
HEAD = re.compile(r'^(?!\([A-Ha-h]\))(.+?)\s*\((\d{1,3})\)\s*$')
# A part letter printed as a bare HEADING, with its price on the sub-heads
# below it rather than beside it. 2019 Ordinary B-1 sets "(b) Interpenetration"
# and then "Interpenetration on Left Hand Side (5)" and "... Right Hand Side
# (6)" under it: eleven marks the paper letters (b) and the scheme never
# prices on one line. Read as a wrapped part the letter took the first
# sub-head's five marks and the other six fell off the letter altogether.
PART_SCOPE = re.compile(r'^\(([A-Ha-h])\)\s*(\S.*)$')
TOTAL = re.compile(r'^Total\s*=\s*(\d{1,3})\s*$', re.I)

# The banner the drawn solutions open under. Everything after it is a picture
# with a question number over it, and reading it as scheme text produced twelve
# empty questions a sitting.
SOLUTIONS = re.compile(r'^(?:Sample Solutions|Marking Scheme Question)\b', re.I)
# The coursework, marked from a portfolio rather than from this examination.
ASSIGNMENT = re.compile(r'^Student Assignment\b', re.I)

# Running heads, foliation and the column caption.
NOISE = re.compile(
    r'^(?:##\s|MARKS\s*$|LEAVING CERTIFICATE\b|Leaving Certificate\b'
    r'|Design (?:&|and) Comm|Coimisiún|State Examinations'
    r'|-\s*\d{1,3}\s*-\s*$|Page\s+\d+\s+of\s+\d+\s*$|\d{1,3}\s*$'
    r'|Marking Scheme\s*$|Note:\s*Other valid solutions)', re.I)

# The dotted leader the SEC sets between a step and its mark, plus the stray
# ellipsis it sometimes leaves inside the step's own words.
LEADER = re.compile(r'[\s.…·]{2,}$')

# A marker at the head of a logical entry, whether or not its mark has arrived.
OPENS = re.compile(r'^\((?:[A-Ha-h]|' + '|'.join(ROMANS) + r')\)')

# Where the SEC's own arithmetic contradicts itself, keyed (year, level,
# section, question, letter) and never inferred. Each entry records the mark
# the scheme PRINTS, the mark its own steps and its own "Total =" line
# require, and the sum that proves it — a misprint is a fact about one page,
# so it is written down rather than smoothed over by a rule.
MISPRINTS = {
    (2012, 'hl', 'C', 5, 'a'): {
        'printed': 42, 'corrected': 41,
        'why': 'the part\'s own eight named groups price 5+10+3+4+2+7+4+6 = '
               '41, and the question\'s printed "Total = 45" is that 41 plus '
               'the 4 the scheme prices part (b) at',
    },
}

# The same thing for an UNLETTERED head — an assembly's named component, which
# is how Section C question 5 is priced. A head is what separates one unit
# from the next, so a head whose printed mark disagrees with its own steps
# does not merely mis-state that unit: every later head is read as a GROUP
# inside the unit that is still unpaid, and its steps fall off into the
# question's trailer. That is a silent loss of whole components, and it is
# invisible to the arithmetic check, because the trailer counts toward the
# question's total either way. Keyed (year, level, section, question, title).
HEAD_MISPRINTS = {
    (2022, 'hl', 'C', 5, 'Base'): {
        'printed': 13, 'corrected': 12,
        'why': 'the unit\'s own four steps price 4+3+2+3 = 12, and the nine '
               'component heads of the question sum to 61 against the '
               'scheme\'s printed "Total = 60" — 12 is the value that '
               'satisfies both. Read at the printed 13 the five components '
               'after it (Vertical Spindle 7, Vice Pivot 6, Lower Jaw '
               'Spindle 8, Clamping Jaw 4, Rotating Boss & Dowel 7) were '
               'never opened as units at all',
    },
}


def _entries(lines):
    """The scheme's LOGICAL lines: a wrapped step joined back to its mark.

    The SEC breaks a long step across two printed lines and sets the mark at
    the end of the SECOND one:

        (xiv) Completion of elevation by projection of point F back to elevation
        incl. correct transfer of distances, etc. ............................ 3

    Read line by line, neither half is a priced step: the first has no mark
    and the second has no marker, so three marks vanish and the part reports
    a shortfall against its own printed total. Six Higher parts across 2016
    and 2017 were short for exactly this reason. A marker opens an entry and
    the entry stays open until a mark closes it.
    """
    out = []
    pending = None
    for line in lines:
        if pending is not None:
            joined = f'{pending} {line}'
            # Two markers running together is not a wrap, and neither is a
            # marker followed by a line that is already complete on its own:
            # "(b) Interpenetration" above "Interpenetration on Left Hand
            # Side (5)" is a lettered SCOPE over two priced sub-heads, and
            # joining them gave the letter one sub-head's marks and lost the
            # other's. Emit the opener as it stands.
            #
            # The marker test comes FIRST, before the join is tried, because
            # a joined pair can itself LOOK like one step: 2010 Higher C-3
            # divides part (c) with unpriced roman sub-heads, and "(i)
            # Surfaces B and C" joined to "(viii) Use of correct widths on
            # surface B (or surface C) ... 1" matches STEP as a single step
            # numbered (i) whose text is the two lines welded together. Four
            # Higher questions across 2010-2012 lost their roman run that way
            # and the step the SEC printed under the divider was never read
            # under its own number.
            if OPENS.match(line):
                out.append(pending)
                pending = None
                # fall through: the opener below is re-examined on its own
            elif STEP.match(joined) or PART.match(joined):
                out.append(joined)
                pending = None
                continue
            elif HEAD.match(line) or len(pending) > 400:
                out.append(pending)
                pending = None
            else:
                pending = joined
                continue
        if OPENS.match(line) and not STEP.match(line) and not PART.match(line):
            pending = line
            continue
        out.append(line)
    if pending is not None:
        out.append(pending)
    return out


# Words that carry no subject matter in either document, for the one scorer
# the census and the authoring pass share. The positional ones matter as much
# as the grammatical: the scheme divides one interpenetration into
# "Interpenetration on Left Hand Side" and "... Right Hand Side" while the
# paper asks for it once, so "left", "right", "hand" and "side" are three
# quarters of that title and none of them says what the drawing is.
STOPWORDS = frozenset("""a an and are as at be been by draw drawn for from
given in including into is it its of on or required shown that the their then
there these this to with your
left right hand side lhs rhs upper lower top bottom front back part parts
complete completion correct required""".split())

WORD = re.compile(r"[A-Za-z][A-Za-z'\u2019-]+")


def words(text):
    """The content words of a printed line, for scoring one against another."""
    out = set()
    for w in WORD.findall((text or '').lower()):
        w = w.rstrip('s') if len(w) > 4 and w.endswith('s') else w
        if w not in STOPWORDS and len(w) > 2:
            out.add(w)
    return out


def cue_score(unit_title, ask_text):
    """The share of the scheme's own words for a unit that the ask holds."""
    u = words(unit_title)
    if not u:
        return 0.0
    return len(u & words(ask_text)) / len(u)


# How much of a unit's title the paper's ask must hold before the pairing
# counts as confirmed by wording rather than by the printed address.
CUE_FLOOR = 0.34


class Step:
    __slots__ = ('roman', 'text', 'marks', 'group')

    def __init__(self, roman, text, marks, group):
        self.roman, self.text, self.marks, self.group = roman, text, marks, group

    def __repr__(self):
        return f'({self.roman}) {self.text} = {self.marks}'


class Unit:
    """One priced unit of a question: a lettered part, or the question itself."""

    __slots__ = ('letter', 'title', 'marks', 'steps')

    def __init__(self, letter, title, marks):
        self.letter, self.title, self.marks = letter, title, marks
        self.steps = []

    @property
    def step_sum(self):
        return sum(s.marks for s in self.steps)

    def __repr__(self):
        return f'<{self.letter or "whole"} "{self.title}" {self.marks}>'


class Question:
    __slots__ = ('section', 'q', 'total', 'units', 'trailer', 'page')

    def __init__(self, section, q, page):
        self.section, self.q, self.page = section, q, page
        self.total = None
        self.units = []
        self.trailer = []          # question-level steps ("Presentation")

    @property
    def key(self):
        return (self.section, self.q)

    @property
    def unit_sum(self):
        return sum(u.marks for u in self.units) + sum(s.marks
                                                      for s in self.trailer)

    def unit(self, letter):
        for u in self.units:
            if u.letter == letter:
                return u
        return None

    def faults(self):
        out = []
        if self.total is None:
            out.append('no "Total =" printed')
        elif self.unit_sum != self.total:
            out.append(f'units sum to {self.unit_sum}, the scheme prints '
                       f'Total = {self.total}')
        for u in self.units:
            if u.step_sum != u.marks:
                out.append(f'({u.letter or "whole"}) steps sum to '
                           f'{u.step_sum}, the scheme prints ({u.marks})')
        # The arithmetic alone cannot see a LOST unit. A question whose
        # trailer holds the marks of five components still sums to its printed
        # total, because the trailer counts toward the total too — 2022 Higher
        # C-5 balanced perfectly with Vertical Spindle, Vice Pivot, Lower Jaw
        # Spindle, Clamping Jaw and Rotating Boss & Dowel never read as units
        # at all. What the loss DOES disturb is the roman run: the SEC numbers
        # a question's steps (i), (ii), (iii)… straight through, so a unit
        # holding a gapped run, or a trailer opening before the units end, is
        # a step that has been filed under the wrong head.
        order = {r: i for i, r in enumerate(ROMANS)}
        for u in self.units:
            idx = [order[s.roman] for s in u.steps if s.roman in order]
            if idx and idx != list(range(idx[0], idx[0] + len(idx))):
                out.append(f'({u.letter or "whole"}) "{u.title}" holds a '
                           f'broken roman run '
                           f'{[s.roman for s in u.steps]}')
        placed = [order[s.roman] for u in self.units for s in u.steps
                  if s.roman in order]
        tail = [order[s.roman] for s in self.trailer if s.roman in order]
        if tail and placed and min(tail) < max(placed):
            out.append(f'the question-level steps '
                       f'{[s.roman for s in self.trailer]} open before the '
                       f'units end at ({ROMANS[max(placed)]}) — a priced head '
                       f'was read as a group instead of a unit')
        return out

    def __repr__(self):
        return f'<{self.section}-{self.q} {self.total}>'


def scheme_path(year, level, subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes',
                        f'{year}-{level}.md')


def has_scheme(year, level, subject=SUBJECT):
    return os.path.exists(scheme_path(year, level, subject))


class DcgScheme:
    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = scheme_path(year, level, subject)
        self.questions = {}
        self.flags = []
        self._read()

    def _read(self):
        page = 0
        cur = None
        unit = None
        group = None
        letter_scope = None
        stopped = False
        with open(self.path, encoding='utf-8') as fh:
            raw = fh.read()
        lines = [' '.join(l.split()) for l in raw.split('\n')]
        for line in _entries([l for l in lines if l]):
            if line.startswith('## Page'):
                page = int(line.split()[-1])
                continue
            if SOLUTIONS.match(line) or ASSIGNMENT.match(line):
                stopped = True
                cur = unit = None
                continue
            if stopped:
                continue
            m = QHEAD.match(line)
            if m:
                key = (m.group(1), int(m.group(2)))
                seen = self.questions.get(key)
                if seen is not None and seen.total is not None:
                    # The DRAWN solutions, which the SEC heads with the same
                    # "Question B-1" over a full-page picture. Read as scheme
                    # text they replaced eight finished questions of the 2020
                    # Higher scheme with eight empty ones -- 29 priced steps
                    # where the sitting prices 130.
                    stopped = True
                    cur = unit = group = letter_scope = None
                    continue
                if seen is not None:
                    # A question the SEC broke over a page and re-headed.
                    cur, unit, group, letter_scope = seen, None, None, None
                    continue
                cur = Question(key[0], key[1], page)
                unit = group = letter_scope = None
                self.questions[key] = cur
                continue
            if cur is None or NOISE.match(line):
                continue
            t = TOTAL.match(line)
            if t:
                cur.total = int(t.group(1))
                cur = unit = letter_scope = None
                continue
            scope = PART_SCOPE.match(line)
            if scope and not PART.match(line) and not STEP.match(line):
                letter_scope = scope.group(1).lower()
                unit = None
                group = _clean(scope.group(2))
                continue
            p = PART.match(line)
            if p:
                letter_scope = None
                marks = int(p.group(3))
                fix = MISPRINTS.get((self.year, self.level, cur.section, cur.q,
                                     p.group(1).lower()))
                if fix and fix['printed'] == marks:
                    marks = fix['corrected']
                    self.flags.append({
                        'type': 'sec-misprint',
                        'where': f'{self.year} {self.level} {cur.section}-'
                                 f'{cur.q}({p.group(1)})',
                        'detail': f'the scheme prints ({fix["printed"]}) where '
                                  f'{fix["corrected"]} is required: '
                                  f'{fix["why"]}'})
                unit = Unit(p.group(1).lower(), _clean(p.group(2)), marks)
                group = None
                cur.units.append(unit)
                continue
            s = STEP.match(line)
            if s:
                marks = int(s.group(3))
                step = Step(s.group(1), _clean(s.group(2)), marks, group)
                if unit is not None and unit.step_sum + marks <= unit.marks:
                    unit.steps.append(step)
                else:
                    cur.trailer.append(step)
                continue
            h = HEAD.match(line)
            if h:
                title, marks = _clean(h.group(1)), int(h.group(2))
                fix = HEAD_MISPRINTS.get((self.year, self.level, cur.section,
                                          cur.q, title))
                if fix and fix['printed'] == marks:
                    marks = fix['corrected']
                    self.flags.append({
                        'type': 'sec-misprint',
                        'where': f'{self.year} {self.level} {cur.section}-'
                                 f'{cur.q} "{title}"',
                        'detail': f'the scheme prints ({fix["printed"]}) where '
                                  f'{fix["corrected"]} is required: '
                                  f'{fix["why"]}'})
                if unit is None or unit.step_sum >= unit.marks:
                    # Inside a bare lettered scope the head is that letter's
                    # own unit; outside one it is the question's.
                    letter = letter_scope
                    # A priced head where nothing is open, or where the open
                    # part is already paid for in full, is a UNIT of its own.
                    # 2021 Ordinary B-3 prices the interpenetration between
                    # (a) and (b) as two unlettered heads, "Interpenetration
                    # on Left Hand Side (8)" and "... Right Hand Side (8)";
                    # read as groups inside (a) their sixteen marks fell off
                    # the question altogether, and the paper's part (b) had
                    # nothing priced against it.
                    unit = Unit(letter, title, marks)
                    group = None
                    cur.units.append(unit)
                else:
                    group = title
                continue
            # A bare label with no marks: the SEC's own divider inside a part
            # ("Earthworks between A and B (Level) – Embankment").
            group = _clean(line)

    # ------------------------------------------------------------- accessors
    def priced(self):
        """Every priced unit, in the order the scheme prints it."""
        for key in sorted(self.questions):
            for unit in self.questions[key].units:
                yield self.questions[key], unit

    def faults(self):
        out = []
        for key in sorted(self.questions):
            for fault in self.questions[key].faults():
                out.append((key, fault))
        return out


def _clean(text):
    text = LEADER.sub('', ' '.join(str(text).split())).strip()
    return text.strip(' .·…')


def sittings(subject=SUBJECT):
    out = []
    for f in sorted(glob.glob(scheme_path('[0-9][0-9][0-9][0-9]', '[ho]l',
                                          subject))):
        m = re.fullmatch(r'(\d{4})-(hl|ol)\.md', os.path.basename(f))
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def audit(subject=SUBJECT):
    bad = 0
    qs = steps = 0
    for year, level in sittings(subject):
        S = DcgScheme(year, level, subject)
        faults = S.faults()
        nq = len(S.questions)
        nsteps = sum(len(u.steps) for q in S.questions.values()
                     for u in q.units)
        nunits = sum(len(q.units) for q in S.questions.values())
        qs += nunits
        steps += nsteps
        line = (f'{year} {level}: {nq} questions, {nunits} priced units, '
                f'{nsteps} priced steps')
        if faults or nq != 12 or S.flags:
            bad += 1
            line += '  <<<'
        print(line)
        for flag in S.flags:
            print(f'    FLAG {flag["type"]} {flag["where"]}: {flag["detail"]}')
        for key, fault in faults:
            print(f'    {key[0]}-{key[1]}: {fault}')
    print(f'{qs} priced units holding {steps} priced steps; '
          f'{bad} sitting(s) with something to explain')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()
    if args.audit:
        return 0 if audit() == 0 else 1
    S = DcgScheme(args.year, args.level)
    for key in sorted(S.questions):
        qq = S.questions[key]
        print(f'== {qq.section}-{qq.q}  Total = {qq.total}  (p{qq.page})')
        for u in qq.units:
            print(f'   ({u.letter or "whole"}) {u.title} ({u.marks})')
            for s in u.steps:
                print(f'        {"[" + s.group + "] " if s.group else ""}'
                      f'({s.roman}) {s.text} = {s.marks}')
        for s in qq.trailer:
            print(f'   QUESTION-LEVEL ({s.roman}) {s.text} = {s.marks}')
        for fault in qq.faults():
            print(f'   FAULT {fault}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
