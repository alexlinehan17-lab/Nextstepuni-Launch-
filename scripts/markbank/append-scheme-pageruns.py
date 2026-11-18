#!/usr/bin/env python3
"""
Mark Bank — recover marking points that run across a scheme's PAGE BREAK.

    python3 scripts/markbank/append-scheme-pageruns.py <subject> <year> <hl|ol>

The flat extraction writes a page's footer, and then the next page's first
lines, between the two halves of a paragraph the SEC simply ran on to the next
page. 2021 Higher Engineering answers Q7(b)(i) with a paragraph that breaks
after "Natural rubber has only moderate resistance to damage from exposure to
heat, light and" at the foot of scheme page 20 and resumes "the ozone in the
air." at the head of page 21; between them the markdown holds "Page 19", the
extrusion diagram's callouts and the next page's banner. No marking point that
crosses the break can trace, though the SEC printed every word of it in order.

This reads the PAGE: the paragraph that closes page N -- the run of body lines
up from the last one, at that line's own left margin and ordinary leading --
and the paragraph that opens page N+1, the same way down from its first line.
Where the first does not close a sentence or the second opens lower case, the
two are one paragraph, and the pair is emitted as one line.

APPEND-ONLY, the same safety argument append-scheme-columns.py makes:
comparableScheme() joins every line, so each substring that matches today
still matches afterwards. Nothing is invented -- every emitted line is words
the SEC printed, in the order it printed them.
"""
from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markbank_text import unligature  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- markbank:page-runs -->'
END = '<!-- /markbank:page-runs -->'

LINE_TOL = 3.0          # words within this of a line's top are on that line
MARGIN_TOL = 4.0        # how far a line's left edge may sit from the paragraph's
HEADER = 50.0           # the running head lives above this
FOOTER = 70.0           # and the page footer within this of the foot
# A line that is a tariff or the page's own furniture, not prose: "8",
# "4 + 4", "Any two @ 8 + 8", "Page 19", "(50 Marks)".
FURNITURE = re.compile(r'^(?:\(?\d{1,3}(?:\s*[+@]\s*\d{1,3})*\)?|Page\s+\d+|'
                       r'\(\s*\d{1,3}\s*Marks?\s*\)|Any\s+\w+\s*@.*)$', re.I)
TERMINAL = re.compile(r'[.?!:]\s*$')


def body_lines(page):
    """[(top, x0, text)] for the page's printed lines, furniture dropped."""
    words = [w for w in page.get_text('words') if w[4].strip()]
    words.sort(key=lambda w: (round(w[1], 1), w[0]))
    lines, cur, top = [], [], None
    for w in words:
        if cur and abs(w[1] - top) > LINE_TOL:
            lines.append((top, cur))
            cur = []
        if not cur:
            top = w[1]
        cur.append(w)
    if cur:
        lines.append((top, cur))
    out = []
    for top, ws in lines:
        ws.sort(key=lambda w: w[0])
        text = ' '.join(w[4] for w in ws)
        if top < HEADER or top > page.rect.height - FOOTER:
            continue
        if FURNITURE.match(text.strip()):
            continue
        out.append((top, ws[0][0], text))
    return out


def _step(lines):
    gaps = [b[0] - a[0] for a, b in zip(lines, lines[1:]) if 0 < b[0] - a[0] < 40]
    return statistics.median(gaps) if gaps else 15.0


def tail_paragraph(lines):
    if not lines:
        return []
    step = _step(lines)
    margin = lines[-1][1]
    para = [lines[-1]]
    for ln in reversed(lines[:-1]):
        if abs(ln[1] - margin) > MARGIN_TOL or para[0][0] - ln[0] > step * 1.6:
            break
        para.insert(0, ln)
    return para


def head_paragraph(lines):
    if not lines:
        return []
    step = _step(lines)
    margin = lines[0][1]
    para = [lines[0]]
    for ln in lines[1:]:
        if abs(ln[1] - margin) > MARGIN_TOL or ln[0] - para[-1][0] > step * 1.6:
            break
        para.append(ln)
    return para


def page_runs(pdf: Path) -> list[str]:
    out = []
    with pymupdf.open(pdf) as doc:
        pages = [body_lines(p) for p in doc]
    for here, there in zip(pages, pages[1:]):
        tail, head = tail_paragraph(here), head_paragraph(there)
        if not tail or not head:
            continue
        last, first = tail[-1][2].strip(), head[0][2].strip()
        if TERMINAL.search(last) and not first[:1].islower():
            continue
        text = ' '.join(t for _, _, t in tail + head)
        text = unligature(re.sub(r'\s+', ' ', text).strip())
        if len(text) >= 24:
            out.append(text)
    return out


def apply(subject: str, year: int, level: str) -> None:
    md = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.md'
    pdf = md.with_suffix('.pdf')
    if not md.exists() or not pdf.exists():
        raise SystemExit(f'no scheme markdown and PDF at {md.with_suffix("")}')
    lines = page_runs(pdf)
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    text = md.read_text(encoding='utf-8')
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', text, flags=re.S)
    md.write_text(text.rstrip('\n') + '\n\n' + body, encoding='utf-8')
    print(f'{subject} {year} {level}: appended {len(lines)} page runs to {md.name}')


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(__doc__.strip().splitlines()[2].strip())
    apply(sys.argv[1], int(sys.argv[2]), sys.argv[3])


if __name__ == '__main__':
    main()
