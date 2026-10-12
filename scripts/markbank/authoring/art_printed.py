#!/usr/bin/env python3
"""Lift the SEC's own Art wording from the printed page.

Every string an audited Art card shows under the SEC's name comes from here:
the descriptor bullets for the short questions and for the four Section B/C
criteria, the scheme's marking notes and each question's scheme row, each with
the page it is printed on. Only the text layer is normalised: Symbol bullets,
whitespace, hyphen code points, and a word broken at a printed hyphen across
two lines. Text the page does not show (white text on an unfilled page, such
as the dot leaders hidden in some scheme rows) is dropped, and the marks table
printed beside the short descriptor is clipped away so it never interleaves
with the bullets.

``printed(path, text)`` is the gate: a string is the SEC's only if it occurs,
so normalised, in the visible text of its own document.
"""
from __future__ import annotations

from functools import lru_cache
import os
import re

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
SCHEME_ROOT = os.path.join(ROOT, 'examiner-reports', 'art', 'schemes')
PAPER_ROOT = os.path.join(ROOT, 'examiner-reports', 'art', 'papers')
LEVEL_SHORT = {'higher': 'hl', 'ordinary': 'ol'}
BULLET = '•'
WHITE = 0xffffff


def clean(text: str) -> str:
    text = text.replace('', BULLET).replace('•', BULLET)
    text = re.sub(r'(\w[‐-])[ \t]*\n\s*(?=\w)', r'\1', text)
    return ' '.join(text.split())


def normal(text: str) -> str:
    """Comparison form: hyphen code points and spacing are layout, not words."""
    text = text.replace('‐', '-').replace('‑', '-').replace('\xa0', ' ')
    return ' '.join(text.split())


def scheme_path(year: int, level: str) -> str:
    return os.path.join(SCHEME_ROOT, f'{year}-{LEVEL_SHORT[level]}.pdf')


def paper_path(year: int, level: str) -> str:
    return os.path.join(PAPER_ROOT, f'{year}-{LEVEL_SHORT[level]}-paper.pdf')


@lru_cache(maxsize=None)
def _open(path: str) -> fitz.Document:
    return fitz.open(path)


def _doc(year: int, level: str) -> fitz.Document:
    return _open(scheme_path(year, level))


def _fills(page: fitz.Page) -> list[fitz.Rect]:
    return [fitz.Rect(d['rect']) for d in page.get_drawings()
            if d.get('fill') and tuple(round(c, 2) for c in d['fill']) != (1.0, 1.0, 1.0)]


def _shown(span: dict, fills: list[fitz.Rect]) -> bool:
    """White text shows only where it is drawn over a coloured fill."""
    if span['color'] != WHITE:
        return True
    rect = fitz.Rect(span['bbox'])
    centre = fitz.Point((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)
    return any(centre in fill for fill in fills)


def visible_words(page: fitz.Page) -> list[tuple]:
    """``get_text('words')`` without words lying inside a hidden span."""
    fills = _fills(page)
    hidden = [fitz.Rect(span['bbox'])
              for block in page.get_text('dict')['blocks']
              for line in block.get('lines', [])
              for span in line['spans']
              if span['text'].strip() and not _shown(span, fills)]

    def shown(word: tuple) -> bool:
        centre = fitz.Point((word[0] + word[2]) / 2, (word[1] + word[3]) / 2)
        return not any(centre in rect for rect in hidden)
    return [word for word in page.get_text('words') if shown(word)]


def words_text(words: list[tuple]) -> str:
    """Words in reading order, one printed line per line, then cleaned."""
    lines: dict[tuple[int, int], list[str]] = {}
    for word in words:
        lines.setdefault((word[5], word[6]), []).append(word[4])
    return clean('\n'.join(' '.join(line) for line in lines.values()))


def visible_lines(page: fitz.Page, clip: fitz.Rect | None = None) -> str:
    """The page's visible characters, one printed line per line, cleaned.

    Character level, because a hidden run can touch a printed word with no
    space between them (the white ".." before "designers" in 2026 OL Q6)."""
    fills = _fills(page)
    lines: list[str] = []
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines', []):
            chars = []
            for span in line['spans']:
                if not _shown(span, fills):
                    continue
                for char in span['chars']:
                    box = fitz.Rect(char['bbox'])
                    centre = fitz.Point((box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)
                    if clip is None or centre in clip:
                        chars.append(char['c'])
            text = ''.join(chars)
            if text.strip():
                lines.append(text)
    return clean('\n'.join(lines))


def cell_text(page: fitz.Page, rect: tuple | fitz.Rect) -> str:
    """The visible text printed inside one table cell."""
    return visible_lines(page, fitz.Rect(rect))


@lru_cache(maxsize=None)
def document_text(path: str) -> str:
    """The visible text of a whole document, normalised for comparison."""
    return normal(' '.join(visible_lines(page) for page in _open(path)))


def printed(path: str, text: str) -> bool:
    return bool(text.strip()) and normal(text) in document_text(path)


TABLE_WORDS = re.compile(r'^(?:Marks?|Low|High|Mod-?|erate|\d+(?:\s*[-–]\s*\d+)?)$')


def page_text(year: int, level: str, page: int, beside_table: bool = False) -> str:
    """The page's visible words in reading order, without its footer number.

    With ``beside_table`` only the words that start left of the marks table
    printed beside the short descriptor are kept, so whole words are never
    cut and the table never interleaves with the bullets."""
    pg = _doc(year, level)[page - 1]
    words = [w for w in visible_words(pg) if w[1] < pg.rect.height * 0.93]
    if beside_table:
        table = [w[0] for w in words if w[0] > pg.rect.width * 0.5 and TABLE_WORDS.match(w[4])]
        assert table, (year, level, page, 'no marks table found')
        edge = min(table) - 1
        words = [w for w in words if w[0] < edge]
    return words_text(words)


def find_page(year: int, level: str, marker: str) -> int:
    pages = [i for i, pg in enumerate(_doc(year, level), start=1) if marker in clean(pg.get_text())]
    assert len(pages) == 1, (year, level, marker, pages)
    return pages[0]


def bullets(block: str) -> list[str]:
    return [item.strip() for item in block.split(BULLET)[1:] if item.strip()]


SHORT_LEAD = 'The response shows evidence of the following where appropriate:'
LONG_LEAD = 'The response shows evidence of:'


def short_descriptors(year: int, level: str) -> dict:
    """The printed 'Descriptor for short questions': its three bullet lists
    (low, moderate, high), lifted from the text column."""
    page = find_page(year, level, 'Descriptor for short questions')
    text = page_text(year, level, page, beside_table=True)
    blocks = text.split(SHORT_LEAD)
    assert len(blocks) == 4, (year, level, page, len(blocks))
    bands = {}
    for level_name, block in zip(('low', 'moderate', 'high'), blocks[1:]):
        items = bullets(block)
        assert items, (year, level, page, level_name)
        bands[level_name] = items
    return {'page': page, 'lead': SHORT_LEAD, 'bands': bands}


LONG_LABELS = ('Coherence and Focus', 'Subject Knowledge', 'Relevant Examples',
               'Visual Language (terminology and/or sketches)')
LONG_IDS = ('coherence-focus', 'subject-knowledge', 'relevant-examples', 'visual-language')


def long_descriptors(year: int, level: str) -> list[dict]:
    """The four printed 'Band Descriptor for Section B and Section C' tables."""
    out = []
    for criterion_id, label in zip(LONG_IDS, LONG_LABELS):
        pages = [i for i, pg in enumerate(_doc(year, level), start=1)
                 if 'Band Descriptor for Section B and Section C' in clean(pg.get_text())
                 and re.search(rf'{re.escape(label)}\.?\s*\d+\s*Marks', clean(pg.get_text()), re.I)]
        assert len(pages) == 1, (year, level, label, pages)
        page = pages[0]
        text = page_text(year, level, page)
        head = re.search(rf'({re.escape(label)})\.?\s*(\d+)\s*Marks\.?', text, re.I)
        bands = {}
        parts = re.split(r'\b(Low|Moderate|High)\s+(\d+\s*[-–]\s*\d+)\s+' + re.escape(LONG_LEAD), text)
        # parts: [pre, name, range, body, name, range, body, ...]
        for index in range(1, len(parts), 3):
            name, marks, body = parts[index].lower(), parts[index + 1], parts[index + 2]
            items = bullets(re.split(r'\s\d{1,2}\s*$', body)[0])
            assert items, (year, level, label, name)
            low, high = (int(x) for x in re.split(r'\s*[-–]\s*', marks))
            bands[name] = {'marks': list(range(low, high + 1)), 'guidance': items}
        assert list(bands) == ['low', 'moderate', 'high'], (year, level, label, list(bands))
        out.append({
            'id': criterion_id,
            'label': head.group(1),
            'maxMarks': int(head.group(2)),
            'page': page,
            'lead': LONG_LEAD,
            'bands': bands,
        })
    return out


# The scheme's own notes on applying each descriptor, printed once per section
# (located by these exact sentences; the gate re-finds each on its page).
NOTES = {
    'current-short-descriptors': (
        'These descriptors should be interpreted in the context of the challenges and demands of the '
        'question the candidate has chosen.',
    ),
    'current-long-descriptors': (
        'Candidates may choose from a wide range of relevant examples and content to answer a question. '
        'Relevant content must be credited.',
        'These descriptors should be interpreted in the context of the challenges and demands of the '
        'question the candidate has chosen.',
    ),
}
NOTE_ANCHORS = {
    'current-short-descriptors': 'Candidates must answer any five questions in this section',
    'current-long-descriptors': 'Candidates must answer one question from this section',
}


def scheme_notes(year: int, level: str) -> dict:
    """Each note with the first page that prints it beside its section's own
    instruction (the short note sits with Section A's, the long notes with
    Section B/C's)."""
    out = {}
    for kind, sentences in NOTES.items():
        anchor = NOTE_ANCHORS[kind]
        pages = [i for i, pg in enumerate(_doc(year, level), start=1)
                 if anchor in normal(visible_lines(pg))
                 and all(normal(s) in normal(visible_lines(pg)) for s in sentences)]
        assert pages, (year, level, kind)
        out[kind] = {'page': pages[0], 'text': list(sentences)}
    return out
