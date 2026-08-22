#!/usr/bin/env python3
"""Exam question papers, any subject — the printed wording, lifted.

Nothing in this module composes question text. Every string it returns is a
slice of examiner-reports/<subject>/papers/<year>-<level>[-<component>]-paper.pdf
as pymupdf reads it, with page furniture removed and whitespace collapsed.

That distinction is the reason the module exists. The marking scheme prints a
compressed cue for the examiner — "Identify the following plants" — while the
paper prints what the candidate actually read: "Identify each of the following
plants." Only the second belongs on a card, and only the paper has it.

    P = Paper('agricultural-science', 2021, 'hl')
    P.text(1, 'a')          -> 'Identify each of the following plants.'
    P.text(2, 'b', 'iii')   -> 'Identify one way the student could improve ...'
    P.stem(13, 'a')         -> the stimulus prose printed above the parts

Why blocks and not lines
------------------------
Reading the pages as lines drags a neighbouring column into the question: on
2021 HL Q6 the tick-box options 'Ribosome / Mitochondria / Chloroplast' land
inside part (iii), and on Q15(b)(ii) an entire graph axis does. pymupdf's block
segmentation keeps a part marker and its own text together in one block and
leaves the option list, the table and the ruled answer boxes as separate blocks,
so walking blocks rather than lines removes that whole class of contamination.

A part occasionally runs across two blocks, which shows up as text that stops
without terminal punctuation. Continuation handles exactly that case and stops
as soon as the sentence closes, so it cannot swallow a table.
"""
import os
import re

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
def papers_dir(subject):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')

# Subjects head their questions differently and both forms have to be read:
# Agricultural Science and Economics print "Question 4", Chemistry and Physics
# print "4." straight into the text. The bare form is anchored on a following
# capital or bracket so it cannot match a numbered answer line or a figure.
QHEAD = re.compile(r'^(?:Question\s+(\d{1,2})\b|(\d{1,2})\.\s+(?=[A-Z(]))')
MARKER = re.compile(r'^\(([a-z]{1,4})\)\s*')
LETTER = re.compile(r'[a-h]')
ROMAN = re.compile(r'i{1,3}|iv|vi{0,3}')
RUBRIC = re.compile(r'^Answer (either|any|all)\b')
PAGE_FURNITURE = re.compile(r'^Leaving Certificate Examination\s+\d{4}')
# Answer-booklet scaffolding: a numbered answer line, or a short fill-in label
# ending in a colon ('Named crop:', 'Symptoms:'). Verified across all ten
# papers: 294 such lines occur and not one is the opening line of a part.
FURNITURE = re.compile(r'^(\d{1,2}\.|[^.?!]{1,34}:)$')
TERMINAL = re.compile(r'[.?!]$')
# Biology, Chemistry and Physics set several parts inside one block, so a marker
# turns up mid-text: "(ii) How did the student make the temperature 0 °C?".
# Anchored on a following capital or bracket, which keeps "(15)" and "(a)" of a
# chemical name out of it.
INLINE_MARKER = re.compile(
    r'\s(?=\((?:[a-h]|i{1,3}|iv|vi{0,3})\)\s+[A-Z(])')
# A block holding nothing but figure labels ('A B C', 'A: B: C:'). It captions
# the artwork, so it belongs to the figure, not to the question's prose.
LABELS_ONLY = re.compile(r'^[A-H]\s*:?(\s+[A-H]\s*:?)*$')


def _blocks(path):
    """Every non-empty text block, in page then top-to-bottom, left-to-right order."""
    with pymupdf.open(path) as doc:
        pages = [sorted(doc[n].get_text('blocks'), key=lambda b: (round(b[1], 1), b[0]))
                 for n in range(doc.page_count)]
    for page in pages:
        for b in page:
            text = ' '.join(b[4].split())
            if text and not PAGE_FURNITURE.match(text):
                yield text


def _leading(text):
    """Strip leading part markers. '(a) (i) Explain x' -> ('a', 'i', 'Explain x')."""
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


class Paper:
    """One paper, indexed by question number and part path."""

    def __init__(self, subject, year, level):
        level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.subject, self.year, self.level = subject, year, level
        # A sitting may be printed as several booklets — Biology sets Sections A
        # and B in one and Section C in another — and the question numbering
        # runs on across them, so every component is read in order as one paper.
        root = papers_dir(subject)
        self.files = sorted(
            os.path.join(root, f) for f in os.listdir(root)
            if re.fullmatch(rf'{year}-{level}(-\d+)?-paper\.pdf', f))
        if not self.files:
            raise FileNotFoundError(f'no {year} {level} paper for {subject}')
        self.path = self.files[0]

        self.parts, self.stems = {}, {}
        q = letter = roman = None
        open_key = None          # the part a continuation block may extend
        for text in self._all_blocks():
            m = QHEAD.match(text)
            if m:
                q = int(m.group(1) or m.group(2))
                letter, roman, open_key = None, None, None
                self.stems.setdefault((q, None), [])
                rest = text[m.end():].strip()
                if rest and not RUBRIC.match(rest):
                    self.stems[(q, None)].append(rest)
                continue
            if q is None:
                continue
            if RUBRIC.match(text):
                continue

            found_letter, found_roman, rest = _leading(text)
            if found_letter or found_roman:
                if found_letter:
                    letter, roman = found_letter, found_roman
                else:
                    roman = found_roman
                key = (q, letter, roman)
                self.parts.setdefault(key, [])
                if rest:
                    self.parts[key].append(rest)
                # A part that opens a group ('(a)' with prose but no roman yet)
                # doubles as the stem for the romans beneath it.
                open_key = key
                continue

            if FURNITURE.match(text):
                open_key = None
                continue

            if open_key and not TERMINAL.search(' '.join(self.parts[open_key])):
                self.parts[open_key].append(text)      # continuation
                continue

            if letter is None:
                self.stems.setdefault((q, None), []).append(text)
            else:
                self.stems.setdefault((q, letter), []).append(text)
            open_key = None

    def _all_blocks(self):
        for path in self.files:
            for text in _blocks(path):
                for piece in INLINE_MARKER.split(text):
                    piece = piece.strip()
                    if piece:
                        yield piece

    @staticmethod
    def _flat(lines):
        return ' '.join(' '.join(lines).split()) or None

    @staticmethod
    def _prose(lines):
        return [l for l in lines if not LABELS_ONLY.match(l)]

    def text(self, qnum, letter=None, roman=None):
        """The printed wording of one part, verbatim. None if the part is absent."""
        got = self.parts.get((qnum, letter, roman))
        return self._flat(got) if got is not None else None

    def stem(self, qnum, letter=None):
        """Stimulus prose printed above the parts, verbatim."""
        return self._flat(self._prose(self.stems.get((qnum, letter)) or []))

    def paths(self):
        return sorted(self.parts, key=lambda k: (k[0], k[1] or '', k[2] or ''))

    def suspect(self, qnum, letter=None, roman=None):
        """True when this part's text needs human eyes before it becomes a card.

        Question text is normally sentences, so text that stops without terminal
        punctuation is the signal that block segmentation cut it short or pulled
        in a neighbour. It is only a signal, not a verdict: of the 41 parts it
        flags across the ten papers, most are legitimately unpunctuated — a
        true/false statement, a word bank, a match-the-item list, a fill-in-the-
        blank, or a question ending in a colon above its sub-headings. The
        authoring layer refuses to card a flagged part until the caller has
        looked at the page and said so.
        """
        t = self.text(qnum, letter, roman)
        return not t or not TERMINAL.search(t)

    @staticmethod
    def ref(key):
        q, letter, roman = key
        return f'Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


if __name__ == '__main__':
    import sys
    P = Paper(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    for key in P.paths():
        print(f'{P.ref(key):<14} {(P.text(*key) or "")}')
