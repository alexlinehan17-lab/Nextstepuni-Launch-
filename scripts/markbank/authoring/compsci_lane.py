#!/usr/bin/env python3
"""Computer Science cards authored part by part from the page (lane of 5 Nov 2026).

    python3 scripts/markbank/authoring/compsci_lane.py sheet 2026 hl      # worksheet
    python3 scripts/markbank/authoring/compsci_lane.py lines 2026 hl 038 3 # page lines + boxes
    python3 scripts/markbank/authoring/compsci_lane.py crops 2026 hl       # render + publish crops
    python3 scripts/markbank/authoring/compsci_lane.py build 2026 hl       # merge cards into the JSON
    python3 scripts/markbank/authoring/compsci_lane.py build all           # every sitting module

The 336 Computer Science cards that shipped in August came out of an automatic
author (computer_science_all.py) that never reached main. This lane does not
regenerate them. It adds a card for every printed ask the bank does not yet
hold, one module per sitting in compsci_sittings/, and each module says, part
by part, what the page shows and how its card is built:

  * the QUESTION is lifted from the paper's own text layer, by a pair of
    selectors that must both be found on the named page -- the text between
    them is the SEC's, never typed here;
  * every marking point is lifted the same way from the scheme's .md (the very
    file build-deck's provenance gate reads), so a row that is not the scheme's
    own words cannot be written;
  * the tariff is the one the scheme prints, and the module names where: either
    cs_scheme.CsScheme reads it on the part's own row, or `printed=` quotes the
    scheme's tariff cell, which must be found on the scheme page;
  * printed matter the ask depends on (a program, a table, a figure) is a crop
    of the paper page, rendered here and opened before it is published; an
    answer the scheme gives as a drawing is a crop of the scheme page, shown
    only after the reveal (`solution`).

A module's card for an id the bank already ships is an error unless it says
`replaces=` with the reason: shipped ids key students' review history.
"""
import hashlib
import importlib
import json
import os
import re
import sys

import pymupdf

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))
SUBJECT = 'computer-science'
PAPERS = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'papers')
SCHEMES = os.path.join(ROOT, 'examiner-reports', SUBJECT, 'schemes')
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{SUBJECT}.json')
FIGURES = os.path.join(ROOT, 'components', 'MarkBank', 'figures.json')
FIG_DIR = os.path.join(ROOT, 'public', 'exam-figures', SUBJECT, 'markbank')
FIG_SRC = f'/exam-figures/{SUBJECT}/markbank'
SCALE = 2.5          # crop resolution: 180 dpi, the shipped crops' own
# Previews go outside the repository; set COMPSCI_PREVIEW to choose where.
PREVIEW = os.environ.get('COMPSCI_PREVIEW', '/private/tmp/compsci-preview')

TOPICS = {'cs-1-1', 'cs-1-2', 'cs-1-3', 'cs-2-1', 'cs-2-2', 'cs-2-3', 'cs-2-4',
          'cs-2-5', 'cs-3-1', 'cs-3-2', 'cs-3-3', 'cs-3-4'}
UNPRINTED_ANSWER = 'The scheme prints no answer for this part.'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
ROMANS = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']


class LaneError(SystemExit):
    pass


# Private-use glyphs the SEC's symbol fonts leave in the text layer, each read
# by rendering the glyph it draws. Only these are folded; anything else in the
# private-use area still reaches build-deck, which refuses it.
#   U+F0E0  Wingdings 0xE0, a right arrow: "1 -> 3 -> 4 -> 2", 2026 HL scheme
#           p14 (Q14(a)(ii)) and 2023 HL scheme p13 (Q13(b)(i)), both rendered
#           and looked at.
#   U+F0B7  Symbol 0xB7, a bullet: the papers' clue and rule lists (2025 HL
#           Q3, Q9); glyphmap.json already reads it as U+2022.
#   U+F0FC  Wingdings 0xFC, a tick, and U+F04A, Wingdings 0x4A, a smiling
#           face: 2022 OL paper p12 (Q13(b)(i)), rendered at 150 dpi and looked
#           at; folded to U+2713 and U+263A.
LANE_GLYPHS = {'\uf0e0': '\u2192', '\uf0b7': '\u2022', '\uf0fc': '\u2713', '\uf04a': '\u263a'}


def fold(text):
    for k, v in LANE_GLYPHS.items():
        text = text.replace(k, v)
    return text


def ws(text):
    return ' '.join(str(text).split())


def norm(text):
    """build-deck's normalise(): lower case, letters and digits only."""
    t = str(text).lower()
    t = re.sub(r'[‐-―]', '-', t)
    return re.sub(r'[^a-z0-9Ā-ſЀ-ӿ]+', '', t)


# ── what a module writes ────────────────────────────────────────────────────
class Lift:
    """A slice of a printed page, from `start` to `end` inclusive.

    `doc` is '038' (Sections A & B), '040' (Section C) or 'scheme'. `page` is
    the one-based page of that document. Both selectors are matched against
    the page's whitespace-normalised text; `nth` picks the nth occurrence of
    `start` (1-based) where the same words are printed twice on the page.
    """
    def __init__(self, doc, page, start, end=None, nth=1, end_nth=1):
        self.doc, self.page, self.start, self.end, self.nth = doc, page, start, end, nth
        self.end_nth = end_nth

    def __repr__(self):
        return f'Lift({self.doc!r}, {self.page}, {self.start[:30]!r}, {str(self.end)[:30]!r})'


def P(page, start, end=None, nth=1, end_nth=1):
    """A slice of the Sections A & B booklet (-038-)."""
    return Lift('038', page, start, end, nth, end_nth)


def C(page, start, end=None, nth=1, end_nth=1):
    """A slice of the Section C booklet (-040-)."""
    return Lift('040', page, start, end, nth, end_nth)


def S(page, start, end=None, nth=1, end_nth=1):
    """A slice of the marking scheme, as its .md prints it."""
    return Lift('scheme', page, start, end, nth, end_nth)


def T(page, start, end=None, nth=1, end_nth=1):
    """A slice of one scheme page's TABLE CELLS, read column by column (see
    append_cells): a rubric grid the flat text reads across."""
    return Lift('cells', page, start, end, nth, end_nth)


class At:
    """The text printed inside one rectangle of a page, read by position: a
    table cell holding a single character ("e", "R", "?") that no selector
    could pick out of the page's text unambiguously. `rect` is in PDF points,
    measured on the page and opened before use."""
    def __init__(self, doc, page, rect):
        self.doc, self.page, self.rect = doc, page, rect


class Pair:
    """A menu option that names its heading: "Validation examples (x 2) — Range
    check: ...". Both halves are lifted; build-deck traces each half on its own,
    which is how a label beside its value is checked (a scheme heading over a
    list prints the two apart)."""
    def __init__(self, label, value):
        self.label, self.value = label, value


def pt(text, marks, note=None, route=None, head=None):
    return {'kind': 'point', 'text': text, 'marks': marks, 'note': note, 'route': route,
            'head': head}


def allof(text, marks, note=None):
    return {'kind': 'allOf', 'text': text, 'marks': marks, 'note': note}


def crit(text, marks, steps, note=None, head=None, route=None, parts=None):
    """A judgement the scheme prices on printed steps ("Very good ... 3 marks /
    Fair ... 2 marks"). `steps` are the printed marks below the top one."""
    return {'kind': 'criterion', 'text': text, 'marks': marks, 'steps': steps,
            'note': note, 'head': head, 'route': route, 'parts': parts}


def anyn(options, claim, each, head, note=None, open_list=False, steps=None, route=None):
    """A bounded choice: any `claim` of the scheme's `options`, `each` marks
    apiece (or `steps`, a descending ladder the scheme prints)."""
    return {'kind': 'anyN', 'options': options, 'claim': claim, 'each': each,
            'head': head, 'note': note, 'open': open_list, 'steps': steps, 'route': route}


def ask_row():
    """The scheme answers with a drawing and prints no words to claim."""
    return {'kind': 'ask'}


def unprinted(note):
    return {'kind': 'unprinted', 'note': note}


# ── the documents ───────────────────────────────────────────────────────────
class Sitting:
    def __init__(self, year, level):
        self.year, self.level = year, level
        self.docs = {}
        for comp in ('038', '040'):
            path = os.path.join(PAPERS, f'{year}-{level}-{comp}-paper.pdf')
            if os.path.exists(path):
                self.docs[comp] = pymupdf.open(path)
        spath = os.path.join(SCHEMES, f'{year}-{level}.pdf')
        self.docs['scheme'] = pymupdf.open(spath) if os.path.exists(spath) else None
        md = open(os.path.join(SCHEMES, f'{year}-{level}.md'), encoding='utf8').read()
        self.md = md
        flat = md.split(CELLS_START)[0]
        self.md_pages = {}
        for m in re.finditer(r'^## Page (\d+)\n(.*?)(?=^## Page \d+\n|\Z)', flat, re.S | re.M):
            self.md_pages[int(m.group(1))] = ws(fold(m.group(2)))
        self.cell_pages = {}
        for m in re.finditer(r'<!-- compsci:cells page (\d+) -->\n(.*?)(?=<!-- compsci:cells|\Z)',
                             md, re.S):
            self.cell_pages[int(m.group(1))] = ws(m.group(2).replace(CELLS_END, ''))
        self.md_norm = comparable(md)
        self._page_text = {}

    def text(self, doc, page):
        key = (doc, page)
        if key not in self._page_text:
            if doc == 'scheme':
                if page not in self.md_pages:
                    raise LaneError(f'{self.year} {self.level}: scheme .md has no page {page}')
                self._page_text[key] = self.md_pages[page]
            elif doc == 'cells':
                if page not in self.cell_pages:
                    raise LaneError(f'{self.year} {self.level}: no cells read for scheme page '
                                    f'{page}; run cells')
                self._page_text[key] = self.cell_pages[page]
            else:
                d = self.docs.get(doc)
                if d is None:
                    raise LaneError(f'{self.year} {self.level}: no {doc} booklet on disk')
                self._page_text[key] = ws(fold(d[page - 1].get_text()))
        return self._page_text[key]

    def lift(self, item):
        """Resolve a Lift, a list of Lifts (joined by a space), or None."""
        if item is None:
            return None
        if isinstance(item, (list, tuple)):
            return ' '.join(self.lift(i) for i in item)
        if isinstance(item, Pair):
            return f'{self.lift(item.label)} — {self.lift(item.value)}'
        if isinstance(item, At):
            d = self.docs[item.doc]
            out = ws(d[item.page - 1].get_textbox(pymupdf.Rect(*item.rect)))
            if not out:
                raise LaneError(f'{self.year} {self.level} At{item.rect}: nothing printed there')
            return out
        if not isinstance(item, Lift):
            raise LaneError(f'{item!r}: every printed word on a card is lifted (P/C/S), '
                            f'never typed')
        t = self.text(item.doc, item.page)
        start = ws(item.start)
        pos, i = -1, 0
        for _ in range(item.nth):
            pos = t.find(start, i)
            if pos < 0:
                break
            i = pos + 1
        if pos < 0:
            raise LaneError(f'{self.year} {self.level} {item}: start not found on page')
        if item.end is None:
            out = t[pos:pos + len(start)]
        else:
            end = ws(item.end)
            j = t.find(end, pos)
            # the end must close the slice AFTER the start begins
            while j >= 0 and j + len(end) < pos + len(start):
                j = t.find(end, j + 1)
            for _ in range(item.end_nth - 1):
                if j >= 0:
                    j = t.find(end, j + 1)
            if j < 0:
                raise LaneError(f'{self.year} {self.level} {item}: end not found after start')
            out = t[pos:j + len(end)]
        if len(out) > 4000:
            raise LaneError(f'{self.year} {self.level} {item}: slice of {len(out)} chars -- '
                            f'selectors too far apart')
        return out


CELLS_START = '<!-- compsci:cells -->'
CELLS_END = '<!-- /compsci:cells -->'


def append_cells(year, level, pages):
    """Append the table cells of the named scheme pages to the scheme .md.

    A rubric grid -- 2026 HL Q16(b)'s four criteria at three levels -- reads
    ACROSS the page in the flat extraction, so one criterion's items arrive
    interleaved with the other levels' and no card can quote them. find_tables()
    reads the cells whole; they are written COLUMN by column, top to bottom,
    so a criterion's own cells sit together. Append-only, the safety argument
    of append-scheme-tables.py: comparableScheme() joins every line, so a claim
    that traces now still traces after. Only the pages named are read --
    find_tables() over a page of prose returns word fragments, and those are
    not appended anywhere. Re-running replaces the block.
    """
    path = os.path.join(SCHEMES, f'{year}-{level}.md')
    md = open(path, encoding='utf8').read().split(CELLS_START)[0].rstrip('\n') + '\n'
    doc = pymupdf.open(os.path.join(SCHEMES, f'{year}-{level}.pdf'))
    out = [CELLS_START]
    for page in pages:
        out.append(f'<!-- compsci:cells page {page} -->')
        for table in doc[page - 1].find_tables().tables:
            grid = table.extract()
            width = max(len(r) for r in grid)
            for col in range(width):
                for row in grid:
                    cell = ws(row[col] or '') if col < len(row) else ''
                    if cell:
                        out.append(cell)
    out.append(CELLS_END)
    with open(path, 'w', encoding='utf8') as fh:
        fh.write(md + '\n'.join(out) + '\n')
    return len(out)


# build-deck's comparableScheme(), its first form: marks-only and label-only
# lines removed, the rest joined and normalised. A row that is found here is
# found by the build's provenance gate.
MARKS_ONLY = re.compile(r'^\s*\d+\s*(\(\s*\d+\s*\))?\s*$')
LABEL_ONLY = re.compile(r'^\s*\(?\s*([ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s*$', re.I)
LEADING_LABEL = re.compile(r'^\s*\(\s*(?:[ivx]{1,4}|[a-z]|\d{1,2})\s*\)\s+(?=\S)', re.I)


def comparable(md):
    raw = re.sub(r'⟨[^⟩]*⟩', ' ', md)
    raw = re.sub(r'^##\s*Page\s*\d+\s*$', ' ', raw, flags=re.M)
    lines = [l for l in raw.split('\n') if not MARKS_ONLY.match(l) and not LABEL_ONLY.match(l)]
    return [norm(' '.join(lines)),
            norm(' '.join(LEADING_LABEL.sub('', l) for l in lines))]


def traces(sitting, claim):
    c = norm(claim)
    return bool(c) and any(c in form for form in sitting.md_norm)


# ── cards ───────────────────────────────────────────────────────────────────
def part_id(year, level, q, letter=None, roman=None):
    return f'cs-{year}-{level}-q{q}' + (f'-{letter}' if letter else '') + (f'-{roman}' if roman else '')


def part_ref(year, level, q, letter=None, roman=None):
    return f'{year} {level.upper()} Q{q}' + (f'({letter})' if letter else '') + (f'({roman})' if roman else '')


STOP = {'the', 'a', 'an', 'of', 'to', 'and', 'in', 'on', 'for', 'is', 'that', 'this',
        'with', 'be', 'as', 'by', 'your', 'you', 'it', 'its', 'are', 'or', 'from', 'each',
        'any', 'one', 'two', 'three', 'which', 'what', 'how', 'why', 'used', 'below',
        'shown', 'following', 'state', 'explain', 'describe', 'outline', 'name', 'give',
        'identify', 'suggest', 'figure'}


def concept_for(text):
    words = [w for w in re.findall(r'[a-z0-9]+', text.lower()) if w not in STOP]
    return '-'.join(words[:6]) or 'question'


def section_for(q):
    return 'A' if q <= 12 else ('B' if q <= 15 else 'C')


def doc_for(q):
    return '040' if q >= 16 else '038'


def build_row(sitting, spec, i, question_text, where):
    rid = f'r-{i + 1}'
    kind = spec['kind']
    if kind == 'unprinted':
        return {'id': rid, 'kind': 'criterion', 'verbatim': UNPRINTED_ANSWER, 'marks': None,
                'unprinted': True, 'contextNote': sitting.lift(spec['note'])}
    if kind == 'ask':
        return {'id': rid, 'kind': 'point', 'verbatim': question_text, 'marks': None, 'ask': True}
    if kind == 'anyN':
        options = [sitting.lift(o) for o in spec['options']]
        for o in options:
            halves = o.split(' — ')
            if not traces(sitting, o) and not (
                    len(halves) == 2 and all(traces(sitting, h) for h in halves)):
                raise LaneError(f'{where}: option not in the scheme .md: {o[:70]!r}')
        if spec['claim'] > len(options):
            raise LaneError(f'{where}: any {spec["claim"]} of {len(options)} options')
        head = sitting.lift(spec['head'])
        group = {'claimMax': spec['claim'], 'perOption': spec['each'], 'options': options}
        if spec.get('steps'):
            if len(spec['steps']) != spec['claim']:
                raise LaneError(f'{where}: steps must have one value per claim')
            group['perOptionSteps'] = spec['steps']
        row = {'id': rid, 'kind': 'anyN', 'verbatim': head, 'marks': None, 'group': group}
        if spec.get('open'):
            row['openList'] = True
        if spec.get('note'):
            row['contextNote'] = sitting.lift(spec['note'])
        if spec.get('route'):
            row['route'] = spec['route']
        return row
    text = sitting.lift(spec['text'])
    if spec.get('head') is not None:
        text = f"{sitting.lift(spec['head'])} — {text}"
    claim = text.split(' — ')[-1]
    if not traces(sitting, claim):
        raise LaneError(f'{where}: row not in the scheme .md: {text[:70]!r}')
    row = {'id': rid, 'kind': kind, 'verbatim': text, 'marks': spec['marks']}
    if kind == 'criterion' and spec.get('parts'):
        # Named components the scheme prices separately ("Name: 1 mark /
        # Explanation: 5 or 2"), each placed on its own printed steps.
        parts, sums = [], {0}
        for j, (lift, m, st) in enumerate(spec['parts']):
            ladder = [0] + list(st) + [m]
            parts.append({'id': f'p-{j + 1}', 'verbatim': sitting.lift(lift), 'marks': m,
                          'permittedMarks': ladder})
            sums = {a + b for a in sums for b in ladder}
        if sum(p['marks'] for p in parts) != spec['marks']:
            raise LaneError(f'{where}: parts do not add up to the row')
        row['parts'] = parts
        row['permittedMarks'] = sorted(sums)
    elif kind == 'criterion':
        steps = [0] + list(spec['steps']) + [spec['marks']]
        if steps != sorted(set(steps)):
            raise LaneError(f'{where}: criterion steps {steps} are not ascending')
        row['permittedMarks'] = steps
    if spec.get('note'):
        row['contextNote'] = sitting.lift(spec['note'])
    if spec.get('route'):
        row['route'] = spec['route']
    return row


def row_worth(row):
    if row['kind'] == 'anyN':
        g = row['group']
        if g.get('perOptionSteps'):
            return sum(g['perOptionSteps'][:g['claimMax']])
        return g['claimMax'] * g['perOption']
    return row['marks'] or 0


def build_card(sitting, mod, entry, figures):
    year, level = sitting.year, sitting.level
    q, letter, roman = entry['key']
    cid = entry.get('id') or part_id(year, level, q, letter, roman)
    where = f'{year} {level} {cid}'
    if not entry.get('why'):
        raise LaneError(f'{where}: say what the page shows (why=)')
    topic = entry.get('topic')
    if topic not in TOPICS:
        raise LaneError(f'{where}: topic {topic!r} is not a Computer Science topic')
    question = sitting.lift(entry['ask'])
    stem = sitting.lift(entry.get('stem'))
    tariff = entry.get('tariff', 'fixed')
    total = entry['total']
    printed = entry.get('printed')
    if printed is not None:
        page = printed.page if isinstance(printed, Lift) else None
        sitting.lift(printed)              # the tariff cell must be on the page
        if str(total) not in ws(sitting.lift(printed)):
            raise LaneError(f'{where}: total {total} is not in the printed tariff '
                            f'{sitting.lift(printed)!r}')
    else:
        from cs_scheme import CsScheme
        sch = _scheme(year, level)
        read = sch.tariff(q, letter, roman)
        if read != total:
            raise LaneError(f'{where}: the scheme reads {read} marks for this part, the module '
                            f'says {total}; quote the tariff cell with printed=S(...)')
    rows = [build_row(sitting, spec, i, question, where) for i, spec in enumerate(entry['rows'])]
    if tariff == 'questionTotal':
        tariff_model = {'kind': 'questionTotal'}
        for r in rows:
            if r['kind'] != 'anyN':
                r['marks'] = None
    else:
        tariff_model = {'kind': 'fixed'}
        if not any(r.get('unprinted') or r.get('ask') for r in rows):
            common = sum(row_worth(r) for r in rows if not r.get('route'))
            routes = {}
            for r in rows:
                if r.get('route'):
                    routes[r['route']] = routes.get(r['route'], 0) + row_worth(r)
            for name, worth in (routes or {None: 0}).items():
                if common + worth != total:
                    raise LaneError(f'{where}: rows are worth {common + worth}'
                                    f'{" on route " + name if name else ""}, the tariff is {total}')
    if any(r.get('ask') for r in rows) and len(rows) == 1:
        rows[0]['marks'] = total
    if any(r.get('unprinted') for r in rows):
        rows[0]['marks'] = total
    card = {
        'id': cid, 'topicId': topic,
        'conceptId': entry.get('concept') or concept_for(question),
        'level': LEVEL_WORD[level], 'year': year, 'subjectId': SUBJECT,
        'section': section_for(q), 'questionRef': part_ref(year, level, q, letter, roman),
        'questionText': question, 'tariffModel': tariff_model, 'totalMarks': total,
        'rows': rows,
    }
    if stem:
        card['stem'] = stem
    for field, name in (('figureKey', entry.get('figure')),
                        ('questionFigureKey', entry.get('qfigure'))):
        if name:
            key = figure_key(year, level, name)
            if key not in figures:
                raise LaneError(f'{where}: figure {key} is not published -- run crops')
            card[field] = key
    if card.get('questionFigureKey'):
        # The crop is the printed matter beside the ask, never the ask itself:
        # the lifted stem and question stay on the card around it.
        card['questionFigureIncludesPrompt'] = False
    if any(r.get('ask') for r in rows):
        if not card.get('figureKey') or not figures[card['figureKey']].get('solution'):
            raise LaneError(f'{where}: an ask row needs the scheme\'s drawing as a solution figure')
    return card


_SCHEMES = {}


def _scheme(year, level):
    from cs_scheme import CsScheme
    if (year, level) not in _SCHEMES:
        _SCHEMES[(year, level)] = CsScheme(year, level)
    return _SCHEMES[(year, level)]


# ── crops ───────────────────────────────────────────────────────────────────
def figure_key(year, level, name):
    """'q1-code' -> computer-science-2026-HL-paper-q1-code; 's-q3' -> ...-scheme-q3."""
    if name.startswith('s-'):
        return f'{SUBJECT}-{year}-{level.upper()}-scheme-{name[2:]}'
    return f'{SUBJECT}-{year}-{level.upper()}-paper-{name}'


def crop(doc, page, rect, alt, ref, solution=False):
    """One printed region: `doc` '038'/'040'/'scheme', one-based `page`, `rect`
    in PDF points (x0, y0, x1, y1), measured on the page and opened before use."""
    return {'parts': [(doc, page, rect)], 'alt': alt, 'ref': ref, 'solution': solution}


def stack(parts, alt, ref, solution=False):
    """Several printed regions of ONE question, stacked top to bottom in the
    order the paper prints them, with a white gap: a question whose printed
    matter is spread across a page around its answer boxes (2026 HL Q14(a):
    Figure 3 at the top right, Figures 4 and 5 below, the table at the foot)."""
    return {'parts': parts, 'alt': alt, 'ref': ref, 'solution': solution}


GAP = 18


def render_crop(sitting, spec):
    pixes = []
    for doc, pageno, rect in spec['parts']:
        d = sitting.docs['scheme' if doc == 'scheme' else doc]
        page = d[pageno - 1]
        clip = pymupdf.Rect(*rect) & page.rect
        pixes.append(page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), clip=clip, alpha=False))
    if len(pixes) == 1:
        return pixes[0]
    width = max(p.width for p in pixes)
    height = sum(p.height for p in pixes) + GAP * (len(pixes) - 1)
    out = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, width, height), False)
    out.set_rect(out.irect, (255, 255, 255))
    y = 0
    for p in pixes:
        p.set_origin(0, y)
        out.copy(p, p.irect)
        y += p.height + GAP
    return out


def publish_crops(sitting, mod, write=True, only=None):
    figures = json.load(open(FIGURES, encoding='utf8'))
    os.makedirs(FIG_DIR if write else PREVIEW, exist_ok=True)
    out = []
    word = 'Higher' if sitting.level == 'hl' else 'Ordinary'
    for name, spec in getattr(mod, 'CROPS', {}).items():
        if only and name not in only:
            continue
        key = figure_key(sitting.year, sitting.level, name)
        pix = render_crop(sitting, spec)
        path = os.path.join(FIG_DIR, f'{key}.png')
        if write:
            pix.save(path)
            md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
            rec = {
                'src': f'{FIG_SRC}/{key}.png', 'md5': md5, 'alt': spec['alt'],
            }
            if spec.get('solution'):
                rec['solution'] = True
            rec.update({'lettersVisible': [], 'labelMeanings': [],
                        'questionRef': spec['ref'], 'year': sitting.year,
                        'level': LEVEL_WORD[sitting.level],
                        'attribution': f'SEC Leaving Certificate Computer Science {sitting.year} '
                                       f'{word} Level — © State Examinations Commission'})
            figures[key] = rec
        else:
            path = os.path.join(PREVIEW, f'{key}.png')
            pix.save(path)
        out.append((key, path, pix.width, pix.height))
    if write:
        with open(FIGURES, 'w', encoding='utf8') as fh:
            json.dump(figures, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
    return out


# ── modules ─────────────────────────────────────────────────────────────────
def module(year, level):
    name = f'compsci_sittings.y{year}_{level}'
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name == name:
            return None
        raise


def sittings():
    out = []
    pkg = os.path.join(DIR, 'compsci_sittings')
    for f in sorted(os.listdir(pkg)):
        m = re.match(r'^y(\d{4})_(hl|ol)\.py$', f)
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


def build(targets):
    deck = json.load(open(AUTHORED, encoding='utf8'))
    figures = json.load(open(FIGURES, encoding='utf8'))
    lane_ids = set()
    made = []
    for year, level in targets:
        mod = module(year, level)
        if mod is None:
            raise LaneError(f'no module compsci_sittings/y{year}_{level}.py')
        sitting = Sitting(year, level)
        errors = []
        for entry in mod.CARDS:
            try:
                card = build_card(sitting, mod, entry, figures)
            except LaneError as exc:
                errors.append(str(exc))
                continue
            if card['id'] in lane_ids:
                raise LaneError(f'{card["id"]}: two module entries make this card')
            lane_ids.add(card['id'])
            made.append((entry, card))
        if errors:
            raise LaneError('\n'.join(errors))
    owned = _owned()
    by_id = {c['id']: i for i, c in enumerate(deck)}
    for entry, card in made:
        cid = card['id']
        if cid in by_id and cid not in owned and not entry.get('replaces'):
            raise LaneError(f'{cid}: the bank already ships this id; a lane card for it '
                            f'must say replaces= and why')
        if cid in by_id:
            deck[by_id[cid]] = card
        else:
            by_id[cid] = len(deck)
            deck.append(card)
    _record_owned(owned | lane_ids)
    with open(AUTHORED, 'w', encoding='utf8') as fh:
        json.dump(deck, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return [c for _, c in made]


OWNED = os.path.join(DIR, 'compsci_sittings', 'owned.json')


def _owned():
    return set(json.load(open(OWNED))) if os.path.exists(OWNED) else set()


def _record_owned(ids):
    with open(OWNED, 'w') as fh:
        json.dump(sorted(ids), fh, indent=1)
        fh.write('\n')


# ── worksheets ──────────────────────────────────────────────────────────────
def sheet(year, level):
    """Every census leaf of the sitting: open or covered, tariff, reader text."""
    import paper as PP
    import reconcile as R
    from paper_census import census_subject
    census = census_subject(SUBJECT)
    leaves = next(p['leaves'] for p in census['papers']
                  if p['year'] == year and p['level'] == level)
    res = R.reconcile_subject(SUBJECT, census)
    open_labels = set()
    for p in res['papers']:
        if p['year'] == year and p['level'] == level:
            open_labels |= set(p['open'])
    sch = _scheme(year, level)
    paper = PP.Paper(SUBJECT, year, level)
    for leaf in leaves:
        s, q, a, r = leaf['key']
        state = 'OPEN' if leaf['label'] in open_labels else 'cov '
        print(f"{state} {leaf['label']:<24} t={sch.tariff(q, a, r)!s:<4} "
              f"{ws(paper.text(q, a, r) or '')[:100]}")


def lines(year, level, doc, page):
    s = Sitting(year, level)
    d = s.docs[doc]
    p = d[page - 1]
    print(f'page {page}: {p.rect}')
    for b in p.get_text('dict')['blocks']:
        if b.get('type') == 1:
            print(f"  IMAGE {tuple(round(v) for v in b['bbox'])}")
            continue
        for ln in b.get('lines', []):
            t = ''.join(sp['text'] for sp in ln['spans']).strip()
            if t:
                print(f"  {tuple(round(v) for v in ln['bbox'])} {t[:90]}")
    rects = [dr['rect'] for dr in p.get_drawings() if dr['rect'].width > 30 or dr['rect'].height > 30]
    if rects:
        u = rects[0]
        for r in rects[1:]:
            u |= r
        print(f'  DRAWINGS {len(rects)} union {tuple(round(v) for v in u)}')


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == 'sheet':
        sheet(int(argv[2]), argv[3])
    elif cmd == 'lines':
        lines(int(argv[2]), argv[3], argv[4], int(argv[5]))
    elif cmd == 'crops':
        year, level = int(argv[2]), argv[3]
        only = set(argv[4].split(',')) if len(argv) > 4 else None
        mod = module(year, level)
        for key, path, w, h in publish_crops(Sitting(year, level), mod, only=only):
            print(f'{key} {w}x{h} {path}')
    elif cmd == 'preview':
        year, level = int(argv[2]), argv[3]
        only = set(argv[4].split(',')) if len(argv) > 4 else None
        mod = module(year, level)
        for key, path, w, h in publish_crops(Sitting(year, level), mod, write=False, only=only):
            print(f'{key} {w}x{h} {path}')
    elif cmd == 'cells':
        n = append_cells(int(argv[2]), argv[3], [int(x) for x in argv[4].split(',')])
        print(f'{n} lines in the cells block')
    elif cmd == 'build':
        targets = sittings() if argv[2] == 'all' else [(int(argv[2]), argv[3])]
        cards = build(targets)
        print(f'{len(cards)} lane card(s) written for {targets}')
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    # Run through the importable module, so the Lift class the sitting modules
    # build their entries from is the one this code checks against.
    import compsci_lane
    sys.exit(compsci_lane.main(sys.argv))
