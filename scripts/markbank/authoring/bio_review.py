#!/usr/bin/env python3
"""Build one reviewed Biology sitting into Mark Bank cards, or check it.

    python3 scripts/markbank/authoring/bio_review.py 2026 hl           # check only
    python3 scripts/markbank/authoring/bio_review.py 2026 hl --write   # write cards

The ledger is bio_review_<year>_<level>.py. Everything a student reads as the
SEC's words is lifted from the PDFs by bio_review_lib; this script assembles
the cards, crops the figures, and refuses on any of:

  * a source PDF whose bytes or page count differ from the ledger's pins;
  * a selection directive on the question pages that the ledger has not
    classified, or a classified one the paper no longer prints;
  * a task whose rows do not add up to its total, a question or part whose
    tasks do not add up to the printed total, or rows whose mark units do not
    reproduce the scheme's own tick summary;
  * a paper ask and its scheme reprint that do not share their wording;
  * a census leaf (paper_census.py, an independent reader) no task claims, or a
    task that resolves to no census leaf;
  * a task filed under a topic the Topic Atlas does not give its question;
  * a card id that existed before and is not produced again.

With --write it replaces this sitting's cards in authored/biology.json (and
only those), writes the figures into public/exam-figures/biology/markbank/
and components/MarkBank/figures-biology.json, and records the review ledger
in authored/biology-review-audit.json.
"""
import argparse
import copy
import hashlib
import importlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bio_review_lib as B  # noqa: E402
import paper_census as PC  # noqa: E402

ROOT = B.ROOT
AUTHORED = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'biology.json')
AUDIT = os.path.join(ROOT, 'scripts', 'markbank', 'authored', 'biology-review-audit.json')
CORRECTIONS = os.path.join(ROOT, 'scripts', 'markbank', 'card-corrections.json')
FIG_DIR = os.path.join(ROOT, 'public', 'exam-figures', 'biology', 'markbank')
FIG_MANIFEST = os.path.join(ROOT, 'components', 'MarkBank', 'figures-biology.json')
ATLAS_MAP = os.path.join(ROOT, 'data', 'examTopics', 'biology-{year}-exam-topic-map.json')
CROSSWALK = os.path.join(ROOT, 'data', 'examTopics', 'biology-curriculum-crosswalk.json')

SCAN = re.compile(r'\b(any\s+(?:one|two|three|four|five|six)|either|choose|one of the following'
                  r'|the following|or|both)\b', re.I)
LABEL_SPLIT = re.compile(r'^([A-Z][A-Za-z ()-]{0,30}):\s+(\S.*)$')


class Refusal(Exception):
    pass


def fail(problems):
    if problems:
        raise Refusal('\n'.join(f'  - {p}' for p in problems))


def level_word(level):
    return B.LEVEL_WORD[level]


def booklet(sec, ledger=None):
    """The booklet a section is printed in. From 2019 the paper is two booklets
    (038: Sections A and B, 040: Section C); up to 2018 it is one, keyed
    'paper' in the ledger's SOURCES."""
    if ledger is not None and 'paper' in ledger.SOURCES:
        return 'paper'
    return '038' if sec in ('A', 'B') else '040'


# ------------------------------------------------------------------ lifting --

class Lifter:
    def __init__(self, ledger):
        self.ledger = ledger
        self.srcs = {}
        problems = []
        for key, pin in ledger.SOURCES.items():
            path = os.path.join(ROOT, pin['path'])
            if not os.path.exists(path):
                problems.append(f'{key}: {pin["path"]} is missing')
                continue
            src = B.Src(path, key)
            if src.sha != pin['sha256']:
                problems.append(f'{key}: sha256 {src.sha} != pinned {pin["sha256"]}')
            if src.pages != pin['pages']:
                problems.append(f'{key}: {src.pages} pages != pinned {pin["pages"]}')
            self.srcs[key] = src
        fail(problems)
        self.used = defaultdict(set)   # src -> pages lifted from

    def lift(self, sel, task_doc, scheme_page=None, scheme_lo=None):
        if sel.get('src') == 'marker':
            doc = sel.get('doc') or task_doc
            lines = self.srcs[doc].lines[sel['page']]
            if not any(l == sel['text'] or l.startswith(sel['text'] + ' ') for l in lines):
                raise LookupError(f'{doc} p{sel["page"]}: marker {sel["text"]!r} is not printed')
            return sel['text'], {'page': sel['page'], 'starred': False, 'lines': None, 'doc': doc}
        doc = (sel.get('doc') or task_doc) if sel.get('src') == 'paper' else 'scheme'
        src = self.srcs[doc]
        page = sel.get('page') or scheme_page
        lo = scheme_lo if (doc == 'scheme' and page == scheme_page and scheme_lo
                           and not sel.get('after')) else 0
        text, meta = src.select(page, sel['start'], sel.get('end'), after=sel.get('after'),
                                before=sel.get('before'), nth=sel.get('nth', 1), lo=lo,
                                end_nth=sel.get('end_nth', 1), skip_marks=sel.get('skip_marks', False),
                                wordbreak=sel.get('wordbreak', False))
        self.used[doc].add(page)
        if sel.get('piece'):
            pieces = sel['piece'] if isinstance(sel['piece'], list) else [sel['piece']]
            seps = sel.get('psep') or ['/'] * len(pieces)
            seps = seps if isinstance(seps, list) else [seps]
            for index, sep in zip(pieces, seps):
                cut = [x.strip() for x in text.split(sep)]
                if not 1 <= index <= len(cut):
                    raise LookupError(f'{doc} p{page}: no piece {index} in {text!r}')
                text = cut[index - 1]
        return text, {**meta, 'doc': doc}


def join(parts):
    return B.join_lines(p for p in parts if p)


def strip_stars(text):
    return re.sub(r'\s+', ' ', text.replace('*', '')).strip()


# ----------------------------------------------------------------- geometry --

def _center(r):
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)


def read_geo(lifter, spec, sp):
    """The answer a scheme prints as a mark, read from glyph positions."""
    src = lifter.srcs['scheme']
    page = spec.get('page') or sp
    clip = spec['clip']
    kind = spec['kind']
    lifter.used['scheme'].add(page)
    if kind in ('tick-row', 'tick-col'):
        ticks = src.answer_ticks(page, clip)
        if len(ticks) != 1:
            raise Refusal(f'{kind} p{page} {clip}: {len(ticks)} answer ticks, expected 1')
        tx, ty = _center(ticks[0])
        if kind == 'tick-row':
            scored = []
            for choice in spec['choices']:
                # A choice is its printed text, or (text, clip) where the same
                # words print twice in the row ("Cell wall" / "No cell wall").
                choice, cclip = choice if isinstance(choice, (tuple, list)) else (choice, clip)
                boxes = src.find_box(page, choice, cclip)
                if not boxes:
                    raise Refusal(f'tick-row p{page}: choice {choice!r} not printed in {cclip}')
                b = boxes[0]
                dy = abs((b.y0 + b.y1) / 2 - ty)
                dx = abs(ticks[0].x0 - b.x1)
                scored.append((round(dy / 6), dx, choice))
            value = min(scored)[2]
        else:
            scored = []
            for head in spec['headers']:
                boxes = [b for b in src.find_exact(page, head) if b.y1 <= clip[1] + 2]
                if not boxes:
                    raise Refusal(f'tick-col p{page}: header {head!r} not above {clip}')
                b = max(boxes, key=lambda r: r.y0)
                if sum(1 for r in boxes if abs(r.y0 - b.y0) < 2) > 1:
                    raise Refusal(f'tick-col p{page}: header {head!r} printed twice on one line')
                scored.append((abs((b.x0 + b.x1) / 2 - tx), head))
            value = min(scored)[1]
    elif kind == 'under':
        # A letter the scheme prints in a table cell under its part's column
        # header (the 2020 Higher true/false key: "(c)" over "T"), read from
        # the column the header heads.
        heads = src.find_exact(page, spec['head'], clip)
        if len(heads) != 1:
            raise Refusal(f'under p{page}: header {spec["head"]!r} printed {len(heads)} times in {clip}')
        h = heads[0]
        hx = (h.x0 + h.x1) / 2
        below = [(r, t) for r, t in src.words(page, clip)
                 if r.y0 >= h.y1 - 1 and abs((r.x0 + r.x1) / 2 - hx) < 12]
        value = ' '.join(t for _, t in sorted(below, key=lambda w: (round(w[0].y0), w[0].x0)))
    elif kind == 'circled':
        boxes = src.find_box(page, spec['part'], clip)
        if not boxes:
            raise Refusal(f'circled p{page}: {spec["part"]!r} not printed in {clip}')
        b = boxes[0]
        row = [n for r, n in src.wingdings_digits(page, clip)
               if abs(_center(r)[1] - (b.y0 + b.y1) / 2) < 6 and r.x0 > b.x1]
        if len(row) != 1:
            raise Refusal(f'circled p{page}: {len(row)} circled numbers beside {spec["part"]!r}')
        value = f'{spec["part"]} — {chr(0x2460 + row[0] - 1)}'
    elif kind == 'tokens':
        words = sorted(src.words(page, clip), key=lambda w: (round(w[0].y0 / 8), w[0].x0))
        # `strip` drops the printed answer line a filled-in blank sits on
        # ("____hormones______" reads "hormones"); the word itself is untouched.
        value = ' '.join(t.strip(spec['strip']) if spec.get('strip') else t for _, t in words)
    elif kind == 'lines':
        # Printed rows, top to bottom, each read left to right: a formula the
        # scheme sets as its letters over their numbers ("C H O" / "6 12 6").
        rows = []
        for r, t in sorted(src.words(page, clip), key=lambda w: _center(w[0])[1]):
            cy = _center(r)[1]
            if rows and abs(rows[-1][0] - cy) < 6:
                rows[-1][1].append((r.x0, t))
            else:
                rows.append([cy, [(r.x0, t)]])
        value = ' — '.join(' '.join(t for _, t in sorted(cells)) for _, cells in rows)
    elif kind == 'tokens-x':
        # Left to right only: a formula whose subscripts sit below the line.
        words = sorted(src.words(page, clip), key=lambda w: w[0].x0)
        value = ' '.join(t for _, t in words)
    elif kind == 'pair':
        words = [(r, t) for r, t in src.words(page, clip) if len(t) == 1]
        rows = []
        for r, t in sorted(words, key=lambda w: _center(w[0])[1]):
            cy = _center(r)[1]
            if rows and abs(rows[-1][0] - cy) < 6:
                rows[-1][1].append((r.x0, t))
            else:
                rows.append([cy, [(r.x0, t)]])
        pairs = [' — '.join(t for _, t in sorted(cells)) for _, cells in rows]
        value = pairs[spec['index']]
    else:
        raise Refusal(f'unknown geometry kind {kind!r}')
    if value != spec['expect']:
        raise Refusal(f'{kind} p{page}: glyph positions read {value!r}, reviewer read '
                      f'{spec["expect"]!r}')
    return value


# ------------------------------------------------------------------- building --

def build_row(lifter, spec, row_id, task_doc, sp, lo):
    notes = []
    if spec['type'] == 'geo':
        value = read_geo(lifter, spec, sp)
        label = None
        if spec.get('label'):
            label, _ = lifter.lift(spec['label'], task_doc, sp, lo)
            label = strip_stars(label).rstrip(':').strip()
        kind = spec.get('row_kind') or ('gate' if spec.get('gate') else 'point')
        row = {'id': row_id, 'kind': kind,
               'verbatim': f'{label} — {value}' if label else value, 'marks': spec['marks']}
        if kind == 'gate':
            row['exactTermRequired'] = True
        units, worth = [spec['marks']], spec['marks']
    elif spec['type'] == 'allof':
        # One mark for several answers printed on separate lines, all of which
        # must be given ("Name stage A: *Lag / Name stage B: *Log / ... All
        # three 3"): each answer, with its printed label, in one row.
        pieces, starred = [], False
        for lab, ans in spec['parts']:
            text, meta = lifter.lift(ans, task_doc, sp, lo)
            starred |= meta['starred'] or '*' in text
            text = strip_stars(text)
            if lab:
                label, _ = lifter.lift(lab, task_doc, sp, lo)
                text = f'{strip_stars(label).rstrip(":").strip()} — {text}'
            pieces.append(text)
        row = {'id': row_id, 'kind': 'gate' if starred else 'point', 'verbatim': ' / '.join(pieces),
               'marks': spec['marks']}
        if starred:
            row['exactTermRequired'] = True
        units, worth = [spec['marks']], spec['marks']
    elif spec['type'] == 'pt':
        text, meta = lifter.lift(spec['sel'], task_doc, sp, lo)
        starred = meta['starred'] or '*' in text
        if spec.get('first_alt'):
            text = text.split(' or ')[0]
        text = strip_stars(text)
        label = None
        if spec.get('label'):
            label, _ = lifter.lift(spec['label'], task_doc, sp, lo)
            label = label.rstrip(':').strip()
        elif not spec.get('whole'):
            m = LABEL_SPLIT.match(text)
            if m:
                label, text = m.group(1), m.group(2)
        kind = spec.get('kind')
        if not kind:
            kind = 'gate' if starred else ('alt' if ' or ' in text else 'point')
        row = {'id': row_id, 'kind': kind,
               'verbatim': f'{label} — {text}' if label else text,
               'marks': spec['marks']}
        if kind == 'gate':
            row['exactTermRequired'] = True
        if 'other correct' in text.lower():
            row['openList'] = True
        units = spec['units']
        worth = spec['marks']
    else:
        options, starred_any = [], False
        if spec.get('options'):
            for o in spec['options']:
                if o.get('type') == 'geo':
                    options.append(read_geo(lifter, o, sp))
                    continue
                sel = o['sel'] if 'sel' in o else o
                osel = dict(sel)
                if isinstance(o, dict) and o.get('end_nth'):
                    osel['end_nth'] = o['end_nth']
                t, meta = lifter.lift(osel, task_doc, sp, lo)
                starred_any |= meta['starred'] or '*' in t
                if o.get('first_alt'):
                    t = t.split(' or ')[0]
                options.append(strip_stars(t))
        else:
            t, meta = lifter.lift(spec['sel'], task_doc, sp, lo)
            starred_any |= '*' in t
            # A menu printed as one "or" list ("Common cold virus or HIV or
            # ...", "Name two") is cut at the scheme's own "or".
            options = [strip_stars(B.clean_option(x)) for x in t.split(spec.get('sep') or '/')]
            if spec.get('sep') == ',' and options:
                # A comma list closes with the sentence's own full stop
                # ("..., glomerulus."), which is not part of its last item.
                options[-1] = re.sub(r'\.$', '', options[-1])
            # The scheme's tally ("Any three") printed at the end of the menu's
            # last line is not an option: it goes to the row's note.
            tally = re.search(r'\s+\(?((?:Any|any) (?:one|two|three|four|five|six))\)?$', options[-1]) \
                if options else None
            if tally:
                notes.append(tally.group(1))
                options[-1] = options[-1][:tally.start()]
        open_list = any(o.lower() == 'other correct' for o in options)
        options = [o for o in options if o and o.lower() != 'other correct']
        # The scheme's trailing ellipsis ("oxygen……….") and a closing "or
        # examples" both mean the menu is open; neither is itself an option.
        tail = [o for o in options if o.lower().startswith('or ')]
        if tail:
            notes.append(' '.join(tail))
            options = [o for o in options if o not in tail]
            open_list = True
        trimmed = [re.sub(r'\s*[.…]{3,}$', '', o) for o in options]
        if trimmed != options:
            open_list = True
            options = trimmed
        if any('other correct' in o.lower() for o in options):
            open_list = True
        if spec.get('open_list'):
            # The scheme prints its menu as examples ("Any six correct labels
            # e.g. ..."): open, though no option says so.
            open_list = True
        group = {'claimMax': spec['claim'], 'perOption': spec['per'], 'options': options}
        if spec.get('steps'):
            group['perOptionSteps'] = spec['steps']
        row = {'id': row_id, 'kind': 'anyN', 'verbatim': ' / '.join(options), 'marks': None,
               'group': group}
        if open_list:
            row['openList'] = True
        units = spec['steps'] or [spec['per']] * spec['claim']
        worth = sum(units)
        if len(options) < spec['claim']:
            raise Refusal(f'{row_id}: {len(options)} options for claim {spec["claim"]}')
    if spec.get('note_sel'):
        n, _ = lifter.lift(spec['note_sel'], task_doc, sp, lo)
        n = strip_stars(n)
        notes.append(f'{spec["note_lead"]} {n}' if spec.get('note_lead') else n)
    if spec.get('note'):
        notes.append(spec['note'])
    if notes:
        row['contextNote'] = ' '.join(notes)
    return row, units, worth


def _unpriced_spec(spec):
    """A row spec of a whole-part (questionTotal) task, built with placeholder
    zero marks: the rows of such a card carry none of their own."""
    s = dict(spec)
    if s['type'] == 'pt':
        s['marks'], s['units'] = 0, [0]
    elif s['type'] == 'anyn':
        s['per'], s['steps'] = 0, None
        s['claim'] = s.get('claim') or 1
    else:
        s['marks'] = 0
    return s


def _unpriced_rows(row):
    """The rows a whole-part card shows for one built row: unpriced, and a
    menu as one row per printed option (never one welded string)."""
    if row['kind'] != 'anyN':
        out = {k: v for k, v in row.items() if k != 'marks'}
        out['marks'] = None
        return [out]
    opts = row['group']['options']
    rows = []
    for j, o in enumerate(opts):
        r = {'id': None, 'kind': 'alt' if ' or ' in o else 'point', 'verbatim': o, 'marks': None}
        if j == 0 and row.get('contextNote'):
            r['contextNote'] = row['contextNote']
        if j == len(opts) - 1 and row.get('openList'):
            r['openList'] = True
        rows.append(r)
    return rows


def ladder_key(ledger, qn, letter):
    """The LADDERS key a part belongs to: its question, or (question, letters)."""
    for k in getattr(ledger, 'LADDERS', {}):
        if k == qn or (isinstance(k, tuple) and k[0] == qn and letter and letter in k[1]):
            return k
    return None


def build(ledger, year, level):
    lifter = Lifter(ledger)
    LT = B.LEVEL_TOKEN[level]
    problems = []

    # --- selection scan ---------------------------------------------------
    found = []
    for doc, pages in ledger.SCAN_PAGES.items():
        for p in pages:
            text = lifter.srcs[doc].page_text(p)
            found += [(doc, p, m.group(0).lower()) for m in SCAN.finditer(text)]
    pinned = [(d, p, w) for d, p, w, _ in ledger.SELECTION_SCAN]
    if found != pinned:
        a, b = Counter(found), Counter(pinned)
        problems.append(f'selection scan drifted: unclassified {sorted((a - b).elements())}, '
                        f'stale {sorted((b - a).elements())}')
    fail(problems)

    # --- tasks ------------------------------------------------------------
    cards, audit_tasks, excluded = [], [], []
    units_by = defaultdict(Counter)
    ladder_units = defaultdict(Counter)
    totals_q, totals_part = defaultdict(int), defaultdict(int)
    # Tasks of a laddered question that sit under no ladder: a whole-part
    # (questionTotal) card or a part priced on its own beside the ladders.
    free_q = defaultdict(int)
    seen_ids = set()
    for t in ledger.TASKS:
        doc = booklet(t['sec'], ledger)
        # The paper's own ask.
        qsels = t['q'] if isinstance(t['q'], list) else [t['q']]
        qparts, qmetas = [], []
        try:
            for s in qsels:
                txt, meta = lifter.lift(s, doc)
                qparts.append(txt)
                qmetas.append(meta)
            stem_parts = [lifter.lift(s, doc)[0] for s in t['stem']]
        except LookupError as e:
            problems.append(f'{t["key"]} question/stem: {e}')
            continue
        qtext = ''
        for s_, txt in zip(qsels, qparts):
            if not qtext:
                qtext = txt
            elif s_.get('br'):
                qtext = f'{qtext}\n{txt}'
            else:
                qtext = join([qtext, txt])
        stem = join(stem_parts)
        # The scheme's reprint: the pairing anchor and the scope of the rows.
        sq = t['sq']
        try:
            sq_lo = 0
            for anchor in sq.get('path', []):
                lines = lifter.srcs['scheme'].lines[sq['page']]
                hit = next((i for i in range(sq_lo, len(lines)) if lines[i] == anchor), None)
                if hit is None:
                    raise LookupError(f'scheme p{sq["page"]}: path line {anchor!r} not found')
                sq_lo = hit + 1
            sq_text, sq_meta = lifter.srcs['scheme'].select(
                sq['page'], sq['start'], sq.get('end'), after=sq.get('after'), nth=sq.get('nth', 1),
                lo=sq_lo)
        except LookupError as e:
            problems.append(f'{t["key"]} scheme reprint: {e}')
            continue
        lifter.used['scheme'].add(sq['page'])
        lo = sq_meta['lines'][1] + 1
        if sq.get('welded'):
            # A bare anchor on a part marker that opens its own answer's printed
            # line ("(a) Protein", 2015 Higher Section A, a scheme that prints no
            # reprints): the marker is the anchor, and the rows are searched from
            # that same line.
            mk = re.match(r'(\((?:[a-h]|i|ii|iii|iv|v|vi|vii|viii|ix|x)\))\s+\S', sq_text)
            if not (sq.get('bare') and mk):
                problems.append(f'{t["key"]}: a welded anchor is a bare part marker opening its answer\'s line; '
                                f'got {sq_text!r}')
                continue
            sq_text = mk.group(1)
            lo = sq_meta['lines'][0]
        # Wording check: most of the scheme reprint's content words are in the ask
        # (or its stem: the scheme often reprints the lead-in with the ask).
        score = B.overlap(sq_text, qtext + ' ' + stem)
        if sq.get('bare'):
            if not (sq.get('paired') and re.fullmatch(r'\((?:[a-h]|i|ii|iii|iv|v|vi|vii|viii|ix|x)\)', sq_text)):
                problems.append(f'{t["key"]}: a bare scheme anchor must be a part marker alone, with the '
                                f'reviewer\'s reason; got {sq_text!r}')
        elif score < 0.6 and not (sq.get('paired') and score >= 0.25):
            problems.append(f'{t["key"]}: scheme reprint "{sq_text[:60]}" shares {score:.0%} of its '
                            f'words with the paper ask "{qtext[:60]}"')
        rows, task_units, worth = [], [], 0
        whole = t.get('tariff') == 'questionTotal'
        for i, spec in enumerate(t['rows']):
            try:
                row, units, w = build_row(lifter, _unpriced_spec(spec) if whole else spec, f'r{i + 1}',
                                          doc, sq['page'], lo)
            except (LookupError, Refusal) as e:
                problems.append(f'{t["key"]} row {i + 1}: {e}')
                continue
            if whole:
                rows += _unpriced_rows(row)
                continue
            rows.append(row)
            task_units += units
            worth += w
        if whole:
            for i, r in enumerate(rows):
                r['id'] = f'r{i + 1}'
            wq, wl, wr, _ = B.parse_ref(t['ref'])
            printed = ledger.PART_TOTALS.get((wq, wl)) if wl else ledger.QUESTION_TOTALS.get(wq)
            if wr is not None or t['route'] or t.get('item'):
                problems.append(f'{t["key"]}: a questionTotal task cards a whole printed part')
            if printed != t['total']:
                problems.append(f'{t["key"]}: questionTotal {t["total"]} is not the printed part total {printed}')
        elif worth != t['total']:
            problems.append(f'{t["key"]}: rows are worth {worth}, task total is {t["total"]}')
        variants = None
        if t['key'] in getattr(ledger, 'ANSWER_VARIANTS', {}):
            variants = []
            for vid, vlabel, specs in ledger.ANSWER_VARIANTS[t['key']]:
                vrows, vworth = [], 0
                for i, spec in enumerate(specs):
                    row, _, w = build_row(lifter, spec, f'r{i + 1}', doc, sq['page'], lo)
                    vrows.append(row)
                    vworth += w
                if vworth != t['total']:
                    problems.append(f'{t["key"]} variant {vid}: worth {vworth} != {t["total"]}')
                variants.append({'id': vid, 'label': vlabel, 'rows': vrows})
        qn, letter, roman, item = B.parse_ref(t['ref'])
        key_part = (qn, letter)
        item = t.get('item')
        cid = t.get('id') or B.card_id(year, level, t['ref'],
                                       t['route'] or (item[0] if item else None))
        if cid in seen_ids:
            problems.append(f'{cid}: duplicate card id')
        seen_ids.add(cid)
        # Route cards share one task: count its tariff once.
        first_route = not t['route'] or t['route'] == ledger.ROUTES[t['ref']][0]
        # LADDER_OF names the ladder of a task whose part holds more than one
        # (2018 HL Q11(b): the labels' ladder, then "2(3) + 2 + 2(1)" over
        # (ii) and (iii)); every other task finds its ladder by question/letter.
        lk = getattr(ledger, 'LADDER_OF', {}).get(t['key']) or ladder_key(ledger, qn, letter)
        if whole and lk is not None:
            problems.append(f'{t["key"]}: a questionTotal part cannot also sit under ladder {lk}')
        if first_route:
            ck = key_part if key_part in ledger.CHECKSUMS else qn
            if whole and ck in ledger.CHECKSUMS:
                problems.append(f'{t["key"]}: a questionTotal part has no tick summary to check ({ck})')
            units_by[ck].update(task_units)
            if lk is not None:
                ladder_units[lk].update(task_units)
            totals_q[qn] += t['total']
            if lk is None:
                free_q[qn] += t['total']
            if key_part in ledger.PART_TOTALS:
                totals_part[key_part] += t['total']
        card = {
            'id': cid, 'subjectId': 'biology', 'topicId': t['topic'], 'conceptId': t['concept'],
            'section': t['sec'],
            'questionRef': f'{year} {LT} {t["ref"]}' + (f' — {t["route"]}' if t['route'] else '')
                           + (f' — {item[1]}' if item else ''),
        }
        if stem:
            card['stem'] = stem
        tariff = {'kind': 'questionTotal'} if whole else {'kind': 'fixed'}
        # A part the scheme prices on its own beside a ladder (a drawing's
        # "3" and "3" before "4 + 2 + 2 + 2 + 2 + 6") keeps its own marks.
        exempt = t['key'] in getattr(ledger, 'LADDER_EXEMPT', ())
        lspec = getattr(ledger, 'LADDERS', {}).get(lk) if lk is not None and not exempt else None
        if isinstance(lspec, dict) and lspec.get('notation'):
            # "2(5) + 5(2)": what a response earns depends on how many came
            # before it, so the rows carry no marks of their own; the card's
            # total is its responses at the ladder's first rate.
            tariff = {'kind': 'orderedSplit', 'notation': lspec['notation']}
            for r in rows + [r for v in (variants or []) for r in v['rows']]:
                r['marks'] = None
        card.update({'questionText': qtext, 'tariffModel': tariff,
                     'totalMarks': t['total'], 'rows': rows})
        if variants:
            card['answerVariants'] = variants
        notes = ' '.join(x for x in (t['decision'], t['notes']) if x)
        card['notes'] = (notes + ' ' if notes else '') + \
            f'Reviewed {getattr(ledger, "REVIEWED_AT", "2026-10-11")} against the paper and scheme; ledger bio_review_{year}_{level}.py.'
        card.update({'year': year, 'level': level_word(level)})
        if t['fig']:
            card['figureKey'] = f'biology-{year}-{level}-{t["fig"]}'
        if t['qfig']:
            card['questionFigureKey'] = f'biology-{year}-{level}-{t["qfig"]}'
        if t['labels']:
            key = []
            for lab in t['labels']:
                meaning, _ = lifter.lift(lab['sel'], doc)
                # A scheme row label ("Nucleus:") names the part without its colon.
                meaning = strip_stars(meaning).rstrip(':').strip()
                key.append({'letter': lab['letter'], 'meaning': meaning,
                            'askedInThisQuestion': lab['asked']})
            card['labelKey'] = key
        if t['source_pages']:
            card['sourceMaterial'] = {
                'kind': 'source-illustration', 'label': 'OFFICIAL QUESTION PAGE',
                'title': 'Official question page', 'pages': t['source_pages'],
                'attribution': f'SEC Biology {year} {"Higher" if level == "hl" else "Ordinary"} '
                               'Level examination paper — © State Examinations Commission.',
                'presentationNote': 'Open the exact examination page to use its published chart, '
                                    'table, photograph or diagram.',
            }
        if t.get('excluded'):
            if not t.get('evidence'):
                problems.append(f'{t["key"]}: an exclusion needs the SEC evidence for its reason')
            excluded.append({'key': t['key'], 'id': cid, 'questionRef': card['questionRef'],
                             'total': t['total'], 'reason': t['excluded'],
                             'evidence': t.get('evidence'),
                             'schemeRows': [r['verbatim'] for r in rows]})
        else:
            cards.append(card)
        audit_tasks.append({
            'status': 'excluded' if t.get('excluded') else 'carded',
            'key': t['key'], 'id': cid, 'questionRef': card['questionRef'], 'section': t['sec'],
            'paper': {'doc': doc, 'pages': sorted({m['page'] for m in qmetas})},
            'scheme': {'pages': sorted({sq['page']})},
            'total': t['total'], 'markUnits': task_units, 'topic': t['topic'],
            'concept': t['concept'], 'route': t['route'],
            **({'tariff': 'questionTotal'} if whole else {}),
            **({'item': item[1]} if item else {}), 'rows': len(rows),
            'figure': t['fig'], 'questionFigure': t['qfig'],
            'sourcePages': t['source_pages'], 'pairingScore': round(score, 2),
            **({'pairedBy': sq['paired']} if sq.get('paired') else {}),
            'decision': t['decision'] or None, 'notes': t['notes'] or None,
        })

    # The build ships one card per questionRef, so two must never share one.
    dup_refs = [r for r, n in Counter(c['questionRef'] for c in cards).items() if n > 1]
    if dup_refs:
        problems.append(f'questionRefs shared by more than one card: {dup_refs}')

    # --- totals and checksums --------------------------------------------
    ladders = getattr(ledger, 'LADDERS', {})
    for qn, total in ledger.QUESTION_TOTALS.items():
        got = totals_q.get(qn, 0)
        lkeys = [k for k in ladders if k == qn or (isinstance(k, tuple) and k[0] == qn)]
        if lkeys:
            # A ladder ("6(3) + (2)", "2(5) + 5(2)"): each response is carded
            # at the ladder's first step, and the ladder, not the sum of the
            # cards, makes the printed total. A ladder may sit beside a part
            # the scheme prices on its own ("3(1)" then "5(3) + 2"):
            # {'steps': [...], 'fixed': {mark: count}} names those units; a
            # question may hold two ladders, keyed (qn, 'letters'); and
            # 'responses' allows more carded responses than steps, as in a
            # best-five-of-six question, or fewer where a response's ask is
            # left open or excluded without a task (OPEN_LEAVES,
            # EXCLUDED_LEAVES).
            # A part under no ladder (a whole-part card, 2019 Ordinary Q7(b)
            # beside Q7(a)'s "4 + 2") adds its own total to the ladders'.
            ladder_total = free_q.get(qn, 0)
            for lk in lkeys:
                spec = ladders[lk]
                steps, fixed = (spec['steps'], Counter(spec.get('fixed', {}))) \
                    if isinstance(spec, dict) else (spec, Counter())
                want = spec.get('responses', len(steps)) if isinstance(spec, dict) else len(steps)
                units = ladder_units.get(lk, Counter()) - fixed
                got_fixed = ladder_units.get(lk, Counter()) & fixed
                units = sorted(units.elements())
                fixed_total = sum(m * n for m, n in fixed.items())
                ladder_total += sum(steps) + fixed_total
                if len(units) != want or set(units) != {steps[0]} or got_fixed != fixed:
                    problems.append(f'Q{qn} ladder {lk}: {len(units)} responses at {set(units)} (+ '
                                    f'fixed {dict(got_fixed)}) do not fit {steps}')
            if ladder_total != total:
                problems.append(f'Q{qn}: ladders (and parts under none) make {ladder_total}, paper prints {total}')
        elif qn in getattr(ledger, 'BEST_OF', {}):
            n, per = ledger.BEST_OF[qn]
            parts = [c for c in cards
                     if B.parse_ref(c['questionRef'].split(' ', 2)[2].split(' — ')[0])[0] == qn]
            if any(c['totalMarks'] != per for c in parts) or n * per != total:
                problems.append(f'Q{qn}: best {n} of parts at {per} does not make {total}')
        elif got != total:
            problems.append(f'Q{qn}: tasks total {got}, paper prints {total}')
    for kp, total in ledger.PART_TOTALS.items():
        if totals_part.get(kp, 0) != total:
            problems.append(f'Q{kp[0]}({kp[1]}): tasks total {totals_part.get(kp, 0)}, '
                            f'scheme prints {total}')
    for ck, want in ledger.CHECKSUMS.items():
        got = dict(units_by.get(ck, {}))
        if got != want:
            problems.append(f'checksum {ck}: rows give {got}, scheme tick summary says {want}')

    # --- census: every leaf claimed, every task a leaf --------------------
    parts, _texts, _files = PC.census_merged('biology', year, level, None)
    leaves = set(PC.leaves_of(parts))
    claimed = set()
    for t in ledger.TASKS:
        # An excluded task is reviewed and accounted for: it claims its leaf.
        qn, letter, roman, _ = B.parse_ref(t['ref'])
        key = (qn, letter, roman)
        hit = [l for l in leaves if l == key or (l[0] == qn and l[1] == letter and roman is None)]
        if not hit and letter is None and roman is None and t.get('tariff') == 'questionTotal':
            # A whole QUESTION carded as one task (its scheme prints a tariff the
            # answers fit no reading of, 2013 Higher Q5 and Q6 "1 + 1 + 8 + 6 +
            # 4(1)") claims every leaf the census reads under that question.
            hit = [l for l in leaves if l[0] == qn]
        if not hit:
            problems.append(f'{t["key"]}: {t["ref"]} is no census leaf')
        claimed.update(hit)
    # A census leaf left OPEN: the paper prints the ask and the scheme prints
    # nothing for it to lift (2010 Ordinary Q11(c)(vii): scheme p7's Q11(c)
    # block stops at (vi), then blank rows). It is neither carded nor
    # excluded: it stays open for reconcile.py to report, with its reason and
    # page evidence recorded in the audit.
    open_leaves = getattr(ledger, 'OPEN_LEAVES', {})
    open_list = []
    for leaf, why in sorted(open_leaves.items(), key=lambda kv: str(kv[0])):
        if leaf not in leaves:
            problems.append(f'OPEN_LEAVES {leaf} is no census leaf')
        elif leaf in claimed:
            problems.append(f'OPEN_LEAVES {leaf} is claimed by a task')
        elif not (why.get('reason') and why.get('evidence')):
            problems.append(f'OPEN_LEAVES {leaf} needs its reason and its page evidence')
        open_list.append({'leaf': f'Q{leaf[0]}' + ''.join(f'({x})' for x in leaf[1:] if x),
                          'reason': why.get('reason'), 'evidence': why.get('evidence')})
    # A census leaf EXCLUDED without a task: the same case as an open leaf
    # (the scheme prints nothing to lift, so there are no scheme rows to
    # price), recorded as an exclusion once that is decided (2010 Ordinary
    # Q11(c)(vii), 2026-10-27). reconcile.py counts exclusions from
    # exclusions/biology.json, so the same ref, reason and evidence must
    # stand there: the ledger and the coverage count cannot drift apart.
    excl_leaves = getattr(ledger, 'EXCLUDED_LEAVES', {})
    excl_list = []
    if excl_leaves:
        excl_path = os.path.join(HERE, 'exclusions', 'biology.json')
        excl_file = json.load(open(excl_path, encoding='utf-8')) if os.path.exists(excl_path) else []
    for leaf, why in sorted(excl_leaves.items(), key=lambda kv: str(kv[0])):
        label = f'Q{leaf[0]}' + ''.join(f'({x})' for x in leaf[1:] if x)
        if leaf not in leaves:
            problems.append(f'EXCLUDED_LEAVES {leaf} is no census leaf')
        elif leaf in claimed:
            problems.append(f'EXCLUDED_LEAVES {leaf} is claimed by a task')
        elif leaf in open_leaves:
            problems.append(f'EXCLUDED_LEAVES {leaf} is also in OPEN_LEAVES')
        elif not (why.get('reason') and why.get('evidence')):
            problems.append(f'EXCLUDED_LEAVES {leaf} needs its reason and its page evidence')
        ref = f'{year} {level.upper()} {label}'
        entry = [e for e in excl_file if e.get('ref') == ref]
        if len(entry) != 1 or entry[0].get('reason') != why.get('reason') \
                or entry[0].get('evidence') != why.get('evidence'):
            problems.append(f'EXCLUDED_LEAVES {leaf}: exclusions/biology.json needs one entry "{ref}" '
                            'with this reason and evidence')
        excl_list.append({'leaf': label, 'reason': why.get('reason'), 'evidence': why.get('evidence')})
    for leaf in sorted(leaves - claimed - set(open_leaves) - set(excl_leaves), key=str):
        problems.append(f'census leaf {leaf} has no task')

    # --- figure keys -----------------------------------------------------
    # Every figure a task names is cropped, and every crop is shown by a task.
    named = {k for t in ledger.TASKS for k in (t['fig'], t['qfig']) if k}
    for k in sorted(named - set(ledger.FIGURES)):
        problems.append(f'figure {k!r} is named by a task but has no crop in FIGURES')
    for k in sorted(set(ledger.FIGURES) - named):
        problems.append(f'figure {k!r} is cropped but no task shows it')

    # --- question figures carry the printed ask -----------------------------
    # The app shows a question figure IN PLACE of the card's question text and
    # stem, so the crop must itself print the ask: every paper selector of the
    # task's question has to open inside the crop's rectangle on its page.
    for t in ledger.TASKS:
        if not t['qfig'] or t['qfig'] not in ledger.FIGURES:
            continue
        fdoc, fpage, frect = ledger.FIGURES[t['qfig']][:3]
        for sel in (t['q'] if isinstance(t['q'], list) else [t['q']]):
            sdoc = sel.get('doc') or booklet(t['sec'], ledger)
            if sel.get('src') != 'paper':
                continue
            # Searched up to its first symbol glyph ("Tick (✓) ..."), which the
            # text search cannot match.
            probe = re.match(r"[\w\s,.;:'’‘()\-]+", sel['start'])
            probe = (probe.group(0) if probe else sel['start'])[:60].strip()
            boxes = [] if (sdoc, sel['page']) != (fdoc, fpage) else \
                lifter.srcs[sdoc].find_box(fpage, probe, fitz.Rect(*frect))
            if not boxes:
                problems.append(f'{t["key"]}: question figure {t["qfig"]!r} does not print the ask '
                                f'{sel["start"][:50]!r} (a question figure replaces the question text)')

    # --- Atlas topics -----------------------------------------------------
    atlas = json.load(open(ATLAS_MAP.format(year=year), encoding='utf-8'))
    crosswalk = json.load(open(CROSSWALK, encoding='utf-8'))
    atlas_view = defaultdict(lambda: {'atlasTopics': [], 'taskTopics': set()})
    for t in ledger.TASKS:
        qn = B.parse_ref(t['ref'])[0]
        topics = atlas['questions'].get(f'{level_word(level)}|{qn}', [])
        nodes = {n for tp in topics for n in crosswalk.get(tp, [])}
        view = atlas_view[qn]
        view['atlasTopics'] = topics
        view['taskTopics'].add(t['topic'])
        filed = getattr(ledger, 'ATLAS_UNIT_EQUIV', {}).get(t['topic'], t['topic'])
        # An excluded task makes no card, so nothing is filed under its topic:
        # a part the SEC withdrew as outside the syllabus must not pull its
        # topic onto the question's Atlas entry.
        if filed not in nodes and not t.get('excluded'):
            problems.append(f'{t["key"]}: topic {t["topic"]} is not among the Atlas topics for '
                            f'Q{qn} ({sorted(nodes)})')

    # --- column layouts ---------------------------------------------------
    # A two-column scheme layout reads into the text layer line by line, so
    # which column a row belongs to is checked from where it is printed: the
    # row's left edge must sit nearest the left edge of its own heading.
    layout = []
    for check in getattr(ledger, 'LAYOUT_CHECKS', []):
        doc, page, item, heads, want = check[:5]
        clip = check[5] if len(check) > 5 else None
        src = lifter.srcs[doc]
        ib = src.find_exact(page, item, clip)
        if len(ib) != 1:
            problems.append(f'layout {doc} p{page}: {item!r} printed {len(ib)} times')
            continue
        ib = ib[0]
        scored = []
        for h in heads:
            hb = [b for b in src.find_exact(page, h, clip) if b.y0 < ib.y0]
            if not hb:
                problems.append(f'layout {doc} p{page}: no {h!r} above {item!r}')
                continue
            b = max(hb, key=lambda r: r.y0)
            scored.append((abs(b.x0 - ib.x0), h))
        if scored and min(scored)[1] != want:
            problems.append(f'layout {doc} p{page}: {item!r} sits under {min(scored)[1]!r}, '
                            f'ledger says {want!r}')
        layout.append({'doc': doc, 'page': page, 'item': item, 'column': want})
    fail(problems)
    checks = {
        'censusLeaves': len(leaves), 'censusLeavesClaimed': len(claimed),
        'atlas': {str(q): {'atlasTopics': v['atlasTopics'], 'taskTopics': sorted(v['taskTopics'])}
                  for q, v in sorted(atlas_view.items())},
        'atlasRule': 'every task topic is a curriculum node of one of its question\'s Topic '
                     'Atlas topics (biology-<year>-exam-topic-map.json via '
                     'biology-curriculum-crosswalk.json)',
        'tickChecksumsMatched': len(ledger.CHECKSUMS),
        **({'layoutChecks': layout} if layout else {}),
        'excluded': excluded,
        **({'openLeaves': open_list} if open_list else {}),
        **({'excludedLeaves': excl_list} if excl_list else {}),
    }
    return lifter, cards, audit_tasks, checks


# ------------------------------------------------------------------ figures --

def figures(ledger, lifter, year, level, write):
    out, records = {}, []
    # Crops render from a freshly opened copy of each PDF: the lifter's copy
    # has had every page's text layer read, and PyMuPDF 1.2x on this machine
    # intermittently crashes building a display list on such a page.
    fresh = {}
    for suffix, spec in ledger.FIGURES.items():
        doc, page, rect, credit, letters, alt, solution = spec[:7]
        masks = spec[7] if len(spec) > 7 else []
        key = f'biology-{year}-{level}-{suffix}'
        src = lifter.srcs[doc]
        if doc not in fresh:
            fresh[doc] = fitz.open(src.path)
        pg = fresh[doc][page - 1]
        clip = fitz.Rect(*rect)
        if not pg.rect.contains(clip):
            raise Refusal(f'{key}: crop {rect} leaves page {page}')
        zoom = 4 if clip.height < 60 else 3
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
        for m in masks:
            mr = fitz.Rect(*m) & clip
            if mr.is_empty:
                raise Refusal(f'{key}: mask {m} is outside the crop')
            # A clipped pixmap keeps page coordinates: its irect starts at the
            # clip's own origin, not at (0, 0).
            ir = fitz.IRect(round(mr.x0 * zoom), round(mr.y0 * zoom),
                            round(mr.x1 * zoom), round(mr.y1 * zoom)) & pix.irect
            pix.set_rect(ir, (255, 255, 255))
        png = pix.tobytes('png')
        rel = f'/exam-figures/biology/markbank/{key}.png'
        level_name = 'Higher' if level == 'hl' else 'Ordinary'
        what = 'marking scheme' if doc == 'scheme' else 'examination paper'
        attribution = f'SEC Leaving Certificate Biology {year} {level_name} Level {what} — © State Examinations Commission'
        if credit != ledger.SEC:
            attribution += f'; source credited in the paper\'s acknowledgements: {credit}'
        entry = {'src': rel, 'md5': hashlib.md5(png).hexdigest(), 'alt': alt,
                 'lettersVisible': letters, 'labelMeanings': [], 'questionRef': None,
                 'year': year, 'level': level_word(level), 'attribution': attribution,
                 'sourceDocument': ledger.SOURCES[doc]['fileid'], 'sourcePage': page,
                 'sourceRect': list(rect)}
        if masks:
            entry['maskedFurniture'] = [list(m) for m in masks]
        if solution:
            entry['solution'] = True
        out[key] = entry
        records.append((key, png))
        if write:
            os.makedirs(FIG_DIR, exist_ok=True)
            with open(os.path.join(FIG_DIR, f'{key}.png'), 'wb') as fh:
                fh.write(png)
    return out, records


# -------------------------------------------------------------------- write --

# Fields a student sees, compared to decide whether a pre-existing card already
# says what the review says. Row ids and the card's own notes are bookkeeping.
COMPARED = ('section', 'questionRef', 'stem', 'questionText', 'tariffModel', 'totalMarks',
            'rows', 'answerVariants', 'topicId', 'figureKey', 'questionFigureKey', 'labelKey',
            'sourceMaterial')


def _seen(card, field):
    v = card.get(field)
    if field == 'rows' and v is not None:
        return [{k: x for k, x in r.items() if k != 'id'} for r in v]
    if field == 'answerVariants' and v is not None:
        return [{**a, 'rows': [{k: x for k, x in r.items() if k != 'id'} for r in a['rows']]}
                for a in v]
    return v


def legacy_cards(ledger, prefix):
    """The sitting's cards as they stood before its review (pinned commit), so
    every re-run measures its corrections against the same original."""
    import subprocess
    raw = subprocess.check_output(['git', 'show', f'{ledger.BASELINE_COMMIT}:'
                                   'scripts/markbank/authored/biology.json'], cwd=ROOT)
    return [c for c in json.loads(raw) if c['id'].startswith(prefix)]


def reconcile_existing(ledger, prefix, cards):
    """Correct a previously carded sitting in place.

    Every pre-existing id survives: a reviewed task that maps to it either
    leaves it exactly as it was (verified) or replaces what a student sees
    (corrected, with the fields it had before recorded); an id no task maps to
    must be declared in RETAINED with its reason. A new task is placed after
    the nearest pre-existing card before it in paper order, so every existing
    card keeps its place in the bank. Returns (replacements, additions,
    record): the card to stand at each existing id, and the new cards to
    insert after each anchor id (None: before the sitting's first card)."""
    legacy = legacy_cards(ledger, prefix)
    by_id = {c['id']: c for c in legacy}
    produced = {c['id']: c for c in cards}
    retained = getattr(ledger, 'RETAINED', {})
    unaccounted = [i for i in by_id if i not in produced and i not in retained]
    if unaccounted:
        raise Refusal(f'pre-existing ids no task maps to and none retained: {unaccounted}')
    clash = [i for i in retained if i in produced]
    if clash:
        raise Refusal(f'ids both retained and produced: {clash}')
    replacements, additions = {}, defaultdict(list)
    record = {'verified': [], 'corrected': [], 'added': [], 'retained': []}
    for old in legacy:
        if old['id'] in retained:
            replacements[old['id']] = old
            record['retained'].append({'id': old['id'], 'questionRef': old['questionRef'],
                                       'reason': retained[old['id']]})
            continue
        new = dict(produced[old['id']])
        changed = [f for f in COMPARED if _seen(old, f) != _seen(new, f)]
        if not changed:
            replacements[old['id']] = old
            record['verified'].append(old['id'])
            continue
        if old.get('conceptId'):
            new['conceptId'] = old['conceptId']
        replacements[old['id']] = new
        dropped = sorted(k for k in old if k not in new and k not in COMPARED and k != 'notes')
        record['corrected'].append({
            'id': old['id'], 'before': {'questionRef': old['questionRef']},
            'after': {'questionRef': new['questionRef']}, 'changed': changed,
            'fieldsBefore': {f: old.get(f) for f in changed + dropped},
            'notesBefore': old.get('notes'),
        })
    anchor = None
    for c in cards:
        if c['id'] in by_id:
            anchor = c['id']
            continue
        additions[anchor].append(c)
        record['added'].append(c['id'])
    return replacements, additions, record


def write_all(ledger, year, level, cards, audit_tasks, figs, lifter, checks):
    prefix = f'bio-{year}-{level}-'
    raw = open(AUTHORED, encoding='utf-8').read()
    bank = json.loads(raw)
    record = None
    if getattr(ledger, 'BASELINE_COMMIT', None):
        replacements, additions, record = reconcile_existing(ledger, prefix, cards)
        status = {i: 'verified' for i in record['verified']}
        status.update({r['id']: 'corrected' for r in record['corrected']})
        status.update({i: 'added' for i in record['added']})
        for t in audit_tasks:
            if t['status'] == 'carded':
                t['status'] = status[t['id']]
    else:
        before = [c['id'] for c in bank if c['id'].startswith(prefix)]
        new_ids = {c['id'] for c in cards}
        lost = [i for i in before if i not in new_ids]
        if lost:
            raise Refusal(f'refusing to drop existing card ids: {lost}')
        block = cards
    if record is not None:
        # Every pre-existing card stays where it stood; new cards follow their
        # anchor. Cards this pipeline added on an earlier run are dropped first.
        out, first = [], True
        for c in bank:
            if c['id'].startswith(prefix) and c['id'] not in replacements:
                continue
            if c['id'] in replacements:
                if first:
                    out.extend(additions.get(None, []))
                    first = False
                out.append(replacements[c['id']])
                out.extend(additions.get(c['id'], []))
            else:
                out.append(c)
        bank = out
    else:
        # The sitting's cards go back where they were (appended when new), so
        # a re-run leaves every other card, and the bank's order, untouched.
        at = next((i for i, c in enumerate(bank) if c['id'].startswith(prefix)), len(bank))
        kept = [c for c in bank if not c['id'].startswith(prefix)]
        at -= sum(1 for c in bank[:at] if c['id'].startswith(prefix))
        bank = kept[:at] + block + kept[at:]
    with open(AUTHORED, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(bank, indent=1, ensure_ascii=False))

    # Pre-existing cards the build never shipped (figure twins superseded by
    # their base card) are withdrawn explicitly, so a corrected base whose
    # questionRef changed cannot expose them.
    withdraw = getattr(ledger, 'WITHDRAW', {})
    if withdraw:
        corr = json.load(open(CORRECTIONS, encoding='utf-8'))
        bio = corr.setdefault('biology', {})
        for wid, (replacement, reason) in withdraw.items():
            bio[wid] = {'reason': reason, 'drop': True, 'replacementId': replacement}
        with open(CORRECTIONS, 'w', encoding='utf-8') as fh:
            json.dump(corr, fh, indent=1, ensure_ascii=False)
            fh.write('\n')

    manifest = {}
    if os.path.exists(FIG_MANIFEST):
        manifest = json.load(open(FIG_MANIFEST, encoding='utf-8'))
    manifest = {k: v for k, v in manifest.items() if not k.startswith(f'biology-{year}-{level}-')}
    for c in cards:
        for field in ('figureKey', 'questionFigureKey'):
            if c.get(field):
                figs[c[field]].setdefault('usedBy', []).append(c['id'])
    unused = [k for k, v in figs.items() if not v.get('usedBy')]
    if unused:
        raise Refusal(f'figures cropped but bound to no card: {unused}')
    for k, v in figs.items():
        v['questionRef'] = sorted({next(c['questionRef'] for c in cards if c['id'] == i)
                                   for i in v['usedBy']})[0]
        v.pop('usedBy')
    manifest.update(figs)
    with open(FIG_MANIFEST, 'w', encoding='utf-8') as fh:
        json.dump(dict(sorted(manifest.items())), fh, indent=1, ensure_ascii=False)
        fh.write('\n')

    audit = {}
    if os.path.exists(AUDIT):
        audit = json.load(open(AUDIT, encoding='utf-8'))
    audit.setdefault('schemaVersion', 1)
    audit.setdefault('subject', 'biology')
    audit.setdefault('sittings', {})
    srcs = {k: {'path': v['path'], 'fileid': v['fileid'], 'sha256': v['sha256'],
                'bytes': lifter.srcs[k].bytes, 'pages': v['pages'],
                'pageRoles': {str(p): r for p, r in ledger.PAGE_ROLES[k].items()},
                'pagesLifted': sorted(lifter.used.get(k, []))}
            for k, v in ledger.SOURCES.items()}
    audit['sittings'][f'{year}-{level}'] = {
        'status': 'reviewed',
        'reviewedAt': getattr(ledger, 'REVIEWED_AT', '2026-10-11'),
        'ledger': f'scripts/markbank/authoring/bio_review_{year}_{level}.py',
        'method': ledger.__doc__.strip().split('\n\n')[0],
        'sources': srcs,
        'visualSweep': {k: f'all {v["pages"]} pages rendered and read' for k, v in ledger.SOURCES.items()},
        'questionTotals': {str(k): v for k, v in ledger.QUESTION_TOTALS.items()},
        'partTotals': {f'{k[0]}{k[1]}': v for k, v in ledger.PART_TOTALS.items()},
        'tickChecksums': {(f'{k[0]}{k[1]}' if isinstance(k, tuple) else str(k)):
                          {str(m): n for m, n in v.items()} for k, v in ledger.CHECKSUMS.items()},
        'selectionScan': [{'doc': d, 'page': p, 'directive': w, 'disposition': r}
                          for d, p, w, r in ledger.SELECTION_SCAN],
        'routes': ledger.ROUTES,
        'tasks': audit_tasks,
        **({'review': {'baselineCommit': ledger.BASELINE_COMMIT, **record,
                       'withdrawn': {k: {'replacementId': v[0], 'reason': v[1]}
                                     for k, v in getattr(ledger, 'WITHDRAW', {}).items()}}}
           if record else {}),
        'cardCount': len(cards),
        'baseTaskCount': len({t['key'] for t in ledger.TASKS}),
        'figures': sorted(figs),
        'checks': checks,
    }
    with open(AUDIT, 'w', encoding='utf-8') as fh:
        json.dump(audit, fh, indent=1, ensure_ascii=False)
        fh.write('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('year', type=int)
    ap.add_argument('level', choices=['hl', 'ol'])
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    ledger = importlib.import_module(f'bio_review_{args.year}_{args.level}')
    try:
        lifter, cards, audit_tasks, checks = build(ledger, args.year, args.level)
        figs, _ = figures(ledger, lifter, args.year, args.level, args.write)
        if args.write:
            write_all(ledger, args.year, args.level, cards, audit_tasks, figs, lifter, checks)
    except Refusal as e:
        print(f'REFUSED {args.year} {args.level}:\n{e}')
        sys.stdout.flush()
        os._exit(1)
    base = len({t['key'] for t in ledger.TASKS})
    print(f'biology {args.year} {args.level}: {base} reviewed tasks -> {len(cards)} cards, '
          f'{len(checks["excluded"])} excluded, {len(figs)} figures'
          + (' (written)' if args.write else ' (check only)'))
    for h in checks['excluded']:
        print(f'  EXCLUDED {h["questionRef"]}: {h["reason"]}')
    for h in checks.get('openLeaves', []):
        print(f'  OPEN {h["leaf"]}: {h["reason"]}')
    for h in checks.get('excludedLeaves', []):
        print(f'  EXCLUDED {h["leaf"]} (no task): {h["reason"]}')
    # Leave without interpreter teardown: PyMuPDF 1.26 on this machine
    # intermittently segfaults freeing its documents at exit, which would turn
    # a finished run's status into 139 after all its work is done.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


if __name__ == '__main__':
    main()
