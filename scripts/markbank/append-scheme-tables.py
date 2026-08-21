#!/usr/bin/env python3
"""
Mark Bank — recover table cells that the flat scheme extraction loses.

    python3 scripts/markbank/append-scheme-tables.py <subject> <year> <hl|ol>

SEC schemes lay marking points out in tables, and the extracted markdown reads
them ACROSS the row: a card that correctly pairs "Runners" with its example
"(strawberries)" fails provenance, because the markdown puts three other methods
between them. Same for stacked fractions and isotope notation. This is the
single largest cause of dropped cards outside Home Economics.

The cells are recoverable -- PyMuPDF's find_tables() reads them with the columns
intact. This APPENDS them to the scheme markdown rather than replacing the flat
text, and that choice is the whole safety argument: comparableScheme() joins all
lines, so every substring that matches today still matches afterwards. A card
that passes cannot start failing. Only claims that span a column boundary gain a
match they should always have had.

Nothing is invented: every appended line is text the SEC printed, read out of
its own cell. Re-running replaces the block, so it is idempotent.

MEASURED 2026-08-21, and the result is why this is a tool rather than something
already applied. Run across every scheme whose PDF is in the repo, it recovered
ONE card. The cells become traceable -- "sublevel: 2p" and "orbital: e.g. 2px"
both match afterwards where neither did before -- but the cards that fail do not
quote a cell. They quote a PAIRING the author composed across two cells
("sublevel: 2p; orbital: e.g. 2px"), and only 2 of 133 failing claims are joins
whose every part matches. So the remaining ~95 dropped cards need genuine
re-authoring against the scheme, not a mechanical fix.

Run this at the point someone authors those questions -- 27,000 appended lines
across nine ground-truth scheme files is not worth carrying for one card.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from markbank_text import unligature  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
START = '<!-- markbank:table-cells -->'
END = '<!-- /markbank:table-cells -->'


def pdf_for(subject: str, year: int, level: str) -> Path | None:
    """The marking-scheme PDF for exactly this subject, year and level.

    The explicitly-levelled name is preferred over the bare one, and a Deferred
    Examinations cover is refused outright. Both matter: examiner-reports holds
    biology/2023-marking-scheme.pdf, which is the DEFERRED Higher Level paper —
    a different exam with different answers — alongside the real 2023-hl one.
    Preferring the bare name appended the deferred paper's marking points to the
    main paper's scheme text, where they would let a card trace to wording the
    paper it cites never printed. That is the one thing the provenance gate
    exists to stop.
    """
    d = ROOT / 'examiner-reports' / subject
    names = ([f'{year}-{level}-marking-scheme.pdf'] if level == 'ol'
             else [f'{year}-hl-marking-scheme.pdf', f'{year}-marking-scheme.pdf'])
    for name in names:
        path = d / name
        if not path.exists():
            continue
        with pymupdf.open(path) as doc:
            cover = ' '.join(doc[0].get_text().split())
        if 'Deferred' in cover:
            continue
        want = 'Ordinary Level' if level == 'ol' else 'Higher Level'
        if want not in cover:
            continue
        return path
    return None


def cells(pdf: Path) -> list[str]:
    doc = pymupdf.open(pdf)
    out, seen = [], set()
    for page in doc:
        # "lines" only sees ruled tables; SEC schemes align most of theirs with
        # whitespace alone, which only "text" detects -- 4026 cells against 126
        # on the 2024 chemistry scheme. Both are used and the results deduped.
        tables = []
        for strategy in ('lines', 'text'):
            try:
                tables += page.find_tables(strategy=strategy).tables
            except Exception:
                continue
        for table in tables:
            try:
                data = table.extract()
            except Exception:
                continue
            width = max((len(r) for r in data), default=0)
            # Every cell on its own...
            for row in data:
                for cell in row:
                    if not cell:
                        continue
                    # The PDF font encodes ligatures as glyphs like "Ɵ" for
                    # "ti", so "letters" extracts as "leƩers". extract-scheme.py
                    # folds these; anything appended here has to as well, or the
                    # mangled form lands in a shipped marking point.
                    text = unligature(re.sub(r'\s+', ' ', cell).strip())
                    # A cell of pure marks or a lone label carries no marking
                    # point, and comparableScheme drops those lines anyway.
                    if len(text) < 3 or text in seen:
                        continue
                    seen.add(text)
                    out.append(text)
            # ...and each column's consecutive run rejoined. A cell whose text
            # wraps is extracted as several rows -- "Celebrity" / "Endorsements
            # /Social Media" / "Influencers" is ONE marking point split three
            # ways -- so the run is emitted joined as well. Continuation rows
            # are the ones where this is the only column carrying anything.
            for col in range(width):
                run = []
                for row in data:
                    # A wholly empty row is layout, not a break in the record --
                    # the text strategy interleaves one between every line.
                    if not any(re.sub(r'\s+', ' ', (c or '')).strip() for c in row):
                        continue
                    cell = row[col] if col < len(row) else None
                    text = unligature(re.sub(r'\s+', ' ', cell or '').strip())
                    # A new RECORD is signalled by a column to the LEFT filling
                    # in (the "1." / "2." index, or the stub column). Columns to
                    # the right wrap too, so their content means nothing here.
                    starts_record = any(re.sub(r'\s+', ' ', (row[i] or '')).strip()
                                        for i in range(min(col, len(row))))
                    if text and (not run or not starts_record):
                        run.append(text)
                        continue
                    if len(run) > 1:
                        joined = ' '.join(run)
                        if joined not in seen:
                            seen.add(joined)
                            out.append(joined)
                    run = [text] if text else []
                if len(run) > 1:
                    joined = ' '.join(run)
                    if joined not in seen:
                        seen.add(joined)
                        out.append(joined)
    return out


def main() -> None:
    subject, year, level = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    md = ROOT / 'examiner-reports' / subject / 'schemes' / f'{year}-{level}.md'
    if not md.exists():
        raise SystemExit(f'no scheme markdown at {md}')
    pdf = pdf_for(subject, year, level)
    if pdf is None:
        raise SystemExit(f'no marking-scheme PDF for {subject} {year} {level}')
    lines = cells(pdf)
    body = f'{START}\n' + '\n'.join(lines) + f'\n{END}\n'
    text = md.read_text(encoding='utf-8')
    if START in text:
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', text, flags=re.S)
    md.write_text(text.rstrip('\n') + '\n\n' + body, encoding='utf-8')
    print(f'{subject} {year} {level}: appended {len(lines)} table cells to {md.name}')


if __name__ == '__main__':
    main()
