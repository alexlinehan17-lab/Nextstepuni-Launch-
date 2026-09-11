#!/usr/bin/env python3
"""
Mark Bank — the Japanese scheme as a reader of Japanese sees it.

    python3 scripts/markbank/append-scheme-furigana.py japanese 2024 hl
    python3 scripts/markbank/append-scheme-furigana.py --all

The flat extraction reads a page line by line, and a Japanese scheme page has
TWO layers of type on most of its lines: the text, and the furigana the SEC
sets in small kana above the kanji it glosses. Read flat they interleave —

    ポッキーの歴史
    れきし

— so a card quoting what the scheme prints, 歴史（れきし）, matches nothing and
is dropped as untraceable even though the SEC printed it exactly.

`ja_text.page_rows` folds each ruby run back into the character it was centred
over. This appends that rendering of every page, so the provenance gate holds
BOTH: the flat one, which is what every Latin-script card is checked against,
and the folded one, which is what a Japanese card quotes.

APPEND-ONLY, and that is the whole safety argument, the same one
append-scheme-columns.py makes: comparableScheme() joins every line, so each
substring that matches today still matches afterwards. No card that passes can
start failing. Nothing is invented either — every emitted character is one the
SEC printed, in the order its own page reads.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'authoring'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pymupdf                                                  # noqa: E402
from ja_text import page_rows                                   # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- markbank:furigana-folded -->'
END = '<!-- /markbank:furigana-folded -->'


def folded(pdf: Path) -> list[str]:
    out = []
    with pymupdf.open(pdf) as doc:
        for page in doc:
            for groups in page_rows(page):
                line = ' '.join(t for _x0, _x1, t in groups).strip()
                if line:
                    out.append(line)
    return out


def apply(subject: str, year: int, level: str) -> None:
    md = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.md'
    pdf = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.pdf'
    if not md.exists():
        raise SystemExit(f'no scheme markdown at {md}')
    if not pdf.exists():
        raise SystemExit(f'no marking-scheme PDF at {pdf}')
    lines = folded(pdf)
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    text = md.read_text(encoding='utf-8')
    # Re-running replaces the block rather than stacking another, so this is
    # idempotent and the diff of a re-run shows only what actually changed.
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '',
                      text, flags=re.S)
    md.write_text(text.rstrip('\n') + '\n\n' + body, encoding='utf-8')
    print(f'{subject} {year} {level}: appended {len(lines)} folded line(s)')


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ['--all']:
        for md in sorted((ROOT / 'examiner-reports' / 'japanese' / 'schemes')
                         .glob('*.md')):
            year, level = md.stem.split('-')
            apply('japanese', int(year), level)
        return
    if len(args) < 3:
        raise SystemExit(__doc__.strip().splitlines()[2].strip())
    apply(args[0], int(args[1]), args[2])


if __name__ == '__main__':
    main()
