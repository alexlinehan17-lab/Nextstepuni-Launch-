#!/usr/bin/env python3
"""Design & Communication Graphics question papers — the printed ask.

    python3 scripts/markbank/authoring/dcg_paper.py 2024 hl
    python3 scripts/markbank/authoring/dcg_paper.py --audit

The examination
---------------
DCG is SEC subject 562 and it is sat as TWO booklets on one morning, under one
marking scheme:

    M81A    Section A   Core - Short Questions       60 marks
                        A-1 to A-4 are printed, a candidate answers any three,
                        20 marks each, on one A3 sheet inside the booklet.
    M81BC   Section B   Core - Long Questions        )
            Section C   Applied Graphics - Long      ) 180 marks
                        B-1 to B-3 are printed and two answered; C-1 to C-5 are
                        the five Applied Graphics OPTIONS and one is answered.
                        60 marks each.

Every one of the 33 sittings on disk — 2010 to 2026, less the 2020 Ordinary
sitting that Covid cancelled — prints exactly those twelve questions, in those
three sections, at those tariffs. That uniformity is the denominator: 12
questions a paper, 396 questions over the corpus, and `--audit` asserts it.

WHICH BOOKLET IS WHICH IS NOT THE FILE NAME. The SEC's component code for the
Section A booklet is 014 in every year but 2011, where the two are swapped and
000 carries Section A. Reading the code would have censused 2011's Section A
twice and its Sections B and C never — Law 3's wholesale loss. The booklet is
identified by the markers it PRINTS: the one that heads questions "A-1" is the
Section A booklet.

THE TRAP THIS READER EXISTS FOR
-------------------------------
**Section A is set sideways, in quadrants, on an A3 sheet.** The page carries
/Rotate 90 and its text is drawn at dir (0,-1), so pymupdf hands back a line
whose x0 is its VERTICAL position on the sheet and whose y runs backwards
along it. Read as ordinary coordinates the four questions interleave: 2024
Higher returns A-2, A-4, A-1, A-3 in block order and every continuation line
lands under whichever question happens to sit beside it.

`rows()` turns a rotated line back into reading coordinates — vy the line's
position down the sheet, vx its position across it — and `_quadrants()` then
cuts the sheet the way the SEC set it: the markers themselves name the two
COLUMNS, and inside a column a line belongs to the last marker above it. The
same routine reads the portrait Sections B and C pages, where there is one
question to a page and the geometry is already the right way up.

**The marker is often alone on its line.** "A-3." is a line, and the ask opens
on the next one — while "A-1. The 3D graphic below shows a truncated" glues
the two together. Both spellings are the SEC's, in the same booklet, on the
same sheet, so the head is taken as a PREFIX of its row rather than as a row.
"""
import argparse
import collections
import functools
import glob
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

SUBJECT = 'dcg'
SECTIONS = ('A', 'B', 'C')
# How many questions each section PRINTS, in every sitting on disk. Asserted
# by --audit, never assumed. What each is WORTH is not a constant and is not
# here: 2019 prices Sections B and C at 45 marks a question and sets two
# Applied Graphics options, where 2020 onwards prices them at 60 and sets one.
# Both make the 240 the covers state. The tariff is read from the paper's own
# cover instead -- see SECTION_TARIFF.
SECTION_SHAPE = {'A': 4, 'B': 3, 'C': 5}

# "• All questions in Section A carry 20 marks each." -- the paper's own
# statement of what one question of a section is worth. The 2021 and 2022
# sittings name two sections at once, "All questions in Section B and Section
# C carry 60 marks each", because those two Covid papers MERGE them: eight
# questions are presented across B and C and a candidate answers any two,
# where every other year sets two of three in B and one option of five in C.
SECTION_TARIFF = re.compile(
    r'All questions in Sections?\s+([ABC])(?:\s+and\s+Section\s+([ABC]))?'
    r'\s+carry\s+(\d{1,3})\s+marks', re.I)
# "Section A  (60 marks)", "Section B and C  (180 marks)" -- the cover total.
COVER_TOTAL = re.compile(r'Sections?\s+[ABC](?:\s+and\s+[ABC])?\s*'
                         r'\((\d{2,3})\s*marks\)', re.I)
LETTERS = 'abcdefgh'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']

# "A-1.", "B-2", "C-4." — the SEC's own address for a question, and the same
# string the marking scheme heads its answer with.
QHEAD = re.compile(r'^([ABC])\s*[-‐-―]\s*([1-9])\s*\.?(?![0-9])\s*')
# A part marker at the head of a row. The SEC letters parts (a)..(h) and
# numbers the level below them in romans; "(c) (i)" opens both at once.
PART = re.compile(r'^\(([a-h])\)\s*')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{1,3}|ix|x)\)\s*')

# Page furniture. Everything here is printed on the page and none of it is an
# ask: the running head and foot, the figure and scale captions the drawing
# carries, the section rubric, and the cover's instruction block.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate(?:\s+Examination)?\b'
    r'|Page\s+\d+\s+of\s+\d+\b'
    r'|Design\s*&\s*Comm'
    r'|\d{1,2}$'
    r'|N\.?B\.?:?\s*Scale\b|Scale\s*\d?\s*1\s*:\s*\d'
    r'|SECTION\s+[ABC]\b|Section\s+[ABC]\s*[-–]'
    r'|Section\s+[ABC]\s*$'
    r'|Answer\s+(?:any|one|Any)\b'
    r'|This examination\b|This document\b|Do not hand this up'
    r'|Examination\s+Number|Centre\s+No'
    r'|Coimisiún|State Examinations'
    r'|General Instructions|Construction lines must|The graphics presented'
    r'|Write the question number|Work on one side|All dimensions are given'
    r'|Write your Examination number|purposes\.?$'
    r'|There is no examination material'
    r'|Core\s*[-–]|Applied Graphics'
    r'|from this section on drawing paper'
    r')', re.I)

# The drawing's own caption, printed beside the graphic: "Fig. B-1", "Fig.
# C-4(a)". Furniture only where the whole line IS the label — "Fig. B-1 shows
# the plan and elevation of a similar studio desk" is the question telling the
# candidate what the drawing shows, and dropping it left eleven Section B
# stems opening mid-sentence with " of a similar studio desk."
FIG_LABEL = re.compile(r'^Fig\.?\s*[ABC]\s*[-‐-―]\s*\d\s*(?:\([a-z]\))?\s*$',
                       re.I)

# The SEC sets a specification as a bulleted list and the bullet arrives as
# its own drawing operation — sometimes glued to its line, sometimes a block
# of its own. Neither is furniture: "• the portion from A to C is level at an
# altitude of 60 m" is the ask's own data.
BULLET = re.compile(r'^[•\u2022\u25aa\u00b7\u2219]\s*')

# The five Applied Graphics options, printed as a banner on each Section C
# page. They are what a candidate CHOOSES between, so they are carried on the
# ask rather than dropped as furniture — the citation and the topic both need
# to say which option a card belongs to.
OPTIONS = {
    'geologic geometry': 'Geologic Geometry',
    'structural forms': 'Structural Forms',
    'surface geometry': 'Surface Geometry',
    'dynamic mechanisms': 'Dynamic Mechanisms',
    'assemblies': 'Assemblies',
}


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def rows(page):
    """Every printed line as (vy, vx, vx_end, text), in READING coordinates.

    A Section A sheet is drawn sideways: /Rotate 90 with text at dir (0,-1),
    so the line's x is its position DOWN the sheet and its y runs backwards
    ACROSS it. Undoing that here means one walker reads both booklets.
    """
    out = []
    for block in page.get_text('dict')['blocks']:
        if block['type'] != 0:
            continue
        for line in block['lines']:
            text = ''.join(s['text'] for s in line['spans']).strip()
            if not text:
                continue
            x0, y0, x1, y1 = line['bbox']
            direction = (round(line['dir'][0]), round(line['dir'][1]))
            if direction == (0, -1):
                out.append((x0, -y1, -y0, text))
            elif direction == (0, 1):
                out.append((-x1, y0, y1, text))
            else:
                out.append((y0, x0, x1, text))
    return sorted(out)


def _quadrants(page_rows, heads):
    """{marker -> [rows]} for a sheet that sets several questions side by side.

    The markers name the COLUMNS — Section A sets A-1 and A-2 down the left of
    the A3 sheet and A-3 and A-4 down the right — so a line belongs to the
    column whose marker it is nearest across the sheet, and inside that column
    to the last marker printed above it. Cutting on order alone interleaves
    the four questions; cutting on the column alone loses the row below.
    """
    anchors = sorted({round(vx) for _vy, vx, _vx2, _t in heads})
    merged = []
    for a in anchors:
        if merged and a - merged[-1] < 250:
            continue
        merged.append(a)
    owned = collections.defaultdict(list)
    for row in page_rows:
        vy, vx = row[0], row[1]
        col = min(merged, key=lambda a: abs(vx - a))
        above = [h for h in heads
                 if min(merged, key=lambda a: abs(h[1] - a)) == col
                 and h[0] <= vy + 3]
        if not above:
            continue
        owned[max(above)].append(row)
    return owned


def _banded(page_rows, tol=2.5):
    """Rows in reading order, with each printed BASELINE read across first."""
    out = []
    for row in sorted(page_rows):
        if out and abs(row[0] - out[-1][0][0]) <= tol:
            out[-1].append(row)
        else:
            out.append([row])
    return [row for band in out for row in sorted(band, key=lambda r: r[1])]


class Ask:
    """One leaf the paper prints, and the address the SEC prints for it."""

    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'stem', 'option',
                 'marks')

    def __init__(self, section, q, letter, roman, text, stem, option, marks):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.stem, self.option, self.marks = \
            text, stem, option, marks

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    @property
    def full_text(self):
        return self.text

    def __repr__(self):
        return f'<{self.section}-{self.q}({self.letter}){self.roman or ""}>'


class DcgPaper:
    """One sitting: the Section A booklet and the Sections B and C booklet."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.flags = []
        self.files = self._find_files()
        self.questions = {}          # (section, q) -> {'stem', 'option', 'parts'}
        self.section_marks = {}      # 'A' -> what one question there is worth
        self.covers = []             # the totals the two covers state
        self._read_covers()
        self._read()

    # ---------------------------------------------------------------- files
    def _find_files(self):
        found = sorted(glob.glob(os.path.join(
            papers_dir(self.subject),
            f'{self.year}-{self.level}-*-paper.pdf')))
        if len(found) != 2:
            raise FileNotFoundError(
                f'{self.subject} {self.year} {self.level}: '
                f'{len(found)} paper(s) on disk, expected two booklets')
        return found

    def _read_covers(self):
        """What the paper says a question is worth, from its own front page.

        Read rather than assumed. Hard-coded at 20/60/60 the reader was wrong
        about 2019, which prices Sections B and C at 45 marks a question and
        has a candidate answer TWO Applied Graphics options rather than one --
        the same 240 by a different route.
        """
        for path in self.files:
            doc = pymupdf.open(path)
            text = doc[0].get_text()
            doc.close()
            for m in SECTION_TARIFF.finditer(text):
                for token in (m.group(1), m.group(2)):
                    if token:
                        self.section_marks[token.upper()] = int(m.group(3))
            for m in COVER_TOTAL.finditer(text):
                self.covers.append(int(m.group(1)))
        missing = [s for s in SECTIONS if s not in self.section_marks]
        if missing:
            self.flags.append({
                'type': 'no-printed-tariff',
                'where': f'{self.year} {self.level}',
                'detail': 'neither cover states what a question of Section '
                          + ', '.join(missing) + ' is worth'})

    # ----------------------------------------------------------------- read
    def _read(self):
        by_section = collections.defaultdict(list)
        for path in self.files:
            doc = pymupdf.open(path)
            for page in doc:
                page_rows = rows(page)
                heads = [r for r in page_rows if QHEAD.match(r[3])]
                if not heads:
                    continue
                option = None
                for row in page_rows:
                    name = OPTIONS.get(row[3].strip().lower())
                    if name:
                        option = name
                if len(heads) == 1:
                    groups = {heads[0]: page_rows}
                else:
                    groups = _quadrants(page_rows, heads)
                for head, owned in groups.items():
                    m = QHEAD.match(head[3])
                    section, q = m.group(1), int(m.group(2))
                    body = self._body(head, owned)
                    by_section[section].append((q, body, option))
            doc.close()

        for section in SECTIONS:
            want = SECTION_SHAPE[section]
            marks = self.section_marks.get(section)
            seen = {}
            for q, body, option in by_section.get(section, []):
                if q in seen:
                    self.flags.append({
                        'type': 'duplicate-question',
                        'where': f'{self.year} {self.level} {section}-{q}',
                        'detail': 'the booklets print this address twice'})
                    continue
                seen[q] = (body, option)
            missing = [q for q in range(1, want + 1) if q not in seen]
            if missing:
                self.flags.append({
                    'type': 'question-gap',
                    'where': f'{self.year} {self.level} Section {section}',
                    'detail': f'no question head printed for '
                              f'{", ".join(f"{section}-{q}" for q in missing)}'})
            for q, (body, option) in sorted(seen.items()):
                stem, parts = self._split(body)
                self.questions[(section, q)] = {
                    'stem': stem, 'option': option, 'parts': parts,
                    'marks': marks}

    @staticmethod
    def _body(head, owned):
        """The question's own printed lines, head first and furniture gone.

        Rows are banded by BASELINE before they are ordered across the page.
        The SEC does not always set a part marker on its own text's baseline:
        2014 Ordinary C-3 puts "(a)" at y=187.74 and "Draw the given views."
        at y=187.31, four tenths of a point apart, and ordered by y alone the
        ask arrives BEFORE the marker that opens it -- so it lands in the
        question's stem and part (a) ships empty. The band is 2.5pt against a
        13pt line, so no two printed lines can share one.
        """
        lines = []
        for row in _banded(owned):
            text = ' '.join(row[3].split())
            if row == head:
                text = QHEAD.sub('', text).strip()
                if not text:
                    continue
            elif FURNITURE.match(text) or FIG_LABEL.match(text):
                continue
            text = BULLET.sub('', text).strip()
            if len(text) < 3:
                continue
            elif text.strip().lower() in OPTIONS:
                continue
            lines.append(text)
        return lines

    @staticmethod
    def _split(lines):
        """The stem, then {(letter, roman) -> text} in the order printed.

        A part marker OPENS a row — that is what separates "(a) Draw the given
        plan" from "the arc PA for (a) one complete revolution". A row may open
        two levels at once, "(c) (i) Determine the angle of inclination", which
        is the SEC's usual way of setting the first roman under a letter.
        """
        stem = []
        parts = []                       # [(letter, roman, [lines])]
        letter = roman = None
        for text in lines:
            m = PART.match(text)
            if m:
                letter, roman = m.group(1), None
                text = PART.sub('', text)
                r = ROMAN.match(text)
                if r:
                    roman = r.group(1)
                    text = ROMAN.sub('', text)
                parts.append((letter, roman, [text] if text else []))
                continue
            r = ROMAN.match(text)
            if r and letter is not None:
                roman = r.group(1)
                parts.append((letter, roman, [ROMAN.sub('', text)]))
                continue
            if parts:
                parts[-1][2].append(text)
            else:
                stem.append(text)
        out = []
        for lt, rm, body in parts:
            out.append((lt, rm, ' '.join(t for t in body if t).strip()))
        return ' '.join(stem).strip(), out

    # ----------------------------------------------------------------- asks
    @functools.lru_cache(maxsize=None)
    def asks(self):
        """Every LEAF the paper prints, in the SEC's own order."""
        out = []
        for (section, q), qq in sorted(self.questions.items()):
            parts = qq['parts']
            if not parts:
                out.append(Ask(section, q, None, None, qq['stem'], '',
                               qq['option'], qq['marks']))
                continue
            with_romans = {lt for lt, rm, _t in parts if rm}
            for lt, rm, text in parts:
                if rm is None and lt in with_romans:
                    continue          # a letter that opens romans is a parent
                out.append(Ask(section, q, lt, rm, text, qq['stem'],
                               qq['option'], qq['marks']))
        return tuple(out)

    def parent_text(self, section, q, letter):
        """A lettered parent's own words, for the romans printed under it."""
        for lt, rm, text in self.questions.get((section, q), {}).get('parts', []):
            if lt == letter and rm is None:
                return text
        return ''

    def cover_marks(self):
        """The total the two covers state between them, read not assumed.

        "Section A (60 marks)" on one booklet and "Section B and C (180
        marks)" on the other. The pair is printed on BOTH booklets in most
        years, so the distinct values are summed rather than the occurrences.
        """
        return sum(sorted(set(self.covers))) or 240


_LOADED = {}


def load(year, level, subject=SUBJECT):
    """One DcgPaper per sitting per process.

    Reading a DCG booklet means parsing a page of dense vector graphics for
    every line of text on it, and the census, the authoring pass and the
    figure worklist all want the same 33 sittings. Cached so the three make
    one pass rather than three.
    """
    key = (subject, year, level)
    if key not in _LOADED:
        _LOADED[key] = DcgPaper(year, level, subject)
    return _LOADED[key]


# The SAME markers, read a completely different way: a regex over the page's
# flat text, sharing no code with rows(), _quadrants() or _split(). Law 1 says
# the denominator may not be a product of the reader that produces the cards,
# so --audit reads it twice and the two have to agree.
FLAT_MARKER = re.compile(r'(?m)^\s*([ABC])\s*-\s*([1-9])\b')


def flat_questions(year, level, subject=SUBJECT):
    """{(section, q)} straight out of the raw text, no geometry involved."""
    out = set()
    for path in sorted(glob.glob(os.path.join(
            papers_dir(subject), f'{year}-{level}-*-paper.pdf'))):
        doc = pymupdf.open(path)
        for page in doc:
            for m in FLAT_MARKER.finditer(page.get_text()):
                out.add((m.group(1), int(m.group(2))))
        doc.close()
    return out


def audit(subject=SUBJECT):
    """Every sitting on disk, read, with the paper's own shape asserted."""
    seen = collections.defaultdict(set)
    for f in sorted(os.listdir(papers_dir(subject))):
        m = re.fullmatch(r'(\d{4})-(hl|ol)-[a-z0-9]+-paper\.pdf', f)
        if m:
            seen[int(m.group(1))].add(m.group(2))
    bad = 0
    for year in sorted(seen):
        for level in sorted(seen[year]):
            P = DcgPaper(year, level, subject)
            shape = collections.Counter(k[0] for k in P.questions)
            ok = all(shape[s] == SECTION_SHAPE[s] for s in SECTIONS)
            flat = flat_questions(year, level, subject)
            expected = {(sec, q) for sec, n in SECTION_SHAPE.items()
                        for q in range(1, n + 1)}
            ok = ok and flat == expected == set(P.questions)
            asks = P.asks()
            blank = [a.key for a in asks if len(a.text) < 12]
            first = min(sorted(P.questions))
            last = max(sorted(P.questions))
            line = (f'{year} {level}: {len(P.questions)} questions '
                    f'(A{shape["A"]} B{shape["B"]} C{shape["C"]}), '
                    f'first {first[0]}-{first[1]} last {last[0]}-{last[1]}, '
                    f'{len(flat)} by the flat-text reader, '
                    f'{len(asks)} leaf asks, '
                    f'A{P.section_marks.get("A")}/B{P.section_marks.get("B")}/'
                    f'C{P.section_marks.get("C")} marks a question, '
                    f'{P.cover_marks()} on the covers')
            if not ok or P.flags or blank:
                bad += 1
                line += '  <<<'
            print(line)
            for flag in P.flags:
                print(f'    FLAG {flag["type"]} {flag["where"]}: {flag["detail"]}')
            for key in blank:
                print(f'    SHORT {key}')
            if flat != set(P.questions):
                print('    READERS DISAGREE '
                      f'{sorted(flat ^ set(P.questions))}')
    print(f'{bad} sitting(s) with something to explain')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()
    if args.audit:
        return 0 if audit() == 0 else 1
    P = DcgPaper(args.year, args.level)
    for (section, q), qq in sorted(P.questions.items()):
        print(f'== {section}-{q} '
              f'{"[" + qq["option"] + "] " if qq["option"] else ""}'
              f'{qq["marks"]} marks')
        if qq['stem']:
            print(f'   stem: {qq["stem"][:300]}')
        for lt, rm, text in qq['parts']:
            print(f'   ({lt}){f"({rm})" if rm else ""} {text[:220]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
