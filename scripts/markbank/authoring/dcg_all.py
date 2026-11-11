#!/usr/bin/env python3
"""Author every Design & Communication Graphics part the scheme prices.

    python3 scripts/markbank/authoring/dcg_all.py --report   # counts, refusals
    python3 scripts/markbank/authoring/dcg_all.py --write    # authored/dcg.json

--write, never a shell redirect: the generator reads the shipped file for the
cards edited by hand after generation (SHIPPED_EDITS), and `> dcg.json`
empties that file before the script can read it.

WHAT A DCG CARD IS. The scheme prices one drawing as a numbered sequence of
CONSTRUCTION STEPS, each with its own mark:

    (b) Dihedral Angle between surfaces A and B                          (20)
      (iii) X1Y1 parallel to line of intersection ......................... 6
      (iv)  Projection of planes and line of intersection on new X1Y1 ..... 4
      (v)   New X2Y2 perpendicular to line of intersection ................ 5
      (vi)  Projection of planes as lines and indicating dihedral angle ... 5

So a card is the priced unit, its rows are those steps at those marks, and the
shape is Applied Maths': ONE bounded row holding the whole ordered sequence, so
a student ticks the steps they actually drew. Nothing is apportioned and
nothing is averaged -- every number on a card is printed in the scheme, and
`dcg_scheme` has already checked that the steps sum to the part and the parts
sum to the question's own "Total =".

WHAT THE PAIRING RESTS ON (Law 4). The paper and the scheme agree on the
QUESTION -- both print "B-2", "C-4" -- and that is the only join taken for
free. Below it the scheme numbers its own way: 2021 Ordinary B-3 prices the
paper's part (b) as two unlettered heads and then letters the paper's part (c)
"(b)". So a unit is paired to the paper's ask by an order-preserving alignment
scored on the WORDS the two documents share, with the letter used to confirm
rather than to decide. `--report` prints, per sitting, how many pairings were
confirmed by wording, how many by the letter alone, how many were forced (one
ask, or one unit), and how many rested on order alone -- those are refused.

REFUSALS are named buckets, counted with a real example by `--report`.
"""
import argparse
import collections
import functools
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(DIR)))

import cardlint                                              # noqa: E402
import dcg_paper as DP                                       # noqa: E402
import dcg_topics as DT                                      # noqa: E402
import paper_census as PC                                    # noqa: E402
from dcg_scheme import (CUE_FLOOR, DcgScheme, cue_score,     # noqa: E402
                        has_scheme)

SUBJECT = 'dcg'
LEVEL_WORD = {'hl': 'higher', 'ol': 'ordinary'}
LEVEL_TOKEN = {'higher': 'hl', 'ordinary': 'ol'}
# The sittings this deck cards. The census reads every sitting on disk,
# 2010-2026; the deck grows a sitting at a time, each admitted here once its
# cards, crops, paper link and Atlas question have been checked. A sitting not
# yet admitted shows in the ledger as OPEN instead of vanishing behind a window.
CARDED = ({(year, level) for year in range(2019, 2027) for level in ('hl', 'ol')}
          | {(2018, 'hl'), (2018, 'ol')})

# Cards edited by hand after generation, kept exactly as shipped. None since
# November 2026: #294 had cut 2023 Ordinary B-3(c) into its four priced lines
# by hand, with "elevation (2) and plan (2)" as parts, and step_row() now
# builds exactly that from the scheme for every card.
SHIPPED_EDITS = ()
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', f'{SUBJECT}.json')

# The Topic Atlas files every printed question under the syllabus headings it
# was verified against, question by question. A card must sit under a topic its
# own Atlas question carries, or a student browsing that topic finds the
# question and not the card. A card whose classified topic is not one of its
# question's Atlas topics takes the question's primary Atlas topic: 2018
# Higher B-3(c) classified as Rotation for the words "true length", inside a
# question the Atlas files, rightly, under Intersecting Planes. Applied to every
# sitting since November 2026, when it moved 77 of the 2019-2026 cards.
ATLAS_TAGS = os.path.join(ROOT, 'scripts', 'paper-trail', 'topic-tags', 'tags',
                          'design-and-communication-graphics.json')


@functools.lru_cache(maxsize=None)
def atlas_topics():
    """{(year, level word, paperKey, n): [primary, secondary...]} for EV papers."""
    with open(ATLAS_TAGS, encoding='utf-8') as fh:
        tags = json.load(fh)
    out = {}
    for paper in tags:
        if paper['lang'] != 'ev':
            continue
        for q in paper['q']:
            out[(paper['year'], paper['level'], paper['paperKey'], q['n'])] = \
                [q['primary']] + ([q['secondary']] if q.get('secondary') else [])
    return out


def atlas_address(section, q):
    """The Atlas's (paperKey, n) for a printed question: Section A is its own
    booklet, numbered 1-4; Sections B and C share one, numbered 1-8."""
    if section == 'A':
        return 'section-a', str(q)
    return 'single', str(q if section == 'B' else q + 3)

# MAX_LONG_OPTION_ROWS in types/markBank.ts: the most options any one bounded
# row may show. A unit longer than this is split by the scheme's OWN named
# groups, which is the only division of it the SEC printed.
MAX_STEPS_SHOWN = 16
# MAX_ROWS in types/markBank.ts: the most REQUIRED rows a fixed-tariff card may
# carry. test/markBankDeck.test.ts enforces it, with a debt list it says never
# to grow.
MAX_ROWS = 6

# ------------------------------------------------------------------ pairing
def pair(units, leaves, texts):
    """[(unit, [leaf keys])] — the scheme's units against the paper's asks.

    Where BOTH documents letter the same parts in the same order -- 339 of the
    corpus's 396 questions -- the letters are two documents agreeing on the
    address, and that is the pairing. Nothing is inferred and nothing can
    drift: 2025 Ordinary A-2 letters "Locate points", "Draw curve" and "Focal
    points" against asks that letter (a), (b), (c), and scored on wording
    alone the first unit's words fit the THIRD ask just as well as its own.

    Where they do not agree, an order-preserving alignment scored on the words
    the two documents share: a unit may cover several asks, several units may
    divide one ask, but neither document's order is ever crossed.
    """
    m, n = len(units), len(leaves)
    if not m or not n:
        return []
    paper_letters = []
    for key in leaves:
        if key[2] and key[2] not in paper_letters:
            paper_letters.append(key[2])
    if m == len(paper_letters) and [u.letter for u in units] == paper_letters:
        return [(u, [k for k in leaves if k[2] == u.letter]) for u in units]

    # Every pairing the alignment makes has to PAY for itself. Scored on the
    # wording alone, spreading one unit over two asks always scores more than
    # placing it on one, because it adds another term -- 2025 Ordinary C-2's
    # "End view of Hyperbolic Paraboloid" was paired with the paper's (b) AND
    # its (c) for exactly that reason. So each pairing is charged CUE_FLOOR,
    # the same bar a pairing has to clear to count as confirmed at all, and a
    # pairing that does not clear it makes the alignment worse rather than
    # better. The LETTER is deliberately not scored here: this alignment only
    # runs where the two documents letter DIFFERENTLY, and there the scheme's
    # letter is the thing that is wrong.
    def fit(i, j):
        return cue_score(units[i].title, texts.get(leaves[j], '')) - CUE_FLOOR

    @functools.lru_cache(maxsize=None)
    def best(i, j):
        if i == m - 1:
            return sum(fit(i, k) for k in range(j, n)), 'down'
        if j == n - 1:
            return sum(fit(k, j) for k in range(i, m)), 'right'
        here = fit(i, j)
        # Ties are the rule rather than the exception here -- a unit that
        # matches nothing scores zero against every ask -- so the tie-break is
        # stated rather than left to whichever label sorts first. Advancing
        # BOTH is preferred: it is the reading where the two documents divide
        # the question the same way, which is what they do in 339 of the
        # corpus's 396 questions. Picked by string order instead, the 2025
        # Ordinary A-2 scheme's "Draw curve" was paired with "Locate the focal
        # points".
        options = [
            (here + best(i + 1, j + 1)[0], 2, 'diag'),
            (here + best(i + 1, j)[0], 1, 'right'),
            (here + best(i, j + 1)[0], 0, 'down'),
        ]
        value, _rank, move = max(options)
        return value, move

    out = collections.defaultdict(list)
    i = j = 0
    while True:
        out[i].append(leaves[j])
        if i == m - 1 and j == n - 1:
            break
        if i == m - 1:
            j += 1
            continue
        if j == n - 1:
            i += 1
            continue
        move = best(i, j)[1]
        if move == 'diag':
            i, j = i + 1, j + 1
        elif move == 'right':
            i += 1
        else:
            j += 1
    return [(units[k], out[k]) for k in range(m)]


# --------------------------------------------------------------- citations
def ref_for(year, level, section, q, covered, all_leaves):
    """The paper's own address for what one card holds."""
    head = f'{year} {level.upper()} Section {section} Q{q}'
    siblings = [k for k in all_leaves if k[0] == section and k[1] == q]
    if len(covered) == len(siblings):
        return head
    letters = []
    for key in covered:
        if key[2] and key[2] not in letters:
            letters.append(key[2])
    if not letters:
        return head
    if len(letters) > 1:
        return head + '(' + ')('.join(letters[:1]) + ')' + ''.join(
            f', ({x})' for x in letters[1:])
    letter = letters[0]
    under = [k for k in siblings if k[2] == letter]
    romans = [k[3] for k in covered if k[3]]
    if len(covered) == len(under) or not romans:
        return f'{head}({letter})'
    return (f'{head}({letter})(' + romans[0] + ')'
            + ''.join(f', ({r})' for r in romans[1:]))


# The parts list an assembly question prints beside its drawing. It is a
# TABLE -- "Part | Name | Qty." over ten rows -- and the text layer hands it
# back as one run of column cells: "Part Name Qty. Sliding Plunger End Cutter
# End Cap Handle Link Arm". The crop carries the table as the SEC set it; on
# the card it is a wall of two-word fragments after the ask has finished.
PARTS_LIST = re.compile(r'\s*\bPart\s+Name\s+Qty\.?.*$', re.I | re.S)


def _squash(text):
    return re.sub(r'[^a-z0-9]+', '', (text or '').lower())


def ask_text(covered, texts, parent):
    """The paper's own wording for every ask one card covers, in order."""
    parts = []
    for key in covered:
        text = ' '.join((texts.get(key) or '').split())
        if not text:
            continue
        parts.append(f'({key[3]}) {text}' if key[3] and len(covered) > 1
                     else text)
    joined = ' '.join(parts).strip()
    if not joined:
        joined = ' '.join((parent or '').split())
    return PARTS_LIST.sub('', joined).strip()


def parent_words(P, section, q, covered):
    """The lettered parts' own words, for a card that covers romans under them.

    A letter that opens romans often states the data the romans work from:
    2018 Higher C-4(a) describes the mechanism there -- "Crank OA, which is
    48mm long ... AB and CB are both 110mm long" -- and its romans only say
    what to draw, so a card without the letter's words asks for the locus of
    a mechanism it never described. Lifted into the card's STEM, in order, once
    per letter. 26 cards needed it in November 2026.
    """
    out = []
    for letter in dict.fromkeys(k[2] for k in covered if k[2] and k[3]):
        own = ' '.join((P.parent_text(section, q, letter) or '').split())
        if own:
            out.append(own)
    return out


def card_id(year, level, section, q, covered, ordinal, many):
    letters = sorted({k[2] for k in covered if k[2]})
    tail = letters[0] if len(letters) == 1 else ''
    romans = sorted({k[3] for k in covered if k[3]})
    if len(romans) == 1 and len(letters) <= 1:
        tail += romans[0]
    base = f'dcg-{year}-{level}-{section.lower()}{q}{tail}'
    return f'{base}-{ordinal}' if many else base


# -------------------------------------------------------------------- rows
# A step the scheme prices in parts, inside its own words. Three printed forms,
# and nothing else is read as a price: "(2,2,2)" (and "(1, 2, 1)", "(3x1,2)",
# "(4 or 1,1,1,1)"), "(4×1)", and "(Any = 1)" -- any curve earns 1, the
# correct one the step's full marks. "(3 lines)" and "(12 min.)" are not
# prices: a token that is not a number or a count of marks refuses the whole.
SUB_PRICE = re.compile(r'\(([^()]*\d[^()]*)\)')
ANY_PRICE = re.compile(r'^\s*any\s*=?\s*(\d{1,2})\s*$', re.I)
COUNT = re.compile(r'^(\d{1,2})\s*[x×X]\s*(\d{1,2})$')
# "Projections from elevation (2) and plan (2)": the step names its parts.
NAMED_PRICE = re.compile(r"([A-Za-z][A-Za-z'’ -]*?)\s*\((\d{1,2})\)")


def _subset_sums(values):
    sums = {0}
    for v in values:
        sums |= {s + v for s in sums}
    return sums


def sub_ladder(text, marks):
    """The marks a step can earn at the values printed inside it, or None.

    Every reachable total of the printed parts and nothing between them: a
    step priced "(2,2,2)" earns 0, 2, 4 or 6, never 3. Refused, and left a
    single claim, wherever the printed parts do not add up to the step's own
    printed mark -- 2024 Higher A-4 prints "(1,2)" against a 2-mark step.
    """
    for m in reversed(SUB_PRICE.findall(text)):
        inner = m.strip()
        a = ANY_PRICE.match(inner)
        if a:
            k = int(a.group(1))
            return [0, k, marks] if 0 < k < marks else None
        reach = set()
        for route in re.split(r'\s+or\s+', inner):
            values = []
            for token in re.split(r'\s*[,&+]\s*', route.strip()):
                c = COUNT.match(token)
                if c:
                    values += [int(c.group(2))] * int(c.group(1))
                elif token.isdigit():
                    values.append(int(token))
                else:
                    return None
            if sum(values) != marks:
                return None
            reach |= _subset_sums(values)
        return sorted(reach) if len(reach) > 2 else None
    return None


def named_parts(text, marks):
    """[(name, marks)] where the step prices its own named parts, or None."""
    found = NAMED_PRICE.findall(text)
    if len(found) < 2 or sum(int(n) for _w, n in found) != marks:
        return None
    return [(w.split()[-1], int(n)) for w, n in found]


# A step that names another step by its roman: "Draw plan of horizontal section
# (identified at (xi)) on AEFG", "Use of points established at (xii) & (xiii)".
CITES_ROMAN = re.compile(r'\((?:x{0,2}(?:ix|iv|v?i{0,3}))\)')


def numbered(steps):
    """Do this unit's steps need the scheme's own romans to be told apart?

    Where a step cites another by its roman, or the scheme prints the same step
    twice under no heading (2017 Higher C-4(b) prints "Draw required locus" as
    (xv) and (xix), once per 60° movement), a step's words alone cannot say
    which one it is. The roman is printed beside every step in the scheme, so
    it is lifted with the step's words, and only in such units.
    """
    texts = [s.text for s in steps]
    return (len(set(texts)) != len(texts)
            or any(CITES_ROMAN.search(t.replace('()', '')) for t in texts))


def shown(step, with_roman):
    return f'({step.roman}) {step.text}' if with_roman else step.text


def step_row(row_id, step, with_roman=False):
    """One step as a claim row: a point, or stepped where the step prints parts."""
    named = named_parts(step.text, step.marks)
    if named:
        return {'id': row_id, 'kind': 'criterion', 'verbatim': shown(step, with_roman),
                'marks': step.marks, 'permittedMarks': [0, step.marks],
                'parts': [{'id': name.lower(), 'verbatim': name, 'marks': n,
                           'permittedMarks': [0, n]} for name, n in named]}
    ladder = sub_ladder(step.text, step.marks)
    if ladder:
        return {'id': row_id, 'kind': 'criterion',
                'verbatim': shown(step, with_roman),
                'marks': step.marks, 'permittedMarks': ladder}
    return {'id': row_id, 'kind': 'point', 'verbatim': shown(step, with_roman),
            'marks': step.marks}


def step_ladder(step):
    """A step's own steps when it is one PART of a long unit's row."""
    named = named_parts(step.text, step.marks)
    if named:
        return sorted(_subset_sums([n for _w, n in named]))
    return sub_ladder(step.text, step.marks) or [0, step.marks]


PRESENTATION = re.compile(r'^Presentation\b', re.I)
PRESENTATION_NOTE = ('The scheme prices Presentation on the whole question, '
                     'not on one part: claim it once, here, for the finished '
                     'drawing.')


def step_rows(card_id, title, steps, extra=()):
    """The scheme's priced steps as claim rows, each at its own printed marks.

    A DCG drawing is priced as a run of construction steps, every one of them
    REQUIRED and each worth its own printed mark. They were carried as one
    anyN group ("All 3 of these -- 1 then 2 then 5 marks"), and an anyN group
    pays by HOW MANY options are ticked, in the order the marks are listed:
    ticking only dcg-2019-hl-a1b's 5-mark step scored 1. A step is a point the
    student either drew or did not, so it is a row of its own, claimed on its
    own, scored at its own price.

    Up to MAX_ROWS steps, one point row per step. Past it -- 57 of the deck's
    units price seven to sixteen steps -- one criterion row whose PARTS are the
    steps, each awarded on its own at 0 or its printed marks: the model
    Construction Studies prices its named components in, and the same claim,
    since a part scores what is placed on it and nothing else.
    """
    tail = [{'id': '', 'kind': 'point', 'verbatim': s.text, 'marks': s.marks,
             'contextNote': PRESENTATION_NOTE} for s in extra]
    with_roman = numbered(steps)
    if len(steps) + len(tail) <= MAX_ROWS:
        rows = [step_row(f'{card_id}-r{i}', s, with_roman)
                for i, s in enumerate(steps, 1)]
    else:
        rows = [_parts_row(card_id, title, steps, with_roman)]
    for row in tail:
        row['id'] = f'{card_id}-r{len(rows) + 1}'
        rows.append(row)
    return rows


def _parts_row(card_id, title, steps, with_roman=False):
    total = sum(s.marks for s in steps)
    return {
        'id': f'{card_id}-r1', 'kind': 'criterion', 'verbatim': title,
        'marks': total, 'permittedMarks': [0, total],
        'contextNote': 'The scheme prices this drawing step by step: award '
                       'each step you drew its own marks.',
        'parts': [{'id': f'step-{i}', 'verbatim': shown(s, with_roman),
                   'marks': s.marks,
                   'permittedMarks': step_ladder(s)}
                  for i, s in enumerate(steps, 1)],
    }


# ------------------------------------------------------------ source material
# Section C's Geologic Geometry question is answered ON a contour map that the
# SEC prints on the back page of the SECTION A booklet, not with the question:
# "This Contour Map is part of Section C and should only be used for the
# answering of the Geologic Geometry Option". The question crop cannot show
# it, so every C-1 card carries that page as source material, opened in the
# official page reader from the Section A booklet (resolved by build-deck from
# its Paper Trail label, never typed).
# Matched across the line breaks and double spaces some years print in it.
CONTOUR_CAPTION = re.compile(r'This\s+Contour\s+Map\s+is\s+part\s+of\s+Section\s+C', re.I)


# The map is printed SIDEWAYS: its caption runs down a portrait page, and the
# reader turns the page by this much, clockwise, to set it upright. Read from
# the caption's own text direction, less any /Rotate the page already carries
# (2013's booklets set /Rotate 270 and need nothing more).
UPRIGHT = {(0, 1): 270, (0, -1): 90, (1, 0): 0, (-1, 0): 180}


@functools.lru_cache(maxsize=None)
def contour_map_page(year, level):
    """(one-based page, clockwise turn) of the contour map in the Section A
    booklet, or None."""
    import pymupdf
    P = DP.load(year, level, SUBJECT)
    for path in P.files:
        with pymupdf.open(path) as doc:
            prints_a = any(DP.QHEAD.match(r[3]) and r[3].startswith('A')
                           for page in doc for r in DP.rows(page))
            if not prints_a:
                continue
            pages = [i for i, page in enumerate(doc)
                     if CONTOUR_CAPTION.search(page.get_text())]
            if len(pages) != 1:
                continue
            page = doc[pages[0]]
            dirs = {tuple(round(v) for v in line['dir'])
                    for block in page.get_text('dict')['blocks']
                    for line in block.get('lines', [])
                    if CONTOUR_CAPTION.search(' '.join(
                        ''.join(sp['text'] for sp in line['spans']).split())
                        + ' is part of Section C')
                    or 'Contour Map' in ''.join(sp['text'] for sp in line['spans'])}
            if len(dirs) != 1 or next(iter(dirs)) not in UPRIGHT:
                return None
            return pages[0] + 1, (UPRIGHT[next(iter(dirs))] - page.rotation) % 360
    return None


def contour_map(year, level):
    found = contour_map_page(year, level)
    if found is None:
        return None
    page, turn = found
    word = 'Higher' if level == 'hl' else 'Ordinary'
    return {
        'kind': 'source-illustration',
        'label': 'Contour Map',
        'title': 'The contour map for Question C-1, on the back page of the '
                 'Section A booklet',
        'pages': [page],
        **({'pageRotations': {str(page): turn}} if turn else {}),
        'sourceLabel': 'Section A',
        'attribution': f'SEC Leaving Certificate Design and Communication '
                       f'Graphics {year} {word} Level, Section A — © State '
                       f'Examinations Commission.',
        'presentationNote': 'The back page of the Section A booklet, exactly '
                            'as it was printed for the examination.',
    }


# ----------------------------------------------------------------- figures
def figure_index():
    """The inspected question crops, keyed by the question they were cut FOR.

    One crop per QUESTION: the SEC prints the drawing once and every part of
    that question is answered from it. Read from the manifest a figure pass
    wrote, so a crop nobody has looked at is not in here to be bound.
    """
    figs = {}
    for name in ('figures.json', f'figures-{SUBJECT}.json'):
        path = os.path.join(ROOT, 'components', 'MarkBank', name)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8') as fh:
            manifest = json.load(fh)
        for key in manifest:
            m = re.fullmatch(r'dcg-(\d{4})-(HL|OL)-paper-sec([ABC])'
                             r'-q(\d)-art', key)
            if m:
                figs[(int(m.group(1)), m.group(2).lower(), m.group(3),
                      int(m.group(4)))] = key
    return figs


# ------------------------------------------------------------------ author
def repeats(unit):
    """Does this unit print the same step twice?

    The earthworks questions do, and so does every interpenetration priced by
    side: 2022 Ordinary B-2(b) prices "Projection from elevation", "Locate
    points in plan" and "Complete the plan" once for the ramp and again for
    the front cut. On one card that is three pairs of identical rows and a
    student cannot tell which is which -- but the SEC prints a HEADING over
    each set ("Interpenetration into ramp", "Front ramp cut"), so the card is
    cut where the scheme cut it instead.
    """
    texts = [s.text for s in unit.steps]
    return len(set(texts)) != len(texts)


def split_by_groups(unit):
    """A unit cut where the SEC's own headings cut it.

    Two units reach this. The assembly drawings are past the display cap --
    2021 Higher C-5 prices one sectional elevation in eighteen steps, under
    eight named component headings each carrying its own printed mark, "Main
    Body (14)", "Clamping Jaw (8)". And the earthworks and interpenetration
    questions price the SAME step once per section of the course, under a
    heading naming the section: "Earthworks between A and B (Level) –
    Embankment", "... – Cutting".

    The headings are the SEC's and so are the marks; where the heading carries
    no printed mark of its own the piece is worth the sum of the steps printed
    under it, which is arithmetic on printed numbers and not a tariff invented
    for it. Returns [(label, marks, [steps])] or None where there is nothing
    printed to split on.
    """
    groups = []
    for step in unit.steps:
        # A step printed before the unit's first heading belongs to the whole
        # unit, not to either section of it: 2016 Higher C-1(a) opens with
        # "(i) Measure required 10mm distances perp. to pool edge" above its
        # Embankment and Cutting headings. It is a piece of its own, under the
        # unit's own printed title. After a heading, an unheaded step still
        # refuses: nothing printed says where it belongs.
        if not step.group:
            if groups and groups[-1][0] != unit.title:
                return None
            if not groups:
                groups.append((unit.title, []))
            groups[-1][1].append(step)
            continue
        if not groups or groups[-1][0] != step.group:
            groups.append((step.group, []))
        groups[-1][1].append(step)
    if len(groups) < 2:
        return None
    out = []
    for label, steps in groups:
        if len(steps) > MAX_STEPS_SHOWN:
            return None
        out.append((label, sum(s.marks for s in steps), steps))
    return out


def author(bind_figures=True):
    census = PC.census_subject(SUBJECT)
    figures = figure_index() if bind_figures else {}
    cards, refused, examples = [], collections.Counter(), collections.defaultdict(list)
    verdicts, stats = [], []

    for paper in census['papers']:
        year, level = paper['year'], paper['level']
        if (year, level) not in CARDED:
            refused['this sitting is censused and not yet carded'] += \
                paper['leafCount']
            continue
        P = DP.load(year, level, SUBJECT)
        leaves = {tuple(leaf['key']) for leaf in paper['leaves']}
        texts = {ask.key: ask.full_text for ask in P.asks()}
        assert set(texts) == leaves, \
            f'{year} {level}: the authored leaf set is not the census leaf set'
        if not has_scheme(year, level, SUBJECT):
            for key in sorted(leaves):
                refused['no marking scheme is published for this sitting'] += 1
            continue
        S = DcgScheme(year, level, SUBJECT)
        wording = letter_only = forced = order_only = 0

        for qkey in sorted(P.questions):
            section, q = qkey
            qq = P.questions[qkey]
            unit_list = S.questions[qkey].units if qkey in S.questions else []
            mine = sorted(k for k in leaves if k[0] == section and k[1] == q)

            # A step the scheme prices on the QUESTION rather than on any of
            # its parts. Every Ordinary question ends with one -- a
            # presentation mark for the finished drawing, printed as the next
            # roman in the run after the last part's last step. There is no
            # ask on the paper to price it against, so it is not folded into
            # any part's tariff: it is its own row on the question's first
            # card, saying so (PRESENTATION_NOTE), and that card's total grows
            # by exactly the printed mark, so the question's cards add up to
            # the question.
            # Presentation is the one such step every Ordinary question prints,
            # and it is a printed price, so it is claimable: a row on the
            # question's FIRST card, saying the scheme prices it on the whole
            # question. Any other question-level step stays a named refusal.
            presentation = [step for step in (
                S.questions[qkey].trailer if qkey in S.questions else [])
                if PRESENTATION.match(step.text)]
            for step in (S.questions[qkey].trailer if qkey in S.questions
                         else []):
                if step in presentation:
                    continue
                reason = ('the scheme prices this step on the QUESTION, '
                          'under no part the paper asks')
                refused[reason] += 1
                if len(examples[reason]) < 80:
                    examples[reason].append(
                        f'{year} {level.upper()} {section}-{q}: '
                        f'({step.roman}) {step.text} = {step.marks}')
            if not unit_list:
                for key in mine:
                    ref = ref_for(year, level, section, q, [key], leaves)
                    refused['the scheme prices nothing under this question'] += 1
                    examples['the scheme prices nothing under this question'] \
                        .append(f'{ref}')
                continue
            pairing = pair(unit_list, mine, texts)
            per_address = collections.Counter(
                tuple(cov) for _u, cov in pairing)
            ordinal = collections.Counter()
            # Two units covering DIFFERENT spans of one question can still
            # land on the same id: a span crossing two letters is keyed by the
            # question alone. Counted over the whole question, so the suffix
            # is decided by how many cards the question makes and not by how
            # many share one address.
            bases = collections.Counter(
                card_id(year, level, section, q, cov, 1, False)
                for _u, cov in pairing)

            question_carded = False
            for index, (unit, covered) in enumerate(pairing, 1):
                ref = ref_for(year, level, section, q, covered, leaves)
                base = card_id(year, level, section, q, covered, 1, False)
                many = per_address[tuple(covered)] > 1
                ordinal[base] += 1
                cid = card_id(year, level, section, q, covered,
                              ordinal[base], bases[base] > 1)

                def note(reason, detail=''):
                    verdicts.append({'year': year, 'level': level, 'ref': ref,
                                     'reason': reason})
                    refused[reason] += 1
                    if len(examples[reason]) < 80:
                        examples[reason].append(f'{ref}: {detail[:80]}')

                # --- Law 4: how was this unit paired to the paper's ask?
                score = max(cue_score(unit.title, texts.get(k, ''))
                            for k in covered)
                if len(unit_list) == 1 or len(mine) == 1:
                    forced += 1
                elif score >= CUE_FLOOR:
                    wording += 1
                elif unit.letter and any(unit.letter == k[2] for k in covered):
                    letter_only += 1
                else:
                    order_only += 1
                    note('the pairing of this priced unit to a printed ask '
                         'rests on order alone', unit.title)
                    continue

                if not unit.steps:
                    note('the scheme prices this unit but states no step '
                         'under it', unit.title)
                    continue
                if not unit.marks:
                    note('the scheme prints no tariff for this unit',
                         unit.title)
                    continue

                question = ask_text(covered, texts,
                                    P.parent_text(section, q, covered[0][2]))
                if len(question) < 12:
                    note('the paper prints no ask at this address', unit.title)
                    continue

                pieces = [(None, unit.marks, unit.steps)]
                if len(unit.steps) > MAX_STEPS_SHOWN or repeats(unit):
                    split = split_by_groups(unit)
                    # A step printed twice under no heading at all is told
                    # apart by its roman, which step_rows then shows.
                    if not split and len(unit.steps) <= MAX_STEPS_SHOWN \
                            and numbered(unit.steps):
                        split = pieces
                    if not split:
                        note('the scheme states the same priced step twice, '
                             'or more than '
                             f'{MAX_STEPS_SHOWN} steps, and names no groups '
                             'to split them by', unit.title)
                        continue
                    pieces = split

                stem = ' '.join([' '.join((qq['stem'] or '').split())]
                                + parent_words(P, section, q, covered)).strip()
                # A question the paper asks WHOLE has no ask of its own: its
                # leaf text IS the stem, so the card would print the same
                # paragraph twice, once above the other.
                if stem and _squash(stem) in _squash(question):
                    stem = ''
                topic, why = DT.topic_for(section, qq['option'],
                                          ' '.join([stem, question, unit.title]
                                                   + [s.text for s in unit.steps]))
                if topic is None:
                    note('files under no syllabus heading', why)
                    continue
                tags = atlas_topics().get(
                    (year, LEVEL_WORD[level]) + atlas_address(section, q))
                if not tags:
                    note('the Topic Atlas lists no question at this '
                         'address', ref)
                    continue
                if topic not in tags:
                    topic = tags[0]
                figure = figures.get((year, level, section, q))
                if cardlint.NAMES_LETTERS.search(f'{stem} {question}') \
                        and not cardlint.INVITES_DRAWING.search(question):
                    note('names a lettered part this author cannot decode',
                         question)
                    continue
                if cardlint.SCHEME_LEAK.search(f'{stem} {question}'):
                    note('the paper text carries scheme metadata', question)
                    continue

                for piece_no, (label, marks, steps) in enumerate(pieces, 1):
                    options = [s.text for s in steps]
                    step_marks = [s.marks for s in steps]
                    if sum(step_marks) != marks:
                        note('the priced steps do not sum to the mark the '
                             'scheme prints for this unit', unit.title)
                        continue
                    if any(not o for o in options):
                        note('the scheme states no words for one of the '
                             'priced steps', unit.title)
                        continue
                    piece_ref = ref
                    piece_id = cid
                    title = label or unit.title
                    if label or many:
                        piece_ref = f'{ref} — {title}'
                    if label:
                        piece_id = f'{cid}-{piece_no}'
                    extra = presentation if not question_carded else []
                    question_carded = True
                    rows = step_rows(piece_id, title, steps, extra)
                    marks += sum(s.marks for s in extra)
                    cards.append({
                        'id': piece_id,
                        'topicId': topic,
                        'conceptId': DT.concept_for(topic),
                        'level': LEVEL_WORD[level],
                        'year': year,
                        'subjectId': SUBJECT,
                        'section': section,
                        'questionRef': piece_ref,
                        'questionText': question,
                        'stem': stem,
                        'figureKey': '',
                        'questionFigureKey': figure or '',
                        'labelKey': [],
                        'tariffModel': {'kind': 'fixed',
                                        'notation': f'({marks})'},
                        'totalMarks': marks,
                        'rows': rows,
                        **({'sourceMaterial': contour_map(year, level)}
                           if section == 'C' and qq['option'] == 'Geologic Geometry'
                           and contour_map(year, level) else {}),
                        'notes': (f'The scheme heads this {title!r} and prices '
                                  f'it at {marks - sum(s.marks for s in extra)}. '
                                  'Construction lines must be shown on all '
                                  'solutions, and the scheme notes that other '
                                  'valid solutions are acceptable and are '
                                  'marked accordingly.'),
                    })
        stats.append((year, level, wording, letter_only, forced, order_only))

    return cards, refused, examples, verdicts, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--verdicts')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    cards, refused, examples, verdicts, stats = author()

    if args.verdicts:
        with open(args.verdicts, 'w', encoding='utf-8') as fh:
            json.dump(verdicts, fh, indent=1)
        print(f'wrote {args.verdicts}: {len(verdicts)} refusals')
    if args.report:
        census = PC.census_subject(SUBJECT)
        total = sum(p['leafCount'] for p in census['papers'])
        print(f'{len(cards)} card(s) against {total} census asks')
        print()
        print("PAIRING (Law 4): how each sitting's priced units were joined")
        for year, level, w, lo, f, oo in stats:
            n = w + lo + f + oo
            print(f'  {year} {level.upper()}: {w:3} confirmed by wording, '
                  f'{lo:3} by the letter alone, {f:3} forced (one ask or one '
                  f'unit), {oo:3} refused for resting on order alone'
                  f'   [{100 * (w + f) // max(n, 1)}%]')
        print()
        for reason, n in refused.most_common():
            print(f'  {n:4} REFUSED  {reason}')
            for e in examples[reason][:80 if args.all else 3]:
                print(f'            {e}')
        return 0
    with open(AUTHORED, encoding='utf-8') as fh:
        text = fh.read()
    if not text.strip():
        raise SystemExit(f'{AUTHORED} is empty: run with --write, not a shell '
                         'redirect, which empties the file before it is read')
    shipped = {c['id']: c for c in json.loads(text)}
    generated = {c['id'] for c in cards}
    for cid in SHIPPED_EDITS:
        assert cid in shipped and cid in generated, f'{cid}: not in both decks'
    cards = [shipped[c['id']] if c['id'] in SHIPPED_EDITS else c
             for c in cards]
    out = json.dumps(cards, ensure_ascii=False, indent=1) + '\n'
    if args.write:
        with open(AUTHORED, 'w', encoding='utf-8') as fh:
            fh.write(out)
        print(f'wrote {len(cards)} cards to {AUTHORED}')
    else:
        sys.stdout.write(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
