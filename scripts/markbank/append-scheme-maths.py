#!/usr/bin/env python3
"""
Mark Bank — recover the pages whose equations the span reader doubles.

    python3 scripts/markbank/append-scheme-maths.py <subject> <year> <hl|ol>
    python3 scripts/markbank/append-scheme-maths.py --all

extract-scheme.py reads a page span by span, because that is the only way to
measure the gap between two spans and tell a word split across them ("propagat
ion") from two real words. On a page set with the SEC's equation editor that
reader returns every character of the formula TWICE:

    span text : 𝟏𝟏𝟏𝟏𝟏𝟏 = 0.015 moles (CH2)n(COOH)2
    printed   : 118

118 becomes "111111" and 2.43 becomes "22.4444", so no card can quote the
working the scheme prices. PyMuPDF's plain text reader gets the same page right;
it is only the span reader that doubles. So the pages carrying equations are
read again the plain way and appended.

Append-only, the same argument append-scheme-tables.py and
append-scheme-columns.py make: comparableScheme() joins every line, so nothing
that matches today can stop matching. And the primary extraction is left exactly
as it is — it is the ground truth the schemes were converted with, and rewriting
it wholesale to fix a hundred pages would put every other page at risk.

Only pages whose spans actually carry Mathematical Alphanumeric characters are
appended: 102 of 1,874 across the six Mark Bank subjects.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markbank_text import unligature  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- markbank:maths-pages -->'
END = '<!-- /markbank:maths-pages -->'

# The Mathematical Alphanumeric Symbols block. Its presence in a SPAN is what
# marks a page as set with the equation editor.
MATHS = re.compile(r'[\U0001D400-\U0001D7FF]')

# A tariff stranded at the head of a line, e.g. "(3)" or "[3 + 3]". Left in, the
# line takes the shape test/markBankSchemes.test.ts refuses, because a bracketed
# label introducing prose is how an agent narrating a figure writes.
LEADING_TARIFF = re.compile(r'^(?:\[[^\]]*\]|⟨[^⟩]*⟩|\((?:\d+[^)]*)\))\s*')


def maths_lines(pdf: Path) -> list[str]:
    doc = pymupdf.open(pdf)
    out, seen = [], set()
    for page in doc:
        spans = ''.join(
            s['text']
            for b in page.get_text('dict')['blocks'] if b.get('type') == 0
            for line in b['lines'] for s in line['spans']
        )
        if not MATHS.search(spans):
            continue
        for raw in page.get_text().split('\n'):
            text = LEADING_TARIFF.sub('', unligature(re.sub(r'\s+', ' ', raw).strip())).strip()
            # A line of pure marks or a lone label carries no marking point, and
            # comparableScheme drops those lines anyway.
            if len(text) < 6 or text in seen:
                continue
            seen.add(text)
            out.append(text)
    doc.close()
    return out


def pdf_for(subject: str, year: int, level: str) -> Path | None:
    """The marking-scheme PDF for exactly this subject, year and level.

    Same resolution as append-scheme-columns.py, and for the same reason: the
    bare `<year>-marking-scheme.pdf` name is sometimes a DEFERRED paper, whose
    answers belong to a different exam.
    """
    d = ROOT / 'examiner-reports' / subject
    # schemes/<year>-<level>.pdf FIRST: that is where fetch-corpus.py puts every
    # scheme, it is explicitly levelled, and the fetcher never pulls a deferred
    # paper. Without it a newly fetched subject silently got no folds at all —
    # Construction Studies folded 2 of its 10 schemes and reported the other
    # eight as "no PDF, skipped", which reads like nothing needed doing.
    names = ([f'{year}-{level}-marking-scheme.pdf'] if level == 'ol'
             else [f'{year}-hl-marking-scheme.pdf', f'{year}-marking-scheme.pdf'])
    # LAST, never first: schemes/<year>-<level>.pdf is where fetch-corpus.py
    # puts every scheme, so a newly fetched subject has only this copy and
    # without it gets no folds at all — Construction Studies folded 2 of its 10
    # and reported the rest as "no PDF, skipped", which reads like nothing
    # needed doing. Preferring it would have been worse: the two copies are not
    # byte-identical, and re-running rewrote the fold blocks under all seven
    # shipped subjects, which is provenance every shipped card traces against.
    names.append(f'schemes/{year}-{level}.pdf')
    for name in names:
        path = d / name
        if not path.exists():
            continue
        with pymupdf.open(path) as doc:
            cover = ' '.join(doc[0].get_text().split())
        if 'Deferred' in cover:
            continue
        if ('Ordinary Level' if level == 'ol' else 'Higher Level') not in cover:
            continue
        return path
    return None


def apply(subject: str, year: int, level: str) -> None:
    md = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.md'
    if not md.exists():
        raise SystemExit(f'no scheme markdown at {md}')
    pdf = pdf_for(subject, year, level)
    if pdf is None:
        raise SystemExit(f'no marking-scheme PDF for {subject} {year} {level}')
    lines = maths_lines(pdf)
    text = md.read_text(encoding='utf-8')
    # Re-running replaces the block rather than stacking another.
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', text, flags=re.S)
    if not lines:
        md.write_text(text.rstrip('\n') + '\n', encoding='utf-8')
        print(f'{subject} {year} {level}: no equation pages')
        return
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    md.write_text(text.rstrip('\n') + '\n\n' + body, encoding='utf-8')
    print(f'{subject} {year} {level}: appended {len(lines)} lines from equation pages')


def main() -> None:
    if sys.argv[1:2] == ['--all']:
        for md in sorted((ROOT / 'examiner-reports').glob('*/schemes/*.md')):
            subject = md.parents[1].name
            year, level = md.stem.split('-')
            if pdf_for(subject, int(year), level) is None:
                print(f'{subject} {year} {level}: no PDF, skipped')
                continue
            apply(subject, int(year), level)
        return
    if len(sys.argv) < 4:
        raise SystemExit('usage: append-scheme-maths.py <subject> <year> <hl|ol>')
    apply(sys.argv[1], int(sys.argv[2]), sys.argv[3])


if __name__ == '__main__':
    main()
