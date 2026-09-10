#!/usr/bin/env python3
"""Non-curricular EU language papers — the printed ask, and which is a leaf.

    python3 scripts/markbank/authoring/eu_paper.py portuguese 2024 hl
    python3 scripts/markbank/authoring/eu_paper.py portuguese 2022 ol --aural
    python3 scripts/markbank/authoring/eu_paper.py portuguese --audit

ONE reader, three subjects
--------------------------
Portuguese (SEC 018), Romanian (SEC 553) and Dutch (SEC 017) are the same
examination printed in three languages, and Polish's reader (pl_paper.py)
already showed what that examination looks like: a booklet printed in ONE
language edition rather than the bilingual 'B' booklet the curricular languages
use, a reading comprehension whose questions are LETTERED so no marker is ever
ambiguous with a numbered passage paragraph, and — in Portuguese only — a
Listening Comprehension Test in a booklet of its own.

Rather than a fourth, fifth and sixth copy of that walker, the marker
vocabulary is a table (`LANGS`) and the walk is shared. What differs between
the three is words, not structure: "Questão"/"PARTEA"/the Dutch paper's bare
"1.", "Parte A"/"PARTEA I", "Adaptado:"/"Publicat în".

TWO ERAS, and the corpus says which
-----------------------------------
* CLASSIC. One booklet, sat at ONE level, numbered questions on one or two
  printed texts, and — the fact that makes it cardable — **the tariff is
  printed on the QUESTION PAPER**, in its right-hand margin: "(5)", "(5×1)",
  "(5 puncte)", "(1 punt)". The scheme for these sittings prints answers and no
  marks at all, so the paper is the only place the price is written down.
  Portuguese 2021, and every Romanian and Dutch sitting in the corpus.
* MODERN. Two booklets and two levels, rebuilt in 2022: Part A Reading and
  Part B Written Production in the written booklet (component 000), and a
  Listening Comprehension Test in its own (component A00). Here the PAPER
  prints no per-ask marks and the SCHEME prices every ask. Portuguese 2022
  onward, and nothing else in this family.

The era is read from the booklets on disk, never assumed: a sitting with a
`-000-` component is modern, a lone `<year>-<level>-paper.pdf` is classic.
"""
import argparse
import glob
import os
import re
import sys
import unicodedata

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))
from markbank_text import unligature                            # noqa: E402


# --------------------------------------------------------- the vocabulary ---
# Everything that differs between the three subjects, and nothing that does
# not. A regex here is matched against a whole printed LINE, already normalised
# (see _norm) so U+00A0 and the SEC's private-use spaces are ordinary spaces.
LANGS = {
    'portuguese': {
        'name': 'Portuguese',
        # "Questão 1:", "Questão 1 – Leia este texto…", "Questão 3".
        'q_head': r'^Quest[ãa]o\s*(\d{1,2})\b',
        # The section tab the SEC sets in the margin of the page each section
        # opens on: "Parte A   Compreensão Escrita", "Parte B   Escrita".
        # "[AB]" and not "\w", because the same word heads the reading text's
        # own subsections — "Parte 1 – Como começou" — and a looser class read
        # those as section boundaries.
        'section_tab': r'^Parte\s+([AB])\b',
        'aural_tab': r'^Parte\s+([A-E])\b',
        # The classic examination's two halves, printed as words.
        'classic_part': r'^(Primeira|Segunda)\s+Parte\b',
        'classic_part_map': {'primeira': 'I', 'segunda': 'II'},
        # The second part's essay options, which the SEC titles rather than
        # numbers: "Tópico 1", "Tópico 2". The scheme numbers them "Tema 1"
        # and "Tema 2", so the paper's own title carries the number.
        'essay_title': r'^T[óo]pico\s+(\d)\b',
        'furniture': (r'^(?:Leaving\s+Certificate|Coimisi[úu]n|'
                      r'State\s+Examinations|Portuguese\s*[–—-]|'
                      r'Page\s*\d+)\b|^\d{1,3}$'),
        # The attribution the SEC prints under a reading text.
        'source_line': (r'^(?:Adaptado|Adapta[çc][ãa]o|Texto\s+adaptado|'
                        r'Fonte\s*:|In\s*:|Retirado)'),
        # Rubric printed between asks, which belongs to no ask.
        'rubric': (r'^(?:Responda\b|Answer\b|Based\s+on\b|Baseado\b|'
                   r'Leia\s+(?:o|este|atentamente)\b|Escreva\b|'
                   r'Todas\s+as\s+respostas\b|Observe\s+as\s+imagens\b)'),
    },
}


def cfg(subject, key, default=None):
    return LANGS[subject].get(key, default)


def papers_dir(subject):
    return os.path.join(ROOT, 'examiner-reports', subject, 'papers')


def paper_path(year, level, component, subject):
    """The booklet on disk, whatever the fetcher called it.

    A classic sitting is a single booklet and lands as `2021-hl-paper.pdf` with
    no component token; a modern one prints two and lands as `…-000-paper.pdf`
    and `…-A00-paper.pdf`. Requiring the component silently found nothing for
    the classic sittings, which is every Romanian and Dutch paper in the
    corpus.
    """
    stem = f'{year}-{level}'
    names = ([f'{stem}-{component}-paper.pdf'] if component
             else [f'{stem}-paper.pdf', f'{stem}-000-paper.pdf'])
    for name in names:
        path = os.path.join(papers_dir(subject), name)
        if os.path.exists(path):
            return path
    return None


# --------------------------------------------------------------- the page ---
# The SEC sets these booklets with U+00A0 between every word in some years and
# with ordinary spaces in others. Folded here so one set of patterns reads
# every sitting.
NBSP = '\u00a0\u2000\u2001\u2002\u2003\u2007\u2009\u200a\u202f\u2060\ufeff'
# The Symbol and Wingdings space, which those fonts encode in the private-use
# area. It is a space and nothing else, and left as itself it reaches a card as
# an unresolvable glyph the build refuses.
SYMBOL_SPACE = '\uf020\uf0a0'


def _norm(text):
    """One printed line, with the SEC's broken font glyphs put back.

    `unligature` is the bank's shared map rather than a local one: these papers
    set "ginásƟca" and "İsico" with a subset font whose ti and fi ligatures
    have no ToUnicode entry, and a card carrying either quotes a word the SEC
    never printed.
    """
    out = ''.join(' ' if c in NBSP or c in SYMBOL_SPACE else c
                  for c in unligature(text))
    return re.sub(r'\s+', ' ', out).strip()


class Line:
    __slots__ = ('page', 'x', 'y', 'x1', 'text')

    def __init__(self, page, x, y, x1, text):
        self.page, self.x, self.y, self.x1, self.text = page, x, y, x1, text

    def __repr__(self):
        return (f'Line(p{self.page} x={self.x:.1f} y={self.y:.1f} '
                f'{self.text[:60]!r})')


# A marker printed alone in its cell, in every form these booklets use: the
# bracketed letter or roman "(b)", the classic paper's bare "b)", the numbered
# "1." and — the Listening booklet's own — the bracketed number "(1)". Without
# the last, an item whose question wrapped onto a second line kept the wrap and
# lost the marker's own line, and censused as an empty leaf.
MARKER_ONLY = re.compile(r'^\(\s*([a-z]{1,4})\s*\)\.?$|^([a-z])\s*\)$|'
                         r'^(\d{1,2})\s*[.)]$|^\(\s*(\d{1,2})\s*\)$', re.I)
# How far above or below its own baseline the text beside a marker may sit.
# A marker is set CENTRED in its table cell while the sentence beside it wraps
# around it, so the whole cell is gathered rather than one baseline.
CELL_TOL = 20.0
# How far right of the letter column a marker may still be a LETTER. Measured
# rather than guessed: the SEC's own table cells drift several points inside
# one page.
LETTER_TOL = 8.0
# How far below a kept line the next one may sit and still be the same ask.
# Below the ask comes the answer space, which is blank.
LINE_GAP = 32.0


def read_lines(path):
    """Every printed line, in reading order, with the marker column intact.

    A part marker is set in its own table cell — "(b)" at x=56.7 and its
    question at x=85.1 on the same baseline — so the two are joined back
    together here. Left apart, every lettered ask in the corpus reads as an
    empty leaf.
    """
    out = []
    with pymupdf.open(path) as doc:
        for pno, page in enumerate(doc, 1):
            raw = []
            for block in page.get_text('dict')['blocks']:
                if block.get('type') != 0:
                    continue
                for line in block['lines']:
                    text = _norm(''.join(s['text'] for s in line['spans']))
                    if not text:
                        continue
                    x0, y0, x1, y1 = line['bbox']
                    raw.append(Line(pno, x0, (y0 + y1) / 2, x1, text))
            raw.sort(key=lambda l: (round(l.y, 0), l.x))
            out += _join_markers(raw)
    return out


def _join_markers(lines):
    """Glue a marker printed alone in its cell onto the text beside it."""
    out, used = [], set()
    for i, line in enumerate(lines):
        if i in used:
            continue
        if MARKER_ONLY.match(line.text):
            mates = [j for j in range(max(0, i - 4), min(i + 5, len(lines)))
                     if j != i and j not in used and lines[j].x > line.x + 4
                     and abs(lines[j].y - line.y) <= CELL_TOL
                     and not MARKER_ONLY.match(lines[j].text)]
            if mates:
                # Only the marker's OWN column. A table sets the marker in a
                # narrow cell and the question beside it wraps over three
                # lines, but the page also carries a wider rubric at a
                # different margin within the same band, and a purely vertical
                # window pulled that in instead of the question.
                near = min(mates, key=lambda j: abs(lines[j].y - line.y))
                column = lines[near].x
                mates = [j for j in mates if abs(lines[j].x - column) <= 8]
                mates.sort(key=lambda j: (lines[j].y, lines[j].x))
                used.update(mates)
                body = ' '.join(lines[j].text for j in mates)
                out.append(Line(line.page, line.x,
                                min([line.y] + [lines[j].y for j in mates]),
                                max(lines[j].x1 for j in mates),
                                f'{line.text} {body}'))
                continue
        out.append(line)
    return out


# ------------------------------------------------------------- the markers ---
# A lettered part, in either of the two ways this family prints one: "(a)" in
# the modern booklets and a bare "a)" in the classic ones.
LETTER = re.compile(r'^\(?\s*([a-l])\s*\)\s*(.*)$', re.I)
ROMAN = re.compile(r'^\(\s*(i{1,3}|iv|vi{0,3}|ix|x)\s*\)\s*(.*)$', re.I)
NUMBERED = re.compile(r'^\(?(\d{1,2})\s*[.)]\s*(.*)$')
# The first roman marker printed INSIDE an item's own line, after its stem.
INNER_FIRST_ROMAN = re.compile(r'\(\s*i\s*\)\s*')
LETTERS = 'abcdefghijkl'
# The price the CLASSIC paper prints in its right-hand margin, and the only
# place that sitting's tariff is written down: "(5)", "(5×1)", "(5 puncte)",
# "(1 punt)", "(10 puncte)". Read from the paper because the classic schemes
# print answers with no marks beside them at all.
PAPER_TARIFF = re.compile(
    r'\(\s*(?:(\d{1,2})\s*[x×]\s*)?(\d{1,2})\s*'
    r'(?:puncte|puncts?|punte|punt|punten|pontos?|marks?|m)?\s*\)', re.I)
# The same, with the multiplier written second: "(5×1)" is five answers at one
# point each and the SEC also sets "(1×5)". Both are read, and which is the
# count is settled by the group beneath it, never by picking the larger.
TRAILING_MARK = re.compile(
    r'\s*\(\s*\d{1,2}\s*(?:[x×]\s*\d{1,2}\s*)?'
    r'(?:puncte|puncts?|punte|punt|punten|pontos?|marks?)?\s*\)\s*$', re.I)


def next_letter(current):
    """The SEC's own numbering, used as a second way in.

    A marker that is the NEXT letter after the one before it IS that letter,
    wherever the cell puts it. "(i)" is excluded from this path on purpose: it
    is the one marker that can also be a roman, so it still has to satisfy BOTH
    the column and the sequence.
    """
    return 'a' if not current else chr(ord(current) + 1)


class Ask:
    __slots__ = ('section', 'q', 'letter', 'roman', 'text', 'page', 'stem',
                 'tariff', 'notation')

    def __init__(self, section, q, letter, roman, text, page):
        self.section, self.q = section, q
        self.letter, self.roman = letter, roman
        self.text, self.page = text, page
        self.stem = ''
        # (count, per, total) where the CLASSIC paper printed a price beside
        # this ask, and None where it did not. Never inferred.
        self.tariff = None
        self.notation = ''

    @property
    def key(self):
        """The address the PAPER prints: its section tab, then its number."""
        return (self.section, self.q, self.letter, self.roman)

    @property
    def full_text(self):
        """The ask as a reader meets it: its parent's stem, then its own."""
        if self.stem and len(self.text) < 60:
            return _norm(f'{self.stem} {self.text}')
        return self.text

    def __repr__(self):
        return f'Ask({self.key} {self.text[:60]!r})'


class EuPaper:
    """One sitting's booklets, walked into the leaf asks they print."""

    def __init__(self, year, level, subject):
        self.year, self.level, self.subject = year, level, subject
        self.path = paper_path(year, level, None, subject)
        if self.path is None:
            raise FileNotFoundError(
                f'no {subject} written paper for {year} {level}')
        self.aural_path = paper_path(year, level, 'A00', subject)
        # The era, read from the booklets on disk rather than from a year.
        self.era = ('modern' if self.path.endswith('-000-paper.pdf')
                    else 'classic')
        self.lines = read_lines(self.path)
        self.flags = []
        self.text_pages = {}          # question number -> [pages of its text]
        self.leads = {}               # question number -> its printed title
        self.letter_x = self._letter_column()
        self.left_margin = self._left_margin()
        self._asks = (self._walk() if self.era == 'modern'
                      else self._walk_classic())
        self._aural = self._walk_aural() if self.aural_path else []

    # ------------------------------------------------------------ layout ---
    def _letter_column(self):
        """Where a part LETTER is printed, measured from the unambiguous ones.

        a-h and j-l are letters and nothing else; only "(i)" can be read two
        ways. So the column is measured from the markers that cannot lie, and
        "(i)" is then tested against it. The MODE, never the minimum: one
        outlier four points left of the column its thirty siblings sit in put
        every real letter outside the tolerance when the minimum was used.
        """
        head = re.compile(cfg(self.subject, 'q_head'))
        by_q, q = {}, None
        for line in self.lines:
            m = head.match(line.text)
            if m:
                q = int(m.group(1))
                continue
            if re.match(r'^\(?\s*[a-hj-l]\s*\)\s', line.text):
                by_q.setdefault(q, []).append(round(line.x))
        self.letter_x_by_q = {k: max(set(v), key=v.count)
                              for k, v in by_q.items()}
        every = [x for v in by_q.values() for x in v]
        return max(set(every), key=every.count) if every else 56.7

    def _left_margin(self):
        """The page's own left margin — the x most printed lines start at."""
        xs = [round(l.x) for l in self.lines]
        return max(set(xs), key=xs.count) if xs else 56.7

    def _column_for(self, q):
        return self.letter_x_by_q.get(q, self.letter_x)

    def _is_letter(self, x, prev_letter, q=None):
        """Is this "(i)" the ninth letter or the first roman?

        Both conditions, never one. Indent alone reads an indented roman as a
        letter; sequence alone reads "(h)(i)" as the letter after (h).
        """
        return x <= self._column_for(q) + LETTER_TOL and prev_letter == 'h'

    # ------------------------------------------------------------- walking --
    def _walk(self):
        """The MODERN booklet: Part A Reading and Part B Written Production."""
        q_head = re.compile(cfg(self.subject, 'q_head'))
        section_tab = re.compile(cfg(self.subject, 'section_tab'))
        furniture = re.compile(cfg(self.subject, 'furniture'), re.I)
        source_line = re.compile(cfg(self.subject, 'source_line'), re.I)
        rubric = re.compile(cfg(self.subject, 'rubric'), re.I)

        asks, q = [], None
        letter = roman = None
        current, last_y = None, None
        text_pages, leads = {}, {}

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        # The section tab is printed in the MARGIN of the page its section
        # opens on, and pymupdf reports it after the questions beside it. Read
        # in stream order it arrives too late to file a single ask. It is a
        # property of the PAGE, so it is resolved per page before the walk —
        # and the pages BEFORE the first tab are Part A, because the tab marks
        # where a section starts and Part A is the first one.
        by_page = self._section_by_page(self.lines, section_tab, first='A')
        section = 'A'

        for line in self.lines:
            if furniture.match(line.text) and len(line.text) < 60:
                continue
            section = by_page.get(line.page, section)
            if section_tab.match(line.text):
                continue
            head = q_head.match(line.text)
            if head and not _is_choice_rubric(line.text):
                close()
                q = int(head.group(1))
                letter = roman = None
                last_y = None
                leads[q] = line.text
                continue
            if q is None:
                continue
            lm = LETTER.match(line.text)
            rm = ROMAN.match(line.text)
            marker = None
            if rm and not (rm.group(1).lower() == 'i'
                           and self._is_letter(line.x, letter, q)):
                marker = ('roman', rm.group(1).lower(), rm.group(2))
            elif lm and (not rm or self._is_letter(line.x, letter, q)):
                # A letter marker stands at the question's own left margin. A
                # word that merely begins with a bracketed letter does not.
                if line.x <= self._column_for(q) + LETTER_TOL \
                        or lm.group(1).lower() == next_letter(letter):
                    marker = ('letter', lm.group(1).lower(), lm.group(2))
            if marker:
                kind, mark, rest = marker
                close()
                if kind == 'letter':
                    letter, roman = mark, None
                    # "(e) (i) Qual é o seu público-alvo?" — the SEC glues a
                    # letter and its first roman onto one printed line, and
                    # reading only the letter loses the roman entirely.
                    inner = ROMAN.match(rest)
                    if inner:
                        roman, rest = inner.group(1).lower(), inner.group(2)
                else:
                    roman = mark
                current = Ask(section, q, letter, roman, rest, line.page)
                last_y = line.y
                continue
            if current is not None and line.page == current.page \
                    and last_y is not None and 0 <= line.y - last_y <= LINE_GAP \
                    and not rubric.match(line.text):
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
            # In the WRITTEN PRODUCTION section a question's rubric is its
            # options' only printed words: 2023 Higher heads Question 5
            # "Observe as imagens com atenção e escolha uma: (a) ou (b) ou
            # (c)." and then prints three PICTURES, so (a), (b) and (c) have
            # no text of their own at all. Kept on the question, the option is
            # an ask a reader can see; dropped, it censuses as an empty leaf.
            if section == 'B' and letter is None and q is not None \
                    and len(leads.get(q, '')) < 400:
                leads[q] = _norm(f'{leads.get(q, "")} {line.text}')
            # Everything printed before the first ask of a question is its
            # reading text, and the card carries those pages beside the ask.
            if letter is None and not source_line.match(line.text):
                text_pages.setdefault(q, [])
                if line.page not in text_pages[q]:
                    text_pages[q].append(line.page)
        close()
        self.text_pages, self.leads = text_pages, leads
        asks = _dedupe(asks)
        self._check_sections(asks)
        return asks

    def _walk_classic(self):
        """The CLASSIC booklet: two or three numbered PARTS on printed texts.

        The passage comes first and the questions after it, both at the same
        left margin. What separates them is not wording: it is the SEC's own
        NUMBERING. A question opens with the number after the one before it —
        1, then 2, then 3 — printed with a full stop at the part's left margin,
        and no line of a passage does that. Reading the boundary off an
        attribution line instead found nothing at all in 2021, whose text is
        signed "Sophia de Mello Breyner Andresen, in Contos Exemplares".

        The tariff is printed HERE, in the right-hand margin — "(5)", "(5×1)",
        "(5 puncte)" — and nowhere else in the sitting's two documents, because
        the classic schemes print answers with no marks beside them at all.
        """
        part_pat = re.compile(cfg(self.subject, 'classic_part'), re.I)
        part_map = cfg(self.subject, 'classic_part_map')
        essay_pat = cfg(self.subject, 'essay_title')
        essay_pat = re.compile(essay_pat, re.I) if essay_pat else None
        furniture = re.compile(cfg(self.subject, 'furniture'), re.I)

        asks, part, q, letter = [], None, None, None
        current, last_y = None, None
        text_pages = {}

        def close():
            nonlocal current
            if current is not None:
                _read_paper_tariff(current)
                current.text = _norm(TRAILING_MARK.sub('', current.text))
                asks.append(current)
                current = None

        for line in self.lines:
            if furniture.match(line.text) and len(line.text) < 60:
                continue
            pm = part_pat.match(line.text)
            if pm:
                close()
                token = pm.group(1).lower()
                part = part_map.get(token, token.upper())
                q, letter = None, None
                continue
            if part is None:
                continue
            nm = NUMBERED.match(line.text)
            lm = LETTER.match(line.text)
            # The number after the one before it, at the left margin, IS the
            # next question. Both conditions: a passage sentence can open with
            # a year and a full stop, and a wrapped line can start at the
            # margin, but neither is ever the next number in the run.
            if nm and int(nm.group(1)) == (q or 0) + 1 \
                    and line.x <= self.left_margin + LETTER_TOL:
                close()
                q, letter = int(nm.group(1)), None
                current = Ask(part, q, None, None, nm.group(2), line.page)
                last_y = line.y
                continue
            # The essay options of the second part, which the SEC titles
            # rather than numbers: "Tópico 1", "Tópico 2".
            if essay_pat is not None and essay_pat.match(line.text):
                close()
                q = int(essay_pat.match(line.text).group(1))
                letter = None
                current = Ask(part, q, None, None, line.text, line.page)
                last_y = line.y
                continue
            if lm and q is not None \
                    and (lm.group(1).lower() == next_letter(letter)
                         or line.x <= self.letter_x + LETTER_TOL):
                close()
                letter = lm.group(1).lower()
                current = Ask(part, q, letter, None, lm.group(2), line.page)
                last_y = line.y
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
            if q is None:
                text_pages.setdefault(part, [])
                if line.page not in text_pages[part]:
                    text_pages[part].append(line.page)
        close()
        # The classic examination sets its text or texts before the questions
        # and asks every question of the part about them, so the pages are
        # collected under the PART and handed to each of its questions.
        self.text_pages = {}
        for a in asks:
            self.text_pages.setdefault(a.q, text_pages.get(a.section) or [])
        self.leads = {}
        _walk_down_paper_splits(asks)
        return asks

    @staticmethod
    def _section_by_page(lines, pattern, first=None):
        """{page: section}, the tab carrying forward until the next one."""
        seen, out, current = {}, {}, first
        for line in lines:
            m = pattern.match(line.text)
            if m and line.page not in seen:
                seen[line.page] = m.group(1).upper()
        for page in range(1, max((l.page for l in lines), default=0) + 1):
            current = seen.get(page, current)
            out[page] = current
        return out

    def _check_sections(self, asks):
        """The tab and the question numbers must tell the same story."""
        by_q = {}
        for a in asks:
            by_q.setdefault(a.q, set()).add(a.section)
        for q, secs in sorted(by_q.items()):
            if len(secs) > 1:
                self.flags.append(
                    {'type': 'section-split', 'where': f'Q{q}',
                     'detail': f'the same question is tabbed {sorted(secs)}'})
        reading = sorted(q for q, s in by_q.items() if s == {'A'})
        writing = sorted(q for q, s in by_q.items() if s == {'B'})
        if reading and writing and max(reading) >= min(writing):
            self.flags.append(
                {'type': 'section-order', 'where': '',
                 'detail': f'Section A holds {reading} and Section B {writing}'})
        if None in {a.section for a in asks}:
            self.flags.append({'type': 'section-missing', 'where': '',
                               'detail': 'an ask was printed before any tab'})

    # ----------------------------------------------------------- listening --
    def _walk_aural(self):
        """The Listening Comprehension booklet's own asks.

        Counted, never carded: the ask can only be answered from the recording.
        The count is what the denominator needs and what the exclusions ledger
        has to match one for one.
        """
        aural_tab = re.compile(cfg(self.subject, 'aural_tab'))
        furniture = re.compile(cfg(self.subject, 'furniture'), re.I)
        asks, section, item, roman = [], None, None, None
        current, last_y = None, None

        def close():
            nonlocal current
            if current is not None:
                current.text = _norm(current.text)
                asks.append(current)
                current = None

        lines = read_lines(self.aural_path)
        by_page = self._section_by_page(lines, aural_tab)
        for line in lines:
            if furniture.match(line.text) and len(line.text) < 60:
                continue
            page_section = by_page.get(line.page)
            if page_section != section:
                close()
                section, item, roman = page_section, None, None
            if aural_tab.match(line.text):
                continue
            if section is None:
                continue
            nm = NUMBERED.match(line.text)
            if nm:
                close()
                item, roman = int(nm.group(1)), None
                rest = nm.group(2)
                inner = ROMAN.match(rest)
                if inner:
                    roman, rest = inner.group(1).lower(), inner.group(2)
                # "(1) Aconteceu algo misterioso. (i) Quando?" — the SEC
                # sets an item's stem and its FIRST part on one printed line
                # of the listening booklet, and reading only the number left
                # the roman inside the stem: the part censused as absent and
                # its sibling "(ii)" reported a roman-gap for having no (i).
                inner = INNER_FIRST_ROMAN.search(rest)
                if roman is None and inner and inner.start() > 0:
                    stem = _norm(rest[:inner.start()])
                    if stem:
                        asks.append(Ask(f'L{section}', item, None, None, stem,
                                        line.page))
                    roman, rest = 'i', rest[inner.end():]
                current = Ask(f'L{section}', item, None, roman, rest, line.page)
                last_y = line.y
                continue
            rm = ROMAN.match(line.text)
            if rm and item is not None:
                close()
                roman = rm.group(1).lower()
                current = Ask(f'L{section}', item, None, roman, rm.group(2),
                              line.page)
                last_y = line.y
                continue
            if current is not None and last_y is not None \
                    and 0 <= line.y - last_y <= LINE_GAP \
                    and line.page == current.page:
                current.text += ' ' + line.text
                last_y = line.y
                continue
            close()
        close()
        return _dedupe(asks)

    # ------------------------------------------------------------- the API --
    def all_asks(self):
        """Every leaf the booklets print: a lettered ask with romans under it
        is not a leaf, its romans are."""
        asks = self._asks + self._aural
        has_roman = {(a.section, a.q, a.letter) for a in asks if a.roman}
        has_letter = {(a.section, a.q) for a in asks if a.letter}
        parents = {(a.section, a.q, a.letter): a for a in asks
                   if a.roman is None}
        parents.update({(a.section, a.q, None): a for a in asks
                        if a.letter is None and a.roman is None})
        out = []
        for a in asks:
            if a.roman:
                parent = parents.get((a.section, a.q, a.letter))
                a.stem = parent.text if parent is not None else ''
                out.append(a)
            elif a.letter:
                parent = parents.get((a.section, a.q, None))
                if parent is not None and parent is not a:
                    a.stem = parent.text
                elif not CHOICE_ONLY.sub('', a.text).strip():
                    # No parent ask, and no words of its own: the question's
                    # own printed rubric is all this option has.
                    a.stem = self.leads.get(a.q, '')
                if (a.section, a.q, a.letter) not in has_roman:
                    out.append(a)
            elif (a.section, a.q) not in has_letter \
                    and (a.section, a.q, None) not in has_roman:
                out.append(a)
        return out

    def reading_asks(self):
        return [a for a in self.all_asks()
                if a.section == 'A' or a.section == 'I']

    def writing_asks(self):
        return [a for a in self.all_asks() if a.section in ('B', 'II', 'III')]

    def aural_asks(self):
        return [a for a in self.all_asks() if (a.section or '').startswith('L')]

    def lead(self, q):
        return self.leads.get(q, '')

    def pages_for(self, q):
        return self.text_pages.get(q) or []

    def cover_marks(self):
        """What the booklets say on their own covers or instructions, added."""
        total = 0
        for path in [self.path] + ([self.aural_path] if self.aural_path else []):
            with pymupdf.open(path) as doc:
                text = _norm(' '.join(doc[p].get_text()
                                      for p in range(min(3, doc.page_count))))
            # The sentence the booklet states its own total in, before any
            # per-section figure: "This examination carries 180 marks in
            # total." Taking the first "N marks" on the page instead took
            # Section A's 50 in 2022 and called the booklet a 50-mark paper.
            m = re.search(r'carries\s+(\d{2,3})\s*marks', text, re.I) \
                or re.search(r'(?:M[áa]ximo|Maximum)\s*(?:de)?\s*(\d{2,3})\b',
                             text, re.I) \
                or re.search(r'(\d{2,3})\s*marks\b', text, re.I)
            if m:
                total += int(m.group(1))
        return total


# The word the SEC prints BETWEEN two options of a choice. It is furniture, not
# an ask's text: 2024 Ordinary's Question 5(c) is a picture with "OU" above it,
# and read as the option's own words it censused as a leaf saying "OU".
CHOICE_ONLY = re.compile(r'^\s*(?:OU|OR|NO)\s*$', re.I)


def _dedupe(asks):
    """An ask printed twice keeps the printing that has the question in it.

    The written booklet reprints Question 5's three options on a page of its
    own as an ANSWER SHEET — "Opção:  (a)   (b)   (c)" — and the listening
    booklet does the same with a table. Those markers open asks with no words
    at all, and taken as the later printing they overwrote the real question:
    every Section B option in the corpus censused as an empty leaf.
    """
    best = {}
    order = []
    for a in asks:
        if a.key not in best:
            best[a.key] = a
            order.append(a.key)
        elif len(a.text) > len(best[a.key].text):
            best[a.key] = a
    return [best[k] for k in order]


def _walk_down_paper_splits(asks):
    """A split printed on the QUESTION, walked down to the parts it prices.

    The classic paper prices Question 1 "(5×1)" in its right-hand margin and
    then prints five expressions a) to e) beneath it with no marks beside any
    of them. The tariff for each part IS stated — it is the "1" of the "5×1" —
    but one level above the ask it belongs to. Walked ONLY where the split and
    the parts agree in number; where they do not, nothing is inferred and each
    part keeps whatever it printed for itself.
    """
    kids = {}
    for a in asks:
        if a.letter:
            kids.setdefault((a.section, a.q), []).append(a)
    for a in asks:
        if a.letter or a.tariff is None:
            continue
        group = kids.get((a.section, a.q)) or []
        count, per, _total = a.tariff
        if not group or len(group) != count or any(k.tariff for k in group):
            continue
        for kid in group:
            kid.tariff = (1, per, per)
            kid.notation = (f'{a.notation} on the head of Q{a.q}, walked down '
                            f'to its {count} parts')


def _read_paper_tariff(ask):
    """The price the CLASSIC paper prints in its right-hand margin.

    "(5)" is a total; "(5×1)" is five answers at one point each. Both are read
    and neither is invented — a classic sitting whose ask carries no bracketed
    number keeps `tariff = None` and is refused rather than priced by guesswork.
    """
    m = None
    for candidate in PAPER_TARIFF.finditer(ask.text):
        m = candidate                       # the LAST one on the ask's lines
    if not m:
        return
    if m.group(1):
        count, per = int(m.group(1)), int(m.group(2))
        ask.tariff = (count, per, count * per)
    else:
        ask.tariff = (1, int(m.group(2)), int(m.group(2)))
    ask.notation = m.group(0).strip()


# The line that NAMES the questions of a section rather than heading one:
# "Responda às TRÊS questões - Questão 3 (a) ou (b) ou (c), Questão 4 …". The
# SEC wraps it, so its tail reaches the reader as a line of its own that opens
# with a question head and is not one. Recognised by naming TWO question
# numbers, which a real head never does.
def _is_choice_rubric(text):
    return len(re.findall(r'Quest[ãa]o\s*\d', text, re.I)) > 1


# --------------------------------------------------------------- matching ---
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
# Words too common to be evidence of anything, in any of the three languages
# or in the English half of the paper.
STOP = {
    'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'is', 'are', 'on',
    'at', 'by', 'with', 'from', 'that', 'this', 'it', 'as', 'be', 'what',
    'which', 'how', 'why', 'does', 'do', 'did', 'was', 'were', 'has', 'have',
    'give', 'details', 'detail', 'about', 'his', 'her', 'him', 'she', 'they',
    'que', 'nao', 'para', 'com', 'uma', 'dos', 'das', 'por', 'seu', 'sua',
    'como', 'quais', 'qual', 'razao', 'texto', 'segundo', 'acordo',
    'paragrafo', 'paragrafos', 'parte', 'partes', 'sao', 'esta', 'este',
    'dos', 'nos', 'mais', 'pelo', 'pela', 'ele', 'ela', 'seus', 'suas',
}


def fold(text):
    """Lower-cased and accent-stripped, so ã and a are one word.

    Portuguese, Romanian and Dutch diacritics all survive the text layer
    intact, so this is a matching convenience, not a repair.
    """
    text = (text or '').lower()
    return ''.join(c for c in unicodedata.normalize('NFKD', text)
                   if not unicodedata.combining(c))


def bag(text):
    return {w for w in WORD.findall(fold(text)) if w not in STOP and len(w) > 2}


def score(a, b):
    """Shared content words over the LONGER side."""
    if not a or not b:
        return 0.0
    return len(a & b) / max(len(a), len(b))


# ----------------------------------------------------------------- the CLI ---
def sittings(subject):
    out = set()
    for path in glob.glob(os.path.join(papers_dir(subject), '*-paper.pdf')):
        m = re.match(r'(\d{4})-(hl|ol|cl)', os.path.basename(path))
        if m:
            out.add((int(m.group(1)), m.group(2)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('subject')
    ap.add_argument('year', nargs='?', type=int)
    ap.add_argument('level', nargs='?')
    ap.add_argument('--aural', action='store_true')
    ap.add_argument('--audit', action='store_true')
    args = ap.parse_args()

    if args.audit:
        for year, level in sittings(args.subject):
            P = EuPaper(year, level, args.subject)
            print(f'{year} {level.upper():2}  {P.era:7} '
                  f'{len(P.all_asks()):4} leaves '
                  f'({len(P.reading_asks())} reading, '
                  f'{len(P.writing_asks())} writing, '
                  f'{len(P.aural_asks())} listening)  '
                  f'cover {P.cover_marks()} marks  '
                  f'letter column x={P.letter_x:.1f}')
            for f in P.flags:
                print(f'      FLAG {f["type"]} {f["where"]} — {f["detail"]}')
        return 0

    P = EuPaper(args.year, args.level, args.subject)
    asks = P.aural_asks() if args.aural else [
        a for a in P.all_asks() if not (a.section or '').startswith('L')]
    for a in asks:
        label = f'{a.section} Q{a.q}' + (f'({a.letter})' if a.letter else '')
        label += f'({a.roman})' if a.roman else ''
        print(f'p{a.page:<3} {label:22} {a.notation:10} {a.text[:100]}')
    print(f'\n{len(asks)} leaf ask(s)')
    for f in P.flags:
        print(f'FLAG {f["type"]} {f["where"]} — {f["detail"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
