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
                 cells for that band, verbatim;
  the Notes      a "... mark on its merits - Max 10 marks" clause is a ceiling
                 the student ticks; every other Note is a direction.

Nothing is typed. The one string a card carries that the SEC did not print is
`markingGuideNote`, which says how the grid is used.

The tariff is the scheme's grid head ("20 Marks x2"), checked against the
ask's own head tariff and the paper's printed marks; any disagreement stops
the build unless the sitting module records it (DISAGREE) with the evidence.

Cards land in components/MarkBank/cards/religious-education/rubric-authored.json
(build-deck folds them into the deck), and a sitting built here leaves the
point-card file (scripts/markbank/authored/religious-education.json) at the
same time, so no ask is carded twice. Shipped ids are kept: the id is the
same function of the address re_all.py used.
"""
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


# The subset fonts' broken text layer, repaired as build-deck repairs a point
# card (glyphmap.json, derived from the schemes themselves): "seƫng out
# informaƟon" is "setting out information". A rubric card does not pass
# through build-deck's repair, so the lane applies it, and refuses any glyph
# in the broken range the map cannot read.
GLYPHMAP = json.load(open(os.path.join(HERE, 'glyphmap.json'), encoding='utf8'))
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
    def __init__(self, page, top, head, per, times, bands):
        self.page, self.top, self.head, self.per, self.times, self.bands = page, top, head, per, times, bands

    def __repr__(self):
        return f'<Grid p{self.page} {self.head!r} {self.per}x{self.times} {len(self.bands)} bands>'


def _marks_of(cell):
    m = RANGE.match(cell.replace('–', '-'))
    if not m:
        return None
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    return list(range(min(a, b), max(a, b) + 1))


def read_grids(year, level):
    """Every exam band grid in the scheme, in page order. A coursework grid
    (the journal's "Set Points" / "Set Questions" tables) is not an exam ask
    and is skipped."""
    doc = pymupdf.open(os.path.join(schemes_dir(), f'{year}-{level}.pdf'))
    out = []
    for pno, page in enumerate(doc):
        for table in page.find_tables().tables:
            rows = [[ws(c) for c in row] for row in table.extract()]
            rows = [r for r in rows if any(r)]
            if not rows or not BAND_WORD.search(' '.join(rows[0][1:])):
                continue
            if re.search(r'Set\s+(?:Points|Ques)', ' '.join(rows[0])):
                continue
            width = max(len(r) for r in rows)
            rows = [r + [''] * (width - len(r)) for r in rows]
            keep = [j for j in range(width) if any(r[j] for r in rows)]
            rows = [[r[j] for j in keep] for r in rows]
            # A header the scheme sets over several range columns ("WEAK - VERY
            # WEAK - NO GRADE" over 7-5 and 4-0) leaves the later columns
            # blank: each range carries the label printed over it.
            labels = []
            for label in rows[0][1:]:
                labels.append(label or (labels[-1] if labels else ''))
            at = None
            for i in range(len(rows) - 1, 0, -1):
                cells = rows[i][1:]
                if cells and all(_marks_of(c) for c in cells):
                    at = i
                    break
            if at is None:
                raise LaneError(f'{year} {level} p{pno + 1}: a band grid with no marks row: {rows[-1]}')
            head = rows[at][0]
            nums = [int(n) for n in re.findall(r'\d+', head)]
            times = 2 if re.search(r'x\s*2|×\s*2', head, re.I) else 1
            per = nums[0] if nums else None
            bands = []
            for k, label in enumerate(labels):
                printed = rows[at][k + 1]
                descriptor = []
                for r in rows[1:at]:
                    crit, cell = r[0], r[k + 1]
                    if cell:
                        descriptor.append(f'{crit}: {cell}' if crit else cell)
                bands.append(Band(label, printed, _marks_of(printed), descriptor))
            if per is None:
                per = max(m for b in bands for m in b.marks)
            out.append(Grid(pno + 1, table.bbox[1], head, per, times, bands))
    return out


def grid_problem(grid):
    marks = sorted(m for b in grid.bands for m in b.marks)
    if marks != list(range(grid.per + 1)):
        return f'bands cover {marks} not 0..{grid.per}'
    return None


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
    if not os.path.exists(POINT_JSON):
        return {}
    return {c['id']: c for c in json.load(open(POINT_JSON, encoding='utf8'))}


def build_sitting(year, level, shipped=None):
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
    if len(grids) != len(asks):
        raise LaneError(f'{year} {level}: {len(grids)} band grids for {len(asks)} asks: {grids}')
    pages = md_page_of(S)
    cards = []
    for n, (ask, grid) in enumerate(zip(asks, grids)):
        key = ask.key
        where = f'{year} {level} {question_ref(year, level, key)}'
        head_page = pages[ask.line]
        next_page = pages[asks[n + 1].line] if n + 1 < len(asks) else 10 ** 3
        if not head_page <= grid.page <= next_page:
            raise LaneError(f'{where}: its grid is on p{grid.page}, outside its block '
                            f'(p{head_page}-{next_page})')
        problem = grid_problem(grid)
        if problem:
            raise LaneError(f'{where}: {grid}: {problem}')
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
        if ceilings:
            rubric['ceilings'] = ceilings
        rubric['directions'] = directions
        rubric['markingGuideNote'] = (note + ' ' if note else '') + (MARKING_GUIDE_X if grid.times > 1 else MARKING_GUIDE)
        rubric['schemePages'] = sorted({head_page, grid.page} | set(range(head_page, grid.page + 1)))
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
        cards.append(card)
    return cards


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
