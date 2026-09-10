#!/usr/bin/env python3
"""German question papers — the printed ask, in the language it was printed in.

    python3 scripts/markbank/authoring/de_paper.py 2024 hl
    python3 scripts/markbank/authoring/de_paper.py 2021 ol --aural

What this reader is, and what it borrows
----------------------------------------
The same bilingual layout French has, so the same machinery reads it: every
ask a candidate may answer in Irish or English is set TWICE, Irish in a left
column and English in a right one, on the same printed lines, and pymupdf
reads that as one interleaved stream. `fr_paper._rows` already cuts a page into
its columns on the page's own right-hand column bound, and this module calls
it rather than keeping a second copy — with one parameter added, because a
German ask is addressed "(b) (i)" and a Roman numeral is not one of the
markers a French column ever opens with.

Where German differs
--------------------
**The passage is not a decoy.** A French reading comprehension prints its
passage in NUMBERED PARAGRAPHS at the question margin, so every "1." on the
page is as likely to open the passage as the ask. A German passage is prose
with LINE NUMBERS in a narrow margin — bare "5", "10", "15", never "5." — and
its sections are headed with titles. The ask is still located by the scheme's
own reprinted wording (Law 4), because that is the only join that survives a
paper printing the same ask in two languages; but the candidate set is small
and the winning score is high.

**Three levels of address.** A German reading question runs to "2.(b)(ii)",
where French stops at "1.(a)". The marker may open all three at once — "2. (a)
(i)" — or inherit the two above it, and a marker in the left column inherits
from the left column only.

**The written sections print alternatives, not questions.** Angewandte
Grammatik sets "1." and "2." and a candidate answers one; Äußerung zum Thema
and Schriftliche Produktion set "(a)" and "(b)" the same way. Each is an ask
the paper prints, so each is a census leaf — exactly as a French Section B
alternative is.

**The listening booklet letters its OPTIONS.** A multiple-choice listening item
prints "(a)" to "(d)" under it, and those are the boxes, not four asks. The
asks in that booklet are "1." and "1. (i)", so a letter there is never a leaf —
counting them would have inflated the denominator by four for every such item.
"""
import argparse
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)

from fr_paper import _rows, _best_run, bag                    # noqa: E402

SUBJECT = 'german'


def papers_dir(subject=SUBJECT):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


# ------------------------------------------------------------- the units ----
# A section head OPENS its printed group and states what the section is worth.
# Both halves matter: the instructions page names every section in a sentence
# — "Freagair rogha (a) nó (b) sa roinn Schriftliche Produktion (Scríobh na
# Teanga) (50 marc)" — and a head matched anywhere in a line started the
# written-production section on page 2 and ran it to the end of the booklet.
UNIT_LV = re.compile(r'^TEXT\s+(I{1,3}|[123])\s*:?\s*LESEVERST[ÄA]NDNIS\s*:?\s*\(\d', re.I)
UNIT_AG = re.compile(r'^TEXT\s+(?:I{1,3}|[123])\s*:?\s*ANGEWANDTE\s+GRAMMATIK\s*:?\s*\(\d',
                     re.I)
UNIT_AT = re.compile(r'^TEXT\s+(?:I{1,3}|[123])\s*:?\s*'
                     r'[ÄA]U[ßSs]{1,2}ERUNG\s+ZUM\s+THEMA\s*:?\s*\(\d', re.I)
UNIT_SP = re.compile(r'^SCHRIFTLICHE\s+PRODUKTION\s*:?\s*\(\d', re.I)
TEXT_NUM = {'i': 1, 'ii': 2, 'iii': 3, '1': 1, '2': 2, '3': 3}

# A printed marker at the head of a column, in every depth the paper sets:
#   "2." · "2. (a)" · "2. (a) (i)" · "(b)" · "(b) (i)" · "(ii)"
NUM_MARK = re.compile(
    r'^(\d{1,2})\s*\.\s*(?:\(\s*([a-h])\s*\)\s*)?'
    r'(?:\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*)?(.*)$', re.S | re.I)
LETTER_MARK = re.compile(
    r'^\(\s*([a-h])\s*\)\s*(?:\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*)?(.*)$', re.S | re.I)
ROMAN_MARK = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|v)\s*\)\s*(.*)$', re.S | re.I)
MARKER_START = re.compile(
    r'^(?:\d{1,2}\s*\.|\(\s*(?:[a-h]|i{1,3}|iv|vi{0,3}|v)\s*\)|TEXT\s)', re.I)
# The English column's own marker, swept into the Irish group beside it. The
# two columns are set eighteen points apart at their widest and the words
# inside a line three to six, so where an Irish question runs long the gap
# between its last word and the English marker closes below the column bound
# and the two group together: 2024 Higher prints the row as "3. (a) Cén fáth a
# bhfuil cinneadh déanta ag 3. (a)". The trailing marker is the English
# column's, and put back where it belongs it opens the English ask; left where
# it fell, that ask was appended to the previous question's answer.
SWEPT_MARKER = re.compile(
    r'\s(\d{1,2}\.\s*(?:\(\s*[a-h]\s*\)\s*)?(?:\(\s*(?:i{1,3}|iv|vi{0,3}|v)\s*\)\s*)?'
    r'|\(\s*[a-h]\s*\)\s*(?:\(\s*(?:i{1,3}|iv|vi{0,3}|v)\s*\)\s*)?)$', re.I)

# Page furniture the SEC prints on every page of both booklets.
# Page furniture the SEC prints on every page of both booklets. Every pattern
# is anchored on the whole token it names: "Example" alone matched the middle
# of a printed question — "example you give. You may refer to a theme" — and
# took five words out of the 2022 Higher theme question.
FURNITURE = re.compile(
    r'^(?:Leaving Certificate|Scr[úu]d[úu] na hArdteistim|German\s*[–‒-]|'
    r'Gearm[áa]inis\s*[–‒-]|N[íi]l aon [áa]bhar|There is no examination|'
    r'Thall\s*/|Page \d+$|\d{1,3}$|Bileog|Freagair\b|Answer\s+(?:Question|Text|'
    r'either|question|Questions)|Treoracha\s*$|Instructions\s*$|N[ÓO]/OR\s*$|'
    r'ODER\s*$|OR\s*$|N[óo]ta\s*:|Note\s*:|Sampla\b|Example\s*:|Beispiel\s*:|'
    r'Lesen Sie\b|Bearbeiten Sie\b|Quellen\s*:|Nach\s*:)', re.I)

# The instruction line that names the language an ask must be answered in. The
# paper states it, in both of its own languages, above the questions it governs.
LANG_LINE = re.compile(
    r'Answer\s+(?:Question|Questions)\s+([\d,\s]+(?:and\s+\d)?)\s+in\s+(English|German)'
    r'|Beantworten\s+Sie\s+Frage\s+(\d)[^.]*auf\s+(Deutsch)', re.I)

# The listening booklet's four parts, named on the page in both languages.
# The source credit at the foot of a passage.
CREDIT = re.compile(r'^(?:Nach|Quellen?|Aus|Adaptiert)\s*:\s*(.*)$', re.I)

# Where an applied-grammar exercise's own items begin, inside the column the
# instruction does not run down: "(i) Spielzeugauto (Abschnitt 1)".
ITEM_RUN = re.compile(r'\(\s*(?:i|1)\s*\)\s*\S')

AURAL_PART = re.compile(r'^(?:(First|Second|Third|Fourth|Fifth)\s+Part'
                        r'|Cuid\s+a\s+(hAon|D[óo]|Tr[íi]|Ceathair|C[úu]ig))\b', re.I)
AURAL_END = re.compile(r'^(?:CR[ÍI]OCH|END)\s*$|^(?:F[óo]gra c[óo]ipchirt|'
                       r'Copyright notice|Acknowledge)', re.I)
PART_NAMES = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
              'haon': 1, 'dó': 2, 'do': 2, 'trí': 3, 'tri': 3, 'ceathair': 4,
              'cúig': 5, 'cuig': 5}


LEADING_MARKER = re.compile(
    r'^(\d{1,2}\.\s*(?:\(\s*[a-h]\s*\)\s*)?(?:\(\s*(?:i{1,3}|iv|vi{0,3}|v)\s*\)\s*)?'
    r'|\(\s*[a-h]\s*\)\s*(?:\(\s*(?:i{1,3}|iv|vi{0,3}|v)\s*\)\s*)?)', re.I)


def _unsweep(groups):
    """Put a swept English marker back at the head of its own column.

    Two shapes, both from the same cause — the gap between the Irish column's
    last word and the English column's first closing below the width that
    separates two columns:

      * the marker alone at the end of the Irish group, with its own English
        text already cut off into a group of its own ("… déanta ag 3. (a)" /
        "Why have some young people decided");
      * the marker AND the English words behind it, all inside the Irish
        group, which is recognised because the row then prints the SAME
        address twice ("3. (a) Tá tuairimí agus mothúcháin dhifriúla 3. (a)
        Lena, the narrator"). Nothing else in this paper repeats an address
        inside one printed line.
    """
    rows = list(groups)
    out = []
    carry = None
    for i, (x, side, text) in enumerate(rows):
        if carry:
            text = f'{carry} {text}'.strip()
            side = 'R'
            carry = None
        if side == 'L':
            m0 = LEADING_MARKER.match(text)
            if m0:
                mk = m0.group(1).strip()
                at = text.find(f' {mk} ', len(mk))
                if at > 0:
                    out.append((x, 'L', text[:at].rstrip()))
                    out.append((x + 1, 'R', text[at:].strip()))
                    continue
            nxt = rows[i + 1] if i + 1 < len(rows) else None
            if nxt and nxt[1] == 'R' and not MARKER_START.match(nxt[2]):
                m = SWEPT_MARKER.search(text)
                if m:
                    out.append((x, 'L', text[:m.start()].rstrip()))
                    carry = m.group(1).strip()
                    continue
        out.append((x, side, text))
    return out


class Block:
    """One printed marker and the lines beneath it, in one column."""

    __slots__ = ('page', 'side', 'unit', 'q', 'letter', 'roman', 'lines')

    def __init__(self, page, side, unit, q, letter, roman):
        self.page, self.side, self.unit = page, side, unit
        self.q, self.letter, self.roman = q, letter, roman
        self.lines = []

    @property
    def key(self):
        return (self.unit, self.q, self.letter, self.roman)

    @property
    def text(self):
        return ' '.join(' '.join(self.lines).split())

    @property
    def printed(self):
        """The block with the paper's own line breaks kept — a multiple-choice
        ask prints one option per line, and joining them makes a run-on."""
        return '\n'.join(' '.join(l.split()) for l in self.lines if l.strip())

    def __repr__(self):
        return (f'<Block p{self.page + 1} {self.side} {self.unit} {self.q}'
                f'{self.letter or ""}{self.roman or ""} {self.text[:40]!r}>')


class DePaper:
    """One sitting's written booklet, plus the listening booklet beside it."""

    def __init__(self, year, level, subject=SUBJECT):
        self.year, self.level, self.subject = year, level, subject
        self.path = self._written_path()
        self.aural_path = self._aural_path()
        self.blocks = []
        self.unit_pages = {}       # unit -> [1-based pages it is printed on]
        self.alternatives = []     # (unit, letter, text, page) for AT and SP
        self.grammar = []          # (q, text, page) for the two AG alternatives
        self.language_lines = []   # what the paper says about answer language
        self._read()

    # -- files --------------------------------------------------------------
    def _written_path(self):
        p = os.path.join(papers_dir(self.subject),
                         f'{self.year}-{self.level}-000-paper.pdf')
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        return p

    def _aural_path(self):
        p = os.path.join(papers_dir(self.subject),
                         f'{self.year}-{self.level}-A00-paper.pdf')
        return p if os.path.exists(p) else None

    # -- the walk -----------------------------------------------------------
    def _read(self):
        unit = None
        cur = {}                 # side -> the block still taking lines
        current = None           # the (question, letter) the page is under
        first_page, last_page = {}, {}
        for pno, groups in _rows(self.path, marker=MARKER_START):
            groups = _unsweep(groups)
            new_unit = None
            for _x, _s, t in groups:
                new_unit = self._unit_of(t.strip()) or new_unit
            if new_unit:
                unit, cur, current = new_unit, {}, None
            if unit is None:
                continue
            first_page.setdefault(unit, pno)
            last_page[unit] = pno
            for _x0, side, text in groups:
                if LANG_LINE.search(text):
                    self.language_lines.append((unit, ' '.join(text.split())))
                if FURNITURE.match(text):
                    continue
                if unit in ('AT', 'SP'):
                    self._alternative(unit, side, text, pno)
                    continue
                if unit == 'AG':
                    self._grammar(side, text, pno)
                    continue
                q = letter = roman = rest = None
                m = NUM_MARK.match(text)
                if m:
                    q, letter, roman, rest = (int(m.group(1)), m.group(2),
                                              (m.group(3) or '').lower() or None,
                                              m.group(4))
                    current = (q, letter)
                else:
                    # A lettered or Roman marker inherits the numbers above it,
                    # and the address it inherits belongs to the ROW, not to one
                    # column. The question number is printed once per row and
                    # the two columns can close up around it — 2024 Higher sets
                    # "3. (a) Céard a dhéanann Geiger chun teacht 3.", the
                    # English column's own "3." swept into the Irish group
                    # beside it. Keeping a per-column memory instead filed every
                    # English rendering of question 3 under question 2, which is
                    # the rendering the scheme marks.
                    m = LETTER_MARK.match(text)
                    if m and current:
                        q = current[0]
                        letter = m.group(1)
                        roman = (m.group(2) or '').lower() or None
                        rest = m.group(3)
                        current = (q, letter)
                    else:
                        m = ROMAN_MARK.match(text)
                        if m and current:
                            q, letter = current
                            roman = m.group(1).lower()
                            rest = m.group(2)
                if q is None:
                    if cur.get(side) is not None:
                        cur[side].lines.append(text)
                    continue
                block = Block(pno, side, unit, q, letter, roman)
                if rest.strip():
                    block.lines.append(rest.strip())
                self.blocks.append(block)
                cur[side] = block
        for unit, first in first_page.items():
            self.unit_pages[unit] = list(
                range(first + 1, last_page.get(unit, first) + 2))

    @staticmethod
    def _unit_of(line):
        m = UNIT_LV.match(line)
        if m:
            return f'T{TEXT_NUM[m.group(1).lower()]}'
        if UNIT_AG.match(line):
            return 'AG'
        if UNIT_AT.match(line):
            return 'AT'
        if UNIT_SP.match(line):
            return 'SP'
        return None

    def _alternative(self, unit, side, text, pno):
        m = LETTER_MARK.match(text)
        if m and m.group(1) in 'ab' and not m.group(2):
            self.alternatives.append([unit, m.group(1), [m.group(3).strip()],
                                      pno + 1, side])
            return
        for row in reversed(self.alternatives):
            if row[0] == unit and row[4] == side:
                row[2].append(text)
                return

    def _grammar(self, side, text, pno):
        m = NUM_MARK.match(text)
        if m and m.group(1) in '12' and not m.group(2):
            self.grammar.append([int(m.group(1)), [m.group(4).strip()],
                                 pno + 1, side])
            return
        for row in reversed(self.grammar):
            if row[3] == side:
                row[1].append(text)
                return

    def credit(self, unit):
        """The source credit the paper prints at the foot of a passage.

        "Nach: Arno Geiger: Das glückliche Geheimnis" on a literary extract,
        "Quellen: taz.de / sueddeutsche.de / welt.de" on a journalistic one.
        It is the paper's own statement of what kind of text it set, and it is
        what de_topics files the card against.
        """
        pages = self.unit_pages.get(unit)
        if not pages:
            return None
        with pymupdf.open(self.path) as doc:
            for pno in pages:
                lines = doc[pno - 1].get_text().split('\n')
                for i, line in enumerate(lines):
                    m = CREDIT.match(' '.join(line.split()))
                    if not m:
                        continue
                    tail = m.group(1).strip()
                    if not tail and i + 1 < len(lines):
                        # 2022 and 2024 Higher break the credit after the
                        # colon, so the words that say what the text is sit on
                        # the line below the word that introduces them.
                        tail = ' '.join(lines[i + 1].split())
                    if tail:
                        return tail
        return None

    # -- matching -----------------------------------------------------------
    def candidates(self, unit, q, letter, roman):
        return [b for b in self.blocks if b.key == (unit, q, letter, roman)]

    def find(self, unit, q, letter, roman, cue, floor=0.34, whole=False):
        """The printed ask this scheme cue is marking: (text, page, score).

        The cue decides, never the marker, for the reason align.py exists: the
        ask is printed twice, once in Irish and once in English, and the one the
        scheme marks is the one whose wording it reprints.
        """
        want = bag(cue)
        best = (0.0, None)
        for block in self.candidates(unit, q, letter, roman):
            text, sc = _best_run(block.lines, want)
            if sc > best[0]:
                best = (sc, (block.printed if whole else text, block.page + 1, sc))
        if best[1] is None or best[0] < floor:
            return None
        return best[1]

    def by_key(self, unit, q, letter, roman, whole=True):
        """The printed ask at this address, where the scheme reprints NO wording.

        Law 4 does not require align.py; it requires a join on something BOTH
        documents print. The Ordinary paragraph-headings, matching and
        true/false questions are the one shape here whose scheme prints only
        the answer key — "2 d 3 a 4 c 5 f 6 b" — so there is no wording to
        score. The address is then the only thing both print, and it addresses
        one printed block per column: the English rendering is taken, and the
        pairing is recorded as an ADDRESS pairing rather than a wording one so
        the ledger can say which cards rest on it.
        """
        blocks = self.candidates(unit, q, letter, roman)
        if not blocks:
            return None
        best = max(blocks, key=lambda b: (b.side == 'R', len(b.text)))
        return ((best.printed if whole else best.text), best.page + 1, None)

    def written_alternatives(self, unit):
        """[(letter, text, page)] for Äußerung zum Thema or Schriftliche
        Produktion — the two tasks the paper prints and a candidate chooses
        between. The longer rendering of the two columns is kept, which is the
        German one where the paper sets the task in German."""
        best = {}
        for u, letter, lines, page, side in self.alternatives:
            if u != unit:
                continue
            text = ' '.join(' '.join(lines).split())
            # The English rendering where the paper prints one — the right-hand
            # column — and the longest otherwise, which is the German the task
            # is set in where the paper sets it in German alone.
            rank = (side == 'R', len(text))
            if letter not in best or rank > best[letter][2]:
                best[letter] = (text, page, rank)
        return [(k, best[k][0], best[k][1]) for k in sorted(best)]

    def grammar_alternatives(self):
        """[(q, text, page)] for the two applied-grammar alternatives.

        The instruction and the items it governs are set in DIFFERENT columns
        at Ordinary: the English instruction runs down the right-hand column
        and the five compounds or sentences the candidate works on down the
        left, beside the Irish. So the question is the English instruction
        followed by the items themselves — without them the card asks a
        student to name the parts of a compound word it never shows. At Higher
        the whole exercise is set in German across the measure and there is no
        second column to join.
        """
        by_side = {}
        pages = {}
        for q, lines, page, side in self.grammar:
            text = ' '.join(' '.join(lines).split())
            if len(text) > len(by_side.get((q, side), '')):
                by_side[(q, side)] = text
            pages.setdefault(q, page)
        out = []
        for q in sorted({k[0] for k in by_side}):
            english = by_side.get((q, 'R'), '')
            irish = by_side.get((q, 'L'), '')
            if english:
                m = ITEM_RUN.search(irish)
                text = f'{english} {irish[m.start():]}'.strip() if m else english
            else:
                text = irish
            out.append((q, ' '.join(text.split()), pages[q]))
        return out

    # -- the listening booklet ----------------------------------------------
    def aural_asks(self):
        """[(part, item, roman, text)] for the Listening Comprehension Test.

        Read for the census only: an ask here is answerable from the recording
        alone, and de_all.py excludes every one of them with that evidence.
        """
        if not self.aural_path:
            return []
        out = []
        part = None
        cur = {}
        state = {}
        for _pno, groups in _rows(self.aural_path, marker=MARKER_START):
            for _x0, side, text in groups:
                m = AURAL_PART.match(text)
                if m:
                    token = (m.group(1) or m.group(2) or '').lower()
                    part = PART_NAMES.get(token)
                    cur, state = {}, {}
                    continue
                if AURAL_END.match(text):
                    part = None
                    continue
                if part is None or FURNITURE.match(text):
                    continue
                item = roman = rest = None
                m = NUM_MARK.match(text)
                if m:
                    item = int(m.group(1))
                    roman = (m.group(3) or '').lower() or None
                    rest = m.group(4)
                    state[side] = item
                else:
                    m = ROMAN_MARK.match(text)
                    if m and state.get(side):
                        item, roman, rest = state[side], m.group(1).lower(), m.group(2)
                if item is None:
                    if cur.get(side) is not None:
                        cur[side][3].append(text)
                    continue
                row = [part, item, roman, [rest.strip()] if rest.strip() else []]
                out.append(row)
                cur[side] = row
        seen = {}
        for part, item, roman, lines in out:
            key = (part, item, roman)
            text = ' '.join(' '.join(lines).split())
            # The same ask is printed in Irish and in English. Keep the longer
            # rendering so the census row carries something a person can read;
            # the count is what it is for, and the count is one.
            if key not in seen or len(text) > len(seen[key]):
                seen[key] = text
        # A head whose roman parts are the asks is not itself an ask.
        romanned = {(p, i) for p, i, r in seen if r}
        return [(p, i, r, seen[(p, i, r)])
                for p, i, r in sorted(seen, key=lambda k: (k[0], k[1], k[2] or ''))
                if r or (p, i) not in romanned]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level')
    ap.add_argument('--subject', default=SUBJECT)
    ap.add_argument('--aural', action='store_true')
    args = ap.parse_args()
    P = DePaper(args.year, args.level, args.subject)
    if args.aural:
        asks = P.aural_asks()
        print(f'{args.year} {args.level.upper()} aural: {len(asks)} asks')
        for part, item, roman, text in asks:
            print(f'  Part {part} Q{item}{f"({roman})" if roman else ""}  {text[:80]}')
        return 0
    print(f'{args.year} {args.level.upper()}: {len(P.blocks)} printed blocks')
    for unit, pages in sorted(P.unit_pages.items()):
        print(f'  {unit}: pages {pages}')
    for unit in ('AT', 'SP'):
        for letter, text, page in P.written_alternatives(unit):
            print(f'  {unit} ({letter}) p{page}: {text[:90]}')
    for q, text, page in P.grammar_alternatives():
        print(f'  AG {q} p{page}: {text[:90]}')
    for unit, line in P.language_lines:
        print(f'  LANG {unit}: {line[:90]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
