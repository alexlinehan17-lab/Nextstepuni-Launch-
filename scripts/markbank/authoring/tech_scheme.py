#!/usr/bin/env python3
"""The Technology marking scheme, read as priced blocks.

    python3 scripts/markbank/authoring/tech_scheme.py 2024 hl

Technology's scheme is the easy half of this subject, and it is why the
subject was chosen: it REPRINTS the question it is marking, prints the
accepted answer under it, and then prints the tariff on a line of its own.

    (i) Name the main electronic component used in a Darlington pair.
    Transistor.
    (ii) Outline how a Darlington pair works.
    A Darlington pair is a configuration of two bipolar transistors ...
    (6 marks, 2 + 4)

So a block is bounded by its own tariff, its parts are the roman markers
inside it, and the split names what each part is worth -- 2 for (i), 4 for
(ii). Nothing is inferred: a block whose split does not have one term per part
keeps its total and divides nothing, and a block with no printed tariff is not
a block at all.

The reprint also does the job align.py exists for. The scheme's own heading is
the question, in the question's words, so a scheme part can be paired with the
paper part it marks on wording rather than on the (question, letter, roman)
key that Law 4 refuses to trust. `cue_score` is that evidence, and
tech_all.py refuses a pairing that cannot show it.

Three tariff shapes are printed across the ten sittings, and all three are
read here:

    "(6 marks, 3 + 3)"   total, then the split          (Higher, every year)
    "(4+4 marks)"        the split alone; total is its sum   (Ordinary)
    "(6 marks)"          a total with no split          (one-part questions)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

ROMANS = ['i', 'ii', 'iii', 'iv', 'v']

# The three printed tariff shapes. Ordered longest-first: "(6 marks, 3 + 3)"
# also matches the total-only form, and reading it that way would throw the
# split away and leave a two-part block priced as one.
# "arks" as well as "marks": the SEC's own text layer drops the M of
# "(10 Marks, 4+6)" on page 17 of the 2023 Ordinary scheme, and demanding the
# spelling lost Option 5(c) -- a printed tariff, read as no tariff at all.
_M = r'm?arks?'
TARIFF = re.compile(
    r'\(\s*(?P<total>\d{1,3})\s*' + _M + r'\s*[,;]?\s*(?P<split>\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*\)'
    r'|\(\s*(?P<splitonly>\d{1,2}(?:\s*\+\s*\d{1,2})+)\s*' + _M + r'\s*\)'
    # "(6 x 1 mark)" -- the 2021 Higher table question, six cells at one mark.
    r'|\(\s*(?P<each>\d{1,2})\s*[x\u00d7\u2715]\s*(?P<per>\d{1,2})\s*' + _M + r'\s*\)'
    r'|\(\s*(?P<only>\d{1,3})\s*' + _M + r'\s*\)', re.I)

# The Ordinary papers price a pure sketch question by QUALITY, not by content:
# "(Very good sketch - 8 marks, good sketch - 6 marks, fair sketch - 4 marks)".
# It is a printed tariff and it bounds the block, so it is read -- but it names
# no answer, which is what decides whether the block can become a card.
BAND = re.compile(
    r'\(\s*(?:very good|good|fair)\s+(?:sketch|diagram|drawing)[^)]*?'
    r'(\d{1,2})\s*' + _M + r'[^)]*\)', re.I)

# A section total printed as a heading ("Section A - Core 72 marks") or an
# option's own price ("40 marks"). It is not a block's tariff, and reading it
# as one closed a block that had not started.
SECTION_TOTALS = {24, 40, 72, 200, 300, 130, 100}

SECTION_HEAD = re.compile(r'^Section\s+([ABC])\b')
OPTION_HEAD = re.compile(r'^Option\s+(\d)\b')
# "1." at Section A; "2(a)" and "2(a) (i)" in Sections B and C. The dot form
# is Section A's alone -- Section B never prints "2." -- so the two heads
# cannot be confused.
# A head may have its line to ITSELF -- 2025 Higher sets "5." alone and the
# question below it -- so the trailing text is optional. The forward-only
# guard at the call site is what keeps a numbered list inside an answer out.
A_HEAD = re.compile(r'^(\d{1,2})\.(?:\s+(?=\S)|\s*$)')
BC_HEAD = re.compile(r'^(\d{1,2})\s*\(\s*([a-d])\s*\)\s*')
ROMAN_HEAD = re.compile(r'^\(\s*(i{1,3}|iv|v)\s*\)\s*')
# The rubric above a section, in either of the two forms the schemes print.
# It is not a marking point and it does not belong to the question after it.
RUBRIC = re.compile(
    r'^\(?[a-z]?\)?\s*Answer\s+(?:any\s+)?\w+\s+'
    r'(?:of\s+the\s+\w+\s+)?questions?\b'
    r'|^All\s+questions?\b.*\bcarr(?:y|ies)\b'
    r'|^Each\s+question\b.*\bcarr(?:y|ies)\b'
    r'|^Write\s+your\s+answers?\b'
    r'|^Instructions:', re.I)

# Page furniture: the running footer, the section name repeated in the margin,
# the rubric line above each section, and the extractor's page markers.
FURNITURE = re.compile(
    r'^##\s*Page\s*\d+\s*$'
    r'|^Leaving Certificate(?:\s+Examination)?[,\s]'
    r'|^Technology\s*[-–—]\s*(?:Higher|Ordinary)\s+Level'
    r'|^Section\s+[ABC](?:\s+\d+)?(?:\s+Marking\s+Scheme)?\s*$'
    r'|^Marking\s+Scheme\s*$'
    r'|^\d{1,3}\s*$'
    r'|^Answer\s+\d\(\w\)\s+(?:and|or)\s+\d\(\w\)\s*$'
    r'|^OR\s*$', re.I)

# The examiner talking to the examiner rather than stating an answer, and the
# scheme's own lead-in to a list. Neither is a marking point.
NOT_A_POINT = re.compile(
    r'^(?:suggested solution|any valid alternative|note:|accept any|'
    r'or any other valid|any other valid|etc\.?)\s*[:.]?\s*$', re.I)


def _words(text):
    return {w for w in re.findall(r"[a-z']+", (text or '').lower()) if len(w) > 2}


def cue_score(cue, ask):
    """How much of the SCHEME's reprinted question the paper's ask contains.

    The scheme compresses -- "Draw flowchart." for "Draw a flowchart for the
    operating sequence of the deterrent" -- so the measure is one-sided: what
    share of the cue's content words the ask holds. A short cue proves little,
    which is why tech_all.py also requires the cue to carry words at all.
    """
    a, b = _words(cue), _words(ask)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a)


class Block:
    """One priced unit of the scheme: a question, or a lettered part of one."""

    def __init__(self, section, q, letter):
        self.section, self.q, self.letter = section, q, letter
        self.lines = []            # (roman or None, text)
        self.total = None
        self.terms = []
        self.notation = ''
        # Whether the scheme PRINTED this block's number, or the number was
        # filled in from the block's position in the run.
        self.numbered = True

    @property
    def key(self):
        return (self.section, self.q, self.letter)

    def romans(self):
        out = []
        for roman, _ in self.lines:
            if roman and roman not in out:
                out.append(roman)
        return out

    def part_lines(self, roman):
        return [t for r, t in self.lines if r == roman]

    def head_lines(self):
        """Lines printed before the first roman marker: the block's own cue."""
        return [t for r, t in self.lines if r is None]

    def marks_for(self, roman):
        """What the printed split says this part is worth, or None.

        Never a guess. The split is used only where it has exactly one term
        per part the block prints, which is what makes "2 + 4" mean "(i) is
        worth 2 and (ii) is worth 4" rather than an arrangement of six marks
        the scheme has not attributed.
        """
        romans = self.romans()
        if not romans or len(self.terms) != len(romans):
            return None
        return self.terms[romans.index(roman)]


class TechScheme:
    def __init__(self, year, level):
        self.year = year
        self.level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.path = os.path.join(
            ROOT, 'examiner-reports/technology/schemes',
            f'{year}-{self.level}.md')
        self.blocks = {}
        self._parse()

    def _parse(self):
        with open(self.path, encoding='utf-8') as fh:
            raw = fh.read()
        # Section A first, named or not. Two sittings print no "Section A"
        # heading at all -- 2025 Higher opens straight into "Answer any twelve
        # questions" -- and requiring the heading lost all fifteen of that
        # paper's short questions, silently.
        section = 'A'
        # Everything before the first section heading, rubric or question head
        # is the cover, the note to teachers and the annotation table. None of
        # it is a marking point and the marks printed on it are not tariffs.
        started = False
        lines, roman = [], None
        head_q, head_letter = None, None
        last_q = 0
        order = []

        def close(total, terms, notation):
            """Emit the block the tariff just ended."""
            nonlocal lines, roman, head_q, head_letter, last_q
            if lines:
                q = head_q
                if q is None:
                    # A Section A head the extractor lost. Three sittings drop
                    # the "1." / "3." / "8." of a short question into a cell of
                    # their own that lands elsewhere on the page, so the block
                    # arrives with its answer and its tariff and no number.
                    # The block still exists -- the tariff bounds it -- and its
                    # number is the one next due. That is POSITIONAL, which
                    # Law 4 does not accept on its own, so tech_all.py will not
                    # card such a block unless the scheme's reprinted question
                    # matches the paper's ask for that number by wording.
                    q = last_q + 1 if section == 'A' else None
                if q is not None:
                    block = Block(section, q, head_letter)
                    block.lines = lines
                    block.total, block.terms = total, terms
                    block.notation = notation
                    block.numbered = head_q is not None
                    if block.key not in self.blocks:
                        order.append(block.key)
                    self.blocks[block.key] = block
                    last_q = q
            lines, roman = [], None
            head_q, head_letter = None, None

        for text in _lines(raw):
            # Page furniture, unless it is carrying a tariff: the 2021
            # Ordinary scheme sets Question 3(d)'s "(6 Marks, 4+2)" on the same
            # line as the running footer, and dropping the line whole dropped
            # the tariff with it -- one priced block lost, silently.
            if FURNITURE.match(text):
                if not TARIFF.search(text) and not BAND.search(text):
                    continue
                text = FURNITURE.sub('', text, count=1).strip()
            sh = SECTION_HEAD.match(text)
            heading = bool(sh) or bool(RUBRIC.match(text))
            if heading:
                # A heading or a rubric closes nothing and belongs to nothing.
                # Whatever has accumulated above it is the cover page or the
                # instructions page, not a question: 2021 read "Coimisiun na
                # Scruduithe Stait ... (72 marks)" as Section A Question 1,
                # which shifted every real head out of reach of the
                # forward-only guard and left all fifteen questions unnumbered
                # and off by one.
                lines, roman, head_q, head_letter = [], None, None, None
                started = True
            if sh and sh.group(1) > section and any(
                    k[0] == section for k in self.blocks):
                # A section moves forward, and only once the CURRENT one holds
                # a block. The instructions page lists every section with its
                # marks -- "Section B - Core (24 marks) / Section C - Options
                # (40 marks)" -- and following that listing walked the tracker
                # to C before the scheme had begun, filing all of Section B's
                # eight blocks under Section C. Three sittings, twenty-four
                # blocks, and the census would have called them all covered.
                section, last_q = sh.group(1), 0
            if heading:
                continue
            oh = OPTION_HEAD.match(text)
            if oh and section == 'C':
                lines, roman, head_q, head_letter = [], None, None, None
                last_q = int(oh.group(1)) - 1
                continue

            m = BC_HEAD.match(text) if section in ('B', 'C') else None
            if m:
                started = True
                head_q, head_letter = int(m.group(1)), m.group(2)
                roman = None
                text = text[m.end():]
            elif section == 'A':
                m = A_HEAD.match(text)
                # Forward only, and only within reach. A short question's
                # ANSWER can be a numbered list -- 2025 Higher Q11 answers a
                # work breakdown structure as "1. Research and design 2. Select
                # materials" -- and reading those as heads re-opened Question 1
                # inside Question 11.
                if m and last_q < int(m.group(1)) <= last_q + 3:
                    head_q, head_letter, roman = int(m.group(1)), None, None
                    text = text[m.end():]
                    started = True

            if not started:
                continue

            rh = ROMAN_HEAD.match(text)
            if rh:
                roman = rh.group(1)
                text = text[rh.end():]

            # The tariff may end a line of prose ("...over budget, etc.
            # (4+4 marks)") as often as it has a line to itself.
            hit = TARIFF.search(text)
            band = None if hit else BAND.search(text)
            if hit or band:
                m = hit or band
                total, terms = (_tariff(hit) if hit
                                else (int(band.group(1)), []))
                tail = (text[:m.start()] + ' ' + text[m.end():]).strip()
                if not lines and not tail and total in SECTION_TOTALS and not terms:
                    continue            # a section or option heading's price
                if tail:
                    lines.append((roman, tail))
                close(total, terms, m.group(0))
                continue

            if text and not NOT_A_POINT.match(text):
                lines.append((roman, text))
        self.order = order

    def priced(self):
        """Every block the scheme actually prices, in printed order."""
        return [self.blocks[k] for k in self.order if self.blocks[k].total]


def _lines(raw):
    """The scheme's lines, with a parenthesis that wraps put back together.

    The quality band is the only thing in these schemes that runs across a
    line break inside its own brackets -- "(Very good sketch - 8 marks," on
    one line and "fair sketch - 4 marks)" on the next -- and neither half is a
    tariff on its own. Five Ordinary sketch questions were invisible because
    of it, and worse, each one's answer then ran on into the block below it.
    """
    out = []
    pending = None
    for line in raw.split('\n'):
        text = ' '.join(line.split())
        if not text:
            continue
        if pending is not None:
            text = f'{pending} {text}'
            pending = None
        # An unclosed bracket that mentions marks, and nothing else: a tariff
        # cannot span more than the line after its own.
        if text.count('(') > text.count(')') and re.search(r'\bm?arks?\b', text, re.I):
            pending = text
            continue
        out.append(text)
    if pending is not None:
        out.append(pending)
    return out


def _tariff(hit):
    if hit.group('each'):
        n, per = int(hit.group('each')), int(hit.group('per'))
        return n * per, [per] * n
    if hit.group('total'):
        terms = [int(x) for x in re.findall(r'\d+', hit.group('split'))]
        return int(hit.group('total')), terms
    if hit.group('splitonly'):
        terms = [int(x) for x in re.findall(r'\d+', hit.group('splitonly'))]
        return sum(terms), terms
    return int(hit.group('only')), []


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    S = TechScheme(year, level)
    print(f'{year} {level.upper()}: {len(S.priced())} priced block(s)')
    for b in S.priced():
        ref = f'Section {b.section} Q{b.q}' + (f'({b.letter})' if b.letter else '')
        romans = b.romans()
        split = '+'.join(str(t) for t in b.terms) or '-'
        print(f'  {ref:<24} {b.total:>3} [{split:<10}] romans={romans}')
        for r in romans or [None]:
            head = ' | '.join(b.part_lines(r))[:110]
            print(f'        ({r or "-"}) {head}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
