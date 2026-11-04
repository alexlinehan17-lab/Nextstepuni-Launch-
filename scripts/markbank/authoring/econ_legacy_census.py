#!/usr/bin/env python3
"""Economics 2010-2020: the old-syllabus paper, read as the page sets it.

    python3 scripts/markbank/authoring/econ_legacy_census.py 2019 hl   # one paper, every leaf

The papers sat before the 2021 specification are a different examination from
the ones after it, and the generic merged walker (paper.py) read them as if
they were the same. It found 8 to 46 asks a paper where a hand count of the
page finds 55 to 75, for three reasons, each seen on the rendered pages:

  * Section B RESTARTS at Question 1. Section A prints nine short questions,
    1-9, and Section B eight long ones numbered 1-8 again. paper.py keeps one
    forward-only question counter per sitting, so every Section B head was
    rejected as going backwards and all eight long questions (about 55 asks)
    were filed as romans of Section A's Question 9.
  * Numbered TABLE ROWS read as heads. A true/false table prints its
    statements "1." to "4." (2019 HL Section A Q2), and the statement numbered
    3 became Question 3 while the real Question 3 ("Distinguish between the
    terms Economic Development and Economic Growth") was lost.
  * Ruled ANSWER SLOTS read as parts. "Outline two main contributions ...
    (i)____ (ii)____" is one ask with two lines to write on, not two asks.

What the pages print instead, measured over all 21 papers before this was
written: every paper has exactly seventeen question heads (9 + 8), each a BOLD
number at the left margin (x < 100pt); a table row is set in regular weight
further right. Every section opens on a banner that prints its marks,
"SECTION A (100 marks)" / "Section B (300 marks)" (the cover lists both, and
"Section B." also ends a footer sentence, so a banner without its marks is
not one). Part letters (a)-(c) and romans (i)-(iv) open their own printed
line. So this walker reads LINES with their position and weight, in reading
order, and keys every ask (section, question, letter, roman).

The same pages print the marks, which give an independent check: a Section A
question prints "(16 marks)" or "(17 marks)" once, and a Section B question
prints its parts' marks ("(30 marks)" in 2010-2018, "[25]" in 2019-2020) and
"[75 marks]" for the whole. A Section B question whose printed part marks do
not add up to its printed total has lost or gained a part, and is flagged.

Used by paper_census.census_subject for Economics sittings up to
LEGACY_LAST_YEAR; 2021 onwards is read by paper.py exactly as before.
"""
import os
import re
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paper as PP  # noqa: E402

LEGACY_LAST_YEAR = 2020

# A question head: the number and its full stop, bold, in the left margin.
HEAD = re.compile(r'^(\d{1,2})\s*\.(?=\s|$|\()')
HEAD_MAX_X = 100
# A section banner carries its marks; "(continued)" repeats the open section.
BANNER = re.compile(r'^(?:SECTION|Section)\s+([AB])\s*\(\s*\d+\s*marks\s*\)', re.I)
LETTER = re.compile(r'^\(([a-h])\)(?=\s|$|[A-Z_])')
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
ROMAN = re.compile(r'^\((i{1,3}|iv|vi{0,3}|ix|x)\)(?=\s|$|[A-Za-z_‘“(])')
# A marker that is a reference to a part, not the opening of one: "explain
# why ... in part (b) (i), explain" wraps so the address opens a line.
CROSSREF_AFTER = re.compile(r'^\s*(?:,|above\b|\)|and\b|or\b)')
CROSSREF_BEFORE = re.compile(r'\b(?:part|parts|Question|question)\s*$')
UNDERSCORES = re.compile(r'_{3,}')
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination,? \d{4}|Page \d+ of \d+|\d{1,2}'
    r'|Economics\s*[–—-]\s*(?:Higher|Ordinary) Level'
    r'|Remember to return this (?:examination|question) paper.*|(?:the )?[Qq]uestions in Section B\.?'
    r'|There is no examination material on this page'
    r'|Write your Examination Number here.*|Section B\.)\s*$')
SECTION_A_MARKS = re.compile(r'\(\s*(\d{1,3})\s*marks\s*\)', re.I)
QUESTION_TOTAL = re.compile(r'\[\s*(\d{1,3})\s*marks\s*\]', re.I)
# A part's marks, in the three forms the papers use: "(30 marks)" (2010,
# 2016-2018), a bare "(20)" closing its line (2011-2015 Higher) and "[25]"
# (2019-2020).
PART_MARKS = re.compile(r'\(\s*(\d{1,2})\s*marks\s*\)|\[\s*(\d{1,2})\s*\](?!\s*marks)'
                        r'|(?:^|\s)\(\s*(\d{1,2})\s*\)\s*$', re.I)


def _lines(path):
    """Every printed line of the paper in reading order: (page, x, text, bold).

    Lines a few points apart in y are one printed row (a head "7." sits 1.8pt
    below its own "(a)" on 2019 HL p4), and a row reads left to right.
    """
    out = []
    with fitz.open(path) as doc:
        for pno, page in enumerate(doc, 1):
            raw = []
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    spans = [s for s in line['spans'] if s['text'].strip()]
                    if not spans:
                        continue
                    text = ''.join(s['text'] for s in line['spans']).strip()
                    bold = 'Bold' in spans[0]['font'] or bool(spans[0]['flags'] & 16)
                    raw.append((spans[0]['bbox'][1], spans[0]['bbox'][0], text, bold))
            raw.sort()
            rows, cur, top = [], [], None
            for y, x, text, bold in raw:
                if cur and y - top > 3:
                    rows.append(cur)
                    cur = []
                if not cur:
                    top = y
                cur.append((x, text, bold))
            if cur:
                rows.append(cur)
            for row in rows:
                for x, text, bold in sorted(row):
                    out.append((pno, x, PP.unligature(text), bold))
    return out


def census_legacy(year, level, path=None):
    """(parts, texts, files, marks, flags) for one old-syllabus paper.

    parts: every leaf ask keyed (section, q, letter, roman); a question that
    prints no part is keyed whole, (section, q, None, None).
    marks: {(section, q): printed marks} for the cross-year checksum.
    flags: this layout's own checks (part marks against the question total).
    """
    if path is None:
        path = os.path.join(PP.papers_dir('economics'), f'{year}-{level}-paper.pdf')
    lines = _lines(path)
    parts, stems = {}, {}
    q_marks, part_marks = {}, {}
    section = q = letter = roman = None
    prev_text = ''

    def key():
        return (section, q, letter, roman)

    for i, (pno, x, text, bold) in enumerate(lines):
        b = BANNER.match(text)
        if b:
            # Sections only move forward, and only once the open one holds an
            # ask: the cover lists both banners before the paper begins.
            if b.group(1) != section and (section is None or (
                    b.group(1) > section and any(k[0] == section for k in parts))):
                section, q, letter, roman = b.group(1), None, None, None
            continue
        if section is None:
            continue
        rest = text
        h = HEAD.match(rest)
        if h and bold and x < HEAD_MAX_X:
            n = int(h.group(1))
            if (q is None and n == 1) or (q is not None and q < n <= q + 2):
                q, letter, roman = n, None, None
                parts.setdefault(key(), [])
                rest = rest[h.end():].strip()
                prev_text = ''
        if q is None:
            continue
        # Part markers opening the line, possibly several: "1. (a) (i) Define".
        while rest:
            lm = LETTER.match(rest)
            rm = ROMAN.match(rest)
            m = lm or rm
            if not m:
                break
            after = rest[m.end():]
            if CROSSREF_AFTER.match(after) or (rest is text and CROSSREF_BEFORE.search(prev_text)):
                break
            # These papers print the letter ABOVE the roman, "(a) (i)". A letter
            # after a roman that has no letter over it labels a row inside that
            # roman: 2020 HL Section A Q4(ii) is "Tick one option only" over a
            # table whose rows are lettered (a)-(c).
            if lm and (letter is None or lm.group(1) > letter) and not (letter is None and roman):
                letter, roman = lm.group(1), None
                parts.setdefault(key(), [])
                rest = after.strip()
                continue
            # A roman not yet printed under the open letter. Not "the next one
            # due": 2015 OL Section A Q1 numbers four blanks (i)-(iv) in a grid
            # of two rows, read (ii) (iv) then (i) (iii).
            if rm and (section, q, letter, rm.group(1)) not in parts:
                tail = after.strip()
                nxt = lines[i + 1][2] if i + 1 < len(lines) else ''
                # A ruled answer slot: the numeral labels a line to write on.
                if tail.startswith('_') or (not tail and nxt.startswith('_')):
                    rest = UNDERSCORES.sub(' ', tail).strip()
                    break
                roman = rm.group(1)
                parts.setdefault(key(), [])
                rest = tail
                continue
            break
        rest = UNDERSCORES.sub(' ', rest).strip()
        if rest and not FURNITURE.match(rest):
            parts.setdefault(key(), []).append(rest)
            # The marks the page prints, read where they are printed.
            tm = QUESTION_TOTAL.search(rest)
            if tm:
                q_marks[(section, q)] = int(tm.group(1))
            elif section == 'A':
                am = SECTION_A_MARKS.search(rest)
                if am and (section, q) not in q_marks:
                    q_marks[(section, q)] = int(am.group(1))
            else:
                for pm in PART_MARKS.finditer(rest):
                    part_marks.setdefault((section, q), []).append(int(pm.group(1) or pm.group(2) or pm.group(3)))
            prev_text = rest

    # Text printed before a question's first part is its stem; a question
    # with parts is not itself an ask, and one without is asked whole.
    leaves = {}
    for k, v in parts.items():
        if k[2] is None and k[3] is None:
            stems[k] = v
            if any(o[:2] == k[:2] and (o[2] or o[3]) for o in parts):
                continue
        leaves[k] = v
    texts = {k: ' '.join(' '.join(v).split()) for k, v in leaves.items()}
    flags = []
    for (sec, n), total in sorted(q_marks.items()):
        if sec == 'B':
            got = part_marks.get((sec, n), [])
            if sum(got) != total:
                flags.append({'type': 'marks-checksum', 'where': f'Section B Q{n}',
                              'detail': f'printed part marks {got} sum {sum(got)}, question prints {total}'})
    for n in range(1, 10):
        if ('A', n) in {k[:2] for k in leaves} and ('A', n) not in q_marks:
            flags.append({'type': 'marks-checksum', 'where': f'Section A Q{n}',
                          'detail': 'no printed marks found'})
    return set(leaves), texts, [path], q_marks, flags


def _label(k):
    sec, q, letter, roman = k
    return f'Section {sec} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


def leaves_only(parts):
    """The asks a student answers: a letter with romans under it is not one."""
    return {k for k in parts if not (k[3] is None and k[2] is not None and any(
        o[:3] == k[:3] and o[3] for o in parts))}


def main():
    year, level = int(sys.argv[1]), sys.argv[2]
    parts, texts, _, marks, flags = census_legacy(year, level)
    leaves = leaves_only(parts)
    order = sorted(leaves, key=lambda k: (k[0], k[1], k[2] or '', ROMANS.index(k[3]) if k[3] else -1))
    for k in order:
        print(f'{_label(k):24} {texts[k][:110]}')
    print(f'{year} {level}: {len(leaves)} asks '
          f'(A {sum(k[0] == "A" for k in leaves)}, B {sum(k[0] == "B" for k in leaves)}), '
          f'marks {sum(marks.values())} over {len(marks)} questions')
    for f in flags:
        print('  FLAG', f)


if __name__ == '__main__':
    main()
