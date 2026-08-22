#!/usr/bin/env python3
"""Marking schemes, any subject — the accepted answers, lifted.

Companion to agsci_paper.py. That module supplies what the candidate was asked;
this one supplies what the examiner accepted. Neither composes anything: a
marking point handed back here is a slice of
examiner-reports/<subject>/schemes/<year>-<level>.md.

    S = Scheme('agricultural-science', 2021, 'hl')
    S.points(1, 'a')     -> ['A = Buttercup', 'B = Thistle', 'C = Dock (leaf)']
    S.marks(1, 'a')      -> ['2', '2', '2']

Layout the schemes hold to, verified across all ten: a coursework rubric first,
then 'Section A', then parts headed 'Q1 (a)' or 'Q1 (a)(i)' carrying a
compressed cue for the examiner, with the accepted answers beneath and the mark
column pushed to the end of a line — or onto a line of its own.

Alternatives are separated by ' / ', which is the scheme's own notation.

Proposals, not verdicts
-----------------------
points() returns candidates. Whether one may become a row is decided by
verify(), which shells out to verify-claims.mjs so the rule applied is the same
comparableScheme/claimMatches the build applies — never a Python restatement of
it. A marking point that straddles the mark column ('...following exposure to 2
herbicide...') stays verbatim and still traces, but reads badly on a card, so
straddling() flags it for a cleaner sibling to be chosen instead.
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
def schemes_dir(subject):
    return os.path.join(ROOT, 'examiner-reports', subject, 'schemes')
VERIFIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify-claims.mjs')

QHEAD = re.compile(r'^Q\s?(\d{1,2})\b\s*(.*)$')
MARKER = re.compile(r'^\(([a-z]{1,4})\)\s*')
LETTER = re.compile(r'[a-h]')
ROMAN = re.compile(r'i{1,3}|iv|vi{0,3}')
PAGE = re.compile(r'^##\s*Page\s*\d+\s*$')
# The mark column: a whole line, or the tail of one. '2', '2(2)', '1+1', '4+2'.
# '2', '2(2)', '1+1', '4+2', and the multiplied form '3 x 2' / '5x2' the later
# papers use when one tariff covers several identical answers.
MARKS_ONLY = re.compile(r'^\d{1,2}\s*(\(\s*\d{1,2}\s*\))?$|^\d(\+\d)+$'
                        r'|^\d{1,2}\s*[x\u00d7]\s*\d{1,2}$')
MARKS_TAIL = re.compile(r'\s(\d{1,2}(?:\(\d{1,2}\))?|\d(?:\+\d)+'
                        r'|\d{1,2}\s*[x\u00d7]\s*\d{1,2})$')
NOISE = re.compile(r'^(OR|Or|or)$')
# Mark-band tables, not content: "Q1 (a) - (f) Number of correct responses 1 2 3
# 4 5 6 Mark 4 8 12 16 20" and "Marks 18-20 14-17 10-13". Read as content they
# invent a part per band and, worse, a question per band number.
BAND = re.compile(r'Number of correct responses|^Marks?\s+\d+\s*[-‐–]\s*\d+')
# 'A = Simmental B = Landrace C = Blackface mountain D = Jersey' — an identify
# question whose answers share one combined tariff ('4(1)'), so the mark column
# never delimits them. The labels do.
LABELLED = re.compile(r'(?:(?<=^)|(?<=\s))([A-H])\s*[=:\u2010\u2013\u2014-]\s+')
# ' / ' separates alternatives, but it is also how the schemes write a rate:
# 'kg DM / ha', 'cfu / ml', '400 c / kg'. Splitting there invents an answer
# whose whole text is a unit, so these are rejoined. Listed explicitly rather
# than guessed at by length, because 'hay' is a real answer and 'ha' is not.
UNIT = ('ha', 'ml', 'l', 'litre', 'litres', 'kg', 'kgs', 'g', 'mg', 'cm', 'm',
        'm2', 'day', 'days', 'week', 'weeks', 'year', 'head', 'cfu', 'hd',
        'ewe', 'cow', 'animal', 'acre', 'ac', 'lu')
UNIT_START = re.compile(r'^(?:%s)\b' % '|'.join(UNIT), re.I)


def _leading(text):
    letter = roman = None
    while True:
        m = MARKER.match(text)
        if not m:
            break
        tok = m.group(1)
        if LETTER.fullmatch(tok):
            letter, roman = tok, None
        elif ROMAN.fullmatch(tok):
            roman = tok
        else:
            break
        text = text[m.end():]
    return letter, roman, text


class Scheme:
    """One marking scheme, indexed the same way as the paper."""

    def __init__(self, subject, year, level):
        level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.subject, self.year, self.level = subject, year, level
        SCHEMES = schemes_dir(subject)
        self.path = os.path.join(SCHEMES, f'{year}-{level}.md')
        raw = open(self.path, errors='ignore').read().replace('\xa0', ' ')
        # append-scheme-blocks.py adds the PDF's block-ordered text to this file
        # so the provenance gate can match claims lifted from either rendering.
        # That section is a second copy of the whole scheme — parsing it as well
        # would report every part twice — so this parser stops at the marker.
        raw = raw.split('<!-- pdf-block-order')[0]

        # Skip the marking preamble. 'Section A' bounds it where a paper has
        # one; where it does not — Chemistry prints no such heading — the first
        # question header is the boundary, which is what 'Section A' was
        # standing in for anyway.
        # Skip the marking preamble. Its instructions are NUMBERED — "1. Key
        # words or terms may be awarded marks", "2. Cancelled answers" — and
        # read as questions they put three phantom questions in front of the
        # paper and slide every real one out of step. So the boundary is the
        # spelled-out word, never a bare number.
        start = raw.find('Section A')
        if start < 0:
            m = re.search(r'^(?:QUESTION|Question)\s+\d', raw, re.M)
            start = m.start() if m else 0
        body = raw[start:]

        # A bare number on the line before a '## Page n' marker is that page's
        # printed footer, not a mark. Dropped here so it cannot be read as one.
        src = [' '.join(l.split()) for l in body.splitlines()]
        for i, line in enumerate(src):
            if PAGE.match(line):
                for j in range(i - 1, -1, -1):
                    if src[j]:
                        if re.fullmatch(r'\d{1,3}', src[j]):
                            src[j] = ''
                        break

        self.parts, self.cues = {}, {}
        q = letter = roman = None
        for line in src:
            if not line or PAGE.match(line) or NOISE.match(line) or BAND.search(line):
                continue
            m = QHEAD.match(line)
            if m:
                q = int(next(g for g in m.groups() if g))
                letter, roman, rest = _leading(m.group(2))
                key = (q, letter, roman)
                self.parts.setdefault(key, [])
                self.cues[key] = rest
                continue
            if q is None:
                continue
            found_letter, found_roman, rest = _leading(line)
            if found_letter or found_roman:
                if found_letter:
                    letter, roman = found_letter, found_roman
                else:
                    roman = found_roman
                key = (q, letter, roman)
                self.parts.setdefault(key, [])
                self.cues[key] = rest
                continue
            self.parts.setdefault((q, letter, roman), []).append(line)

    def _body(self, qnum, letter=None, roman=None):
        return self.parts.get((qnum, letter, roman))

    def marks(self, qnum, letter=None, roman=None):
        """Every mark token printed against this part, in order."""
        lines = self._body(qnum, letter, roman) or []
        out = []
        for line in lines:
            if MARKS_ONLY.match(line):
                out.append(line)
                continue
            m = MARKS_TAIL.search(line)
            if m:
                out.append(m.group(1))
        return out

    def points(self, qnum, letter=None, roman=None):
        """Candidate marking points, verbatim.

        Split on ' / ', the scheme's own separator, and additionally at a line
        that ends in the mark column — but only when the part carries more than
        one mark. The column is right-aligned artwork: against a part worth a
        single 2 it is centred on whichever line happens to be vertically
        middle, so it falls mid-sentence and delimits nothing ('...following
        exposure to 2 / herbicide that would normally be lethal...'). Against a
        part worth 2, 2, 2 there is one number per answer and the line really
        does close a point ('A = Buttercup 2').
        """
        lines = self._body(qnum, letter, roman)
        if lines is None:
            return []
        delimits = len(self.marks(qnum, letter, roman)) > 1
        groups, buf = [], []
        for line in lines:
            if MARKS_ONLY.match(line):
                continue    # the column on its own line, mid-answer: not a boundary
            stripped = MARKS_TAIL.search(line)
            buf.append(MARKS_TAIL.sub('', line))
            if stripped and delimits:
                groups.append(' '.join(buf))
                buf = []
        if buf:
            groups.append(' '.join(buf))
        out = []
        for g in groups:
            pieces = []
            for piece in ' '.join(g.split()).split(' / '):
                piece = piece.strip()
                if not piece:
                    continue
                if pieces and UNIT_START.match(piece):
                    pieces[-1] = f'{pieces[-1]} / {piece}'    # a rate, not a choice
                else:
                    pieces.append(piece)
            for piece in pieces:
                out.extend(self._by_label(piece))
        return out

    @staticmethod
    def _by_label(piece):
        """Split an identify answer that packs several labels onto one line."""
        starts = [m.start() for m in LABELLED.finditer(piece)]
        if len(starts) < 2:
            return [piece]
        starts.append(len(piece))
        return [piece[a:b].strip() for a, b in zip(starts, starts[1:]) if piece[a:b].strip()]

    def straddling(self, point):
        """True if this point swallowed the mark column and will read badly."""
        return bool(re.search(r'\s\d{1,2}\s', point))

    def verify(self, claims):
        """Which of these claims the build's own gate accepts. -> (ok, bad)"""
        if not claims:
            return [], []
        payload = json.dumps({'scheme': os.path.relpath(self.path, ROOT),
                              'claims': list(claims)})
        proc = subprocess.run(['node', VERIFIER], input=payload, capture_output=True,
                              text=True, cwd=ROOT)
        if proc.returncode != 0:
            raise RuntimeError(f'verify-claims.mjs failed: {proc.stderr.strip()}')
        got = json.loads(proc.stdout)
        return got['ok'], got['bad']

    def paths(self):
        return sorted(self.parts, key=lambda k: (k[0], k[1] or '', k[2] or ''))

    @staticmethod
    def ref(key):
        q, letter, roman = key
        return f'Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


if __name__ == '__main__':
    import sys
    S = Scheme(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    for key in S.paths():
        pts = S.points(*key)
        print(f'{S.ref(key):<14} marks={",".join(S.marks(*key)) or "-":<12} {len(pts):>2} pts')
        for p in pts[:4]:
            flag = '  <-- straddles mark column' if S.straddling(p) else ''
            print(f'      - {p[:96]}{flag}')
