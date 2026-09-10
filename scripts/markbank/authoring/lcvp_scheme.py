#!/usr/bin/env python3
"""Read one LCVP marking scheme into ordered parts, tariffs and marking points.

    python3 scripts/markbank/authoring/lcvp_scheme.py 2025      # print the parts

LCVP's scheme is the Economics "menu" shape: a priced ask followed by an
UNPRICED numbered list of alternative marking points, quantified by a group
tariff — "3@2m (1 + 1)", "3 x 2 marks (1+1)", "4 x 1 mark". Two placements
coexist in every year: some asks print the tariff on the head line beside the
marks, others under the ask and above the list, and 2018-2020 print it BELOW
the list as often as above it. All three are read from the whole part.

Parts are held in DOCUMENT ORDER and keyed by position, not by the address the
scheme prints. The scheme's own numbering cannot be trusted as a key: the 2021
scheme sets a specimen questionnaire — "Q.1 Male ☐ Female ☐" through "Q.8 Any
further comments" — inside the model answer to Section C Q.3(c), and keying on
what is printed made the real Q.4 append itself to the specimen's fourth
question. The printed address is kept as evidence; lcvp_lib pairs a part with
the PAPER's ask by wording and order, which is Law 4.

Nothing here decides what a card says. It reports what the scheme prints, so
that lcvp_all.py can refuse anything it cannot read one way.
"""
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

SECTION = re.compile(r'^Section\s+([A-C])\b')
QHEAD = re.compile(r'^Q\.?\s*(\d{1,2})[.)]?\s*')
LETTER = re.compile(r'^\(([a-h])\)\s*')
ROMAN = re.compile(r'^\((i{1,3}|iv|vi{0,3}|ix|x)\)\s*')
# A numbered marking point, at a line start or — where the SEC sets the list in
# two columns and the flattened text runs across the page — part way along one.
# 2019 prints "1. Personal details 5. Hobbies/interests" as a single line, and
# reading that as point 1 ships the SEC's fifth answer inside its first.
# The space after the dot is OPTIONAL: 2018 sets its Section A answers as
# "1.Price", "2.Promotion", "3.Place", with no space at all, and demanding one
# left five whole questions looking as though the scheme listed nothing. The
# lookahead requires a LETTER or bracket after the dot, so "€9.45" and "9.5"
# cannot become point 9.
POINT = re.compile(r'(?:^|(?<=\s))(\d{1,2})\.\s*(?=[A-Za-z(‘“])')
BULLET = re.compile('^[ \\t]*[\u2022\u00b7\u25aa\u2023\u27a2\u25cf\uf0b7\u2192][ \\t]*')
PAGE = re.compile(r'^##\s*Page\s*\d+\s*$')
BARE_NUMBER = re.compile(r'^\s*\d+\s*$')

# The group tariff. "3@2m (1 + 1)", "3 x 2 marks (1+1)", "4 x 1 mark",
# "5 @ 1m", "4x2 (1+1)" — the trailing m/mark is optional because 2025 prints
# "2@2 (1+1)" and "4x2 (1+1)" without it.
GROUP = re.compile(r'\b(\d{1,2})\s*[@x×]\s*(\d{1,2})\s*(?:m\b|marks?\b)?', re.I)
# The marks the SEC prints for a part: "6 marks", "1 mark", "(9 mark)".
MARKS = re.compile(r'\(?\s*(\d{1,3})\s*marks?\b\)?', re.I)
# Printed, but nobody's answer: running page furniture and the examiner-facing
# headings the extractor lifts alongside the answers.
FURNITURE = re.compile(
    r'^(?:LCVP\b|Link Modules|Leaving Certificate|Marking Scheme|Coimis'
    r'|Solution & Marking|Written Examination|Examination Total'
    r'|Distinction\b|Merit\b|Pass\b|Section\s+[A-C]\b|Part\s+\d\b|PART\s+\d\b)',
    re.I)


def scheme_path(year):
    return os.path.join(ROOT, 'examiner-reports', 'lcvp', 'schemes', f'{year}-cl.md')


def _lines(year):
    with open(scheme_path(year), encoding='utf-8') as fh:
        raw = fh.read()
    return [line.rstrip() for line in raw.split('\n')
            if line.strip() and not PAGE.match(line) and not BARE_NUMBER.match(line)]


def split_points(text):
    """The numbered marking points in one run of scheme prose.

    Restored to the SEC's own numbering rather than the order the flattened
    text happens to produce: a two-column list flattens to 1, 5, 2, 6, 3, 7, 4.
    """
    spans = list(POINT.finditer(text))
    if not spans:
        return []
    out = []
    for i, m in enumerate(spans):
        end = spans[i + 1].start() if i + 1 < len(spans) else len(text)
        out.append((int(m.group(1)), ' '.join(text[m.end():end].split())))
    numbers = [n for n, _ in out]
    if sorted(numbers) == list(range(1, len(numbers) + 1)):
        out.sort(key=lambda pair: pair[0])
    return [t for _, t in out if t]


def split_bullets(lines):
    out, current = [], None
    for line in lines:
        if BULLET.match(line):
            if current is not None:
                out.append(' '.join(current.split()))
            current = BULLET.sub('', line)
        elif current is not None:
            current += ' ' + line
    if current is not None:
        out.append(' '.join(current.split()))
    return [t for t in out if t]


def _is_bare_tariff(line):
    """A line that prices answers and says nothing else — "RP 2@1m", "3 @ 1m"."""
    residue = re.sub(r'[^A-Za-z]+', '', MARKS.sub(' ', GROUP.sub(' ', line)))
    return bool(GROUP.search(line)) and len(residue) <= 4


def _runs(lines):
    """Split a part's lines where the SEC starts a SECOND numbered answer.

    2021 sets Section A Q.8's two asks under one head — "Two valid reasons 2 @
    1 mark", seven points, then "Do you agree with Kate's evaluation…", "Two
    valid reasons 2 x 2 marks (1+1)", seven more. One part there is two asks
    with two tariffs, and a card built on it would price one ask at both.

    A run restarts at a LINE-INITIAL "1.", never a mid-line one: a two-column
    list flattens to "1. Personal details 5. Hobbies/interests" and the numbers
    that follow the first are the second column, not a new answer.
    """
    starts = [0]
    seen = False
    for i, line in enumerate(lines):
        # A tariff printed BELOW a run of answers closes that run. 2018 sets
        # "Explain the benefits ... How might poor industrial relations affect
        # the business? 6 marks" as one part with two lists — "Benefits:" 1-6,
        # "3@1m", "Affect of poor Industrial relations." 7-10, "3@1m" — and
        # because the numbering runs on rather than restarting, nothing split
        # them: the card would have paid one list at both tariffs. Only where
        # answers have already been seen, so the far commoner tariff-above-the
        # -list placement cannot orphan its own list.
        if seen and _is_bare_tariff(line) and i + 1 < len(lines) \
                and any(re.match(r'^\d{1,2}\.\s*[A-Za-z(]', nxt)
                        for nxt in lines[i + 1:]):
            starts.append(i + 1)
            seen = False
            continue
        m = re.match(r'^(\d{1,2})\.\s*[A-Za-z(]', line)
        if not m:
            continue
        if m.group(1) == '1' and seen:
            # The new run's own cue and tariff are the lines since the last
            # point of the previous run.
            back = i
            while back - 1 > starts[-1] and not re.match(r'^\d{1,2}\.\s*[A-Za-z(]',
                                                         lines[back - 1]):
                back -= 1
            # 2018-2020 print the tariff UNDER the list it prices — "RP 2@1m"
            # lands between the last answer of one run and the heading of the
            # next — so a walk-back that swallowed it left the first run with
            # no tariff and gave the second one two. A line that is almost
            # nothing but a tariff belongs to the run above it; a line with a
            # sentence in it opens the run below.
            while back < i and _is_bare_tariff(lines[back]):
                back += 1
            if back > starts[-1]:
                starts.append(back)
            seen = False
            continue
        seen = True
    starts.append(len(lines))
    return [lines[a:b] for a, b in zip(starts, starts[1:]) if lines[a:b]]


def restore_dots(lines):
    """Put back the full stop the SEC dropped from a numbered answer.

    2018 sets Section A Q.4 as "1. Loves the sport of gaelic football." then
    "2 Sports teams play a huge role..." and "3 The stronger the locality...",
    with no dot after the 2 or the 3. The list then read as ONE answer, and
    the card claimed two answers from a list of one. Only where the number is
    exactly the next one due, so a sentence that happens to open with a figure
    cannot become a marking point.
    """
    out, expect = [], None
    for line in lines:
        m = re.match(r'^(\d{1,2})\.\s*[A-Za-z(]', line)
        if m:
            expect = int(m.group(1)) + 1
            out.append(line)
            continue
        m = re.match(r'^(\d{1,2})\s+(?=[A-Z])', line)
        if m and expect is not None and int(m.group(1)) == expect:
            expect += 1
            out.append(f'{m.group(1)}. {line[m.end():]}')
            continue
        out.append(line)
    return out


class Part:
    """One run of the scheme: an ask, what it pays, and the answers offered."""

    def __init__(self, index, section, address, lines):
        self.index = index
        self.borrowed_cue = False
        self.section = section
        self.address = address            # (section, q, letter, roman) as PRINTED
        lines = restore_dots(lines)
        self.lines = lines
        body = '\n'.join(lines)
        self.body = body
        points = split_points(body)
        if not points:
            points = split_bullets(lines)
        self.points = points
        first = POINT.search(body)
        head = body[:first.start()] if first else body
        if not first and self.points:
            head = ''
        self.head = ' '.join(head.split())
        self.groups = [(int(a), int(b)) for a, b in GROUP.findall(body)]
        # The tariff comes OUT before the marks are read. "Three valid answers
        # 3 x 2 marks (1+1)" prints two numbers and only the first is a count;
        # reading the raw line made the part worth 2 marks rather than 6, on
        # 130 of the corpus's 472 parts.
        m = MARKS.search(GROUP.sub(' ', self.head))
        self.marks = int(m.group(1)) if m else None
        cue = MARKS.sub(' ', GROUP.sub(' ', self.head))
        self.cue = ' '.join(cue.split())
        # Does this part STATE an answer, or is it only the SEC restating the
        # ask? Several years print both asks of a two-part question first and
        # both answers after, and those cue shells carry a tariff and a marks
        # cell but no answer at all — pairing them with the paper consumed the
        # slot the real answer needed and shifted every pairing after it.
        letters = len(re.sub(r'[^A-Za-z]', '',
                             MARKS.sub(' ', GROUP.sub(' ', body))))
        self.states_answer = bool(self.points) or (
            letters - len(re.sub(r'[^A-Za-z]', '', self.cue)) >= 12)
        # The tariff EXACTLY as the SEC prints it, for the card's notation:
        # "3 @ 2m (1 + 1)" says more than "3 x 2" — the bracket is how the two
        # marks inside one point are split, and the card shows it.
        self.notation = ''
        m = GROUP.search(body)
        if m:
            end = m.end()
            tail = re.match(r'\s*\((?:\d+\s*[+/]\s*)+\d+\)', body[end:])
            if tail:
                end += tail.end()
            self.notation = ' '.join(body[m.start():end].split())

    @property
    def group(self):
        """The one tariff this part reads as, or None if it reads several."""
        distinct = sorted(set(self.groups))
        return distinct[0] if len(distinct) == 1 else None

    def __repr__(self):
        return f'<Part {self.address} marks={self.marks} groups={self.groups} points={len(self.points)}>'


class LcvpScheme:
    def __init__(self, year):
        self.year = year
        self.parts = []
        section = q = letter = roman = None
        pending = None
        for line in _lines(year):
            sh = SECTION.match(line)
            if sh and len(line) < 60:
                self._flush(pending, section)
                pending = None
                section, q, letter, roman = sh.group(1), None, None, None
                continue
            if section is None:
                continue
            text = line
            opened = False
            qh = QHEAD.match(text)
            if qh:
                q, letter, roman = int(qh.group(1)), None, None
                text, opened = text[qh.end():], True
            lh = LETTER.match(text)
            if lh:
                letter, roman = lh.group(1), None
                text, opened = text[lh.end():], True
            rh = ROMAN.match(text)
            if rh:
                roman = rh.group(1)
                text, opened = text[rh.end():], True
            if opened:
                self._flush(pending, section)
                pending = {'address': (section, q, letter, roman), 'lines': []}
            if pending is None or FURNITURE.match(text.strip()):
                continue
            if text.strip():
                pending['lines'].append(text)
        self._flush(pending, section)
        self._adopt_cues()

    def _adopt_cues(self):
        """Give an answer block the cue the SEC printed for it further up.

        Several years set both asks of a two-part question first and both
        answers after: "Q.6 (i) What resources does Ciara need...  (ii) Why is
        using ICT beneficial...  6 marks" and then "(i) 2@1m  1. Laptop ...".
        The answer block carries the tariff and the answers but no wording at
        all, so nothing could pair it with the paper's ask. Its cue is the one
        the scheme printed at the SAME address above it — evidence, not a
        guess — and only the cue is taken: the marks on that line price the
        whole question, and adopting them would make a 4-mark part claim 6.
        """
        for i, part in enumerate(self.parts):
            if part.cue or not part.points:
                continue
            for earlier in reversed(self.parts[:i]):
                if earlier.address == part.address and earlier.cue \
                        and not earlier.points:
                    part.cue = earlier.cue
                    part.borrowed_cue = True
                    break

    def _flush(self, pending, section):
        if not pending or not pending['lines']:
            return
        for lines in _runs(pending['lines']):
            self.parts.append(
                Part(len(self.parts), pending['address'][0], pending['address'],
                     lines))

    def answering(self):
        """Parts whose answers the SEC NUMBERED. These anchor the pairing.

        A numbered list is unmistakably an answer; a run of prose may be an
        answer or may be the SEC restating the ask, and only the paper can
        settle which. So the numbered parts are paired first and the prose
        ones are read afterwards, inside the window the anchors leave.
        """
        return [p for p in self.parts if p.points]

    def cardable(self):
        """Parts that state something — a shell with neither is not an answer."""
        return [p for p in self.parts if p.points or p.groups or p.marks]


def _report(year):
    S = LcvpScheme(year)
    for p in S.parts:
        print(f'{year} {p.index:3d} {p.address} marks={p.marks} '
              f'groups={sorted(set(p.groups))} points={len(p.points)}')
        print(f'        cue: {p.cue[:104]}')
        if p.points:
            print(f'        p1 : {p.points[0][:104]}')


if __name__ == '__main__':
    for arg in (sys.argv[1:] or [str(y) for y in range(2018, 2026)]):
        _report(int(arg))
