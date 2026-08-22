#!/usr/bin/env python3
"""Agricultural Science question papers — the printed wording, lifted.

Nothing in this module composes question text. Every string it returns is a
slice of examiner-reports/agricultural-science/papers/<year>-<level>-paper.pdf
as pymupdf reads it, with page furniture removed and whitespace collapsed.

That distinction is the reason the module exists. The marking scheme prints a
compressed cue for the examiner — "Identify the following plants" — while the
paper prints what the candidate actually read: "Identify each of the following
plants." Only the second belongs on a card, and only the paper has it.

    P = Paper(2021, 'hl')
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
PAPERS = os.path.join(ROOT, 'examiner-reports', 'agricultural-science', 'papers')

QHEAD = re.compile(r'^Question\s+(\d{1,2})\b')
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

    def __init__(self, year, level):
        level = {'higher': 'hl', 'ordinary': 'ol'}.get(level, level)
        self.year, self.level = year, level
        self.path = os.path.join(PAPERS, f'{year}-{level}-paper.pdf')

        self.parts, self.stems = {}, {}
        q = letter = roman = None
        open_key = None          # the part a continuation block may extend
        for text in _blocks(self.path):
            m = QHEAD.match(text)
            if m:
                q, letter, roman, open_key = int(m.group(1)), None, None, None
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
    P = Paper(int(sys.argv[1]), sys.argv[2])
    for key in P.paths():
        print(f'{P.ref(key):<14} {(P.text(*key) or "")}')
