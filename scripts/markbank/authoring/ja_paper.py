#!/usr/bin/env python3
"""Japanese question papers — every ask the SEC printed, and where.

    python3 scripts/markbank/authoring/ja_paper.py 2024 hl
    python3 scripts/markbank/authoring/ja_paper.py 2024 ol --aural
    python3 scripts/markbank/authoring/ja_paper.py --all

The shape of the paper
----------------------
A sitting is two booklets printed the same afternoon: the written paper (SEC
component 000) and the Listening Comprehension Test (component A00). Both are
printed BILINGUALLY, and the two levels do it differently — Higher sets Irish
and English on one line divided by a slash, Ordinary sets them in two columns.
`ja_text.page_rows` cuts a row into its gap groups so both read the same way.

The written booklet sets five questions, headed in Japanese: 問題1 … 問題5.
Questions 1-3 are reading comprehension and questions 4-5 are written
production. Inside a question the SEC heads its parts either "Cuid A / Part A"
(Higher's question 1) or with a bare letter at the margin — "A:", "B: KANJI",
"C: GRAMADACH / GRAMMAR" — and each part numbers its own items from 1, or
prints bare romans with no number above them at all.

So the ADDRESS of an ask is the question, the part, the item and the roman,
and the census's section token carries the first two: "2B" is 問題2's Part B,
the kanji section, and "LC" is the listening booklet's Part C. A citation
reads "2024 HL Section 2B Q1(i)".

What this reader had to be told
-------------------------------
* **An uppercase letter at the margin is a part head; the same letter indented
  is a multiple-choice option.** 2025 Ordinary question 3 prints "A. a chef",
  "B. a maths teacher" under its own "A. Freagair ceisteanna 1-3", and reading
  those as part heads invented four parts and lost the asks under the real one.
  The page's own margin separates them, and MARGIN is measured per booklet.
* **The cloze numbers its blanks inside the sentence, not at the margin.**
  Question 4 at Ordinary prints a passage with twelve numbered gaps —
  "(i) ＿＿＿ 日本にいます。" in 2024, "(2) ＿＿＿の朝に" in 2025 — which is
  twelve asks the scheme prices at three marks each. No marker opens a line,
  so a part that opens no marker at the margin is re-read for INLINE blanks
  before it is called a single whole ask.
* **"e.g." is not an ask.** Every matching, kanji and grammar part prints a
  worked example first, in the same shape as the items under it.
"""
import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

from ja_text import doc_rows, page_count                       # noqa: E402

SUBJECT = 'japanese'
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
          'xi', 'xii', 'xiii', 'xiv', 'xv']


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, component='000', subject=SUBJECT):
    return os.path.join(papers_dir(subject),
                        f'{year}-{level}-{component}-paper.pdf')


# A furigana gloss, folded in by ja_text. Stripped before any marker or head is
# matched: 問（もん）題（だい）3 and 問題（もんだい）3 are the same head, and
# only one of them survives a regex written against the printed characters.
RUBY = re.compile(r'（[぀-ヿ々ー]+）')


def plain(text):
    return RUBY.sub('', text)


# 問題 N — the paper's own question head, printed in Japanese at both levels.
Q_HEAD = re.compile(r'問\s*題\s*(\d{1,2})\b')
# "A:", "B.", "C ：" at the margin, and Higher question 1's "Cuid A / Part A".
PART_HEAD = re.compile(r'^([A-D])\s*[:.：]')
PART_CUID = re.compile(r'(?:Cuid|Part)\s*([A-D])\b')
# The listening booklet's own four parts.
# The listening booklet heads its parts in capitals and without punctuation --
# "CUID A" beside "PART A" -- where the written booklet heads "Cuid A / Part A".
AURAL_PART = re.compile(r'^(?:Cuid|Part)\s*([A-D])\b', re.I)

NUM_MARK = re.compile(r'^(\d{1,2})\s*[.)．]\s*')
LETTER_MARK = re.compile(r'^\(\s*([a-h])\s*\)\s*')
# A roman is matched as a RUN of roman letters and then checked against the
# list, because an alternation ordered by hand drops one: written
# `x?i{1,3}|iv|vi{0,3}|ix|xi{1,3}` it silently refused a bare "x", and the
# thirteen-item kanji section of 2024 Ordinary censused twelve asks.
ROMAN_MARK = re.compile(r'^\(\s*([ivx]{1,5})\s*\)\s*', re.I)
# The cloze's inline gaps: "(i) ＿＿＿" and "(2) ＿＿＿", numbered inside the
# sentence they interrupt.
INLINE_BLANK = re.compile(r'\(([ivx]{1,5}|\d{1,2})\)\s*[_＿]', re.I)
EG = re.compile(r'^\(?\s*e\.?\s*g\.?\s*\)?[.\s]', re.I)
RULE = re.compile(r'[_＿]{3,}')

# Where a part stops printing what the candidate READS and starts printing what
# the candidate ANSWERS. Question 1 sets a web page whose menu is a numbered
# list -- "1. ホーム 2. ポッキーの歴史 ... 10. ポッキーのアウトレット" -- printed
# in exactly the shape its asks are printed in, and reading those as asks
# invented six leaves per sitting and lost the matching task under them. The
# SEC always divides the two with an instruction, in Irish and in English, and
# that instruction is the cut. The row carrying it may itself be the first ask
# ("1. Scríobh uimhir an naisc mar atá sa sampla."), so the cut INCLUDES it.
RUBRIC = re.compile(
    r'\b(?:Freagair|Answer|Scr[íi]obh|Write|Comhl[áa]naigh|Complete'
    r'|Cuir\s+(?:ciorcal|isteach|tic)|Circle|Insert|Indicate|Tick'
    r'|Aistrigh|Translate|Liostaigh|List\b|Tabhair|Give|Ainmnigh|Name'
    r'|D[ée]an\s+cur\s+s[íi]os|Describe|Mention|Roghnaigh|Choose'
    r'|C[ée]n\b|Cad\b|Conas\b|Cathain|C[áa]\b|What\b|Why\b|How\b'
    r'|When\b|Where\b|Which\b|Who\b)', re.I)
LATIN = re.compile(r'[A-Za-z\u00c0-\u017f]{3,}')

# Page furniture, and the front matter that carries an "A." of its own.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate Examination|Scr[úu]d[úu] na hArdteistim'
    r'|Japanese\s*[—–-]|Seap[áa]inis\s*[—–-]|N[áa] scr[íi]obh'
    r'|Do not write|F[óo]gra c[óo]ipchirt|Copyright notice'
    r'|Focl[óo]ir\s*/\s*Vocabulary|Leathanach|Blank Page)', re.I)
COVER = re.compile(r'SCR[ÚU]DUIMHIR|FREAGRA[ÍI]ODH|STAMPA AN IONAID'
                   r'|Coimisi[úu]n na Scr[úu]duithe|OBAIR SCR[ÍI]OFA'
                   r'|WRITTEN PRODUCTION', re.I)


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'page')

    def __init__(self, section, q, letter, roman, text, page):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.page = text, page

    @property
    def key(self):
        return (self.section, self.q, self.letter, self.roman)

    def __repr__(self):
        return f'<Ask {self.key} {self.text[:48]!r} p{self.page + 1}>'


class Node:
    """One printed marker inside one part, and the markers beneath it."""

    def __init__(self, q, letter, roman, text, page):
        self.q, self.letter, self.roman = q, letter, roman
        self.text, self.page = text, page
        self.kids = []


class JaPaper:
    """The two booklets of one sitting, read as one paper."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, '000', subject)
        aural = paper_path(year, level, 'A00', subject)
        self.aural_path = aural if os.path.exists(aural) else None
        self._written = None
        self._aural = None
        self.question_marks = {}
        self.section_pages = {}

    # ---------------------------------------------------------- written ---
    @property
    def written(self):
        if self._written is None:
            self._written = self._walk_written()
        return self._written

    def _margin(self, rows):
        """The x the paper sets its own part heads at.

        Measured per booklet rather than assumed: Higher sets its margin at
        42.5 and Ordinary at 56.7, and a fixed threshold read one level's
        multiple-choice options as the other level's part heads. It is the
        MODE of the page's own left edges, not the minimum: 2024 Ordinary
        sets one rubric four points inside the trim at x=19, and reading that
        as the margin put every 問題 head outside it and censused the paper at
        zero asks.
        """
        xs = collections.Counter(round(g[0]) for _p, groups in rows
                                 for g in groups[:1])
        return (xs.most_common(1)[0][0] + 8) if xs else 0

    def _walk_written(self):
        rows = doc_rows(self.path)
        margin = self._margin(rows)
        section = None
        q = None
        parts = collections.OrderedDict()     # section token -> [(x, text, page)]
        for pno, groups in rows:
            joined = plain(' '.join(t for _x, _x1, t in groups))
            if pno == 0 or COVER.search(joined):
                head = Q_HEAD.search(joined)
                if not head:
                    if q is not None and re.search(
                            r'OBAIR SCR[ÍI]OFA|WRITTEN PRODUCTION', joined, re.I):
                        continue
                    continue
            head = Q_HEAD.search(joined)
            if head and groups[0][0] <= margin + 12:
                q = int(head.group(1))
                section = str(q)
                parts.setdefault(section, [])
                self.section_pages.setdefault(section, []).append(pno)
                m = re.search(r'\((\d{1,3})\s*mar[ck]', joined)
                if m:
                    self.question_marks.setdefault(q, int(m.group(1)))
                cuid = PART_CUID.search(joined)
                if cuid:
                    section = f'{q}{cuid.group(1)}'
                    parts.setdefault(section, [])
                    self.section_pages.setdefault(section, []).append(pno)
                continue
            if q is None:
                continue
            first_x, _x1, first_t = groups[0]
            ft = plain(first_t)
            cuid = PART_CUID.match(ft)
            ph = PART_HEAD.match(ft)
            if (cuid or (ph and first_x <= margin)) and not FURNITURE.match(ft):
                letter = (cuid or ph).group(1)
                section = f'{q}{letter}'
                parts.setdefault(section, [])
                self.section_pages.setdefault(section, []).append(pno)
                rest = ft[(cuid or ph).end():].strip()
                row = ([(first_x, rest)] if rest else []) + \
                      [(g[0], plain(g[2])) for g in groups[1:]]
                if row:
                    parts[section].append((row, pno))
                continue
            if section is None:
                continue
            self.section_pages.setdefault(section, []).append(pno)
            row = [(x, plain(t)) for x, _x1, t in groups
                   if not FURNITURE.match(plain(t))]
            if row:
                parts[section].append((row, pno))
        return {k: v for k, v in parts.items() if v}

    def asks(self):
        """Every leaf ask the written booklet prints, in printed order."""
        out = []
        lettered = {s[0] for s in self.written if len(s) > 1}
        for section, rows in self.written.items():
            # The rows a question prints BEFORE its first part head are its
            # stimulus -- the web page, the article, the blog the parts are
            # about. A question that heads parts sets no ask of its own.
            if len(section) == 1 and section in lettered:
                continue
            out.extend(_section_asks(section, rows))
        return out

    # ------------------------------------------------------------ aural ---
    def aural_asks(self):
        if self.aural_path is None:
            return []
        if self._aural is None:
            self._aural = self._walk_aural()
        return self._aural

    def _walk_aural(self):
        # The COVER is skipped whole. It prints a marking table listing "Cuid A
        # / Part A" down to "Cuid D / Part D" for the examiner to total, in
        # exactly the shape the part heads inside the booklet take, and reading
        # those as heads opened four empty parts before the booklet began.
        rows = doc_rows(self.aural_path, page_from=1)
        section = None
        parts = collections.OrderedDict()
        for pno, groups in rows:
            first_x, _x1, first_t = groups[0]
            ft = plain(first_t)
            m = AURAL_PART.match(ft)
            # A head is the WHOLE of its group ("CUID A", "PART A"). The
            # booklet's own margin moves page to page -- 62 on the table page,
            # 41 on the next -- so an x threshold read one level's first part
            # as body text and lost it.
            if m and not ft[m.end():].strip():
                section = f'L{m.group(1)}'
                parts.setdefault(section, [])
                rest = ft[m.end():].strip()
                row = ([(first_x, rest)] if rest else []) + \
                      [(g[0], plain(g[2])) for g in groups[1:]]
                if row:
                    parts[section].append((row, pno))
                continue
            if section is None:
                continue
            row = [(x, plain(t)) for x, _x1, t in groups
                   if not FURNITURE.match(plain(t))]
            if row:
                parts[section].append((row, pno))
        out = []
        for section, rows_ in parts.items():
            out.extend(_section_asks(section, rows_))
        return out

    def all_asks(self):
        return self.asks() + self.aural_asks()


def _read_marker(text):
    """(the address a group opens, in PRINTED order, and the text after it).

    The order is not fixed: the written booklet prints "問題4 (a) (i)" — letter
    outside, roman inside — and the listening booklet prints "1. (iii) (a)",
    the other way round. Both are read as they are printed and the depth is
    settled afterwards, in `_section_asks`.
    """
    found, rest = [], text
    n = NUM_MARK.match(rest)
    if n:
        found.append(('num', int(n.group(1))))
        rest = rest[n.end():]
    for _ in range(2):
        r = ROMAN_MARK.match(rest)
        if r and r.group(1).lower() in ROMANS:
            found.append(('roman', r.group(1).lower()))
            rest = rest[r.end():]
            continue
        l = LETTER_MARK.match(rest)
        if l:
            found.append(('letter', l.group(1)))
            rest = rest[l.end():]
            continue
        break
    return (found, rest.strip()) if found else None


def _markers(rows):
    """[(address, text, page)] for every marker a part opens.

    A marker is read off the groups a row OPENS with, and a group is only read
    once every group to its left has been a BARE marker. 2024 Higher question 3
    prints its multiple-choice readings as gap groups of their own -- "(i) 高校
    | (a) がっこう | (b) こうこう | (c) たかこう | (d) ここ" -- and reading those
    as lettered parts turned six asks into four options and eight phantoms.
    """
    out = []
    for r, (row, page) in enumerate(rows):
        for i, (_x, t) in enumerate(row):
            if EG.match(t):
                break
            got = _read_marker(t)
            if got is None:
                break
            found, rest = got
            tail = ' '.join(t2 for _x2, t2 in row[i + 1:])
            text = RULE.sub(' ', f'{rest} {tail}').strip()
            out.append((found, ' '.join(text.split()), page, r))
            if rest:
                break
    return out


def _first_rubric(rows):
    """The row a part prints its first instruction on. See RUBRIC."""
    for i, (row, _page) in enumerate(rows):
        joined = ' '.join(t for _x, t in row)
        if LATIN.search(joined) and RUBRIC.search(joined):
            return i
    return 0


def _section_asks(section, rows):
    """The leaves one part prints, from its own printed markers."""
    # The cloze numbers its gaps INSIDE the sentence they interrupt, so most of
    # them open no row and the few that do would be the only asks read. Five
    # numbered gaps in one part is the cloze and nothing else in the paper.
    blanks = _inline_blanks(rows)
    marks = [] if len(blanks) >= 5 else _markers(rows)
    # Everything the SEC asks, it asks in Irish and in English. A marker
    # printed BEFORE the part's own instruction and carrying no Latin script is
    # therefore not an ask but a numbered piece of the STIMULUS -- question 1's
    # web page prints its menu as "1. ホーム 2. ポッキーの歴史 … 10. ポッキーの
    # アウトレット", ten markers in exactly the shape its asks take.
    #
    # Cutting the rows at the instruction instead lost the item head of every
    # listening part, whose own "1. Zoom call before Yuji's arrival" is printed
    # ABOVE the first question and reads as an instruction to nothing.
    first = _first_rubric(rows)
    marks = [m for m in marks if m[3] >= first or LATIN.search(m[1])]
    if not marks:
        if blanks:
            return [Ask(section, None, None, b, text, page)
                    for b, text, page in blanks]
        text = ' '.join(t for row, _p in rows for _x, t in row)[:400]
        page = rows[0][1] if rows else 0
        return [Ask(section, None, None, None, text, page)]

    # Build the tree in printed order, de-duplicating the bilingual reprint:
    # the same address printed twice is one ask, and the longer text wins.
    #
    # An address is at most TWO levels deep below the part. The written booklet
    # never prints three; the listening booklet does — "1. (iii) (a) Where is
    # Yuji's room? (b) Describe Yuji's room" — and there the printed order puts
    # the roman outside the letter, which the (question, letter, roman) key
    # cannot hold without citing an address the paper does not print. So the
    # ROMAN is the leaf there and the letters beneath it are folded into it:
    # what they split is one segment of one recording, and every ask in that
    # booklet is excluded from the bank in any case (see the exclusions file).
    tree = collections.OrderedDict()
    cur = []
    for found, rest, page, _row in marks:
        # Where the marker sits is decided by the path already open, not by a
        # fixed letter-then-roman order: a token of a type the path already
        # holds is a SIBLING of it, and a token of a type it does not hold is
        # one level DEEPER. That is what lets 問題3 at Ordinary number "1.(a)"
        # and "2.(i)" under one part head, and 問題4 at Higher nest "(a)(i)"
        # with no number above either.
        path = list(cur)
        for kind, tok in found:
            if kind == 'num':
                path = [(kind, tok)]
                continue
            at = next((j for j, (k, _t) in enumerate(path) if k == kind), None)
            if at is None and kind == 'letter' and path and path[-1][0] == 'roman':
                # A LETTER beneath a ROMAN is never an ask of its own. At
                # Ordinary it is a multiple-choice option — 2021's listening
                # test prints "(iii) The restaurant is open (a) from 9am to
                # 10pm (b) for 90 minutes every day (c) … (d) …", and reading
                # those four as asks quadrupled that booklet's denominator. At
                # Higher it is the scheme's own split of one recorded segment
                # ("(ii) (a) Where is Yuji's room? (b) Describe Yuji's room"),
                # which reconcile already grants through the part the scheme
                # priced it under. Either way the roman is the leaf.
                continue
            path = (path[:at] if at is not None else path) + [(kind, tok)]
        path = path[:2]
        cur = path
        num = letter = roman = None
        for kind, tok in path:
            if kind == 'num':
                num = tok
            elif kind == 'letter':
                letter = tok
            else:
                roman = tok
        key = (num, letter, roman)
        if not rest and (letter or roman):
            # An ANSWER SLOT, not an ask. The Ordinary paper rules its answer
            # spaces "(i) ____ (ii) ____ (iii) ____" under a question the
            # scheme prices whole ("Name three sports available at Tokyo Dome
            # ... any 3, 1 mark each (3 marks)"), in the same shape it prints a
            # real sub-part in. A sub-part always carries printed words; a slot
            # never does.
            continue
        prev = tree.get(key)
        if prev is None:
            tree[key] = (rest, page)
        elif rest and rest not in prev[0]:
            # Everything below the second level is folded into the leaf above
            # it: the listening booklet prints "1. (iii) (a) Where is Yuji's
            # room? (b) Describe Yuji's room", and a (question, letter, roman)
            # key cannot hold a roman OUTSIDE a letter without citing an
            # address the paper never prints. Every ask in that booklet is
            # excluded from the bank in any case (see the exclusions file).
            tree[key] = ((prev[0] + ' ' + rest).strip(), prev[1])

    # A leaf is a node nothing hangs beneath.
    keys = list(tree)
    leaves = []
    for num, letter, roman in keys:
        deeper = any(
            (n == num and (letter is None or l == letter)
             and (l, r) != (letter, roman)
             and (letter is None and l is not None
                  or roman is None and r is not None))
            for n, l, r in keys)
        if deeper:
            continue
        text, page = tree[(num, letter, roman)]
        leaves.append(Ask(section, num, letter, roman, text, page))
    leaves.sort(key=lambda a: (a.q or 0,
                               'abcdefghijkl'.index(a.letter) if a.letter else -1,
                               ROMANS.index(a.roman) if a.roman else -1))
    return leaves


def _inline_blanks(rows):
    out, seen = [], set()
    for row, page in rows:
      for _x, t in row:
        for m in INLINE_BLANK.finditer(t):
            tok = m.group(1).lower()
            tok = tok if tok in ROMANS else tok
            if tok in seen:
                continue
            seen.add(tok)
            out.append((tok, ' '.join(RULE.sub(' ', t).split()), page))
    return out


def sittings(subject=SUBJECT):
    out = set()
    for f in sorted(os.listdir(papers_dir(subject))):
        m = re.match(r'^(\d{4})-(hl|ol)-000-paper\.pdf$', f)
        if m:
            out.add((int(m.group(1)), m.group(2)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--aural', action='store_true')
    args = ap.parse_args()
    targets = sittings() if args.all else [(args.year, args.level)]
    for year, level in targets:
        P = JaPaper(year, level)
        asks = P.aural_asks() if args.aural else P.all_asks()
        print(f'=== {year} {level.upper()}: {len(asks)} asks '
              f'({page_count(P.path)} + '
              f'{page_count(P.aural_path) if P.aural_path else 0} pages)')
        for a in asks:
            print(f'  {a.section:>4} q={a.q} l={a.letter} r={a.roman} '
                  f'p{a.page + 1} {a.text[:80]}')


if __name__ == '__main__':
    main()
