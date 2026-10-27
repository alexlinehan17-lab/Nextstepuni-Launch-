#!/usr/bin/env python3
"""Lifting helpers for the Chemistry papers set in the PRINTED layout.

The 2026 papers (and the pre-2021 ones) are printed, not tabled: the paper
numbers its questions "1." with italic part markers "(a)" "(i)" down the left,
and the scheme REPRINTS each question in plain type with its answers in bold
beneath, the marks in square brackets at the right margin ("[5+2]") and the
examiner's asides in bold italic brackets ("[any two]"). chem_scheme.py reads
the five-column tables of 2021-2025 and does not apply here.

Both documents number their parts the same way, so one reader splits each into
parts keyed (question, letter, roman, alternative). A card's question text is
the PAPER's print of its part, cut where the scheme's reprint of the same part
ends, so the lead-in the paper sets before the next part ("The solvent was
removed by distillation.") is carried to that next part as context rather than
glued to this one. Its marking points are the scheme's bold lines, closed by
the mark cell on their row.

Every string a card shows comes out of one of the two PDFs through this module.
The super/subscripts Chemistry is written in are read from the baseline
(chem_scheme._script_text), so "Na₂CO₃" and "Co²⁺" stay what the SEC printed.
Nothing here types exam content.

    P = Printed(2026, 'hl')
    P.ask(('1', 'a', 'i', None))        # the paper's words for Q1(a)(i)
    P.items(('1', 'a', 'i', None))      # the scheme's answers, with their cells
"""
import collections
import json
import os
import re
import subprocess
import sys
import unicodedata

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chem_scheme import _script_text  # noqa: E402
from markbank_authoring import anyN, make_audit, make_card, make_emit, point, tidy  # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
PAPERS = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'chemistry', 'schemes')

# The 2021-2022 schemes set their footer as three runs: "Higher Level",
# "Chemistry 2022", "Page 5".
FOOTER = re.compile(r'^(Leaving Certificate( Examination)?,? 20\d\d|Chemistry\s*[–-]\s*(Higher|Ordinary) Level'
                    r'|Marking Scheme|\d{1,2}|Page \d{1,2}|(Higher|Ordinary) Level|Chemistry 20\d\d'
                    # The 2020 Ordinary scheme: "LC Ordinary Level Chemistry   8   2020".
                    r'|LC (Higher|Ordinary) Level Chemistry|20\d\d'
                    # 2017 OL: the paper's footer "Page 5 of 12" (y 782) and the scheme's
                    # "Page 3 of 16" (y 790) were read as text, welded onto the asks
                    # (Q4(k)B "... by mass. Page 5 of 12") and filed as answer items.
                    # Printed at the foot of the 2010-2017 papers and some of their
                    # schemes only; no sitting carded so far prints it.
                    r'|Page \d{1,2} of \d{1,2})\s*$')
# A mark cell at the scheme's right margin: "[2]", "[5+2]", "[6+2+2+2]", "[3×1 + 3]".
# The Ordinary scheme brackets a run of equal steps: "[12+10+(8×1)]".
# The 2023 Ordinary scheme sets the run in square brackets inside a round cell,
# "(6 + [6 × 3])"; as_cell() writes it the first way, "[6 + (6 × 3)]".
_TERM = (r'(?:\d{1,2}(?:\s*[×x]\s*\d{1,2})?|\(\s*\d{1,2}\s*[×x]\s*\d{1,2}\s*\)'
         r'|\[\s*\d{1,2}\s*[×x]\s*\d{1,2}\s*\])')
MARK_CELL = re.compile(r'^\[\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\]$')
ROUND_CELL = re.compile(r'^\(\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\)$')
TRAILING_ROUND = re.compile(r'\s+(\(\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\))$')
TRAILING_CELL = re.compile(r'\s*(\[\s*' + _TERM + r'(?:\s*\+\s*' + _TERM + r')*\s*\])$')


def as_cell(round_cell):
    """A round cell as the square one the reader keys on: "(2 × 3)" -> "[2 × 3]",
    "(6 + [6 × 3])" -> "[6 + (6 × 3)]"."""
    body = round_cell.strip()[1:-1]
    return '[' + re.sub(r'\[(\s*\d{1,2}\s*[×x]\s*\d{1,2}\s*)\]', r'(\1)', body) + ']'
# The examiner's aside in brackets: "[any two]", "[do not accept clear]".
ASIDE = re.compile(r'^\[[^\]]*[a-zA-Z]{3}[^\]]*\]$')
ANY = re.compile(r'^\[any (one|two|three|four|five|six)\]$', re.I)
EQUATION_ASIDE = re.compile(r'^\[formulae \((\d+)\), balancing \((\d+)\)\]$')
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
MAX_OPTIONS = 14


class Line:
    __slots__ = ('page', 'x0', 'y0', 'x1', 'y1', 'text', 'bold', 'math')

    def __init__(self, page, bbox, text, bold, math=False):
        self.page = page
        self.x0, self.y0, self.x1, self.y1 = bbox
        self.text, self.bold, self.math = text, bold, math

    def __repr__(self):
        return (f'<p{self.page} {self.x0:.0f},{self.y0:.0f}-{self.x1:.0f} '
                f'{"B" if self.bold else "-"} {self.text!r}>')


def _bold_share(ln):
    total = sum(len(s['text'].strip()) for s in ln['spans'])
    if not total:
        return 0.0
    bold = sum(len(s['text'].strip()) for s in ln['spans']
               if s['flags'] & 16 or 'Bold' in s['font'])
    return bold / total


_LIGATURES = None


def ligatures():
    """The bank's own ligature table (schemeText.mjs LIGATURES): the SEC's
    fonts set "tt" as one glyph that extracts as "Ʃ", so "plotted" reads
    "ploƩed". Read from the module, never retyped."""
    global _LIGATURES
    if _LIGATURES is None:
        js = "import(process.argv[1]).then(m => console.log(JSON.stringify(m.LIGATURES)))"
        url = 'file://' + os.path.join(ROOT, 'scripts', 'markbank', 'schemeText.mjs')
        _LIGATURES = json.loads(subprocess.run(['node', '--input-type=module', '-e', js, url],
                                               capture_output=True, text=True, check=True).stdout)
    return _LIGATURES


def _spaced(spans):
    """Keep the spaces a script run carries. _script_text reads a small span
    as a super/subscript and strips it, so "cm" + "3 " + "portions" came out
    "cm³portions", and a space set in a smaller size between "HCl" and
    "needed" vanished. A trailing space is split off into a span of the line's
    own size, and a space-only span is read as one space of that size."""
    if not spans:
        return spans
    base = max(sp['size'] for sp in spans)
    out = []
    for sp in spans:
        t = sp['text']
        if t and not t.strip():
            # A no-break space set as a span of its own ("represented",
            # "\xa0", "by") is a space: _script_text keeps only " ".
            out.append(dict(sp, text=' ', size=base))
        elif t != t.rstrip() and sp['size'] < base - 1.0:
            out.append(dict(sp, text=t.rstrip()))
            out.append(dict(sp, text=' ', size=base))
        else:
            out.append(sp)
    return out


# Calibri draws "tt" and "tti" as single ligature glyphs, ids 425 and 427
# (established bank-wide in #233 from 1,585 sightings, each repaired word
# cropped and read). Some text layers report them as U+01A9 / U+01AB, which
# the ligature table reads; others report gid 425 as a single "t" -- the 2024
# Ordinary scheme's "pipete". Read by glyph id, they are what the page draws.
CALIBRI_LIGATURES = {425: 'tt', 427: 'tti'}


def _ligature_origins(page):
    """{rounded glyph origin: 'tt' | 'tti'} for Calibri's ligature glyphs."""
    out = {}
    for tr in page.get_texttrace():
        if 'Calibri' not in tr.get('font', ''):
            continue
        chars = tr['chars']
        for i, ch in enumerate(chars):
            rep = CALIBRI_LIGATURES.get(ch[1])
            if not rep:
                continue
            # A layer that already spells the ligature out follows the glyph
            # with its other letters at the same origin, glyph id -1 ("t" 425,
            # "t" -1 is "tt" as printed): nothing to expand.
            nxt = chars[i + 1] if i + 1 < len(chars) else None
            if nxt and nxt[1] == -1 and abs(nxt[2][0] - ch[2][0]) < 0.05:
                continue
            out[(round(ch[2][0], 1), round(ch[2][1], 1))] = rep
    return out


def _span_texts(page):
    """page.get_text('dict') with each span's text rebuilt from its glyphs,
    Calibri's ligatures read by glyph id."""
    ligs = _ligature_origins(page)
    d = page.get_text('rawdict')
    for bl in d['blocks']:
        for ln in bl.get('lines', []):
            for sp in ln['spans']:
                sp['text'] = ''.join(
                    ligs.get((round(c['origin'][0], 1), round(c['origin'][1], 1)), c['c'])
                    if c['c'] in ('t', '\u01a9', '\u01ab') else c['c'] for c in sp['chars'])
    return d


def read_lines(path, first=1, last=None):
    """Every printed line, page by page, rows clustered then read left to right."""
    lig = ligatures()
    doc = fitz.open(path)
    out = []
    for pno in range(first, (last or doc.page_count) + 1):
        page = doc[pno - 1]
        cells = []
        for bl in _span_texts(page)['blocks']:
            for ln in bl.get('lines', []):
                # The equation font's digits are read as the digits they are
                # BEFORE the Maths demangler sees them: it collapses a doubled
                # maths character (a Maths-font quirk), which turned the
                # Chemistry scheme's "1000" into "10" and "26.55" into "26.5".
                ln = dict(ln, spans=_spaced([dict(sp, text=''.join(
                    unicodedata.normalize('NFKD', c) if 0x1D7CE <= ord(c) <= 0x1D7FF
                    else lig.get(c, c) for c in sp['text'])) for sp in ln['spans']]))
                text = ' '.join(_script_text(ln).split())
                # A full stop or comma set in the script's small size has no
                # script form; _script_text wraps it as "_(.)". Unwrap it.
                text = re.sub(r'[_^]\(([^0-9A-Za-z]+)\)', r'\1', text)
                if not text:
                    continue
                if ln['bbox'][1] > 765 and FOOTER.match(text):
                    continue
                # The schemes set worked arithmetic in an equation font, not in
                # bold: it is answer text all the same.
                math = any('Math' in sp['font'] for sp in ln['spans'] if sp['text'].strip())
                cells.append(Line(pno, ln['bbox'], text, _bold_share(ln) >= 0.6, math))
        # A printed row is not one y: a superscript starts higher than its
        # marker (chem_scheme._lines). Cluster at 5 points, then read across.
        cells.sort(key=lambda c: (c.y0, c.x0))
        row = []
        for c in cells:
            if row and c.y0 - row[0].y0 > 5.0:
                out.extend(sorted(row, key=lambda r: r.x0))
                row = []
            row.append(c)
        out.extend(sorted(row, key=lambda r: r.x0))
    return out


def _recluster(lines, pages):
    """Read the rows of `pages` across again, as read_lines does.

    read_lines clusters a page's lines into rows within 5 points of a row's
    first line. A figure's label can be that first line: on 2020 HL page 7 the
    table cell "pH at source" sits 4.6 points above "the OH- ion concentration
    of the source water.", drew it into its row, and left the "(ii)" printed
    beside it 5.6 points down to open the next row -- after its own words, so
    (d)(i) read both asks and (d)(ii) read the next lead-in. Once a page's
    figure lines are gone its rows are formed again from what remains; a page
    that lost nothing keeps its order exactly."""
    if not pages:
        return lines
    out, by_page, order = [], {}, []
    for l in lines:
        if l.page not in by_page:
            by_page[l.page] = []
            order.append(l.page)
        by_page[l.page].append(l)
    for page in order:
        cells = by_page[page]
        if page not in pages:
            out.extend(cells)
            continue
        cells = sorted(cells, key=lambda c: (c.y0, c.x0))
        row = []
        for c in cells:
            if row and c.y0 - row[0].y0 > 5.0:
                out.extend(sorted(row, key=lambda r: r.x0))
                row = []
            row.append(c)
        out.extend(sorted(row, key=lambda r: r.x0))
    return out


# ── splitting a document into its printed parts ─────────────────────────────
QNUM = re.compile(r'^(\d{1,2})\.?$')
HEADER = re.compile(r'^(Section [AB]|See page 1 for instructions.*'
                    r'|This question continues( on the next page)?\.?)$')
LETTER = re.compile(r'^\(([a-l])\)$')
ROMAN = re.compile(r'^\((i|ii|iii|iv|v|vi|vii|viii|ix|x)\)$')
ALTMARK = re.compile(r'^\(?([AB])\)?$')
PAPER_MARK = re.compile(r'^\((\d{1,2})\)$|^\(\d\s*×\s*\d{1,2}\)$')
TRAILING_MARK = re.compile(r'\s\((\d{1,2})\)$')
# "Answer part A or part B." -- some text layers drop the space ("Aor").
CHOICE_AB = re.compile(r'Answer part A\s*or part B')
LETTER_ALT = re.compile(r'^\(([a-l])\)\s*([AB])$')
LEAD_MARKER = re.compile(r'^(\([a-l]\)|\((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\))\s+(.+)$')
# An alternative's letter set in the same run as its reprint: "A Identify ...".
ALT_LEAD = re.compile(r'^([AB])\s+(\S.*)$')
# A question's number set in one run with its first letter: 2016 OL paper page 7
# prints "7. (a)" as one run (x 57, y 453), so no "7." head was read and Questions
# 7-11 fell into Q6(d)(ii) -- Q11(c)'s A and B became "Q6(d)A/B". The 2010-2013
# papers print the same run ("9. (a)", "5. (a) State two ..."); no carded sitting does.
QNUM_LETTER = re.compile(r'^(\d{1,2})\.\s+(\([a-l]\)(?:\s+\S.*)?)$')


def _split_markers(lines):
    """A line the PDF set as one run, "(c) (i) State Le Chatelier's principle.",
    read as its markers and its text, the way the page prints them."""
    alt_letter = None
    for l in lines:
        t = l.text
        qn = QNUM_LETTER.match(t)
        if qn and l.x0 < 70:
            # (2016 OL: "7. (a)" read as the head "7." and the letter "(a)".)
            yield Line(l.page, (l.x0, l.y0, l.x0 + 12, l.y1), qn.group(1) + '.', l.bold, l.math)
            l = Line(l.page, (l.x0 + 21, l.y0, l.x1, l.y1), qn.group(2), l.bold, l.math)
            t = l.text
        both = LETTER_ALT.match(t)
        if both and l.x0 < 100:
            # The 2025 Higher scheme sets "(d)A" as one run, and "(d)B" again
            # for the second alternative of the same letter: the letter is
            # read once, at its first alternative.
            if both.group(1) != alt_letter:
                yield Line(l.page, (l.x0, l.y0, l.x1, l.y1), f'({both.group(1)})', l.bold, l.math)
            alt_letter = both.group(1)
            yield Line(l.page, (l.x0 + 20, l.y0, l.x1, l.y1), f'({both.group(2)})', l.bold, l.math)
            continue
        m = LEAD_MARKER.match(t)
        # Romans sit at x 113 in the 2021-2026 papers: "(vii) are not involved
        # in bonding?" (2023 HL Q10(a)) opens its line with its marker.
        while m and l.x0 < 125:
            yield Line(l.page, (l.x0, l.y0, l.x1, l.y1), m.group(1), l.bold, l.math)
            t = m.group(2)
            m = LEAD_MARKER.match(t)
        tc = TRAILING_CELL.search(t)
        if tc and tc.start() > 0:
            # "pyramidal [12+10+(8×1)]": a mark cell the PDF set in the same
            # run as the answer before it.
            x0 = l.x0 + (28 if t != l.text else 0)
            split = x0 + (l.x1 - x0) * tc.start() / len(t)
            yield Line(l.page, (x0, l.y0, split, l.y1), t[:tc.start()], l.bold, l.math)
            yield Line(l.page, (max(split, 460), l.y0, l.x1, l.y1), tc.group(1).strip(), True)
            continue
        yield l if t == l.text else Line(l.page, (l.x0 + 28, l.y0, l.x1, l.y1), t, l.bold, l.math)


# A question's number set in one run with the first words of its lead-in: the
# 2013 OL paper prints "1. A sample of soap was prepared ..." (page 2, x 50, y 108),
# "2. A group of students ..." (page 3), "4. Answer eight ...", "6. Alkanes and
# alkenes ...", "8. Answer the questions ..." and "10."/"11. Answer any two ..."
# (pages 4-7) as one run each. QNUM wants the number alone and QNUM_LETTER a letter
# after it, so no "1." head was read and the paper reader found no question at all
# (its scheme, headed "QUESTION 1" ..., read all eleven). Read as the head and its
# words, the way the page prints them, for the sittings listed: 2013 OL. (The 2010
# and 2011 Ordinary papers print the same run; each joins by its own audit.)
OLD_OL_HEADS = {(2013, 'ol')}
QNUM_TEXT = re.compile(r'^(\d{1,2})\.\s+(\S.*)$')
# The same sittings' schemes print the running footer "Chemistry ATGL 2013" (2013 OL
# scheme, every page, y 789), dropped for them in Printed.
OLD_OL_FOOTER = re.compile(r'^Chemistry ATGL 20\d\d$')
# 2011 OL: the paper sets its heads the same way, "1. The two arrangements of apparatus
# ..." (page 2, x 50, y 100), "2. A 0.05 M standard solution ..." and "3. A student
# ..." (page 3), "4. Answer eight ..." (page 4), "6. Hydrogen ..." and "8. Answer the
# questions ..." (page 5), "10." and "11. Answer any two ..." (pages 6-7); unread, the
# paper reader found no question at all (its "5. (a)", "7. (a)" and "9. (a)" are
# QNUM_LETTER's). No other line of the 2011 Ordinary paper at x < 70 opens with a
# number and a full stop. The sitting joins split_heads' set. (Its scheme's footer
# reads "ATGL Chemistry 2011", which OLD_OL_FOOTER does not match; dropped in Printed,
# gated to 2011 OL.)
OLD_OL_HEADS.add((2011, 'ol'))


def split_heads(lines, year, lvl):
    """The paper's lines with a head set in one run with its words ("1. A sample
    ...") read as the head "1." and the words, for (year, lvl) in OLD_OL_HEADS
    (2013 OL); every other sitting's lines are returned as they are."""
    if (year, lvl) not in OLD_OL_HEADS:
        return lines
    out = []
    for l in lines:
        m = QNUM_TEXT.match(l.text)
        if m and l.x0 < 70 and not QNUM_LETTER.match(l.text):
            # (2013 OL: the words start at the lead-in's indent, x 72.)
            out.append(Line(l.page, (l.x0, l.y0, l.x0 + 12, l.y1), m.group(1) + '.', l.bold, l.math))
            out.append(Line(l.page, (l.x0 + 22, l.y0, l.x1, l.y1), m.group(2), l.bold, l.math))
        else:
            out.append(l)
    return out

# 2012 HL: the paper sets one head in one run with its words, "4. Answer eight of the
# following items (a), (b), (c), etc." (page 4, x 43, y 90); its other ten heads stand
# alone ("5.", page 4, x 43, y 472). Unread, the paper reader found Questions 1-3 only:
# Q4(a)-(e) were read as words of Q3(e), Q4(f)-(k) as Q3(f)-(k), and Questions 5-11 fell
# under Q3(k) and a phantom Q3(l). The sitting joins split_heads' set: no other line of the
# 2012 Higher paper at x < 70 opens with a number, a full stop and words.
OLD_OL_HEADS.add((2012, 'hl'))


# Parts the paper numbers wrongly, as (the key read, the marker printed).
MISPRINTED = []

# 2013 HL: the paper sets three of its heads in one run with their words, as the 2013
# Ordinary paper sets all of its own: "8. Study the reaction scheme and answer the
# questions that follow." (page 5, x 50, y 600), "10. Answer any two of the parts (a), (b)
# and (c)." (page 6, x 50, y 376) and "11. Answer any two ..." (page 7, x 50, y 42).
# Unread, the paper reader found Questions 1-7 only and filed Q8-Q11 under Q7(e). The
# sitting joins split_heads' set: no other line of the 2013 Higher paper at x < 70 opens
# with a number and a full stop. (Its scheme's footer reads "Chemistry ATAL 2013", which
# the Ordinary footer rule does not match; it is dropped in Printed, gated to 2013 HL.)
OLD_OL_HEADS.add((2013, 'hl'))
# 2013 HL paper page 7 sets Q11(c)'s choice as "Answer either part A or part B." (x 72,
# y 406). CHOICE_AB reads "Answer part A or part B.", so the bold "A" (x 87, y 425) and "B"
# (x 88, y 623) were read as words of Q11(c) and B's romans fell on A's: the census counted
# five asks, Q11(c)(i) "What is meant by electrolysis? (4) Distinguish between the terms
# feedstock ...", where the page prints nine. The letters listed are read as alternatives
# in the paper (segments' alt_letters). The 2011 Higher paper prints the same words, and
# joins by its own audit.
PAPER_ALT_LETTERS = {(2013, 'hl'): {('11', 'c')}}


# ── the labelled ("cue") scheme layout, 2010-2023 ───────────────────────────
# "QUESTION 2" heads a question; the letter, roman and the examiner's cue in
# capitals ("IDENTIFY:", "STATE and EXPLAIN:") open a row, then the answer, then
# the mark cell in the right margin, "(3)" or "ANY THREE: (3 × 3)". The question
# is not reprinted, so every line under a part that is not a marker is answer.
QUESTION_HEAD = re.compile(r'^QUESTION\s+(\d{1,2})\b\.?\s*$', re.I)
# The head of an "any two" question with its rubric set on the same line:
# "QUESTION 10: Answer any two of the parts (a), (b) and (c)." (2019 Ordinary
# scheme, PDF pages 14 and 16; the 2011, 2015-2018 Ordinary and 2013 Higher schemes
# print the same line). Read as the head alone: the rubric is the paper's own
# instruction, not an answer. Missed, every row of Q10 and Q11 fell into Q9(c).
QUESTION_HEAD_RUBRIC = re.compile(r'^QUESTION\s+(\d{1,2})\s*:\s*Answer any two of the parts '
                                  r'\(a\), \(b\) and \(c\)\.?\s*$')
CUE_WORD = r"[A-Z]{2,}[A-Z’']*"
CUE = re.compile(r'^(' + CUE_WORD + r'(?:\s+(?:and|or|&|' + CUE_WORD + r'))*)(?:,?\s*etc)?\s*:\s*')
TITLE_CUE = re.compile(r'^(Calculate|Explain|Name|State|Describe|Identify|Define|Write|Give|Draw|'
                       r'How|Why|What|Find|Show|List|Outline|Deduce|Distinguish)\s*:\s*')
ANY_CELL = re.compile(r'^ANY\s+(ONE|TWO|THREE|FOUR|FIVE|SIX)(?:\s+POINTS(?:\s+FROM\s+TABLE)?)?'
                      r'\s*:?\s*([\(\[].+[\)\]])\s*$', re.I)
# A cell the 2022 Ordinary scheme labels with its count of points: "SIX POINTS:
# [11 + 6 + 6 + 2 + 2 + 2]", "FOUR POINTS: (9 + 9 + 4 + 4)".
POINTS_CELL = re.compile(r'^(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)\s+POINTS\s*:\s*([\(\[].+[\)\]])\s*$')
# A cell the Ordinary schemes label with how many answers it counts: "FIRST SIX:
# (7 + (6 × 3))" beside 2019 Q10(a)'s seven words (PDF page 14), "FIRST FIVE:
# (5 × 5)" (2016). Read as the cell; the generator quotes the label.
FIRST_CELL = re.compile(r'^FIRST\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT)\s*:\s*([\(\[].+[\)\]])\s*$')


def any_bracket_cell(t):
    """A cell in round or square brackets, as the square cell the reader keys on."""
    t = t.strip()
    return as_cell('(' + t[1:-1].strip() + ')') if t.startswith('[') else as_cell(t)
LEAD_TOKEN = re.compile(r'^\(([a-l]|i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s*:?\s*')
OUTLINE_PAGE = re.compile(r'^Outline Marking Scheme', re.I)
# "BALANCING OF CORRECT FORMULAE: (3)" is the 2019 Ordinary scheme's Q4(e) (PDF page 8).
FORMULAE_CELL = re.compile(r'^(?:PRODUCT\s+)?FORMULAE:\s*\((\d{1,2})\)[,;]?\s*BALANC(?:ING|ED)'
                           r'(?:\s+OF\s+CORRECT\s+FORMULAE)?:?\s*\((\d{1,2})\)$')
# The 2016-2018 Ordinary schemes label the first part of an equation's price by
# what it marks: "PRODUCTS: (3), BALANCING: (3)" (2018 OL Q1(e)(iii), PDF page 5),
# "REACTANTS & PRODUCT: (3), BALANCING: (3)" (2018 OL Q4(d), page 9). Unread, the
# cue took "PRODUCTS:" off, the trailing "(3)" became the cell and "(3),
# BALANCING:" was welded onto the equation. Read as FORMULAE_CELL is, the aside
# quoting the scheme's own label.
PRODUCTS_CELL = re.compile(r'^((?:REACTANTS\s*&\s*)?PRODUCTS?):\s*\((\d{1,2})\),?\s*BALANCING:\s*'
                           r'\((\d{1,2})\)$')
ALT_BEFORE_CUE = re.compile(r'^([AB])\s+(?=(?:' + CUE_WORD + r')\s*:)')
# The rest of a cue the scheme wraps onto the rows below it, in the cue column
# ("SKETCH: (i)" over "& LABEL" over "ON GRAPH", 2022 HL Q3(d)).
CUE_TAIL = re.compile(r"&|(?:&\s*)?[A-Z]{2,}(?:\s+(?:&|[A-Z]{2,}))*:?")
# A cell the scheme labels with the number of parts it prices: "TWO PARTS :
# (2 × 2)" (2022 HL Q11(c)(i)).
PARTS_CELL = re.compile(r'^(TWO|THREE|FOUR)\s+(?:PARTS|BONDS)\s*:\s*(\(.+\))\s*$')
# A cell the 2020 Higher scheme labels with what it prices: "BALANCED EQUATION:
# (3)" beside the equation that Q6(d)(ii) asks for before its calculation.
LABEL_CELL = re.compile(r'^()(?:BALANCED\s+)?EQUATION\s*:\s*(\(\d{1,2}\))\s*$')
# A cell set between two answers on one row: "(3)" followed by more text.
MID_ROUND = re.compile(r'\s\((\d{1,2}(?:\s*[×x]\s*\d{1,2})?)\)\s+(?=\S)')


def is_cue_scheme(lines):
    return any(QUESTION_HEAD.match(l.text) for l in lines)


def cue_lines(lines):
    """A labelled scheme's lines rewritten into the shape segments() reads:
    question heads as "N.", markers and cues split off each row's start (the
    cue dropped: it restates the ask), "ANY THREE: (3 × 3)" as an aside and a
    cell, and a cell set at the end of an answer line split off as a cell.
    Where a row holds two answers each closed by its own cell ("water (H₂O)
    (3)   calcium carbide (CaC₂) (3)"), what follows the first cell is moved
    to a row of its own. The scheme's outline pages (the tariffs listed
    question by question) are left out: they are a summary, not the scheme."""
    outline = {l.page for l in lines if OUTLINE_PAGE.match(l.text)}
    margin = [(m.page, m.y0) for m in lines if m.x0 > 480
              and (ROUND_CELL.match(m.text.strip()) or MARK_CELL.match(m.text.strip()))]
    out = []
    zones = []                       # (page, y0, x): later text on this row starts a new row

    def shifted(l, x0=None):
        x = l.x0 if x0 is None else x0
        bump = sum(6.0 for pg, y, zx in zones if pg == l.page and abs(l.y0 - y) <= 5.0 and x >= zx)
        return (l.y0 + bump, l.y1 + bump)

    for l in lines:
        if l.page in outline:
            continue
        t = l.text
        m = QUESTION_HEAD.match(t) or QUESTION_HEAD_RUBRIC.match(t)
        if m:
            out.append(Line(l.page, (30, l.y0, 60, l.y1), m.group(1) + '.', True))
            continue
        m = ANY_CELL.match(t)
        if m and l.x0 > 350:
            y0, y1 = shifted(l)
            out.append(Line(l.page, (l.x0, y0, l.x0 + 60, y1), f'[any {m.group(1).lower()}]', False))
            out.append(Line(l.page, (max(l.x1 - 40, 481), y0, l.x1, y1),
                            any_bracket_cell(m.group(2)), True))
            continue
        m = POINTS_CELL.match(t) or FIRST_CELL.match(t)
        if m and l.x0 > 350:
            y0, y1 = shifted(l)
            out.append(Line(l.page, (max(l.x1 - 40, 481), y0, l.x1, y1),
                            any_bracket_cell(m.group(2)), True))
            continue
        m = PARTS_CELL.match(t) or LABEL_CELL.match(t)
        if m and l.x0 > 350:
            y0, y1 = shifted(l)
            out.append(Line(l.page, (max(l.x1 - 40, 481), y0, l.x1, y1), as_cell(m.group(2)), True))
            continue
        m = FORMULAE_CELL.match(t) or PRODUCTS_CELL.match(t)
        # (2019 OL Q4(e)'s longer label opens at x 342; no other scheme sets one left of 350.)
        if m and l.x0 > 300:
            # An equation priced in two parts: "FORMULAE: (3) BALANCING: (3)".
            # (2018 OL: PRODUCTS_CELL's labels take the same branch, the aside
            # quoting the label the scheme prints.)
            label = 'formulae' if m.re is FORMULAE_CELL else m.group(1).lower()
            first, second = m.groups()[-2:]
            y0, y1 = shifted(l)
            out.append(Line(l.page, (l.x0, y0, l.x0 + 60, y1), f'[{label} ({first}), balancing '
                                                                f'({second})]', False))
            out.append(Line(l.page, (max(l.x1 - 40, 481), y0, l.x1, y1),
                            f'[{first} + {second}]', True))
            continue
        if ROUND_CELL.match(t.strip()) and any(
                o.page == l.page and abs(o.y0 - l.y0) <= 5.0 and o.x1 <= l.x0 + 1
                and o.text.count('[') > o.text.count(']') for o in out[-3:]):
            # "[Allow" (3) "for increase concentration ...]": a cell quoted
            # inside an aside that the text layer splits into pieces.
            y0, y1 = shifted(l)
            out.append(Line(l.page, (l.x0, y0, l.x1, y1), t.strip(), l.bold, l.math))
            continue
        if ROUND_CELL.match(t.strip()):
            y0, y1 = shifted(l)
            out.append(Line(l.page, (max(l.x0, 481), y0, max(l.x1, 500), y1),
                            as_cell(t), True))
            if l.x0 < 350:
                zones.append((l.page, l.y0, l.x1))     # a cell mid-row: what follows is a new row
            continue
        if l.x0 < 132 and CUE_TAIL.fullmatch(t.strip()):
            continue                 # a cue wrapped in its column: "SKETCH: (i)" / "& LABEL" / "ON GRAPH"
        x = l.x0
        y0, y1 = shifted(l)
        while True:
            m = LEAD_TOKEN.match(t)
            if m:
                out.append(Line(l.page, (x, y0, x + 15, y1), f'({m.group(1)})', False))
                t, x = t[m.end():], x + 20
                continue
            m = CUE.match(t) or TITLE_CUE.match(t)
            if m:
                t, x = t[m.end():], x + 30
                continue
            m = ALT_BEFORE_CUE.match(t)
            if m:
                # "A WRITE: CaCO₃ + SO₂ → ...": an alternative's letter, then its cue.
                out.append(Line(l.page, (x, y0, x + 10, y1), m.group(1), False))
                t, x = t[m.end():], x + 14
                continue
            break
        t = t.strip()
        if not t:
            continue
        m = MID_ROUND.search(t)
        if m and t[:m.start()].rfind('[') > t[:m.start()].rfind(']'):
            # "[Allow (3) for ...]": a cell quoted inside an aside, whatever
            # aside closed before it ("blue to red.] [Allow (3) for", 2023 OL).
            m = None
        if m and (re.search(r'[=+\-–×÷*/]\s*$', t[:m.start()])
                  or re.match(r'\s*[=+\-–×÷*/]', t[m.end():])):
            # "Mr = (10 × 12) + 16 = 136" (2023 OL Q4(f)): arithmetic, not a cell.
            m = None
        if m and l.x0 < 350:
            out.append(Line(l.page, (x, y0, x + 100, y1), t[:m.start()].strip(), l.bold, l.math))
            out.append(Line(l.page, (481, y0, 500, y1), '[' + m.group(1) + ']', True))
            rest = t[m.end():].strip()
            if rest:
                rest_line = Line(l.page, (x + 120, y0 + 6, l.x1, y1 + 6), rest, l.bold, l.math)
                out.extend(cue_lines([rest_line]))
            zones.append((l.page, l.y0, l.x0 + 1))
            continue
        m = TRAILING_ROUND.search(t)
        if m and any(pg == l.page and abs(y - l.y0) <= 5.0 for pg, y in margin):
            m = None                 # the row's cell is at the margin: "F: 3.98 (4)" is the answer's
        if m and m.start() > 0:
            out.append(Line(l.page, (x, y0, l.x1 - 20, y1), t[:m.start()], l.bold, l.math))
            out.append(Line(l.page, (max(l.x1 - 20, 481), y0, l.x1, y1),
                            as_cell(m.group(1)), True))
            if l.x1 < 400:
                zones.append((l.page, l.y0, l.x1))
            continue
        out.append(Line(l.page, (x, y0, l.x1, y1), t, l.bold, l.math))
    return out


class Seg:
    """One printed part: everything from its marker up to the next marker.
    `marks_at` records, for a paper part, where in its text each printed mark
    fell: (number of text lines before it, the mark)."""
    __slots__ = ('key', 'marker', 'text', 'answers', 'tail', 'marks_at')

    def __init__(self, key, marker):
        self.key, self.marker = key, marker
        self.text, self.answers, self.tail, self.marks_at = [], [], [], []

    def lead_from(self):
        """Where the paper's lead-in for the NEXT part starts in this part's
        text, read from the page when no scheme reprint can say: after the
        part's last printed mark, or at the first line set back from the
        part's own indent (a lead-in sits at the letter's or question's
        indent, the ask at the part's)."""
        if not self.text:
            return None
        if self.marks_at:
            at = self.marks_at[-1][0]
            return at if at < len(self.text) else None
        indent = self.text[0].x0
        for i, l in enumerate(self.text[1:], 1):
            if l.x0 < indent - 10:
                return i
        return None

    def __repr__(self):
        return f'<Seg {self.key} {self.marker!r}>'


def _bare_choice(l, cur, queue):
    """2016 OL paper page 5: Q4(k) sets its alternatives as a bold "A" (x 113,
    y 626) and a bold "B" (x 113, y 665) with a bold "or" between them, and no
    "Answer part A or part B." above -- every other 2010-2026 paper prints that
    line -- so the choice went unread and the census counted one Q4(k). A bold
    "A" that opens its letter, followed before the next marker by a bold "or"
    and a bold "B" at the A's own indent, is that choice."""
    if l.text != 'A' or not l.bold or cur is None or not cur.key[1] or cur.key[2] \
            or cur.key[3] or cur.text:
        return False
    seen_or = False
    for m in queue:
        if LETTER.match(m.text) or ROMAN.match(m.text) or QNUM.match(m.text):
            return False
        if m.bold and m.text == 'or':
            seen_or = True
        elif seen_or and m.bold and m.text == 'B' and abs(m.x0 - l.x0) < 3:
            return True
    return False


def joined(lines):
    return tidy(' '.join(l.text for l in lines))


def segments(lines, first_q='1', answers=True, alt_letters=(), cue=False):
    """Split printed lines into parts keyed (q, letter, roman, alt).

    The PAPER and the SCHEME number parts the same way, so one reader serves
    both; only the scheme has answers (its bold lines and mark cells). The
    letter (i) and the roman (i) are told apart by what came before: (i)
    follows (h) only where it sits at the letters' own indent. A bare A or B is
    an alternative only inside a part that says "Answer part A or part B"; the
    scheme brackets its alternatives "(A)".
    `alt_letters` names the (question, letter) pairs the PAPER sets as
    alternatives: the 2025 Ordinary scheme heads Q11(d)'s alternatives "A" and
    "B" without printing "(d)", so an A there opens the next letter.
    Returns (ordered list of Seg, {(q, letter, None, None): printed marks}).
    """
    segs, marks = [], {}
    bare = set()                       # letters whose A/B choice prints no rubric (2016 OL)
    q = letter = roman = alt = None
    letter_x = None
    cur = None
    lines = list(_split_markers(lines))
    # A row of worked arithmetic set wholly in the equation font, priced by a
    # cell at its right, is an answer row although nothing on it is bold. A
    # numerator printed above a bold answer line is not: it stays out.
    math_rows = set()
    if answers:
        for l in lines:
            if not l.math:
                continue
            row = [m for m in lines if m.page == l.page and abs(m.y0 - l.y0) <= 5.0]
            words = [m for m in row if m.bold and not MARK_CELL.match(m.text)
                     and m.text.strip('/ ')]
            if any(MARK_CELL.match(m.text) for m in row) and not words:
                math_rows.add(id(l))
    queue = collections.deque(lines)
    while queue:
        l = queue.popleft()
        t = l.text
        if HEADER.match(t):
            continue
        ab = ALT_LEAD.match(t)
        if ab and answers and q is not None and not l.bold and l.x0 < 100 and (
                (q, letter) in alt_letters
                or (ab.group(1) == 'A' and (q, chr(ord(letter or '`') + 1)) in alt_letters)):
            # The 2024 schemes set an alternative's letter in the run of its
            # reprint: "(l) A Identify three chemical species ...", "B Outline
            # the contributions ...". Read as the marker, then the reprint.
            queue.appendleft(Line(l.page, (l.x0 + 14, l.y0, l.x1, l.y1), ab.group(2), l.bold, l.math))
            queue.appendleft(Line(l.page, (l.x0, l.y0, l.x0 + 10, l.y1), ab.group(1), l.bold, l.math))
            continue
        if not answers and t.startswith('There is no examination material on this page'):
            continue                 # a blank page's notice
        if not answers and t in ('Acknowledgements', 'Copyright notice'):
            break                    # the paper's back page: credits and copyright
        m = QNUM.match(t)
        if m and q is not None and m.group(1) == q and l.x0 < 40:
            continue        # the question's number again, heading a continuation page
        want = first_q if q is None else str(int(q) + 1)
        if m and l.x0 < 70 and m.group(1) == want \
                and (not answers or not l.bold or l.x0 < 40):
            q, letter, roman, alt = m.group(1), None, None, None
            cur = Seg((q, None, None, None), t)
            segs.append(cur)
            continue
        if q is None:
            continue
        am = ALTMARK.match(t)
        nxt_letter = chr(ord(letter or '`') + 1)
        if am and am.group(1) == 'A' and l.x0 < 100 and (q, letter) not in alt_letters \
                and (q, nxt_letter) in alt_letters:
            letter, roman, alt = nxt_letter, None, None
            segs.append(Seg((q, letter, None, None), f'({letter})'))
        if am and not answers and (_bare_choice(l, cur, queue) or (
                am.group(1) == 'B' and (q, letter) in bare and alt == 'A')):
            bare.add((q, letter))          # 2016 OL Q4(k): see _bare_choice
        if am and l.x0 < 150 and (t.startswith('(') or (q, letter) in alt_letters or (
                not answers and (q, letter) in bare) or any(
                CHOICE_AB.search(joined(sg.text))
                for sg in segs if sg.key[:2] == (q, letter))):
            alt, roman = am.group(1), None
            cur = Seg((q, letter, None, alt), t)
            segs.append(cur)
            continue
        # A bold letter at the left margin is still a part marker when it is
        # the next letter: the 2026 Ordinary scheme sets "(b)" of Q10 in bold.
        # A bold "(i)" there is an answer's own label (Q4's "(i) 27").
        nxt = LETTER.match(t)
        bold_letter = bool(answers and l.bold and nxt and l.x0 < 100 and not ROMAN.match(t)
                           and nxt.group(1) == chr(ord(letter or '`') + 1))
        if not (answers and l.bold) or bold_letter:
            pm = PAPER_MARK.match(t)
            # A part's mark sits at the right margin, or -- where a diagram
            # takes the right of the page -- at the end of the text column.
            if pm and (l.x0 > 400 or (not answers and l.x0 > 250)):
                if pm.group(1):
                    marks[(q, letter, None, None)] = int(pm.group(1))
                    if not answers and cur is not None:
                        cur.marks_at.append((len(cur.text), int(pm.group(1))))
                continue
            lm = LETTER.match(t)
            rm = ROMAN.match(t)
            is_letter = lm and (letter is None or lm.group(1) > letter) and (
                not rm or (letter == 'h' and letter_x is not None and abs(l.x0 - letter_x) < 4))
            if is_letter:
                letter, roman, alt, letter_x = lm.group(1), None, None, l.x0
                cur = Seg((q, letter, None, None), t)
                segs.append(cur)
                continue
            if rm:
                if not answers and rm.group(1) == roman and cur is not None \
                        and cur.key == (q, letter, roman, alt) and roman in ROMAN_ORDER[:-1]:
                    # The paper repeating the roman it is in is a misprint for
                    # the next one: 2024 HL Q2(c) prints "(ii)" twice, and the
                    # scheme marks the second (iii).
                    nxt_roman = ROMAN_ORDER[ROMAN_ORDER.index(roman) + 1]
                    MISPRINTED.append(((q, letter, nxt_roman, alt), t))
                    roman = nxt_roman
                    cur = Seg((q, letter, roman, alt), f'({roman})')
                    segs.append(cur)
                    continue
                roman = rm.group(1)
                again = [sg for sg in segs if sg.key == (q, letter, roman, alt)] if answers else []
                if again:
                    # The 2024 Higher scheme reprints Q4(h)'s "(i) during water
                    # treatment, (ii) during the tertiary stage ..." and then
                    # labels each answer with its roman again: "(i)
                    # flocculation (ii) to remove phosphates". A roman the
                    # letter has already opened is that part's answer label.
                    cur = again[0]
                    continue
                cur = Seg((q, letter, roman, alt), t)
                segs.append(cur)
                continue
        if answers and (cue or l.bold or MARK_CELL.match(t) or (l.math and id(l) in math_rows)):
            cur.answers.append(l)
        elif answers and cur.answers:
            cur.tail.append(l)
        else:
            tm = TRAILING_MARK.search(t)
            if tm and not answers:
                marks[(q, letter, None, None)] = int(tm.group(1))
                l = Line(l.page, (l.x0, l.y0, l.x1, l.y1), t[:tm.start()], l.bold)
            nxt_roman = (ROMAN_ORDER[ROMAN_ORDER.index(roman) + 1]
                         if not answers and roman in ROMAN_ORDER[:-1] else None)
            inline = re.search(r'[,;]\s+\((' + nxt_roman + r')\)\s+(?=\S)', l.text) if nxt_roman else None
            if inline:
                # The next roman set inside this one's line, continuing the run:
                # 2023 HL Q10(a) "... carbon to carbon bonding, (vii) are not
                # involved in bonding?"
                split = l.x0 + (l.x1 - l.x0) * inline.start() / max(len(l.text), 1)
                cur.text.append(Line(l.page, (l.x0, l.y0, split, l.y1), l.text[:inline.start() + 1],
                                     l.bold, l.math))
                roman = nxt_roman
                cur = Seg((q, letter, roman, alt), f'({roman})')
                segs.append(cur)
                cur.text.append(Line(l.page, (split, l.y0, l.x1, l.y1), l.text[inline.end():],
                                     l.bold, l.math))
                continue
            cur.text.append(l)
    return segs, marks


# ── matching the paper's words to the scheme's reprint ──────────────────────
_FOLD = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉', '01234567890123456789')
_DASHES = str.maketrans('—–−⁻₋⁺', '-----+')


def norm(t):
    """The provenance gate's normalise(), in Python: case, scripts and
    punctuation folded away, and the Mathematical Alphanumeric block the SEC
    sets stacked fractions in ("𝟎.𝟏𝟎") read as the digits it is
    (scripts/markbank/schemeText.mjs). A guide while authoring; the build's
    own gate is the judge."""
    t = ''.join(unicodedata.normalize('NFKD', c) if 0x1D400 <= ord(c) <= 0x1D7FF else c
                for c in t)
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', t.translate(_FOLD).lower())


def cut_to(text, target):
    """The shortest prefix of `text` whose normalised form is `target`'s.

    Returns (prefix, rest, exact). Where the reprint differs from the paper by
    a letter -- the paper prints "chorine", the scheme "chlorine" -- no prefix
    matches exactly; the cut then falls at the sentence end nearest the
    reprint's length and `exact` is False, for the caller to report.
    """
    want = norm(target)
    n, best = 0, None
    for i, ch in enumerate(text):
        n += len(norm(ch))
        if n == len(want) and norm(text[:i + 1]) == want:
            # Take the closing punctuation with it: the reprint's "flask." ends
            # where the paper's does, not one character short.
            j = i + 1
            while j < len(text) and not text[j].isspace() and text[j] != '(' \
                    and not norm(text[j]):
                j += 1
            return text[:j].strip(), text[j:].strip(), True
        if ch in '.?' and (best is None or abs(n - len(want)) < best[0]):
            best = (abs(n - len(want)), i)
    if best is None or best[0] > 4:
        return None, None, False
    i = best[1]
    return text[:i + 1].strip(), text[i + 1:].strip(), False


# What a diagram's label looks like when its text runs into the prose beside
# it: a number ("14", "(18)"), an orbital ("4p"), one capitalised word
# ("Energy"), or a letter or two ("X", "pH"). A formula, an arrow or a sign is
# never one -- dropping "HCl + NaOH → NaCl + H₂O" because the scheme sets the
# equation apart from its reprint of the lead-in would lose the equation.
LABEL = re.compile(r'^(\(?\d+(\.\d+)?\)?|\d[spdf]|[A-Z][a-z]{1,7}|[A-Za-z]{1,2})$')


def without_labels(text, target):
    """(ask, rest) when the paper's words, less some diagram labels, are
    exactly the reprint's; else None."""
    import difflib
    pw, want = text.split(), norm(target)
    sw = target.split()
    for j in range(1, len(pw) + 1):
        if len(norm(' '.join(pw[:j]))) < len(want):
            continue
        sm = difflib.SequenceMatcher(None, [norm(w) for w in pw[:j]], [norm(w) for w in sw],
                                     autojunk=False)
        drop, ok = set(), True
        for op, a1, a2, b1, b2 in sm.get_opcodes():
            if op == 'equal':
                continue
            if op == 'delete' and all(LABEL.match(w) for w in pw[a1:a2]):
                drop.update(range(a1, a2))
                continue
            ok = False
            break
        if not ok:
            continue
        kept = [w for i, w in enumerate(pw[:j]) if i not in drop]
        if norm(' '.join(kept)) == want:
            return ' '.join(kept), ' '.join(pw[j:])
    return None


def cut_at_tail(text, target, n=12):
    """(prefix, rest) of `text` ending where `target`'s last `n` normalised
    characters end in it, or (None, None)."""
    tail = norm(target)[-n:]
    if len(tail) < n:
        return None, None
    acc, end = '', None
    for i, ch in enumerate(text):
        acc += norm(ch)
        if acc.endswith(tail):
            end = i + 1
    if end is None:
        return None, None
    while end < len(text) and not text[end].isspace() and text[end] != '(' and not norm(text[end]):
        end += 1
    return text[:end].strip(), text[end:].strip()


# ── the scheme's answers ────────────────────────────────────────────────────
class PRow:
    """One printed row of a scheme answer: its words, mark cell and asides."""
    __slots__ = ('text', 'cell', 'asides', 'x1', 'page', 'y')

    def __init__(self, text, cell, asides, x1, page, y):
        self.text, self.cell, self.asides = text, cell, asides
        self.x1, self.page, self.y = x1, page, y

    def __repr__(self):
        return f'<PRow {self.text!r} {self.cell} {self.asides} x1={self.x1:.0f}>'


def prows(lines):
    """Answer lines grouped into the rows they print on, read left to right."""
    out, used = [], set()
    for l in lines:
        if id(l) in used:
            continue
        row = [m for m in lines if m.page == l.page and abs(m.y0 - l.y0) <= 5.0
               and id(m) not in used]
        for m in row:
            used.add(id(m))
        row.sort(key=lambda m: m.x0)
        words = [m for m in row if not MARK_CELL.match(m.text) and not ASIDE.match(m.text)]
        cell = next((m.text for m in row if MARK_CELL.match(m.text)), None)
        asides = [m.text for m in row if ASIDE.match(m.text)]
        out.append(PRow(tidy(' '.join(m.text for m in words)), cell, asides,
                        max((m.x1 for m in words), default=0.0), l.page, l.y0))
    return out


class Item:
    """The rows one mark cell closes."""
    __slots__ = ('rows', 'cell', 'asides')

    def __init__(self, rows, cell, asides):
        self.rows, self.cell, self.asides = rows, cell, asides

    @property
    def text(self):
        return tidy(' '.join(r.text for r in self.rows))

    def points(self, wrap_x=440):
        """The separately printed marking points in this item.

        A row ending "//" closes its point, as does a short row: the scheme sets
        each point on its own line. A row that runs on to the margin and has no
        "//" wraps into the next one.
        """
        pts, cur = [], []
        for r in self.rows:
            if not r.text:
                if r.asides and cur:
                    # An aside on a row of its own closes the point above it
                    # ("[Deduct 1 for brackets not square.]" between pH and Kw,
                    # 2022 HL Q9(a)).
                    pts.append(tidy(' '.join(cur)).rstrip('/ ').strip())
                    cur = []
                continue
            if not cur and pts and re.fullmatch(r'\([^()]*\)', r.text):
                # "(only)" on a row of its own qualifies the point above it.
                pts[-1] = tidy(pts[-1] + ' ' + r.text)
                continue
            cur.append(r.text)
            t = r.text.rstrip()
            # "ethyne is insoluble in water /" runs on: a single solidus at the
            # end of a row offers the next row as an alternative.
            if t.endswith('/') and not t.endswith('//'):
                continue
            if t.endswith(','):
                continue        # a list broken across rows: "..., rough titration,"

            sofar = ' '.join(cur)
            if sofar.count('[') > sofar.count(']'):
                # An aside begun at the end of an answer's row wraps onto the
                # next ("pH meter [Deduct 2 marks if indicator / named
                # indicator used instead of" / "universal indicator / pH
                # meter.]", 2023 OL Q7(d)(iii)): one point, its aside inline.
                continue
            if t.endswith('//') or r.x1 < wrap_x:
                pts.append(tidy(' '.join(cur)).rstrip('/ ').strip())
                cur = []
        if cur:
            pts.append(tidy(' '.join(cur)).rstrip('/ ').strip())
        return [p for p in pts if p]

    def options(self):
        """Every answer the scheme separates with //, across all its rows.

        A menu the scheme marks "[any two]" and sets on one line with single
        solidi and no "//" ("CH₄ / C₄H₁₀ / C₅H₁₂", 2025 OL Q6(b)(i)) lists its
        options with the single solidus: there the solidus cannot mean
        "equally acceptable wording of one answer", since the student is told
        to give two of them."""
        if '//' not in self.text and any(ANY.match(a) for a in self.asides):
            pts = self.points(wrap_x=500)
            if len(pts) > 1:
                # A menu printed one option to a row (2024 OL Q2(a)(ii)): each
                # row is an option, its single solidi alternative wordings. A
                # row runs on only when it reaches the text column's edge
                # (~520) or ends in a comma, not merely past 440.
                return pts
            if ' / ' not in self.text and ', ' in self.text:
                # "charging, melting, refining, tapping, casting [any three]"
                return [o.strip() for o in self.text.split(', ') if o.strip()]
            return [o.strip() for o in self.text.split(' / ') if o.strip()]
        return [o.strip() for o in self.text.split('//') if o.strip()]

    def __repr__(self):
        return f'<Item {self.text!r} {self.cell} {self.asides}>'


def _wrapped_asides(rows):
    """An aside the scheme sets on rows of its own and wraps ("[SKETCH marks
    are available if (d) (i) sketch is not on the graph in part (c) but labels"
    / "essential.]", 2022 HL Q3(d)(i)) is one aside: its rows are joined and,
    when the brackets close, carried as the row's aside rather than its words."""
    out, i = [], 0
    while i < len(rows):
        r = rows[i]
        t = r.text.strip()
        if t.startswith('[') and t.count('[') > t.count(']') and not r.cell:
            j, text = i, t
            while text.count('[') > text.count(']') and j + 1 < len(rows) \
                    and not rows[j + 1].cell and j - i < 4:
                j += 1
                text = tidy(text + ' ' + rows[j].text)
            if text.count('[') == text.count(']') and re.fullmatch(r'(\s*\[[^\[\]]*\]\.?)+\s*', text):
                out.append(PRow('', None, r.asides + [text], r.x1, r.page, r.y))
                i = j + 1
                continue
        out.append(r)
        i += 1
    return out


def items_of(lines):
    rows, out, cur, asides = _wrapped_asides(prows(lines)), [], [], []
    # "or" alone on a row between an alternative's last answer and the next
    # alternative is a separator, not an answer. Inside one answer -- two
    # wordings priced by the one cell below them, 2023 OL Q11(d)A(vi) -- it
    # stays, so the answer reads as the scheme prints it. Not where the answer
    # is "//" points, which the cards split on: there the "or" sets two sets of
    # points side by side (2023 HL Q11(a)(i)) and is the card's to state.
    for r in rows:
        if r.text.strip().lower() == 'or' and not r.cell and not r.asides:
            if cur and cur[-1].text and not any('//' in x.text for x in cur):
                cur.append(r)
            continue
        if not r.text and r.asides and not r.cell and not cur and out:
            out[-1].asides.extend(r.asides)
            continue
        cur.append(r)
        asides.extend(r.asides)
        if r.cell:
            out.append(Item(cur, r.cell, asides))
            cur, asides = [], []
    if cur or asides:
        out.append(Item(cur, None, asides))
    return out


def mark_value(cell):
    """The total a mark cell prints: "[5+2]" -> 7, "[3 × 3]" -> 9, "[3×1 + 3]" -> 6."""
    body = cell.strip('[] ')
    total = 0
    for term in re.split(r'\s*\+\s*', body):
        f = [int(n) for n in re.split(r'\s*[×x]\s*', term.strip('() '))]
        total += f[0] * (f[1] if len(f) > 1 else 1)
    return total


def mark_terms(cell):
    """"[5+2]" -> [5, 2]; "[2×3]" -> [3, 3]; "[3×1 + 3]" -> [1, 1, 1, 3]."""
    out = []
    for term in re.split(r'\s*\+\s*', cell.strip('[] ')):
        f = [int(n) for n in re.split(r'\s*[×x]\s*', term.strip('() '))]
        out += [f[1]] * f[0] if len(f) > 1 else [f[0]]
    return out


# Script letters with no Unicode subscript form, and the raised "o" the papers
# set for a degree sign. Display only: the provenance gate folds both away.
# A state symbol read half as subscript ("H₂O₍g)") is set as the plain
# bracket it is, and a raised exponent with no Unicode form ("10^(-2.8)") as
# a caret.
_SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
_SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
# Some papers (2025 Higher) set a negative charge or power with a raised em
# dash, which the text layer reads as "—": "MnO₄—", "A—", "10^(—14)",
# "mol^—1". It is the minus the page prints raised. A dash between two
# symbols ("the Cl—Cl bond") is a bond and stays.
DISPLAY = [(re.compile(r'\^(?:\([—–](\d+)\)|[—–](\d+)(?!\d|\.\d))'),
            lambda m: '⁻' + (m.group(1) or m.group(2)).translate(_SUP)),
           (re.compile(r'(?<=[A-Za-z₀-₉⁰-⁹⁺)*])—(?=[\s),.;:(]|$)'), '⁻'),
           # A subscript with a full stop set in its size: "NF_(3.)".
           (re.compile(r'_\((\d+)([.,])\)'), lambda m: m.group(1).translate(_SUB) + m.group(2)),
           (re.compile(r'_\(([a-zA-Z])\)'), r'\1'), (re.compile(r'\^\(o\)C'), '°C'),
           (re.compile(r'₍([a-z]{1,3})\)'), r'(\1)'), (re.compile(r'\^\(([^()\s]+)\)'), r'^\1'),
           # The text layer drops the space after a script run ("C₅H₁₂including",
           # "cm³portions"); the page prints one.
           (re.compile(r'([₀-₉⁰-⁹⁺⁻])([a-z]{2,})'), r'\1 \2'), (re.compile(r'\b(and)(\d)'), r'\1 \2')]


# The glyphs an SEC equation font maps into the wrong Unicode block ("ൌ" for
# "=", "ሺ" for "("). The repair is the bank's own (schemeText.mjs
# repairGlyphs), asked once per sitting for the characters it actually holds,
# never a second hand-made table.
BROKEN = re.compile(r'[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]')
REPAIR = {}


def learn_repairs(texts):
    chars = sorted({c for t in texts for c in t if BROKEN.match(c)} - set(REPAIR))
    if not chars:
        return
    js = ("import(process.argv[1]).then(m => { const cs = JSON.parse(process.argv[2]);"
          " console.log(JSON.stringify(cs.map(c => m.repairGlyphs(c)))); })")
    url = 'file://' + os.path.join(ROOT, 'scripts', 'markbank', 'schemeText.mjs')
    out = subprocess.run(['node', '--input-type=module', '-e', js, url, json.dumps(chars)],
                         capture_output=True, text=True, check=True).stdout
    for c, r in zip(chars, json.loads(out)):
        REPAIR[c] = r


# Two Symbol-font characters the shared glyph map does not carry, read by the
# font's own encoding (0xDE arrowdblright, 0xB4 multiply): the 2021-2022
# schemes print "⇒" in Symbol and the 2022 paper "(2 × 25)" in SymbolMT, and
# every one of them in the Chemistry corpus comes from those two fonts.
# 0xB5 (proportional) is SymbolMT's ∝ in the 2019 Ordinary scheme's Q4(b),
# "p ∝ 1/V / V ∝ 1/p" (PDF page 8), which the shared map reads as nothing.
SYMBOL_FONT = {'\uf0de': '⇒', '\uf0b4': '×', '\uf0b5': '∝'}


def display(t):
    t = ''.join(SYMBOL_FONT.get(c, c) for c in t)
    t = ''.join(REPAIR.get(c, c) for c in t)
    t = ''.join(unicodedata.normalize('NFKD', c) if 0x1D400 <= ord(c) <= 0x1D7FF else c for c in t)
    # The equation font spaces a decimal point from its digits: "26. 55".
    t = re.sub(r'(\d)\. (\d)', r'\1.\2', t)
    for rx, rep in DISPLAY:
        t = rx.sub(rep, t)
    return tidy(t)


class Printed:
    """One sitting in the printed layout: its paper and its scheme, split into parts."""

    def __init__(self, year, lvl, figures=False):
        self.year, self.lvl = year, lvl
        self.paper_path = os.path.join(PAPERS, f'{year}-{lvl}-paper.pdf')
        self.scheme_path = os.path.join(SCHEMES, f'{year}-{lvl}.pdf')
        # (2013 OL: a head set in one run with its words, split_heads.)
        self.paper_lines = split_heads(read_lines(self.paper_path), year, lvl)
        if (year, lvl) == (2012, 'hl'):
            # 2012 HL paper page 5 sets the state symbol "(l)" of the product Q6(a)(iii) draws in
            # full (2,2,4-trimethylpentane) as a run of its own after the structure's last "H"
            # (x 509, y 140). Read alone it is a letter marker: it opened a phantom Q6(l) after
            # (b), which took (b)'s second ask, (c), (d) and (e) with it. A state symbol, not a
            # part: dropped. No other line of the paper reads "(l)" alone.
            sym = [l for l in self.paper_lines if l.text == '(l)']
            assert len(sym) == 1 and sym[0].page == 5 and abs(sym[0].x0 - 508.9) < 1 \
                and abs(sym[0].y0 - 139.6) < 1, sym
            self.paper_lines = [l for l in self.paper_lines if l is not sym[0]]
        self.figures = figures
        if figures:
            self.paper_lines = self._outside_figures(self.paper_lines)
        self.scheme_lines = read_lines(self.scheme_path)
        if (year, lvl) == (2019, 'hl'):
            # 2019 HL scheme PDF page 29: a "(c)" at the letters' margin (x 49.6,
            # y 339.4) lies under the white fill of Q11(b)(ii)'s third working box;
            # the page prints no (c) there (Q11(c) opens on page 30 with its "A",
            # unlettered). Read as a marker it opened Q11(c) inside (b)(ii)'s
            # working and took (b)(iii) with it.
            hidden = [l for l in self.scheme_lines if l.page == 29 and l.text == '(c)'
                      and abs(l.x0 - 49.6) < 1 and abs(l.y0 - 339.4) < 1]
            assert len(hidden) == 1, hidden
            self.scheme_lines = [l for l in self.scheme_lines if l is not hidden[0]]
        if (year, lvl) == (2013, 'hl'):
            # 2013 HL scheme PDF page 3 (the Introduction) numbers its six notes "1."-"6."
            # at x 50 (y 136-467) in roman type; every other scheme sets them in bold,
            # which the reader passes over. Read as heads they opened Q1-Q6 before the
            # scheme's own "QUESTION 1" (page 5), which was then not the next number:
            # the rows of Questions 1-6 were all filed under Q6, and paper Q1-Q5 had no
            # scheme part. The notes are not marking; their numbers are dropped. The
            # running footer "Chemistry ATAL 2013" (every page, x 50, y 796) is not one
            # FOOTER reads, and in a labelled scheme every line is answer: it was filed
            # as an answer of each page's last part. Dropped too.
            notes = [l for l in self.scheme_lines if l.page == 3 and abs(l.x0 - 50) < 1
                     and not l.bold and QNUM.match(l.text)]
            assert [l.text for l in notes] == ['1.', '2.', '3.', '4.', '5.', '6.'], notes
            self.scheme_lines = [l for l in self.scheme_lines if l not in notes and not (
                l.y0 > 765 and l.text == 'Chemistry ATAL 2013')]
        if (year, lvl) == (2014, 'ol'):
            # 2014 OL scheme PDF page 15 heads Question 10 "QUESTION 10:" (x 56.6,
            # y 34.3), a colon after the number and its rubric on the line below
            # ("Answer any two of the parts (a), (b) and (c).", y 46.7). Neither
            # QUESTION_HEAD (no colon) nor QUESTION_HEAD_RUBRIC (the rubric on the
            # head's line) reads it, so Q10's rows fell into Q9(b) and, the next
            # head "QUESTION 11" then not being the next number, Q11's with them
            # (Q9(b)(i)-(iii), Q9(c)(i)-(v)). No other 2010-2026 scheme prints a
            # head of this shape. Read as the head the page prints.
            head = [l for l in self.scheme_lines if l.page == 15 and l.text == 'QUESTION 10:'
                    and abs(l.x0 - 56.6) < 1 and abs(l.y0 - 34.3) < 1]
            assert len(head) == 1, head
            head[0].text = 'QUESTION 10'
        if (year, lvl) == (2012, 'ol'):
            # 2012 OL scheme PDF page 8 prints Question 4's answers under "SECTION B"
            # (x 262, y 91.5) and the rubric "Eight items to be answered. ..." with no
            # "QUESTION 4" head; page 9 opens "QUESTION 5". Unread, Q4's items (a)-(k)
            # fell into Q3(e)-(k) and, "QUESTION 5" then not being the next number,
            # every later question with them. Section B opens with Question 4 on the
            # paper (page 4, "4. Answer eight of the following items"): read as its head.
            head = [l for l in self.scheme_lines if l.page == 8 and l.text == 'SECTION B'
                    and abs(l.x0 - 262.0) < 1 and abs(l.y0 - 91.5) < 1]
            assert len(head) == 1, head
            head[0].text = 'QUESTION 4'
            # Its running footer "Chemistry ATGL 2012 Marking Scheme Page 3of 15" (one run,
            # PDF pages 3-17, x 85.4, y 764.3) is not one FOOTER reads, and in a labelled
            # scheme every line is answer: it was filed as an answer of each page's last part.
            foot = re.compile(r'^Chemistry ATGL 2012 Marking Scheme Page \d{1,2}of 15$')
            assert sum(1 for l in self.scheme_lines if foot.match(l.text) and l.y0 > 760) == 15
            self.scheme_lines = [l for l in self.scheme_lines if not (l.y0 > 760 and foot.match(l.text))]
        if (year, lvl) == (2012, 'hl'):
            # 2012 HL scheme PDF pages 3-17 print the running footer "ATAL Chemistry 2012 –
            # Marking Scheme Page 3 of 15" as one run (x 65, y 731), which FOOTER does not read
            # (it drops runs below y 765 only); page 8 heads Section B "SECTION B" (x 234, y 44)
            # and page 17 opens "Question 11 continued/" (x 65, y 69). In a labelled scheme every
            # line is answer: each was filed as an answer of the part before it ("... Treat
            # answers not given to two decimal places as slips. ATAL Chemistry 2012 – Marking
            # Scheme Page 3 of 15", Q1(e)(ii)). None is marking; dropped.
            foot = re.compile(r'^ATAL Chemistry 2012 – Marking Scheme Page \d{1,2} of 15$')
            furniture = [l for l in self.scheme_lines if (l.y0 > 725 and foot.match(l.text)) or (
                l.page == 8 and l.text == 'SECTION B') or (l.page == 17 and l.text == 'Question 11 continued/')]
            assert len(furniture) == 17, furniture
            self.scheme_lines = [l for l in self.scheme_lines if not any(l is f for f in furniture)]
        if (year, lvl) == (2014, 'hl'):
            # 2014 HL scheme PDF pages 7 and 10 head Questions 2 and 4 "QUSESTION 2"
            # and "QUSESTION 4" (x 49.7, y 48.6), an SEC misprint; every other head of
            # this scheme is spelled "QUESTION". QUESTION_HEAD missed both, so the
            # scheme never left Question 1: Q2's rows were filed under Q1(a)-(g),
            # and "QUESTION 3" (not the next number) and every later head with them
            # (Q1(e)(i)-(ii), Q1(g)-(k) ...). No other 2010-2026 Chemistry scheme
            # prints the misspelling. Read as the heads the page means.
            for page, num in ((7, '2'), (10, '4')):
                head = [l for l in self.scheme_lines if l.page == page and l.text == 'QUSESTION ' + num
                        and abs(l.x0 - 49.7) < 1 and abs(l.y0 - 48.6) < 1]
                assert len(head) == 1, head
                head[0].text = 'QUESTION ' + num
        if (year, lvl) == (2011, 'ol'):
            # 2011 OL scheme PDF pages 3-15 print the running footer "ATGL Chemistry 2011",
            # "Marking Scheme", "Page 3 of 13" as three runs at y 761.5 (x 52, 257, 493-497).
            # FOOTER reads the last two only below y 765, and OLD_OL_FOOTER reads the 2013
            # wording ("Chemistry ATGL 2013"); in a labelled scheme every line is answer, so
            # all three were filed as an answer of each page's last part ("to prevent
            # bumping ... ATGL Chemistry 2011 Marking Scheme Page 3 of 13", Q1(d)). Dropped.
            foot = re.compile(r'^(ATGL Chemistry 2011|Marking Scheme|Page \d{1,2} of 13)$')
            assert sum(1 for l in self.scheme_lines if l.y0 > 755 and foot.match(l.text)) == 39
            self.scheme_lines = [l for l in self.scheme_lines if not (l.y0 > 755 and foot.match(l.text))]
        if (year, lvl) in OLD_OL_HEADS:
            # 2013 OL: the scheme's running footer "Chemistry ATGL 2013" (every page,
            # x 64, y 789; also the 2011 and 2012 Ordinary schemes', and no carded
            # sitting's) is not one FOOTER reads, and in a labelled scheme every
            # line is answer: it was filed as an answer of each page's last part.
            self.scheme_lines = [l for l in self.scheme_lines
                                 if not (l.y0 > 765 and OLD_OL_FOOTER.match(l.text))]
        if (year, lvl) == (2013, 'ol'):
            # 2013 OL scheme PDF page 5 sets Question 2's last answer under the cue
            # "FIND:" (x 85, y 477) with no "(f)": every other letter of the page
            # opens its row with its marker ("(e) OUTL:", x 64, y 327). The paper
            # prints (f) "Find, correct to two decimal places, ..." with (i) and
            # (ii); unread, the scheme filed its (i) and (ii) under (e). Read with
            # the letter the paper prints.
            find = [l for l in self.scheme_lines if l.page == 5 and l.text == 'FIND:'
                    and abs(l.x0 - 85) < 1 and abs(l.y0 - 477) < 1]
            assert len(find) == 1, find
            find[0].text = '(f) FIND:'
        if figures:
            self.scheme_lines = self._outside_scheme_art(self.scheme_lines)
        # The 2021-2025 schemes print their mark cells in round brackets,
        # "(3)", at the same right margin the 2026 schemes print "[3]" at.
        # Read there, and only there, they are the same cell.
        lines = []
        margin = [(m.page, m.y0) for m in self.scheme_lines
                  if m.x0 > 480 and ROUND_CELL.match(m.text)]
        for l in self.scheme_lines:
            if (l.x0 > 480 or l.bold) and ROUND_CELL.match(l.text):
                l.text = as_cell(l.text)
            elif l.bold and l.x0 < 480 and not any(
                    pg == l.page and abs(y - l.y0) <= 5.0 for pg, y in margin):
                # (Not where the row has its cell at the margin: then a bracket
                # ending the answer is the answer's, "F: 3.98 (4)", 2022 OL.)
                # Where a diagram takes the right margin the scheme sets the
                # cell at the end of the answer itself: "occupy singly (3)".
                m = TRAILING_ROUND.search(l.text)
                if m and m.start() > 0:
                    lines.append(Line(l.page, (l.x0, l.y0, l.x1 - 20, l.y1), l.text[:m.start()],
                                      l.bold, l.math))
                    l = Line(l.page, (max(l.x1 - 20, 481), l.y0, l.x1, l.y1),
                             as_cell(m.group(1)), True)
            lines.append(l)
        self.scheme_lines = lines
        # (2013 HL: Q11(c)'s alternatives under "Answer either part A or part B.",
        # PAPER_ALT_LETTERS.)
        self.pseg, self.marks = segments(self.paper_lines, answers=False,
                                         alt_letters=PAPER_ALT_LETTERS.get((year, lvl), ()))
        alt_letters = {s.key[:2] for s in self.pseg if s.key[3]}
        self.cue = is_cue_scheme(self.scheme_lines)
        if self.cue:
            self.scheme_lines = cue_lines(self.scheme_lines)
        self.sseg, _ = segments(self.scheme_lines, answers=True, alt_letters=alt_letters,
                                cue=self.cue)
        self.scheme_md = open(os.path.join(SCHEMES, f'{year}-{lvl}.md')).read()
        # The gate folds the SEC's ligature glyphs before it compares ("soŌ"
        # is "soft"); so does this guide to it.
        lig = ligatures()
        self.scheme_norm = norm(''.join(lig.get(c, c) for c in self.scheme_md))
        learn_repairs(l.text for l in self.paper_lines + self.scheme_lines)
        self.inexact = []

    def _outside_figures(self, lines):
        """The paper's lines less those printed inside a figure the card shows.

        A diagram's labels ("steam from a steam generator", a graph's axis
        numbers, "molten PbBr2") are part of its picture, not of the question's
        words; where the sitting's cropped paper figures cover them
        (chem_print_figures.CROPS), they are read as the picture's and left
        out of the asks and lead-ins. A part marker or a mark inside a crop
        means the rectangle is wrong, and stops the run."""
        from chem_print_figures import CROPS
        boxes = [(page, rect) for _n, src, page, rect in CROPS.get((self.year, self.lvl), [])
                 if src in ('paper', 'paper-image', 'labels')]
        kept, emptied = [], set()
        for l in lines:
            inside = any(l.page == page and l.x0 >= r[0] - 1 and l.y0 >= r[1] - 1
                         and l.x1 <= r[2] + 1 and l.y1 <= r[3] + 1 for page, r in boxes)
            if not inside:
                kept.append(l)
                continue
            emptied.add(l.page)
            if LETTER.match(l.text) or ROMAN.match(l.text) or PAPER_MARK.match(l.text) \
                    or (QNUM.match(l.text) and l.x0 < 70 and l.text.endswith('.')):
                # (A table's plain "1", a group number, is not a question's.)
                raise ValueError(f'a figure crop covers the marker {l.text!r} on page {l.page}')
        return _recluster(kept, emptied)

    def _outside_scheme_art(self, lines):
        """The scheme's lines less those inside a drawing it answers with.

        A drawn structure's atom symbols ("H", "C", "Cl") are text on the page,
        and read as text they are label soup filed as an answer. Where the
        sitting crops that drawing as the answer picture ('scheme-art') or marks
        its region ('scheme-labels', chem_print_figures.CROPS), the lines inside
        are the picture's. A mark cell or a part marker inside means the
        rectangle is wrong, and stops the run."""
        from chem_print_figures import CROPS
        boxes = [(page, rect) for _n, src, page, rect in CROPS.get((self.year, self.lvl), [])
                 if src in ('scheme-art', 'scheme-labels')]
        if not boxes:
            return lines
        kept = []
        for l in lines:
            inside = any(l.page == page and l.x0 >= r[0] - 1 and l.y0 >= r[1] - 1
                         and l.x1 <= r[2] + 1 and l.y1 <= r[3] + 1 for page, r in boxes)
            if not inside:
                kept.append(l)
            elif MARK_CELL.match(l.text) or ROUND_CELL.match(l.text) or LETTER.match(l.text) \
                    or ROMAN.match(l.text) or (QNUM.match(l.text) and l.x0 < 70):
                raise ValueError(f'a scheme drawing covers {l.text!r} on page {l.page}')
        return kept

    def rearranged(self, text, old, new):
        """`text` with `old` set as `new`, where `new` is the same printed
        characters in the order the page shows them -- a nuclide's mass and
        atomic numbers the text layer reads after its symbol ("Cr³⁺ 52 ion? 24"
        for the printed ⁵²₂₄Cr³⁺). Refused unless the characters are the same."""
        def chars(t):
            return sorted(re.sub(r'\s+', '', t.translate(_FOLD)).translate(_DASHES))
        if old not in text:
            raise ValueError(f'{old!r} is not in {text!r}')
        if chars(old) != chars(new):
            raise ValueError(f'{new!r} is not a rearrangement of {old!r}')
        return text.replace(old, new)

    # ── lookup ───────────────────────────────────────────────────────────
    def _one(self, segs, key, what):
        hits = [s for s in segs if s.key == key]
        if len(hits) != 1:
            raise KeyError(f'{what}: {len(hits)} parts keyed {key}')
        return hits[0]

    def pseg_of(self, key):
        return self._one(self.pseg, key, 'paper')

    def sseg_of(self, key):
        return self._one(self.sseg, key, 'scheme')

    @staticmethod
    def _below(segs, key):
        """The part `key` and every part printed under it."""
        q, letter, roman, alt = key
        out = []
        for s in segs:
            k = s.key
            if k[0] != q or (letter and k[1] != letter) or (roman and k[2] != roman) \
                    or (alt and k[3] != alt):
                continue
            out.append(s)
        return out

    # ── the paper ────────────────────────────────────────────────────────
    def _split(self, key):
        """(the paper's ask for this part, the lead-in it prints after it)."""
        seg = self.pseg_of(key)
        p = joined(seg.text)
        try:
            s = joined(self.sseg_of(key).text)
        except KeyError:
            s = ''
        if not s:
            text = list(seg.text)
            if self.cue and text and text[-1].text.strip() == 'or':
                text = text[:-1]          # the "or" between alternatives A and B
            at = seg.lead_from() if self.cue else None
            if at and at < len(text):
                return joined(text[:at]), joined(text[at:])
            return joined(text), ''
        ask, rest, exact = cut_to(p, s)
        if not exact:
            # A diagram set beside the ask puts its labels into the ask's
            # lines ("Draw the shape of the atomic 4p orbital ... in a 3d
            # bromine atom"). Where dropping a few short words from the paper
            # leaves exactly the scheme's reprint, those words were the
            # diagram's, and the ask is the paper's own remaining words.
            got = without_labels(p, s)
            if got:
                ask, rest, exact = got[0], got[1], True
        if ask is None:
            # The reprint words the part differently ("Name two" for the
            # paper's "Identify two"): end the ask where the reprint's last
            # words fall in the paper.
            ask, rest = cut_at_tail(p, s)
            exact = False
        if ask is None and norm(s).startswith(norm(p)):
            # The scheme reprints a part's sub-parts inline ("Name the scientist
            # who determined (i) ..."); the paper sets them as parts of their own.
            return p, ''
        if ask is None:
            raise ValueError(f'{key}: the paper and the scheme reprint disagree\n  P: {p}\n  S: {s}')
        if not exact:
            self.inexact.append((key, ask, s))
        return ask, rest

    def ask(self, key, deep=False, upto=None):
        """The paper's words for a part. `deep` takes the parts printed under
        it too, with their markers -- a Q4 item asks "(i) ..., (ii) ..." in one."""
        if not deep:
            text = self._split(key)[0]
        else:
            parts = []
            for s in self._below(self.pseg, key):
                t = self._split(s.key)[0]
                parts.append(t if s.key == key else f'{s.marker} {t}')
            text = tidy(' '.join(parts))
        if upto is not None:
            text = text[:text.index(upto) + len(upto)]
        return display(text)

    def lead(self, key):
        """What the paper prints after a part's ask and before the next part.

        A diagram beside the asks leaves its labels here too ("4s", "Energy",
        a graph's axis numbers). Where the scheme reprints the lead-in, the
        paper's words are kept only as far as they are the reprint's (less
        such labels); where it does not, a run with no sentence in it is a
        diagram's labels and is no lead-in."""
        rest = self._split(key)[1]
        try:
            tail = joined(self.sseg_of(key).tail)
        except KeyError:
            tail = ''
        if rest and tail:
            got = without_labels(rest, tail)
            if got:
                return display(got[0])
        if rest and not self.figures and not re.search(r'[A-Za-z]{3,}[^.?:]*\b\w+[.?:]', rest):
            # Without the sitting's figure rectangles, a run with no sentence
            # in it is read as a diagram's labels. With them, the labels are
            # already gone and such a run is an equation the paper prints.
            return ''
        return display(rest)

    def text(self, key, upto=None, drop=()):
        """A part's own printed text (a question's or a letter's lead-in)."""
        t = joined(self.pseg_of(key).text)
        if upto is not None:
            t = t[:t.index(upto) + len(upto)]
        for d in drop:
            if d not in t:
                raise ValueError(f'{key}: {d!r} is not in its text')
            t = t.replace(d, ' ')
        return display(t)

    # ── the scheme ───────────────────────────────────────────────────────
    def items(self, key, deep=False):
        segs = self._below(self.sseg, key) if deep else [self.sseg_of(key)]
        return items_of([l for s in segs for l in s.answers])

    def traceable(self, claim):
        """Found in the scheme by the gate's own rule (schemeText.claimMatches):
        normalised, then -- for a font that prints the tt ligature as one t
        ("pipete") -- with tt collapsed on both sides."""
        c = norm(claim)
        if c in self.scheme_norm:
            return True
        if not hasattr(self, '_collapsed'):
            self._collapsed = self.scheme_norm.replace('tt', 't')
        if c.replace('tt', 't') in self._collapsed:
            return True
        return self._gate(claim)

    def _gate(self, claim):
        """Ask the build's own rule (schemeText.claimMatches over every form it
        compares, the equation font's doubled letters among them), for a claim
        this module's forms miss. Cached."""
        cache = self.__dict__.setdefault('_gate_cache', {})
        if claim not in cache:
            js = ("import fs from 'node:fs'; const m = await import(process.argv[1]);"
                  " const md = m.comparableScheme(fs.readFileSync(process.argv[2], 'utf8'));"
                  " console.log(m.claimMatches(md, process.argv[3]) ? 'yes' : 'no');")
            url = 'file://' + os.path.join(ROOT, 'scripts', 'markbank', 'schemeText.mjs')
            md = os.path.join(SCHEMES, f'{self.year}-{self.lvl}.md')
            out = subprocess.run(['node', '--input-type=module', '-e', js, url, md, claim],
                                 capture_output=True, text=True, check=True).stdout.strip()
            cache[claim] = out == 'yes'
        return cache[claim]


__all__ = ['Printed', 'Item', 'PRow', 'segments', 'items_of', 'prows', 'joined', 'norm',
           'cut_to', 'display', 'mark_value', 'mark_terms', 'anyN', 'point', 'make_audit',
           'make_card', 'make_emit', 'tidy', 'MARK_CELL', 'ASIDE', 'ANY', 'WORDS', 'MAX_OPTIONS',
           'Line', 'Seg', 'read_lines']


# ── cards ───────────────────────────────────────────────────────────────────
# The commit the Chemistry audit started from: origin/main when the worktree
# was cut. Every pre-audit card is read from here, never from the working
# deck, so a re-run compares against the same thing every time.
AUDIT_BASE = 'e7ec7a532de3c03f8511d416cf943354dfe3e74e'
_PRIOR = None


def prior_deck():
    global _PRIOR
    if _PRIOR is None:
        raw = subprocess.run(['git', 'show', f'{AUDIT_BASE}:scripts/markbank/authored/chemistry.json'],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        _PRIOR = {c['id']: c for c in json.loads(raw)}
    return _PRIOR


def prior_card(cid):
    return prior_deck().get(cid)

_LETTER_SCRIPTS = str.maketrans('ₙⁿₘᵐₓˣ', 'nnmmxx')
# An examiner's aside is wording ("[do not accept clear]", "[state/imply]"); a
# concentration term is not ("[PCl₃]", "[NOBr]"): it has no run of three
# lower-case letters. Nor is a bracket set hard against the symbol before it:
# "pH = –log√Ka[acid]" (2022 HL Q9(d)(iii)) is a concentration, whatever its
# letters; an aside follows a space or opens the text.
INLINE_ASIDE = re.compile(r'(?:(?<=\s)|(?<=^)|(?<=[.;:,)]))\s*(\[[^\]]*[a-z]{3}[^\]]*\])')
ROMAN_ORDER = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']


class Refused(Exception):
    pass


def _asides_note(asides):
    asides = [a for a in asides if not ANY.match(a)]
    return ('The scheme adds: ' + ' '.join(asides)) if asides else ''


class Cards:
    """The cards one printed sitting yields, and the parts it leaves open."""

    def __init__(self, P):
        self.P = P
        self.cards, self.open = [], []
        self.level = 'higher' if P.lvl == 'hl' else 'ordinary'
        self.prefix = f'chem-{P.year}-{P.lvl}-'
        self._card = make_card('chemistry')
        self._fixes_used = set()
        # Carry a lead-in printed after one letter into the next letter's
        # context. Off for the sittings carded before it existed.
        self.letter_leads = (P.year, P.lvl) not in {(2025, 'hl'), (2025, 'ol'), (2026, 'hl'),
                                                     (2026, 'ol')}

    def _fixes_applied(self, keys, fixes):
        """A fix is keyed by the reader's own text; if the reader changes, a
        fix that no longer matches would silently stop applying. Refuse it."""
        unused = set(fixes or {}) - self._fixes_used
        self._fixes_used = set()
        if unused:
            raise Refused(f'{keys}: fixes matched nothing: {sorted(unused)}')

    # ── naming ───────────────────────────────────────────────────────────
    @staticmethod
    def label(key):
        q, letter, roman, alt = key
        return (f'({letter})' if letter else '') + (alt or '') + (f'({roman})' if roman else '')

    def ref(self, keys):
        first, last = keys[0], keys[-1]
        r = f'{self.P.year} {self.P.lvl.upper()} Q{first[0]}{self.label(first)}'
        if last != first:
            r += '–' + (f'({last[2]})' if last[:2] == first[:2] and last[3] == first[3]
                        else self.label(last))
        return r

    @staticmethod
    def slug(key):
        q, letter, roman, alt = key
        return '-'.join(p for p in (f'q{q}', letter, alt and alt.lower(), roman) if p)

    def cid(self, keys):
        c = self.slug(keys[0])
        if keys[-1] != keys[0]:
            c += '-' + (keys[-1][2] or self.slug(keys[-1]))
        return c

    # ── text ─────────────────────────────────────────────────────────────
    def context(self, key, heads=True):
        """The paper's lead-ins above a part: its question's, its letter's, its
        alternative's, and any the paper prints between earlier parts. An
        instruction ("Answer part A or part B.") is not context and is left out;
        so is anything the paper prints after a lead-in's last sentence that the
        scheme does not reprint -- a diagram's labels."""
        P = self.P
        q, letter, roman, alt = key
        above = [(q, None, None, None)]
        if letter and (roman or alt):
            above.append((q, letter, None, None))
        if alt and roman:
            above.append((q, letter, None, alt))
        out = []
        prev_lead = self._previous_letter_lead(key) if heads else ''
        for k in (above if heads else []):
            if k == (q, letter, None, None) and prev_lead:
                # What the paper prints after the previous letter's last part
                # and before this letter opens is this letter's lead-in:
                # 2024 HL Q8 sets "Reaction B takes place in the presence of
                # chlorine (Cl₂) gas and ultraviolet light." after (a).
                out.append(prev_lead)
            try:
                t = P.ask(k)
            except KeyError:
                continue
            if t and not t.startswith('Answer '):
                out.append(t)
            # What the paper prints after a lead-in and before the first part
            # under it -- an equation the scheme sets in bold, so its reprint
            # ends at "the following balanced chemical equation:" -- is the
            # lead-in's still.
            lead = P.lead(k) if k != key else ''
            if lead and lead != 'or':
                out.append(lead)
        if roman:
            for r in ROMAN_ORDER[:ROMAN_ORDER.index(roman)]:
                try:
                    lead = P.lead((q, letter, r, alt))
                except KeyError:
                    continue
                if lead and lead != 'or':
                    out.append(lead)
        return tidy(' '.join(out))

    def _previous_letter_lead(self, key):
        q, letter, roman, alt = key
        if not letter or alt or not self.letter_leads or q == '4':
            return ''            # Q4's items stand alone: one's sentence is no other's lead
        letters = [s.key[1] for s in self.P.pseg if s.key[0] == q and s.key[1]]
        before = [x for x in dict.fromkeys(letters) if x < letter]
        if not before:
            return ''
        prev = before[-1]
        last = [s.key for s in self.P.pseg if s.key[0] == q and s.key[1] == prev and not s.key[3]]
        if not last:
            return ''
        try:
            lead = self.P.lead(last[-1])
        except KeyError:
            return ''
        return '' if lead in ('', 'or') else lead

    def qtext(self, keys, deep=False):
        """One part's ask, or several parts' asks with their printed markers
        and any lead-in the paper sets between them."""
        if len(keys) == 1:
            return self.P.ask(keys[0], deep=deep)
        out = []
        for i, k in enumerate(keys):
            out.append(f'({k[2]}) {self.P.ask(k)}')
            lead = self.P.lead(k) if i < len(keys) - 1 else ''
            if lead and lead != 'or':
                out.append(lead)
        return tidy(' '.join(out))

    # ── rows ─────────────────────────────────────────────────────────────
    def _verbatim(self, text, fixes, where):
        notes = INLINE_ASIDE.findall(text)
        text = tidy(INLINE_ASIDE.sub('', text))
        for k in (text, display(text)):
            if k in fixes:
                self._fixes_used.add(k)
                text = fixes[k]
                break
        shown = display(text)
        if self.P.traceable(shown):
            text = shown
        elif self.P.traceable(shown.translate(_LETTER_SCRIPTS)):
            # A letter set as a script ("Eₙ") has no plain form the gate folds;
            # the scheme's own text carries it on the line ("Em – En = hf").
            text = shown.translate(_LETTER_SCRIPTS)
        if not self.P.traceable(text):
            raise Refused(f'{where}: "{text}" is not in the {self.P.year} {self.P.lvl} scheme')
        return text, notes

    def points(self, key, fixes=None, notes=None, deep=False, skip=(), each=False, tail=False):
        """One fixed row per mark cell, worth what the cell prints. An item in
        `skip` is a line the scheme sets among the answers that answers
        nothing -- a reprint of the paper's next equation -- and is left out.
        With `each`, a cell "[n × m]" closing n separately printed points
        ("A: 2,2-dichlorobutane", "B: propan-2-ol", ...) is n rows of m."""
        fixes, notes = fixes or {}, notes or {}
        rows, skipped = [], set()
        for it in self.P.items(key, deep=deep):
            if it.cell is None and display(it.text) in skip:
                skipped.add(display(it.text))
                continue
            if it.cell is None and rows and re.fullmatch(
                    r'(or\s+)?(\s*\[[^\[\]]*(\[[^\]]*\][^\[\]]*)*\]\.?)+\s*', it.text):
                # A bracketed line under the last cell: the scheme's own
                # aside, such as the whole balanced equation after its parts,
                # or two of them on one line ("[award 3 marks if reversed]
                # [allow 3 marks for condensation]").
                rows[-1]['contextNote'] = tidy(rows[-1].get('contextNote', '') +
                                               ' The scheme adds: ' + it.text)
                continue
            if it.cell is None and rows and tail:
                # An examiner's instruction set as prose after the last cell
                # ("Where 6 marks not awarded above 5 marks may be awarded any
                # one of the following. ...", 2022 HL Q4(c)): it rides on the
                # row above, quoted.
                rows[-1]['contextNote'] = tidy(' '.join(x for x in [
                    rows[-1].get('contextNote', ''), _asides_note(it.asides),
                    'The scheme adds: "' + display(it.text).lstrip('/ ') + '"'] if x))
                continue
            if it.cell is None:
                raise Refused(f'{key}: "{it.text}" has no mark cell of its own')
            # (The products / reactants & product asides: 2018 OL, PRODUCTS_CELL.)
            equation = any(a.startswith(('[formulae', '[products (', '[product (',
                                         '[reactants & product')) for a in it.asides)
            if '+' in it.cell and not re.search(r'×', it.cell) and not equation:
                raise Refused(f'{key}: {it.cell} is a split, not a fixed point')
            # An equation priced "FORMULAE: (2) BALANCING: (2)" is one point, the
            # equation, worth the two together; its aside says how they split.
            terms = mark_terms(it.cell)
            pts = it.points()
            if each and len(pts) != len(terms) and len(it.text.split('//')) == len(terms):
                # "protons // two" on one row, priced (2 × 3) (2023 OL Q4(c)).
                pts = [x.strip() for x in it.text.split('//')]
            if each and '+' not in it.cell and len(terms) > 1 and len(pts) == len(terms):
                for j, ptext in enumerate(pts):
                    text, inline = self._verbatim(ptext, fixes, key)
                    note = ' '.join(x for x in [
                        _asides_note(inline + (it.asides if j == len(pts) - 1 else [])),
                        f'The scheme prices these points {it.cell}, one each.' if j == 0 else '',
                        notes.get(len(rows), '')] if x)
                    rows.append(point(f'r-{len(rows) + 1}', text, terms[j], note))
                continue
            # A trailing solidus offers an alternative the scheme never printed
            # ("higher yield methanol / more methanol /", 2022 HL Q7(d)(ii)).
            text, inline = self._verbatim(re.sub(r'(\s*/)+\s*$', '', it.text), fixes, key)
            note = ' '.join(x for x in [_asides_note(inline + it.asides),
                                        f'The scheme prices this point {it.cell}.'
                                        if mark_value(it.cell) != mark_terms(it.cell)[0] else '',
                                        notes.get(len(rows), '')] if x)
            rows.append(point(f'r-{len(rows) + 1}', text, mark_value(it.cell), note))
        if set(skip) - skipped:
            raise Refused(f'{key}: nothing to skip for {sorted(set(skip) - skipped)}')
        return rows

    def split(self, keys, fixes=None, notes=None, drawn=(), drop=(), criteria=(), deep=False):
        """Points the scheme prices together ("[6+2+2+2]"): one null row each,
        a choice among them as one null anyN group. Returns (rows, cell).

        A part in `drawn` is one the scheme answers with a drawing: its row is
        the paper's own ask, and whatever words the scheme prints beside the
        drawing ride on that row's note."""
        fixes, notes = fixes or {}, notes or {}
        rows, cells, asides_all, dropped = [], [], [], set()
        for key in keys:
            if key in drawn:
                its = self.P.items(key)
                cells += [it.cell for it in its if it.cell]
                said = [display(it.text) for it in its if it.text] + [display(a) for it in its
                                                                      for a in it.asides]
                ask = self.drawn_ask(key)
                rows.append(self.mark_ask(point(f'r-{len(rows) + 1}', ask, None, ' '.join(x for x in [
                    f'The scheme answers ({key[2]}) with a drawing; its own print is shown with '
                    f'the answer.', ('It adds: ' + ' '.join(said)) if said else '',
                    notes.get(len(rows), '')] if x))))
                continue
            if deep:
                # A part whose scheme answers sit under markers of the scheme's
                # own ("(i) 2 (ii) 1" under 2024 HL Q4(a)): each marker's answer
                # is read on its own and labelled with it, so two answers set
                # on one printed line stay two points.
                lab = []
                for sg in self.P._below(self.P.sseg, key):
                    for it in items_of(sg.answers):
                        lab.append((sg.key[2] if sg.key != key and sg.key[2] else None, it))
            else:
                lab = [(None, it) for it in self.P.items(key)]
            for label, it in lab:
                if it.cell:
                    cells.append(it.cell)
                anyk = next((WORDS[ANY.match(a).group(1).lower()] for a in it.asides if ANY.match(a)), None)
                inline_notes = []
                if anyk:
                    opts = []
                    for o in it.options():
                        t, inl = self._verbatim(o, fixes, key)
                        opts.append(t)
                        inline_notes += inl
                    r = {'id': f'r-{len(rows) + 1}', 'kind': 'anyN', 'verbatim': opts[0],
                         'marks': None, 'openList': True,
                         'contextNote': ' '.join(x for x in [f'Any {anyk} of these.',
                                                             _asides_note(inline_notes + it.asides),
                                                             notes.get(len(rows), '')] if x),
                         'group': {'claimMax': anyk, 'options': opts}}
                    rows.append(r)
                    continue
                pts = it.points()
                for crit in criteria:
                    # An instruction to the examiner ("any correct example"),
                    # not an answer: it goes on the card's notes, where it
                    # still tells the student what earns the mark.
                    if display(crit) in [display(x) for x in pts]:
                        pts = [x for x in pts if display(x) != display(crit)]
                        self._criteria.append(f'For ({key[2] or key[1]}) the scheme prints only '
                                              f'the criterion "{display(crit)}".')
                        dropped.add(crit)
                for d in drop:
                    if display(d) in [display(x) for x in pts]:
                        pts = [x for x in pts if display(x) != display(d)]
                        dropped.add(d)
                for j, ptext in enumerate(pts):
                    if label and j == 0 and not self.P.cue and self.P.traceable(f'({label}) {ptext}'):
                        ptext = f'({label}) {ptext}'
                    t, inl = self._verbatim(ptext, fixes, key)
                    if not t and inl and rows:
                        # A point that is wholly the examiner's aside, wrapped
                        # onto rows of its own (2023 OL Q7(d)(iii)): it rides
                        # on the point above.
                        rows[-1]['contextNote'] = tidy(rows[-1].get('contextNote', '') + ' ' +
                                                       _asides_note(inl + (it.asides if j == len(pts) - 1 else [])))
                        continue
                    if label and j == 0 and self.P.cue:
                        # A labelled scheme sets its cue between the marker and
                        # the answer ("(iv) WHICH: Mg (magnesium)"), so the
                        # marker leads the row as a label, which the gate reads
                        # past: "(iv) — Mg (magnesium)".
                        t = f'({label}) — {t}'
                    note = ' '.join(x for x in [_asides_note(inl + (it.asides if j == len(pts) - 1 else [])),
                                                notes.get(len(rows), '')] if x)
                    r = point(f'r-{len(rows) + 1}', t, None, note)
                    rows.append(r)
        if (set(drop) | set(criteria)) - dropped:
            raise Refused(f'{keys}: nothing to drop for {sorted((set(drop) | set(criteria)) - dropped)}')
        if len(cells) != 1:
            raise Refused(f'{keys}: {len(cells)} mark cells across a split ({cells})')
        return rows, cells[0]

    def anyn(self, key, claim=None, fixes=None, note=''):
        """A printed menu the student picks from: one anyN row."""
        fixes = fixes or {}
        its = self.P.items(key)
        trailing = [x for x in its[1:] if x.cell is None and re.fullmatch(
            r'(or\s+)?(\s*\[[^\[\]]*(\[[^\]]*\][^\[\]]*)*\]\.?)+\s*', x.text)]
        if len(its) - len(trailing) != 1:
            raise Refused(f'{key}: {len(its)} items where one menu was expected')
        it = its[0]
        if trailing:
            note = tidy(note + ' The scheme adds: ' + ' '.join(display(x.text) for x in trailing))
        anyk = next((WORDS[ANY.match(a).group(1).lower()] for a in it.asides if ANY.match(a)), None)
        claim = claim or anyk
        if not claim:
            raise Refused(f'{key}: no claim limit printed or given')
        opts, inl = [], []
        for o in it.options():
            t, i = self._verbatim(o, fixes, key)
            opts.append(t)
            inl += i
        terms = mark_terms(it.cell)
        if len(terms) != claim:
            raise Refused(f'{key}: {it.cell} prices {len(terms)} answers, the student claims {claim}')
        steps = terms if len(set(terms)) > 1 else None
        nt = ' '.join(x for x in [_asides_note(inl + it.asides), note] if x)
        return [anyN('r-1', opts[0], sum(terms), claim, terms[0], opts, nt, steps=steps)], sum(terms)

    # ── cards ────────────────────────────────────────────────────────────
    def add(self, keys, topic, concept, rows, *, kind='fixed', notation=None, total=None,
            stem=None, notes='', figure='', deep=False, qtext=None, cid=None, label_key=None,
            ref_suffix=None):
        keys = [tuple(k) for k in keys]
        if total is None:
            total = sum(r['marks'] for r in rows) if kind == 'fixed' and not any(
                r['kind'] == 'anyN' for r in rows) else None
            if total is None:
                raise Refused(f'{keys}: give the total')
        q = int(keys[0][0])
        if stem is None:
            stem = self.context(keys[0])
        full = self.prefix + (cid or self.cid(keys))
        if topic is None or concept is None:
            # A card corrected in place keeps the syllabus filing and concept
            # its pre-audit version carried, unless the audit gives new ones.
            before = prior_card(full)
            if not before:
                raise Refused(f'{full}: no pre-audit card to inherit a topic or concept from')
            topic = topic or before['topicId']
            concept = concept or before['conceptId']
        # Two cards on one printed part -- a calculation whose steps outrun a
        # card's rows -- each name the part and which of its steps they hold
        # ("2025 HL Q10(c)(i) — steps 1–5"): the build keeps one card per
        # citation, and the reconciler reads only what precedes the " — ".
        ref = self.ref(keys) + (f' — {ref_suffix}' if ref_suffix else '')
        c = self._card(full, self.P.year, self.level, topic,
                       concept, ref, qtext or self.qtext(keys, deep=deep),
                       notation or '', total, rows, notes, stem=stem,
                       tariff_kind=kind, section='A' if q <= 3 else 'B', figure_key=figure,
                       label_key=label_key)
        if kind == 'orderedSplit':
            c['tariffModel'] = {'kind': 'orderedSplit', 'notation': notation}
        elif kind == 'fixed':
            c['tariffModel'] = {'kind': 'fixed'}
        c['keys'] = keys
        self.cards.append(c)
        return c

    def fixed(self, keys, topic, concept, **kw):
        fixes, notes, deep = kw.pop('fixes', None), kw.pop('row_notes', None), kw.get('deep', False)
        # In the labelled schemes "[2 × 3]" closes two "//"-separated points, one
        # each: read them as two rows of 3 unless told otherwise.
        skip, each = kw.pop('skip', ()), kw.pop('each', self.P.cue)
        tail = kw.pop('tail', False)
        rows = []
        self._fixes_used = set()
        for k in keys:
            rows += self.points(tuple(k), fixes, notes, deep=deep, skip=skip, each=each, tail=tail)
        self._fixes_applied(keys, fixes)
        for i, r in enumerate(rows):
            r['id'] = f'r-{i + 1}'
        return self.add(keys, topic, concept, rows, **kw)

    def ordered(self, keys, topic, concept, **kw):
        self._criteria = []
        self._fixes_used = set()
        fixes = kw.pop('fixes', None)
        rows, cell = self.split([tuple(k) for k in keys], fixes,
                                kw.pop('row_notes', None), drawn=kw.pop('drawn', ()),
                                drop=kw.pop('drop', ()), criteria=kw.pop('criteria', ()),
                                deep=kw.get('deep', False))
        self._fixes_applied(keys, fixes)
        note = (f'The scheme prices these points together as {cell} without saying which '
                f'point earns which part, so no per-point value is shown.')
        kw['notes'] = tidy(' '.join([note] + self._criteria + [kw.get('notes', '')]))
        return self.add(keys, topic, concept, rows, kind='orderedSplit', notation=cell,
                        total=mark_value(cell), **kw)

    def priced_menu(self, keys, topic, concept, claim, options, **kw):
        """A choice the scheme prices as a whole ("[6]" for any two of five)
        without a value per option: one null anyN row, and the question's
        total as the only number (questionTotal)."""
        opts = []
        for o in options:
            if not self.P.traceable(o):
                raise Refused(f'{keys}: "{o}" is not in the scheme')
            opts.append(o)
        its = self.P.items(tuple(keys[0]))
        cells = [it.cell for it in its if it.cell]
        if len(cells) != 1:
            raise Refused(f'{keys}: {len(cells)} cells for a priced menu')
        note = kw.pop('note', '')
        row = {'id': 'r-1', 'kind': 'anyN', 'verbatim': opts[0], 'marks': None, 'openList': True,
               'contextNote': tidy(f'Any {claim} of these. ' + note),
               'group': {'claimMax': claim, 'options': opts}}
        c = self.add(keys, topic, concept, [row], kind='questionTotal',
                     total=mark_value(cells[0]), **kw)
        c['tariffModel'] = {'kind': 'questionTotal'}
        return c

    def menu(self, keys, topic, concept, claim=None, **kw):
        self._fixes_used = set()
        fixes = kw.pop('fixes', None)
        rows, total = self.anyn(tuple(keys[0]), claim, fixes, kw.pop('note', ''))
        self._fixes_applied(keys, fixes)
        return self.add(keys, topic, concept, rows, total=total, **kw)

    def drawn_ask(self, key):
        """The marking point for a drawn answer: the paper's ask, or -- where
        the scheme reprints it in other words -- the scheme's own reprint. In
        a labelled scheme (no reprint) the paper's ask is returned and the row
        is marked an ask row (see mark_ask): it claims nothing from the scheme."""
        ask = self.P.ask(key)
        if self.P.traceable(ask):
            return ask
        reprint = display(joined(self.P.sseg_of(key).text)) if not self.P.cue else ''
        if reprint and self.P.traceable(reprint):
            return reprint
        if self.P.cue:
            return ask
        raise Refused(f'{key}: neither the ask nor its reprint is in the scheme')

    def ask_row(self, key, marks, note):
        """A row that is the part's own ask (see mark_ask), worth `marks`."""
        return self.mark_ask(point('r-1', self.drawn_ask(tuple(key)), marks, note))

    def mark_ask(self, row):
        """Flag a drawn row whose text is the paper's ask and not the scheme's."""
        if not self.P.traceable(row['verbatim']):
            row['ask'] = True
        return row

    def drawn(self, keys, topic, concept, figure, **kw):
        """A part the scheme answers with a DRAWING and no words.

        The marking point is the part itself -- the paper's ask, which the
        scheme reprints, so the provenance gate finds it -- and the answer is
        the scheme's own drawing, cropped and published as a solution figure
        the session holds back until the student has committed. The mark is
        what the part's cells print, summed, with the cells quoted."""
        key = tuple(keys[0])
        its = self.P.items(key)
        cells = [it.cell for it in its if it.cell]
        if not cells:
            raise Refused(f'{key}: no mark cell for a drawn answer')
        asides = [a for it in its for a in it.asides]
        # Asides set two to a line ("[n acceptable for 2][Allow end bonds shown
        # or not shown.]", 2022 OL Q11(d)B(iv)) reach here as the item's words.
        asides += [it.text for it in its
                   if re.fullmatch(r'(\s*\[[^\[\]]*\]\.?)+\s*', it.text)]
        ask = self.drawn_ask(key)
        total = sum(mark_value(c) for c in cells)
        note = ' '.join(x for x in [
            "The scheme answers this part with a drawing or notation its text cannot carry; "
            "its own print is shown with the answer.",
            f"It prices the part {' and '.join(cells)}." if len(cells) > 1 or mark_value(cells[0]) != mark_terms(cells[0])[0] else '',
            _asides_note(asides)] if x)
        return self.add([key], topic, concept, [self.mark_ask(point('r-1', ask, total, note))],
                        total=total, figure=figure, **kw)

    def drawn_with(self, keys, topic, concept, figure, **kw):
        """A part the scheme answers with a DRAWING priced beside worded points
        ("[3]" for the structure, "[3]" for "one C–Cl bond indicated ..."). Each
        cell is a row: a cell with no words is the drawing, whose row is the
        paper's ask; a cell with words is that point, as printed. The scheme's
        drawing is the card's solution figure."""
        key = tuple(keys[0])
        fixes, notes = kw.pop('fixes', None) or {}, kw.pop('row_notes', None) or {}
        rows = []
        for it in self.P.items(key):
            if it.cell is None:
                if rows and re.fullmatch(r'(\s*\[[^\[\]]*\])+\s*', it.text):
                    rows[-1]['contextNote'] = tidy(rows[-1].get('contextNote', '') +
                                                   ' The scheme adds: ' + display(it.text))
                    continue
                if not it.text.strip() and it.asides:
                    rows[-1]['contextNote'] = tidy(rows[-1].get('contextNote', '') + ' ' +
                                                   _asides_note(it.asides))
                    continue
                raise Refused(f'{key}: "{it.text}" has no mark cell of its own')
            if '+' in it.cell:
                raise Refused(f'{key}: {it.cell} is a split, not a fixed point')
            value = mark_value(it.cell)
            extra = f'The scheme prices this point {it.cell}.' \
                if value != mark_terms(it.cell)[0] else ''
            if not it.text.strip():
                note = ' '.join(x for x in [
                    'The scheme answers this with a drawing; its own print is shown with the answer.',
                    extra, _asides_note(it.asides), notes.get(len(rows), '')] if x)
                rows.append(self.mark_ask(point(f'r-{len(rows) + 1}', self.drawn_ask(key), value,
                                                note)))
            else:
                text, inline = self._verbatim(it.text, fixes, key)
                note = ' '.join(x for x in [_asides_note(inline + it.asides), extra,
                                            notes.get(len(rows), '')] if x)
                rows.append(point(f'r-{len(rows) + 1}', text, value, note))
        if not any(r['verbatim'] == self.drawn_ask(key) for r in rows):
            raise Refused(f'{key}: no cell prices a drawing')
        return self.add([key], topic, concept, rows, figure=figure, **kw)

    def route(self, keys, topic, concept, figure='', fixes=None, row_notes=None, take=None,
              **kw):
        """A calculation the scheme prices as an answer and its total ("0.6
        litres ethyne (9)"), then the working that earns it, step by step,
        each with its own cell, then other routes after "or". The card's rows
        are the first route's steps, which add to the total; the scheme's own
        print of every route is the card's figure.

        `take` names how many items after the answer line are the first
        route, where "or" does not mark where it ends."""
        key = tuple(keys[0])
        fixes, row_notes = fixes or {}, row_notes or {}
        its = [it for it in self.P.items(key) if it.cell or it.text.strip()]
        if not its or not its[0].cell:
            raise Refused(f'{key}: no answer line with a total to start a route')
        total = mark_value(its[0].cell)
        steps, got = [], 0
        for it in its[1:(1 + take) if take else None]:
            if it.cell is None:
                break
            if take is None and steps and re.match(r'^or\b', it.text.strip()):
                break
            steps.append(it)
            got += mark_value(it.cell)
            if take is None and got >= total:
                break
        if got != total:
            raise Refused(f'{key}: the first route adds to {got}, the answer is priced {total}')
        self._fixes_used = set()
        rows = []
        for it in steps:
            text, inline = self._verbatim(re.sub(r'^or\s+', '', it.text.strip()), fixes, key)
            note = ' '.join(x for x in [_asides_note(inline + it.asides),
                                        f'The scheme prices this step {it.cell}.'
                                        if mark_value(it.cell) != mark_terms(it.cell)[0] else '',
                                        row_notes.get(len(rows), '')] if x)
            rows.append(point(f'r-{len(rows) + 1}', text, mark_value(it.cell), note))
        self._fixes_applied(keys, fixes)
        answer, _ = self._verbatim(its[0].text, fixes={}, where=key)
        extra = kw.pop('notes', '')
        notes = tidy(f'The scheme gives the answer, {answer}, priced {its[0].cell}, then the working '
                     f'that earns it, step by step; the steps here are its first route'
                     + (', and its own print of every route it accepts is shown with the answer.'
                        if figure else '.') + (' ' + extra if extra else ''))
        return self.add([key], topic, concept, rows, figure=figure, notes=notes, **kw)

    def answer_only(self, keys, topic, concept, figure, fixes=None, **kw):
        """A calculation whose working the text layer cannot carry (stacked
        fractions, routes printed side by side, the 2023 equation font's
        doubled digits): the row is the scheme's answer line with the cell
        that prices the whole part, and the scheme's own print of the working,
        with the marks it gives each step, is the card's figure."""
        key = tuple(keys[0])
        its = [it for it in self.P.items(key) if it.cell or it.text.strip()]
        if not its or not its[0].cell:
            raise Refused(f'{key}: no answer line priced for the whole part')
        self._fixes_used = set()
        text, inline = self._verbatim(its[0].text, fixes or {}, key)
        self._fixes_applied(keys, fixes)
        total = mark_value(its[0].cell)
        note = ' '.join(x for x in [
            'The scheme prices the answer for the whole part and sets out the working that earns '
            'it, with the marks for each step, in a form its text cannot carry; its own print is '
            'shown with the answer.', _asides_note(inline + its[0].asides)] if x)
        return self.add([key], topic, concept, [point('r-1', text, total, note)], total=total,
                        figure=figure, **kw)

    def lifted(self, rid, text, marks, note=''):
        """A row whose text the reader could not assemble on its own (a line
        set wholly as fractions), given in the one form the provenance gate
        finds in the scheme. Refused if the gate would not find it."""
        if not self.P.traceable(text):
            raise Refused(f'"{text}" is not in the {self.P.year} {self.P.lvl} scheme')
        return point(rid, text, marks, note)

    def leave_open(self, keys, reason):
        self.open.append((self.ref([tuple(k) for k in keys]), reason))

    # ── checks ───────────────────────────────────────────────────────────
    def letter_totals(self):
        """Every letter's cards against the paper's printed mark for it."""
        got = {}
        for c in self.cards:
            k = c['keys'][0]
            got.setdefault((k[0], k[1], None, None), 0)
            got[(k[0], k[1], None, None)] += c['totalMarks']
        return {k: (got.get(k), v) for k, v in self.P.marks.items() if k[1]}

    def finish(self):
        for c in self.cards:
            c.pop('keys', None)
        return self.cards
