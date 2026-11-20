#!/usr/bin/env python3
"""Lithuanian listening answers, read from the scheme's own lines.

    python3 scripts/markbank/authoring/lt_listen.py 2024 hl      # one sitting
    python3 scripts/markbank/authoring/lt_listen.py --coverage   # every sitting, against the paper

languages-q3 lane, 20 Nov 2026. lt_scheme.listening() is shared with Latvian
and Czech and reads only Question 1 of each section ("1. (a)"), so the
Lithuanian listening cards read the answers here instead, without touching
the shared reader (lead ruling, 20 Nov 2026).

The listening part of a Lithuanian scheme (2022-2026) is regular:

    Section B (21 Marks)
    Answer the questions in Lithuanian.
    1. (a) Kas buvo Mikalojus Konstantinas Čiurlionis? Parašykite dvi 4 marks (2 x 2)
    detales.
    Any two of:
    • Dailininkas
    ...
    (b) Parašykite dvi detales apie Čiurlionio butą. 4 marks (2 x 2)

An ask opens on its printed head: a number and a letter ("1. (a)"), a letter
alone under the current number ("(b)"), or a number alone ("3. Kur ..."). It
holds every line up to the next head, section, page furniture or the CD
script. Nothing here is guessed: each record names the scheme lines it was
read from, and the cards lift their rows from those lines (lt_specs.py).

The re-extracted 2023 and 2026 Higher schemes carry a "<!-- columns -->"
reading after each page (extract-scheme.py --columns); it is skipped here,
since the page's own rows already hold the same words in reading order.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCHEMES = os.path.join(ROOT, 'examiner-reports', 'lithuanian', 'schemes')

START = re.compile(r'^Listening Comprehension Test\b')
END = re.compile(r'^(APPENDIX|CD SCRIPT|<!-- markbank:column-runs)')
SECTION = re.compile(r'^Section ([A-E])\b')
HEAD_NUM = re.compile(r'^(\d{1,2})\.\s*(?:\(([a-h])\)\s*)?(.*)$')
HEAD_LET = re.compile(r'^\(([a-h])\)\s*(.*)$')
BULLET = re.compile(r'^[•]\s*')
DIRECTIVE = re.compile(r'^(One of|Any (?:one|two|three|four|five) of|Any \d of)\s*:?\s*$', re.I)
# A price as the scheme prints it: "4 marks", "3 Marks", "1 mark", optionally
# followed by a split "(2 x 2)" / "(2 × 3 marks)".
PRICE = re.compile(r'(\d{1,2})\s*[Mm]arks?\b(?:\s*\((\d)\s*[x×]\s*(\d{1,2})(?:\s*[Mm]arks?)?\))?')
SPLIT = re.compile(r'\((\d)\s*[x×]\s*(\d{1,2})(?:\s*[Mm]arks?)?\)')
PAGE_NO = re.compile(r'^\d{1,3}$')
# The head of a true/false tick grid (CARD-STANDARD 10c: one ask, folded).
TICK_HEAD = re.compile(r'true or false|Mark the correct and incorrect|teisingus ir neteisingus|Pažymėkite', re.I)
TF_HEADER = re.compile(r'^(True\s+False|Teisingai\s+Neteisingai|Teisingas\s+Neteisingas|T\s+F)$', re.I)
INSTRUCTION = re.compile(r'^Answer the questions? in (Lithuanian|English)\.?$', re.I)
GENERAL = re.compile(r'^(General observations|N\.B\.|\d\.\s+(Accept|Serious|If both)|If the correct|marking scheme|If both|Serious)', re.I)


class Ask:
    def __init__(self, section, q, letter, line):
        self.key = ('L' + section, q, letter, None)
        self.head = [line]          # scheme line numbers of the head (a wrapped head runs on)
        self.lines = []             # every line number after the head, up to the next ask
        self.language = None
        self.note = None            # what the scheme's print of the head leaves out
        self.section_lines = []     # the section's own lines before its first ask (a section-wide price)

    def __repr__(self):
        return f'Ask({self.key} head={self.head} lines={self.lines[:3]}...)'


def scheme_lines(year, level):
    with open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf-8') as fh:
        return fh.read().split('\n')


def asks(year, level):
    """{key: Ask} for the listening part of one sitting's scheme."""
    raw = scheme_lines(year, level)
    out, order = {}, []
    inside, skipping, section, q, cur, language = False, False, None, None, None, None
    section_lines = []
    table = False                   # inside a true/false table opened under the current head
    for n, line in enumerate(raw, 1):
        t = line.strip()
        if not inside:
            inside = bool(START.match(t))
            continue
        if END.match(t):
            break
        if t.startswith('## Page'):
            skipping = False
            continue
        if t == '<!-- columns -->':
            skipping = True
            continue
        if skipping or not t or PAGE_NO.match(t):
            continue
        m = SECTION.match(t)
        if m:
            section, q, cur, table = m.group(1), None, None, False
            section_lines = []
            continue
        if TF_HEADER.match(t) or re.fullmatch(r'Statement\s+True\s+False', t, re.I):
            table = True
            if cur is not None:
                cur.lines.append(n)
            else:
                section_lines.append(n)
            continue
        m = INSTRUCTION.match(t)
        if m:
            language = m.group(1)
            continue
        if section is None:
            continue
        m = HEAD_NUM.match(t)
        if m and not GENERAL.match(t):
            q = int(m.group(1))
            cur = Ask(section, q, m.group(2), n)
            cur.language = language
            cur.section_lines = list(section_lines)
            table = False
            if cur.key in out:
                raise ValueError(f'{year} {level}: {cur.key} printed twice (lines {out[cur.key].head[0]}, {n})')
            out[cur.key] = cur
            order.append(cur.key)
            continue
        m = HEAD_LET.match(t)
        # A lettered line inside a true/false table is a statement of the grid,
        # not a new ask: it carries a tick (here or on its next line) and no
        # price. A head carries a price.
        if m and table and not PRICE.search(t):
            cur.lines.append(n)
            continue
        if m and q is None and TICK_HEAD.search(t):
            # 2024 OL Section C prints its first question, a tick grid, as
            # "(a) Indicate whether ..." with no number: the paper's Q1.
            q = 1
            cur = Ask(section, q, None, n)
            cur.language = language
            cur.note = 'the scheme prints this grid as "(a)" with no question number; the paper prints it as Question 1'
            out[cur.key] = cur
            order.append(cur.key)
            table = False
            continue
        if m and q is not None:
            cur = Ask(section, q, m.group(1), n)
            cur.language = language
            cur.section_lines = list(section_lines)
            table = False
            if cur.key in out:
                raise ValueError(f'{year} {level}: {cur.key} printed twice (lines {out[cur.key].head[0]}, {n})')
            out[cur.key] = cur
            order.append(cur.key)
            continue
        if cur is None:
            section_lines.append(n)
            continue
        if cur is not None:
            # A wrapped head: a line before any bullet or directive that is
            # neither, read as the rest of the question.
            # (A head already priced is complete: an unbulleted line after it
            # is the answer, printed without a bullet.)
            head_text = ' '.join(raw[x - 1] for x in cur.head)
            if not cur.lines and not BULLET.match(t) and not DIRECTIVE.match(t) and not _price_only(t) \
                    and not PRICE.search(head_text) and not SPLIT.search(head_text):
                cur.head.append(n)
            else:
                cur.lines.append(n)
    return {k: out[k] for k in order}


def _price_only(t):
    """A line that is only a price or a split: "(2 x 3)", "4 marks"."""
    return bool(re.fullmatch(r'(?:\d{1,2}\s*[Mm]arks?)?\s*(?:\(\d\s*[x×]\s*\d{1,2}(?:\s*[Mm]arks?)?\))?', t)) and bool(t)




def paper_listening_keys(year, level):
    sys.path.insert(0, HERE)
    import lt_paper
    P = lt_paper.LtPaper(year, level)
    return [a.key for a in P.aural_asks()]


def coverage():
    """Every listening ask the paper prints, against the scheme's heads."""
    bad = 0
    for year in range(2022, 2027):
        for level in ('hl', 'ol'):
            paper = paper_listening_keys(year, level)
            have = asks(year, level)
            # The paper keys a row of a tick grid with a roman; the scheme heads
            # the grid once (CARD-STANDARD 10c folds it, LT_FOLDED_ASKS).
            # A row of a folded grid is met by the grid's own head: a roman row
            # under a letter (k[:3]) or a lettered statement under a number (k[:2]).
            missing = [k for k in paper if k not in have and k[:3] + (None,) not in have
                       and k[:2] + (None, None) not in have]
            extra = [k for k in have if k not in paper and not any(p[:3] == k[:3] for p in paper)]
            bad += len(missing) + len(extra)
            print(f'{year} {level}: paper {len(paper)} listening asks; scheme heads {len(have)}; '
                  f'lifted {len(paper) - len(missing)}/{len(paper)}'
                  + (f'; MISSING {missing}' if missing else '') + (f'; EXTRA {extra}' if extra else ''))
    return bad


def main():
    if sys.argv[1:2] == ['--coverage']:
        raise SystemExit(1 if coverage() else 0)
    year, level = int(sys.argv[1]), sys.argv[2]
    raw = scheme_lines(year, level)
    for k, a in asks(year, level).items():
        print(k, a.language, '| head:', ' / '.join(raw[n - 1].strip() for n in a.head)[:110])
        for n in a.lines:
            print(f'     {n}: {raw[n - 1].strip()[:110]}')


if __name__ == '__main__':
    main()
