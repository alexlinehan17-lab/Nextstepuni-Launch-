#!/usr/bin/env python3
"""Religious Education lane: every printed ask as a band-grid rubric card.

    python3 scripts/markbank/authoring/re_lane.py check 2026 hl     # build in memory, report
    python3 scripts/markbank/authoring/re_lane.py build 2026 hl     # write the sitting's cards
    python3 scripts/markbank/authoring/re_lane.py show 2026 hl      # one line per card

The SEC marks every Religious Education answer, 2010 to 2026, on ONE printed
band grid -- two grids where the tariff reads "20M x 2" -- and prices nothing
per point: the scheme's bullets are examples ("e.g.", "Possible Points") of
what an answer in the top band might say. So a card here is a
`religious-education` rubric (types/markBank.ts), never a list of rows:

  the ask        the paper's own words (re_paper.py, the census reader);
  the criteria   the scheme's "An excellent answer will show ..." (re_scheme.py);
  the points     the scheme's points of reference, without its closing "Etc.";
  the grid       the scheme's band table, read cell by cell from the PDF with
                 find_tables(): each band's label, printed range and the grid's
                 cells for that band, verbatim. Where 2021 prints no grid under
                 its questions, the one MC marking grid it prints sideways is
                 read instead, and each question takes the column whose top
                 range is its per-answer tariff (read_shared_grid);
  the Notes      a "... mark on its merits - Max 10 marks" clause is a ceiling
                 the student ticks; every other Note is a direction.

Nothing is typed. The one string a card carries that the SEC did not print is
`markingGuideNote`, which says how the grid is used (and, where it applies,
which shared grid page its bands come from).

The tariff is the scheme's grid head ("20 Marks x2"), checked against the
ask's own head tariff and the paper's printed marks; any disagreement stops
the build unless the sitting module records it (DISAGREE) with the evidence.
A grid printing two marks rows ("40 Marks" and "20 Marks x2", 2022) is two
ways of marking the answer: the card's own is the row the ask's head names
first, the other is `otherWay`, and the student picks the one they wrote.

Cards land in components/MarkBank/cards/religious-education/rubric-authored.json
(build-deck folds them into the deck), and a sitting built here leaves the
point-card file (scripts/markbank/authored/religious-education.json) at the
same time, so no ask is carded twice. Shipped ids are kept: the id is the
same function of the address re_all.py used.
"""
import collections
import json
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

from re_paper import RePaper                                   # noqa: E402
from re_scheme import ReScheme, schemes_dir                    # noqa: E402
from re_topics import topic_for, concept_for                   # noqa: E402

SUBJECT = 'religious-education'
LIGATURE_WORDS = json.load(open(os.path.join(HERE, 'ligature_words.json'), encoding='utf8'))
RUBRIC_JSON = os.path.join(ROOT, 'components', 'MarkBank', 'cards', SUBJECT, 'rubric-authored.json')
POINT_JSON = os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{SUBJECT}.json')
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_LETTER = {'hl': 'A', 'ol': 'G'}
SPEC_VERSION = 'lc-religious-education-2003'
REVIEWED_AT = '2026-11-05'
MARKING_GUIDE = ('The SEC marks every Religious Education answer on its printed band grid. '
                 'The points of reference are examples, not marks: place the whole answer in one band.')
MARKING_GUIDE_X = ('The SEC marks every Religious Education answer on its printed band grid, here '
                   'once for each answer. The points of reference are examples, not marks: place '
                   'each answer in one band.')
MARKING_GUIDE_WAYS = ('The SEC marks every Religious Education answer on its printed band grid; this '
                      'grid prints a marks row for each way of answering. The points of reference are '
                      'examples, not marks: place each answer in one band.')

# Where the paper's printed marks and the scheme's grid disagree, the card
# follows the GRID (the instrument the examiner marks with) and says so in its
# marking note. Each entry is evidence read off both documents, by key.
DISAGREE = {
    # 2026 Ordinary G(b): the paper prints (80) for the whole part; the scheme
    # heads it "Question G (b) (20MX2)" and its grid "20 Marks x 2".
    (2026, 'ol', ('G', None, 'b', None)): (
        'The paper prints 80 marks for this part; its marking scheme marks it as two '
        'answers at 20 marks each, which is what the grid below shows.'),
}


class LaneError(Exception):
    pass


# Asks held for the coordinator's ruling: a printed grid shape the card cannot
# carry as it stands. A held ask gets no card (it stays open in the ledger)
# until it is ruled on; nothing is guessed in the meantime.
HOLD = {
    # 2019 Higher I(b)(i), 10M: the printed ranges overlap -- 9-10, 6-8, 4-5,
    # 3-4, 2-3, 1-2, 0-1 -- so 1, 2, 3 and 4 each sit in two bands.
    (2019, 'hl', ('I', None, 'b', 'i')): 'the printed ranges overlap',
    # 2018 Higher B(a)(i), 5Mx4: one range cell, "1 [arrow] 0", is printed
    # beside WEAK, VERY WEAK and NO GRADE together.
    (2018, 'hl', ('B', None, 'a', 'i')): 'one range cell printed over three bands',
}
HELD = []


HEAD_TIMES = []        # asks whose "x 2" is read off the ask's head, not the grid

HEAD_TARIFF = re.compile(r'(\d{1,3})\s*M\s*(?:[x×]\s*(\d))?', re.I)


def head_tariffs(notation):
    """(per answer, answers) for each tariff a scheme head prints, in printed
    order: "40M/20Mx2" is [(40, 1), (20, 2)]."""
    return [(int(m.group(1)), int(m.group(2) or 1)) for m in HEAD_TARIFF.finditer(notation or '')]


# The subset fonts' broken text layer, repaired as build-deck repairs a point
# card (glyphmap.json, derived from the schemes themselves): "seƫng out
# informaƟon" is "setting out information". A rubric card does not pass
# through build-deck's repair, so the lane applies it, and refuses any glyph
# in the broken range the map cannot read.
GLYPHMAP = json.load(open(os.path.join(HERE, 'glyphmap.json'), encoding='utf8'))
# this subject's own two, settled by crop (re_paper._glyphs says where each is)
GLYPHMAP.update(json.load(open(os.path.join(HERE, 'glyphmap-religious-education.json'), encoding='utf8')))
BROKEN = re.compile(r'[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]')
REAL = re.compile(r'[\u0100-\u017F\u0218-\u021B\u02B0-\u02FF\u0302\u0305\u0307\u0308\u0370-\u03FF'
                  r'\u0400-\u04FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\u1D62-\u1D6A\u1F00-\u1FFF]')
LIGATURE_CODEPOINTS = re.compile(r'[\u019E\u019F\u01A1\u01A9\u01AB\uFB00-\uFB06]')


def repair(text, where):
    out = ''.join(GLYPHMAP.get(ch, ch) if BROKEN.match(ch) else ch for ch in text)
    # The same fonts' "tt" glyph read as ONE t leaves no odd code point:
    # "very litle errors". repair_ligature_words.py records every misread
    # form it found in this subject's papers and schemes with the word the
    # page prints, and that record is applied here, whole words only.
    for misread, printed in LIGATURE_WORDS.get(SUBJECT, {}).items():
        out = re.sub(rf'(?<![\w]){re.escape(misread)}(?![\w])', printed, out)
    left = [ch for ch in out if (BROKEN.match(ch) and not REAL.match(ch)) or LIGATURE_CODEPOINTS.match(ch)]
    if left:
        raise LaneError(f'{where}: unreadable glyph(s) {left} in {out[:80]!r}')
    return out


def repair_all(node, where):
    if isinstance(node, str):
        return repair(node, where)
    if isinstance(node, list):
        return [repair_all(x, where) for x in node]
    if isinstance(node, dict):
        return {k: (v if k in ('id', 'conceptId', 'topicId') else repair_all(v, where)) for k, v in node.items()}
    return node


def ws(text):
    return ' '.join(str(text or '').split())


def card_id(year, level, key):
    section, q, letter, roman = key
    parts = ['re', str(year), level, section.lower()]
    if q is not None:
        parts.append(str(q))
    if letter:
        parts.append(letter)
    if roman:
        parts.append(roman)
    return '-'.join(parts)


def question_ref(year, level, key):
    section, q, letter, roman = key
    ref = f'{year} {level.upper()} Section {section}'
    if q is None and letter is None and roman is None:
        return ref                       # a section that prints ONE unlettered ask
    ref += ' Q'
    if q is not None:
        ref += str(q)
    if letter:
        ref += f'({letter})'
    if roman:
        ref += f'({roman})'
    return ref


# ── the band grid ───────────────────────────────────────────────────────────
BAND_WORD = re.compile(r'EXCELLENT|VERY\s*GOOD|GOOD|FAIR|WEAK|POOR|NO\s*GRADE', re.I)
RANGE = re.compile(r'^\s*(\d{1,2})\s*(?:[-–—>]\s*(\d{1,2}))?\s*$')


class Band:
    def __init__(self, label, printed, marks, descriptor):
        self.label, self.printed, self.marks, self.descriptor = label, printed, marks, descriptor

    def as_json(self):
        out = {'label': self.label, 'printed': self.printed, 'marks': self.marks}
        if self.descriptor:
            out['descriptor'] = self.descriptor
        return out


class Grid:
    def __init__(self, page, top, head, per, times, bands, last=None, rows=None):
        self.page, self.top, self.head, self.per, self.times, self.bands = page, top, head, per, times, bands
        self.last = last or page        # the page its last row is on (a grid the page break cuts)
        # every marks row the grid prints, (head, per, times, printed ranges):
        # 2022 prints a "40 Marks" row AND a "20 Marks x2" row under one grid
        self.rows = rows or [(head, per, times, [b.printed for b in bands])]
        self.row_grid = self.beside_x2 = False
        self.problem = None             # a printed shape the card cannot carry yet: the ask stops

    def use(self, k):
        self.head, self.per, self.times, printed = self.rows[k]
        for b, p in zip(self.bands, printed):
            b.printed, b.marks = p, _marks_of(p)

    def __repr__(self):
        return f'<Grid p{self.page} {self.head!r} {self.per}x{self.times} {len(self.bands)} bands>'


def _marks_of(cell):
    m = RANGE.match(cell.replace('–', '-'))
    if not m:
        return None
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return list(range(min(a, b), max(a, b) + 1))


# Words the sitting's scheme prints, for rejoining a word a narrow grid cell
# wraps WITHOUT a hyphen ("substanti" / "al errors(s)", 2023 Ordinary H(a)).
VOCAB = collections.Counter()


def _cell(text):
    lines = [l.strip() for l in str(text or '').split('\n') if l.strip()]
    out = ''
    for line in lines:
        # a compound word the cell wraps AT its hyphen ("non-" / "violence",
        # "decision-" / "making") is one printed word: rejoined, hyphen kept
        if re.search(r'[A-Za-z][-\u2010]$', out) and line[:1].isalpha():
            out += line
            continue
        if out and VOCAB:
            left = re.search(r'([a-z]+)$', out)
            right = re.match(r'([a-z]+)', line)
            if left and right:
                whole = left.group(1) + right.group(1)
                # joined only when the whole word is printed more often than
                # either fragment: the md carries the same wrap once or twice
                if VOCAB[whole] > max(VOCAB[left.group(1)], VOCAB[right.group(1)]):
                    out += line
                    continue
        out = f'{out} {line}' if out else line
    return ws(out)


def _rows(table):
    rows = [[_cell(c) for c in row] for row in table.extract()]
    return [r for r in rows if any(r)]


BAND_LABEL = re.compile(r'^[-/–\s]*(?:(?:EXCELLENT|VERY|GOOD|FAIR|WEAK|POOR|NO|GRADE)\s*[-/–]?\s*)+$', re.I)


def _is_band_header(row):
    """A grid's header row: every cell after the first is made of band label
    words only (or blank under a label set over two columns). A descriptor
    row can open with band WORDS too -- "Use of skill(s)": "Excellent",
    "very good", "good", "some" -- and reading it as a header kept 2022
    Ordinary C(b)'s continuation from joining its grid. A label the cell
    wraps ("VERY" over "GOOD") is still band words."""
    cells = [c for c in row[1:] if c]
    return len(cells) >= 4 and all(BAND_LABEL.match(c) for c in cells)


def _has_marks_row(rows):
    return any(r[1:] and all(_marks_of(c) for c in r[1:] if c) and any(r[1:]) and
               sum(1 for c in r[1:] if c) >= 3 for r in rows[1:])


def _is_marks(row):
    cells = [c for c in row[1:] if c]
    return len(cells) >= 3 and all(_marks_of(c) for c in cells)


def _merge_fragments(rows):
    """A cell whose text the table reader cut across two rows is put back
    together, one printed cell again:
      - under the header, a row of band words only is the rest of a wrapped
        label ("VERY" over "GOOD", 2022 Higher B(c)(ii)) and joins the header;
      - a row with only its first cell is the rest of the criterion above it
        ("Evidence of MC one ..." over "Saint Patrick during ...");
      - a row with no criterion of its own joins the row below when that row
        names a criterion ("Completely" over "& clearly relevant", 2024
        Ordinary) -- unless the row below is the marks row, when it is the
        rest of the row above ("some major" over "errors(s)", 2022 Ordinary)."""
    out = [rows[0]]
    i = 1
    while i < len(rows) and not rows[i][0] and _is_band_header(['x'] + rows[i][1:]) is False \
            and all(not c or BAND_LABEL.match(c) for c in rows[i][1:]) and any(rows[i][1:]):
        out[0] = [ws(f'{a} {b}') for a, b in zip(out[0], rows[i])]
        i += 1
    pending = None
    for n in range(i, len(rows)):
        row = rows[n]
        if row[0] and not any(row[1:]) and len(out) > 1:
            out[-1] = [ws(f'{out[-1][0]} {row[0]}')] + out[-1][1:]
            continue
        if not row[0] and not _is_marks(row):
            nxt = rows[n + 1] if n + 1 < len(rows) else None
            if (nxt is None or _is_marks(nxt)) and len(out) > 1 and pending is None:
                out[-1] = [ws(f'{a} {b}') for a, b in zip(out[-1], row)]
                continue
            pending = row if pending is None else [ws(f'{a} {b}') for a, b in zip(pending, row)]
            continue
        if pending is not None:
            row = [ws(f'{a} {b}') if k else b for k, (a, b) in enumerate(zip(pending, row))]
            pending = None
        out.append(row)
    if pending is not None:
        out[-1] = [ws(f'{a} {b}') for a, b in zip(out[-1], pending)]
    return out


# Cells are the RULED cells: 'lines_strict' builds rows from the drawn rules
# alone, so a cell whose text runs to two lines stays one cell. The default
# also cuts rows at text lines ("Completely" over "& clearly relevant").
STRATEGY = 'lines_strict'


class _Table:
    """A table's box and rows, read once: a later find_tables() call on the
    same page invalidates the earlier result's cells (2026 Higher p20's grid
    read back EMPTY after the page-wide table above it was re-read). `cells`
    keeps every row's cell boxes, unfiltered, with `texts` beside them."""
    def __init__(self, bbox, rows, cells=None, texts=None):
        self.bbox, self.rows = tuple(bbox), rows
        self.cells, self.texts = cells or [], texts or []


def _read(page, clip=None):
    found = page.find_tables(clip=clip, strategy=STRATEGY).tables if clip is not None \
        else page.find_tables(strategy=STRATEGY).tables
    out = []
    for t in found:
        texts = [[_cell(c) for c in row] for row in t.extract()]
        cells = [[tuple(c) if c else None for c in row.cells] for row in t.rows]
        out.append(_Table(t.bbox, [r for r in texts if any(r)], cells, texts))
    return out


# ── the row grid (2018-2020) ────────────────────────────────────────────────
# 2018-2020 print each ask's grid a band to a ROW: two bulleted descriptor
# columns in one ruled cell, the band's label, its range ("• substantial
# evidence of MC  • no major error(s)  EXCELLENT  17 - 20"). No marks head is
# printed; a two-answer ask's grid has "x2" printed beside its top range.
ROW_BULLETS = '•●\uf0b7\uf06c'


def _is_row_grid(texts):
    """Every row a band label then its range. A range cell the scheme sets
    over several bands (2018 Higher B(a)(i): "1 ↑ 0" beside WEAK, VERY WEAK and
    NO GRADE) leaves the rows below it blank: the grid is still read, and the
    ask stops for a ruling."""
    rows = [r for r in texts if any(r)]
    return len(rows) >= 4 and all(len(r) >= 3 and BAND_LABEL.match(r[-2] or '') for r in rows) \
        and bool(_marks_of(rows[0][-1]))


def _bullet_items(page, rect):
    """A descriptor cell's bullets, read down each printed column in turn: the
    cell sets two columns of bullets side by side, and reading it by line
    would interleave them."""
    words = [w for w in page.get_text('words', clip=pymupdf.Rect(rect))]
    starts = []
    for x in sorted(round(w[0]) for w in words if w[4] and w[4][0] in ROW_BULLETS):
        if not starts or x - starts[-1] > 20:
            starts.append(x)
    if not starts:
        return []
    columns = [[] for _ in starts]
    for w in words:
        k = max([i for i, x in enumerate(starts) if w[0] >= x - 3] or [0])
        columns[k].append(w)
    items = []
    for col in columns:
        # lines by the words' middles, then each line left to right: a bullet
        # sits a fraction of a point off its text's baseline (510.7 against
        # 510.5), and sorting on a rounded top put it after its own words
        lines = []
        for w in sorted(col, key=lambda w: (w[1] + w[3]) / 2):
            mid = (w[1] + w[3]) / 2
            if lines and abs(mid - lines[-1][0]) < 4:
                lines[-1][1].append(w)
            else:
                lines.append([mid, [w]])
        text = _cell('\n'.join(' '.join(w[4] for w in sorted(ws_, key=lambda w: w[0])) for _, ws_ in lines))
        items.extend(ws(x) for x in re.split(f'[{ROW_BULLETS}]', text) if ws(x))
    return items


def _row_grid(page, pno, table, year, level):
    rows = [(r, c) for r, c in zip(table.texts, table.cells) if any(r)]
    bands = []
    for text, cells in rows:
        label, printed = text[-2], text[-1]
        descriptor = []
        for box in cells[:-2]:
            if box is not None:
                descriptor.extend(_bullet_items(page, box))
        if not descriptor:
            raise LaneError(f'{year} {level} p{pno + 1}: a row-grid band with no bulleted descriptors: {text}')
        bands.append(Band(label, printed, _marks_of(printed), descriptor))
    x0, y0, x1, y1 = table.bbox
    beside = ' '.join(w[4] for w in page.get_text('words', clip=pymupdf.Rect(x1, y0 - 2, page.rect.width, y1)))
    per = max(m for b in bands for m in (b.marks or []))
    grid = Grid(pno + 1, y0, None, per, 1, bands)
    grid.row_grid = True
    unread = [(b.label, b.printed) for b in bands if not b.marks]
    if unread:
        grid.problem = f'band ranges not one per band as printed: {unread}'
    else:
        marks = sorted(m for b in bands for m in b.marks)
        if marks != list(range(per + 1)):
            grid.problem = ('the printed ranges overlap or leave a gap: '
                            + ', '.join(f'{b.label} {b.printed}' for b in bands))
    grid.beside_x2 = bool(re.fullmatch(r'\s*[xX×]\s*2\s*', beside))
    if beside.strip() and not grid.beside_x2:
        raise LaneError(f'{year} {level} p{pno + 1}: {beside!r} printed beside a row grid')
    return grid


def _page_tables(page):
    """The page's tables, with a page-wide layout table (2024 Ordinary sets
    the prose above a grid and the grid in one table that spans the page,
    offsetting every column by one) re-read inside the content columns."""
    out = []
    for table in _read(page):
        if table.bbox[0] < 40 and table.bbox[2] > page.rect.width - 40:
            out.extend(_read(page, pymupdf.Rect(60, table.bbox[1], page.rect.width - 40, table.bbox[3])))
        else:
            out.append(table)
    return out


def read_grids(year, level):
    """Every exam band grid in the scheme, in page order. A coursework grid
    (the journal's "Set Points" / "Set Questions" tables) is not an exam ask
    and is skipped. A grid the page break cuts in two (2024: the header and
    first rows at the foot of one page, the rest at the head of the next) is
    read back as one, its continuation re-read inside the first part's
    columns so a page-wide layout table above it cannot shift them."""
    doc = pymupdf.open(os.path.join(schemes_dir(), f'{year}-{level}.pdf'))
    VOCAB.clear()
    VOCAB.update(re.findall(r'[a-z]+', open(os.path.join(schemes_dir(), f'{year}-{level}.md'),
                                         encoding='utf8').read().lower()))
    out = []
    taken = set()                 # (page, rounded top) of continuations already read
    for pno, page in enumerate(doc):
        for table in _page_tables(page):
            if (pno, round(table.bbox[1])) in taken:
                continue
            if _rotated(page, table.bbox):
                continue                 # the shared grid printed sideways: read_shared_grid
            if _is_row_grid(table.texts):
                grid = _row_grid(page, pno, table, year, level)
                if not grid.problem and 0 not in grid.bands[-1].marks:
                    raise LaneError(f'{year} {level} p{pno + 1}: a row grid that stops above 0: {grid}')
                out.append(grid)
                continue
            rows = table.rows
            start = next((i for i, r in enumerate(rows) if _is_band_header(r)), None)
            if start is None:
                continue
            rows = rows[start:]          # prose the table reader swept in above the grid
            last = pno + 1
            if re.search(r'Set\s+(?:Points|Ques)', ' '.join(rows[0])):
                continue
            if not _has_marks_row(rows) and pno + 1 < doc.page_count:
                x0, x1 = table.bbox[0], table.bbox[2]
                nxt = doc[pno + 1]
                cont = sorted(_read(nxt, pymupdf.Rect(x0 - 2, 0, x1 + 2, nxt.rect.height)),
                              key=lambda t: t.bbox[1])
                cont = [t for t in cont if t.rows]
                if cont and not _is_band_header(cont[0].rows[0]):
                    more = cont[0].rows
                    width = max(len(r) for r in rows + more)
                    rows = [r + [''] * (width - len(r)) for r in rows]
                    more = [r + [''] * (width - len(r)) for r in more]
                    # The break can cut a ROW, leaving its rest at the head of
                    # the next page: with no criterion of its own (2022 Higher
                    # C(a): "looking closely" under "very good"), or with the
                    # rest of the criterion, which then opens in lower case
                    # (2022 Ordinary G(b)(ii): "drawing accurate conclusions"
                    # under "Use of skill(s) examining and"). Every criterion
                    # the grids print opens with a capital.
                    if more and (not more[0][0] or more[0][0][:1].islower()):
                        rows[-1] = [ws(f'{a} {b}') for a, b in zip(rows[-1], more[0])]
                        more = more[1:]
                    rows = rows + more
                    last = pno + 2
                    for t in _page_tables(nxt):
                        if t.bbox[1] <= cont[0].bbox[3] and t.bbox[3] >= cont[0].bbox[1]:
                            taken.add((pno + 1, round(t.bbox[1])))
            width = max(len(r) for r in rows)
            rows = [r + [''] * (width - len(r)) for r in rows]
            keep = [j for j in range(width) if any(r[j] for r in rows)]
            rows = [[r[j] for j in keep] for r in rows]
            rows = _merge_fragments(rows)
            # A header the scheme sets over several range columns ("WEAK - VERY
            # WEAK - NO GRADE" over 7-5 and 4-0) leaves the later columns
            # blank: each range carries the label printed over it.
            labels = []
            for label in rows[0][1:]:
                labels.append(label or (labels[-1] if labels else ''))
            # The marks rows close the grid: every row whose cells all read as
            # ranges. A grid can print two (2022: "40 Marks" for the answer
            # whole, "20 Marks x2" for it in two), and a marks row is never a
            # descriptor: the card takes the one its ask's head names.
            marks_at = [i for i in range(1, len(rows))
                        if rows[i][1:] and all(_marks_of(c) for c in rows[i][1:])]
            if not marks_at:
                raise LaneError(f'{year} {level} p{pno + 1}: a band grid with no marks row: {rows[-1]}')
            if marks_at != list(range(marks_at[0], len(rows))):
                raise LaneError(f'{year} {level} p{pno + 1}: a descriptor row after a marks row: {rows}')
            at = marks_at[0]
            alts = []
            for i in marks_at:
                head = rows[i][0]
                nums = [int(n) for n in re.findall(r'\d+', head)]
                times = 2 if re.search(r'x\s*2|×\s*2', head, re.I) else 1
                printed = rows[i][1:]
                per = nums[0] if nums else max(m for p in printed for m in _marks_of(p))
                alts.append((head, per, times, printed))
            bands = []
            for k, label in enumerate(labels):
                descriptor = []
                for r in rows[1:at]:
                    crit, cell = r[0], r[k + 1]
                    if cell:
                        descriptor.append(f'{crit}: {cell}' if crit else cell)
                bands.append(Band(label, '', None, descriptor))
            grid = Grid(pno + 1, table.bbox[1], *alts[-1][:3], bands, last=last, rows=alts)
            grid.use(len(alts) - 1)
            out.append(grid)
    return out


def grid_problem(grid):
    marks = sorted(m for b in grid.bands for m in b.marks)
    if marks != list(range(grid.per + 1)):
        return f'bands cover {marks} not 0..{grid.per}'
    return None


# ── the shared grid (2021) ──────────────────────────────────────────────────
# 2021 prints no grid under its questions. Each question prints "Code MC" (or
# "Code MCx2"), and ONE table, printed sideways on its own page, is the MC
# marking grid: a row per band, the band's descriptors in two bulleted cells,
# then one range column per tariff, with no heading over the columns. The
# coordinator's ruling (5 Nov): each question takes the column whose top
# range is its per-answer tariff; no match, or two, and the question stops.

def _rotated(page, bbox):
    """True when the text inside bbox runs down the page, not across it."""
    across = down = 0
    for b in page.get_text('dict', clip=pymupdf.Rect(bbox))['blocks']:
        for line in b.get('lines', []):
            if not line['spans'] or not ''.join(s['text'] for s in line['spans']).strip():
                continue
            if abs(line['dir'][0]) > 0.9:
                across += 1
            else:
                down += 1
    return down > across


class SharedGrid:
    def __init__(self, page, folio, labels, descriptors, columns):
        self.page, self.folio = page, folio
        self.labels, self.descriptors, self.columns = labels, descriptors, columns

    def column(self, per):
        """The printed ranges of the column whose top is `per`, or None."""
        hits = [c for c in self.columns if c[0] == per]
        if len(hits) != 1:
            return None
        return hits[0][1]


BULLET = '\uf06c'      # the Wingdings bullet each descriptor opens with


def read_shared_grid(year, level):
    """The one sideways band grid of a scheme that prints none under its
    questions, read cell by cell: the drawn rules give the cells (their rows
    on the page are the grid's columns), and each cell's text is its lines in
    reading order (text running down the page reads right to left)."""
    doc = pymupdf.open(os.path.join(schemes_dir(), f'{year}-{level}.pdf'))
    found = []
    for pno, page in enumerate(doc):
        for t in page.find_tables(strategy=STRATEGY).tables:
            if not _rotated(page, t.bbox):
                continue
            lines = []
            for b in page.get_text('dict', clip=pymupdf.Rect(t.bbox))['blocks']:
                for line in b.get('lines', []):
                    text = ''.join(s['text'] for s in line['spans'])
                    if text.strip() and tuple(round(x, 2) for x in line['dir']) == (0.0, 1.0):
                        lines.append((pymupdf.Rect(line['bbox']), text))
            grid = []                       # the grid's columns, each a cell per band
            merged = False
            for row in t.rows:
                cells = []
                for c in row.cells:
                    if c is None:
                        merged = True
                        cells.append([])
                        continue
                    rect = pymupdf.Rect(c)
                    inside = [(r, x) for r, x in lines
                              if rect.contains(pymupdf.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))]
                    inside.sort(key=lambda z: (-z[0].x1, z[0].y0))
                    cells.append([x for _, x in inside])
                grid.append(cells[::-1])        # the band read first is the rightmost
            labels = [ws(' '.join(c)) for c in grid[0]]
            if not all(BAND_LABEL.match(x) for x in labels) or len(labels) < 4:
                continue                    # the coursework tables, also printed sideways
            if merged:
                raise LaneError(f'{year} {level} p{pno + 1}: a merged cell in the sideways grid')
            descriptors = [[] for _ in labels]
            columns = []
            for col in grid[1:]:
                texts = [ws(' '.join(c)) for c in col]
                if all(_marks_of(x) for x in texts):
                    top = max(m for x in texts for m in _marks_of(x))
                    columns.append((top, texts))
                    continue
                if columns:
                    raise LaneError(f'{year} {level} p{pno + 1}: a descriptor column after a range column')
                for k, cell in enumerate(col):
                    text = ws(' '.join(cell))
                    if not text.startswith(BULLET):
                        raise LaneError(f'{year} {level} p{pno + 1}: a descriptor cell without bullets: {text!r}')
                    descriptors[k].extend(ws(x) for x in text.split(BULLET) if ws(x))
            for top, texts in columns:
                marks = sorted(m for x in texts for m in _marks_of(x))
                if marks != list(range(top + 1)):
                    raise LaneError(f'{year} {level} p{pno + 1}: the {top} column covers {marks}')
            folio = next((ws(b[4]) for b in page.get_text('blocks')
                          if re.fullmatch(r'\d{1,2}', ws(b[4])) and b[1] > page.rect.height - 80), None)
            if folio is None:
                raise LaneError(f'{year} {level} p{pno + 1}: no printed page number under the sideways grid')
            found.append(SharedGrid(pno + 1, folio, labels, descriptors, columns))
    if len(found) > 1:
        raise LaneError(f'{year} {level}: {len(found)} sideways grids; one is expected')
    return found[0] if found else None


CODE_MC = re.compile(r'^Code\s+MC\s*(?:[x×]\s*(\d))?\s+in\b')


def code_mc(scheme, ask, nxt):
    """(N, line) for the one "Code MC" / "Code MCxN" line the ask's block
    prints, or None."""
    end = nxt.line if nxt is not None else len(scheme.lines)
    hits = [(i, CODE_MC.match(scheme.lines[i].strip())) for i in range(ask.line, end)]
    hits = [(i, m) for i, m in hits if m]
    if len(hits) != 1:
        return None
    i, m = hits[0]
    return int(m.group(1) or 1), i


# ── Notes: ceilings and directions ──────────────────────────────────────────
CEILING = re.compile(r'(If a candidate\b.*?)\s*[-–]?\s*Max(?:imum)?\.?\s*(\d{1,2})\s*marks?'
                     r'(\s*[x×]\s*2)?\s*\.?', re.I | re.S)


def split_notes(notes, answers, where):
    ceilings, directions = [], []
    for note in notes:
        text = ws(note)
        rest = text
        for m in CEILING.finditer(text):
            when = ws(m.group(1)).rstrip(' ,-–')
            per_answer = bool(m.group(3))
            if answers > 1 and not per_answer:
                raise LaneError(f'{where}: a ceiling on a two-answer ask without "x 2": {text!r}')
            ceilings.append({'when': when, 'max': int(m.group(2))})
            rest = rest.replace(m.group(0), ' ')
        rest = ws(rest)
        if rest and rest not in ('Note:',):
            directions.append(rest)
    return ceilings, directions


# ── one sitting ─────────────────────────────────────────────────────────────
def md_page_of(scheme):
    pages, page = [], 0
    for line in scheme.lines:
        m = re.match(r'^##\s*Page\s*(\d+)', line)
        if m:
            page = int(m.group(1))
        pages.append(page)
    return pages


def shipped_cards():
    """Every RE card already shipped, by id: the point cards not yet rebuilt and
    the band-grid cards already built, so a rebuild keeps topic, concept and
    stem whichever deck the card is in."""
    out = {}
    if os.path.exists(POINT_JSON):
        out.update({c['id']: c for c in json.load(open(POINT_JSON, encoding='utf8'))})
    if os.path.exists(RUBRIC_JSON):
        out.update({c['id']: c for c in json.load(open(RUBRIC_JSON, encoding='utf8'))['cards']})
    return out


def build_sitting(year, level, shipped=None, survey=None):
    """The sitting's cards. With `survey` (a list), an ask that stops is noted
    there and left out, so every stop in a sitting can be seen at once; a
    build never passes it."""
    shipped = shipped_cards() if shipped is None else shipped
    P = RePaper(year, level)
    S = ReScheme(year, level)
    if S.refused:
        raise LaneError(f'{year} {level}: the scheme reader refused {S.refused}')
    asks = sorted(S.asks, key=lambda a: a.line)
    keys = [a.key for a in asks]
    if set(keys) != set(P.asks) or len(keys) != len(set(keys)):
        raise LaneError(f'{year} {level}: scheme asks {sorted(map(str, set(keys) ^ set(P.asks)))} '
                        f'do not pair with the paper')
    grids = read_grids(year, level)
    shared = read_shared_grid(year, level) if not grids else None
    if shared is None and len(grids) != len(asks):
        raise LaneError(f'{year} {level}: {len(grids)} band grids for {len(asks)} asks: {grids}')
    pages = md_page_of(S)
    cards = []
    def one(n, ask):
            key = ask.key
            where = f'{year} {level} {question_ref(year, level, key)}'
            head_page = pages[ask.line]
            next_page = pages[asks[n + 1].line] if n + 1 < len(asks) else 10 ** 3
            shared_note = None
            if shared is not None:
                grid, shared_note, block_end = shared_grid_for(S, asks, n, shared, where)
                last_page = pages[block_end]
            else:
                grid = grids[n]
                if not head_page <= grid.page <= next_page:
                    raise LaneError(f'{where}: its grid is on p{grid.page}, outside its block '
                                    f'(p{head_page}-{next_page})')
                last_page = grid.last
            # A row grid prints no marks head: its top range is the per-answer
            # tariff, and the ask's head says how many answers ("20Mx2"); an "x2"
            # printed beside the grid must agree.
            if grid.problem:
                raise LaneError(f'{where}: STOP: {grid.problem}')
            if grid.row_grid:
                named = [t for t in head_tariffs(ask.notation) if t[0] == grid.per]
                if len(named) != 1:
                    raise LaneError(f'{where}: STOP: the row grid tops out at {grid.per}; head {ask.notation!r}')
                grid.times = named[0][1]
                if grid.beside_x2 and grid.times != 2:
                    raise LaneError(f'{where}: "x2" beside the grid, head {ask.notation!r}')
                grid.head = ask.notation
            # A grid printing two marks rows is two printed ways of marking the
            # answer: the card's own way is the row its head names first, and the
            # other row rides along as `otherWay` for the student to pick.
            other_way = None
            if len(grid.rows) > 1:
                if len(grid.rows) != 2:
                    raise LaneError(f'{where}: {len(grid.rows)} marks rows in one grid: {grid.rows}')
                named = head_tariffs(ask.notation)
                if not named:
                    raise LaneError(f'{where}: two marks rows and a head {ask.notation!r} naming neither')
                pick = [k for k, r in enumerate(grid.rows) if (r[1], r[2]) == named[0]]
                if len(pick) != 1:
                    raise LaneError(f'{where}: the head\'s {named[0]} matches {len(pick)} of the grid\'s '
                                    f'marks rows {[r[:3] for r in grid.rows]}')
                grid.use(pick[0])
                head, per, times, printed = grid.rows[1 - pick[0]]
                marks = sorted(m for p in printed for m in _marks_of(p))
                if marks != list(range(per + 1)) or per * times != ask.total:
                    raise LaneError(f'{where}: the other marks row {head!r} covers {marks}, {per}x{times}')
                other_way = {'gridHead': head, 'answers': times, 'answerMax': per,
                             'bands': [{'printed': p, 'marks': _marks_of(p)} for p in printed]}
            problem = grid_problem(grid)
            if problem:
                raise LaneError(f'{where}: {grid}: {problem}')
            # A grid whose marks cell omits the "x 2" its own ask's head prints
            # (2024 Ordinary B(a): head "(20M x 2)", grid "20 Marks", "Code MC
            # x 2" above it) is the per-answer grid of a two-answer ask: the
            # scheme says so on the head, so the head's multiplier is read.
            if (grid.times == 1 and grid.per * 2 == ask.total
                    and re.search(r'[x×]\s*2', ask.notation or '', re.I)):
                grid.times = 2
                HEAD_TIMES.append(where)
            total = grid.per * grid.times
            paper_marks = P.marks.get(key)
            note = DISAGREE.get((year, level, key))
            if total != ask.total or (paper_marks is not None and paper_marks != total):
                if not note:
                    raise LaneError(f'{where}: grid {grid.head!r} = {total}, scheme head {ask.notation!r} = '
                                    f'{ask.total}, paper ({paper_marks})')
            question = P.asks[key]
            stem = P.stem(key)
            cid = card_id(year, level, key)
            old = shipped.get(cid)
            topic = old['topicId'] if old else topic_for(key[0])
            if not topic:
                raise LaneError(f'{where}: section {key[0]} is not a syllabus section')
            if not ask.lead:
                raise LaneError(f'{where}: the scheme prints no "An excellent answer" criteria')
            ceilings, directions = split_notes(ask.notes, grid.times, where)
            if other_way and ceilings:
                raise LaneError(f'{where}: STOP: a ceiling on a grid with two marks rows')
            for c in ceilings:
                if not 0 < c['max'] < grid.per:
                    raise LaneError(f'{where}: ceiling {c} not inside the answer\'s {grid.per}')
            rubric = {
                'system': 'religious-education',
                'criteria': ask.lead,
                'points': ask.points,
                'openList': bool(ask.open_list),
                'answers': grid.times,
                'answerMax': grid.per,
                'gridHead': grid.head,
                'bands': [b.as_json() for b in grid.bands],
            }
            if other_way:
                rubric['otherWay'] = other_way
            if ceilings:
                rubric['ceilings'] = ceilings
            rubric['directions'] = directions
            rubric['markingGuideNote'] = ''.join(n + ' ' for n in (note, shared_note) if n) + \
                (MARKING_GUIDE_WAYS if other_way else MARKING_GUIDE_X if grid.times > 1 else MARKING_GUIDE)
            rubric['schemePages'] = sorted({head_page, grid.page} | set(range(head_page, last_page + 1)))
            rubric['schemeFileid'] = f'LC223{LEVEL_LETTER[level]}LP000EV.pdf'
            card = {
                'id': cid, 'subjectId': SUBJECT, 'source': 'sec', 'kind': 'rubric',
                'year': year, 'level': LEVEL_WORD[level], 'section': key[0],
                'questionRef': question_ref(year, level, key),
                'topicId': topic,
                'conceptId': old['conceptId'] if old else concept_for(question),
                'paperFileid': f'LC223{LEVEL_LETTER[level]}LP000EV',
                'questionText': question,
            }
            if old and old.get('stem'):
                card['stem'] = old['stem']
            elif stem and len(stem) >= 20:
                card['stem'] = stem
            card.update({
                'totalMarks': total,
                'specVersion': SPEC_VERSION,
                'schemeCitation': (f'Marking criteria, points and band grid quoted from the SEC marking scheme, Religious Education '
                                   f'{year} {LEVEL_WORD[level].title()} Level — © State Examinations Commission.'),
                'qa': {'gates': ['verbatim', 'tariff', 'band-grid'], 'humanReviewedBy': 'agent-verified',
                       'humanReviewedAt': REVIEWED_AT},
                'rubric': rubric,
            })
            card = repair_all(card, where)
            if old and old['questionText'] != card['questionText']:
                raise LaneError(f'{where}: the shipped card\'s question differs from the paper reading')
            words = LIGATURE_WORDS.get(SUBJECT, {})
            flat = json.dumps(card, ensure_ascii=False)
            hit = next((w for w in words if re.search(rf'(?<![\w]){re.escape(w)}(?![\w])', flat)), None)
            if hit:
                raise LaneError(f'{where}: misread ligature {hit!r} (printed {words[hit]!r})')
            return card

    for n, ask in enumerate(asks):
        if (year, level, ask.key) in HOLD:
            HELD.append(f'{year} {level} {question_ref(year, level, ask.key)}: {HOLD[(year, level, ask.key)]}')
            continue
        if survey is not None:
            try:
                cards.append(one(n, ask))
            except LaneError as e:
                survey.append(str(e))
            continue
        cards.append(one(n, ask))
    return cards


def shared_grid_for(S, asks, n, shared, where):
    """The ask's bands off the shared grid: the column whose top range is the
    ask's per-answer tariff, the one "Code MC" line its block prints agreeing
    with the head on how many answers are marked. Returns the grid, the note
    naming the source, and the md line the block ends on."""
    ask = asks[n]
    named = head_tariffs(ask.notation)
    if len(named) != 1:
        raise LaneError(f'{where}: STOP: head {ask.notation!r} names {len(named)} tariffs')
    per, times = named[0]
    if per * times != ask.total:
        raise LaneError(f'{where}: head {ask.notation!r} reads {per}x{times}, total {ask.total}')
    code = code_mc(S, ask, asks[n + 1] if n + 1 < len(asks) else None)
    if code is None:
        raise LaneError(f'{where}: STOP: the block prints no single "Code MC" line')
    if code[0] != times:
        raise LaneError(f'{where}: STOP: the block codes MC x{code[0]}, the head {ask.notation!r}')
    printed = shared.column(per)
    if printed is None:
        tops = [c[0] for c in shared.columns]
        raise LaneError(f'{where}: STOP: per-answer tariff {per} matches {tops.count(per)} of the '
                        f'shared grid\'s columns (tops {tops})')
    bands = [Band(label, p, _marks_of(p), list(desc))
             for label, p, desc in zip(shared.labels, printed, shared.descriptors)]
    grid = Grid(shared.page, 0, ask.notation, per, times, bands)
    note = f'Bands from the scheme\'s MC marking grid (page {shared.folio}).'
    return grid, note, code[1]


def sittings_built():
    if not os.path.exists(RUBRIC_JSON):
        return []
    data = json.load(open(RUBRIC_JSON, encoding='utf8'))
    return sorted({(c['year'], {'higher': 'hl', 'ordinary': 'ol'}[c['level']]) for c in data['cards']})


def write(year, level, cards):
    data = json.load(open(RUBRIC_JSON, encoding='utf8')) if os.path.exists(RUBRIC_JSON) else {'v': 1, 'cards': []}
    word = LEVEL_WORD[level]
    kept = [c for c in data['cards'] if not (c['year'] == year and c['level'] == word)]
    allc = kept + cards
    order = {'higher': 0, 'ordinary': 1}
    allc.sort(key=lambda c: (-c['year'], order[c['level']]))
    data = {'v': 1, 'cardCount': len(allc), 'cards': allc}
    with open(RUBRIC_JSON, 'w', encoding='utf8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    # the point cards of this sitting leave the point deck: one card per ask
    if os.path.exists(POINT_JSON):
        points = json.load(open(POINT_JSON, encoding='utf8'))
        left = [c for c in points if not (c['year'] == year and c['level'] == word)]
        if len(left) != len(points):
            with open(POINT_JSON, 'w', encoding='utf8') as fh:
                json.dump(left, fh, ensure_ascii=False, indent=1)
                fh.write('\n')
        return len(points) - len(left)
    return 0


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    cmd, year, level = argv[1], int(argv[2]), argv[3]
    cards = build_sitting(year, level)
    if cmd == 'check':
        x2 = sum(1 for c in cards if c['rubric']['answers'] > 1)
        ceil = sum(len(c['rubric'].get('ceilings', [])) for c in cards)
        kept = sum(1 for c in cards if c['id'] in shipped_cards())
        print(f'{year} {level}: {len(cards)} cards ({kept} shipped ids kept), {x2} two-answer grids, '
              f'{ceil} ceilings, {sum(c["totalMarks"] for c in cards)} marks')
        for where in HEAD_TIMES:
            print(f'   x 2 read off the head: {where}')
        for where in HELD:
            print(f'   HELD for a ruling: {where}')
    elif cmd == 'show':
        for c in cards:
            r = c['rubric']
            print(f"{c['questionRef']:<34} {c['totalMarks']:>3} {r['gridHead']!r:<16} "
                  f"bands={'/'.join(b['label'] + ':' + b['printed'] for b in r['bands'])} "
                  f"pts={len(r['points'])} ceil={r.get('ceilings', [])} dir={r['directions']}")
    elif cmd == 'build':
        removed = write(year, level, cards)
        print(f'{year} {level}: {len(cards)} rubric cards written; {removed} point cards left the point deck')
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except LaneError as e:
        print(f'LANE ERROR: {e}', file=sys.stderr)
        sys.exit(1)
