#!/usr/bin/env python3
"""Agricultural Science marking schemes, read from the PDF — the table repair.

The companion to agsci_scheme.Scheme, not a replacement for it. Both lift only;
neither composes anything.

Scheme reads the flattened markdown and is right about most of the paper. It is
wrong wherever the examiners used a table: flattening a two-column page to lines
interleaves the columns, which is how a marking point came out reading
"C: Poor 15%/carry boluses/farms." and how a comparison of liquid milk against
creamery milk came out spliced into one unreadable answer.

SchemePdf reads the scheme PDF through pymupdf's block segmentation, which keeps
each table cell separate and in reading order. The same answer reads
"A: Good B: Moderate C: Poor".

So why not use this everywhere? Because it loses what the other one keeps. Short
answers that sit alone in their own block get attributed to a neighbouring part
or absorbed by the mark column, and several parts come back empty that Scheme
reports correctly. Measured across the ten schemes, each parser finds marking
points the other misses.

Hence two, and the caller chooses per part: Scheme by default, SchemePdf where a
table has been mangled. Both are safe to mix because append-scheme-blocks.py has
added the PDF's block-ordered text to the markdown the gate reads, so a claim
lifted by either parser traces against the same file.

The question cue is left at the front of a part rather than stripped. Guessing
where a cue ends cost a whole paper's answers when an unpunctuated cue was
mistaken for the entire block, so it shows up as the first candidate and the
caller leaves it out — visible and skippable beats clever and wrong.
"""
import json
import os
import re
import subprocess

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'agricultural-science', 'schemes')
VERIFIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify-claims.mjs')

QHEAD = re.compile(r'^Q\s?(\d{1,2})\b\s*')
MARKER = re.compile(r'^\(([a-z]{1,4})\)\s*')
LETTER = re.compile(r'[a-h]')
ROMAN = re.compile(r'i{1,3}|iv|vi{0,3}')
# The mark column, alone in its block or trailing a column heading:
# '2', '2(2)', '1+1', '3 x 2', '4(2) + 2(1)', 'Housing 4+2'.
TARIFF = r'\d{1,2}\s*(?:\(\s*\d{1,2}\s*\))?(?:\s*[x×]\s*\d{1,2})?(?:\s*\+\s*\d{1,2}\s*(?:\(\s*\d{1,2}\s*\))?)*'
MARKS_BLOCK = re.compile(r'^(?:[A-Za-z][A-Za-z ]{0,24}?\s)?(%s)$' % TARIFF)
MARKS_TAIL = re.compile(r'\s(%s)$' % TARIFF)
PAGENO = re.compile(r'^\d{1,3}$')
NOISE = re.compile(r'^(OR|Or|or)$')
# ' / ' separates alternatives, but it is also how the schemes write a rate:
# 'kg DM / ha', 'cfu / ml'. Listed explicitly because 'hay' is a real answer.
UNIT = ('ha', 'ml', 'l', 'litre', 'litres', 'kg', 'kgs', 'g', 'mg', 'cm', 'm',
        'm2', 'day', 'days', 'week', 'weeks', 'year', 'head', 'cfu', 'hd',
        'ewe', 'cow', 'animal', 'acre', 'ac', 'lu')
UNIT_START = re.compile(r'^(?:%s)\b' % '|'.join(UNIT), re.I)
# 'A = Simmental B = Landrace C = Blackface mountain' — an identify answer whose
# parts share one combined tariff, so the labels delimit them, not the column.
LABELLED = re.compile(r'(?:(?<=^)|(?<=\s))([A-H])\s*[=:‐–—-]\s+')
WORD = re.compile(r'[a-z]+')
# Some schemes set several parts in a single block, so a part marker turns up
# mid-text: '... C = Dock (leaf) 2 (b) Distinguish between annual and biennial'.
# Split there. The marker must follow whitespace and be followed by a capital or
# a further marker, which keeps '(leaf)' and '(2)' out of it.
INLINE_MARKER = re.compile(
    r'\s(?=\((?:[a-h])\)(?:\((?:i{1,3}|iv|vi{0,3})\))?\s+[A-Z(]'
    r'|\s?\((?:i{1,3}|iv|vi{0,3})\)\s+[A-Z(])')


def _leading(text):
    """Strip leading part markers. 'Q9 (b)(i) Based on ...' -> ('b','i','Based on ...')."""
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


class SchemePdf:
    """One marking scheme, indexed the same way as the paper."""

    def __init__(self, year, level):
        level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.year, self.level = year, level
        self.pdf = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self.path = os.path.join(SCHEMES, f'{year}-{level}.md')   # the gate's copy

        self.parts, self.cues, self._marks = {}, {}, {}
        q = letter = roman = None
        key = None
        for text in self._blocks():
            if PAGENO.match(text) or NOISE.match(text):
                continue

            m = MARKS_BLOCK.match(text)
            if m and key is not None:
                self._marks.setdefault(key, []).append(m.group(1).strip())
                continue

            head = QHEAD.match(text)
            rest = text
            if head:
                q = int(head.group(1))
                rest = text[head.end():]
            found_letter, found_roman, rest = _leading(rest)
            if (head or found_letter or found_roman) and (head or q is not None):
                if found_letter:
                    letter, roman = found_letter, found_roman
                elif found_roman:
                    roman = found_roman
                elif head:
                    letter = roman = None
                key = (q, letter, roman)
                self.parts.setdefault(key, [])
                self.cues.setdefault(key, rest)
                body = self._strip_cue(rest)
                if body:
                    self.parts[key].append(body)
                continue

            if key is None:
                continue
            tail = MARKS_TAIL.search(text)
            if tail:
                self._marks.setdefault(key, []).append(tail.group(1).strip())
                text = MARKS_TAIL.sub('', text)
            if text.strip():
                self.parts[key].append(text.strip())

    def _blocks(self):
        with pymupdf.open(self.pdf) as doc:
            pages = [sorted(doc[n].get_text('blocks'), key=lambda b: (round(b[1], 1), b[0]))
                     for n in range(doc.page_count)]
        for page in pages:
            for b in page:
                text = ' '.join(b[4].split())
                if not text:
                    continue
                for piece in INLINE_MARKER.split(text):
                    piece = piece.strip()
                    if piece:
                        yield piece

    @staticmethod
    def _strip_cue(text):
        """Drop the examiner's question cue from the front of a part's block.

        A part block opens with the cue and often runs straight into the first
        accepted answer — 'Explain agroforestry. Integration of trees with
        either crops or livestock ...' — with nothing but a full stop between
        them, and frequently not even that: 'Identify and state the function of
        machine A and B A = (fertiliser) spreader ...'.

        Only the punctuated case is cut, and only when text follows it. Guessing
        at the unpunctuated one cost a whole paper's answers when the cue was
        mistaken for the entire block, so the cue is left in place instead and
        shows up as the first candidate, where the caller can see it and leave
        it out. Visible and skippable beats clever and wrong.
        """
        m = re.search(r'\.\s+', text)
        return text[m.end():].strip() if m else text.strip()

    def marks(self, qnum, letter=None, roman=None):
        return list(self._marks.get((qnum, letter, roman), []))

    def points(self, qnum, letter=None, roman=None):
        """Candidate marking points, verbatim, split on the scheme's own ' / '."""
        lines = self.parts.get((qnum, letter, roman))
        if lines is None:
            return []
        out = []
        for line in lines:
            pieces = []
            for piece in ' '.join(line.split()).split(' / '):
                piece = piece.strip()
                if not piece:
                    continue
                if pieces and UNIT_START.match(piece):
                    pieces[-1] = f'{pieces[-1]} / {piece}'      # a rate, not a choice
                else:
                    pieces.append(piece)
            for piece in pieces:
                out.extend(self._by_label(piece))
        return out

    @staticmethod
    def _by_label(piece):
        starts = [m.start() for m in LABELLED.finditer(piece)]
        if len(starts) < 2:
            return [piece]
        starts.append(len(piece))
        return [piece[a:b].strip() for a, b in zip(starts, starts[1:]) if piece[a:b].strip()]

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
    S = Scheme(int(sys.argv[1]), sys.argv[2])
    for key in S.paths():
        pts = S.points(*key)
        print(f'{S.ref(key):<14} marks={",".join(S.marks(*key)) or "-":<14} {len(pts):>2} pts')
        for p in pts[:4]:
            print(f'      - {p[:96]}')
