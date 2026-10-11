#!/usr/bin/env python3
"""Shared machinery for independently reviewed Geography sittings.

A reviewed sitting is described by a hand-written ledger module
(``geography_review_<year>_<hl|ol>.py``) recording, for every separately
priced task, the printed boundary, the published tariff, the canonical topic,
the Topic Atlas topics, the official sources the task needs and every finite
printed route. The ledger never types examination wording: it names VERBATIM
anchors, and this module lifts the question text from the question paper and
the marking guidance from the marking scheme between those anchors. A missing
or ambiguous anchor, a tariff that no scheme line prints, a criterion total
that does not equal the printed task tariff, or a task total that does not
equal the paper's printed question tariff stops generation.
"""

from __future__ import annotations

import hashlib
import itertools
import os
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

import fitz


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'geography', 'papers')
SCHEME_ROOT = os.path.join(ROOT, 'examiner-reports', 'geography', 'schemes')
CORPUS_ROOT = os.path.join(ROOT, 'paper-trail-corpus', 'exampapers')

LEVEL_SHORT = {'higher': 'hl', 'ordinary': 'ol'}
LEVEL_REF = {'higher': 'HL', 'ordinary': 'OL'}

# Symbol-font glyphs the SEC PDFs use for ticks and bullets. They are mapped
# to their printed meaning, never deleted, so "ticking (✓)" survives.
GLYPHS = {
    '': '✓', '': '•', '': '•', '': '•', '': '•',
    '­': '', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl',
    'ﬃ': 'ffi', 'ﬄ': 'ffl', '\xa0': ' ', ' ': ' ',
    ' ': ' ', '‐': '-', '‑': '-', '‒': '-', '−': '-',
}


def clean(value: str) -> str:
    for bad, good in GLYPHS.items():
        value = value.replace(bad, good)
    return value


def compact(value: str) -> str:
    return re.sub(r'\s+', ' ', clean(value)).strip()


def sha256(path: str) -> str:
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def slug(value: str, limit: int = 72) -> str:
    value = unicodedata.normalize('NFKD', value)
    value = ''.join(char for char in value if not unicodedata.combining(char))
    value = value.lower().replace('’', '').replace("'", '')
    value = re.sub(r'[^a-z0-9]+', '-', value).strip('-')
    return value[:limit].rstrip('-') or 'route'


class Document:
    """One SEC PDF read as compacted page text and as printed lines."""

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise AssertionError(f'missing source PDF {os.path.relpath(path, ROOT)}')
        self.path = path
        self.doc = fitz.open(path)
        self._text: dict[int, str] = {}

    def __len__(self) -> int:
        return len(self.doc)

    def page_text(self, page: int) -> str:
        if page not in self._text:
            self._text[page] = compact(self.doc[page - 1].get_text('text', sort=True))
        return self._text[page]

    def lift(self, page: int, start: str, end: str | None = None,
             nth: int | None = None) -> str:
        """The printed text from ``start`` through ``end`` (both inclusive).

        ``nth`` picks one occurrence of an anchor the page prints more than
        once; without it the anchor must be unique on the page."""
        text = self.page_text(page)
        start = compact(start)
        hits = [m.start() for m in re.finditer(re.escape(start), text)]
        if nth is None and len(hits) != 1:
            raise AssertionError(
                f'{os.path.basename(self.path)} p{page}: start anchor {start!r} '
                f'found {len(hits)} times')
        if nth is not None and len(hits) <= nth:
            raise AssertionError(
                f'{os.path.basename(self.path)} p{page}: start anchor {start!r} '
                f'has no occurrence {nth}')
        begin = hits[nth or 0]
        if end is None:
            return text[begin:begin + len(start)]
        end = compact(end)
        stop = text.find(end, begin)
        if stop < 0:
            raise AssertionError(
                f'{os.path.basename(self.path)} p{page}: end anchor {end!r} '
                f'not found after {start!r}')
        return text[begin:stop + len(end)]

    def lines(self, page: int, clip: tuple[float, float, float, float] | None = None
              ) -> list[str]:
        """Printed lines in reading order, with same-baseline cells joined and
        wrapped bullet continuations folded into their bullet."""
        pdf_page = self.doc[page - 1]
        rect = None
        if clip is not None:
            w, h = pdf_page.rect.width, pdf_page.rect.height
            rect = fitz.Rect(clip[0] * w, clip[1] * h, clip[2] * w, clip[3] * h)
        fragments: list[tuple[float, float, float, str]] = []
        for block in pdf_page.get_text('dict', clip=rect)['blocks']:
            for line in block.get('lines', ()):
                text = clean(''.join(span['text'] for span in line['spans']))
                if text.strip():
                    fragments.append((line['bbox'][1], line['bbox'][0],
                                      line['bbox'][3], text))
        fragments.sort()
        rows: list[list[Any]] = []
        for top, left, bottom, text in fragments:
            if rows and abs(rows[-1][0] - top) <= 2.5:
                rows[-1][2].append((left, text))
                rows[-1][3] = max(rows[-1][3], bottom)
            else:
                rows.append([top, left, [(left, text)], bottom])
        out: list[tuple[float, float, float, str, bool]] = []
        for top, _left, cells, bottom in rows:
            cells.sort()
            # A wrapped line is sometimes set at the bullet's x with leading
            # spaces standing in for the indent.
            padded = bool(re.match(r'^ {3,}\S', cells[0][1]))
            # Separate printed cells of one row (an allocation and its marks)
            # with a visible divider; the words of each cell are untouched.
            joined = ' · '.join(c for c in (compact(text) for _, text in cells) if c)
            # A bullet glyph set as its own cell belongs to the text beside it.
            joined = re.sub(r'^• · ', '• ', joined)
            if joined:
                out.append((cells[0][0], top, bottom, joined, padded))
        merged: list[str] = []
        bullet_x: float | None = None
        last_bottom = 0.0
        for left, top, bottom, text, padded in out:
            if text.startswith('•'):
                bullet_x = left
                merged.append(text)
            elif (bullet_x is not None and merged and merged[-1].startswith('•')
                  and (bullet_x + 8 <= left <= bullet_x + 40
                       or (padded and abs(left - bullet_x) < 4))
                  and top - last_bottom < 9
                  and not re.fullmatch(r'\[\d+m\]|\d{1,2}', text)):
                # A wrapped bullet continues at the text indent, directly
                # below; a table or page number after a gap is not part of it.
                merged[-1] = f'{merged[-1]} {text}'
            else:
                bullet_x = None
                merged.append(text)
            last_bottom = bottom
        return merged

    def table_lines(self, page: int, start: str) -> list[str]:
        """Rows of the ruled table whose first row holds ``start``."""
        start = compact(start)
        found = []
        for table in self.doc[page - 1].find_tables().tables:
            rows = [[compact(cell or '') for cell in row] for row in table.extract()]
            if rows and start in ' '.join(rows[0]):
                found.append([' · '.join(cell for cell in row if cell) for row in rows])
        if len(found) != 1:
            raise AssertionError(
                f'{os.path.basename(self.path)} p{page}: table {start!r} found {len(found)}')
        return [row for row in found[0] if row]

    def line_slice(self, page: int, start: str, end: str | None,
                   clip: tuple[float, float, float, float] | None = None,
                   after: str | None = None) -> list[str]:
        """Printed lines from the one holding ``start`` up to (excluding) the
        first later line holding ``end``; to the page foot when ``end`` is None.

        ``after`` scopes the search to lines after a unique block heading, for
        a scheme that prints the same allocation line under several questions."""
        lines = self.lines(page, clip)
        start = compact(start)
        offset = 0
        if after is not None:
            heads = [i for i, line in enumerate(lines) if compact(after) in line]
            if len(heads) != 1:
                raise AssertionError(
                    f'{os.path.basename(self.path)} p{page}: block {after!r} '
                    f'in {len(heads)} lines')
            offset = heads[0]
        hits = [i for i, line in enumerate(lines) if i >= offset and start in line]
        if not hits or (after is None and len(hits) != 1):
            raise AssertionError(
                f'{os.path.basename(self.path)} p{page}: scheme start {start!r} '
                f'in {len(hits)} lines')
        first = hits[0]
        if end is None:
            last = len(lines)
        else:
            end = compact(end)
            later = [i for i in range(first + 1, len(lines)) if end in lines[i]]
            if not later:
                raise AssertionError(
                    f'{os.path.basename(self.path)} p{page}: scheme end {end!r} '
                    f'not found after {start!r}')
            last = later[0]
        out = lines[first:last]
        # Page furniture: a bare printed page number is never guidance.
        return [line for line in out if not re.fullmatch(r'\d{1,2}', line)]


@dataclass(frozen=True)
class Lift:
    """A verbatim span of the question paper."""
    page: int
    start: str
    end: str | None = None
    booklet: int | None = None
    nth: int | None = None


@dataclass(frozen=True)
class SchemeSlice:
    page: int
    start: str
    end: str | None
    clip: tuple[float, float, float, float] | None = None
    after: str | None = None
    table: bool = False


@dataclass(frozen=True)
class Criterion:
    label: str
    max: int
    permitted: tuple[int, ...]
    kind: str  # 'exact' | 'srp'
    lines: tuple[str, ...]  # anchors; each must hit exactly one sliced scheme line


@dataclass(frozen=True)
class Route:
    slug: str
    label: str
    card_id: str
    legacy: bool
    replace: tuple[tuple[str, str], ...] = ()
    keep_bullets: tuple[str, ...] | None = None
    prompt: tuple[Lift, ...] | None = None
    scheme: tuple[SchemeSlice, ...] | None = None
    criteria: tuple[Criterion, ...] | None = None
    topic: str | None = None
    atlas: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Task:
    key: str
    part: int
    question: str           # printed number: '2', '2B', '13'
    sub: str                # printed part address: '', '(i)', '(ii)(a)'
    marks: int
    page: int               # paper page holding the ask
    title: Lift
    prompt: tuple[Lift, ...]
    scheme: tuple[SchemeSlice, ...]
    criteria: tuple[Criterion, ...]
    topic: str
    atlas: tuple[str, ...]
    sources: tuple[str, ...]
    card_id: str
    legacy: bool
    stem: tuple[Lift, ...] = ()
    routes: tuple[Route, ...] = ()
    row_labels: tuple[Lift | None, ...] = ()
    note: str = ''


def evens(maximum: int, step: int = 2) -> tuple[int, ...]:
    return tuple(range(0, maximum + 1, step))


def upto(maximum: int) -> tuple[int, ...]:
    return tuple(range(0, maximum + 1))


def srp(label: str, count: int, line: str | Sequence[str], value: int = 2) -> Criterion:
    lines = (line,) if isinstance(line, str) else tuple(line)
    return Criterion(label, count * value, evens(count * value, value), 'srp', lines)


def fixed(label: str, marks: int, line: str | Sequence[str],
          permitted: Sequence[int] | None = None, kind: str = 'exact') -> Criterion:
    lines = (line,) if isinstance(line, str) else tuple(line)
    return Criterion(label, marks, tuple(permitted) if permitted else (0, marks), kind, lines)


def ref_label(year: int, level: str, task: Task) -> str:
    return f'{year} {LEVEL_REF[level]} Part {task.part} Q{task.question}{task.sub}'


@dataclass
class Sitting:
    year: int
    level: str
    papers: dict[int, Document]
    scheme: Document

    @classmethod
    def open(cls, year: int, level: str) -> 'Sitting':
        short = LEVEL_SHORT[level]
        return cls(
            year=year, level=level,
            papers={part: Document(os.path.join(
                PAPER_ROOT, f'{year}-{short}-04{part + 1}-paper.pdf')) for part in (1, 2)},
            scheme=Document(os.path.join(SCHEME_ROOT, f'{year}-{short}.pdf')),
        )

    def lift(self, part: int, item: Lift) -> str:
        return self.papers[item.booklet or part].lift(
            item.page, item.start, item.end, item.nth)

    def scheme_lines(self, piece: SchemeSlice) -> list[str]:
        if piece.table:
            return self.scheme.table_lines(piece.page, piece.start)
        return self.scheme.line_slice(
            piece.page, piece.start, piece.end, piece.clip, piece.after)


def display(text: str) -> str:
    """Restore the paper's line structure for bullets and lettered items."""
    text = re.sub(r'\s*•\s*', '\n• ', text)
    text = re.sub(r'\s+(?=\((?:a|b|c|d)\)\s)', '\n', text)
    return text.strip()


def build_task_cards(sitting: Sitting, task: Task, fileid: str,
                     companions: dict[str, dict[str, Any]],
                     topic_ids: set[str]) -> list[dict[str, Any]]:
    """Every practice card for one reviewed task (one per finite route)."""
    year, level = sitting.year, sitting.level
    title = sitting.lift(task.part, task.title)
    stem_parts = [sitting.lift(task.part, item) for item in task.stem]
    def prompt_for(items: Sequence[Lift]) -> str:
        return '\n'.join(display(sitting.lift(task.part, item)) for item in items)
    if task.marks <= 0:
        raise AssertionError(f'{task.key}: no tariff')
    routes = task.routes or (Route('', '', task.card_id, task.legacy),)
    if task.routes and task.routes[0].card_id != task.card_id:
        raise AssertionError(f'{task.key}: the first route must keep the task id')
    cards = []
    for route in routes:
        text = prompt_for(route.prompt or task.prompt)
        for old, new in route.replace:
            if text.count(old) != 1:
                raise AssertionError(f'{task.key} {route.slug}: route text {old!r} '
                                     f'found {text.count(old)} times')
            text = text.replace(old, new)
        if route.keep_bullets is not None:
            bullets = [line for line in text.splitlines() if line.startswith('• ')]
            keep = [f'• {item}' for item in route.keep_bullets]
            if not set(keep) <= set(bullets):
                raise AssertionError(f'{task.key} {route.slug}: {keep} not in {bullets}')
            text = '\n'.join(line for line in text.splitlines()
                             if not line.startswith('• ') or line in keep)
        scheme_slices = route.scheme or task.scheme
        lines: list[str] = []
        for piece in scheme_slices:
            lines.extend(sitting.scheme_lines(piece))
        criteria = route.criteria or task.criteria
        if sum(c.max for c in criteria) != task.marks:
            raise AssertionError(
                f'{task.key} {route.slug}: criteria total '
                f'{sum(c.max for c in criteria)} != printed tariff {task.marks}')
        used: set[int] = set()
        criteria_out = []
        row_labels = [None if item is None else sitting.lift(task.part, item)
                      for item in task.row_labels]
        if row_labels and len(row_labels) != len(criteria):
            raise AssertionError(f'{task.key}: {len(row_labels)} printed rows for '
                                 f'{len(criteria)} scheme rows')
        for index, criterion in enumerate(criteria, start=1):
            if (min(criterion.permitted) != 0 or max(criterion.permitted) != criterion.max
                    or len(set(criterion.permitted)) != len(criterion.permitted)):
                raise AssertionError(f'{task.key}: bad permitted marks for {criterion.label}')
            guidance = []
            for anchor in criterion.lines:
                # '=' demands the whole printed line, for a line that is also
                # a substring of its neighbour ("2 + 2 marks"); '?' marks a
                # heading only some of the scheme's pages print.
                optional = anchor.startswith('?')
                anchor = anchor.lstrip('?')
                if anchor.startswith('='):
                    hits = [i for i, line in enumerate(lines) if line == compact(anchor[1:])]
                else:
                    hits = [i for i, line in enumerate(lines) if compact(anchor) in line]
                if optional and not hits:
                    continue
                if len(hits) != 1:
                    raise AssertionError(
                        f'{task.key} {route.slug}: criterion line {anchor!r} '
                        f'hit {len(hits)} scheme lines in {lines!r}')
                used.add(hits[0])
                guidance.append(lines[hits[0]])
            label = (row_labels[index - 1] if row_labels and row_labels[index - 1]
                     else criterion.label)
            criteria_out.append({
                'id': f'c{index}',
                'label': label,
                'maxMarks': criterion.max,
                'permittedMarks': list(criterion.permitted),
                'guidanceKind': criterion.kind,
                'guidance': guidance,
            })
        directions = [line for i, line in enumerate(lines) if i not in used
                      and not re.fullmatch(r'\[\d+m\]', line)]
        topic = route.topic or task.topic
        topic_id = f'geography-{topic}'
        if topic_id not in topic_ids:
            raise AssertionError(f'{task.key}: unknown canonical topic {topic_id}')
        atlas = list(route.atlas or task.atlas)
        if not atlas:
            raise AssertionError(f'{task.key}: no Topic Atlas topic')
        sources = []
        for source in task.sources:
            if source == 'page':
                sources.append({
                    'kind': 'source-illustration',
                    'label': f'PART {task.part} · Q{task.question}',
                    'title': 'Official question page',
                    'pages': [task.page],
                    'attribution': (
                        f'State Examinations Commission Geography {LEVEL_REF[level]} '
                        f'question paper {year} — © State Examinations Commission.'),
                    'presentationNote': (
                        'Official examination layout, reproduced page-for-page so every '
                        'printed map, chart, photograph and source remains in context.'),
                })
            else:
                sources.append(dict(companions[source]))
        ref = ref_label(year, level, task)
        kinds = {c['guidanceKind'] for c in criteria_out}
        card: dict[str, Any] = {
            'id': route.card_id,
            'year': year,
            'level': level,
            'part': task.part,
            'questionRef': ref if not route.label else f'{ref} · {route.label}',
            'stem': ' — '.join([title, ' '.join(stem_parts)]) if stem_parts else title,
            'questionText': text,
            'paperPage': task.page,
            'paperFileid': fileid,
            'totalMarks': task.marks,
            'schemePage': scheme_slices[0].page,
            'topicId': topic_id,
            'conceptId': f'geography-{topic}-{slug(title, 40)}'
                         + (f'-{slug(task.sub, 12)}' if task.sub else '')
                         + (f'-{route.slug}' if route.slug else ''),
            'taskRequirements': ([f'Use the printed route: {route.label}.']
                                 if route.label else []),
            'guidanceKind': 'srp' if 'srp' in kinds else 'exact',
            'schemeGuidance': [line for c in criteria_out for line in c['guidance']],
            'criteria': criteria_out,
            'directions': directions,
            'atlasTopicIds': atlas,
            'reviewed': True,
        }
        if sources:
            card['sourceMaterial'] = sources[0]
        if len(sources) > 1:
            card['additionalSourceMaterials'] = sources[1:]
        cards.append(card)
    return cards


SELECTION_PATTERN = re.compile(
    r'\banswer\s+\(i\)\s+or\s+\(ii\)|'
    r'\b(?:any\s+(?:one|two|three|four|ten|\d+)|'
    r'(?:one|two|three|four)\s+of\s+the\s+following|either|choose|'
    r'or\s+one|attempt\s+(?:any\s+)?\w+)\b', re.I)


def selection_scan(sitting: Sitting) -> list[list[Any]]:
    """Every raw selection directive on every page of both booklets."""
    out = []
    for part, document in sitting.papers.items():
        for page in range(1, len(document) + 1):
            for match in SELECTION_PATTERN.finditer(document.page_text(page)):
                out.append([part, page, match.group(0).lower()])
    return out
