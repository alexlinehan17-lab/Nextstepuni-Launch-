#!/usr/bin/env python3
"""Religious Education question papers — the printed wording, lifted.

    python3 scripts/markbank/authoring/re_paper.py 2023 hl

Why this subject needs its own reader
-------------------------------------
paper.py reads a sitting as one forward-numbered run of "Question N", and the
sections walker in paper_census.py reads a sitting whose numbering restarts.
Religious Education is neither. Its paper is three UNITS holding ten lettered
SECTIONS (A-J), and only Section A — Unit One — numbers questions at all:

    Unit One      Section A   Question 1 (a) (i)      ... Question 3 (b)
    Unit Two      Section B   (a)  (b)  (c)           Sections C and D likewise
    Unit Three    Section E   (a)  (b) (i)  (b) (ii)  ... through Section J

So an ask in Sections B-J has no question number at all: its address is the
section and the part. Running it through a reader that requires a question
head loses every one of them, which is 80% of the paper.

The second reason is layout. pymupdf's block segmentation welds four printed
asks into one block here — "Answer (a) and (b). (a) (i) Imagine Plato ... (20)
(ii) Explain ..." is a single block on the 2023 Higher paper — because the SEC
sets the part markers in a narrow left column and the ask beside them, with no
blank line between parts. The markers are, however, unambiguous on the PAGE:
they open a printed line at the left margin. So the pages are read as LINES,
grouped on the baseline with a tolerance (a marker's baseline sits a point or
two off the text it heads), and a line whose first token is a part marker
starts a new ask. Nothing here composes text: an ask is the lines between its
own marker and the next one, joined.
"""
import argparse
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def papers_dir():
    return os.path.join(ROOT, 'examiner-reports', 'religious-education', 'papers')


def _glyphs():
    """The corpus-derived repair table, as paper.py builds it.

    Religious Education's papers set their option bullets in Wingdings, which
    reaches the text layer as U+F06C. Left alone it is an unreadable glyph that
    build-deck refuses; glyphmap.json maps it to a real bullet.
    """
    table = {}
    for name in ('glyphmap.json', 'glyphmap-religious-education.json'):
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            with open(path, encoding='utf-8') as fh:
                table.update({ord(k): v for k, v in json.load(fh).items()})
    return table


GLYPHS = _glyphs()

# Lines the SEC prints on every page, and the front and back matter. None of
# them is ever part of an ask.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate\b'
    r'|Religious Education\b'
    r'|Coimisi[uú]n na Scr[uú]duithe St[aá]it'
    r'|State Examinations Commission'
    r'|Higher Level|Ordinary Level|Higher level|Ordinary level'
    r'|Total Marks\b|Page \d|\d{1,3}$'
    r'|There is no examination material on this page'
    r'|Do not hand up this question paper'
    r'|This document will not be returned'
    r'|Acknowledgements?\b|Copyright notice'
    r'|Images? on page|Text on page|Image on page'
    r'|\(?Source:|\(Adapted from'
    r'|https?://|www\.'
    r'|General Directions for Candidates'
    r'|\d{4}\.\s*M\d+|\d{4}L\d+'
    r'|Monday|Tuesday|Wednesday|Thursday|Friday)', re.I)

# Where the examination material STOPS. Everything after this heading is the
# SEC's image and text credits — "Second Picture: https://www.istockphoto.com/
# vector/diverse-crowd-of-people-of- different-ages..." — and those lines carry
# no marker of their own, so the ask that happened to be open when the credits
# began swallowed them. Twelve cards shipped with a URL inside the question
# before this stop existed. It is the last thing on the paper, so stopping here
# can lose nothing: eight of the ten papers print it on their last page and the
# other two print no credits at all.
END_OF_MATERIAL = re.compile(r'^(?:Acknowledgements?\b|Copyright notice\b)', re.I)

# A picture credit printed in the MARGIN, which the baseline grouping pulls onto
# the line it sits beside: "...associated with two of the following religions:
# (Source: Adapted from cerisnet.org)". It is the SEC's attribution for the
# decorative clipart, never part of the ask, and it is removed for the same
# reason paper.py removes a running footer.
SOURCE_CREDIT = re.compile(
    r'\s*\((?:Source|Adapted from)\b[^)]*\)?'
    r'|\s*\(?(?:https?://|www\.)\S*'
    r'|\s*(?:or\s+)?//\S*'
    r'|\s*\S*\.(?:com|org|net|ie|co\.uk)\)?(?=\s|$)', re.I)

# The rubric: what to answer, never what is asked.
RUBRIC = re.compile(
    r'^(?:Answer\b|You must answer\b|Candidates must answer\b'
    r'|CANDIDATES MUST ANSWER\b|YOU MUST ANSWER\b'
    r'|\(All (?:questions|sections) carry\b'
    r'|or$|OR$)', re.I)

UNIT = re.compile(r'^(?:UNIT|Unit)\s+(ONE|TWO|THREE|One|Two|Three)\b\s*$')
SECTION = re.compile(r'^(?:SECTION|Section)\s+([A-J])\b\s*(.*)$')
QUESTION = re.compile(r'^(?:QUESTION|Question)\s+(\d)\.?\s*(.*)$')

# Two printings of a part marker. 2021 sets "a)" with no opening bracket;
# every other year sets "(a)". A roman may follow on the same line.
# 2021 sets its romans "i." and "ii." with a full stop and no bracket, where
# every other year sets "(i)". Reading only the bracketed form lost five asks
# in 2021 Ordinary — every roman in Sections E, H, I and J.
MARKER = re.compile(
    r'^(?:\(([a-h])\)|([a-h])\))\s*'
    r'(?:\((i{1,3}|iv|v)\)|(i{1,3}|iv|v)\.(?=\s))?\s*')
ROMAN_ONLY = re.compile(r'^(?:\((i{1,3}|iv|v)\)|(i{1,3}|iv|v)\.(?=\s))\s*')

# The tariff the PAPER prints beside an ask: "(20)", "(40 marks)", "(80)".
# Read to cross-check the scheme, never to price a card on its own.
PAPER_MARKS = re.compile(r'\((\d{2})(?:\s*marks?)?\)\s*$')
ANY_MARKS = re.compile(r'\((\d{2})(?:\s*marks?)?\)')

ROMANS = ['i', 'ii', 'iii', 'iv', 'v']


def _lines(path):
    """(page, x0, text) for every printed line, in reading order.

    Words are grouped on the baseline with a tolerance rather than on an exact
    y, because the SEC sets a part marker a point or two off the line it heads
    — "(a)" at y=594 beside "Justice can be understood as" at y=592 — and an
    exact grouping puts the marker on a line of its own, below the text it
    introduces.
    """
    with pymupdf.open(path) as doc:
        for pno in range(doc.page_count):
            rows = []
            for x0, y0, x1, y1, word, *_ in doc[pno].get_text('words'):
                word = word.translate(GLYPHS)
                if not word.strip():
                    continue
                mid = (y0 + y1) / 2
                for row in rows:
                    if abs(row['mid'] - mid) <= 4.0:
                        row['w'].append((x0, x1, word))
                        break
                else:
                    rows.append({'mid': mid, 'w': [(x0, x1, word)]})
            ordered = [sorted(row['w']) for row in sorted(rows, key=lambda r: r['mid'])]
            for x0, text in _merge_option_columns(ordered):
                yield pno, x0, text



BULLET_TOKEN = re.compile(r'^[\u2022\u25c6\u25cf\u25aa\u25a0]')
# The gap that separates one printed COLUMN from the next. Words inside a line
# of prose sit about one space apart (3-6pt at this size); the columns of an
# option table are set 20pt or more apart.
COLUMN_GAP = 18.0


def _merge_option_columns(rows):
    """Read a two-line option TABLE down its columns, not across its rows.

    The SEC sets an option list as a row of bullets with the long labels
    wrapping onto a second line, each under its own bullet:

        • FOUNDERS & REFORMERS   • RELIGIOUS   • SOCIAL     • SPIRITUAL
          OF RELIGIOUS ORDERS      WRITERS      REFORMERS     THINKERS

    Read left to right the second line becomes "OF RELIGIOUS ORDERS WRITERS
    REFORMERS THINKERS" and the card offers "FOUNDERS & REFORMERS" as an
    option nobody printed.

    The test is a GAP, not an alignment. Aligning on the column starts alone
    shredded six asks whose bullet row is simply followed by the sentence that
    asks the question — "• Buddhism Explain how the • Christianity
    understanding • Hinduism of God/gods/the ..." — because a long prose line
    happens to place a word near every column. A wrapped option label does not
    merely start at its column: it is SEPARATED from its neighbour by the
    white space between the columns, and running prose never is.
    """
    out = []
    skip = set()
    for i, ws in enumerate(rows):
        if i in skip:
            continue
        cols = [x0 for x0, _x1, w in ws if BULLET_TOKEN.match(w)]
        merged = None
        if len(cols) >= 2 and i + 1 < len(rows):
            nxt = rows[i + 1]
            words = [w for _x0, _x1, w in nxt]
            # Split the continuation into the GROUPS the page prints, on the
            # white space between columns. A wrapped option label is one such
            # group and lies wholly inside its own column; a line of running
            # prose is a single group that crosses every column start, which
            # is what tells the two apart. Alignment alone does not: a long
            # sentence places a word near every column by chance, and using
            # that test shredded six asks into "• Buddhism Explain how the
            # • Christianity understanding • Hinduism of God/gods/the ...".
            groups = []
            for j, (x0, x1, w) in enumerate(nxt):
                if j and x0 - nxt[j - 1][1] < COLUMN_GAP:
                    groups[-1][1] = x1
                else:
                    groups.append([x0, x1])
            bounds = list(zip(cols, cols[1:] + [10 ** 6]))
            fits = (len(groups) >= 2
                    and all(any(lo - 14 <= g0 and g1 <= hi for lo, hi in bounds)
                            for g0, g1 in groups))
            if (not any(BULLET_TOKEN.match(w) for w in words)
                    and len(words) <= 12
                    and not re.search(r'[.?!:]$', words[-1])
                    and nxt[0][0] >= cols[0] - 2
                    and fits):
                buckets = {c: [] for c in cols}
                for x0, _x1, w in nxt:
                    home = max((c for c in cols if x0 >= c - 14), default=cols[0])
                    buckets[home].append(w)
                pieces = []
                for c in cols:
                    ceiling = min([o for o in cols if o > c] + [10 ** 6])
                    own = [w for x0, _x1, w in ws if c <= x0 < ceiling]
                    pieces.append(' '.join(own + buckets[c]))
                lead = [w for x0, _x1, w in ws if x0 < cols[0]]
                merged = ' '.join(lead + pieces)
                skip.add(i + 1)
        out.append((ws[0][0], merged if merged is not None
                    else ' '.join(w for _x0, _x1, w in ws)))
    return out


class RePaper:
    """One sitting: every ask the paper prints, keyed (section, q, letter, roman).

    `q` is None in Sections B-J, which print no question number — the section
    IS the question there, and inventing one would put an address on a card
    that the paper does not print.
    """

    def __init__(self, year, level):
        self.year, self.level = year, level
        self.path = os.path.join(papers_dir(), f'{year}-{level}-paper.pdf')
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.section_titles = {}
        self.question_titles = {}
        self.asks = {}
        self.marks = {}
        self.stems = {}
        self._read()

    def _read(self):
        section = q = letter = roman = None
        cur = None                       # the key currently accumulating text
        buf = []
        pending_stem = []

        def flush():
            nonlocal buf, cur
            if cur is not None and buf:
                text = ' '.join(' '.join(buf).split())
                self.asks[cur] = (self.asks.get(cur, '') + ' ' + text).strip()
            buf = []

        for _pno, _x, raw in _lines(self.path):
            line = ' '.join(raw.split())
            if not line:
                continue
            if END_OF_MATERIAL.match(line):
                break
            if FURNITURE.match(line):
                continue
            if UNIT.match(line):
                flush()
                cur, q, letter, roman = None, None, None, None
                pending_stem = []
                continue
            m = SECTION.match(line)
            if m:
                flush()
                section, q, letter, roman, cur = m.group(1), None, None, None, None
                title = ANY_MARKS.sub('', m.group(2)).strip()
                if title:
                    self.section_titles.setdefault(section, title)
                pending_stem = []
                continue
            m = QUESTION.match(line)
            if m:
                flush()
                q, letter, roman, cur = int(m.group(1)), None, None, None
                title = ANY_MARKS.sub('', m.group(2)).strip()
                if title and not RUBRIC.match(title):
                    self.question_titles.setdefault((section, q), title)
                pending_stem = []
                continue
            if RUBRIC.match(line):
                flush()
                cur = None
                continue
            m = MARKER.match(line)
            if m:
                flush()
                letter = m.group(1) or m.group(2)
                roman = m.group(3) or m.group(4)
                cur = (section, q, letter, roman)
                rest = line[m.end():].strip()
                if pending_stem:
                    self.stems.setdefault((section, q, letter), ' '.join(pending_stem))
                    pending_stem = []
                buf = [rest] if rest else []
                continue
            m = ROMAN_ONLY.match(line)
            if m and letter is not None:
                flush()
                roman = m.group(1) or m.group(2)
                cur = (section, q, letter, roman)
                rest = line[m.end():].strip()
                buf = [rest] if rest else []
                continue
            if cur is None:
                # Prose printed under a section or question head, before its
                # first part opens: the stimulus the parts share.
                if section is not None:
                    pending_stem.append(line)
                continue
            buf.append(line)
        flush()
        self._finish()

    def _finish(self):
        # Take the paper's printed tariff off the end of each ask and record it.
        for key, text in list(self.asks.items()):
            stripped = ' '.join(SOURCE_CREDIT.sub(' ', text).split())
            if stripped != ' '.join(text.split()):
                # A credit set across two lines leaves the "or" that joined its
                # halves behind: 2021 Higher E(a) prints "(Source: https://www."
                # above "or depositphotos.com)". No ask ends in "or".
                stripped = re.sub(r'\s+or\s*$', '', stripped)
            text = stripped
            marks = None
            m = PAPER_MARKS.search(text)
            if m:
                marks = int(m.group(1))
                text = text[:m.start()].strip()
            else:
                found = ANY_MARKS.findall(text)
                if found:
                    marks = int(found[-1])
            if marks is not None:
                self.marks[key] = marks
            self.asks[key] = text
        # A letter that opened a run of romans holds no ask of its own; the
        # romans beneath it are the leaves. Where such a letter DID accumulate
        # text (a shared stimulus printed beside the marker), it becomes the
        # stem for its romans rather than a leaf.
        for key in list(self.asks):
            section, q, letter, roman = key
            if roman is not None:
                continue
            kids = [k for k in self.asks
                    if k[:3] == key[:3] and k[3] is not None]
            if kids:
                text = self.asks.pop(key)
                self.marks.pop(key, None)
                if text:
                    self.stems[(section, q, letter)] = ' '.join(
                        x for x in (self.stems.get((section, q, letter)), text) if x)
        self.asks = {k: v for k, v in self.asks.items() if v.strip()}

    # -- the address a card cites -------------------------------------------
    def ref(self, key):
        section, q, letter, roman = key
        head = f'{self.year} {self.level.upper()} Section {section} Q'
        if q is not None:
            head += str(q)
        if letter:
            head += f'({letter})'
        if roman:
            head += f'({roman})'
        return head

    def stem(self, key):
        section, q, letter, _roman = key
        return (self.stems.get((section, q, letter))
                or self.stems.get((section, q, None)))

    def keys(self):
        def order(k):
            return (k[0], k[1] if k[1] is not None else 0, k[2] or '',
                    ROMANS.index(k[3]) if k[3] in ROMANS else -1)
        return sorted(self.asks, key=order)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    args = ap.parse_args()
    P = RePaper(args.year, args.level)
    print(f'{args.year} {args.level.upper()}: {len(P.asks)} asks, '
          f'{len(P.section_titles)} sections')
    for key in P.keys():
        print(f'  {P.ref(key):<28} {P.marks.get(key, "?"):>4}  '
              f'{P.asks[key][:96]}')
    for s, t in sorted(P.section_titles.items()):
        print(f'  SECTION {s} {t}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
