#!/usr/bin/env python3
"""History question papers — the printed wording, lifted.

    python3 scripts/markbank/authoring/hist_paper.py 2021 hl lm

THE SUBJECT IS TWO PAPERS, NOT ONE
----------------------------------
History is examined in two FIELDS OF STUDY, and a candidate sits one of them:
Later Modern 1815-1993 (SEC subject 004) and Early Modern 1492-1815 (SEC
subject 096). Both are set on the same afternoon, both are printed as separate
papers, and ONE marking scheme prints both. fetch-corpus.py only ever fetched
004, so half of what the scheme answers had no paper to be anchored against.
Both are on disk now, as `<year>-<level>-lm-paper.pdf` and `-em-paper.pdf`,
and a citation names its field: "2021 HL Early Modern Section 1 Q1(a)".

WHY LINES AND NOT BLOCKS
------------------------
paper.py reads blocks, because in the sciences a block keeps a part marker with
its own text. Here it does the opposite: the SEC sets the DBQ's part markers in
a narrow left column and their text beside them, so pymupdf welds "1. (a) ...
(b) ... (c) ... (20)" into one block, and the Section 2 topics likewise arrive
as one block per topic. On the PAGE the structure is unambiguous — a marker
opens a printed line at the margin — so the pages are read as LINES, words
grouped on the baseline with a tolerance because a marker sits a point or two
off the text it heads. Nothing here composes text: an ask is the lines between
its own marker and the next one, joined.

THE ADDRESSES THE PAPER PRINTS
------------------------------
    Section 1     the Documents-Based Question: "1. (a)" .. "4."
    Section 2/3   Ireland / Europe and the wider world, each split into TOPICS
                  that restart their numbering, so a topic is part of the
                  address: "Section 2 Topic 1 Q3".
    Higher        a topic sets four essays, each priced (100).
    Ordinary      a topic sets three priced parts — A (30 marks), five short
                  questions on a printed extract; B (30 marks), a paragraph on
                  one of four headings; C (40 marks), a longer paragraph on one
                  of four questions. Only A numbers asks the scheme prices
                  separately ("A1." .. "A5."); B and C are priced whole, so the
                  four headings under each are printed ALTERNATIVES, not asks.
                  Their keys are "Section 2 Topic 1 A Q1" and "Section 2 Topic
                  1 B".
    Extra A       2023-2025 Ordinary print one further stimulus unit after
                  Section 3 for candidates following that year's alternative
                  instructions. The scheme answers it under "Extra Section A
                  questions on page 15 of the exam paper", and it keys
                  "Section 3 Extra A Q1".
"""
import argparse
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

FIELDS = {'lm': 'Later Modern', 'em': 'Early Modern'}


def papers_dir():
    return os.path.join(ROOT, 'examiner-reports', 'history', 'papers')


def _glyphs():
    table = {}
    for name in ('glyphmap.json', 'glyphmap-history.json'):
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            with open(path, encoding='utf-8') as fh:
                table.update({ord(k): v for k, v in json.load(fh).items()})
    return table


GLYPHS = _glyphs()

# Running heads, footers and the SEC's front and back matter. None is ever an
# ask, and every one of them is printed on a line of its own.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate\b'
    r'|History\s*[-–]\s*(?:Later|Early) Modern\b'
    r'|Coimisi[uú]n na Scr[uú]duithe St[aá]it'
    r'|State Examinations Commission'
    r'|LEAVING CERTIFICATE EXAMINATION'
    r'|HISTORY\b|FIELD OF STUDY'
    r'|Written examination|Pre-submitted Research Study Report'
    r'|Instructions to candidates|Use ONE of the following sets'
    r'|\d?\.?\s*(?:Usual instructions|Alternative instructions)'
    r'|Answer (?:all parts|one question|three questions|Sections)'
    r'|Answer one of the following|Answer the following'
    r'|Write a short paragraph on one of the following'
    r'|Study the documents? (?:opposite|below)'
    r'|Read it and answer|Read the (?:extract|following)'
    r'|Recommended maximum time'
    r'|Section \d \(\d+ marks\)|Sections? \d(?: (?:&|and) \d)? \(\d+ marks\)'
    r'|(?:Ireland|Europe and the wider world)\s*:\s*Topics\b'
    r'|OR \d\.|Do not hand up|It will not be returned'
    r'|Copyright notice|Acknowledgements?\b'
    r'|This examination paper|Any subsequent use|The Commission does not'
    r'|examination paper has been prepared|owner, and which may'
    r'|accept liability|Monday|Tuesday|Wednesday|Thursday|Friday'
    r'|\d{4}\.\s*M\d+|\d{4}L\d+|Page \d+$|\d{1,3}$)', re.I)

# Where the examination material stops.
END_OF_MATERIAL = re.compile(r'^(?:Copyright notice|Acknowledgements?)\b', re.I)

SECTION = re.compile(r'^SECTION\s+(\d)\s*:', re.I)
# "Ireland: Topic 1" / "Europe and the wider world: Topic 6". The 2025 Higher
# Early Modern paper heads its documents question "Europe: Topic 1" — the same
# area, abbreviated — and the full-name-only pattern left that paper's DBQ with
# no case-study topic at all.
TOPIC = re.compile(
    r'^(Ireland|Europe(?: and the wider world)?)\s*:\s*Topic\s+(\d)\s*$', re.I)
# "A (30 marks)" heads an Ordinary topic's first priced part. 2021 Ordinary
# Early Modern prints "B 30 marks)" for Europe Topic 1 — the opening bracket is
# missing from the SEC's own page. It is a MISPRINT, recorded below rather than
# read by a loosened pattern, because a loosened pattern would also swallow a
# sentence that happens to end "... 30 marks)".
PART = re.compile(r'^([ABC])\s*\((\d{2})\s*marks\)\s*$')
MISPRINTS = {
    # (year, level, field): {printed line: the line the SEC meant}
    (2021, 'ol', 'em'): {'B 30 marks)': 'B (30 marks)'},
}
EXTRA = re.compile(r'^Answer the questions below if you are following the '
                   r'Alternative Instructions', re.I)
# "1." / "1. (a) ..." — a numbered ask at the margin.
QNUM = re.compile(r'^(\d{1,2})\.\s*(.*)$')
LETTER = re.compile(r'^\(([a-f])\)\s*(.*)$')
# The tariff the paper prints for an ask: "(20)", "(100)", "(40)".
TARIFF = re.compile(r'\((\d{2,3})\)\s*$')
# The SEC's attribution under a printed extract — never part of the ask.
SOURCE_LINE = re.compile(r'^(?:Source|Adapted from)\s*:', re.I)
# The dash the SEC sets around a document label is not always the ASCII one:
# 2022 uses U+2010 HYPHEN throughout, and the narrower class missed every
# document head on that paper.
DOCUMENT_HEAD = re.compile('^[\u2010-\u2015\\-]\\s*Document\\s+([AB])\\s*[\u2010-\u2015\\-]')
# The SEC drops the definite article on some papers: "Case study to which
# documents relate:". Requiring it left three Ordinary papers with no case
# study on their documents cards.
CASE_STUDY = re.compile(r'^Case study to which (?:the )?documents? relate', re.I)
COVER_MARKS = re.compile(r'Written examination:\s*(\d{3})\s*marks', re.I)


def lines(path):
    """(page, x0, text) for every printed line, in reading order."""
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
            for row in sorted(rows, key=lambda r: r['mid']):
                ws = sorted(row['w'])
                yield pno + 1, ws[0][0], ' '.join(w for _a, _b, w in ws)


class HistPaper:
    """One sitting of one field: every ask the paper prints.

    Keys are (section, q, letter, roman) so the ledger reads them in `sections`
    mode. `section` carries the topic and the Ordinary A/B/C part because that
    is how the paper addresses an ask — "Section 2 Topic 1 A" restarts at 1 in
    every topic, so a bare question number is not an address here.
    """

    def __init__(self, year, level, field):
        self.year, self.level, self.field = year, level, field
        self.path = os.path.join(papers_dir(),
                                 f'{year}-{level}-{field}-paper.pdf')
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self.asks = {}
        self.marks = {}
        self.stems = {}
        self.topic_titles = {}
        self.unit_marks = {}
        self.unit_pages = {}
        self.case_study = None
        self.case_title = None
        self.document_pages = []
        self.cover_marks = None
        self._read()

    # -- reading ---------------------------------------------------------
    def _read(self):
        misprints = MISPRINTS.get((self.year, self.level, self.field), {})
        section = None          # '1' | '2' | '3'
        topic = None            # int
        part = None             # 'A' | 'B' | 'C' | None
        extra = False
        want_title = None       # the topic title line expected next
        cur = None              # key currently accumulating
        buf = []
        stem_buf = []
        pending_q = None        # the DBQ question number, for its letters
        page = 1                # the page the current ask is printed on
        want_case = False       # the case-study title line expected next
        stem_closed = False     # the printed extract's attribution has begun

        def flush():
            nonlocal buf, cur
            if cur is not None and buf:
                self.unit_pages.setdefault(cur[0], page)
                text = ' '.join(' '.join(buf).split())
                m = TARIFF.search(text)
                if m:
                    # In the DBQ the tariff is printed once, under the LAST
                    # lettered part, and prices the whole question: "(20)" sits
                    # below (a)-(d) of Question 1, not beside (d). Filing it on
                    # (d) would put 20 marks on a part the scheme prices at 5.
                    owner = ('1', cur[1], None, None) if cur[0] == '1' else cur
                    self.marks[owner] = int(m.group(1))
                    text = TARIFF.sub('', text).strip()
                if text:
                    self.asks[cur] = (self.asks.get(cur, '')
                                      + ' ' + text).strip()
            buf = []

        def unit_key():
            """The section token an ask under the current heads belongs to."""
            if extra:
                # The paper heads this unit with no section and no topic, so
                # neither is invented: its address is what the scheme calls it,
                # "Extra Section A".
                return 'Extra A'
            if section == '1':
                return '1'
            token = f'{section} Topic {topic}'
            return f'{token} {part}' if part else token

        for pno, _x, raw in lines(self.path):
            page = pno
            line = ' '.join(raw.split())
            line = misprints.get(line, line)
            if not line:
                continue
            if self.cover_marks is None:
                m = COVER_MARKS.search(line)
                if m:
                    self.cover_marks = int(m.group(1))
            if DOCUMENT_HEAD.match(line):
                flush()
                cur = None
                if pno not in self.document_pages:
                    self.document_pages.append(pno)
                continue
            if END_OF_MATERIAL.match(line):
                flush()
                break
            m = SECTION.match(line)
            if m:
                flush()
                section, topic, part, cur, pending_q = m.group(1), None, None, None, None
                stem_closed = False
                stem_buf = []
                continue
            if EXTRA.match(line):
                flush()
                extra, part, cur, pending_q = True, 'A', None, None
                stem_closed = False
                stem_buf = []
                continue
            m = TOPIC.match(line)
            if m:
                flush()
                # The topic named directly under "SECTION 1" is the DBQ's own
                # case-study topic, not a Section 2/3 unit; Section 1 sets no
                # topics of its own, so it never opens one.
                if section == '1':
                    # The DBQ's own case-study topic — "Europe and the wider
                    # world: Topic 6" — printed under the Section 1 head. It is
                    # where the documents question's cards file, and (the extra
                    # Part A aside) the one topic Sections 2 and 3 leave out.
                    self.case_study = ('2' if m.group(1).lower() == 'ireland'
                                       else '3', int(m.group(2)))
                    want_title = None
                    continue
                topic, part, cur, pending_q = int(m.group(2)), None, None, None
                stem_closed = False
                # The SEC prints the topic's TITLE on the line under its
                # number, on the paper and in the scheme alike. It is the
                # wording evidence that a topic on one document is the topic
                # on the other — the join Law 4 demands, at the level where a
                # mis-numbering would swap thirteen asks at once.
                want_title = f'{section} Topic {topic}'
                stem_buf = []
                continue
            if want_title:
                self.topic_titles[want_title] = line
                want_title = None
                continue
            m = PART.match(line)
            if m and section in ('2', '3'):
                flush()
                part, cur, pending_q = m.group(1), None, None
                stem_closed = False
                stem_buf = []
                # The part's own printed ceiling, kept against the UNIT so it
                # can be checked against what the scheme prices: Part A's (30)
                # against five answers at (6), B's against "Max CM = 20 Max OE
                # = 10", C's against 30 + 10.
                self.unit_marks[unit_key()] = int(m.group(2))
                if part in ('B', 'C'):
                    # B and C are priced WHOLE — "B - Max CM = 20 marks Max OE
                    # = 10 marks" is the scheme's only entry for either — so
                    # the printed 1..4 under them are alternatives a candidate
                    # chooses between, not asks. The priced unit is the part.
                    cur = (unit_key(), None, None, None)
                    self.marks[cur] = int(m.group(2))
                continue
            if CASE_STUDY.match(line):
                # "Case study to which the documents relate:" heads the DBQ's
                # own subject on the next line. It is the paper's own words and
                # it is what a documents card is ABOUT, so it rides on the card
                # as its stem.
                want_case = True
                continue
            if want_case:
                self.case_title = line
                want_case = False
                continue
            if FURNITURE.match(line):
                continue
            if SOURCE_LINE.match(line):
                # The SEC's attribution under a printed extract, and it CLOSES
                # the extract: what follows it is the rest of the citation,
                # which wraps onto a second and sometimes a third line with no
                # marker of its own. Skipping only the "Source:" line left
                # "Language, Literature and History (Dublin, Trinity Irish
                # Studies, 2004)." on the end of the stem a student reads.
                stem_closed = True
                continue
            if section is None:
                continue

            if section == '1':
                m = QNUM.match(line)
                if m and int(m.group(1)) <= 9:
                    flush()
                    pending_q = int(m.group(1))
                    rest = m.group(2)
                    lm = LETTER.match(rest)
                    if lm:
                        cur = ('1', pending_q, lm.group(1), None)
                        buf = [lm.group(2)]
                    else:
                        cur = ('1', pending_q, None, None)
                        buf = [rest] if rest else []
                    continue
                m = LETTER.match(line)
                if m and pending_q is not None:
                    flush()
                    cur = ('1', pending_q, m.group(1), None)
                    # A question whose letters follow was opened letterless by
                    # the head line; that opening is the question's own lead-in
                    # and belongs to no leaf of its own.
                    self.asks.pop(('1', pending_q, None, None), None)
                    buf = [m.group(2)]
                    continue
                if cur is not None:
                    buf.append(line)
                continue

            # Sections 2 and 3.
            if part in ('B', 'C'):
                # The printed alternatives are the part's own choice list; they
                # are kept as its text so the card can show what was offered.
                if cur is not None:
                    buf.append(line)
                continue
            m = QNUM.match(line)
            if m and int(m.group(1)) <= 9:
                flush()
                cur = (unit_key(), int(m.group(1)), None, None)
                buf = [m.group(2)]
                if part == 'A' and stem_buf:
                    self.stems[unit_key()] = ' '.join(
                        ' '.join(stem_buf).split())
                    stem_buf = []
                continue
            if cur is not None:
                buf.append(line)
            elif (part == 'A' or extra) and not stem_closed:
                stem_buf.append(line)
        flush()
        # Every Ordinary A part carries the printed extract its questions ask
        # about; the stem is recorded against the unit, not the leaf, because
        # all five questions read the same extract.
        for key in list(self.asks):
            if key[0] in self.stems:
                pass

    # -- accessors -------------------------------------------------------
    def stem(self, key):
        return self.stems.get(key[0])

    def leaves(self):
        return sorted(self.asks, key=lambda k: tuple(str(x) for x in k))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=('hl', 'ol'))
    ap.add_argument('field', choices=('lm', 'em'))
    args = ap.parse_args()
    P = HistPaper(args.year, args.level, args.field)
    print(f'{P.path}  cover={P.cover_marks}  documents on page(s) '
          f'{P.document_pages}')
    for key in P.leaves():
        stem = P.stems.get(key[0])
        print(f'{str(key):<40} ({P.marks.get(key)})  {P.asks[key][:110]}')
        if stem and key[1] in (1, None):
            print(f'{"":<40} STEM {stem[:150]}')
    print(f'{len(P.asks)} ask(s)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
