#!/usr/bin/env python3
"""The Mathematics marking scheme, read page by page.

    python3 scripts/markbank/authoring/maths_scheme.py 2025 hl

A Maths scheme is one page per part, set as two columns: the Model Solution on
the left and the Marking Notes on the right. See mathtext.py for why only the
left column is damaged by extraction and why the right one is the better answer
for a card.

A page carries:
  * which paper it belongs to -- the year sets TWO papers and both number their
    questions from 1, so a part is keyed (paper, question, letter);
  * the question and part it answers, printed as "Q3" and "(c)";
  * a partial-credit ladder, "Scale 15D (0, 4, 7, 10, 15)", which is the tariff;
  * either a numbered step list or Low/High Partial Credit descriptors, which
    are what a card can carry as text;
  * the model solution's bounding box, for cropping it as a figure.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathtext                                              # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
SCHEMES = os.path.join(ROOT, 'examiner-reports/maths/schemes')

QHEAD = re.compile(r'^Q\s*(\d{1,2})\b')
PART = re.compile(r'^\(([a-h])\)\s*$')
ROMAN = re.compile(r'^\((i{1,3}|iv|v|vi{0,3})\)\s*$', re.I)
PAPER = re.compile(r'\bPaper\s*([12])\b')
CREDIT = re.compile(r'^(Low|Mid|High)\s+Partial\s+Credit\s*:?\s*$', re.I)
FULL = re.compile(r'^Full\s+Credit\s*(-\s*\d+)?\s*:?\s*$', re.I)


class Scheme:
    def __init__(self, year, level):
        import pymupdf
        self.year, self.level = year, level
        self.path = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self.doc = pymupdf.open(self.path)
        self.pages = {}
        paper, q, letter = 1, None, None
        for i, page in enumerate(self.doc):
            flat = page.get_text()
            m = PAPER.search(flat)
            if m:
                paper = int(m.group(1))
            sol, notes = mathtext.columns(page)
            if not notes or 'Marking Notes' not in ' '.join(notes[:3]):
                continue
            # The question and part are printed in the left column's first
            # lines, and a page that names neither continues the one before it.
            for line in sol[:6]:
                h = QHEAD.match(line.strip())
                if h:
                    q = int(h.group(1))
                    letter = None
                p = PART.match(line.strip()) or ROMAN.match(line.strip())
                if p:
                    letter = p.group(1)
            if q is None:
                continue
            self.pages.setdefault((paper, q, letter), []).append(i)

    def parts(self):
        return sorted(self.pages, key=lambda k: (k[0], k[1], k[2] or ''))

    def notes(self, key):
        out = []
        for i in self.pages[key]:
            out += mathtext.columns(self.doc[i])[1]
        return out

    def solution(self, key):
        out = []
        for i in self.pages[key]:
            out += mathtext.columns(self.doc[i])[0]
        return out

    def tariff(self, key):
        """(total, ladder) from the part's Scale line, or (None, None)."""
        _, total, ladder = mathtext.steps_and_scale(self.notes(key))
        return total, ladder

    def answer_rows(self, key):
        """[(label, text)] — the marking notes as a card's answer.

        Two shapes, both the scheme's own. Where it numbers the steps, each step
        is a row. Where it does not, the Low/Mid/High Partial Credit headings
        and what follows them are the rows: those name what a partially correct
        answer looks like, which is the thing a student most needs told.
        """
        notes = self.notes(key)
        steps, _, _ = mathtext.steps_and_scale(notes)
        if steps:
            return [(f'Step {n}', t) for n, t in steps]
        out, label, buf = [], None, []
        for line in notes:
            t = line.strip()
            if CREDIT.match(t) or FULL.match(t):
                if label and buf:
                    out.append((label, ' '.join(buf).strip()))
                label, buf = t.rstrip(':'), []
                continue
            if label and t and not t.startswith('Scale') and t != 'Marking Notes':
                buf.append(t.lstrip('• ').strip())
        if label and buf:
            out.append((label, ' '.join(buf).strip()))
        return out


if __name__ == '__main__':
    S = Scheme(int(sys.argv[1]), sys.argv[2])
    print(f'{len(S.parts())} parts across {len(S.doc)} pages')
    for key in S.parts()[:8]:
        total, ladder = S.tariff(key)
        rows = S.answer_rows(key)
        p, q, l = key
        print(f'  P{p} Q{q}({l or "-"})  {total} marks, ladder {ladder}, {len(rows)} rows')
        for lab, txt in rows[:3]:
            print(f'        {lab}: {txt[:66]}')
